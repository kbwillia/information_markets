"""Example script for running wallet-based strategies."""
from src.strategies.wallet_strategies import (
    FollowWinningWalletsStrategy,
    BetAgainstLosingWalletsStrategy
)
from src.wallet_tracker.wallet_tracker import WalletTracker

# Initialize wallet tracker
wallet_tracker = WalletTracker()

# Example: Follow winning wallets
print("Running Follow Winning Wallets Strategy...")
follow_winners = FollowWinningWalletsStrategy(
    min_win_rate=0.65,
    min_trades=15,
    min_profit=100.0
)

signals = follow_winners.generate_signals()
print(f"Generated {len(signals)} signals")

for signal in signals[:5]:  # Show top 5
    print(f"  Market: {signal['market_id']}, "
          f"Action: {signal['action']} {signal['side']}, "
          f"Confidence: {signal['confidence']:.2%}")

# Execute strategy (commented out to avoid actual trades)
# executed = follow_winners.execute_strategy()
# print(f"Executed {len([t for t in executed if t['status'] == 'executed'])} trades")

# Example: Bet against losing wallets
print("\nRunning Bet Against Losing Wallets Strategy...")
bet_against = BetAgainstLosingWalletsStrategy(
    max_win_rate=0.35,
    min_trades=15,
    max_profit=-50.0
)

signals = bet_against.generate_signals()
print(f"Generated {len(signals)} signals")

for signal in signals[:5]:
    print(f"  Market: {signal['market_id']}, "
          f"Action: {signal['action']} {signal['side']}, "
          f"Confidence: {signal['confidence']:.2%}")

# Example: Create and analyze wallet groups
print("\nCreating wallet group...")
winning_wallets = wallet_tracker.get_winning_wallets(limit=10)
wallet_addresses = [w['address'] for w in winning_wallets]

if wallet_addresses:
    group_id = wallet_tracker.create_wallet_group("Top Winners", wallet_addresses)
    print(f"Created group {group_id} with {len(wallet_addresses)} wallets")
    
    group_stats = wallet_tracker.get_group_stats(group_id)
    print(f"Group Stats: {group_stats}")

