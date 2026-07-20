> **SUPERSEDED (2026-07-19, same evening).** This draft is superseded by `docs/RULE_PROPOSAL_1946_2a_ATTACHMENT_20260719.md`, delivered per the errata-cycle directive's narrowed Task 3 (adds the §1946.2(a)(2) variant with attorney-directed trigger logic, and per-tenant rather than aggregate occupancy inputs). Retained here for the record, not for ratification — do not act on this version.

# Candidate Rule Proposal — §1946.2(a) Just-Cause Attachment Threshold

**Date:** 2026-07-19
**Status:** PROPOSED — YELLOW, not applied. `ca_eviction_v2.json` remains untouched at vProof1.
**Origin:** v0.3 held-out miss autopsy (`docs/AUTOPSY_v0_3_MISSES_20260719.md`), CA-NOT-C-18.
**Authorized by:** Cowork Change Directive "v0.3 Held-Out Score Ingestion & AB 1482 Rule-Gap Cycle" (Andy, 2026-07-19), Task 3 — contingent on Task 2 confirming the rule is genuinely absent from vProof1. Confirmed absent for this provision (see autopsy).
**Scope note:** The directive's working hypothesis named three candidate provisions. Two — §1946.2(e)(7) and (e)(8) — turned out on inspection to already be fully encoded in vProof1, and the two golden-set items that appeared to miss on them (C-21, C-22) were subsequently determined by attorney errata (`docs/ERRATA_MEMO_v0_3_20260719.docx`) to be ground-truth errors, not model or rule errors. **No rule is proposed for those provisions — none is warranted.** This document proposes a rule for the third provision only: §1946.2(a).

---

## PROPOSED-2026-001 — §1946.2(a) just-cause attachment threshold

**Statutory pin:** Civ. Code §1946.2(a).

**Operative text (source: frozen golden-set authority field for CA-NOT-C-18, attorney-verified 2026-07-16 — this is the canonical text per the directive; no independent verbatim statute text is asserted beyond it):**

> "Just-cause protection attaches only after 12 months of continuous and lawful occupancy; 24-month variant where additional adult tenants added, Sec. 1946.2(a)(2)."

Companion provision already encoded and unaffected: Civ. Code §1946.1(c) — 30-day notice sufficient where occupancy is under 12 months (`notice.notice_types.termination.tenancy_under_1yr`, `days: 30`, `condition: all_occupants_residency_max_years < 1`).

**Golden-set item resolved:** CA-NOT-C-18 (9-month tenancy, no just-cause reason stated in a 30-day notice; frozen outcome NOTICE_VALID — just cause had not yet attached). Under the current encoding (`just_cause_required: true`, unconditional), the model has no path to reach VALID on facts like these; it will flag `missing_just_cause_reason` regardless of tenancy duration. This candidate rule closes that gap.

**Proposed encoding** (illustrative JSON, for Andy's ratification — not applied to any file):

```json
"just_cause_attachment": {
  "statute": "Civ. Code §1946.2(a)",
  "condition": "all_occupants_residency_max_years >= 1",
  "count_method": "calendar_days_to_years, same input convention as tenancy_under_1yr/tenancy_1yr_plus",
  "note": "PROPOSED 2026-07-19 (origin: v0.3 miss autopsy, CA-NOT-C-18). Just-cause protection under §1946.2 does not attach until the tenant (or, per the Stancil any-occupant convention already used for §1946.1(b)/(c) above, any current occupant) has resided 12 months. Before 12 months, no just-cause reason is required and §1946.1(c)'s 30-day notice governs. Reuses the existing max_occupant_residency_years input — no new fact input required.",
  "verification_needed": "Andy: confirm whether the Stancil any-occupant convention (used for §1946.1(b)/(c)) is the correct input methodology for §1946.2(a) attachment too, or whether §1946.2(a) uses a different (e.g. named-tenant-only) measure. The golden-set authority field for C-18 does not specify; C-18's facts do not distinguish the two methodologies (single named tenant, no other occupants)."
}
```

**Proposed defect-gate update** (`notice.notice_defects[3]`, `missing_just_cause_reason` — the `ab1482_coverage_gate`), for Andy's ratification:

Add, ahead of the existing exemption checklist: *"Before applying this defect, first confirm just-cause protection has attached: has any occupant resided 12+ months (`just_cause_attachment` above)? If not, this defect does not apply regardless of exemption status — see §1946.1(c) instead."*

**24-month / §1946.2(a)(2) variant — NOT drafted, flagged only.** The golden-set authority field references a "24-month variant where additional adult tenants added" but no frozen item tests it, and Cowork does not have attorney-verified text specifying the machine-checkable trigger (e.g., what counts as "additional," from what baseline date, whether it resets the 12-month clock or extends it). Per this project's no-fabrication discipline, no encoding is proposed for (a)(2) here. **Recommend deferring (a)(2) to the same drafting/ratification cycle as PROPOSED-2026-001 if Andy wants it now, or to a v0.4 freeze cycle if a test item is drafted for it first** — Andy's call.

**Day-count discipline check:** this proposal introduces no new day/period counting — it gates an existing boolean on an existing duration input (`all_occupants_residency_max_years`, already `calendar_days`-based per the `tenancy_under_1yr`/`tenancy_1yr_plus` fields it's drawn from). No bare "days" language used.

**Traceability:** originates from v0.3 held-out miss autopsy (`docs/AUTOPSY_v0_3_MISSES_20260719.md`), CA-NOT-C-18, confirmed as a genuine coverage gap (not superseded by the 2026-07-19 errata, unlike C-21/C-22).

---

## Ratification checklist (Andy, item-by-item, mirroring golden-set freeze discipline)

- [ ] PROPOSED-2026-001 (§1946.2(a) 12-month attachment threshold, general case): RATIFY / REJECT / MODIFY
- [ ] Attachment-methodology question above (Stancil any-occupant convention vs. named-tenant-only): resolve
- [ ] §1946.2(a)(2) 24-month/additional-adult-tenants variant: DEFER (recommended) / DRAFT NOW (needs source text from Andy) / OUT OF SCOPE

**On ratification:** per the directive's Task 4 (staged, not executed until ratification), Cowork will cut a new rules version (vProof1 remains immutable; new file, new SHA, changelog entry linking to this ratification), run the Direction D-1 dev-set regression (v0.2 dev, 12 items — must be 12/12 with `newly_failing=0`, or revert-and-report RED), and explicitly will NOT re-score the v0.3 held-out set (permanently burned; a v0.4 set would be required for the next held-out measurement, drafted only on Andy's direction).

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
