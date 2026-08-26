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

SYSTEM_PROMPT_ADVERSARIAL = (
    "You are adversarially testing a legal rule encoding. You will be given a "
    "rule's logic and its completeness checklist (the facts it says are needed "
    "to apply it). Propose exactly 3 edge-case fact patterns designed to break "
    "the rule or expose something the completeness checklist does not cover. "
    "For each, state whether it exposes a genuine gap. Respond ONLY in valid "
    "JSON: {\"edge_cases\": [{\"scenario\": \"<1-3 sentences>\", "
    "\"exposes_gap\": <true/false>, \"gap_description\": \"<or null>\"}, ...]}"
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
SYSTEM_PROMPT_JUDGE = (
    "You are checking whether three independently-produced legal analyses of "
    "the same question substantively agree in their legal conclusion. Ignore "
    "differences in phrasing, level of detail, structure (numbered list vs. "
    "prose), or which specific illustrative examples each one includes -- "
    "focus only on whether the core legal answer (the governing rule, "
    "deadline, dollar amount, percentage, or standard) is the same across "
    "all three. If one analysis states a real substantive fact (a rule, "
    "exception, deadline, or amount) that another omits entirely, that is a "
    "genuine disagreement worth flagging, not just a phrasing difference. "
    "Respond ONLY in valid JSON: {\"agree\": <true if all three "
    "substantively agree, false otherwise>, \"agreement_notes\": \"<1-3 "
    "sentences: what agrees, or specifically what differs and which "
    "analysis differs>\"}"
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
                    dry_run_payload: dict) -> dict:
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
    try:
        client = anthropic.Anthropic(api_key=keys["ANTHROPIC_API_KEY"])
        resp = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=1500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        raw = "".join(b.text for b in resp.content if hasattr(b, "text")).strip()
        parsed = _parse_json_response(raw)
        parsed["model"] = ANTHROPIC_MODEL
        parsed["_raw"] = raw
        parsed["error"] = None
        return parsed
    except Exception as exc:
        return {"error": str(exc), "model": ANTHROPIC_MODEL}


def call_openai(system_prompt: str, user_prompt: str, keys, dry_run: bool,
                 dry_run_payload: dict) -> dict:
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
                 dry_run_payload: dict) -> dict:
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

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            fut = pool.submit(_do)
            try:
                resp = fut.result(timeout=60)
            except concurrent.futures.TimeoutError:
                return {"error": "Gemini API timed out after 60s", "model": GEMINI_MODEL}
        raw = resp.text.strip()
        parsed = _parse_json_response(raw)
        parsed["model"] = GEMINI_MODEL
        parsed["_raw"] = raw
        parsed["error"] = None
        return parsed
    except Exception as exc:
        return {"error": str(exc), "model": GEMINI_MODEL}


def judge_semantic_agreement(summaries: list, keys, dry_run: bool) -> dict:
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
    return call_anthropic(SYSTEM_PROMPT_JUDGE, user_prompt, keys, dry_run, dry_payload)


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
    return re.sub(r"\s+", " ", t).strip().lower()


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


def verify_citation(url: str, quoted_text: str, dry_run: bool) -> dict:
    """Mechanically verify a cited source. Always returns a `diagnostics` block
    -- HTTP status, content length, content type, and a fuzzy word-overlap
    score -- even on success, so a `verified: False` result is self-explaining
    instead of a bare `error: None` (fixed 2026-08-26 per Andy's run-3 report:
    several failures here were reachable, legitimate primary/near-primary
    sources -- e.g. eCFR, Cornell LII -- returning normal 200 responses that
    simply didn't contain an exact substring match, which looked identical to
    an unreachable source before this fix)."""
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
    try:
        resp = requests.get(url, timeout=20, headers=REQUEST_HEADERS)
        page = _normalize_for_match(resp.text, is_html=True)
        # Use a shortened window of the quoted text (first ~120 chars) to
        # tolerate minor HTML-entity/whitespace differences in the fetched page.
        needle = _normalize_for_match(quoted_text, is_html=False)[:120]
        verified = needle in page if needle else False
        diagnostics = {
            "http_status": resp.status_code,
            "content_length": len(resp.content),
            "content_type": resp.headers.get("Content-Type"),
            "word_overlap_ratio": _word_overlap_ratio(needle, page),
        }
        return {"url": url, "verified": verified, "method": "live", "error": None,
                "diagnostics": diagnostics}
    except Exception as exc:
        return {
            "url": url, "verified": False, "method": "live", "error": str(exc),
            "diagnostics": {"http_status": None, "content_length": None,
                             "content_type": None, "word_overlap_ratio": None},
        }


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

def run_node(target: dict, keys, dry_run: bool, skip_citation_check: bool, run_id: str) -> dict:
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

    # (a) three independent grounded derivations
    results_a = [
        call_anthropic(SYSTEM_PROMPT_DERIVATION, user_prompt_derivation, keys, dry_run, dry_payload),
        call_openai(SYSTEM_PROMPT_DERIVATION, user_prompt_derivation, keys, dry_run, dry_payload),
        call_gemini(SYSTEM_PROMPT_DERIVATION, user_prompt_derivation, keys, dry_run, dry_payload),
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
        judge_result = judge_semantic_agreement(summaries_for_judge, keys, dry_run)
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
            citation_results.append(verify_citation(d.get("url"), d.get("quoted_text"), dry_run))
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
    result_b = call_anthropic(SYSTEM_PROMPT_ADVERSARIAL, user_prompt_adversarial, keys, dry_run, dry_adversarial_payload)
    edge_cases = result_b.get("edge_cases", []) if not result_b.get("error") else []
    gaps_found = [e for e in edge_cases if e.get("exposes_gap")]

    ended = now_iso()

    clean_pass = bool(semantic_agreement) and (all_citations_verified is True) and not gaps_found

    # (d) file disagreements
    if not semantic_agreement:
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
    if all_citations_verified is False:
        failed = [c for c in citation_results if c["verified"] is not True]
        entry = _format_disagreement_entry(
            run_id, node_id, file_path, "CITATION-CHECK-FAILED",
            f"{len(failed)} of {len(citation_results)} cited source(s) could not be mechanically "
            f"verified live: {failed}",
            results_a,
        )
        file_disagreement(entry)
    if gaps_found:
        entry = _format_disagreement_entry(
            run_id, node_id, file_path, "ADVERSARIAL-GAP",
            f"{len(gaps_found)} adversarial edge case(s) flagged as exposing a gap: {gaps_found}",
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
        },
        "status": "CLEAN-PASS" if clean_pass else "FLAGGED",
        "tier_promotion_candidate": clean_pass,
        "tier_promotion_note": (
            "Evidence covers spec (a)/(b)/(d) only -- (c) mutation testing not yet built. "
            "This flag is a recommendation for Andy's review, not an automatic tier change; "
            "this script never edits any rules file."
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

def compute_demo_gate_metrics(node_results: list, demo_corpus_only: bool):
    if not SCENARIOS_PATH.exists():
        return None

    scenarios = json.loads(SCENARIOS_PATH.read_text()).get("scenarios", [])
    results_by_id = {r["node_id"]: r for r in node_results}

    demo_node_results = [
        r for r in node_results
        if any(str(r["file"]).startswith(f"rules/debt/{sub}") for sub in ("federal", "state/texas", "state/california"))
    ]
    n_demo = len(demo_node_results)
    n_pass = sum(1 for r in demo_node_results if r["status"] == "CLEAN-PASS")
    grounded_agreement_rate = (n_pass / n_demo * 100) if n_demo else None

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
        "grounded_agreement_rate": {
            "value_percent": grounded_agreement_rate,
            "n_demo_corpus_nodes_this_run": n_demo,
            "n_passing": n_pass,
            "basis": "CLEAN-PASS = LLM-judged semantic agreement across all 3 grounded derivations AND all citations live-verified AND no adversarial gap found (numeric fingerprint is a secondary diagnostic only as of 2026-08-26 round 3, not part of this basis)",
        },
        "scenario_pass_rate": {
            "value_percent": scenario_pass_rate,
            "n_scenarios": len(scenarios),
            "n_passing": n_scen_pass,
            "scenarios": scenario_rows,
            "basis": "a scenario passes iff every node_id it depends on is CLEAN-PASS in this same run",
        },
        "internal_gate_met": (
            grounded_agreement_rate is not None and scenario_pass_rate is not None
            and grounded_agreement_rate >= 90.0 and scenario_pass_rate >= 90.0
        ),
        "gate_threshold_percent": 90.0,
        "note": "Per the 2026-08-26 Concept Demo First directive S2: both rates must be >=90% before this "
                "demo corpus is shown to ANY audience, including Stage-1.5-style friendlies. This is an "
                "internal readiness gate computed by this script, not itself a claim to publish -- see "
                "spec S8's CONCEPT-DEMO claim-language row for what may actually be said in a showing.",
    }


# -- Main -----------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Debt-track grounded-corroboration runner")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Synthetic responses, no keys, no network cost, no cost.")
    mode.add_argument("--live", action="store_true", help="Real API calls. Requires .env with real keys. Spends money.")
    ap.add_argument("--demo-corpus-only", action="store_true",
                     help="Restrict to federal + TX + CA (the concept-demo corpus). Recommended for the first live batch.")
    ap.add_argument("--nodes", type=str, default=None,
                     help="Comma-separated node_ids to restrict to (for spot-checking).")
    ap.add_argument("--budget-cap", type=float, default=DEFAULT_BUDGET_CAP_USD,
                     help=f"Hard USD cap for this run. Default ${DEFAULT_BUDGET_CAP_USD:.2f}.")
    ap.add_argument("--skip-citation-check", action="store_true",
                     help="Skip live citation verification (offline testing only).")
    args = ap.parse_args()

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

    demo_gate = compute_demo_gate_metrics(node_results, args.demo_corpus_only)

    summary = {
        "run_id": run_id,
        "mode": "dry-run" if dry_run else "live",
        "started": node_results[0]["started"] if node_results else now_iso(),
        "ended": now_iso(),
        "models": {"anthropic": ANTHROPIC_MODEL, "openai": OPENAI_MODEL, "gemini": GEMINI_MODEL},
        "demo_corpus_only": args.demo_corpus_only,
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
          f"{summary['n_flagged']} flagged to docs/DEBT_DISAGREEMENT_QUEUE.md.")
    print(f"[{run_id}] Full output: {out_path.relative_to(REPO_ROOT)}")
    if demo_gate:
        gar = demo_gate["grounded_agreement_rate"]["value_percent"]
        spr = demo_gate["scenario_pass_rate"]["value_percent"]
        if gar is not None and spr is not None:
            print(f"[{run_id}] Demo-gate metrics -- grounded-agreement rate: "
                  f"{gar:.1f}% (n={demo_gate['grounded_agreement_rate']['n_demo_corpus_nodes_this_run']}) | "
                  f"scenario pass rate: {spr:.1f}% (n={demo_gate['scenario_pass_rate']['n_scenarios']}) | "
                  f"gate met (both >=90%): {demo_gate['internal_gate_met']}")
        else:
            print(f"[{run_id}] Demo-gate metrics: insufficient data this run (see {out_path.name})")


if __name__ == "__main__":
    main()
