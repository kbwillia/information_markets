"""Tests for trading strategies."""
import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

from src.strategies.trading.base import (
    BaseStrategy, Signal, SignalType, SignalStrength, Trade, TradeResult
)
from src.strategies.trading.lead_lag import LeadLagStrategy
from src.strategies.trading.volume_spike import VolumeSpikeStrategy
from src.strategies.trading.price_alerts import PriceAlertStrategy, AlertType
from src.strategies.trading.price_convergence import PriceConvergenceStrategy
from src.strategies.trading.momentum import MomentumStrategy
from src.strategies.trading.arbitrage import ArbitrageStrategy, ArbitrageType
from src.core.data_manager import DataManager, MarketData, MatchedMarket


@pytest.fixture
def mock_data_manager():
    """Create a mock DataManager."""
    dm = Mock(spec=DataManager)
    dm.get_all_markets.return_value = []
    dm.get_price.return_value = None
    dm.get_matched_markets.return_value = []
    dm.get_price_history.return_value = []
    dm.on_price_update = Mock()
    return dm


class TestSignal:
    """Test Signal class."""
    
    def test_signal_creation(self):
        """Test creating a signal."""
        signal = Signal(
            strategy_name="test",
            signal_type=SignalType.BUY,
            strength=SignalStrength.STRONG,
            platform="kalshi",
            market_id="TEST",
            market_title="Test Market",
            side="yes",
            target_price=0.60,
            current_price=0.50,
            confidence=0.85,
            reasoning="Test reason"
        )
        
        assert signal.strategy_name == "test"
        assert signal.signal_type == SignalType.BUY
        assert signal.confidence == 0.85
    
    def test_signal_to_dict(self):
        """Test signal serialization."""
        signal = Signal(
            strategy_name="test",
            signal_type=SignalType.SELL,
            strength=SignalStrength.WEAK,
            platform="polymarket",
            market_id="123",
            market_title="Test",
            side="no",
            target_price=0.40,
            current_price=0.50,
            confidence=0.55,
            reasoning="Test"
        )
        
        d = signal.to_dict()
        
        assert d['strategy_name'] == 'test'
        assert d['signal_type'] == 'sell'
        assert d['strength'] == 'weak'
        assert d['platform'] == 'polymarket'


class TestLeadLagStrategy:
    """Test LeadLagStrategy."""
    
    def test_initialization(self, mock_data_manager):
        """Test strategy initialization."""
        strategy = LeadLagStrategy(mock_data_manager)
        
        assert strategy.name == "lead_lag"
        assert strategy.min_move_threshold == 0.02
        assert strategy.paper_trading is True
    
    def test_analyze_no_matched_markets(self, mock_data_manager):
        """Test analysis with no matched markets."""
        strategy = LeadLagStrategy(mock_data_manager)
        
        signals = strategy.analyze()
        
        assert signals == []
    
    def test_price_change_callback(self, mock_data_manager):
        """Test that price changes are tracked."""
        strategy = LeadLagStrategy(mock_data_manager)
        
        # Simulate a price change callback
        strategy._on_price_change('kalshi', 'TEST', 0.50, 0.55)
        
        key = 'kalshi:TEST'
        assert key in strategy.recent_moves
        assert strategy.recent_moves[key]['direction'] == 'up'
        assert abs(strategy.recent_moves[key]['magnitude'] - 0.10) < 0.001  # 10% move (with float tolerance)


class TestVolumeSpikeStrategy:
    """Test VolumeSpikeStrategy."""
    
    def test_initialization(self, mock_data_manager):
        """Test strategy initialization."""
        strategy = VolumeSpikeStrategy(mock_data_manager)
        
        assert strategy.name == "volume_spike"
        assert strategy.spike_threshold == 2.0
    
    def test_analyze_low_volume(self, mock_data_manager):
        """Test that low volume markets are ignored."""
        market = MarketData(
            id='TEST',
            platform='kalshi',
            title='Test Market',
            description='',
            yes_price=0.50,
            no_price=0.50,
            yes_bid=0.49,
            yes_ask=0.51,
            volume=100,  # Below min_volume
            liquidity=None,
            end_date=None,
            status='active',
            category=None,
            raw_data={}
        )
        mock_data_manager.get_all_markets.return_value = [market]
        
        strategy = VolumeSpikeStrategy(mock_data_manager, min_volume=1000)
        signals = strategy.analyze()
        
        assert signals == []


class TestPriceAlertStrategy:
    """Test PriceAlertStrategy."""
    
    def test_add_alert(self, mock_data_manager):
        """Test adding price alerts."""
        strategy = PriceAlertStrategy(mock_data_manager, auto_detect_levels=False)
        
        alert = strategy.add_alert(
            platform='kalshi',
            market_id='TEST',
            market_title='Test Market',
            alert_type=AlertType.BELOW,
            price_level=0.30,
            side_to_trade='yes',
            action='buy'
        )
        
        assert len(strategy.alerts) == 1
        assert alert.price_level == 0.30
        assert alert.active is True
        assert alert.triggered is False
    
    def test_alert_triggered(self, mock_data_manager):
        """Test that alerts trigger correctly."""
        mock_data_manager.get_price.return_value = 0.25  # Below threshold
        
        strategy = PriceAlertStrategy(mock_data_manager, auto_detect_levels=False)
        strategy.add_alert(
            platform='kalshi',
            market_id='TEST',
            market_title='Test Market',
            alert_type=AlertType.BELOW,
            price_level=0.30,
            side_to_trade='yes',
            action='buy'
        )
        
        signals = strategy.analyze()
        
        assert len(signals) == 1
        assert signals[0].signal_type == SignalType.BUY
        assert strategy.alerts[0].triggered is True
    
    def test_alert_not_triggered(self, mock_data_manager):
        """Test that alerts don't trigger prematurely."""
        mock_data_manager.get_price.return_value = 0.35  # Above threshold
        
        strategy = PriceAlertStrategy(mock_data_manager, auto_detect_levels=False)
        strategy.add_alert(
            platform='kalshi',
            market_id='TEST',
            market_title='Test Market',
            alert_type=AlertType.BELOW,
            price_level=0.30,
            side_to_trade='yes',
            action='buy'
        )
        
        signals = strategy.analyze()
        
        assert len(signals) == 0
        assert strategy.alerts[0].triggered is False


class TestPriceConvergenceStrategy:
    """Test PriceConvergenceStrategy."""
    
    def test_initialization(self, mock_data_manager):
        """Test strategy initialization."""
        strategy = PriceConvergenceStrategy(mock_data_manager)
        
        assert strategy.name == "price_convergence"
        assert strategy.min_divergence == 0.05
    
    def test_find_divergence(self, mock_data_manager):
        """Test finding price divergences."""
        kalshi_market = MarketData(
            id='K-TEST', platform='kalshi', title='Test Market',
            description='', yes_price=0.40, no_price=0.60,
            yes_bid=0.39, yes_ask=0.41, volume=10000,
            liquidity=None, end_date=None, status='active',
            category=None, raw_data={}
        )
        poly_market = MarketData(
            id='P-TEST', platform='polymarket', title='Test Market',
            description='', yes_price=0.50, no_price=0.50,
            yes_bid=None, yes_ask=None, volume=10000,
            liquidity=None, end_date=None, status='active',
            category=None, raw_data={}
        )
        
        match = MatchedMarket(
            kalshi=kalshi_market,
            polymarket=poly_market,
            similarity_score=0.95,
            normalized_title='test market',
            text_similarity=0.95,
            semantic_similarity=0.90,
            end_date_match=False
        )
        
        mock_data_manager.get_matched_markets.return_value = [match]
        
        strategy = PriceConvergenceStrategy(mock_data_manager)
        signals = strategy.analyze()
        
        # Should generate a signal because 0.40 vs 0.50 = 22% divergence
        assert len(signals) == 1
        assert signals[0].platform == 'kalshi'  # Lower price


class TestMomentumStrategy:
    """Test MomentumStrategy."""
    
    def test_initialization(self, mock_data_manager):
        """Test strategy initialization."""
        strategy = MomentumStrategy(mock_data_manager)
        
        assert strategy.name == "momentum"
        assert strategy.min_momentum == 0.03
    
    def test_momentum_detection(self, mock_data_manager):
        """Test detecting momentum."""
        market = MarketData(
            id='TEST', platform='kalshi', title='Test Market',
            description='', yes_price=0.55, no_price=0.45,
            yes_bid=0.54, yes_ask=0.56, volume=10000,
            liquidity=None, end_date=None, status='active',
            category=None, raw_data={}
        )
        
        # Return price history showing upward momentum - only return for kalshi
        def get_markets(platform):
            if platform == 'kalshi':
                return [market]
            return []
        mock_data_manager.get_all_markets.side_effect = get_markets
        
        mock_data_manager.get_price_history.return_value = [
            {'price': 0.50, 'timestamp': 1000},
            {'price': 0.52, 'timestamp': 1001},
            {'price': 0.54, 'timestamp': 1002},
            {'price': 0.55, 'timestamp': 1003},
        ]
        
        strategy = MomentumStrategy(mock_data_manager, min_momentum=0.05)
        signals = strategy.analyze()
        
        # 10% momentum should trigger (at least one signal)
        assert len(signals) >= 1
        assert signals[0].signal_type == SignalType.BUY


class TestArbitrageStrategy:
    """Test ArbitrageStrategy."""
    
    def test_initialization(self, mock_data_manager):
        """Test strategy initialization."""
        strategy = ArbitrageStrategy(mock_data_manager)
        
        assert strategy.name == "arbitrage"
        assert strategy.min_net_profit == 0.01
        assert strategy.kalshi_fees.profit_fee_rate == 0.10
    
    def test_dutch_book_detection(self, mock_data_manager):
        """Test Dutch book arbitrage detection."""
        # Create matched market with STRONG arbitrage opportunity
        # Need total cost < 1.0 - fees to be profitable
        # Kalshi YES = 0.30, Polymarket NO = 0.50
        # Total cost = 0.80, gross profit = 0.20 (20%)
        # Kalshi fee = 10% of 0.70 profit = 0.07
        # Net profit = 0.20 - 0.07 - 0.02 (gas) = 0.11 (11%)
        kalshi_market = MarketData(
            id='K-TEST', platform='kalshi', title='Test Market',
            description='', yes_price=0.30, no_price=0.70,
            yes_bid=0.29, yes_ask=0.31, volume=10000,
            liquidity=None, end_date=None, status='active',
            category=None, raw_data={}
        )
        poly_market = MarketData(
            id='P-TEST', platform='polymarket', title='Test Market',
            description='', yes_price=0.50, no_price=0.50,
            yes_bid=None, yes_ask=None, volume=10000,
            liquidity=None, end_date=None, status='active',
            category=None, raw_data={}
        )
        
        match = MatchedMarket(
            kalshi=kalshi_market,
            polymarket=poly_market,
            similarity_score=0.95,
            normalized_title='test market',
            text_similarity=0.95,
            semantic_similarity=0.90,
            end_date_match=False
        )
        
        mock_data_manager.get_matched_markets.return_value = [match]
        
        strategy = ArbitrageStrategy(mock_data_manager, min_net_profit=0.01)
        signals = strategy.analyze()
        
        # Should detect arbitrage opportunity
        assert len(signals) >= 1
        
        # Check that it's an arbitrage opportunity
        arb_signal = signals[0]
        assert arb_signal.metadata.get('arb_type') in ['dutch_book', 'price_gap']
    
    def test_no_arbitrage_when_prices_fair(self, mock_data_manager):
        """Test that no arbitrage is detected when prices are fair."""
        kalshi_market = MarketData(
            id='K-TEST', platform='kalshi', title='Test Market',
            description='', yes_price=0.50, no_price=0.50,
            yes_bid=0.49, yes_ask=0.51, volume=10000,
            liquidity=None, end_date=None, status='active',
            category=None, raw_data={}
        )
        poly_market = MarketData(
            id='P-TEST', platform='polymarket', title='Test Market',
            description='', yes_price=0.50, no_price=0.50,
            yes_bid=None, yes_ask=None, volume=10000,
            liquidity=None, end_date=None, status='active',
            category=None, raw_data={}
        )
        
        match = MatchedMarket(
            kalshi=kalshi_market,
            polymarket=poly_market,
            similarity_score=0.95,
            normalized_title='test market',
            text_similarity=0.95,
            semantic_similarity=0.90,
            end_date_match=False
        )
        
        mock_data_manager.get_matched_markets.return_value = [match]
        
        strategy = ArbitrageStrategy(mock_data_manager, min_net_profit=0.03)
        signals = strategy.analyze()
        
        # Should NOT detect arbitrage (prices are fair)
        assert len(signals) == 0
    
    def test_fee_calculation(self, mock_data_manager):
        """Test that fees are properly calculated."""
        strategy = ArbitrageStrategy(
            mock_data_manager,
            kalshi_fee_rate=0.10,
            polymarket_gas_cost=0.02
        )
        
        # Check fee structures
        assert strategy.kalshi_fees.profit_fee_rate == 0.10
        assert strategy.polymarket_fees.fixed_fee_per_trade == 0.02
        
        # Check required spread calculation
        spread_info = strategy.calculate_required_spread()
        
        assert 'min_spread_break_even' in spread_info
        assert 'min_spread_profitable' in spread_info
        assert spread_info['kalshi_fee_estimate'] == 0.05  # 10% of 0.50
        assert spread_info['polymarket_gas_cost'] == 0.02


class TestTradeExecution:
    """Test trade execution."""
    
    def test_paper_trade(self, mock_data_manager):
        """Test paper trading."""
        strategy = MomentumStrategy(mock_data_manager, paper_trading=True)
        
        signal = Signal(
            strategy_name="test",
            signal_type=SignalType.BUY,
            strength=SignalStrength.MODERATE,
            platform="kalshi",
            market_id="TEST",
            market_title="Test",
            side="yes",
            target_price=0.60,
            current_price=0.55,
            confidence=0.75,
            reasoning="Test"
        )
        
        trade = strategy.generate_trade(signal)
        result = strategy.execute_trade(trade)
        
        assert result.success is True
        assert result.order_id.startswith("PAPER-")
        assert result.filled_quantity > 0

