#!/usr/bin/env python3
"""
Protocol Adapter — retaliation_holdings_v3 (Generate-From-Source)
=================================================================
Wraps rules/validation/l2/retaliation_holdings_v3_runner.py for use
with the shared ValidationHarness. Handles:

  - Unit enumeration: (state × case) pairs from draft files
  - GPT-empty retry: trimmed input on first retry; Claude-haiku fallback
    if GPT still fails (Claude ≠ Gemini, satisfies independence rule)
  - TransientError on CL quota exhaustion (all CL retries depleted)
  - Provenance annotation: which model actually verified per case

Independence constraint (from direction): the model that GENERATES the
holding and the model that VERIFIES it MUST be different. This adapter
uses Gemini (generate) → GPT-4o (verify) → Claude-haiku (fallback verify).
Claude-haiku satisfies independence vs. Gemini. GPT and Claude-haiku are
never used as generators.

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

from __future__ import annotations

import hashlib
import sys
import time
from pathlib import Path

# Pull in the v3 runner (safe — runner has if __name__ == "__main__" guard)
_L2_DIR = Path(__file__).parent.parent / "l2"
sys.path.insert(0, str(_L2_DIR))

from retaliation_holdings_v3_runner import (  # noqa: E402
    CONSENSUS_STATES,
    GENERATE_MODEL_NAME,
    VERIFY_MODEL_NAME,
    VERIFY_PROMPT,
    call_gpt,
    call_gemini,
    check_a_existence,
    check_b_currency,
    check_c_generate_from_source,
    check_d_from_c,
    cl_get_opinion_text,
    load_draft_cases,
)

# Harness exception types
sys.path.insert(0, str(Path(__file__).parent.parent))
from harness import TransientError, PermanentError, call_claude_fallback  # noqa: E402

PROTOCOL_NAME = "retaliation_holdings_v3"

# ---------------------------------------------------------------------------
# Unit enumeration
# ---------------------------------------------------------------------------

def get_units(states: list[str]) -> list[dict]:
    """Return one unit dict per (state, case) pair."""
    units = []
    for state in states:
        cases = load_draft_cases(state)
        if not cases:
            # Still create a sentinel unit so the harness logs the skip
            units.append({
                "unit_id": f"{state}::__no_cases__",
                "state": state,
                "case_name": "__no_cases__",
                "case_data": None,
            })
            continue
        for case in cases:
            cname = case.get("case_name", "unknown")
            uid = hashlib.md5(f"{state}::{cname}".encode()).hexdigest()[:12]
            units.append({
                "unit_id": uid,
                "state": state,
                "case_name": cname,
                "case_data": case,
            })
    return units


# ---------------------------------------------------------------------------
# GPT-empty fallback: retry trimmed → Claude-haiku
# ---------------------------------------------------------------------------

def _verify_with_fallback(ver_prompt: str, gen_holding: str, gen_quote: str | None,
                          opinion_text: str, prior_holding: str) -> tuple[dict, str]:
    """
    Try GPT-4o to verify. If empty/error:
      1. Retry with trimmed opinion text (first 3000 chars).
      2. Fallback to Claude-haiku (different provider from Gemini generator).
    Returns (verify_response_dict, actual_verify_model_name).
    """
    # Attempt 1: GPT full
    ver_resp = call_gpt(ver_prompt, max_tokens=1000)
    if isinstance(ver_resp, dict) and "error" not in ver_resp:
        return ver_resp, VERIFY_MODEL_NAME

    # Attempt 2: GPT trimmed (3000 chars)
    trimmed_text = opinion_text[:3000]
    quote_display = f'"{gen_quote}"' if gen_quote else "none provided"
    trimmed_prompt = VERIFY_PROMPT.format(
        opinion_text=trimmed_text,
        holding_characterization=gen_holding,
        candidate_quote_display=quote_display,
        draft_holding=prior_holding or "(no draft holding available)",
    )
    ver_resp = call_gpt(trimmed_prompt, max_tokens=800)
    if isinstance(ver_resp, dict) and "error" not in ver_resp:
        return ver_resp, f"{VERIFY_MODEL_NAME}:trimmed"

    # Attempt 3: Claude-haiku fallback (different provider, satisfies independence)
    ver_resp = call_claude_fallback(trimmed_prompt, max_tokens=800)
    if isinstance(ver_resp, dict) and "error" not in ver_resp:
        return ver_resp, "claude:claude-haiku-4-5-20251001"

    # All attempts failed
    return {"error": "all verify attempts failed"}, "none"


# ---------------------------------------------------------------------------
# Core unit runner (called by harness via run_with_retry)
# ---------------------------------------------------------------------------

def run_unit(unit: dict) -> dict:
    """
    Process one (state, case) unit. Returns a result dict compatible with
    harness provenance enforcement.

    Raises TransientError if CourtListener quota appears exhausted
    (all CL retries failed with 429 → harness will sleep + retry the unit).
    Raises PermanentError only on structural issues that retrying won't fix.
    """
    state     = unit["state"]
    case_data = unit.get("case_data")
    case_name = unit.get("case_name", "")

    # Sentinel: no cases for this state
    if case_data is None:
        return {
            "unit_id": unit["unit_id"],
            "state": state,
            "case_name": case_name,
            "disposition": "permanent-failure",
            "disposition_note": "No candidate cases in draft file for this state.",
            "queue_routing": None,
            "provenance": {
                "generate_model": None,
                "verify_model": None,
                "verify_actually_answered": False,
            },
        }

    prior_holding = case_data.get("holding_gpt") or case_data.get("holding_gemini") or ""
    citation_gpt  = case_data.get("citation_gpt")
    citation_gem  = case_data.get("citation_gemini")
    year          = case_data.get("year")

    # ---- Check A: existence + citation ----
    check_a = check_a_existence(case_name, citation_gpt, citation_gem, year)
    time.sleep(10)

    # Detect CL quota exhaustion: exists=FLAG with "429" in basis
    if check_a.get("exists") == "FLAG":
        basis = check_a.get("basis") or ""
        if "429" in basis or "quota" in basis.lower() or "error" in basis.lower():
            raise TransientError(f"CL quota/network error on Check A for {case_name}: {basis[:120]}")

    # ---- Fetch opinion text ----
    opinion_text = None
    opinion_text_source = None
    cl_opinion_id = check_a.get("cl_opinion_id")
    if cl_opinion_id:
        opinion_text = cl_get_opinion_text(cl_opinion_id)
        if opinion_text:
            opinion_text_source = f"CL opinion/{cl_opinion_id} full text"
        time.sleep(5)
    if not opinion_text:
        snippets = check_a.get("cl_snippets")
        if snippets:
            opinion_text = snippets
            opinion_text_source = "CL search snippet (abbreviated)"

    # ---- Check B: currency ----
    check_b = check_b_currency(check_a.get("cl_cluster_id"))
    time.sleep(5)

    # ---- Check C: generate (Gemini) → verify with fallback ----
    # We override Check C here to use the fallback-aware verify.
    # If opinion text is short, call standard generate-from-source which
    # handles FLAG-no-text correctly.
    if not opinion_text or len(opinion_text.strip()) < 200:
        check_c = {
            "check": "C_generate_from_source",
            "generate_model": GENERATE_MODEL_NAME,
            "verify_model": VERIFY_MODEL_NAME,
            "holding": "FLAG-no-text",
            "source_generated_holding": None,
            "controlling_quote": None,
            "quote_verified_verbatim": None,
            "draft_agreement": None,
            "generate_output": None,
            "verify_output": None,
            "queue_routing": "PR",
            "pr_reason": "opinion-text-unavailable",
            "basis": "Opinion text unavailable — CL did not return retrievable text.",
        }
        actual_verify_model = "none"
        verify_actually_answered = False
    else:
        # Step 1: Generate (Gemini) — reuse standard function
        from retaliation_holdings_v3_runner import GENERATE_PROMPT  # noqa
        text_excerpt = opinion_text[:8000]
        gen_prompt = GENERATE_PROMPT.format(opinion_text=text_excerpt)
        gen_resp = call_gemini(gen_prompt, max_tokens=1000)

        if isinstance(gen_resp, dict) and "error" not in gen_resp and gen_resp.get("addresses_retaliation_defense"):
            gen_holding = gen_resp.get("holding_characterization") or ""
            gen_quote   = gen_resp.get("candidate_quote")

            # Step 2: Verify with fallback-aware caller
            quote_display = f'"{gen_quote}"' if gen_quote else "none provided"
            ver_prompt = VERIFY_PROMPT.format(
                opinion_text=text_excerpt,
                holding_characterization=gen_holding,
                candidate_quote_display=quote_display,
                draft_holding=prior_holding or "(no draft holding available)",
            )
            ver_resp, actual_verify_model = _verify_with_fallback(
                ver_prompt, gen_holding, gen_quote, opinion_text, prior_holding
            )
            verify_actually_answered = actual_verify_model != "none"

            # Rebuild check_c from these outputs
            ver_accuracy = ver_resp.get("text_supports_characterization") if verify_actually_answered else None
            ver_verbatim = ver_resp.get("quote_is_verbatim")
            ver_onpoint  = ver_resp.get("quote_is_on_point")
            ver_altquote = ver_resp.get("alternative_quote")
            draft_agree  = ver_resp.get("draft_agreement")

            if gen_quote and ver_verbatim is True and ver_onpoint is True:
                controlling_quote = gen_quote
                qvv = True
            elif ver_altquote:
                controlling_quote = ver_altquote
                qvv = "gpt-alternative"
            else:
                controlling_quote = None
                qvv = False

            if verify_actually_answered and ver_accuracy in ("accurate", "partially_accurate"):
                c_holding = "corroborated"
                c_queue   = None
                c_basis   = (f"Gemini generated: '{gen_holding[:80]}'. "
                             f"{actual_verify_model} verified as '{ver_accuracy}'. "
                             f"Draft agreement: {draft_agree}.")
            elif not verify_actually_answered:
                c_holding = "FLAG-verify-failed"
                c_queue   = "RC"
                c_basis   = "All verify attempts (GPT, GPT-trimmed, Claude) failed."
            else:
                c_holding = "FLAG-verify-disputed"
                c_queue   = "RC"
                c_basis   = (f"{actual_verify_model} found characterization '{ver_accuracy}'. "
                             f"Note: {str(ver_resp.get('verification_note',''))[:100]}")

            check_c = {
                "check": "C_generate_from_source",
                "generate_model": GENERATE_MODEL_NAME,
                "verify_model": actual_verify_model,
                "holding": c_holding,
                "source_generated_holding": gen_holding,
                "controlling_quote": controlling_quote,
                "quote_verified_verbatim": qvv,
                "draft_agreement": draft_agree,
                "generate_output": gen_resp,
                "verify_output": ver_resp,
                "queue_routing": c_queue,
                "basis": c_basis,
            }
        else:
            # Gemini generate failed or said not-relevant
            actual_verify_model = "none"
            verify_actually_answered = False
            if isinstance(gen_resp, dict) and "error" in gen_resp:
                c_holding = "FLAG-generate-failed"
                c_basis   = f"Gemini generate failed: {gen_resp['error']}"
            else:
                c_holding = "FLAG-irrelevant"
                c_basis   = f"Gemini: case does not address retaliation. About: {(gen_resp or {}).get('what_opinion_is_about','?')[:100]}"
            check_c = {
                "check": "C_generate_from_source",
                "generate_model": GENERATE_MODEL_NAME,
                "verify_model": actual_verify_model,
                "holding": c_holding,
                "source_generated_holding": None,
                "controlling_quote": None,
                "quote_verified_verbatim": None,
                "draft_agreement": None,
                "generate_output": gen_resp,
                "verify_output": None,
                # PR: wrong/unrelated document retrieved. RC: generate API failure (text was present).
                "queue_routing": "PR" if c_holding == "FLAG-irrelevant" else "RC",
                "pr_reason": "case-not-relevant-to-retaliation-likely-wrong-doc" if c_holding == "FLAG-irrelevant" else None,
                "basis": c_basis,
            }

    # ---- Check D: derived from C ----
    check_d = check_d_from_c(check_c)

    # ---- Disposition + Bucket (v3 reporting direction 2026-06-23) ----
    # Two rates: method_rate = MV÷(MV+CI+RC), overall_rate = MV÷all.
    # PR = retrieval failure — NOT a verification failure, never attorney lane.
    # Buckets: MV, CI, RC, PR, SM (SM set by harness enforce_provenance).
    a_ok = check_a.get("exists") in ("true",)
    b_ok = check_b.get("currency") == "OK-machine"
    c_ok = check_c.get("holding") == "corroborated"
    d_ok = check_d.get("control") in ("STATED", "STATED-single-model", "INFERRED")

    # PR detection: was opinion text actually retrieved and usable?
    text_retrieved = bool(opinion_text and len(opinion_text.strip()) >= 200)
    citation_mismatch = (check_a.get("exists") == "FLAG-citation-mismatch")
    c_holding_val = check_c.get("holding", "")
    is_pr = (
        citation_mismatch
        or c_holding_val == "FLAG-no-text"
        or not text_retrieved
        or c_holding_val == "FLAG-irrelevant"  # CL returned wrong/unrelated document
    )

    pr_reason: str | None = None

    if is_pr:
        bucket = "PR"
        queue  = "PR"
        if citation_mismatch:
            pr_reason = "citation-mismatch"
        elif not text_retrieved or c_holding_val == "FLAG-no-text":
            pr_reason = "opinion-text-unavailable"
        else:
            pr_reason = "case-not-relevant-to-retaliation-likely-wrong-doc"
        # Inherit pr_reason from check_c if already set there
        pr_reason = check_c.get("pr_reason") or pr_reason
        disposition = "pending-retrieval"
        dispo_note  = f"PR: {pr_reason}. Quarantined for retrieval retry. Not attorney lane."
    elif a_ok and b_ok and c_ok and check_d.get("control") == "INFERRED":
        bucket = "CI"
        queue  = "CI"
        disposition = "needs-attorney"
        dispo_note  = (f"CI: text retrieved, two-model corroborated, D=INFERRED "
                       f"(no controlling quote). Cheap confirm lane.")
    elif a_ok and b_ok and c_ok and d_ok:
        bucket = "MV"
        queue  = None
        disposition = "machine-verified"
        dispo_note  = (f"MV: A=true B=OK-machine C=corroborated D={check_d['control']}. "
                       f"Below attorney line.")
    else:
        # Text was retrieved but holding failed verification → genuine defect
        bucket = "RC"
        queue  = check_c.get("queue_routing") or "RC"
        failed = []
        if not a_ok: failed.append(f"A={check_a.get('exists')}")
        if not b_ok: failed.append(f"B={check_b.get('currency')}")
        if not c_ok: failed.append(f"C={check_c.get('holding')}")
        if not d_ok: failed.append(f"D={check_d.get('control')}")
        disposition = "needs-attorney"
        dispo_note  = (f"RC: text retrieved, holding failed verification. "
                       f"Flagged: {', '.join(failed)}. Source-generated holding → attorney.")

    return {
        "unit_id": unit["unit_id"],
        "state": state,
        "case_name": case_name,
        "citation_gpt": citation_gpt,
        "citation_gemini": citation_gem,
        "year": year,
        "prior_holding": prior_holding,
        "source_generated_holding": check_c.get("source_generated_holding"),
        "check_a": check_a,
        "check_b": check_b,
        "check_c": check_c,
        "check_d": check_d,
        "disposition": disposition,
        "disposition_note": dispo_note,
        "bucket": bucket,                   # MV | CI | RC | PR | SM (SM set by harness)
        "pr_reason": pr_reason,             # set for PR cases; None otherwise
        "controlling_quote": check_d.get("controlling_quote"),
        "queue_routing": queue,             # MV→None, CI→"CI", RC→"RC", PR→"PR"
        "provenance": {
            "generate_model": GENERATE_MODEL_NAME,
            "verify_model": check_c.get("verify_model") or "none",
            "verify_actually_answered": verify_actually_answered if "verify_actually_answered" in dir() else False,
            "opinion_text_source": opinion_text_source,
            "draft_agreement": check_c.get("draft_agreement"),
            "text_retrieved": text_retrieved,
            "harness_version": "v1",
        },
    }
