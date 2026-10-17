"""HTTP API for the information markets dashboard."""
import json
import sys
import threading
import time
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
    if _chart_cache["mtime"] != mtime or _chart_cache["payload"] is None:
        _chart_cache["payload"] = load_chart_payload(ROOT / "data" / "eda")
        _chart_cache["mtime"] = mtime
    return _chart_cache["payload"]


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

