"""Polymarket API client for market data and trading."""
import requests
from typing import Dict, List, Optional
from datetime import datetime

from src.config import Config


class PolymarketClient:
    """Client for interacting with Polymarket API."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.POLYMARKET_API_KEY
        self.base_url = Config.POLYMARKET_BASE_URL
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
    
    def get_user_positions(self) -> Dict:
        """Get current user positions (requires authentication)."""
        return self._request("GET", "/user/positions")
    
    def get_user_balance(self) -> Dict:
        """Get user balance (requires authentication)."""
        # Try different possible endpoints - Polymarket API structure may vary
        endpoints = ["/user/balance", "/balance", "/v1/balance", "/api/v1/balance"]
        last_error = None
        for endpoint in endpoints:
            try:
                return self._request("GET", endpoint)
            except Exception as e:
                last_error = e
                continue
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

