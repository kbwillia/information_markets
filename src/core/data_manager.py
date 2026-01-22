"""
Unified Data Manager for both Kalshi and Polymarket.

This is the SINGLE entry point for all market data. It:
- Serves data from cache (fast)
- Refreshes cache in background (non-blocking)
- Provides unified API for both platforms
- Handles market matching between platforms using text + semantic similarity + end dates
"""
import threading
import time
import re
import json
from typing import Dict, List, Optional, Tuple, Callable
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
import difflib
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    SEMANTIC_AVAILABLE = True
except ImportError:
    SEMANTIC_AVAILABLE = False
    SentenceTransformer = None

from src.core.cache import MarketCache
from src.data_collectors.kalshi_client import KalshiClient
from src.data_collectors.polymarket_client import PolymarketClient
from src.config import Config


@dataclass
class MarketData:
    """Unified market data structure."""
    id: str
    platform: str
    title: str
    description: str
    yes_price: Optional[float]
    no_price: Optional[float]
    yes_bid: Optional[float]
    yes_ask: Optional[float]
    volume: Optional[float]
    liquidity: Optional[float]
    end_date: Optional[str]
    status: str
    category: Optional[str]
    raw_data: Dict
    
    @property
    def mid_price(self) -> Optional[float]:
        if self.yes_bid and self.yes_ask:
            return (self.yes_bid + self.yes_ask) / 2
        return self.yes_price
    
    @property
    def spread(self) -> Optional[float]:
        if self.yes_bid and self.yes_ask:
            return self.yes_ask - self.yes_bid
        return None


@dataclass
class MatchedMarket:
    """A market that exists on both platforms."""
    kalshi: MarketData
    polymarket: MarketData
    similarity_score: float  # Combined score (0-1)
    normalized_title: str
    text_similarity: float = 0.0  # Text-based similarity (0-1)
    semantic_similarity: float = 0.0  # Embedding-based similarity (0-1)
    end_date_match: bool = False  # Whether end dates are close
    end_date_diff_days: Optional[int] = None  # Days difference between end dates


class DataManager:
    """
    Central data manager that serves cached data and handles refresh.
    
    Usage Pattern:
        dm = DataManager()
        dm.start_background_refresh()  # Start background refresh
        
        # All these are INSTANT (read from cache)
        markets = dm.get_all_markets()
        price = dm.get_price('kalshi', 'TICKER')
        matched = dm.get_matched_markets()
        
        dm.stop_background_refresh()  # Cleanup
    """
    
    def __init__(self, kalshi_client: KalshiClient = None,
                 polymarket_client: PolymarketClient = None,
                 cache: MarketCache = None,
                 use_semantic_matching: bool = True,
                 semantic_model: str = 'all-MiniLM-L6-v2'):
        self.cache = cache or MarketCache()
        
        # Lazy initialization of clients (only when needed for refresh)
        self._kalshi_client = kalshi_client
        self._polymarket_client = polymarket_client
        
        # Background refresh control
        self._refresh_thread: Optional[threading.Thread] = None
        self._stop_refresh = threading.Event()
        self._refresh_interval = 10  # seconds
        
        # Market matching cache
        self._matched_markets: List[MatchedMarket] = []
        self._match_lock = threading.Lock()
        
        # Callbacks for price updates
        self._price_callbacks: List[Callable] = []
        
        # Semantic matching setup
        self.use_semantic_matching = use_semantic_matching and SEMANTIC_AVAILABLE
        self._semantic_model: Optional[SentenceTransformer] = None
        self._semantic_model_name = semantic_model
        self._embedding_cache: Dict[str, np.ndarray] = {}  # Cache embeddings
    
    @property
    def kalshi(self) -> KalshiClient:
        """Lazy-load Kalshi client."""
        if self._kalshi_client is None:
            self._kalshi_client = KalshiClient()
        return self._kalshi_client
    
    @property
    def polymarket(self) -> PolymarketClient:
        """Lazy-load Polymarket client."""
        if self._polymarket_client is None:
            self._polymarket_client = PolymarketClient()
        return self._polymarket_client
    
    # =========================================================================
    # PUBLIC API - These all read from cache (instant)
    # =========================================================================
    
    def get_all_markets(self, platform: str = None, 
                        allow_stale: bool = True) -> List[MarketData]:
        """Get all cached markets."""
        markets = []
        
        platforms = [platform] if platform else ['kalshi', 'polymarket']
        
        for p in platforms:
            cached = self.cache.get(p, 'markets', allow_stale=allow_stale)
            if cached:
                for m in cached:
                    markets.append(self._normalize_market(m, p))
        
        return markets
    
    def get_market(self, platform: str, market_id: str,
                   allow_stale: bool = True) -> Optional[MarketData]:
        """Get a specific market."""
        cached = self.cache.get(platform, 'market', market_id, allow_stale=allow_stale)
        if cached:
            return self._normalize_market(cached, platform)
        return None
    
    def get_price(self, platform: str, market_id: str,
                  allow_stale: bool = True) -> Optional[float]:
        """Get current price for a market."""
        cached = self.cache.get(platform, 'price', market_id, allow_stale=allow_stale)
        if cached:
            return cached.get('yes_price') or cached.get('price')
        
        # Fallback to orderbook
        orderbook = self.cache.get(platform, 'orderbook', market_id, allow_stale=allow_stale)
        if orderbook:
            return self._extract_price_from_orderbook(orderbook, platform)
        
        return None
    
    def get_orderbook(self, platform: str, market_id: str,
                      allow_stale: bool = True) -> Optional[Dict]:
        """Get orderbook for a market."""
        return self.cache.get(platform, 'orderbook', market_id, allow_stale=allow_stale)
    
    def get_price_history(self, platform: str, market_id: str,
                          minutes: int = 60) -> List[Dict]:
        """Get price history for a market."""
        return self.cache.get_price_history(market_id, platform, minutes)
    
    def get_matched_markets(self) -> List[MatchedMarket]:
        """Get markets that exist on both platforms."""
        with self._match_lock:
            return self._matched_markets.copy()
    
    def get_volume(self, platform: str, market_id: str) -> Optional[float]:
        """Get trading volume for a market."""
        market = self.get_market(platform, market_id)
        return market.volume if market else None
    
    def get_spread(self, platform: str, market_id: str) -> Optional[float]:
        """Get bid-ask spread for a market."""
        market = self.get_market(platform, market_id)
        return market.spread if market else None
    
    # =========================================================================
    # PRICE CALLBACK REGISTRATION
    # =========================================================================
    
    def on_price_update(self, callback: Callable[[str, str, float, float], None]):
        """
        Register callback for price updates.
        
        Callback signature: callback(platform, market_id, old_price, new_price)
        """
        self._price_callbacks.append(callback)
    
    def _notify_price_update(self, platform: str, market_id: str,
                             old_price: float, new_price: float):
        """Notify all registered callbacks of a price update."""
        for callback in self._price_callbacks:
            try:
                callback(platform, market_id, old_price, new_price)
            except Exception as e:
                print(f"Error in price callback: {e}")
    
    # =========================================================================
    # BACKGROUND REFRESH
    # =========================================================================
    
    def start_background_refresh(self, interval: float = 10):
        """Start background thread to refresh cache."""
        if self._refresh_thread and self._refresh_thread.is_alive():
            return
        
        self._refresh_interval = interval
        self._stop_refresh.clear()
        self._refresh_thread = threading.Thread(
            target=self._refresh_loop,
            daemon=True
        )
        self._refresh_thread.start()
        print(f"Background refresh started (interval: {interval}s)")
    
    def stop_background_refresh(self):
        """Stop background refresh thread."""
        self._stop_refresh.set()
        if self._refresh_thread:
            self._refresh_thread.join(timeout=5)
        print("Background refresh stopped")
    
    def _refresh_loop(self):
        """Main refresh loop."""
        while not self._stop_refresh.is_set():
            try:
                self.refresh_all()
            except Exception as e:
                print(f"Error in refresh loop: {e}")
            
            # Wait for interval or stop signal
            self._stop_refresh.wait(timeout=self._refresh_interval)
    
    def refresh_all(self):
        """Refresh all cached data."""
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(self._refresh_kalshi_markets),
                executor.submit(self._refresh_polymarket_markets),
            ]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Refresh error: {e}")
        
        # Update matched markets
        self._update_matched_markets()
    
    def _refresh_kalshi_markets(self):
        """Refresh Kalshi market data."""
        if not self.kalshi:
            print("Skipping Kalshi refresh: client not available (check API keys in .env)")
            return
        try:
            response = self.kalshi.get_markets(limit=200)
            markets = response.get('markets', []) if isinstance(response, dict) else []
            
            if markets:
                self.cache.set('kalshi', 'markets', markets)
                
                # Cache individual markets and record prices
                for m in markets:
                    ticker = m.get('ticker')
                    if ticker:
                        self.cache.set('kalshi', 'market', m, identifier=ticker)
                        
                        # Extract and record price
                        yes_price = m.get('yes_price', m.get('last_price'))
                        if yes_price:
                            # Kalshi uses cents (0-100), normalize to 0-1
                            price = yes_price / 100 if yes_price > 1 else yes_price
                            
                            # Check for price change
                            old_price = self.get_price('kalshi', ticker)
                            
                            self.cache.set('kalshi', 'price', 
                                          {'yes_price': price}, identifier=ticker)
                            self.cache.record_price(ticker, 'kalshi', price,
                                                   m.get('volume'))
                            
                            if old_price and abs(price - old_price) > 0.001:
                                self._notify_price_update('kalshi', ticker, 
                                                         old_price, price)
            
            print(f"Refreshed {len(markets)} Kalshi markets")
        except Exception as e:
            print(f"Error refreshing Kalshi: {e}")
    
    def _refresh_polymarket_markets(self):
        """Refresh Polymarket market data."""
        if not self.polymarket:
            print("Skipping Polymarket refresh: client not available")
            return
        try:
            response = self.polymarket.get_markets(limit=200)
            # Handle different response formats
            if isinstance(response, list):
                markets = response
            elif isinstance(response, dict):
                markets = response.get('markets', response.get('data', []))
            else:
                markets = []
            
            if markets:
                self.cache.set('polymarket', 'markets', markets)
                
                # Cache individual markets and record prices
                for m in markets:
                    market_id = m.get('id') or m.get('condition_id')
                    if market_id:
                        self.cache.set('polymarket', 'market', m, identifier=market_id)
                        
                        # Extract price (Polymarket uses 0-1)
                        # Handle different price field formats
                        yes_price = None
                        if isinstance(m, dict):
                            outcome_prices = m.get('outcomePrices')
                            
                            # Handle JSON string format (e.g., '["0", "0"]')
                            if isinstance(outcome_prices, str):
                                try:
                                    outcome_prices = json.loads(outcome_prices)
                                except (json.JSONDecodeError, ValueError):
                                    outcome_prices = []
                            
                            if outcome_prices and isinstance(outcome_prices, list) and len(outcome_prices) > 0:
                                yes_price = outcome_prices[0]
                            if yes_price is None:
                                yes_price = m.get('yes_price') or m.get('price')
                        
                        if yes_price is not None:
                            price = self._safe_price(yes_price, 'polymarket')
                            if price is None:
                                # Skip if price can't be converted
                                continue
                            
                            # Check for price change
                            old_price = self.get_price('polymarket', market_id)
                            
                            self.cache.set('polymarket', 'price',
                                          {'yes_price': price}, identifier=market_id)
                            self.cache.record_price(market_id, 'polymarket', price,
                                                   m.get('volume'))
                            
                            if old_price and abs(price - old_price) > 0.001:
                                self._notify_price_update('polymarket', market_id,
                                                         old_price, price)
            
            print(f"Refreshed {len(markets)} Polymarket markets")
        except Exception as e:
            print(f"Error refreshing Polymarket: {e}")
    
    def refresh_orderbook(self, platform: str, market_id: str):
        """Refresh orderbook for a specific market (on-demand)."""
        try:
            if platform == 'kalshi':
                orderbook = self.kalshi.get_orderbook(market_id)
            else:
                orderbook = self.polymarket.get_orderbook(market_id)
            
            self.cache.set(platform, 'orderbook', orderbook, identifier=market_id)
            return orderbook
        except Exception as e:
            print(f"Error refreshing orderbook: {e}")
            return None
    
    # =========================================================================
    # MARKET MATCHING
    # =========================================================================
    
    def _get_semantic_model(self) -> Optional[SentenceTransformer]:
        """Lazy-load semantic model."""
        if not self.use_semantic_matching:
            return None
        
        if self._semantic_model is None:
            try:
                print(f"Loading semantic model: {self._semantic_model_name}")
                self._semantic_model = SentenceTransformer(self._semantic_model_name)
                print("Semantic model loaded successfully")
            except Exception as e:
                print(f"Failed to load semantic model: {e}. Falling back to text-only matching.")
                self.use_semantic_matching = False
                return None
        
        return self._semantic_model
    
    def _get_embedding(self, text: str) -> Optional[np.ndarray]:
        """Get embedding for text, using cache."""
        if not self.use_semantic_matching:
            return None
        
        # Check cache first
        if text in self._embedding_cache:
            return self._embedding_cache[text]
        
        model = self._get_semantic_model()
        if model is None:
            return None
        
        try:
            embedding = model.encode(text, convert_to_numpy=True)
            self._embedding_cache[text] = embedding
            return embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
    
    def _semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts."""
        emb1 = self._get_embedding(text1)
        emb2 = self._get_embedding(text2)
        
        if emb1 is None or emb2 is None:
            return 0.0
        
        # Cosine similarity
        dot_product = np.dot(emb1, emb2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return float(similarity)
    
    def _normalize_title(self, title: str) -> str:
        """Normalize market title for matching."""
        # Lowercase
        title = title.lower()
        # Remove special characters
        title = re.sub(r'[^\w\s]', '', title)
        # Normalize whitespace
        title = ' '.join(title.split())
        # Remove common words
        stopwords = {'will', 'the', 'be', 'to', 'in', 'on', 'at', 'by', 'for', 'a', 'an'}
        words = [w for w in title.split() if w not in stopwords]
        return ' '.join(words)
    
    def _parse_end_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse end date string to datetime."""
        if not date_str:
            return None
        
        try:
            # Try ISO format first (with timezone)
            if 'T' in date_str:
                # Handle ISO format with or without timezone
                if date_str.endswith('Z'):
                    date_str_clean = date_str.replace('Z', '+00:00')
                elif '+' in date_str or date_str.count('-') >= 3:
                    # Already has timezone or is ISO format
                    date_str_clean = date_str
                else:
                    # ISO format without timezone
                    date_str_clean = date_str
                
                try:
                    return datetime.fromisoformat(date_str_clean.replace('Z', '+00:00'))
                except ValueError:
                    # Try without timezone
                    date_str_no_tz = date_str.split('+')[0].split('-')[0] if '-' in date_str else date_str
                    date_str_no_tz = date_str_no_tz.replace('Z', '').strip()
                    if date_str_no_tz:
                        return datetime.fromisoformat(date_str_no_tz)
            else:
                # Try other common formats
                for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%m/%d/%Y', '%Y-%m-%dT%H:%M:%S']:
                    try:
                        return datetime.strptime(date_str, fmt)
                    except ValueError:
                        continue
        except Exception as e:
            # If all parsing fails, return None
            pass
        
        return None
    
    def _end_dates_match(self, date1: Optional[str], date2: Optional[str], 
                        tolerance_days: int = 7) -> Tuple[bool, Optional[int]]:
        """
        Check if two end dates are close enough to be the same event.
        
        Returns:
            (match, days_difference)
        """
        dt1 = self._parse_end_date(date1)
        dt2 = self._parse_end_date(date2)
        
        if dt1 is None or dt2 is None:
            return (False, None)
        
        diff = abs((dt1 - dt2).days)
        return (diff <= tolerance_days, diff)
    
    def _update_matched_markets(self):
        """Find and cache matched markets between platforms using multi-factor matching."""
        kalshi_markets = self.get_all_markets('kalshi')
        poly_markets = self.get_all_markets('polymarket')
        
        if not kalshi_markets or not poly_markets:
            return
        
        # Build lookup by normalized title
        kalshi_lookup = {}
        for m in kalshi_markets:
            normalized = self._normalize_title(m.title)
            kalshi_lookup[normalized] = m
        
        matched = []
        
        # Pre-compute embeddings for all Polymarket markets (batch for efficiency)
        if self.use_semantic_matching:
            poly_titles = [pm.title for pm in poly_markets]
            # Embeddings will be cached automatically
        
        for pm in poly_markets:
            pm_normalized = self._normalize_title(pm.title)
            best_match = None
            best_combined_score = 0.0
            best_text_score = 0.0
            best_semantic_score = 0.0
            end_date_match = False
            end_date_diff = None
            
            # Try exact match first
            if pm_normalized in kalshi_lookup:
                km = kalshi_lookup[pm_normalized]
                text_score = 1.0
                semantic_score = 1.0 if not self.use_semantic_matching else self._semantic_similarity(pm.title, km.title)
                end_date_match, end_date_diff = self._end_dates_match(pm.end_date, km.end_date)
                
                # Combined score: text (40%) + semantic (40%) + end date (20%)
                combined = 0.4 * text_score + 0.4 * semantic_score + (0.2 if end_date_match else 0.0)
                
                matched.append(MatchedMarket(
                    kalshi=km,
                    polymarket=pm,
                    similarity_score=min(1.0, combined),
                    normalized_title=pm_normalized,
                    text_similarity=text_score,
                    semantic_similarity=semantic_score,
                    end_date_match=end_date_match,
                    end_date_diff_days=end_date_diff
                ))
                continue
            
            # Try fuzzy match with all factors
            for k_normalized, km in kalshi_lookup.items():
                # Text similarity
                text_score = difflib.SequenceMatcher(
                    None, pm_normalized, k_normalized
                ).ratio()
                
                # Semantic similarity
                semantic_score = 0.0
                if self.use_semantic_matching:
                    semantic_score = self._semantic_similarity(pm.title, km.title)
                
                # End date matching
                end_date_match, end_date_diff = self._end_dates_match(pm.end_date, km.end_date)
                
                # Combined score: text (40%) + semantic (40%) + end date (20%)
                combined = (0.4 * text_score + 
                           0.4 * semantic_score + 
                           (0.2 if end_date_match else 0.0))
                
                # Minimum thresholds: text > 0.6 OR semantic > 0.7, AND combined > 0.65
                if (text_score > 0.6 or semantic_score > 0.7) and combined > 0.65:
                    if combined > best_combined_score:
                        best_combined_score = combined
                        best_match = km
                        best_text_score = text_score
                        best_semantic_score = semantic_score
                        end_date_match = end_date_match
                        end_date_diff = end_date_diff
            
            if best_match:
                matched.append(MatchedMarket(
                    kalshi=best_match,
                    polymarket=pm,
                    similarity_score=min(1.0, best_combined_score),
                    normalized_title=pm_normalized,
                    text_similarity=best_text_score,
                    semantic_similarity=best_semantic_score,
                    end_date_match=end_date_match,
                    end_date_diff_days=end_date_diff
                ))
        
        with self._match_lock:
            self._matched_markets = matched
        
        # Print matching statistics
        exact_matches = sum(1 for m in matched if m.text_similarity == 1.0)
        semantic_boosted = sum(1 for m in matched if m.semantic_similarity > m.text_similarity)
        date_matched = sum(1 for m in matched if m.end_date_match)
        
        print(f"Found {len(matched)} matched markets "
              f"(exact: {exact_matches}, semantic-boosted: {semantic_boosted}, "
              f"date-matched: {date_matched})")
    
    # =========================================================================
    # HELPERS
    # =========================================================================
    
    def _normalize_market(self, raw: Dict, platform: str) -> MarketData:
        """Convert raw API response to MarketData."""
        if platform == 'kalshi':
            return MarketData(
                id=raw.get('ticker', ''),
                platform=platform,
                title=raw.get('title', ''),
                description=raw.get('subtitle', ''),
                yes_price=self._safe_price(raw.get('yes_price'), platform),
                no_price=self._safe_price(raw.get('no_price'), platform),
                yes_bid=self._safe_price(raw.get('yes_bid'), platform),
                yes_ask=self._safe_price(raw.get('yes_ask'), platform),
                volume=raw.get('volume'),
                liquidity=raw.get('open_interest'),
                end_date=raw.get('close_time'),
                status=raw.get('status', 'active'),
                category=raw.get('category'),
                raw_data=raw
            )
        else:  # polymarket
            outcome_prices = raw.get('outcomePrices', [])
            
            # Safely extract prices - handle various formats
            yes_price = None
            no_price = None
            
            if outcome_prices:
                # Handle JSON string format (e.g., '["0", "0"]')
                if isinstance(outcome_prices, str):
                    try:
                        outcome_prices = json.loads(outcome_prices)
                    except (json.JSONDecodeError, ValueError):
                        outcome_prices = []
                
                # Handle list format
                if isinstance(outcome_prices, list) and len(outcome_prices) > 0:
                    try:
                        yes_price_val = outcome_prices[0]
                        yes_price = self._safe_price(yes_price_val, platform)
                    except (ValueError, TypeError, IndexError):
                        pass
                
                if isinstance(outcome_prices, list) and len(outcome_prices) > 1:
                    try:
                        no_price_val = outcome_prices[1]
                        no_price = self._safe_price(no_price_val, platform)
                    except (ValueError, TypeError, IndexError):
                        pass
            
            # Fallback to other price fields
            if yes_price is None:
                yes_price = self._safe_price(raw.get('yes_price') or raw.get('price'), platform)
            
            return MarketData(
                id=raw.get('id') or raw.get('condition_id', ''),
                platform=platform,
                title=raw.get('question', raw.get('title', '')),
                description=raw.get('description', ''),
                yes_price=yes_price,
                no_price=no_price,
                yes_bid=None,  # Need orderbook for this
                yes_ask=None,
                volume=raw.get('volume'),
                liquidity=raw.get('liquidity'),
                end_date=raw.get('endDate'),
                status=raw.get('active', True) and 'active' or 'closed',
                category=raw.get('category'),
                raw_data=raw
            )
    
    def _safe_price(self, price, platform: str) -> Optional[float]:
        """Safely convert price to 0-1 scale."""
        if price is None:
            return None
        
        # Handle string representations
        if isinstance(price, str):
            # Skip if it looks like a list or other invalid format
            price_str = price.strip()
            if not price_str or price_str[0] in ['[', '{', '(']:
                return None
            try:
                price = float(price_str)
            except (ValueError, TypeError):
                return None
        else:
            try:
                price = float(price)
            except (ValueError, TypeError):
                return None
        
        if platform == 'kalshi' and price > 1:
            return price / 100  # Kalshi uses cents
        return price
    
    def _extract_price_from_orderbook(self, orderbook: Dict, 
                                      platform: str) -> Optional[float]:
        """Extract mid price from orderbook."""
        try:
            if platform == 'kalshi':
                yes_bids = orderbook.get('yes', {}).get('bids', [])
                yes_asks = orderbook.get('yes', {}).get('asks', [])
            else:
                yes_bids = orderbook.get('bids', [])
                yes_asks = orderbook.get('asks', [])
            
            best_bid = max(b['price'] for b in yes_bids) if yes_bids else None
            best_ask = min(a['price'] for a in yes_asks) if yes_asks else None
            
            if best_bid and best_ask:
                mid = (best_bid + best_ask) / 2
                return mid / 100 if platform == 'kalshi' and mid > 1 else mid
            
            return best_bid or best_ask
        except Exception:
            return None

