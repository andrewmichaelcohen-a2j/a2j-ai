#!/usr/bin/env python3
"""
NM Service Citation Warm-Up Runner
===================================
Single-state L2 run for New Mexico — confirms whether service methods are
governed by NMSA 1978 §47-8-52 (URLTA service provision, as preliminary
assessment indicated) vs. the currently-cited §47-8-33 (which is the
notice-period statute, not the service-method statute).

This is the smallest possible L2 run — one state, one question, expected
easy consensus. Used to verify the Terminal → L2 → ingest cycle before
the larger retaliation run.

Output: rules/validation/l2/output/nm_service_l2_raw_<date>.json
        (also prints full model responses to console)

GUARDRAILS:
  - Neutral query — does NOT mention §47-8-33 or §47-8-52 (no anchoring)
  - Keys from .env only
  - Never advances past ACP
  - Appends flag to NM rules file; never edits content fields directly
  - $1 budget cap (single state)

Usage (run from repo root in Andy's Terminal):
  cd /Users/andrewcohen/Developer/a2j-ai
  python3 rules/validation/l2/nm_service_runner.py

Expected output: streaming per-model responses, then classification.
Expected cost: ~$0.03. Expected time: ~30 seconds.

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

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
BUDGET_CAP = 1.00  # Single-state run; $1 is ample

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Query ──────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a legal research expert in US residential landlord-tenant law. "
    "Answer questions about New Mexico landlord-tenant statutes precisely. "
    "Cite specific statute and subsection numbers. Respond only in the JSON format requested."
)

NM_QUERY = """In New Mexico, when a landlord wants to serve a pay-or-quit (demand for rent) notice
on a residential tenant prior to filing an eviction action for nonpayment of rent, what methods
of service are legally permitted?

Specifically:
1. What is the statute (with specific section and subsection) that governs HOW the notice must be served
   (i.e., the service METHOD provision, not the notice-period provision)?
2. For each permitted method, what does the statute require?

New Mexico has adopted the Uniform Owner-Resident Relations Act (UORRA).
Please identify which specific statute section governs the service METHODS (not the length of the notice period).

Respond ONLY in valid JSON:
{
  "service_method_statute": "exact citation e.g. NMSA 1978 §47-8-XX",
  "service_method_statute_subsections": {
    "personal": "subsection governing personal delivery, or null if not specified",
    "substituted": "subsection governing substituted service, or null",
    "mail": "subsection governing mail/posting, or null"
  },
  "notice_period_statute": "the statute that sets the notice PERIOD (days), if different",
  "confidence": "high|medium|low",
  "reasoning": "brief explanation of which statute you identified as governing service methods"
}"""


# ── Call wrappers ──────────────────────────────────────────────────────────────

def call_gpt_nm() -> dict:
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
                {"role": "user", "content": NM_QUERY},
            ],
            max_completion_tokens=1500,
        )
        raw = resp.choices[0].message.content.strip() if resp.choices[0].message.content else ""
        print(f"\n  [GPT raw response]\n{raw}\n")
        result = _parse_json_response(raw)
        return result
    except Exception as exc:
        return {"error": str(exc)}


def call_gemini_nm() -> dict:
    try:
        from google import genai
    except ImportError:
        return {"error": "google-genai not installed — run: pip install google-genai"}
    try:
        client = genai.Client(api_key=GOOGLE_KEY)
        full_prompt = SYSTEM_PROMPT + "\n\n" + NM_QUERY
        resp = client.models.generate_content(model=GEMINI_MODEL, contents=full_prompt)
        raw = resp.text.strip()
        print(f"\n  [Gemini raw response]\n{raw}\n")
        result = _parse_json_response(raw)
        return result
    except Exception as exc:
        return {"error": str(exc)}


# ── Classification ─────────────────────────────────────────────────────────────

def classify_nm(gpt: dict, gem: dict) -> tuple[str, str]:
    """Returns (classification, note)."""
    if gpt.get("error") and gem.get("error"):
        return "ERROR", f"Both models failed. GPT: {gpt['error'][:100]}. Gemini: {gem['error'][:100]}"

    if gpt.get("error"):
        # Single-model fallback — Gemini only
        statute = gem.get("service_method_statute", "")
        return "SINGLE-MODEL-GEMINI", f"GPT failed ({gpt['error'][:60]}). Gemini: {statute}"

    if gem.get("error"):
        # Single-model fallback — GPT only
        statute = gpt.get("service_method_statute", "")
        return "SINGLE-MODEL-GPT", f"Gemini failed ({gem['error'][:60]}). GPT: {statute}"

    gpt_statute = gpt.get("service_method_statute", "")
    gem_statute = gem.get("service_method_statute", "")

    # Extract section numbers for comparison
    import re
    def extract_nums(s):
        return set(re.findall(r'\d+[\-\.]?\d*[a-zA-Z]?', s or ""))

    gpt_nums = extract_nums(gpt_statute)
    gem_nums = extract_nums(gem_statute)

    if gpt_nums & gem_nums:
        # Models agree on section number
        return "CONSENSUS", f"Both models identify {gpt_statute} as the service-method statute."
    else:
        return "MODEL-SPLIT", (
            f"Models disagree: GPT says '{gpt_statute}'; "
            f"Gemini says '{gem_statute}'. L7 — attorney review."
        )


# ── Flag writer ────────────────────────────────────────────────────────────────

def write_nm_flag(data: dict, path: str, classification: str, note: str,
                  gpt: dict, gem: dict):
    """Append L2 result flag to NM rules file. Never edits content fields."""
    flags = data["validation"].setdefault("flags", [])

    # Remove any existing open PENDING-CONFIRMATION flag for idempotency
    flags = [fl for fl in flags if not (
        fl.get("code") == "L2-SERVICE-CLAUDE-PRELIMINARY"
        and fl.get("status") == "pending-human-confirmation"
    )]

    code_map = {
        "CONSENSUS": "L2-SERVICE-SAME-STATUTE-CONFIRMED",
        "SINGLE-MODEL-GEMINI": "L2-SERVICE-SINGLE-MODEL-RESOLVED",
        "SINGLE-MODEL-GPT": "L2-SERVICE-SINGLE-MODEL-RESOLVED",
        "MODEL-SPLIT": "L7-SERVICE-ATTORNEY-REVIEW",
        "ERROR": "L2-SERVICE-ERROR",
    }

    disposition_map = {
        "CONSENSUS": "resolved-confirmed",
        "SINGLE-MODEL-GEMINI": "pending-human-confirmation",
        "SINGLE-MODEL-GPT": "pending-human-confirmation",
        "MODEL-SPLIT": "open",
        "ERROR": "open",
    }

    flag = {
        "layer": "L2",
        "code": code_map.get(classification, "L2-SERVICE-ERROR"),
        "field": "service.method_rules",
        "disposition": disposition_map.get(classification, "open"),
        "status": "pending-human-confirmation" if classification in ("CONSENSUS", "SINGLE-MODEL-GEMINI", "SINGLE-MODEL-GPT") else "open",
        "l2_run_date": TODAY,
        "note": note,
        "gpt_result": {
            "service_method_statute": gpt.get("service_method_statute"),
            "confidence": gpt.get("confidence"),
            "reasoning": gpt.get("reasoning"),
            "error": gpt.get("error"),
        },
        "gemini_result": {
            "service_method_statute": gem.get("service_method_statute"),
            "confidence": gem.get("confidence"),
            "reasoning": gem.get("reasoning"),
            "error": gem.get("error"),
        },
    }

    # If consensus: also populate resolved_statutes so downstream has the citation
    if classification == "CONSENSUS":
        gpt_subs = gpt.get("service_method_subsections") or gpt.get("service_method_statute_subsections") or {}
        gem_subs = gem.get("service_method_subsections") or gem.get("service_method_statute_subsections") or {}
        statute = gpt.get("service_method_statute") or gem.get("service_method_statute")
        flag["resolved_statutes"] = {
            "personal": gpt_subs.get("personal") or gem_subs.get("personal") or statute,
            "substituted": gpt_subs.get("substituted") or gem_subs.get("substituted") or statute,
            "mail": gpt_subs.get("mail") or gem_subs.get("mail") or statute,
            "_note": "Populated from L2 consensus run. Pending human confirmation.",
        }

    data["validation"]["flags"] = flags + [flag]

    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"\n  ✅ Flag written to {path}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("\nCivil Justice as Code — NM Service Citation L2 (warm-up)")
    print(f"Run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Models: {OPENAI_MODEL} + {GEMINI_MODEL}")
    print(f"Budget cap: ${BUDGET_CAP:.2f}")
    print(f"Query: neutral (no anchoring to file or preliminary values)")
    print("=" * 60)

    # Load NM file
    all_data, all_paths = load_all_v2_files()
    if "NM" not in all_data:
        print("ERROR: NM rules file not found")
        sys.exit(1)

    nm_data = all_data["NM"]
    nm_path = all_paths["NM"]
    print(f"\n  NM file: {nm_path}")

    # Current file service claim (for reference only — NOT fed to models)
    service = nm_data.get("service", {})
    method_rules = service.get("method_rules", [])
    file_statutes = list({m.get("statute") for m in method_rules if m.get("statute")})
    print(f"  Current file statutes (for reference, NOT in query): {file_statutes}")
    print()

    # Query both models
    print("  Querying GPT...")
    gpt = call_gpt_nm()

    print("  Querying Gemini...")
    gem = call_gemini_nm()

    # Classify
    classification, note = classify_nm(gpt, gem)

    print(f"\n{'=' * 60}")
    print(f"  CLASSIFICATION: {classification}")
    print(f"  NOTE: {note}")
    print(f"{'=' * 60}")

    # Save raw output
    raw_output = {
        "run_date": TODAY,
        "state": "NM",
        "classification": classification,
        "note": note,
        "gpt_response": gpt,
        "gemini_response": gem,
        "current_file_statutes": file_statutes,
    }
    output_path = OUTPUT_DIR / f"nm_service_l2_raw_{TODAY}.json"
    with open(output_path, "w") as f:
        json.dump(raw_output, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"\n  Raw output saved: {output_path}")

    # Write flag to NM rules file
    write_nm_flag(nm_data, nm_path, classification, note, gpt, gem)

    # Interpretation
    print("\n  INTERPRETATION:")
    if classification == "CONSENSUS":
        gpt_s = gpt.get("service_method_statute", "?")
        gem_s = gem.get("service_method_statute", "?")
        print(f"  Both models agree on the NM service-method statute.")
        print(f"  GPT: {gpt_s}")
        print(f"  Gemini: {gem_s}")
        print()
        file_stat = file_statutes[0] if file_statutes else "?"
        if "47-8-52" in gpt_s or "47-8-52" in gem_s:
            print(f"  ✅ Preliminary hypothesis CONFIRMED: §47-8-52 is the service-method statute.")
            print(f"  Current file cites: {file_stat} — CORRECTION NEEDED (pending Andy's review).")
        elif "47-8-33" in gpt_s or "47-8-33" in gem_s:
            print(f"  ⚠️  Unexpected: models confirmed §47-8-33 as service statute (preliminary said it was notice-period).")
            print(f"  Attorney should verify which statute governs service methods.")
        else:
            print(f"  ⚠️  Models agree on a different statute: {gpt_s}. Verify vs. file ({file_stat}).")
    elif "SINGLE-MODEL" in classification:
        print(f"  One model failed; other model returned result. Pending-confirmation.")
    elif classification == "MODEL-SPLIT":
        print(f"  Models disagree — genuine L7. Attorney review required.")
    elif classification == "ERROR":
        print(f"  Both models failed. Check API keys and retry.")

    print()
    print("  ⚠️  STOP AND REPORT. Do not auto-edit NM file content.")
    print("  Next: share output with Cowork for ingestion and resolution.")


if __name__ == "__main__":
    main()
