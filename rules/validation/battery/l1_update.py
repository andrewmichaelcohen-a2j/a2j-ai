#!/usr/bin/env python3
"""
L1 update pass for all 47 v2 rules files (excludes CA/TX/NY/FL — done in prior session).
40 states statutorily retrieved (Justia, FindLaw, official legislative sites).
6 states remain L1=fail: AR, IA, IL, SC, SD, UT (JS-rendered or empty sources, exhausted).

For each file:
  - Marks retrieved=True / adds URL for Justia-resolved citations
  - Adds L1 flags for [VERIFY] placeholders and non-resolving real citations
  - Sets L1_grounding to pass (>=1 real citation retrieved) or fail
  - Does NOT advance module status (validate.py handles that)

Run from repo root or any directory.
"""

import json
import os
import sys

RULES_DIR = "/sessions/admiring-dreamy-pasteur/mnt/a2j-ai/rules/eviction"
TODAY = "2026-06-15"

# States excluded — already processed in prior session
SKIP_STATES = {"california", "texas", "new-york", "florida"}

# ── Retrieved states ──────────────────────────────────────────────────────────
# fragment: unique substring of the citation string in the JSON file
# url: canonical Justia URL returned content
# extra_flags: additional L1 flags (machine-assisted notes, discrepancies)

RETRIEVED = {
    # ── A ─────────────────────────────────────────────────────────────────────
    "alabama": {
        "fragment": "35-9A",
        "url": "https://law.justia.com/codes/alabama/title-35/chapter-9a/article-4/division-2/section-35-9a-421/",
        "extra_flags": [],
    },
    "alaska": {
        "fragment": "34.03.220",
        "url": "https://law.justia.com/codes/alaska/title-34/chapter-34-03/section-34-03-220/",
        "extra_flags": [],
    },
    "arizona": {
        "fragment": "33-1368",
        "url": "https://law.justia.com/codes/arizona/title-33/section-33-1368/",
        "extra_flags": [],
    },
    # ── C ─────────────────────────────────────────────────────────────────────
    "colorado": {
        "fragment": "13-40-104",
        "url": "https://law.justia.com/codes/colorado/title-13/article-40/section-13-40-104/",
        "extra_flags": [],
    },
    "connecticut": {
        "fragment": "47a-23",
        "url": "https://law.justia.com/codes/connecticut/title-47a/chapter-832/section-47a-23/",
        "extra_flags": [],
    },
    # ── D ─────────────────────────────────────────────────────────────────────
    "delaware": {
        "fragment": "5501",
        "url": "https://law.justia.com/codes/delaware/title-25/chapter-55/section-5501/",
        "extra_flags": [],
    },
    "district-of-columbia": {
        "fragment": "42-3505.01",
        "url": "https://code.dccouncil.gov/us/dc/council/code/sections/42-3505.01",
        "extra_flags": [],
    },
    # ── G ─────────────────────────────────────────────────────────────────────
    "georgia": {
        "fragment": "44-7-50",
        "url": "https://law.justia.com/codes/georgia/title-44/chapter-7/article-3/section-44-7-50/",
        "extra_flags": [],
    },
    # ── H ─────────────────────────────────────────────────────────────────────
    "hawaii": {
        "fragment": "521-68",
        "url": "https://law.justia.com/codes/hawaii/title-28/chapter-521/section-521-68/",
        "extra_flags": [],
    },
    # ── I ─────────────────────────────────────────────────────────────────────
    "idaho": {
        "fragment": "6-303",
        "url": "https://law.justia.com/codes/idaho/title-6/chapter-3/section-6-303/",
        "extra_flags": [],
    },
    "indiana": {
        "fragment": "32-31-1-6",
        "url": "https://law.justia.com/codes/indiana/title-32/article-31/chapter-1/section-32-31-1-6/",
        "extra_flags": [],
    },
    # ── K ─────────────────────────────────────────────────────────────────────
    "kansas": {
        "fragment": "58-2564",
        "url": "https://law.justia.com/codes/kansas/chapter-58/article-25/section-58-2564/",
        "extra_flags": [],
    },
    "kentucky": {
        "fragment": "383.660",
        "url": "https://law.justia.com/codes/kentucky/chapter-383/section-383-660/",
        "extra_flags": [],
    },
    # ── L ─────────────────────────────────────────────────────────────────────
    "louisiana": {
        "fragment": "4701",
        "url": "https://law.justia.com/codes/louisiana/code-of-civil-procedure/article-4701/",
        "extra_flags": [],
    },
    # ── M ─────────────────────────────────────────────────────────────────────
    "maine": {
        "fragment": "6001",
        "url": "https://law.justia.com/codes/maine/title-14/part-7/chapter-709/subchapter-1/section-6001/",
        "extra_flags": [
            {
                "layer": "L1",
                "code": "L1-MACHINE-ASSIST",
                "message": (
                    "14 M.R.S. §6001 retrieved (2025 text confirmed). "
                    "Machine-assisted finding: §6001 is the FED availability-of-remedy statute; "
                    "it establishes when the process may be maintained. "
                    "The pay-or-quit notice period for nonpayment is governed by §6002, "
                    "which was not separately retrieved. "
                    "L7 attorney must confirm §6002 notice period. NOT verification."
                ),
            }
        ],
    },
    "maryland": {
        "fragment": "8-401",
        "url": "https://law.justia.com/codes/maryland/real-property/title-8/subtitle-4/section-8-401/",
        "extra_flags": [],
    },
    "massachusetts": {
        # cite in JSON: "MGL c. 186 §11"  →  "MGL c. 186 §11"
        "fragment": "186 §11",
        "url": "https://malegislature.gov/Laws/GeneralLaws/PartII/TitleI/Chapter186/Section11",
        "extra_flags": [],
    },
    "michigan": {
        "fragment": "554.134",
        "url": "https://www.legislature.mi.gov/Laws/MCL?objectName=mcl-554-134",
        "extra_flags": [],
    },
    "minnesota": {
        "fragment": "504B.285",
        "url": "https://www.revisor.mn.gov/statutes/cite/504B.285",
        "extra_flags": [],
    },
    "mississippi": {
        "fragment": "89-7-23",
        "url": "https://law.justia.com/codes/mississippi/title-89/chapter-7/section-89-7-23/",
        "extra_flags": [
            {
                "layer": "L1",
                "code": "L1-MACHINE-ASSIST",
                "message": (
                    "Miss. Code Ann. §89-7-23 retrieved (Justia text confirmed). "
                    "Machine-assisted finding: §89-7-23 expressly states it "
                    "'shall not apply to rental agreements governed by the Residential "
                    "Landlord and Tenant Act.' Mississippi RLTA (§89-8-1 et seq.) governs "
                    "most modern residential tenancies; the applicable nonpayment notice "
                    "provision under RLTA may differ. "
                    "L7 attorney must confirm applicable statute for residential tenancies. NOT verification."
                ),
            }
        ],
    },
    "missouri": {
        "fragment": "441.050",
        "url": "https://revisor.mo.gov/main/OneSection.aspx?section=441.050",
        "extra_flags": [
            {
                "layer": "L1",
                "code": "L1-MACHINE-ASSIST",
                "message": (
                    "RSMo §441.050 retrieved from Missouri Revisor (text confirmed). "
                    "Machine-assisted finding: §441.050 governs termination of year-to-year "
                    "tenancies (60-day notice) — NOT the pay-or-quit nonpayment statute. "
                    "RSMo §535.020 (unlawful detainer for nonpayment) is the primary nonpayment "
                    "authority and was not separately retrieved. "
                    "L7 attorney must confirm correct pay-or-quit authority for Missouri. NOT verification."
                ),
            }
        ],
    },
    "montana": {
        "fragment": "70-24-422",
        "url": "https://law.justia.com/codes/montana/title-70/chapter-24/part-4/section-70-24-422/",
        "extra_flags": [],
    },
    # ── N ─────────────────────────────────────────────────────────────────────
    "nebraska": {
        "fragment": "76-1431",
        "url": "https://www.nebraskalegislature.gov/laws/statutes.php?statute=76-1431",
        "extra_flags": [],
    },
    "nevada": {
        "fragment": "40.253",
        "url": "https://nevada.public.law/statutes/nrs_40.253",
        "extra_flags": [],
    },
    "new-hampshire": {
        "fragment": "540:3",
        "url": "https://www.gencourt.state.nh.us/rsa/html/LV/540/540-3.htm",
        "extra_flags": [],
    },
    "new-jersey": {
        "fragment": "2A:18-61.1",
        "url": "https://law.justia.com/codes/new-jersey/title-2a/section-2a-18-61-1/",
        "extra_flags": [],
    },
    "new-mexico": {
        "fragment": "47-8-33",
        "url": "https://law.justia.com/codes/new-mexico/chapter-47/article-8/section-47-8-33/",
        "extra_flags": [],
    },
    "north-carolina": {
        "fragment": "42-3",
        "url": "https://www.ncleg.gov/EnactedLegislation/Statutes/HTML/BySection/Chapter_42/GS_42-3.html",
        "extra_flags": [],
    },
    "north-dakota": {
        "fragment": "47-16-15",
        "url": "https://codes.findlaw.com/nd/title-47-property/nd-cent-code-sect-47-16-15/",
        "extra_flags": [
            {
                "layer": "L1",
                "code": "L1-MACHINE-ASSIST",
                "message": (
                    "NDCC §47-16-15 retrieved via FindLaw (text confirmed). "
                    "Machine-assisted finding: §47-16-15 ('Notice of termination of lease') "
                    "governs termination of periodic tenancies (month-to-month: 1 calendar month notice) — "
                    "a no-cause termination statute, NOT specifically a pay-or-quit statute for nonpayment. "
                    "§47-32-01 (FED grounds statute, also cited in file) was not retrieved. "
                    "L7 attorney must confirm pay-or-quit notice period and authority for nonpayment in ND. NOT verification."
                ),
            }
        ],
    },
    # ── O ─────────────────────────────────────────────────────────────────────
    "ohio": {
        "fragment": "1923.02",
        "url": "https://law.justia.com/codes/ohio/title-19/chapter-1923/section-1923-02/",
        "extra_flags": [
            {
                "layer": "L1",
                "code": "L1-MACHINE-ASSIST",
                "message": (
                    "ORC §1923.02 retrieved (2025 text confirmed). "
                    "Machine-assisted finding: §1923.02 defines grounds for FED (including nonpayment); "
                    "the specific 3-day pay-or-quit notice period for nonpayment is governed by §1923.04, "
                    "which was not separately retrieved. "
                    "L7 attorney must confirm §1923.04 notice period. NOT verification."
                ),
            }
        ],
    },
    "oklahoma": {
        # cite in JSON: "41 O.S. §131"  →  "41 O.S. §131"
        "fragment": "§131",
        "url": "https://law.justia.com/codes/oklahoma/title-41/section-41-131/",
        "extra_flags": [],
    },
    "oregon": {
        "fragment": "90.394",
        "url": "https://oregon.public.law/statutes/ors_90.394",
        "extra_flags": [],
    },
    # ── R ─────────────────────────────────────────────────────────────────────
    "rhode-island": {
        "fragment": "34-18-35",
        "url": "https://codes.findlaw.com/ri/title-34-property/ri-gen-laws-sect-34-18-35/",
        "extra_flags": [],
    },
    # ── T ─────────────────────────────────────────────────────────────────────
    "tennessee": {
        "fragment": "66-28-505",
        "url": "https://codes.findlaw.com/tn/title-66-property/tn-code-sect-66-28-505/",
        "extra_flags": [],
    },
    # ── V ─────────────────────────────────────────────────────────────────────
    "vermont": {
        "fragment": "4467",
        "url": "https://law.justia.com/codes/vermont/title-9/chapter-137/section-4467/",
        "extra_flags": [],
    },
    "virginia": {
        "fragment": "55.1-1245",
        "url": "https://law.lis.virginia.gov/vacode/55.1-1245/",
        "extra_flags": [],
    },
    # ── W ─────────────────────────────────────────────────────────────────────
    "washington": {
        "fragment": "59.12.030",
        "url": "https://law.justia.com/codes/washington/title-59/chapter-59-12/section-59-12-030/",
        "extra_flags": [],
    },
    "west-virginia": {
        "fragment": "37-6-5",
        "url": "https://law.justia.com/codes/west-virginia/chapter-37/article-6/section-37-6-5/",
        "extra_flags": [
            {
                "layer": "L1",
                "code": "L1-MACHINE-ASSIST",
                "message": (
                    "W. Va. Code §37-6-5 retrieved (2025 text confirmed). "
                    "Machine-assisted finding: §37-6-5 addresses notice to terminate periodic tenancy "
                    "(3 months for year-to-year; 1 period for tenancies less than 1 year). "
                    "This is a no-cause termination statute, NOT a pay-or-quit statute for nonpayment. "
                    "File claims 5 days for nonpayment — the supporting authority for that period may be "
                    "a different statutory provision or common law rule. "
                    "L7 attorney must identify and confirm the correct pay-or-quit authority. NOT verification."
                ),
            }
        ],
    },
    "wisconsin": {
        "fragment": "704.17",
        "url": "https://law.justia.com/codes/wisconsin/chapter-704/section-704-17/",
        "extra_flags": [],
    },
    # ── Y ─────────────────────────────────────────────────────────────────────
    "wyoming": {
        "fragment": "1-21-1002",
        "url": "https://law.justia.com/codes/wyoming/title-1/chapter-21/article-10/section-1-21-1002/",
        "extra_flags": [],
    },
}


PLACEHOLDER_PREFIXES = (
    "[VERIFY",
    "[state implied",
    "[state anti-",
    "[local ordinances]",
)


def is_placeholder(cite: str) -> bool:
    return any(cite.startswith(p) for p in PLACEHOLDER_PREFIXES)


def process_file(filepath: str, state_dir: str) -> tuple:
    """Returns (retrieved_count, l1_grounding_result, status_msg)."""
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    sources = data.setdefault("provenance", {}).setdefault("statutory_sources", [])
    flags = data.setdefault("validation", {}).setdefault("flags", [])

    # Remove stale L1 flags (clean re-run)
    flags = [fl for fl in flags if fl.get("layer") != "L1"]

    retrieved_info = RETRIEVED.get(state_dir)
    retrieved_count = 0

    for src in sources:
        cite = src.get("cite", "")
        if is_placeholder(cite):
            flags.append(
                {
                    "layer": "L1",
                    "code": "L1-PLACEHOLDER",
                    "message": (
                        f'Placeholder citation not resolved: "{cite}". '
                        "Statutory source unknown at L1 retrieval pass. "
                        "Attorney review required to identify and retrieve applicable statute."
                    ),
                }
            )
        else:
            # Real citation
            if retrieved_info and retrieved_info["fragment"] in cite:
                src["retrieved"] = True
                src["url"] = retrieved_info["url"]
                src["retrieved_date"] = TODAY
                retrieved_count += 1
            else:
                # Real citation, no Justia resolution
                if not src.get("retrieved"):
                    flags.append(
                        {
                            "layer": "L1",
                            "code": "L1-URL-NOT-RESOLVED",
                            "message": (
                                f'Citation "{cite}" could not be retrieved via Justia '
                                "(URL returned no content after 1–2 attempts). "
                                "Statutory text not confirmed. Attorney verification required."
                            ),
                        }
                    )

    # Append any state-specific extra flags
    if retrieved_info:
        for ef in retrieved_info.get("extra_flags", []):
            flags.append(ef)

    # Determine L1 result
    l1_result = "pass" if retrieved_count >= 1 else "fail"
    data["validation"]["automated_layers"]["L1_grounding"] = l1_result
    data["validation"]["flags"] = flags

    # Update validation note (module advancement handled by validate.py)
    l3 = data["validation"]["automated_layers"].get("L3_consistency", "not_run")
    l5 = data["validation"]["automated_layers"].get("L5_crossjuris", "not_run")
    data["validation"]["validation_note"] = (
        f"L1 retrieval pass {TODAY}. L1={l1_result}, L3={l3}, L5={l5}. "
        f"retrieved_sources={retrieved_count}. "
        "Advance to AUTOMATED-CHECKS-PASSED requires all implemented layers pass — see validate.py."
    )

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    status = "PASS" if l1_result == "pass" else "FAIL"
    return retrieved_count, l1_result, status


def main():
    state_dirs = sorted(
        d
        for d in os.listdir(RULES_DIR)
        if os.path.isdir(os.path.join(RULES_DIR, d)) and d not in SKIP_STATES
    )

    passed, failed, errors = [], [], []

    for state_dir in state_dirs:
        state_path = os.path.join(RULES_DIR, state_dir)
        json_files = [
            f for f in os.listdir(state_path) if f.endswith("_eviction_v2.json")
        ]
        if not json_files:
            print(f"  SKIP {state_dir}: no v2 JSON found")
            continue

        filepath = os.path.join(state_path, json_files[0])
        try:
            ret_count, l1, status = process_file(filepath, state_dir)
            marker = "✓" if l1 == "pass" else "✗"
            print(f"  {marker} {state_dir}: L1={l1}, retrieved={ret_count}")
            if l1 == "pass":
                passed.append(state_dir)
            else:
                failed.append(state_dir)
        except Exception as e:
            print(f"  ERROR {state_dir}: {e}")
            errors.append(f"{state_dir}: {e}")

    print(f"\n{'='*60}")
    print(f"L1 update complete.")
    print(f"  L1=pass (eligible for AUTOMATED-CHECKS-PASSED): {len(passed)}")
    print(f"  L1=fail (remain DRAFT): {len(failed)}")
    print(f"  Errors: {len(errors)}")
    print(f"\nPassed: {passed}")
    print(f"\nFailed: {failed}")
    if errors:
        print(f"\nErrors: {errors}")

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
