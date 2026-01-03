"""Test script to verify Kalshi and Polymarket API keys and connections."""
import sys
import os
from datetime import datetime
import requests

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_success(message):
    """Print success message."""
    try:
        print(f"✓ {message}")
    except UnicodeEncodeError:
        print(f"[OK] {message}")

def print_error(message):
    """Print error message."""
    try:
        print(f"✗ {message}")
    except UnicodeEncodeError:
        print(f"[ERROR] {message}")

def print_warning(message):
    """Print warning message."""
    try:
        print(f"⚠ {message}")
    except UnicodeEncodeError:
        print(f"[WARNING] {message}")

def print_info(message):
    """Print info message."""
    print(f"  {message}")

def test_kalshi_api():
    """Test Kalshi API connection and authentication."""
    print_header("Testing Kalshi API")
    
    try:
        from src.config import Config
        from src.data_collectors.kalshi_client import KalshiClient
        
        # Check if API keys are set
        if not Config.KALSHI_API_KEY:
            print_error("Kalshi API key not configured in .env file")
            print_info("Required: KALSHI_API_KEY (API key ID from Kalshi account)")
            return False
        
        has_private_key = bool(Config.KALSHI_PRIVATE_KEY_PATH or Config.KALSHI_PRIVATE_KEY_PEM)
        if not has_private_key:
            print_error("Kalshi private key not configured in .env file")
            print_info("Required: KALSHI_PRIVATE_KEY_PATH (path to .pem file) OR KALSHI_PRIVATE_KEY_PEM (key content)")
            print_info("Get your private key from: https://kalshi.com/account/profile")
            return False
        
        print_info(f"API Key ID: {Config.KALSHI_API_KEY[:10]}...{Config.KALSHI_API_KEY[-4:]}")
        if Config.KALSHI_PRIVATE_KEY_PATH:
            print_info(f"Private Key: {Config.KALSHI_PRIVATE_KEY_PATH}")
        else:
            print_info("Private Key: Provided as PEM content")
        print_info(f"Base URL: {Config.KALSHI_BASE_URL}")
        
        # Initialize client
        print_info("Initializing Kalshi client (using official SDK)...")
        try:
            client = KalshiClient()
        except ImportError as e:
            print_error("Kalshi SDK not installed")
            print_info("Install with: pip install kalshi-python-sync")
            return False
        except Exception as e:
            print_error(f"Failed to initialize client: {e}")
            print_info("Check that your private key file exists and is valid")
            return False
        
        # Test 1: Exchange status (public endpoint, no auth required)
        print_info("\nTest 1: Checking exchange status (public endpoint)...")
        try:
            status = client.get_exchange_status()
            print_success("Exchange status retrieved")
            print_info(f"  Status: {status}")
        except requests.exceptions.ConnectionError as e:
            print_warning("Network connection failed - cannot reach Kalshi API")
            print_info("  This could be a network issue or the API endpoint may have changed")
            print_info("  Check your internet connection and verify the API URL")
            return False
        except Exception as e:
            print_warning(f"Exchange status check failed: {e}")
            print_info("  This might be normal if the endpoint structure differs")
        
        # Test 2: Get markets (public endpoint)
        print_info("\nTest 2: Fetching markets (public endpoint)...")
        try:
            markets = client.get_markets(limit=100)
            # Handle different response formats
            if isinstance(markets, dict):
                market_list = markets.get("markets", markets.get("data", []))
            elif hasattr(markets, 'markets'):
                market_list = markets.markets
            elif hasattr(markets, 'data'):
                market_list = markets.data
            elif isinstance(markets, list):
                market_list = markets
            else:
                market_list = []
            
            market_count = len(market_list) if isinstance(market_list, list) else 0
            print_success(f"Markets retrieved: {market_count} markets")
            if market_count > 0:
                sample_market = market_list[0] if isinstance(market_list, list) else {}
                if isinstance(sample_market, dict):
                    title = sample_market.get('title', sample_market.get('event_ticker', 'N/A'))
                elif hasattr(sample_market, 'title'):
                    title = sample_market.title
                else:
                    title = str(sample_market)[:50]
                print_info(f"  Sample market: {title[:50]}...")
        except requests.exceptions.ConnectionError as e:
            print_error("Network connection failed - cannot reach Kalshi API")
            print_info("  Check your internet connection and verify the API URL")
            return False
        except Exception as e:
            print_error(f"Failed to fetch markets: {e}")
            return False
        
        # Test 3: Get portfolio/balance (requires authentication)
        print_info("\nTest 3: Checking account balance (authenticated endpoint)...")
        try:
            balance = client.get_balance()
            print_success("Account balance retrieved - Authentication successful!")
            print_info(f"  Balance data: {balance}")
            return True
        except requests.exceptions.ConnectionError as e:
            print_error("Network connection failed - cannot reach Kalshi API")
            print_info("  Check your internet connection and verify the API URL")
            return False
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "Unauthorized" in error_msg or "authentication" in error_msg.lower():
                print_error("Authentication failed - Invalid API credentials")
                print_info("  Please verify your KALSHI_API_KEY and KALSHI_API_SECRET")
            elif "403" in error_msg or "Forbidden" in error_msg:
                print_error("Access forbidden - API key may not have required permissions")
            else:
                print_error(f"Failed to get balance: {e}")
            return False
        
    except ImportError as e:
        print_error(f"Failed to import Kalshi client: {e}")
        print_info("  Make sure all dependencies are installed: pip install -r requirements.txt")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def test_polymarket_api():
    """Test Polymarket API connection and authentication."""
    print_header("Testing Polymarket API")
    
    try:
        from src.config import Config
        from src.data_collectors.polymarket_client import PolymarketClient
        
        # Check if API key is set
        if not Config.POLYMARKET_API_KEY:
            print_warning("Polymarket API key not configured (optional)")
            print_info("  Some Polymarket endpoints may work without authentication")
            print_info("  Set POLYMARKET_API_KEY in .env for authenticated endpoints")
        
        print_info(f"Base URL: {Config.POLYMARKET_BASE_URL}")
        if Config.POLYMARKET_API_KEY:
            print_info(f"API Key: {Config.POLYMARKET_API_KEY[:10]}...{Config.POLYMARKET_API_KEY[-4:]}")
        
        # Initialize client
        print_info("Initializing Polymarket client...")
        client = PolymarketClient()
        
        # Test 1: Get markets (public endpoint)
        print_info("\nTest 1: Fetching markets (public endpoint)...")
        try:
            markets = client.get_markets(limit=5)
            market_list = markets.get("markets", []) if isinstance(markets, dict) else markets
            market_count = len(market_list) if isinstance(market_list, list) else 0
            
            if market_count > 0:
                print_success(f"Markets retrieved: {market_count} markets")
                sample_market = market_list[0] if isinstance(market_list, list) else {}
                market_title = sample_market.get("question", sample_market.get("title", "N/A"))
                print_info(f"  Sample market: {market_title[:50]}...")
            else:
                print_warning("No markets returned (API structure may differ)")
                print_info(f"  Response: {str(markets)[:200]}...")
        except requests.exceptions.ConnectionError as e:
            print_error("Network connection failed - cannot reach Polymarket API")
            print_info("  Check your internet connection and verify the API URL")
            return False
        except Exception as e:
            print_error(f"Failed to fetch markets: {e}")
            print_info("  Note: Polymarket API structure may have changed")
            return False
        
        # Test 2: Get user balance (requires authentication)
        if Config.POLYMARKET_API_KEY:
            print_info("\nTest 2: Checking account balance (authenticated endpoint)...")
            try:
                balance = client.get_user_balance()
                print_success("Account balance retrieved - Authentication successful!")
                print_info(f"  Balance data: {balance}")
                return True
            except Exception as e:
                error_msg = str(e)
                if "401" in error_msg or "Unauthorized" in error_msg or "authentication" in error_msg.lower():
                    print_error("Authentication failed - Invalid API key")
                    print_info("  Please verify your POLYMARKET_API_KEY")
                elif "403" in error_msg or "Forbidden" in error_msg:
                    print_error("Access forbidden - API key may not have required permissions")
                else:
                    print_warning(f"Balance check failed: {e}")
                    print_info("  This endpoint may require different authentication")
                return False
        else:
            print_info("\nTest 2: Skipping authenticated endpoints (no API key)")
            print_success("Public endpoints working - API connection successful!")
            return True
        
    except ImportError as e:
        print_error(f"Failed to import Polymarket client: {e}")
        print_info("  Make sure all dependencies are installed: pip install -r requirements.txt")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def test_arbitrage_detector():
    """Test arbitrage detector (requires both APIs to work)."""
    print_header("Testing Arbitrage Detector")
    
    try:
        from src.data_collectors.arbitrage_detector import ArbitrageDetector
        
        print_info("Initializing arbitrage detector...")
        detector = ArbitrageDetector()
        
        print_info("Scanning for arbitrage opportunities (this may take a moment)...")
        opportunities = detector.scan_for_arbitrage(limit=20)
        
        if opportunities:
            print_success(f"Found {len(opportunities)} arbitrage opportunities!")
            print_info("  Top opportunities:")
            for i, opp in enumerate(opportunities[:3], 1):
                print_info(f"    {i}. {opp.get('market_title', 'Unknown')[:40]}...")
                print_info(f"       Profit: {opp.get('profit', 0):.2%}")
        else:
            print_info("No arbitrage opportunities found at this time")
            print_info("  This is normal - arbitrage opportunities are rare")
        
        return True
        
    except Exception as e:
        print_error(f"Arbitrage detector test failed: {e}")
        return False

def main():
    """Run all API tests."""
    print("\n" + "=" * 60)
    print("  API Keys Test Suite")
    print("  " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print_warning(".env file not found!")
        print_info("  Copy config.example.env to .env and add your API keys")
        print_info("  Run: cp config.example.env .env")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    results = []
    
    # Test Kalshi
    kalshi_result = test_kalshi_api()
    results.append(("Kalshi API", kalshi_result))
    
    # Test Polymarket
    polymarket_result = test_polymarket_api()
    results.append(("Polymarket API", polymarket_result))
    
    # Test arbitrage (if both work)
    if kalshi_result and polymarket_result:
        arbitrage_result = test_arbitrage_detector()
        results.append(("Arbitrage Detector", arbitrage_result))
    
    # Summary
    print_header("Test Summary")
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name:.<40} {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print_success("All API tests passed!")
        print_info("Your API keys are configured correctly and working.")
    else:
        print_warning("Some API tests failed.")
        print_info("Please check:")
        print_info("  1. API keys are set correctly in .env file")
        print_info("  2. API keys are valid and not expired")
        print_info("  3. API keys have required permissions")
        print_info("  4. Network connection is working")
        print_info("  5. API endpoints are accessible")
    
    print("=" * 60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

