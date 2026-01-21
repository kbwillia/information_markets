"""Polymarket API client for market data and trading."""
import requests
from typing import Dict, List, Optional
from datetime import datetime

from src.config import Config


class PolymarketClient:
    """Client for interacting with Polymarket API."""
    
    def __init__(self, api_key: str = None, api_secret: str = None, api_passphrase: str = None, 
                 private_key: str = None, base_url: str = None):
        self.api_key = api_key or Config.POLYMARKET_API_KEY
        self.api_secret = api_secret or Config.POLYMARKET_API_SECRET
        self.api_passphrase = api_passphrase or Config.POLYMARKET_API_PASSPHRASE
        self.private_key = private_key or Config.POLYMARKET_PRIVATE_KEY
        # Use provided base_url, or default to Data API
        self.base_url = base_url or Config.POLYMARKET_BASE_URL
        # Store all API URLs for easy access
        self.clob_url = Config.POLYMARKET_CLOB_URL
        self.gamma_url = Config.POLYMARKET_GAMMA_URL
        self.data_url = Config.POLYMARKET_DATA_URL
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}"
            })
    
    def _request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict:
        """Make request to Polymarket API."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    def get_markets(self, limit: int = 100, offset: int = 0) -> Dict:
        """Get available markets."""
        result = self._request("GET", "/markets", {
            "limit": limit,
            "offset": offset
        })
        # Polymarket returns data in 'data' field, normalize to 'markets' for consistency
        if isinstance(result, dict) and 'data' in result and 'markets' not in result:
            result['markets'] = result.pop('data')
        return result
    
    def get_market(self, market_id: str) -> Dict:
        """Get specific market by ID."""
        return self._request("GET", f"/markets/{market_id}")
    
    def get_orderbook(self, market_id: str) -> Dict:
        """Get orderbook for a market."""
        return self._request("GET", f"/markets/{market_id}/orderbook")
    
    def get_market_trades(self, market_id: str, limit: int = 100) -> Dict:
        """Get recent trades for a market (CLOB API)."""
        original_url = self.base_url
        self.use_clob_api()
        try:
            return self._request("GET", f"/markets/{market_id}/trades", {
                "limit": limit
            })
        finally:
            self.base_url = original_url
    
    def get_user_positions(self, user: str = None, market: List[str] = None, 
                          event_id: List[int] = None, size_threshold: float = 1.0,
                          redeemable: bool = False, mergeable: bool = False,
                          limit: int = 100, offset: int = 0,
                          sort_by: str = "TOKENS", sort_direction: str = "DESC",
                          title: str = None) -> Dict:
        """
        Get user positions from Data API.
        
        Args:
            user: User address (0x-prefixed, 40 hex chars) - REQUIRED
            market: Comma-separated list of condition IDs (mutually exclusive with event_id)
            event_id: Comma-separated list of event IDs (mutually exclusive with market)
            size_threshold: Minimum size threshold (default: 1.0)
            redeemable: Filter for redeemable positions (default: False)
            mergeable: Filter for mergeable positions (default: False)
            limit: Number of results (0-500, default: 100)
            offset: Pagination offset (0-10000, default: 0)
            sort_by: Sort field (CURRENT, INITIAL, TOKENS, CASHPNL, PERCENTPNL, TITLE, RESOLVING, PRICE, AVGPRICE)
            sort_direction: Sort direction (ASC, DESC, default: DESC)
            title: Filter by title (max 100 chars)
        
        Returns:
            Dict with position data
        """
        if not user:
            raise ValueError("user parameter is required (user address)")
        
        params = {
            "user": user,
            "sizeThreshold": size_threshold,
            "redeemable": redeemable,
            "mergeable": mergeable,
            "limit": limit,
            "offset": offset,
            "sortBy": sort_by,
            "sortDirection": sort_direction
        }
        
        if market:
            params["market"] = ",".join(market) if isinstance(market, list) else market
        elif event_id:
            params["eventId"] = ",".join(map(str, event_id)) if isinstance(event_id, list) else str(event_id)
        
        if title:
            params["title"] = title[:100]  # Enforce max length
        
        # Use Data API for positions
        original_url = self.base_url
        self.use_data_api()
        try:
            url = f"{self.base_url}/positions"
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        finally:
            self.base_url = original_url
    
    def get_user_balance(self) -> Dict:
        """
        Get user balance (requires authentication).
        
        Note: Balance endpoint location may vary. This method tries multiple APIs and endpoints.
        """
        # Try different possible endpoints on current API
        endpoints = ["/balance", "/user/balance", "/v1/balance", "/api/v1/balance", "/portfolio/balance"]
        last_error = None
        
        # Try current API first
        for endpoint in endpoints:
            try:
                return self._request("GET", endpoint)
            except Exception as e:
                last_error = e
                continue
        
        # If current API failed, try CLOB API (balance might be there)
        if self.base_url != self.clob_url:
            original_url = self.base_url
            self.use_clob_api()
            try:
                for endpoint in endpoints:
                    try:
                        return self._request("GET", endpoint)
                    except Exception as e:
                        last_error = e
                        continue
            finally:
                self.base_url = original_url
        
        # If all endpoints fail, raise the last error
        raise last_error if last_error else Exception("Could not find valid balance endpoint")
    
    def place_order(self, market_id: str, side: str, size: float, 
                   price: float, order_type: str = "LIMIT") -> Dict:
        """
        Place an order.
        
        Args:
            market_id: Market identifier
            side: 'BUY' or 'SELL'
            size: Order size
            price: Order price (0-1 for probability)
            order_type: 'LIMIT' or 'MARKET'
        """
        order_data = {
            "market": market_id,
            "side": side,
            "size": size,
            "price": price,
            "type": order_type
        }
        return self._request("POST", "/orders", data=order_data)
    
    def cancel_order(self, order_id: str) -> Dict:
        """Cancel an order."""
        return self._request("DELETE", f"/orders/{order_id}")
    
    def get_order_status(self, order_id: str) -> Dict:
        """Get status of an order."""
        return self._request("GET", f"/orders/{order_id}")
    
    def get_market_prices(self, market_id: str) -> Dict:
        """Get current market prices."""
        orderbook = self.get_orderbook(market_id)
        # Extract best bid/ask from orderbook
        bids = orderbook.get("bids", [])
        asks = orderbook.get("asks", [])
        
        best_bid = max(bids, key=lambda x: x["price"]) if bids else None
        best_ask = min(asks, key=lambda x: x["price"]) if asks else None
        
        return {
            "best_bid": best_bid,
            "best_ask": best_ask,
            "spread": best_ask["price"] - best_bid["price"] if (best_bid and best_ask) else None
        }
    
    def use_clob_api(self):
        """Switch to CLOB API (for order management, prices, and order books)."""
        self.base_url = self.clob_url
    
    def use_gamma_api(self):
        """Switch to Gamma API (for market discovery, metadata, and events)."""
        self.base_url = self.gamma_url
    
    def use_data_api(self):
        """Switch to Data API (for user positions, activity, and history)."""
        self.base_url = self.data_url
    
    # ========================================================================
    # GAMMA API - Market Discovery, Metadata, and Events
    # ========================================================================
    
    def get_events(self, limit: int = 100, offset: int = 0) -> Dict:
        """Get list of events (an event can contain multiple markets)."""
        original_url = self.base_url
        self.use_gamma_api()
        try:
            return self._request("GET", "/events", {
                "limit": limit,
                "offset": offset
            })
        finally:
            self.base_url = original_url
    
    def get_event(self, event_id: str) -> Dict:
        """Get details for a specific event."""
        original_url = self.base_url
        self.use_gamma_api()
        try:
            return self._request("GET", f"/events/{event_id}")
        finally:
            self.base_url = original_url
    
    def get_categories(self) -> Dict:
        """List all market categories (Politics, Crypto, Pop Culture, etc.)."""
        original_url = self.base_url
        self.use_gamma_api()
        try:
            return self._request("GET", "/categories")
        finally:
            self.base_url = original_url
    
    def get_tags(self) -> Dict:
        """Get tags used for filtering markets."""
        original_url = self.base_url
        self.use_gamma_api()
        try:
            return self._request("GET", "/tags")
        finally:
            self.base_url = original_url
    
    def search(self, query: str, limit: int = 100, offset: int = 0) -> Dict:
        """Search for specific markets or events by keywords."""
        original_url = self.base_url
        self.use_gamma_api()
        try:
            return self._request("GET", "/search", {
                "q": query,
                "limit": limit,
                "offset": offset
            })
        finally:
            self.base_url = original_url
    
    def get_notifications(self, limit: int = 100, offset: int = 0) -> Dict:
        """Fetch system-wide notifications or market updates."""
        original_url = self.base_url
        self.use_gamma_api()
        try:
            return self._request("GET", "/notifications", {
                "limit": limit,
                "offset": offset
            })
        finally:
            self.base_url = original_url
    
    def get_resolution_requests(self, limit: int = 100, offset: int = 0) -> Dict:
        """See markets currently pending resolution."""
        original_url = self.base_url
        self.use_gamma_api()
        try:
            return self._request("GET", "/resolution-requests", {
                "limit": limit,
                "offset": offset
            })
        finally:
            self.base_url = original_url
    
    def get_series(self, limit: int = 100, offset: int = 0) -> Dict:
        """Fetches 'Series' groupings (e.g., all 2026 election events)."""
        original_url = self.base_url
        self.use_gamma_api()
        try:
            return self._request("GET", "/series", {
                "limit": limit,
                "offset": offset
            })
        finally:
            self.base_url = original_url
    
    def get_sports(self) -> Dict:
        """Lists available sports for betting."""
        original_url = self.base_url
        self.use_gamma_api()
        try:
            return self._request("GET", "/sports")
        finally:
            self.base_url = original_url
    
    def get_teams(self) -> Dict:
        """Fetches team metadata, abbreviations, and league info."""
        original_url = self.base_url
        self.use_gamma_api()
        try:
            return self._request("GET", "/teams")
        finally:
            self.base_url = original_url
    
    def get_leagues(self) -> Dict:
        """Lists supported sports leagues."""
        original_url = self.base_url
        self.use_gamma_api()
        try:
            return self._request("GET", "/leagues")
        finally:
            self.base_url = original_url
    
    def get_comments(self, market_id: str = None, event_id: str = None, limit: int = 100, offset: int = 0) -> Dict:
        """Fetches comment threads for a specific market or event."""
        original_url = self.base_url
        self.use_gamma_api()
        try:
            params = {
                "limit": limit,
                "offset": offset
            }
            if market_id:
                params["market"] = market_id
            elif event_id:
                params["event"] = event_id
            return self._request("GET", "/comments", params)
        finally:
            self.base_url = original_url
    
    def get_comment(self, comment_id: str) -> Dict:
        """Get details for a specific comment thread."""
        original_url = self.base_url
        self.use_gamma_api()
        try:
            return self._request("GET", f"/comments/{comment_id}")
        finally:
            self.base_url = original_url
    
    def get_profile(self, address: str) -> Dict:
        """Get social profile data for a specific wallet (username, bio)."""
        original_url = self.base_url
        self.use_gamma_api()
        try:
            return self._request("GET", f"/profiles/{address}")
        finally:
            self.base_url = original_url
    
    def get_health(self) -> Dict:
        """Status check for the Gamma service."""
        original_url = self.base_url
        self.use_gamma_api()
        try:
            return self._request("GET", "/health")
        finally:
            self.base_url = original_url
    
    # ========================================================================
    # DATA API - Analytics, Stats, and User Data
    # ========================================================================
    
    def get_global_stats(self) -> Dict:
        """Get total volume, active users, and TVL across the platform."""
        original_url = self.base_url
        self.use_data_api()
        try:
            return self._request("GET", "/stats/global")
        finally:
            self.base_url = original_url
    
    def get_daily_stats(self, days: int = 30) -> Dict:
        """Get time-series data of daily volume and trades."""
        original_url = self.base_url
        self.use_data_api()
        try:
            return self._request("GET", "/stats/daily", {
                "days": days
            })
        finally:
            self.base_url = original_url
    
    def get_market_volume(self, market_id: str) -> Dict:
        """Get historical volume for a specific market."""
        original_url = self.base_url
        self.use_data_api()
        try:
            return self._request("GET", f"/markets/{market_id}/volume")
        finally:
            self.base_url = original_url
    
    def get_market_holders(self, market_id: str) -> Dict:
        """Get data on the number of unique holders for a market's tokens."""
        original_url = self.base_url
        self.use_data_api()
        try:
            return self._request("GET", f"/markets/{market_id}/holders")
        finally:
            self.base_url = original_url
    
    def get_leaderboard(self, limit: int = 100, offset: int = 0) -> Dict:
        """Get the top-performing traders by PnL (Profit and Loss)."""
        original_url = self.base_url
        self.use_data_api()
        try:
            return self._request("GET", "/leaderboard", {
                "limit": limit,
                "offset": offset
            })
        finally:
            self.base_url = original_url
    
    def get_user_activity(self, user_address: str, limit: int = 100, offset: int = 0) -> Dict:
        """Fetch the public trading history for a specific wallet address."""
        original_url = self.base_url
        self.use_data_api()
        try:
            return self._request("GET", f"/user/{user_address}/activity", {
                "limit": limit,
                "offset": offset
            })
        finally:
            self.base_url = original_url
    
    def get_user_profit(self, user_address: str) -> Dict:
        """Fetch PnL statistics for a specific wallet address."""
        original_url = self.base_url
        self.use_data_api()
        try:
            return self._request("GET", f"/user/{user_address}/profit")
        finally:
            self.base_url = original_url
    
    def get_user_value(self, user_address: str) -> Dict:
        """Fetch the current net worth/value of a user's total portfolio."""
        original_url = self.base_url
        self.use_data_api()
        try:
            return self._request("GET", f"/value", params={"user": user_address})
        finally:
            self.base_url = original_url
    
    def get_user_pnl(self, user_address: str) -> Dict:
        """Historical Profit and Loss tracking for a specific wallet."""
        original_url = self.base_url
        self.use_data_api()
        try:
            return self._request("GET", f"/pnl", params={"user": user_address})
        finally:
            self.base_url = original_url
    
    def get_trades(self, user: str = None, market: str = None, side: str = None, 
                   limit: int = 100, offset: int = 0) -> Dict:
        """
        List of all trades. Can be filtered by user, market, or side.
        
        Args:
            user: Filter by user address
            market: Filter by market/condition ID
            side: Filter by side (YES/NO)
            limit: Number of results
            offset: Pagination offset
        """
        original_url = self.base_url
        self.use_data_api()
        try:
            params = {
                "limit": limit,
                "offset": offset
            }
            if user:
                params["user"] = user
            if market:
                params["market"] = market
            if side:
                params["side"] = side
            return self._request("GET", "/trades", params)
        finally:
            self.base_url = original_url
    
    def get_activity(self, user: str = None, limit: int = 100, offset: int = 0) -> Dict:
        """
        General account activity (includes trades, but also 'Splits,' 'Merges,' and 'Redemptions').
        
        Args:
            user: Filter by user address
            limit: Number of results
            offset: Pagination offset
        """
        original_url = self.base_url
        self.use_data_api()
        try:
            params = {
                "limit": limit,
                "offset": offset
            }
            if user:
                params["user"] = user
            return self._request("GET", "/activity", params)
        finally:
            self.base_url = original_url
    
    def get_orders_history(self, user: str = None, limit: int = 100, offset: int = 0) -> Dict:
        """
        (Historical) Fetches past order history (distinct from the CLOB 'Open Orders' endpoint).
        
        Args:
            user: Filter by user address
            limit: Number of results
            offset: Pagination offset
        """
        original_url = self.base_url
        self.use_data_api()
        try:
            params = {
                "limit": limit,
                "offset": offset
            }
            if user:
                params["user"] = user
            return self._request("GET", "/orders", params)
        finally:
            self.base_url = original_url
    
    def get_market_stats(self, condition_id: str) -> Dict:
        """Aggregated volume and liquidity stats for a specific condition."""
        original_url = self.base_url
        self.use_data_api()
        try:
            return self._request("GET", f"/stats/market/{condition_id}")
        finally:
            self.base_url = original_url
    
    # ========================================================================
    # CLOB API - Order Management (COMMENTED OUT FOR NOW)
    # ========================================================================
    
    # def place_order_clob(self, market_id: str, side: str, size: float, 
    #                     price: float, order_type: str = "LIMIT") -> Dict:
    #     """Place a new limit order on CLOB."""
    #     original_url = self.base_url
    #     self.use_clob_api()
    #     try:
    #         order_data = {
    #             "market": market_id,
    #             "side": side,
    #             "size": size,
    #             "price": price,
    #             "type": order_type
    #         }
    #         return self._request("POST", "/order", data=order_data)
    #     finally:
    #         self.base_url = original_url
    # 
    # def cancel_order_clob(self, order_id: str) -> Dict:
    #     """Cancel a specific order on CLOB."""
    #     original_url = self.base_url
    #     self.use_clob_api()
    #     try:
    #         return self._request("DELETE", f"/order", params={"orderID": order_id})
    #     finally:
    #         self.base_url = original_url
    # 
    # def cancel_all_orders_clob(self) -> Dict:
    #     """Cancel all open orders on CLOB."""
    #     original_url = self.base_url
    #     self.use_clob_api()
    #     try:
    #         return self._request("DELETE", "/orders")
    #     finally:
    #         self.base_url = original_url
    # 
    # def get_orders_clob(self, limit: int = 100, offset: int = 0) -> Dict:
    #     """Fetch your open orders from CLOB."""
    #     original_url = self.base_url
    #     self.use_clob_api()
    #     try:
    #         return self._request("GET", "/orders", {
    #             "limit": limit,
    #             "offset": offset
    #         })
    #     finally:
    #         self.base_url = original_url
    # 
    # def get_order_status_clob(self, order_id: str) -> Dict:
    #     """Get the status of a specific order from CLOB."""
    #     original_url = self.base_url
    #     self.use_clob_api()
    #     try:
    #         return self._request("GET", f"/order/{order_id}")
    #     finally:
    #         self.base_url = original_url
    # 
    # def get_book_clob(self, market_id: str) -> Dict:
    #     """Get the current L2 order book for a specific market (token ID) from CLOB."""
    #     original_url = self.base_url
    #     self.use_clob_api()
    #     try:
    #         return self._request("GET", "/book", {
    #             "token": market_id
    #         })
    #     finally:
    #         self.base_url = original_url
    # 
    # def get_prices_history_clob(self, market_id: str, days: int = 30) -> Dict:
    #     """Fetch historical price data for a market from CLOB."""
    #     original_url = self.base_url
    #     self.use_clob_api()
    #     try:
    #         return self._request("GET", "/prices-history", {
    #             "token": market_id,
    #             "days": days
    #         })
    #     finally:
    #         self.base_url = original_url
    # 
    # def get_midpoint_clob(self, market_id: str) -> Dict:
    #     """Get the current midpoint price between bid and ask from CLOB."""
    #     original_url = self.base_url
    #     self.use_clob_api()
    #     try:
    #         return self._request("GET", "/midpoint", {
    #             "token": market_id
    #         })
    #     finally:
    #         self.base_url = original_url
    # 
    # def get_spread_clob(self, market_id: str) -> Dict:
    #     """Get the current bid-ask spread from CLOB."""
    #     original_url = self.base_url
    #     self.use_clob_api()
    #     try:
    #         return self._request("GET", "/spread", {
    #             "token": market_id
    #         })
    #     finally:
    #         self.base_url = original_url
    # 
    # def get_api_keys_clob(self) -> Dict:
    #     """View your active API keys from CLOB."""
    #     original_url = self.base_url
    #     self.use_clob_api()
    #     try:
    #         return self._request("GET", "/api-keys")
    #     finally:
    #         self.base_url = original_url
    # 
    # def create_api_key_clob(self) -> Dict:
    #     """Create a new API key on CLOB."""
    #     original_url = self.base_url
    #     self.use_clob_api()
    #     try:
    #         return self._request("POST", "/api-key")
    #     finally:
    #         self.base_url = original_url
    # 
    # def revoke_api_key_clob(self, api_key_id: str) -> Dict:
    #     """Revoke an API key on CLOB."""
    #     original_url = self.base_url
    #     self.use_clob_api()
    #     try:
    #         return self._request("DELETE", "/api-key", params={"keyID": api_key_id})
    #     finally:
    #         self.base_url = original_url

