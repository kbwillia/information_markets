"""Kalshi API client using the official Kalshi Python SDK."""
from typing import Dict, List, Optional
from datetime import datetime
import os

try:
    from kalshi_python_sync import Configuration, KalshiClient as KalshiSDKClient
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    KalshiSDKClient = None
    Configuration = None

from src.config import Config


class KalshiClient:
    """Client for interacting with Kalshi API using the official SDK."""
    
    def __init__(self, api_key_id: str = None, private_key_path: str = None, 
                 private_key_pem: str = None, host: str = None):
        """
        Initialize Kalshi client.
        
        Args:
            api_key_id: Kalshi API key ID
            private_key_path: Path to RSA private key file (.pem)
            private_key_pem: Private key content as string (alternative to path)
            host: API host URL (defaults to Config.KALSHI_BASE_URL)
        """
        if not SDK_AVAILABLE:
            raise ImportError(
                "Kalshi SDK not installed. Install with: pip install kalshi-python-sync"
            )
        
        self.api_key_id = api_key_id or Config.KALSHI_API_KEY
        self.host = host or Config.KALSHI_BASE_URL
        
        # Load private key
        if private_key_pem:
            self.private_key_pem = private_key_pem
        elif private_key_path:
            if os.path.exists(private_key_path):
                with open(private_key_path, 'r') as f:
                    self.private_key_pem = f.read()
            else:
                raise FileNotFoundError(f"Private key file not found: {private_key_path}")
        elif Config.KALSHI_PRIVATE_KEY_PATH:
            key_path = Config.KALSHI_PRIVATE_KEY_PATH
            # Handle both relative and absolute paths
            if not os.path.isabs(key_path):
                # Try relative to current working directory
                if not os.path.exists(key_path):
                    # Try relative to project root (where .env is)
                    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                    abs_key_path = os.path.join(project_root, key_path)
                    if os.path.exists(abs_key_path):
                        key_path = abs_key_path
            if os.path.exists(key_path):
                with open(key_path, 'r') as f:
                    self.private_key_pem = f.read()
            else:
                raise FileNotFoundError(
                    f"Private key file not found: {key_path}\n"
                    f"Current working directory: {os.getcwd()}\n"
                    f"Tried path: {os.path.abspath(key_path) if not os.path.isabs(key_path) else key_path}"
                )
        elif Config.KALSHI_PRIVATE_KEY_PEM:
            # Handle newlines - replace \n with actual newlines if needed
            private_key = Config.KALSHI_PRIVATE_KEY_PEM
            if '\\n' in private_key:
                private_key = private_key.replace('\\n', '\n')
            self.private_key_pem = private_key
        else:
            raise ValueError(
                "Private key required. Provide private_key_path, private_key_pem, "
                "or set KALSHI_PRIVATE_KEY_PATH or KALSHI_PRIVATE_KEY_PEM in .env"
            )
        
        # Configure and initialize SDK client
        config = Configuration(
            host=self.host
        )
        config.api_key_id = self.api_key_id
        config.private_key_pem = self.private_key_pem
        
        self.client = KalshiSDKClient(config)
    
    def get_markets(self, limit: int = 100, cursor: str = None, **kwargs) -> Dict:
        """Get available markets using the SDK."""
        try:
            # Try SDK first - it handles auth properly
            response = self.client.get_markets(limit=limit, cursor=cursor, **kwargs)
            # Convert SDK response to dict format
            if hasattr(response, 'dict'):
                return response.dict()
            elif hasattr(response, '__dict__'):
                return {k: v for k, v in response.__dict__.items() if not k.startswith('_')}
            return response
        except Exception as e:
            # Handle Pydantic validation errors (None values in required fields)
            error_str = str(e)
            if 'validation' in error_str.lower() or 'string_type' in error_str or 'int_type' in error_str:
                # SDK validation failed - get raw response using SDK's REST client
                # This way we still use SDK auth but bypass validation
                try:
                    from kalshi_python_sync.api.market_api import MarketApi
                    import json
                    
                    # Use SDK's MarketApi to get raw response
                    market_api = MarketApi(self.client.api_client if hasattr(self.client, 'api_client') else None)
                    if market_api.api_client is None:
                        market_api.api_client = self.client.api_client if hasattr(self.client, 'api_client') else self.client
                    
                    # Get raw response without preload (bypasses validation)
                    raw_response = market_api.get_markets_without_preload_content(
                        limit=limit,
                        cursor=cursor,
                        **{k: v for k, v in kwargs.items() if k in ['event_ticker', 'series_ticker', 'status', 'tickers']}
                    )
                    
                    # Parse JSON response
                    data = json.loads(raw_response.data)
                    
                    # Clean None values to match SDK model requirements
                    if isinstance(data, dict) and 'markets' in data:
                        for market in data['markets']:
                            if isinstance(market, dict):
                                if market.get('category') is None:
                                    market['category'] = 'Uncategorized'
                                if market.get('risk_limit_cents') is None:
                                    market['risk_limit_cents'] = 0
                    
                    return data
                except Exception as e2:
                    # If that fails, try using the SDK's REST client directly
                    try:
                        if hasattr(self.client, 'api_client') and hasattr(self.client.api_client, 'rest_client'):
                            rest_client = self.client.api_client.rest_client
                            # Make request using SDK's authenticated REST client
                            url = f"{self.host}/exchange/markets"
                            params = {'limit': limit}
                            if cursor:
                                params['cursor'] = cursor
                            
                            # Use SDK's REST client (handles auth)
                            response = rest_client.GET(url, query_params=params)
                            data = json.loads(response.data)
                            
                            # Clean None values
                            if isinstance(data, dict) and 'markets' in data:
                                for market in data['markets']:
                                    if isinstance(market, dict):
                                        if market.get('category') is None:
                                            market['category'] = 'Uncategorized'
                                        if market.get('risk_limit_cents') is None:
                                            market['risk_limit_cents'] = 0
                            
                            return data
                    except Exception as e3:
                        print(f"Warning: Kalshi SDK validation error. Tried SDK methods but all failed: {e3}")
                        return {'markets': [], 'cursor': None}
            else:
                raise Exception(f"Error getting markets: {e}")
    
    def get_market(self, ticker: str) -> Dict:
        """Get specific market by ticker."""
        try:
            response = self.client.get_market(ticker)
            if hasattr(response, 'dict'):
                return response.dict()
            elif hasattr(response, '__dict__'):
                return {k: v for k, v in response.__dict__.items() if not k.startswith('_')}
            return response
        except Exception as e:
            raise Exception(f"Error getting market {ticker}: {e}")
    
    def get_orderbook(self, ticker: str) -> Dict:
        """Get orderbook for a market."""
        try:
            response = self.client.get_orderbook(ticker)
            if hasattr(response, 'dict'):
                return response.dict()
            elif hasattr(response, '__dict__'):
                return {k: v for k, v in response.__dict__.items() if not k.startswith('_')}
            return response
        except Exception as e:
            raise Exception(f"Error getting orderbook for {ticker}: {e}")
    
    def get_portfolio(self) -> Dict:
        """Get current portfolio."""
        try:
            response = self.client.get_portfolio()
            if hasattr(response, 'dict'):
                return response.dict()
            elif hasattr(response, '__dict__'):
                return {k: v for k, v in response.__dict__.items() if not k.startswith('_')}
            return response
        except Exception as e:
            raise Exception(f"Error getting portfolio: {e}")
    
    def get_balance(self) -> Dict:
        """Get account balance."""
        try:
            response = self.client.get_balance()
            if hasattr(response, 'dict'):
                return response.dict()
            elif hasattr(response, '__dict__'):
                return {k: v for k, v in response.__dict__.items() if not k.startswith('_')}
            return response
        except Exception as e:
            raise Exception(f"Error getting balance: {e}")
    
    def get_positions(self) -> Dict:
        """Get current positions."""
        try:
            response = self.client.get_positions()
            if hasattr(response, 'dict'):
                return response.dict()
            elif hasattr(response, '__dict__'):
                return {k: v for k, v in response.__dict__.items() if not k.startswith('_')}
            return response
        except Exception as e:
            raise Exception(f"Error getting positions: {e}")
    
    def place_order(self, ticker: str, side: str, action: str, 
                   count: int, price: int = None, yes_price: int = None,
                   no_price: int = None) -> Dict:
        """
        Place an order.
        
        Args:
            ticker: Market ticker
            side: 'yes' or 'no'
            action: 'buy' or 'sell'
            count: Number of contracts
            price: Limit price (in cents, 0-100)
            yes_price: Yes price for market orders
            no_price: No price for market orders
        """
        try:
            # Build order request based on SDK API
            order_params = {
                "ticker": ticker,
                "side": side,
                "action": action,
                "count": count
            }
            
            if price:
                order_params["price"] = price
            if yes_price:
                order_params["yes_price"] = yes_price
            if no_price:
                order_params["no_price"] = no_price
            
            response = self.client.create_order(**order_params)
            if hasattr(response, 'dict'):
                return response.dict()
            elif hasattr(response, '__dict__'):
                return {k: v for k, v in response.__dict__.items() if not k.startswith('_')}
            return response
        except Exception as e:
            raise Exception(f"Error placing order: {e}")
    
    def get_orders(self, limit: int = 100, cursor: str = None, status: str = None) -> Dict:
        """Get your order history."""
        try:
            params = {"limit": limit}
            if cursor:
                params["cursor"] = cursor
            if status:
                params["status"] = status
            
            response = self.client.get_orders(**params)
            if hasattr(response, 'dict'):
                return response.dict()
            elif hasattr(response, '__dict__'):
                return {k: v for k, v in response.__dict__.items() if not k.startswith('_')}
            return response
        except Exception as e:
            raise Exception(f"Error getting orders: {e}")
    
    def get_order_status(self, order_id: str) -> Dict:
        """Get status of an order."""
        try:
            response = self.client.get_order(order_id)
            if hasattr(response, 'dict'):
                return response.dict()
            elif hasattr(response, '__dict__'):
                return {k: v for k, v in response.__dict__.items() if not k.startswith('_')}
            return response
        except Exception as e:
            raise Exception(f"Error getting order status: {e}")
    
    def cancel_order(self, order_id: str) -> Dict:
        """Cancel an order."""
        try:
            response = self.client.cancel_order(order_id)
            if hasattr(response, 'dict'):
                return response.dict()
            elif hasattr(response, '__dict__'):
                return {k: v for k, v in response.__dict__.items() if not k.startswith('_')}
            return response
        except Exception as e:
            raise Exception(f"Error canceling order: {e}")
    
    def get_exchange_status(self) -> Dict:
        """Get exchange status."""
        try:
            response = self.client.get_exchange_status()
            if hasattr(response, 'dict'):
                return response.dict()
            elif hasattr(response, '__dict__'):
                return {k: v for k, v in response.__dict__.items() if not k.startswith('_')}
            return response
        except Exception as e:
            raise Exception(f"Error getting exchange status: {e}")
    
    def get_market_history(self, ticker: str, limit: int = 100) -> Dict:
        """Get market trading history."""
        try:
            response = self.client.get_market_history(ticker, limit=limit)
            if hasattr(response, 'dict'):
                return response.dict()
            elif hasattr(response, '__dict__'):
                return {k: v for k, v in response.__dict__.items() if not k.startswith('_')}
            return response
        except Exception as e:
            raise Exception(f"Error getting market history: {e}")
