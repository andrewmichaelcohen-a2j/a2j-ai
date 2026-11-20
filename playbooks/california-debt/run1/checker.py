#!/usr/bin/env python3
"""Run 1 Checker for the California debt playbook slice.

What it does
  For each test item, it sends the draft answer plus the saved source text to an OpenAI
  model and asks it to check every claim against ONLY those sources. It then verifies,
  in plain code, that each quote the model gives really appears in the saved source text.
  It writes a readable report. It never edits an item and never approves one.

Safety
  * With no flags it only estimates cost. It calls nothing.
  * Real calls need --run.
  * The API key is read from the environment variable OPENAI_API_KEY. It is never written to a file.
  * A hard budget stops the run before any call that could push total estimated spend over it.

Needs only Python 3 (standard library). No installs.
"""
import argparse
import datetime
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # playbooks/california-debt
ITEMS_FILE = os.path.join(HERE, "items.json")
SOURCE_FILES = [
    (os.path.join(ROOT, "sources", "ca-statutes-2026-11-19.md"), ""),
    (os.path.join(ROOT, "sources", "ca-statutes-effective-2027-01-01.md"), "@2027"),
    (os.path.join(ROOT, "sources", "ca-holidays-federal-2026-11-19.md"), ""),
    (os.path.join(ROOT, "sources", "reference-checks-2026-11-19.md"), ""),
    (os.path.join(ROOT, "sources", "forms", "ca-forms-2026-11-19.md"), ""),
]
RESULTS_DIR = os.path.join(HERE, "results")
LEDGER = os.path.join(HERE, "spend-log.tsv")
DECISION_LOG = os.path.join(HERE, "decision-log.tsv")
TODAY = "2026-11-19"

# USD per 1M tokens (input, output), from third-party reports of OpenAI's Nov 17, 2026 launch.
# Check them against OpenAI's pricing page. These are estimates, not your bill.
PRICES = {"gpt-6.2-astra": (8.0, 40.0), "gpt-6.2-sol": (2.0, 10.0)}
EXPECTED_OUT_TOKENS = 5000  # for the dry-run estimate only

SCHEMA = {
    "type": "object",
    "properties": {
        "label": {"type": "string", "enum": ["Source-read", "Lawyers differ", "Not yet checked"]},
        "claims": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "claim": {"type": "string"},
                    "supported": {"type": "string", "enum": ["yes", "partly", "no", "source_not_provided"]},
                    "source_id": {"type": "string"},
                    "quote": {"type": "string"},
                    "note": {"type": "string"},
                },
                "required": ["claim", "supported", "source_id", "quote", "note"],
                "additionalProperties": False,
            },
        },
        "flags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string",
                             "enum": ["error", "gap", "overbroad", "advice_like", "harm_risk", "date_change", "other"]},
                    "text": {"type": "string"},
                },
                "required": ["type", "text"],
                "additionalProperties": False,
            },
        },
        "summary": {"type": "string"},
    },
    "required": ["label", "claims", "flags", "summary"],
    "additionalProperties": False,
}

INSTRUCTIONS = (
    "You are the Checker in a fact-checking pipeline for a public-information playbook for people "
    "sued over consumer debt in California. Your only job is to test whether each claim in a draft "
    "answer is supported by the source texts provided. Rules:\n"
    "1. Use ONLY the source texts provided. Never use memory or outside knowledge as support. If a claim "
    "needs a source that was not provided, mark it supported=\"source_not_provided\".\n"
    "2. Break the draft answer into its separate factual claims (each number, deadline, condition, "
    "exception, form name and instruction).\n"
    "3. For each claim, copy a supporting quote EXACTLY, character for character, from one provided "
    "source (at most 400 characters), and give that source's id. If no quote supports the claim, leave "
    "the quote empty.\n"
    "4. supported values: \"yes\" = the quote fully supports the claim as worded; \"partly\" = the "
    "source supports less than the draft says, or the draft omits a condition or exception that would "
    "change the practical answer; \"no\" = the source contradicts the claim or says nothing about it.\n"
    "5. Add flags for: error, gap, overbroad statements, advice-like wording aimed at one person's "
    "situation, and anything that could push a person toward a harmful move (the draft's harm_flag "
    "says what the harm is). Today's date is " + TODAY + ". Source ids ending in @2027 are versions "
    "that take effect on January 1, 2027. Check the draft against the version in effect today. If the "
    "2027 version differs in a way that matters, add a flag of type date_change.\n"
    "6. label: \"Source-read\" only if every claim is \"yes\" with a quote. \"Lawyers differ\" only if the "
    "provided sources themselves allow competing readings. Otherwise \"Not yet checked\". Never assign "
    "any other label.\n"
    "7. Judge the draft within the scope stated in applies_when. Do not mark a claim \"partly\" or add an "
    "overbroad flag only because the draft leaves out an exception that applies outside that stated scope. "
    "Do flag it when applies_when itself is too broad, when the draft omits a condition that matters inside "
    "that scope, or when the draft says more than the source says.\n"
    "8. Do not rewrite or improve the answer. Do not approve it. Be concise."
)


KEY_FILE = os.path.join(os.path.expanduser("~"), ".config", "cjac", "openai_key")


def get_key():
    """The private key file wins; the OPENAI_API_KEY environment variable is the fallback.
    (File first, so an old key left over in a Terminal window can never override a freshly saved one.)"""
    key, source = "", ""
    if os.path.exists(KEY_FILE):
        key = open(KEY_FILE, encoding="utf-8").read()
        source = KEY_FILE
    if not key.strip():
        key = os.environ.get("OPENAI_API_KEY", "")
        source = "this Terminal's environment"
    key = re.sub(r"[\s\"']", "", key)
    return key, source


def norm(s):
    s = s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip().lower()


def load_sources():
    sources = {}
    for path, suffix in SOURCE_FILES:
        if not os.path.exists(path):
            print("Missing source file: " + path)
            sys.exit(1)
        cur, buf = None, []
        for line in open(path, encoding="utf-8").read().split("\n"):
            m = re.match(r"^## (\S+)", line)
            if m:
                if cur:
                    sources[cur] = "\n".join(buf).strip()
                cur, buf = m.group(1) + suffix, []
            elif line.strip() == "---":
                if cur:
                    sources[cur] = "\n".join(buf).strip()
                cur, buf = None, []
            elif cur:
                buf.append(line)
        if cur:
            sources[cur] = "\n".join(buf).strip()
    return sources


def build_request(item, ref, sources, model, effort, max_out):
    provided = {sid: sources[sid] for sid in item["sources_available"] if sid in sources}
    payload = {
        "item_ref": ref,
        "question_the_answer_responds_to": item["question"],
        "draft_answer": item["answer"],
        "applies_when": item["applies_when"],
        "harm_flag": item["harm_flag"],
        "citations_named_in_draft": item["cited_in_draft"],
        "sources_provided": provided,
        "sources_named_but_not_provided": item["sources_not_available"],
    }
    body = {
        "model": model,
        "input": [
            {"role": "developer", "content": INSTRUCTIONS},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False, indent=1)},
        ],
        "reasoning": {"effort": effort},
        "max_output_tokens": max_out,
        "text": {"format": {"type": "json_schema", "name": "checker_result", "strict": True, "schema": SCHEMA}},
    }
    chars = len(INSTRUCTIONS) + len(body["input"][1]["content"]) + len(json.dumps(SCHEMA))
    return body, int(chars / 3.2) + 200  # conservative token estimate


def cost(model, tin, tout):
    pin, pout = PRICES.get(model, PRICES["gpt-6.2-astra"])
    return (tin * pin + tout * pout) / 1e6


def ledger_total():
    if not os.path.exists(LEDGER):
        return 0.0
    total = 0.0
    for line in open(LEDGER, encoding="utf-8").read().split("\n")[1:]:
        parts = line.split("\t")
        if len(parts) >= 6:
            try:
                total += float(parts[5])
            except ValueError:
                pass
    return total


def ledger_add(ref, model, tin, tout):
    new = not os.path.exists(LEDGER)
    with open(LEDGER, "a", encoding="utf-8") as f:
        if new:
            f.write("timestamp\titem_ref\tmodel\tinput_tokens\toutput_tokens\test_cost_usd\n")
        f.write("%s\t%s\t%s\t%d\t%d\t%.4f\n" % (datetime.datetime.now().isoformat(timespec="seconds"),
                                              ref, model, tin, tout, cost(model, tin, tout)))


def decision_log(decision, why, evidence, result):
    new = not os.path.exists(DECISION_LOG)
    with open(DECISION_LOG, "a", encoding="utf-8") as f:
        if new:
            f.write("timestamp\tphase\tdecision\twhy\tevidence\tresult\n")
        row = [datetime.datetime.now().isoformat(timespec="seconds"), "run1", decision, why, evidence, result]
        f.write("\t".join(x.replace("\t", " ").replace("\n", " ") for x in row) + "\n")


def call_openai(body, key):
    data = json.dumps(body).encode("utf-8")
    delay = 5
    for attempt in range(4):
        req = urllib.request.Request(
            "https://api.openai.com/v1/responses", data=data, method="POST",
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=420) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            text = e.read().decode("utf-8", "replace")
            if e.code in (429, 503) and attempt < 3 and "insufficient_quota" not in text \
                    and "credit_balance_exhausted" not in text:
                wait = int(e.headers.get("Retry-After") or delay)
                print("   OpenAI asked us to wait (HTTP %d). Waiting %ds, then retrying." % (e.code, wait))
                time.sleep(wait)
                delay *= 3
                continue
            print("   OpenAI error HTTP %d: %s" % (e.code, text[:600]))
            return None
        except urllib.error.URLError as e:
            print("   Network error: %s" % e)
            if attempt < 3:
                time.sleep(delay)
                delay *= 3
                continue
            return None
    return None


def extract(resp):
    """Return (parsed_result, raw_text, input_tokens, output_tokens, problem)."""
    usage = resp.get("usage", {}) or {}
    tin, tout = int(usage.get("input_tokens", 0)), int(usage.get("output_tokens", 0))
    if resp.get("status") == "incomplete":
        reason = (resp.get("incomplete_details") or {}).get("reason", "unknown")
        return None, "", tin, tout, "response incomplete (" + reason + ")"
    text = ""
    for out in resp.get("output", []) or []:
        if out.get("type") == "message":
            for c in out.get("content", []) or []:
                if c.get("type") == "output_text":
                    text += c.get("text", "")
                elif c.get("type") == "refusal":
                    return None, "", tin, tout, "model refused: " + str(c.get("refusal"))[:200]
    try:
        return json.loads(text), text, tin, tout, None
    except ValueError:
        return None, text, tin, tout, "could not parse the model's JSON"


def mock_response(item, sources):
    sid = item["sources_available"][0] if item["sources_available"] else ""
    real = ""
    if sid:
        body = [l for l in sources[sid].split("\n") if len(l) > 60]
        real = body[0][:120] if body else ""
    out = {"label": "Source-read",
           "claims": [{"claim": "mock claim with a real quote", "supported": "yes", "source_id": sid, "quote": real, "note": ""},
                      {"claim": "mock claim with an invented quote", "supported": "yes", "source_id": sid,
                       "quote": "This sentence does not appear in any source.", "note": ""}],
           "flags": [], "summary": "mock"}
    return {"status": "completed", "usage": {"input_tokens": 3000, "output_tokens": 1500},
            "output": [{"type": "message", "content": [{"type": "output_text", "text": json.dumps(out)}]}]}


def verify(result, item, sources):
    claims = result.get("claims", [])
    for c in claims:
        q = c.get("quote", "")
        if not q:
            c["quote_verified"] = None
            continue
        sid = c.get("source_id", "")
        hay = norm(sources[sid]) if sid in sources else " ".join(norm(sources[s]) for s in item["sources_available"] if s in sources)
        c["quote_verified"] = norm(q) in hay
    bad_flags = [f for f in result.get("flags", []) if f["type"] in ("error", "gap", "overbroad", "harm_risk")]
    all_yes = bool(claims) and all(c["supported"] == "yes" and c.get("quote_verified") for c in claims)
    reasons = []
    final = result["label"]
    if final == "Source-read":
        if not item["sources_available"]:
            final, reasons = "Not yet checked", ["no source text available"]
        elif not all_yes:
            final = "Not yet checked"
            if any(c.get("quote_verified") is False for c in claims):
                reasons.append("a quoted passage was not found in the saved source text")
            if any(c["supported"] != "yes" for c in claims):
                reasons.append("not every claim is fully supported")
            if not claims:
                reasons.append("no claims listed")
        elif bad_flags:
            final, reasons = "Not yet checked", ["the Checker raised error, gap or overbroad flags"]
    caught = bool(bad_flags) or any(c["supported"] in ("partly", "no") for c in claims)
    return {"model_label": result["label"], "final_label": final, "downgrade_reasons": reasons,
            "seeded_error_caught": caught if (item.get("private_notes") or {}).get("seeded") else None}


def check_key():
    key, source = get_key()
    print("Key found: %s" % (("yes, from " + source) if key else "NO"))
    if not key:
        print("Run:  bash " + os.path.join(HERE, "setup-key.sh"))
        return
    print("Length: %d characters. Starts with: %s" % (len(key), key[:3] + "..."))
    if len(key) < 40:
        print("WARNING: that is shorter than a normal OpenAI key. It may be cut off.")
    req = urllib.request.Request("https://api.openai.com/v1/models", headers={"Authorization": "Bearer " + key})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("OpenAI accepted the key (HTTP %d). Nothing was spent." % r.status)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            msg = json.loads(body).get("error", {}).get("message", body)
        except ValueError:
            msg = body
        print("OpenAI returned HTTP %d." % e.code)
        print("OpenAI says: " + str(msg)[:500])
        print("(If it mentions missing scopes or permissions, the key is a restricted key. Create one with All permissions.)")
        print("(If it says the key is incorrect, the paste or the key itself is wrong, or it came from another service.)")
    except urllib.error.URLError as e:
        print("Could not reach OpenAI: %s" % e)


def main():
    ap = argparse.ArgumentParser(description="Run 1 Checker. With no flags it only estimates cost.")
    ap.add_argument("--check-key", action="store_true", help="check the key works (free)")
    ap.add_argument("--run", action="store_true", help="make real OpenAI calls (costs money)")
    ap.add_argument("--mock", action="store_true", help="use fake responses to test the code (free)")
    ap.add_argument("--only", help="comma-separated item ids, e.g. D-11-SEEDED")
    ap.add_argument("--model", default="gpt-6.2-astra")
    ap.add_argument("--effort", default="medium", choices=["low", "medium", "high"])
    ap.add_argument("--max-output-tokens", type=int, default=10000)
    ap.add_argument("--budget", type=float, default=15.0, help="stop if total estimated spend would exceed this (USD)")
    ap.add_argument("--redo", action="store_true", help="re-check items that already have results")
    ap.add_argument("--dir", default=HERE, help="folder holding items.json and results/ (default: run1; use ../run2 for Run 2)")
    a = ap.parse_args()
    global ITEMS_FILE, RESULTS_DIR
    ITEMS_FILE = os.path.join(os.path.abspath(a.dir), "items.json")
    RESULTS_DIR = os.path.join(os.path.abspath(a.dir), "results")

    if a.check_key:
        check_key()
        return

    sources = load_sources()
    items = json.load(open(ITEMS_FILE, encoding="utf-8"))["items"]
    if a.only:
        want = set(x.strip() for x in a.only.split(","))
        items = [i for i in items if i["id"] in want]
        if not items:
            print("No matching item ids.")
            return
    os.makedirs(RESULTS_DIR, exist_ok=True)

    key, _src = get_key()
    real = a.run and not a.mock
    if real and not key:
        print("No OpenAI key found. Run:  bash " + os.path.join(HERE, "setup-key.sh"))
        return

    plan, worst_total, exp_total = [], 0.0, 0.0
    all_items = json.load(open(ITEMS_FILE, encoding="utf-8"))["items"]
    print("Model: %s | effort: %s | max output tokens per call: %d\n" % (a.model, a.effort, a.max_output_tokens))
    print("%-14s %-8s %10s %14s %14s" % ("item", "ref", "input_tok", "worst_case_$", "expected_$"))
    for it in items:
        ref = "X%02d" % (all_items.index(it) + 1)  # blinded reference sent to the model
        body, tin = build_request(it, ref, sources, a.model, a.effort, a.max_output_tokens)
        w, e = cost(a.model, tin, a.max_output_tokens), cost(a.model, tin, EXPECTED_OUT_TOKENS)
        worst_total += w
        exp_total += e
        plan.append((it, ref, body, tin))
        print("%-14s %-8s %10d %14.3f %14.3f" % (it["id"], ref, tin, w, e))
    spent = ledger_total()
    print("\nTotal: expected about $%.2f, worst case $%.2f. Already logged as spent: $%.2f. Budget: $%.2f."
          % (exp_total, worst_total, spent, a.budget))
    print("These are estimates, not your bill. Check usage on OpenAI's site.")
    if not a.run:
        print("\nDry run only. Nothing was sent. Add --run to make real calls.")
        return

    done = 0
    for it, ref, body, tin in plan:
        out_path = os.path.join(RESULTS_DIR, it["id"] + ".json")
        if os.path.exists(out_path) and not a.redo:
            print("Skipping %s (already has a result; use --redo to repeat)." % it["id"])
            continue
        remaining = a.budget - ledger_total()
        w = cost(a.model, tin, a.max_output_tokens)
        if w > remaining:
            print("STOP: the worst case for %s ($%.2f) could pass the remaining budget ($%.2f)." % (it["id"], w, remaining))
            break
        print("Checking %s ..." % it["id"])
        if a.mock:
            resp = mock_response(it, sources)
        else:
            resp = call_openai(body, key)
        if resp is None:
            print("   No usable response. Stopping so you can look at the error above.")
            break
        parsed, raw, tin_a, tout_a, problem = extract(resp)
        ledger_add(ref, a.model if not a.mock else "mock", tin_a, tout_a)
        if problem:
            print("   Problem: " + problem)
            json.dump({"id": it["id"], "ref": ref, "problem": problem, "raw": raw}, open(out_path + ".problem", "w"), indent=1)
            decision_log("problem on " + it["id"], problem, "tokens in/out %d/%d" % (tin_a, tout_a), "no result saved")
            continue
        chk = verify(parsed, it, sources)
        rec = {"id": it["id"], "ref": ref, "model": a.model, "result": parsed, "checks": chk,
               "usage": {"input_tokens": tin_a, "output_tokens": tout_a},
               "est_cost_usd": round(cost(a.model, tin_a, tout_a), 4)}
        json.dump(rec, open(out_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        decision_log("checked " + it["id"], "Run 1 Checker pass", "results/" + it["id"] + ".json",
                     "final label: " + chk["final_label"])
        done += 1
        print("   label: %s (model said %s) | flags: %d" % (chk["final_label"], chk["model_label"], len(parsed["flags"])))
    write_report()
    print("\nDone. %d item(s) checked this time. Estimated total spend so far: $%.2f." % (done, ledger_total()))
    print("Open this file to read the results:\n  " + os.path.join(RESULTS_DIR, "RESULTS.md"))


def write_report():
    recs = []
    for fn in sorted(os.listdir(RESULTS_DIR)):
        if fn.endswith(".json"):
            recs.append(json.load(open(os.path.join(RESULTS_DIR, fn), encoding="utf-8")))
    L = ["# Checker results: " + os.path.basename(os.path.dirname(RESULTS_DIR)), "",
         "Generated by checker.py. AI checks catch errors and unsupported claims. They do not show the law is right. "
         "Quotes marked verified were found word for word in the saved source text.", "",
         "Estimated spend so far: $%.2f" % ledger_total(), "",
         "| Item | Checker label | Final label | Claims fully supported | Flags | Seeded error |",
         "| --- | --- | --- | --- | --- | --- |"]
    for r in recs:
        cl = r["result"]["claims"]
        ok = sum(1 for c in cl if c["supported"] == "yes" and c.get("quote_verified"))
        seeded = r["checks"]["seeded_error_caught"]
        L.append("| %s | %s | %s | %d of %d | %d | %s |" % (
            r["id"], r["checks"]["model_label"], r["checks"]["final_label"], ok, len(cl), len(r["result"]["flags"]),
            "n/a" if seeded is None else ("CAUGHT" if seeded else "MISSED")))
    L += ["", "## Details", ""]
    for r in recs:
        L += ["### " + r["id"], "", "Summary: " + r["result"]["summary"], ""]
        if r["checks"]["downgrade_reasons"]:
            L.append("Downgraded to Not yet checked because: " + "; ".join(r["checks"]["downgrade_reasons"]))
            L.append("")
        for f in r["result"]["flags"]:
            L.append("- **%s:** %s" % (f["type"], f["text"]))
        for c in r["result"]["claims"]:
            mark = {True: "quote verified", False: "QUOTE NOT FOUND in source", None: "no quote"}[c.get("quote_verified")]
            L.append("- Claim (%s, %s): %s" % (c["supported"], mark, c["claim"]))
        L.append("")
    open(os.path.join(RESULTS_DIR, "RESULTS.md"), "w", encoding="utf-8").write("\n".join(L))


if __name__ == "__main__":
    main()
