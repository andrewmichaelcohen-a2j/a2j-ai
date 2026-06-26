#!/usr/bin/env python3
"""
Eviction Rules — L2 Multi-Model Consensus Runner
=================================================
Cross-checks each file's notice module pay_or_quit claim against two independent
model families (OpenAI GPT + Google Gemini). Classifies each state as:
  CONSENSUS-CONFIRM   — file, GPT, Gemini all agree on the period
  CITATION-DIVERGENCE — period agrees, but cited statute differs
  PERIOD-DIVERGENCE   — period itself differs (highest-priority human review)
  MODEL-SPLIT         — the two models disagree with each other
  ERROR               — API call failed

Models (verified June 2026):
  OpenAI:  gpt-5.5         (flagship, $5/$30 per 1M in/out; April 2026 release)
  Google:  gemini-2.5-pro  (stable flagship Pro; gemini-2.0-flash is SHUT DOWN)

GUARDRAILS (do not remove):
  - Keys read from .env at repo root; never hardcoded, logged, or committed
  - L2 never advances any file past AUTOMATED-CHECKS-PASSED
  - L2 never auto-edits content; divergences become flags for human review
  - Divergence is weighted as the stronger signal vs. agreement
  - Hard budget cap: $20

Usage:
  python l2_runner.py --states ME,OH,WV,MO,MS,ND,IL,SD   # Phase 1 pilot
  python l2_runner.py --states ALL                         # All states
  python l2_runner.py --dry-run --states ME,OH             # No API calls, no write-back

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import os
import re
import sys
import glob
import time
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple, List
from collections import Counter

# ── Key handling — load .env FIRST, before anything else ─────────────────────

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv not installed. Run: pip install python-dotenv --break-system-packages")
    sys.exit(1)

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_ENV_PATH = _REPO_ROOT / ".env"

if not _ENV_PATH.exists():
    print(
        "ERROR: .env not found at repo root.\n"
        f"Expected: {_ENV_PATH}\n"
        "Create it with:\n"
        "  OPENAI_API_KEY=sk-...\n"
        "  GOOGLE_API_KEY=...\n"
        "NEVER commit .env. Confirm .gitignore has it (line 20 ✓)."
    )
    sys.exit(1)

load_dotenv(_ENV_PATH)

OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")
GOOGLE_KEY = os.environ.get("GOOGLE_API_KEY", "")

if not OPENAI_KEY:
    print("ERROR: OPENAI_API_KEY not set in .env")
    sys.exit(1)
if not GOOGLE_KEY:
    print("ERROR: GOOGLE_API_KEY not set in .env")
    sys.exit(1)

# ── Configuration ─────────────────────────────────────────────────────────────

OPENAI_MODEL = "gpt-5.5"          # OpenAI flagship (API string confirmed April 2026; $5/$30 per 1M)
                                   # For maximum accuracy: also available as "gpt-5.5-pro" ($30/$180)
GEMINI_MODEL = "gemini-2.5-pro"   # Google flagship (stable; confirmed model code ai.google.dev/gemini-api/docs/models)
                                   # NOTE: gemini-2.0-flash is SHUT DOWN as of 2026-06; do not use
BUDGET_CAP_USD = 20.00
# Per-state cost estimate: gpt-5.5 (~500 in / 300 out) + gemini-2.5-pro (same scale)
# gpt-5.5: ~$0.0025 in + $0.009 out = ~$0.012; gemini-2.5-pro: ~$0.005; total ~$0.017/state
APPROX_COST_PER_STATE_USD = 0.02  # Conservative; 51 states ≈ $1.02 — well within $20 cap

RULES_EVICTION_DIR = _REPO_ROOT / "rules" / "eviction"
DOCS_DIR = _REPO_ROOT / "docs"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# ── Neutral query construction ────────────────────────────────────────────────

QUERY_TEMPLATE = (
    "Under {state_name} law, what is the statutory notice period a landlord must give "
    "a residential tenant for nonpayment of rent before filing an eviction action? "
    "If no notice period is required before filing, state that explicitly. "
    "Answer with: (1) the number of days required, or 'none' if no notice is required "
    "before filing; (2) the specific statute or code section that establishes this; "
    "(3) a one- to two-sentence rationale.\n\n"
    "Respond ONLY in valid JSON using this exact structure:\n"
    "{{\"days\": <integer or null>, \"notice_required\": <true or false>, "
    "\"statute\": \"<citation>\", \"rationale\": \"<1-2 sentences>\"}}"
)

SYSTEM_PROMPT = (
    "You are a legal research assistant specializing in US residential landlord-tenant law. "
    "Answer based on current statutory law only. Cite the specific statute section number. "
    "Do not include caveats about consulting an attorney. Respond only in the JSON format requested."
)


def build_query(state_name: str) -> str:
    return QUERY_TEMPLATE.format(state_name=state_name)


# ── OpenAI call ───────────────────────────────────────────────────────────────

def call_openai(query: str, dry_run: bool = False) -> dict:
    if dry_run:
        return {"days": 99, "notice_required": True, "statute": "DRY-RUN", "rationale": "dry run", "model": OPENAI_MODEL, "_raw": ""}

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
            max_completion_tokens=8000,  # gpt-5.5 reasoning model: chain-of-thought exhausted 2000 → 119/120 SM units empty. Raised to 8000 (ratified YELLOW 2026-06-25). Validation: attach re-run will measure before/after SM rate.
            timeout=60,  # 60s hard timeout — prevents infinite hang on slow API response
        )
        raw = resp.choices[0].message.content.strip()
        parsed = _parse_json_response(raw)
        parsed["model"] = OPENAI_MODEL
        parsed["_raw"] = raw
        return parsed
    except Exception as exc:
        return _error_result(str(exc), OPENAI_MODEL)


# ── Google Gemini call ────────────────────────────────────────────────────────

def call_gemini(query: str, dry_run: bool = False) -> dict:
    if dry_run:
        return {"days": 99, "notice_required": True, "statute": "DRY-RUN", "rationale": "dry run", "model": GEMINI_MODEL, "_raw": ""}

    try:
        from google import genai  # google-genai SDK (not deprecated google-generativeai)
    except ImportError:
        return _error_result("google-genai package not installed. Run: pip install google-genai", GEMINI_MODEL)

    try:
        import concurrent.futures
        client = genai.Client(api_key=GOOGLE_KEY)
        full_prompt = SYSTEM_PROMPT + "\n\n" + query

        def _do_gemini():
            return client.models.generate_content(model=GEMINI_MODEL, contents=full_prompt)

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            fut = pool.submit(_do_gemini)
            try:
                resp = fut.result(timeout=60)  # 60s hard timeout — SDK-agnostic
            except concurrent.futures.TimeoutError:
                return _error_result("Gemini API timed out after 60s", GEMINI_MODEL)

        raw = resp.text.strip()
        parsed = _parse_json_response(raw)
        parsed["model"] = GEMINI_MODEL
        parsed["_raw"] = raw
        return parsed
    except Exception as exc:
        return _error_result(str(exc), GEMINI_MODEL)


# ── Response parsing ──────────────────────────────────────────────────────────

def _parse_json_response(raw: str) -> dict:
    """Extract JSON from model response (may be wrapped in markdown fences)."""
    # Strip markdown fences
    text = re.sub(r"```(?:json)?", "", raw).strip()
    # Find outermost {...}
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    # Last-ditch attempt on the full stripped text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"days": None, "notice_required": None, "statute": None, "rationale": f"PARSE_ERROR: {raw[:200]}"}


def _error_result(msg: str, model: str) -> dict:
    return {"error": msg, "days": None, "notice_required": None, "statute": None, "rationale": None, "model": model, "_raw": ""}


# ── File loading ──────────────────────────────────────────────────────────────

def load_all_v2_files() -> Tuple[dict, dict]:
    """Returns (data_by_state, path_by_state)."""
    data_by_state = {}
    path_by_state = {}
    for state_dir in sorted(RULES_EVICTION_DIR.glob("*")):
        if not state_dir.is_dir():
            continue
        for jf in state_dir.glob("*_eviction_v2.json"):
            try:
                with open(jf) as f:
                    data = json.load(f)
            except (json.JSONDecodeError, IOError) as exc:
                print(f"  WARN: could not parse {jf.name}: {exc}")
                continue
            code = data.get("jurisdiction", {}).get("state", "??")
            data_by_state[code] = data
            path_by_state[code] = str(jf)
    return data_by_state, path_by_state


def extract_file_claim(data: dict) -> dict:
    """Extract the file's pay_or_quit notice claim."""
    pq = data.get("notice", {}).get("notice_types", {}).get("pay_or_quit", {})
    notice_required = pq.get("notice_required", True)  # default: required unless stated otherwise

    days = None
    statute = None
    for sub in ("tenancy_all", "tenancy_under_1yr", "tenancy_any"):
        if sub in pq and isinstance(pq[sub], dict):
            days = pq[sub].get("days")
            statute = pq[sub].get("statute")
            break

    # Check for L1-MACHINE-ASSIST flags
    flags = data.get("validation", {}).get("flags", [])
    has_machine_assist = any(
        fl.get("layer") == "L1" and "MACHINE-ASSIST" in fl.get("code", "")
        for fl in flags
    )

    return {
        "days": days,
        "notice_required": notice_required,
        "statute": statute,
        "has_machine_assist_flag": has_machine_assist,
    }


# ── Classification ────────────────────────────────────────────────────────────

def _normalize_days(val) -> Optional[int]:
    """Normalize days to int or None (None = no notice required)."""
    if val is None:
        return None
    if isinstance(val, bool):
        return None
    if isinstance(val, int):
        return val if val > 0 else None  # 0 → treat as no notice
    if isinstance(val, str):
        low = val.lower().strip()
        if low in ("none", "null", "no notice", "no notice required", "0", ""):
            return None
        try:
            v = int(low)
            return v if v > 0 else None
        except ValueError:
            return None
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


def _extract_section_nums(citation: str) -> set[str]:
    """
    Extract specific section identifiers for citation comparison.
    Focuses on the section number after § (most reliable) or after a /
    in ILCS-style citations. Ignores leading chapter/title numbers to
    avoid false matches on shared prefixes (e.g., '14' in '14 MRS §6001').
    """
    if not citation:
        return set()
    # Priority 1: numbers after § symbol (handles most US citation formats)
    after_section = re.findall(r"§\s*([\w.:\-]+)", citation)
    if after_section:
        return set(s.lower().strip() for s in after_section)
    # Priority 2: slash-style citations (e.g. 735 ILCS 5/9-209 → '9-209')
    slash_parts = re.findall(r"/(\d+[\w.\-]*)", citation)
    if slash_parts:
        return set(p.lower() for p in slash_parts)
    # Fallback: no structured marker found; skip citation comparison
    return set()


def classify(file_claim: dict, gpt: dict, gemini: dict) -> str:
    if gpt.get("error") or gemini.get("error"):
        return "ERROR"

    file_days = _normalize_days(file_claim.get("days"))
    gpt_days = _normalize_days(gpt.get("days"))
    gem_days = _normalize_days(gemini.get("days"))

    # Step 1: Do the two models agree with each other?
    if gpt_days != gem_days:
        return "MODEL-SPLIT"

    # Models agree on period — does the file agree?
    if file_days != gpt_days:
        return "PERIOD-DIVERGENCE"

    # Periods all agree — check citation overlap
    file_secs = _extract_section_nums(file_claim.get("statute") or "")
    gpt_secs = _extract_section_nums(gpt.get("statute") or "")
    gem_secs = _extract_section_nums(gemini.get("statute") or "")

    # If both models cite sections that don't overlap with file's citation at all
    # AND the file has a citation to check, flag citation divergence
    if file_secs and gpt_secs and gem_secs:
        # Models agree with each other on citation
        models_share_section = bool(gpt_secs & gem_secs)
        models_match_file = bool((gpt_secs | gem_secs) & file_secs)
        if models_share_section and not models_match_file:
            return "CITATION-DIVERGENCE"

    return "CONSENSUS-CONFIRM"


# ── Write-back ────────────────────────────────────────────────────────────────

def write_back(file_path: str, data: dict, classification: str, gpt: dict, gemini: dict):
    """Write L2 results into validation block. NEVER advances module_status."""
    val = data.setdefault("validation", {})
    al = val.setdefault("automated_layers", {})
    flags = val.setdefault("flags", [])

    # Set L2_consensus layer result
    if classification == "CONSENSUS-CONFIRM":
        al["L2_consensus"] = "pass"
    elif classification == "ERROR":
        al["L2_consensus"] = "warning"
    else:
        al["L2_consensus"] = "flagged"

    # Store full L2 result block (non-schema-breaking extra field)
    val["l2_results"] = {
        "run_date": TODAY,
        "classification": classification,
        "gpt": {
            "model": gpt.get("model"),
            "days": gpt.get("days"),
            "statute": gpt.get("statute"),
            "rationale": gpt.get("rationale"),
        },
        "gemini": {
            "model": gemini.get("model"),
            "days": gemini.get("days"),
            "statute": gemini.get("statute"),
            "rationale": gemini.get("rationale"),
        },
    }

    # Add divergence flag (open, requires human review)
    if classification not in ("CONSENSUS-CONFIRM", "ERROR"):
        new_flag = {
            "layer": "L2",
            "code": f"L2-{classification}",
            "field": "notice.notice_types.pay_or_quit",
            "disposition": "open",
            "note": (
                f"L2-{classification}: pay_or_quit nonpayment notice — divergence detected. "
                f"GPT ({gpt.get('model')}): {gpt.get('days')}d | {gpt.get('statute')}. "
                f"Gemini ({gemini.get('model')}): {gemini.get('days')}d | {gemini.get('statute')}. "
                f"Human review required."
            ),
            "gpt_answer": {
                "days": gpt.get("days"),
                "statute": gpt.get("statute"),
                "rationale": gpt.get("rationale"),
            },
            "gemini_answer": {
                "days": gemini.get("days"),
                "statute": gemini.get("statute"),
                "rationale": gemini.get("rationale"),
            },
            "l2_run_date": TODAY,
        }
        flags.append(new_flag)

    # Persist — file_status stays at its current value (never auto-advanced)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── Report generation ─────────────────────────────────────────────────────────

def write_report(results: list[dict], phase_label: str, report_path: str):
    from collections import Counter
    counts = Counter(r["classification"] for r in results)

    lines = [
        f"# L2 Multi-Model Consensus Report — {phase_label}",
        "",
        f"**Run date:** {TODAY}",
        f"**Models:** OpenAI `{OPENAI_MODEL}` · Google `{GEMINI_MODEL}`",
        f"**Target:** Notice module — `pay_or_quit` nonpayment notice period and statutory citation",
        f"**States run:** {len(results)}",
        "",
        "> **Interpretation caveat:** Model consensus partly reflects shared secondary sources,",
        "> so agreement is corroborating-but-not-independent. **Divergence is the stronger",
        "> signal** — where the file and the two models disagree, that is where a human should",
        "> look. Do not treat unanimous agreement as proof of correctness.",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Classification | Count |",
        "|---------------|-------|",
        f"| ✅ CONSENSUS-CONFIRM | {counts.get('CONSENSUS-CONFIRM', 0)} |",
        f"| ⚠️ CITATION-DIVERGENCE | {counts.get('CITATION-DIVERGENCE', 0)} |",
        f"| 🔴 PERIOD-DIVERGENCE | {counts.get('PERIOD-DIVERGENCE', 0)} |",
        f"| ⚠️ MODEL-SPLIT | {counts.get('MODEL-SPLIT', 0)} |",
        f"| ❌ ERROR | {counts.get('ERROR', 0)} |",
        "",
        "---",
        "",
        "## Per-State Results",
        "",
        "| State | MA flag | File days | File statute | GPT days | GPT statute | Gemini days | Gemini statute | Result |",
        "|-------|---------|-----------|-------------|---------|------------|------------|---------------|--------|",
    ]

    for r in results:
        c = r["classification"]
        icon = {"CONSENSUS-CONFIRM": "✅", "CITATION-DIVERGENCE": "⚠️", "PERIOD-DIVERGENCE": "🔴", "MODEL-SPLIT": "⚠️", "ERROR": "❌"}.get(c, c)
        ma = "L1-MA" if r["file_claim"].get("has_machine_assist_flag") else ""
        fd = str(r["file_claim"]["days"]) if r["file_claim"]["days"] is not None else "none"
        fs = (r["file_claim"].get("statute") or "")[:45]
        gd = str(r["gpt"].get("days")) if r["gpt"].get("days") is not None else "none"
        gs = (r["gpt"].get("statute") or "ERR")[:45]
        md = str(r["gemini"].get("days")) if r["gemini"].get("days") is not None else "none"
        ms = (r["gemini"].get("statute") or "ERR")[:45]
        lines.append(f"| {r['state']} | {ma} | {fd} | {fs} | {gd} | {gs} | {md} | {ms} | {icon} {c} |")

    lines += [
        "",
        "---",
        "",
        "## Divergence Details",
        "",
    ]

    divergences = [r for r in results if r["classification"] not in ("CONSENSUS-CONFIRM", "ERROR")]
    if not divergences:
        lines.append("No divergences detected in this phase.")
    else:
        for r in divergences:
            c = r["classification"]
            icon = "⚠️" if c != "PERIOD-DIVERGENCE" else "🔴"
            lines += [
                f"### {r['state']} ({r['state_name']}) — {icon} {c}",
                "",
                f"- **File:** `{r['file_claim']['days']}d` · `{r['file_claim'].get('statute', 'unknown')}`",
                f"- **GPT ({OPENAI_MODEL}):** `{r['gpt'].get('days')}d` · `{r['gpt'].get('statute')}` — {r['gpt'].get('rationale', '')}",
                f"- **Gemini ({GEMINI_MODEL}):** `{r['gemini'].get('days')}d` · `{r['gemini'].get('statute')}` — {r['gemini'].get('rationale', '')}",
                f"- **Action required:** Flag written to `validation.flags` in the state file. Human review needed.",
                "",
            ]

    if counts.get("ERROR", 0) > 0:
        lines += ["## API Errors", ""]
        for r in results:
            if r["classification"] == "ERROR":
                lines += [
                    f"### {r['state']} — ERROR",
                    f"- GPT: {r['gpt'].get('error', 'ok')}",
                    f"- Gemini: {r['gemini'].get('error', 'ok')}",
                    "",
                ]

    lines += [
        "---",
        "",
        "*L2 corroborates and flags. It never blesses and never auto-edits content.*",
        "*All divergences require human review (L7 attorney or Andy triage).*",
        "*No file was advanced past AUTOMATED-CHECKS-PASSED by this run.*",
        "",
        f"*Copyright 2026 Andrew M Cohen. Apache 2.0.*",
    ]

    with open(report_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Report → {os.path.basename(report_path)}")


# ── Main runner ───────────────────────────────────────────────────────────────

def run_l2(
    target_codes: list[str],
    phase_label: str,
    dry_run: bool = False,
    no_writeback: bool = False,
    sleep_secs: float = 0,
) -> list[dict]:
    all_data, all_paths = load_all_v2_files()

    # Validate requested states
    missing = [c for c in target_codes if c not in all_data]
    if missing:
        print(f"  WARN: these state codes not found in library: {missing}")
        target_codes = [c for c in target_codes if c in all_data]

    if not target_codes:
        print("  ERROR: no valid states to run.")
        sys.exit(1)

    # Budget pre-check
    est = len(target_codes) * APPROX_COST_PER_STATE_USD
    print(f"\n  States: {len(target_codes)} · Est. cost: ~${est:.2f} · Hard cap: ${BUDGET_CAP_USD:.2f}")
    if est > BUDGET_CAP_USD:
        print(f"  ERROR: estimated cost ${est:.2f} exceeds budget cap ${BUDGET_CAP_USD:.2f}. Aborting.")
        sys.exit(1)
    if dry_run:
        print("  MODE: DRY RUN — no API calls, no write-back")

    results = []
    spend_approx = 0.0

    for code in target_codes:
        data = all_data[code]
        state_name = data.get("jurisdiction", {}).get("state_name", code)
        file_claim = extract_file_claim(data)
        query = build_query(state_name)

        print(f"  {code} ({state_name})...", end=" ", flush=True)

        gpt_result = call_openai(query, dry_run=dry_run)
        gemini_result = call_gemini(query, dry_run=dry_run)

        if gpt_result.get("error"):
            print(f"\n    GPT ERROR: {gpt_result['error'][:80]}")
        if gemini_result.get("error"):
            print(f"\n    Gemini ERROR: {gemini_result['error'][:80]}")

        classification = classify(file_claim, gpt_result, gemini_result)
        spend_approx += APPROX_COST_PER_STATE_USD

        fd = file_claim["days"]
        gd = gpt_result.get("days")
        md = gemini_result.get("days")
        print(f"→ {classification}  (file:{fd}d | gpt:{gd}d | gem:{md}d)")

        if spend_approx > BUDGET_CAP_USD:
            print(f"\n  BUDGET CAP HIT (~${spend_approx:.2f}). Stopping.")
            break

        if not dry_run and not no_writeback:
            write_back(all_paths[code], data, classification, gpt_result, gemini_result)

        results.append({
            "state": code,
            "state_name": state_name,
            "file_claim": file_claim,
            "gpt": gpt_result,
            "gemini": gemini_result,
            "classification": classification,
        })

        if sleep_secs > 0 and code != target_codes[-1]:
            time.sleep(sleep_secs)

    # Save raw output file (provenance record per COWORK_DIRECTION_PROVENANCE.md)
    if not dry_run:
        OUTPUT_DIR = Path(__file__).parent / "output"
        OUTPUT_DIR.mkdir(exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        raw_path = OUTPUT_DIR / f"notice_l2_raw_{ts}.json"
        raw_record = {
            "run_date": ts,
            "module": "notice.notice_types.pay_or_quit",
            "phase": phase_label,
            "models": {"gpt": OPENAI_MODEL, "gemini": GEMINI_MODEL},
            "states_run": len(results),
            "spend_estimate": round(spend_approx, 4),
            "counts": dict(Counter(r["classification"] for r in results)),
            "results": results,
        }
        with open(raw_path, "w") as f:
            json.dump(raw_record, f, indent=2, ensure_ascii=False)
        print(f"\n  Raw output saved: {raw_path}")

    # Write report
    DOCS_DIR.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    report_path = str(DOCS_DIR / f"L2_CONSENSUS_REPORT_{ts}.md")
    if not dry_run:
        write_report(results, phase_label, report_path)
    else:
        print(f"  (dry run — report not written)")

    # Final summary
    from collections import Counter
    counts = Counter(r["classification"] for r in results)
    print(f"\n  ─── {phase_label} summary ───")
    print(f"  {len(results)} states processed | ~${spend_approx:.3f} spent")
    print(f"  ✅ CONFIRM: {counts.get('CONSENSUS-CONFIRM',0)}  "
          f"⚠️ CITATION-DIV: {counts.get('CITATION-DIVERGENCE',0)}  "
          f"🔴 PERIOD-DIV: {counts.get('PERIOD-DIVERGENCE',0)}  "
          f"⚠️ MODEL-SPLIT: {counts.get('MODEL-SPLIT',0)}  "
          f"❌ ERROR: {counts.get('ERROR',0)}")

    return results


# ── CLI entry point ───────────────────────────────────────────────────────────

PHASE1_STATES = ["ME", "OH", "WV", "MO", "MS", "ND", "IL", "SD"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="L2 Multi-Model Consensus Runner — Civil Justice as Code"
    )
    parser.add_argument(
        "--states",
        default=",".join(PHASE1_STATES),
        help=(
            f"Comma-separated state codes. Default: Phase 1 flag states ({','.join(PHASE1_STATES)}). "
            "Use ALL for all 51 states."
        ),
    )
    parser.add_argument(
        "--phase",
        default="Phase 1 — Machine-Assist Flag States",
        help="Phase label for report header.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse files and print plan; skip API calls and write-back.",
    )
    parser.add_argument(
        "--no-writeback",
        action="store_true",
        help="Call APIs and classify, but do not write results back to files.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0,
        help="Seconds to sleep between states (rate-limit guard). Default: 0.",
    )
    args = parser.parse_args()

    print(f"\nCivil Justice as Code — L2 Multi-Model Consensus")
    print(f"Run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Models: {OPENAI_MODEL} + {GEMINI_MODEL}")
    print(f"Budget cap: ${BUDGET_CAP_USD:.2f}")

    if args.states.upper() == "ALL":
        all_data, _ = load_all_v2_files()
        target = sorted(all_data.keys())
        print(f"\nPhase: ALL states ({len(target)} found)")
        print("⚠️  This is Phase 2. Confirm Phase 1 results reviewed before proceeding.")
    else:
        target = [s.strip().upper() for s in args.states.split(",") if s.strip()]
        print(f"\nPhase: {args.phase}")
        print(f"States: {', '.join(target)}")

    run_l2(
        target_codes=target,
        phase_label=args.phase,
        dry_run=args.dry_run,
        no_writeback=args.no_writeback,
        sleep_secs=args.sleep,
    )
