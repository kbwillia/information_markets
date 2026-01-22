# Strategy Visualization Dashboard

The visualization system provides comprehensive charts and graphs to track and analyze trading strategy performance.

**📖 For instructions on running with real data, see [RUNNING_WITH_REAL_DATA.md](RUNNING_WITH_REAL_DATA.md)**

## Features

The dashboard generates several types of visualizations:

1. **Performance Over Time** - Tracks signals, trades, success rate, and cycle duration over time
2. **Strategy Comparison** - Compares all strategies side-by-side on key metrics
3. **Signal Distribution** - Shows distribution of signals by strategy and strength
4. **Market Matching Statistics** - Visualizes the quality of market matching between platforms
5. **Arbitrage Opportunities** - Tracks arbitrage opportunities detected over time

## Usage

### Basic Usage

Generate all charts from log files:
```bash
python visualize_strategies.py
```

Generate charts for a specific time period:
```bash
python visualize_strategies.py --days 30
```

Generate a specific chart (creates separate file):
```bash
python visualize_strategies.py --chart performance --separate
python visualize_strategies.py --chart comparison --separate
```

Customize dashboard filename:
```bash
python visualize_strategies.py --dashboard-name my_dashboard.html
```

### Using with Active Runner

If you have a running strategy instance, you can visualize its current state:
```bash
python visualize_strategies.py --runner
```

### Programmatic Usage

```python
from src.visualization.dashboard import StrategyDashboard
from src.strategies.trading.runner import create_default_runner

# Create runner and run some cycles
runner = create_default_runner(paper_trading=True)
runner.run_cycle()

# Create dashboard
dashboard = StrategyDashboard(runner=runner)

# Generate all charts
dashboard.generate_all_charts()

# Or generate specific charts
dashboard.plot_performance_over_time(save=True)
dashboard.plot_strategy_comparison(save=True)
dashboard.plot_signal_distribution(save=True)
dashboard.plot_market_matching_stats(save=True)
dashboard.plot_arbitrage_opportunities(save=True)
```

## Chart Descriptions

### Performance Over Time
- **Signals Generated**: Number of trading signals generated per cycle
- **Trades Executed**: Number of trades executed per cycle
- **Success Rate**: Percentage of successful trades over time
- **Cycle Duration**: Time taken to run each strategy cycle

### Strategy Comparison
- **Total Signals**: Bar chart comparing signal generation across strategies
- **Total Trades**: Bar chart comparing trade execution across strategies
- **Success Rate**: Bar chart showing win rate for each strategy
- **Paper P&L**: Bar chart showing profit/loss for each strategy (paper trading)

### Signal Distribution
- **By Strategy**: Pie chart showing distribution of signals across strategies
- **By Strength**: Bar chart showing distribution of signal strengths (strong/moderate/weak)

### Market Matching Statistics
- **Similarity Score Distribution**: Histogram of similarity scores for matched markets
- **Text vs Semantic Similarity**: Scatter plot comparing text-based vs embedding-based similarity
- **End Date Matching**: Pie chart showing how many matches have close end dates
- **End Date Difference**: Histogram of days difference between matched market end dates

### Arbitrage Opportunities
- **Over Time**: Line chart showing arbitrage opportunities detected per day
- **By Type**: Bar chart showing distribution of arbitrage types (Dutch book vs price gap)

## Output Location

By default, all charts are combined into a **single interactive dashboard** saved to `data/visualizations/`:
- `trading_dashboard.html` - **Combined dashboard with all charts** (default)

The dashboard includes tabs for:
- **Performance Over Time** - Signals, trades, success rate, and cycle duration
- **Strategy Comparison** - Side-by-side comparison of all strategies
- **Signal Distribution** - Analysis of signals by strategy and strength
- **Market Matching Stats** - Market matching quality metrics
- **Arbitrage Opportunities** - Arbitrage detection over time

**Simply open `trading_dashboard.html` in your web browser** to view all charts in one place with:
- Tab navigation to switch between different views
- Zoom and pan capabilities
- Hover tooltips with detailed information
- Click to toggle data series
- Export options (PNG, SVG, etc.)
- Dark theme optimized for viewing

### Separate Files (Optional)

If you prefer separate files, use the `--separate` flag:
```bash
python visualize_strategies.py --separate
```

This will generate individual HTML files:
- `performance_over_time.html`
- `strategy_comparison.html`
- `signal_distribution.html`
- `market_matching_stats.html`
- `arbitrage_opportunities.html`

## Data Sources

The visualization system can pull data from:

1. **Active Runner**: If a `StrategyRunner` instance is provided, it uses in-memory data
2. **Log Files**: Reads from JSONL log files in `data/logs/runner/` and `data/logs/paper_trades/`
3. **Market Cache**: Reads market matching data from the `DataManager`

## Requirements

- plotly (for interactive HTML charts)
- pandas
- numpy

These are automatically installed when you install the project dependencies.

## Interactive Features

The HTML charts include:
- **Zoom & Pan**: Click and drag to zoom, double-click to reset
- **Hover Tooltips**: Hover over data points for detailed information
- **Toggle Series**: Click legend items to show/hide data series
- **Export**: Download charts as PNG, SVG, or HTML
- **Dark Theme**: Charts use a dark theme by default (configurable)

## Demo

To see the visualization system in action with sample data:

```bash
python demo_visualization.py
```

This will generate sample data and create all visualization charts.

