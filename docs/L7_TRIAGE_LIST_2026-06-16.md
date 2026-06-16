# L7 Triage List — Substantive Defenses Requiring Attorney Review
*Generated: June 16, 2026 | Five-Module Build*

## Overview

This list identifies entries in the `substantive_defenses` module that require specialist attorney review before the library can advance beyond AUTOMATED-CHECKS-PASSED. These are **grounding_gap** entries — defenses where the doctrine is open-textured, fact-dependent, or case-law-derived in ways that resist mechanical encoding.

**Total triage entries: 264** (across all 51 states — 5 per state, 6 for just-cause states)

**No `[VERIFY]` entries remain in any module as of this build.**

---

## Pattern by Defense Type

All 51 states have the same core triage entries in `substantive_defenses`:

| Defense | Status | Reason |
|---------|--------|--------|
| `habitability_warranty` | statute grounded — fact_dependent | Statute identified; elements, remedies, and rent-withholding defense availability are fact-dependent |
| `retaliation` | statute grounded — fact_dependent | Statute identified; presumption period, protected activities, and causal link are fact-dependent |
| `discrimination` | grounding_gap | 42 U.S.C. §3604 + state fair housing statute identified; discriminatory intent / disparate impact analysis is specialist-required |
| `breach_of_quiet_enjoyment` | grounding_gap | Primarily common law; constructive eviction standard varies — no reliable statute to cite |
| `improper_rent_calculation` | grounding_gap | State-specific rules on what may be included in rent demand require specialist review |
| `other` (just-cause states only) | grounding_gap | Just cause statute identified; coverage exemptions and enumerated grounds require specialist analysis |

---

## States Requiring Specialist Review for All 5 Core Defenses

**All 51 states.** The substantive_defenses module is intentionally not certifiable via automated checks — all entries carry `review_weight: specialist_required`.

---

## Just-Cause States (6 triage entries each)

These 9 states have an additional `other` defense entry for just cause eviction requirements:

| State | Just Cause Statute | grounding_gap Note |
|-------|---------------------|-------------------|
| **CA** | Civ. Code §1946.2 (AB 1482) | Coverage exemptions; no-fault grounds and relocation assistance |
| **DC** | D.C. Code §42-3505.01 | Rent stabilization coverage, exemptions |
| **MD** | Md. Code, Real Prop. §8-402.1 (Baltimore City) | Local vs. statewide applicability; MD has no statewide just cause |
| **ME** | 14 MRS §6002 | Enumerated grounds; notice requirements |
| **NH** | RSA 540:2 | "Refusal to vacate after notice" ground — current doctrine |
| **NJ** | NJSA 2A:18-61.1 | Applicable ground from 18 enumerated; relocation assistance |
| **NY** | RPL §226-c; RPAPL §1400 et seq. | Good Cause Eviction Law coverage exemptions; opt-out jurisdictions |
| **OR** | ORS 90.427 | Qualifying cause; notice period; relocation assistance |
| **WA** | RCW 59.18.650 | Coverage applicability; enumerated grounds |

---

## What Attorney Review Should Cover

For each state, a reviewing attorney should confirm:

1. **`habitability_warranty`**: Does the state recognize rent withholding as an affirmative defense to eviction (not just a damages claim)? What is the notice-and-cure requirement? Are there procedural prerequisites (escrow, etc.)?

2. **`retaliation`**: What is the rebuttable presumption period in this state? What activities are "protected"? Is the defense available in nonpayment evictions?

3. **`discrimination`**: Any state-specific protected classes beyond federal FHA? State administrative complaint requirements vs. direct civil action?

4. **`breach_of_quiet_enjoyment`**: Is constructive eviction recognized as a defense to eviction in this state? What is the standard?

5. **`improper_rent_calculation`**: If landlord's demand included unauthorized fees (late fees, attorney fees, etc.), does that void the notice or the claim? State-specific rule?

6. **`other` (just-cause states)**: Verify coverage scope, applicable enumerated ground, notice content requirements, and relocation assistance obligations.

---

## Prioritization for Attorney Review

**Priority 1 — Demo states:** CA (most developed), TX, NY (just-cause complexity)
**Priority 2 — DRAFT states (L5 flags):** DC, MA, MN, NJ, TN, VT, WA
**Priority 3 — Remaining 44 ACP states:** alphabetical order

---

*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*
