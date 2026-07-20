# Candidate Rule Proposal — Civ. Code §1946.2(a) Just-Cause Attachment Threshold (incl. (a)(2) variant)

**Date:** 2026-07-19
**Status:** ✅ RATIFIED 2026-07-20 (Andy: "confirmed - i approve") and APPLIED in `rules/eviction/california/ca_eviction_v3.json` (`ca_notice_rules_v3_20260720`, SHA `65f1d9a46487873163cd9ef5c5e2285c95a68bddb81e876a17e534b3de947c7d`). `ca_eviction_v2.json` remains untouched and immutable at vProof1 (`cc0cfab63ae1591e2b88…`) — v3 is a new file, not an edit. Dev-set regression gate: PENDING (see `docs/VALIDATION_METRICS_LEDGER.md`, v3 record).
**Directed by:** errata-cycle Cowork Change Directive (Andy, 2026-07-19), Task 3 — narrowed and proceeding now (this task is directed, not routing-gated; distinguish from the disconfirmed (e)(7)/(e)(8) hypothesis, for which no rule is proposed — see `docs/WIRING_DETERMINATION_1946_2e_20260719.md`).
**Traceability:** v0.3 held-out miss CA-NOT-C-18; `docs/AUTOPSY_v0_3_MISSES_20260719.md` (2026-07-19).
**Supersedes:** `docs/RULE_PROPOSALS_AB1482_20260719.md` (2026-07-19, earlier same evening — narrower draft, no (a)(2) encoding).

---

## PROPOSED-2026-001 (revised) — `just_cause_attachment_threshold`

**Statutory pin:** Civ. Code §1946.2(a), including the §1946.2(a)(2) additional-adult-tenant variant.

**Consequence if this precondition is NOT met:** `notice.notice_defects[3]` (`missing_just_cause_reason`) does not apply — just cause is not yet required, and Civ. Code §1946.1(c) governs instead (already correctly encoded: 30-day notice sufficient, `all_occupants_residency_max_years < 1`).

### Source text

**General rule (§1946.2(a))** — source: frozen golden-set authority field, CA-NOT-C-18, attorney-verified 2026-07-16:
> "Just-cause protection attaches only after 12 months of continuous and lawful occupancy."

Corroborated by CA-NOT-C-19's frozen authority field (attorney-verified 2026-07-16): *"Civ. Code Sec. 1946.2(a) (just cause required after 12 months' continuous and lawful occupancy; notice must state the just cause)"* — and the already-encoded voidness consequence, Civ. Code §1946.2(g), quoted verbatim in that same field: *"An owner's failure to comply with any provision of this section shall render the written termination notice void."* (§1946.2(g) is already encoded elsewhere in the rules file; not re-proposed here.)

**§1946.2(a)(2) variant** — source: attorney-directed operative text, this directive, 2026-07-19 (Andy, errata-cycle directive, Task 3):
> "the (a)(2) variant (additional adult tenant added: 12 months for all tenants or 24 months for at least one)"

**Provenance note on the (a)(2) text:** this is attorney-directed text supplied directly in the governing Cowork Change Directive, not independently verified by Cowork against the codified statute (no golden-set item tests it, and no prior frozen authority field states it). Recommend Andy confirm it against §1946.2(a)(2)'s verbatim text at ratification, consistent with this project's standing citation-verification discipline (e.g. the freeze memo's pre-review verification step) — flagged, not blocking.

### Golden-set items resolved / corroborated

- **CA-NOT-C-18** (resolved): 9-month tenancy, no just-cause reason in a 30-day notice; frozen NOTICE_VALID. Under current encoding (`just_cause_required: true`, unconditional), the model has no path to VALID regardless of duration. This proposal closes that gap — at 9 months, `just_cause_attachment_threshold` would evaluate false (single tenant, no (a)(2) trigger), so `missing_just_cause_reason` would not apply, and §1946.1(c)'s existing 30-day rule governs.
- **CA-NOT-C-19** (corroborates, does not need re-resolution — already scores correctly): 14-month tenancy, no just-cause reason in a 30-day notice; frozen NOTICE_INVALID. Under this proposal, at 14 months the general-rule threshold is met (single tenant, no (a)(2) trigger indicated in the facts), so `missing_just_cause_reason` applies and the notice is void — consistent with the frozen outcome and with C-19's own already-correct model prediction. Included here as a non-regression check: this proposal must not change C-19's (already-correct) result.

### Proposed encoding (illustrative JSON, for Andy's ratification — not applied to any file)

```json
"just_cause_attachment_threshold": {
  "statute": "Civ. Code §1946.2(a)",
  "inputs": [
    "per_tenant_continuous_occupancy_years — array, one value per current adult tenant (NOT the aggregate max_occupant_residency_years used elsewhere; this rule needs per-tenant granularity to evaluate the (a)(2) variant)",
    "additional_adult_tenant_added — boolean, true if any current adult tenant was added to the unit after the tenancy's initial commencement"
  ],
  "condition_general": {
    "applies_when": "additional_adult_tenant_added == false",
    "condition": "max(per_tenant_continuous_occupancy_years) >= 1",
    "note": "PROPOSED 2026-07-19 (origin: v0.3 miss autopsy, CA-NOT-C-18; corroborated CA-NOT-C-19). §1946.2(a) general rule: just-cause protection attaches once any current tenant has resided 12 months. Uses the Stancil any-occupant convention already applied to §1946.1(b)/(c) above — VERIFICATION NEEDED (see below): confirm this convention is correct for §1946.2(a) attachment specifically, not assumed from the §1946.1 provisions."
  },
  "condition_variant_a2": {
    "statute": "Civ. Code §1946.2(a)(2)",
    "applies_when": "additional_adult_tenant_added == true",
    "condition": "all(t >= 1 for t in per_tenant_continuous_occupancy_years) OR max(per_tenant_continuous_occupancy_years) >= 2",
    "note": "PROPOSED 2026-07-19, attorney-directed text (errata-cycle directive, Task 3): where an additional adult tenant has been added, just-cause attaches when EITHER all current tenants have resided 12 months, OR at least one tenant has resided 24 months. Source text not independently statute-verified by Cowork — flagged for Andy's confirmation at ratification (see Provenance note above)."
  }
}
```

**Proposed defect-gate update** (`notice.notice_defects[3]`, `missing_just_cause_reason` — the `ab1482_coverage_gate`), for Andy's ratification:

Add, ahead of the existing exemption checklist: *"Before applying this defect, first confirm just-cause protection has attached under `just_cause_attachment_threshold` (§1946.2(a), including the (a)(2) additional-adult-tenant variant). If not attached, this defect does not apply regardless of exemption status — see §1946.1(c) instead."*

**Day-count discipline check:** inputs are expressed in years (consistent with the existing `tenancy_under_1yr`/`tenancy_1yr_plus`/exemption fields, which are themselves derived from calendar-day counts); no new bare "days" language introduced.

### What this proposal does NOT do

- Does not touch `ca_eviction_v2.json`. Illustrative JSON only.
- Does not re-litigate the (e)(7)/(e)(8) determination — see `docs/WIRING_DETERMINATION_1946_2e_20260719.md` (separate, already ratified, no rule change).
- Does not encode anything for C-21/C-22 — those are ground-truth corrections (errata memo), not rule changes.

---

## Ratification checklist (Andy, item-by-item)

- [ ] `condition_general` (§1946.2(a), 12-month general threshold): RATIFY / REJECT / MODIFY
- [ ] Methodology confirmation: does the Stancil any-occupant convention apply to §1946.2(a) attachment (as proposed), or should it use a different measure?
- [ ] `condition_variant_a2` (§1946.2(a)(2), additional-adult-tenant variant): RATIFY the attorney-directed logic as encoded / MODIFY / confirm against verbatim statute text first
- [ ] Proposed `ab1482_coverage_gate` update to `missing_just_cause_reason`: RATIFY / REJECT / MODIFY

**On ratification:** per the directive's Task 4 (staged): Cowork cuts a new rules version (vProof1 immutable; new file, new SHA, changelog entry linking to this ratification), embeds the wiring determination (`docs/WIRING_DETERMINATION_1946_2e_20260719.md`) in that version's internal notes/metadata, and runs the Direction D-1 dev-set regression (v0.2 dev, 12 items — must be 12/12 with `newly_failing=0`, or revert-and-report RED). The v0.3 held-out set is NOT re-scored (permanently burned); a v0.4 set would be required for the next held-out measurement, drafted only on Andy's direction.

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
