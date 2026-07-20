#!/usr/bin/env python3
"""
CA Notice Scorer — Direction B, CJaC
Copyright 2026 Andrew M Cohen. Apache 2.0.

Reads attorney-frozen golden set from Excel (goldenset.xlsx format),
applies the encoded CA-notice rules via a dual-model pipeline, and reports
held-out vs. non-held-out accuracy as separate numbers.

Usage:
    # Dry run (no API calls — validates schema, shows queries, mocks predictions)
    python3 ca_notice_scorer.py --golden PATH/TO/goldenset.xlsx --dry-run

    # Score all frozen items (calls GPT + Gemini)
    python3 ca_notice_scorer.py --golden PATH/TO/goldenset.xlsx

    # Held-out partition only (burns the held-out set — do this once, at publication)
    python3 ca_notice_scorer.py --golden PATH/TO/goldenset.xlsx --held-out-only

    # Non-held-out only (safe to iterate on — tuning partition)
    python3 ca_notice_scorer.py --golden PATH/TO/goldenset.xlsx --non-held-out-only

Hard integrity constraints (non-negotiable):
  1. Immutability: read-only on frozen set. Fails loudly on parse error; never silently skips.
  2. Held-out isolation: held-out score computed + reported separately. No auto-tuning wiring.
  3. No answer leakage: model sees only facts + encoded rules. Never sees correct outcome.
  4. Determinism: SHA256 of Excel file + rules file hash logged with every run.
  5. YELLOW surface: any schema/enum mismatch surfaces as YELLOW and halts or flags — never guesses.
"""

import os
import re
import sys
import json
import time
import hashlib
import argparse
import datetime
import concurrent.futures
from pathlib import Path

try:
    import openpyxl
except ImportError:
    sys.exit("❌ openpyxl not installed. Run: pip install openpyxl --break-system-packages")

try:
    from dotenv import load_dotenv
    _env_path = Path(__file__).resolve().parents[3] / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)
except ImportError:
    pass

# ── Constants ─────────────────────────────────────────────────────────────────

REPO_ROOT  = Path(__file__).resolve().parents[3]
RULES_DIR  = REPO_ROOT / "rules" / "eviction"
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Excel column names — exactly as they appear in the sheet header row.
# YELLOW if any are missing.
EXPECTED_COLUMNS = [
    "ID",
    "Module",
    "Jurisdiction",
    "Facts (scenario)",
    "Drafted outcome",
    "Controlling authority",
    "ATTORNEY VERDICT",
    "Correct outcome (if corrected)",
    "Reason / note (required if corrected)",
    "Status",
    "Held-out (TRUE/FALSE)",
    "Reviewed by",
    "Date",
]

# Canonical outcome enum. YELLOW if a frozen item's correct outcome is outside this set.
KNOWN_OUTCOMES = frozenset({
    "NOTICE_VALID",
    "NOTICE_INVALID",
    "UD_DEFECTIVE_PREMATURE",
    "UD_NOT_SUSTAINABLE",
})

# Status values
FROZEN   = "FROZEN"
EXCLUDED = "EXCLUDED"
DRAFT    = "DRAFT"

# Held-out field values
HELD_OUT_TRUE  = "TRUE"
HELD_OUT_FALSE = "FALSE"
HELD_OUT_NA    = "N/A"

# Model identifiers (mirror l2_runner.py)
OPENAI_MODEL = "gpt-5.5"
GEMINI_MODEL = "gemini-2.5-pro"

OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")
GOOGLE_KEY = os.environ.get("GOOGLE_API_KEY", "")

# ── System prompt ─────────────────────────────────────────────────────────────
# Rules: model sees ONLY facts + encoded rules. Correct outcome never included.

SCORER_SYSTEM_PROMPT = """\
You are a deterministic legal rules engine for California residential eviction law.

You will receive:
  1. A JSON excerpt of the encoded CA-notice rules from the official state rules file.
  2. A specific tenant scenario (facts).

Your task: Apply ONLY the encoded rules to the facts. Do not use general legal knowledge.

Valid outcomes — return EXACTLY ONE:
  NOTICE_VALID          — the notice is facially valid under the encoded rules
  NOTICE_INVALID        — the notice has a defect (void or invalid) per the encoded rules
  UD_DEFECTIVE_PREMATURE — a UD action was (or would be) filed before notice properly expired
  UD_NOT_SUSTAINABLE    — the UD claim fails on the merits under the encoded rules (e.g., tenant cured timely)
  UNCERTAIN             — the encoded rules do not address this specific fact pattern

Application rules:
  1. If a notice_defect is present in the facts and its consequence is "notice_void", outcome = NOTICE_INVALID.
  2. If the notice satisfies all requirements in notice_types for the applicable type, outcome = NOTICE_VALID.
  3. If a UD was filed while the notice period was still running, outcome = UD_DEFECTIVE_PREMATURE.
  4. If the tenant timely cured a curable defect or otherwise defeats the claim on the merits, outcome = UD_NOT_SUSTAINABLE.
  5. If the rules file is silent on the controlling issue, outcome = UNCERTAIN.
  6. Cite the EXACT field path or defect name from the JSON (e.g. "notice_defects[includes_late_fees]").
  7. Return ONLY valid JSON. No prose. No markdown fences.

Return this exact structure:
{
  "outcome": "<one of the five values above>",
  "controlling_rule": "<exact defect name or field path from the JSON>",
  "reasoning": "<one or two sentences — how the specific encoded rule applies to these facts>",
  "confidence": "HIGH" | "MEDIUM" | "LOW",
  "rules_addressed_question": true | false
}
"""

# ── Integrity helpers ─────────────────────────────────────────────────────────

def sha256_file(path: Path) -> str:
    """SHA256 of raw file bytes — proves the Excel was not edited after scoring."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_row(item: dict) -> str:
    """SHA256 of a frozen item's key fields — detects individual row edits."""
    canonical = {
        "id":             item.get("id"),
        "facts":          item.get("facts"),
        "correct_outcome": item.get("correct_outcome"),
        "held_out":       item.get("held_out"),
        "status":         item.get("status"),
        "reviewed_by":    item.get("reviewed_by"),
        "date":           str(item.get("date", "")),
    }
    return hashlib.sha256(
        json.dumps(canonical, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()


def sha256_rules(section: dict) -> str:
    """SHA256 of the encoded rules section — ties each score to a specific rules version."""
    return hashlib.sha256(
        json.dumps(section, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()

# ── Schema validation ─────────────────────────────────────────────────────────

class YellowFlag(Exception):
    """Non-fatal schema/enum mismatch that requires Andy's ratification."""
    pass


class IntegrityError(Exception):
    """Fatal integrity violation — halts the scorer immediately."""
    pass


def validate_schema(headers: list) -> list[str]:
    """
    Check that all expected columns are present.
    Returns list of YELLOW messages (empty = all good).
    """
    yellows = []
    header_set = set(headers)
    for col in EXPECTED_COLUMNS:
        if col not in header_set:
            yellows.append(f"YELLOW-SCHEMA: Expected column '{col}' not found in Excel. "
                           f"Found columns: {headers}")
    return yellows


def validate_outcome_enum(items: list) -> list[str]:
    """
    Check that all frozen items' correct_outcome values are in KNOWN_OUTCOMES.
    Returns list of YELLOW messages.
    """
    yellows = []
    for item in items:
        outcome = item.get("correct_outcome", "")
        if outcome and outcome not in KNOWN_OUTCOMES:
            yellows.append(
                f"YELLOW-OUTCOME-ENUM: {item['id']} has correct_outcome='{outcome}' "
                f"which is not in the known enum {sorted(KNOWN_OUTCOMES)}. "
                f"Proposed mapping: [Andy must confirm — scorer cannot auto-resolve]."
            )
    return yellows


def validate_frozen_completeness(items: list) -> list[str]:
    """
    FROZEN items must have correct_outcome and held_out set.
    Returns list of YELLOW messages for incomplete items.
    """
    yellows = []
    for item in items:
        if not item.get("correct_outcome"):
            yellows.append(
                f"YELLOW-INCOMPLETE: FROZEN item {item['id']} is missing "
                f"'Correct outcome (if corrected)'. Cannot score. Skipping."
            )
        if item.get("held_out") not in (HELD_OUT_TRUE, HELD_OUT_FALSE):
            yellows.append(
                f"YELLOW-HELD-OUT: FROZEN item {item['id']} has held_out="
                f"'{item.get('held_out')}' (expected TRUE or FALSE). "
                f"Cannot partition. Andy must fix."
            )
    return yellows

# ── Excel loader ──────────────────────────────────────────────────────────────

def load_golden_set(xlsx_path: Path) -> tuple[list[dict], list[str]]:
    """
    Load and parse the golden set from Excel.

    Returns:
        (items, yellows) — items is a list of dicts for FROZEN items only;
        yellows is a list of YELLOW messages (schema, enum, completeness).
        EXCLUDED and DRAFT items are silently dropped (they are not scored).

    Raises IntegrityError if a FROZEN item fails to parse.
    """
    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        raise IntegrityError("Excel file has no rows.")

    headers = [str(c) if c is not None else "" for c in rows[0]]

    # Schema validation — must pass before any parsing
    yellows = validate_schema(headers)
    if yellows:
        return [], yellows  # Schema mismatch: return immediately with YELLOWs

    # Column index map
    col = {h: i for i, h in enumerate(headers)}

    items = []
    for row_num, row in enumerate(rows[1:], start=2):
        status = str(row[col["Status"]] or "").strip()

        if status in (EXCLUDED, DRAFT, ""):
            continue  # Silently skip — not scoreable

        if status != FROZEN:
            yellows.append(
                f"YELLOW-UNKNOWN-STATUS: Row {row_num} has Status='{status}' "
                f"(not FROZEN/EXCLUDED/DRAFT). Skipping."
            )
            continue

        # Parse FROZEN item — loud failure if required fields missing
        try:
            item_id = str(row[col["ID"]] or "").strip()
            if not item_id:
                raise IntegrityError(f"FROZEN row {row_num} has empty ID field.")

            attorney_verdict = str(row[col["ATTORNEY VERDICT"]] or "").strip()
            correct_outcome_field = str(row[col["Correct outcome (if corrected)"]] or "").strip()
            drafted_outcome       = str(row[col["Drafted outcome"]] or "").strip()
            held_out_raw          = str(row[col["Held-out (TRUE/FALSE)"]] or "").strip().upper()

            # 2026-07-18 fix: "Correct outcome (if corrected)" is, by its own
            # column name, meant to be left blank when the attorney did NOT
            # correct the drafted outcome -- i.e. when ATTORNEY VERDICT is
            # CONFIRM. That is not missing data; it's the attorney's own
            # CONFIRM verdict on this same row saying "Drafted outcome is
            # correct as-is." Read it, don't discard it. This is reading an
            # already-complete attorney judgment, not repairing an
            # incomplete one -- the "never silently repairs frozen items"
            # rule (see the except-block message below) is about the scorer
            # never GUESSING a missing correct answer; it does not apply
            # here, since CONFIRM + Drafted outcome together already fully
            # specify the answer. Any other ATTORNEY VERDICT value (or a
            # blank one) with no explicit "Correct outcome" still falls
            # through to validate_frozen_completeness()'s YELLOW-INCOMPLETE
            # below, unchanged -- the fallback is scoped narrowly to CONFIRM.
            if correct_outcome_field:
                correct_outcome = correct_outcome_field
                outcome_source = "corrected"
            elif attorney_verdict.upper() in ("CONFIRM", "CONFIRMED") and drafted_outcome:
                correct_outcome = drafted_outcome
                outcome_source = "drafted (ATTORNEY VERDICT=CONFIRM)"
                print(
                    f"  ℹ️  {item_id}: 'Correct outcome' blank + verdict CONFIRM — "
                    f"using Drafted outcome '{drafted_outcome}'.",
                    flush=True,
                )
            else:
                correct_outcome = ""
                outcome_source = "missing"

            item = {
                "id":              item_id,
                "module":          str(row[col["Module"]] or "").strip(),
                "jurisdiction":    str(row[col["Jurisdiction"]] or "").strip(),
                "facts":           str(row[col["Facts (scenario)"]] or "").strip(),
                "controlling_authority": str(row[col["Controlling authority"]] or "").strip(),
                "attorney_verdict": attorney_verdict,
                "drafted_outcome": drafted_outcome,
                "correct_outcome": correct_outcome,
                "outcome_source":  outcome_source,
                "reason_note":     str(row[col["Reason / note (required if corrected)"]] or "").strip(),
                "status":          status,
                "held_out":        held_out_raw if held_out_raw in (HELD_OUT_TRUE, HELD_OUT_FALSE, HELD_OUT_NA) else held_out_raw,
                "reviewed_by":     str(row[col["Reviewed by"]] or "").strip(),
                "date":            row[col["Date"]],
            }
            item["_row_hash"] = sha256_row(item)
            items.append(item)

        except IntegrityError:
            raise
        except Exception as exc:
            raise IntegrityError(
                f"FROZEN row {row_num} (ID={row[col['ID']]}) failed to parse: {exc}. "
                f"Fix the source data — scorer never silently repairs frozen items."
            )

    # Post-load validation
    yellows += validate_outcome_enum(items)
    yellows += validate_frozen_completeness(items)

    return items, yellows

# ── Rules loader ──────────────────────────────────────────────────────────────

# Active rules file. Prior versions remain immutable in the repo and are never
# overwritten (e.g. ca_eviction_v2.json = vProof1, cc0cfab63ae1591e2b88...,
# permanently the v0.3 held-out scoring anchor — retained for record even
# though no longer active). Bumping this constant is the only change needed
# to activate a new ratified version; see each file's version_history block.
ACTIVE_RULES_FILE = "ca_eviction_v3.json"

def load_ca_notice_rules() -> tuple[dict, str]:
    """Load CA notice module from the active rules file. Returns (rules_dict, file_sha256)."""
    rules_path = RULES_DIR / "california" / ACTIVE_RULES_FILE
    if not rules_path.exists():
        raise FileNotFoundError(f"CA rules file not found: {rules_path}")
    data   = json.loads(rules_path.read_text())
    notice = data.get("notice")
    if notice is None:
        raise KeyError(f"'notice' module not found in {ACTIVE_RULES_FILE}")
    file_hash = sha256_file(rules_path)
    return notice, file_hash

# ── Query builder ─────────────────────────────────────────────────────────────

def build_query(rules_section: dict, item: dict) -> str:
    """Build the query string fed to the model. Never includes correct_outcome."""
    return (
        f"ENCODED CA-NOTICE RULES:\n"
        f"{json.dumps(rules_section, indent=2)}\n\n"
        f"FACTS (Item {item['id']}):\n"
        f"{item['facts']}\n\n"
        f"Apply the encoded rules to these facts and return the JSON outcome."
    )

# ── Model callers (scorer-specific system prompt) ─────────────────────────────

def _parse_json(raw: str) -> dict:
    text  = re.sub(r"```(?:json)?", "", raw).strip()
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": f"json-parse-failure", "_raw": raw[:300]}


def _call_gpt(query: str) -> dict:
    try:
        from openai import OpenAI
    except ImportError:
        return {"error": "openai not installed", "model": OPENAI_MODEL}
    try:
        client = OpenAI(api_key=OPENAI_KEY)
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SCORER_SYSTEM_PROMPT},
                {"role": "user",   "content": query},
            ],
            max_completion_tokens=4000,
            timeout=90,
        )
        raw    = resp.choices[0].message.content.strip()
        parsed = _parse_json(raw)
        parsed["model"] = OPENAI_MODEL
        parsed["_raw"]  = raw
        return parsed
    except Exception as exc:
        return {"error": str(exc), "model": OPENAI_MODEL}


def _call_gemini(query: str) -> dict:
    try:
        from google import genai
    except ImportError:
        return {"error": "google-genai not installed", "model": GEMINI_MODEL}
    try:
        client      = genai.Client(api_key=GOOGLE_KEY)
        full_prompt = SCORER_SYSTEM_PROMPT + "\n\n" + query

        def _do():
            return client.models.generate_content(model=GEMINI_MODEL, contents=full_prompt)

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            fut  = pool.submit(_do)
            resp = fut.result(timeout=90)

        raw    = resp.text.strip()
        parsed = _parse_json(raw)
        parsed["model"] = GEMINI_MODEL
        parsed["_raw"]  = raw
        return parsed
    except Exception as exc:
        return {"error": str(exc), "model": GEMINI_MODEL}


def _mock_call(query: str, item_id: str) -> dict:
    """
    Dry-run mock: returns a deterministic stub.
    Used in --dry-run mode to verify the pipeline without spending API credits.
    """
    return {
        "outcome": "DRY-RUN-MOCK",
        "controlling_rule": "DRY-RUN",
        "reasoning": f"Dry run mock for {item_id} — no API call made.",
        "confidence": "N/A",
        "rules_addressed_question": None,
        "model": "DRY-RUN",
        "_raw": "",
    }

# ── Outcome normalizer ────────────────────────────────────────────────────────

def normalize_outcome(raw: str) -> str:
    """
    Map a raw model output string to the canonical outcome enum.
    If it maps cleanly, return the canonical value.
    If not, return raw (caller will YELLOW-flag it).
    """
    if not raw:
        return "EMPTY"
    r = raw.strip().upper()
    # Exact match (most cases)
    if r in KNOWN_OUTCOMES:
        return r
    # Common partial matches (defensive)
    if "INVALID" in r or "VOID" in r:
        return "NOTICE_INVALID"
    if "VALID" in r and "INVALID" not in r:
        return "NOTICE_VALID"
    if "PREMATURE" in r or "DEFECTIVE" in r:
        return "UD_DEFECTIVE_PREMATURE"
    if "NOT_SUSTAINABLE" in r or "SUSTAINABLE" in r:
        return "UD_NOT_SUSTAINABLE"
    if "UNCERTAIN" in r or "UNKNOWN" in r:
        return "UNCERTAIN"
    return raw  # Cannot normalize — caller will YELLOW

# ── Per-item scoring ──────────────────────────────────────────────────────────

def run_item(item: dict, rules: dict, dry_run: bool = False,
             sleep_s: int = 3) -> tuple[dict, list[str]]:
    """
    Run a single frozen item through the pipeline.
    Returns (result_dict, item_yellows).
    Never passes correct_outcome or authority to the model.
    """
    query = build_query(rules, item)
    item_yellows = []

    if dry_run:
        gpt     = _mock_call(query, item["id"])
        gemini  = _mock_call(query, item["id"])
    else:
        gpt     = _call_gpt(query)
        if sleep_s > 0:
            time.sleep(sleep_s)
        gemini  = _call_gemini(query)
        if sleep_s > 0 and sleep_s > 1:
            time.sleep(1)  # brief pause between items

    gpt_raw_outcome    = gpt.get("outcome",    "")
    gemini_raw_outcome = gemini.get("outcome", "")

    gpt_norm    = normalize_outcome(gpt_raw_outcome)
    gemini_norm = normalize_outcome(gemini_raw_outcome)

    # YELLOW if either model output doesn't map to the known enum
    for model_name, raw_out, norm_out in [
        ("GPT",    gpt_raw_outcome,    gpt_norm),
        ("Gemini", gemini_raw_outcome, gemini_norm),
    ]:
        if norm_out not in KNOWN_OUTCOMES and norm_out not in ("UNCERTAIN", "DRY-RUN-MOCK", "EMPTY"):
            item_yellows.append(
                f"YELLOW-OUTCOME-NOT-MAPPED: {item['id']} / {model_name} returned "
                f"'{raw_out}' which does not map to the outcome enum. "
                f"Proposed mapping: [Andy must confirm]. Item scored as mismatch."
            )

    # Agreement
    if gpt.get("error") and gemini.get("error"):
        agreement    = "BOTH-ERROR"
        primary_norm = "ERROR"
    elif gpt.get("error"):
        agreement    = "GPT-ERROR"
        primary_norm = gemini_norm
    elif not gemini_raw_outcome:
        agreement    = "GEMINI-EMPTY"
        primary_norm = gpt_norm
    elif gpt_norm == gemini_norm:
        agreement    = "AGREE"
        primary_norm = gpt_norm
    else:
        agreement    = "DISAGREE"
        primary_norm = gpt_norm  # GPT is primary; flag for review

    # Consensus validity: True only when BOTH models returned a usable outcome.
    # A run with consensus_valid=False on any item is NOT consensus-validated.
    # "DISAGREE" counts as consensus-operative — two models answered, even if they differed.
    consensus_valid = agreement in ("AGREE", "DISAGREE")

    correct_outcome = item["correct_outcome"]  # ground truth (never given to model)
    is_correct      = (primary_norm == correct_outcome and
                       primary_norm in KNOWN_OUTCOMES)
    score           = 1 if is_correct else 0

    result = {
        "id":                  item["id"],
        "held_out":            item["held_out"],
        "frozen_correct_outcome": correct_outcome,
        "predicted_outcome":   primary_norm,
        "is_correct":          is_correct,
        "score":               score,
        "model_agreement":     agreement,
        "consensus_valid":     consensus_valid,
        "gpt_outcome":         gpt_norm,
        "gemini_outcome":      gemini_norm,
        "gpt_controlling_rule":    gpt.get("controlling_rule",    ""),
        "gemini_controlling_rule": gemini.get("controlling_rule", ""),
        "gpt_reasoning":       gpt.get("reasoning",    ""),
        "gemini_reasoning":    gemini.get("reasoning", ""),
        "gpt_confidence":      gpt.get("confidence"),
        "gemini_confidence":   gemini.get("confidence"),
        "gpt_error":           gpt.get("error"),
        "gemini_error":        gemini.get("error"),
        # Mismatch context — controlling authority shown only on mismatch
        "controlling_authority_on_mismatch": (
            item.get("controlling_authority", "") if not is_correct else ""
        ),
        "_row_hash":           item["_row_hash"],
        "dry_run":             dry_run,
    }
    return result, item_yellows

# ── Scoring summary ───────────────────────────────────────────────────────────

def _partition_and_score(results: list[dict]) -> dict:
    """
    Split results into held-out and non-held-out partitions.
    Return summary dict with both scores kept separate.
    """
    held_out     = [r for r in results if r["held_out"] == HELD_OUT_TRUE]
    non_held_out = [r for r in results if r["held_out"] == HELD_OUT_FALSE]
    total        = [r for r in results]  # all scoreable (no partition filter)

    def _stats(partition: list) -> dict:
        n        = len(partition)
        correct  = sum(r["score"] for r in partition)
        pct      = round(100 * correct / n, 1) if n else None
        agree    = sum(1 for r in partition if r["model_agreement"] == "AGREE")
        disagree = sum(1 for r in partition if r["model_agreement"] == "DISAGREE")
        errors   = sum(1 for r in partition if "ERROR" in r.get("model_agreement", ""))
        sm_items = sum(1 for r in partition if not r.get("consensus_valid", True))
        return {"n": n, "correct": correct, "accuracy_pct": pct,
                "model_agree": agree, "model_disagree": disagree, "api_errors": errors,
                "single_model_items": sm_items}

    return {
        "held_out":     _stats(held_out),
        "non_held_out": _stats(non_held_out),
        "all_frozen":   _stats(total),
    }

# ── Consensus status classifier ───────────────────────────────────────────────

def _consensus_status(results: list[dict]) -> str:
    """
    Classify the run's consensus status across all scored items.

    Returns one of:
      DUAL-MODEL-CONSENSUS    — every item had responses from both models
      SM-GPT                  — all items were Gemini-empty; GPT was the sole model
      SM-GEMINI               — all items had GPT-error; Gemini was the sole model
      SM-BOTH-ERROR           — all items had errors from both models
      PARTIAL-CONSENSUS (k/n) — some items had dual-model, others did not
      NO-ITEMS                — nothing was scored
    """
    n = len(results)
    if n == 0:
        return "NO-ITEMS"
    n_sm = sum(1 for r in results if not r.get("consensus_valid", True))
    if n_sm == 0:
        return "DUAL-MODEL-CONSENSUS"
    n_dual = n - n_sm
    if n_sm == n:
        # Determine which model was absent
        agreements = [r.get("model_agreement", "") for r in results]
        if all(a == "GEMINI-EMPTY" for a in agreements):
            return "SM-GPT"
        if all(a == "GPT-ERROR" for a in agreements):
            return "SM-GEMINI"
        if all(a == "BOTH-ERROR" for a in agreements):
            return "SM-BOTH-ERROR"
        return "SM-MIXED-FAILURE"
    return f"PARTIAL-CONSENSUS ({n_dual}/{n} items dual-model)"


# ── Console report ────────────────────────────────────────────────────────────

def _print_report(results: list[dict], summary: dict, yellows: list[str],
                  state: str, module: str, dry_run: bool, run_meta: dict):
    print()
    print("═" * 70)
    print(f"DIRECTION B SCORE REPORT — {state} / {module}")
    if dry_run:
        print("  ⚠️  DRY RUN — no API calls made; predictions are mocks")
    print("═" * 70)

    # ── Consensus status banner (MUST appear before scores) ──────────────────
    cs = run_meta.get("consensus_status", "UNKNOWN")
    if cs == "DUAL-MODEL-CONSENSUS":
        print(f"\n  ✅ CONSENSUS STATUS: {cs}")
    else:
        print()
        print("  " + "⛔" * 35)
        print("  ⛔  CONSENSUS NOT OPERATIVE — THIS RUN IS SINGLE-MODEL")
        print(f"  ⛔  Consensus status: {cs}")
        print("  ⛔")
        print("  ⛔  Per CJaC protocol: a run where any model returns empty is")
        print("  ⛔  NOT consensus-validated. Results below are PRELIMINARY ONLY.")
        print("  ⛔  Machine-verified status requires ≥2 models returning non-empty.")
        print("  ⛔  DO NOT score or cite as consensus-validated.")
        print("  ⛔  Re-run when both models are available.")
        print("  " + "⛔" * 35)
        print()

    if yellows:
        print(f"\n  ⚠️  {len(yellows)} YELLOW FLAG(S) — Andy ratification required:")
        for y in yellows:
            print(f"    🟡 {y}")
        print()

    # Per-item table
    print(f"\n{'ID':<14} {'Held-out':<9} {'Correct':<26} {'Predicted':<26} {'Match':<6} {'Agree'}")
    print("─" * 98)
    for r in results:
        match_sym = "✅" if r["is_correct"] else "❌"
        print(f"{r['id']:<14} {r['held_out']:<9} {r['frozen_correct_outcome']:<26} "
              f"{r['predicted_outcome']:<26} {match_sym:<6} {r['model_agreement']}")
        if not r["is_correct"] and r["controlling_authority_on_mismatch"]:
            print(f"  {'':>14} ↳ authority: {r['controlling_authority_on_mismatch'][:70]}")

    # Summary
    print("\n" + "─" * 70)
    print("SCORES (held-out and non-held-out NEVER blended):\n")

    ho   = summary["held_out"]
    nho  = summary["non_held_out"]
    all_ = summary["all_frozen"]

    if ho["n"] > 0:
        sm_note = f", ⚠SM-items={ho['single_model_items']}" if ho.get("single_model_items", 0) > 0 else ""
        print(f"  🔒 HELD-OUT score:      {ho['correct']}/{ho['n']} = {ho['accuracy_pct']}%"
              f"  (agree={ho['model_agree']}, disagree={ho['model_disagree']}, "
              f"errors={ho['api_errors']}{sm_note})")
        if ho.get("single_model_items", 0) > 0:
            print(f"     ⚠  {ho['single_model_items']}/{ho['n']} held-out items were SINGLE-MODEL — not consensus-validated.")
        print(f"     ⚠  This is the headline number. Held-out set is now burned.")
    else:
        print(f"  🔒 HELD-OUT score:      no held-out items in this run")

    if nho["n"] > 0:
        nho_sm_note = f", ⚠SM-items={nho['single_model_items']}" if nho.get("single_model_items", 0) > 0 else ""
        print(f"  📊 NON-HELD-OUT score:  {nho['correct']}/{nho['n']} = {nho['accuracy_pct']}%"
              f"  (agree={nho['model_agree']}, disagree={nho['model_disagree']}, "
              f"errors={nho['api_errors']}{nho_sm_note})")
    else:
        print("  📊 NON-HELD-OUT score:  (no items)")

    print(f"\n  ALL frozen:  {all_['correct']}/{all_['n']} = {all_['accuracy_pct']}%")

    print("\n" + "─" * 70)
    print("Provenance:")
    print(f"  Excel file SHA256:  {run_meta.get('excel_sha256', 'N/A')[:20]}…")
    print(f"  Rules file SHA256:  {run_meta.get('rules_sha256', 'N/A')[:20]}…")
    print(f"  Run date:           {run_meta.get('run_date', 'N/A')}")
    print(f"  Scorer version:     {run_meta.get('scorer_version', 'N/A')}")
    print()
    print("Attorney-line reminder:")
    print("  A high score raises confidence in machine-verified output.")
    print("  It does NOT promote anything across the attorney-validated line.")
    print("  Crossing the attorney line requires a named human.")
    print("═" * 70)

# ── Main runner ───────────────────────────────────────────────────────────────

def run(xlsx_path: Path, dry_run: bool = False,
        held_out_only: bool = False, non_held_out_only: bool = False,
        sleep_s: int = 5, show_query_preview: bool = False) -> dict:
    """
    Full scoring run. Returns the output dict (also saved to OUTPUT_DIR).

    Never passes correct_outcome to the model.
    Fails loudly on any integrity or schema problem.
    """
    print(f"\n📂 Loading golden set: {xlsx_path.name}")
    excel_sha = sha256_file(xlsx_path)
    print(f"   SHA256: {excel_sha[:20]}…")

    # Load + validate
    all_items, yellows = load_golden_set(xlsx_path)

    # Hard-stop if schema is broken (no items could be parsed cleanly)
    schema_yellows = [y for y in yellows if y.startswith("YELLOW-SCHEMA")]
    if schema_yellows:
        print("\n🚨 SCHEMA MISMATCH — cannot proceed. Andy ratification required:")
        for y in schema_yellows:
            print(f"   {y}")
        raise SystemExit(1)

    # Hard-stop on completeness issues (FROZEN item without correct_outcome)
    completeness_yellows = [y for y in yellows if "INCOMPLETE" in y]
    if completeness_yellows:
        print("\n🚨 FROZEN ITEMS INCOMPLETE — cannot score:")
        for y in completeness_yellows:
            print(f"   {y}")
        # Don't halt entire run — filter out incomplete items
        incomplete_ids = {y.split()[2] for y in completeness_yellows}
        all_items = [i for i in all_items if i["id"] not in incomplete_ids]

    # Load rules
    rules, rules_sha = load_ca_notice_rules()
    print(f"📄 CA notice rules loaded. SHA256: {rules_sha[:20]}…")

    print(f"✅ {len(all_items)} FROZEN items loaded"
          + (f"; {len(yellows)} YELLOW(s) will be reported" if yellows else ""))

    # Partition filter
    if held_out_only and non_held_out_only:
        raise ValueError("Cannot use both --held-out-only and --non-held-out-only.")

    items_to_score = all_items
    if held_out_only:
        items_to_score = [i for i in all_items if i["held_out"] == HELD_OUT_TRUE]
        print(f"🔒 Held-out only: {len(items_to_score)} items")
        if not items_to_score:
            print("⚠️  No held-out items found. "
                  "If this is unexpected, check the 'Held-out (TRUE/FALSE)' column.")
    elif non_held_out_only:
        items_to_score = [i for i in all_items if i["held_out"] == HELD_OUT_FALSE]
        print(f"📊 Non-held-out only: {len(items_to_score)} items")

    if dry_run:
        print("\n🔍 DRY RUN — showing query preview for first 2 items; mocking all predictions\n")
        for item in items_to_score[:2]:
            print(f"── Query for {item['id']} ──────────────────────────────────────")
            query = build_query(rules, item)
            print(query[:800] + ("…" if len(query) > 800 else ""))
            print()

    # Score all items
    print(f"\n{'─' * 70}")
    print(f"Scoring {len(items_to_score)} items"
          + (" [DRY RUN — mock predictions]" if dry_run else "") + "…\n")

    results      = []
    all_yellows  = list(yellows)  # carry schema/enum yellows forward

    for i, item in enumerate(items_to_score):
        print(f"  [{i+1:>2}/{len(items_to_score)}] {item['id']}  "
              f"({item['held_out']} held-out) …", end="", flush=True)
        result, item_yellows = run_item(item, rules, dry_run=dry_run, sleep_s=sleep_s)
        results.append(result)
        all_yellows.extend(item_yellows)

        mark   = "✅" if result["is_correct"] else ("🔵" if dry_run else "❌")
        sm_tag = " ⚠SM" if not result.get("consensus_valid", True) else ""
        print(f"  {mark}  correct={result['frozen_correct_outcome']:<22}  "
              f"predicted={result['predicted_outcome']:<22}  "
              f"agree={result['model_agreement']}{sm_tag}")

    summary = _partition_and_score(results)
    cs      = _consensus_status(results)

    run_date = datetime.date.today().isoformat()
    run_id   = (f"ca_notice_score_{run_date}"
                + ("_dryrun" if dry_run else "")
                + ("_held-out" if held_out_only else "")
                + ("_non-held-out" if non_held_out_only else ""))

    n_sm = sum(1 for r in results if not r.get("consensus_valid", True))

    run_meta = {
        "run_id":              run_id,
        "run_date":            run_date,
        "scorer_version":      "v2.0-excel-native",
        "excel_path":          str(xlsx_path),
        "excel_sha256":        excel_sha,
        "rules_sha256":        rules_sha,
        "dry_run":             dry_run,
        "held_out_only":       held_out_only,
        "non_held_out_only":   non_held_out_only,
        "n_items_scored":      len(results),
        "n_yellows":           len(all_yellows),
        "consensus_status":    cs,
        "single_model_items":  n_sm,
        "consensus_note": (
            "DUAL-MODEL-CONSENSUS: both models answered on all scored items. "
            "Results may be cited as consensus-validated (subject to attorney review)."
        ) if cs == "DUAL-MODEL-CONSENSUS" else (
            f"NOT CONSENSUS-VALIDATED ({cs}). "
            f"{n_sm}/{len(results)} items had only one model respond. "
            "Results are PRELIMINARY ONLY. "
            "Re-run with both models operational before citing scores."
        ),
    }

    _print_report(results, summary, all_yellows,
                  state="CA", module="notice",
                  dry_run=dry_run, run_meta=run_meta)

    output = {
        **run_meta,
        "summary":         summary,
        "yellow_flags":    all_yellows,
        "results":         results,
        "attorney_line_note": (
            "A high score here raises confidence in machine-verified output. "
            "It does NOT promote anything across the attorney-validated line. "
            "Crossing that line requires a named human attorney."
        ),
    }

    out_path = OUTPUT_DIR / f"{run_id}.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False, default=str))
    print(f"📁 Output saved: {out_path.relative_to(REPO_ROOT)}")

    return output

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Direction B scorer — CA notice golden set vs. encoded rules"
    )
    parser.add_argument("--golden", required=True,
                        help="Path to goldenset.xlsx (attorney-reviewed Excel file)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Skip API calls; validate schema + show query previews only")
    parser.add_argument("--held-out-only", action="store_true",
                        help="Score held-out partition only (burns it — run once at publication)")
    parser.add_argument("--non-held-out-only", action="store_true",
                        help="Score non-held-out partition only (safe to iterate on)")
    parser.add_argument("--sleep", type=int, default=5,
                        help="Seconds between GPT and Gemini calls per item (default 5)")
    args = parser.parse_args()

    xlsx_path = Path(args.golden)
    if not xlsx_path.is_absolute():
        # Try relative to scorer dir, then repo root
        for base in (Path(__file__).parent, REPO_ROOT):
            candidate = base / xlsx_path
            if candidate.exists():
                xlsx_path = candidate
                break

    if not xlsx_path.exists():
        print(f"❌ Golden set file not found: {args.golden}")
        sys.exit(1)

    run(
        xlsx_path       = xlsx_path,
        dry_run         = args.dry_run,
        held_out_only   = args.held_out_only,
        non_held_out_only = args.non_held_out_only,
        sleep_s         = args.sleep,
    )


if __name__ == "__main__":
    main()
