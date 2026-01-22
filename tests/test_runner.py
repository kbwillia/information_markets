"""Tests for the strategy runner."""
import pytest
from unittest.mock import Mock, patch
import tempfile
import os

from src.strategies.trading.runner import StrategyRunner, create_default_runner


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


class TestStrategyRunner:
    """Test StrategyRunner class."""
    
    def test_initialization(self, mock_clients):
        """Test runner initialization."""
        runner = StrategyRunner(paper_trading=True)
        
        assert runner.paper_trading is True
        assert len(runner.strategies) == 0
    
    def test_add_strategy(self, mock_clients):
        """Test adding strategies."""
        runner = StrategyRunner()
        
        runner.add_strategy('momentum', enabled=True)
        runner.add_strategy('lead_lag', enabled=True)
        
        assert 'momentum' in runner.strategies
        assert 'lead_lag' in runner.strategies
        assert len(runner.strategies) == 2
    
    def test_disable_strategy(self, mock_clients):
        """Test disabling strategies."""
        runner = StrategyRunner()
        
        runner.add_strategy('momentum', enabled=True)
        assert 'momentum' in runner.strategies
        
        runner.disable_strategy('momentum')
        assert 'momentum' not in runner.strategies
    
    def test_run_cycle(self, mock_clients):
        """Test running a single cycle."""
        runner = StrategyRunner(paper_trading=True)
        runner.add_strategy('momentum', enabled=True)
        
        stats = runner.run_cycle()
        
        assert stats.strategies_run == 1
        assert stats.cycle_duration_ms >= 0
    
    def test_daily_trade_limit(self, mock_clients):
        """Test that daily trade limit is respected."""
        runner = StrategyRunner(paper_trading=True, max_daily_trades=0)
        runner.add_strategy('momentum', enabled=True)
        
        stats = runner.run_cycle()
        
        assert stats.trades_executed == 0
    
    def test_performance_summary(self, mock_clients):
        """Test getting performance summary."""
        runner = StrategyRunner(paper_trading=True)
        runner.add_strategy('momentum', enabled=True)
        
        # Run a cycle
        runner.run_cycle()
        
        summary = runner.get_performance_summary()
        
        assert 'paper_trading' in summary
        assert 'total_trades' in summary
        assert 'strategies_enabled' in summary


class TestCreateDefaultRunner:
    """Test the create_default_runner function."""
    
    def test_creates_all_strategies(self, mock_clients):
        """Test that all strategies are created."""
        runner = create_default_runner(paper_trading=True)
        
        expected_strategies = [
            'lead_lag',
            'volume_spike',
            'price_alerts',
            'price_convergence',
            'momentum',
            'arbitrage'
        ]
        
        for strategy in expected_strategies:
            assert strategy in runner.strategies, f"Missing strategy: {strategy}"
    
    def test_paper_trading_mode(self, mock_clients):
        """Test paper trading mode setting."""
        runner = create_default_runner(paper_trading=True)
        assert runner.paper_trading is True
        
        runner = create_default_runner(paper_trading=False)
        assert runner.paper_trading is False

