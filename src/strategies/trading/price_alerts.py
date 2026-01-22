"""
Strategy 3: Price Alerts System

This strategy monitors prices and generates signals when they cross
important levels. Useful for:
- Entry points (buy when price drops to support)
- Exit points (sell when price hits resistance)
- Breakout detection (trade when price breaks key levels)

Key insight: Price levels matter - support/resistance often holds.
"""
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from src.strategies.trading.base import (
    BaseStrategy, Signal, SignalType, SignalStrength
)
from src.core.data_manager import DataManager


class AlertType(Enum):
    """Type of price alert."""
    ABOVE = "above"      # Price goes above threshold
    BELOW = "below"      # Price goes below threshold
    CROSS_UP = "cross_up"    # Price crosses threshold from below
    CROSS_DOWN = "cross_down"  # Price crosses threshold from above


@dataclass
class PriceAlert:
    """A price alert configuration."""
    platform: str
    market_id: str
    market_title: str
    alert_type: AlertType
    price_level: float
    side_to_trade: str  # 'yes' or 'no'
    action: str  # 'buy' or 'sell'
    confidence: float = 0.7
    note: str = ""
    active: bool = True
    triggered: bool = False
    created_at: datetime = field(default_factory=datetime.now)


class PriceAlertStrategy(BaseStrategy):
    """
    Generate signals when prices cross configured alert levels.
    
    How it works:
    1. User/system adds price alerts with target levels
    2. Strategy monitors current prices against alerts
    3. When price crosses alert level, generate signal
    4. Support various alert types (above, below, cross)
    
    Usage:
        strategy = PriceAlertStrategy(data_manager)
        
        # Add alerts
        strategy.add_alert(
            platform='kalshi',
            market_id='TICKER',
            market_title='Will X happen?',
            alert_type=AlertType.BELOW,
            price_level=0.30,
            side_to_trade='yes',
            action='buy',
            note='Good entry point'
        )
        
        # Run analysis
        signals = strategy.analyze()
    """
    
    def __init__(self, data_manager: DataManager,
                 paper_trading: bool = True,
                 max_position_size: float = None,
                 auto_detect_levels: bool = True):
        super().__init__(data_manager, paper_trading, max_position_size)
        
        self.auto_detect_levels = auto_detect_levels
        self.alerts: List[PriceAlert] = []
        self.last_prices: Dict[str, float] = {}  # For cross detection
        
        # Callbacks for alert triggers
        self.alert_callbacks: List[Callable[[PriceAlert, Signal], None]] = []
    
    @property
    def name(self) -> str:
        return "price_alerts"
    
    @property
    def description(self) -> str:
        return "Trade when prices cross configured alert levels"
    
    def add_alert(self, platform: str, market_id: str, market_title: str,
                  alert_type: AlertType, price_level: float,
                  side_to_trade: str, action: str,
                  confidence: float = 0.7, note: str = "") -> PriceAlert:
        """Add a new price alert."""
        alert = PriceAlert(
            platform=platform,
            market_id=market_id,
            market_title=market_title,
            alert_type=alert_type,
            price_level=price_level,
            side_to_trade=side_to_trade,
            action=action,
            confidence=confidence,
            note=note
        )
        self.alerts.append(alert)
        return alert
    
    def remove_alert(self, platform: str, market_id: str, 
                    price_level: float = None):
        """Remove an alert."""
        self.alerts = [
            a for a in self.alerts
            if not (a.platform == platform and a.market_id == market_id
                   and (price_level is None or a.price_level == price_level))
        ]
    
    def on_alert_triggered(self, callback: Callable[[PriceAlert, Signal], None]):
        """Register callback for when an alert triggers."""
        self.alert_callbacks.append(callback)
    
    def analyze(self) -> List[Signal]:
        """Analyze prices against configured alerts."""
        signals = []
        
        # Check configured alerts
        for alert in self.alerts:
            if not alert.active or alert.triggered:
                continue
            
            signal = self._check_alert(alert)
            if signal:
                signals.append(signal)
                alert.triggered = True
                
                # Notify callbacks
                for callback in self.alert_callbacks:
                    try:
                        callback(alert, signal)
                    except Exception as e:
                        print(f"Alert callback error: {e}")
        
        # Auto-detect levels if enabled
        if self.auto_detect_levels:
            auto_signals = self._auto_detect_signals()
            signals.extend(auto_signals)
        
        return signals
    
    def _check_alert(self, alert: PriceAlert) -> Optional[Signal]:
        """Check if an alert should trigger."""
        current_price = self.data_manager.get_price(alert.platform, alert.market_id)
        
        if current_price is None:
            return None
        
        market_key = f"{alert.platform}:{alert.market_id}"
        last_price = self.last_prices.get(market_key)
        self.last_prices[market_key] = current_price
        
        triggered = False
        
        if alert.alert_type == AlertType.ABOVE:
            triggered = current_price > alert.price_level
        elif alert.alert_type == AlertType.BELOW:
            triggered = current_price < alert.price_level
        elif alert.alert_type == AlertType.CROSS_UP:
            if last_price is not None:
                triggered = last_price <= alert.price_level < current_price
        elif alert.alert_type == AlertType.CROSS_DOWN:
            if last_price is not None:
                triggered = last_price >= alert.price_level > current_price
        
        if not triggered:
            return None
        
        signal_type = SignalType.BUY if alert.action == 'buy' else SignalType.SELL
        
        # Strength based on how far price moved past level
        price_diff = abs(current_price - alert.price_level)
        if price_diff > 0.05:
            strength = SignalStrength.STRONG
        elif price_diff > 0.02:
            strength = SignalStrength.MODERATE
        else:
            strength = SignalStrength.WEAK
        
        return Signal(
            strategy_name=self.name,
            signal_type=signal_type,
            strength=strength,
            platform=alert.platform,
            market_id=alert.market_id,
            market_title=alert.market_title,
            side=alert.side_to_trade,
            target_price=current_price,
            current_price=current_price,
            confidence=alert.confidence,
            reasoning=f"Alert triggered: Price {alert.alert_type.value} {alert.price_level:.2f}. "
                     f"Current: {current_price:.2f}. {alert.note}",
            metadata={
                'alert_type': alert.alert_type.value,
                'price_level': alert.price_level,
                'note': alert.note
            }
        )
    
    def _auto_detect_signals(self) -> List[Signal]:
        """Automatically detect significant price levels and generate signals."""
        signals = []
        
        for platform in ['kalshi', 'polymarket']:
            markets = self.data_manager.get_all_markets(platform)
            
            for market in markets:
                if not market.yes_price:
                    continue
                
                price = market.yes_price
                
                # Look for prices near key psychological levels
                key_levels = [0.10, 0.20, 0.25, 0.30, 0.40, 0.50, 
                             0.60, 0.70, 0.75, 0.80, 0.90]
                
                for level in key_levels:
                    # Price just crossed above a key level
                    market_key = f"{platform}:{market.id}"
                    last_price = self.last_prices.get(market_key, price)
                    
                    if last_price < level <= price:
                        # Bullish breakout
                        signals.append(Signal(
                            strategy_name=self.name,
                            signal_type=SignalType.BUY,
                            strength=SignalStrength.MODERATE,
                            platform=platform,
                            market_id=market.id,
                            market_title=market.title,
                            side="yes",
                            target_price=price + 0.05,
                            current_price=price,
                            confidence=0.6,
                            reasoning=f"Price broke above key level {level:.0%}",
                            metadata={'level': level, 'direction': 'breakout_up'}
                        ))
                    
                    elif last_price > level >= price:
                        # Bearish breakdown
                        signals.append(Signal(
                            strategy_name=self.name,
                            signal_type=SignalType.SELL,
                            strength=SignalStrength.MODERATE,
                            platform=platform,
                            market_id=market.id,
                            market_title=market.title,
                            side="no",
                            target_price=price - 0.05,
                            current_price=price,
                            confidence=0.6,
                            reasoning=f"Price broke below key level {level:.0%}",
                            metadata={'level': level, 'direction': 'breakout_down'}
                        ))
                
                self.last_prices[market_key] = price
        
        return signals
    
    def get_active_alerts(self) -> List[PriceAlert]:
        """Get all active (non-triggered) alerts."""
        return [a for a in self.alerts if a.active and not a.triggered]
    
    def reset_alerts(self):
        """Reset all triggered alerts to active."""
        for alert in self.alerts:
            alert.triggered = False

