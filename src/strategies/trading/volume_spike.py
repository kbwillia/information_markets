"""
Strategy 2: Volume Spike Detection

This strategy detects unusual volume spikes that often precede price movements.
High volume can indicate:
- New information entering the market
- Large player activity
- Institutional buying/selling
- Market manipulation (which we can ride)

Key insight: Volume spikes often happen BEFORE price moves catch up.
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

from src.strategies.trading.base import (
    BaseStrategy, Signal, SignalType, SignalStrength
)
from src.core.data_manager import DataManager, MarketData


class VolumeSpikeStrategy(BaseStrategy):
    """
    Detect volume spikes and trade in the direction of the spike.
    
    How it works:
    1. Track volume over time for each market
    2. Calculate rolling average and standard deviation
    3. When volume exceeds threshold (e.g., 2x average), it's a spike
    4. Determine direction from price movement during spike
    5. Trade in that direction, expecting continuation
    
    Parameters:
    - spike_threshold: Multiple of average volume to consider a spike (default: 2.0)
    - lookback_minutes: Minutes of history to consider (default: 60)
    - min_volume: Minimum absolute volume to consider (default: 1000)
    """
    
    def __init__(self, data_manager: DataManager,
                 paper_trading: bool = True,
                 max_position_size: float = None,
                 spike_threshold: float = 2.0,
                 lookback_minutes: int = 60,
                 min_volume: float = 1000):
        super().__init__(data_manager, paper_trading, max_position_size)
        
        self.spike_threshold = spike_threshold
        self.lookback_minutes = lookback_minutes
        self.min_volume = min_volume
        
        # Volume tracking
        self.volume_history: Dict[str, List[Dict]] = defaultdict(list)
        self.last_volumes: Dict[str, float] = {}
    
    @property
    def name(self) -> str:
        return "volume_spike"
    
    @property
    def description(self) -> str:
        return "Trade when unusual volume spikes are detected"
    
    def analyze(self) -> List[Signal]:
        """Analyze markets for volume spikes."""
        signals = []
        
        for platform in ['kalshi', 'polymarket']:
            markets = self.data_manager.get_all_markets(platform)
            
            for market in markets:
                signal = self._analyze_market_volume(market, platform)
                if signal:
                    signals.append(signal)
        
        return signals
    
    def _analyze_market_volume(self, market: MarketData, 
                                platform: str) -> Optional[Signal]:
        """Analyze volume for a single market."""
        market_key = f"{platform}:{market.id}"
        
        current_volume = market.volume
        if not current_volume or current_volume < self.min_volume:
            return None
        
        # Get volume history
        history = self.volume_history.get(market_key, [])
        
        # Record current volume
        now = datetime.now()
        self.volume_history[market_key].append({
            'volume': current_volume,
            'timestamp': now,
            'price': market.yes_price
        })
        
        # Keep only recent history
        cutoff = now - timedelta(minutes=self.lookback_minutes)
        self.volume_history[market_key] = [
            h for h in self.volume_history[market_key]
            if h['timestamp'] > cutoff
        ]
        
        history = self.volume_history[market_key]
        
        if len(history) < 5:
            # Not enough history
            return None
        
        # Calculate average and detect spike
        volumes = [h['volume'] for h in history[:-1]]  # Exclude current
        avg_volume = statistics.mean(volumes)
        
        if avg_volume == 0:
            return None
        
        volume_ratio = current_volume / avg_volume
        
        if volume_ratio < self.spike_threshold:
            # No spike
            return None
        
        # Spike detected! Determine direction from price movement
        prices = [h['price'] for h in history if h['price']]
        
        if len(prices) < 2:
            return None
        
        # Price trend during spike
        recent_prices = prices[-min(5, len(prices)):]
        price_trend = recent_prices[-1] - recent_prices[0]
        
        current_price = market.yes_price
        if not current_price:
            return None
        
        # Determine signal
        if price_trend > 0:
            signal_type = SignalType.BUY
            side = "yes"
            target_price = current_price * 1.02  # Expect 2% more upside
        elif price_trend < 0:
            signal_type = SignalType.SELL
            side = "no"
            target_price = current_price * 0.98  # Expect 2% more downside
        else:
            # No clear direction
            return None
        
        # Calculate confidence based on spike magnitude and volume
        confidence = min(0.9, 0.5 + (volume_ratio - self.spike_threshold) * 0.1)
        
        # Determine strength
        if volume_ratio > 4.0:
            strength = SignalStrength.STRONG
        elif volume_ratio > 2.5:
            strength = SignalStrength.MODERATE
        else:
            strength = SignalStrength.WEAK
        
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
            reasoning=f"Volume spike: {volume_ratio:.1f}x average ({current_volume:,.0f} vs avg {avg_volume:,.0f}). "
                     f"Price trending {'up' if price_trend > 0 else 'down'}.",
            metadata={
                'volume_ratio': volume_ratio,
                'current_volume': current_volume,
                'average_volume': avg_volume,
                'price_trend': price_trend,
                'spike_threshold': self.spike_threshold
            }
        )
    
    def get_volume_stats(self) -> Dict:
        """Get volume statistics across tracked markets."""
        stats = {
            'markets_tracked': len(self.volume_history),
            'spikes_detected_today': 0,
            'top_volume_markets': []
        }
        
        volumes_by_market = []
        for market_key, history in self.volume_history.items():
            if history:
                latest = history[-1]
                volumes_by_market.append({
                    'market': market_key,
                    'volume': latest['volume'],
                    'history_length': len(history)
                })
        
        # Sort by volume
        volumes_by_market.sort(key=lambda x: x['volume'], reverse=True)
        stats['top_volume_markets'] = volumes_by_market[:10]
        
        return stats

