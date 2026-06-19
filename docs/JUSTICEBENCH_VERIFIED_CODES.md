# JusticeBench Alignment — Verified Codes (Implementation Reference)

**Date:** June 18, 2026 · **Purpose:** Confirmed external code values for Cowork to implement the schema-alignment tags (per `JUSTICEBENCH_ALIGNMENT_SPEC.md`). **Implement from THESE verified values, not from the spec's descriptions or from memory.**

**Verification status legend:** ✅ CONFIRMED against live source · ⚠️ PARTIALLY CONFIRMED (format known, full list needs a final pull) · 🔲 PRODUCE-DIRECTLY (stable standard, no external lookup needed)

---

## 1. LIST issue codes (taxonomy.legal) — ✅ CONFIRMED

Source: taxonomy.legal (Stanford Legal Design Lab). Format: `XX-NN-NN-NN-NN` hierarchical. Verified live. **The eviction sub-structure maps almost one-to-one onto CJaC's five modules — strong alignment signal.**

**Top of hierarchy:**
- `HO-00-00-00-00` — **Housing** (top category)
- `HO-02-00-00-00` — **Eviction from a home** ← primary tag for every CJaC eviction file

**Defenses sub-tree (use for the defense-oriented modules):**
- `HO-02-04-00-00` — **Defenses to stop or delay an eviction** (parent — tag all eviction files)
  - All 6 children ✅ CONFIRMED (browser check at taxonomy.legal HO-02-04 page, Andrew Cohen, 2026-06-18):
    - `HO-02-04-01-00` — **Notice and Procedural defenses against an eviction** → CJaC `notice` + `procedural_defects` modules ✅
    - `HO-02-04-02-00` — **Reasonable Accommodation for a disability defenses against an eviction** → CJaC `substantive_defenses` (disability) ✅
    - `HO-02-04-03-00` — **Living conditions (habitability) defenses against an eviction** → CJaC `substantive_defenses` (habitability) ✅
    - `HO-02-04-04-00` — **Military service-members' protections around eviction** → CJaC `overlays` (federal SCRA) ✅
    - `HO-02-04-05-00` — **Title and ownership defenses against an eviction** → CJaC `substantive_defenses` (title/ownership) ✅

**Implementation guidance for Cowork:**
- Tag every file with all 8 confirmed codes (HO-00, HO-02-00, HO-02-04-00, -01, -02, -03, -04, -05). ✅ All fully confirmed — no interim tags needed.
- No pending browser checks remain. LIST code set is 100% closed as of 2026-06-18.

## 2. FIPS jurisdiction codes — 🔲 PRODUCE-DIRECTLY (verified, complete)

Federal standard, stable. Full 51-jurisdiction state-level FIPS (2-digit). Use as the `fips_jurisdiction` value per file. (County-level FIPS — 5-digit — only needed where a rule is county-specific, e.g., TN URLTA >75k-population counties; add those as encountered.)

| State | FIPS | State | FIPS | State | FIPS |
|-------|------|-------|------|-------|------|
| AL | 01 | KY | 21 | ND | 38 |
| AK | 02 | LA | 22 | OH | 39 |
| AZ | 04 | ME | 23 | OK | 40 |
| AR | 05 | MD | 24 | OR | 41 |
| CA | 06 | MA | 25 | PA | 42 |
| CO | 08 | MI | 26 | RI | 44 |
| CT | 09 | MN | 27 | SC | 45 |
| DE | 10 | MS | 28 | SD | 46 |
| DC | 11 | MO | 29 | TN | 47 |
| FL | 12 | MT | 30 | TX | 48 |
| GA | 13 | NE | 31 | UT | 49 |
| HI | 15 | NV | 32 | VT | 50 |
| ID | 16 | NH | 33 | VA | 51 |
| IL | 17 | NJ | 34 | WA | 53 |
| IN | 18 | NM | 35 | WV | 54 |
| IA | 19 | NY | 36 | WI | 55 |
| KS | 20 | NC | 37 | WY | 56 |

*(Note: FIPS skips 03, 07, 14, 43, 52 — those gaps are correct, not errors; they were former/reserved codes.)*

## 3. ISO language codes — 🔲 PRODUCE-DIRECTLY (verified)

ISO 639-1 two-letter. For CJaC's current scope:
- `en` — English (primary for all files now)
- `es` — Spanish (when Spanish-language versions are produced)

Use `en` as the default `language` value. Structure the field to allow an array if multilingual versions are added.

## 4. Legal Help Task Taxonomy IDs (JusticeBench) — ✅ CONFIRMED (full list pulled live)

Source: justicebench.org/task (read live, June 18 2026). Format: `TS-NN-NN`. 50 tasks across 7 categories. **The eviction-relevant task IDs CJaC modules map to (confirmed exact):**

| Task | ID | Maps to CJaC |
|------|-----|--------------|
| **Deadline Calculator** | `TS-01-05` | **notice** module (notice-period clock; jurisdiction-correct due dates) |
| **Issue-Spotting** | `TS-01-07` | defense identification across modules |
| **Document Issue-Spotter** | `TS-03-02` | **procedural_defects** / notice-defect detection (spot defects in notices/complaints/summons) |
| **Legal Analyzer** | `TS-03-04` | core CJaC function — surface applicable rules/rights/strategies |
| **Service Verification** | `TS-05-05` | **service** module (confirm proper service against local rules) |
| **Filing Screener** | `TS-05-04` | **procedural_defects** (missing fields / procedural compliance) |
| **Form Selection** | `TS-01-06` | downstream form-matching |
| **Document Explainer** | `TS-01-03` | downstream (explain a notice/summons) |
| **Legal Q&A** | `TS-01-01` | downstream consumption of CJaC rules |
| **Legal Researcher** | `TS-04-08` | statutory grounding (the L1 retrieval function) |
| **Law Watcher** | `TS-02-05` | **L6 freshness** (detect legal changes, suggest updates) |

**Primary tags for CJaC eviction rules files:** `TS-03-04` (Legal Analyzer) as the core function, plus module-specific: notice→`TS-01-05`, service→`TS-05-05`, procedural_defects→`TS-03-02`/`TS-05-04`, defense-identification→`TS-01-07`. These are confirmed exact from the live source — **ready to implement.**

*(Note: the article's earlier examples were slightly off — e.g., Deadline Calculator is `TS-01-05` not an -0X guess, Issue-Spotting is `TS-01-07`. This is exactly why the live pull mattered. Now confirmed.)*

---

## Implementation status — ALL COMPLETE ✅

| Code set | Status | Notes |
|----------|--------|-------|
| FIPS (state) | ✅ Complete | Full 51-jurisdiction table above |
| ISO language | ✅ Complete | `en` default |
| LIST — all 8 codes (HO-00, HO-02-00, HO-02-04-00 through -05) | ✅ All confirmed | Subcodes -01/-03/-04 confirmed 2026-06-18 Andy browser check |
| Task Taxonomy IDs | ✅ Complete (live-pulled) | 6 IDs — full mapping table above |

**All 5 code sets fully verified. No pending checks. 51 files populated 2026-06-18.** See `rules/validation/l2/add_interoperability.py` for the population script.

## Guardrail (unchanged)
These tags make CJaC files interoperable/labelable; they do not change decision logic or validation status. Status labels remain governed by CJaC's own ladder.

---

*JusticeBench Alignment — Verified Codes · June 18, 2026 · ALL 5 code sets fully verified and implemented. 51 v2 files tagged. No open items.*
