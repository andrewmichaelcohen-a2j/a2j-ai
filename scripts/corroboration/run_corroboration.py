#!/usr/bin/env python3
"""
run_corroboration.py — Debt-track grounded-corroboration runner
=================================================================
Implements DEBT_PROJECT_ARCHITECTURE_SPEC.md §3(a), (b), (d) as a standalone,
Andy-run pipeline. Package per Cowork Direction "Phase A Unblock" (2026-08-26)
item 2, interface per Andy's 2026-08-26 follow-up message.

WHAT THIS RUNS, PER QUEUED NODE
--------------------------------
(a) Grounded derivation by three independent frontier models -- Anthropic
    (claude-opus-5), OpenAI (gpt-5.5), Google (gemini-2.5-pro). Each model is
    given ONLY the node's cited source text (grounded_derivation.derived_from)
    and title -- NOT the node's existing `logic`/`consequences` fields -- and
    asked to derive its own answer from that text alone, in a fixed JSON shape.
    This tests whether independent derivation from the same primary-source text
    reaches the same result; a model that can't ground its answer in the given
    text is scored as non-corroborating.

    Agreement is computed as a MECHANICAL NUMERIC/CITATION FINGERPRINT, not an
    LLM-judged semantic match: every number (day count, dollar amount, percent,
    year count) each model states in its derivation is extracted via regex and
    compared as a set across all three models. Identical fingerprint sets across
    all three = grounded-agreement. Any mismatch = disagreement, filed per (d).
    This is a deliberately conservative, auditable proxy -- it will not catch a
    subtle wording disagreement with no numeric component, and it is not a
    substitute for the human disagreement-queue review those flags route to.

    Citations are separately, mechanically verified: for every derived_from
    entry, the runner fetches the URL and checks whether a normalized version
    of quoted_text appears in the fetched page. This runs on live network
    regardless of --dry-run/--live (no model cost), unless --skip-citation-check
    is passed. Under --dry-run, citation checks are synthesized instead (no
    network call), consistent with "no keys, no cost, synthetic responses."

(b) Adversarial-generation pass. One model (Anthropic, a separate call from its
    (a) derivation) is given the node's full completeness_checklist and logic
    and asked to propose edge-case fact patterns designed to break it, each
    flagged for whether it exposes a genuine gap. Any exposed gap is filed to
    the disagreement queue per (d).

(d) Disagreement queue. Every (a) numeric-fingerprint mismatch, every failed
    citation check, and every (b) exposed gap is auto-filed with evidence to
    docs/DEBT_DISAGREEMENT_QUEUE.md -- appended only, never overwritten by this
    script (same append-only discipline as docs/HUMAN_REVIEW_QUEUE.md).

NOT IN THIS RUNNER (flagged, not silently absorbed):
  - (c) Mutation testing (spec section 3c) -- a separate, not-yet-built pipeline
    stage. Section 4's DRAFT->CORROBORATED promotion rule technically requires
    (a)-(d); this runner produces (a)/(b)/(d) evidence only. Treat this
    script's "tier_promotion_candidate" flag as partial evidence, not a
    complete basis for an actual tier edit -- and note this script NEVER edits
    any rules file or tier field itself (no agent ratifies anything, spec S11).
  - (e)/(f)/(g) sampling audit, adjudication, attorney certification -- Phase D,
    a separate, later stage (see docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md S3, S10).

DEMO-GATE METRICS (2026-08-26 "Concept Demo First" directive S2)
------------------------------------------------------------------
When scenarios.json is present (scripts/corroboration/scenarios.json), the run
summary also reports:
  - grounded_agreement_rate: % of processed demo-corpus nodes with full 3-model
    numeric-fingerprint agreement AND all citations live-verified AND no
    adversarial gap found.
  - scenario_pass_rate: % of defined demo scenarios where every node_id the
    scenario depends on passed the above bar.
Both are reported WITH their basis (n counted, which nodes/scenarios failed and
why) -- never as a bare percentage. The internal go/no-go gate is both >= 90%
before the demo is shown to anyone (including Stage-1.5-style friendlies).

USAGE
-----
  # 1. Verify the install costs nothing and touches no real API:
  python3 run_corroboration.py --dry-run

  # 2. First live batch -- demo corpus only (federal + TX + CA), the near-term
  #    priority per the 2026-08-26 concept-demo directive:
  python3 run_corroboration.py --live --demo-corpus-only

  # 3. Full corpus (all states, including UT/AZ/NY DRAFT stubs) once ready:
  python3 run_corroboration.py --live

  # Single node, for spot-checking:
  python3 run_corroboration.py --live --nodes TX-SOL-CONSUMER-DEBT

See README.md in this folder for full setup instructions.

GUARDRAILS (do not remove)
---------------------------
  - Keys read from .env at repo root (see .env.example); never hardcoded,
    logged, or committed. Never printed even in verbose/debug output.
  - This script NEVER writes to any rules/ file. Output is entirely additive:
    rules/debt/validation/runs/ (JSON) and docs/DEBT_DISAGREEMENT_QUEUE.md
    (Markdown, append-only). Tier promotion is a human/Andy decision.
  - Hard per-run budget cap (default $15.00, override with --budget-cap). The
    run stops BEFORE starting a node that would push projected spend over cap.
  - Exactly one of --dry-run / --live is required. Neither given -> error,
    nothing runs. This mirrors the eviction line's live_verified gate.

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import argparse
import glob
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEBT_RULES_DIR = REPO_ROOT / "rules" / "debt"
RUNS_DIR = REPO_ROOT / "rules" / "debt" / "validation" / "runs"
DISAGREEMENT_QUEUE_PATH = REPO_ROOT / "docs" / "DEBT_DISAGREEMENT_QUEUE.md"
SCENARIOS_PATH = Path(__file__).resolve().parent / "scenarios.json"
ENV_PATH = REPO_ROOT / ".env"

DEMO_CORPUS_DIRS = [
    DEBT_RULES_DIR / "federal",
    DEBT_RULES_DIR / "state" / "texas",
    DEBT_RULES_DIR / "state" / "california",
]

# -- Models (three independent frontier families, per spec S3a / S11) --------
ANTHROPIC_MODEL = "claude-opus-5"
OPENAI_MODEL = "gpt-5.5"
GEMINI_MODEL = "gemini-2.5-pro"

# -- Budget --------------------------------------------------------------
DEFAULT_BUDGET_CAP_USD = 15.00
# Per-node estimate: 3 grounded-derivation calls (~1,200 in / ~600 out tokens
# each, cited text + reasoning) + 1 adversarial-generation call (~1,800 in /
# ~900 out, full node context). Blended flagship pricing ballpark used
# elsewhere in this repo (l2_runner.py): call it $0.03-0.08/model-call at
# these token counts across the three families. ESTIMATE, NOT A GUARANTEE --
# prices and token usage vary by node complexity; the --dry-run pass prints a
# projected total before any live call using this same constant, so Andy sees
# the number before spending anything.
APPROX_COST_PER_NODE_USD = 0.45  # bumped 2026-08-26 round 3: +1 judge call/node for LLM-judged semantic agreement (still an estimate, not a guarantee -- see below)
# 36 total DRAFT nodes in the full corpus as of 2026-08-26 -> full-corpus
# estimate ~= $12.60, within the $15 default cap with modest headroom. Demo
# corpus (federal + TX + CA, ~18 nodes as of 2026-08-26) ~= $6.30.

SYSTEM_PROMPT_DERIVATION = (
    "You are a legal research assistant. You will be given a short excerpt of "
    "primary-source statutory or case-law text and a title describing what "
    "question it answers. Derive the answer STRICTLY from the text given -- do "
    "not use outside knowledge of the law, and do not guess if the text does "
    "not contain the answer. Respond ONLY in valid JSON: "
    '{"derivation_summary": "<2-4 sentence plain-language answer derived only '
    'from the given text>", "grounded": <true if you could derive the answer '
    'from the given text, false if the text was insufficient>, '
    '"citation_used": "<the cite you relied on>"}'
)

# Round 20 (2026-08-30), materiality bar added per Andy's explicit directive. Round
# 19 fixed a truncation bug that had silently disabled this stage for the project's
# entire history; once fixed, it found SOMETHING to flag on nearly every node -- some
# genuinely important (FDCPA-FALSE-DECEPTIVE-CATALOG's encoded list skips straight
# from subsection (5) to (8), missing (6) and (7) entirely -- a real gap), some
# trivially immaterial (a $0.03 interest-amount discrepancy, a corporate-suffix
# variant). Treating every one identically as gate-blocking defeats the purpose of
# the whole project: Andy's framing, verbatim -- "if we are looking for any
# difference between the 3 models, we'll find one every time and default to having
# a human attorney review every difference... the project would essentially fail."
# The model is now asked to reason explicitly about two separate questions before
# calling something a gap: is the fact pattern realistic and reasonably common (not
# a contrived corner case), and would the rule actually give a WRONG or materially
# misleading answer as a result (not just an incomplete-but-harmless one). Both
# sub-answers are recorded in the output for auditability -- nothing is hidden, an
# immaterial finding is just not gate-blocking. All edge cases (material or not)
# are still preserved in the run JSON for future use in improving the underlying
# rule encoding, per Andy's "at some point we should use these runs to make the
# underlying code more accurate" -- that is future work, not lost data.
SYSTEM_PROMPT_ADVERSARIAL = (
    "You are adversarially testing a legal rule encoding, looking only for MATERIAL "
    "gaps -- not any conceivable difference. You will be given a rule's logic and "
    "its completeness checklist (the facts it says are needed to apply it). Propose "
    "exactly 3 edge-case fact patterns designed to probe the rule or its checklist "
    "for gaps. For each, assess two separate questions: (1) is this fact pattern "
    "realistic and reasonably common -- something an actual person in this legal "
    "situation might plausibly present, not a contrived or rare corner case; and "
    "(2) would the rule, applied as encoded, actually produce a WRONG or materially "
    "misleading answer for that person -- not just an incomplete-but-harmless one. "
    "Only mark exposes_gap true if BOTH are true. A technically-real but trivial "
    "distinction -- a one-cent computational discrepancy, a corporate name variant, "
    "a hypertechnical subsection omission unlikely to be what an actual dispute "
    "turns on -- is NOT a material gap even if you can construct a scenario "
    "involving it. Respond ONLY in valid JSON: {\"edge_cases\": [{\"scenario\": "
    "\"<1-3 sentences>\", \"realistic_and_common\": <true/false>, "
    "\"would_cause_wrong_answer\": <true/false>, \"exposes_gap\": <true only if "
    "both above are true>, \"gap_description\": \"<or null>\"}, ...]}"
)

# Added 2026-08-26 (third round): replaces the numeric/citation-fingerprint
# comparison as the PRIMARY grounded-derivation agreement signal, per Andy's
# ratified decision after the fingerprint proxy produced three separate
# false-positive patterns in live use (citation-reference noise, the "no
# one" pronoun, and uncited subsection cross-references like "Paragraph
# (b)(2)(ii)") -- each fixed individually, but the pattern of new edge
# cases surfacing one per live run made clear that a mechanical proxy for
# this specific job (judging substantive legal agreement) has an
# open-ended failure surface. An LLM is a much better fit for "do these
# three answers agree in substance" than a digit-extraction regex is.
# The numeric fingerprint is NOT removed -- it is kept and reported as a
# secondary diagnostic (see stage_a_grounded_derivation.fingerprints),
# since it is fast, free, and occasionally a useful sanity cross-check --
# but it no longer gates CLEAN-PASS.
# Round 19 (2026-08-30), recalibrated per Andy's explicit directive: after round 18
# removed citation-liveness from the CLEAN-PASS gate, a live 18-node run still showed
# only 66.7% grounded-agreement. Full node-by-node read of every flag found ZERO actual
# legal conflicts -- 4 of 6 flags were the SAME pattern: all three models stated the
# identical governing rule with no contradiction, but one (usually Gemini) omitted a
# secondary, non-dispositive detail (an exception clause, a procedural deadline) that
# the other two included. The ORIGINAL judge prompt (round 3, 2026-08-26) explicitly
# instructed the judge to treat any such omission as "genuine disagreement" -- a
# deliberate design choice at the time, but one that, on this evidence, was gating
# CLEAN-PASS on completeness-of-summary rather than correctness-of-law. Andy's call:
# "if an omission but not a conflict then we should not flag; we should only flag
# actual conflicts." This prompt is rewritten accordingly. Omissions are NOT deleted
# from view -- the judge still surfaces them in agreement_notes for visibility -- they
# just no longer make agree=false on their own. Only an actual conflict (two analyses
# that cannot both be true of the same governing rule -- different amounts, different
# deadlines, different standards, or one asserting a rule applies while another
# asserts it does not) makes agree=false now.
# Round 20 (2026-08-30): materiality qualifier added to round 19's conflict-only
# fix, per the same directive as SYSTEM_PROMPT_ADVERSARIAL above -- Andy's framing:
# Claude is the primary author; the other two models corroborate, they are not three
# equal votes where any technical split forces human review. A genuine conflict
# (different dollar amount, different deadline) is materially different almost by
# definition, so this qualifier is mostly a backstop against a hypertechnical
# contradiction that wouldn't actually change the answer a real person gets --
# but it closes that door explicitly rather than leaving it open.
SYSTEM_PROMPT_JUDGE = (
    "You are checking whether three independently-produced legal analyses of the same "
    "question actually CONFLICT in their legal conclusion in a way that would change "
    "the practical answer a real person gets, as opposed to merely differing in what "
    "each one chose to mention or in some hypertechnical way that doesn't affect the "
    "outcome. Ignore differences in phrasing, level of detail, structure, "
    "illustrative examples, and -- importantly -- cases where one analysis includes a "
    "real detail (a rule, exception, deadline, or amount) that another simply omits "
    "without contradicting it. An omission by itself is NOT a disagreement. Respond "
    "\"agree\": false ONLY if two or more analyses state something that cannot both be "
    "true of the same governing rule AND that difference is material -- meaning it "
    "would change the practical answer or advice given to a typical person in a "
    "common scenario. Materially different dollar amounts, deadlines, or standards "
    "count; a technically-real but inconsequential wording distinction does not. If "
    "all three are consistent with each other on the material question -- even if "
    "some are less complete than others -- respond \"agree\": true, and use "
    "agreement_notes to note any real completeness differences worth a human's "
    "attention (this is informational, not a reason for agree=false). Respond ONLY "
    "in valid JSON: {\"agree\": <true if no analysis actually and materially "
    "conflicts with another, false only on a real, material conflict>, "
    "\"agreement_notes\": \"<1-3 sentences: confirm the shared conclusion, and separately "
    "note any completeness differences (non-gating) or, if agree=false, the specific "
    "material conflict and which analyses differ>\"}"
)

NUMBER_RE = re.compile(r"\$?\d[\d,]*(?:\.\d+)?%?")

# -- Fingerprint bug fix (2026-08-26, Andy's run 3 diagnosis) ------------------
# Root cause found by inspecting real run output: the fingerprint was comparing
# raw digit-only regex matches across models. Two independent problems, not a
# provider-specific parsing/auth/environment issue:
#   1. Models routinely spell small numbers as WORDS in prose ("three years")
#      rather than digits ("3 years") -- OpenAI and Gemini did this far more
#      often than Anthropic in the real run, so their fingerprints came back
#      empty even when their prose *agreed* with Anthropic's on the substance.
#   2. Citation references embedded in a model's own prose (e.g. "A.R.S.
#      S 12-543", "12 C.F.R. S 1006.34") contain digits that got swept into the
#      fingerprint as if they were part of the legal ANSWER -- so even
#      Anthropic's "successful" fingerprints were sometimes matching a statute
#      section number, not the actual day-count/dollar/year figure. This
#      produced spurious mismatches (or, worse, spurious matches) unrelated to
#      whether the models actually agreed on the law.
# Fix: (a) strip citation-shaped substrings before extracting numbers, (b)
# convert spelled-out number words to digits first. This is a runner-side fix
# only -- confirmed against real run output that this is a fingerprint-
# extraction bug, not a Python/OpenSSL/LibreSSL/environment issue on Andy's
# machine (his three keys returned real 200-level API responses; the models'
# raw derivation_summary text was correct prose in both the run-3 evidence and
# this fix's own test cases -- the bug was entirely in how that prose got
# reduced to a comparable fingerprint afterward).

# NOTE: an earlier draft of this regex used a literal ASCII "S" as a stand-in
# for the section-sign character and under re.IGNORECASE it matched the "s" in
# ordinary words like "six" or "considers", silently eating real answer text
# (caught in this session's own test run before shipping -- see
# scripts/corroboration/README.md changelog). Uses the actual section sign
# (\u00a7) and requires a digit before consuming a "Section"/"Rule"/abbreviation
# match, so it cannot fire on prose that merely contains those words.
_CITATION_STRIP_RE = re.compile(
    r"("
    r"\d+\s*U\.?\s*S\.?\s*C\.?\s*(?:\u00a7+|Section|Sec\.)?\s*[\w.\-()]*"   # 15 U.S.C. S1692g(a)
    r"|\d+\s*C\.?\s*F\.?\s*R\.?\s*(?:\u00a7+|Section|Sec\.)?\s*[\w.\-()]*"  # 12 C.F.R. S1006.34
    r"|\u00a7+\s*[\w.\-()]*"                                                 # bare S 12-543
    r"|\b(?:Section|Sec\.|Rule|Art\.|Article)\s+[\w.\-()]*\d[\w.\-()]*"       # Section 5, Rule 12(a)(1) -- must be followed by a digit-bearing token
    r"|\b(?:[A-Z]\.){2,}\s*\u00a7+\s*[\w.\-()]*"                              # A.R.S. S 12-548(A)
    r"|\b[A-Z]{2,}\s*\u00a7+\s*[\w.\-()]*"                                    # CCP S 337, CPLR S 213
    r")",
    re.IGNORECASE,
)

_NUMBER_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
    "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
    "eighty": 80, "ninety": 90, "hundred": 100,
}
# NOTE (found 2026-08-26, second round): "one" is also the indefinite pronoun
# in phrases like "no one may file suit" -- an earlier version of this regex
# converted that "one" to the digit 1, contributing a spurious \'1\' to the
# fingerprint that only shows up when a model happens to phrase a sentence
# that way (confirmed against real live-run prose on CA-SOL-WRITTEN-CONTRACT-
# DEBT: Anthropic\'s "no one may file suit" produced a stray \'1\' that the
# other two models\' differently-worded sentences never would have matched).
# The negative lookbehind below excludes the common pronoun-forming words
# that precede "one" in this idiomatic (non-numeral) sense; it does not
# affect genuine numeral usage like "one year" or compounds like
# "twenty-one days" (those aren\'t preceded by "no"/"any"/"some"/"every"/
# "each").
_NUMBER_WORD_RE = re.compile(
    r"(?<!no )(?<!any )(?<!some )(?<!every )(?<!each )"
    r"\b(" + "|".join(sorted(_NUMBER_WORDS, key=len, reverse=True)) + r")"
    r"(?:[\s-](" + "|".join(sorted(_NUMBER_WORDS, key=len, reverse=True)) + r"))?\b",
    re.IGNORECASE,
)


def _words_to_digits(text: str) -> str:
    """Replace spelled-out numbers (e.g. 'thirty', 'twenty-five', 'three') with
    their digit form so they compare equal to a model that wrote the digit."""
    def _sub(m):
        first = _NUMBER_WORDS.get(m.group(1).lower(), 0)
        second = _NUMBER_WORDS.get(m.group(2).lower(), 0) if m.group(2) else 0
        # "twenty-five" -> 20 + 5; "hundred" alone (rare, no tens word) -> 100
        total = first + second if second else first
        return str(total)
    return _NUMBER_WORD_RE.sub(_sub, text or "")


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_of(obj) -> str:
    blob = json.dumps(obj, sort_keys=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def sha256_of_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_numbers(text: str):
    """Extract a set of normalized numeric tokens from free text -- the
    fingerprint used for the (a) grounded-derivation agreement check.

    Pipeline (fixed 2026-08-26, see block comment above): strip citation-shaped
    substrings first (so a statute section number doesn't get compared as if
    it were part of the legal answer), then convert spelled-out numbers to
    digits (so 'three years' and '3 years' produce the same token), then
    extract digit runs. Drops commas, keeps $ and % markers since those change
    meaning ('30' vs '30%' vs '$30' are different facts).
    """
    cleaned = _CITATION_STRIP_RE.sub(" ", text or "")
    cleaned = _words_to_digits(cleaned)
    found = NUMBER_RE.findall(cleaned)
    normed = set()
    for tok in found:
        core = tok.replace(",", "")
        normed.add(core)
    return normed


# -- .env / key loading (only required under --live) -------------------------

def load_keys():
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("ERROR: python-dotenv not installed. Run:")
        print("  pip install -r scripts/corroboration/requirements.txt --break-system-packages")
        sys.exit(1)

    if not ENV_PATH.exists():
        print(
            f"ERROR: .env not found at repo root ({ENV_PATH}).\n"
            "Copy the template and fill in real keys:\n"
            "  cp .env.example .env\n"
            "Then edit .env with your real ANTHROPIC_API_KEY / OPENAI_API_KEY / "
            "GOOGLE_API_KEY. Never commit .env (already gitignored)."
        )
        sys.exit(1)

    load_dotenv(ENV_PATH)
    keys = {
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", ""),
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
        "GOOGLE_API_KEY": os.environ.get("GOOGLE_API_KEY", ""),
    }
    missing = [k for k, v in keys.items() if not v]
    if missing:
        print(f"ERROR: missing from .env: {', '.join(missing)}")
        sys.exit(1)
    return keys


# -- Model callers -------------------------------------------------------------
# Each returns: {"derivation_summary": str, "grounded": bool, "citation_used": str,
#                "model": str, "_raw": str, "error": str|None}

def _parse_json_response(raw: str) -> dict:
    text = re.sub(r"```(?:json)?", "", raw or "").strip()
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"derivation_summary": None, "grounded": False,
                "citation_used": None, "_parse_error": raw[:300] if raw else None}


def call_anthropic(system_prompt: str, user_prompt: str, keys, dry_run: bool,
                    dry_run_payload: dict, max_tokens: int = 1500,
                    retry_on_empty_or_truncated: bool = False,
                    replay_responses: list = None) -> dict:
    """Round 19 note: max_tokens is now a parameter, not a hardcoded 1500 shared by
    every call site. Root cause found by reading raw run output: the adversarial
    stage (3 edge cases, each with a scenario + gap_description) routinely produced
    JSON that got cut off mid-string at 1500 tokens, causing _parse_json_response to
    fail and silently discard real, correctly-identified gap findings (visible in the
    truncated _raw text even though the parsed result came back empty). Derivation
    and judge calls are shorter and were not observed truncating -- they keep the
    1500 default; the adversarial call site now passes a larger budget.

    Round 23 note (2026-08-30): round 19's fix reduced but did not eliminate
    truncation -- a live run still showed several adversarial calls cut off
    mid-string even at 3000 tokens, plus a separate failure mode (an empty
    completion, _raw: "", error: None, with no retry) neither round 19 nor any
    prior round addressed. Both were silently indistinguishable from "no gaps
    found" in the run JSON. `_stop_reason` now surfaces the API's own
    stop_reason so truncation is visible going forward. `retry_on_empty_or_truncated`
    (used only by the adversarial call site, not derivation/judge, which have
    never shown this) adds up to one retry: same budget for an empty
    completion (empirically transient), 1.5x budget for a max_tokens
    truncation (to actually fix it rather than just retry into the same wall)."""
    if replay_responses is not None:
        # Round 26 (freeze item 2): deterministic offline replay -- consumes
        # canned {"raw", "stop_reason", "error"} dicts in the same order the
        # live retry loop below would produce them, through the SAME
        # _parse_json_response + retry-decision logic (not a reimplementation),
        # so a calibration fixture genuinely exercises the parsing/retry code,
        # not a bypass of it. No keys, no network, no cost.
        _queue = list(replay_responses)

        def _one_call_replay(tokens: int) -> dict:
            item = _queue.pop(0) if _queue else {"raw": "", "stop_reason": None, "error": None}
            raw = item.get("raw") or ""
            parsed = _parse_json_response(raw)
            parsed["model"] = ANTHROPIC_MODEL
            parsed["_raw"] = raw
            parsed["error"] = item.get("error")
            parsed["_stop_reason"] = item.get("stop_reason")
            return parsed

        try:
            parsed = _one_call_replay(max_tokens)
            if retry_on_empty_or_truncated:
                empty = not parsed.get("_raw")
                truncated = parsed.get("_stop_reason") == "max_tokens" or bool(parsed.get("_parse_error"))
                if empty or truncated:
                    retry_tokens = max_tokens if empty else int(max_tokens * 2.5)
                    retry_parsed = _one_call_replay(retry_tokens)
                    retry_parsed["_retried_after"] = "empty_completion" if empty else "max_tokens_truncation"
                    return retry_parsed
            return parsed
        except Exception as exc:
            return {"error": str(exc), "model": ANTHROPIC_MODEL}
    if dry_run:
        out = dict(dry_run_payload)
        out["model"] = ANTHROPIC_MODEL
        out["_raw"] = "DRY-RUN"
        out["error"] = None
        return out
    try:
        import anthropic
    except ImportError:
        return {"error": "anthropic package not installed", "model": ANTHROPIC_MODEL}

    def _one_call(tokens: int) -> dict:
        client = anthropic.Anthropic(api_key=keys["ANTHROPIC_API_KEY"])
        resp = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        raw = "".join(b.text for b in resp.content if hasattr(b, "text")).strip()
        parsed = _parse_json_response(raw)
        parsed["model"] = ANTHROPIC_MODEL
        parsed["_raw"] = raw
        parsed["error"] = None
        parsed["_stop_reason"] = getattr(resp, "stop_reason", None)
        return parsed

    try:
        parsed = _one_call(max_tokens)
        if retry_on_empty_or_truncated:
            empty = not parsed.get("_raw")
            truncated = parsed.get("_stop_reason") == "max_tokens" or bool(parsed.get("_parse_error"))
            if empty or truncated:
                # Round 24: 1.5x (round 23) still wasn't enough for the 2 most
                # verbose nodes on a live run (still _parse_error after retry)
                # -- bumped to 2.5x for real headroom.
                retry_tokens = max_tokens if empty else int(max_tokens * 2.5)
                retry_parsed = _one_call(retry_tokens)
                retry_parsed["_retried_after"] = "empty_completion" if empty else "max_tokens_truncation"
                return retry_parsed
        return parsed
    except Exception as exc:
        return {"error": str(exc), "model": ANTHROPIC_MODEL}


def call_openai(system_prompt: str, user_prompt: str, keys, dry_run: bool,
                 dry_run_payload: dict, replay_response: dict = None) -> dict:
    if replay_response is not None:
        raw = replay_response.get("raw") or ""
        parsed = _parse_json_response(raw)
        parsed["model"] = OPENAI_MODEL
        parsed["_raw"] = raw
        parsed["error"] = replay_response.get("error")
        return parsed
    if dry_run:
        out = dict(dry_run_payload)
        out["model"] = OPENAI_MODEL
        out["_raw"] = "DRY-RUN"
        out["error"] = None
        return out
    try:
        from openai import OpenAI
    except ImportError:
        return {"error": "openai package not installed", "model": OPENAI_MODEL}
    try:
        client = OpenAI(api_key=keys["OPENAI_API_KEY"])
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_completion_tokens=1500,
            timeout=60,
        )
        raw = resp.choices[0].message.content.strip()
        parsed = _parse_json_response(raw)
        parsed["model"] = OPENAI_MODEL
        parsed["_raw"] = raw
        parsed["error"] = None
        return parsed
    except Exception as exc:
        return {"error": str(exc), "model": OPENAI_MODEL}


def call_gemini(system_prompt: str, user_prompt: str, keys, dry_run: bool,
                 dry_run_payload: dict, replay_response: dict = None) -> dict:
    """Round 17 note: 4 of 18 nodes in the 2026-08-28 full live run flagged
    solely because Gemini returned a transient 503 UNAVAILABLE ("high demand,
    try again later") -- an infra hiccup on Google's side, not a real error,
    but with no retry it silently costs a clean-pass every time it happens
    (roughly 1 in 4-5 nodes that run). citation_check already retries once on
    a flaky fetch (round 13); this mirrors that pattern here: retry once,
    brief pause, only for the specific transient-overload signature so a
    genuine error (bad key, malformed request, real API failure) still fails
    fast instead of waiting out a pointless retry.

    Round 19 fix: the original round-17 code retried on a transient 503, but a
    60s TimeoutError took a DIFFERENT branch (`except concurrent.futures.TimeoutError`)
    that returned immediately, bypassing the retry loop entirely -- so a plain
    timeout (observed live, 2026-08-30: FDCPA-UNFAIR-PRACTICES-CATALOG-1692f)
    still cost a clean-pass with zero retry, the exact failure mode round 17 was
    supposed to fix. Timeouts now retry once too, same budget as a 503."""
    if replay_response is not None:
        raw = replay_response.get("raw") or ""
        parsed = _parse_json_response(raw)
        parsed["model"] = GEMINI_MODEL
        parsed["_raw"] = raw
        parsed["error"] = replay_response.get("error")
        return parsed
    if dry_run:
        out = dict(dry_run_payload)
        out["model"] = GEMINI_MODEL
        out["_raw"] = "DRY-RUN"
        out["error"] = None
        return out
    try:
        from google import genai
    except ImportError:
        return {"error": "google-genai package not installed", "model": GEMINI_MODEL}
    try:
        import concurrent.futures
        client = genai.Client(api_key=keys["GOOGLE_API_KEY"])
        full_prompt = system_prompt + "\n\n" + user_prompt

        def _do():
            return client.models.generate_content(model=GEMINI_MODEL, contents=full_prompt)

        last_error = None
        for attempt in range(2):
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                fut = pool.submit(_do)
                try:
                    resp = fut.result(timeout=60)
                except concurrent.futures.TimeoutError:
                    last_error = "Gemini API timed out after 60s"
                    if attempt == 0:
                        continue
                    return {"error": last_error, "model": GEMINI_MODEL}
                except Exception as exc:
                    last_error = str(exc)
                    transient = "503" in last_error or "UNAVAILABLE" in last_error
                    if transient and attempt == 0:
                        time.sleep(3)
                        continue
                    return {"error": last_error, "model": GEMINI_MODEL}
                else:
                    raw = resp.text.strip()
                    parsed = _parse_json_response(raw)
                    parsed["model"] = GEMINI_MODEL
                    parsed["_raw"] = raw
                    parsed["error"] = None
                    return parsed
        return {"error": last_error, "model": GEMINI_MODEL}
    except Exception as exc:
        return {"error": str(exc), "model": GEMINI_MODEL}


def judge_semantic_agreement(summaries: list, keys, dry_run: bool, replay_response: dict = None) -> dict:
    """Ask a model to judge whether N independently-produced legal summaries
    substantively agree (2026-08-26, third round -- see SYSTEM_PROMPT_JUDGE
    comment for why this replaces the numeric fingerprint as the primary
    agreement signal). Summaries are presented unlabeled (just "Analysis 1/2/
    3") so the judge isn't told which provider wrote which -- a standard
    mitigation for self-preference bias in LLM-as-judge setups; Anthropic is
    used as the judge model here since it's already the anchor model for
    stage (b) adversarial generation in this pipeline, not because it's one
    of the three being judged (it is, which is a known limitation, not
    something this fix pretends to fully solve -- flagged in the README)."""
    if len(summaries) < 2 or any(not s for s in summaries):
        return {"agree": False, "agreement_notes": "Fewer than 2 non-empty summaries to compare.",
                "model": ANTHROPIC_MODEL, "_raw": "", "error": None, "_skipped": True}
    dry_payload = {
        "agree": True,
        "agreement_notes": "[DRY-RUN synthetic judgment -- all summaries synthetic and identical]",
    }
    numbered = "\n\n".join(f"Analysis {i+1}:\n{s}" for i, s in enumerate(summaries))
    user_prompt = f"Here are {len(summaries)} independent analyses of the same legal question:\n\n{numbered}"
    return call_anthropic(SYSTEM_PROMPT_JUDGE, user_prompt, keys, dry_run, dry_payload,
                           replay_responses=([replay_response] if replay_response is not None else None))


# -- Citation verification -----------------------------------------------------

import html as _html_module

_SCRIPT_STYLE_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.IGNORECASE | re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")


def _strip_html(raw_html: str) -> str:
    """Reduce raw HTML to visible text. Real root cause found this session
    (2026-08-26, Andy's run-3 diagnosis): the checker was matching against
    RAW, un-stripped HTML -- and both eCFR and Cornell LII (genuinely
    reachable, 200-status, content-correct pages, confirmed by manual fetch)
    wrap individual legal terms in inline <a> tags with NO surrounding
    whitespace in the source markup (e.g. '...initial<a href="...">
    communication</a>with a<a...>consumer</a>...'). A naive
    whitespace-normalize-only pass over the raw markup can concatenate
    adjacent words across a tag boundary ('debtcollector') and will never
    match a clean quoted sentence. Tags are replaced with a SPACE (not
    deleted) specifically so adjacent inline-linked words don't merge. This
    is a regex-based strip (no HTML parser dependency); documented
    limitation: malformed HTML or deeply nested comment/CDATA edge cases
    could still slip through -- acceptable for a mechanical sanity check that
    routes uncertain cases to a human either way."""
    t = _SCRIPT_STYLE_RE.sub(" ", raw_html or "")
    t = _TAG_RE.sub(" ", t)
    return t


def _normalize_for_match(raw_html_or_text: str, is_html: bool = True) -> str:
    t = _strip_html(raw_html_or_text) if is_html else (raw_html_or_text or "")
    t = _html_module.unescape(t)
    # Smart quotes/dashes that survive as literal unicode
    t = (t.replace("\u2018", "'").replace("\u2019", "'")
           .replace("\u201c", '"').replace("\u201d", '"')
           .replace("\u2013", "-").replace("\u2014", "-"))
    t = re.sub(r"\s+", " ", t).strip().lower()
    # Fixed 2026-08-30 (round 23): collapse whitespace immediately inside
    # parentheses. Root-caused via raw_html_context_at_break, captured for
    # the first time on a live run this round: eCFR (and similarly-marked-up
    # sources) wrap each character of a paragraph-hierarchy marker like "(1)"
    # in its own nested <span> -- e.g. <span class="paragraph-hierarchy">
    # <span class="paren">(</span>1<span class="paren">)</span></span> --
    # and _strip_html's blanket tag-to-space replacement (needed elsewhere to
    # avoid concatenating adjacent inline-linked WORDS) turns "(1)" into
    # "( 1 )" on the page side only. No quoted_text field in this corpus (and
    # no normal legal prose) ever has a space touching an opening or closing
    # parenthesis, so this is a safe, one-directional fix: it repairs the
    # page-side HTML-stripping artifact and is a no-op on the needle side.
    # Confirmed against this run's diagnostics: FDCPA-VALIDATION-NOTICE-1692g's
    # 12 C.F.R. 1006.34 citation broke exactly at "(1)", with
    # raw_html_context_at_break showing the nested-span markup verbatim.
    t = re.sub(r"\(\s+", "(", t)
    t = re.sub(r"\s+\)", ")", t)
    # Fixed 2026-08-31 (round 28): collapse whitespace immediately BEFORE
    # common sentence punctuation (comma/period/semicolon/colon). Root-caused
    # this round via FDCPA-REGF-CALL-FREQUENCY-1006.14b's 12 C.F.R.
    # 1006.14(b)(4) break (run_20260831T212748Z.json,
    # longest_matching_prefix_chars=34, breaking exactly at "paragraph (b),").
    # The round-23 fix above handles whitespace INSIDE parens (page-side "(
    # 1 )") but not this distinct pattern: eCFR wraps an inline
    # cross-reference like "paragraph (b)" in a single <a> tag whose CLOSING
    # tag lands immediately after the reference's own closing paren and
    # before the sentence's next punctuation mark -- e.g. raw markup
    # "...this <a href="...">paragraph (b)</a>, particular debt means...".
    # _strip_html's blanket tag-to-space substitution turns "</a>," into
    # " ,", inserting a stray space between ")" and "," that the round-23
    # fix doesn't touch (it only fires immediately inside a paren pair, not
    # after one). Confirmed directly against the live eCFR page fetched this
    # round: the actual visible/rendered text is genuinely "paragraph (b),
    # particular debt means..." with no space before the comma -- this is a
    # page-side HTML-stripping artifact, not a real difference in the text.
    # Same one-directional, additive-only reasoning as round 23: no normal
    # legal prose (and no quoted_text field in this corpus) ever has a space
    # before a comma/period/semicolon/colon, so this only ever helps a
    # correct match, never hides a real mismatch. New calibration fixture
    # (CAL-09) reproduces this exact tag-boundary-before-punctuation pattern
    # to regression-guard it.
    t = re.sub(r"\s+([,.;:])", r"\1", t)
    return t


def _word_overlap_ratio(needle: str, haystack: str) -> float:
    """Diagnostic-only fuzzy score: fraction of needle's words found anywhere
    in haystack. Never used to set `verified` -- verified stays gated on the
    strict substring check; this is purely to help a human tell 'source
    unreachable' apart from 'source reachable, wording just doesn't match
    exactly' when verified=False."""
    needle_words = [w for w in re.findall(r"[a-z0-9]+", needle) if len(w) > 2]
    if not needle_words:
        return 0.0
    haystack_words = set(re.findall(r"[a-z0-9]+", haystack))
    hits = sum(1 for w in needle_words if w in haystack_words)
    return round(hits / len(needle_words), 3)


def _longest_matching_prefix_len(needle: str, haystack: str) -> int:
    """Diagnostic-only: binary-search for the longest prefix of `needle` that
    appears verbatim (contiguously) in `haystack`. Added 2026-08-28 (round 14)
    per Andy's directive item 2 -- when word_overlap_ratio is high but
    verified is False, this pinpoints exactly where the contiguous match
    breaks down (e.g. an inserted link, an entity that didn't normalize, a
    stray heading), instead of leaving a human to re-fetch and manually diff.
    Pre-registered hypothesis for FDCPA-REGF-CALL-FREQUENCY-1006.14b's
    second citation (12 C.F.R. 1006.14(b)(4)): word_overlap_ratio was 1.0
    (every word present) but verified was False on the last live run, and a
    clean markdown approximation of the same page matched this quoted_text
    with no changes needed -- so the most likely cause is something in
    eCFR's raw HTML that a plain-text approximation doesn't reproduce (an
    internal cross-reference link inserted mid-sentence, e.g. around
    'paragraph (b)' or a definition term, adding or removing whitespace at
    a tag boundary; or a smart-quote/entity variant not covered by
    _normalize_for_match). This diagnostic will show the exact break point
    on the next live run instead of requiring another guess.
    """
    if not needle:
        return 0
    lo, hi = 0, len(needle)
    best = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if needle[:mid] in haystack:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def _raw_context_at_break(needle: str, prefix_len: int, raw_html: str):
    """Diagnostic-only (round 17): when a citation fails with a high word-overlap
    but a short matching prefix (the eCFR/Cornell pattern -- see verify_citation's
    normalization docstring), this pinpoints WHERE by returning a slice of raw,
    UN-stripped HTML from around the break point, so the actual markup (an inline
    <a> tag, an entity, a footnote marker) is visible instead of just the
    normalized/stripped text. Root-cause investigation this session confirmed the
    round-11 tag-to-space fix handles simple inline links correctly, and got as
    far as viewing the eCFR page's rendered content (via web_fetch's markdown
    approximation) without finding an obvious culprit -- but raw HTML fetches are
    blocked from this sandbox's network egress, so the exact byte-level cause is
    still unconfirmed. This diagnostic captures the raw markup on Andy's next live
    run (his machine has normal network access), removing the need for another
    round of guessing. Best-effort only: searches raw_html case-insensitively for
    the last ~20 normalized characters of the matched prefix; if that anchor can't
    be found in the raw text (e.g. it fell inside an HTML entity), returns None
    rather than a misleading snippet."""
    if prefix_len < 20 or not raw_html:
        return None
    anchor = needle[max(0, prefix_len - 20):prefix_len]
    idx = raw_html.lower().find(anchor.lower())
    if idx < 0:
        return None
    start = max(0, idx)
    return raw_html[start:start + 250]


def verify_citation(url: str, quoted_text: str, dry_run: bool, manual_verification: dict = None,
                     replay_page_html: str = None) -> dict:
    """Mechanically verify a cited source. Always returns a `diagnostics` block
    -- HTTP status, content length, content type, and a fuzzy word-overlap
    score -- even on success, so a `verified: False` result is self-explaining
    instead of a bare `error: None` (fixed 2026-08-26 per Andy's run-3 report:
    several failures here were reachable, legitimate primary/near-primary
    sources -- e.g. eCFR, Cornell LII -- returning normal 200 responses that
    simply didn't contain an exact substring match, which looked identical to
    an unreachable source before this fix)."""
    # Manual-verification override (round 17): a small number of primary/official
    # sources are confirmed-correct but structurally unverifiable by a plain HTTP
    # GET -- the site is a client-rendered SPA that serves the same generic shell
    # to every URL (statutes.capitol.texas.gov, confirmed 2026-08-29: CP.16, CN.16,
    # PR.41, and PR.42 all returned an identical 250874-byte page regardless of
    # which section was requested; direct browser rendering confirmed the real,
    # correct statute text loads client-side and matches quoted_text verbatim),
    # or the page itself is a loading-shell for an API-backed viewer (CourtListener
    # opinion pages return HTTP 202 with ~2KB of placeholder markup to a plain GET,
    # even though the CourtListener API returns the real, matching opinion text).
    # This is the same class of limitation as the already-documented azleg.gov
    # JS-gating (round 9) -- rather than let a structurally-unverifiable-by-design
    # source masquerade as a silent failure indistinguishable from a genuinely
    # wrong or unreachable citation, a human confirms it once, records how and
    # when, and the runner honors that confirmation explicitly and visibly
    # (method="manual", never silently, and never used to paper over an actual
    # content mismatch -- if the confirmed quote is later found wrong, the fix is
    # to correct the rules file and re-confirm, not to keep the manual flag).
    if replay_page_html is not None:
        # Round 26 (freeze item 2): replays the EXACT SAME needle-construction
        # and matching logic the live path uses (not a reimplementation) --
        # against a recorded page fixture instead of a live HTTP fetch. This
        # is what lets a calibration fixture genuinely exercise both the
        # round-23 paren-collapse fix and the round-24 ellipsis-split fix.
        page = _normalize_for_match(replay_page_html, is_html=True)
        quoted_text_for_match = (quoted_text or "").split("...", 1)[0]
        needle = _normalize_for_match(quoted_text_for_match, is_html=False)[:120]
        verified = needle in page if needle else False
        prefix_len = _longest_matching_prefix_len(needle, page) if needle else 0
        diagnostics = {
            "http_status": 200, "content_length": len(replay_page_html),
            "content_type": "text/html", "word_overlap_ratio": _word_overlap_ratio(needle, page),
            "retry_attempt": 1,
            "longest_matching_prefix_chars": prefix_len,
            "text_at_break_point": needle[prefix_len:prefix_len + 40] if not verified else None,
            "raw_html_context_at_break": (
                _raw_context_at_break(needle, prefix_len, replay_page_html) if not verified else None
            ),
        }
        return {"url": url, "verified": verified, "method": "replay", "error": None, "diagnostics": diagnostics}
    if manual_verification:
        return {
            "url": url, "verified": True, "method": "manual", "error": None,
            "diagnostics": {
                "http_status": None, "content_length": None, "content_type": None,
                "word_overlap_ratio": None,
                "manual_verification_note": manual_verification.get("note"),
                "manual_verification_date": manual_verification.get("date"),
            },
        }
    if dry_run:
        return {
            "url": url, "verified": True, "method": "dry-run-synthetic", "error": None,
            "diagnostics": {"http_status": None, "content_length": None,
                             "content_type": None, "word_overlap_ratio": None},
        }
    try:
        import requests
    except ImportError:
        return {
            "url": url, "verified": False, "method": "live",
            "error": "requests package not installed",
            "diagnostics": {"http_status": None, "content_length": None,
                             "content_type": None, "word_overlap_ratio": None},
        }
    # NOTE (found 2026-08-26, third round): the previous User-Agent
    # ("Mozilla/5.0 (CJaC corroboration runner)") caused eCFR to serve a
    # generic ~10.6KB fallback page -- identical byte count regardless of
    # which section was requested -- instead of real regulation text.
    # eCFR's own site displays a "you are using an unsupported browser"
    # banner for non-standard user agents, and the fallback served to this
    # UA lacked any real content. Confirmed by fetching the exact same URL
    # with a standard browser UA and getting the full, real section text.
    # FindLaw and Justia's 403s on every request in the same live run are
    # consistent with the same kind of basic bot-signature check (their
    # blocks may also depend on request volume/rate, which this header
    # change alone won't fix -- flagged as still-open below). Using a
    # standard, honest browser UA string is normal practice for polite
    # programmatic access to public, unauthenticated legal text; this is
    # not an attempt to evade any access control tied to identity or
    # payment.
    REQUEST_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    # NOTE (found 2026-08-26, round 13, investigating the TX re-pin):
    # statutes.capitol.texas.gov is intermittently flaky in a way distinct
    # from eCFR's old UA block or Justia/FindLaw's 403s -- the SAME exact
    # URL, fetched with no change in headers, alternated between the real
    # statute text and the site's bare navigation shell across successive
    # requests during this session (confirmed directly: PR.42.htm returned
    # the nav shell on attempt 1, then full real text on attempt 2; a large
    # constitution-article page timed out/returned empty twice before
    # succeeding on a 3rd attempt). This looks like edge-cache or
    # server-render-timeout flakiness, not a hard block -- a short retry
    # resolves it. Retry once (2 attempts total, brief pause between) only
    # when the first attempt got a real HTTP response but didn't verify;
    # a citation that's genuinely wrong will still fail on the retry, so
    # this doesn't mask real mismatches, only transient serving flakiness.
    last_result = None
    for attempt in range(2):
        try:
            resp = requests.get(url, timeout=20, headers=REQUEST_HEADERS)
            page = _normalize_for_match(resp.text, is_html=True)
            # Round 24 fix: if quoted_text contains an editorial ellipsis
            # ("...", used to elide text between two cited clauses -- a
            # normal, established practice in this corpus, see e.g. round 21's
            # FDCPA-FALSE-DECEPTIVE-CATALOG-1692e fix), only the text BEFORE
            # the first ellipsis is guaranteed to be a literal, contiguous
            # excerpt -- everything after it is deliberately non-contiguous
            # with the page by design. Confirmed via raw_html_context_at_break
            # on a live run this round: two citations broke exactly at their
            # own "..." with the actual page text perfectly clean and
            # contiguous at that point (e.g. CCP 683.020's "(a) The judgment
            # may not be enforced. (b) All enforcement procedures..." reads
            # straight through with no gap on the page -- our own ellipsis was
            # the only thing that didn't literally appear). Using a blind
            # 120-char window of the full quoted_text could land past the
            # ellipsis and require the literal three dots to appear on a real
            # page, which no real page will ever contain. Text before the
            # ellipsis is used verbatim (still capped to 120 chars); if there
            # is no ellipsis this is a no-op.
            quoted_text_for_match = (quoted_text or "").split("...", 1)[0]
            # Use a shortened window of the quoted text (first ~120 chars) to
            # tolerate minor HTML-entity/whitespace differences in the fetched page.
            needle = _normalize_for_match(quoted_text_for_match, is_html=False)[:120]
            verified = needle in page if needle else False
            prefix_len = _longest_matching_prefix_len(needle, page) if needle else 0
            diagnostics = {
                "http_status": resp.status_code,
                "content_length": len(resp.content),
                "content_type": resp.headers.get("Content-Type"),
                "word_overlap_ratio": _word_overlap_ratio(needle, page),
                "retry_attempt": attempt + 1,
                # Diagnostic pinpoint (round 14): how many leading characters of
                # `needle` matched contiguously before the match broke, and the
                # exact text that was expected next but wasn't found there.
                # Only meaningful when verified is False -- when True this
                # equals len(needle) and text_at_break_point is None.
                "longest_matching_prefix_chars": prefix_len,
                "text_at_break_point": needle[prefix_len:prefix_len + 40] if not verified else None,
                "raw_html_context_at_break": (
                    _raw_context_at_break(needle, prefix_len, resp.text) if not verified else None
                ),
            }
            last_result = {"url": url, "verified": verified, "method": "live", "error": None,
                            "diagnostics": diagnostics}
            if verified:
                return last_result
            if attempt == 0:
                time.sleep(2)
        except Exception as exc:
            last_result = {
                "url": url, "verified": False, "method": "live", "error": str(exc),
                "diagnostics": {"http_status": None, "content_length": None,
                                 "content_type": None, "word_overlap_ratio": None,
                                 "retry_attempt": attempt + 1},
            }
            if attempt == 0:
                time.sleep(2)
    return last_result


# -- Node discovery ---------------------------------------------------------------

def discover_nodes(demo_corpus_only: bool, only_node_ids=None):
    """Returns list of dicts: {file, node, node_id, node_index}."""
    if demo_corpus_only:
        search_dirs = DEMO_CORPUS_DIRS
    else:
        search_dirs = [DEBT_RULES_DIR]

    files = set()
    for d in search_dirs:
        if d.exists():
            files.update(Path(p) for p in glob.glob(str(d / "**" / "*.json"), recursive=True))

    out = []
    for f in sorted(files):
        try:
            data = json.loads(f.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        for idx, node in enumerate(data.get("nodes", [])):
            if node.get("tier") != "DRAFT":
                continue  # only DRAFT nodes are corroboration candidates
            if only_node_ids and node.get("node_id") not in only_node_ids:
                continue
            out.append({"file": f, "node": node, "node_id": node.get("node_id"), "node_index": idx})
    return out


# -- Disagreement queue filing -------------------------------------------------

DISAGREEMENT_QUEUE_HEADER = """# Debt-track Disagreement Queue

**Module:** Debt Defense Prototype (all states/federal) - **Layer:** grounded-corroboration + adversarial-generation
**Runner rule:** `scripts/corroboration/run_corroboration.py` appends new flagged items only. It never edits or
overwrites the Resolution, Resolved by, or Date fields -- those belong to Andy / the certifying attorney.
Built per DEBT_PROJECT_ARCHITECTURE_SPEC.md S3(d), generalizing Direction D-2 (`docs/DIRECTION_D_ROADMAP.md`) into
the debt track, per the 2026-08-26 Phase-A-Unblock direction item 6.

> **How to use this queue:** work top-to-bottom. Each entry has a candidate classification (rule gap / model error /
> citation-aggregator error) computed mechanically by the runner as a *hint*, not a determination -- the runner does
> not and cannot decide which side is legally correct. Fill in Resolution and Resolved-by, then move to Resolved.

---

## Open

"""


def ensure_disagreement_queue_exists():
    if not DISAGREEMENT_QUEUE_PATH.exists():
        DISAGREEMENT_QUEUE_PATH.write_text(DISAGREEMENT_QUEUE_HEADER)


def file_disagreement(entry_md: str):
    ensure_disagreement_queue_exists()
    text = DISAGREEMENT_QUEUE_PATH.read_text()
    marker = "## Open\n"
    idx = text.find(marker)
    if idx == -1:
        text = text + "\n" + marker
        idx = text.find(marker)
    insert_at = idx + len(marker)
    new_text = text[:insert_at] + "\n" + entry_md + "\n" + text[insert_at:]
    DISAGREEMENT_QUEUE_PATH.write_text(new_text)


# -- Per-node pipeline --------------------------------------------------------

def run_node(target: dict, keys, dry_run: bool, skip_citation_check: bool, run_id: str,
             replay_fixture: dict = None) -> dict:
    node = target["node"]
    node_id = target["node_id"]
    file_path = target["file"]
    started = now_iso()

    derived_from = node.get("grounded_derivation", {}).get("derived_from", [])
    source_text = "\n\n".join(
        f"Cite: {d.get('cite')}\nText: {d.get('quoted_text')}" for d in derived_from
    )
    user_prompt_derivation = (
        f"Title: {node.get('title')}\n\nSource text (this is ALL you may rely on):\n{source_text}\n\n"
        "Derive the answer strictly from this text."
    )

    dry_payload = {
        "derivation_summary": f"[DRY-RUN synthetic derivation for {node_id}]",
        "grounded": True,
        "citation_used": derived_from[0].get("cite") if derived_from else None,
    }
    replay = (replay_fixture or {}).get("_replay")

    # (a) three independent grounded derivations
    results_a = [
        call_anthropic(SYSTEM_PROMPT_DERIVATION, user_prompt_derivation, keys, dry_run, dry_payload,
                        replay_responses=(replay["stage_a"]["anthropic"] if replay else None)),
        call_openai(SYSTEM_PROMPT_DERIVATION, user_prompt_derivation, keys, dry_run, dry_payload,
                     replay_response=(replay["stage_a"]["openai"] if replay else None)),
        call_gemini(SYSTEM_PROMPT_DERIVATION, user_prompt_derivation, keys, dry_run, dry_payload,
                     replay_response=(replay["stage_a"]["gemini"] if replay else None)),
    ]

    fingerprints = []
    for r in results_a:
        summary = (r.get("derivation_summary") or "") if not r.get("error") else ""
        fingerprints.append(normalize_numbers(summary))

    all_grounded = all(bool(r.get("grounded")) and not r.get("error") for r in results_a)
    # Numeric fingerprint agreement -- kept as a secondary diagnostic only as
    # of 2026-08-26 round 3 (see SYSTEM_PROMPT_JUDGE comment). No longer
    # gates CLEAN-PASS.
    fp_agreement = (
        len(fingerprints) == 3
        and fingerprints[0] == fingerprints[1] == fingerprints[2]
        and all_grounded
    )

    # Semantic (LLM-judged) agreement -- the PRIMARY grounded-derivation
    # agreement signal as of 2026-08-26 round 3. Skip the extra call (save
    # cost) when a model already errored or reported ungrounded -- that's
    # not a case the judge needs to weigh in on, it's already a fail.
    if all_grounded:
        summaries_for_judge = [(r.get("derivation_summary") or "") for r in results_a]
        judge_result = judge_semantic_agreement(summaries_for_judge, keys, dry_run,
                                                 replay_response=(replay["judge"] if replay else None))
        semantic_agreement = bool(judge_result.get("agree")) and not judge_result.get("error")
    else:
        judge_result = {
            "agree": False,
            "agreement_notes": "Skipped -- not all three models returned a grounded, error-free result.",
            "model": ANTHROPIC_MODEL, "_raw": "", "error": None, "_skipped": True,
        }
        semantic_agreement = False

    # Citation verification (mechanical, all cited sources)
    citation_results = []
    for d in derived_from:
        if skip_citation_check:
            citation_results.append({"url": d.get("url"), "verified": None, "method": "skipped", "error": None})
        else:
            citation_results.append(verify_citation(
                d.get("url"), d.get("quoted_text"), dry_run, d.get("manual_verification"),
                replay_page_html=((replay.get("citation") or {}).get(d.get("url")) if replay else None)))
    if skip_citation_check:
        all_citations_verified = None
    else:
        all_citations_verified = bool(citation_results) and all(c["verified"] is True for c in citation_results)

    # (b) adversarial generation -- one call, Anthropic
    user_prompt_adversarial = (
        f"Node title: {node.get('title')}\n\n"
        f"Logic: {json.dumps(node.get('logic', {}))}\n\n"
        f"Completeness checklist: {json.dumps(node.get('completeness_checklist', []))}"
    )
    dry_adversarial_payload = {
        "edge_cases": [
            {"scenario": "[DRY-RUN synthetic edge case 1]", "exposes_gap": False, "gap_description": None},
            {"scenario": "[DRY-RUN synthetic edge case 2]", "exposes_gap": False, "gap_description": None},
            {"scenario": "[DRY-RUN synthetic edge case 3]", "exposes_gap": False, "gap_description": None},
        ]
    }
    # Round 23: budget bumped 3000 -> 4000 (still truncating some verbose
    # 3-scenario responses at 3000), and retry_on_empty_or_truncated enabled
    # -- see call_anthropic's round-23 docstring note.
    result_b = call_anthropic(SYSTEM_PROMPT_ADVERSARIAL, user_prompt_adversarial, keys, dry_run,
                               dry_adversarial_payload, max_tokens=4000,
                               retry_on_empty_or_truncated=True,
                               replay_responses=(replay["adversarial"] if replay else None))
    # Round 26 fix (found during the round-25 stage-level attribution pass on
    # run_20260831T082700Z): _parse_json_response's failure fallback dict has
    # no "edge_cases" key at all -- so `result_b.get("edge_cases", [])` was
    # silently returning [] on a genuine parse failure (error stays None;
    # only _parse_error is set), identical to a real "no gaps found" result.
    # TX-WAGE-GARNISHMENT-PROHIBITION showed CLEAN-PASS in that run despite an
    # unrecovered _parse_error -- a Stage B failure must not read as clean.
    stage_b_parsed_ok = ("edge_cases" in result_b) and not result_b.get("error")
    edge_cases = result_b.get("edge_cases", []) if stage_b_parsed_ok else []
    gaps_found = [e for e in edge_cases if e.get("exposes_gap")]

    ended = now_iso()

    # Round 18 (2026-08-29): per Andy's explicit directive ("proceed without a live
    # citation verification -- that can be done later ... validating the legal rule and
    # not focus on the byte for byte match"), a SKIPPED citation check (all_citations_verified
    # is None) no longer blocks CLEAN-PASS -- only an actively FAILED check (False) does.
    # This intentionally decouples "is the legal rule correctly derived and complete"
    # (grounded derivation + semantic agreement + adversarial check -- the actual point of
    # this pipeline) from "is a website reachable via plain HTTP GET right now" (citation
    # liveness -- an infrastructure concern, re-triaged 2026-08-29 as the dominant source of
    # noise across rounds 9-17: 11 of the last 13 flags traced to this, zero to legal error).
    clean_pass = (
        bool(semantic_agreement) and (all_citations_verified is not False)
        and not gaps_found and stage_b_parsed_ok
    )

    # (d) file disagreements -- round 26: never filed during --replay, since
    # calibration fixtures are synthetic by design (several are deliberately
    # FLAGGED to prove the checker still catches real problems) and have no
    # business appearing in the real, attorney-facing disagreement queue.
    if replay_fixture is None and not semantic_agreement:
        entry = _format_disagreement_entry(
            run_id, node_id, file_path, "MODEL-DISAGREEMENT",
            f"LLM-judged semantic agreement: {judge_result.get('agreement_notes')} "
            f"(judge model: {judge_result.get('model')}"
            + (", judge call errored: " + str(judge_result.get("error")) if judge_result.get("error") else "")
            + f"). Numeric-fingerprint diagnostic (secondary, not gating): "
            f"Anthropic={sorted(fingerprints[0]) if len(fingerprints) > 0 else 'n/a'}, "
            f"OpenAI={sorted(fingerprints[1]) if len(fingerprints) > 1 else 'n/a'}, "
            f"Gemini={sorted(fingerprints[2]) if len(fingerprints) > 2 else 'n/a'} "
            f"(fingerprint_agreement={fp_agreement}).",
            results_a,
        )
        file_disagreement(entry)
    if replay_fixture is None and all_citations_verified is False:
        failed = [c for c in citation_results if c["verified"] is not True]
        entry = _format_disagreement_entry(
            run_id, node_id, file_path, "CITATION-CHECK-FAILED",
            f"{len(failed)} of {len(citation_results)} cited source(s) could not be mechanically "
            f"verified live: {failed}",
            results_a,
        )
        file_disagreement(entry)
    if replay_fixture is None and gaps_found:
        entry = _format_disagreement_entry(
            run_id, node_id, file_path, "ADVERSARIAL-GAP",
            f"{len(gaps_found)} adversarial edge case(s) flagged as exposing a gap: {gaps_found}",
            results_a,
        )
        file_disagreement(entry)
    if replay_fixture is None and not stage_b_parsed_ok:
        entry = _format_disagreement_entry(
            run_id, node_id, file_path, "STAGE-B-PARSE-FAILURE",
            f"Adversarial check did not return parseable edge_cases even after retry "
            f"(error={result_b.get('error')!r}, _parse_error={result_b.get('_parse_error')!r}, "
            f"_stop_reason={result_b.get('_stop_reason')!r}) -- gaps cannot be assessed this run, "
            f"so this node cannot be CLEAN-PASS regardless of Stage A/citation results (round 26 fix).",
            results_a,
        )
        file_disagreement(entry)

    return {
        "node_id": node_id,
        "file": str(file_path.relative_to(REPO_ROOT)),
        "started": started,
        "ended": ended,
        "input_sha256": sha256_of_file(file_path),
        "node_sha256": sha256_of(node),
        "stage_a_grounded_derivation": {
            "results": results_a,
            "all_grounded": all_grounded,
            "semantic_agreement": semantic_agreement,
            "semantic_agreement_judge": judge_result,
            "fingerprints_diagnostic_only": [sorted(f) for f in fingerprints],
            "fingerprint_agreement_diagnostic_only": fp_agreement,
        },
        "citation_check": {
            "results": citation_results,
            "all_verified": all_citations_verified,
        },
        "stage_b_adversarial": {
            "result": result_b,
            "gaps_found": gaps_found,
            "parsed_successfully": stage_b_parsed_ok,
        },
        "status": "CLEAN-PASS" if clean_pass else "FLAGGED",
        "tier_promotion_candidate": clean_pass,
        "tier_promotion_note": (
            "Evidence covers spec (a)/(b)/(d) only -- (c) mutation testing not yet built. "
            "This flag is a recommendation for Andy's review, not an automatic tier change; "
            "this script never edits any rules file."
            + (
                " CITATION VERIFICATION WAS SKIPPED THIS RUN (--skip-citation-check, round 18 "
                "directive 2026-08-29) -- this CLEAN-PASS reflects grounded-derivation, "
                "semantic-agreement, and adversarial-check evidence only, NOT citation liveness. "
                "Citation verification is deferred, not waived; re-run without the flag (or use "
                "manual_verification) before treating a citation as confirmed."
                if skip_citation_check else ""
            )
        ),
    }


def _format_disagreement_entry(run_id, node_id, file_path, kind, evidence, model_results):
    ts = now_iso()
    rel = file_path.relative_to(REPO_ROOT)
    model_lines = "\n".join(
        f"  - {r.get('model')}: grounded={r.get('grounded')}, error={r.get('error')}, "
        f"summary={r.get('derivation_summary')!r}"
        for r in model_results
    )
    return f"""### [{node_id}] {kind} -- run {run_id}, {ts}

**File:** `{rel}`
**Classification hint (mechanical, not authoritative):** {kind}
**Evidence:** {evidence}

**Per-model derivation results:**
{model_lines}

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---
"""


# -- Scenario/demo-gate metrics ------------------------------------------------

def compute_demo_gate_metrics(node_results: list, demo_corpus_only: bool, citation_check_skipped: bool = False,
                               force_include_all: bool = False) -> dict:
    """Round 26 rewrite (freeze item 1's reconciliation finding, 2026-08-31):
    the old single 'grounded_agreement_rate' was named for Stage A (grounded
    derivation + cross-model agreement) but its actual computed basis was
    full CLEAN-PASS -- semantic agreement AND citation verification AND no
    adversarial gap. A run with 100% real Stage A agreement but a struggling
    citation-checker (run_20260831T082700Z: 18/18 Stage A, 6/18 citations,
    1/18 full CLEAN-PASS) reported a 5.6% "grounded-agreement rate," which
    understated the actual grounding quality by conflating three different
    stages into one number under a name that only described one of them.

    Every metric below is documented with its exact stage, numerator, and
    denominator (Andy's directive) -- see also
    docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md S4's round-26 entry for the
    canonical reference version of this table.

    force_include_all (round 26): the calibration/replay harness's fixtures
    live under scripts/corroboration/calibration_fixtures/, outside
    rules/debt/, so the normal demo-corpus path-prefix filter would exclude
    every one of them. Setting this bypasses that filter and treats every
    node_result passed in as the metric-computation population -- used only
    by run_replay_calibration(), never by a real --dry-run/--live run."""
    if not SCENARIOS_PATH.exists() and not force_include_all:
        return None

    scenarios = json.loads(SCENARIOS_PATH.read_text()).get("scenarios", []) if SCENARIOS_PATH.exists() else []
    results_by_id = {r["node_id"]: r for r in node_results}

    if force_include_all:
        demo_node_results = list(node_results)
    else:
        demo_node_results = [
            r for r in node_results
            if any(str(r["file"]).startswith(f"rules/debt/{sub}") for sub in ("federal", "state/texas", "state/california"))
        ]
    n_demo = len(demo_node_results)

    n_pass = sum(1 for r in demo_node_results if r["status"] == "CLEAN-PASS")
    full_pipeline_clean_pass_rate = (n_pass / n_demo * 100) if n_demo else None

    n_stage_a_pass = sum(
        1 for r in demo_node_results
        if r["stage_a_grounded_derivation"]["all_grounded"] and r["stage_a_grounded_derivation"]["semantic_agreement"]
    )
    stage_a_grounded_agreement_rate = (n_stage_a_pass / n_demo * 100) if n_demo else None

    if citation_check_skipped:
        citation_verification_rate = None
        n_citation_pass = None
    else:
        n_citation_pass = sum(1 for r in demo_node_results if r["citation_check"]["all_verified"] is True)
        citation_verification_rate = (n_citation_pass / n_demo * 100) if n_demo else None

    n_stage_b_pass = sum(1 for r in demo_node_results if r["stage_b_adversarial"].get("parsed_successfully"))
    stage_b_parse_success_rate = (n_stage_b_pass / n_demo * 100) if n_demo else None

    scenario_rows = []
    n_scen_pass = 0
    for s in scenarios:
        deps = s.get("depends_on_node_ids", [])
        missing = [d for d in deps if d not in results_by_id]
        dep_results = [results_by_id[d] for d in deps if d in results_by_id]
        passed = bool(dep_results) and not missing and all(r["status"] == "CLEAN-PASS" for r in dep_results)
        if passed:
            n_scen_pass += 1
        scenario_rows.append({
            "scenario_id": s.get("id"),
            "passed": passed,
            "depends_on_node_ids": deps,
            "missing_from_this_run": missing,
            "failing_deps": [r["node_id"] for r in dep_results if r["status"] != "CLEAN-PASS"],
        })
    scenario_pass_rate = (n_scen_pass / len(scenarios) * 100) if scenarios else None

    return {
        "stage_a_grounded_agreement_rate": {
            "value_percent": stage_a_grounded_agreement_rate,
            "n_demo_corpus_nodes_this_run": n_demo,
            "n_passing": n_stage_a_pass,
            "stage": "Stage A only",
            "numerator": "nodes where all 3 models returned grounded==true AND the LLM judge found semantic agreement",
            "denominator": "all demo-corpus nodes attempted this run",
            "basis": "does NOT require citation verification or a clean adversarial check -- purely: "
                     "did the 3 models derive the same rule from the cited text, independently.",
        },
        "citation_verification_rate": {
            "value_percent": citation_verification_rate,
            "n_demo_corpus_nodes_this_run": n_demo,
            "n_passing": n_citation_pass,
            "stage": "citation-check only",
            "numerator": "nodes where every cited source's quoted_text verified as a substring of the fetched page",
            "denominator": "all demo-corpus nodes attempted this run (null/not computed if --skip-citation-check)",
            "basis": "mechanical HTTP fetch + substring match, no model involved.",
        },
        "stage_b_parse_success_rate": {
            "value_percent": stage_b_parse_success_rate,
            "n_demo_corpus_nodes_this_run": n_demo,
            "n_passing": n_stage_b_pass,
            "stage": "Stage B only",
            "numerator": "nodes where the adversarial call returned parseable edge_cases (not truncated, not "
                         "empty, no error) -- even after the round-23/24 retry",
            "denominator": "all demo-corpus nodes attempted this run",
            "basis": "an infrastructure/reliability signal, not a gap-count -- a node can parse successfully "
                     "and still expose real gaps, or fail to parse and expose none we know of.",
        },
        "full_pipeline_clean_pass_rate": {
            "value_percent": full_pipeline_clean_pass_rate,
            "n_demo_corpus_nodes_this_run": n_demo,
            "n_passing": n_pass,
            "stage": "all three stages combined -- this is the renamed former 'grounded_agreement_rate' "
                     "(round 26; the old name was found to be mislabeled relative to its own definition, "
                     "see docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md S4's round-24 entry)",
            "numerator": "nodes with status == CLEAN-PASS",
            "denominator": "all demo-corpus nodes attempted this run",
            "basis": (
                "CLEAN-PASS = LLM-judged semantic agreement across all 3 grounded derivations AND no "
                "adversarial gap found AND the adversarial check itself parsed successfully (round 26 -- a "
                "Stage B parse failure no longer silently reads as \"no gaps\"). Citation verification was "
                "SKIPPED this run (--skip-citation-check, round 18 directive 2026-08-29) and is explicitly "
                "NOT part of this basis while skipped. Numeric fingerprint remains a secondary diagnostic "
                "only (round 3), not part of this basis either."
                if citation_check_skipped else
                "CLEAN-PASS = LLM-judged semantic agreement across all 3 grounded derivations AND all "
                "citations live-verified AND no adversarial gap found AND the adversarial check itself "
                "parsed successfully (round 26 -- a Stage B parse failure no longer silently reads as "
                "\"no gaps\", see spec S4). Numeric fingerprint is a secondary diagnostic only as of "
                "2026-08-26 round 3, not part of this basis either."
            ),
        },
        "grounded_agreement_rate": {
            "value_percent": full_pipeline_clean_pass_rate,
            "deprecated": True,
            "note": "Deprecated alias for full_pipeline_clean_pass_rate (round 26), kept only so anything "
                    "still reading this exact key doesn't break. This name was found to be mislabeled -- it "
                    "was never actually a Stage-A-only measure despite the name. Use "
                    "full_pipeline_clean_pass_rate (the honest name for the same number) or "
                    "stage_a_grounded_agreement_rate (genuinely Stage-A-only) going forward.",
        },
        "scenario_pass_rate": {
            "value_percent": scenario_pass_rate,
            "n_scenarios": len(scenarios),
            "n_passing": n_scen_pass,
            "scenarios": scenario_rows,
            "stage": "scenario level (depends on multiple nodes' CLEAN-PASS status)",
            "numerator": "concept-demo scenarios where every node_id they depend on is CLEAN-PASS this run",
            "denominator": "all concept-demo scenarios defined in the scenarios file",
            "basis": "a scenario passes iff every node_id it depends on is CLEAN-PASS in this same run",
        },
        "internal_gate_met": (
            full_pipeline_clean_pass_rate is not None and scenario_pass_rate is not None
            and full_pipeline_clean_pass_rate >= 90.0 and scenario_pass_rate >= 90.0
        ),
        "gate_threshold_percent": 90.0,
        "note": "Per the 2026-08-26 Concept Demo First directive S2: both rates must be >=90% before this "
                "demo corpus is shown to ANY audience, including Stage-1.5-style friendlies. This is an "
                "internal readiness gate computed by this script, not itself a claim to publish -- see "
                "spec S8's CONCEPT-DEMO claim-language row for what may actually be said in a showing. "
                "Round 26: added stage_a_grounded_agreement_rate, citation_verification_rate, and "
                "stage_b_parse_success_rate as separately-reported per-stage metrics (freeze item 1's "
                "reconciliation finding) -- grounded_agreement_rate is now full_pipeline_clean_pass_rate.",
    }


# -- Main -----------------------------------------------------------------------

CALIBRATION_FIXTURES_DIR = REPO_ROOT / "scripts" / "corroboration" / "calibration_fixtures"


def _get_nested(d, dotted_key):
    cur = d
    for part in dotted_key.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def run_replay_calibration(fixtures_dir: Path = None) -> bool:
    """Freeze items 2/3 (2026-08-31, round 26): runs the ENTIRE pipeline
    offline against a small, frozen, checked-in set of recorded fixtures --
    no keys, no network, no cost -- and asserts BOTH per-fixture node-level
    outcomes AND the aggregate demo-gate metrics against known-answer
    expected values.

    Mirrors the discipline documented at Open Question #11 in
    docs/OPEN_QUESTIONS_AND_LIMITATIONS.md ("a known-answer calibration
    suite proving the scorer reports correctly in every branch, including
    forced-disagreement and malformed-output cases") and its concrete
    implementation pattern in
    rules/validation/tests/test_ca_notice_scorer_outcome_fallback.py: real,
    individually-reviewable fixture files, one assertion per branch with a
    descriptive pass/fail line, no external test framework, exit non-zero
    on any failure.

    Each fixture is a real, checked-in JSON file (same {"nodes": [...]}
    shape discover_nodes() reads, plus "_replay" recorded-response data and
    an "_expected" known-answer block) under
    scripts/corroboration/calibration_fixtures/ -- outside rules/debt/, so
    these never get picked up by a real corpus run or the schema CI check,
    and are never mistaken for real rule content."""
    fixtures_dir = fixtures_dir or CALIBRATION_FIXTURES_DIR
    fixture_paths = (
        sorted(p for p in fixtures_dir.glob("*.json") if not p.name.startswith("_"))
        if fixtures_dir.exists() else []
    )
    if not fixture_paths:
        print(f"[replay] No calibration fixtures found under {fixtures_dir}. FAIL.")
        return False

    node_results = []
    fixture_all_ok = True
    print(f"[replay] Running {len(fixture_paths)} calibration fixture(s), fully offline "
          f"(no keys, no network, no cost)...\n")
    for fp in sorted(fixture_paths):
        fx = json.loads(fp.read_text())
        node = fx["nodes"][0]
        node_id = node.get("node_id")
        target = {"file": fp, "node": node, "node_id": node_id, "node_index": 0}
        result = run_node(target, keys=None, dry_run=False, skip_citation_check=False,
                           run_id="replay", replay_fixture=fx)
        node_results.append(result)

        exp = fx.get("_expected", {})
        checks = [
            ("status", result["status"], exp.get("status")),
            ("all_grounded", result["stage_a_grounded_derivation"]["all_grounded"], exp.get("all_grounded")),
            ("semantic_agreement", result["stage_a_grounded_derivation"]["semantic_agreement"], exp.get("semantic_agreement")),
            ("all_citations_verified", result["citation_check"]["all_verified"], exp.get("all_citations_verified")),
            ("gaps_found_count", len(result["stage_b_adversarial"]["gaps_found"]), exp.get("gaps_found_count")),
            ("stage_b_parsed_successfully", result["stage_b_adversarial"]["parsed_successfully"], exp.get("stage_b_parsed_successfully")),
        ]
        this_fixture_ok = True
        for label, actual, expected in checks:
            ok = actual == expected
            this_fixture_ok = this_fixture_ok and ok
            fixture_all_ok = fixture_all_ok and ok
            mark = "OK  " if ok else "FAIL"
            print(f"  {mark} [{fx.get('id', node_id)}] {label}: actual={actual!r} expected={expected!r}")
        fx_label = fx.get("id", node_id)
        fx_desc = fx.get("description", "")
        fx_verdict = "PASS" if this_fixture_ok else "FAIL"
        print(f"  {fx_verdict} -- {fx_label}: {fx_desc}\n")

    demo_gate = compute_demo_gate_metrics(node_results, demo_corpus_only=False,
                                           citation_check_skipped=False, force_include_all=True)

    # Round 26, Andy's addition: the calibration set gets known-answer
    # expected values for the METRICS themselves, not just per-fixture
    # pass/fail -- so compute_demo_gate_metrics() is regression-tested, not
    # just the pipeline stages feeding it.
    manifest_path = fixtures_dir / "_expected_metrics.json"
    metrics_all_ok = True
    if manifest_path.exists():
        expected_metrics = json.loads(manifest_path.read_text())
        print("[replay] Aggregate metric assertions:")
        for dotted_key, expected_value in expected_metrics.items():
            actual_value = _get_nested(demo_gate, dotted_key)
            ok = actual_value == expected_value
            metrics_all_ok = metrics_all_ok and ok
            print(f"  {'OK  ' if ok else 'FAIL'} {dotted_key}: actual={actual_value!r} expected={expected_value!r}")
        print()
    else:
        print(f"[replay] WARNING: no {manifest_path.name} found -- aggregate metrics not asserted this run.\n")
        metrics_all_ok = False

    overall_ok = fixture_all_ok and metrics_all_ok
    print(f"[replay] Result: {'PASS' if overall_ok else 'FAIL'} "
          f"({len(fixture_paths)} fixture(s), metric assertions {'PASS' if metrics_all_ok else 'FAIL'})")
    return overall_ok


def main():
    ap = argparse.ArgumentParser(description="Debt-track grounded-corroboration runner")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Synthetic responses, no keys, no network cost, no cost.")
    mode.add_argument("--live", action="store_true", help="Real API calls. Requires .env with real keys. Spends money.")
    mode.add_argument("--replay", action="store_true",
                       help="Round 26 (freeze item 2): runs the full pipeline offline against the frozen "
                            "calibration fixture set, no keys, no network, no cost, and asserts known-answer "
                            "expected outcomes for every fixture AND the aggregate metrics. Exits 1 on any "
                            "failure. Bypasses the normal corpus-discovery/budget-cap flow entirely.")
    ap.add_argument("--demo-corpus-only", action="store_true",
                     help="Restrict to federal + TX + CA (the concept-demo corpus). Recommended for the first live batch.")
    ap.add_argument("--nodes", type=str, default=None,
                     help="Comma-separated node_ids to restrict to (for spot-checking).")
    ap.add_argument("--budget-cap", type=float, default=DEFAULT_BUDGET_CAP_USD,
                     help=f"Hard USD cap for this run. Default ${DEFAULT_BUDGET_CAP_USD:.2f}.")
    ap.add_argument("--skip-citation-check", action="store_true",
                     help="Skip live citation verification (offline testing only).")
    args = ap.parse_args()

    if args.replay:
        ok = run_replay_calibration()
        sys.exit(0 if ok else 1)

    dry_run = args.dry_run
    only_node_ids = set(x.strip() for x in args.nodes.split(",")) if args.nodes else None

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    run_id = "run_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    print(f"[{run_id}] mode={'DRY-RUN' if dry_run else 'LIVE'} "
          f"demo_corpus_only={args.demo_corpus_only} budget_cap=${args.budget_cap:.2f}")

    targets = discover_nodes(args.demo_corpus_only, only_node_ids)
    if not targets:
        print("No DRAFT-tier nodes found matching the given filters. Nothing to do.")
        sys.exit(0)

    projected_total = APPROX_COST_PER_NODE_USD * len(targets)
    print(f"[{run_id}] {len(targets)} DRAFT node(s) queued. "
          f"Projected cost @ ${APPROX_COST_PER_NODE_USD:.2f}/node estimate: ${projected_total:.2f} "
          f"(ESTIMATE, not a guarantee -- see script header).")
    if args.skip_citation_check:
        print(f"[{run_id}] NOTE: citation verification SKIPPED this run (--skip-citation-check, round 18 "
              f"directive 2026-08-29). CLEAN-PASS reflects grounded-derivation + semantic-agreement + "
              f"adversarial-check evidence only -- NOT citation liveness. Deferred, not waived.")
    if not dry_run and projected_total > args.budget_cap:
        print(f"[{run_id}] STOPPING: projected cost ${projected_total:.2f} exceeds --budget-cap ${args.budget_cap:.2f}. "
              f"Re-run with a higher cap, --demo-corpus-only, or --nodes to scope down.")
        sys.exit(1)

    keys = None if dry_run else load_keys()

    node_results = []
    spent_estimate = 0.0
    for i, target in enumerate(targets, 1):
        if not dry_run and (spent_estimate + APPROX_COST_PER_NODE_USD) > args.budget_cap:
            print(f"[{run_id}] STOPPING before node {i}/{len(targets)} "
                  f"({target['node_id']}): would exceed --budget-cap ${args.budget_cap:.2f}. "
                  f"{i-1} node(s) completed this run; re-run to continue.")
            break
        print(f"[{run_id}] ({i}/{len(targets)}) {target['node_id']} ...", end=" ", flush=True)
        result = run_node(target, keys, dry_run, args.skip_citation_check, run_id)
        node_results.append(result)
        spent_estimate += APPROX_COST_PER_NODE_USD
        print(result["status"])

    demo_gate = compute_demo_gate_metrics(node_results, args.demo_corpus_only, args.skip_citation_check)

    summary = {
        "run_id": run_id,
        "mode": "dry-run" if dry_run else "live",
        "started": node_results[0]["started"] if node_results else now_iso(),
        "ended": now_iso(),
        "models": {"anthropic": ANTHROPIC_MODEL, "openai": OPENAI_MODEL, "gemini": GEMINI_MODEL},
        "demo_corpus_only": args.demo_corpus_only,
        "citation_check_skipped": args.skip_citation_check,
        "budget_cap_usd": args.budget_cap,
        "approx_cost_per_node_usd_estimate": APPROX_COST_PER_NODE_USD,
        "n_queued": len(targets),
        "n_completed": len(node_results),
        "n_clean_pass": sum(1 for r in node_results if r["status"] == "CLEAN-PASS"),
        "n_flagged": sum(1 for r in node_results if r["status"] == "FLAGGED"),
        "demo_gate_metrics": demo_gate,
        "node_results": node_results,
    }

    out_path = RUNS_DIR / f"{run_id}.json"
    out_path.write_text(json.dumps(summary, indent=2))
    print(f"\n[{run_id}] Done. {summary['n_clean_pass']}/{summary['n_completed']} clean-pass, "
          f"{summary['n_flagged']} flagged to docs/DEBT_DISAGREEMENT_QUEUE.md."
          + (" [citation verification SKIPPED this run]" if args.skip_citation_check else ""))
    print(f"[{run_id}] Full output: {out_path.relative_to(REPO_ROOT)}")
    if demo_gate:
        fpr = demo_gate["full_pipeline_clean_pass_rate"]["value_percent"]
        spr = demo_gate["scenario_pass_rate"]["value_percent"]
        sar = demo_gate["stage_a_grounded_agreement_rate"]["value_percent"]
        cvr = demo_gate["citation_verification_rate"]["value_percent"]
        sbr = demo_gate["stage_b_parse_success_rate"]["value_percent"]
        if fpr is not None and spr is not None:
            print(f"[{run_id}] Demo-gate metrics (round 26: reported per-stage, not one blended number) -- "
                  f"Stage A grounded-agreement: {sar:.1f}% | "
                  f"citation-verification: {'n/a (skipped)' if cvr is None else f'{cvr:.1f}%'} | "
                  f"Stage B parse-success: {sbr:.1f}% | "
                  f"full-pipeline clean-pass: {fpr:.1f}% (n={demo_gate['full_pipeline_clean_pass_rate']['n_demo_corpus_nodes_this_run']}) | "
                  f"scenario pass rate: {spr:.1f}% (n={demo_gate['scenario_pass_rate']['n_scenarios']}) | "
                  f"gate met (both >=90%): {demo_gate['internal_gate_met']}")
        else:
            print(f"[{run_id}] Demo-gate metrics: insufficient data this run (see {out_path.name})")


if __name__ == "__main__":
    main()
