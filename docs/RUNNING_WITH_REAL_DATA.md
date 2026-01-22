# Running Dashboard with Real Data

To visualize real trading data, you need to first run your strategies to generate data, then visualize it.

**Quick Start for 7 Days of Data:**
1. Run strategies continuously: `python run_strategies.py --interval 30 --paper` (keep running for 7 days)
2. Visualize: `python visualize_strategies.py --days 7`

## Step 1: Run Strategies to Generate Data

First, run your trading strategies to collect real data. The strategies will log their activity to files that the dashboard can read.

### Run Once (Quick Test)

Run strategies once to generate some initial data:

```bash
python run_strategies.py --once --paper
```

This will:
- Run all strategies once
- Generate signals and trades
- Save data to log files in `data/logs/`

### Run Continuously (Production)

Run strategies continuously to collect ongoing data:

```bash
# Run every 30 seconds in paper trading mode
python run_strategies.py --interval 30 --paper

# Run every 60 seconds
python run_strategies.py --interval 60 --paper

# Run specific strategies only
python run_strategies.py --strategies arbitrage,momentum --interval 30 --paper
```

**Note:** Press `Ctrl+C` to stop the continuous run.

### Run with Real Trading (CAREFUL!)

If you want to use real money (not recommended for testing):

```bash
python run_strategies.py --interval 30 --real
```

⚠️ **Warning:** This uses real money! Make sure you understand the risks.

## Step 2: Visualize the Data

Once you have data from running strategies, visualize it:

### View Recent Data (Last 7 Days)

```bash
python visualize_strategies.py
```

This will:
- Load data from log files
- Generate a combined dashboard: `trading_dashboard.html`
- Show all charts with real data

### View More History

```bash
# Last 30 days
python visualize_strategies.py --days 30

# Last 90 days
python visualize_strategies.py --days 90
```

### With Active Runner

If you have a runner currently running, you can visualize its in-memory data:

```bash
python visualize_strategies.py --runner
```

This creates a runner instance and uses its current state (note: this creates a new runner, not the one you're running).

## Collecting 7 Days of Data

You have two options to get 7 days of data:

### Option A: Run Strategies on Historical Data (Recommended)

**Yes! Both Kalshi and Polymarket APIs provide historical data.** You can run your strategies on past market data and visualize immediately:

```bash
# Step 1: Run strategies on historical data (fetches data + runs strategies)
python scripts/run_strategies_on_history.py --days 7

# Step 2: Visualize the results
python visualize_strategies.py --days 7
```

This will:
- Fetch historical market data from APIs
- Run your actual strategies on that historical data (backtesting)
- Generate logs in the exact format the dashboard expects
- Save logs to `data/logs/runner/` (same format as live strategies)
- Allow immediate visualization in the dashboard

**Alternative: Just Fetch and Convert Data**

If you just want to fetch historical data without running strategies:

```bash
# Fetch and convert historical data to dashboard format
python scripts/fetch_historical_data.py --days 7

# Then visualize
python visualize_strategies.py --days 7
```

**Available Historical Data:**
- **Kalshi**: Market history, trade history, order history (your account)
- **Polymarket**: Price history (up to 15 days per call, or use 'max' interval), trade history, activity history

### Option B: Run Strategies Continuously

Alternatively, you can run strategies continuously for 7 days to collect data:

### Option 1: Run Continuously

Run strategies continuously and let them accumulate data over time:

```bash
# Run strategies every 30 seconds (adjust interval as needed)
python run_strategies.py --interval 30 --paper

# Keep this running for 7 days
# The strategies will automatically log data each day
```

**Tips for long-running sessions:**
- Use `screen` or `tmux` to keep it running if you disconnect:
  ```bash
  # Using screen
  screen -S trading
  python run_strategies.py --interval 30 --paper
  # Press Ctrl+A then D to detach
  # Reattach later with: screen -r trading
  ```

- Or run as a background process:
  ```bash
  nohup python run_strategies.py --interval 30 --paper > trading.log 2>&1 &
  ```

### Option 2: Run Periodically

If you can't run continuously, run strategies periodically throughout the week:

```bash
# Day 1
python run_strategies.py --once --paper

# Day 2 (next day)
python run_strategies.py --once --paper

# ... continue for 7 days
```

### Verify You Have 7 Days of Data

Check if you have log files for the last 7 days:

```bash
# Windows
dir data\logs\runner\
dir data\logs\paper_trades\

# Linux/Mac
ls -la data/logs/runner/
ls -la data/logs/paper_trades/
```

You should see files like:
- `runner_20250101.jsonl` (Day 1)
- `runner_20250102.jsonl` (Day 2)
- ... up to today

### View Your 7 Days of Data

Once you have 7 days of data:

```bash
# View last 7 days (default)
python visualize_strategies.py

# Or explicitly specify 7 days
python visualize_strategies.py --days 7
```

The dashboard will automatically load data from all log files within the last 7 days.

## Complete Workflow Example

Here's a typical workflow for collecting and viewing 7 days of data:

```bash
# Terminal 1: Run strategies continuously for a week
python run_strategies.py --interval 30 --paper

# After 7 days, or anytime during the week...

# Terminal 2: Generate dashboard with last 7 days
python visualize_strategies.py --days 7

# Open data/visualizations/trading_dashboard.html in your browser
```

## Data Storage

The strategies save data to:

- **Run history**: `data/logs/runner/runner_YYYYMMDD.jsonl`
- **Paper trades**: `data/logs/paper_trades/paper_trades_YYYYMMDD.jsonl`

The dashboard automatically reads from these files based on the `--days` parameter.

## Troubleshooting

### No Data Found

If you see "No data found in log files":

1. **Check if strategies have run:**
   ```bash
   ls data/logs/runner/
   ls data/logs/paper_trades/
   ```

2. **Run strategies first:**
   ```bash
   python run_strategies.py --once --paper
   ```

3. **Check the date range:**
   - Default is last 7 days
   - Use `--days` to increase the range
   - Make sure log files exist for that date range

### Empty Charts

If charts are empty or show "No data available":

- The strategies may not have generated any signals/trades yet
- Try running strategies for longer
- Check strategy parameters (they may be too conservative)

### Real-time Updates

The dashboard reads from log files, so:
- Run `visualize_strategies.py` again to refresh with new data
- Or use `--runner` flag to see current in-memory state (if you have a runner instance)

## Advanced Usage

### Custom Dashboard Name

```bash
python visualize_strategies.py --dashboard-name my_analysis.html
```

### Separate Files Instead of Combined Dashboard

```bash
python visualize_strategies.py --separate
```

This generates individual HTML files for each chart type.

### Specific Chart Only

```bash
python visualize_strategies.py --chart performance --separate
```

## Tips

1. **Use historical data fetching** - Don't wait 7 days! Use `scripts/fetch_historical_data.py` to get past data immediately
2. **Let strategies run for a while** before visualizing - you need data to see meaningful charts
3. **Use paper trading mode** (`--paper`) for testing - it's safer and still generates real data
4. **Check log files** if data seems missing - they should be in `data/logs/`
5. **Refresh dashboard regularly** - run `visualize_strategies.py` again to see latest data
6. **For 7 days of data**: Either fetch historical data OR run strategies continuously for a week
7. **Data accumulates automatically** - each day's run creates a new log file, and the dashboard combines them
8. **You can view partial data** - even if you only have 2-3 days, the dashboard will show what's available
9. **Historical data is stored separately** - fetched historical data goes to `data/historical/`, while strategy logs go to `data/logs/`

