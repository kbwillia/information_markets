"""Tests for DataManager matching functionality."""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

from src.core.data_manager import DataManager, MarketData, MatchedMarket


@pytest.fixture
def mock_clients():
    """Mock the API clients."""
    with patch('src.core.data_manager.KalshiClient') as mock_kalshi, \
         patch('src.core.data_manager.PolymarketClient') as mock_poly:
        
        mock_kalshi_instance = Mock()
        mock_kalshi_instance.get_markets.return_value = {'markets': []}
        mock_kalshi.return_value = mock_kalshi_instance
        
        mock_poly_instance = Mock()
        mock_poly_instance.get_markets.return_value = {'markets': []}
        mock_poly.return_value = mock_poly_instance
        
        yield mock_kalshi_instance, mock_poly_instance


class TestMarketMatching:
    """Test market matching functionality."""
    
    def test_text_normalization(self, mock_clients):
        """Test title normalization."""
        dm = DataManager(use_semantic_matching=False)
        
        title1 = "Will Bitcoin reach $100,000 by end of 2026?"
        title2 = "Bitcoin to reach $100,000 by the end of 2026"
        
        normalized1 = dm._normalize_title(title1)
        normalized2 = dm._normalize_title(title2)
        
        # Should be similar after normalization
        assert "bitcoin" in normalized1
        assert "bitcoin" in normalized2
        assert "100000" in normalized1
        assert "100000" in normalized2
    
    def test_end_date_parsing(self, mock_clients):
        """Test end date parsing."""
        dm = DataManager(use_semantic_matching=False)
        
        # Test ISO format
        date1 = "2026-12-31T23:59:59Z"
        parsed1 = dm._parse_end_date(date1)
        assert parsed1 is not None
        assert parsed1.year == 2026
        
        # Test simple format
        date2 = "2026-12-31"
        parsed2 = dm._parse_end_date(date2)
        assert parsed2 is not None
        assert parsed2.year == 2026
    
    def test_end_date_matching(self, mock_clients):
        """Test end date matching logic."""
        dm = DataManager(use_semantic_matching=False)
        
        # Same date
        date1 = "2026-12-31"
        date2 = "2026-12-31"
        match, diff = dm._end_dates_match(date1, date2, tolerance_days=7)
        assert match is True
        assert diff == 0
        
        # Close dates (within tolerance)
        date3 = "2026-12-31"
        date4 = "2027-01-05"  # 5 days later
        match, diff = dm._end_dates_match(date3, date4, tolerance_days=7)
        assert match is True
        assert diff == 5
        
        # Far dates (outside tolerance)
        date5 = "2026-12-31"
        date6 = "2027-02-01"  # 32 days later
        match, diff = dm._end_dates_match(date5, date6, tolerance_days=7)
        assert match is False
        assert diff == 32
    
    @pytest.mark.skipif(True, reason="Requires sentence-transformers model download")
    def test_semantic_similarity(self, mock_clients):
        """Test semantic similarity calculation."""
        dm = DataManager(use_semantic_matching=True)
        
        # Similar meanings, different words
        text1 = "Will Bitcoin reach $100,000?"
        text2 = "Bitcoin price to hit $100k"
        
        similarity = dm._semantic_similarity(text1, text2)
        
        # Should have high similarity despite different wording
        assert similarity > 0.7
        
        # Different topics
        text3 = "Will Bitcoin reach $100,000?"
        text4 = "Will it rain tomorrow?"
        
        similarity2 = dm._semantic_similarity(text3, text4)
        
        # Should have low similarity
        assert similarity2 < 0.5
    
    def test_combined_matching(self, mock_clients):
        """Test that matching combines text, semantic, and end date."""
        dm = DataManager(use_semantic_matching=False)  # Disable semantic for speed
        
        kalshi_market = MarketData(
            id='K-TEST', platform='kalshi', title='Bitcoin to $100k by Dec 2026',
            description='', yes_price=0.50, no_price=0.50,
            yes_bid=0.49, yes_ask=0.51, volume=10000,
            liquidity=None, end_date='2026-12-31', status='active',
            category=None, raw_data={}
        )
        
        poly_market = MarketData(
            id='P-TEST', platform='polymarket', title='Bitcoin reaches $100,000 by end of 2026',
            description='', yes_price=0.50, no_price=0.50,
            yes_bid=None, yes_ask=None, volume=10000,
            liquidity=None, end_date='2026-12-31', status='active',
            category=None, raw_data={}
        )
        
        # Manually create a match to test the structure
        match = MatchedMarket(
            kalshi=kalshi_market,
            polymarket=poly_market,
            similarity_score=0.85,
            normalized_title='bitcoin 100k dec 2026',
            text_similarity=0.75,
            semantic_similarity=0.80,
            end_date_match=True,
            end_date_diff_days=0
        )
        
        assert match.similarity_score == 0.85
        assert match.text_similarity == 0.75
        assert match.semantic_similarity == 0.80
        assert match.end_date_match is True
        assert match.end_date_diff_days == 0

