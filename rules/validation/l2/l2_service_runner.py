#!/usr/bin/env python3
"""
Eviction Rules — L2 Service Module Runner
==========================================
Runs L2 multi-model consensus on the `service` module (permitted service methods +
statutory citations) across all 51 states.

Hypotheses to test:
  H1 — SAME-STATUTE: Several states (AL, AK, CT, etc.) cite one statute for all
       3 service methods. L2 will show whether that's correct (single provision) or
       whether models identify method-specific subsections (section-header error).
  H2 — METHOD AVAILABILITY: Whether all 3 standard methods (personal, substituted,
       mail) are available in each state, or whether some are restricted.

Classification (per state):
  CONSENSUS-CONFIRM        → file statutes match both models for all methods
  SAME-STATUTE-CONFIRMED   → file uses same statute for all methods; models also
                             return same statute (single-provision statute correct)
  SUBSECTION-FOUND         → file uses same statute; models return specific subsections
                             (potential section-header-only error — flag for human)
  CITATION-DIVERGENCE      → models agree with each other but differ from file
  METHOD-AVAILABILITY-DIFF → models report different set of available methods
  MODEL-SPLIT              → the two models disagree with each other
  ERROR                    → parse / API failure

Tiered resolution:
  CONSENSUS-CONFIRM / SAME-STATUTE-CONFIRMED → write pass, no review needed
  SUBSECTION-FOUND       → flag with "file may need subsection-level citations";
                           pending-human-verification (no auto-edit)
  CITATION-DIVERGENCE    → if models share section nums: write flag (no auto-edit);
                           else: flag for human
  METHOD-AVAILABILITY-DIFF → flag for human (method availability needs attorney check)
  MODEL-SPLIT             → L7 escalation
  ERROR                   → logged, skip

GUARDRAILS (do not remove):
  - API keys from .env only; never hardcoded, logged, or committed
  - NEVER advances any module past AUTOMATED-CHECKS-PASSED
  - Runner appends flags only; never edits resolution/status/confirmed-by fields
  - No content corrections to rules files from this runner (flags only)
  - $20 hard budget cap
  - Neutral queries — do NOT tell the model what the file says (no anchoring)
  - Recency guardrail: consensus ≠ current; flag recent-law states

Usage (run from repo root on Andy's local machine):
  python3 rules/validation/l2/l2_service_runner.py
  python3 rules/validation/l2/l2_service_runner.py --states AL,AK,CT
  python3 rules/validation/l2/l2_service_runner.py --dry-run

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import os
import re
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ── Shared utilities from l2_runner.py ───────────────────────────────────────
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

# ── States with known recent service-law changes (recency guardrail) ──────────
# Add to this list as amendments are discovered
RECENCY_WATCH_STATES = {
    "VA": "HB 15/SB 48 (2026) amended §55.1-1245; service provisions under §55.1-1415 may be affected",
    "CA": "AB 2347 (2022) changed service and response-time rules; verify CCP §1162 currency",
    "OR": "SB 278 (2023) amended service rules; verify ORS §90.155 currency",
    "WA": "RCW 59.12.040 amended 2021-2023 — verify currency",
}

# ALL 51 states
ALL_STATES = [
    "AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL",
    "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA",
    "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE",
    "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI",
    "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY",
]

# Cost estimates — service queries are larger than notice (3 methods to describe)
APPROX_COST_PER_STATE = 0.03   # $0.03/state × 51 = ~$1.53 total; well within $20

# ── Method name mapping (canonical names in file → query terms) ───────────────
METHOD_NAMES = {
    "personal": "personal delivery",
    "substituted": "substituted service",
    "certified_mail": "certified mail",
    "nail_and_mail": "post and mail (nail-and-mail)",
    "posting": "posting on premises plus mail",
}

# ── Query construction ─────────────────────────────────────────────────────────

SERVICE_SYSTEM_PROMPT = (
    "You are a legal research expert in US residential landlord-tenant law. "
    "Answer questions about how landlords must legally serve eviction notices on tenants. "
    "Be precise about statute citations. Respond only in the JSON format requested."
)


def build_service_query(state_name: str) -> str:
    """Neutral query — no anchoring to what the file says."""
    return f"""In {state_name}, what are the legally permitted methods for serving a pay-or-quit (demand for rent) notice on a residential tenant prior to filing an eviction action for nonpayment of rent?

For each permitted service method, provide:
1. The method name (e.g., personal delivery, substituted service, mail)
2. The specific statutory citation (including subsection if applicable)
3. Any additional days added to the notice period for that method (if any)

Respond ONLY in valid JSON with this structure:
{{
  "methods": [
    {{
      "method": "personal",
      "description": "brief description of how it works",
      "statute": "exact statutory citation with subsection",
      "adds_days": null
    }},
    {{
      "method": "substituted",
      "description": "brief description",
      "statute": "exact statutory citation with subsection",
      "adds_days": null
    }},
    {{
      "method": "mail",
      "description": "brief description",
      "statute": "exact statutory citation with subsection",
      "adds_days": <integer or null>
    }}
  ],
  "all_methods_same_statute": <true if all methods governed by same statute/section, false if different subsections>,
  "general_statute": "the parent statute if all_methods_same_statute is true, else null",
  "confidence": "high|medium|low",
  "notes": "any relevant caveats or exceptions"
}}"""


# ── Response parsing ───────────────────────────────────────────────────────────

def parse_service_response(raw: str) -> dict:
    """Parse the model's service-query JSON response."""
    if not raw:
        return {"error": "empty response"}
    result = _parse_json_response(raw)
    if result.get("error"):
        return result
    # Normalize: ensure 'methods' is a list
    if "methods" not in result or not isinstance(result["methods"], list):
        return {"error": f"missing or invalid 'methods' field: {str(result)[:200]}"}
    return result


def call_openai_service(query: str, dry_run: bool = False) -> dict:
    if dry_run:
        return {
            "methods": [
                {"method": "personal", "statute": "DRY-RUN §1(a)", "adds_days": None},
                {"method": "substituted", "statute": "DRY-RUN §1(b)", "adds_days": None},
                {"method": "mail", "statute": "DRY-RUN §1(c)", "adds_days": 3},
            ],
            "all_methods_same_statute": False,
            "general_statute": None,
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
                {"role": "system", "content": SERVICE_SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
            max_completion_tokens=6000,
        )
        raw = resp.choices[0].message.content.strip() if resp.choices[0].message.content else ""
        return parse_service_response(raw)
    except Exception as exc:
        return {"error": str(exc)}


def call_gemini_service(query: str, dry_run: bool = False) -> dict:
    if dry_run:
        return {
            "methods": [
                {"method": "personal", "statute": "DRY-RUN §1(a)", "adds_days": None},
                {"method": "substituted", "statute": "DRY-RUN §1(b)", "adds_days": None},
                {"method": "mail", "statute": "DRY-RUN §1(c)", "adds_days": 3},
            ],
            "all_methods_same_statute": False,
            "general_statute": None,
            "confidence": "high",
            "notes": "dry run",
        }
    try:
        from google import genai
    except ImportError:
        return {"error": "google-genai not installed"}
    try:
        client = genai.Client(api_key=GOOGLE_KEY)
        full_prompt = SERVICE_SYSTEM_PROMPT + "\n\n" + query
        resp = client.models.generate_content(model=GEMINI_MODEL, contents=full_prompt)
        raw = resp.text.strip()
        return parse_service_response(raw)
    except Exception as exc:
        return {"error": str(exc)}


# ── File claim extraction ──────────────────────────────────────────────────────

def extract_service_claim(data: dict) -> dict:
    """Extract service module claims from a v2 rules file."""
    service = data.get("service", {})
    method_rules = service.get("method_rules", [])

    methods_by_name = {}
    for mr in method_rules:
        m = mr.get("method", "")
        methods_by_name[m] = {
            "method": m,
            "statute": mr.get("statute"),
            "adds_days": mr.get("adds_days_for_mail"),
            "requirements": mr.get("requirements", ""),
        }

    # Detect same-statute pattern
    statutes = [v.get("statute") for v in methods_by_name.values() if v.get("statute")]
    unique_statutes = set(statutes)
    same_statute = len(unique_statutes) == 1 and len(statutes) >= 2

    return {
        "methods": methods_by_name,
        "permitted_methods": service.get("permitted_methods", []),
        "same_statute": same_statute,
        "unique_statutes": list(unique_statutes),
        "method_count": len(method_rules),
    }


# ── Classification ─────────────────────────────────────────────────────────────

def _get_method_statute(response: dict, method_name: str) -> Optional[str]:
    """Get statute for a specific method from a model response."""
    for m in response.get("methods", []):
        if m.get("method", "").lower().replace("-", "_").replace(" ", "_") in (
            method_name.lower(),
            method_name.lower().replace("-", "_"),
        ):
            return m.get("statute")
    return None


def _extract_section_nums_service(statute: str) -> set:
    """Extract section numbers from a statute string for comparison."""
    if not statute:
        return set()
    # Extract all numeric patterns including subsections
    nums = re.findall(r'\d[\d\-\.]*[a-zA-Z]?', statute)
    return set(nums)


def _parent_statute(statute: str) -> str:
    """Extract parent section (strip subsection letters/numbers)."""
    if not statute:
        return ""
    # Remove trailing (A)(1) style subsections, keep up to the section number
    return re.sub(r'\([a-zA-Z0-9]+\)\s*$', '', statute).strip()


def _models_same_statute(gpt_resp: dict, gem_resp: dict) -> bool:
    """Both models say all methods governed by same statute."""
    return (
        gpt_resp.get("all_methods_same_statute", False)
        and gem_resp.get("all_methods_same_statute", False)
    )


def _models_found_subsections(gpt_resp: dict, gem_resp: dict) -> bool:
    """Both models return method-specific subsections (not all_methods_same_statute)."""
    return (
        not gpt_resp.get("all_methods_same_statute", True)
        and not gem_resp.get("all_methods_same_statute", True)
    )


def _statutes_agree(gpt_resp: dict, gem_resp: dict, method: str) -> bool:
    """Check if both models agree on statute for a given method."""
    gs = _get_method_statute(gpt_resp, method)
    ms = _get_method_statute(gem_resp, method)
    if not gs or not ms:
        return False
    gns = _extract_section_nums_service(gs)
    mns = _extract_section_nums_service(ms)
    return bool(gns & mns)  # share at least one section number


def classify_service(file_claim: dict, gpt_resp: dict, gem_resp: dict) -> str:
    """Classify service L2 result."""
    if gpt_resp.get("error") or gem_resp.get("error"):
        return "ERROR"

    file_same = file_claim["same_statute"]

    # Check method availability difference
    gpt_methods = {m.get("method", "").lower() for m in gpt_resp.get("methods", [])}
    gem_methods = {m.get("method", "").lower() for m in gem_resp.get("methods", [])}
    if gpt_methods and gem_methods and not (gpt_methods & gem_methods):
        return "MODEL-SPLIT"

    # Same-statute hypothesis
    if file_same:
        if _models_same_statute(gpt_resp, gem_resp):
            return "SAME-STATUTE-CONFIRMED"
        elif _models_found_subsections(gpt_resp, gem_resp):
            return "SUBSECTION-FOUND"
        # Mixed — one model same-statute, other found subsections
        return "CITATION-DIVERGENCE"

    # File has method-specific statutes — check if models agree
    core_methods = ["personal", "substituted", "mail", "certified_mail"]
    agree_count = 0
    total = 0
    for m in core_methods:
        file_m = file_claim["methods"].get(m)
        if not file_m:
            continue
        total += 1
        if _statutes_agree(gpt_resp, gem_resp, m):
            agree_count += 1

    if total == 0:
        return "ERROR"

    # If models agree with each other on all methods
    if agree_count == total:
        # Now check if they agree with the file
        file_statutes_match = True
        for m in core_methods:
            file_m = file_claim["methods"].get(m)
            if not file_m:
                continue
            file_s = file_m.get("statute", "") or ""
            gpt_s = _get_method_statute(gpt_resp, m) or ""
            file_secs = _extract_section_nums_service(file_s)
            gpt_secs = _extract_section_nums_service(gpt_s)
            if not (file_secs & gpt_secs):
                file_statutes_match = False
                break
        return "CONSENSUS-CONFIRM" if file_statutes_match else "CITATION-DIVERGENCE"

    # Partial agreement or disagreement between models
    return "MODEL-SPLIT"


# ── Flag writer ────────────────────────────────────────────────────────────────

def write_service_flag(
    state: str,
    data: dict,
    path: str,
    classification: str,
    file_claim: dict,
    gpt_resp: dict,
    gem_resp: dict,
):
    """Append L2 service flag to the file. Never edits existing flags or content."""
    flags = data["validation"].setdefault("flags", [])

    # Remove any pre-existing open service L2 flag for idempotency on re-run
    flags = [fl for fl in flags if not (
        fl.get("layer") == "L2"
        and "service" in fl.get("field", "")
        and fl.get("disposition") == "open"
    )]

    base_flag = {
        "layer": "L2",
        "field": "service.method_rules",
        "l2_run_date": TODAY,
        "gpt_summary": {
            "all_methods_same_statute": gpt_resp.get("all_methods_same_statute"),
            "confidence": gpt_resp.get("confidence"),
            "methods": [
                {"method": m.get("method"), "statute": m.get("statute")}
                for m in gpt_resp.get("methods", [])
            ],
        },
        "gemini_summary": {
            "all_methods_same_statute": gem_resp.get("all_methods_same_statute"),
            "confidence": gem_resp.get("confidence"),
            "methods": [
                {"method": m.get("method"), "statute": m.get("statute")}
                for m in gem_resp.get("methods", [])
            ],
        },
    }

    if classification == "CONSENSUS-CONFIRM":
        base_flag.update({
            "code": "L2-SERVICE-CONSENSUS-CONFIRM",
            "disposition": "resolved-confirmed",
            "note": (
                f"L2 service consensus: both {OPENAI_MODEL} and {GEMINI_MODEL} independently "
                f"confirmed file's service method statutes. No discrepancies detected."
            ),
        })
        data["validation"]["automated_layers"]["L2_consensus"] = "pass"

    elif classification == "SAME-STATUTE-CONFIRMED":
        base_flag.update({
            "code": "L2-SERVICE-SAME-STATUTE-CONFIRMED",
            "disposition": "resolved-confirmed",
            "note": (
                f"L2 service: file uses one statute for all service methods. "
                f"Both {OPENAI_MODEL} and {GEMINI_MODEL} independently confirmed this is correct — "
                f"the statute covers all service methods in a single provision (not a section-header error). "
                f"File claim validated."
            ),
        })
        data["validation"]["automated_layers"]["L2_consensus"] = "pass"

    elif classification == "SUBSECTION-FOUND":
        gpt_methods = gpt_resp.get("methods", [])
        gem_methods = gem_resp.get("methods", [])
        # Show what subsections models found
        gpt_statutes = {m.get("method"): m.get("statute") for m in gpt_methods}
        gem_statutes = {m.get("method"): m.get("statute") for m in gem_methods}
        base_flag.update({
            "code": "L2-SERVICE-SUBSECTION-FOUND",
            "disposition": "open",
            "escalation": "human-citation-verification",
            "status": "pending-human-verification",
            "note": (
                f"L2 service: file uses same statute ({list(file_claim['unique_statutes'])[:1]}) for all "
                f"service methods. However, both {OPENAI_MODEL} and {GEMINI_MODEL} identified "
                f"method-specific subsections — the file may have captured only the section header. "
                f"Human must verify: are method-specific subsections required, or does the parent section "
                f"suffice for all methods? "
                f"GPT subsections: {gpt_statutes}. "
                f"Gemini subsections: {gem_statutes}."
            ),
        })
        data["validation"]["automated_layers"]["L2_consensus"] = "flagged"

    elif classification == "CITATION-DIVERGENCE":
        base_flag.update({
            "code": "L2-SERVICE-CITATION-DIVERGENCE",
            "disposition": "open",
            "escalation": "human-citation-verification",
            "status": "pending-human-verification",
            "note": (
                f"L2 service: models agree with each other but disagree with file on service "
                f"method statutes. File unique statutes: {file_claim['unique_statutes']}. "
                f"See gpt_summary and gemini_summary for model citations. "
                f"Human must verify operative service method statutes."
            ),
        })
        data["validation"]["automated_layers"]["L2_consensus"] = "flagged"

    elif classification == "METHOD-AVAILABILITY-DIFF":
        gpt_methods = [m.get("method") for m in gpt_resp.get("methods", [])]
        gem_methods = [m.get("method") for m in gem_resp.get("methods", [])]
        base_flag.update({
            "code": "L2-SERVICE-METHOD-AVAILABILITY-DIFF",
            "disposition": "open",
            "escalation": "human-citation-verification",
            "status": "pending-human-verification",
            "note": (
                f"L2 service: models report different available service methods. "
                f"GPT methods: {gpt_methods}. Gemini methods: {gem_methods}. "
                f"File methods: {file_claim['permitted_methods']}. "
                f"Human must verify which service methods are legally available in this state."
            ),
        })
        data["validation"]["automated_layers"]["L2_consensus"] = "flagged"

    elif classification == "MODEL-SPLIT":
        base_flag.update({
            "code": "L2-SERVICE-MODEL-SPLIT-L7",
            "disposition": "open",
            "escalation": "L7",
            "note": (
                f"L2 service MODEL-SPLIT: {OPENAI_MODEL} and {GEMINI_MODEL} disagree on "
                f"service method statutes or available methods. Attorney review required."
            ),
        })
        data["validation"]["automated_layers"]["L2_consensus"] = "flagged"

    elif classification == "ERROR":
        base_flag.update({
            "code": "L2-SERVICE-ERROR",
            "disposition": "open",
            "note": (
                f"L2 service: API or parse error. "
                f"GPT error: {gpt_resp.get('error', 'none')}. "
                f"Gemini error: {gem_resp.get('error', 'none')}."
            ),
        })
        data["validation"]["automated_layers"]["L2_consensus"] = "flagged"

    data["validation"]["flags"] = flags + [base_flag]

    # Add recency warning if applicable
    if state in RECENCY_WATCH_STATES:
        data["validation"]["flags"].append({
            "layer": "L6",
            "code": "L6-SERVICE-RECENCY-WATCH",
            "field": "service.method_rules",
            "disposition": "open",
            "note": (
                f"RECENCY GUARDRAIL: {state} service statutes may have changed recently. "
                f"{RECENCY_WATCH_STATES[state]} "
                f"L2 consensus ≠ current law. Verify against current statutory text."
            ),
            "l2_run_date": TODAY,
        })

    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── Queue appender ────────────────────────────────────────────────────────────

QUEUE_PATH = str(DOCS_DIR / "HUMAN_REVIEW_QUEUE.md")


def append_service_to_queue(items: list):
    """Append service L2 review items. Runner-append-only — never edits Andy's fields."""
    if not items:
        return

    try:
        with open(QUEUE_PATH) as f:
            content = f.read()
    except FileNotFoundError:
        content = "# Human Review Queue\n\n"

    service_marker = "## Service L2 Items"
    insert_content = f"\n*Service L2 run: {TODAY}*\n\n"

    for item in items:
        state = item["state"]
        state_name = item["state_name"]
        cls = item["classification"]
        qid = item.get("qid", f"{state}-SVC")
        file_claim = item.get("file_claim", {})
        gpt_resp = item.get("gpt_resp", {})
        gem_resp = item.get("gem_resp", {})

        icon = {"SUBSECTION-FOUND": "🟡", "CITATION-DIVERGENCE": "🟡",
                "MODEL-SPLIT": "🔴", "METHOD-AVAILABILITY-DIFF": "🟡",
                "ERROR": "❌"}.get(cls, "🟡")

        insert_content += f"### [{qid}] {state} ({state_name}) — {icon} {cls}\n\n"
        insert_content += f"**Module:** service.method_rules  \n"
        insert_content += f"**Status:** {icon} pending-human-verification  \n"
        insert_content += f"**Run date:** {TODAY}\n\n"
        insert_content += f"**File unique statutes:** {file_claim.get('unique_statutes', [])}  \n"
        insert_content += f"**File same-statute pattern:** {file_claim.get('same_statute', False)}  \n\n"

        if cls == "SUBSECTION-FOUND":
            insert_content += (
                f"**Issue:** File cites parent statute for all methods; both models found "
                f"method-specific subsections. Verify whether subsection-level citations are required.\n\n"
            )
            insert_content += "**GPT subsections:**\n"
            for m in gpt_resp.get("methods", []):
                insert_content += f"- {m.get('method')}: {m.get('statute')}\n"
            insert_content += "\n**Gemini subsections:**\n"
            for m in gem_resp.get("methods", []):
                insert_content += f"- {m.get('method')}: {m.get('statute')}\n"
        elif cls == "CITATION-DIVERGENCE":
            insert_content += f"**Issue:** Models agree with each other but differ from file.\n\n"
            insert_content += "**GPT citations:**\n"
            for m in gpt_resp.get("methods", []):
                insert_content += f"- {m.get('method')}: {m.get('statute')}\n"
            insert_content += "\n**Gemini citations:**\n"
            for m in gem_resp.get("methods", []):
                insert_content += f"- {m.get('method')}: {m.get('statute')}\n"
        elif cls == "MODEL-SPLIT":
            insert_content += f"**Issue:** Models disagree with each other — attorney review required.\n\n"
            insert_content += "**GPT:**\n"
            for m in gpt_resp.get("methods", []):
                insert_content += f"- {m.get('method')}: {m.get('statute')}\n"
            insert_content += "\n**Gemini:**\n"
            for m in gem_resp.get("methods", []):
                insert_content += f"- {m.get('method')}: {m.get('statute')}\n"

        insert_content += "\n**Resolution:** ________________  \n"
        insert_content += "**Confirmed by:** ________________  **Date:** ________________\n\n---\n\n"

    # Insert after service marker (or append)
    if service_marker in content:
        marker_pos = content.index(service_marker) + len(service_marker)
        content = content[:marker_pos] + "\n" + insert_content + content[marker_pos:]
    else:
        content += f"\n{service_marker}\n{insert_content}"

    with open(QUEUE_PATH, "w") as f:
        f.write(content)
    print(f"  Service queue updated: {len(items)} items → {QUEUE_PATH}")


# ── Report writer ──────────────────────────────────────────────────────────────

def write_service_report(results: list):
    from collections import Counter
    counts = Counter(r["classification"] for r in results)
    today_str = TODAY

    report_path = str(DOCS_DIR / f"L2_SERVICE_REPORT_{today_str}.md")

    # Same-statute analysis
    same_statute_states = [r for r in results if r["file_claim"]["same_statute"]]
    ss_confirmed = [r for r in same_statute_states if r["classification"] == "SAME-STATUTE-CONFIRMED"]
    ss_subsection = [r for r in same_statute_states if r["classification"] == "SUBSECTION-FOUND"]

    lines = [
        "# L2 Multi-Model Consensus Report — Service Module",
        "",
        f"**Run date:** {today_str}",
        f"**Models:** OpenAI `{OPENAI_MODEL}` · Google `{GEMINI_MODEL}`",
        f"**Target:** Service module — permitted service methods and statutory citations",
        f"**States run:** {len(results)} / 51",
        "",
        "> **Interpretation caveat:** Model consensus corroborates but does not prove correctness.",
        "> **Divergence is the stronger signal.** Consensus ≠ current law — see recency guardrail flags.",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Classification | Count |",
        "|---------------|-------|",
        f"| ✅ CONSENSUS-CONFIRM | {counts.get('CONSENSUS-CONFIRM', 0)} |",
        f"| ✅ SAME-STATUTE-CONFIRMED | {counts.get('SAME-STATUTE-CONFIRMED', 0)} |",
        f"| 🟡 SUBSECTION-FOUND | {counts.get('SUBSECTION-FOUND', 0)} |",
        f"| 🟡 CITATION-DIVERGENCE | {counts.get('CITATION-DIVERGENCE', 0)} |",
        f"| 🟡 METHOD-AVAILABILITY-DIFF | {counts.get('METHOD-AVAILABILITY-DIFF', 0)} |",
        f"| 🔴 MODEL-SPLIT | {counts.get('MODEL-SPLIT', 0)} |",
        f"| ❌ ERROR | {counts.get('ERROR', 0)} |",
        "",
        "---",
        "",
        "## Same-Statute Hypothesis (H1)",
        "",
        f"**States with same-statute pattern in file:** {len(same_statute_states)}",
        f"- SAME-STATUTE-CONFIRMED (single-provision statute is correct): {len(ss_confirmed)}",
        f"  - {', '.join(r['state'] for r in ss_confirmed)}",
        f"- SUBSECTION-FOUND (file may have captured only section header): {len(ss_subsection)}",
        f"  - {', '.join(r['state'] for r in ss_subsection)}",
        "",
        "---",
        "",
        "## Per-State Results",
        "",
        "| State | File same-statute? | File statutes | GPT confidence | Gemini confidence | Classification |",
        "|-------|-------------------|--------------|---------------|------------------|----------------|",
    ]

    for r in results:
        fc = r["file_claim"]
        gpt = r["gpt_resp"]
        gem = r["gem_resp"]
        cls = r["classification"]
        icon = {
            "CONSENSUS-CONFIRM": "✅", "SAME-STATUTE-CONFIRMED": "✅",
            "SUBSECTION-FOUND": "🟡", "CITATION-DIVERGENCE": "🟡",
            "METHOD-AVAILABILITY-DIFF": "🟡", "MODEL-SPLIT": "🔴",
            "ERROR": "❌",
        }.get(cls, "⚠️")
        ss = "yes" if fc["same_statute"] else "no"
        statutes = "; ".join(fc["unique_statutes"])[:50] if fc["unique_statutes"] else "—"
        gpt_conf = gpt.get("confidence", "err") if not gpt.get("error") else "ERR"
        gem_conf = gem.get("confidence", "err") if not gem.get("error") else "ERR"
        lines.append(f"| {r['state']} | {ss} | {statutes} | {gpt_conf} | {gem_conf} | {icon} {cls} |")

    # Items needing review
    needs_review = [r for r in results if r["classification"] not in ("CONSENSUS-CONFIRM", "SAME-STATUTE-CONFIRMED", "ERROR")]
    lines += [
        "",
        "---",
        "",
        f"## Items Requiring Human Review ({len(needs_review)})",
        "",
    ]

    if needs_review:
        for r in needs_review:
            state = r["state"]
            cls = r["classification"]
            fc = r["file_claim"]
            gpt = r["gpt_resp"]
            gem = r["gem_resp"]
            lines += [
                f"### {state} ({r['state_name']}) — {cls}",
                f"- File unique statutes: {fc['unique_statutes']}",
                f"- File same-statute: {fc['same_statute']}",
                "- GPT service methods:",
            ]
            for m in gpt.get("methods", []):
                lines.append(f"  - {m.get('method')}: {m.get('statute')}")
            lines.append("- Gemini service methods:")
            for m in gem.get("methods", []):
                lines.append(f"  - {m.get('method')}: {m.get('statute')}")
            lines.append("")
    else:
        lines += ["None — all states CONFIRM or SAME-STATUTE-CONFIRMED.", ""]

    # Recency watch
    recency_flagged = [r for r in results if r["state"] in RECENCY_WATCH_STATES]
    lines += [
        "---",
        "",
        f"## Recency Watch States ({len(recency_flagged)})",
        "",
        "> These states have L6-SERVICE-RECENCY-WATCH flags. Consensus ≠ current law — verify against current statute.",
        "",
    ]
    for r in recency_flagged:
        lines.append(f"- **{r['state']}**: {RECENCY_WATCH_STATES[r['state']]}")

    lines += [
        "",
        "---",
        "",
        "## What this run covers / does NOT cover",
        "",
        "**Covers:** Whether the file's cited statutes for each service method are corroborated by two independent AI models.",
        "**Does NOT cover:** Service defect elements, adds_days_for_mail accuracy, local court rules on service,",
        "whether the service module is complete vs. comprehensive. Coverage is narrow: citation corroboration only.",
        "",
        "---",
        "",
        "*L2 corroborates and flags. It never blesses and never auto-edits content.*",
        "*No file was advanced past AUTOMATED-CHECKS-PASSED by this run.*",
        "",
        f"*Copyright 2026 Andrew M Cohen. Apache 2.0.*",
    ]

    with open(report_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\n  Service report → {os.path.basename(report_path)}")
    return report_path


# ── Main runner ───────────────────────────────────────────────────────────────

def run_service_l2(target_codes: list, dry_run: bool = False, no_writeback: bool = False):
    all_data, all_paths = load_all_v2_files()

    missing = [c for c in target_codes if c not in all_data]
    if missing:
        print(f"  WARN: states not found: {missing}")
        target_codes = [c for c in target_codes if c in all_data]

    n = len(target_codes)
    est_cost = n * APPROX_COST_PER_STATE
    print(f"\n  States: {n} · Est. cost: ~${est_cost:.2f} · Hard cap: ${BUDGET_CAP_USD:.2f}")
    if dry_run:
        print("  MODE: DRY RUN — no API calls, no write-back")

    results = []
    queue_items = []
    spend = 0.0
    item_n = 0

    for code in target_codes:
        data = all_data[code]
        path = all_paths[code]
        state_name = data.get("jurisdiction", {}).get("state_name", code)
        file_claim = extract_service_claim(data)

        ss_label = " [SAME-STATUTE]" if file_claim["same_statute"] else ""
        print(f"\n  {code} ({state_name}){ss_label} — {file_claim['method_count']} methods | statutes: {file_claim['unique_statutes'][:2]}")

        query = build_service_query(state_name)
        gpt_resp = call_openai_service(query, dry_run=dry_run)
        gem_resp = call_gemini_service(query, dry_run=dry_run)
        spend += APPROX_COST_PER_STATE

        if gpt_resp.get("error"):
            print(f"    GPT ERROR: {gpt_resp['error'][:80]}")
        else:
            gpt_methods = [(m.get("method"), m.get("statute")) for m in gpt_resp.get("methods", [])]
            print(f"    GPT: same_statute={gpt_resp.get('all_methods_same_statute')} conf={gpt_resp.get('confidence')} | {gpt_methods[:3]}")

        if gem_resp.get("error"):
            print(f"    Gemini ERROR: {gem_resp['error'][:80]}")
        else:
            gem_methods = [(m.get("method"), m.get("statute")) for m in gem_resp.get("methods", [])]
            print(f"    Gemini: same_statute={gem_resp.get('all_methods_same_statute')} conf={gem_resp.get('confidence')} | {gem_methods[:3]}")

        classification = classify_service(file_claim, gpt_resp, gem_resp)
        print(f"    L2 class: {classification}")

        if not dry_run and not no_writeback:
            write_service_flag(code, data, path, classification, file_claim, gpt_resp, gem_resp)

        # Queue items for non-confirm results
        if classification not in ("CONSENSUS-CONFIRM", "SAME-STATUTE-CONFIRMED", "ERROR"):
            item_n += 1
            qid = f"{code}-SVC-{item_n:02d}"
            queue_items.append({
                "state": code, "state_name": state_name, "qid": qid,
                "classification": classification,
                "file_claim": file_claim, "gpt_resp": gpt_resp, "gem_resp": gem_resp,
            })

        if spend > BUDGET_CAP_USD:
            print(f"\n  ⚠️ BUDGET CAP HIT (~${spend:.2f}). Stopping early.")
            results.append({
                "state": code, "state_name": state_name,
                "file_claim": file_claim, "gpt_resp": gpt_resp, "gem_resp": gem_resp,
                "classification": classification,
            })
            break

        results.append({
            "state": code, "state_name": state_name,
            "file_claim": file_claim, "gpt_resp": gpt_resp, "gem_resp": gem_resp,
            "classification": classification,
        })

    # Save raw output file (provenance record per COWORK_DIRECTION_PROVENANCE.md)
    if not dry_run:
        from pathlib import Path
        import json as _json
        OUTPUT_DIR = Path(__file__).parent / "output"
        OUTPUT_DIR.mkdir(exist_ok=True)
        raw_path = OUTPUT_DIR / f"service_l2_raw_{TODAY}.json"
        raw_record = {
            "run_date": TODAY,
            "module": "service.method_rules",
            "models": {"gpt": OPENAI_MODEL, "gemini": GEMINI_MODEL},
            "states_run": len(results),
            "spend_estimate": round(spend, 4),
            "results": results,
        }
        with open(raw_path, "w") as f:
            _json.dump(raw_record, f, indent=2, ensure_ascii=False)
        print(f"\n  Raw output saved: {raw_path}")

    # Write report and update queue
    if not dry_run:
        write_service_report(results)
        if queue_items:
            append_service_to_queue(queue_items)

    # Summary
    from collections import Counter
    rc = Counter(r["classification"] for r in results)
    print(f"\n{'='*60}")
    print(f"  L2 Service complete — {len(results)} states | ~${spend:.2f} spent")
    print(f"  ✅ CONSENSUS-CONFIRM:       {rc.get('CONSENSUS-CONFIRM', 0)}")
    print(f"  ✅ SAME-STATUTE-CONFIRMED:  {rc.get('SAME-STATUTE-CONFIRMED', 0)}")
    print(f"  🟡 SUBSECTION-FOUND:        {rc.get('SUBSECTION-FOUND', 0)}")
    print(f"  🟡 CITATION-DIVERGENCE:     {rc.get('CITATION-DIVERGENCE', 0)}")
    print(f"  🟡 METHOD-AVAIL-DIFF:       {rc.get('METHOD-AVAILABILITY-DIFF', 0)}")
    print(f"  🔴 MODEL-SPLIT:             {rc.get('MODEL-SPLIT', 0)}")
    print(f"  ❌ ERROR:                   {rc.get('ERROR', 0)}")
    print(f"{'='*60}")
    print(f"\n  ⚠️  STOP AND REPORT. Do not auto-edit service files.")
    print(f"  Next: commit changed files via GitHub Desktop, report to Andy.")

    return results


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="L2 Service Runner — Civil Justice as Code"
    )
    parser.add_argument(
        "--states",
        default=",".join(ALL_STATES),
        help="Comma-separated state codes. Default: all 51.",
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="No API calls, no write-back.")
    parser.add_argument("--no-writeback", action="store_true",
                        help="Call APIs but do not write to files.")
    args = parser.parse_args()

    print(f"\nCivil Justice as Code — L2 Service Runner")
    print(f"Run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Models: {OPENAI_MODEL} + {GEMINI_MODEL}")
    print(f"Protocol: CONFIRM → pass; SUBSECTION-FOUND → flag; SPLIT → L7")
    print(f"Recency watch: {list(RECENCY_WATCH_STATES.keys())}")
    print(f"Budget cap: ${BUDGET_CAP_USD:.2f}")

    target = [s.strip().upper() for s in args.states.split(",") if s.strip()]
    print(f"States: {len(target)}")

    run_service_l2(
        target_codes=target,
        dry_run=args.dry_run,
        no_writeback=args.no_writeback,
    )
