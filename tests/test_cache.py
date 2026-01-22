"""Tests for the caching layer."""
import pytest
import time
import tempfile
import os
from pathlib import Path

from src.core.cache import MarketCache


class TestMarketCache:
    """Test the MarketCache class."""
    
    @pytest.fixture
    def cache(self):
        """Create a temporary cache for testing."""
        tmpdir = tempfile.mkdtemp()
        cache_path = os.path.join(tmpdir, "test_cache.db")
        cache = MarketCache(db_path=cache_path)
        yield cache
        # Close connections to allow cleanup on Windows
        if hasattr(cache, '_local') and hasattr(cache._local, 'conn'):
            try:
                cache._local.conn.close()
            except:
                pass
    
    def test_set_and_get(self, cache):
        """Test basic set and get operations."""
        cache.set('kalshi', 'markets', [{'ticker': 'TEST'}])
        
        result = cache.get('kalshi', 'markets')
        assert result is not None
        assert len(result) == 1
        assert result[0]['ticker'] == 'TEST'
    
    def test_get_nonexistent(self, cache):
        """Test getting nonexistent data returns None."""
        result = cache.get('kalshi', 'markets')
        assert result is None
    
    def test_ttl_expiration(self, cache):
        """Test that cached data expires after TTL."""
        cache.set('kalshi', 'test', {'value': 1}, ttl_seconds=0.1)
        
        # Should be available immediately
        assert cache.get('kalshi', 'test') is not None
        
        # Wait for expiration
        time.sleep(0.2)
        
        # Should be expired
        assert cache.get('kalshi', 'test') is None
        
        # But should be available with allow_stale
        assert cache.get('kalshi', 'test', allow_stale=True) is not None
    
    def test_identifier(self, cache):
        """Test caching with identifiers."""
        cache.set('kalshi', 'market', {'ticker': 'A'}, identifier='A')
        cache.set('kalshi', 'market', {'ticker': 'B'}, identifier='B')
        
        a = cache.get('kalshi', 'market', 'A')
        b = cache.get('kalshi', 'market', 'B')
        
        assert a['ticker'] == 'A'
        assert b['ticker'] == 'B'
    
    def test_price_history(self, cache):
        """Test price history recording."""
        # Use different timestamps to avoid uniqueness constraint
        base_time = time.time()
        cache.record_price('TEST', 'kalshi', 0.50, volume=1000, timestamp=base_time)
        cache.record_price('TEST', 'kalshi', 0.52, volume=1100, timestamp=base_time + 1)
        cache.record_price('TEST', 'kalshi', 0.55, volume=1200, timestamp=base_time + 2)
        
        history = cache.get_price_history('TEST', 'kalshi', minutes=60)
        
        assert len(history) == 3
        assert history[0]['price'] == 0.50
        assert history[2]['price'] == 0.55
    
    def test_invalidate(self, cache):
        """Test cache invalidation."""
        cache.set('kalshi', 'markets', [{'ticker': 'TEST'}])
        cache.set('polymarket', 'markets', [{'id': 'TEST'}])
        
        # Invalidate kalshi only
        cache.invalidate(platform='kalshi')
        
        assert cache.get('kalshi', 'markets') is None
        assert cache.get('polymarket', 'markets') is not None
    
    def test_cache_stats(self, cache):
        """Test getting cache statistics."""
        cache.set('kalshi', 'markets', [])
        cache.set('polymarket', 'markets', [])
        cache.set('kalshi', 'orderbook', {}, identifier='TEST')
        
        stats = cache.get_cache_stats()
        
        assert stats['db_entries'] == 3
        assert stats['by_platform']['kalshi'] == 2
        assert stats['by_platform']['polymarket'] == 1


class TestCachePerformance:
    """Performance tests for the cache."""
    
    @pytest.fixture
    def cache(self):
        """Create a temporary cache for testing."""
        tmpdir = tempfile.mkdtemp()
        cache_path = os.path.join(tmpdir, "perf_cache.db")
        cache = MarketCache(db_path=cache_path)
        yield cache
        # Close connections to allow cleanup on Windows
        if hasattr(cache, '_local') and hasattr(cache._local, 'conn'):
            try:
                cache._local.conn.close()
            except:
                pass
    
    def test_bulk_write_performance(self, cache):
        """Test that bulk writes are fast."""
        start = time.time()
        
        for i in range(1000):
            cache.set('kalshi', 'market', {'ticker': f'TEST{i}'}, identifier=f'TEST{i}')
        
        duration = time.time() - start
        
        # Should complete in under 2 seconds
        assert duration < 2.0, f"Bulk write took {duration:.2f}s"
    
    def test_bulk_read_performance(self, cache):
        """Test that bulk reads from memory cache are instant."""
        # Populate cache
        for i in range(100):
            cache.set('kalshi', 'market', {'ticker': f'TEST{i}'}, identifier=f'TEST{i}')
        
        # Read all back
        start = time.time()
        
        for i in range(100):
            cache.get('kalshi', 'market', f'TEST{i}')
        
        duration = time.time() - start
        
        # Should complete in under 50ms (memory cache)
        assert duration < 0.05, f"Bulk read took {duration:.2f}s"

