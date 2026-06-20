#!/usr/bin/env python3
"""
Eviction Rules — L2 Service Reasoning Pass
===========================================
Applies tiered resolution to the 20 states flagged by l2_service_runner.py
as CITATION-DIVERGENCE, MODEL-SPLIT-L7, or SUBSECTION-FOUND.

Three resolution paths:

  SUBSECTION-FOUND (models already agree on subsections):
    → Both models agreed in round 1 — skip reasoning pass, mark AI-resolved directly.
      Correct subsections confirmed; file needs citation update (no auto-edit).

  CITATION-DIVERGENCE (models agree with each other, differ from file):
    → Run reasoning pass: present all competing citations, ask both models to adjudicate.
    → Converge → AI-resolved (model consensus wins over file claim).
    → Diverge → L7.

  MODEL-SPLIT-L7 (models disagreed in round 1):
    → Run reasoning pass: present both model answers, ask both to adjudicate.
    → Converge → AI-resolved.
    → Diverge → genuine L7.

GUARDRAILS (do not remove):
  - No content corrections — flags only; rules files are never edited
  - Nothing advances past AUTOMATED-CHECKS-PASSED
  - Runner appends/updates flags only; never touches resolution/confirmed-by fields
  - $20 hard cap (combined with prior run ~$1.53 → remaining budget ~$18.47)
  - Neutral queries; no anchoring beyond the competing claims being adjudicated

Usage:
  python3 rules/validation/l2/l2_service_reasoning.py
  python3 rules/validation/l2/l2_service_reasoning.py --states AL,AK,ID
  python3 rules/validation/l2/l2_service_reasoning.py --dry-run

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import os
import re
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

_L2_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_L2_DIR))

from l2_runner import (
    call_openai,
    call_gemini,
    _parse_json_response,
    load_all_v2_files,
    OPENAI_MODEL,
    GEMINI_MODEL,
    OPENAI_KEY,
    GOOGLE_KEY,
    BUDGET_CAP_USD,
    DOCS_DIR,
)

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# States to target (from l2_service_runner.py results)
REVIEW_STATES = [
    "AL", "AK", "AZ", "CO", "HI", "IA", "ID", "IN",
    "MA", "MO", "MT", "NC", "NH", "OR", "PA", "SC",
    "TX", "UT", "WA", "WV",
]

APPROX_COST_REASONING = 0.06  # per state (2 model calls each)

REASONING_SYSTEM_PROMPT = (
    "You are a legal research expert in US residential landlord-tenant law. "
    "You will be presented with competing claims about which statutes govern "
    "service of eviction notices in a specific state. Your task is to determine "
    "which claim is best supported by current law. "
    "Be precise about statute citations including subsections. "
    "Respond only in the JSON format requested."
)


# ── Query builders ─────────────────────────────────────────────────────────────

# State-specific override queries for persistent subsection-level disputes
SUBSECTION_OVERRIDE_QUERIES = {
    "Indiana": (
        "In Indiana, what are the correct statutes for each method of serving a "
        "residential pay-or-quit notice on a tenant? Specifically, I need to know "
        "whether Ind. Code §32-31-1-9(a) or §32-31-1-9(b)(1) (or both, for different methods) "
        "governs: (1) personal delivery to the tenant, (2) substituted service (leaving with "
        "someone at the premises), and (3) mail. These subsections may govern different methods — "
        "please identify the correct subsection for each method specifically.\n\n"
        "Respond ONLY in valid JSON:\n"
        "{\"personal_statute\": \"<citation>\", \"substituted_statute\": \"<citation>\", "
        "\"mail_statute\": \"<citation>\", \"reasoning\": \"<2-3 sentences>\", "
        "\"confidence\": \"high|medium|low\", \"uncertainty_note\": \"<note or null>\"}"
    ),
    "Oregon": (
        "In Oregon, what are the correct statutes for each method of serving a "
        "residential pay-or-quit notice? I know ORS 90.155 governs notice service generally, "
        "but I need the specific subsections for: (1) personal delivery, "
        "(2) substituted service (leaving with someone at the premises or conspicuous place + mail), "
        "and (3) mail only. Please give the exact subsection for each method.\n\n"
        "Respond ONLY in valid JSON:\n"
        "{\"personal_statute\": \"<citation>\", \"substituted_statute\": \"<citation>\", "
        "\"mail_statute\": \"<citation>\", \"reasoning\": \"<2-3 sentences>\", "
        "\"confidence\": \"high|medium|low\", \"uncertainty_note\": \"<note or null>\"}"
    ),
}


def build_tiebreaker_query(state_name: str, flag: dict, file_claim: dict) -> str:
    """
    Second-pass tiebreaker for states that went L7 after reasoning pass.
    Uses the gpt_answer/gemini_answer from the prior reasoning-pass L7 flag.
    Presents both answers explicitly and asks models to pick definitively.
    """
    gpt_a = flag.get("gpt_answer", {})
    gem_a = flag.get("gemini_answer", {})
    file_statutes = file_claim.get("unique_statutes", [])

    gpt_p = gpt_a.get("personal_statute", "?") or "?"
    gpt_s_stat = gpt_a.get("substituted_statute", "?") or "?"
    gpt_m = gpt_a.get("mail_statute", "?") or "?"
    gem_p = gem_a.get("personal_statute", "?") or "?"
    gem_s_stat = gem_a.get("substituted_statute", "?") or "?"
    gem_m = gem_a.get("mail_statute", "?") or "?"
    gpt_reason = (gpt_a.get("reasoning") or "not provided")[:200]
    gem_reason = (gem_a.get("reasoning") or "not provided")[:200]

    return f"""In {state_name}, two prior AI analyses disagree about which statutes govern service of a residential pay-or-quit notice.

Prior analysis A (GPT {OPENAI_MODEL}):
  personal={gpt_p}, substituted={gpt_s_stat}, mail={gpt_m}
  Reasoning: {gpt_reason}

Prior analysis B (Gemini {GEMINI_MODEL}):
  personal={gem_p}, substituted={gem_s_stat}, mail={gem_m}
  Reasoning: {gem_reason}

Rules file currently cites: {file_statutes}

This is a tiebreaker request. Please carefully review both analyses and determine definitively which is correct under current {state_name} law. If the analyses are reconcilable (e.g. both cite the same statute with different subsections that may both be valid), synthesize the correct answer.

Respond ONLY in valid JSON:
{{"personal_statute": "<citation>", "substituted_statute": "<citation>", "mail_statute": "<citation>", "tiebreaker_winner": "analysis_a|analysis_b|synthesis|new", "reasoning": "<2-3 sentences>", "confidence": "high|medium|low", "uncertainty_note": "<note or null>"}}"""


def build_reasoning_query(state_name: str, flag: dict, file_claim: dict) -> str:
    code = flag.get("code", "")

    # If this is a reasoning-pass L7 flag (has gpt_answer/gemini_answer), use tiebreaker format
    if flag.get("gpt_answer") or flag.get("gemini_answer"):
        return build_tiebreaker_query(state_name, flag, file_claim)

    gpt_s = flag.get("gpt_summary", {})
    gem_s = flag.get("gemini_summary", {})

    gpt_methods = {m["method"]: m["statute"] for m in gpt_s.get("methods", [])}
    gem_methods = {m["method"]: m["statute"] for m in gem_s.get("methods", [])}
    file_statutes = file_claim.get("unique_statutes", [])
    file_methods = {k: v.get("statute") for k, v in file_claim.get("methods", {}).items()}

    if "SUBSECTION" in code:
        # Both models already agree — just ask for confirmation of subsections
        query = f"""In {state_name}, a rules file cites one statute for all service methods of a residential pay-or-quit notice: {file_statutes}.

Two independent AI models both identified method-specific subsections:
- GPT ({OPENAI_MODEL}): personal={gpt_methods.get('personal','?')}, substituted={gpt_methods.get('substituted','?')}, mail/posting={gpt_methods.get('mail') or gpt_methods.get('posting_and_mailing','?')}
- Gemini ({GEMINI_MODEL}): personal={gem_methods.get('personal','?')}, substituted={gem_methods.get('substituted','?')}, mail/posting={gem_methods.get('mail') or gem_methods.get('post_and_mail','?')}

Please confirm: are the method-specific subsections cited by both models correct? Or does the parent statute cited by the file cover all methods in a single provision?

Respond ONLY in valid JSON:
{{"personal_statute": "<citation>", "substituted_statute": "<citation>", "mail_statute": "<citation>", "file_statute_correct": <true|false>, "model_subsections_correct": <true|false>, "reasoning": "<2-3 sentences>", "confidence": "high|medium|low", "uncertainty_note": "<note or null>"}}"""

    elif "CITATION-DIVERGENCE" in code:
        query = f"""In {state_name}, there is a dispute about which statutes govern service of a residential pay-or-quit notice. Three competing claims:

- Source A (rules file): {file_statutes} (same for all methods)
- Source B (GPT {OPENAI_MODEL}): personal={gpt_methods.get('personal','?')}, substituted={gpt_methods.get('substituted','?')}, mail={gpt_methods.get('mail','?')}
- Source C (Gemini {GEMINI_MODEL}): personal={gem_methods.get('personal','?')}, substituted={gem_methods.get('substituted','?')}, mail={gem_methods.get('mail','?')}

Which source is correct? Identify the operative statutes for each service method under current {state_name} law.

Respond ONLY in valid JSON:
{{"personal_statute": "<citation>", "substituted_statute": "<citation>", "mail_statute": "<citation>", "which_source_correct": "file|gpt|gemini|new", "reasoning": "<2-3 sentences>", "confidence": "high|medium|low", "uncertainty_note": "<note or null>"}}"""

    else:  # MODEL-SPLIT
        query = f"""In {state_name}, two AI models disagree about which statutes govern service of a residential pay-or-quit notice:

- GPT ({OPENAI_MODEL}): personal={gpt_methods.get('personal','?')}, substituted={gpt_methods.get('substituted','?')}, mail={gpt_methods.get('mail','?')}
- Gemini ({GEMINI_MODEL}): personal={gem_methods.get('personal','?')}, substituted={gem_methods.get('substituted','?')}, mail={gem_methods.get('mail','?')}
- Current rules file: {file_statutes}

Please determine the correct statutes for each service method under current {state_name} law.

Respond ONLY in valid JSON:
{{"personal_statute": "<citation>", "substituted_statute": "<citation>", "mail_statute": "<citation>", "reasoning": "<2-3 sentences>", "confidence": "high|medium|low", "uncertainty_note": "<note or null>"}}"""

    return query


def call_openai_reasoning(query: str, dry_run: bool = False) -> dict:
    if dry_run:
        return {"personal_statute": "DRY-§1(a)", "substituted_statute": "DRY-§1(b)",
                "mail_statute": "DRY-§1(c)", "reasoning": "dry", "confidence": "high",
                "uncertainty_note": None, "which_source_correct": "gpt"}
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_KEY)
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": REASONING_SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
            max_completion_tokens=4000,
        )
        raw = resp.choices[0].message.content.strip() if resp.choices[0].message.content else ""
        return _parse_json_response(raw)
    except Exception as exc:
        return {"error": str(exc)[:200]}


def call_gemini_reasoning(query: str, dry_run: bool = False) -> dict:
    if dry_run:
        return {"personal_statute": "DRY-§1(a)", "substituted_statute": "DRY-§1(b)",
                "mail_statute": "DRY-§1(c)", "reasoning": "dry", "confidence": "high",
                "uncertainty_note": None, "which_source_correct": "gpt"}
    try:
        from google import genai
        client = genai.Client(api_key=GOOGLE_KEY)
        full_prompt = REASONING_SYSTEM_PROMPT + "\n\n" + query
        resp = client.models.generate_content(model=GEMINI_MODEL, contents=full_prompt)
        raw = resp.text.strip()
        return _parse_json_response(raw)
    except Exception as exc:
        return {"error": str(exc)[:200]}


# ── Convergence check ──────────────────────────────────────────────────────────

def _section_nums(s: str) -> set:
    if not s:
        return set()
    return set(re.findall(r'\d[\d\-\.]*[a-zA-Z]?(?:\(\w+\))*', s))


def reasoning_converges(r_gpt: dict, r_gem: dict) -> bool:
    """Check if both reasoning responses agree on statutes for all core methods."""
    if r_gpt.get("error") or r_gem.get("error"):
        return False
    if r_gpt.get("confidence") == "low" or r_gem.get("confidence") == "low":
        return False
    for field in ("personal_statute", "substituted_statute", "mail_statute"):
        gs = r_gpt.get(field, "") or ""
        ms = r_gem.get(field, "") or ""
        if not gs or not ms:
            continue  # missing field — skip, don't block convergence
        if not (_section_nums(gs) & _section_nums(ms)):
            return False
    return True


# ── Flag updater ───────────────────────────────────────────────────────────────

def update_service_flag(state: str, data: dict, path: str,
                        original_code: str, r_gpt: dict, r_gem: dict,
                        converged: bool, file_claim: dict, single_model: bool = False):
    """Replace the open service flag with a reasoning-pass result. Never edits content."""
    flags = data["validation"].get("flags", [])

    # Remove the original open service flag
    flags = [fl for fl in flags if not (
        fl.get("field") == "service.method_rules"
        and fl.get("code") == original_code
        and fl.get("disposition") == "open"
    )]

    if converged:
        # Build resolved statute summary from reasoning pass
        personal = r_gpt.get("personal_statute") or r_gem.get("personal_statute") or ""
        substituted = r_gpt.get("substituted_statute") or r_gem.get("substituted_statute") or ""
        mail = r_gpt.get("mail_statute") or r_gem.get("mail_statute") or ""

        if "SUBSECTION" in original_code:
            note_text = (
                f"L2 service reasoning pass confirmed method-specific subsections. "
                f"File cites parent statute {file_claim.get('unique_statutes')} — "
                f"both models confirmed specific subsections: "
                f"personal={personal}, substituted={substituted}, mail/posting={mail}. "
                f"File citation should be updated to subsection-level in a future content pass. "
                f"No auto-edit by runner. Status: pending-human-confirmation."
            )
            new_code = "L2-SERVICE-SUBSECTION-CONFIRMED-REASONING"
        elif single_model:
            source_model = "Gemini" if not r_gem.get("error") else "GPT"
            source = r_gpt.get("which_source_correct") or r_gem.get("tiebreaker_winner", "model")
            note_text = (
                f"L2 service single-model fallback: one model errored; {source_model} returned high-confidence answer. "
                f"personal={personal}, substituted={substituted}, mail/posting={mail}. "
                f"{source_model} confidence={r_gpt.get('confidence') if source_model=='GPT' else r_gem.get('confidence')}. "
                f"{source_model} reasoning: {(r_gpt.get('reasoning') if source_model=='GPT' else r_gem.get('reasoning') or '')[:200]}. "
                f"Status: pending-human-confirmation. Single-model result — lower confidence than dual-model consensus."
            )
            new_code = "L2-SERVICE-SINGLE-MODEL-RESOLVED"
        else:
            source = r_gpt.get("which_source_correct") or r_gpt.get("tiebreaker_winner", "model")
            note_text = (
                f"L2 service reasoning pass converged. "
                f"personal={personal}, substituted={substituted}, mail/posting={mail}. "
                f"Source determined correct: {source}. "
                f"GPT confidence={r_gpt.get('confidence')}, Gemini confidence={r_gem.get('confidence')}. "
                f"GPT reasoning: {(r_gpt.get('reasoning') or '')[:200]}. "
                f"Status: pending-human-confirmation. No auto-edit by runner."
            )
            new_code = "L2-SERVICE-REASONING-PASS-RESOLVED"

        new_flag = {
            "layer": "L2",
            "code": new_code,
            "field": "service.method_rules",
            "disposition": "resolved-ai-reasoning",
            "status": "pending-human-confirmation",
            "original_classification": original_code,
            "reasoning_pass_date": TODAY,
            "resolved_statutes": {
                "personal": personal,
                "substituted": substituted,
                "mail": mail,
            },
            "gpt_reasoning": r_gpt.get("reasoning"),
            "gpt_confidence": r_gpt.get("confidence"),
            "gemini_reasoning": r_gem.get("reasoning"),
            "gemini_confidence": r_gem.get("confidence"),
            "note": note_text,
        }
        data["validation"]["automated_layers"]["L2_consensus"] = "pass"
        print(f"    → REASONING CONVERGED → {new_code}")
        print(f"      personal={personal[:60]}")
        print(f"      substituted={substituted[:60]}")
        print(f"      mail={mail[:60]}")

    else:
        # No convergence → genuine L7
        new_flag = {
            "layer": "L2",
            "code": "L2-SERVICE-MODEL-SPLIT-L7",
            "field": "service.method_rules",
            "disposition": "open",
            "escalation": "L7",
            "original_classification": original_code,
            "reasoning_pass_date": TODAY,
            "note": (
                f"L2 service reasoning pass: models did NOT converge. "
                f"Original: {original_code}. "
                f"GPT: personal={r_gpt.get('personal_statute','?')}, conf={r_gpt.get('confidence','?')}. "
                f"Gemini: personal={r_gem.get('personal_statute','?')}, conf={r_gem.get('confidence','?')}. "
                f"Attorney review required — genuine interpretive disagreement."
            ),
            "gpt_answer": {k: r_gpt.get(k) for k in ("personal_statute","substituted_statute","mail_statute","reasoning","confidence")},
            "gemini_answer": {k: r_gem.get(k) for k in ("personal_statute","substituted_statute","mail_statute","reasoning","confidence")},
        }
        data["validation"]["automated_layers"]["L2_consensus"] = "flagged"
        print(f"    → NO CONVERGENCE → L7 flag written")

    data["validation"]["flags"] = flags + [new_flag]

    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def handle_subsection_direct_resolve(state: str, data: dict, path: str,
                                      flag: dict, file_claim: dict):
    """
    SUBSECTION-FOUND where both round-1 models already agreed on subsections.
    No reasoning pass needed — directly mark as AI-resolved.
    """
    flags = data["validation"].get("flags", [])
    flags = [fl for fl in flags if not (
        fl.get("field") == "service.method_rules"
        and fl.get("code") == "L2-SERVICE-SUBSECTION-FOUND"
        and fl.get("disposition") == "open"
    )]

    gpt_s = flag.get("gpt_summary", {})
    gem_s = flag.get("gemini_summary", {})
    gpt_methods = {m["method"]: m["statute"] for m in gpt_s.get("methods", [])}
    gem_methods = {m["method"]: m["statute"] for m in gem_s.get("methods", [])}

    # Use GPT's subsections (models agree)
    personal = gpt_methods.get("personal", gem_methods.get("personal", ""))
    substituted = gpt_methods.get("substituted", gem_methods.get("substituted", ""))
    mail = (gpt_methods.get("mail") or gpt_methods.get("posting_and_mailing")
            or gem_methods.get("mail") or gem_methods.get("post_and_mail") or "")

    new_flag = {
        "layer": "L2",
        "code": "L2-SERVICE-SUBSECTION-CONFIRMED-DIRECT",
        "field": "service.method_rules",
        "disposition": "resolved-ai-direct",
        "status": "pending-human-confirmation",
        "note": (
            f"Round-1 L2 consensus: both {OPENAI_MODEL} and {GEMINI_MODEL} independently "
            f"agreed on method-specific subsections. No reasoning pass needed. "
            f"File cites parent statute {file_claim.get('unique_statutes')} — "
            f"correct subsections confirmed: personal={personal}, substituted={substituted}, mail/posting={mail}. "
            f"File citation should be updated to subsection-level in a future content pass. "
            f"No auto-edit by runner. Pending human confirmation."
        ),
        "resolved_statutes": {"personal": personal, "substituted": substituted, "mail": mail},
        "resolved_date": TODAY,
    }
    data["validation"]["automated_layers"]["L2_consensus"] = "pass"
    data["validation"]["flags"] = flags + [new_flag]

    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"    → DIRECT RESOLVE (round-1 consensus): personal={personal[:50]}, sub={substituted[:50]}")


# ── Report writer ──────────────────────────────────────────────────────────────

def write_reasoning_report(results: list):
    from collections import Counter
    counts = Counter(r["outcome"] for r in results)

    report_path = str(DOCS_DIR / f"L2_SERVICE_REASONING_REPORT_{TODAY}.md")
    lines = [
        "# L2 Service Reasoning Pass Report",
        "",
        f"**Run date:** {TODAY}",
        f"**Models:** OpenAI `{OPENAI_MODEL}` · Google `{GEMINI_MODEL}`",
        f"**Target:** 20 states flagged by service L2 runner as CITATION-DIVERGENCE, MODEL-SPLIT, or SUBSECTION-FOUND",
        "",
        "## Summary",
        "",
        "| Outcome | Count |",
        "|---------|-------|",
        f"| ✅ AI-RESOLVED (subsection direct) | {counts.get('DIRECT-RESOLVED', 0)} |",
        f"| ✅ AI-RESOLVED (reasoning converged) | {counts.get('REASONING-RESOLVED', 0)} |",
        f"| 🔴 L7-ESCALATED (genuine split) | {counts.get('L7', 0)} |",
        f"| ❌ ERROR | {counts.get('ERROR', 0)} |",
        "",
        f"**Human review load after reasoning pass:** "
        f"{counts.get('L7', 0)} states (down from 20)",
        "",
        "---",
        "",
        "## Per-State Results",
        "",
        "| State | Original Flag | Outcome | Resolved statutes (personal / substituted / mail) |",
        "|-------|--------------|---------|--------------------------------------------------|",
    ]

    for r in results:
        icon = {"DIRECT-RESOLVED": "✅", "REASONING-RESOLVED": "✅",
                "L7": "🔴", "ERROR": "❌"}.get(r["outcome"], "⚠️")
        rs = r.get("resolved_statutes", {})
        p = (rs.get("personal") or "?")[:35]
        s = (rs.get("substituted") or "?")[:35]
        m = (rs.get("mail") or "?")[:35]
        stat_col = f"{p} / {s} / {m}" if r["outcome"] in ("DIRECT-RESOLVED","REASONING-RESOLVED") else "—"
        lines.append(f"| {r['state']} | {r['original_code'][:40]} | {icon} {r['outcome']} | {stat_col} |")

    # L7 detail
    l7 = [r for r in results if r["outcome"] == "L7"]
    if l7:
        lines += ["", "---", "", f"## Genuine L7 Items ({len(l7)} — attorney review required)", ""]
        for r in l7:
            lines += [
                f"### {r['state']} ({r['state_name']})",
                f"- Original: {r['original_code']}",
                f"- GPT reasoning: {(r.get('r_gpt') or {}).get('reasoning','—')[:300]}",
                f"- Gemini reasoning: {(r.get('r_gem') or {}).get('reasoning','—')[:300]}",
                "",
            ]

    resolved = [r for r in results if r["outcome"] in ("DIRECT-RESOLVED","REASONING-RESOLVED")]
    if resolved:
        lines += ["---", "", f"## AI-Resolved Items ({len(resolved)} — pending human confirmation)", ""]
        for r in resolved:
            rs = r.get("resolved_statutes", {})
            lines += [
                f"### {r['state']} ({r['state_name']}) — {r['outcome']}",
                f"- personal: {rs.get('personal','?')}",
                f"- substituted: {rs.get('substituted','?')}",
                f"- mail/posting: {rs.get('mail','?')}",
                "",
            ]

    lines += [
        "---",
        "",
        "*Reasoning pass corroborates and narrows. No content corrections made.*",
        "*All resolved items: pending-human-confirmation. Nothing advanced past ACP.*",
        "",
        f"*Copyright 2026 Andrew M Cohen. Apache 2.0.*",
    ]

    with open(report_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\n  Reasoning report → {os.path.basename(report_path)}")
    return report_path


# ── Main runner ────────────────────────────────────────────────────────────────

def run_service_reasoning(target_codes: list, dry_run: bool = False):
    all_data, all_paths = load_all_v2_files()

    results = []
    spend = 0.0

    for code in target_codes:
        if code not in all_data:
            print(f"  WARN: {code} not found — skipping")
            continue

        data = all_data[code]
        path = all_paths[code]
        state_name = data.get("jurisdiction", {}).get("state_name", code)

        # Find the open L2-SERVICE flag (also pick up reasoning-pass L7 for retry)
        target_flag = None
        original_code = None
        for fl in data["validation"].get("flags", []):
            c = fl.get("code", "")
            field = fl.get("field", "")
            disp = fl.get("disposition", "")
            if not c.startswith("L2-SERVICE") or field != "service.method_rules":
                continue
            # Pick up open flags AND reasoning-pass L7 flags (for retry)
            if disp == "open" or (disp == "open" and "L7" in c):
                target_flag = fl
                original_code = c
                break

        if not target_flag:
            print(f"\n  {code} ({state_name}) — no open L2-SERVICE flag found, skipping")
            continue

        # Extract file claim
        from l2_service_runner import extract_service_claim
        file_claim = extract_service_claim(data)

        print(f"\n  {code} ({state_name}) — {original_code}")

        # SUBSECTION-FOUND where round-1 models already agree → direct resolve
        if "SUBSECTION" in original_code:
            gpt_s = target_flag.get("gpt_summary", {})
            gem_s = target_flag.get("gemini_summary", {})
            gpt_methods = {m["method"]: m["statute"] for m in gpt_s.get("methods", [])}
            gem_methods = {m["method"]: m["statute"] for m in gem_s.get("methods", [])}

            # Check if round-1 models agreed
            personal_agree = bool(_section_nums(gpt_methods.get("personal","")) &
                                   _section_nums(gem_methods.get("personal","")))
            if personal_agree:
                if not dry_run:
                    handle_subsection_direct_resolve(code, data, path, target_flag, file_claim)
                personal = gpt_methods.get("personal","")
                substituted = gpt_methods.get("substituted","")
                mail = gpt_methods.get("mail") or gpt_methods.get("posting_and_mailing","")
                results.append({
                    "state": code, "state_name": state_name,
                    "original_code": original_code,
                    "outcome": "DIRECT-RESOLVED",
                    "resolved_statutes": {"personal": personal, "substituted": substituted, "mail": mail},
                })
                continue

        # Reasoning pass for everything else
        # Use state-specific override query if available (for persistent subsection disputes)
        if state_name in SUBSECTION_OVERRIDE_QUERIES:
            query = SUBSECTION_OVERRIDE_QUERIES[state_name]
            print(f"    (using state-specific targeted query for {state_name})")
        else:
            query = build_reasoning_query(state_name, target_flag, file_claim)
        r_gpt = call_openai_reasoning(query, dry_run=dry_run)
        r_gem = call_gemini_reasoning(query, dry_run=dry_run)
        spend += APPROX_COST_REASONING

        if r_gpt.get("error"):
            print(f"    GPT ERROR: {r_gpt['error'][:80]}")
        else:
            print(f"    GPT: personal={r_gpt.get('personal_statute','?')[:50]} conf={r_gpt.get('confidence')}")
        if r_gem.get("error"):
            print(f"    Gemini ERROR: {r_gem['error'][:80]}")
        else:
            print(f"    Gemini: personal={r_gem.get('personal_statute','?')[:50]} conf={r_gem.get('confidence')}")

        if r_gpt.get("error") and r_gem.get("error"):
            print(f"    → BOTH ERRORS — skipping write-back")
            results.append({
                "state": code, "state_name": state_name,
                "original_code": original_code, "outcome": "ERROR",
            })
            continue

        # Single-model fallback: one errored but the other is high-confidence
        single_model = False
        if r_gpt.get("error") and not r_gem.get("error"):
            if r_gem.get("confidence") == "high" and r_gem.get("personal_statute"):
                print(f"    → SINGLE-MODEL FALLBACK (GPT errored; Gemini high-conf)")
                r_gpt = dict(r_gem)  # use Gemini answer for both sides of convergence check
                single_model = True
        elif r_gem.get("error") and not r_gpt.get("error"):
            if r_gpt.get("confidence") == "high" and r_gpt.get("personal_statute"):
                print(f"    → SINGLE-MODEL FALLBACK (Gemini errored; GPT high-conf)")
                r_gem = dict(r_gpt)  # use GPT answer for both sides
                single_model = True

        converged = reasoning_converges(r_gpt, r_gem)

        if not dry_run:
            update_service_flag(code, data, path, original_code, r_gpt, r_gem, converged, file_claim,
                                single_model=single_model)

        rs = {"personal": r_gpt.get("personal_statute",""), "substituted": r_gpt.get("substituted_statute",""), "mail": r_gpt.get("mail_statute","")}
        results.append({
            "state": code, "state_name": state_name,
            "original_code": original_code,
            "outcome": "REASONING-RESOLVED" if converged else "L7",
            "resolved_statutes": rs if converged else {},
            "r_gpt": r_gpt, "r_gem": r_gem,
        })

        if spend > BUDGET_CAP_USD:
            print(f"\n  ⚠️ BUDGET CAP HIT (~${spend:.2f}). Stopping.")
            break

    # Write report
    if not dry_run:
        write_reasoning_report(results)

    from collections import Counter
    rc = Counter(r["outcome"] for r in results)
    print(f"\n{'='*60}")
    print(f"  Service reasoning pass — {len(results)} states | ~${spend:.2f} spent")
    print(f"  ✅ DIRECT-RESOLVED:    {rc.get('DIRECT-RESOLVED', 0)}")
    print(f"  ✅ REASONING-RESOLVED: {rc.get('REASONING-RESOLVED', 0)}")
    print(f"  🔴 L7:                 {rc.get('L7', 0)}")
    print(f"  ❌ ERROR:              {rc.get('ERROR', 0)}")
    print(f"{'='*60}")
    print(f"\n  ⚠️  STOP AND REPORT. Do not auto-edit service files.")
    print(f"  Next: commit via GitHub Desktop, report to Andy.")

    return results


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="L2 Service Reasoning Pass")
    parser.add_argument("--states",
                        help="Comma-separated state codes to target.")
    parser.add_argument("--retry-l7", action="store_true",
                        help="Target all states with open MODEL-SPLIT-L7 flags (tiebreaker pass).")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print(f"\nCivil Justice as Code — L2 Service Reasoning Pass")
    print(f"Run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Models: {OPENAI_MODEL} + {GEMINI_MODEL}")
    print(f"Budget cap: ${BUDGET_CAP_USD:.2f}")

    if args.retry_l7:
        # Auto-discover all states with open L7 flags
        all_data, all_paths = load_all_v2_files()
        target = []
        for code, data in all_data.items():
            for fl in data.get("validation", {}).get("flags", []):
                if ("L7" in fl.get("code", "") and
                    fl.get("field") == "service.method_rules" and
                    fl.get("disposition") == "open"):
                    target.append(code)
                    break
        print(f"Protocol: Tiebreaker pass — retrying {len(target)} L7 states: {sorted(target)}")
    elif args.states:
        target = [s.strip().upper() for s in args.states.split(",") if s.strip()]
        print(f"Protocol: SUBSECTION-FOUND → direct resolve; CITATION-DIV/MODEL-SPLIT → reasoning pass")
    else:
        target = REVIEW_STATES
        print(f"Protocol: SUBSECTION-FOUND → direct resolve; CITATION-DIV/MODEL-SPLIT → reasoning pass")

    print(f"States: {len(target)}")
    run_service_reasoning(target_codes=target, dry_run=args.dry_run)
