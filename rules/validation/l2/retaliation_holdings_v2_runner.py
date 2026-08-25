#!/usr/bin/env python3
"""
Retaliation Defense — Holdings Verification Runner v2 (prompt revision v3, 2026-06-23)
======================================================
Implements COWORK_DIRECTION_HOLDINGS_VERIFICATION.md (2026-06-21).

Authoritative-source verification of candidate case citations produced by
retaliation_holdings_runner.py (the draft/identification run). This runner
does NOT re-identify cases — it verifies each candidate against real sources.

SOURCE ARCHITECTURE (per Step 0 empirical check, 2026-06-21):
  Primary: CourtListener REST API (https://api.courtlistener.com/api/rest/v4/)
    - ~10M federal + state opinions including historical (1970s+)
    - Free, no key required; key = higher rate limits
    - Reachable from Andy's Terminal (proxy blocks it in Cowork sandbox)
    - Provides: existence, citation verification, full opinion text, citator
  Backup: Harvard Caselaw Access Project (via CourtListener bulk export)
  NOT available from Terminal: Legal Data Hunter MCP (sandbox-only)

CHECK PROTOCOL (per direction):
  Check A — Existence + citation correctness
    Query CourtListener by case name; verify returned citation matches.
    exists: true | FLAG (not found / ambiguous)
  Check B — Currency ("still good law")
    Pull CourtListener cluster data for citing treatment.
    currency: OK-machine (source + as-of date recorded)
           | NEGATIVE-FLAG (any negative treatment found)
           | UNVERIFIED-no-citator (API error / no data)
  Check C — Holding characterization accuracy
    Fetch full opinion text from CourtListener.
    Both models independently characterize the holding from the retrieved text.
    Models agree + text supports characterization → holding: corroborated
    Otherwise → holding: FLAG
  Check D — Control determination (the key one)
    Models extract the controlling quote + pin cite from the retrieved opinion.
    control: STATED (quote found + both models agree on it)
           | INFERRED (no specific quote; control would be analogized)

DISPOSITION:
  machine-verified: A ✓ + B OK ✓ + C corroborated ✓ + D STATED ✓
  needs-attorney: any check FLAG / NEGATIVE / UNVERIFIED / INFERRED

LABELING DISCIPLINE:
  machine-verified is BELOW the attorney line.
  Nothing is `validated` on machine output alone.
  Ceiling for this runner: machine-verified.

UNIQUE OUTPUT FILE:
  retaliation_holdings_v2_{STATE_COUNT}states_{DATE}_{RUN_ID}.json
  Never overwrites a prior run (state-count + date + run ID).

Usage:
  cd /Users/andrewcohen/Developer/a2j-ai
  python3 rules/validation/l2/retaliation_holdings_v2_runner.py --states CA
  python3 rules/validation/l2/retaliation_holdings_v2_runner.py --states AZ,CA,DC,IA

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

OPENAI_MODEL  = "gpt-4o"              # gpt-4.5-preview is retired; gpt-4o is widely available
GEMINI_MODEL  = "gemini-2.5-pro"
BUDGET_CAP    = 15.00                 # hard stop
CL_BASE       = "https://www.courtlistener.com/api/rest/v4"
CL_TOKEN      = os.getenv("COURTLISTENER_API_TOKEN", "")  # optional; higher rate limit

# States with genuine two-model consensus on elements layer (run holdings on these only)
CONSENSUS_STATES = [
    "AZ","CA","DC","IA","KY","MA","ME","MN","NE","NH","RI","WA",  # CONFIRMED (period exists)
    "DE",                                                            # CONFIRMED (8-state retry)
    "AR","IN","MO","VA",                                            # NO-PERIOD (8-state retry)
    "FL","GA","ID","IL","MD","MS","MT","NC","OH","OR","PA",
    "SD","TN","TX","UT","WI","WY",                                  # NO-PERIOD (51-state run)
]

OUTPUT_DIR = Path(__file__).parent / "output"

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))

# ---------------------------------------------------------------------------
# CourtListener helpers
# ---------------------------------------------------------------------------

def cl_headers():
    h = {"Accept": "application/json", "User-Agent": "CivilJusticeAsCode/1.0"}
    if CL_TOKEN:
        h["Authorization"] = f"Token {CL_TOKEN}"
    return h


def cl_search_case(case_name: str, year: int | None = None,
                   citation_gpt: str | None = None, citation_gem: str | None = None) -> dict | None:
    """Search CourtListener for a case by name, with citation fallback.

    Strategy order:
    1. Name search + year bounds (primary)
    2. Name search without year bounds (if 1 fails)
    3. Citation search using model citations (fallback when name search returns wrong case or 429)
    Validates name-token overlap to guard against wrong-case returns.
    """
    def _search(q, extra_params):
        params = {"q": q, "type": "o", "order_by": "score desc", "format": "json"}
        params.update(extra_params)
        for attempt in range(5):
            r = requests.get(f"{CL_BASE}/search/", params=params, headers=cl_headers(), timeout=15)
            if r.status_code == 429:
                wait = 3 * (2 ** attempt)  # 3s, 6s, 12s, 24s, 48s
                print(f"        [CL rate limit 429 — waiting {wait}s before retry]")
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json().get("results", [])
        r.raise_for_status()  # final raise if still 429
        return []

    def _citation_search(cite: str) -> list:
        """Search by citation string directly — more precise than name search."""
        params = {"citation": cite, "type": "o", "format": "json"}
        for attempt in range(3):
            r = requests.get(f"{CL_BASE}/search/", params=params, headers=cl_headers(), timeout=15)
            if r.status_code == 429:
                wait = 3 * (2 ** attempt)
                print(f"        [CL rate limit 429 on citation search — waiting {wait}s]")
                time.sleep(wait)
                continue
            if r.status_code == 200:
                return r.json().get("results", [])
            return []
        return []

    def _validate_hit(hit: dict, query: str) -> bool:
        """Returns True if the hit looks like the right case (name token overlap)."""
        query_tokens = set(t.lower() for t in query.replace(".", " ").split() if len(t) > 3)
        hit_name = (hit.get("caseName") or "").lower()
        return not query_tokens or any(t in hit_name for t in query_tokens)

    try:
        year_params = {}
        if year:
            year_params = {"filed_after": f"{year - 1}-01-01", "filed_before": f"{year + 1}-12-31"}

        # Strategy 1: name + year
        results = _search(case_name, year_params)
        if not results and year_params:
            # Strategy 2: name only
            results = _search(case_name, {})

        if results and _validate_hit(results[0], case_name):
            return results[0]

        # Strategy 3: citation search (fallback — more precise, avoids name-search confusion)
        model_cites = [c for c in [citation_gpt, citation_gem] if c]
        for cite in model_cites:
            cite_results = _citation_search(cite)
            if cite_results:
                hit = cite_results[0]
                print(f"        [Citation-search fallback for '{case_name}' via '{cite}' → '{hit.get('caseName')}']")
                return hit

        # If name search returned something but wrong case, return it flagged
        if results:
            hit = results[0]
            hit["_search_warning"] = f"Name overlap check failed for '{case_name}' — may be wrong case"
            return hit

        return None
    except Exception as e:
        return {"error": str(e)}


def cl_get_cluster(cluster_id: int) -> dict | None:
    """Fetch the opinion cluster (case metadata + citations)."""
    try:
        r = requests.get(f"{CL_BASE}/clusters/{cluster_id}/", headers=cl_headers(), timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def cl_get_opinion_id_for_cluster(cluster_id: int) -> int | None:
    """Get the primary opinion ID for a cluster via the opinions endpoint.
    Retries on 429 with exponential backoff — callers must not swallow 429 silently.
    """
    for attempt in range(5):
        try:
            r = requests.get(
                f"{CL_BASE}/opinions/",
                params={"cluster": cluster_id, "format": "json"},
                headers=cl_headers(),
                timeout=15,
            )
            if r.status_code == 429:
                wait = 3 * (2 ** attempt)  # 3s, 6s, 12s, 24s, 48s
                print(f"        [CL rate limit 429 on opinion lookup cluster {cluster_id} — waiting {wait}s]")
                time.sleep(wait)
                continue
            r.raise_for_status()
            results = r.json().get("results", [])
            return results[0]["id"] if results else None
        except Exception as e:
            if attempt < 4:
                time.sleep(3)
                continue
            return None
    return None


def cl_get_opinion_text(opinion_id: int) -> str | None:
    """Fetch the plain text of an opinion, trying all available text fields."""
    try:
        r = requests.get(f"{CL_BASE}/opinions/{opinion_id}/", headers=cl_headers(), timeout=15)
        r.raise_for_status()
        d = r.json()
        # Try text fields in preference order (Harvard XML > plain > HTML variants)
        for field in ["plain_text", "xml_harvard", "html_anon_2020", "html_lawbox",
                      "html_columbia", "html_with_citations", "html", "html_lawbox_extract"]:
            val = d.get(field) or ""
            if len(val.strip()) > 200:
                return val
        return None
    except Exception:
        return None


def cl_get_citing_opinions(cluster_id: int, max_results: int = 20) -> list[dict]:
    """Get opinions that cite the given cluster (subsequent treatment signal)."""
    try:
        r = requests.get(
            f"{CL_BASE}/search/",
            params={"q": f"cites:{cluster_id}", "type": "o", "format": "json", "count": max_results},
            headers=cl_headers(),
            timeout=15,
        )
        r.raise_for_status()
        return r.json().get("results", [])
    except Exception:
        return []


NEGATIVE_TREATMENT_KEYWORDS = [
    "overruled", "abrogated", "superseded", "disapproved", "reversed on other grounds",
    "no longer good law", "limited by", "distinguished into oblivion",
]

def detect_negative_treatment(citing_cases: list[dict]) -> tuple[bool, str | None]:
    """Scan citing case snippets for negative treatment language. Returns (is_negative, note)."""
    for c in citing_cases:
        snippet = (c.get("snippet") or "").lower()
        for kw in NEGATIVE_TREATMENT_KEYWORDS:
            if kw in snippet:
                return True, f"Potential negative treatment in {c.get('caseName','(unknown)')} ({c.get('dateFiled','')}): '{kw}' found in snippet"
    return False, None


# ---------------------------------------------------------------------------
# LLM helpers
# ---------------------------------------------------------------------------

def gpt(prompt: str, max_tokens: int = 2000, json_mode: bool = True) -> dict | str | None:
    try:
        kwargs = dict(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=max_tokens,
            temperature=1,
        )
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        r = openai_client.chat.completions.create(**kwargs)
        content = r.choices[0].message.content or ""
        if not content.strip():
            return {"error": "empty response"}
        if json_mode:
            try:
                return json.loads(content)
            except Exception:
                return {"error": "json_parse_error", "raw": content[:500]}
        return content
    except Exception as e:
        return {"error": str(e)}


def gemini(prompt: str, max_tokens: int = 2000, json_mode: bool = True):
    try:
        config = genai_types.GenerateContentConfig(
            max_output_tokens=max_tokens,
            temperature=1.0,
            response_mime_type="application/json" if json_mode else "text/plain",
            # Use minimal thinking budget (0 is invalid for this model; 512 keeps costs low)
            thinking_config=genai_types.ThinkingConfig(thinking_budget=512),
        )
        r = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=config,
        )
        # New SDK: r.text may be None if candidates are blocked or empty.
        # Try multiple extraction paths.
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
            # Check for safety/block reason
            try:
                reason = r.candidates[0].finish_reason
                return {"error": f"empty response (finish_reason={reason})"}
            except Exception:
                return {"error": "empty response"}
        text = str(text)
        if json_mode:
            try:
                return json.loads(text)
            except Exception:
                return {"error": "json_parse_error", "raw": text[:500]}
        return text
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# The 4 checks
# ---------------------------------------------------------------------------

def check_a_existence(case_name: str, citation_gpt: str | None, citation_gem: str | None, year: int | None) -> dict:
    """Check A: Existence + citation correctness via CourtListener."""
    result = {
        "check": "A_existence_citation",
        "cl_hit": None,
        "cl_cluster_id": None,
        "cl_opinion_id": None,
        "cl_url": None,
        "cl_citation": None,
        "citation_match": None,
        "exists": "uncertain",
        "basis": None,
    }

    hit = cl_search_case(case_name, year, citation_gpt=citation_gpt, citation_gem=citation_gem)
    if not hit or "error" in hit:
        result["exists"] = "FLAG"
        result["basis"] = f"CourtListener search error or no results: {hit}"
        return result

    result["cl_hit"] = {
        "case_name": hit.get("caseName"),
        "date": hit.get("dateFiled"),
        "court": hit.get("court"),
        "citation": hit.get("citation", []),
        "cluster_id": hit.get("cluster_id"),
    }
    result["cl_url"] = hit.get("absolute_url") and f"https://www.courtlistener.com{hit['absolute_url']}"
    result["cl_cluster_id"] = hit.get("cluster_id")

    # Extract opinion ID and collect snippets from all opinions in the search result.
    # Prefer lead-opinion from search result's `opinions` field; fall back to /opinions/?cluster=.
    # IMPORTANT: Do NOT fall back to cluster_id — cluster IDs and opinion IDs are different namespaces.
    opinions_field = hit.get("opinions") or []
    snippets = []
    for op in opinions_field:
        if isinstance(op, dict):
            op_type = op.get("type", "")
            op_id = op.get("id")
            # Collect snippet text (sourced from CL's search index — authoritative text)
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
            time.sleep(1)  # breathing room before secondary API call
            oid = cl_get_opinion_id_for_cluster(cluster_id)
            if oid:
                result["cl_opinion_id"] = oid
    # Store aggregated snippets as fallback text for Checks C and D
    result["cl_snippets"] = " | ".join(snippets) if snippets else None

    # Use ALL citations from search result for matching (CL returns parallel citations).
    cl_cites = hit.get("citation") or []
    result["cl_citation"] = cl_cites[0] if cl_cites else None
    result["cl_all_citations"] = cl_cites

    # Citation match: check model citations against ALL CL citations (handles parallel reporters).
    # Normalize: remove spaces and punctuation for comparison.
    def normalize_cite(c):
        return "".join(ch for ch in str(c).lower() if ch.isalnum())

    candidate_citations = [c for c in [citation_gpt, citation_gem] if c]
    if cl_cites and candidate_citations:
        norm_cl = [normalize_cite(c) for c in cl_cites]
        matched = any(normalize_cite(mc) in norm_cl or any(normalize_cite(mc) in nc for nc in norm_cl)
                      for mc in candidate_citations)
        result["citation_match"] = matched
        result["exists"] = "true" if matched else "FLAG-citation-mismatch"
        result["basis"] = f"CL citations {cl_cites}; model citations {candidate_citations}; match={matched}"
    elif not cl_cites:
        result["exists"] = "true"
        result["basis"] = "Case found by name in CL; no citation to cross-check"
    else:
        result["exists"] = "true"
        result["basis"] = "Case found; no model citation to compare against"

    return result


def check_b_currency(cl_cluster_id: int | None) -> dict:
    """Check B: Currency via CourtListener citing treatment."""
    result = {
        "check": "B_currency",
        "currency": "UNVERIFIED-no-citator",
        "negative_flag": False,
        "negative_note": None,
        "citing_count": 0,
        "basis": None,
        "as_of_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }

    if not cl_cluster_id:
        result["basis"] = "No CourtListener cluster ID — cannot check currency"
        return result

    citing = cl_get_citing_opinions(cl_cluster_id)
    result["citing_count"] = len(citing)

    is_neg, neg_note = detect_negative_treatment(citing)
    if is_neg:
        result["currency"] = "NEGATIVE-FLAG"
        result["negative_flag"] = True
        result["negative_note"] = neg_note
        result["basis"] = f"Negative treatment language detected in {len(citing)} citing opinions"
    else:
        result["currency"] = "OK-machine"
        result["basis"] = f"No negative treatment detected in {len(citing)} citing opinions via CourtListener as of {result['as_of_date']}. Note: absence of negative treatment in snippet scan ≠ confirmed good law — attorney should verify."

    return result


HOLDING_PROMPT = """You are reviewing an appellate case to identify its relevance to the tenant defense of retaliatory eviction.

CASE TEXT (retrieved from CourtListener):
---
{opinion_text}
---

Your tasks:
1. Does this case address the tenant's DEFENSE of retaliatory eviction — i.e., does it discuss whether a landlord may evict a tenant in retaliation for the tenant's protected activity (complaining about habitability, reporting code violations, organizing, exercising legal rights, etc.)?
2. If YES: state in 1-2 sentences what the case held on this question. Be precise about what the court decided.
3. If NO: briefly describe what the case is actually about.

Respond in JSON:
{{
  "addresses_retaliation_defense": true,
  "holding_on_retaliation": "...",
  "what_case_is_about": "...",
  "confidence": "high" | "medium" | "low",
  "note": "..."
}}

If the case does NOT address the retaliation defense, respond:
{{
  "addresses_retaliation_defense": false,
  "holding_on_retaliation": null,
  "what_case_is_about": "...",
  "confidence": "high" | "medium" | "low",
  "note": "..."
}}"""


def check_c_holding(opinion_text: str | None, prior_holding: str, case_name: str) -> dict:
    """Check C: Relevance + fresh holding derivation from retrieved opinion text.

    v3 approach (2026-06-23): Fresh-derives the holding from text rather than comparing
    against the v1 draft prior_holding. Removes dependency on draft characterization
    quality. Corroborated = both models independently confirm case addresses retaliation
    defense. Stores AI-derived holding for use by attorneys reviewing the queue.
    """
    result = {
        "check": "C_holding_relevance_and_derivation",
        "holding": "FLAG",
        "derived_holding_gpt": None,
        "derived_holding_gem": None,
        "gpt_holding": None,
        "gem_holding": None,
        "derived_holding_consensus": None,
        "agreement": None,
        "basis": None,
    }

    if not opinion_text or len(opinion_text.strip()) < 200:
        result["holding"] = "FLAG-no-text"
        result["basis"] = "Opinion text unavailable or too short — cannot verify holding"
        return result

    # Truncate for prompt (keep first 8000 chars — enough for most opinions)
    text_excerpt = opinion_text[:8000]
    prompt = HOLDING_PROMPT.format(opinion_text=text_excerpt)

    # Run both models in parallel — saves ~10-15s per case vs. sequential.
    with ThreadPoolExecutor(max_workers=2) as executor:
        fut_g   = executor.submit(gpt,    prompt, 800)
        fut_gem = executor.submit(gemini, prompt, 800)
        g_resp   = fut_g.result()
        gem_resp = fut_gem.result()

    result["gpt_holding"] = g_resp
    result["gem_holding"] = gem_resp

    # Extract relevance and derived holdings
    g_relevant  = g_resp.get("addresses_retaliation_defense")  if isinstance(g_resp, dict)   and "error" not in g_resp   else None
    gem_relevant = gem_resp.get("addresses_retaliation_defense") if isinstance(gem_resp, dict) and "error" not in gem_resp else None
    g_hold   = g_resp.get("holding_on_retaliation")   if isinstance(g_resp, dict)   else None
    gem_hold = gem_resp.get("holding_on_retaliation") if isinstance(gem_resp, dict) else None

    result["derived_holding_gpt"] = g_hold
    result["derived_holding_gem"] = gem_hold

    if g_relevant is True and gem_relevant is True:
        result["holding"] = "corroborated"
        result["derived_holding_consensus"] = g_hold or gem_hold  # primary for attorney use
        result["agreement"] = True
        result["basis"] = (
            f"Both models confirm case addresses retaliation defense. "
            f"GPT: '{str(g_hold or '')[:120]}' | Gemini: '{str(gem_hold or '')[:120]}'"
        )
    elif g_relevant is False and gem_relevant is False:
        result["holding"] = "FLAG-irrelevant"
        g_about   = g_resp.get("what_case_is_about", "")   if isinstance(g_resp, dict)   else ""
        gem_about = gem_resp.get("what_case_is_about", "") if isinstance(gem_resp, dict) else ""
        result["agreement"] = True
        result["basis"] = f"Both models: case does NOT address retaliation defense. GPT: '{g_about[:100]}'. Gemini: '{gem_about[:100]}'"
    elif g_relevant is None and gem_relevant is None:
        result["holding"] = "FLAG-models-failed"
        result["agreement"] = None
        result["basis"] = "Both models failed to return relevance assessment"
    else:
        # One model says relevant, one says not — treat as needs-attorney
        result["holding"] = "FLAG-split-relevance"
        result["agreement"] = False
        result["basis"] = f"Models disagree on relevance: GPT={g_relevant}, Gemini={gem_relevant}. GPT hold: '{str(g_hold or '')[:80]}'"

    return result


CONTROL_PROMPT = """You are verifying whether an appellate case CONTROLS (i.e., is binding or leading authority for) the following legal question in a residential landlord-tenant context:

LEGAL QUESTION: Does the tenant have an affirmative defense of retaliatory eviction? Specifically: what are the elements, and (if applicable) what is the statutory presumption period?

RETRIEVED CASE TEXT:
---
{opinion_text}
---

Your task:
1. Determine whether this case STATES the controlling rule on this question — meaning the court explicitly addressed this question and its language controls the answer.
2. If the control is STATED with a clear verbatim passage: quote the specific language that most directly states the controlling rule.
3. If the court establishes the rule through reasoning and prose (no single quotable sentence) but you can derive a clear rule from the text: classify as STATED-derived and state the rule in your own words synthesized from the opinion.
4. If the rule can only be INFERRED by analogy (the court addressed a different question and you'd have to extrapolate): classify as INFERRED.

CRITICAL: Never fabricate a verbatim quote. If you cannot find specific language use STATED-derived (for rules clearly established in the opinion) or INFERRED (for analogized rules).

Respond in JSON:
{{
  "control_type": "STATED" | "STATED-derived" | "INFERRED",
  "controlling_quote": "exact verbatim quote" | null,
  "derived_rule": "rule in your own words from the text (for STATED-derived only)" | null,
  "quote_context": "brief description of where in the opinion this appears" | null,
  "control_note": "...",
  "confidence": "high" | "medium" | "low"
}}"""


def check_d_control(opinion_text: str | None, case_name: str) -> dict:
    """Check D: Control determination — STATED with quote vs. INFERRED."""
    result = {
        "check": "D_control",
        "control": "INFERRED",
        "gpt_control": None,
        "gem_control": None,
        "controlling_quote": None,
        "quote_agreement": False,
        "basis": None,
    }

    if not opinion_text or len(opinion_text.strip()) < 200:
        result["basis"] = "Opinion text unavailable — cannot determine control type"
        return result

    text_excerpt = opinion_text[:8000]
    prompt = CONTROL_PROMPT.format(opinion_text=text_excerpt)

    # Run both models in parallel — saves ~10-15s per case vs. sequential.
    with ThreadPoolExecutor(max_workers=2) as executor:
        fut_g   = executor.submit(gpt,    prompt, 1000)
        fut_gem = executor.submit(gemini, prompt, 1000)
        g_resp   = fut_g.result()
        gem_resp = fut_gem.result()

    result["gpt_control"] = g_resp
    result["gem_control"] = gem_resp

    g_type   = g_resp.get("control_type")   if isinstance(g_resp, dict)   and "error" not in g_resp   else None
    gem_type = gem_resp.get("control_type") if isinstance(gem_resp, dict) and "error" not in gem_resp else None
    g_quote   = g_resp.get("controlling_quote")   if isinstance(g_resp, dict)   else None
    gem_quote = gem_resp.get("controlling_quote") if isinstance(gem_resp, dict) else None
    g_derived   = g_resp.get("derived_rule")   if isinstance(g_resp, dict)   else None
    gem_derived = gem_resp.get("derived_rule") if isinstance(gem_resp, dict) else None

    STATED_TYPES = ("STATED", "STATED-derived")

    if g_type == "STATED" and gem_type == "STATED" and g_quote and gem_quote:
        result["control"] = "STATED"
        result["controlling_quote"] = g_quote  # use GPT's quote (both agreed)
        result["quote_agreement"] = True
        result["basis"] = "Both models classified control as STATED and provided verbatim quotes"

    elif g_type in STATED_TYPES and gem_type in STATED_TYPES:
        # Both agree the rule is established in the opinion (may be verbatim or derived)
        quote = g_quote or gem_quote
        derived = g_derived or gem_derived
        if quote:
            result["control"] = "STATED-single-model"
            result["controlling_quote"] = quote
        else:
            result["control"] = "STATED-derived"
            result["controlling_quote"] = derived  # synthesized rule, not verbatim
        result["quote_agreement"] = True
        result["basis"] = f"Both models agree rule is established in opinion: GPT={g_type}, Gemini={gem_type}. {'Verbatim quote available.' if quote else 'Rule derived from prose — attorney should verify precise language.'}"

    elif g_type in STATED_TYPES and (g_quote or g_derived):
        result["control"] = "STATED-single-model"
        result["controlling_quote"] = g_quote or g_derived
        result["basis"] = f"GPT: {g_type}. Gemini: {gem_type}. Single-model — attorney should verify."

    elif gem_type in STATED_TYPES and (gem_quote or gem_derived):
        result["control"] = "STATED-single-model"
        result["controlling_quote"] = gem_quote or gem_derived
        result["basis"] = f"Gemini: {gem_type}. GPT: {g_type}. Single-model — attorney should verify."

    else:
        result["control"] = "INFERRED"
        result["basis"] = f"Neither model found stated or derivable rule: GPT={g_type}, Gemini={gem_type}"

    return result


# ---------------------------------------------------------------------------
# Per-case verification
# ---------------------------------------------------------------------------

def verify_case(case: dict, state: str) -> dict:
    """Run all 4 checks on a single candidate case."""
    case_name = case.get("case_name", "")
    citation_gpt = case.get("citation_gpt")
    citation_gem = case.get("citation_gemini")
    year = case.get("year")
    prior_holding = case.get("holding_gpt") or case.get("holding_gemini") or ""

    print(f"    Verifying: {case_name} ({year})")

    # Check A
    print(f"      Check A: existence/citation...")
    check_a = check_a_existence(case_name, citation_gpt, citation_gem, year)
    cl_cluster_id = check_a.get("cl_cluster_id")
    cl_opinion_id = check_a.get("cl_opinion_id")
    time.sleep(10)  # rate limiting — 10s inter-call sleep to avoid CL session quota exhaustion

    # Fetch opinion text once (used for checks C and D).
    # Primary: /opinions/{id}/ structured fields.
    # Fallback: snippets extracted from CL search result (authoritative source, shorter).
    opinion_text = None
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
            opinion_text_source = "CL search index snippet (authoritative source; abbreviated)"
            print(f"      Full text unavailable — using search snippet as fallback")

    # Check B
    print(f"      Check B: currency...")
    check_b = check_b_currency(cl_cluster_id)
    time.sleep(5)

    # Check C
    print(f"      Check C: holding accuracy...")
    check_c = check_c_holding(opinion_text, prior_holding, case_name)

    # Check D
    print(f"      Check D: control type...")
    check_d = check_d_control(opinion_text, case_name)

    # Disposition
    a_ok = check_a["exists"] in ("true",)
    b_ok = check_b["currency"] == "OK-machine"
    c_ok = check_c["holding"] == "corroborated"
    d_ok = check_d["control"] in ("STATED", "STATED-single-model", "STATED-derived")

    if a_ok and b_ok and c_ok and d_ok:
        disposition = "machine-verified"
        disposition_note = "All 4 checks passed: existence ✓, citation ✓, currency OK-machine ✓, holding corroborated ✓, control STATED ✓. Below attorney line — attorney must confirm before use."
    else:
        failed = []
        if not a_ok: failed.append(f"A={check_a['exists']}")
        if not b_ok: failed.append(f"B={check_b['currency']}")
        if not c_ok: failed.append(f"C={check_c['holding']}")
        if not d_ok: failed.append(f"D={check_d['control']}")
        disposition = "needs-attorney"
        disposition_note = f"Flagged: {', '.join(failed)}. Attorney review required."

    print(f"      → {disposition} (A={check_a['exists']}, B={check_b['currency']}, C={check_c['holding']}, D={check_d['control']})")

    return {
        "case_name": case_name,
        "citation_gpt": citation_gpt,
        "citation_gemini": citation_gem,
        "year": year,
        "prior_holding": prior_holding,
        "check_a": check_a,
        "check_b": check_b,
        "check_c": check_c,
        "check_d": check_d,
        "disposition": disposition,
        "disposition_note": disposition_note,
        "controlling_quote": check_d.get("controlling_quote"),
    }


# ---------------------------------------------------------------------------
# Per-state runner
# ---------------------------------------------------------------------------

def load_draft_cases(state: str) -> list[dict]:
    """Load candidate cases from the v1 holdings draft raw file."""
    # Find most recent v1 raw file
    output_files = sorted(OUTPUT_DIR.glob("retaliation_holdings_l2_raw_*.json"), reverse=True)
    if not output_files:
        print(f"  WARNING: No v1 holdings draft file found in {OUTPUT_DIR}")
        return []
    draft_file = output_files[0]
    with open(draft_file) as f:
        draft = json.load(f)
    for sr in draft.get("results", []):
        if sr.get("state") == state:
            return sr.get("case_results", [])
    return []


def run_state(state: str, dry_run: bool = False) -> dict:
    """Run full holdings verification for one state."""
    print(f"\n{state}")
    cases = load_draft_cases(state)

    if not cases:
        print(f"  No candidate cases found in draft file — skipping")
        return {
            "state": state,
            "cases_verified": 0,
            "machine_verified": 0,
            "needs_attorney": 0,
            "case_results": [],
            "note": "No candidate cases in draft file",
        }

    print(f"  {len(cases)} candidate case(s) to verify")
    if dry_run:
        print(f"  [DRY RUN — skipping API calls]")
        return {"state": state, "cases_verified": 0, "dry_run": True, "case_results": []}

    results = []
    for case in cases:
        vr = verify_case(case, state)
        results.append(vr)

    mv = sum(1 for r in results if r["disposition"] == "machine-verified")
    na = sum(1 for r in results if r["disposition"] == "needs-attorney")

    print(f"  → {mv} machine-verified | {na} needs-attorney")

    return {
        "state": state,
        "cases_verified": len(results),
        "machine_verified": mv,
        "needs_attorney": na,
        "case_results": results,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Retaliation Holdings Verification Runner v2")
    parser.add_argument("--states", help="Comma-separated state codes (default: all consensus states)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.states:
        states = [s.strip().upper() for s in args.states.split(",")]
    else:
        states = CONSENSUS_STATES

    # Validate
    invalid = [s for s in states if s not in CONSENSUS_STATES]
    if invalid:
        print(f"WARNING: {invalid} not in consensus states list — only elements-consensus states should run holdings")

    run_id = uuid.uuid4().hex[:8]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("=" * 60)
    print(f"Retaliation Holdings Verification v2 — {len(states)} states")
    print(f"Run ID: {run_id} | Date: {today}")
    print(f"Source: CourtListener REST API")
    print(f"Models: {OPENAI_MODEL} + {GEMINI_MODEL}")
    print(f"Protocol: 4-check verification (A: existence/citation, B: currency, C: holding, D: control)")
    print(f"Budget cap: ${BUDGET_CAP:.2f}")
    print(f"CRITICAL: machine-verified is below the attorney line. Nothing here is `validated`.")
    print("=" * 60)

    all_results = []
    total_mv = 0
    total_na = 0
    total_cases = 0

    for state in states:
        sr = run_state(state, dry_run=args.dry_run)
        all_results.append(sr)
        total_mv += sr.get("machine_verified", 0)
        total_na += sr.get("needs_attorney", 0)
        total_cases += sr.get("cases_verified", 0)

    # Save raw output — unique path per run
    raw_record = {
        "run_date": today,
        "run_id": run_id,
        "module": "substantive_defenses.retaliation.layer_decomposition.holdings",
        "runner_version": "v2",
        "source": "CourtListener REST API",
        "models": {"gpt": OPENAI_MODEL, "gemini": GEMINI_MODEL},
        "states_run": len(states),
        "state_list": states,
        "total_cases_verified": total_cases,
        "total_machine_verified": total_mv,
        "total_needs_attorney": total_na,
        "machine_verified_rate": f"{total_mv/total_cases:.1%}" if total_cases else "N/A",
        "dry_run": args.dry_run,
        "results": all_results,
    }

    out_filename = f"retaliation_holdings_v2_{len(states)}states_{today}_{run_id}.json"
    out_path = OUTPUT_DIR / out_filename

    if not args.dry_run:
        with open(out_path, "w") as f:
            json.dump(raw_record, f, indent=2, ensure_ascii=False)
        print(f"\nRaw output saved: {out_path}")
    else:
        print(f"\n[DRY RUN] Would save to: {out_path}")

    print("\n" + "=" * 60)
    print(f"Retaliation Holdings v2 — {len(states)} states")
    print(f"Cases verified: {total_cases}")
    print(f"✅ machine-verified: {total_mv} ({total_mv/total_cases:.0%})" if total_cases else "")
    print(f"⚠️  needs-attorney:   {total_na} ({total_na/total_cases:.0%})" if total_cases else "")
    print()
    print("CRITICAL REMINDER: machine-verified = draft grade BELOW attorney line.")
    print("machine-verified items are research starting points, not confirmed citations.")
    print("Only attorney-signed-off holdings may be cited publicly.")
    print()
    print("⚠️ STOP AND REPORT. Share output file with Cowork for ingestion.")
    print(f"Output: {out_path}")
    print()
    print("STEP 3 — AUDIT:")
    print("After ingestion, run the audit sampler:")
    print(f"  python3 rules/validation/l2/retaliation_holdings_v2_audit.py {out_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
