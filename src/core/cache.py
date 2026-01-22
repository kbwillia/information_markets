"""
SQLite-based caching layer for market data.

Minimizes API calls by caching data locally with configurable TTL.
This ensures API calls are NEVER the bottleneck - we always trade on cached data.
"""
import sqlite3
import json
import time
import threading
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class CacheEntry:
    """A single cache entry with metadata."""
    key: str
    value: Any
    timestamp: float
    ttl_seconds: float
    platform: str
    data_type: str  # 'market', 'orderbook', 'trades', 'price_history'
    
    @property
    def is_expired(self) -> bool:
        return time.time() > (self.timestamp + self.ttl_seconds)
    
    @property
    def age_seconds(self) -> float:
        return time.time() - self.timestamp


class MarketCache:
    """
    High-performance SQLite cache for market data.
    
    Design Philosophy:
    - All reads come from cache (microseconds)
    - Background threads refresh cache (doesn't block trading)
    - Stale data is still usable for certain operations
    - API calls only happen during refresh cycles
    """
    
    # Default TTL values (in seconds)
    TTL_MARKETS = 60        # Market list updates every minute
    TTL_ORDERBOOK = 5       # Orderbooks update every 5 seconds
    TTL_PRICE = 2           # Prices update every 2 seconds
    TTL_TRADES = 30         # Recent trades update every 30 seconds
    TTL_PRICE_HISTORY = 300 # Historical prices update every 5 minutes
    
    def __init__(self, db_path: str = "data/cache/market_cache.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._local = threading.local()
        self._init_db()
        
        # In-memory cache for ultra-fast reads (L1 cache)
        self._memory_cache: Dict[str, CacheEntry] = {}
        self._memory_lock = threading.RLock()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get thread-local database connection."""
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            self._local.conn = sqlite3.connect(
                str(self.db_path),
                check_same_thread=False
            )
            self._local.conn.row_factory = sqlite3.Row
            # Enable WAL mode for better concurrent access
            self._local.conn.execute("PRAGMA journal_mode=WAL")
            self._local.conn.execute("PRAGMA synchronous=NORMAL")
        return self._local.conn
    
    def _init_db(self):
        """Initialize database schema."""
        conn = self._get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                timestamp REAL NOT NULL,
                ttl_seconds REAL NOT NULL,
                platform TEXT NOT NULL,
                data_type TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_cache_platform_type 
            ON cache(platform, data_type)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_cache_timestamp 
            ON cache(timestamp)
        """)
        
        # Price history table for time series data
        conn.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                market_id TEXT NOT NULL,
                platform TEXT NOT NULL,
                price REAL NOT NULL,
                volume REAL,
                timestamp REAL NOT NULL,
                UNIQUE(market_id, platform, timestamp)
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_price_history_market_time 
            ON price_history(market_id, platform, timestamp DESC)
        """)
        conn.commit()
    
    def _make_key(self, platform: str, data_type: str, identifier: str = "") -> str:
        """Generate cache key."""
        return f"{platform}:{data_type}:{identifier}".strip(":")
    
    def get(self, platform: str, data_type: str, identifier: str = "",
            allow_stale: bool = False) -> Optional[Any]:
        """
        Get cached data.
        
        Args:
            platform: 'kalshi' or 'polymarket'
            data_type: Type of data ('markets', 'orderbook', 'price', etc.)
            identifier: Market ID or ticker (optional)
            allow_stale: If True, return expired data rather than None
        
        Returns:
            Cached data or None if not found/expired
        """
        key = self._make_key(platform, data_type, identifier)
        
        # Check L1 (memory) cache first
        with self._memory_lock:
            if key in self._memory_cache:
                entry = self._memory_cache[key]
                if not entry.is_expired or allow_stale:
                    return entry.value
        
        # Check L2 (SQLite) cache
        conn = self._get_connection()
        row = conn.execute(
            "SELECT value, timestamp, ttl_seconds FROM cache WHERE key = ?",
            (key,)
        ).fetchone()
        
        if row:
            is_expired = time.time() > (row['timestamp'] + row['ttl_seconds'])
            if not is_expired or allow_stale:
                value = json.loads(row['value'])
                # Populate L1 cache
                with self._memory_lock:
                    self._memory_cache[key] = CacheEntry(
                        key=key,
                        value=value,
                        timestamp=row['timestamp'],
                        ttl_seconds=row['ttl_seconds'],
                        platform=platform,
                        data_type=data_type
                    )
                return value
        
        return None
    
    def set(self, platform: str, data_type: str, value: Any,
            identifier: str = "", ttl_seconds: float = None):
        """
        Set cached data.
        
        Args:
            platform: 'kalshi' or 'polymarket'
            data_type: Type of data
            value: Data to cache
            identifier: Market ID or ticker
            ttl_seconds: TTL override (uses default if not specified)
        """
        key = self._make_key(platform, data_type, identifier)
        timestamp = time.time()
        
        # Determine TTL
        if ttl_seconds is None:
            ttl_map = {
                'markets': self.TTL_MARKETS,
                'orderbook': self.TTL_ORDERBOOK,
                'price': self.TTL_PRICE,
                'trades': self.TTL_TRADES,
                'price_history': self.TTL_PRICE_HISTORY,
            }
            ttl_seconds = ttl_map.get(data_type, 60)
        
        # Store in L1 (memory) cache
        entry = CacheEntry(
            key=key,
            value=value,
            timestamp=timestamp,
            ttl_seconds=ttl_seconds,
            platform=platform,
            data_type=data_type
        )
        with self._memory_lock:
            self._memory_cache[key] = entry
        
        # Store in L2 (SQLite) cache
        conn = self._get_connection()
        conn.execute("""
            INSERT OR REPLACE INTO cache 
            (key, value, timestamp, ttl_seconds, platform, data_type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (key, json.dumps(value), timestamp, ttl_seconds, platform, data_type))
        conn.commit()
    
    def record_price(self, market_id: str, platform: str, price: float,
                    volume: float = None, timestamp: float = None):
        """Record a price point for historical analysis."""
        if timestamp is None:
            timestamp = time.time()
        
        conn = self._get_connection()
        try:
            conn.execute("""
                INSERT OR REPLACE INTO price_history 
                (market_id, platform, price, volume, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (market_id, platform, price, volume, timestamp))
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # Duplicate timestamp, ignore
    
    def get_price_history(self, market_id: str, platform: str,
                         minutes: int = 60) -> List[Dict]:
        """Get recent price history for a market."""
        cutoff = time.time() - (minutes * 60)
        
        conn = self._get_connection()
        rows = conn.execute("""
            SELECT price, volume, timestamp FROM price_history
            WHERE market_id = ? AND platform = ? AND timestamp > ?
            ORDER BY timestamp ASC
        """, (market_id, platform, cutoff)).fetchall()
        
        return [
            {'price': r['price'], 'volume': r['volume'], 'timestamp': r['timestamp']}
            for r in rows
        ]
    
    def get_all_prices_at_time(self, platform: str, 
                               timestamp: float = None,
                               tolerance_seconds: float = 5.0) -> Dict[str, float]:
        """Get all market prices at a specific time."""
        if timestamp is None:
            timestamp = time.time()
        
        conn = self._get_connection()
        rows = conn.execute("""
            SELECT market_id, price, MAX(timestamp) as ts 
            FROM price_history
            WHERE platform = ? 
              AND timestamp BETWEEN ? AND ?
            GROUP BY market_id
        """, (platform, timestamp - tolerance_seconds, timestamp + tolerance_seconds)).fetchall()
        
        return {r['market_id']: r['price'] for r in rows}
    
    def invalidate(self, platform: str = None, data_type: str = None,
                   identifier: str = None):
        """Invalidate cache entries matching the criteria."""
        conditions = []
        params = []
        
        if platform:
            conditions.append("platform = ?")
            params.append(platform)
        if data_type:
            conditions.append("data_type = ?")
            params.append(data_type)
        if identifier:
            conditions.append("key LIKE ?")
            params.append(f"%:{identifier}")
        
        # Clear from memory cache
        with self._memory_lock:
            keys_to_remove = []
            for key, entry in self._memory_cache.items():
                if platform and entry.platform != platform:
                    continue
                if data_type and entry.data_type != data_type:
                    continue
                if identifier and identifier not in key:
                    continue
                keys_to_remove.append(key)
            for key in keys_to_remove:
                del self._memory_cache[key]
        
        # Clear from SQLite cache
        if conditions:
            conn = self._get_connection()
            conn.execute(
                f"DELETE FROM cache WHERE {' AND '.join(conditions)}",
                params
            )
            conn.commit()
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics."""
        conn = self._get_connection()
        
        stats = {
            'memory_entries': len(self._memory_cache),
            'db_entries': conn.execute("SELECT COUNT(*) FROM cache").fetchone()[0],
            'price_history_entries': conn.execute(
                "SELECT COUNT(*) FROM price_history"
            ).fetchone()[0],
            'by_platform': {},
            'by_type': {}
        }
        
        # Count by platform
        for row in conn.execute(
            "SELECT platform, COUNT(*) as cnt FROM cache GROUP BY platform"
        ).fetchall():
            stats['by_platform'][row['platform']] = row['cnt']
        
        # Count by type
        for row in conn.execute(
            "SELECT data_type, COUNT(*) as cnt FROM cache GROUP BY data_type"
        ).fetchall():
            stats['by_type'][row['data_type']] = row['cnt']
        
        return stats
    
    def cleanup_expired(self):
        """Remove expired entries from the database."""
        now = time.time()
        
        # Clean memory cache
        with self._memory_lock:
            keys_to_remove = [
                key for key, entry in self._memory_cache.items()
                if entry.is_expired
            ]
            for key in keys_to_remove:
                del self._memory_cache[key]
        
        # Clean SQLite cache
        conn = self._get_connection()
        conn.execute(
            "DELETE FROM cache WHERE timestamp + ttl_seconds < ?",
            (now,)
        )
        conn.commit()
    
    def cleanup_old_price_history(self, days: int = 7):
        """Remove old price history data."""
        cutoff = time.time() - (days * 24 * 60 * 60)
        conn = self._get_connection()
        conn.execute("DELETE FROM price_history WHERE timestamp < ?", (cutoff,))
        conn.commit()

