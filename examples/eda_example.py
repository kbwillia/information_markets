"""Example script for running EDA analysis."""
from src.wallet_tracker.wallet_tracker import WalletTracker
from src.wallet_tracker.data_collector import WalletDataCollector
from src.eda.analyzer import TradingAnalyzer

# Initialize components
wallet_tracker = WalletTracker()
collector = WalletDataCollector(wallet_tracker)
analyzer = TradingAnalyzer(wallet_tracker)

# First, collect some wallet data
print("Collecting wallet data...")
# Option 1: Add sample data for testing
collector.add_sample_wallets()

# Option 2: Collect real data from APIs (if available)
# collector.collect_kalshi_trades(limit=100)
# collector.collect_polymarket_trades(limit=100)

# Example: Analyze a specific wallet
wallet_address = "example_wallet_address"
analysis = analyzer.analyze_wallet_performance(wallet_address)

if analysis:
    print(f"Wallet Analysis for {wallet_address}:")
    print(f"  Win Rate: {analysis['basic_stats']['win_rate']:.2%}")
    print(f"  Total Profit: ${analysis['basic_stats']['total_profit']:.2f}")
    print(f"  Total Trades: {analysis['basic_stats']['total_trades']}")
    
    # Generate visualization
    analyzer.plot_wallet_performance(wallet_address, save_path="data/wallet_analysis.png")
    
    # Find patterns
    patterns = analyzer.find_patterns(wallet_address)
    print(f"\nTrading Patterns:")
    print(f"  Best Hours: {patterns.get('best_hours', {})}")
    print(f"  Best Days: {patterns.get('best_days', {})}")

# Example: Compare multiple wallets
wallet_addresses = ["wallet1", "wallet2", "wallet3"]
comparison = analyzer.compare_wallets(wallet_addresses)
print("\nWallet Comparison:")
print(comparison)

# Example: Get winning wallets
winning_wallets = wallet_tracker.get_winning_wallets(min_trades=10, min_win_rate=0.6)
print(f"\nFound {len(winning_wallets)} winning wallets")

