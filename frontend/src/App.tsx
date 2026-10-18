import { useEffect, useRef, useState } from "react";
import EdaBoard from "./eda.tsx";

type Loose = Record<string, any>;

type Market = {
  platform: string;
  id: string;
  title?: string;
  volume?: number | null;
  yes_price?: number | null;
  fetched_at_est?: string;
  started_at_est?: string;
  ends_at_est?: string;
  end_date?: string;
  error?: string;
  slug?: string;
  event_slug?: string;
  condition_id?: string;
  playbook?: {
    api?: string;
    cost?: string;
    strategy?: string;
    endpoint?: string;
    label?: string;
    family?: string;
  };
};

type CatalogResponse = {
  status?: string;
  loaded?: number;
  total?: number;
  markets?: Market[];
  fetched_at_est?: string;
};

type PlaybookFamily = {
  family: string;
  label: string;
  markets: number;
};

type PlaybookResponse = {
  families?: PlaybookFamily[];
  fetched_at_est?: string;
  markets?: number;
  status?: string;
};

const TABS = [
  { id: "overview", label: "Overview" },
  { id: "live", label: "Live trading" },
  { id: "paper", label: "Paper trading" },
  { id: "accounts", label: "Top Accounts" },
  { id: "copy-markets", label: "Copy markets" },
  { id: "markets", label: "Markets" },
  { id: "eda", label: "EDA" },
  { id: "strategies", label: "Strategies" },
  { id: "logs", label: "Logs" },
];

async function getJson<T = Loose>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(path, options);
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = typeof body?.detail === "string" ? body.detail : "";
    throw new Error(detail || `Request failed (${response.status})`);
  }
  return body as T;
}

function money(value: unknown): string {
  if (value === null || value === undefined || value === "") return "--";
  const number = Number(value);
  if (Number.isNaN(number)) return String(value);
  return number.toLocaleString("en-US", { maximumFractionDigits: 2 });
}

function pct(value: unknown, digits = 1): string {
  if (value === null || value === undefined || value === "") return "--";
  const number = Number(value);
  if (Number.isNaN(number)) return String(value);
  return `${number.toFixed(digits)}%`;
}

function price(value: unknown): string {
  if (value === null || value === undefined || value === "") return "--";
  const number = Number(value);
  if (Number.isNaN(number)) return String(value);
  return number.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 3 });
}

type HistoryPoint = { t: number; price: number; time_est: string };

function PriceChart({ points, compact = false }: { points: HistoryPoint[]; compact?: boolean }) {
  const width = compact ? 148 : 640;
  const height = compact ? 46 : 168;
  const pad = compact
    ? { left: 4, right: 4, top: 4, bottom: 4 }
    : { left: 36, right: 12, top: 12, bottom: 22 };
  if (points.length < 2) {
    return <span className="muted">No price history yet</span>;
  }
  const prices = points.map((point) => point.price);
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  const span = max - min || 0.05;
  const innerW = width - pad.left - pad.right;
  const innerH = height - pad.top - pad.bottom;
  const xOf = (index: number) => pad.left + (index / (points.length - 1)) * innerW;
  const yOf = (value: number) => pad.top + (1 - (value - min) / span) * innerH;
  const line = points.map((point, index) => `${xOf(index)},${yOf(point.price)}`).join(" ");
  const last = points[points.length - 1];
  return (
    <svg className={compact ? "spark" : "price-chart"} viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Yes price history">
      {compact ? null : (
        <>
          <text x={4} y={pad.top + 4} className="axis">{max.toFixed(2)}</text>
          <text x={4} y={height - pad.bottom} className="axis">{min.toFixed(2)}</text>
          <text x={width - pad.right} y={height - 4} textAnchor="end" className="axis">{last.time_est}</text>
        </>
      )}
      <polyline points={line} className="actual" />
    </svg>
  );
}

function nowEst(): string {
  const stamp = new Date().toLocaleString("en-US", {
    timeZone: "America/New_York",
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  });
  return `${stamp} EST`;
}

function dollars(value: unknown): string {
  if (value === null || value === undefined || value === "") return "--";
  const number = Number(value);
  if (Number.isNaN(number)) return String(value);
  const formatted = Math.abs(number).toLocaleString("en-US", { maximumFractionDigits: 2 });
  return number < 0 ? `-$${formatted}` : `$${formatted}`;
}

function asEst(value: unknown): string {
  if (value === null || value === undefined || value === "") return "";
  const text = String(value);
  if (text.includes("EST")) return text;
  const parsed = new Date(text.includes("T") ? text : text.replace(" ", "T"));
  if (Number.isNaN(parsed.getTime())) return text;
  const stamp = parsed.toLocaleString("en-US", {
    timeZone: "America/New_York",
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  });
  return `${stamp} EST`;
}

function marketStart(market: Loose): string {
  return asEst(market.started_at_est || market.start_date || market.startDate) || "--";
}

function marketEnd(market: Loose): string {
  return asEst(market.ends_at_est || market.end_date || market.endDate) || "--";
}

function MarketWindow({ market }: { market: Loose }) {
  return (
    <div className="muted">
      Started {marketStart(market)}
      <br />
      Ends {marketEnd(market)}
    </div>
  );
}

function shortAddr(addr: string | null | undefined): string {
  if (!addr || addr.length < 12) return addr || "--";
  return `${addr.slice(0, 6)}...${addr.slice(-4)}`;
}

function AccountBook({ mode, book }: { mode: "live" | "paper"; book: Loose | null }) {
  const positions: Loose[] = book?.positions || [];
  const summary = book?.summary;
  const live = mode === "live";
  return (
    <>
      <div className="grid">
        <div className="card">
          <span>Open positions</span>
          <strong>{summary ? summary.positions : "--"}</strong>
        </div>
        <div className="card">
          <span>Cost</span>
          <strong>{summary ? dollars(summary.cost_usd) : "--"}</strong>
        </div>
        <div className="card">
          <span>Mark value</span>
          <strong>{summary ? dollars(summary.value_usd) : "--"}</strong>
        </div>
        <div className="card">
          <span>Unrealized</span>
          <strong className={Number(summary?.unrealized_usd) < 0 ? "bad" : Number(summary?.unrealized_usd) > 0 ? "good" : ""}>
            {summary ? dollars(summary.unrealized_usd) : "--"}
          </strong>
        </div>
      </div>
      <section className="panel">
        <h2>{live ? "Live account" : "Paper account"}</h2>
        <p className="muted">
          {live
            ? "Open positions on the Kalshi and Polymarket accounts configured for this desk."
            : "Open paper positions, netted from simulated fills. Copy-watchlist and copy-top-trader fills name the source account."}
        </p>
        <p className="muted">{book?.fetched_at_est ? `Updated ${book.fetched_at_est}.` : "Loading the account book."}</p>
        {Array.isArray(book?.errors) && book.errors.length > 0 ? (
          <p className="error">{book.errors.join(" ")}</p>
        ) : null}
        {book === null ? (
          <p className="muted">Loading positions.</p>
        ) : positions.length === 0 ? (
          <p className="muted">
            {live
              ? "No open live positions on this account."
              : "No open paper positions. Start the paper runner or run a cycle to create some."}
          </p>
        ) : (
          <div className="market-list">
            <table>
              <thead>
                <tr>
                  <th>Platform</th>
                  <th>Market</th>
                  <th>Side</th>
                  <th>Size</th>
                  <th>Avg entry</th>
                  <th>Mark</th>
                  <th>Cost</th>
                  <th>Unrealized</th>
                  {live ? null : <th>Strategy</th>}
                  {live ? null : <th>Copied from</th>}
                  <th>Opened</th>
                </tr>
              </thead>
              <tbody>
                {positions.map((row) => (
                  <tr key={`${row.platform}-${row.market_id}-${row.side}`}>
                    <td>{row.platform}</td>
                    <td>
                      {row.url ? (
                        <a className="external" href={row.url} target="_blank" rel="noopener noreferrer">
                          {row.title}
                        </a>
                      ) : (
                        row.title
                      )}
                      <MarketWindow market={row} />
                    </td>
                    <td>
                      {row.direction === "short" ? "Short " : ""}
                      {String(row.side || "").toUpperCase()}
                    </td>
                    <td>{money(row.size)}</td>
                    <td>{price(row.avg_price)}</td>
                    <td>{price(row.mark_price)}</td>
                    <td>{dollars(row.cost_usd)}</td>
                    <td className={Number(row.unrealized_usd) < 0 ? "bad" : Number(row.unrealized_usd) > 0 ? "good" : ""}>
                      {dollars(row.unrealized_usd)}
                    </td>
                    {live ? null : <td>{row.strategy || "--"}</td>}
                    {live ? null : <td>{row.copied_account || "—"}</td>}
                    <td>{row.opened_at_est || "--"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </>
  );
}

export default function App() {
  const [tab, setTab] = useState("overview");
  const [status, setStatus] = useState<Loose | null>(null);
  const [runner, setRunner] = useState<Loose | null>(null);
  const [strategies, setStrategies] = useState<Loose[]>([]);
  const [logs, setLogs] = useState<Loose[]>([]);
  const [liveBook, setLiveBook] = useState<Loose | null>(null);
  const [paperBook, setPaperBook] = useState<Loose | null>(null);
  const [favorites, setFavorites] = useState<Loose | null>(null);
  const [backtests, setBacktests] = useState<Loose | null>(null);
  const [charts, setCharts] = useState<Loose | null>(null);
  const [topAccountsData, setTopAccountsData] = useState<Loose | null>(null);
  const [accountSort, setAccountSort] = useState("rov");
  const [cohortFilter, setCohortFilter] = useState("all");
  const [accountPeriod, setAccountPeriod] = useState("ALL");
  const [selectedAddress, setSelectedAddress] = useState("");
  const [accountPage, setAccountPage] = useState(false);
  const [customWallet, setCustomWallet] = useState("");
  const [copyAmountUsd, setCopyAmountUsd] = useState("100");
  const [platform, setPlatform] = useState("polymarket");
  const [family, setFamily] = useState("");
  const [playbooks, setPlaybooks] = useState<PlaybookResponse | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [refreshedAt, setRefreshedAt] = useState("");
  const [catalog, setCatalog] = useState<CatalogResponse | null>(null);
  const [marketQuery, setMarketQuery] = useState("");
  const [marketPage, setMarketPage] = useState(0);
  const [followed, setFollowed] = useState<Market[]>(() => {
    try {
      const saved = JSON.parse(localStorage.getItem("followed-markets") || "[]");
      return Array.isArray(saved) ? saved : [];
    } catch {
      return [];
    }
  });
  const [latest, setLatest] = useState<Market[]>([]);
  const [latestAt, setLatestAt] = useState("");
  const [histories, setHistories] = useState<Record<string, { window?: string; points: HistoryPoint[]; error?: string }>>({});
  const [marketDetail, setMarketDetail] = useState<Loose | null>(null);
  const [detailBusy, setDetailBusy] = useState(false);
  const [accountTrades, setAccountTrades] = useState<Loose[] | null>(null);
  const [accountClosed, setAccountClosed] = useState<Loose[] | null>(null);
  const [accountProfileUrl, setAccountProfileUrl] = useState("");
  const historyRequested = useRef(new Set<string>());
  const pageSize = 50;

  async function refresh() {
    const [nextStatus, nextRunner, nextStrategies, nextLogs, nextFavorites, nextBacktests, nextCharts, nextAccounts] =
      await Promise.all([
        getJson("/api/status"),
        getJson("/api/runner"),
        getJson("/api/strategies"),
        getJson("/api/logs?limit=30"),
        getJson("/api/eda/favorites").catch(() => null),
        getJson("/api/eda/backtests").catch(() => null),
        getJson("/api/eda/charts").catch(() => null),
        getJson("/api/accounts/top").catch(() => null),
      ]);
    setStatus(nextStatus);
    setRunner(nextRunner);
    setStrategies(nextStrategies.strategies);
    setLogs(nextLogs.entries);
    setFavorites(nextFavorites);
    setBacktests(nextBacktests);
    setCharts(nextCharts);
    if (nextAccounts) {
      setTopAccountsData(nextAccounts);
    }
    setRefreshedAt(nowEst());
    setError("");
  }

  async function refreshOverview() {
    setBusy(true);
    setError("");
    try {
      await refresh();
      const books = await getJson<PlaybookResponse>("/api/markets/playbooks").catch(() => null);
      if (books) setPlaybooks(books);
      await loadCatalog(marketPage, true);
      if (followed.length > 0) await loadLatest(false);
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setBusy(false);
    }
  }

  async function loadCatalog(page = marketPage, rebuild = false) {
    const params = new URLSearchParams({
      limit: String(pageSize),
      offset: String(page * pageSize),
    });
    if (platform) params.set("platform", platform);
    if (family) params.set("family", family);
    if (marketQuery.trim()) params.set("q", marketQuery.trim());
    if (rebuild) params.set("rebuild", "true");
    const body = await getJson(`/api/markets/catalog?${params}`);
    setCatalog(body);
    return body;
  }

  useEffect(() => {
    if (tab !== "live" && tab !== "paper") return undefined;
    let cancelled = false;
    const path = tab === "live" ? "/api/account/live" : "/api/account/paper";
    const apply = tab === "live" ? setLiveBook : setPaperBook;
    const load = () => {
      getJson(path)
        .then((body) => {
          if (!cancelled) apply(body);
        })
        .catch((err) => {
          if (cancelled) return;
          const message = errorMessage(err);
          setError(message);
          apply((current: Loose | null) => current || { positions: [], summary: null, errors: [message] });
        });
    };
    load();
    const timer = setInterval(load, 15000);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [tab]);

  useEffect(() => {
    refresh().catch((err) => setError(err.message));
    const timer = setInterval(() => {
      refresh().catch((err) => setError(err.message));
    }, 8000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    localStorage.setItem("followed-markets", JSON.stringify(followed));
  }, [followed]);

  useEffect(() => {
    if (tab !== "markets") return undefined;
    let cancelled = false;
    getJson("/api/markets/playbooks")
      .then((body) => {
        if (!cancelled) setPlaybooks(body);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      });
    return () => {
      cancelled = true;
    };
  }, [tab, catalog?.status]);

  useEffect(() => {
    if (tab !== "markets") return undefined;
    let cancelled = false;
    loadCatalog(marketPage).catch((err) => {
      if (!cancelled) setError(err.message);
    });
    return () => {
      cancelled = true;
    };
  }, [tab, platform, family, marketQuery, marketPage]);

  useEffect(() => {
    if (tab !== "markets" || catalog?.status !== "loading") return undefined;
    const timer = setInterval(() => {
      loadCatalog(marketPage).catch((err) => setError(err.message));
    }, 2000);
    return () => clearInterval(timer);
  }, [tab, catalog?.status, platform, family, marketQuery, marketPage]);

function errorMessage(err: unknown): string {
  return err instanceof Error ? err.message : "Request failed";
}

async function act(path: string, body?: Loose) {
    setBusy(true);
    setError("");
    try {
      const res = await getJson(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: body ? JSON.stringify(body) : undefined,
      });
      await refresh();
      return res;
    } catch (err) {
      setError(errorMessage(err));
      return null;
    } finally {
      setBusy(false);
    }
  }

  async function handleAnalyzeWallet(addressToAnalyze?: string) {
    const target = (addressToAnalyze || customWallet).trim();
    if (!target) return;
    const res = await act("/api/accounts/analyze", {
      address: target,
      time_period: accountPeriod,
      model: "llama3.2:latest",
    });
    if (res?.account?.address) {
      openAccount(res.account.address);
      if (!addressToAnalyze) setCustomWallet("");
    }
  }

  async function handleToggleWatchlist(account: Loose) {
    await act("/api/accounts/watchlist/toggle", {
      address: account.address,
      user_name: account.user_name,
      archetype: account.llm_analysis?.archetype || "",
      copyability_score: account.llm_analysis?.copyability_score || 7,
      pnl: account.pnl || 0,
      volume: account.volume || 0,
      max_position_usd: Number(copyAmountUsd) || 100,
      max_price_drift: 0.05,
    });
  }

  async function handleCopyPosition(signalOrPos: Loose, trader?: Loose) {
    const traderAddress = signalOrPos.trader_address || trader?.address || "";
    const traderName = signalOrPos.trader_name || trader?.user_name || "";
    const curPrice = signalOrPos.current_price ?? signalOrPos.cur_price ?? 0.5;
    const avgPrice = signalOrPos.trader_avg_price ?? signalOrPos.avg_price ?? curPrice;
    await act("/api/accounts/copy-trade", {
      copy_all_followed: false,
      trader_address: traderAddress,
      trader_name: traderName,
      condition_id: signalOrPos.condition_id || "",
      title: signalOrPos.title || "",
      outcome: signalOrPos.outcome || "Yes",
      side: signalOrPos.side || "yes",
      price: curPrice,
      trader_avg_price: avgPrice,
      amount_usd: Number(copyAmountUsd) || 100,
    });
  }

  function marketKey(market: Market) {
    return `${market.platform}:${market.id}`;
  }

  function walletAddress(value: string) {
    const match = String(value || "").toLowerCase().match(/0x[a-f0-9]{40}/);
    return match ? match[0] : String(value || "").toLowerCase();
  }

  function polymarketProfileUrl(address: string, name?: string) {
    const handle = String(name || "").trim().replace(/^@/, "");
    if (/^[A-Za-z0-9_]{2,32}$/.test(handle)) {
      return `https://polymarket.com/@${handle}`;
    }
    return `https://polymarket.com/profile/${walletAddress(address)}`;
  }

  function openAccount(address: string) {
    setSelectedAddress(walletAddress(address));
    setAccountPage(true);
    setTab("accounts");
  }

  function closeAccountPage() {
    setAccountPage(false);
  }

  function normalizeTitle(value: unknown) {
    return String(value || "")
      .trim()
      .toLowerCase()
      .replace(/[^\w\s]/g, "")
      .replace(/\s+/g, " ");
  }

  function marketMatchesPosition(market: Loose, position: Loose) {
    const condition = String(market.condition_id || "").toLowerCase();
    const posCondition = String(position.condition_id || "").toLowerCase();
    if (condition && posCondition && condition === posCondition) return true;
    const slugs = [market.slug, market.event_slug, market.id].filter(Boolean).map((item) => String(item).toLowerCase());
    const posSlugs = [position.slug, position.event_slug].filter(Boolean).map((item) => String(item).toLowerCase());
    if (slugs.some((slug) => posSlugs.includes(slug))) return true;
    const marketTitle = normalizeTitle(market.title);
    const posTitle = normalizeTitle(position.title);
    return Boolean(marketTitle && posTitle && marketTitle === posTitle);
  }

  function holdersOnMarket(market: Loose) {
    const holders: Loose[] = [];
    rawAccounts.forEach((account) => {
      (account.open_positions || []).forEach((position: Loose) => {
        if (!marketMatchesPosition(market, position)) return;
        holders.push({
          ...position,
          trader_address: account.address,
          trader_name: account.user_name,
          trader_archetype: account.llm_analysis?.archetype || "",
          copyability_score: account.llm_analysis?.copyability_score,
          is_followed_trader: Boolean(account.is_followed),
          earning_cohort_label: account.earning_cohort_label,
        });
      });
    });
    return holders.sort((a, b) => Number(b.is_followed_trader) - Number(a.is_followed_trader) || (b.current_value || 0) - (a.current_value || 0));
  }

  function liveTopAccountMarkets() {
    const groups = new Map<string, Loose>();
    rawAccounts.forEach((account) => {
      (account.open_positions || []).forEach((position: Loose) => {
        const key = String(position.condition_id || position.slug || position.title || "").toLowerCase();
        if (!key) return;
        if (!groups.has(key)) {
          groups.set(key, {
            platform: "polymarket",
            id: position.condition_id || position.slug || position.title,
            condition_id: position.condition_id,
            slug: position.slug,
            title: position.title,
            end_date: position.end_date,
            holders: [],
          });
        }
        groups.get(key).holders.push({
          ...position,
          trader_address: account.address,
          trader_name: account.user_name,
          trader_archetype: account.llm_analysis?.archetype || "",
          copyability_score: account.llm_analysis?.copyability_score,
          is_followed_trader: Boolean(account.is_followed),
          earning_cohort_label: account.earning_cohort_label,
        });
      });
    });
    return [...groups.values()]
      .map((item) => ({
        ...item,
        holders: item.holders.sort(
          (a: Loose, b: Loose) => Number(b.is_followed_trader) - Number(a.is_followed_trader) || (b.current_value || 0) - (a.current_value || 0),
        ),
      }))
      .sort((a, b) => b.holders.length - a.holders.length || (b.holders[0]?.current_value || 0) - (a.holders[0]?.current_value || 0));
  }

  function HolderTable({ holders }: { holders: Loose[] }) {
    if (holders.length === 0) {
      return <p className="muted">No investigated top account is in this market right now.</p>;
    }
    return (
      <div className="market-list">
        <table>
          <thead>
            <tr>
              <th>Account</th>
              <th>Outcome</th>
              <th>Their entry</th>
              <th>Current</th>
              <th>Drift</th>
              <th>Size</th>
              <th>Unrealized</th>
              <th>Copy</th>
            </tr>
          </thead>
          <tbody>
            {holders.map((holder, index) => (
              <tr key={`${holder.trader_address}-${holder.outcome}-${index}`}>
                <td>
                  <button className="linkish" onClick={() => openAccount(holder.trader_address)}>
                    {holder.trader_name}
                  </button>
                  <div className="muted">
                    {holder.is_followed_trader ? "On your copy list" : holder.earning_cohort_label || ""}
                    {holder.copyability_score ? ` | ${holder.copyability_score}/10` : ""}
                  </div>
                </td>
                <td>{holder.outcome}</td>
                <td>{price(holder.avg_price)}</td>
                <td>{price(holder.cur_price)}</td>
                <td className={holder.price_drift <= 0.03 ? "good" : holder.price_drift > 0.1 ? "bad" : ""}>
                  {holder.price_drift > 0 ? `+${Number(holder.price_drift).toFixed(3)}` : Number(holder.price_drift || 0).toFixed(3)}
                </td>
                <td>${money(holder.current_value)}</td>
                <td className={holder.cash_pnl >= 0 ? "good" : "bad"}>
                  ${money(holder.cash_pnl)} ({pct(holder.percent_pnl, 1)})
                </td>
                <td>
                  <button disabled={busy || holder.copyable === false} onClick={() => handleCopyPosition(holder)}>
                    {holder.copyable === false ? "Settling" : `Paper copy ($${copyAmountUsd})`}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  async function openMarketDetail(market: Market) {
    setTab("markets");
    setDetailBusy(true);
    setMarketDetail({
      platform: market.platform,
      id: market.id,
      title: market.title,
      playbook: market.playbook,
      started_at_est: market.started_at_est,
      ends_at_est: market.ends_at_est || market.end_date,
    });
    try {
      const body = await getJson<Loose>(
        `/api/markets/detail?platform=${encodeURIComponent(market.platform)}&id=${encodeURIComponent(market.id)}`,
      );
      setMarketDetail({ ...body, playbook: market.playbook });
      setHistories((current) => ({
        ...current,
        [marketKey(market)]: { window: body.window, points: body.points || [] },
      }));
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setDetailBusy(false);
    }
  }

  async function loadHistory(market: Market) {
    const key = marketKey(market);
    const body = await getJson<{ window?: string; points?: HistoryPoint[] }>(
      `/api/markets/history?platform=${encodeURIComponent(market.platform)}&id=${encodeURIComponent(market.id)}`,
    );
    setHistories((current) => ({
      ...current,
      [key]: { window: body.window, points: body.points || [] },
    }));
  }

  function isFollowed(market: Market) {
    return followed.some((item) => item.platform === market.platform && item.id === market.id);
  }

  function toggleFollow(market: Market) {
    setFollowed((current) => {
      if (current.some((item) => item.platform === market.platform && item.id === market.id)) {
        return current.filter((item) => !(item.platform === market.platform && item.id === market.id));
      }
      return [...current, {
        platform: market.platform,
        id: market.id,
        title: market.title || market.id,
        started_at_est: market.started_at_est,
        ends_at_est: market.ends_at_est,
      }];
    });
  }

  function togglePage(marketsOnPage: Market[]) {
    const keys = new Set(marketsOnPage.map(marketKey));
    const allOn = marketsOnPage.every((market) => isFollowed(market));
    setFollowed((current) => {
      if (allOn) {
        return current.filter((item) => !keys.has(marketKey(item)));
      }
      const next = current.filter((item) => !keys.has(marketKey(item)));
      return [
        ...next,
        ...marketsOnPage.map((market) => ({
          platform: market.platform,
          id: market.id,
          title: market.title || market.id,
          started_at_est: market.started_at_est,
          ends_at_est: market.ends_at_est,
        })),
      ];
    });
  }

  async function loadLatest(manageBusy = true) {
    if (followed.length === 0) return;
    if (manageBusy) {
      setBusy(true);
      setError("");
    }
    try {
      const titles = new Map(followed.map((item) => [marketKey(item), item.title]));
      const collected: Market[] = [];
      let fetchedAt = "";
      for (let index = 0; index < followed.length; index += 80) {
        const chunk = followed.slice(index, index + 80);
        const body = await getJson<{ markets?: Market[]; fetched_at_est?: string }>("/api/markets/latest", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            markets: chunk.map((item) => ({ platform: item.platform, id: item.id })),
          }),
        });
        collected.push(...(body.markets || []));
        fetchedAt = body.fetched_at_est || fetchedAt;
      }
      setLatest(
        collected.map((market) => ({
          ...market,
          title: market.title || titles.get(marketKey(market)) || market.id,
        })),
      );
      setLatestAt(fetchedAt);
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      if (manageBusy) setBusy(false);
    }
  }

  const summary = runner?.summary;
  const historyKey = [...(catalog?.markets || []), ...latest].map((market) => marketKey(market)).join("|");
  useEffect(() => {
    if (tab !== "markets" || !historyKey) return undefined;
    const wanted = [...(catalog?.markets || []), ...latest];
    const missing = wanted.filter((market) => !historyRequested.current.has(marketKey(market)));
    if (missing.length === 0) return undefined;
    missing.forEach((market) => historyRequested.current.add(marketKey(market)));
    const queue = [...missing];
    async function worker() {
      while (queue.length > 0) {
        const market = queue.shift();
        if (!market) break;
        try {
          await loadHistory(market);
        } catch (err) {
          setHistories((current) => ({
            ...current,
            [marketKey(market)]: { points: [], error: errorMessage(err) },
          }));
        }
      }
    }
    void Promise.all([worker(), worker(), worker()]);
    return undefined;
  }, [tab, historyKey]);

  const catalogMarkets = catalog?.markets || [];
  const catalogTotal = catalog?.total || 0;
  const pageCount = Math.max(1, Math.ceil(catalogTotal / pageSize));

  const rawAccounts: Loose[] = Array.isArray(topAccountsData?.accounts) ? topAccountsData.accounts : [];
  const liveAccountMarkets = liveTopAccountMarkets();
  const filteredAccounts = rawAccounts
    .filter((acc) => {
      if (cohortFilter === "pct") return acc.earning_cohort === "pct_earner" || acc.earning_cohort === "both";
      if (cohortFilter === "volume") return acc.earning_cohort === "volume_earner" || acc.earning_cohort === "both";
      if (cohortFilter === "followed") return Boolean(acc.is_followed);
      return true;
    })
    .slice()
    .sort((a, b) => {
      if (accountSort === "rov") return (b.return_on_volume_pct || 0) - (a.return_on_volume_pct || 0);
      if (accountSort === "realized_roi") return (b.realized_roi_pct ?? -999) - (a.realized_roi_pct ?? -999);
      if (accountSort === "volume") return (b.volume || 0) - (a.volume || 0);
      if (accountSort === "pnl") return (b.pnl || 0) - (a.pnl || 0);
      if (accountSort === "win_rate") return (b.win_rate_pct ?? -1) - (a.win_rate_pct ?? -1);
      if (accountSort === "copyability") {
        return (
          (b.llm_analysis?.copyability_score || 0) - (a.llm_analysis?.copyability_score || 0) ||
          (b.return_on_volume_pct || 0) - (a.return_on_volume_pct || 0)
        );
      }
      return 0;
    });

  const selectedAccount =
    rawAccounts.find((a) => walletAddress(a.address) === walletAddress(selectedAddress)) || null;
  const synthesis = topAccountsData?.synthesis;
  const copySignals: Loose[] = Array.isArray(topAccountsData?.copy_signals) ? topAccountsData.copy_signals : [];
  const paperCopyTrades: Loose[] = Array.isArray(topAccountsData?.paper_copy_trades) ? topAccountsData.paper_copy_trades : [];
  const followedAccountsCount = rawAccounts.filter((a) => a.is_followed).length;

  useEffect(() => {
    const address = selectedAddress || selectedAccount?.address;
    if (tab !== "accounts" || !accountPage || !address) {
      return undefined;
    }
    let cancelled = false;
    setAccountTrades(null);
    setAccountClosed(null);
    const wallet = walletAddress(address);
    setAccountProfileUrl(polymarketProfileUrl(wallet, selectedAccount?.user_name));
    const params = new URLSearchParams({ address: wallet, limit: "120" });
    if (selectedAccount?.user_name) params.set("name", selectedAccount.user_name);
    getJson<{ trades?: Loose[]; closed?: Loose[]; profile_url?: string }>(
      `/api/accounts/trades?${params}`,
    )
      .then((body) => {
        if (cancelled) return;
        setAccountTrades(body.trades || []);
        setAccountClosed(body.closed || []);
        if (body.profile_url) setAccountProfileUrl(body.profile_url);
      })
      .catch((err) => {
        if (!cancelled) {
          setAccountTrades([]);
          setAccountClosed([]);
          setError(errorMessage(err));
        }
      });
    return () => {
      cancelled = true;
    };
  }, [tab, accountPage, selectedAddress, selectedAccount?.address]);

  return (
    <div className="app">
      <header>
        <div>
          <h1>Information Markets</h1>
          <p className="sub">Paper trading desk for Kalshi and Polymarket strategies.</p>
        </div>
      </header>

      <div className="tabs">
        {TABS.map((item) => (
          <button
            key={item.id}
            className={tab === item.id ? "active" : ""}
            onClick={() => setTab(item.id)}
          >
            {item.label}
          </button>
        ))}
      </div>

      {error ? <p className="error">{error}</p> : null}

      {tab === "overview" && (
        <>
          <div className="grid">
            <div className="card">
              <span>Runner</span>
              <strong>{status?.runner_running ? "Running" : "Stopped"}</strong>
            </div>
            <div className="card">
              <span>Mode</span>
              <strong>{status?.paper_trading ? "Paper" : "Live"}</strong>
            </div>
            <div className="card">
              <span>Trades today</span>
              <strong>
                {status?.trades_today ?? 0} / {status?.max_daily_trades ?? "--"}
              </strong>
            </div>
            <div className="card">
              <span>Paper P&amp;L</span>
              <strong>{summary ? money(summary.paper_pnl) : "--"}</strong>
            </div>
          </div>
          <section className="panel">
            <div className="row">
              <button disabled={busy} onClick={() => act("/api/runner/start", { interval_seconds: 30, paper_trading: true })}>
                Start paper runner
              </button>
              <button disabled={busy} onClick={() => act("/api/runner/cycle")}>
                Run one cycle
              </button>
              <button disabled={busy} onClick={() => act("/api/runner/stop")}>
                Stop
              </button>
              <button disabled={busy} onClick={() => refreshOverview()}>
                {busy ? "Refreshing" : "Refresh"}
              </button>
            </div>
            <p className="muted">{refreshedAt ? `Updated ${refreshedAt}.` : "Waiting for the first update."}</p>
            <p className="muted">
              {status
                ? `Kalshi credentials ${status.kalshi_configured ? "are set" : "are missing"}. Polymarket credentials ${status.polymarket_configured ? "are set" : "are missing"}.`
                : "Checking credentials."}{" "}
              Cycles read the local market cache and will not place live orders while paper mode is on.
            </p>
            {summary ? (
              <p className="muted">
                {summary.total_signals} signals, {summary.total_trades} trades,{" "}
                {(summary.success_rate * 100).toFixed(0)}% success across {summary.run_cycles} cycles.
              </p>
            ) : (
              <p className="muted">No in-memory cycle yet. Start the runner or run one cycle.</p>
            )}
          </section>
        </>
      )}

      {(tab === "live" || tab === "paper") && (
        <AccountBook
          mode={tab}
          book={tab === "live" ? liveBook : paperBook}
        />
      )}

      {tab === "accounts" && accountPage && (
        <section className="panel" id="account-page">
          <div className="inspector-header">
            <div>
              <h2>{selectedAccount?.user_name || selectedAddress}</h2>
              <p className="muted">{walletAddress(selectedAccount?.address || selectedAddress)}</p>
            </div>
            <div className="row">
              <button onClick={closeAccountPage}>Back to accounts</button>
              {selectedAccount ? (
                <button onClick={() => handleToggleWatchlist(selectedAccount)}>
                  {selectedAccount.is_followed ? "Remove from Copy Watchlist" : "Add to Copy Watchlist"}
                </button>
              ) : null}
              <button disabled={busy} onClick={() => handleAnalyzeWallet(selectedAddress)}>
                Re-run LLM Analysis
              </button>
              <a
                className="external"
                href={polymarketProfileUrl(selectedAddress, selectedAccount?.user_name)}
                target="_blank"
                rel="noopener noreferrer"
              >
                Open on Polymarket
              </a>
            </div>
          </div>
          {selectedAccount ? (
            <>
              <div className="grid">
                <div className="card">
                  <span>LLM Strategy Archetype</span>
                  <strong>{selectedAccount.llm_analysis?.archetype || "--"}</strong>
                  <span className="muted">Edge: {selectedAccount.llm_analysis?.edge_source || "--"}</span>
                </div>
                <div className="card">
                  <span>Return on Volume vs Realized ROI</span>
                  <strong className="good">
                    {pct(selectedAccount.return_on_volume_pct, 2)} / {pct(selectedAccount.realized_roi_pct, 1)}
                  </strong>
                  <span className="muted">
                    ${money(selectedAccount.pnl)} net on ${money(selectedAccount.volume)} volume
                  </span>
                </div>
                <div className="card">
                  <span>Win Rate</span>
                  <strong>
                    {pct(selectedAccount.win_rate_pct, 1)} ({selectedAccount.wins}W/{selectedAccount.losses}L)
                  </strong>
                </div>
                <div className="card">
                  <span>Copyability</span>
                  <strong>{selectedAccount.llm_analysis?.copyability_score || "--"}/10</strong>
                </div>
              </div>
              <div className="llm-box">
                <p>
                  <strong>LLM Strategy Summary:</strong> {selectedAccount.llm_analysis?.strategy_summary}
                </p>
                <p>
                  <strong>Copy Recommendation:</strong> {selectedAccount.llm_analysis?.copy_recommendation}
                </p>
              </div>
            </>
          ) : (
            <p className="muted">Loading this wallet from Polymarket. The live bets below do not need a prior investigation.</p>
          )}

          <div className="subpanel">
            <h2>Previous bets</h2>
            {accountClosed === null ? (
              <p className="muted">Loading closed positions.</p>
            ) : accountClosed.length === 0 ? (
              <p className="muted">No closed positions returned for this wallet.</p>
            ) : (
              <div className="market-list">
                <table>
                  <thead>
                    <tr>
                      <th>Closed (EST)</th>
                      <th>Market</th>
                      <th>Outcome</th>
                      <th>Avg entry</th>
                      <th>Cost</th>
                      <th>Realized PnL</th>
                      <th>ROI</th>
                    </tr>
                  </thead>
                  <tbody>
                    {accountClosed.map((pos, index) => (
                      <tr key={`${pos.title}-${pos.closed_at_est}-${index}`}>
                        <td>{pos.closed_at_est || "--"}</td>
                        <td>
                          {pos.url ? (
                            <a className="external" href={pos.url} target="_blank" rel="noreferrer">
                              {pos.title}
                            </a>
                          ) : (
                            pos.title
                          )}
                          <MarketWindow market={pos} />
                        </td>
                        <td>{pos.outcome || "--"}</td>
                        <td>{price(pos.avg_price)}</td>
                        <td>${money(pos.cost_usd)}</td>
                        <td className={pos.realized_pnl >= 0 ? "good" : "bad"}>${money(pos.realized_pnl)}</td>
                        <td className={(pos.roi_pct || 0) >= 0 ? "good" : "bad"}>{pos.roi_pct == null ? "--" : pct(pos.roi_pct, 1)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          <div className="subpanel">
            <h2>Recent trades</h2>
            {accountTrades === null ? (
              <p className="muted">Loading trades from Polymarket.</p>
            ) : accountTrades.length === 0 ? (
              <p className="muted">No recent trades returned for this wallet.</p>
            ) : (
              <div className="market-list">
                <table>
                  <thead>
                    <tr>
                      <th>Time (EST)</th>
                      <th>Market</th>
                      <th>Side</th>
                      <th>Outcome</th>
                      <th>Price</th>
                      <th>Size</th>
                      <th>Notional</th>
                    </tr>
                  </thead>
                  <tbody>
                    {accountTrades.map((trade, index) => (
                      <tr key={`${trade.title}-${trade.time_est}-${index}`}>
                        <td>{trade.time_est || "--"}</td>
                        <td>
                          {trade.url ? (
                            <a className="external" href={trade.url} target="_blank" rel="noreferrer">
                              {trade.title}
                            </a>
                          ) : (
                            trade.title
                          )}
                        </td>
                        <td>{trade.side || "--"}</td>
                        <td>{trade.outcome || "--"}</td>
                        <td>{price(trade.price)}</td>
                        <td>{money(trade.size)}</td>
                        <td>${money(trade.notional)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {selectedAccount?.open_positions?.length > 0 && (
            <div className="subpanel">
              <h2>Open positions</h2>
              <HolderTable
                holders={selectedAccount.open_positions.map((pos: Loose) => ({
                  ...pos,
                  trader_address: selectedAccount.address,
                  trader_name: selectedAccount.user_name,
                  is_followed_trader: Boolean(selectedAccount.is_followed),
                  earning_cohort_label: selectedAccount.earning_cohort_label,
                  copyability_score: selectedAccount.llm_analysis?.copyability_score,
                }))}
              />
            </div>
          )}
        </section>
      )}

      {tab === "accounts" && !accountPage && (
        <>
          <div className="grid">
            <div className="card">
              <span>Top % Return (Profit / Vol)</span>
              <strong className="good">
                {synthesis?.leaders?.top_pct_rov
                  ? `${synthesis.leaders.top_pct_rov.user_name} (${pct(synthesis.leaders.top_pct_rov.return_on_volume_pct, 2)})`
                  : "--"}
              </strong>
              <span className="muted">
                {synthesis?.leaders?.top_pct_rov
                  ? `$${money(synthesis.leaders.top_pct_rov.pnl)} PnL on $${money(synthesis.leaders.top_pct_rov.volume)} Vol`
                  : ""}
              </span>
            </div>
            <div className="card">
              <span>Top Volume Whale</span>
              <strong>
                {synthesis?.leaders?.top_volume
                  ? `${synthesis.leaders.top_volume.user_name} ($${money(synthesis.leaders.top_volume.volume)})`
                  : "--"}
              </strong>
              <span className="muted">
                {synthesis?.leaders?.top_volume
                  ? `${pct(synthesis.leaders.top_volume.return_on_volume_pct, 2)} margin ($${money(synthesis.leaders.top_volume.pnl)} PnL)`
                  : ""}
              </span>
            </div>
            <div className="card">
              <span>Top Net Profit ($)</span>
              <strong className="good">
                {synthesis?.leaders?.top_pnl
                  ? `${synthesis.leaders.top_pnl.user_name} ($${money(synthesis.leaders.top_pnl.pnl)})`
                  : "--"}
              </strong>
              <span className="muted">
                {synthesis?.leaders?.top_pnl
                  ? `${pct(synthesis.leaders.top_pnl.return_on_volume_pct, 2)} RoV on $${money(synthesis.leaders.top_pnl.volume)} Vol`
                  : ""}
              </span>
            </div>
            <div className="card">
              <span>Copied Accounts &amp; Signals</span>
              <strong>
                {followedAccountsCount} followed / {copySignals.length} signals
              </strong>
              <span className="muted">
                {topAccountsData?.generated_at_est
                  ? `Updated ${topAccountsData.generated_at_est}`
                  : "Investigation running"}
              </span>
            </div>
          </div>

          {synthesis && (
            <section className="panel">
              <h2>% ROI Earners vs. Volume Whales: Investigation Findings</h2>
              <p className="muted">
                Scanned {topAccountsData?.pool_scanned || 0} leaderboard accounts ({topAccountsData?.time_period || "ALL"}) and profiled{" "}
                {synthesis.total_accounts_investigated} accounts with Ollama ({topAccountsData?.llm_model || "llama3.2:latest"}) as of{" "}
                {topAccountsData?.generated_at_est || "--"}.
              </p>
              <div className="grid compact-grid">
                <div className="card">
                  <span>% Earners Avg Return / Vol</span>
                  <strong className="good">{pct(synthesis.pct_earners_avg_rov_pct, 2)}</strong>
                  <span className="muted">
                    Win rate: {pct(synthesis.pct_earners_avg_win_rate_pct, 1)} | Copyability: {synthesis.pct_earners_avg_copyability ?? "--"}/10
                  </span>
                </div>
                <div className="card">
                  <span>Volume Whales Avg Return / Vol</span>
                  <strong>{pct(synthesis.vol_earners_avg_rov_pct, 2)}</strong>
                  <span className="muted">
                    Win rate: {pct(synthesis.vol_earners_avg_win_rate_pct, 1)} | Copyability: {synthesis.vol_earners_avg_copyability ?? "--"}/10
                  </span>
                </div>
              </div>
              <ul className="findings-list">
                {(synthesis.key_findings || []).map((finding: string, idx: number) => (
                  <li key={idx}>{finding}</li>
                ))}
              </ul>
            </section>
          )}

          <section className="panel">
            <div className="row">
              <label htmlFor="account-sort">Rank by</label>
              <select
                id="account-sort"
                value={accountSort}
                onChange={(e) => setAccountSort(e.target.value)}
              >
                <option value="rov">% Return on Volume (Profit / Vol)</option>
                <option value="realized_roi">Realized ROI % (Closed Positions)</option>
                <option value="volume">Total Volume ($)</option>
                <option value="pnl">Total Net Profit ($)</option>
                <option value="win_rate">Win Rate (%)</option>
                <option value="copyability">LLM Copyability Score</option>
              </select>

              <label htmlFor="cohort-filter">Cohort</label>
              <select
                id="cohort-filter"
                value={cohortFilter}
                onChange={(e) => setCohortFilter(e.target.value)}
              >
                <option value="all">All Investigated ({rawAccounts.length})</option>
                <option value="pct">Top % Earners</option>
                <option value="volume">Top Volume Whales</option>
                <option value="followed">Copy Watchlist ({followedAccountsCount})</option>
              </select>

              <label htmlFor="account-period">Window</label>
              <select
                id="account-period"
                value={accountPeriod}
                onChange={(e) => setAccountPeriod(e.target.value)}
              >
                <option value="ALL">All-Time + Monthly Active</option>
                <option value="MONTH">Monthly Leaders</option>
                <option value="WEEK">Weekly Leaders</option>
                <option value="DAY">Daily Leaders</option>
              </select>

              <button
                disabled={busy || topAccountsData?.investigation_running}
                onClick={() =>
                  act("/api/accounts/investigate", {
                    time_period: accountPeriod,
                    count: 16,
                    model: "llama3.2:latest",
                  })
                }
              >
                {topAccountsData?.investigation_running ? "LLM Investigation Running..." : "Refresh LLM Investigation"}
              </button>
            </div>

            <div className="row">
              <input
                value={customWallet}
                placeholder="Paste any 0x Polymarket wallet address to investigate with LLM"
                onChange={(e) => setCustomWallet(e.target.value)}
              />
              <button disabled={busy || !customWallet.trim()} onClick={() => handleAnalyzeWallet()}>
                Analyze Wallet with LLM
              </button>
              <label htmlFor="copy-size">Paper copy size ($)</label>
              <input
                id="copy-size"
                type="number"
                className="small-input"
                min="10"
                max="10000"
                value={copyAmountUsd}
                onChange={(e) => setCopyAmountUsd(e.target.value)}
              />
              <button
                disabled={busy || followedAccountsCount === 0}
                onClick={() =>
                  act("/api/accounts/copy-trade", {
                    copy_all_followed: true,
                    amount_usd: Number(copyAmountUsd) || 100,
                    max_price_drift: 0.06,
                  })
                }
              >
                Paper Copy All Followed Signals
              </button>
            </div>

            <div className="market-list">
              <table>
                <thead>
                  <tr>
                    <th>Copy</th>
                    <th>Account</th>
                    <th>Cohort</th>
                    <th>Net PnL ($)</th>
                    <th>Volume ($)</th>
                    <th>Return / Vol (%)</th>
                    <th>Realized ROI (%)</th>
                    <th>Win Rate</th>
                    <th>LLM Strategy Archetype</th>
                    <th>Copyability</th>
                    <th>Inspect</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredAccounts.map((acc) => {
                    const llm = acc.llm_analysis || {};
                    const isSelected = selectedAccount?.address === acc.address;
                    return (
                      <tr key={acc.address} className={isSelected ? "selected-row pick" : "pick"} onClick={() => openAccount(acc.address)}>
                        <td onClick={(event) => event.stopPropagation()}>
                          <input
                            type="checkbox"
                            checked={Boolean(acc.is_followed)}
                            aria-label={`Copy ${acc.user_name}`}
                            onChange={() => handleToggleWatchlist(acc)}
                          />
                        </td>
                        <td>
                          <button className="linkish" onClick={() => openAccount(acc.address)}>
                            {acc.user_name}
                          </button>
                          <div className="muted">{shortAddr(acc.address)}</div>
                        </td>
                        <td>
                          <span className={`badge badge-${acc.earning_cohort}`}>
                            {acc.earning_cohort_label}
                          </span>
                        </td>
                        <td className={acc.pnl >= 0 ? "good" : "bad"}>${money(acc.pnl)}</td>
                        <td>${money(acc.volume)}</td>
                        <td className={acc.return_on_volume_pct >= 10 ? "good" : ""}>
                          {pct(acc.return_on_volume_pct, 2)}
                        </td>
                        <td className={(acc.realized_roi_pct || 0) >= 0 ? "good" : "bad"}>
                          {acc.realized_roi_pct !== null && acc.realized_roi_pct !== undefined
                            ? pct(acc.realized_roi_pct, 1)
                            : "--"}
                        </td>
                        <td>
                          {acc.win_rate_pct !== null && acc.win_rate_pct !== undefined
                            ? `${pct(acc.win_rate_pct, 1)} (${acc.wins}W/${acc.losses}L)`
                            : "--"}
                        </td>
                        <td>
                          <div>{llm.archetype || "--"}</div>
                          <div className="muted">
                            Topic: {acc.patterns?.dominant_topic || "--"} | Avg entry: {price(acc.patterns?.avg_entry_price)}
                          </div>
                        </td>
                        <td
                          className={
                            (llm.copyability_score || 0) >= 7
                              ? "good"
                              : (llm.copyability_score || 0) <= 3
                                ? "bad"
                                : ""
                          }
                        >
                          {llm.copyability_score ? `${llm.copyability_score}/10 (${llm.copyability_label})` : "--"}
                        </td>
                        <td>
                          <button onClick={() => openAccount(acc.address)}>Open</button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </section>

          <section className="panel">
            <h2>Actionable Copy Signals Across Top Accounts</h2>
            <p className="muted">
              Live open positions held by investigated accounts where the market is still active (price between 0.03 and 0.95) and current price has not drifted more than +0.12 past the trader&apos;s average entry.
            </p>
            {copySignals.length === 0 ? (
              <p className="muted">No qualifying open positions at this moment.</p>
            ) : (
              <div className="market-list">
                <table>
                  <thead>
                    <tr>
                      <th>Trader</th>
                      <th>Market</th>
                      <th>Outcome</th>
                      <th>Trader Entry</th>
                      <th>Current Price</th>
                      <th>Drift</th>
                      <th>Whale Size</th>
                      <th>Signal Score</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {copySignals.slice(0, 30).map((sig, index) => (
                      <tr key={`${sig.trader_address}-${sig.condition_id}-${index}`}>
                        <td>
                          <strong>{sig.trader_name}</strong>
                          <div className="muted">
                            RoV {pct(sig.trader_return_on_volume_pct, 1)} | Copy {sig.copyability_score}/10
                          </div>
                        </td>
                        <td>
                          {sig.title}
                          <MarketWindow market={sig} />
                          <div className="muted">{sig.recommended_action}</div>
                        </td>
                        <td>{sig.outcome}</td>
                        <td>{price(sig.trader_avg_price)}</td>
                        <td>{price(sig.current_price)}</td>
                        <td className={sig.price_drift <= 0.02 ? "good" : ""}>
                          {sig.price_drift > 0 ? `+${sig.price_drift.toFixed(3)}` : sig.price_drift.toFixed(3)}
                        </td>
                        <td>${money(sig.trader_position_value_usd)}</td>
                        <td className={sig.signal_score >= 6.5 ? "good" : ""}>{sig.signal_score}</td>
                        <td>
                          <button disabled={busy} onClick={() => handleCopyPosition(sig)}>
                            Paper Copy (${copyAmountUsd})
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>

          {paperCopyTrades.length > 0 && (
            <section className="panel">
              <h2>Paper Copy Trade Log</h2>
              <table>
                <thead>
                  <tr>
                    <th>Executed (EST)</th>
                    <th>Copied Trader</th>
                    <th>Market</th>
                    <th>Outcome</th>
                    <th>Entry Price</th>
                    <th>Trader Avg</th>
                    <th>Amount ($)</th>
                    <th>Shares</th>
                  </tr>
                </thead>
                <tbody>
                  {paperCopyTrades.map((trade, index) => (
                    <tr key={`${trade.timestamp}-${index}`}>
                      <td>{trade.executed_at_est}</td>
                      <td>{trade.trader_name}</td>
                      <td>{trade.title}</td>
                      <td>{trade.outcome}</td>
                      <td>{price(trade.entry_price)}</td>
                      <td>{price(trade.trader_avg_price)}</td>
                      <td>${money(trade.amount_usd)}</td>
                      <td>{money(trade.shares)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>
          )}
        </>
      )}

      {tab === "copy-markets" && (
        <section className="panel">
          <h2>Markets with top accounts</h2>
          <p className="muted">
            Live Polymarket contracts that an investigated top account is in right now. Open the market, follow it, or paper-copy their side.
          </p>
          {liveAccountMarkets.length === 0 ? (
            <p className="muted">No open positions from the current top-account investigation. Refresh the investigation on Top Accounts if this is empty.</p>
          ) : (
            liveAccountMarkets.map((item) => (
              <div className="subpanel" key={`${item.condition_id || item.slug || item.title}`}>
                <div className="row">
                  <button className="linkish" onClick={() => openMarketDetail(item)}>
                    {item.title}
                  </button>
                  <MarketWindow market={item} />
                  <span className="muted">{item.holders.length} account{item.holders.length === 1 ? "" : "s"}</span>
                  <button onClick={() => toggleFollow(item)}>
                    {isFollowed(item) ? "Unfollow" : "Follow"}
                  </button>
                  {item.slug ? (
                    <a className="external" href={`https://polymarket.com/event/${item.slug}`} target="_blank" rel="noopener noreferrer">
                      Open market
                    </a>
                  ) : null}
                </div>
                <HolderTable holders={item.holders} />
              </div>
            ))
          )}
        </section>
      )}

      {tab === "markets" && (
        <>
          <section className="panel">
            <p className="muted">
              Markets that top accounts are currently in live on the <button className="linkish" onClick={() => setTab("copy-markets")}>Copy markets</button> tab.
            </p>
          </section>
          <section className="panel">
            <div className="choice-block">
              <p className="choice-label">Venue</p>
              <div className="choice-row">
                {[
                  { id: "", label: "All venues" },
                  { id: "kalshi", label: "Kalshi" },
                  { id: "polymarket", label: "Polymarket" },
                ].map((item) => (
                  <button
                    key={item.id || "all"}
                    type="button"
                    className={platform === item.id ? "choice active" : "choice"}
                    onClick={() => {
                      setPlatform(item.id);
                      setMarketPage(0);
                    }}
                  >
                    {item.label}
                  </button>
                ))}
              </div>
              <p className="choice-label">Data source</p>
              <div className="choice-row">
                <button
                  type="button"
                  className={family === "" ? "choice active" : "choice"}
                  onClick={() => {
                    setFamily("");
                    setMarketPage(0);
                  }}
                >
                  Every family
                </button>
                {(playbooks?.families || []).map((item) => (
                  <button
                    key={item.family}
                    type="button"
                    className={family === item.family ? "choice active" : "choice"}
                    onClick={() => {
                      setFamily(item.family);
                      setMarketPage(0);
                    }}
                  >
                    {item.label}
                    <small>{item.markets.toLocaleString("en-US")}</small>
                  </button>
                ))}
              </div>
            </div>
            <div className="row">
              <input
                id="market-search"
                value={marketQuery}
                placeholder="Search title or ticker"
                onChange={(event) => {
                  setMarketQuery(event.target.value);
                  setMarketPage(0);
                }}
              />
              <button disabled={busy || followed.length === 0} onClick={() => loadLatest()}>
                Get latest data ({followed.length})
              </button>
              <button
                disabled={catalog?.status === "loading"}
                onClick={() => loadCatalog(0, true).catch((err) => setError(errorMessage(err)))}
              >
                Reload catalog
              </button>
            </div>
            <p className="muted">
              {catalog?.status === "loading"
                ? `Loading every open market. ${catalog.loaded || 0} found so far.`
                : catalog?.fetched_at_est
                  ? `${catalogTotal} markets in this view. Catalog as of ${catalog.fetched_at_est}. Check a row to follow it. Click the title for the chart and the live market page.`
                  : "Loading the market catalog."}
            </p>
            {catalog?.status === "ready" && catalogMarkets.length === 0 ? (
              <p className="muted">No markets match this filter.</p>
            ) : null}
            {catalogMarkets.length > 0 ? (
              <>
                <div className="row">
                  <button onClick={() => togglePage(catalogMarkets)}>
                    {catalogMarkets.every((market) => isFollowed(market)) ? "Unfollow this page" : "Follow this page"}
                  </button>
                  <button disabled={marketPage === 0} onClick={() => setMarketPage((page) => page - 1)}>
                    Previous
                  </button>
                  <span className="muted">
                    Page {marketPage + 1} of {pageCount}
                  </span>
                  <button disabled={marketPage + 1 >= pageCount} onClick={() => setMarketPage((page) => page + 1)}>
                    Next
                  </button>
                </div>
                <div className="market-list">
                  <table>
                    <thead>
                      <tr>
                        <th>Follow</th>
                        <th>Platform</th>
                        <th>Market</th>
                        <th>Started</th>
                        <th>Ends</th>
                        <th>Volume</th>
                        <th>Top accounts in</th>
                        <th>Yes chart</th>
                        <th>Public API</th>
                        <th>Cost</th>
                        <th>Strategy</th>
                      </tr>
                    </thead>
                    <tbody>
                      {catalogMarkets.map((market) => {
                        const followedRow = isFollowed(market);
                        const holders = holdersOnMarket(market);
                        return (
                        <tr
                          key={marketKey(market)}
                          className={followedRow ? "pick followed" : "pick"}
                        >
                          <td onClick={(event) => event.stopPropagation()}>
                            <input
                              type="checkbox"
                              checked={followedRow}
                              aria-label={`Follow ${market.title || market.id}`}
                              onChange={() => toggleFollow(market)}
                            />
                          </td>
                          <td>{market.platform}</td>
                          <td>
                            <button className="linkish" onClick={() => openMarketDetail(market)}>
                              {market.title || market.id}
                            </button>
                            <div className="muted">{market.id}</div>
                          </td>
                          <td>{marketStart(market)}</td>
                          <td>{marketEnd(market)}</td>
                          <td>{money(market.volume)}</td>
                          <td>
                            {holders.length === 0 ? (
                              <span className="muted">--</span>
                            ) : (
                              holders.slice(0, 3).map((holder) => holder.trader_name).join(", ") +
                              (holders.length > 3 ? ` +${holders.length - 3}` : "")
                            )}
                          </td>
                          <td onClick={(event) => event.stopPropagation()}>
                            {histories[marketKey(market)]?.error ? (
                              <span className="muted">Chart unavailable</span>
                            ) : (
                              <PriceChart compact points={histories[marketKey(market)]?.points || []} />
                            )}
                          </td>
                          <td>
                            {market.playbook?.api || "--"}
                            <div className="muted">{market.playbook?.endpoint || ""}</div>
                          </td>
                          <td>{market.playbook?.cost || "--"}</td>
                          <td className="strategy">{market.playbook?.strategy || "--"}</td>
                        </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </>
            ) : null}
          </section>
          {marketDetail ? (
            <section className="panel">
              <div className="inspector-header">
                <div>
                  <h2>{marketDetail.title || marketDetail.id}</h2>
                  <p className="muted">
                    {marketDetail.platform} | {marketDetail.id}
                    {` | Started ${marketStart(marketDetail)} | Ends ${marketEnd(marketDetail)}`}
                    {marketDetail.fetched_at_est ? ` | As of ${marketDetail.fetched_at_est}` : ""}
                  </p>
                </div>
                <div className="row">
                  <button onClick={() => toggleFollow(marketDetail as Market)}>
                    {isFollowed(marketDetail as Market) ? "Unfollow" : "Follow"}
                  </button>
                  {marketDetail.url ? (
                    <a className="external" href={marketDetail.url} target="_blank" rel="noreferrer">
                      {marketDetail.url_label || "Open market"}
                    </a>
                  ) : null}
                  <button onClick={() => setMarketDetail(null)}>Close</button>
                </div>
              </div>
              {detailBusy ? <p className="muted">Loading market detail and price history.</p> : null}
              <div className="grid">
                <div className="card">
                  <span>Yes</span>
                  <strong>{price(marketDetail.yes_price)}</strong>
                  <span className="muted">
                    {marketDetail.yes_bid != null ? `Bid ${price(marketDetail.yes_bid)} / Ask ${price(marketDetail.yes_ask)}` : marketDetail.status || ""}
                  </span>
                </div>
                <div className="card">
                  <span>Volume</span>
                  <strong>{money(marketDetail.volume)}</strong>
                </div>
                <div className="card">
                  <span>Chart window</span>
                  <strong>{marketDetail.window || "--"}</strong>
                </div>
              </div>
              <PriceChart points={marketDetail.points || []} />
              {Array.isArray(marketDetail.outcomes) && marketDetail.outcomes.length > 0 ? (
                <table>
                  <thead>
                    <tr>
                      <th>Outcome</th>
                      <th>Price</th>
                    </tr>
                  </thead>
                  <tbody>
                    {marketDetail.outcomes.map((outcome: Loose) => (
                      <tr key={outcome.name}>
                        <td>{outcome.name}</td>
                        <td>{price(outcome.price)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : null}
              {marketDetail.description ? <p className="detail-copy">{marketDetail.description}</p> : null}
              <div className="subpanel">
                <h2>Top accounts in this market</h2>
                <HolderTable holders={holdersOnMarket(marketDetail)} />
              </div>
              {marketDetail.playbook?.strategy ? (
                <p className="muted">{marketDetail.playbook.strategy}</p>
              ) : null}
            </section>
          ) : null}
          <section className="panel">
            <h2>Latest data</h2>
            {latest.length === 0 ? (
              <p className="muted">Select markets above, then get the most recent quotes for those only.</p>
            ) : (
              <>
                <p className="muted">{latestAt ? `Quotes as of ${latestAt}` : ""}</p>
                {latest.map((market) => {
                  const history = histories[marketKey(market)];
                  return (
                    <div className="latest-card" key={marketKey(market)}>
                      <div className="row">
                        <button className="linkish" onClick={() => openMarketDetail(market)}>
                          {market.title || market.id}
                        </button>
                        <span className="muted">{market.platform}</span>
                        <span>Yes {price(market.yes_price)}</span>
                        <span>Volume {money(market.volume)}</span>
                        <span className="muted">Started {marketStart(market)}</span>
                        <span className="muted">Ends {marketEnd(market)}</span>
                        <span className="muted">{history?.window || market.fetched_at_est || ""}</span>
                      </div>
                      {history?.error ? <p className="muted">Chart unavailable</p> : <PriceChart points={history?.points || []} />}
                    </div>
                  );
                })}
              </>
            )}
          </section>
        </>
      )}

      {tab === "eda" && <EdaBoard charts={charts} accounts={topAccountsData} onOpenAccount={(acc) => openAccount(acc.address)} />}

      {tab === "eda" && backtests && (
        <section className="panel">
          <h2>Backtests</h2>
          <p className="muted">
            {backtests.rule} Built {backtests.generated_at_est}. {backtests.binary_markets} binary markets and {backtests.events} multi-outcome events.
          </p>
          <table>
            <thead>
              <tr>
                <th>Rule</th>
                <th>Train</th>
                <th>Train wins</th>
                <th>Train return</th>
                <th>Test</th>
                <th>Test wins</th>
                <th>Test return</th>
                <th>Result</th>
              </tr>
            </thead>
            <tbody>
              {backtests.strategies.map((row: Loose) => (
                <tr key={row.name}>
                  <td>
                    {row.label}
                    <div className="muted">{row.description}</div>
                  </td>
                  <td>{row.train.n}</td>
                  <td>{row.train.win_rate === null ? "--" : `${(row.train.win_rate * 100).toFixed(0)}%`}</td>
                  <td className={row.train.roi < 0 ? "bad" : "good"}>
                    {row.train.roi === null ? "--" : `${(row.train.roi * 100).toFixed(1)}%`}
                  </td>
                  <td>{row.test.n}</td>
                  <td>{row.test.win_rate === null ? "--" : `${(row.test.win_rate * 100).toFixed(0)}%`}</td>
                  <td className={row.test.roi < 0 ? "bad" : "good"}>
                    {row.test.roi === null ? "--" : `${(row.test.roi * 100).toFixed(1)}%`}
                  </td>
                  <td className={row.kept ? "good" : ""}>{row.kept ? "Kept" : "Dropped"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}

      {tab === "eda" && favorites && (
        <section className="panel">
          <h2>Favorite study, bucket numbers</h2>
          <table>
              <thead>
                <tr>
                  <th>Bucket</th>
                  <th>Markets</th>
                  <th>Avg price</th>
                  <th>Actual</th>
                  <th>Return</th>
                </tr>
              </thead>
              <tbody>
                {favorites.buckets.map((bucket: Loose) => (
                  <tr key={bucket.label}>
                    <td>{bucket.label}</td>
                    <td>{bucket.count}</td>
                    <td>{bucket.mean_price === null ? "--" : bucket.mean_price.toFixed(3)}</td>
                    <td>{bucket.actual === null ? "--" : bucket.actual.toFixed(3)}</td>
                    <td className={bucket.roi < 0 ? "bad" : "good"}>
                      {bucket.roi === null ? "--" : `${(bucket.roi * 100).toFixed(1)}%`}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
        </section>
      )}

      {tab === "strategies" && (
        <section className="panel">
          <table>
            <thead>
              <tr>
                <th>Strategy</th>
                <th>Weight</th>
                <th>Status</th>
                <th>What it does</th>
              </tr>
            </thead>
            <tbody>
              {strategies.map((strategy) => (
                <tr key={strategy.name}>
                  <td>{strategy.label}</td>
                  <td>{strategy.weight ?? "1.0"}</td>
                  <td className={strategy.enabled ? "good" : ""}>{strategy.enabled ? "Enabled" : "Off"}</td>
                  <td>{strategy.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}

      {tab === "logs" && (
        <section className="panel">
          {logs.length === 0 ? (
            <p className="muted">No runner logs in data/logs/runner yet.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Signals</th>
                  <th>Trades</th>
                  <th>Successful</th>
                  <th>Duration</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((entry, index) => (
                  <tr key={`${entry.timestamp}-${index}`}>
                    <td>{entry.time_est || entry.timestamp}</td>
                    <td>{entry.signals}</td>
                    <td>{entry.trades}</td>
                    <td>{entry.successful}</td>
                    <td>{entry.duration_ms ? `${Math.round(entry.duration_ms)} ms` : "--"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      )}
    </div>
  );
}
