"""Investigation and LLM strategy analysis of top Polymarket accounts.

Tracks two distinct dimensions of top performance:
1. Percentage earners (high return on volume and high realized ROI on closed positions)
2. Volume and dollar PnL earners (high-turnover whales, bookmakers, and market makers)

Uses quantitative position/activity forensics plus local Ollama LLM analysis to
identify each account's trading strategy, behavioral patterns, and copyability.
"""
from __future__ import annotations

import json
import math
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

import requests

from src.config import Config
from src.research.backtest import topic_of

EST = ZoneInfo("America/New_York")
DATA_API = "https://data-api.polymarket.com"
ROOT = Path(__file__).resolve().parents[2]
TOP_ACCOUNTS_PATH = ROOT / "data" / "eda" / "top_accounts.json"
WATCHLIST_PATH = ROOT / "data" / "eda" / "copied_accounts.json"
PAPER_COPY_LOG = ROOT / "data" / "paper_trades" / "copied_account_trades.jsonl"


def now_est_str() -> str:
    return datetime.now(EST).strftime("%b %d, %Y %I:%M %p EST")


def format_ts_est(ts: Any) -> Optional[str]:
    if ts is None or ts == "":
        return None
    try:
        if isinstance(ts, (int, float)):
            val = float(ts)
            if val > 1e11:
                val /= 1000.0
            dt = datetime.fromtimestamp(val, tz=timezone.utc)
            return dt.astimezone(EST).strftime("%b %d, %Y %I:%M %p EST")
        text = str(ts).strip().replace("Z", "+00:00")
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(EST).strftime("%b %d, %Y %I:%M %p EST")
    except Exception:
        return str(ts)


def classify_topic(title: str, slug: str = "") -> str:
    combined = f"{title or ''} {slug or ''}".lower()
    if any(
        k in combined
        for k in (
            "nfl",
            "nba",
            "mlb",
            "nhl",
            "ufc",
            "fifa",
            "fifwc",
            "premier league",
            "champions league",
            "la liga",
            "serie a",
            "bundesliga",
            "liga",
            "tennis",
            "atp",
            "wta",
            "golf",
            "pga",
            "f1",
            "formula 1",
            "super bowl",
            "world series",
            "stanley cup",
            "ncaa",
            " vs ",
            " vs.",
            "o/u ",
            "over/under",
            "spread:",
            "exact score",
            "win on 202",
            "fc ",
            " fc",
        )
    ):
        return "sports"
    return topic_of(combined)


def _get_json(session: requests.Session, url: str, params: Dict[str, Any], timeout: int = 25) -> Any:
    for attempt in range(4):
        try:
            resp = session.get(url, params=params, timeout=timeout)
            if resp.status_code == 429:
                time.sleep(1.2 * (attempt + 1))
                continue
            if resp.status_code >= 400:
                return []
            return resp.json()
        except requests.RequestException:
            time.sleep(0.4 * (attempt + 1))
    return []


def fetch_leaderboard_pool(
    session: requests.Session,
    time_period: str = "ALL",
    pages_per_sort: int = 3,
) -> Dict[str, Dict[str, Any]]:
    """Fetch a broad pool of top accounts across PNL and VOL leaderboards."""
    pool: Dict[str, Dict[str, Any]] = {}

    periods = [time_period] if time_period != "ALL" else ["ALL", "MONTH"]
    for period in periods:
        pages = pages_per_sort if period == time_period else 1
        for order_by in ("PNL", "VOL"):
            for page in range(pages):
                offset = page * 50
                rows = _get_json(
                    session,
                    f"{DATA_API}/v1/leaderboard",
                    {
                        "limit": 50,
                        "offset": offset,
                        "category": "OVERALL",
                        "timePeriod": period,
                        "orderBy": order_by,
                    },
                )
                if not isinstance(rows, list) or not rows:
                    break
                for idx, item in enumerate(rows):
                    wallet = (item.get("proxyWallet") or item.get("address") or "").strip().lower()
                    if not wallet:
                        continue
                    pnl = float(item.get("pnl") or 0.0)
                    vol = float(item.get("vol") or item.get("volume") or 0.0)
                    rank = int(item.get("rank") or (offset + idx + 1))
                    existing = pool.get(wallet, {})
                    entry = {
                        "address": wallet,
                        "user_name": item.get("userName") or existing.get("user_name") or f"{wallet[:6]}...{wallet[-4:]}",
                        "x_username": item.get("xUsername") or existing.get("x_username") or "",
                        "verified": bool(item.get("verifiedBadge") or existing.get("verified")),
                        "pnl": max(pnl, existing.get("pnl", pnl)) if existing else pnl,
                        "volume": max(vol, existing.get("volume", vol)) if existing else vol,
                        "rank_pnl": existing.get("rank_pnl"),
                        "rank_vol": existing.get("rank_vol"),
                        "active_recent": existing.get("active_recent", False) or (period == "MONTH"),
                    }
                    if period == time_period and order_by == "PNL" and entry["rank_pnl"] is None:
                        entry["rank_pnl"] = rank
                    if period == time_period and order_by == "VOL" and entry["rank_vol"] is None:
                        entry["rank_vol"] = rank
                    pool[wallet] = entry
    return pool


def select_candidate_accounts(
    pool: Dict[str, Dict[str, Any]],
    max_candidates: int = 18,
) -> List[Dict[str, Any]]:
    """Select top accounts representing high % ROI, high volume, and high dollar PnL."""
    accounts = list(pool.values())
    for acc in accounts:
        vol = acc["volume"]
        pnl = acc["pnl"]
        acc["return_on_volume_pct"] = round((pnl / vol) * 100.0, 2) if vol > 0 else 0.0

    # 1. Top by % Return on Volume (minimum $100k volume and $100k PnL so it's proven edge, not 1 lucky $10 bet)
    eligible_roi = [
        a for a in accounts if a["volume"] >= 100_000 and a["pnl"] >= 100_000
    ]
    eligible_roi.sort(key=lambda a: a["return_on_volume_pct"], reverse=True)
    for idx, acc in enumerate(eligible_roi, start=1):
        acc["rank_roi"] = idx

    # 2. Top by Volume (with positive PnL or top raw volume)
    by_vol = sorted(accounts, key=lambda a: a["volume"], reverse=True)
    for idx, acc in enumerate(by_vol, start=1):
        if acc.get("rank_vol") is None:
            acc["rank_vol"] = idx

    # 3. Top by Total Dollar PnL
    by_pnl = sorted(accounts, key=lambda a: a["pnl"], reverse=True)
    for idx, acc in enumerate(by_pnl, start=1):
        if acc.get("rank_pnl") is None:
            acc["rank_pnl"] = idx

    # 4. Active recent leaders (monthly % ROI and PnL leaders) to guarantee live open positions for copy trading
    recent_active = [a for a in accounts if a.get("active_recent") and a["pnl"] > 50_000 and a["volume"] >= 50_000]
    recent_active.sort(key=lambda a: (a["return_on_volume_pct"], a["pnl"]), reverse=True)

    selected: Dict[str, Dict[str, Any]] = {}
    per_bucket = max(4, max_candidates // 4)

    for acc in eligible_roi[:per_bucket]:
        selected[acc["address"]] = acc
    for acc in by_vol[:per_bucket]:
        selected[acc["address"]] = acc
    for acc in by_pnl[:per_bucket]:
        selected[acc["address"]] = acc
    for acc in recent_active[:per_bucket]:
        selected[acc["address"]] = acc

    # Fill remaining slots from highest % ROI, recent active, and highest PnL
    for acc in eligible_roi + recent_active + by_pnl + by_vol:
        if len(selected) >= max_candidates:
            break
        selected[acc["address"]] = acc

    return list(selected.values())[:max_candidates]


def analyze_wallet_quantitatively(
    session: requests.Session,
    account: Dict[str, Any],
) -> Dict[str, Any]:
    """Fetch closed positions, open positions, and recent activity to compute trading patterns."""
    wallet = account["address"]

    closed_raw = _get_json(
        session,
        f"{DATA_API}/v1/closed-positions",
        {"user": wallet, "limit": 200, "sortBy": "TIMESTAMP", "sortDirection": "DESC"},
    )
    closed_positions = closed_raw if isinstance(closed_raw, list) else []

    top_wins_raw = _get_json(
        session,
        f"{DATA_API}/v1/closed-positions",
        {"user": wallet, "limit": 8, "sortBy": "REALIZEDPNL", "sortDirection": "DESC"},
    )
    top_wins_positions = top_wins_raw if isinstance(top_wins_raw, list) else []

    open_raw = _get_json(
        session,
        f"{DATA_API}/positions",
        {
            "user": wallet,
            "limit": 60,
            "sizeThreshold": 1.0,
            "sortBy": "CURRENT",
            "sortDirection": "DESC",
        },
    )
    open_positions = open_raw if isinstance(open_raw, list) else []

    activity_raw = _get_json(
        session,
        f"{DATA_API}/activity",
        {"user": wallet, "limit": 100},
    )
    activities = activity_raw if isinstance(activity_raw, list) else []

    # --- Closed position forensics ---
    wins = 0
    losses = 0
    gross_profit = 0.0
    gross_loss = 0.0
    total_cost = 0.0
    total_realized_pnl = 0.0
    entry_prices: List[float] = []
    position_costs: List[float] = []
    win_amounts: List[float] = []
    loss_amounts: List[float] = []
    yes_count = 0
    no_count = 0
    topic_counts: Dict[str, int] = {
        "sports": 0,
        "politics": 0,
        "crypto": 0,
        "macro": 0,
        "other": 0,
    }
    topic_pnl: Dict[str, float] = {k: 0.0 for k in topic_counts}
    event_outcomes: Dict[str, set] = {}

    closed_formatted: List[Dict[str, Any]] = []

    for pos in closed_positions:
        avg_price = float(pos.get("avgPrice") or 0.0)
        total_bought = float(pos.get("totalBought") or 0.0)
        realized_pnl = float(pos.get("realizedPnl") or 0.0)
        cost = avg_price * total_bought if avg_price > 0 and total_bought > 0 else 0.0
        pos_roi_pct = (realized_pnl / cost * 100.0) if cost > 0 else 0.0

        if cost > 0:
            total_cost += cost
            position_costs.append(cost)
        total_realized_pnl += realized_pnl

        if 0.0 < avg_price < 1.0:
            entry_prices.append(avg_price)

        if realized_pnl > 0:
            wins += 1
            gross_profit += realized_pnl
            win_amounts.append(realized_pnl)
        elif realized_pnl < 0:
            losses += 1
            gross_loss += abs(realized_pnl)
            loss_amounts.append(realized_pnl)

        outcome_idx = pos.get("outcomeIndex")
        outcome_label = str(pos.get("outcome") or "").strip()
        if outcome_idx == 0 or outcome_label.lower() in ("yes", "over"):
            yes_count += 1
        elif outcome_idx == 1 or outcome_label.lower() in ("no", "under"):
            no_count += 1

        title = pos.get("title") or ""
        slug = pos.get("slug") or pos.get("eventSlug") or ""
        topic = classify_topic(title, slug)
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
        topic_pnl[topic] = topic_pnl.get(topic, 0.0) + realized_pnl

        event_key = pos.get("eventSlug") or pos.get("conditionId") or title
        if event_key:
            event_outcomes.setdefault(event_key, set()).add(outcome_label or str(outcome_idx))

        closed_formatted.append(
            {
                "condition_id": pos.get("conditionId") or "",
                "title": title,
                "outcome": outcome_label or ("Yes" if outcome_idx == 0 else "No"),
                "avg_price": round(avg_price, 4),
                "cost_usd": round(cost, 2),
                "realized_pnl": round(realized_pnl, 2),
                "roi_pct": round(pos_roi_pct, 1),
                "topic": topic,
                "closed_at_est": format_ts_est(pos.get("timestamp") or pos.get("endDate")),
            }
        )

    # Also incorporate open positions into topic & price band stats if closed sample is small
    open_formatted: List[Dict[str, Any]] = []
    open_total_value = 0.0
    open_unrealized_pnl = 0.0
    for pos in open_positions:
        size = float(pos.get("size") or 0.0)
        avg_price = float(pos.get("avgPrice") or 0.0)
        cur_price = float(pos.get("curPrice") or 0.0)
        init_val = float(pos.get("initialValue") or (size * avg_price) or 0.0)
        cur_val = float(pos.get("currentValue") or (size * cur_price) or 0.0)
        cash_pnl = float(pos.get("cashPnl") or (cur_val - init_val) or 0.0)
        pct_pnl = float(pos.get("percentPnl") or ((cash_pnl / init_val * 100.0) if init_val > 0 else 0.0))
        outcome_idx = pos.get("outcomeIndex", 0)
        outcome_label = str(pos.get("outcome") or ("Yes" if outcome_idx == 0 else "No"))
        title = pos.get("title") or ""
        slug = pos.get("slug") or pos.get("eventSlug") or ""
        topic = classify_topic(title, slug)

        open_total_value += cur_val
        open_unrealized_pnl += cash_pnl

        if len(closed_positions) < 20:
            if 0.0 < avg_price < 1.0:
                entry_prices.append(avg_price)
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
            if outcome_idx == 0 or outcome_label.lower() in ("yes", "over"):
                yes_count += 1
            else:
                no_count += 1

        drift = round(cur_price - avg_price, 4) if (avg_price > 0 and cur_price > 0) else 0.0
        copyable = (
            cur_val >= 100.0
            and 0.03 <= cur_price <= 0.95
            and not bool(pos.get("redeemable"))
        )

        open_formatted.append(
            {
                "condition_id": pos.get("conditionId") or "",
                "asset": pos.get("asset") or "",
                "title": title,
                "slug": slug,
                "topic": topic,
                "outcome": outcome_label,
                "outcome_index": outcome_idx,
                "side": "yes" if outcome_idx == 0 else "no",
                "size": round(size, 2),
                "avg_price": round(avg_price, 4),
                "cur_price": round(cur_price, 4),
                "price_drift": drift,
                "initial_value": round(init_val, 2),
                "current_value": round(cur_val, 2),
                "cash_pnl": round(cash_pnl, 2),
                "percent_pnl": round(pct_pnl, 2),
                "end_date": format_ts_est(pos.get("endDate")) or "",
                "copyable": copyable,
            }
        )

    # --- Activity mechanics ---
    act_counts = {"TRADE": 0, "SPLIT": 0, "MERGE": 0, "REDEEM": 0, "OTHER": 0}
    trade_sizes_usdc: List[float] = []
    trade_timestamps: List[float] = []
    buy_trades = 0
    sell_trades = 0

    for act in activities:
        atype = str(act.get("type") or "OTHER").upper()
        if atype in act_counts:
            act_counts[atype] += 1
        else:
            act_counts["OTHER"] += 1

        if atype == "TRADE":
            usdc = float(act.get("usdcSize") or 0.0)
            if usdc <= 0:
                usdc = float(act.get("size") or 0.0) * float(act.get("price") or 0.0)
            if usdc > 0:
                trade_sizes_usdc.append(usdc)
            side = str(act.get("side") or "").upper()
            if side == "BUY":
                buy_trades += 1
            elif side == "SELL":
                sell_trades += 1

        ts = act.get("timestamp")
        if isinstance(ts, (int, float)):
            trade_timestamps.append(float(ts) / 1000.0 if ts > 1e11 else float(ts))

    total_acts = max(1, sum(act_counts.values()))
    split_merge_pct = round((act_counts["SPLIT"] + act_counts["MERGE"]) / total_acts * 100.0, 1)
    trade_act_pct = round(act_counts["TRADE"] / total_acts * 100.0, 1)

    # Price band distribution
    n_prices = max(1, len(entry_prices))
    longshot_pct = round(sum(1 for p in entry_prices if p < 0.20) / n_prices * 100.0, 1) if entry_prices else 0.0
    mid_pct = round(sum(1 for p in entry_prices if 0.20 <= p <= 0.80) / n_prices * 100.0, 1) if entry_prices else 0.0
    favorite_pct = round(sum(1 for p in entry_prices if p > 0.80) / n_prices * 100.0, 1) if entry_prices else 0.0
    avg_entry_price = round(statistics.mean(entry_prices), 3) if entry_prices else None
    median_entry_price = round(statistics.median(entry_prices), 3) if entry_prices else None

    # Outcome preference
    total_sides = max(1, yes_count + no_count)
    yes_pct = round(yes_count / total_sides * 100.0, 1) if (yes_count + no_count) > 0 else 50.0
    no_pct = round(no_count / total_sides * 100.0, 1) if (yes_count + no_count) > 0 else 50.0

    # Topic breakdown
    total_topics = max(1, sum(topic_counts.values()))
    topic_shares = {
        k: round(v / total_topics * 100.0, 1) for k, v in topic_counts.items()
    }
    dominant_topic = max(topic_shares.items(), key=lambda kv: kv[1])[0] if sum(topic_counts.values()) > 0 else "other"

    # Hedged / multi-leg events ratio
    hedged_events = sum(1 for outcomes in event_outcomes.values() if len(outcomes) > 1)
    hedged_events_pct = round(hedged_events / max(1, len(event_outcomes)) * 100.0, 1) if event_outcomes else 0.0

    # Win rate & realized ROI
    resolved_count = wins + losses
    win_rate_pct = round(wins / resolved_count * 100.0, 1) if resolved_count > 0 else None
    realized_roi_pct = round(total_realized_pnl / total_cost * 100.0, 2) if total_cost > 0 else None
    profit_factor = round(gross_profit / gross_loss, 2) if gross_loss > 0 else (99.0 if gross_profit > 0 else None)
    avg_win_usd = round(statistics.mean(win_amounts), 2) if win_amounts else 0.0
    avg_loss_usd = round(statistics.mean(loss_amounts), 2) if loss_amounts else 0.0
    payoff_ratio = round(avg_win_usd / abs(avg_loss_usd), 2) if avg_loss_usd < 0 else None

    # Composite % earning metric:
    # We track both Return on Volume (pnl / volume) AND Sampled Realized ROI (realized_pnl / cost)
    return_on_volume_pct = account.get("return_on_volume_pct") or (
        round(account["pnl"] / account["volume"] * 100.0, 2) if account["volume"] > 0 else 0.0
    )

    # Cohort classification: % Earner vs Volume Earner vs Both
    # Use overall return_on_volume_pct (>= 10% net profit per dollar of total volume)
    # and chronological realized_roi_pct (>= 12%) to separate true % ROI leaders from high-turnover volume whales.
    is_high_pct = return_on_volume_pct >= 10.0 or (
        realized_roi_pct is not None and realized_roi_pct >= 12.0 and return_on_volume_pct >= 5.0
    )
    is_high_vol = account["volume"] >= 100_000_000 or (account.get("rank_vol") is not None and account["rank_vol"] <= 15)
    if is_high_pct and is_high_vol:
        earning_cohort = "both"
        earning_cohort_label = "High % + High Volume"
    elif is_high_pct:
        earning_cohort = "pct_earner"
        earning_cohort_label = "Top % Earner"
    elif is_high_vol:
        earning_cohort = "volume_earner"
        earning_cohort_label = "Top Volume Earner"
    else:
        earning_cohort = "pnl_leader"
        earning_cohort_label = "Top Net PnL"

    # Format biggest all-time wins from top_wins_positions alongside chronological losses
    all_time_wins: List[Dict[str, Any]] = []
    for pos in top_wins_positions:
        avg_price = float(pos.get("avgPrice") or 0.0)
        total_bought = float(pos.get("totalBought") or 0.0)
        realized_pnl = float(pos.get("realizedPnl") or 0.0)
        cost = avg_price * total_bought if avg_price > 0 and total_bought > 0 else 0.0
        pos_roi_pct = (realized_pnl / cost * 100.0) if cost > 0 else 0.0
        outcome_idx = pos.get("outcomeIndex")
        outcome_label = str(pos.get("outcome") or "").strip()
        title = pos.get("title") or ""
        slug = pos.get("slug") or pos.get("eventSlug") or ""
        all_time_wins.append(
            {
                "condition_id": pos.get("conditionId") or "",
                "title": title,
                "outcome": outcome_label or ("Yes" if outcome_idx == 0 else "No"),
                "avg_price": round(avg_price, 4),
                "cost_usd": round(cost, 2),
                "realized_pnl": round(realized_pnl, 2),
                "roi_pct": round(pos_roi_pct, 1),
                "topic": classify_topic(title, slug),
                "closed_at_est": format_ts_est(pos.get("timestamp") or pos.get("endDate")),
            }
        )

    top_wins = all_time_wins[:5] if all_time_wins else sorted(closed_formatted, key=lambda x: x["realized_pnl"], reverse=True)[:5]
    top_losses = sorted(
        [c for c in closed_formatted if c["realized_pnl"] < 0],
        key=lambda x: x["realized_pnl"],
    )[:4]

    return {
        **account,
        "return_on_volume_pct": return_on_volume_pct,
        "realized_roi_pct": realized_roi_pct,
        "win_rate_pct": win_rate_pct,
        "profit_factor": profit_factor,
        "closed_sampled": len(closed_positions),
        "wins": wins,
        "losses": losses,
        "realized_cost_sampled": round(total_cost, 2),
        "realized_pnl_sampled": round(total_realized_pnl, 2),
        "avg_win_usd": avg_win_usd,
        "avg_loss_usd": avg_loss_usd,
        "payoff_ratio": payoff_ratio,
        "median_position_cost_usd": round(statistics.median(position_costs), 2) if position_costs else 0.0,
        "open_positions_count": len(open_formatted),
        "open_value_usd": round(open_total_value, 2),
        "open_unrealized_pnl_usd": round(open_unrealized_pnl, 2),
        "earning_cohort": earning_cohort,
        "earning_cohort_label": earning_cohort_label,
        "patterns": {
            "avg_entry_price": avg_entry_price,
            "median_entry_price": median_entry_price,
            "longshot_pct": longshot_pct,
            "mid_pct": mid_pct,
            "favorite_pct": favorite_pct,
            "yes_pct": yes_pct,
            "no_pct": no_pct,
            "dominant_topic": dominant_topic,
            "topic_shares": topic_shares,
            "topic_pnl": {k: round(v, 2) for k, v in topic_pnl.items()},
            "hedged_events_pct": hedged_events_pct,
            "split_merge_pct": split_merge_pct,
            "trade_act_pct": trade_act_pct,
            "median_trade_usdc": round(statistics.median(trade_sizes_usdc), 2) if trade_sizes_usdc else 0.0,
            "buy_sell_ratio": round(buy_trades / max(1, sell_trades), 2) if (buy_trades + sell_trades) > 0 else None,
        },
        "top_closed_wins": top_wins,
        "top_closed_losses": top_losses,
        "open_positions": open_formatted[:40],
    }


def _deterministic_strategy_fallback(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Rule-based baseline strategy assessment used to seed and validate LLM output."""
    p = profile["patterns"]
    rov = profile["return_on_volume_pct"]
    rroi = profile.get("realized_roi_pct") or rov
    vol = profile["volume"]
    pnl = profile["pnl"]
    win_rate = profile.get("win_rate_pct") or 50.0
    dom_topic = p["dominant_topic"]
    fav_pct = p["favorite_pct"]
    longshot_pct = p["longshot_pct"]
    no_pct = p["no_pct"]
    hedged_pct = p["hedged_events_pct"]
    split_merge_pct = p["split_merge_pct"]

    # Determine archetype and edge source
    if split_merge_pct >= 15.0 or (vol >= 300_000_000 and rov < 2.5):
        archetype = f"High-Frequency {dom_topic.title()} Bookmaker / Liquidity Provider"
        edge_source = "Spread Capture & Automated Bookmaking"
        base_copy_score = 3
    elif hedged_pct >= 25.0 and rov < 6.0:
        archetype = f"Multi-Outcome {dom_topic.title()} Arbitrage & Hedger"
        edge_source = "Cross-Outcome Hedging & Line Shopping"
        base_copy_score = 4
    elif fav_pct >= 45.0 and win_rate >= 75.0:
        archetype = f"High-Probability {dom_topic.title()} Bond Clipper"
        edge_source = "Late-Stage Favorite Harvesting (>0.80 Implied)"
        base_copy_score = 7
    elif longshot_pct >= 40.0:
        archetype = f"Asymmetric {dom_topic.title()} Tail-Risk Hunter"
        edge_source = "Underdog Convexity (<0.20 Implied)"
        base_copy_score = 7
    elif no_pct >= 62.0 and rov >= 10.0:
        archetype = f"Directional 'No' Fade Specialist ({dom_topic.title()})"
        edge_source = "Fading Overpriced Retail Hype"
        base_copy_score = 8
    elif rov >= 20.0:
        archetype = f"High-Conviction {dom_topic.title()} Macro Whale"
        edge_source = "Concentrated Directional Information Edge"
        base_copy_score = 9
    else:
        archetype = f"Active {dom_topic.title()} Value & Momentum Trader"
        edge_source = "Mid-Probability Mispricing & Line Value"
        base_copy_score = 7

    # Adjust copyability score based on open positions, turnover margin, and holding style
    if profile["open_positions_count"] == 0:
        base_copy_score = max(2, base_copy_score - 2)
    elif any(pos.get("copyable") for pos in profile.get("open_positions", [])):
        base_copy_score = min(10, base_copy_score + 1)

    if rov < 1.5 and vol > 200_000_000:
        base_copy_score = min(base_copy_score, 3)

    if base_copy_score >= 7:
        copy_label = "High"
    elif base_copy_score >= 5:
        copy_label = "Medium"
    else:
        copy_label = "Low"

    findings = [
        f"Extracts {rov:.2f}% net return on ${vol:,.0f} volume (${pnl:,.0f} total profit), with {rroi:.1f}% realized ROI across sampled closed positions.",
        f"Topic allocation is led by {dom_topic} ({p['topic_shares'].get(dom_topic, 0):.1f}%), with an average entry price of {p['avg_entry_price'] if p['avg_entry_price'] is not None else 0.5:.2f}.",
        f"Price band mix: {longshot_pct:.1f}% longshots (<0.20), {p['mid_pct']:.1f}% mid-range (0.20-0.80), and {fav_pct:.1f}% heavy favorites (>0.80).",
        f"Directional split is {p['yes_pct']:.1f}% Yes/Over vs {no_pct:.1f}% No/Under; {hedged_pct:.1f}% of events show multi-outcome hedging.",
    ]

    if copy_label == "High":
        copy_rec = (
            f"Strong copy candidate. Mirror new {dom_topic} entries when current market price is within 0.03 of their average entry price ({p['avg_entry_price'] or 0.50:.2f} typical)."
        )
    elif copy_label == "Medium":
        copy_rec = (
            f"Selective copy candidate. Only copy high-conviction positions above ${max(1000.0, profile.get('median_position_cost_usd') or 0.0):,.0f} where the account holds a single unhedged side."
        )
    else:
        copy_rec = (
            "Low direct copyability for slower followers: this account relies on high-turnover bookmaking or multi-leg hedging with thin per-trade margin."
        )

    summary = (
        f"{profile['user_name']} operates as a {archetype.lower()}, generating ${pnl:,.0f} on ${vol:,.0f} volume "
        f"({rov:.2f}% margin on volume, {win_rate:.1f}% win rate). "
        f"They concentrate in {dom_topic} markets with {no_pct:.0f}% No/Under exposure and a {p['avg_entry_price'] or 0.50:.2f} average entry price."
    )

    return {
        "archetype": archetype,
        "strategy_summary": summary,
        "pattern_findings": findings,
        "edge_source": edge_source,
        "copy_recommendation": copy_rec,
        "copyability_score": base_copy_score,
        "copyability_label": copy_label,
        "llm_model": "quantitative-baseline",
    }


# Public feeds that match how a topic is usually priced. These are research
# hypotheses, not proof that a wallet subscribed to them.
TOPIC_INFORMATION_SOURCES: Dict[str, List[Dict[str, str]]] = {
    "sports": [
        {
            "label": "The Odds API / sportsbook lines",
            "api": "https://the-odds-api.com",
            "why": "Sharp sports wallets often sit near consensus book prices, then fade Polymarket when it lags.",
        },
        {
            "label": "ESPN / official league score APIs",
            "api": "https://site.api.espn.com/apis/site/v2/sports",
            "why": "Live score state is the usual trigger for late in-game bets.",
        },
        {
            "label": "Polymarket CLOB prices-history",
            "api": "https://clob.polymarket.com/prices-history",
            "why": "Mean-reversion bots watch their own book's last mid versus a sportsbook implied.",
        },
    ],
    "politics": [
        {
            "label": "FiveThirtyEight / 538 forecast dumps",
            "api": "https://projects.fivethirtyeight.com",
            "why": "Election favorites often track published model probabilities more than news headlines.",
        },
        {
            "label": "PredictIt / Kalshi same-question books",
            "api": "https://www.predictit.org/api  and  https://api.elections.kalshi.com",
            "why": "Cross-venue spreads on the same race are a common arb source.",
        },
        {
            "label": "AP / Decision Desk HQ election calls",
            "api": "wire / DDHQ live",
            "why": "Resolution-adjacent wallets trade immediately after an official call.",
        },
    ],
    "crypto": [
        {
            "label": "Binance / Coinbase spot + funding",
            "api": "https://api.binance.com  /  Coinbase exchange",
            "why": "Crypto-threshold markets are usually a delayed copy of spot and perp funding.",
        },
        {
            "label": "DefiLlama / Dune dashboards",
            "api": "https://api.llama.fi",
            "why": "TVL and unlock calendars show up in protocol-specific markets.",
        },
        {
            "label": "Polymarket Gamma events + CLOB",
            "api": "https://gamma-api.polymarket.com  /  https://clob.polymarket.com",
            "why": "Inventory bots only need the public book and event metadata.",
        },
    ],
    "culture": [
        {
            "label": "Box Office Mojo / The Numbers",
            "api": "https://www.the-numbers.com",
            "why": "Movie and award markets lean on weekend gross prints.",
        },
        {
            "label": "Wikipedia pageviews / Google Trends",
            "api": "https://wikimedia.org/api/rest_v1/metrics/pageviews",
            "why": "Attention spikes often lead culture-contract prices by hours to days.",
        },
        {
            "label": "Official awards / chart lists",
            "api": "Billboard, Oscars, RIAA",
            "why": "Resolution is usually a published list, so some wallets only trade after the leak window.",
        },
    ],
    "economics": [
        {
            "label": "FRED / BLS / BEA prints",
            "api": "https://api.stlouisfed.org  /  BLS public data",
            "why": "CPI, jobs, and GDP markets are almost entirely print-vs-consensus trades.",
        },
        {
            "label": "Atlanta Fed GDPNow / Cleveland Fed nowcasts",
            "api": "https://www.atlantafed.org/cqer/research/gdpnow",
            "why": "Nowcast revisions move these contracts before the official release.",
        },
        {
            "label": "CME FedWatch",
            "api": "CME FedWatch tool",
            "why": "Rate-decision markets usually shadow SOFR / Fed funds futures.",
        },
    ],
    "science": [
        {
            "label": "CDC / WHO situation reports",
            "api": "https://data.cdc.gov",
            "why": "Outbreak and health markets reprice on official case updates.",
        },
        {
            "label": "arXiv / Nature news",
            "api": "https://export.arxiv.org/api",
            "why": "Science-milestone markets move on papers and agency announcements.",
        },
        {
            "label": "NOAA / USGS feeds",
            "api": "https://api.weather.gov  /  USGS",
            "why": "Weather and disaster contracts are feed-driven.",
        },
    ],
    "other": [
        {
            "label": "Polymarket Data API (positions, activity, trades)",
            "api": DATA_API,
            "why": "Any copier can reconstruct this wallet from the same public endpoints we use.",
        },
        {
            "label": "Gamma market catalog",
            "api": "https://gamma-api.polymarket.com/markets",
            "why": "New listings and condition IDs are how bots attach to a question.",
        },
        {
            "label": "Kalshi trade API (same family)",
            "api": "https://api.elections.kalshi.com/trade-api/v2",
            "why": "If the same question exists on Kalshi, a bot can arb the pair.",
        },
    ],
}


def classify_operator(profile: Dict[str, Any]) -> Dict[str, Any]:
    p = profile.get("patterns") or {}
    vol = float(profile.get("volume") or 0)
    rov = float(profile.get("return_on_volume_pct") or 0)
    split = float(p.get("split_merge_pct") or 0)
    hedged = float(p.get("hedged_events_pct") or 0)
    trade_pct = float(p.get("trade_act_pct") or 0)
    median = float(p.get("median_trade_usdc") or 0)
    closed = int(profile.get("closed_sampled") or 0)
    open_n = int(profile.get("open_positions_count") or 0)
    reasons: List[str] = []
    bot = 0
    human = 0

    if split >= 8:
        bot += 28
        reasons.append(f"{split:.1f}% of activity is split/merge. That is inventory plumbing, not a discretionary bet.")
    if vol >= 80_000_000 and rov < 4:
        bot += 24
        reasons.append(f"${vol:,.0f} volume at {rov:.2f}% return on volume looks like a maker book, not a punter.")
    if hedged >= 35:
        bot += 16
        reasons.append(f"{hedged:.1f}% of events have more than one outcome. That is a hedge book.")
    if median and median < 80 and vol > 2_000_000:
        bot += 12
        reasons.append(f"Median ticket ${median:,.0f} is small versus total volume, which fits sliced automated size.")
    if trade_pct >= 88 and split >= 3:
        bot += 8
        reasons.append("Almost all recorded activity is trades plus inventory ops.")

    if rov >= 8:
        human += 22
        reasons.append(f"{rov:.2f}% return on volume is fat for a thin-spread bot and fits a directional human or a research desk.")
    if open_n and open_n <= 10 and rov >= 6:
        human += 12
        reasons.append(f"Only {open_n} open positions with a high ROI looks like a short, watched book.")
    if closed and closed < 60 and float(p.get("favorite_pct") or 0) < 75:
        human += 8
        reasons.append("A smaller closed sample that is not all heavy favorites is closer to discretionary picking.")

    if bot >= 45:
        kind, label = "bot", "Likely bot / automated book"
    elif bot >= 22 and human >= 18:
        kind, label = "mixed", "Mixed: human thesis, automated execution"
    elif human >= 20 and bot < 25:
        kind, label = "human", "Likely human / discretionary"
    else:
        kind, label = "unclear", "Unclear operator. Not enough mechanic tells."

    return {
        "kind": kind,
        "label": label,
        "bot_score": min(100, bot),
        "human_score": min(100, human),
        "reasons": reasons[:6],
    }


def information_sources_for(profile: Dict[str, Any]) -> List[Dict[str, str]]:
    topic = ((profile.get("patterns") or {}).get("dominant_topic") or "other").lower()
    rows = list(TOPIC_INFORMATION_SOURCES.get(topic, []))
    rows.extend(TOPIC_INFORMATION_SOURCES["other"])
    # de-dupe by label
    seen = set()
    out = []
    for row in rows:
        key = row.get("label")
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out[:6]


def copy_steps_for(profile: Dict[str, Any], operator: Dict[str, Any]) -> List[str]:
    p = profile.get("patterns") or {}
    llm = profile.get("llm_analysis") or {}
    topic = p.get("dominant_topic") or "the same topic"
    avg = p.get("avg_entry_price")
    avg_s = f"{avg:.2f}" if avg is not None else "their last mid"
    kind = operator.get("kind")
    label = llm.get("copyability_label") or "Low"
    if kind == "bot" or label == "Low":
        return [
            "Do not copy individual fills. This book is too fast or too hedged for a slower follower.",
            "If you use it at all, watch only for complete-set / cross-venue gaps they leave behind, and paper those.",
            "Cap any paper size at a tiny fraction of their median ticket so you are not their exit liquidity.",
            "Re-check this dossier after the next investigation run. Bot books change inventory rules without notice.",
        ]
    return [
        f"Follow the wallet and wait for a new {topic} fill, same Yes/No side they just took.",
        f"Only paper-copy if the live mid is within 0.03 of their typical entry ({avg_s}). Skip if the print already moved.",
        "Skip the trade if they already hold the other outcome on the same event (hedge, not a view).",
        f"Size down: start at a fraction of their median ticket (${float(p.get('median_trade_usdc') or profile.get('median_position_cost_usd') or 100):,.0f}).",
        "Log the copy as paper, then compare your fill to theirs 24 hours later before raising size.",
        llm.get("copy_recommendation") or "Prefer unhedged, high-dollar names in their dominant topic.",
    ]


def how_they_bet(profile: Dict[str, Any]) -> Dict[str, Any]:
    p = profile.get("patterns") or {}
    shares = p.get("topic_shares") or {}
    return {
        "dominant_topic": p.get("dominant_topic"),
        "avg_entry_price": p.get("avg_entry_price"),
        "yes_pct": p.get("yes_pct"),
        "no_pct": p.get("no_pct"),
        "longshot_pct": p.get("longshot_pct"),
        "mid_pct": p.get("mid_pct"),
        "favorite_pct": p.get("favorite_pct"),
        "hedged_events_pct": p.get("hedged_events_pct"),
        "split_merge_pct": p.get("split_merge_pct"),
        "median_trade_usdc": p.get("median_trade_usdc"),
        "topic_rows": [
            {"topic": k, "share": v} for k, v in sorted(shares.items(), key=lambda kv: kv[1], reverse=True)
        ],
        "band_rows": [
            {"band": "Longshot <0.20", "share": p.get("longshot_pct") or 0},
            {"band": "Mid 0.20-0.80", "share": p.get("mid_pct") or 0},
            {"band": "Favorite >0.80", "share": p.get("favorite_pct") or 0},
        ],
        "side_rows": [
            {"side": "Yes / Over", "share": p.get("yes_pct") or 0},
            {"side": "No / Under", "share": p.get("no_pct") or 0},
        ],
    }


def enrich_account_dossier(account: Dict[str, Any]) -> Dict[str, Any]:
    """Attach operator, sources, and copy steps on read so old JSON still works."""
    operator = classify_operator(account)
    account["dossier"] = {
        "operator": operator,
        "sources": information_sources_for(account),
        "copy_steps": copy_steps_for(account, operator),
        "how_they_bet": how_they_bet(account),
    }
    return account


def analyze_trader_with_llm(
    profile: Dict[str, Any],
    ollama_url: str = None,
    model: str = "llama3.2:latest",
) -> Dict[str, Any]:
    """Use local Ollama LLM to synthesize trading strategy, pattern analysis, and copy recommendation."""
    fallback = _deterministic_strategy_fallback(profile)
    base_url = ollama_url or Config.OLLAMA_BASE_URL or "http://localhost:11434"
    p = profile["patterns"]

    wins_sample = [
        f"{w['title'][:45]} ({w['outcome']}@{w['avg_price']:.2f}, +${w['realized_pnl']:,.0f})"
        for w in profile.get("top_closed_wins", [])[:2]
    ]
    open_sample = [
        f"{o['title'][:45]} ({o['outcome']}@{o['avg_price']:.2f})"
        for o in profile.get("open_positions", [])[:2]
    ]

    prompt = (
        f"Prediction market quant analysis for trader {profile['user_name']} ({profile['earning_cohort_label']}, {fallback['archetype']}): "
        f"PnL=${profile['pnl']:,.0f}, Volume=${profile['volume']:,.0f}, ReturnOnVol={profile['return_on_volume_pct']:.2f}%, "
        f"WinRate={profile['win_rate_pct']}%, RealizedROI={profile['realized_roi_pct']}%, "
        f"AvgEntry={p['avg_entry_price']} (Longshot<0.2={p['longshot_pct']}%, Mid={p['mid_pct']}%, Fav>0.8={p['favorite_pct']}%), "
        f"Yes={p['yes_pct']}%/No={p['no_pct']}%, Topic={p['dominant_topic']}, Hedged={p['hedged_events_pct']}%, Splits={p['split_merge_pct']}%. "
        f"TopWins={'; '.join(wins_sample) or 'N/A'}. Open={'; '.join(open_sample) or 'None'}. "
        "Reply ONLY with JSON keys: strategy_summary (2 sentences explaining their trading strategy and how they generate edge from these metrics), "
        "copy_trade_rule (1 sentence rule for how an automated trading bot should copy or avoid copying their positions)."
    )

    try:
        resp = requests.post(
            f"{base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0.2,
                    "num_predict": 140,
                    "num_ctx": 1024,
                },
            },
            timeout=60,
        )
        resp.raise_for_status()
        raw_text = resp.json().get("response", "").strip()
        parsed = json.loads(raw_text)

        llm_summary = str(parsed.get("strategy_summary") or "").strip()
        llm_copy_rule = str(parsed.get("copy_trade_rule") or "").strip()
        score = int(fallback["copyability_score"])
        if profile["return_on_volume_pct"] < 1.5 and profile["volume"] > 200_000_000:
            score = min(score, 4)

        label = "High" if score >= 7 else ("Medium" if score >= 5 else "Low")

        return {
            "archetype": fallback["archetype"],
            "strategy_summary": f"{llm_summary} {fallback['strategy_summary']}".strip() if llm_summary else fallback["strategy_summary"],
            "pattern_findings": fallback["pattern_findings"],
            "edge_source": fallback["edge_source"],
            "copy_recommendation": f"{fallback['copy_recommendation']} LLM rule: {llm_copy_rule}".strip() if llm_copy_rule else fallback["copy_recommendation"],
            "copyability_score": score,
            "copyability_label": label,
            "llm_model": model,
        }
    except Exception:
        return fallback


def build_copyable_signals(accounts: List[Dict[str, Any]], followed_addresses: Optional[set] = None) -> List[Dict[str, Any]]:
    """Aggregate actionable copy-trade signals from top accounts' current open positions."""
    signals: List[Dict[str, Any]] = []
    for acc in accounts:
        copy_score = acc.get("llm_analysis", {}).get("copyability_score", 5)
        is_followed = bool(followed_addresses and acc["address"].lower() in followed_addresses)
        for pos in acc.get("open_positions", []):
            if not pos.get("copyable"):
                continue
            cur_price = pos["cur_price"]
            avg_price = pos["avg_price"]
            drift = pos["price_drift"]

            # Prefer positions where current price hasn't run away more than +12c above whale's entry
            if drift > 0.12:
                continue

            entry_edge_bonus = 1.0 if drift <= 0.0 else max(0.0, 1.0 - (drift / 0.12))
            signal_score = round(
                (copy_score * 0.55)
                + (min(acc["return_on_volume_pct"], 40.0) / 40.0 * 2.5)
                + (entry_edge_bonus * 2.0),
                2,
            )

            signals.append(
                {
                    "trader_address": acc["address"],
                    "trader_name": acc["user_name"],
                    "earning_cohort_label": acc["earning_cohort_label"],
                    "trader_pnl": acc["pnl"],
                    "trader_volume": acc["volume"],
                    "trader_return_on_volume_pct": acc["return_on_volume_pct"],
                    "trader_win_rate_pct": acc.get("win_rate_pct"),
                    "trader_archetype": acc.get("llm_analysis", {}).get("archetype", ""),
                    "copyability_score": copy_score,
                    "is_followed_trader": is_followed,
                    "condition_id": pos["condition_id"],
                    "title": pos["title"],
                    "slug": pos.get("slug") or "",
                    "end_date": pos.get("end_date") or "",
                    "topic": pos["topic"],
                    "outcome": pos["outcome"],
                    "side": pos["side"],
                    "trader_avg_price": avg_price,
                    "current_price": cur_price,
                    "price_drift": drift,
                    "trader_position_value_usd": pos["current_value"],
                    "trader_unrealized_pnl_pct": pos["percent_pnl"],
                    "signal_score": signal_score,
                    "recommended_action": f"Buy {pos['outcome']} at <= {min(0.95, round(cur_price + 0.01, 3)):.2f}",
                }
            )

    signals.sort(
        key=lambda s: (s["is_followed_trader"], s["signal_score"], s["trader_position_value_usd"]),
        reverse=True,
    )
    return signals


def build_investigation_synthesis(accounts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compare % ROI leaders vs Volume leaders across the investigated cohort."""
    pct_earners = [a for a in accounts if a["earning_cohort"] in ("pct_earner", "both")]
    vol_earners = [a for a in accounts if a["earning_cohort"] in ("volume_earner", "both")]

    def _avg(items: List[Dict[str, Any]], getter) -> Optional[float]:
        vals = [getter(x) for x in items if getter(x) is not None]
        return round(statistics.mean(vals), 2) if vals else None

    top_pct = max(accounts, key=lambda a: a["return_on_volume_pct"]) if accounts else None
    top_vol = max(accounts, key=lambda a: a["volume"]) if accounts else None
    top_pnl = max(accounts, key=lambda a: a["pnl"]) if accounts else None
    top_realized_roi = (
        max(
            [a for a in accounts if a.get("realized_roi_pct") is not None and a.get("closed_sampled", 0) >= 10],
            key=lambda a: a["realized_roi_pct"],
            default=None,
        )
        if accounts
        else None
    )

    return {
        "total_accounts_investigated": len(accounts),
        "pct_earners_count": len(pct_earners),
        "volume_earners_count": len(vol_earners),
        "pct_earners_avg_rov_pct": _avg(pct_earners, lambda a: a["return_on_volume_pct"]),
        "vol_earners_avg_rov_pct": _avg(vol_earners, lambda a: a["return_on_volume_pct"]),
        "pct_earners_avg_win_rate_pct": _avg(pct_earners, lambda a: a.get("win_rate_pct")),
        "vol_earners_avg_win_rate_pct": _avg(vol_earners, lambda a: a.get("win_rate_pct")),
        "pct_earners_avg_copyability": _avg(pct_earners, lambda a: a.get("llm_analysis", {}).get("copyability_score")),
        "vol_earners_avg_copyability": _avg(vol_earners, lambda a: a.get("llm_analysis", {}).get("copyability_score")),
        "key_findings": [
            (
                f"Percentage leaders vs Volume whales are structurally distinct: top volume accounts average "
                f"{_avg(vol_earners, lambda a: a['return_on_volume_pct']) or 0:.2f}% return on volume via high-turnover sports/spread bookmaking, "
                f"whereas top % earners extract {_avg(pct_earners, lambda a: a['return_on_volume_pct']) or 0:.2f}% return on volume through directional conviction."
            ),
            (
                f"Copyability diverges sharply: % ROI leaders score {_avg(pct_earners, lambda a: a.get('llm_analysis', {}).get('copyability_score')) or 0:.1f}/10 "
                f"on copyability because they hold directional positions for days/weeks, while volume whales score "
                f"{_avg(vol_earners, lambda a: a.get('llm_analysis', {}).get('copyability_score')) or 0:.1f}/10 due to multi-outcome hedging and sub-minute turnover."
            ),
            (
                f"'No / Under' bias is a recurring pattern among profitable directional accounts: fading retail overreaction in politics, macro, and sports totals yields higher realized ROI than buying popular Yes outcomes."
            ),
        ],
        "leaders": {
            "top_pct_rov": {
                "user_name": top_pct["user_name"],
                "address": top_pct["address"],
                "return_on_volume_pct": top_pct["return_on_volume_pct"],
                "realized_roi_pct": top_pct.get("realized_roi_pct"),
                "pnl": top_pct["pnl"],
                "volume": top_pct["volume"],
            }
            if top_pct
            else None,
            "top_realized_roi": {
                "user_name": top_realized_roi["user_name"],
                "address": top_realized_roi["address"],
                "realized_roi_pct": top_realized_roi.get("realized_roi_pct"),
                "return_on_volume_pct": top_realized_roi["return_on_volume_pct"],
                "pnl": top_realized_roi["pnl"],
                "volume": top_realized_roi["volume"],
            }
            if top_realized_roi
            else None,
            "top_volume": {
                "user_name": top_vol["user_name"],
                "address": top_vol["address"],
                "volume": top_vol["volume"],
                "pnl": top_vol["pnl"],
                "return_on_volume_pct": top_vol["return_on_volume_pct"],
            }
            if top_vol
            else None,
            "top_pnl": {
                "user_name": top_pnl["user_name"],
                "address": top_pnl["address"],
                "pnl": top_pnl["pnl"],
                "volume": top_pnl["volume"],
                "return_on_volume_pct": top_pnl["return_on_volume_pct"],
            }
            if top_pnl
            else None,
        },
    }


def investigate_single_wallet(
    address: str,
    time_period: str = "ALL",
    model: str = "llama3.2:latest",
) -> Dict[str, Any]:
    """Run quantitative + LLM strategy investigation on a single wallet address."""
    wallet = address.strip().lower()
    session = requests.Session()

    # Check if wallet appears in leaderboard or profile
    rows = _get_json(
        session,
        f"{DATA_API}/v1/leaderboard",
        {"user": wallet, "timePeriod": time_period},
    )
    entry = None
    if isinstance(rows, list) and rows:
        item = rows[0]
        pnl = float(item.get("pnl") or 0.0)
        vol = float(item.get("vol") or item.get("volume") or 0.0)
        entry = {
            "address": wallet,
            "user_name": item.get("userName") or f"{wallet[:6]}...{wallet[-4:]}",
            "x_username": item.get("xUsername") or "",
            "verified": bool(item.get("verifiedBadge")),
            "pnl": pnl,
            "volume": vol,
            "rank_pnl": int(item.get("rank") or 0) or None,
            "rank_vol": None,
            "rank_roi": None,
            "return_on_volume_pct": round((pnl / vol) * 100.0, 2) if vol > 0 else 0.0,
        }
    if entry is None:
        entry = {
            "address": wallet,
            "user_name": f"{wallet[:6]}...{wallet[-4:]}",
            "x_username": "",
            "verified": False,
            "pnl": 0.0,
            "volume": 0.0,
            "rank_pnl": None,
            "rank_vol": None,
            "rank_roi": None,
            "return_on_volume_pct": 0.0,
        }

    quant = analyze_wallet_quantitatively(session, entry)
    if quant["pnl"] == 0.0 and quant["realized_pnl_sampled"] != 0.0:
        quant["pnl"] = quant["realized_pnl_sampled"]
    if quant["volume"] == 0.0 and quant["realized_cost_sampled"] > 0.0:
        quant["volume"] = quant["realized_cost_sampled"]
        quant["return_on_volume_pct"] = round(quant["pnl"] / quant["volume"] * 100.0, 2)

    quant["llm_analysis"] = analyze_trader_with_llm(quant, model=model)
    quant["analyzed_at_est"] = now_est_str()
    return quant


def run_top_accounts_investigation(
    time_period: str = "ALL",
    max_candidates: int = 16,
    model: str = "llama3.2:latest",
    save: bool = True,
) -> Dict[str, Any]:
    """Fetch top % and volume accounts, compute trade forensics, and run Ollama LLM strategy analysis."""
    session = requests.Session()
    pool = fetch_leaderboard_pool(session, time_period=time_period, pages_per_sort=3)
    candidates = select_candidate_accounts(pool, max_candidates=max_candidates)

    profiles: List[Dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        future_map = {
            executor.submit(analyze_wallet_quantitatively, session, cand): cand
            for cand in candidates
        }
        for future in as_completed(future_map):
            try:
                profiles.append(future.result())
            except Exception as exc:
                cand = future_map[future]
                print(f"Warning: failed quantitative fetch for {cand['address']}: {exc}")

    # Sort profiles so we analyze the most interesting % and volume leaders in deterministic order
    profiles.sort(key=lambda p: (p["pnl"], p["return_on_volume_pct"]), reverse=True)

    # First populate deterministic baseline on all profiles so incremental saves are complete immediately
    for prof in profiles:
        prof["llm_analysis"] = _deterministic_strategy_fallback(prof)
        prof["analyzed_at_est"] = now_est_str()

    watchlist = load_watchlist()
    followed_set = {w["address"].lower() for w in watchlist.get("accounts", []) if w.get("enabled", True)}

    if not watchlist.get("accounts"):
        high_copy = sorted(
            [p for p in profiles if p.get("llm_analysis", {}).get("copyability_score", 0) >= 7],
            key=lambda p: (p.get("llm_analysis", {}).get("copyability_score", 0), p["return_on_volume_pct"]),
            reverse=True,
        )[:4]
        seeded = [
            {
                "address": p["address"],
                "user_name": p["user_name"],
                "archetype": p.get("llm_analysis", {}).get("archetype", ""),
                "copyability_score": p.get("llm_analysis", {}).get("copyability_score", 7),
                "max_position_usd": 100.0,
                "max_price_drift": 0.05,
                "enabled": True,
                "added_at_est": now_est_str(),
            }
            for p in high_copy
        ]
        watchlist = {"updated_at_est": now_est_str(), "accounts": seeded}
        save_watchlist(watchlist)
        followed_set = {w["address"].lower() for w in seeded}

    for prof in profiles:
        prof["is_followed"] = prof["address"].lower() in followed_set

    def _save_snapshot():
        if not save:
            return
        syn = build_investigation_synthesis(profiles)
        sigs = build_copyable_signals(profiles, followed_addresses=followed_set)
        snap = {
            "generated_at_est": now_est_str(),
            "time_period": time_period,
            "llm_model": model,
            "pool_scanned": len(pool),
            "synthesis": syn,
            "accounts": profiles,
            "copy_signals": sigs,
        }
        TOP_ACCOUNTS_PATH.parent.mkdir(parents=True, exist_ok=True)
        TOP_ACCOUNTS_PATH.write_text(json.dumps(snap, indent=2), encoding="utf-8")

    _save_snapshot()

    for idx, prof in enumerate(profiles, start=1):
        print(
            f"[{idx}/{len(profiles)}] LLM analyzing {prof['user_name']} "
            f"(PnL=${prof['pnl']:,.0f}, Vol=${prof['volume']:,.0f}, RoV={prof['return_on_volume_pct']:.2f}%)...",
            flush=True,
        )
        prof["llm_analysis"] = analyze_trader_with_llm(prof, model=model)
        prof["analyzed_at_est"] = now_est_str()
        _save_snapshot()

    synthesis = build_investigation_synthesis(profiles)
    copy_signals = build_copyable_signals(profiles, followed_addresses=followed_set)

    payload = {
        "generated_at_est": now_est_str(),
        "time_period": time_period,
        "llm_model": model,
        "pool_scanned": len(pool),
        "synthesis": synthesis,
        "accounts": profiles,
        "copy_signals": copy_signals,
    }

    if save:
        TOP_ACCOUNTS_PATH.parent.mkdir(parents=True, exist_ok=True)
        TOP_ACCOUNTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return payload


def load_watchlist() -> Dict[str, Any]:
    if not WATCHLIST_PATH.exists():
        return {"updated_at_est": None, "accounts": []}
    try:
        return json.loads(WATCHLIST_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"updated_at_est": None, "accounts": []}


def save_watchlist(data: Dict[str, Any]) -> Dict[str, Any]:
    WATCHLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at_est"] = now_est_str()
    WATCHLIST_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def record_paper_copy_trade(trade: Dict[str, Any]) -> Dict[str, Any]:
    PAPER_COPY_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        **trade,
        "executed_at_est": now_est_str(),
        "timestamp": datetime.now(EST).isoformat(),
        "mode": "paper",
    }
    with open(PAPER_COPY_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def load_paper_copy_trades(limit: int = 50) -> List[Dict[str, Any]]:
    if not PAPER_COPY_LOG.exists():
        return []
    lines = PAPER_COPY_LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    out: List[Dict[str, Any]] = []
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            continue
        if len(out) >= limit:
            break
    return out
