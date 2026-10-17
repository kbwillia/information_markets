"""
Trader Statistics Collection and Analysis

Fetches and processes trader/leaderboard data from Polymarket.
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from src.data_collectors.polymarket_client import PolymarketClient


def calculate_trader_profitable_percentage(trader_address: str, client: PolymarketClient = None) -> Optional[float]:
    """
    Calculate profitable trade percentage for a trader by analyzing their closed positions.
    
    Args:
        trader_address: Trader's wallet address
        client: Optional PolymarketClient instance (creates new one if not provided)
    
    Returns:
        Profitable percentage (0-100) or None if data unavailable
    """
    if client is None:
        client = PolymarketClient()
    
    try:
        # Try to get closed positions which have PnL data
        # Use the v1/closed-positions endpoint
        original_url = client.base_url
        client.use_data_api()
        try:
            # Try v1/closed-positions endpoint first
            try:
                result = client._request("GET", "/v1/closed-positions", {
                    "user": trader_address,
                    "limit": 500  # Get up to 500 closed positions
                })
            except:
                # Fallback to /closed-positions
                result = client._request("GET", "/closed-positions", {
                    "user": trader_address,
                    "limit": 500
                })
            
            # Handle different response formats
            if isinstance(result, list):
                closed_positions = result
            elif isinstance(result, dict):
                closed_positions = result.get('data', result.get('positions', result.get('results', [])))
            else:
                closed_positions = []
            
            if not closed_positions:
                return None
            
            # Calculate profitable percentage from closed positions
            total_positions = len(closed_positions)
            profitable_positions = 0
            
            for position in closed_positions:
                # Check if position was profitable
                # Look for PnL fields: realizedPnl (most common), cashPnl, percentPnl, pnl, etc.
                realized_pnl = position.get('realizedPnl') or position.get('realized_pnl')
                cash_pnl = position.get('cashPnl') or position.get('cash_pnl') or position.get('pnl')
                percent_pnl = position.get('percentPnl') or position.get('percent_pnl')
                
                # Try realizedPnl first (this is what Polymarket API actually returns)
                if realized_pnl is not None:
                    try:
                        pnl_value = float(realized_pnl)
                        if pnl_value > 0:
                            profitable_positions += 1
                    except (ValueError, TypeError):
                        # Fall through to other fields
                        pass
                elif cash_pnl is not None:
                    try:
                        pnl_value = float(cash_pnl)
                        if pnl_value > 0:
                            profitable_positions += 1
                    except (ValueError, TypeError):
                        continue
                elif percent_pnl is not None:
                    try:
                        pnl_pct = float(percent_pnl)
                        if pnl_pct > 0:
                            profitable_positions += 1
                    except (ValueError, TypeError):
                        continue
            
            if total_positions > 0:
                return (profitable_positions / total_positions) * 100
            return None
        finally:
            client.base_url = original_url
            
    except Exception as e:
        print(f"Error calculating profitable percentage for trader {trader_address[:8]}...: {e}")
        return None


def fetch_trader_leaderboard(limit: int = 50, time_period: str = "ALL", include_profitable_pct: bool = True) -> List[Dict]:
    """Fetch top traders from Polymarket leaderboard.
    
    Args:
        limit: Number of traders to fetch (max 50)
        time_period: Time period (DAY, WEEK, MONTH, ALL)
        include_profitable_pct: Whether to calculate profitable trade percentage (slower but more accurate)
    
    Returns:
        List of trader dictionaries with rank, username, pnl, volume, etc.
    """
    client = PolymarketClient()
    try:
        result = client.get_leaderboard(
            limit=limit,
            time_period=time_period,
            order_by="PNL"
        )
        
        # Handle different response formats
        if isinstance(result, list):
            traders = result
        elif isinstance(result, dict):
            traders = result.get('data', result.get('traders', result.get('results', [])))
        else:
            traders = []
        
        # If profitable percentage is requested and not in API response, calculate it
        if include_profitable_pct and traders:
            print(f"Calculating profitable trade percentages for {len(traders)} traders...")
            for i, trader in enumerate(traders):
                # Check if already has profitable percentage
                if trader.get('winRate') or trader.get('win_rate') or trader.get('profitable_pct'):
                    continue
                
                # Get trader address
                trader_address = trader.get('proxyWallet') or trader.get('address')
                if trader_address:
                    profitable_pct = calculate_trader_profitable_percentage(trader_address, client)
                    if profitable_pct is not None:
                        trader['profitable_pct'] = profitable_pct / 100  # Store as decimal (0-1)
                        trader['winRate'] = profitable_pct  # Also store as percentage for compatibility
                    if (i + 1) % 5 == 0:
                        print(f"  Processed {i + 1}/{len(traders)} traders...")
        
        return traders
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        return []


def calculate_trader_metrics(traders: List[Dict]) -> Dict:
    """Calculate aggregate metrics from trader data.
    
    Args:
        traders: List of trader dictionaries
    
    Returns:
        Dictionary with aggregate statistics
    """
    if not traders:
        return {
            'total_traders': 0,
            'total_pnl': 0,
            'total_volume': 0,
            'avg_pnl': 0,
            'avg_volume': 0,
            'profitable_count': 0,
            'profitable_pct': 0,
            'top_pnl': 0,
            'top_volume': 0
        }
    
    pnls = [float(t.get('pnl', 0) or 0) for t in traders]
    volumes = [float(t.get('vol', t.get('volume', 0)) or 0) for t in traders]
    
    profitable = [p for p in pnls if p > 0]
    
    return {
        'total_traders': len(traders),
        'total_pnl': sum(pnls),
        'total_volume': sum(volumes),
        'avg_pnl': sum(pnls) / len(pnls) if pnls else 0,
        'avg_volume': sum(volumes) / len(volumes) if volumes else 0,
        'profitable_count': len(profitable),
        'profitable_pct': (len(profitable) / len(traders) * 100) if traders else 0,
        'top_pnl': max(pnls) if pnls else 0,
        'top_volume': max(volumes) if volumes else 0,
        'median_pnl': sorted(pnls)[len(pnls)//2] if pnls else 0
    }

