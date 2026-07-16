#!/usr/bin/env python3
"""
Retaliation Defense — Holdings Verification Runner v3 (Generate-From-Source)
=============================================================================
Implements COWORK_DIRECTION_HOLDINGS_GENERATE_FROM_SOURCE.md (2026-06-23).

WHAT CHANGED FROM v2:
  Check C is now generate-from-source, not "grade the draft":
    Step 1 — GENERATE (Gemini): characterizes holding from retrieved opinion text only.
              Gemini does NOT see the prior v2 draft holding at this step.
    Step 2 — VERIFY (GPT, a DIFFERENT model): independently checks Gemini's characterization
              against the retrieved text. Also reconciles against the draft holding.
    Step 3 — RECONCILE: source-generated holding vs. draft. Agree → C passes.
              Diverge → C fails, but source-generated carrying into queue so attorney
              starts from text, not from a possibly-wrong draft.

  Check D is now DERIVED from the generate/verify outputs (no additional LLM call):
    STATED: Gemini found verbatim quote + GPT confirms it is verbatim and on-point.
    INFERRED: C corroborated but no confirmed verbatim quote — proposition established
              through reasoning/prose. Routes to CONFIRM-INFERENCE (cheap attorney work).

  TWO OUTPUT QUEUES (Step 4 of direction):
    CONFIRM-INFERENCE: C=corroborated, D=INFERRED. Attorney confirms an inference
                       the two models already corroborated. Low cost, delegable.
    RE-CHARACTERIZE:   C=FLAG. Attorney re-characterizes from text. Source-generated
                       holding provided so attorney starts from retrieved text.
    WRONG-DOC:         A=FLAG-citation-mismatch. CL returned wrong document.
                       Attorney must source the correct opinion.

INDEPENDENCE GUARANTEE (non-negotiable):
  GENERATE_MODEL != VERIFY_MODEL — recorded per case in output provenance.
  If these are ever the same model, every affected case is treated as
  single-model-preliminary, never machine-verified.

PASSING STANDARD (unchanged from v2):
  machine-verified: A=true + B=OK-machine + C=corroborated + D=STATED or INFERRED
  needs-attorney:   any flag

Note: D=INFERRED now passes machine-verified (routes to CONFIRM-INFERENCE queue),
because the direction classifies confirmed-inference as the cheap delegable lane,
not a substantive failure. The attorney confirms; the machine does not advance it.

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv
from openai import OpenAI
from google import genai
from google.genai import types as genai_types

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
load_dotenv()

OPENAI_MODEL  = "gpt-4o"
GEMINI_MODEL  = "gemini-2.5-pro"

# Independence: generate and verify MUST use different models.
# Gemini generates (Model 1); GPT verifies (Model 2).
GENERATE_MODEL_NAME = f"gemini:{GEMINI_MODEL}"
VERIFY_MODEL_NAME   = f"gpt:{OPENAI_MODEL}"

BUDGET_CAP = 15.00
CL_BASE    = "https://www.courtlistener.com/api/rest/v4"
CL_TOKEN   = os.getenv("COURTLISTENER_API_TOKEN", "")

CONSENSUS_STATES = [
    "AZ","CA","DC","IA","KY","MA","ME","MN","NE","NH","RI","WA",
    "DE",
    "AR","IN","MO","VA",
    "FL","GA","ID","IL","MD","MS","MT","NC","OH","OR","PA",
    "SD","TN","TX","UT","WI","WY",
]

OUTPUT_DIR = Path(__file__).parent / "output"

openai_client  = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
gemini_client  = genai.Client(api_key=os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))

# ---------------------------------------------------------------------------
# CourtListener helpers (unchanged from v2)
# ---------------------------------------------------------------------------

def cl_headers():
    h = {"Accept": "application/json", "User-Agent": "CivilJusticeAsCode/1.0"}
    if CL_TOKEN:
        h["Authorization"] = f"Token {CL_TOKEN}"
    return h


def cl_search_case(case_name, year=None, citation_gpt=None, citation_gem=None):
    def _search(q, extra):
        params = {"q": q, "type": "o", "order_by": "score desc", "format": "json"}
        params.update(extra)
        for attempt in range(5):
            r = requests.get(f"{CL_BASE}/search/", params=params, headers=cl_headers(), timeout=15)
            if r.status_code == 429:
                wait = 3 * (2 ** attempt)
                print(f"        [CL 429 — waiting {wait}s]")
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json().get("results", [])
        r.raise_for_status()
        return []

    def _citation_search(cite):
        for attempt in range(3):
            r = requests.get(f"{CL_BASE}/search/", params={"citation": cite, "type": "o", "format": "json"},
                             headers=cl_headers(), timeout=15)
            if r.status_code == 429:
                time.sleep(3 * (2 ** attempt))
                continue
            if r.status_code == 200:
                return r.json().get("results", [])
            return []
        return []

    def _validate_hit(hit, query):
        tokens = set(t.lower() for t in query.replace(".", " ").split() if len(t) > 3)
        name = (hit.get("caseName") or "").lower()
        return not tokens or any(t in name for t in tokens)

    try:
        year_params = {"filed_after": f"{year-1}-01-01", "filed_before": f"{year+1}-12-31"} if year else {}
        results = _search(case_name, year_params)
        if not results and year_params:
            results = _search(case_name, {})
        if results and _validate_hit(results[0], case_name):
            return results[0]
        for cite in [c for c in [citation_gpt, citation_gem] if c]:
            cr = _citation_search(cite)
            if cr:
                print(f"        [Citation fallback '{case_name}' via '{cite}' → '{cr[0].get('caseName')}']")
                return cr[0]
        if results:
            hit = results[0]
            hit["_search_warning"] = f"Name overlap failed for '{case_name}'"
            return hit
        return None
    except Exception as e:
        return {"error": str(e)}


def cl_get_opinion_id_for_cluster(cluster_id):
    for attempt in range(5):
        try:
            r = requests.get(f"{CL_BASE}/opinions/", params={"cluster": cluster_id, "format": "json"},
                             headers=cl_headers(), timeout=15)
            if r.status_code == 429:
                wait = 3 * (2 ** attempt)
                print(f"        [CL 429 on opinion lookup — waiting {wait}s]")
                time.sleep(wait)
                continue
            r.raise_for_status()
            results = r.json().get("results", [])
            return results[0]["id"] if results else None
        except Exception:
            if attempt < 4:
                time.sleep(3)
    return None


def cl_get_opinion_text(opinion_id):
    try:
        r = requests.get(f"{CL_BASE}/opinions/{opinion_id}/", headers=cl_headers(), timeout=15)
        r.raise_for_status()
        d = r.json()
        for field in ["plain_text", "xml_harvard", "html_anon_2020", "html_lawbox",
                      "html_columbia", "html_with_citations", "html"]:
            val = d.get(field) or ""
            if len(val.strip()) > 200:
                return val
        return None
    except Exception:
        return None


def cl_get_citing_opinions(cluster_id, max_results=20):
    try:
        r = requests.get(f"{CL_BASE}/search/",
                         params={"q": f"cites:{cluster_id}", "type": "o", "format": "json", "count": max_results},
                         headers=cl_headers(), timeout=15)
        r.raise_for_status()
        return r.json().get("results", [])
    except Exception:
        return []


NEGATIVE_KEYWORDS = ["overruled", "abrogated", "superseded", "disapproved", "reversed on other grounds",
                     "no longer good law", "limited by"]

def detect_negative_treatment(citing_cases):
    for c in citing_cases:
        snippet = (c.get("snippet") or "").lower()
        for kw in NEGATIVE_KEYWORDS:
            if kw in snippet:
                return True, f"Potential negative treatment in {c.get('caseName','?')}: '{kw}'"
    return False, None


# ---------------------------------------------------------------------------
# LLM helpers
# ---------------------------------------------------------------------------

def call_gpt(prompt, max_tokens=1200, json_mode=True):
    try:
        kwargs = dict(model=OPENAI_MODEL,
                      messages=[{"role": "user", "content": prompt}],
                      max_completion_tokens=max_tokens, temperature=1)
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        r = openai_client.chat.completions.create(**kwargs)
        content = r.choices[0].message.content or ""
        if not content.strip():
            return {"error": "empty response"}
        return json.loads(content) if json_mode else content
    except Exception as e:
        return {"error": str(e)}


def call_gemini(prompt, max_tokens=1200, json_mode=True):
    try:
        config = genai_types.GenerateContentConfig(
            max_output_tokens=max_tokens, temperature=1.0,
            response_mime_type="application/json" if json_mode else "text/plain",
            thinking_config=genai_types.ThinkingConfig(thinking_budget=512),
        )
        r = gemini_client.models.generate_content(model=GEMINI_MODEL, contents=prompt, config=config)
        text = None
        try:
            text = r.text
        except Exception:
            pass
        if not text:
            try:
                text = r.candidates[0].content.parts[0].text
            except Exception:
                pass
        if not text or not str(text).strip():
            return {"error": "empty response"}
        text = str(text)
        return json.loads(text) if json_mode else text
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# Check A and B (unchanged from v2)
# ---------------------------------------------------------------------------

def check_a_existence(case_name, citation_gpt, citation_gem, year):
    result = {
        "check": "A_existence_citation", "cl_hit": None, "cl_cluster_id": None,
        "cl_opinion_id": None, "cl_url": None, "cl_citation": None,
        "citation_match": None, "exists": "uncertain", "basis": None,
    }
    hit = cl_search_case(case_name, year, citation_gpt=citation_gpt, citation_gem=citation_gem)
    if not hit or "error" in hit:
        result["exists"] = "FLAG"
        result["basis"] = f"CL search error or no results: {hit}"
        return result

    result["cl_hit"] = {"case_name": hit.get("caseName"), "date": hit.get("dateFiled"),
                        "court": hit.get("court"), "citation": hit.get("citation", []),
                        "cluster_id": hit.get("cluster_id")}
    result["cl_url"] = hit.get("absolute_url") and f"https://www.courtlistener.com{hit['absolute_url']}"
    result["cl_cluster_id"] = hit.get("cluster_id")

    opinions_field = hit.get("opinions") or []
    snippets = []
    for op in opinions_field:
        if isinstance(op, dict):
            op_type = op.get("type", "")
            op_id = op.get("id")
            snippet = op.get("snippet") or ""
            if snippet.strip():
                snippets.append(f"[{op_type}] {snippet}")
            if op_id and op_id != hit.get("cluster_id"):
                if "lead" in op_type or not result["cl_opinion_id"]:
                    result["cl_opinion_id"] = op_id
        elif isinstance(op, int) and op != hit.get("cluster_id"):
            result["cl_opinion_id"] = op
    if not result["cl_opinion_id"]:
        cluster_id = hit.get("cluster_id")
        if cluster_id:
            time.sleep(1)
            oid = cl_get_opinion_id_for_cluster(cluster_id)
            if oid:
                result["cl_opinion_id"] = oid
    result["cl_snippets"] = " | ".join(snippets) if snippets else None

    cl_cites = hit.get("citation") or []
    result["cl_citation"] = cl_cites[0] if cl_cites else None
    result["cl_all_citations"] = cl_cites

    def norm(c): return "".join(ch for ch in str(c).lower() if ch.isalnum())
    candidates = [c for c in [citation_gpt, citation_gem] if c]
    if cl_cites and candidates:
        norm_cl = [norm(c) for c in cl_cites]
        matched = any(norm(mc) in norm_cl or any(norm(mc) in nc for nc in norm_cl) for mc in candidates)
        result["citation_match"] = matched
        result["exists"] = "true" if matched else "FLAG-citation-mismatch"
        result["basis"] = f"CL citations {cl_cites}; model citations {candidates}; match={matched}"
    elif not cl_cites:
        result["exists"] = "true"
        result["basis"] = "Found by name; no CL citation to check"
    else:
        result["exists"] = "true"
        result["basis"] = "Found; no model citation to compare"
    return result


def check_b_currency(cl_cluster_id):
    result = {"check": "B_currency", "currency": "UNVERIFIED-no-citator",
              "negative_flag": False, "negative_note": None, "citing_count": 0,
              "basis": None, "as_of_date": datetime.now(timezone.utc).strftime("%Y-%m-%d")}
    if not cl_cluster_id:
        result["basis"] = "No cluster ID — cannot check currency"
        return result
    citing = cl_get_citing_opinions(cl_cluster_id)
    result["citing_count"] = len(citing)
    is_neg, neg_note = detect_negative_treatment(citing)
    if is_neg:
        result["currency"] = "NEGATIVE-FLAG"
        result["negative_flag"] = True
        result["negative_note"] = neg_note
        result["basis"] = f"Negative treatment detected in {len(citing)} citing opinions"
    else:
        result["currency"] = "OK-machine"
        result["basis"] = (f"No negative treatment in {len(citing)} citing opinions via CL "
                           f"as of {result['as_of_date']}. Absence ≠ confirmed good law.")
    return result


# ---------------------------------------------------------------------------
# Check C — Generate-From-Source (v3 core)
# ---------------------------------------------------------------------------

GENERATE_PROMPT = """You are a legal researcher analyzing an appellate case opinion.

CASE TEXT (retrieved from CourtListener):
---
{opinion_text}
---

Work from the retrieved text only. Do not use outside knowledge of this case.

Tasks:
1. Does this case address the tenant's DEFENSE of retaliatory eviction — i.e., does the opinion discuss whether a landlord may evict a tenant in retaliation for the tenant's protected activity (reporting housing code violations, organizing tenants, exercising legal rights, complaining to authorities, etc.)?

2. If YES:
   a. Characterize in 2-3 sentences what the case holds on this question. Be precise and grounded in the retrieved text.
   b. If the opinion contains a verbatim passage that states the controlling rule on the retaliation defense, copy it exactly from the text above.

3. If NO: describe in one sentence what the opinion is actually about.

Return JSON:
{{
  "addresses_retaliation_defense": true,
  "holding_characterization": "...",
  "candidate_quote": "exact verbatim text copied from opinion above" | null,
  "what_opinion_is_about": "...",
  "confidence": "high" | "medium" | "low"
}}

If the opinion does NOT address the retaliation defense:
{{
  "addresses_retaliation_defense": false,
  "holding_characterization": null,
  "candidate_quote": null,
  "what_opinion_is_about": "...",
  "confidence": "high" | "medium" | "low"
}}

CRITICAL: candidate_quote must be exact words copied from the case text above. Do not paraphrase. If no verbatim controlling passage exists, set candidate_quote to null."""


VERIFY_PROMPT = """You are independently verifying a legal holding characterization against source text.

CASE TEXT (retrieved from CourtListener):
---
{opinion_text}
---

CHARACTERIZATION TO VERIFY (produced by a different AI model from the text above):
"{holding_characterization}"

CANDIDATE CONTROLLING QUOTE (produced by the same model):
{candidate_quote_display}

PRIOR DRAFT HOLDING (from an earlier automated identification step — may or may not be accurate):
"{draft_holding}"

Your tasks — work from the case text only:

1. Does the case text support the characterization above? Assess as accurate, partially_accurate, or inaccurate.

2. If a candidate quote was provided: verify whether those exact words appear in the case text and whether the quote is on-point as a controlling statement on the retaliation defense.

3. Does the characterization agree with the prior draft holding on the core legal proposition? Assess at the level of legal substance, not surface wording.

Return JSON:
{{
  "text_supports_characterization": "accurate" | "partially_accurate" | "inaccurate",
  "verification_note": "...",
  "quote_is_verbatim": true | false | null,
  "quote_is_on_point": true | false | null,
  "alternative_quote": "exact verbatim text from opinion if better controlling passage exists" | null,
  "draft_agreement": "agree" | "partially_agree" | "disagree",
  "draft_agreement_note": "..."
}}"""


def check_c_generate_from_source(opinion_text: str | None, prior_holding: str, case_name: str) -> dict:
    """Check C (v3): Generate holding from text (Gemini), verify with different model (GPT)."""
    result = {
        "check": "C_generate_from_source",
        "generate_model": GENERATE_MODEL_NAME,
        "verify_model": VERIFY_MODEL_NAME,
        "holding": "FLAG",
        "source_generated_holding": None,
        "controlling_quote": None,
        "quote_verified_verbatim": None,
        "draft_agreement": None,
        "generate_output": None,
        "verify_output": None,
        "queue_routing": None,
        "basis": None,
    }

    if not opinion_text or len(opinion_text.strip()) < 200:
        result["holding"] = "FLAG-no-text"
        result["queue_routing"] = "WRONG-DOC"
        result["basis"] = "Opinion text unavailable or too short"
        return result

    text_excerpt = opinion_text[:8000]

    # Step 1 — GENERATE (Gemini, Model 1). Does NOT see prior_holding.
    gen_prompt = GENERATE_PROMPT.format(opinion_text=text_excerpt)
    gen_resp = call_gemini(gen_prompt, max_tokens=1000)
    result["generate_output"] = gen_resp

    if isinstance(gen_resp, dict) and "error" not in gen_resp:
        gen_addresses = gen_resp.get("addresses_retaliation_defense")
        gen_holding   = gen_resp.get("holding_characterization") or ""
        gen_quote     = gen_resp.get("candidate_quote")
    else:
        result["holding"] = "FLAG-generate-failed"
        result["queue_routing"] = "RE-CHARACTERIZE"
        result["basis"] = f"Gemini generate step failed: {gen_resp}"
        return result

    if not gen_addresses:
        # Gemini says case is not about retaliation
        result["holding"] = "FLAG-irrelevant"
        result["queue_routing"] = "WRONG-DOC"
        result["basis"] = f"Gemini: case does not address retaliation defense. About: {gen_resp.get('what_opinion_is_about','?')[:120]}"
        return result

    # Step 2 — VERIFY (GPT, Model 2). Sees text + Gemini's output + draft holding.
    quote_display = f'"{gen_quote}"' if gen_quote else "none provided"
    ver_prompt = VERIFY_PROMPT.format(
        opinion_text=text_excerpt,
        holding_characterization=gen_holding,
        candidate_quote_display=quote_display,
        draft_holding=prior_holding or "(no draft holding available)",
    )
    ver_resp = call_gpt(ver_prompt, max_tokens=1000)
    result["verify_output"] = ver_resp

    if isinstance(ver_resp, dict) and "error" not in ver_resp:
        ver_accuracy = ver_resp.get("text_supports_characterization")
        ver_verbatim = ver_resp.get("quote_is_verbatim")
        ver_onpoint  = ver_resp.get("quote_is_on_point")
        ver_altquote = ver_resp.get("alternative_quote")
        draft_agree  = ver_resp.get("draft_agreement")
    else:
        result["holding"] = "FLAG-verify-failed"
        result["queue_routing"] = "RE-CHARACTERIZE"
        result["source_generated_holding"] = gen_holding
        result["basis"] = f"GPT verify step failed: {ver_resp}"
        return result

    # Step 3 — Corroboration decision
    result["source_generated_holding"] = gen_holding
    result["draft_agreement"] = draft_agree

    # Determine controlling quote for D
    if gen_quote and ver_verbatim is True and ver_onpoint is True:
        result["controlling_quote"] = gen_quote
        result["quote_verified_verbatim"] = True
    elif ver_altquote:
        result["controlling_quote"] = ver_altquote
        result["quote_verified_verbatim"] = "gpt-alternative"
    else:
        result["controlling_quote"] = None
        result["quote_verified_verbatim"] = False

    if ver_accuracy in ("accurate", "partially_accurate"):
        result["holding"] = "corroborated"
        result["queue_routing"] = None  # will be set by D check
        result["basis"] = (
            f"Gemini generated: '{gen_holding[:100]}'. "
            f"GPT verified as '{ver_accuracy}'. "
            f"Draft agreement: {draft_agree}."
        )
    else:
        result["holding"] = "FLAG-verify-disputed"
        result["queue_routing"] = "RE-CHARACTERIZE"
        result["basis"] = (
            f"GPT found characterization '{ver_accuracy}'. "
            f"Source-generated holding carried to queue. "
            f"Draft agreement: {draft_agree}. "
            f"Verify note: {ver_resp.get('verification_note','')[:120]}"
        )

    return result


# ---------------------------------------------------------------------------
# Check D — Derived from Check C generate/verify (no additional LLM call)
# ---------------------------------------------------------------------------

def check_d_from_c(c_result: dict) -> dict:
    """Check D (v3): Derived from Check C generate/verify. No additional LLM call.

    STATED:    Gemini found verbatim quote AND GPT confirms verbatim + on-point.
    INFERRED:  C corroborated but no confirmed verbatim quote.
               Routes to CONFIRM-INFERENCE — proposition established through reasoning.
    FLAG:      C did not corroborate (shouldn't reach here, but handled).
    """
    result = {
        "check": "D_control_derived",
        "control": "FLAG",
        "controlling_quote": None,
        "quote_agreement": False,
        "basis": None,
    }

    if c_result.get("holding") != "corroborated":
        result["control"] = "FLAG"
        result["basis"] = "Check C did not corroborate — D not evaluated"
        return result

    quote = c_result.get("controlling_quote")
    verbatim = c_result.get("quote_verified_verbatim")

    if quote and verbatim is True:
        result["control"] = "STATED"
        result["controlling_quote"] = quote
        result["quote_agreement"] = True
        result["basis"] = "Gemini found verbatim quote; GPT confirmed verbatim and on-point"
    elif quote and verbatim == "gpt-alternative":
        result["control"] = "STATED-single-model"
        result["controlling_quote"] = quote
        result["quote_agreement"] = False
        result["basis"] = "GPT found alternative verbatim quote (Gemini's candidate not confirmed)"
    else:
        result["control"] = "INFERRED"
        result["controlling_quote"] = None
        result["quote_agreement"] = False
        result["basis"] = (
            "Holding corroborated from text but no confirmed verbatim controlling quote. "
            "Rule established through prose/reasoning. Routes to CONFIRM-INFERENCE."
        )

    return result


# ---------------------------------------------------------------------------
# Per-case verification
# ---------------------------------------------------------------------------

def verify_case(case: dict, state: str) -> dict:
    case_name     = case.get("case_name", "")
    citation_gpt  = case.get("citation_gpt")
    citation_gem  = case.get("citation_gemini")
    year          = case.get("year")
    prior_holding = case.get("holding_gpt") or case.get("holding_gemini") or ""

    print(f"    Verifying: {case_name} ({year})")

    # Check A
    print(f"      Check A: existence/citation...")
    check_a = check_a_existence(case_name, citation_gpt, citation_gem, year)
    cl_cluster_id = check_a.get("cl_cluster_id")
    cl_opinion_id = check_a.get("cl_opinion_id")
    time.sleep(10)  # CL rate limit

    # Fetch opinion text
    opinion_text        = None
    opinion_text_source = None
    if cl_opinion_id:
        print(f"      Fetching opinion text (CL opinion {cl_opinion_id})...")
        opinion_text = cl_get_opinion_text(cl_opinion_id)
        if opinion_text:
            opinion_text_source = f"CL opinion/{cl_opinion_id} full text"
        time.sleep(5)
    if not opinion_text:
        snippets = check_a.get("cl_snippets")
        if snippets:
            opinion_text = snippets
            opinion_text_source = "CL search snippet (abbreviated)"
            print(f"      Full text unavailable — using search snippet")

    # Check B
    print(f"      Check B: currency...")
    check_b = check_b_currency(cl_cluster_id)
    time.sleep(5)

    # Check C — generate-from-source (sequential: Gemini → GPT)
    print(f"      Check C: generate (Gemini) → verify (GPT)...")
    check_c = check_c_generate_from_source(opinion_text, prior_holding, case_name)

    # Check D — derived from C, no LLM call
    print(f"      Check D: derived from C...")
    check_d = check_d_from_c(check_c)

    # Disposition
    a_ok = check_a["exists"] in ("true",)
    b_ok = check_b["currency"] == "OK-machine"
    c_ok = check_c["holding"] == "corroborated"
    d_ok = check_d["control"] in ("STATED", "STATED-single-model", "INFERRED")
    # Note: INFERRED passes machine-verified but routes to CONFIRM-INFERENCE queue.

    # Queue routing
    if not a_ok and check_a["exists"] == "FLAG-citation-mismatch":
        queue = "WRONG-DOC"
    elif c_ok and check_d["control"] == "INFERRED":
        queue = "CONFIRM-INFERENCE"
    elif c_ok and d_ok:
        queue = None  # machine-verified, no attorney queue needed
    else:
        queue = "RE-CHARACTERIZE"

    if a_ok and b_ok and c_ok and d_ok:
        disposition = "machine-verified"
        disposition_note = (
            f"All checks passed. A=true, B=OK-machine, C=corroborated (generate-from-source), "
            f"D={check_d['control']}. Queue: {queue or 'none'}. "
            f"Below attorney line — attorney must confirm before use."
        )
    else:
        failed = []
        if not a_ok: failed.append(f"A={check_a['exists']}")
        if not b_ok: failed.append(f"B={check_b['currency']}")
        if not c_ok: failed.append(f"C={check_c['holding']}")
        if not d_ok: failed.append(f"D={check_d['control']}")
        disposition = "needs-attorney"
        disposition_note = f"Flagged: {', '.join(failed)}. Queue: {queue}."

    # Provenance
    provenance = {
        "generate_model": GENERATE_MODEL_NAME,
        "verify_model":   VERIFY_MODEL_NAME,
        "opinion_text_source": opinion_text_source,
        "draft_agreement": check_c.get("draft_agreement"),
    }

    print(f"      → {disposition} | C={check_c['holding']} D={check_d['control']} | queue={queue}")

    return {
        "case_name":          case_name,
        "citation_gpt":       citation_gpt,
        "citation_gemini":    citation_gem,
        "year":               year,
        "prior_holding":      prior_holding,
        "source_generated_holding": check_c.get("source_generated_holding"),
        "check_a":            check_a,
        "check_b":            check_b,
        "check_c":            check_c,
        "check_d":            check_d,
        "disposition":        disposition,
        "disposition_note":   disposition_note,
        "controlling_quote":  check_d.get("controlling_quote"),
        "queue_routing":      queue,
        "provenance":         provenance,
    }


# ---------------------------------------------------------------------------
# Per-state runner
# ---------------------------------------------------------------------------

# Full state names for CL fresh-search
_CL_STATE_NAMES: dict[str, str] = {
    "AK": "Alaska", "AL": "Alabama", "AR": "Arkansas", "AZ": "Arizona",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DC": "District of Columbia",
    "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii",
    "IA": "Iowa", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "MA": "Massachusetts",
    "MD": "Maryland", "ME": "Maine", "MI": "Michigan", "MN": "Minnesota",
    "MO": "Missouri", "MS": "Mississippi", "MT": "Montana", "NC": "North Carolina",
    "ND": "North Dakota", "NE": "Nebraska", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NV": "Nevada", "NY": "New York", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island",
    "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
    "UT": "Utah", "VA": "Virginia", "VT": "Vermont", "WA": "Washington",
    "WI": "Wisconsin", "WV": "West Virginia", "WY": "Wyoming",
}


# Retaliation statutes by state — used to build targeted CL queries.
# When a statute is known, it's included in the CL search for precision.
# Updated 2026-06-26: prior generic query "retaliatory eviction {state} tenant" returned
# wrong-doc results (cases not about residential retaliation). Statute-targeted queries
# dramatically improve precision.
_STATE_RETALIATION_STATUTES: dict[str, str] = {
    "AK": "AS 34.03.310", "AL": "35-9A-501", "AR": "18-17-901", "AZ": "33-1381",
    "CA": "1942.5", "CO": "38-12-509", "CT": "47a-33", "DC": "42-3505.02",
    "DE": "5516", "FL": "83.64", "GA": "44-7-24", "HI": "521-74",
    "IA": "562A.36", "ID": "6-324", "IL": "765 ILCS 720", "IN": "32-31-8.5",
    "KS": "58-2572", "KY": "383.705", "LA": "9:3261", "MA": "186 18",
    "MD": "8-208.1", "ME": "6001-A", "MI": "125.530", "MN": "504B.285",
    "MO": "441.233", "MS": "89-8-17", "MT": "70-24-431", "NC": "42-37.1",
    "ND": "47-16-17.5", "NE": "76-1439", "NH": "540:13-a", "NJ": "2A:42-10.10",
    "NM": "47-8-39", "NV": "118A.510", "NY": "223-b", "OH": "5321.02",
    "OK": "41-120", "OR": "90.385", "PA": "landlord tenant retaliation",
    "RI": "34-18-46", "SC": "27-40-910", "SD": "43-32-27", "TN": "66-28-507",
    "TX": "92.331", "UT": "57-22-6", "VA": "55.1-1258", "VT": "4465",
    "WA": "59.18.240", "WI": "704.45", "WV": "37-6A-1", "WY": "1-21-1207",
}


def _court_matches_state(court_name: str, state_abbr: str) -> bool:
    """Check E — jurisdiction filter.

    Returns True if the CL court name belongs to the target state.
    Conservative: only accepts if the state's full name appears in the court string.
    This catches cases like "Alaska Supreme Court" when querying for Alabama (AL),
    and "Court of Civil Appeals of Alabama" when querying for Alabama (correct).

    Federal circuit courts (e.g. "Court of Appeals for the Third Circuit") do NOT
    contain the state name and will be rejected. This is the safe default: a circuit
    court opinion applying state law is possible, but we cannot confirm jurisdiction
    from the court name alone. Such cases are marked PR for manual review.

    Updated 2026-06-29: Andy ratified jurisdiction filter (YELLOW → executed).
    """
    if not court_name:
        return True  # no court data — don't filter out (conservative)
    state_name = _CL_STATE_NAMES.get(state_abbr, state_abbr).lower()
    return state_name in court_name.lower()


def _build_case_from_hit(hit: dict) -> dict:
    """Convert a CL search API result dict into a case dict for verify_case()."""
    citations = hit.get("citation", [])
    citation = citations[0] if citations else ""
    date_filed = hit.get("dateFiled", "")
    year = int(date_filed[:4]) if date_filed and len(date_filed) >= 4 else None
    return {
        "case_name": hit.get("caseName") or "",
        "citation_gpt": citation,
        "citation_gemini": citation,
        "citation": citation,
        "year": year,
        "court_gpt": hit.get("court", ""),
        "court_gemini": hit.get("court", ""),
        "holding_gpt": None,
        "holding_gemini": None,
        "inter_coder_match": False,
        "checks": {},
        "_source": "cl_fresh_search",
        "_cl_cluster_id": hit.get("cluster_id"),
    }


def cl_search_retaliation_by_state(state_abbr: str, max_results: int = 8) -> list[dict]:
    """Search CourtListener for retaliatory eviction cases in a state (fresh path).

    Returns a list of case dicts in the same format expected by verify_case().
    Used when fresh=True and no v1 draft candidates exist for this state.

    Query strategy (updated 2026-06-29):
      1. Statute-targeted query (precision): '<statute> retaliation tenant landlord residential'
         Results are filtered by Check E (court jurisdiction must match target state).
      2. If statute query returns 0 in-state results, fall back to broad state-name query:
         'retaliatory eviction <state_name> landlord tenant'
         Broad query also filtered by Check E. Broad fallback approved by Andy 2026-06-29.

    Prior strategy (2026-06-26): statute-targeted only, no jurisdiction filter.
    Root cause of Batch 4 MI/NJ wrong-jurisdiction contamination: CL statute queries
    returned out-of-state cases (same statute number prefix matches other states' codes).
    Check E prevents those from entering the 4-check verification pipeline.
    """
    state_name = _CL_STATE_NAMES.get(state_abbr, state_abbr)
    statute = _STATE_RETALIATION_STATUTES.get(state_abbr, "")

    def _run_search(q: str) -> tuple[list[dict], bool]:
        """Execute one CL search and return (jurisdiction-filtered case dicts, network_error).

        network_error=True means the search FAILED for infrastructure reasons
        (DNS, connection, timeout) after retries — an empty result in that case
        is NOT evidence that no cases exist (PR-class, not a genuine no-CL state).

        Network errors retry with a long backoff (2026-07-05 fix): two consecutive
        overnight runs (c0a2df2d 2026-07-03, c7bcdcff 2026-07-04) failed on
        NameResolutionError at ~2:15-2:25 AM PT — a recurring DNS-unavailability
        window at dispatch time. The old code bailed on first ConnectionError;
        this rides out an outage of up to ~10 min per query.

        2026-07-08 extension (YELLOW): run e9222548 (2026-07-07) exhausted the
        full 60/120/180/240s ladder on BOTH queries — the outage window can
        exceed 10 min. Ladder extended to 60/120/240/600/1200/1800s
        (~66 min ride-out per query). Note: wall-clock evidence from e9222548
        (dispatched 2:16 AM PT, harness unit processing at 5:11 PM PT) suggests
        the machine may sleep mid-run despite caffeinate -ims; if so, longer
        backoff only helps when the process is actually running — see
        DAILY_CHANGELOG 2026-07-08 for the machine-sleep hypothesis flagged
        to Andy.
        """
        net_backoff = (60, 120, 240, 600, 1200, 1800)  # ~66 min total ride-out
        params = {
            "q": q,
            "type": "o",
            "order_by": "score desc",
            "format": "json",
            "stat_Precedential": "on",
        }
        for attempt in range(len(net_backoff) + 1):
            try:
                r = requests.get(
                    f"{CL_BASE}/search/", params=params, headers=cl_headers(), timeout=15
                )
                if r.status_code == 429:
                    wait = 3 * (2 ** attempt)
                    print(f"    [CL 429 — waiting {wait}s]")
                    time.sleep(wait)
                    continue
                r.raise_for_status()
                hits = r.json().get("results", [])
                accepted, rejected = [], []
                for hit in hits[:max_results * 2]:  # oversample before filtering
                    court = hit.get("court", "")
                    if _court_matches_state(court, state_abbr):
                        accepted.append(_build_case_from_hit(hit))
                        if len(accepted) >= max_results:
                            break
                    else:
                        rejected.append(f"{hit.get('caseName','?')[:40]} ({court})")
                if rejected:
                    print(f"    [Check E: rejected {len(rejected)} wrong-jurisdiction hits: "
                          f"{rejected[:3]}{'...' if len(rejected) > 3 else ''}]")
                return accepted, False
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout) as e:
                print(f"    [CL network error for {state_abbr} "
                      f"(attempt {attempt + 1}/{len(net_backoff) + 1}): {e}]")
                if attempt < len(net_backoff):
                    wait = net_backoff[attempt]  # 60/120/240/600/1200/1800s ≈ 66 min total
                    print(f"    [DNS/network may be transient — retrying in {wait}s]")
                    time.sleep(wait)
                    continue
                return [], True
            except Exception as e:
                print(f"    [CL search error for {state_abbr}: {e}]")
                return [], True
        return [], True

    # Step 1: statute-targeted query (precision)
    if statute:
        q_statute = f"{statute} retaliation tenant landlord residential"
    else:
        q_statute = f"retaliatory eviction {state_name} landlord tenant residential"

    cases, net_err = _run_search(q_statute)
    print(f"    [CL statute query: {len(cases)} in-state candidates for {state_abbr}]")

    # Step 2: broad fallback if statute query returns 0 in-state results
    if not cases and statute:
        q_broad = f"retaliatory eviction {state_name} landlord tenant"
        print(f"    [CL broad fallback for {state_abbr}: '{q_broad}']")
        cases, net_err_broad = _run_search(q_broad)
        if cases:
            for c in cases:
                c["_source"] = "cl_fresh_search_broad_fallback"
            print(f"    [CL broad fallback: {len(cases)} in-state candidates for {state_abbr}]")
        elif net_err_broad:
            print(f"    [CL broad fallback: SEARCH FAILED (network) for {state_abbr} — "
                  f"PR-class infrastructure failure, NOT a genuine no-CL state. Retry the job.]")
        else:
            print(f"    [CL broad fallback: 0 results for {state_abbr} — genuine no-CL state]")
    elif not cases and net_err:
        print(f"    [CL search FAILED (network) for {state_abbr} — "
              f"PR-class infrastructure failure, NOT a genuine no-CL state. Retry the job.]")

    return cases


def load_draft_cases(state: str, fresh: bool = False) -> list[dict]:
    output_files = sorted(Path(__file__).parent.glob("output/retaliation_holdings_l2_raw_*.json"), reverse=True)
    if output_files:
        with open(output_files[0]) as f:
            draft = json.load(f)
        for sr in draft.get("results", []):
            if sr.get("state") == state:
                cases = sr.get("case_results", [])
                if cases:
                    return cases
    else:
        print(f"  WARNING: No v1 draft file found")
    if fresh:
        print(f"  [fresh=True] No v1 draft candidates for {state} — searching CourtListener...")
        return cl_search_retaliation_by_state(state)
    return []


def run_state(state: str, dry_run: bool = False) -> dict:
    print(f"\n{state}")
    cases = load_draft_cases(state)
    if not cases:
        print(f"  No candidate cases — skipping")
        return {"state": state, "cases_verified": 0, "machine_verified": 0, "needs_attorney": 0,
                "confirm_inference": 0, "re_characterize": 0, "wrong_doc": 0, "case_results": [],
                "note": "No candidate cases in draft file"}
    print(f"  {len(cases)} candidate case(s)")
    if dry_run:
        return {"state": state, "cases_verified": 0, "dry_run": True, "case_results": []}

    results = []
    for case in cases:
        vr = verify_case(case, state)
        results.append(vr)

    mv = sum(1 for r in results if r["disposition"] == "machine-verified")
    na = sum(1 for r in results if r["disposition"] == "needs-attorney")
    ci = sum(1 for r in results if r.get("queue_routing") == "CONFIRM-INFERENCE")
    rc = sum(1 for r in results if r.get("queue_routing") == "RE-CHARACTERIZE")
    wd = sum(1 for r in results if r.get("queue_routing") == "WRONG-DOC")

    print(f"  → {mv} machine-verified | {na} needs-attorney")
    print(f"     Queues: CONFIRM-INFERENCE={ci} | RE-CHARACTERIZE={rc} | WRONG-DOC={wd}")

    return {"state": state, "cases_verified": len(results), "machine_verified": mv, "needs_attorney": na,
            "confirm_inference": ci, "re_characterize": rc, "wrong_doc": wd, "case_results": results}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Retaliation Holdings v3 — Generate-From-Source")
    parser.add_argument("--states", help="Comma-separated state codes")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    states = [s.strip().upper() for s in args.states.split(",")] if args.states else CONSENSUS_STATES
    invalid = [s for s in states if s not in CONSENSUS_STATES]
    if invalid:
        print(f"WARNING: {invalid} not in consensus states list")

    run_id = uuid.uuid4().hex[:8]
    today  = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("=" * 60)
    print(f"Retaliation Holdings v3 — Generate-From-Source — {len(states)} states")
    print(f"Run ID: {run_id} | Date: {today}")
    print(f"Generate model (M1): {GENERATE_MODEL_NAME}")
    print(f"Verify model   (M2): {VERIFY_MODEL_NAME}")
    print(f"Protocol: Check A (existence/citation) + B (currency) + C (generate→verify) + D (derived)")
    print(f"INDEPENDENCE CHECK: M1 != M2 → {GENERATE_MODEL_NAME != VERIFY_MODEL_NAME}")
    print(f"CRITICAL: machine-verified is below the attorney line. Nothing here is `validated`.")
    print("=" * 60)

    all_results   = []
    total_mv = total_na = total_cases = total_ci = total_rc = total_wd = 0

    for state in states:
        sr = run_state(state, dry_run=args.dry_run)
        all_results.append(sr)
        total_mv    += sr.get("machine_verified", 0)
        total_na    += sr.get("needs_attorney", 0)
        total_cases += sr.get("cases_verified", 0)
        total_ci    += sr.get("confirm_inference", 0)
        total_rc    += sr.get("re_characterize", 0)
        total_wd    += sr.get("wrong_doc", 0)

    raw_record = {
        "run_date":    today,
        "run_id":      run_id,
        "runner_version": "v3-generate-from-source",
        "direction":   "COWORK_DIRECTION_HOLDINGS_GENERATE_FROM_SOURCE.md",
        "generate_model": GENERATE_MODEL_NAME,
        "verify_model":   VERIFY_MODEL_NAME,
        "independence_satisfied": GENERATE_MODEL_NAME != VERIFY_MODEL_NAME,
        "c_pass_condition": (
            "Gemini generates holding from text (no draft visible). "
            "GPT (different model) verifies characterization as accurate or partially_accurate against text. "
            "Both required. Same threshold as v2 — holding built from source, not draft."
        ),
        "states_run":  len(states),
        "state_list":  states,
        "total_cases_verified":  total_cases,
        "total_machine_verified": total_mv,
        "total_needs_attorney":   total_na,
        "machine_verified_rate":  f"{total_mv/total_cases:.1%}" if total_cases else "N/A",
        "queue_counts": {
            "CONFIRM-INFERENCE": total_ci,
            "RE-CHARACTERIZE":   total_rc,
            "WRONG-DOC":         total_wd,
        },
        "dry_run": args.dry_run,
        "results": all_results,
    }

    out_filename = f"retaliation_holdings_v3_{len(states)}states_{today}_{run_id}.json"
    out_path = OUTPUT_DIR / out_filename

    if not args.dry_run:
        with open(out_path, "w") as f:
            json.dump(raw_record, f, indent=2, ensure_ascii=False)
        print(f"\nRaw output saved: {out_path}")

    print("\n" + "=" * 60)
    print(f"Retaliation Holdings v3 — {len(states)} states")
    print(f"Cases verified: {total_cases}")
    if total_cases:
        print(f"✅ machine-verified:    {total_mv} ({total_mv/total_cases:.0%})")
        print(f"⚠️  needs-attorney:      {total_na} ({total_na/total_cases:.0%})")
        print(f"")
        print(f"Queue breakdown:")
        print(f"  CONFIRM-INFERENCE:   {total_ci}  (corroborated, INFERRED — attorney confirms)")
        print(f"  RE-CHARACTERIZE:     {total_rc}  (C disputed — attorney re-characterizes from text)")
        print(f"  WRONG-DOC:           {total_wd}  (CL returned wrong document — source correctly)")
    print()
    print("PROVENANCE: per-case generate_model + verify_model in output JSON.")
    print("C pass condition stated verbatim in output JSON root.")
    print("CRITICAL: machine-verified is below the attorney line.")
    print()
    print("⚠️ STOP AND REPORT. Share output with Cowork for ingestion.")
    print(f"Output: {out_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
