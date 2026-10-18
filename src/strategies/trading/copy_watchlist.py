"""Straight-copy recent fills from followed (or investigated) top accounts."""
from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Any, Dict, List

import requests

from src.research.top_accounts import DATA_API, TOP_ACCOUNTS_PATH, load_watchlist
from src.strategies.trading.base import BaseStrategy, Signal, SignalStrength, SignalType


def _as_list(payload: Any) -> List[Dict]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("data", "activity", "trades", "results"):
            rows = payload.get(key)
            if isinstance(rows, list):
                return [row for row in rows if isinstance(row, dict)]
    return []


def _parse_time(value: Any) -> datetime | None:
    if value is None:
        return None
    try:
        if isinstance(value, (int, float)):
            stamp = float(value)
            if stamp > 1e12:
                stamp /= 1000.0
            return datetime.fromtimestamp(stamp)
        text = str(value).replace("Z", "+00:00")
        return datetime.fromisoformat(text).replace(tzinfo=None)
    except (TypeError, ValueError, OSError):
        return None


def _side_from_activity(row: Dict) -> str:
    outcome = str(row.get("outcome") or row.get("outcomeName") or "").strip().lower()
    if outcome.startswith("no") or "under" in outcome:
        return "no"
    if outcome.startswith("yes") or "over" in outcome:
        return "yes"
    raw = str(row.get("outcomeIndex") or "0")
    return "no" if str(raw) in {"1", "no"} else "yes"


def _action_from_activity(row: Dict) -> str:
    raw = str(row.get("side") or row.get("type") or "buy").strip().lower()
    if raw in {"sell", "sold"}:
        return "sell"
    return "buy"


class CopyWatchlistStrategy(BaseStrategy):
    """Mirror TRADE activity from the copy watchlist with almost no filters."""

    def __init__(
        self,
        data_manager,
        paper_trading: bool = True,
        max_position_size: float = None,
        lookback_hours: int = 12,
        max_accounts: int = 8,
        max_fills_per_account: int = 8,
    ):
        super().__init__(data_manager, paper_trading, max_position_size)
        self.lookback_hours = lookback_hours
        self.max_accounts = max_accounts
        self.max_fills_per_account = max_fills_per_account
        self._seen: set[str] = set()

    @property
    def name(self) -> str:
        return "copy_watchlist"

    @property
    def description(self) -> str:
        return "Straight-copy recent buys and sells from followed top accounts"

    def _source_accounts(self) -> List[Dict[str, Any]]:
        watch = load_watchlist()
        rows = [
            item
            for item in watch.get("accounts") or []
            if item.get("enabled", True) and (item.get("address") or "").strip()
        ]
        if rows:
            return rows[: self.max_accounts]
        if not TOP_ACCOUNTS_PATH.exists():
            return []
        try:
            payload = json.loads(TOP_ACCOUNTS_PATH.read_text(encoding="utf-8"))
        except Exception:
            return []
        investigated = list(payload.get("accounts") or [])
        investigated.sort(
            key=lambda acc: float((acc.get("llm_analysis") or {}).get("copyability_score") or 0),
            reverse=True,
        )
        return [
            {
                "address": acc.get("address"),
                "user_name": acc.get("user_name") or (acc.get("address") or "")[:10],
            }
            for acc in investigated[: self.max_accounts]
            if acc.get("address")
        ]

    def _recent_trades(self, address: str) -> List[Dict]:
        try:
            payload = requests.get(
                f"{DATA_API}/activity",
                params={"user": address, "limit": 40},
                timeout=12,
            )
            payload.raise_for_status()
            rows = _as_list(payload.json())
        except Exception:
            return []
        cutoff = datetime.now() - timedelta(hours=self.lookback_hours)
        trades = []
        for row in rows:
            kind = str(row.get("type") or row.get("activityType") or "").lower()
            if kind not in {"trade", "buy", "sell"}:
                continue
            when = _parse_time(row.get("timestamp") or row.get("createdAt") or row.get("time"))
            if when and when < cutoff:
                continue
            trades.append(row)
        return trades[: self.max_fills_per_account]

    def analyze(self) -> List[Signal]:
        signals: List[Signal] = []
        for acc in self._source_accounts():
            address = str(acc.get("address") or "").strip().lower()
            name = acc.get("user_name") or address[:10]
            if not address:
                continue
            for row in self._recent_trades(address):
                condition_id = str(row.get("conditionId") or row.get("condition_id") or row.get("asset") or "")
                if not condition_id:
                    continue
                stamp = row.get("timestamp") or row.get("createdAt") or row.get("transactionHash") or ""
                key = f"{address}:{condition_id}:{stamp}:{row.get('side')}:{row.get('outcome')}"
                if key in self._seen:
                    continue
                self._seen.add(key)
                price = row.get("price") or row.get("avgPrice")
                try:
                    price = float(price)
                except (TypeError, ValueError):
                    continue
                if price <= 0 or price >= 1:
                    continue
                side = _side_from_activity(row)
                action = _action_from_activity(row)
                title = row.get("title") or row.get("slug") or condition_id
                trader_label = str(name)
                signals.append(
                    Signal(
                        strategy_name=self.name,
                        signal_type=SignalType.BUY if action == "buy" else SignalType.SELL,
                        strength=SignalStrength.STRONG,
                        platform="polymarket",
                        market_id=condition_id,
                        market_title=str(title)[:140],
                        side=side,
                        target_price=price,
                        current_price=price,
                        confidence=1.0,
                        reasoning=f"Straight copy of {trader_label} {action} {side} @ {price:.2f}",
                        metadata={
                            "copied_account": trader_label,
                            "trader_name": trader_label,
                            "trader_address": address,
                            "source": "watchlist_fill",
                            "activity_timestamp": stamp,
                        },
                    )
                )
        return signals
