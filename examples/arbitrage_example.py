"""Example script for arbitrage detection."""
from src.data_collectors.arbitrage_detector import ArbitrageDetector

# Initialize arbitrage detector
detector = ArbitrageDetector()

# Scan for arbitrage opportunities
print("Scanning for arbitrage opportunities...")
opportunities = detector.scan_for_arbitrage(limit=100)

if opportunities:
    print(f"\nFound {len(opportunities)} arbitrage opportunities:\n")
    
    for i, opp in enumerate(opportunities[:10], 1):  # Show top 10
        print(f"{i}. {opp['market_title']}")
        print(f"   Type: {opp['type']}")
        print(f"   Profit: {opp['profit']:.2%}")
        print(f"   Kalshi Price: {opp['kalshi_price']:.4f}")
        print(f"   Polymarket Price: {opp['polymarket_price']:.4f}")
        print()
else:
    print("No arbitrage opportunities found at this time.")

# Example: Check specific market
print("\nChecking specific market prices...")
# You would need actual market IDs/tickers
# prices = detector.get_market_prices("KALSHI_TICKER", "POLYMARKET_ID")
# opportunity = detector.calculate_arbitrage_opportunity(prices)
# if opportunity:
#     print(f"Arbitrage opportunity: {opportunity}")

