# Coverage Audit — v2 Rules Library
**Civil Justice as Code · a2j-ai repo**
**Audit date:** June 16, 2026 · **Auditor:** Claude (Cowork, read-only) · **Requested by:** Andy Cohen
**Scope:** All 51 `*_eviction_v2.json` files · All 5 modules per file · Read-and-report only — no file edits, no status changes.

---

## Purpose

The State of Record reports validation status (DRAFT / AUTOMATED-CHECKS-PASSED) but not content depth. This audit answers the prior question: *how much content actually exists in each module, and how much is empty scaffolding?* The goal is to size the build with real numbers before committing to a full five-module population effort.

---

## Summary Table

| Module | Populated | Skeletal | Stubbed | Absent | Depth (dominant) | Grounding rate | One-line finding |
|--------|-----------|----------|---------|--------|------------------|----------------|-----------------|
| **notice** | 51 | 0 | 0 | 0 | full | 51 / 51 | Only fully complete module — real days + statutes for all 51 states |
| **service** | 4 | 47 | 0 | 0 | skeletal | 4 / 51 | Demo states (CA/TX/NY/FL) have real statutes; 47 states have method names but statute: null throughout |
| **overlays** | — | — | — | 0 | mixed | varies by layer | Three-layer module; federal consistent; state_prot 43/51 all-placeholder; local critically contaminated |
| **substantive\_defenses** | 0 | 51 | 0 | 0 | skeletal | 0 / 51 | Uniform 5–6 item taxonomy, named defenses + elements — but zero real statutes across all 51 files |
| **procedural\_defects** | 0 | 51 | 0 | 0 | skeletal | 1 / 51 | Same pattern — consistent defect taxonomy, consequence text — but 203/204 statutes are [VERIFY] placeholder |

*Depth tiers: **full** = real values in all core fields; **skeletal** = named items with prose structure, statutes all placeholder or null; **stubbed** = schema key exists, nothing filled. **Absent** = top-level key missing.*

*Grounding = at least one non-placeholder statutory citation in the module for that state.*

---

## Per-Module Narrative

### 1. notice

**51 / 51 populated. 51 / 51 grounded. The most mature module by a wide margin.**

Every file has a `notice_types` dict with three keys (`pay_or_quit`, `cure_or_quit`, `termination`). Two of the three (`pay_or_quit` and one other) have real statutory content: actual days, a real statute citation (not a placeholder), and a `count_method` value. This is the direct output of the L1 retrieval pass, which ran to completion across all 51 states.

Notice defects are populated in all 51 files: 43 files carry 2 defects, 7 carry 3, 1 (CA) carries 4. These include entries like `late_fees_in_notice_void_notice` and `demand_amount_overstated` — specific, substantive, and in many cases already cited to a statute.

The only thing to note is that `cure_or_quit` and `termination` entries have somewhat less depth than `pay_or_quit` for non-demo states (cure_or_quit days may be present without full count_method detail). But no file is empty or placeholder on notice. This module is ready for L7 attorney review as-is.

---

### 2. service

**4 / 51 with real statutory grounding (CA, TX, NY, FL). 47 / 51 structurally present but ungrounded.**

Every file has a `permitted_methods` list (2–3 entries: `personal`, `substituted` or `certified_mail`, and `nail_and_mail` or `posting` or `mail` depending on state). Every file has 2 `service_defects` entries. Structure-wise, this looks populated for all 51 states.

The quality split is sharp: the 4 demo states have real statutory citations throughout (CA cites CCP §1162; TX cites Tex. Prop. Code §24.005(a)/(f); NY cites RPAPL §735; FL cites Fla. Stat. §83.56). For the other 47 states, `statute` is consistently `null` — not a `[VERIFY]` placeholder, just empty. This is the distinguishing pattern: the field wasn't filled with even an aspirational marker.

The permitted method types (`personal`, `substituted`, `certified_mail`) look reasonable and are likely accurate for most states, but without statutory backing they cannot be confirmed. The method_rules dict, which carries state-specific rules for each method (e.g., attempts required before substituted service, mailing requirements), is structurally present but empty of statutes in all 47 non-demo states.

**The service module is the "hidden risk" module**: it passes ACP because method entries exist, but the actual statutory grounding required for any real-world use is present for only 4 states.

---

### 3. overlays

**All 51 files have entries. Quality varies dramatically by sub-layer. The local sub-layer has a critical data quality issue.**

The overlays module has three sub-layers. Each requires separate assessment:

**Federal sub-layer (51 / 51, consistent):** Every file has 1 entry — the CARES Act §4024 overlay. The content is consistent and plausible (applies_when, effect, and a statutory reference). This sub-layer is the most reliable in the module. 0 files are absent or placeholder.

**State-protective sub-layer (8 real-grounded / 43 all-placeholder):** Every file has 2 `state_protective` entries. The most common entries are "Implied Warranty of Habitability" and "Anti-Retaliation Protection." For 43 of 51 states, both entries carry `statute: "[VERIFY STATE STATUTE]"` — they are named but ungrounded. For 8 states (CA, NY, TX, FL, and a few others that received more research during generation), the entries carry real statutory citations. The content even in the placeholder states is not wrong — habitability warranty and anti-retaliation are genuine state-level protections in essentially every state — but it is unverified.

**Local sub-layer (critical data quality issue — cross-state contamination in 42 / 51 states):** This is the most significant finding in the audit. Every file has local entries (551 total across all 51 files), but only 77 of those 551 entries are both in-state and real-sourced. The bulk of the remaining 474 entries break into two categories:

- **Cross-state contamination (244 entries across 42 states):** The v2 generation process appears to have templated a set of "notable cities with tenant protections" — Phoenix, Tucson, Denver, Atlanta, Chicago, Cook County — into local overlay slots for states where those cities do not exist. Georgia's local overlays include Phoenix, Tucson, and Denver. Maryland's include the same three, plus Chicago and Cook County. Indiana's include all five. These are not placeholder prompts — they are named jurisdictions in the wrong states' files.

- **Placeholder entries for correct-state cities (186 entries):** Many files do have correct-state cities listed (e.g., Atlanta in Georgia, Baltimore City in Maryland) but with `source: "[VERIFY]"` — placeholders indicating the work was scoped but not done.

The only state with clean, uncontaminated local data is California (7 in-state real entries, 0 cross-state contamination, 0 placeholders). New Jersey, New York, and Illinois are the next best — they have real entries for their major cities, though they may also have some contamination entries.

**The local sub-layer needs a dedicated cleanup pass before it can be considered even skeletal for the 42 contaminated states.** Cross-state city entries are not just incomplete — they are incorrect.

---

### 4. substantive\_defenses

**0 / 51 grounded. 51 / 51 skeletal. Zero real statutory citations anywhere in this module.**

Every file has 5–6 defenses. The same taxonomy appears in all 51 states: `habitability_warranty`, `retaliation`, `discrimination`, `breach_of_quiet_enjoyment`, `improper_rent_calculation` (and `other` in 9 states). Each defense has a `defense` key, an `elements` array (4–6 elements), an `openness` value (`fact_dependent`), a `review_weight` (`human_required`), and a `statute` field.

Every single `statute` field across all 51 files and all 264 defense entries reads `"[VERIFY STATE STATUTE — e.g., implied warranty of habitability]"` or similar. There are no exceptions. No state has a real statutory citation for any substantive defense.

The `elements` arrays are substantive prose (e.g., "Landlord knew or had notice of the defect," "Tenant gave landlord reasonable time to repair") and appear to reflect genuine common-law doctrine rather than random placeholder text. But these elements are clearly generic — the same text appears verbatim across all 51 states. They are a useful starting scaffold, but state law differs meaningfully on which defenses are available, their statutory basis, and the elements courts have applied.

**This module is large-build territory across all 51 states.** The taxonomy provides a useful skeleton; the element text provides a draft starting point; but everything needs state-specific statutory research and attorney-level review before any of it can be presented as accurate.

---

### 5. procedural\_defects

**0 / 51 meaningfully grounded (1 real statute in CA only, out of 204 total statute fields). 51 / 51 skeletal. Same pattern as substantive\_defenses.**

Every file has 4–5 defects. The taxonomy is consistent: `complaint_filed_before_notice_period_expired`, `improper_service_method`, `notice_not_in_writing`, `notice_defective_on_face` (and occasionally `filing_fee_not_paid` in CA). Each defect has a `defect` key, a `consequence` field with substantive prose (e.g., "Unlawful detainer action is premature; court lacks jurisdiction; may be dismissed"), and a `statute` field.

204 out of 205 statute fields read `"[VERIFY STATE STATUTE]"`. California's file has a single real citation (`CCP §1162`) in one of its 5 defects — the only exception across all 51 files.

The `consequence` text is more formulaic than the substantive_defenses elements, but it is not empty. Defects like "complaint filed before notice period expired" have accurate consequence descriptions that are likely correct in most states (premature filing = jurisdictional defect). However, the statutory basis for each defect varies by state — some states have bright-line statutes, others derive the rule from case law — and none of that state-specific grounding exists here.

**This module is also large-build territory, but potentially smaller than substantive\_defenses** because procedural defects tend to be more mechanical (filing timing, service method, notice form) and their elements are less open-textured. The taxonomy and consequence text are a reasonable scaffold.

---

## Flags

### Empty scaffolding across all/most states (the large-build modules)

- **`substantive_defenses`**: Uniform 5–6 item taxonomy, all 264 statutes placeholder. Zero states have real statutory grounding. Identical defense name sets in all 51 files (2 patterns: 42 states have 5 defenses, 9 states have 6). This module is not "started" in any meaningful legal sense — it is a labeled schema with generic doctrine prose.

- **`procedural_defects`**: Same pattern. Consistent defect taxonomy, consequence text present, 203/204 statutes placeholder. CA is the single exception (1 real statute).

### Ungrounded populated content (confidence-calibration priorities)

- **`service` (47 non-demo states)**: Structurally present, passes validation, but `statute: null` throughout. The method types listed are plausible but not verified to match each state's service statute. These 47 files should not be presented as having researched service rules — they have names, not law.

- **`overlays / state_protective` (43 states)**: Habitability warranty and anti-retaliation are named for all 51 states, but 43/51 have only `[VERIFY STATE STATUTE]`. Named-but-ungrounded protections in an L7-facing file are a confidence calibration risk: a reviewer could read them as "we know this applies" when the accurate reading is "this likely applies but has not been verified."

### Overlays local layer — specific flag requested

The local sub-layer in the overlays module has **no real local-ordinance content for 19 states, and cross-state contamination in 42 states.** The only state with clean, accurate local overlay data is California. The 77 "in-state real" entries distributed across the other 50 states include entries for major cities that happen to be in the right state (e.g., Denver in Colorado, Chicago in Illinois), but most states' files also carry wrong-state city entries alongside them.

The "local" question from the audit direction — *is there any local-ordinance content (city/county rent control, just-cause), or only federal/state?* — the honest answer is: yes, there is local content, but the majority of it is in the wrong states' files. There is essentially no reliable local layer outside of California.

---

## Counts for Reference

| Item | Count |
|------|-------|
| v2 files audited | 51 |
| notice module: files with real days + statute | 51 / 51 |
| notice_defects entries (total) | ~115 across 51 files |
| service module: files with real statute citations | 4 / 51 (CA, TX, NY, FL) |
| service module: files with statute: null | 47 / 51 |
| overlays federal entries (total) | 51 (1 per file) |
| overlays state_protective: real statutes | 21 entries across 8 states |
| overlays state_protective: [VERIFY] statutes | 86 entries across 43 states |
| overlays local: total entries | 551 |
| overlays local: in-state real-sourced | 77 |
| overlays local: cross-state contamination | 244 (in 42 states) |
| overlays local: placeholder [VERIFY] | 186 |
| substantive_defenses: total entries | 264 (5–6 per file) |
| substantive_defenses: real statutes | 0 |
| substantive_defenses: [VERIFY] statutes | 264 |
| procedural_defects: total entries | ~205 (4–5 per file) |
| procedural_defects: real statutes | 1 (CA) |
| procedural_defects: [VERIFY] statutes | 204 |

---

*Read-only audit — no files were modified. Sizes the five-module build. Andy and Claude to use these numbers for build sequencing.*
*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*
