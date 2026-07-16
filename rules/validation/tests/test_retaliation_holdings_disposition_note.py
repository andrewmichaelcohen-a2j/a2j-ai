#!/usr/bin/env python3
"""
Regression tests for the Item 11 fix (2026-07-15): search-network-failure vs.
genuine no-candidates disposition_note.

Bug: the search-network-failure path (CourtListener unreachable during the
fresh-candidate search) recorded the SAME disposition note as the genuine
no-CL-coverage path ("No candidate cases in draft file for this state."),
conflating outages with true coverage gaps and slowing run forensics (e.g.
the KS/NV/SC coverage-gap analysis, which depends on distinguishing the two).
Confirmed in real historical run artifacts: c0a2df2d (2026-07-03), c7bcdcff
(2026-07-04), and e9222548 (2026-07-08) all show this exact mislabeled note
despite the DAILY_CHANGELOG documenting them as DNS/network outages.

Note: rules/validation/l2/retaliation_holdings_v3_runner.py already gained a
real network-retry ladder in two prior, separate sessions (2026-07-05 fix,
2026-07-08 extension to a ~66-min 60/120/240/600/1200/1800s ladder) that
correctly distinguishes network failure from a genuine empty search INSIDE
_run_search() / cl_search_retaliation_by_state() (returns (cases, net_err)
and prints the distinction) — but that signal was never wired to the
disposition_note the harness actually persists. This is the missing piece.

Fix (cosmetic/forensic only — no routing change):
  - rules/validation/l2/retaliation_holdings_v3_runner.py: at the end of
    cl_search_retaliation_by_state(), the final net_err verdict (from the
    existing retry ladder) is recorded in module-level
    _LAST_SEARCH_NETWORK_FAILURE[state] — True only when the search ended in
    a network failure with no cases found, False on any real HTTP response
    (including 0 hits) or when cases were found. Does not change the
    existing retry/backoff behavior at all.
  - rules/validation/protocols/retaliation_holdings_v3.py: get_units() tags
    the "no cases" sentinel unit with search_network_failure; run_unit()
    emits a distinct disposition_note for that case while leaving
    disposition ("permanent-failure"), bucket, and queue_routing (None)
    byte-identical to before.

Run with:
  python3 rules/validation/tests/test_retaliation_holdings_disposition_note.py

GREEN: all tests pass → the fix is safe and PR/RC/attorney-lane routing is
unchanged. RED: any failure → do not queue.

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "rules" / "validation" / "l2"))
sys.path.insert(0, str(_REPO_ROOT / "rules" / "validation" / "protocols"))
sys.path.insert(0, str(_REPO_ROOT / "rules" / "validation"))

import requests  # noqa: E402

import retaliation_holdings_v3_runner as runner  # noqa: E402
import retaliation_holdings_v3 as protocol  # noqa: E402

# ── Test harness (mirrors test_l2_procedural_defects.py) ──────────────────────

_PASS = []
_FAIL = []


def test(name: str, condition: bool, detail: str = ""):
    if condition:
        _PASS.append(name)
        print(f"  ✓  {name}")
    else:
        _FAIL.append(name)
        print(f"  ✗  {name}{' — ' + detail if detail else ''}")


def _mock_response(status_code=200, json_data=None):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_data or {"results": []}
    resp.raise_for_status = MagicMock()
    return resp


# ══════════════════════════════════════════════════════════════════════════════
# _run_search / cl_search_retaliation_by_state — network-failure tracking
# ══════════════════════════════════════════════════════════════════════════════

def test_network_failure_flagged_after_full_backoff_ladder():
    """All 7 attempts (1 initial + 6 backoff waits) raise a ConnectionError ->
    flagged True, returns []. Exercises the REAL 2026-07-05/07-08 ladder
    (60/120/240/600/1200/1800s) — time.sleep is mocked so this runs instantly."""
    runner._LAST_SEARCH_NETWORK_FAILURE.pop("ZZ", None)
    with patch.object(runner, "time") as mock_time, \
         patch.object(runner.requests, "get",
                       side_effect=requests.exceptions.ConnectionError("DNS failure")) as mock_get:
        cases = runner.cl_search_retaliation_by_state("ZZ")

    test("network failure returns empty list (unchanged external behavior)",
         cases == [])
    test("network failure sets _LAST_SEARCH_NETWORK_FAILURE[state] = True",
         runner._LAST_SEARCH_NETWORK_FAILURE.get("ZZ") is True)
    # ZZ has no configured statute -> only one query variant is run (no broad
    # fallback branch), so exactly 7 attempts (1 + 6 backoff slots) should
    # have been made, per the real ladder length in the runner.
    test("full backoff ladder attempted (7 tries) before giving up",
         mock_get.call_count == 7, f"got {mock_get.call_count} calls")
    test("backoff sleep called between retries (not fail-fast)",
         mock_time.sleep.call_count >= 6)


def test_genuine_empty_result_not_flagged_as_network_failure():
    """A real HTTP 200 with zero hits is NOT a network failure."""
    runner._LAST_SEARCH_NETWORK_FAILURE.pop("YY", None)
    with patch.object(runner, "time"), \
         patch.object(runner.requests, "get",
                       return_value=_mock_response(200, {"results": []})):
        cases = runner.cl_search_retaliation_by_state("YY")

    test("genuine empty search returns empty list", cases == [])
    test("genuine empty search sets _LAST_SEARCH_NETWORK_FAILURE[state] = False",
         runner._LAST_SEARCH_NETWORK_FAILURE.get("YY") is False)


def test_recovery_after_transient_network_errors_clears_flag():
    """Transport errors on early attempts, then a real response -> flag clears."""
    runner._LAST_SEARCH_NETWORK_FAILURE.pop("XX", None)
    responses = [
        requests.exceptions.ConnectionError("DNS failure"),
        requests.exceptions.Timeout("timed out"),
        _mock_response(200, {"results": []}),
    ]

    def _side_effect(*a, **kw):
        r = responses.pop(0)
        if isinstance(r, Exception):
            raise r
        return r

    with patch.object(runner, "time"), \
         patch.object(runner.requests, "get", side_effect=_side_effect):
        cases = runner.cl_search_retaliation_by_state("XX")

    test("recovers to empty list after transient errors then success", cases == [])
    test("flag cleared to False once a real HTTP response is received",
         runner._LAST_SEARCH_NETWORK_FAILURE.get("XX") is False)


def test_non_connection_exception_also_flagged_not_a_coverage_determination():
    """A non-ConnectionError/Timeout exception (e.g. bad JSON) is handled by the
    runner's generic except-Exception branch, which ALSO returns net_err=True
    (fail-fast, no retry — but still correctly NOT treated as evidence of a
    genuine empty search). This matches the real runner's existing semantics;
    this fix does not change that branch at all."""
    runner._LAST_SEARCH_NETWORK_FAILURE.pop("WW", None)
    bad_resp = MagicMock()
    bad_resp.status_code = 200
    bad_resp.raise_for_status = MagicMock()
    bad_resp.json.side_effect = ValueError("bad json")

    with patch.object(runner, "time"), \
         patch.object(runner.requests, "get", return_value=bad_resp) as mock_get:
        cases = runner.cl_search_retaliation_by_state("WW")

    test("non-connection exception still returns empty list", cases == [])
    test("non-connection exception is flagged not-a-coverage-determination "
         "(True) — matches the runner's existing fail-fast-but-not-genuine "
         "semantics, unchanged by this fix",
         runner._LAST_SEARCH_NETWORK_FAILURE.get("WW") is True)
    test("non-connection exception does not retry (fail-fast, unchanged prior behavior)",
         mock_get.call_count == 1, f"got {mock_get.call_count} calls")


def test_cases_found_always_clears_the_flag():
    """If cases are actually found, the flag must be False regardless of any
    earlier transient error on the statute-query attempt (defense in depth —
    get_units() only creates a sentinel unit when cases is empty, but the
    flag itself should never mislead if read for any other reason)."""
    runner._LAST_SEARCH_NETWORK_FAILURE.pop("VV-cases", None)
    hit = {
        "caseName": "Doe v. Roe", "court": "Vermont Supreme Court",
        "absolute_url": "/opinion/1/doe-v-roe/", "cluster_id": 1,
        "id": 1, "dateFiled": "2020-01-01",
    }
    with patch.object(runner, "time"), \
         patch.object(runner, "_court_matches_state", return_value=True), \
         patch.object(runner, "_build_case_from_hit", return_value={"case_name": "Doe v. Roe"}), \
         patch.object(runner.requests, "get",
                       return_value=_mock_response(200, {"results": [hit]})):
        cases = runner.cl_search_retaliation_by_state("VV-cases")

    test("cases found when CL returns a matching hit", len(cases) == 1, cases)
    test("flag is False when cases were found",
         runner._LAST_SEARCH_NETWORK_FAILURE.get("VV-cases") is False)


# ══════════════════════════════════════════════════════════════════════════════
# get_units() — sentinel unit tagging
# ══════════════════════════════════════════════════════════════════════════════

def test_get_units_tags_sentinel_with_network_failure():
    runner._LAST_SEARCH_NETWORK_FAILURE["VV"] = True
    with patch.object(protocol, "load_draft_cases", return_value=[]):
        units = protocol.get_units(["VV"], fresh=True)

    test("sentinel unit created for state with no cases", len(units) == 1)
    test("sentinel unit case_data is None", units[0]["case_data"] is None)
    test("sentinel unit tagged search_network_failure=True",
         units[0]["search_network_failure"] is True)


def test_get_units_tags_sentinel_genuine_no_candidates():
    runner._LAST_SEARCH_NETWORK_FAILURE["UU"] = False
    with patch.object(protocol, "load_draft_cases", return_value=[]):
        units = protocol.get_units(["UU"], fresh=True)

    test("sentinel unit tagged search_network_failure=False for genuine gap",
         units[0]["search_network_failure"] is False)


def test_get_units_defaults_to_false_when_flag_never_set():
    """Non-fresh runs (no CL search attempted) must not be mislabeled either."""
    runner._LAST_SEARCH_NETWORK_FAILURE.pop("TT", None)
    with patch.object(protocol, "load_draft_cases", return_value=[]):
        units = protocol.get_units(["TT"], fresh=False)

    test("sentinel unit defaults search_network_failure=False when unset",
         units[0]["search_network_failure"] is False)


# ══════════════════════════════════════════════════════════════════════════════
# run_unit() — the actual disposition_note text + routing byte-identity
# ══════════════════════════════════════════════════════════════════════════════

_GENUINE_NOTE = "No candidate cases in draft file for this state."
_NETWORK_NOTE = ("search-network-failure: CourtListener unreachable after full "
                  "backoff ladder — not a coverage determination")


def test_run_unit_network_failure_gets_distinct_note():
    unit = {
        "unit_id": "SS::__no_cases__",
        "state": "SS",
        "case_name": "__no_cases__",
        "case_data": None,
        "search_network_failure": True,
    }
    result = protocol.run_unit(unit)

    test("network-failure disposition_note matches suggested text exactly",
         result["disposition_note"] == _NETWORK_NOTE, result["disposition_note"])
    test("network-failure note is distinct from the genuine no-candidates note",
         result["disposition_note"] != _GENUINE_NOTE)
    test("network-failure disposition unchanged (permanent-failure)",
         result["disposition"] == "permanent-failure")
    test("network-failure queue_routing unchanged (None)",
         result["queue_routing"] is None)


def test_run_unit_genuine_no_candidates_note_unchanged():
    """Byte-identical to the pre-fix text — this is the regression guard."""
    unit = {
        "unit_id": "RR::__no_cases__",
        "state": "RR",
        "case_name": "__no_cases__",
        "case_data": None,
        "search_network_failure": False,
    }
    result = protocol.run_unit(unit)

    test("genuine no-candidates disposition_note is byte-identical to before the fix",
         result["disposition_note"] == _GENUINE_NOTE, result["disposition_note"])
    test("genuine no-candidates disposition unchanged (permanent-failure)",
         result["disposition"] == "permanent-failure")
    test("genuine no-candidates queue_routing unchanged (None)",
         result["queue_routing"] is None)


def test_run_unit_missing_flag_defaults_to_genuine_note():
    """Sentinel units built before this fix (no key at all) must not break."""
    unit = {
        "unit_id": "QQ::__no_cases__",
        "state": "QQ",
        "case_name": "__no_cases__",
        "case_data": None,
    }
    result = protocol.run_unit(unit)

    test("missing search_network_failure key defaults to the genuine note",
         result["disposition_note"] == _GENUINE_NOTE, result["disposition_note"])


# ── Runner ──────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("retaliation_holdings_v3 disposition_note — Regression Test Suite (Item 11)")
    print("=" * 60)
    print()

    print("_run_search / cl_search_retaliation_by_state — network-failure tracking")
    test_network_failure_flagged_after_full_backoff_ladder()
    test_genuine_empty_result_not_flagged_as_network_failure()
    test_recovery_after_transient_network_errors_clears_flag()
    test_non_connection_exception_also_flagged_not_a_coverage_determination()
    test_cases_found_always_clears_the_flag()
    print()

    print("get_units() — sentinel unit tagging")
    test_get_units_tags_sentinel_with_network_failure()
    test_get_units_tags_sentinel_genuine_no_candidates()
    test_get_units_defaults_to_false_when_flag_never_set()
    print()

    print("run_unit() — disposition_note text + routing byte-identity")
    test_run_unit_network_failure_gets_distinct_note()
    test_run_unit_genuine_no_candidates_note_unchanged()
    test_run_unit_missing_flag_defaults_to_genuine_note()
    print()

    print("=" * 60)
    print(f"Results: {len(_PASS)}/{len(_PASS) + len(_FAIL)} passed, {len(_FAIL)} failed")
    print("=" * 60)
    if _FAIL:
        print("\nRED: fix before queueing.")
        return 1
    print("\nAll tests pass. Routing verified byte-identical. Safe to queue.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
