# v0.3 Held-Out Miss Autopsy — CA-NOT-C-18, C-21, C-22

**Date:** 2026-07-19
**Trigger:** Cowork Change Directive "v0.3 Held-Out Score Ingestion & AB 1482 Rule-Gap Cycle," approved by Andrew M. Cohen, 2026-07-19, Task 2.
**Scope:** Miss autopsy only. Task 3 (candidate rule drafting) was **NOT executed** — see Conclusion.

---

## Hypothesis under test

The directive's working hypothesis: the pipeline recognizes when AB 1482 protections *condemn* a notice (C-19, C-20 scored correctly) but not when a threshold or exemption *saves* one — because the relevant rules (§1946.2(a) attachment threshold, §1946.2(e)(7), §1946.2(e)(8)) are absent from `ca_eviction_v2.json` at vProof1, causing the models to default to the protective (void) answer with nothing to retrieve.

## Method

1. Inspected `rules/eviction/california/ca_eviction_v2.json` (SHA256 `cc0cfab63ae1591e2b88…`, confirmed identical to the vProof1 freeze — the exact file used for this scoring run) directly, structurally, for each of the three provisions.
2. Pulled each item's `gpt_controlling_rule` / `gemini_controlling_rule` and full reasoning text from `rules/validation/scorer/output/ca_notice_score_2026-07-19_held-out.json` to see which defect the models actually fired on.
3. Cross-referenced the two.

## Findings — per-provision present/absent

| Provision | Status in vProof1 | Detail |
|---|---|---|
| **§1946.2(a) 12-month/24-month just-cause attachment threshold** | **ABSENT** | `notice.notice_types.termination.just_cause_required` is a flat boolean (`true`), with no duration-based gating condition anywhere in the file. No occupancy-length input feeds into whether just-cause protection has "attached" yet. Confirmed by full-file search: zero hits for any 12-month/24-month attachment-duration logic outside one unrelated `substantive_defenses` presumption-period field (a different module entirely). |
| **§1946.2(e)(7) new-construction/15-year C-of-O exemption** | **PRESENT, fully encoded** | `termination.exemptions[3]`: `exemption_id: new_construction_15yr`, statute `§1946.2(e)(7)`, condition `certificate_of_occupancy_date_within_15_years_of_notice_date`, with an explicit note that the 15-year window is rolling (measured from notice date). Ratified by Andy 2026-07-01. |
| **§1946.2(e)(8) separately-alienable SFH/condo exemption** | **PRESENT, fully encoded** | `termination.exemptions[0]`: `exemption_id: sfh_non_entity_owner`, two-prong test per `(e)(8)(A)` (owner not REIT/corp/LLC-with-corporate-member) and `(e)(8)(B)` (written exemption notice given), explicitly distinguished from the separate `(e)(5)` owner-occupied exemption. Ratified by Andy 2026-07-01. |

## Findings — per-item classification

**CA-NOT-C-18** — both models fired `notice_defects[missing_just_cause_reason]`. This defect *does* carry an `ab1482_coverage_gate` listing all eight `(e)` exemptions — but the gate only checks whether an `(e)` exemption applies, not whether just-cause protection has *attached* yet under `(a)`. Since `just_cause_required` is unconditionally `true`, there is no encoded path by which a short (<12-month) tenancy could avoid the defect. **Missing-rule hypothesis CONFIRMED for this item** — this is a genuine coverage gap.

**CA-NOT-C-21 and CA-NOT-C-22** — both models fired `notice_defects[notice_period_too_short]` (the §1946.1(b)/Stancil 60-day rule for 1+-year tenancies), **not** `missing_just_cause_reason`. The `ab1482_coverage_gate` — which correctly encodes both `(e)(7)` and `(e)(8)` — is attached to `notice_defects[3]` (`missing_just_cause_reason`) **only**. It is not present on `notice_defects[2]` (`notice_period_too_short`), nor on any other defect in the file (checked all 7). The exemption rules the model needed exist, correctly encoded, ratified — they simply are not wired to the defect that actually fired. **Missing-rule hypothesis DISCONFIRMED for these two items.**

## Error taxonomy

C-21/C-22 don't fit the existing "missing rule" class cleanly. Proposing a new class (YELLOW, for Andy's consideration, not yet adopted): **exemption-scope-limited-to-single-defect** — an exemption is correctly encoded and reachable from one defect's evaluation path but not cross-wired to sibling defects it may also legally bear on. Distinct from a pure coverage gap (rule absent) and from a retrieval failure (rule present, reachable, but the model didn't find/use it) — here the rule is present but structurally unreachable from the defect that needed it.

One open substantive question this autopsy cannot resolve: whether `(e)(7)`/`(e)(8)` exemption from AB 1482 just-cause *also* exempts a unit from the general (non-AB-1482) §1946.1(b)/Stancil 60-day notice-period requirement, or whether Andy's C-21/C-22 ground truth rests on some other fact not captured in the encoded inputs. That is a legal-substance question, not an engineering one.

## Conclusion — STOP, escalate as RED, Task 3 not executed

Per the directive's own instruction: *"If the missing-rule hypothesis is DISCONFIRMED (rules exist but misfired), STOP the cycle at this point and queue the autopsy for Andy as RED — a retrieval/application failure is a different and more serious problem than a coverage gap."*

Two of the three misses (C-21, C-22) show exactly that pattern — and the open question above (whether the exemption *should* reach the notice-period defect at all) is a legal determination, not something Cowork should resolve unilaterally by drafting rule text. Task 3 (candidate rule proposals) was therefore **not executed** this cycle. `ca_eviction_v2.json` remains untouched at vProof1.

**Recommended next step (Andy's call, not actioned):** a decision on whether `(e)(7)`/`(e)(8)` should gate `notice_period_too_short` (and possibly other defects) the same way they gate `missing_just_cause_reason` — and separately, whether/how to encode the `(a)` 12-month attachment threshold for C-18. Once Andy resolves the legal question, Task 3-style rule drafting can proceed against a correct target rather than a guess.

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
