#!/usr/bin/env python3
"""
NJ failure_to_attach Reformulated Retry — 2026-06-26
======================================================
Targeted retry for New Jersey's failure_to_attach_lease_or_notice_to_complaint
procedural defect. Three prior runs produced ERROR (both models empty / GPT timeout).
NJ probe (nj_attach_probe_20260626.py) confirmed: Gemini returns content with
consequence-framing queries; GPT consistently times out at 60s.

This runner:
  - Uses a shorter, more focused query (reduce GPT reasoning time)
  - Increases GPT timeout to 120s (from 60s)
  - Uses consequence-framing for Gemini (query that worked in probe)
  - If GPT still times out → classify SM-GEMINI; record best Gemini answer
  - If both answer → classify CONSENSUS-CONFIRM or CONSENSUS-IMPROVE per normal logic

Evidence from probe (nj_attach_probe_20260626.json):
  P3 (best Gemini answer): N.J. Court Rule 6:3-4(c) — notice required to be attached;
    failure is valid defense; only notice required (not lease); valid_defense_if_omitted=true
  Current file statute: "NJSA 2A:18-51 et seq. (pleading requirements)" — too generic

Output: rules/validation/l2/output/nj_attach_retry_20260626.json
Then: STOP AND REPORT to Cowork for ingestion.

Usage:
  python3 rules/validation/l2/nj_attach_retry_20260626.py
  python3 rules/validation/l2/nj_attach_retry_20260626.py --dry-run

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import os
import re
import sys
import time
import argparse
import concurrent.futures
from datetime import datetime, timezone
from pathlib import Path

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
    OPENAI_MODEL,
    GEMINI_MODEL,
    _parse_json_response,
)

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
STATE = "NJ"
STATE_NAME = "New Jersey"
DEFECT = "failure_to_attach_lease_or_notice_to_complaint"
NJ_FILE = _REPO_ROOT / "rules" / "eviction" / "new-jersey" / "nj_eviction_v2.json"
OUT_DIR = _SCRIPT_DIR / "output"

# Current file statute (from prior runs): "NJSA 2A:18-51 et seq. (pleading requirements)"
CURRENT_STATUTE = "NJSA 2A:18-51 et seq. (pleading requirements)"

SYSTEM_PROMPT = (
    "You are a legal research expert in US residential landlord-tenant law and civil procedure. "
    "Answer questions about eviction procedure in New Jersey. Be precise about statute and court "
    "rule citations. Return only the JSON format requested — no markdown fences or commentary."
)

# Shorter, more focused query to reduce GPT reasoning time.
# Framing: consequence-first (worked best in probe P3).
NJ_QUERY = (
    "In New Jersey, what specific court rule requires a landlord to attach the eviction "
    "notice (notice to quit or notice to pay) to the summary dispossess complaint when filing? "
    "Is failure to attach a valid procedural defense for the tenant?\n\n"
    "IMPORTANT: Focus only on the specific court rule — NOT the general pleading statute. "
    "The answer is a specific New Jersey Court Rule (R. 6:x-x). If you are uncertain of the "
    "exact rule number, give your best answer with a confidence level.\n\n"
    "Return JSON only:\n"
    "{\n"
    '  "attachment_required": true or false,\n'
    '  "statute": "specific N.J. Court Rule citation",\n'
    '  "what_must_be_attached": "notice only | lease only | both | neither",\n'
    '  "consequence_if_missing": "brief consequence",\n'
    '  "confidence": "high|medium|low",\n'
    '  "note": "any caveat or null"\n'
    "}"
)


def call_openai_nj(dry_run: bool = False) -> dict:
    """Call GPT with 120s timeout (instead of default 60s)."""
    if dry_run:
        return {
            "attachment_required": True,
            "statute": "DRY-RUN",
            "what_must_be_attached": "notice only",
            "consequence_if_missing": "dismissal",
            "confidence": "high",
            "note": None,
            "model": OPENAI_MODEL,
            "_raw": "",
        }

    try:
        from openai import OpenAI
    except ImportError:
        return {"error": "openai package not installed", "model": OPENAI_MODEL}

    try:
        client = OpenAI(api_key=OPENAI_KEY)
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": NJ_QUERY},
            ],
            max_completion_tokens=8000,
            timeout=120,   # increased from 60s — NJ GPT consistently times out at 60s
        )
        raw = resp.choices[0].message.content.strip()
        parsed = _parse_json_response(raw)
        parsed["model"] = OPENAI_MODEL
        parsed["_raw"] = raw
        return parsed
    except Exception as exc:
        return {"error": str(exc), "model": OPENAI_MODEL}


def call_gemini_nj(dry_run: bool = False) -> dict:
    """Call Gemini with 90s timeout — same consequence-framing that worked in probe P3."""
    if dry_run:
        return {
            "attachment_required": True,
            "statute": "N.J. Court Rule 6:3-4(c) [DRY-RUN]",
            "what_must_be_attached": "notice only",
            "consequence_if_missing": "valid procedural defense; may cause dismissal",
            "confidence": "high",
            "note": None,
            "model": GEMINI_MODEL,
            "_raw": "",
        }

    try:
        from google import genai
    except ImportError:
        return {"error": "google-genai package not installed", "model": GEMINI_MODEL}

    try:
        client = genai.Client(api_key=GOOGLE_KEY)
        full_prompt = SYSTEM_PROMPT + "\n\n" + NJ_QUERY

        def _do_gemini():
            return client.models.generate_content(model=GEMINI_MODEL, contents=full_prompt)

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            fut = pool.submit(_do_gemini)
            try:
                resp = fut.result(timeout=90)
            except concurrent.futures.TimeoutError:
                return {"error": "Gemini API timed out after 90s", "model": GEMINI_MODEL}

        raw = resp.text.strip()
        parsed = _parse_json_response(raw)
        parsed["model"] = GEMINI_MODEL
        parsed["_raw"] = raw
        return parsed
    except Exception as exc:
        return {"error": str(exc), "model": GEMINI_MODEL}


def citations_similar(a: str, b: str) -> bool:
    """True if both citations share a court rule number (e.g. 6:3-4)."""
    if not a or not b:
        return False
    rule_re = re.compile(r'\b(\d+:\d+-\d+(?:\([a-z]\))?)\b', re.IGNORECASE)
    a_rules = set(rule_re.findall(a))
    b_rules = set(rule_re.findall(b))
    return bool(a_rules & b_rules)


def classify(gpt: dict, gem: dict) -> dict:
    """
    Classify the two-model result using the standard L2 taxonomy.
    Returns dict with classification + recommended_statute + note.
    """
    gpt_err = bool(gpt.get("error"))
    gem_err = bool(gem.get("error"))

    if gpt_err and gem_err:
        return {
            "classification": "ERROR",
            "recommended_statute": None,
            "note": f"Both models empty. GPT={gpt.get('error','?')}; Gem={gem.get('error','?')}",
        }

    if gpt_err:
        gem_stat = gem.get("statute") or gem.get("statute_or_rule")
        return {
            "classification": "SM-GEMINI",
            "recommended_statute": gem_stat,
            "note": (
                f"GPT timed out ({gpt.get('error','?')}). Gemini: {gem_stat}. "
                f"Set l2_sm_statute to best Gemini answer; flag for GPT re-run."
            ),
        }

    if gem_err:
        gpt_stat = gpt.get("statute")
        return {
            "classification": "SM-GPT",
            "recommended_statute": gpt_stat,
            "note": f"Gemini empty ({gem.get('error','?')}). GPT: {gpt_stat}. Flag for re-run.",
        }

    # Both answered — compare
    gpt_stat = (gpt.get("statute") or "").strip()
    gem_stat = (gem.get("statute") or gem.get("statute_or_rule") or "").strip()
    gpt_req  = gpt.get("attachment_required")
    gem_req  = gem.get("attachment_required")

    # If both say "no specific rule" or not required
    if not gpt_req and not gem_req:
        return {
            "classification": "NO-SPECIFIC-RULE",
            "recommended_statute": None,
            "note": "Both models: no specific attachment rule. General pleading governs.",
        }

    # If both say required and cite similar rule
    if gpt_req and gem_req and citations_similar(gpt_stat, gem_stat):
        recommended = gpt_stat if len(gpt_stat) >= len(gem_stat) else gem_stat
        if recommended != CURRENT_STATUTE:
            return {
                "classification": "CONSENSUS-IMPROVE",
                "recommended_statute": recommended,
                "note": f"Both models agree: {recommended}. More specific than current '{CURRENT_STATUTE}'.",
            }
        else:
            return {
                "classification": "CONSENSUS-CONFIRM",
                "recommended_statute": CURRENT_STATUTE,
                "note": "Both models confirm current statute.",
            }

    # Both required but different citations
    if gpt_req and gem_req:
        return {
            "classification": "MODEL-SPLIT",
            "recommended_statute": None,
            "note": (
                f"Both say required, but different rules: "
                f"GPT={gpt_stat[:80]} | Gemini={gem_stat[:80]}. "
                f"L7 flag written."
            ),
        }

    # One says required, other doesn't
    return {
        "classification": "MODEL-SPLIT",
        "recommended_statute": None,
        "note": (
            f"Split on whether required: GPT_req={gpt_req}, Gem_req={gem_req}. "
            f"GPT={gpt_stat[:60]}, Gem={gem_stat[:60]}. L7 flag written."
        ),
    }


def update_nj_file(result: dict, dry_run: bool) -> bool:
    """
    Write classification back to NJ v2 file (same update logic as main runner).
    Returns True if file was modified.
    """
    if not NJ_FILE.exists():
        print(f"ERROR: NJ file not found: {NJ_FILE}")
        return False

    with open(NJ_FILE) as f:
        data = json.load(f)

    pd = data.get("procedural_defects", [])
    defect_map = {item["defect"]: item for item in pd}
    item = defect_map.get(DEFECT)
    if not item:
        print(f"ERROR: {DEFECT} not found in NJ file procedural_defects")
        return False

    cl = result["classification"]
    note = result.get("note", "")
    recommended = result.get("recommended_statute")
    modified = False

    if cl == "CONSENSUS-IMPROVE" and recommended:
        item["statute"] = recommended
        item.setdefault("validation_flags", [])
        if "L2-PROCEDURAL-CONFIRMED" not in item["validation_flags"]:
            item["validation_flags"].append("L2-PROCEDURAL-CONFIRMED")
        # Remove prior ERROR/SM flags since we now have a result
        for stale in ("L2-PROCEDURAL-SM-GEMINI", "L2-PROCEDURAL-ERROR"):
            if stale in item["validation_flags"]:
                item["validation_flags"].remove(stale)
        item["l2_note"] = f"[RETRY 2026-06-26] CONSENSUS-IMPROVE: {recommended[:80]}"
        item["l2_run_date"] = TODAY
        modified = True

    elif cl == "CONSENSUS-CONFIRM":
        item.setdefault("validation_flags", [])
        if "L2-PROCEDURAL-CONFIRMED" not in item["validation_flags"]:
            item["validation_flags"].append("L2-PROCEDURAL-CONFIRMED")
        for stale in ("L2-PROCEDURAL-SM-GEMINI", "L2-PROCEDURAL-ERROR"):
            if stale in item["validation_flags"]:
                item["validation_flags"].remove(stale)
        item["l2_note"] = f"[RETRY 2026-06-26] CONSENSUS-CONFIRM: current statute confirmed."
        item["l2_run_date"] = TODAY
        modified = True

    elif cl == "NO-SPECIFIC-RULE":
        item.setdefault("validation_flags", [])
        if "L2-PROCEDURAL-NO-SPECIFIC-RULE" not in item["validation_flags"]:
            item["validation_flags"].append("L2-PROCEDURAL-NO-SPECIFIC-RULE")
        for stale in ("L2-PROCEDURAL-SM-GEMINI", "L2-PROCEDURAL-ERROR"):
            if stale in item["validation_flags"]:
                item["validation_flags"].remove(stale)
        item["l2_note"] = f"[RETRY 2026-06-26] NO-SPECIFIC-RULE: general pleading governs."
        item["l2_run_date"] = TODAY
        modified = True

    elif cl == "MODEL-SPLIT":
        item.setdefault("validation_flags", [])
        if "L2-PROCEDURAL-SPLIT-L7" not in item["validation_flags"]:
            item["validation_flags"].append("L2-PROCEDURAL-SPLIT-L7")
        item["l2_note"] = f"[RETRY 2026-06-26] MODEL-SPLIT: {note[:120]}"
        item["l2_run_date"] = TODAY
        modified = True

    elif cl == "SM-GEMINI" and recommended:
        # Update sm_statute with latest Gemini answer from retry
        item["l2_sm_statute"] = recommended
        item.setdefault("validation_flags", [])
        # Keep SM-GEMINI flag, remove ERROR since Gemini now answered
        if "L2-PROCEDURAL-ERROR" in item["validation_flags"]:
            item["validation_flags"].remove("L2-PROCEDURAL-ERROR")
        if "L2-PROCEDURAL-SM-GEMINI" not in item["validation_flags"]:
            item["validation_flags"].append("L2-PROCEDURAL-SM-GEMINI")
        item["l2_note"] = (
            f"[RETRY 2026-06-26] SM-GEMINI: GPT timed out again at 120s. "
            f"Gemini: {recommended[:80]}. Needs GPT re-run with longer timeout or different model."
        )
        item["l2_run_date"] = TODAY
        modified = True

    elif cl == "ERROR":
        # Both still empty — log but don't change flags (already have them)
        item["l2_note"] = f"[RETRY 2026-06-26] ERROR: both models empty. {note[:100]}"
        item["l2_run_date"] = TODAY
        modified = True

    if modified and not dry_run:
        data["last_updated"] = TODAY
        with open(NJ_FILE, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  ✓ File updated: {NJ_FILE.name}")

    return modified


def run(dry_run: bool = False):
    print("=" * 64)
    print(f"NJ failure_to_attach Reformulated Retry — {TODAY}")
    print(f"GPT timeout: 120s (was 60s) | Gemini timeout: 90s")
    print(f"Dry run: {dry_run}")
    print("=" * 64)

    print(f"\n[1/2] Calling GPT ({OPENAI_MODEL}) ...")
    gpt = call_openai_nj(dry_run)
    gpt_stat = gpt.get("statute") or gpt.get("error", "empty")
    print(f"  GPT: {gpt_stat[:80]}")

    print(f"\n[2/2] Calling Gemini ({GEMINI_MODEL}) ...")
    gem = call_gemini_nj(dry_run)
    gem_stat = gem.get("statute") or gem.get("statute_or_rule") or gem.get("error", "empty")
    print(f"  Gem: {gem_stat[:80]}")

    cl = classify(gpt, gem)
    classification = cl["classification"]
    print(f"\nClassification: {classification}")
    print(f"  Note: {cl.get('note','')[:120]}")
    print(f"  Recommended: {cl.get('recommended_statute','none')}")

    # Write back to NJ file
    if not dry_run:
        print(f"\nUpdating NJ file ...")
        update_nj_file(cl, dry_run=False)

    # Write output JSON (provenance)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"nj_attach_retry_20260626.json"
    if not dry_run:
        with open(out_path, "w") as f:
            json.dump({
                "runner": "nj_attach_retry_20260626",
                "state": STATE,
                "defect": DEFECT,
                "run_date": TODAY,
                "gpt_timeout_secs": 120,
                "gemini_timeout_secs": 90,
                "prior_runs": 3,
                "query_reformulation": "consequence-framing + shorter text to reduce GPT reasoning time",
                "gpt_result": {k: v for k, v in gpt.items() if k != "_raw"},
                "gemini_result": {k: v for k, v in gem.items() if k != "_raw"},
                "classification": classification,
                "recommended_statute": cl.get("recommended_statute"),
                "note": cl.get("note"),
                "current_file_statute": CURRENT_STATUTE,
                "file_updated": not dry_run,
            }, f, indent=2, ensure_ascii=False)
        print(f"\nOutput: {out_path}")

    print("\n" + "=" * 64)
    if classification == "SM-GEMINI":
        print("RESULT: SM-GEMINI — GPT still timing out.")
        print("  Best Gemini answer recorded as l2_sm_statute in NJ file.")
        print("  Next step: consider GPT-4o fallback or submit via Anthropic API.")
    elif classification in ("CONSENSUS-IMPROVE", "CONSENSUS-CONFIRM", "NO-SPECIFIC-RULE"):
        print(f"RESULT: {classification} — two-model result achieved!")
    elif classification == "MODEL-SPLIT":
        print("RESULT: MODEL-SPLIT — L7 flag written. Add to HUMAN_REVIEW_QUEUE.")
    else:
        print(f"RESULT: {classification} — check output file.")
    print("=" * 64)
    print("\n⚠️  STOP AND REPORT. Share output filename with Cowork for ingestion.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NJ failure_to_attach retry runner")
    parser.add_argument("--dry-run", action="store_true",
                        help="Query models but don't write files")
    args = parser.parse_args()
    run(dry_run=args.dry_run)
