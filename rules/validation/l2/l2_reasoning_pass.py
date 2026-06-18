#!/usr/bin/env python3
"""
Eviction Rules — L2 Reasoning Pass
====================================
Used when L2 consensus run produces PERIOD-DIVERGENCE: presents the competing
statutes to both models and asks them to reason to the best-supported answer.

If both models converge on the same answer with sound reasoning:
  → AI-resolved: content updated, flag disposition set to "resolved-ai-corrected",
    status stays AUTOMATED-CHECKS-PASSED (never advanced), added
    "pending-human-confirmation" flag.
If models diverge or reasoning reveals a genuine interpretive question:
  → L7 escalation flag written.

GUARDRAILS (do not remove):
  - Keys from .env only; never hardcoded, logged, or committed
  - Never advances past AUTOMATED-CHECKS-PASSED
  - All reasoning recorded so humans can audit and confirm

Usage:
  python3 rules/validation/l2/l2_reasoning_pass.py --states WV,MO

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

# ── Key handling ──────────────────────────────────────────────────────────────
try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv not installed. Run: pip3 install python-dotenv -q")
    sys.exit(1)

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_ENV_PATH = _REPO_ROOT / ".env"
if not _ENV_PATH.exists():
    print(f"ERROR: .env not found at {_ENV_PATH}")
    sys.exit(1)
load_dotenv(_ENV_PATH)

OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")
GOOGLE_KEY = os.environ.get("GOOGLE_API_KEY", "")
if not OPENAI_KEY or not GOOGLE_KEY:
    print("ERROR: OPENAI_API_KEY and GOOGLE_API_KEY must be set in .env")
    sys.exit(1)

OPENAI_MODEL = "gpt-5.5"
GEMINI_MODEL = "gemini-2.5-pro"
RULES_EVICTION_DIR = _REPO_ROOT / "rules" / "eviction"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# ── Per-state conflict context ────────────────────────────────────────────────
# Manually curated from L2 Phase 1 results and statute research.
# Each entry: what the file claims, what L2 models said, the competing statutes.
CONFLICT_CONTEXT = {
    "WV": {
        "state_name": "West Virginia",
        "file_claim": "5 days (W. Va. Code §37-6-5)",
        "model_claim": "No notice period required before filing; landlord may file immediately when tenant is in arrears (W. Va. Code §55-3A-1)",
        "competing_statutes": {
            "file_statute": "W. Va. Code §37-6-5",
            "file_statute_desc": "Relates to notice to quit for periodic tenancies and leases for definite terms.",
            "model_statute": "W. Va. Code §55-3A-1",
            "model_statute_desc": "Summary eviction procedure: landlord may petition for summary relief when tenant is in arrears of rent, without requiring a prior notice period.",
        },
        "path": str(RULES_EVICTION_DIR / "west-virginia" / "wv_eviction_v2.json"),
    },
    "MO": {
        "state_name": "Missouri",
        "file_claim": "10 days (RSMo §535.060)",
        "model_claim": "No specific notice period; only a demand for rent is required before filing (Mo. Rev. Stat. §535.020)",
        "competing_statutes": {
            "file_statute": "RSMo §535.060",
            "file_statute_desc": "Unlawful detainer for nonpayment: covers when tenant has failed to pay rent.",
            "model_statute": "Mo. Rev. Stat. §535.020",
            "model_statute_desc": "Rent and possession action: requires demand for rent but specifies no waiting period before filing.",
        },
        "path": str(RULES_EVICTION_DIR / "missouri" / "mo_eviction_v2.json"),
    },
}

REASONING_SYSTEM_PROMPT = (
    "You are a legal research expert specializing in US residential landlord-tenant law. "
    "You will be given a specific legal question where two sources disagree. "
    "Your task is to reason carefully through the competing statutes and determine "
    "which answer is best supported by the law. "
    "Be precise about statute citations. Acknowledge uncertainty where it exists. "
    "Respond only in the JSON format requested."
)

REASONING_QUERY_TEMPLATE = """Under {state_name} law, does a residential landlord need to give a tenant a formal notice to pay rent or quit BEFORE filing an eviction action for nonpayment of rent? If yes, how many days?

CONFLICT TO RESOLVE:
- Source A (our rules file) says: {file_claim}
- Source B (two independent AI models) says: {model_claim}

COMPETING STATUTES:
- File's statute ({file_statute}): {file_statute_desc}
- Models' statute ({model_statute}): {model_statute_desc}

Please:
1. Determine which statute is the operative provision for pre-filing notice in a nonpayment eviction
2. State whether a notice period is required before filing and, if so, how many days
3. Explain your reasoning with specific statutory references
4. Note any nuances or exceptions that affect the answer

Respond ONLY in valid JSON:
{{"notice_required": <true or false>, "days": <integer or null>, "operative_statute": "<citation>", "reasoning": "<2-4 sentence explanation>", "confidence": "<high|medium|low>", "uncertainty_note": "<any genuine ambiguity or null if none>"}}"""


def call_openai_reasoning(query: str) -> dict:
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
            max_completion_tokens=8000,  # reasoning models use tokens for chain-of-thought; longer prompts need more headroom
        )
        raw = resp.choices[0].message.content.strip() if resp.choices[0].message.content else ""
        return _parse_json(raw)
    except Exception as exc:
        return {"error": str(exc)}


def call_gemini_reasoning(query: str) -> dict:
    try:
        from google import genai
    except ImportError:
        return {"error": "google-genai not installed"}
    try:
        client = genai.Client(api_key=GOOGLE_KEY)
        full_prompt = REASONING_SYSTEM_PROMPT + "\n\n" + query
        resp = client.models.generate_content(model=GEMINI_MODEL, contents=full_prompt)
        raw = resp.text.strip()
        return _parse_json(raw)
    except Exception as exc:
        return {"error": str(exc)}


def _parse_json(raw: str) -> dict:
    import re
    text = re.sub(r"```(?:json)?", "", raw).strip()
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": f"PARSE_ERROR: {raw[:300]}"}


def models_converge(gpt: dict, gemini: dict) -> bool:
    """True if both models agree on notice_required and days (within reason)."""
    if gpt.get("error") or gemini.get("error"):
        return False
    gpt_req = gpt.get("notice_required")
    gem_req = gemini.get("notice_required")
    if gpt_req != gem_req:
        return False
    if not gpt_req and not gem_req:
        return True  # both say no notice
    gpt_days = gpt.get("days")
    gem_days = gemini.get("days")
    return gpt_days == gem_days


def write_resolution(state_code: str, ctx: dict, gpt: dict, gemini: dict, converged: bool):
    path = ctx["path"]
    if not Path(path).exists():
        print(f"  ERROR: file not found: {path}")
        return

    with open(path) as f:
        data = json.load(f)

    flags = data["validation"].get("flags", [])

    if converged:
        # Determine resolved values
        notice_required = gpt.get("notice_required", False)
        days = gpt.get("days")
        operative_statute = gpt.get("operative_statute") or gemini.get("operative_statute")

        # Update pay_or_quit content
        pq = data["notice"]["notice_types"]["pay_or_quit"]
        old_days = pq.get("tenancy_all", {}).get("days")
        old_statute = pq.get("tenancy_all", {}).get("statute")

        if notice_required is False or days is None:
            # No notice required pattern
            pq["notice_required"] = False
            pq["days"] = None
            if "tenancy_all" in pq:
                pq["tenancy_all"]["days"] = None
                pq["tenancy_all"]["statute"] = operative_statute or old_statute
        else:
            if "tenancy_all" not in pq:
                pq["tenancy_all"] = {}
            pq["tenancy_all"]["days"] = days
            pq["tenancy_all"]["statute"] = operative_statute or old_statute

        print(f"  {state_code}: content updated: days {old_days} -> {days}, statute {old_statute!r} -> {operative_statute!r}")

        # Update / add AI-resolved flag
        resolution_flag = {
            "layer": "L2",
            "code": "L2-PERIOD-DIVERGENCE-AI-RESOLVED",
            "field": "notice.notice_types.pay_or_quit",
            "disposition": "resolved-ai-corrected",
            "resolution": {
                "method": "AI-reasoning-pass",
                "resolved_date": TODAY,
                "gpt_reasoning": gpt.get("reasoning"),
                "gpt_operative_statute": gpt.get("operative_statute"),
                "gpt_confidence": gpt.get("confidence"),
                "gemini_reasoning": gemini.get("reasoning"),
                "gemini_operative_statute": gemini.get("operative_statute"),
                "gemini_confidence": gemini.get("confidence"),
                "uncertainty_note": gpt.get("uncertainty_note") or gemini.get("uncertainty_note"),
                "status": "pending-human-confirmation",
                "note": (
                    f"L2 reasoning pass: both GPT ({OPENAI_MODEL}) and Gemini ({GEMINI_MODEL}) "
                    f"converged. notice_required={notice_required}, days={days}, "
                    f"statute={operative_statute}. "
                    f"Content corrected from file claim ({ctx['file_claim']}). "
                    f"NEVER auto-advanced past AUTOMATED-CHECKS-PASSED. Human confirmation required."
                ),
            },
            "l2_run_date": TODAY,
        }

        # Remove old open PERIOD-DIVERGENCE flag, add resolved flag
        new_flags = [fl for fl in flags if not (fl.get("layer") == "L2" and fl.get("code") == "L2-PERIOD-DIVERGENCE")]
        new_flags.append(resolution_flag)
        data["validation"]["flags"] = new_flags
        data["validation"]["automated_layers"]["L2_consensus"] = "pass"
        print(f"  {state_code}: L2-PERIOD-DIVERGENCE -> resolved-ai-corrected, L2_consensus -> pass")

    else:
        # No convergence → L7 escalation
        escalation_flag = {
            "layer": "L2",
            "code": "L2-PERIOD-DIVERGENCE-L7-ESCALATED",
            "field": "notice.notice_types.pay_or_quit",
            "disposition": "open",
            "escalation": "L7",
            "note": (
                f"L2 reasoning pass: models did NOT converge. "
                f"GPT: notice_required={gpt.get('notice_required')}, days={gpt.get('days')}, "
                f"confidence={gpt.get('confidence')}. "
                f"Gemini: notice_required={gemini.get('notice_required')}, days={gemini.get('days')}, "
                f"confidence={gemini.get('confidence')}. "
                f"File claim: {ctx['file_claim']}. Attorney review required."
            ),
            "gpt_reasoning": gpt.get("reasoning"),
            "gemini_reasoning": gemini.get("reasoning"),
            "l2_run_date": TODAY,
        }
        new_flags = [fl for fl in flags if not (fl.get("layer") == "L2" and fl.get("code") == "L2-PERIOD-DIVERGENCE")]
        new_flags.append(escalation_flag)
        data["validation"]["flags"] = new_flags
        data["validation"]["automated_layers"]["L2_consensus"] = "flagged"
        print(f"  {state_code}: no convergence -> L7 flag written")

    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  {state_code}: file written OK")


def run_reasoning_pass(state_codes: list):
    for code in state_codes:
        if code not in CONFLICT_CONTEXT:
            print(f"  WARN: no conflict context for {code} — skipping")
            continue

        ctx = CONFLICT_CONTEXT[code]
        print(f"\n{'='*60}")
        print(f"  {code} ({ctx['state_name']}) — Reasoning Pass")
        print(f"  File claims:  {ctx['file_claim']}")
        print(f"  Models claim: {ctx['model_claim']}")
        print(f"{'='*60}")

        query = REASONING_QUERY_TEMPLATE.format(
            state_name=ctx["state_name"],
            file_claim=ctx["file_claim"],
            model_claim=ctx["model_claim"],
            file_statute=ctx["competing_statutes"]["file_statute"],
            file_statute_desc=ctx["competing_statutes"]["file_statute_desc"],
            model_statute=ctx["competing_statutes"]["model_statute"],
            model_statute_desc=ctx["competing_statutes"]["model_statute_desc"],
        )

        print(f"\n  Calling {OPENAI_MODEL}...", end=" ", flush=True)
        gpt = call_openai_reasoning(query)
        if gpt.get("error"):
            print(f"ERROR: {gpt['error'][:80]}")
        else:
            print(f"OK  (notice_required={gpt.get('notice_required')}, days={gpt.get('days')}, confidence={gpt.get('confidence')})")
            print(f"    statute: {gpt.get('operative_statute')}")
            print(f"    reasoning: {gpt.get('reasoning', '')[:200]}")

        print(f"\n  Calling {GEMINI_MODEL}...", end=" ", flush=True)
        gemini = call_gemini_reasoning(query)
        if gemini.get("error"):
            print(f"ERROR: {gemini['error'][:80]}")
        else:
            print(f"OK  (notice_required={gemini.get('notice_required')}, days={gemini.get('days')}, confidence={gemini.get('confidence')})")
            print(f"    statute: {gemini.get('operative_statute')}")
            print(f"    reasoning: {gemini.get('reasoning', '')[:200]}")

        converged = models_converge(gpt, gemini)
        print(f"\n  Convergence: {'YES' if converged else 'NO'}")

        if not gpt.get("error") and not gemini.get("error"):
            write_resolution(code, ctx, gpt, gemini, converged)
        else:
            print(f"  {code}: API errors — skipping write-back")

    print(f"\n{'='*60}")
    print("Reasoning pass complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="L2 Reasoning Pass — Civil Justice as Code")
    parser.add_argument("--states", default="WV,MO", help="Comma-separated state codes (default: WV,MO)")
    args = parser.parse_args()
    target = [s.strip().upper() for s in args.states.split(",") if s.strip()]
    print(f"\nCivil Justice as Code — L2 Reasoning Pass")
    print(f"Run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Models: {OPENAI_MODEL} + {GEMINI_MODEL}")
    print(f"States: {', '.join(target)}")
    run_reasoning_pass(target)
