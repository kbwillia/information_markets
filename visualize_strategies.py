"""
Visualization script for trading strategies.

Usage:
    python visualize_strategies.py                    # Generate all charts
    python visualize_strategies.py --days 30          # Last 30 days
    python visualize_strategies.py --chart performance # Specific chart
"""
import argparse
from pathlib import Path

from src.visualization.dashboard import StrategyDashboard
from src.strategies.trading.runner import create_default_runner


def main():
    parser = argparse.ArgumentParser(description='Visualize trading strategy performance')
    parser.add_argument('--days', type=int, default=7, 
                       help='Number of days of history to load (default: 7)')
    parser.add_argument('--chart', type=str, choices=[
        'all', 'performance', 'comparison', 'signals', 'matching', 'arbitrage'
    ], default='all', help='Which chart to generate (default: all)')
    parser.add_argument('--runner', action='store_true',
                       help='Use active runner instance (if available)')
    parser.add_argument('--demo', action='store_true',
                       help='Generate demo data if no real data is available')
    parser.add_argument('--combined', action='store_true', default=True,
                       help='Generate combined dashboard (default: True)')
    parser.add_argument('--separate', action='store_true',
                       help='Generate separate HTML files instead of combined dashboard')
    parser.add_argument('--dashboard-name', type=str, default='trading_dashboard.html',
                       help='Name for combined dashboard file (default: trading_dashboard.html)')
    
    args = parser.parse_args()
    
    # Handle conflicting flags
    if args.separate:
        args.combined = False
    
    # Create dashboard
    if args.runner:
        print("Creating runner instance...")
        runner = create_default_runner(paper_trading=True)
        dashboard = StrategyDashboard(runner=runner)
    elif args.demo:
        print("Creating runner instance with demo data...")
        from demo_visualization import create_demo_runner
        runner = create_demo_runner()
        dashboard = StrategyDashboard(runner=runner)
        print(f"Using demo data with {len(runner.run_history)} cycles, "
              f"{len(runner.signal_history)} signals, "
              f"{len(runner.trade_history)} trades")
    else:
        dashboard = StrategyDashboard()
        # Check if we have any data
        data = dashboard.load_history_from_logs(days=args.days)
        if not data['run_history'] and not data['trades']:
            print("No data found in log files.")
            print("Generating demo charts with sample data...")
            from demo_visualization import create_demo_runner
            runner = create_demo_runner()
            dashboard = StrategyDashboard(runner=runner)
            print(f"Using demo data with {len(runner.run_history)} cycles, "
                  f"{len(runner.signal_history)} signals, "
                  f"{len(runner.trade_history)} trades")
    
    # Generate charts
    if args.chart == 'all':
        dashboard.generate_all_charts(days=args.days, combined=args.combined, filename=args.dashboard_name)
    elif args.chart == 'performance':
        dashboard.plot_performance_over_time(days=args.days, save=True)
    elif args.chart == 'comparison':
        if dashboard.runner:
            dashboard.plot_strategy_comparison(save=True)
        else:
            print("Strategy comparison requires an active runner. Use --runner or --demo flag.")
    elif args.chart == 'signals':
        if dashboard.runner:
            dashboard.plot_signal_distribution(save=True)
        else:
            print("Signal distribution requires an active runner. Use --runner or --demo flag.")
    elif args.chart == 'matching':
        dashboard.plot_market_matching_stats(save=True)
    elif args.chart == 'arbitrage':
        if dashboard.runner:
            dashboard.plot_arbitrage_opportunities(save=True)
        else:
            print("Arbitrage chart requires an active runner. Use --runner or --demo flag.")


if __name__ == '__main__':
    main()

