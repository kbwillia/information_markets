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
    
    def get_trades(self, market_id: str, limit: int = 100) -> Dict:
        """Get recent trades for a market."""
        return self._request("GET", f"/markets/{market_id}/trades", {
            "limit": limit
        })
    
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

