#!/usr/bin/env python3
"""
LSC Baseline Cross-Check Runner
================================
Compares CJaC eviction-v2 notice/pay_or_quit values against the LSC/Temple
LawAtlas State Eviction Laws Dataset (Jan 2021).

Prerequisites:
  1. Download the LSC dataset Excel from:
     https://lawatlas.org/datasets/state-eviction-laws
     (free account required)
  2. pip install openpyxl --break-system-packages

Usage:
  python3 rules/validation/l2/lsc_crosscheck_runner.py --lsc-file /path/to/data.xlsx
  python3 rules/validation/l2/lsc_crosscheck_runner.py --lsc-file /path/to/data.xlsx --dry-run

Output:
  docs/LSC_CROSSCHECK_REPORT_<date>.md

Security: No API keys required. No network calls. Pure file comparison.

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

_L2_DIR = Path(__file__).resolve().parent
_RULES_DIR = _L2_DIR.parent.parent
_DOCS_DIR = _RULES_DIR.parent / "docs"
_EVICTION_DIR = _RULES_DIR / "eviction"

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# State code → full name mapping (for matching against LSC "State" column)
STATE_NAMES = {
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

# Known post-2021 statutory changes that explain expected divergences
# Add to this as they're identified
KNOWN_POST_2021_CHANGES = {
    "MN": "14-day pay-or-quit notice enacted in 2023 Housing Omnibus (HF 3019) — post-2021",
    "VA": "14-day period effective 2026-07-01 per HB 15/SB 48 — post-2021 (current: 5d)",
    "SD": "§21-16-2 repealed by SB 90 (2024); NJ-style no-notice pattern — post-2021",
    "OR": "Various RLTA amendments 2019-2023 may affect notice periods",
    "WA": "RCW 59.18.057 14-day pay-or-vacate enacted 2019 — may be in or out of 2021 snapshot",
}


def load_cjac_files():
    """Load all 51 CJaC v2 files and extract notice/pay_or_quit data."""
    cjac_data = {}
    for state_dir in sorted(_EVICTION_DIR.iterdir()):
        if not state_dir.is_dir():
            continue
        for f in state_dir.glob("*_v2.json"):
            try:
                with open(f) as fh:
                    data = json.load(fh)
                code = data.get("jurisdiction", {}).get("state_code") or \
                       data.get("jurisdiction", {}).get("state_abbreviation")
                if not code:
                    continue
                pay_or_quit = (data.get("notice", {})
                               .get("nonpayment", {})
                               .get("pay_or_quit", {}))
                if not pay_or_quit:
                    pay_or_quit = (data.get("notice", {})
                                   .get("pay_or_quit", {}))
                if not pay_or_quit:
                    continue
                cjac_data[code] = {
                    "notice_required": pay_or_quit.get("notice_required"),
                    "days": pay_or_quit.get("days"),
                    "count_method": pay_or_quit.get("count_method"),
                    "statute": pay_or_quit.get("statute"),
                    "validation_flags": [
                        f for f in data.get("validation", {}).get("flags", [])
                        if f.get("disposition") == "open"
                    ],
                    "file": str(f),
                }
            except Exception as e:
                print(f"  WARN: {f}: {e}")
    return cjac_data


def load_lsc_excel(path: str):
    """
    Load LSC dataset Excel. Returns dict: state_name → {notice_required, days, ...}

    Column names vary by dataset version — this function tries common patterns.
    Inspect the Codebook for exact column names and update NOTICE_COL / DAYS_COL
    below if the script can't find the right columns.
    """
    if not HAS_OPENPYXL:
        print("ERROR: openpyxl not installed.")
        print("Run: pip install openpyxl --break-system-packages")
        sys.exit(1)

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    header = [str(c).strip() if c else "" for c in rows[0]]
    print(f"  Columns found: {header[:20]}")

    # Common column name patterns — update from Codebook if needed
    JURISDICTION_COL_CANDIDATES = ["Jurisdiction", "State", "State/Territory", "jurisdiction"]
    NOTICE_REQUIRED_COL_CANDIDATES = [
        "NonpaymentNoticeRequired", "Nonpayment Notice Required",
        "Notice Required (Nonpayment)", "notice_required"
    ]
    DAYS_COL_CANDIDATES = [
        "NonpaymentNoticeDays", "Nonpayment Notice Days",
        "Notice Period (Days)", "days", "MinDays"
    ]

    def find_col(candidates):
        for c in candidates:
            if c in header:
                return header.index(c)
        # Case-insensitive fallback
        for c in candidates:
            for i, h in enumerate(header):
                if h.lower() == c.lower():
                    return i
        return None

    juris_idx = find_col(JURISDICTION_COL_CANDIDATES)
    notice_idx = find_col(NOTICE_REQUIRED_COL_CANDIDATES)
    days_idx = find_col(DAYS_COL_CANDIDATES)

    if juris_idx is None:
        print(f"ERROR: Can't find jurisdiction column. Headers: {header}")
        print("Update JURISDICTION_COL_CANDIDATES in this script to match the Codebook.")
        sys.exit(1)
    if notice_idx is None:
        print(f"WARN: Can't find nonpayment-notice-required column. Headers: {header}")
    if days_idx is None:
        print(f"WARN: Can't find notice days column. Headers: {header}")

    lsc_data = {}
    for row in rows[1:]:
        if not row[juris_idx]:
            continue
        juris = str(row[juris_idx]).strip()
        lsc_data[juris] = {
            "notice_required_raw": row[notice_idx] if notice_idx else None,
            "days_raw": row[days_idx] if days_idx else None,
        }

    print(f"  LSC dataset: {len(lsc_data)} jurisdictions loaded")
    return lsc_data, header


def classify(code, cjac, lsc_name, lsc):
    """Classify the CJaC vs LSC comparison for one state."""
    c_required = cjac.get("notice_required")
    c_days = cjac.get("days")
    l_raw_req = str(lsc.get("notice_required_raw") or "").strip().lower()
    l_raw_days = lsc.get("days_raw")

    # Parse LSC notice required
    l_required = None
    if l_raw_req in ("yes", "true", "1"):
        l_required = True
    elif l_raw_req in ("no", "false", "0", "not specified", "none", ""):
        l_required = False

    # Parse LSC days (may be int, float, "N/A", None)
    l_days = None
    try:
        l_days = int(float(l_raw_days)) if l_raw_days not in (None, "", "N/A") else None
    except (ValueError, TypeError):
        l_days = None

    # Open L7?
    open_l7 = any("L7" in f.get("code", "") for f in cjac.get("validation_flags", []))

    # Known post-2021 change?
    post_2021 = code in KNOWN_POST_2021_CHANGES

    # Classification
    if l_required is None:
        return "LSC-PARSE-ERROR", None, None

    if c_required is False and l_required is False:
        return "MATCH-NO-NOTICE", None, None

    if c_required is True and l_required is True:
        if c_days == l_days:
            return "MATCH-PERIOD", c_days, l_days
        elif post_2021:
            return "DIVERGENCE-POST2021-CHANGE", c_days, l_days
        else:
            return "DIVERGENCE-PERIOD", c_days, l_days

    if c_required is False and l_required is True:
        if post_2021:
            return "DIVERGENCE-POST2021-CHANGE", c_days, l_days
        return "DIVERGENCE-CJAC-NO-NOTICE-LSC-REQUIRES", c_days, l_days

    if c_required is True and l_required is False:
        if post_2021:
            return "DIVERGENCE-POST2021-CHANGE", c_days, l_days
        if open_l7:
            return "OPEN-L7-LSC-SUPPORTS-NO-NOTICE", c_days, l_days
        return "DIVERGENCE-CJAC-REQUIRES-LSC-NO-MINIMUM", c_days, l_days

    if c_required is None:
        return "CJAC-UNKNOWN", c_days, l_days

    return "UNCLASSIFIED", c_days, l_days


def run_crosscheck(lsc_path: str, dry_run: bool = False):
    print(f"\nCivil Justice as Code — LSC Baseline Cross-Check")
    print(f"Run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"LSC file: {lsc_path}")
    print()

    cjac = load_cjac_files()
    print(f"CJaC: {len(cjac)} states loaded")

    lsc, headers = load_lsc_excel(lsc_path)

    # Build name → code reverse lookup
    name_to_code = {v: k for k, v in STATE_NAMES.items()}
    # Also try aliases
    name_to_code["District of Columbia"] = "DC"
    name_to_code["D.C."] = "DC"

    results = []
    unmatched_lsc = []

    for lsc_name, lsc_row in lsc.items():
        code = name_to_code.get(lsc_name)
        if not code:
            unmatched_lsc.append(lsc_name)
            continue
        if code not in cjac:
            results.append((code, lsc_name, "NOT-IN-CJAC", None, None, lsc_row))
            continue
        classification, c_days, l_days = classify(code, cjac[code], lsc_name, lsc_row)
        results.append((code, lsc_name, classification, c_days, l_days, lsc_row))

    # Count by category
    from collections import Counter
    counts = Counter(r[2] for r in results)

    # Build report
    lines = [
        f"# LSC Baseline Cross-Check Report",
        f"",
        f"**Civil Justice as Code · {TODAY} · LSC dataset: Jan 1, 2021 · CJaC: current**",
        f"",
        f"## Summary",
        f"",
        f"| Category | Count |",
        f"|----------|-------|",
    ]
    for cat, n in sorted(counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {cat} | {n} |")

    lines += [
        f"",
        f"**Total states compared:** {len(results)}",
        f"**Unmatched LSC jurisdictions (territories, etc.):** {len(unmatched_lsc)} — {', '.join(unmatched_lsc[:10])}",
        f"",
        f"---",
        f"",
        f"## Results by State",
        f"",
        f"| Code | State | Classification | CJaC days | LSC days | Note |",
        f"|------|-------|----------------|-----------|----------|------|",
    ]

    for code, name, cls, c_days, l_days, lsc_row in sorted(results, key=lambda x: x[0]):
        note = ""
        if code in KNOWN_POST_2021_CHANGES and "POST2021" in cls:
            note = KNOWN_POST_2021_CHANGES[code]
        open_l7 = any("L7" in f.get("code", "") for f in cjac.get(code, {}).get("validation_flags", []))
        if open_l7:
            note = (note + " [OPEN L7]").strip()
        lines.append(f"| {code} | {name} | {cls} | {c_days} | {l_days} | {note} |")

    lines += [
        f"",
        f"---",
        f"",
        f"## Actionable items",
        f"",
        f"### 🔴 Priority: Pre-2021 divergences (CJaC may have error)",
        f"",
    ]

    priority = [r for r in results if r[2] in (
        "DIVERGENCE-PERIOD",
        "DIVERGENCE-CJAC-NO-NOTICE-LSC-REQUIRES",
        "DIVERGENCE-CJAC-REQUIRES-LSC-NO-MINIMUM",
    )]
    if priority:
        for code, name, cls, c_days, l_days, _ in priority:
            lines.append(f"- **{code} ({name}):** CJaC={c_days}d / LSC={l_days}d ({cls}) — investigate")
    else:
        lines.append("- None found 🎉")

    lines += [
        f"",
        f"### ✅ Corroborations (MATCH)",
        f"",
    ]
    matches = [r for r in results if r[2].startswith("MATCH")]
    lines.append(f"- {len(matches)} states matched independently — use as corroboration evidence")
    for code, name, cls, c_days, l_days, _ in sorted(matches, key=lambda x: x[0]):
        lines.append(f"  - {code} ({name}): {cls}, days={c_days}")

    lines += [
        f"",
        f"### ⚠️ Post-2021 changes (CJaC is more current)",
        f"",
    ]
    post = [r for r in results if "POST2021" in r[2]]
    for code, name, cls, c_days, l_days, _ in post:
        note = KNOWN_POST_2021_CHANGES.get(code, "")
        lines.append(f"- **{code}:** {note} (CJaC={c_days}d, LSC={l_days}d)")
    if not post:
        lines.append("- None auto-identified (check KNOWN_POST_2021_CHANGES in script)")

    lines += [
        f"",
        f"### 🔵 L7 open items with LSC corroboration",
        f"",
    ]
    l7_lsc = [r for r in results if "LSC-SUPPORTS" in r[2] or "OPEN-L7" in r[2]]
    if l7_lsc:
        for code, name, cls, c_days, l_days, _ in l7_lsc:
            lines.append(f"- **{code}:** LSC says no minimum (2021); CJaC L7 open — feed to attorney review")
    else:
        lines.append("- None (or L7 items already resolved)")

    lines += [
        f"",
        f"---",
        f"",
        f"## Using this report",
        f"",
        f"- **MATCH rows → corroboration evidence.** Log count in VALIDATION_METRICS_LEDGER.md.",
        f"- **DIVERGENCE-PERIOD / NO-NOTICE divergence → investigate first.** If the law didn't change post-2021, one side is wrong.",
        f"- **DIVERGENCE-POST2021-CHANGE → cite as recency advantage.** LSC is frozen; CJaC reflects current law.",
        f"- **OPEN-L7-LSC-SUPPORTS → feed to attorney review.** Independent 2021 coding corroborates one position.",
        f"",
        f"---",
        f"",
        f"*LSC Cross-Check Report · Civil Justice as Code · {TODAY} · Copyright 2026 Andrew M Cohen · Apache 2.0*",
    ]

    report = "\n".join(lines)
    report_path = _DOCS_DIR / f"LSC_CROSSCHECK_REPORT_{TODAY}.md"

    if dry_run:
        print(report)
        print(f"\n[DRY RUN — not written]")
    else:
        with open(report_path, "w") as f:
            f.write(report)
        print(f"\nReport written: {report_path}")

    # Print summary to console
    print(f"\n{'='*60}")
    print(f"LSC Cross-Check Summary")
    for cat, n in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {n}")
    print(f"{'='*60}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LSC Baseline Cross-Check")
    parser.add_argument("--lsc-file", required=True,
                        help="Path to downloaded LawAtlas Excel file")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print report to stdout instead of writing file")
    args = parser.parse_args()

    run_crosscheck(lsc_path=args.lsc_file, dry_run=args.dry_run)
