#!/usr/bin/env python3
"""
Regression tests for ca_notice_scorer.py's "Correct outcome (if corrected)"
fallback fix (2026-07-18, discovered while ingesting the v0.3 held-out
FROZEN set for Broaden Proof 1 Steps 5-7).

Root issue: every FROZEN row in goldenset_CA_notice_v0.3_FROZEN_20260716.xlsx
has ATTORNEY VERDICT=CONFIRM and a blank "Correct outcome (if corrected)"
cell -- by the column's own name, blank means "not corrected," not "missing."
The scorer previously required that column to be populated for every FROZEN
item regardless of verdict, which would have skipped all 26 held-out items
as YELLOW-INCOMPLETE. Fixed by falling back to "Drafted outcome" ONLY when
ATTORNEY VERDICT is CONFIRM/CONFIRMED -- an explicit "Correct outcome" value
always wins, and any other (or blank) verdict still fails loud via the
existing YELLOW-INCOMPLETE path. No frozen data file is modified by this
fix; it only changes how the existing columns are interpreted.

Uses in-memory openpyxl workbooks (no real xlsx files touched, no network).

Run with:
  python3 rules/validation/tests/test_ca_notice_scorer_outcome_fallback.py

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import sys
import tempfile
from pathlib import Path

import openpyxl

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "rules" / "validation" / "scorer"))

import ca_notice_scorer as cns  # noqa: E402

_PASS = []
_FAIL = []


def test(name: str, condition: bool, detail: str = ""):
    if condition:
        _PASS.append(name)
        print(f"  ✓  {name}")
    else:
        _FAIL.append(name)
        print(f"  ✗  {name}{' — ' + detail if detail else ''}")


HEADERS = [
    "ID", "Module", "Jurisdiction", "Facts (scenario)", "Drafted outcome",
    "Controlling authority", "ATTORNEY VERDICT", "Correct outcome (if corrected)",
    "Reason / note (required if corrected)", "Status", "Held-out (TRUE/FALSE)",
    "Reviewed by", "Date",
]


def _make_xlsx(rows: list[dict]) -> Path:
    """Build a minimal golden-set xlsx from a list of row dicts (keys = a
    subset of HEADERS; missing keys default to '')."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(HEADERS)
    for row in rows:
        ws.append([row.get(h, "") for h in HEADERS])
    tmp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
    wb.save(tmp.name)
    return Path(tmp.name)


def _base_row(**overrides) -> dict:
    row = {
        "ID": "CA-NOT-X-01",
        "Module": "notice",
        "Jurisdiction": "CA",
        "Facts (scenario)": "some facts",
        "Drafted outcome": "NOTICE_VALID",
        "Controlling authority": "CCP 1161",
        "ATTORNEY VERDICT": "CONFIRM",
        "Correct outcome (if corrected)": "",
        "Reason / note (required if corrected)": "",
        "Status": "FROZEN",
        "Held-out (TRUE/FALSE)": "TRUE",
        "Reviewed by": "Andrew M. Cohen",
        "Date": "2026-07-16",
    }
    row.update(overrides)
    return row


# ══════════════════════════════════════════════════════════════════════════════
# The core fallback behavior
# ══════════════════════════════════════════════════════════════════════════════

def test_confirm_blank_correct_outcome_falls_back_to_drafted():
    xlsx = _make_xlsx([_base_row(ID="CA-NOT-X-01", **{"Drafted outcome": "NOTICE_INVALID"})])
    items, yellows = cns.load_golden_set(xlsx)
    test("CONFIRM + blank correct_outcome resolves to drafted_outcome",
         len(items) == 1 and items[0]["correct_outcome"] == "NOTICE_INVALID", items)
    test("outcome_source records it came from the CONFIRM fallback",
         items[0]["outcome_source"] == "drafted (ATTORNEY VERDICT=CONFIRM)", items[0].get("outcome_source"))
    test("no YELLOW-INCOMPLETE raised for a resolved CONFIRM row",
         not any("YELLOW-INCOMPLETE" in y and "CA-NOT-X-01" in y for y in yellows), yellows)


def test_confirmed_variant_also_falls_back():
    xlsx = _make_xlsx([_base_row(**{"ATTORNEY VERDICT": "CONFIRMED", "Drafted outcome": "NOTICE_VALID"})])
    items, yellows = cns.load_golden_set(xlsx)
    test("'CONFIRMED' (v0.2-style verdict text) also triggers the fallback",
         items[0]["correct_outcome"] == "NOTICE_VALID", items)


def test_explicit_correct_outcome_always_wins_over_drafted():
    """Non-regression: v0.2-style rows that DO populate 'Correct outcome'
    explicitly (even when confirming) must keep using that value, never the
    fallback -- matches the existing v0.2 FROZEN file convention exactly."""
    xlsx = _make_xlsx([_base_row(
        **{"Drafted outcome": "NOTICE_VALID", "Correct outcome (if corrected)": "NOTICE_INVALID"}
    )])
    items, yellows = cns.load_golden_set(xlsx)
    test("an explicit 'Correct outcome' value is never overridden by 'Drafted outcome'",
         items[0]["correct_outcome"] == "NOTICE_INVALID", items)
    test("outcome_source records it as an explicit correction",
         items[0]["outcome_source"] == "corrected", items[0].get("outcome_source"))


def test_blank_verdict_with_blank_correct_outcome_still_fails_loud():
    """Non-regression: the whole point of the original design (never
    silently repair frozen items) must still hold for genuinely incomplete
    rows -- i.e. anything that ISN'T an explicit CONFIRM verdict."""
    xlsx = _make_xlsx([_base_row(**{"ATTORNEY VERDICT": "", "Drafted outcome": "NOTICE_VALID"})])
    items, yellows = cns.load_golden_set(xlsx)
    test("a blank verdict with blank correct_outcome does NOT get the fallback",
         items[0]["correct_outcome"] == "", items)
    test("a blank verdict with blank correct_outcome still raises YELLOW-INCOMPLETE",
         any("YELLOW-INCOMPLETE" in y and "CA-NOT-X-01" in y for y in yellows), yellows)


def test_unrecognized_verdict_with_blank_correct_outcome_still_fails_loud():
    xlsx = _make_xlsx([_base_row(**{"ATTORNEY VERDICT": "REVISE", "Drafted outcome": "NOTICE_VALID"})])
    items, yellows = cns.load_golden_set(xlsx)
    test("an unrecognized verdict (not CONFIRM/CONFIRMED) does not trigger the fallback",
         items[0]["correct_outcome"] == "", items)
    test("...and still raises YELLOW-INCOMPLETE (fail loud, not silently guessed)",
         any("YELLOW-INCOMPLETE" in y for y in yellows), yellows)


def test_confirm_with_blank_drafted_outcome_still_fails_loud():
    """Edge case: CONFIRM verdict but Drafted outcome is ALSO blank -- there
    is nothing to fall back to, so this must still fail loud rather than
    silently producing an empty correct_outcome that looks resolved."""
    xlsx = _make_xlsx([_base_row(**{"ATTORNEY VERDICT": "CONFIRM", "Drafted outcome": ""})])
    items, yellows = cns.load_golden_set(xlsx)
    test("CONFIRM with no Drafted outcome to fall back to leaves correct_outcome blank",
         items[0]["correct_outcome"] == "", items)
    test("...and raises YELLOW-INCOMPLETE rather than silently succeeding",
         any("YELLOW-INCOMPLETE" in y for y in yellows), yellows)


def test_excluded_rows_still_silently_skipped_regardless():
    xlsx = _make_xlsx([_base_row(Status="EXCLUDED", **{"ATTORNEY VERDICT": "EXCLUDE"})])
    items, yellows = cns.load_golden_set(xlsx)
    test("EXCLUDED status rows are still silently skipped (unaffected by this fix)",
         items == [] and yellows == [], (items, yellows))


def test_mixed_set_matches_v0_3_real_pattern():
    """Reproduces the exact real-world v0.3 pattern: a run of CONFIRM/blank
    rows plus an EXCLUDED row, checking the whole batch resolves correctly
    and only the FROZEN rows are scoreable."""
    rows = [
        _base_row(ID="CA-NOT-X-01", **{"Drafted outcome": "NOTICE_INVALID"}),
        _base_row(ID="CA-NOT-X-02", **{"Drafted outcome": "NOTICE_VALID"}),
        _base_row(ID="CA-NOT-X-03", Status="EXCLUDED", **{"ATTORNEY VERDICT": "EXCLUDE"}),
    ]
    xlsx = _make_xlsx(rows)
    items, yellows = cns.load_golden_set(xlsx)
    ids = {i["id"]: i["correct_outcome"] for i in items}
    test("mixed CONFIRM+EXCLUDED batch resolves exactly like the real v0.3 file",
         ids == {"CA-NOT-X-01": "NOTICE_INVALID", "CA-NOT-X-02": "NOTICE_VALID"}, ids)
    test("no YELLOWs at all for a clean CONFIRM+EXCLUDED batch", yellows == [], yellows)


# ══════════════════════════════════════════════════════════════════════════════
# Runner
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    print(f"Running {len(tests)} test functions...\n")
    for t in tests:
        t()
    print(f"\nResults: {len(_PASS)}/{len(_PASS) + len(_FAIL)} passed")
    if _FAIL:
        print(f"FAILED: {_FAIL}")
        sys.exit(1)
