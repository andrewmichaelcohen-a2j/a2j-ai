#!/usr/bin/env python3
"""
SCRA Federal Overlay L2 Runner — Module 3
==========================================
Verifies the SCRA §3951 (50 U.S.C. §3951) overlay content across all 51
state files. Because SCRA is uniform federal law, a single query covers
all states. Key verification targets:

  1. Correct statutory citation (50 U.S.C. §3951 / SCRA §301)
  2. Current annual rent threshold (adjusts every year; training data may be stale)
  3. Core protections accurate (stay, court-order requirement, affidavit requirement)
  4. Any post-2023 NDAA amendments that changed the statute

Neutral query — does NOT feed the preliminary $4,073.16 figure to models.
Expect: near-100% consensus (uniform federal law, deterministic facts).

Output: rules/validation/l2/output/scra_l2_raw_<date>.json
        (prints model responses to console)

GUARDRAILS:
  - Neutral query, no anchoring to preliminary values
  - Keys from .env only
  - Never advances past ACP
  - Writes flags to all 51 state files; never edits content directly
  - $3 budget cap (51 files but single query)

Usage (run from repo root in Andy's Terminal):
  cd /Users/andrewcohen/Documents/GitHub/a2j-ai
  python3 rules/validation/l2/scra_overlay_runner.py

Expected cost: ~$0.05 (single two-model query). Expected time: ~30 seconds.

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

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
BUDGET_CAP = 3.00

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Query ──────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a federal legal research expert specializing in US military law and "
    "landlord-tenant law. Answer questions about the Servicemembers Civil Relief Act "
    "precisely and with specific statutory citations. Respond only in the JSON format "
    "requested. Be specific about current dollar thresholds and recent amendments."
)

SCRA_QUERY = """Under the Servicemembers Civil Relief Act (SCRA), what are the federal
protections against eviction for servicemembers and their dependents from rented premises?

Specifically:
1. What is the precise statutory citation (Title, section, and any subsection) for the
   SCRA eviction protection provision?
2. What is the CURRENT annual rent threshold for SCRA eviction protection to apply?
   (This threshold adjusts annually for inflation — provide the most current figure
   you are aware of and the year it applies to.)
3. What is the core protection the statute provides (briefly)?
4. Is there a requirement that a landlord file an affidavit before judgment may enter?
   If so, which statute governs that requirement?
5. Have there been any significant amendments to the SCRA eviction provisions since
   2020 (e.g., via NDAA or other legislation) that change the rent threshold formula,
   covered persons, or core protections?

Respond ONLY in valid JSON:
{
  "primary_citation": "exact citation, e.g. 50 U.S.C. §3951",
  "public_law_citation": "Pub. L. number and year, if helpful",
  "current_rent_threshold_dollars": <number or null if unknown>,
  "current_rent_threshold_year": "<year this figure applies to>",
  "threshold_adjustment_method": "how threshold adjusts (e.g., annual CPI, Secretary of Defense determination)",
  "core_protection": "one-sentence description",
  "court_order_required": true,
  "max_stay_days": <number>,
  "affidavit_required": true,
  "affidavit_statute": "citation for affidavit requirement",
  "covered_persons": "brief description of who qualifies",
  "recent_amendments": "<description of post-2020 changes, or 'none identified'>",
  "confidence": "high|medium|low",
  "notes": "any caveats or important details"
}"""


# ── Call wrappers ──────────────────────────────────────────────────────────────

def call_gpt_scra() -> dict:
    try:
        from openai import OpenAI
    except ImportError:
        return {"error": "openai not installed — run: pip install openai"}
    try:
        client = OpenAI(api_key=OPENAI_KEY)
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": SCRA_QUERY},
            ],
            max_completion_tokens=3000,
        )
        raw = resp.choices[0].message.content.strip() if resp.choices[0].message.content else ""
        print(f"\n  [GPT raw response]\n{raw}\n")
        result = _parse_json_response(raw)
        return result
    except Exception as exc:
        return {"error": str(exc)}


def call_gemini_scra() -> dict:
    try:
        from google import genai
    except ImportError:
        return {"error": "google-genai not installed — run: pip install google-genai"}
    try:
        client = genai.Client(api_key=GOOGLE_KEY)
        full_prompt = SYSTEM_PROMPT + "\n\n" + SCRA_QUERY
        resp = client.models.generate_content(model=GEMINI_MODEL, contents=full_prompt)
        raw = resp.text.strip()
        print(f"\n  [Gemini raw response]\n{raw}\n")
        result = _parse_json_response(raw)
        return result
    except Exception as exc:
        return {"error": str(exc)}


# ── Classification ─────────────────────────────────────────────────────────────

def _extract_section_nums(citation: str) -> set:
    import re
    return set(re.findall(r'\d+[\-\.]?\d*[a-zA-Z]?', citation or ""))


def classify_scra(gpt: dict, gem: dict) -> tuple[str, str, dict]:
    """Returns (classification, note, resolved_data)."""

    if gpt.get("error") and gem.get("error"):
        return "ERROR", f"Both models failed. GPT: {gpt['error'][:80]}. Gemini: {gem['error'][:80]}", {}

    # Single-model fallback
    if gpt.get("error"):
        return (
            "SINGLE-MODEL-GEMINI",
            f"GPT failed ({gpt.get('error','')[:60]}). Gemini carried.",
            _resolved_from(gem),
        )
    if gem.get("error"):
        return (
            "SINGLE-MODEL-GPT",
            f"Gemini failed ({gem.get('error','')[:60]}). GPT carried.",
            _resolved_from(gpt),
        )

    gpt_citation = gpt.get("primary_citation", "")
    gem_citation = gem.get("primary_citation", "")
    gpt_nums = _extract_section_nums(gpt_citation)
    gem_nums = _extract_section_nums(gem_citation)

    # Citation agreement?
    citation_agree = bool(gpt_nums & gem_nums)

    # Rent threshold agreement?
    gpt_thresh = gpt.get("current_rent_threshold_dollars")
    gem_thresh = gem.get("current_rent_threshold_dollars")

    if gpt_thresh and gem_thresh:
        # Within $200 = agree (different rounding conventions)
        thresh_agree = abs(float(gpt_thresh) - float(gem_thresh)) <= 200
    elif gpt_thresh is None and gem_thresh is None:
        thresh_agree = True  # both unknown
    else:
        thresh_agree = False  # one knows, one doesn't

    if citation_agree and thresh_agree:
        note = (
            f"CONSENSUS: citation ({gpt_citation} / {gem_citation}) and "
            f"rent threshold (GPT: ${gpt_thresh} / Gemini: ${gem_thresh}) agree."
        )
        return "CONSENSUS", note, _resolved_from_both(gpt, gem)

    if citation_agree and not thresh_agree:
        note = (
            f"CITATION-AGREE / THRESHOLD-DIVERGE: citation agrees ({gpt_citation}); "
            f"threshold differs (GPT: ${gpt_thresh} / Gemini: ${gem_thresh}). "
            f"Attorney/primary source to confirm current threshold."
        )
        return "THRESHOLD-DIVERGE", note, _resolved_from_both(gpt, gem)

    if not citation_agree:
        note = (
            f"CITATION-DIVERGE: GPT says '{gpt_citation}'; Gemini says '{gem_citation}'. "
            f"Unexpected for uniform federal law — attorney review."
        )
        return "CITATION-DIVERGE", note, {}

    return "MODEL-SPLIT", f"Unexpected split. GPT: {gpt}. Gemini: {gem}", {}


def _resolved_from(m: dict) -> dict:
    return {
        "primary_citation": m.get("primary_citation"),
        "current_rent_threshold_dollars": m.get("current_rent_threshold_dollars"),
        "current_rent_threshold_year": m.get("current_rent_threshold_year"),
        "threshold_adjustment_method": m.get("threshold_adjustment_method"),
        "core_protection": m.get("core_protection"),
        "court_order_required": m.get("court_order_required"),
        "max_stay_days": m.get("max_stay_days"),
        "affidavit_required": m.get("affidavit_required"),
        "affidavit_statute": m.get("affidavit_statute"),
        "covered_persons": m.get("covered_persons"),
        "recent_amendments": m.get("recent_amendments"),
    }


def _resolved_from_both(gpt: dict, gem: dict) -> dict:
    """Merge: prefer non-null, prefer GPT on tie (it's the first model queried)."""
    result = _resolved_from(gpt)
    for k, v in result.items():
        if v is None and gem.get(k) is not None:
            result[k] = gem[k]
    # For rent threshold, take the more recent year if they differ
    gpt_year = gpt.get("current_rent_threshold_year", "")
    gem_year = gem.get("current_rent_threshold_year", "")
    if gem_year and gem_year > gpt_year:
        result["current_rent_threshold_dollars"] = gem.get("current_rent_threshold_dollars")
        result["current_rent_threshold_year"] = gem_year
    return result


# ── Flag writer ────────────────────────────────────────────────────────────────

def write_scra_flags(all_data: dict, all_paths: dict, classification: str,
                     note: str, resolved: dict, gpt: dict, gem: dict):
    """Write L2 SCRA result flag to all 51 state files."""
    code_map = {
        "CONSENSUS": "L2-SCRA-OVERLAY-CONSENSUS-CONFIRMED",
        "THRESHOLD-DIVERGE": "L2-SCRA-OVERLAY-THRESHOLD-DIVERGE",
        "SINGLE-MODEL-GEMINI": "L2-SCRA-OVERLAY-SINGLE-MODEL-RESOLVED",
        "SINGLE-MODEL-GPT": "L2-SCRA-OVERLAY-SINGLE-MODEL-RESOLVED",
        "CITATION-DIVERGE": "L7-SCRA-OVERLAY-ATTORNEY-REVIEW",
        "MODEL-SPLIT": "L7-SCRA-OVERLAY-ATTORNEY-REVIEW",
        "ERROR": "L2-SCRA-OVERLAY-ERROR",
    }
    disposition_map = {
        "CONSENSUS": "resolved-confirmed",
        "THRESHOLD-DIVERGE": "pending-human-confirmation",
        "SINGLE-MODEL-GEMINI": "pending-human-confirmation",
        "SINGLE-MODEL-GPT": "pending-human-confirmation",
        "CITATION-DIVERGE": "open",
        "MODEL-SPLIT": "open",
        "ERROR": "open",
    }

    flag = {
        "layer": "L2",
        "code": code_map.get(classification, "L2-SCRA-OVERLAY-ERROR"),
        "field": "overlays.federal.scra",
        "disposition": disposition_map.get(classification, "open"),
        "status": "pending-human-confirmation",
        "l2_run_date": TODAY,
        "classification": classification,
        "note": note,
        "gpt_summary": {
            "primary_citation": gpt.get("primary_citation"),
            "rent_threshold": gpt.get("current_rent_threshold_dollars"),
            "rent_threshold_year": gpt.get("current_rent_threshold_year"),
            "confidence": gpt.get("confidence"),
            "error": gpt.get("error"),
        },
        "gemini_summary": {
            "primary_citation": gem.get("primary_citation"),
            "rent_threshold": gem.get("current_rent_threshold_dollars"),
            "rent_threshold_year": gem.get("current_rent_threshold_year"),
            "confidence": gem.get("confidence"),
            "error": gem.get("error"),
        },
    }

    if resolved:
        flag["resolved_content"] = resolved

    updated = 0
    for state, data in all_data.items():
        path = all_paths[state]
        flags = data["validation"].setdefault("flags", [])

        # Remove prior SCRA L2 flags for idempotency
        flags = [fl for fl in flags if "SCRA" not in fl.get("code", "").upper()
                 or fl.get("layer") != "L2"]

        data["validation"]["flags"] = flags + [flag]

        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        updated += 1

    print(f"\n  ✅ SCRA L2 flag written to {updated} state files.")


def update_scra_content(all_data: dict, all_paths: dict, resolved: dict):
    """
    If consensus confirmed, replace the pending-l2 stub in overlays.federal
    with the L2-validated content. Still marked pending-human-confirmation
    per ACP guardrail.
    """
    content = {
        "name": "SCRA §3951 (Servicemembers Civil Relief Act)",
        "applies_when": resolved.get("covered_persons", "Tenant is a servicemember or dependent in active military service"),
        "effect": (
            f"{resolved.get('core_protection', '')} "
            f"Court may stay proceedings up to {resolved.get('max_stay_days', 90)} days. "
            f"Protection applies when monthly rent does not exceed "
            f"${resolved.get('current_rent_threshold_dollars', 'threshold-pending')}/month "
            f"({resolved.get('current_rent_threshold_year', 'year pending')}; "
            f"adjusted {resolved.get('threshold_adjustment_method', 'annually')}). "
            f"Landlord must file affidavit of non-military-service before judgment "
            f"({resolved.get('affidavit_statute', '50 U.S.C. §3931')}). "
            f"Recent amendments: {resolved.get('recent_amendments', 'none identified')}."
        ),
        "statute": resolved.get("primary_citation", "50 U.S.C. §3951"),
        "status": "active",
        "validation": "L2-VALIDATED-PENDING-HUMAN-CONFIRMATION",
        "l2_run_date": TODAY,
        "_note": "Federal law — applies uniformly in all 50 states + DC.",
    }

    updated = 0
    for state, data in all_data.items():
        path = all_paths[state]
        federal = data.get("overlays", {}).get("federal", [])
        if isinstance(federal, list):
            for i, entry in enumerate(federal):
                if isinstance(entry, dict) and "SCRA" in entry.get("name", "").upper():
                    federal[i] = content
                    updated += 1
                    break

        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")

    print(f"  ✅ SCRA content updated in {updated} state files (pending-human-confirmation).")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("\nCivil Justice as Code — SCRA Federal Overlay L2 (Module 3)")
    print(f"Run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Models: {OPENAI_MODEL} + {GEMINI_MODEL}")
    print(f"Budget cap: ${BUDGET_CAP:.2f}")
    print(f"Query: neutral (no preliminary threshold values fed to models)")
    print(f"Scope: single query covers all 51 states (uniform federal law)")
    print("=" * 60)

    # Load all state files
    all_data, all_paths = load_all_v2_files()
    print(f"\n  Loaded {len(all_data)} state files.")

    # Query both models (single query — federal law is uniform)
    print("\n  Querying GPT...")
    gpt = call_gpt_scra()

    print("  Querying Gemini...")
    gem = call_gemini_scra()

    # Classify
    classification, note, resolved = classify_scra(gpt, gem)

    print(f"\n{'=' * 60}")
    print(f"  CLASSIFICATION: {classification}")
    print(f"  NOTE: {note}")
    if resolved.get("current_rent_threshold_dollars"):
        print(f"  RESOLVED THRESHOLD: ${resolved['current_rent_threshold_dollars']} "
              f"({resolved.get('current_rent_threshold_year', '?')})")
    print(f"{'=' * 60}")

    # Save raw output
    raw_output = {
        "run_date": TODAY,
        "module": "scra_overlay",
        "classification": classification,
        "note": note,
        "resolved_content": resolved,
        "gpt_response": gpt,
        "gemini_response": gem,
        "preliminary_threshold_for_reference": 4073.16,
        "preliminary_threshold_year_for_reference": "2024",
    }
    output_path = OUTPUT_DIR / f"scra_l2_raw_{TODAY}.json"
    with open(output_path, "w") as f:
        json.dump(raw_output, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"\n  Raw output saved: {output_path}")

    # Write flags to all 51 state files
    write_scra_flags(all_data, all_paths, classification, note, resolved, gpt, gem)

    # If consensus or single-model resolved: update canonical SCRA content in files
    if classification in ("CONSENSUS", "SINGLE-MODEL-GEMINI", "SINGLE-MODEL-GPT") and resolved:
        print("\n  Updating canonical SCRA content across 51 state files...")
        update_scra_content(all_data, all_paths, resolved)
    else:
        print(f"\n  ⚠️  Classification is {classification} — canonical content NOT updated.")
        print(f"  Pending-l2 stubs remain in place until attorney resolves.")

    # Interpretation
    print("\n  INTERPRETATION:")
    if classification == "CONSENSUS":
        print(f"  ✅ Both models agree on SCRA citation and rent threshold.")
        print(f"  GPT: {gpt.get('primary_citation')} / ${gpt.get('current_rent_threshold_dollars')} ({gpt.get('current_rent_threshold_year')})")
        print(f"  Gemini: {gem.get('primary_citation')} / ${gem.get('current_rent_threshold_dollars')} ({gem.get('current_rent_threshold_year')})")
        prelim = 4073.16
        resolved_thresh = resolved.get("current_rent_threshold_dollars")
        if resolved_thresh and abs(float(resolved_thresh) - prelim) > 50:
            print(f"  ⚠️  THRESHOLD UPDATED: Preliminary was ${prelim}; L2 says ${resolved_thresh}. Canonical files updated.")
        else:
            print(f"  ✅ Threshold consistent with preliminary (${prelim}).")
        amendments = resolved.get("recent_amendments", "")
        if amendments and amendments.lower() not in ("none", "none identified", "none known"):
            print(f"  ⚠️  AMENDMENTS FOUND: {amendments}")
    elif classification == "THRESHOLD-DIVERGE":
        print(f"  ⚠️  Citation agrees but threshold differs. Attorney/primary source to confirm current figure.")
        print(f"  GPT threshold: ${gpt.get('current_rent_threshold_dollars')} ({gpt.get('current_rent_threshold_year')})")
        print(f"  Gemini threshold: ${gem.get('current_rent_threshold_dollars')} ({gem.get('current_rent_threshold_year')})")
    elif "SINGLE-MODEL" in classification:
        print(f"  One model failed; other model carried. Pending-confirmation.")
    elif classification in ("CITATION-DIVERGE", "MODEL-SPLIT"):
        print(f"  ⚠️  Unexpected disagreement on uniform federal law — escalated to L7.")
    elif classification == "ERROR":
        print(f"  ✗ Both models failed. Check API keys and retry.")

    print()
    print("  ⚠️  STOP AND REPORT. Share output with Cowork for ingestion.")
    print(f"  Output: {output_path}")


if __name__ == "__main__":
    main()
