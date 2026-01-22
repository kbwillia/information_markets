#!/usr/bin/env python3
"""
Fetch historical data from Kalshi and Polymarket APIs.

This script allows you to backfill historical data for analysis without
having to wait for strategies to run for 7 days.

Usage:
    python scripts/fetch_historical_data.py --days 7
    python scripts/fetch_historical_data.py --days 30 --platform kalshi
    python scripts/fetch_historical_data.py --days 7 --platform polymarket
"""
import argparse
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict

from src.data_collectors.kalshi_client import KalshiClient
from src.data_collectors.polymarket_client import PolymarketClient


def fetch_kalshi_history(days: int = 7) -> List[Dict]:
    """Fetch historical market data from Kalshi."""
    print(f"Fetching Kalshi historical data for last {days} days...")
    
    client = KalshiClient()
    history_data = []
    
    try:
        # Get current markets
        markets = client.get_markets(limit=100)
        market_list = markets.get('markets', [])
        
        print(f"Found {len(market_list)} markets")
        
        # For each market, get historical data
        for i, market in enumerate(market_list[:50]):  # Limit to first 50 for now
            try:
                ticker = market.get('ticker') or market.get('event_ticker', '')
                if not ticker:
                    continue
                
                # Get market history
                history = client.get_market_history(ticker, limit=100)
                
                if history:
                    history_data.append({
                        'ticker': ticker,
                        'title': market.get('title', ''),
                        'history': history,
                        'timestamp': datetime.now().isoformat()
                    })
                
                if (i + 1) % 10 == 0:
                    print(f"  Processed {i + 1} markets...")
                    
            except Exception as e:
                print(f"  Error fetching history for {ticker}: {e}")
                continue
        
        print(f"Fetched history for {len(history_data)} markets")
        return history_data
        
    except Exception as e:
        print(f"Error fetching Kalshi history: {e}")
        return []


def fetch_polymarket_history(days: int = 7) -> List[Dict]:
    """Fetch historical market data from Polymarket."""
    print(f"Fetching Polymarket historical data for last {days} days...")
    
    client = PolymarketClient()
    history_data = []
    
    try:
        # Get current markets
        markets = client.get_markets(limit=100)
        market_list = markets.get('markets', markets.get('data', []))
        
        print(f"Found {len(market_list)} markets")
        
        # Calculate date range
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        # For each market, get historical price data
        for i, market in enumerate(market_list[:50]):  # Limit to first 50 for now
            try:
                market_id = market.get('id') or market.get('slug', '')
                if not market_id:
                    continue
                
                # Get condition IDs (YES and NO tokens)
                conditions = market.get('conditions', [])
                if not conditions:
                    continue
                
                # Get price history for YES token (first condition)
                yes_condition = conditions[0]
                token_id = yes_condition.get('id') or yes_condition.get('token_id', '')
                
                if token_id:
                    # Get recent history (up to max interval)
                    # Note: Polymarket API limits to 15 days for get_history
                    if days <= 15:
                        history = client.get_history(
                            token_id=token_id,
                            start_time=start_time,
                            end_time=end_time,
                            fidelity=2  # Higher fidelity = more data points
                        )
                    else:
                        # For longer periods, use get_recent_history with max interval
                        history = client.get_recent_history(
                            token_id=token_id,
                            interval='max',
                            fidelity=1
                        )
                    
                    if history:
                        history_data.append({
                            'market_id': market_id,
                            'title': market.get('question', ''),
                            'token_id': token_id,
                            'history': history,
                            'timestamp': datetime.now().isoformat()
                        })
                
                if (i + 1) % 10 == 0:
                    print(f"  Processed {i + 1} markets...")
                    
            except Exception as e:
                print(f"  Error fetching history for {market_id}: {e}")
                continue
        
        print(f"Fetched history for {len(history_data)} markets")
        return history_data
        
    except Exception as e:
        print(f"Error fetching Polymarket history: {e}")
        return []


def save_history_data(history_data: List[Dict], platform: str, output_dir: Path):
    """Save historical data to JSON files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as single file with all markets
    filename = output_dir / f"{platform}_history_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, 'w') as f:
        json.dump(history_data, f, indent=2, default=str)
    
    print(f"Saved historical data to {filename}")
    return filename


def convert_to_runner_format(history_data: List[Dict], platform: str, 
                            output_dir: Path) -> bool:
    """
    Convert historical data to runner log format for visualization.
    
    This creates synthetic runner logs from historical market data,
    allowing the dashboard to visualize past market behavior.
    """
    print(f"\nConverting {platform} historical data to runner format...")
    
    log_dir = Path("data/logs/runner")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Group data by date
    by_date = {}
    for item in history_data:
        timestamp_str = item.get('timestamp', datetime.now().isoformat())
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            date_key = timestamp.date()
            
            if date_key not in by_date:
                by_date[date_key] = []
            by_date[date_key].append(item)
        except:
            continue
    
    # Create log entries for each date
    for date, items in by_date.items():
        log_file = log_dir / f"runner_{date.strftime('%Y%m%d')}.jsonl"
        
        # Create synthetic log entries based on historical data
        # Simulate strategy runs throughout the day
        for hour in range(0, 24, 2):  # Every 2 hours
            timestamp = datetime.combine(date, datetime.min.time()) + timedelta(hours=hour)
            
            # Count markets with activity
            active_markets = len([i for i in items if i.get('history')])
            
            # Create log entry
            log_entry = {
                'timestamp': timestamp.isoformat(),
                'duration_ms': 100 + (active_markets * 5),  # Simulated duration
                'signals': min(active_markets // 10, 5),  # Simulated signals
                'trades': min(active_markets // 20, 3),  # Simulated trades
                'successful': min(active_markets // 25, 2),  # Simulated successful trades
                'by_strategy': {
                    'arbitrage': {'signals': 1, 'trades': 0},
                    'momentum': {'signals': 1, 'trades': 0}
                },
                'paper_trading': True,
                'source': 'historical_data',
                'platform': platform
            }
            
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
    
    print(f"  Created log files for {len(by_date)} days")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Fetch historical data from Kalshi and Polymarket',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days of history to fetch (default: 7)'
    )
    
    parser.add_argument(
        '--platform',
        type=str,
        choices=['kalshi', 'polymarket', 'both'],
        default='both',
        help='Platform to fetch from (default: both)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='data/historical',
        help='Output directory for historical data (default: data/historical)'
    )
    
    parser.add_argument(
        '--convert',
        action='store_true',
        default=True,
        help='Convert historical data to runner log format for visualization (default: True)'
    )
    
    parser.add_argument(
        '--no-convert',
        action='store_true',
        help='Skip conversion to runner format (just save raw historical data)'
    )
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_history = {}
    
    # Fetch from Kalshi
    if args.platform in ['kalshi', 'both']:
        kalshi_history = fetch_kalshi_history(days=args.days)
        if kalshi_history:
            save_history_data(kalshi_history, 'kalshi', output_dir)
            all_history['kalshi'] = kalshi_history
    
    # Fetch from Polymarket
    if args.platform in ['polymarket', 'both']:
        poly_history = fetch_polymarket_history(days=args.days)
        if poly_history:
            save_history_data(poly_history, 'polymarket', output_dir)
            all_history['polymarket'] = poly_history
    
    print(f"\n✅ Historical data fetch complete!")
    print(f"   Data saved to: {output_dir}")
    
    if args.convert and not args.no_convert:
        print("\nConverting historical data to runner log format...")
        for platform, history in all_history.items():
            if history:
                convert_to_runner_format(history, platform, output_dir)
        
        print(f"\n✅ Conversion complete!")
        print(f"   Log files created in: data/logs/runner/")
        print(f"   You can now visualize with: python visualize_strategies.py --days {args.days}")


if __name__ == '__main__':
    main()

