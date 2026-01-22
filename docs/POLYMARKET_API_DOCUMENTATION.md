# Polymarket API Documentation

> This document was automatically converted from the PDF documentation.
> Source: `docs/Polymarket API Documentation black and white.pdf`

---

Polymarket API Documentation
Developer Quickstart
Get started building with Polymarket APIs
Polymarket provides a suite of APIs and SDKs for building prediction market applications.
This guide will help you understand what’s available and where to find it.
What Can You Build?
If you want to… Start here
Fetch markets & prices Fetching Market Data
Place orders for yourself Placing Your First Order
Build a trading app for users Builders Program Introduction
Provide liquidity Market Makers
Fetching Market Data
Fetch Polymarket data in minutes with no authentication required
Get market data with zero setup. No API key, no authentication, no wallet required.
Understanding the Data Model
Before fetching data, understand how Polymarket structures its markets:
1 Event
The top-level object representing a question like “Will X happen?”
2 Market
Each event contains one or more markets. Each market is a specific tradable binary
outcome.
3 Outcomes & Prices
Markets have `outcomes` and `outcomePrices` arrays that map 1:1. These prices
represent implied probabilities.

{
"outcomes": "[\"Yes\", \"No\"]",
"outcomePrices": "[\"0.20\", \"0.80\"]"
}
// Index 0: "Yes" → 0.20 (20% probability)
// Index 1: "No" → 0.80 (80% probability)
Fetch Active Events

### List all currently active events on Polymarket

```bash
curl "https://gamma-api.polymarket.com/events?active=true&closed=false&limit=5"
Example Response:
[
{
"id": "123456",
"slug": "will-bitcoin-reach-100k-by-2025",
"title": "Will Bitcoin reach $100k by 2025?",
```
"active": true,
"closed": false,
"tags": [
{ "id": "21", "label": "Crypto", "slug": "crypto" }
],
"markets": [
{
"id": "789",
"question": "Will Bitcoin reach $100k by 2025?",
"clobTokenIds": ["TOKEN_YES_ID", "TOKEN_NO_ID"],
"outcomes": "[\"Yes\", \"No\"]",
"outcomePrices": "[\"0.65\", \"0.35\"]"
}
]
}
]
(!) Always use active=true&closed=false to filter for live, tradable events. (!)
Market Discovery Best Practices
For Sports Events
Use the /sports endpoint to discover leagues, then query by series_id :
# Get all supported sports leagues
```bash
curl "https://gamma-api.polymarket.com/sports"

# Get events for a specific league (e.g., NBA series_id=10345)
curl "https://gamma-api.polymarket.com/events?
series_id=10345&active=true&closed=false"
```
# Filter to just game bets (not futures) using tag_id=100639
```bash
curl "https://gamma-api.polymarket.com/events?
series_id=10345&tag_id=100639&active=true&closed=false&order=startTime&ascending=true"
```
(!) /sports only returns automated leagues. For others (UFC, Boxing, F1, Golf, Chess), use
tag IDs via /events?tag_id=<tag_id> . (!)
For Non-Sports Topics
Use /tags to discover all available categories, then filter events:
# Get all available tags
```bash
curl "https://gamma-api.polymarket.com/tags?limit=100"
# Query events by topic
curl "https://gamma-api.polymarket.com/events?tag_id=2&active=true&closed=false"
(!) Each event response includes a tags array, useful for discovering categories from live
```
data and building your own tag mapping. (!)
Get Market Details
Once you have an event, get details for a specific market using its ID or slug:
```bash
curl "https://gamma-api.polymarket.com/markets?slug=will-bitcoin-reach-100k-by-2025"
The response includes clobTokenIds , you’ll need these to fetch prices and place orders.
```
Get Market Details
Once you have an event, get details for a specific market using its ID or slug:
```bash
curl "https://gamma-api.polymarket.com/markets?slug=will-bitcoin-reach-100k-by-2025"
The response includes clobTokenIds , you’ll need these to fetch prices and place orders.
```
Get Current Price
Query the CLOB for the current price of any token:
```bash
curl "https://clob.polymarket.com/price?token_id=YOUR_TOKEN_ID&side=buy"

Example Response:
{
"price": "0.65"
}
Get Orderbook Depth
See all bids and asks for a market:
curl "https://clob.polymarket.com/book?token_id=YOUR_TOKEN_ID"
Example Response:
{
"market": "0x...",
"asset_id": "YOUR_TOKEN_ID",
"bids": [
{ "price": "0.64", "size": "500" },
{ "price": "0.63", "size": "1200" }
],
"asks": [
{ "price": "0.66", "size": "300" },
{ "price": "0.67", "size": "800" }
]
}
Placing Your First Order
Set up authentication and submit your first trade
This guide walks you through placing an order on Polymarket using your own wallet.
Installation
TypeScript
npm install @polymarket/clob-client ethers@5
Python
pip install py-clob-client
Step 1: Initialize Client with Private Key
TypeScript

import { ClobClient } from "@polymarket/clob-client";
import { Wallet } from "ethers"; // v5.8.0
const HOST = "https://clob.polymarket.com";
```
const CHAIN_ID = 137; // Polygon mainnet
const signer = new Wallet(process.env.PRIVATE_KEY);
const client = new ClobClient(HOST, CHAIN_ID, signer);
Python
```python
from py_clob_client.client import ClobClient
import os
host = "https://clob.polymarket.com"
chain_id = 137 # Polygon mainnet
private_key = os.getenv("PRIVATE_KEY")
client = ClobClient(host, key=private_key, chain_id=chain_id)
Step 2: Derive User API Credentials
Your private key is used once to derive API credentials. These credentials authenticate all
subsequent requests.
TypeScript
// Get existing API key, or create one if none exists
const userApiCreds = await client.createOrDeriveApiKey();
```
console.log("API Key:", userApiCreds.apiKey);
console.log("Secret:", userApiCreds.secret);
console.log("Passphrase:", userApiCreds.passphrase);
Python
# Get existing API key, or create one if none exists
user_api_creds = client.create_or_derive_api_creds()
print("API Key:", user_api_creds["apiKey"])
print("Secret:", user_api_creds["secret"])
print("Passphrase:", user_api_creds["passphrase"])
Step 3: Configure Signature Type and Funder
Before reinitializing the client, determine your signature type and funder address:

How do you want to trade? Type Value Funder
Address
I want to use an EOA wallet. It holds USDCe EOA 0 Your EOA
and position tokens, and I’ll pay my own gas. wallet address
I want to trade through my Polymarket.com POLY_PROXY 1 Your proxy
account (Magic Link email/Google login). wallet address
I want to trade through my Polymarket.com GNOSIS_SAFE 2 Your proxy
account (browser wallet connection). wallet address
(!) If you have a Polymarket.com account, your funds are in a proxy wallet (visible in the
profile dropdown). Use type 1 or 2. Type 0 is for standalone EOA wallets only. (!)
Step 4: Reinitialize with Full Authentication
TypeScript
// Choose based on your wallet type (see table above)
const SIGNATURE_TYPE = 0; // EOA example
const FUNDER_ADDRESS = signer.address; // For EOA, funder is your wallet
const client = new ClobClient(
HOST,

## Chain_Id,

signer,
userApiCreds,

## Signature_Type,


## Funder_Address

);
Python
# Choose based on your wallet type (see table above)
signature_type = 0 # EOA example
funder_address = "YOUR_WALLET_ADDRESS" # For EOA, funder is your wallet
client = ClobClient(
host,
key=private_key,
chain_id=chain_id,
creds=user_api_creds,
signature_type=signature_type,
funder=funder_address
)
(!) Do not use Builder API credentials in place of User API credentials! Builder
credentials are for order attribution, not user authentication. See Builder Order Attribution. (!)

Step 5: Place an Order
Now you’re ready to trade! First, get a token ID from the Gamma API.
TypeScript
```python
import { Side, OrderType } from "@polymarket/clob-client";
// Get market info first
const market = await client.getMarket("TOKEN_ID");
```
const response = await client.createAndPostOrder(
{
tokenID: "TOKEN_ID",
price: 0.50, // Price per share ($0.50)
size: 10, // Number of shares
side: Side.BUY, // BUY or SELL
},
{
tickSize: market.tickSize,
negRisk: market.negRisk, // true for multi-outcome events
},
OrderType.GTC // Good-Til-Cancelled
);
console.log("Order ID:", response.orderID);
console.log("Status:", response.status);
Python
```python
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY
# Get market info first
market = client.get_market("TOKEN_ID")
response = client.create_and_post_order(
OrderArgs(
token_id="TOKEN_ID",
price=0.50, # Price per share ($0.50)
```
size=10, # Number of shares
side=BUY, # BUY or SELL
),
options={
"tick_size": market["tickSize"],
"neg_risk": market["negRisk"], # True for multi-outcome events
},
order_type=OrderType.GTC # Good-Til-Cancelled
)

print("Order ID:", response["orderID"])
print("Status:", response["status"])
Step 6: Check Your Orders
TypeScript
// View all open orders
const openOrders = await client.getOpenOrders();
console.log(`You have ${openOrders.length} open orders`);
// View your trade history
const trades = await client.getTrades();
console.log(`You've made ${trades.length} trades`);
// Cancel an order
await client.cancelOrder(response.orderID);
Python
# View all open orders
open_orders = trading_client.get_open_orders()
print(f"You have {len(open_orders)} open orders")
# View your trade history
trades = trading_client.get_trades()
print(f"You've made {len(trades)} trades")
# Cancel an order
trading_client.cancel_order(response["orderID"])
Troubleshooting
1. Invalid Signature / L2 Auth Not Available
Wrong private key, signature type, or funder address for the derived User API
credentials.Double check the following values when creating User API credentials

### via createOrDeriveApiKey() 

Do not use Builder API credentials in place of User API credentials
Check signatureType matches your account type (0, 1, or 2)
Ensure funder is correct for your wallet type
2. Unauthorized / Invalid API Key
Wrong API key, secret, or passphrase.Re-derive credentials with createOrDeriveApiKey() and
update your config.
3. Not Enough Balance / Allowance

Either not enough USDCe / position tokens in your funder address, or you lack approvals to
spend your tokens.
Deposit USDCe to your funder address.
Ensure you have more USDCe than what’s committed in open orders.
Check that you’ve set all necessary token approvals.
4. Blocked by Cloudflare / Geoblock
You’re trying to place a trade from a restricted region.See Geographic Restrictions for
details.
Adding Builder API Credentials
If you’re building an app that routes orders for your users, you can add builder credentials to

### get attribution on the Builder Leaderboard

TypeScript
```python
import { BuilderConfig, BuilderApiKeyCreds } from "@polymarket/builder-signing-sdk";
const builderCreds: BuilderApiKeyCreds = {
key: process.env.POLY_BUILDER_API_KEY!,
```
secret: process.env.POLY_BUILDER_SECRET!,
passphrase: process.env.POLY_BUILDER_PASSPHRASE!,
};
const builderConfig = new BuilderConfig({ localBuilderCreds: builderCreds });
// Add builderConfig as the last parameter
const client = new ClobClient(
HOST,

## Chain_Id,

signer,
userApiCreds,
signatureType,
funderAddress,
undefined,
false,
builderConfig
);
Builder credentials are separate from user credentials. You use your builder credentials to
tag orders, but each user still needs their own L2 credentials to trade.
Full Builder Guide

Complete documentation for order attribution and gasless transactions
Glossary
Key terms and concepts for Polymarket developers
Markets & Events
Term Definition
Event A collection of related markets grouped under a common topic. Example:
“2024 US Presidential Election” contains markets for each candidate.
Market A single tradeable outcome within an event. Each market has a Yes and No
side. Corresponds to a condition ID, question ID, and pair of token IDs.
Token Represents a position in a specific outcome (Yes or No). Prices range from
0.00 to 1.00. Winning tokens redeem for $1 USDCe. Also called outcome
token or referenced by token ID.
Token ID The unique identifier for a specific outcome token. Required when placing
orders or querying prices.
Condition Onchain identifier for a market’s resolution condition. Used in CTF
ID operations.
Question Identifier linking a market to its resolution oracle (UMA).
ID
Slug Human-readable URL identifier for a market or event. Found in Polymarket
URLs: polymarket.com/event/[slug]
Trading
Term Definition
CLOB Central Limit Order Book. Polymarket’s off-chain order matching system.
Orders are matched here before onchain settlement.
Tick The minimum price increment for a market. Usually 0.01 (1 cent)
Size or 0.001 (0.1 cent).
Fill When an order is matched and executed. Orders can be partially or fully filled.
Order Types

Term Definition
GTC Good-Til-Cancelled. An order that remains open until filled or manually cancelled.
GTD Good-Til-Date. An order that expires at a specified time if not filled.
FOK Fill-Or-Kill. An order that must be filled entirely and immediately, or it’s cancelled.
No partial fills.
FAK Fill-And-Kill. An order that fills as much as possible immediately, then cancels any
remaining unfilled portion.
Market Types
Term Definition
Binary Market A market with exactly two outcomes: Yes and No. The prices always
sum to approximately $1.
Negative Risk A multi-outcome event where only one outcome can resolve Yes.
(NegRisk) Requires negRisk: true in order parameters. Details
Wallets
Term Definition
EOA Externally Owned Account. A standard Ethereum wallet controlled by a
private key.
Funder The wallet address that holds funds and tokens for trading.
Address
Signature Identifies wallet type when trading. 0 = EOA, 1 = Magic Link
Type proxy, 2 = Gnosis Safe proxy.
Token Operations (CTF)
Term Definition
CTF Conditional Token Framework. The onchain smart contracts that manage
outcome tokens.
Split Convert USDCe into a complete set of outcome tokens (one Yes + one No).

Term Definition
Merge Convert a complete set of outcome tokens back into USDCe.
Redeem After resolution, exchange winning tokens for $1 USDCe each.
Infrastructure
Term Definition
Polygon The blockchain network where Polymarket operates. Chain ID: 137 .
USDCe The stablecoin used as collateral on Polymarket. Bridged USDC on Polygon.
API Rate Limits
How Rate Limiting Works
All rate limits are enforced using Cloudflare’s throttling system. When you exceed the
maximum configured rate for any endpoint, requests are throttled rather than immediately

### rejected. This means

Throttling: Requests over the limit are delayed/queued rather than dropped
Burst Allowances: Some endpoints allow short bursts above the sustained rate
Time Windows: Limits reset based on sliding time windows (e.g., per 10 seconds, per
minute)
General Rate Limits
Endpoint Limit Notes
General Rate 15000 requests / Throttle requests over the maximum
Limiting 10s configured rate
”OK” Endpoint 100 requests / 10s Throttle requests over the maximum
configured rate
Data API Rate Limits
Endpoint Limit Notes
Data API (General) 1000 requests / Throttle requests over the maximum
10s configured rate
Data API /trades 200 requests / Throttle requests over the maximum
10s configured rate

Endpoint Limit Notes
Data API /positions 150 requests / Throttle requests over the maximum
10s configured rate
Data API /closed- 150 requests / Throttle requests over the maximum
positions 10s configured rate
Data API “OK” 100 requests / Throttle requests over the maximum
Endpoint 10s configured rate
GAMMA API Rate Limits
Endpoint Limit Notes
GAMMA (General) 4000 requests / Throttle requests over the maximum
10s configured rate
GAMMA Get Comments 200 requests / Throttle requests over the maximum
10s configured rate
GAMMA /events 500 requests / Throttle requests over the maximum
10s configured rate
GAMMA /markets 300 requests / Throttle requests over the maximum
10s configured rate
GAMMA /markets /events 900 requests / Throttle requests over the maximum
listing 10s configured rate
GAMMA Tags 200 requests / Throttle requests over the maximum
10s configured rate
GAMMA Search 350 requests / Throttle requests over the maximum
10s configured rate
CLOB API Rate Limits
General CLOB Endpoints
Endpoint Limit Notes
CLOB (General) 9000 requests / Throttle requests over the maximum
10s configured rate
CLOB GET Balance 200 requests / Throttle requests over the maximum
Allowance 10s configured rate
CLOB UPDATE Balance 50 requests / Throttle requests over the maximum
Allowance 10s configured rate
CLOB Market Data

Endpoint Limit Notes
CLOB /book 1500 requests / Throttle requests over the maximum configured
10s rate
CLOB /books 500 requests / 10s Throttle requests over the maximum configured
rate
CLOB /price 1500 requests / Throttle requests over the maximum configured
10s rate
CLOB /prices 500 requests / 10s Throttle requests over the maximum configured
rate
CLOB /midprice 1500 requests / Throttle requests over the maximum configured
10s rate
CLOB /midprices 500 requests / 10s Throttle requests over the maximum configured
rate
CLOB Ledger Endpoints
Endpoint Limit Notes
CLOB Ledger 900 Throttle requests over the
( /trades /orders /notifications /order ) requests / maximum configured rate
10s
CLOB Ledger /data/orders 500 Throttle requests over the
requests / maximum configured rate
10s
CLOB Ledger /data/trades 500 Throttle requests over the
requests / maximum configured rate
10s
CLOB /notifications 125 Throttle requests over the
requests / maximum configured rate
10s
CLOB Markets & Pricing
Endpoint Limit Notes
CLOB Price History 1000 requests / Throttle requests over the maximum
10s configured rate
CLOB Market Tick 200 requests / Throttle requests over the maximum
Size 10s configured rate
CLOB Authentication

Endpoint Limit Notes
CLOB API 100 requests / Throttle requests over the maximum configured
Keys 10s rate
CLOB Trading Endpoints
Endpoint Limit Notes
CLOB POST /order 3500 requests / 10s BURST - Throttle requests over the
(500/s) maximum configured rate
CLOB POST /order 36000 requests / 10 Throttle requests over the
minutes (60/s) maximum configured rate
CLOB DELETE /order 3000 requests / 10s BURST - Throttle requests over the
(300/s) maximum configured rate
CLOB DELETE /order 30000 requests / 10 Throttle requests over the
minutes (50/s) maximum configured rate
CLOB POST /orders 1000 requests / 10s BURST - Throttle requests over the
(100/s) maximum configured rate
CLOB POST /orders 15000 requests / 10 Throttle requests over the
minutes (25/s) maximum configured rate
CLOB DELETE /orders 1000 requests / 10s BURST - Throttle requests over the
(100/s) maximum configured rate
CLOB DELETE /orders 15000 requests / 10 Throttle requests over the
minutes (25/s) maximum configured rate
CLOB DELETE /cancel-all 250 requests / 10s BURST - Throttle requests over the
(25/s) maximum configured rate
CLOB DELETE /cancel-all 6000 requests / 10 Throttle requests over the
minutes (10/s) maximum configured rate
CLOB DELETE /cancel- 1000 requests / 10s BURST - Throttle requests over the
market-orders (100/s) maximum configured rate
CLOB DELETE /cancel- 1500 requests / 10 Throttle requests over the
market-orders minutes (25/s) maximum configured rate
Other API Rate Limits
Endpoint Limit Notes
RELAYER /submit 25 requests / 1 Throttle requests over the maximum
minute configured rate
User PNL API 200 requests / 10s Throttle requests over the maximum
configured rate

Endpoints
All Polymarket API URLs and base endpoints
All base URLs for Polymarket APIs. See individual API documentation for available routes
and parameters.
REST APIs
API Base URL Description
CLOB API https://clob.polymarket.com Order management, prices, orderbooks
Gamma API https://gamma-api.polymarket.com Market discovery, metadata, events
Data API https://data-api.polymarket.com User positions, activity, history
WebSocket Endpoints
Service URL Description
CLOB wss://ws-subscriptions- Orderbook updates, order
WebSocket clob.polymarket.com/ws/ status
RTDS wss://ws-live-data.polymarket.com Low-latency crypto prices,
comments
Quick Reference

## Clob Api

https://clob.polymarket.com

### Common endpoints

GET /price — Get current price for a token
GET /book — Get orderbook for a token
GET /midpoint — Get midpoint price
POST /order — Place an order (auth required)
DELETE /order — Cancel an order (auth required)

Full CLOB documentation →
Gamma API
https://gamma-api.polymarket.com

### Common endpoints

GET /events — List events
GET /markets — List markets
GET /events/{id} — Get event details
Full Gamma documentation →
Data API
https://data-api.polymarket.com

### Common endpoints

GET /positions — Get user positions
GET /activity — Get user activity
GET /trades — Get trade history
Full Data API documentation →
CLOB WebSocket
wss://ws-subscriptions-clob.polymarket.com/ws/

### Channels

market — Orderbook and price updates (public)
user — Order status updates (authenticated)
Full WebSocket documentation →
RTDS (Real-Time Data Stream)
wss://ws-live-data.polymarket.com

### Channels

Crypto price feeds
Comment streams
Full RTDS documentation →

Central Limit Order Book
CLOB Introduction
Welcome to the Polymarket Order Book API! This documentation provides overviews,
explanations, examples, and annotations to simplify interaction with the order book. The
following sections detail the Polymarket Order Book and the API usage.
System
Polymarket’s Order Book, or CLOB (Central Limit Order Book), is hybrid-decentralized. It
includes an operator for off-chain matching/ordering, with settlement executed on-chain,
non-custodially, via signed order messages.The exchange uses a custom Exchange contract
facilitating atomic swaps between binary Outcome Tokens (CTF ERC1155 assets and
ERC20 PToken assets) and collateral assets (ERC20), following signed limit orders.
Designed for binary markets, the contract enables complementary tokens to match across a
unified order book.Orders are EIP712-signed structured data. Matched orders have one
maker and one or more takers, with price improvements benefiting the taker. The operator
handles off-chain order management and submits matched trades to the blockchain for on-
chain execution.
API
The Polymarket Order Book API enables market makers and traders to programmatically
manage market orders. Orders of any amount can be created, listed, fetched, or read from
the market order books. Data includes all available markets, market prices, and order history
via REST and WebSocket endpoints.
Security
Polymarket’s Exchange contract has been audited by Chainsecurity (View Audit).The
operator’s privileges are limited to order matching, non-censorship, and ensuring correct
ordering. Operators can’t set prices or execute unauthorized trades. Users can cancel orders
on-chain independently if trust issues arise.
Fees
Schedule
Subject to change
Volume Level Maker Fee Base Rate (bps) Taker Fee Base Rate (bps)

## >0 Usdc 0 0

Overview

Fees apply symmetrically in output assets (proceeds). This symmetry ensures fairness and
market integrity. Fees are calculated differently depending on whether you are buying or

### selling

Selling outcome tokens (base) for collateral (quote):
feeQuote=baseRate×min( price,1−price)×sizefeeQuote=baseRate×min(price,1−price)×size
Buying outcome tokens (base) with collateral (quote):
feeBase=baseRate×min (price,1−price)×sizepricefeeBase=baseRate×min(price,1−price)×pric
e/size
Additional Resources
Exchange contract source code
Exchange contract documentation
Status

### Check the status of the Polymarket Order Book

Status Page
Quickstart
Initialize the CLOB and place your first order.
Installation
TypeScript
```bash
npm install @polymarket/clob-client ethers
Python
pip install py-clob-client
Quick Start
1. Setup Client
TypeScript
import { ClobClient } from "@polymarket/clob-client";
import { Wallet } from "ethers"; // v5.8.0
const HOST = "https://clob.polymarket.com";
```
const CHAIN_ID = 137; // Polygon mainnet

const signer = new Wallet(process.env.PRIVATE_KEY);
// Create or derive user API credentials
const tempClient = new ClobClient(HOST, CHAIN_ID, signer);
const apiCreds = await tempClient.createOrDeriveApiKey();
// See 'Signature Types' note below
const signatureType = 0;
// Initialize trading client
const client = new ClobClient(
HOST,

## Chain_Id,

signer,
apiCreds,
signatureType
);
Python
```python
from py_clob_client.client import ClobClient
import os
host = "https://clob.polymarket.com"
chain_id = 137 # Polygon mainnet
private_key = os.getenv("PRIVATE_KEY")
# Create or derive user API credentials
temp_client = ClobClient(host, key=private_key, chain_id=chain_id)
api_creds = await temp_client.create_or_derive_api_key()
# See 'Signature Types' note below
```
signature_type = 0
# Initialize trading client
client = ClobClient(
host,
key=private_key,
chain_id=chain_id,
creds=api_creds,
signature_type=signature_type
)
(!) This quick start sets your EOA as the trading account. You’ll need to fund this wallet to
trade and pay for gas on transactions. Gas-less transactions are only available by deploying
a proxy wallet and using Polymarket’s Polygon relayer infrastructure. (!)
Signature Types

Wallet Type ID When to Use
EOA 0 Standard Ethereum wallet (MetaMask)
Custom Proxy 1 Specific to Magic Link users from Polymarket only
Gnosis Safe 2 Injected providers (Metamask, Rabby, embedded wallets)
2. Place an Order
TypeScript
```python
import { Side } from "@polymarket/clob-client";
// Place a limit order in one step
const response = await client.createAndPostOrder({
tokenID: "YOUR_TOKEN_ID", // Get from Gamma API
price: 0.65, // Price per share
size: 10, // Number of shares
side: Side.BUY, // or SELL
});
```
console.log(`Order placed! ID: ${response.orderID}`);
Python
```python
from py_clob_client.clob_types import OrderArgs
from py_clob_client.order_builder.constants import BUY
# Place a limit order in one step
response = await client.create_and_post_order(
OrderArgs(
token_id="YOUR_TOKEN_ID", # Get from Gamma API
price=0.65, # Price per share
size=10, # Number of shares
side=BUY, # or SELL
)
)
print(f"Order placed! ID: {response['orderID']}")
```
3. Check Your Orders
TypeScript
// View all open orders
const openOrders = await client.getOpenOrders();
console.log(`You have ${openOrders.length} open orders`);
// View your trade history

const trades = await client.getTrades();
console.log(`You've made ${trades.length} trades`);
Python
# View all open orders
open_orders = await client.get_open_orders()
print(f"You have {len(open_orders)} open orders")
# View your trade history
trades = await client.get_trades()
print(f"You've made {len(trades)} trades")
Complete Example
TypeScript
```python
import { ClobClient, Side } from "@polymarket/clob-client";
import { Wallet } from "ethers";
async function trade() {
const HOST = "https://clob.polymarket.com";
```
const CHAIN_ID = 137; // Polygon mainnet
const signer = new Wallet(process.env.PRIVATE_KEY);
const tempClient = new ClobClient(HOST, CHAIN_ID, signer);
const apiCreds = await tempClient.createOrDeriveApiKey();
const signatureType = 0;
const client = new ClobClient(
HOST,

## Chain_Id,

signer,
apiCreds,
signatureType
);
const response = await client.createAndPostOrder({
tokenID: "YOUR_TOKEN_ID",
price: 0.65,
size: 10,
side: Side.BUY,
});
console.log(`Order placed! ID: ${response.orderID}`);
}
trade();

Python
```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs
from py_clob_client.order_builder.constants import BUY
import asyncio
import os
async def trade():
host = "https://clob.polymarket.com"
chain_id = 137 # Polygon mainnet
private_key = os.getenv("PRIVATE_KEY")
temp_client = ClobClient(host, key=private_key, chain_id=chain_id)
creds = await temp_client.create_or_derive_api_key()
signature_type=0
client = ClobClient(
host,
chain_id=chain_id,
key=private_key,
creds=creds,
signature_type=signature_type
)
response = await client.create_and_post_order(
OrderArgs(
token_id="YOUR_TOKEN_ID",
price=0.65,
size=10,
side=BUY
)
)
print(f"Order placed! ID: {response['orderID']}")
```

### if __name__ == "__main__"

asyncio.run(trade())
Troubleshooting
1. Error: L2_AUTH_NOT_AVAILABLE
You forgot to call createOrDeriveApiKey() . Make sure you initialize the client with API

### credentials

const creds = await clobClient.createOrDeriveApiKey();
const client = new ClobClient(host, chainId, wallet, creds);

2. Order rejected: insufficient balance

### Ensure you have

USDC in your funder address for BUY orders
Outcome tokens in your funder address for SELL orders
Check your balance at polymarket.com/portfolio.
3. Order rejected: insufficient allowance
You need to approve the Exchange contract to spend your tokens. This is typically done
through the Polymarket UI on your first trade. Or use the CTF
contract’s setApprovalForAll() method.
4. What's my funder address?
Your funder address is the Polymarket proxy wallet where you deposit funds. Find it:
1. Go to polymarket.com/settings
2. Look for “Wallet Address” or “Profile Address”
3. This is your FUNDER_ADDRESS
Authentication
Understanding authentication using Polymarket’s CLOB
The CLOB uses two levels of authentication: L1 (Private Key) and L2 (API Key). Either can
be accomplished using the CLOB client or REST API. Authentication is not required to
access client public methods and public endpoints.
L1 Authentication - Use the private key of the user’s account to sign messages
L2 Authentication - Use API credentials (key, secret, passphrase) to authenticate
requests to the CLOB
L1 Authentication
What is L1?
L1 authentication uses the wallet’s private key to sign an EIP-712 message used in the
request header. It proves ownership and control over the private key. The private key stays
in control of the user and all trading activity remains non-custodial.
What This Enables
Access to L1 methods that create or derive L2 authentication headers.

Create user API credentials
Derive existing user API credentials
Sign/create user’s orders locally
CLOB Client
TypeScript
```python
import { ClobClient } from "@polymarket/clob-client";
import { Wallet } from "ethers"; // v5.8.0
const HOST = "https://clob.polymarket.com";
```
const CHAIN_ID = 137; // Polygon mainnet
const signer = new Wallet(process.env.PRIVATE_KEY);
const client = new ClobClient(
HOST,

## Chain_Id,

signer // Signer enables L1 methods
);
// Gets API key, or else creates
const apiCreds = await client.createOrDeriveApiKey();
/*
apiCreds = {
"apiKey": "550e8400-e29b-41d4-a716-446655440000",
"secret": "base64EncodedSecretString",
"passphrase": "randomPassphraseString"
}
*/
Python
```python
from py_clob_client.client import ClobClient
import os
host = "https://clob.polymarket.com"
chain_id = 137 # Polygon mainnet
private_key = os.getenv("PRIVATE_KEY")
client = ClobClient(
host=host,
chain_id=chaind_id,
key=private_key # Signer enables L1 methods
)
# Gets API key, or else creates
api_creds = await client.create_or_derive_api_key()

# api_creds = {
# "apiKey": "550e8400-e29b-41d4-a716-446655440000",
# "secret": "base64EncodedSecretString",
# "passphrase": "randomPassphraseString"
# }
Never commit private keys to version control. Always use environment variables or
secure key management systems.
REST API
While we highly recommend using our provided clients to handle signing and authentication,
the following is for developers who choose NOT to use
our Python or TypeScript clients.When making direct REST API calls with L1 authentication,
include these headers:
Header Required? Description
```
POLY_ADDRESS yes Polygon signer address
POLY_SIGNATURE yes CLOB EIP 712 signature
POLY_TIMESTAMP yes Current UNIX timestamp
POLY_NONCE yes Nonce. Default 0
The POLY_SIGNATURE is generated by signing the following EIP-712 struct.
EIP-712 Signing Example
Typescript
const domain = {
name: "ClobAuthDomain",
version: "1",
chainId: chainId, // Polygon Chain ID 137
};
const types = {
ClobAuth: [
{ name: "address", type: "address" },
{ name: "timestamp", type: "string" },
{ name: "nonce", type: "uint256" },
{ name: "message", type: "string" },
],
};
const value = {
address: signingAddress, // The Signing address
timestamp: ts, // The CLOB API server timestamp
nonce: nonce, // The nonce used

message: "This message attests that I control the given wallet",
};
const sig = await signer._signTypedData(domain, types, value);
Python
domain = {
"name": "ClobAuthDomain",
"version": "1",
"chainId": chainId, # Polygon Chain ID 137
}
types = {
"ClobAuth": [
{"name": "address", "type": "address"},
{"name": "timestamp", "type": "string"},
{"name": "nonce", "type": "uint256"},
{"name": "message", "type": "string"},
]
}
value = {
"address": signingAddress, # The signing address
"timestamp": ts, # The CLOB API server timestamp
"nonce": nonce, # The nonce used
"message": "This message attests that I control the given wallet",
}
sig = await signer._signTypedData(domain, types, value)

### Reference implementations

TypeScript
Python
Create API Credentials
Create new API credentials for user.
POST {clob-endpoint}/auth/api-key
Derive API Credentials
Derive API credentials for user.
GET {clob-endpoint}/auth/derive-api-key

Response
{
"apiKey": "550e8400-e29b-41d4-a716-446655440000",
"secret": "base64EncodedSecretString",
"passphrase": "randomPassphraseString"
}
You’ll need all three values for L2 authentication.
L2 Authentication
What is L2?
The next level of authentication is called L2, and it consists of the user’s API credentials
(apiKey, secret, passphrase) generated from L1 authentication. These are used solely to
authenticate requests made to the CLOB API. Requests are signed using HMAC-SHA256.
What This Enables
Access to L2 methods such as posting signed/created orders, viewing open orders,
cancelling open orders, getting trades
Cancel or get user’s open orders
Check user’s balances and allowances
Post user’s signed orders
CLOB Client
TypeScript
```python
import { ClobClient } from "@polymarket/clob-client";
import { Wallet } from "ethers"; // v5.8.0
const HOST = "https://clob.polymarket.com";
```
const CHAIN_ID = 137; // Polygon mainnet
const signer = new Wallet(process.env.PRIVATE_KEY);
const client = new ClobClient(
HOST,

## Chain_Id,

signer,
apiCreds, // Generated from L1 auth, API credentials enable L2 methods
1, // signatureType explained below
FUNDER // funder explained below
);

// Now you can trade!*
const order = await client.createAndPostOrder(
{ tokenID: "123456", price: 0.65, size: 100, side: "BUY" },
{ tickSize: "0.01", negRisk: false }
);
Python
```python
from py_clob_client.client import ClobClient
import os
host = "https://clob.polymarket.com"
chain_id = 137 # Polygon mainnet
private_key = os.getenv("PRIVATE_KEY")
client = ClobClient(
host="https://clob.polymarket.com",
chain_id=137,
key=os.getenv("PRIVATE_KEY"),
creds=api_creds, # Generated from L1 auth, API credentials enable L2 methods
signature_type=1, # signatureType explained below
funder=os.getenv("FUNDER_ADDRESS") # funder explained below
)
# Now you can trade!*
```
order = await client.create_and_post_order(
{"token_id": "123456", "price": 0.65, "size": 100, "side": "BUY"},
{"tick_size": "0.01", "neg_risk": False}
)
(!) Even with L2 authentication headers, methods that create user orders still require the
user to sign the order payload. (!)

## Rest Api

While we highly recommend using our provided clients to handle signing and authentication,
the following is for developers who choose NOT to use
our Python or TypeScript clients.When making direct REST API calls with L2 authentication,

### include these headers

Header Required? Description
POLY_ADDRESS yes Polygon signer address
POLY_SIGNATURE yes HMAC signature for request
POLY_TIMESTAMP yes Current UNIX timestamp
POLY_API_KEY yes User’s API apiKey value
POLY_PASSPHRASE yes User’s API passphrase value

The POLY_SIGNATURE for L2 is an HMAC-SHA256 signature created using the user’s API
credentials secret value. Reference implementations can be found in
the Typescript and Python clients.
Signature Types and Funder
When initializing the L2 client, you must specify your wallet signatureType and

### the funder address which holds the funds

Signature Value Description
Type
EOA 0 Standard Ethereum wallet (MetaMask). Funder is the EOA
address and will need POL to pay gas on transactions.
POLY_PROXY 1 A custom proxy wallet only used with users who logged in via
Magic Link email/Google. Using this requires the user to have
exported their PK from Polymarket.com and imported into your
app.
GNOSIS_SAFE 2 Gnosis Safe multisig proxy wallet (most common). Use this for
any new or returning user who does not fit the other 2 types.
The wallet addresses displayed to the user on Polymarket.com is the proxy wallet and
should be used as the funder. These can be deterministically derived or you can deploy them
on behalf of the user. These proxy wallets are automatically deployed for the user on their
first login to Polymarket.com.
Troubleshooting
1. Error: INVALID_SIGNATURE
Your wallet’s private key is incorrect or improperly formatted.Solution:
Verify your private key is a valid hex string (starts with “0x”)
Ensure you’re using the correct key for the intended address
Check that the key has proper permissions
2. Error: NONCE_ALREADY_USED
The nonce you provided has already been used to create an API key.Solution:
Use deriveApiKey() with the same nonce to retrieve existing credentials
Or use a different nonce with createApiKey()
3. Error: Invalid Funder Address

Your funder address is incorrect or doesn’t match your wallet.Solution: Check your
Polymarket profile address at polymarket.com/settings.If it does not exist or user has never
logged into Polymarket.com, deploy it first before creating L2 authentication.
4. Lost API credentials but have nonce
// Use deriveApiKey with the original nonce
const recovered = await client.deriveApiKey(originalNonce);
5. Lost both credentials and nonce
Unfortunately, there’s no way to recover lost API credentials without the nonce. You’ll need to

### create new credentials

// Create fresh credentials with a new nonce
const newCreds = await client.createApiKey();
// Save the nonce this time!
Geographic Restrictions
Check geographic restrictions before placing orders on Polymarket’s CLOB
Overview
Polymarket restricts order placement from certain geographic locations due to regulatory
requirements and compliance with international sanctions. Before placing orders, builders
should verify the location.
Orders submitted from blocked regions will be rejected. Implement geoblock checks in your
application to provide users with appropriate feedback before they attempt to trade.
Server Infrastructure
Primary Servers: eu-west-2
Closest Non-Georestricted Region: eu-west-1
Geoblock Endpoint
Check the geographic eligibility of the requesting IP address:
GET https://polymarket.com/api/geoblock

Response
{
"blocked": boolean;
"ip": string;
"country": string;
"region": string;
}
Field Type Description
blocked boolean Whether the user is blocked from placing orders
ip string Detected IP address
country string ISO 3166-1 alpha-2 country code
region string Region/state code
Blocked Countries
The following 33 countries are completely restricted from placing orders on Polymarket:
Country Code Country Name
AU Australia
BE Belgium
BY Belarus
BI Burundi
CF Central African Republic
CD Congo (Kinshasa)
CU Cuba
DE Germany
ET Ethiopia
FR France
GB United Kingdom
IR Iran
IQ Iraq
IT Italy
KP North Korea
LB Lebanon

Country Code Country Name
LY Libya
MM Myanmar
NI Nicaragua
PL Poland
RU Russia
SG Singapore
SO Somalia
SS South Sudan
SD Sudan
SY Syria
TH Thailand
TW Taiwan
UM United States Minor Outlying Islands
US United States
VE Venezuela
YE Yemen
ZW Zimbabwe
Blocked Regions
In addition to fully blocked countries, the following specific regions within otherwise

### accessible countries are also restricted

Country Region Region Code
Canada (CA) Ontario ON
Ukraine (UA) Crimea 43
Ukraine (UA) Donetsk 14
Ukraine (UA) Luhansk 09
Usage Examples
TypeScript

interface GeoblockResponse {
blocked: boolean;
ip: string;
country: string;
region: string;
}
async function checkGeoblock(): Promise<GeoblockResponse> {
const response = await fetch("https://polymarket.com/api/geoblock");
return response.json();
}
// Usage
const geo = await checkGeoblock();
if (geo.blocked) {
console.log(`Trading not available in ${geo.country}`);
} else {
console.log("Trading available");
}
Python
```python
import requests
def check_geoblock() -> dict:
response = requests.get("https://polymarket.com/api/geoblock")
return response.json()
# Usage
geo = check_geoblock()
if geo["blocked"]:
print(f"Trading not available in {geo['country']}")
```

### else

print("Trading available")
Methods Overview
CLOB client methods require different levels of authentication. This reference is organized
by what credentials you need to call each method.
Public Methods
Access market data, orderbooks, and prices
L1 Methods
Private key authentication to create or derive API keys (L2 headers).

L2 Methods
Manage and close orders. Creating orders requires signer.[
Builder Program Methods
Builder-specific operations for those in the Builders Program.
Client Initialization by Use Case
Get Market Data
TypeScript
// No signer or credentials needed
const client = new ClobClient(
"https://clob.polymarket.com",
137
);
// All public methods available
const markets = await client.getMarkets();
const book = await client.getOrderBook(tokenId);
const price = await client.getPrice(tokenId, "BUY");
Python
# No signer or credentials needed
client = new ClobClient(
host="https://clob.polymarket.com",
chain_id=137
)
# All public methods available
markets = client.get_markets()
book = client.get_order_book()
price = client.get_price()
Generate User API Credentials
TypeScript
// Create client with signer
const client = new ClobClient(
"https://clob.polymarket.com",

137,
signer
);
// All public and L1 methods available
const newCreds = createApiKey();
const derivedCreds = deriveApiKey();
const creds = createOrDeriveApiKey();
Python
# Create client with signer
client = new ClobClient(
host="https://clob.polymarket.com",
chain_id=137
key="private_key"
)
# All public and L1 methods available
new_creds = client.create_api_key()
derived_creds = client.derive_api_key()
creds = client.create_or_derive_api_key()
Create and Post Order
TypeScript
// Create client with signer and creds
const client = new ClobClient(
"https://clob.polymarket.com",
137,
signer,
creds,
2, // Indicates Gnosis Safe proxy
funder // Safe wallet address holding funds
);
// All public, L1, and L2 methods available
const order = await client.createOrder({ /* ... */ });
const result = await client.postOrder(order);
const trades = await client.getTrades();
Python
# Create client with signer and creds
const client = new ClobClient(
host="https://clob.polymarket.com",
chain_id=137,
key="private_key",
creds=creds,

signature_type=2, // Indicates Gnosis Safe proxy
funder="funder_address" // Safe wallet address holding funds
)
# All public, L1, and L2 methods available
order = client.create_order({ /* ... */ })
result = client.post_order(order)
trades = client.get_trades()
Get Builders Orders
TypeScript
// Create client with builder's authentication headers
```python
import { BuilderConfig, BuilderApiKeyCreds } from "@polymarket/builder-signing-sdk";
const builderCreds: BuilderApiKeyCreds = {
key: process.env.POLY_BUILDER_API_KEY!,
```
secret: process.env.POLY_BUILDER_SECRET!,
passphrase: process.env.POLY_BUILDER_PASSPHRASE!
};
const builderConfig: BuilderConfig = {
localBuilderCreds: builderCreds
};
const client = new ClobClient(
"https://clob.polymarket.com",
137,
signer,
creds, // User's API credentials
2,
funder,
undefined,
false,
builderConfig // Builder's API credentials
);
// You can call all methods including builder methods
const builderTrades = await client.getBuilderTrades();
Python
# Create client with builder's authentication headers
```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds
from py_builder_signing_sdk.config import BuilderConfig, BuilderApiKeyCreds
builder_creds = BuilderApiKeyCreds(
key="POLY_BUILDER_API_KEY",
secret="POLY_BUILDER_SECRET,

passphrase="POLY_BUILDER_PASSPHRASE"
)
builder_config = BuilderConfig(
local_builder_creds=builder_creds
)
client = ClobClient(
host="https://clob.polymarket.com",
chain_id=137,
key="private_key",
creds=creds, # User's API credentials
```
signature_type=2,
funder=funder_address,
builder_config=builder_config # Builder's API credentials
)
# You can call all methods including builder methods
builder_trades = client.get_builder_trades()
Learn more about the Builders Program and Relay Client here
Resources
TypeScript Client
Open source TypeScript client on GitHub
Python Client
Open source Python client for GitHub[
TypeScript Examples
TypeScript client method examples[
Python Examples
Python client method examples[
CLOB Rest API Reference
Complete REST endpoint documentation[
Web Socket API
Real-time market data streaming
Public Methods

These methods can be called without a signer or user credentials. Use these for reading
market data, prices, and order books.
Client Initialization
Public methods require the client to initialize with the host URL and Polygon chain ID.
TypeScript
```python
import { ClobClient } from "@polymarket/clob-client";
const client = new ClobClient(
"https://clob.polymarket.com",
137
);
```
// Ready to call public methods
const markets = await client.getMarkets();
Python
```python
from py_clob_client.client import ClobClient
client = ClobClient(
host="https://clob.polymarket.com",
chain_id=137
)
# Ready to call public methods
markets = await client.get_markets()
Health Check
getOk()
Health check endpoint to verify the CLOB service is operational.
Signature
async getOk(): Promise<any>
Markets

getMarket()
Get details for a single market by condition ID.
Signature
async getMarket(conditionId: string): Promise<Market>
Response
interface MarketToken {
outcome: string;
```
price: number;
token_id: string;
winner: boolean;
}
interface Market {
accepting_order_timestamp: string | null;
accepting_orders: boolean;
active: boolean;
archived: boolean;
closed: boolean;
condition_id: string;
description: string;
enable_order_book: boolean;
end_date_iso: string;
fpmm: string;
game_start_time: string;
icon: string;
image: string;
is_50_50_outcome: boolean;
maker_base_fee: number;
market_slug: string;
minimum_order_size: number;
minimum_tick_size: number;
neg_risk: boolean;
neg_risk_market_id: string;
neg_risk_request_id: string;
notifications_enabled: boolean;
question: string;
question_id: string;
rewards: {
max_spread: number;
min_size: number;
rates: any | null;
};
seconds_delay: number;
tags: string[];

taker_base_fee: number;
tokens: MarketToken[];
}
getMarkets()
Get details for multiple markets paginated.
Signature
async getMarkets(): Promise<PaginationPayload>
Response
interface PaginationPayload {
limit: number;
count: number;
data: Market[];
}
interface Market {
accepting_order_timestamp: string | null;
accepting_orders: boolean;
active: boolean;
archived: boolean;
closed: boolean;
condition_id: string;
description: string;
enable_order_book: boolean;
end_date_iso: string;
fpmm: string;
game_start_time: string;
icon: string;
image: string;
is_50_50_outcome: boolean;
maker_base_fee: number;
market_slug: string;
minimum_order_size: number;
minimum_tick_size: number;
neg_risk: boolean;
neg_risk_market_id: string;
neg_risk_request_id: string;
notifications_enabled: boolean;
question: string;
question_id: string;
rewards: {
max_spread: number;
min_size: number;
rates: any | null;

};
seconds_delay: number;
tags: string[];
taker_base_fee: number;
tokens: MarketToken[];
}
interface MarketToken {
outcome: string;
price: number;
token_id: string;
winner: boolean;
}
getSimplifiedMarkets()
Get simplified market data paginated for faster loading.
Signature
async getSimplifiedMarkets(): Promise<PaginationPayload>
Response
interface PaginationPayload {
limit: number;
count: number;
data: SimplifiedMarket[];
}
interface SimplifiedMarket {
accepting_orders: boolean;
active: boolean;
archived: boolean;
closed: boolean;
condition_id: string;
rewards: {
rates: any | null;
min_size: number;
max_spread: number;
};
tokens: SimplifiedToken[];
}
interface SimplifiedToken {
outcome: string;
price: number;

token_id: string;
}
getSamplingMarkets()
Signature
async getSamplingMarkets(): Promise<PaginationPayload>
Response
interface PaginationPayload {
limit: number;
count: number;
data: Market[];
}
interface Market {
accepting_order_timestamp: string | null;
accepting_orders: boolean;
active: boolean;
archived: boolean;
closed: boolean;
condition_id: string;
description: string;
enable_order_book: boolean;
end_date_iso: string;
fpmm: string;
game_start_time: string;
icon: string;
image: string;
is_50_50_outcome: boolean;
maker_base_fee: number;
market_slug: string;
minimum_order_size: number;
minimum_tick_size: number;
neg_risk: boolean;
neg_risk_market_id: string;
neg_risk_request_id: string;
notifications_enabled: boolean;
question: string;
question_id: string;
rewards: {
max_spread: number;
min_size: number;
rates: any | null;
};
seconds_delay: number;

tags: string[];
taker_base_fee: number;
tokens: MarketToken[];
}
interface MarketToken {
outcome: string;
price: number;
token_id: string;
winner: boolean;
}
getSamplingSimplifiedMarkets()
Signature
async getSamplingSimplifiedMarkets(): Promise<PaginationPayload>
Response
interface PaginationPayload {
limit: number;
count: number;
data: SimplifiedMarket[];
}
interface SimplifiedMarket {
accepting_orders: boolean;
active: boolean;
archived: boolean;
closed: boolean;
condition_id: string;
rewards: {
rates: any | null;
min_size: number;
max_spread: number;
};
tokens: SimplifiedToken[];
}
interface SimplifiedToken {
outcome: string;
price: number;
token_id: string;
}

Order Books and Prices
calculateMarketPrice()
Signature
async calculateMarketPrice(
tokenID: string,
side: Side,
amount: number,
orderType: OrderType = OrderType.FOK
): Promise<number>
Params
enum OrderType {
GTC = "GTC", // Good Till Cancelled
FOK = "FOK", // Fill or Kill
GTD = "GTD", // Good Till Date
FAK = "FAK", // Fill and Kill
}
enum Side {

## Buy = "Buy",


## Sell = "Sell",

}
Response
number // calculated market price
getOrderBook()
Get the order book for a specific token ID.
Signature
async getOrderBook(tokenID: string): Promise<OrderBookSummary>
Response
interface OrderBookSummary {
market: string;
asset_id: string;

timestamp: string;
bids: OrderSummary[];
asks: OrderSummary[];
min_order_size: string;
tick_size: string;
neg_risk: boolean;
hash: string;
}
interface OrderSummary {
price: string;
size: string;
}
getOrderBooks()
Get order books for multiple token IDs.
Signature
async getOrderBooks(params: BookParams[]): Promise<OrderBookSummary[]>
Params
interface BookParams {
token_id: string;
side: Side; // Side.BUY or Side.SELL
}
Response
OrderBookSummary[]
getPrice()
Get the current best price for buying or selling a token ID.
Signature
async getPrice(
tokenID: string,
side: "BUY" | "SELL"
): Promise<any>

Response
{
price: string;
}
getPrices()
Get the current best prices for multiple token IDs.
Signature
async getPrices(params: BookParams[]): Promise<PricesResponse>
Params
interface BookParams {
token_id: string;
side: Side; // Side.BUY or Side.SELL
}
Response
interface TokenPrices {
BUY?: string;
SELL?: string;
}
type PricesResponse = {
[tokenId: string]: TokenPrices;
}
getMidpoint()
Get the midpoint price (average of best bid and best ask) for a token ID.
Signature
async getMidpoint(tokenID: string): Promise<any>
Response
{
mid: string;

}
getMidpoints()
Get the midpoint prices (average of best bid and best ask) for multiple token IDs.
Signature
async getMidpoints(params: BookParams[]): Promise<any>
Params
interface BookParams {
token_id: string;
side: Side; // Side is ignored
}
Response
{
[tokenId: string]: string;
}
getSpread()
Get the spread (difference between best ask and best bid) for a token ID.
Signature
async getSpread(tokenID: string): Promise<SpreadResponse>
Response
interface SpreadResponse {
spread: string;
}
getSpreads()
Get the spreads (difference between best ask and best bid) for multiple token IDs.

Signature
async getSpreads(params: BookParams[]): Promise<SpreadsResponse>
Params
interface BookParams {
token_id: string;
side: Side;
}
Response
type SpreadsResponse = {
[tokenId: string]: string;
}
getPricesHistory()
Get historical price data for a token.
Signature
async getPricesHistory(params: PriceHistoryFilterParams): Promise<MarketPrice[]>
Params
interface PriceHistoryFilterParams {
market: string; // tokenID
startTs?: number;
endTs?: number;
fidelity?: number;
interval: PriceHistoryInterval;
}
enum PriceHistoryInterval {
MAX = "max",
ONE_WEEK = "1w",
ONE_DAY = "1d",
SIX_HOURS = "6h",
ONE_HOUR = "1h",
}
Response

interface MarketPrice {
t: number; // timestamp
p: number; // price
}
Trades
getLastTradePrice()
Get the price of the most recent trade for a token.
Signature
async getLastTradePrice(tokenID: string): Promise<LastTradePrice>
Response
interface LastTradePrice {
price: string;
side: string;
}
getLastTradesPrices()
Get the price of the most recent trade for a token.
Signature
async getLastTradesPrices(params: BookParams[]): Promise<LastTradePriceWithToken[]>
Params
interface BookParams {
token_id: string;
side: Side;
}
Response
interface LastTradePriceWithToken {
price: string;

side: string;
token_id: string;
}
getMarketTradesEvents
Signature
async getMarketTradesEvents(conditionID: string): Promise<MarketTradeEvent[]>
Response
interface MarketTradeEvent {
event_type: string;
market: {
condition_id: string;
asset_id: string;
question: string;
icon: string;
slug: string;
};
user: {
address: string;
username: string;
profile_picture: string;
optimized_profile_picture: string;
pseudonym: string;
};
side: Side;
size: string;
fee_rate_bps: string;
price: string;
outcome: string;
outcome_index: number;
transaction_hash: string;
timestamp: string;
}
Market Parameters
getFeeRateBps()
Get the fee rate in basis points for a token.
Signature

async getFeeRateBps(tokenID: string): Promise<number>
Response
number
getTickSize()
Get the tick size (minimum price increment) for a market.
Signature
async getTickSize(tokenID: string): Promise<TickSize>
Response
type TickSize = "0.1" | "0.01" | "0.001" | "0.0001";
getNegRisk()
Check if a market uses negative risk (binary complementary tokens).
Signature
async getNegRisk(tokenID: string): Promise<boolean>
Response
boolean
Time & Server Info
getServerTime()
Get the current server timestamp.
Signature
async getServerTime(): Promise<number>

Response
number // Unix timestamp in seconds
L1 Methods
These methods require a wallet signer (private key) but do not require user API credentials.
Use these for initial setup.
Client Initialization
L1 methods require the client to initialize with a signer.
TypeScript
```python
import { ClobClient } from "@polymarket/clob-client";
import { Wallet } from "ethers";
const signer = new Wallet(process.env.PRIVATE_KEY);
```
const client = new ClobClient(
"https://clob.polymarket.com",
137,
signer // Signer required for L1 methods
);
// Ready to create user API credentials
const apiKey = await client.createApiKey();
Python
```python
from py_clob_client.client import ClobClient
import os
private_key = os.getenv("PRIVATE_KEY")
client = ClobClient(
host="https://clob.polymarket.com",
chain_id=137,
key=private_key # Signer required for L1 methods
)
# Ready to create user API credentials
api_key = await client.create_api_key()
(!) Security: Never commit private keys to version control. Always use environment
```
variables or secure key management systems. (!)

API Key Management
createApiKey()
Creates a new API key (L2 credentials) for the wallet signer. This generates a new set of
credentials that can be used for L2 authenticated requests. Each wallet can only have one
active API key at a time. Creating a new key invalidates the previous one.
Signature
async createApiKey(nonce?: number): Promise<ApiKeyCreds>
Params
`nonce` (optional): Custom nonce for deterministic key generation. If not provided, a
default derivation is used.
Response
interface ApiKeyCreds {
apiKey: string;
secret: string;
passphrase: string;
}
deriveApiKey()
Derives an existing API key (L2 credentials) using a specific nonce. If you’ve already created
API credentials with a particular nonce, this method will return the same credentials again.
Signature
async deriveApiKey(nonce?: number): Promise<ApiKeyCreds>
Params
`nonce` (optional): Custom nonce for deterministic key generation. If not provided, a
default derivation is used.
Response
interface ApiKeyCreds {
apiKey: string;

secret: string;
passphrase: string;
}
createOrDeriveApiKey()
Convenience method that attempts to derive an API key with the default nonce, or creates a
new one if it doesn’t exist. This is the recommended method for initial setup if you’re unsure
if credentials already exist.
Signature
async createOrDeriveApiKey(nonce?: number): Promise<ApiKeyCreds>
Params
`nonce` (optional): Custom nonce for deterministic key generation. If not provided, a
default derivation is used.
Response
interface ApiKeyCreds {
apiKey: string;
secret: string;
passphrase: string;
}
Order Signing
createOrder()
Create and sign a limit order locally without posting it to the CLOB. Use this when you want
to sign orders in advance or implement custom order submission logic. Place order via L2
methods postOrder or postOrders.
Signature
async createOrder(
userOrder: UserOrder,
options?: Partial<CreateOrderOptions>
): Promise<SignedOrder>
Params

interface UserOrder {
tokenID: string;
price: number;
size: number;
side: Side;
feeRateBps?: number;
nonce?: number;
expiration?: number;
taker?: string;
}
interface CreateOrderOptions {
tickSize: TickSize;
negRisk?: boolean;
}
Response
interface SignedOrder {
salt: string;
maker: string;
signer: string;
taker: string;
tokenId: string;
makerAmount: string;
takerAmount: string;
side: number; // 0 = BUY, 1 = SELL
expiration: string;
nonce: string;
feeRateBps: string;
signatureType: number;
signature: string;
}
createMarketOrder()
Create and sign a market order locally without posting it to the CLOB. Use this when you
want to sign orders in advance or implement custom order submission logic. Place orders
via L2 methods postOrder or postOrders.
Signature
async createMarketOrder(
userMarketOrder: UserMarketOrder,
options?: Partial<CreateOrderOptions>
): Promise<SignedOrder>

Params
interface UserMarketOrder {
tokenID: string;
amount: number; // BUY: dollar amount, SELL: number of shares
side: Side;
price?: number; // Optional price limit
feeRateBps?: number;
nonce?: number;
taker?: string;
orderType?: OrderType.FOK | OrderType.FAK;
}
Response
interface SignedOrder {
salt: string;
maker: string;
signer: string;
taker: string;
tokenId: string;
makerAmount: string;
takerAmount: string;
side: number; // 0 = BUY, 1 = SELL
expiration: string;
nonce: string;
feeRateBps: string;
signatureType: number;
signature: string;
}
Troubleshooting
1. Error: INVALID_SIGNATURE
Your wallet’s private key is incorrect or improperly formatted.Solution:
Verify your private key is a valid hex string (starts with “0x”)
Ensure you’re using the correct key for the intended address
Check that the key has proper permissions
2. Error: NONCE_ALREADY_USED
The nonce you provided has already been used to create an API key.Solution:
Use deriveApiKey() with the same nonce to retrieve existing credentials
Or use a different nonce with createApiKey()
3. Error: Invalid Funder Address

Your funder address is incorrect or doesn’t match your wallet.Solution: Check your
Polymarket profile address at polymarket.com/settings.If it does not exist or user has never
logged into Polymarket.com, deploy it first before creating L2 authentication.
4. Lost API credentials but have nonce
// Use deriveApiKey with the original nonce
const recovered = await client.deriveApiKey(originalNonce);
5. Lost both credentials and nonce
Unfortunately, there’s no way to recover lost API credentials without the nonce. You’ll need to

### create new credentials

// Create fresh credentials with a new nonce
const newCreds = await client.createApiKey();
// Save the nonce this time!
L2 Methods
These methods require user API credentials (L2 headers). Use these for placing trades and
managing user’s positions.
Client Initialization
L2 methods require the client to initialize with the signer, signatureType, user API
credentials, and funder.
TypeScript
```python
import { ClobClient } from "@polymarket/clob-client";
import { Wallet } from "ethers";
const signer = new Wallet(process.env.PRIVATE_KEY)
const apiCreds = {
apiKey: process.env.API_KEY,
secret: process.env.SECRET,
passphrase: process.env.PASSPHRASE,
};
```
const client = new ClobClient(
"https://clob.polymarket.com",
137,
signer,
apiCreds,
2, // Deployed Safe proxy wallet

process.env.FUNDER_ADDRESS // Address of deployed Safe proxy wallet
);
// Ready to send authenticated requests to the CLOB API!
const order = await client.postOrder(signedOrder);
Python
```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds
import os
api_creds = ApiCreds(
api_key=os.getenv("API_KEY"),
api_secret=os.getenv("SECRET"),
api_passphrase=os.getenv("PASSPHRASE")
)
client = ClobClient(
host="https://clob.polymarket.com",
chain_id=137,
key=os.getenv("PRIVATE_KEY"),
creds=api_creds,
signature_type=2, # Deployed Safe proxy wallet
funder=os.getenv("FUNDER_ADDRESS") # Address of deployed Safe proxy wallet
)
# Ready to send authenticated requests to the CLOB API!
```
order = await client.post_order(signed_order)
Order Creation and Management
createAndPostOrder()
A convenience method that creates, prompts signature, and posts an order in a single call.
Use when you want to buy/sell at a specific price and can wait.
Signature
async createAndPostOrder(
userOrder: UserOrder,
options?: Partial<CreateOrderOptions>,
orderType?: OrderType.GTC | OrderType.GTD, // Defaults to GTC
): Promise<OrderResponse>

Params
interface UserOrder {
tokenID: string;
price: number;
size: number;
side: Side;
feeRateBps?: number;
nonce?: number;
expiration?: number;
taker?: string;
}
type CreateOrderOptions = {
tickSize: TickSize;
negRisk?: boolean;
}
type TickSize = "0.1" | "0.01" | "0.001" | "0.0001";
Response
interface OrderResponse {
success: boolean;
errorMsg: string;
orderID: string;
transactionsHashes: string[];
status: string;
takingAmount: string;
makingAmount: string;
}
createAndPostMarketOrder()
A convenience method that creates, prompts signature, and posts an order in a single call.
Use when you want to buy/sell right now at whatever the market price is.
Signature
async createAndPostMarketOrder(
userMarketOrder: UserMarketOrder,
options?: Partial<CreateOrderOptions>,
orderType?: OrderType.FOK | OrderType.FAK, // Defaults to FOK
): Promise<OrderResponse>
Params

interface UserMarketOrder {
tokenID: string;
amount: number;
side: Side;
price?: number;
feeRateBps?: number;
nonce?: number;
taker?: string;
orderType?: OrderType.FOK | OrderType.FAK;
}
type CreateOrderOptions = {
tickSize: TickSize;
negRisk?: boolean;
}
type TickSize = "0.1" | "0.01" | "0.001" | "0.0001";
Response
interface OrderResponse {
success: boolean;
errorMsg: string;
orderID: string;
transactionsHashes: string[];
status: string;
takingAmount: string;
makingAmount: string;
}
postOrder()
Posts a pre-signed and created order to the CLOB.
Signature
async postOrder(
order: SignedOrder,
orderType?: OrderType, // Defaults to GTC
postOnly?: boolean, // Defaults to false
): Promise<OrderResponse>
Params
order: SignedOrder // Pre-signed order from createOrder() or createMarketOrder()
orderType?: OrderType // Optional, defaults to GTC
postOnly?: boolean // Optional, defaults to false

Response
interface OrderResponse {
success: boolean;
errorMsg: string;
orderID: string;
transactionsHashes: string[];
status: string;
takingAmount: string;
makingAmount: string;
}
postOrders()
Posts up to 15 pre-signed and created orders in a single batch.
async postOrders(
args: PostOrdersArgs[],
): Promise<OrderResponse[]>
Params
interface PostOrdersArgs {
order: SignedOrder;
orderType: OrderType;
postOnly?: boolean; // Defaults to false
}
Response
OrderResponse[] // Array of OrderResponse objects
interface OrderResponse {
success: boolean;
errorMsg: string;
orderID: string;
transactionsHashes: string[];
status: string;
takingAmount: string;
makingAmount: string;
}
cancelOrder()
Cancels a single open order.

Signature
async cancelOrder(orderID: string): Promise<CancelOrdersResponse>
Response
interface CancelOrdersResponse {
canceled: string[];
not_canceled: Record<string, any>;
}
cancelOrders()
Cancels multiple orders in a single batch.
Signature
async cancelOrders(orderIDs: string[]): Promise<CancelOrdersResponse>
Params
orderIDs: string[];
Response
interface CancelOrdersResponse {
canceled: string[];
not_canceled: Record<string, any>;
}
cancelAll()
Cancels all open orders.
Signature
async cancelAll(): Promise<CancelResponse>
Response
interface CancelOrdersResponse {
canceled: string[];

not_canceled: Record<string, any>;
}
cancelMarketOrders()
Cancels all open orders for a specific market.
Signature
async cancelMarketOrders(
payload: OrderMarketCancelParams
): Promise<CancelOrdersResponse>
Parameters
interface OrderMarketCancelParams {
market?: string;
asset_id?: string;
}
Response
interface CancelOrdersResponse {
canceled: string[];
not_canceled: Record<string, any>;
}
Order and Trade Queries
getOrder()
Get details for a specific order.
Signature
async getOrder(orderID: string): Promise<OpenOrder>
Response
interface OpenOrder {
id: string;
status: string;

owner: string;
maker_address: string;
market: string;
asset_id: string;
side: string;
original_size: string;
size_matched: string;
price: string;
associate_trades: string[];
outcome: string;
created_at: number;
expiration: string;
order_type: string;
}
getOpenOrders()
Get all your open orders.
Signature
async getOpenOrders(
params?: OpenOrderParams,
only_first_page?: boolean,
): Promise<OpenOrdersResponse>
Params
interface OpenOrderParams {
id?: string; // Order ID
market?: string; // Market condition ID
asset_id?: string; // Token ID
}
only_first_page?: boolean // Defaults to false
Response
type OpenOrdersResponse = OpenOrder[];
interface OpenOrder {
id: string;
status: string;
owner: string;
maker_address: string;
market: string;
asset_id: string;
side: string;

original_size: string;
size_matched: string;
price: string;
associate_trades: string[];
outcome: string;
created_at: number;
expiration: string;
order_type: string;
}
getTrades()
Get your trade history (filled orders).
Signature
async getTrades(
params?: TradeParams,
only_first_page?: boolean,
): Promise<Trade[]>
Params
interface TradeParams {
id?: string;
maker_address?: string;
market?: string;
asset_id?: string;
before?: string;
after?: string;
}
only_first_page?: boolean // Defaults to false
Response
interface Trade {
id: string;
taker_order_id: string;
market: string;
asset_id: string;
side: Side;
size: string;
fee_rate_bps: string;
price: string;
status: string;
match_time: string;
last_update: string;

outcome: string;
bucket_index: number;
owner: string;
maker_address: string;
maker_orders: MakerOrder[];
transaction_hash: string;
trader_side: "TAKER" | "MAKER";
}
interface MakerOrder {
order_id: string;
owner: string;
maker_address: string;
matched_amount: string;
price: string;
fee_rate_bps: string;
asset_id: string;
outcome: string;
side: Side;
}
getTradesPaginated()
Get trade history with pagination for large result sets.
Signature
async getTradesPaginated(
params?: TradeParams,
): Promise<TradesPaginatedResponse>
Params
interface TradeParams {
id?: string;
maker_address?: string;
market?: string;
asset_id?: string;
before?: string;
after?: string;
}
Response
interface TradesPaginatedResponse {
trades: Trade[];
limit: number;

count: number;
}
Balance and Allowances
getBalanceAllowance()
Get your balance and allowance for specific tokens.
Signature
async getBalanceAllowance(
params?: BalanceAllowanceParams
): Promise<BalanceAllowanceResponse>
Params
interface BalanceAllowanceParams {
asset_type: AssetType;
token_id?: string;
}
enum AssetType {

## Collateral = "Collateral",


## Conditional = "Conditional",

}
Response
interface BalanceAllowanceResponse {
balance: string;
allowance: string;
}
updateBalanceAllowance()
Updates the cached balance and allowance for specific tokens.
Signature
async updateBalanceAllowance(
params?: BalanceAllowanceParams

): Promise<void>
Params
interface BalanceAllowanceParams {
asset_type: AssetType;
token_id?: string;
}
enum AssetType {

## Collateral = "Collateral",


## Conditional = "Conditional",

}
API Key Management (L2)
getApiKeys()
Get all API keys associated with your account.
Signature
async getApiKeys(): Promise<ApiKeysResponse>
Response
interface ApiKeysResponse {
apiKeys: ApiKeyCreds[];
}
interface ApiKeyCreds {
key: string;
secret: string;
passphrase: string;
}
deleteApiKey()
Deletes (revokes) the currently authenticated API key.TypeScript Signature:
async deleteApiKey(): Promise<any>

Notifications
getNotifications()
Retrieves all event notifications for the L2 authenticated user. Records are removed
automatically after 48 hours or if manually removed via dropNotifications().
Signature
public async getNotifications(): Promise<Notification[]>
Response
interface Notification {
id: number; // Unique notification ID
owner: string; // User's L2 credential apiKey or empty string for global
notifications
payload: any; // Type-specific payload data
timestamp?: number; // Unix timestamp
type: number; // Notification type (see type mapping below)
}
Notification Type Mapping
Name Value Description
Order Cancellation 1 User’s order was canceled
Order Fill 2 User’s order was filled (maker or taker)
Market Resolved 4 Market was resolved
dropNotifications()
Mark notifications as read/dismissed.
Signature
public async dropNotifications(params?: DropNotificationParams): Promise<void>
Params
interface DropNotificationParams {
ids: string[]; // Array of notification IDs to mark as read

}
Builder Methods
These methods require builder API credentials and are only relevant for Builders Program
order attribution.
Client Initialization
Builder methods require the client to initialize with a separate authentication setup using
builder configs acquired from Polymarket.com and the @polymarket/builder-signing-
sdk package.
Local Builder Credentials
TypeScript
```python
import { ClobClient } from "@polymarket/clob-client";
import { BuilderConfig, BuilderApiKeyCreds } from "@polymarket/builder-signing-sdk";
const builderConfig = new BuilderConfig({
localBuilderCreds: new BuilderApiKeyCreds({
key: process.env.BUILDER_API_KEY,
secret: process.env.BUILDER_SECRET,
passphrase: process.env.BUILDER_PASS_PHRASE,
}),
});
```
const clobClient = new ClobClient(
"https://clob.polymarket.com",
137,
signer,
apiCreds, // The user's API credentials generated from L1 authentication
signatureType,
funderAddress,
undefined,
false,
builderConfig
);
Python
```python
from py_clob_client.client import ClobClient
from py_builder_signing_sdk.config import BuilderConfig, BuilderApiKeyCreds
import os
builder_config = BuilderConfig(
local_builder_creds=BuilderApiKeyCreds(

key=os.getenv("BUILDER_API_KEY"),
secret=os.getenv("BUILDER_SECRET"),
passphrase=os.getenv("BUILDER_PASS_PHRASE"),
)
)
clob_client = ClobClient(
host="https://clob.polymarket.com",
chain_id=137,
key=os.getenv("PRIVATE_KEY"),
creds=creds, # The user's API credentials generated from L1 authentication
```
signature_type=signature_type,
funder=funder,
builder_config=builder_config
)
Remote Builder Signing
TypeScript
```python
import { ClobClient } from "@polymarket/clob-client";
import { BuilderConfig } from "@polymarket/builder-signing-sdk";
const builderConfig = new BuilderConfig({
remoteBuilderConfig: {url: "http://localhost:3000/sign"}
});
```
const clobClient = new ClobClient(
"https://clob.polymarket.com",
137,
signer,
apiCreds, // The user's API credentials generated from L1 authentication
signatureType,
funder,
undefined,
false,
builderConfig
);
Python
```python
from py_clob_client.client import ClobClient
from py_builder_signing_sdk.config import BuilderConfig, RemoteBuilderConfig
import os
builder_config = BuilderConfig(
remote_builder_config=RemoteBuilderConfig(
url="http://localhost:3000/sign"
)
)

clob_client = ClobClient(
host="https://clob.polymarket.com",
chain_id=137,
key=os.getenv("PRIVATE_KEY"),
creds=creds, # The user's API credentials generated from L1 authentication
```
signature_type=signature_type,
funder=funder,
builder_config=builder_config
)
More information on builder signing
Methods
getBuilderTrades()
Retrieves all trades attributed to your builder account. This method allows builders to track
which trades were routed through your platform.
Signature
async getBuilderTrades(
params?: TradeParams,
): Promise<BuilderTradesPaginatedResponse>
Params
interface TradeParams {
id?: string;
maker_address?: string;
market?: string;
asset_id?: string;
before?: string;
after?: string;
}
Response
interface BuilderTradesPaginatedResponse {
trades: BuilderTrade[];
next_cursor: string;
limit: number;
count: number;
}

interface BuilderTrade {
id: string;
tradeType: string;
takerOrderHash: string;
builder: string;
market: string;
assetId: string;
side: string;
size: string;
sizeUsdc: string;
price: string;
status: string;
outcome: string;
outcomeIndex: number;
owner: string;
maker: string;
transactionHash: string;
matchTime: string;
bucketIndex: number;
fee: string;
feeUsdc: string;
err_msg?: string | null;
createdAt: string | null;
updatedAt: string | null;
}
revokeBuilderApiKey()
Revokes the builder API key used to authenticate the current request. After revocation, the
key can no longer be used to make builder-authenticated requests.
Signature
async revokeBuilderApiKey(): Promise<any>

## Rest Api

Orderbook
Get order book summary
Retrieves the order book summary for a specific token
GET/book
Get order book summary
```bash
cURL

curl --request GET \
--url https://clob.polymarket.com/book
Python
import requests
url = "https://clob.polymarket.com/book"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://clob.polymarket.com/book', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://clob.polymarket.com/book",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}

Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://clob.polymarket.com/book"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://clob.polymarket.com/book")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://clob.polymarket.com/book")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
{
"market": "0x1b6f76e5b8587ee896c35847e12d11e75290a8c3934c5952e8a9d6e4c6f03cfa",
"asset_id": "1234567890",

"timestamp": "2023-10-01T12:00:00Z",
"hash": "0xabc123def456...",
"bids": [
{
"price": "1800.50",
"size": "10.5"
}
],
"asks": [
{
"price": "1800.50",
"size": "10.5"
}
],
"min_order_size": "0.001",
"tick_size": "0.01",
"neg_risk": false
}
400
{
"error": "Invalid token id"
}
404
{
"error": "No orderbook exists for the requested token id"
}
500
{
"error": "error getting the orderbook"
}
Query Parameters
token_id
string
required
The unique identifier for the token
Response

200
application/json
Successful response
market
string
required
Market identifier
Example: "0x1b6f76e5b8587ee896c35847e12d11e75290a8c3934c5952e8a9d6e4c6f03cfa"
asset_id
string
required
Asset identifier
Example: "1234567890"
timestamp
string`
required
Timestamp of the order book snapshot
Example: "2023-10-01T12:00:00Z"
hash
string
required
Hash of the order book state
Example: "0xabc123def456..."

bids
object[]
required
Array of bid levels

### Child attributes

bids.price
string
required
Price level (as string to maintain precision)
Example: "1800.50"
bids.size
string
required
Total size at this price level
Example: "10.5"
asks
object[]
required
Array of ask levels

### Child attributes

asks.price
string
required
Price level (as string to maintain precision)
Example: "1800.50"
asks.size
string
required

Total size at this price level
Example: "10.5"
min_order_size
string
required
Minimum order size for this market
Example: "0.001"
tick_size
string
required
Minimum price increment
Example: "0.01"
neg_risk
boolean
required
Whether negative risk is enabled
Example: false
Response
400
application/json
Bad request

error
string
required
Error message describing what went wrong

### Example

"Invalid token id"
Response
404
application/json
Order book not found
error
string
required
Error message describing what went wrong

### Example

"Invalid token id"
Response
500
application/json
Internal server error
error
string
required
Error message describing what went wrong

### Example

"Invalid token id"
Get multiple order books summaries by request

Retrieves order book summaries for specified tokens via POST request
POST/books
Get multiple order books summaries by request
```bash
cURL
curl --request POST \
--url https://clob.polymarket.com/books \
```
--header 'Content-Type: application/json' \
--data '
[
{
"token_id": "1234567890"
},
{
"token_id": "0987654321"
}
]
'
Python
```python
import requests
url = "https://clob.polymarket.com/books"
payload = [{ "token_id": "1234567890" }, { "token_id": "0987654321" }]
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=payload, headers=headers)
print(response.text)
JavaScript
const options = {
method: 'POST',
```
headers: {'Content-Type': 'application/json'},
body: JSON.stringify([{token_id: '1234567890'}, {token_id: '0987654321'}])
};
fetch('https://clob.polymarket.com/books', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP

<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://clob.polymarket.com/books",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "POST",
CURLOPT_POSTFIELDS => json_encode([
[
'token_id' => '1234567890'
```
],
[
'token_id' => '0987654321'
]
]),
```bash
CURLOPT_HTTPHEADER => [
"Content-Type: application/json"
],
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"strings"
"net/http"
"io"
)
func main() {
url := "https://clob.polymarket.com/books"

payload := strings.NewReader("[\n {\n \"token_id\": \"1234567890\"\n },\n
```
{\n \"token_id\": \"0987654321\"\n }\n]")
req, _ := http.NewRequest("POST", url, payload)
req.Header.Add("Content-Type", "application/json")
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.post("https://clob.polymarket.com/books")
.header("Content-Type", "application/json")
.body("[\n {\n \"token_id\": \"1234567890\"\n },\n {\n \"token_id\":
\"0987654321\"\n }\n]")
.asString();
Ruby
require 'uri'
require 'net/http'
url = URI("https://clob.polymarket.com/books")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Post.new(url)
request["Content-Type"] = 'application/json'
request.body = "[\n {\n \"token_id\": \"1234567890\"\n },\n {\n \"token_id\":
\"0987654321\"\n }\n]"
response = http.request(request)
puts response.read_body
200
[
{
"market": "0x1b6f76e5b8587ee896c35847e12d11e75290a8c3934c5952e8a9d6e4c6f03cfa",
"asset_id": "1234567890",
"timestamp": "2023-10-01T12:00:00Z",
"hash": "0xabc123def456...",

"bids": [
{
"price": "1800.50",
"size": "10.5"
}
],
"asks": [
{
"price": "1800.50",
"size": "10.5"
}
],
"min_order_size": "0.001",
"tick_size": "0.01",
"neg_risk": false
}
]
400
{
"error": "Invalid payload"
}
500
{
"error": "Invalid token id"
}
Body
application/json
Maximum array length: 500
token_id
string
required
The unique identifier for the token

### Example

"1234567890"

side
enum`
Optional side parameter for certain operations
Available options: BUY, SELL

### Example

"BUY"
Response
200
application/json
Successful response
market
string
required
Market identifier

### Example

"0x1b6f76e5b8587ee896c35847e12d11e75290a8c3934c5952e8a9d6e4c6f03cfa"
asset_id
string
required
Asset identifier

### Example

"1234567890"
timestamp
string`
required
Timestamp of the order book snapshot


### Example


## "2023-10-01T12:00:00Z"

hash
string
required
Hash of the order book state

### Example

"0xabc123def456..."
bids
object[]
required
Array of bid levels

### Child attributes

bids.price
string
required
Price level (as string to maintain precision)
Example: "1800.50"
bids.size
string
required
Total size at this price level
Example: "10.5"
asks
object[]

required
Array of ask levels

### Child attributes

asks.price
string
required
Price level (as string to maintain precision)
Example: "1800.50"
asks.size
string
required
Total size at this price level
Example: "10.5"
min_order_size
string
required
Minimum order size for this market

### Example

"0.001"
tick_size
string
required
Minimum price increment

### Example

"0.01"
neg_risk
boolean

required
Whether negative risk is enabled

### Example

false
Response
400
application/json
Bad request - Invalid payload or exceeds limit
error
string
required
Error message describing what went wrong

### Example

"Invalid token id"
Response
500
application/json
Internal server error
error
string
required
Error message describing what went wrong

### Example

"Invalid token id"
Pricing
Get market price

Retrieves the market price for a specific token and side
GET/price
Get market price
```bash
cURL
curl --request GET \
--url https://clob.polymarket.com/price
Python
import requests
url = "https://clob.polymarket.com/price"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://clob.polymarket.com/price', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://clob.polymarket.com/price",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);

if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://clob.polymarket.com/price"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://clob.polymarket.com/price")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://clob.polymarket.com/price")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
200
{
"price": "1800.50"
}
400
{
"error": "Invalid token id"
}
404
{
"error": "No orderbook exists for the requested token id"
}
500
{ "error": "Invalid token id"}
Query Parameters
token_id
string
required
The unique identifier for the token
side
enum`
required
The side of the market (BUY or SELL)
Available options: BUY, SELL
Response
200

application/json
Successful response
price
string
required
The market price (as string to maintain precision)

### Example

"1800.50"
Get multiple market prices
Retrieves market prices for multiple tokens and sides
GET/prices
Get multiple market prices
```bash
cURL
curl --request GET \
--url https://clob.polymarket.com/prices
Python
import requests
url = "https://clob.polymarket.com/prices"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://clob.polymarket.com/prices', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();

```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://clob.polymarket.com/prices",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://clob.polymarket.com/prices"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://clob.polymarket.com/prices")
.asString();
```

Ruby
require 'uri'
require 'net/http'
url = URI("https://clob.polymarket.com/prices")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
{
"1234567890": {

## "Buy": "1800.50",


## "Sell": "1801.00"

},
"0987654321": {

## "Buy": "50.25",


## "Sell": "50.30"

}
}
400
{
"error": "Invalid token id"
}
500
{
"error": "Invalid token id"
}
Response
200
application/json
Successful response
Map of token_id to side to price

{key}
object

### Child attributes

{key}.{key}
string
Response
400
Bad request
error
string
required
Error message describing what went wrong

### Example

"Invalid token id"
Response
500
Internal server error
error
string
required
Error message describing what went wrong

### Example

"Invalid token id"
Get multiple market prices by request
Retrieves market prices for specified tokens and sides via POST request
POST/prices
Get multiple market prices by request
```bash
cURL

curl --request POST \
--url https://clob.polymarket.com/prices \
```
--header 'Content-Type: application/json' \
--data '
[
{
"token_id": "1234567890",
"side": "BUY"
},
{
"token_id": "0987654321",
"side": "SELL"
}
]
'
Python
```python
import requests
url = "https://clob.polymarket.com/prices"
payload = [
{
"token_id": "1234567890",
"side": "BUY"
},
{
"token_id": "0987654321",
"side": "SELL"
}
]
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=payload, headers=headers)
print(response.text)
JavaScript
const options = {
method: 'POST',
```
headers: {'Content-Type': 'application/json'},
body: JSON.stringify([{token_id: '1234567890', side: 'BUY'}, {token_id:
'0987654321', side: 'SELL'}])
};
fetch('https://clob.polymarket.com/prices', options)
.then(res => res.json())

.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://clob.polymarket.com/prices",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "POST",
CURLOPT_POSTFIELDS => json_encode([
[
'token_id' => '1234567890',
```
'side' => 'BUY'
],
[
'token_id' => '0987654321',
'side' => 'SELL'
]
]),
```bash
CURLOPT_HTTPHEADER => [
"Content-Type: application/json"
],
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"strings"
"net/http"

"io"
)
func main() {
url := "https://clob.polymarket.com/prices"
payload := strings.NewReader("[\n {\n \"token_id\": \"1234567890\",\n
```
\"side\": \"BUY\"\n },\n {\n \"token_id\": \"0987654321\",\n \"side\":
\"SELL\"\n }\n]")
req, _ := http.NewRequest("POST", url, payload)
req.Header.Add("Content-Type", "application/json")
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.post("https://clob.polymarket.com/prices")
.header("Content-Type", "application/json")
.body("[\n {\n \"token_id\": \"1234567890\",\n \"side\": \"BUY\"\n },\n {\n
\"token_id\": \"0987654321\",\n \"side\": \"SELL\"\n }\n]")
.asString();
Ruby
require 'uri'
require 'net/http'
url = URI("https://clob.polymarket.com/prices")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Post.new(url)
request["Content-Type"] = 'application/json'
request.body = "[\n {\n \"token_id\": \"1234567890\",\n \"side\": \"BUY\"\n
},\n {\n \"token_id\": \"0987654321\",\n \"side\": \"SELL\"\n }\n]"
response = http.request(request)
puts response.read_body

200
{
"1234567890": {

## "Buy": "1800.50",


## "Sell": "1801.00"

},
"0987654321": {

## "Buy": "50.25",


## "Sell": "50.30"

}
}
400
{
"error": "Invalid payload"
}
404
{
"error": "No orderbook exists for the requested token id"
}
500
{
"error": "Invalid token id"
}
Body
application/json
Maximum array length: 500
token_id
string
required
The unique identifier for the token

### Example

"1234567890"

side
enum`
required
The side of the market (BUY or SELL)
Available options: BUY, SELL

### Example

"BUY"
Response
200
application/json
Successful response
Map of token_id to side to price
{key}
object

### Child attributes

{key}.{key}
string
Response
400
application/json
Bad request - Invalid payload, exceeds limit, or invalid side
error
string
required
Error message describing what went wrong

### Example

"Invalid token id"

Response
404
application/json
Order book not found
error
string
required
Error message describing what went wrong

### Example

"Invalid token id"
Response
500
application/json
Internal server error
error
string
required
Error message describing what went wrong

### Example

"Invalid token id"
Get midpoint price
Retrieves the midpoint price for a specific token
GET/midpoint
Get midpoint price
```bash
cURL
curl --request GET \
--url https://clob.polymarket.com/midpoint

Python
import requests
url = "https://clob.polymarket.com/midpoint"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://clob.polymarket.com/midpoint', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://clob.polymarket.com/midpoint",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main

```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://clob.polymarket.com/midpoint"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://clob.polymarket.com/midpoint")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://clob.polymarket.com/midpoint")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
{
"mid": "1800.75"
}
400
{ "error": "Invalid token id" }

404
{ "error": "No orderbook exists for the requested token id" }
500
{ "error": "Invalid token id" }
Query Parameters
token_id
string
required
The unique identifier for the token
Response
200
application/json
Successful response
mid
string
required
The midpoint price (as string to maintain precision)

### Example

"1800.75"
Response
400
application/json
Bad request
error
string
required
Error message describing what went wrong


### Example

"Invalid token id"
Response
404
application/json
Order book not found
error
stringrequired
Error message describing what went wrong

### Example

"Invalid token id"
Response
500
application/json
Internal server error
error
string
required
Error message describing what went wrong

### Example

"Invalid token id"
Get price history for a traded token
Fetches historical price data for a specified market token
GET/prices-history
Get price history for a traded token

```bash
cURL
curl --request GET \
--url https://clob.polymarket.com/prices-history
Python
import requests
url = "https://clob.polymarket.com/prices-history"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://clob.polymarket.com/prices-history', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://clob.polymarket.com/prices-history",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {

echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://clob.polymarket.com/prices-history"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://clob.polymarket.com/prices-
history")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://clob.polymarket.com/prices-history")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200

{
"history": [
{
"t": 1697875200,
"p": 1800.75
}
]
}
400
{
"error": "Invalid token id"
}
404
{
"error": "Invalid token id"
}
500
{
"error": "Invalid token id"
}
Query Parameters
market
string
required
The CLOB token ID for which to fetch price history
startTs
number
The start time, a Unix timestamp in UTC
endTs
number
The end time, a Unix timestamp in UTC

interval
enum`
A string representing a duration ending at the current time. Mutually exclusive with startTs
and endTs
Available options: 1m, 1w, 1d, 6h, 1h, max
fidelity
number
The resolution of the data, in minutes
Response
200
application/json
A list of timestamp/price pairs
history
object[]required
Hide child attributes
history.t
numberrequired
UTC timestamp

### Example

1697875200
history.p
numberrequired
Price

### Example

1800.75

Response
400
application/json
Bad request
error
string
required
Error message describing what went wrong

### Example

"Invalid token id"
Response
404
application/json
Market not found
error
string
required
Error message describing what went wrong

### Example

"Invalid token id"
Response
500
application/json
Internal server error
error
string
required
Error message describing what went wrong


### Example

"Invalid token id"
Spreads
Get bid-ask spreads
Retrieves bid-ask spreads for multiple tokens
POST/spreads
Get bid-ask spreads
```bash
cURL
curl --request POST \
--url https://clob.polymarket.com/spreads \
```
--header 'Content-Type: application/json' \
--data '
[
{
"token_id": "1234567890"
},
{
"token_id": "0987654321"
}
]
'
Python
```python
import requests
url = "https://clob.polymarket.com/spreads"
payload = [{ "token_id": "1234567890" }, { "token_id": "0987654321" }]
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=payload, headers=headers)
print(response.text)
JavaScript
const options = {
method: 'POST',
```
headers: {'Content-Type': 'application/json'},
body: JSON.stringify([{token_id: '1234567890'}, {token_id: '0987654321'}])

};
fetch('https://clob.polymarket.com/spreads', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://clob.polymarket.com/spreads",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "POST",
CURLOPT_POSTFIELDS => json_encode([
[
'token_id' => '1234567890'
```
],
[
'token_id' => '0987654321'
]
]),
```bash
CURLOPT_HTTPHEADER => [
"Content-Type: application/json"
],
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"

"strings"
"net/http"
"io"
)
func main() {
url := "https://clob.polymarket.com/spreads"
payload := strings.NewReader("[\n {\n \"token_id\": \"1234567890\"\n },\n
```
{\n \"token_id\": \"0987654321\"\n }\n]")
req, _ := http.NewRequest("POST", url, payload)
req.Header.Add("Content-Type", "application/json")
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.post("https://clob.polymarket.com/spreads")
.header("Content-Type", "application/json")
.body("[\n {\n \"token_id\": \"1234567890\"\n },\n {\n \"token_id\":
\"0987654321\"\n }\n]")
.asString();
Ruby
require 'uri'
require 'net/http'
url = URI("https://clob.polymarket.com/spreads")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Post.new(url)
request["Content-Type"] = 'application/json'
request.body = "[\n {\n \"token_id\": \"1234567890\"\n },\n {\n \"token_id\":
\"0987654321\"\n }\n]"
response = http.request(request)
puts response.read_body

200
{
"1234567890": "0.50",
"0987654321": "0.05"
}
400
{
"error": "Invalid payload"
}
500
{
"error": "error getting the spread"
}
Body
application/json
Maximum array length: 500
token_id
string
required
The unique identifier for the token

### Example

"1234567890"
side
enum`
Optional side parameter for certain operations
Available options: BUY, SELL

### Example

"BUY"
Response

200
application/json
Successful response
Map of token_id to spread value
{key}
string
Response
400
application/json
Bad request - Invalid payload or exceeds limit
error
stringrequired
Error message describing what went wrong

### Example

"Invalid token id"
Response
500
application/json
Internal server error
error
stringrequired
Error message describing what went wrong

### Example

"Invalid token id"
Historical Timeseries Data
Fetches historical price data for a specified market token.

GET/prices-history
Get price history for a traded token
```bash
cURL
curl --request GET \
--url https://clob.polymarket.com/prices-history
Python
import requests
url = "https://clob.polymarket.com/prices-history"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://clob.polymarket.com/prices-history', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://clob.polymarket.com/prices-history",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```

echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://clob.polymarket.com/prices-history"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://clob.polymarket.com/prices-
history")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://clob.polymarket.com/prices-history")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body

200
{
"history": [
{
"t": 1697875200,
"p": 1800.75
}
]
}
400
{
"error": "Invalid token id"
}
404
{
"error": "Invalid token id"
}
500
{
"error": "Invalid token id"
}
The CLOB provides detailed price history for each traded token.

## **Http Request

** GET /<clob-endpoint>/prices-history
We also have a Interactive Notebook to visualize the data from this endpoint available here.
Query Parameters
market
stringrequired
The CLOB token ID for which to fetch price history

startTs
number
The start time, a Unix timestamp in UTC
endTs
number
The end time, a Unix timestamp in UTC
interval
enum`
A string representing a duration ending at the current time. Mutually exclusive with startTs
and endTs
Available options: 1m, 1w, 1d, 6h, 1h, max
fidelity
number
The resolution of the data, in minutes
Response
200
application/json
A list of timestamp/price pairs
history
object[]
required

### Child attributes

history.t
number

required
UTC timestamp

### Example

1697875200
history.p
number
required
Price

### Example

1800.75
Response
400
application/json
Bad request
error
string
required
Error message describing what went wrong

### Example

"Invalid token id"
Response
404
application/json
Bad request
error
string

required
Error message describing what went wrong

### Example

"Invalid token id"
Response
500
application/json
Internal server error
error
string
required
Error message describing what went wrong

### Example

"Invalid token id"
Orders Management
Orders Overview
Detailed instructions for creating, placing, and managing orders using Polymarket’s CLOB
API.
All orders are expressed as limit orders (can be marketable). The underlying order primitive
must be in the form expected and executable by the on-chain binary limit order protocol
contract. Preparing such an order is quite involved (structuring, hashing, signing), thus
Polymarket suggests using the open source typescript, python and golang libraries.
Allowances
To place an order, allowances must be set by the funder address for the
specified maker asset for the Exchange contract. When buying, this means the funder must
have set a USDC allowance greater than or equal to the spending amount. When selling, the
funder must have set an allowance for the conditional token that is greater than or equal to
the selling amount. This allows the Exchange contract to execute settlement according to the
signed order instructions created by a user and matched by the operator.

Signature Types
Polymarket’s CLOB supports 3 signature types. Orders must identify what signature type
they use. The available typescript and python clients abstract the complexity of signing and
preparing orders with the following signature types by allowing a funder address and signer
type to be specified on initialization. The supported signature types are:
Type ID Description
EOA 0 EIP712 signature signed by an EOA
POLY_PROXY 1 EIP712 signatures signed by a signer associated with
funding Polymarket proxy wallet
POLY_GNOSIS_SAFE 2 EIP712 signatures signed by a signer associated with
funding Polymarket gnosis safe wallet
Validity Checks
Orders are continually monitored to make sure they remain valid. Specifically, this includes
continually tracking underlying balances, allowances and on-chain order cancellations. Any
maker that is caught intentionally abusing these checks (which are essentially real time) will
be blacklisted.Additionally, there are rails on order placement in a market. Specifically, you
can only place orders that sum to less than or equal to your available balance for each
market. For example if you have 500 USDC in your funding wallet, you can place one order
to buy 1000 YES in marketA @ $.50, then any additional buy orders to that market will be
rejected since your entire balance is reserved for the first (and only) buy order. More
explicitly the max size you can place for an order is:
maxOrderSize=underlyingAssetBalance−∑(orderSize−orderFillAmount)maxOrderSize=unde
rlyingAssetBalance−∑(orderSize−orderFillAmount)
Place Single Order
Detailed instructions for creating, placing, and managing orders using Polymarket’s CLOB
API.
Create and Place an Order
This endpoint requires a L2 Header
Create and place an order using the Polymarket CLOB API clients. All orders are
represented as “limit” orders, but “market” orders are also supported. To place a market
order, simply ensure your price is marketable against current resting limit orders, which are
executed on input at the best price.

## Http Request


POST /<clob-endpoint>/order
Request Payload Parameters
Name Required Type Description
order yes Order signed object
owner yes string api key of order owner
orderType yes string order type (“FOK”, “GTC”, “GTD”)
postOnly no boolean if true , the order will only rest on the book and not
match immediately (default: false )
Post-only orders
postOnly submits a limit order that will not match resting liquidity upon entry.
If a postOnly order would cross the spread (i.e., it is marketable), it will be rejected rather
than executed.
postOnly cannot be combined with market order types (e.g., FOK or FAK). If postOnly =
true is sent with a market order type, the order will be rejected.

### An order object is the form

Name Required Type Description
salt yes integer random salt used to create unique order
maker yes string maker address (funder)
signer yes string signing address
taker yes string taker address (operator)
tokenId yes string ERC1155 token ID of conditional token being traded
makerAmount yes string maximum amount maker is willing to spend
takerAmount yes string minimum amount taker will pay the maker in return
expiration yes string unix expiration timestamp
nonce yes string maker’s exchange nonce of the order is associated
feeRateBps yes string fee rate basis points as required by the operator
side yes string buy or sell enum index
signatureType yes integer signature type enum index
signature yes string hex encoded signature
Order types

FOK: A Fill-Or-Kill order is an market order to buy (in dollars) or sell (in shares) shares
that must be executed immediately in its entirety; otherwise, the entire order will be
cancelled.
FAK: A Fill-And-Kill order is a market order to buy (in dollars) or sell (in shares) that will
be executed immediately for as many shares as are available; any portion not filled at
once is cancelled.
GTC: A Good-Til-Cancelled order is a limit order that is active until it is fulfilled or
cancelled.
GTD: A Good-Til-Date order is a type of order that is active until its specified date (UTC
seconds timestamp), unless it has already been fulfilled or cancelled. There is a security
threshold of one minute. If the order needs to expire in 90 seconds the correct expiration
value is: now + 1 minute + 30 seconds
Response Format
Name Type Description
success boolean boolean indicating if server-side err ( success = false ) -> server-
side error
errorMsg string error message in case of unsuccessful placement (in
case success = false , e.g. client-side error , the reason is
in errorMsg )
orderId string id of order
orderHashes string[] hash of settlement transaction order was marketable and
triggered a match
Insert Error Messages
If the errorMsg field of the response object from placement is not an empty string, the order
was not able to be immediately placed. This might be because of a delay or because of a
failure. If the success is not true , then there was an issue placing the order. The

### following errorMessages are possible

Error
Error Success Message Description
INVALID_ORDER_MIN_TICK_SIZE yes order is order price
invalid. isn’t
Price breaks accurate to
minimum correct tick
tick size sizing
rules

Error Success Message Description
INVALID_ORDER_MIN_SIZE yes order is order size
invalid. Size must meet
lower than min size
the minimum threshold
requirement
INVALID_ORDER_DUPLICATED yes order is
invalid.
Duplicated.
Same order
has already
been
placed, can’t
be placed
again
INVALID_ORDER_NOT_ENOUGH_BALANCE yes not enough funder
balance / address
allowance doesn’t have
sufficient
balance or
allowance
for order
INVALID_ORDER_EXPIRATION yes invalid expiration
expiration field
expresses a
time before
now
INVALID_ORDER_ERROR yes could not system error
insert order while
inserting
order
INVALID_POST_ONLY_ORDER_TYPE yes invalid post- post only
only order: flag
only GTC attached to
and GTD a market
order types order
are allowed
INVALID_POST_ONLY_ORDER yes invalid post- post only
only order: order would
order match
crosses book
EXECUTION_ERROR yes could not system error
run the while
execution attempting
to execute
trade

Error Success Message Description
ORDER_DELAYED no order match order
delayed due placement
to market delayed
conditions
DELAYING_ORDER_ERROR yes error system error
delaying the while
order delaying
order
FOK_ORDER_NOT_FILLED_ERROR yes order FOK order
couldn’t be not fully
fully filled, filled so
FOK orders can’t be
are fully placed
filled/killed
MARKET_NOT_READY no the market system not
is not yet accepting
ready to orders for
process new market yet
orders
Insert Statuses
When placing an order, a status field is included. The status field provides additional
information regarding the order’s state as a result of the placement. Possible values include:
Status
Status Description
matched order placed and matched with an existing resting order
live order placed and resting on the book
delayed order marketable, but subject to matching delay
unmatched order marketable, but failure delaying, placement successful
Place Multiple Orders (Batching)
Instructions for placing multiple orders(Batch)
This endpoint requires a L2 Header
Polymarket’s CLOB supports batch orders, allowing you to place up to 15 orders in a single
request. Before using this feature, make sure you’re comfortable placing a single order first.
You can find the documentation for that here.


## Http Request

POST /<clob-endpoint>/orders
Request Payload Parameters
Name Required Type Description
PostOrder yes PostOrders[] list of signed order objects (Signed Order + Order
Type + Owner)

### A PostOrder object is the form

Name Required Type Description
order yes order See below table for details on crafting this object
orderType yes string order type (“FOK”, “GTC”, “GTD”, “FAK”)
owner yes string api key of order owner
postOnly no boolean if true , the order will only rest on the book and not
match immediately (default: false )

### An order object is the form

Name Required Type Description
salt yes integer random salt used to create unique order
maker yes string maker address (funder)
signer yes string signing address
taker yes string taker address (operator)
tokenId yes string ERC1155 token ID of conditional token being traded
makerAmount yes string maximum amount maker is willing to spend
takerAmount yes string minimum amount taker will pay the maker in return
expiration yes string unix expiration timestamp
nonce yes string maker’s exchange nonce of the order is associated
feeRateBps yes string fee rate basis points as required by the operator
side yes string buy or sell enum index
signatureType yes integer signature type enum index
signature yes string hex encoded signature
Order types

FOK: A Fill-Or-Kill order is an market order to buy (in dollars) or sell (in shares) shares
that must be executed immediately in its entirety; otherwise, the entire order will be
cancelled.
FAK: A Fill-And-Kill order is a market order to buy (in dollars) or sell (in shares) that will
be executed immediately for as many shares as are available; any portion not filled at
once is cancelled.
GTC: A Good-Til-Cancelled order is a limit order that is active until it is fulfilled or
cancelled.
GTD: A Good-Til-Date order is a type of order that is active until its specified date (UTC
seconds timestamp), unless it has already been fulfilled or cancelled. There is a security
threshold of one minute. If the order needs to expire in 90 seconds the correct expiration
value is: now + 1 minute + 30 seconds
Response Format
Name Type Description
success boolean boolean indicating if server-side err ( success = false ) -> server-
side error
errorMsg string error message in case of unsuccessful placement (in
case success = false , e.g. client-side error , the reason is
in errorMsg )
orderId string id of order
orderHashes string[] hash of settlement transaction order was marketable and
triggered a match
Insert Error Messages
If the errorMsg field of the response object from placement is not an empty string, the order
was not able to be immediately placed. This might be because of a delay or because of a
failure. If the success is not true , then there was an issue placing the order. The

### following errorMessages are possible

Error
Error Success Message Description
INVALID_ORDER_MIN_TICK_SIZE yes order is order price
invalid. isn’t
Price breaks accurate to
minimum correct tick
tick size sizing
rules

Error Success Message Description
INVALID_ORDER_MIN_SIZE yes order is order size
invalid. Size must meet
lower than min size
the minimum threshold
requirement
INVALID_ORDER_DUPLICATED yes order is
invalid.
Duplicated.
Same order
has already
been
placed, can’t
be placed
again
INVALID_ORDER_NOT_ENOUGH_BALANCE yes not enough funder
balance / address
allowance doesn’t have
sufficient
balance or
allowance
for order
INVALID_ORDER_EXPIRATION yes invalid expiration
expiration field
expresses a
time before
now
INVALID_ORDER_ERROR yes could not system error
insert order while
inserting
order
INVALID_POST_ONLY_ORDER_TYPE yes invalid post- post only
only order: flag
only GTC attached to
and GTD a market
order types order
are allowed
INVALID_POST_ONLY_ORDER yes invalid post- post only
only order: order would
order match
crosses book
EXECUTION_ERROR yes could not system error
run the while
execution attempting
to execute
trade

Error Success Message Description
ORDER_DELAYED no order match order
delayed due placement
to market delayed
conditions
DELAYING_ORDER_ERROR yes error system error
delaying the while
order delaying
order
FOK_ORDER_NOT_FILLED_ERROR yes order FOK order
couldn’t be not fully
fully filled, filled so
FOK orders can’t be
are fully placed
filled/killed
MARKET_NOT_READY no the market system not
is not yet accepting
ready to orders for
process new market yet
orders
Insert Statuses
When placing an order, a status field is included. The status field provides additional
information regarding the order’s state as a result of the placement. Possible values include:
Status
Status Description
matched order placed and matched with an existing resting order
live order placed and resting on the book
delayed order marketable, but subject to matching delay
unmatched order marketable, but failure delaying, placement successful
Get Order
Get information about an existing order
This endpoint requires a L2 Header.
Get single order by id.

## Http Request

GET /<clob-endpoint>/data/order/<order_hash>

Request Parameters
Name Required Type Description
id no string id of order to get information about
Response Format
Name Type Description
order OpenOrder order if it exists

### An OpenOrder object is of the form

Name Type Description
associate_trades string[] any Trade id the order has been partially included in
id string order id
status string order current status
market string market id (condition id)
original_size string original order size at placement
outcome string human readable outcome the order is for
maker_address string maker address (funder)
owner string api key
price string price
side string buy or sell
size_matched string size of order that has been matched/filled
asset_id string token id
expiration string unix timestamp when the order expired, 0 if it does not expire
type string order type (GTC, FOK, GTD)
created_at string unix timestamp when the order was created
Get Active Orders
This endpoint requires a L2 Header.
Get active order(s) for a specific market.

## Http Request

GET /<clob-endpoint>/data/orders

Request Parameters
Name Required Type Description
id no string id of order to get information about
market no string condition id of market
asset_id no string id of the asset/token
Response Format
Name Type Description
null OpenOrder[] list of open orders filtered by the query parameters
Check Order Reward Scoring
Check if an order is eligble or scoring for Rewards purposes
This endpoint requires a L2 Header.
Returns a boolean value where it is indicated if an order is scoring or not.

## Http Request

GET /<clob-endpoint>/order-scoring?order_id={...}
Request Parameters
Name Required Type Description
orderId yes string id of order to get information about
Response Format
Name Type Description
null OrdersScoring order scoring data

### An OrdersScoring object is of the form

Name Type Description
scoring boolean indicates if the order is scoring or not
Check if some orders are scoring

This endpoint requires a L2 Header.
Returns to a dictionary with boolean value where it is indicated if an order is scoring or not.

## Http Request

POST /<clob-endpoint>/orders-scoring
Request Parameters
Name Required Type Description
orderIds yes string[] ids of the orders to get information about
Response Format
Name Type Description
null OrdersScoring orders scoring data
An OrdersScoring object is a dictionary that indicates the order by if it score.
Cancel Orders(s)
Multiple endpoints to cancel a single order, multiple orders, all orders or all orders from a
single market.
Cancel an single Order
This endpoint requires a L2 Header.
Cancel an order.

## Http Request

DELETE /<clob-endpoint>/order
Request Payload Parameters
Name Required Type Description
orderID yes string ID of order to cancel
Response Format
Name Type Description
canceled string[] list of canceled orders

Name Type Description
not_canceled a order id -> reason map that explains why that order couldn’t
be canceled
Python
resp =
client.cancel(order_id="0x38a73eed1e6d177545e9ab027abddfb7e08dbe975fa777123b1752d203d6
ac88")
print(resp)
Typescript
async function main() {
// Send it to the server
const resp = await clobClient.cancelOrder({

### orderID

"0x38a73eed1e6d177545e9ab027abddfb7e08dbe975fa777123b1752d203d6ac88",
});
console.log(resp);
console.log(`Done!`);
}
main();
Cancel Multiple Orders
This endpoint requires a L2 Header.
HTTP REQUEST DELETE /<clob-endpoint>/orders
Request Payload Parameters
Name Required Type Description
null yes string[] IDs of the orders to cancel
Response Format
Name Type Description
canceled string[] list of canceled orders
not_canceled a order id -> reason map that explains why that order couldn’t
be canceled
Python

resp =
client.cancel_orders(["0x38a73eed1e6d177545e9ab027abddfb7e08dbe975fa777123b1752d203d6a
c88", "0xaaaa..."])
print(resp)
Typescript
async function main() {
// Send it to the server
const resp = await clobClient.cancelOrders([
"0x38a73eed1e6d177545e9ab027abddfb7e08dbe975fa777123b1752d203d6ac88",
"0xaaaa...",
]);
console.log(resp);
console.log(`Done!`);
}
main();
Cancel ALL Orders
This endpoint requires a L2 Header.
Cancel all open orders posted by a user.

## Http Request

DELETE /<clob-endpoint>/cancel-all
Response Format
Name Type Description
canceled string[] list of canceled orders
not_canceled a order id -> reason map that explains why that order couldn’t
be canceled
Python
resp = client.cancel_all()
print(resp)
print("Done!")
Typescript
async function main() {
const resp = await clobClient.cancelAll();
console.log(resp);
console.log(`Done!`);
}

main();
Cancel orders from market
This endpoint requires a L2 Header.
Cancel orders from market.

## Http Request

DELETE /<clob-endpoint>/cancel-market-orders
Request Payload Parameters
Name Required Type Description
market no string condition id of the market
asset_id no string id of the asset/token
Response Format
Name Type Description
canceled string[] list of canceled orders
not_canceled a order id -> reason map that explains why that order couldn’t
be canceled
Python
resp =
client.cancel_market_orders(market="0xbd31dc8a20211944f6b70f31557f1001557b59905b773848
0ca09bd4532f84af",
asset_id="5211431950124591551605510604688420996992612748282795467444384642781381322242
6")
print(resp)
Typescript
async function main() {
// Send it to the server
const resp = await clobClient.cancelMarketOrders({

### market

"0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",

### asset_id

"52114319501245915516055106046884209969926127482827954674443846427813813222426",
});

console.log(resp);
console.log(`Done!`);
}
main();
Onchain Order Info
How do I interpret the OrderFilled onchain event?

### Given an OrderFilled event

orderHash : a unique hash for the Order being filled
maker : the user generating the order and the source of funds for the order
taker : the user filling the order OR the Exchange contract if the order fills multiple limit
orders
makerAssetId : id of the asset that is given out. If 0, indicates that the Order is a BUY,
giving USDC in exchange for Outcome tokens. Else, indicates that the Order is a SELL,
giving Outcome tokens in exchange for USDC.
takerAssetId : id of the asset that is received. If 0, indicates that the Order is a SELL,
receiving USDC in exchange for Outcome tokens. Else, indicates that the Order is a
BUY, receiving Outcome tokens in exchange for USDC.
makerAmountFilled : the amount of the asset that is given out.
takerAmountFilled : the amount of the asset that is received.
fee : the fees paid by the order maker
Trades
Trades Overview
Overview
All historical trades can be fetched via the Polymarket CLOB REST API. A trade is initiated
by a “taker” who creates a marketable limit order. This limit order can be matched against
one or more resting limit orders on the associated book. A trade can be in various states as
described below. Note: in some cases (due to gas limitations) the execution of a “trade” must
be broken into multiple transactions which case separate trade entities will be returned. To
associate trade entities, there is a bucket_index field and a match_time field. Trades that
have been broken into multiple trade objects can be reconciled by combining trade objects
with the same market_order_id, match_time and incrementing bucket_index’s into a top level
“trade” client side.
Statuses

Status Terminal? Description
MATCHED no trade has been matched and sent to the executor service by
the operator, the executor service submits the trade as a
transaction to the Exchange contract
MINED no trade is observed to be mined into the chain, no finality
threshold established
CONFIRMED yes trade has achieved strong probabilistic finality and was
successful
RETRYING no trade transaction has failed (revert or reorg) and is being
retried/resubmitted by the operator
FAILED yes trade has failed and is not being retried
Get Trades
This endpoint requires a L2 Header.
Get trades for the authenticated user based on the provided filters.HTTP REQUEST GET
/<clob-endpoint>/data/trades
Request Parameters
Name Required Type Description
id no string id of trade to fetch
taker no string address to get trades for where it is included as a taker
maker no string address to get trades for where it is included as a maker
market no string market for which to get the trades (condition ID)
before no string unix timestamp representing the cutoff up to which trades
that happened before then can be included
after no string unix timestamp representing the cutoff for which trades that
happened after can be included
Response Format
Name Type Description
null Trade[] list of trades filtered by query parameters

### A Trade object is of the form


Name Type Description
id string trade id
taker_order_id string hash of taker order (market order) that catalyzed the
trade
market string market id (condition id)
asset_id string asset id (token id) of taker order (market order)
side string buy or sell
size string size
fee_rate_bps string the fees paid for the taker order expressed in basic
points
price string limit price of taker order
status string trade status (see above)
match_time string time at which the trade was matched
last_update string timestamp of last status update
outcome string human readable outcome of the trade
maker_address string funder address of the taker of the trade
owner string api key of taker of the trade
transaction_hash string hash of the transaction where the trade was executed
bucket_index integer index of bucket for trade in case trade is executed in
multiple transactions
maker_orders MakerOrder[] list of the maker trades the taker trade was filled
against
type string side of the trade: TAKER or MAKER

### A MakerOrder object is of the form

Name Type Description
order_id string id of maker order
maker_address string maker address of the order
owner string api key of the owner of the order
matched_amount string size of maker order consumed with this trade
fee_rate_bps string the fees paid for the taker order expressed in basic points
price string price of maker order
asset_id string token/asset id
outcome string human readable outcome of the maker order
side string the side of the maker order. Can be buy or sell

Websocket
WSS Overview
Overview and general information about the Polymarket Websocket
Overview
The Polymarket CLOB API provides websocket (wss) channels through which clients can get
pushed updates. These endpoints allow clients to maintain almost real-time views of their
orders, their trades and markets in general. There are two available
channels user and market .
Subscription
To subscribe send a message including the following authentication and intent information
upon opening the connection.
Field Type Description
auth Auth see next page for auth information
markets string[] array of markets (condition IDs) to receive events for
(for user channel)
assets_ids string[] array of asset ids (token IDs) to receive events for
(for market channel)
type string id of channel to subscribe to (USER or MARKET)
custom_feature_enabled bool enabling / disabling custom features
Where the auth field is of type Auth which has the form described in the WSS
Authentication section below.
Subscribe to more assets
Once connected, the client can subscribe and unsubscribe to asset_ids by sending the

### following message

Field Type Description
assets_ids string[] array of asset ids (token IDs) to receive events for
(for market channel)
markets string[] array of market ids (condition IDs) to receive events
for (for user channel)
operation string ”subscribe” or “unsubscribe”
custom_feature_enabled bool enabling / disabling custom features

WSS Quickstart
The following code samples and explanation will show you how to subscribe to the Marker
and User channels of the Websocket. You’ll need your API keys to do this so we’ll start with
that.
Getting your API Keys
DeriveAPIKeys-Python
```python
from py_clob_client.client import ClobClient
host: str = "https://clob.polymarket.com"
key: str = "" #This is your Private Key. If using email login export from
https://reveal.magic.link/polymarket otherwise export from your Web3 Application
chain_id: int = 137 #No need to adjust this
POLYMARKET_PROXY_ADDRESS: str = '' #This is the address you deposit/send USDC to to
```
FUND your Polymarket account.
#Select from the following 3 initialization options to matches your login method, and
remove any unused lines so only one client is initialized.
### Initialization of a client using a Polymarket Proxy associated with an Email/Magic
account. If you login with your email use this example.
client = ClobClient(host, key=key, chain_id=chain_id, signature_type=1,
funder=POLYMARKET_PROXY_ADDRESS)
### Initialization of a client using a Polymarket Proxy associated with a Browser
Wallet(Metamask, Coinbase Wallet, etc)
client = ClobClient(host, key=key, chain_id=chain_id, signature_type=2,
funder=POLYMARKET_PROXY_ADDRESS)
### Initialization of a client that trades directly from an EOA.
client = ClobClient(host, key=key, chain_id=chain_id)
print( client.derive_api_key() )
DeriveAPIKeys-TS
//npm install @polymarket/clob-client
//npm install ethers
//Client initialization example and dumping API Keys
```python
import {ClobClient, ApiKeyCreds } from "@polymarket/clob-client";
import { Wallet } from "@ethersproject/wallet";
const host = 'https://clob.polymarket.com';
```
const signer = new Wallet("YourPrivateKey"); //This is your Private Key. If using
email login export from https://reveal.magic.link/polymarket otherwise export from
your Web3 Application

// Initialize the clob client
// NOTE: the signer must be approved on the CTFExchange contract
const clobClient = new ClobClient(host, 137, signer);
(async () => {
const apiKey = await clobClient.deriveApiKey();
console.log(apiKey);
})();
Using those keys to connect to the Market or User Websocket
WSS-Connection
```python
from websocket import WebSocketApp
import json
import time
import threading
MARKET_CHANNEL = "market"
USER_CHANNEL = "user"
class WebSocketOrderBook:
def __init__(self, channel_type, url, data, auth, message_callback, verbose):
self.channel_type = channel_type
self.url = url
self.data = data
self.auth = auth
self.message_callback = message_callback
self.verbose = verbose
furl = url + "/ws/" + channel_type
```
self.ws = WebSocketApp(
furl,
on_message=self.on_message,
on_error=self.on_error,
on_close=self.on_close,
on_open=self.on_open,
)
self.orderbooks = {}

### def on_message(self, ws, message)

print(message)
pass

### def on_error(self, ws, error)

print("Error: ", error)
exit(1)
def on_close(self, ws, close_status_code, close_msg):
print("closing")

exit(0)

### def on_open(self, ws)


### if self.channel_type == MARKET_CHANNEL

ws.send(json.dumps({"assets_ids": self.data, "type": MARKET_CHANNEL}))
elif self.channel_type == USER_CHANNEL and self.auth:
ws.send(
json.dumps(
{"markets": self.data, "type": USER_CHANNEL, "auth": self.auth}
)
)

### else

exit(1)
thr = threading.Thread(target=self.ping, args=(ws,))
thr.start()

### def subscribe_to_tokens_ids(self, assets_ids)


### if self.channel_type == MARKET_CHANNEL

self.ws.send(json.dumps({"assets_ids": assets_ids, "operation":
"subscribe"}))

### def unsubscribe_to_tokens_ids(self, assets_ids)


### if self.channel_type == MARKET_CHANNEL

self.ws.send(json.dumps({"assets_ids": assets_ids, "operation":
"unsubscribe"}))

### def ping(self, ws)


### while True

ws.send("PING")
time.sleep(10)

### def run(self)

self.ws.run_forever()

### if __name__ == "__main__"

url = "wss://ws-subscriptions-clob.polymarket.com"
#Complete these by exporting them from your initialized client.
api_key = ""
api_secret = ""
api_passphrase = ""
asset_ids = [
"109681959945973300464568698402968596289258214226684818748321941747028805721376",
]
condition_ids = [] # no really need to filter by this one
auth = {"apiKey": api_key, "secret": api_secret, "passphrase": api_passphrase}

market_connection = WebSocketOrderBook(
MARKET_CHANNEL, url, asset_ids, auth, None, True
)
user_connection = WebSocketOrderBook(
USER_CHANNEL, url, condition_ids, auth, None, True
)
market_connection.subscribe_to_tokens_ids(["123"])
# market_connection.unsubscribe_to_tokens_ids(["123"])
market_connection.run()
# user_connection.run()
# WSS Authentication
Only connections to user channel require authentication.
Field Optional Description
apikey yes Polygon account’s CLOB api key
secret yes Polygon account’s CLOB api secret
passphrase yes Polygon account’s CLOB api passphrase
User Channel
Authenticated channel for updates related to user activities (orders, trades), filtered for
authenticated user by apikey.

## Subscribe

<wss-channel> user
Trade Message

### Emitted when

when a market order is matched (“MATCHED”)
when a limit order for the user is included in a trade (“MATCHED”)
subsequent status changes for trade (“MINED”, “CONFIRMED”, “RETRYING”, “FAILED”)
Structure
Name Type Description
asset_id string asset id (token ID) of order (market order)
event_type string ”trade”
id string trade id

Name Type Description
last_update string time of last update to trade
maker_orders MakerOrder[] array of maker order details
market string market identifier (condition ID)
matchtime string time trade was matched
outcome string outcome
owner string api key of event owner
price string price
side string BUY/SELL
size string size
status string trade status
taker_order_id string id of taker order
timestamp string time of event
trade_owner string api key of trade owner
type string ”TRADE”

### Where a MakerOrder object is of the form

Name Type Description
asset_id string asset of the maker order
matched_amount string amount of maker order matched in trade
order_id string maker order ID
outcome string outcome
owner string owner of maker order
price string price of maker order
Response
{

### "asset_id"

"52114319501245915516055106046884209969926127482827954674443846427813813222426",
"event_type": "trade",
"id": "28c4d2eb-bbea-40e7-a9f0-b2fdb56b2c2e",
"last_update": "1672290701",
"maker_orders": [
{

### "asset_id"

"52114319501245915516055106046884209969926127482827954674443846427813813222426",
"matched_amount": "10",


### "order_id"

"0xff354cd7ca7539dfa9c28d90943ab5779a4eac34b9b37a757d7b32bdfb11790b",
"outcome": "YES",
"owner": "9180014b-33c8-9240-a14b-bdca11c0a465",
"price": "0.57"
}
],
"market": "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
"matchtime": "1672290701",
"outcome": "YES",
"owner": "9180014b-33c8-9240-a14b-bdca11c0a465",
"price": "0.57",
"side": "BUY",
"size": "10",
"status": "MATCHED",

### "taker_order_id"

"0x06bc63e346ed4ceddce9efd6b3af37c8f8f440c92fe7da6b2d0f9e4ccbc50c42",
"timestamp": "1672290701",
"trade_owner": "9180014b-33c8-9240-a14b-bdca11c0a465",
"type": "TRADE"
}
Order Message

### Emitted when

When an order is placed (PLACEMENT)
When an order is updated (some of it is matched) (UPDATE)
When an order is canceled (CANCELLATION)
Structure
Name Type Description
asset_id string asset ID (token ID) of order
associate_trades string[] array of ids referencing trades that the order has been
included in
event_type string ”order”
id string order id
market string condition ID of market
order_owner string owner of order
original_size string original order size
outcome string outcome
owner string owner of orders
price string price of order

Name Type Description
side string BUY/SELL
size_matched string size of order that has been matched
timestamp string time of event
type string PLACEMENT/UPDATE/CANCELLATION
Response
{

### "asset_id"

"52114319501245915516055106046884209969926127482827954674443846427813813222426",
"associate_trades": null,
"event_type": "order",
"id": "0xff354cd7ca7539dfa9c28d90943ab5779a4eac34b9b37a757d7b32bdfb11790b",
"market": "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
"order_owner": "9180014b-33c8-9240-a14b-bdca11c0a465",
"original_size": "10",
"outcome": "YES",
"owner": "9180014b-33c8-9240-a14b-bdca11c0a465",
"price": "0.57",
"side": "SELL",
"size_matched": "0",
"timestamp": "1672290687",
"type": "PLACEMENT"
}
Market Channel
Public channel for updates related to market updates (level 2 price data).

## Subscribe

<wss-channel> market
book Message

### Emitted When

First subscribed to a market
When there is a trade that affects the book
Structure
Name Type Description
event_type string ”book”
asset_id string asset ID (token ID)

Name Type Description
market string condition ID of market
timestamp string unix timestamp the current book generation in
milliseconds (1/1,000 second)
hash string hash summary of the orderbook content
buys OrderSummary[] list of type (size, price) aggregate book levels for buys
sells OrderSummary[] list of type (size, price) aggregate book levels for sells

### Where a OrderSummary object is of the form

Name Type Description
price string size available at that price level
size string price of the orderbook level
Response
{
"event_type": "book",

### "asset_id"

"65818619657568813474341868652308942079804919287380422192892211131408793125422",
"market": "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
"bids": [
{ "price": ".48", "size": "30" },
{ "price": ".49", "size": "20" },
{ "price": ".50", "size": "15" }
],
"asks": [
{ "price": ".52", "size": "25" },
{ "price": ".53", "size": "60" },
{ "price": ".54", "size": "10" }
],
"timestamp": "123456789000",
"hash": "0x0...."
}
price_change Message
⚠ Breaking Change Notice: The price_change message schema will be updated on
September 15, 2025 at 11 PM UTC. Please see the migration guide for details.

### Emitted When

A new order is placed
An order is cancelled

Structure
Name Type Description
event_type string ”price_change”
market string condition ID of market
price_changes PriceChange[] array of price change objects
timestamp string unix timestamp in milliseconds

### Where a PriceChange object is of the form

Name Type Description
asset_id string asset ID (token ID)
price string price level affected
size string new aggregate size for price level
side string ”BUY” or “SELL”
hash string hash of the order
best_bid string current best bid price
best_ask string current best ask price
Response
{
"market": "0x5f65177b394277fd294cd75650044e32ba009a95022d88a0c1d565897d72f8f1",
"price_changes": [
{

### "asset_id"

"71321045679252212594626385532706912750332728571942532289631379312455583992563",
"price": "0.5",
"size": "200",
"side": "BUY",
"hash": "56621a121a47ed9333273e21c83b660cff37ae50",
"best_bid": "0.5",
"best_ask": "1"
},
{

### "asset_id"

"52114319501245915516055106046884209969926127482827954674443846427813813222426",
"price": "0.5",
"size": "200",
"side": "SELL",
"hash": "1895759e4df7a796bf4f1c5a5950b748306923e2",
"best_bid": "0",
"best_ask": "0.5"

}
],
"timestamp": "1757908892351",
"event_type": "price_change"
}
tick_size_change Message

### Emitted When

The minimum tick size of the market changes. This happens when the book’s price
reaches the limits: price > 0.96 or price < 0.04
Structure
Name Type Description
event_type string ”price_change”
asset_id string asset ID (token ID)
market string condition ID of market
old_tick_size string previous minimum tick size
new_tick_size string current minimum tick size
side string buy/sell
timestamp string time of event
Response
{
"event_type": "tick_size_change",

### "asset_id"

"65818619657568813474341868652308942079804919287380422192892211131408793125422",\
"market": "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
"old_tick_size": "0.01",
"new_tick_size": "0.001",
"timestamp": "100000000"
}
last_trade_price Message

### Emitted When

When a maker and taker order is matched creating a trade event.
Response

{
"asset_id":"11412207150964437967801872790870956022661814800337144611011450980660149307
1694",
"event_type":"last_trade_price",
"fee_rate_bps":"0",
"market":"0x6a67b9d828d53862160e470329ffea5246f338ecfffdf2cab45211ec578b0347",
"price":"0.456",
"side":"BUY",
"size":"219.217767",
"timestamp":"1750428146322"
}
best_bid_ask Message

### Emitted When

The best bid and ask prices for a market change.
(This message is behind the custom_feature_enabled flag)
Structure
Name Type Description
event_type string ”best_bid_ask”
market string condition ID of market
asset_id string asset ID (token ID)
best_bid string current best bid price
best_ask string current best ask price
spread string spread between best bid and ask
timestamp string unix timestamp in milliseconds
Example
Response
{
"event_type": "best_bid_ask",
"market": "0x0005c0d312de0be897668695bae9f32b624b4a1ae8b140c49f08447fcc74f442",

### "asset_id"

"85354956062430465315924116860125388538595433819574542752031640332592237464430",
"best_bid": "0.73",
"best_ask": "0.77",
"spread": "0.04",
"timestamp": "1766789469958"
}

new_market Message

### Emitted When

A new market is created.
(This message is behind the custom_feature_enabled flag)
Structure
Name Type Description
id string market ID
question string market question
market string condition ID of market
slug string market slug
description string market description
assets_ids string[] list of asset IDs
outcomes string[] list of outcomes
event_message object event message object
timestamp string unix timestamp in milliseconds
event_type string ”new_market”

### Where a EventMessage object is of the form

Name Type Description
id string event message ID
ticker string event message ticker
slug string event message slug
title string event message title
description string event message description
Example
Response
{
"id": "1031769",
"question": "Will NVIDIA (NVDA) close above $240 end of January?",
"market": "0x311d0c4b6671ab54af4970c06fcf58662516f5168997bdda209ec3db5aa6b0c1",
"slug": "nvda-above-240-on-january-30-2026",

"description": "This market will resolve to \"Yes\" if the official closing price
for NVIDIA (NVDA) on the final trading day of January 2026 is higher than the listed
price. Otherwise, this market will resolve to \"No\".\n\nIf the final trading day of
the month is shortened (for example, due to a market-holiday schedule), the official
closing price published for that shortened session will still be used for
resolution.\n\nIf no official closing price is published for that session (for
example, due to a trading halt into the close, system issue, or other disruption), the
market will use the last valid on-exchange trade price of the regular session as the
effective closing price.\n\nThe resolution source for this market is Yahoo Finance —
specifically, the NVIDIA (NVDA) \"Close\" prices available at
https://finance.yahoo.com/quote/NVDA/history, published under \"Historical
Prices.\"\n\nIn the event of a stock split, reverse stock split, or similar corporate
action affecting the listed company during the listed time frame, this market will
resolve based on split-adjusted prices as displayed on Yahoo Finance.",
"assets_ids": [
"76043073756653678226373981964075571318267289248134717369284518995922789326425",
"31690934263385727664202099278545688007799199447969475608906331829650099442770"
],
"outcomes": [
"Yes",
"No"
],
"event_message": {
"id": "125819",
"ticker": "nvda-above-in-january-2026",
"slug": "nvda-above-in-january-2026",
"title": "Will NVIDIA (NVDA) close above ___ end of January?",
"description": "This market will resolve to \"Yes\" if the official closing
price for NVIDIA (NVDA) on the final trading day of January 2026 is higher than the
listed price. Otherwise, this market will resolve to \"No\".\n\nIf the final trading
day of the month is shortened (for example, due to a market-holiday schedule), the
official closing price published for that shortened session will still be used for
resolution.\n\nIf no official closing price is published for that session (for
example, due to a trading halt into the close, system issue, or other disruption), the
market will use the last valid on-exchange trade price of the regular session as the
effective closing price.\n\nThe resolution source for this market is Yahoo Finance —
specifically, the NVIDIA (NVDA) \"Close\" prices available at
https://finance.yahoo.com/quote/NVDA/history, published under \"Historical
Prices.\"\n\nIn the event of a stock split, reverse stock split, or similar corporate
action affecting the listed company during the listed time frame, this market will
resolve based on split-adjusted prices as displayed on Yahoo Finance."
},
"timestamp": "1766790415550",
"event_type": "new_market"
}
market_resolved Message

### Emitted When


A market is resolved.
(This message is behind the custom_feature_enabled flag)
Structure
Name Type Description
id string market ID
question string market question
market string condition ID of market
slug string market slug
description string market description
assets_ids string[] list of asset IDs
outcomes string[] list of outcomes
winning_asset_id string winning asset ID
winning_outcome string winning outcome
event_message object event message object
timestamp string unix timestamp in milliseconds
event_type string ”market_resolved”

### Where a EventMessage object is of the form

Name Type Description
id string event message ID
ticker string event message ticker
slug string event message slug
title string event message title
description string event message description
Example
Response
{
"id": "1031769",
"question": "Will NVIDIA (NVDA) close above $240 end of January?",
"market": "0x311d0c4b6671ab54af4970c06fcf58662516f5168997bdda209ec3db5aa6b0c1",
"slug": "nvda-above-240-on-january-30-2026",
"description": "This market will resolve to \"Yes\" if the official closing price
for NVIDIA (NVDA) on the final trading day of January 2026 is higher than the listed

price. Otherwise, this market will resolve to \"No\".\n\nIf the final trading day of
the month is shortened (for example, due to a market-holiday schedule), the official
closing price published for that shortened session will still be used for
resolution.\n\nIf no official closing price is published for that session (for
example, due to a trading halt into the close, system issue, or other disruption), the
market will use the last valid on-exchange trade price of the regular session as the
effective closing price.\n\nThe resolution source for this market is Yahoo Finance —
specifically, the NVIDIA (NVDA) \"Close\" prices available at
https://finance.yahoo.com/quote/NVDA/history, published under \"Historical
Prices.\"\n\nIn the event of a stock split, reverse stock split, or similar corporate
action affecting the listed company during the listed time frame, this market will
resolve based on split-adjusted prices as displayed on Yahoo Finance.",
"assets_ids": [
"76043073756653678226373981964075571318267289248134717369284518995922789326425",
"31690934263385727664202099278545688007799199447969475608906331829650099442770"
],

### "winning_asset_id"

"76043073756653678226373981964075571318267289248134717369284518995922789326425",
"winning_outcome": "Yes",
"event_message": {
"id": "125819",
"ticker": "nvda-above-in-january-2026",
"slug": "nvda-above-in-january-2026",
"title": "Will NVIDIA (NVDA) close above ___ end of January?",
"description": "This market will resolve to \"Yes\" if the official closing
price for NVIDIA (NVDA) on the final trading day of January 2026 is higher than the
listed price. Otherwise, this market will resolve to \"No\".\n\nIf the final trading
day of the month is shortened (for example, due to a market-holiday schedule), the
official closing price published for that shortened session will still be used for
resolution.\n\nIf no official closing price is published for that session (for
example, due to a trading halt into the close, system issue, or other disruption), the
market will use the last valid on-exchange trade price of the regular session as the
effective closing price.\n\nThe resolution source for this market is Yahoo Finance —
specifically, the NVIDIA (NVDA) \"Close\" prices available at
https://finance.yahoo.com/quote/NVDA/history, published under \"Historical
Prices.\"\n\nIn the event of a stock split, reverse stock split, or similar corporate
action affecting the listed company during the listed time frame, this market will
resolve based on split-adjusted prices as displayed on Yahoo Finance."
},
"timestamp": "1766790415550",
"event_type": "new_market"
}
Real Time Data Stream
Real Time Data Socket
Overview

The Polymarket Real-Time Data Socket (RTDS) is a WebSocket-based streaming service
that provides real-time updates for various Polymarket data streams. The service allows
clients to subscribe to multiple data feeds simultaneously and receive live updates as events
occur on the platform.
Polymarket provides a Typescript client for interacting with this streaming service. Download
and view it’s documentation here
Connection Details
WebSocket URL: wss://ws-live-data.polymarket.com
Protocol: WebSocket
Data Format: JSON
Authentication
The RTDS supports two types of authentication depending on the subscription type:
1. CLOB Authentication: Required for certain trading-related subscriptions
key : API key
secret : API secret
passphrase : API passphrase
2. Gamma Authentication: Required for user-specific data
address : User wallet address
Connection Management

### The WebSocket connection supports

Dynamic Subscriptions: Without disconnecting from the socket users can add, remove
and modify topics and filters they are subscribed to.
Ping/Pong: You should send PING messages (every 5 seconds ideally) to maintain
connection
Available Subscription Types
Although this connection technically supports additional activity and subscription types, they
are not fully supported at this time. Users are free to use them but there may be some
unexpected behavior.
The RTDS currently supports the following subscription types:
1. Crypto Prices - Real-time cryptocurrency price updates
2. Comments - Comment-related events including reactions
Message Structure

All messages received from the WebSocket follow this structure:
{
"topic": "string",
"type": "string",
"timestamp": "number",
"payload": "object"
}
topic : The subscription topic (e.g., “crypto_prices”, “comments”, “activity”)
type : The message type/event (e.g., “update”, “reaction_created”, “orders_matched”)
timestamp : Unix timestamp in milliseconds
payload : Event-specific data object
Subscription Management
Subscribe to Topics
To subscribe to data streams, send a JSON message with this structure:
{
"action": "subscribe",
"subscriptions": [
{
"topic": "topic_name",
"type": "message_type",
"filters": "optional_filter_string",
"clob_auth": {
"key": "api_key",
"secret": "api_secret",
"passphrase": "api_passphrase"
},
"gamma_auth": {
"address": "wallet_address"
}
}
]
}
Unsubscribe from Topics
To unsubscribe from data streams, send a similar message with "action": "unsubscribe" .
Error Handling
Connection errors will trigger automatic reconnection attempts
Invalid subscription messages may result in connection closure
Authentication failures will prevent successful subscription to protected topics

RTDS Crypto Prices
Polymarket provides a Typescript client for interacting with this streaming service. Download
and view it’s documentation here
Overview
The crypto prices subscription provides real-time updates for cryptocurrency price data from

### two different sources

Binance Source ( crypto_prices ): Real-time price data from Binance exchange
Chainlink Source ( crypto_prices_chainlink ): Price data from Chainlink oracle networks
Both streams deliver current market prices for various cryptocurrency trading pairs, but use
different symbol formats and subscription structures.
Binance Source (crypto_prices)
Subscription Details
Topic: crypto_prices
Type: update
Authentication: Not required
Filters: Optional (specific symbols can be filtered)
Symbol Format: Lowercase concatenated pairs (e.g., solusdt , btcusdt )
Subscription Message
{
"action": "subscribe",
"subscriptions": [
{
"topic": "crypto_prices",
"type": "update"
}
]
}
With Symbol Filter
To subscribe to specific cryptocurrency symbols, include a filters parameter:
{
"action": "subscribe",
"subscriptions": [
{
"topic": "crypto_prices",
"type": "update",

"filters": "solusdt,btcusdt,ethusdt"
}
]
}
Chainlink Source (crypto_prices_chainlink)
Subscription Details
Topic: crypto_prices_chainlink
Type: * (all types)
Authentication: Not required
Filters: Optional (JSON object with symbol specification)
Symbol Format: Slash-separated pairs (e.g., eth/usd , btc/usd )
Subscription Message
{
"action": "subscribe",
"subscriptions": [
{
"topic": "crypto_prices_chainlink",
"type": "*",
"filters": ""
}
]
}
With Symbol Filter
To subscribe to specific cryptocurrency symbols, include a JSON filters parameter:
{
"action": "subscribe",
"subscriptions": [
{
"topic": "crypto_prices_chainlink",
"type": "*",
"filters": "{\"symbol\":\"eth/usd\"}"
}
]
}
Message Format
Binance Source Message Format

When subscribed to Binance crypto prices ( crypto_prices ), you’ll receive messages with the

### following structure

{
"topic": "crypto_prices",
"type": "update",
"timestamp": 1753314064237,
"payload": {
"symbol": "solusdt",
"timestamp": 1753314064213,
"value": 189.55
}
}
Chainlink Source Message Format
When subscribed to Chainlink crypto prices ( crypto_prices_chainlink ), you’ll receive messages

### with the following structure

{
"topic": "crypto_prices_chainlink",
"type": "update",
"timestamp": 1753314064237,
"payload": {
"symbol": "eth/usd",
"timestamp": 1753314064213,
"value": 3456.78
}
}
Payload Fields
Field Type Description
symbol string Trading pair symbol
Binance: lowercase concatenated (e.g., “solusdt”, “btcusdt”)
Chainlink: slash-separated (e.g., “eth/usd”, “btc/usd”)
timestamp number Price timestamp in Unix milliseconds
value number Current price value in the quote currency
Example Messages
Binance Source Examples
Solana Price Update (Binance)

{
"topic": "crypto_prices",
"type": "update",
"timestamp": 1753314064237,
"payload": {
"symbol": "solusdt",
"timestamp": 1753314064213,
"value": 189.55
}
}
Bitcoin Price Update (Binance)
{
"topic": "crypto_prices",
"type": "update",
"timestamp": 1753314088421,
"payload": {
"symbol": "btcusdt",
"timestamp": 1753314088395,
"value": 67234.50
}
}
Chainlink Source Examples
Ethereum Price Update (Chainlink)
{
"topic": "crypto_prices_chainlink",
"type": "update",
"timestamp": 1753314064237,
"payload": {
"symbol": "eth/usd",
"timestamp": 1753314064213,
"value": 3456.78
}
}
Bitcoin Price Update (Chainlink)
{
"topic": "crypto_prices_chainlink",
"type": "update",
"timestamp": 1753314088421,
"payload": {
"symbol": "btc/usd",
"timestamp": 1753314088395,
"value": 67234.50

}
}
Supported Symbols
Binance Source Symbols
The Binance source supports various cryptocurrency trading pairs using lowercase

### concatenated format

btcusdt - Bitcoin to USDT
ethusdt - Ethereum to USDT
solusdt - Solana to USDT
xrpusdt - XRP to USDT
Chainlink Source Symbols
The Chainlink source supports cryptocurrency trading pairs using slash-separated format:
btc/usd - Bitcoin to USD
eth/usd - Ethereum to USD
sol/usd - Solana to USD
xrp/usd - XRP to USD
Notes
General
Price updates are sent as market prices change
The timestamp in the payload represents when the price was recorded
The outer timestamp represents when the message was sent via WebSocket
No authentication is required for crypto price data
RTDS Comments
Polymarket provides a Typescript client for interacting with this streaming service. Download
and view it’s documentation here
Overview
The comments subscription provides real-time updates for comment-related events on the
Polymarket platform. This includes new comments being created, as well as other comment
interactions like reactions and replies.
Subscription Details
Topic: comments

Type: comment_created (and potentially other comment event types like reaction_created )
Authentication: May require Gamma authentication for user-specific data
Filters: Optional (can filter by specific comment IDs, users, or events)
Subscription Message
{
"action": "subscribe",
"subscriptions": [
{
"topic": "comments",
"type": "comment_created"
}
]
}
Message Format
When subscribed to comments, you’ll receive messages with the following structure:
{
"topic": "comments",
"type": "comment_created",
"timestamp": 1753454975808,
"payload": {
"body": "do you know what the term encircle means? it means to surround from all
sides, Russia has present on only 1 side, that's the opposite of an encirclement",
"createdAt": "2025-07-25T14:49:35.801298Z",
"id": "1763355",
"parentCommentID": "1763325",
"parentEntityID": 18396,
"parentEntityType": "Event",
"profile": {
"baseAddress": "0xce533188d53a16ed580fd5121dedf166d3482677",
"displayUsernamePublic": true,
"name": "salted.caramel",
"proxyWallet": "0x4ca749dcfa93c87e5ee23e2d21ff4422c7a4c1ee",
"pseudonym": "Adored-Disparity"
},
"reactionCount": 0,
"replyAddress": "0x0bda5d16f76cd1d3485bcc7a44bc6fa7db004cdd",
"reportCount": 0,
"userAddress": "0xce533188d53a16ed580fd5121dedf166d3482677"
}
}
Message Types
comment_created

Triggered when a user creates a new comment on an event or in reply to another comment.
comment_removed
Triggered when a comment is removed or deleted.
reaction_created
Triggered when a user adds a reaction to an existing comment.
reaction_removed
Triggered when a reaction is removed from a comment.
Payload Fields
Field Type Description
body string The text content of the comment
createdAt string ISO 8601 timestamp when the comment was created
id string Unique identifier for this comment
parentCommentID string ID of the parent comment if this is a reply (null for top-level
comments)
parentEntityID number ID of the parent entity (event, market, etc.)
parentEntityType string Type of parent entity (e.g., “Event”, “Market”)
profile object Profile information of the user who created the comment
reactionCount number Current number of reactions on this comment
replyAddress string Polygon address for replies (may be different from
userAddress)
reportCount number Current number of reports on this comment
userAddress string Polygon address of the user who created the comment
Profile Object Fields
Field Type Description
baseAddress string User profile address
displayUsernamePublic boolean Whether the username should be displayed publicly
name string User’s display name
proxyWallet string Proxy wallet address used for transactions
pseudonym string Generated pseudonym for the user

Parent Entity Types

### The following parent entity types are supported

Event - Comments on prediction events
Market - Comments on specific markets
Additional entity types may be available
Example Messages
New Comment Created
{
"topic": "comments",
"type": "comment_created",
"timestamp": 1753454975808,
"payload": {
"body": "do you know what the term encircle means? it means to surround from all
sides, Russia has present on only 1 side, that's the opposite of an encirclement",
"createdAt": "2025-07-25T14:49:35.801298Z",
"id": "1763355",
"parentCommentID": "1763325",
"parentEntityID": 18396,
"parentEntityType": "Event",
"profile": {
"baseAddress": "0xce533188d53a16ed580fd5121dedf166d3482677",
"displayUsernamePublic": true,
"name": "salted.caramel",
"proxyWallet": "0x4ca749dcfa93c87e5ee23e2d21ff4422c7a4c1ee",
"pseudonym": "Adored-Disparity"
},
"reactionCount": 0,
"replyAddress": "0x0bda5d16f76cd1d3485bcc7a44bc6fa7db004cdd",
"reportCount": 0,
"userAddress": "0xce533188d53a16ed580fd5121dedf166d3482677"
}
}
Reply to Existing Comment
{
"topic": "comments",
"type": "comment_created",
"timestamp": 1753454985123,
"payload": {
"body": "That's a good point about the definition of encirclement.",
"createdAt": "2025-07-25T14:49:45.120000Z",
"id": "1763356",
"parentCommentID": "1763355",
"parentEntityID": 18396,

"parentEntityType": "Event",
"profile": {
"baseAddress": "0x1234567890abcdef1234567890abcdef12345678",
"displayUsernamePublic": true,
"name": "trader",
"proxyWallet": "0x9876543210fedcba9876543210fedcba98765432",
"pseudonym": "Bright-Analysis"
},
"reactionCount": 0,
"replyAddress": "0x0bda5d16f76cd1d3485bcc7a44bc6fa7db004cdd",
"reportCount": 0,
"userAddress": "0x1234567890abcdef1234567890abcdef12345678"
}
}
Comment Hierarchy

### Comments support nested threading

Top-level comments: parentCommentID is null or empty
Reply comments: parentCommentID contains the ID of the parent comment
All comments are associated with a parentEntityID and parentEntityType
Use Cases
Real-time comment feed displays
Discussion thread monitoring
Community sentiment analysis
Content
Comments include reactionCount and reportCount
Comment body contains the full text content
Notes
The createdAt timestamp uses ISO 8601 format with timezone information
The outer timestamp field represents when the WebSocket message was sent
User profiles include both primary addresses and proxy wallet addresses
Gamma Structure
Overview
All market data necessary for market resolution is available on-chain (ie ancillaryData in
UMA 00 request), but Polymarket also provides a hosted service, Gamma, that indexes this
data and provides additional market metadata (ie categorization, indexed volume, etc). This
service is made available through a REST API. For public users, this resource read only and

can be used to fetch useful information about markets for things like non-profit research
projects, alternative trading interfaces, automated trading systems etc.
Endpoint
https://gamma-api.polymarket.com
Gamma Structure
Gamma provides some organizational models. These include events, and markets. The
most fundamental element is always markets and the other models simply provide additional
organization.
Detail
1. Market
1. Contains data related to a market that is traded on. Maps onto a pair of clob token
ids, a market address, a question id and a condition id
2. Event
2. Contains a set of markets

### 3. Variants

1. Event with 1 market (i.e., resulting in an SMP)
2. Event with 2 or more markets (i.e., resulting in an GMP)
Example
[Event] Where will Barron Trump attend College?
[Market] Will Barron attend Georgetown?
[Market] Will Barron attend NYU?
[Market] Will Barron attend UPenn?
[Market] Will Barron attend Harvard?
[Market] Will Barron attend another college?
How to Fetch Markets
Both the getEvents and getMarkets are paginated. See pagination section for details.
This guide covers the three recommended approaches for fetching market data from the
Gamma API, each optimized for different use cases.
Overview
There are three main strategies for retrieving market data:
1. By Slug - Best for fetching specific individual markets or events
2. By Tags - Ideal for filtering markets by category or sport

3. Via Events Endpoint - Most efficient for retrieving all active markets
1. Fetch by Slug
Use Case: When you need to retrieve a specific market or event that you already know
about.Individual markets and events are best fetched using their unique slug identifier. The
slug can be found directly in the Polymarket frontend URL.
How to Extract the Slug
```python
From any Polymarket URL, the slug is the path segment after /event/ or /market/ :
https://polymarket.com/event/fed-decision-in-october?tid=1758818660485
```
↑
Slug: fed-decision-in-october
API Endpoints
For Events: GET /events/slug/
For Markets: GET /markets/slug/
Examples
```bash
curl "https://gamma-api.polymarket.com/events/slug/fed-decision-in-october"
2. Fetch by Tags
Use Case: When you want to filter markets by category, sport, or topic.Tags provide a
powerful way to categorize and filter markets. You can discover available tags and then use
them to filter your market requests.
Discover Available Tags
General Tags: GET /tags
Sports Tags & Metadata: GET /sports
```
The /sports endpoint returns comprehensive metadata for sports including tag IDs, images,
resolution sources, and series information.
Using Tags in Market Requests
Once you have tag IDs, you can use them with the tag_id parameter in both markets and
events endpoints.

Markets with Tags: GET /markets
Events with Tags: GET /events
```bash
curl "https://gamma-api.polymarket.com/events?tag_id=100381&limit=1&closed=false"
Additional Tag Filtering
You can also:
Use related_tags=true to include related tag markets
Exclude specific tags with exclude_tag_id
3. Fetch All Active Markets
Use Case: When you need to retrieve all available active markets, typically for broader
analysis or market discovery.
The most efficient approach is to use the /events endpoint and work backwards, as events
contain their associated markets.
Events Endpoint: GET /events
Markets Endpoint: GET /markets
Key Parameters
order=id - Order by event ID
ascending=false - Get newest events first
closed=false - Only active markets
limit - Control response size
offset - For pagination
Examples
curl "https://gamma-api.polymarket.com/events?
order=id&ascending=false&closed=false&limit=100"
```
This approach gives you all active markets ordered from newest to oldest, allowing you to
systematically process all available trading opportunities.
Pagination
For large datasets, use pagination with limit and offset parameters:
limit=50 - Return 50 results per page
offset=0 - Start from the beginning (increment by limit for subsequent pages)


### Pagination Examples

# Page 1: First 50 results (offset=0)
```bash
curl "https://gamma-api.polymarket.com/events?
order=id&ascending=false&closed=false&limit=50&offset=0"
```
# Page 2: Next 50 results (offset=50)
```bash
curl "https://gamma-api.polymarket.com/events?
order=id&ascending=false&closed=false&limit=50&offset=50"
```
# Page 3: Next 50 results (offset=100)
```bash
curl "https://gamma-api.polymarket.com/events?
order=id&ascending=false&closed=false&limit=50&offset=100"
```
# Paginating through markets with tag filtering
```bash
curl "https://gamma-api.polymarket.com/markets?
tag_id=100381&closed=false&limit=25&offset=0"
```
# Next page of markets with tag filtering
```bash
curl "https://gamma-api.polymarket.com/markets?
tag_id=100381&closed=false&limit=25&offset=25"
```
Best Practices
1. For Individual Markets: Always use the slug method for best performance
2. For Category Browsing: Use tag filtering to reduce API calls
3. For Complete Market Discovery: Use the events endpoint with pagination
4. Always Include closed=false : Unless you specifically need historical data
5. Implement Rate Limiting: Respect API limits for production applications
Related Endpoints
Get Markets - Full markets endpoint documentation
Get Events - Full events endpoint documentation
Search Markets - Search functionality
Gamma API Health check
GET/status
Gamma API Health check
```bash
cURL

curl --request GET \
--url https://gamma-api.polymarket.com/status
Python
import requests
url = "https://gamma-api.polymarket.com/status"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/status', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/status",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}

Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/status"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-api.polymarket.com/status")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/status")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
"OK"

Response
200 - text/plain
OK
The response is of type string .

### Example

"OK"
Sports
List teams
GET/teams
List teams
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/teams
Python
import requests
url = "https://gamma-api.polymarket.com/teams"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/teams', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP

<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/teams",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/teams"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java

HttpResponse<String> response = Unirest.get("https://gamma-api.polymarket.com/teams")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/teams")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"id": 123,
"name": "<string>",
"league": "<string>",
"record": "<string>",
"logo": "<string>",
"abbreviation": "<string>",
"alias": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
]
Query Parameters
Query Parameters
limit
integer
Required range: x >= 0
offset
integer
Required range: x >= 0

order
string
Comma-separated list of fields to order by
ascending
boolean
league
string[]
name
string[]
abbreviation
string[]
Response
200 - application/json
List of teams
id
integer
name
string | null

league
string | null
record
string | null
logo
string | null
abbreviation
string | null
alias
string | null
createdAt
string` | null
updatedAt
string` | null
Get sports metadata information
Retrieves metadata for various sports including images, resolution sources, ordering
preferences, tags, and series information. This endpoint provides comprehensive sport
configuration data used throughout the platform.

GET/sports
Get sports metadata information
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/sports
Python
import requests
url = "https://gamma-api.polymarket.com/sports"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/sports', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/sports",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```

echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/sports"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-api.polymarket.com/sports")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/sports")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body

200
[
{
"sport": "<string>",
"image": "<string>",
"resolution": "<string>",
"ordering": "<string>",
"tags": "<string>",
"series": "<string>"
}
]
Response
200 - application/json
List of sports metadata objects containing sport configuration details, visual assets, and
related identifiers
sport
string
The sport identifier or abbreviation
image
string`
URL to the sport's logo or image asset
resolution
string`
URL to the official resolution source for the sport (e.g., league website)
ordering

string
Preferred ordering for sport display, typically "home" or "away"
tags
string
Comma-separated list of tag IDs associated with the sport for categorization and filtering
series
string
Series identifier linking the sport to a specific tournament or season series
Get valid sports market types
Get a list of all valid sports market types available on the platform. Use these values when
filtering markets by the sportsMarketTypes parameter.
GET/sports/market-types
Get valid sports market types
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/sports/market-types
Python
import requests
url = "https://gamma-api.polymarket.com/sports/market-types"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/sports/market-types', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));

PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/sports/market-types",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/sports/market-types"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}

Java
HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/sports/market-types")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/sports/market-types")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
{
"marketTypes": [
"<string>"
]
}
Response
200 - application/json
List of valid sports market types
marketTypes
string[]
List of all valid sports market types
List tags
GET/tags
List tags

```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/tags
Python
import requests
url = "https://gamma-api.polymarket.com/tags"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/tags', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/tags",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {

echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/tags"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-api.polymarket.com/tags")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/tags")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200

[
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
]
Query Parameters
limit
integer
Required range: x >= 0
offset
integer
Required range: x >= 0
order
string
Comma-separated list of fields to order by
ascending
boolean
include_template

boolean
is_carousel
boolean
Response
200 - application/json
List of tags
id
string
label
string | null
slug
string | null
forceShow
boolean | null
publishedAt
string | null
createdBy
integer | null

updatedBy
integer | null
createdAt
string` | null
updatedAt
string` | null
forceHide
boolean | null
isCarousel
boolean | null
Get tag by id
GET/tags/{id}
Get tag by id
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/tags/{id}
Python
import requests
url = "https://gamma-api.polymarket.com/tags/{id}"
response = requests.get(url)

print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/tags/{id}', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/tags/{id}",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {

url := "https://gamma-api.polymarket.com/tags/{id}"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/tags/{id}")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/tags/{id}")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}

Path Parameters
id
integer
required
Query Parameters
include_template
boolean
Response
200
application/json
Tag
id
string
label
string | null
slug
string | null

forceShow
boolean | null
publishedAt
string | null
createdBy
integer | null
updatedBy
integer | null
createdAt
string` | null
updatedAt
string` | null
forceHide
boolean | null
isCarousel
boolean | null

404
Not found
Get tag by slug
GET/tags/slug/{slug}
Get tag by slug
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/tags/slug/{slug}
Python
import requests
url = "https://gamma-api.polymarket.com/tags/slug/{slug}"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/tags/slug/{slug}', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/tags/slug/{slug}",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```

$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/tags/slug/{slug}"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/tags/slug/{slug}")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/tags/slug/{slug}")
http = Net::HTTP.new(url.host, url.port)

http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
Path Parameters
slug
string
required
Query Parameters
include_template
boolean
Response
200
application/json
Tag
id
string

label
string | null
slug
string | null
forceShow
boolean | null
publishedAt
string | null
createdBy
integer | null
updatedBy
integer | null
createdAt
string` | null
updatedAt
string` | null

forceHide
boolean | null
isCarousel
boolean | null
Response
404
Not found
Get related tags (relationships) by tag id
GET/tags/{id}/related-tags
Get related tags (relationships) by tag id
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/tags/{id}/related-tags
Python
import requests
url = "https://gamma-api.polymarket.com/tags/{id}/related-tags"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/tags/{id}/related-tags', options)
.then(res => res.json())

.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/tags/{id}/related-tags",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/tags/{id}/related-tags"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)

fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/tags/{id}/related-tags")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/tags/{id}/related-tags")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"id": "<string>",
"tagID": 123,
"relatedTagID": 123,
"rank": 123
}
]
Path Parameters
id
integer
required
Query Parameters

omit_empty
boolean
status
enum`
Available options: active, closed, all
Response
200 - application/json
Related tag relationships
id
string
tagID
integer | null
relatedTagID
integer | null
rank
integer | null
Get related tags (relationships) by tag slug
GET/tags/slug/{slug}/related-tags

Get related tags (relationships) by tag slug
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/tags/slug/{slug}/related-tags
Python
import requests
url = "https://gamma-api.polymarket.com/tags/slug/{slug}/related-tags"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/tags/slug/{slug}/related-tags', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/tags/slug/{slug}/related-tags",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {

echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/tags/slug/{slug}/related-tags"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/tags/slug/{slug}/related-tags")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/tags/slug/{slug}/related-tags")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200

[
{
"id": "<string>",
"tagID": 123,
"relatedTagID": 123,
"rank": 123
}
]
Path Parameters
slug
string
required
Query Parameters
omit_empty
boolean
status
enum`
Available options: active, closed, all
Response
200 - application/json
Related tag relationships
id
string

tagID
integer | null
relatedTagID
integer | null
rank
integer | null
Get tags related to a tag id
GET/tags/{id}/related-tags/tags
Get tags related to a tag id
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/tags/{id}/related-tags/tags
Python
import requests
url = "https://gamma-api.polymarket.com/tags/{id}/related-tags/tags"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/tags/{id}/related-tags/tags', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));

PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/tags/{id}/related-tags/tags",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/tags/{id}/related-tags/tags"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}

Java
HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/tags/{id}/related-tags/tags")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/tags/{id}/related-tags/tags")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
]
Path Parameters
id
integer
required

Query Parameters
omit_empty
boolean
status
enum`
Available options: active, closed, all
Response
200 - application/json
Related tags
id
string
label
string | null
slug
string | null
forceShow
boolean | null

publishedAt
string | null
createdBy
integer | null
updatedBy
integer | null
createdAt
string` | null
updatedAt
string` | null
forceHide
boolean | null
isCarousel
boolean | null
Get tags related to a tag slug
GET/tags/slug/{slug}/related-tags/tags
Get tags related to a tag slug
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/tags/slug/{slug}/related-tags/tags

Python
import requests
url = "https://gamma-api.polymarket.com/tags/slug/{slug}/related-tags/tags"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/tags/slug/{slug}/related-tags/tags', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/tags/slug/{slug}/related-
tags/tags",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go

package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/tags/slug/{slug}/related-tags/tags"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/tags/slug/{slug}/related-tags/tags")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/tags/slug/{slug}/related-tags/tags")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"id": "<string>",
"label": "<string>",

"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
]
Path Parameters
slug
string
required
Query Parameters
omit_empty
boolean
status
enum`
Available options: active, closed, all
Response
200 - application/json
Related tags
id
string

label
string | null
slug
string | null
forceShow
boolean | null
publishedAt
string | null
createdBy
integer | null
updatedBy
integer | null
createdAt
string` | null
updatedAt
string` | null
forceHide
boolean | null

isCarousel
boolean | null
List events
GET/events
List events
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/events
Python
import requests
url = "https://gamma-api.polymarket.com/events"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/events', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/events",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,

CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/events"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-api.polymarket.com/events")
.asString();
```
Ruby
require 'uri'
require 'net/http'

url = URI("https://gamma-api.polymarket.com/events")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"creationDate": "2023-11-07T05:31:56Z",
"endDate": "2023-11-07T05:31:56Z",
"image": "<string>",
"icon": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"liquidity": 123,
"volume": 123,
"openInterest": 123,
"sortBy": "<string>",
"category": "<string>",
"subcategory": "<string>",
"isTemplate": true,
"templateVariables": "<string>",
"published_at": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"competitive": 123,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,

"featuredImage": "<string>",
"disqusThread": "<string>",
"parentEvent": "<string>",
"enableOrderBook": true,
"liquidityAmm": 123,
"liquidityClob": 123,
"negRisk": true,
"negRiskMarketID": "<string>",
"negRiskFeeBips": 123,
"commentCount": 123,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"featuredImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"subEvents": [
"<string>"
],
"markets": [
{
"id": "<string>",

"question": "<string>",
"conditionId": "<string>",
"slug": "<string>",
"twitterCardImage": "<string>",
"resolutionSource": "<string>",
"endDate": "2023-11-07T05:31:56Z",
"category": "<string>",
"ammType": "<string>",
"liquidity": "<string>",
"sponsorName": "<string>",
"sponsorImage": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"xAxisValue": "<string>",
"yAxisValue": "<string>",
"denominationToken": "<string>",
"fee": "<string>",
"image": "<string>",
"icon": "<string>",
"lowerBound": "<string>",
"upperBound": "<string>",
"description": "<string>",
"outcomes": "<string>",
"outcomePrices": "<string>",
"volume": "<string>",
"active": true,
"marketType": "<string>",
"formatType": "<string>",
"lowerBoundDate": "<string>",
"upperBoundDate": "<string>",
"closed": true,
"marketMakerAddress": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"closedTime": "<string>",
"wideFormat": true,
"new": true,
"mailchimpTag": "<string>",
"featured": true,
"archived": true,
"resolvedBy": "<string>",
"restricted": true,
"marketGroup": 123,
"groupItemTitle": "<string>",
"groupItemThreshold": "<string>",
"questionID": "<string>",
"umaEndDate": "<string>",
"enableOrderBook": true,
"orderPriceMinTickSize": 123,
"orderMinSize": 123,
"umaResolutionStatus": "<string>",

"curationOrder": 123,
"volumeNum": 123,
"liquidityNum": 123,
"endDateIso": "<string>",
"startDateIso": "<string>",
"umaEndDateIso": "<string>",
"hasReviewedDates": true,
"readyForCron": true,
"commentsEnabled": true,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,
"gameStartTime": "<string>",
"secondsDelay": 123,
"clobTokenIds": "<string>",
"disqusThread": "<string>",
"shortOutcomes": "<string>",
"teamAID": "<string>",
"teamBID": "<string>",
"umaBond": "<string>",
"umaReward": "<string>",
"fpmmLive": true,
"volume24hrAmm": 123,
"volume1wkAmm": 123,
"volume1moAmm": 123,
"volume1yrAmm": 123,
"volume24hrClob": 123,
"volume1wkClob": 123,
"volume1moClob": 123,
"volume1yrClob": 123,
"volumeAmm": 123,
"volumeClob": 123,
"liquidityAmm": 123,
"liquidityClob": 123,
"makerBaseFee": 123,
"takerBaseFee": 123,
"customLiveness": 123,
"acceptingOrders": true,
"notificationsEnabled": true,
"score": 123,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"

},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"events": "<array>",
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"creator": "<string>",
"ready": true,
"funded": true,
"pastSlugs": "<string>",
"readyTimestamp": "2023-11-07T05:31:56Z",
"fundedTimestamp": "2023-11-07T05:31:56Z",
"acceptingOrdersTimestamp": "2023-11-07T05:31:56Z",
"competitive": 123,
"rewardsMinSize": 123,
"rewardsMaxSpread": 123,

"spread": 123,
"automaticallyResolved": true,
"oneDayPriceChange": 123,
"oneHourPriceChange": 123,
"oneWeekPriceChange": 123,
"oneMonthPriceChange": 123,
"oneYearPriceChange": 123,
"lastTradePrice": 123,
"bestBid": 123,
"bestAsk": 123,
"automaticallyActive": true,
"clearBookOnStart": true,
"chartColor": "<string>",
"seriesColor": "<string>",
"showGmpSeries": true,
"showGmpOutcome": true,
"manualActivation": true,
"negRiskOther": true,
"gameId": "<string>",
"groupItemRange": "<string>",
"sportsMarketType": "<string>",
"line": 123,
"umaResolutionStatuses": "<string>",
"pendingDeployment": true,
"deploying": true,
"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",
"rfqEnabled": true,
"eventStartTime": "2023-11-07T05:31:56Z"
}
],
"series": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"seriesType": "<string>",
"recurrence": "<string>",
"description": "<string>",
"image": "<string>",
"icon": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": true,

"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"competitive": "<string>",
"volume24hr": 123,
"volume": 123,
"liquidity": 123,
"startDate": "2023-11-07T05:31:56Z",
"pythTokenID": "<string>",
"cgAssetName": "<string>",
"score": 123,
"events": "<array>",
"collections": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",
"image": "<string>",
"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,

"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
}
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",

"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"commentCount": 123,
"chats": [
{
"id": "<string>",
"channelId": "<string>",
"channelName": "<string>",
"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",
"endTime": "2023-11-07T05:31:56Z"
}
]
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"collections": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",
"image": "<string>",
"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,

"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
}
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,

"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"cyom": true,
"closedTime": "2023-11-07T05:31:56Z",
"showAllOutcomes": true,
"showMarketImages": true,
"automaticallyResolved": true,
"enableNegRisk": true,
"automaticallyActive": true,
"eventDate": "<string>",
"startTime": "2023-11-07T05:31:56Z",
"eventWeek": 123,
"seriesSlug": "<string>",
"score": "<string>",
"elapsed": "<string>",
"period": "<string>",
"live": true,
"ended": true,
"finishedTimestamp": "2023-11-07T05:31:56Z",
"gmpChartMode": "<string>",
"eventCreators": [
{
"id": "<string>",
"creatorName": "<string>",
"creatorHandle": "<string>",
"creatorUrl": "<string>",
"creatorImage": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tweetCount": 123,
"chats": [
{
"id": "<string>",
"channelId": "<string>",
"channelName": "<string>",
"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",
"endTime": "2023-11-07T05:31:56Z"
}
],
"featuredOrder": 123,
"estimateValue": true,

"cantEstimate": true,
"estimatedValue": "<string>",
"templates": [
{
"id": "<string>",
"eventTitle": "<string>",
"eventSlug": "<string>",
"eventImage": "<string>",
"marketTitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",
"negRisk": true,
"sortBy": "<string>",
"showMarketImages": true,
"seriesSlug": "<string>",
"outcomes": "<string>"
}
],
"spreadsMainLine": 123,
"totalsMainLine": 123,
"carouselMap": "<string>",
"pendingDeployment": true,
"deploying": true,
"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",
"gameStatus": "<string>"
}
]
Query Parameters
limit
integer
Required range: x >= 0
offset
integer
Required range: x >= 0
order
string
Comma-separated list of fields to order by
ascending
boolean
id
integer[]

tag_id
integer
exclude_tag_id
integer[]
slug
string[]
tag_slug
string
related_tags
boolean
active
boolean
archived
boolean
featured
boolean
cyom
boolean
include_chat
boolean
include_template
boolean
recurrence
string
closed
boolean
liquidity_min
number

liquidity_max
number
volume_min
number
volume_max
number
start_date_min
string <date-time> start_date_max string
end_date_min
string <date-time> end_date_max string
Response
200 - application/json
List of events
id
string
ticker
string | null
slug
string | null
title
string | null
subtitle
string | null
description
string | null
resolutionSource
string | null

startDate
string <date-time> | null creationDate string | null
endDate
string <date-time> | null image string | null icon string | null active boolean | null closed boolean | null
archived boolean | null new boolean | null featured boolean | null restricted boolean | null liquidity
number | null volume number | null openInterest number | null sortBy string | null category string | null
subcategory string | null isTemplate boolean | null templateVariables string | null published_at string |
null createdBy string | null updatedBy string | null createdAt string | null
updatedAt
string` | null
commentsEnabled
boolean | null
competitive
number | null
volume24hr
number | null
volume1wk
number | null
volume1mo
number | null
volume1yr
number | null
featuredImage
string | null
disqusThread
string | null
parentEvent
string | null
enableOrderBook
boolean | null
liquidityAmm

number | null
liquidityClob
number | null
negRisk
boolean | null
negRiskMarketID
string | null
negRiskFeeBips
integer | null
commentCount
integer | null
imageOptimized
object
Hide child attributes
imageOptimized.id
string
imageOptimized.imageUrlSource
string | null
imageOptimized.imageUrlOptimized
string | null
imageOptimized.imageSizeKbSource
number | null
imageOptimized.imageSizeKbOptimized
number | null
imageOptimized.imageOptimizedComplete
boolean | null
imageOptimized.imageOptimizedLastUpdated
string | null
imageOptimized.relID

integer | null
imageOptimized.field
string | null
imageOptimized.relname
string | null
iconOptimized
object
Hide child attributes
iconOptimized.id
string
iconOptimized.imageUrlSource
string | null
iconOptimized.imageUrlOptimized
string | null
iconOptimized.imageSizeKbSource
number | null
iconOptimized.imageSizeKbOptimized
number | null
iconOptimized.imageOptimizedComplete
boolean | null
iconOptimized.imageOptimizedLastUpdated
string | null
iconOptimized.relID
integer | null
iconOptimized.field
string | null
iconOptimized.relname
string | null
featuredImageOptimized

object
Hide child attributes
featuredImageOptimized.id
string
featuredImageOptimized.imageUrlSource
string | null
featuredImageOptimized.imageUrlOptimized
string | null
featuredImageOptimized.imageSizeKbSource
number | null
featuredImageOptimized.imageSizeKbOptimized
number | null
featuredImageOptimized.imageOptimizedComplete
boolean | null
featuredImageOptimized.imageOptimizedLastUpdated
string | null
featuredImageOptimized.relID
integer | null
featuredImageOptimized.field
string | null
featuredImageOptimized.relname
string | null
subEvents
string[] | null
markets
object[]
Hide child attributes
markets.id
string

markets.question
string | null
markets.conditionId
string
markets.slug
string | null
markets.twitterCardImage
string | null
markets.resolutionSource
string | null
markets.endDate
string <date-time> | null markets.category string | null markets.ammType string | null markets.liquidity
string | null markets.sponsorName string | null markets.sponsorImage string | null markets.startDate
string | null
markets.xAxisValue
string | null
markets.yAxisValue
string | null
markets.denominationToken
string | null
markets.fee
string | null
markets.image
string | null
markets.icon
string | null
markets.lowerBound
string | null
markets.upperBound

string | null
markets.description
string | null
markets.outcomes
string | null
markets.outcomePrices
string | null
markets.volume
string | null
markets.active
boolean | null
markets.marketType
string | null
markets.formatType
string | null
markets.lowerBoundDate
string | null
markets.upperBoundDate
string | null
markets.closed
boolean | null
markets.marketMakerAddress
string
markets.createdBy
integer | null
markets.updatedBy
integer | null
markets.createdAt
string <date-time> | null markets.updatedAt string | null

markets.closedTime
string | null
markets.wideFormat
boolean | null
markets.new
boolean | null
markets.mailchimpTag
string | null
markets.featured
boolean | null
markets.archived
boolean | null
markets.resolvedBy
string | null
markets.restricted
boolean | null
markets.marketGroup
integer | null
markets.groupItemTitle
string | null
markets.groupItemThreshold
string | null
markets.questionID
string | null
markets.umaEndDate
string | null
markets.enableOrderBook
boolean | null

markets.orderPriceMinTickSize
number | null
markets.orderMinSize
number | null
markets.umaResolutionStatus
string | null
markets.curationOrder
integer | null
markets.volumeNum
number | null
markets.liquidityNum
number | null
markets.endDateIso
string | null
markets.startDateIso
string | null
markets.umaEndDateIso
string | null
markets.hasReviewedDates
boolean | null
markets.readyForCron
boolean | null
markets.commentsEnabled
boolean | null
markets.volume24hr
number | null
markets.volume1wk
number | null
markets.volume1mo

number | null
markets.volume1yr
number | null
markets.gameStartTime
string | null
markets.secondsDelay
integer | null
markets.clobTokenIds
string | null
markets.disqusThread
string | null
markets.shortOutcomes
string | null
markets.teamAID
string | null
markets.teamBID
string | null
markets.umaBond
string | null
markets.umaReward
string | null
markets.fpmmLive
boolean | null
markets.volume24hrAmm
number | null
markets.volume1wkAmm
number | null
markets.volume1moAmm
number | null

markets.volume1yrAmm
number | null
markets.volume24hrClob
number | null
markets.volume1wkClob
number | null
markets.volume1moClob
number | null
markets.volume1yrClob
number | null
markets.volumeAmm
number | null
markets.volumeClob
number | null
markets.liquidityAmm
number | null
markets.liquidityClob
number | null
markets.makerBaseFee
integer | null
markets.takerBaseFee
integer | null
markets.customLiveness
integer | null
markets.acceptingOrders
boolean | null
markets.notificationsEnabled
boolean | null

markets.score
integer | null
markets.imageOptimized
object
Hide child attributes
markets.imageOptimized.id
string
markets.imageOptimized.imageUrlSource
string | null
markets.imageOptimized.imageUrlOptimized
string | null
markets.imageOptimized.imageSizeKbSource
number | null
markets.imageOptimized.imageSizeKbOptimized
number | null
markets.imageOptimized.imageOptimizedComplete
boolean | null
markets.imageOptimized.imageOptimizedLastUpdated
string | null
markets.imageOptimized.relID
integer | null
markets.imageOptimized.field
string | null
markets.imageOptimized.relname
string | null
markets.iconOptimized
object
Hide child attributes
markets.iconOptimized.id

string
markets.iconOptimized.imageUrlSource
string | null
markets.iconOptimized.imageUrlOptimized
string | null
markets.iconOptimized.imageSizeKbSource
number | null
markets.iconOptimized.imageSizeKbOptimized
number | null
markets.iconOptimized.imageOptimizedComplete
boolean | null
markets.iconOptimized.imageOptimizedLastUpdated
string | null
markets.iconOptimized.relID
integer | null
markets.iconOptimized.field
string | null
markets.iconOptimized.relname
string | null
markets.events
array
markets.categories
object[]
Hide child attributes
markets.categories.id
string
markets.categories.label
string | null
markets.categories.parentCategory

string | null
markets.categories.slug
string | null
markets.categories.publishedAt
string | null
markets.categories.createdBy
string | null
markets.categories.updatedBy
string | null
markets.categories.createdAt
string <date-time> | null markets.categories.updatedAt string | null
markets.tags
object[]
Hide child attributes
markets.tags.id
string
markets.tags.label
string | null
markets.tags.slug
string | null
markets.tags.forceShow
boolean | null
markets.tags.publishedAt
string | null
markets.tags.createdBy
integer | null
markets.tags.updatedBy
integer | null
markets.tags.createdAt

string <date-time> | null markets.tags.updatedAt string | null
markets.tags.forceHide
boolean | null
markets.tags.isCarousel
boolean | null
markets.creator
string | null
markets.ready
boolean | null
markets.funded
boolean | null
markets.pastSlugs
string | null
markets.readyTimestamp
string <date-time> | null markets.fundedTimestamp string | null
markets.acceptingOrdersTimestamp
string <date-time> | null markets.competitive number | null markets.rewardsMinSize number | null
markets.rewardsMaxSpread number | null markets.spread number | null markets.automaticallyResolved
boolean | null markets.oneDayPriceChange number | null markets.oneHourPriceChange number | null
markets.oneWeekPriceChange number | null markets.oneMonthPriceChange number | null
markets.oneYearPriceChange number | null markets.lastTradePrice number | null markets.bestBid
number | null markets.bestAsk number | null markets.automaticallyActive boolean | null
markets.clearBookOnStart boolean | null markets.chartColor string | null markets.seriesColor string | null
markets.showGmpSeries boolean | null markets.showGmpOutcome boolean | null
markets.manualActivation boolean | null markets.negRiskOther boolean | null markets.gameId string |
null markets.groupItemRange string | null markets.sportsMarketType string | null markets.line number |
null markets.umaResolutionStatuses string | null markets.pendingDeployment boolean | null
markets.deploying boolean | null markets.deployingTimestamp string | null
markets.scheduledDeploymentTimestamp
string <date-time> | null markets.rfqEnabled boolean | null markets.eventStartTime string | null
series
object[]
Hide child attributes

series.id
string
series.ticker
string | null
series.slug
string | null
series.title
string | null
series.subtitle
string | null
series.seriesType
string | null
series.recurrence
string | null
series.description
string | null
series.image
string | null
series.icon
string | null
series.layout
string | null
series.active
boolean | null
series.closed
boolean | null
series.archived
boolean | null

series.new
boolean | null
series.featured
boolean | null
series.restricted
boolean | null
series.isTemplate
boolean | null
series.templateVariables
boolean | null
series.publishedAt
string | null
series.createdBy
string | null
series.updatedBy
string | null
series.createdAt
string <date-time> | null series.updatedAt string | null
series.commentsEnabled
boolean | null
series.competitive
string | null
series.volume24hr
number | null
series.volume
number | null
series.liquidity
number | null
series.startDate

string` | null
series.pythTokenID
string | null
series.cgAssetName
string | null
series.score
integer | null
series.events
array
series.collections
object[]
Hide child attributes
series.collections.id
string
series.collections.ticker
string | null
series.collections.slug
string | null
series.collections.title
string | null
series.collections.subtitle
string | null
series.collections.collectionType
string | null
series.collections.description
string | null
series.collections.tags
string | null
series.collections.image

string | null
series.collections.icon
string | null
series.collections.headerImage
string | null
series.collections.layout
string | null
series.collections.active
boolean | null
series.collections.closed
boolean | null
series.collections.archived
boolean | null
series.collections.new
boolean | null
series.collections.featured
boolean | null
series.collections.restricted
boolean | null
series.collections.isTemplate
boolean | null
series.collections.templateVariables
string | null
series.collections.publishedAt
string | null
series.collections.createdBy
string | null
series.collections.updatedBy
string | null

series.collections.createdAt
string <date-time> | null series.collections.updatedAt string | null
series.collections.commentsEnabled
boolean | null
series.collections.imageOptimized
object
Hide child attributes
series.collections.imageOptimized.id
string
series.collections.imageOptimized.imageUrlSource
string | null
series.collections.imageOptimized.imageUrlOptimized
string | null
series.collections.imageOptimized.imageSizeKbSource
number | null
series.collections.imageOptimized.imageSizeKbOptimized
number | null
series.collections.imageOptimized.imageOptimizedComplete
boolean | null
series.collections.imageOptimized.imageOptimizedLastUpdated
string | null
series.collections.imageOptimized.relID
integer | null
series.collections.imageOptimized.field
string | null
series.collections.imageOptimized.relname
string | null
series.collections.iconOptimized

object
Hide child attributes
series.collections.iconOptimized.id
string
series.collections.iconOptimized.imageUrlSource
string | null
series.collections.iconOptimized.imageUrlOptimized
string | null
series.collections.iconOptimized.imageSizeKbSource
number | null
series.collections.iconOptimized.imageSizeKbOptimized
number | null
series.collections.iconOptimized.imageOptimizedComplete
boolean | null
series.collections.iconOptimized.imageOptimizedLastUpdated
string | null
series.collections.iconOptimized.relID
integer | null
series.collections.iconOptimized.field
string | null
series.collections.iconOptimized.relname
string | null
series.collections.headerImageOptimized
object
Hide child attributes
series.collections.headerImageOptimized.id
string
series.collections.headerImageOptimized.imageUrlSource
string | null

series.collections.headerImageOptimized.imageUrlOptimized
string | null
series.collections.headerImageOptimized.imageSizeKbSource
number | null
series.collections.headerImageOptimized.imageSizeKbOptimized
number | null
series.collections.headerImageOptimized.imageOptimizedComplete
boolean | null
series.collections.headerImageOptimized.imageOptimizedLastUpdated
string | null
series.collections.headerImageOptimized.relID
integer | null
series.collections.headerImageOptimized.field
string | null
series.collections.headerImageOptimized.relname
string | null
series.categories
object[]
Hide child attributes
series.categories.id
string
series.categories.label
string | null
series.categories.parentCategory
string | null
series.categories.slug
string | null
series.categories.publishedAt
string | null

series.categories.createdBy
string | null
series.categories.updatedBy
string | null
series.categories.createdAt
string <date-time> | null series.categories.updatedAt string | null
series.tags
object[]
Hide child attributes
series.tags.id
string
series.tags.label
string | null
series.tags.slug
string | null
series.tags.forceShow
boolean | null
series.tags.publishedAt
string | null
series.tags.createdBy
integer | null
series.tags.updatedBy
integer | null
series.tags.createdAt
string <date-time> | null series.tags.updatedAt string | null
series.tags.forceHide
boolean | null
series.tags.isCarousel
boolean | null

series.commentCount
integer | null
series.chats
object[]
Hide child attributes
series.chats.id
string
series.chats.channelId
string | null
series.chats.channelName
string | null
series.chats.channelImage
string | null
series.chats.live
boolean | null
series.chats.startTime
string <date-time> | null series.chats.endTime string | null
categories
object[]
Hide child attributes
categories.id
string
categories.label
string | null
categories.parentCategory
string | null
categories.slug
string | null

categories.publishedAt
string | null
categories.createdBy
string | null
categories.updatedBy
string | null
categories.createdAt
string <date-time> | null categories.updatedAt string | null
collections
object[]
Hide child attributes
collections.id
string
collections.ticker
string | null
collections.slug
string | null
collections.title
string | null
collections.subtitle
string | null
collections.collectionType
string | null
collections.description
string | null
collections.tags
string | null
collections.image
string | null

collections.icon
string | null
collections.headerImage
string | null
collections.layout
string | null
collections.active
boolean | null
collections.closed
boolean | null
collections.archived
boolean | null
collections.new
boolean | null
collections.featured
boolean | null
collections.restricted
boolean | null
collections.isTemplate
boolean | null
collections.templateVariables
string | null
collections.publishedAt
string | null
collections.createdBy
string | null
collections.updatedBy
string | null
collections.createdAt

string <date-time> | null collections.updatedAt string | null
collections.commentsEnabled
boolean | null
collections.imageOptimized
object
Hide child attributes
collections.imageOptimized.id
string
collections.imageOptimized.imageUrlSource
string | null
collections.imageOptimized.imageUrlOptimized
string | null
collections.imageOptimized.imageSizeKbSource
number | null
collections.imageOptimized.imageSizeKbOptimized
number | null
collections.imageOptimized.imageOptimizedComplete
boolean | null
collections.imageOptimized.imageOptimizedLastUpdated
string | null
collections.imageOptimized.relID
integer | null
collections.imageOptimized.field
string | null
collections.imageOptimized.relname
string | null
collections.iconOptimized
object
Hide child attributes

collections.iconOptimized.id
string
collections.iconOptimized.imageUrlSource
string | null
collections.iconOptimized.imageUrlOptimized
string | null
collections.iconOptimized.imageSizeKbSource
number | null
collections.iconOptimized.imageSizeKbOptimized
number | null
collections.iconOptimized.imageOptimizedComplete
boolean | null
collections.iconOptimized.imageOptimizedLastUpdated
string | null
collections.iconOptimized.relID
integer | null
collections.iconOptimized.field
string | null
collections.iconOptimized.relname
string | null
collections.headerImageOptimized
object
Hide child attributes
collections.headerImageOptimized.id
string
collections.headerImageOptimized.imageUrlSource
string | null
collections.headerImageOptimized.imageUrlOptimized
string | null

collections.headerImageOptimized.imageSizeKbSource
number | null
collections.headerImageOptimized.imageSizeKbOptimized
number | null
collections.headerImageOptimized.imageOptimizedComplete
boolean | null
collections.headerImageOptimized.imageOptimizedLastUpdated
string | null
collections.headerImageOptimized.relID
integer | null
collections.headerImageOptimized.field
string | null
collections.headerImageOptimized.relname
string | null
tags
object[]
Hide child attributes
tags.id
string
tags.label
string | null
tags.slug
string | null
tags.forceShow
boolean | null
tags.publishedAt
string | null
tags.createdBy
integer | null
tags.updatedBy

integer | null
tags.createdAt
string <date-time> | null tags.updatedAt string | null
tags.forceHide
boolean | null
tags.isCarousel
boolean | null
cyom
boolean | null
closedTime
string <date-time> | null showAllOutcomes boolean | null showMarketImages boolean | null
automaticallyResolved boolean | null enableNegRisk boolean | null automaticallyActive boolean | null
eventDate string | null startTime string | null
eventWeek
integer | null
seriesSlug
string | null
score
string | null
elapsed
string | null
period
string | null
live
boolean | null
ended
boolean | null
finishedTimestamp
string` | null

gmpChartMode
string | null
eventCreators
object[]
Hide child attributes
eventCreators.id
string
eventCreators.creatorName
string | null
eventCreators.creatorHandle
string | null
eventCreators.creatorUrl
string | null
eventCreators.creatorImage
string | null
eventCreators.createdAt
string <date-time> | null eventCreators.updatedAt string | null
tweetCount
integer | null
chats
object[]
Hide child attributes
chats.id
string
chats.channelId
string | null
chats.channelName
string | null
chats.channelImage

string | null
chats.live
boolean | null
chats.startTime
string <date-time> | null chats.endTime string | null
featuredOrder
integer | null
estimateValue
boolean | null
cantEstimate
boolean | null
estimatedValue
string | null
templates
object[]
Hide child attributes
templates.id
string
templates.eventTitle
string | null
templates.eventSlug
string | null
templates.eventImage
string | null
templates.marketTitle
string | null
templates.description
string | null
templates.resolutionSource

string | null
templates.negRisk
boolean | null
templates.sortBy
string | null
templates.showMarketImages
boolean | null
templates.seriesSlug
string | null
templates.outcomes
string | null
spreadsMainLine
number | null
totalsMainLine
number | null
carouselMap
string | null
pendingDeployment
boolean | null
deploying
boolean | null
deployingTimestamp
string <date-time> | null scheduledDeploymentTimestamp string | null
gameStatus
string | null
Get event by id
GET/events/{id}
Get event by id
```bash
cURL

curl --request GET \
--url https://gamma-api.polymarket.com/events/{id}
Python
import requests
url = "https://gamma-api.polymarket.com/events/{id}"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/events/{id}', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/events/{id}",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}

Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/events/{id}"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/events/{id}")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/events/{id}")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
{
"id": "<string>",

"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"creationDate": "2023-11-07T05:31:56Z",
"endDate": "2023-11-07T05:31:56Z",
"image": "<string>",
"icon": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"liquidity": 123,
"volume": 123,
"openInterest": 123,
"sortBy": "<string>",
"category": "<string>",
"subcategory": "<string>",
"isTemplate": true,
"templateVariables": "<string>",
"published_at": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"competitive": 123,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,
"featuredImage": "<string>",
"disqusThread": "<string>",
"parentEvent": "<string>",
"enableOrderBook": true,
"liquidityAmm": 123,
"liquidityClob": 123,
"negRisk": true,
"negRiskMarketID": "<string>",
"negRiskFeeBips": 123,
"commentCount": 123,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,

"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"featuredImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"subEvents": [
"<string>"
],
"markets": [
{
"id": "<string>",
"question": "<string>",
"conditionId": "<string>",
"slug": "<string>",
"twitterCardImage": "<string>",
"resolutionSource": "<string>",
"endDate": "2023-11-07T05:31:56Z",
"category": "<string>",
"ammType": "<string>",
"liquidity": "<string>",
"sponsorName": "<string>",
"sponsorImage": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"xAxisValue": "<string>",
"yAxisValue": "<string>",
"denominationToken": "<string>",
"fee": "<string>",

"image": "<string>",
"icon": "<string>",
"lowerBound": "<string>",
"upperBound": "<string>",
"description": "<string>",
"outcomes": "<string>",
"outcomePrices": "<string>",
"volume": "<string>",
"active": true,
"marketType": "<string>",
"formatType": "<string>",
"lowerBoundDate": "<string>",
"upperBoundDate": "<string>",
"closed": true,
"marketMakerAddress": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"closedTime": "<string>",
"wideFormat": true,
"new": true,
"mailchimpTag": "<string>",
"featured": true,
"archived": true,
"resolvedBy": "<string>",
"restricted": true,
"marketGroup": 123,
"groupItemTitle": "<string>",
"groupItemThreshold": "<string>",
"questionID": "<string>",
"umaEndDate": "<string>",
"enableOrderBook": true,
"orderPriceMinTickSize": 123,
"orderMinSize": 123,
"umaResolutionStatus": "<string>",
"curationOrder": 123,
"volumeNum": 123,
"liquidityNum": 123,
"endDateIso": "<string>",
"startDateIso": "<string>",
"umaEndDateIso": "<string>",
"hasReviewedDates": true,
"readyForCron": true,
"commentsEnabled": true,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,
"gameStartTime": "<string>",
"secondsDelay": 123,
"clobTokenIds": "<string>",

"disqusThread": "<string>",
"shortOutcomes": "<string>",
"teamAID": "<string>",
"teamBID": "<string>",
"umaBond": "<string>",
"umaReward": "<string>",
"fpmmLive": true,
"volume24hrAmm": 123,
"volume1wkAmm": 123,
"volume1moAmm": 123,
"volume1yrAmm": 123,
"volume24hrClob": 123,
"volume1wkClob": 123,
"volume1moClob": 123,
"volume1yrClob": 123,
"volumeAmm": 123,
"volumeClob": 123,
"liquidityAmm": 123,
"liquidityClob": 123,
"makerBaseFee": 123,
"takerBaseFee": 123,
"customLiveness": 123,
"acceptingOrders": true,
"notificationsEnabled": true,
"score": 123,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"events": "<array>",
"categories": [
{

"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"creator": "<string>",
"ready": true,
"funded": true,
"pastSlugs": "<string>",
"readyTimestamp": "2023-11-07T05:31:56Z",
"fundedTimestamp": "2023-11-07T05:31:56Z",
"acceptingOrdersTimestamp": "2023-11-07T05:31:56Z",
"competitive": 123,
"rewardsMinSize": 123,
"rewardsMaxSpread": 123,
"spread": 123,
"automaticallyResolved": true,
"oneDayPriceChange": 123,
"oneHourPriceChange": 123,
"oneWeekPriceChange": 123,
"oneMonthPriceChange": 123,
"oneYearPriceChange": 123,
"lastTradePrice": 123,
"bestBid": 123,
"bestAsk": 123,
"automaticallyActive": true,
"clearBookOnStart": true,
"chartColor": "<string>",
"seriesColor": "<string>",
"showGmpSeries": true,
"showGmpOutcome": true,

"manualActivation": true,
"negRiskOther": true,
"gameId": "<string>",
"groupItemRange": "<string>",
"sportsMarketType": "<string>",
"line": 123,
"umaResolutionStatuses": "<string>",
"pendingDeployment": true,
"deploying": true,
"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",
"rfqEnabled": true,
"eventStartTime": "2023-11-07T05:31:56Z"
}
],
"series": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"seriesType": "<string>",
"recurrence": "<string>",
"description": "<string>",
"image": "<string>",
"icon": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": true,
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"competitive": "<string>",
"volume24hr": 123,
"volume": 123,
"liquidity": 123,
"startDate": "2023-11-07T05:31:56Z",
"pythTokenID": "<string>",
"cgAssetName": "<string>",
"score": 123,
"events": "<array>",
"collections": [

{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",
"image": "<string>",
"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {

"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
}
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"commentCount": 123,
"chats": [
{
"id": "<string>",
"channelId": "<string>",
"channelName": "<string>",
"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",
"endTime": "2023-11-07T05:31:56Z"
}

]
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"collections": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",
"image": "<string>",
"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",

"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
}
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"cyom": true,
"closedTime": "2023-11-07T05:31:56Z",
"showAllOutcomes": true,
"showMarketImages": true,
"automaticallyResolved": true,
"enableNegRisk": true,
"automaticallyActive": true,

"eventDate": "<string>",
"startTime": "2023-11-07T05:31:56Z",
"eventWeek": 123,
"seriesSlug": "<string>",
"score": "<string>",
"elapsed": "<string>",
"period": "<string>",
"live": true,
"ended": true,
"finishedTimestamp": "2023-11-07T05:31:56Z",
"gmpChartMode": "<string>",
"eventCreators": [
{
"id": "<string>",
"creatorName": "<string>",
"creatorHandle": "<string>",
"creatorUrl": "<string>",
"creatorImage": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tweetCount": 123,
"chats": [
{
"id": "<string>",
"channelId": "<string>",
"channelName": "<string>",
"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",
"endTime": "2023-11-07T05:31:56Z"
}
],
"featuredOrder": 123,
"estimateValue": true,
"cantEstimate": true,
"estimatedValue": "<string>",
"templates": [
{
"id": "<string>",
"eventTitle": "<string>",
"eventSlug": "<string>",
"eventImage": "<string>",
"marketTitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",
"negRisk": true,
"sortBy": "<string>",
"showMarketImages": true,
"seriesSlug": "<string>",
"outcomes": "<string>"

}
],
"spreadsMainLine": 123,
"totalsMainLine": 123,
"carouselMap": "<string>",
"pendingDeployment": true,
"deploying": true,
"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",
"gameStatus": "<string>"
}
Path Parameters
id
integer
required
Query Parameters
include_chat
boolean
include_template
boolean
Response
200 - application/json
Event
id
string
ticker
string | null
slug
string | null
title

string | null
subtitle
string | null
description
string | null
resolutionSource
string | null
startDate
string <date-time> | null creationDate string | null
endDate
string <date-time> | null image string | null icon string | null active boolean | null closed boolean | null
archived boolean | null new boolean | null featured boolean | null restricted boolean | null liquidity
number | null volume number | null openInterest number | null sortBy string | null category string | null
subcategory string | null isTemplate boolean | null templateVariables string | null published_at string |
null createdBy string | null updatedBy string | null createdAt string | null
updatedAt
string` | null
commentsEnabled
boolean | null
competitive
number | null
volume24hr
number | null
volume1wk
number | null
volume1mo
number | null
volume1yr
number | null
featuredImage
string | null

disqusThread
string | null
parentEvent
string | null
enableOrderBook
boolean | null
liquidityAmm
number | null
liquidityClob
number | null
negRisk
boolean | null
negRiskMarketID
string | null
negRiskFeeBips
integer | null
commentCount
integer | null
imageOptimized
object
Hide child attributes
imageOptimized.id
string
imageOptimized.imageUrlSource
string | null
imageOptimized.imageUrlOptimized
string | null
imageOptimized.imageSizeKbSource
number | null

imageOptimized.imageSizeKbOptimized
number | null
imageOptimized.imageOptimizedComplete
boolean | null
imageOptimized.imageOptimizedLastUpdated
string | null
imageOptimized.relID
integer | null
imageOptimized.field
string | null
imageOptimized.relname
string | null
iconOptimized
object
Hide child attributes
iconOptimized.id
string
iconOptimized.imageUrlSource
string | null
iconOptimized.imageUrlOptimized
string | null
iconOptimized.imageSizeKbSource
number | null
iconOptimized.imageSizeKbOptimized
number | null
iconOptimized.imageOptimizedComplete
boolean | null
iconOptimized.imageOptimizedLastUpdated
string | null

iconOptimized.relID
integer | null
iconOptimized.field
string | null
iconOptimized.relname
string | null
featuredImageOptimized
object
Hide child attributes
featuredImageOptimized.id
string
featuredImageOptimized.imageUrlSource
string | null
featuredImageOptimized.imageUrlOptimized
string | null
featuredImageOptimized.imageSizeKbSource
number | null
featuredImageOptimized.imageSizeKbOptimized
number | null
featuredImageOptimized.imageOptimizedComplete
boolean | null
featuredImageOptimized.imageOptimizedLastUpdated
string | null
featuredImageOptimized.relID
integer | null
featuredImageOptimized.field
string | null
featuredImageOptimized.relname
string | null

subEvents
string[] | null
markets
object[]
Hide child attributes
markets.id
string
markets.question
string | null
markets.conditionId
string
markets.slug
string | null
markets.twitterCardImage
string | null
markets.resolutionSource
string | null
markets.endDate
string <date-time> | null markets.category string | null markets.ammType string | null markets.liquidity
string | null markets.sponsorName string | null markets.sponsorImage string | null markets.startDate
string | null
markets.xAxisValue
string | null
markets.yAxisValue
string | null
markets.denominationToken
string | null
markets.fee
string | null

markets.image
string | null
markets.icon
string | null
markets.lowerBound
string | null
markets.upperBound
string | null
markets.description
string | null
markets.outcomes
string | null
markets.outcomePrices
string | null
markets.volume
string | null
markets.active
boolean | null
markets.marketType
string | null
markets.formatType
string | null
markets.lowerBoundDate
string | null
markets.upperBoundDate
string | null
markets.closed
boolean | null
markets.marketMakerAddress

string
markets.createdBy
integer | null
markets.updatedBy
integer | null
markets.createdAt
string <date-time> | null markets.updatedAt string | null
markets.closedTime
string | null
markets.wideFormat
boolean | null
markets.new
boolean | null
markets.mailchimpTag
string | null
markets.featured
boolean | null
markets.archived
boolean | null
markets.resolvedBy
string | null
markets.restricted
boolean | null
markets.marketGroup
integer | null
markets.groupItemTitle
string | null
markets.groupItemThreshold
string | null

markets.questionID
string | null
markets.umaEndDate
string | null
markets.enableOrderBook
boolean | null
markets.orderPriceMinTickSize
number | null
markets.orderMinSize
number | null
markets.umaResolutionStatus
string | null
markets.curationOrder
integer | null
markets.volumeNum
number | null
markets.liquidityNum
number | null
markets.endDateIso
string | null
markets.startDateIso
string | null
markets.umaEndDateIso
string | null
markets.hasReviewedDates
boolean | null
markets.readyForCron
boolean | null

markets.commentsEnabled
boolean | null
markets.volume24hr
number | null
markets.volume1wk
number | null
markets.volume1mo
number | null
markets.volume1yr
number | null
markets.gameStartTime
string | null
markets.secondsDelay
integer | null
markets.clobTokenIds
string | null
markets.disqusThread
string | null
markets.shortOutcomes
string | null
markets.teamAID
string | null
markets.teamBID
string | null
markets.umaBond
string | null
markets.umaReward
string | null
markets.fpmmLive

boolean | null
markets.volume24hrAmm
number | null
markets.volume1wkAmm
number | null
markets.volume1moAmm
number | null
markets.volume1yrAmm
number | null
markets.volume24hrClob
number | null
markets.volume1wkClob
number | null
markets.volume1moClob
number | null
markets.volume1yrClob
number | null
markets.volumeAmm
number | null
markets.volumeClob
number | null
markets.liquidityAmm
number | null
markets.liquidityClob
number | null
markets.makerBaseFee
integer | null
markets.takerBaseFee
integer | null

markets.customLiveness
integer | null
markets.acceptingOrders
boolean | null
markets.notificationsEnabled
boolean | null
markets.score
integer | null
markets.imageOptimized
object
Hide child attributes
markets.imageOptimized.id
string
markets.imageOptimized.imageUrlSource
string | null
markets.imageOptimized.imageUrlOptimized
string | null
markets.imageOptimized.imageSizeKbSource
number | null
markets.imageOptimized.imageSizeKbOptimized
number | null
markets.imageOptimized.imageOptimizedComplete
boolean | null
markets.imageOptimized.imageOptimizedLastUpdated
string | null
markets.imageOptimized.relID
integer | null
markets.imageOptimized.field
string | null

markets.imageOptimized.relname
string | null
markets.iconOptimized
object
Hide child attributes
markets.iconOptimized.id
string
markets.iconOptimized.imageUrlSource
string | null
markets.iconOptimized.imageUrlOptimized
string | null
markets.iconOptimized.imageSizeKbSource
number | null
markets.iconOptimized.imageSizeKbOptimized
number | null
markets.iconOptimized.imageOptimizedComplete
boolean | null
markets.iconOptimized.imageOptimizedLastUpdated
string | null
markets.iconOptimized.relID
integer | null
markets.iconOptimized.field
string | null
markets.iconOptimized.relname
string | null
markets.events
array
markets.categories

object[]
Hide child attributes
markets.categories.id
string
markets.categories.label
string | null
markets.categories.parentCategory
string | null
markets.categories.slug
string | null
markets.categories.publishedAt
string | null
markets.categories.createdBy
string | null
markets.categories.updatedBy
string | null
markets.categories.createdAt
string <date-time> | null markets.categories.updatedAt string | null
markets.tags
object[]
Hide child attributes
markets.tags.id
string
markets.tags.label
string | null
markets.tags.slug
string | null
markets.tags.forceShow
boolean | null

markets.tags.publishedAt
string | null
markets.tags.createdBy
integer | null
markets.tags.updatedBy
integer | null
markets.tags.createdAt
string <date-time> | null markets.tags.updatedAt string | null
markets.tags.forceHide
boolean | null
markets.tags.isCarousel
boolean | null
markets.creator
string | null
markets.ready
boolean | null
markets.funded
boolean | null
markets.pastSlugs
string | null
markets.readyTimestamp
string <date-time> | null markets.fundedTimestamp string | null
markets.acceptingOrdersTimestamp
string <date-time> | null markets.competitive number | null markets.rewardsMinSize number | null
markets.rewardsMaxSpread number | null markets.spread number | null markets.automaticallyResolved
boolean | null markets.oneDayPriceChange number | null markets.oneHourPriceChange number | null
markets.oneWeekPriceChange number | null markets.oneMonthPriceChange number | null
markets.oneYearPriceChange number | null markets.lastTradePrice number | null markets.bestBid
number | null markets.bestAsk number | null markets.automaticallyActive boolean | null
markets.clearBookOnStart boolean | null markets.chartColor string | null markets.seriesColor string | null
markets.showGmpSeries boolean | null markets.showGmpOutcome boolean | null
markets.manualActivation boolean | null markets.negRiskOther boolean | null markets.gameId string |

null markets.groupItemRange string | null markets.sportsMarketType string | null markets.line number |
null markets.umaResolutionStatuses string | null markets.pendingDeployment boolean | null
markets.deploying boolean | null markets.deployingTimestamp string | null
markets.scheduledDeploymentTimestamp
string <date-time> | null markets.rfqEnabled boolean | null markets.eventStartTime string | null
series
object[]
Hide child attributes
series.id
string
series.ticker
string | null
series.slug
string | null
series.title
string | null
series.subtitle
string | null
series.seriesType
string | null
series.recurrence
string | null
series.description
string | null
series.image
string | null
series.icon
string | null
series.layout
string | null

series.active
boolean | null
series.closed
boolean | null
series.archived
boolean | null
series.new
boolean | null
series.featured
boolean | null
series.restricted
boolean | null
series.isTemplate
boolean | null
series.templateVariables
boolean | null
series.publishedAt
string | null
series.createdBy
string | null
series.updatedBy
string | null
series.createdAt
string <date-time> | null series.updatedAt string | null
series.commentsEnabled
boolean | null
series.competitive
string | null

series.volume24hr
number | null
series.volume
number | null
series.liquidity
number | null
series.startDate
string` | null
series.pythTokenID
string | null
series.cgAssetName
string | null
series.score
integer | null
series.events
array
series.collections
object[]
Hide child attributes
series.collections.id
string
series.collections.ticker
string | null
series.collections.slug
string | null
series.collections.title
string | null
series.collections.subtitle
string | null

series.collections.collectionType
string | null
series.collections.description
string | null
series.collections.tags
string | null
series.collections.image
string | null
series.collections.icon
string | null
series.collections.headerImage
string | null
series.collections.layout
string | null
series.collections.active
boolean | null
series.collections.closed
boolean | null
series.collections.archived
boolean | null
series.collections.new
boolean | null
series.collections.featured
boolean | null
series.collections.restricted
boolean | null
series.collections.isTemplate
boolean | null
series.collections.templateVariables

string | null
series.collections.publishedAt
string | null
series.collections.createdBy
string | null
series.collections.updatedBy
string | null
series.collections.createdAt
string <date-time> | null series.collections.updatedAt string | null
series.collections.commentsEnabled
boolean | null
series.collections.imageOptimized
object
Hide child attributes
series.collections.imageOptimized.id
string
series.collections.imageOptimized.imageUrlSource
string | null
series.collections.imageOptimized.imageUrlOptimized
string | null
series.collections.imageOptimized.imageSizeKbSource
number | null
series.collections.imageOptimized.imageSizeKbOptimized
number | null
series.collections.imageOptimized.imageOptimizedComplete
boolean | null
series.collections.imageOptimized.imageOptimizedLastUpdated
string | null
series.collections.imageOptimized.relID

integer | null
series.collections.imageOptimized.field
string | null
series.collections.imageOptimized.relname
string | null
series.collections.iconOptimized
object
Hide child attributes
series.collections.iconOptimized.id
string
series.collections.iconOptimized.imageUrlSource
string | null
series.collections.iconOptimized.imageUrlOptimized
string | null
series.collections.iconOptimized.imageSizeKbSource
number | null
series.collections.iconOptimized.imageSizeKbOptimized
number | null
series.collections.iconOptimized.imageOptimizedComplete
boolean | null
series.collections.iconOptimized.imageOptimizedLastUpdated
string | null
series.collections.iconOptimized.relID
integer | null
series.collections.iconOptimized.field
string | null
series.collections.iconOptimized.relname
string | null
series.collections.headerImageOptimized

object
Hide child attributes
series.collections.headerImageOptimized.id
string
series.collections.headerImageOptimized.imageUrlSource
string | null
series.collections.headerImageOptimized.imageUrlOptimized
string | null
series.collections.headerImageOptimized.imageSizeKbSource
number | null
series.collections.headerImageOptimized.imageSizeKbOptimized
number | null
series.collections.headerImageOptimized.imageOptimizedComplete
boolean | null
series.collections.headerImageOptimized.imageOptimizedLastUpdated
string | null
series.collections.headerImageOptimized.relID
integer | null
series.collections.headerImageOptimized.field
string | null
series.collections.headerImageOptimized.relname
string | null
series.categories
object[]
Hide child attributes
series.categories.id
string
series.categories.label
string | null

series.categories.parentCategory
string | null
series.categories.slug
string | null
series.categories.publishedAt
string | null
series.categories.createdBy
string | null
series.categories.updatedBy
string | null
series.categories.createdAt
string <date-time> | null series.categories.updatedAt string | null
series.tags
object[]
Hide child attributes
series.tags.id
string
series.tags.label
string | null
series.tags.slug
string | null
series.tags.forceShow
boolean | null
series.tags.publishedAt
string | null
series.tags.createdBy
integer | null
series.tags.updatedBy
integer | null

series.tags.createdAt
string <date-time> | null series.tags.updatedAt string | null
series.tags.forceHide
boolean | null
series.tags.isCarousel
boolean | null
series.commentCount
integer | null
series.chats
object[]
Hide child attributes
series.chats.id
string
series.chats.channelId
string | null
series.chats.channelName
string | null
series.chats.channelImage
string | null
series.chats.live
boolean | null
series.chats.startTime
string <date-time> | null series.chats.endTime string | null
categories
object[]
Hide child attributes
categories.id
string

categories.label
string | null
categories.parentCategory
string | null
categories.slug
string | null
categories.publishedAt
string | null
categories.createdBy
string | null
categories.updatedBy
string | null
categories.createdAt
string <date-time> | null categories.updatedAt string | null
collections
object[]
Hide child attributes
collections.id
string
collections.ticker
string | null
collections.slug
string | null
collections.title
string | null
collections.subtitle
string | null
collections.collectionType
string | null

collections.description
string | null
collections.tags
string | null
collections.image
string | null
collections.icon
string | null
collections.headerImage
string | null
collections.layout
string | null
collections.active
boolean | null
collections.closed
boolean | null
collections.archived
boolean | null
collections.new
boolean | null
collections.featured
boolean | null
collections.restricted
boolean | null
collections.isTemplate
boolean | null
collections.templateVariables
string | null
collections.publishedAt

string | null
collections.createdBy
string | null
collections.updatedBy
string | null
collections.createdAt
string <date-time> | null collections.updatedAt string | null
collections.commentsEnabled
boolean | null
collections.imageOptimized
object
Hide child attributes
collections.imageOptimized.id
string
collections.imageOptimized.imageUrlSource
string | null
collections.imageOptimized.imageUrlOptimized
string | null
collections.imageOptimized.imageSizeKbSource
number | null
collections.imageOptimized.imageSizeKbOptimized
number | null
collections.imageOptimized.imageOptimizedComplete
boolean | null
collections.imageOptimized.imageOptimizedLastUpdated
string | null
collections.imageOptimized.relID
integer | null
collections.imageOptimized.field

string | null
collections.imageOptimized.relname
string | null
collections.iconOptimized
object
Hide child attributes
collections.iconOptimized.id
string
collections.iconOptimized.imageUrlSource
string | null
collections.iconOptimized.imageUrlOptimized
string | null
collections.iconOptimized.imageSizeKbSource
number | null
collections.iconOptimized.imageSizeKbOptimized
number | null
collections.iconOptimized.imageOptimizedComplete
boolean | null
collections.iconOptimized.imageOptimizedLastUpdated
string | null
collections.iconOptimized.relID
integer | null
collections.iconOptimized.field
string | null
collections.iconOptimized.relname
string | null
collections.headerImageOptimized
object
Hide child attributes

collections.headerImageOptimized.id
string
collections.headerImageOptimized.imageUrlSource
string | null
collections.headerImageOptimized.imageUrlOptimized
string | null
collections.headerImageOptimized.imageSizeKbSource
number | null
collections.headerImageOptimized.imageSizeKbOptimized
number | null
collections.headerImageOptimized.imageOptimizedComplete
boolean | null
collections.headerImageOptimized.imageOptimizedLastUpdated
string | null
collections.headerImageOptimized.relID
integer | null
collections.headerImageOptimized.field
string | null
collections.headerImageOptimized.relname
string | null
tags
object[]
Hide child attributes
tags.id
string
tags.label
string | null
tags.slug
string | null
tags.forceShow

boolean | null
tags.publishedAt
string | null
tags.createdBy
integer | null
tags.updatedBy
integer | null
tags.createdAt
string <date-time> | null tags.updatedAt string | null
tags.forceHide
boolean | null
tags.isCarousel
boolean | null
cyom
boolean | null
closedTime
string <date-time> | null showAllOutcomes boolean | null showMarketImages boolean | null
automaticallyResolved boolean | null enableNegRisk boolean | null automaticallyActive boolean | null
eventDate string | null startTime string | null
eventWeek
integer | null
seriesSlug
string | null
score
string | null
elapsed
string | null
period
string | null

live
boolean | null
ended
boolean | null
finishedTimestamp
string` | null
gmpChartMode
string | null
eventCreators
object[]
Hide child attributes
eventCreators.id
string
eventCreators.creatorName
string | null
eventCreators.creatorHandle
string | null
eventCreators.creatorUrl
string | null
eventCreators.creatorImage
string | null
eventCreators.createdAt
string <date-time> | null eventCreators.updatedAt string | null
tweetCount
integer | null
chats
object[]
Hide child attributes
chats.id

string
chats.channelId
string | null
chats.channelName
string | null
chats.channelImage
string | null
chats.live
boolean | null
chats.startTime
string <date-time> | null chats.endTime string | null
featuredOrder
integer | null
estimateValue
boolean | null
cantEstimate
boolean | null
estimatedValue
string | null
templates
object[]
Hide child attributes
templates.id
string
templates.eventTitle
string | null
templates.eventSlug
string | null
templates.eventImage

string | null
templates.marketTitle
string | null
templates.description
string | null
templates.resolutionSource
string | null
templates.negRisk
boolean | null
templates.sortBy
string | null
templates.showMarketImages
boolean | null
templates.seriesSlug
string | null
templates.outcomes
string | null
spreadsMainLine
number | null
totalsMainLine
number | null
carouselMap
string | null
pendingDeployment
boolean | null
deploying
boolean | null
deployingTimestamp
string <date-time> | null scheduledDeploymentTimestamp string | null

gameStatus
string | null
Response
404
Not found
Get event tags
GET/events/{id}/tags
Get event tags
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/events/{id}/tags
Python
import requests
url = "https://gamma-api.polymarket.com/events/{id}/tags"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/events/{id}/tags', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/events/{id}/tags",
CURLOPT_RETURNTRANSFER => true,

CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/events/{id}/tags"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/events/{id}/tags")
.asString();
```
Ruby

require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/events/{id}/tags")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
]
Path Parameters
id
integer
required
Response
200 - application/json
Tags attached to the event
id
string

label
string | null
slug
string | null
forceShow
boolean | null
publishedAt
string | null
createdBy
integer | null
updatedBy
integer | null
createdAt
string` | null
updatedAt
string` | null
forceHide
boolean | null

isCarousel
boolean | null
Response
404
Not found
Get event by slug
GET/events/slug/{slug}
Get event by slug
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/events/slug/{slug}
Python
import requests
url = "https://gamma-api.polymarket.com/events/slug/{slug}"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/events/slug/{slug}', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP

<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/events/slug/{slug}",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/events/slug/{slug}"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java

HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/events/slug/{slug}")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/events/slug/{slug}")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"creationDate": "2023-11-07T05:31:56Z",
"endDate": "2023-11-07T05:31:56Z",
"image": "<string>",
"icon": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"liquidity": 123,
"volume": 123,
"openInterest": 123,
"sortBy": "<string>",
"category": "<string>",
"subcategory": "<string>",
"isTemplate": true,
"templateVariables": "<string>",
"published_at": "<string>",
"createdBy": "<string>",

"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"competitive": 123,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,
"featuredImage": "<string>",
"disqusThread": "<string>",
"parentEvent": "<string>",
"enableOrderBook": true,
"liquidityAmm": 123,
"liquidityClob": 123,
"negRisk": true,
"negRiskMarketID": "<string>",
"negRiskFeeBips": 123,
"commentCount": 123,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"featuredImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,

"field": "<string>",
"relname": "<string>"
},
"subEvents": [
"<string>"
],
"markets": [
{
"id": "<string>",
"question": "<string>",
"conditionId": "<string>",
"slug": "<string>",
"twitterCardImage": "<string>",
"resolutionSource": "<string>",
"endDate": "2023-11-07T05:31:56Z",
"category": "<string>",
"ammType": "<string>",
"liquidity": "<string>",
"sponsorName": "<string>",
"sponsorImage": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"xAxisValue": "<string>",
"yAxisValue": "<string>",
"denominationToken": "<string>",
"fee": "<string>",
"image": "<string>",
"icon": "<string>",
"lowerBound": "<string>",
"upperBound": "<string>",
"description": "<string>",
"outcomes": "<string>",
"outcomePrices": "<string>",
"volume": "<string>",
"active": true,
"marketType": "<string>",
"formatType": "<string>",
"lowerBoundDate": "<string>",
"upperBoundDate": "<string>",
"closed": true,
"marketMakerAddress": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"closedTime": "<string>",
"wideFormat": true,
"new": true,
"mailchimpTag": "<string>",
"featured": true,
"archived": true,
"resolvedBy": "<string>",
"restricted": true,

"marketGroup": 123,
"groupItemTitle": "<string>",
"groupItemThreshold": "<string>",
"questionID": "<string>",
"umaEndDate": "<string>",
"enableOrderBook": true,
"orderPriceMinTickSize": 123,
"orderMinSize": 123,
"umaResolutionStatus": "<string>",
"curationOrder": 123,
"volumeNum": 123,
"liquidityNum": 123,
"endDateIso": "<string>",
"startDateIso": "<string>",
"umaEndDateIso": "<string>",
"hasReviewedDates": true,
"readyForCron": true,
"commentsEnabled": true,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,
"gameStartTime": "<string>",
"secondsDelay": 123,
"clobTokenIds": "<string>",
"disqusThread": "<string>",
"shortOutcomes": "<string>",
"teamAID": "<string>",
"teamBID": "<string>",
"umaBond": "<string>",
"umaReward": "<string>",
"fpmmLive": true,
"volume24hrAmm": 123,
"volume1wkAmm": 123,
"volume1moAmm": 123,
"volume1yrAmm": 123,
"volume24hrClob": 123,
"volume1wkClob": 123,
"volume1moClob": 123,
"volume1yrClob": 123,
"volumeAmm": 123,
"volumeClob": 123,
"liquidityAmm": 123,
"liquidityClob": 123,
"makerBaseFee": 123,
"takerBaseFee": 123,
"customLiveness": 123,
"acceptingOrders": true,
"notificationsEnabled": true,
"score": 123,
"imageOptimized": {
"id": "<string>",

"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"events": "<array>",
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"creator": "<string>",

"ready": true,
"funded": true,
"pastSlugs": "<string>",
"readyTimestamp": "2023-11-07T05:31:56Z",
"fundedTimestamp": "2023-11-07T05:31:56Z",
"acceptingOrdersTimestamp": "2023-11-07T05:31:56Z",
"competitive": 123,
"rewardsMinSize": 123,
"rewardsMaxSpread": 123,
"spread": 123,
"automaticallyResolved": true,
"oneDayPriceChange": 123,
"oneHourPriceChange": 123,
"oneWeekPriceChange": 123,
"oneMonthPriceChange": 123,
"oneYearPriceChange": 123,
"lastTradePrice": 123,
"bestBid": 123,
"bestAsk": 123,
"automaticallyActive": true,
"clearBookOnStart": true,
"chartColor": "<string>",
"seriesColor": "<string>",
"showGmpSeries": true,
"showGmpOutcome": true,
"manualActivation": true,
"negRiskOther": true,
"gameId": "<string>",
"groupItemRange": "<string>",
"sportsMarketType": "<string>",
"line": 123,
"umaResolutionStatuses": "<string>",
"pendingDeployment": true,
"deploying": true,
"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",
"rfqEnabled": true,
"eventStartTime": "2023-11-07T05:31:56Z"
}
],
"series": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"seriesType": "<string>",
"recurrence": "<string>",
"description": "<string>",
"image": "<string>",
"icon": "<string>",

"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": true,
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"competitive": "<string>",
"volume24hr": 123,
"volume": 123,
"liquidity": 123,
"startDate": "2023-11-07T05:31:56Z",
"pythTokenID": "<string>",
"cgAssetName": "<string>",
"score": 123,
"events": "<array>",
"collections": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",
"image": "<string>",
"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,

"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
}
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tags": [

{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"commentCount": 123,
"chats": [
{
"id": "<string>",
"channelId": "<string>",
"channelName": "<string>",
"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",
"endTime": "2023-11-07T05:31:56Z"
}
]
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"collections": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",
"image": "<string>",

"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"

}
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"cyom": true,
"closedTime": "2023-11-07T05:31:56Z",
"showAllOutcomes": true,
"showMarketImages": true,
"automaticallyResolved": true,
"enableNegRisk": true,
"automaticallyActive": true,
"eventDate": "<string>",
"startTime": "2023-11-07T05:31:56Z",
"eventWeek": 123,
"seriesSlug": "<string>",
"score": "<string>",
"elapsed": "<string>",
"period": "<string>",
"live": true,
"ended": true,
"finishedTimestamp": "2023-11-07T05:31:56Z",
"gmpChartMode": "<string>",
"eventCreators": [
{
"id": "<string>",
"creatorName": "<string>",
"creatorHandle": "<string>",
"creatorUrl": "<string>",
"creatorImage": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tweetCount": 123,
"chats": [
{
"id": "<string>",
"channelId": "<string>",

"channelName": "<string>",
"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",
"endTime": "2023-11-07T05:31:56Z"
}
],
"featuredOrder": 123,
"estimateValue": true,
"cantEstimate": true,
"estimatedValue": "<string>",
"templates": [
{
"id": "<string>",
"eventTitle": "<string>",
"eventSlug": "<string>",
"eventImage": "<string>",
"marketTitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",
"negRisk": true,
"sortBy": "<string>",
"showMarketImages": true,
"seriesSlug": "<string>",
"outcomes": "<string>"
}
],
"spreadsMainLine": 123,
"totalsMainLine": 123,
"carouselMap": "<string>",
"pendingDeployment": true,
"deploying": true,
"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",
"gameStatus": "<string>"
}
Path Parameters
slug
string
required
Query Parameters

include_chat
boolean
include_template
boolean
Response
200 - application/json
Event
id
string
ticker
string | null
slug
string | null
title
string | null
subtitle
string | null
description
string | null
resolutionSource
string | null
startDate
string <date-time> | null creationDate string | null
endDate
string <date-time> | null image string | null icon string | null active boolean | null closed boolean | null
archived boolean | null new boolean | null featured boolean | null restricted boolean | null liquidity
number | null volume number | null openInterest number | null sortBy string | null category string | null
subcategory string | null isTemplate boolean | null templateVariables string | null published_at string |
null createdBy string | null updatedBy string | null createdAt string | null

updatedAt
string` | null
commentsEnabled
boolean | null
competitive
number | null
volume24hr
number | null
volume1wk
number | null
volume1mo
number | null
volume1yr
number | null
featuredImage
string | null
disqusThread
string | null
parentEvent
string | null
enableOrderBook
boolean | null
liquidityAmm
number | null
liquidityClob
number | null
negRisk
boolean | null
negRiskMarketID

string | null
negRiskFeeBips
integer | null
commentCount
integer | null
imageOptimized
object
Hide child attributes
imageOptimized.id
string
imageOptimized.imageUrlSource
string | null
imageOptimized.imageUrlOptimized
string | null
imageOptimized.imageSizeKbSource
number | null
imageOptimized.imageSizeKbOptimized
number | null
imageOptimized.imageOptimizedComplete
boolean | null
imageOptimized.imageOptimizedLastUpdated
string | null
imageOptimized.relID
integer | null
imageOptimized.field
string | null
imageOptimized.relname
string | null
iconOptimized

object
Hide child attributes
iconOptimized.id
string
iconOptimized.imageUrlSource
string | null
iconOptimized.imageUrlOptimized
string | null
iconOptimized.imageSizeKbSource
number | null
iconOptimized.imageSizeKbOptimized
number | null
iconOptimized.imageOptimizedComplete
boolean | null
iconOptimized.imageOptimizedLastUpdated
string | null
iconOptimized.relID
integer | null
iconOptimized.field
string | null
iconOptimized.relname
string | null
featuredImageOptimized
object
Hide child attributes
featuredImageOptimized.id
string
featuredImageOptimized.imageUrlSource
string | null

featuredImageOptimized.imageUrlOptimized
string | null
featuredImageOptimized.imageSizeKbSource
number | null
featuredImageOptimized.imageSizeKbOptimized
number | null
featuredImageOptimized.imageOptimizedComplete
boolean | null
featuredImageOptimized.imageOptimizedLastUpdated
string | null
featuredImageOptimized.relID
integer | null
featuredImageOptimized.field
string | null
featuredImageOptimized.relname
string | null
subEvents
string[] | null
markets
object[]
Hide child attributes
markets.id
string
markets.question
string | null
markets.conditionId
string
markets.slug
string | null

markets.twitterCardImage
string | null
markets.resolutionSource
string | null
markets.endDate
string <date-time> | null markets.category string | null markets.ammType string | null markets.liquidity
string | null markets.sponsorName string | null markets.sponsorImage string | null markets.startDate
string | null
markets.xAxisValue
string | null
markets.yAxisValue
string | null
markets.denominationToken
string | null
markets.fee
string | null
markets.image
string | null
markets.icon
string | null
markets.lowerBound
string | null
markets.upperBound
string | null
markets.description
string | null
markets.outcomes
string | null
markets.outcomePrices

string | null
markets.volume
string | null
markets.active
boolean | null
markets.marketType
string | null
markets.formatType
string | null
markets.lowerBoundDate
string | null
markets.upperBoundDate
string | null
markets.closed
boolean | null
markets.marketMakerAddress
string
markets.createdBy
integer | null
markets.updatedBy
integer | null
markets.createdAt
string <date-time> | null markets.updatedAt string | null
markets.closedTime
string | null
markets.wideFormat
boolean | null
markets.new
boolean | null

markets.mailchimpTag
string | null
markets.featured
boolean | null
markets.archived
boolean | null
markets.resolvedBy
string | null
markets.restricted
boolean | null
markets.marketGroup
integer | null
markets.groupItemTitle
string | null
markets.groupItemThreshold
string | null
markets.questionID
string | null
markets.umaEndDate
string | null
markets.enableOrderBook
boolean | null
markets.orderPriceMinTickSize
number | null
markets.orderMinSize
number | null
markets.umaResolutionStatus
string | null

markets.curationOrder
integer | null
markets.volumeNum
number | null
markets.liquidityNum
number | null
markets.endDateIso
string | null
markets.startDateIso
string | null
markets.umaEndDateIso
string | null
markets.hasReviewedDates
boolean | null
markets.readyForCron
boolean | null
markets.commentsEnabled
boolean | null
markets.volume24hr
number | null
markets.volume1wk
number | null
markets.volume1mo
number | null
markets.volume1yr
number | null
markets.gameStartTime
string | null
markets.secondsDelay

integer | null
markets.clobTokenIds
string | null
markets.disqusThread
string | null
markets.shortOutcomes
string | null
markets.teamAID
string | null
markets.teamBID
string | null
markets.umaBond
string | null
markets.umaReward
string | null
markets.fpmmLive
boolean | null
markets.volume24hrAmm
number | null
markets.volume1wkAmm
number | null
markets.volume1moAmm
number | null
markets.volume1yrAmm
number | null
markets.volume24hrClob
number | null
markets.volume1wkClob
number | null

markets.volume1moClob
number | null
markets.volume1yrClob
number | null
markets.volumeAmm
number | null
markets.volumeClob
number | null
markets.liquidityAmm
number | null
markets.liquidityClob
number | null
markets.makerBaseFee
integer | null
markets.takerBaseFee
integer | null
markets.customLiveness
integer | null
markets.acceptingOrders
boolean | null
markets.notificationsEnabled
boolean | null
markets.score
integer | null
markets.imageOptimized
object
Hide child attributes
markets.imageOptimized.id
string

markets.imageOptimized.imageUrlSource
string | null
markets.imageOptimized.imageUrlOptimized
string | null
markets.imageOptimized.imageSizeKbSource
number | null
markets.imageOptimized.imageSizeKbOptimized
number | null
markets.imageOptimized.imageOptimizedComplete
boolean | null
markets.imageOptimized.imageOptimizedLastUpdated
string | null
markets.imageOptimized.relID
integer | null
markets.imageOptimized.field
string | null
markets.imageOptimized.relname
string | null
markets.iconOptimized
object
Hide child attributes
markets.iconOptimized.id
string
markets.iconOptimized.imageUrlSource
string | null
markets.iconOptimized.imageUrlOptimized
string | null
markets.iconOptimized.imageSizeKbSource
number | null

markets.iconOptimized.imageSizeKbOptimized
number | null
markets.iconOptimized.imageOptimizedComplete
boolean | null
markets.iconOptimized.imageOptimizedLastUpdated
string | null
markets.iconOptimized.relID
integer | null
markets.iconOptimized.field
string | null
markets.iconOptimized.relname
string | null
markets.events
array
markets.categories
object[]
Hide child attributes
markets.categories.id
string
markets.categories.label
string | null
markets.categories.parentCategory
string | null
markets.categories.slug
string | null
markets.categories.publishedAt
string | null
markets.categories.createdBy
string | null

markets.categories.updatedBy
string | null
markets.categories.createdAt
string <date-time> | null markets.categories.updatedAt string | null
markets.tags
object[]
Hide child attributes
markets.tags.id
string
markets.tags.label
string | null
markets.tags.slug
string | null
markets.tags.forceShow
boolean | null
markets.tags.publishedAt
string | null
markets.tags.createdBy
integer | null
markets.tags.updatedBy
integer | null
markets.tags.createdAt
string <date-time> | null markets.tags.updatedAt string | null
markets.tags.forceHide
boolean | null
markets.tags.isCarousel
boolean | null
markets.creator
string | null

markets.ready
boolean | null
markets.funded
boolean | null
markets.pastSlugs
string | null
markets.readyTimestamp
string <date-time> | null markets.fundedTimestamp string | null
markets.acceptingOrdersTimestamp
string <date-time> | null markets.competitive number | null markets.rewardsMinSize number | null
markets.rewardsMaxSpread number | null markets.spread number | null markets.automaticallyResolved
boolean | null markets.oneDayPriceChange number | null markets.oneHourPriceChange number | null
markets.oneWeekPriceChange number | null markets.oneMonthPriceChange number | null
markets.oneYearPriceChange number | null markets.lastTradePrice number | null markets.bestBid
number | null markets.bestAsk number | null markets.automaticallyActive boolean | null
markets.clearBookOnStart boolean | null markets.chartColor string | null markets.seriesColor string | null
markets.showGmpSeries boolean | null markets.showGmpOutcome boolean | null
markets.manualActivation boolean | null markets.negRiskOther boolean | null markets.gameId string |
null markets.groupItemRange string | null markets.sportsMarketType string | null markets.line number |
null markets.umaResolutionStatuses string | null markets.pendingDeployment boolean | null
markets.deploying boolean | null markets.deployingTimestamp string | null
markets.scheduledDeploymentTimestamp
string <date-time> | null markets.rfqEnabled boolean | null markets.eventStartTime string | null
series
object[]
Hide child attributes
series.id
string
series.ticker
string | null
series.slug
string | null
series.title

string | null
series.subtitle
string | null
series.seriesType
string | null
series.recurrence
string | null
series.description
string | null
series.image
string | null
series.icon
string | null
series.layout
string | null
series.active
boolean | null
series.closed
boolean | null
series.archived
boolean | null
series.new
boolean | null
series.featured
boolean | null
series.restricted
boolean | null
series.isTemplate
boolean | null

series.templateVariables
boolean | null
series.publishedAt
string | null
series.createdBy
string | null
series.updatedBy
string | null
series.createdAt
string <date-time> | null series.updatedAt string | null
series.commentsEnabled
boolean | null
series.competitive
string | null
series.volume24hr
number | null
series.volume
number | null
series.liquidity
number | null
series.startDate
string` | null
series.pythTokenID
string | null
series.cgAssetName
string | null
series.score
integer | null

series.events
array
series.collections
object[]
Hide child attributes
series.collections.id
string
series.collections.ticker
string | null
series.collections.slug
string | null
series.collections.title
string | null
series.collections.subtitle
string | null
series.collections.collectionType
string | null
series.collections.description
string | null
series.collections.tags
string | null
series.collections.image
string | null
series.collections.icon
string | null
series.collections.headerImage
string | null
series.collections.layout
string | null

series.collections.active
boolean | null
series.collections.closed
boolean | null
series.collections.archived
boolean | null
series.collections.new
boolean | null
series.collections.featured
boolean | null
series.collections.restricted
boolean | null
series.collections.isTemplate
boolean | null
series.collections.templateVariables
string | null
series.collections.publishedAt
string | null
series.collections.createdBy
string | null
series.collections.updatedBy
string | null
series.collections.createdAt
string <date-time> | null series.collections.updatedAt string | null
series.collections.commentsEnabled
boolean | null
series.collections.imageOptimized
object
Hide child attributes

series.collections.imageOptimized.id
string
series.collections.imageOptimized.imageUrlSource
string | null
series.collections.imageOptimized.imageUrlOptimized
string | null
series.collections.imageOptimized.imageSizeKbSource
number | null
series.collections.imageOptimized.imageSizeKbOptimized
number | null
series.collections.imageOptimized.imageOptimizedComplete
boolean | null
series.collections.imageOptimized.imageOptimizedLastUpdated
string | null
series.collections.imageOptimized.relID
integer | null
series.collections.imageOptimized.field
string | null
series.collections.imageOptimized.relname
string | null
series.collections.iconOptimized
object
Hide child attributes
series.collections.iconOptimized.id
string
series.collections.iconOptimized.imageUrlSource
string | null
series.collections.iconOptimized.imageUrlOptimized
string | null

series.collections.iconOptimized.imageSizeKbSource
number | null
series.collections.iconOptimized.imageSizeKbOptimized
number | null
series.collections.iconOptimized.imageOptimizedComplete
boolean | null
series.collections.iconOptimized.imageOptimizedLastUpdated
string | null
series.collections.iconOptimized.relID
integer | null
series.collections.iconOptimized.field
string | null
series.collections.iconOptimized.relname
string | null
series.collections.headerImageOptimized
object
Hide child attributes
series.collections.headerImageOptimized.id
string
series.collections.headerImageOptimized.imageUrlSource
string | null
series.collections.headerImageOptimized.imageUrlOptimized
string | null
series.collections.headerImageOptimized.imageSizeKbSource
number | null
series.collections.headerImageOptimized.imageSizeKbOptimized
number | null
series.collections.headerImageOptimized.imageOptimizedComplete
boolean | null

series.collections.headerImageOptimized.imageOptimizedLastUpdated
string | null
series.collections.headerImageOptimized.relID
integer | null
series.collections.headerImageOptimized.field
string | null
series.collections.headerImageOptimized.relname
string | null
series.categories
object[]
Hide child attributes
series.categories.id
string
series.categories.label
string | null
series.categories.parentCategory
string | null
series.categories.slug
string | null
series.categories.publishedAt
string | null
series.categories.createdBy
string | null
series.categories.updatedBy
string | null
series.categories.createdAt
string <date-time> | null series.categories.updatedAt string | null
series.tags

object[]
Hide child attributes
series.tags.id
string
series.tags.label
string | null
series.tags.slug
string | null
series.tags.forceShow
boolean | null
series.tags.publishedAt
string | null
series.tags.createdBy
integer | null
series.tags.updatedBy
integer | null
series.tags.createdAt
string <date-time> | null series.tags.updatedAt string | null
series.tags.forceHide
boolean | null
series.tags.isCarousel
boolean | null
series.commentCount
integer | null
series.chats
object[]
Hide child attributes
series.chats.id
string

series.chats.channelId
string | null
series.chats.channelName
string | null
series.chats.channelImage
string | null
series.chats.live
boolean | null
series.chats.startTime
string <date-time> | null series.chats.endTime string | null
categories
object[]
Hide child attributes
categories.id
string
categories.label
string | null
categories.parentCategory
string | null
categories.slug
string | null
categories.publishedAt
string | null
categories.createdBy
string | null
categories.updatedBy
string | null
categories.createdAt
string <date-time> | null categories.updatedAt string | null

collections
object[]
Hide child attributes
collections.id
string
collections.ticker
string | null
collections.slug
string | null
collections.title
string | null
collections.subtitle
string | null
collections.collectionType
string | null
collections.description
string | null
collections.tags
string | null
collections.image
string | null
collections.icon
string | null
collections.headerImage
string | null
collections.layout
string | null
collections.active
boolean | null

collections.closed
boolean | null
collections.archived
boolean | null
collections.new
boolean | null
collections.featured
boolean | null
collections.restricted
boolean | null
collections.isTemplate
boolean | null
collections.templateVariables
string | null
collections.publishedAt
string | null
collections.createdBy
string | null
collections.updatedBy
string | null
collections.createdAt
string <date-time> | null collections.updatedAt string | null
collections.commentsEnabled
boolean | null
collections.imageOptimized
object
Hide child attributes
collections.imageOptimized.id
string

collections.imageOptimized.imageUrlSource
string | null
collections.imageOptimized.imageUrlOptimized
string | null
collections.imageOptimized.imageSizeKbSource
number | null
collections.imageOptimized.imageSizeKbOptimized
number | null
collections.imageOptimized.imageOptimizedComplete
boolean | null
collections.imageOptimized.imageOptimizedLastUpdated
string | null
collections.imageOptimized.relID
integer | null
collections.imageOptimized.field
string | null
collections.imageOptimized.relname
string | null
collections.iconOptimized
object
Hide child attributes
collections.iconOptimized.id
string
collections.iconOptimized.imageUrlSource
string | null
collections.iconOptimized.imageUrlOptimized
string | null
collections.iconOptimized.imageSizeKbSource
number | null

collections.iconOptimized.imageSizeKbOptimized
number | null
collections.iconOptimized.imageOptimizedComplete
boolean | null
collections.iconOptimized.imageOptimizedLastUpdated
string | null
collections.iconOptimized.relID
integer | null
collections.iconOptimized.field
string | null
collections.iconOptimized.relname
string | null
collections.headerImageOptimized
object
Hide child attributes
collections.headerImageOptimized.id
string
collections.headerImageOptimized.imageUrlSource
string | null
collections.headerImageOptimized.imageUrlOptimized
string | null
collections.headerImageOptimized.imageSizeKbSource
number | null
collections.headerImageOptimized.imageSizeKbOptimized
number | null
collections.headerImageOptimized.imageOptimizedComplete
boolean | null
collections.headerImageOptimized.imageOptimizedLastUpdated
string | null

collections.headerImageOptimized.relID
integer | null
collections.headerImageOptimized.field
string | null
collections.headerImageOptimized.relname
string | null
tags
object[]
Hide child attributes
tags.id
string
tags.label
string | null
tags.slug
string | null
tags.forceShow
boolean | null
tags.publishedAt
string | null
tags.createdBy
integer | null
tags.updatedBy
integer | null
tags.createdAt
string <date-time> | null tags.updatedAt string | null
tags.forceHide
boolean | null
tags.isCarousel
boolean | null
cyom

boolean | null
closedTime
string <date-time> | null showAllOutcomes boolean | null showMarketImages boolean | null
automaticallyResolved boolean | null enableNegRisk boolean | null automaticallyActive boolean | null
eventDate string | null startTime string | null
eventWeek
integer | null
seriesSlug
string | null
score
string | null
elapsed
string | null
period
string | null
live
boolean | null
ended
boolean | null
finishedTimestamp
string` | null
gmpChartMode
string | null
eventCreators
object[]
Hide child attributes
eventCreators.id
string
eventCreators.creatorName
string | null

eventCreators.creatorHandle
string | null
eventCreators.creatorUrl
string | null
eventCreators.creatorImage
string | null
eventCreators.createdAt
string <date-time> | null eventCreators.updatedAt string | null
tweetCount
integer | null
chats
object[]
Hide child attributes
chats.id
string
chats.channelId
string | null
chats.channelName
string | null
chats.channelImage
string | null
chats.live
boolean | null
chats.startTime
string <date-time> | null chats.endTime string | null
featuredOrder
integer | null
estimateValue
boolean | null

cantEstimate
boolean | null
estimatedValue
string | null
templates
object[]
Hide child attributes
templates.id
string
templates.eventTitle
string | null
templates.eventSlug
string | null
templates.eventImage
string | null
templates.marketTitle
string | null
templates.description
string | null
templates.resolutionSource
string | null
templates.negRisk
boolean | null
templates.sortBy
string | null
templates.showMarketImages
boolean | null
templates.seriesSlug
string | null

templates.outcomes
string | null
spreadsMainLine
number | null
totalsMainLine
number | null
carouselMap
string | null
pendingDeployment
boolean | null
deploying
boolean | null
deployingTimestamp
string <date-time> | null scheduledDeploymentTimestamp string | null
gameStatus
string | null
List markets
GET/markets
List markets
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/markets
Python
import requests
url = "https://gamma-api.polymarket.com/markets"
response = requests.get(url)
print(response.text)
JavaScript

const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/markets', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/markets",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/markets"
req, _ := http.NewRequest("GET", url, nil)

res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/markets")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/markets")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"id": "<string>",
"question": "<string>",
"conditionId": "<string>",
"slug": "<string>",
"twitterCardImage": "<string>",
"resolutionSource": "<string>",
"endDate": "2023-11-07T05:31:56Z",
"category": "<string>",
"ammType": "<string>",
"liquidity": "<string>",
"sponsorName": "<string>",
"sponsorImage": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"xAxisValue": "<string>",
"yAxisValue": "<string>",
"denominationToken": "<string>",

"fee": "<string>",
"image": "<string>",
"icon": "<string>",
"lowerBound": "<string>",
"upperBound": "<string>",
"description": "<string>",
"outcomes": "<string>",
"outcomePrices": "<string>",
"volume": "<string>",
"active": true,
"marketType": "<string>",
"formatType": "<string>",
"lowerBoundDate": "<string>",
"upperBoundDate": "<string>",
"closed": true,
"marketMakerAddress": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"closedTime": "<string>",
"wideFormat": true,
"new": true,
"mailchimpTag": "<string>",
"featured": true,
"archived": true,
"resolvedBy": "<string>",
"restricted": true,
"marketGroup": 123,
"groupItemTitle": "<string>",
"groupItemThreshold": "<string>",
"questionID": "<string>",
"umaEndDate": "<string>",
"enableOrderBook": true,
"orderPriceMinTickSize": 123,
"orderMinSize": 123,
"umaResolutionStatus": "<string>",
"curationOrder": 123,
"volumeNum": 123,
"liquidityNum": 123,
"endDateIso": "<string>",
"startDateIso": "<string>",
"umaEndDateIso": "<string>",
"hasReviewedDates": true,
"readyForCron": true,
"commentsEnabled": true,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,
"gameStartTime": "<string>",
"secondsDelay": 123,

"clobTokenIds": "<string>",
"disqusThread": "<string>",
"shortOutcomes": "<string>",
"teamAID": "<string>",
"teamBID": "<string>",
"umaBond": "<string>",
"umaReward": "<string>",
"fpmmLive": true,
"volume24hrAmm": 123,
"volume1wkAmm": 123,
"volume1moAmm": 123,
"volume1yrAmm": 123,
"volume24hrClob": 123,
"volume1wkClob": 123,
"volume1moClob": 123,
"volume1yrClob": 123,
"volumeAmm": 123,
"volumeClob": 123,
"liquidityAmm": 123,
"liquidityClob": 123,
"makerBaseFee": 123,
"takerBaseFee": 123,
"customLiveness": 123,
"acceptingOrders": true,
"notificationsEnabled": true,
"score": 123,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"events": [
{

"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"creationDate": "2023-11-07T05:31:56Z",
"endDate": "2023-11-07T05:31:56Z",
"image": "<string>",
"icon": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"liquidity": 123,
"volume": 123,
"openInterest": 123,
"sortBy": "<string>",
"category": "<string>",
"subcategory": "<string>",
"isTemplate": true,
"templateVariables": "<string>",
"published_at": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"competitive": 123,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,
"featuredImage": "<string>",
"disqusThread": "<string>",
"parentEvent": "<string>",
"enableOrderBook": true,
"liquidityAmm": 123,
"liquidityClob": 123,
"negRisk": true,
"negRiskMarketID": "<string>",
"negRiskFeeBips": 123,
"commentCount": 123,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,

"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"featuredImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"subEvents": [
"<string>"
],
"markets": "<array>",
"series": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"seriesType": "<string>",
"recurrence": "<string>",
"description": "<string>",
"image": "<string>",
"icon": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,

"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": true,
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"competitive": "<string>",
"volume24hr": 123,
"volume": 123,
"liquidity": 123,
"startDate": "2023-11-07T05:31:56Z",
"pythTokenID": "<string>",
"cgAssetName": "<string>",
"score": 123,
"events": "<array>",
"collections": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",
"image": "<string>",
"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,

"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
}
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,

"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"commentCount": 123,
"chats": [
{
"id": "<string>",
"channelId": "<string>",
"channelName": "<string>",
"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",
"endTime": "2023-11-07T05:31:56Z"
}
]
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"collections": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",
"image": "<string>",
"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,
"closed": true,

"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
}
}
],
"tags": [
{

"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"cyom": true,
"closedTime": "2023-11-07T05:31:56Z",
"showAllOutcomes": true,
"showMarketImages": true,
"automaticallyResolved": true,
"enableNegRisk": true,
"automaticallyActive": true,
"eventDate": "<string>",
"startTime": "2023-11-07T05:31:56Z",
"eventWeek": 123,
"seriesSlug": "<string>",
"score": "<string>",
"elapsed": "<string>",
"period": "<string>",
"live": true,
"ended": true,
"finishedTimestamp": "2023-11-07T05:31:56Z",
"gmpChartMode": "<string>",
"eventCreators": [
{
"id": "<string>",
"creatorName": "<string>",
"creatorHandle": "<string>",
"creatorUrl": "<string>",
"creatorImage": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tweetCount": 123,
"chats": [
{
"id": "<string>",
"channelId": "<string>",
"channelName": "<string>",
"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",
"endTime": "2023-11-07T05:31:56Z"

}
],
"featuredOrder": 123,
"estimateValue": true,
"cantEstimate": true,
"estimatedValue": "<string>",
"templates": [
{
"id": "<string>",
"eventTitle": "<string>",
"eventSlug": "<string>",
"eventImage": "<string>",
"marketTitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",
"negRisk": true,
"sortBy": "<string>",
"showMarketImages": true,
"seriesSlug": "<string>",
"outcomes": "<string>"
}
],
"spreadsMainLine": 123,
"totalsMainLine": 123,
"carouselMap": "<string>",
"pendingDeployment": true,
"deploying": true,
"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",
"gameStatus": "<string>"
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",

"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"creator": "<string>",
"ready": true,
"funded": true,
"pastSlugs": "<string>",
"readyTimestamp": "2023-11-07T05:31:56Z",
"fundedTimestamp": "2023-11-07T05:31:56Z",
"acceptingOrdersTimestamp": "2023-11-07T05:31:56Z",
"competitive": 123,
"rewardsMinSize": 123,
"rewardsMaxSpread": 123,
"spread": 123,
"automaticallyResolved": true,
"oneDayPriceChange": 123,
"oneHourPriceChange": 123,
"oneWeekPriceChange": 123,
"oneMonthPriceChange": 123,
"oneYearPriceChange": 123,
"lastTradePrice": 123,
"bestBid": 123,
"bestAsk": 123,
"automaticallyActive": true,
"clearBookOnStart": true,
"chartColor": "<string>",
"seriesColor": "<string>",
"showGmpSeries": true,
"showGmpOutcome": true,
"manualActivation": true,
"negRiskOther": true,
"gameId": "<string>",
"groupItemRange": "<string>",
"sportsMarketType": "<string>",
"line": 123,
"umaResolutionStatuses": "<string>",
"pendingDeployment": true,
"deploying": true,
"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",
"rfqEnabled": true,
"eventStartTime": "2023-11-07T05:31:56Z"
}
]
Query Parameters

limit
integer
Required range: x >= 0
offset
integer
Required range: x >= 0
order
string
Comma-separated list of fields to order by
ascending
boolean
id
integer[]
slug
string[]
clob_token_ids
string[]
condition_ids
string[]
market_maker_address
string[]
liquidity_num_min
number
liquidity_num_max
number
volume_num_min
number
volume_num_max
number

start_date_min
string <date-time> start_date_max string
end_date_min
string <date-time> end_date_max string
tag_id
integer
related_tags
boolean
cyom
boolean
uma_resolution_status
string
game_id
string
sports_market_types
string[]
rewards_min_size
number
question_ids
string[]
include_tag
boolean
closed
boolean
Response
200 - application/json
List of markets
id

string
question
string | null
conditionId
string
slug
string | null
twitterCardImage
string | null
resolutionSource
string | null
endDate
string <date-time> | null category string | null ammType string | null liquidity string | null sponsorName
string | null sponsorImage string | null startDate string | null
xAxisValue
string | null
yAxisValue
string | null
denominationToken
string | null
fee
string | null
image
string | null
icon
string | null
lowerBound
string | null
upperBound

string | null
description
string | null
outcomes
string | null
outcomePrices
string | null
volume
string | null
active
boolean | null
marketType
string | null
formatType
string | null
lowerBoundDate
string | null
upperBoundDate
string | null
closed
boolean | null
marketMakerAddress
string
createdBy
integer | null
updatedBy
integer | null
createdAt
string <date-time> | null updatedAt string | null

closedTime
string | null
wideFormat
boolean | null
new
boolean | null
mailchimpTag
string | null
featured
boolean | null
archived
boolean | null
resolvedBy
string | null
restricted
boolean | null
marketGroup
integer | null
groupItemTitle
string | null
groupItemThreshold
string | null
questionID
string | null
umaEndDate
string | null
enableOrderBook
boolean | null

orderPriceMinTickSize
number | null
orderMinSize
number | null
umaResolutionStatus
string | null
curationOrder
integer | null
volumeNum
number | null
liquidityNum
number | null
endDateIso
string | null
startDateIso
string | null
umaEndDateIso
string | null
hasReviewedDates
boolean | null
readyForCron
boolean | null
commentsEnabled
boolean | null
volume24hr
number | null
volume1wk
number | null
volume1mo

number | null
volume1yr
number | null
gameStartTime
string | null
secondsDelay
integer | null
clobTokenIds
string | null
disqusThread
string | null
shortOutcomes
string | null
teamAID
string | null
teamBID
string | null
umaBond
string | null
umaReward
string | null
fpmmLive
boolean | null
volume24hrAmm
number | null
volume1wkAmm
number | null
volume1moAmm
number | null

volume1yrAmm
number | null
volume24hrClob
number | null
volume1wkClob
number | null
volume1moClob
number | null
volume1yrClob
number | null
volumeAmm
number | null
volumeClob
number | null
liquidityAmm
number | null
liquidityClob
number | null
makerBaseFee
integer | null
takerBaseFee
integer | null
customLiveness
integer | null
acceptingOrders
boolean | null
notificationsEnabled
boolean | null

score
integer | null
imageOptimized
object
Hide child attributes
imageOptimized.id
string
imageOptimized.imageUrlSource
string | null
imageOptimized.imageUrlOptimized
string | null
imageOptimized.imageSizeKbSource
number | null
imageOptimized.imageSizeKbOptimized
number | null
imageOptimized.imageOptimizedComplete
boolean | null
imageOptimized.imageOptimizedLastUpdated
string | null
imageOptimized.relID
integer | null
imageOptimized.field
string | null
imageOptimized.relname
string | null
iconOptimized
object
Hide child attributes
iconOptimized.id

string
iconOptimized.imageUrlSource
string | null
iconOptimized.imageUrlOptimized
string | null
iconOptimized.imageSizeKbSource
number | null
iconOptimized.imageSizeKbOptimized
number | null
iconOptimized.imageOptimizedComplete
boolean | null
iconOptimized.imageOptimizedLastUpdated
string | null
iconOptimized.relID
integer | null
iconOptimized.field
string | null
iconOptimized.relname
string | null
events
object[]
Hide child attributes
events.id
string
events.ticker
string | null
events.slug
string | null
events.title

string | null
events.subtitle
string | null
events.description
string | null
events.resolutionSource
string | null
events.startDate
string <date-time> | null events.creationDate string | null
events.endDate
string <date-time> | null events.image string | null events.icon string | null events.active boolean | null
events.closed boolean | null events.archived boolean | null events.new boolean | null events.featured
boolean | null events.restricted boolean | null events.liquidity number | null events.volume number | null
events.openInterest number | null events.sortBy string | null events.category string | null
events.subcategory string | null events.isTemplate boolean | null events.templateVariables string | null
events.published_at string | null events.createdBy string | null events.updatedBy string | null
events.createdAt string | null
events.updatedAt
string` | null
events.commentsEnabled
boolean | null
events.competitive
number | null
events.volume24hr
number | null
events.volume1wk
number | null
events.volume1mo
number | null
events.volume1yr
number | null

events.featuredImage
string | null
events.disqusThread
string | null
events.parentEvent
string | null
events.enableOrderBook
boolean | null
events.liquidityAmm
number | null
events.liquidityClob
number | null
events.negRisk
boolean | null
events.negRiskMarketID
string | null
events.negRiskFeeBips
integer | null
events.commentCount
integer | null
events.imageOptimized
object
Hide child attributes
events.imageOptimized.id
string
events.imageOptimized.imageUrlSource
string | null
events.imageOptimized.imageUrlOptimized
string | null

events.imageOptimized.imageSizeKbSource
number | null
events.imageOptimized.imageSizeKbOptimized
number | null
events.imageOptimized.imageOptimizedComplete
boolean | null
events.imageOptimized.imageOptimizedLastUpdated
string | null
events.imageOptimized.relID
integer | null
events.imageOptimized.field
string | null
events.imageOptimized.relname
string | null
events.iconOptimized
object
Hide child attributes
events.iconOptimized.id
string
events.iconOptimized.imageUrlSource
string | null
events.iconOptimized.imageUrlOptimized
string | null
events.iconOptimized.imageSizeKbSource
number | null
events.iconOptimized.imageSizeKbOptimized
number | null
events.iconOptimized.imageOptimizedComplete
boolean | null

events.iconOptimized.imageOptimizedLastUpdated
string | null
events.iconOptimized.relID
integer | null
events.iconOptimized.field
string | null
events.iconOptimized.relname
string | null
events.featuredImageOptimized
object
Hide child attributes
events.featuredImageOptimized.id
string
events.featuredImageOptimized.imageUrlSource
string | null
events.featuredImageOptimized.imageUrlOptimized
string | null
events.featuredImageOptimized.imageSizeKbSource
number | null
events.featuredImageOptimized.imageSizeKbOptimized
number | null
events.featuredImageOptimized.imageOptimizedComplete
boolean | null
events.featuredImageOptimized.imageOptimizedLastUpdated
string | null
events.featuredImageOptimized.relID
integer | null
events.featuredImageOptimized.field
string | null

events.featuredImageOptimized.relname
string | null
events.subEvents
string[] | null
events.markets
array
events.series
object[]
Hide child attributes
events.series.id
string
events.series.ticker
string | null
events.series.slug
string | null
events.series.title
string | null
events.series.subtitle
string | null
events.series.seriesType
string | null
events.series.recurrence
string | null
events.series.description
string | null
events.series.image
string | null
events.series.icon
string | null

events.series.layout
string | null
events.series.active
boolean | null
events.series.closed
boolean | null
events.series.archived
boolean | null
events.series.new
boolean | null
events.series.featured
boolean | null
events.series.restricted
boolean | null
events.series.isTemplate
boolean | null
events.series.templateVariables
boolean | null
events.series.publishedAt
string | null
events.series.createdBy
string | null
events.series.updatedBy
string | null
events.series.createdAt
string <date-time> | null events.series.updatedAt string | null
events.series.commentsEnabled
boolean | null
events.series.competitive

string | null
events.series.volume24hr
number | null
events.series.volume
number | null
events.series.liquidity
number | null
events.series.startDate
string` | null
events.series.pythTokenID
string | null
events.series.cgAssetName
string | null
events.series.score
integer | null
events.series.events
array
events.series.collections
object[]
Hide child attributes
events.series.collections.id
string
events.series.collections.ticker
string | null
events.series.collections.slug
string | null
events.series.collections.title
string | null
events.series.collections.subtitle

string | null
events.series.collections.collectionType
string | null
events.series.collections.description
string | null
events.series.collections.tags
string | null
events.series.collections.image
string | null
events.series.collections.icon
string | null
events.series.collections.headerImage
string | null
events.series.collections.layout
string | null
events.series.collections.active
boolean | null
events.series.collections.closed
boolean | null
events.series.collections.archived
boolean | null
events.series.collections.new
boolean | null
events.series.collections.featured
boolean | null
events.series.collections.restricted
boolean | null
events.series.collections.isTemplate
boolean | null

events.series.collections.templateVariables
string | null
events.series.collections.publishedAt
string | null
events.series.collections.createdBy
string | null
events.series.collections.updatedBy
string | null
events.series.collections.createdAt
string <date-time> | null events.series.collections.updatedAt string | null
events.series.collections.commentsEnabled
boolean | null
events.series.collections.imageOptimized
object
Hide child attributes
events.series.collections.imageOptimized.id
string
events.series.collections.imageOptimized.imageUrlSource
string | null
events.series.collections.imageOptimized.imageUrlOptimized
string | null
events.series.collections.imageOptimized.imageSizeKbSource
number | null
events.series.collections.imageOptimized.imageSizeKbOptimized
number | null
events.series.collections.imageOptimized.imageOptimizedComplete
boolean | null
events.series.collections.imageOptimized.imageOptimizedLastUpdated
string | null

events.series.collections.imageOptimized.relID
integer | null
events.series.collections.imageOptimized.field
string | null
events.series.collections.imageOptimized.relname
string | null
events.series.collections.iconOptimized
object
Hide child attributes
events.series.collections.iconOptimized.id
string
events.series.collections.iconOptimized.imageUrlSource
string | null
events.series.collections.iconOptimized.imageUrlOptimized
string | null
events.series.collections.iconOptimized.imageSizeKbSource
number | null
events.series.collections.iconOptimized.imageSizeKbOptimized
number | null
events.series.collections.iconOptimized.imageOptimizedComplete
boolean | null
events.series.collections.iconOptimized.imageOptimizedLastUpdated
string | null
events.series.collections.iconOptimized.relID
integer | null
events.series.collections.iconOptimized.field
string | null
events.series.collections.iconOptimized.relname
string | null

events.series.collections.headerImageOptimized
object
Hide child attributes
events.series.collections.headerImageOptimized.id
string
events.series.collections.headerImageOptimized.imageUrlSource
string | null
events.series.collections.headerImageOptimized.imageUrlOptimized
string | null
events.series.collections.headerImageOptimized.imageSizeKbSource
number | null
events.series.collections.headerImageOptimized.imageSizeKbOptimized
number | null
events.series.collections.headerImageOptimized.imageOptimizedComplete
boolean | null
events.series.collections.headerImageOptimized.imageOptimizedLastUpdated
string | null
events.series.collections.headerImageOptimized.relID
integer | null
events.series.collections.headerImageOptimized.field
string | null
events.series.collections.headerImageOptimized.relname
string | null
events.series.categories
object[]
Hide child attributes
events.series.categories.id
string

events.series.categories.label
string | null
events.series.categories.parentCategory
string | null
events.series.categories.slug
string | null
events.series.categories.publishedAt
string | null
events.series.categories.createdBy
string | null
events.series.categories.updatedBy
string | null
events.series.categories.createdAt
string <date-time> | null events.series.categories.updatedAt string | null
events.series.tags
object[]
Hide child attributes
events.series.tags.id
string
events.series.tags.label
string | null
events.series.tags.slug
string | null
events.series.tags.forceShow
boolean | null
events.series.tags.publishedAt
string | null
events.series.tags.createdBy
integer | null

events.series.tags.updatedBy
integer | null
events.series.tags.createdAt
string <date-time> | null events.series.tags.updatedAt string | null
events.series.tags.forceHide
boolean | null
events.series.tags.isCarousel
boolean | null
events.series.commentCount
integer | null
events.series.chats
object[]
Hide child attributes
events.series.chats.id
string
events.series.chats.channelId
string | null
events.series.chats.channelName
string | null
events.series.chats.channelImage
string | null
events.series.chats.live
boolean | null
events.series.chats.startTime
string <date-time> | null events.series.chats.endTime string | null
events.categories
object[]
Hide child attributes

events.categories.id
string
events.categories.label
string | null
events.categories.parentCategory
string | null
events.categories.slug
string | null
events.categories.publishedAt
string | null
events.categories.createdBy
string | null
events.categories.updatedBy
string | null
events.categories.createdAt
string <date-time> | null events.categories.updatedAt string | null
events.collections
object[]
Hide child attributes
events.collections.id
string
events.collections.ticker
string | null
events.collections.slug
string | null
events.collections.title
string | null
events.collections.subtitle
string | null

events.collections.collectionType
string | null
events.collections.description
string | null
events.collections.tags
string | null
events.collections.image
string | null
events.collections.icon
string | null
events.collections.headerImage
string | null
events.collections.layout
string | null
events.collections.active
boolean | null
events.collections.closed
boolean | null
events.collections.archived
boolean | null
events.collections.new
boolean | null
events.collections.featured
boolean | null
events.collections.restricted
boolean | null
events.collections.isTemplate
boolean | null

events.collections.templateVariables
string | null
events.collections.publishedAt
string | null
events.collections.createdBy
string | null
events.collections.updatedBy
string | null
events.collections.createdAt
string <date-time> | null events.collections.updatedAt string | null
events.collections.commentsEnabled
boolean | null
events.collections.imageOptimized
object
Hide child attributes
events.collections.imageOptimized.id
string
events.collections.imageOptimized.imageUrlSource
string | null
events.collections.imageOptimized.imageUrlOptimized
string | null
events.collections.imageOptimized.imageSizeKbSource
number | null
events.collections.imageOptimized.imageSizeKbOptimized
number | null
events.collections.imageOptimized.imageOptimizedComplete
boolean | null
events.collections.imageOptimized.imageOptimizedLastUpdated
string | null

events.collections.imageOptimized.relID
integer | null
events.collections.imageOptimized.field
string | null
events.collections.imageOptimized.relname
string | null
events.collections.iconOptimized
object
Hide child attributes
events.collections.iconOptimized.id
string
events.collections.iconOptimized.imageUrlSource
string | null
events.collections.iconOptimized.imageUrlOptimized
string | null
events.collections.iconOptimized.imageSizeKbSource
number | null
events.collections.iconOptimized.imageSizeKbOptimized
number | null
events.collections.iconOptimized.imageOptimizedComplete
boolean | null
events.collections.iconOptimized.imageOptimizedLastUpdated
string | null
events.collections.iconOptimized.relID
integer | null
events.collections.iconOptimized.field
string | null
events.collections.iconOptimized.relname
string | null

events.collections.headerImageOptimized
object
Hide child attributes
events.collections.headerImageOptimized.id
string
events.collections.headerImageOptimized.imageUrlSource
string | null
events.collections.headerImageOptimized.imageUrlOptimized
string | null
events.collections.headerImageOptimized.imageSizeKbSource
number | null
events.collections.headerImageOptimized.imageSizeKbOptimized
number | null
events.collections.headerImageOptimized.imageOptimizedComplete
boolean | null
events.collections.headerImageOptimized.imageOptimizedLastUpdated
string | null
events.collections.headerImageOptimized.relID
integer | null
events.collections.headerImageOptimized.field
string | null
events.collections.headerImageOptimized.relname
string | null
events.tags
object[]
Hide child attributes
events.tags.id
string
events.tags.label

string | null
events.tags.slug
string | null
events.tags.forceShow
boolean | null
events.tags.publishedAt
string | null
events.tags.createdBy
integer | null
events.tags.updatedBy
integer | null
events.tags.createdAt
string <date-time> | null events.tags.updatedAt string | null
events.tags.forceHide
boolean | null
events.tags.isCarousel
boolean | null
events.cyom
boolean | null
events.closedTime
string <date-time> | null events.showAllOutcomes boolean | null events.showMarketImages boolean |
null events.automaticallyResolved boolean | null events.enableNegRisk boolean | null
events.automaticallyActive boolean | null events.eventDate string | null events.startTime string | null
events.eventWeek
integer | null
events.seriesSlug
string | null
events.score
string | null

events.elapsed
string | null
events.period
string | null
events.live
boolean | null
events.ended
boolean | null
events.finishedTimestamp
string` | null
events.gmpChartMode
string | null
events.eventCreators
object[]
Hide child attributes
events.eventCreators.id
string
events.eventCreators.creatorName
string | null
events.eventCreators.creatorHandle
string | null
events.eventCreators.creatorUrl
string | null
events.eventCreators.creatorImage
string | null
events.eventCreators.createdAt
string <date-time> | null events.eventCreators.updatedAt string | null
events.tweetCount
integer | null

events.chats
object[]
Hide child attributes
events.chats.id
string
events.chats.channelId
string | null
events.chats.channelName
string | null
events.chats.channelImage
string | null
events.chats.live
boolean | null
events.chats.startTime
string <date-time> | null events.chats.endTime string | null
events.featuredOrder
integer | null
events.estimateValue
boolean | null
events.cantEstimate
boolean | null
events.estimatedValue
string | null
events.templates
object[]
Hide child attributes
events.templates.id
string
events.templates.eventTitle

string | null
events.templates.eventSlug
string | null
events.templates.eventImage
string | null
events.templates.marketTitle
string | null
events.templates.description
string | null
events.templates.resolutionSource
string | null
events.templates.negRisk
boolean | null
events.templates.sortBy
string | null
events.templates.showMarketImages
boolean | null
events.templates.seriesSlug
string | null
events.templates.outcomes
string | null
events.spreadsMainLine
number | null
events.totalsMainLine
number | null
events.carouselMap
string | null
events.pendingDeployment
boolean | null

events.deploying
boolean | null
events.deployingTimestamp
string <date-time> | null events.scheduledDeploymentTimestamp string | null
events.gameStatus
string | null
categories
object[]
Hide child attributes
categories.id
string
categories.label
string | null
categories.parentCategory
string | null
categories.slug
string | null
categories.publishedAt
string | null
categories.createdBy
string | null
categories.updatedBy
string | null
categories.createdAt
string <date-time> | null categories.updatedAt string | null
tags
object[]
Hide child attributes

tags.id
string
tags.label
string | null
tags.slug
string | null
tags.forceShow
boolean | null
tags.publishedAt
string | null
tags.createdBy
integer | null
tags.updatedBy
integer | null
tags.createdAt
string <date-time> | null tags.updatedAt string | null
tags.forceHide
boolean | null
tags.isCarousel
boolean | null
creator
string | null
ready
boolean | null
funded
boolean | null
pastSlugs
string | null

readyTimestamp
string <date-time> | null fundedTimestamp string | null
acceptingOrdersTimestamp
string <date-time> | null competitive number | null rewardsMinSize number | null rewardsMaxSpread
number | null spread number | null automaticallyResolved boolean | null oneDayPriceChange number |
null oneHourPriceChange number | null oneWeekPriceChange number | null oneMonthPriceChange
number | null oneYearPriceChange number | null lastTradePrice number | null bestBid number | null
bestAsk number | null automaticallyActive boolean | null clearBookOnStart boolean | null chartColor
string | null seriesColor string | null showGmpSeries boolean | null showGmpOutcome boolean | null
manualActivation boolean | null negRiskOther boolean | null gameId string | null groupItemRange string
| null sportsMarketType string | null line number | null umaResolutionStatuses string | null
pendingDeployment boolean | null deploying boolean | null deployingTimestamp string | null
scheduledDeploymentTimestamp
string <date-time> | null rfqEnabled boolean | null eventStartTime string | null
Get market by id
GET/markets/{id}
Get market by id
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/markets/{id}
Python
import requests
url = "https://gamma-api.polymarket.com/markets/{id}"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/markets/{id}', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));

PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/markets/{id}",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/markets/{id}"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}

Java
HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/markets/{id}")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/markets/{id}")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
{
"id": "<string>",
"question": "<string>",
"conditionId": "<string>",
"slug": "<string>",
"twitterCardImage": "<string>",
"resolutionSource": "<string>",
"endDate": "2023-11-07T05:31:56Z",
"category": "<string>",
"ammType": "<string>",
"liquidity": "<string>",
"sponsorName": "<string>",
"sponsorImage": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"xAxisValue": "<string>",
"yAxisValue": "<string>",
"denominationToken": "<string>",
"fee": "<string>",
"image": "<string>",
"icon": "<string>",
"lowerBound": "<string>",
"upperBound": "<string>",
"description": "<string>",
"outcomes": "<string>",
"outcomePrices": "<string>",
"volume": "<string>",
"active": true,

"marketType": "<string>",
"formatType": "<string>",
"lowerBoundDate": "<string>",
"upperBoundDate": "<string>",
"closed": true,
"marketMakerAddress": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"closedTime": "<string>",
"wideFormat": true,
"new": true,
"mailchimpTag": "<string>",
"featured": true,
"archived": true,
"resolvedBy": "<string>",
"restricted": true,
"marketGroup": 123,
"groupItemTitle": "<string>",
"groupItemThreshold": "<string>",
"questionID": "<string>",
"umaEndDate": "<string>",
"enableOrderBook": true,
"orderPriceMinTickSize": 123,
"orderMinSize": 123,
"umaResolutionStatus": "<string>",
"curationOrder": 123,
"volumeNum": 123,
"liquidityNum": 123,
"endDateIso": "<string>",
"startDateIso": "<string>",
"umaEndDateIso": "<string>",
"hasReviewedDates": true,
"readyForCron": true,
"commentsEnabled": true,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,
"gameStartTime": "<string>",
"secondsDelay": 123,
"clobTokenIds": "<string>",
"disqusThread": "<string>",
"shortOutcomes": "<string>",
"teamAID": "<string>",
"teamBID": "<string>",
"umaBond": "<string>",
"umaReward": "<string>",
"fpmmLive": true,
"volume24hrAmm": 123,
"volume1wkAmm": 123,

"volume1moAmm": 123,
"volume1yrAmm": 123,
"volume24hrClob": 123,
"volume1wkClob": 123,
"volume1moClob": 123,
"volume1yrClob": 123,
"volumeAmm": 123,
"volumeClob": 123,
"liquidityAmm": 123,
"liquidityClob": 123,
"makerBaseFee": 123,
"takerBaseFee": 123,
"customLiveness": 123,
"acceptingOrders": true,
"notificationsEnabled": true,
"score": 123,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"events": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"creationDate": "2023-11-07T05:31:56Z",
"endDate": "2023-11-07T05:31:56Z",

"image": "<string>",
"icon": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"liquidity": 123,
"volume": 123,
"openInterest": 123,
"sortBy": "<string>",
"category": "<string>",
"subcategory": "<string>",
"isTemplate": true,
"templateVariables": "<string>",
"published_at": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"competitive": 123,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,
"featuredImage": "<string>",
"disqusThread": "<string>",
"parentEvent": "<string>",
"enableOrderBook": true,
"liquidityAmm": 123,
"liquidityClob": 123,
"negRisk": true,
"negRiskMarketID": "<string>",
"negRiskFeeBips": 123,
"commentCount": 123,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",

"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"featuredImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"subEvents": [
"<string>"
],
"markets": "<array>",
"series": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"seriesType": "<string>",
"recurrence": "<string>",
"description": "<string>",
"image": "<string>",
"icon": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": true,
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,

"competitive": "<string>",
"volume24hr": 123,
"volume": 123,
"liquidity": 123,
"startDate": "2023-11-07T05:31:56Z",
"pythTokenID": "<string>",
"cgAssetName": "<string>",
"score": 123,
"events": "<array>",
"collections": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",
"image": "<string>",
"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",

"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
}
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"commentCount": 123,

"chats": [
{
"id": "<string>",
"channelId": "<string>",
"channelName": "<string>",
"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",
"endTime": "2023-11-07T05:31:56Z"
}
]
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"collections": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",
"image": "<string>",
"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",

"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
}
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,

"isCarousel": true
}
],
"cyom": true,
"closedTime": "2023-11-07T05:31:56Z",
"showAllOutcomes": true,
"showMarketImages": true,
"automaticallyResolved": true,
"enableNegRisk": true,
"automaticallyActive": true,
"eventDate": "<string>",
"startTime": "2023-11-07T05:31:56Z",
"eventWeek": 123,
"seriesSlug": "<string>",
"score": "<string>",
"elapsed": "<string>",
"period": "<string>",
"live": true,
"ended": true,
"finishedTimestamp": "2023-11-07T05:31:56Z",
"gmpChartMode": "<string>",
"eventCreators": [
{
"id": "<string>",
"creatorName": "<string>",
"creatorHandle": "<string>",
"creatorUrl": "<string>",
"creatorImage": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tweetCount": 123,
"chats": [
{
"id": "<string>",
"channelId": "<string>",
"channelName": "<string>",
"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",
"endTime": "2023-11-07T05:31:56Z"
}
],
"featuredOrder": 123,
"estimateValue": true,
"cantEstimate": true,
"estimatedValue": "<string>",
"templates": [
{
"id": "<string>",
"eventTitle": "<string>",

"eventSlug": "<string>",
"eventImage": "<string>",
"marketTitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",
"negRisk": true,
"sortBy": "<string>",
"showMarketImages": true,
"seriesSlug": "<string>",
"outcomes": "<string>"
}
],
"spreadsMainLine": 123,
"totalsMainLine": 123,
"carouselMap": "<string>",
"pendingDeployment": true,
"deploying": true,
"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",
"gameStatus": "<string>"
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"creator": "<string>",
"ready": true,

"funded": true,
"pastSlugs": "<string>",
"readyTimestamp": "2023-11-07T05:31:56Z",
"fundedTimestamp": "2023-11-07T05:31:56Z",
"acceptingOrdersTimestamp": "2023-11-07T05:31:56Z",
"competitive": 123,
"rewardsMinSize": 123,
"rewardsMaxSpread": 123,
"spread": 123,
"automaticallyResolved": true,
"oneDayPriceChange": 123,
"oneHourPriceChange": 123,
"oneWeekPriceChange": 123,
"oneMonthPriceChange": 123,
"oneYearPriceChange": 123,
"lastTradePrice": 123,
"bestBid": 123,
"bestAsk": 123,
"automaticallyActive": true,
"clearBookOnStart": true,
"chartColor": "<string>",
"seriesColor": "<string>",
"showGmpSeries": true,
"showGmpOutcome": true,
"manualActivation": true,
"negRiskOther": true,
"gameId": "<string>",
"groupItemRange": "<string>",
"sportsMarketType": "<string>",
"line": 123,
"umaResolutionStatuses": "<string>",
"pendingDeployment": true,
"deploying": true,
"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",
"rfqEnabled": true,
"eventStartTime": "2023-11-07T05:31:56Z"
}
Path Parameters
slug
string
required
Query Parameters
include_tag
boolean

Response
200 - application/json
Market
id
string
question
string | null
conditionId
string
slug
string | null
twitterCardImage
string | null
resolutionSource
string | null
endDate
string <date-time> | null category string | null ammType string | null liquidity string | null sponsorName
string | null sponsorImage string | null startDate string | null
xAxisValue
string | null
yAxisValue
string | null
denominationToken
string | null
fee
string | null
image
string | null
icon

string | null
lowerBound
string | null
upperBound
string | null
description
string | null
outcomes
string | null
outcomePrices
string | null
volume
string | null
active
boolean | null
marketType
string | null
formatType
string | null
lowerBoundDate
string | null
upperBoundDate
string | null
closed
boolean | null
marketMakerAddress
string
createdBy
integer | null

updatedBy
integer | null
createdAt
string <date-time> | null updatedAt string | null
closedTime
string | null
wideFormat
boolean | null
new
boolean | null
mailchimpTag
string | null
featured
boolean | null
archived
boolean | null
resolvedBy
string | null
restricted
boolean | null
marketGroup
integer | null
groupItemTitle
string | null
groupItemThreshold
string | null
questionID
string | null

umaEndDate
string | null
enableOrderBook
boolean | null
orderPriceMinTickSize
number | null
orderMinSize
number | null
umaResolutionStatus
string | null
curationOrder
integer | null
volumeNum
number | null
liquidityNum
number | null
endDateIso
string | null
startDateIso
string | null
umaEndDateIso
string | null
hasReviewedDates
boolean | null
readyForCron
boolean | null
commentsEnabled
boolean | null
volume24hr

number | null
volume1wk
number | null
volume1mo
number | null
volume1yr
number | null
gameStartTime
string | null
secondsDelay
integer | null
clobTokenIds
string | null
disqusThread
string | null
shortOutcomes
string | null
teamAID
string | null
teamBID
string | null
umaBond
string | null
umaReward
string | null
fpmmLive
boolean | null
volume24hrAmm
number | null

volume1wkAmm
number | null
volume1moAmm
number | null
volume1yrAmm
number | null
volume24hrClob
number | null
volume1wkClob
number | null
volume1moClob
number | null
volume1yrClob
number | null
volumeAmm
number | null
volumeClob
number | null
liquidityAmm
number | null
liquidityClob
number | null
makerBaseFee
integer | null
takerBaseFee
integer | null
customLiveness
integer | null

acceptingOrders
boolean | null
notificationsEnabled
boolean | null
score
integer | null
imageOptimized
object
Hide child attributes
imageOptimized.id
string
imageOptimized.imageUrlSource
string | null
imageOptimized.imageUrlOptimized
string | null
imageOptimized.imageSizeKbSource
number | null
imageOptimized.imageSizeKbOptimized
number | null
imageOptimized.imageOptimizedComplete
boolean | null
imageOptimized.imageOptimizedLastUpdated
string | null
imageOptimized.relID
integer | null
imageOptimized.field
string | null
imageOptimized.relname
string | null

iconOptimized
object
Hide child attributes
iconOptimized.id
string
iconOptimized.imageUrlSource
string | null
iconOptimized.imageUrlOptimized
string | null
iconOptimized.imageSizeKbSource
number | null
iconOptimized.imageSizeKbOptimized
number | null
iconOptimized.imageOptimizedComplete
boolean | null
iconOptimized.imageOptimizedLastUpdated
string | null
iconOptimized.relID
integer | null
iconOptimized.field
string | null
iconOptimized.relname
string | null
events
object[]
Hide child attributes
events.id
string
events.ticker

string | null
events.slug
string | null
events.title
string | null
events.subtitle
string | null
events.description
string | null
events.resolutionSource
string | null
events.startDate
string <date-time> | null events.creationDate string | null
events.endDate
string <date-time> | null events.image string | null events.icon string | null events.active boolean | null
events.closed boolean | null events.archived boolean | null events.new boolean | null events.featured
boolean | null events.restricted boolean | null events.liquidity number | null events.volume number | null
events.openInterest number | null events.sortBy string | null events.category string | null
events.subcategory string | null events.isTemplate boolean | null events.templateVariables string | null
events.published_at string | null events.createdBy string | null events.updatedBy string | null
events.createdAt string | null
events.updatedAt
string` | null
events.commentsEnabled
boolean | null
events.competitive
number | null
events.volume24hr
number | null
events.volume1wk
number | null

events.volume1mo
number | null
events.volume1yr
number | null
events.featuredImage
string | null
events.disqusThread
string | null
events.parentEvent
string | null
events.enableOrderBook
boolean | null
events.liquidityAmm
number | null
events.liquidityClob
number | null
events.negRisk
boolean | null
events.negRiskMarketID
string | null
events.negRiskFeeBips
integer | null
events.commentCount
integer | null
events.imageOptimized
object
Hide child attributes
events.imageOptimized.id
string

events.imageOptimized.imageUrlSource
string | null
events.imageOptimized.imageUrlOptimized
string | null
events.imageOptimized.imageSizeKbSource
number | null
events.imageOptimized.imageSizeKbOptimized
number | null
events.imageOptimized.imageOptimizedComplete
boolean | null
events.imageOptimized.imageOptimizedLastUpdated
string | null
events.imageOptimized.relID
integer | null
events.imageOptimized.field
string | null
events.imageOptimized.relname
string | null
events.iconOptimized
object
Hide child attributes
events.iconOptimized.id
string
events.iconOptimized.imageUrlSource
string | null
events.iconOptimized.imageUrlOptimized
string | null
events.iconOptimized.imageSizeKbSource
number | null

events.iconOptimized.imageSizeKbOptimized
number | null
events.iconOptimized.imageOptimizedComplete
boolean | null
events.iconOptimized.imageOptimizedLastUpdated
string | null
events.iconOptimized.relID
integer | null
events.iconOptimized.field
string | null
events.iconOptimized.relname
string | null
events.featuredImageOptimized
object
Hide child attributes
events.featuredImageOptimized.id
string
events.featuredImageOptimized.imageUrlSource
string | null
events.featuredImageOptimized.imageUrlOptimized
string | null
events.featuredImageOptimized.imageSizeKbSource
number | null
events.featuredImageOptimized.imageSizeKbOptimized
number | null
events.featuredImageOptimized.imageOptimizedComplete
boolean | null
events.featuredImageOptimized.imageOptimizedLastUpdated
string | null

events.featuredImageOptimized.relID
integer | null
events.featuredImageOptimized.field
string | null
events.featuredImageOptimized.relname
string | null
events.subEvents
string[] | null
events.markets
array
events.series
object[]
Hide child attributes
events.series.id
string
events.series.ticker
string | null
events.series.slug
string | null
events.series.title
string | null
events.series.subtitle
string | null
events.series.seriesType
string | null
events.series.recurrence
string | null
events.series.description
string | null

events.series.image
string | null
events.series.icon
string | null
events.series.layout
string | null
events.series.active
boolean | null
events.series.closed
boolean | null
events.series.archived
boolean | null
events.series.new
boolean | null
events.series.featured
boolean | null
events.series.restricted
boolean | null
events.series.isTemplate
boolean | null
events.series.templateVariables
boolean | null
events.series.publishedAt
string | null
events.series.createdBy
string | null
events.series.updatedBy
string | null
events.series.createdAt

string <date-time> | null events.series.updatedAt string | null
events.series.commentsEnabled
boolean | null
events.series.competitive
string | null
events.series.volume24hr
number | null
events.series.volume
number | null
events.series.liquidity
number | null
events.series.startDate
string` | null
events.series.pythTokenID
string | null
events.series.cgAssetName
string | null
events.series.score
integer | null
events.series.events
array
events.series.collections
object[]
Hide child attributes
events.series.collections.id
string
events.series.collections.ticker
string | null
events.series.collections.slug

string | null
events.series.collections.title
string | null
events.series.collections.subtitle
string | null
events.series.collections.collectionType
string | null
events.series.collections.description
string | null
events.series.collections.tags
string | null
events.series.collections.image
string | null
events.series.collections.icon
string | null
events.series.collections.headerImage
string | null
events.series.collections.layout
string | null
events.series.collections.active
boolean | null
events.series.collections.closed
boolean | null
events.series.collections.archived
boolean | null
events.series.collections.new
boolean | null
events.series.collections.featured
boolean | null

events.series.collections.restricted
boolean | null
events.series.collections.isTemplate
boolean | null
events.series.collections.templateVariables
string | null
events.series.collections.publishedAt
string | null
events.series.collections.createdBy
string | null
events.series.collections.updatedBy
string | null
events.series.collections.createdAt
string <date-time> | null events.series.collections.updatedAt string | null
events.series.collections.commentsEnabled
boolean | null
events.series.collections.imageOptimized
object
Hide child attributes
events.series.collections.imageOptimized.id
string
events.series.collections.imageOptimized.imageUrlSource
string | null
events.series.collections.imageOptimized.imageUrlOptimized
string | null
events.series.collections.imageOptimized.imageSizeKbSource
number | null
events.series.collections.imageOptimized.imageSizeKbOptimized
number | null

events.series.collections.imageOptimized.imageOptimizedComplete
boolean | null
events.series.collections.imageOptimized.imageOptimizedLastUpdated
string | null
events.series.collections.imageOptimized.relID
integer | null
events.series.collections.imageOptimized.field
string | null
events.series.collections.imageOptimized.relname
string | null
events.series.collections.iconOptimized
object
Hide child attributes
events.series.collections.iconOptimized.id
string
events.series.collections.iconOptimized.imageUrlSource
string | null
events.series.collections.iconOptimized.imageUrlOptimized
string | null
events.series.collections.iconOptimized.imageSizeKbSource
number | null
events.series.collections.iconOptimized.imageSizeKbOptimized
number | null
events.series.collections.iconOptimized.imageOptimizedComplete
boolean | null
events.series.collections.iconOptimized.imageOptimizedLastUpdated
string | null
events.series.collections.iconOptimized.relID
integer | null

events.series.collections.iconOptimized.field
string | null
events.series.collections.iconOptimized.relname
string | null
events.series.collections.headerImageOptimized
object
Hide child attributes
events.series.collections.headerImageOptimized.id
string
events.series.collections.headerImageOptimized.imageUrlSource
string | null
events.series.collections.headerImageOptimized.imageUrlOptimized
string | null
events.series.collections.headerImageOptimized.imageSizeKbSource
number | null
events.series.collections.headerImageOptimized.imageSizeKbOptimized
number | null
events.series.collections.headerImageOptimized.imageOptimizedComplete
boolean | null
events.series.collections.headerImageOptimized.imageOptimizedLastUpdated
string | null
events.series.collections.headerImageOptimized.relID
integer | null
events.series.collections.headerImageOptimized.field
string | null
events.series.collections.headerImageOptimized.relname
string | null
events.series.categories

object[]
Hide child attributes
events.series.categories.id
string
events.series.categories.label
string | null
events.series.categories.parentCategory
string | null
events.series.categories.slug
string | null
events.series.categories.publishedAt
string | null
events.series.categories.createdBy
string | null
events.series.categories.updatedBy
string | null
events.series.categories.createdAt
string <date-time> | null events.series.categories.updatedAt string | null
events.series.tags
object[]
Hide child attributes
events.series.tags.id
string
events.series.tags.label
string | null
events.series.tags.slug
string | null
events.series.tags.forceShow
boolean | null

events.series.tags.publishedAt
string | null
events.series.tags.createdBy
integer | null
events.series.tags.updatedBy
integer | null
events.series.tags.createdAt
string <date-time> | null events.series.tags.updatedAt string | null
events.series.tags.forceHide
boolean | null
events.series.tags.isCarousel
boolean | null
events.series.commentCount
integer | null
events.series.chats
object[]
Hide child attributes
events.series.chats.id
string
events.series.chats.channelId
string | null
events.series.chats.channelName
string | null
events.series.chats.channelImage
string | null
events.series.chats.live
boolean | null
events.series.chats.startTime
string <date-time> | null events.series.chats.endTime string | null

events.categories
object[]
Hide child attributes
events.categories.id
string
events.categories.label
string | null
events.categories.parentCategory
string | null
events.categories.slug
string | null
events.categories.publishedAt
string | null
events.categories.createdBy
string | null
events.categories.updatedBy
string | null
events.categories.createdAt
string <date-time> | null events.categories.updatedAt string | null
events.collections
object[]
Hide child attributes
events.collections.id
string
events.collections.ticker
string | null
events.collections.slug
string | null

events.collections.title
string | null
events.collections.subtitle
string | null
events.collections.collectionType
string | null
events.collections.description
string | null
events.collections.tags
string | null
events.collections.image
string | null
events.collections.icon
string | null
events.collections.headerImage
string | null
events.collections.layout
string | null
events.collections.active
boolean | null
events.collections.closed
boolean | null
events.collections.archived
boolean | null
events.collections.new
boolean | null
events.collections.featured
boolean | null
events.collections.restricted

boolean | null
events.collections.isTemplate
boolean | null
events.collections.templateVariables
string | null
events.collections.publishedAt
string | null
events.collections.createdBy
string | null
events.collections.updatedBy
string | null
events.collections.createdAt
string <date-time> | null events.collections.updatedAt string | null
events.collections.commentsEnabled
boolean | null
events.collections.imageOptimized
object
Hide child attributes
events.collections.imageOptimized.id
string
events.collections.imageOptimized.imageUrlSource
string | null
events.collections.imageOptimized.imageUrlOptimized
string | null
events.collections.imageOptimized.imageSizeKbSource
number | null
events.collections.imageOptimized.imageSizeKbOptimized
number | null
events.collections.imageOptimized.imageOptimizedComplete

boolean | null
events.collections.imageOptimized.imageOptimizedLastUpdated
string | null
events.collections.imageOptimized.relID
integer | null
events.collections.imageOptimized.field
string | null
events.collections.imageOptimized.relname
string | null
events.collections.iconOptimized
object
Hide child attributes
events.collections.iconOptimized.id
string
events.collections.iconOptimized.imageUrlSource
string | null
events.collections.iconOptimized.imageUrlOptimized
string | null
events.collections.iconOptimized.imageSizeKbSource
number | null
events.collections.iconOptimized.imageSizeKbOptimized
number | null
events.collections.iconOptimized.imageOptimizedComplete
boolean | null
events.collections.iconOptimized.imageOptimizedLastUpdated
string | null
events.collections.iconOptimized.relID
integer | null
events.collections.iconOptimized.field

string | null
events.collections.iconOptimized.relname
string | null
events.collections.headerImageOptimized
object
Hide child attributes
events.collections.headerImageOptimized.id
string
events.collections.headerImageOptimized.imageUrlSource
string | null
events.collections.headerImageOptimized.imageUrlOptimized
string | null
events.collections.headerImageOptimized.imageSizeKbSource
number | null
events.collections.headerImageOptimized.imageSizeKbOptimized
number | null
events.collections.headerImageOptimized.imageOptimizedComplete
boolean | null
events.collections.headerImageOptimized.imageOptimizedLastUpdated
string | null
events.collections.headerImageOptimized.relID
integer | null
events.collections.headerImageOptimized.field
string | null
events.collections.headerImageOptimized.relname
string | null
events.tags
object[]
Hide child attributes

events.tags.id
string
events.tags.label
string | null
events.tags.slug
string | null
events.tags.forceShow
boolean | null
events.tags.publishedAt
string | null
events.tags.createdBy
integer | null
events.tags.updatedBy
integer | null
events.tags.createdAt
string <date-time> | null events.tags.updatedAt string | null
events.tags.forceHide
boolean | null
events.tags.isCarousel
boolean | null
events.cyom
boolean | null
events.closedTime
string <date-time> | null events.showAllOutcomes boolean | null events.showMarketImages boolean |
null events.automaticallyResolved boolean | null events.enableNegRisk boolean | null
events.automaticallyActive boolean | null events.eventDate string | null events.startTime string | null
events.eventWeek
integer | null
events.seriesSlug

string | null
events.score
string | null
events.elapsed
string | null
events.period
string | null
events.live
boolean | null
events.ended
boolean | null
events.finishedTimestamp
string` | null
events.gmpChartMode
string | null
events.eventCreators
object[]
Hide child attributes
events.eventCreators.id
string
events.eventCreators.creatorName
string | null
events.eventCreators.creatorHandle
string | null
events.eventCreators.creatorUrl
string | null
events.eventCreators.creatorImage
string | null
events.eventCreators.createdAt

string <date-time> | null events.eventCreators.updatedAt string | null
events.tweetCount
integer | null
events.chats
object[]
Hide child attributes
events.chats.id
string
events.chats.channelId
string | null
events.chats.channelName
string | null
events.chats.channelImage
string | null
events.chats.live
boolean | null
events.chats.startTime
string <date-time> | null events.chats.endTime string | null
events.featuredOrder
integer | null
events.estimateValue
boolean | null
events.cantEstimate
boolean | null
events.estimatedValue
string | null
events.templates
object[]
Hide child attributes

events.templates.id
string
events.templates.eventTitle
string | null
events.templates.eventSlug
string | null
events.templates.eventImage
string | null
events.templates.marketTitle
string | null
events.templates.description
string | null
events.templates.resolutionSource
string | null
events.templates.negRisk
boolean | null
events.templates.sortBy
string | null
events.templates.showMarketImages
boolean | null
events.templates.seriesSlug
string | null
events.templates.outcomes
string | null
events.spreadsMainLine
number | null
events.totalsMainLine
number | null

events.carouselMap
string | null
events.pendingDeployment
boolean | null
events.deploying
boolean | null
events.deployingTimestamp
string <date-time> | null events.scheduledDeploymentTimestamp string | null
events.gameStatus
string | null
categories
object[]
Hide child attributes
categories.id
string
categories.label
string | null
categories.parentCategory
string | null
categories.slug
string | null
categories.publishedAt
string | null
categories.createdBy
string | null
categories.updatedBy
string | null
categories.createdAt
string <date-time> | null categories.updatedAt string | null

tags
object[]
Hide child attributes
tags.id
string
tags.label
string | null
tags.slug
string | null
tags.forceShow
boolean | null
tags.publishedAt
string | null
tags.createdBy
integer | null
tags.updatedBy
integer | null
tags.createdAt
string <date-time> | null tags.updatedAt string | null
tags.forceHide
boolean | null
tags.isCarousel
boolean | null
creator
string | null
ready
boolean | null
funded
boolean | null

pastSlugs
string | null
readyTimestamp
string <date-time> | null fundedTimestamp string | null
acceptingOrdersTimestamp
string <date-time> | null competitive number | null rewardsMinSize number | null rewardsMaxSpread
number | null spread number | null automaticallyResolved boolean | null oneDayPriceChange number |
null oneHourPriceChange number | null oneWeekPriceChange number | null oneMonthPriceChange
number | null oneYearPriceChange number | null lastTradePrice number | null bestBid number | null
bestAsk number | null automaticallyActive boolean | null clearBookOnStart boolean | null chartColor
string | null seriesColor string | null showGmpSeries boolean | null showGmpOutcome boolean | null
manualActivation boolean | null negRiskOther boolean | null gameId string | null groupItemRange string
| null sportsMarketType string | null line number | null umaResolutionStatuses string | null
pendingDeployment boolean | null deploying boolean | null deployingTimestamp string | null
scheduledDeploymentTimestamp
string <date-time> | null rfqEnabled boolean | null eventStartTime string | null
Response
404
Not found
Get market tags by id
GET/markets/{id}/tags
Get market tags by id
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/markets/{id}/tags
Python
import requests
url = "https://gamma-api.polymarket.com/markets/{id}/tags"
response = requests.get(url)

print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/markets/{id}/tags', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/markets/{id}/tags",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {

url := "https://gamma-api.polymarket.com/markets/{id}/tags"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/markets/{id}/tags")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/markets/{id}/tags")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true

}
]
Path Parameters
id
integer
required
Response
200
application/json
Tags attached to the market
id
string
label
string | null
slug
string | null
forceShow
boolean | null
publishedAt
string | null
createdBy
integer | null
updatedBy
integer | null
createdAt
string <date-time> | null updatedAt string | null
forceHide
boolean | null

isCarousel
boolean | null
Response
404
Not found
Get market by slug
GET/markets/slug/{slug}
Get market by slug
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/markets/slug/{slug}
Python
import requests
url = "https://gamma-api.polymarket.com/markets/slug/{slug}"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/markets/slug/{slug}', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();

```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/markets/slug/{slug}",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/markets/slug/{slug}"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/markets/slug/{slug}")

.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/markets/slug/{slug}")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
{
"id": "<string>",
"question": "<string>",
"conditionId": "<string>",
"slug": "<string>",
"twitterCardImage": "<string>",
"resolutionSource": "<string>",
"endDate": "2023-11-07T05:31:56Z",
"category": "<string>",
"ammType": "<string>",
"liquidity": "<string>",
"sponsorName": "<string>",
"sponsorImage": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"xAxisValue": "<string>",
"yAxisValue": "<string>",
"denominationToken": "<string>",
"fee": "<string>",
"image": "<string>",
"icon": "<string>",
"lowerBound": "<string>",
"upperBound": "<string>",
"description": "<string>",
"outcomes": "<string>",
"outcomePrices": "<string>",
"volume": "<string>",
"active": true,
"marketType": "<string>",
"formatType": "<string>",
"lowerBoundDate": "<string>",
"upperBoundDate": "<string>",
"closed": true,

"marketMakerAddress": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"closedTime": "<string>",
"wideFormat": true,
"new": true,
"mailchimpTag": "<string>",
"featured": true,
"archived": true,
"resolvedBy": "<string>",
"restricted": true,
"marketGroup": 123,
"groupItemTitle": "<string>",
"groupItemThreshold": "<string>",
"questionID": "<string>",
"umaEndDate": "<string>",
"enableOrderBook": true,
"orderPriceMinTickSize": 123,
"orderMinSize": 123,
"umaResolutionStatus": "<string>",
"curationOrder": 123,
"volumeNum": 123,
"liquidityNum": 123,
"endDateIso": "<string>",
"startDateIso": "<string>",
"umaEndDateIso": "<string>",
"hasReviewedDates": true,
"readyForCron": true,
"commentsEnabled": true,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,
"gameStartTime": "<string>",
"secondsDelay": 123,
"clobTokenIds": "<string>",
"disqusThread": "<string>",
"shortOutcomes": "<string>",
"teamAID": "<string>",
"teamBID": "<string>",
"umaBond": "<string>",
"umaReward": "<string>",
"fpmmLive": true,
"volume24hrAmm": 123,
"volume1wkAmm": 123,
"volume1moAmm": 123,
"volume1yrAmm": 123,
"volume24hrClob": 123,
"volume1wkClob": 123,
"volume1moClob": 123,

"volume1yrClob": 123,
"volumeAmm": 123,
"volumeClob": 123,
"liquidityAmm": 123,
"liquidityClob": 123,
"makerBaseFee": 123,
"takerBaseFee": 123,
"customLiveness": 123,
"acceptingOrders": true,
"notificationsEnabled": true,
"score": 123,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"events": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"creationDate": "2023-11-07T05:31:56Z",
"endDate": "2023-11-07T05:31:56Z",
"image": "<string>",
"icon": "<string>",
"active": true,
"closed": true,
"archived": true,

"new": true,
"featured": true,
"restricted": true,
"liquidity": 123,
"volume": 123,
"openInterest": 123,
"sortBy": "<string>",
"category": "<string>",
"subcategory": "<string>",
"isTemplate": true,
"templateVariables": "<string>",
"published_at": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"competitive": 123,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,
"featuredImage": "<string>",
"disqusThread": "<string>",
"parentEvent": "<string>",
"enableOrderBook": true,
"liquidityAmm": 123,
"liquidityClob": 123,
"negRisk": true,
"negRiskMarketID": "<string>",
"negRiskFeeBips": 123,
"commentCount": 123,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",

"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"featuredImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"subEvents": [
"<string>"
],
"markets": "<array>",
"series": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"seriesType": "<string>",
"recurrence": "<string>",
"description": "<string>",
"image": "<string>",
"icon": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": true,
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"competitive": "<string>",
"volume24hr": 123,
"volume": 123,
"liquidity": 123,
"startDate": "2023-11-07T05:31:56Z",

"pythTokenID": "<string>",
"cgAssetName": "<string>",
"score": 123,
"events": "<array>",
"collections": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",
"image": "<string>",
"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",

"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
}
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"commentCount": 123,
"chats": [
{
"id": "<string>",
"channelId": "<string>",
"channelName": "<string>",

"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",
"endTime": "2023-11-07T05:31:56Z"
}
]
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"collections": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",
"image": "<string>",
"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",

"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
}
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"cyom": true,
"closedTime": "2023-11-07T05:31:56Z",

"showAllOutcomes": true,
"showMarketImages": true,
"automaticallyResolved": true,
"enableNegRisk": true,
"automaticallyActive": true,
"eventDate": "<string>",
"startTime": "2023-11-07T05:31:56Z",
"eventWeek": 123,
"seriesSlug": "<string>",
"score": "<string>",
"elapsed": "<string>",
"period": "<string>",
"live": true,
"ended": true,
"finishedTimestamp": "2023-11-07T05:31:56Z",
"gmpChartMode": "<string>",
"eventCreators": [
{
"id": "<string>",
"creatorName": "<string>",
"creatorHandle": "<string>",
"creatorUrl": "<string>",
"creatorImage": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tweetCount": 123,
"chats": [
{
"id": "<string>",
"channelId": "<string>",
"channelName": "<string>",
"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",
"endTime": "2023-11-07T05:31:56Z"
}
],
"featuredOrder": 123,
"estimateValue": true,
"cantEstimate": true,
"estimatedValue": "<string>",
"templates": [
{
"id": "<string>",
"eventTitle": "<string>",
"eventSlug": "<string>",
"eventImage": "<string>",
"marketTitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",

"negRisk": true,
"sortBy": "<string>",
"showMarketImages": true,
"seriesSlug": "<string>",
"outcomes": "<string>"
}
],
"spreadsMainLine": 123,
"totalsMainLine": 123,
"carouselMap": "<string>",
"pendingDeployment": true,
"deploying": true,
"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",
"gameStatus": "<string>"
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"creator": "<string>",
"ready": true,
"funded": true,
"pastSlugs": "<string>",
"readyTimestamp": "2023-11-07T05:31:56Z",
"fundedTimestamp": "2023-11-07T05:31:56Z",
"acceptingOrdersTimestamp": "2023-11-07T05:31:56Z",

"competitive": 123,
"rewardsMinSize": 123,
"rewardsMaxSpread": 123,
"spread": 123,
"automaticallyResolved": true,
"oneDayPriceChange": 123,
"oneHourPriceChange": 123,
"oneWeekPriceChange": 123,
"oneMonthPriceChange": 123,
"oneYearPriceChange": 123,
"lastTradePrice": 123,
"bestBid": 123,
"bestAsk": 123,
"automaticallyActive": true,
"clearBookOnStart": true,
"chartColor": "<string>",
"seriesColor": "<string>",
"showGmpSeries": true,
"showGmpOutcome": true,
"manualActivation": true,
"negRiskOther": true,
"gameId": "<string>",
"groupItemRange": "<string>",
"sportsMarketType": "<string>",
"line": 123,
"umaResolutionStatuses": "<string>",
"pendingDeployment": true,
"deploying": true,
"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",
"rfqEnabled": true,
"eventStartTime": "2023-11-07T05:31:56Z"
}
Response
200 - application/json
Market
id
string
question
string | null
conditionId
string

slug
string | null
twitterCardImage
string | null
resolutionSource
string | null
endDate
string <date-time> | null category string | null ammType string | null liquidity string | null sponsorName
string | null sponsorImage string | null startDate string | null
xAxisValue
string | null
yAxisValue
string | null
denominationToken
string | null
fee
string | null
image
string | null
icon
string | null
lowerBound
string | null
upperBound
string | null
description
string | null
outcomes
string | null

outcomePrices
string | null
volume
string | null
active
boolean | null
marketType
string | null
formatType
string | null
lowerBoundDate
string | null
upperBoundDate
string | null
closed
boolean | null
marketMakerAddress
string
createdBy
integer | null
updatedBy
integer | null
createdAt
string <date-time> | null updatedAt string | null
closedTime
string | null
wideFormat
boolean | null
new

boolean | null
mailchimpTag
string | null
featured
boolean | null
archived
boolean | null
resolvedBy
string | null
restricted
boolean | null
marketGroup
integer | null
groupItemTitle
string | null
groupItemThreshold
string | null
questionID
string | null
umaEndDate
string | null
enableOrderBook
boolean | null
orderPriceMinTickSize
number | null
orderMinSize
number | null
umaResolutionStatus
string | null

curationOrder
integer | null
volumeNum
number | null
liquidityNum
number | null
endDateIso
string | null
startDateIso
string | null
umaEndDateIso
string | null
hasReviewedDates
boolean | null
readyForCron
boolean | null
commentsEnabled
boolean | null
volume24hr
number | null
volume1wk
number | null
volume1mo
number | null
volume1yr
number | null
gameStartTime
string | null

secondsDelay
integer | null
clobTokenIds
string | null
disqusThread
string | null
shortOutcomes
string | null
teamAID
string | null
teamBID
string | null
umaBond
string | null
umaReward
string | null
fpmmLive
boolean | null
volume24hrAmm
number | null
volume1wkAmm
number | null
volume1moAmm
number | null
volume1yrAmm
number | null
volume24hrClob
number | null
volume1wkClob

number | null
volume1moClob
number | null
volume1yrClob
number | null
volumeAmm
number | null
volumeClob
number | null
liquidityAmm
number | null
liquidityClob
number | null
makerBaseFee
integer | null
takerBaseFee
integer | null
customLiveness
integer | null
acceptingOrders
boolean | null
notificationsEnabled
boolean | null
score
integer | null
imageOptimized
object
Hide child attributes
imageOptimized.id

string
imageOptimized.imageUrlSource
string | null
imageOptimized.imageUrlOptimized
string | null
imageOptimized.imageSizeKbSource
number | null
imageOptimized.imageSizeKbOptimized
number | null
imageOptimized.imageOptimizedComplete
boolean | null
imageOptimized.imageOptimizedLastUpdated
string | null
imageOptimized.relID
integer | null
imageOptimized.field
string | null
imageOptimized.relname
string | null
iconOptimized
object
Hide child attributes
iconOptimized.id
string
iconOptimized.imageUrlSource
string | null
iconOptimized.imageUrlOptimized
string | null
iconOptimized.imageSizeKbSource

number | null
iconOptimized.imageSizeKbOptimized
number | null
iconOptimized.imageOptimizedComplete
boolean | null
iconOptimized.imageOptimizedLastUpdated
string | null
iconOptimized.relID
integer | null
iconOptimized.field
string | null
iconOptimized.relname
string | null
events
object[]
Hide child attributes
events.id
string
events.ticker
string | null
events.slug
string | null
events.title
string | null
events.subtitle
string | null
events.description
string | null
events.resolutionSource

string | null
events.startDate
string <date-time> | null events.creationDate string | null
events.endDate
string <date-time> | null events.image string | null events.icon string | null events.active boolean | null
events.closed boolean | null events.archived boolean | null events.new boolean | null events.featured
boolean | null events.restricted boolean | null events.liquidity number | null events.volume number | null
events.openInterest number | null events.sortBy string | null events.category string | null
events.subcategory string | null events.isTemplate boolean | null events.templateVariables string | null
events.published_at string | null events.createdBy string | null events.updatedBy string | null
events.createdAt string | null
events.updatedAt
string` | null
events.commentsEnabled
boolean | null
events.competitive
number | null
events.volume24hr
number | null
events.volume1wk
number | null
events.volume1mo
number | null
events.volume1yr
number | null
events.featuredImage
string | null
events.disqusThread
string | null
events.parentEvent
string | null

events.enableOrderBook
boolean | null
events.liquidityAmm
number | null
events.liquidityClob
number | null
events.negRisk
boolean | null
events.negRiskMarketID
string | null
events.negRiskFeeBips
integer | null
events.commentCount
integer | null
events.imageOptimized
object
Hide child attributes
events.imageOptimized.id
string
events.imageOptimized.imageUrlSource
string | null
events.imageOptimized.imageUrlOptimized
string | null
events.imageOptimized.imageSizeKbSource
number | null
events.imageOptimized.imageSizeKbOptimized
number | null
events.imageOptimized.imageOptimizedComplete
boolean | null

events.imageOptimized.imageOptimizedLastUpdated
string | null
events.imageOptimized.relID
integer | null
events.imageOptimized.field
string | null
events.imageOptimized.relname
string | null
events.iconOptimized
object
Hide child attributes
events.iconOptimized.id
string
events.iconOptimized.imageUrlSource
string | null
events.iconOptimized.imageUrlOptimized
string | null
events.iconOptimized.imageSizeKbSource
number | null
events.iconOptimized.imageSizeKbOptimized
number | null
events.iconOptimized.imageOptimizedComplete
boolean | null
events.iconOptimized.imageOptimizedLastUpdated
string | null
events.iconOptimized.relID
integer | null
events.iconOptimized.field
string | null

events.iconOptimized.relname
string | null
events.featuredImageOptimized
object
Hide child attributes
events.featuredImageOptimized.id
string
events.featuredImageOptimized.imageUrlSource
string | null
events.featuredImageOptimized.imageUrlOptimized
string | null
events.featuredImageOptimized.imageSizeKbSource
number | null
events.featuredImageOptimized.imageSizeKbOptimized
number | null
events.featuredImageOptimized.imageOptimizedComplete
boolean | null
events.featuredImageOptimized.imageOptimizedLastUpdated
string | null
events.featuredImageOptimized.relID
integer | null
events.featuredImageOptimized.field
string | null
events.featuredImageOptimized.relname
string | null
events.subEvents
string[] | null
events.markets
array

events.series
object[]
Hide child attributes
events.series.id
string
events.series.ticker
string | null
events.series.slug
string | null
events.series.title
string | null
events.series.subtitle
string | null
events.series.seriesType
string | null
events.series.recurrence
string | null
events.series.description
string | null
events.series.image
string | null
events.series.icon
string | null
events.series.layout
string | null
events.series.active
boolean | null
events.series.closed
boolean | null

events.series.archived
boolean | null
events.series.new
boolean | null
events.series.featured
boolean | null
events.series.restricted
boolean | null
events.series.isTemplate
boolean | null
events.series.templateVariables
boolean | null
events.series.publishedAt
string | null
events.series.createdBy
string | null
events.series.updatedBy
string | null
events.series.createdAt
string <date-time> | null events.series.updatedAt string | null
events.series.commentsEnabled
boolean | null
events.series.competitive
string | null
events.series.volume24hr
number | null
events.series.volume
number | null
events.series.liquidity

number | null
events.series.startDate
string` | null
events.series.pythTokenID
string | null
events.series.cgAssetName
string | null
events.series.score
integer | null
events.series.events
array
events.series.collections
object[]
Hide child attributes
events.series.collections.id
string
events.series.collections.ticker
string | null
events.series.collections.slug
string | null
events.series.collections.title
string | null
events.series.collections.subtitle
string | null
events.series.collections.collectionType
string | null
events.series.collections.description
string | null
events.series.collections.tags

string | null
events.series.collections.image
string | null
events.series.collections.icon
string | null
events.series.collections.headerImage
string | null
events.series.collections.layout
string | null
events.series.collections.active
boolean | null
events.series.collections.closed
boolean | null
events.series.collections.archived
boolean | null
events.series.collections.new
boolean | null
events.series.collections.featured
boolean | null
events.series.collections.restricted
boolean | null
events.series.collections.isTemplate
boolean | null
events.series.collections.templateVariables
string | null
events.series.collections.publishedAt
string | null
events.series.collections.createdBy
string | null

events.series.collections.updatedBy
string | null
events.series.collections.createdAt
string <date-time> | null events.series.collections.updatedAt string | null
events.series.collections.commentsEnabled
boolean | null
events.series.collections.imageOptimized
object
Hide child attributes
events.series.collections.imageOptimized.id
string
events.series.collections.imageOptimized.imageUrlSource
string | null
events.series.collections.imageOptimized.imageUrlOptimized
string | null
events.series.collections.imageOptimized.imageSizeKbSource
number | null
events.series.collections.imageOptimized.imageSizeKbOptimized
number | null
events.series.collections.imageOptimized.imageOptimizedComplete
boolean | null
events.series.collections.imageOptimized.imageOptimizedLastUpdated
string | null
events.series.collections.imageOptimized.relID
integer | null
events.series.collections.imageOptimized.field
string | null
events.series.collections.imageOptimized.relname
string | null

events.series.collections.iconOptimized
object
Hide child attributes
events.series.collections.iconOptimized.id
string
events.series.collections.iconOptimized.imageUrlSource
string | null
events.series.collections.iconOptimized.imageUrlOptimized
string | null
events.series.collections.iconOptimized.imageSizeKbSource
number | null
events.series.collections.iconOptimized.imageSizeKbOptimized
number | null
events.series.collections.iconOptimized.imageOptimizedComplete
boolean | null
events.series.collections.iconOptimized.imageOptimizedLastUpdated
string | null
events.series.collections.iconOptimized.relID
integer | null
events.series.collections.iconOptimized.field
string | null
events.series.collections.iconOptimized.relname
string | null
events.series.collections.headerImageOptimized
object
Hide child attributes
events.series.collections.headerImageOptimized.id
string

events.series.collections.headerImageOptimized.imageUrlSource
string | null
events.series.collections.headerImageOptimized.imageUrlOptimized
string | null
events.series.collections.headerImageOptimized.imageSizeKbSource
number | null
events.series.collections.headerImageOptimized.imageSizeKbOptimized
number | null
events.series.collections.headerImageOptimized.imageOptimizedComplete
boolean | null
events.series.collections.headerImageOptimized.imageOptimizedLastUpdated
string | null
events.series.collections.headerImageOptimized.relID
integer | null
events.series.collections.headerImageOptimized.field
string | null
events.series.collections.headerImageOptimized.relname
string | null
events.series.categories
object[]
Hide child attributes
events.series.categories.id
string
events.series.categories.label
string | null
events.series.categories.parentCategory
string | null
events.series.categories.slug
string | null

events.series.categories.publishedAt
string | null
events.series.categories.createdBy
string | null
events.series.categories.updatedBy
string | null
events.series.categories.createdAt
string <date-time> | null events.series.categories.updatedAt string | null
events.series.tags
object[]
Hide child attributes
events.series.tags.id
string
events.series.tags.label
string | null
events.series.tags.slug
string | null
events.series.tags.forceShow
boolean | null
events.series.tags.publishedAt
string | null
events.series.tags.createdBy
integer | null
events.series.tags.updatedBy
integer | null
events.series.tags.createdAt
string <date-time> | null events.series.tags.updatedAt string | null
events.series.tags.forceHide
boolean | null

events.series.tags.isCarousel
boolean | null
events.series.commentCount
integer | null
events.series.chats
object[]
Hide child attributes
events.series.chats.id
string
events.series.chats.channelId
string | null
events.series.chats.channelName
string | null
events.series.chats.channelImage
string | null
events.series.chats.live
boolean | null
events.series.chats.startTime
string <date-time> | null events.series.chats.endTime string | null
events.categories
object[]
Hide child attributes
events.categories.id
string
events.categories.label
string | null
events.categories.parentCategory
string | null

events.categories.slug
string | null
events.categories.publishedAt
string | null
events.categories.createdBy
string | null
events.categories.updatedBy
string | null
events.categories.createdAt
string <date-time> | null events.categories.updatedAt string | null
events.collections
object[]
Hide child attributes
events.collections.id
string
events.collections.ticker
string | null
events.collections.slug
string | null
events.collections.title
string | null
events.collections.subtitle
string | null
events.collections.collectionType
string | null
events.collections.description
string | null
events.collections.tags
string | null

events.collections.image
string | null
events.collections.icon
string | null
events.collections.headerImage
string | null
events.collections.layout
string | null
events.collections.active
boolean | null
events.collections.closed
boolean | null
events.collections.archived
boolean | null
events.collections.new
boolean | null
events.collections.featured
boolean | null
events.collections.restricted
boolean | null
events.collections.isTemplate
boolean | null
events.collections.templateVariables
string | null
events.collections.publishedAt
string | null
events.collections.createdBy
string | null
events.collections.updatedBy

string | null
events.collections.createdAt
string <date-time> | null events.collections.updatedAt string | null
events.collections.commentsEnabled
boolean | null
events.collections.imageOptimized
object
Hide child attributes
events.collections.imageOptimized.id
string
events.collections.imageOptimized.imageUrlSource
string | null
events.collections.imageOptimized.imageUrlOptimized
string | null
events.collections.imageOptimized.imageSizeKbSource
number | null
events.collections.imageOptimized.imageSizeKbOptimized
number | null
events.collections.imageOptimized.imageOptimizedComplete
boolean | null
events.collections.imageOptimized.imageOptimizedLastUpdated
string | null
events.collections.imageOptimized.relID
integer | null
events.collections.imageOptimized.field
string | null
events.collections.imageOptimized.relname
string | null
events.collections.iconOptimized

object
Hide child attributes
events.collections.iconOptimized.id
string
events.collections.iconOptimized.imageUrlSource
string | null
events.collections.iconOptimized.imageUrlOptimized
string | null
events.collections.iconOptimized.imageSizeKbSource
number | null
events.collections.iconOptimized.imageSizeKbOptimized
number | null
events.collections.iconOptimized.imageOptimizedComplete
boolean | null
events.collections.iconOptimized.imageOptimizedLastUpdated
string | null
events.collections.iconOptimized.relID
integer | null
events.collections.iconOptimized.field
string | null
events.collections.iconOptimized.relname
string | null
events.collections.headerImageOptimized
object
Hide child attributes
events.collections.headerImageOptimized.id
string
events.collections.headerImageOptimized.imageUrlSource
string | null

events.collections.headerImageOptimized.imageUrlOptimized
string | null
events.collections.headerImageOptimized.imageSizeKbSource
number | null
events.collections.headerImageOptimized.imageSizeKbOptimized
number | null
events.collections.headerImageOptimized.imageOptimizedComplete
boolean | null
events.collections.headerImageOptimized.imageOptimizedLastUpdated
string | null
events.collections.headerImageOptimized.relID
integer | null
events.collections.headerImageOptimized.field
string | null
events.collections.headerImageOptimized.relname
string | null
events.tags
object[]
Hide child attributes
events.tags.id
string
events.tags.label
string | null
events.tags.slug
string | null
events.tags.forceShow
boolean | null
events.tags.publishedAt
string | null

events.tags.createdBy
integer | null
events.tags.updatedBy
integer | null
events.tags.createdAt
string <date-time> | null events.tags.updatedAt string | null
events.tags.forceHide
boolean | null
events.tags.isCarousel
boolean | null
events.cyom
boolean | null
events.closedTime
string <date-time> | null events.showAllOutcomes boolean | null events.showMarketImages boolean |
null events.automaticallyResolved boolean | null events.enableNegRisk boolean | null
events.automaticallyActive boolean | null events.eventDate string | null events.startTime string | null
events.eventWeek
integer | null
events.seriesSlug
string | null
events.score
string | null
events.elapsed
string | null
events.period
string | null
events.live
boolean | null
events.ended

boolean | null
events.finishedTimestamp
string` | null
events.gmpChartMode
string | null
events.eventCreators
object[]
Hide child attributes
events.eventCreators.id
string
events.eventCreators.creatorName
string | null
events.eventCreators.creatorHandle
string | null
events.eventCreators.creatorUrl
string | null
events.eventCreators.creatorImage
string | null
events.eventCreators.createdAt
string <date-time> | null events.eventCreators.updatedAt string | null
events.tweetCount
integer | null
events.chats
object[]
Hide child attributes
events.chats.id
string
events.chats.channelId
string | null

events.chats.channelName
string | null
events.chats.channelImage
string | null
events.chats.live
boolean | null
events.chats.startTime
string <date-time> | null events.chats.endTime string | null
events.featuredOrder
integer | null
events.estimateValue
boolean | null
events.cantEstimate
boolean | null
events.estimatedValue
string | null
events.templates
object[]
Hide child attributes
events.templates.id
string
events.templates.eventTitle
string | null
events.templates.eventSlug
string | null
events.templates.eventImage
string | null
events.templates.marketTitle
string | null

events.templates.description
string | null
events.templates.resolutionSource
string | null
events.templates.negRisk
boolean | null
events.templates.sortBy
string | null
events.templates.showMarketImages
boolean | null
events.templates.seriesSlug
string | null
events.templates.outcomes
string | null
events.spreadsMainLine
number | null
events.totalsMainLine
number | null
events.carouselMap
string | null
events.pendingDeployment
boolean | null
events.deploying
boolean | null
events.deployingTimestamp
string <date-time> | null events.scheduledDeploymentTimestamp string | null
events.gameStatus
string | null

categories
object[]
Hide child attributes
categories.id
string
categories.label
string | null
categories.parentCategory
string | null
categories.slug
string | null
categories.publishedAt
string | null
categories.createdBy
string | null
categories.updatedBy
string | null
categories.createdAt
string <date-time> | null categories.updatedAt string | null
tags
object[]
Hide child attributes
tags.id
string
tags.label
string | null
tags.slug
string | null
tags.forceShow

boolean | null
tags.publishedAt
string | null
tags.createdBy
integer | null
tags.updatedBy
integer | null
tags.createdAt
string <date-time> | null tags.updatedAt string | null
tags.forceHide
boolean | null
tags.isCarousel
boolean | null
creator
string | null
ready
boolean | null
funded
boolean | null
pastSlugs
string | null
readyTimestamp
string <date-time> | null fundedTimestamp string | null
acceptingOrdersTimestamp
string <date-time> | null competitive number | null rewardsMinSize number | null rewardsMaxSpread
number | null spread number | null automaticallyResolved boolean | null oneDayPriceChange number |
null oneHourPriceChange number | null oneWeekPriceChange number | null oneMonthPriceChange
number | null oneYearPriceChange number | null lastTradePrice number | null bestBid number | null
bestAsk number | null automaticallyActive boolean | null clearBookOnStart boolean | null chartColor
string | null seriesColor string | null showGmpSeries boolean | null showGmpOutcome boolean | null
manualActivation boolean | null negRiskOther boolean | null gameId string | null groupItemRange string
| null sportsMarketType string | null line number | null umaResolutionStatuses string | null

pendingDeployment boolean | null deploying boolean | null deployingTimestamp string | null
scheduledDeploymentTimestamp
string <date-time> | null rfqEnabled boolean | null eventStartTime string | null
Response
404
Not found
List series
GET/series
List series
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/series
Python
import requests
url = "https://gamma-api.polymarket.com/series"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/series', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php

$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/series",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/series"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java

HttpResponse<String> response = Unirest.get("https://gamma-api.polymarket.com/series")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/series")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"seriesType": "<string>",
"recurrence": "<string>",
"description": "<string>",
"image": "<string>",
"icon": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": true,
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"competitive": "<string>",
"volume24hr": 123,
"volume": 123,

"liquidity": 123,
"startDate": "2023-11-07T05:31:56Z",
"pythTokenID": "<string>",
"cgAssetName": "<string>",
"score": 123,
"events": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"creationDate": "2023-11-07T05:31:56Z",
"endDate": "2023-11-07T05:31:56Z",
"image": "<string>",
"icon": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"liquidity": 123,
"volume": 123,
"openInterest": 123,
"sortBy": "<string>",
"category": "<string>",
"subcategory": "<string>",
"isTemplate": true,
"templateVariables": "<string>",
"published_at": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"competitive": 123,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,
"featuredImage": "<string>",
"disqusThread": "<string>",
"parentEvent": "<string>",
"enableOrderBook": true,
"liquidityAmm": 123,
"liquidityClob": 123,
"negRisk": true,
"negRiskMarketID": "<string>",

"negRiskFeeBips": 123,
"commentCount": 123,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"featuredImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"subEvents": [
"<string>"
],
"markets": [
{
"id": "<string>",
"question": "<string>",
"conditionId": "<string>",
"slug": "<string>",
"twitterCardImage": "<string>",
"resolutionSource": "<string>",
"endDate": "2023-11-07T05:31:56Z",
"category": "<string>",
"ammType": "<string>",

"liquidity": "<string>",
"sponsorName": "<string>",
"sponsorImage": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"xAxisValue": "<string>",
"yAxisValue": "<string>",
"denominationToken": "<string>",
"fee": "<string>",
"image": "<string>",
"icon": "<string>",
"lowerBound": "<string>",
"upperBound": "<string>",
"description": "<string>",
"outcomes": "<string>",
"outcomePrices": "<string>",
"volume": "<string>",
"active": true,
"marketType": "<string>",
"formatType": "<string>",
"lowerBoundDate": "<string>",
"upperBoundDate": "<string>",
"closed": true,
"marketMakerAddress": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"closedTime": "<string>",
"wideFormat": true,
"new": true,
"mailchimpTag": "<string>",
"featured": true,
"archived": true,
"resolvedBy": "<string>",
"restricted": true,
"marketGroup": 123,
"groupItemTitle": "<string>",
"groupItemThreshold": "<string>",
"questionID": "<string>",
"umaEndDate": "<string>",
"enableOrderBook": true,
"orderPriceMinTickSize": 123,
"orderMinSize": 123,
"umaResolutionStatus": "<string>",
"curationOrder": 123,
"volumeNum": 123,
"liquidityNum": 123,
"endDateIso": "<string>",
"startDateIso": "<string>",
"umaEndDateIso": "<string>",
"hasReviewedDates": true,
"readyForCron": true,

"commentsEnabled": true,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,
"gameStartTime": "<string>",
"secondsDelay": 123,
"clobTokenIds": "<string>",
"disqusThread": "<string>",
"shortOutcomes": "<string>",
"teamAID": "<string>",
"teamBID": "<string>",
"umaBond": "<string>",
"umaReward": "<string>",
"fpmmLive": true,
"volume24hrAmm": 123,
"volume1wkAmm": 123,
"volume1moAmm": 123,
"volume1yrAmm": 123,
"volume24hrClob": 123,
"volume1wkClob": 123,
"volume1moClob": 123,
"volume1yrClob": 123,
"volumeAmm": 123,
"volumeClob": 123,
"liquidityAmm": 123,
"liquidityClob": 123,
"makerBaseFee": 123,
"takerBaseFee": 123,
"customLiveness": 123,
"acceptingOrders": true,
"notificationsEnabled": true,
"score": 123,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,

"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"events": "<array>",
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"creator": "<string>",
"ready": true,
"funded": true,
"pastSlugs": "<string>",
"readyTimestamp": "2023-11-07T05:31:56Z",
"fundedTimestamp": "2023-11-07T05:31:56Z",
"acceptingOrdersTimestamp": "2023-11-07T05:31:56Z",
"competitive": 123,
"rewardsMinSize": 123,
"rewardsMaxSpread": 123,
"spread": 123,
"automaticallyResolved": true,
"oneDayPriceChange": 123,
"oneHourPriceChange": 123,
"oneWeekPriceChange": 123,
"oneMonthPriceChange": 123,
"oneYearPriceChange": 123,
"lastTradePrice": 123,

"bestBid": 123,
"bestAsk": 123,
"automaticallyActive": true,
"clearBookOnStart": true,
"chartColor": "<string>",
"seriesColor": "<string>",
"showGmpSeries": true,
"showGmpOutcome": true,
"manualActivation": true,
"negRiskOther": true,
"gameId": "<string>",
"groupItemRange": "<string>",
"sportsMarketType": "<string>",
"line": 123,
"umaResolutionStatuses": "<string>",
"pendingDeployment": true,
"deploying": true,
"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",
"rfqEnabled": true,
"eventStartTime": "2023-11-07T05:31:56Z"
}
],
"series": "<array>",
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"collections": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",
"image": "<string>",
"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,

"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
}
}
],
"tags": [

{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"cyom": true,
"closedTime": "2023-11-07T05:31:56Z",
"showAllOutcomes": true,
"showMarketImages": true,
"automaticallyResolved": true,
"enableNegRisk": true,
"automaticallyActive": true,
"eventDate": "<string>",
"startTime": "2023-11-07T05:31:56Z",
"eventWeek": 123,
"seriesSlug": "<string>",
"score": "<string>",
"elapsed": "<string>",
"period": "<string>",
"live": true,
"ended": true,
"finishedTimestamp": "2023-11-07T05:31:56Z",
"gmpChartMode": "<string>",
"eventCreators": [
{
"id": "<string>",
"creatorName": "<string>",
"creatorHandle": "<string>",
"creatorUrl": "<string>",
"creatorImage": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tweetCount": 123,
"chats": [
{
"id": "<string>",
"channelId": "<string>",
"channelName": "<string>",
"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",

"endTime": "2023-11-07T05:31:56Z"
}
],
"featuredOrder": 123,
"estimateValue": true,
"cantEstimate": true,
"estimatedValue": "<string>",
"templates": [
{
"id": "<string>",
"eventTitle": "<string>",
"eventSlug": "<string>",
"eventImage": "<string>",
"marketTitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",
"negRisk": true,
"sortBy": "<string>",
"showMarketImages": true,
"seriesSlug": "<string>",
"outcomes": "<string>"
}
],
"spreadsMainLine": 123,
"totalsMainLine": 123,
"carouselMap": "<string>",
"pendingDeployment": true,
"deploying": true,
"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",
"gameStatus": "<string>"
}
],
"collections": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",
"image": "<string>",
"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,

"restricted": true,
"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
}
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",

"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"commentCount": 123,
"chats": [
{
"id": "<string>",
"channelId": "<string>",
"channelName": "<string>",
"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",
"endTime": "2023-11-07T05:31:56Z"
}
]
}
]
Query Parameters
limit
integer
Required range: x >= 0
offset
integer
Required range: x >= 0
order

string
Comma-separated list of fields to order by
ascending
boolean
slug
string[]
categories_ids
integer[]
categories_labels
string[]
closed
boolean
include_chat
boolean
recurrence
string
Response
200 - application/json
List of series
id
string
ticker
string | null
slug
string | null
title
string | null

subtitle
string | null
seriesType
string | null
recurrence
string | null
description
string | null
image
string | null
icon
string | null
layout
string | null
active
boolean | null
closed
boolean | null
archived
boolean | null
new
boolean | null
featured
boolean | null
restricted
boolean | null
isTemplate
boolean | null
templateVariables

boolean | null
publishedAt
string | null
createdBy
string | null
updatedBy
string | null
createdAt
string <date-time> | null updatedAt string | null
commentsEnabled
boolean | null
competitive
string | null
volume24hr
number | null
volume
number | null
liquidity
number | null
startDate
string` | null
pythTokenID
string | null
cgAssetName
string | null
score
integer | null
events

object[]
Hide child attributes
events.id
string
events.ticker
string | null
events.slug
string | null
events.title
string | null
events.subtitle
string | null
events.description
string | null
events.resolutionSource
string | null
events.startDate
string <date-time> | null events.creationDate string | null
events.endDate
string <date-time> | null events.image string | null events.icon string | null events.active boolean | null
events.closed boolean | null events.archived boolean | null events.new boolean | null events.featured
boolean | null events.restricted boolean | null events.liquidity number | null events.volume number | null
events.openInterest number | null events.sortBy string | null events.category string | null
events.subcategory string | null events.isTemplate boolean | null events.templateVariables string | null
events.published_at string | null events.createdBy string | null events.updatedBy string | null
events.createdAt string | null
events.updatedAt
string` | null
events.commentsEnabled
boolean | null
events.competitive

number | null
events.volume24hr
number | null
events.volume1wk
number | null
events.volume1mo
number | null
events.volume1yr
number | null
events.featuredImage
string | null
events.disqusThread
string | null
events.parentEvent
string | null
events.enableOrderBook
boolean | null
events.liquidityAmm
number | null
events.liquidityClob
number | null
events.negRisk
boolean | null
events.negRiskMarketID
string | null
events.negRiskFeeBips
integer | null
events.commentCount
integer | null

events.imageOptimized
object
Hide child attributes
events.imageOptimized.id
string
events.imageOptimized.imageUrlSource
string | null
events.imageOptimized.imageUrlOptimized
string | null
events.imageOptimized.imageSizeKbSource
number | null
events.imageOptimized.imageSizeKbOptimized
number | null
events.imageOptimized.imageOptimizedComplete
boolean | null
events.imageOptimized.imageOptimizedLastUpdated
string | null
events.imageOptimized.relID
integer | null
events.imageOptimized.field
string | null
events.imageOptimized.relname
string | null
events.iconOptimized
object
Hide child attributes
events.iconOptimized.id
string

events.iconOptimized.imageUrlSource
string | null
events.iconOptimized.imageUrlOptimized
string | null
events.iconOptimized.imageSizeKbSource
number | null
events.iconOptimized.imageSizeKbOptimized
number | null
events.iconOptimized.imageOptimizedComplete
boolean | null
events.iconOptimized.imageOptimizedLastUpdated
string | null
events.iconOptimized.relID
integer | null
events.iconOptimized.field
string | null
events.iconOptimized.relname
string | null
events.featuredImageOptimized
object
Hide child attributes
events.featuredImageOptimized.id
string
events.featuredImageOptimized.imageUrlSource
string | null
events.featuredImageOptimized.imageUrlOptimized
string | null
events.featuredImageOptimized.imageSizeKbSource
number | null

events.featuredImageOptimized.imageSizeKbOptimized
number | null
events.featuredImageOptimized.imageOptimizedComplete
boolean | null
events.featuredImageOptimized.imageOptimizedLastUpdated
string | null
events.featuredImageOptimized.relID
integer | null
events.featuredImageOptimized.field
string | null
events.featuredImageOptimized.relname
string | null
events.subEvents
string[] | null
events.markets
object[]
Hide child attributes
events.markets.id
string
events.markets.question
string | null
events.markets.conditionId
string
events.markets.slug
string | null
events.markets.twitterCardImage
string | null
events.markets.resolutionSource
string | null

events.markets.endDate
string <date-time> | null events.markets.category string | null events.markets.ammType string | null
events.markets.liquidity string | null events.markets.sponsorName string | null
events.markets.sponsorImage string | null events.markets.startDate string | null
events.markets.xAxisValue
string | null
events.markets.yAxisValue
string | null
events.markets.denominationToken
string | null
events.markets.fee
string | null
events.markets.image
string | null
events.markets.icon
string | null
events.markets.lowerBound
string | null
events.markets.upperBound
string | null
events.markets.description
string | null
events.markets.outcomes
string | null
events.markets.outcomePrices
string | null
events.markets.volume
string | null
events.markets.active
boolean | null

events.markets.marketType
string | null
events.markets.formatType
string | null
events.markets.lowerBoundDate
string | null
events.markets.upperBoundDate
string | null
events.markets.closed
boolean | null
events.markets.marketMakerAddress
string
events.markets.createdBy
integer | null
events.markets.updatedBy
integer | null
events.markets.createdAt
string <date-time> | null events.markets.updatedAt string | null
events.markets.closedTime
string | null
events.markets.wideFormat
boolean | null
events.markets.new
boolean | null
events.markets.mailchimpTag
string | null
events.markets.featured
boolean | null

events.markets.archived
boolean | null
events.markets.resolvedBy
string | null
events.markets.restricted
boolean | null
events.markets.marketGroup
integer | null
events.markets.groupItemTitle
string | null
events.markets.groupItemThreshold
string | null
events.markets.questionID
string | null
events.markets.umaEndDate
string | null
events.markets.enableOrderBook
boolean | null
events.markets.orderPriceMinTickSize
number | null
events.markets.orderMinSize
number | null
events.markets.umaResolutionStatus
string | null
events.markets.curationOrder
integer | null
events.markets.volumeNum
number | null
events.markets.liquidityNum

number | null
events.markets.endDateIso
string | null
events.markets.startDateIso
string | null
events.markets.umaEndDateIso
string | null
events.markets.hasReviewedDates
boolean | null
events.markets.readyForCron
boolean | null
events.markets.commentsEnabled
boolean | null
events.markets.volume24hr
number | null
events.markets.volume1wk
number | null
events.markets.volume1mo
number | null
events.markets.volume1yr
number | null
events.markets.gameStartTime
string | null
events.markets.secondsDelay
integer | null
events.markets.clobTokenIds
string | null
events.markets.disqusThread
string | null

events.markets.shortOutcomes
string | null
events.markets.teamAID
string | null
events.markets.teamBID
string | null
events.markets.umaBond
string | null
events.markets.umaReward
string | null
events.markets.fpmmLive
boolean | null
events.markets.volume24hrAmm
number | null
events.markets.volume1wkAmm
number | null
events.markets.volume1moAmm
number | null
events.markets.volume1yrAmm
number | null
events.markets.volume24hrClob
number | null
events.markets.volume1wkClob
number | null
events.markets.volume1moClob
number | null
events.markets.volume1yrClob
number | null

events.markets.volumeAmm
number | null
events.markets.volumeClob
number | null
events.markets.liquidityAmm
number | null
events.markets.liquidityClob
number | null
events.markets.makerBaseFee
integer | null
events.markets.takerBaseFee
integer | null
events.markets.customLiveness
integer | null
events.markets.acceptingOrders
boolean | null
events.markets.notificationsEnabled
boolean | null
events.markets.score
integer | null
events.markets.imageOptimized
object
Hide child attributes
events.markets.imageOptimized.id
string
events.markets.imageOptimized.imageUrlSource
string | null
events.markets.imageOptimized.imageUrlOptimized
string | null

events.markets.imageOptimized.imageSizeKbSource
number | null
events.markets.imageOptimized.imageSizeKbOptimized
number | null
events.markets.imageOptimized.imageOptimizedComplete
boolean | null
events.markets.imageOptimized.imageOptimizedLastUpdated
string | null
events.markets.imageOptimized.relID
integer | null
events.markets.imageOptimized.field
string | null
events.markets.imageOptimized.relname
string | null
events.markets.iconOptimized
object
Hide child attributes
events.markets.iconOptimized.id
string
events.markets.iconOptimized.imageUrlSource
string | null
events.markets.iconOptimized.imageUrlOptimized
string | null
events.markets.iconOptimized.imageSizeKbSource
number | null
events.markets.iconOptimized.imageSizeKbOptimized
number | null
events.markets.iconOptimized.imageOptimizedComplete
boolean | null

events.markets.iconOptimized.imageOptimizedLastUpdated
string | null
events.markets.iconOptimized.relID
integer | null
events.markets.iconOptimized.field
string | null
events.markets.iconOptimized.relname
string | null
events.markets.events
array
events.markets.categories
object[]
Hide child attributes
events.markets.categories.id
string
events.markets.categories.label
string | null
events.markets.categories.parentCategory
string | null
events.markets.categories.slug
string | null
events.markets.categories.publishedAt
string | null
events.markets.categories.createdBy
string | null
events.markets.categories.updatedBy
string | null
events.markets.categories.createdAt
string <date-time> | null events.markets.categories.updatedAt string | null

events.markets.tags
object[]
Hide child attributes
events.markets.tags.id
string
events.markets.tags.label
string | null
events.markets.tags.slug
string | null
events.markets.tags.forceShow
boolean | null
events.markets.tags.publishedAt
string | null
events.markets.tags.createdBy
integer | null
events.markets.tags.updatedBy
integer | null
events.markets.tags.createdAt
string <date-time> | null events.markets.tags.updatedAt string | null
events.markets.tags.forceHide
boolean | null
events.markets.tags.isCarousel
boolean | null
events.markets.creator
string | null
events.markets.ready
boolean | null
events.markets.funded
boolean | null

events.markets.pastSlugs
string | null
events.markets.readyTimestamp
string <date-time> | null events.markets.fundedTimestamp string | null
events.markets.acceptingOrdersTimestamp
string <date-time> | null events.markets.competitive number | null events.markets.rewardsMinSize
number | null events.markets.rewardsMaxSpread number | null events.markets.spread number | null
events.markets.automaticallyResolved boolean | null events.markets.oneDayPriceChange number | null
events.markets.oneHourPriceChange number | null events.markets.oneWeekPriceChange number | null
events.markets.oneMonthPriceChange number | null events.markets.oneYearPriceChange number |
null events.markets.lastTradePrice number | null events.markets.bestBid number | null
events.markets.bestAsk number | null events.markets.automaticallyActive boolean | null
events.markets.clearBookOnStart boolean | null events.markets.chartColor string | null
events.markets.seriesColor string | null events.markets.showGmpSeries boolean | null
events.markets.showGmpOutcome boolean | null events.markets.manualActivation boolean | null
events.markets.negRiskOther boolean | null events.markets.gameId string | null
events.markets.groupItemRange string | null events.markets.sportsMarketType string | null
events.markets.line number | null events.markets.umaResolutionStatuses string | null
events.markets.pendingDeployment boolean | null events.markets.deploying boolean | null
events.markets.deployingTimestamp string | null
events.markets.scheduledDeploymentTimestamp
string <date-time> | null events.markets.rfqEnabled boolean | null events.markets.eventStartTime string
| null
events.series
array
events.categories
object[]
Hide child attributes
events.categories.id
string
events.categories.label
string | null
events.categories.parentCategory
string | null
events.categories.slug

string | null
events.categories.publishedAt
string | null
events.categories.createdBy
string | null
events.categories.updatedBy
string | null
events.categories.createdAt
string <date-time> | null events.categories.updatedAt string | null
events.collections
object[]
Hide child attributes
events.collections.id
string
events.collections.ticker
string | null
events.collections.slug
string | null
events.collections.title
string | null
events.collections.subtitle
string | null
events.collections.collectionType
string | null
events.collections.description
string | null
events.collections.tags
string | null
events.collections.image

string | null
events.collections.icon
string | null
events.collections.headerImage
string | null
events.collections.layout
string | null
events.collections.active
boolean | null
events.collections.closed
boolean | null
events.collections.archived
boolean | null
events.collections.new
boolean | null
events.collections.featured
boolean | null
events.collections.restricted
boolean | null
events.collections.isTemplate
boolean | null
events.collections.templateVariables
string | null
events.collections.publishedAt
string | null
events.collections.createdBy
string | null
events.collections.updatedBy
string | null

events.collections.createdAt
string <date-time> | null events.collections.updatedAt string | null
events.collections.commentsEnabled
boolean | null
events.collections.imageOptimized
object
Hide child attributes
events.collections.imageOptimized.id
string
events.collections.imageOptimized.imageUrlSource
string | null
events.collections.imageOptimized.imageUrlOptimized
string | null
events.collections.imageOptimized.imageSizeKbSource
number | null
events.collections.imageOptimized.imageSizeKbOptimized
number | null
events.collections.imageOptimized.imageOptimizedComplete
boolean | null
events.collections.imageOptimized.imageOptimizedLastUpdated
string | null
events.collections.imageOptimized.relID
integer | null
events.collections.imageOptimized.field
string | null
events.collections.imageOptimized.relname
string | null
events.collections.iconOptimized

object
Hide child attributes
events.collections.iconOptimized.id
string
events.collections.iconOptimized.imageUrlSource
string | null
events.collections.iconOptimized.imageUrlOptimized
string | null
events.collections.iconOptimized.imageSizeKbSource
number | null
events.collections.iconOptimized.imageSizeKbOptimized
number | null
events.collections.iconOptimized.imageOptimizedComplete
boolean | null
events.collections.iconOptimized.imageOptimizedLastUpdated
string | null
events.collections.iconOptimized.relID
integer | null
events.collections.iconOptimized.field
string | null
events.collections.iconOptimized.relname
string | null
events.collections.headerImageOptimized
object
Hide child attributes
events.collections.headerImageOptimized.id
string
events.collections.headerImageOptimized.imageUrlSource
string | null

events.collections.headerImageOptimized.imageUrlOptimized
string | null
events.collections.headerImageOptimized.imageSizeKbSource
number | null
events.collections.headerImageOptimized.imageSizeKbOptimized
number | null
events.collections.headerImageOptimized.imageOptimizedComplete
boolean | null
events.collections.headerImageOptimized.imageOptimizedLastUpdated
string | null
events.collections.headerImageOptimized.relID
integer | null
events.collections.headerImageOptimized.field
string | null
events.collections.headerImageOptimized.relname
string | null
events.tags
object[]
Hide child attributes
events.tags.id
string
events.tags.label
string | null
events.tags.slug
string | null
events.tags.forceShow
boolean | null
events.tags.publishedAt
string | null

events.tags.createdBy
integer | null
events.tags.updatedBy
integer | null
events.tags.createdAt
string <date-time> | null events.tags.updatedAt string | null
events.tags.forceHide
boolean | null
events.tags.isCarousel
boolean | null
events.cyom
boolean | null
events.closedTime
string <date-time> | null events.showAllOutcomes boolean | null events.showMarketImages boolean |
null events.automaticallyResolved boolean | null events.enableNegRisk boolean | null
events.automaticallyActive boolean | null events.eventDate string | null events.startTime string | null
events.eventWeek
integer | null
events.seriesSlug
string | null
events.score
string | null
events.elapsed
string | null
events.period
string | null
events.live
boolean | null
events.ended

boolean | null
events.finishedTimestamp
string` | null
events.gmpChartMode
string | null
events.eventCreators
object[]
Hide child attributes
events.eventCreators.id
string
events.eventCreators.creatorName
string | null
events.eventCreators.creatorHandle
string | null
events.eventCreators.creatorUrl
string | null
events.eventCreators.creatorImage
string | null
events.eventCreators.createdAt
string <date-time> | null events.eventCreators.updatedAt string | null
events.tweetCount
integer | null
events.chats
object[]
Hide child attributes
events.chats.id
string
events.chats.channelId
string | null

events.chats.channelName
string | null
events.chats.channelImage
string | null
events.chats.live
boolean | null
events.chats.startTime
string <date-time> | null events.chats.endTime string | null
events.featuredOrder
integer | null
events.estimateValue
boolean | null
events.cantEstimate
boolean | null
events.estimatedValue
string | null
events.templates
object[]
Hide child attributes
events.templates.id
string
events.templates.eventTitle
string | null
events.templates.eventSlug
string | null
events.templates.eventImage
string | null
events.templates.marketTitle
string | null

events.templates.description
string | null
events.templates.resolutionSource
string | null
events.templates.negRisk
boolean | null
events.templates.sortBy
string | null
events.templates.showMarketImages
boolean | null
events.templates.seriesSlug
string | null
events.templates.outcomes
string | null
events.spreadsMainLine
number | null
events.totalsMainLine
number | null
events.carouselMap
string | null
events.pendingDeployment
boolean | null
events.deploying
boolean | null
events.deployingTimestamp
string <date-time> | null events.scheduledDeploymentTimestamp string | null
events.gameStatus
string | null

collections
object[]
Hide child attributes
collections.id
string
collections.ticker
string | null
collections.slug
string | null
collections.title
string | null
collections.subtitle
string | null
collections.collectionType
string | null
collections.description
string | null
collections.tags
string | null
collections.image
string | null
collections.icon
string | null
collections.headerImage
string | null
collections.layout
string | null
collections.active
boolean | null

collections.closed
boolean | null
collections.archived
boolean | null
collections.new
boolean | null
collections.featured
boolean | null
collections.restricted
boolean | null
collections.isTemplate
boolean | null
collections.templateVariables
string | null
collections.publishedAt
string | null
collections.createdBy
string | null
collections.updatedBy
string | null
collections.createdAt
string <date-time> | null collections.updatedAt string | null
collections.commentsEnabled
boolean | null
collections.imageOptimized
object
Hide child attributes
collections.imageOptimized.id
string

collections.imageOptimized.imageUrlSource
string | null
collections.imageOptimized.imageUrlOptimized
string | null
collections.imageOptimized.imageSizeKbSource
number | null
collections.imageOptimized.imageSizeKbOptimized
number | null
collections.imageOptimized.imageOptimizedComplete
boolean | null
collections.imageOptimized.imageOptimizedLastUpdated
string | null
collections.imageOptimized.relID
integer | null
collections.imageOptimized.field
string | null
collections.imageOptimized.relname
string | null
collections.iconOptimized
object
Hide child attributes
collections.iconOptimized.id
string
collections.iconOptimized.imageUrlSource
string | null
collections.iconOptimized.imageUrlOptimized
string | null
collections.iconOptimized.imageSizeKbSource
number | null

collections.iconOptimized.imageSizeKbOptimized
number | null
collections.iconOptimized.imageOptimizedComplete
boolean | null
collections.iconOptimized.imageOptimizedLastUpdated
string | null
collections.iconOptimized.relID
integer | null
collections.iconOptimized.field
string | null
collections.iconOptimized.relname
string | null
collections.headerImageOptimized
object
Hide child attributes
collections.headerImageOptimized.id
string
collections.headerImageOptimized.imageUrlSource
string | null
collections.headerImageOptimized.imageUrlOptimized
string | null
collections.headerImageOptimized.imageSizeKbSource
number | null
collections.headerImageOptimized.imageSizeKbOptimized
number | null
collections.headerImageOptimized.imageOptimizedComplete
boolean | null
collections.headerImageOptimized.imageOptimizedLastUpdated
string | null

collections.headerImageOptimized.relID
integer | null
collections.headerImageOptimized.field
string | null
collections.headerImageOptimized.relname
string | null
categories
object[]
Hide child attributes
categories.id
string
categories.label
string | null
categories.parentCategory
string | null
categories.slug
string | null
categories.publishedAt
string | null
categories.createdBy
string | null
categories.updatedBy
string | null
categories.createdAt
string <date-time> | null categories.updatedAt string | null
tags
object[]
Hide child attributes
tags.id

string
tags.label
string | null
tags.slug
string | null
tags.forceShow
boolean | null
tags.publishedAt
string | null
tags.createdBy
integer | null
tags.updatedBy
integer | null
tags.createdAt
string <date-time> | null tags.updatedAt string | null
tags.forceHide
boolean | null
tags.isCarousel
boolean | null
commentCount
integer | null
chats
object[]
Hide child attributes
chats.id
string
chats.channelId
string | null
chats.channelName

string | null
chats.channelImage
string | null
chats.live
boolean | null
chats.startTime
string <date-time> | null chats.endTime string | null
Get series by id
GET/series/{id}
Get series by id
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/series/{id}
Python
import requests
url = "https://gamma-api.polymarket.com/series/{id}"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/series/{id}', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [

CURLOPT_URL => "https://gamma-api.polymarket.com/series/{id}",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/series/{id}"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/series/{id}")
.asString();
```

Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/series/{id}")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"seriesType": "<string>",
"recurrence": "<string>",
"description": "<string>",
"image": "<string>",
"icon": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": true,
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"competitive": "<string>",
"volume24hr": 123,
"volume": 123,
"liquidity": 123,
"startDate": "2023-11-07T05:31:56Z",
"pythTokenID": "<string>",
"cgAssetName": "<string>",
"score": 123,

"events": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"creationDate": "2023-11-07T05:31:56Z",
"endDate": "2023-11-07T05:31:56Z",
"image": "<string>",
"icon": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"liquidity": 123,
"volume": 123,
"openInterest": 123,
"sortBy": "<string>",
"category": "<string>",
"subcategory": "<string>",
"isTemplate": true,
"templateVariables": "<string>",
"published_at": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"competitive": 123,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,
"featuredImage": "<string>",
"disqusThread": "<string>",
"parentEvent": "<string>",
"enableOrderBook": true,
"liquidityAmm": 123,
"liquidityClob": 123,
"negRisk": true,
"negRiskMarketID": "<string>",
"negRiskFeeBips": 123,
"commentCount": 123,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",

"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"featuredImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"subEvents": [
"<string>"
],
"markets": [
{
"id": "<string>",
"question": "<string>",
"conditionId": "<string>",
"slug": "<string>",
"twitterCardImage": "<string>",
"resolutionSource": "<string>",
"endDate": "2023-11-07T05:31:56Z",
"category": "<string>",
"ammType": "<string>",
"liquidity": "<string>",
"sponsorName": "<string>",
"sponsorImage": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"xAxisValue": "<string>",

"yAxisValue": "<string>",
"denominationToken": "<string>",
"fee": "<string>",
"image": "<string>",
"icon": "<string>",
"lowerBound": "<string>",
"upperBound": "<string>",
"description": "<string>",
"outcomes": "<string>",
"outcomePrices": "<string>",
"volume": "<string>",
"active": true,
"marketType": "<string>",
"formatType": "<string>",
"lowerBoundDate": "<string>",
"upperBoundDate": "<string>",
"closed": true,
"marketMakerAddress": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"closedTime": "<string>",
"wideFormat": true,
"new": true,
"mailchimpTag": "<string>",
"featured": true,
"archived": true,
"resolvedBy": "<string>",
"restricted": true,
"marketGroup": 123,
"groupItemTitle": "<string>",
"groupItemThreshold": "<string>",
"questionID": "<string>",
"umaEndDate": "<string>",
"enableOrderBook": true,
"orderPriceMinTickSize": 123,
"orderMinSize": 123,
"umaResolutionStatus": "<string>",
"curationOrder": 123,
"volumeNum": 123,
"liquidityNum": 123,
"endDateIso": "<string>",
"startDateIso": "<string>",
"umaEndDateIso": "<string>",
"hasReviewedDates": true,
"readyForCron": true,
"commentsEnabled": true,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,

"gameStartTime": "<string>",
"secondsDelay": 123,
"clobTokenIds": "<string>",
"disqusThread": "<string>",
"shortOutcomes": "<string>",
"teamAID": "<string>",
"teamBID": "<string>",
"umaBond": "<string>",
"umaReward": "<string>",
"fpmmLive": true,
"volume24hrAmm": 123,
"volume1wkAmm": 123,
"volume1moAmm": 123,
"volume1yrAmm": 123,
"volume24hrClob": 123,
"volume1wkClob": 123,
"volume1moClob": 123,
"volume1yrClob": 123,
"volumeAmm": 123,
"volumeClob": 123,
"liquidityAmm": 123,
"liquidityClob": 123,
"makerBaseFee": 123,
"takerBaseFee": 123,
"customLiveness": 123,
"acceptingOrders": true,
"notificationsEnabled": true,
"score": 123,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},

"events": "<array>",
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"creator": "<string>",
"ready": true,
"funded": true,
"pastSlugs": "<string>",
"readyTimestamp": "2023-11-07T05:31:56Z",
"fundedTimestamp": "2023-11-07T05:31:56Z",
"acceptingOrdersTimestamp": "2023-11-07T05:31:56Z",
"competitive": 123,
"rewardsMinSize": 123,
"rewardsMaxSpread": 123,
"spread": 123,
"automaticallyResolved": true,
"oneDayPriceChange": 123,
"oneHourPriceChange": 123,
"oneWeekPriceChange": 123,
"oneMonthPriceChange": 123,
"oneYearPriceChange": 123,
"lastTradePrice": 123,
"bestBid": 123,
"bestAsk": 123,
"automaticallyActive": true,
"clearBookOnStart": true,
"chartColor": "<string>",

"seriesColor": "<string>",
"showGmpSeries": true,
"showGmpOutcome": true,
"manualActivation": true,
"negRiskOther": true,
"gameId": "<string>",
"groupItemRange": "<string>",
"sportsMarketType": "<string>",
"line": 123,
"umaResolutionStatuses": "<string>",
"pendingDeployment": true,
"deploying": true,
"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",
"rfqEnabled": true,
"eventStartTime": "2023-11-07T05:31:56Z"
}
],
"series": "<array>",
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"collections": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",
"image": "<string>",
"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,

"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
}
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,

"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"cyom": true,
"closedTime": "2023-11-07T05:31:56Z",
"showAllOutcomes": true,
"showMarketImages": true,
"automaticallyResolved": true,
"enableNegRisk": true,
"automaticallyActive": true,
"eventDate": "<string>",
"startTime": "2023-11-07T05:31:56Z",
"eventWeek": 123,
"seriesSlug": "<string>",
"score": "<string>",
"elapsed": "<string>",
"period": "<string>",
"live": true,
"ended": true,
"finishedTimestamp": "2023-11-07T05:31:56Z",
"gmpChartMode": "<string>",
"eventCreators": [
{
"id": "<string>",
"creatorName": "<string>",
"creatorHandle": "<string>",
"creatorUrl": "<string>",
"creatorImage": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tweetCount": 123,
"chats": [
{
"id": "<string>",
"channelId": "<string>",
"channelName": "<string>",
"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",
"endTime": "2023-11-07T05:31:56Z"
}
],
"featuredOrder": 123,
"estimateValue": true,

"cantEstimate": true,
"estimatedValue": "<string>",
"templates": [
{
"id": "<string>",
"eventTitle": "<string>",
"eventSlug": "<string>",
"eventImage": "<string>",
"marketTitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",
"negRisk": true,
"sortBy": "<string>",
"showMarketImages": true,
"seriesSlug": "<string>",
"outcomes": "<string>"
}
],
"spreadsMainLine": 123,
"totalsMainLine": 123,
"carouselMap": "<string>",
"pendingDeployment": true,
"deploying": true,
"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",
"gameStatus": "<string>"
}
],
"collections": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",
"image": "<string>",
"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",

"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
}
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",

"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"commentCount": 123,
"chats": [
{
"id": "<string>",
"channelId": "<string>",
"channelName": "<string>",
"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",
"endTime": "2023-11-07T05:31:56Z"
}
]
}
Path Parameters
id
integer
required
Query Parameters
include_chat
boolean
Response
200

application/json
Series
id
string
ticker
string | null
slug
string | null
title
string | null
subtitle
string | null
seriesType
string | null
recurrence
string | null
description
string | null
image
string | null
icon
string | null
layout
string | null
active
boolean | null
closed
boolean | null
archived
boolean | null

new
boolean | null
featured
boolean | null
restricted
boolean | null
isTemplate
boolean | null
templateVariables
boolean | null
publishedAt
string | null
createdBy
string | null
updatedBy
string | null
createdAt
string <date-time> | null updatedAt string | null
commentsEnabled
boolean | null
competitive
string | null
volume24hr
number | null
volume
number | null
liquidity
number | null

startDate
string` | null
pythTokenID
string | null
cgAssetName
string | null
score
integer | null
events
object[]
Hide child attributes
events.id
string
events.ticker
string | null
events.slug
string | null
events.title
string | null
events.subtitle
string | null
events.description
string | null
events.resolutionSource
string | null
events.startDate
string <date-time> | null events.creationDate string | null
events.endDate
string <date-time> | null events.image string | null events.icon string | null events.active boolean | null
events.closed boolean | null events.archived boolean | null events.new boolean | null events.featured

boolean | null events.restricted boolean | null events.liquidity number | null events.volume number | null
events.openInterest number | null events.sortBy string | null events.category string | null
events.subcategory string | null events.isTemplate boolean | null events.templateVariables string | null
events.published_at string | null events.createdBy string | null events.updatedBy string | null
events.createdAt string | null
events.updatedAt
string` | null
events.commentsEnabled
boolean | null
events.competitive
number | null
events.volume24hr
number | null
events.volume1wk
number | null
events.volume1mo
number | null
events.volume1yr
number | null
events.featuredImage
string | null
events.disqusThread
string | null
events.parentEvent
string | null
events.enableOrderBook
boolean | null
events.liquidityAmm
number | null
events.liquidityClob
number | null

events.negRisk
boolean | null
events.negRiskMarketID
string | null
events.negRiskFeeBips
integer | null
events.commentCount
integer | null
events.imageOptimized
object
Hide child attributes
events.imageOptimized.id
string
events.imageOptimized.imageUrlSource
string | null
events.imageOptimized.imageUrlOptimized
string | null
events.imageOptimized.imageSizeKbSource
number | null
events.imageOptimized.imageSizeKbOptimized
number | null
events.imageOptimized.imageOptimizedComplete
boolean | null
events.imageOptimized.imageOptimizedLastUpdated
string | null
events.imageOptimized.relID
integer | null
events.imageOptimized.field
string | null

events.imageOptimized.relname
string | null
events.iconOptimized
object
Hide child attributes
events.iconOptimized.id
string
events.iconOptimized.imageUrlSource
string | null
events.iconOptimized.imageUrlOptimized
string | null
events.iconOptimized.imageSizeKbSource
number | null
events.iconOptimized.imageSizeKbOptimized
number | null
events.iconOptimized.imageOptimizedComplete
boolean | null
events.iconOptimized.imageOptimizedLastUpdated
string | null
events.iconOptimized.relID
integer | null
events.iconOptimized.field
string | null
events.iconOptimized.relname
string | null
events.featuredImageOptimized
object
Hide child attributes

events.featuredImageOptimized.id
string
events.featuredImageOptimized.imageUrlSource
string | null
events.featuredImageOptimized.imageUrlOptimized
string | null
events.featuredImageOptimized.imageSizeKbSource
number | null
events.featuredImageOptimized.imageSizeKbOptimized
number | null
events.featuredImageOptimized.imageOptimizedComplete
boolean | null
events.featuredImageOptimized.imageOptimizedLastUpdated
string | null
events.featuredImageOptimized.relID
integer | null
events.featuredImageOptimized.field
string | null
events.featuredImageOptimized.relname
string | null
events.subEvents
string[] | null
events.markets
object[]
Hide child attributes
events.markets.id
string
events.markets.question
string | null

events.markets.conditionId
string
events.markets.slug
string | null
events.markets.twitterCardImage
string | null
events.markets.resolutionSource
string | null
events.markets.endDate
string <date-time> | null events.markets.category string | null events.markets.ammType string | null
events.markets.liquidity string | null events.markets.sponsorName string | null
events.markets.sponsorImage string | null events.markets.startDate string | null
events.markets.xAxisValue
string | null
events.markets.yAxisValue
string | null
events.markets.denominationToken
string | null
events.markets.fee
string | null
events.markets.image
string | null
events.markets.icon
string | null
events.markets.lowerBound
string | null
events.markets.upperBound
string | null
events.markets.description

string | null
events.markets.outcomes
string | null
events.markets.outcomePrices
string | null
events.markets.volume
string | null
events.markets.active
boolean | null
events.markets.marketType
string | null
events.markets.formatType
string | null
events.markets.lowerBoundDate
string | null
events.markets.upperBoundDate
string | null
events.markets.closed
boolean | null
events.markets.marketMakerAddress
string
events.markets.createdBy
integer | null
events.markets.updatedBy
integer | null
events.markets.createdAt
string <date-time> | null events.markets.updatedAt string | null
events.markets.closedTime
string | null

events.markets.wideFormat
boolean | null
events.markets.new
boolean | null
events.markets.mailchimpTag
string | null
events.markets.featured
boolean | null
events.markets.archived
boolean | null
events.markets.resolvedBy
string | null
events.markets.restricted
boolean | null
events.markets.marketGroup
integer | null
events.markets.groupItemTitle
string | null
events.markets.groupItemThreshold
string | null
events.markets.questionID
string | null
events.markets.umaEndDate
string | null
events.markets.enableOrderBook
boolean | null
events.markets.orderPriceMinTickSize
number | null

events.markets.orderMinSize
number | null
events.markets.umaResolutionStatus
string | null
events.markets.curationOrder
integer | null
events.markets.volumeNum
number | null
events.markets.liquidityNum
number | null
events.markets.endDateIso
string | null
events.markets.startDateIso
string | null
events.markets.umaEndDateIso
string | null
events.markets.hasReviewedDates
boolean | null
events.markets.readyForCron
boolean | null
events.markets.commentsEnabled
boolean | null
events.markets.volume24hr
number | null
events.markets.volume1wk
number | null
events.markets.volume1mo
number | null
events.markets.volume1yr

number | null
events.markets.gameStartTime
string | null
events.markets.secondsDelay
integer | null
events.markets.clobTokenIds
string | null
events.markets.disqusThread
string | null
events.markets.shortOutcomes
string | null
events.markets.teamAID
string | null
events.markets.teamBID
string | null
events.markets.umaBond
string | null
events.markets.umaReward
string | null
events.markets.fpmmLive
boolean | null
events.markets.volume24hrAmm
number | null
events.markets.volume1wkAmm
number | null
events.markets.volume1moAmm
number | null
events.markets.volume1yrAmm
number | null

events.markets.volume24hrClob
number | null
events.markets.volume1wkClob
number | null
events.markets.volume1moClob
number | null
events.markets.volume1yrClob
number | null
events.markets.volumeAmm
number | null
events.markets.volumeClob
number | null
events.markets.liquidityAmm
number | null
events.markets.liquidityClob
number | null
events.markets.makerBaseFee
integer | null
events.markets.takerBaseFee
integer | null
events.markets.customLiveness
integer | null
events.markets.acceptingOrders
boolean | null
events.markets.notificationsEnabled
boolean | null
events.markets.score
integer | null

events.markets.imageOptimized
object
Hide child attributes
events.markets.imageOptimized.id
string
events.markets.imageOptimized.imageUrlSource
string | null
events.markets.imageOptimized.imageUrlOptimized
string | null
events.markets.imageOptimized.imageSizeKbSource
number | null
events.markets.imageOptimized.imageSizeKbOptimized
number | null
events.markets.imageOptimized.imageOptimizedComplete
boolean | null
events.markets.imageOptimized.imageOptimizedLastUpdated
string | null
events.markets.imageOptimized.relID
integer | null
events.markets.imageOptimized.field
string | null
events.markets.imageOptimized.relname
string | null
events.markets.iconOptimized
object
Hide child attributes
events.markets.iconOptimized.id
string
events.markets.iconOptimized.imageUrlSource

string | null
events.markets.iconOptimized.imageUrlOptimized
string | null
events.markets.iconOptimized.imageSizeKbSource
number | null
events.markets.iconOptimized.imageSizeKbOptimized
number | null
events.markets.iconOptimized.imageOptimizedComplete
boolean | null
events.markets.iconOptimized.imageOptimizedLastUpdated
string | null
events.markets.iconOptimized.relID
integer | null
events.markets.iconOptimized.field
string | null
events.markets.iconOptimized.relname
string | null
events.markets.events
array
events.markets.categories
object[]
Hide child attributes
events.markets.categories.id
string
events.markets.categories.label
string | null
events.markets.categories.parentCategory
string | null
events.markets.categories.slug

string | null
events.markets.categories.publishedAt
string | null
events.markets.categories.createdBy
string | null
events.markets.categories.updatedBy
string | null
events.markets.categories.createdAt
string <date-time> | null events.markets.categories.updatedAt string | null
events.markets.tags
object[]
Hide child attributes
events.markets.tags.id
string
events.markets.tags.label
string | null
events.markets.tags.slug
string | null
events.markets.tags.forceShow
boolean | null
events.markets.tags.publishedAt
string | null
events.markets.tags.createdBy
integer | null
events.markets.tags.updatedBy
integer | null
events.markets.tags.createdAt
string <date-time> | null events.markets.tags.updatedAt string | null
events.markets.tags.forceHide

boolean | null
events.markets.tags.isCarousel
boolean | null
events.markets.creator
string | null
events.markets.ready
boolean | null
events.markets.funded
boolean | null
events.markets.pastSlugs
string | null
events.markets.readyTimestamp
string <date-time> | null events.markets.fundedTimestamp string | null
events.markets.acceptingOrdersTimestamp
string <date-time> | null events.markets.competitive number | null events.markets.rewardsMinSize
number | null events.markets.rewardsMaxSpread number | null events.markets.spread number | null
events.markets.automaticallyResolved boolean | null events.markets.oneDayPriceChange number | null
events.markets.oneHourPriceChange number | null events.markets.oneWeekPriceChange number | null
events.markets.oneMonthPriceChange number | null events.markets.oneYearPriceChange number |
null events.markets.lastTradePrice number | null events.markets.bestBid number | null
events.markets.bestAsk number | null events.markets.automaticallyActive boolean | null
events.markets.clearBookOnStart boolean | null events.markets.chartColor string | null
events.markets.seriesColor string | null events.markets.showGmpSeries boolean | null
events.markets.showGmpOutcome boolean | null events.markets.manualActivation boolean | null
events.markets.negRiskOther boolean | null events.markets.gameId string | null
events.markets.groupItemRange string | null events.markets.sportsMarketType string | null
events.markets.line number | null events.markets.umaResolutionStatuses string | null
events.markets.pendingDeployment boolean | null events.markets.deploying boolean | null
events.markets.deployingTimestamp string | null
events.markets.scheduledDeploymentTimestamp
string <date-time> | null events.markets.rfqEnabled boolean | null events.markets.eventStartTime string
| null
events.series
array
events.categories

object[]
Hide child attributes
events.categories.id
string
events.categories.label
string | null
events.categories.parentCategory
string | null
events.categories.slug
string | null
events.categories.publishedAt
string | null
events.categories.createdBy
string | null
events.categories.updatedBy
string | null
events.categories.createdAt
string <date-time> | null events.categories.updatedAt string | null
events.collections
object[]
Hide child attributes
events.collections.id
string
events.collections.ticker
string | null
events.collections.slug
string | null
events.collections.title
string | null

events.collections.subtitle
string | null
events.collections.collectionType
string | null
events.collections.description
string | null
events.collections.tags
string | null
events.collections.image
string | null
events.collections.icon
string | null
events.collections.headerImage
string | null
events.collections.layout
string | null
events.collections.active
boolean | null
events.collections.closed
boolean | null
events.collections.archived
boolean | null
events.collections.new
boolean | null
events.collections.featured
boolean | null
events.collections.restricted
boolean | null

events.collections.isTemplate
boolean | null
events.collections.templateVariables
string | null
events.collections.publishedAt
string | null
events.collections.createdBy
string | null
events.collections.updatedBy
string | null
events.collections.createdAt
string <date-time> | null events.collections.updatedAt string | null
events.collections.commentsEnabled
boolean | null
events.collections.imageOptimized
object
Hide child attributes
events.collections.imageOptimized.id
string
events.collections.imageOptimized.imageUrlSource
string | null
events.collections.imageOptimized.imageUrlOptimized
string | null
events.collections.imageOptimized.imageSizeKbSource
number | null
events.collections.imageOptimized.imageSizeKbOptimized
number | null
events.collections.imageOptimized.imageOptimizedComplete
boolean | null

events.collections.imageOptimized.imageOptimizedLastUpdated
string | null
events.collections.imageOptimized.relID
integer | null
events.collections.imageOptimized.field
string | null
events.collections.imageOptimized.relname
string | null
events.collections.iconOptimized
object
Hide child attributes
events.collections.iconOptimized.id
string
events.collections.iconOptimized.imageUrlSource
string | null
events.collections.iconOptimized.imageUrlOptimized
string | null
events.collections.iconOptimized.imageSizeKbSource
number | null
events.collections.iconOptimized.imageSizeKbOptimized
number | null
events.collections.iconOptimized.imageOptimizedComplete
boolean | null
events.collections.iconOptimized.imageOptimizedLastUpdated
string | null
events.collections.iconOptimized.relID
integer | null
events.collections.iconOptimized.field
string | null

events.collections.iconOptimized.relname
string | null
events.collections.headerImageOptimized
object
Hide child attributes
events.collections.headerImageOptimized.id
string
events.collections.headerImageOptimized.imageUrlSource
string | null
events.collections.headerImageOptimized.imageUrlOptimized
string | null
events.collections.headerImageOptimized.imageSizeKbSource
number | null
events.collections.headerImageOptimized.imageSizeKbOptimized
number | null
events.collections.headerImageOptimized.imageOptimizedComplete
boolean | null
events.collections.headerImageOptimized.imageOptimizedLastUpdated
string | null
events.collections.headerImageOptimized.relID
integer | null
events.collections.headerImageOptimized.field
string | null
events.collections.headerImageOptimized.relname
string | null
events.tags
object[]
Hide child attributes
events.tags.id

string
events.tags.label
string | null
events.tags.slug
string | null
events.tags.forceShow
boolean | null
events.tags.publishedAt
string | null
events.tags.createdBy
integer | null
events.tags.updatedBy
integer | null
events.tags.createdAt
string <date-time> | null events.tags.updatedAt string | null
events.tags.forceHide
boolean | null
events.tags.isCarousel
boolean | null
events.cyom
boolean | null
events.closedTime
string <date-time> | null events.showAllOutcomes boolean | null events.showMarketImages boolean |
null events.automaticallyResolved boolean | null events.enableNegRisk boolean | null
events.automaticallyActive boolean | null events.eventDate string | null events.startTime string | null
events.eventWeek
integer | null
events.seriesSlug
string | null

events.score
string | null
events.elapsed
string | null
events.period
string | null
events.live
boolean | null
events.ended
boolean | null
events.finishedTimestamp
string` | null
events.gmpChartMode
string | null
events.eventCreators
object[]
Hide child attributes
events.eventCreators.id
string
events.eventCreators.creatorName
string | null
events.eventCreators.creatorHandle
string | null
events.eventCreators.creatorUrl
string | null
events.eventCreators.creatorImage
string | null
events.eventCreators.createdAt
string <date-time> | null events.eventCreators.updatedAt string | null

events.tweetCount
integer | null
events.chats
object[]
Hide child attributes
events.chats.id
string
events.chats.channelId
string | null
events.chats.channelName
string | null
events.chats.channelImage
string | null
events.chats.live
boolean | null
events.chats.startTime
string <date-time> | null events.chats.endTime string | null
events.featuredOrder
integer | null
events.estimateValue
boolean | null
events.cantEstimate
boolean | null
events.estimatedValue
string | null
events.templates
object[]
Hide child attributes
events.templates.id

string
events.templates.eventTitle
string | null
events.templates.eventSlug
string | null
events.templates.eventImage
string | null
events.templates.marketTitle
string | null
events.templates.description
string | null
events.templates.resolutionSource
string | null
events.templates.negRisk
boolean | null
events.templates.sortBy
string | null
events.templates.showMarketImages
boolean | null
events.templates.seriesSlug
string | null
events.templates.outcomes
string | null
events.spreadsMainLine
number | null
events.totalsMainLine
number | null
events.carouselMap
string | null

events.pendingDeployment
boolean | null
events.deploying
boolean | null
events.deployingTimestamp
string <date-time> | null events.scheduledDeploymentTimestamp string | null
events.gameStatus
string | null
collections
object[]
Hide child attributes
collections.id
string
collections.ticker
string | null
collections.slug
string | null
collections.title
string | null
collections.subtitle
string | null
collections.collectionType
string | null
collections.description
string | null
collections.tags
string | null
collections.image
string | null

collections.icon
string | null
collections.headerImage
string | null
collections.layout
string | null
collections.active
boolean | null
collections.closed
boolean | null
collections.archived
boolean | null
collections.new
boolean | null
collections.featured
boolean | null
collections.restricted
boolean | null
collections.isTemplate
boolean | null
collections.templateVariables
string | null
collections.publishedAt
string | null
collections.createdBy
string | null
collections.updatedBy
string | null

collections.createdAt
string <date-time> | null collections.updatedAt string | null
collections.commentsEnabled
boolean | null
collections.imageOptimized
object
Hide child attributes
collections.imageOptimized.id
string
collections.imageOptimized.imageUrlSource
string | null
collections.imageOptimized.imageUrlOptimized
string | null
collections.imageOptimized.imageSizeKbSource
number | null
collections.imageOptimized.imageSizeKbOptimized
number | null
collections.imageOptimized.imageOptimizedComplete
boolean | null
collections.imageOptimized.imageOptimizedLastUpdated
string | null
collections.imageOptimized.relID
integer | null
collections.imageOptimized.field
string | null
collections.imageOptimized.relname
string | null
collections.iconOptimized
object
Hide child attributes

collections.iconOptimized.id
string
collections.iconOptimized.imageUrlSource
string | null
collections.iconOptimized.imageUrlOptimized
string | null
collections.iconOptimized.imageSizeKbSource
number | null
collections.iconOptimized.imageSizeKbOptimized
number | null
collections.iconOptimized.imageOptimizedComplete
boolean | null
collections.iconOptimized.imageOptimizedLastUpdated
string | null
collections.iconOptimized.relID
integer | null
collections.iconOptimized.field
string | null
collections.iconOptimized.relname
string | null
collections.headerImageOptimized
object
Hide child attributes
collections.headerImageOptimized.id
string
collections.headerImageOptimized.imageUrlSource
string | null
collections.headerImageOptimized.imageUrlOptimized
string | null

collections.headerImageOptimized.imageSizeKbSource
number | null
collections.headerImageOptimized.imageSizeKbOptimized
number | null
collections.headerImageOptimized.imageOptimizedComplete
boolean | null
collections.headerImageOptimized.imageOptimizedLastUpdated
string | null
collections.headerImageOptimized.relID
integer | null
collections.headerImageOptimized.field
string | null
collections.headerImageOptimized.relname
string | null
categories
object[]
Hide child attributes
categories.id
string
categories.label
string | null
categories.parentCategory
string | null
categories.slug
string | null
categories.publishedAt
string | null
categories.createdBy
string | null

categories.updatedBy
string | null
categories.createdAt
string <date-time> | null categories.updatedAt string | null
tags
object[]
Hide child attributes
tags.id
string
tags.label
string | null
tags.slug
string | null
tags.forceShow
boolean | null
tags.publishedAt
string | null
tags.createdBy
integer | null
tags.updatedBy
integer | null
tags.createdAt
string <date-time> | null tags.updatedAt string | null
tags.forceHide
boolean | null
tags.isCarousel
boolean | null
commentCount
integer | null

chats
object[]
Hide child attributes
chats.id
string
chats.channelId
string | null
chats.channelName
string | null
chats.channelImage
string | null
chats.live
boolean | null
chats.startTime
string <date-time> | null chats.endTime string | null
Response
404
Not found
Comments
List comments
GET/comments
List comments
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/comments

Python
import requests
url = "https://gamma-api.polymarket.com/comments"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/comments', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/comments",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main

```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/comments"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/comments")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/comments")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"id": "<string>",
"body": "<string>",
"parentEntityType": "<string>",
"parentEntityID": 123,

"parentCommentID": "<string>",
"userAddress": "<string>",
"replyAddress": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"profile": {
"name": "<string>",
"pseudonym": "<string>",
"displayUsernamePublic": true,
"bio": "<string>",
"isMod": true,
"isCreator": true,
"proxyWallet": "<string>",
"baseAddress": "<string>",
"profileImage": "<string>",
"profileImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"positions": [
{
"tokenId": "<string>",
"positionSize": "<string>"
}
]
},
"reactions": [
{
"id": "<string>",
"commentID": 123,
"reactionType": "<string>",
"icon": "<string>",
"userAddress": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"profile": {
"name": "<string>",
"pseudonym": "<string>",
"displayUsernamePublic": true,
"bio": "<string>",
"isMod": true,
"isCreator": true,
"proxyWallet": "<string>",
"baseAddress": "<string>",
"profileImage": "<string>",

"profileImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"positions": [
{
"tokenId": "<string>",
"positionSize": "<string>"
}
]
}
}
],
"reportCount": 123,
"reactionCount": 123
}
]
Query Parameters
limit
integer
Required range: x >= 0
offset
integer
Required range: x >= 0
order
string
Comma-separated list of fields to order by
ascending
boolean
parent_entity_type
enum`
Available options: Event, Series, market

parent_entity_id
integer
get_positions
boolean
holders_only
boolean
Response
200 - application/json
List of comments
id
string
body
string | null
parentEntityType
string | null
parentEntityID
integer | null
parentCommentID
string | null
userAddress
string | null
replyAddress
string | null
createdAt
string <date-time> | null updatedAt string | null
profile
object
Hide child attributes

profile.name
string | null
profile.pseudonym
string | null
profile.displayUsernamePublic
boolean | null
profile.bio
string | null
profile.isMod
boolean | null
profile.isCreator
boolean | null
profile.proxyWallet
string | null
profile.baseAddress
string | null
profile.profileImage
string | null
profile.profileImageOptimized
object
Hide child attributes
profile.profileImageOptimized.id
string
profile.profileImageOptimized.imageUrlSource
string | null
profile.profileImageOptimized.imageUrlOptimized
string | null
profile.profileImageOptimized.imageSizeKbSource
number | null

profile.profileImageOptimized.imageSizeKbOptimized
number | null
profile.profileImageOptimized.imageOptimizedComplete
boolean | null
profile.profileImageOptimized.imageOptimizedLastUpdated
string | null
profile.profileImageOptimized.relID
integer | null
profile.profileImageOptimized.field
string | null
profile.profileImageOptimized.relname
string | null
profile.positions
object[]
Hide child attributes
profile.positions.tokenId
string | null
profile.positions.positionSize
string | null
reactions
object[]
Hide child attributes
reactions.id
string
reactions.commentID
integer | null
reactions.reactionType
string | null

reactions.icon
string | null
reactions.userAddress
string | null
reactions.createdAt
string` | null
reactions.profile
object
Hide child attributes
reactions.profile.name
string | null
reactions.profile.pseudonym
string | null
reactions.profile.displayUsernamePublic
boolean | null
reactions.profile.bio
string | null
reactions.profile.isMod
boolean | null
reactions.profile.isCreator
boolean | null
reactions.profile.proxyWallet
string | null
reactions.profile.baseAddress
string | null
reactions.profile.profileImage
string | null
reactions.profile.profileImageOptimized
object
Hide child attributes

reactions.profile.profileImageOptimized.id
string
reactions.profile.profileImageOptimized.imageUrlSource
string | null
reactions.profile.profileImageOptimized.imageUrlOptimized
string | null
reactions.profile.profileImageOptimized.imageSizeKbSource
number | null
reactions.profile.profileImageOptimized.imageSizeKbOptimized
number | null
reactions.profile.profileImageOptimized.imageOptimizedComplete
boolean | null
reactions.profile.profileImageOptimized.imageOptimizedLastUpdated
string | null
reactions.profile.profileImageOptimized.relID
integer | null
reactions.profile.profileImageOptimized.field
string | null
reactions.profile.profileImageOptimized.relname
string | null
reactions.profile.positions
object[]
Hide child attributes
reactions.profile.positions.tokenId
string | null
reactions.profile.positions.positionSize
string | null
reportCount
integer | null

reactionCount
integer | null
Get comments by comment id
GET/comments/{id}
Get comments by comment id
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/comments/{id}
Python
import requests
url = "https://gamma-api.polymarket.com/comments/{id}"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/comments/{id}', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/comments/{id}",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,

CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/comments/{id}"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/comments/{id}")
.asString();
```
Ruby
require 'uri'
require 'net/http'

url = URI("https://gamma-api.polymarket.com/comments/{id}")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"id": "<string>",
"body": "<string>",
"parentEntityType": "<string>",
"parentEntityID": 123,
"parentCommentID": "<string>",
"userAddress": "<string>",
"replyAddress": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"profile": {
"name": "<string>",
"pseudonym": "<string>",
"displayUsernamePublic": true,
"bio": "<string>",
"isMod": true,
"isCreator": true,
"proxyWallet": "<string>",
"baseAddress": "<string>",
"profileImage": "<string>",
"profileImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"positions": [
{
"tokenId": "<string>",
"positionSize": "<string>"
}
]
},

"reactions": [
{
"id": "<string>",
"commentID": 123,
"reactionType": "<string>",
"icon": "<string>",
"userAddress": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"profile": {
"name": "<string>",
"pseudonym": "<string>",
"displayUsernamePublic": true,
"bio": "<string>",
"isMod": true,
"isCreator": true,
"proxyWallet": "<string>",
"baseAddress": "<string>",
"profileImage": "<string>",
"profileImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"positions": [
{
"tokenId": "<string>",
"positionSize": "<string>"
}
]
}
}
],
"reportCount": 123,
"reactionCount": 123
}
]
Path Parameters
id
integer
required

Query Parameters
get_positions
boolean
Response
200 - application/json
Comments
id
string
body
string | null
parentEntityType
string | null
parentEntityID
integer | null
parentCommentID
string | null
userAddress
string | null
replyAddress
string | null
createdAt
string <date-time> | null updatedAt string | null
profile
object
Hide child attributes
profile.name

string | null
profile.pseudonym
string | null
profile.displayUsernamePublic
boolean | null
profile.bio
string | null
profile.isMod
boolean | null
profile.isCreator
boolean | null
profile.proxyWallet
string | null
profile.baseAddress
string | null
profile.profileImage
string | null
profile.profileImageOptimized
object
Hide child attributes
profile.profileImageOptimized.id
string
profile.profileImageOptimized.imageUrlSource
string | null
profile.profileImageOptimized.imageUrlOptimized
string | null
profile.profileImageOptimized.imageSizeKbSource
number | null
profile.profileImageOptimized.imageSizeKbOptimized

number | null
profile.profileImageOptimized.imageOptimizedComplete
boolean | null
profile.profileImageOptimized.imageOptimizedLastUpdated
string | null
profile.profileImageOptimized.relID
integer | null
profile.profileImageOptimized.field
string | null
profile.profileImageOptimized.relname
string | null
profile.positions
object[]
Hide child attributes
profile.positions.tokenId
string | null
profile.positions.positionSize
string | null
reactions
object[]
Hide child attributes
reactions.id
string
reactions.commentID
integer | null
reactions.reactionType
string | null
reactions.icon
string | null

reactions.userAddress
string | null
reactions.createdAt
string` | null
reactions.profile
object
Hide child attributes
reactions.profile.name
string | null
reactions.profile.pseudonym
string | null
reactions.profile.displayUsernamePublic
boolean | null
reactions.profile.bio
string | null
reactions.profile.isMod
boolean | null
reactions.profile.isCreator
boolean | null
reactions.profile.proxyWallet
string | null
reactions.profile.baseAddress
string | null
reactions.profile.profileImage
string | null
reactions.profile.profileImageOptimized
object
Hide child attributes

reactions.profile.profileImageOptimized.id
string
reactions.profile.profileImageOptimized.imageUrlSource
string | null
reactions.profile.profileImageOptimized.imageUrlOptimized
string | null
reactions.profile.profileImageOptimized.imageSizeKbSource
number | null
reactions.profile.profileImageOptimized.imageSizeKbOptimized
number | null
reactions.profile.profileImageOptimized.imageOptimizedComplete
boolean | null
reactions.profile.profileImageOptimized.imageOptimizedLastUpdated
string | null
reactions.profile.profileImageOptimized.relID
integer | null
reactions.profile.profileImageOptimized.field
string | null
reactions.profile.profileImageOptimized.relname
string | null
reactions.profile.positions
object[]
Hide child attributes
reactions.profile.positions.tokenId
string | null
reactions.profile.positions.positionSize
string | null
Get comments by user address

GET/comments/user_address/{user_address}
Get comments by user address
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/comments/user_address/{user_address}
Python
import requests
url = "https://gamma-api.polymarket.com/comments/user_address/{user_address}"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/comments/user_address/{user_address}',
options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-
api.polymarket.com/comments/user_address/{user_address}",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);

if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/comments/user_address/{user_address}"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-
api.polymarket.com/comments/user_address/{user_address}")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/comments/user_address/{user_address}")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
200
[
{
"id": "<string>",
"body": "<string>",
"parentEntityType": "<string>",
"parentEntityID": 123,
"parentCommentID": "<string>",
"userAddress": "<string>",
"replyAddress": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"profile": {
"name": "<string>",
"pseudonym": "<string>",
"displayUsernamePublic": true,
"bio": "<string>",
"isMod": true,
"isCreator": true,
"proxyWallet": "<string>",
"baseAddress": "<string>",
"profileImage": "<string>",
"profileImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"positions": [
{
"tokenId": "<string>",
"positionSize": "<string>"
}
]
},
"reactions": [
{
"id": "<string>",
"commentID": 123,
"reactionType": "<string>",
"icon": "<string>",
"userAddress": "<string>",

"createdAt": "2023-11-07T05:31:56Z",
"profile": {
"name": "<string>",
"pseudonym": "<string>",
"displayUsernamePublic": true,
"bio": "<string>",
"isMod": true,
"isCreator": true,
"proxyWallet": "<string>",
"baseAddress": "<string>",
"profileImage": "<string>",
"profileImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"positions": [
{
"tokenId": "<string>",
"positionSize": "<string>"
}
]
}
}
],
"reportCount": 123,
"reactionCount": 123
}
]
Path Parameters
user_address
string
required
Query Parameters
limit

integer
Required range: x >= 0
offset
integer
Required range: x >= 0
order
string
Comma-separated list of fields to order by
ascending
boolean
Response
200 - application/json
Comments
id
string
body
string | null
parentEntityType
string | null
parentEntityID
integer | null
parentCommentID
string | null
userAddress
string | null
replyAddress
string | null
createdAt

string <date-time> | null updatedAt string | null
profile
object
Hide child attributes
profile.name
string | null
profile.pseudonym
string | null
profile.displayUsernamePublic
boolean | null
profile.bio
string | null
profile.isMod
boolean | null
profile.isCreator
boolean | null
profile.proxyWallet
string | null
profile.baseAddress
string | null
profile.profileImage
string | null
profile.profileImageOptimized
object
Hide child attributes
profile.profileImageOptimized.id
string
profile.profileImageOptimized.imageUrlSource
string | null

profile.profileImageOptimized.imageUrlOptimized
string | null
profile.profileImageOptimized.imageSizeKbSource
number | null
profile.profileImageOptimized.imageSizeKbOptimized
number | null
profile.profileImageOptimized.imageOptimizedComplete
boolean | null
profile.profileImageOptimized.imageOptimizedLastUpdated
string | null
profile.profileImageOptimized.relID
integer | null
profile.profileImageOptimized.field
string | null
profile.profileImageOptimized.relname
string | null
profile.positions
object[]
Hide child attributes
profile.positions.tokenId
string | null
profile.positions.positionSize
string | null
reactions
object[]
Hide child attributes
reactions.id
string

reactions.commentID
integer | null
reactions.reactionType
string | null
reactions.icon
string | null
reactions.userAddress
string | null
reactions.createdAt
string` | null
reactions.profile
object
Hide child attributes
reactions.profile.name
string | null
reactions.profile.pseudonym
string | null
reactions.profile.displayUsernamePublic
boolean | null
reactions.profile.bio
string | null
reactions.profile.isMod
boolean | null
reactions.profile.isCreator
boolean | null
reactions.profile.proxyWallet
string | null
reactions.profile.baseAddress
string | null

reactions.profile.profileImage
string | null
reactions.profile.profileImageOptimized
object
Hide child attributes
reactions.profile.profileImageOptimized.id
string
reactions.profile.profileImageOptimized.imageUrlSource
string | null
reactions.profile.profileImageOptimized.imageUrlOptimized
string | null
reactions.profile.profileImageOptimized.imageSizeKbSource
number | null
reactions.profile.profileImageOptimized.imageSizeKbOptimized
number | null
reactions.profile.profileImageOptimized.imageOptimizedComplete
boolean | null
reactions.profile.profileImageOptimized.imageOptimizedLastUpdated
string | null
reactions.profile.profileImageOptimized.relID
integer | null
reactions.profile.profileImageOptimized.field
string | null
reactions.profile.profileImageOptimized.relname
string | null
reactions.profile.positions
object[]
Hide child attributes
reactions.profile.positions.tokenId

string | null
reactions.profile.positions.positionSize
string | null
Profiles
Get public profile by wallet address
GET/public-profile
Get public profile by wallet address
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/public-profile
Python
import requests
url = "https://gamma-api.polymarket.com/public-profile"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/public-profile', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/public-profile",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,

CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://gamma-api.polymarket.com/public-profile"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-api.polymarket.com/public-
profile")
.asString();
```
Ruby
require 'uri'
require 'net/http'

url = URI("https://gamma-api.polymarket.com/public-profile")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
{
"createdAt": "2023-11-07T05:31:56Z",
"proxyWallet": "<string>",
"profileImage": "<string>",
"displayUsernamePublic": true,
"bio": "<string>",
"pseudonym": "<string>",
"name": "<string>",
"users": [
{
"id": "<string>",
"creator": true,
"mod": true
}
],
"xUsername": "<string>",
"verifiedBadge": true
}
400
{
"type": "validation error",
"error": "invalid address"
}
404
{
"type": "not found error",
"error": "profile not found"
}
Query Parameters
address

string
required
The wallet address (proxy wallet or user address)
Response
200
application/json
Public profile information
createdAt
string` | null
ISO 8601 timestamp of when the profile was created
proxyWallet
string | null
The proxy wallet address
profileImage
string` | null
URL to the profile image
displayUsernamePublic
boolean | null
Whether the username is displayed publicly
bio
string | null
Profile bio
pseudonym
string | null
Auto-generated pseudonym
name
string | null
User-chosen display name

users
object[] | null
Array of associated user objects
Hide child attributes
users.id
string
User ID
users.creator
boolean
Whether the user is a creator
users.mod
boolean
Whether the user is a moderator
xUsername
string | null
X (Twitter) username
verifiedBadge
boolean | null
Whether the profile has a verified badge
Response
400
application/json
Invalid address format
Error response for public profile endpoint
type
string
Error type classification

error
string
Error message
Response
404
application/json
Profile not found
Error response for public profile endpoint
type
string
Error type classification
error
string
Error message
Search
Search markets, events, and profiles
GET/public-search
Search markets, events, and profiles
```bash
cURL
curl --request GET \
--url https://gamma-api.polymarket.com/public-search
Python
import requests
url = "https://gamma-api.polymarket.com/public-search"
response = requests.get(url)

print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://gamma-api.polymarket.com/public-search', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://gamma-api.polymarket.com/public-search",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {

url := "https://gamma-api.polymarket.com/public-search"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://gamma-api.polymarket.com/public-
search")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://gamma-api.polymarket.com/public-search")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
{
"events": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"creationDate": "2023-11-07T05:31:56Z",
"endDate": "2023-11-07T05:31:56Z",

"image": "<string>",
"icon": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"liquidity": 123,
"volume": 123,
"openInterest": 123,
"sortBy": "<string>",
"category": "<string>",
"subcategory": "<string>",
"isTemplate": true,
"templateVariables": "<string>",
"published_at": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"competitive": 123,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,
"featuredImage": "<string>",
"disqusThread": "<string>",
"parentEvent": "<string>",
"enableOrderBook": true,
"liquidityAmm": 123,
"liquidityClob": 123,
"negRisk": true,
"negRiskMarketID": "<string>",
"negRiskFeeBips": 123,
"commentCount": 123,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",

"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"featuredImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"subEvents": [
"<string>"
],
"markets": [
{
"id": "<string>",
"question": "<string>",
"conditionId": "<string>",
"slug": "<string>",
"twitterCardImage": "<string>",
"resolutionSource": "<string>",
"endDate": "2023-11-07T05:31:56Z",
"category": "<string>",
"ammType": "<string>",
"liquidity": "<string>",
"sponsorName": "<string>",
"sponsorImage": "<string>",
"startDate": "2023-11-07T05:31:56Z",
"xAxisValue": "<string>",
"yAxisValue": "<string>",
"denominationToken": "<string>",
"fee": "<string>",
"image": "<string>",
"icon": "<string>",
"lowerBound": "<string>",
"upperBound": "<string>",
"description": "<string>",
"outcomes": "<string>",
"outcomePrices": "<string>",
"volume": "<string>",
"active": true,

"marketType": "<string>",
"formatType": "<string>",
"lowerBoundDate": "<string>",
"upperBoundDate": "<string>",
"closed": true,
"marketMakerAddress": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"closedTime": "<string>",
"wideFormat": true,
"new": true,
"mailchimpTag": "<string>",
"featured": true,
"archived": true,
"resolvedBy": "<string>",
"restricted": true,
"marketGroup": 123,
"groupItemTitle": "<string>",
"groupItemThreshold": "<string>",
"questionID": "<string>",
"umaEndDate": "<string>",
"enableOrderBook": true,
"orderPriceMinTickSize": 123,
"orderMinSize": 123,
"umaResolutionStatus": "<string>",
"curationOrder": 123,
"volumeNum": 123,
"liquidityNum": 123,
"endDateIso": "<string>",
"startDateIso": "<string>",
"umaEndDateIso": "<string>",
"hasReviewedDates": true,
"readyForCron": true,
"commentsEnabled": true,
"volume24hr": 123,
"volume1wk": 123,
"volume1mo": 123,
"volume1yr": 123,
"gameStartTime": "<string>",
"secondsDelay": 123,
"clobTokenIds": "<string>",
"disqusThread": "<string>",
"shortOutcomes": "<string>",
"teamAID": "<string>",
"teamBID": "<string>",
"umaBond": "<string>",
"umaReward": "<string>",
"fpmmLive": true,
"volume24hrAmm": 123,
"volume1wkAmm": 123,

"volume1moAmm": 123,
"volume1yrAmm": 123,
"volume24hrClob": 123,
"volume1wkClob": 123,
"volume1moClob": 123,
"volume1yrClob": 123,
"volumeAmm": 123,
"volumeClob": 123,
"liquidityAmm": 123,
"liquidityClob": 123,
"makerBaseFee": 123,
"takerBaseFee": 123,
"customLiveness": 123,
"acceptingOrders": true,
"notificationsEnabled": true,
"score": 123,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"events": "<array>",
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"

}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"creator": "<string>",
"ready": true,
"funded": true,
"pastSlugs": "<string>",
"readyTimestamp": "2023-11-07T05:31:56Z",
"fundedTimestamp": "2023-11-07T05:31:56Z",
"acceptingOrdersTimestamp": "2023-11-07T05:31:56Z",
"competitive": 123,
"rewardsMinSize": 123,
"rewardsMaxSpread": 123,
"spread": 123,
"automaticallyResolved": true,
"oneDayPriceChange": 123,
"oneHourPriceChange": 123,
"oneWeekPriceChange": 123,
"oneMonthPriceChange": 123,
"oneYearPriceChange": 123,
"lastTradePrice": 123,
"bestBid": 123,
"bestAsk": 123,
"automaticallyActive": true,
"clearBookOnStart": true,
"chartColor": "<string>",
"seriesColor": "<string>",
"showGmpSeries": true,
"showGmpOutcome": true,
"manualActivation": true,
"negRiskOther": true,
"gameId": "<string>",
"groupItemRange": "<string>",
"sportsMarketType": "<string>",
"line": 123,
"umaResolutionStatuses": "<string>",
"pendingDeployment": true,
"deploying": true,

"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",
"rfqEnabled": true,
"eventStartTime": "2023-11-07T05:31:56Z"
}
],
"series": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"seriesType": "<string>",
"recurrence": "<string>",
"description": "<string>",
"image": "<string>",
"icon": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": true,
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"competitive": "<string>",
"volume24hr": 123,
"volume": 123,
"liquidity": 123,
"startDate": "2023-11-07T05:31:56Z",
"pythTokenID": "<string>",
"cgAssetName": "<string>",
"score": 123,
"events": "<array>",
"collections": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",

"image": "<string>",
"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",

"relname": "<string>"
}
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"commentCount": 123,
"chats": [
{
"id": "<string>",
"channelId": "<string>",
"channelName": "<string>",
"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",
"endTime": "2023-11-07T05:31:56Z"
}
]
}
],
"categories": [
{
"id": "<string>",
"label": "<string>",
"parentCategory": "<string>",
"slug": "<string>",

"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"collections": [
{
"id": "<string>",
"ticker": "<string>",
"slug": "<string>",
"title": "<string>",
"subtitle": "<string>",
"collectionType": "<string>",
"description": "<string>",
"tags": "<string>",
"image": "<string>",
"icon": "<string>",
"headerImage": "<string>",
"layout": "<string>",
"active": true,
"closed": true,
"archived": true,
"new": true,
"featured": true,
"restricted": true,
"isTemplate": true,
"templateVariables": "<string>",
"publishedAt": "<string>",
"createdBy": "<string>",
"updatedBy": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"commentsEnabled": true,
"imageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"iconOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,

"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"headerImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
}
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"forceShow": true,
"publishedAt": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"forceHide": true,
"isCarousel": true
}
],
"cyom": true,
"closedTime": "2023-11-07T05:31:56Z",
"showAllOutcomes": true,
"showMarketImages": true,
"automaticallyResolved": true,
"enableNegRisk": true,
"automaticallyActive": true,
"eventDate": "<string>",
"startTime": "2023-11-07T05:31:56Z",
"eventWeek": 123,
"seriesSlug": "<string>",
"score": "<string>",
"elapsed": "<string>",
"period": "<string>",
"live": true,
"ended": true,

"finishedTimestamp": "2023-11-07T05:31:56Z",
"gmpChartMode": "<string>",
"eventCreators": [
{
"id": "<string>",
"creatorName": "<string>",
"creatorHandle": "<string>",
"creatorUrl": "<string>",
"creatorImage": "<string>",
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z"
}
],
"tweetCount": 123,
"chats": [
{
"id": "<string>",
"channelId": "<string>",
"channelName": "<string>",
"channelImage": "<string>",
"live": true,
"startTime": "2023-11-07T05:31:56Z",
"endTime": "2023-11-07T05:31:56Z"
}
],
"featuredOrder": 123,
"estimateValue": true,
"cantEstimate": true,
"estimatedValue": "<string>",
"templates": [
{
"id": "<string>",
"eventTitle": "<string>",
"eventSlug": "<string>",
"eventImage": "<string>",
"marketTitle": "<string>",
"description": "<string>",
"resolutionSource": "<string>",
"negRisk": true,
"sortBy": "<string>",
"showMarketImages": true,
"seriesSlug": "<string>",
"outcomes": "<string>"
}
],
"spreadsMainLine": 123,
"totalsMainLine": 123,
"carouselMap": "<string>",
"pendingDeployment": true,
"deploying": true,
"deployingTimestamp": "2023-11-07T05:31:56Z",
"scheduledDeploymentTimestamp": "2023-11-07T05:31:56Z",

"gameStatus": "<string>"
}
],
"tags": [
{
"id": "<string>",
"label": "<string>",
"slug": "<string>",
"event_count": 123
}
],
"profiles": [
{
"id": "<string>",
"name": "<string>",
"user": 123,
"referral": "<string>",
"createdBy": 123,
"updatedBy": 123,
"createdAt": "2023-11-07T05:31:56Z",
"updatedAt": "2023-11-07T05:31:56Z",
"utmSource": "<string>",
"utmMedium": "<string>",
"utmCampaign": "<string>",
"utmContent": "<string>",
"utmTerm": "<string>",
"walletActivated": true,
"pseudonym": "<string>",
"displayUsernamePublic": true,
"profileImage": "<string>",
"bio": "<string>",
"proxyWallet": "<string>",
"profileImageOptimized": {
"id": "<string>",
"imageUrlSource": "<string>",
"imageUrlOptimized": "<string>",
"imageSizeKbSource": 123,
"imageSizeKbOptimized": 123,
"imageOptimizedComplete": true,
"imageOptimizedLastUpdated": "<string>",
"relID": 123,
"field": "<string>",
"relname": "<string>"
},
"isCloseOnly": true,
"isCertReq": true,
"certReqDate": "2023-11-07T05:31:56Z"
}
],
"pagination": {
"hasMore": true,
"totalResults": 123

}
}
Query Parameters
q
string
required
cache
boolean
events_status
string
limit_per_type
integer
page
integer
events_tag
string[]
keep_closed_markets
integer
sort
string
ascending
boolean
search_tags
boolean
search_profiles
boolean
recurrence
string
exclude_tag_id

integer[]
optimized
boolean
Response
200 - application/json
Search results
events
object[] | null
Hide child attributes
events.id
string
events.ticker
string | null
events.slug
string | null
events.title
string | null
events.subtitle
string | null
events.description
string | null
events.resolutionSource
string | null
events.startDate
string <date-time> | null events.creationDate string | null
events.endDate
string <date-time> | null events.image string | null events.icon string | null events.active boolean | null
events.closed boolean | null events.archived boolean | null events.new boolean | null events.featured

boolean | null events.restricted boolean | null events.liquidity number | null events.volume number | null
events.openInterest number | null events.sortBy string | null events.category string | null
events.subcategory string | null events.isTemplate boolean | null events.templateVariables string | null
events.published_at string | null events.createdBy string | null events.updatedBy string | null
events.createdAt string | null
events.updatedAt
string` | null
events.commentsEnabled
boolean | null
events.competitive
number | null
events.volume24hr
number | null
events.volume1wk
number | null
events.volume1mo
number | null
events.volume1yr
number | null
events.featuredImage
string | null
events.disqusThread
string | null
events.parentEvent
string | null
events.enableOrderBook
boolean | null
events.liquidityAmm
number | null
events.liquidityClob
number | null

events.negRisk
boolean | null
events.negRiskMarketID
string | null
events.negRiskFeeBips
integer | null
events.commentCount
integer | null
events.imageOptimized
object
Hide child attributes
events.imageOptimized.id
string
events.imageOptimized.imageUrlSource
string | null
events.imageOptimized.imageUrlOptimized
string | null
events.imageOptimized.imageSizeKbSource
number | null
events.imageOptimized.imageSizeKbOptimized
number | null
events.imageOptimized.imageOptimizedComplete
boolean | null
events.imageOptimized.imageOptimizedLastUpdated
string | null
events.imageOptimized.relID
integer | null
events.imageOptimized.field
string | null

events.imageOptimized.relname
string | null
events.iconOptimized
object
Hide child attributes
events.iconOptimized.id
string
events.iconOptimized.imageUrlSource
string | null
events.iconOptimized.imageUrlOptimized
string | null
events.iconOptimized.imageSizeKbSource
number | null
events.iconOptimized.imageSizeKbOptimized
number | null
events.iconOptimized.imageOptimizedComplete
boolean | null
events.iconOptimized.imageOptimizedLastUpdated
string | null
events.iconOptimized.relID
integer | null
events.iconOptimized.field
string | null
events.iconOptimized.relname
string | null
events.featuredImageOptimized
object
Hide child attributes

events.featuredImageOptimized.id
string
events.featuredImageOptimized.imageUrlSource
string | null
events.featuredImageOptimized.imageUrlOptimized
string | null
events.featuredImageOptimized.imageSizeKbSource
number | null
events.featuredImageOptimized.imageSizeKbOptimized
number | null
events.featuredImageOptimized.imageOptimizedComplete
boolean | null
events.featuredImageOptimized.imageOptimizedLastUpdated
string | null
events.featuredImageOptimized.relID
integer | null
events.featuredImageOptimized.field
string | null
events.featuredImageOptimized.relname
string | null
events.subEvents
string[] | null
events.markets
object[]
Hide child attributes
events.markets.id
string
events.markets.question
string | null

events.markets.conditionId
string
events.markets.slug
string | null
events.markets.twitterCardImage
string | null
events.markets.resolutionSource
string | null
events.markets.endDate
string <date-time> | null events.markets.category string | null events.markets.ammType string | null
events.markets.liquidity string | null events.markets.sponsorName string | null
events.markets.sponsorImage string | null events.markets.startDate string | null
events.markets.xAxisValue
string | null
events.markets.yAxisValue
string | null
events.markets.denominationToken
string | null
events.markets.fee
string | null
events.markets.image
string | null
events.markets.icon
string | null
events.markets.lowerBound
string | null
events.markets.upperBound
string | null
events.markets.description

string | null
events.markets.outcomes
string | null
events.markets.outcomePrices
string | null
events.markets.volume
string | null
events.markets.active
boolean | null
events.markets.marketType
string | null
events.markets.formatType
string | null
events.markets.lowerBoundDate
string | null
events.markets.upperBoundDate
string | null
events.markets.closed
boolean | null
events.markets.marketMakerAddress
string
events.markets.createdBy
integer | null
events.markets.updatedBy
integer | null
events.markets.createdAt
string <date-time> | null events.markets.updatedAt string | null
events.markets.closedTime
string | null

events.markets.wideFormat
boolean | null
events.markets.new
boolean | null
events.markets.mailchimpTag
string | null
events.markets.featured
boolean | null
events.markets.archived
boolean | null
events.markets.resolvedBy
string | null
events.markets.restricted
boolean | null
events.markets.marketGroup
integer | null
events.markets.groupItemTitle
string | null
events.markets.groupItemThreshold
string | null
events.markets.questionID
string | null
events.markets.umaEndDate
string | null
events.markets.enableOrderBook
boolean | null
events.markets.orderPriceMinTickSize
number | null

events.markets.orderMinSize
number | null
events.markets.umaResolutionStatus
string | null
events.markets.curationOrder
integer | null
events.markets.volumeNum
number | null
events.markets.liquidityNum
number | null
events.markets.endDateIso
string | null
events.markets.startDateIso
string | null
events.markets.umaEndDateIso
string | null
events.markets.hasReviewedDates
boolean | null
events.markets.readyForCron
boolean | null
events.markets.commentsEnabled
boolean | null
events.markets.volume24hr
number | null
events.markets.volume1wk
number | null
events.markets.volume1mo
number | null
events.markets.volume1yr

number | null
events.markets.gameStartTime
string | null
events.markets.secondsDelay
integer | null
events.markets.clobTokenIds
string | null
events.markets.disqusThread
string | null
events.markets.shortOutcomes
string | null
events.markets.teamAID
string | null
events.markets.teamBID
string | null
events.markets.umaBond
string | null
events.markets.umaReward
string | null
events.markets.fpmmLive
boolean | null
events.markets.volume24hrAmm
number | null
events.markets.volume1wkAmm
number | null
events.markets.volume1moAmm
number | null
events.markets.volume1yrAmm
number | null

events.markets.volume24hrClob
number | null
events.markets.volume1wkClob
number | null
events.markets.volume1moClob
number | null
events.markets.volume1yrClob
number | null
events.markets.volumeAmm
number | null
events.markets.volumeClob
number | null
events.markets.liquidityAmm
number | null
events.markets.liquidityClob
number | null
events.markets.makerBaseFee
integer | null
events.markets.takerBaseFee
integer | null
events.markets.customLiveness
integer | null
events.markets.acceptingOrders
boolean | null
events.markets.notificationsEnabled
boolean | null
events.markets.score
integer | null

events.markets.imageOptimized
object
Hide child attributes
events.markets.imageOptimized.id
string
events.markets.imageOptimized.imageUrlSource
string | null
events.markets.imageOptimized.imageUrlOptimized
string | null
events.markets.imageOptimized.imageSizeKbSource
number | null
events.markets.imageOptimized.imageSizeKbOptimized
number | null
events.markets.imageOptimized.imageOptimizedComplete
boolean | null
events.markets.imageOptimized.imageOptimizedLastUpdated
string | null
events.markets.imageOptimized.relID
integer | null
events.markets.imageOptimized.field
string | null
events.markets.imageOptimized.relname
string | null
events.markets.iconOptimized
object
Hide child attributes
events.markets.iconOptimized.id
string
events.markets.iconOptimized.imageUrlSource

string | null
events.markets.iconOptimized.imageUrlOptimized
string | null
events.markets.iconOptimized.imageSizeKbSource
number | null
events.markets.iconOptimized.imageSizeKbOptimized
number | null
events.markets.iconOptimized.imageOptimizedComplete
boolean | null
events.markets.iconOptimized.imageOptimizedLastUpdated
string | null
events.markets.iconOptimized.relID
integer | null
events.markets.iconOptimized.field
string | null
events.markets.iconOptimized.relname
string | null
events.markets.events
array
events.markets.categories
object[]
Hide child attributes
events.markets.categories.id
string
events.markets.categories.label
string | null
events.markets.categories.parentCategory
string | null
events.markets.categories.slug

string | null
events.markets.categories.publishedAt
string | null
events.markets.categories.createdBy
string | null
events.markets.categories.updatedBy
string | null
events.markets.categories.createdAt
string <date-time> | null events.markets.categories.updatedAt string | null
events.markets.tags
object[]
Hide child attributes
events.markets.tags.id
string
events.markets.tags.label
string | null
events.markets.tags.slug
string | null
events.markets.tags.forceShow
boolean | null
events.markets.tags.publishedAt
string | null
events.markets.tags.createdBy
integer | null
events.markets.tags.updatedBy
integer | null
events.markets.tags.createdAt
string <date-time> | null events.markets.tags.updatedAt string | null
events.markets.tags.forceHide

boolean | null
events.markets.tags.isCarousel
boolean | null
events.markets.creator
string | null
events.markets.ready
boolean | null
events.markets.funded
boolean | null
events.markets.pastSlugs
string | null
events.markets.readyTimestamp
string <date-time> | null events.markets.fundedTimestamp string | null
events.markets.acceptingOrdersTimestamp
string <date-time> | null events.markets.competitive number | null events.markets.rewardsMinSize
number | null events.markets.rewardsMaxSpread number | null events.markets.spread number | null
events.markets.automaticallyResolved boolean | null events.markets.oneDayPriceChange number | null
events.markets.oneHourPriceChange number | null events.markets.oneWeekPriceChange number | null
events.markets.oneMonthPriceChange number | null events.markets.oneYearPriceChange number |
null events.markets.lastTradePrice number | null events.markets.bestBid number | null
events.markets.bestAsk number | null events.markets.automaticallyActive boolean | null
events.markets.clearBookOnStart boolean | null events.markets.chartColor string | null
events.markets.seriesColor string | null events.markets.showGmpSeries boolean | null
events.markets.showGmpOutcome boolean | null events.markets.manualActivation boolean | null
events.markets.negRiskOther boolean | null events.markets.gameId string | null
events.markets.groupItemRange string | null events.markets.sportsMarketType string | null
events.markets.line number | null events.markets.umaResolutionStatuses string | null
events.markets.pendingDeployment boolean | null events.markets.deploying boolean | null
events.markets.deployingTimestamp string | null
events.markets.scheduledDeploymentTimestamp
string <date-time> | null events.markets.rfqEnabled boolean | null events.markets.eventStartTime string
| null
events.series
object[]
Hide child attributes

events.series.id
string
events.series.ticker
string | null
events.series.slug
string | null
events.series.title
string | null
events.series.subtitle
string | null
events.series.seriesType
string | null
events.series.recurrence
string | null
events.series.description
string | null
events.series.image
string | null
events.series.icon
string | null
events.series.layout
string | null
events.series.active
boolean | null
events.series.closed
boolean | null
events.series.archived
boolean | null

events.series.new
boolean | null
events.series.featured
boolean | null
events.series.restricted
boolean | null
events.series.isTemplate
boolean | null
events.series.templateVariables
boolean | null
events.series.publishedAt
string | null
events.series.createdBy
string | null
events.series.updatedBy
string | null
events.series.createdAt
string <date-time> | null events.series.updatedAt string | null
events.series.commentsEnabled
boolean | null
events.series.competitive
string | null
events.series.volume24hr
number | null
events.series.volume
number | null
events.series.liquidity
number | null
events.series.startDate

string` | null
events.series.pythTokenID
string | null
events.series.cgAssetName
string | null
events.series.score
integer | null
events.series.events
array
events.series.collections
object[]
Hide child attributes
events.series.collections.id
string
events.series.collections.ticker
string | null
events.series.collections.slug
string | null
events.series.collections.title
string | null
events.series.collections.subtitle
string | null
events.series.collections.collectionType
string | null
events.series.collections.description
string | null
events.series.collections.tags
string | null
events.series.collections.image

string | null
events.series.collections.icon
string | null
events.series.collections.headerImage
string | null
events.series.collections.layout
string | null
events.series.collections.active
boolean | null
events.series.collections.closed
boolean | null
events.series.collections.archived
boolean | null
events.series.collections.new
boolean | null
events.series.collections.featured
boolean | null
events.series.collections.restricted
boolean | null
events.series.collections.isTemplate
boolean | null
events.series.collections.templateVariables
string | null
events.series.collections.publishedAt
string | null
events.series.collections.createdBy
string | null
events.series.collections.updatedBy
string | null

events.series.collections.createdAt
string <date-time> | null events.series.collections.updatedAt string | null
events.series.collections.commentsEnabled
boolean | null
events.series.collections.imageOptimized
object
Hide child attributes
events.series.collections.imageOptimized.id
string
events.series.collections.imageOptimized.imageUrlSource
string | null
events.series.collections.imageOptimized.imageUrlOptimized
string | null
events.series.collections.imageOptimized.imageSizeKbSource
number | null
events.series.collections.imageOptimized.imageSizeKbOptimized
number | null
events.series.collections.imageOptimized.imageOptimizedComplete
boolean | null
events.series.collections.imageOptimized.imageOptimizedLastUpdated
string | null
events.series.collections.imageOptimized.relID
integer | null
events.series.collections.imageOptimized.field
string | null
events.series.collections.imageOptimized.relname
string | null
events.series.collections.iconOptimized

object
Hide child attributes
events.series.collections.iconOptimized.id
string
events.series.collections.iconOptimized.imageUrlSource
string | null
events.series.collections.iconOptimized.imageUrlOptimized
string | null
events.series.collections.iconOptimized.imageSizeKbSource
number | null
events.series.collections.iconOptimized.imageSizeKbOptimized
number | null
events.series.collections.iconOptimized.imageOptimizedComplete
boolean | null
events.series.collections.iconOptimized.imageOptimizedLastUpdated
string | null
events.series.collections.iconOptimized.relID
integer | null
events.series.collections.iconOptimized.field
string | null
events.series.collections.iconOptimized.relname
string | null
events.series.collections.headerImageOptimized
object
Hide child attributes
events.series.collections.headerImageOptimized.id
string
events.series.collections.headerImageOptimized.imageUrlSource
string | null

events.series.collections.headerImageOptimized.imageUrlOptimized
string | null
events.series.collections.headerImageOptimized.imageSizeKbSource
number | null
events.series.collections.headerImageOptimized.imageSizeKbOptimized
number | null
events.series.collections.headerImageOptimized.imageOptimizedComplete
boolean | null
events.series.collections.headerImageOptimized.imageOptimizedLastUpdated
string | null
events.series.collections.headerImageOptimized.relID
integer | null
events.series.collections.headerImageOptimized.field
string | null
events.series.collections.headerImageOptimized.relname
string | null
events.series.categories
object[]
Hide child attributes
events.series.categories.id
string
events.series.categories.label
string | null
events.series.categories.parentCategory
string | null
events.series.categories.slug
string | null
events.series.categories.publishedAt
string | null

events.series.categories.createdBy
string | null
events.series.categories.updatedBy
string | null
events.series.categories.createdAt
string <date-time> | null events.series.categories.updatedAt string | null
events.series.tags
object[]
Hide child attributes
events.series.tags.id
string
events.series.tags.label
string | null
events.series.tags.slug
string | null
events.series.tags.forceShow
boolean | null
events.series.tags.publishedAt
string | null
events.series.tags.createdBy
integer | null
events.series.tags.updatedBy
integer | null
events.series.tags.createdAt
string <date-time> | null events.series.tags.updatedAt string | null
events.series.tags.forceHide
boolean | null
events.series.tags.isCarousel
boolean | null

events.series.commentCount
integer | null
events.series.chats
object[]
Hide child attributes
events.series.chats.id
string
events.series.chats.channelId
string | null
events.series.chats.channelName
string | null
events.series.chats.channelImage
string | null
events.series.chats.live
boolean | null
events.series.chats.startTime
string <date-time> | null events.series.chats.endTime string | null
events.categories
object[]
Hide child attributes
events.categories.id
string
events.categories.label
string | null
events.categories.parentCategory
string | null
events.categories.slug
string | null

events.categories.publishedAt
string | null
events.categories.createdBy
string | null
events.categories.updatedBy
string | null
events.categories.createdAt
string <date-time> | null events.categories.updatedAt string | null
events.collections
object[]
Hide child attributes
events.collections.id
string
events.collections.ticker
string | null
events.collections.slug
string | null
events.collections.title
string | null
events.collections.subtitle
string | null
events.collections.collectionType
string | null
events.collections.description
string | null
events.collections.tags
string | null
events.collections.image
string | null

events.collections.icon
string | null
events.collections.headerImage
string | null
events.collections.layout
string | null
events.collections.active
boolean | null
events.collections.closed
boolean | null
events.collections.archived
boolean | null
events.collections.new
boolean | null
events.collections.featured
boolean | null
events.collections.restricted
boolean | null
events.collections.isTemplate
boolean | null
events.collections.templateVariables
string | null
events.collections.publishedAt
string | null
events.collections.createdBy
string | null
events.collections.updatedBy
string | null
events.collections.createdAt

string <date-time> | null events.collections.updatedAt string | null
events.collections.commentsEnabled
boolean | null
events.collections.imageOptimized
object
Hide child attributes
events.collections.imageOptimized.id
string
events.collections.imageOptimized.imageUrlSource
string | null
events.collections.imageOptimized.imageUrlOptimized
string | null
events.collections.imageOptimized.imageSizeKbSource
number | null
events.collections.imageOptimized.imageSizeKbOptimized
number | null
events.collections.imageOptimized.imageOptimizedComplete
boolean | null
events.collections.imageOptimized.imageOptimizedLastUpdated
string | null
events.collections.imageOptimized.relID
integer | null
events.collections.imageOptimized.field
string | null
events.collections.imageOptimized.relname
string | null
events.collections.iconOptimized
object
Hide child attributes

events.collections.iconOptimized.id
string
events.collections.iconOptimized.imageUrlSource
string | null
events.collections.iconOptimized.imageUrlOptimized
string | null
events.collections.iconOptimized.imageSizeKbSource
number | null
events.collections.iconOptimized.imageSizeKbOptimized
number | null
events.collections.iconOptimized.imageOptimizedComplete
boolean | null
events.collections.iconOptimized.imageOptimizedLastUpdated
string | null
events.collections.iconOptimized.relID
integer | null
events.collections.iconOptimized.field
string | null
events.collections.iconOptimized.relname
string | null
events.collections.headerImageOptimized
object
Hide child attributes
events.collections.headerImageOptimized.id
string
events.collections.headerImageOptimized.imageUrlSource
string | null
events.collections.headerImageOptimized.imageUrlOptimized
string | null

events.collections.headerImageOptimized.imageSizeKbSource
number | null
events.collections.headerImageOptimized.imageSizeKbOptimized
number | null
events.collections.headerImageOptimized.imageOptimizedComplete
boolean | null
events.collections.headerImageOptimized.imageOptimizedLastUpdated
string | null
events.collections.headerImageOptimized.relID
integer | null
events.collections.headerImageOptimized.field
string | null
events.collections.headerImageOptimized.relname
string | null
events.tags
object[]
Hide child attributes
events.tags.id
string
events.tags.label
string | null
events.tags.slug
string | null
events.tags.forceShow
boolean | null
events.tags.publishedAt
string | null
events.tags.createdBy
integer | null

events.tags.updatedBy
integer | null
events.tags.createdAt
string <date-time> | null events.tags.updatedAt string | null
events.tags.forceHide
boolean | null
events.tags.isCarousel
boolean | null
events.cyom
boolean | null
events.closedTime
string <date-time> | null events.showAllOutcomes boolean | null events.showMarketImages boolean |
null events.automaticallyResolved boolean | null events.enableNegRisk boolean | null
events.automaticallyActive boolean | null events.eventDate string | null events.startTime string | null
events.eventWeek
integer | null
events.seriesSlug
string | null
events.score
string | null
events.elapsed
string | null
events.period
string | null
events.live
boolean | null
events.ended
boolean | null
events.finishedTimestamp

string` | null
events.gmpChartMode
string | null
events.eventCreators
object[]
Hide child attributes
events.eventCreators.id
string
events.eventCreators.creatorName
string | null
events.eventCreators.creatorHandle
string | null
events.eventCreators.creatorUrl
string | null
events.eventCreators.creatorImage
string | null
events.eventCreators.createdAt
string <date-time> | null events.eventCreators.updatedAt string | null
events.tweetCount
integer | null
events.chats
object[]
Hide child attributes
events.chats.id
string
events.chats.channelId
string | null
events.chats.channelName
string | null

events.chats.channelImage
string | null
events.chats.live
boolean | null
events.chats.startTime
string <date-time> | null events.chats.endTime string | null
events.featuredOrder
integer | null
events.estimateValue
boolean | null
events.cantEstimate
boolean | null
events.estimatedValue
string | null
events.templates
object[]
Hide child attributes
events.templates.id
string
events.templates.eventTitle
string | null
events.templates.eventSlug
string | null
events.templates.eventImage
string | null
events.templates.marketTitle
string | null
events.templates.description
string | null

events.templates.resolutionSource
string | null
events.templates.negRisk
boolean | null
events.templates.sortBy
string | null
events.templates.showMarketImages
boolean | null
events.templates.seriesSlug
string | null
events.templates.outcomes
string | null
events.spreadsMainLine
number | null
events.totalsMainLine
number | null
events.carouselMap
string | null
events.pendingDeployment
boolean | null
events.deploying
boolean | null
events.deployingTimestamp
string <date-time> | null events.scheduledDeploymentTimestamp string | null
events.gameStatus
string | null
tags
object[] | null
Hide child attributes

tags.id
string
tags.label
string
tags.slug
string
tags.event_count
integer
profiles
object[] | null
Hide child attributes
profiles.id
string
profiles.name
string | null
profiles.user
integer | null
profiles.referral
string | null
profiles.createdBy
integer | null
profiles.updatedBy
integer | null
profiles.createdAt
string <date-time> | null profiles.updatedAt string | null
profiles.utmSource
string | null
profiles.utmMedium
string | null

profiles.utmCampaign
string | null
profiles.utmContent
string | null
profiles.utmTerm
string | null
profiles.walletActivated
boolean | null
profiles.pseudonym
string | null
profiles.displayUsernamePublic
boolean | null
profiles.profileImage
string | null
profiles.bio
string | null
profiles.proxyWallet
string | null
profiles.profileImageOptimized
object
Hide child attributes
profiles.profileImageOptimized.id
string
profiles.profileImageOptimized.imageUrlSource
string | null
profiles.profileImageOptimized.imageUrlOptimized
string | null
profiles.profileImageOptimized.imageSizeKbSource
number | null

profiles.profileImageOptimized.imageSizeKbOptimized
number | null
profiles.profileImageOptimized.imageOptimizedComplete
boolean | null
profiles.profileImageOptimized.imageOptimizedLastUpdated
string | null
profiles.profileImageOptimized.relID
integer | null
profiles.profileImageOptimized.field
string | null
profiles.profileImageOptimized.relname
string | null
profiles.isCloseOnly
boolean | null
profiles.isCertReq
boolean | null
profiles.certReqDate
string` | null
pagination
object
Hide child attributes
pagination.hasMore
boolean
pagination.totalResults
integer
Data-API
Data API Status

Data API Health check
GET
Data API Health check
```bash
cURL
curl --request GET \
--url https://data-api.polymarket.com/
Python
import requests
url = "https://data-api.polymarket.com/"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://data-api.polymarket.com/', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://data-api.polymarket.com/",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);

if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://data-api.polymarket.com/"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://data-api.polymarket.com/")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://data-api.polymarket.com/")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
200
{
"data": "OK"
}
Response
200 - application/json
OK
data
string

### Example

"OK"
Core
Get current positions for a user
Returns positions filtered by user and optional filters.
GET/positions
Get current positions for a user
```bash
cURL
curl --request GET \
--url 'https://data-api.polymarket.com/positions?
```
sizeThreshold=1&limit=100&sortBy=TOKENS&sortDirection=DESC'
Python
```python
import requests
url = "https://data-api.polymarket.com/positions?
```
sizeThreshold=1&limit=100&sortBy=TOKENS&sortDirection=DESC"
response = requests.get(url)
print(response.text)

JavaScript
const options = {method: 'GET'};
fetch('https://data-api.polymarket.com/positions?
sizeThreshold=1&limit=100&sortBy=TOKENS&sortDirection=DESC', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://data-api.polymarket.com/positions?
sizeThreshold=1&limit=100&sortBy=TOKENS&sortDirection=DESC",
```
```bash
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {

url := "https://data-api.polymarket.com/positions?
```
sizeThreshold=1&limit=100&sortBy=TOKENS&sortDirection=DESC"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://data-
api.polymarket.com/positions?
sizeThreshold=1&limit=100&sortBy=TOKENS&sortDirection=DESC")
.asString();
Ruby
require 'uri'
require 'net/http'
url = URI("https://data-api.polymarket.com/positions?
sizeThreshold=1&limit=100&sortBy=TOKENS&sortDirection=DESC")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"proxyWallet": "0x56687bf447db6ffa42ffe2204a05edaa20f55839",
"asset": "<string>",

### "conditionId"

"0xdd22472e552920b8438158ea7238bfadfa4f736aa4cee91a6b86c39ead110917",
"size": 123,
"avgPrice": 123,
"initialValue": 123,
"currentValue": 123,
"cashPnl": 123,

"percentPnl": 123,
"totalBought": 123,
"realizedPnl": 123,
"percentRealizedPnl": 123,
"curPrice": 123,
"redeemable": true,
"mergeable": true,
"title": "<string>",
"slug": "<string>",
"icon": "<string>",
"eventSlug": "<string>",
"outcome": "<string>",
"outcomeIndex": 123,
"oppositeOutcome": "<string>",
"oppositeAsset": "<string>",
"endDate": "<string>",
"negativeRisk": true
}
]
400
{
"error": "<string>"
}
401
{
"error": "<string>"
}
500
{
"error": "<string>"
}
Query Parameters
user
string
required
User address (required)
User Profile Address (0x-prefixed, 40 hex chars)

### Example

"0x56687bf447db6ffa42ffe2204a05edaa20f55839"

market
string[]
Comma-separated list of condition IDs. Mutually exclusive with eventId.
0x-prefixed 64-hex string
eventId
integer[]
Comma-separated list of event IDs. Mutually exclusive with market.
Required range: x >= 1
sizeThreshold
numberdefault:1
Required range: x >= 0
redeemable
booleandefault:false
mergeable
booleandefault:false
limit
integerdefault:100
Required range: 0 <= x <= 500
offset
integerdefault:0
Required range: 0 <= x <= 10000
sortBy
enum <string>default:TOKENS Available options: CURRENT, INITIAL, TOKENS, CASHPNL,
PERCENTPNL, TITLE, RESOLVING, PRICE, AVGPRICE sortDirection enum default:DESC
Available options: ASC, DESC
title
string
Maximum string length: 100
Response

200
application/json
Success
proxyWallet
string
User Profile Address (0x-prefixed, 40 hex chars)

### Example

"0x56687bf447db6ffa42ffe2204a05edaa20f55839"
asset
string
conditionId
string
0x-prefixed 64-hex string

### Example

"0xdd22472e552920b8438158ea7238bfadfa4f736aa4cee91a6b86c39ead110917"
size
number
avgPrice
number
initialValue
number
currentValue
number
cashPnl
number
percentPnl
number
totalBought
number

realizedPnl
number
percentRealizedPnl
number
curPrice
number
redeemable
boolean
mergeable
boolean
title
string
slug
string
icon
string
eventSlug
string
outcome
string
outcomeIndex
integer
oppositeOutcome
string
oppositeAsset
string
endDate
string

negativeRisk
boolean
Response
400
application/json
Bad Request
error
string
required
Response
401
application/json
Unauthorized
error
string
required
Response
500
application/json
Server Error
error
string
required
Get trades for a user or markets

GET/trades
Get trades for a user or markets
```bash
cURL
curl --request GET \
--url 'https://data-api.polymarket.com/trades?limit=100&takerOnly=true'
```
Python
```python
import requests
url = "https://data-api.polymarket.com/trades?limit=100&takerOnly=true"
```
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
fetch('https://data-api.polymarket.com/trades?limit=100&takerOnly=true', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://data-api.polymarket.com/trades?limit=100&takerOnly=true",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```

echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://data-api.polymarket.com/trades?limit=100&takerOnly=true"
```
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://data-api.polymarket.com/trades?
limit=100&takerOnly=true")
.asString();
Ruby
require 'uri'
require 'net/http'
url = URI("https://data-api.polymarket.com/trades?limit=100&takerOnly=true")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body

200
[
{
"proxyWallet": "0x56687bf447db6ffa42ffe2204a05edaa20f55839",
"side": "BUY",
"asset": "<string>",

### "conditionId"

"0xdd22472e552920b8438158ea7238bfadfa4f736aa4cee91a6b86c39ead110917",
"size": 123,
"price": 123,
"timestamp": 123,
"title": "<string>",
"slug": "<string>",
"icon": "<string>",
"eventSlug": "<string>",
"outcome": "<string>",
"outcomeIndex": 123,
"name": "<string>",
"pseudonym": "<string>",
"bio": "<string>",
"profileImage": "<string>",
"profileImageOptimized": "<string>",
"transactionHash": "<string>"
}
]
400
{
"error": "<string>"
}
401
{
"error": "<string>"
}
500
{
"error": "<string>"
}
Query Parameters
limit

integerdefault:100
Required range: 0 <= x <= 10000
offset
integerdefault:0
Required range: 0 <= x <= 10000
takerOnly
booleandefault:true
filterType
enum`
Must be provided together with filterAmount.
Available options: CASH, TOKENS
filterAmount
number
Must be provided together with filterType.
Required range: x >= 0
market
string[]
Comma-separated list of condition IDs. Mutually exclusive with eventId.
0x-prefixed 64-hex string
eventId
integer[]
Comma-separated list of event IDs. Mutually exclusive with market.
Required range: x >= 1
user
string
User Profile Address (0x-prefixed, 40 hex chars)

### Example

"0x56687bf447db6ffa42ffe2204a05edaa20f55839"
side
enum`
Available options: BUY, SELL

Response
200
application/json
Success
proxyWallet
string
User Profile Address (0x-prefixed, 40 hex chars)

### Example

"0x56687bf447db6ffa42ffe2204a05edaa20f55839"
side
enum`
Available options: BUY, SELL
asset
string
conditionId
string
0x-prefixed 64-hex string

### Example

"0xdd22472e552920b8438158ea7238bfadfa4f736aa4cee91a6b86c39ead110917"
size
number
price
number
timestamp
integer`
title
string
slug

string
icon
string
eventSlug
string
outcome
string
outcomeIndex
integer
name
string
pseudonym
string
bio
string
profileImage
string
profileImageOptimized
string
transactionHash
string
Get user activity
Returns on-chain activity for a user.
GET/activity
Get user activity
```bash
cURL

curl --request GET \
--url 'https://data-api.polymarket.com/activity?
```
limit=100&sortBy=TIMESTAMP&sortDirection=DESC'
Python
```python
import requests
url = "https://data-api.polymarket.com/activity?
```
limit=100&sortBy=TIMESTAMP&sortDirection=DESC"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
fetch('https://data-api.polymarket.com/activity?
limit=100&sortBy=TIMESTAMP&sortDirection=DESC', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://data-api.polymarket.com/activity?
limit=100&sortBy=TIMESTAMP&sortDirection=DESC",
```
```bash
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {

echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://data-api.polymarket.com/activity?
```
limit=100&sortBy=TIMESTAMP&sortDirection=DESC"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://data-api.polymarket.com/activity?
limit=100&sortBy=TIMESTAMP&sortDirection=DESC")
.asString();
Ruby
require 'uri'
require 'net/http'
url = URI("https://data-api.polymarket.com/activity?
limit=100&sortBy=TIMESTAMP&sortDirection=DESC")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body

200
[
{
"proxyWallet": "0x56687bf447db6ffa42ffe2204a05edaa20f55839",
"timestamp": 123,

### "conditionId"

"0xdd22472e552920b8438158ea7238bfadfa4f736aa4cee91a6b86c39ead110917",
"type": "TRADE",
"size": 123,
"usdcSize": 123,
"transactionHash": "<string>",
"price": 123,
"asset": "<string>",
"side": "BUY",
"outcomeIndex": 123,
"title": "<string>",
"slug": "<string>",
"icon": "<string>",
"eventSlug": "<string>",
"outcome": "<string>",
"name": "<string>",
"pseudonym": "<string>",
"bio": "<string>",
"profileImage": "<string>",
"profileImageOptimized": "<string>"
}
]
400
{
"error": "<string>"
}
401
{
"error": "<string>"
}
500
{
"error": "<string>"
}
Query Parameters

limit
integerdefault:100
Required range: 0 <= x <= 500
offset
integerdefault:0
Required range: 0 <= x <= 10000
user
stringrequired
User Profile Address (0x-prefixed, 40 hex chars)

### Example

"0x56687bf447db6ffa42ffe2204a05edaa20f55839"
market
string[]
Comma-separated list of condition IDs. Mutually exclusive with eventId.
0x-prefixed 64-hex string
eventId
integer[]
Comma-separated list of event IDs. Mutually exclusive with market.
Required range: x >= 1
type
enum <string>[] Available options: TRADE, SPLIT, MERGE, REDEEM, REWARD, CONVERSION,
MAKER_REBATE start integer Required range: x >= 0 end integer Required range: x >= 0 sortBy
enum default:TIMESTAMP
Available options: TIMESTAMP, TOKENS, CASH
sortDirection
enum <string>default:DESC Available options: ASC, DESC side enum
Available options: BUY, SELL
Response
200

application/json
Success
proxyWallet
string
User Profile Address (0x-prefixed, 40 hex chars)

### Example

"0x56687bf447db6ffa42ffe2204a05edaa20f55839"
timestamp
integer`
conditionId
string
0x-prefixed 64-hex string

### Example

"0xdd22472e552920b8438158ea7238bfadfa4f736aa4cee91a6b86c39ead110917"
type
enum <string> Available options: TRADE, SPLIT, MERGE, REDEEM, REWARD, CONVERSION,
MAKER_REBATE size number usdcSize number transactionHash string price number asset string
side enum
Available options: BUY, SELL
outcomeIndex
integer
title
string
slug
string
icon
string
eventSlug
string
outcome

string
name
string
pseudonym
string
bio
string
profileImage
string
profileImageOptimized
string
Response
400
application/json
Bad Request
error
string
required
Response
401
application/json
Unauthorized
error
string
required

Response
500
application/json
Server Error
error
string
required
Get top holders for markets
GET/holdersTry it
Get top holders for markets
```bash
cURL
curl --request GET \
--url 'https://data-api.polymarket.com/holders?limit=20&minBalance=1'
```
Python
```python
import requests
url = "https://data-api.polymarket.com/holders?limit=20&minBalance=1"
```
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
fetch('https://data-api.polymarket.com/holders?limit=20&minBalance=1', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();

```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://data-api.polymarket.com/holders?limit=20&minBalance=1",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://data-api.polymarket.com/holders?limit=20&minBalance=1"
```
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://data-api.polymarket.com/holders?
limit=20&minBalance=1")

.asString();
Ruby
require 'uri'
require 'net/http'
url = URI("https://data-api.polymarket.com/holders?limit=20&minBalance=1")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"token": "<string>",
"holders": [
{
"proxyWallet": "0x56687bf447db6ffa42ffe2204a05edaa20f55839",
"bio": "<string>",
"asset": "<string>",
"pseudonym": "<string>",
"amount": 123,
"displayUsernamePublic": true,
"outcomeIndex": 123,
"name": "<string>",
"profileImage": "<string>",
"profileImageOptimized": "<string>"
}
]
}
]
400
{
"error": "<string>"
}
401
{
"error": "<string>"

}
500
{
"error": "<string>"
}
Query Parameters
limit
integerdefault:20
Maximum number of holders to return per token. Capped at 20.
Required range: 0 <= x <= 20
market
string[]required
Comma-separated list of condition IDs.
0x-prefixed 64-hex string
minBalance
integerdefault:1
Required range: 0 <= x <= 999999
Response
200
application/json
Success
token
string
holders
object[]
Hide child attributes
holders.proxyWallet

string
User Profile Address (0x-prefixed, 40 hex chars)

### Example

"0x56687bf447db6ffa42ffe2204a05edaa20f55839"
holders.bio
string
holders.asset
string
holders.pseudonym
string
holders.amount
number
holders.displayUsernamePublic
boolean
holders.outcomeIndex
integer
holders.name
string
holders.profileImage
string
holders.profileImageOptimized
string
Response
400
application/json
Bad Request
error

string
required
Response
401
application/json
Unauthorized
error
string
required
Response
500
application/json
Server Error
error
string
required
Get total value of a user's positions
GET/value
Get total value of a user's positions
```bash
cURL
curl --request GET \
--url https://data-api.polymarket.com/value
Python
import requests

url = "https://data-api.polymarket.com/value"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://data-api.polymarket.com/value', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://data-api.polymarket.com/value",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"

)
func main() {
url := "https://data-api.polymarket.com/value"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://data-api.polymarket.com/value")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://data-api.polymarket.com/value")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"user": "0x56687bf447db6ffa42ffe2204a05edaa20f55839",
"value": 123
}
]
400
{
"error": "<string>"

}
500
{
"error": "<string>"
}
Query Parameters
user
string
required
User Profile Address (0x-prefixed, 40 hex chars)

### Example

"0x56687bf447db6ffa42ffe2204a05edaa20f55839"
market
string[]
0x-prefixed 64-hex string
Response
200
application/json
Success
user
string
User Profile Address (0x-prefixed, 40 hex chars)

### Example

"0x56687bf447db6ffa42ffe2204a05edaa20f55839"
value
number

Response
400
application/json
Bad Request
error
string
required
Response
500
application/json
Server Error
error
string
required
Get closed positions for a user
Fetches closed positions for a user(address)
GET/v1/closed-positions
Get closed positions for a user
```bash
cURL
curl --request GET \
--url 'https://data-api.polymarket.com/v1/closed-positions?
```
limit=10&sortBy=REALIZEDPNL&sortDirection=DESC'
Python
```python
import requests
url = "https://data-api.polymarket.com/v1/closed-positions?
```
limit=10&sortBy=REALIZEDPNL&sortDirection=DESC"

response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
fetch('https://data-api.polymarket.com/v1/closed-positions?
limit=10&sortBy=REALIZEDPNL&sortDirection=DESC', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://data-api.polymarket.com/v1/closed-positions?
limit=10&sortBy=REALIZEDPNL&sortDirection=DESC",
```
```bash
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"

)
func main() {
url := "https://data-api.polymarket.com/v1/closed-positions?
```
limit=10&sortBy=REALIZEDPNL&sortDirection=DESC"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://data-
api.polymarket.com/v1/closed-positions?
limit=10&sortBy=REALIZEDPNL&sortDirection=DESC")
.asString();
Ruby
require 'uri'
require 'net/http'
url = URI("https://data-api.polymarket.com/v1/closed-positions?
limit=10&sortBy=REALIZEDPNL&sortDirection=DESC")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"proxyWallet": "0x56687bf447db6ffa42ffe2204a05edaa20f55839",
"asset": "<string>",

### "conditionId"

"0xdd22472e552920b8438158ea7238bfadfa4f736aa4cee91a6b86c39ead110917",
"avgPrice": 123,

"totalBought": 123,
"realizedPnl": 123,
"curPrice": 123,
"timestamp": 123,
"title": "<string>",
"slug": "<string>",
"icon": "<string>",
"eventSlug": "<string>",
"outcome": "<string>",
"outcomeIndex": 123,
"oppositeOutcome": "<string>",
"oppositeAsset": "<string>",
"endDate": "<string>"
}
]
400
{
"error": "<string>"
}
401
{
"error": "<string>"
}
500
{
"error": "<string>"
}
Query Parameters
user
string
required
The address of the user in question
User Profile Address (0x-prefixed, 40 hex chars)

### Example

"0x56687bf447db6ffa42ffe2204a05edaa20f55839"
market

string[]
The conditionId of the market in question. Supports multiple csv separated values. Cannot
be used with the eventId param.
0x-prefixed 64-hex string
title
string
Filter by market title
Maximum string length: 100
eventId
integer[]
The event id of the event in question. Supports multiple csv separated values. Returns
positions for all markets for those event ids. Cannot be used with the market param.
Required range: x >= 1
limit
integerdefault:10
The max number of positions to return
Required range: 0 <= x <= 50
offset
integerdefault:0
The starting index for pagination
Required range: 0 <= x <= 100000
sortBy
enum`default:REALIZEDPNL
The sort criteria
Available options: REALIZEDPNL, TITLE, PRICE, AVGPRICE, TIMESTAMP
sortDirection
enum`default:DESC
The sort direction
Available options: ASC, DESC
Response

200
application/json
Success
proxyWallet
string
User Profile Address (0x-prefixed, 40 hex chars)

### Example

"0x56687bf447db6ffa42ffe2204a05edaa20f55839"
asset
string
conditionId
string
0x-prefixed 64-hex string

### Example

"0xdd22472e552920b8438158ea7238bfadfa4f736aa4cee91a6b86c39ead110917"
avgPrice
number
totalBought
number
realizedPnl
number
curPrice
number
timestamp
integer`
title
string
slug
string

icon
string
eventSlug
string
outcome
string
outcomeIndex
integer
oppositeOutcome
string
oppositeAsset
string
endDate
string
Response
400
application/json
Bad Request
error
string
required
Response
401
application/json
Unauthorized
error

string
required
Response
500
application/json
Server Error
error
string
required
Get trader leaderboard rankings
Returns trader leaderboard rankings filtered by category, time period, and ordering.
GET/v1/leaderboard
Get trader leaderboard rankings
```bash
cURL
curl --request GET \
--url 'https://data-api.polymarket.com/v1/leaderboard?
```
category=OVERALL&timePeriod=DAY&orderBy=PNL&limit=25'
Python
```python
import requests
url = "https://data-api.polymarket.com/v1/leaderboard?
```
category=OVERALL&timePeriod=DAY&orderBy=PNL&limit=25"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
fetch('https://data-api.polymarket.com/v1/leaderboard?

category=OVERALL&timePeriod=DAY&orderBy=PNL&limit=25', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://data-api.polymarket.com/v1/leaderboard?
category=OVERALL&timePeriod=DAY&orderBy=PNL&limit=25",
```
```bash
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://data-api.polymarket.com/v1/leaderboard?
```
category=OVERALL&timePeriod=DAY&orderBy=PNL&limit=25"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)

defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://data-
api.polymarket.com/v1/leaderboard?
category=OVERALL&timePeriod=DAY&orderBy=PNL&limit=25")
.asString();
Ruby
require 'uri'
require 'net/http'
url = URI("https://data-api.polymarket.com/v1/leaderboard?
category=OVERALL&timePeriod=DAY&orderBy=PNL&limit=25")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"rank": "<string>",
"proxyWallet": "0x56687bf447db6ffa42ffe2204a05edaa20f55839",
"userName": "<string>",
"vol": 123,
"pnl": 123,
"profileImage": "<string>",
"xUsername": "<string>",
"verifiedBadge": true
}
]
400
{
"error": "<string>"

}
500
{
"error": "<string>"
}
Query Parameters
category
enum`default:OVERALL
Market category for the leaderboard
Available options: OVERALL, POLITICS, SPORTS, CRYPTO, CULTURE, MENTIONS,

## Weather, Economics, Tech, Finance

timePeriod
enum`default:DAY
Time period for leaderboard results
Available options: DAY, WEEK, MONTH, ALL
orderBy
enum`default:PNL
Leaderboard ordering criteria
Available options: PNL, VOL
limit
integerdefault:25
Max number of leaderboard traders to return
Required range: 1 <= x <= 50
offset
integerdefault:0
Starting index for pagination
Required range: 0 <= x <= 1000
user
string
Limit leaderboard to a single user by address
User Profile Address (0x-prefixed, 40 hex chars)


### Example

"0x56687bf447db6ffa42ffe2204a05edaa20f55839"
userName
string
Limit leaderboard to a single username
Response
200
application/json
Success
rank
string
The rank position of the trader
proxyWallet
string
User Profile Address (0x-prefixed, 40 hex chars)

### Example

"0x56687bf447db6ffa42ffe2204a05edaa20f55839"
userName
string
The trader's username
vol
number
Trading volume for this trader
pnl
number
Profit and loss for this trader
profileImage

string
URL to the trader's profile image
xUsername
string
The trader's X (Twitter) username
verifiedBadge
boolean
Whether the trader has a verified badge
Response
400
application/json
Bad Request
error
string
required
Response
500
application/json
Server Error
error
string
required
Misc
Get total markets a user has traded
GET/traded

Get total markets a user has traded
```bash
cURL
curl --request GET \
--url https://data-api.polymarket.com/traded
Python
import requests
url = "https://data-api.polymarket.com/traded"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://data-api.polymarket.com/traded', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://data-api.polymarket.com/traded",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {

echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://data-api.polymarket.com/traded"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://data-api.polymarket.com/traded")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://data-api.polymarket.com/traded")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200

{
"user": "0x56687bf447db6ffa42ffe2204a05edaa20f55839",
"traded": 123
}
400
{
"error": "<string>"
}
401
{
"error": "<string>"
}
500
{
"error": "<string>"
}
Query Parameters
user
string
required
User Profile Address (0x-prefixed, 40 hex chars)

### Example

"0x56687bf447db6ffa42ffe2204a05edaa20f55839"
Response
200
application/json
Success
user
string
User Profile Address (0x-prefixed, 40 hex chars)


### Example

"0x56687bf447db6ffa42ffe2204a05edaa20f55839"
traded
integer
Response
400
application/json
Bad Request
error
string
required
Response
401
application/json
Unauthorized
error
string
required
Response
500
application/json
Server Error
error
string
required

Get open interest
GET/oi
Get open interest
```bash
cURL
curl --request GET \
--url https://data-api.polymarket.com/oi
Python
import requests
url = "https://data-api.polymarket.com/oi"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://data-api.polymarket.com/oi', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://data-api.polymarket.com/oi",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);

```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://data-api.polymarket.com/oi"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://data-api.polymarket.com/oi")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://data-api.polymarket.com/oi")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
200
[
{
"market": "0xdd22472e552920b8438158ea7238bfadfa4f736aa4cee91a6b86c39ead110917",
"value": 123
}
]
400
{
"error": "<string>"
}
500
{
"error": "<string>"
}
Query Parameters
market
string[]
0x-prefixed 64-hex string
Response
200
application/json
Success
market
string
0x-prefixed 64-hex string

### Example

"0xdd22472e552920b8438158ea7238bfadfa4f736aa4cee91a6b86c39ead110917"

value
number
Response
400
application/json
Bad Request
error
string
required
Response
500
application/json
Server Error
error
string
required
Get live volume for an event
GET/live-volume
Get live volume for an event
```bash
cURL
curl --request GET \
--url https://data-api.polymarket.com/live-volume
Python

import requests
url = "https://data-api.polymarket.com/live-volume"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://data-api.polymarket.com/live-volume', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://data-api.polymarket.com/live-volume",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"

"net/http"
"io"
)
func main() {
url := "https://data-api.polymarket.com/live-volume"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://data-api.polymarket.com/live-
volume")
.asString();
```
Ruby
require 'uri'
require 'net/http'
url = URI("https://data-api.polymarket.com/live-volume")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"total": 123,
"markets": [
{

### "market"

"0xdd22472e552920b8438158ea7238bfadfa4f736aa4cee91a6b86c39ead110917",
"value": 123

}
]
}
]
400
{
"error": "<string>"
}
500
{
"error": "<string>"
}
Query Parameters
id
integerrequired
Required range: x >= 1
Response
200
application/json
Success
total
number
markets
object[]
Hide child attributes
markets.market
string
0x-prefixed 64-hex string


### Example

"0xdd22472e552920b8438158ea7238bfadfa4f736aa4cee91a6b86c39ead110917"
markets.value
number
Response
400
application/json
Bad Request
error
string
required
Response
500
application/json
Server Error
error
string
required
Builders
Get aggregated builder leaderboard
Returns aggregated builder rankings with one entry per builder showing total for the
specified time period. Supports pagination.
GET/v1/builders/leaderboard
Get aggregated builder leaderboard

```bash
cURL
curl --request GET \
--url 'https://data-api.polymarket.com/v1/builders/leaderboard?
```
timePeriod=DAY&limit=25'
Python
```python
import requests
url = "https://data-api.polymarket.com/v1/builders/leaderboard?
```
timePeriod=DAY&limit=25"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
fetch('https://data-api.polymarket.com/v1/builders/leaderboard?
timePeriod=DAY&limit=25', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://data-api.polymarket.com/v1/builders/leaderboard?
timePeriod=DAY&limit=25",
```
```bash
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```

echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://data-api.polymarket.com/v1/builders/leaderboard?
```
timePeriod=DAY&limit=25"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://data-
api.polymarket.com/v1/builders/leaderboard?timePeriod=DAY&limit=25")
.asString();
Ruby
require 'uri'
require 'net/http'
url = URI("https://data-api.polymarket.com/v1/builders/leaderboard?
timePeriod=DAY&limit=25")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
200
[
{
"rank": "<string>",
"builder": "<string>",
"volume": 123,
"activeUsers": 123,
"verified": true,
"builderLogo": "<string>"
}
]
400
{
"error": "<string>"
}
500
{
"error": "<string>"
}
Query Parameters
timePeriod
enum`default:DAY
The time period to aggregate results over.
Available options: DAY, WEEK, MONTH, ALL
limit
integerdefault:25
Maximum number of builders to return
Required range: 0 <= x <= 50
offset
integerdefault:0
Starting index for pagination
Required range: 0 <= x <= 1000

Response
200
application/json
Success
rank
string
The rank position of the builder
builder
string
The builder name or identifier
volume
number
Total trading volume attributed to this builder
activeUsers
integer
Number of active users for this builder
verified
boolean
Whether the builder is verified
builderLogo
string
URL to the builder's logo image
Response
400
application/json
Bad Request

error
string
required
Response
500
application/json
Server Error
error
string
required
Get daily builder volume time-series
Returns daily time-series volume data with multiple entries per builder (one per day), each
including a dt timestamp. No pagination.
GET/v1/builders/volume
Get daily builder volume time-series
```bash
cURL
curl --request GET \
--url 'https://data-api.polymarket.com/v1/builders/volume?timePeriod=DAY'
```
Python
```python
import requests
url = "https://data-api.polymarket.com/v1/builders/volume?timePeriod=DAY"
```
response = requests.get(url)
print(response.text)
JavaScript

const options = {method: 'GET'};
fetch('https://data-api.polymarket.com/v1/builders/volume?timePeriod=DAY', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://data-api.polymarket.com/v1/builders/volume?timePeriod=DAY",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://data-api.polymarket.com/v1/builders/volume?timePeriod=DAY"
```
req, _ := http.NewRequest("GET", url, nil)

res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://data-
api.polymarket.com/v1/builders/volume?timePeriod=DAY")
.asString();
Ruby
require 'uri'
require 'net/http'
url = URI("https://data-api.polymarket.com/v1/builders/volume?timePeriod=DAY")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
[
{
"dt": "2025-11-15T00:00:00Z",
"builder": "<string>",
"builderLogo": "<string>",
"verified": true,
"volume": 123,
"activeUsers": 123,
"rank": "<string>"
}
]
400
{
"error": "<string>"
}

500
{
"error": "<string>"
}
Query Parameters
timePeriod
enum`default:DAY
The time period to fetch daily records for.
Available options: DAY, WEEK, MONTH, ALL
Response
200
application/json
Success - Returns array of daily volume records
dt
string`
The timestamp for this volume entry in ISO 8601 format

### Example


## "2025-11-15T00:00:00Z"

builder
string
The builder name or identifier
builderLogo
string
URL to the builder's logo image
verified
boolean
Whether the builder is verified

volume
number
Trading volume for this builder on this date
activeUsers
integer
Number of active users for this builder on this date
rank
string
The rank position of the builder on this date
Response
400
application/json
Bad Request
error
string
required
Response
500
application/json
Server Error
error
string
required
Bridge & Swap

Overview
Bridge and swap assets to Polymarket
Overview
The Polymarket Bridge API enables seamless deposits between multiple blockchains and
Polymarket.
USDC.e on Polygon
Polymarket uses USDC.e (Bridged USDC) on Polygon as collateral for all trading
activities. USDC.e is the bridged version of USDC from Ethereum, and it serves as the
native currency for placing orders and settling trades on Polymarket.When you deposit

### assets to Polymarket

1. You can deposit from various supported chains (Ethereum, Solana, Arbitrum, Base, etc.)
2. Your assets are automatically bridged/swapped to USDC.e on Polygon
3. USDC.e is credited to your Polymarket wallet
4. You can now trade on any Polymarket market
Base URL
https://bridge.polymarket.com
Key Features
Multi-chain deposits: Bridge assets from EVM chains (Ethereum, Arbitrum, Base, etc.),
Solana, and Bitcoin
Automatic conversion: Assets are automatically bridged/swapped to USDC.e on
Polygon
Simple addressing: One deposit address per blockchain type (EVM, SVM, BTC)
Endpoints
POST /deposit - Create unique deposit addresses for bridging assets
GET /supported-assets - Get all supported chains and tokens
Create deposit addresses
Generate unique deposit addresses for bridging assets to Polymarket.

### How it works

1. Request deposit addresses for your Polymarket wallet
2. Receive deposit addresses for each blockchain type (EVM, Solana, Bitcoin)

3. Send assets to the appropriate deposit address for your source chain
4. Assets are automatically bridged and swapped to USDC.e on Polygon
5. USDC.e is credited to your Polymarket wallet for trading
POST/deposit
Create deposit addresses
```bash
cURL
curl --request POST \
--url https://bridge.polymarket.com/deposit \
```
--header 'Content-Type: application/json' \
--data '
{
"address": "0x56687bf447db6ffa42ffe2204a05edaa20f55839"
}
'
Python
```python
import requests
url = "https://bridge.polymarket.com/deposit"
payload = { "address": "0x56687bf447db6ffa42ffe2204a05edaa20f55839" }
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=payload, headers=headers)
print(response.text)
JavaScript
const options = {
method: 'POST',
```
headers: {'Content-Type': 'application/json'},
body: JSON.stringify({address: '0x56687bf447db6ffa42ffe2204a05edaa20f55839'})
};
fetch('https://bridge.polymarket.com/deposit', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php

$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://bridge.polymarket.com/deposit",
CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "POST",
CURLOPT_POSTFIELDS => json_encode([
'address' => '0x56687bf447db6ffa42ffe2204a05edaa20f55839'
```
]),
```bash
CURLOPT_HTTPHEADER => [
"Content-Type: application/json"
],
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"strings"
"net/http"
"io"
)
func main() {
url := "https://bridge.polymarket.com/deposit"
payload := strings.NewReader("{\n \"address\":
```
\"0x56687bf447db6ffa42ffe2204a05edaa20f55839\"\n}")
req, _ := http.NewRequest("POST", url, payload)
req.Header.Add("Content-Type", "application/json")
res, _ := http.DefaultClient.Do(req)

defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.post("https://bridge.polymarket.com/deposit")
.header("Content-Type", "application/json")
.body("{\n \"address\": \"0x56687bf447db6ffa42ffe2204a05edaa20f55839\"\n}")
.asString();
Ruby
require 'uri'
require 'net/http'
url = URI("https://bridge.polymarket.com/deposit")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Post.new(url)
request["Content-Type"] = 'application/json'
request.body = "{\n \"address\": \"0x56687bf447db6ffa42ffe2204a05edaa20f55839\"\n}"
response = http.request(request)
puts response.read_body
201
{
"address": {
"evm": "0x23566f8b2E82aDfCf01846E54899d110e97AC053",
"svm": "CrvTBvzryYxBHbWu2TiQpcqD5M7Le7iBKzVmEj3f36Jb",
"btc": "bc1q8eau83qffxcj8ht4hsjdza3lha9r3egfqysj3g"
},
"note": "Only certain chains and tokens are supported. See /supported-assets for
details."
}
400
{
"error": "<string>"
}

500
{
"error": "<string>"
}
Body
application/json
address
string
required
Your Polymarket wallet address

### Example

"0x56687bf447db6ffa42ffe2204a05edaa20f55839"
Response
201
application/json
Deposit addresses created successfully
address
object
Deposit addresses for different blockchain networks
Hide child attributes
address.evm
string
EVM-compatible deposit address (Ethereum, Polygon, Arbitrum, Base, etc.)

### Example

"0x23566f8b2E82aDfCf01846E54899d110e97AC053"
address.svm
string
Solana Virtual Machine deposit address


### Example

"CrvTBvzryYxBHbWu2TiQpcqD5M7Le7iBKzVmEj3f36Jb"
address.btc
string
Bitcoin deposit address

### Example

"bc1q8eau83qffxcj8ht4hsjdza3lha9r3egfqysj3g"
note
string
Additional information about supported chains

### Example

"Only certain chains and tokens are supported. See /supported-assets for details."
Response
400
application/json
Bad Request - Invalid address or request body
error
string
required
Response
500
application/json
Server Error
error
string
required

Get supported assets
Retrieve all supported chains and tokens for deposits.
USDC.e on Polygon: Polymarket uses USDC.e (Bridged USDC from Ethereum) on Polygon
as the native collateral for all markets. When you deposit assets from other chains, they are
automatically bridged and swapped to USDC.e on Polygon, which is then used as collateral
for trading on Polymarket.
Minimum Deposit Amounts: Each asset has a minCheckoutUsd field indicating the
minimum deposit amount required in USD. Make sure your deposit meets this minimum to
avoid transaction failures.
GET/supported-assets
Get supported assets
```bash
cURL
curl --request GET \
--url https://bridge.polymarket.com/supported-assets
Python
import requests
url = "https://bridge.polymarket.com/supported-assets"
response = requests.get(url)
print(response.text)
JavaScript
const options = {method: 'GET'};
```
fetch('https://bridge.polymarket.com/supported-assets', options)
.then(res => res.json())
.then(res => console.log(res))
.catch(err => console.error(err));
PHP
<?php
$curl = curl_init();
```bash
curl_setopt_array($curl, [
CURLOPT_URL => "https://bridge.polymarket.com/supported-assets",

CURLOPT_RETURNTRANSFER => true,
CURLOPT_ENCODING => "",
CURLOPT_MAXREDIRS => 10,
CURLOPT_TIMEOUT => 30,
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
CURLOPT_CUSTOMREQUEST => "GET",
]);
```
$response = curl_exec($curl);
$err = curl_error($curl);
```bash
curl_close($curl);
if ($err) {
```
echo "cURL Error #:" . $err;
} else {
echo $response;
}
Go
package main
```python
import (
"fmt"
"net/http"
"io"
)
func main() {
url := "https://bridge.polymarket.com/supported-assets"
req, _ := http.NewRequest("GET", url, nil)
res, _ := http.DefaultClient.Do(req)
defer res.Body.Close()
body, _ := io.ReadAll(res.Body)
fmt.Println(string(body))
}
Java
HttpResponse<String> response = Unirest.get("https://bridge.polymarket.com/supported-
assets")
.asString();
```

Ruby
require 'uri'
require 'net/http'
url = URI("https://bridge.polymarket.com/supported-assets")
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true
request = Net::HTTP::Get.new(url)
response = http.request(request)
puts response.read_body
200
{
"supportedAssets": [
{
"chainId": "1",
"chainName": "Ethereum",
"token": {
"name": "USD Coin",
"symbol": "USDC",
"address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
"decimals": 6
},
"minCheckoutUsd": 45
}
]
}
500
{
"error": "<string>"
}
Response
200
application/json
Successfully retrieved supported assets
supportedAssets

object[]
List of supported assets with minimum deposit amounts
Hide child attributes
supportedAssets.chainId
string
Chain ID

### Example

"1"
supportedAssets.chainName
string
Human-readable chain name

### Example

"Ethereum"
supportedAssets.token
object
Hide child attributes
supportedAssets.token.name
string
Full token name

### Example

"USD Coin"
supportedAssets.token.symbol
string
Token symbol

### Example


## "Usdc"

supportedAssets.token.address
string
Token contract address


### Example

"0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
supportedAssets.token.decimals
integer
Token decimals

### Example

6
supportedAssets.minCheckoutUsd
number
Minimum deposit amount in USD

### Example

45
Response
500
application/json
Server Error
error
string
required
Subgraph
Overview
Subgraph Overview
Polymarket has written and open sourced a subgraph that provides, via a GraphQL query
interface, useful aggregate calculations and event indexing for things like volume, user
position, market and liquidity data. The subgraph updates in real time to be able to be mixed,
and match core data from the primary Polymarket interface, providing positional data, activity
history and more. The subgraph can be hosted by anyone but is also hosted and made
publicly available by a 3rd party provider, Goldsky.

Source
The Polymarket subgraph is entirely open source and can be found on the Polymarket
Github.Subgraph Github Repository
Note: The available models/schemas can be found in the schema.graphql file.
Hosted Version
The subgraphs are hosted on goldsky, each with an accompanying GraphQL playground:
Orders
subgraph: https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgrap
hs/orderbook-subgraph/0.0.1/gn
Positions
subgraph: https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgrap
hs/positions-subgraph/0.0.7/gn
Activity
subgraph: https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgrap
hs/activity-subgraph/0.0.4/gn
Open Interest
subgraph: https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgrap
hs/oi-subgraph/0.0.6/gn
PNL
subgraph: https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgrap
hs/pnl-subgraph/0.0.14/gn
Resolution
UMA Optimistic Oracle Integration
Overview
Polymarket leverages UMA’s Optimistic Oracle (OO) to resolve arbitrary questions,
permissionlessly. From UMA’s docs:“UMA’s Optimistic Oracle allows contracts to quickly
request and receive data information … The Optimistic Oracle acts as a generalized
escalation game between contracts that initiate a price request and UMA’s dispute resolution
system known as the Data Verification Mechanism (DVM). Prices proposed by the Optimistic
Oracle will not be sent to the DVM unless it is disputed. If a dispute is raised, a request is
sent to the DVM. All contracts built on UMA use the DVM as a backstop to resolve disputes.
Disputes sent to the DVM will be resolved within a few days — after UMA tokenholders vote
on what the correct outcome should have been.”To allow CTF markets to be resolved via the
OO, Polymarket developed a custom adapter contract called UmaCtfAdapter that provides a
way for the two contract systems to interface.

Clarifications
Recent versions (v2+) of the UmaCtfAdapter also include a bulletin board feature that allows
market creators to issue “clarifications”. Questions that allow updates will include the
sentence in their ancillary data:“Updates made by the question creator via the bulletin board
on 0x6A5D0222186C0FceA7547534cC13c3CFd9b7b6A4F74 should be considered. In
summary, clarifications that do not impact the question’s intent should be considered.”Where
the transaction reference outlining what outlining should be considered.
Resolution Process
Actions
Initiate - Binary CTF markets are initialized via the UmaCtfAdapter ’s initialize() function.
This stores the question parameters on the contract, prepares the CTF and requests a
price for a question from the OO. It returns a questionID that is also used to reference on

### the UmaCtfAdapter . The caller provides

1. ancillaryData - data used to resolve a question (i.e the question + clarifications)
2. rewardToken - ERC20 token address used for payment of rewards and fees
3. reward - Reward amount offered to a successful proposer. The caller must have set
allowance so that the contract can pull this reward in.
4. proposalBond - Bond required to be posted by OO proposers/disputers. If 0, the
default OO bond is used.
5. liveness - UMA liveness period in seconds. If 0, the default liveness period is used.
Propose Price - Anyone can then propose a price to the question on the OO. To do this
they must post the proposalBond . The liveness period begins after a price is proposed.
Dispute - Anyone that disagrees with the proposed price has the opportunity to dispute
the price by posting a counter bond via the OO, this proposed will now be escalated to
the DVM for a voter-wide vote.
Possible Flows
When the first proposed price is disputed for a questionID on the adapter, a callback is made
and posted as the reward for this new proposal. This means a second questionID , making a
new questionID to the OO (the reward is returned before the callback is made and posted as
the reward for this new proposal). This allows for a second round of resolution, and
correspondingly a second dispute is required for it to go to the DVM. The thinking behind this
is to doubles the cost of a potential griefing vector (two disputes are required just one) and
also allows far-fetched (incorrect) first price proposals to not delay the resolution. As such

### there are two possible flows

Initialize (CTFAdapter) -> Propose (OO) -> Resolve (CTFAdapter)
Initialize (CTFAdaptor) -> Propose (OO) -> Challenge (OO) -> Propose (OO) ->
Resolve (CTFAdaptor)

Initialize (CTFAdaptor) -> Propose (OO) -> Challenge (OO) -> Propose (OO) ->
Challenge (CtfAdapter) -> Resolve (CTFAdaptor)
Deployed Addresses
v3.0
Network Address
Polygon Mainnet 0x157Ce2d672854c848c9b79C49a8Cc6cc89176a49
v2.0
Network Address
Polygon Mainnet 0x6A9D0222186C0FceA7547534cC13c3CFd9b7b6A4F74
v1.0
Network Address
Polygon Mainnet 0xC8B122858a4EF82C2d4eE2E6A276C719e692995130
Additional Resources
Audit
Source Code
UMA Documentation
UMA Oracle Portal
Conditional Token Frameworks
Overview
All outcomes on Polymarket are tokenized on the Polygon network. Specifically, Polymarket
outcomes shares are binary outcomes (ie “YES” and “NO”) using Gnosis’ Conditional Token
Framework (CTF). They are distinct ERC1155 tokens related to a parent condition and
backed by the same collateral. More technically, the binary outcome tokens are referred to
as “positionIds” in Gnosis’s documentation. “PositionIds” are derived from a collateral token
and distinct “collectionIds”. “CollectionIds” are derived from a “parentCollectionId”, (always
bytes32(0) in our case) a “conditionId”, and a unique “indexSet”.The “indexSet” is a 256 bit
array denoting which outcome slots are in an outcome collection; it MUST be a nonempty
proper subset of a condition’s outcome slots. In the binary case, which we are interested in,
there are two “indexSets”, one for the first outcome and one for the second. The first

outcome’s “indexSet” is 0b01 = 1 and the second’s is 0b10 = 2. The parent “conditionId”
(shared by both “collectionIds” and therefore “positionIds”) is derived from a “questionId” (a
hash of the UMA ancillary data), an “oracle” (the UMA adapter V2), and an
“outcomeSlotCount” (always 2 in the binary case). The steps for calculating the ERC1155

### token ids (positionIds) is as follows

1. Get the conditionId

### 1. Function

1. getConditionId(oracle, questionId, outcomeSlotCount)

### 2. Inputs

1. oracle : address - UMA adapter V2
2. questionId : bytes32 - hash of the UMA ancillary data
3. outcomeSlotCount : uint - 2 for binary markets
2. Get the two collectionIds

### 1. Function

1. getCollectionId(parentCollectionId, conditionId, indexSet)

### 2. Inputs

1. parentCollectionId : bytes32 - bytes32(0)
2. conditionId : bytes32 - the conditionId derived from (1)
3. indexSet : uint - 1 (0b01) for the first and 2 (0b10) for the second.
3. Get the two positionIds

### 1. Function

1. getPositionId(collateralToken, collectionId)

### 2. Inputs

1. collateralToken : IERC20 - address of ERC20 token collateral (USDC)
2. collectionId : bytes32 - the two collectionIds derived from (3)
Leveraging the relations above, specifically “conditionIds” -> “positionIds” the Gnosis CTF
contract allows for “splitting” and “merging” full outcome sets. We explore these actions and
provide code examples below.
Splitting USDC
At any time, after a condition has been prepared on the CTF contract (via prepareCondition ),
it is possible to “split” collateral into a full (position) set. In other words, one unit USDC can
be split into 1 YES unit and 1 NO unit. If splitting from the collateral, the CTF contract will
attempt to transfer amount collateral from the message sender to itself. If
successful, amount stake will be minted in the split target positions. If any of the transfers,
mints, or burns fail, the transaction will revert. The transaction will also revert if the given
partition is trivial, invalid, or refers to more slots than the condition is prepared with. This
operation happens via the splitPosition() function on the CTF contract with the following

### parameters


collateralToken : IERC20 - The address of the positions’ backing collateral token.
parentCollectionId : bytes32 - The ID of the outcome collections common to the position
being split and the split target positions. Null in Polymarket case.
conditionId : bytes32 - The ID of the condition to split on.
partition : uint[] - An array of disjoint index sets representing a nontrivial partition of the
outcome slots of the given condition. E.G. A|B and C but not A|B and B|C (is not disjoint).
Each element’s a number which, together with the condition, represents the outcome
collection. E.G. 0b110 is A|B, 0b010 is B, etc. In the Polymarket case 1|2.
amount - The amount of collateral or stake to split. Also the number of full sets to
receive.
Merging Tokens
In addition to splitting collateral for a full set, the inverse can also happen; a full set can be
“merged” for collateral. This operation can again happen at any time after a condition has
been prepared on the CTF contract. One unit of each position in a full set is burned in return
for 1 collateral unit. This operation happens via the mergePositions() function on the CTF

### contract with the following parameters

collateralToken : IERC20 - The address of the positions’ backing collateral token.
parentCollectionId : bytes32 - The ID of the outcome collections common to the position
being merged and the merge target positions. Null in Polymarket case.
conditionId : bytes32 - The ID of the condition to merge on.
partition : uint[] - An array of disjoint index sets representing a nontrivial partition of the
outcome slots of the given condition. E.G. A|B and C but not A|B and B|C (is not disjoint).
Each element’s a number which, together with the condition, represents the outcome
collection. E.G. 0b110 is A|B, 0b010 is B, etc. In the Polymarket case 1|2.
amount - The number of full sets to merge. Also the amount of collateral to receive.
Reedeeming Tokens
Once a condition has had it’s payouts reported (ie by the UMACTFAdapter
calling reportPayouts on the CTF contract), users with shares in the winning outcome can
redeem them for the underlying collateral. Specifically, users can call
the redeemPositions function on the CTF contract which will burn all valuable conditional
tokens in return for collateral according to the reported payout vector. This function has the

### following parameters

collateralToken : IERC20 - The address of the positions’ backing collateral token.
parentCollectionId : bytes32 - The ID of the outcome collections common to the position
being redeemed. Null in Polymarket case.
indexSets : uint[] - The ID of the condition to redeem.
indexSets : uint[] - An array of disjoint index sets representing a nontrivial partition of the
outcome slots of the given condition. E.G. A|B and C but not A|B and B|C (is not disjoint).

Each element’s a number which, together with the condition, represents the outcome
collection. E.G. 0b110 is A|B, 0b010 is B, etc. In the Polymarket case 1|2.
Deployment and Additional Information
Deployment
The CTF contract is deployed (and verified) at the following addresses:
Network Deployed Address
Polygon Mainnet 0x4D97DCd97eC945f40cF65F87097ACe5EA0476045
Polygon Mainnet 0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E
Polymarket provides code samples in both Python and TypeScript for interacting with our
smart chain contracts. You will need an RPC endpoint to access the blockchain, and you’ll
be responsible for paying gas fees when executing these RPC/function calls. Please ensure
you’re using the correct example for your wallet type (Safe Wallet vs Proxy Wallet) when
implementing.
Resources
On-Chain Code Samples
Polygon RPC List
CTF Source Code
Audits
Gist For positionId Calculation
Proxy Wallets
Proxy wallet
Overview
When a user first uses Polymarket.com to trade they are prompted to create a wallet. When
they do this, a 1 of 1 multisig is deployed to Polygon which is controlled/owned by the
accessing EOA (either MetaMask wallet or MagicLink wallet). This proxy wallet is where all
the user’s positions (ERC1155) and USDC (ERC20) are held.Using proxy wallets allows
Polymarket to provide an improved UX where multi-step transactions can be executed
atomically and transactions can be relayed by relayers on the gas station network. If you are
a developer looking to programmatically access positions you accumulated via the
Polymarket.com interface, you can either continue using the smart contract wallet by
executing transactions through it from the owner account, or you can transfer these assets to
a new address using the owner account.

Deployments
Each user has their own proxy wallet (and thus proxy wallet address) but the factories are
available at the following deployed addresses on the Polygon network:
Address Details
0xaacfeea03eb1561c4e67d661e40682bd20e3541b Gnosis safe factory – Gnosis
safes are used for all MetaMask
users
0xaB45c5A4B0c941a2F231C04C3f49182e1A254052 Polymarket proxy factory –
Polymarket custom proxy
contracts are used for all
MagicLink users
Negative Risk
Overview
Certain events which meet the criteria of being “winner-take-all” may be deployed
as “negative risk” events/markets. The Gamma API includes a boolean field on
events, negRisk , which indicates whether the event is negative risk.Negative risk allows for
increased capital efficiency by relating all markets within events via a convert action. More
explicitly, a NO share in any market can be converted into 1 YES share in all other markets.
Converts can be exercised via the Negative Adapter. You can read more about negative
risk here.
Augmented Negative Risk
There is a known issue with the negative risk architecture which is that the outcome universe
must be complete before conversions are made or otherwise conversion will “cost”
something. In most cases, the outcome universe can be made complete by deploying all the
named outcomes and then an “other” option. But in some cases this is undesirable as new
outcomes can come out of nowhere and you’d rather them be directly named versus
grouped together in an “other”.To fix this, some markets use a system of “augmented
negative risk”, where named outcomes, a collection of unnamed outcomes, and an other is
deployed. When a new outcome needs to be added, an unnamed outcome can be clarified
to be the new outcome via the bulletin board. This means the “other” in the case of
augmented negative risk can effectively change definitions (outcomes can be taken out of
it).As such, trading should only happen on the named outcomes, and the other outcomes
should be ignored until they are named or until resolution occurs. The Polymarket UI will not

show unnamed outcomes.If a market becomes resolvable and the correct outcome is not
named (originally or via placeholder clarification), it should resolve to the “other” outcome. An
event can be considered “augmented negative risk” when enableNegRisk is
true AND negRiskAugmented is true.The naming conventions are as follows:
Original Outcomes
Outcome A
Outcome B
…
Placeholder Outcomes
Person A -> can be clarified to a named outcome
Person B -> can be clarified to a named outcome
…
Explicit Other
Other -> not meant to be traded as the definition of this changes as placeholder
outcomes are clarified to named outcomes