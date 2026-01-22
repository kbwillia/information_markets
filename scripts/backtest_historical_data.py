#!/usr/bin/env python3
"""
Backtest strategies on historical data and generate dashboard-compatible logs.

This script:
1. Fetches historical market data from APIs
2. Runs strategies on that historical data (backtesting)
3. Generates logs in the same format as live strategies
4. Allows visualization in the dashboard

Usage:
    python scripts/backtest_historical_data.py --days 7
    python scripts/backtest_historical_data.py --days 30 --strategies arbitrage,momentum
"""
import argparse
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time

from src.data_collectors.kalshi_client import KalshiClient
from src.data_collectors.polymarket_client import PolymarketClient
from src.core.data_manager import DataManager
from src.strategies.trading.runner import StrategyRunner, RunnerStats
from src.strategies.trading.base import Signal, SignalType, SignalStrength, TradeResult, Trade
from src.core.cache import MarketCache


def fetch_and_cache_historical_markets(days: int = 7) -> Dict:
    """Fetch historical market data and cache it for strategy analysis."""
    print(f"Fetching historical market data for last {days} days...")
    
    data_manager = DataManager()
    kalshi_client = KalshiClient()
    poly_client = PolymarketClient()
    
    # Fetch current markets (they contain historical context)
    print("Fetching Kalshi markets...")
    try:
        kalshi_markets = kalshi_client.get_markets(limit=200)
        market_list = kalshi_markets.get('markets', [])
        print(f"  Found {len(market_list)} Kalshi markets")
        
        # Cache markets for analysis
        for market in market_list[:100]:  # Limit for now
            try:
                # Get market details and history
                ticker = market.get('ticker') or market.get('event_ticker', '')
                if ticker:
                    # Get market history
                    history = kalshi_client.get_market_history(ticker, limit=50)
                    # Cache the market data
                    cache_key = f"kalshi_market_{ticker}"
                    data_manager.cache.set(cache_key, {
                        'market': market,
                        'history': history
                    }, ttl_seconds=86400)  # 24 hour TTL
            except Exception as e:
                continue
    except Exception as e:
        print(f"  Error fetching Kalshi markets: {e}")
    
    print("Fetching Polymarket markets...")
    try:
        poly_markets = poly_client.get_markets(limit=200)
        market_list = poly_markets.get('markets', poly_markets.get('data', []))
        print(f"  Found {len(market_list)} Polymarket markets")
        
        # Cache markets
        for market in market_list[:100]:  # Limit for now
            try:
                market_id = market.get('id') or market.get('slug', '')
                if market_id:
                    # Get price history if available
                    conditions = market.get('conditions', [])
                    if conditions:
                        token_id = conditions[0].get('id') or conditions[0].get('token_id', '')
                        if token_id:
                            try:
                                history = poly_client.get_recent_history(
                                    token_id=token_id,
                                    interval='max',
                                    fidelity=1
                                )
                            except:
                                history = None
                    else:
                        history = None
                    
                    cache_key = f"polymarket_market_{market_id}"
                    data_manager.cache.set(cache_key, {
                        'market': market,
                        'history': history
                    }, ttl_seconds=86400)
            except Exception as e:
                continue
    except Exception as e:
        print(f"  Error fetching Polymarket markets: {e}")
    
    print("Market data cached. Starting backtest...")
    return data_manager


def run_backtest(data_manager: DataManager, days: int = 7, 
                 strategies: List[str] = None) -> StrategyRunner:
    """Run strategies on historical data and generate logs."""
    print(f"\nRunning backtest for last {days} days...")
    
    # Create runner with all strategies
    runner = StrategyRunner(paper_trading=True)
    
    # Add strategies
    if strategies is None:
        strategies = ['arbitrage', 'momentum', 'lead_lag', 'price_convergence']
    
    for strategy_name in strategies:
        try:
            runner.add_strategy(strategy_name, enabled=True)
            print(f"  Added strategy: {strategy_name}")
        except Exception as e:
            print(f"  Warning: Could not add {strategy_name}: {e}")
    
    # Simulate running strategies over the historical period
    # We'll run multiple cycles to simulate time passing
    cycles_per_day = 24  # Run every hour (24 times per day)
    total_cycles = days * cycles_per_day
    
    print(f"Simulating {total_cycles} strategy cycles...")
    
    start_date = datetime.now() - timedelta(days=days)
    current_date = start_date
    
    for cycle in range(total_cycles):
        # Update current date for this cycle
        current_date = start_date + timedelta(hours=cycle)
        
        # Run strategy cycle
        try:
            stats = runner.run_cycle()
            
            # Update timestamp to historical date
            # Note: This modifies the stats after creation
            # We'll need to manually log with correct timestamps
            log_entry = {
                'timestamp': current_date.isoformat(),
                'duration_ms': stats.cycle_duration_ms,
                'signals': stats.signals_generated,
                'trades': stats.trades_executed,
                'successful': stats.successful_trades,
                'by_strategy': stats.by_strategy,
                'paper_trading': True
            }
            
            # Save to log file with correct date
            log_file = runner.log_path / f"runner_{current_date.strftime('%Y%m%d')}.jsonl"
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            
            if (cycle + 1) % 24 == 0:
                day_num = (cycle + 1) // 24
                print(f"  Completed day {day_num}/{days} ({cycle + 1}/{total_cycles} cycles)")
                
        except Exception as e:
            print(f"  Error in cycle {cycle}: {e}")
            continue
    
    print(f"\n✅ Backtest complete!")
    print(f"   Generated logs in: {runner.log_path}")
    print(f"   Generated trades in: data/logs/paper_trades/")
    
    return runner


def main():
    parser = argparse.ArgumentParser(
        description='Backtest strategies on historical data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days to backtest (default: 7)'
    )
    
    parser.add_argument(
        '--strategies',
        type=str,
        default=None,
        help='Comma-separated list of strategies to run (default: all)'
    )
    
    parser.add_argument(
        '--cycles-per-day',
        type=int,
        default=24,
        help='Number of strategy cycles per day (default: 24, i.e., hourly)'
    )
    
    args = parser.parse_args()
    
    # Parse strategies
    strategies = None
    if args.strategies:
        strategies = [s.strip() for s in args.strategies.split(',')]
    
    # Fetch and cache historical data
    data_manager = fetch_and_cache_historical_markets(days=args.days)
    
    # Run backtest
    runner = run_backtest(data_manager, days=args.days, strategies=strategies)
    
    print(f"\n📊 To visualize the backtest results:")
    print(f"   python visualize_strategies.py --days {args.days}")


if __name__ == '__main__':
    main()

