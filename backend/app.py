"""HTTP API for the information markets dashboard."""
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import Config
from src.research.market_playbooks import playbook_for, summarize as summarize_playbooks

EST = ZoneInfo("America/New_York")
LOG_DIR = ROOT / "data" / "logs" / "runner"

STRATEGIES = [
    {
        "name": "lead_lag",
        "label": "Lead-lag",
        "weight": 1.0,
        "description": "Trade when one venue moves and the matched market has not caught up.",
    },
    {
        "name": "volume_spike",
        "label": "Volume spike",
        "weight": 0.8,
        "description": "Flag markets whose recent volume is well above its lookback baseline.",
    },
    {
        "name": "price_alerts",
        "label": "Price alerts",
        "weight": 0.6,
        "description": "Watch price levels and emit a signal when a market crosses one.",
    },
    {
        "name": "price_convergence",
        "label": "Price convergence",
        "weight": 1.2,
        "description": "Look for Kalshi and Polymarket prices on the same event that have diverged.",
    },
    {
        "name": "momentum",
        "label": "Momentum",
        "weight": 0.7,
        "description": "Follow short-window price momentum above a minimum move.",
    },
    {
        "name": "arbitrage",
        "label": "Arbitrage",
        "weight": 1.5,
        "description": "Estimate locked-in profit after Kalshi fees and Polymarket costs.",
    },
    {
        "name": "complete_set",
        "label": "Complete set",
        "weight": 1.5,
        "description": "Buy or sell every outcome of a mutually exclusive event when the prices do not add up to $1.",
    },
    {
        "name": "copy_top_traders",
        "label": "Copy top traders",
        "weight": 1.0,
        "description": "Mirror recent activity from high-PnL Polymarket wallets.",
    },
    {
        "name": "copy_watchlist",
        "label": "Copy watchlist fills",
        "weight": 1.0,
        "description": "Straight-copy recent buys and sells from accounts on your copy watchlist. If the list is empty, it uses the highest-copyability investigated wallets.",
    },
]

app = FastAPI(title="Information Markets")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

_runner = None
_runner_lock = threading.Lock()


class RunnerStart(BaseModel):
    interval_seconds: float = Field(default=30, ge=5, le=3600)
    paper_trading: bool = True


def _format_est(value: str | None) -> str | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=EST)
    return parsed.astimezone(EST).strftime("%b %d, %Y %I:%M %p EST")


def _get_runner():
    global _runner
    with _runner_lock:
        if _runner is None:
            from src.strategies.trading.runner import create_default_runner

            _runner = create_default_runner(paper_trading=True)
        return _runner


@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/eda/favorites")
def favorite_calibration():
    path = ROOT / "data" / "eda" / "favorite_calibration.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Favorite calibration has not been built")
    return json.loads(path.read_text(encoding="utf-8"))


@app.get("/api/eda/backtests")
def strategy_backtests():
    path = ROOT / "data" / "eda" / "strategy_backtests.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Strategy backtests have not been built")
    return json.loads(path.read_text(encoding="utf-8"))


_chart_cache = {"mtime": None, "payload": None}


@app.get("/api/eda/charts")
def eda_charts():
    from src.research.eda_charts import load_chart_payload

    path = ROOT / "data" / "eda" / "backtest_observations.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Backtest observations have not been built")
    mtime = path.stat().st_mtime
    cached = _chart_cache["payload"]
    if _chart_cache["mtime"] != mtime or cached is None or "families" not in cached:
        _chart_cache["payload"] = load_chart_payload(ROOT / "data" / "eda")
        _chart_cache["mtime"] = mtime
    payload = dict(_chart_cache["payload"] or {})
    with _catalog_lock:
        live = list(_catalog["polymarket"]) + list(_catalog["kalshi"])
        fetched = _catalog.get("fetched_at_est")
    from src.research.eda_charts import ladder_breaks, open_family_shape

    payload["open_families"] = open_family_shape(live)
    payload["ladder_breaks"] = ladder_breaks(live)
    payload["catalog_as_of_est"] = fetched
    return payload


@app.get("/api/status")
def status():
    runner = _runner
    thread = getattr(runner, "_runner_thread", None) if runner else None
    return {
        "paper_trading": True if runner is None else runner.paper_trading,
        "runner_running": bool(thread and thread.is_alive()),
        "kalshi_configured": bool(
            Config.KALSHI_API_KEY
            and (Config.KALSHI_PRIVATE_KEY_PATH or Config.KALSHI_PRIVATE_KEY_PEM)
        ),
        "polymarket_configured": bool(Config.POLYMARKET_API_KEY),
        "max_daily_trades": Config.MAX_DAILY_TRADES,
        "max_position_size": Config.MAX_POSITION_SIZE,
        "trades_today": 0 if runner is None else runner.trades_today,
    }


@app.get("/api/strategies")
def strategies():
    runner = _runner
    enabled = set(runner.strategies.keys()) if runner else {item["name"] for item in STRATEGIES}
    rows = []
    for item in STRATEGIES:
        config = runner.strategy_configs.get(item["name"]) if runner else None
        rows.append(
            {
                **item,
                "enabled": item["name"] in enabled,
                "weight": item["weight"] if config is None else config.weight,
            }
        )
    return {"strategies": rows}


@app.get("/api/logs")
def logs(limit: int = 40):
    limit = max(1, min(limit, 200))
    if not LOG_DIR.exists():
        return {"entries": []}
    files = sorted(LOG_DIR.glob("runner_*.jsonl"))
    entries = []
    for path in reversed(files):
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for line in reversed(lines):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            entry["time_est"] = _format_est(entry.get("timestamp"))
            entries.append(entry)
            if len(entries) >= limit:
                return {"entries": entries}
    return {"entries": entries}


PAPER_TRADE_DIRS = [
    ROOT / "data" / "paper_trades",
    ROOT.parent / "data" / "paper_trades",
]
_book_lock = threading.Lock()
_book_cache: dict = {"paper": (0.0, None), "live": (0.0, None)}
BOOK_TTL_SECONDS = 20
_wallet_cache: dict = {"at": 0.0, "wallets": None, "error": None}


def _cached_book(kind: str, builder):
    now = time.time()
    with _book_lock:
        cached_at, payload = _book_cache.get(kind, (0.0, None))
        if payload is not None and now - cached_at < BOOK_TTL_SECONDS:
            return payload
    payload = builder()
    with _book_lock:
        _book_cache[kind] = (time.time(), payload)
    return payload


def _paper_fills():
    seen = set()
    fills = []
    for directory in PAPER_TRADE_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.jsonl")):
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                order_id = str(entry.get("order_id") or "")
                if order_id and order_id in seen:
                    continue
                if order_id:
                    seen.add(order_id)
                fills.append(entry)
    try:
        from src.research.top_accounts import load_paper_copy_trades

        for trade in load_paper_copy_trades(limit=200):
            order_id = f"PAPER-COPY-{trade.get('timestamp')}-{trade.get('trader_address')}-{trade.get('condition_id')}"
            if order_id in seen:
                continue
            seen.add(order_id)
            side = str(trade.get("side") or "yes").lower()
            if side not in ("yes", "no"):
                outcome = str(trade.get("outcome") or "").lower()
                side = "no" if outcome.startswith("no") else "yes"
            fills.append(
                {
                    "success": True,
                    "order_id": order_id,
                    "filled_price": trade.get("entry_price"),
                    "filled_quantity": trade.get("shares"),
                    "timestamp": trade.get("timestamp"),
                    "trade": {
                        "platform": "polymarket",
                        "market_id": trade.get("condition_id") or trade.get("title"),
                        "side": side,
                        "action": "buy",
                        "quantity": trade.get("shares"),
                        "price": trade.get("entry_price"),
                        "signal": {
                            "strategy_name": "copy_watchlist",
                            "market_title": trade.get("title"),
                            "metadata": {
                                "copied_account": trade.get("trader_name"),
                                "trader_name": trade.get("trader_name"),
                                "trader_address": trade.get("trader_address"),
                            },
                        },
                    },
                }
            )
    except Exception:
        pass
    runner = _runner
    if runner is not None:
        for result in runner.trade_history:
            entry = result.to_dict()
            order_id = str(entry.get("order_id") or "")
            if not order_id.startswith("PAPER-") or order_id in seen:
                continue
            seen.add(order_id)
            fills.append(entry)
    fills.sort(key=lambda entry: str(entry.get("timestamp") or ""))
    return fills


def _apply_paper_fill(book: dict, entry: dict):
    if not entry.get("success"):
        return
    trade = entry.get("trade") or {}
    signal = trade.get("signal") or {}
    platform = str(trade.get("platform") or "").lower()
    market_id = str(trade.get("market_id") or "")
    side = str(trade.get("side") or "yes").lower()
    action = str(trade.get("action") or "").lower()
    if platform not in ("kalshi", "polymarket") or not market_id or action not in ("buy", "sell"):
        return
    qty = _number(entry.get("filled_quantity"))
    if qty is None:
        qty = _number(trade.get("quantity"))
    price = _number(entry.get("filled_price"))
    if price is None:
        price = _number(trade.get("price"))
    if qty is None or qty <= 0 or price is None:
        return
    signed = qty if action == "buy" else -qty
    key = (platform, market_id, side)
    row = book.get(key)
    if row is None:
        row = {
            "platform": platform,
            "market_id": market_id,
            "title": signal.get("market_title") or market_id,
            "side": side,
            "qty": 0.0,
            "avg_price": 0.0,
            "strategy": signal.get("strategy_name") or "",
            "copied_account": ((signal.get("metadata") or {}).get("copied_account")
                               or (signal.get("metadata") or {}).get("trader_name")
                               or ""),
            "opened_at": entry.get("timestamp"),
        }
        book[key] = row
    current = row["qty"]
    new_qty = current + signed
    same_direction = current == 0 or (current > 0 and signed > 0) or (current < 0 and signed < 0)
    if same_direction and new_qty != 0:
        total = abs(current) * row["avg_price"] + abs(signed) * price
        row["avg_price"] = total / abs(new_qty)
        if current == 0:
            row["opened_at"] = entry.get("timestamp")
            row["strategy"] = signal.get("strategy_name") or row["strategy"]
            row["title"] = signal.get("market_title") or row["title"]
            meta = signal.get("metadata") or {}
            row["copied_account"] = meta.get("copied_account") or meta.get("trader_name") or row.get("copied_account") or ""
    elif abs(signed) < abs(current):
        pass
    elif abs(new_qty) < 1e-9:
        new_qty = 0.0
        row["avg_price"] = 0.0
    else:
        row["avg_price"] = price
        row["opened_at"] = entry.get("timestamp")
        row["strategy"] = signal.get("strategy_name") or row["strategy"]
        row["title"] = signal.get("market_title") or row["title"]
        meta = signal.get("metadata") or {}
        row["copied_account"] = meta.get("copied_account") or meta.get("trader_name") or row.get("copied_account") or ""
    row["qty"] = new_qty


def _quote_map(positions: list[dict]) -> dict:
    quotes = {}
    kalshi_ids = [row["market_id"] for row in positions if row["platform"] == "kalshi"]
    poly_ids = [row["market_id"] for row in positions if row["platform"] == "polymarket"]
    if kalshi_ids:
        try:
            for row in _latest_kalshi(kalshi_ids[:40]):
                quotes[("kalshi", row.get("id"))] = row
        except (requests.RequestException, HTTPException, ValueError, KeyError):
            pass

    def one_poly(market_id: str):
        try:
            return market_id, _latest_polymarket(market_id)
        except (requests.RequestException, HTTPException, ValueError, KeyError):
            return market_id, None

    if poly_ids:
        with ThreadPoolExecutor(max_workers=6) as pool:
            for market_id, row in pool.map(one_poly, poly_ids[:30]):
                if row:
                    quotes[("polymarket", market_id)] = row
    return quotes


def _position_row(raw: dict, quote: dict | None, live_mark: float | None = None) -> dict:
    side = raw["side"]
    size = abs(raw["qty"])
    avg = raw["avg_price"]
    yes_price = None if quote is None else _number(quote.get("yes_price"))
    if live_mark is not None:
        mark = live_mark
    elif yes_price is None:
        mark = None
    elif side == "no":
        mark = round(max(0.0, 1 - yes_price), 4)
    else:
        mark = yes_price
    direction = "long" if raw["qty"] > 0 else "short"
    cost = round(avg * size, 2)
    value = None if mark is None else round(mark * size, 2)
    if mark is None:
        unrealized = None
    elif direction == "long":
        unrealized = round((mark - avg) * size, 2)
    else:
        unrealized = round((avg - mark) * size, 2)
    title = raw.get("title") or raw["market_id"]
    slug = ""
    event_slug = ""
    if quote:
        if quote.get("title"):
            title = quote["title"]
        slug = quote.get("slug") or ""
        event_slug = quote.get("event_slug") or ""
    if raw["platform"] == "polymarket":
        url = raw.get("url") or _polymarket_url(slug, event_slug)
    else:
        url = _kalshi_url(raw["market_id"], raw["market_id"])
    return {
        "platform": raw["platform"],
        "market_id": raw["market_id"],
        "title": title,
        "side": side,
        "direction": direction,
        "size": round(size, 2),
        "avg_price": round(avg, 4) if avg is not None else None,
        "mark_price": None if mark is None else round(mark, 4),
        "cost_usd": cost,
        "value_usd": value,
        "unrealized_usd": unrealized,
        "strategy": raw.get("strategy") or "",
        "copied_account": raw.get("copied_account") or "",
        "opened_at_est": _format_est(raw.get("opened_at")),
        "started_at_est": (quote or {}).get("started_at_est") or _format_est(raw.get("started_at")),
        "ends_at_est": (quote or {}).get("ends_at_est") or _format_est(raw.get("ends_at")),
        "url": url,
    }


def _book_summary(positions: list[dict]) -> dict:
    unrealized = [row["unrealized_usd"] for row in positions if row["unrealized_usd"] is not None]
    values = [row["value_usd"] for row in positions if row["value_usd"] is not None]
    return {
        "positions": len(positions),
        "cost_usd": round(sum(row["cost_usd"] or 0 for row in positions), 2),
        "value_usd": round(sum(values), 2) if values else None,
        "unrealized_usd": round(sum(unrealized), 2) if unrealized else None,
    }


def _build_paper_book() -> dict:
    book: dict = {}
    for entry in _paper_fills():
        _apply_paper_fill(book, entry)
    open_rows = [row for row in book.values() if abs(row["qty"]) > 1e-6]
    quotes = _quote_map(open_rows)
    positions = [
        _position_row(row, quotes.get((row["platform"], row["market_id"])))
        for row in open_rows
    ]
    positions.sort(key=lambda row: (row["platform"], row["title"]))
    return {
        "mode": "paper",
        "summary": _book_summary(positions),
        "positions": positions,
        "errors": [],
        "fetched_at_est": datetime.now(EST).strftime("%b %d, %Y %I:%M %p EST"),
    }


def _polymarket_wallets() -> tuple[list[str], str | None]:
    now = time.time()
    if _wallet_cache["wallets"] is not None and now - _wallet_cache["at"] < 600:
        return _wallet_cache["wallets"], _wallet_cache["error"]
    key = (Config.POLYMARKET_PRIVATE_KEY or "").strip()
    if not key:
        _wallet_cache.update({"at": now, "wallets": [], "error": "Polymarket private key is not set."})
        return [], _wallet_cache["error"]
    try:
        from eth_account import Account

        eoa = Account.from_key(key).address.lower()
    except Exception as exc:
        _wallet_cache.update({"at": now, "wallets": [], "error": f"Polymarket wallet: {exc}"})
        return [], _wallet_cache["error"]
    wallets = [eoa]
    error = None
    try:
        response = requests.get(
            "https://gamma-api.polymarket.com/public-profile",
            params={"address": eoa},
            timeout=12,
        )
        if response.ok:
            body = response.json() if response.content else {}
            if isinstance(body, dict):
                proxy = str(body.get("proxyWallet") or "").strip().lower()
                if re.fullmatch(r"0x[a-f0-9]{40}", proxy) and proxy not in wallets:
                    wallets.append(proxy)
    except requests.RequestException as exc:
        error = f"Polymarket profile: {exc}"
    _wallet_cache.update({"at": now, "wallets": wallets, "error": error})
    return wallets, error


def _polymarket_account_positions(wallets: list[str]) -> tuple[list[dict], list[str]]:
    rows = []
    errors = []
    seen = set()
    for wallet in wallets:
        try:
            response = requests.get(
                "https://data-api.polymarket.com/positions",
                params={
                    "user": wallet,
                    "limit": 100,
                    "sizeThreshold": 0.01,
                    "sortBy": "CURRENT",
                    "sortDirection": "DESC",
                },
                timeout=20,
            )
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException as exc:
            errors.append(f"Polymarket positions: {exc}")
            continue
        if not isinstance(payload, list):
            continue
        for pos in payload:
            asset = str(pos.get("asset") or "")
            if asset and asset in seen:
                continue
            if asset:
                seen.add(asset)
            size = _number(pos.get("size")) or 0.0
            if size <= 0:
                continue
            outcome = str(pos.get("outcome") or "").lower()
            side = "no" if outcome in ("no", "under") or pos.get("outcomeIndex") == 1 else "yes"
            slug = pos.get("slug") or ""
            event_slug = pos.get("eventSlug") or ""
            rows.append(
                {
                    "platform": "polymarket",
                    "market_id": str(pos.get("conditionId") or asset or slug),
                    "title": pos.get("title") or slug or "Polymarket market",
                    "side": side,
                    "qty": size,
                    "avg_price": _number(pos.get("avgPrice")) or 0.0,
                    "mark": _number(pos.get("curPrice")),
                    "opened_at": None,
                    "ends_at": pos.get("endDate"),
                    "url": _polymarket_url(slug, event_slug),
                    "strategy": "",
                }
            )
    return rows, errors


def _kalshi_account_positions() -> tuple[list[dict], list[str]]:
    configured = bool(
        Config.KALSHI_API_KEY and (Config.KALSHI_PRIVATE_KEY_PATH or Config.KALSHI_PRIVATE_KEY_PEM)
    )
    if not configured:
        return [], ["Kalshi credentials are not set."]
    try:
        from src.data_collectors.kalshi_client import KalshiClient

        payload = KalshiClient().get_positions(limit=200, count_filter="position")
    except Exception as exc:
        return [], [f"Kalshi positions: {exc}"]
    raw_rows = payload.get("market_positions") if isinstance(payload, dict) else None
    if raw_rows is None and hasattr(payload, "market_positions"):
        raw_rows = payload.market_positions
    rows = []
    for pos in raw_rows or []:
        if not isinstance(pos, dict):
            pos = pos.to_dict() if hasattr(pos, "to_dict") else getattr(pos, "__dict__", {})
        contracts = _number(pos.get("position")) or 0.0
        if abs(contracts) < 1e-9:
            continue
        size = abs(contracts)
        exposure = _number(pos.get("market_exposure_dollars"))
        if exposure is None and pos.get("market_exposure") is not None:
            exposure = (_number(pos.get("market_exposure")) or 0.0) / 100.0
        avg = (abs(exposure) / size) if exposure is not None and size else 0.0
        updated = pos.get("last_updated_ts")
        opened = updated.isoformat() if hasattr(updated, "isoformat") else (str(updated) if updated else None)
        rows.append(
            {
                "platform": "kalshi",
                "market_id": str(pos.get("ticker") or ""),
                "title": str(pos.get("ticker") or "Kalshi market"),
                "side": "yes" if contracts > 0 else "no",
                "qty": size,
                "avg_price": avg,
                "mark": None,
                "opened_at": opened,
                "url": None,
                "strategy": "",
            }
        )
    return rows, []


def _build_live_book() -> dict:
    errors = []
    kalshi_rows, kalshi_errors = _kalshi_account_positions()
    errors.extend(kalshi_errors)
    wallets, wallet_error = _polymarket_wallets()
    if wallet_error:
        errors.append(wallet_error)
    poly_rows, poly_errors = _polymarket_account_positions(wallets)
    errors.extend(poly_errors)
    raw_rows = [row for row in kalshi_rows + poly_rows if row.get("market_id")]
    quotes = _quote_map([row for row in raw_rows if row["platform"] == "kalshi"])
    positions = []
    for row in raw_rows:
        quote = quotes.get((row["platform"], row["market_id"]))
        live_mark = row.get("mark")
        if row["platform"] == "polymarket":
            quote = None
        positions.append(_position_row(row, quote, live_mark=live_mark))
    positions.sort(key=lambda row: (row["platform"], row["title"]))
    return {
        "mode": "live",
        "summary": _book_summary(positions),
        "positions": positions,
        "errors": errors,
        "fetched_at_est": datetime.now(EST).strftime("%b %d, %Y %I:%M %p EST"),
    }


@app.get("/api/account/paper")
def paper_book():
    return _cached_book("paper", _build_paper_book)


@app.get("/api/account/live")
def live_book():
    return _cached_book("live", _build_live_book)


_live_lock = threading.Lock()
_live_cache: dict = {"at": 0.0, "payload": None}
LIVE_TTL_SECONDS = 45

_catalog_lock = threading.Lock()
_catalog: dict = {
    "status": "idle",
    "polymarket": [],
    "kalshi": [],
    "fetched_at_est": None,
    "errors": [],
    "built_at": 0.0,
}
CATALOG_TTL_SECONDS = 600


def _number(value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _yes_price_from_outcomes(raw):
    prices = raw
    if isinstance(prices, str):
        try:
            prices = json.loads(prices)
        except json.JSONDecodeError:
            return None
    if not isinstance(prices, list) or not prices:
        return None
    return _number(prices[0])


def _polymarket_row(market: dict) -> dict:
    volume = _number(market.get("volume24hr"))
    if volume is None:
        volume = _number(market.get("volumeNum"))
    return {
        "platform": "polymarket",
        "id": str(market.get("id") or market.get("conditionId") or ""),
        "title": market.get("question") or "",
        "yes_price": _yes_price_from_outcomes(market.get("outcomePrices")),
        "volume": volume,
        "status": "open" if market.get("closed") is not True else "closed",
        "category": market.get("category"),
        "slug": market.get("slug") or "",
        "event_slug": ((market.get("events") or [{}])[0] or {}).get("slug") or "",
        "condition_id": str(market.get("conditionId") or ""),
        "started_at_est": _format_est(market.get("startDate") or market.get("acceptingOrdersTimestamp")),
        "ends_at_est": _format_est(market.get("endDate")),
    }


def _fetch_polymarket(limit: int) -> list[dict]:
    response = requests.get(
        "https://gamma-api.polymarket.com/markets",
        params={
            "active": "true",
            "closed": "false",
            "limit": limit,
            "order": "volume24hr",
            "ascending": "false",
        },
        timeout=25,
    )
    response.raise_for_status()
    return [_polymarket_row(market) for market in response.json()]


def _fetch_all_polymarket() -> list[dict]:
    rows = []
    seen = set()
    offset = 0
    page_size = 100
    while offset < 20000:
        response = requests.get(
            "https://gamma-api.polymarket.com/markets",
            params={
                "active": "true",
                "closed": "false",
                "limit": page_size,
                "offset": offset,
                "order": "volume24hr",
                "ascending": "false",
            },
            timeout=25,
        )
        response.raise_for_status()
        batch = response.json()
        if not isinstance(batch, list) or not batch:
            break
        fresh = 0
        for market in batch:
            row = _polymarket_row(market)
            if not row["id"] or row["id"] in seen:
                continue
            seen.add(row["id"])
            rows.append(row)
            fresh += 1
        with _catalog_lock:
            _catalog["polymarket"] = list(rows)
        if fresh == 0 or len(batch) < page_size:
            break
        offset += page_size
    return rows


def _kalshi_yes_price(market: dict):
    bid = _number(market.get("yes_bid_dollars"))
    ask = _number(market.get("yes_ask_dollars"))
    last = _number(market.get("last_price_dollars"))
    if bid is not None and ask is not None and ask > 0:
        return round((bid + ask) / 2, 4)
    if last is not None and last > 0:
        return last
    if ask is not None and ask > 0:
        return ask
    return last


def _kalshi_row(market: dict) -> dict:
    return {
        "platform": "kalshi",
        "id": market.get("ticker") or "",
        "title": market.get("title") or market.get("yes_sub_title") or "",
        "yes_price": _kalshi_yes_price(market),
        "volume": _number(market.get("volume_fp")),
        "status": market.get("status") or "open",
        "category": market.get("category"),
        "event_ticker": market.get("event_ticker") or "",
        "started_at_est": _format_est(market.get("open_time")),
        "ends_at_est": _format_est(market.get("close_time") or market.get("expiration_time")),
    }


def _fetch_kalshi(limit: int) -> list[dict]:
    response = requests.get(
        "https://api.elections.kalshi.com/trade-api/v2/markets",
        params={"status": "open", "limit": max(limit, 100), "mve_filter": "exclude"},
        timeout=25,
    )
    response.raise_for_status()
    markets = response.json().get("markets") or []
    rows = [_kalshi_row(market) for market in markets]
    rows.sort(key=lambda row: row["volume"] or 0, reverse=True)
    return rows[:limit]


def _fetch_all_kalshi() -> list[dict]:
    rows = []
    seen = set()
    cursor = None
    pages = 0
    while pages < 80:
        params = {"status": "open", "limit": 200, "mve_filter": "exclude"}
        if cursor:
            params["cursor"] = cursor
        response = requests.get(
            "https://api.elections.kalshi.com/trade-api/v2/markets",
            params=params,
            timeout=25,
        )
        response.raise_for_status()
        body = response.json()
        batch = body.get("markets") or []
        if not batch:
            break
        for market in batch:
            row = _kalshi_row(market)
            if not row["id"] or row["id"] in seen:
                continue
            seen.add(row["id"])
            rows.append(row)
        with _catalog_lock:
            _catalog["kalshi"] = list(rows)
        cursor = body.get("cursor") or ""
        pages += 1
        if not cursor:
            break
    return rows


def _build_catalog():
    errors = []
    try:
        _fetch_all_polymarket()
    except requests.RequestException as exc:
        errors.append(f"Polymarket: {exc}")
    try:
        _fetch_all_kalshi()
    except requests.RequestException as exc:
        errors.append(f"Kalshi: {exc}")
    fetched = datetime.now(EST).strftime("%b %d, %Y %I:%M %p EST")
    with _catalog_lock:
        _catalog["status"] = "ready"
        _catalog["fetched_at_est"] = fetched
        _catalog["errors"] = errors
        _catalog["built_at"] = time.time()
        _catalog["polymarket"].sort(key=lambda row: row["volume"] or 0, reverse=True)
        _catalog["kalshi"].sort(key=lambda row: row["volume"] or 0, reverse=True)


def _start_catalog(force: bool = False):
    with _catalog_lock:
        fresh = _catalog["status"] == "ready" and time.time() - _catalog["built_at"] < CATALOG_TTL_SECONDS
        if _catalog["status"] == "loading":
            return
        if fresh and not force:
            return
        _catalog["status"] = "loading"
        if force:
            _catalog["polymarket"] = []
            _catalog["kalshi"] = []
            _catalog["errors"] = []
    thread = threading.Thread(target=_build_catalog, name="market-catalog", daemon=True)
    thread.start()


def _catalog_rows(platform: str | None, query: str | None, family: str | None = None) -> list[dict]:
    with _catalog_lock:
        if platform == "polymarket":
            rows = list(_catalog["polymarket"])
        elif platform == "kalshi":
            rows = list(_catalog["kalshi"])
        else:
            rows = list(_catalog["polymarket"]) + list(_catalog["kalshi"])
    rows.sort(key=lambda row: row["volume"] or 0, reverse=True)
    needle = (query or "").strip().lower()
    if needle:
        rows = [
            row
            for row in rows
            if needle in f"{row['title']} {row['id']} {row.get('category') or ''}".lower()
        ]
    if family:
        rows = [
            row
            for row in rows
            if playbook_for(row.get("platform") or "", row.get("id") or "", row.get("title") or "")["family"] == family
        ]
    return rows


class MarketRef(BaseModel):
    platform: str
    id: str


class LatestRequest(BaseModel):
    markets: list[MarketRef] = Field(min_length=1, max_length=100)


def _latest_polymarket(market_id: str) -> dict:
    response = requests.get(
        f"https://gamma-api.polymarket.com/markets/{market_id}",
        timeout=25,
    )
    response.raise_for_status()
    row = _polymarket_row(response.json())
    return row


def _latest_kalshi(tickers: list[str]) -> list[dict]:
    rows = []
    for start in range(0, len(tickers), 20):
        chunk = tickers[start : start + 20]
        response = requests.get(
            "https://api.elections.kalshi.com/trade-api/v2/markets",
            params={"tickers": ",".join(chunk), "limit": len(chunk)},
            timeout=25,
        )
        response.raise_for_status()
        found = {market.get("ticker"): market for market in response.json().get("markets") or []}
        for ticker in chunk:
            market = found.get(ticker)
            if market is None:
                rows.append({"platform": "kalshi", "id": ticker, "error": "Market not found"})
            else:
                rows.append(_kalshi_row(market))
    return rows


@app.get("/api/markets/catalog")
def market_catalog(
    platform: str | None = None,
    q: str | None = None,
    family: str | None = None,
    offset: int = 0,
    limit: int = 50,
    rebuild: bool = False,
):
    if platform not in (None, "", "kalshi", "polymarket"):
        raise HTTPException(status_code=400, detail="Platform must be kalshi or polymarket")
    platform = platform or None
    _start_catalog(force=rebuild)
    offset = max(0, offset)
    limit = max(1, min(limit, 100))
    with _catalog_lock:
        status_name = _catalog["status"]
        fetched = _catalog["fetched_at_est"]
        errors = list(_catalog["errors"])
        loaded = len(_catalog["polymarket"]) + len(_catalog["kalshi"])
    rows = _catalog_rows(platform, q, family or None)
    page = []
    for row in rows[offset : offset + limit]:
        item = dict(row)
        item["playbook"] = playbook_for(item.get("platform") or "", item.get("id") or "", item.get("title") or "")
        page.append(item)
    return {
        "status": status_name,
        "loaded": loaded,
        "total": len(rows),
        "offset": offset,
        "limit": limit,
        "markets": page,
        "fetched_at_est": fetched,
        "errors": errors,
    }


@app.get("/api/markets/playbooks")
def market_playbooks():
    _start_catalog()
    with _catalog_lock:
        rows = list(_catalog["polymarket"]) + list(_catalog["kalshi"])
        status_name = _catalog["status"]
        fetched = _catalog["fetched_at_est"]
    return {
        "status": status_name,
        "fetched_at_est": fetched,
        "markets": len(rows),
        "families": summarize_playbooks(rows),
    }


@app.post("/api/markets/latest")
def market_latest(body: LatestRequest):
    polymarket_ids = []
    kalshi_ids = []
    seen = set()
    for item in body.markets:
        platform = item.platform.strip().lower()
        market_id = item.id.strip()
        if platform not in ("kalshi", "polymarket") or not market_id:
            raise HTTPException(status_code=400, detail="Each market needs a kalshi or polymarket id")
        key = (platform, market_id)
        if key in seen:
            continue
        seen.add(key)
        if platform == "polymarket":
            polymarket_ids.append(market_id)
        else:
            kalshi_ids.append(market_id)

    rows = []
    errors = []
    if kalshi_ids:
        try:
            rows.extend(_latest_kalshi(kalshi_ids))
        except requests.RequestException as exc:
            errors.append(f"Kalshi: {exc}")
    for market_id in polymarket_ids:
        try:
            rows.append(_latest_polymarket(market_id))
        except requests.RequestException as exc:
            errors.append(f"Polymarket {market_id}: {exc}")
            rows.append({"platform": "polymarket", "id": market_id, "error": "Could not load this market"})
    fetched = datetime.now(EST).strftime("%b %d, %Y %I:%M %p EST")
    for row in rows:
        row["fetched_at_est"] = fetched
    if not rows and errors:
        raise HTTPException(status_code=502, detail="; ".join(errors))
    return {"markets": rows, "fetched_at_est": fetched, "errors": errors}


_history_lock = threading.Lock()
_history_cache: dict[str, dict] = {}
HISTORY_TTL_SECONDS = 180


def _epoch_est(ts: int) -> str:
    return datetime.fromtimestamp(int(ts), EST).strftime("%b %d, %I:%M %p EST")


def _candle_close(candle: dict):
    price = candle.get("price") or {}
    close = _number(price.get("close_dollars"))
    if close is None:
        close = _number(price.get("close"))
    if close is not None and close > 0:
        return close
    bid = _number((candle.get("yes_bid") or {}).get("close_dollars"))
    ask = _number((candle.get("yes_ask") or {}).get("close_dollars"))
    if bid is not None and ask is not None and ask > 0:
        return round((bid + ask) / 2, 4)
    if ask is not None and ask > 0:
        return ask
    return bid


def _history_points(raw: list[tuple[int, float]]) -> list[dict]:
    points = [{"t": ts, "price": price, "time_est": _epoch_est(ts)} for ts, price in raw if price is not None]
    if len(points) <= 80:
        return points
    step = max(1, len(points) // 80)
    trimmed = points[::step]
    if trimmed[-1]["t"] != points[-1]["t"]:
        trimmed.append(points[-1])
    return trimmed


def _polymarket_token(market_id: str) -> str:
    response = requests.get(f"https://gamma-api.polymarket.com/markets/{market_id}", timeout=25)
    response.raise_for_status()
    raw = response.json().get("clobTokenIds")
    if isinstance(raw, str):
        raw = json.loads(raw)
    if not isinstance(raw, list) or not raw:
        raise HTTPException(status_code=404, detail="This Polymarket market has no price series")
    return str(raw[0])


def _polymarket_history(market_id: str) -> dict:
    token = _polymarket_token(market_id)
    response = requests.get(
        "https://clob.polymarket.com/prices-history",
        params={"market": token, "interval": "1w", "fidelity": 30},
        timeout=25,
    )
    response.raise_for_status()
    history = response.json().get("history") or []
    window = "Past week"
    if len(history) < 2:
        response = requests.get(
            "https://clob.polymarket.com/prices-history",
            params={"market": token, "interval": "max", "fidelity": 180},
            timeout=25,
        )
        response.raise_for_status()
        history = response.json().get("history") or []
        window = "Available history"
    points = _history_points([(int(point["t"]), float(point["p"])) for point in history if point.get("t") is not None and point.get("p") is not None])
    return {"window": window, "points": points}


def _kalshi_history(ticker: str) -> dict:
    response = requests.get(f"https://api.elections.kalshi.com/trade-api/v2/markets/{ticker}", timeout=25)
    response.raise_for_status()
    market = response.json().get("market") or {}
    series = str(market.get("event_ticker") or "").split("-")[0]
    if not series:
        raise HTTPException(status_code=404, detail="This Kalshi market has no candlestick series")
    end = int(time.time())
    windows = (
        (60, 14 * 86400, "Past 14 days"),
        (1, 86400, "Past day"),
        (1440, 120 * 86400, "Available history"),
    )
    points: list[dict] = []
    window = windows[-1][2]
    for interval, span, label in windows:
        candle_response = requests.get(
            f"https://api.elections.kalshi.com/trade-api/v2/series/{series}/markets/{ticker}/candlesticks",
            params={"start_ts": end - span, "end_ts": end, "period_interval": interval},
            timeout=25,
        )
        candle_response.raise_for_status()
        candles = candle_response.json().get("candlesticks") or []
        raw = []
        for candle in candles:
            close = _candle_close(candle)
            ts = candle.get("end_period_ts")
            if close is None or ts is None:
                continue
            raw.append((int(ts), close))
        series_points = _history_points(raw)
        if len(series_points) > len(points):
            points = series_points
            window = label
        if len(points) >= 2:
            break
    return {"window": window, "points": points}


@app.get("/api/markets/history")
def market_history(platform: str, id: str):
    platform = platform.strip().lower()
    market_id = id.strip()
    if platform not in ("kalshi", "polymarket") or not market_id:
        raise HTTPException(status_code=400, detail="History needs a kalshi or polymarket id")
    key = f"{platform}:{market_id}"
    now = time.time()
    with _history_lock:
        cached = _history_cache.get(key)
        if cached and now - cached["at"] < HISTORY_TTL_SECONDS:
            return cached["payload"]
    try:
        if platform == "polymarket":
            series = _polymarket_history(market_id)
        else:
            series = _kalshi_history(market_id)
    except HTTPException:
        raise
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    payload = {"platform": platform, "id": market_id, **series}
    with _history_lock:
        _history_cache[key] = {"at": now, "payload": payload}
    return payload


def _lookup_polymarket(market_id: str) -> dict:
    params: list[dict] = []
    if market_id.startswith("0x"):
        params.append({"condition_ids": market_id})
    elif market_id.isdigit():
        params.append({"id": market_id})
    else:
        params.append({"slug": market_id})
        params.append({"id": market_id})
    last_error = None
    for query in params:
        try:
            response = requests.get("https://gamma-api.polymarket.com/markets", params=query, timeout=25)
            response.raise_for_status()
            raw = response.json()
            if isinstance(raw, list):
                raw = raw[0] if raw else {}
            if raw:
                return raw
        except requests.RequestException as exc:
            last_error = exc
    try:
        response = requests.get(f"https://gamma-api.polymarket.com/markets/{market_id}", timeout=25)
        response.raise_for_status()
        raw = response.json()
        if raw:
            return raw
    except requests.RequestException as exc:
        last_error = exc
    if last_error:
        raise last_error
    raise HTTPException(status_code=404, detail="Market not found")


def _polymarket_profile_url(address: str, user_name: str | None = None) -> str:
    handle = (user_name or "").strip().lstrip("@")
    if re.fullmatch(r"[A-Za-z0-9_]{2,32}", handle):
        return f"https://polymarket.com/@{handle}"
    return f"https://polymarket.com/profile/{address}"


def _polymarket_url(slug: str, event_slug: str) -> str | None:
    if event_slug and slug and event_slug != slug:
        return f"https://polymarket.com/event/{event_slug}/{slug}"
    token = event_slug or slug
    if not token:
        return None
    return f"https://polymarket.com/event/{token}"


def _kalshi_url(ticker: str, event_ticker: str) -> str | None:
    series = (event_ticker or ticker).split("-")[0].lower()
    event = (event_ticker or ticker).lower()
    if not series or not event:
        return None
    return f"https://kalshi.com/markets/{series}/{event}"


def _label_prices(names, prices) -> list[dict]:
    if isinstance(names, str):
        try:
            names = json.loads(names)
        except json.JSONDecodeError:
            names = []
    if isinstance(prices, str):
        try:
            prices = json.loads(prices)
        except json.JSONDecodeError:
            prices = []
    if not isinstance(names, list):
        names = []
    if not isinstance(prices, list):
        prices = []
    rows = []
    for index, name in enumerate(names):
        price = _number(prices[index]) if index < len(prices) else None
        rows.append({"name": str(name), "price": price})
    return rows


@app.get("/api/markets/detail")
def market_detail(platform: str, id: str):
    platform = platform.strip().lower()
    market_id = id.strip()
    if platform not in ("kalshi", "polymarket") or not market_id:
        raise HTTPException(status_code=400, detail="Detail needs a kalshi or polymarket id")
    try:
        if platform == "polymarket":
            raw = _lookup_polymarket(market_id)
            event = (raw.get("events") or [{}])[0] or {}
            slug = raw.get("slug") or ""
            event_slug = event.get("slug") or ""
            gamma_id = str(raw.get("id") or market_id)
            history = _polymarket_history(gamma_id)
            row = _polymarket_row(raw)
            detail = {
                **row,
                "description": raw.get("description") or "",
                "end_date": _format_est(raw.get("endDate")),
                "started_at_est": row.get("started_at_est"),
                "ends_at_est": row.get("ends_at_est"),
                "outcomes": _label_prices(raw.get("outcomes"), raw.get("outcomePrices")),
                "url": _polymarket_url(slug, event_slug),
                "url_label": "Open on Polymarket",
                **history,
            }
        else:
            response = requests.get(
                f"https://api.elections.kalshi.com/trade-api/v2/markets/{market_id}",
                timeout=25,
            )
            response.raise_for_status()
            raw = response.json().get("market") or {}
            if not raw:
                raise HTTPException(status_code=404, detail="Market not found")
            history = _kalshi_history(market_id)
            event_ticker = raw.get("event_ticker") or ""
            detail = {
                **_kalshi_row(raw),
                "description": raw.get("rules_primary") or raw.get("rules_secondary") or "",
                "end_date": _format_est(raw.get("close_time") or raw.get("expiration_time")),
                "started_at_est": _format_est(raw.get("open_time")),
                "ends_at_est": _format_est(raw.get("close_time") or raw.get("expiration_time")),
                "outcomes": [
                    {"name": "Yes", "price": _kalshi_yes_price(raw)},
                    {
                        "name": "No",
                        "price": None
                        if _kalshi_yes_price(raw) is None
                        else round(1 - _kalshi_yes_price(raw), 4),
                    },
                ],
                "yes_bid": _number(raw.get("yes_bid_dollars")),
                "yes_ask": _number(raw.get("yes_ask_dollars")),
                "url": _kalshi_url(market_id, event_ticker),
                "url_label": "Open on Kalshi",
                **history,
            }
    except HTTPException:
        raise
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    detail["fetched_at_est"] = datetime.now(EST).strftime("%b %d, %Y %I:%M %p EST")
    return detail


def _wallet_address(address: str) -> str:
    raw = (address or "").strip().lower()
    match = re.search(r"0x[a-f0-9]{40}", raw)
    if not match:
        raise HTTPException(status_code=400, detail="Address must be a 0x wallet")
    return match.group(0)


def _trade_time(value) -> str | None:
    if value is None or value == "":
        return None
    if isinstance(value, str) and not value.isdigit():
        return _format_est(value)
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number > 1e12:
        number = number / 1000.0
    return _epoch_est(int(number))


@app.get("/api/accounts/trades")
def account_trades(address: str, name: str | None = None, limit: int = 100):
    wallet = _wallet_address(address)
    limit = max(1, min(limit, 200))
    trades = []
    closed = []
    errors = []
    try:
        response = requests.get(
            "https://data-api.polymarket.com/trades",
            params={"user": wallet, "limit": limit},
            timeout=25,
        )
        response.raise_for_status()
        raw = response.json()
        if not isinstance(raw, list):
            raw = []
        for trade in raw:
            slug = trade.get("slug") or ""
            event_slug = trade.get("eventSlug") or ""
            size = _number(trade.get("size"))
            price = _number(trade.get("price"))
            notional = None if size is None or price is None else round(size * price, 2)
            trades.append(
                {
                    "title": trade.get("title") or slug or "Market",
                    "outcome": trade.get("outcome") or "",
                    "side": trade.get("side") or "",
                    "price": price,
                    "size": size,
                    "notional": notional,
                    "time_est": _trade_time(trade.get("timestamp")),
                    "url": _polymarket_url(slug, event_slug),
                }
            )
    except requests.RequestException as exc:
        errors.append(f"Trades: {exc}")
    try:
        response = requests.get(
            "https://data-api.polymarket.com/v1/closed-positions",
            params={"user": wallet, "limit": limit, "sortBy": "TIMESTAMP", "sortDirection": "DESC"},
            timeout=25,
        )
        response.raise_for_status()
        raw = response.json()
        if not isinstance(raw, list):
            raw = []
        for pos in raw:
            avg_price = _number(pos.get("avgPrice")) or 0.0
            total_bought = _number(pos.get("totalBought")) or 0.0
            realized = _number(pos.get("realizedPnl")) or 0.0
            cost = avg_price * total_bought if avg_price > 0 and total_bought > 0 else 0.0
            slug = pos.get("slug") or ""
            event_slug = pos.get("eventSlug") or ""
            closed.append(
                {
                    "title": pos.get("title") or slug or "Market",
                    "outcome": pos.get("outcome") or "",
                    "avg_price": avg_price,
                    "cost_usd": round(cost, 2),
                    "realized_pnl": realized,
                    "roi_pct": round(realized / cost * 100.0, 1) if cost > 0 else None,
                    "closed_at_est": _trade_time(pos.get("timestamp") or pos.get("endDate")),
                    "ends_at_est": _format_est(pos.get("endDate")),
                    "url": _polymarket_url(slug, event_slug),
                }
            )
    except requests.RequestException as exc:
        errors.append(f"Closed positions: {exc}")
    return {
        "address": wallet,
        "profile_url": _polymarket_profile_url(wallet, name),
        "trades": trades,
        "closed": closed,
        "errors": errors,
    }


def _live_markets(platform: str | None, limit: int) -> dict:
    now = time.time()
    with _live_lock:
        cached = _live_cache["payload"]
        if cached and now - _live_cache["at"] < LIVE_TTL_SECONDS:
            payload = cached
        else:
            errors = []
            try:
                polymarket = _fetch_polymarket(limit)
            except requests.RequestException as exc:
                polymarket = []
                errors.append(f"Polymarket: {exc}")
            try:
                kalshi = _fetch_kalshi(limit)
            except requests.RequestException as exc:
                kalshi = []
                errors.append(f"Kalshi: {exc}")
            fetched = datetime.now(EST).strftime("%b %d, %Y %I:%M %p EST")
            payload = {
                "polymarket": polymarket,
                "kalshi": kalshi,
                "fetched_at_est": fetched,
                "errors": errors,
            }
            _live_cache["at"] = now
            _live_cache["payload"] = payload

    if platform == "polymarket":
        selected = payload["polymarket"][:limit]
    elif platform == "kalshi":
        selected = payload["kalshi"][:limit]
    else:
        selected = (payload["polymarket"][:limit] + payload["kalshi"][:limit])[: limit * 2]
    for row in selected:
        row["fetched_at_est"] = payload["fetched_at_est"]
    return {
        "markets": selected,
        "live": True,
        "fetched_at_est": payload["fetched_at_est"],
        "errors": payload["errors"],
    }


@app.get("/api/markets")
def markets(platform: str | None = None, limit: int = 40):
    limit = max(1, min(limit, 100))
    return _live_markets(platform, limit)


@app.get("/api/runner")
def runner_state():
    runner = _runner
    if runner is None:
        return {
            "loaded": False,
            "running": False,
            "summary": None,
            "signals": [],
            "trades": [],
        }
    thread = runner._runner_thread
    return {
        "loaded": True,
        "running": bool(thread and thread.is_alive()),
        "summary": runner.get_performance_summary(),
        "signals": runner.get_recent_signals(limit=20),
        "trades": runner.get_recent_trades(limit=20),
    }


@app.post("/api/runner/start")
def start_runner(body: RunnerStart):
    runner = _get_runner()
    runner.paper_trading = body.paper_trading
    runner.start(interval=body.interval_seconds)
    return {"running": True, "paper_trading": runner.paper_trading, "interval_seconds": body.interval_seconds}


@app.post("/api/runner/stop")
def stop_runner():
    if _runner is None:
        return {"running": False}
    _runner.stop()
    return {"running": False}


@app.post("/api/runner/cycle")
def run_cycle():
    runner = _get_runner()
    try:
        stats = runner.run_cycle()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {
        "time_est": stats.timestamp.replace(tzinfo=EST).strftime("%b %d, %Y %I:%M %p EST")
        if stats.timestamp.tzinfo is None
        else stats.timestamp.astimezone(EST).strftime("%b %d, %Y %I:%M %p EST"),
        "duration_ms": round(stats.cycle_duration_ms, 1),
        "signals_generated": stats.signals_generated,
        "trades_executed": stats.trades_executed,
        "successful_trades": stats.successful_trades,
        "failed_trades": stats.failed_trades,
        "by_strategy": stats.by_strategy,
    }


_investigation_lock = threading.Lock()
_investigation_state = {
    "running": False,
    "started_at_est": None,
    "last_error": None,
}


class InvestigateRequest(BaseModel):
    time_period: str = Field(default="ALL")
    count: int = Field(default=16, ge=4, le=40)
    model: str = Field(default="llama3.2:latest")


class AnalyzeWalletRequest(BaseModel):
    address: str
    time_period: str = Field(default="ALL")
    model: str = Field(default="llama3.2:latest")


class WatchlistToggleRequest(BaseModel):
    address: str
    user_name: str = ""
    archetype: str = ""
    copyability_score: int = 7
    pnl: float = 0.0
    volume: float = 0.0
    max_position_usd: float = 100.0
    max_price_drift: float = 0.05


class CopyTradeRequest(BaseModel):
    copy_all_followed: bool = False
    trader_address: str = ""
    trader_name: str = ""
    condition_id: str = ""
    title: str = ""
    outcome: str = "Yes"
    side: str = "yes"
    price: float = 0.5
    trader_avg_price: float = 0.5
    amount_usd: float = Field(default=100.0, gt=0, le=50000)
    max_price_drift: float = Field(default=0.06, ge=-1.0, le=1.0)


@app.get("/api/accounts/top")
def top_accounts():
    from src.research.top_accounts import (
        TOP_ACCOUNTS_PATH,
        build_copyable_signals,
        build_investigation_synthesis,
        enrich_account_dossier,
        load_paper_copy_trades,
        load_watchlist,
    )

    watchlist = load_watchlist()
    followed_set = {
        (item.get("address") or "").strip().lower()
        for item in watchlist.get("accounts", [])
        if item.get("enabled", True)
    }

    if not TOP_ACCOUNTS_PATH.exists():
        return {
            "status": "running" if _investigation_state["running"] else "empty",
            "investigation_running": _investigation_state["running"],
            "generated_at_est": None,
            "synthesis": None,
            "accounts": [],
            "copy_signals": [],
            "watchlist": watchlist,
            "paper_copy_trades": load_paper_copy_trades(limit=40),
        }

    try:
        payload = json.loads(TOP_ACCOUNTS_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to read top accounts: {exc}") from exc

    accounts = payload.get("accounts") or []
    for acc in accounts:
        acc["is_followed"] = (acc.get("address") or "").strip().lower() in followed_set
        enrich_account_dossier(acc)

    signals = build_copyable_signals(accounts, followed_addresses=followed_set)
    synthesis = payload.get("synthesis") or build_investigation_synthesis(accounts)

    return {
        "status": "ready",
        "investigation_running": _investigation_state["running"],
        "last_error": _investigation_state["last_error"],
        "generated_at_est": payload.get("generated_at_est"),
        "time_period": payload.get("time_period", "ALL"),
        "llm_model": payload.get("llm_model", "llama3.2:latest"),
        "pool_scanned": payload.get("pool_scanned", len(accounts)),
        "synthesis": synthesis,
        "accounts": accounts,
        "copy_signals": signals,
        "watchlist": watchlist,
        "paper_copy_trades": load_paper_copy_trades(limit=40),
    }


@app.post("/api/accounts/investigate")
def start_accounts_investigation(body: InvestigateRequest):
    from src.research.top_accounts import now_est_str, run_top_accounts_investigation

    period = body.time_period.upper()
    if period not in ("DAY", "WEEK", "MONTH", "ALL"):
        raise HTTPException(status_code=400, detail="time_period must be DAY, WEEK, MONTH, or ALL")

    with _investigation_lock:
        if _investigation_state["running"]:
            return {
                "running": True,
                "started_at_est": _investigation_state["started_at_est"],
            }
        _investigation_state["running"] = True
        _investigation_state["started_at_est"] = now_est_str()
        _investigation_state["last_error"] = None

    def _worker():
        try:
            run_top_accounts_investigation(
                time_period=period,
                max_candidates=body.count,
                model=body.model,
                save=True,
            )
        except Exception as exc:
            _investigation_state["last_error"] = str(exc)
        finally:
            with _investigation_lock:
                _investigation_state["running"] = False

    thread = threading.Thread(target=_worker, name="top-accounts-investigator", daemon=True)
    thread.start()
    return {
        "running": True,
        "started_at_est": _investigation_state["started_at_est"],
        "time_period": period,
        "count": body.count,
        "model": body.model,
    }


@app.post("/api/accounts/analyze")
def analyze_single_account(body: AnalyzeWalletRequest):
    from src.research.top_accounts import (
        TOP_ACCOUNTS_PATH,
        build_copyable_signals,
        build_investigation_synthesis,
        enrich_account_dossier,
        investigate_single_wallet,
        load_watchlist,
        now_est_str,
    )

    addr = body.address.strip().lower()
    if not addr.startswith("0x") or len(addr) < 10:
        raise HTTPException(status_code=400, detail="Provide a valid 0x wallet address")

    try:
        profile = investigate_single_wallet(
            address=addr,
            time_period=body.time_period.upper(),
            model=body.model,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    watchlist = load_watchlist()
    followed_set = {
        (item.get("address") or "").strip().lower()
        for item in watchlist.get("accounts", [])
        if item.get("enabled", True)
    }
    profile["is_followed"] = addr in followed_set
    enrich_account_dossier(profile)

    if TOP_ACCOUNTS_PATH.exists():
        try:
            payload = json.loads(TOP_ACCOUNTS_PATH.read_text(encoding="utf-8"))
        except Exception:
            payload = {"accounts": []}
    else:
        payload = {"accounts": []}

    accounts = [a for a in (payload.get("accounts") or []) if (a.get("address") or "").lower() != addr]
    accounts.insert(0, profile)
    payload["accounts"] = accounts
    payload["generated_at_est"] = now_est_str()
    payload["synthesis"] = build_investigation_synthesis(accounts)
    payload["copy_signals"] = build_copyable_signals(accounts, followed_addresses=followed_set)
    TOP_ACCOUNTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOP_ACCOUNTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return {"account": profile}


@app.post("/api/accounts/watchlist/toggle")
def toggle_account_watchlist(body: WatchlistToggleRequest):
    from src.research.top_accounts import load_watchlist, now_est_str, save_watchlist

    addr = body.address.strip().lower()
    if not addr:
        raise HTTPException(status_code=400, detail="Address is required")

    watchlist = load_watchlist()
    accounts = watchlist.get("accounts") or []
    existing = next((a for a in accounts if (a.get("address") or "").lower() == addr), None)
    if existing:
        accounts = [a for a in accounts if (a.get("address") or "").lower() != addr]
        followed = False
    else:
        accounts.append(
            {
                "address": addr,
                "user_name": body.user_name or f"{addr[:6]}...{addr[-4:]}",
                "archetype": body.archetype,
                "copyability_score": body.copyability_score,
                "pnl": body.pnl,
                "volume": body.volume,
                "max_position_usd": body.max_position_usd,
                "max_price_drift": body.max_price_drift,
                "enabled": True,
                "added_at_est": now_est_str(),
            }
        )
        followed = True

    watchlist["accounts"] = accounts
    saved = save_watchlist(watchlist)
    return {"followed": followed, "watchlist": saved}


@app.post("/api/accounts/copy-trade")
def execute_paper_copy_trade(body: CopyTradeRequest):
    from src.research.top_accounts import (
        TOP_ACCOUNTS_PATH,
        build_copyable_signals,
        load_watchlist,
        record_paper_copy_trade,
    )

    executed = []
    if body.copy_all_followed:
        if not TOP_ACCOUNTS_PATH.exists():
            raise HTTPException(status_code=400, detail="Top accounts investigation not loaded yet")
        payload = json.loads(TOP_ACCOUNTS_PATH.read_text(encoding="utf-8"))
        watchlist = load_watchlist()
        followed_set = {
            (item.get("address") or "").strip().lower()
            for item in watchlist.get("accounts", [])
            if item.get("enabled", True)
        }
        if not followed_set:
            raise HTTPException(status_code=400, detail="No accounts are currently selected in the copy watchlist")

        signals = build_copyable_signals(payload.get("accounts") or [], followed_addresses=followed_set)
        qualifying = [
            s
            for s in signals
            if s.get("is_followed_trader") and s.get("price_drift", 0.0) <= body.max_price_drift
        ][:10]
        for sig in qualifying:
            price = float(sig.get("current_price") or 0.5)
            shares = round(body.amount_usd / price, 2) if price > 0 else 0.0
            entry = record_paper_copy_trade(
                {
                    "trader_address": sig["trader_address"],
                    "trader_name": sig["trader_name"],
                    "condition_id": sig["condition_id"],
                    "title": sig["title"],
                    "outcome": sig["outcome"],
                    "side": sig["side"],
                    "entry_price": round(price, 4),
                    "trader_avg_price": round(float(sig.get("trader_avg_price") or price), 4),
                    "price_drift": round(float(sig.get("price_drift") or 0.0), 4),
                    "amount_usd": round(body.amount_usd, 2),
                    "shares": shares,
                }
            )
            executed.append(entry)
        return {"executed_count": len(executed), "trades": executed}

    if not body.title and not body.condition_id:
        raise HTTPException(status_code=400, detail="Provide a market position to copy")

    price = max(0.01, min(0.99, float(body.price or 0.5)))
    shares = round(body.amount_usd / price, 2)
    drift = round(price - float(body.trader_avg_price or price), 4)
    entry = record_paper_copy_trade(
        {
            "trader_address": body.trader_address,
            "trader_name": body.trader_name or body.trader_address[:10],
            "condition_id": body.condition_id,
            "title": body.title,
            "outcome": body.outcome,
            "side": body.side,
            "entry_price": round(price, 4),
            "trader_avg_price": round(float(body.trader_avg_price or price), 4),
            "price_drift": drift,
            "amount_usd": round(body.amount_usd, 2),
            "shares": shares,
        }
    )
    executed.append(entry)
    return {"executed_count": 1, "trades": executed}

