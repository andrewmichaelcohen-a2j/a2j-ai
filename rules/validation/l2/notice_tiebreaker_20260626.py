#!/usr/bin/env python3
"""
Notice Module — Tiebreaker Runner (2026-06-26)
================================================
Targeted tiebreaker queries for 7 states with NOTICE-L2 divergences from the
provenance rerun. Each query is state-specific and designed to directly resolve
the documented split (more targeted than the standard QUERY_TEMPLATE).

States: GA (CRITICAL), AR, MN, OR, SD, WY, TN
See HUMAN_REVIEW_QUEUE.md [NOTICE-L2-01] through [NOTICE-L2-09] for context.

Outcomes:
  TIEBREAKER-RESOLVED   → both models agree → log recommendation; file may be updated
  TIEBREAKER-SPLIT      → models still disagree → escalate to L7
  SM-TIEBREAKER         → one model empty (transient) → log, retry
  ERROR                 → both empty → log, retry

Usage:
  python rules/validation/l2/notice_tiebreaker_20260626.py
  python rules/validation/l2/notice_tiebreaker_20260626.py --dry-run

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import sys
import time
import argparse
from datetime import datetime, timezone
from pathlib import Path

# ── Repo root + env loading ───────────────────────────────────────────────────

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_ENV_PATH = _REPO_ROOT / ".env"

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv not installed. Run: pip install python-dotenv --break-system-packages")
    sys.exit(1)

load_dotenv(_ENV_PATH)

# Re-use call_openai and call_gemini from l2_runner
sys.path.insert(0, str(Path(__file__).parent))
from l2_runner import call_openai, call_gemini

# ── Tiebreaker queries (state-specific, targeted) ─────────────────────────────

TIEBREAKERS = [
    {
        "state_code": "GA",
        "state_name": "Georgia",
        "notice_l2_id": "NOTICE-L2-06",
        "priority": "CRITICAL",
        "file_value": {"days": 3, "notice_required": True, "statute": "OCGA §44-7-50"},
        "dispute": "GPT says no notice required (0d); file says 3d required; Gemini empty",
        "query": (
            "Under Georgia law (OCGA), when a residential tenant fails to pay rent, "
            "must the landlord give written notice to the tenant BEFORE filing an eviction "
            "(dispossessory) action? If yes, how many days notice is required and what is "
            "the specific statute? If no advance written notice is required before filing, "
            "state that explicitly — Georgia is one of several states where landlords may "
            "file immediately without prior notice.\n\n"
            "Focus specifically on: OCGA §44-7-50 and §44-7-52. Does either require "
            "advance written notice to the tenant, or do they only govern the dispossessory "
            "warrant process after filing?\n\n"
            "Respond ONLY in valid JSON:\n"
            "{\"days\": <integer or null>, \"notice_required\": <true or false>, "
            "\"statute\": \"<citation>\", \"rationale\": \"<2-3 sentences explaining "
            "whether advance written notice is required before filing>\"}"
        ),
    },
    {
        "state_code": "AR",
        "state_name": "Arkansas",
        "notice_l2_id": "NOTICE-L2-01",
        "priority": "NORMAL",
        "file_value": {"days": 3, "notice_required": True, "statute": "Ark. Code Ann. §18-17-701"},
        "dispute": "GPT says 3d; Gemini says 5d; both cite same statute",
        "query": (
            "Under Arkansas Residential Landlord-Tenant Act (Ark. Code Ann. Title 18, "
            "Chapter 17), specifically §18-17-701, how many days written notice must a "
            "landlord give a residential tenant for nonpayment of rent before the landlord "
            "may terminate the tenancy and file for eviction?\n\n"
            "Is the notice period 3 days or 5 days? Please read the statute carefully — "
            "there may be a distinction between the notice period and the cure period.\n\n"
            "Respond ONLY in valid JSON:\n"
            "{\"days\": <integer>, \"notice_required\": true, \"statute\": \"Ark. Code Ann. §18-17-701\", "
            "\"rationale\": \"<2-3 sentences citing the specific statutory language>\"}"
        ),
    },
    {
        "state_code": "MN",
        "state_name": "Minnesota",
        "notice_l2_id": "NOTICE-L2-02",
        "priority": "NORMAL",
        "file_value": {"days": 14, "notice_required": True, "statute": "Minn. Stat. §504B.321"},
        "dispute": "GPT says 14d (post-2023 HF 3019); Gemini says no notice required",
        "query": (
            "Under current Minnesota law (as of 2024), what is the required notice period "
            "for a landlord to give a residential tenant before filing an eviction for "
            "nonpayment of rent?\n\n"
            "IMPORTANT CONTEXT: Minnesota HF 3019 (2023) amended eviction notice "
            "requirements, adding a 14-day written notice requirement before a landlord "
            "may file an eviction for nonpayment. Please apply the law as amended by "
            "HF 3019, effective 2024. Does current Minnesota law require a 14-day notice "
            "period before filing for nonpayment eviction, or is no advance notice required?\n\n"
            "Respond ONLY in valid JSON:\n"
            "{\"days\": <integer or null>, \"notice_required\": <true or false>, "
            "\"statute\": \"<citation>\", \"rationale\": \"<2-3 sentences including whether "
            "HF 3019 / 2023 amendment applies and what the current requirement is>\"}"
        ),
    },
    {
        "state_code": "OR",
        "state_name": "Oregon",
        "notice_l2_id": "NOTICE-L2-03",
        "priority": "NORMAL",
        "file_value": {"days": 3, "notice_required": True, "statute": "ORS 90.394"},
        "dispute": "GPT says 10d; Gemini says 3d (72 hours); file says 3d",
        "query": (
            "Under Oregon Residential Landlord and Tenant Act, specifically ORS 90.394, "
            "how many days written notice must a landlord give a residential tenant for "
            "nonpayment of rent before the landlord may terminate the rental agreement "
            "and file for eviction?\n\n"
            "Note: Oregon has different notice periods for different situations. This "
            "question asks specifically about the standard nonpayment of rent notice "
            "under ORS 90.394. Is it 72 hours (3 days) or 10 days?\n\n"
            "Respond ONLY in valid JSON:\n"
            "{\"days\": <integer>, \"notice_required\": true, \"statute\": \"ORS 90.394\", "
            "\"rationale\": \"<2-3 sentences citing the specific statutory language and "
            "the exact number of hours/days>\"}"
        ),
    },
    {
        "state_code": "SD",
        "state_name": "South Dakota",
        "notice_l2_id": "NOTICE-L2-04",
        "priority": "NORMAL",
        "file_value": {"days": None, "notice_required": False, "statute": "SDCL (§21-16-2 repealed)"},
        "dispute": "GPT says no notice required (consistent with 2024 §21-16-2 repeal); Gemini says 3d",
        "query": (
            "Under South Dakota law, is a landlord required to give a residential tenant "
            "written notice before filing for eviction for nonpayment of rent?\n\n"
            "IMPORTANT CONTEXT: South Dakota SB 90 (enacted 2024) repealed SDCL §21-16-2 "
            "which had previously required a 3-day notice. After this repeal, is South "
            "Dakota a 'no advance notice required' state for nonpayment evictions?\n\n"
            "Please apply the law AS CURRENTLY IN EFFECT after SB 90 (2024). Is there "
            "still a notice requirement, or may landlords file immediately?\n\n"
            "Respond ONLY in valid JSON:\n"
            "{\"days\": <integer or null>, \"notice_required\": <true or false>, "
            "\"statute\": \"<current operative statute or null if none>\", "
            "\"rationale\": \"<2-3 sentences addressing the SB 90 repeal and current state>\"}"
        ),
    },
    {
        "state_code": "WY",
        "state_name": "Wyoming",
        "notice_l2_id": "NOTICE-L2-08",
        "priority": "LOW",
        "file_value": {"days": 3, "notice_required": True, "statute": "Wyo. Stat. §1-21-1003"},
        "dispute": "Period agrees (3d); GPT cites §1-21-1002, Gemini+file cite §1-21-1003",
        "query": (
            "Under Wyoming law, the landlord must give a residential tenant 3 days written "
            "notice for nonpayment of rent before filing for eviction. What is the SPECIFIC "
            "statute section that establishes this 3-day notice requirement?\n\n"
            "Is it Wyoming Statute §1-21-1002 or §1-21-1003? Please identify which "
            "section sets out the notice requirement for nonpayment of rent.\n\n"
            "Respond ONLY in valid JSON:\n"
            "{\"days\": 3, \"notice_required\": true, \"statute\": \"<exact citation: Wyo. Stat. §1-21-1002 or §1-21-1003>\", "
            "\"rationale\": \"<2 sentences explaining which section and what it says>\"}"
        ),
    },
    {
        "state_code": "TN",
        "state_name": "Tennessee",
        "notice_l2_id": "NOTICE-L2-09",
        "priority": "PIPELINE",
        "file_value": {"days": 14, "notice_required": True, "statute": "TCA §66-28-505"},
        "dispute": "Gemini says 14d (agrees with file); GPT timed out in prior run",
        "query": (
            "Under Tennessee Residential Landlord and Tenant Act, specifically TCA "
            "§66-28-505, how many days written notice must a landlord give a residential "
            "tenant for nonpayment of rent before filing an eviction action?\n\n"
            "Respond ONLY in valid JSON:\n"
            "{\"days\": <integer>, \"notice_required\": true, \"statute\": \"<citation>\", "
            "\"rationale\": \"<1-2 sentences>\"}"
        ),
    },
]

# ── Output path ───────────────────────────────────────────────────────────────

OUTPUT_DIR = _REPO_ROOT / "rules" / "validation" / "l2" / "output"
OUTPUT_FILE = OUTPUT_DIR / "notice_tiebreaker_20260626.json"


def classify(gpt: dict, gem: dict, file_val: dict) -> str:
    gpt_days = gpt.get("days") if not gpt.get("error") else None
    gem_days = gem.get("days") if not gem.get("error") else None
    gpt_req = gpt.get("notice_required") if not gpt.get("error") else None
    gem_req = gem.get("notice_required") if not gem.get("error") else None

    gpt_empty = gpt.get("error") or (gpt_days is None and gpt_req is None)
    gem_empty = gem.get("error") or (gem_days is None and gem_req is None)

    if gpt_empty and gem_empty:
        return "ERROR"
    if gpt_empty:
        return "SM-GEMINI"
    if gem_empty:
        return "SM-GPT"

    # Both responded — compare notice_required and days
    req_agree = (gpt_req == gem_req)
    days_agree = (gpt_days == gem_days)

    if req_agree and days_agree:
        # Check if agrees with file
        file_req = file_val.get("notice_required")
        file_days = file_val.get("days")
        if gpt_req == file_req and gpt_days == file_days:
            return "TIEBREAKER-CONFIRM-FILE"
        else:
            return "TIEBREAKER-RESOLVED-DIFFERS-FROM-FILE"
    else:
        return "TIEBREAKER-SPLIT"


def main():
    parser = argparse.ArgumentParser(description="Notice module tiebreaker — 7 states")
    parser.add_argument("--dry-run", action="store_true", help="No API calls")
    parser.add_argument("--sleep", type=int, default=15, help="Seconds between states (rate limit)")
    args = parser.parse_args()

    TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    results = []

    print(f"\n{'='*70}")
    print(f"NOTICE TIEBREAKER PASS — {TODAY}")
    print(f"States: {', '.join(t['state_code'] for t in TIEBREAKERS)}")
    print(f"{'='*70}\n")

    for i, tb in enumerate(TIEBREAKERS):
        code = tb["state_code"]
        print(f"[{i+1}/{len(TIEBREAKERS)}] {code} ({tb['notice_l2_id']}) — {tb['priority']}")
        print(f"  Dispute: {tb['dispute']}")

        if i > 0 and not args.dry_run:
            print(f"  (sleeping {args.sleep}s for rate limit...)")
            time.sleep(args.sleep)

        gpt = call_openai(tb["query"], dry_run=args.dry_run)
        gem = call_gemini(tb["query"], dry_run=args.dry_run)

        gpt_days = gpt.get("days") if not gpt.get("error") else "ERROR"
        gem_days = gem.get("days") if not gem.get("error") else "ERROR"
        gpt_req = gpt.get("notice_required") if not gpt.get("error") else "ERROR"
        gem_req = gem.get("notice_required") if not gem.get("error") else "ERROR"
        gpt_stat = gpt.get("statute", "") if not gpt.get("error") else gpt.get("error", "")
        gem_stat = gem.get("statute", "") if not gem.get("error") else gem.get("error", "")

        classification = classify(gpt, gem, tb["file_val"] if "file_val" in tb else tb["file_value"])

        print(f"  GPT:    notice_required={gpt_req}, days={gpt_days}, statute={(gpt_stat or '')[:60]}")
        print(f"  Gemini: notice_required={gem_req}, days={gem_days}, statute={(gem_stat or '')[:60]}")
        print(f"  File:   notice_required={tb['file_value']['notice_required']}, days={tb['file_value']['days']}")
        print(f"  → {classification}")

        if classification == "TIEBREAKER-CONFIRM-FILE":
            print(f"  ✅ CONFIRMED — file value correct, no change needed")
        elif classification == "TIEBREAKER-RESOLVED-DIFFERS-FROM-FILE":
            print(f"  ⚠️  RESOLVED BUT FILE DIFFERS — recommend file update (YELLOW)")
        elif classification == "TIEBREAKER-SPLIT":
            print(f"  🔴 STILL SPLIT — escalate to L7")
        elif classification in ("SM-GPT", "SM-GEMINI"):
            print(f"  🔁 SINGLE-MODEL — retry needed")
        else:
            print(f"  ❌ ERROR — both empty, retry")

        results.append({
            "state_code": code,
            "state_name": tb["state_name"],
            "notice_l2_id": tb["notice_l2_id"],
            "priority": tb["priority"],
            "dispute": tb["dispute"],
            "file_value": tb["file_value"],
            "gpt": {k: v for k, v in gpt.items() if k != "_raw"},
            "gemini": {k: v for k, v in gem.items() if k != "_raw"},
            "classification": classification,
            "run_date": TODAY,
        })
        print()

    # ── Summary ────────────────────────────────────────────────────────────────
    from collections import Counter
    counts = Counter(r["classification"] for r in results)
    print(f"{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    for cls, cnt in sorted(counts.items()):
        print(f"  {cls}: {cnt}")

    print()
    print("RECOMMENDATIONS:")
    for r in results:
        cls = r["classification"]
        if cls == "TIEBREAKER-CONFIRM-FILE":
            print(f"  ✅ {r['state_code']}: file confirmed correct — no action needed")
        elif cls == "TIEBREAKER-RESOLVED-DIFFERS-FROM-FILE":
            gpt_d = r["gpt"].get("days")
            gpt_s = r["gpt"].get("statute", "")
            print(f"  ⚠️  {r['state_code']}: tiebreaker resolved (days={gpt_d}, statute={gpt_s}) — file update needed (YELLOW)")
        elif cls == "TIEBREAKER-SPLIT":
            print(f"  🔴 {r['state_code']}: still split — escalate [NOTICE-L2-{r['notice_l2_id'][-2:]}] to L7")
        elif cls in ("SM-GPT", "SM-GEMINI"):
            print(f"  🔁 {r['state_code']}: single-model — retry pass needed")
        else:
            print(f"  ❌ {r['state_code']}: ERROR — both empty")

    # ── Write output ───────────────────────────────────────────────────────────
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump({
            "run_type": "notice_tiebreaker",
            "run_date": TODAY,
            "states": [r["state_code"] for r in results],
            "results": results,
            "summary": dict(counts),
        }, f, indent=2)

    print(f"\nOutput: {OUTPUT_FILE}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
