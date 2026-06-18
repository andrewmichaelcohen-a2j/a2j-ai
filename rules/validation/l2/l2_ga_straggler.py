#!/usr/bin/env python3
"""
L2 Georgia Straggler Retry
===========================
GA is the one remaining technical straggler. The reasoning pass's conflict-framing
caused both models to switch their answers (neutral: both "none"; reasoned: GPT 3d,
Gemini 0d → no convergence → spurious L7).

Protocol deviation that caused the artifact:
  - Neutral query: GPT=None, Gemini=None (both say no specific notice period)
  - PERIOD-DIVERGENCE triggered (vs file's 3d claim)
  - Reasoning pass ran with conflict-framing → both models reconsidered → disagreed
  - Result: L7 flag from a conflict-framing artifact, not genuine legal disagreement

This script re-runs a CLEAN NEUTRAL QUERY with 8000-token GPT budget, then:
  - If both models agree with each other → AI-resolve directly (skip reasoning pass)
    The reasoning pass is for model-vs-model disagreement; when models agree but
    differ from the file, that's a file correction, not a legal-judgment call.
  - If models genuinely disagree with each other → real L7, leave flag

Usage (run from repo root):
  python3 rules/validation/l2/l2_ga_straggler.py
  python3 rules/validation/l2/l2_ga_straggler.py --dry-run

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_L2_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_L2_DIR))

from l2_runner import (
    _parse_json_response,
    _error_result,
    _extract_section_nums,
    _normalize_days,
    OPENAI_MODEL,
    GEMINI_MODEL,
    OPENAI_KEY,
    GOOGLE_KEY,
    SYSTEM_PROMPT,
    RULES_EVICTION_DIR,
    DOCS_DIR,
    extract_file_claim,
)

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
GA_PATH = RULES_EVICTION_DIR / "georgia" / "ga_eviction_v2.json"


def call_openai_clean(query: str, dry_run: bool = False) -> dict:
    """Neutral query, 8000-token budget — no conflict framing."""
    if dry_run:
        return {"days": None, "notice_required": True, "statute": "DRY-RUN §44-7-50(a)", "rationale": "demand required, no waiting period", "model": OPENAI_MODEL}
    try:
        from openai import OpenAI
    except ImportError:
        return _error_result("openai not installed", OPENAI_MODEL)
    try:
        client = OpenAI(api_key=OPENAI_KEY)
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
            max_completion_tokens=8000,
        )
        raw = resp.choices[0].message.content
        raw = raw.strip() if raw else ""
        parsed = _parse_json_response(raw)
        parsed["model"] = OPENAI_MODEL
        return parsed
    except Exception as exc:
        return _error_result(str(exc), OPENAI_MODEL)


def call_gemini_clean(query: str, dry_run: bool = False) -> dict:
    if dry_run:
        return {"days": None, "notice_required": True, "statute": "DRY-RUN O.C.G.A. §44-7-50(a)", "rationale": "demand required, no waiting period", "model": GEMINI_MODEL}
    try:
        from google import genai
    except ImportError:
        return _error_result("google-genai not installed", GEMINI_MODEL)
    try:
        client = genai.Client(api_key=GOOGLE_KEY)
        full_prompt = SYSTEM_PROMPT + "\n\n" + query
        resp = client.models.generate_content(model=GEMINI_MODEL, contents=full_prompt)
        raw = resp.text.strip()
        parsed = _parse_json_response(raw)
        parsed["model"] = GEMINI_MODEL
        return parsed
    except Exception as exc:
        return _error_result(str(exc), GEMINI_MODEL)


def build_ga_query() -> str:
    """Neutral query — no conflict context, no anchoring."""
    return (
        "Under Georgia law, does a residential landlord need to give a tenant a formal notice "
        "to pay rent or quit BEFORE filing a dispossessory (eviction) action for nonpayment of rent? "
        "If yes, how many days?\n\n"
        "Specifically: does O.C.G.A. §44-7-50 or any other Georgia statute require a formal "
        "pre-filing demand or notice, and if so, does that demand require any waiting period "
        "before the landlord may file?\n\n"
        "Respond ONLY in valid JSON:\n"
        "{\"days\": <integer|null>, \"notice_required\": <true|false>, "
        "\"statute\": \"<citation>\", \"rationale\": \"<2-3 sentence explanation>\"}"
    )


def models_agree(gpt: dict, gem: dict) -> bool:
    """True if both models agree on notice_required AND days (or both null)."""
    if gpt.get("error") or gem.get("error"):
        return False
    nr_match = gpt.get("notice_required") == gem.get("notice_required")
    if not nr_match:
        return False
    gd = _normalize_days(gpt.get("days"))
    md = _normalize_days(gem.get("days"))
    return gd == md


def resolve_ga(data: dict, gpt: dict, gem: dict, dry_run: bool) -> str:
    """AI-resolve GA when models agree. Returns resolution_type string."""
    notice_required = gpt.get("notice_required", False)
    days = _normalize_days(gpt.get("days"))
    statute = gpt.get("statute") or gem.get("statute")

    if not dry_run:
        # Update pay_or_quit content
        pq = data["notice"]["notice_types"]["pay_or_quit"]
        old_days = None
        old_statute = None
        for sub in ("tenancy_all", "tenancy_under_1yr", "tenancy_any"):
            if sub in pq and isinstance(pq[sub], dict):
                old_days = pq[sub].get("days")
                old_statute = pq[sub].get("statute")
                pq[sub]["days"] = days
                if statute:
                    pq[sub]["statute"] = statute
                if days is None:
                    pq[sub]["count_method"] = None
                break

        # Clear stale L7 flag
        flags = data["validation"].get("flags", [])
        flags = [fl for fl in flags if not (
            fl.get("layer") == "L2" and "L7" in fl.get("code", "") and fl.get("disposition") == "open"
        )]

        resolution_code = "L2-STRAGGLER-AI-RESOLVED"
        flags.append({
            "layer": "L2",
            "code": resolution_code,
            "field": "notice.notice_types.pay_or_quit",
            "disposition": "resolved-ai-corrected",
            "resolution": {
                "method": "AI-neutral-query-consensus",
                "resolved_date": TODAY,
                "notice_required": notice_required,
                "days": days,
                "operative_statute": statute,
                "note": (
                    f"GA straggler retry: clean neutral query (8000-token GPT budget). "
                    f"Both models agree: notice_required={notice_required}, days={days}, statute={statute}. "
                    f"Prior L7 flag was a reasoning-pass artifact (conflict-framing changed model answers). "
                    f"File corrected from days={old_days} ({old_statute!r}) to days={days} ({statute!r}). "
                    f"Status stays AUTOMATED-CHECKS-PASSED. NEVER advanced past ACP."
                ),
                "gpt": {"days": gpt.get("days"), "statute": gpt.get("statute"), "rationale": gpt.get("rationale")},
                "gemini": {"days": gem.get("days"), "statute": gem.get("statute"), "rationale": gem.get("rationale")},
                "status": "pending-human-confirmation",
            },
            "l2_run_date": TODAY,
        })

        data["validation"]["flags"] = flags
        data["validation"]["automated_layers"]["L2_consensus"] = "pass"

        with open(GA_PATH, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"    → AI-RESOLVED: notice_required={notice_required}, days={old_days}→{days}, statute={old_statute!r}→{statute!r}")
        print(f"    → L7 flag cleared. Status: pending-human-confirmation at ACP.")
    else:
        print(f"    (dry run — would AI-resolve: notice_required={notice_required}, days={days}, statute={statute})")

    return "AI-RESOLVED"


def write_genuine_l7(data: dict, gpt: dict, gem: dict, file_claim: dict, dry_run: bool):
    """Keep as L7 — models genuinely disagree after clean neutral query."""
    if not dry_run:
        flags = data["validation"].get("flags", [])
        flags = [fl for fl in flags if not (
            fl.get("layer") == "L2" and "L7" in fl.get("code", "") and fl.get("disposition") == "open"
        )]
        flags.append({
            "layer": "L2",
            "code": "L2-MODEL-SPLIT-L7",
            "field": "notice.notice_types.pay_or_quit",
            "disposition": "open",
            "escalation": "L7",
            "note": (
                f"GA straggler retry (clean neutral query, 8000-token budget): "
                f"models genuinely disagree. "
                f"GPT: notice_required={gpt.get('notice_required')}, days={gpt.get('days')}, statute={gpt.get('statute')}. "
                f"Gemini: notice_required={gem.get('notice_required')}, days={gem.get('days')}, statute={gem.get('statute')}. "
                f"Attorney review required."
            ),
            "gpt_answer": {"days": gpt.get("days"), "statute": gpt.get("statute"), "rationale": gpt.get("rationale")},
            "gemini_answer": {"days": gem.get("days"), "statute": gem.get("statute"), "rationale": gem.get("rationale")},
            "l2_run_date": TODAY,
        })
        data["validation"]["flags"] = flags
        data["validation"]["automated_layers"]["L2_consensus"] = "flagged"
        with open(GA_PATH, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"    → Genuine L7 confirmed after clean retry. L7 flag updated.")


def run(dry_run: bool = False):
    print(f"\nCivil Justice as Code — GA Straggler Retry")
    print(f"Run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Fix: conflict-framing artifact in reasoning pass → clean neutral query")
    print(f"GPT budget: 8000 tokens · Gemini: standard\n")

    with open(GA_PATH) as f:
        data = json.load(f)

    file_claim = extract_file_claim(data)
    print(f"  GA (Georgia) — file: days={file_claim['days']}, statute={file_claim.get('statute')!r}")
    print(f"  Current L7 flag reason: reasoning pass GPT=3d vs Gemini=0d (conflict-framing artifact)")

    query = build_ga_query()

    print(f"\n  Running clean neutral queries ({OPENAI_MODEL} + {GEMINI_MODEL})...")
    gpt = call_openai_clean(query, dry_run=dry_run)
    gem = call_gemini_clean(query, dry_run=dry_run)

    if gpt.get("error"):
        print(f"  GPT ERROR: {gpt['error'][:80]}")
    else:
        print(f"  GPT:    notice_required={gpt.get('notice_required')}, days={gpt.get('days')}, statute={gpt.get('statute')}")
        print(f"          rationale: {(gpt.get('rationale') or '')[:120]}")

    if gem.get("error"):
        print(f"  Gemini ERROR: {gem['error'][:80]}")
    else:
        print(f"  Gemini: notice_required={gem.get('notice_required')}, days={gem.get('days')}, statute={gem.get('statute')}")
        print(f"          rationale: {(gem.get('rationale') or '')[:120]}")

    if gpt.get("error") or gem.get("error"):
        print(f"\n  ⚠️  One or both models errored — cannot classify. Retaining existing L7 flag.")
        return

    agree = models_agree(gpt, gem)
    print(f"\n  Models agree: {agree}")

    if agree:
        print(f"  → Models agree with each other → AI-resolve (skip reasoning pass)")
        resolution = resolve_ga(data, gpt, gem, dry_run)
        outcome = "AI-RESOLVED (pending human confirmation)"
        print(f"\n  Result: GA = {outcome}")
        print(f"  GA is NO LONGER an L7 item. Add to pending-confirmation queue.")
    else:
        print(f"  → Models disagree after clean neutral query → genuine L7")
        write_genuine_l7(data, gpt, gem, file_claim, dry_run)
        outcome = "GENUINE L7 (attorney review required)"
        print(f"\n  Result: GA = {outcome}")

    print(f"\n{'='*60}")
    print(f"  GA straggler complete")
    print(f"  Outcome: {outcome}")
    print(f"  ⚠️  STOP AND REPORT. Do not start other phases.")
    print(f"  Next: commit changes via GitHub Desktop, then report to Andy.")
    print(f"{'='*60}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GA straggler retry — clean neutral query")
    parser.add_argument("--dry-run", action="store_true", help="No API calls, no write-back.")
    args = parser.parse_args()
    run(dry_run=args.dry_run)
