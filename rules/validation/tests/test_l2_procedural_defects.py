#!/usr/bin/env python3
"""
Regression tests for l2_procedural_defects_runner.py

Every bug caught in the 2026-06-24 smoke-test iterations is a test case here.
These tests are mock-based and run entirely in the sandbox — no API calls, no
Terminal needed. Run with:

  python3 -m pytest rules/validation/tests/test_l2_procedural_defects.py -v
  # or without pytest:
  python3 rules/validation/tests/test_l2_procedural_defects.py

GREEN: all tests pass → runner is safe to queue overnight.
RED: any failure → fix before queueing.

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import sys
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the l2 directory to path
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "rules" / "validation" / "l2"))

# ── Import the module under test ──────────────────────────────────────────────
from l2_procedural_defects_runner import (
    citations_equivalent,
    is_more_specific,
    query_model,
    classify_unit,
    update_file,
    IMPROVE_TARGETS,
)

# ── Test harness ──────────────────────────────────────────────────────────────

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
# BUG 1 (2026-06-24): citations_equivalent — false MODEL-SPLIT on abbreviations
# Fix: section-number match added so "Tex. R. Civ. P. 510.4(b)-(c)" ≡
#      "Texas Rule of Civil Procedure 510.4" because both contain "510.4".
# ══════════════════════════════════════════════════════════════════════════════

def test_citations_equivalent():
    print("\ncitations_equivalent — section-number match (Bug 1 regression)")

    # True matches — different abbreviations, same section
    test("TX summons abbreviation vs full name",
         citations_equivalent("Tex. R. Civ. P. 510.4(b)-(c)",
                              "Texas Rule of Civil Procedure 510.4"))

    test("NY summons abbreviated vs spelled out",
         citations_equivalent("N.Y. Real Prop. Acts. Law § 735",
                              "New York Real Property Actions and Proceedings Law § 735"))

    test("CA summons abbreviated vs full",
         citations_equivalent("CCP § 415.45",
                              "California Code of Civil Procedure § 415.45"))

    test("Exact match",
         citations_equivalent("CCP § 1161", "CCP § 1161"))

    test("High token overlap (≥70%)",
         citations_equivalent("Texas Rules of Civil Procedure 510.4(b)-(c)",
                              "Texas Rules of Civil Procedure 510.4(b)"))

    # True splits — genuinely different statutes
    test("Different section numbers → SPLIT",
         not citations_equivalent("CCP § 1161", "CCP § 415.45"),
         "1161 ≠ 415.45")

    test("Different codes, same approximate number → SPLIT",
         not citations_equivalent("Tex. Prop. Code § 24.005", "Tex. R. Civ. P. 510.4"),
         "24.005 ≠ 510.4")

    test("Empty vs non-empty → SPLIT",
         not citations_equivalent("", "CCP § 1161"))

    test("Both empty → SPLIT",
         not citations_equivalent("", ""))


# ══════════════════════════════════════════════════════════════════════════════
# BUG 2 (2026-06-24): query_model called model_fn(SYSTEM_PROMPT, prompt)
# with two args; call_openai/call_gemini take one arg.
# Fix: model_fn(prompt) only; return already-parsed dict.
# ══════════════════════════════════════════════════════════════════════════════

def test_query_model_signature():
    print("\nquery_model — single-arg signature + dict return (Bug 2 regression)")

    # Mock that records call args and returns a valid parsed dict
    calls = []
    def mock_model(prompt):
        calls.append(prompt)
        return {"statute": "Mock § 100", "confidence": "high", "_raw": '{"statute":"Mock § 100"}'}

    result = query_model(mock_model, "Test prompt", state="CA", defect="test")

    test("model_fn called with exactly one arg",
         len(calls) == 1 and calls[0] == "Test prompt",
         f"calls={calls}")

    test("result has 'parsed' key",
         "parsed" in result)

    test("parsed contains statute from model",
         result.get("parsed", {}).get("statute") == "Mock § 100")

    test("no error on valid response",
         result.get("error") is None)


def test_query_model_error_handling():
    print("\nquery_model — error detection")

    # Model returns error dict (as call_openai/_error_result does)
    def mock_error_model(prompt):
        return {"error": "Connection error.", "statute": None, "_raw": ""}

    result = query_model(mock_error_model, "Test prompt")

    test("error detected from result dict",
         result.get("error") == "Connection error.")

    test("parsed is None on error",
         result.get("parsed") is None)


def test_query_model_empty_raw():
    print("\nquery_model — empty _raw triggers retry (Bug 4 regression)")

    call_count = [0]
    def mock_empty_then_valid(prompt):
        call_count[0] += 1
        if call_count[0] == 1:
            # First call: empty response (reasoning model stall)
            return {"statute": "", "_raw": ""}
        # Second call: valid response
        return {"statute": "Real § 42", "confidence": "high", "_raw": '{"statute":"Real § 42"}'}

    # Patch time.sleep so tests run fast
    with patch("l2_procedural_defects_runner.time.sleep"):
        result = query_model(mock_empty_then_valid, "Test prompt")

    test("retried on empty _raw",
         call_count[0] == 2,
         f"call_count={call_count[0]}")

    test("second call result used",
         result.get("parsed", {}).get("statute") == "Real § 42")


# ══════════════════════════════════════════════════════════════════════════════
# BUG 3 (2026-06-24): GPT empty response discarded Gemini's valid answer as ERROR
# Fix: SM-GEMINI / SM-GPT classification preserves surviving model's answer.
# ══════════════════════════════════════════════════════════════════════════════

def test_classify_unit_sm_gemini():
    print("\nclassify_unit — SM-GEMINI when GPT empty, Gemini has answer (Bug 3 regression)")

    gpt_empty = {"raw": "", "parsed": {"statute": "", "_raw": ""}, "error": None}
    gem_valid = {"raw": '{"statute":"RPAPL § 735"}',
                 "parsed": {"statute": "RPAPL § 735", "confidence": "high", "_raw": ""},
                 "error": None}

    cl = classify_unit("NY", "summons_improperly_issued_or_served",
                       "RPAPL §701 et seq.", gpt_empty, gem_valid)

    test("classified as SM-GEMINI (not ERROR)",
         cl["classification"] == "SM-GEMINI",
         f"got {cl['classification']}")

    test("recommended_statute is Gemini's answer",
         cl["recommended_statute"] == "RPAPL § 735")

    test("note mentions GPT empty",
         "GPT" in cl.get("note", "") and "empty" in cl.get("note", "").lower())


def test_classify_unit_sm_gpt():
    print("\nclassify_unit — SM-GPT when Gemini empty, GPT has answer")

    gpt_valid = {"raw": '{"statute":"CCP § 1167(a)"}',
                 "parsed": {"statute": "CCP § 1167(a)", "confidence": "high", "_raw": ""},
                 "error": None}
    gem_empty = {"raw": "", "parsed": {"statute": "", "_raw": ""}, "error": None}

    cl = classify_unit("CA", "summons_improperly_issued_or_served",
                       "CCP §1161 et seq.", gpt_valid, gem_empty)

    test("classified as SM-GPT (not ERROR)",
         cl["classification"] == "SM-GPT",
         f"got {cl['classification']}")

    test("recommended_statute is GPT's answer",
         cl["recommended_statute"] == "CCP § 1167(a)")


def test_classify_unit_both_empty_is_error():
    print("\nclassify_unit — both empty → ERROR (not SM)")

    both_empty = {"raw": "", "parsed": {"statute": "", "_raw": ""}, "error": None}

    cl = classify_unit("CA", "failure_to_attach_lease_or_notice_to_complaint",
                       "CCP §1161 et seq.", both_empty, both_empty)

    test("both empty → ERROR",
         cl["classification"] == "ERROR",
         f"got {cl['classification']}")


# ══════════════════════════════════════════════════════════════════════════════
# NO-SPECIFIC-RULE branch for attachment defect
# ══════════════════════════════════════════════════════════════════════════════

def test_classify_unit_no_specific_rule():
    print("\nclassify_unit — NO-SPECIFIC-RULE for attach when both models say attachment_required=false")

    gpt_no = {"raw": '{"attachment_required":false,"statute":null}',
              "parsed": {"attachment_required": False, "statute": None, "_raw": ""},
              "error": None}
    gem_no = {"raw": '{"attachment_required":false,"statute":null}',
              "parsed": {"attachment_required": False, "statute": None, "_raw": ""},
              "error": None}

    cl = classify_unit("TX", "failure_to_attach_lease_or_notice_to_complaint",
                       "Tex. Prop. Code §24.001 et seq.", gpt_no, gem_no)

    test("both attachment_required=false → NO-SPECIFIC-RULE",
         cl["classification"] == "NO-SPECIFIC-RULE",
         f"got {cl['classification']}")


# ══════════════════════════════════════════════════════════════════════════════
# update_file — SM-GEMINI writes l2_sm_statute, does not overwrite statute
# ══════════════════════════════════════════════════════════════════════════════

def test_update_file_sm_gemini():
    print("\nupdate_file — SM-GEMINI preserves sm_statute without overwriting statute")

    # Build a minimal state file
    state_data = {
        "state": "NY",
        "procedural_defects": [
            {
                "defect": "summons_improperly_issued_or_served",
                "statute": "RPAPL §701 et seq.; state civil procedure rules (service of process)",
                "consequence": "Motion to quash summons."
            }
        ],
        "last_updated": "2026-06-24"
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(state_data, f, indent=2)
        tmp_path = Path(f.name)

    try:
        from l2_procedural_defects_runner import update_file
        update_file(
            tmp_path, "NY", "summons_improperly_issued_or_served",
            "SM-GEMINI", "RPAPL § 735",
            "GPT empty; Gemini single-model: RPAPL § 735", dry_run=False
        )

        with open(tmp_path) as f:
            updated = json.load(f)

        defect = updated["procedural_defects"][0]

        test("original statute not overwritten",
             defect["statute"] == "RPAPL §701 et seq.; state civil procedure rules (service of process)",
             f"statute={defect.get('statute')}")

        test("l2_sm_statute written with Gemini's answer",
             defect.get("l2_sm_statute") == "RPAPL § 735",
             f"l2_sm_statute={defect.get('l2_sm_statute')}")

        test("L2-PROCEDURAL-SM-GEMINI flag added",
             "L2-PROCEDURAL-SM-GEMINI" in defect.get("validation_flags", []))

        test("l2_run_date written",
             "l2_run_date" in defect)

    finally:
        tmp_path.unlink(missing_ok=True)


# ══════════════════════════════════════════════════════════════════════════════
# CONSENSUS-IMPROVE: improves statute, adds flag
# ══════════════════════════════════════════════════════════════════════════════

def test_update_file_consensus_improve():
    print("\nupdate_file — CONSENSUS-IMPROVE updates statute field")

    state_data = {
        "state": "NY",
        "procedural_defects": [
            {
                "defect": "summons_improperly_issued_or_served",
                "statute": "RPAPL §701 et seq.; state civil procedure rules (service of process)",
                "consequence": "Motion to quash."
            }
        ]
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(state_data, f, indent=2)
        tmp_path = Path(f.name)

    try:
        update_file(
            tmp_path, "NY", "summons_improperly_issued_or_served",
            "CONSENSUS-IMPROVE", "N.Y. Real Prop. Acts. Law (RPAPL) § 735",
            "Both models agree on more specific citation.", dry_run=False
        )

        with open(tmp_path) as f:
            updated = json.load(f)

        defect = updated["procedural_defects"][0]

        test("statute updated to specific citation",
             "§ 735" in defect.get("statute", ""),
             f"statute={defect.get('statute')}")

        test("L2-PROCEDURAL-IMPROVED flag added",
             "L2-PROCEDURAL-IMPROVED" in defect.get("validation_flags", []))

    finally:
        tmp_path.unlink(missing_ok=True)


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("l2_procedural_defects_runner — Regression Test Suite")
    print("=" * 60)

    test_citations_equivalent()
    test_query_model_signature()
    test_query_model_error_handling()
    test_query_model_empty_raw()
    test_classify_unit_sm_gemini()
    test_classify_unit_sm_gpt()
    test_classify_unit_both_empty_is_error()
    test_classify_unit_no_specific_rule()
    test_update_file_sm_gemini()
    test_update_file_consensus_improve()

    print()
    print("=" * 60)
    total = len(_PASS) + len(_FAIL)
    print(f"Results: {len(_PASS)}/{total} passed, {len(_FAIL)} failed")
    if _FAIL:
        print(f"\nFAILED:")
        for name in _FAIL:
            print(f"  ✗  {name}")
        print("\nFix failures before queueing overnight run.")
        sys.exit(1)
    else:
        print("\nAll tests pass. Safe to queue overnight run.")
    print("=" * 60)


if __name__ == "__main__":
    main()
