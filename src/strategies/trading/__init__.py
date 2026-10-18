"""Trading strategies module."""
from src.strategies.trading.base import BaseStrategy, Signal, Trade, TradeResult
from src.strategies.trading.lead_lag import LeadLagStrategy
from src.strategies.trading.volume_spike import VolumeSpikeStrategy
from src.strategies.trading.price_alerts import PriceAlertStrategy
from src.strategies.trading.price_convergence import PriceConvergenceStrategy
from src.strategies.trading.momentum import MomentumStrategy
from src.strategies.trading.arbitrage import ArbitrageStrategy
from src.strategies.trading.complete_set import CompleteSetStrategy
from src.strategies.trading.copy_top_traders import CopyTopTradersStrategy
from src.strategies.trading.copy_watchlist import CopyWatchlistStrategy

__all__ = [
    'BaseStrategy',
    'Signal',
    'Trade',
    'TradeResult',
    'LeadLagStrategy',
    'VolumeSpikeStrategy',
    'PriceAlertStrategy',
    'PriceConvergenceStrategy',
    'MomentumStrategy',
    'ArbitrageStrategy',
    'CompleteSetStrategy',
    'CopyTopTradersStrategy',
    'CopyWatchlistStrategy',
]

