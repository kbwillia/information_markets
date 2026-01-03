"""Trading strategies based on wallet tracking."""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import pandas as pd

from src.wallet_tracker.wallet_tracker import WalletTracker
from src.data_collectors.kalshi_client import KalshiClient
from src.data_collectors.polymarket_client import PolymarketClient
from src.config import Config


class WalletStrategy:
    """Base class for wallet-based strategies."""
    
    def __init__(self):
        self.wallet_tracker = WalletTracker()
        self.kalshi = KalshiClient()
        self.polymarket = PolymarketClient()
        self.max_position_size = Config.MAX_POSITION_SIZE
    
    def execute_trade(self, platform: str, market_id: str, side: str, 
                     action: str, size: float, price: float = None):
        """Execute a trade on the specified platform."""
        try:
            if platform.lower() == "kalshi":
                # Convert size to count (contracts)
                count = int(size)
                # Convert price to cents (0-100)
                price_cents = int(price * 100) if price else None
                
                result = self.kalshi.place_order(
                    ticker=market_id,
                    side=side,
                    action=action,
                    count=count,
                    price=price_cents
                )
                return result
            
            elif platform.lower() == "polymarket":
                result = self.polymarket.place_order(
                    market_id=market_id,
                    side=side.upper(),
                    size=size,
                    price=price,
                    order_type="LIMIT" if price else "MARKET"
                )
                return result
        except Exception as e:
            print(f"Error executing trade: {e}")
            return None


class FollowWinningWalletsStrategy(WalletStrategy):
    """Strategy to follow trades from winning wallets."""
    
    def __init__(self, min_win_rate: float = 0.6, min_trades: int = 10,
                 min_profit: float = 0.0, lookback_hours: int = 24):
        super().__init__()
        self.min_win_rate = min_win_rate
        self.min_trades = min_trades
        self.min_profit = min_profit
        self.lookback_hours = lookback_hours
    
    def get_winning_wallets(self) -> List[Dict]:
        """Get list of winning wallets."""
        return self.wallet_tracker.get_winning_wallets(
            min_trades=self.min_trades,
            min_win_rate=self.min_win_rate,
            min_profit=self.min_profit
        )
    
    def get_recent_trades(self, wallet_address: str) -> pd.DataFrame:
        """Get recent trades from a wallet."""
        cutoff_time = datetime.now() - timedelta(hours=self.lookback_hours)
        trades_df = self.wallet_tracker.get_recent_trades(wallet_address, limit=100)
        
        if trades_df.empty:
            return pd.DataFrame()
        
        trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'])
        recent_trades = trades_df[trades_df['timestamp'] >= cutoff_time]
        
        return recent_trades
    
    def generate_signals(self) -> List[Dict]:
        """Generate trading signals based on winning wallet activity."""
        signals = []
        winning_wallets = self.get_winning_wallets()
        
        for wallet in winning_wallets[:20]:  # Top 20 winning wallets
            recent_trades = self.get_recent_trades(wallet['address'])
            
            if recent_trades.empty:
                continue
            
            # Analyze recent trades for patterns
            for _, trade in recent_trades.iterrows():
                # Mirror the trade
                signal = {
                    "strategy": "follow_winning_wallet",
                    "wallet_address": wallet['address'],
                    "wallet_win_rate": wallet['win_rate'],
                    "wallet_profit": wallet['total_profit'],
                    "market_id": trade.get('market_id'),
                    "platform": trade.get('platform'),
                    "side": trade.get('side'),
                    "action": trade.get('action'),
                    "price": trade.get('price'),
                    "quantity": min(trade.get('quantity', 1), int(self.max_position_size)),
                    "confidence": min(wallet['win_rate'], 0.9),  # Cap at 90%
                    "timestamp": datetime.now().isoformat()
                }
                signals.append(signal)
        
        return signals
    
    def execute_strategy(self) -> List[Dict]:
        """Execute the strategy and place trades."""
        signals = self.generate_signals()
        executed_trades = []
        
        for signal in signals:
            try:
                result = self.execute_trade(
                    platform=signal['platform'],
                    market_id=signal['market_id'],
                    side=signal['side'],
                    action=signal['action'],
                    size=signal['quantity'],
                    price=signal.get('price')
                )
                
                if result:
                    executed_trades.append({
                        "signal": signal,
                        "result": result,
                        "status": "executed"
                    })
            except Exception as e:
                print(f"Error executing signal: {e}")
                executed_trades.append({
                    "signal": signal,
                    "error": str(e),
                    "status": "failed"
                })
        
        return executed_trades


class FollowWalletGroupStrategy(WalletStrategy):
    """Strategy to follow trades from a group of correlated wallets."""
    
    def __init__(self, group_id: int, consensus_threshold: float = 0.6):
        super().__init__()
        self.group_id = group_id
        self.consensus_threshold = consensus_threshold
    
    def get_group_trades(self, lookback_hours: int = 24) -> pd.DataFrame:
        """Get recent trades from all wallets in the group."""
        import sqlite3
        cutoff_time = datetime.now() - timedelta(hours=lookback_hours)
        
        conn = sqlite3.connect(self.wallet_tracker.db_path)
        
        query = """
            SELECT t.* FROM trades t
            JOIN wallet_group_members wgm ON t.wallet_address = wgm.wallet_address
            WHERE wgm.group_id = ?
            AND t.timestamp >= ?
            ORDER BY t.timestamp DESC
        """
        
        df = pd.read_sql_query(query, conn, params=(self.group_id, cutoff_time.isoformat()))
        conn.close()
        
        return df
    
    def find_consensus_trades(self, trades_df: pd.DataFrame) -> List[Dict]:
        """Find trades where multiple wallets in the group agree."""
        if trades_df.empty:
            return []
        
        # Group by market and side to find consensus
        consensus = trades_df.groupby(['market_id', 'side', 'action']).agg({
            'wallet_address': 'count',
            'price': 'mean'
        }).reset_index()
        
        consensus = consensus[consensus['wallet_address'] >= 
                             len(trades_df['wallet_address'].unique()) * self.consensus_threshold]
        
        signals = []
        for _, row in consensus.iterrows():
            signals.append({
                "strategy": "follow_wallet_group",
                "group_id": self.group_id,
                "market_id": row['market_id'],
                "side": row['side'],
                "action": row['action'],
                "price": row['price'],
                "wallet_count": int(row['wallet_address']),
                "confidence": min(row['wallet_address'] / 10, 0.9),
                "timestamp": datetime.now().isoformat()
            })
        
        return signals
    
    def execute_strategy(self) -> List[Dict]:
        """Execute the strategy."""
        trades_df = self.get_group_trades()
        signals = self.find_consensus_trades(trades_df)
        executed_trades = []
        
        for signal in signals:
            try:
                # Determine platform from trades
                platform = trades_df[trades_df['market_id'] == signal['market_id']]['platform'].iloc[0]
                
                result = self.execute_trade(
                    platform=platform,
                    market_id=signal['market_id'],
                    side=signal['side'],
                    action=signal['action'],
                    size=self.max_position_size * signal['confidence'],
                    price=signal.get('price')
                )
                
                if result:
                    executed_trades.append({
                        "signal": signal,
                        "result": result,
                        "status": "executed"
                    })
            except Exception as e:
                print(f"Error executing group strategy: {e}")
        
        return executed_trades


class BetAgainstLosingWalletsStrategy(WalletStrategy):
    """Strategy to take opposite positions from losing wallets."""
    
    def __init__(self, max_win_rate: float = 0.4, min_trades: int = 10,
                 max_profit: float = 0.0, lookback_hours: int = 24):
        super().__init__()
        self.max_win_rate = max_win_rate
        self.min_trades = min_trades
        self.max_profit = max_profit
        self.lookback_hours = lookback_hours
    
    def get_losing_wallets(self) -> List[Dict]:
        """Get list of losing wallets."""
        return self.wallet_tracker.get_losing_wallets(
            min_trades=self.min_trades,
            max_win_rate=self.max_win_rate,
            max_profit=self.max_profit
        )
    
    def get_recent_trades(self, wallet_address: str) -> pd.DataFrame:
        """Get recent trades from a losing wallet."""
        cutoff_time = datetime.now() - timedelta(hours=self.lookback_hours)
        trades_df = self.wallet_tracker.get_recent_trades(wallet_address, limit=100)
        
        if trades_df.empty:
            return pd.DataFrame()
        
        trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'])
        recent_trades = trades_df[trades_df['timestamp'] >= cutoff_time]
        
        return recent_trades
    
    def generate_signals(self) -> List[Dict]:
        """Generate trading signals by taking opposite positions from losing wallets."""
        signals = []
        losing_wallets = self.get_losing_wallets()
        
        for wallet in losing_wallets[:20]:  # Top 20 losing wallets
            recent_trades = self.get_recent_trades(wallet['address'])
            
            if recent_trades.empty:
                continue
            
            # Take opposite positions
            for _, trade in recent_trades.iterrows():
                # Flip the side/action
                original_side = trade.get('side')
                original_action = trade.get('action')
                
                # If they bought yes, we buy no (or sell yes)
                if original_side == 'yes' and original_action == 'buy':
                    new_side = 'no'
                    new_action = 'buy'
                elif original_side == 'yes' and original_action == 'sell':
                    new_side = 'yes'
                    new_action = 'buy'
                elif original_side == 'no' and original_action == 'buy':
                    new_side = 'yes'
                    new_action = 'buy'
                else:
                    new_side = 'no'
                    new_action = 'buy'
                
                signal = {
                    "strategy": "bet_against_losing_wallet",
                    "wallet_address": wallet['address'],
                    "wallet_win_rate": wallet['win_rate'],
                    "wallet_profit": wallet['total_profit'],
                    "market_id": trade.get('market_id'),
                    "platform": trade.get('platform'),
                    "original_side": original_side,
                    "original_action": original_action,
                    "side": new_side,
                    "action": new_action,
                    "price": trade.get('price'),
                    "quantity": min(trade.get('quantity', 1), int(self.max_position_size)),
                    "confidence": min(1.0 - wallet['win_rate'], 0.9),  # Higher confidence for worse wallets
                    "timestamp": datetime.now().isoformat()
                }
                signals.append(signal)
        
        return signals
    
    def execute_strategy(self) -> List[Dict]:
        """Execute the strategy and place trades."""
        signals = self.generate_signals()
        executed_trades = []
        
        for signal in signals:
            try:
                result = self.execute_trade(
                    platform=signal['platform'],
                    market_id=signal['market_id'],
                    side=signal['side'],
                    action=signal['action'],
                    size=signal['quantity'],
                    price=signal.get('price')
                )
                
                if result:
                    executed_trades.append({
                        "signal": signal,
                        "result": result,
                        "status": "executed"
                    })
            except Exception as e:
                print(f"Error executing signal: {e}")
        
        return executed_trades

