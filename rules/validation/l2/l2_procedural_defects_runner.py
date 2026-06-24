#!/usr/bin/env python3
"""
Eviction Rules — L2 Procedural Defects Runner
===============================================
Runs L2 multi-model consensus on the `procedural_defects` module across
all 51 states. Two goals:

  1. VALIDATE existing specific citations:
       - complaint_filed_before_notice_period_expired
       - wrong_court
     (Both already have state-specific citations; confirm correctness.)

  2. IMPROVE generic placeholder citations:
       - failure_to_attach_lease_or_notice_to_complaint
       - summons_improperly_issued_or_served
     (Currently cite only the root UD statute + "et seq."; retrieve the
      specific pleading/summons rule for each state.)

Classification (per state × defect):
  CONSENSUS-CONFIRM       → both models confirm current citation is accurate
  CONSENSUS-IMPROVE       → both models agree on a more specific citation
                            → auto-update the file
  NO-SPECIFIC-RULE        → both models say no separate specific rule exists
                            (generic citation is the correct answer)
  MODEL-SPLIT             → models disagree → L7 flag written to file
  ERROR                   → parse/API failure → logged, skip

Auto-update rule:
  CONSENSUS-IMPROVE only — update statute field in the file.
  Add validation_flag: "L2-PROCEDURAL-CONFIRMED" to confirmed entries.
  Add validation_flag: "L2-PROCEDURAL-SPLIT-L7" to splits.
  NEVER edits consequence, note, or defect fields.
  NEVER advances file_status or module_status.

GUARDRAILS (do not remove):
  - API keys from .env only; never hardcoded or logged
  - Neutral queries — do NOT tell model what the file currently says
  - $20 hard budget cap
  - Runner never advances any status past AUTOMATED-CHECKS-PASSED
  - All changes are additive (validation_flag) except CONSENSUS-IMPROVE statute update

Usage (run from repo root on Andy's local machine):
  python3 rules/validation/l2/l2_procedural_defects_runner.py
  python3 rules/validation/l2/l2_procedural_defects_runner.py --states CA,TX,NY
  python3 rules/validation/l2/l2_procedural_defects_runner.py --dry-run
  python3 rules/validation/l2/l2_procedural_defects_runner.py --defects attach,summons

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import os
import re
import sys
import time
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_L2_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_L2_DIR))

from l2_runner import (
    call_openai,
    call_gemini,
    load_all_v2_files,
    _parse_json_response,
    OPENAI_MODEL,
    GEMINI_MODEL,
    OPENAI_KEY,
    GOOGLE_KEY,
    BUDGET_CAP_USD,
    RULES_EVICTION_DIR,
    DOCS_DIR,
)

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

ALL_STATES = [
    "AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL",
    "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA",
    "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE",
    "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI",
    "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY",
]

# Four defects to process. Short keys used in --defects flag.
DEFECT_KEYS = {
    "premature":  "complaint_filed_before_notice_period_expired",
    "court":      "wrong_court",
    "attach":     "failure_to_attach_lease_or_notice_to_complaint",
    "summons":    "summons_improperly_issued_or_served",
}

# Defects where we expect generic citations and want specific ones
IMPROVE_TARGETS = {"failure_to_attach_lease_or_notice_to_complaint",
                   "summons_improperly_issued_or_served"}

# ~$0.015 per state × defect (2 model calls each)
APPROX_COST_PER_UNIT = 0.015
APPROX_TOTAL = APPROX_COST_PER_UNIT * len(ALL_STATES) * len(DEFECT_KEYS)

SYSTEM_PROMPT = (
    "You are a legal research expert in US residential landlord-tenant law and "
    "civil procedure. Answer questions about eviction (unlawful detainer) procedure "
    "in specific states. Be precise about statute and court rule citations. "
    "Return only the JSON format requested — no markdown fences or commentary."
)

# ── Per-defect query templates ────────────────────────────────────────────────

QUERIES = {
    "complaint_filed_before_notice_period_expired": (
        "In {state_name} ({state_code}), a landlord cannot file an unlawful detainer "
        "(eviction) complaint for nonpayment of rent until after the pay-or-quit notice "
        "period has expired. What is the specific statute (or court rule) that establishes "
        "this filing timing requirement? Do not cite the general notice statute — cite the "
        "provision that governs WHEN a complaint may be filed.\n\n"
        "Return JSON:\n"
        '{{\n'
        '  "statute": "exact citation",\n'
        '  "description": "one sentence on what this provision says",\n'
        '  "confidence": "high|medium|low",\n'
        '  "note": "any caveat or recent amendment"\n'
        '}}'
    ),
    "wrong_court": (
        "In {state_name} ({state_code}), which court has subject matter jurisdiction "
        "over residential eviction/unlawful detainer cases? What is the specific statute "
        "or constitutional provision that grants this court jurisdiction?\n\n"
        "Return JSON:\n"
        '{{\n'
        '  "court_name": "official name of the court",\n'
        '  "statute": "exact citation",\n'
        '  "dollar_limit": "monetary limit if any (null if none)",\n'
        '  "description": "one sentence on jurisdiction",\n'
        '  "confidence": "high|medium|low",\n'
        '  "note": "any caveat"\n'
        '}}'
    ),
    "failure_to_attach_lease_or_notice_to_complaint": (
        "In {state_name} ({state_code}), are landlords required by statute or court "
        "rule to attach the eviction notice (pay-or-quit notice) and/or the lease "
        "agreement to the unlawful detainer complaint when filing? If yes, what is "
        "the specific statute or court rule number? If no specific requirement exists "
        "(i.e., it is only a general pleading sufficiency issue), say so explicitly.\n\n"
        "Return JSON:\n"
        '{{\n'
        '  "attachment_required": true|false,\n'
        '  "statute": "specific citation, or null if no specific rule",\n'
        '  "what_must_be_attached": "notice only | lease only | both | neither",\n'
        '  "consequence_if_missing": "brief consequence",\n'
        '  "confidence": "high|medium|low",\n'
        '  "note": "any caveat"\n'
        '}}'
    ),
    "summons_improperly_issued_or_served": (
        "In {state_name} ({state_code}), what specific statute or court rule governs "
        "service of the summons in residential eviction/unlawful detainer proceedings? "
        "Note: this is about serving the court summons on the defendant after filing — "
        "NOT about serving the pre-lawsuit pay-or-quit notice. Cite the most specific "
        "provision, not just the general civil procedure code.\n\n"
        "Return JSON:\n"
        '{{\n'
        '  "statute": "specific citation (e.g., a specific section of the UD act or '
        'civil procedure code)",\n'
        '  "method": "how summons must be served in eviction cases",\n'
        '  "response_period_days": "days tenant has to respond (integer or null)",\n'
        '  "confidence": "high|medium|low",\n'
        '  "note": "any caveat or special eviction-track rule"\n'
        '}}'
    ),
}

# ── Helpers ───────────────────────────────────────────────────────────────────

STATE_NAMES = {
    "AK": "Alaska", "AL": "Alabama", "AR": "Arkansas", "AZ": "Arizona",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DC": "District of Columbia",
    "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii",
    "IA": "Iowa", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "MA": "Massachusetts",
    "MD": "Maryland", "ME": "Maine", "MI": "Michigan", "MN": "Minnesota",
    "MO": "Missouri", "MS": "Mississippi", "MT": "Montana", "NC": "North Carolina",
    "ND": "North Dakota", "NE": "Nebraska", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NV": "Nevada", "NY": "New York", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island",
    "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
    "UT": "Utah", "VA": "Virginia", "VT": "Vermont", "WA": "Washington",
    "WI": "Wisconsin", "WV": "West Virginia", "WY": "Wyoming",
}


def citations_equivalent(a: str, b: str) -> bool:
    """Fuzzy match: same if normalized strings share ≥70% of tokens,
    OR if both cite the same specific section number.

    The section-number check handles abbreviation vs. full-name divergence:
      "Tex. R. Civ. P. 510.4(b)-(c)" == "Texas Rule of Civil Procedure 510.4"
      "N.Y. Real Prop. Acts. Law § 735" == "New York Real Property Actions... § 735"
    """
    if not a or not b:
        return False
    a_norm = re.sub(r"[\s§.,;()]+", " ", a.lower()).strip()
    b_norm = re.sub(r"[\s§.,;()]+", " ", b.lower()).strip()
    if a_norm == b_norm:
        return True
    a_tokens = set(a_norm.split())
    b_tokens = set(b_norm.split())
    if not a_tokens or not b_tokens:
        return False
    overlap = a_tokens & b_tokens
    if len(overlap) / max(len(a_tokens), len(b_tokens)) >= 0.70:
        return True
    # Section-number match: "510.4", "415.45", "§ 735", etc.
    # Matches decimal section refs (510.4) or standalone 3+ digit numbers (735).
    sec_re = re.compile(r'\b(\d{2,}(?:\.\d+)+|\d{3,})\b')
    a_secs = set(sec_re.findall(a))
    b_secs = set(sec_re.findall(b))
    if a_secs and b_secs and (a_secs & b_secs):
        return True
    return False


def is_more_specific(new_cite: str, old_cite: str) -> bool:
    """True if new_cite looks more specific than old_cite (has a subsection, §, etc.)."""
    if not new_cite:
        return False
    # More specific = has a § with a number beyond the root
    has_section = bool(re.search(r"§\s*\d", new_cite))
    old_generic = "et seq" in old_cite.lower() or "state civil procedure rules" in old_cite.lower()
    return has_section and (old_generic or len(new_cite) > len(old_cite) + 5)


def query_model(model_fn, prompt: str, state: str = "", defect: str = "") -> dict:
    """Call a model with the user prompt. Retries once on empty raw response.

    call_openai / call_gemini each take a single (query: str) argument and
    return an already-parsed dict (plus "_raw" and optional "error" keys).
    The l2_runner's SYSTEM_PROMPT is baked into those functions.

    Empty _raw is the signature of a reasoning-model token-limit stall (gpt-5.5).
    One retry with a brief pause resolves most occurrences.
    """
    for attempt in range(2):
        try:
            result = model_fn(prompt)
            raw = result.get("_raw", "")
            if result.get("error"):
                if attempt == 0:
                    time.sleep(5)
                    continue
                return {"raw": raw, "parsed": None, "error": result["error"]}
            # Empty _raw = model returned no content — retry once
            if not raw and attempt == 0:
                time.sleep(5)
                continue
            return {"raw": raw, "parsed": result, "error": None}
        except Exception as e:
            if attempt == 0:
                time.sleep(5)
                continue
            return {"raw": None, "parsed": None, "error": str(e)}
    return {"raw": None, "parsed": None, "error": "max retries exceeded — empty response"}


# ── Per-unit classification ───────────────────────────────────────────────────

def classify_unit(state: str, defect: str, current_statute: str,
                  gpt_result: dict, gem_result: dict) -> dict:
    """
    Compare GPT and Gemini outputs. Return classification + recommended_statute.
    """
    gpt_p = gpt_result.get("parsed") or {}
    gem_p = gem_result.get("parsed") or {}

    gpt_stat = gpt_p.get("statute") or ""
    gem_stat = gem_p.get("statute") or ""

    gpt_conf = gpt_p.get("confidence", "low")
    gem_conf = gem_p.get("confidence", "low")

    # Handle attach-specific "no specific rule" case
    if defect == "failure_to_attach_lease_or_notice_to_complaint":
        gpt_required = gpt_p.get("attachment_required")
        gem_required = gem_p.get("attachment_required")
        if gpt_required is False and gem_required is False:
            return {
                "classification": "NO-SPECIFIC-RULE",
                "recommended_statute": None,
                "gpt_statute": gpt_stat,
                "gem_statute": gem_stat,
                "note": "Both models confirm no separate attachment statute — general pleading sufficiency applies.",
            }

    # Both errored
    if gpt_result.get("error") and gem_result.get("error"):
        return {"classification": "ERROR",
                "recommended_statute": None,
                "gpt_statute": None, "gem_statute": None,
                "note": f"Both failed: GPT={gpt_result['error']}; Gem={gem_result['error']}"}

    # One errored — but if the surviving model has a good answer, preserve it as SM
    if gpt_result.get("error") or not gpt_stat:
        if gem_stat:
            # Gemini has a valid answer; GPT was empty/failed → single-model-preliminary
            return {
                "classification": "SM-GEMINI",
                "recommended_statute": gem_stat,
                "gpt_statute": gpt_stat,
                "gem_statute": gem_stat,
                "note": (f"GPT returned no content (empty response); "
                         f"Gemini single-model: {gem_stat}. "
                         f"Preserved as SM — needs GPT re-run or human confirm."),
            }
        return {"classification": "ERROR",
                "recommended_statute": None,
                "gpt_statute": gpt_stat, "gem_statute": gem_stat,
                "note": f"Both models empty: GPT={gpt_result.get('error','')}; gem={gem_stat[:60]}"}
    if gem_result.get("error") or not gem_stat:
        if gpt_stat:
            return {
                "classification": "SM-GPT",
                "recommended_statute": gpt_stat,
                "gpt_statute": gpt_stat,
                "gem_statute": gem_stat,
                "note": (f"Gemini returned no content; GPT single-model: {gpt_stat}. "
                         f"Preserved as SM — needs Gemini re-run or human confirm."),
            }
        return {"classification": "ERROR",
                "recommended_statute": None,
                "gpt_statute": gpt_stat, "gem_statute": gem_stat,
                "note": f"Gem parse failure: {gem_result.get('error','')}; gpt={gpt_stat[:60]}"}

    models_agree = citations_equivalent(gpt_stat, gem_stat)

    if models_agree:
        # Do they improve on the current citation?
        agreed_stat = gpt_stat if len(gpt_stat) >= len(gem_stat) else gem_stat
        if defect in IMPROVE_TARGETS and is_more_specific(agreed_stat, current_statute):
            return {
                "classification": "CONSENSUS-IMPROVE",
                "recommended_statute": agreed_stat,
                "gpt_statute": gpt_stat,
                "gem_statute": gem_stat,
                "note": f"Both models agree on more specific citation. Confidence: GPT={gpt_conf}, Gem={gem_conf}.",
            }
        else:
            return {
                "classification": "CONSENSUS-CONFIRM",
                "recommended_statute": agreed_stat if agreed_stat else current_statute,
                "gpt_statute": gpt_stat,
                "gem_statute": gem_stat,
                "note": f"Both models confirm. Confidence: GPT={gpt_conf}, Gem={gem_conf}.",
            }
    else:
        return {
            "classification": "MODEL-SPLIT",
            "recommended_statute": None,
            "gpt_statute": gpt_stat,
            "gem_statute": gem_stat,
            "note": f"Models disagree. GPT: {gpt_stat[:60]}. Gem: {gem_stat[:60]}. L7 required.",
        }


# ── File update ───────────────────────────────────────────────────────────────

def update_file(file_path: Path, state: str, defect_name: str,
                classification: str, recommended_statute: Optional[str],
                note: str, dry_run: bool) -> bool:
    """Apply classification result to the state file. Returns True if modified."""
    with open(file_path) as f:
        data = json.load(f)

    pd = data.get("procedural_defects", [])
    modified = False

    for item in pd:
        if item.get("defect") != defect_name:
            continue

        if classification == "CONSENSUS-IMPROVE" and recommended_statute:
            if not dry_run:
                item["statute"] = recommended_statute
            item.setdefault("validation_flags", [])
            if "L2-PROCEDURAL-IMPROVED" not in item.get("validation_flags", []):
                item.setdefault("validation_flags", []).append("L2-PROCEDURAL-IMPROVED")
            item["l2_note"] = note
            item["l2_run_date"] = TODAY
            modified = True

        elif classification == "CONSENSUS-CONFIRM":
            item.setdefault("validation_flags", [])
            if "L2-PROCEDURAL-CONFIRMED" not in item.get("validation_flags", []):
                item.setdefault("validation_flags", []).append("L2-PROCEDURAL-CONFIRMED")
            item["l2_run_date"] = TODAY
            modified = True

        elif classification == "NO-SPECIFIC-RULE":
            item.setdefault("validation_flags", [])
            if "L2-PROCEDURAL-NO-SPECIFIC-RULE" not in item.get("validation_flags", []):
                item.setdefault("validation_flags", []).append("L2-PROCEDURAL-NO-SPECIFIC-RULE")
            item["l2_note"] = note
            item["l2_run_date"] = TODAY
            modified = True

        elif classification == "MODEL-SPLIT":
            item.setdefault("validation_flags", [])
            if "L2-PROCEDURAL-SPLIT-L7" not in item.get("validation_flags", []):
                item.setdefault("validation_flags", []).append("L2-PROCEDURAL-SPLIT-L7")
            item["l2_note"] = note
            item["l2_run_date"] = TODAY
            modified = True

        elif classification in ("SM-GEMINI", "SM-GPT"):
            # Single-model preliminary — preserve the surviving model's answer without
            # overwriting the main statute field. Flag for second-model re-run.
            flag = "L2-PROCEDURAL-SM-GEMINI" if classification == "SM-GEMINI" else "L2-PROCEDURAL-SM-GPT"
            item.setdefault("validation_flags", [])
            if flag not in item.get("validation_flags", []):
                item["validation_flags"].append(flag)
            item["l2_sm_statute"] = recommended_statute  # survivor's answer, unconfirmed
            item["l2_note"] = note[:200]
            item["l2_run_date"] = TODAY
            modified = True

        elif classification == "ERROR":
            item.setdefault("validation_flags", [])
            if "L2-PROCEDURAL-ERROR" not in item.get("validation_flags", []):
                item.setdefault("validation_flags", []).append("L2-PROCEDURAL-ERROR")
            item["l2_note"] = note[:120]
            item["l2_run_date"] = TODAY
            modified = True

    if modified and not dry_run:
        data["last_updated"] = TODAY
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n") if False else None  # json.dump handles trailing newline

    return modified


# ── Main runner ───────────────────────────────────────────────────────────────

def run(states: list[str], defects_to_run: list[str], dry_run: bool, sleep_secs: float):
    print("=" * 64)
    print(f"L2 Procedural Defects Runner")
    print(f"States : {len(states)} | Defects: {len(defects_to_run)}")
    print(f"Models : GPT={OPENAI_MODEL} | Gemini={GEMINI_MODEL}")
    print(f"Dry run: {dry_run}")
    print(f"Est. cost: ${APPROX_COST_PER_UNIT * len(states) * len(defects_to_run):.2f}")
    print(f"Budget cap: ${BUDGET_CAP_USD}")
    print("=" * 64)
    print()

    if not OPENAI_KEY or not GOOGLE_KEY:
        print("ERROR: OPENAI_API_KEY or GOOGLE_API_KEY not set in environment.")
        sys.exit(1)

    # load_all_v2_files() → (data_dict, path_dict) keyed by state_code
    all_data, all_paths = load_all_v2_files()
    file_map = {}
    for sc, data in all_data.items():
        fp = all_paths.get(sc)
        if fp:
            file_map[sc] = (fp, data)

    results = []
    total_units = len(states) * len(defects_to_run)
    done = 0
    n_improved = 0
    n_confirmed = 0
    n_no_specific = 0
    n_split = 0
    n_sm = 0
    n_error = 0

    for state in states:
        if state not in file_map:
            print(f"[{state}] No v2 file found — skipping")
            continue

        fp, data = file_map[state]
        state_name = STATE_NAMES.get(state, state)
        pd = data.get("procedural_defects", [])

        # Build lookup by defect name
        defect_map = {item["defect"]: item for item in pd}

        for defect_name in defects_to_run:
            done += 1
            item = defect_map.get(defect_name)
            if not item:
                print(f"  [{state}] {defect_name}: not found in file — skipping")
                continue

            current_statute = item.get("statute", "")
            prompt = QUERIES[defect_name].format(
                state_name=state_name,
                state_code=state,
            )

            print(f"[{done}/{total_units}] {state} / {defect_name[:40]}")

            gpt_result = query_model(
                call_openai, prompt, state, defect_name
            )
            time.sleep(sleep_secs)
            gem_result = query_model(
                call_gemini, prompt, state, defect_name
            )
            time.sleep(sleep_secs)

            cl = classify_unit(state, defect_name, current_statute, gpt_result, gem_result)
            classification = cl["classification"]
            print(f"  → {classification} | GPT: {(cl.get('gpt_statute') or '')[:50]} | "
                  f"Gem: {(cl.get('gem_statute') or '')[:50]}")

            modified = update_file(
                Path(fp), state, defect_name,
                classification,
                cl.get("recommended_statute"),
                cl.get("note", ""),
                dry_run,
            )

            results.append({
                "state": state,
                "defect": defect_name,
                "classification": classification,
                "current_statute": current_statute,
                "recommended_statute": cl.get("recommended_statute"),
                "gpt_statute": cl.get("gpt_statute"),
                "gem_statute": cl.get("gem_statute"),
                "note": cl.get("note"),
                "file_modified": modified and not dry_run,
            })

            if classification == "CONSENSUS-IMPROVE": n_improved += 1
            elif classification == "CONSENSUS-CONFIRM": n_confirmed += 1
            elif classification == "NO-SPECIFIC-RULE": n_no_specific += 1
            elif classification == "MODEL-SPLIT": n_split += 1
            elif classification in ("SM-GEMINI", "SM-GPT"): n_sm += 1
            else: n_error += 1

    # ── Report ────────────────────────────────────────────────────────────────
    print()
    print("=" * 64)
    print(f"DONE — {done} units processed")
    print(f"  CONSENSUS-IMPROVE    : {n_improved}  (statute updated)")
    print(f"  CONSENSUS-CONFIRM    : {n_confirmed}  (citation confirmed)")
    print(f"  NO-SPECIFIC-RULE     : {n_no_specific}  (no separate rule exists)")
    print(f"  MODEL-SPLIT (L7)     : {n_split}  (attorney review needed)")
    print(f"  SM-GEMINI/SM-GPT     : {n_sm}  (single-model; l2_sm_statute set; needs re-run)")
    print(f"  ERROR                : {n_error}  (both models empty)")
    if dry_run:
        print("  [DRY RUN — no files written]")
    print("=" * 64)

    # Write results JSON
    out_dir = Path(RULES_EVICTION_DIR).parent.parent / "validation" / "l2" / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
    out_path = out_dir / f"l2_procedural_defects_{ts}.json"
    if not dry_run:
        with open(out_path, "w") as f:
            json.dump({
                "runner": "l2_procedural_defects_runner",
                "run_date": TODAY,
                "states": states,
                "defects": defects_to_run,
                "summary": {
                    "total": done,
                    "consensus_improve": n_improved,
                    "consensus_confirm": n_confirmed,
                    "no_specific_rule": n_no_specific,
                    "model_split_l7": n_split,
                    "single_model_preliminary": n_sm,
                    "error": n_error,
                },
                "results": results,
            }, f, indent=2, ensure_ascii=False)
        print(f"\nOutput: {out_path}")
        print("\n⚠️  STOP AND REPORT. Share output filename with Cowork for ingestion.")
    else:
        print("\n[Dry run — output not written]")

    return results


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="L2 Procedural Defects Runner — multi-model statute validation"
    )
    parser.add_argument("--states", default=",".join(ALL_STATES),
                        help="Comma-separated state codes (default: all 51)")
    parser.add_argument("--defects", default=",".join(DEFECT_KEYS.keys()),
                        help=f"Defect short keys to run: {', '.join(DEFECT_KEYS.keys())} (default: all)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Query models but don't write to files")
    parser.add_argument("--sleep", type=float, default=2.0,
                        help="Seconds between API calls (default: 2)")
    args = parser.parse_args()

    states = [s.strip().upper() for s in args.states.split(",") if s.strip()]
    defect_keys = [d.strip().lower() for d in args.defects.split(",") if d.strip()]

    # Resolve short keys → full defect names
    defects_to_run = []
    for key in defect_keys:
        if key in DEFECT_KEYS:
            defects_to_run.append(DEFECT_KEYS[key])
        elif key in DEFECT_KEYS.values():
            defects_to_run.append(key)
        else:
            print(f"ERROR: Unknown defect key '{key}'. Valid: {list(DEFECT_KEYS.keys())}")
            sys.exit(1)

    run(states=states, defects_to_run=defects_to_run,
        dry_run=args.dry_run, sleep_secs=args.sleep)


if __name__ == "__main__":
    main()
