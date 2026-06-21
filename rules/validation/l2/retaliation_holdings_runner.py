#!/usr/bin/env python3
"""
Retaliation Defense — Holdings Layer L2 Runner  (Step 2)
=========================================================
Runs L2 multi-model validation on the HOLDINGS layer of the retaliation
defense across all 51 states.

Holdings layer = the controlling/seminal cases establishing or interpreting
the retaliatory-eviction defense in each state.

THIS RUNNER IS FUNDAMENTALLY DIFFERENT FROM BRIGHT-LINE RUNNERS.
The known failure mode is models confidently citing overruled or misstated
case law. This runner VERIFIES, not just generates.

Per COWORK_DIRECTION_RETALIATION_L2.md:

  Phase A — Independent identification (both models separately):
    Both models return their independent case lists. This is the inter-coder
    step for case law.

  Phase B — 4-check mandatory verification for every case either model names:
    1. EXISTENCE    — both models named it independently (inter-coder check)
    2. CITATION     — citation numbers consistent across models
    3. HOLDING      — holding summaries agree thematically
    4. CURRENCY     — explicit verification: "still good law / overruled?"

  Phase C — Disposition (honest by construction):
    DRAFT-CORROBORATED:  all 4 checks pass → holdings-draft-corroborated
    NEEDS-ATTORNEY:      any check fails/uncertain → holdings-needs-attorney
                         (with specific failure reason named)

NOTHING IS EVER AUTO-CONFIRMED.
The honest ceiling here is AI drafts and corroborates candidate holdings;
an attorney confirms they are real, correctly stated, and still good law.
Expect ~30–40% attorney-needed rate — this is correct, not a failure.

Labels:
  layer_decomposition.holdings.validation_status = "L2-HOLDINGS-DRAFT"
  (never "L2-HOLDINGS-CONFIRMED" — only a named attorney may confirm)

GUARDRAILS:
  - Neutral Phase A query: no file case_law values fed to models
  - No auto-confirm under any conditions
  - Keys from .env only
  - Never advances past ACP
  - $20 budget cap (51 × Phase A + per-case Phase B verification)

Usage (run from repo root in Andy's Terminal):
  cd /Users/andrewcohen/Documents/GitHub/a2j-ai
  python3 rules/validation/l2/retaliation_holdings_runner.py

Single state (testing):
  python3 rules/validation/l2/retaliation_holdings_runner.py --states CA

Dry run:
  python3 rules/validation/l2/retaliation_holdings_runner.py --dry-run

Expected: ~51 × $0.10 (Phase A) + ~102 × $0.03 (Phase B) = ~$8–12 total.
Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import os
import re
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List

# ── Shared utilities ───────────────────────────────────────────────────────────
_L2_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_L2_DIR))

from l2_runner import (
    load_all_v2_files,
    _parse_json_response,
    OPENAI_MODEL,
    GEMINI_MODEL,
    OPENAI_KEY,
    GOOGLE_KEY,
)

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
BUDGET_CAP = 20.00
APPROX_COST_PHASE_A = 0.08   # per state (both models, identification query)
APPROX_COST_PHASE_B = 0.03   # per case (both models, currency verification)
MAX_CASES_PER_MODEL = 4       # cap to control Phase B cost and quality

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

ALL_STATES = [
    "AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL",
    "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA",
    "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE",
    "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI",
    "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY",
]

# States with well-known major retaliation cases — for QA comparison
LANDMARK_WATCH = {
    "CA": "Aweeka v. Bonds (1971) or Civ. Code §1942.5 statutory regime",
    "NY": "Hilbert v. Daly or RPL §223-b statutory regime",
    "NJ": "Marini v. Ireland (1971)",
    "WA": "RCW 59.18.240-250 statutory; Lochridge v. Standard Furniture",
    "IL": "765 ILCS 720 statutory; Clore v. Fredman",
}

# ── System prompt ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a legal research expert in US residential landlord-tenant law. "
    "You answer questions about case law governing tenant defenses in eviction proceedings. "
    "Be precise about case citations. Only include cases you are genuinely confident are "
    "real, correctly cited, and relevant — do NOT include cases you are uncertain about. "
    "Respond only in the JSON format requested."
)

# ── Phase A: Identification queries ───────────────────────────────────────────

def build_identification_query(state_name: str) -> str:
    """
    Neutral query — no file case_law values fed to models.
    Asks for top controlling/seminal cases only.
    """
    return f"""In {state_name}, what are the controlling or seminal cases establishing or
interpreting the RETALIATORY EVICTION defense for residential tenants?

Include only the most important cases — maximum {MAX_CASES_PER_MODEL} cases.
Do NOT include cases you are uncertain about or cannot fully cite.
Focus on cases that established or significantly shaped the law in {state_name}.

For each case, provide:
- Full case name (plaintiff v. defendant)
- Reporter citation (volume, reporter, page — e.g., "123 Cal.App.3d 456")
- Year decided
- Court (e.g., "Cal. Ct. App." or "{state_name} Supreme Court")
- One-sentence statement of what it held regarding retaliation

If {state_name} has NO controlling case law on retaliatory eviction (e.g., because the
defense is entirely statutory with no significant judicial interpretation), say so explicitly.

Respond ONLY in valid JSON:
{{
  "has_controlling_cases": true,
  "cases": [
    {{
      "case_name": "Plaintiff v. Defendant",
      "citation": "123 [Reporter] 456",
      "year": 1974,
      "court": "court name",
      "holding_summary": "one-sentence description of what this case held"
    }}
  ],
  "statutory_only": false,
  "statutory_note": "if statutory_only=true, describe the statutory regime briefly",
  "confidence": "high|medium|low",
  "note": "any important caveats"
}}"""


def build_currency_query(state_name: str, case_name: str, citation: str, year: int) -> str:
    """
    Explicit currency verification query per case.
    This is the critical Phase B step 4.
    """
    return f"""Regarding the case: {case_name}, {citation} ({year}), decided in {state_name}:

Has this case been overruled, superseded, abrogated, or significantly limited by later
authority (either judicial decisions or statute) in the context of residential retaliatory
eviction law?

Be precise. If you are uncertain whether this case still represents good law, say so.

Respond ONLY in valid JSON:
{{
  "still_good_law": true,
  "currency_status": "good_law|overruled|superseded|limited|uncertain",
  "limiting_authority": "name any later decision or statute that limits/overrules this case, or null",
  "limitation_scope": "description of how the case was limited, or null",
  "confidence": "high|medium|low",
  "note": "any important caveats"
}}"""


# ── API callers ────────────────────────────────────────────────────────────────

DRY_RUN_IDENTIFICATION = {
    "has_controlling_cases": True,
    "cases": [
        {
            "case_name": "Plaintiff v. Defendant (DRY RUN)",
            "citation": "123 Dry.App. 456",
            "year": 1974,
            "court": "State Supreme Court",
            "holding_summary": "Established retaliatory eviction defense requiring causal connection.",
        }
    ],
    "statutory_only": False,
    "statutory_note": None,
    "confidence": "high",
    "note": "dry run",
}

DRY_RUN_CURRENCY = {
    "still_good_law": True,
    "currency_status": "good_law",
    "limiting_authority": None,
    "limitation_scope": None,
    "confidence": "high",
    "note": "dry run",
}


def _call_gpt(query: str, max_tokens: int = 2000) -> dict:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_KEY)
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
            max_completion_tokens=max_tokens,
        )
        raw = resp.choices[0].message.content.strip() if resp.choices[0].message.content else ""
        return _parse_json_response(raw) if raw else {"error": "empty response"}
    except ImportError:
        return {"error": "openai not installed"}
    except Exception as exc:
        return {"error": str(exc)}


def _call_gemini(query: str) -> dict:
    try:
        from google import genai
        client = genai.Client(api_key=GOOGLE_KEY)
        full_prompt = SYSTEM_PROMPT + "\n\n" + query
        resp = client.models.generate_content(model=GEMINI_MODEL, contents=full_prompt)
        raw = resp.text.strip()
        return _parse_json_response(raw) if raw else {"error": "empty response"}
    except ImportError:
        return {"error": "google-genai not installed"}
    except Exception as exc:
        return {"error": str(exc)}


def call_gpt_identification(state_name: str, dry_run: bool = False) -> dict:
    if dry_run:
        return DRY_RUN_IDENTIFICATION.copy()
    result = _call_gpt(build_identification_query(state_name), max_tokens=6000)  # 6000 required: gpt-5.5 chain-of-thought exhausts <6000 (confirmed 2026-06-21)
    # Validate schema
    if not result.get("error") and "cases" not in result:
        return {"error": f"unexpected schema — keys: {list(result.keys())[:6]}"}
    return result


def call_gemini_identification(state_name: str, dry_run: bool = False) -> dict:
    if dry_run:
        return DRY_RUN_IDENTIFICATION.copy()
    result = _call_gemini(build_identification_query(state_name))
    if not result.get("error") and "cases" not in result:
        return {"error": f"unexpected schema — keys: {list(result.keys())[:6]}"}
    return result


def call_gpt_currency(
    state_name: str, case_name: str, citation: str, year: int, dry_run: bool = False
) -> dict:
    if dry_run:
        return DRY_RUN_CURRENCY.copy()
    return _call_gpt(build_currency_query(state_name, case_name, citation, year), max_tokens=3000)  # increased from 800; currency queries are shorter but still need headroom


def call_gemini_currency(
    state_name: str, case_name: str, citation: str, year: int, dry_run: bool = False
) -> dict:
    if dry_run:
        return DRY_RUN_CURRENCY.copy()
    return _call_gemini(build_currency_query(state_name, case_name, citation, year))


# ── Case matching ──────────────────────────────────────────────────────────────

def _name_tokens(name: str) -> set:
    """Extract meaningful tokens from a case name for matching."""
    # Remove common words, keep party names
    stop = {"v", "v.", "vs", "vs.", "in", "re", "the", "of", "and", "&", "et", "al"}
    tokens = set(re.findall(r"[a-zA-Z]+", name.lower())) - stop
    return tokens


def _citation_nums(citation: str) -> set:
    """Extract numeric parts from a citation."""
    return set(re.findall(r"\d+", citation or ""))


def match_cases(gpt_cases: list, gem_cases: list) -> list:
    """
    Match cases across two model responses.

    Returns a list of dicts, each with:
      matched: bool — True if both models named it
      gpt_case: dict or None
      gem_case: dict or None
      canonical_name: str
      canonical_citation: str
      canonical_year: int
    """
    matched = []
    used_gem = set()

    for gi, gc in enumerate(gpt_cases):
        gpt_name = gc.get("case_name", "")
        gpt_year = gc.get("year")
        gpt_cit = gc.get("citation", "")
        gpt_tokens = _name_tokens(gpt_name)
        gpt_nums = _citation_nums(gpt_cit)

        best_gem_idx = None
        for zi, zc in enumerate(gem_cases):
            if zi in used_gem:
                continue
            gem_name = zc.get("case_name", "")
            gem_year = zc.get("year")
            gem_tokens = _name_tokens(gem_name)
            gem_cit = _citation_nums(zc.get("citation", ""))

            # Match heuristic: year agrees (or both null) + ≥2 name tokens overlap
            # OR: citation page/volume numbers overlap substantially
            year_match = (
                gpt_year == gem_year
                or (gpt_year is None and gem_year is None)
                or (gpt_year and gem_year and abs(int(gpt_year) - int(gem_year)) <= 2)
            )
            name_overlap = len(gpt_tokens & gem_tokens) >= 2
            cit_overlap = len(gpt_nums & gem_cit) >= 2 if (gpt_nums and gem_cit) else False

            if year_match and (name_overlap or cit_overlap):
                best_gem_idx = zi
                break

        if best_gem_idx is not None:
            zc = gem_cases[best_gem_idx]
            used_gem.add(best_gem_idx)
            matched.append({
                "matched": True,
                "gpt_case": gc,
                "gem_case": zc,
                "canonical_name": gc.get("case_name") or zc.get("case_name"),
                "canonical_citation": gc.get("citation") or zc.get("citation"),
                "canonical_year": gc.get("year") or zc.get("year"),
            })
        else:
            matched.append({
                "matched": False,
                "gpt_case": gc,
                "gem_case": None,
                "canonical_name": gc.get("case_name"),
                "canonical_citation": gc.get("citation"),
                "canonical_year": gc.get("year"),
            })

    # Add Gemini-only cases (not matched to any GPT case)
    for zi, zc in enumerate(gem_cases):
        if zi not in used_gem:
            matched.append({
                "matched": False,
                "gpt_case": None,
                "gem_case": zc,
                "canonical_name": zc.get("case_name"),
                "canonical_citation": zc.get("citation"),
                "canonical_year": zc.get("year"),
            })

    return matched


# ── 4-check classification ─────────────────────────────────────────────────────

def _check_citation_consistency(mc: dict) -> tuple:
    """
    Returns ('pass'|'uncertain'|'fail', note).
    Pass: citation numbers overlap between both model versions.
    Uncertain: only one model cited this case.
    Fail: irreconcilable citations.
    """
    if not mc["matched"]:
        return "uncertain", "Only one model cited this case — citation cannot be cross-checked."

    gpt_nums = _citation_nums(mc["gpt_case"].get("citation", ""))
    gem_nums = _citation_nums(mc["gem_case"].get("citation", ""))

    if not gpt_nums and not gem_nums:
        return "uncertain", "Neither model provided a citation."
    if not gpt_nums or not gem_nums:
        return "uncertain", f"Only one model provided a citation number."

    if gpt_nums & gem_nums:
        return "pass", (
            f"Citation numbers overlap. GPT: {mc['gpt_case'].get('citation')}; "
            f"Gemini: {mc['gem_case'].get('citation')}."
        )
    else:
        return "fail", (
            f"Citations do not share numbers — possible different cases or error. "
            f"GPT: {mc['gpt_case'].get('citation')}; Gemini: {mc['gem_case'].get('citation')}."
        )


def _check_holding_accuracy(mc: dict) -> tuple:
    """
    Returns ('pass'|'uncertain', note).
    Pass: both models named the case (independent corroboration of relevance).
    Uncertain: only one model named it (no cross-check possible without attorney).
    """
    if not mc["matched"]:
        return (
            "uncertain",
            "Only one model cited this case — holding accuracy cannot be cross-checked."
        )

    gpt_sum = mc["gpt_case"].get("holding_summary", "")
    gem_sum = mc["gem_case"].get("holding_summary", "")

    # Check for outright contradictions (simple keyword heuristic)
    positive_words = {"established", "recognized", "affirmed", "holds", "held", "defense"}
    negative_words = {"overruled", "rejected", "denied", "reversed"}

    gpt_pos = bool(set(re.findall(r"\w+", gpt_sum.lower())) & positive_words)
    gem_neg = bool(set(re.findall(r"\w+", gem_sum.lower())) & negative_words)
    gem_pos = bool(set(re.findall(r"\w+", gem_sum.lower())) & positive_words)
    gpt_neg = bool(set(re.findall(r"\w+", gpt_sum.lower())) & negative_words)

    if (gpt_pos and gem_neg) or (gem_pos and gpt_neg):
        return (
            "uncertain",
            f"Holding summaries appear contradictory. GPT: '{gpt_sum[:80]}'; Gemini: '{gem_sum[:80]}'. Attorney review required."
        )

    return (
        "pass",
        f"Both models independently identified this case. GPT summary: '{gpt_sum[:80]}'; Gemini: '{gem_sum[:80]}'."
    )


def _check_currency(
    gpt_currency: Optional[dict], gem_currency: Optional[dict], mc: dict
) -> tuple:
    """
    Returns ('pass'|'uncertain'|'fail', note).
    Pass: both verification queries confirm still_good_law=true.
    Uncertain: either query returned uncertain or error.
    Fail: either query says overruled/superseded.
    """
    # Only one model was queried (because only one model identified the case)
    active_currency = None
    source_label = ""
    if gpt_currency and not gpt_currency.get("error") and gem_currency and not gem_currency.get("error"):
        # Both queried
        gpt_slg = gpt_currency.get("currency_status", "uncertain")
        gem_slg = gem_currency.get("currency_status", "uncertain")

        if gpt_slg in ("overruled", "superseded") or gem_slg in ("overruled", "superseded"):
            limiting = (
                gpt_currency.get("limiting_authority")
                or gem_currency.get("limiting_authority")
                or "see notes"
            )
            return (
                "fail",
                f"At least one model flags this case as no longer good law. "
                f"GPT status: {gpt_slg}; Gemini status: {gem_slg}. "
                f"Limiting authority: {limiting}."
            )
        if gpt_slg == "good_law" and gem_slg == "good_law":
            return (
                "pass",
                f"Both models confirm still good law. GPT conf: {gpt_currency.get('confidence')}; Gemini conf: {gem_currency.get('confidence')}."
            )
        # One or both uncertain
        return (
            "uncertain",
            f"Currency uncertain. GPT: {gpt_slg} (conf={gpt_currency.get('confidence')}); Gemini: {gem_slg} (conf={gem_currency.get('confidence')})."
        )

    elif gpt_currency and not gpt_currency.get("error"):
        active_currency = gpt_currency
        source_label = "GPT only"
    elif gem_currency and not gem_currency.get("error"):
        active_currency = gem_currency
        source_label = "Gemini only"
    else:
        return "uncertain", "Currency verification failed (both models errored)."

    slg = active_currency.get("currency_status", "uncertain")
    if slg in ("overruled", "superseded"):
        return "fail", f"{source_label}: case flagged as no longer good law ({slg})."
    if slg == "good_law":
        return "uncertain", f"{source_label} only: confirms good law, but single-model — attorney confirmation required."
    return "uncertain", f"{source_label}: status={slg} (conf={active_currency.get('confidence')})."


def classify_case(
    mc: dict,
    gpt_currency: Optional[dict],
    gem_currency: Optional[dict],
) -> dict:
    """
    Run all 4 checks and produce the final per-case classification.

    Returns a structured result dict.
    """
    # Check 1: Existence (inter-coder)
    if mc["matched"]:
        existence_status = "pass"
        existence_note = "Both models independently identified this case."
    else:
        existence_status = "uncertain"
        source = "GPT" if mc["gpt_case"] else "Gemini"
        existence_note = f"Only {source} cited this case — existence cannot be inter-coder confirmed."

    # Check 2: Citation consistency
    citation_status, citation_note = _check_citation_consistency(mc)

    # Check 3: Holding accuracy
    holding_status, holding_note = _check_holding_accuracy(mc)

    # Check 4: Currency
    currency_status, currency_note = _check_currency(gpt_currency, gem_currency, mc)

    checks = {
        "existence": existence_status,
        "citation_consistency": citation_status,
        "holding_accuracy": holding_status,
        "currency": currency_status,
    }

    # Determine disposition
    passing = all(v == "pass" for v in checks.values())

    if passing:
        disposition = "holdings-draft-corroborated"
        disposition_note = (
            "All 4 checks pass. Draft corroborated — pending attorney confirmation "
            "that case is real, correctly cited, and still good law."
        )
        needs_attorney = False
    else:
        disposition = "holdings-needs-attorney"
        failed_checks = [k for k, v in checks.items() if v != "pass"]
        disposition_note = (
            f"Flagged: {', '.join(failed_checks)} check(s) did not pass. "
            f"Attorney review required before including in canonical holdings."
        )
        needs_attorney = True

    return {
        "case_name": mc["canonical_name"],
        "citation_gpt": mc["gpt_case"].get("citation") if mc["gpt_case"] else None,
        "citation_gemini": mc["gem_case"].get("citation") if mc["gem_case"] else None,
        "citation": mc["canonical_citation"],
        "year": mc["canonical_year"],
        "court_gpt": mc["gpt_case"].get("court") if mc["gpt_case"] else None,
        "court_gemini": mc["gem_case"].get("court") if mc["gem_case"] else None,
        "holding_gpt": mc["gpt_case"].get("holding_summary") if mc["gpt_case"] else None,
        "holding_gemini": mc["gem_case"].get("holding_summary") if mc["gem_case"] else None,
        "inter_coder_match": mc["matched"],
        "checks": checks,
        "check_notes": {
            "existence": existence_note,
            "citation_consistency": citation_note,
            "holding_accuracy": holding_note,
            "currency": currency_note,
        },
        "disposition": disposition,
        "disposition_note": disposition_note,
        "needs_attorney": needs_attorney,
        "currency_gpt": gpt_currency,
        "currency_gemini": gem_currency,
    }


# ── Holdings layer writer ──────────────────────────────────────────────────────

def write_holdings_layer(
    data: dict,
    path: str,
    state_code: str,
    state_name: str,
    gpt_id: dict,
    gem_id: dict,
    case_results: list,
    statutory_only: bool,
    statutory_note: Optional[str],
) -> None:
    """
    Writes layer_decomposition.holdings to the retaliation defense.
    NEVER marks as confirmed. Status is always L2-HOLDINGS-DRAFT.
    Never edits case_law field in the flat structure.
    """
    for defense in data.get("substantive_defenses", []):
        if defense.get("defense") != "retaliation":
            continue

        ld = defense.setdefault("layer_decomposition", {})
        holdings = ld.setdefault("holdings", {})

        draft_corroborated = [r for r in case_results if r["disposition"] == "holdings-draft-corroborated"]
        needs_attorney_cases = [r for r in case_results if r["disposition"] == "holdings-needs-attorney"]

        holdings["validation_method"] = "L2-holdings-4-check-verification"
        holdings["l2_run_date"] = TODAY
        holdings["models"] = {"openai": OPENAI_MODEL, "gemini": GEMINI_MODEL}

        if statutory_only:
            holdings["validation_status"] = "L2-HOLDINGS-DRAFT"
            holdings["statutory_only"] = True
            holdings["statutory_note"] = statutory_note or ""
            holdings["cases_draft_corroborated"] = []
            holdings["cases_needs_attorney"] = []
            holdings["draft_corroborated_count"] = 0
            holdings["needs_attorney_count"] = 0
            holdings["l2_note"] = (
                f"Both models indicate {state_name} retaliation defense is primarily statutory "
                f"with limited significant case law. {statutory_note or ''}"
            )
        else:
            holdings["validation_status"] = "L2-HOLDINGS-DRAFT"
            holdings["statutory_only"] = False

            # Store cases without the full currency raw data (keep file size reasonable)
            def slim_case(r: dict) -> dict:
                return {
                    "case_name": r["case_name"],
                    "citation": r["citation"],
                    "citation_gpt": r["citation_gpt"],
                    "citation_gemini": r["citation_gemini"],
                    "year": r["year"],
                    "court_gpt": r["court_gpt"],
                    "holding_gpt": r["holding_gpt"],
                    "holding_gemini": r["holding_gemini"],
                    "inter_coder_match": r["inter_coder_match"],
                    "disposition": r["disposition"],
                    "disposition_note": r["disposition_note"],
                    "checks": r["checks"],
                    "check_notes": r["check_notes"],
                }

            holdings["cases_draft_corroborated"] = [slim_case(r) for r in draft_corroborated]
            holdings["cases_needs_attorney"] = [slim_case(r) for r in needs_attorney_cases]
            holdings["draft_corroborated_count"] = len(draft_corroborated)
            holdings["needs_attorney_count"] = len(needs_attorney_cases)
            holdings["total_cases_evaluated"] = len(case_results)
            holdings["l2_note"] = (
                f"Phase A: GPT identified {len(gpt_id.get('cases', []))} cases, "
                f"Gemini identified {len(gem_id.get('cases', []))} cases. "
                f"Phase B: {len(case_results)} evaluated; "
                f"{len(draft_corroborated)} draft-corroborated; "
                f"{len(needs_attorney_cases)} needs-attorney. "
                f"ALL draft-corroborated cases require attorney confirmation before public citation."
            )

        holdings["labeling_note"] = (
            "IMPORTANT: No holdings are auto-confirmed. "
            "L2-HOLDINGS-DRAFT status requires attorney review before these cases "
            "may be cited in any public document or legal advice. "
            "Label: holdings-draft-corroborated = AI drafted + 4-check verified; "
            "attorney must confirm case is real, cited correctly, still good law."
        )

        # Add validation flag
        flags = data["validation"].setdefault("flags", [])
        flags.append({
            "layer": "L2",
            "code": "L2-RETALIATION-HOLDINGS-DRAFT",
            "field": "substantive_defenses.retaliation.layer_decomposition.holdings",
            "disposition": "draft-pending-attorney-confirmation",
            "l2_run_date": TODAY,
            "draft_corroborated": len(draft_corroborated),
            "needs_attorney": len(needs_attorney_cases),
            "note": (
                "Holdings draft complete. All cases require attorney confirmation. "
                "Never cite draft-corroborated cases publicly without attorney sign-off."
            ),
        })
        data["validation"]["flags"] = flags

        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")

        return  # done — only one retaliation defense per state


# ── Main runner ────────────────────────────────────────────────────────────────

def run_holdings(target_codes: List[str], dry_run: bool = False) -> list:
    all_data, all_paths = load_all_v2_files()

    missing = [c for c in target_codes if c not in all_data]
    if missing:
        print(f"  WARN: states not found: {missing}")
        target_codes = [c for c in target_codes if c in all_data]

    n = len(target_codes)
    print(f"\n  States: {n} · Hard cap: ${BUDGET_CAP:.2f}")
    print(f"  Phase A: identification (~${APPROX_COST_PHASE_A * n:.2f})")
    print(f"  Phase B: currency verification per case (~${APPROX_COST_PHASE_B:.2f}/case)")
    if dry_run:
        print("  MODE: DRY RUN — no API calls, no write-back")

    results = []
    spend = 0.0
    total_draft = 0
    total_needs_atty = 0
    total_cases = 0
    statutory_only_states = []
    no_cases_states = []

    for code in target_codes:
        data = all_data[code]
        path = all_paths[code]
        state_name = data.get("jurisdiction", {}).get("state_name", code)

        print(f"\n  {code} ({state_name})")

        # ── Phase A: Independent identification ─────────────────────────────
        print(f"    Phase A: identification...")
        gpt_id = call_gpt_identification(state_name, dry_run=dry_run)
        gem_id = call_gemini_identification(state_name, dry_run=dry_run)
        spend += APPROX_COST_PHASE_A

        if gpt_id.get("error"):
            print(f"    GPT error: {gpt_id['error'][:70]}")
            gpt_cases = []
        else:
            gpt_cases = gpt_id.get("cases", [])[:MAX_CASES_PER_MODEL]
            print(f"    GPT: {len(gpt_cases)} cases, conf={gpt_id.get('confidence')}, "
                  f"statutory_only={gpt_id.get('statutory_only')}")

        if gem_id.get("error"):
            print(f"    Gemini error: {gem_id['error'][:70]}")
            gem_cases = []
        else:
            gem_cases = gem_id.get("cases", [])[:MAX_CASES_PER_MODEL]
            print(f"    Gemini: {len(gem_cases)} cases, conf={gem_id.get('confidence')}, "
                  f"statutory_only={gem_id.get('statutory_only')}")

        # Check statutory-only consensus
        gpt_stat = gpt_id.get("statutory_only", False) if not gpt_id.get("error") else None
        gem_stat = gem_id.get("statutory_only", False) if not gem_id.get("error") else None
        statutory_only = bool(gpt_stat and gem_stat)
        statutory_note = (
            gpt_id.get("statutory_note") or gem_id.get("statutory_note")
            if statutory_only else None
        )

        if statutory_only:
            print(f"    → Both models: statutory-only regime (no controlling case law)")
            statutory_only_states.append(code)

        # Handle no-cases scenario
        all_cases = list(gpt_cases) + [c for c in gem_cases if c not in gpt_cases]
        if not gpt_cases and not gem_cases:
            print(f"    → No cases identified by either model")
            no_cases_states.append(code)

        # ── Case matching ────────────────────────────────────────────────────
        matched_cases = match_cases(gpt_cases, gem_cases) if (gpt_cases or gem_cases) else []
        inter_coder_count = sum(1 for mc in matched_cases if mc["matched"])
        print(f"    Matched cases: {inter_coder_count}/{len(matched_cases)} inter-coder")

        # ── Phase B: Currency verification per case ──────────────────────────
        case_results = []
        for mc in matched_cases:
            case_name = mc["canonical_name"] or "Unknown"
            citation = mc["canonical_citation"] or ""
            year = mc["canonical_year"] or 0

            # Decide which model to query for currency
            # If only one model identified the case, only that model does currency check
            should_gpt = mc["gpt_case"] is not None
            should_gem = mc["gem_case"] is not None

            print(f"      [{code}] Currency check: {case_name[:50]}...")
            gpt_curr = None
            gem_curr = None

            if not dry_run:
                if should_gpt:
                    gpt_curr = call_gpt_currency(state_name, case_name, citation, year)
                    spend += APPROX_COST_PHASE_B / 2
                if should_gem:
                    gem_curr = call_gemini_currency(state_name, case_name, citation, year)
                    spend += APPROX_COST_PHASE_B / 2
            else:
                if should_gpt:
                    gpt_curr = DRY_RUN_CURRENCY.copy()
                if should_gem:
                    gem_curr = DRY_RUN_CURRENCY.copy()

            gpt_cs = gpt_curr.get("currency_status", "?") if gpt_curr else "not-queried"
            gem_cs = gem_curr.get("currency_status", "?") if gem_curr else "not-queried"
            print(f"        GPT currency: {gpt_cs} | Gemini currency: {gem_cs}")

            classified = classify_case(mc, gpt_curr, gem_curr)
            case_results.append(classified)

            if spend >= BUDGET_CAP:
                print(f"\n  ⚠️  BUDGET CAP HIT (~${spend:.2f}). Stopping case processing for {code}.")
                break

        # State totals
        draft_count = sum(1 for r in case_results if r["disposition"] == "holdings-draft-corroborated")
        atty_count = sum(1 for r in case_results if r["disposition"] == "holdings-needs-attorney")
        total_draft += draft_count
        total_needs_atty += atty_count
        total_cases += len(case_results)

        for r in case_results:
            status = "✅ DRAFT" if r["disposition"] == "holdings-draft-corroborated" else "🔍 NEEDS-ATTORNEY"
            failed = [k for k, v in r["checks"].items() if v != "pass"]
            print(f"      {status}: {r['case_name'][:50]} ({r['year']}) — "
                  f"{'ALL PASS' if not failed else 'FAILED: '+', '.join(failed)}")

        state_result = {
            "state": code,
            "state_name": state_name,
            "statutory_only": statutory_only,
            "gpt_identification": gpt_id,
            "gem_identification": gem_id,
            "cases_evaluated": len(case_results),
            "draft_corroborated": draft_count,
            "needs_attorney": atty_count,
            "case_results": case_results,
            "landmark_watch": code in LANDMARK_WATCH,
            "landmark_note": LANDMARK_WATCH.get(code),
        }
        results.append(state_result)

        if not dry_run:
            write_holdings_layer(
                data, path, code, state_name,
                gpt_id, gem_id, case_results,
                statutory_only, statutory_note,
            )

        if spend >= BUDGET_CAP:
            print(f"\n  ⚠️  BUDGET CAP HIT (~${spend:.2f}). Stopping at {code}.")
            break

    # Save raw output
    output_path = OUTPUT_DIR / f"retaliation_holdings_l2_raw_{TODAY}.json"
    if not dry_run:
        with open(output_path, "w") as f:
            json.dump({
                "run_date": TODAY,
                "module": "Retaliation Holdings Layer L2 — 4-Check Verification",
                "models": {"openai": OPENAI_MODEL, "gemini": GEMINI_MODEL},
                "states_run": len(results),
                "spend_estimate": spend,
                "total_cases_evaluated": total_cases,
                "total_draft_corroborated": total_draft,
                "total_needs_attorney": total_needs_atty,
                "statutory_only_states": statutory_only_states,
                "no_cases_states": no_cases_states,
                "results": results,
            }, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"\n  Raw output saved: {output_path}")

    # ── Summary ────────────────────────────────────────────────────────────────
    print(f"\n{'=' * 70}")
    print(f"  Retaliation Holdings L2 — {len(results)} states | ~${spend:.2f}")
    print(f"  Cases evaluated:          {total_cases}")
    print(f"  ✅ DRAFT-CORROBORATED:    {total_draft}  (all 4 checks pass; attorney confirms)")
    print(f"  🔍 NEEDS-ATTORNEY:         {total_needs_atty}  (any check failed/uncertain)")
    if total_cases > 0:
        atty_pct = total_needs_atty / total_cases * 100
        draft_pct = total_draft / total_cases * 100
        print(f"  Draft rate:               {draft_pct:.0f}%")
        print(f"  Attorney-needed rate:     {atty_pct:.0f}%  (expected ~30–40%)")
    if statutory_only_states:
        print(f"  Statutory-only states:    {statutory_only_states}")
    if no_cases_states:
        print(f"  No cases identified:      {no_cases_states}")
    print(f"  Landmark-watch states:    {[r['state'] for r in results if r.get('landmark_watch')]}")
    print(f"{'=' * 70}")

    print(f"\n  CRITICAL REMINDER: NO holdings are auto-confirmed.")
    print(f"  DRAFT-CORROBORATED = AI verified via 4 checks; attorney must still confirm.")
    print(f"  Only attorney-signed-off holdings may be cited publicly.")
    print(f"\n  ⚠️  STOP AND REPORT. Share output file with Cowork for ingestion.")
    print(f"  Output: {output_path if not dry_run else '(dry run — no output)'}")

    return results


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Retaliation Holdings L2 Runner — Civil Justice as Code"
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

    print(f"\nCivil Justice as Code — Retaliation Holdings L2 Runner (Step 2)")
    print(f"Run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Models: {OPENAI_MODEL} + {GEMINI_MODEL}")
    print(f"Protocol: Phase A identification → Phase B 4-check verification")
    print(f"          existence | citation | holding-accuracy | currency")
    print(f"Budget cap: ${BUDGET_CAP:.2f}")
    print(f"CRITICAL: Nothing auto-confirmed. All holdings are L2-HOLDINGS-DRAFT.")
    print(f"Landmark watch: {list(LANDMARK_WATCH.keys())}")
    print(f"NOTE: No file case_law values fed to models. Neutral queries only.")

    target = [s.strip().upper() for s in args.states.split(",") if s.strip()]
    print(f"States: {len(target)}")

    run_holdings(
        target_codes=target,
        dry_run=args.dry_run,
    )
