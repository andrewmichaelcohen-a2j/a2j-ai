#!/usr/bin/env python3
"""
NJ failure_to_attach Persistent ERROR Probe (2026-06-26)
=========================================================
NJ has errored (both models empty) on 3 consecutive failure_to_attach runs.
This probe isolates the issue with 3 increasingly simple queries to determine
whether the problem is:
  (a) Query complexity — NJ's eviction system is highly complex (Anti-Eviction Act)
      and the models may not respond to the standard procedural-defect query
  (b) True NSR — NJ has no separate pleading rule for attaching lease/notice,
      but the models don't surface "no rule" cleanly for NJ
  (c) API/network issue — transient but persistent for NJ specifically

Three probes (simplest to most specific):
  P1: Ultra-simple — just ask if NJ requires attaching lease to complaint
  P2: Statute-direct — ask about NJ court rules for UD complaints
  P3: Alternative framing — ask what happens if landlord doesn't attach lease

If P1/P2/P3 all return empty → likely NJ-specific model limitation
If any returns content → that content informs NSR determination

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import sys
import time
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv not installed.")
    sys.exit(1)

load_dotenv(_REPO_ROOT / ".env")

sys.path.insert(0, str(Path(__file__).parent))
from l2_runner import call_openai, call_gemini

PROBES = [
    {
        "id": "P1",
        "label": "Ultra-simple: does NJ require attaching lease/notice to eviction complaint?",
        "query": (
            "In New Jersey eviction (summary dispossess) proceedings, is a landlord "
            "required to attach a copy of the lease and/or the notice to quit to the "
            "eviction complaint filed with the court?\n\n"
            "Answer YES or NO, identify any specific court rule or statute, and note if "
            "there is no such specific requirement.\n\n"
            "Respond in JSON: {\"required\": <true or false or null>, "
            "\"statute_or_rule\": \"<citation or 'no specific rule'>\", "
            "\"rationale\": \"<1-2 sentences>\"}"
        ),
    },
    {
        "id": "P2",
        "label": "Rule-direct: NJ court rules for landlord-tenant complaint contents",
        "query": (
            "Under New Jersey Court Rules (specifically the rules governing Special Civil "
            "Part proceedings and landlord-tenant matters), what documents must a landlord "
            "include with or attach to a complaint for possession (summary dispossess) "
            "filed for nonpayment of rent?\n\n"
            "Is there a specific rule requiring attachment of the lease agreement and/or "
            "the rent demand notice? Cite the specific NJ Court Rule (R.) if applicable.\n\n"
            "Respond in JSON: {\"must_attach_lease\": <true or false>, "
            "\"must_attach_notice\": <true or false>, "
            "\"governing_rule\": \"<NJ Court Rule citation or 'no specific rule'>\", "
            "\"rationale\": \"<2 sentences>\"}"
        ),
    },
    {
        "id": "P3",
        "label": "Consequence-framing: what happens if NJ landlord doesn't attach lease?",
        "query": (
            "In New Jersey landlord-tenant court (Special Civil Part), if a landlord "
            "files a complaint for possession for nonpayment of rent WITHOUT attaching "
            "a copy of the lease or the rent demand notice, what happens?\n\n"
            "Specifically: (a) Is there a court rule requiring these attachments? "
            "(b) Can the tenant raise failure to attach as a procedural defect defense? "
            "(c) Does NJ distinguish between attaching the lease vs. the notice to quit?\n\n"
            "Respond in JSON: {\"attachment_required_by_rule\": <true or false or null>, "
            "\"valid_defense_if_omitted\": <true or false or null>, "
            "\"governing_authority\": \"<citation or 'primarily case law' or 'no specific rule'>\", "
            "\"rationale\": \"<2-3 sentences>\"}"
        ),
    },
]


def main():
    print("\n" + "="*65)
    print("NJ failure_to_attach PROBE — persistent ERROR investigation")
    print("="*65 + "\n")

    results = []
    for i, probe in enumerate(PROBES):
        print(f"[{probe['id']}] {probe['label']}")
        if i > 0:
            print("  (sleeping 15s...)")
            time.sleep(15)

        gpt = call_openai(probe["query"])
        gem = call_gemini(probe["query"])

        gpt_err = gpt.get("error")
        gem_err = gem.get("error")

        print(f"  GPT:    {'ERROR: ' + str(gpt_err)[:60] if gpt_err else json.dumps({k: v for k, v in gpt.items() if k not in ('_raw', 'model')})[:120]}")
        print(f"  Gemini: {'ERROR: ' + str(gem_err)[:60] if gem_err else json.dumps({k: v for k, v in gem.items() if k not in ('_raw', 'model')})[:120]}")
        print()

        results.append({
            "probe_id": probe["id"],
            "label": probe["label"],
            "gpt": {k: v for k, v in gpt.items() if k != "_raw"},
            "gemini": {k: v for k, v in gem.items() if k != "_raw"},
        })
        time.sleep(5)

    # Diagnosis
    print("="*65)
    print("DIAGNOSIS")
    print("="*65)
    any_content = False
    for r in results:
        gpt_ok = not r["gpt"].get("error") and r["gpt"].get("statute_or_rule") or r["gpt"].get("governing_authority") or r["gpt"].get("governing_rule")
        gem_ok = not r["gemini"].get("error") and r["gemini"].get("statute_or_rule") or r["gemini"].get("governing_authority") or r["gemini"].get("governing_rule")
        if gpt_ok or gem_ok:
            any_content = True
            print(f"  [{r['probe_id']}] ✅ Got content — NJ query is answerable with different framing")
        else:
            print(f"  [{r['probe_id']}] ❌ Still empty — models not responding")

    if not any_content:
        print("\n  CONCLUSION: NJ failure_to_attach is a genuine model-limitation case.")
        print("  Both models persistently return empty for NJ in this context.")
        print("  Likely cause: NJ's Anti-Eviction Act complexity causes models to not")
        print("  return structured JSON for NJ-specific pleading rules.")
        print("  RECOMMENDATION: Classify as NSR-PRESUMED for NJ (no specific rule")
        print("  requiring attachment appears to be a separate procedural defect)")
        print("  and add a manual note citing R. 6:3-3(a) (NJ landlord-tenant complaint")
        print("  form requirements) for attorney verification.")
    else:
        print("\n  CONCLUSION: Query framing was the issue. Review content above.")
        print("  A reformulated query can resolve NJ's failure_to_attach classification.")

    # Output
    out_path = _REPO_ROOT / "rules" / "validation" / "l2" / "output" / "nj_attach_probe_20260626.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump({"probe": "NJ-failure_to_attach", "results": results}, f, indent=2)
    print(f"\n  Output: {out_path}")
    print("="*65 + "\n")


if __name__ == "__main__":
    main()
