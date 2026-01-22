"""
Unified Strategy Runner

Orchestrates multiple strategies, handles:
- Strategy lifecycle management
- Performance tracking
- Risk management
- Logging and monitoring
"""
import time
import threading
import json
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field

from src.core.data_manager import DataManager
from src.strategies.trading.base import BaseStrategy, Signal, TradeResult
from src.strategies.trading.lead_lag import LeadLagStrategy
from src.strategies.trading.volume_spike import VolumeSpikeStrategy
from src.strategies.trading.price_alerts import PriceAlertStrategy
from src.strategies.trading.price_convergence import PriceConvergenceStrategy
from src.strategies.trading.momentum import MomentumStrategy
from src.strategies.trading.arbitrage import ArbitrageStrategy
from src.config import Config


@dataclass
class StrategyConfig:
    """Configuration for a single strategy."""
    name: str
    enabled: bool = True
    weight: float = 1.0  # Position size multiplier
    max_signals_per_run: int = 5
    params: Dict = field(default_factory=dict)


@dataclass
class RunnerStats:
    """Statistics from a strategy run cycle."""
    timestamp: datetime
    cycle_duration_ms: float
    strategies_run: int
    signals_generated: int
    trades_executed: int
    successful_trades: int
    failed_trades: int
    by_strategy: Dict[str, Dict]


class StrategyRunner:
    """
    Unified runner for all trading strategies.
    
    Features:
    - Runs multiple strategies in parallel
    - Paper trading mode by default
    - Risk management (max daily trades, position limits)
    - Performance tracking and logging
    - Background operation with configurable interval
    
    Usage:
        runner = StrategyRunner(paper_trading=True)
        runner.add_strategy('lead_lag', enabled=True)
        runner.add_strategy('momentum', enabled=True)
        
        # Run once
        results = runner.run_cycle()
        
        # Or run continuously
        runner.start(interval=30)  # Every 30 seconds
        # ... later ...
        runner.stop()
    """
    
    def __init__(self, paper_trading: bool = True,
                 max_daily_trades: int = None,
                 max_position_size: float = None,
                 log_path: str = "data/logs/runner"):
        self.paper_trading = paper_trading
        self.max_daily_trades = max_daily_trades or Config.MAX_DAILY_TRADES
        self.max_position_size = max_position_size or Config.MAX_POSITION_SIZE
        
        # Initialize data manager
        self.data_manager = DataManager()
        
        # Strategy registry
        self.strategy_configs: Dict[str, StrategyConfig] = {}
        self.strategies: Dict[str, BaseStrategy] = {}
        
        # Track daily activity
        self.trades_today = 0
        self.last_reset_date = datetime.now().date()
        
        # Logging
        self.log_path = Path(log_path)
        self.log_path.mkdir(parents=True, exist_ok=True)
        
        # Background runner control
        self._runner_thread: Optional[threading.Thread] = None
        self._stop_runner = threading.Event()
        self._run_interval = 30
        
        # History
        self.run_history: List[RunnerStats] = []
        self.signal_history: List[Signal] = []
        self.trade_history: List[TradeResult] = []
    
    def add_strategy(self, strategy_name: str, enabled: bool = True,
                     weight: float = 1.0, max_signals: int = 5,
                     **params):
        """Add a strategy to the runner."""
        config = StrategyConfig(
            name=strategy_name,
            enabled=enabled,
            weight=weight,
            max_signals_per_run=max_signals,
            params=params
        )
        self.strategy_configs[strategy_name] = config
        
        # Instantiate strategy
        if enabled:
            self.strategies[strategy_name] = self._create_strategy(config)
    
    def _create_strategy(self, config: StrategyConfig) -> BaseStrategy:
        """Create a strategy instance from config."""
        adjusted_position = self.max_position_size * config.weight
        
        strategy_classes = {
            'lead_lag': LeadLagStrategy,
            'volume_spike': VolumeSpikeStrategy,
            'price_alerts': PriceAlertStrategy,
            'price_convergence': PriceConvergenceStrategy,
            'momentum': MomentumStrategy,
            'arbitrage': ArbitrageStrategy
        }
        
        cls = strategy_classes.get(config.name)
        if not cls:
            raise ValueError(f"Unknown strategy: {config.name}")
        
        return cls(
            data_manager=self.data_manager,
            paper_trading=self.paper_trading,
            max_position_size=adjusted_position,
            **config.params
        )
    
    def enable_strategy(self, strategy_name: str):
        """Enable a strategy."""
        if strategy_name in self.strategy_configs:
            config = self.strategy_configs[strategy_name]
            config.enabled = True
            if strategy_name not in self.strategies:
                self.strategies[strategy_name] = self._create_strategy(config)
    
    def disable_strategy(self, strategy_name: str):
        """Disable a strategy."""
        if strategy_name in self.strategy_configs:
            self.strategy_configs[strategy_name].enabled = False
        if strategy_name in self.strategies:
            del self.strategies[strategy_name]
    
    def run_cycle(self) -> RunnerStats:
        """Run one cycle of all enabled strategies."""
        start_time = time.time()
        
        # Check if we need to reset daily counter
        today = datetime.now().date()
        if today > self.last_reset_date:
            self.trades_today = 0
            self.last_reset_date = today
        
        # Check if we've hit daily limit
        if self.trades_today >= self.max_daily_trades:
            print(f"Daily trade limit reached ({self.max_daily_trades})")
            return RunnerStats(
                timestamp=datetime.now(),
                cycle_duration_ms=0,
                strategies_run=0,
                signals_generated=0,
                trades_executed=0,
                successful_trades=0,
                failed_trades=0,
                by_strategy={}
            )
        
        all_signals = []
        all_results = []
        by_strategy = {}
        
        # Run each enabled strategy
        for name, strategy in self.strategies.items():
            config = self.strategy_configs[name]
            
            try:
                # Analyze (reads from cache only)
                signals = strategy.analyze()
                
                # Limit signals per strategy
                signals = signals[:config.max_signals_per_run]
                
                # Execute trades
                results = []
                for signal in signals:
                    if self.trades_today >= self.max_daily_trades:
                        break
                    
                    trade = strategy.generate_trade(signal)
                    if trade:
                        result = strategy.execute_trade(trade)
                        results.append(result)
                        if result.success:
                            self.trades_today += 1
                
                all_signals.extend(signals)
                all_results.extend(results)
                
                by_strategy[name] = {
                    'signals': len(signals),
                    'trades': len(results),
                    'successful': sum(1 for r in results if r.success)
                }
            
            except Exception as e:
                print(f"Error running strategy {name}: {e}")
                by_strategy[name] = {'error': str(e)}
        
        # Record history
        self.signal_history.extend(all_signals)
        self.trade_history.extend(all_results)
        
        # Keep history bounded
        if len(self.signal_history) > 1000:
            self.signal_history = self.signal_history[-1000:]
        if len(self.trade_history) > 1000:
            self.trade_history = self.trade_history[-1000:]
        
        # Calculate stats
        cycle_duration = (time.time() - start_time) * 1000
        
        stats = RunnerStats(
            timestamp=datetime.now(),
            cycle_duration_ms=cycle_duration,
            strategies_run=len(self.strategies),
            signals_generated=len(all_signals),
            trades_executed=len(all_results),
            successful_trades=sum(1 for r in all_results if r.success),
            failed_trades=sum(1 for r in all_results if not r.success),
            by_strategy=by_strategy
        )
        
        self.run_history.append(stats)
        if len(self.run_history) > 100:
            self.run_history = self.run_history[-100:]
        
        # Update signal and trade history
        self.signal_history.extend(all_signals)
        if len(self.signal_history) > 1000:
            self.signal_history = self.signal_history[-1000:]
        
        self.trade_history.extend(all_results)
        if len(self.trade_history) > 1000:
            self.trade_history = self.trade_history[-1000:]
        
        # Log
        self._log_cycle(stats, all_signals, all_results)
        
        return stats
    
    def _log_cycle(self, stats: RunnerStats, signals: List[Signal],
                   results: List[TradeResult]):
        """Log cycle results to file."""
        log_file = self.log_path / f"runner_{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        log_entry = {
            'timestamp': stats.timestamp.isoformat(),
            'duration_ms': stats.cycle_duration_ms,
            'signals': len(signals),
            'trades': stats.trades_executed,
            'successful': stats.successful_trades,
            'by_strategy': stats.by_strategy,
            'paper_trading': self.paper_trading
        }
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def start(self, interval: float = 30):
        """Start continuous background operation."""
        if self._runner_thread and self._runner_thread.is_alive():
            print("Runner already running")
            return
        
        # Start data manager background refresh
        self.data_manager.start_background_refresh(interval=interval / 3)
        
        self._run_interval = interval
        self._stop_runner.clear()
        self._runner_thread = threading.Thread(
            target=self._run_loop,
            daemon=True
        )
        self._runner_thread.start()
        
        print(f"Strategy runner started (interval: {interval}s, paper_trading: {self.paper_trading})")
    
    def stop(self):
        """Stop background operation."""
        self._stop_runner.set()
        if self._runner_thread:
            self._runner_thread.join(timeout=5)
        
        self.data_manager.stop_background_refresh()
        print("Strategy runner stopped")
    
    def _run_loop(self):
        """Main runner loop."""
        while not self._stop_runner.is_set():
            try:
                stats = self.run_cycle()
                print(f"Cycle completed: {stats.signals_generated} signals, "
                      f"{stats.trades_executed} trades in {stats.cycle_duration_ms:.0f}ms")
            except Exception as e:
                print(f"Error in runner loop: {e}")
            
            self._stop_runner.wait(timeout=self._run_interval)
    
    def get_performance_summary(self) -> Dict:
        """Get overall performance summary."""
        total_trades = len(self.trade_history)
        successful = sum(1 for t in self.trade_history if t.success)
        
        # Calculate paper P&L
        paper_pnl = 0.0
        for result in self.trade_history:
            if result.success and result.filled_price:
                if result.trade.action == 'buy':
                    paper_pnl -= result.filled_price * result.filled_quantity
                else:
                    paper_pnl += result.filled_price * result.filled_quantity
        
        return {
            'paper_trading': self.paper_trading,
            'total_signals': len(self.signal_history),
            'total_trades': total_trades,
            'successful_trades': successful,
            'failed_trades': total_trades - successful,
            'success_rate': successful / total_trades if total_trades > 0 else 0,
            'paper_pnl': paper_pnl,
            'trades_today': self.trades_today,
            'max_daily_trades': self.max_daily_trades,
            'strategies_enabled': list(self.strategies.keys()),
            'run_cycles': len(self.run_history),
            'avg_cycle_duration_ms': (
                sum(r.cycle_duration_ms for r in self.run_history) / len(self.run_history)
                if self.run_history else 0
            )
        }
    
    def get_recent_signals(self, limit: int = 20) -> List[Dict]:
        """Get recent signals."""
        return [s.to_dict() for s in self.signal_history[-limit:]]
    
    def get_recent_trades(self, limit: int = 20) -> List[Dict]:
        """Get recent trades."""
        return [t.to_dict() for t in self.trade_history[-limit:]]


def create_default_runner(paper_trading: bool = True) -> StrategyRunner:
    """Create a runner with all strategies enabled using default settings."""
    runner = StrategyRunner(paper_trading=paper_trading)
    
    # Add all strategies
    runner.add_strategy('lead_lag', enabled=True, weight=1.0,
                       min_move_threshold=0.02, max_lag_seconds=300)
    runner.add_strategy('volume_spike', enabled=True, weight=0.8,
                       spike_threshold=2.0, lookback_minutes=60)
    runner.add_strategy('price_alerts', enabled=True, weight=0.6,
                       auto_detect_levels=True)
    runner.add_strategy('price_convergence', enabled=True, weight=1.2,
                       min_divergence=0.05)
    runner.add_strategy('momentum', enabled=True, weight=0.7,
                       lookback_minutes=15, min_momentum=0.03)
    # Arbitrage has highest weight - most reliable profits
    runner.add_strategy('arbitrage', enabled=True, weight=1.5,
                       min_net_profit=0.01, kalshi_fee_rate=0.10,
                       polymarket_gas_cost=0.02)
    
    return runner

