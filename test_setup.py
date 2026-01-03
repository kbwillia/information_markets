"""Test script to verify setup and configuration."""
import sys
import os

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import requests
        import pandas
        import numpy
        import matplotlib
        import seaborn
        import praw
        print("✓ All core dependencies imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("  Run: pip install -r requirements.txt")
        return False

def test_config():
    """Test configuration loading."""
    print("\nTesting configuration...")
    try:
        from src.config import Config
        print(f"✓ Config loaded")
        print(f"  Kalshi API Key: {'Set' if Config.KALSHI_API_KEY else 'Not set'}")
        print(f"  Reddit Client ID: {'Set' if Config.REDDIT_CLIENT_ID else 'Not set'}")
        print(f"  Ollama URL: {Config.OLLAMA_BASE_URL}")
        print(f"  Ollama Model: {Config.OLLAMA_MODEL}")
        return True
    except Exception as e:
        print(f"✗ Config error: {e}")
        return False

def test_ollama():
    """Test Ollama connection."""
    print("\nTesting Ollama connection...")
    try:
        import requests
        from src.config import Config
        
        response = requests.get(f"{Config.OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [m.get('name', '') for m in models]
            print(f"✓ Ollama is running")
            print(f"  Available models: {', '.join(model_names) if model_names else 'None'}")
            
            if Config.OLLAMA_MODEL in [m.split(':')[0] for m in model_names]:
                print(f"  ✓ Model '{Config.OLLAMA_MODEL}' is available")
            else:
                print(f"  ⚠ Model '{Config.OLLAMA_MODEL}' not found. Run: ollama pull {Config.OLLAMA_MODEL}")
            return True
        else:
            print(f"✗ Ollama returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to Ollama")
        print("  Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"✗ Ollama test error: {e}")
        return False

def test_database():
    """Test database initialization."""
    print("\nTesting database...")
    try:
        from src.wallet_tracker.wallet_tracker import WalletTracker
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        tracker = WalletTracker()
        print("✓ Database initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def test_reddit():
    """Test Reddit API connection."""
    print("\nTesting Reddit API...")
    try:
        from src.reddit.reddit_scraper import RedditScraper
        from src.config import Config
        
        if not Config.REDDIT_CLIENT_ID or not Config.REDDIT_CLIENT_SECRET:
            print("⚠ Reddit credentials not set (optional)")
            return True
        
        scraper = RedditScraper()
        # Try to access a public subreddit
        posts = scraper.get_posts_from_subreddit("test", limit=1)
        print("✓ Reddit API connection successful")
        return True
    except Exception as e:
        print(f"⚠ Reddit API test failed: {e}")
        print("  Reddit integration is optional")
        return True  # Don't fail the whole test

def main():
    """Run all tests."""
    print("=" * 50)
    print("Trading Bot Setup Verification")
    print("=" * 50)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Database", test_database()))
    results.append(("Ollama", test_ollama()))
    results.append(("Reddit", test_reddit()))
    
    print("\n" + "=" * 50)
    print("Summary")
    print("=" * 50)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✓ All critical tests passed!")
        print("You're ready to start using the trading bot.")
    else:
        print("\n⚠ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

