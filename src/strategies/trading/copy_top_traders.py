"""
Strategy: Copy Top Traders

This strategy:
1. Fetches top traders from Polymarket leaderboard
2. Gets their recent trading activity/positions
3. Generates signals to copy their trades
4. Only copies trades from profitable traders with good track records

Key insight: Top traders often have better information or analysis.
By copying their positions, we can ride their coattails.
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict

from src.strategies.trading.base import (
    BaseStrategy, Signal, SignalType, SignalStrength
)
from src.core.data_manager import DataManager, MarketData
from src.data_collectors.polymarket_client import PolymarketClient


class CopyTopTradersStrategy(BaseStrategy):
    """
    Copy trades from top-performing traders on Polymarket.
    
    How it works:
    1. Fetch top N traders from leaderboard (by PnL)
    2. Get their recent positions/activity
    3. Generate signals to copy their positions
    4. Only copy from traders with:
       - Positive PnL
       - Minimum volume threshold
       - Recent activity
    
    Parameters:
    - top_traders_count: Number of top traders to follow (default: 10)
    - min_trader_pnl: Minimum PnL for a trader to be considered (default: 1000)
    - min_trader_volume: Minimum volume for a trader (default: 10000)
    - lookback_hours: How far back to look for trader activity (default: 24)
    - min_confidence: Minimum confidence to copy a trade (default: 0.6)
    - time_period: Leaderboard time period (DAY, WEEK, MONTH, ALL) (default: ALL)
    """
    
    def __init__(self, data_manager: DataManager,
                 paper_trading: bool = True,
                 max_position_size: float = None,
                 top_traders_count: int = 10,
                 min_trader_pnl: float = 1000.0,
                 min_trader_volume: float = 10000.0,
                 lookback_hours: int = 24,
                 min_confidence: float = 0.6,
                 time_period: str = "ALL"):
        super().__init__(data_manager, paper_trading, max_position_size)
        
        self.top_traders_count = top_traders_count
        self.min_trader_pnl = min_trader_pnl
        self.min_trader_volume = min_trader_volume
        self.lookback_hours = lookback_hours
        self.min_confidence = min_confidence
        self.time_period = time_period
        
        self.polymarket_client = PolymarketClient()
        
        # Cache trader data to avoid repeated API calls
        self._trader_cache: Dict[str, Dict] = {}
        self._cache_timestamp: Optional[datetime] = None
        self._cache_ttl = timedelta(minutes=15)  # Cache for 15 minutes
    
    @property
    def name(self) -> str:
        return "copy_top_traders"
    
    @property
    def description(self) -> str:
        return "Copy trades from top-performing traders on Polymarket"
    
    def _get_top_traders(self) -> List[Dict]:
        """Get top traders from leaderboard, filtered by criteria."""
        # Check cache
        if (self._cache_timestamp and 
            datetime.now() - self._cache_timestamp < self._cache_ttl and
            'traders' in self._trader_cache):
            return self._trader_cache['traders']
        
        # Fetch from API
        try:
            result = self.polymarket_client.get_leaderboard(
                limit=50,  # Get more to filter
                time_period=self.time_period,
                order_by="PNL"
            )
            
            # Handle different response formats
            if isinstance(result, list):
                all_traders = result
            elif isinstance(result, dict):
                all_traders = result.get('data', result.get('traders', result.get('results', [])))
            else:
                all_traders = []
        except Exception as e:
            print(f"Error fetching leaderboard: {e}")
            all_traders = []
        
        # Filter by criteria and incorporate investigated copy watchlist
        filtered_traders = []
        seen_wallets = set()
        try:
            from src.research.top_accounts import TOP_ACCOUNTS_PATH, load_watchlist
            import json

            watchlist = load_watchlist()
            for item in watchlist.get("accounts", []):
                if not item.get("enabled", True):
                    continue
                addr = (item.get("address") or "").strip().lower()
                if not addr or addr in seen_wallets:
                    continue
                seen_wallets.add(addr)
                filtered_traders.append(
                    {
                        "proxyWallet": addr,
                        "userName": item.get("user_name") or addr[:10],
                        "pnl": float(item.get("pnl", 100000) or 100000),
                        "vol": float(item.get("volume", 500000) or 500000),
                        "rank": 1,
                        "copyability_score": int(item.get("copyability_score") or 8),
                    }
                )
        except Exception:
            pass

        for trader in all_traders:
            addr = (trader.get('proxyWallet') or trader.get('address') or '').strip().lower()
            if not addr or addr in seen_wallets:
                continue
            pnl = float(trader.get('pnl', 0) or 0)
            vol = float(trader.get('vol', trader.get('volume', 0)) or 0)
            rov_pct = (pnl / vol * 100.0) if vol > 0 else 0.0

            # Only include profitable traders with sufficient volume and non-HFT margin (>= 1.5% RoV)
            if pnl >= self.min_trader_pnl and vol >= self.min_trader_volume and rov_pct >= 1.5:
                seen_wallets.add(addr)
                filtered_traders.append(trader)
        
        # Sort by % return on volume and PnL and take top N
        filtered_traders.sort(
            key=lambda t: (
                int(t.get('copyability_score') or 0),
                float(t.get('pnl', 0) or 0),
            ),
            reverse=True,
        )
        top_traders = filtered_traders[:self.top_traders_count]
        
        # Cache results
        self._trader_cache['traders'] = top_traders
        self._cache_timestamp = datetime.now()
        
        return top_traders
    
    def _get_trader_positions(self, trader_address: str) -> List[Dict]:
        """Get current positions for a trader."""
        try:
            positions = self.polymarket_client.get_user_positions(
                user=trader_address,
                limit=50,
                sort_by="TOKENS",
                sort_direction="DESC"
            )
            
            # Handle different response formats
            if isinstance(positions, list):
                return positions
            elif isinstance(positions, dict):
                return positions.get('data', positions.get('positions', []))
            return []
        except Exception as e:
            print(f"Error fetching positions for trader {trader_address[:8]}...: {e}")
            return []
    
    
    def analyze(self) -> List[Signal]:
        """Analyze top traders and generate copy signals."""
        signals = []
        
        # Get top traders
        top_traders = self._get_top_traders()
        
        if not top_traders:
            return signals
        
        # For each top trader, get their positions and recent activity
        for trader in top_traders:
            trader_address = trader.get('proxyWallet') or trader.get('address')
            if not trader_address:
                continue
            
            trader_pnl = float(trader.get('pnl', 0) or 0)
            trader_vol = float(trader.get('vol', trader.get('volume', 0)) or 0)
            trader_rank = int(trader.get('rank', 0) or 0)
            trader_name = trader.get('userName') or trader.get('user_name') or trader_address[:10]
            
            # Calculate confidence based on trader performance
            # Higher PnL and volume = higher confidence
            pnl_confidence = min(trader_pnl / 100000, 0.5)  # Cap at 0.5
            rank_confidence = max(0.3, 0.5 - (trader_rank - 1) * 0.02)  # Top rank = 0.5, decreases
            base_confidence = (pnl_confidence + rank_confidence) / 2
            
            if base_confidence < self.min_confidence:
                continue
            
            # Get trader's current positions
            positions = self._get_trader_positions(trader_address)
            
            # Generate signals from positions
            for position in positions[:20]:  # Limit to top 20 positions
                try:
                    # Extract market information
                    condition_id = position.get('conditionId') or position.get('condition_id') or position.get('asset')
                    if not condition_id:
                        continue
                    
                    # Get market data
                    market = self.data_manager.get_market('polymarket', condition_id)
                    if not market:
                        # Try to find market by condition ID
                        all_markets = self.data_manager.get_all_markets('polymarket')
                        market = next((m for m in all_markets if m.id == condition_id or 
                                      getattr(m, 'condition_id', None) == condition_id), None)
                    
                    if not market:
                        continue
                    
                    # Determine side based on position
                    # Positive balance = YES position, negative = NO position
                    balance = float(position.get('balance', position.get('tokens', 0)) or 0)
                    if balance <= 0:
                        continue
                    
                    # Get current price
                    current_price = market.yes_price
                    if not current_price:
                        continue
                    
                    # Determine signal direction
                    # If trader has YES position, we buy YES
                    # If trader has NO position, we buy NO
                    outcome_index = position.get('outcomeIndex', 0)
                    side = 'yes' if outcome_index == 0 else 'no'
                    
                    # Calculate confidence based on position size and trader performance
                    position_size = abs(balance)
                    size_confidence = min(position_size / 1000, 0.3)  # Larger positions = more confidence
                    final_confidence = min(base_confidence + size_confidence, 0.95)
                    
                    if final_confidence < self.min_confidence:
                        continue
                    
                    # Determine signal strength
                    if final_confidence >= 0.8:
                        strength = SignalStrength.STRONG
                    elif final_confidence >= 0.65:
                        strength = SignalStrength.MODERATE
                    else:
                        strength = SignalStrength.WEAK
                    
                    # Create signal
                    signal = Signal(
                        strategy_name=self.name,
                        signal_type=SignalType.BUY,
                        strength=strength,
                        platform='polymarket',
                        market_id=condition_id,
                        market_title=market.title[:100] if market.title else 'Unknown Market',
                        side=side,
                        target_price=current_price * 1.05,  # Expect 5% upside
                        current_price=current_price,
                        confidence=final_confidence,
                        reasoning=f"Copying {trader_name} (Rank {trader_rank}, PnL: ${trader_pnl:,.0f}, Vol: ${trader_vol:,.0f}). Position size: {position_size:.2f}",
                        metadata={
                            'copied_account': trader_name,
                            'trader_name': trader_name,
                            'trader_address': trader_address,
                            'trader_rank': trader_rank,
                            'trader_pnl': trader_pnl,
                            'trader_volume': trader_vol,
                            'position_size': position_size,
                            'outcome_index': outcome_index
                        }
                    )
                    signals.append(signal)
                    
                except Exception as e:
                    print(f"Error processing position for trader {trader_address[:8]}...: {e}")
                    continue
            
            # Also check recent activity for new trades (using get_activity)
            try:
                activity = self.polymarket_client.get_activity(
                    user=trader_address,
                    limit=50
                )
                
                # Handle different response formats
                if isinstance(activity, list):
                    activities = activity
                elif isinstance(activity, dict):
                    activities = activity.get('data', activity.get('activity', []))
                else:
                    activities = []
                
                # Filter by time
                cutoff_time = datetime.now() - timedelta(hours=self.lookback_hours)
                recent_activity = []
                for act in activities:
                    # Parse timestamp (could be in various formats)
                    timestamp = act.get('timestamp') or act.get('time') or act.get('createdAt')
                    if timestamp:
                        try:
                            if isinstance(timestamp, (int, float)):
                                act_time = datetime.fromtimestamp(timestamp / 1000 if timestamp > 1e10 else timestamp)
                            elif isinstance(timestamp, str):
                                from dateutil import parser
                                act_time = parser.parse(timestamp)
                            else:
                                continue
                            
                            if act_time >= cutoff_time:
                                recent_activity.append(act)
                        except:
                            continue
            except Exception as e:
                print(f"Error fetching activity for trader {trader_address[:8]}...: {e}")
                recent_activity = []
            
            for activity in recent_activity[:10]:  # Limit to 10 most recent
                try:
                    # Only process trade activities
                    activity_type = activity.get('type') or activity.get('activityType')
                    if activity_type not in ['trade', 'TRADE', 'buy', 'sell']:
                        continue
                    
                    # Extract market information
                    condition_id = activity.get('conditionId') or activity.get('condition_id') or activity.get('asset')
                    if not condition_id:
                        continue
                    
                    # Get market data
                    market = self.data_manager.get_market('polymarket', condition_id)
                    if not market:
                        all_markets = self.data_manager.get_all_markets('polymarket')
                        market = next((m for m in all_markets if m.id == condition_id or 
                                      getattr(m, 'condition_id', None) == condition_id), None)
                    
                    if not market:
                        continue
                    
                    # Determine side from activity
                    side = activity.get('side', 'yes').lower()
                    if side not in ['yes', 'no']:
                        side = 'yes'  # Default
                    
                    # Get current price
                    current_price = market.yes_price
                    if not current_price:
                        continue
                    
                    # Activity-based confidence is slightly lower (they may have already closed)
                    activity_confidence = base_confidence * 0.8
                    
                    if activity_confidence < self.min_confidence:
                        continue
                    
                    # Determine signal strength
                    if activity_confidence >= 0.75:
                        strength = SignalStrength.STRONG
                    elif activity_confidence >= 0.6:
                        strength = SignalStrength.MODERATE
                    else:
                        strength = SignalStrength.WEAK
                    
                    # Create signal
                    signal = Signal(
                        strategy_name=self.name,
                        signal_type=SignalType.BUY,
                        strength=strength,
                        platform='polymarket',
                        market_id=condition_id,
                        market_title=market.title[:100] if market.title else 'Unknown Market',
                        side=side,
                        target_price=current_price * 1.05,
                        current_price=current_price,
                        confidence=activity_confidence,
                        reasoning=f"Copying recent trade from {trader_name} (Rank {trader_rank}, PnL: ${trader_pnl:,.0f})",
                        metadata={
                            'copied_account': trader_name,
                            'trader_name': trader_name,
                            'trader_address': trader_address,
                            'trader_rank': trader_rank,
                            'trader_pnl': trader_pnl,
                            'activity_type': activity_type,
                            'activity_timestamp': activity.get('timestamp')
                        }
                    )
                    signals.append(signal)
                    
                except Exception as e:
                    print(f"Error processing activity for trader {trader_address[:8]}...: {e}")
                    continue
        
        return signals
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics for this strategy."""
        return {
            'strategy_name': self.name,
            'top_traders_tracked': self.top_traders_count,
            'min_trader_pnl': self.min_trader_pnl,
            'min_trader_volume': self.min_trader_volume,
            'time_period': self.time_period
        }

