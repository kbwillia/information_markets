"""
Complete-set arbitrage for mutually exclusive outcomes.

When exactly one outcome pays $1, one share of every outcome is worth $1.

- Buy every Yes if the asks add up to less than $1.
- Sell every Yes if the bids add up to more than $1.

Polymarket: neg-risk events that are not augmented. Augmented events can
still add an outcome, so the listed names are not a complete set.

Kalshi: events whose mutually_exclusive flag was stamped onto the cached
markets. Threshold ladders share an event ticker and are left alone.
"""
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from src.core.data_manager import MarketData
from src.strategies.trading.base import (
    BaseStrategy, Signal, SignalType, SignalStrength, Trade, TradeResult
)


@dataclass
class OutcomeLeg:
    """One outcome inside an exclusive event."""
    market_id: str
    label: str
    bid: Optional[float]
    ask: Optional[float]


@dataclass
class ExclusiveEvent:
    """A set of outcomes where exactly one can resolve yes."""
    platform: str
    event_id: str
    title: str
    legs: List[OutcomeLeg] = field(default_factory=list)


@dataclass
class CompleteSetOpportunity:
    """A basket whose prices do not add up to $1."""
    event: ExclusiveEvent
    direction: str  # buy_all_yes or sell_all_yes
    prices: List[float]
    price_sum: float
    gross_profit: float
    fees: float
    net_profit: float

    def is_profitable(self, min_net_profit: float) -> bool:
        return self.net_profit >= min_net_profit


def _as_price(value) -> Optional[float]:
    """Parse a price onto the 0-1 scale. Cents above 1 are scaled down."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, str):
        text = value.strip()
        if not text or text[0] in "[{":
            return None
        try:
            value = float(text)
        except ValueError:
            return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    if value > 1:
        value = value / 100.0
    if value < 0 or value > 1:
        return None
    return value


def _parse_events(raw: Dict) -> List[Dict]:
    events = raw.get("events") or []
    if isinstance(events, str):
        try:
            events = json.loads(events)
        except (TypeError, json.JSONDecodeError):
            return []
    if not isinstance(events, list):
        return []
    return [event for event in events if isinstance(event, dict)]


def _truthy(value) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes"}
    return bool(value)


def outcome_quotes(market: MarketData) -> tuple:
    """Best bid and ask for Yes. A zero bid is an empty book."""
    raw = market.raw_data or {}
    bid = market.yes_bid if market.yes_bid else None
    ask = market.yes_ask if market.yes_ask else None
    if bid is None:
        bid = _as_price(raw.get("bestBid"))
        if bid is None:
            bid = _as_price(raw.get("yes_bid_dollars"))
        if bid is None:
            bid = _as_price(raw.get("yes_bid"))
    if ask is None:
        ask = _as_price(raw.get("bestAsk"))
        if ask is None:
            ask = _as_price(raw.get("yes_ask_dollars"))
        if ask is None:
            ask = _as_price(raw.get("yes_ask"))
    if bid is not None and bid <= 0:
        bid = None
    if ask is not None and (ask <= 0 or ask > 1):
        ask = None
    return bid, ask


def _is_open(market: MarketData) -> bool:
    if market.status in {"closed", "settled", "determined", "finalized"}:
        return False
    raw = market.raw_data or {}
    if raw.get("closed") is True or raw.get("active") is False:
        return False
    result = raw.get("result")
    if isinstance(result, str) and result.strip().lower() in {"yes", "no"}:
        return False
    return True


def _polymarket_event(market: MarketData) -> Optional[tuple]:
    """Return (event_id, title) for a non-augmented neg-risk outcome."""
    raw = market.raw_data or {}
    if not _truthy(raw.get("negRisk")):
        return None
    events = _parse_events(raw)
    if not events:
        return None
    event = events[0]
    if _truthy(event.get("negRiskAugmented")):
        return None
    if event.get("negRisk") is False or event.get("closed") is True:
        return None
    if event.get("active") is False:
        return None
    event_id = event.get("id") or event.get("slug") or event.get("ticker")
    if not event_id:
        return None
    title = event.get("title") or market.title
    return str(event_id), title


def _kalshi_event(market: MarketData) -> Optional[tuple]:
    """Return (event_ticker, title) only when the event is mutually exclusive."""
    raw = market.raw_data or {}
    if raw.get("mutually_exclusive") is not True:
        return None
    event_id = raw.get("event_ticker")
    if not event_id:
        return None
    title = raw.get("event_title") or market.title or str(event_id)
    return str(event_id), title


def _leg_label(market: MarketData) -> str:
    raw = market.raw_data or {}
    return (
        raw.get("groupItemTitle")
        or raw.get("yes_sub_title")
        or raw.get("subtitle")
        or market.title
        or market.id
    )


def group_exclusive_events(markets: List[MarketData]) -> List[ExclusiveEvent]:
    """Group open markets that form one exhaustive either-or event."""
    grouped: Dict[tuple, ExclusiveEvent] = {}
    seen_ids: Dict[tuple, set] = {}

    for market in markets:
        if not _is_open(market):
            continue
        if market.platform == "polymarket":
            identity = _polymarket_event(market)
        elif market.platform == "kalshi":
            identity = _kalshi_event(market)
        else:
            identity = None
        if identity is None:
            continue

        event_id, title = identity
        key = (market.platform, event_id)
        event = grouped.get(key)
        if event is None:
            event = ExclusiveEvent(
                platform=market.platform,
                event_id=event_id,
                title=title,
            )
            grouped[key] = event
            seen_ids[key] = set()
        if market.id in seen_ids[key]:
            continue
        seen_ids[key].add(market.id)
        bid, ask = outcome_quotes(market)
        event.legs.append(OutcomeLeg(
            market_id=market.id,
            label=str(_leg_label(market)),
            bid=bid,
            ask=ask,
        ))

    return [event for event in grouped.values() if len(event.legs) >= 2]


def buy_all_yes(asks: List[float], fee_rate: float, fixed_per_leg: float) -> tuple:
    """Profit from buying one Yes of each outcome. Fee uses the worst winner."""
    gross = 1.0 - sum(asks)
    fees = fee_rate * (1.0 - min(asks)) + fixed_per_leg * len(asks)
    return gross, fees, gross - fees


def sell_all_yes(bids: List[float], fee_rate: float, fixed_per_leg: float) -> tuple:
    """Profit from selling one Yes of each outcome. Fee uses the worst winner."""
    gross = sum(bids) - 1.0
    fees = fee_rate * (sum(bids) - min(bids)) + fixed_per_leg * len(bids)
    return gross, fees, gross - fees


def find_complete_set(
    event: ExclusiveEvent,
    fee_rate: float = 0.0,
    fixed_per_leg: float = 0.0,
) -> List[CompleteSetOpportunity]:
    """Return buy and sell baskets that clear the fee on this event."""
    opportunities = []
    asks = [leg.ask for leg in event.legs]
    if all(price is not None for price in asks):
        gross, fees, net = buy_all_yes(asks, fee_rate, fixed_per_leg)
        if gross > 0:
            opportunities.append(CompleteSetOpportunity(
                event=event,
                direction="buy_all_yes",
                prices=asks,
                price_sum=sum(asks),
                gross_profit=gross,
                fees=fees,
                net_profit=net,
            ))

    bids = [leg.bid for leg in event.legs]
    if all(price is not None for price in bids):
        gross, fees, net = sell_all_yes(bids, fee_rate, fixed_per_leg)
        if gross > 0:
            opportunities.append(CompleteSetOpportunity(
                event=event,
                direction="sell_all_yes",
                prices=bids,
                price_sum=sum(bids),
                gross_profit=gross,
                fees=fees,
                net_profit=net,
            ))
    return opportunities


class CompleteSetStrategy(BaseStrategy):
    """Look for exclusive events whose outcome prices do not add up to $1."""

    def __init__(self, data_manager,
                 paper_trading: bool = True,
                 max_position_size: float = None,
                 min_net_profit: float = 0.01,
                 kalshi_fee_rate: float = 0.10,
                 polymarket_cost_per_leg: float = 0.0):
        super().__init__(data_manager, paper_trading, max_position_size)
        self.min_net_profit = min_net_profit
        self.kalshi_fee_rate = kalshi_fee_rate
        self.polymarket_cost_per_leg = polymarket_cost_per_leg

    @property
    def name(self) -> str:
        return "complete_set"

    @property
    def description(self) -> str:
        return "Buy or sell every outcome when a mutually exclusive event does not add up to $1"

    def _fee_args(self, platform: str) -> tuple:
        if platform == "kalshi":
            return self.kalshi_fee_rate, 0.0
        return 0.0, self.polymarket_cost_per_leg

    def analyze(self) -> List[Signal]:
        """Scan cached markets for complete-set mispricings."""
        signals = []
        for platform in ("polymarket", "kalshi"):
            markets = self.data_manager.get_all_markets(platform)
            for event in group_exclusive_events(markets):
                fee_rate, fixed_per_leg = self._fee_args(event.platform)
                for opportunity in find_complete_set(event, fee_rate, fixed_per_leg):
                    if opportunity.is_profitable(self.min_net_profit):
                        signals.append(self._create_signal(opportunity))
        signals.sort(key=lambda signal: signal.metadata.get("net_profit", 0), reverse=True)
        return signals

    def _create_signal(self, opportunity: CompleteSetOpportunity) -> Signal:
        event = opportunity.event
        buying = opportunity.direction == "buy_all_yes"
        net = opportunity.net_profit
        if net >= 0.03:
            strength = SignalStrength.STRONG
        elif net >= 0.015:
            strength = SignalStrength.MODERATE
        else:
            strength = SignalStrength.WEAK

        action = "buy" if buying else "sell"
        legs = []
        for leg, price in zip(event.legs, opportunity.prices):
            legs.append({
                "market_id": leg.market_id,
                "label": leg.label,
                "side": "yes",
                "action": action,
                "price": price,
            })

        names = ", ".join(leg["label"] for leg in legs)
        if buying:
            reasoning = (
                f"Asks on {event.title} sum to ${opportunity.price_sum:.3f}. "
                f"Buying every Yes ({names}) costs that and pays $1. "
                f"Net ${net:.3f} per set after ${opportunity.fees:.3f} fees, "
                f"quoted from the top of each book."
            )
        else:
            reasoning = (
                f"Bids on {event.title} sum to ${opportunity.price_sum:.3f}. "
                f"Selling every Yes ({names}) collects that and owes $1. "
                f"Net ${net:.3f} per set after ${opportunity.fees:.3f} fees, "
                f"quoted from the top of each book."
            )

        return Signal(
            strategy_name=self.name,
            signal_type=SignalType.BUY if buying else SignalType.SELL,
            strength=strength,
            platform=event.platform,
            market_id=event.event_id,
            market_title=event.title,
            side="yes",
            target_price=opportunity.price_sum,
            current_price=opportunity.price_sum,
            confidence=min(0.95, 0.5 + net / 0.10),
            reasoning=reasoning,
            metadata={
                "arb_type": "complete_set",
                "direction": opportunity.direction,
                "event_id": event.event_id,
                "outcome_count": len(event.legs),
                "price_sum": opportunity.price_sum,
                "gross_profit": opportunity.gross_profit,
                "fees": opportunity.fees,
                "net_profit": net,
                "legs": legs,
            },
        )

    def generate_trade(self, signal: Signal) -> Optional[Trade]:
        """Size the basket so the cash at risk stays inside the position limit."""
        if signal.signal_type == SignalType.HOLD:
            return None
        legs = signal.metadata.get("legs") or []
        if len(legs) < 2:
            return None

        if signal.strength == SignalStrength.STRONG:
            size_multiplier = 1.0
        elif signal.strength == SignalStrength.MODERATE:
            size_multiplier = 0.6
        else:
            size_multiplier = 0.3

        budget = self.max_position_size * size_multiplier * signal.confidence
        if signal.metadata.get("direction") == "buy_all_yes":
            unit_cost = signal.metadata.get("price_sum") or signal.target_price
        else:
            unit_cost = 1.0
        if not unit_cost or unit_cost <= 0:
            return None
        quantity = int(budget / unit_cost)
        if quantity < 1:
            return None

        return Trade(
            signal=signal,
            platform=signal.platform,
            market_id=signal.market_id,
            side="yes",
            action="buy" if signal.signal_type == SignalType.BUY else "sell",
            quantity=quantity,
            price=signal.target_price,
            order_type="limit",
        )

    def execute_trade(self, trade: Trade) -> TradeResult:
        """Send the same size to every outcome. The basket is one result."""
        legs = trade.signal.metadata.get("legs") or []
        leg_results = []
        for leg in legs:
            leg_trade = Trade(
                signal=trade.signal,
                platform=trade.platform,
                market_id=leg["market_id"],
                side=leg.get("side", "yes"),
                action=leg.get("action", trade.action),
                quantity=trade.quantity,
                price=leg["price"],
                order_type="limit",
            )
            if self.paper_trading:
                leg_results.append(self._paper_trade(leg_trade))
            else:
                leg_results.append(self._real_trade(leg_trade))

        failed = [result for result in leg_results if not result.success]
        summary = TradeResult(
            trade=trade,
            success=len(leg_results) == len(legs) and not failed,
            order_id=leg_results[0].order_id if leg_results else None,
            filled_price=trade.price,
            filled_quantity=trade.quantity if not failed else 0,
            error=failed[0].error if failed else None,
        )
        summary.trade.signal.metadata["leg_results"] = [result.to_dict() for result in leg_results]
        return summary
