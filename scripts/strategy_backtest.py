"""Backtest entry rules on resolved Polymarket markets.

Binary markets are entered from the last trade before a horizon and held to
resolution. Multi-outcome events are priced the same way, one print per outcome,
and tested as a complete set. Train is everything before 2025-07-01. Test is
everything after that.
"""
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.research.backtest import CUTOFF, score_rules, topic_of

OUT = ROOT / "data" / "eda" / "strategy_backtests.json"
CACHE = ROOT / "data" / "eda" / "backtest_observations.json"
GAMMA = "https://gamma-api.polymarket.com"
CLOB = "https://clob.polymarket.com/prices-history"
MIN_VOLUME = 5000
MAX_PER_MONTH = 40
MAX_EVENTS = 220
WORKERS = 8
HISTORY_CACHE = ROOT / "data" / "eda" / "price_histories.jsonl"
EST = ZoneInfo("America/New_York")


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


def get_json(session, url, params):
    for attempt in range(6):
        try:
            response = session.get(url, params=params, timeout=40)
        except requests.RequestException:
            time.sleep(0.4 * (attempt + 1))
            continue
        if response.status_code == 429:
            time.sleep(1.5 * (attempt + 1))
            continue
        if response.status_code == 422:
            return []
        response.raise_for_status()
        return response.json()
    return []


def month_starts():
    cursor = datetime(2023, 1, 1, tzinfo=timezone.utc)
    stop = datetime(2026, 11, 1, tzinfo=timezone.utc)
    while cursor < stop:
        nxt = datetime(cursor.year + (cursor.month == 12), cursor.month % 12 + 1, 1, tzinfo=timezone.utc)
        yield cursor, nxt
        cursor = nxt


def fetch_markets(session):
    markets = []
    seen = set()
    for start, end in month_starts():
        offset = 0
        month_count = 0
        while offset <= 2000 and month_count < MAX_PER_MONTH:
            batch = get_json(
                session,
                f"{GAMMA}/markets",
                {
                    "closed": "true",
                    "limit": 100,
                    "offset": offset,
                    "order": "volumeNum",
                    "ascending": "false",
                    "end_date_min": start.strftime("%Y-%m-%dT00:00:00Z"),
                    "end_date_max": end.strftime("%Y-%m-%dT00:00:00Z"),
                },
            )
            if not isinstance(batch, list) or not batch:
                break
            for market in batch:
                volume = _volume(market)
                if volume < MIN_VOLUME:
                    continue
                key = market.get("conditionId") or market.get("id")
                if key in seen:
                    continue
                seen.add(key)
                markets.append(market)
                month_count += 1
                if month_count >= MAX_PER_MONTH:
                    break
            offset += len(batch)
            if len(batch) < 100:
                break
            time.sleep(0.05)
        print(f"markets through {start.strftime('%Y-%m')}: {len(markets)}", flush=True)
    return markets


def fetch_events(session):
    events = []
    seen = set()
    for start, end in month_starts():
        offset = 0
        month_kept = 0
        while offset <= 500 and month_kept < 4 and len(events) < MAX_EVENTS:
            batch = get_json(
                session,
                f"{GAMMA}/events",
                {
                    "closed": "true",
                    "limit": 50,
                    "offset": offset,
                    "order": "volume",
                    "ascending": "false",
                    "end_date_min": start.strftime("%Y-%m-%dT00:00:00Z"),
                    "end_date_max": end.strftime("%Y-%m-%dT00:00:00Z"),
                },
            )
            if not batch:
                break
            if not isinstance(batch, list):
                break
            for event in batch:
                markets = event.get("markets") or []
                if len(markets) < 3 or len(markets) > 40:
                    continue
                key = event.get("id")
                if key in seen:
                    continue
                seen.add(key)
                events.append(event)
                month_kept += 1
                if month_kept >= 4 or len(events) >= MAX_EVENTS:
                    break
            offset += len(batch)
            if len(batch) < 50:
                break
            time.sleep(0.05)
        print(f"events through {start.strftime('%Y-%m')}: {len(events)}", flush=True)
    return events


def _volume(market):
    raw = market.get("volumeNum")
    if raw is None:
        raw = market.get("volume") or 0
    try:
        return float(raw)
    except (TypeError, ValueError):
        return 0.0


def binary_candidate(market):
    outcomes = parse_list(market.get("outcomes"))
    prices = parse_list(market.get("outcomePrices"))
    tokens = parse_list(market.get("clobTokenIds"))
    if len(outcomes) != 2 or len(prices) != 2 or not tokens:
        return None
    try:
        settled = [float(prices[0]), float(prices[1])]
    except (TypeError, ValueError):
        return None
    if max(settled) < 0.99 or min(settled) > 0.01:
        return None
    end = parse_time(market.get("endDate"))
    closed = parse_time(market.get("closedTime"))
    anchors = [item for item in (end, closed) if item is not None]
    if not anchors:
        return None
    return {
        "kind": "binary",
        "question": market.get("question") or "",
        "token": str(tokens[0]),
        "yes_won": settled[0] >= 0.99,
        "volume": _volume(market),
        "anchor": min(anchors).isoformat(),
        "topic": topic_of(market.get("question") or ""),
    }


def event_candidates(event):
    markets = []
    for market in event.get("markets") or []:
        item = binary_candidate(market)
        if item is None:
            return None
        item["event_id"] = str(event.get("id"))
        item["event_title"] = event.get("title") or ""
        markets.append(item)
    if len(markets) < 3:
        return None
    return markets


def load_history_cache():
    cached = {}
    if not HISTORY_CACHE.exists():
        return cached
    for line in HISTORY_CACHE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        points = row["points"]
        if points and isinstance(points[0], list):
            points = [{"t": point[0], "p": point[1]} for point in points]
        cached[row["token"]] = points
    return cached


def history_for(token):
    for attempt in range(4):
        try:
            response = requests.get(
                CLOB,
                params={"market": token, "interval": "max", "fidelity": 720},
                timeout=30,
            )
        except requests.RequestException:
            time.sleep(0.4 * (attempt + 1))
            continue
        if response.status_code == 429:
            time.sleep(1.5 * (attempt + 1))
            continue
        if response.status_code >= 400:
            return []
        points = response.json().get("history") or []
        points = [point for point in points if "t" in point and "p" in point]
        points.sort(key=lambda point: point["t"])
        return points
    return []


def price_before(points, cutoff_ts, max_age_seconds):
    prior = [point for point in points if point["t"] <= cutoff_ts]
    if not prior:
        return None
    last = prior[-1]
    if cutoff_ts - last["t"] > max_age_seconds:
        return None
    price = float(last["p"])
    if price <= 0.01 or price >= 0.99:
        return None
    return price


def attach_prices(candidates):
    tokens = sorted({item["token"] for item in candidates})
    histories = load_history_cache()
    missing = [token for token in tokens if token not in histories]
    print(f"histories cached {len(tokens) - len(missing)} missing {len(missing)}", flush=True)
    lock = threading.Lock()
    HISTORY_CACHE.parent.mkdir(parents=True, exist_ok=True)
    with HISTORY_CACHE.open("a", encoding="utf-8") as handle:
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futures = {pool.submit(history_for, token): token for token in missing}
            done = 0
            for future in as_completed(futures):
                done += 1
                token = futures[future]
                points = future.result()
                histories[token] = points
                compact = [[point["t"], point["p"]] for point in points]
                with lock:
                    handle.write(json.dumps({"token": token, "points": compact}) + "\n")
                    handle.flush()
                if done % 100 == 0:
                    print(f"histories {done}/{len(missing)}", flush=True)
    day = 24 * 3600
    windows = (("p1", 1 * day, 2 * day), ("p7", 7 * day, 4 * day), ("p30", 30 * day, 10 * day))
    observations = []
    for item in candidates:
        anchor = parse_time(item["anchor"])
        if anchor is None:
            continue
        points = histories.get(item["token"]) or []
        priced = dict(item)
        for key, lead, max_age in windows:
            priced[key] = price_before(points, anchor.timestamp() - lead, max_age)
        if priced["p1"] is None and priced["p7"] is None and priced["p30"] is None:
            continue
        observations.append(priced)
    return observations


def baskets_from(priced_markets):
    grouped = {}
    for item in priced_markets:
        grouped.setdefault(item["event_id"], []).append(item)
    baskets = []
    for event_id, legs in grouped.items():
        usable = [leg for leg in legs if leg.get("p1") is not None]
        if len(usable) != len(legs):
            continue
        winners = sum(1 for leg in usable if leg["yes_won"])
        cheapest = min(usable, key=lambda leg: leg["p1"])
        baskets.append(
            {
                "kind": "basket",
                "event_id": event_id,
                "question": usable[0].get("event_title") or "",
                "anchor": min(leg["anchor"] for leg in usable),
                "n_legs": len(usable),
                "sum_yes": round(sum(leg["p1"] for leg in usable), 4),
                "exactly_one": winners == 1,
                "cheapest": cheapest["p1"],
                "cheapest_won": cheapest["yes_won"],
                "volume": round(sum(leg["volume"] for leg in usable), 2),
            }
        )
    return baskets


def main():
    session = requests.Session()
    raw_markets = fetch_markets(session)
    binary = [item for item in (binary_candidate(market) for market in raw_markets) if item]
    print(f"binary candidates {len(binary)}", flush=True)
    binary_obs = attach_prices(binary)

    raw_events = fetch_events(session)
    event_markets = []
    for event in raw_events:
        legs = event_candidates(event)
        if legs:
            event_markets.extend(legs)
    print(f"event legs {len(event_markets)}", flush=True)
    event_obs = attach_prices(event_markets) if event_markets else []
    basket_obs = baskets_from(event_obs)

    observations = binary_obs + basket_obs
    generated = datetime.now(EST).strftime("%b %d, %Y %I:%M %p EST")
    payload = {
        "generated_at_est": generated,
        "source": "Polymarket closed markets and neg-risk events, CLOB price history",
        "cutoff": CUTOFF,
        "slippage": 0.01,
        "binary_markets": len(binary_obs),
        "events": len(basket_obs),
        "rule": "Train is an anchor date before 2025-07-01. Test is on or after that date. A kept rule made money in both samples with at least 40 trades each, after 0.01 slippage per share.",
        "strategies": score_rules(observations),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(observations), encoding="utf-8")
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    kept = [row["name"] for row in payload["strategies"] if row["kept"]]
    print(json.dumps({"binary": len(binary_obs), "events": len(basket_obs), "kept": kept}, indent=2))
    for row in payload["strategies"]:
        test = row["test"]
        print(f"{row['name']:20} train {row['train']['n']:5} {row['train']['roi']}  test {test['n']:5} {test['roi']}  kept {row['kept']}")


if __name__ == "__main__":
    main()
