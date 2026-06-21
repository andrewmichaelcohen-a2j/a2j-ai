#!/usr/bin/env python3
"""
GPT empty-response diagnostic — Civil Justice as Code
Run from Terminal: python3 rules/validation/l2/gpt_diagnostic.py

Purpose: isolate WHY GPT returns empty for substantive-defenses queries.
Two hypotheses:
  A) JSON output schema requirement too complex → GPT returns empty
  B) Query content / framing triggers filter → GPT returns empty for any form

If Probe 1 (plain text) returns content but Probe 3 (JSON) returns empty → Hypothesis A (fix: simplify output schema)
If Probe 1 (plain text) also returns empty → Hypothesis B (fix: reframe query)
If all probes return content → the original runner has a different issue (token budget, etc.)
"""
import os, json
from pathlib import Path

# Load .env from project root
env_path = Path(__file__).parent.parent.parent.parent / ".env"
if not env_path.exists():
    env_path = Path(__file__).parent.parent.parent / ".env"
try:
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"'))
except Exception as e:
    print(f"Warning: could not load .env from {env_path}: {e}")

from openai import OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = "gpt-5.5"

def probe(label, content, max_tokens=1000):
    print(f"\n{'='*60}")
    print(f"PROBE {label}")
    print(f"Query: {content[:120]}...")
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": content}],
            max_completion_tokens=max_tokens
        )
        raw = resp.choices[0].message.content
        if raw and raw.strip():
            print(f"✅ RESPONSE ({len(raw)} chars): {raw[:400]}")
        else:
            print(f"❌ EMPTY RESPONSE (raw={repr(raw)})")
        return raw
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

print("GPT Diagnostic — Civil Justice as Code")
print(f"Model: {MODEL}")
print("="*60)

# Probe 1: Plain text, simple legal question — no JSON
r1 = probe(
    "1-PLAIN-TEXT (no JSON requirement)",
    "In California, what are the elements of a retaliatory eviction defense under Civil Code § 1942.5? "
    "What is the presumption period (number of days)? Please answer in plain prose."
)

# Probe 2: Very short JSON — single field
r2 = probe(
    "2-SHORT-JSON (single field)",
    'California Civil Code § 1942.5(a) creates a rebuttable presumption period. How many days? '
    'Respond ONLY with valid JSON: {"days": <integer>}'
)

# Probe 3: Original retaliation runner query format (as built)
r3 = probe(
    "3-ORIGINAL-FORMAT (retaliation_elements_runner.py query)",
    "In California, what are the elements of a retaliatory eviction defense, and what is the statutory "
    "presumption period (the time window after protected activity that creates a rebuttable presumption of "
    "retaliation), if any? Cite the specific statute and subsection. "
    "Respond with JSON containing keys: elements (object with protected_activity, landlord_knowledge, "
    "adverse_action, causal_connection), primary_statute, primary_statute_subsection, "
    "presumption_period_days (integer or null), presumption_period_basis, has_anti_retaliation_statute, "
    "confidence (high/medium/low)."
)

# Probe 4: Original format with higher token limit
r4 = probe(
    "4-ORIGINAL-FORMAT-HIGH-TOKENS (max_tokens=6000)",
    "In California, what are the elements of a retaliatory eviction defense, and what is the statutory "
    "presumption period (the time window after protected activity that creates a rebuttable presumption of "
    "retaliation), if any? Cite the specific statute and subsection. "
    "Respond with JSON containing keys: elements (object with protected_activity, landlord_knowledge, "
    "adverse_action, causal_connection), primary_statute, primary_statute_subsection, "
    "presumption_period_days (integer or null), presumption_period_basis, has_anti_retaliation_statute, "
    "confidence (high/medium/low).",
    max_tokens=6000
)

# Probe 5: Non-legal framing (control — does GPT respond to any JSON query?)
r5 = probe(
    "5-CONTROL (non-legal JSON query)",
    'What is the capital of California and its population? Respond with JSON: {"capital": "<string>", "population": <number>}'
)

print("\n" + "="*60)
print("DIAGNOSTIC SUMMARY")
print("="*60)
results = {
    "1-PLAIN-TEXT": bool(r1 and r1.strip()),
    "2-SHORT-JSON": bool(r2 and r2.strip()),
    "3-ORIGINAL-FORMAT-2K-TOKENS": bool(r3 and r3.strip()),
    "4-ORIGINAL-FORMAT-6K-TOKENS": bool(r4 and r4.strip()),
    "5-CONTROL": bool(r5 and r5.strip()),
}
for label, responded in results.items():
    icon = "✅" if responded else "❌"
    print(f"  {icon} {label}: {'responded' if responded else 'EMPTY'}")

if results.get("5-CONTROL") and not results.get("1-PLAIN-TEXT"):
    print("\n→ HYPOTHESIS B: GPT filters on retaliation/legal defense content framing.")
    print("  Fix: rephrase query to avoid triggering filter.")
elif results.get("1-PLAIN-TEXT") and not results.get("3-ORIGINAL-FORMAT-2K-TOKENS"):
    if results.get("4-ORIGINAL-FORMAT-6K-TOKENS"):
        print("\n→ HYPOTHESIS A (token budget): max_completion_tokens=2000 too low.")
        print("  Fix: set max_completion_tokens=6000 in runner.")
    else:
        print("\n→ HYPOTHESIS A (JSON schema complexity): GPT returns empty only for structured JSON output.")
        print("  Fix: simplify output schema or use two-pass (plain text → parse).")
elif all(results.values()):
    print("\n→ All probes responded. GPT is working now. Runner may have had transient issue.")
    print("  Next: run full 51-state retaliation elements run.")
else:
    print("\n→ Mixed/unclear — review individual probe outputs above.")

print("\nShare this output with Cowork for diagnosis and fix.")
