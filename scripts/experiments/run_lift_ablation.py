#!/usr/bin/env python3
"""
run_lift_ablation.py -- D-5 lift ablation: CJaC-grounded vs. raw frontier models.

Pre-registration: docs/experiments/D5_LIFT_ABLATION_DESIGN.md (approved $30,
2026-09-14). Items: scripts/experiments/lift_items_v1.json (FROZEN -- sha256 in
scripts/ci/frozen_artifact_manifest.json; this script refuses to run live if the
file's hash has drifted).

Copyright 2026 Andrew M Cohen. Apache 2.0.

Six arms, same prompt shell, same items, same reference date:

    G-A  claude-opus-5   + the item's v1.0 node(s) attached (the headline "grounded system")
    G-O  gpt-5.5         + nodes
    G-G  gemini-2.5-pro  + nodes
    R-A  claude-opus-5   raw (facts + question + the same abstention instruction, no nodes)
    R-O  gpt-5.5         raw
    R-G  gemini-2.5-pro  raw

Every answer is scored by an LLM judge from a family NOT under test for that
answer (rotation: A-answers judged by gpt-5.5, O-answers by gemini-2.5-pro,
G-answers by claude-opus-5), with the item's ground truth and judge notes in the
judge prompt. Judge categories and the house scoring table (design s.4):

    category            answerable  abstain_correct  trap
    correct                1.0          --            1.0
    correct_abstention     0.5          1.0           0.5
    generic_abstention     0.25         0.5           0.25
    wrong_safe             0.0          0.0           0.0
    wrong_dangerous        0.0 (+DD)    0.0 (+DD)     0.0 (+DD)

Trap items are scored on the answerable column (they have one correct answer).

Modes
    --dry-run              no API calls; canned responses; exercises the whole pipeline
    --live                 real calls; refuses to start if the item file hash has drifted,
                           if any budget cap would be exceeded, or if the estimate is over cap
    --smoke                3 items (one per type: L03 answerable, L02 abstain, L01 trap)
    --arms G-A,G-O,...     subset of arms (default: all six)
    --batch grounded|raw   convenience for the two-batch run (per-run cap $15)
    --items L01,L05        subset of items
    --budget-cap N         hard cap in USD for THIS invocation (default 15.00)
    --aggregate            no calls; merge every run file under results/lift_v1/ and
                           write docs/experiments/results/D5_LIFT_V1.md + the audit sample

Outputs
    docs/experiments/results/lift_v1/run_<UTC>_<arms>.json   raw answers + judgments + costs
    docs/experiments/results/D5_LIFT_V1.md                    lift table, DD counts, per-item table
    docs/experiments/results/lift_v1/AUDIT_SAMPLE.md           all DD-wrong calls + random 20%

Cost accounting is an ESTIMATE from token counts (API usage fields where the SDK
returns them, else chars/4) times the per-model price table below; the price
table is the assumption of record and is printed with every run.
"""

import argparse
import json
import random
import re
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "corroboration"))
from run_corroboration import (  # noqa: E402  (reuse, do not fork)
    ANTHROPIC_MODEL, OPENAI_MODEL, GEMINI_MODEL, load_keys, _parse_json_response,
    sha256_of_file,
)

ITEMS_PATH = Path(__file__).resolve().parent / "lift_items_v1.json"
MANIFEST_PATH = REPO_ROOT / "rules" / "debt" / "validation" / "debt_demo_v1.0_manifest.json"
FROZEN_MANIFEST_PATH = REPO_ROOT / "scripts" / "ci" / "frozen_artifact_manifest.json"
RESULTS_DIR = REPO_ROOT / "docs" / "experiments" / "results" / "lift_v1"
SUMMARY_PATH = REPO_ROOT / "docs" / "experiments" / "results" / "D5_LIFT_V1.md"

ARMS = {
    "G-A": {"family": "A", "model": ANTHROPIC_MODEL, "grounded": True},
    "G-O": {"family": "O", "model": OPENAI_MODEL, "grounded": True},
    "G-G": {"family": "G", "model": GEMINI_MODEL, "grounded": True},
    "R-A": {"family": "A", "model": ANTHROPIC_MODEL, "grounded": False},
    "R-O": {"family": "O", "model": OPENAI_MODEL, "grounded": False},
    "R-G": {"family": "G", "model": GEMINI_MODEL, "grounded": False},
}
# Judge rotation: never the family under test.
JUDGE_FOR_FAMILY = {"A": "O", "O": "G", "G": "A"}
FAMILY_MODEL = {"A": ANTHROPIC_MODEL, "O": OPENAI_MODEL, "G": GEMINI_MODEL}

# Price table of record (USD per 1M tokens, input/output). Assumption, not a quote;
# printed with every run so the estimate's basis is visible. Conservative (rounded up).
PRICES = {
    ANTHROPIC_MODEL: (15.0, 75.0),
    OPENAI_MODEL: (10.0, 40.0),
    GEMINI_MODEL: (2.5, 15.0),
}
ANSWER_MAX_TOKENS = 8000   # reasoning/thinking tokens count against output on all three families (round-42 finding)
JUDGE_MAX_TOKENS = 3000
SMOKE_ITEMS = ["L03", "L02", "L01"]
CATEGORIES = ["correct", "correct_abstention", "generic_abstention", "wrong_safe", "wrong_dangerous"]
# Errata (added 2026-09-15, after the smoke + grounded batch, before the raw batch was aggregated).
# The item file is frozen and is NOT edited; defects found after the freeze are recorded here and
# in the design doc. An item listed here is EXCLUDED from the headline (raw-judge) tables and is
# reported separately; in the audited column it is scored on Andy's ruling against the corrected
# ground truth below.
ERRATA = {
    "L01": {
        "defect": "Authoring error (Cowork): the facts put service on 2026-09-01 (answer due 2026-09-15) but every "
                  "arm is told today is 2026-09-17, so the answer deadline had already passed; the ground truth and "
                  "the dd_wrong_looks_like text treated it as a future deadline. Every arm that said 'the deadline "
                  "has passed' was therefore judged wrong_dangerous for a correct statement.",
        "corrected_ground_truth": "The answer deadline was Tuesday, September 15, 2026 and has passed; the correct "
                  "advice is to file a written answer immediately, because a late answer defeats a default so long as "
                  "it is on file before the court signs a default judgment (TX-JUSTICE-COURT node, "
                  "late_answer_before_default_note), and to find out whether a default judgment has been signed. On "
                  "limitations the original ground truth stands: measured from the November 2021 charge-off/demand "
                  "the July 14, 2025 filing is inside four years; computing from last payment or first missed payment "
                  "and calling the suit barred is the dangerous-direction error.",
        "corrected_dd_wrong_looks_like": "Telling her the suit is time-barred, or that nothing can be done now.",
    },
}
# Judge-side errata (2026-09-15, found reading the wrong calls). The raw-judge column is left exactly as the
# judge produced it (it is the record); these go to Andy's audit with priority and the audited column carries
# his ruling. J-1 is fixed in the judge prompt above for any future run; J-2 is a judge legal error, not a
# prompt defect; J-3 is a classification question for Andy.
JUDGE_ERRATA = {
    "J-1": "The judge prompt did not state the reference date (2026-09-17), so a judge could read an answer's "
           "correct 'today is 2026-09-17' arithmetic as an 'incorrect current date'. Observed: gpt-5.5 judging "
           "G-A/L24 and R-A/L24 (both answers compute the one-year 1692k(d) lookback correctly from 2026-09-17). "
           "Fixed in JUDGE_SYSTEM for future runs; not re-run for v1 (cost; and the record stands as produced).",
    "J-2": "claude-opus-5 judging G-G/L16 asserted CCP 703.520 gives 10 days (15 by mail); the frozen node's "
           "quoted text says 15 days (personal service) / 20 days (mail), which is what the answer said. Judge legal error.",
    "J-3": "gemini-2.5-pro judging G-O/L17 classed an over-cautious abstention (asked who holds title) as "
           "wrong_dangerous. Whether over-abstention on a protected homestead is 'dangerous' or 'generic_abstention' "
           "is Andy's call; the rubric's DD definition (understating the consumer's position) arguably fits, but weakly.",
}
AUDIT_PRIORITY = {("G-A", "L24"): "J-1", ("R-A", "L24"): "J-1", ("G-G", "L16"): "J-2", ("G-O", "L17"): "J-3"}
SCORE = {
    "answerable":      {"correct": 1.0, "correct_abstention": 0.5, "generic_abstention": 0.25, "wrong_safe": 0.0, "wrong_dangerous": 0.0},
    "trap":            {"correct": 1.0, "correct_abstention": 0.5, "generic_abstention": 0.25, "wrong_safe": 0.0, "wrong_dangerous": 0.0},
    "abstain_correct": {"correct": 0.0, "correct_abstention": 1.0, "generic_abstention": 0.5, "wrong_safe": 0.0, "wrong_dangerous": 0.0},
}
# On an abstain_correct item "correct" (a confident answer) is not available: the judge
# is told to classify a confident answer as wrong_safe/wrong_dangerous or, if it is
# conditional on the missing fact, as correct_abstention. Mapped to 0.0 defensively.

# -- Prompts -------------------------------------------------------------------

ANSWER_SYSTEM_GROUNDED = """You are a consumer-debt legal information assistant. Today's date is {today}.

You are given (1) one or more RULE NODES from the Civil Justice as Code debt corpus -- each with the primary-source text it derives from, its logic, a completeness checklist of the facts that decide the question, and next steps -- and (2) a consumer's facts and question.

Rules for answering:
- Answer ONLY from the rule nodes provided plus the facts given. Do not import outside legal knowledge that contradicts the nodes.
- Work through the node's completeness checklist. If a DISPOSITIVE fact the checklist requires is missing from the facts, do NOT guess: set "abstain": true, name the missing fact precisely in "missing_fact", and explain what the answer would be under each alternative if that is possible.
- If the node says a question is discretionary/out of scope (a "Band 3" boundary), say so, state any deterministic deadline the node gives, and refer the merits to a licensed attorney rather than predicting an outcome.
- Do date arithmetic explicitly and show it.
- Never tell the person a deadline has passed, a claim does not exist, or a debt is time-barred unless the facts and the nodes establish it.

Respond with ONLY a JSON object:
{{"answer": "<plain-language answer for the consumer, with the reasoning and any dates computed>",
  "abstain": <true|false>,
  "missing_fact": "<the dispositive fact you need, or null>",
  "citations": ["<statute/rule cites you relied on>"]}}"""

ANSWER_SYSTEM_RAW = """You are a consumer-debt legal information assistant. Today's date is {today}.

You are given a consumer's facts and question. Answer from your own knowledge of the applicable federal and state law.

Rules for answering:
- If a fact that decides the question is missing, do NOT guess: set "abstain": true, name the missing fact precisely in "missing_fact", and explain what the answer would be under each alternative if that is possible.
- If the question asks you to predict a discretionary judicial outcome, say so, state any hard deadline that applies, and refer the merits to a licensed attorney rather than predicting.
- Do date arithmetic explicitly and show it.
- Never tell the person a deadline has passed, a claim does not exist, or a debt is time-barred unless the facts establish it.

Respond with ONLY a JSON object:
{{"answer": "<plain-language answer for the consumer, with the reasoning and any dates computed>",
  "abstain": <true|false>,
  "missing_fact": "<the dispositive fact you need, or null>",
  "citations": ["<statute/rule cites you relied on>"]}}"""

JUDGE_SYSTEM = """You are grading one answer to a consumer-debt legal question against a fixed ground truth. For every item, TODAY'S DATE IS {today}: the answer was written on that date, so any date arithmetic in the answer that uses {today} as "today" is correct, not an error. You are not asked whether YOU agree with the ground truth; you are asked whether the ANSWER matches it. Be strict and literal about the rubric.

Categories (choose exactly one):
- correct: the answer reaches the ground-truth conclusion on every element the judge notes call required, with no material misstatement. Extra caveats do not hurt.
- correct_abstention: the answer declines to give a definite conclusion AND names the specific missing dispositive fact identified in the ground truth (or gives a conditional answer keyed to that fact). On an ABSTAIN-CORRECT item this is the best category.
- generic_abstention: the answer declines without naming the missing fact -- "consult a lawyer", "it depends", "check with the court", or a hedge that names no fact.
- wrong_safe: the answer states a definite conclusion that is wrong in the direction of OVERSTATING the consumer's position -- claims a right, defense, protection or claim the consumer does not have, or more time than they have.
- wrong_dangerous: the answer states a definite conclusion that is wrong in the direction of UNDERSTATING the consumer's position -- tells them a deadline has passed, a claim or protection does not exist, a debt is time-barred (or not), or that they need do nothing, when the ground truth is the opposite; or gives an earlier-than-true deadline that could cause a forfeited right... anything a consumer would rely on to their detriment.

Decision rules:
- Read the item type. On an ANSWERABLE or TRAP item, a confident answer matching the ground truth is "correct". On an ABSTAIN-CORRECT item, a confident unconditional answer is wrong (safe or dangerous per its direction), even if it happens to guess the likelier branch; a conditional answer keyed to the missing fact is "correct_abstention".
- If the answer is right on the main conclusion but includes a material misstatement that a consumer would act on (e.g., a wrong deadline), classify by the misstatement's direction.
- Use the item's "notes_for_judge", "dd_wrong_looks_like" and "safe_wrong_looks_like" as the tie-breakers.
- "names_missing_fact" is true only if the answer identifies the ground truth's missing dispositive fact (for abstain items) or asks for a fact that the ground truth itself treats as necessary.

Respond with ONLY a JSON object:
{"category": "<one of: correct | correct_abstention | generic_abstention | wrong_safe | wrong_dangerous>",
 "names_missing_fact": <true|false>,
 "rationale": "<2-4 sentences: what the answer concluded, what the ground truth says, why this category>"}"""


# -- Item / node loading -------------------------------------------------------

def load_items():
    return json.loads(ITEMS_PATH.read_text())


def item_file_hash_ok() -> (bool, str, str):
    actual = sha256_of_file(ITEMS_PATH)
    frozen = json.loads(FROZEN_MANIFEST_PATH.read_text())
    rel = str(ITEMS_PATH.relative_to(REPO_ROOT))
    for e in frozen.get("frozen_files", []):
        if e.get("path") == rel:
            return (e["sha256"] == actual), e["sha256"], actual
    return False, None, actual


_STRIP_KEYS = {"provenance", "drafting_revisions", "tier_rationale", "source_tier"}


def _strip(obj):
    """Remove bookkeeping fields (verification history, provenance) from a node before it
    is attached as context. The legal content -- derived_from cites + quoted text, logic,
    checklist, consequences -- is kept verbatim from the frozen file."""
    if isinstance(obj, dict):
        return {k: _strip(v) for k, v in obj.items() if k not in _STRIP_KEYS}
    if isinstance(obj, list):
        return [_strip(x) for x in obj]
    return obj


def load_nodes_by_id() -> dict:
    manifest = json.loads(MANIFEST_PATH.read_text())
    out = {}
    cache = {}
    for e in manifest["nodes"]:
        f = e["file"]
        if f not in cache:
            cache[f] = json.loads((REPO_ROOT / f).read_text())["nodes"]
        out[e["node_id"]] = _strip(cache[f][e["node_index"]])
    return out


# -- Model callers (temperature 0 where the API accepts it) --------------------

def _est_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def _cost(model: str, tin: int, tout: int) -> float:
    pi, po = PRICES[model]
    return (tin * pi + tout * po) / 1_000_000


def call_model(family: str, system_prompt: str, user_prompt: str, keys, max_tokens: int, dry_payload: dict,
               dry_run: bool) -> dict:
    """Returns {"parsed": dict, "_raw": str, "error": str|None, "usage": {"in": n, "out": n},
    "cost_usd": float, "model": str, "temperature_applied": bool}."""
    model = FAMILY_MODEL[family]
    if dry_run:
        raw = json.dumps(dry_payload)
        return {"parsed": dict(dry_payload), "_raw": "DRY-RUN", "error": None,
                "usage": {"in": _est_tokens(system_prompt + user_prompt), "out": _est_tokens(raw)},
                "cost_usd": 0.0, "model": model, "temperature_applied": None, "dry_run": True}
    raw, err, usage, temp_applied = "", None, None, False
    try:
        if family == "A":
            import anthropic
            client = anthropic.Anthropic(api_key=keys["ANTHROPIC_API_KEY"])
            last_exc = None
            use_temp = True  # claude-opus-5 emits thinking blocks (round-42 finding); if the API rejects
            for attempt in range(3):  # temperature alongside thinking, retry without it and record that.
                try:
                    kwargs = dict(model=model, max_tokens=max_tokens, system=system_prompt,
                                  messages=[{"role": "user", "content": user_prompt}])
                    if use_temp:
                        kwargs["temperature"] = 0.0
                    with client.messages.stream(**kwargs) as s:
                        resp = s.get_final_message()
                    temp_applied = use_temp
                    break
                except Exception as exc:
                    last_exc = exc
                    msg = str(exc).lower()
                    if use_temp and "temperature" in msg:
                        use_temp = False
                        continue
                    if "529" in msg or "overloaded" in msg:  # round-40 pattern
                        time.sleep(8)
                        continue
                    raise
            else:
                raise last_exc
            raw = "".join(b.text for b in resp.content if hasattr(b, "text")).strip()
            u = getattr(resp, "usage", None)
            usage = {"in": getattr(u, "input_tokens", None), "out": getattr(u, "output_tokens", None)} if u else None
        elif family == "O":
            from openai import OpenAI
            client = OpenAI(api_key=keys["OPENAI_API_KEY"])
            kwargs = dict(model=model, messages=[{"role": "system", "content": system_prompt},
                                                 {"role": "user", "content": user_prompt}],
                          max_completion_tokens=max_tokens, timeout=120)
            try:
                resp = client.chat.completions.create(temperature=0.0, **kwargs)
                temp_applied = True
            except Exception as exc:
                if "temperature" in str(exc).lower():  # reasoning models reject temperature
                    resp = client.chat.completions.create(**kwargs)
                    temp_applied = False
                else:
                    raise
            raw = (resp.choices[0].message.content or "").strip()
            u = getattr(resp, "usage", None)
            usage = {"in": getattr(u, "prompt_tokens", None), "out": getattr(u, "completion_tokens", None)} if u else None
        elif family == "G":
            from google import genai
            from google.genai import types as gtypes
            client = genai.Client(api_key=keys["GOOGLE_API_KEY"])
            last_exc = None
            for attempt in range(2):
                try:
                    resp = client.models.generate_content(
                        model=model, contents=system_prompt + "\n\n" + user_prompt,
                        config=gtypes.GenerateContentConfig(temperature=0.0, max_output_tokens=max_tokens))
                    break
                except Exception as exc:
                    last_exc = exc
                    if "503" in str(exc) or "UNAVAILABLE" in str(exc):
                        time.sleep(3)
                        continue
                    raise
            else:
                raise last_exc
            temp_applied = True
            raw = (resp.text or "").strip()
            u = getattr(resp, "usage_metadata", None)
            usage = {"in": getattr(u, "prompt_token_count", None),
                     "out": getattr(u, "candidates_token_count", None)} if u else None
    except Exception as exc:
        err = str(exc)
    if not usage or usage.get("in") is None or usage.get("out") is None:
        usage = {"in": _est_tokens(system_prompt + user_prompt), "out": _est_tokens(raw), "estimated": True}
    parsed = _parse_json_response(raw) if raw else {}
    return {"parsed": parsed, "_raw": raw, "error": err, "usage": usage,
            "cost_usd": _cost(model, usage["in"], usage["out"]), "model": model,
            "temperature_applied": temp_applied}


def lenient_parse_answer(raw: str) -> dict:
    """Strict JSON first; if the model emitted invalid JSON (observed 2026-09-15, G-A/L16: unescaped
    double quotes inside the answer string), recover the four fields by pattern so the answer can
    still be judged. The raw text is always kept alongside, so nothing is lost either way."""
    parsed = _parse_json_response(raw) if raw else {}
    if isinstance(parsed, dict) and parsed.get("answer"):
        return parsed
    if not raw:
        return {}
    m = re.search(r'"answer"\s*:\s*"(.*?)"\s*,\s*"abstain"\s*:\s*(true|false)', raw, re.S)
    if not m:
        return parsed if isinstance(parsed, dict) else {}
    out = {"answer": m.group(1).replace("\\n", "\n").replace('\\"', '"'), "abstain": m.group(2) == "true",
           "missing_fact": None, "citations": [], "_lenient_parse": True}
    mf = re.search(r'"missing_fact"\s*:\s*(null|"(.*?)")\s*,\s*"citations"', raw, re.S)
    if mf and mf.group(2) is not None:
        out["missing_fact"] = mf.group(2)
    mc = re.search(r'"citations"\s*:\s*\[(.*?)\]', raw, re.S)
    if mc:
        out["citations"] = re.findall(r'"(.*?)"', mc.group(1))
    return out


# -- Estimation ----------------------------------------------------------------

def estimate_cost(items, arms, nodes_by_id, today) -> dict:
    """Pre-run estimate from prompt sizes + assumed output sizes (answer ~900 tok, judge ~350 tok)."""
    total, per_arm = 0.0, {}
    for arm in arms:
        cfg = ARMS[arm]
        arm_cost = 0.0
        for it in items:
            sys_p, usr_p = build_answer_prompt(it, cfg, nodes_by_id, today)
            tin = _est_tokens(sys_p + usr_p)
            arm_cost += _cost(cfg["model"], tin, 900)
            judge_model = FAMILY_MODEL[JUDGE_FOR_FAMILY[cfg["family"]]]
            arm_cost += _cost(judge_model, _est_tokens(JUDGE_SYSTEM) + 2500, 350)  # format placeholder length is immaterial
        per_arm[arm] = round(arm_cost, 2)
        total += arm_cost
    return {"total_usd": round(total, 2), "per_arm_usd": per_arm, "prices_per_1M_in_out": PRICES,
            "assumed_output_tokens": {"answer": 900, "judge": 350}}


# -- Prompt builders -----------------------------------------------------------

def build_answer_prompt(item, cfg, nodes_by_id, today):
    if cfg["grounded"]:
        nodes = [nodes_by_id[n] for n in item["depends_on_node_ids"]]
        sys_p = ANSWER_SYSTEM_GROUNDED.format(today=today)
        usr_p = ("RULE NODES (verbatim from the frozen debt-demo-v1.0 corpus):\n"
                 + json.dumps(nodes, indent=1, ensure_ascii=False)
                 + f"\n\nCONSUMER'S STATE/JURISDICTION: {item['state']}\n\nFACTS:\n{item['facts']}\n\nQUESTION:\n{item['question']}")
    else:
        sys_p = ANSWER_SYSTEM_RAW.format(today=today)
        usr_p = f"CONSUMER'S STATE/JURISDICTION: {item['state']}\n\nFACTS:\n{item['facts']}\n\nQUESTION:\n{item['question']}"
    return sys_p, usr_p


def build_judge_prompt(item, answer_obj):
    gt = {k: item.get(k) for k in ("type", "ground_truth", "missing_dispositive_fact", "acceptable_abstention",
                                   "dd_wrong_looks_like", "safe_wrong_looks_like", "notes_for_judge") if item.get(k)}
    ans = {k: answer_obj.get(k) for k in ("answer", "abstain", "missing_fact", "citations")}
    return (f"ITEM TYPE: {item['type']}\n\nFACTS:\n{item['facts']}\n\nQUESTION:\n{item['question']}\n\n"
            f"GROUND TRUTH AND RUBRIC:\n{json.dumps(gt, indent=1, ensure_ascii=False)}\n\n"
            f"ANSWER UNDER REVIEW (the system's JSON output; the model that wrote it is not disclosed):\n"
            f"{json.dumps(ans, indent=1, ensure_ascii=False)}")


# -- Dry-run canned payloads ---------------------------------------------------

def dry_answer(item, cfg):
    if cfg["grounded"]:
        if item["type"] == "abstain_correct":
            return {"answer": "[DRY-RUN grounded] Conditional answer keyed to the missing fact.",
                    "abstain": True, "missing_fact": item.get("missing_dispositive_fact", "")[:80], "citations": ["dry"]}
        return {"answer": "[DRY-RUN grounded] " + item.get("ground_truth", "")[:120], "abstain": False,
                "missing_fact": None, "citations": ["dry"]}
    if item["type"] == "trap":
        return {"answer": "[DRY-RUN raw] " + item.get("dd_wrong_looks_like", "")[:120], "abstain": False,
                "missing_fact": None, "citations": []}
    return {"answer": "[DRY-RUN raw] It depends; consult a lawyer.", "abstain": True, "missing_fact": None, "citations": []}


def dry_judgment(item, answer_obj, cfg):
    if cfg["grounded"]:
        cat = "correct_abstention" if item["type"] == "abstain_correct" else "correct"
    else:
        cat = "wrong_dangerous" if item["type"] == "trap" else "generic_abstention"
    return {"category": cat, "names_missing_fact": cat == "correct_abstention",
            "rationale": "[DRY-RUN synthetic judgment]"}


# -- Scoring / statistics ------------------------------------------------------

def score_for(item_type: str, category: str) -> float:
    return SCORE[item_type].get(category, 0.0)


def bootstrap_ci(values, n_boot=5000, seed=20260914):
    if not values:
        return (None, None)
    rng = random.Random(seed)
    means = []
    n = len(values)
    for _ in range(n_boot):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    return (round(means[int(0.025 * n_boot)], 3), round(means[int(0.975 * n_boot)] - 1e-12, 3))


def paired_lift_ci(pairs, n_boot=5000, seed=20260914):
    """pairs: list of (grounded_score, raw_score) for the same item. Bootstrap over items."""
    if not pairs:
        return (None, None, None)
    diffs = [g - r for g, r in pairs]
    mean = sum(diffs) / len(diffs)
    lo, hi = bootstrap_ci(diffs, n_boot, seed)
    return round(mean, 3), lo, hi


# -- Run -----------------------------------------------------------------------

def run(args):
    data = load_items()
    today = data["reference_date"]
    items = data["items"]
    if args.smoke:
        items = [i for i in items if i["id"] in SMOKE_ITEMS]
    if args.items:
        want = set(args.items.split(","))
        items = [i for i in items if i["id"] in want]
    arms = list(ARMS)
    if args.batch == "grounded":
        arms = [a for a in arms if ARMS[a]["grounded"]]
    elif args.batch == "raw":
        arms = [a for a in arms if not ARMS[a]["grounded"]]
    if args.arms:
        arms = [a.strip() for a in args.arms.split(",")]
        bad = [a for a in arms if a not in ARMS]
        if bad:
            sys.exit(f"Unknown arm(s): {bad}. Valid: {list(ARMS)}")
    nodes_by_id = load_nodes_by_id()

    ok, frozen_hash, actual_hash = item_file_hash_ok()
    est = estimate_cost(items, arms, nodes_by_id, today)
    print(f"Items: {len(items)} {[i['id'] for i in items]}")
    print(f"Arms:  {arms}")
    print(f"Item file sha256: {actual_hash}  frozen-manifest match: {ok}")
    print(f"Pre-run cost ESTIMATE: ${est['total_usd']} (per arm: {est['per_arm_usd']}); "
          f"prices/1M in,out: {PRICES}; cap this run: ${args.budget_cap:.2f}")
    if args.live:
        if not ok:
            sys.exit("REFUSING LIVE RUN: lift_items_v1.json hash does not match scripts/ci/frozen_artifact_manifest.json "
                     f"(frozen={frozen_hash}, actual={actual_hash}). The item set must be frozen before any arm runs.")
        if est["total_usd"] > args.budget_cap:
            sys.exit(f"REFUSING LIVE RUN: estimate ${est['total_usd']} exceeds this run's cap ${args.budget_cap:.2f}. "
                     "Use --batch grounded / --batch raw, fewer --arms, or raise --budget-cap deliberately.")
        keys = load_keys()
    else:
        keys = None

    started = datetime.now(timezone.utc)
    run_id = started.strftime("run_%Y%m%dT%H%M%SZ") + "_" + "-".join(a.replace("-", "") for a in arms)
    spent = 0.0
    records = []
    halted = None
    for arm in arms:
        cfg = ARMS[arm]
        judge_family = JUDGE_FOR_FAMILY[cfg["family"]]
        for it in items:
            if args.live and spent >= args.budget_cap:
                halted = f"budget cap ${args.budget_cap:.2f} reached after ${spent:.2f}; stopped before {arm}/{it['id']}"
                break
            sys_p, usr_p = build_answer_prompt(it, cfg, nodes_by_id, today)
            a = call_model(cfg["family"], sys_p, usr_p, keys, ANSWER_MAX_TOKENS, dry_answer(it, cfg), not args.live)
            spent += a["cost_usd"]
            answer_obj = lenient_parse_answer(a["_raw"]) if a["_raw"] else {}
            if a["error"] or not answer_obj.get("answer"):
                j = {"parsed": {"category": None, "names_missing_fact": None,
                                "rationale": f"answer call failed or unparseable: {a['error'] or 'no answer field'}"},
                     "_raw": "", "error": a["error"] or "unparseable", "usage": {"in": 0, "out": 0}, "cost_usd": 0.0,
                     "model": FAMILY_MODEL[judge_family], "skipped": True}
            else:
                j = call_model(judge_family, JUDGE_SYSTEM.replace("{today}", today), build_judge_prompt(it, answer_obj), keys, JUDGE_MAX_TOKENS,
                               dry_judgment(it, answer_obj, cfg), not args.live)
                spent += j["cost_usd"]
            jp = j["parsed"] if isinstance(j["parsed"], dict) else {}
            cat = jp.get("category")
            if cat not in CATEGORIES:
                cat = None
            rec = {
                "arm": arm, "model": cfg["model"], "grounded": cfg["grounded"], "item_id": it["id"],
                "item_type": it["type"], "state": it["state"], "depends_on_node_ids": it["depends_on_node_ids"],
                "answer": answer_obj, "answer_raw": a["_raw"], "answer_error": a["error"], "answer_usage": a["usage"],
                "answer_temperature_applied": a.get("temperature_applied"),
                "judge_model": j["model"], "judge_category": cat, "judge_names_missing_fact": jp.get("names_missing_fact"),
                "judge_rationale": jp.get("rationale"), "judge_raw": j["_raw"], "judge_error": j.get("error"),
                "score": score_for(it["type"], cat) if cat else None,
                "dd_wrong": cat == "wrong_dangerous",
                "cost_usd": round(a["cost_usd"] + j["cost_usd"], 4),
                "audited_category": None, "audit_note": None,
            }
            records.append(rec)
            print(f"  {arm:4s} {it['id']} [{it['type']:15s}] -> {cat or 'UNSCORED':18s} "
                  f"score={rec['score']}  ${rec['cost_usd']:.3f}  (run total ${spent:.2f})")
        if halted:
            print("HALTED:", halted)
            break

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out = {
        "_copyright": "Copyright 2026 Andrew M Cohen. Apache 2.0.",
        "run_id": run_id, "mode": "live" if args.live else "dry-run", "smoke": bool(args.smoke),
        "started_utc": started.isoformat(), "finished_utc": datetime.now(timezone.utc).isoformat(),
        "reference_date": today, "items": [i["id"] for i in items], "arms": arms,
        "item_file_sha256": actual_hash, "item_file_frozen_match": ok,
        "models": FAMILY_MODEL, "judge_rotation": JUDGE_FOR_FAMILY, "prices_per_1M_in_out": PRICES,
        "estimate_usd": est, "spent_usd_estimated": round(spent, 2), "budget_cap_usd": args.budget_cap, "halted": halted,
        "records": records,
    }
    path = RESULTS_DIR / f"{run_id}.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"\nWrote {path.relative_to(REPO_ROOT)}   spent (est.) ${spent:.2f}")
    if not args.live:
        print("DRY-RUN: no API calls were made; the run file is synthetic and should NOT be committed as a result.")
    return path


# -- Aggregate -----------------------------------------------------------------

def aggregate(args):
    files = sorted(RESULTS_DIR.glob("run_*.json"))
    runs = [json.loads(f.read_text()) for f in files]
    if args.live_only:
        runs = [r for r in runs if r.get("mode") == "live"]
    runs = [r for r in runs if not r.get("smoke")] if not args.include_smoke else runs
    if not runs:
        sys.exit("No run files to aggregate (after filters). Run the arms first.")
    data = load_items()
    items_by_id = {i["id"]: i for i in data["items"]}
    # Latest record wins per (arm, item)
    latest = {}
    for r in runs:
        for rec in r["records"]:
            latest[(rec["arm"], rec["item_id"])] = (r["run_id"], rec)
    recs = [rec for _, rec in latest.values()]

    def eff_cat(rec):
        return rec.get("audited_category") or rec.get("judge_category")

    def table(use_audit, exclude_errata=True):
        rows = {}
        for arm in ARMS:
            rs = [r for r in recs if r["arm"] == arm and (not exclude_errata or r["item_id"] not in ERRATA)]
            if not rs:
                continue
            cats = [(r, (eff_cat(r) if use_audit else r["judge_category"])) for r in rs]
            scores = [score_for(r["item_type"], c) for r, c in cats if c]
            unscored = sum(1 for _, c in cats if not c)
            dd = sum(1 for _, c in cats if c == "wrong_dangerous")
            by_type = {}
            for t in ("answerable", "abstain_correct", "trap"):
                ts = [score_for(r["item_type"], c) for r, c in cats if c and r["item_type"] == t]
                by_type[t] = round(sum(ts) / len(ts), 3) if ts else None
            abst = [(r, c) for r, c in cats if c in ("correct_abstention", "generic_abstention")]
            prec = (sum(1 for _, c in abst if c == "correct_abstention") / len(abst)) if abst else None
            rows[arm] = {"n": len(scores), "unscored": unscored, "mean": round(sum(scores) / len(scores), 3) if scores else None,
                         "ci": bootstrap_ci(scores), "dd": dd, "by_type": by_type,
                         "abstention_precision": round(prec, 3) if prec is not None else None,
                         "cats": {c: sum(1 for _, cc in cats if cc == c) for c in CATEGORIES}}
        lifts = {}
        for fam in "AOG":
            g, r_ = f"G-{fam}", f"R-{fam}"
            pairs, pairs_by_type = [], {"answerable": [], "abstain_correct": [], "trap": []}
            for iid in items_by_id:
                if exclude_errata and iid in ERRATA:
                    continue
                gr = next((x for x in recs if x["arm"] == g and x["item_id"] == iid), None)
                rr = next((x for x in recs if x["arm"] == r_ and x["item_id"] == iid), None)
                if not gr or not rr:
                    continue
                gc, rc = (eff_cat(gr), eff_cat(rr)) if use_audit else (gr["judge_category"], rr["judge_category"])
                if not gc or not rc:
                    continue
                p = (score_for(gr["item_type"], gc), score_for(rr["item_type"], rc))
                pairs.append(p)
                pairs_by_type[gr["item_type"]].append(p)
            lifts[fam] = {"n": len(pairs), "pooled": paired_lift_ci(pairs),
                          "by_type": {t: paired_lift_ci(v) for t, v in pairs_by_type.items()}}
        all_pairs = []
        for fam in "AOG":
            g, r_ = f"G-{fam}", f"R-{fam}"
            for iid in items_by_id:
                if exclude_errata and iid in ERRATA:
                    continue
                gr = next((x for x in recs if x["arm"] == g and x["item_id"] == iid), None)
                rr = next((x for x in recs if x["arm"] == r_ and x["item_id"] == iid), None)
                if gr and rr:
                    gc, rc = (eff_cat(gr), eff_cat(rr)) if use_audit else (gr["judge_category"], rr["judge_category"])
                    if gc and rc:
                        all_pairs.append((score_for(gr["item_type"], gc), score_for(rr["item_type"], rc)))
        lifts["pooled_all_models"] = {"n": len(all_pairs), "pooled": paired_lift_ci(all_pairs)}
        return rows, lifts

    raw_rows, raw_lifts = table(False, exclude_errata=True)
    aud_rows, aud_lifts = table(True, exclude_errata=False)
    audited_n = sum(1 for r in recs if r.get("audited_category"))
    modes = sorted({r.get("mode") for r in runs})
    spent = round(sum(r.get("spent_usd_estimated", 0) for r in runs), 2)

    def fmt_ci(ci):
        return f"[{ci[0]}, {ci[1]}]" if ci and ci[0] is not None else "n/a"

    L = []
    L.append("# D-5 lift ablation v1 -- results\n")
    L.append(f"*Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} by "
             f"`scripts/experiments/run_lift_ablation.py --aggregate` from {len(runs)} run file(s) "
             f"({', '.join(r['run_id'] for r in runs)}); modes: {modes}. Copyright 2026 Andrew M Cohen. Apache 2.0.*\n")
    if "dry-run" in modes:
        L.append("> **WARNING: at least one aggregated run is a DRY-RUN with synthetic responses. These numbers are not results.**\n")
    L.append("## Basis statement (for any use of the headline number)\n")
    n_items = len(items_by_id)
    L.append(f"Lift is measured on **{n_items} frozen items** (`scripts/experiments/lift_items_v1.json`, sha256 "
             f"`{runs[-1].get('item_file_sha256')}`; {data['item_type_proportion']['answerable']} answerable, "
             f"{data['item_type_proportion']['abstain_correct']} abstain-correct, {data['item_type_proportion']['trap']} trap), "
             f"reference date {data['reference_date']}, models {FAMILY_MODEL}, judge rotation {JUDGE_FOR_FAMILY} "
             f"(never the family under test), temperature 0 requested (accepted by: {sorted({r['model'] for r in recs if r.get('answer_temperature_applied')})}; "
             f"rejected, API default used: {sorted({r['model'] for r in recs if r.get('answer_temperature_applied') is False})}), "
             f"audit: {audited_n} of {len(recs)} judgments hand-reviewed so far (target: all DD-wrong + a random 20%). "
             f"**The headline 'grounded system' is arm G-A** (claude-opus-5 with the v1.0 node attached), per the design. "
             f"Estimated spend across aggregated runs: ${spent}. Known limitations: design s.8.\n")

    def render(rows, lifts, label):
        L.append(f"## {label}\n")
        L.append("| Arm | n | mean score | 95% CI (bootstrap) | DD-wrong | answerable | abstain-correct | trap | abstention precision | correct / c-abst / g-abst / wrong-safe / wrong-DD |")
        L.append("|---|---|---|---|---|---|---|---|---|---|")
        for arm, r in rows.items():
            c = r["cats"]
            L.append(f"| {arm} | {r['n']}{'+'+str(r['unscored'])+' unscored' if r['unscored'] else ''} | {r['mean']} | {fmt_ci(r['ci'])} | **{r['dd']}** | "
                     f"{r['by_type']['answerable']} | {r['by_type']['abstain_correct']} | {r['by_type']['trap']} | {r['abstention_precision']} | "
                     f"{c['correct']} / {c['correct_abstention']} / {c['generic_abstention']} / {c['wrong_safe']} / {c['wrong_dangerous']} |")
        L.append("")
        L.append("| Lift (G minus R, paired by item) | n pairs | pooled mean | 95% CI | answerable | abstain-correct | trap |")
        L.append("|---|---|---|---|---|---|---|")
        for fam in "AOG":
            lf = lifts[fam]
            p = lf["pooled"]
            bt = lf["by_type"]
            L.append(f"| {FAMILY_MODEL[fam]} | {lf['n']} | {p[0]} | {fmt_ci((p[1], p[2]))} | "
                     f"{bt['answerable'][0]} {fmt_ci((bt['answerable'][1], bt['answerable'][2]))} | "
                     f"{bt['abstain_correct'][0]} {fmt_ci((bt['abstain_correct'][1], bt['abstain_correct'][2]))} | "
                     f"{bt['trap'][0]} {fmt_ci((bt['trap'][1], bt['trap'][2]))} |")
        pa = lifts["pooled_all_models"]["pooled"]
        L.append(f"| **pooled, all three models** | {lifts['pooled_all_models']['n']} | **{pa[0]}** | {fmt_ci((pa[1], pa[2]))} | | | |")
        L.append("")

    if ERRATA:
        L.append("## Errata (defects found after the freeze; item file unchanged)\n")
        for iid, e in ERRATA.items():
            L.append(f"**{iid}** -- {e['defect']}\n")
            L.append(f"*Corrected ground truth (audited column only):* {e['corrected_ground_truth']}\n")
            L.append(f"*Corrected dangerous-direction error:* {e['corrected_dd_wrong_looks_like']}\n")
        L.append(f"Errata items are EXCLUDED from the raw-judge tables below (n = {n_items - len(ERRATA)} items). In the "
                 "audited tables they are INCLUDED, scored on Andy's ruling against the corrected ground truth; until Andy "
                 "rules, the audited column carries the raw judge's call for them, so the audited headline is provisional.\n")
    if JUDGE_ERRATA:
        L.append("## Judge errata (raw-judge column left as produced; resolved in the audited column)\n")
        for k, v in JUDGE_ERRATA.items():
            L.append(f"**{k}** -- {v}\n")
        L.append("Records flagged for priority audit: " + ", ".join(f"{a}/{i} ({k})" for (a, i), k in AUDIT_PRIORITY.items()) + ".\n")
    render(raw_rows, raw_lifts, f"Raw LLM-judge results (dual report, column 1; errata items excluded, n = {n_items - len(ERRATA)})")
    render(aud_rows, aud_lifts, f"Audited results (dual report, column 2; all {n_items} items) -- {audited_n} judgments overridden/confirmed by Andy so far")
    L.append("## Pre-registered predictions -- status\n")
    L.append("| # | Prediction | Raw-judge reading | Audited reading |")
    L.append("|---|---|---|---|")

    def pred_status(lifts):
        l1 = all((lifts[f]["pooled"][0] or 0) > 0 for f in "AOG") and all(
            (lifts[f]["by_type"]["trap"][0] or 0) >= max((lifts[f]["by_type"][t][0] or 0) for t in ("answerable", "abstain_correct")) for f in "AOG")
        return l1

    L.append(f"| L1 | Lift > 0 for all three models, largest on trap items | {'supported' if pred_status(raw_lifts) else 'not supported / mixed (see tables)'} | "
             f"{'supported' if pred_status(aud_lifts) else 'not supported / mixed (see tables)'} |")
    L.append("| L2 | Raw models abstain less and produce more DD-wrong answers on abstain-correct items | see DD-wrong and abstention columns above | same |")
    L.append("| L3 | Lift on answerable items smaller for the strongest raw model; value concentrates in abstention and traps | see by-type lift columns | same |")
    L.append("\n*Predictions L2/L3 are read off the tables by hand and recorded in the changelog; this generator does not adjudicate them.*\n")
    L.append("## Per-item results\n")
    L.append("| Item | Type | " + " | ".join(ARMS) + " |")
    L.append("|---|---|" + "---|" * len(ARMS))
    for iid, it in items_by_id.items():
        cells = []
        for arm in ARMS:
            r = next((x for x in recs if x["arm"] == arm and x["item_id"] == iid), None)
            if not r:
                cells.append("--")
                continue
            c = eff_cat(r) or "UNSCORED"
            mark = "" if not r.get("audited_category") else "*"
            cells.append(f"{c}{mark}")
        L.append(f"| {iid} | {it['type']} | " + " | ".join(cells) + " |")
    L.append("\n`*` = category set by Andy's audit (overrides the judge). Full answers, judge rationales and costs are in the run JSON files under `docs/experiments/results/lift_v1/`.\n")
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text("\n".join(L) + "\n")

    # Audit sample: every DD-wrong + random 20% of the rest (seeded), for Andy.
    rng = random.Random(20260914)
    def _prio(r):
        return r.get("judge_category") == "wrong_dangerous" or r["item_id"] in ERRATA or (r["arm"], r["item_id"]) in AUDIT_PRIORITY
    dd = [r for r in recs if _prio(r)]
    rest = [r for r in recs if r.get("judge_category") and not _prio(r)]
    k = max(1, round(0.2 * len(rest))) if rest else 0
    sample = dd + rng.sample(rest, k) if rest else dd
    A = ["# D-5 lift ablation v1 -- audit sample for Andy\n",
         f"*{len(dd)} dangerous-direction, errata-item and priority judgments (all included) + {k} random others (seed 20260914) = {len(sample)} of {len(recs)} judgments. "
         "For each: read the answer, read the judge's call, then write your ruling into the run JSON's `audited_category` "
         "(one of: correct, correct_abstention, generic_abstention, wrong_safe, wrong_dangerous) and `audit_note`, "
         "or hand the rulings to Cowork to enter. Re-run `--aggregate` afterwards; the audited column updates.*\n"]
    for r in sample:
        it = items_by_id[r["item_id"]]
        A.append(f"## {r['arm']} / {r['item_id']} ({it['type']}) -- judge: **{r['judge_category']}**\n")
        if (r["arm"], r["item_id"]) in AUDIT_PRIORITY:
            k = AUDIT_PRIORITY[(r["arm"], r["item_id"])]
            A.append(f"**PRIORITY -- suspected judge defect {k}:** {JUDGE_ERRATA[k]}\n")
        A.append(f"**Question:** {it['question']}\n")
        if r["item_id"] in ERRATA:
            A.append(f"**ERRATA ITEM -- rule against the CORRECTED ground truth:** {ERRATA[r['item_id']]['corrected_ground_truth']}\n")
        else:
            A.append(f"**Ground truth:** {it.get('ground_truth') or it.get('missing_dispositive_fact')}\n")
        A.append(f"**Answer ({r['model']}):** {(r['answer'] or {}).get('answer')}\n")
        A.append(f"abstain={ (r['answer'] or {}).get('abstain') }; missing_fact={ (r['answer'] or {}).get('missing_fact') }\n")
        A.append(f"**Judge ({r['judge_model']}) rationale:** {r['judge_rationale']}\n")
        A.append("**Andy's ruling:** [  ] confirm   [  ] override to: ______________   note: ______________\n")
    (RESULTS_DIR / "AUDIT_SAMPLE.md").write_text("\n".join(A) + "\n")
    # Review PDFs (Addendum s.2 standard): one entry per page for the audit sample; the results doc as-is.
    try:
        sys.path.insert(0, str(REPO_ROOT / "scripts" / "review"))
        from md_to_pdf import build as _pdf
        (REPO_ROOT / "review").mkdir(exist_ok=True)
        _pdf("\n".join(A) + "\n", str(REPO_ROOT / "review" / "D5_LIFT_AUDIT_SAMPLE.pdf"), "## ", True,
             "D-5 lift ablation -- audit sample for Andy")
        _pdf("\n".join(L) + "\n", str(REPO_ROOT / "review" / "D5_LIFT_V1_RESULTS.pdf"), None, False,
             "D-5 lift ablation v1 -- results")
        print("Wrote review/D5_LIFT_AUDIT_SAMPLE.pdf and review/D5_LIFT_V1_RESULTS.pdf")
    except Exception as exc:  # reportlab missing on this machine is not an error for the results
        print(f"(review PDFs not written: {exc}; Cowork regenerates them)")
    print(f"Wrote {SUMMARY_PATH.relative_to(REPO_ROOT)} and {(RESULTS_DIR / 'AUDIT_SAMPLE.md').relative_to(REPO_ROOT)}")
    print(f"Judgments: {len(recs)}; priority (DD-wrong + errata + judge-flagged): {len(dd)}; audit sample: {len(sample)}")


def rejudge(args):
    """Re-run ONLY judgments that came back unparseable/empty (judge_category None). If the answer JSON
    was invalid at run time, recover it first with lenient_parse_answer from answer_raw. Writes back
    into the same run file with a note. Live: a few cents each. Added 2026-09-15 (G-A/L16)."""
    data = load_items()
    items_by_id = {i["id"]: i for i in data["items"]}
    keys = load_keys() if not args.dry_run else None
    spent, fixed = 0.0, 0
    for f in sorted(RESULTS_DIR.glob("run_*.json")):
        d = json.loads(f.read_text())
        if d.get("mode") != "live" and not args.dry_run:
            continue
        changed = False
        for rec in d["records"]:
            if rec.get("judge_category") is not None:
                continue
            if not (rec.get("answer") or {}).get("answer") and rec.get("answer_raw"):
                recovered = lenient_parse_answer(rec["answer_raw"])
                if recovered.get("answer"):
                    rec["answer"] = recovered
                    rec["answer_error"] = None
                    rec["answer_recovery_note"] = "answer JSON was invalid at run time; fields recovered by lenient parse from answer_raw"
            if not (rec.get("answer") or {}).get("answer"):
                continue
            it = items_by_id[rec["item_id"]]
            cfg = ARMS[rec["arm"]]
            jf = JUDGE_FOR_FAMILY[cfg["family"]]
            j = call_model(jf, JUDGE_SYSTEM.replace("{today}", data["reference_date"]), build_judge_prompt(it, rec["answer"]), keys, JUDGE_MAX_TOKENS,
                           dry_judgment(it, rec["answer"], cfg), args.dry_run)
            spent += j["cost_usd"]
            jp = j["parsed"] if isinstance(j["parsed"], dict) else {}
            cat = jp.get("category") if jp.get("category") in CATEGORIES else None
            rec.update({"judge_category": cat, "judge_names_missing_fact": jp.get("names_missing_fact"),
                        "judge_rationale": jp.get("rationale"), "judge_raw": j["_raw"], "judge_error": j.get("error"),
                        "score": score_for(it["type"], cat) if cat else None, "dd_wrong": cat == "wrong_dangerous",
                        "cost_usd": round(rec.get("cost_usd", 0) + j["cost_usd"], 4),
                        "rejudged_utc": datetime.now(timezone.utc).isoformat(),
                        "rejudge_note": "first judgment empty/unparseable; re-run once with the same judge model and prompt"})
            print(f"  rejudged {rec['arm']} {rec['item_id']} -> {cat or 'STILL UNSCORED'}  ${j['cost_usd']:.3f}")
            fixed += 1
            changed = True
        if changed and args.dry_run:
            print(f"DRY-RUN: would update {f.relative_to(REPO_ROOT)} (not written)")
        elif changed:
            d["spent_usd_estimated"] = round(d.get("spent_usd_estimated", 0) + spent, 2)
            f.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
            print(f"Updated {f.relative_to(REPO_ROOT)}")
    print(f"Re-judged {fixed} record(s); spent (est.) ${spent:.2f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--live", action="store_true")
    mode.add_argument("--aggregate", action="store_true")
    mode.add_argument("--rejudge", action="store_true", help="re-run only empty/unparseable judgments (live; cents)")
    ap.add_argument("--smoke", action="store_true", help="3 items: L03 (answerable), L02 (abstain-correct), L01 (trap)")
    ap.add_argument("--arms", help="comma list, e.g. G-A,R-A")
    ap.add_argument("--batch", choices=["grounded", "raw"], help="run the three grounded or the three raw arms")
    ap.add_argument("--items", help="comma list of item ids")
    ap.add_argument("--budget-cap", type=float, default=15.0, help="USD hard cap for this invocation (default 15)")
    ap.add_argument("--live-only", action="store_true", help="(aggregate) ignore dry-run files")
    ap.add_argument("--rejudge-dry", dest="dry_run", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--include-smoke", action="store_true", help="(aggregate) include smoke runs")
    args = ap.parse_args()
    if args.aggregate:
        return aggregate(args)
    if args.rejudge:
        return rejudge(args)
    if not (args.dry_run or args.live):
        ap.error("choose --dry-run, --live or --aggregate")
    run(args)


if __name__ == "__main__":
    main()
