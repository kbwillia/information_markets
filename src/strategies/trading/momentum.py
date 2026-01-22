"""
Strategy 5: Momentum Trading

This strategy rides price momentum - buying when prices are trending up
and selling when trending down. Markets often continue in the same
direction for short periods due to information cascades and herding behavior.

Key insight: Trends persist - buy strength, sell weakness.
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

from src.strategies.trading.base import (
    BaseStrategy, Signal, SignalType, SignalStrength
)
from src.core.data_manager import DataManager, MarketData


class MomentumStrategy(BaseStrategy):
    """
    Trade price momentum - buy uptrends, sell downtrends.
    
    How it works:
    1. Calculate price change over lookback period
    2. If change exceeds threshold, it's a trend
    3. Enter position in direction of trend
    4. Exit when momentum slows or reverses
    
    Parameters:
    - lookback_minutes: Period to calculate momentum (default: 15)
    - min_momentum: Minimum price change to consider a trend (default: 3%)
    - exit_threshold: Exit when momentum drops below this (default: 1%)
    """
    
    def __init__(self, data_manager: DataManager,
                 paper_trading: bool = True,
                 max_position_size: float = None,
                 lookback_minutes: int = 15,
                 min_momentum: float = 0.03,
                 exit_threshold: float = 0.01):
        super().__init__(data_manager, paper_trading, max_position_size)
        
        self.lookback_minutes = lookback_minutes
        self.min_momentum = min_momentum
        self.exit_threshold = exit_threshold
        
        # Track positions
        self.open_positions: Dict[str, Dict] = {}
        
        # Track momentum history for each market
        self.momentum_history: Dict[str, List[float]] = defaultdict(list)
    
    @property
    def name(self) -> str:
        return "momentum"
    
    @property
    def description(self) -> str:
        return "Trade price momentum - buy uptrends, sell downtrends"
    
    def analyze(self) -> List[Signal]:
        """Analyze markets for momentum signals."""
        signals = []
        
        for platform in ['kalshi', 'polymarket']:
            markets = self.data_manager.get_all_markets(platform)
            
            for market in markets:
                # Check for new momentum opportunities
                signal = self._analyze_momentum(market, platform)
                if signal:
                    signals.append(signal)
                
                # Check for exit signals
                market_key = f"{platform}:{market.id}"
                if market_key in self.open_positions:
                    exit_signal = self._check_exit(market, platform, market_key)
                    if exit_signal:
                        signals.append(exit_signal)
        
        return signals
    
    def _analyze_momentum(self, market: MarketData, 
                           platform: str) -> Optional[Signal]:
        """Analyze momentum for a single market."""
        market_key = f"{platform}:{market.id}"
        
        # Don't enter if we already have a position
        if market_key in self.open_positions:
            return None
        
        # Get price history
        price_history = self.data_manager.get_price_history(
            platform, market.id, self.lookback_minutes
        )
        
        if len(price_history) < 3:
            return None
        
        # Calculate momentum
        prices = [p['price'] for p in price_history]
        start_price = prices[0]
        current_price = prices[-1]
        
        if start_price == 0:
            return None
        
        momentum = (current_price - start_price) / start_price
        
        # Track momentum history
        self.momentum_history[market_key].append(momentum)
        if len(self.momentum_history[market_key]) > 100:
            self.momentum_history[market_key] = self.momentum_history[market_key][-100:]
        
        # Check if momentum is strong enough
        if abs(momentum) < self.min_momentum:
            return None
        
        # Calculate momentum acceleration (is it speeding up?)
        if len(self.momentum_history[market_key]) >= 3:
            recent_momenta = self.momentum_history[market_key][-3:]
            acceleration = recent_momenta[-1] - recent_momenta[0]
        else:
            acceleration = 0
        
        # Determine signal
        if momentum > 0:
            signal_type = SignalType.BUY
            side = "yes"
            target_price = current_price * (1 + abs(momentum) * 0.5)  # Expect half more
        else:
            signal_type = SignalType.SELL
            side = "no"
            target_price = current_price * (1 - abs(momentum) * 0.5)
        
        # Calculate confidence based on momentum strength and consistency
        confidence = min(0.9, 0.5 + abs(momentum) * 2)
        
        # Boost confidence if momentum is accelerating
        if (momentum > 0 and acceleration > 0) or (momentum < 0 and acceleration < 0):
            confidence = min(0.95, confidence + 0.1)
        
        # Determine strength
        if abs(momentum) > 0.10:
            strength = SignalStrength.STRONG
        elif abs(momentum) > 0.05:
            strength = SignalStrength.MODERATE
        else:
            strength = SignalStrength.WEAK
        
        # Record position
        self.open_positions[market_key] = {
            'entry_price': current_price,
            'entry_momentum': momentum,
            'entry_time': datetime.now(),
            'side': side,
            'direction': 'up' if momentum > 0 else 'down'
        }
        
        return Signal(
            strategy_name=self.name,
            signal_type=signal_type,
            strength=strength,
            platform=platform,
            market_id=market.id,
            market_title=market.title,
            side=side,
            target_price=target_price,
            current_price=current_price,
            confidence=confidence,
            reasoning=f"Strong momentum: {momentum*100:+.1f}% over {self.lookback_minutes} min. "
                     f"{'Accelerating' if acceleration != 0 and (momentum > 0) == (acceleration > 0) else 'Steady'}.",
            metadata={
                'momentum': momentum,
                'acceleration': acceleration,
                'lookback_minutes': self.lookback_minutes,
                'price_history_length': len(prices)
            }
        )
    
    def _check_exit(self, market: MarketData, platform: str,
                    market_key: str) -> Optional[Signal]:
        """Check if we should exit a momentum position."""
        position = self.open_positions.get(market_key)
        if not position:
            return None
        
        current_price = market.yes_price
        if not current_price:
            return None
        
        entry_price = position['entry_price']
        direction = position['direction']
        
        # Calculate current momentum from entry
        if entry_price == 0:
            return None
        
        current_momentum = (current_price - entry_price) / entry_price
        
        # Check exit conditions
        should_exit = False
        exit_reason = ""
        
        # 1. Momentum reversed
        if direction == 'up' and current_momentum < -self.exit_threshold:
            should_exit = True
            exit_reason = "Momentum reversed (turned negative)"
        elif direction == 'down' and current_momentum > self.exit_threshold:
            should_exit = True
            exit_reason = "Momentum reversed (turned positive)"
        
        # 2. Momentum stalled
        time_in_position = datetime.now() - position['entry_time']
        if time_in_position > timedelta(minutes=self.lookback_minutes * 2):
            if abs(current_momentum) < self.exit_threshold:
                should_exit = True
                exit_reason = "Momentum stalled"
        
        # 3. Take profit (momentum reached target)
        if abs(current_momentum) > abs(position['entry_momentum']) * 1.5:
            should_exit = True
            exit_reason = "Take profit - target reached"
        
        if not should_exit:
            return None
        
        # Calculate P&L
        pnl = current_momentum if direction == 'up' else -current_momentum
        
        # Remove position
        del self.open_positions[market_key]
        
        return Signal(
            strategy_name=self.name,
            signal_type=SignalType.SELL if direction == 'up' else SignalType.BUY,
            strength=SignalStrength.STRONG,
            platform=platform,
            market_id=market.id,
            market_title=market.title,
            side=position['side'],
            target_price=current_price,
            current_price=current_price,
            confidence=0.9,
            reasoning=f"Exit momentum position: {exit_reason}. "
                     f"P&L: {pnl*100:+.1f}%",
            metadata={
                'entry_price': entry_price,
                'exit_price': current_price,
                'pnl': pnl,
                'entry_momentum': position['entry_momentum'],
                'exit_momentum': current_momentum,
                'hold_time_minutes': time_in_position.total_seconds() / 60
            }
        )
    
    def get_open_positions(self) -> List[Dict]:
        """Get all open momentum positions."""
        result = []
        for market_key, position in self.open_positions.items():
            platform, market_id = market_key.split(':', 1)
            current_price = self.data_manager.get_price(platform, market_id)
            
            if current_price and position['entry_price']:
                current_pnl = (current_price - position['entry_price']) / position['entry_price']
                if position['direction'] == 'down':
                    current_pnl = -current_pnl
            else:
                current_pnl = 0
            
            result.append({
                'market_key': market_key,
                'direction': position['direction'],
                'entry_price': position['entry_price'],
                'current_price': current_price,
                'pnl': current_pnl,
                'hold_time_minutes': (datetime.now() - position['entry_time']).total_seconds() / 60
            })
        
        return result
    
    def get_momentum_leaders(self, top_n: int = 10) -> List[Dict]:
        """Get markets with the strongest current momentum."""
        momentum_data = []
        
        for platform in ['kalshi', 'polymarket']:
            markets = self.data_manager.get_all_markets(platform)
            
            for market in markets:
                market_key = f"{platform}:{market.id}"
                if market_key in self.momentum_history and self.momentum_history[market_key]:
                    latest_momentum = self.momentum_history[market_key][-1]
                    momentum_data.append({
                        'platform': platform,
                        'market_id': market.id,
                        'title': market.title,
                        'momentum': latest_momentum,
                        'abs_momentum': abs(latest_momentum)
                    })
        
        # Sort by absolute momentum
        momentum_data.sort(key=lambda x: x['abs_momentum'], reverse=True)
        
        return momentum_data[:top_n]

