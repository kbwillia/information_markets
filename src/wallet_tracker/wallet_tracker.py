"""Track and analyze wallet performance across platforms."""
import os
import pandas as pd
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
from collections import defaultdict
import sqlite3

from src.data_collectors.kalshi_client import KalshiClient
from src.data_collectors.polymarket_client import PolymarketClient


class WalletTracker:
    """Track wallet addresses and their trading performance."""
    
    def __init__(self, db_path: str = "data/wallets.db"):
        self.db_path = db_path
        # Ensure the data directory exists
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        # Initialize API clients lazily (only when needed)
        # This allows WalletTracker to work even without API credentials
        self._kalshi = None
        self._polymarket = None
        
        self._init_database()
    
    @property
    def kalshi(self):
        """Lazy-load Kalshi client."""
        if self._kalshi is None:
            try:
                self._kalshi = KalshiClient()
            except Exception as e:
                print(f"Warning: Could not initialize Kalshi client: {e}")
                print("WalletTracker will work but Kalshi features will be unavailable")
                self._kalshi = None
        return self._kalshi
    
    @property
    def polymarket(self):
        """Lazy-load Polymarket client."""
        if self._polymarket is None:
            try:
                self._polymarket = PolymarketClient()
            except Exception as e:
                print(f"Warning: Could not initialize Polymarket client: {e}")
                print("WalletTracker will work but Polymarket features will be unavailable")
                self._polymarket = None
        return self._polymarket
    
    def _init_database(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wallets (
                address TEXT PRIMARY KEY,
                platform TEXT,
                first_seen TIMESTAMP,
                last_seen TIMESTAMP,
                total_trades INTEGER DEFAULT 0,
                total_profit REAL DEFAULT 0.0,
                win_rate REAL DEFAULT 0.0
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wallet_address TEXT,
                platform TEXT,
                market_id TEXT,
                side TEXT,
                action TEXT,
                price REAL,
                quantity INTEGER,
                timestamp TIMESTAMP,
                profit REAL,
                FOREIGN KEY (wallet_address) REFERENCES wallets(address)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wallet_groups (
                group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                created_at TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wallet_group_members (
                group_id INTEGER,
                wallet_address TEXT,
                added_at TIMESTAMP,
                PRIMARY KEY (group_id, wallet_address),
                FOREIGN KEY (group_id) REFERENCES wallet_groups(group_id),
                FOREIGN KEY (wallet_address) REFERENCES wallets(address)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_wallet(self, address: str, platform: str):
        """Add a wallet to tracking."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR IGNORE INTO wallets (address, platform, first_seen, last_seen)
            VALUES (?, ?, ?, ?)
        """, (address, platform, datetime.now(), datetime.now()))
        
        cursor.execute("""
            UPDATE wallets SET last_seen = ? WHERE address = ?
        """, (datetime.now(), address))
        
        conn.commit()
        conn.close()
    
    def record_trade(self, wallet_address: str, platform: str, market_id: str,
                    side: str, action: str, price: float, quantity: int,
                    profit: float = None):
        """Record a trade for a wallet."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO trades (wallet_address, platform, market_id, side, action,
                              price, quantity, timestamp, profit)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (wallet_address, platform, market_id, side, action, price, quantity,
              datetime.now(), profit))
        
        # Update wallet stats
        cursor.execute("""
            UPDATE wallets 
            SET total_trades = total_trades + 1,
                total_profit = total_profit + COALESCE(?, 0)
            WHERE address = ?
        """, (profit, wallet_address))
        
        # Recalculate win rate
        cursor.execute("""
            SELECT COUNT(*), SUM(CASE WHEN profit > 0 THEN 1 ELSE 0 END)
            FROM trades
            WHERE wallet_address = ? AND profit IS NOT NULL
        """, (wallet_address,))
        
        result = cursor.fetchone()
        if result and result[0] > 0:
            win_rate = result[1] / result[0]
            cursor.execute("""
                UPDATE wallets SET win_rate = ? WHERE address = ?
            """, (win_rate, wallet_address))
        
        conn.commit()
        conn.close()
    
    def get_wallet_stats(self, address: str) -> Dict:
        """Get statistics for a wallet."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM wallets WHERE address = ?
        """, (address,))
        
        wallet = cursor.fetchone()
        if not wallet:
            conn.close()
            return None
        
        cursor.execute("""
            SELECT COUNT(*), SUM(profit), AVG(profit), 
                   MAX(profit), MIN(profit)
            FROM trades
            WHERE wallet_address = ? AND profit IS NOT NULL
        """, (address,))
        
        trade_stats = cursor.fetchone()
        
        conn.close()
        
        return {
            "address": wallet[0],
            "platform": wallet[1],
            "first_seen": wallet[2],
            "last_seen": wallet[3],
            "total_trades": wallet[4],
            "total_profit": wallet[5],
            "win_rate": wallet[6],
            "avg_profit": trade_stats[2] if trade_stats else 0,
            "max_profit": trade_stats[3] if trade_stats else 0,
            "min_profit": trade_stats[4] if trade_stats else 0,
        }
    
    def get_winning_wallets(self, min_trades: int = 10, min_win_rate: float = 0.6,
                           min_profit: float = 0.0, limit: int = 100) -> List[Dict]:
        """Get wallets with high win rates and profits."""
        conn = sqlite3.connect(self.db_path)
        
        query = """
            SELECT * FROM wallets
            WHERE total_trades >= ? 
            AND win_rate >= ?
            AND total_profit >= ?
            ORDER BY win_rate DESC, total_profit DESC
            LIMIT ?
        """
        
        df = pd.read_sql_query(query, conn, params=(min_trades, min_win_rate, min_profit, limit))
        conn.close()
        
        return df.to_dict('records')
    
    def get_losing_wallets(self, min_trades: int = 10, max_win_rate: float = 0.4,
                          max_profit: float = 0.0, limit: int = 100) -> List[Dict]:
        """Get wallets with low win rates and losses."""
        conn = sqlite3.connect(self.db_path)
        
        query = """
            SELECT * FROM wallets
            WHERE total_trades >= ?
            AND win_rate <= ?
            AND total_profit <= ?
            ORDER BY win_rate ASC, total_profit ASC
            LIMIT ?
        """
        
        df = pd.read_sql_query(query, conn, params=(min_trades, max_win_rate, max_profit, limit))
        conn.close()
        
        return df.to_dict('records')
    
    def create_wallet_group(self, name: str, wallet_addresses: List[str]) -> int:
        """Create a group of wallets."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO wallet_groups (name, created_at)
            VALUES (?, ?)
        """, (name, datetime.now()))
        
        group_id = cursor.lastrowid
        
        for address in wallet_addresses:
            cursor.execute("""
                INSERT OR IGNORE INTO wallet_group_members (group_id, wallet_address, added_at)
                VALUES (?, ?, ?)
            """, (group_id, address, datetime.now()))
        
        conn.commit()
        conn.close()
        
        return group_id
    
    def get_group_stats(self, group_id: int) -> Dict:
        """Get aggregated statistics for a wallet group."""
        conn = sqlite3.connect(self.db_path)
        
        query = """
            SELECT 
                COUNT(DISTINCT w.address) as wallet_count,
                SUM(w.total_trades) as total_trades,
                SUM(w.total_profit) as total_profit,
                AVG(w.win_rate) as avg_win_rate
            FROM wallet_groups wg
            JOIN wallet_group_members wgm ON wg.group_id = wgm.group_id
            JOIN wallets w ON wgm.wallet_address = w.address
            WHERE wg.group_id = ?
        """
        
        df = pd.read_sql_query(query, conn, params=(group_id,))
        conn.close()
        
        if df.empty:
            return None
        
        return df.iloc[0].to_dict()
    
    def get_recent_trades(self, wallet_address: str, limit: int = 50) -> pd.DataFrame:
        """Get recent trades for a wallet."""
        conn = sqlite3.connect(self.db_path)
        
        query = """
            SELECT * FROM trades
            WHERE wallet_address = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """
        
        df = pd.read_sql_query(query, conn, params=(wallet_address, limit))
        conn.close()
        
        return df
    
    def find_correlated_wallets(self, wallet_address: str, 
                               correlation_threshold: float = 0.7) -> List[str]:
        """Find wallets that trade similarly to the given wallet."""
        conn = sqlite3.connect(self.db_path)
        
        # Get markets this wallet trades
        query = """
            SELECT DISTINCT market_id FROM trades
            WHERE wallet_address = ?
        """
        target_markets = pd.read_sql_query(query, conn, params=(wallet_address,))
        target_markets_set = set(target_markets['market_id'].values)
        
        # Find other wallets trading in same markets
        query = """
            SELECT wallet_address, COUNT(DISTINCT market_id) as common_markets
            FROM trades
            WHERE market_id IN ({})
            AND wallet_address != ?
            GROUP BY wallet_address
        """.format(','.join(['?'] * len(target_markets_set)))
        
        params = list(target_markets_set) + [wallet_address]
        correlated = pd.read_sql_query(query, conn, params=params)
        
        # Calculate correlation based on common markets
        total_markets = len(target_markets_set)
        correlated['correlation'] = correlated['common_markets'] / total_markets
        
        correlated = correlated[correlated['correlation'] >= correlation_threshold]
        conn.close()
        
        return correlated['wallet_address'].tolist()

