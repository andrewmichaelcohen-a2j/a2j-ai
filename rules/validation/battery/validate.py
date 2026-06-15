#!/usr/bin/env python3
"""
Eviction Rules — Automated Validation Battery (v2)
Validates all *_eviction_v2.json files against the eviction-v2 schema.

Operational layers today: L1 (statutory grounding), L3 (internal consistency),
L5 (cross-jurisdiction anomaly detection).
Not implemented (scaffold only): L2 (consensus), L4 (golden set), L6 (freshness).

Three enforced guardrails:
  G1 — No auto-advance: automated processes may never advance a module beyond
       AUTOMATED-CHECKS-PASSED. A module at UNDER REVIEW / VALIDATED / CERTIFIED
       with reviewer=null is a VALIDATION FAILURE.
  G2 — file_status = min(module_status). Never set directly. Computed here and
       written back to the file.
  G3 — Option-A gate: a module advances to AUTOMATED-CHECKS-PASSED only when ALL
       currently-implemented layers pass. Today's implemented layers: L1, L3, L5.
       Layers marked not_implemented never block advancement.

Usage:
  python validate.py                    # validate all v2 files
  python validate.py --state CA         # validate one state
  python validate.py --report           # write reports/ output

Copyright 2026 Andrew M Cohen.
Licensed under the Apache License, Version 2.0.
"""

import json
import os
import sys
import glob
import argparse
from datetime import datetime

# ── Paths ─────────────────────────────────────────────────────────────────────

RULES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "eviction")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")

# ── Constants ─────────────────────────────────────────────────────────────────

STATUS_ORDER = [
    "DRAFT",
    "AUTOMATED-CHECKS-PASSED",
    "UNDER REVIEW",
    "VALIDATED",
    "CERTIFIED",
    "NEEDS UPDATE",
]

# For file_status min computation, NEEDS UPDATE is treated as lowest
STATUS_RANK = {
    "NEEDS UPDATE": -1,
    "DRAFT": 0,
    "AUTOMATED-CHECKS-PASSED": 1,
    "UNDER REVIEW": 2,
    "VALIDATED": 3,
    "CERTIFIED": 4,
}

MODULES = ["notice", "service", "overlays", "substantive_defenses", "procedural_defects"]

VALID_STATUSES = set(STATUS_RANK.keys())

# Layers implemented today (used for Option-A gate)
IMPLEMENTED_LAYERS = {"L1_grounding", "L3_consistency", "L5_crossjuris"}

TODAY = datetime.utcnow().strftime("%Y-%m-%d")
COVERAGE_LEVEL = "L1,L3,L5"


# ── Guardrail G1: No auto-advance check ───────────────────────────────────────

def guardrail_no_auto_advance(data):
    """
    G1: Any module at UNDER REVIEW, VALIDATED, or CERTIFIED with reviewer=null
    is a hard FAIL. validate.py must never advance beyond AUTOMATED-CHECKS-PASSED.
    """
    errors = []
    ms = data.get("validation", {}).get("module_status", {})
    for mod in MODULES:
        entry = ms.get(mod, {})
        status = entry.get("status", "DRAFT")
        reviewer = entry.get("reviewer")
        if status in {"UNDER REVIEW", "VALIDATED", "CERTIFIED"} and not reviewer:
            errors.append(
                f"G1-NO-REVIEWER: module '{mod}' is at '{status}' but reviewer=null. "
                "Only a named attorney may advance past AUTOMATED-CHECKS-PASSED."
            )
    return errors


# ── Guardrail G2: file_status = min(module_status) ────────────────────────────

def compute_min_status(data):
    """
    G2: Compute the correct file_status as min(module_status).
    Returns the correct status string.
    NEEDS UPDATE propagates regardless of min (negative rank).
    """
    ms = data.get("validation", {}).get("module_status", {})
    statuses = [ms.get(mod, {}).get("status", "DRAFT") for mod in MODULES]
    # If any module is NEEDS UPDATE, file is NEEDS UPDATE
    if "NEEDS UPDATE" in statuses:
        return "NEEDS UPDATE"
    min_rank = min(STATUS_RANK.get(s, 0) for s in statuses)
    for s, r in STATUS_RANK.items():
        if r == min_rank:
            return s
    return "DRAFT"


def guardrail_file_status(data):
    """
    G2: Check that file_status matches min(module_status). Return errors and correct value.
    """
    errors = []
    current = data.get("validation", {}).get("file_status", "DRAFT")
    correct = compute_min_status(data)
    if current != correct:
        errors.append(
            f"G2-STATUS-MISMATCH: file_status='{current}' but min(module_status)='{correct}'. "
            "file_status will be corrected."
        )
    return errors, correct


# ── Layer 1: Statutory Grounding ──────────────────────────────────────────────

def layer1(data):
    """
    L1: Check whether statutory_retrieval_performed=true in validation.automated_layers.
    For v2, L1 is about whether real statutes were retrieved and are embedded.
    """
    result = data.get("validation", {}).get("automated_layers", {}).get("L1_grounding", "not_run")
    flags = []
    if result == "pass":
        flags.append("L1-RETRIEVED: statutory retrieval flagged as complete")
    elif result == "fail":
        flags.append("L1-FAIL: statutory retrieval flagged as failed")
    else:
        # Check provenance for actual retrieval evidence
        sources = data.get("provenance", {}).get("statutory_sources", [])
        retrieved_count = sum(1 for s in sources if s.get("retrieved"))
        if retrieved_count > 0:
            flags.append(f"L1-RETRIEVED: {retrieved_count} sources marked retrieved in provenance")
            result = "pass"
        else:
            flags.append("L1-PENDING: no statutory retrieval recorded — mark retrieved after live pull")
            result = "not_run"
    return result, flags


# ── Layer 3: Internal Consistency ─────────────────────────────────────────────

def layer3_notice(notice, state):
    """L3 checks for the notice module."""
    errors, warnings = [], []
    if not isinstance(notice, dict):
        errors.append("3-NOTICE-01: notice module must be an object")
        return errors, warnings

    nt = notice.get("notice_types", {})
    if not isinstance(nt, dict):
        errors.append("3-NOTICE-02: notice.notice_types must be an object")
    else:
        # pay_or_quit presence
        if "pay_or_quit" not in nt:
            warnings.append("3-NOTICE-03: notice.notice_types.pay_or_quit missing — expected for residential evictions")
        else:
            pq = nt["pay_or_quit"]
            # Notice period
            days = None
            for subkey in ["tenancy_all", "tenancy_under_1yr", "tenancy_any"]:
                if subkey in pq and isinstance(pq[subkey], dict):
                    days = pq[subkey].get("days")
                    break
            if days is None:
                warnings.append("3-NOTICE-04: cannot determine pay_or_quit notice period — check notice_types.pay_or_quit structure")
            elif not isinstance(days, int) or days < 1:
                errors.append(f"3-NOTICE-04: pay_or_quit notice period must be positive integer, got {days!r}")
            elif days > 60:
                warnings.append(f"3-NOTICE-04: pay_or_quit period of {days} days is unusually long — verify")
            # late_fees_permitted boolean
            lfp = pq.get("late_fees_permitted")
            if lfp is not None and not isinstance(lfp, bool):
                errors.append("3-NOTICE-05: notice.notice_types.pay_or_quit.late_fees_permitted must be boolean")
            # permitted_amounts
            pa = pq.get("permitted_amounts", [])
            if not isinstance(pa, list) or len(pa) == 0:
                warnings.append("3-NOTICE-06: notice.notice_types.pay_or_quit.permitted_amounts is empty or missing")

        # cure_or_quit days check vs pay_or_quit
        coq = nt.get("cure_or_quit", {})
        pq = nt.get("pay_or_quit", {})
        if isinstance(coq, dict) and isinstance(pq, dict):
            cure_days = coq.get("days")
            nonpay_days = None
            for sk in ["tenancy_all", "tenancy_under_1yr", "tenancy_any"]:
                if sk in pq and isinstance(pq[sk], dict):
                    nonpay_days = pq[sk].get("days")
                    break
            if cure_days and nonpay_days and cure_days < nonpay_days:
                warnings.append(
                    f"3-NOTICE-07: cure_or_quit.days ({cure_days}) < pay_or_quit days ({nonpay_days}) — unusual, verify"
                )

        # termination presence
        if "termination" not in nt:
            warnings.append("3-NOTICE-08: notice.notice_types.termination missing — expected for no-fault scenarios")

    # notice_defects
    nd = notice.get("notice_defects", [])
    if not isinstance(nd, list):
        errors.append("3-NOTICE-09: notice.notice_defects must be an array")
    else:
        valid_consequence = {"notice_void", "defective_curable", "warning"}
        valid_severity = {"void", "defective_curable", "warning"}
        for i, d in enumerate(nd):
            if not isinstance(d, dict):
                errors.append(f"3-NOTICE-10: notice_defects[{i}] must be an object")
                continue
            if "defect" not in d:
                errors.append(f"3-NOTICE-10: notice_defects[{i}] missing 'defect'")
            cons = d.get("consequence")
            if cons not in valid_consequence:
                errors.append(f"3-NOTICE-11: notice_defects[{i}].consequence '{cons}' not in {valid_consequence}")
            sev = d.get("severity")
            if sev not in valid_severity:
                errors.append(f"3-NOTICE-11: notice_defects[{i}].severity '{sev}' not in {valid_severity}")
        # improper_service_method expected
        defect_ids = [d.get("defect", "") for d in nd if isinstance(d, dict)]
        if "improper_service_method" not in defect_ids:
            warnings.append("3-NOTICE-12: 'improper_service_method' not in notice_defects — expected in all states")

    return errors, warnings


def layer3_service(service, state):
    """L3 checks for the service module."""
    errors, warnings = [], []
    if not isinstance(service, dict):
        errors.append("3-SVC-01: service module must be an object")
        return errors, warnings

    permitted = service.get("permitted_methods", [])
    if not isinstance(permitted, list) or len(permitted) == 0:
        errors.append("3-SVC-02: service.permitted_methods must be non-empty list")

    method_rules = service.get("method_rules", [])
    if not isinstance(method_rules, list):
        errors.append("3-SVC-03: service.method_rules must be an array")
    else:
        for i, rule in enumerate(method_rules):
            if not isinstance(rule, dict):
                errors.append(f"3-SVC-04: service.method_rules[{i}] must be an object")
                continue
            for req in ["method", "requirements", "statute"]:
                if not rule.get(req):
                    errors.append(f"3-SVC-04: service.method_rules[{i}].{req} is required")

    svc_defects = service.get("service_defects", [])
    if not isinstance(svc_defects, list):
        errors.append("3-SVC-05: service.service_defects must be an array")

    return errors, warnings


def layer3_overlays(overlays, state):
    """L3 checks for the overlays module."""
    errors, warnings = [], []
    if not isinstance(overlays, dict):
        errors.append("3-OVL-01: overlays module must be an object")
        return errors, warnings

    federal = overlays.get("federal", [])
    if not isinstance(federal, list):
        errors.append("3-OVL-02: overlays.federal must be an array")
    else:
        valid_status = {"active", "expired", "conditional"}
        for i, f in enumerate(federal):
            if not isinstance(f, dict):
                errors.append(f"3-OVL-03: overlays.federal[{i}] must be an object")
                continue
            for req in ["name", "applies_when", "effect", "statute"]:
                if not f.get(req):
                    errors.append(f"3-OVL-03: overlays.federal[{i}].{req} is required")
            if f.get("status") and f["status"] not in valid_status:
                errors.append(f"3-OVL-04: overlays.federal[{i}].status '{f['status']}' not in {valid_status}")

    state_prot = overlays.get("state_protective", [])
    if not isinstance(state_prot, list):
        errors.append("3-OVL-05: overlays.state_protective must be an array")

    local = overlays.get("local", [])
    if not isinstance(local, list):
        errors.append("3-OVL-06: overlays.local must be an array")
    else:
        valid_type = {"rent_control", "just_cause", "relocation", "moratorium", "other"}
        for i, loc in enumerate(local):
            if not isinstance(loc, dict):
                errors.append(f"3-OVL-07: overlays.local[{i}] must be an object")
                continue
            if not loc.get("jurisdiction"):
                errors.append(f"3-OVL-07: overlays.local[{i}].jurisdiction is required")
            if loc.get("type") and loc["type"] not in valid_type:
                errors.append(f"3-OVL-08: overlays.local[{i}].type '{loc['type']}' not in {valid_type}")

    return errors, warnings


def layer3_substantive_defenses(sub_def, state):
    """L3 checks for substantive_defenses module."""
    errors, warnings = [], []
    if not isinstance(sub_def, list):
        errors.append("3-SUB-01: substantive_defenses must be an array")
        return errors, warnings

    if len(sub_def) == 0:
        errors.append("3-SUB-02: substantive_defenses is empty — expected at minimum habitability and retaliation defenses")
        return errors, warnings

    valid_openness = {"bright_line", "fact_dependent", "open_textured"}
    valid_weight = {"automated_ok", "human_required", "specialist_required"}
    valid_defense = {"retaliation", "habitability_warranty", "discrimination",
                     "breach_of_quiet_enjoyment", "improper_rent_calculation", "other"}

    defense_types = []
    for i, d in enumerate(sub_def):
        if not isinstance(d, dict):
            errors.append(f"3-SUB-03: substantive_defenses[{i}] must be an object")
            continue
        defense_types.append(d.get("defense"))
        if "defense" not in d:
            errors.append(f"3-SUB-03: substantive_defenses[{i}] missing 'defense'")
        elif d["defense"] not in valid_defense:
            errors.append(f"3-SUB-03: substantive_defenses[{i}].defense '{d['defense']}' not in {valid_defense}")
        if "elements" not in d or not isinstance(d.get("elements"), list) or len(d.get("elements", [])) == 0:
            warnings.append(f"3-SUB-04: substantive_defenses[{i}] missing or empty 'elements'")
        if d.get("openness") not in valid_openness:
            errors.append(f"3-SUB-05: substantive_defenses[{i}].openness '{d.get('openness')}' not in {valid_openness}")
        if d.get("review_weight") not in valid_weight:
            errors.append(f"3-SUB-05: substantive_defenses[{i}].review_weight '{d.get('review_weight')}' not in {valid_weight}")

    # Core defenses expected
    for expected in ["habitability_warranty", "retaliation"]:
        if expected not in defense_types:
            warnings.append(f"3-SUB-06: '{expected}' not in substantive_defenses — expected in all jurisdictions")

    return errors, warnings


def layer3_procedural_defects(proc_def, state):
    """L3 checks for procedural_defects module."""
    errors, warnings = [], []
    if not isinstance(proc_def, list):
        errors.append("3-PROC-01: procedural_defects must be an array")
        return errors, warnings

    if len(proc_def) == 0:
        warnings.append("3-PROC-02: procedural_defects is empty — at minimum expect complaint defects and summons defects")

    for i, d in enumerate(proc_def):
        if not isinstance(d, dict):
            errors.append(f"3-PROC-03: procedural_defects[{i}] must be an object")
            continue
        if not d.get("defect"):
            errors.append(f"3-PROC-03: procedural_defects[{i}] missing 'defect'")
        if not d.get("consequence"):
            errors.append(f"3-PROC-04: procedural_defects[{i}] missing 'consequence'")

    return errors, warnings


def layer3_top_level(data, state):
    """L3 checks on top-level v2 file structure."""
    errors, warnings = [], []

    if data.get("schema_version") != "eviction-v2":
        errors.append("3-TOP-01: schema_version must be 'eviction-v2'")

    if not data.get("_copyright"):
        warnings.append("3-TOP-02: _copyright field missing")

    j = data.get("jurisdiction", {})
    if not isinstance(j, dict):
        errors.append("3-TOP-03: jurisdiction must be an object")
    else:
        for sf in ["state", "state_name", "type"]:
            if not j.get(sf):
                errors.append(f"3-TOP-03: jurisdiction.{sf} missing")
        if j.get("state") and len(j["state"]) != 2:
            errors.append("3-TOP-03: jurisdiction.state must be 2-letter code")

    prov = data.get("provenance", {})
    if not isinstance(prov, dict):
        errors.append("3-TOP-04: provenance must be an object")
    else:
        gen = prov.get("generated", {})
        for gf in ["date", "model", "method"]:
            if not gen.get(gf):
                warnings.append(f"3-TOP-04: provenance.generated.{gf} missing")
        sources = prov.get("statutory_sources", [])
        if not isinstance(sources, list) or len(sources) == 0:
            errors.append("3-TOP-05: provenance.statutory_sources must be non-empty list")

    return errors, warnings


def layer3_all(data, state):
    """Run all L3 module checks. Returns per-module results."""
    results = {}

    top_errors, top_warnings = layer3_top_level(data, state)

    for mod, fn in [
        ("notice", layer3_notice),
        ("service", layer3_service),
        ("overlays", layer3_overlays),
        ("substantive_defenses", layer3_substantive_defenses),
        ("procedural_defects", layer3_procedural_defects),
    ]:
        mod_data = data.get(mod)
        errors, warnings = fn(mod_data, state)
        # Top-level errors apply to all modules
        all_errors = top_errors + errors
        results[mod] = {
            "errors": all_errors,
            "warnings": warnings,
            "pass": len(all_errors) == 0,
        }

    return results


# ── Layer 5: Cross-Jurisdiction Anomaly Detection (per-module) ────────────────

def layer5_cross_jurisdiction(all_files_data):
    """
    Compare each file to the full library.
    Returns per-state, per-module flags.
    """
    # Collect pay_or_quit periods across all files
    periods = {}
    for code, data in all_files_data.items():
        pq = data.get("notice", {}).get("notice_types", {}).get("pay_or_quit", {})
        days = None
        for sk in ["tenancy_all", "tenancy_under_1yr", "tenancy_any"]:
            if sk in pq and isinstance(pq[sk], dict):
                days = pq[sk].get("days")
                break
        periods[code] = days

    valid_periods = [d for d in periods.values() if isinstance(d, int)]
    median_period = sorted(valid_periods)[len(valid_periods) // 2] if valid_periods else 0
    mean_period = round(sum(valid_periods) / len(valid_periods), 1) if valid_periods else 0

    # Count how many states have each defense type in substantive_defenses
    defense_presence = {}
    for data in all_files_data.values():
        defenses = data.get("substantive_defenses", [])
        if isinstance(defenses, list):
            for d in defenses:
                dtype = d.get("defense", "")
                defense_presence[dtype] = defense_presence.get(dtype, 0) + 1

    results = {}
    for code, data in all_files_data.items():
        per_module_flags = {m: [] for m in MODULES}

        # Notice: period outlier
        p = periods.get(code)
        if isinstance(p, int):
            if p > 2 * median_period and median_period > 0:
                per_module_flags["notice"].append(
                    f"L5-NOTICE-PERIOD-HIGH: pay_or_quit period ({p} days) is >2x median ({median_period}) — verify"
                )
            elif p < 3 and median_period > 5:
                per_module_flags["notice"].append(
                    f"L5-NOTICE-PERIOD-LOW: pay_or_quit period ({p} days) may be very short — verify"
                )

        # Notice: termination missing
        nt = data.get("notice", {}).get("notice_types", {})
        if isinstance(nt, dict) and "termination" not in nt:
            per_module_flags["notice"].append(
                "L5-NOTICE-NO-TERMINATION: termination not in notice_types — present in most states"
            )

        # Substantive defenses: core defenses present in 45+ states but missing here
        state_defenses = [d.get("defense", "") for d in data.get("substantive_defenses", [])
                          if isinstance(d, dict)]
        for dtype, count in defense_presence.items():
            if count >= 45 and dtype not in state_defenses:
                per_module_flags["substantive_defenses"].append(
                    f"L5-DEFENSE-MISSING: '{dtype}' present in {count} states but absent here"
                )

        # Overlays: no federal overlays
        federal = data.get("overlays", {}).get("federal", [])
        if isinstance(federal, list) and len(federal) == 0:
            per_module_flags["overlays"].append(
                "L5-OVERLAY-NO-FEDERAL: no federal overlays — CARES Act stub expected in all states"
            )

        results[code] = per_module_flags

    return results, {"mean_nonpay_period": mean_period, "median_nonpay_period": median_period}


# ── Guardrail G3: Option-A gate ───────────────────────────────────────────────

def guardrail_option_a_gate(data, l1_result, l3_module_results, l5_module_flags, module):
    """
    G3: A module may advance to AUTOMATED-CHECKS-PASSED only when all currently
    implemented layers pass. Today's implemented layers: L1, L3, L5.

    Returns True if the module passes the Option-A gate.
    """
    # L1: must be 'pass'
    if l1_result != "pass":
        return False

    # L3: module must have no errors
    if not l3_module_results.get(module, {}).get("pass", False):
        return False

    # L5: module must have no flags
    if l5_module_flags.get(module, []):
        return False

    return True


# ── Write-back: update file with computed statuses ────────────────────────────

def write_back_results(file_path, data, l1_result, l3_module_results, l5_module_flags):
    """
    After validation, update the v2 file:
    - Update validation.automated_layers.L1/L3/L5 results
    - For each module: if Option-A gate passes and module is DRAFT, advance to AUTOMATED-CHECKS-PASSED
    - Recompute file_status = min(module_status)
    - Write back
    """
    val = data.get("validation", {})
    al = val.get("automated_layers", {})
    ms = val.get("module_status", {})

    # Update layer results
    al["L1_grounding"] = l1_result

    # Determine overall L3 pass (all modules must pass)
    all_l3_pass = all(r.get("pass", False) for r in l3_module_results.values())
    al["L3_consistency"] = "pass" if all_l3_pass else "fail"

    # L5: fail if any module has flags
    any_l5_flags = any(flags for flags in l5_module_flags.values())
    al["L5_crossjuris"] = "warning" if any_l5_flags else "pass"

    # Per-module: advance DRAFT → AUTOMATED-CHECKS-PASSED if Option-A gate passes
    for mod in MODULES:
        entry = ms.get(mod, {})
        current_status = entry.get("status", "DRAFT")

        # G1: never auto-advance past AUTOMATED-CHECKS-PASSED
        if current_status in {"UNDER REVIEW", "VALIDATED", "CERTIFIED"}:
            continue  # Don't touch; G1 errors already reported

        if current_status == "DRAFT":
            gates_pass = guardrail_option_a_gate(
                data, l1_result, l3_module_results, l5_module_flags, mod
            )
            if gates_pass:
                entry["status"] = "AUTOMATED-CHECKS-PASSED"
                entry["coverage_level"] = COVERAGE_LEVEL
            # else stays DRAFT

        ms[mod] = entry

    # G2: recompute file_status
    # Temporarily update module_status in data for computation
    val["module_status"] = ms
    val["automated_layers"] = al
    data["validation"] = val
    correct_file_status = compute_min_status(data)
    val["file_status"] = correct_file_status

    # Build flags list for validation.flags
    all_flags = []
    for mod in MODULES:
        for flag in l5_module_flags.get(mod, []):
            all_flags.append({
                "layer": "L5",
                "field": mod,
                "note": flag,
                "disposition": "open"
            })
        l3 = l3_module_results.get(mod, {})
        for w in l3.get("warnings", []):
            all_flags.append({
                "layer": "L3",
                "field": mod,
                "note": w,
                "disposition": "open"
            })

    # Preserve existing acknowledged/resolved flags
    existing_flags = val.get("flags", [])
    preserved = [f for f in existing_flags if f.get("disposition") in {"acknowledged", "resolved"}]
    val["flags"] = preserved + all_flags

    val["coverage_level"] = COVERAGE_LEVEL
    val["validation_note"] = (
        f"Automated validation run {TODAY}. "
        f"Layers run: {COVERAGE_LEVEL}. "
        f"file_status={correct_file_status}."
    )

    data["validation"] = val

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    return data


# ── File loading ──────────────────────────────────────────────────────────────

def load_all_v2_files():
    """Load all *_eviction_v2.json files from rules/eviction/*/."""
    all_data = {}
    all_paths = {}
    for state_dir in sorted(glob.glob(os.path.join(RULES_DIR, "*"))):
        if not os.path.isdir(state_dir):
            continue
        v2_files = glob.glob(os.path.join(state_dir, "*_eviction_v2.json"))
        for jf in v2_files:
            try:
                with open(jf) as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"  ERROR: could not parse {jf}: {e}")
                continue
            code = data.get("jurisdiction", {}).get("state", os.path.basename(jf)[:2].upper())
            all_data[code] = data
            all_paths[code] = jf
    return all_data, all_paths


# ── Main runner ───────────────────────────────────────────────────────────────

def run_validation(target_state=None, write_reports=True, write_back=True):
    all_data, all_paths = load_all_v2_files()
    if not all_data:
        print("No v2 rules files found. Run generate_v2.py first.")
        return

    # L5 runs across all files (needs full library)
    l5_results, l5_stats = layer5_cross_jurisdiction(all_data)

    report = {
        "generated": datetime.utcnow().isoformat() + "Z",
        "schema_version": "eviction-v2",
        "total_files": len(all_data),
        "library_stats": l5_stats,
        "coverage": COVERAGE_LEVEL,
        "files": {}
    }

    states_to_check = [target_state] if target_state else sorted(all_data.keys())

    for code in states_to_check:
        if code not in all_data:
            print(f"  State {code} not found in library")
            continue

        data = all_data[code]
        path = all_paths[code]

        # G1 check
        g1_errors = guardrail_no_auto_advance(data)

        # L1
        l1_result, l1_flags = layer1(data)

        # L3 (all modules)
        l3_module_results = layer3_all(data, code)

        # L5 (per-module flags for this state)
        l5_module_flags = l5_results.get(code, {m: [] for m in MODULES})

        # G2 check (before write-back)
        g2_errors, correct_status = guardrail_file_status(data)

        # Collect all errors
        all_errors = g1_errors + g2_errors
        for mod_res in l3_module_results.values():
            all_errors.extend(mod_res.get("errors", []))

        all_warnings = []
        for mod_res in l3_module_results.values():
            all_warnings.extend(mod_res.get("warnings", []))
        for mod_flags in l5_module_flags.values():
            all_warnings.extend(mod_flags)

        # Write-back: update file with computed results
        if write_back and not g1_errors:
            data = write_back_results(path, data, l1_result, l3_module_results, l5_module_flags)
            all_data[code] = data  # update in-memory copy

        overall = "FAIL" if all_errors else "PASS"

        # Per-module summary for report
        module_report = {}
        for mod in MODULES:
            l3m = l3_module_results.get(mod, {})
            module_report[mod] = {
                "l3_pass": l3m.get("pass", False),
                "l3_errors": l3m.get("errors", []),
                "l3_warnings": l3m.get("warnings", []),
                "l5_flags": l5_module_flags.get(mod, []),
                "status_after": data.get("validation", {}).get("module_status", {}).get(mod, {}).get("status", "DRAFT"),
            }

        report["files"][code] = {
            "state": data.get("jurisdiction", {}).get("state_name", code),
            "file_status": data.get("validation", {}).get("file_status", "DRAFT"),
            "overall": overall,
            "guardrail_errors": g1_errors + g2_errors,
            "l1": l1_result,
            "l3_total_errors": sum(len(v.get("errors", [])) for v in l3_module_results.values()),
            "l3_total_warnings": sum(len(v.get("warnings", [])) for v in l3_module_results.values()),
            "l5_total_flags": sum(len(v) for v in l5_module_flags.values()),
            "modules": module_report,
        }

        # Console output
        icon = "✓" if overall == "PASS" else "✗"
        l3_err = sum(len(v.get("errors", [])) for v in l3_module_results.values())
        l3_warn = sum(len(v.get("warnings", [])) for v in l3_module_results.values())
        l5_count = sum(len(v) for v in l5_module_flags.values())
        file_status = data.get("validation", {}).get("file_status", "DRAFT")

        print(
            f"  {icon} {code}: L1={l1_result} L3={'PASS' if l3_err==0 else f'FAIL({l3_err})'} "
            f"warn={l3_warn} L5={f'FLAGS({l5_count})' if l5_count else 'PASS'} "
            f"→ file_status={file_status}"
            + (f" | G1-ERRORS: {len(g1_errors)}" if g1_errors else "")
        )

    # Summary
    total = len(report["files"])
    passed = sum(1 for v in report["files"].values() if v["overall"] == "PASS")
    retrieved = sum(1 for v in report["files"].values() if v["l1"] == "pass")
    auto_passed = sum(
        1 for v in report["files"].values()
        if v["file_status"] == "AUTOMATED-CHECKS-PASSED"
    )

    print(f"\nLibrary summary ({COVERAGE_LEVEL}):")
    print(f"  {total} files | L3 PASS: {passed} | L3 FAIL: {total-passed}")
    print(f"  L1 retrieved: {retrieved} | file_status=AUTOMATED-CHECKS-PASSED: {auto_passed}")
    print(f"  Notice period: mean={l5_stats['mean_nonpay_period']}d median={l5_stats['median_nonpay_period']}d")

    if write_reports:
        os.makedirs(REPORTS_DIR, exist_ok=True)
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(REPORTS_DIR, f"validation_report_v2_{ts}.json")
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        latest_path = os.path.join(REPORTS_DIR, "validation_report_v2_latest.json")
        with open(latest_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n  Report → {os.path.basename(report_path)}")

    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Eviction Rules Validation Battery v2")
    parser.add_argument("--state", help="Validate a single state (2-letter code, e.g. CA)")
    parser.add_argument("--no-writeback", action="store_true", help="Don't update files with computed results")
    parser.add_argument("--report", action="store_true", help="Write validation reports to reports/")
    args = parser.parse_args()

    print(f"\nCivil Justice as Code — Validation Battery v2 — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Layers: {COVERAGE_LEVEL} (L2/L4/L6: not_implemented)")
    print(f"Scope: {'all states' if not args.state else args.state}\n")

    run_validation(
        target_state=args.state,
        write_reports=True,
        write_back=not args.no_writeback,
    )
