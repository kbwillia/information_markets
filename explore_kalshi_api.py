"""Explore and document Kalshi API endpoints and available data."""
from src.data_collectors.kalshi_client import KalshiClient
import json

def explore_kalshi_api():
    """Explore what data is available from Kalshi API."""
    print("=" * 70)
    print("KALSHI API ENDPOINTS AND DATA EXPLORATION")
    print("=" * 70)
    
    try:
        client = KalshiClient()
        print("\n✓ Kalshi client initialized successfully\n")
    except Exception as e:
        print(f"✗ Failed to initialize client: {e}")
        return
    
    # 1. Exchange Status
    print("\n" + "=" * 70)
    print("1. EXCHANGE STATUS")
    print("=" * 70)
    try:
        status = client.get_exchange_status()
        print("Endpoint: GET /exchange/status")
        print("Data available:")
        print(json.dumps(status, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")
    
    # 2. Markets
    print("\n" + "=" * 70)
    print("2. MARKETS")
    print("=" * 70)
    try:
        markets = client.get_markets(limit=3)
        print("Endpoint: GET /markets")
        print(f"Retrieved {len(markets.get('markets', []))} sample markets")
        
        if markets.get('markets'):
            sample_market = markets['markets'][0]
            print("\nSample market structure:")
            print(json.dumps(sample_market, indent=2, default=str)[:1000] + "...")
            
            # Get detailed market info
            ticker = sample_market.get('ticker') or sample_market.get('event_ticker', '')
            if ticker:
                print(f"\n--- Detailed Market Info for {ticker} ---")
                market_detail = client.get_market(ticker)
                print(json.dumps(market_detail, indent=2, default=str)[:1500] + "...")
    except Exception as e:
        print(f"Error: {e}")
    
    # 3. Orderbook
    print("\n" + "=" * 70)
    print("3. ORDERBOOK")
    print("=" * 70)
    try:
        markets = client.get_markets(limit=1)
        market_list = markets.get('markets', [])
        if market_list:
            ticker = market_list[0].get('ticker') or market_list[0].get('event_ticker', '')
            if ticker:
                print(f"Endpoint: GET /markets/{ticker}/orderbook")
                orderbook = client.get_orderbook(ticker)
                print("Orderbook data structure:")
                print(json.dumps(orderbook, indent=2, default=str)[:1000] + "...")
    except Exception as e:
        print(f"Error: {e}")
    
    # 4. Market History
    print("\n" + "=" * 70)
    print("4. MARKET HISTORY / TRADES")
    print("=" * 70)
    try:
        markets = client.get_markets(limit=1)
        market_list = markets.get('markets', [])
        if market_list:
            ticker = market_list[0].get('ticker') or market_list[0].get('event_ticker', '')
            if ticker:
                print(f"Endpoint: GET /markets/{ticker}/history")
                history = client.get_market_history(ticker, limit=10)
                print("Market history/trades structure:")
                print(json.dumps(history, indent=2, default=str)[:1500] + "...")
    except Exception as e:
        print(f"Error: {e}")
    
    # 5. Portfolio (Authenticated)
    print("\n" + "=" * 70)
    print("5. PORTFOLIO (AUTHENTICATED)")
    print("=" * 70)
    try:
        print("Endpoint: GET /portfolio")
        portfolio = client.get_portfolio()
        print("Portfolio data structure:")
        print(json.dumps(portfolio, indent=2, default=str)[:1000] + "...")
    except Exception as e:
        print(f"Error: {e}")
    
    # 6. Balance (Authenticated)
    print("\n" + "=" * 70)
    print("6. BALANCE (AUTHENTICATED)")
    print("=" * 70)
    try:
        print("Endpoint: GET /portfolio/balance")
        balance = client.get_balance()
        print("Balance data:")
        print(json.dumps(balance, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")
    
    # 7. Positions (Authenticated)
    print("\n" + "=" * 70)
    print("7. POSITIONS (AUTHENTICATED)")
    print("=" * 70)
    try:
        print("Endpoint: GET /portfolio/positions")
        positions = client.get_positions()
        print("Positions data structure:")
        print(json.dumps(positions, indent=2, default=str)[:1000] + "...")
    except Exception as e:
        print(f"Error: {e}")
    
    # 8. Explore SDK methods
    print("\n" + "=" * 70)
    print("8. AVAILABLE SDK METHODS")
    print("=" * 70)
    print("Exploring Kalshi SDK client methods...")
    sdk_client = client.client
    methods = [m for m in dir(sdk_client) if not m.startswith('_') and callable(getattr(sdk_client, m))]
    print(f"\nFound {len(methods)} methods in SDK client:")
    for method in sorted(methods):
        print(f"  - {method}")
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
Available Kalshi API Endpoints:

PUBLIC ENDPOINTS (No authentication required):
1. GET /exchange/status - Exchange status and trading hours
2. GET /markets - List all markets (with pagination)
3. GET /markets/{ticker} - Get specific market details
4. GET /markets/{ticker}/orderbook - Get orderbook for a market
5. GET /markets/{ticker}/history - Get trading history for a market

AUTHENTICATED ENDPOINTS (Requires API key):
6. GET /portfolio - Get your portfolio overview
7. GET /portfolio/balance - Get account balance
8. GET /portfolio/positions - Get your current positions
9. GET /portfolio/orders - Get your orders
10. POST /portfolio/orders - Place a new order
11. DELETE /portfolio/orders/{order_id} - Cancel an order
12. GET /portfolio/orders/{order_id} - Get order status

KEY DATA POINTS FOR WALLET TRACKING:
- Market data: ticker, title, status, prices, volume
- Orderbook: bid/ask prices, depth
- Trade history: prices, volumes, timestamps
- Portfolio: your positions, P&L
- Orders: your order history

NOTE: Wallet addresses are NOT exposed in public APIs.
To track other users' wallets, you would need:
- Blockchain monitoring (if trades are on-chain)
- Private/internal APIs (if available)
- Manual tracking of publicly shared addresses
    """)

if __name__ == "__main__":
    explore_kalshi_api()

