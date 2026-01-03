"""EDA tools for analyzing wallet performance and market data."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import sqlite3

from src.wallet_tracker.wallet_tracker import WalletTracker


class TradingAnalyzer:
    """Comprehensive EDA tools for trading data."""
    
    def __init__(self, wallet_tracker: WalletTracker = None):
        self.wallet_tracker = wallet_tracker or WalletTracker()
        sns.set_style("darkgrid")
        plt.rcParams['figure.figsize'] = (12, 6)
    
    def analyze_wallet_performance(self, wallet_address: str) -> Dict:
        """Comprehensive analysis of a wallet's performance."""
        stats = self.wallet_tracker.get_wallet_stats(wallet_address)
        if not stats:
            return None
        
        trades_df = self.wallet_tracker.get_recent_trades(wallet_address, limit=1000)
        
        if trades_df.empty:
            return stats
        
        analysis = {
            "basic_stats": stats,
            "trade_analysis": {}
        }
        
        # Time-based analysis
        trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'])
        trades_df['date'] = trades_df['timestamp'].dt.date
        trades_df['hour'] = trades_df['timestamp'].dt.hour
        trades_df['day_of_week'] = trades_df['timestamp'].dt.day_name()
        
        # Profit analysis
        profitable_trades = trades_df[trades_df['profit'] > 0] if 'profit' in trades_df.columns else pd.DataFrame()
        losing_trades = trades_df[trades_df['profit'] < 0] if 'profit' in trades_df.columns else pd.DataFrame()
        
        analysis['trade_analysis'] = {
            "total_trades": len(trades_df),
            "profitable_trades": len(profitable_trades),
            "losing_trades": len(losing_trades),
            "avg_profit_per_trade": trades_df['profit'].mean() if 'profit' in trades_df.columns else 0,
            "total_profit": trades_df['profit'].sum() if 'profit' in trades_df.columns else 0,
            "max_profit": trades_df['profit'].max() if 'profit' in trades_df.columns else 0,
            "max_loss": trades_df['profit'].min() if 'profit' in trades_df.columns else 0,
            "profit_std": trades_df['profit'].std() if 'profit' in trades_df.columns else 0,
        }
        
        # Platform analysis
        if 'platform' in trades_df.columns:
            platform_stats = trades_df.groupby('platform').agg({
                'profit': ['count', 'sum', 'mean'] if 'profit' in trades_df.columns else 'count'
            })
            analysis['trade_analysis']['platform_breakdown'] = platform_stats.to_dict()
        
        # Market analysis
        if 'market_id' in trades_df.columns:
            market_stats = trades_df.groupby('market_id').agg({
                'profit': ['count', 'sum', 'mean'] if 'profit' in trades_df.columns else 'count'
            })
            analysis['trade_analysis']['top_markets'] = market_stats.nlargest(10, ('profit', 'sum') if 'profit' in trades_df.columns else ('profit', 'count')).to_dict()
        
        return analysis
    
    def plot_wallet_performance(self, wallet_address: str, save_path: Optional[str] = None):
        """Create visualization of wallet performance."""
        trades_df = self.wallet_tracker.get_recent_trades(wallet_address, limit=1000)
        
        if trades_df.empty:
            print(f"No trades found for wallet {wallet_address}")
            return
        
        trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'])
        trades_df = trades_df.sort_values('timestamp')
        
        if 'profit' in trades_df.columns:
            trades_df['cumulative_profit'] = trades_df['profit'].cumsum()
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Cumulative profit over time
        if 'cumulative_profit' in trades_df.columns:
            axes[0, 0].plot(trades_df['timestamp'], trades_df['cumulative_profit'])
            axes[0, 0].set_title('Cumulative Profit Over Time')
            axes[0, 0].set_xlabel('Date')
            axes[0, 0].set_ylabel('Cumulative Profit')
            axes[0, 0].grid(True)
        
        # Profit distribution
        if 'profit' in trades_df.columns:
            axes[0, 1].hist(trades_df['profit'], bins=50, edgecolor='black')
            axes[0, 1].set_title('Profit Distribution')
            axes[0, 1].set_xlabel('Profit')
            axes[0, 1].set_ylabel('Frequency')
            axes[0, 1].axvline(0, color='red', linestyle='--', label='Break Even')
            axes[0, 1].legend()
        
        # Trades by platform
        if 'platform' in trades_df.columns:
            platform_counts = trades_df['platform'].value_counts()
            axes[1, 0].bar(platform_counts.index, platform_counts.values)
            axes[1, 0].set_title('Trades by Platform')
            axes[1, 0].set_xlabel('Platform')
            axes[1, 0].set_ylabel('Number of Trades')
        
        # Trades by hour of day
        trades_df['hour'] = trades_df['timestamp'].dt.hour
        hour_counts = trades_df['hour'].value_counts().sort_index()
        axes[1, 1].bar(hour_counts.index, hour_counts.values)
        axes[1, 1].set_title('Trades by Hour of Day')
        axes[1, 1].set_xlabel('Hour')
        axes[1, 1].set_ylabel('Number of Trades')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def compare_wallets(self, wallet_addresses: List[str]) -> pd.DataFrame:
        """Compare performance across multiple wallets."""
        comparisons = []
        
        for address in wallet_addresses:
            stats = self.wallet_tracker.get_wallet_stats(address)
            if stats:
                comparisons.append(stats)
        
        if not comparisons:
            return pd.DataFrame()
        
        df = pd.DataFrame(comparisons)
        return df
    
    def analyze_wallet_group(self, group_id: int) -> Dict:
        """Analyze performance of a wallet group."""
        group_stats = self.wallet_tracker.get_group_stats(group_id)
        
        conn = sqlite3.connect(self.wallet_tracker.db_path)
        
        # Get all wallets in group
        query = """
            SELECT w.* FROM wallets w
            JOIN wallet_group_members wgm ON w.address = wgm.wallet_address
            WHERE wgm.group_id = ?
        """
        
        wallets_df = pd.read_sql_query(query, conn, params=(group_id,))
        
        # Get all trades from group
        query = """
            SELECT t.* FROM trades t
            JOIN wallet_group_members wgm ON t.wallet_address = wgm.wallet_address
            WHERE wgm.group_id = ?
        """
        
        trades_df = pd.read_sql_query(query, conn)
        conn.close()
        
        if trades_df.empty:
            return group_stats
        
        analysis = {
            "group_stats": group_stats,
            "aggregate_performance": {
                "total_trades": len(trades_df),
                "total_profit": trades_df['profit'].sum() if 'profit' in trades_df.columns else 0,
                "avg_profit_per_trade": trades_df['profit'].mean() if 'profit' in trades_df.columns else 0,
            },
            "top_performers": wallets_df.nlargest(5, 'total_profit').to_dict('records'),
            "worst_performers": wallets_df.nsmallest(5, 'total_profit').to_dict('records'),
        }
        
        return analysis
    
    def find_patterns(self, wallet_address: str) -> Dict:
        """Find trading patterns in wallet behavior."""
        trades_df = self.wallet_tracker.get_recent_trades(wallet_address, limit=1000)
        
        if trades_df.empty:
            return {}
        
        trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'])
        patterns = {}
        
        # Time patterns
        trades_df['hour'] = trades_df['timestamp'].dt.hour
        trades_df['day_of_week'] = trades_df['timestamp'].dt.day_name()
        
        if 'profit' in trades_df.columns:
            # Best trading hours
            hourly_profit = trades_df.groupby('hour')['profit'].mean()
            patterns['best_hours'] = hourly_profit.nlargest(3).to_dict()
            patterns['worst_hours'] = hourly_profit.nsmallest(3).to_dict()
            
            # Best trading days
            daily_profit = trades_df.groupby('day_of_week')['profit'].mean()
            patterns['best_days'] = daily_profit.nlargest(3).to_dict()
            patterns['worst_days'] = daily_profit.nsmallest(3).to_dict()
        
        # Market preferences
        if 'market_id' in trades_df.columns:
            market_counts = trades_df['market_id'].value_counts()
            patterns['favorite_markets'] = market_counts.head(5).to_dict()
        
        # Side preferences
        if 'side' in trades_df.columns:
            side_counts = trades_df['side'].value_counts()
            patterns['side_preferences'] = side_counts.to_dict()
        
        return patterns

