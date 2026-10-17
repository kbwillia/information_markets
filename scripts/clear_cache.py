"""
Script to clear the market cache and force a fresh data refresh.
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.data_manager import DataManager
from src.core.cache import MarketCache

def clear_cache():
    """Clear all cached market data."""
    print("Clearing market cache...")
    
    # Create cache instance
    cache = MarketCache()
    
    # Invalidate all markets for both platforms
    print("  Clearing Kalshi markets cache...")
    cache.invalidate(platform='kalshi', data_type='markets')
    
    print("  Clearing Polymarket markets cache...")
    cache.invalidate(platform='polymarket', data_type='markets')
    
    # Also clear individual market caches
    cache.invalidate(platform='kalshi', data_type='market')
    cache.invalidate(platform='polymarket', data_type='market')
    
    print("Cache cleared!")
    
    # Show cache stats
    stats = cache.get_cache_stats()
    print(f"\nCache stats after clearing:")
    print(f"  Memory entries: {stats['memory_entries']}")
    print(f"  DB entries: {stats['db_entries']}")
    print(f"  By platform: {stats['by_platform']}")
    
    return cache

def refresh_data():
    """Clear cache and refresh data from APIs."""
    print("=" * 60)
    print("Clearing cache and refreshing market data...")
    print("=" * 60)
    
    # Clear cache
    cache = clear_cache()
    
    # Create data manager and refresh
    print("\nRefreshing market data from APIs...")
    dm = DataManager(cache=cache)
    
    print("\nRefreshing Kalshi markets...")
    dm._refresh_kalshi_markets()
    
    print("\nRefreshing Polymarket markets...")
    dm._refresh_polymarket_markets()
    
    # Show results
    kalshi_markets = dm.get_all_markets('kalshi')
    poly_markets = dm.get_all_markets('polymarket')
    
    print("\n" + "=" * 60)
    print("Refresh complete!")
    print("=" * 60)
    print(f"Kalshi markets: {len(kalshi_markets)}")
    print(f"Polymarket markets: {len(poly_markets)}")
    print(f"Total markets: {len(kalshi_markets) + len(poly_markets)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Clear market cache and optionally refresh data")
    parser.add_argument('--refresh', action='store_true', 
                       help='Refresh data from APIs after clearing cache')
    args = parser.parse_args()
    
    if args.refresh:
        refresh_data()
    else:
        clear_cache()
        print("\nTo refresh data, run: python scripts/clear_cache.py --refresh")

