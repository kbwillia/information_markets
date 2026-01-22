"""
Strategy 4: Price Convergence Trading

This strategy exploits price differences between platforms for the same event.
Prices MUST converge at resolution, so significant divergences present
opportunities.

Key insight: As resolution approaches, prices converge - this is guaranteed.
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from src.strategies.trading.base import (
    BaseStrategy, Signal, SignalType, SignalStrength
)
from src.core.data_manager import DataManager, MatchedMarket


@dataclass
class DivergenceOpportunity:
    """A price divergence opportunity between platforms."""
    kalshi_market: str
    polymarket_market: str
    market_title: str
    kalshi_price: float
    polymarket_price: float
    divergence: float  # Absolute difference
    divergence_pct: float  # Percentage difference
    time_to_resolution: Optional[timedelta]
    recommended_platform: str  # Platform to buy on (lower price)
    expected_profit: float


class PriceConvergenceStrategy(BaseStrategy):
    """
    Trade price divergences between platforms, betting on convergence.
    
    How it works:
    1. Find matched markets (same event on both platforms)
    2. Calculate price divergence
    3. If divergence exceeds threshold, buy on lower-priced platform
    4. Hold until prices converge (or resolution)
    
    Parameters:
    - min_divergence: Minimum price difference to trade (default: 5%)
    - max_time_to_resolution: Don't trade if resolution too far (default: 30 days)
    - convergence_threshold: Close position when divergence drops to this (default: 1%)
    """
    
    def __init__(self, data_manager: DataManager,
                 paper_trading: bool = True,
                 max_position_size: float = None,
                 min_divergence: float = 0.05,
                 max_time_to_resolution_days: int = 30,
                 convergence_threshold: float = 0.01):
        super().__init__(data_manager, paper_trading, max_position_size)
        
        self.min_divergence = min_divergence
        self.max_time_to_resolution_days = max_time_to_resolution_days
        self.convergence_threshold = convergence_threshold
        
        # Track open convergence positions
        self.open_positions: Dict[str, DivergenceOpportunity] = {}
    
    @property
    def name(self) -> str:
        return "price_convergence"
    
    @property
    def description(self) -> str:
        return "Trade price divergences between platforms, betting on convergence"
    
    def analyze(self) -> List[Signal]:
        """Analyze matched markets for divergence opportunities."""
        signals = []
        
        # Get matched markets
        matched_markets = self.data_manager.get_matched_markets()
        
        for match in matched_markets:
            # Check for new opportunities
            opportunity = self._find_divergence(match)
            if opportunity:
                signal = self._create_entry_signal(opportunity)
                if signal:
                    signals.append(signal)
            
            # Check if existing positions should be closed
            market_key = match.normalized_title
            if market_key in self.open_positions:
                close_signal = self._check_convergence(match, market_key)
                if close_signal:
                    signals.append(close_signal)
        
        return signals
    
    def _find_divergence(self, match: MatchedMarket) -> Optional[DivergenceOpportunity]:
        """Find price divergence opportunity in a matched market."""
        kalshi_price = match.kalshi.yes_price
        poly_price = match.polymarket.yes_price
        
        if not kalshi_price or not poly_price:
            return None
        
        # Calculate divergence
        divergence = abs(kalshi_price - poly_price)
        avg_price = (kalshi_price + poly_price) / 2
        divergence_pct = divergence / avg_price if avg_price > 0 else 0
        
        if divergence_pct < self.min_divergence:
            return None
        
        # Check time to resolution
        time_to_resolution = None
        kalshi_end = match.kalshi.end_date
        poly_end = match.polymarket.end_date
        
        if kalshi_end:
            try:
                end_date = datetime.fromisoformat(kalshi_end.replace('Z', '+00:00'))
                time_to_resolution = end_date - datetime.now(end_date.tzinfo)
                
                if time_to_resolution.days > self.max_time_to_resolution_days:
                    return None  # Too far out
            except:
                pass
        
        # Determine which platform to buy on
        if kalshi_price < poly_price:
            recommended_platform = 'kalshi'
            expected_profit = poly_price - kalshi_price
        else:
            recommended_platform = 'polymarket'
            expected_profit = kalshi_price - poly_price
        
        return DivergenceOpportunity(
            kalshi_market=match.kalshi.id,
            polymarket_market=match.polymarket.id,
            market_title=match.kalshi.title,
            kalshi_price=kalshi_price,
            polymarket_price=poly_price,
            divergence=divergence,
            divergence_pct=divergence_pct,
            time_to_resolution=time_to_resolution,
            recommended_platform=recommended_platform,
            expected_profit=expected_profit
        )
    
    def _create_entry_signal(self, opp: DivergenceOpportunity) -> Optional[Signal]:
        """Create a signal to enter a convergence trade."""
        market_key = opp.market_title.lower()
        
        # Don't enter if we already have a position
        if market_key in self.open_positions:
            return None
        
        # Record the position
        self.open_positions[market_key] = opp
        
        # Determine signal strength based on divergence
        if opp.divergence_pct > 0.15:
            strength = SignalStrength.STRONG
            confidence = 0.85
        elif opp.divergence_pct > 0.10:
            strength = SignalStrength.MODERATE
            confidence = 0.75
        else:
            strength = SignalStrength.WEAK
            confidence = 0.65
        
        # Adjust confidence based on time to resolution
        if opp.time_to_resolution:
            days = opp.time_to_resolution.days
            if days < 7:
                confidence += 0.1  # Higher confidence near resolution
            elif days > 21:
                confidence -= 0.1  # Lower confidence far from resolution
        
        confidence = min(0.95, max(0.5, confidence))
        
        # Create signal
        if opp.recommended_platform == 'kalshi':
            market_id = opp.kalshi_market
            current_price = opp.kalshi_price
            target_price = opp.polymarket_price  # Converge to this
        else:
            market_id = opp.polymarket_market
            current_price = opp.polymarket_price
            target_price = opp.kalshi_price  # Converge to this
        
        return Signal(
            strategy_name=self.name,
            signal_type=SignalType.BUY,
            strength=strength,
            platform=opp.recommended_platform,
            market_id=market_id,
            market_title=opp.market_title,
            side="yes",
            target_price=target_price,
            current_price=current_price,
            confidence=confidence,
            reasoning=f"Price divergence: {opp.divergence_pct*100:.1f}% "
                     f"(Kalshi: {opp.kalshi_price:.2f}, Poly: {opp.polymarket_price:.2f}). "
                     f"Buy on {opp.recommended_platform} (lower), expect convergence.",
            metadata={
                'divergence': opp.divergence,
                'divergence_pct': opp.divergence_pct,
                'kalshi_price': opp.kalshi_price,
                'polymarket_price': opp.polymarket_price,
                'expected_profit': opp.expected_profit,
                'time_to_resolution_days': opp.time_to_resolution.days if opp.time_to_resolution else None
            }
        )
    
    def _check_convergence(self, match: MatchedMarket, 
                           market_key: str) -> Optional[Signal]:
        """Check if prices have converged enough to close position."""
        position = self.open_positions.get(market_key)
        if not position:
            return None
        
        kalshi_price = match.kalshi.yes_price
        poly_price = match.polymarket.yes_price
        
        if not kalshi_price or not poly_price:
            return None
        
        # Calculate current divergence
        divergence = abs(kalshi_price - poly_price)
        avg_price = (kalshi_price + poly_price) / 2
        divergence_pct = divergence / avg_price if avg_price > 0 else 0
        
        # Check if converged enough
        if divergence_pct > self.convergence_threshold:
            return None  # Not converged yet
        
        # Close the position
        del self.open_positions[market_key]
        
        # Create exit signal (opposite of entry)
        if position.recommended_platform == 'kalshi':
            market_id = position.kalshi_market
            current_price = kalshi_price
        else:
            market_id = position.polymarket_market
            current_price = poly_price
        
        # Calculate actual profit
        if position.recommended_platform == 'kalshi':
            actual_profit = current_price - position.kalshi_price
        else:
            actual_profit = current_price - position.polymarket_price
        
        return Signal(
            strategy_name=self.name,
            signal_type=SignalType.SELL,
            strength=SignalStrength.STRONG,
            platform=position.recommended_platform,
            market_id=market_id,
            market_title=position.market_title,
            side="yes",
            target_price=current_price,
            current_price=current_price,
            confidence=0.9,
            reasoning=f"Prices converged: {divergence_pct*100:.1f}% divergence "
                     f"(was {position.divergence_pct*100:.1f}%). "
                     f"Profit: {actual_profit*100:.1f}%",
            metadata={
                'entry_divergence': position.divergence_pct,
                'exit_divergence': divergence_pct,
                'actual_profit': actual_profit,
                'expected_profit': position.expected_profit
            }
        )
    
    def get_open_positions(self) -> List[Dict]:
        """Get all open convergence positions."""
        return [
            {
                'market_title': opp.market_title,
                'platform': opp.recommended_platform,
                'entry_divergence': opp.divergence_pct,
                'expected_profit': opp.expected_profit,
                'time_to_resolution_days': opp.time_to_resolution.days if opp.time_to_resolution else None
            }
            for opp in self.open_positions.values()
        ]
    
    def get_current_divergences(self) -> List[DivergenceOpportunity]:
        """Get all current divergence opportunities (for monitoring)."""
        opportunities = []
        matched_markets = self.data_manager.get_matched_markets()
        
        for match in matched_markets:
            opp = self._find_divergence(match)
            if opp:
                opportunities.append(opp)
        
        # Sort by divergence (highest first)
        opportunities.sort(key=lambda x: x.divergence_pct, reverse=True)
        return opportunities

