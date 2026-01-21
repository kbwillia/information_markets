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
    
    # 3. Get Events (Gamma API)
    print_section("3. GET EVENTS (Gamma API)")
    try:
        result = client.get_events(limit=5)
        print_result("GET /events (limit=5)", result)
        
        # Extract an event ID for subsequent tests
        event_list = result.get("events", [])
        if not event_list and isinstance(result, list):
            event_list = result[:1]
        elif isinstance(result, dict) and 'data' in result:
            event_list = result['data'][:1] if isinstance(result['data'], list) else []
        
        test_event_id = None
        if event_list:
            test_event_id = event_list[0].get('id') or event_list[0].get('slug')
            if test_event_id:
                print(f"\n  Using event ID for subsequent tests: {test_event_id}")
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
        test_event_id = None
    
    # 4. Get Event Details (Gamma API)
    if test_event_id:
        print_section("4. GET EVENT DETAILS (Gamma API)")
        try:
            result = client.get_event(test_event_id)
            print_result(f"GET /events/{test_event_id}", result)
        except Exception as e:
            print(f"\n[ERROR] Failed: {e}")
    
    # 5. Get Categories (Gamma API)
    print_section("5. GET CATEGORIES (Gamma API)")
    try:
        result = client.get_categories()
        print_result("GET /categories", result)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # 6. Get Tags (Gamma API)
    print_section("6. GET TAGS (Gamma API)")
    try:
        result = client.get_tags()
        print_result("GET /tags", result)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # 7. Search (Gamma API)
    print_section("7. SEARCH (Gamma API)")
    try:
        result = client.search("election", limit=5)
        print_result("GET /search (q='election', limit=5)", result)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # 8. Get Notifications (Gamma API)
    print_section("8. GET NOTIFICATIONS (Gamma API)")
    try:
        result = client.get_notifications(limit=5)
        print_result("GET /notifications (limit=5)", result)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # 9. Get Resolution Requests (Gamma API)
    print_section("9. GET RESOLUTION REQUESTS (Gamma API)")
    try:
        result = client.get_resolution_requests(limit=5)
        print_result("GET /resolution-requests (limit=5)", result)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # 10. Get Series (Gamma API)
    print_section("10. GET SERIES (Gamma API)")
    try:
        result = client.get_series(limit=5)
        print_result("GET /series (limit=5)", result)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # 11. Get Sports (Gamma API)
    print_section("11. GET SPORTS (Gamma API)")
    try:
        result = client.get_sports()
        print_result("GET /sports", result)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # 12. Get Teams (Gamma API)
    print_section("12. GET TEAMS (Gamma API)")
    try:
        result = client.get_teams()
        print_result("GET /teams", result)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # 13. Get Leagues (Gamma API)
    print_section("13. GET LEAGUES (Gamma API)")
    try:
        result = client.get_leagues()
        print_result("GET /leagues", result)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # 14. Get Comments (Gamma API)
    if test_market_id:
        print_section("14. GET COMMENTS (Gamma API)")
        try:
            result = client.get_comments(market_id=test_market_id, limit=5)
            print_result(f"GET /comments (market={test_market_id[:20]}..., limit=5)", result)
        except Exception as e:
            print(f"\n[ERROR] Failed: {e}")
    
    # 15. Get Comment Details (Gamma API)
    if test_market_id:
        print_section("15. GET COMMENT DETAILS (Gamma API)")
        try:
            # First get comments to find a comment ID
            comments = client.get_comments(market_id=test_market_id, limit=1)
            comment_list = comments.get("comments", [])
            if not comment_list and isinstance(comments, list):
                comment_list = comments[:1]
            elif isinstance(comments, dict) and 'data' in comments:
                comment_list = comments['data'][:1] if isinstance(comments['data'], list) else []
            
            if comment_list:
                comment_id = comment_list[0].get('id')
                if comment_id:
                    result = client.get_comment(comment_id)
                    print_result(f"GET /comments/{comment_id}", result)
                else:
                    print("\n⚠ No comment ID found")
            else:
                print("\n⚠ No comments available")
        except Exception as e:
            print(f"\n[ERROR] Failed: {e}")
    
    # 16. Get Profile (Gamma API)
    print_section("16. GET PROFILE (Gamma API)")
    user_address = None  # Set this to a valid user address for testing
    if not user_address:
        print("\n⚠ Skipping - user address not provided")
        print("  To test this endpoint, set a valid user address in the test file")
    else:
        try:
            result = client.get_profile(user_address)
            print_result(f"GET /profiles/{user_address[:10]}...", result)
        except Exception as e:
            print(f"\n[ERROR] Failed: {e}")
    
    # 17. Get Health (Gamma API)
    print_section("17. GET HEALTH (Gamma API)")
    try:
        result = client.get_health()
        print_result("GET /health", result)
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
    
    # ========================================================================
    # CLOB API - Order Management, Prices, and Order Books
    # ========================================================================
    # NOTE: CLOB endpoints are commented out for now
    
    # print_section("CLOB API - Order Management")
    # 
    # # 10. Get Orderbook (CLOB API)
    # if test_market_id:
    #     print_section("10. GET ORDERBOOK (CLOB API)")
    #     try:
    #         client.use_clob_api()
    #         result = client.get_orderbook(test_market_id)
    #         print_result(f"GET /markets/{test_market_id}/orderbook", result)
    #     except Exception as e:
    #         print(f"\n[ERROR] Failed: {e}")
    # 
    # # 11. Get Trades (CLOB API)
    # if test_market_id:
    #     print_section("11. GET TRADES (CLOB API)")
    #     try:
    #         client.use_clob_api()
    #         result = client.get_trades(test_market_id, limit=5)
    #         print_result(f"GET /markets/{test_market_id}/trades (limit=5)", result)
    #     except Exception as e:
    #         print(f"\n[ERROR] Failed: {e}")
    # 
    # # 12. Place Order (CLOB API) - COMMENTED OUT
    # # print_section("12. PLACE ORDER (CLOB API)")
    # # try:
    # #     result = client.place_order_clob(
    # #         market_id=test_market_id,
    # #         side="BUY",
    # #         size=1.0,
    # #         price=0.5,
    # #         order_type="LIMIT"
    # #     )
    # #     print_result("POST /order", result)
    # # except Exception as e:
    # #     print(f"\n[ERROR] Failed: {e}")
    # 
    # # 13. Get Orders (CLOB API)
    # print_section("13. GET ORDERS (CLOB API)")
    # try:
    #     result = client.get_orders_clob(limit=5)
    #     print_result("GET /orders (limit=5)", result)
    # except Exception as e:
    #     print(f"\n[ERROR] Failed: {e}")
    # 
    # # 14. Get Book (CLOB API)
    # if test_market_id:
    #     print_section("14. GET BOOK (CLOB API)")
    #     try:
    #         result = client.get_book_clob(test_market_id)
    #         print_result(f"GET /book (token={test_market_id})", result)
    #     except Exception as e:
    #         print(f"\n[ERROR] Failed: {e}")
    # 
    # # 15. Get Prices History (CLOB API)
    # if test_market_id:
    #     print_section("15. GET PRICES HISTORY (CLOB API)")
    #     try:
    #         result = client.get_prices_history_clob(test_market_id, days=7)
    #         print_result(f"GET /prices-history (token={test_market_id}, days=7)", result)
    #     except Exception as e:
    #         print(f"\n[ERROR] Failed: {e}")
    # 
    # # 16. Get Midpoint (CLOB API)
    # if test_market_id:
    #     print_section("16. GET MIDPOINT (CLOB API)")
    #     try:
    #         result = client.get_midpoint_clob(test_market_id)
    #         print_result(f"GET /midpoint (token={test_market_id})", result)
    #     except Exception as e:
    #         print(f"\n[ERROR] Failed: {e}")
    # 
    # # 17. Get Spread (CLOB API)
    # if test_market_id:
    #     print_section("17. GET SPREAD (CLOB API)")
    #     try:
    #         result = client.get_spread_clob(test_market_id)
    #         print_result(f"GET /spread (token={test_market_id})", result)
    #     except Exception as e:
    #         print(f"\n[ERROR] Failed: {e}")
    # 
    # # 18. Get API Keys (CLOB API)
    # print_section("18. GET API KEYS (CLOB API)")
    # try:
    #     result = client.get_api_keys_clob()
    #     print_result("GET /api-keys", result)
    # except Exception as e:
    #     print(f"\n[ERROR] Failed: {e}")
    
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
        # 18. Get Global Stats (Data API)
        print_section("18. GET GLOBAL STATS (Data API)")
        try:
            result = client.get_global_stats()
            print_result("GET /stats/global", result)
        except Exception as e:
            print(f"\n[ERROR] Failed: {e}")
        
        # 19. Get Daily Stats (Data API)
        print_section("19. GET DAILY STATS (Data API)")
        try:
            result = client.get_daily_stats(days=7)
            print_result("GET /stats/daily (days=7)", result)
        except Exception as e:
            print(f"\n[ERROR] Failed: {e}")
        
        # 20. Get Market Volume (Data API)
        if test_market_id:
            print_section("20. GET MARKET VOLUME (Data API)")
            try:
                result = client.get_market_volume(test_market_id)
                print_result(f"GET /markets/{test_market_id}/volume", result)
            except Exception as e:
                print(f"\n[ERROR] Failed: {e}")
        
        # 21. Get Market Holders (Data API)
        if test_market_id:
            print_section("21. GET MARKET HOLDERS (Data API)")
            try:
                result = client.get_market_holders(test_market_id)
                print_result(f"GET /markets/{test_market_id}/holders", result)
            except Exception as e:
                print(f"\n[ERROR] Failed: {e}")
        
        # 22. Get Leaderboard (Data API)
        print_section("22. GET LEADERBOARD (Data API)")
        try:
            result = client.get_leaderboard(limit=10)
            print_result("GET /leaderboard (limit=10)", result)
        except Exception as e:
            print(f"\n[ERROR] Failed: {e}")
        
        # 23. Get User Activity (Data API)
        print_section("23. GET USER ACTIVITY (Data API)")
        # Note: This requires a user address - you may need to provide one
        user_address = None  # Set this to a valid user address for testing (e.g., "0x56687bf447db6ffa42ffe2204a05edaa20f55839")
        if not user_address:
            print("\n⚠ Skipping - user address not provided")
            print("  To test this endpoint, set a valid user address in the test file")
            print("  Example: user_address = '0x56687bf447db6ffa42ffe2204a05edaa20f55839'")
        else:
            try:
                result = client.get_user_activity(user_address, limit=10)
                print_result(f"GET /user/{user_address[:10]}.../activity (limit=10)", result)
            except Exception as e:
                print(f"\n[ERROR] Failed: {e}")
        
        # 24. Get User Profit (Data API)
        if user_address:
            print_section("24. GET USER PROFIT (Data API)")
            try:
                result = client.get_user_profit(user_address)
                print_result(f"GET /user/{user_address[:10]}.../profit", result)
            except Exception as e:
                print(f"\n[ERROR] Failed: {e}")
        
        # 25. Get User Value (Data API)
        if user_address:
            print_section("25. GET USER VALUE (Data API)")
            try:
                result = client.get_user_value(user_address)
                print_result(f"GET /value (user={user_address[:10]}...)", result)
            except Exception as e:
                print(f"\n[ERROR] Failed: {e}")
        
        # 26. Get User PnL (Data API)
        if user_address:
            print_section("26. GET USER PNL (Data API)")
            try:
                result = client.get_user_pnl(user_address)
                print_result(f"GET /pnl (user={user_address[:10]}...)", result)
            except Exception as e:
                print(f"\n[ERROR] Failed: {e}")
        
        # 27. Get Trades (Data API)
        print_section("27. GET TRADES (Data API)")
        try:
            result = client.get_trades(limit=10)
            print_result("GET /trades (limit=10)", result)
        except Exception as e:
            print(f"\n[ERROR] Failed: {e}")
        
        # 27b. Get Trades - With Filters (Data API)
        if user_address or test_market_id:
            print_section("27b. GET TRADES - With Filters (Data API)")
            try:
                params = {}
                if user_address:
                    params["user"] = user_address
                if test_market_id:
                    params["market"] = test_market_id
                result = client.get_trades(**params, limit=10)
                print_result(f"GET /trades (with filters, limit=10)", result)
            except Exception as e:
                print(f"\n[ERROR] Failed: {e}")
        
        # 28. Get Activity (Data API)
        print_section("28. GET ACTIVITY (Data API)")
        try:
            result = client.get_activity(limit=10)
            print_result("GET /activity (limit=10)", result)
        except Exception as e:
            print(f"\n[ERROR] Failed: {e}")
        
        # 28b. Get Activity - With User Filter (Data API)
        if user_address:
            print_section("28b. GET ACTIVITY - With User Filter (Data API)")
            try:
                result = client.get_activity(user=user_address, limit=10)
                print_result(f"GET /activity (user={user_address[:10]}..., limit=10)", result)
            except Exception as e:
                print(f"\n[ERROR] Failed: {e}")
        
        # 29. Get Orders History (Data API)
        print_section("29. GET ORDERS HISTORY (Data API)")
        try:
            result = client.get_orders_history(limit=10)
            print_result("GET /orders (limit=10)", result)
        except Exception as e:
            print(f"\n[ERROR] Failed: {e}")
        
        # 29b. Get Orders History - With User Filter (Data API)
        if user_address:
            print_section("29b. GET ORDERS HISTORY - With User Filter (Data API)")
            try:
                result = client.get_orders_history(user=user_address, limit=10)
                print_result(f"GET /orders (user={user_address[:10]}..., limit=10)", result)
            except Exception as e:
                print(f"\n[ERROR] Failed: {e}")
        
        # 30. Get Market Stats (Data API)
        if test_market_id:
            print_section("30. GET MARKET STATS (Data API)")
            try:
                result = client.get_market_stats(test_market_id)
                print_result(f"GET /stats/market/{test_market_id}", result)
            except Exception as e:
                print(f"\n[ERROR] Failed: {e}")
        
        # 31. Get User Positions - Basic (Data API)
        print_section("31. GET USER POSITIONS - Basic (Data API)")
        
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
        
        # 31b. Get User Positions - With Market Filter (Data API)
        if user_address and test_market_id:
            print_section("31b. GET USER POSITIONS - With Market Filter (Data API)")
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
        
        # 31c. Get User Positions - With Event ID Filter (Data API)
        if user_address:
            print_section("31c. GET USER POSITIONS - With Event ID Filter (Data API)")
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
        
        # 31d. Get User Positions - With Size Threshold (Data API)
        if user_address:
            print_section("31d. GET USER POSITIONS - With Size Threshold (Data API)")
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
        
        # 31e. Get User Positions - With Sorting Options (Data API)
        if user_address:
            print_section("31e. GET USER POSITIONS - With Sorting Options (Data API)")
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
        
        # 31f. Get User Positions - With Title Filter (Data API)
        if user_address:
            print_section("31f. GET USER POSITIONS - With Title Filter (Data API)")
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
        
        # 32. Get User Balance (Data API)
        print_section("32. GET USER BALANCE (Data API)")
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
    print("  3. get_events() - List events")
    print("  4. get_event(event_id) - Get event details")
    print("  5. get_categories() - List categories")
    print("  6. get_tags() - Get tags")
    print("  7. search(query) - Search markets/events")
    print("  8. get_notifications() - Get notifications")
    print("  9. get_resolution_requests() - Get pending resolutions")
    print("  10. get_series() - Get series groupings")
    print("  11. get_sports() - List sports")
    print("  12. get_teams() - Get teams")
    print("  13. get_leagues() - List leagues")
    print("  14. get_comments() - Get comments")
    print("  15. get_comment(comment_id) - Get comment details")
    print("  16. get_profile(address) - Get user profile")
    print("  17. get_health() - Health check")
    print("\nCLOB API - Order Management (https://clob.polymarket.com):")
    print("  [COMMENTED OUT FOR NOW]")
    print("  - Order management endpoints")
    print("  - Market data endpoints (book, prices-history, midpoint, spread)")
    print("  - API key management endpoints")
    print("\nDATA API - Analytics & User Data (https://data-api.polymarket.com):")
    print("  18. get_global_stats() - Global platform stats")
    print("  19. get_daily_stats() - Daily volume/trades")
    print("  20. get_market_volume(market_id) - Market volume")
    print("  21. get_market_holders(market_id) - Market holders")
    print("  22. get_leaderboard() - Top traders")
    print("  23. get_user_activity(address) - User trading history")
    print("  24. get_user_profit(address) - User PnL stats")
    print("  25. get_user_value(address) - User portfolio value")
    print("  26. get_user_pnl(address) - User PnL history")
    print("  27. get_trades() - List all trades")
    print("  28. get_activity() - General account activity")
    print("  29. get_orders_history() - Historical order history")
    print("  30. get_market_stats(condition_id) - Market stats")
    print("  31. get_user_positions() - Get user positions (basic)")
    print("  31b-31f. GET /positions - With various filters and sorting")
    print("  32. get_user_balance() - Get user balance")
    print("\nAll endpoints tested. Check results above to see which ones work.")
    print("\nNote: Data API endpoints require:")
    print("  - Valid API credentials (API key, secret, passphrase, private key)")
    print("  - User address parameter for position queries")
    print("  - Proper authentication headers")
    print("\nNote: Market-specific endpoints require valid market IDs from Gamma API.")
    print("Note: Some endpoints may require additional parameters or authentication.")

if __name__ == "__main__":
    test_all_endpoints()

