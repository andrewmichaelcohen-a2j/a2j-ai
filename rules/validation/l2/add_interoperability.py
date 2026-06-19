#!/usr/bin/env python3
"""
add_interoperability.py — JusticeBench schema alignment pass
Adds interoperability block to all 51 eviction v2 rules files.
Implements ONLY from JUSTICEBENCH_VERIFIED_CODES.md confirmed values.
Insertion point: after "provenance", before "validation".

v2 update (2026-06-18): All 6 HO-02-04 defense subcodes now confirmed.
  HO-02-04-01-00 (Notice/Procedural), HO-02-04-03-00 (Habitability),
  HO-02-04-04-00 (Military) confirmed by Andy from taxonomy.legal browser check.
  _list_pending_subcodes field removed — no pending items.

Copyright 2026 Andrew M Cohen. Apache 2.0.
"""

import json
import os
import glob
import sys

# FIPS table — verified from JUSTICEBENCH_VERIFIED_CODES.md (federal standard, stable)
FIPS = {
    "AL": "01", "AK": "02", "AZ": "04", "AR": "05", "CA": "06",
    "CO": "08", "CT": "09", "DE": "10", "DC": "11", "FL": "12",
    "GA": "13", "HI": "15", "ID": "16", "IL": "17", "IN": "18",
    "IA": "19", "KS": "20", "KY": "21", "LA": "22", "ME": "23",
    "MD": "24", "MA": "25", "MI": "26", "MN": "27", "MS": "28",
    "MO": "29", "MT": "30", "NE": "31", "NV": "32", "NH": "33",
    "NJ": "34", "NM": "35", "NY": "36", "NC": "37", "ND": "38",
    "OH": "39", "OK": "40", "OR": "41", "PA": "42", "RI": "44",
    "SC": "45", "SD": "46", "TN": "47", "TX": "48", "UT": "49",
    "VT": "50", "VA": "51", "WA": "53", "WV": "54", "WI": "55",
    "WY": "56"
}

# Task taxonomy IDs — confirmed from justicebench.org/task live pull June 18, 2026
TASK_TAXONOMY_IDS = [
    "TS-03-04",  # Legal Analyzer (core CJaC function)
    "TS-01-07",  # Issue-Spotting (defense identification across modules)
    "TS-01-05",  # Deadline Calculator (notice module — jurisdiction-correct due dates)
    "TS-05-05",  # Service Verification (service module)
    "TS-03-02",  # Document Issue-Spotter (procedural_defects — spot defects in notices)
    "TS-05-04"   # Filing Screener (procedural_defects — procedural compliance)
]

# LIST codes — ALL 8 confirmed from taxonomy.legal (Stanford Legal Design Lab), June 18, 2026
# Top codes confirmed live June 18 (initial pass).
# Three defense subcodes confirmed June 18 by Andy browser check at taxonomy.legal HO-02-04 page:
#   HO-02-04-01-00 (Notice/Procedural), HO-02-04-03-00 (Habitability), HO-02-04-04-00 (Military)
# Module → subcode mapping:
#   notice → HO-02-04-01-00
#   procedural_defects → HO-02-04-01-00
#   substantive_defenses (habitability) → HO-02-04-03-00
#   overlays (servicemembers/SCRA) → HO-02-04-04-00
#   substantive_defenses (disability/RA) → HO-02-04-02-00
#   substantive_defenses (title) → HO-02-04-05-00
LIST_CODES = [
    "HO-00-00-00-00",  # Housing (top category)
    "HO-02-00-00-00",  # Eviction from a home (primary tag for all CJaC eviction files)
    "HO-02-04-00-00",  # Defenses to stop or delay an eviction (parent — tag all files)
    "HO-02-04-01-00",  # Notice and Procedural defenses → notice + procedural_defects modules
    "HO-02-04-02-00",  # Reasonable Accommodation for a disability → substantive_defenses (disability)
    "HO-02-04-03-00",  # Living conditions (habitability) defenses → substantive_defenses (habitability)
    "HO-02-04-04-00",  # Military service-members' protections → overlays (SCRA/servicemembers)
    "HO-02-04-05-00"   # Title and ownership defenses → substantive_defenses (title/ownership)
]


def build_interoperability(state_abbr):
    """Build the interoperability block for a given state abbreviation."""
    fips = FIPS.get(state_abbr)
    if fips is None:
        raise ValueError(f"Unknown state abbreviation: {state_abbr!r}")
    return {
        "fips_jurisdiction": fips,
        "language": ["en"],
        "task_taxonomy_ids": TASK_TAXONOMY_IDS,
        "list_codes": LIST_CODES
        # _list_pending_subcodes removed — all 6 HO-02-04 subcodes confirmed 2026-06-18
    }


def insert_after_provenance(data: dict, interop: dict) -> dict:
    """
    Returns a new dict with interoperability inserted after 'provenance'.
    Python 3.7+ dicts preserve insertion order.
    """
    new_data = {}
    inserted = False
    for key, value in data.items():
        if key == "interoperability":
            # Skip existing interoperability — we'll re-insert in the right place
            continue
        new_data[key] = value
        if key == "provenance" and not inserted:
            new_data["interoperability"] = interop
            inserted = True
    if not inserted:
        # provenance not found — append at end (shouldn't happen in valid v2 files)
        new_data["interoperability"] = interop
        print("  WARNING: 'provenance' key not found — interoperability appended at end")
    return new_data


def process_file(path: str) -> tuple[bool, str]:
    """Process a single v2 file. Returns (success, message)."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return False, f"JSON parse error: {e}"

    state = data.get("jurisdiction", {}).get("state", "")
    if not state:
        return False, "No jurisdiction.state found"

    try:
        interop = build_interoperability(state)
    except ValueError as e:
        return False, str(e)

    new_data = insert_after_provenance(data, interop)

    # Serialize — 2-space indent, no trailing newline (matches existing file style)
    output = json.dumps(new_data, indent=2, ensure_ascii=False)

    with open(path, "w", encoding="utf-8") as f:
        f.write(output)

    return True, f"FIPS={interop['fips_jurisdiction']}"


def main():
    rules_dir = "/sessions/admiring-dreamy-pasteur/mnt/a2j-ai/rules/eviction"
    pattern = os.path.join(rules_dir, "*", "*_v2.json")
    files = sorted(glob.glob(pattern))

    print(f"Found {len(files)} v2 files")
    print()

    success_count = 0
    fail_count = 0

    for path in files:
        short = os.path.relpath(path, rules_dir)
        ok, msg = process_file(path)
        status = "OK" if ok else "FAIL"
        print(f"  {status}  {short}  ({msg})")
        if ok:
            success_count += 1
        else:
            fail_count += 1

    print()
    print(f"Done: {success_count} succeeded, {fail_count} failed")
    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
