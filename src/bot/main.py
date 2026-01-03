"""Main trading bot orchestration."""
import asyncio
import time
from datetime import datetime
from typing import List, Dict, Optional
import json

from src.config import Config
from src.wallet_tracker.wallet_tracker import WalletTracker
from src.data_collectors.arbitrage_detector import ArbitrageDetector
from src.strategies.wallet_strategies import (
    FollowWinningWalletsStrategy,
    FollowWalletGroupStrategy,
    BetAgainstLosingWalletsStrategy
)
from src.reddit.reddit_scraper import RedditScraper
from src.llm.ollama_client import OllamaClient
from src.eda.analyzer import TradingAnalyzer


class TradingBot:
    """Main trading bot that orchestrates all strategies and data collection."""
    
    def __init__(self):
        Config.validate()
        
        self.wallet_tracker = WalletTracker()
        self.arbitrage_detector = ArbitrageDetector()
        self.reddit_scraper = RedditScraper()
        self.ollama_client = OllamaClient()
        self.analyzer = TradingAnalyzer(self.wallet_tracker)
        
        # Initialize strategies
        self.follow_winners = FollowWinningWalletsStrategy()
        self.follow_groups = None  # Will be set when group_id is provided
        self.bet_against_losers = BetAgainstLosingWalletsStrategy()
        
        self.running = False
        self.trade_history = []
    
    def collect_wallet_data(self, platforms: List[str] = ["kalshi", "polymarket"]):
        """Collect wallet data from platforms (placeholder - implement based on API capabilities)."""
        # Note: Actual implementation depends on API access to trade history
        # This is a placeholder for the data collection logic
        print("Collecting wallet data...")
        # In practice, you'd need to:
        # 1. Monitor public trade feeds
        # 2. Track wallet addresses from trades
        # 3. Record trades in the wallet tracker
        pass
    
    def scan_reddit_for_signals(self, subreddits: List[str] = None, 
                                keywords: List[str] = None) -> List[Dict]:
        """Scan Reddit for trading signals."""
        if not subreddits:
            subreddits = ["predictit", "polymarket", "kalshi", "wallstreetbets"]
        
        if not keywords:
            keywords = ["prediction market", "kalshi", "polymarket", "bet", "trade"]
        
        all_posts = []
        
        for subreddit in subreddits:
            try:
                posts = self.reddit_scraper.get_posts_from_subreddit(
                    subreddit, limit=50, time_filter="day"
                )
                all_posts.extend(posts)
            except Exception as e:
                print(f"Error scraping {subreddit}: {e}")
        
        # Use Ollama to detect signals
        signals = self.ollama_client.detect_trading_signals(all_posts, keywords)
        
        return signals
    
    def analyze_reddit_user(self, username: str) -> Dict:
        """Analyze a Reddit user for trading signal value."""
        posts = self.reddit_scraper.get_user_posts(username, limit=50)
        comments = self.reddit_scraper.get_user_comments(username, limit=100)
        profile = self.reddit_scraper.get_user_profile(username)
        
        analysis = self.ollama_client.analyze_reddit_account(username, posts, comments)
        
        return {
            "profile": profile,
            "analysis": analysis,
            "post_count": len(posts),
            "comment_count": len(comments)
        }
    
    def run_arbitrage_scan(self) -> List[Dict]:
        """Scan for arbitrage opportunities."""
        print("Scanning for arbitrage opportunities...")
        opportunities = self.arbitrage_detector.scan_for_arbitrage(limit=100)
        
        if opportunities:
            print(f"Found {len(opportunities)} arbitrage opportunities")
            for opp in opportunities[:5]:  # Show top 5
                print(f"  {opp['market_title']}: {opp['profit']:.2%} profit")
        
        return opportunities
    
    def run_wallet_strategies(self) -> Dict:
        """Run all wallet-based strategies."""
        results = {}
        
        print("Running Follow Winning Wallets strategy...")
        try:
            winner_trades = self.follow_winners.execute_strategy()
            results["follow_winners"] = {
                "trades_executed": len([t for t in winner_trades if t.get("status") == "executed"]),
                "trades_failed": len([t for t in winner_trades if t.get("status") == "failed"]),
                "details": winner_trades
            }
        except Exception as e:
            print(f"Error in follow winners strategy: {e}")
            results["follow_winners"] = {"error": str(e)}
        
        print("Running Bet Against Losing Wallets strategy...")
        try:
            loser_trades = self.bet_against_losers.execute_strategy()
            results["bet_against_losers"] = {
                "trades_executed": len([t for t in loser_trades if t.get("status") == "executed"]),
                "trades_failed": len([t for t in loser_trades if t.get("status") == "failed"]),
                "details": loser_trades
            }
        except Exception as e:
            print(f"Error in bet against losers strategy: {e}")
            results["bet_against_losers"] = {"error": str(e)}
        
        return results
    
    def run_eda_analysis(self, wallet_address: str = None):
        """Run exploratory data analysis."""
        if wallet_address:
            print(f"Analyzing wallet {wallet_address}...")
            analysis = self.analyzer.analyze_wallet_performance(wallet_address)
            patterns = self.analyzer.find_patterns(wallet_address)
            
            print(f"  Win Rate: {analysis['basic_stats']['win_rate']:.2%}")
            print(f"  Total Profit: ${analysis['basic_stats']['total_profit']:.2f}")
            print(f"  Total Trades: {analysis['basic_stats']['total_trades']}")
            
            if patterns:
                print(f"  Best Trading Hours: {patterns.get('best_hours', {})}")
            
            return analysis
        else:
            # Analyze top wallets
            print("Analyzing top winning wallets...")
            winning_wallets = self.wallet_tracker.get_winning_wallets(limit=10)
            
            for wallet in winning_wallets:
                print(f"  {wallet['address'][:10]}... - Win Rate: {wallet['win_rate']:.2%}, Profit: ${wallet['total_profit']:.2f}")
    
    def run(self, interval_seconds: int = 300, strategies: List[str] = None):
        """
        Run the trading bot continuously.
        
        Args:
            interval_seconds: Time between strategy runs
            strategies: List of strategies to run ('arbitrage', 'wallet', 'reddit')
        """
        if strategies is None:
            strategies = ["arbitrage", "wallet", "reddit"]
        
        self.running = True
        print(f"Starting trading bot at {datetime.now()}")
        print(f"Running strategies: {', '.join(strategies)}")
        print(f"Interval: {interval_seconds} seconds")
        
        try:
            while self.running:
                cycle_start = time.time()
                
                if "arbitrage" in strategies:
                    opportunities = self.run_arbitrage_scan()
                    # Execute arbitrage trades if opportunities found
                    # (Implementation would go here)
                
                if "wallet" in strategies:
                    wallet_results = self.run_wallet_strategies()
                    self.trade_history.extend([
                        r for r in wallet_results.values() 
                        if isinstance(r, dict) and "details" in r
                        for detail in r["details"]
                    ])
                
                if "reddit" in strategies:
                    reddit_signals = self.scan_reddit_for_signals()
                    if reddit_signals:
                        print(f"Found {len(reddit_signals)} Reddit signals")
                        # Process signals and potentially generate trades
                
                # Wait for next cycle
                elapsed = time.time() - cycle_start
                sleep_time = max(0, interval_seconds - elapsed)
                
                if sleep_time > 0:
                    print(f"Cycle complete. Sleeping for {sleep_time:.1f} seconds...")
                    time.sleep(sleep_time)
                else:
                    print("Warning: Cycle took longer than interval!")
        
        except KeyboardInterrupt:
            print("\nStopping bot...")
            self.running = False
        except Exception as e:
            print(f"Error in bot run loop: {e}")
            self.running = False
    
    def stop(self):
        """Stop the bot."""
        self.running = False
    
    def get_status(self) -> Dict:
        """Get current bot status."""
        return {
            "running": self.running,
            "total_trades": len(self.trade_history),
            "wallet_count": len(self.wallet_tracker.get_winning_wallets(limit=1000)),
            "timestamp": datetime.now().isoformat()
        }


if __name__ == "__main__":
    bot = TradingBot()
    bot.run(interval_seconds=300)

