#!/usr/bin/env python3
"""
Eviction Rules — L2 Phase 2 Retry Runner
==========================================
Targeted retry for 9 states that failed in Phase 2 due to GPT parse errors
(chain-of-thought filling the 2000-token budget before JSON output) or
Gemini API errors.

Affected states:
  GPT parse-error pseudo-splits: AR, DC, KY, LA, MA, TN, VA
  Both-model errors:             GA, IA

Fix: raise GPT max_completion_tokens to 6000 (enough for chain-of-thought + JSON).
     Gemini is retried normally.

After retry:
  - If both models now agree → classify normally (CONFIRM / CITATION-AI-RESOLVED / etc.)
  - If still split after real answers → genuine L7 → escalate
  - Clears the stale L7 flags written by Phase 2 for these states
  - Appends retry outcomes to HUMAN_REVIEW_QUEUE.md
  - Writes retry section to L2_CONSENSUS_REPORT_PHASE2_2026-06-18.md (appends)

Usage (run from repo root on Andy's local machine):
  python3 rules/validation/l2/l2_phase2_retry.py
  python3 rules/validation/l2/l2_phase2_retry.py --dry-run

GUARDRAILS: same as all L2 runners — never advances past ACP; never hardcodes keys.

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_L2_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_L2_DIR))

from l2_runner import (
    _parse_json_response,
    _error_result,
    classify,
    extract_file_claim,
    load_all_v2_files,
    _extract_section_nums,
    OPENAI_MODEL,
    GEMINI_MODEL,
    OPENAI_KEY,
    GOOGLE_KEY,
    SYSTEM_PROMPT,
    RULES_EVICTION_DIR,
    DOCS_DIR,
    BUDGET_CAP_USD,
)

from l2_phase2_runner import (
    resolve_citation,
    run_reasoning_pass,
    write_model_split_l7,
    write_consensus_confirm,
    append_to_queue,
    build_query,
)

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# ── Retry targets ─────────────────────────────────────────────────────────────

# 7 GPT-parse-error states + 2 both-model-error states
RETRY_STATES = ["AR", "DC", "GA", "IA", "KY", "LA", "MA", "TN", "VA"]

# Cost: 9 states × $0.02 (higher token budget still cheap) + possible reasoning passes
APPROX_COST_PER_STATE = 0.04  # conservative — higher tokens
REASONING_COST = 0.08

# ── GPT call with higher token budget ────────────────────────────────────────

def call_openai_retry(query: str, dry_run: bool = False) -> dict:
    """Same as call_openai but with 6000 token budget to clear chain-of-thought."""
    if dry_run:
        return {"days": 3, "notice_required": True, "statute": "DRY-RUN", "rationale": "dry run retry", "model": OPENAI_MODEL, "_raw": ""}
    try:
        from openai import OpenAI
    except ImportError:
        return _error_result("openai package not installed", OPENAI_MODEL)
    try:
        client = OpenAI(api_key=OPENAI_KEY)
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
            max_completion_tokens=6000,  # raised from 2000 to clear chain-of-thought
        )
        raw = resp.choices[0].message.content
        raw = raw.strip() if raw else ""
        parsed = _parse_json_response(raw)
        parsed["model"] = OPENAI_MODEL
        parsed["_raw"] = raw
        return parsed
    except Exception as exc:
        return _error_result(str(exc), OPENAI_MODEL)


def call_gemini_retry(query: str, dry_run: bool = False) -> dict:
    """Standard Gemini call (same as Phase 2)."""
    if dry_run:
        return {"days": 3, "notice_required": True, "statute": "DRY-RUN", "rationale": "dry run retry", "model": GEMINI_MODEL, "_raw": ""}
    try:
        from google import genai
    except ImportError:
        return _error_result("google-genai not installed", GEMINI_MODEL)
    try:
        client = genai.Client(api_key=GOOGLE_KEY)
        full_prompt = SYSTEM_PROMPT + "\n\n" + query
        resp = client.models.generate_content(model=GEMINI_MODEL, contents=full_prompt)
        raw = resp.text.strip()
        parsed = _parse_json_response(raw)
        parsed["model"] = GEMINI_MODEL
        parsed["_raw"] = raw
        return parsed
    except Exception as exc:
        return _error_result(str(exc), GEMINI_MODEL)


# ── Clear stale Phase 2 L7 flags ─────────────────────────────────────────────

def clear_stale_l7_flags(data: dict) -> dict:
    """Remove L7 flags written by Phase 2 for parse-error pseudo-splits."""
    flags = data["validation"].get("flags", [])
    stale_codes = {"L2-MODEL-SPLIT-L7", "L2-PERIOD-DIVERGENCE-L7-ESCALATED"}
    before = len(flags)
    flags = [
        fl for fl in flags
        if not (fl.get("layer") == "L2" and fl.get("code") in stale_codes and fl.get("disposition") == "open")
    ]
    if len(flags) < before:
        print(f"    Cleared {before - len(flags)} stale Phase 2 L7 flag(s)")
    data["validation"]["flags"] = flags
    return data


# ── Write retry outcome back to file ─────────────────────────────────────────

def write_retry_confirm(state: str, data: dict, path: str, gpt: dict, gemini: dict):
    """Record CONSENSUS-CONFIRM result from retry."""
    data["validation"].setdefault("automated_layers", {})["L2_consensus"] = "pass"
    data["validation"]["l2_results"] = {
        "run_date": TODAY,
        "classification": "CONSENSUS-CONFIRM",
        "retry": True,
        "gpt": {"model": gpt.get("model"), "days": gpt.get("days"), "statute": gpt.get("statute"), "rationale": gpt.get("rationale")},
        "gemini": {"model": gemini.get("model"), "days": gemini.get("days"), "statute": gemini.get("statute"), "rationale": gemini.get("rationale")},
    }
    # Add a CONFIRM flag noting the retry resolved the parse error
    flags = data["validation"].get("flags", [])
    flags.append({
        "layer": "L2",
        "code": "L2-RETRY-CONSENSUS-CONFIRM",
        "disposition": "resolved",
        "note": (
            f"Phase 2 retry (6000-token GPT budget): CONSENSUS-CONFIRM. "
            f"GPT: {gpt.get('days')}d, {gpt.get('statute')}. "
            f"Gemini: {gemini.get('days')}d, {gemini.get('statute')}. "
            f"Phase 2 GPT parse error was a token-budget artifact, not a genuine split."
        ),
        "l2_run_date": TODAY,
    })
    data["validation"]["flags"] = flags
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── Retry report ──────────────────────────────────────────────────────────────

def append_retry_to_report(results: list[dict]):
    """Append retry section to the Phase 2 report."""
    from collections import Counter

    report_path = DOCS_DIR / f"L2_CONSENSUS_REPORT_PHASE2_{TODAY}.md"
    # Try to find any Phase 2 report if today's doesn't exist
    if not report_path.exists():
        candidates = sorted(DOCS_DIR.glob("L2_CONSENSUS_REPORT_PHASE2_*.md"), reverse=True)
        if candidates:
            report_path = candidates[0]

    rc = Counter(r["resolution_type"] for r in results)

    retry_lines = [
        "",
        "---",
        "",
        f"## Retry Run — {TODAY} (9 states: 7 GPT-parse-error + 2 model-error)",
        "",
        f"**Reason:** Phase 2 classified 7 states as MODEL-SPLIT→L7 due to GPT chain-of-thought",
        f"filling the 2000-token budget before producing JSON output. Fix: `max_completion_tokens=6000`.",
        "",
        "| State | File days | GPT (retry) | Gemini (retry) | L2 Class | Resolution |",
        "|-------|-----------|------------|----------------|----------|------------|",
    ]

    for r in results:
        fc = r["file_claim"]
        gpt = r["gpt"]
        gem = r["gemini"]
        rt = r.get("resolution_type", r.get("classification", "?"))
        icon = {
            "CONSENSUS-CONFIRM": "✅", "CITATION-AI-RESOLVED": "✅", "PERIOD-AI-RESOLVED": "✅",
            "L7-ESCALATED": "🔴", "PERIOD-L7-ESCALATED": "🔴", "ERROR": "❌",
            "CITATION-UNRESOLVED": "🟡",
        }.get(rt, "⚠️")
        fd = str(fc["days"]) if fc["days"] is not None else "none"
        gd = str(gpt.get("days")) if gpt.get("days") is not None else ("ERR" if gpt.get("error") else "none")
        md = str(gem.get("days")) if gem.get("days") is not None else ("ERR" if gem.get("error") else "none")
        gs = (gpt.get("statute") or "ERR")[:30]
        ms = (gem.get("statute") or "ERR")[:30]
        retry_lines.append(f"| {r['state']} | {fd} | {gd} ({gs}) | {md} ({ms}) | {r['classification']} | {icon} {rt} |")

    retry_lines += [
        "",
        f"**Retry summary:** ✅ CONFIRM: {rc.get('CONSENSUS-CONFIRM', 0)} · "
        f"✅ CITATION-AI-RES: {rc.get('CITATION-AI-RESOLVED', 0)} · "
        f"✅ PERIOD-AI-RES: {rc.get('PERIOD-AI-RESOLVED', 0)} · "
        f"🔴 L7: {rc.get('L7-ESCALATED', 0) + rc.get('PERIOD-L7-ESCALATED', 0)} · "
        f"❌ ERROR: {rc.get('ERROR', 0)}",
        "",
    ]

    if report_path.exists():
        with open(report_path) as f:
            content = f.read()
        with open(report_path, "w") as f:
            f.write(content.rstrip() + "\n" + "\n".join(retry_lines) + "\n")
    else:
        # Write standalone retry report
        retry_report_path = DOCS_DIR / f"L2_RETRY_REPORT_{TODAY}.md"
        with open(retry_report_path, "w") as f:
            f.write(f"# L2 Phase 2 Retry Report — {TODAY}\n" + "\n".join(retry_lines) + "\n")
        report_path = retry_report_path

    print(f"\n  Retry results appended → {report_path.name}")


# ── Main ──────────────────────────────────────────────────────────────────────

def run_retry(dry_run: bool = False):
    all_data, all_paths = load_all_v2_files()

    missing = [c for c in RETRY_STATES if c not in all_data]
    if missing:
        print(f"  WARN: states not found: {missing}")

    states = [c for c in RETRY_STATES if c in all_data]
    est_cost = len(states) * APPROX_COST_PER_STATE + 3 * REASONING_COST  # assume up to 3 reasoning passes
    print(f"\nCivil Justice as Code — L2 Phase 2 Retry Runner")
    print(f"Run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"States: {states}")
    print(f"Fix: GPT max_completion_tokens 2000 → 6000")
    print(f"Est. cost: ~${est_cost:.2f} · Hard cap: ${BUDGET_CAP_USD:.2f}")
    if dry_run:
        print("MODE: DRY RUN — no API calls, no write-back\n")

    results = []
    queue_items = []
    spend = 0.0
    item_n = 0

    for code in states:
        data = all_data[code]
        path = all_paths[code]
        state_name = data.get("jurisdiction", {}).get("state_name", code)
        file_claim = extract_file_claim(data)

        statute_preview = repr(file_claim.get("statute", ""))[:40]
        print(f"\n  {code} ({state_name}) — file: {file_claim['days']}d {statute_preview}")

        # Clear stale Phase 2 L7 flags before retry
        if not dry_run:
            data = clear_stale_l7_flags(data)

        query = build_query(state_name)
        gpt = call_openai_retry(query, dry_run=dry_run)
        gem = call_gemini_retry(query, dry_run=dry_run)
        spend += APPROX_COST_PER_STATE

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

        resolution_type = classification
        r_gpt, r_gem = {}, {}

        if classification == "CONSENSUS-CONFIRM":
            if not dry_run:
                write_retry_confirm(code, data, path, gpt, gem)

        elif classification == "CITATION-DIVERGENCE":
            if not dry_run:
                resolution_type = resolve_citation(code, data, path, file_claim, gpt, gem)
            else:
                gpt_secs = _extract_section_nums(gpt.get("statute") or "")
                gem_secs = _extract_section_nums(gem.get("statute") or "")
                resolution_type = "CITATION-AI-RESOLVED" if (gpt_secs & gem_secs) else "CITATION-UNRESOLVED"
                print(f"    (dry run — would be {resolution_type})")
            item_n += 1
            queue_items.append({
                "state": code, "state_name": state_name,
                "qid": f"{code}-RETRY-{item_n:02d}",
                "classification": classification, "resolution_type": resolution_type,
                "file_claim": file_claim, "gpt": gpt, "gemini": gem,
            })

        elif classification == "PERIOD-DIVERGENCE":
            spend += REASONING_COST
            if not dry_run:
                resolution_type, r_gpt, r_gem, _ = run_reasoning_pass(
                    code, state_name, data, path, file_claim, gpt, gem, dry_run=False)
            else:
                resolution_type = "PERIOD-AI-RESOLVED"
                print("    (dry run — would run reasoning pass)")
            item_n += 1
            queue_items.append({
                "state": code, "state_name": state_name,
                "qid": f"{code}-RETRY-{item_n:02d}",
                "classification": classification, "resolution_type": resolution_type,
                "file_claim": file_claim, "gpt": gpt, "gemini": gem,
                "r_gpt": r_gpt, "r_gem": r_gem,
            })

        elif classification == "MODEL-SPLIT":
            # After retry with higher token budget, this is a genuine split
            if not dry_run:
                write_model_split_l7(code, data, path, file_claim, gpt, gem)
            resolution_type = "L7-ESCALATED"
            print(f"    → Genuine MODEL-SPLIT after retry → L7")
            item_n += 1
            queue_items.append({
                "state": code, "state_name": state_name,
                "qid": f"{code}-RETRY-{item_n:02d}",
                "classification": classification, "resolution_type": resolution_type,
                "file_claim": file_claim, "gpt": gpt, "gemini": gem,
            })

        elif classification == "ERROR":
            resolution_type = "ERROR"
            print(f"    ERROR after retry — will need manual investigation")

        if spend > BUDGET_CAP_USD:
            print(f"\n  ⚠️ BUDGET CAP HIT (~${spend:.2f}). Stopping.")
            results.append({
                "state": code, "state_name": state_name,
                "file_claim": file_claim, "gpt": gpt, "gemini": gem,
                "classification": classification, "resolution_type": resolution_type,
                "r_gpt": r_gpt, "r_gem": r_gem,
            })
            break

        results.append({
            "state": code, "state_name": state_name,
            "file_claim": file_claim, "gpt": gpt, "gemini": gem,
            "classification": classification, "resolution_type": resolution_type,
            "r_gpt": r_gpt, "r_gem": r_gem,
        })

    # Write report and update queue
    if not dry_run:
        append_retry_to_report(results)
        if queue_items:
            append_to_queue(queue_items)

    from collections import Counter
    rc = Counter(r["resolution_type"] for r in results)

    print(f"\n{'='*60}")
    print(f"  L2 Phase 2 Retry complete — {len(results)} states | ~${spend:.2f} spent")
    print(f"  ✅ CONFIRM:          {rc.get('CONSENSUS-CONFIRM', 0)}")
    print(f"  ✅ CITATION-AI-RES:  {rc.get('CITATION-AI-RESOLVED', 0)} (pending confirmation)")
    print(f"  ✅ PERIOD-AI-RES:    {rc.get('PERIOD-AI-RESOLVED', 0)} (pending confirmation)")
    print(f"  🟡 CITATION-UNRES:   {rc.get('CITATION-UNRESOLVED', 0)} (human review)")
    print(f"  🔴 L7-ESCALATED:    {rc.get('L7-ESCALATED', 0) + rc.get('PERIOD-L7-ESCALATED', 0)}")
    print(f"  ❌ ERROR:            {rc.get('ERROR', 0)}")
    print(f"{'='*60}")
    print(f"\n  ⚠️  STOP AND REPORT. Do not start Phase 3.")
    print(f"  Next: commit all changed files via GitHub Desktop, then report to Andy.")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="L2 Phase 2 Retry — fix GPT parse errors with higher token budget"
    )
    parser.add_argument("--dry-run", action="store_true", help="No API calls, no write-back.")
    args = parser.parse_args()

    run_retry(dry_run=args.dry_run)
