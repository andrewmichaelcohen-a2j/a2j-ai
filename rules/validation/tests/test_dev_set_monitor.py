#!/usr/bin/env python3
"""
Regression tests for dev_set_monitor.py (Item 13, Direction D-1).

Covers the guardrails and the regression-flag (newly_failing) path with no
live API calls and no network access — pure functions + tmp-file I/O only.

Run with:
  python3 rules/validation/tests/test_dev_set_monitor.py

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "rules" / "validation" / "scorer"))

import dev_set_monitor as dsm  # noqa: E402

_PASS = []
_FAIL = []


def test(name: str, condition: bool, detail: str = ""):
    if condition:
        _PASS.append(name)
        print(f"  ✓  {name}")
    else:
        _FAIL.append(name)
        print(f"  ✗  {name}{' — ' + detail if detail else ''}")


# ══════════════════════════════════════════════════════════════════════════════
# compute_newly_failing — the regression alarm itself
# ══════════════════════════════════════════════════════════════════════════════

def test_newly_failing_detects_a_fresh_regression():
    prev = {"A": True, "B": True, "C": True}
    curr = {"A": True, "B": False, "C": True}  # B flipped pass -> fail
    result = dsm.compute_newly_failing(prev, curr)
    test("single simulated regression (B) is detected", result == ["B"], result)


def test_newly_failing_ignores_persistent_failures():
    prev = {"A": False, "B": True}
    curr = {"A": False, "B": True}  # A was already failing — not NEW
    result = dsm.compute_newly_failing(prev, curr)
    test("persistent (pre-existing) failure is NOT reported as newly failing",
         result == [], result)


def test_newly_failing_ignores_recoveries():
    prev = {"A": False}
    curr = {"A": True}
    result = dsm.compute_newly_failing(prev, curr)
    test("a recovered item produces no alarm", result == [], result)


def test_newly_failing_first_run_no_prior_data():
    prev = {}
    curr = {"A": False, "B": True}
    result = dsm.compute_newly_failing(prev, curr)
    test("first run (no prior trend) does not alarm on failures "
         "(nothing to regress FROM)", result == [], str(result))


def test_newly_failing_new_item_with_no_baseline_not_flagged():
    """A dev-set item added after the baseline was established shouldn't be
    treated as a 'regression' the first time it's scored, even if a prior
    trend already exists for OTHER items."""
    prev = {"A": True}
    curr = {"A": True, "NEW-ITEM": False}
    result = dsm.compute_newly_failing(prev, curr)
    test("brand-new item with no prior record is not flagged as a regression",
         result == [], str(result))


def test_newly_failing_multiple_simultaneous_regressions():
    prev = {"A": True, "B": True, "C": True, "D": False}
    curr = {"A": False, "B": False, "C": True, "D": False}
    result = dsm.compute_newly_failing(prev, curr)
    test("multiple simultaneous regressions all detected, pre-existing D excluded",
         result == ["A", "B"], result)


# ══════════════════════════════════════════════════════════════════════════════
# Time-window guard (must avoid the overnight DNS-RED window)
# ══════════════════════════════════════════════════════════════════════════════

def test_daytime_window_blocks_overnight_hour():
    now = datetime(2026, 7, 15, 3, 0)  # 3 AM — inside the DNS-failure window
    test("3 AM is blocked (inside DNS RED window)", dsm.in_daytime_window(now) is False)


def test_daytime_window_allows_proposed_run_time():
    now = datetime(2026, 7, 15, 18, 0)  # 6 PM PT — the directive's proposed time
    test("6 PM (proposed run time) is allowed", dsm.in_daytime_window(now) is True)


def test_daytime_window_boundaries():
    test("09:00 boundary is allowed (inclusive start)",
         dsm.in_daytime_window(datetime(2026, 7, 15, 9, 0)) is True)
    test("23:00 boundary is blocked (exclusive end)",
         dsm.in_daytime_window(datetime(2026, 7, 15, 23, 0)) is False)
    test("08:59 is blocked", dsm.in_daytime_window(datetime(2026, 7, 15, 8, 59)) is False)


# ══════════════════════════════════════════════════════════════════════════════
# Cadence guard (every 3 days)
# ══════════════════════════════════════════════════════════════════════════════

def test_cadence_due_when_no_prior_runs():
    test("cadence is due when trend is empty (first run)",
         dsm.cadence_due([], datetime(2026, 7, 15, 18, 0)) is True)


def test_cadence_not_due_within_window():
    trend = [{"run_timestamp": datetime(2026, 7, 14, 18, 0).isoformat()}]
    test("cadence NOT due 1 day after last run (< 3 days)",
         dsm.cadence_due(trend, datetime(2026, 7, 15, 18, 0)) is False)


def test_cadence_due_after_three_days():
    trend = [{"run_timestamp": datetime(2026, 7, 10, 18, 0).isoformat()}]
    test("cadence due 5 days after last run (>= 3 days)",
         dsm.cadence_due(trend, datetime(2026, 7, 15, 18, 0)) is True)


# ══════════════════════════════════════════════════════════════════════════════
# Ledger / changelog append — the "surfaces in report logic" path
# ══════════════════════════════════════════════════════════════════════════════

_BASE_RUN_META = {
    "run_id": "ca_notice_score_TEST",
    "run_date": "2026-07-15",
    "dev_score": 11,
    "n": 12,
    "dev_score_pct": 91.7,
    "alpha": 0.917,
    "consensus_status": "DUAL-MODEL-CONSENSUS",
    "newly_failing": [],
    "newly_failing_count": 0,
}


def test_ledger_entry_created_with_section_header_on_first_write():
    with tempfile.TemporaryDirectory() as td:
        ledger_path = Path(td) / "VALIDATION_METRICS_LEDGER.md"
        ledger_path.write_text("# Existing ledger\n\nSome prior content.\n")
        with patch.object(dsm, "METRICS_LEDGER", ledger_path):
            dsm.append_ledger_entry(_BASE_RUN_META)
        text = ledger_path.read_text()
        test("ledger section header added on first write",
             dsm.LEDGER_SECTION_HEADER in text)
        test("prior ledger content preserved (append-only)",
             "Some prior content." in text)
        test("run row present in ledger", "ca_notice_score_TEST" in text)


def test_ledger_entry_appends_without_duplicating_header():
    with tempfile.TemporaryDirectory() as td:
        ledger_path = Path(td) / "VALIDATION_METRICS_LEDGER.md"
        ledger_path.write_text("# Existing ledger\n")
        with patch.object(dsm, "METRICS_LEDGER", ledger_path):
            dsm.append_ledger_entry(_BASE_RUN_META)
            meta2 = dict(_BASE_RUN_META, run_id="ca_notice_score_TEST2", run_date="2026-07-18")
            dsm.append_ledger_entry(meta2)
        text = ledger_path.read_text()
        test("section header appears exactly once across two runs",
             text.count(dsm.LEDGER_SECTION_HEADER) == 1)
        test("both run rows present", "TEST" in text and "TEST2" in text)


def test_changelog_alert_fires_only_when_newly_failing_nonempty():
    with tempfile.TemporaryDirectory() as td:
        changelog_path = Path(td) / "DAILY_CHANGELOG.md"
        changelog_path.write_text("# CJaC Daily Changelog\n\n*header text*\n\n---\n\n## prior entry\n")
        clean_meta = dict(_BASE_RUN_META)
        with patch.object(dsm, "DAILY_CHANGELOG", changelog_path):
            dsm.append_changelog_alert(clean_meta)
        test("no alert written when newly_failing is empty",
             changelog_path.read_text() == "# CJaC Daily Changelog\n\n*header text*\n\n---\n\n## prior entry\n")


def test_changelog_alert_fires_and_names_the_regressed_items():
    with tempfile.TemporaryDirectory() as td:
        changelog_path = Path(td) / "DAILY_CHANGELOG.md"
        changelog_path.write_text("# CJaC Daily Changelog\n\n*header text*\n\n---\n\n## prior entry\n")
        regressed_meta = dict(_BASE_RUN_META, newly_failing=["CA-NOT-B-06"], newly_failing_count=1)
        with patch.object(dsm, "DAILY_CHANGELOG", changelog_path):
            dsm.append_changelog_alert(regressed_meta)
        text = changelog_path.read_text()
        test("regression alarm block written to changelog",
             "regression alarm" in text)
        test("regressed item ID named in the alert", "CA-NOT-B-06" in text)
        test("prior changelog content preserved", "## prior entry" in text)


# ── Runner ──────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("dev_set_monitor.py — Regression Test Suite (Item 13)")
    print("=" * 60)
    print()

    print("compute_newly_failing — the regression alarm")
    test_newly_failing_detects_a_fresh_regression()
    test_newly_failing_ignores_persistent_failures()
    test_newly_failing_ignores_recoveries()
    test_newly_failing_first_run_no_prior_data()
    test_newly_failing_new_item_with_no_baseline_not_flagged()
    test_newly_failing_multiple_simultaneous_regressions()
    print()

    print("in_daytime_window — DNS-RED overnight guard")
    test_daytime_window_blocks_overnight_hour()
    test_daytime_window_allows_proposed_run_time()
    test_daytime_window_boundaries()
    print()

    print("cadence_due — every-3-days guard")
    test_cadence_due_when_no_prior_runs()
    test_cadence_not_due_within_window()
    test_cadence_due_after_three_days()
    print()

    print("ledger / changelog append — regression surfaces in report logic")
    test_ledger_entry_created_with_section_header_on_first_write()
    test_ledger_entry_appends_without_duplicating_header()
    test_changelog_alert_fires_only_when_newly_failing_nonempty()
    test_changelog_alert_fires_and_names_the_regressed_items()
    print()

    print("=" * 60)
    print(f"Results: {len(_PASS)}/{len(_PASS) + len(_FAIL)} passed, {len(_FAIL)} failed")
    print("=" * 60)
    if _FAIL:
        print("\nRED: fix before queueing.")
        return 1
    print("\nAll tests pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
