"""Run the top earning accounts (% ROI vs Volume) investigation with Ollama LLM analysis."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.research.top_accounts import TOP_ACCOUNTS_PATH, run_top_accounts_investigation


def main():
    parser = argparse.ArgumentParser(description="Investigate top Polymarket accounts by % ROI and Volume with LLM.")
    parser.add_argument("--period", default="ALL", choices=["DAY", "WEEK", "MONTH", "ALL"])
    parser.add_argument("--count", type=int, default=16)
    parser.add_argument("--model", default="llama3.2:latest")
    args = parser.parse_args()

    payload = run_top_accounts_investigation(
        time_period=args.period,
        max_candidates=args.count,
        model=args.model,
        save=True,
    )

    syn = payload["synthesis"]
    print("\n=== TOP ACCOUNTS INVESTIGATION SUMMARY ===")
    print(f"Generated at: {payload['generated_at_est']}")
    print(f"Pool scanned: {payload['pool_scanned']} accounts | Deeply profiled: {syn['total_accounts_investigated']}")
    print(
        f"% Earners avg RoV: {syn['pct_earners_avg_rov_pct']}% (Copyability {syn['pct_earners_avg_copyability']}/10) | "
        f"Volume Whales avg RoV: {syn['vol_earners_avg_rov_pct']}% (Copyability {syn['vol_earners_avg_copyability']}/10)"
    )
    print("\n--- Accounts Profiled ---")
    for acc in payload["accounts"]:
        llm = acc.get("llm_analysis", {})
        print(
            f"{acc['user_name']:18} | Cohort: {acc['earning_cohort_label']:20} | "
            f"PnL: ${acc['pnl']:12,.0f} | Vol: ${acc['volume']:14,.0f} | "
            f"RoV: {acc['return_on_volume_pct']:6.2f}% | "
            f"Realized ROI: {str(acc['realized_roi_pct']) + '%':8} | "
            f"WinRate: {str(acc['win_rate_pct']) + '%':6} | "
            f"Copy: {llm.get('copyability_score')}/10 | {llm.get('archetype')}"
        )
    print(f"\nSaved to {TOP_ACCOUNTS_PATH} ({len(payload['copy_signals'])} copyable open signals found)")


if __name__ == "__main__":
    main()
