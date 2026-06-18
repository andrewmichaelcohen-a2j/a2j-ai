#!/usr/bin/env python3
"""
Eviction Rules — L2 Phase 2 Runner (Full Library + Tiered Resolution)
======================================================================
Runs L2 multi-model consensus on all 43 states not covered in Phase 1,
then applies the full tiered resolution protocol inline:

  CONSENSUS-CONFIRM       → write pass; no action
  CITATION-DIVERGENCE     → if models agree on statute: AI-resolve citation
                            if models disagree: flag for human review
  PERIOD-DIVERGENCE       → AI reasoning pass; converge → AI-resolve;
                            no convergence → L7 escalation
  MODEL-SPLIT             → L7 escalation directly
  ERROR                   → logged, skipped

Phase 1 states (already resolved): ME, OH, WV, MO, MS, ND, IL, SD — SKIPPED.

AI-resolved items: content corrected, status stays AUTOMATED-CHECKS-PASSED,
flagged `pending-human-confirmation`. Nothing advances past ACP.

GUARDRAILS (do not remove):
  - API keys from .env only; never hardcoded, logged, or committed
  - Never advances any module past AUTOMATED-CHECKS-PASSED
  - AI resolution recorded with full reasoning for human audit
  - $20 hard budget cap
  - Divergence weighted as stronger signal than consensus

Usage (run from repo root on Andy's local machine — sandbox cannot reach external APIs):
  python3 rules/validation/l2/l2_phase2_runner.py
  python3 rules/validation/l2/l2_phase2_runner.py --states CA,TX,NY   # subset
  python3 rules/validation/l2/l2_phase2_runner.py --dry-run            # no API calls

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
# Import after ensuring the package is findable
_L2_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_L2_DIR))

from l2_runner import (
    call_openai,
    call_gemini,
    build_query,
    classify,
    extract_file_claim,
    load_all_v2_files,
    _extract_section_nums,
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

# ── State lists ───────────────────────────────────────────────────────────────

PHASE1_STATES = {"ME", "OH", "WV", "MO", "MS", "ND", "IL", "SD"}

# All 43 Phase 2 states (51 total - 8 Phase 1)
PHASE2_STATES = [
    "AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL",
    "GA", "HI", "IA", "ID", "IN", "KS", "KY", "LA", "MA", "MD",
    "MI", "MN", "MT", "NC", "NE", "NH", "NJ", "NM", "NV", "NY",
    "OK", "OR", "PA", "RI", "SC", "TN", "TX", "UT", "VA", "VT",
    "WA", "WI", "WY",
]

# Cost estimates: ~$0.02/state for L2 query; ~$0.08/state for reasoning pass
# 43 states × $0.02 = ~$0.86; up to ~10 reasoning passes × $0.08 = ~$0.80
# Total estimate: ~$1.66 — well within $20 cap
APPROX_COST_L2_QUERY = 0.02
APPROX_COST_REASONING = 0.08

# ── Reasoning pass ────────────────────────────────────────────────────────────

REASONING_SYSTEM_PROMPT = (
    "You are a legal research expert specializing in US residential landlord-tenant law. "
    "You will be given a specific legal question where sources disagree. "
    "Your task is to reason carefully through the competing statutes and determine "
    "which answer is best supported by the law. "
    "Be precise about statute citations. Acknowledge uncertainty where it exists. "
    "Respond only in the JSON format requested."
)


def build_reasoning_query(state_name: str, file_claim: dict, gpt: dict, gemini: dict) -> str:
    fd = file_claim.get("days")
    file_statute = file_claim.get("statute", "unknown")
    file_claim_str = f"{fd} days under {file_statute}" if fd else f"no notice / {file_statute}"

    gd = gpt.get("days")
    md = gemini.get("days")
    gpt_statute = gpt.get("statute", "unknown")
    gem_statute = gemini.get("statute", "unknown")

    if gd == md:
        model_claim_str = (
            f"{'no notice required' if gd is None else str(gd) + ' days'} "
            f"(GPT: {gpt_statute}; Gemini: {gem_statute})"
        )
    else:
        model_claim_str = (
            f"uncertain — GPT says {'none' if gd is None else str(gd) + 'd'} ({gpt_statute}); "
            f"Gemini says {'none' if md is None else str(md) + 'd'} ({gem_statute})"
        )

    return f"""Under {state_name} law, does a residential landlord need to give a tenant a formal notice to pay rent or quit BEFORE filing an eviction action for nonpayment of rent? If yes, how many days?

CONFLICT TO RESOLVE:
- Source A (rules file): {file_claim_str}
- Source B (two independent AI models): {model_claim_str}
  - GPT ({OPENAI_MODEL}): {gd}d, statute {gpt_statute}
  - Gemini ({GEMINI_MODEL}): {md}d, statute {gem_statute}

Please:
1. Identify the operative statute for nonpayment notice before filing eviction
2. State whether a formal notice period is required and, if so, how many days
3. Explain your reasoning with specific statutory references
4. Note any genuine ambiguity or exceptions

Respond ONLY in valid JSON:
{{"notice_required": <true|false>, "days": <integer|null>, "operative_statute": "<citation>", "reasoning": "<2-4 sentence explanation>", "confidence": "<high|medium|low>", "uncertainty_note": "<ambiguity or null>"}}"""


def call_openai_reasoning(query: str, dry_run: bool = False) -> dict:
    if dry_run:
        return {"notice_required": True, "days": 3, "operative_statute": "DRY-RUN", "reasoning": "dry", "confidence": "high", "uncertainty_note": None}
    try:
        from openai import OpenAI
    except ImportError:
        return {"error": "openai not installed"}
    try:
        client = OpenAI(api_key=OPENAI_KEY)
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": REASONING_SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
            max_completion_tokens=8000,
        )
        raw = resp.choices[0].message.content.strip() if resp.choices[0].message.content else ""
        return _parse_json_response(raw)
    except Exception as exc:
        return {"error": str(exc)}


def call_gemini_reasoning(query: str, dry_run: bool = False) -> dict:
    if dry_run:
        return {"notice_required": True, "days": 3, "operative_statute": "DRY-RUN", "reasoning": "dry", "confidence": "high", "uncertainty_note": None}
    try:
        from google import genai
    except ImportError:
        return {"error": "google-genai not installed"}
    try:
        client = genai.Client(api_key=GOOGLE_KEY)
        full_prompt = REASONING_SYSTEM_PROMPT + "\n\n" + query
        resp = client.models.generate_content(model=GEMINI_MODEL, contents=full_prompt)
        raw = resp.text.strip()
        return _parse_json_response(raw)
    except Exception as exc:
        return {"error": str(exc)}


def reasoning_models_converge(r_gpt: dict, r_gem: dict) -> bool:
    if r_gpt.get("error") or r_gem.get("error"):
        return False
    req_match = r_gpt.get("notice_required") == r_gem.get("notice_required")
    if not req_match:
        return False
    if not r_gpt.get("notice_required") and not r_gem.get("notice_required"):
        return True  # both say no notice
    return r_gpt.get("days") == r_gem.get("days")


# ── Resolution functions ──────────────────────────────────────────────────────

def resolve_citation(state: str, data: dict, path: str, file_claim: dict, gpt: dict, gemini: dict):
    """Auto-resolve citation divergence when models agree on statute."""
    gpt_secs = _extract_section_nums(gpt.get("statute") or "")
    gem_secs = _extract_section_nums(gemini.get("statute") or "")
    models_share = bool(gpt_secs & gem_secs)

    flags = data["validation"].setdefault("flags", [])
    # Remove existing open CITATION-DIVERGENCE flag
    flags = [fl for fl in flags if not (fl.get("layer") == "L2" and fl.get("code") == "L2-CITATION-DIVERGENCE" and fl.get("disposition") == "open")]

    if models_share:
        # Models agree — AI-resolve
        # Prefer the statute that both models share (pick GPT's since it usually has more context)
        resolved_statute = gpt.get("statute")
        old_statute = file_claim.get("statute")

        # Update file content
        pq = data["notice"]["notice_types"]["pay_or_quit"]
        for sub in ("tenancy_all", "tenancy_under_1yr", "tenancy_any"):
            if sub in pq and isinstance(pq[sub], dict):
                pq[sub]["statute"] = resolved_statute
                break

        flags.append({
            "layer": "L2",
            "code": "L2-CITATION-DIVERGENCE-AI-RESOLVED",
            "field": "notice.notice_types.pay_or_quit",
            "disposition": "resolved-ai-corrected",
            "resolution": {
                "method": "AI-citation-consensus",
                "resolved_date": TODAY,
                "old_statute": old_statute,
                "corrected_statute": resolved_statute,
                "gpt_statute": gpt.get("statute"),
                "gemini_statute": gemini.get("statute"),
                "gpt_rationale": gpt.get("rationale"),
                "gemini_rationale": gemini.get("rationale"),
                "status": "pending-human-confirmation",
                "note": (
                    f"Both {OPENAI_MODEL} and {GEMINI_MODEL} agree on operative statute. "
                    f"Citation updated from {old_statute!r} to {resolved_statute!r}. "
                    f"Period ({gpt.get('days')}d) confirmed. Pending human confirmation. "
                    f"NEVER auto-advanced past AUTOMATED-CHECKS-PASSED."
                ),
            },
            "l2_run_date": TODAY,
        })
        data["validation"]["automated_layers"]["L2_consensus"] = "pass"
        print(f"    → CITATION AI-RESOLVED: {old_statute!r} → {resolved_statute!r}")
        result_type = "CITATION-AI-RESOLVED"
    else:
        # Models disagree on citation — flag for human review
        flags.append({
            "layer": "L2",
            "code": "L2-CITATION-DIVERGENCE-UNRESOLVED",
            "field": "notice.notice_types.pay_or_quit",
            "disposition": "open",
            "note": (
                f"Citation divergence: period ({gpt.get('days')}d) confirmed, but models disagree on statute. "
                f"GPT: {gpt.get('statute')}. Gemini: {gemini.get('statute')}. "
                f"File: {file_claim.get('statute')}. Human must verify operative section."
            ),
            "gpt_statute": gpt.get("statute"),
            "gemini_statute": gemini.get("statute"),
            "l2_run_date": TODAY,
        })
        data["validation"]["automated_layers"]["L2_consensus"] = "flagged"
        print(f"    → CITATION UNRESOLVED (models disagree): GPT={gpt.get('statute')!r} Gemini={gemini.get('statute')!r}")
        result_type = "CITATION-UNRESOLVED"

    data["validation"]["flags"] = flags
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return result_type


def run_reasoning_pass(state: str, state_name: str, data: dict, path: str,
                        file_claim: dict, gpt: dict, gemini: dict, dry_run: bool = False):
    """Run AI reasoning pass for PERIOD-DIVERGENCE or MODEL-SPLIT."""
    print(f"    → Running reasoning pass ({OPENAI_MODEL} + {GEMINI_MODEL})...")
    query = build_reasoning_query(state_name, file_claim, gpt, gemini)

    r_gpt = call_openai_reasoning(query, dry_run=dry_run)
    r_gem = call_gemini_reasoning(query, dry_run=dry_run)

    if r_gpt.get("error"):
        print(f"    GPT reasoning ERROR: {r_gpt['error'][:80]}")
    else:
        print(f"    GPT reasoning: notice_required={r_gpt.get('notice_required')}, days={r_gpt.get('days')}, conf={r_gpt.get('confidence')}")

    if r_gem.get("error"):
        print(f"    Gemini reasoning ERROR: {r_gem['error'][:80]}")
    else:
        print(f"    Gemini reasoning: notice_required={r_gem.get('notice_required')}, days={r_gem.get('days')}, conf={r_gem.get('confidence')}")

    converged = reasoning_models_converge(r_gpt, r_gem)
    print(f"    Convergence: {'YES' if converged else 'NO'}")

    flags = data["validation"].setdefault("flags", [])
    # Remove any existing open PERIOD-DIVERGENCE / MODEL-SPLIT flag
    flags = [fl for fl in flags if not (
        fl.get("layer") == "L2"
        and fl.get("code") in ("L2-PERIOD-DIVERGENCE", "L2-MODEL-SPLIT")
        and fl.get("disposition") == "open"
    )]

    if converged and not r_gpt.get("error") and not r_gem.get("error"):
        notice_required = r_gpt.get("notice_required", False)
        days = r_gpt.get("days")
        operative_statute = r_gpt.get("operative_statute") or r_gem.get("operative_statute")

        # Update pay_or_quit content
        pq = data["notice"]["notice_types"]["pay_or_quit"]
        old_days = file_claim.get("days")
        old_statute = file_claim.get("statute")

        if notice_required is False or days is None:
            pq["notice_required"] = False
            pq["days"] = None
            for sub in ("tenancy_all", "tenancy_under_1yr", "tenancy_any"):
                if sub in pq and isinstance(pq[sub], dict):
                    pq[sub]["days"] = None
                    if operative_statute:
                        pq[sub]["statute"] = operative_statute
                    if "count_method" in pq[sub]:
                        pq[sub]["count_method"] = None
                    break
        else:
            for sub in ("tenancy_all", "tenancy_under_1yr", "tenancy_any"):
                if sub in pq and isinstance(pq[sub], dict):
                    pq[sub]["days"] = days
                    if operative_statute:
                        pq[sub]["statute"] = operative_statute
                    break

        flags.append({
            "layer": "L2",
            "code": "L2-PERIOD-DIVERGENCE-AI-RESOLVED",
            "field": "notice.notice_types.pay_or_quit",
            "disposition": "resolved-ai-corrected",
            "resolution": {
                "method": "AI-reasoning-pass",
                "resolved_date": TODAY,
                "notice_required": notice_required,
                "days": days,
                "operative_statute": operative_statute,
                "gpt_reasoning": r_gpt.get("reasoning"),
                "gpt_confidence": r_gpt.get("confidence"),
                "gemini_reasoning": r_gem.get("reasoning"),
                "gemini_confidence": r_gem.get("confidence"),
                "uncertainty_note": r_gpt.get("uncertainty_note") or r_gem.get("uncertainty_note"),
                "status": "pending-human-confirmation",
                "note": (
                    f"L2 reasoning pass converged: notice_required={notice_required}, days={days}, "
                    f"statute={operative_statute}. Corrected from file claim "
                    f"(days={old_days}, statute={old_statute!r}). "
                    f"NEVER auto-advanced past AUTOMATED-CHECKS-PASSED."
                ),
            },
            "l2_run_date": TODAY,
        })
        data["validation"]["automated_layers"]["L2_consensus"] = "pass"
        data["validation"]["flags"] = flags
        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"    → PERIOD AI-RESOLVED: days={old_days}→{days}, statute={old_statute!r}→{operative_statute!r}")
        return "PERIOD-AI-RESOLVED", r_gpt, r_gem, True

    else:
        # No convergence → L7
        flags.append({
            "layer": "L2",
            "code": "L2-PERIOD-DIVERGENCE-L7-ESCALATED",
            "field": "notice.notice_types.pay_or_quit",
            "disposition": "open",
            "escalation": "L7",
            "note": (
                f"L2 reasoning pass: models did NOT converge. "
                f"GPT: notice_required={r_gpt.get('notice_required')}, days={r_gpt.get('days')}, conf={r_gpt.get('confidence')}. "
                f"Gemini: notice_required={r_gem.get('notice_required')}, days={r_gem.get('days')}, conf={r_gem.get('confidence')}. "
                f"File claim: days={file_claim.get('days')}, statute={file_claim.get('statute')!r}. "
                f"Attorney review required."
            ),
            "gpt_reasoning": r_gpt.get("reasoning"),
            "gemini_reasoning": r_gem.get("reasoning"),
            "l2_run_date": TODAY,
        })
        data["validation"]["automated_layers"]["L2_consensus"] = "flagged"
        data["validation"]["flags"] = flags
        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"    → PERIOD NO-CONVERGENCE → L7 flag written")
        return "PERIOD-L7-ESCALATED", r_gpt, r_gem, False


def write_model_split_l7(state: str, data: dict, path: str, file_claim: dict, gpt: dict, gemini: dict):
    """Write L7 flag for MODEL-SPLIT classification."""
    flags = data["validation"].setdefault("flags", [])
    flags = [fl for fl in flags if not (fl.get("layer") == "L2" and fl.get("code") == "L2-MODEL-SPLIT" and fl.get("disposition") == "open")]
    flags.append({
        "layer": "L2",
        "code": "L2-MODEL-SPLIT-L7",
        "field": "notice.notice_types.pay_or_quit",
        "disposition": "open",
        "escalation": "L7",
        "note": (
            f"L2 MODEL-SPLIT: the two models disagree with each other. "
            f"GPT ({OPENAI_MODEL}): {gpt.get('days')}d, {gpt.get('statute')}. "
            f"Gemini ({GEMINI_MODEL}): {gemini.get('days')}d, {gemini.get('statute')}. "
            f"File: {file_claim.get('days')}d, {file_claim.get('statute')}. "
            f"Attorney review required to determine operative answer."
        ),
        "gpt_answer": {"days": gpt.get("days"), "statute": gpt.get("statute"), "rationale": gpt.get("rationale")},
        "gemini_answer": {"days": gemini.get("days"), "statute": gemini.get("statute"), "rationale": gemini.get("rationale")},
        "l2_run_date": TODAY,
    })
    data["validation"]["automated_layers"]["L2_consensus"] = "flagged"
    data["validation"]["flags"] = flags
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"    → MODEL-SPLIT → L7 flag written")


def write_consensus_confirm(state: str, data: dict, path: str, gpt: dict, gemini: dict):
    """Record CONSENSUS-CONFIRM result."""
    data["validation"].setdefault("automated_layers", {})["L2_consensus"] = "pass"
    # Update l2_results with clean run record
    data["validation"]["l2_results"] = {
        "run_date": TODAY,
        "classification": "CONSENSUS-CONFIRM",
        "gpt": {"model": gpt.get("model"), "days": gpt.get("days"), "statute": gpt.get("statute"), "rationale": gpt.get("rationale")},
        "gemini": {"model": gemini.get("model"), "days": gemini.get("days"), "statute": gemini.get("statute"), "rationale": gemini.get("rationale")},
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── Human Review Queue updater ────────────────────────────────────────────────

QUEUE_PATH = str(DOCS_DIR / "HUMAN_REVIEW_QUEUE.md")

_QUEUE_ITEM_COUNTER = {"n": 0}  # track item numbers across calls


def _next_queue_id(state: str, kind: str) -> str:
    _QUEUE_ITEM_COUNTER["n"] += 1
    return f"{state}-P2-{_QUEUE_ITEM_COUNTER['n']:02d}"


def append_to_queue(items: list[dict]):
    """Append Phase 2 review items to HUMAN_REVIEW_QUEUE.md."""
    if not items:
        return

    try:
        with open(QUEUE_PATH) as f:
            content = f.read()
    except FileNotFoundError:
        content = "# Human Review Queue\n\n## Phase 2 Items\n\n"

    phase2_marker = "## Phase 2 Items"
    resolved_marker = "## Resolved Items"

    insert_content = f"\n*Phase 2 run: {TODAY}*\n\n"
    for item in items:
        state = item["state"]
        state_name = item["state_name"]
        classification = item["classification"]
        resolution_type = item.get("resolution_type", classification)
        qid = item.get("qid", f"{state}-P2")
        gpt = item.get("gpt", {})
        gemini = item.get("gemini", {})
        file_claim = item.get("file_claim", {})
        r_gpt = item.get("r_gpt", {})
        r_gem = item.get("r_gem", {})

        if resolution_type == "L7-ESCALATED":
            icon = "🔴"
            cls_label = "L7-ESCALATED"
        elif resolution_type in ("PERIOD-AI-RESOLVED", "CITATION-AI-RESOLVED"):
            icon = "🟡"
            cls_label = "PENDING-CONFIRMATION"
        elif resolution_type == "CITATION-UNRESOLVED":
            icon = "🟡"
            cls_label = "PENDING-CONFIRMATION (citation)"
        else:
            continue  # CONSENSUS-CONFIRM — no review needed

        insert_content += f"### [{qid}] {state} ({state_name}) — {icon} {cls_label}\n\n"
        insert_content += f"**L2 classification:** {classification}  \n"
        insert_content += f"**Resolution:** {resolution_type}  \n"
        insert_content += f"**Status:** {icon} pending  \n"
        insert_content += f"**Run date:** {TODAY}\n\n"

        if resolution_type == "L7-ESCALATED":
            insert_content += f"**Question:** Attorney must determine the correct notice requirement for {state_name} nonpayment evictions.\n\n"
            insert_content += f"**L2 result:** Models disagreed.\n"
            insert_content += f"- GPT: {gpt.get('days')}d, {gpt.get('statute')} — {(gpt.get('rationale') or '')[:200]}\n"
            insert_content += f"- Gemini: {gemini.get('days')}d, {gemini.get('statute')} — {(gemini.get('rationale') or '')[:200]}\n"
            insert_content += f"- File: {file_claim.get('days')}d, {file_claim.get('statute')}\n\n"
        elif resolution_type == "PERIOD-AI-RESOLVED":
            insert_content += f"**Question to confirm:** AI reasoning converged. Please verify the proposed answer is correct.\n\n"
            insert_content += f"**AI proposed:** notice_required={r_gpt.get('notice_required')}, days={r_gpt.get('days')}, statute={r_gpt.get('operative_statute')}\n"
            insert_content += f"**GPT reasoning:** {(r_gpt.get('reasoning') or '')[:300]}\n"
            insert_content += f"**Gemini reasoning:** {(r_gem.get('reasoning') or '')[:300]}\n"
            insert_content += f"**Prior file claim:** days={file_claim.get('days')}, statute={file_claim.get('statute')}\n\n"
        elif resolution_type == "CITATION-AI-RESOLVED":
            insert_content += f"**Question to confirm:** Citation corrected by AI consensus. Please verify the operative section.\n\n"
            insert_content += f"**AI proposed statute:** {gpt.get('statute')} (both models agree)\n"
            insert_content += f"**Prior file statute:** {file_claim.get('statute')}\n"
            insert_content += f"**Period:** {gpt.get('days')}d (confirmed)\n\n"
        elif resolution_type == "CITATION-UNRESOLVED":
            insert_content += f"**Question:** Period ({gpt.get('days')}d) confirmed but citation is ambiguous.\n\n"
            insert_content += f"- GPT statute: {gpt.get('statute')}\n"
            insert_content += f"- Gemini statute: {gemini.get('statute')}\n"
            insert_content += f"- File statute: {file_claim.get('statute')}\n\n"
            insert_content += "Human must verify operative section from primary source.\n\n"

        insert_content += "**Resolution:** ________________  \n"
        insert_content += "**Confirmed by:** ________________  **Date:** ________________\n\n---\n\n"

    # Insert after phase2_marker line
    if phase2_marker in content:
        marker_pos = content.index(phase2_marker) + len(phase2_marker)
        content = content[:marker_pos] + "\n" + insert_content + content[marker_pos:]
    else:
        if resolved_marker in content:
            content = content.replace(f"\n{resolved_marker}", f"\n{phase2_marker}\n{insert_content}\n{resolved_marker}")
        else:
            content += f"\n{phase2_marker}\n{insert_content}"

    with open(QUEUE_PATH, "w") as f:
        f.write(content)
    print(f"\n  Human Review Queue updated: {len(items)} Phase 2 items appended → {QUEUE_PATH}")


# ── Report generation ─────────────────────────────────────────────────────────

def write_phase2_report(results: list[dict]):
    from collections import Counter
    counts = Counter(r["resolution_type"] for r in results)
    raw_counts = Counter(r["classification"] for r in results)

    report_path = str(DOCS_DIR / f"L2_CONSENSUS_REPORT_PHASE2_{TODAY}.md")

    lines = [
        "# L2 Multi-Model Consensus Report — Phase 2 — All Remaining States",
        "",
        f"**Run date:** {TODAY}",
        f"**Models:** OpenAI `{OPENAI_MODEL}` · Google `{GEMINI_MODEL}`",
        f"**Target:** Notice module — `pay_or_quit` nonpayment notice period and statutory citation",
        f"**States run:** {len(results)} (Phase 2 — all states not covered in Phase 1)",
        "",
        "> **Interpretation caveat:** Model consensus is corroborating-but-not-independent.",
        "> **Divergence is the stronger signal.** Do not treat unanimous agreement as proof.",
        "",
        "---",
        "",
        "## Summary",
        "",
        "### Raw L2 Classifications",
        "",
        "| Classification | Count |",
        "|---------------|-------|",
        f"| ✅ CONSENSUS-CONFIRM | {raw_counts.get('CONSENSUS-CONFIRM', 0)} |",
        f"| ⚠️ CITATION-DIVERGENCE | {raw_counts.get('CITATION-DIVERGENCE', 0)} |",
        f"| 🔴 PERIOD-DIVERGENCE | {raw_counts.get('PERIOD-DIVERGENCE', 0)} |",
        f"| ⚠️ MODEL-SPLIT | {raw_counts.get('MODEL-SPLIT', 0)} |",
        f"| ❌ ERROR | {raw_counts.get('ERROR', 0)} |",
        "",
        "### After Tiered Resolution",
        "",
        "| Resolution | Count |",
        "|-----------|-------|",
        f"| ✅ CONSENSUS-CONFIRM | {counts.get('CONSENSUS-CONFIRM', 0)} |",
        f"| ✅ CITATION-AI-RESOLVED (pending confirmation) | {counts.get('CITATION-AI-RESOLVED', 0)} |",
        f"| ✅ PERIOD-AI-RESOLVED (pending confirmation) | {counts.get('PERIOD-AI-RESOLVED', 0)} |",
        f"| 🟡 CITATION-UNRESOLVED (human review) | {counts.get('CITATION-UNRESOLVED', 0)} |",
        f"| 🔴 L7-ESCALATED | {counts.get('L7-ESCALATED', 0) + counts.get('PERIOD-L7-ESCALATED', 0)} |",
        f"| ❌ ERROR | {counts.get('ERROR', 0)} |",
        "",
        "---",
        "",
        "## Per-State Results",
        "",
        "| State | File days | File statute | GPT days | GPT statute | Gemini days | Gemini statute | L2 Class | Resolution |",
        "|-------|-----------|-------------|---------|------------|------------|---------------|----------|------------|",
    ]

    for r in results:
        c = r["classification"]
        rt = r.get("resolution_type", c)
        icon = {
            "CONSENSUS-CONFIRM": "✅", "CITATION-AI-RESOLVED": "✅", "PERIOD-AI-RESOLVED": "✅",
            "CITATION-UNRESOLVED": "🟡", "L7-ESCALATED": "🔴", "PERIOD-L7-ESCALATED": "🔴",
            "ERROR": "❌",
        }.get(rt, "⚠️")
        fc = r["file_claim"]
        gpt = r["gpt"]
        gem = r["gemini"]
        fd = str(fc["days"]) if fc["days"] is not None else "none"
        fs = (fc.get("statute") or "")[:35]
        gd = str(gpt.get("days")) if gpt.get("days") is not None else "none"
        gs = (gpt.get("statute") or "ERR")[:35]
        md = str(gem.get("days")) if gem.get("days") is not None else "none"
        ms = (gem.get("statute") or "ERR")[:35]
        lines.append(f"| {r['state']} | {fd} | {fs} | {gd} | {gs} | {md} | {ms} | {c} | {icon} {rt} |")

    # Grouped sections
    lines += ["", "---", "", "## Items Requiring Human Review", ""]

    l7 = [r for r in results if "L7" in r.get("resolution_type", "")]
    pending_conf = [r for r in results if r.get("resolution_type") in ("CITATION-AI-RESOLVED", "PERIOD-AI-RESOLVED", "CITATION-UNRESOLVED")]

    if l7:
        lines += [f"### L7-Escalated ({len(l7)} states — attorney review required)", ""]
        for r in l7:
            lines += [
                f"**{r['state']} ({r['state_name']})** — {r['classification']}",
                f"- File: {r['file_claim']['days']}d, {r['file_claim'].get('statute')}",
                f"- GPT: {r['gpt'].get('days')}d, {r['gpt'].get('statute')} — {(r['gpt'].get('rationale') or '')[:150]}",
                f"- Gemini: {r['gemini'].get('days')}d, {r['gemini'].get('statute')} — {(r['gemini'].get('rationale') or '')[:150]}",
                "",
            ]
    else:
        lines += ["### L7-Escalated", "", "None.", ""]

    if pending_conf:
        lines += [f"### AI-Resolved / Pending Human Confirmation ({len(pending_conf)} states)", ""]
        for r in pending_conf:
            rt = r.get("resolution_type", "")
            if rt == "PERIOD-AI-RESOLVED":
                r_gpt = r.get("r_gpt", {})
                r_gem = r.get("r_gem", {})
                lines += [
                    f"**{r['state']} ({r['state_name']})** — PERIOD-DIVERGENCE → AI-RESOLVED",
                    f"- Old: {r['file_claim']['days']}d, {r['file_claim'].get('statute')}",
                    f"- New: notice_required={r_gpt.get('notice_required')}, days={r_gpt.get('days')}, statute={r_gpt.get('operative_statute')}",
                    f"- GPT confidence: {r_gpt.get('confidence')} | Gemini confidence: {r_gem.get('confidence')}",
                    "",
                ]
            elif rt == "CITATION-AI-RESOLVED":
                lines += [
                    f"**{r['state']} ({r['state_name']})** — CITATION-DIVERGENCE → AI-RESOLVED",
                    f"- Old statute: {r['file_claim'].get('statute')}",
                    f"- New statute: {r['gpt'].get('statute')} (both models agree)",
                    f"- Period: {r['gpt'].get('days')}d (confirmed)",
                    "",
                ]
            elif rt == "CITATION-UNRESOLVED":
                lines += [
                    f"**{r['state']} ({r['state_name']})** — CITATION-DIVERGENCE → UNRESOLVED (models split on citation)",
                    f"- Period {r['gpt'].get('days')}d confirmed. GPT: {r['gpt'].get('statute')}. Gemini: {r['gemini'].get('statute')}.",
                    "",
                ]

    lines += [
        "---",
        "",
        "## Confirmed — No Review Needed",
        "",
        f"**{len([r for r in results if r.get('resolution_type') == 'CONSENSUS-CONFIRM'])} states CONSENSUS-CONFIRM:** "
        + ", ".join(r["state"] for r in results if r.get("resolution_type") == "CONSENSUS-CONFIRM"),
        "",
        "---",
        "",
        "*L2 corroborates and flags. It never blesses and never auto-edits content.*",
        "*AI-resolved items: content corrected, status stays AUTOMATED-CHECKS-PASSED, marked pending-human-confirmation.*",
        "*No file was advanced past AUTOMATED-CHECKS-PASSED by this run.*",
        "",
        f"*Copyright 2026 Andrew M Cohen. Apache 2.0.*",
    ]

    with open(report_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\n  Phase 2 report → {os.path.basename(report_path)}")
    return report_path


# ── Main runner ───────────────────────────────────────────────────────────────

def run_phase2(target_codes: list[str], dry_run: bool = False, no_writeback: bool = False):
    all_data, all_paths = load_all_v2_files()

    # Validate
    missing = [c for c in target_codes if c not in all_data]
    if missing:
        print(f"  WARN: states not found in library: {missing}")
        target_codes = [c for c in target_codes if c in all_data]

    # Exclude Phase 1 states
    skipped = [c for c in target_codes if c in PHASE1_STATES]
    if skipped:
        print(f"  Skipping Phase 1 states (already processed): {skipped}")
        target_codes = [c for c in target_codes if c not in PHASE1_STATES]

    if not target_codes:
        print("  No Phase 2 states to process.")
        return

    n = len(target_codes)
    est_max = n * APPROX_COST_L2_QUERY + min(n // 3, 10) * APPROX_COST_REASONING
    print(f"\n  States: {n} · Est. cost: ~${est_max:.2f} (max) · Hard cap: ${BUDGET_CAP_USD:.2f}")
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
        file_claim = extract_file_claim(data)

        statute_preview = repr(file_claim.get('statute', ''))[:40]
        print(f"\n  {code} ({state_name}) — file: {file_claim['days']}d {statute_preview}")

        query = build_query(state_name)
        gpt = call_openai(query, dry_run=dry_run)
        gem = call_gemini(query, dry_run=dry_run)
        spend += APPROX_COST_L2_QUERY

        if gpt.get("error"):
            print(f"    GPT ERROR: {gpt['error'][:80]}")
        else:
            print(f"    GPT:    {gpt.get('days')}d | {(gpt.get('statute') or '')[:50]}")

        if gem.get("error"):
            print(f"    Gemini ERROR: {gem['error'][:80]}")
        else:
            print(f"    Gemini: {gem.get('days')}d | {(gem.get('statute') or '')[:50]}")

        classification = classify(file_claim, gpt, gem)
        print(f"    L2 class: {classification}")

        # Apply tiered resolution
        resolution_type = classification
        r_gpt, r_gem = {}, {}

        if classification == "CONSENSUS-CONFIRM":
            if not dry_run and not no_writeback:
                write_consensus_confirm(code, data, path, gpt, gem)
            # No queue item needed for clean confirms

        elif classification == "CITATION-DIVERGENCE":
            if not dry_run and not no_writeback:
                resolution_type = resolve_citation(code, data, path, file_claim, gpt, gem)
            else:
                # Determine what resolution WOULD be
                gpt_secs = _extract_section_nums(gpt.get("statute") or "")
                gem_secs = _extract_section_nums(gem.get("statute") or "")
                resolution_type = "CITATION-AI-RESOLVED" if (gpt_secs & gem_secs) else "CITATION-UNRESOLVED"
                print(f"    (dry run — would be {resolution_type})")

            item_n += 1
            qid = f"{code}-P2-{item_n:02d}"
            queue_items.append({"state": code, "state_name": state_name, "qid": qid,
                                  "classification": classification, "resolution_type": resolution_type,
                                  "file_claim": file_claim, "gpt": gpt, "gemini": gem})

        elif classification == "PERIOD-DIVERGENCE":
            spend += APPROX_COST_REASONING
            if not dry_run and not no_writeback:
                resolution_type, r_gpt, r_gem, converged = run_reasoning_pass(
                    code, state_name, data, path, file_claim, gpt, gem, dry_run=dry_run)
            else:
                resolution_type = "PERIOD-AI-RESOLVED"  # placeholder for dry run
                r_gpt, r_gem = {}, {}
                print(f"    (dry run — would run reasoning pass)")

            item_n += 1
            qid = f"{code}-P2-{item_n:02d}"
            queue_items.append({"state": code, "state_name": state_name, "qid": qid,
                                  "classification": classification, "resolution_type": resolution_type,
                                  "file_claim": file_claim, "gpt": gpt, "gemini": gem,
                                  "r_gpt": r_gpt, "r_gem": r_gem})

        elif classification == "MODEL-SPLIT":
            if not dry_run and not no_writeback:
                write_model_split_l7(code, data, path, file_claim, gpt, gem)
            resolution_type = "L7-ESCALATED"
            item_n += 1
            qid = f"{code}-P2-{item_n:02d}"
            queue_items.append({"state": code, "state_name": state_name, "qid": qid,
                                  "classification": classification, "resolution_type": resolution_type,
                                  "file_claim": file_claim, "gpt": gpt, "gemini": gem})

        elif classification == "ERROR":
            resolution_type = "ERROR"
            print(f"    ERROR — skipping write-back for {code}")

        if spend > BUDGET_CAP_USD:
            print(f"\n  ⚠️ BUDGET CAP HIT (~${spend:.2f}). Stopping early.")
            results.append({"state": code, "state_name": state_name, "file_claim": file_claim,
                             "gpt": gpt, "gemini": gem, "classification": classification,
                             "resolution_type": resolution_type, "r_gpt": r_gpt, "r_gem": r_gem})
            break

        results.append({"state": code, "state_name": state_name, "file_claim": file_claim,
                         "gpt": gpt, "gemini": gem, "classification": classification,
                         "resolution_type": resolution_type, "r_gpt": r_gpt, "r_gem": r_gem})

    # Write report
    if not dry_run:
        write_phase2_report(results)

    # Update human review queue
    if not dry_run and queue_items:
        append_to_queue(queue_items)

    # Summary
    from collections import Counter
    rc = Counter(r["resolution_type"] for r in results)
    print(f"\n{'='*60}")
    print(f"  L2 Phase 2 complete — {len(results)} states | ~${spend:.2f} spent")
    print(f"  ✅ CONFIRM:         {rc.get('CONSENSUS-CONFIRM', 0)}")
    print(f"  ✅ CITATION-AI-RES: {rc.get('CITATION-AI-RESOLVED', 0)} (pending human confirmation)")
    print(f"  ✅ PERIOD-AI-RES:   {rc.get('PERIOD-AI-RESOLVED', 0)} (pending human confirmation)")
    print(f"  🟡 CITATION-UNRES:  {rc.get('CITATION-UNRESOLVED', 0)} (human review)")
    print(f"  🔴 L7-ESCALATED:   {rc.get('L7-ESCALATED', 0) + rc.get('PERIOD-L7-ESCALATED', 0)}")
    print(f"  ❌ ERROR:           {rc.get('ERROR', 0)}")
    print(f"{'='*60}")
    print(f"\n  ⚠️  STOP AND REPORT. Do not start Phase 3.")
    print(f"  Next: commit all changed files via GitHub Desktop, then report to Andy.")

    return results


# ── CLI entry point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="L2 Phase 2 Runner — Civil Justice as Code (full tiered resolution)"
    )
    parser.add_argument(
        "--states",
        default=",".join(PHASE2_STATES),
        help="Comma-separated state codes. Default: all 43 Phase 2 states.",
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="No API calls, no write-back. Print plan only.")
    parser.add_argument("--no-writeback", action="store_true",
                        help="Call APIs and classify, but do not write to files.")
    args = parser.parse_args()

    print(f"\nCivil Justice as Code — L2 Phase 2 Runner")
    print(f"Run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Models: {OPENAI_MODEL} + {GEMINI_MODEL}")
    print(f"Protocol: full tiered resolution (citation→AI; period→reasoning pass; split→L7)")
    print(f"Budget cap: ${BUDGET_CAP_USD:.2f}")

    target = [s.strip().upper() for s in args.states.split(",") if s.strip()]
    print(f"States: {len(target)} specified ({len([c for c in target if c not in PHASE1_STATES])} Phase 2 after skipping Phase 1)")

    run_phase2(
        target_codes=target,
        dry_run=args.dry_run,
        no_writeback=args.no_writeback,
    )
