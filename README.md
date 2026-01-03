# Information Markets Trading Bot

An intelligent trading bot for prediction markets (Kalshi and Polymarket) with wallet tracking, Reddit sentiment analysis, and LLM-powered signal detection.

## Features

- **Multi-Platform Trading**: Support for Kalshi and Polymarket
- **Wallet Tracking**: Follow winning wallets, groups of wallets, and bet against losing wallets
- **EDA Tools**: Comprehensive exploratory data analysis for market and wallet performance
- **Reddit Integration**: Scrape and analyze Reddit posts and accounts for trading signals
- **LLM Analysis**: Use Ollama to summarize Reddit content and detect trading opportunities
- **Arbitrage Detection**: Find and exploit price differences between platforms

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp config.example.env .env
# Edit .env with your API keys and configuration
```

3. **Kalshi API Setup (using official SDK):**
   - Get your API key ID and RSA private key from: https://kalshi.com/account/profile
   - Set `KALSHI_API_KEY` to your API key ID
   - Set `KALSHI_PRIVATE_KEY_PATH` to the path of your downloaded private key (.pem file)
   - Or set `KALSHI_PRIVATE_KEY_PEM` with the private key content directly
   - The default API URL is already configured: `https://api.elections.kalshi.com/trade-api/v2`

3. Ensure Ollama is running locally:
```bash
ollama serve
# Pull a model: ollama pull llama3.2
```

## Project Structure

```
information_markets/
├── src/
│   ├── data_collectors/     # API clients for Kalshi and Polymarket
│   ├── wallet_tracker/      # Wallet tracking and analysis
│   ├── strategies/          # Trading strategies
│   ├── eda/                 # Exploratory data analysis tools
│   ├── reddit/              # Reddit scraping and analysis
│   ├── llm/                 # Ollama integration
│   └── bot/                 # Main bot orchestration
├── data/                    # Data storage
├── notebooks/               # Jupyter notebooks for EDA
└── tests/                   # Unit tests
```

## Usage

```python
from src.bot.main import TradingBot

bot = TradingBot()
bot.run()
```

## Strategies

1. **Follow Winning Wallets**: Track high-performing wallets and mirror their trades
2. **Follow Wallet Groups**: Identify correlated wallet groups and follow collective behavior
3. **Bet Against Losers**: Identify consistently losing wallets and take opposite positions
4. **Arbitrage**: Exploit price differences between Kalshi and Polymarket

## License

MIT
