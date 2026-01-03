"""Test all Kalshi API endpoints and print results."""
import sys
import json

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

from src.data_collectors.kalshi_client import KalshiClient

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_result(endpoint_name, result, max_length=500):
    """Print endpoint result in a readable format."""
    print(f"\n✓ {endpoint_name} - SUCCESS")
    result_str = json.dumps(result, indent=2, default=str)
    if len(result_str) > max_length:
        print(result_str[:max_length] + f"\n... (truncated, total length: {len(result_str)} chars)")
    else:
        print(result_str)

def test_all_endpoints():
    """Test all Kalshi API endpoints."""
    print("=" * 70)
    print("  TESTING ALL KALSHI API ENDPOINTS")
    print("=" * 70)
    
    try:
        client = KalshiClient()
        print("\n✓ Kalshi client initialized successfully")
    except Exception as e:
        print(f"\n[ERROR] Failed to initialize client: {e}")
        return
    
    # 1. Exchange Status
    print_section("1. EXCHANGE STATUS")
    try:
        result = client.get_exchange_status()
        print_result("GET /exchange/status", result, max_length=1000)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # 2. List Markets
    print_section("2. LIST MARKETS")
    try:
        result = client.get_markets(limit=2)
        print_result("GET /markets (limit=2)", result)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # 2b. List Markets with Filters
    print_section("2b. LIST MARKETS WITH FILTERS")
    try:
        # Test with status filter
        result = client.get_markets(limit=2, status='open')
        print_result("GET /markets (limit=2, status=open)", result)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # 2c. List Markets with Series/Event Filters
    print_section("2c. LIST MARKETS WITH SERIES/EVENT FILTERS")
    try:
        # First get a market to extract series_ticker or event_ticker
        markets = client.get_markets(limit=1)
        market_list = markets.get('markets', [])
        if not market_list and hasattr(markets, 'markets'):
            market_list = markets.markets
        elif isinstance(markets, list):
            market_list = markets[:1]
        
        if market_list:
            series_ticker = market_list[0].get('series_ticker', '')
            event_ticker = market_list[0].get('event_ticker', '')
            
            if series_ticker:
                result = client.get_markets(limit=2, series_ticker=series_ticker)
                print_result(f"GET /markets (limit=2, series_ticker={series_ticker})", result)
            elif event_ticker:
                result = client.get_markets(limit=2, event_ticker=event_ticker)
                print_result(f"GET /markets (limit=2, event_ticker={event_ticker})", result)
            else:
                print("\n⚠ No series_ticker or event_ticker found in market data")
        else:
            print("\n⚠ No markets available")
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # 3. Get Market Details (if we have a ticker)
    print_section("3. GET MARKET DETAILS")
    try:
        markets = client.get_markets(limit=1)
        market_list = markets.get('markets', [])
        if not market_list and hasattr(markets, 'markets'):
            market_list = markets.markets
        elif isinstance(markets, list):
            market_list = markets[:1]
        
        if market_list:
            ticker = market_list[0].get('ticker') or market_list[0].get('event_ticker', '')
            if ticker:
                result = client.get_market(ticker)
                print_result(f"GET /markets/{ticker}", result)
            else:
                print("\n⚠ No ticker found in market data")
        else:
            print("\n⚠ No markets available to test")
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # 4. Get Orderbook
    print_section("4. GET ORDERBOOK")
    try:
        markets = client.get_markets(limit=1)
        market_list = markets.get('markets', [])
        if not market_list and hasattr(markets, 'markets'):
            market_list = markets.markets
        elif isinstance(markets, list):
            market_list = markets[:1]
        
        if market_list:
            ticker = market_list[0].get('ticker') or market_list[0].get('event_ticker', '')
            if not ticker and hasattr(market_list[0], 'ticker'):
                ticker = market_list[0].ticker
            if ticker:
                # Try different method names
                if hasattr(client.client, 'get_market_orderbook'):
                    result = client.client.get_market_orderbook(ticker, depth=10)
                elif hasattr(client.client, 'get_orderbook'):
                    result = client.client.get_orderbook(ticker)
                elif hasattr(client.client, 'get_markets_orderbook'):
                    result = client.client.get_markets_orderbook(ticker)
                else:
                    # Try accessing through SDK directly
                    result = client.client.call_api('/markets/{ticker}/orderbook'.format(ticker=ticker), 'GET')
                print_result(f"GET /markets/{ticker}/orderbook (depth=10)", result)
            else:
                print("\n⚠ No ticker found")
        else:
            print("\n⚠ No markets available")
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
        print("Note: This endpoint may not be available in the SDK or may use a different method name")
    
    # 5. Get Market History
    print_section("5. GET MARKET HISTORY")
    try:
        markets = client.get_markets(limit=1)
        market_list = markets.get('markets', [])
        if not market_list and hasattr(markets, 'markets'):
            market_list = markets.markets
        elif isinstance(markets, list):
            market_list = markets[:1]
        
        if market_list:
            ticker = market_list[0].get('ticker') or market_list[0].get('event_ticker', '')
            if not ticker and hasattr(market_list[0], 'ticker'):
                ticker = market_list[0].ticker
            if ticker:
                # Try different method names
                if hasattr(client.client, 'get_market_history'):
                    result = client.client.get_market_history(ticker, limit=2)
                elif hasattr(client.client, 'get_markets_history'):
                    result = client.client.get_markets_history(ticker, limit=2)
                else:
                    result = client.get_market_history(ticker, limit=2)
                print_result(f"GET /markets/{ticker}/history (limit=2)", result)
            else:
                print("\n⚠ No ticker found")
        else:
            print("\n⚠ No markets available")
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
        print("Note: This endpoint may not be available in the SDK or may use a different method name")
    
    # 5b. Get Trades (All Markets)
    print_section("5b. GET TRADES (ALL MARKETS)")
    try:
        # Try different method names
        if hasattr(client.client, 'get_trades'):
            result = client.client.get_trades(limit=2)
        elif hasattr(client.client, 'get_markets_trades'):
            result = client.client.get_markets_trades(limit=2)
        else:
            # Try calling directly through SDK
            result = client.client.call_api('/markets/trades?limit=2', 'GET')
        print_result("GET /markets/trades (limit=2)", result)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
        print("Note: This endpoint may not be available in the SDK or may use a different method name")
    
    # 5b2. Get Trades with Filters
    print_section("5b2. GET TRADES WITH FILTERS")
    try:
        # Get a market ticker first
        markets = client.get_markets(limit=1)
        market_list = markets.get('markets', [])
        if not market_list and hasattr(markets, 'markets'):
            market_list = markets.markets
        elif isinstance(markets, list):
            market_list = markets[:1]
        
        if market_list:
            ticker = market_list[0].get('ticker') or market_list[0].get('event_ticker', '')
            if not ticker and hasattr(market_list[0], 'ticker'):
                ticker = market_list[0].ticker
            
            if ticker:
                # Try different method names with ticker filter
                if hasattr(client.client, 'get_trades'):
                    result = client.client.get_trades(limit=2, ticker=ticker)
                elif hasattr(client.client, 'get_markets_trades'):
                    result = client.client.get_markets_trades(limit=2, ticker=ticker)
                else:
                    result = None
                
                if result:
                    print_result(f"GET /markets/trades (limit=2, ticker={ticker})", result)
                else:
                    print("\n⚠ Could not call trades endpoint with filter")
            else:
                print("\n⚠ No ticker found")
        else:
            print("\n⚠ No markets available")
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
        print("Note: This endpoint may not be available in the SDK or may use a different method name")
    
    # 5c. Get Market Candlesticks
    print_section("5c. GET MARKET CANDLESTICKS")
    try:
        markets = client.get_markets(limit=1)
        market_list = markets.get('markets', [])
        if not market_list and hasattr(markets, 'markets'):
            market_list = markets.markets
        elif isinstance(markets, list):
            market_list = markets[:1]
        
        if market_list:
            market_ticker = market_list[0].get('ticker') or market_list[0].get('event_ticker', '')
            if not market_ticker and hasattr(market_list[0], 'ticker'):
                market_ticker = market_list[0].ticker
            
            # Try to get series_ticker from market data
            series_ticker = market_list[0].get('series_ticker') or market_list[0].get('series_ticker', '')
            if not series_ticker and hasattr(market_list[0], 'series_ticker'):
                series_ticker = market_list[0].series_ticker
            
            if market_ticker:
                # Try different method names
                if hasattr(client.client, 'get_market_candlesticks'):
                    if series_ticker:
                        result = client.client.get_market_candlesticks(
                            ticker=series_ticker,
                            market_ticker=market_ticker,
                            period_interval='1h'
                        )
                    else:
                        # Try with just market ticker
                        result = client.client.get_market_candlesticks(
                            ticker=market_ticker,
                            market_ticker=market_ticker,
                            period_interval='1h'
                        )
                elif hasattr(client.client, 'get_markets_candlesticks'):
                    result = client.client.get_markets_candlesticks(
                        ticker=series_ticker or market_ticker,
                        market_ticker=market_ticker,
                        period_interval='1h'
                    )
                else:
                    print("\n⚠ Method not found on SDK client")
                    result = None
                
                if result:
                    print_result(f"GET /series/{series_ticker or 'SERIES'}/markets/{market_ticker}/candlesticks", result)
                else:
                    print("\n⚠ Could not call candlesticks endpoint")
            else:
                print("\n⚠ No market ticker found")
        else:
            print("\n⚠ No markets available")
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
        print("Note: This endpoint requires a series ticker and market ticker. It may not be available for all markets.")
    
    # 6. Get Portfolio (Authenticated)
    print_section("6. GET PORTFOLIO (AUTHENTICATED)")
    try:
        # Try different method names
        if hasattr(client.client, 'get_portfolio'):
            result = client.client.get_portfolio()
        else:
            result = client.get_portfolio()
        print_result("GET /portfolio", result)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
        print("Note: This endpoint may not be available in the SDK or may use a different method name")
    
    # 7. Get Balance (Authenticated)
    print_section("7. GET BALANCE (AUTHENTICATED)")
    try:
        result = client.get_balance()
        print_result("GET /portfolio/balance", result)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # 8. Get Positions (Authenticated)
    print_section("8. GET POSITIONS (AUTHENTICATED)")
    try:
        result = client.get_positions()
        print_result("GET /portfolio/positions", result)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # 9. Get Orders (Authenticated)
    print_section("9. GET ORDERS (AUTHENTICATED)")
    try:
        result = client.get_orders(limit=2)
        print_result("GET /portfolio/orders (limit=2)", result)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    print("\nMARKETS API CLASS - All Methods Tested:")
    print("  1. get_exchange_status() - Exchange status")
    print("  2. get_markets() - List markets (basic)")
    print("  2b. get_markets() - With status filter")
    print("  2c. get_markets() - With series/event filters")
    print("  3. get_market(ticker) - Get market details")
    print("  4. get_market_orderbook(ticker, depth) - Get orderbook")
    print("  5. get_market_history(ticker, limit) - Get market history")
    print("  5b. get_trades() - Get all trades")
    print("  5b2. get_trades() - With ticker filter")
    print("  5c. get_market_candlesticks() - Get candlestick data")
    print("\nPORTFOLIO API CLASS - Methods Tested:")
    print("  6. get_portfolio() - Portfolio overview")
    print("  7. get_balance() - Account balance")
    print("  8. get_positions() - Current positions")
    print("  9. get_orders() - Order history")
    print("\nAll endpoints tested. Check results above to see which ones work.")
    print("\nNote: Authenticated endpoints require valid API credentials.")
    print("Market-specific endpoints require valid market tickers.")
    print("Some endpoints may require specific market types (e.g., candlesticks need series).")

if __name__ == "__main__":
    test_all_endpoints()

