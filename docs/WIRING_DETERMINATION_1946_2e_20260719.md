# Wiring Determination — §1946.2(e) exemptions and the `notice_period_too_short` defect

**Date:** 2026-07-19
**Determined by:** Andrew M. Cohen, Attorney of Record (per errata memo `docs/ERRATA_MEMO_v0_3_20260719.docx` §1, and Amended Task 2 of the errata-cycle Cowork Change Directive, 2026-07-19)
**Status:** Attorney-ratified negative determination. **Do not "fix."**
**Applies to:** `rules/eviction/california/ca_eviction_v2.json` (vProof1, `cc0cfab63ae1591e2b88…`) and all successor versions.

---

## Determination

The `ab1482_coverage_gate` attached to `notice.notice_defects[3]` (`missing_just_cause_reason`) is **intentionally NOT applied** to `notice.notice_defects[2]` (`notice_period_too_short`). This is correct as encoded and is not a wiring gap, coverage gap, or bug.

**Basis:** Civil Code §1946.2(e) exemptions (including (e)(7) new-construction and (e)(8) separately-alienable-SFH) remove the AB 1482 *just-cause* obligation of §1946.2 only. They do not shorten, displace, or excuse compliance with Civil Code §1946.1(b)/(c)'s notice-period requirements, which apply independently of AB 1482 coverage or exemption status. See *Stancil v. Superior Court* (2021) 11 Cal.5th 381 (60-day notice attaches once any occupant has resided one year or more, regardless of AB 1482 status).

A unit validly exempt from just cause under §1946.2(e)(7) or (e)(8) can still require a 60-day termination notice under §1946.1(b) if a tenant has resided one year or more — the two statutory schemes are independent and both must be satisfied.

## Origin and correction history

This determination resolves a question first raised by the v0.3 held-out miss autopsy (`docs/AUTOPSY_v0_3_MISSES_20260719.md`), which — working only from the score run and the rules file, without the benefit of this determination — could not itself rule out a wiring gap and flagged the question as open. Subsequent attorney review (same day) determined that CA-NOT-C-21 and CA-NOT-C-22's frozen ground truth, not the rules encoding, was the error: both items were 1+-year tenancies served 30-day notices, void under §1946.1(b)/Stancil regardless of their valid §1946.2(e) exemptions. See `docs/ERRATA_MEMO_v0_3_20260719.docx`, ERRATUM-2026-001 and -002, for the full correction.

## Taxonomy note

The autopsy's proposed error-taxonomy class, "exemption-scope-limited-to-single-defect," is **NOT ADOPTED for this instance** — the limitation it described turned out to be legally correct, not a gap. The class definition is retained in taxonomy notes (see autopsy addendum) as a candidate check for *future* autopsies, where the same pattern might, on a different provision, turn out to be a genuine gap rather than a correct limitation.

## Effective and durable

This determination is effective now and travels with `ca_eviction_v2.json` going forward:
- **Immediate:** recorded here as a companion doc (this file), referenced from `docs/PROJECT_STATE_OF_RECORD.md`. `ca_eviction_v2.json` itself is NOT edited — vProof1 remains byte-frozen at `cc0cfab63ae1591e2b88…` permanently, per standing project discipline.
- **✅ Embedded 2026-07-20:** the §1946.2(a) attachment-threshold rule was ratified and applied in `rules/eviction/california/ca_eviction_v3.json` — this determination is now embedded verbatim in that file's `provenance.determinations` array (id `WIRING-DETERMINATION-2026-07-19`), so it travels with the rules file itself going forward, not only in this companion doc.

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
