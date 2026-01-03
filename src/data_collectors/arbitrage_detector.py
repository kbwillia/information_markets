"""Detect arbitrage opportunities between Kalshi and Polymarket."""
from typing import Dict, List, Optional, Tuple
import pandas as pd
from datetime import datetime

from src.data_collectors.kalshi_client import KalshiClient
from src.data_collectors.polymarket_client import PolymarketClient
from src.config import Config


class ArbitrageDetector:
    """Detect and analyze arbitrage opportunities between platforms."""
    
    def __init__(self):
        self.kalshi = KalshiClient()
        self.polymarket = PolymarketClient()
        self.min_profit_threshold = Config.MIN_PROFIT_THRESHOLD
    
    def normalize_market_name(self, name: str) -> str:
        """Normalize market names for comparison across platforms."""
        # Remove common prefixes/suffixes, normalize case, etc.
        name = name.lower().strip()
        # Add more normalization logic as needed
        return name
    
    def find_matching_markets(self, kalshi_markets: List[Dict], 
                             polymarket_markets: List[Dict]) -> List[Tuple[Dict, Dict]]:
        """Find markets that exist on both platforms."""
        matches = []
        
        # Create normalized lookup
        kalshi_lookup = {
            self.normalize_market_name(m.get("title", "")): m 
            for m in kalshi_markets
        }
        
        for pm_market in polymarket_markets:
            normalized = self.normalize_market_name(pm_market.get("question", ""))
            if normalized in kalshi_lookup:
                matches.append((kalshi_lookup[normalized], pm_market))
        
        return matches
    
    def get_market_prices(self, kalshi_ticker: str, polymarket_id: str) -> Dict:
        """Get prices for the same market on both platforms."""
        try:
            kalshi_orderbook = self.kalshi.get_orderbook(kalshi_ticker)
            polymarket_orderbook = self.polymarket.get_orderbook(polymarket_id)
            
            # Extract best bid/ask from Kalshi
            kalshi_yes_bids = kalshi_orderbook.get("yes", {}).get("bids", [])
            kalshi_yes_asks = kalshi_orderbook.get("yes", {}).get("asks", [])
            
            kalshi_yes_bid = max(kalshi_yes_bids, key=lambda x: x["price"]) if kalshi_yes_bids else None
            kalshi_yes_ask = min(kalshi_yes_asks, key=lambda x: x["price"]) if kalshi_yes_asks else None
            
            # Extract best bid/ask from Polymarket
            polymarket_bids = polymarket_orderbook.get("bids", [])
            polymarket_asks = polymarket_orderbook.get("asks", [])
            
            pm_best_bid = max(polymarket_bids, key=lambda x: x["price"]) if polymarket_bids else None
            pm_best_ask = min(polymarket_asks, key=lambda x: x["price"]) if polymarket_asks else None
            
            return {
                "kalshi": {
                    "yes_bid": kalshi_yes_bid["price"] / 100 if kalshi_yes_bid else None,
                    "yes_ask": kalshi_yes_ask["price"] / 100 if kalshi_yes_ask else None,
                },
                "polymarket": {
                    "bid": pm_best_bid["price"] if pm_best_bid else None,
                    "ask": pm_best_ask["price"] if pm_best_ask else None,
                }
            }
        except Exception as e:
            print(f"Error getting prices: {e}")
            return {}
    
    def calculate_arbitrage_opportunity(self, prices: Dict) -> Optional[Dict]:
        """Calculate if there's an arbitrage opportunity."""
        kalshi_yes_bid = prices.get("kalshi", {}).get("yes_bid")
        kalshi_yes_ask = prices.get("kalshi", {}).get("yes_ask")
        pm_bid = prices.get("polymarket", {}).get("bid")
        pm_ask = prices.get("polymarket", {}).get("ask")
        
        if not all([kalshi_yes_bid, kalshi_yes_ask, pm_bid, pm_ask]):
            return None
        
        opportunities = []
        
        # Opportunity 1: Buy on Kalshi (yes), sell on Polymarket
        if kalshi_yes_ask < pm_bid:
            profit = pm_bid - kalshi_yes_ask
            if profit >= self.min_profit_threshold:
                opportunities.append({
                    "type": "buy_kalshi_sell_polymarket",
                    "profit": profit,
                    "kalshi_price": kalshi_yes_ask,
                    "polymarket_price": pm_bid,
                    "direction": "yes"
                })
        
        # Opportunity 2: Buy on Polymarket, sell on Kalshi (yes)
        if pm_ask < kalshi_yes_bid:
            profit = kalshi_yes_bid - pm_ask
            if profit >= self.min_profit_threshold:
                opportunities.append({
                    "type": "buy_polymarket_sell_kalshi",
                    "profit": profit,
                    "kalshi_price": kalshi_yes_bid,
                    "polymarket_price": pm_ask,
                    "direction": "yes"
                })
        
        if opportunities:
            return max(opportunities, key=lambda x: x["profit"])
        return None
    
    def scan_for_arbitrage(self, limit: int = 50) -> List[Dict]:
        """Scan for arbitrage opportunities across all markets."""
        opportunities = []
        
        try:
            kalshi_markets = self.kalshi.get_markets(limit=limit).get("markets", [])
            polymarket_markets = self.polymarket.get_markets(limit=limit).get("markets", [])
            
            matches = self.find_matching_markets(kalshi_markets, polymarket_markets)
            
            for kalshi_market, pm_market in matches:
                prices = self.get_market_prices(
                    kalshi_market["ticker"],
                    pm_market["id"]
                )
                
                opportunity = self.calculate_arbitrage_opportunity(prices)
                if opportunity:
                    opportunity.update({
                        "kalshi_ticker": kalshi_market["ticker"],
                        "polymarket_id": pm_market["id"],
                        "market_title": kalshi_market.get("title", ""),
                        "timestamp": datetime.now().isoformat()
                    })
                    opportunities.append(opportunity)
        
        except Exception as e:
            print(f"Error scanning for arbitrage: {e}")
        
        return sorted(opportunities, key=lambda x: x["profit"], reverse=True)

