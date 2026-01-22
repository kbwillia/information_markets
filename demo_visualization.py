"""
Demo script to show visualization capabilities.

This creates some sample data and generates visualizations.
"""
from datetime import datetime, timedelta
from src.visualization.dashboard import StrategyDashboard
from src.strategies.trading.runner import StrategyRunner, RunnerStats
from src.strategies.trading.base import Signal, SignalType, SignalStrength, TradeResult, Trade
from src.core.data_manager import MarketData, MatchedMarket


def create_demo_runner():
    """Create a runner with some demo data."""
    runner = StrategyRunner(paper_trading=True)
    
    # Add some strategies
    runner.add_strategy('arbitrage', enabled=True)
    runner.add_strategy('momentum', enabled=True)
    runner.add_strategy('lead_lag', enabled=True)
    
    # Create some demo run history
    base_time = datetime.now() - timedelta(days=7)
    for i in range(20):
        timestamp = base_time + timedelta(hours=i*2)
        stats = RunnerStats(
            timestamp=timestamp,
            cycle_duration_ms=150 + i * 5,
            strategies_run=3,
            signals_generated=2 + (i % 3),
            trades_executed=1 + (i % 2),
            successful_trades=1 if i % 2 == 0 else 0,
            failed_trades=0 if i % 2 == 0 else 1,
            by_strategy={
                'arbitrage': {'signals': 1, 'trades': 1},
                'momentum': {'signals': 1, 'trades': 0},
                'lead_lag': {'signals': 0, 'trades': 0}
            }
        )
        runner.run_history.append(stats)
    
    # Create some demo signals
    for i in range(15):
        signal = Signal(
            strategy_name='arbitrage' if i % 2 == 0 else 'momentum',
            signal_type=SignalType.BUY,
            strength=SignalStrength.STRONG if i % 3 == 0 else SignalStrength.MODERATE,
            platform='kalshi' if i % 2 == 0 else 'polymarket',
            market_id=f'MARKET-{i}',
            market_title=f'Demo Market {i}',
            side='yes',
            target_price=0.50 + (i * 0.01),
            current_price=0.48 + (i * 0.01),
            confidence=0.7 + (i * 0.02),
            reasoning=f'Demo signal {i}',
            metadata={'arb_type': 'dutch_book' if i % 2 == 0 else 'price_gap'},
            timestamp=base_time + timedelta(hours=i*3)
        )
        runner.signal_history.append(signal)
    
    # Create some demo trades
    for i in range(10):
        signal = runner.signal_history[i] if i < len(runner.signal_history) else runner.signal_history[0]
        trade = Trade(
            signal=signal,
            platform=signal.platform,
            market_id=signal.market_id,
            side=signal.side,
            action='buy',
            quantity=10,
            price=signal.current_price
        )
        result = TradeResult(
            trade=trade,
            success=i % 3 != 0,  # Some failures
            order_id=f'ORDER-{i}',
            filled_price=signal.current_price + 0.01 if i % 3 != 0 else None,
            filled_quantity=10 if i % 3 != 0 else 0,
            timestamp=base_time + timedelta(hours=i*4)
        )
        runner.trade_history.append(result)
    
    return runner


def main():
    print("Creating demo runner with sample data...")
    runner = create_demo_runner()
    
    print("Creating dashboard...")
    dashboard = StrategyDashboard(runner=runner)
    
    print("\nGenerating visualizations...")
    dashboard.generate_all_charts(days=7, combined=True, filename="trading_dashboard.html")
    
    print("\nDemo complete! Check the data/visualizations/ directory for the dashboard.")
    print("Open trading_dashboard.html in your browser to view all charts in one place!")


if __name__ == '__main__':
    main()

