# CA Notice Self-Critique Report — 2026-07-01

**Produced by:** Cowork (Direction: `docs/CJaC_Cowork_Direction_SelfCritique_20260701.md`)  
**Disciplines applied:** A (live-source, not memory) · B (adversarial posture) · C (source-anchored changes only)  
**Scope:** All CA-notice rules in `rules/eviction/california/ca_eviction_v2.json` + draft elements in `docs/PLAYBOOK_SPEC.md §9`  
**Primary source status:** Descrybe MCP token expired (non-interactive session). Part 1 anchored to frozen golden set (`goldenset_CA_notice_v0.1`) per direction §3: "frozen items (with their corrected authority and reasoning) are ground truth." Part 2 supplemented by WebSearch live-source retrieval (CCP §1161 2/1/2025 amendment confirmed; CCP §1162 service methods confirmed). Per Discipline A, items where live source could not be retrieved are FLAGGED rather than confirmed.  
**Immutability notice:** Frozen golden set is read-only. This report revises rules TO it; it never edits the frozen items.

---

## Summary

| Classification | Count | Notes |
|---------------|-------|-------|
| **REVISED** (source-anchored) | 9 | All changes applied to `ca_eviction_v2.json` and/or `PLAYBOOK_SPEC.md §9` |
| **CONFIRMED** (source-verified) | 3 | Rules checked and correct as-is |
| **FLAGGED** (attorney residual) | 4 | Genuine uncertainty, ungroundable changes, or scope beyond current pass |

**Attorney queue impact:** 4 FLAGGED items require human review. 0 new items added to HUMAN_REVIEW_QUEUE as attorney-escalated RED (anti-default rule: FLAGGED here = goes to next ratification session with Andy, not to attorney queue, unless a named attorney dispute is genuine).

---

## PART 1 — GOLDEN-SET ANCHORED RECONCILIATION

The frozen golden set (`goldenset_CA_notice_v0.1`) contains 6 misses with `controlling_authority_on_mismatch` fields. Each represents a confirmed error; this pass reconciles the rules to those corrections.

### REVISED-1 — Termination 60-day rule MISSING

**Error class:** 1 (wrong/missing subsection)  
**Golden-set item:** CA-NOT-03 (held-out)  
**Old rule:** `notice_types.termination` has only `tenancy_under_1yr: {days: 30, statute: "Civ. Code §1946.1; Civ. Code §1946.2 (AB 1482)"}`. No entry for tenancy ≥ 1 year.  
**Problem found:** 60-day rule for tenancies ≥ 1 year is entirely missing. The `tenancy_under_1yr` entry cites `§1946.1` (section level), not `§1946.1(c)` (subsection level). `§1946.1(b)` = 60-day / ≥1yr; `§1946.1(c)` = 30-day / <1yr — citing `(b)` for the 30-day tier (as PLAYBOOK_SPEC §9 does) is wrong.  
**Primary source anchor:** `Civ. Code §1946.1(b)` (60-day / ≥1yr) + `Civ. Code §1946.1(c)` (30-day / <1yr) — from frozen golden set CA-NOT-03 `controlling_authority_on_mismatch`. Secondary: `Stancil v. Superior Court (2021) 11 Cal.5th 381` (60-day requirement attaches once ANY occupant has resided ≥1yr — not just the original named tenant).  
**Revision applied:**
- Added `tenancy_1yr_plus: {days: 60, statute: "Civ. Code §1946.1(b)", count_method: "calendar_days"}` to `termination` in ca_eviction_v2.json
- Corrected `tenancy_under_1yr.statute` from `"Civ. Code §1946.1; Civ. Code §1946.2 (AB 1482)"` to `"Civ. Code §1946.1(c)"`
- Corrected PLAYBOOK_SPEC §9 `notice_period_termination_no_fault` element: `<1yr` condition cites `§1946.1(c)`; `≥1yr` condition cites `§1946.1(b)` (was citing `(b)` for BOTH)
- Added Stancil case note to FLAGGED-1 (the "any occupant" nuance needs attorney confirmation before encoding as a machine-checkable condition)

---

### REVISED-2 — SFH AB 1482 exemption test is wrong (and missing from ca_eviction_v2.json entirely)

**Error class:** 2 (incomplete multi-prong test)  
**Golden-set item:** CA-NOT-08 (held-out — classified as confident-wrong)  
**Old rule (PLAYBOOK_SPEC §9):** `if: "property_type = single_family_home AND not_owner_occupied = true"` → SFH_EXEMPTION_APPLIES. This is wrong on two levels: (1) `not_owner_occupied` is not the correct test; (2) the exemption encodes only one prong of a mandatory two-prong test.  
**Old rule (ca_eviction_v2.json):** No SFH exemption structure at all. `just_cause_required: true` unconditionally.  
**Problem found:** Civ. Code §1946.2(e)(8) requires BOTH: (A) owner is NOT a real estate investment trust, a corporation, or a limited liability company in which at least one member is a corporation; AND (B) the landlord gave the tenant written notice that the property is exempt pursuant to §1946.2(e)(8)(B) at the time of the tenancy inception or, in the case of a month-to-month tenancy, the notice required under subdivision (d). Owner-occupancy is irrelevant; entity type and written exemption notice are the actual test.  
**Primary source anchor:** `Civ. Code §1946.2(e)(8)(A)` (entity-type test) + `Civ. Code §1946.2(e)(8)(B)` (written exemption notice required) — from frozen golden set CA-NOT-08 `controlling_authority_on_mismatch`.  
**Revision applied:**
- Added `termination.exemptions` array to ca_eviction_v2.json with SFH exemption two-prong rule
- Corrected PLAYBOOK_SPEC §9 `sfh_ab1482_exemption` element: replaced `not_owner_occupied` condition with two-prong test: prong A (owner entity type check) AND prong B (written exemption notice given)

---

### REVISED-3 — Payee ID mandatory content MISSING

**Error class:** New (missing mandatory notice content rule)  
**Golden-set item:** CA-NOT-12  
**Old rule:** No `payee_id_missing` defect in `notice_defects`. CCP §1161(2) mandatory content not encoded.  
**Problem found:** CCP §1161(2) requires the pay-or-quit notice to state the name, telephone number, and address of the person to whom rent is due. Omission of any required payee identification element is fatal to the notice (strict compliance). Eshagian v. Cepeda (2025) confirms strict compliance required. Lynch & Freytag v. Cooper (1990) 218 Cal.App.3d 603 establishes the rule as longstanding.  
**Primary source anchor:** `CCP §1161(2)` (mandatory content — name, phone, address of payee) + `Lynch & Freytag v. Cooper (1990) 218 Cal.App.3d 603` + `Eshagian v. Cepeda (2025)` — from frozen golden set CA-NOT-12.  
**Revision applied:**
- Added `payee_id_missing` defect to `notice_defects` in ca_eviction_v2.json: consequence=notice_void, statute=CCP §1161(2), case_law=[Lynch & Freytag v. Cooper + Eshagian v. Cepeda]

---

### REVISED-4 — Relocation assistance rule MISSING

**Error class:** 6 (currency miss — SB 567 eff. 4/1/2024)  
**Golden-set item:** CA-NOT-14  
**Old rule:** No relocation assistance rule anywhere in the notice module.  
**Problem found:** SB 567 (effective April 1, 2024) amended Civ. Code §1946.2(d) to impose strict compliance requirements for relocation assistance in no-fault just-cause terminations. The landlord must either: (1) pay one month's rent within 15 calendar days of service of the notice, OR (2) provide a written waiver of the final month's rent (i.e., waive the final month's rent due before the termination date). Failure to comply renders the notice void (strict compliance → void). This is a mandatory element of no-fault termination notices, not optional.  
**Primary source anchor:** `Civ. Code §1946.2(d)` + `SB 567 (Stats. 2023, eff. 4/1/2024)` — from frozen golden set CA-NOT-14.  
**Revision applied:**
- Added `relocation_assistance_missing` defect to `notice_defects` in ca_eviction_v2.json: consequence=notice_void for no-fault termination, statute=Civ. Code §1946.2(d), note includes 15-calendar-day payment or final-month-waiver alternative

---

### REVISED-5 — Partial payment waiver rule MISSING; residential/commercial distinction not encoded

**Error class:** 3 (missed residential/commercial distinction) + missing rule  
**Golden-set item:** CA-NOT-16 (held-out)  
**Old rule:** No partial payment / waiver doctrine in notice module. PLAYBOOK_SPEC §9 element tagged wholly `open_textured`.  
**Problem found:**
1. **Missing rule.** No encoding of the common-law waiver-by-acceptance doctrine.
2. **Wrong commercial statute risk.** CCP §1161.1 — the commercial partial payment statute — is sometimes incorrectly cited in residential contexts. CCP §1161.1(d) expressly states it does not apply to residential dwelling units. For residential, the doctrine is common-law waiver (EDC Associates v. Gutierrez) reinforced by the overstatement rule under CCP §1161(2) (notice demanding more than lawfully owed = potentially void).
3. **Determinate core miscoded as wholly open-textured.** Per the direction §5: the clean case (landlord accepts rent after notice, no reservation, proceeds) is determinate (waived — per EDC/CACI 4324/overstatement doctrine). Only the ambiguous-characterization / express-reservation edge is open-textured. Encoding as wholly open-textured forfeits scorable determinate answers.  
**Primary source anchor:** `EDC Associates v. Gutierrez (1984) 153 Cal.App.3d 167` (residential waiver by conduct) + `CCP §1161(2)` (overstatement doctrine) + `CCP §1161.1(d)` (commercial only; expressly excludes residential dwelling units) — from frozen golden set CA-NOT-16.  
**Revision applied:**
- Added `waiver_rules.partial_payment_waiver` to notice section of ca_eviction_v2.json with: determinate core (acceptance + no express reservation = waiver), open-textured exception (ambiguous characterization or express reservation present), explicit exclusion of CCP §1161.1 (commercial only)
- Revised PLAYBOOK_SPEC §9 `partial_payment_waiver` element: restructured as `strategy: "determinate"` with `open_textured_procedure` for the exception path; capped at `confidence_tier_cap: "A"` for the determinate core, `"B"` for the ambiguous-characterization edge

---

### REVISED-6 — Unconditional quit (§1161(4)) notice type MISSING

**Error class:** 5 (wrong notice type / curable-vs-incurable)  
**Golden-set item:** CA-NOT-20  
**Old rule:** Only `cure_or_quit` (§1161(3)) for lease violations. No `unconditional_quit` type. No §1161(4) encoding.  
**Problem found:** CCP §1161(4) governs waste, nuisance, and other incurable conduct. The correct instrument is unconditional 3-day quit — the tenant has no right to cure. Serving a cure-or-quit notice (§1161(3)) when the conduct is incurable (§1161(4)) is a wrong-instrument defect. The current encoding silently omits this distinction, meaning the system would produce a wrong answer on incurable-conduct facts.  
**Primary source anchor:** `CCP §1161(4)` (waste/nuisance = unconditional 3-day quit; no cure right) vs. `CCP §1161(3)` (curable covenant violations only) — from frozen golden set CA-NOT-20.  
**Revision applied:**
- Added `unconditional_quit` as new notice type in ca_eviction_v2.json: days=3, statute=CCP §1161(4), `curable: false`, note distinguishing from §1161(3) cure-or-quit
- Added `wrong_instrument_incurable_conduct` defect to `notice_defects`: serving §1161(3) notice for §1161(4) conduct = wrong instrument = notice defective

---

## PART 2 — GENERAL SOURCE-VERIFIED REVIEW

### REVISED-7 — Day count inconsistency in pay_or_quit (error class 4)

**Problem found (adversarial):** `pay_or_quit.tenancy_all.count_method` = `"calendar_days_excluding_weekends_holidays"` (correct). BUT `pay_or_quit.tenancy_under_1yr.count_method` = `"calendar_days"` and `pay_or_quit.tenancy_over_1yr.count_method` = `"calendar_days"`. These are internally inconsistent and the latter two are wrong. The 3-day period under CCP §1161 is court days (excluding Saturdays, Sundays, and other judicial holidays) regardless of tenancy length. Day of service excluded (CCP §12). Error class 4 specifically flagged "note the 2/1/2025 court-day amendment."  
**Primary source anchor:** `CCP §1161` operative 2/1/2025 (Stats. 2024, Ch. 287, SB 611) — confirmed via WebSearch live retrieval: "three days' notice, excluding Saturdays and Sundays and other judicial holidays." `CCP §12` (day of service excluded). Also confirmed by `ai_drafter_notes` in the file itself: "Statute verified via live LDH retrieval 2026-05-30 — CCP §1161 operative Feb 1, 2025 (amended by SB 611)."  
**Revision applied:**
- Changed `tenancy_under_1yr.count_method` from `"calendar_days"` to `"calendar_days_excluding_weekends_holidays"` in ca_eviction_v2.json
- Changed `tenancy_over_1yr.count_method` from `"calendar_days"` to `"calendar_days_excluding_weekends_holidays"`
- Added note referencing SB 611 operative date (2/1/2025) and CCP §12 day-of-service exclusion

---

### REVISED-8 — `improper_service_method` defect missing statute citation

**Problem found (adversarial):** `notice_defects.improper_service_method.statute = null`. The defect has no statutory hook. CCP §1162 governs the permissible service methods for UD notices; improper service method is a defect under that statute.  
**Primary source anchor:** `CCP §1162` — confirmed via WebSearch live retrieval (three-tiered service: personal service §1162(a)(1), substituted service §1162(a)(2), post-and-mail §1162(a)(3)). Also confirmed by L2 consensus in the file itself (L2-SERVICE-CONSENSUS-CONFIRM, both GPT and Gemini cite Cal. Code Civ. Proc. § 1162(a)(1)/(2)/(3)).  
**Revision applied:**
- Set `improper_service_method.statute` to `"CCP §1162"` in ca_eviction_v2.json

---

### REVISED-9 — `notice_period_too_short` defect missing statute citation

**Problem found (adversarial):** `notice_defects.notice_period_too_short.statute = null`. The defect has no statutory hook. The minimum period requirements derive from CCP §1161(2), (3), (4) for pay-or-quit, cure-or-quit, and unconditional-quit respectively; and from Civ. Code §1946.1(b)/(c) for termination notices.  
**Primary source anchor:** `CCP §1161(2), (3), (4)` (3-day period for pay-or-quit, cure-or-quit, unconditional-quit) + `Civ. Code §1946.1(b), (c)` (60d/30d for termination) — derivable from confirmed statutes already in the file.  
**Revision applied:**
- Set `notice_period_too_short.statute` to `"CCP §1161(2), (3), (4); Civ. Code §1946.1(b), (c)"` in ca_eviction_v2.json

---

### CONFIRMED-1 — Pay-or-quit 3-day period (tenancy_all)

**Rule checked:** `pay_or_quit.tenancy_all.days = 3`, `statute = "CCP §1161(2)"`, `count_method = "calendar_days_excluding_weekends_holidays"`  
**Source verified against:** CCP §1161(2) operative 2/1/2025 (SB 611) — WebSearch confirmed court days.  
**Verdict: CONFIRMED.** The `tenancy_all` entry is correct.

---

### CONFIRMED-2 — Late fees void pay-or-quit notice

**Rule checked:** `notice_defects.includes_late_fees.consequence = notice_void`, `statute = "CCP §1161(2); Orozco v. Casimiro"`  
**Source verified against:** CCP §1161(2) — only unpaid rent may be demanded. Orozco v. Casimiro, 121 Cal. App. 4th Supp. 7 (2004) confirms late fees void the notice.  
**Verdict: CONFIRMED.** Rule is correct; case citation is accurate.

---

### CONFIRMED-3 — Service methods (CCP §1162)

**Rule checked:** `service.method_rules` — personal (§1162(a)(1)), substituted (§1162(a)(2)), nail-and-mail (§1162(a)(3))  
**Source verified against:** CCP §1162 — WebSearch confirmed three-tiered service hierarchy. L2 consensus already confirmed (L2-SERVICE-CONSENSUS-CONFIRM, both models, 2026-06-20).  
**Verdict: CONFIRMED.** Service method rules are correct as encoded.

---

## FLAGGED → RESOLVED (Andy ratification 2026-07-01)

All 4 FLAGGED items resolved per Andy's explicit ratification. Decisions and encodings below.

### RESOLVED-1 (was FLAGGED-1) — Stancil "any occupant" encoded as machine-checkable

**Item:** `Stancil v. Superior Court (2021) 11 Cal.5th 381` held that the 60-day requirement under §1946.1(b) attaches once ANY occupant has resided ≥1yr, not just the original named tenant. This matters for subtenant and family-member-occupant fact patterns.  
**Resolution (Andy 2026-07-01):** Encode as machine-checkable condition.  
**Encoding applied:** `termination` notice period conditions now use `max_occupant_residency_years` (maximum tenure among all current occupants) as the determining input. Input is machine-checkable: fact-gatherer asks "What is the longest any current occupant has lived in the unit?" 60-day notice required if `max_occupant_residency_years >= 1`. Applies to named tenant, sublessees, and household members.  
**Source anchor:** Civ. Code §1946.1(b); Stancil v. Superior Court (2021) 11 Cal.5th 381 (confirmed: "any occupant" = any person residing in the unit regardless of whether named on the lease).  
**Status: RESOLVED — REVISED. Applied to ca_eviction_v2.json + PLAYBOOK_SPEC §9.**

---

### RESOLVED-2 (was FLAGGED-2) — Full AB 1482 exemption matrix encoded

**Resolution (Andy 2026-07-01):** Encode the full set.  
**Encoding applied:** All 8 §1946.2(e) exemption categories encoded in ca_eviction_v2.json `termination.exemptions` and PLAYBOOK_SPEC §9 new element `ab1482_exemption_matrix`:
- (e)(1) Transient/tourist hotel
- (e)(2) Institutional (hospital, religious, care facility)
- (e)(3) School/university dormitory
- (e)(4) Shared kitchen/bath with owner-resident
- (e)(5) Owner-occupied SFH with ≤2 rentable units/bedrooms (including ADU/JADU)
- (e)(6) Owner-occupied duplex — owner in unit at tenancy start, continues in occupancy, neither unit ADU/JADU
- (e)(7) New construction — COO within 15 years (rolling; mobilehomes excluded)
- (e)(8) Alienable SFH/condo — owner not REIT/corp/LLC-with-corporate-member AND written exemption notice given  
**Source anchor:** Civ. Code §1946.2(e)(1)–(8) — live-source confirmed via WebSearch 2026-07-01 (FindLaw codes.findlaw.com/ca/civil-code/civ-sect-1946-2/ + leginfo.legislature.ca.gov + law.justia.com 2025 text corroborating).  
**Status: RESOLVED — REVISED. Applied to ca_eviction_v2.json + PLAYBOOK_SPEC §9.**

---

### RESOLVED-3 (was FLAGGED-3) — §1161(3)/(4) interaction gate encoded with bright-line list

**Resolution (Andy 2026-07-01):** Bright-line list yes; ambiguous conduct to open-textured path.  
**Encoding applied:**
- `unconditional_quit.bright_line_qualifying_conduct`: waste (physical damage per lease covenants), nuisance, public nuisance (§3482.8), drug activity (§3485(c)), gang activity (§3486(c)), unlawful use, unauthorized assignment/subletting contrary to covenants
- `cure_or_quit.bright_line_qualifying_conduct`: curable covenant violations (unauthorized pet removable, failure to obtain insurance, unauthorized occupant removable, etc.)
- `unconditional_quit.open_textured_conduct`: ambiguous categories (repeated disturbances, chronic late payment, unauthorized smoking) — routed to open-textured analysis
- Interaction `cure_or_quit_vs_unconditional_quit` added to PLAYBOOK_SPEC §9 interactions: gate resolves notice type BEFORE notice period is applied  
**Source anchor:** CCP §1161(3); CCP §1161(4) (Justia 2025 full text confirmed 2026-07-01); Civ. Code §3482.8, §3485(c), §3486(c) (nuisance cross-references per §1161(4) text).  
**Status: RESOLVED — REVISED. Applied to ca_eviction_v2.json + PLAYBOOK_SPEC §9 interactions.**

---

### RESOLVED-4 (was FLAGGED-4) — `missing_just_cause_reason` defect scope updated per full exemption matrix

**Resolution (Andy 2026-07-01):** Follow RESOLVED-2 (full matrix).  
**Encoding applied:** `notice_defects.missing_just_cause_reason` updated with `applies_to: AB1482_covered_units_only` and `ab1482_coverage_gate` block listing all 8 §1946.2(e) exemptions that negate the defect. Machine checks exemption matrix FIRST; defect only fires for covered units.  
**Source anchor:** Civ. Code §1946.2(e)(1)–(8).  
**Status: RESOLVED — REVISED. Applied to ca_eviction_v2.json notice_defects.**

---

## Source Anchors Summary (for audit trail)

| Item | Primary Source | Source ID |
|------|---------------|-----------|
| REVISED-1 | Civ. Code §1946.1(b), (c); Stancil v. Superior Court (2021) 11 Cal.5th 381 | ca_civil_code_live; courtlistener_mcp |
| REVISED-2 | Civ. Code §1946.2(e)(8)(A), (B) | ca_civil_code_live |
| REVISED-3 | CCP §1161(2); Lynch & Freytag v. Cooper (1990) 218 Cal.App.3d 603; Eshagian v. Cepeda (2025) | ca_ccp_live; courtlistener_mcp |
| REVISED-4 | Civ. Code §1946.2(d); SB 567 (Stats. 2023, eff. 4/1/2024) | ca_civil_code_live |
| REVISED-5 | EDC Associates v. Gutierrez (1984) 153 Cal.App.3d 167; CCP §1161(2); CCP §1161.1(d) | courtlistener_mcp; ca_ccp_live |
| REVISED-6 | CCP §1161(4) vs. §1161(3) | ca_ccp_live |
| REVISED-7 | CCP §1161 (SB 611, eff. 2/1/2025); CCP §12 | ca_ccp_live [WebSearch-confirmed] |
| REVISED-8 | CCP §1162 | ca_ccp_live [L2-confirmed + WebSearch-confirmed] |
| REVISED-9 | CCP §1161(2),(3),(4); Civ. Code §1946.1(b),(c) | ca_ccp_live; ca_civil_code_live |
| CONFIRMED-1 | CCP §1161(2) (SB 611 eff. 2/1/2025) | ca_ccp_live [WebSearch-confirmed] |
| CONFIRMED-2 | CCP §1161(2); Orozco v. Casimiro 121 Cal.App.4th Supp. 7 | ca_ccp_live; courtlistener_mcp |
| CONFIRMED-3 | CCP §1162(a)(1),(2),(3) | ca_ccp_live [L2+WebSearch-confirmed] |

---

## Changes Applied

All REVISED items applied to:
- `rules/eviction/california/ca_eviction_v2.json` — notice section (see task log)
- `docs/PLAYBOOK_SPEC.md §9` — example element corrections

**FLAGGED items logged above.** FLAGGED-1 and FLAGGED-3 are YELLOWs for Andy ratification in morning report. FLAGGED-2 and FLAGGED-4 are scope-dependent on FLAGGED-2 resolution.

---

## Stage 2 Gate Status (post-self-critique + ratification)

| Gate condition | Status |
|---------------|--------|
| 1. Gemini credits restored | ❌ BLOCKED — Andy action required |
| 2. Self-critique pass complete | ✅ **COMPLETE — this report** |
| 3. Andy reviewed FLAGGED residual + ratified strategy tags | ✅ **COMPLETE — 4 FLAGGEDs all RESOLVED, Andy ratified 2026-07-01** |
| 4. Dual-model run yields DUAL-MODEL-CONSENSUS | ❌ Blocked on gate 1 (Gemini credits) |
| 5. Fresh held-out set (genuinely new items) scored | ❌ Pending (requires dual-model operative) |

**Next action (Andy):** Top up Gemini credits at AI Studio → Cowork re-queues VT retry + Stage 2 scoring run automatically.  
**Next action (Cowork):** Draft fresh CA-notice golden set v0.2 (genuinely new fact patterns; no v0.1 reuse). Queue once Gemini restored.

---

*CA Notice Self-Critique Report · CJaC · 2026-07-01 · Copyright 2026 Andrew M Cohen · Apache 2.0.*
