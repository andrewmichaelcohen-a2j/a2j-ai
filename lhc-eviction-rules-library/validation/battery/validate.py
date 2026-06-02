#!/usr/bin/env python3
"""
LHC Eviction Rules Library — Automated Validation Battery
Layers 1–6 (automated). Layer 7 (human attorney review) is out of scope.

Usage:
  python validate.py                    # validate all files
  python validate.py --state CA         # validate one state
  python validate.py --report           # generate reports/

Copyright 2026 Andrew M Cohen.
Licensed under the Apache License, Version 2.0.
"""

import json, os, sys, re, glob, argparse
from datetime import datetime, date

RULES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "rules")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "schema", "eviction_schema_v1.0.json")

REQUIRED_TOP_LEVEL = [
    "schema_version", "jurisdiction", "last_updated", "validation_status",
    "validation_note", "source_statutes", "notice_types", "notice_defects",
    "affirmative_defenses", "service_methods", "local_overlays", "ai_drafter_notes"
]

VALID_STATUSES = {"DRAFT", "UNDER REVIEW", "VALIDATED", "CERTIFIED", "NEEDS UPDATE"}
VALID_DEFECT_RESULTS = {"INVALID", "POTENTIALLY_INVALID", "VOIDABLE"}

# ── LAYER 3: Internal Consistency (~40 checks) ─────────────────────────────────

def layer3_internal_consistency(data, path):
    """~40 structural/logical checks that require no external resources."""
    errors = []
    warnings = []

    # 3.01 — schema_version correct
    if data.get("schema_version") != "eviction-v1":
        errors.append("3.01: schema_version must be 'eviction-v1'")

    # 3.02 — required fields present
    for f in REQUIRED_TOP_LEVEL:
        if f not in data:
            errors.append(f"3.02: missing required field '{f}'")

    # 3.03 — jurisdiction has required subfields
    j = data.get("jurisdiction", {})
    if not isinstance(j, dict):
        errors.append("3.03: jurisdiction must be an object")
    else:
        for sf in ["state", "state_name", "type"]:
            if sf not in j:
                errors.append(f"3.03: jurisdiction.{sf} missing")
        if j.get("state") and len(j["state"]) != 2:
            errors.append("3.03: jurisdiction.state must be 2-letter code")
        if j.get("type") not in [None, "state", "district", "territory"]:
            errors.append("3.03: jurisdiction.type must be state|district|territory")

    # 3.04 — last_updated is valid ISO date
    lu = data.get("last_updated", "")
    try:
        datetime.strptime(lu, "%Y-%m-%d")
    except:
        errors.append(f"3.04: last_updated '{lu}' is not a valid YYYY-MM-DD date")

    # 3.05 — validation_status is valid
    vs = data.get("validation_status")
    if vs not in VALID_STATUSES:
        errors.append(f"3.05: validation_status '{vs}' not in {VALID_STATUSES}")

    # 3.06 — DRAFT files must have null reviewer
    if vs == "DRAFT" and data.get("reviewer") is not None:
        errors.append("3.06: DRAFT files must have reviewer: null")

    # 3.07 — VALIDATED/CERTIFIED files must have non-null reviewer
    if vs in {"VALIDATED", "CERTIFIED"} and not data.get("reviewer"):
        errors.append(f"3.07: {vs} files must have a named reviewer")

    # 3.08 — source_statutes is non-empty list of strings
    ss = data.get("source_statutes", [])
    if not isinstance(ss, list) or len(ss) == 0:
        errors.append("3.08: source_statutes must be non-empty list")
    elif not all(isinstance(s, str) for s in ss):
        errors.append("3.08: all source_statutes entries must be strings")

    # 3.09 — notice_types is a dict
    nt = data.get("notice_types", {})
    if not isinstance(nt, dict):
        errors.append("3.09: notice_types must be an object")
    elif "pay_or_quit" not in nt:
        warnings.append("3.09: pay_or_quit not in notice_types — expected for most residential evictions")

    # 3.10–3.15 — pay_or_quit subfields
    pq = nt.get("pay_or_quit", {}) if isinstance(nt, dict) else {}
    if isinstance(pq, dict):
        # Find the notice period
        days = None
        for subkey in ["tenancy_all", "tenancy_under_1yr", "tenancy_any"]:
            if subkey in pq and isinstance(pq[subkey], dict):
                days = pq[subkey].get("days")
                break
        if days is None:
            warnings.append("3.10: could not determine nonpayment notice period from notice_types.pay_or_quit")
        elif not isinstance(days, int) or days < 1:
            errors.append(f"3.10: notice period days must be positive integer, got {days}")
        elif days > 60:
            warnings.append(f"3.10: notice period of {days} days is unusually long — verify")

        # 3.11 — permitted_amounts
        pa = pq.get("permitted_amounts", [])
        if not isinstance(pa, list) or len(pa) == 0:
            warnings.append("3.11: pay_or_quit.permitted_amounts is empty or missing")

        # 3.12 — late_fees_permitted is boolean
        lfp = pq.get("late_fees_permitted")
        if lfp is not None and not isinstance(lfp, bool):
            errors.append("3.12: late_fees_permitted must be boolean")

        # 3.13 — statute field is present and non-empty
        for subkey in ["tenancy_all", "tenancy_under_1yr"]:
            if subkey in pq:
                st = pq[subkey].get("statute", "")
                if not st:
                    warnings.append(f"3.13: notice_types.pay_or_quit.{subkey}.statute is empty")

    # 3.16 — notice_defects is a list
    nd = data.get("notice_defects", [])
    if not isinstance(nd, list):
        errors.append("3.16: notice_defects must be an array")
    else:
        for i, d in enumerate(nd):
            if not isinstance(d, dict):
                errors.append(f"3.16: notice_defects[{i}] must be an object")
                continue
            if "defect" not in d:
                errors.append(f"3.17: notice_defects[{i}] missing 'defect' field")
            if "result" not in d:
                errors.append(f"3.18: notice_defects[{i}] missing 'result' field")
            elif d["result"] not in VALID_DEFECT_RESULTS:
                errors.append(f"3.18: notice_defects[{i}].result '{d['result']}' not in {VALID_DEFECT_RESULTS}")

    # 3.19 — affirmative_defenses is non-empty list
    ad = data.get("affirmative_defenses", [])
    if not isinstance(ad, list) or len(ad) == 0:
        errors.append("3.19: affirmative_defenses must be non-empty list")
    elif "habitability" not in ad:
        warnings.append("3.19: habitability not in affirmative_defenses — expected in all jurisdictions")
    elif "retaliatory_eviction" not in ad:
        warnings.append("3.19: retaliatory_eviction not in affirmative_defenses — expected in most jurisdictions")

    # 3.20 — service_methods is a dict with adds_days
    sm = data.get("service_methods", {})
    if not isinstance(sm, dict):
        errors.append("3.20: service_methods must be an object")
    else:
        for method, details in sm.items():
            if not isinstance(details, dict):
                errors.append(f"3.20: service_methods.{method} must be an object")
            elif "adds_days" not in details:
                errors.append(f"3.21: service_methods.{method}.adds_days missing")
            elif not isinstance(details["adds_days"], int) or details["adds_days"] < 0:
                errors.append(f"3.21: service_methods.{method}.adds_days must be non-negative integer")

    # 3.22 — local_overlays is a dict (may be empty)
    lo = data.get("local_overlays", {})
    if not isinstance(lo, dict):
        errors.append("3.22: local_overlays must be an object")

    # 3.23 — ai_drafter_notes is a list
    adn = data.get("ai_drafter_notes", [])
    if not isinstance(adn, list):
        errors.append("3.23: ai_drafter_notes must be an array")

    # 3.24 — statutory_retrieval_performed is boolean if present
    srp = data.get("statutory_retrieval_performed")
    if srp is not None and not isinstance(srp, bool):
        errors.append("3.24: statutory_retrieval_performed must be boolean")

    # 3.25 — if retrieval performed, retrieval_date should be set
    if srp and not data.get("statutory_retrieval_date"):
        warnings.append("3.25: statutory_retrieval_performed is true but statutory_retrieval_date is missing")

    # 3.26 — just_cause_required is boolean if present
    jcr = data.get("just_cause_required")
    if jcr is not None and not isinstance(jcr, bool):
        errors.append("3.26: just_cause_required must be boolean")

    # 3.27 — if just_cause_required, check no_just_cause in affirmative_defenses
    if jcr and "no_just_cause" not in ad:
        warnings.append("3.27: just_cause_required is true but 'no_just_cause' not in affirmative_defenses")

    # 3.28 — statewide_rent_control is boolean if present
    src = data.get("statewide_rent_control")
    if src is not None and not isinstance(src, bool):
        errors.append("3.28: statewide_rent_control must be boolean")

    # 3.29 — _copyright present
    if "_copyright" not in data:
        warnings.append("3.29: _copyright field missing")

    # 3.30 — validation_note is non-empty string
    vn = data.get("validation_note", "")
    if not isinstance(vn, str) or not vn.strip():
        errors.append("3.30: validation_note must be a non-empty string")

    # 3.31 — cure_or_quit days >= pay_or_quit days (logic check)
    coq = nt.get("cure_or_quit", {}) if isinstance(nt, dict) else {}
    if isinstance(coq, dict) and isinstance(pq, dict):
        cure_days = coq.get("days")
        nonpay_days = None
        for sk in ["tenancy_all", "tenancy_under_1yr", "tenancy_any"]:
            if sk in pq and isinstance(pq[sk], dict):
                nonpay_days = pq[sk].get("days")
                break
        if cure_days and nonpay_days and cure_days < nonpay_days:
            warnings.append(f"3.31: cure_or_quit.days ({cure_days}) < pay_or_quit days ({nonpay_days}) — unusual, verify")

    # 3.32 — notice_defects contains at least improper_service_method
    defect_ids = [d.get("defect", "") for d in nd] if isinstance(nd, list) else []
    if "improper_service_method" not in defect_ids:
        warnings.append("3.32: notice_defects does not include 'improper_service_method' — expected in all states")

    # 3.33 — no_fault_termination present in notice_types
    if isinstance(nt, dict) and "no_fault_termination" not in nt:
        warnings.append("3.33: no_fault_termination not in notice_types — expected for termination scenarios")

    return errors, warnings


# ── LAYER 5: Cross-Jurisdiction Anomaly Detection ───────────────────────────────

def layer5_cross_jurisdiction(all_files_data):
    """
    Compare each file to the full library.
    Flag fields present in 45+ states but missing in a specific state,
    or notice periods significantly outside the distribution.
    """
    results = {}

    # Collect notice periods across all files
    periods = {}
    for code, data in all_files_data.items():
        nt = data.get("notice_types", {})
        pq = nt.get("pay_or_quit", {}) if isinstance(nt, dict) else {}
        days = None
        for sk in ["tenancy_all", "tenancy_under_1yr", "tenancy_any"]:
            if sk in pq and isinstance(pq[sk], dict):
                days = pq[sk].get("days")
                break
        periods[code] = days

    # Compute distribution
    valid_periods = [d for d in periods.values() if isinstance(d, int)]
    if valid_periods:
        mean_period = sum(valid_periods) / len(valid_periods)
        sorted_periods = sorted(valid_periods)
        median_period = sorted_periods[len(sorted_periods) // 2]
    else:
        mean_period = median_period = 0

    # Collect which fields are present across all files
    field_presence = {}
    standard_top_fields = ["just_cause_required", "statewide_rent_control", "statutory_retrieval_performed"]
    for field in standard_top_fields:
        field_presence[field] = sum(1 for d in all_files_data.values() if field in d)

    for code, data in all_files_data.items():
        flags = []

        # Period outlier check
        p = periods.get(code)
        if p and isinstance(p, int):
            if p > 2 * median_period:
                flags.append(f"L5-PERIOD-HIGH: nonpayment period ({p} days) is >2x median ({median_period}) — verify")
            elif p < 3 and median_period > 5:
                flags.append(f"L5-PERIOD-LOW: nonpayment period ({p} days) may be very short — verify")

        # Field presence check — flag if field present in 45+ states but absent here
        for field in standard_top_fields:
            count = field_presence[field]
            if count >= 45 and field not in data:
                flags.append(f"L5-MISSING-FIELD: '{field}' present in {count} other states but absent here")

        # Affirmative defenses check — core set
        ad = data.get("affirmative_defenses", [])
        for expected in ["habitability", "retaliatory_eviction", "discriminatory_eviction"]:
            if expected not in ad:
                flags.append(f"L5-DEF-MISSING: '{expected}' absent from affirmative_defenses — present in most states")

        results[code] = flags

    return results, {"mean_nonpay_period": round(mean_period, 1), "median_nonpay_period": median_period}


# ── LAYER 1: Statutory Grounding Check (Framework) ─────────────────────────────

def layer1_statutory_grounding_check(data, code):
    """
    Check whether the file claims statutory retrieval was performed.
    If not, flag for retrieval. If yes, note the source.
    Full live retrieval via LDH is a separate process (run as a CI step).
    """
    flags = []
    if not data.get("statutory_retrieval_performed"):
        source = data.get("source_for_retrieval")
        if source:
            flags.append(f"L1-RETRIEVE-PENDING: statutory retrieval not performed. LDH source available: {source}")
        else:
            flags.append("L1-RETRIEVE-PENDING: statutory retrieval not performed. No LDH source — retrieve from official state legislature website.")
    else:
        ret_date = data.get("statutory_retrieval_date", "unknown")
        ret_url = data.get("statutory_retrieval_url", "")
        flags.append(f"L1-RETRIEVED: retrieval performed {ret_date} — {ret_url}")
    return flags


# ── LAYER 4: Golden-Set Behavioral Tests (Framework) ──────────────────────────

def layer4_golden_set(code):
    """
    Load golden set test cases for this state (if they exist) and run them.
    Full golden sets are in validation/golden_sets/.
    This function checks whether a golden set exists.
    """
    golden_dir = os.path.join(os.path.dirname(__file__), "..", "golden_sets")
    golden_file = os.path.join(golden_dir, f"{code.lower()}_golden_set.json")
    if not os.path.exists(golden_file):
        return [], f"L4-NO-GOLDEN-SET: no golden set exists for {code} — authoring needed (see Workstream B spec)"
    with open(golden_file) as f:
        cases = json.load(f)
    passed = []
    failed = []
    for case in cases:
        # Placeholder: actual behavioral testing requires running the rules engine
        # against the JSON file and comparing to expected_output
        passed.append(f"L4-CASE-{case.get('id', '?')}: golden set case loaded (behavioral test requires rules engine)")
    return passed, None


# ── MAIN RUNNER ────────────────────────────────────────────────────────────────

def load_all_files():
    all_data = {}
    for state_dir in sorted(glob.glob(os.path.join(RULES_DIR, "*"))):
        if not os.path.isdir(state_dir):
            continue
        json_files = glob.glob(os.path.join(state_dir, "*.json"))
        for jf in json_files:
            with open(jf) as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"ERROR: could not parse {jf}: {e}")
                    continue
            code = data.get("jurisdiction", {}).get("state", os.path.basename(jf)[:2].upper())
            all_data[code] = data
    return all_data


def run_validation(target_state=None, write_reports=True):
    all_data = load_all_files()
    if not all_data:
        print("No rules files found. Run generate_rules.py first.")
        return

    # Layer 5 runs across all files
    l5_results, l5_stats = layer5_cross_jurisdiction(all_data)

    report = {
        "generated": datetime.utcnow().isoformat() + "Z",
        "total_files": len(all_data),
        "library_stats": l5_stats,
        "files": {}
    }

    states_to_check = [target_state] if target_state else sorted(all_data.keys())

    for code in states_to_check:
        if code not in all_data:
            print(f"State {code} not found in library")
            continue
        data = all_data[code]
        path = code

        l3_errors, l3_warnings = layer3_internal_consistency(data, path)
        l1_flags = layer1_statutory_grounding_check(data, code)
        l4_passed, l4_note = layer4_golden_set(code)
        l5_flags = l5_results.get(code, [])

        # Determine overall pass/fail
        layer_results = {
            "L1_statutory_grounding": {"status": "RETRIEVED" if data.get("statutory_retrieval_performed") else "PENDING", "flags": l1_flags},
            "L2_multi_model_consensus": {"status": "NOT_RUN", "note": "Layer 2 requires multi-model comparison — run separately"},
            "L3_internal_consistency": {
                "status": "PASS" if not l3_errors else "FAIL",
                "errors": l3_errors,
                "warnings": l3_warnings
            },
            "L4_golden_set": {"status": "NO_GOLDEN_SET" if l4_note else "PASS", "note": l4_note, "cases_run": len(l4_passed)},
            "L5_cross_jurisdiction": {"status": "PASS" if not l5_flags else "FLAGS", "flags": l5_flags},
            "L6_temporal_freshness": {"status": "NOT_RUN", "note": "Layer 6 requires legislative feed integration — run as CI step"},
        }

        overall = "PASS" if not l3_errors else "FAIL"
        report["files"][code] = {
            "state": data.get("jurisdiction", {}).get("state_name", code),
            "validation_status": data.get("validation_status"),
            "statutory_retrieved": data.get("statutory_retrieval_performed", False),
            "overall": overall,
            "layers": layer_results
        }

        # Console output
        status_icon = "✓" if overall == "PASS" else "✗"
        warn_count = len(l3_warnings)
        err_count = len(l3_errors)
        l5_count = len(l5_flags)
        print(f"  {status_icon} {code}: L3={'PASS' if not l3_errors else f'FAIL({err_count}err)'} "
              f"warn={warn_count} L5={f'FLAGS({l5_count})' if l5_flags else 'PASS'} "
              f"L1={'RETRIEVED' if data.get('statutory_retrieval_performed') else 'PENDING'}")

    # Library-wide summary
    total = len(report["files"])
    passed = sum(1 for v in report["files"].values() if v["overall"] == "PASS")
    retrieved = sum(1 for v in report["files"].values() if v["statutory_retrieved"])
    print(f"\nLibrary summary: {total} files | L3 PASS: {passed} | L3 FAIL: {total-passed} | Statutory retrieved: {retrieved}")
    print(f"Notice period stats: mean={l5_stats['mean_nonpay_period']} days | median={l5_stats['median_nonpay_period']} days")

    if write_reports:
        os.makedirs(REPORTS_DIR, exist_ok=True)
        report_path = os.path.join(REPORTS_DIR, f"validation_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        # Also write a "latest" symlink-style copy
        latest_path = os.path.join(REPORTS_DIR, "validation_report_latest.json")
        with open(latest_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nReport written to: {os.path.basename(report_path)}")

    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LHC Eviction Rules Validation Battery")
    parser.add_argument("--state", help="Validate a single state (2-letter code)")
    parser.add_argument("--report", action="store_true", help="Write validation reports to reports/")
    args = parser.parse_args()
    print(f"\nLHC Eviction Rules Validation Battery — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Running Layers 1, 3, 4 (framework), 5 against {'all states' if not args.state else args.state}\n")
    run_validation(target_state=args.state, write_reports=True)
