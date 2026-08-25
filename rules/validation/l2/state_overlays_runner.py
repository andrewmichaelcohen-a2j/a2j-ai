#!/usr/bin/env python3
"""
State-Protective Overlays L2 Runner — Module 4
===============================================
Citation check for all state_protective overlay entries across all 51 state
files. 107 total overlay items (avg ~2 per state). For each state, queries
GPT + Gemini: "What statutes govern these protections in [STATE]?" — neutral,
no file citations fed to models.

The two most common overlays (all 51 states have them):
  - Implied Warranty of Habitability (sometimes case-law-only)
  - Anti-Retaliation Protection

Some states have additional overlays (CA: AB1482; NY: HSTPA, Good Cause, Rent
Stabilization; DC: TOPA, rent control, etc.)

Special-attention states per prior assessment:
  - PA: anti-retaliation is case-law; statute unclear
  - MI: MCL §600.5720 — may be wrong section
  - NY: complex (4 overlays; recent HSTPA + Good Cause changes)
  - WA: RCW 59.18.240 flagged for recent legislative activity

Output: rules/validation/l2/output/state_overlays_l2_raw_<date>.json
        (prints per-state results to console)

GUARDRAILS:
  - Neutral query per state — file citations NOT fed to models
  - Keys from .env only
  - Never advances past ACP
  - Writes flags to state files; never edits citation content directly
  - $15 budget cap (~51 states × 2 models; expect ~$5-8)

Usage (run from repo root in Andy's Terminal):
  cd /Users/andrewcohen/Developer/a2j-ai
  python3 rules/validation/l2/state_overlays_runner.py

Expected cost: ~$5-8. Expected time: ~10-15 minutes.

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_L2_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_L2_DIR))

from l2_runner import (
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
COST_PER_STATE = 0.15   # conservative estimate; actual likely ~$0.10

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# States that need extra attention (from prior assessment)
FLAGGED_STATES = {
    "PA": "anti-retaliation primarily case law; verify whether statutory basis exists",
    "MI": "MCL §600.5720 flagged — may be wrong section for retaliation; MCL 554.139 is habitability",
    "NY": "complex overlays (4 items); HSTPA 2019 + Good Cause 2024 are recent",
    "WA": "RCW 59.18.240 flagged for recent legislative activity (2021-2023)",
}

# Full state names for query clarity
STATE_NAMES = {
    "AK":"Alaska","AL":"Alabama","AR":"Arkansas","AZ":"Arizona","CA":"California",
    "CO":"Colorado","CT":"Connecticut","DC":"District of Columbia","DE":"Delaware",
    "FL":"Florida","GA":"Georgia","HI":"Hawaii","IA":"Iowa","ID":"Idaho",
    "IL":"Illinois","IN":"Indiana","KS":"Kansas","KY":"Kentucky","LA":"Louisiana",
    "MA":"Massachusetts","MD":"Maryland","ME":"Maine","MI":"Michigan","MN":"Minnesota",
    "MO":"Missouri","MS":"Mississippi","MT":"Montana","NC":"North Carolina",
    "ND":"North Dakota","NE":"Nebraska","NH":"New Hampshire","NJ":"New Jersey",
    "NM":"New Mexico","NV":"Nevada","NY":"New York","OH":"Ohio","OK":"Oklahoma",
    "OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina",
    "SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VA":"Virginia",
    "VT":"Vermont","WA":"Washington","WI":"Wisconsin","WV":"West Virginia","WY":"Wyoming",
}


# ── Query builder ──────────────────────────────────────────────────────────────

def build_query(state: str, overlay_names: list[str]) -> str:
    full_name = STATE_NAMES.get(state, state)
    names_list = "\n".join(f"  {i+1}. {n}" for i, n in enumerate(overlay_names))
    return f"""In {full_name}, for each of the following tenant protections, provide the primary
statutory citation. Do NOT rely on generic knowledge — be specific to {full_name} law.

Protections to verify:
{names_list}

For each protection, respond with:
- The exact statute citation (Code name, title, chapter, section, and subsection if applicable)
- Whether the protection is established by statute or primarily by case law
- Confidence level (high/medium/low)
- Any important caveats or recent changes (post-2020)

Respond ONLY in valid JSON as an array:
[
  {{
    "protection_name": "<exact name from the list above>",
    "primary_citation": "<exact statutory citation or 'case law only'>",
    "secondary_citation": "<any additional relevant citation, or null>",
    "is_statutory": true,
    "confidence": "high|medium|low",
    "recent_changes": "<description of post-2020 changes, or 'none identified'>",
    "notes": "<any important caveats>"
  }}
]

Return exactly {len(overlay_names)} items in the array, one per protection listed above."""


SYSTEM_PROMPT = (
    "You are a legal research expert in US residential landlord-tenant law. "
    "For each US state, provide precise statutory citations for tenant protections. "
    "Be specific: cite exact code names, section numbers, and subsections. "
    "If a protection exists only in case law (not statute), say 'case law only' for the citation "
    "and set is_statutory to false. "
    "Respond ONLY in the JSON array format requested. "
    "Do not add commentary outside the JSON."
)


# ── API callers ────────────────────────────────────────────────────────────────

def call_gpt(state: str, query: str, retries: int = 2) -> dict:
    try:
        from openai import OpenAI
    except ImportError:
        return {"error": "openai not installed"}
    client = OpenAI(api_key=OPENAI_KEY)
    for attempt in range(retries + 1):
        try:
            resp = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": query},
                ],
                max_completion_tokens=6000,  # increased from 4000; gpt-5.5 chain-of-thought exhausts <6000 (confirmed 2026-06-21 diagnostic)
            )
            raw = resp.choices[0].message.content.strip() if resp.choices[0].message.content else ""
            if not raw:
                if attempt < retries:
                    time.sleep(2)
                    continue
                return {"error": "empty response after retries"}
            result = _parse_json_response(raw)
            # Validate: should be a list
            if isinstance(result, list):
                return {"overlays": result}
            elif isinstance(result, dict) and result.get("error"):
                if attempt < retries:
                    time.sleep(2)
                    continue
                return result
            else:
                # Might be a dict wrapping the list
                if isinstance(result, dict):
                    for v in result.values():
                        if isinstance(v, list):
                            return {"overlays": v}
                if attempt < retries:
                    time.sleep(2)
                    continue
                return {"error": f"unexpected format: {type(result)}", "raw": raw[:200]}
        except Exception as exc:
            if attempt < retries:
                time.sleep(2)
                continue
            return {"error": str(exc)}
    return {"error": "exhausted retries"}


def call_gemini(state: str, query: str) -> dict:
    try:
        from google import genai
    except ImportError:
        return {"error": "google-genai not installed"}
    try:
        client = genai.Client(api_key=GOOGLE_KEY)
        full_prompt = SYSTEM_PROMPT + "\n\n" + query
        resp = client.models.generate_content(model=GEMINI_MODEL, contents=full_prompt)
        raw = resp.text.strip()
        result = _parse_json_response(raw)
        if isinstance(result, list):
            return {"overlays": result}
        elif isinstance(result, dict):
            for v in result.values():
                if isinstance(v, list):
                    return {"overlays": v}
            return result
        return {"error": f"unexpected format: {type(result)}", "raw": raw[:200]}
    except Exception as exc:
        return {"error": str(exc)}


# ── Classification ─────────────────────────────────────────────────────────────

def extract_nums(citation: str) -> set:
    if not citation or citation.lower() in ("case law only", "null", "none", "n/a"):
        return set()
    return set(re.findall(r'\d+[\-\.]?\d*[a-zA-Z]?', citation))


def classify_overlay(file_citation: str, gpt_item: Optional[dict], gem_item: Optional[dict]):
    """Returns (classification, note)."""
    gpt_cite = (gpt_item or {}).get("primary_citation", "") if gpt_item else ""
    gem_cite = (gem_item or {}).get("primary_citation", "") if gem_item else ""

    gpt_ok = gpt_item and not gpt_item.get("error")
    gem_ok = gem_item and not gem_item.get("error")

    if not gpt_ok and not gem_ok:
        return "ERROR", "Both models failed to return overlay data."

    # Case-law-only check
    gpt_case_law = gpt_ok and "case law" in gpt_cite.lower()
    gem_case_law = gem_ok and "case law" in gem_cite.lower()
    if gpt_case_law and gem_case_law:
        return "CASE-LAW-CONFIRMED", f"Both models: protection is case-law-only (no statute). File: {file_citation}"
    if (gpt_case_law and gem_ok) or (gem_case_law and gpt_ok):
        return "CASE-LAW-ONE-MODEL", f"Split: one model says case law, other says statute. GPT: '{gpt_cite}'. Gemini: '{gem_cite}'."

    # Single-model fallback
    if not gpt_ok:
        file_nums = extract_nums(file_citation)
        gem_nums = extract_nums(gem_cite)
        if file_nums & gem_nums:
            return "FILE-CITATION-GEMINI-CONFIRMED", f"GPT failed. Gemini confirms file citation. Gem: {gem_cite}"
        else:
            return "GEMINI-SUGGESTS-DIFFERENT", f"GPT failed. Gemini proposes: {gem_cite} (file: {file_citation})"

    if not gem_ok:
        file_nums = extract_nums(file_citation)
        gpt_nums = extract_nums(gpt_cite)
        if file_nums & gpt_nums:
            return "FILE-CITATION-GPT-CONFIRMED", f"Gemini failed. GPT confirms file citation. GPT: {gpt_cite}"
        else:
            return "GPT-SUGGESTS-DIFFERENT", f"Gemini failed. GPT proposes: {gpt_cite} (file: {file_citation})"

    # Both models have citations — compare to each other and to file
    file_nums = extract_nums(file_citation)
    gpt_nums = extract_nums(gpt_cite)
    gem_nums = extract_nums(gem_cite)

    models_agree = bool(gpt_nums & gem_nums) or (gpt_cite.lower() == gem_cite.lower())
    file_matches_gpt = bool(file_nums & gpt_nums)
    file_matches_gem = bool(file_nums & gem_nums)
    file_matches_either = file_matches_gpt or file_matches_gem

    if models_agree and file_matches_either:
        return "CITATION-CONFIRMED", f"Models agree and file citation matches. GPT: {gpt_cite} | Gem: {gem_cite}"

    if models_agree and not file_matches_either:
        return "CITATION-DIVERGE-FROM-FILE", (
            f"Models agree with each other but differ from file. "
            f"File: {file_citation} | GPT: {gpt_cite} | Gem: {gem_cite}"
        )

    if not models_agree:
        return "MODEL-SPLIT", (
            f"Models disagree. File: {file_citation} | GPT: {gpt_cite} | Gem: {gem_cite}"
        )

    return "UNKNOWN", f"GPT: {gpt_cite} | Gem: {gem_cite} | File: {file_citation}"


# ── Flag writer ────────────────────────────────────────────────────────────────

NEEDS_QUEUE = {"CITATION-DIVERGE-FROM-FILE", "MODEL-SPLIT", "CASE-LAW-ONE-MODEL",
               "GEMINI-SUGGESTS-DIFFERENT", "GPT-SUGGESTS-DIFFERENT", "ERROR"}

def write_overlay_flag(data: dict, path: str, state: str, overlay_results: list):
    """Append per-state overlay L2 results flag. Never edits citation content."""

    # Build per-overlay summary
    overlay_summary = []
    needs_queue = False
    for r in overlay_results:
        cls = r["classification"]
        if cls in NEEDS_QUEUE:
            needs_queue = True
        overlay_summary.append({
            "name": r["name"],
            "file_citation": r["file_citation"],
            "classification": cls,
            "note": r["note"],
            "gpt_citation": r.get("gpt_citation"),
            "gemini_citation": r.get("gemini_citation"),
        })

    code = "L2-OVERLAY-STATE-PROTECTIVE-CITATIONS-VERIFIED" if not needs_queue \
           else "L2-OVERLAY-STATE-PROTECTIVE-CITATIONS-NEEDS-REVIEW"

    flag = {
        "layer": "L2",
        "code": code,
        "field": "overlays.state_protective",
        "disposition": "pending-human-confirmation" if not needs_queue else "open",
        "status": "pending-human-confirmation" if not needs_queue else "open",
        "l2_run_date": TODAY,
        "overlay_results": overlay_summary,
        "needs_queue": needs_queue,
        "note": (
            f"All {len(overlay_results)} overlay citations verified by L2 — no changes needed."
            if not needs_queue else
            f"{sum(1 for r in overlay_results if r['classification'] in NEEDS_QUEUE)}/{len(overlay_results)} "
            f"overlays have citation issues — see overlay_results for detail."
        ),
    }

    if state in FLAGGED_STATES:
        flag["special_attention"] = FLAGGED_STATES[state]

    # Remove prior state-protective overlay flags for idempotency
    flags = data["validation"].get("flags", [])
    flags = [fl for fl in flags if "OVERLAY-STATE-PROTECTIVE" not in fl.get("code", "")]
    flags.append(flag)
    data["validation"]["flags"] = flags

    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("\nCivil Justice as Code — State-Protective Overlays L2 (Module 4)")
    print(f"Run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Models: {OPENAI_MODEL} + {GEMINI_MODEL}")
    print(f"Budget cap: ${BUDGET_CAP:.2f}")
    print(f"Query: neutral per state — file citations NOT fed to models")
    print(f"Special-attention states: {', '.join(FLAGGED_STATES.keys())}")
    print("=" * 60)

    all_data, all_paths = load_all_v2_files()
    print(f"\nLoaded {len(all_data)} state files.")

    results = []
    estimated_cost = 0.0
    confirmed = 0
    needs_review = 0
    errors = 0

    for state in sorted(all_data.keys()):
        if estimated_cost > BUDGET_CAP:
            print(f"\n⚠️  BUDGET CAP ${BUDGET_CAP:.2f} reached after {len(results)} states. Stopping.")
            break

        data = all_data[state]
        path = all_paths[state]

        # Extract overlay names and current citations from file
        sp = data.get("overlays", {}).get("state_protective", [])
        if not sp or not isinstance(sp, list):
            print(f"  [{state}] No state_protective overlays — skipping.")
            continue

        overlay_names = [item.get("name", f"Protection {i+1}") for i, item in enumerate(sp)
                        if isinstance(item, dict)]
        overlay_citations = [item.get("statute", "unknown") for item in sp if isinstance(item, dict)]

        if not overlay_names:
            continue

        flag_str = " ⚠️ FLAGGED" if state in FLAGGED_STATES else ""
        print(f"\n  [{state}]{flag_str} {len(overlay_names)} overlays: {', '.join(overlay_names[:2])}"
              + (f" + {len(overlay_names)-2} more" if len(overlay_names) > 2 else ""))

        query = build_query(state, overlay_names)

        gpt = call_gpt(state, query)
        gem = call_gemini(state, query)

        # Match model responses to overlay items
        gpt_overlays = gpt.get("overlays", []) if not gpt.get("error") else []
        gem_overlays = gem.get("overlays", []) if not gem.get("error") else []

        def find_item(items, name):
            """Find overlay item by protection name (fuzzy match)."""
            name_lower = name.lower()
            for item in items:
                if isinstance(item, dict):
                    item_name = item.get("protection_name", "").lower()
                    if item_name == name_lower or name_lower[:20] in item_name or item_name[:20] in name_lower:
                        return item
            # Fallback: return by index
            return None

        overlay_results = []
        state_needs_review = False

        for i, (name, file_cite) in enumerate(zip(overlay_names, overlay_citations)):
            gpt_item = find_item(gpt_overlays, name)
            if gpt_item is None and i < len(gpt_overlays):
                gpt_item = gpt_overlays[i]

            gem_item = find_item(gem_overlays, name)
            if gem_item is None and i < len(gem_overlays):
                gem_item = gem_overlays[i]

            cls, note = classify_overlay(file_cite, gpt_item, gem_item)
            if cls in NEEDS_QUEUE:
                state_needs_review = True

            gpt_cite_out = (gpt_item or {}).get("primary_citation") if gpt_item else None
            gem_cite_out = (gem_item or {}).get("primary_citation") if gem_item else None

            print(f"    [{cls}] {name[:50]}")
            if cls in NEEDS_QUEUE:
                print(f"      File: {file_cite}")
                print(f"      GPT:  {gpt_cite_out}")
                print(f"      Gem:  {gem_cite_out}")

            overlay_results.append({
                "name": name,
                "file_citation": file_cite,
                "classification": cls,
                "note": note,
                "gpt_citation": gpt_cite_out,
                "gemini_citation": gem_cite_out,
                "gpt_confidence": (gpt_item or {}).get("confidence") if gpt_item else None,
                "gemini_confidence": (gem_item or {}).get("confidence") if gem_item else None,
                "recent_changes": (gem_item or {}).get("recent_changes") if gem_item else None,
            })

        if state_needs_review:
            needs_review += 1
            print(f"    → NEEDS REVIEW")
        else:
            confirmed += 1
            print(f"    → OK")

        write_overlay_flag(data, path, state, overlay_results)

        results.append({
            "state": state,
            "overlay_count": len(overlay_names),
            "overlay_results": overlay_results,
            "needs_review": state_needs_review,
            "gpt_error": gpt.get("error"),
            "gemini_error": gem.get("error"),
        })

        estimated_cost += COST_PER_STATE
        time.sleep(0.5)  # rate limiting

    # Save raw output
    raw_output = {
        "run_date": TODAY,
        "module": "state_overlays",
        "states_run": len(results),
        "confirmed": confirmed,
        "needs_review": needs_review,
        "estimated_cost": estimated_cost,
        "results": results,
    }
    output_path = OUTPUT_DIR / f"state_overlays_l2_raw_{TODAY}.json"
    with open(output_path, "w") as f:
        json.dump(raw_output, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"\n{'=' * 60}")
    print(f"  MODULE 4 COMPLETE")
    print(f"  States run:     {len(results)}/51")
    print(f"  Citations OK:   {confirmed}")
    print(f"  Needs review:   {needs_review}")
    print(f"  Est. cost:      ${estimated_cost:.2f}")
    print(f"  Output:         {output_path}")
    print(f"{'=' * 60}")
    print()
    print("  ⚠️  STOP AND REPORT. Share output with Cowork for ingestion.")


if __name__ == "__main__":
    main()
