"""Chart series for the EDA tab, built from the saved backtest sample."""
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from src.research.backtest import (
    buy,
    rule_fade_week,
    rule_favorite_80,
    rule_follow_week,
    rule_underdog_1d,
    rule_underdog_30d,
    rule_underdog_7d,
)
from src.research.market_playbooks import PLAYBOOKS, family_for

LADDER_STRIKE = re.compile(
    r"(?:above|over|at least|or more|or higher)\s+\$?\(?"
    r"(-?\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(billion|million|thousand|bn|mn|b|m|k)?",
    re.IGNORECASE,
)
WINS_BY = re.compile(r"^(.+?)\s+wins by\b", re.IGNORECASE)
STRIKE_SCALE = {
    "b": 1_000_000_000,
    "bn": 1_000_000_000,
    "billion": 1_000_000_000,
    "m": 1_000_000,
    "mn": 1_000_000,
    "million": 1_000_000,
    "k": 1_000,
    "thousand": 1_000,
}

EST = ZoneInfo("America/New_York")
VOLUME_BANDS = (
    ("Under 10k", 0, 10_000),
    ("10k-50k", 10_000, 50_000),
    ("50k-250k", 50_000, 250_000),
    ("250k-1m", 250_000, 1_000_000),
    ("1m+", 1_000_000, float("inf")),
)
MOVE_BANDS = (
    ("Down 0.20+", -9, -0.20),
    ("Down 0.08-0.20", -0.20, -0.08),
    ("Flat", -0.08, 0.08),
    ("Up 0.08-0.20", 0.08, 0.20),
    ("Up 0.20+", 0.20, 9),
)
SUM_BANDS = (
    ("Under 0.90", 0, 0.90),
    ("0.90-0.97", 0.90, 0.97),
    ("0.97-1.03", 0.97, 1.03),
    ("1.03-1.10", 1.03, 1.10),
    ("Over 1.10", 1.10, 9),
)


def _round(value, digits=4):
    if value is None:
        return None
    return round(value, digits)


def _roi(trades):
    if not trades:
        return None
    cost = sum(trade["cost"] for trade in trades)
    if cost == 0:
        return None
    return _round(sum(trade["pnl"] for trade in trades) / cost)


def _buckets(pairs):
    rows = []
    for index in range(10):
        low = index / 10
        high = (index + 1) / 10
        chosen = [
            pair
            for pair in pairs
            if low <= pair[0] < high or (high == 1 and pair[0] == 1)
        ]
        count = len(chosen)
        if count == 0:
            rows.append(
                {
                    "label": f"{low:.1f}-{high:.1f}",
                    "midpoint": (low + high) / 2,
                    "count": 0,
                    "mean_price": None,
                    "actual": None,
                    "roi": None,
                }
            )
            continue
        cost = sum(pair[0] for pair in chosen)
        wins = sum(1 for pair in chosen if pair[1])
        priced = [buy(pair[0], pair[1]) for pair in chosen]
        priced = [trade for trade in priced if trade]
        rows.append(
            {
                "label": f"{low:.1f}-{high:.1f}",
                "midpoint": (low + high) / 2,
                "count": count,
                "mean_price": _round(cost / count),
                "actual": _round(wins / count),
                "roi": _roi(priced),
            }
        )
    return rows


def _pairs(observations, horizon):
    pairs = []
    for obs in observations:
        if obs.get("kind") != "binary":
            continue
        price = obs.get(horizon)
        if price is None or obs.get("yes_won") is None:
            continue
        pairs.append((float(price), bool(obs["yes_won"])))
    return pairs


def _topic_rows(observations):
    grouped = defaultdict(list)
    for obs in observations:
        if obs.get("kind") == "binary":
            grouped[obs.get("topic") or "other"].append(obs)
    rows = []
    for topic, items in sorted(grouped.items()):
        yes_trades = []
        underdog_trades = []
        wins = 0
        priced = 0
        for obs in items:
            price = obs.get("p1")
            if price is None:
                continue
            priced += 1
            wins += 1 if obs.get("yes_won") else 0
            trade = buy(price, obs.get("yes_won"))
            if trade:
                yes_trades.append(trade)
            underdog = rule_underdog_1d(obs)
            if underdog:
                underdog_trades.append(underdog)
        rows.append(
            {
                "topic": topic,
                "count": len(items),
                "priced": priced,
                "yes_rate": None if priced == 0 else _round(wins / priced),
                "yes_roi": _roi(yes_trades),
                "underdog_n": len(underdog_trades),
                "underdog_roi": _roi(underdog_trades),
            }
        )
    return rows


def _band_rows(observations):
    rows = []
    for label, low, high in VOLUME_BANDS:
        chosen = [
            obs
            for obs in observations
            if obs.get("kind") == "binary" and low <= float(obs.get("volume") or 0) < high
        ]
        underdog = [rule_underdog_1d(obs) for obs in chosen]
        favorite = [rule_favorite_80(obs) for obs in chosen]
        yes = []
        for obs in chosen:
            if obs.get("p1") is None:
                continue
            trade = buy(obs["p1"], obs.get("yes_won"))
            if trade:
                yes.append(trade)
        rows.append(
            {
                "label": label,
                "count": len(chosen),
                "yes_roi": _roi(yes),
                "underdog_roi": _roi([trade for trade in underdog if trade]),
                "favorite_roi": _roi([trade for trade in favorite if trade]),
                "underdog_n": sum(1 for trade in underdog if trade),
                "favorite_n": sum(1 for trade in favorite if trade),
            }
        )
    return rows


def _month_key(anchor):
    text = anchor or ""
    return text[:7]


def _monthly(observations):
    grouped = defaultdict(list)
    for obs in observations:
        if obs.get("kind") != "binary" or obs.get("p1") is None:
            continue
        grouped[_month_key(obs.get("anchor"))].append(obs)
    rows = []
    for month in sorted(grouped):
        items = grouped[month]
        wins = sum(1 for obs in items if obs.get("yes_won"))
        rows.append(
            {
                "month": month,
                "count": len(items),
                "yes_rate": _round(wins / len(items)),
                "mean_price": _round(sum(obs["p1"] for obs in items) / len(items)),
            }
        )
    return rows


def _equity(observations, rule):
    points = []
    for obs in observations:
        if obs.get("kind") != "binary":
            continue
        trade = rule(obs)
        if trade is None:
            continue
        points.append((obs.get("anchor") or "", trade["pnl"]))
    points.sort()
    by_month = defaultdict(float)
    for anchor, pnl in points:
        by_month[_month_key(anchor)] += pnl
    running = 0.0
    series = []
    for month in sorted(by_month):
        running += by_month[month]
        series.append({"month": month, "pnl": round(running, 2)})
    return series


def _buy_yes(obs):
    if obs.get("kind") != "binary" or obs.get("p1") is None:
        return None
    return buy(obs["p1"], obs.get("yes_won"))


def _moves(observations):
    rows = []
    for label, low, high in MOVE_BANDS:
        chosen = []
        for obs in observations:
            if obs.get("kind") != "binary" or obs.get("p1") is None or obs.get("p7") is None:
                continue
            delta = obs["p1"] - obs["p7"]
            if low <= delta < high:
                chosen.append(obs)
        wins = sum(1 for obs in chosen if obs.get("yes_won"))
        rows.append(
            {
                "label": label,
                "count": len(chosen),
                "yes_rate": None if not chosen else _round(wins / len(chosen)),
            }
        )
    return rows


def _price_hist(observations):
    counts = [0] * 10
    for obs in observations:
        if obs.get("kind") != "binary" or obs.get("p1") is None:
            continue
        index = min(int(obs["p1"] * 10), 9)
        counts[index] += 1
    return [
        {"label": f"{index / 10:.1f}-{(index + 1) / 10:.1f}", "count": counts[index]}
        for index in range(10)
    ]


def _quarters(months):
    grouped = defaultdict(lambda: {"count": 0, "yes": 0.0, "price": 0.0})
    for row in months:
        year, month = row["month"].split("-")
        quarter = (int(month) - 1) // 3 + 1
        key = f"{year} Q{quarter}"
        bucket = grouped[key]
        bucket["count"] += row["count"]
        bucket["yes"] += (row["yes_rate"] or 0) * row["count"]
        bucket["price"] += (row["mean_price"] or 0) * row["count"]
    rows = []
    for label in sorted(grouped):
        bucket = grouped[label]
        count = bucket["count"] or 1
        rows.append(
            {
                "label": label,
                "count": bucket["count"],
                "yes_rate": _round(bucket["yes"] / count),
                "mean_price": _round(bucket["price"] / count),
            }
        )
    return rows


def _years(observations):
    grouped = defaultdict(list)
    for obs in observations:
        if obs.get("kind") != "binary" or obs.get("p1") is None:
            continue
        grouped[(obs.get("anchor") or "")[:4]].append(obs)
    rows = []
    for year in sorted(grouped):
        if not year:
            continue
        items = grouped[year]
        errors = [(obs["p1"] - (1 if obs.get("yes_won") else 0)) ** 2 for obs in items]
        trades = [buy(obs["p1"], obs.get("yes_won")) for obs in items]
        rows.append(
            {
                "year": year,
                "count": len(items),
                "brier": _round(sum(errors) / len(errors)),
                "yes_roi": _roi([trade for trade in trades if trade]),
            }
        )
    return rows


def _baskets(observations):
    baskets = [obs for obs in observations if obs.get("kind") == "basket" and obs.get("sum_yes") is not None]
    bands = []
    for label, low, high in SUM_BANDS:
        bands.append(
            {
                "label": label,
                "count": sum(1 for obs in baskets if low <= obs["sum_yes"] < high),
            }
        )
    return {
        "n": len(baskets),
        "exactly_one": sum(1 for obs in baskets if obs.get("exactly_one")),
        "bands": bands,
    }


def _family_history(observations):
    grouped = defaultdict(list)
    for obs in observations:
        if obs.get("kind") != "binary" or obs.get("p1") is None:
            continue
        family = family_for("polymarket", obs.get("token") or "", obs.get("question") or "")
        grouped[family].append(obs)
    rows = []
    for family, items in grouped.items():
        trades = []
        wins = 0
        for obs in items:
            wins += 1 if obs.get("yes_won") else 0
            trade = buy(obs.get("p1"), obs.get("yes_won"))
            if trade:
                trades.append(trade)
        mean_price = sum(obs["p1"] for obs in items) / len(items)
        actual = wins / len(items)
        rows.append(
            {
                "family": family,
                "label": PLAYBOOKS[family]["label"],
                "count": len(items),
                "mean_price": _round(mean_price),
                "actual": _round(actual),
                "gap": _round(actual - mean_price),
                "yes_roi": _roi(trades),
            }
        )
    rows.sort(key=lambda row: row["count"], reverse=True)
    return rows


def _ladder_strike(title: str):
    match = LADDER_STRIKE.search(title or "")
    if not match:
        return None
    value = float(match.group(1).replace(",", ""))
    scale = STRIKE_SCALE.get((match.group(2) or "").lower(), 1)
    return value * scale


def _group_key(row: dict) -> str:
    title = row.get("title") or ""
    side = WINS_BY.match(title)
    side_key = side.group(1).strip().lower() if side else ""
    if row.get("platform") == "polymarket" and row.get("event_slug"):
        return f"polymarket:{row['event_slug']}:{side_key}"
    ticker = row.get("id") or ""
    parts = ticker.split("-")
    base = "-".join(parts[:-1]) if len(parts) > 1 else ticker
    return f"kalshi:{base}:{side_key}"


def ladder_breaks(rows, minimum_gap=0.04):
    """Higher 'above/over' strikes that are priced richer than a lower strike."""
    groups = defaultdict(list)
    for row in rows:
        groups[_group_key(row)].append(row)
    breaks = []
    for key, items in groups.items():
        ladder = []
        for item in items:
            strike = _ladder_strike(item.get("title") or "")
            price = item.get("yes_price")
            if strike is None or price in (None, ""):
                continue
            price = float(price)
            leg_volume = float(item.get("volume") or 0)
            if price <= 0.02 or price >= 0.98 or leg_volume < 1:
                continue
            ladder.append((strike, price, item))
        if len(ladder) < 2:
            continue
        ladder.sort(key=lambda point: point[0])
        worst = None
        for left, right in zip(ladder, ladder[1:]):
            if right[0] <= left[0]:
                continue
            gap = right[1] - left[1]
            if gap < minimum_gap:
                continue
            if worst is None or gap > worst[0]:
                worst = (gap, left, right)
        if worst is None:
            continue
        gap, left, right = worst
        volume = sum(float(item.get("volume") or 0) for item in items)
        family = family_for(left[2].get("platform") or "", left[2].get("id") or "", left[2].get("title") or "")
        breaks.append(
            {
                "family": family,
                "label": PLAYBOOKS[family]["label"],
                "group": key.split(":", 1)[-1],
                "lower_title": left[2].get("title") or left[2].get("id"),
                "lower_price": round(left[1], 4),
                "higher_title": right[2].get("title") or right[2].get("id"),
                "higher_price": round(right[1], 4),
                "gap": round(gap, 4),
                "volume": round(volume, 2),
                "contracts": len(ladder),
            }
        )
    breaks.sort(key=lambda row: (row["gap"], row["volume"]), reverse=True)
    return breaks[:40]


def open_family_shape(rows):
    grouped = defaultdict(list)
    for row in rows:
        family = family_for(row.get("platform") or "", row.get("id") or "", row.get("title") or "")
        grouped[family].append(row)
    summary = []
    for family, items in grouped.items():
        priced = [float(item["yes_price"]) for item in items if item.get("yes_price") not in (None, "")]
        cheap = sum(1 for price in priced if price < 0.15)
        summary.append(
            {
                "family": family,
                "label": PLAYBOOKS[family]["label"],
                "markets": len(items),
                "priced": len(priced),
                "cheap_share": None if not priced else round(cheap / len(priced), 4),
                "volume": round(sum(float(item.get("volume") or 0) for item in items), 2),
            }
        )
    summary.sort(key=lambda row: row["markets"], reverse=True)
    return summary


def build_charts(observations, favorites=None, backtests=None):
    binary = [obs for obs in observations if obs.get("kind") == "binary"]
    return {
        "generated_at_est": datetime.now(EST).strftime("%b %d, %Y %I:%M %p EST"),
        "sample": {
            "binary": len(binary),
            "p1": len(_pairs(observations, "p1")),
            "p7": len(_pairs(observations, "p7")),
            "p30": len(_pairs(observations, "p30")),
            "baskets": sum(1 for obs in observations if obs.get("kind") == "basket"),
        },
        "calibration": {
            "1d": _buckets(_pairs(observations, "p1")),
            "7d": _buckets(_pairs(observations, "p7")),
            "30d": _buckets(_pairs(observations, "p30")),
        },
        "favorite_buckets": (favorites or {}).get("buckets") or [],
        "favorite_summary": {
            "observations": (favorites or {}).get("observations"),
            "brier": (favorites or {}).get("brier"),
            "favorite_roi": (favorites or {}).get("favorite_roi"),
            "favorite_win_rate": (favorites or {}).get("favorite_win_rate"),
            "favorite_mean_price": (favorites or {}).get("favorite_mean_price"),
        },
        "topics": _topic_rows(observations),
        "families": _family_history(observations),
        "volume_bands": _band_rows(observations),
        "months": _monthly(observations),
        "quarters": _quarters(_monthly(observations)),
        "price_hist": _price_hist(observations),
        "moves": _moves(observations),
        "years": _years(observations),
        "baskets": _baskets(observations),
        "equity": {
            "buy_yes": _equity(observations, _buy_yes),
            "underdog_1d": _equity(observations, rule_underdog_1d),
            "underdog_7d": _equity(observations, rule_underdog_7d),
            "underdog_30d": _equity(observations, rule_underdog_30d),
            "favorite_80": _equity(observations, rule_favorite_80),
            "follow_week": _equity(observations, rule_follow_week),
            "fade_week": _equity(observations, rule_fade_week),
        },
        "strategies": (backtests or {}).get("strategies") or [],
        "backtest_rule": (backtests or {}).get("rule"),
        "backtest_built": (backtests or {}).get("generated_at_est"),
    }


def load_chart_payload(eda_dir: Path):
    observations_path = eda_dir / "backtest_observations.json"
    if not observations_path.exists():
        return None
    observations = json.loads(observations_path.read_text(encoding="utf-8"))
    favorites_path = eda_dir / "favorite_calibration.json"
    backtests_path = eda_dir / "strategy_backtests.json"
    favorites = json.loads(favorites_path.read_text(encoding="utf-8")) if favorites_path.exists() else None
    backtests = json.loads(backtests_path.read_text(encoding="utf-8")) if backtests_path.exists() else None
    return build_charts(observations, favorites, backtests)
