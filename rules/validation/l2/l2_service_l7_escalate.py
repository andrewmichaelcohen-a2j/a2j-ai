#!/usr/bin/env python3
"""
L2 Service — L7 Escalation Script
===================================
Writes clean L7-ESCALATED flags for states that could not be resolved
by the L2 service runner or reasoning/tiebreaker passes.

Targets:
  - DC: persistent ERROR (both models failed 3+ attempts, no recoverable data)
  - IN: genuine MODEL-SPLIT (both models high-confidence but disagreeing through
         two tiebreaker passes: GPT §32-31-1-9(b)(1) vs Gemini §32-31-1-9(a))
  - NM: persistent ERROR (both models failed 3+ attempts, no recoverable data)

These states require attorney review (L7). No content edits made.
Nothing advances past AUTOMATED-CHECKS-PASSED.

Usage:
  python3 rules/validation/l2/l2_service_l7_escalate.py
  python3 rules/validation/l2/l2_service_l7_escalate.py --states DC,IN,NM

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import sys
import argparse
import glob
from datetime import datetime, timezone
from pathlib import Path

_L2_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_L2_DIR))

from l2_runner import load_all_v2_files, DOCS_DIR

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Default targets — states with zero recoverable model data after 3+ attempts
# IN and OR excluded here: they have model data and get one more reasoning pass first
DEFAULT_TARGETS = ["DC", "NM"]

ESCALATION_REASONS = {
    "DC": (
        "Persistent API failure across 3+ runs of both GPT and Gemini. "
        "No model data recoverable. Service statute(s) for D.C. pay-or-quit "
        "notices require attorney verification."
    ),
    "IN": (
        "Genuine model split after two tiebreaker passes: "
        "GPT identifies Ind. Code §32-31-1-9(b)(1); "
        "Gemini identifies Ind. Code §32-31-1-9(a). "
        "Both models high-confidence. Adjacent subsections — real interpretive "
        "question about which subsection governs tenant service. "
        "Attorney review required to determine correct operative provision."
    ),
    "NM": (
        "Persistent API failure across 3+ runs of both GPT and Gemini. "
        "No model data recoverable. Service statute(s) for N.M. pay-or-quit "
        "notices require attorney verification."
    ),
}


def escalate_state(code: str, data: dict, path: str, reason: str):
    """Replace open L2-SERVICE flag with a clean L7-ESCALATED flag."""
    flags = data["validation"].get("flags", [])

    # Remove existing open L2-SERVICE flags for service.method_rules
    prior_code = None
    for fl in flags:
        if (fl.get("field") == "service.method_rules" and
                fl.get("disposition") == "open" and
                fl.get("code", "").startswith("L2-SERVICE")):
            prior_code = fl.get("code")
            break

    flags = [fl for fl in flags if not (
        fl.get("field") == "service.method_rules" and
        fl.get("disposition") == "open" and
        fl.get("code", "").startswith("L2-SERVICE")
    )]

    new_flag = {
        "layer": "L7",
        "code": "L7-SERVICE-ATTORNEY-REVIEW",
        "field": "service.method_rules",
        "disposition": "open",
        "escalation": "L7",
        "escalation_date": TODAY,
        "prior_l2_code": prior_code,
        "note": reason,
    }

    data["validation"]["flags"] = flags + [new_flag]
    data["validation"]["automated_layers"]["L2_consensus"] = "escalated-L7"

    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  {code}: L7-SERVICE-ATTORNEY-REVIEW written (prior: {prior_code})")


def run_escalation(target_codes: list):
    all_data, all_paths = load_all_v2_files()

    escalated = []
    for code in target_codes:
        if code not in all_data:
            print(f"  WARN: {code} not found — skipping")
            continue

        data = all_data[code]
        path = all_paths[code]
        state_name = data.get("jurisdiction", {}).get("state_name", code)
        reason = ESCALATION_REASONS.get(code,
            f"Service module L2 could not resolve — escalated to L7 attorney review.")

        escalate_state(code, data, path, reason)
        escalated.append((code, state_name))

    # Append to HUMAN_REVIEW_QUEUE.md
    if escalated:
        queue_path = str(DOCS_DIR / "HUMAN_REVIEW_QUEUE.md")
        try:
            with open(queue_path) as f:
                content = f.read()
        except FileNotFoundError:
            content = "# Human Review Queue\n\n## Service L7 Items\n"

        new_items = []
        for code, name in escalated:
            reason = ESCALATION_REASONS.get(code, "L7 escalation — attorney review required.")
            new_items.append(
                f"\n### {code} ({name}) — L7-SERVICE-ATTORNEY-REVIEW\n"
                f"- Date: {TODAY}\n"
                f"- Reason: {reason}\n"
                f"- Action needed: Identify correct service statute(s) for pay-or-quit notice\n"
            )

        if "## Service L7 Items" in content:
            content = content.replace("## Service L7 Items",
                                      "## Service L7 Items\n" + "".join(new_items), 1)
        else:
            content += "\n## Service L7 Items\n" + "".join(new_items)

        with open(queue_path, "w") as f:
            f.write(content)
        print(f"\n  Queue updated: {len(escalated)} items → HUMAN_REVIEW_QUEUE.md")

    print(f"\n{'='*50}")
    print(f"  L7 escalation complete: {len(escalated)} states")
    for code, name in escalated:
        print(f"  🔴 {code} ({name})")
    print(f"  No content edits. Nothing advanced past ACP.")
    print(f"{'='*50}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="L2 Service L7 Escalation")
    parser.add_argument("--states", default=",".join(DEFAULT_TARGETS),
                        help=f"Comma-separated state codes. Default: {','.join(DEFAULT_TARGETS)}")
    args = parser.parse_args()

    target = [s.strip().upper() for s in args.states.split(",") if s.strip()]
    print(f"\nCivil Justice as Code — L2 Service L7 Escalation")
    print(f"Run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"States: {target}")
    print()
    run_escalation(target_codes=target)
