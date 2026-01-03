# Quick Start Guide

## Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running locally
   - Download from: https://ollama.ai
   - Start Ollama: `ollama serve`
   - Pull a model: `ollama pull llama3.2` (or mistral, llama2, etc.)

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure API keys:**
```bash
cp config.example.env .env
# Edit .env with your API keys:
# - Kalshi: Get API key ID and RSA private key from https://kalshi.com/account/profile
#   Set KALSHI_API_KEY (your API key ID)
#   Set KALSHI_PRIVATE_KEY_PATH (path to your .pem file) OR KALSHI_PRIVATE_KEY_PEM (key content)
# - Polymarket: Get API credentials from https://polymarket.com/settings?tab=builder
#   Set POLYMARKET_API_KEY, POLYMARKET_API_SECRET, POLYMARKET_API_PASSPHRASE, POLYMARKET_PRIVATE_KEY
# - Reddit API credentials (client_id, client_secret)
```

3. **Get Reddit API credentials:**
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create App" or "Create Another App"
   - Choose "script" type
   - Copy the client ID and secret to your .env file

## Testing API Keys

**Important:** Before running the bot, verify your API keys work:

```bash
python test_api_keys.py
```

This will test:
- Kalshi API connection and authentication
- Polymarket API connection and authentication
- Arbitrage detector functionality

## Running Examples

### EDA Analysis
```bash
python examples/eda_example.py
```

### Reddit Analysis with Ollama
```bash
python examples/reddit_analysis_example.py
```

### Wallet Strategies
```bash
python examples/wallet_strategy_example.py
```

### Arbitrage Detection
```bash
python examples/arbitrage_example.py
```

## Running the Main Bot

```python
from src.bot.main import TradingBot

bot = TradingBot()

# Run with default settings (all strategies, 5-minute intervals)
bot.run()

# Or customize:
bot.run(
    interval_seconds=300,  # 5 minutes
    strategies=["arbitrage", "wallet"]  # Only run these strategies
)
```

## Key Features

### 1. Wallet Tracking
- Track wallet performance across platforms
- Identify winning and losing wallets
- Create wallet groups for collective analysis

### 2. Trading Strategies
- **Follow Winning Wallets**: Mirror trades from high-performing wallets
- **Follow Wallet Groups**: Trade based on consensus from wallet groups
- **Bet Against Losers**: Take opposite positions from consistently losing wallets

### 3. Reddit Analysis
- Scrape posts from relevant subreddits
- Use Ollama LLM to analyze sentiment and detect signals
- Analyze Reddit user credibility

### 4. Arbitrage Detection
- Find price differences between Kalshi and Polymarket
- Automatically detect profitable arbitrage opportunities

### 5. EDA Tools
- Comprehensive wallet performance analysis
- Pattern detection (best trading hours, days, markets)
- Visualization tools

## Data Storage

- Wallet data: `data/wallets.db` (SQLite database)
- Logs: `logs/` directory (if configured)
- Analysis outputs: `data/` directory

## Important Notes

⚠️ **Trading Risk**: This bot executes real trades. Always:
- Start with small position sizes
- Test strategies thoroughly before deploying
- Monitor performance closely
- Set appropriate risk limits

⚠️ **API Limits**: Be aware of rate limits for:
- Kalshi API
- Polymarket API
- Reddit API

⚠️ **Ollama**: Ensure Ollama is running before using LLM features. The bot will fail if Ollama is not accessible.

## Troubleshooting

### Ollama Connection Error
- Ensure Ollama is running: `ollama serve`
- Check OLLAMA_BASE_URL in .env (default: http://localhost:11434)
- Verify model is pulled: `ollama list`

### API Authentication Errors
- Verify API keys in .env file
- Check API key permissions
- Ensure keys are not expired

### Database Errors
- Ensure `data/` directory exists
- Check file permissions
- Database will be created automatically on first run

## Next Steps

1. Review example scripts in `examples/`
2. Explore EDA notebook: `notebooks/eda_notebook_template.ipynb`
3. Customize strategies in `src/strategies/`
4. Add your own wallet addresses to track
5. Configure risk parameters in `config.py`

