#!/usr/bin/env python3
"""
Main entry point for running trading strategies.

This script provides a command-line interface to:
- Run strategies once (for testing)
- Run strategies continuously (for production)
- View performance statistics
- Configure strategy parameters

Usage:
    # Run once in paper trading mode
    python run_strategies.py --once --paper
    
    # Run continuously with 30 second interval
    python run_strategies.py --interval 30 --paper
    
    # Run specific strategies only
    python run_strategies.py --strategies momentum,lead_lag,arbitrage --paper
    
    # Run in real trading mode (CAREFUL!)
    python run_strategies.py --interval 30 --real
"""
import argparse
import signal
import sys
import time
from datetime import datetime

from src.strategies.trading.runner import StrategyRunner, create_default_runner


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Run trading strategies on Kalshi and Polymarket',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run strategies once and exit'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=30,
        help='Interval between strategy runs in seconds (default: 30)'
    )
    
    parser.add_argument(
        '--paper',
        action='store_true',
        default=True,
        help='Run in paper trading mode (default)'
    )
    
    parser.add_argument(
        '--real',
        action='store_true',
        help='Run in real trading mode (CAREFUL!)'
    )
    
    parser.add_argument(
        '--strategies',
        type=str,
        default='all',
        help='Comma-separated list of strategies to run (default: all). '
             'Options: lead_lag, volume_spike, price_alerts, price_convergence, momentum, arbitrage'
    )
    
    parser.add_argument(
        '--max-daily-trades',
        type=int,
        default=50,
        help='Maximum trades per day (default: 50)'
    )
    
    parser.add_argument(
        '--max-position',
        type=float,
        default=100.0,
        help='Maximum position size in dollars (default: 100)'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )
    
    return parser.parse_args()


def setup_runner(args) -> StrategyRunner:
    """Set up the strategy runner based on arguments."""
    paper_trading = not args.real
    
    if not paper_trading:
        print("\n" + "=" * 60)
        print("WARNING: Running in REAL TRADING mode!")
        print("Real money will be used. Press Ctrl+C within 5 seconds to cancel.")
        print("=" * 60 + "\n")
        time.sleep(5)
    
    runner = StrategyRunner(
        paper_trading=paper_trading,
        max_daily_trades=args.max_daily_trades,
        max_position_size=args.max_position
    )
    
    # Add strategies
    if args.strategies == 'all':
        strategies = ['lead_lag', 'volume_spike', 'price_alerts', 
                     'price_convergence', 'momentum', 'arbitrage']
    else:
        strategies = [s.strip() for s in args.strategies.split(',')]
    
    for strategy in strategies:
        try:
            runner.add_strategy(strategy, enabled=True)
            print(f"  Added strategy: {strategy}")
        except ValueError as e:
            print(f"  Warning: Could not add strategy '{strategy}': {e}")
    
    return runner


def print_summary(runner: StrategyRunner):
    """Print performance summary."""
    summary = runner.get_performance_summary()
    
    print("\n" + "=" * 60)
    print("PERFORMANCE SUMMARY")
    print("=" * 60)
    print(f"  Mode: {'Paper Trading' if summary['paper_trading'] else 'REAL TRADING'}")
    print(f"  Strategies: {', '.join(summary['strategies_enabled'])}")
    print(f"  Run cycles: {summary['run_cycles']}")
    print(f"  Avg cycle time: {summary['avg_cycle_duration_ms']:.1f}ms")
    print()
    print(f"  Total signals: {summary['total_signals']}")
    print(f"  Total trades: {summary['total_trades']}")
    print(f"  Successful: {summary['successful_trades']}")
    print(f"  Failed: {summary['failed_trades']}")
    print(f"  Success rate: {summary['success_rate']*100:.1f}%")
    print()
    print(f"  Trades today: {summary['trades_today']}/{summary['max_daily_trades']}")
    print(f"  Paper P&L: ${summary['paper_pnl']:.2f}")
    print("=" * 60)
    
    # Show recent signals
    recent_signals = runner.get_recent_signals(5)
    if recent_signals:
        print("\nRecent Signals:")
        for sig in recent_signals:
            print(f"  [{sig['timestamp'][:19]}] {sig['strategy_name']}: "
                  f"{sig['signal_type'].upper()} {sig['market_title'][:30]} "
                  f"@ {sig['current_price']:.2f} (conf: {sig['confidence']:.0%})")
    
    # Show recent trades
    recent_trades = runner.get_recent_trades(5)
    if recent_trades:
        print("\nRecent Trades:")
        for trade in recent_trades:
            t = trade['trade']
            status = "OK" if trade['success'] else "FAIL"
            print(f"  [{trade['timestamp'][:19]}] {status}: "
                  f"{t['action'].upper()} {t['quantity']} {t['side']} "
                  f"@ {t['price']:.2f} on {t['platform']}")


def run_once(runner: StrategyRunner, verbose: bool):
    """Run strategies once."""
    print("\nRunning strategies once...")
    
    stats = runner.run_cycle()
    
    print(f"\nCompleted in {stats.cycle_duration_ms:.0f}ms")
    print(f"  Signals generated: {stats.signals_generated}")
    print(f"  Trades executed: {stats.trades_executed}")
    print(f"  Successful: {stats.successful_trades}")
    
    if verbose:
        print("\nBy strategy:")
        for name, data in stats.by_strategy.items():
            if 'error' in data:
                print(f"  {name}: ERROR - {data['error']}")
            else:
                print(f"  {name}: {data['signals']} signals, "
                      f"{data['trades']} trades ({data['successful']} success)")


def run_continuous(runner: StrategyRunner, interval: int, verbose: bool):
    """Run strategies continuously."""
    print(f"\nStarting continuous operation (interval: {interval}s)")
    print("Press Ctrl+C to stop\n")
    
    # Handle graceful shutdown
    stop_event = False
    
    def signal_handler(sig, frame):
        nonlocal stop_event
        print("\n\nShutting down...")
        stop_event = True
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start the runner
    runner.start(interval=interval)
    
    cycle_count = 0
    try:
        while not stop_event:
            time.sleep(interval)
            cycle_count += 1
            
            if verbose and cycle_count % 5 == 0:
                print_summary(runner)
    except KeyboardInterrupt:
        pass
    finally:
        runner.stop()
        print_summary(runner)


def main():
    """Main entry point."""
    args = parse_args()
    
    print("=" * 60)
    print("PREDICTION MARKET TRADING STRATEGIES")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'Paper Trading' if not args.real else 'REAL TRADING'}")
    print()
    
    # Set up runner
    print("Setting up strategies...")
    runner = setup_runner(args)
    
    if not runner.strategies:
        print("Error: No strategies configured!")
        sys.exit(1)
    
    print(f"\n{len(runner.strategies)} strategies ready")
    
    # Run
    if args.once:
        run_once(runner, args.verbose)
    else:
        run_continuous(runner, args.interval, args.verbose)
    
    print("\nDone!")


if __name__ == '__main__':
    main()

