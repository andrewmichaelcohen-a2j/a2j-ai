# CJaC — Cowork Direction: Broaden Proof 1 (CA-notice held-out set to n≈30)

**From:** Andrew M. Cohen  
**Date:** 2026-07-02  
**Type:** Stage-2 continuation. Sits on top of the Playbook Architecture Directive and the self-critique disciplines. Changes nothing in the 7-layer stack or held-out discipline.  
**Goal:** Turn the CA-notice held-out result from a directional n=5 signal into a statistically meaningful, citable held-out score (target n≈30) against a frozen rule version. This is the "demonstrated results" artifact — the number that supports adoption conversations.  
**Strategic choice:** Broaden Proof 1 (make the CA-notice proof robust) BEFORE Proof 2 (retaliation). A robust, reproducible number on a complete bright-line module does more for the mission than a second thin proof.

---

## 0. Hard gate — do this first, do NOT proceed until it passes

B3 regression check must pass before any broadening.

Run (Andy's terminal):
```
python3 rules/validation/scorer/ca_notice_scorer.py --golden rules/validation/scorer/FROZEN/goldenset_CA_notice_v0.2_20260701.xlsx --non-held-out-only
```

Required result: dev 12/12, newly_failing = 0 (confirms REVISED-8 §1161(2) days/hours and REVISED-9 subletting §1161(3) fixes landed with no regression). If newly_failing > 0 → STOP, fix source-anchored per Discipline C, re-run. Do not broaden on top of a regressed rule set.

**STATUS: ✅ GATE PASSED — 2026-07-02. 12/12 = 100.0% DUAL-MODEL-CONSENSUS (agree=12, disagree=0, errors=0). Confirmed three times. Rules SHA256: see vProof1 freeze record below.**

---

## 1. Freeze the rule version FIRST (integrity crux)

Once B3 passes, the CA-notice rule set is frozen for this scoring round:

- Snapshot the rules file; record its SHA256 as `ca_notice_rules_vProof1` (or equivalent version tag).
- No rule edits between now and the broadened score. The broadened held-out set is scored against THIS frozen rule version.
- This is what makes the number honest: the rules did not get to see the new held-out items, and they will not be tuned to pass them.

**The Goodhart trap to avoid:** do NOT draft new held-out items and then adjust rules to pass them. That inverts the entire discipline. New items test frozen rules; discovered gaps become development work for a FUTURE version with its OWN fresh held-out set — never a re-score of these items after tuning.

**STATUS: ✅ FROZEN — 2026-07-02.**
- File: `rules/eviction/california/ca_eviction_v2.json`
- SHA256 (`ca_notice_rules_vProof1`): see VALIDATION_METRICS_LEDGER.md — vProof1 freeze record
- Frozen state: post REVISED-8 (§1161(2) days_hours) + REVISED-9 (subletting §1161(3)→curable); 9 self-critique revisions from 2026-07-01
- **No rule edits permitted until after the broadened held-out score is complete and logged.**

---

## 2. Draft the broadened held-out set (~25–30 genuinely new items)

Cowork drafts candidate fact patterns; Andy freezes (attorney judgment sets ground truth). Same division as v0.1/v0.2.

**Independence discipline (mandatory — this is what makes the number credible):**

- Items must be genuinely new fact patterns the rule-writing never saw — NOT paraphrases or duration-swaps of v0.1/v0.2 items (recall CA-NOT-B-04 was dropped for exactly this).
- Source them independently of the rule-writing pass:
  - CA Judicial Council UD Benchguide (BG31) hypotheticals and fact patterns (per the extract already in the registry) — cross-check any post-2015 rule against current statute per Discipline A, since BG31 is 2015.
  - Anonymized real-world legal-aid fact patterns where available.
  - Boundary / edge cases the existing 17 items do not cover — e.g., exact-threshold tenancy durations (11 vs. 12 vs. 13 months), notice served on the boundary court-day, partial-payment amounts at edges, multiple-defect notices (does the rule catch the controlling defect when two are present?), and valid-notice cases (the rule must not over-flag).
- Coverage balance: span NOTICE_VALID and NOTICE_INVALID (and UD_DEFECTIVE_PREMATURE / UD_NOT_SUSTAINABLE where apt) so the set tests discrimination, not just defect-detection. Report the coverage distribution (B1).

**Target size:** ~25–30 frozen held-out items. n≈30 is the reliability threshold; below it the score is directional only. If attorney-freeze time forces a smaller set, report the actual n and its confidence interval honestly — do not present a small-n rate as a precision figure.

**STATUS: ✅ DRAFT COMPLETE — 2026-07-02. 28 candidates drafted.**
- File: `rules/validation/scorer/FROZEN/goldenset_CA_notice_v0.3_DRAFT_20260702.xlsx`
- All items Status=DRAFT. Andy reviews, corrects, and sets Status=FROZEN for each item.

---

## 3. Freeze, then score ONCE

1. Andy reviews Cowork's drafts, corrects, and freezes each item (Status=FROZEN, correct outcome, reviewer, date). Immutable ground truth.
2. Lock the file; record its SHA256.
3. Score once, dual-model, against the frozen rule version (§1). Require `consensus_status == DUAL-MODEL-CONSENSUS` (Gemini is working again as of 2026-07-02; if it lapses, PRELIMINARY only, never cited).
4. This is a one-shot: the held-out set is scored once and burned. Do not re-score these items after any rule change.

**Note on the existing 17-item v0.2 set:** those items (dev + already-burned held-out) remain the development set. They are NOT reused as held-out here. This is an entirely fresh held-out set.

---

## 4. Report (apply all four measurement directives)

- **Held-out rate WITH its 95% confidence interval** — the headline, reported with the CI so the precision is honest (e.g., "28/30 = 93.3%, 95% CI [x, y]"). Never report the rate without n and CI.
- **B1 coverage:** known/unknown element coverage; accuracy paired with coverage; the VALID/INVALID distribution of the set.
- **B2 confident-wrong:** classified separately, higher severity. Target zero. Any confident-wrong is the priority finding.
- **B3 regression:** confirm the frozen rules still pass the v0.2 development set (no regression introduced by anything since).
- **B4 currency:** each item's authority checked for post-encoding amendments (esp. SB 611 2/1/2025, SB 567 4/1/2024 — and note BG31 is 2015).
- **Krippendorff's α** for model agreement, with the small-n caveat if applicable.
- **Reporting scope note:** state-law bright-line CA notice only; overlays and open-textured modules separate.

---

## 5. Expectation-setting (important — do not optimize for a perfect score)

Expect to learn, not to confirm. A larger, more independent held-out set is LIKELY to surface a gap or two the current rules miss — that is the set doing its job, exactly as the dev set found B-02 and B-09. A 27/30 or 28/30 with two honestly-reported misses is a MORE credible artifact than a suspicious 30/30, because it shows the test is real and the discipline intact. Do NOT tune rules to chase 30/30 (that would burn the set's integrity). Report the honest number, whatever it is; discovered gaps route to the next development cycle.

---

## 6. What this unlocks

A robust CA-notice held-out number (n≈30, dual-model, with CI) is the "demonstrated results" artifact — the point at which the collateral can move from "process credibility, first module" to "validated accuracy rate on a complete bright-line module, reproducibly." It also sets the template for every future module: freeze rules → large independent held-out set → score once → report with CI. Proof 2 (retaliation / bounded-reasoning) follows after this lands.

---

## 7. Sequence summary

1. ✅ B3 regression check passes (Andy terminal) — GATE.
2. ✅ Freeze the CA-notice rule version; record hash.
3. ✅ Cowork drafts ~25–30 independent, edge-case-rich held-out candidates (benchguide + real patterns + boundaries).
4. 🔲 Andy freezes the set.
5. 🔲 Score once, dual-model, against frozen rules.
6. 🔲 Report held-out rate + CI + B1–B4 + α + scope note.
7. 🔲 If clean and robust → update collateral to "demonstrated results"; then plan Proof 2.

**Do not:** edit rules after the freeze; reuse v0.2 items as held-out; tune to pass new items; report a rate without n and CI.

---

*CJaC · Cowork Direction: Broaden Proof 1 · Copyright 2026 Andrew M Cohen · Apache 2.0.*
