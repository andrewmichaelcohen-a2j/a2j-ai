#!/usr/bin/env python3
"""
dev_set_monitor.py — Direction D, Component 1: Monitoring / Measurement
Copyright 2026 Andrew M Cohen. Apache 2.0.

Implements Item 13 (Cowork Change Directive, 2026-07-15, ratified YELLOW):
scheduled scorer re-runs on the v0.2 dev split ONLY, tracking score over
time and flagging regressions.

Hard guardrails (non-negotiable, enforced here — not just by convention):
  - Dev set only. Always calls ca_notice_scorer.run(..., non_held_out_only=True)
    against the v0.2 FROZEN golden set. The held-out split is never scored.
  - Read-only w.r.t. rules. This module never writes to rules/eviction/** or
    PLAYBOOK_SPEC. It only reads scorer output and appends to the ledger/
    changelog (append-only, descriptive-evidence docs — see METRICS_LEDGER's
    own "Discipline" section).
  - No training-signal creep. The tracked signal is the scorer's legal-accuracy
    score against attorney-frozen ground truth. This module has no path to
    litigation-outcome data and does not accept any.

Timing guardrail (Item 13, point 3): the Gemini-endpoint DNS RED means this
job must NOT run in the overnight window. This module self-enforces a
daytime/evening window (09:00-23:00 Pacific by default) regardless of when
the external scheduler invokes it — if invoked inside the blocked window it
DEFERS (does not call the scorer, does not consume the cadence) rather than
trusting external cron/launchd configuration alone.

Cadence guardrail (Item 13, point 3): every 3 days, OR immediately when
TRIGGER_FLAG_PATH exists (wired for "immediately after any ratified rule
change" — currently never fires because no rule change is possible until
v0.3 scoring completes, but the trigger mechanism is live now per the
directive: "wire the trigger now").

Usage:
    # Normal scheduled invocation (self-throttles on time-window + cadence)
    python3 dev_set_monitor.py

    # Force a run regardless of window/cadence (baseline / manual)
    python3 dev_set_monitor.py --force

    # Dry run (no live API calls; validates the whole pipeline end-to-end)
    python3 dev_set_monitor.py --force --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore

_SCORER_DIR = Path(__file__).resolve().parent
_VAL_ROOT = _SCORER_DIR.parent
_REPO_ROOT = _VAL_ROOT.parent.parent
sys.path.insert(0, str(_SCORER_DIR))

import ca_notice_scorer  # noqa: E402

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

FROZEN_XLSX = _SCORER_DIR / "FROZEN" / "goldenset_CA_notice_v0.2_20260701.xlsx"

TREND_LOG   = _SCORER_DIR / "output" / "dev_set_trend.jsonl"
TRIGGER_FLAG_PATH = _SCORER_DIR / "output" / "RULE_CHANGE_TRIGGER.flag"

DAILY_CHANGELOG = _REPO_ROOT / "docs" / "DAILY_CHANGELOG.md"
METRICS_LEDGER  = _REPO_ROOT / "docs" / "VALIDATION_METRICS_LEDGER.md"

CADENCE_DAYS = 3

# Daytime/evening window (Pacific), inclusive start, exclusive end. Chosen to
# comfortably avoid the ~2-5 AM DNS-failure window plus margin on both sides.
# Proposed run time in the directive: ~6:00 PM PT, which falls inside this
# window. Revisit (YELLOW, log for ratification) once the DNS RED closes.
DAYTIME_WINDOW_START_HOUR = 9
DAYTIME_WINDOW_END_HOUR   = 23
PACIFIC_TZ = "America/Los_Angeles"

# The 12 items that make up the v0.2 dev (non-held-out) split, per
# VALIDATION_METRICS_LEDGER / DAILY_CHANGELOG 2026-07-01 (v0.2 FROZEN, 17
# items, 5 held out). Used as a defense-in-depth assertion only — the actual
# partition is always computed by ca_notice_scorer from the Held-out column,
# never hardcoded into the scoring path itself.
EXPECTED_DEV_SET_IDS = {
    "CA-NOT-B-02", "CA-NOT-B-05", "CA-NOT-B-06", "CA-NOT-B-07", "CA-NOT-B-08",
    "CA-NOT-B-09", "CA-NOT-B-10", "CA-NOT-B-11", "CA-NOT-B-12", "CA-NOT-B-15",
    "CA-NOT-B-16", "CA-NOT-B-17",
}


# ---------------------------------------------------------------------------
# Time / cadence guards
# ---------------------------------------------------------------------------

def _pacific_now() -> datetime:
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo(PACIFIC_TZ))
    return datetime.now(timezone.utc)  # pragma: no cover — fallback only


def in_daytime_window(now: Optional[datetime] = None) -> bool:
    now = now or _pacific_now()
    return DAYTIME_WINDOW_START_HOUR <= now.hour < DAYTIME_WINDOW_END_HOUR


def _load_trend() -> list[dict]:
    if not TREND_LOG.exists():
        return []
    entries = []
    with open(TREND_LOG) as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def _last_run_entry(trend: list[dict]) -> Optional[dict]:
    return trend[-1] if trend else None


def cadence_due(trend: list[dict], now: Optional[datetime] = None) -> bool:
    """True if >= CADENCE_DAYS have passed since the last logged run."""
    last = _last_run_entry(trend)
    if last is None:
        return True
    now = now or _pacific_now()
    last_dt = datetime.fromisoformat(last["run_timestamp"])
    return (now - last_dt).total_seconds() >= CADENCE_DAYS * 86400


def trigger_pending() -> bool:
    return TRIGGER_FLAG_PATH.exists()


def consume_trigger() -> None:
    if TRIGGER_FLAG_PATH.exists():
        TRIGGER_FLAG_PATH.unlink()


def arm_trigger(reason: str) -> None:
    """Called elsewhere (post-ratified-rule-change hook) to force the next run."""
    TRIGGER_FLAG_PATH.parent.mkdir(parents=True, exist_ok=True)
    TRIGGER_FLAG_PATH.write_text(
        json.dumps({"armed_at": _pacific_now().isoformat(), "reason": reason}, indent=2)
    )


# ---------------------------------------------------------------------------
# Pure diff / formatting helpers (independently unit-testable, no API calls)
# ---------------------------------------------------------------------------

def compute_newly_failing(prev_pass_map: dict, curr_pass_map: dict) -> list:
    """
    Items that are failing NOW but were CONFIRMED PASSING on the immediately
    prior run. This is the regression alarm — a detected behavior CHANGE,
    not an absolute failure state.

    An item with no prior record (not in prev_pass_map — either because this
    is the very first monitoring run ever, or the item is new to the dev set)
    is never flagged: there is no known-good baseline to regress FROM, so
    treating it as a "regression" would be a false alarm. It still shows up
    as a failure in the raw dev score for that run; it just isn't a NEW one.
    Deterministic; no I/O.
    """
    newly_failing = []
    for item_id, passed_now in sorted(curr_pass_map.items()):
        if passed_now:
            continue
        if prev_pass_map.get(item_id) is True:
            newly_failing.append(item_id)
    return newly_failing


def format_ledger_entry(run_meta: dict) -> str:
    return (
        f"| {run_meta['run_date']} | {run_meta['dev_score']}/{run_meta['n']} "
        f"({run_meta['dev_score_pct']}%) | {run_meta['newly_failing_count']} | "
        f"{run_meta['alpha']} | {run_meta['consensus_status']} | "
        f"{run_meta['run_id']} |\n"
    )


LEDGER_SECTION_HEADER = "### Direction D-1 — Dev-Set Monitoring (scheduled, non-held-out)"
LEDGER_TABLE_HEADER = (
    "| Date | Dev score | Newly failing | α (dev) | Consensus status | Run ID |\n"
    "| :-- | :-- | :-- | :-- | :-- | :-- |\n"
)


def append_ledger_entry(run_meta: dict) -> None:
    """Append-only. Never edits a prior row (matches the ledger's own discipline
    section: 'Log every run the same way, even when numbers are unflattering')."""
    text = METRICS_LEDGER.read_text() if METRICS_LEDGER.exists() else ""
    row = format_ledger_entry(run_meta)
    if LEDGER_SECTION_HEADER not in text:
        addition = (
            "\n\n---\n\n"
            f"{LEDGER_SECTION_HEADER}\n\n"
            "Scheduled runs of ca_notice_scorer.py against the v0.2 dev split "
            "(12 items, non-held-out) only. The held-out split is never scored "
            "by this component. Tracks score-over-time and regressions "
            "(newly_failing). Cadence: every 3 days, daytime/evening window "
            "only (Item 13, ratified YELLOW 2026-07-15) while the Gemini-endpoint "
            "DNS RED is open.\n\n"
            + LEDGER_TABLE_HEADER
            + row
        )
        text = text.rstrip("\n") + addition
    else:
        text = text.rstrip("\n") + "\n" + row
    METRICS_LEDGER.write_text(text)


def format_changelog_alert(run_meta: dict) -> str:
    lines = [
        "",
        f"**Direction D-1 regression alarm — dev-set monitor ({run_meta['run_id']})**",
        f"- Dev score: {run_meta['dev_score']}/{run_meta['n']} "
        f"({run_meta['dev_score_pct']}%). Consensus status: {run_meta['consensus_status']}.",
        (f"- Newly failing ({run_meta['newly_failing_count']}): "
         + ", ".join(run_meta['newly_failing'])) if run_meta['newly_failing'] else
        "- Newly failing: none",
        "- Regression findings are reported, not auto-fixed — rules remain frozen "
        "as vProof1. Queued for Andy per Direction D read-only guardrail.",
        "",
    ]
    return "\n".join(lines)


def append_changelog_alert(run_meta: dict) -> None:
    if not run_meta["newly_failing"]:
        return
    text = DAILY_CHANGELOG.read_text() if DAILY_CHANGELOG.exists() else ""
    alert = format_changelog_alert(run_meta)
    # Insert right after the file header so it is impossible to miss on the
    # next read, without disturbing any existing dated sections below.
    marker = "\n---\n"
    idx = text.find(marker)
    if idx == -1:
        text = text.rstrip("\n") + "\n" + alert
    else:
        insert_at = idx + len(marker)
        text = text[:insert_at] + alert + text[insert_at:]
    DAILY_CHANGELOG.write_text(text)


# ---------------------------------------------------------------------------
# Main run
# ---------------------------------------------------------------------------

def run_dev_set_monitor(force: bool = False, dry_run: bool = False,
                         sleep_s: int = 2) -> dict:
    now = _pacific_now()
    trend = _load_trend()

    if not force and not in_daytime_window(now):
        return {"status": "deferred-time-window",
                "detail": f"Pacific hour={now.hour}, allowed "
                          f"[{DAYTIME_WINDOW_START_HOUR},{DAYTIME_WINDOW_END_HOUR})"}

    triggered = trigger_pending()
    if not force and not triggered and not cadence_due(trend, now):
        last = _last_run_entry(trend)
        return {"status": "deferred-cadence",
                "detail": f"last run {last['run_timestamp']} < {CADENCE_DAYS}d ago"}

    # ---- Run the scorer, dev split only ----
    output = ca_notice_scorer.run(
        FROZEN_XLSX, dry_run=dry_run, non_held_out_only=True, sleep_s=sleep_s,
    )

    if triggered:
        consume_trigger()

    non_ho = output["summary"]["non_held_out"]
    n = non_ho["n"] or 0

    scored_ids = {r["id"] for r in output["results"]}
    if not dry_run and scored_ids and scored_ids - EXPECTED_DEV_SET_IDS:
        # Defense in depth: the scorer's own held_out column is authoritative,
        # but if the dev split ever drifts from what this component expects,
        # STOP rather than silently score an unexpected item (could be a
        # held-out item if the golden set were ever mis-edited).
        raise RuntimeError(
            "Dev-set guardrail violation: scored items include IDs outside "
            f"the expected v0.2 dev split: {sorted(scored_ids - EXPECTED_DEV_SET_IDS)}. "
            "Refusing to log this run. Escalate — do not re-run automatically."
        )

    curr_pass_map = {r["id"]: bool(r["is_correct"]) for r in output["results"]}

    prev_entry = _last_run_entry(trend)
    prev_pass_map = prev_entry["per_item_pass"] if prev_entry else {}
    newly_failing = compute_newly_failing(prev_pass_map, curr_pass_map)

    alpha = round(non_ho["model_agree"] / n, 3) if n else None

    run_meta = {
        "run_id":             output["run_id"],
        "run_date":           output["run_date"],
        "run_timestamp":      now.isoformat(),
        "dev_score":          non_ho["correct"],
        "n":                  n,
        "dev_score_pct":      non_ho["accuracy_pct"],
        "alpha":              alpha,
        "consensus_status":   output["consensus_status"],
        "single_model_items": non_ho.get("single_model_items", 0),
        "newly_failing":      newly_failing,
        "newly_failing_count": len(newly_failing),
        "per_item_pass":      curr_pass_map,
        "dry_run":            dry_run,
        "triggered_by_rule_change": triggered,
    }

    # ---- Persist ----
    TREND_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(TREND_LOG, "a") as f:
        f.write(json.dumps(run_meta, default=str) + "\n")

    if not dry_run:
        append_ledger_entry(run_meta)
        append_changelog_alert(run_meta)

    run_meta["status"] = "ran"
    return run_meta


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--force", action="store_true",
                         help="Ignore time-window and cadence guards (baseline/manual run).")
    parser.add_argument("--dry-run", action="store_true",
                         help="No live API calls; mocked predictions; still appended to "
                              "the trend log so the pipeline can be exercised end-to-end, "
                              "but does NOT write to the ledger/changelog (those are for "
                              "real runs only).")
    parser.add_argument("--sleep", type=int, default=2)
    args = parser.parse_args()

    result = run_dev_set_monitor(force=args.force, dry_run=args.dry_run, sleep_s=args.sleep)
    print(json.dumps(result, indent=2, default=str))
    if result.get("status", "").startswith("deferred"):
        sys.exit(0)
    if result.get("newly_failing"):
        print(f"\n⚠️  REGRESSION ALARM: {len(result['newly_failing'])} newly-failing "
              f"item(s): {result['newly_failing']}", file=sys.stderr)


if __name__ == "__main__":
    main()
