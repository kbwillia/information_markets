"""
Strategy 1: Event Lead/Lag Analysis

This strategy exploits the fact that one platform often moves before the other
when news breaks. By detecting which platform moves first, we can trade on
the lagging platform before it catches up.

Key insight: Information doesn't propagate instantly across platforms.
"""
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

from src.strategies.trading.base import (
    BaseStrategy, Signal, SignalType, SignalStrength
)
from src.core.data_manager import DataManager, MatchedMarket


class LeadLagStrategy(BaseStrategy):
    """
    Detect lead/lag relationships between platforms and trade on the lagging one.
    
    How it works:
    1. Monitor price changes on matched markets (same event on both platforms)
    2. Detect when one platform moves significantly
    3. If the other platform hasn't moved yet, trade in the same direction
    4. Capture the price movement as the lagging platform catches up
    
    Parameters:
    - min_move_threshold: Minimum price change to consider significant (default: 2%)
    - max_lag_seconds: Maximum time to consider a move "lagged" (default: 300s)
    - min_confidence: Minimum historical accuracy to trade (default: 0.6)
    """
    
    def __init__(self, data_manager: DataManager,
                 paper_trading: bool = True,
                 max_position_size: float = None,
                 min_move_threshold: float = 0.02,
                 max_lag_seconds: int = 300,
                 min_confidence: float = 0.6):
        super().__init__(data_manager, paper_trading, max_position_size)
        
        self.min_move_threshold = min_move_threshold
        self.max_lag_seconds = max_lag_seconds
        self.min_confidence = min_confidence
        
        # Track lead/lag patterns
        self.lead_history: Dict[str, List[Dict]] = defaultdict(list)
        
        # Register for price updates
        self.recent_moves: Dict[str, Dict] = {}  # market_id -> {platform, direction, timestamp, magnitude}
        data_manager.on_price_update(self._on_price_change)
    
    @property
    def name(self) -> str:
        return "lead_lag"
    
    @property
    def description(self) -> str:
        return "Trade on lagging platform when lead platform moves first"
    
    def _on_price_change(self, platform: str, market_id: str,
                        old_price: float, new_price: float):
        """Callback for price updates - track significant moves."""
        if old_price is None or old_price == 0:
            return
        
        change = (new_price - old_price) / old_price
        
        if abs(change) >= self.min_move_threshold:
            direction = "up" if change > 0 else "down"
            
            # Record this move
            self.recent_moves[f"{platform}:{market_id}"] = {
                'platform': platform,
                'market_id': market_id,
                'direction': direction,
                'magnitude': abs(change),
                'old_price': old_price,
                'new_price': new_price,
                'timestamp': datetime.now()
            }
    
    def analyze(self) -> List[Signal]:
        """Analyze for lead/lag opportunities."""
        signals = []
        
        # Get matched markets
        matched_markets = self.data_manager.get_matched_markets()
        
        for match in matched_markets:
            signal = self._analyze_matched_market(match)
            if signal:
                signals.append(signal)
        
        return signals
    
    def _analyze_matched_market(self, match: MatchedMarket) -> Optional[Signal]:
        """Analyze a single matched market for lead/lag opportunity."""
        kalshi_id = match.kalshi.id
        poly_id = match.polymarket.id
        
        kalshi_key = f"kalshi:{kalshi_id}"
        poly_key = f"polymarket:{poly_id}"
        
        # Check if one platform moved recently
        kalshi_move = self.recent_moves.get(kalshi_key)
        poly_move = self.recent_moves.get(poly_key)
        
        now = datetime.now()
        lead_platform = None
        lag_platform = None
        lead_move = None
        
        # Determine lead/lag
        if kalshi_move and not poly_move:
            if (now - kalshi_move['timestamp']).total_seconds() < self.max_lag_seconds:
                lead_platform = 'kalshi'
                lag_platform = 'polymarket'
                lead_move = kalshi_move
        elif poly_move and not kalshi_move:
            if (now - poly_move['timestamp']).total_seconds() < self.max_lag_seconds:
                lead_platform = 'polymarket'
                lag_platform = 'kalshi'
                lead_move = poly_move
        elif kalshi_move and poly_move:
            # Both moved - check timing
            kalshi_age = (now - kalshi_move['timestamp']).total_seconds()
            poly_age = (now - poly_move['timestamp']).total_seconds()
            
            if kalshi_age < poly_age - 10:  # Kalshi moved 10+ seconds earlier
                lead_platform = 'kalshi'
                lag_platform = 'polymarket'
                lead_move = kalshi_move
            elif poly_age < kalshi_age - 10:  # Polymarket moved 10+ seconds earlier
                lead_platform = 'polymarket'
                lag_platform = 'kalshi'
                lead_move = poly_move
        
        if not lead_platform or not lead_move:
            return None
        
        # Get current prices
        if lag_platform == 'kalshi':
            current_price = self.data_manager.get_price('kalshi', kalshi_id)
            market_id = kalshi_id
            market_title = match.kalshi.title
        else:
            current_price = self.data_manager.get_price('polymarket', poly_id)
            market_id = poly_id
            market_title = match.polymarket.title
        
        if not current_price:
            return None
        
        # Calculate expected move on lagging platform
        expected_change = lead_move['magnitude']
        if lead_move['direction'] == "up":
            target_price = current_price * (1 + expected_change)
            signal_type = SignalType.BUY
            side = "yes"
        else:
            target_price = current_price * (1 - expected_change)
            signal_type = SignalType.SELL
            side = "no"
        
        # Calculate confidence based on historical patterns
        confidence = self._calculate_confidence(match.normalized_title, lead_platform)
        
        if confidence < self.min_confidence:
            return None
        
        # Determine signal strength
        if confidence > 0.8 and expected_change > 0.05:
            strength = SignalStrength.STRONG
        elif confidence > 0.65:
            strength = SignalStrength.MODERATE
        else:
            strength = SignalStrength.WEAK
        
        # Record this for future confidence calculations
        self._record_lead_lag(match.normalized_title, lead_platform)
        
        return Signal(
            strategy_name=self.name,
            signal_type=signal_type,
            strength=strength,
            platform=lag_platform,
            market_id=market_id,
            market_title=market_title,
            side=side,
            target_price=target_price,
            current_price=current_price,
            confidence=confidence,
            reasoning=f"{lead_platform} moved {lead_move['direction']} by {lead_move['magnitude']*100:.1f}%. "
                     f"Expecting {lag_platform} to follow.",
            metadata={
                'lead_platform': lead_platform,
                'lead_direction': lead_move['direction'],
                'lead_magnitude': lead_move['magnitude'],
                'lead_timestamp': lead_move['timestamp'].isoformat(),
                'matched_market_score': match.similarity_score
            }
        )
    
    def _calculate_confidence(self, normalized_title: str, lead_platform: str) -> float:
        """Calculate confidence based on historical lead/lag patterns."""
        history = self.lead_history.get(normalized_title, [])
        
        if not history:
            return 0.6  # Default confidence for new markets
        
        # Count how often this platform leads
        same_leader = sum(1 for h in history if h['lead'] == lead_platform)
        total = len(history)
        
        if total < 5:
            # Not enough data, use default with slight adjustment
            return 0.6 + (same_leader / total) * 0.1
        
        # Historical accuracy
        accuracy = same_leader / total
        
        # More recent patterns weight more
        recent = history[-10:]
        recent_accuracy = sum(1 for h in recent if h['lead'] == lead_platform) / len(recent)
        
        # Weighted average (recent patterns matter more)
        return 0.6 * recent_accuracy + 0.4 * accuracy
    
    def _record_lead_lag(self, normalized_title: str, lead_platform: str):
        """Record a lead/lag event for future reference."""
        self.lead_history[normalized_title].append({
            'lead': lead_platform,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 100 events per market
        if len(self.lead_history[normalized_title]) > 100:
            self.lead_history[normalized_title] = self.lead_history[normalized_title][-100:]
    
    def get_lead_lag_stats(self) -> Dict:
        """Get statistics on lead/lag patterns."""
        stats = {
            'markets_tracked': len(self.lead_history),
            'kalshi_leads': 0,
            'polymarket_leads': 0,
            'by_market': {}
        }
        
        for market, history in self.lead_history.items():
            kalshi_leads = sum(1 for h in history if h['lead'] == 'kalshi')
            poly_leads = len(history) - kalshi_leads
            
            stats['kalshi_leads'] += kalshi_leads
            stats['polymarket_leads'] += poly_leads
            stats['by_market'][market] = {
                'kalshi_leads': kalshi_leads,
                'polymarket_leads': poly_leads,
                'total': len(history)
            }
        
        return stats

