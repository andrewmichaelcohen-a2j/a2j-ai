# CJaC — Cowork Direction: Source-Grounded Self-Critique & Rule Revision (Stage 2 pre-encoding)

**From:** Andrew M. Cohen
**Date:** 2026-07-01
**Type:** Stage 2 direction — adds a pre-validation self-critique pass to the pipeline. Sits on top of the Playbook Architecture Directive; changes nothing in the 7-layer stack or golden-set discipline.
**Principle:** AI does the heavy lifting, with multi-layer protection. Human judgment (Andy + attorneys) is spent on the flagged residual — NOT on granular review of every rule. Cowork replicates the error-catching that has been happening in Claude Chat, at scale, by being directed to do the three things that make AI legal review reliable.

---

## 0. Why this direction exists

In Claude Chat, reviewing the CA-notice golden set surfaced systematic errors in the draft rules (wrong statutory subsections, incomplete multi-prong tests, missed residential/commercial distinctions). Those catches were reliable NOT because of a better model, but because the review did three specific things the initial drafting did not:

1. **Verified against LIVE primary sources** (actual statute text and case holdings retrieved), not training-memory synthesis.
2. **Adopted an ADVERSARIAL posture** — actively hunting for what is wrong, not confirming what looks right.
3. **Reconciled against the FROZEN golden-set corrections** as ground truth.

Cowork can and must do the same. This direction structures a self-critique pass so Cowork replicates all three. Making Andy or Claude Chat the manual reviewer of every rule defeats the thesis; the mechanism is Cowork with layered self-checks, humans adjudicating only the residual.

---

## 1. What this does NOT change

- The 7-layer validation stack (L1–L7), multi-model consensus, golden-set discipline, held-out isolation, honesty discipline, attorney-as-final-gate (L7). All intact.
- The frozen golden set (`goldenset_CA_notice_v0.1`) is IMMUTABLE ground truth. This pass reconciles rules TO it; it never edits the frozen items.
- Human sign-off remains the top gate. This pass changes WHAT humans review (the flagged residual) — not WHETHER they review.

---

## 2. The self-critique pass — three disciplines (mandatory)

For every CA-notice rule/element, Cowork runs a critique-and-revise pass governed by three hard rules:

**Discipline A — Live-source verification, not memory.**
Every rule's citation and condition must be checked against LIVE primary source text retrieved via the registry (ca_ccp_live, ca_civil_code_live, courtlistener_mcp). Do NOT confirm a rule from training knowledge. If the primary source cannot be retrieved for a given rule, that rule is FLAGGED (not confirmed, not revised) — retrieval failure is not verification.

**Discipline B — Adversarial posture.**
For each rule, the task is "find what is WRONG with this" — wrong subsection, incomplete test, missing exception, missed jurisdictional distinction, wrong notice type — not "confirm this looks right." Models over-confirm their own prior output; the adversarial framing counteracts this. Explicitly check each rule for the error CLASSES found in the golden-set review (see Section 4).

**Discipline C — Source-anchored changes only; flag the ungroundable.**
Any revision MUST cite the specific primary source (statute subsection or case holding) that supports the change. A change that cannot be grounded in a retrieved primary source is NOT made — it is FLAGGED for attorney review instead. "Revise generally" is permitted ONLY under this constraint: every change is source-anchored; ungroundable uncertainty is surfaced, never guessed.

---

## 3. Two-part scope

**Part 1 — Anchored reconciliation (do first).**
Reconcile every CA-notice rule against the frozen golden-set corrections in `goldenset_CA_notice_v0.1`. The frozen items (with their corrected authority and reasoning) are ground truth. Where a draft rule conflicts with a frozen correction, the rule is wrong — revise it to match, citing the frozen item + its primary source. This part is high-confidence because it is anchored to already-validated corrections.

**Part 2 — General source-verified review (do second).**
Extend the adversarial, source-grounded critique to the full CA-notice rule set beyond the golden-set items — catching errors the golden set did not happen to cover. Same three disciplines. This part is higher-value but higher-risk (unanchored), so Discipline C is strictly enforced: source-anchored changes only; everything ungroundable is flagged.

---

## 4. Known error classes to hunt (from the golden-set review — check every rule against these)

1. **Wrong statutory subsection** — e.g., the notice-period rule citing Civ. Code §1946.1(b) for BOTH 30-day and 60-day. Correct: (b) = 60-day / one-year-or-more; **(c) = 30-day / under-one-year**. Verify subsection-level citations against live statute text.
2. **Incomplete multi-prong tests** — e.g., the SFH AB 1482 exemption encoded as `not_owner_occupied`. Correct two-prong test: (a) owner is NOT a REIT/corporation/LLC-with-corporate-member, AND (b) the statutory written exemption notice under §1946.2(e)(8)(B) was given. Owner-occupancy is NOT the test. Every exemption/exception must encode ALL required prongs.
3. **Missed residential/commercial distinction** — e.g., partial-payment waiver: CCP §1161.1 is the COMMERCIAL statute and reaches the OPPOSITE result; the residential rule is common-law waiver (EDC Associates v. Gutierrez; CACI 4324) reinforced by overstatement. Do not apply §1161.1 to residential facts.
4. **Missing day-count mechanics** — e.g., the 3-day period is COURT days (CCP §1161 excludes weekends/holidays) with day-of-service excluded (CCP §12); premature filing before period expiry is defective (CA-NOT-11). Verify against current statute (note the 2/1/2025 court-day amendment).
5. **Wrong notice type / curable-vs-incurable** — e.g., waste is CCP §1161(4) unconditional quit, NOT §1161(3) cure-or-quit (CA-NOT-20). Verify notice-type rules encode the (3)/(4) distinction.
6. **Currency misses** — SB 567 (eff. 4/1/2024) relocation-assistance "strict compliance → void" for no-fault termination (CA-NOT-14). Verify AB 1482 rules reflect post-SB 567 law.

---

## 5. Also correct the PLAYBOOK_SPEC §9 draft elements

The draft `determinate` elements in PLAYBOOK_SPEC.md §9 currently repeat several of the above errors (notice-period cites (b) for both tiers; SFH exemption uses `not_owner_occupied`; partial-payment lacks the residential/commercial anchor). Re-derive these elements FROM the frozen golden-set corrections, not from the current drafts.

**Tagging correction — determinate core vs. open edge:** Re-examine every `open_textured` tag. Many elements have a DETERMINATE CORE with only a narrow OPEN EDGE. Example: `partial_payment_waiver` — the clean case (landlord accepts rent after notice, no reservation, proceeds) is DETERMINATE (waived, per EDC/CACI 4324/overstatement); only the ambiguous-characterization / express-reservation edge is open-textured. Encode these as a determinate rule WITH an open-textured exception path — do NOT cap the whole element at Tier B and forfeit scorable determinate answers. Wholesale `open_textured` should be reserved for elements whose CORE genuinely requires judgment (e.g., retaliatory motive).

---

## 6. Output format (confidence-tiered, for human review of the residual only)

Cowork produces a reconciliation report classifying every rule/element as:

- **REVISED (source-anchored):** changed to match a frozen correction or a retrieved primary source. Report: old → new, the primary-source cite, and the error class.
- **CONFIRMED (source-verified):** checked against live primary source and correct as-is. Report: the source verified against.
- **FLAGGED (attorney residual):** genuine uncertainty, ungroundable change, or contested interpretation. Report: the question and why it needs human judgment.

Andy / attorneys review ONLY the FLAGGED residual. REVISED items are logged with their source anchor (auditable, reversible, but not requiring pre-approval since each is source-anchored). This is the "AI does the volume; humans adjudicate the residual" division.

---

## 7. Fresh golden set — leakage guard

When drafting CA-notice golden set v0.2:
- The 16 frozen v0.1 items may serve as the DEVELOPMENT/non-held-out set (they informed the rules — fine).
- The fresh HELD-OUT set must be GENUINELY NEW fact patterns the revised rules were NOT written against. Reusing any v0.1 item (especially the 5 burned held-out items) as a held-out scoring item is leakage. "Fresh" = new held-out items, not a re-split of the 16.

---

## 8. Stage 2 gate (updated)

Encoding/scoring proceeds only when ALL hold:
1. Gemini credits restored (multi-model consensus operative).
2. **Self-critique pass complete** — CA-notice rules reconciled against frozen corrections (Part 1) and source-verified generally (Part 2); REVISED/CONFIRMED/FLAGGED report produced.
3. Andy has reviewed the FLAGGED residual and ratified strategy tags + any contested content.
4. Dual-model run yields `consensus_status == DUAL-MODEL-CONSENSUS`.
5. Fresh held-out set (genuinely new items) scored; held-out number reported with the scope note.

---

## 9. Documentation

- Log the self-critique pass and its REVISED/CONFIRMED/FLAGGED report in DAILY_CHANGELOG and as an artifact in the repo.
- Every REVISED item records its primary-source anchor and error class (auditable trail — same discipline as the golden-set correction notes).
- Update WORK_QUEUE: this pass is the NOW for Stage 2 pre-encoding.
- Preserve the reasoning: this pass is why human review is now scoped to the residual, not every rule.

---

*CJaC · Cowork Direction: Source-Grounded Self-Critique & Rule Revision · Copyright 2026 Andrew M Cohen · Apache 2.0.*
