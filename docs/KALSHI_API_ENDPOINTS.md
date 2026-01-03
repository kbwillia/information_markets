# Kalshi API Endpoints and Data Guide

## Overview

Kalshi provides a REST API for accessing market data, trading, and portfolio management. The API uses RSA-PSS signing for authentication.

**Base URL:** `https://api.elections.kalshi.com/trade-api/v2`

## Public Endpoints (No Authentication Required)

### 1. Exchange Status
**Endpoint:** `GET /exchange/status`

**Description:** Get exchange status and trading hours

**Returns:**
- `exchange_active` (bool): Whether exchange is active
- `trading_active` (bool): Whether trading is currently active
- `exchange_estimated_resume_time` (timestamp): When trading will resume (if paused)

**Example:**
```python
status = client.get_exchange_status()
# Returns: {'exchange_active': True, 'trading_active': True, ...}
```

---

### 2. List Markets
**Endpoint:** `GET /markets`

**Description:** Get list of available markets

**Parameters:**
- `limit` (int): Number of markets to return (default: 100)
- `cursor` (str): Pagination cursor for next page
- `status` (str): Filter by market status
- `series_ticker` (str): Filter by series
- `event_ticker` (str): Filter by event

**Returns:**
- List of market objects with:
  - `ticker` or `event_ticker`: Market identifier
  - `title`: Market question/title
  - `subtitle`: Additional context
  - `status`: Market status (open, closed, etc.)
  - `yes_bid`, `yes_ask`: Current yes prices
  - `no_bid`, `no_ask`: Current no prices
  - `volume`: Trading volume
  - `open_time`, `close_time`: Market timing
  - `category`: Market category
  - `series_ticker`: Series identifier

**Example:**
```python
markets = client.get_markets(limit=100)
# Returns: {'markets': [...], 'cursor': '...'}
```

---

### 3. Get Market Details
**Endpoint:** `GET /markets/{ticker}`

**Description:** Get detailed information about a specific market

**Returns:**
- Full market object with all details
- Current prices and orderbook summary
- Market rules and settlement information

**Example:**
```python
market = client.get_market("TICKER-123")
```

---

### 4. Get Orderbook
**Endpoint:** `GET /markets/{ticker}/orderbook`

**Description:** Get full orderbook (bids and asks) for a market

**Returns:**
- `yes`: Orderbook for YES side
  - `bids`: List of buy orders (price, size)
  - `asks`: List of sell orders (price, size)
- `no`: Orderbook for NO side
  - `bids`: List of buy orders
  - `asks`: List of sell orders

**Example:**
```python
orderbook = client.get_orderbook("TICKER-123")
# Returns: {'yes': {'bids': [...], 'asks': [...]}, 'no': {...}}
```

**Use Cases:**
- Calculate bid-ask spreads
- Find best prices for trading
- Analyze market depth
- Detect arbitrage opportunities

---

### 5. Get Market History/Trades
**Endpoint:** `GET /markets/{ticker}/history`

**Description:** Get trading history for a market

**Parameters:**
- `limit` (int): Number of trades to return

**Returns:**
- List of trade objects with:
  - `ts` (timestamp): Trade timestamp
  - `price`: Trade price
  - `yes_price`, `no_price`: Side prices
  - `count`: Number of contracts
  - `side`: "yes" or "no"
  - `action`: "buy" or "sell"

**Example:**
```python
history = client.get_market_history("TICKER-123", limit=100)
```

**Note:** This shows aggregate trades, NOT individual wallet addresses. Wallet addresses are not exposed in public APIs.

---

## Authenticated Endpoints (Requires API Key)

### 6. Get Portfolio
**Endpoint:** `GET /portfolio`

**Description:** Get your portfolio overview

**Returns:**
- Portfolio summary
- Total value
- Positions summary

**Example:**
```python
portfolio = client.get_portfolio()
```

---

### 7. Get Balance
**Endpoint:** `GET /portfolio/balance`

**Description:** Get your account balance

**Returns:**
- `balance` (int): Account balance in cents
- `portfolio_value` (int): Total portfolio value
- `updated_ts` (timestamp): Last update time

**Example:**
```python
balance = client.get_balance()
# Returns: {'balance': 0, 'portfolio_value': 0, 'updated_ts': 1767467498}
```

---

### 8. Get Positions
**Endpoint:** `GET /portfolio/positions`

**Description:** Get your current open positions

**Returns:**
- List of position objects with:
  - `ticker`: Market ticker
  - `position`: Number of contracts (positive = long, negative = short)
  - `entry_price`: Average entry price
  - `current_price`: Current market price
  - `unrealized_pnl`: Unrealized profit/loss

**Example:**
```python
positions = client.get_positions()
```

---

### 9. Get Orders
**Endpoint:** `GET /portfolio/orders`

**Description:** Get your order history

**Parameters:**
- `limit`: Number of orders to return
- `cursor`: Pagination cursor
- `status`: Filter by order status

**Returns:**
- List of order objects with:
  - `order_id`: Unique order identifier
  - `ticker`: Market ticker
  - `side`: "yes" or "no"
  - `action`: "buy" or "sell"
  - `count`: Number of contracts
  - `price`: Limit price (if limit order)
  - `status`: Order status (pending, filled, cancelled, etc.)
  - `ts`: Timestamp

**Example:**
```python
orders = client.get_orders(limit=100)
```

---

### 10. Place Order
**Endpoint:** `POST /portfolio/orders`

**Description:** Place a new order

**Parameters:**
- `ticker` (str): Market ticker
- `side` (str): "yes" or "no"
- `action` (str): "buy" or "sell"
- `count` (int): Number of contracts
- `price` (int, optional): Limit price in cents (0-100)
- `yes_price` (int, optional): Yes price for market orders
- `no_price` (int, optional): No price for market orders

**Returns:**
- Order confirmation with order_id

**Example:**
```python
order = client.place_order(
    ticker="TICKER-123",
    side="yes",
    action="buy",
    count=10,
    price=45  # 45 cents = $0.45
)
```

---

### 11. Get Order Status
**Endpoint:** `GET /portfolio/orders/{order_id}`

**Description:** Get status of a specific order

**Returns:**
- Full order details and current status

**Example:**
```python
order = client.get_order_status("order_123")
```

---

### 12. Cancel Order
**Endpoint:** `DELETE /portfolio/orders/{order_id}`

**Description:** Cancel an open order

**Returns:**
- Cancellation confirmation

**Example:**
```python
result = client.cancel_order("order_123")
```

---

## Key Data Points for Wallet Tracking

### What Data IS Available:
✅ Market prices and orderbooks  
✅ Aggregate trade history (prices, volumes, timestamps)  
✅ Your own orders and trades  
✅ Your own positions and P&L  
✅ Market statistics and volumes  

### What Data is NOT Available:
❌ Individual wallet addresses  
❌ Other users' orders or positions  
❌ Wallet-to-wallet transaction mapping  
❌ Individual user trading history  

## Limitations for Wallet Tracking

**Kalshi does NOT expose wallet addresses in their public API.** This means:

1. **You cannot track other users' wallets** through the API
2. **You can only track your own trading activity** (your orders, positions, P&L)
3. **To track other wallets, you would need:**
   - Blockchain monitoring (if Kalshi uses on-chain settlement)
   - Private/internal APIs (if available to partners)
   - Manual tracking of publicly shared wallet addresses
   - Social media/forum scraping to find wallet addresses

## Alternative Approaches

### 1. Track Your Own Performance
- Use authenticated endpoints to track your own trades
- Analyze your win rate, profit, and trading patterns
- Build strategies based on your historical performance

### 2. Market-Level Analysis
- Analyze market-level data (prices, volumes, orderbook depth)
- Track market trends and patterns
- Identify profitable market conditions

### 3. Social Signals
- Scrape Reddit, Twitter, Discord for wallet addresses
- Track wallets that users publicly share
- Follow influencers who share their trading activity

### 4. Blockchain Analysis (if applicable)
- If Kalshi settles on-chain, monitor blockchain transactions
- Extract wallet addresses from on-chain trades
- Build wallet tracking from blockchain data

## Example: What You Can Do

```python
from src.data_collectors.kalshi_client import KalshiClient

client = KalshiClient()

# Get all active markets
markets = client.get_markets(limit=500)

# Analyze each market
for market in markets['markets']:
    ticker = market['ticker']
    
    # Get orderbook
    orderbook = client.get_orderbook(ticker)
    
    # Get trade history
    history = client.get_market_history(ticker, limit=100)
    
    # Analyze for trading opportunities
    # (spread analysis, volume patterns, etc.)

# Track your own performance
portfolio = client.get_portfolio()
positions = client.get_positions()
orders = client.get_orders(limit=1000)

# Calculate your win rate and profit
# Build strategies based on your data
```

## Summary

The Kalshi API provides comprehensive market data and trading capabilities, but **does not expose individual wallet addresses**. For wallet tracking strategies, you'll need to:

1. Focus on your own trading performance
2. Use market-level analysis
3. Find alternative data sources (blockchain, social media)
4. Manually track wallets if addresses are shared publicly

