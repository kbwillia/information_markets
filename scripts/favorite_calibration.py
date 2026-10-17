"""Calibration of Polymarket prices: implied probability vs what actually happened.

The price used as the prediction is the last CLOB trade at least 24 hours before
the earlier of the market end time and the close time. Post-resolution prints
at 0 or 1 are not treated as forecasts.
"""
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "eda" / "favorite_calibration.json"
GAMMA = "https://gamma-api.polymarket.com/markets"
CLOB = "https://clob.polymarket.com/prices-history"
BUCKETS = [(i / 10, (i + 1) / 10) for i in range(10)]
MIN_VOLUME = 5000
MAX_MARKETS = 6000
WORKERS = 10


def parse_time(value):
    if not value:
        return None
    text = str(value).strip().replace("Z", "+00:00")
    if " " in text and "T" not in text:
        text = text.replace(" ", "T")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def parse_list(value):
    if isinstance(value, list):
        return value
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return []
    return parsed if isinstance(parsed, list) else []


def fetch_market_pages():
    """Page closed markets by end-date month.

    The list endpoint rejects offsets past 2,000, so one global sort cannot
    reach past the largest markets. Each month gets its own offset budget.
    """
    session = requests.Session()
    markets = []
    seen = set()
    cursor = datetime(2023, 1, 1, tzinfo=timezone.utc)
    stop = datetime(2026, 11, 1, tzinfo=timezone.utc)
    while cursor < stop and len(markets) < MAX_MARKETS:
        nxt = datetime(cursor.year + (cursor.month == 12), cursor.month % 12 + 1, 1, tzinfo=timezone.utc)
        offset = 0
        while offset <= 2000 and len(markets) < MAX_MARKETS:
            response = None
            for attempt in range(6):
                response = session.get(
                    GAMMA,
                    params={
                        "closed": "true",
                        "limit": 100,
                        "offset": offset,
                        "order": "volumeNum",
                        "ascending": "false",
                        "end_date_min": cursor.strftime("%Y-%m-%dT00:00:00Z"),
                        "end_date_max": nxt.strftime("%Y-%m-%dT00:00:00Z"),
                    },
                    timeout=40,
                )
                if response.status_code == 429:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                break
            if response.status_code == 422:
                break
            response.raise_for_status()
            batch = response.json()
            if not batch:
                break
            for market in batch:
                volume = market.get("volumeNum") or 0
                try:
                    volume = float(volume)
                except (TypeError, ValueError):
                    volume = 0
                if volume < MIN_VOLUME:
                    continue
                key = market.get("conditionId") or market.get("id")
                if key in seen:
                    continue
                seen.add(key)
                markets.append(market)
            offset += len(batch)
            if len(batch) < 100:
                break
            time.sleep(0.08)
        print(f"through {cursor.strftime('%Y-%m')} scanned {len(markets)}", flush=True)
        cursor = nxt
    return markets[:MAX_MARKETS]


def eligible(market):
    outcomes = parse_list(market.get("outcomes"))
    prices = parse_list(market.get("outcomePrices"))
    tokens = parse_list(market.get("clobTokenIds"))
    if len(outcomes) != 2 or len(prices) != 2 or len(tokens) < 1:
        return None
    try:
        settled = [float(prices[0]), float(prices[1])]
    except (TypeError, ValueError):
        return None
    if max(settled) < 0.99 or min(settled) > 0.01:
        return None
    volume = market.get("volumeNum") or 0
    try:
        volume = float(volume)
    except (TypeError, ValueError):
        volume = 0
    if volume < MIN_VOLUME:
        return None
    end = parse_time(market.get("endDate"))
    closed = parse_time(market.get("closedTime"))
    anchors = [item for item in (end, closed) if item is not None]
    if not anchors:
        return None
    return {
        "question": market.get("question") or "",
        "token": str(tokens[0]),
        "yes_won": settled[0] >= 0.99,
        "volume": volume,
        "anchor": min(anchors),
    }


def snapshot_price(item):
    cutoff = item["anchor"].timestamp() - 24 * 3600
    for attempt in range(3):
        try:
            response = requests.get(
                CLOB,
                params={"market": item["token"], "interval": "max", "fidelity": 720},
                timeout=30,
            )
            if response.status_code == 429:
                time.sleep(1.5 * (attempt + 1))
                continue
            response.raise_for_status()
            history = response.json().get("history") or []
            break
        except requests.RequestException:
            time.sleep(0.4 * (attempt + 1))
    else:
        return None
    prior = [point for point in history if point.get("t", 0) <= cutoff]
    if not prior:
        return None
    price = float(prior[-1]["p"])
    if price <= 0.01 or price >= 0.99:
        return None
    return price


def bucket_index(price):
    if price >= 1:
        return 9
    return min(int(price * 10), 9)


def main():
    raw = fetch_market_pages()
    candidates = [item for item in (eligible(market) for market in raw) if item]
    observations = []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(snapshot_price, item): item for item in candidates}
        done = 0
        for future in as_completed(futures):
            done += 1
            item = futures[future]
            price = future.result()
            if price is None:
                continue
            observations.append(
                {
                    "question": item["question"],
                    "price": round(price, 4),
                    "yes_won": item["yes_won"],
                    "volume": round(item["volume"], 2),
                }
            )
            if done % 100 == 0:
                print(f"priced {done}/{len(candidates)} kept {len(observations)}", flush=True)

    buckets = []
    for low, high in BUCKETS:
        rows = [row for row in observations if low <= row["price"] < high or (high == 1 and row["price"] == 1)]
        wins = sum(1 for row in rows if row["yes_won"])
        count = len(rows)
        actual = (wins / count) if count else None
        midpoint = (low + high) / 2
        cost = sum(row["price"] for row in rows)
        payout = float(wins)
        pnl = payout - cost
        buckets.append(
            {
                "low": low,
                "high": high,
                "label": f"{low:.1f}-{high:.1f}",
                "midpoint": midpoint,
                "count": count,
                "wins": wins,
                "actual": None if actual is None else round(actual, 4),
                "mean_price": None if count == 0 else round(cost / count, 4),
                "pnl_per_share": None if count == 0 else round(pnl, 2),
                "roi": None if not cost else round(pnl / cost, 4),
            }
        )

    favorite_rows = []
    for row in observations:
        favorite_price = row["price"] if row["price"] >= 0.5 else 1 - row["price"]
        favorite_won = row["yes_won"] if row["price"] >= 0.5 else not row["yes_won"]
        favorite_rows.append((favorite_price, favorite_won))
    favorite_cost = sum(price for price, _ in favorite_rows)
    favorite_wins = sum(1 for _, won in favorite_rows if won)
    favorite_pnl = favorite_wins - favorite_cost

    priced = [row for row in observations]
    brier = (
        sum((row["price"] - (1 if row["yes_won"] else 0)) ** 2 for row in priced) / len(priced)
        if priced
        else None
    )
    payload = {
        "source": "Polymarket Gamma closed markets plus CLOB price history",
        "rule": "Last trade at least 24 hours before the earlier of end date and close time. Resolved binary markets with volume of at least 5,000, taken from each month from Jan 2023 through Oct 2026.",
        "scanned": len(raw),
        "candidates": len(candidates),
        "observations": len(observations),
        "brier": None if brier is None else round(brier, 4),
        "favorite_bets": len(favorite_rows),
        "favorite_wins": favorite_wins,
        "favorite_win_rate": None if not favorite_rows else round(favorite_wins / len(favorite_rows), 4),
        "favorite_mean_price": None if not favorite_rows else round(favorite_cost / len(favorite_rows), 4),
        "favorite_pnl": None if not favorite_rows else round(favorite_pnl, 2),
        "favorite_roi": None if not favorite_cost else round(favorite_pnl / favorite_cost, 4),
        "buckets": buckets,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({k: payload[k] for k in payload if k != "buckets"}, indent=2))
    print(json.dumps(buckets, indent=2))


if __name__ == "__main__":
    main()
