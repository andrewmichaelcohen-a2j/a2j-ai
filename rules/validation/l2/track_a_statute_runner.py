#!/usr/bin/env python3
"""
Track A — Statute-Direct Retaliation Verification
===================================================
For states where CourtListener fresh-search found NO appellate case law
(permanent-failure / __no_cases__) and where statute verification without
CL is appropriate.

Track A states (as of 2026-06-26): KS, NV, NY, SC
  - KS: __no_cases__ in nc17_fresh_v2 (KSA 58-2572)
  - NV: __no_cases__ in nc17_fresh_v2 (NRS 118A.510); Paullin v. Sutton
        was wrong-doc (not about residential retaliation)
  - NY: prior Track B research found no leading Court of Appeals case;
        RPL §223-b is the operative statute
  - SC: no candidates found in nc17_fresh_v2 (SC Code §27-40-910)

What this runner does:
  - Skips CL entirely
  - Asks GPT + Gemini: does this statute protect residential tenants from
    retaliatory eviction, and what is the operative retaliation statute?
  - Classifies as: STATUTE-CONFIRMED, STATUTE-DIVERGENCE, or ERROR
  - Writes result to the state v2 file as a Track-A validation flag
  - Does NOT attempt machine-verified status (no opinion text = no MV)
  - Output is a citation-grade "statute-verified" record for the holdings module

This is below the attorney line. Attorney confirmation required before
any statute can be cited publicly as the authoritative retaliation basis.

Usage:
  python3 rules/validation/l2/track_a_statute_runner.py
  python3 rules/validation/l2/track_a_statute_runner.py --states KS,NV
  python3 rules/validation/l2/track_a_statute_runner.py --dry-run

Output: rules/validation/l2/output/track_a_statute_YYYYMMDD.json
Then: STOP AND REPORT to Cowork for ingestion.

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ── Key handling ───────────────────────────────────────────────────────────────

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv not installed. Run: pip install python-dotenv --break-system-packages")
    sys.exit(1)

_REPO_ROOT = _SCRIPT_DIR.parent.parent.parent
_ENV_PATH = _REPO_ROOT / ".env"

if not _ENV_PATH.exists():
    print(f"ERROR: .env not found at {_ENV_PATH}")
    sys.exit(1)

load_dotenv(_ENV_PATH)

OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")
GOOGLE_KEY = os.environ.get("GOOGLE_API_KEY", "")

if not OPENAI_KEY:
    print("ERROR: OPENAI_API_KEY not set in .env")
    sys.exit(1)
if not GOOGLE_KEY:
    print("ERROR: GOOGLE_API_KEY not set in .env")
    sys.exit(1)

from l2_runner import (
    call_openai,
    call_gemini,
    OPENAI_MODEL,
    GEMINI_MODEL,
    RULES_EVICTION_DIR,
)

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
OUT_DIR = _SCRIPT_DIR / "output"

# ── Track A states ─────────────────────────────────────────────────────────────

TRACK_A_STATES = {
    "KS": {
        "name": "Kansas",
        "statute": "KSA 58-2572",
        "statute_full": "K.S.A. § 58-2572",
        "reason": "__no_cases__ in nc17_fresh_v2 CL fresh search",
    },
    "NV": {
        "name": "Nevada",
        "statute": "NRS 118A.510",
        "statute_full": "Nev. Rev. Stat. § 118A.510",
        "reason": "__no_cases__ in nc17_fresh_v2; Paullin v. Sutton was wrong-doc",
    },
    "NY": {
        "name": "New York",
        "statute": "RPL 223-b",
        "statute_full": "N.Y. Real Property Law § 223-b",
        "reason": "Prior Track B research found no leading Court of Appeals case; statute is operative",
    },
    "SC": {
        "name": "South Carolina",
        "statute": "SC Code 27-40-910",
        "statute_full": "S.C. Code Ann. § 27-40-910",
        "reason": "No candidates found in nc17_fresh_v2 CL fresh search",
    },
}

SYSTEM_PROMPT = (
    "You are a legal research expert in US residential landlord-tenant law. "
    "Answer questions about state statutes governing retaliation by landlords. "
    "Be precise about statute citations. Return only the JSON format requested — "
    "no markdown fences or commentary."
)


def build_query(state_name: str, statute: str, statute_full: str) -> str:
    return (
        f"Under {state_name} law, does {statute_full} protect residential tenants "
        f"against retaliatory eviction by landlords (e.g., eviction in response to "
        f"tenant complaints about habitability, reporting code violations, or organizing "
        f"tenant associations)?\n\n"
        f"Answer these specific questions:\n"
        f"1. Does the statute prohibit retaliatory eviction?\n"
        f"2. What specific types of protected tenant activity does it cover?\n"
        f"3. Is {statute_full} the operative statutory citation, or is there a more "
        f"   specific subsection?\n"
        f"4. Are there any leading appellate cases interpreting this statute in an "
        f"   eviction context (case name + citation)?\n\n"
        f"Return JSON only:\n"
        f"{{\n"
        f'  "statute_confirmed": true or false,\n'
        f'  "operative_citation": "most specific citation",\n'
        f'  "protects_against_retaliation": true or false,\n'
        f'  "protected_activities": ["list", "of", "protected", "activities"],\n'
        f'  "leading_case": "case name and citation if known, otherwise null",\n'
        f'  "confidence": "high|medium|low",\n'
        f'  "note": "any caveat or null"\n'
        f"}}"
    )


def classify_result(gpt: dict, gem: dict, statute: str) -> dict:
    """Classify two-model result: STATUTE-CONFIRMED, STATUTE-DIVERGENCE, or ERROR."""
    gpt_err = bool(gpt.get("error"))
    gem_err = bool(gem.get("error"))

    if gpt_err and gem_err:
        return {
            "classification": "ERROR",
            "recommended_statute": None,
            "note": f"Both models errored. GPT={gpt.get('error')}; Gem={gem.get('error')}",
        }

    if gpt_err or gem_err:
        answering = gpt if gem_err else gem
        model_name = "GPT" if gem_err else "Gemini"
        return {
            "classification": "SM-ERROR",
            "recommended_statute": answering.get("operative_citation"),
            "note": f"Single model only ({model_name}). {('GPT' if gpt_err else 'Gemini')} errored. Flag for re-run.",
        }

    gpt_confirmed = gpt.get("statute_confirmed", False)
    gem_confirmed = gem.get("statute_confirmed", False)
    gpt_cite = (gpt.get("operative_citation") or statute).strip()
    gem_cite = (gem.get("operative_citation") or statute).strip()
    gpt_protects = gpt.get("protects_against_retaliation", False)
    gem_protects = gem.get("protects_against_retaliation", False)

    # Both confirm and agree on protection
    if gpt_confirmed and gem_confirmed and gpt_protects and gem_protects:
        # Pick more specific citation
        recommended = gpt_cite if len(gpt_cite) >= len(gem_cite) else gem_cite
        leading = gpt.get("leading_case") or gem.get("leading_case")
        return {
            "classification": "STATUTE-CONFIRMED",
            "recommended_statute": recommended,
            "leading_case_found": leading,
            "note": (
                f"Both models confirm {recommended} protects against retaliation. "
                + (f"Leading case found: {leading}." if leading else "No leading appellate case identified.")
            ),
        }

    # Divergence
    return {
        "classification": "STATUTE-DIVERGENCE",
        "recommended_statute": None,
        "note": (
            f"Divergence: GPT_confirmed={gpt_confirmed}, Gem_confirmed={gem_confirmed}; "
            f"GPT_protects={gpt_protects}, Gem_protects={gem_protects}. "
            f"GPT cite={gpt_cite[:60]}, Gem cite={gem_cite[:60]}."
        ),
    }


def update_state_file(state: str, info: dict, result: dict, gpt: dict, gem: dict,
                      dry_run: bool) -> bool:
    """Write Track A result to state v2 file."""
    # Find state file
    import glob
    files = glob.glob(str(RULES_EVICTION_DIR / "**" / f"{state.lower()}_eviction_v2.json"), recursive=True)
    if not files:
        print(f"  WARNING: Could not find v2 file for {state}")
        return False

    fp = Path(files[0])
    with open(fp) as f:
        data = json.load(f)

    sd = data.get('substantive_defenses', [])
    ret = next((item for item in sd if item.get('defense') == 'retaliation'), None)
    if not ret:
        print(f"  WARNING: No retaliation defense found in {state} file")
        return False

    ld = ret.get('layer_decomposition', {})
    if not isinstance(ld, dict):
        ret['layer_decomposition'] = {}
        ld = ret['layer_decomposition']

    holdings = ld.get('holdings', {})
    if not isinstance(holdings, dict):
        holdings = {}
        ld['holdings'] = holdings

    cl = result["classification"]

    # Build Track A record
    track_a_record = {
        "track": "A",
        "validation_method": "statute-direct (no CL opinion text)",
        "run_date": TODAY,
        "runner": "track_a_statute_runner",
        "gpt_model": OPENAI_MODEL,
        "gemini_model": GEMINI_MODEL,
        "classification": cl,
        "recommended_statute": result.get("recommended_statute"),
        "leading_case_found": result.get("leading_case_found"),
        "note": result.get("note", ""),
        "gpt_summary": {
            "statute_confirmed": gpt.get("statute_confirmed"),
            "operative_citation": gpt.get("operative_citation"),
            "protects": gpt.get("protects_against_retaliation"),
            "leading_case": gpt.get("leading_case"),
            "confidence": gpt.get("confidence"),
        },
        "gemini_summary": {
            "statute_confirmed": gem.get("statute_confirmed"),
            "operative_citation": gem.get("operative_citation"),
            "protects": gem.get("protects_against_retaliation"),
            "leading_case": gem.get("leading_case"),
            "confidence": gem.get("confidence"),
        },
        "automation_ceiling": (
            "statute-verified is BELOW machine-verified, BELOW the attorney line. "
            "Not validated. Attorney must confirm before citing."
        ),
    }

    holdings['track_a'] = track_a_record
    if cl == "STATUTE-CONFIRMED":
        holdings.setdefault('validation_flags', [])
        if "TRACK-A-STATUTE-CONFIRMED" not in holdings.get('validation_flags', []):
            holdings.setdefault('validation_flags', []).append("TRACK-A-STATUTE-CONFIRMED")
        # If a leading case was found, add it to candidates for Track B
        leading = result.get("leading_case_found")
        if leading and leading != "null":
            existing_names = {c.get("case_name","") for c in holdings.get("candidates", [])}
            if leading not in existing_names:
                holdings.setdefault("candidates", []).append({
                    "case_name": leading,
                    "citation": None,
                    "cl_cluster_id": None,
                    "status": "track-a-model-suggested",
                    "note": f"Suggested by both models in Track A run {TODAY}. Not CL-verified.",
                })
    elif cl == "STATUTE-DIVERGENCE":
        holdings.setdefault('validation_flags', []).append("TRACK-A-DIVERGENCE")

    if not dry_run:
        data['last_updated'] = TODAY
        with open(fp, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  ✓ File updated: {fp.name}")

    return True


def run(states: list[str], dry_run: bool, sleep_secs: float):
    print("=" * 64)
    print(f"Track A Statute-Direct Retaliation Verification — {TODAY}")
    print(f"States: {', '.join(states)}")
    print(f"Models: GPT={OPENAI_MODEL} | Gemini={GEMINI_MODEL}")
    print(f"Dry run: {dry_run}")
    print("=" * 64)
    print()

    results = []
    n_confirmed = 0
    n_divergence = 0
    n_error = 0

    for i, state in enumerate(states, 1):
        if state not in TRACK_A_STATES:
            print(f"[{i}/{len(states)}] {state}: NOT in Track A states map — skipping")
            print(f"  Track A states: {list(TRACK_A_STATES.keys())}")
            continue

        info = TRACK_A_STATES[state]
        query = build_query(info["name"], info["statute"], info["statute_full"])

        print(f"[{i}/{len(states)}] {state} ({info['name']}) — {info['statute_full']}")
        print(f"  Reason: {info['reason']}")

        print(f"  Calling GPT ({OPENAI_MODEL}) ...")
        gpt = call_openai(query)
        time.sleep(sleep_secs)

        print(f"  Calling Gemini ({GEMINI_MODEL}) ...")
        gem = call_gemini(query)
        time.sleep(sleep_secs)

        cl_result = classify_result(gpt, gem, info["statute"])
        classification = cl_result["classification"]
        print(f"  Classification: {classification}")
        print(f"  Recommended statute: {cl_result.get('recommended_statute','—')}")
        if cl_result.get("leading_case_found"):
            print(f"  Leading case: {cl_result['leading_case_found']}")
        print(f"  Note: {cl_result.get('note','')[:100]}")

        if not dry_run:
            update_state_file(state, info, cl_result, gpt, gem, dry_run=False)

        results.append({
            "state": state,
            "statute": info["statute_full"],
            "reason": info["reason"],
            "classification": classification,
            "recommended_statute": cl_result.get("recommended_statute"),
            "leading_case_found": cl_result.get("leading_case_found"),
            "note": cl_result.get("note", ""),
            "gpt_result": {k: v for k, v in gpt.items() if k not in ("_raw",)},
            "gemini_result": {k: v for k, v in gem.items() if k not in ("_raw",)},
        })

        if classification == "STATUTE-CONFIRMED":
            n_confirmed += 1
        elif classification == "STATUTE-DIVERGENCE":
            n_divergence += 1
        else:
            n_error += 1

        if i < len(states):
            time.sleep(sleep_secs)

    # ── Report ────────────────────────────────────────────────────────────────
    print()
    print("=" * 64)
    print(f"DONE — {len(states)} states processed")
    print(f"  STATUTE-CONFIRMED  : {n_confirmed}")
    print(f"  STATUTE-DIVERGENCE : {n_divergence}")
    print(f"  ERROR/SM-ERROR     : {n_error}")
    if dry_run:
        print("  [DRY RUN — no files written]")
    print("=" * 64)

    # Write output JSON
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = OUT_DIR / f"track_a_statute_{ts}.json"
    if not dry_run:
        with open(out_path, "w") as f:
            json.dump({
                "runner": "track_a_statute_runner",
                "run_date": TODAY,
                "states": states,
                "summary": {
                    "total": len(states),
                    "statute_confirmed": n_confirmed,
                    "statute_divergence": n_divergence,
                    "error": n_error,
                },
                "note": (
                    "Track A = statute-direct (no CL opinion text). "
                    "STATUTE-CONFIRMED = both models agree the statute protects against retaliation. "
                    "Below machine-verified. Attorney must confirm before citing. "
                    "STATUTE-CONFIRMED with leading_case_found → case added to candidates for Track B CL verification."
                ),
                "results": results,
            }, f, indent=2, ensure_ascii=False)
        print(f"\nOutput: {out_path}")

    print("\n⚠️  STOP AND REPORT. Share output filename with Cowork for ingestion.")
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Track A Statute-Direct Retaliation Verification"
    )
    parser.add_argument("--states",
                        default=",".join(TRACK_A_STATES.keys()),
                        help=f"Comma-separated state codes (default: all Track A states: "
                             f"{','.join(TRACK_A_STATES.keys())})")
    parser.add_argument("--dry-run", action="store_true",
                        help="Query models but don't write files")
    parser.add_argument("--sleep", type=float, default=2.0,
                        help="Seconds between API calls (default: 2)")
    args = parser.parse_args()

    states = [s.strip().upper() for s in args.states.split(",") if s.strip()]
    run(states=states, dry_run=args.dry_run, sleep_secs=args.sleep)


if __name__ == "__main__":
    main()
