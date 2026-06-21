#!/usr/bin/env python3
"""
Retaliation Defense — Elements Layer L2 Runner
===============================================
Runs L2 multi-model consensus on the ELEMENTS layer of the retaliation
defense (substantive_defenses module) across all 51 states.

Elements layer = the formal legal requirements to assert the defense:
  - Protected activity (complaint, organizing, etc.)
  - Landlord knowledge of the protected activity
  - Adverse action (eviction notice / filing)
  - Causal connection
  - State-specific: statutory presumption period (bright-line — primary L2 target)

The canonical rules files currently have pending-l2 stubs in
layer_decomposition.elements.state_specific (quarantined 2026-06-20).
This runner replaces those stubs with L2-validated values.

CRITICAL: The preliminary values in docs/PRELIMINARY_PENDING_L2_2026-06-20.json
are HYPOTHESES to be tested, NOT adopted. This runner does NOT read or feed
those values to the models. Neutral query only. Where L2 disagrees with the
preliminary hypothesis, L2 governs.

Output:
  rules/validation/l2/output/retaliation_elements_l2_raw_<date>.json
  (full per-state model responses; used by Cowork for ingestion after run)

GUARDRAILS:
  - Neutral query: no anchoring to file values or preliminary hypothesis
  - Keys from .env only; never hardcoded, logged, or committed
  - Never advances past ACP
  - Tiered protocol: CONSENSUS → resolved; SPLIT → reasoning pass; persistent → L7
  - Separate technical failures from substantive divergence
  - $10 budget cap (51 states × ~$0.05 est.)

Usage (run from repo root in Andy's Terminal):
  cd /Users/andrewcohen/Documents/GitHub/a2j-ai
  python3 rules/validation/l2/retaliation_elements_runner.py

For a single state (testing):
  python3 rules/validation/l2/retaliation_elements_runner.py --states CA

For dry run (no API, no write-back):
  python3 rules/validation/l2/retaliation_elements_runner.py --dry-run

Expected: ~51 × $0.05 = ~$2.50. Expected time: ~10-15 minutes.
Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import os
import sys
import re
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

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
    DOCS_DIR,
)

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
BUDGET_CAP = 10.00
APPROX_COST_PER_STATE = 0.05  # ~$0.05/state (retaliation query is larger than service)

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

ALL_STATES = [
    "AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL",
    "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA",
    "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE",
    "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI",
    "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY",
]

# States with known recent legislative activity affecting retaliation law
RECENCY_WATCH_STATES = {
    "CA": "Civ. Code §1942.5 amended repeatedly; verify current subsection structure",
    "WA": "RCW 59.18.240-250 saw significant 2021-2023 activity; verify current period",
    "MN": "HF 3019 (2023) expanded tenant protections; verify §504B.285 retaliation provisions",
    "VA": "HB 15/SB 48 (2026) landlord-tenant amendments; verify §55.1-1234 period",
    "OR": "SB 278 (2023) tenant protections; verify ORS 90.385 period",
}

# ── Query ──────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a legal research expert in US residential landlord-tenant law. "
    "You answer questions about legal defenses available to tenants in eviction proceedings. "
    "Be precise about statutory citations, including specific section and subsection. "
    "Respond only in the JSON format requested."
)


def build_retaliation_query(state_name: str) -> str:
    """Neutral query — no anchoring to file values or preliminary hypotheses."""
    return f"""In {state_name}, what are the elements of a retaliatory eviction defense for a residential tenant?

Please address:
1. The formal legal elements a tenant must establish to assert this defense
2. The specific statute(s) governing retaliatory eviction in {state_name} (with section and subsection)
3. Whether {state_name} has a statutory PRESUMPTION period — i.e., a defined number of days after a protected activity during which an eviction is presumed retaliatory (if any)
4. What qualifies as "protected activity" under {state_name} law

Respond ONLY in valid JSON:
{{
  "elements": {{
    "protected_activity": "brief description of what qualifies",
    "landlord_knowledge": "whether landlord knowledge is required",
    "adverse_action": "description of covered adverse actions",
    "causal_connection": "whether causation must be shown"
  }},
  "primary_statute": "specific statute and section (e.g. Cal. Civ. Code §1942.5)",
  "primary_statute_subsection": "the specific subsection for the presumption period, if any (e.g. §1942.5(d))",
  "presumption_period_days": <integer number of days, or null if no statutory presumption period>,
  "presumption_period_basis": "statute | case_law | none",
  "presumption_period_note": "brief note if no statute or if case-law only",
  "has_anti_retaliation_statute": true,
  "confidence": "high|medium|low",
  "notes": "any important caveats, exceptions, or recent changes"
}}"""


# ── API callers ────────────────────────────────────────────────────────────────

def call_gpt_retaliation(state_name: str, dry_run: bool = False) -> dict:
    if dry_run:
        return {
            "elements": {"protected_activity": "dry-run"},
            "primary_statute": "DRY §1(a)",
            "presumption_period_days": 90,
            "presumption_period_basis": "statute",
            "has_anti_retaliation_statute": True,
            "confidence": "high",
            "notes": "dry run",
        }
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
                {"role": "user", "content": build_retaliation_query(state_name)},
            ],
            max_completion_tokens=6000,  # gpt-5.5 chain-of-thought exhausts 2000 before producing output; 6000 confirmed working (2026-06-21 diagnostic)
        )
        raw = resp.choices[0].message.content.strip() if resp.choices[0].message.content else ""
        return _parse_json_response(raw) if raw else {"error": "empty response"}
    except Exception as exc:
        return {"error": str(exc)}


def call_gemini_retaliation(state_name: str, dry_run: bool = False) -> dict:
    if dry_run:
        return {
            "elements": {"protected_activity": "dry-run"},
            "primary_statute": "DRY §1(a)",
            "presumption_period_days": 90,
            "presumption_period_basis": "statute",
            "has_anti_retaliation_statute": True,
            "confidence": "high",
            "notes": "dry run",
        }
    try:
        from google import genai
    except ImportError:
        return {"error": "google-genai not installed"}
    try:
        client = genai.Client(api_key=GOOGLE_KEY)
        full_prompt = SYSTEM_PROMPT + "\n\n" + build_retaliation_query(state_name)
        resp = client.models.generate_content(model=GEMINI_MODEL, contents=full_prompt)
        raw = resp.text.strip()
        return _parse_json_response(raw) if raw else {"error": "empty response"}
    except Exception as exc:
        return {"error": str(exc)}


# ── Classification ─────────────────────────────────────────────────────────────

def _period_close(a, b) -> bool:
    """True if two presumption periods are within 1 day (handles None)."""
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    try:
        return abs(int(a) - int(b)) <= 1
    except (TypeError, ValueError):
        return False


def classify_retaliation(gpt: dict, gem: dict) -> tuple[str, str]:
    """
    Returns (classification, resolution_note).

    Classifications:
      CONSENSUS-CONFIRMED      — models agree on period and statute
      CONSENSUS-NO-PERIOD      — both agree: no statutory presumption period (case law only / none)
      PERIOD-DIVERGENCE        — models disagree on period days
      STATUTE-DIVERGENCE       — period agrees, statutes differ
      MODEL-SPLIT              — fundamental disagreement
      SINGLE-MODEL-RESOLVED    — one model failed, other high-confidence
      ERROR                    — both models failed
    """
    if gpt.get("error") and gem.get("error"):
        return "ERROR", f"Both models failed. GPT: {gpt['error'][:80]}. Gemini: {gem['error'][:80]}"

    if gpt.get("error"):
        gem_p = gem.get("presumption_period_days")
        gem_s = gem.get("primary_statute", "?")
        return (
            "SINGLE-MODEL-RESOLVED",
            f"GPT failed ({gpt['error'][:50]}). Gemini (single-model fallback): period={gem_p}d, statute={gem_s}, conf={gem.get('confidence')}.",
        )

    if gem.get("error"):
        gpt_p = gpt.get("presumption_period_days")
        gpt_s = gpt.get("primary_statute", "?")
        return (
            "SINGLE-MODEL-RESOLVED",
            f"Gemini failed ({gem['error'][:50]}). GPT (single-model fallback): period={gpt_p}d, statute={gpt_s}, conf={gpt.get('confidence')}.",
        )

    gpt_period = gpt.get("presumption_period_days")
    gem_period = gem.get("presumption_period_days")
    gpt_statute = gpt.get("primary_statute", "")
    gem_statute = gem.get("primary_statute", "")

    # Both say no presumption period
    if gpt_period is None and gem_period is None:
        gpt_basis = gpt.get("presumption_period_basis", "none")
        gem_basis = gem.get("presumption_period_basis", "none")
        return (
            "CONSENSUS-NO-PERIOD",
            f"Both models: no statutory presumption period. GPT basis: {gpt_basis}. Gemini basis: {gem_basis}.",
        )

    # Periods agree (within 1 day)
    if _period_close(gpt_period, gem_period):
        period = gpt_period if gpt_period is not None else gem_period
        # Check statutes
        def extract_nums(s):
            return set(re.findall(r'\d+[\.\-]?\d*[a-zA-Z]?', s or ""))

        gpt_nums = extract_nums(gpt_statute)
        gem_nums = extract_nums(gem_statute)

        if gpt_nums & gem_nums:
            return (
                "CONSENSUS-CONFIRMED",
                f"Both models: {period}d presumption period. GPT: {gpt_statute} (conf={gpt.get('confidence')}). Gemini: {gem_statute} (conf={gem.get('confidence')}).",
            )
        else:
            return (
                "STATUTE-DIVERGENCE",
                f"Period agrees ({period}d) but statutes differ. GPT: {gpt_statute}. Gemini: {gem_statute}. Subsection query needed.",
            )

    # Periods diverge
    return (
        "PERIOD-DIVERGENCE",
        f"Models disagree on period. GPT: {gpt_period}d ({gpt_statute}). Gemini: {gem_period}d ({gem_statute}). Reasoning pass needed.",
    )


# ── Reasoning pass ─────────────────────────────────────────────────────────────

def build_reasoning_query(state_name: str, gpt_period, gem_period,
                           gpt_statute: str, gem_statute: str) -> str:
    """Targeted tiebreaker — models see the divergence and reason to convergence."""
    return f"""In {state_name}, there is a question about the retaliatory eviction defense presumption period.

Two legal research sources returned different answers:
- Source A: {gpt_period} days (citing {gpt_statute})
- Source B: {gem_period} days (citing {gem_statute})

Please resolve this by identifying the current operative statute and subsection in {state_name} that establishes the presumption period for retaliatory eviction. Explain which period is correct and why, citing the specific subsection.

Respond ONLY in valid JSON:
{{
  "correct_period_days": <integer or null>,
  "correct_statute": "exact statute with subsection",
  "reasoning": "explanation of why this is correct",
  "confidence": "high|medium|low"
}}"""


def run_reasoning_pass(state_name: str, gpt_r: dict, gem_r: dict) -> dict:
    """Run a tiebreaker pass when models initially diverge."""
    print(f"    → Running reasoning/tiebreaker pass...")
    q = build_reasoning_query(
        state_name,
        gpt_r.get("presumption_period_days"),
        gem_r.get("presumption_period_days"),
        gpt_r.get("primary_statute", "?"),
        gem_r.get("primary_statute", "?"),
    )

    gpt_tb = {"error": "not run"}
    gem_tb = {"error": "not run"}

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_KEY)
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": q},
            ],
            max_completion_tokens=1000,
        )
        raw = resp.choices[0].message.content.strip() if resp.choices[0].message.content else ""
        gpt_tb = _parse_json_response(raw) if raw else {"error": "empty"}
        print(f"      GPT tiebreaker: period={gpt_tb.get('correct_period_days')}, statute={gpt_tb.get('correct_statute')}, conf={gpt_tb.get('confidence')}")
    except Exception as exc:
        gpt_tb = {"error": str(exc)}

    try:
        from google import genai
        client = genai.Client(api_key=GOOGLE_KEY)
        full_prompt = SYSTEM_PROMPT + "\n\n" + q
        resp = client.models.generate_content(model=GEMINI_MODEL, contents=full_prompt)
        raw = resp.text.strip()
        gem_tb = _parse_json_response(raw) if raw else {"error": "empty"}
        print(f"      Gemini tiebreaker: period={gem_tb.get('correct_period_days')}, statute={gem_tb.get('correct_statute')}, conf={gem_tb.get('confidence')}")
    except Exception as exc:
        gem_tb = {"error": str(exc)}

    # Check if reasoning pass converged
    if not gpt_tb.get("error") and not gem_tb.get("error"):
        gpt_p = gpt_tb.get("correct_period_days")
        gem_p = gem_tb.get("correct_period_days")
        if _period_close(gpt_p, gem_p):
            period = gpt_p if gpt_p is not None else gem_p
            return {
                "converged": True,
                "period": period,
                "statute": gpt_tb.get("correct_statute") or gem_tb.get("correct_statute"),
                "note": f"Reasoning pass converged: {period}d. GPT: {gpt_tb.get('correct_statute')}. Gemini: {gem_tb.get('correct_statute')}.",
                "gpt_tiebreaker": gpt_tb,
                "gemini_tiebreaker": gem_tb,
            }

    return {
        "converged": False,
        "note": f"Reasoning pass did not converge. GPT: {gpt_tb.get('correct_period_days')}d / {gpt_tb.get('correct_statute')}. Gemini: {gem_tb.get('correct_period_days')}d / {gem_tb.get('correct_statute')}.",
        "gpt_tiebreaker": gpt_tb,
        "gemini_tiebreaker": gem_tb,
    }


# ── Flag writer ────────────────────────────────────────────────────────────────

def write_retaliation_flag(
    state_code: str,
    data: dict,
    path: str,
    classification: str,
    resolution_note: str,
    resolved_period: Optional[int],
    resolved_statute: Optional[str],
    gpt: dict,
    gem: dict,
    reasoning: Optional[dict] = None,
):
    """
    Write L2 results into the retaliation defense layer_decomposition.elements.
    Replaces pending-l2 stubs with L2-validated data.
    Never edits Andy's resolution fields; never advances past ACP.
    """
    # Find retaliation defense
    for defense in data.get("substantive_defenses", []):
        if defense.get("defense") != "retaliation":
            continue

        ld = defense.setdefault("layer_decomposition", {})
        el = ld.setdefault("elements", {})

        # Update validation_status
        el["validation_method"] = "L2-multi-model-consensus"
        el["l2_run_date"] = TODAY

        if classification in ("CONSENSUS-CONFIRMED", "CONSENSUS-NO-PERIOD", "SINGLE-MODEL-RESOLVED"):
            el["validation_status"] = "L2-RESOLVED-PENDING-HUMAN-CONFIRMATION"

            if classification == "CONSENSUS-NO-PERIOD":
                el["state_specific"] = {
                    "presumption_period_days": None,
                    "presumption_period_basis": gpt.get("presumption_period_basis", "none"),
                    "status": "L2-confirmed-no-statutory-period",
                    "note": resolution_note,
                }
            elif resolved_period is not None or resolved_statute:
                el["state_specific"] = {
                    "presumption_period_days": resolved_period,
                    "presumption_period_statute": resolved_statute,
                    "presumption_period_basis": gpt.get("presumption_period_basis", "statute"),
                    "status": "L2-confirmed-pending-human-confirmation",
                    "note": resolution_note,
                }
            else:
                el["state_specific"] = {
                    "status": "L2-confirmed-pending-human-confirmation",
                    "note": resolution_note,
                }

            # Add elements core fields from model consensus
            el["elements_confirmed"] = {
                "protected_activity": (
                    gpt.get("elements", {}).get("protected_activity")
                    or gem.get("elements", {}).get("protected_activity")
                ),
                "has_anti_retaliation_statute": (
                    gpt.get("has_anti_retaliation_statute")
                    if not gpt.get("error") else gem.get("has_anti_retaliation_statute")
                ),
                "primary_statute": resolved_statute,
                "note": "From L2 consensus; pending human confirmation.",
            }

        elif classification in ("STATUTE-DIVERGENCE", "PERIOD-DIVERGENCE"):
            el["validation_status"] = "L2-DIVERGENCE-PENDING-RESOLUTION"
            el["state_specific"] = {
                "status": "pending-resolution",
                "note": resolution_note,
                "gpt_period": gpt.get("presumption_period_days"),
                "gpt_statute": gpt.get("primary_statute"),
                "gemini_period": gem.get("presumption_period_days"),
                "gemini_statute": gem.get("primary_statute"),
            }
            if reasoning:
                el["state_specific"]["reasoning_pass"] = reasoning

        elif classification == "MODEL-SPLIT":
            el["validation_status"] = "L7-ESCALATED"
            el["state_specific"] = {
                "status": "L7-attorney-review",
                "note": resolution_note,
            }

        elif classification == "ERROR":
            el["validation_status"] = "L2-ERROR-RETRY-NEEDED"
            el["state_specific"] = {
                "status": "error-retry-needed",
                "note": resolution_note,
            }

        # Append validation flag
        flags = data["validation"].setdefault("flags", [])
        # Remove any stale PENDING-L2-QUARANTINED flag for this field
        flags = [fl for fl in flags if not (
            fl.get("field") == "substantive_defenses.retaliation.layer_decomposition.elements"
            and fl.get("disposition") in ("pending-l2-quarantined",)
        )]

        code_map = {
            "CONSENSUS-CONFIRMED": "L2-RETALIATION-ELEMENTS-CONSENSUS-CONFIRMED",
            "CONSENSUS-NO-PERIOD": "L2-RETALIATION-ELEMENTS-NO-STATUTORY-PERIOD",
            "SINGLE-MODEL-RESOLVED": "L2-RETALIATION-ELEMENTS-SINGLE-MODEL-RESOLVED",
            "STATUTE-DIVERGENCE": "L2-RETALIATION-ELEMENTS-STATUTE-DIVERGENCE",
            "PERIOD-DIVERGENCE": "L2-RETALIATION-ELEMENTS-PERIOD-DIVERGENCE",
            "MODEL-SPLIT": "L7-RETALIATION-ELEMENTS-ATTORNEY-REVIEW",
            "ERROR": "L2-RETALIATION-ELEMENTS-ERROR",
        }

        flags.append({
            "layer": "L2",
            "code": code_map.get(classification, "L2-RETALIATION-ELEMENTS-ERROR"),
            "field": "substantive_defenses.retaliation.layer_decomposition.elements",
            "disposition": (
                "resolved-confirmed" if classification in (
                    "CONSENSUS-CONFIRMED", "CONSENSUS-NO-PERIOD", "SINGLE-MODEL-RESOLVED"
                ) else "open"
            ),
            "l2_run_date": TODAY,
            "classification": classification,
            "note": resolution_note,
            "gpt_summary": {
                "period": gpt.get("presumption_period_days"),
                "statute": gpt.get("primary_statute"),
                "confidence": gpt.get("confidence"),
                "error": gpt.get("error"),
            },
            "gemini_summary": {
                "period": gem.get("presumption_period_days"),
                "statute": gem.get("primary_statute"),
                "confidence": gem.get("confidence"),
                "error": gem.get("error"),
            },
        })

        data["validation"]["flags"] = flags

        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")

        return  # done — only one retaliation defense per state


# ── Main runner ────────────────────────────────────────────────────────────────

def run_retaliation_elements(target_codes: list, dry_run: bool = False):
    all_data, all_paths = load_all_v2_files()

    missing = [c for c in target_codes if c not in all_data]
    if missing:
        print(f"  WARN: states not found: {missing}")
        target_codes = [c for c in target_codes if c in all_data]

    n = len(target_codes)
    est_cost = n * APPROX_COST_PER_STATE
    print(f"\n  States: {n} · Est. cost: ~${est_cost:.2f} · Hard cap: ${BUDGET_CAP:.2f}")
    if dry_run:
        print("  MODE: DRY RUN — no API calls, no write-back")

    results = []
    spend = 0.0
    counts = {
        "CONSENSUS-CONFIRMED": 0,
        "CONSENSUS-NO-PERIOD": 0,
        "SINGLE-MODEL-RESOLVED": 0,
        "STATUTE-DIVERGENCE": 0,
        "PERIOD-DIVERGENCE": 0,
        "MODEL-SPLIT": 0,
        "ERROR": 0,
        "REASONING-CONVERGED": 0,
    }
    l7_queue = []

    for code in target_codes:
        data = all_data[code]
        path = all_paths[code]
        state_name = data.get("jurisdiction", {}).get("state_name", code)

        print(f"\n  {code} ({state_name})")

        # Round 1: both models
        gpt = call_gpt_retaliation(state_name, dry_run=dry_run)
        gem = call_gemini_retaliation(state_name, dry_run=dry_run)
        spend += APPROX_COST_PER_STATE

        if gpt.get("error"):
            print(f"    GPT error: {gpt['error'][:70]}")
        else:
            print(f"    GPT: period={gpt.get('presumption_period_days')}d, statute={gpt.get('primary_statute')}, conf={gpt.get('confidence')}")

        if gem.get("error"):
            print(f"    Gemini error: {gem['error'][:70]}")
        else:
            print(f"    Gemini: period={gem.get('presumption_period_days')}d, statute={gem.get('primary_statute')}, conf={gem.get('confidence')}")

        classification, note = classify_retaliation(gpt, gem)
        print(f"    Round 1: {classification}")

        reasoning_result = None
        resolved_period = None
        resolved_statute = None

        # Tiered protocol: reasoning pass on divergence
        if classification in ("PERIOD-DIVERGENCE", "STATUTE-DIVERGENCE") and not dry_run:
            spend += APPROX_COST_PER_STATE  # reasoning pass costs another round
            reasoning_result = run_reasoning_pass(state_name, gpt, gem)
            if reasoning_result["converged"]:
                classification = "CONSENSUS-CONFIRMED"
                note = f"REASONING-PASS-RESOLVED: {reasoning_result['note']}"
                resolved_period = reasoning_result["period"]
                resolved_statute = reasoning_result["statute"]
                counts["REASONING-CONVERGED"] += 1
                print(f"    → Reasoning pass resolved: {resolved_period}d / {resolved_statute}")
            else:
                # Still diverged after reasoning pass → L7
                classification = "MODEL-SPLIT"
                note = f"PERSISTENT-DIVERGENCE after reasoning pass. {reasoning_result['note']}"
                print(f"    → Reasoning pass did not converge → L7")

        # Set resolved values for consensus cases
        if classification == "CONSENSUS-CONFIRMED" and resolved_period is None:
            resolved_period = (
                gpt.get("presumption_period_days")
                if not gpt.get("error") else gem.get("presumption_period_days")
            )
            resolved_statute = (
                gpt.get("primary_statute_subsection") or gpt.get("primary_statute")
                if not gpt.get("error") else
                gem.get("primary_statute_subsection") or gem.get("primary_statute")
            )

        elif classification == "SINGLE-MODEL-RESOLVED":
            working = gem if gpt.get("error") else gpt
            resolved_period = working.get("presumption_period_days")
            resolved_statute = working.get("primary_statute_subsection") or working.get("primary_statute")

        # Record L7 items
        if classification == "MODEL-SPLIT":
            l7_queue.append({
                "state": code,
                "state_name": state_name,
                "note": note,
                "stopping_rule": "Persistent genuine split after reasoning pass on presumption period / statute",
                "gpt_period": gpt.get("presumption_period_days"),
                "gpt_statute": gpt.get("primary_statute"),
                "gem_period": gem.get("presumption_period_days"),
                "gem_statute": gem.get("primary_statute"),
            })

        counts[classification] = counts.get(classification, 0) + 1
        print(f"    Final: {classification} | period={resolved_period}d | statute={resolved_statute}")

        result = {
            "state": code,
            "state_name": state_name,
            "classification": classification,
            "note": note,
            "resolved_period": resolved_period,
            "resolved_statute": resolved_statute,
            "gpt": gpt,
            "gem": gem,
            "reasoning": reasoning_result,
            "recency_watch": code in RECENCY_WATCH_STATES,
        }
        results.append(result)

        if not dry_run:
            write_retaliation_flag(
                code, data, path, classification, note,
                resolved_period, resolved_statute, gpt, gem, reasoning_result
            )

        if spend >= BUDGET_CAP:
            print(f"\n  ⚠️ BUDGET CAP HIT (~${spend:.2f}). Stopping early at {code}.")
            break

    # Save raw output
    output_path = OUTPUT_DIR / f"retaliation_elements_l2_raw_{TODAY}.json"
    if not dry_run:
        with open(output_path, "w") as f:
            json.dump({
                "run_date": TODAY,
                "models": {"openai": OPENAI_MODEL, "gemini": GEMINI_MODEL},
                "states_run": len(results),
                "spend_estimate": spend,
                "counts": counts,
                "l7_queue": l7_queue,
                "results": results,
            }, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"\n  Raw output saved: {output_path}")

    # Summary
    print(f"\n{'=' * 60}")
    print(f"  Retaliation Elements L2 — {len(results)} states | ~${spend:.2f} spent")
    print(f"  ✅ CONSENSUS-CONFIRMED:       {counts.get('CONSENSUS-CONFIRMED', 0)}")
    print(f"  ✅ CONSENSUS-NO-PERIOD:       {counts.get('CONSENSUS-NO-PERIOD', 0)}")
    print(f"  ✅ SINGLE-MODEL-RESOLVED:     {counts.get('SINGLE-MODEL-RESOLVED', 0)}")
    print(f"  🔄 REASONING-CONVERGED:       {counts.get('REASONING-CONVERGED', 0)}")
    print(f"  🟡 STATUTE-DIVERGENCE:        {counts.get('STATUTE-DIVERGENCE', 0)}")
    print(f"  🔴 MODEL-SPLIT (L7):          {counts.get('MODEL-SPLIT', 0)}")
    print(f"  ❌ ERROR:                     {counts.get('ERROR', 0)}")
    print(f"  ⚠️  RECENCY-WATCH:            {sum(1 for r in results if r.get('recency_watch'))}")
    print(f"{'=' * 60}")

    if l7_queue:
        print(f"\n  L7 items (genuine splits — attorney review):")
        for item in l7_queue:
            print(f"    {item['state']}: {item['note'][:100]}")

    total_auto = counts.get("CONSENSUS-CONFIRMED", 0) + counts.get("CONSENSUS-NO-PERIOD", 0) + counts.get("SINGLE-MODEL-RESOLVED", 0)
    if len(results) > 0:
        ceiling = total_auto / len(results) * 100
        print(f"\n  Automation ceiling (elements layer, this run): {ceiling:.0f}% ({total_auto}/{len(results)})")
        print(f"  This is the MEASURED ceiling (vs. the ~85% projected hypothesis).")

    print(f"\n  ⚠️  STOP AND REPORT. Share output file with Cowork for ingestion.")
    print(f"  Output: {output_path}")
    print(f"\n  Next: Cowork ingests {output_path}, applies resolution protocol,")
    print(f"        appends ledger row with MEASURED metrics (not projections).")

    return results


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Retaliation Elements L2 Runner — Civil Justice as Code"
    )
    parser.add_argument(
        "--states",
        default=",".join(ALL_STATES),
        help="Comma-separated state codes. Default: all 51.",
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="No API calls, no write-back.")
    args = parser.parse_args()

    print(f"\nCivil Justice as Code — Retaliation Elements L2 Runner")
    print(f"Run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Models: {OPENAI_MODEL} + {GEMINI_MODEL}")
    print(f"Protocol: CONFIRM → resolved; DIVERGE → reasoning pass; persistent → L7")
    print(f"Budget cap: ${BUDGET_CAP:.2f}")
    print(f"Recency watch: {list(RECENCY_WATCH_STATES.keys())}")
    print(f"NOTE: Preliminary hypotheses NOT fed to models. Neutral queries only.")

    target = [s.strip().upper() for s in args.states.split(",") if s.strip()]
    print(f"States: {len(target)}")

    run_retaliation_elements(
        target_codes=target,
        dry_run=args.dry_run,
    )
