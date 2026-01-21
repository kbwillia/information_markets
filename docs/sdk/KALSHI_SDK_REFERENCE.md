# Kalshi SDK Complete Reference

This document contains a complete reference of all methods, classes, and APIs available in the `kalshi-python-sync` SDK.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Client Classes](#client-classes)
- [API Modules](#api-modules)
- [Models/Schemas](#modelsschemas)
- [Method Reference](#method-reference)

## Installation

```bash
pip install kalshi-python-sync
```

## Quick Start

```python
from kalshi_python_sync import Configuration, KalshiClient

# Configure
config = Configuration(host="https://api.elections.kalshi.com/trade-api/v2")
config.api_key_id = "your-api-key-id"
config.private_key_pem = "your-private-key-pem-content"

# Initialize client
client = KalshiClient(config)

# Use the client
markets = client.market_api.get_markets(limit=10)
```

## Configuration

### Configuration Class

The `Configuration` class is used to set up authentication and API settings.

**Attributes:**
- `host` (str): API base URL
- `api_key_id` (str): Your Kalshi API key ID
- `private_key_pem` (str): Your RSA private key content

## Client Classes

### KalshiClient

Main client class for interacting with the Kalshi API.

**API Modules:**
- `client.market_api` - Market operations
- `client.portfolio_api` - Portfolio operations  
- `client.exchange_api` - Exchange operations

## API Modules

### MarketApi

Methods for market-related operations.

**Methods:**
*(Run `python explore_kalshi_sdk.py` to generate complete list)*

### PortfolioApi

Methods for portfolio and account operations.

**Methods:**
*(Run `python explore_kalshi_sdk.py` to generate complete list)*

### ExchangeApi

Methods for exchange status and information.

**Methods:**
*(Run `python explore_kalshi_sdk.py` to generate complete list)*

## Models/Schemas

The SDK includes Pydantic models for request/response objects.

**Common Models:**
*(Run `python explore_kalshi_sdk.py` to generate complete list)*

## Method Reference

### MarketApi Methods

#### get_markets()

Get list of available markets.

**Parameters:**
- `limit` (int, optional): Number of markets to return
- `cursor` (str, optional): Pagination cursor
- `status` (str, optional): Filter by market status
- `series_ticker` (str, optional): Filter by series ticker
- `event_ticker` (str, optional): Filter by event ticker

**Returns:** `GetMarketsResponse` object

**Example:**
```python
response = client.market_api.get_markets(limit=100, status="open")
markets = response.markets
```

#### get_market(ticker)

Get details for a specific market.

**Parameters:**
- `ticker` (str): Market ticker symbol

**Returns:** `Market` object

**Example:**
```python
market = client.market_api.get_market("TICKER-2024-01-01")
```

#### get_orderbook(ticker)

Get orderbook for a market.

**Parameters:**
- `ticker` (str): Market ticker symbol

**Returns:** `Orderbook` object

**Example:**
```python
orderbook = client.market_api.get_orderbook("TICKER-2024-01-01")
```

#### get_market_history(ticker, limit)

Get trading history for a market.

**Parameters:**
- `ticker` (str): Market ticker symbol
- `limit` (int, optional): Number of history entries

**Returns:** `MarketHistoryResponse` object

**Example:**
```python
history = client.market_api.get_market_history("TICKER-2024-01-01", limit=100)
```

### PortfolioApi Methods

#### get_portfolio()

Get portfolio overview.

**Returns:** `Portfolio` object

**Example:**
```python
portfolio = client.portfolio_api.get_portfolio()
```

#### get_balance()

Get account balance.

**Returns:** `Balance` object

**Example:**
```python
balance = client.portfolio_api.get_balance()
```

#### get_positions()

Get current positions.

**Returns:** `PositionsResponse` object

**Example:**
```python
positions = client.portfolio_api.get_positions()
```

#### get_orders(limit, cursor, status)

Get order history.

**Parameters:**
- `limit` (int, optional): Number of orders
- `cursor` (str, optional): Pagination cursor
- `status` (str, optional): Filter by order status

**Returns:** `OrdersResponse` object

**Example:**
```python
orders = client.portfolio_api.get_orders(limit=100, status="filled")
```

#### create_order(...)

Place a new order.

**Parameters:**
- `ticker` (str): Market ticker
- `side` (str): "yes" or "no"
- `action` (str): "buy" or "sell"
- `count` (int): Number of contracts
- `price` (int, optional): Limit price in cents (0-100)
- `yes_price` (int, optional): Yes price for market orders
- `no_price` (int, optional): No price for market orders

**Returns:** `Order` object

**Example:**
```python
order = client.portfolio_api.create_order(
    ticker="TICKER-2024-01-01",
    side="yes",
    action="buy",
    count=10,
    price=50  # 50 cents = $0.50
)
```

#### cancel_order(order_id)

Cancel an order.

**Parameters:**
- `order_id` (str): Order ID

**Returns:** `CancelOrderResponse` object

**Example:**
```python
result = client.portfolio_api.cancel_order("order-123")
```

### ExchangeApi Methods

#### get_exchange_status()

Get exchange status.

**Returns:** `ExchangeStatus` object

**Example:**
```python
status = client.exchange_api.get_exchange_status()
```

## Generating Complete Documentation

To generate a complete list of all SDK methods and classes, run:

```bash
python explore_kalshi_sdk.py > docs/sdk/KALSHI_SDK_COMPLETE.txt
```

This will output all available methods, their signatures, and parameters.

## Additional Resources

- [Kalshi API Documentation](https://trade-api.kalshi.com/trade-api/documentation)
- [Kalshi Python SDK on PyPI](https://pypi.org/project/kalshi-python-sync/)
- [Kalshi GitHub Repository](https://github.com/Kalshi/kalshi-python-sync) (if available)

## Notes

- All timestamps are in Unix epoch format (seconds since 1970-01-01)
- Prices are in cents (0-100 range, where 100 = $1.00)
- The SDK uses Pydantic for request/response validation
- Date filtering parameters may not be supported - filter client-side if needed

