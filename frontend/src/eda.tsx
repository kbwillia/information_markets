import { useState, type ReactNode } from "react";
import AccountDash from "./account-dash.tsx";

type Loose = Record<string, any>;
type ChartRow = Record<string, any>;
type SeriesItem = { key: string; label?: string; color: string };
type LineSeries = { name: string; color: string; points: { y: number | null }[] };
type CalRow = { label: string; actual: number | null; count: number; midpoint: number };

const COLORS = {
  accent: "#7eb6ff",
  good: "#6dcaa0",
  bad: "#e07a7a",
  gold: "#d7b56d",
  purple: "#c58bdb",
  muted: "#8b98a8",
};

function rowsOf(value: unknown): ChartRow[] {
  return Array.isArray(value) ? (value as ChartRow[]) : [];
}

function num(value: unknown): number | null {
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

function pct(value: unknown): string {
  const number = num(value);
  if (number === null) return "--";
  return `${(number * 100).toFixed(1)}%`;
}

function money(value: unknown): string {
  const number = num(value);
  if (number === null) return "--";
  if (number >= 1_000_000) return `$${(number / 1_000_000).toFixed(1)}M`;
  if (number >= 1_000) return `$${(number / 1_000).toFixed(0)}K`;
  return `$${number.toFixed(0)}`;
}

function points(value: unknown): string {
  const number = num(value);
  if (number === null) return "--";
  return `${(number * 100).toFixed(1)} pts`;
}

function ChartCard({
  title,
  note,
  children,
  wide,
}: {
  title: string;
  note?: string;
  children: ReactNode;
  wide?: boolean;
}) {
  return (
    <section className={wide ? "panel chart-card wide" : "panel chart-card"}>
      <h2>{title}</h2>
      {children}
      {note ? <p className="muted">{note}</p> : null}
    </section>
  );
}

function axisTicks(min: number, max: number, count = 4): number[] {
  if (min === max) return [min];
  const ticks = [];
  for (let index = 0; index < count; index += 1) {
    ticks.push(min + ((max - min) * index) / (count - 1));
  }
  return ticks;
}

function formatTick(value: number, mode?: string): string {
  if (mode === "pct") return `${Math.round(value * 100)}%`;
  if (mode === "roi") return `${Math.round(value * 100)}%`;
  if (mode === "money") return value.toFixed(1);
  if (Math.abs(value) >= 100) return String(Math.round(value));
  return value.toFixed(1);
}

function BarChart({
  rows,
  series,
  yMode = "number",
  ariaLabel,
}: {
  rows: ChartRow[];
  series: SeriesItem[];
  yMode?: string;
  ariaLabel: string;
}) {
  const width = 640;
  const height = 280;
  const pad = { left: 48, right: 12, top: 16, bottom: 64 };
  const innerW = width - pad.left - pad.right;
  const innerH = height - pad.top - pad.bottom;
  const values = rows.flatMap((row) => series.map((item) => num(row[item.key]))).filter((value) => value !== null);
  const min = Math.min(0, ...values, 0);
  const max = Math.max(0, ...values, 0.01);
  const span = max - min || 1;
  const yOf = (value: number) => pad.top + ((max - value) / span) * innerH;
  const zero = yOf(0);
  const groupW = innerW / Math.max(rows.length, 1);
  const barW = Math.min(18, (groupW * 0.8) / series.length);

  return (
    <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label={ariaLabel}>
      {axisTicks(min, max).map((tick) => (
        <g key={tick}>
          <line x1={pad.left} x2={width - pad.right} y1={yOf(tick)} y2={yOf(tick)} className="gridline" />
          <text x={pad.left - 6} y={yOf(tick) + 4} textAnchor="end" className="axis">
            {formatTick(tick, yMode)}
          </text>
        </g>
      ))}
      <line x1={pad.left} x2={width - pad.right} y1={zero} y2={zero} className="zero-line" />
      {rows.map((row, rowIndex) =>
        series.map((item, seriesIndex) => {
          const value = num(row[item.key]);
          if (value === null) return null;
          const x = pad.left + rowIndex * groupW + (groupW - series.length * barW) / 2 + seriesIndex * barW;
          const y = Math.min(zero, yOf(value));
          const h = Math.max(1, Math.abs(yOf(value) - zero));
          return <rect key={`${row.label}-${item.key}`} x={x} y={y} width={barW - 2} height={h} fill={item.color} />;
        }),
      )}
      {rows.map((row, rowIndex) => (
        <text
          key={row.label}
          x={pad.left + rowIndex * groupW + groupW / 2}
          y={height - 36}
          textAnchor="end"
          className="axis tick-label"
          transform={`rotate(-40 ${pad.left + rowIndex * groupW + groupW / 2} ${height - 36})`}
        >
          {row.label}
        </text>
      ))}
    </svg>
  );
}

function Legend({ series }: { series: SeriesItem[] }) {
  return (
    <div className="legend">
      {series.map((item) => (
        <span key={item.key}>
          <i style={{ background: item.color }} />
          {item.label}
        </span>
      ))}
    </div>
  );
}

function LineChart({
  series,
  yMode = "number",
  ariaLabel,
  xLabels,
}: {
  series: LineSeries[];
  yMode?: string;
  ariaLabel: string;
  xLabels?: string[];
}) {
  const width = 640;
  const height = 280;
  const pad = { left: 52, right: 12, top: 16, bottom: 36 };
  const innerW = width - pad.left - pad.right;
  const innerH = height - pad.top - pad.bottom;
  const values = series.flatMap((item) => item.points.map((point) => num(point.y))).filter((value) => value !== null);
  const min = Math.min(...values, 0);
  const max = Math.max(...values, 0.01);
  const span = max - min || 1;
  const count = Math.max(...series.map((item) => item.points.length), 1);
  const xOf = (index: number) => pad.left + (count === 1 ? innerW / 2 : (index / (count - 1)) * innerW);
  const yOf = (value: number) => pad.top + ((max - value) / span) * innerH;
  const labels = xLabels || [];
  const labelStep = Math.max(1, Math.ceil(labels.length / 6));

  return (
    <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label={ariaLabel}>
      {axisTicks(min, max).map((tick) => (
        <g key={tick}>
          <line x1={pad.left} x2={width - pad.right} y1={yOf(tick)} y2={yOf(tick)} className="gridline" />
          <text x={pad.left - 6} y={yOf(tick) + 4} textAnchor="end" className="axis">
            {formatTick(tick, yMode)}
          </text>
        </g>
      ))}
      <line x1={pad.left} x2={width - pad.right} y1={yOf(0)} y2={yOf(0)} className="zero-line" />
      {series.map((item) => {
        const points = item.points
          .map((point, index) => {
            const value = num(point.y);
            if (value === null) return null;
            return `${xOf(index)},${yOf(value)}`;
          })
          .filter(Boolean)
          .join(" ");
        return <polyline key={item.name} points={points} fill="none" stroke={item.color} strokeWidth="2" />;
      })}
      {labels.map((label, index) =>
        index % labelStep === 0 ? (
          <text key={label} x={xOf(index)} y={height - 10} textAnchor="middle" className="axis">
            {label.slice(2)}
          </text>
        ) : null,
      )}
    </svg>
  );
}

function CalibrationChart({ series }: { series: { name: string; color: string; rows: CalRow[] }[] }) {
  const width = 640;
  const height = 320;
  const pad = { left: 44, right: 16, top: 16, bottom: 36 };
  const innerW = width - pad.left - pad.right;
  const innerH = height - pad.top - pad.bottom;
  const xOf = (value: number) => pad.left + value * innerW;
  const yOf = (value: number) => pad.top + (1 - value) * innerH;
  const ticks = [0, 0.5, 1];

  return (
    <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Price versus actual win rate">
      {ticks.map((tick) => (
        <g key={tick}>
          <line x1={pad.left} x2={width - pad.right} y1={yOf(tick)} y2={yOf(tick)} className="gridline" />
          <text x={pad.left - 8} y={yOf(tick) + 4} textAnchor="end" className="axis">
            {tick.toFixed(1)}
          </text>
          <text x={xOf(tick)} y={height - 10} textAnchor="middle" className="axis">
            {tick.toFixed(1)}
          </text>
        </g>
      ))}
      <line x1={xOf(0)} y1={yOf(0)} x2={xOf(1)} y2={yOf(1)} className="diagonal" />
      {series.map((item) => {
        const dots = item.rows.filter((row): row is CalRow & { actual: number } => row.actual !== null && row.count > 0);
        const points = dots.map((row) => `${xOf(row.midpoint)},${yOf(row.actual)}`).join(" ");
        return (
          <g key={item.name}>
            <polyline points={points} fill="none" stroke={item.color} strokeWidth="2" />
            {dots.map((row) => (
              <circle key={`${item.name}-${row.label}`} cx={xOf(row.midpoint)} cy={yOf(row.actual)} r="3.5" fill={item.color} />
            ))}
          </g>
        );
      })}
    </svg>
  );
}

function HBar({
  rows,
  valueKey,
  labelKey,
  color,
  ariaLabel,
  format,
}: {
  rows: ChartRow[];
  valueKey: string;
  labelKey: string;
  color: string;
  ariaLabel: string;
  format: (value: number) => string;
}) {
  const longest = rows.reduce((size, row) => Math.max(size, String(row[labelKey] || "").length), 8);
  const padLeft = Math.min(340, Math.max(88, longest * 6.2));
  const width = padLeft + 420;
  const height = Math.max(180, rows.length * 28 + 24);
  const pad = { left: padLeft, right: 72, top: 8, bottom: 8 };
  const values = rows.map((row) => num(row[valueKey])).filter((value) => value !== null);
  const min = Math.min(0, ...values, 0);
  const max = Math.max(0, ...values, 0.01);
  const span = max - min || 1;
  const innerW = width - pad.left - pad.right;
  const xOf = (value: number) => pad.left + ((value - min) / span) * innerW;
  const zero = xOf(0);
  const rowH = (height - pad.top - pad.bottom) / Math.max(rows.length, 1);

  return (
    <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label={ariaLabel}>
      <line x1={zero} x2={zero} y1={pad.top} y2={height - pad.bottom} className="zero-line" />
      {rows.map((row, index) => {
        const value = num(row[valueKey]);
        const y = pad.top + index * rowH + 4;
        if (value === null) return null;
        const x = Math.min(zero, xOf(value));
        const w = Math.max(1, Math.abs(xOf(value) - zero));
        return (
          <g key={row[labelKey]}>
            <text x={pad.left - 8} y={y + 12} textAnchor="end" className="axis">
              {row[labelKey]}
            </text>
            <rect x={x} y={y} width={w} height={14} fill={value < 0 ? COLORS.bad : color} />
            <text x={Math.max(x + w, zero) + 6} y={y + 12} className="axis">
              {format(value)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

const HORIZON_ROI = [
  { key: "roi1", label: "1 day", color: COLORS.accent },
  { key: "roi7", label: "7 days", color: COLORS.gold },
  { key: "roi30", label: "30 days", color: COLORS.purple },
];

export default function EdaBoard({
  charts,
  accounts,
  onOpenAccount,
}: {
  charts: Loose | null;
  accounts: Loose | null;
  onOpenAccount?: (account: Loose) => void;
}) {
  const [edaView, setEdaView] = useState<"families" | "accounts" | "calibration">("families");

  return (
    <>
      <div className="tabs eda-switch">
        <button type="button" className={edaView === "families" ? "active" : ""} onClick={() => setEdaView("families")}>
          Families
        </button>
        <button type="button" className={edaView === "accounts" ? "active" : ""} onClick={() => setEdaView("accounts")}>
          Accounts
        </button>
        <button
          type="button"
          className={edaView === "calibration" ? "active" : ""}
          onClick={() => setEdaView("calibration")}
        >
          Calibration
        </button>
      </div>
      {edaView === "families" ? (
        <FamilyBoard charts={charts} />
      ) : edaView === "accounts" ? (
        <AccountDash accounts={accounts} onOpenAccount={onOpenAccount} />
      ) : (
        <CalibrationBoard charts={charts} accounts={accounts} />
      )}
    </>
  );
}

function FamilyBoard({ charts }: { charts: Loose | null }) {
  if (!charts) {
    return (
      <section className="panel">
        <p className="muted">Family data is not loaded yet.</p>
      </section>
    );
  }

  const resolved = rowsOf(charts.families).filter((row) => row.count >= 40);
  const thin = rowsOf(charts.families).filter((row) => row.count < 40);
  const open = rowsOf(charts.open_families);
  const openCount = open.reduce((sum, row) => sum + (num(row.markets) || 0), 0);
  const watched = [...resolved].sort((a, b) => (num(b.gap) || 0) - (num(a.gap) || 0));
  const first = watched[0];
  const second = watched[1];
  const asOf = charts.catalog_as_of_est || "the latest catalog load";

  return (
    <>
      <div className="grid">
        <div className="card">
          <span>{first ? first.label : "Largest gap"}</span>
          <strong className="good">{first ? points(first.gap) : "--"}</strong>
        </div>
        <div className="card">
          <span>{second ? second.label : "Next gap"}</span>
          <strong className={(num(second?.gap) || 0) > 0 ? "good" : ""}>{second ? points(second.gap) : "--"}</strong>
        </div>
        <div className="card">
          <span>Open contracts</span>
          <strong>{openCount ? openCount.toLocaleString("en-US") : "--"}</strong>
        </div>
        <div className="card">
          <span>Catalog</span>
          <strong>{asOf}</strong>
        </div>
      </div>

      <section className="panel">
        <h2>What is tradable</h2>
        <p>
          {first && second
            ? `${first.label} Yes won ${pct(first.actual)} against a day-ahead price of ${Number(first.mean_price).toFixed(2)} (${first.count} markets, ${pct(first.yes_roi)} after one cent of slippage). ${second.label} won ${pct(second.actual)} against ${Number(second.mean_price).toFixed(2)} (${second.count} markets, ${pct(second.yes_roi)}). Both samples are small.`
            : "The resolved sample does not have two families with at least 40 markets."}
        </p>
        <p className="muted">
          Open above and over ladders were checked against the catalog as of {asOf}. A higher strike bidding through a lower strike's ask did not show up. The mid-price gaps on yields and gas sit on wide books, so they are not a fill. Crypto and temperature look cheap because most strikes are already out of the money.
        </p>
      </section>

      <div className="chart-grid">
        {resolved.length > 0 && (
          <ChartCard
            wide
            title="Resolved Yes rate minus the price, by data source"
            note="Saved resolved sample, one price taken a day before close. Families with at least 40 markets. A bar above zero means Yes won more often than that price."
          >
            <HBar
              rows={resolved.map((row) => ({ label: `${row.label} (${row.count})`, value: row.gap }))}
              labelKey="label"
              valueKey="value"
              color={COLORS.accent}
              ariaLabel="Yes rate minus price by data source family"
              format={(value) => points(value)}
            />
            <FamilyTable rows={resolved} />
          </ChartCard>
        )}

        {open.length > 0 && (
          <ChartCard
            wide
            title="Open contracts by data source"
            note={`Share of contracts priced under 15 cents. Catalog as of ${asOf}. The family chips on Markets are a filtered slice of this book.`}
          >
            <div className="market-list">
              <table>
                <thead>
                  <tr>
                    <th>Family</th>
                    <th>Open markets</th>
                    <th>Under 15 cents</th>
                    <th>Volume</th>
                  </tr>
                </thead>
                <tbody>
                  {open.map((row) => (
                    <tr key={row.family}>
                      <td>{row.label}</td>
                      <td>{Number(row.markets).toLocaleString("en-US")}</td>
                      <td>{pct(row.cheap_share)}</td>
                      <td>{money(row.volume)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </ChartCard>
        )}

        {thin.length > 0 && (
          <ChartCard
            wide
            title="Resolved families with fewer than 40 markets"
            note="These returns are too small to trade from. Weather and player props have no resolved rows in this sample."
          >
            <FamilyTable rows={thin} />
          </ChartCard>
        )}
      </div>
    </>
  );
}

function FamilyTable({ rows }: { rows: ChartRow[] }) {
  return (
    <div className="market-list">
      <table>
        <thead>
          <tr>
            <th>Family</th>
            <th>Markets</th>
            <th>Day-ahead price</th>
            <th>Yes won</th>
            <th>Gap</th>
            <th>Yes return</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.family}>
              <td>{row.label}</td>
              <td>{row.count}</td>
              <td>{Number(row.mean_price).toFixed(2)}</td>
              <td>{Number(row.actual).toFixed(2)}</td>
              <td className={(num(row.gap) || 0) >= 0.08 ? "good" : (num(row.gap) || 0) < 0 ? "bad" : ""}>
                {points(row.gap)}
              </td>
              <td>{row.yes_roi === null || row.yes_roi === undefined ? "--" : pct(row.yes_roi)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function CalibrationBoard({ charts, accounts }: { charts: Loose | null; accounts: Loose | null }) {
  if (!charts) {
    return (
      <section className="panel">
        <p className="muted">Chart data is not loaded yet. The backtest sample has to be built first.</p>
      </section>
    );
  }

  const horizon = (key: string): ChartRow[] => rowsOf(charts.calibration?.[key]);
  const dayBands = horizon("1d");
  const roiRows = dayBands.map((row, index) => ({
    label: row.label,
    roi1: row.roi,
    roi7: horizon("7d")[index]?.roi,
    roi30: horizon("30d")[index]?.roi,
    count: row.count,
  }));
  const countRows = rowsOf(charts.price_hist).map((row) => ({ label: row.label, count: row.count }));
  const equity = charts.equity || {};
  const equitySource: { name: string; color: string; rows: ChartRow[] }[] = [
    { name: "Buy every Yes", color: COLORS.muted, rows: rowsOf(equity.buy_yes) },
    { name: "Underdog, 1 day", color: COLORS.accent, rows: rowsOf(equity.underdog_1d) },
    { name: "Underdog, 7 days", color: COLORS.good, rows: rowsOf(equity.underdog_7d) },
    { name: "Underdog, 30 days", color: COLORS.gold, rows: rowsOf(equity.underdog_30d) },
    { name: "Favorite above 0.80", color: COLORS.bad, rows: rowsOf(equity.favorite_80) },
    { name: "Follow the week", color: COLORS.purple, rows: rowsOf(equity.follow_week) },
    { name: "Fade the week", color: "#8fd0c6", rows: rowsOf(equity.fade_week) },
  ];
  const monthLabels = [...new Set(equitySource.flatMap((item) => item.rows.map((point) => String(point.month))))].sort();
  const equitySeries = equitySource
    .map((item) => {
      const values = new Map(item.rows.map((point) => [String(point.month), num(point.pnl) ?? 0]));
      let last = 0;
      const points = monthLabels.map((month) => {
        const found = values.get(month);
        if (found !== undefined) last = found;
        return { y: last };
      });
      return { name: item.name, color: item.color, points };
    })
    .filter((item) => item.points.some((point) => point.y !== 0));
  const strategyRows = rowsOf(charts.strategies).map((row) => ({
    label: row.label,
    train: row.train?.roi,
    test: row.test?.roi,
    testWins: row.test?.win_rate,
    kept: row.kept,
  }));
  const accountRows = rowsOf(accounts?.accounts)
    .map((account) => ({
      label: account.user_name || "account",
      pnl: num(account.realized_pnl_sampled),
      win: num(account.win_rate_pct),
      roi: num(account.realized_roi_pct),
    }))
    .sort((a, b) => (b.pnl || 0) - (a.pnl || 0));
  const summary = charts.favorite_summary || {};
  const sample = charts.sample || {};

  return (
    <>
      <div className="grid">
        <div className="card">
          <span>Binary markets priced</span>
          <strong>{sample.binary ?? "--"}</strong>
        </div>
        <div className="card">
          <span>Day-ahead prices</span>
          <strong>{sample.p1 ?? "--"}</strong>
        </div>
        <div className="card">
          <span>Week-ahead prices</span>
          <strong>{sample.p7 ?? "--"}</strong>
        </div>
        <div className="card">
          <span>Month-ahead prices</span>
          <strong>{sample.p30 ?? "--"}</strong>
        </div>
        <div className="card">
          <span>Multi-outcome events</span>
          <strong>{sample.baskets ?? "--"}</strong>
        </div>
        <div className="card">
          <span>Favorite-longshot study</span>
          <strong className={summary.favorite_roi < 0 ? "bad" : "good"}>
            {summary.favorite_roi === null || summary.favorite_roi === undefined ? "--" : pct(summary.favorite_roi)}
          </strong>
        </div>
      </div>

      <div className="chart-grid">
        <ChartCard
          wide
          title="Calibration by horizon"
          note="Each dot is the actual Yes win rate in a 0.1 price bucket. The dashed line is a perfect forecast. Built from the backtest sample."
        >
          <Legend
            series={[
              { key: "1d", label: "1 day before close", color: COLORS.accent },
              { key: "7d", label: "7 days", color: COLORS.gold },
              { key: "30d", label: "30 days", color: COLORS.purple },
            ]}
          />
          <CalibrationChart
            series={[
              { name: "1d", color: COLORS.accent, rows: horizon("1d") as CalRow[] },
              { name: "7d", color: COLORS.gold, rows: horizon("7d") as CalRow[] },
              { name: "30d", color: COLORS.purple, rows: horizon("30d") as CalRow[] },
            ]}
          />
        </ChartCard>

        <ChartCard
          wide
          title="Larger favorite study"
          note={`Last trade at least 24 hours before close, across ${summary.observations ?? "--"} resolved markets. Brier score ${summary.brier ?? "--"}. Favorite win rate ${summary.favorite_win_rate === null || summary.favorite_win_rate === undefined ? "--" : pct(summary.favorite_win_rate)} against an average price of ${summary.favorite_mean_price ?? "--"}.`}
        >
          <CalibrationChart series={[{ name: "24h", color: COLORS.accent, rows: rowsOf(charts.favorite_buckets) as CalRow[] }]} />
        </ChartCard>

        <ChartCard
          wide
          title="Return from buying Yes, by price bucket"
          note="One share per market, plus one cent of slippage, held to resolution. A bucket above zero paid more than its price."
        >
          <Legend series={HORIZON_ROI} />
          <BarChart rows={roiRows} series={HORIZON_ROI} yMode="roi" ariaLabel="Yes return by price bucket and horizon" />
        </ChartCard>

        <ChartCard title="Where prices sat a day before close" note="Count of markets in each 0.1 price bucket.">
          <BarChart
            rows={countRows}
            series={[{ key: "count", label: "Markets", color: COLORS.accent }]}
            ariaLabel="Market counts by price"
          />
        </ChartCard>

        <ChartCard title="Yes rate after a week-long move" note="The move is the day-ahead price minus the week-ahead price.">
          <BarChart
            rows={rowsOf(charts.moves).map((row) => ({ label: row.label, yes_rate: row.yes_rate, count: row.count }))}
            series={[{ key: "yes_rate", label: "Yes win rate", color: COLORS.gold }]}
            yMode="pct"
            ariaLabel="Yes win rate by recent move"
          />
        </ChartCard>

        <ChartCard wide title="Cumulative profit by rule" note="Running profit in dollars, one share per signal, marked at each month. This is the same sample as the backtest table.">
          <Legend
            series={equitySeries.map((item) => ({ key: item.name, label: item.name, color: item.color }))}
          />
          <LineChart series={equitySeries} yMode="money" xLabels={monthLabels} ariaLabel="Cumulative profit" />
        </ChartCard>

        <ChartCard title="Return by topic, buying Yes">
          <HBar
            rows={rowsOf(charts.topics)}
            labelKey="topic"
            valueKey="yes_roi"
            color={COLORS.accent}
            ariaLabel="Yes return by topic"
            format={pct}
          />
        </ChartCard>

        <ChartCard title="Return by topic, buying the underdog" note="Underdog means the cheap side priced from 0.03 to 0.15 a day before close.">
          <HBar
            rows={rowsOf(charts.topics)}
            labelKey="topic"
            valueKey="underdog_roi"
            color={COLORS.good}
            ariaLabel="Underdog return by topic"
            format={pct}
          />
        </ChartCard>

        <ChartCard title="Yes win rate by topic">
          <HBar
            rows={rowsOf(charts.topics)}
            labelKey="topic"
            valueKey="yes_rate"
            color={COLORS.gold}
            ariaLabel="Yes win rate by topic"
            format={pct}
          />
        </ChartCard>

        <ChartCard title="Markets by topic">
          <HBar
            rows={rowsOf(charts.topics).map((row) => ({ ...row, label: row.topic }))}
            labelKey="topic"
            valueKey="count"
            color={COLORS.purple}
            ariaLabel="Market count by topic"
            format={(value) => String(Math.round(value))}
          />
        </ChartCard>

        <ChartCard
          wide
          title="Return by volume band"
          note="Bands use total market volume. Underdog and favorite rules are the same ones in the backtest."
        >
          <Legend
            series={[
              { key: "yes_roi", label: "Buy Yes", color: COLORS.accent },
              { key: "underdog_roi", label: "Underdog", color: COLORS.good },
              { key: "favorite_roi", label: "Favorite 0.80+", color: COLORS.bad },
            ]}
          />
          <BarChart
            rows={rowsOf(charts.volume_bands)}
            series={[
              { key: "yes_roi", color: COLORS.accent },
              { key: "underdog_roi", color: COLORS.good },
              { key: "favorite_roi", color: COLORS.bad },
            ]}
            yMode="roi"
            ariaLabel="Return by volume band"
          />
        </ChartCard>

        <ChartCard title="Markets priced each quarter">
          <BarChart
            rows={rowsOf(charts.quarters)}
            series={[{ key: "count", color: COLORS.accent }]}
            ariaLabel="Markets per quarter"
          />
        </ChartCard>

        <ChartCard title="Monthly price versus what happened" note="Mean Yes price against the share of markets that resolved Yes.">
          <Legend
            series={[
              { key: "mean_price", label: "Mean price", color: COLORS.accent },
              { key: "yes_rate", label: "Yes rate", color: COLORS.good },
            ]}
          />
          <LineChart
            yMode="pct"
            ariaLabel="Monthly price and yes rate"
            xLabels={rowsOf(charts.months).map((row) => String(row.month))}
            series={[
              { name: "price", color: COLORS.accent, points: rowsOf(charts.months).map((row) => ({ y: num(row.mean_price) })) },
              { name: "yes", color: COLORS.good, points: rowsOf(charts.months).map((row) => ({ y: num(row.yes_rate) })) },
            ]}
          />
        </ChartCard>

        <ChartCard title="Brier score by year" note="Lower is a sharper forecast. This uses the day-ahead price.">
          <BarChart
            rows={rowsOf(charts.years).map((row) => ({ label: row.year, brier: row.brier }))}
            series={[{ key: "brier", color: COLORS.gold }]}
            ariaLabel="Brier score by year"
          />
        </ChartCard>

        <ChartCard title="Buying Yes, return by year">
          <BarChart
            rows={rowsOf(charts.years).map((row) => ({ label: row.year, yes_roi: row.yes_roi }))}
            series={[{ key: "yes_roi", color: COLORS.accent }]}
            yMode="roi"
            ariaLabel="Yes return by year"
          />
        </ChartCard>

        <ChartCard
          title="Complete-set prices"
          note={`${charts.baskets?.n ?? 0} events had a price on every outcome. ${charts.baskets?.exactly_one ?? 0} of them resolved with exactly one winner.`}
        >
          <BarChart
            rows={rowsOf(charts.baskets?.bands)}
            series={[{ key: "count", color: COLORS.purple }]}
            ariaLabel="Complete set price sums"
          />
        </ChartCard>

        <ChartCard
          wide
          title="Backtest return, train versus later sample"
          note={charts.backtest_rule || "Train is before July 1, 2025. Test is after that."}
        >
          <Legend
            series={[
              { key: "train", label: "Train", color: COLORS.accent },
              { key: "test", label: "Test", color: COLORS.gold },
            ]}
          />
          <HBar
            rows={strategyRows.map((row) => ({ label: row.label, value: row.train }))}
            labelKey="label"
            valueKey="value"
            color={COLORS.accent}
            ariaLabel="Train return by strategy"
            format={pct}
          />
        </ChartCard>

        <ChartCard wide title="Same rules on the later sample">
          <HBar
            rows={strategyRows.map((row) => ({ label: row.label, value: row.test }))}
            labelKey="label"
            valueKey="value"
            color={COLORS.gold}
            ariaLabel="Test return by strategy"
            format={pct}
          />
        </ChartCard>

        <ChartCard title="Test win rate by rule">
          <HBar
            rows={strategyRows.map((row) => ({ label: row.label, value: row.testWins }))}
            labelKey="label"
            valueKey="value"
            color={COLORS.good}
            ariaLabel="Test win rate by strategy"
            format={pct}
          />
        </ChartCard>

        {accountRows.length > 0 && (
          <ChartCard wide title="Sampled realized profit of researched accounts" note="These are the closed positions pulled for the top-account study, not a full account history.">
            <HBar
              rows={accountRows}
              labelKey="label"
              valueKey="pnl"
              color={COLORS.good}
              ariaLabel="Account realized profit"
              format={(value) => value.toLocaleString("en-US", { maximumFractionDigits: 0 })}
            />
          </ChartCard>
        )}

        {accountRows.length > 0 && (
          <ChartCard title="Account win rate" note="Win rate on the sampled closed positions.">
            <HBar
              rows={[...accountRows].sort((a, b) => (b.win || 0) - (a.win || 0))}
              labelKey="label"
              valueKey="win"
              color={COLORS.accent}
              ariaLabel="Account win rate"
              format={(value) => `${value.toFixed(0)}%`}
            />
          </ChartCard>
        )}
      </div>

      <p className="muted chart-stamp">Charts built {charts.generated_at_est}. Backtest file built {charts.backtest_built || "--"}.</p>
    </>
  );
}
