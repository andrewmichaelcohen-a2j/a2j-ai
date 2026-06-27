#!/usr/bin/env python3
"""
Golden Set Scorer — Direction B, CJaC
Copyright 2026 Andrew M Cohen. Apache 2.0.

Runs frozen (or draft) golden-set fact patterns end-to-end through the pipeline
(rules file + model reasoning) and scores the output against attorney-established
correct answers.

Usage:
    python3 golden_set_scorer.py --golden GOLDEN_SET.json --rules CA --module notice
    python3 golden_set_scorer.py --golden FROZEN/CA_notice_v1.json --rules CA --module notice --held-out

Scoring hierarchy:
  - bright_line: deterministic statutory rules (expect ≥90%)
  - open_textured: interpretive / multi-factor (expect lower; scored separately)
  - Never blend the two into a single number.

Output:
  - Console: per-case result + summary table by difficulty band
  - JSON: rules/validation/scorer/output/score_<run_id>.json
"""

import os, sys, json, hashlib, argparse, time, datetime
from pathlib import Path

# ──────────────────────────────────────────────────────────
# Path resolution
# ──────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "rules" / "validation" / "l2"))
from l2_runner import call_openai, call_gemini  # reuse existing model callers

RULES_DIR = REPO_ROOT / "rules" / "eviction"
GOLDEN_DIR = REPO_ROOT / "rules" / "validation" / "golden_sets"
OUTPUT_DIR = REPO_ROOT / "rules" / "validation" / "scorer" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STATE_ABBR_TO_NAME = {
    "CA": "california", "TX": "texas", "NY": "new-york", "FL": "florida",
    "WA": "washington", "OR": "oregon", "CO": "colorado", "MN": "minnesota",
    "NJ": "new-jersey", "IL": "illinois", "AZ": "arizona", "GA": "georgia",
    "NC": "north-carolina", "VA": "virginia", "MA": "massachusetts",
    "MI": "michigan", "OH": "ohio", "PA": "pennsylvania", "WI": "wisconsin",
    "TN": "tennessee", "MO": "missouri", "MD": "maryland", "CT": "connecticut",
    "AL": "alabama", "AK": "alaska", "AR": "arkansas", "DE": "delaware",
    "HI": "hawaii", "ID": "idaho", "IN": "indiana", "IA": "iowa",
    "KS": "kansas", "KY": "kentucky", "LA": "louisiana", "ME": "maine",
    "MS": "mississippi", "MT": "montana", "NE": "nebraska", "NV": "nevada",
    "NH": "new-hampshire", "NM": "new-mexico", "ND": "north-dakota",
    "OK": "oklahoma", "RI": "rhode-island", "SC": "south-carolina",
    "SD": "south-dakota", "UT": "utah", "VT": "vermont", "WV": "west-virginia",
    "WY": "wyoming", "DC": "district-of-columbia",
}

# ──────────────────────────────────────────────────────────
# Integrity check
# ──────────────────────────────────────────────────────────

def content_hash(candidate: dict) -> str:
    """SHA256 of the canonical fields. Matches freeze.py's hash computation."""
    canonical = {
        "id": candidate.get("id"),
        "facts": candidate.get("facts"),
        "question": candidate.get("question"),
        "correct_answer": candidate.get("correct_answer") or candidate.get("DRAFT_answer"),
        "authority": candidate.get("authority"),
    }
    serialized = json.dumps(canonical, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode()).hexdigest()


def verify_integrity(candidates: list) -> list[str]:
    """Verify content hashes for frozen candidates. Returns list of violation messages."""
    violations = []
    for c in candidates:
        stored_hash = c.get("_content_hash")
        if stored_hash is None:
            continue  # DRAFT candidate — no hash yet, skip
        computed = content_hash(c)
        if computed != stored_hash:
            violations.append(
                f"INTEGRITY FAILURE: {c.get('id')} — stored hash {stored_hash[:12]}… "
                f"≠ computed {computed[:12]}…"
            )
    return violations

# ──────────────────────────────────────────────────────────
# Rules file loader
# ──────────────────────────────────────────────────────────

def load_rules_module(state_abbr: str, module: str) -> dict:
    """Load just the relevant module section from the state's v2 rules file."""
    name = STATE_ABBR_TO_NAME.get(state_abbr.upper())
    if not name:
        raise ValueError(f"Unknown state abbreviation: {state_abbr}")
    pattern = RULES_DIR / name / f"{state_abbr.lower()}_eviction_v2.json"
    if not pattern.exists():
        raise FileNotFoundError(f"Rules file not found: {pattern}")
    data = json.loads(pattern.read_text())
    section = data.get(module)
    if section is None:
        raise KeyError(f"Module '{module}' not found in {state_abbr} rules file. "
                       f"Available: {list(data.keys())}")
    return section

# ──────────────────────────────────────────────────────────
# Pipeline query
# ──────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a deterministic legal rules engine. Your job is to apply the encoded
rules from a state eviction law file to a specific fact pattern and answer a legal question.

Rules:
1. Your answer MUST come from the rules file, not general knowledge.
2. Quote the specific rule or defect that controls the outcome.
3. Return ONLY valid JSON — no prose, no markdown.
4. If the rules file does not address the question, say so explicitly.

Return this exact JSON structure:
{
  "answer": "YES" or "NO" or "VALID" or "VOID" or "INSUFFICIENT" or "UNKNOWN",
  "answer_normalized": "YES" or "NO",
  "controlling_rule": "cite the exact field/defect/statute from the rules file",
  "reasoning": "one or two sentences explaining how the rule applies to these facts",
  "confidence": "HIGH" or "MEDIUM" or "LOW",
  "rules_file_addressed_question": true or false
}"""

def build_query(rules_section: dict, module: str, facts: str, question: str) -> str:
    rules_json = json.dumps(rules_section, indent=2)
    return (
        f"MODULE: {module}\n\n"
        f"RULES FILE (excerpt):\n{rules_json}\n\n"
        f"FACTS:\n{facts}\n\n"
        f"QUESTION:\n{question}\n\n"
        f"Apply the rules to these facts and return the JSON answer."
    )


def query_pipeline(rules_section: dict, module: str, facts: str, question: str,
                   use_gemini_verify: bool = True) -> dict:
    """
    Stage 1 (GPT generates): run the fact pattern through the rules file.
    Stage 2 (Gemini verifies): independent corroboration.
    Returns structured result dict.
    """
    query = build_query(rules_section, module, facts, question)

    gpt_raw = call_openai(query)
    gpt_answer = gpt_raw if isinstance(gpt_raw, dict) else {}
    gpt_error = gpt_raw.get("error") if isinstance(gpt_raw, dict) else str(gpt_raw)

    gemini_answer = {}
    if use_gemini_verify:
        gemini_raw = call_gemini(query)
        gemini_answer = gemini_raw if isinstance(gemini_raw, dict) else {}

    # Normalize: both models should agree on answer_normalized
    gpt_norm = (gpt_answer.get("answer_normalized") or
                _normalize_answer(gpt_answer.get("answer", ""))).upper()
    gemini_norm = (gemini_answer.get("answer_normalized") or
                   _normalize_answer(gemini_answer.get("answer", ""))).upper()

    if gpt_error or not gpt_norm:
        model_agreement = "GPT-ERROR"
    elif not gemini_norm:
        model_agreement = "GEMINI-EMPTY"
    elif gpt_norm == gemini_norm:
        model_agreement = "AGREE"
    else:
        model_agreement = "DISAGREE"

    # Primary answer: GPT if available, else Gemini
    primary_norm = gpt_norm or gemini_norm or "UNKNOWN"
    primary_reasoning = (gpt_answer.get("reasoning") or
                         gemini_answer.get("reasoning") or "")
    primary_rule = (gpt_answer.get("controlling_rule") or
                    gemini_answer.get("controlling_rule") or "")

    return {
        "pipeline_answer_normalized": primary_norm,
        "pipeline_reasoning": primary_reasoning,
        "pipeline_controlling_rule": primary_rule,
        "model_agreement": model_agreement,
        "gpt_answer": gpt_norm,
        "gemini_answer": gemini_norm,
        "gpt_confidence": gpt_answer.get("confidence"),
        "gemini_confidence": gemini_answer.get("confidence"),
        "gpt_addressed": gpt_answer.get("rules_file_addressed_question"),
        "gemini_addressed": gemini_answer.get("rules_file_addressed_question"),
    }


def _normalize_answer(raw: str) -> str:
    """Collapse YES/VALID/SUFFICIENT → YES; NO/VOID/INSUFFICIENT → NO."""
    if not raw:
        return ""
    r = str(raw).upper().strip()
    if any(x in r for x in ("YES", "VALID", "SUFFICIENT", "TRUE")):
        return "YES"
    if any(x in r for x in ("NO", "VOID", "INSUFFICIENT", "FALSE", "INVALID")):
        return "NO"
    return r  # UNKNOWN etc.

# ──────────────────────────────────────────────────────────
# Scoring
# ──────────────────────────────────────────────────────────

def score_case(candidate: dict, pipeline_result: dict, is_draft: bool = False) -> dict:
    """Compare pipeline output to correct_answer. Return per-case score record."""
    correct_raw = candidate.get("correct_answer") or candidate.get("DRAFT_answer", "")
    correct_norm = _normalize_answer(correct_raw).upper()
    pipeline_norm = pipeline_result.get("pipeline_answer_normalized", "UNKNOWN").upper()

    if correct_norm in ("YES", "NO") and pipeline_norm in ("YES", "NO"):
        is_correct = (correct_norm == pipeline_norm)
        score = 1 if is_correct else 0
    else:
        # UNKNOWN / unanswered
        is_correct = False
        score = 0

    return {
        "id": candidate.get("id"),
        "scenario": candidate.get("scenario", ""),
        "difficulty": candidate.get("difficulty", "bright_line"),
        "correct_answer": correct_raw,
        "correct_answer_normalized": correct_norm,
        "pipeline_answer": pipeline_norm,
        "model_agreement": pipeline_result.get("model_agreement"),
        "is_correct": is_correct,
        "score": score,
        "pipeline_reasoning": pipeline_result.get("pipeline_reasoning", ""),
        "pipeline_rule": pipeline_result.get("pipeline_controlling_rule", ""),
        "authority": candidate.get("authority", ""),
        "is_draft": is_draft,
        "frozen": candidate.get("_frozen", False),
    }

# ──────────────────────────────────────────────────────────
# Main runner
# ──────────────────────────────────────────────────────────

def run_scorer(golden_path: Path, state_abbr: str, module: str,
               held_out_only: bool = False, sleep_s: int = 5) -> dict:
    golden = json.loads(golden_path.read_text())
    candidates = golden.get("candidates", [])
    is_draft = golden.get("_status", "").startswith("DRAFT")

    # Filter to held-out only if requested
    if held_out_only:
        candidates = [c for c in candidates if c.get("_split") == "held-out"]
        if not candidates:
            print("⚠️  No held-out candidates found. Use without --held-out to score all.")
            return {}

    # Integrity check (frozen candidates only)
    if not is_draft:
        violations = verify_integrity(candidates)
        if violations:
            for v in violations:
                print(f"🚨 {v}")
            raise SystemExit("INTEGRITY CHECK FAILED — halting scorer. Do not proceed.")
        print(f"✅ Integrity check passed ({len([c for c in candidates if c.get('_content_hash')])} hashes verified)")

    # Load rules module
    rules_section = load_rules_module(state_abbr, module)
    print(f"📄 Rules loaded: {state_abbr} / {module}")
    print(f"📋 Candidates: {len(candidates)} {'(DRAFT — not ground truth)' if is_draft else '(FROZEN)'}")
    if held_out_only:
        print("🔒 HELD-OUT partition only")
    print()

    results = []
    for i, c in enumerate(candidates):
        cid = c.get("id", f"case-{i}")
        scenario = c.get("scenario", "")
        print(f"  [{i+1}/{len(candidates)}] {cid}: {scenario[:60]}...")

        pipeline_result = query_pipeline(
            rules_section=rules_section,
            module=module,
            facts=c.get("facts", ""),
            question=c.get("question", ""),
        )

        scored = score_case(c, pipeline_result, is_draft=is_draft)
        results.append(scored)
        status = "✅" if scored["is_correct"] else "❌"
        print(f"         {status} correct={scored['correct_answer_normalized']} "
              f"pipeline={scored['pipeline_answer']} "
              f"agreement={scored['model_agreement']}")

        if sleep_s > 0 and i < len(candidates) - 1:
            time.sleep(sleep_s)

    # Score by difficulty band (never blend)
    return _summarize(results, state_abbr, module, golden_path, is_draft, held_out_only)


def _summarize(results: list, state_abbr: str, module: str,
               golden_path: Path, is_draft: bool, held_out_only: bool) -> dict:
    bands = {}
    for r in results:
        band = r.get("difficulty", "bright_line")
        bands.setdefault(band, []).append(r)

    print("\n" + "═" * 60)
    print(f"SCORE REPORT — {state_abbr} / {module}")
    print(f"{'(DRAFT — not ground truth)' if is_draft else '(FROZEN)'}"
          + (" | HELD-OUT" if held_out_only else ""))
    print("═" * 60)

    band_summaries = {}
    for band, cases in sorted(bands.items()):
        n = len(cases)
        correct = sum(c["score"] for c in cases)
        pct = 100 * correct / n if n else 0
        disagree = sum(1 for c in cases if c["model_agreement"] == "DISAGREE")
        errors = sum(1 for c in cases if c["model_agreement"] in ("GPT-ERROR", "GEMINI-EMPTY"))
        print(f"\n  {band.upper()}")
        print(f"    Score:     {correct}/{n} = {pct:.1f}%")
        print(f"    Disagreed: {disagree} (model split → treat as uncertain)")
        print(f"    Errors:    {errors} (pipeline failure → investigate)")
        for r in cases:
            mark = "✅" if r["is_correct"] else "❌"
            print(f"    {mark} {r['id']}: {r['scenario'][:55]}")
            if not r["is_correct"]:
                print(f"         correct={r['correct_answer_normalized']} "
                      f"pipeline={r['pipeline_answer']} "
                      f"rule='{r['pipeline_rule'][:80]}'")
        band_summaries[band] = {"n": n, "correct": correct, "pct": pct,
                                 "model_disagree": disagree, "errors": errors}

    print(f"\n{'─'*60}")
    if is_draft:
        print("⚠️  DRAFT RUN — answers are DRAFT/UNFROZEN. Results are indicative only.")
        print("   Do NOT publish or present this score as validated ground truth.")
        print("   Freeze golden set (Andy signs off) before treating as real metric.")
    else:
        held_note = " (held-out partition)" if held_out_only else ""
        print(f"FROZEN score{held_note} — this is a real metric against attorney-established truth.")
        if held_out_only:
            print("HOLD THIS NUMBER until ready to publish — the held-out set is now burned.")

    run_id = f"score_{state_abbr}_{module}_{datetime.date.today().isoformat()}"
    output = {
        "run_id": run_id,
        "run_date": datetime.date.today().isoformat(),
        "golden_set": str(golden_path),
        "state": state_abbr,
        "module": module,
        "is_draft": is_draft,
        "held_out_only": held_out_only,
        "band_summaries": band_summaries,
        "results": results,
        "scorer_version": "v1.0",
        "attorney_line_note": (
            "A high score here raises confidence in machine-verified output. "
            "It does NOT promote anything across the attorney-validated line. "
            "Crossing that line still requires a named human."
        ),
    }
    out_path = OUTPUT_DIR / f"{run_id}.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\n📁 Output saved: {out_path.relative_to(REPO_ROOT)}")
    return output


# ──────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Score golden-set fact patterns against pipeline output")
    parser.add_argument("--golden", required=True,
                        help="Path to golden set JSON file (DRAFT or FROZEN)")
    parser.add_argument("--rules", required=True,
                        help="State abbreviation (e.g. CA, TX)")
    parser.add_argument("--module", required=True,
                        help="Rules module to load: notice, service, substantive_defenses, etc.")
    parser.add_argument("--held-out", action="store_true",
                        help="Score held-out partition only (sealed — burns the held-out set)")
    parser.add_argument("--sleep", type=int, default=3,
                        help="Seconds between API calls (default 3)")
    args = parser.parse_args()

    golden_path = Path(args.golden)
    if not golden_path.is_absolute():
        # Try relative to golden_sets dir, then repo root
        for base in (GOLDEN_DIR, REPO_ROOT):
            candidate = base / golden_path
            if candidate.exists():
                golden_path = candidate
                break

    if not golden_path.exists():
        print(f"❌ Golden set file not found: {args.golden}")
        sys.exit(1)

    run_scorer(
        golden_path=golden_path,
        state_abbr=args.rules.upper(),
        module=args.module,
        held_out_only=args.held_out,
        sleep_s=args.sleep,
    )


if __name__ == "__main__":
    main()
