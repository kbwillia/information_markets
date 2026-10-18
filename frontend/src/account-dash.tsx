import { useEffect, useState } from "react";

type Loose = Record<string, any>;

function money(value: unknown): string {
  const n = Number(value);
  if (!Number.isFinite(n)) return "—";
  const abs = Math.abs(n);
  const sign = n < 0 ? "-" : "";
  if (abs >= 1_000_000_000) return `${sign}$${(abs / 1_000_000_000).toFixed(2)}B`;
  if (abs >= 1_000_000) return `${sign}$${(abs / 1_000_000).toFixed(2)}M`;
  if (abs >= 1_000) return `${sign}$${(abs / 1_000).toFixed(1)}k`;
  return `${sign}$${abs.toFixed(0)}`;
}

function pct(value: unknown): string {
  const n = Number(value);
  if (!Number.isFinite(n)) return "—";
  return `${n.toFixed(1)}%`;
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

function price(value: unknown): string {
  const n = Number(value);
  if (!Number.isFinite(n)) return "—";
  return n.toFixed(2);
}

function ShareBars({ rows, labelKey, valueKey }: { rows: Loose[]; labelKey: string; valueKey: string }) {
  const max = Math.max(1, ...rows.map((row) => Number(row[valueKey]) || 0));
  return (
    <div className="share-bars">
      {rows.map((row) => {
        const value = Number(row[valueKey]) || 0;
        return (
          <div className="share-row" key={String(row[labelKey])}>
            <span className="share-label">{row[labelKey]}</span>
            <span className="share-track">
              <span className="share-fill" style={{ width: `${(value / max) * 100}%` }} />
            </span>
            <span className="share-val">{pct(value)}</span>
          </div>
        );
      })}
    </div>
  );
}

export default function AccountDash({
  accounts,
  onOpenAccount,
}: {
  accounts: Loose | null;
  onOpenAccount?: (account: Loose) => void;
}) {
  const list: Loose[] = accounts?.accounts || [];
  const first = list[0]?.address || "";
  const [selected, setSelected] = useState(first);

  useEffect(() => {
    if (!list.some((row) => row.address === selected)) {
      setSelected(list[0]?.address || "");
    }
  }, [list, selected]);

  const acc = list.find((row) => row.address === selected) || null;
  const dossier = acc?.dossier || {};
  const operator = dossier.operator || {};
  const how = dossier.how_they_bet || acc?.patterns || {};
  const llm = acc?.llm_analysis || {};
  const topicRows = how.topic_rows || [];
  const bandRows = how.band_rows || [];
  const sideRows = how.side_rows || [];
  const sources: Loose[] = dossier.sources || [];
  const steps: string[] = dossier.copy_steps || [];
  const opens: Loose[] = (acc?.open_positions || []).slice(0, 12);
  const closed: Loose[] = (acc?.closed_positions || acc?.closed_sample || []).slice(0, 8);
  const kind = operator.kind || "unclear";

  if (!list.length) {
    return (
      <section className="panel">
        <h2>Top account dossiers</h2>
        <p className="muted">
          No investigated accounts yet. Run an investigation from the Top accounts tab, then come back here to switch
          wallets and read how they bet.
        </p>
      </section>
    );
  }

  return (
    <section className="panel">
      <div className="row" style={{ justifyContent: "space-between", alignItems: "flex-end" }}>
        <div>
          <h2>Top account dossiers</h2>
          <p className="muted">
            Switch a wallet to see operator type, how they bet, how to copy it on paper, and the public feeds that
            usually price their topic. Generated {accounts?.generated_at_est || "—"}.
          </p>
        </div>
        <label className="choice-block" style={{ margin: 0 }}>
          <div className="choice-label">Account</div>
          <select value={selected} onChange={(event) => setSelected(event.target.value)} style={{ minWidth: 280 }}>
            {list.map((row) => (
              <option key={row.address} value={row.address}>
                {row.user_name || row.address?.slice(0, 10)} — {money(row.pnl)} PnL
              </option>
            ))}
          </select>
        </label>
      </div>

      {acc && (
        <>
          <div className="dossier-head">
            <div>
              <div className="dossier-name">{acc.user_name || acc.address}</div>
              <div className="muted mono">{acc.address}</div>
            </div>
            <span className={`op-badge op-${kind}`}>{operator.label || "Unclear operator"}</span>
            {acc.profile_url && (
              <a className="external" href={acc.profile_url} target="_blank" rel="noreferrer">
                Open on Polymarket
              </a>
            )}
            {onOpenAccount && (
              <button type="button" className="linkish" onClick={() => onOpenAccount(acc)}>
                Full trade history
              </button>
            )}
          </div>

          <div className="stat-strip">
            <div>
              <div className="muted">Volume</div>
              <strong>{money(acc.volume)}</strong>
            </div>
            <div>
              <div className="muted">PnL</div>
              <strong>{money(acc.pnl)}</strong>
            </div>
            <div>
              <div className="muted">Return on volume</div>
              <strong>{pct(acc.return_on_volume_pct)}</strong>
            </div>
            <div>
              <div className="muted">Win rate</div>
              <strong>{pct(acc.win_rate)}</strong>
            </div>
            <div>
              <div className="muted">Realized ROI</div>
              <strong>{pct(acc.realized_roi_pct)}</strong>
            </div>
            <div>
              <div className="muted">Copyability</div>
              <strong>{llm.copyability_label || "—"}</strong>
            </div>
            <div>
              <div className="muted">Bot score</div>
              <strong>{operator.bot_score ?? "—"}</strong>
            </div>
          </div>

          <div className="dossier-grid">
            <div className="panel inner-panel">
              <h2>General strategy</h2>
              <p>{llm.strategy_summary || llm.archetype || "No LLM write-up yet. Numbers below still describe the book."}</p>
              <p className="muted">{llm.edge_source}</p>
              <ul>
                {(llm.pattern_findings || []).map((item: string) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
            <div className="panel inner-panel">
              <h2>Bot or human</h2>
              <p>
                Scores are from trade plumbing, not from a KYC check. Split/merge, huge thin-margin volume, and heavy
                hedging push toward a bot. Fat return on volume and a short open book push toward a human desk.
              </p>
              <p>
                Bot {operator.bot_score ?? 0} / Human {operator.human_score ?? 0}
              </p>
              <ul>
                {(operator.reasons || []).map((item: string) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
            <div className="panel inner-panel">
              <h2>How to copy it</h2>
              <p>{llm.copy_recommendation}</p>
              <ol>
                {steps.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ol>
            </div>
            <div className="panel inner-panel">
              <h2>Likely APIs and information sources</h2>
              <p className="muted">
                These are the public feeds that usually price {how.dominant_topic || "this"} markets. They are research
                hypotheses, not proof this wallet subscribed to them.
              </p>
              <ul className="source-list">
                {sources.map((src) => (
                  <li key={src.label}>
                    <strong>{src.label}</strong>
                    <div className="muted mono">{src.api}</div>
                    <div>{src.why}</div>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="dossier-grid three">
            <div className="panel inner-panel">
              <h2>Topic mix</h2>
              <ShareBars rows={topicRows} labelKey="topic" valueKey="share" />
            </div>
            <div className="panel inner-panel">
              <h2>Entry price bands</h2>
              <ShareBars rows={bandRows} labelKey="band" valueKey="share" />
              <p className="muted">Typical entry {price(how.avg_entry_price)}</p>
            </div>
            <div className="panel inner-panel">
              <h2>Yes vs No</h2>
              <ShareBars rows={sideRows} labelKey="side" valueKey="share" />
              <p className="muted">Hedged events {pct(how.hedged_events_pct)} · split/merge {pct(how.split_merge_pct)}</p>
            </div>
          </div>

          <h2>Open book</h2>
          {opens.length === 0 ? (
            <p className="muted">No open positions in the last investigation sample.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Market</th>
                  <th>Side</th>
                  <th>Avg</th>
                  <th>Current</th>
                  <th>Size</th>
                </tr>
              </thead>
              <tbody>
                {opens.map((pos) => (
                  <tr key={`${pos.condition_id || pos.title}-${pos.outcome}`}>
                    <td>
                      {pos.title || pos.slug || "—"}
                      <div className="muted">
                        Started {asEst(pos.started_at_est || pos.start_date) || "--"}
                        <br />
                        Ends {asEst(pos.end_date || pos.ends_at_est) || "--"}
                      </div>
                    </td>
                    <td>{pos.outcome || "—"}</td>
                    <td>{price(pos.avgPrice ?? pos.avg_price)}</td>
                    <td>{price(pos.curPrice ?? pos.current_price)}</td>
                    <td>{money(pos.currentValue ?? pos.size)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {closed.length > 0 && (
            <>
              <h2>Recent closed sample</h2>
              <table>
                <thead>
                  <tr>
                    <th>Market</th>
                    <th>Side</th>
                    <th>Entry</th>
                    <th>PnL</th>
                  </tr>
                </thead>
                <tbody>
                  {closed.map((pos: Loose, idx: number) => (
                    <tr key={`${pos.title}-${idx}`}>
                      <td>
                        {pos.title || "—"}
                        <div className="muted">
                          Started {asEst(pos.started_at_est || pos.start_date) || "--"}
                          <br />
                          Ends {asEst(pos.end_date || pos.ends_at_est) || "--"}
                        </div>
                      </td>
                      <td>{pos.outcome || "—"}</td>
                      <td>{price(pos.avgPrice ?? pos.avg_price)}</td>
                      <td>{money(pos.realizedPnl ?? pos.pnl)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}
        </>
      )}
    </section>
  );
}
