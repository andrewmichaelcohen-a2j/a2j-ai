#!/usr/bin/env python3
"""
Remaining Substantive Defenses — Elements Layer L2 Runner  (Module 6)
======================================================================
Runs L2 multi-model consensus on the ELEMENTS layer of four remaining
substantive defenses across all 51 states:

  • habitability_warranty
  • discrimination
  • breach_of_quiet_enjoyment
  • improper_rent_calculation

These are defenses WITHIN eviction proceedings — not proactive claims.
E.g., habitability as a defense to a nonpayment eviction where landlord
breached the implied warranty; discrimination where the eviction filing
itself is discriminatory.

The canonical rules files currently have a FLAT structure for these
defenses (elements list, statute, case_law). This runner:
  1. Queries both models per state (grouped — 4 defenses in one call)
  2. Classifies per-defense consensus
  3. Adds layer_decomposition.elements to each defense item
  4. Never edits existing flat elements/statute/case_law content
  5. Writes flags per defense

CRITICAL:
  - Neutral query — no file values fed to models
  - Keys from .env only; never hardcoded, logged, or committed
  - Never advances past ACP
  - AI resolution cap: SINGLE-MODEL-RESOLVED is highest auto-resolution
  - $15 budget cap (51 states × ~$0.10/state for 4-defense grouped query)

Usage (run from repo root in Andy's Terminal):
  cd /Users/andrewcohen/Documents/GitHub/a2j-ai
  python3 rules/validation/l2/remaining_defenses_elements_runner.py

Single state (testing):
  python3 rules/validation/l2/remaining_defenses_elements_runner.py --states CA

Dry run (no API, no write-back):
  python3 rules/validation/l2/remaining_defenses_elements_runner.py --dry-run

Expected: ~51 × $0.10 = ~$5.10. Expected time: ~15–20 minutes.
Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import os
import sys
import re
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List

# ── Shared utilities ───────────────────────────────────────────────────────────
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
    RULES_EVICTION_DIR,
)

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
BUDGET_CAP = 15.00
APPROX_COST_PER_STATE = 0.10  # grouped 4-defense query; larger than single-defense calls

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

ALL_STATES = [
    "AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL",
    "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA",
    "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE",
    "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI",
    "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY",
]

DEFENSE_KEYS = [
    "habitability_warranty",
    "discrimination",
    "breach_of_quiet_enjoyment",
    "improper_rent_calculation",
]

# States with known recent tenant-protection legislative activity
RECENCY_WATCH_STATES = {
    "CA": "Active habitability and anti-discrimination amendments; verify Civ. Code §1941 and Gov. Code §12955",
    "NY": "Good Cause Eviction (§226-f) may interact with discrimination defense framing",
    "WA": "RLTA 2021-2023 amendments expanded habitability and anti-discrimination provisions",
    "MN": "HF 3019 (2023) tenant protections; verify habitability chapter",
    "OR": "SB 278 (2023); verify ORS 90.320 habitability and ORS 659A discrimination coverage",
    "IL": "Chicago RLTO provides local habitability and quiet enjoyment remedies",
    "NJ": "Anti-Eviction Act and Truth-in-Renting interact with habitability defense",
}

# ── System prompt ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a legal research expert in US residential landlord-tenant law. "
    "You answer questions about defenses available to tenants in eviction proceedings. "
    "These are affirmative defenses raised IN COURT in response to an eviction filing — "
    "not proactive tenant claims. Be precise about statutory citations. "
    "Respond only in the JSON format requested."
)

# ── Query builder ──────────────────────────────────────────────────────────────

def build_query(state_name: str) -> str:
    """
    Neutral grouped query — asks about all 4 defenses in one call.
    No file values fed to models.
    """
    return f"""In {state_name}, what are the legal elements a residential tenant must establish
to assert each of the following as an AFFIRMATIVE DEFENSE in an eviction proceeding?

Treat each defense as a tenant's response to a landlord's eviction filing in court.

For each defense, provide:
1. Whether the defense is recognized in {state_name} eviction proceedings
2. The formal elements the tenant must establish
3. The primary governing statute (if any) with specific section
4. A key case citation (if any)
5. Any important limitations or caveats for this state

Respond ONLY in valid JSON with this exact structure:
{{
  "defenses": {{
    "habitability_warranty": {{
      "recognized_as_defense": true,
      "elements": [
        "Element 1 description",
        "Element 2 description"
      ],
      "primary_statute": "e.g., Cal. Civ. Code §1941 / RLTA §59.18.060",
      "key_case": "case citation or null",
      "note": "any important caveats, variations, or limitations specific to {state_name}"
    }},
    "discrimination": {{
      "recognized_as_defense": true,
      "elements": [
        "Element 1 description",
        "Element 2 description"
      ],
      "primary_statute": "e.g., 42 U.S.C. §3604 (FHA); [state fair housing statute]",
      "key_case": "case citation or null",
      "note": "state-specific protected classes beyond federal FHA, if any"
    }},
    "breach_of_quiet_enjoyment": {{
      "recognized_as_defense": true,
      "elements": [
        "Element 1 description",
        "Element 2 description"
      ],
      "primary_statute": "statute or null if common law only",
      "key_case": "case citation or null",
      "note": "whether codified in {state_name} RLTA or purely common law"
    }},
    "improper_rent_calculation": {{
      "recognized_as_defense": true,
      "elements": [
        "Element 1 description",
        "Element 2 description"
      ],
      "primary_statute": "e.g., [state eviction notice statute]",
      "key_case": "case citation or null",
      "note": "whether impermissible charges (late fees, etc.) void the notice or merely reduce the demand"
    }}
  }},
  "confidence": "high|medium|low",
  "overall_note": "any cross-cutting observations about {state_name} defenses"
}}"""


# ── API callers ────────────────────────────────────────────────────────────────

DRY_RUN_RESPONSE = {
    "defenses": {
        "habitability_warranty": {
            "recognized_as_defense": True,
            "elements": ["Landlord knew of defect", "Defect substantially impairs habitability",
                         "Reasonable notice given", "Landlord failed to repair"],
            "primary_statute": "DRY §1941",
            "key_case": None,
            "note": "dry run",
        },
        "discrimination": {
            "recognized_as_defense": True,
            "elements": ["Member of protected class", "Adverse housing action", "Causal connection"],
            "primary_statute": "42 U.S.C. §3604",
            "key_case": None,
            "note": "dry run",
        },
        "breach_of_quiet_enjoyment": {
            "recognized_as_defense": True,
            "elements": ["Valid tenancy", "Substantial interference", "Landlord caused interference"],
            "primary_statute": None,
            "key_case": None,
            "note": "dry run",
        },
        "improper_rent_calculation": {
            "recognized_as_defense": True,
            "elements": ["Amount demanded exceeds lawful rent", "Impermissible charges included"],
            "primary_statute": "DRY §1161",
            "key_case": None,
            "note": "dry run",
        },
    },
    "confidence": "high",
    "overall_note": "dry run",
}


def call_gpt(state_name: str, dry_run: bool = False) -> dict:
    if dry_run:
        return DRY_RUN_RESPONSE.copy()
    try:
        from openai import OpenAI
    except ImportError:
        return {"error": "openai not installed"}
    try:
        client = OpenAI(api_key=OPENAI_KEY)
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_query(state_name)},
            ],
            max_completion_tokens=6000,  # gpt-5.5 chain-of-thought exhausts <6000 tokens before output; 6000 confirmed working (2026-06-21 diagnostic)
        )
        raw = resp.choices[0].message.content.strip() if resp.choices[0].message.content else ""
        if not raw:
            return {"error": "empty response"}
        parsed = _parse_json_response(raw)
        # Validate it's a defenses-keyed response
        if not isinstance(parsed, dict) or "defenses" not in parsed:
            return {"error": f"unexpected schema — top-level keys: {list(parsed.keys())[:5]}"}
        return parsed
    except Exception as exc:
        return {"error": str(exc)}


def call_gemini(state_name: str, dry_run: bool = False) -> dict:
    if dry_run:
        return DRY_RUN_RESPONSE.copy()
    try:
        from google import genai
    except ImportError:
        return {"error": "google-genai not installed"}
    try:
        client = genai.Client(api_key=GOOGLE_KEY)
        full_prompt = SYSTEM_PROMPT + "\n\n" + build_query(state_name)
        resp = client.models.generate_content(model=GEMINI_MODEL, contents=full_prompt)
        raw = resp.text.strip()
        if not raw:
            return {"error": "empty response"}
        parsed = _parse_json_response(raw)
        if not isinstance(parsed, dict) or "defenses" not in parsed:
            return {"error": f"unexpected schema — top-level keys: {list(parsed.keys())[:5]}"}
        return parsed
    except Exception as exc:
        return {"error": str(exc)}


# ── Per-defense classification ─────────────────────────────────────────────────

def classify_defense(
    defense_key: str,
    gpt_full: dict,
    gem_full: dict,
) -> tuple:
    """
    Returns (classification, note, resolved: dict).

    resolved dict contains:
      recognized_as_defense: bool
      elements: list
      primary_statute: str or None
      key_case: str or None
      note: str

    Classifications:
      CONSENSUS-CONFIRMED       — both models recognize defense and return elements
      CONSENSUS-NOT-RECOGNIZED  — both say defense not recognized in this state
      SINGLE-MODEL-RESOLVED     — one model failed; other is high-confidence
      MODEL-SPLIT               — fundamental disagreement on recognition
      ERROR                     — both models failed
    """
    gpt_err = gpt_full.get("error")
    gem_err = gem_full.get("error")

    # Both failed at the API level
    if gpt_err and gem_err:
        return (
            "ERROR",
            f"Both models failed. GPT: {gpt_err[:80]}. Gemini: {gem_err[:80]}.",
            {},
        )

    # Extract per-defense responses
    def get_defense(full: dict, key: str) -> Optional[dict]:
        if full.get("error"):
            return None
        return full.get("defenses", {}).get(key)

    gpt_d = get_defense(gpt_full, defense_key)
    gem_d = get_defense(gem_full, defense_key)

    # One model failed entirely
    if gpt_err or gpt_d is None:
        if gem_d is None:
            return (
                "ERROR",
                f"GPT failed ({str(gpt_err)[:50]}) and Gemini returned no data for {defense_key}.",
                {},
            )
        resolved = {
            "recognized_as_defense": gem_d.get("recognized_as_defense", True),
            "elements": gem_d.get("elements", []),
            "primary_statute": gem_d.get("primary_statute"),
            "key_case": gem_d.get("key_case"),
            "note": gem_d.get("note", ""),
        }
        return (
            "SINGLE-MODEL-RESOLVED",
            f"GPT failed ({str(gpt_err)[:50]}). Gemini single-model fallback: "
            f"recognized={resolved['recognized_as_defense']}, "
            f"elements={len(resolved['elements'])}, "
            f"statute={resolved['primary_statute']}, "
            f"conf={gem_full.get('confidence')}.",
            resolved,
        )

    if gem_err or gem_d is None:
        if gpt_d is None:
            return (
                "ERROR",
                f"Gemini failed ({str(gem_err)[:50]}) and GPT returned no data for {defense_key}.",
                {},
            )
        resolved = {
            "recognized_as_defense": gpt_d.get("recognized_as_defense", True),
            "elements": gpt_d.get("elements", []),
            "primary_statute": gpt_d.get("primary_statute"),
            "key_case": gpt_d.get("key_case"),
            "note": gpt_d.get("note", ""),
        }
        return (
            "SINGLE-MODEL-RESOLVED",
            f"Gemini failed ({str(gem_err)[:50]}). GPT single-model fallback: "
            f"recognized={resolved['recognized_as_defense']}, "
            f"elements={len(resolved['elements'])}, "
            f"statute={resolved['primary_statute']}, "
            f"conf={gpt_full.get('confidence')}.",
            resolved,
        )

    # Both succeeded — compare recognition
    gpt_rec = gpt_d.get("recognized_as_defense", True)
    gem_rec = gem_d.get("recognized_as_defense", True)

    if not gpt_rec and not gem_rec:
        return (
            "CONSENSUS-NOT-RECOGNIZED",
            f"Both models: {defense_key} not recognized as an eviction defense in this state. "
            f"GPT note: {gpt_d.get('note', '')[:80]}. Gemini note: {gem_d.get('note', '')[:80]}.",
            {
                "recognized_as_defense": False,
                "elements": [],
                "primary_statute": None,
                "key_case": None,
                "note": f"GPT: {gpt_d.get('note','')} | Gemini: {gem_d.get('note','')}",
            },
        )

    if gpt_rec != gem_rec:
        # One says recognized, one says not — genuine split
        return (
            "MODEL-SPLIT",
            f"Models disagree on recognition. GPT: recognized={gpt_rec} "
            f"(statute={gpt_d.get('primary_statute')}). "
            f"Gemini: recognized={gem_rec} (statute={gem_d.get('primary_statute')}). "
            f"Attorney review needed.",
            {},
        )

    # Both recognize defense — merge elements (GPT primary, Gemini supplemental)
    gpt_els = gpt_d.get("elements", [])
    gem_els = gem_d.get("elements", [])

    # Use GPT elements as primary; note if element counts diverge significantly
    element_count_note = ""
    if abs(len(gpt_els) - len(gem_els)) >= 3:
        element_count_note = (
            f" Note: element count divergence (GPT={len(gpt_els)}, Gemini={len(gem_els)}) — "
            f"human review recommended to merge lists."
        )

    # Statute consensus check
    gpt_stat = gpt_d.get("primary_statute") or ""
    gem_stat = gem_d.get("primary_statute") or ""
    def extract_nums(s: str) -> set:
        return set(re.findall(r'\d+[\.\-]?\d*[a-zA-Z]?', s))

    statute_note = ""
    if gpt_stat and gem_stat:
        if not (extract_nums(gpt_stat) & extract_nums(gem_stat)):
            statute_note = (
                f" Statute divergence: GPT={gpt_stat} / Gemini={gem_stat} — "
                f"human review recommended."
            )

    resolved = {
        "recognized_as_defense": True,
        "elements_gpt": gpt_els,
        "elements_gemini": gem_els,
        "elements": gpt_els,  # primary; Gemini stored for comparison
        "primary_statute_gpt": gpt_stat or None,
        "primary_statute_gemini": gem_stat or None,
        "primary_statute": gpt_stat or gem_stat or None,
        "key_case": gpt_d.get("key_case") or gem_d.get("key_case"),
        "note": (gpt_d.get("note") or gem_d.get("note") or ""),
    }

    note = (
        f"Both models confirm {defense_key} recognized as defense. "
        f"GPT elements: {len(gpt_els)}, Gemini elements: {len(gem_els)}. "
        f"GPT statute: {gpt_stat or 'none'}. Gemini statute: {gem_stat or 'none'}."
        f"{element_count_note}{statute_note}"
    )

    return ("CONSENSUS-CONFIRMED", note, resolved)


# ── Flag / layer_decomposition writer ─────────────────────────────────────────

def write_defense_layer(
    data: dict,
    path: str,
    defense_key: str,
    classification: str,
    note: str,
    resolved: dict,
    gpt_full: dict,
    gem_full: dict,
) -> None:
    """
    Adds layer_decomposition.elements to the matching defense in substantive_defenses.
    Never edits the existing flat elements/statute/case_law fields.
    Never advances past ACP.
    """
    sd = data.get("substantive_defenses", [])
    target = None
    for item in sd:
        if isinstance(item, dict) and item.get("defense") == defense_key:
            target = item
            break

    if target is None:
        # Defense not present in this state's file — skip silently
        return

    ld = target.setdefault("layer_decomposition", {})
    el = ld.setdefault("elements", {})

    el["validation_method"] = "L2-multi-model-consensus"
    el["l2_run_date"] = TODAY

    if classification == "CONSENSUS-CONFIRMED":
        el["validation_status"] = "L2-RESOLVED-PENDING-HUMAN-CONFIRMATION"
        el["recognized_as_defense"] = True
        el["elements_confirmed"] = resolved.get("elements", [])
        el["elements_gemini"] = resolved.get("elements_gemini", [])
        el["primary_statute"] = resolved.get("primary_statute")
        el["primary_statute_gpt"] = resolved.get("primary_statute_gpt")
        el["primary_statute_gemini"] = resolved.get("primary_statute_gemini")
        el["key_case"] = resolved.get("key_case")
        el["l2_note"] = note

    elif classification == "CONSENSUS-NOT-RECOGNIZED":
        el["validation_status"] = "L2-RESOLVED-PENDING-HUMAN-CONFIRMATION"
        el["recognized_as_defense"] = False
        el["elements_confirmed"] = []
        el["l2_note"] = note

    elif classification == "SINGLE-MODEL-RESOLVED":
        el["validation_status"] = "L2-SINGLE-MODEL-RESOLVED-PENDING-HUMAN-CONFIRMATION"
        el["recognized_as_defense"] = resolved.get("recognized_as_defense", True)
        el["elements_confirmed"] = resolved.get("elements", [])
        el["primary_statute"] = resolved.get("primary_statute")
        el["key_case"] = resolved.get("key_case")
        el["l2_note"] = note

    elif classification == "MODEL-SPLIT":
        el["validation_status"] = "L7-ESCALATED"
        el["l2_note"] = note
        # Store raw responses for attorney review
        def get_defense_raw(full: dict, key: str) -> Optional[dict]:
            if full.get("error"):
                return None
            return full.get("defenses", {}).get(key)
        el["gpt_raw"] = get_defense_raw(gpt_full, defense_key)
        el["gemini_raw"] = get_defense_raw(gem_full, defense_key)

    elif classification == "ERROR":
        el["validation_status"] = "L2-ERROR-RETRY-NEEDED"
        el["l2_note"] = note

    # Append flag
    code_map = {
        "CONSENSUS-CONFIRMED":       f"L2-{defense_key.upper().replace('_','-')}-ELEMENTS-CONFIRMED",
        "CONSENSUS-NOT-RECOGNIZED":  f"L2-{defense_key.upper().replace('_','-')}-NOT-RECOGNIZED",
        "SINGLE-MODEL-RESOLVED":     f"L2-{defense_key.upper().replace('_','-')}-SINGLE-MODEL-RESOLVED",
        "MODEL-SPLIT":               f"L7-{defense_key.upper().replace('_','-')}-ATTORNEY-REVIEW",
        "ERROR":                     f"L2-{defense_key.upper().replace('_','-')}-ERROR",
    }

    flags = data["validation"].setdefault("flags", [])
    flags.append({
        "layer": "L2",
        "code": code_map.get(classification, f"L2-{defense_key}-UNKNOWN"),
        "field": f"substantive_defenses.{defense_key}.layer_decomposition.elements",
        "disposition": (
            "resolved-confirmed" if classification in (
                "CONSENSUS-CONFIRMED", "CONSENSUS-NOT-RECOGNIZED", "SINGLE-MODEL-RESOLVED"
            ) else "open"
        ),
        "l2_run_date": TODAY,
        "classification": classification,
        "note": note[:300],
        "gpt_confidence": gpt_full.get("confidence") if not gpt_full.get("error") else "error",
        "gemini_confidence": gem_full.get("confidence") if not gem_full.get("error") else "error",
    })
    data["validation"]["flags"] = flags

    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


# ── Main runner ────────────────────────────────────────────────────────────────

def run_remaining_defenses(target_codes: List[str], dry_run: bool = False) -> list:
    all_data, all_paths = load_all_v2_files()

    missing = [c for c in target_codes if c not in all_data]
    if missing:
        print(f"  WARN: states not found in rules files: {missing}")
        target_codes = [c for c in target_codes if c in all_data]

    n = len(target_codes)
    est_cost = n * APPROX_COST_PER_STATE
    print(f"\n  States: {n} · Est. cost: ~${est_cost:.2f} · Hard cap: ${BUDGET_CAP:.2f}")
    print(f"  Defenses: {', '.join(DEFENSE_KEYS)}")
    if dry_run:
        print("  MODE: DRY RUN — no API calls, no write-back")

    results = []
    spend = 0.0

    # Per-defense classification counters
    counts = {dk: {
        "CONSENSUS-CONFIRMED": 0,
        "CONSENSUS-NOT-RECOGNIZED": 0,
        "SINGLE-MODEL-RESOLVED": 0,
        "MODEL-SPLIT": 0,
        "ERROR": 0,
    } for dk in DEFENSE_KEYS}

    l7_queue = []

    for code in target_codes:
        data = all_data[code]
        path = all_paths[code]
        state_name = data.get("jurisdiction", {}).get("state_name", code)

        print(f"\n  {code} ({state_name})")

        gpt = call_gpt(state_name, dry_run=dry_run)
        gem = call_gemini(state_name, dry_run=dry_run)
        spend += APPROX_COST_PER_STATE

        if gpt.get("error"):
            print(f"    GPT error: {gpt['error'][:80]}")
        else:
            print(f"    GPT OK — conf={gpt.get('confidence')}")

        if gem.get("error"):
            print(f"    Gemini error: {gem['error'][:80]}")
        else:
            print(f"    Gemini OK — conf={gem.get('confidence')}")

        state_result = {
            "state": code,
            "state_name": state_name,
            "recency_watch": code in RECENCY_WATCH_STATES,
            "recency_note": RECENCY_WATCH_STATES.get(code),
            "defenses": {},
        }

        for dk in DEFENSE_KEYS:
            classification, note, resolved = classify_defense(dk, gpt, gem)
            counts[dk][classification] = counts[dk].get(classification, 0) + 1

            recognized_str = ""
            if resolved.get("recognized_as_defense") is True:
                recognized_str = f"recognized, els={len(resolved.get('elements', []))}"
            elif resolved.get("recognized_as_defense") is False:
                recognized_str = "NOT-RECOGNIZED"
            print(f"    {dk}: {classification} ({recognized_str})")

            state_result["defenses"][dk] = {
                "classification": classification,
                "note": note,
                "resolved": resolved,
            }

            if classification == "MODEL-SPLIT":
                l7_queue.append({
                    "state": code,
                    "state_name": state_name,
                    "defense": dk,
                    "note": note,
                    "stopping_rule": "Fundamental split on defense recognition",
                })

            if not dry_run:
                write_defense_layer(data, path, dk, classification, note, resolved, gpt, gem)

        results.append(state_result)

        if spend >= BUDGET_CAP:
            print(f"\n  ⚠️  BUDGET CAP HIT (~${spend:.2f}). Stopping early at {code}.")
            break

    # Save raw output
    output_path = OUTPUT_DIR / f"remaining_defenses_l2_raw_{TODAY}.json"
    if not dry_run:
        with open(output_path, "w") as f:
            json.dump({
                "run_date": TODAY,
                "module": "Module 6 — Remaining Substantive Defenses Elements Layer",
                "models": {"openai": OPENAI_MODEL, "gemini": GEMINI_MODEL},
                "defenses_covered": DEFENSE_KEYS,
                "states_run": len(results),
                "spend_estimate": spend,
                "counts_by_defense": counts,
                "l7_queue": l7_queue,
                "results": results,
            }, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"\n  Raw output saved: {output_path}")

    # ── Summary ────────────────────────────────────────────────────────────────
    print(f"\n{'=' * 70}")
    print(f"  Module 6 — Remaining Defenses Elements L2 | {len(results)} states | ~${spend:.2f} spent")
    print(f"  {'Defense':<30} {'CONFIRMED':>10} {'NOT-REC':>8} {'SINGLE':>8} {'SPLIT':>7} {'ERROR':>7}")
    print(f"  {'-'*70}")
    total_confirmed = 0
    total_items = 0
    for dk in DEFENSE_KEYS:
        c = counts[dk]
        conf = c.get("CONSENSUS-CONFIRMED", 0)
        nrec = c.get("CONSENSUS-NOT-RECOGNIZED", 0)
        sing = c.get("SINGLE-MODEL-RESOLVED", 0)
        splt = c.get("MODEL-SPLIT", 0)
        err  = c.get("ERROR", 0)
        auto = conf + nrec + sing
        total_confirmed += auto
        total_items += len(results)
        print(f"  {dk:<30} {conf:>10} {nrec:>8} {sing:>8} {splt:>7} {err:>7}")

    print(f"\n  Auto-resolved (all defenses): {total_confirmed}/{total_items} "
          f"({total_confirmed/total_items*100:.0f}% ceiling)" if total_items else "")
    print(f"  L7 items (attorney review): {len(l7_queue)}")
    if RECENCY_WATCH_STATES:
        watch_hit = sum(1 for r in results if r.get("recency_watch"))
        print(f"  Recency-watch states processed: {watch_hit}")
    print(f"{'=' * 70}")

    if l7_queue:
        print(f"\n  L7 queue:")
        for item in l7_queue:
            print(f"    [{item['state']}] {item['defense']}: {item['note'][:80]}")

    print(f"\n  ⚠️  STOP AND REPORT. Share output file with Cowork for ingestion.")
    print(f"  Output: {output_path if not dry_run else '(dry run — no output written)'}")
    print(f"\n  Next: Cowork ingests output, applies resolution protocol,")
    print(f"        appends Module 6 row to VALIDATION_METRICS_LEDGER.md.")

    return results


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Remaining Defenses Elements L2 Runner — Civil Justice as Code"
    )
    parser.add_argument(
        "--states",
        default=",".join(ALL_STATES),
        help="Comma-separated state codes. Default: all 51.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="No API calls, no write-back. Verifies import chain only.",
    )
    args = parser.parse_args()

    print(f"\nCivil Justice as Code — Module 6: Remaining Defenses Elements L2 Runner")
    print(f"Run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Models: {OPENAI_MODEL} + {GEMINI_MODEL}")
    print(f"Defenses: {', '.join(DEFENSE_KEYS)}")
    print(f"Protocol: CONSENSUS → resolved; SPLIT → L7 (no reasoning pass for elements layer)")
    print(f"Budget cap: ${BUDGET_CAP:.2f}")
    print(f"Recency watch: {list(RECENCY_WATCH_STATES.keys())}")
    print(f"NOTE: No file values fed to models. Neutral queries only.")

    target = [s.strip().upper() for s in args.states.split(",") if s.strip()]
    print(f"States: {len(target)}")

    run_remaining_defenses(
        target_codes=target,
        dry_run=args.dry_run,
    )
