"""
Test script to debug API date filtering for Polymarket and Kalshi.
This script tests various date filtering parameters to see which ones work.
"""
import sys
import os
from datetime import datetime, timezone, timedelta

# Add project root to Python path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.data_collectors.polymarket_client import PolymarketClient
from src.data_collectors.kalshi_client import KalshiClient

# Initialize clients (matching notebook initialization)
print("Initializing API clients...")
try:
    polymarket_client = PolymarketClient()
    print("[OK] Polymarket client initialized")
except Exception as e:
    print(f"[ERROR] Failed to initialize Polymarket client: {e}")
    polymarket_client = None

try:
    kalshi_client = KalshiClient()
    print("[OK] Kalshi client initialized")
except Exception as e:
    print(f"[ERROR] Failed to initialize Kalshi client: {e}")
    kalshi_client = None

if not polymarket_client or not kalshi_client:
    print("\n[WARNING] One or both clients failed to initialize. Some features may be unavailable.")

def parse_date_field(date_value):
    """Parse date from various formats."""
    if date_value is None:
        return None
    try:
        if isinstance(date_value, str):
            if 'T' in date_value:
                date_str = date_value.replace('Z', '+00:00')
                return datetime.fromisoformat(date_str)
            else:
                return datetime.strptime(date_value, '%Y-%m-%d')
        elif isinstance(date_value, (int, float)):
            return datetime.fromtimestamp(date_value)
    except:
        pass
    return None

def test_polymarket_events_filtering():
    """Test Polymarket events API with various date filtering parameters."""
    print("=" * 100)
    print("TESTING POLYMARKET EVENTS API DATE FILTERING")
    print("=" * 100)
    
    # Target date: January 4, 2026, 11 AM - 3 PM EST
    target_date = datetime(2026, 1, 4)
    est_offset = timedelta(hours=-5)
    est_tz = timezone(est_offset)
    
    start_time_est = datetime(2026, 1, 4, 11, 0, 0, tzinfo=est_tz)
    end_time_est = datetime(2026, 1, 4, 15, 0, 0, tzinfo=est_tz)
    
    start_time_utc = start_time_est.astimezone(timezone.utc)
    end_time_utc = end_time_est.astimezone(timezone.utc)
    
    min_ts = int(start_time_utc.timestamp())
    max_ts = int(end_time_utc.timestamp())
    target_date_str = target_date.strftime('%Y-%m-%d')
    
    print(f"\nTarget Window:")
    print(f"  EST: {start_time_est.strftime('%Y-%m-%d %H:%M:%S %Z')} to {end_time_est.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"  UTC: {start_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC')} to {end_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"  Timestamps: {min_ts} to {max_ts}")
    print(f"  Date string: {target_date_str}")
    
    if not polymarket_client:
        print("  ERROR: Polymarket client not initialized. Skipping tests.")
        return
    
    client = polymarket_client
    
    # Test 1: No date filtering (baseline)
    print(f"\n{'='*100}")
    print("TEST 1: No date filtering (baseline - should return all events)")
    print(f"{'='*100}")
    try:
        original_url = client.base_url
        client.use_gamma_api()
        try:
            response = client._request("GET", "/events", {"limit": 10, "offset": 0})
        finally:
            client.base_url = original_url
        
        events = []
        if isinstance(response, list):
            events = response[:10]
        elif isinstance(response, dict):
            events = response.get('events', [])[:10]
            if not events:
                events = response.get('data', [])[:10]
        
        print(f"  Returned {len(events)} events")
        if events:
            sample = events[0]
            print(f"  Sample event date fields:")
            for field in ['endDate', 'expirationDate', 'startDate', 'createdDate', 'end_date', 'expiration_date']:
                val = sample.get(field)
                if val:
                    parsed = parse_date_field(val)
                    print(f"    {field}: {val} -> {parsed}")
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Try various parameter combinations
    test_params = [
        {
            "name": "min_end_ts / max_end_ts (timestamps)",
            "params": {
                "limit": 10,
                "offset": 0,
                "min_end_ts": min_ts,
                "max_end_ts": max_ts,
            }
        },
        {
            "name": "endDate (date string)",
            "params": {
                "limit": 10,
                "offset": 0,
                "endDate": target_date_str,
            }
        },
        {
            "name": "expirationDate (date string)",
            "params": {
                "limit": 10,
                "offset": 0,
                "expirationDate": target_date_str,
            }
        },
        {
            "name": "min_expiration_ts / max_expiration_ts",
            "params": {
                "limit": 10,
                "offset": 0,
                "min_expiration_ts": min_ts,
                "max_expiration_ts": max_ts,
            }
        },
        {
            "name": "min_resolution_ts / max_resolution_ts",
            "params": {
                "limit": 10,
                "offset": 0,
                "min_resolution_ts": min_ts,
                "max_resolution_ts": max_ts,
            }
        },
        {
            "name": "Combined: endDate + min_end_ts",
            "params": {
                "limit": 10,
                "offset": 0,
                "endDate": target_date_str,
                "min_end_ts": min_ts,
                "max_end_ts": max_ts,
            }
        },
        {
            "name": "order by endDate descending",
            "params": {
                "limit": 10,
                "offset": 0,
                "order": "endDate",
                "ascending": "false",
            }
        },
    ]
    
    for test in test_params:
        print(f"\n{'='*100}")
        print(f"TEST: {test['name']}")
        print(f"{'='*100}")
        print(f"  Parameters: {test['params']}")
        
        try:
            original_url = client.base_url
            client.use_gamma_api()
            try:
                # Log the actual request URL and params
                import urllib.parse
                url = f"{client.base_url}/events"
                query_string = urllib.parse.urlencode(test['params'])
                full_url = f"{url}?{query_string}"
                print(f"  Request URL: {full_url}")
                
                response = client._request("GET", "/events", test['params'])
            finally:
                client.base_url = original_url
            
            events = []
            if isinstance(response, list):
                events = response
            elif isinstance(response, dict):
                events = response.get('events', [])
                if not events:
                    events = response.get('data', [])
            
            print(f"  Returned {len(events)} events")
            
            # Check if any events are within our target window
            in_window = 0
            out_of_window = 0
            sample_dates = []
            
            for event in events[:5]:  # Check first 5
                end_date = event.get('endDate') or event.get('expirationDate')
                if end_date:
                    parsed = parse_date_field(end_date)
                    if parsed:
                        event_ts = int(parsed.timestamp())
                        sample_dates.append((end_date, parsed, event_ts))
                        if min_ts <= event_ts <= max_ts:
                            in_window += 1
                        else:
                            out_of_window += 1
            
            print(f"  Events in target window: {in_window}")
            print(f"  Events outside target window: {out_of_window}")
            if sample_dates:
                print(f"  Sample dates from returned events:")
                for date_str, parsed, ts in sample_dates[:3]:
                    print(f"    {date_str} -> {parsed} (ts: {ts})")
                    if min_ts <= ts <= max_ts:
                        print(f"      [IN WINDOW]")
                    else:
                        print(f"      [OUT OF WINDOW] (target: {min_ts} to {max_ts})")
        
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()

def test_kalshi_markets_filtering():
    """Test Kalshi markets API with date filtering parameters."""
    print("\n\n")
    print("=" * 100)
    print("TESTING KALSHI MARKETS API DATE FILTERING")
    print("=" * 100)
    
    # Target date: January 4, 2026, 11 AM - 3 PM EST
    target_date = datetime(2026, 1, 4)
    est_offset = timedelta(hours=-5)
    est_tz = timezone(est_offset)
    
    start_time_est = datetime(2026, 1, 4, 11, 0, 0, tzinfo=est_tz)
    end_time_est = datetime(2026, 1, 4, 15, 0, 0, tzinfo=est_tz)
    
    start_time_utc = start_time_est.astimezone(timezone.utc)
    end_time_utc = end_time_est.astimezone(timezone.utc)
    
    min_ts = int(start_time_utc.timestamp())
    max_ts = int(end_time_utc.timestamp())
    
    print(f"\nTarget Window:")
    print(f"  EST: {start_time_est.strftime('%Y-%m-%d %H:%M:%S %Z')} to {end_time_est.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"  UTC: {start_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC')} to {end_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"  Timestamps: {min_ts} to {max_ts}")
    
    if not kalshi_client:
        print("  ERROR: Kalshi client not initialized. Skipping tests.")
        return
    
    client = kalshi_client
    
    # Test 1: No date filtering (baseline)
    print(f"\n{'='*100}")
    print("TEST 1: No date filtering (baseline - should return all markets)")
    print(f"{'='*100}")
    try:
        response = client.get_markets(limit=10)
        markets = response.get('markets', [])
        if not markets and isinstance(response, list):
            markets = response[:10]
        
        print(f"  Returned {len(markets)} markets")
        if markets:
            sample = markets[0]
            print(f"  Sample market date fields:")
            for field in ['close_time', 'open_time', 'settlement_time']:
                val = sample.get(field)
                if val:
                    if isinstance(val, (int, float)):
                        dt = datetime.fromtimestamp(val)
                        print(f"    {field}: {val} -> {dt}")
                    else:
                        print(f"    {field}: {val}")
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Inspect SDK method signature to see what parameters are accepted
    print(f"\n{'='*100}")
    print("TEST 2: Inspecting SDK get_markets method signature")
    print(f"{'='*100}")
    try:
        import inspect
        if hasattr(client.client, 'get_markets'):
            sig = inspect.signature(client.client.get_markets)
            params = list(sig.parameters.keys())
            print(f"  Accepted parameters: {params}")
            print(f"  Note: Date filtering parameters may not be supported by the SDK")
        else:
            print("  Could not inspect method signature")
    except Exception as e:
        print(f"  Could not inspect: {e}")
    
    # Test 3: With min_close_ts and max_close_ts (snake_case)
    print(f"\n{'='*100}")
    print("TEST 3: With min_close_ts and max_close_ts (snake_case)")
    print(f"{'='*100}")
    print(f"  Parameters: min_close_ts={min_ts}, max_close_ts={max_ts}")
    
    try:
        response = client.get_markets(
            limit=10,
            min_close_ts=min_ts,
            max_close_ts=max_ts
        )
        markets = response.get('markets', [])
        if not markets and isinstance(response, list):
            markets = response
        
        print(f"  Returned {len(markets)} markets")
        
        # Check if markets are within our target window
        in_window = 0
        out_of_window = 0
        sample_dates = []
        
        for market in markets[:5]:  # Check first 5
            close_time = market.get('close_time')
            if close_time:
                if isinstance(close_time, (int, float)):
                    sample_dates.append((close_time, datetime.fromtimestamp(close_time), close_time))
                    if min_ts <= close_time <= max_ts:
                        in_window += 1
                    else:
                        out_of_window += 1
                else:
                    parsed = parse_date_field(close_time)
                    if parsed:
                        event_ts = int(parsed.timestamp())
                        sample_dates.append((close_time, parsed, event_ts))
                        if min_ts <= event_ts <= max_ts:
                            in_window += 1
                        else:
                            out_of_window += 1
        
        print(f"  Markets in target window: {in_window}")
        print(f"  Markets outside target window: {out_of_window}")
        if sample_dates:
            print(f"  Sample close_time values from returned markets:")
            for val, parsed, ts in sample_dates[:3]:
                print(f"    {val} -> {parsed} (ts: {ts})")
                if min_ts <= ts <= max_ts:
                    print(f"      [IN WINDOW]")
                else:
                    print(f"      [OUT OF WINDOW] (target: {min_ts} to {max_ts})")
    
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Try alternative parameter names (camelCase)
    print(f"\n{'='*100}")
    print("TEST 4: Alternative parameter names (minCloseTs, maxCloseTs - camelCase)")
    print(f"{'='*100}")
    print(f"  Parameters: minCloseTs={min_ts}, maxCloseTs={max_ts}")
    print(f"  Note: This will likely fail as SDK uses strict parameter validation")
    
    try:
        response = client.get_markets(
            limit=10,
            minCloseTs=min_ts,
            maxCloseTs=max_ts
        )
        markets = response.get('markets', [])
        if not markets and isinstance(response, list):
            markets = response
        
        print(f"  Returned {len(markets)} markets")
        if markets:
            print(f"  First market close_time: {markets[0].get('close_time')}")
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\n" + "=" * 100)
    print("API DATE FILTERING TEST SCRIPT")
    print("=" * 100)
    print("\nThis script tests date filtering parameters for both Polymarket and Kalshi APIs.")
    print("It will help identify which parameters work and which don't.\n")
    
    # Test Polymarket
    test_polymarket_events_filtering()
    
    # Test Kalshi
    test_kalshi_markets_filtering()
    
    print("\n\n" + "=" * 100)
    print("TESTING COMPLETE")
    print("=" * 100)
    print("\nReview the results above to see:")
    print("  1. Which parameters are accepted by each API")
    print("  2. Whether the filtering actually works (events in vs out of window)")
    print("  3. What date fields are available in the responses")
    print("=" * 100)

