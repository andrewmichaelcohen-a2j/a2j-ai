# L2 Multi-Model Consensus Report — Service Module

**Run date:** 2026-06-20
**Models:** OpenAI `gpt-5.5` · Google `gemini-2.5-pro`
**Target:** Service module — permitted service methods and statutory citations
**States run:** 9 / 51

> **Interpretation caveat:** Model consensus corroborates but does not prove correctness.
> **Divergence is the stronger signal.** Consensus ≠ current law — see recency guardrail flags.

---

## Summary

| Classification | Count |
|---------------|-------|
| ✅ CONSENSUS-CONFIRM | 0 |
| ✅ SAME-STATUTE-CONFIRMED | 2 |
| 🟡 SUBSECTION-FOUND | 0 |
| 🟡 CITATION-DIVERGENCE | 0 |
| 🟡 METHOD-AVAILABILITY-DIFF | 0 |
| 🔴 MODEL-SPLIT | 2 |
| ❌ ERROR | 5 |

---

## Same-Statute Hypothesis (H1)

**States with same-statute pattern in file:** 6
- SAME-STATUTE-CONFIRMED (single-provision statute is correct): 2
  - MS, NE
- SUBSECTION-FOUND (file may have captured only section header): 0
  - 

---

## Per-State Results

| State | File same-statute? | File statutes | GPT confidence | Gemini confidence | Classification |
|-------|-------------------|--------------|---------------|------------------|----------------|
| AR | no | Ark. Code Ann. §18-60-301; §18-17-703; Ark. Code A | ERR | high | ❌ ERROR |
| DC | yes | D.C. Code §42-3208; SCR-LT 5 | ERR | high | ❌ ERROR |
| MS | yes | Miss. Code Ann. §89-7-27 | medium | high | ✅ SAME-STATUTE-CONFIRMED |
| NE | yes | Neb. Rev. Stat. §76-1432 | medium | high | ✅ SAME-STATUTE-CONFIRMED |
| NM | yes | NMSA 1978 §47-8-33 | ERR | high | ❌ ERROR |
| NV | no | NRS 40.280(1)(b); NRS 40.280(1)(c); NRS 40.280(1)( | high | high | 🔴 MODEL-SPLIT |
| TN | no | TCA §66-28-505(a)(1); TCA §66-28-505(a)(3); TCA §6 | high | high | 🔴 MODEL-SPLIT |
| VA | yes | Va. Code §55.1-1245(A) | ERR | high | ❌ ERROR |
| WI | yes | Wis. Stat. §704.21 | ERR | high | ❌ ERROR |

---

## Items Requiring Human Review (2)

### NV (Nevada) — MODEL-SPLIT
- File unique statutes: ['NRS 40.280(1)(b)', 'NRS 40.280(1)(c)', 'NRS 40.280(1)(a)']
- File same-statute: False
- GPT service methods:
  - personal: NRS 40.280(1)(a)
  - substituted: NRS 40.280(1)(b)
  - posting_and_mailing: NRS 40.280(1)(c)
- Gemini service methods:
  - personal: NRS 40.280(1)(a)
  - substituted: NRS 40.280(1)(b)
  - posting_and_mailing: NRS 40.280(1)(c)

### TN (Tennessee) — MODEL-SPLIT
- File unique statutes: ['TCA §66-28-505(a)(1)', 'TCA §66-28-505(a)(3)', 'TCA §66-28-505(a)(2)']
- File same-statute: False
- GPT service methods:
  - personal: Tenn. Code Ann. § 66-28-107(d)(3)
  - mail: Tenn. Code Ann. §§ 66-28-107(d)(3), 66-28-505(b)(1)
- Gemini service methods:
  - personal: T.C.A. § 66-28-105(c)(3)
  - mail: T.C.A. § 66-28-105(c)(3)

---

## Recency Watch States (1)

> These states have L6-SERVICE-RECENCY-WATCH flags. Consensus ≠ current law — verify against current statute.

- **VA**: HB 15/SB 48 (2026) amended §55.1-1245; service provisions under §55.1-1415 may be affected

---

## What this run covers / does NOT cover

**Covers:** Whether the file's cited statutes for each service method are corroborated by two independent AI models.
**Does NOT cover:** Service defect elements, adds_days_for_mail accuracy, local court rules on service,
whether the service module is complete vs. comprehensive. Coverage is narrow: citation corroboration only.

---

*L2 corroborates and flags. It never blesses and never auto-edits content.*
*No file was advanced past AUTOMATED-CHECKS-PASSED by this run.*

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
