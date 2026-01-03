# Kalshi API - Quick Reference

## Available Endpoints

### Public Endpoints (No Auth)
1. **Exchange Status** - `get_exchange_status()`
   - Exchange active status, trading hours

2. **List Markets** - `get_markets(limit, cursor, ...)`
   - All available markets with prices, volumes, status

3. **Market Details** - `get_market(ticker)`
   - Full details for a specific market

4. **Orderbook** - `get_orderbook(ticker)`
   - Full bid/ask orderbook for YES and NO sides

5. **Market History** - `get_market_history(ticker, limit)`
   - Trade history (prices, volumes, timestamps)
   - **Note:** Aggregate data only, no wallet addresses

### Authenticated Endpoints (Requires API Key)
6. **Portfolio** - `get_portfolio()`
   - Your portfolio overview

7. **Balance** - `get_balance()`
   - Your account balance

8. **Positions** - `get_positions()`
   - Your current open positions with P&L

9. **Orders** - `get_orders(limit, cursor, status)`
   - Your order history

10. **Order Status** - `get_order_status(order_id)`
    - Details of a specific order

11. **Place Order** - `place_order(ticker, side, action, count, price, ...)`
    - Create a new order

12. **Cancel Order** - `cancel_order(order_id)`
    - Cancel an open order

## Key Data Available

✅ **Market Data:**
- Market list, details, prices
- Orderbooks (bids/asks)
- Trade history (aggregate)
- Market statistics

✅ **Your Trading Data:**
- Your orders
- Your positions
- Your P&L
- Your balance

❌ **NOT Available:**
- Individual wallet addresses
- Other users' trades/positions
- Wallet-to-wallet mapping

## For Wallet Tracking

**The Kalshi API does NOT expose wallet addresses.** 

To implement wallet tracking strategies, you can:

1. **Track Your Own Performance**
   - Use your order/position history
   - Analyze your win rate and patterns
   - Build strategies from your data

2. **Market-Level Analysis**
   - Analyze price movements
   - Track volume patterns
   - Identify market trends

3. **Alternative Data Sources**
   - Monitor blockchain (if applicable)
   - Scrape social media for shared addresses
   - Use private APIs if available

## Example Usage

```python
from src.data_collectors.kalshi_client import KalshiClient

client = KalshiClient()

# Get markets
markets = client.get_markets(limit=500)

# Analyze each market
for market in markets.get('markets', []):
    ticker = market.get('ticker')
    
    # Get orderbook
    orderbook = client.get_orderbook(ticker)
    
    # Get trade history
    history = client.get_market_history(ticker, limit=100)
    
    # Analyze for opportunities

# Track your own trades
my_orders = client.get_orders(limit=1000)
my_positions = client.get_positions()
my_balance = client.get_balance()
```

See `docs/KALSHI_API_ENDPOINTS.md` for detailed documentation.

