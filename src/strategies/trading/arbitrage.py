"""
Strategy 6: Cross-Platform Arbitrage

TRUE arbitrage exploits price inefficiencies between Kalshi and Polymarket
to lock in risk-free (or near risk-free) profits.

IMPORTANT FEE STRUCTURES:
- Kalshi: 10% fee on PROFITS only (not on trade amount)
  - Example: Buy at $0.40, event resolves YES, you get $1.00
  - Profit = $0.60, Fee = $0.06, Net profit = $0.54
  - If event resolves NO, you lose $0.40, NO FEE
  
- Polymarket: NO trading fees
  - However, there are gas costs for on-chain settlement (~$0.01-$0.10)
  - We model this as a small fixed cost per trade

ARBITRAGE TYPES:
1. DUTCH BOOK: Buy YES on one platform + NO on other platform
   - If YES_price_A + NO_price_B < 1.00, guaranteed profit
   - Risk-free if same event, same resolution

2. PRICE GAP: Same position cheaper on one platform
   - Buy cheap YES on platform A, sell YES on platform B
   - Risk: Positions may not settle simultaneously

Key insight: After fees, the arbitrage must still be profitable!
"""
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from src.strategies.trading.base import (
    BaseStrategy, Signal, SignalType, SignalStrength, Trade, TradeResult
)
from src.core.data_manager import DataManager, MatchedMarket


class ArbitrageType(Enum):
    """Type of arbitrage opportunity."""
    DUTCH_BOOK = "dutch_book"      # Buy YES + NO across platforms
    PRICE_GAP = "price_gap"        # Same position, different prices
    

@dataclass
class FeeStructure:
    """Fee structure for a platform."""
    profit_fee_rate: float  # Percentage of profits taken as fee (0.10 = 10%)
    fixed_fee_per_trade: float  # Fixed cost per trade (gas, etc.)
    name: str


# Define fee structures
KALSHI_FEES = FeeStructure(
    profit_fee_rate=0.10,      # 10% of profits
    fixed_fee_per_trade=0.00,  # No fixed fees
    name="kalshi"
)

POLYMARKET_FEES = FeeStructure(
    profit_fee_rate=0.00,      # No profit fee
    fixed_fee_per_trade=0.02,  # ~$0.02 gas cost estimate per trade
    name="polymarket"
)


@dataclass
class ArbitrageOpportunity:
    """A detected arbitrage opportunity."""
    arb_type: ArbitrageType
    market_title: str
    kalshi_market_id: str
    polymarket_market_id: str
    
    # Prices (0-1 scale)
    kalshi_yes_price: float
    kalshi_no_price: float
    polymarket_yes_price: float
    polymarket_no_price: float
    
    # Trade details
    buy_platform: str
    buy_side: str  # 'yes' or 'no'
    buy_price: float
    
    sell_platform: str
    sell_side: str
    sell_price: float
    
    # Profit calculations
    gross_profit_per_dollar: float  # Before fees
    net_profit_per_dollar: float    # After fees
    total_fees_per_dollar: float
    
    # Risk assessment
    risk_score: float  # 0 = risk-free, 1 = high risk
    
    def is_profitable(self) -> bool:
        return self.net_profit_per_dollar > 0


class ArbitrageStrategy(BaseStrategy):
    """
    Execute arbitrage trades between Kalshi and Polymarket.
    
    How it works:
    1. Find matched markets (same event on both platforms)
    2. Calculate arbitrage opportunities accounting for fees
    3. Execute trades on both platforms simultaneously
    4. Track position until resolution
    
    Parameters:
    - min_net_profit: Minimum net profit (after fees) to execute (default: 1%)
    - max_position_per_arb: Maximum to risk on single arbitrage (default: $50)
    - kalshi_fee_rate: Kalshi profit fee rate (default: 10%)
    - polymarket_gas_cost: Estimated gas cost per trade (default: $0.02)
    """
    
    def __init__(self, data_manager: DataManager,
                 paper_trading: bool = True,
                 max_position_size: float = None,
                 min_net_profit: float = 0.01,
                 max_position_per_arb: float = 50.0,
                 kalshi_fee_rate: float = 0.10,
                 polymarket_gas_cost: float = 0.02):
        super().__init__(data_manager, paper_trading, max_position_size)
        
        self.min_net_profit = min_net_profit
        self.max_position_per_arb = max_position_per_arb
        
        # Configure fees
        self.kalshi_fees = FeeStructure(
            profit_fee_rate=kalshi_fee_rate,
            fixed_fee_per_trade=0.00,
            name="kalshi"
        )
        self.polymarket_fees = FeeStructure(
            profit_fee_rate=0.00,
            fixed_fee_per_trade=polymarket_gas_cost,
            name="polymarket"
        )
        
        # Track open arbitrage positions
        self.open_positions: Dict[str, ArbitrageOpportunity] = {}
    
    @property
    def name(self) -> str:
        return "arbitrage"
    
    @property
    def description(self) -> str:
        return "Cross-platform arbitrage between Kalshi and Polymarket"
    
    def analyze(self) -> List[Signal]:
        """Find and analyze arbitrage opportunities."""
        signals = []
        
        matched_markets = self.data_manager.get_matched_markets()
        
        for match in matched_markets:
            opportunities = self._find_arbitrage_opportunities(match)
            
            for opp in opportunities:
                if opp.is_profitable() and opp.net_profit_per_dollar >= self.min_net_profit:
                    signal = self._create_signal(opp)
                    if signal:
                        signals.append(signal)
        
        return signals
    
    def _find_arbitrage_opportunities(self, match: MatchedMarket) -> List[ArbitrageOpportunity]:
        """Find all arbitrage opportunities for a matched market."""
        opportunities = []
        
        # Get prices
        kalshi_yes = match.kalshi.yes_price
        kalshi_no = match.kalshi.no_price
        poly_yes = match.polymarket.yes_price
        poly_no = match.polymarket.no_price
        
        # Handle missing prices
        if kalshi_yes is None or poly_yes is None:
            return []
        
        # Infer NO prices if not available (NO = 1 - YES)
        if kalshi_no is None:
            kalshi_no = 1.0 - kalshi_yes
        if poly_no is None:
            poly_no = 1.0 - poly_yes
        
        # === DUTCH BOOK ARBITRAGE ===
        # Type 1: Buy Kalshi YES + Polymarket NO
        total_cost_1 = kalshi_yes + poly_no
        if total_cost_1 < 1.0:
            gross_profit = 1.0 - total_cost_1
            opp = self._calculate_dutch_book(
                match=match,
                kalshi_yes=kalshi_yes,
                kalshi_no=kalshi_no,
                poly_yes=poly_yes,
                poly_no=poly_no,
                buy_kalshi_yes=True,
                gross_profit=gross_profit
            )
            if opp:
                opportunities.append(opp)
        
        # Type 2: Buy Polymarket YES + Kalshi NO
        total_cost_2 = poly_yes + kalshi_no
        if total_cost_2 < 1.0:
            gross_profit = 1.0 - total_cost_2
            opp = self._calculate_dutch_book(
                match=match,
                kalshi_yes=kalshi_yes,
                kalshi_no=kalshi_no,
                poly_yes=poly_yes,
                poly_no=poly_no,
                buy_kalshi_yes=False,
                gross_profit=gross_profit
            )
            if opp:
                opportunities.append(opp)
        
        # === PRICE GAP ARBITRAGE ===
        # If YES is cheaper on one platform
        yes_gap = abs(kalshi_yes - poly_yes)
        if yes_gap > 0.02:  # Minimum gap to consider
            opp = self._calculate_price_gap(
                match=match,
                kalshi_yes=kalshi_yes,
                kalshi_no=kalshi_no,
                poly_yes=poly_yes,
                poly_no=poly_no
            )
            if opp:
                opportunities.append(opp)
        
        return opportunities
    
    def _calculate_dutch_book(self, match: MatchedMarket,
                              kalshi_yes: float, kalshi_no: float,
                              poly_yes: float, poly_no: float,
                              buy_kalshi_yes: bool,
                              gross_profit: float) -> Optional[ArbitrageOpportunity]:
        """
        Calculate Dutch book arbitrage opportunity.
        
        Dutch book: Buy YES on one platform + NO on other = guaranteed $1 payout
        """
        if buy_kalshi_yes:
            # Buy Kalshi YES, Buy Polymarket NO
            kalshi_buy_price = kalshi_yes
            kalshi_buy_side = "yes"
            poly_buy_price = poly_no
            poly_buy_side = "no"
        else:
            # Buy Polymarket YES, Buy Kalshi NO
            kalshi_buy_price = kalshi_no
            kalshi_buy_side = "no"
            poly_buy_price = poly_yes
            poly_buy_side = "yes"
        
        # Calculate fees
        # For Dutch book, one side ALWAYS wins
        # Kalshi charges 10% on the winning side's profit
        
        # Expected profit before fees = 1.0 - total_cost
        # After Kalshi fee: profit reduced by 10% of Kalshi winning amount
        
        # If event resolves as predicted by Kalshi side:
        # Kalshi profit = 1.0 - kalshi_buy_price
        # Kalshi fee = 0.10 * (1.0 - kalshi_buy_price)
        # Poly position = 0 (lost)
        
        # If event resolves opposite:
        # Poly profit = 1.0 - poly_buy_price
        # Poly fee = 0 (no profit fee on Polymarket)
        # Kalshi position = 0 (lost, no fee)
        
        # Expected Kalshi fee (50% chance each outcome)
        # But in arbitrage, we're guaranteed one wins
        kalshi_profit_if_win = 1.0 - kalshi_buy_price
        kalshi_fee = self.kalshi_fees.profit_fee_rate * kalshi_profit_if_win
        
        # Fixed fees (gas)
        poly_fixed_fee = self.polymarket_fees.fixed_fee_per_trade
        
        # Net profit per dollar invested
        total_cost = kalshi_buy_price + poly_buy_price
        total_fees = kalshi_fee + poly_fixed_fee
        net_profit = gross_profit - total_fees
        net_profit_per_dollar = net_profit / total_cost if total_cost > 0 else 0
        
        return ArbitrageOpportunity(
            arb_type=ArbitrageType.DUTCH_BOOK,
            market_title=match.kalshi.title,
            kalshi_market_id=match.kalshi.id,
            polymarket_market_id=match.polymarket.id,
            kalshi_yes_price=kalshi_yes,
            kalshi_no_price=kalshi_no,
            polymarket_yes_price=poly_yes,
            polymarket_no_price=poly_no,
            buy_platform="kalshi",
            buy_side=kalshi_buy_side,
            buy_price=kalshi_buy_price,
            sell_platform="polymarket",
            sell_side=poly_buy_side,
            sell_price=poly_buy_price,
            gross_profit_per_dollar=gross_profit / total_cost if total_cost > 0 else 0,
            net_profit_per_dollar=net_profit_per_dollar,
            total_fees_per_dollar=total_fees / total_cost if total_cost > 0 else 0,
            risk_score=0.1  # Dutch book is near risk-free
        )
    
    def _calculate_price_gap(self, match: MatchedMarket,
                             kalshi_yes: float, kalshi_no: float,
                             poly_yes: float, poly_no: float) -> Optional[ArbitrageOpportunity]:
        """
        Calculate price gap arbitrage.
        
        Price gap: Same position (YES) is cheaper on one platform.
        Risk: Must hold until resolution or find exit.
        """
        # Determine which platform has cheaper YES
        if kalshi_yes < poly_yes:
            buy_platform = "kalshi"
            buy_price = kalshi_yes
            sell_platform = "polymarket"
            sell_price = poly_yes
        else:
            buy_platform = "polymarket"
            buy_price = poly_yes
            sell_platform = "kalshi"
            sell_price = kalshi_yes
        
        gap = sell_price - buy_price
        
        # This isn't true arbitrage - it's a bet that prices will converge
        # Risk: Prices might diverge further before converging
        
        # Calculate expected profit accounting for fees
        # Worst case: event resolves, we need to calculate expected value
        
        # If we buy on the cheap platform and event resolves YES:
        # Profit = 1.0 - buy_price
        # If on Kalshi: fee = 10% of profit
        # If on Polymarket: fee = gas only
        
        if buy_platform == "kalshi":
            expected_profit = 1.0 - buy_price
            kalshi_fee = self.kalshi_fees.profit_fee_rate * expected_profit
            fees = kalshi_fee
        else:
            fees = self.polymarket_fees.fixed_fee_per_trade
        
        # Simple model: expected profit is the gap minus fees
        # This assumes 50% chance of resolution either way
        gross_profit = gap
        net_profit = gross_profit - fees
        
        return ArbitrageOpportunity(
            arb_type=ArbitrageType.PRICE_GAP,
            market_title=match.kalshi.title,
            kalshi_market_id=match.kalshi.id,
            polymarket_market_id=match.polymarket.id,
            kalshi_yes_price=kalshi_yes,
            kalshi_no_price=kalshi_no,
            polymarket_yes_price=poly_yes,
            polymarket_no_price=poly_no,
            buy_platform=buy_platform,
            buy_side="yes",
            buy_price=buy_price,
            sell_platform=sell_platform,
            sell_side="yes",
            sell_price=sell_price,
            gross_profit_per_dollar=gross_profit / buy_price if buy_price > 0 else 0,
            net_profit_per_dollar=net_profit / buy_price if buy_price > 0 else 0,
            total_fees_per_dollar=fees / buy_price if buy_price > 0 else 0,
            risk_score=0.5  # Price gap has medium risk
        )
    
    def _create_signal(self, opp: ArbitrageOpportunity) -> Signal:
        """Create a trading signal from an arbitrage opportunity."""
        # Determine strength based on profit and risk
        if opp.net_profit_per_dollar > 0.10 and opp.risk_score < 0.3:
            strength = SignalStrength.STRONG
        elif opp.net_profit_per_dollar > 0.05:
            strength = SignalStrength.MODERATE
        else:
            strength = SignalStrength.WEAK
        
        # Confidence based on arbitrage type
        if opp.arb_type == ArbitrageType.DUTCH_BOOK:
            confidence = 0.95  # Near-certain profit
        else:
            confidence = 0.70  # Price gap has execution risk
        
        return Signal(
            strategy_name=self.name,
            signal_type=SignalType.BUY,
            strength=strength,
            platform=opp.buy_platform,
            market_id=opp.kalshi_market_id if opp.buy_platform == "kalshi" else opp.polymarket_market_id,
            market_title=opp.market_title,
            side=opp.buy_side,
            target_price=opp.buy_price,
            current_price=opp.buy_price,
            confidence=confidence,
            reasoning=f"{opp.arb_type.value.upper()}: "
                     f"Net profit {opp.net_profit_per_dollar*100:.1f}% after fees. "
                     f"Buy {opp.buy_side.upper()} on {opp.buy_platform} @ {opp.buy_price:.3f}, "
                     f"complementary on {opp.sell_platform} @ {opp.sell_price:.3f}. "
                     f"Fees: {opp.total_fees_per_dollar*100:.2f}%",
            metadata={
                'arb_type': opp.arb_type.value,
                'kalshi_yes': opp.kalshi_yes_price,
                'kalshi_no': opp.kalshi_no_price,
                'poly_yes': opp.polymarket_yes_price,
                'poly_no': opp.polymarket_no_price,
                'gross_profit_pct': opp.gross_profit_per_dollar * 100,
                'net_profit_pct': opp.net_profit_per_dollar * 100,
                'fees_pct': opp.total_fees_per_dollar * 100,
                'risk_score': opp.risk_score,
                'complementary_platform': opp.sell_platform,
                'complementary_side': opp.sell_side,
                'complementary_price': opp.sell_price
            }
        )
    
    def execute_trade(self, trade: Trade) -> TradeResult:
        """
        Execute arbitrage trade (includes complementary trade).
        
        For Dutch book arbitrage, we need to execute on BOTH platforms.
        """
        # First, execute the primary trade
        primary_result = super().execute_trade(trade)
        
        if not primary_result.success:
            return primary_result
        
        # For Dutch book, execute complementary trade
        arb_type = trade.signal.metadata.get('arb_type')
        
        if arb_type == ArbitrageType.DUTCH_BOOK.value:
            comp_platform = trade.signal.metadata.get('complementary_platform')
            comp_side = trade.signal.metadata.get('complementary_side')
            comp_price = trade.signal.metadata.get('complementary_price')
            comp_market_id = (
                trade.signal.metadata.get('polymarket_market_id') 
                if comp_platform == 'polymarket' 
                else trade.signal.metadata.get('kalshi_market_id')
            )
            
            # Create complementary trade
            comp_trade = Trade(
                signal=trade.signal,
                platform=comp_platform,
                market_id=comp_market_id or trade.market_id,
                side=comp_side,
                action="buy",
                quantity=trade.quantity,
                price=comp_price,
                order_type="limit"
            )
            
            # Execute complementary trade
            if self.paper_trading:
                comp_result = self._paper_trade(comp_trade)
            else:
                comp_result = self._real_trade(comp_trade)
            
            # Update result to include both trades
            primary_result.trade.signal.metadata['complementary_result'] = comp_result.to_dict()
        
        return primary_result
    
    def get_current_opportunities(self) -> List[Dict]:
        """Get all current arbitrage opportunities (for monitoring)."""
        opportunities = []
        matched_markets = self.data_manager.get_matched_markets()
        
        for match in matched_markets:
            opps = self._find_arbitrage_opportunities(match)
            for opp in opps:
                opportunities.append({
                    'type': opp.arb_type.value,
                    'market': opp.market_title,
                    'kalshi_yes': opp.kalshi_yes_price,
                    'kalshi_no': opp.kalshi_no_price,
                    'poly_yes': opp.polymarket_yes_price,
                    'poly_no': opp.polymarket_no_price,
                    'gross_profit_pct': opp.gross_profit_per_dollar * 100,
                    'net_profit_pct': opp.net_profit_per_dollar * 100,
                    'fees_pct': opp.total_fees_per_dollar * 100,
                    'is_profitable': opp.is_profitable(),
                    'risk_score': opp.risk_score
                })
        
        # Sort by net profit
        opportunities.sort(key=lambda x: x['net_profit_pct'], reverse=True)
        return opportunities
    
    def calculate_required_spread(self, position_size: float = 100.0) -> Dict:
        """
        Calculate the minimum spread needed for profitable arbitrage.
        
        This helps understand what opportunities are actually viable.
        """
        # For Dutch book with Kalshi fee
        # Profit = 1 - (kalshi_price + poly_price) - kalshi_fee - poly_gas
        # For break-even: gross_profit = kalshi_fee + poly_gas
        # Where kalshi_fee = 0.10 * (1 - kalshi_price)
        
        # Simplified: minimum spread needed
        poly_gas = self.polymarket_fees.fixed_fee_per_trade
        kalshi_rate = self.kalshi_fees.profit_fee_rate
        
        # Assuming 50% prices (worst case for fees)
        kalshi_fee_at_50 = kalshi_rate * 0.50
        min_spread_break_even = kalshi_fee_at_50 + poly_gas
        min_spread_profitable = min_spread_break_even + self.min_net_profit
        
        return {
            'min_spread_break_even': min_spread_break_even,
            'min_spread_profitable': min_spread_profitable,
            'kalshi_fee_estimate': kalshi_fee_at_50,
            'polymarket_gas_cost': poly_gas,
            'required_profit_margin': self.min_net_profit,
            'notes': (
                f"For Dutch book arbitrage to be profitable, "
                f"total YES+NO cost must be less than {1-min_spread_profitable:.1%}. "
                f"Kalshi charges {kalshi_rate:.0%} on profits."
            )
        }

