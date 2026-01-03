"""Test all Polymarket API endpoints and print results."""
import sys
import json

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

from src.data_collectors.polymarket_client import PolymarketClient
from src.config import Config

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
    """Test all Polymarket API endpoints."""
    print("=" * 70)
    print("  TESTING ALL POLYMARKET API ENDPOINTS")
    print("=" * 70)
    
    try:
        client = PolymarketClient()
        print("\n✓ Polymarket client initialized successfully")
        print(f"  Default base URL: {client.base_url}")
        print(f"  CLOB URL: {client.clob_url}")
        print(f"  Gamma URL: {client.gamma_url}")
        print(f"  Data URL: {client.data_url}")
    except Exception as e:
        print(f"\n[ERROR] Failed to initialize client: {e}")
        return
    
    # ========================================================================
    # GAMMA API - Market Discovery, Metadata, and Events
    # ========================================================================
    
    print_section("GAMMA API - Market Discovery")
    
    # 1. Get Markets (Gamma API)
    print_section("1. GET MARKETS (Gamma API)")
    try:
        client.use_gamma_api()
        result = client.get_markets(limit=5)
        print_result("GET /markets (limit=5)", result)
        
        # Extract a market ID for subsequent tests
        market_list = result.get("markets", [])
        if not market_list and isinstance(result, list):
            market_list = result[:1]
        elif isinstance(result, dict) and 'data' in result:
            market_list = result['data'][:1] if isinstance(result['data'], list) else []
        
        test_market_id = None
        if market_list:
            test_market_id = market_list[0].get('id') or market_list[0].get('slug') or market_list[0].get('conditionId')
            if test_market_id:
                print(f"\n  Using market ID for subsequent tests: {test_market_id}")
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
        test_market_id = None
    
    # 2. Get Market Details (Gamma API)
    if test_market_id:
        print_section("2. GET MARKET DETAILS (Gamma API)")
        try:
            client.use_gamma_api()
            result = client.get_market(test_market_id)
            print_result(f"GET /markets/{test_market_id}", result)
        except Exception as e:
            print(f"\n[ERROR] Failed: {e}")
    
    # ========================================================================
    # CLOB API - Order Management, Prices, and Order Books
    # ========================================================================
    
    print_section("CLOB API - Order Management")
    
    # 3. Get Orderbook (CLOB API)
    if test_market_id:
        print_section("3. GET ORDERBOOK (CLOB API)")
        try:
            client.use_clob_api()
            result = client.get_orderbook(test_market_id)
            print_result(f"GET /markets/{test_market_id}/orderbook", result)
        except Exception as e:
            print(f"\n[ERROR] Failed: {e}")
    
    # 4. Get Trades (CLOB API)
    if test_market_id:
        print_section("4. GET TRADES (CLOB API)")
        try:
            client.use_clob_api()
            result = client.get_trades(test_market_id, limit=5)
            print_result(f"GET /markets/{test_market_id}/trades (limit=5)", result)
        except Exception as e:
            print(f"\n[ERROR] Failed: {e}")
    
    # ========================================================================
    # DATA API - User Positions, Activity, and History
    # ========================================================================
    
    print_section("DATA API - User Positions")
    
    # Check if we have API credentials
    has_credentials = bool(Config.POLYMARKET_API_KEY and Config.POLYMARKET_API_SECRET and 
                          Config.POLYMARKET_API_PASSPHRASE and Config.POLYMARKET_PRIVATE_KEY)
    
    if not has_credentials:
        print("\n⚠ Skipping Data API tests - API credentials not fully configured")
        print("  Required: POLYMARKET_API_KEY, POLYMARKET_API_SECRET, POLYMARKET_API_PASSPHRASE, POLYMARKET_PRIVATE_KEY")
    else:
        # 5. Get User Positions - Basic (Data API)
        print_section("5. GET USER POSITIONS - Basic (Data API)")
        # Note: This requires a user address - you may need to provide one
        user_address = None  # Set this to a valid user address for testing (e.g., "0x56687bf447db6ffa42ffe2204a05edaa20f55839")
        
        if not user_address:
            print("\n⚠ Skipping - user address not provided")
            print("  To test this endpoint, set a valid user address in the test file")
            print("  Example: user_address = '0x56687bf447db6ffa42ffe2204a05edaa20f55839'")
        else:
            try:
                result = client.get_user_positions(user=user_address, limit=10)
                print_result(f"GET /positions (user={user_address[:10]}..., limit=10)", result)
            except Exception as e:
                print(f"\n[ERROR] Failed: {e}")
        
        # 5b. Get User Positions - With Market Filter (Data API)
        if user_address and test_market_id:
            print_section("5b. GET USER POSITIONS - With Market Filter (Data API)")
            try:
                result = client.get_user_positions(
                    user=user_address,
                    market=[test_market_id],
                    limit=10,
                    offset=0
                )
                print_result(f"GET /positions (user={user_address[:10]}..., market={test_market_id[:20]}...)", result)
            except Exception as e:
                print(f"\n[ERROR] Failed: {e}")
        
        # 5c. Get User Positions - With Event ID Filter (Data API)
        if user_address:
            print_section("5c. GET USER POSITIONS - With Event ID Filter (Data API)")
            try:
                # Try with eventId parameter (you may need to provide a valid event ID)
                event_id = None  # Set this to a valid event ID for testing
                if event_id:
                    result = client.get_user_positions(
                        user=user_address,
                        event_id=[event_id],
                        limit=10,
                        offset=0,
                        redeemable=False,
                        mergeable=False
                    )
                    print_result(f"GET /positions (user={user_address[:10]}..., eventId={event_id})", result)
                else:
                    print("\n⚠ Skipping - event ID not provided")
            except Exception as e:
                print(f"\n[ERROR] Failed: {e}")
        
        # 5d. Get User Positions - With Size Threshold (Data API)
        if user_address:
            print_section("5d. GET USER POSITIONS - With Size Threshold (Data API)")
            try:
                result = client.get_user_positions(
                    user=user_address,
                    size_threshold=1.0,
                    limit=10,
                    offset=0
                )
                print_result(f"GET /positions (user={user_address[:10]}..., sizeThreshold=1.0)", result)
            except Exception as e:
                print(f"\n[ERROR] Failed: {e}")
        
        # 5e. Get User Positions - With Sorting Options (Data API)
        if user_address:
            print_section("5e. GET USER POSITIONS - With Sorting Options (Data API)")
            try:
                # Test different sort options
                sort_options = ["CURRENT", "INITIAL", "TOKENS", "CASHPNL", "PERCENTPNL", "TITLE", "PRICE", "AVGPRICE"]
                
                for sort_by in sort_options[:3]:  # Test first 3 to avoid too many requests
                    try:
                        result = client.get_user_positions(
                            user=user_address,
                            limit=5,
                            offset=0,
                            sort_by=sort_by,
                            sort_direction="DESC"
                        )
                        print_result(f"GET /positions (sortBy={sort_by})", result, max_length=300)
                    except Exception as e:
                        print(f"\n[WARNING] Failed with sortBy={sort_by}: {e}")
            except Exception as e:
                print(f"\n[ERROR] Failed: {e}")
        
        # 5f. Get User Positions - With Title Filter (Data API)
        if user_address:
            print_section("5f. GET USER POSITIONS - With Title Filter (Data API)")
            try:
                result = client.get_user_positions(
                    user=user_address,
                    title="",  # You can set a specific title to filter by
                    limit=10,
                    offset=0
                )
                print_result(f"GET /positions (user={user_address[:10]}..., with title filter)", result)
            except Exception as e:
                print(f"\n[ERROR] Failed: {e}")
        
        # 6. Get User Balance (Data API)
        print_section("6. GET USER BALANCE (Data API)")
        try:
            client.use_data_api()
            result = client.get_user_balance()
            print_result("GET /balance (or /user/balance)", result)
        except Exception as e:
            print(f"\n[ERROR] Failed: {e}")
            print("  Note: This endpoint may require different authentication or endpoint path")
    
    # ========================================================================
    # Summary
    # ========================================================================
    
    print("\n" + "=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    print("\nGAMMA API - Market Discovery (https://gamma-api.polymarket.com):")
    print("  1. get_markets() - List markets")
    print("  2. get_market(market_id) - Get market details")
    print("\nCLOB API - Order Management (https://clob.polymarket.com):")
    print("  3. get_orderbook(market_id) - Get orderbook")
    print("  4. get_trades(market_id, limit) - Get trades")
    print("\nDATA API - User Positions (https://data-api.polymarket.com):")
    print("  5. get_user_positions() - Get user positions (basic)")
    print("  5b. GET /positions - With user address and parameters")
    print("  5c. GET /positions - With market filter")
    print("  5d. GET /positions - With event ID filter")
    print("  5e. GET /positions - With sorting options")
    print("  6. get_user_balance() - Get user balance")
    print("\nAll endpoints tested. Check results above to see which ones work.")
    print("\nNote: Data API endpoints require:")
    print("  - Valid API credentials (API key, secret, passphrase, private key)")
    print("  - User address parameter for position queries")
    print("  - Proper authentication headers")
    print("\nNote: Market-specific endpoints require valid market IDs from Gamma API.")
    print("Note: Some endpoints may require additional parameters or authentication.")

if __name__ == "__main__":
    test_all_endpoints()

