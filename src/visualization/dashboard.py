"""
Interactive Plotly Dashboard for Trading Strategies

Creates interactive HTML charts using Plotly.
"""
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np

from src.strategies.trading.runner import StrategyRunner, RunnerStats
from src.strategies.trading.base import Signal, TradeResult
from src.core.data_manager import DataManager, MatchedMarket


class StrategyDashboard:
    """Interactive dashboard for visualizing strategy performance using Plotly."""
    
    def __init__(self, runner: Optional[StrategyRunner] = None,
                 log_path: str = "data/logs/runner",
                 cache_path: str = "data/cache/market_cache.db"):
        self.runner = runner
        self.log_path = Path(log_path)
        self.cache_path = cache_path
        self.output_dir = Path("data/visualizations")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Color scheme
        self.colors = {
            'arbitrage': '#FF6B6B',
            'momentum': '#4ECDC4',
            'lead_lag': '#45B7D1',
            'volume_spike': '#FFA07A',
            'price_convergence': '#98D8C8',
            'price_alerts': '#F7DC6F',
            'default': '#95A5A6',
            'success': '#2ECC71',
            'failure': '#E74C3C',
            'neutral': '#95A5A6'
        }
        
        # Plotly template
        self.template = 'plotly_dark'
    
    def _create_empty_chart(self, title: str, message: str):
        """Create an empty chart with a message."""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref='paper', yref='paper',
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color='#95A5A6')
        )
        fig.update_layout(
            title=dict(text=title, font=dict(size=20)),
            template=self.template,
            height=400,
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False)
        )
        return fig
    
    def load_history_from_logs(self, days: int = 7) -> Dict:
        """Load historical data from log files."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        run_history = []
        signals = []
        trades = []
        
        # Load from JSONL files
        for log_file in sorted(self.log_path.glob("runner_*.jsonl")):
            try:
                file_date = datetime.strptime(log_file.stem.split('_')[1], '%Y%m%d').date()
                if file_date < cutoff_date.date():
                    continue
                
                with open(log_file, 'r') as f:
                    for line in f:
                        try:
                            entry = json.loads(line)
                            entry_time_str = entry.get('timestamp', '')
                            if entry_time_str:
                                entry_time = datetime.fromisoformat(entry_time_str.replace('Z', '+00:00'))
                                if entry_time >= cutoff_date:
                                    run_history.append(entry)
                        except (json.JSONDecodeError, KeyError, ValueError):
                            continue
            except (ValueError, FileNotFoundError):
                continue
        
        # Load paper trades
        paper_trade_path = Path("data/logs/paper_trades")
        if paper_trade_path.exists():
            for trade_file in sorted(paper_trade_path.glob("*.jsonl")):
                with open(trade_file, 'r') as f:
                    for line in f:
                        try:
                            trade = json.loads(line)
                            trade_time_str = (trade.get('timestamp') or 
                                            trade.get('trade', {}).get('signal', {}).get('timestamp') or
                                            trade.get('timestamp', ''))
                            if trade_time_str:
                                trade_time = datetime.fromisoformat(trade_time_str.replace('Z', '+00:00'))
                                if trade_time >= cutoff_date:
                                    trades.append(trade)
                        except (json.JSONDecodeError, KeyError, ValueError):
                            continue
        
        return {
            'run_history': run_history,
            'signals': signals,
            'trades': trades
        }
    
    def plot_performance_over_time(self, days: int = 7, save: bool = True):
        """Plot strategy performance metrics over time."""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Signals Generated Over Time', 'Trades Executed Over Time',
                           'Success Rate Over Time', 'Cycle Duration Over Time'),
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Load data
        if self.runner:
            history = self.runner.run_history
        else:
            data = self.load_history_from_logs(days)
            history = data['run_history']
        
        if not history:
            fig.add_annotation(
                text='No data available',
                xref='paper', yref='paper',
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            if save:
                output_file = self.output_dir / 'performance_over_time.html'
                fig.write_html(str(output_file))
                print(f"Saved performance chart to {output_file}")
            return fig
        
        # Convert to DataFrame
        if history and isinstance(history[0], RunnerStats):
            history_dicts = [{
                'timestamp': h.timestamp,
                'signals': h.signals_generated,
                'trades': h.trades_executed,
                'successful': h.successful_trades,
                'duration_ms': h.cycle_duration_ms
            } for h in history]
            df = pd.DataFrame(history_dicts)
        else:
            df = pd.DataFrame(history)
        
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
        
        # 1. Signals generated over time
        if 'signals' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df['timestamp'],
                    y=df['signals'],
                    mode='lines+markers',
                    name='Signals',
                    line=dict(color='#4ECDC4', width=2),
                    marker=dict(size=6)
                ),
                row=1, col=1
            )
        
        # 2. Trades executed over time
        if 'trades' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df['timestamp'],
                    y=df['trades'],
                    mode='lines+markers',
                    name='Trades',
                    line=dict(color='#2ECC71', width=2),
                    marker=dict(size=6)
                ),
                row=1, col=2
            )
        
        # 3. Success rate over time
        if 'successful' in df.columns and 'trades' in df.columns:
            df['success_rate'] = (df['successful'] / df['trades'] * 100).fillna(0)
            fig.add_trace(
                go.Scatter(
                    x=df['timestamp'],
                    y=df['success_rate'],
                    mode='lines+markers',
                    name='Success Rate',
                    line=dict(color='#F39C12', width=2),
                    marker=dict(size=6),
                    fill='tozeroy',
                    fillcolor='rgba(243, 156, 18, 0.2)'
                ),
                row=2, col=1
            )
            fig.add_hline(y=50, line_dash="dash", line_color="red", 
                         opacity=0.5, row=2, col=1)
        
        # 4. Cycle duration
        if 'duration_ms' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df['timestamp'],
                    y=df['duration_ms'],
                    mode='lines+markers',
                    name='Duration',
                    line=dict(color='#9B59B6', width=2),
                    marker=dict(size=6)
                ),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title=dict(text='Strategy Performance Over Time', font=dict(size=20)),
            template=self.template,
            height=800,
            showlegend=False
        )
        
        # Update axes
        fig.update_xaxes(title_text="Time", row=2, col=1)
        fig.update_xaxes(title_text="Time", row=2, col=2)
        fig.update_yaxes(title_text="Number of Signals", row=1, col=1)
        fig.update_yaxes(title_text="Number of Trades", row=1, col=2)
        fig.update_yaxes(title_text="Success Rate (%)", row=2, col=1, range=[0, 100])
        fig.update_yaxes(title_text="Duration (ms)", row=2, col=2)
        
        if save:
            output_file = self.output_dir / 'performance_over_time.html'
            fig.write_html(str(output_file))
            print(f"Saved performance chart to {output_file}")
        
        return fig
    
    def plot_strategy_comparison(self, save: bool = True):
        """Compare performance across different strategies."""
        if not self.runner:
            print("No runner available for strategy comparison")
            return None
        
        # Get stats from each strategy
        strategy_stats = {}
        for name, strategy in self.runner.strategies.items():
            stats = strategy.get_performance_stats()
            strategy_stats[name] = stats
        
        if not strategy_stats:
            print("No strategy data available")
            return None
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Total Signals Generated', 'Total Trades Executed',
                           'Success Rate by Strategy', 'Paper Trading P&L'),
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        strategies = list(strategy_stats.keys())
        colors_list = [self.colors.get(s, self.colors['default']) for s in strategies]
        
        # 1. Total signals
        signals = [strategy_stats[s]['total_signals'] for s in strategies]
        fig.add_trace(
            go.Bar(x=strategies, y=signals, name='Signals',
                  marker_color=colors_list, text=signals, textposition='auto'),
            row=1, col=1
        )
        
        # 2. Total trades
        trades = [strategy_stats[s]['total_trades'] for s in strategies]
        fig.add_trace(
            go.Bar(x=strategies, y=trades, name='Trades',
                  marker_color=colors_list, text=trades, textposition='auto'),
            row=1, col=2
        )
        
        # 3. Success rate
        success_rates = [strategy_stats[s]['success_rate'] * 100 for s in strategies]
        colors_success = [self.colors['success'] if sr >= 50 else self.colors['failure'] 
                         for sr in success_rates]
        fig.add_trace(
            go.Bar(x=strategies, y=success_rates, name='Success Rate',
                  marker_color=colors_success, text=[f'{sr:.1f}%' for sr in success_rates],
                  textposition='auto'),
            row=2, col=1
        )
        fig.add_hline(y=50, line_dash="dash", line_color="red", 
                     opacity=0.5, row=2, col=1)
        
        # 4. Paper P&L
        pnl = [strategy_stats[s]['paper_pnl'] for s in strategies]
        colors_pnl = [self.colors['success'] if p >= 0 else self.colors['failure'] 
                     for p in pnl]
        fig.add_trace(
            go.Bar(x=strategies, y=pnl, name='P&L',
                  marker_color=colors_pnl, text=[f'${p:.2f}' for p in pnl],
                  textposition='auto'),
            row=2, col=2
        )
        fig.add_hline(y=0, line_color="black", line_width=1, row=2, col=2)
        
        fig.update_layout(
            title=dict(text='Strategy Comparison', font=dict(size=20)),
            template=self.template,
            height=800,
            showlegend=False
        )
        
        fig.update_yaxes(title_text="Count", row=1, col=1)
        fig.update_yaxes(title_text="Count", row=1, col=2)
        fig.update_yaxes(title_text="Success Rate (%)", row=2, col=1, range=[0, 100])
        fig.update_yaxes(title_text="P&L ($)", row=2, col=2)
        
        if save:
            output_file = self.output_dir / 'strategy_comparison.html'
            fig.write_html(str(output_file))
            print(f"Saved strategy comparison to {output_file}")
        
        return fig
    
    def plot_signal_distribution(self, save: bool = True):
        """Plot distribution of signals by type and strength."""
        if not self.runner or not self.runner.signal_history:
            print("No signal data available")
            return None
        
        signals = self.runner.signal_history
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Signals by Strategy', 'Signals by Strength'),
            specs=[[{"type": "pie"}, {"type": "bar"}]]
        )
        
        # 1. Signals by strategy
        strategy_counts = defaultdict(int)
        for signal in signals:
            strategy_counts[signal.strategy_name] += 1
        
        strategies = list(strategy_counts.keys())
        counts = list(strategy_counts.values())
        colors_list = [self.colors.get(s, self.colors['default']) for s in strategies]
        
        fig.add_trace(
            go.Pie(labels=strategies, values=counts, name="Strategy",
                  marker_colors=colors_list),
            row=1, col=1
        )
        
        # 2. Signals by strength
        strength_counts = defaultdict(int)
        for signal in signals:
            strength_counts[signal.strength.value] += 1
        
        strengths = list(strength_counts.keys())
        strength_values = list(strength_counts.values())
        strength_colors = {
            'strong': '#2ECC71',
            'moderate': '#F39C12',
            'weak': '#E74C3C'
        }
        colors_strength = [strength_colors.get(s, self.colors['default']) for s in strengths]
        
        fig.add_trace(
            go.Bar(x=strengths, y=strength_values, name='Strength',
                  marker_color=colors_strength, text=strength_values,
                  textposition='auto'),
            row=1, col=2
        )
        
        fig.update_layout(
            title=dict(text='Signal Distribution Analysis', font=dict(size=20)),
            template=self.template,
            height=500,
            showlegend=False
        )
        
        fig.update_yaxes(title_text="Count", row=1, col=2)
        
        if save:
            output_file = self.output_dir / 'signal_distribution.html'
            fig.write_html(str(output_file))
            print(f"Saved signal distribution to {output_file}")
        
        return fig
    
    def plot_market_matching_stats(self, save: bool = True):
        """Visualize market matching statistics."""
        dm = DataManager()
        matched = dm.get_matched_markets()
        
        if not matched:
            print("No matched markets available")
            return None
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Similarity Score Distribution', 'Text vs Semantic Similarity',
                           'End Date Matching', 'End Date Difference Distribution'),
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # 1. Similarity score distribution
        scores = [m.similarity_score for m in matched]
        fig.add_trace(
            go.Histogram(x=scores, nbinsx=20, name='Similarity',
                        marker_color='#3498DB'),
            row=1, col=1
        )
        fig.add_vline(x=0.8, line_dash="dash", line_color="red", 
                     opacity=0.5, row=1, col=1)
        
        # 2. Text vs Semantic similarity
        text_sims = [m.text_similarity for m in matched]
        semantic_sims = [m.semantic_similarity for m in matched]
        fig.add_trace(
            go.Scatter(x=text_sims, y=semantic_sims, mode='markers',
                      name='Markets', marker=dict(size=8, opacity=0.6, color='#E74C3C')),
            row=1, col=2
        )
        # Add diagonal line
        fig.add_trace(
            go.Scatter(x=[0, 1], y=[0, 1], mode='lines',
                      line=dict(dash='dash', color='gray'), showlegend=False),
            row=1, col=2
        )
        
        # 3. End date matches
        date_matched = sum(1 for m in matched if m.end_date_match)
        date_not_matched = len(matched) - date_matched
        fig.add_trace(
            go.Pie(labels=['Date Matched', 'Date Not Matched'],
                  values=[date_matched, date_not_matched],
                  marker_colors=['#4ECDC4', '#FF6B6B']),
            row=2, col=1
        )
        
        # 4. End date difference distribution
        date_diffs = [m.end_date_diff_days for m in matched if m.end_date_diff_days is not None]
        if date_diffs:
            fig.add_trace(
                go.Histogram(x=date_diffs, nbinsx=20, name='Days Difference',
                            marker_color='#FF6B6B'),
                row=2, col=2
            )
            fig.add_vline(x=7, line_dash="dash", line_color="red", 
                         opacity=0.5, row=2, col=2)
        
        fig.update_layout(
            title=dict(text='Market Matching Statistics', font=dict(size=20)),
            template=self.template,
            height=800,
            showlegend=False
        )
        
        fig.update_xaxes(title_text="Similarity Score", row=1, col=1)
        fig.update_yaxes(title_text="Count", row=1, col=1)
        fig.update_xaxes(title_text="Text Similarity", row=1, col=2)
        fig.update_yaxes(title_text="Semantic Similarity", row=1, col=2)
        fig.update_xaxes(title_text="Days Difference", row=2, col=2)
        fig.update_yaxes(title_text="Count", row=2, col=2)
        
        if save:
            output_file = self.output_dir / 'market_matching_stats.html'
            fig.write_html(str(output_file))
            print(f"Saved market matching stats to {output_file}")
        
        return fig
    
    def plot_arbitrage_opportunities(self, save: bool = True):
        """Plot arbitrage opportunities detected over time."""
        if not self.runner:
            print("No runner available")
            return None
        
        # Filter arbitrage signals
        arb_signals = [s for s in self.runner.signal_history 
                      if s.strategy_name == 'arbitrage']
        
        if not arb_signals:
            print("No arbitrage signals found")
            return None
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Arbitrage Opportunities Over Time', 'Arbitrage Opportunities by Type'),
            vertical_spacing=0.15
        )
        
        # Group by date
        by_date = defaultdict(list)
        for signal in arb_signals:
            date_key = signal.timestamp.date()
            by_date[date_key].append(signal)
        
        dates = sorted(by_date.keys())
        counts = [len(by_date[d]) for d in dates]
        
        # 1. Over time
        fig.add_trace(
            go.Scatter(x=dates, y=counts, mode='lines+markers',
                      name='Opportunities', line=dict(color='#FF6B6B', width=3),
                      marker=dict(size=8), fill='tozeroy',
                      fillcolor='rgba(255, 107, 107, 0.3)'),
            row=1, col=1
        )
        
        # 2. By type
        arb_types = defaultdict(int)
        for signal in arb_signals:
            arb_type = signal.metadata.get('arb_type', 'unknown')
            arb_types[arb_type] += 1
        
        types = list(arb_types.keys())
        type_counts = list(arb_types.values())
        type_colors = {
            'dutch_book': '#FF6B6B',
            'price_gap': '#4ECDC4',
            'unknown': '#95A5A6'
        }
        colors_type = [type_colors.get(t, self.colors['default']) for t in types]
        
        fig.add_trace(
            go.Bar(x=types, y=type_counts, name='Type',
                  marker_color=colors_type, text=type_counts,
                  textposition='auto'),
            row=2, col=1
        )
        
        fig.update_layout(
            title=dict(text='Arbitrage Opportunities Analysis', font=dict(size=20)),
            template=self.template,
            height=700,
            showlegend=False
        )
        
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_yaxes(title_text="Number of Opportunities", row=1, col=1)
        fig.update_xaxes(title_text="Arbitrage Type", row=2, col=1)
        fig.update_yaxes(title_text="Count", row=2, col=1)
        
        if save:
            output_file = self.output_dir / 'arbitrage_opportunities.html'
            fig.write_html(str(output_file))
            print(f"Saved arbitrage analysis to {output_file}")
        
        return fig
    
    def plot_market_overview(self, save: bool = True):
        """Plot market overview statistics: number of events, active markets, etc."""
        # Get market data from DataManager
        try:
            data_manager = DataManager()
            kalshi_markets = data_manager.get_all_markets('kalshi')
            poly_markets = data_manager.get_all_markets('polymarket')
        except Exception as e:
            print(f"Error fetching market data: {e}")
            # Return empty chart with message
            return self._create_empty_chart("Market Overview", "Unable to fetch market data")
        
        if not kalshi_markets and not poly_markets:
            print("No market data available - markets may not be cached yet")
            return self._create_empty_chart("Market Overview", "No market data available. Run strategies to populate cache.")
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Active Markets by Platform', 'Markets by Status',
                           'Markets by Category', 'Market Status Distribution'),
            vertical_spacing=0.12,
            horizontal_spacing=0.1,
            specs=[[{"type": "bar"}, {"type": "pie"}],
                   [{"type": "bar"}, {"type": "pie"}]]
        )
        
        # 1. Active markets by platform
        kalshi_count = len(kalshi_markets) if kalshi_markets else 0
        poly_count = len(poly_markets) if poly_markets else 0
        
        fig.add_trace(
            go.Bar(x=['Kalshi', 'Polymarket'], y=[kalshi_count, poly_count],
                  marker_color=['#3498DB', '#9B59B6'], text=[kalshi_count, poly_count],
                  textposition='auto', name='Markets'),
            row=1, col=1
        )
        
        # 2. Markets by status (Kalshi)
        if kalshi_markets:
            status_counts = defaultdict(int)
            for m in kalshi_markets:
                status = getattr(m, 'status', 'unknown') or 'unknown'
                status_counts[status] += 1
            
            statuses = list(status_counts.keys())
            counts = list(status_counts.values())
            fig.add_trace(
                go.Pie(labels=statuses, values=counts, name='Kalshi Status',
                      marker_colors=px.colors.qualitative.Set3),
                row=1, col=2
            )
        
        # 3. Markets by category
        category_counts = defaultdict(int)
        for m in (kalshi_markets or []):
            cat = getattr(m, 'category', 'Uncategorized') or 'Uncategorized'
            category_counts[f"Kalshi: {cat}"] += 1
        for m in (poly_markets or []):
            cat = getattr(m, 'category', 'Uncategorized') or 'Uncategorized'
            category_counts[f"Poly: {cat}"] += 1
        
        if category_counts:
            # Get top 10 categories
            top_cats = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            cats = [c[0] for c in top_cats]
            cat_counts = [c[1] for c in top_cats]
            
            fig.add_trace(
                go.Bar(x=cats, y=cat_counts, marker_color='#E74C3C',
                      text=cat_counts, textposition='auto', name='Category'),
                row=2, col=1
            )
            fig.update_xaxes(tickangle=-45, row=2, col=1)
        
        # 4. Platform comparison pie
        total = kalshi_count + poly_count
        if total > 0:
            fig.add_trace(
                go.Pie(labels=['Kalshi', 'Polymarket'], 
                      values=[kalshi_count, poly_count],
                      marker_colors=['#3498DB', '#9B59B6'], name='Platform'),
                row=2, col=2
            )
        
        fig.update_layout(
            title=dict(text='Market Overview Statistics', font=dict(size=20)),
            template=self.template,
            height=800,
            showlegend=False
        )
        
        fig.update_xaxes(title_text="Platform", row=1, col=1)
        fig.update_yaxes(title_text="Number of Markets", row=1, col=1)
        fig.update_xaxes(title_text="Category", row=2, col=1)
        fig.update_yaxes(title_text="Number of Markets", row=2, col=1)
        
        if save:
            output_file = self.output_dir / 'market_overview.html'
            fig.write_html(str(output_file))
            print(f"Saved market overview to {output_file}")
        
        return fig
    
    def plot_volume_metrics(self, save: bool = True):
        """Plot volume metrics: total volume, volume trends, etc."""
        try:
            data_manager = DataManager()
            kalshi_markets = data_manager.get_all_markets('kalshi')
            poly_markets = data_manager.get_all_markets('polymarket')
        except Exception as e:
            print(f"Error fetching market data: {e}")
            return self._create_empty_chart("Volume Metrics", "Unable to fetch market data")
        
        if not kalshi_markets and not poly_markets:
            print("No market data available - markets may not be cached yet")
            return self._create_empty_chart("Volume Metrics", "No market data available. Run strategies to populate cache.")
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Total Volume by Platform', 'Volume Distribution',
                           'Top Markets by Volume', 'Volume vs Liquidity'),
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Collect volume data
        kalshi_volumes = []
        poly_volumes = []
        kalshi_liquidity = []
        poly_liquidity = []
        top_markets = []
        
        for m in (kalshi_markets or []):
            vol = getattr(m, 'volume', 0) or 0
            liq = getattr(m, 'liquidity', 0) or 0
            if vol > 0:
                kalshi_volumes.append(vol)
                kalshi_liquidity.append(liq)
                top_markets.append((getattr(m, 'title', 'Unknown')[:50], vol, 'Kalshi'))
        
        for m in (poly_markets or []):
            vol = getattr(m, 'volume', 0) or 0
            liq = getattr(m, 'liquidity', 0) or 0
            if vol > 0:
                poly_volumes.append(vol)
                poly_liquidity.append(liq)
                top_markets.append((getattr(m, 'title', 'Unknown')[:50], vol, 'Polymarket'))
        
        # 1. Total volume by platform
        kalshi_total = sum(kalshi_volumes) if kalshi_volumes else 0
        poly_total = sum(poly_volumes) if poly_volumes else 0
        
        fig.add_trace(
            go.Bar(x=['Kalshi', 'Polymarket'], y=[kalshi_total, poly_total],
                  marker_color=['#3498DB', '#9B59B6'], text=[f"{kalshi_total:,.0f}", f"{poly_total:,.0f}"],
                  textposition='auto', name='Volume'),
            row=1, col=1
        )
        
        # 2. Volume distribution (log scale histogram)
        all_volumes = kalshi_volumes + poly_volumes
        if all_volumes:
            # Use log scale for better visualization
            log_volumes = [np.log10(v) if v > 0 else 0 for v in all_volumes]
            fig.add_trace(
                go.Histogram(x=log_volumes, nbinsx=30, name='Volume (log10)',
                            marker_color='#E74C3C'),
                row=1, col=2
            )
        
        # 3. Top 10 markets by volume
        top_markets.sort(key=lambda x: x[1], reverse=True)
        top_10 = top_markets[:10]
        if top_10:
            titles = [m[0] for m in top_10]
            volumes = [m[1] for m in top_10]
            colors = ['#3498DB' if m[2] == 'Kalshi' else '#9B59B6' for m in top_10]
            
            fig.add_trace(
                go.Bar(x=titles, y=volumes, marker_color=colors,
                      text=[f"{v:,.0f}" for v in volumes], textposition='auto',
                      name='Volume'),
                row=2, col=1
            )
            fig.update_xaxes(tickangle=-45, row=2, col=1)
        
        # 4. Volume vs Liquidity scatter
        if kalshi_volumes and kalshi_liquidity:
            fig.add_trace(
                go.Scatter(x=kalshi_volumes, y=kalshi_liquidity, mode='markers',
                          name='Kalshi', marker=dict(size=8, color='#3498DB', opacity=0.6)),
                row=2, col=2
            )
        if poly_volumes and poly_liquidity:
            fig.add_trace(
                go.Scatter(x=poly_volumes, y=poly_liquidity, mode='markers',
                          name='Polymarket', marker=dict(size=8, color='#9B59B6', opacity=0.6)),
                row=2, col=2
            )
        
        fig.update_layout(
            title=dict(text='Volume Metrics Analysis', font=dict(size=20)),
            template=self.template,
            height=800,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Platform", row=1, col=1)
        fig.update_yaxes(title_text="Total Volume", row=1, col=1)
        fig.update_xaxes(title_text="Log10(Volume)", row=1, col=2)
        fig.update_yaxes(title_text="Count", row=1, col=2)
        fig.update_xaxes(title_text="Market", row=2, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        fig.update_xaxes(title_text="Volume", row=2, col=2, type="log")
        fig.update_yaxes(title_text="Liquidity", row=2, col=2, type="log")
        
        if save:
            output_file = self.output_dir / 'volume_metrics.html'
            fig.write_html(str(output_file))
            print(f"Saved volume metrics to {output_file}")
        
        return fig
    
    def plot_platform_comparison(self, save: bool = True):
        """Compare Kalshi vs Polymarket across multiple metrics."""
        try:
            data_manager = DataManager()
            kalshi_markets = data_manager.get_all_markets('kalshi')
            poly_markets = data_manager.get_all_markets('polymarket')
        except Exception as e:
            print(f"Error fetching market data: {e}")
            return self._create_empty_chart("Platform Comparison", "Unable to fetch market data")
        
        if not kalshi_markets and not poly_markets:
            print("No market data available - markets may not be cached yet")
            return self._create_empty_chart("Platform Comparison", "No market data available. Run strategies to populate cache.")
        
        # Calculate metrics
        kalshi_metrics = {
            'markets': len(kalshi_markets) if kalshi_markets else 0,
            'total_volume': sum(getattr(m, 'volume', 0) or 0 for m in (kalshi_markets or [])),
            'avg_volume': np.mean([getattr(m, 'volume', 0) or 0 for m in (kalshi_markets or []) if getattr(m, 'volume', 0)]) if kalshi_markets else 0,
            'total_liquidity': sum(getattr(m, 'liquidity', 0) or 0 for m in (kalshi_markets or [])),
            'active_markets': sum(1 for m in (kalshi_markets or []) if getattr(m, 'status', '') == 'open'),
            'categories': len(set(getattr(m, 'category', '') for m in (kalshi_markets or [])))
        }
        
        poly_metrics = {
            'markets': len(poly_markets) if poly_markets else 0,
            'total_volume': sum(getattr(m, 'volume', 0) or 0 for m in (poly_markets or [])),
            'avg_volume': np.mean([getattr(m, 'volume', 0) or 0 for m in (poly_markets or []) if getattr(m, 'volume', 0)]) if poly_markets else 0,
            'total_liquidity': sum(getattr(m, 'liquidity', 0) or 0 for m in (poly_markets or [])),
            'active_markets': sum(1 for m in (poly_markets or []) if getattr(m, 'status', '') == 'active'),
            'categories': len(set(getattr(m, 'category', '') for m in (poly_markets or [])))
        }
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Market Count Comparison', 'Volume Comparison',
                           'Liquidity Comparison', 'Active Markets'),
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # 1. Market count
        fig.add_trace(
            go.Bar(x=['Kalshi', 'Polymarket'], 
                  y=[kalshi_metrics['markets'], poly_metrics['markets']],
                  marker_color=['#3498DB', '#9B59B6'], name='Markets',
                  text=[kalshi_metrics['markets'], poly_metrics['markets']],
                  textposition='auto'),
            row=1, col=1
        )
        
        # 2. Volume comparison
        fig.add_trace(
            go.Bar(x=['Kalshi', 'Polymarket'],
                  y=[kalshi_metrics['total_volume'], poly_metrics['total_volume']],
                  marker_color=['#3498DB', '#9B59B6'], name='Total Volume',
                  text=[f"{kalshi_metrics['total_volume']:,.0f}", f"{poly_metrics['total_volume']:,.0f}"],
                  textposition='auto'),
            row=1, col=2
        )
        
        # 3. Liquidity comparison
        fig.add_trace(
            go.Bar(x=['Kalshi', 'Polymarket'],
                  y=[kalshi_metrics['total_liquidity'], poly_metrics['total_liquidity']],
                  marker_color=['#3498DB', '#9B59B6'], name='Liquidity',
                  text=[f"{kalshi_metrics['total_liquidity']:,.0f}", f"{poly_metrics['total_liquidity']:,.0f}"],
                  textposition='auto'),
            row=2, col=1
        )
        
        # 4. Active markets
        fig.add_trace(
            go.Bar(x=['Kalshi', 'Polymarket'],
                  y=[kalshi_metrics['active_markets'], poly_metrics['active_markets']],
                  marker_color=['#3498DB', '#9B59B6'], name='Active',
                  text=[kalshi_metrics['active_markets'], poly_metrics['active_markets']],
                  textposition='auto'),
            row=2, col=2
        )
        
        fig.update_layout(
            title=dict(text='Platform Comparison: Kalshi vs Polymarket', font=dict(size=20)),
            template=self.template,
            height=800,
            showlegend=False
        )
        
        fig.update_xaxes(title_text="Platform", row=1, col=1)
        fig.update_yaxes(title_text="Number of Markets", row=1, col=1)
        fig.update_xaxes(title_text="Platform", row=1, col=2)
        fig.update_yaxes(title_text="Total Volume", row=1, col=2)
        fig.update_xaxes(title_text="Platform", row=2, col=1)
        fig.update_yaxes(title_text="Total Liquidity", row=2, col=1)
        fig.update_xaxes(title_text="Platform", row=2, col=2)
        fig.update_yaxes(title_text="Active Markets", row=2, col=2)
        
        if save:
            output_file = self.output_dir / 'platform_comparison.html'
            fig.write_html(str(output_file))
            print(f"Saved platform comparison to {output_file}")
        
        return fig
    
    def generate_combined_dashboard(self, days: int = 7, filename: str = "trading_dashboard.html", save: bool = True):
        """Generate a single HTML dashboard with all charts combined."""
        print("Generating combined interactive dashboard...")
        
        charts = {}
        
        # Generate all charts (without saving individually)
        try:
            fig = self.plot_performance_over_time(days=days, save=False)
            if fig:
                charts['performance'] = fig
        except Exception as e:
            print(f"Error generating performance chart: {e}")
        
        try:
            fig = self.plot_strategy_comparison(save=False)
            if fig:
                charts['comparison'] = fig
        except Exception as e:
            print(f"Error generating strategy comparison: {e}")
        
        try:
            fig = self.plot_signal_distribution(save=False)
            if fig:
                charts['signals'] = fig
        except Exception as e:
            print(f"Error generating signal distribution: {e}")
        
        try:
            fig = self.plot_market_matching_stats(save=False)
            if fig:
                charts['matching'] = fig
        except Exception as e:
            print(f"Error generating market matching stats: {e}")
        
        try:
            fig = self.plot_arbitrage_opportunities(save=False)
            if fig:
                charts['arbitrage'] = fig
        except Exception as e:
            print(f"Error generating arbitrage chart: {e}")
        
        # Market statistics charts
        try:
            fig = self.plot_market_overview(save=False)
            if fig:
                charts['market_overview'] = fig
        except Exception as e:
            print(f"Error generating market overview: {e}")
        
        try:
            fig = self.plot_volume_metrics(save=False)
            if fig:
                charts['volume'] = fig
        except Exception as e:
            print(f"Error generating volume metrics: {e}")
        
        try:
            fig = self.plot_platform_comparison(save=False)
            if fig:
                charts['platform_comparison'] = fig
        except Exception as e:
            print(f"Error generating platform comparison: {e}")
        
        if not charts:
            print("No charts available to combine")
            return None
        
        # Create combined HTML
        html_content = self._create_dashboard_html(charts)
        
        if save:
            output_file = self.output_dir / filename
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"\nCombined dashboard saved to: {output_file}")
            print(f"Open {filename} in your browser to view all charts!")
        
        return html_content
    
    def _create_dashboard_html(self, charts: Dict) -> str:
        """Create a single HTML file with all charts using tabs."""
        chart_titles = {
            'performance': 'Performance Over Time',
            'comparison': 'Strategy Comparison',
            'signals': 'Signal Distribution',
            'matching': 'Market Matching Stats',
            'arbitrage': 'Arbitrage Opportunities',
            'market_overview': 'Market Overview',
            'volume': 'Volume Metrics',
            'platform_comparison': 'Platform Comparison'
        }
        
        chart_order = ['performance', 'comparison', 'signals', 'matching', 'arbitrage',
                      'market_overview', 'volume', 'platform_comparison']
        available_charts = [c for c in chart_order if c in charts]
        
        # Generate HTML for each chart
        chart_htmls = {}
        plotly_js_included = False
        
        for chart_name, fig in charts.items():
            # Generate full HTML for this chart
            full_html = fig.to_html(
                include_plotlyjs='cdn' if not plotly_js_included else False,
                div_id=f"chart-{chart_name}",
                config={'displayModeBar': True, 'responsive': True}
            )
            
            # Extract components
            import re
            # Get the div (may span multiple lines)
            div_pattern = r'<div[^>]*id="chart-[^"]*"[^>]*>.*?</div>\s*</div>'
            div_match = re.search(div_pattern, full_html, re.DOTALL)
            
            # Get all scripts
            script_pattern = r'<script[^>]*>.*?</script>'
            script_matches = re.findall(script_pattern, full_html, re.DOTALL)
            
            chart_div = div_match.group(0) if div_match else f'<div id="chart-{chart_name}"></div>'
            
            # Separate Plotly.js script from chart initialization scripts
            plotly_js_script = None
            chart_scripts = []
            
            for script in script_matches:
                if 'plotly' in script.lower() and ('src=' in script or 'cdn' in script.lower()):
                    if not plotly_js_included:
                        plotly_js_script = script
                        plotly_js_included = True
                elif 'Plotly.' in script or 'plotly' in script.lower():
                    chart_scripts.append(script)
            
            chart_htmls[chart_name] = {
                'div': chart_div,
                'scripts': chart_scripts,
                'plotly_js': plotly_js_script
            }
        
        # Create tab navigation
        tabs_html = '<div class="tabs">\n'
        for i, chart_name in enumerate(available_charts):
            active = 'active' if i == 0 else ''
            tabs_html += f'  <button class="tab-button {active}" onclick="showTab(\'{chart_name}\')">{chart_titles.get(chart_name, chart_name)}</button>\n'
        tabs_html += '</div>\n'
        
        # Create chart containers and collect scripts
        charts_html = ''
        all_chart_scripts = []
        plotly_js_script = None
        plotly_js_included = False
        
        for i, chart_name in enumerate(available_charts):
            display = 'block' if i == 0 else 'none'
            charts_html += f'<div id="tab-{chart_name}" class="tab-content" style="display: {display};">\n'
            
            if chart_name in chart_htmls and isinstance(chart_htmls[chart_name], dict):
                chart_data = chart_htmls[chart_name]
                charts_html += f'  {chart_data["div"]}\n'
                
                # Collect Plotly.js (only once)
                if chart_data.get('plotly_js') and not plotly_js_included:
                    plotly_js_script = chart_data['plotly_js']
                    plotly_js_included = True
                
                # Collect chart initialization scripts
                all_chart_scripts.extend(chart_data.get('scripts', []))
            else:
                charts_html += f'  <div id="chart-{chart_name}"></div>\n'
            
            charts_html += '</div>\n'
        
        # Combine all scripts
        scripts_html = ''
        if plotly_js_script:
            scripts_html += plotly_js_script + '\n'
        scripts_html += '\n'.join(all_chart_scripts)
        
        # Full HTML template
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trading Strategy Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #1e1e1e;
            color: #e0e0e0;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            color: white;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }}
        
        .tab-button {{
            padding: 12px 24px;
            background: #2d2d2d;
            border: 2px solid #444;
            color: #e0e0e0;
            cursor: pointer;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        
        .tab-button:hover {{
            background: #3d3d3d;
            border-color: #667eea;
        }}
        
        .tab-button.active {{
            background: #667eea;
            border-color: #667eea;
            color: white;
        }}
        
        .tab-content {{
            background: #2d2d2d;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            min-height: 600px;
        }}
        
        .tab-content > div {{
            width: 100%;
        }}
        
        @media (max-width: 768px) {{
            .tabs {{
                flex-direction: column;
            }}
            
            .tab-button {{
                width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Trading Strategy Dashboard</h1>
        <p>Interactive visualization of strategy performance and market analysis</p>
    </div>
    
    {tabs_html}
    
    {charts_html}
    
    <script>
        function showTab(tabName) {{
            // Hide all tabs
            const tabs = document.querySelectorAll('.tab-content');
            tabs.forEach(tab => {{
                tab.style.display = 'none';
            }});
            
            // Remove active class from all buttons
            const buttons = document.querySelectorAll('.tab-button');
            buttons.forEach(btn => {{
                btn.classList.remove('active');
            }});
            
            // Show selected tab
            document.getElementById('tab-' + tabName).style.display = 'block';
            
            // Add active class to clicked button
            event.target.classList.add('active');
            
            // Resize Plotly charts
            window.dispatchEvent(new Event('resize'));
        }}
        
        // Initialize first tab
        document.addEventListener('DOMContentLoaded', function() {{
            if (document.querySelectorAll('.tab-content').length > 0) {{
                const firstTab = document.querySelector('.tab-content');
                if (firstTab) {{
                    firstTab.style.display = 'block';
                }}
            }}
        }});
        
    </script>
    {scripts_html}
</body>
</html>"""
        
        return html_template
    
    def generate_all_charts(self, days: int = 7, combined: bool = True, filename: str = "trading_dashboard.html"):
        """Generate all available charts, optionally as a combined dashboard."""
        if combined:
            return self.generate_combined_dashboard(days=days, filename=filename, save=True)
        
        # Original behavior: generate separate files
        print("Generating interactive visualization dashboard...")
        
        charts = []
        
        try:
            fig = self.plot_performance_over_time(days=days, save=True)
            if fig:
                charts.append('performance_over_time')
        except Exception as e:
            print(f"Error generating performance chart: {e}")
        
        try:
            fig = self.plot_strategy_comparison(save=True)
            if fig:
                charts.append('strategy_comparison')
        except Exception as e:
            print(f"Error generating strategy comparison: {e}")
        
        try:
            fig = self.plot_signal_distribution(save=True)
            if fig:
                charts.append('signal_distribution')
        except Exception as e:
            print(f"Error generating signal distribution: {e}")
        
        try:
            fig = self.plot_market_matching_stats(save=True)
            if fig:
                charts.append('market_matching_stats')
        except Exception as e:
            print(f"Error generating market matching stats: {e}")
        
        try:
            fig = self.plot_arbitrage_opportunities(save=True)
            if fig:
                charts.append('arbitrage_opportunities')
        except Exception as e:
            print(f"Error generating arbitrage chart: {e}")
        
        print(f"\nGenerated {len(charts)} interactive charts:")
        for chart in charts:
            print(f"  - {chart}.html")
        print(f"\nCharts saved to: {self.output_dir}")
        print("Open the HTML files in your browser to view interactive charts!")
        
        return charts

