# DEBT-DEMO-V1.0 CENSUS AUDIT — TEXAS

*Generated 2026-09-05 from the frozen v1.0 files, `stage_b_dispositions.json`, and `run_20260904T221748Z.json`. Phase LOCK item 4. Copyright 2026 Andrew M Cohen. Apache 2.0.*

Read order is the order below. Each sheet: A logic (full text), B checklist, C citations with tier and verification status, D disposition history, E sign-off. Nothing here edits v1.0; findings go to `POST_V1_BACKLOG.md`.

---

## 1. TX-SOL-CONSUMER-DEBT

**Title:** Statute of limitations on a Texas consumer-debt collection lawsuit  
**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `d5a03cc512034f60be8408070306fa25b7a5fef07dc255ecb649bc237cadb381`

**Reading load:** logic 925 words · checklist 318 · cited text 1,245 · 6 citations · 9 checklist items · 3 drafting revisions

### A. Logic (read in full; this is the content being certified)

**limitations_period_years**

4

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**applies_to**

actions on debt (written or oral contract), consistent with credit-card and other consumer-debt collection suits

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**accrual**

the day the cause of action accrues -- for a revolving account, generally the date of DEFAULT or ACCELERATION (the creditor's demand for the full balance / charge-off), NOT the date of the last payment. CORRECTED 2026-09-05 (round 46), from run_20260904T221748Z.json: the prior text and checklist treated 'last payment' and 'default/breach' as interchangeable. On a credit card the last payment (March 2021) can precede the default that starts limitations (the November 2021 charge-off and demand) by six months to a year; using the last-payment date makes the July 2025 suit look barred when it is timely -- a dangerous-direction error. Texas courts have fixed accrual on revolving accounts at the date the account was charged off / the balance accelerated, or, on some facts, at the first missed payment (GLOSS-FOR-COUNSEL: the accrual date on a revolving account is not settled in a single controlling case; collect all three dates -- last payment, first missed payment, charge-off/demand -- and compute from each).

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**note_re_tolling**

Discovery-rule and fraudulent-concealment tolling, plus minority/unsound-mind/military-service/absence-from-Texas tolling, are recognized under Texas law but NOT encoded here — this node determines the baseline 4-year period only; tolling analysis is a separate, not-yet-built node.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**determination**

expired_if (the date suit was FILED -- or today, only if no suit has been filed) > (accrual_date + 4 years), subject to any tolling not yet encoded. CORRECTED 2026-09-05 (round 46), from run_20260904T221748Z.json, DANGEROUS DIRECTION: the prior formula compared TODAY to accrual + 4 years. Texas limitations is measured to the date the plaintiff FILED suit (CPRC 16.004(a): 'must bring suit ... not later than four years after the day the cause of action accrues'), provided the plaintiff then exercised diligence in obtaining service; a consumer who consults after the four-year mark about a suit the debt buyer filed within it was being told the claim was 'expired' when it is timely. Ask for the file-stamp date on the petition, not the service date and not today. GLOSS-FOR-COUNSEL: the diligence-in-service rule (filing alone does not stop the clock if service is delayed without diligence).

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**post_expiration_payment_note**

ADDED 2026-09-03 (round 38): the accrual definition ('date of default/breach or last payment') must not be applied to a payment made AFTER the 4-year period ran. Under Tex. Civ. Prac. & Rem. Code § 16.065, revival of a barred claim requires a signed WRITTEN acknowledgment, and, where the holder is a DEBT BUYER (Fin. Code 392.307(a)(2)), § 392.307(d) provides that a payment, reaffirmation, or any other activity on a time-barred consumer debt does not revive it (and (c) bars the debt buyer from suing at all). CORRECTED 2026-09-04 (round 39): 392.307 is a debt-buyer provision, not a rule for every creditor; the general rule is 16.065. Debt buyers routinely solicit small 'good faith' payments precisely to manufacture a restart argument; as previously encoded, a 2024 $25 payment on a 2016 default would report a 2025 suit as timely -- the dangerous direction. Appeared in both backlog runs.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**installment_separate_accrual_note**

ADDED 2026-09-03 (round 38): for an installment obligation (auto loan, personal installment loan) that the lender has NOT accelerated, Texas runs limitations separately on each missed installment; installments falling due within the last 4 years remain actionable even if earlier ones are barred (and on optional-acceleration notes, accrual on the full balance runs from actual acceleration). The single-accrual-date, binary output would report the whole claim expired. Case-law gloss, source_tier C; same doctrine noted on the CA nodes.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**judgment_already_entered_note**

ADDED 2026-09-03 (round 38): if a JUDGMENT has already been entered (very often by default, sometimes without the consumer's knowledge), the 4-year contract period is no longer the question -- the claim merged into a judgment on which execution may issue for 10 years, kept alive by issuing a further writ within each 10-year period; if no writ issues the judgment becomes DORMANT and may be revived only within 2 years of dormancy (Tex. Civ. Prac. & Rem. Code §§ 34.001, 31.006 -- CORRECTED 2026-09-04, round 39: not 'renewable indefinitely' as round 38 said). A consumer garnished in 2025 on a 2018 default judgment should not be told the debt 'expired in 2019.' ADDED 2026-09-05 (round 46): for an OUT-OF-STATE judgment being enforced in Texas, CPRC 16.066 (quoted above) bars the action here if it is barred where rendered, and bars any action on a foreign judgment more than 10 years old against a defendant who has lived in Texas for 10 years.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**sol_is_an_affirmative_defense_note**

ADDED 2026-09-03 (round 38): limitations is an affirmative defense that is waived unless pleaded (Tex. R. Civ. P. 94); Texas courts routinely enter default judgments on time-barred consumer debts against non-answering defendants. An 'expired' output must always carry 'you must file an answer and plead it' -- the most common posture for this node is a pro se defendant deciding whether to respond.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**choice_of_law_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json; GLOSS-FOR-COUNSEL. Nearly every consumer card agreement chooses another state's law (Delaware, Utah, South Dakota), some with a 3-year limitations period. Texas has NO general borrowing statute for contract claims (the Stage B finding's citation to CPRC 16.066 was wrong -- that section covers foreign judgments only). Texas courts traditionally treat limitations as PROCEDURAL and apply the forum's (Texas's) four years regardless of a substantive choice-of-law clause; some courts have applied the chosen state's shorter period where the clause expressly reaches limitations, and debt-defense practice routinely raises the argument. The safe encoding is: default to Texas's four years, flag the clause, and refer. Checklist item added.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. THRESHOLD: has a suit been FILED? If so, the file-stamp date on the petition (not the service date, not today) is what is compared to accrual + 4 years; a suit filed inside the period is timely no matter when the consumer consults  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. Three dates, kept separate: date of LAST PAYMENT, date of the FIRST MISSED payment, and date of CHARGE-OFF / demand for the full balance (acceleration) -- accrual on a revolving account is generally the default/acceleration date, not the last-payment date  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. Whether the debt arose from a written or oral contract (both get the 4-year period under § 16.004, but confirms which subsection applies)  (non-dispositive)  [ ] keep  [ ] change  [ ] drop
4. Any facts suggesting tolling (fraudulent concealment, debtor's absence from Texas, debtor's minority or unsound mind, military service) — flagged for the not-yet-built tolling node, not resolved here  (dispositive)  [ ] keep  [ ] change  [ ] drop
5. If the consumer made any payment after default: was it BEFORE or AFTER the 4-year period had run? A post-expiration payment does not revive the claim (CPRC 16.065 requires a signed writing; Fin. Code 392.307)  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. Whether the obligation was an installment loan and, if so, whether the lender ever accelerated -- unaccelerated installments accrue separately and may be only partially barred  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. Whether a JUDGMENT has already been entered on this debt -- if so, the 10-year, renewable judgment-enforcement period (CPRC 34.001/31.006) governs, not this 4-year contract period  (dispositive)  [ ] keep  [ ] change  [ ] drop
8. Whether a suit has been filed and the consumer has answered and pleaded limitations -- an expired period does not prevent a default judgment if the defense is not raised (TRCP 94)  (dispositive)  [ ] keep  [ ] change  [ ] drop
9. Does the card agreement contain a CHOICE-OF-LAW clause (Delaware, Utah, South Dakota, etc.), and does it expressly extend to limitations? Texas generally applies its own four years, but the clause is a live argument either way -- refer (choice_of_law_note)  (non-dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | Tex. Civ. Prac. & Rem. Code § 16.004(a) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/CP/htm/CP.16.htm |
| 2 | Tex. Civ. Prac. & Rem. Code § 16.065 | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/CP/htm/CP.16.htm |
| 3 | Tex. Fin. Code § 392.307(c)-(d) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/FI/htm/FI.392.htm |
| 4 | Tex. Civ. Prac. & Rem. Code § 34.001(a)-(b); § 31.006 | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/CP/htm/CP.34.htm |
| 5 | Tex. R. Civ. P. 94 | A | LIVE-VERIFIED (run_20260904T221748Z) | https://rulesofcivilprocedure.com/tx/rule-94/ |
| 6 | Tex. Civ. Prac. & Rem. Code § 16.066(a)-(b) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/CP/htm/CP.16.htm |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | yes | "Expired" does not stop a default judgment; SOL must be pleaded | Note + checklist on all three (CCP 458 / TRCP 94) |
| 02 | FIXED-VERIFIED | yes | Post-expiration payment (16.065 / Fin. Code 392.307) | Note + checklist |
| 03 | GLOSS-FOR-COUNSEL | partial | Installment separate accrual | Note + checklist |
| 04 | FIXED-VERIFIED | yes | Judgment already entered -> 10-yr renewable (34.001/31.006) | Note + checklist |
| 05 | FIXED-VERIFIED (against 16.004(a) already pinned) + GLOSS (diligence in service) | yes | Determination compared TODAY, not the filing date | determination corrected; threshold checklist |
| 06 | GLOSS-FOR-COUNSEL; 16.066(a)-(b) pinned for foreign judgments | varies | Choice-of-law clause / borrowing statute unscreened (finding's 16.066 cite wrong) | choice_of_law_note; checklist; judgment note extended |
| 07 | FIXED (corrected) + GLOSS (revolving-account accrual date) | yes | Accrual conflated last payment with default/acceleration | accrual corrected; checklist item rewritten |

**Drafting revisions (author / date / summary):**

- 2026-09-03 — Added post-expiration-payment, installment accrual, judgment-already-entered, and affirmative-defense notes + 4 checklist questions. All backlog findings (both runs) addressed; CPRC 16.065, Fin. Code 392.307, CPRC 34.001, TRCP 94 text NOT pinned this session -- SOURCE PENDING.
- 2026-09-04 — Pinned CPRC 16.065, Fin. Code 392.307(c)-(d), CPRC 34.001/31.006, TRCP 94. Two corrections: 392.307 is debt-buyer-specific; judgments go dormant without a writ within 10 years (revivable within 2 years), not 'renewable indefinitely'.
- 2026-09-05 — Round 46: determination corrected to filing date; accrual corrected to default/acceleration with all three dates collected; choice_of_law_note (GLOSS); 16.066(a)-(b) pinned for the foreign-judgment case; three checklist changes.

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed True · material findings 3 (all dispositioned in round 46; see D)

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---

## 2. TX-JUSTICE-COURT-DEBT-ANSWER-DEADLINE

**Title:** Deadline to answer a Texas debt-collection lawsuit in justice court  
**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `25d0999d192a9131c5c8ddc99d9f4b80f3f2cd55665555e85680c7951d7ac6a8`

**Reading load:** logic 778 words · checklist 250 · cited text 518 · 4 citations · 5 checklist items · 3 drafting revisions

### A. Logic (read in full; this is the content being certified)

**answer_deadline_days**

14

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**deadline_computed_from**

date of service (delivery by constable or process server)

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**weekend_holiday_rule**

extends to the next business day if the 14th day falls on a weekend or court holiday

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**jurisdictional_ceiling**

20000

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**note_re_sourcing**

This node's fact figures (14 days, $20,000 ceiling) are corroborated by a reputable attorney-reviewed legal-aid source (TexasLawHelp/TLSC), NOT yet independently verified against the primary Texas Rules of Civil Procedure text itself. Per spec §3(a), grounded corroboration requires derivation from primary source text; this node does not yet meet that bar and should be treated as lower-confidence than the other TX nodes in this file until the primary TRCP 502.5 text is independently pulled and cited verbatim.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**which_court_is_dispositive_note**

ADDED 2026-09-03 (round 38): the checklist used 'amount claimed <= $20,000' as a proxy for justice-court jurisdiction, but county courts at law and district courts have CONCURRENT jurisdiction over small debt claims and debt buyers routinely file there, especially in urban counties. In those courts the answer deadline is Tex. R. Civ. P. 99(b) -- 10:00 a.m. on the Monday next after the expiration of 20 days from service -- not 14 days. The dispositive fact is WHICH COURT is named on the citation, not the dollar amount. A county-court defendant on day 16 told 'your deadline passed' may abandon a timely defense. Appeared in both backlog runs.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**late_answer_before_default_note**

ADDED 2026-09-03 (round 38): the 14-day date is not a hard cutoff for a defendant who has already missed it. In Texas practice a default judgment cannot be entered while an answer is on file, so a LATE answer filed at any time before the court signs a default judgment is effective and defeats the default. For the very common 'I already missed it' caller, the single most consequential instruction is: file an answer immediately, today. This node previously presented the deadline as the end of the road. [SOURCE PENDING: named but not live-fetched this session; screening flag, not a verified quotation.]

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**after_default_signed_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: if a default judgment HAS been signed in the justice court, the answer deadline is behind the defendant but two short, deterministic windows are not: (1) a motion to set aside / motion for new trial within 14 DAYS after the judgment is signed (TRCP 505.3(b)-(e); Craddock factors -- see TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY), and (2) an APPEAL to county court for trial de novo within 21 DAYS after the judgment is signed, or after the 505.3 motion is denied (TRCP 506.1(a)), perfected by a bond (twice the judgment for a defendant), a cash deposit, or a sworn statement of inability to pay -- and the appeal requires NO excuse for the default; the county court simply tries the case anew. For a consumer who learns of the judgment through a bank freeze three weeks after signing, the 21-day appeal is usually the live door when the 14-day motion has closed. After 21 days both are gone and the remaining routes are equitable (bill of review) -- refer. Checklist item 3 rewritten.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**venue_challenge_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: a debt-claim defendant is entitled to be sued in the county AND PRECINCT where he resides (or where the contract was to be performed, etc. -- TRCP 502.4(b)). A debt buyer that files across the county, or in a neighboring county, is in an improper venue. The remedy is a sworn MOTION TO TRANSFER VENUE naming the proper county and precinct, due 'before trial, no later than 21 days after the day the defendant's answer is filed' (502.4(d)). Filing an answer first does NOT waive venue (the Stage B finding to the contrary was checked against the rule text and is wrong); missing the 21-day post-answer window does. Practical sequence for a wrong-precinct defendant: answer by the 14-day deadline, and file the venue motion with it or within 21 days after.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**eviction_case_type_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json, DANGEROUS DIRECTION: this node's 14-day written-answer rule is for SMALL CLAIMS and DEBT CLAIM cases (TRCP 500.3(a)-(b)). An EVICTION (forcible detainer) petition -- even one that also seeks back rent -- is filed in the same justice court but governed by TRCP 510: no written answer is required, trial is set 10-21 days after the petition is filed, and the dispositive obligation is to APPEAR at the trial setting; a tenant who treats the papers as a debt claim and plans to 'answer within 14 days' can lose possession by default at a trial held before that. Eviction defaults, appeals (5 days) and the rest are on the TX-DEFAULT-JUDGMENT node's eviction_carve_out_note and its pinned 510.8(e)/510.9(a). This node's threshold checklist now asks the CASE TYPE before anything else; the eviction line's own nodes (vProof1) govern the substance.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. THRESHOLD: what KIND of justice-court case is it -- a debt claim / small claim (this node: written answer within 14 days) or an EVICTION (forcible detainer, TRCP 510: no written answer, appear at the trial setting 10-21 days out, even if back rent is also claimed)? Read the caption and the citation's first lines  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. Date of service (date the constable or process server delivered the citation and petition)  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. WHICH COURT the citation names -- a justice (JP) court (14-day rule, this node) versus a county court at law or district court (TRCP 99: Monday next after 20 days from service). The dollar amount is NOT a reliable proxy; concurrent jurisdiction means sub-$20,000 suits are routinely filed in county court  (dispositive)  [ ] keep  [ ] change  [ ] drop
4. If the deadline has ALREADY passed: has a default judgment been SIGNED? If NOT, answer immediately (late_answer_before_default_note). If YES: the date it was signed -- a motion to set aside is due within 14 days (TRCP 505.3) and an appeal to county court for a fresh trial, needing no excuse, within 21 days of the judgment or of the motion's denial (TRCP 506.1(a)); after 21 days, refer  (dispositive)  [ ] keep  [ ] change  [ ] drop
5. Is the suit filed in the county AND precinct where the defendant lives (or another proper venue under TRCP 502.4(b))? If not, a sworn motion to transfer venue is due no later than 21 days after the answer is filed (502.4(d)) -- answering first does not waive it  (dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | Tex. R. Civ. P. 502.5 | D | LIVE-VERIFIED (run_20260904T221748Z) | https://texaslawhelp.org/guide/how-to-answer-a-debt-collection-case-in-justice-court |
| 2 | Tex. R. Civ. P. 99(b) | B | LIVE-VERIFIED (run_20260904T221748Z) | https://rulesofcivilprocedure.com/tx/rule-99/ |
| 3 | Tex. R. Civ. P. 506.1(a) | B | ADDED AFTER last run (round 46) -- not yet live-checked | https://www.stcl.edu/lib/TexasRulesProject/TRCP474-522/rule506-12013.html |
| 4 | Tex. R. Civ. P. 502.4(d) (first sentence) | B | ADDED AFTER last run (round 46) -- not yet live-checked | https://www.stcl.edu/lib/TexasRulesProject/TRCP474-522/rule502-42013.html |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | yes | Dollar amount used as proxy for court; county/district = TRCP 99 | Checklist item replaced |
| 02 | FIXED-SOURCE-NAMED | yes | Late answer before default signed still works | Note + checklist |
| 03 | FIXED-VERIFIED | yes | No branch for a default already signed (505.3 / 506.1) | 506.1(a) pinned; after_default_signed_note; checklist rewritten |
| 04 | NOT-A-GAP as stated (rule encoded correctly) | n/a | Venue motion 'must precede the answer' (checked: 21 days AFTER, TRCP 502.4(d)) | 502.4(d) pinned; venue_challenge_note; checklist |
| 05 | FIXED-VERIFIED (510 pinned on sibling) | yes | Eviction case type not screened (TRCP 510) | eviction_case_type_note; threshold checklist |

**Drafting revisions (author / date / summary):**

- 2026-09-03 — Replaced the dollar-amount proxy with a which-court checklist question (TRCP 99 vs. 502.5); added late-answer-before-default note + question. Both backlog findings (both runs) addressed; TRCP 99 text NOT pinned this session -- SOURCE PENDING.
- 2026-09-04 — Pinned TRCP 99(b) (county/district-court answer deadline). Late-answer-before-default remains a practice note (no single rule text quoted); marker retained.
- 2026-09-05 — Round 46: TRCP 506.1(a) pinned + after_default_signed_note + checklist item rewritten; 502.4(d) pinned + venue_challenge_note + checklist (finding NOT-A-GAP as stated, rule encoded correctly); eviction_case_type_note + threshold checklist.

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed True · material findings 3 (all dispositioned in round 46; see D)

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---

## 3. TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY

**Title:** Whether a Texas default judgment will be set aside on a motion for new trial — a genuinely discretionary, multi-factor judicial determination  
**File:** `rules/debt/state/texas/tx_debt_band3_discretionary_v1.json`  
**Band / tier at freeze:** 3 / DRAFT  
**node_sha256 (v1.0):** `e8cb7e983fba809ca75d73ea52a7c3cf7f8d77e7d3639affd65279965d9cf3c0`

**Reading load:** logic 1,574 words · checklist 405 · cited text 1,654 · 9 citations · 10 checklist items · 5 drafting revisions

### A. Logic (read in full; this is the content being certified)

**concept**

BAND 3 -- GENUINELY DISCRETIONARY. This node's only honest output is the boundary marker itself: flagging that a default judgment may be set aside, naming the three factors a Texas court weighs, and stating who bears the burden -- never predicting whether a specific court will actually grant the motion. Predicting the outcome of a discretionary judicial determination is out of scope for this system by design (see spec Band taxonomy, docs/GLOSSARY.md) -- this is a permanent boundary, not a gap to close with more data.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**trigger**

A default judgment (or a judgment following an answer with a subsequent failure to appear, per Ivy v. Carrell, 407 S.W.2d 212 (Tex. 1966), extending Craddock) has already been entered against the person, and the person wants to know whether it can be reopened.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**craddock_factors_named_not_applied**

- (1) the failure to answer was not intentional or the result of conscious indifference, but the result of an accident or mistake
- (2) the motion for new trial sets up a meritorious defense
- (3) granting the motion will occasion no undue delay or otherwise injure the plaintiff

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**procedural_deadline_component_this_IS_deterministic**

The motion for new trial must be filed within 30 days after the judgment is signed (TRCP 329b(a)) -- Band 1 within an otherwise Band 3 node. If it is not decided by written signed order within 75 days of judgment, it is overruled by operation of law (TRCP 329b(c)). Missing the 30-day window forecloses this path entirely regardless of how strong the three Craddock factors are -- this deterministic gate should be surfaced to the user with urgency distinct from the discretionary merits question.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**what_the_system_may_say**

Name the three-factor test, explain each factor in plain language, flag the 30-day filing deadline as hard and case-critical, and tell the person a licensed attorney's judgment is needed to assess factors (1) and (2) against their specific facts. Also: identify which court entered the judgment (district/county vs. justice court) since the filing deadline differs; flag whether the TRCP 306a notice-restart may apply if the person says they only recently learned of the judgment; and flag whether service is disputed at all, since that changes which remedy (Craddock motion vs. restricted appeal vs. bill of review) is even the right one to pursue -- these are the same kind of deterministic, non-discretionary gates as the existing 30-day filing deadline, not predictions of a discretionary outcome.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**what_the_system_may_NOT_say**

Any prediction of whether a specific court will grant or deny the motion; any characterization of the person's facts as clearly meeting or failing a factor; any percentage or likelihood language.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**justice_court_variant_note**

The 30-day/75-day TRCP 329b deadlines above apply in DISTRICT OR COUNTY COURT. If the default judgment was entered in JUSTICE COURT (small-claims-tier, common for consumer debt-buyer suits), the governing deadline is instead TRCP 505.3: 14 days to file a motion to set aside/for new trial, denied by operation of law at 5:00 p.m. on the 21st day if not ruled on. Which court entered the judgment is a threshold, deterministic fact this node must ask before applying either deadline -- like the 30-day TRCP 329b deadline itself, this is Band 1 within an otherwise Band 3 node, not a matter of discretion. EXPANDED 2026-09-05 (round 46), from run_20260904T221748Z.json: the 14-day 505.3 motion is not the only justice-court door, and it is the harder one (Craddock factors apply). TRCP 506.1(a) gives 21 DAYS from the signing of the judgment -- or from denial of the 505.3 motion -- to APPEAL to county court for trial de novo by filing a bond (a defendant's is twice the judgment), a cash deposit, or a sworn statement of inability to pay (contestable, 506.1(d)); no excuse for the default need be shown, and 506.1(f) bars a county-court default until compliance is checked. For the consumer who learns of a Harris County JP default on day 18, the answer is 'the motion window closed on day 14; the appeal window runs to day 21 -- file the statement of inability today.' This is deterministic and belongs on the checklist, not in the discretionary part of this node.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**notice_restart_note**

The filing deadline (30 days under 329b, or 14 days under 505.3) is NOT an absolute bar if the party did not receive notice of the judgment or acquire actual knowledge of it within 20 days after signing. TRCP 306a(4)-(5) restarts the deadline from the date of actual notice/knowledge (up to 90 days after the original signing), on a sworn motion proving that later notice date. A defendant who first learns of a default judgment via a bank garnishment, wage withholding, or credit-report hit weeks after signing may still have a live path -- this deterministic gate should be checked before concluding the window has closed. CORRECTED 2026-09-05 (round 46), from run_20260904T221748Z.json: the 306a(4)-(5) restart described above applies to DISTRICT and COUNTY court judgments. In JUSTICE COURT the general Rules of Civil Procedure apply only when the judge so orders or a rule says so (TRCP 500.3(e); NAMED, not fetched this round), and the 500-series rules contain no 306a analogue; a justice-court defendant who first learns of the judgment 45 days after signing through a bank garnishment has, as a matter of the rules, lost both the 14-day motion and the 21-day de novo appeal. What remains is equitable: a bill of review (GLOSS-FOR-COUNSEL on whether and where a bill of review lies from a justice-court judgment, and the four-year limit), a challenge to the garnishment itself if service of the underlying citation was defective, and, in the garnishment proceeding, assertion of any exemptions. Do not tell a justice-court defendant that 306a restarts the clock.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**defective_service_note**

If service was defective or never happened at all, the Craddock three-factor test (and the meritorious-defense showing it requires) does NOT govern -- Peralta v. Heights Medical Center holds a defendant who was never properly served need not show a meritorious defense at all, because entering judgment without valid service violates due process independent of the merits. Such a defendant, even outside the 329b/505.3/306a windows, may still have a restricted appeal (within 6 months of judgment) or a bill of review (within 4 years) available -- this node should not tell a defendant with a live service defect that no remedy remains just because the ordinary motion-for-new-trial windows have closed.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**eviction_carve_out_note**

ADDED 2026-09-03 (round 38) -- CASE-ENDING if missed: the justice-court branch (TRCP 505.3, 14 days) does NOT apply to an EVICTION (forcible detainer) default. Eviction cases are governed by TRCP 510, which controls over the general justice-court rules; TRCP 510.8(e) bars a motion for new trial in an eviction case, and the operative remedy is an appeal (bond, cash deposit, or sworn statement of inability) within FIVE days of the judgment under TRCP 510.9, after which a writ of possession can issue. Directing an evicted tenant to a 14-day motion blows the 5-day deadline. Appeared in both backlog runs.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**restricted_appeal_not_limited_to_service_defects_note**

ADDED 2026-09-03 (round 38): this node offered the restricted appeal (Tex. R. App. P. 30, six months) and the bill of review only in the 'defective/no service' branch. That is too narrow. A restricted appeal requires only that the party did not participate in the hearing, filed within six months, and that error is apparent on the face of the record -- defective service is merely the most common such error; an unsupported unliquidated-damages award, a facially defective return of service, or a missing TRCP 239a certificate qualify equally. And a bill of review (four years) is available to a validly-served defendant who never received notice of the judgment through no fault of her own (e.g. the clerk never mailed the TRCP 306a notice and she learned of it only via garnishment months later), with a potentially lower showing than the ordinary Baker v. Goldsmith elements. As encoded, a consumer who concedes service but was hit with an inflated default months ago would be told no path remains. Case-law gloss, source_tier C, flagged for counsel confirmation. CORRECTED 2026-09-05 (round 46): the six-month RESTRICTED APPEAL under Tex. R. App. P. 30 is an appeal to the COURT OF APPEALS from a district or county court judgment; it is NOT available from a justice-court judgment, whose only appeal is the 21-day de novo appeal to county court under TRCP 506.1. The prior text did not limit the restricted appeal by court and was wrong as applied to justice court.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**post_motion_appellate_timetable_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: for a DISTRICT or COUNTY court default, a timely motion for new trial that is overruled by operation of law on day 75 (TRCP 329b(c)) is not the end of the road -- it EXTENDS the appellate timetable so that the notice of appeal is due within 90 days after the judgment was signed (Tex. R. App. P. 26.1(a); NAMED, not fetched this round), and the trial court keeps plenary power for 30 days after the motion is overruled (329b(e); NAMED) -- until day 105 -- during which it can still grant the motion or modify the judgment. So on day 76 the defendant has two deterministic options: press the trial court for a ruling before day 105, and file a notice of appeal by day 90 (with a 15-day extension window under TRAP 26.3). An appeal on the merits of the Craddock ruling is the standard route; missing day 90 leaves only the restricted appeal (if the defendant did not participate) or a bill of review. Checklist item added; TRAP 26.1(a)/26.3 and TRCP 329b(e) FIXED-SOURCE-NAMED.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. Has a default judgment (or dismissal-for-failure-to-appear judgment) actually been entered, and on what date was it signed?  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. Is the person still within 30 days of the judgment being signed? (Deterministic gate -- if no, this path is foreclosed regardless of the merits.) -- and, for a JUSTICE COURT judgment, within 21 days (TRCP 506.1(a)) for the no-excuse-needed appeal to county court for a fresh trial, which stays open 7 days past the 14-day motion window  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. Why did the person fail to answer or appear -- their own account of what happened (raw input for factor 1; the system does not characterize it)  (non-dispositive)  [ ] keep  [ ] change  [ ] drop
4. Does the person have a defense to the underlying claim, and what is it (raw input for factor 2; the system does not characterize it)  (non-dispositive)  [ ] keep  [ ] change  [ ] drop
5. Which court entered the default judgment -- district/county court (TRCP 329b: 30/75 days) or justice court (TRCP 505.3: 14/21 days)  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. When the person actually learned of the judgment (received notice or otherwise gained actual knowledge) -- if more than 20 days after signing, TRCP 306a(4)-(5) may restart the filing deadline from that later date, up to 90 days after signing, on a sworn motion  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. Whether the person disputes that they were validly served at all (defective/no service) -- if so, Craddock's meritorious-defense element does not apply, and a restricted appeal (6 months) or bill of review (4 years) may be available even after the ordinary motion window has closed  (dispositive)  [ ] keep  [ ] change  [ ] drop
8. THRESHOLD: is the underlying case an EVICTION (forcible detainer)? If so, TRCP 510 governs -- no motion for new trial (510.8(e)); the remedy is an appeal within 5 days of judgment (510.9). Do not apply the 14-day 505.3 window  (dispositive)  [ ] keep  [ ] change  [ ] drop
9. Even if service was valid: (a) is it within six months of the judgment and is there error apparent on the face of the record (e.g. unsupported damages) -- restricted appeal; (b) did the defendant never receive notice of the judgment through no fault of her own -- bill of review within four years  (dispositive)  [ ] keep  [ ] change  [ ] drop
10. If a timely motion for new trial in district/county court was filed and never ruled on: the 75-day overruling date and the 90-day notice-of-appeal deadline from the judgment (TRAP 26.1(a)), plus the trial court's plenary power to day 105 (329b(e)) -- both are deterministic next steps  (dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | Craddock v. Sunshine Bus Lines, Inc., 133 S.W.2d 124, 126 (Tex. 1939) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://www.courtlistener.com/opinion/4172687/craddock-v-sunshine-bus-lines-inc/ |
| 2 | Tex. R. Civ. P. 329b(a) | C | LIVE-VERIFIED (run_20260904T221748Z) | https://rulesofcivilprocedure.com/tx/rule-329b/ |
| 3 | Tex. R. Civ. P. 329b(c) | C | LIVE-VERIFIED (run_20260904T221748Z) | https://rulesofcivilprocedure.com/tx/rule-329b/ |
| 4 | Tex. R. Civ. P. 505.3(b), (e) | C | LIVE-VERIFIED (run_20260904T221748Z) | https://www.stcl.edu/lib/TexasRulesProject/TRCP474-522/rule505-32013.html |
| 5 | Tex. R. Civ. P. 306a(4)-(5) | C | LIVE-VERIFIED (run_20260904T221748Z) | https://www.stcl.edu/lib/TexasRulesProject/TRCP300-314/rule306a2024.html |
| 6 | Peralta v. Heights Medical Center, Inc., 485 U.S. 80 (1988); Tex. R. App. P. 30; bill of review (4-year limit) | D | n/a (doctrine entry, no url by design) | — |
| 7 | Tex. R. Civ. P. 510.8(e) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.stcl.edu/lib/TexasRulesProject/TRCP474-522/rule510-82013.html |
| 8 | Tex. R. Civ. P. 510.9(a) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.stcl.edu/lib/TexasRulesProject/TRCP474-522/rule510-92013.html |
| 9 | Tex. R. Civ. P. 506.1(a) | B | ADDED AFTER last run (round 46) -- not yet live-checked | https://www.stcl.edu/lib/TexasRulesProject/TRCP474-522/rule506-12013.html |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | yes (case-ending) | Eviction defaults: TRCP 510, no MNT, 5-day appeal | Threshold checklist + note |
| 02 | GLOSS-FOR-COUNSEL | yes | Restricted appeal / bill of review not limited to service defects | Note + checklist |
| 03 | FIXED-VERIFIED | yes | TRCP 506.1 de novo appeal (21 days, no excuse) omitted | 506.1(a) pinned; justice_court_variant_note expanded; checklist |
| 04 | FIXED (notes corrected; TRCP 500.3(e) named) + GLOSS (bill of review) | yes | 306a restart and TRAP 30 restricted appeal wrongly applied to justice court | notice_restart_note and restricted-appeal note corrected |
| 05 | FIXED-SOURCE-NAMED | yes | Post-motion appellate timetable (TRAP 26.1(a), 329b(e)) omitted | post_motion_appellate_timetable_note; checklist |

**Drafting revisions (author / date / summary):**

- 2026-08-30 — Added TRCP 505.3 justice-court variant, TRCP 306a(4)-(5) notice-restart rule, and the Peralta defective-service exception (with the restricted-appeal/bill-of-review alternative remedies); added 3 checklist items and extended what_the_system_may_say to cover these as additional deterministic gates --
- 2026-09-02 — Replaced the 505.3 paraphrase with verbatim (b) and (e); logic unchanged (already correct).
- 2026-09-03 — Added the eviction carve-out (TRCP 510.8/510.9) as a threshold question and broadened the restricted-appeal / bill-of-review paths beyond service defects. Both backlog findings (both runs) addressed; TRCP 510 text NOT pinned this session -- SOURCE PENDING.
- 2026-09-04 — Pinned TRCP 510.8(e) and 510.9(a); removed the SOURCE PENDING marker on the eviction carve-out. Restricted-appeal scope remains a case-law gloss.
- 2026-09-05 — Round 46: TRCP 506.1(a) pinned + justice_court_variant_note expanded + checklist; notice_restart_note and restricted-appeal note corrected for justice court (500.3(e) NAMED; bill of review GLOSS); post_motion_appellate_timetable_note (TRAP 26.1(a), 26.3, TRCP 329b(e) NAMED) + checklist.

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed True · material findings 3 (all dispositioned in round 46; see D)

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---

## 4. TX-WAGE-GARNISHMENT-PROHIBITION

**Title:** Texas constitutionally prohibits wage garnishment for ordinary consumer debt  
**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `154763d5add9fdcf6175213c9382047595d8c0b720a107357cf590eafb37ae6c`

**Reading load:** logic 1,144 words · checklist 368 · cited text 1,375 · 8 citations · 9 checklist items · 4 drafting revisions

### A. Logic (read in full; this is the content being certified)

**current_wages_garnishable_for_consumer_debt**

False

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**exceptions**

- court-ordered child support
- court-ordered spousal maintenance

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**note**

This is a state constitutional protection stronger than federal law (which permits limited wage garnishment for ordinary debts, subject to CCPA caps) — Texas debtors facing a post-judgment collection effort should know their WAGES specifically cannot be garnished for an ordinary debt judgment, though bank account funds CAN generally be frozen/seized (a separate mechanism, garnishment of a bank account rather than of wages -- not the same protection). Do not conflate the two. QUALIFIED 2026-09-03 (round 38): 'can be frozen' is NOT unqualified -- an account holding directly-deposited federal benefits (Social Security, 42 U.S.C. 407; VA, 38 U.S.C. 5301) is protected after deposit, and 31 C.F.R. Part 212 requires the bank to automatically protect two months of such deposits without any claim by the debtor; see bank_account_exempt_deposits_note.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**determination**

if the creditor is attempting to garnish CURRENT WAGES for an ordinary debt judgment (not child support/spousal maintenance), that garnishment is unconstitutional under Texas law

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**federal_override_note**

Tex. Civ. Prac. & Rem. Code § 63.004 -- the statutory companion to the constitutional protection above -- expressly carves out 'except as otherwise provided by ... federal law.' Federal-law wage garnishments DO reach current Texas wages notwithstanding this state protection, including: IRS tax levies (26 U.S.C. § 6331 et seq.), Department of Education administrative wage garnishment on defaulted federal student loans (20 U.S.C. § 1095a), federal criminal restitution orders, and garnishment to satisfy certain federal-court judgments. A Texas debtor facing one of these should NOT be told the garnishment is unconstitutional -- it is not, and treating it as such could cause the debtor to miss the actual hearing/appeal deadlines that federal administrative-garnishment procedures provide as the real remedy.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**personal_service_classification_note**

This node's protection is expressly for 'current wages for PERSONAL SERVICE.' Whether a specific payment counts is NOT simply a matter of W-2-employee vs. 1099-independent-contractor classification -- courts look at whether the amount is compensation currently owed for personal service, and there is a real (if genuinely unsettled and fact-specific) argument for protecting some contractor-type compensation too, particularly amounts not yet reduced to a simple account receivable. This node does NOT resolve that classification question one way or the other -- flagged as a threshold fact question rather than assumed, in either direction, to avoid both overclaiming protection for ordinary business receivables and wrongly denying protection to a genuine personal-service earner simply because they were paid on a 1099.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**out_of_state_employer_caveat**

This node assumes Texas exemption law governs whenever the debtor is a Texas resident. Where a Texas judgment is domesticated in another state and garnishment is served on an out-of-state employer there, which state's garnishment/exemption law actually controls is a genuinely unsettled, fact- and forum-specific conflicts-of-law question -- this node does NOT resolve it and should not be read to guarantee the Texas protection follows the debtor's wages to an out-of-state garnishee. Flagged, not resolved, consistent with how this corpus treats other genuinely contested cross-jurisdictional questions (see, e.g., TX-HOMESTEAD-EXEMPTION's HOA-lien caveat).

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**bank_account_exempt_deposits_note**

ADDED 2026-09-03 (round 38): for the very common debtor whose only income is Social Security/SSDI/VA benefits, a bank garnishment is NOT 'fair game' -- federal law protects those benefits after deposit and the bank must run a two-month lookback and shield that amount automatically (31 C.F.R. Part 212). The debtor's remedies are the bank's account-review protection plus an exemption claim, not acquiescence. Appeared in both backlog runs. EXPANDED 2026-09-05 (round 46), from run_20260904T221748Z.json: the federal-benefit rules above are not the only shield for deposited funds. TEXAS statutory exemptions also follow certain benefits into a bank account: unemployment compensation (Lab. Code 207.075(b)-(c), quoted -- exempt 'from levy, execution, attachment, or any other remedy for debt collection,' and after receipt so long as not commingled, with a necessaries exception); workers' compensation income benefits (Lab. Code 408.201, NAMED); public and private retirement benefits (Prop. Code 42.0021, quoted on the sibling TX-EXEMPT-PERSONAL-PROPERTY node); and current wages themselves for a short window after deposit (see current_wages_deposit_note there -- GLOSS-FOR-COUNSEL, the Texas cases are split on whether wages keep their character once deposited). A debtor whose frozen account holds unemployment benefits must ASSERT the exemption in the garnishment proceeding (answer/claim under TRCP 664a; NAMED) -- Texas exemptions are not self-executing. Checklist item on deposit source expanded.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**turnover_order_note**

ADDED 2026-09-03 (round 38): because wage garnishment is barred, the standard Texas post-judgment tool is a TURNOVER ORDER and receivership under Tex. Civ. Prac. & Rem. Code § 31.002. This node recognized only 'garnishment of wages vs. of a bank account,' so a turnover order directing the debtor to hand over paycheck proceeds would be labeled 'unconstitutional garnishment.' It is not: Tex. Civ. Prac. & Rem. Code § 31.0025 (quoted above) bars any turnover order 'before a judgment debtor is paid wages' -- so a turnover order cannot reach wages still in the employer's hands -- but once wages are PAID to the debtor, turnover/receivership reaching the proceeds is not barred by that section and Texas courts enforce such orders by contempt (Beaumont Bank v. Buller line). PINNED 2026-09-04 (round 39): the unpaid/paid line is now statutory, not just case law. The debtor's remedy is an exemption objection or appeal of the order -- and defying a valid turnover order risks contempt. Appeared in both backlog runs.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**employer_deductions_not_garnishment_note**

ADDED 2026-09-03 (round 38): an EMPLOYER's own payroll deductions (recouping a signed-for advance, unreturned equipment) and VOLUNTARY written wage assignments/authorized payroll deductions to a lender are not garnishment and are not reached by the constitutional prohibition; they are governed by Tex. Lab. Code § 61.018 (deductions lawful only with written authorization or legal authority) and the Texas Workforce Commission wage-claim process. Pointing such an employee at a constitutional 'garnishment' claim sends her to the wrong remedy.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**contractual_alimony_caveat**

ADDED 2026-09-03 (round 38): the 'court-ordered spousal maintenance' exception is Chapter 8 statutory maintenance. Purely CONTRACTUAL alimony in an agreed divorce decree, to the extent it exceeds what Chapter 8 would allow, has been treated by Texas courts as an ordinary contract debt NOT enforceable by wage withholding. Case-law gloss, source_tier C, flagged for counsel confirmation.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**support_withholding_cap_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: the child-support and spousal-maintenance EXCEPTIONS to the wage-garnishment prohibition are not unlimited. Tex. Fam. Code 158.009 caps an income-withholding order for child support at 50% of the obligor's DISPOSABLE EARNINGS (and Fam. Code 8.106 caps spousal-maintenance withholding at the lesser of 20% of average monthly gross or the 158.009 amount; NAMED). An employer withholding 70% is withholding unlawfully even though the underlying order is valid; the obligor's remedy is a motion in the family court that issued the order (and, for arrears, Fam. Code 158.003-.004 govern how much of the withholding may be applied to arrears; NAMED). Federal law adds an outer ceiling (15 U.S.C. 1673(b)). Output should be 'garnishable up to 50% of disposable earnings for support; anything above is challengeable,' never 'no protection.' Checklist item added.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. Whether what's being targeted is wages specifically (garnishable-none, ordinary debt) vs. a bank account (garnishable, separate mechanism) vs. child support/spousal maintenance (garnishable)  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. Whether the garnishing party is a federal agency/program (IRS, Dept. of Education, federal criminal restitution) rather than an ordinary private judgment creditor -- federal garnishments override this state-law protection  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. Whether the payment being garnished is genuinely 'current wages for personal service' as opposed to a business receivable, draw, or other compensation not currently owed for personal service -- this is a fact-specific question not resolved by W-2 vs. 1099 status alone  (dispositive)  [ ] keep  [ ] change  [ ] drop
4. Whether the garnishment is being served on an out-of-state employer in another state's courts (which state's law controls is an unresolved, forum-specific question this node does not answer)  (dispositive)  [ ] keep  [ ] change  [ ] drop
5. If a bank account is targeted: does it hold directly-deposited Social Security, SSDI, or VA benefits? Those remain protected after deposit and the bank must automatically shield two months' worth (42 U.S.C. 407; 31 C.F.R. Part 212) -- OR Texas unemployment benefits (Lab. Code 207.075), workers' compensation (408.201), retirement benefits (Prop. Code 42.0021), or wages deposited within the last pay cycle? Each is a separate exemption that must be asserted in the garnishment proceeding  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. Is the instrument a writ of GARNISHMENT on the employer, or a TURNOVER ORDER/receivership under CPRC 31.002 directed at the debtor for paycheck proceeds already received? The constitutional bar addresses the former; the latter is generally valid as to paid wages  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. Is the deduction being made by the employer itself, or under a written authorization the employee signed? That is a Lab. Code 61.018 / TWC wage-claim question, not garnishment  (dispositive)  [ ] keep  [ ] change  [ ] drop
8. If the exception claimed is spousal maintenance: is it Chapter 8 court-ordered maintenance, or contractual alimony in an agreed decree (which may not be enforceable by withholding beyond Chapter 8 limits)?  (dispositive)  [ ] keep  [ ] change  [ ] drop
9. If the withholding is for CHILD SUPPORT or spousal maintenance: what percentage of DISPOSABLE earnings is being withheld? Support withholding is capped at 50% of disposable earnings (Fam. Code 158.009; maintenance lower under 8.106); amounts above the cap are challengeable in the issuing family court  (dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | Tex. Const. art. XVI, § 28 | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/CN/htm/CN.16.htm |
| 2 | Tex. Civ. Prac. & Rem. Code § 63.004 | B | LIVE-VERIFIED (run_20260904T221748Z) | https://texas.public.law/statutes/tex._civ._practice_and_remedies_code_section_63.004 |
| 3 | 42 U.S.C. § 407(a) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title42-section407&num=0&edition=prelim |
| 4 | 31 C.F.R. § 212.6(a), (c); § 212.3 (lookback period) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.ecfr.gov/current/title-31/subtitle-B/chapter-II/subchapter-A/part-212/section-212.6 |
| 5 | Tex. Civ. Prac. & Rem. Code § 31.0025(a) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/CP/htm/CP.31.htm |
| 6 | Tex. Lab. Code § 61.018 | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/LA/htm/LA.61.htm |
| 7 | Tex. Fam. Code § 158.009 | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/FA/htm/FA.158.htm |
| 8 | Tex. Lab. Code § 207.075(b)-(c) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/LA/htm/LA.207.htm |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | yes | "Bank accounts CAN be frozen" ignores federal-benefit deposits (42 USC 407; 31 CFR 212) | Note qualified + checklist |
| 02 | FIXED-VERIFIED | yes (contempt risk) | Turnover orders / receivership (CPRC 31.002) mislabeled unconstitutional | Note + checklist |
| 03 | FIXED-VERIFIED | no | Employer deductions / wage assignments are not garnishment (Lab. Code 61.018) | Note + checklist |
| 04 | GLOSS-FOR-COUNSEL | no | Contractual alimony vs. Ch. 8 maintenance | Note + checklist |
| 05 | FIXED-VERIFIED (207.075) + NAMED (408.201) | yes | Texas statutory exemptions for deposited benefits omitted | 207.075(b)-(c) pinned; bank_account_exempt_deposits_note expanded; checklist |
| 06 | FIXED-VERIFIED | yes | Support withholding treated as 'no protection'; 50% cap omitted | Fam. Code 158.009 pinned; support_withholding_cap_note; checklist |

**Drafting revisions (author / date / summary):**

- 2026-08-30 — Added Tex. Civ. Prac. & Rem. Code § 63.004's federal-law override clause (IRS/Dept. of Ed/restitution garnishments reach current Texas wages notwithstanding the state protection); added a hedged independent-contractor classification note (flagged as genuinely unsettled/fact-specific rather than repe
- 2026-09-03 — Qualified the 'bank accounts CAN be frozen' statement for federal-benefit deposits; added turnover-order, employer-deduction, and contractual-alimony notes; 4 checklist questions. All 6 backlog findings (both runs) addressed; 42 U.S.C. 407 / 31 CFR 212 / CPRC 31.002 / Lab. Code 61.018 text NOT pinne
- 2026-09-04 — Pinned 42 U.S.C. 407(a), 31 CFR 212.6/212.3, CPRC 31.0025(a), Lab. Code 61.018; removed 3 SOURCE PENDING markers; turnover note now statute-anchored. Contractual-alimony point remains a gloss.
- 2026-09-05 — Round 46: Fam. Code 158.009 pinned + support_withholding_cap_note + checklist; Lab. Code 207.075(b)-(c) pinned + bank_account_exempt_deposits_note expanded (408.201, 42.0021, TRCP 664a NAMED) + checklist reworded.

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed True · material findings 2 (all dispositioned in round 46; see D)

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---

## 5. TX-EXEMPT-PERSONAL-PROPERTY

**Title:** Texas personal-property exemption from creditor seizure  
**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `75cca1af294d98db3591199ec6ae1cc0d2f723c7b2ac642bc7a251f65bdff404`

**Reading load:** logic 1,647 words · checklist 674 · cited text 3,193 · 12 citations · 16 checklist items · 8 drafting revisions

### A. Logic (read in full; this is the content being certified)

**aggregate_cap**

- {"family": 100000, "single_adult_not_in_family": 50000}

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**cap_measured**

aggregate fair market value, exclusive of liens/security interests/other encumbrances, of the § 42.002(a) items combined

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**unlimited_categories_outside_the_cap**

- current wages (except child-support enforcement) -- CROSS-REFERENCE added 2026-09-03 (round 38): see TX-WAGE-GARNISHMENT-PROHIBITION's federal_override_note for the federal carve-outs that DO reach Texas wages (IRS levies, Dept. of Education administrative garnishment on defaulted federal student loans under 20 U.S.C. § 1095a, federal restitution), and Tex. Fam. Code ch. 8 spousal maintenance; 'unlimited' here means unlimited against an ORDINARY private judgment creditor
- professionally prescribed health aids
- alimony/support/separate maintenance
- a religious bible or sacred text (with a landlord-lien carve-out)
- qualified retirement plans, pensions, IRAs, and similar tax-qualified savings accounts (Tex. Prop. Code § 42.0021) -- essentially unlimited in amount for qualifying plans; distributed amounts remain exempt for 60 days after distribution, longer if rolled over
- life insurance cash value and proceeds, and annuity contract/benefit plan proceeds (Tex. Ins. Code § 1108.051) -- fully exempt, outside the § 42.001 aggregate cap, separate from the Property Code chapter this node otherwise draws from -- SUBJECT TO 3 exceptions added 2026-09-02 (round 36): (1) a premium payment made in fraud of a creditor, (2) a debt secured by a pledge of the policy itself, and (3) a child-support lien (Tex. Ins. Code § 1108.053)
- Texas Tomorrow Fund prepaid-tuition contracts, Chapter 54 Education Code savings-trust accounts, and Section 529 qualified tuition programs -- CORRECTED 2026-09-02 (round 36): these are NOT a separate Property Code § 42.0022 (that citation does not resolve to any real, current statute -- confirmed both by a direct fetch of Property Code chapter 42, which has no such section between §42.0021 and §42.003, and by the texas.public.law mirror URL for it redirecting to the site's generic statutes index). They are already covered as 'qualified savings plans' under § 42.0021(a)(8)-(10) -- see that entry above; this is redundant with, not additional to, that exemption

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**note_re_secured_property**

a security interest or lien validly fixed on otherwise-exempt property (e.g., a car loan lien on an exempt vehicle) is NOT defeated by the exemption — § 42.001(c)/§42.002(b).

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**item_level_sub_caps_note**

The § 42.001 aggregate dollar cap is necessary but NOT sufficient -- § 42.002(a) also imposes separate item-level sub-limits within the aggregate, most notably: jewelry is capped at 25% of the aggregate limit; motor vehicles are limited to one per family member or single adult who holds a driver's license (or who relies on another licensed household member to drive); firearms are limited to two. A debtor whose TOTAL value is under the aggregate cap can still have non-exempt property if a specific category exceeds its own sub-limit -- this node does not itself apply those sub-limits.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**override_exceptions_note**

This exemption does not defeat: (1) a validly-fixed lien or security interest on the specific property (already noted in note_re_secured_property); (2) a child-support lien under Tex. Fam. Code ch. 157, subch. G (§ 42.005); (3) property acquired via a fraudulent transfer intended to defraud, delay, or hinder creditors -- generally within 2 years of the TRANSACTION (not necessarily the same as the acquisition date), CORRECTED 2026-09-02 (round 36) to add: an unliquidated or contingent claim may instead be asserted up to 1 year after it is reduced to judgment, which can extend well past the general 2-year window (§ 42.004); or (4) a federal tax lien or levy (26 U.S.C. §§ 6321, 6334), which overrides state exemptions under the Supremacy Clause.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**current_wages_deposit_note**

The unlimited 'current wages' exemption above protects wages only while they remain unpaid, owed compensation for personal service. Once wages are actually paid and deposited into a bank account, Texas case law treats them as losing their 'current wages' character upon deposit and commingling with other funds (subject to limited tracing arguments for a debtor who can show the specific funds are traceable wages, e.g. a single recent, unmingled direct deposit). Bank-account garnishment -- not wage garnishment itself, which Texas separately prohibits outright for ordinary debts -- is the single most common real-world Texas debt-collection scenario, and this node's flat 'current wages are exempt in unlimited amount' framing should not be read to mean a bank account holding a recently-deposited paycheck is automatically fully protected.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**family_definition_note**

The 'family or single-adult-not-in-family' checklist distinction that sets the $100,000 vs. $50,000 cap is not simply about marital status. Under Texas case law, a 'family' for homestead/exemption purposes includes a head of household who lives with and has a legal or moral obligation to support dependents -- e.g., an unmarried or divorced parent supporting minor children in the home -- even without a spouse. Taking a debtor's self-description as 'single' at face value, without asking about dependents living with and supported by them, can wrongly apply the lower $50,000 cap to someone actually entitled to the $100,000 family cap.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**enumerated_list_gate_note**

ADDED 2026-09-03 (round 38) -- THRESHOLD, and the most consequential gap in this node: the $100,000/$50,000 aggregate cap applies ONLY to property that is on the § 42.002(a) list quoted above (home furnishings and heirlooms, provisions for consumption, farm/ranch vehicles and implements, tools/equipment/books/apparatus of a trade or profession, clothing, jewelry (capped), two firearms, athletic and sporting equipment, one motor vehicle per licensed family member, the listed animals, and household pets). Anything NOT on that list is NOT exempt under this chapter at all, no matter how far under the cap the debtor's total is: CASH, BANK DEPOSITS, brokerage/stock/crypto holdings, tax refunds, accounts receivable, and recreational items such as boats are 100% reachable (subject only to OTHER specific exemptions -- e.g. the unlimited categories above, and the federal-benefit protections flagged below). This node previously framed the analysis as 'aggregate value under the cap = exempt,' which would tell a debtor with $36,000 in savings and brokerage accounts that everything is protected. Bank garnishment is the single most common Texas judgment-collection scenario, so the prior framing ran in the dangerous direction for the modal user.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**federal_benefits_in_bank_accounts_note**

ADDED 2026-09-03 (round 38): the current_wages_deposit_note's 'deposited funds generally lose exempt character' point must NOT be applied to federal benefits. Social Security (42 U.S.C. § 407) and VA benefits (38 U.S.C. § 5301) remain exempt after deposit, and the Treasury rule at 31 C.F.R. Part 212 requires the bank receiving a garnishment order to protect, automatically and without any claim by the debtor, two months' worth of directly-deposited federal benefits. Elderly and disabled debtors are a large share of Texas garnishment targets; the checklist never asked the source of deposited funds. EXPANDED 2026-09-05 (round 46), from run_20260904T221748Z.json: the enumerated-list gate ('anything not listed is 100% reachable') is subject to the TEXAS statutory exemptions that follow specific benefits into a bank account, not only the federal ones: unemployment compensation (Lab. Code 207.075(b)-(c), quoted on the sibling TX-WAGE node -- exempt after receipt if not commingled, necessaries excepted); workers' compensation income benefits (Lab. Code 408.201; NAMED); retirement benefits (Prop. Code 42.0021, quoted above). A debtor receiving workers' comp or unemployment by direct deposit whose account is garnished should assert that exemption in the garnishment answer, and should keep those deposits in an account with nothing else in it. Checklist item on deposit source expanded.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**independent_contractor_receivables_note**

ADDED 2026-09-03 (round 38): the unlimited 'current wages for personal services' category protects an EMPLOYEE's unpaid wages. Texas courts distinguish those from an independent contractor's accounts receivable, commissions, and owner draws, which are generally NOT 'current wages' and can be garnished in the payor's hands. A gig/1099 worker should not be told unpaid invoices are exempt. Case-law gloss, source_tier C, flagged for counsel confirmation.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**bankruptcy_domicile_rule_note**

ADDED 2026-09-03 (round 38): in BANKRUPTCY, a debtor domiciled in Texas for fewer than 730 days before filing cannot use Texas exemptions at all -- 11 U.S.C. § 522(b)(3)(A) requires the exemptions of the state of prior domicile (or the federal set), so the $100,000 cap and the unlimited retirement exemption may be unavailable to a recent transplant. Same rule flagged on TX-HOMESTEAD-EXEMPTION.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**marital_property_liability_screen_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: before asking whether an item is EXEMPT, ask whether it is LIABLE. Texas is a community-property state and Fam. Code 3.202 sorts marital property by who incurred the debt and when: (a) a spouse's SEPARATE property is never liable for the other spouse's debt; (b) community property under the NON-debtor spouse's SOLE management (her wages, her separately titled account, property she alone controls) is not liable for the debtor spouse's PREMARITAL debts or NONTORTIOUS debts incurred during marriage; (c) community property under the debtor spouse's sole or JOINT management IS liable for that spouse's debts, before or during marriage. So on a judgment against the wife alone for a card she opened before the marriage: a joint bank account (joint management) is reachable; the husband's paycheck account in his name alone is not; a car titled to him alone and bought with his earnings is not. Fam. Code 3.102 (NAMED) defines sole-management community property (each spouse's personal earnings, revenue from separate property, recoveries for personal injuries, and increases of those). The exemption analysis in this node applies only to property that survives this screen. Checklist item added; 3.102 FIXED-SOURCE-NAMED.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**exemptions_not_self_executing_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: Texas personal-property exemptions are substantive but NOT self-executing in post-judgment enforcement. When a constable levies under a writ of execution, or a bank is served with a writ of garnishment, the debtor must ASSERT the exemption: by a claim of exemption / motion to dissolve or vacate the writ in the issuing court for an execution levy, and by answering in the garnishment proceeding (TRCP 658-679, in particular the 664a motion to dissolve or modify the writ; NAMED, not fetched this round). Deadlines are short and the property can be sold, or the frozen funds paid over, while the debtor waits. There is no automatic $50,000/$100,000 shield that stops a sale on its own. Route any debtor with a levy or garnishment in hand to the procedural step first. Cross-references: TX-WAGE-GARNISHMENT-PROHIBITION's bank_account_exempt_deposits_note (garnishment answer), TX-JUSTICE-COURT node (JP-court garnishments). Checklist item added.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. THRESHOLD, if the debtor is MARRIED: who incurred the debt and when (before or during the marriage), and for each targeted asset, is it the non-debtor spouse's SEPARATE property, community property under the NON-debtor spouse's SOLE management (her own earnings, her sole-name account), or joint/debtor-managed community property? Only the last is liable on a judgment against one spouse for a premarital or nontortious debt (Fam. Code 3.202) -- exemption is the second question, not the first  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. Family or single-adult-not-in-family status of the debtor (sets the $100,000 vs $50,000 cap) -- 'family' includes an unmarried head of household supporting dependents living with them, not only a debtor with a spouse; do not infer 'single adult' status merely from the debtor's own unprompted self-description  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. THRESHOLD: is each specific asset the creditor is targeting actually ON the § 42.002(a) list (furnishings, food, tools of trade, clothing, jewelry, two firearms, sporting equipment, one vehicle per licensed family member, listed animals, pets)? Cash, bank deposits, brokerage/stock accounts, tax refunds, receivables, and boats are NOT listed and are not exempt under this chapter regardless of the aggregate cap  (dispositive)  [ ] keep  [ ] change  [ ] drop
4. Aggregate fair market value of the debtor's § 42.002(a)-listed personal property, net of liens  (dispositive)  [ ] keep  [ ] change  [ ] drop
5. Whether any specific item the creditor is targeting is subject to its own valid lien/security interest (e.g., a financed vehicle) — exemption does not defeat that lien  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. Whether the debtor holds retirement accounts, pensions, or IRAs (exempt in essentially unlimited amount, IN ADDITION TO the aggregate cap, under Tex. Prop. Code § 42.0021 -- not counted against the $100,000/$50,000 limit)  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. Whether any single item category (jewelry, vehicles, firearms) exceeds its own item-level sub-limit within § 42.002(a), even if the aggregate total is under the § 42.001 cap  (dispositive)  [ ] keep  [ ] change  [ ] drop
8. Whether the creditor is a federal tax authority (IRS) or a child-support obligee/agency (both can reach otherwise-exempt property; voluntary liens/security interests are already covered elsewhere in this node)  (dispositive)  [ ] keep  [ ] change  [ ] drop
9. Whether the debtor holds life insurance cash value/proceeds or annuity benefits (Tex. Ins. Code § 1108.051) or 529/Texas Tomorrow Fund college savings accounts (Tex. Prop. Code § 42.0022) -- both exempt in addition to, not counted against, the aggregate cap  (dispositive)  [ ] keep  [ ] change  [ ] drop
10. Whether the property being targeted is unpaid wages still owed (fully exempt) versus wages already paid and deposited/commingled in a bank account (which may lose the unlimited 'current wages' characterization, subject to tracing)  (dispositive)  [ ] keep  [ ] change  [ ] drop
11. If relying on the § 42.004 fraudulent-transfer exception's time bar, confirm whether the creditor's claim was unliquidated or contingent at the time of the transaction -- if so, the 1-year-after-judgment alternative may apply instead of (and extend well past) the general 2-year-from-transaction limit  (dispositive)  [ ] keep  [ ] change  [ ] drop
12. If relying on the life-insurance/annuity exemption, confirm the claim doesn't fall within one of § 1108.053's 3 exceptions (fraudulent premium payment, policy pledged to secure a debt, or a child-support lien)  (dispositive)  [ ] keep  [ ] change  [ ] drop
13. If a bank account is targeted: what is the SOURCE of the deposited funds -- directly-deposited Social Security/VA/other federal benefits are protected after deposit (42 U.S.C. 407; 31 C.F.R. Part 212 automatic 2-month protection), unlike ordinary wages -- including Texas unemployment (Lab. Code 207.075) and workers' compensation (408.201) benefits, which are exempt after deposit if not commingled  (dispositive)  [ ] keep  [ ] change  [ ] drop
14. Whether the debtor is a W-2 employee (unpaid wages exempt) or an independent contractor/owner whose unpaid invoices, commissions, or draws are generally not 'current wages'  (dispositive)  [ ] keep  [ ] change  [ ] drop
15. Whether the exemption is being asserted in a BANKRUPTCY case and, if so, whether the debtor has been domiciled in Texas for at least 730 days -- if not, Texas exemptions may be unavailable (11 U.S.C. 522(b)(3)(A))  (dispositive)  [ ] keep  [ ] change  [ ] drop
16. PROCEDURAL: has a writ of execution been levied or a writ of garnishment served, and has the debtor filed a claim of exemption / motion to dissolve (TRCP 664a) or an answer asserting the exemption? Texas exemptions must be asserted; unclaimed exempt property can be sold or paid over  (dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | Tex. Prop. Code § 42.001(a) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/PR/htm/PR.42.htm |
| 2 | Tex. Prop. Code § 42.001(b) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/PR/htm/PR.42.htm |
| 3 | Tex. Prop. Code § 42.002(a) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/PR/htm/PR.42.htm |
| 4 | Tex. Prop. Code § 42.0021(b), (e) | B | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/PR/htm/PR.42.htm |
| 5 | Tex. Ins. Code § 1108.051 | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/IN/htm/IN.1108.htm |
| 6 | Tex. Prop. Code § 42.005(a) | B | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/PR/htm/PR.42.htm |
| 7 | Tex. Prop. Code § 42.004(a)-(b) | B | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/PR/htm/PR.42.htm |
| 8 | Tex. Ins. Code § 1108.053 | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/IN/htm/IN.1108.htm |
| 9 | 42 U.S.C. § 407(a) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title42-section407&num=0&edition=prelim |
| 10 | 31 C.F.R. § 212.6(a), (c); § 212.3 (lookback period) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.ecfr.gov/current/title-31/subtitle-B/chapter-II/subchapter-A/part-212/section-212.6 |
| 11 | 11 U.S.C. § 522(b)(3)(A) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title11-section522&num=0&edition=prelim |
| 12 | Tex. Fam. Code § 3.202(a)-(c) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/FA/htm/FA.3.htm |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | yes -- the worst one | Everything under the cap treated as exempt; cash/bank/brokerage/boats are not listed | § 42.002(a) already quoted; threshold checklist item inserted at position 1 |
| 02 | FIXED-VERIFIED | yes | Federal benefits in bank accounts | Note + checklist |
| 03 | COVERED | -- | Student-loan AWG / spousal maintenance reach wages | Already in TX-WAGE-GARNISHMENT's federal_override_note; cross-reference added |
| 04 | GLOSS-FOR-COUNSEL | yes | Independent-contractor receivables are not "current wages" | Note + checklist |
| 05 | FIXED-VERIFIED | yes | 730-day bankruptcy domicile rule | Note + checklist |
| 06 | FIXED-SOURCE-NAMED (TRCP 664a) | yes | Exemptions not self-executing; procedure omitted | exemptions_not_self_executing_note; checklist |
| 07 | FIXED-VERIFIED (207.075 on sibling) + NAMED (408.201) | yes | Texas statutory exemptions for deposited benefits omitted | federal_benefits note expanded; checklist |
| 08 | FIXED-VERIFIED | no (overstates creditor) | No marital-property liability screen (Fam. Code 3.202) | 3.202 pinned; marital_property_liability_screen_note; threshold checklist |

**Drafting revisions (author / date / summary):**

- 2026-08-30 — Added Tex. Prop. Code § 42.0021 retirement-account exemption (unlimited, outside the aggregate cap) and § 42.004/§ 42.005 fraudulent-transfer/child-support-lien override derived_from entries; added item_level_sub_caps_note (jewelry 25%, vehicles-per-licensed-driver, two firearms) and override_except
- 2026-08-30 — Added Tex. Ins. Code § 1108.051 (life insurance/annuity) and Tex. Prop. Code § 42.0022 (529/Texas Tomorrow Fund) as exempt-outside-the-cap categories; added current_wages_deposit_note and family_definition_note; tightened checklist item 1's family-status wording and added 2 new checklist items.
- 2026-09-02 — Split the merged §42.005/§42.004 derived_from entry into two clean, independently-verifiable citations. Corrected §42.004's quoted_text and override_exceptions_note to reflect the statute's actual two-branch time bar (2 years from the transaction, OR 1 year after judgment for unliquidated/contingent
- 2026-09-02 — Fixed §42.0021's bracket/mislabeling; removed fabricated §42.0022 citation (content already covered by §42.0021(a)(8)-(10)); fixed and re-pinned §1108.051 to the official statutes site with source_tier upgraded to A; added §1108.053's 3 exceptions to the life-insurance exemption as a new derived_fro
- 2026-09-02 — Added manual_verification (2026-09-02) to: Tex. Prop. Code § 42.0021(b), (e); Tex. Ins. Code § 1108.051; Tex. Prop. Code § 42.005(a); Tex. Prop. Code § 42.004(a)-(b); Tex. Ins. Code § 1108.053 -- consistent with the convention already used for this domain on TX-SOL-CONSUMER-DEBT and others.
- 2026-09-03 — Added the enumerated-list threshold gate (from § 42.002(a) text already verified in this node) -- cash/bank/brokerage/boats are not exempt regardless of the cap; added federal-benefits-in-bank-accounts, independent-contractor, and bankruptcy-domicile notes; cross-referenced the wage node's federal c
- 2026-09-04 — Pinned 42 U.S.C. 407(a), 31 CFR 212.6/212.3, and 11 U.S.C. 522(b)(3)(A); removed 2 SOURCE PENDING markers. Independent-contractor receivables remains a case-law gloss.
- 2026-09-05 — Round 46: exemptions_not_self_executing_note (TRCP 664a NAMED) + checklist; federal_benefits note expanded (207.075 cross-pinned on TX-WAGE; 408.201 NAMED) + checklist; Fam. Code 3.202 pinned + marital_property_liability_screen_note + threshold checklist (3.102 NAMED).

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed True · material findings 3 (all dispositioned in round 46; see D)

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---

## 6. TX-HOMESTEAD-EXEMPTION

**Title:** Texas homestead exemption from creditor seizure  
**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `e435899aa729d8e271b1cfd615a239b5a09107bdcef2da48446399720b7934a0`

**Reading load:** logic 1,259 words · checklist 451 · cited text 1,894 · 10 citations · 11 checklist items · 4 drafting revisions

### A. Logic (read in full; this is the content being certified)

**homestead_exempt_from_ordinary_debt_seizure**

True

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**no_dollar_value_cap**

Texas's homestead exemption, unlike its personal-property exemption, has NO dollar-value cap under STATE law -- acreage-limited only. CAUTION: this is true for ordinary state-court judgment collection, but NOT for a federal bankruptcy filing -- see bankruptcy_value_cap_note below, which is a materially different rule for a debtor in or considering bankruptcy.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**acreage_limits**

- {"urban": "10 acres (family or single adult)", "rural_family": "200 acres", "rural_single_adult": "100 acres"}

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**exceptions_where_homestead_CAN_be_seized**

- purchase-money liens
- property tax liens
- home-improvement liens contracted in writing
- certain divorce-related owelty of partition
- home-equity loans meeting Tex. Const. art. XVI § 50(a)(6)
- reverse mortgages meeting § 50(k)-(p)
- federal tax liens (26 U.S.C. § 6321) and, similarly, federal criminal restitution or forfeiture judgments -- these override the Texas homestead exemption under the U.S. Constitution's Supremacy Clause (United States v. Rodgers, 461 U.S. 677 (1983)); Texas's 'property tax liens' exception in its own exemption statute does not itself reach federal tax debt, but federal supremacy independently does

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**proceeds_protection**

sale proceeds of a homestead are protected from creditor seizure for 6 months after the sale date (§ 41.001(c))

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**bankruptcy_value_cap_note**

In a Chapter 7 or 13 bankruptcy filing, 11 U.S.C. § 522(p) caps the protected homestead equity ACQUIRED IN THE 1,215 DAYS (~40 months) before filing at a periodically-adjusted federal ceiling (currently $214,000, effective for cases filed April 1, 2025 through March 31, 2028) regardless of Texas's uncapped state-law exemption. This particularly affects debtors who recently relocated to Texas from ANOTHER state. CORRECTED 2026-09-05 (round 46): it does NOT reach equity rolled over from a previous Texas principal residence acquired before the 1,215-day window -- 522(p)(2)(B) expressly excludes 'any interest transferred from a debtor's previous principal residence ... into the debtor's current principal residence, if the debtor's previous and current residences are located in the same State.' A lifelong Texan who sold a Houston home owned since 2005 and bought a Dallas house 18 months ago with $400,000 of rolled-over equity keeps that equity under the uncapped Texas exemption; only NEW equity added inside the window (a larger down payment from savings, paydown, appreciation attributable to improvements) counts toward the cap. An earlier version of this note said the reverse and was dangerous in the direction of steering a debtor away from a Chapter 7 she could safely file. § 522(o) separately reduces protected equity traceable to a fraudulent pre-bankruptcy asset transfer. This node's 'no cap' statement applies only outside bankruptcy.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**hoa_lien_caveat**

Homeowners'-association assessment liens are NOT among the clean statutory exceptions in Tex. Prop. Code § 41.001(b) (which lists only purchase-money, tax, contracted-in-writing improvement, owelty, refinance, home-equity-loan, and reverse-mortgage liens). Texas case law (e.g., Inwood North Homeowners' Ass'n v. Harris, 736 S.W.2d 632 (Tex. 1987)) has allowed HOA assessment-lien enforcement against a homestead in some circumstances, generally tied to whether the restrictive-covenant lien predates the homestead claim or fits within the constitutional exceptions. This is a genuinely unsettled, fact-specific area this node does NOT resolve -- flagged rather than asserted either way; a debtor facing HOA foreclosure should not be told the homestead exemption categorically protects the property without case-specific review.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**bankruptcy_domicile_rule_note**

ADDED 2026-09-03 (round 38): the bankruptcy_value_cap_note covers § 522(p)'s 1,215-day cap but the more basic rule was missing -- under 11 U.S.C. § 522(b)(3)(A) a debtor domiciled in Texas for fewer than 730 days before filing cannot use Texas exemptions at all and must use the prior state's (or the federal) exemptions. A family that moved from California or Illinois 14 months ago is not 'protected up to $214,000'; it may get only the prior state's much smaller homestead figure or the federal amount. Appeared in both backlog runs.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**abandonment_and_temporary_absence_note**

ADDED 2026-09-03 (round 38): the checklist's 'actual residence' question must not be read as 'currently living there.' Texas homestead status, once established, is lost only by ABANDONMENT -- proven by clear and convincing evidence of intent not to return -- and temporary absence (a job assignment out of state, caring for a parent) or even renting the house out does not forfeit it absent acquisition of a new homestead. Conversely, acquiring a new homestead elsewhere does end protection. PINNED 2026-09-04 (round 39): the renting-out point is now statutory -- Tex. Prop. Code § 41.003 (quoted above): temporary renting 'does not change its homestead character if the homestead claimant has not acquired another homestead.' The clear-and-convincing-evidence standard for abandonment remains case law.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**form_of_ownership_note**

ADDED 2026-09-03 (round 38): neither the logic nor the checklist asked WHO holds title. Tex. Prop. Code § 41.0021 preserves the exemption for a home held in a 'qualifying trust' (settlor/beneficiary with a present possessory right to occupy rent-free -- most revocable living trusts); property titled in an LLC, corporation, or non-qualifying trust is not the debtor's homestead and is reachable.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**mechanics_lien_formalities_note**

ADDED 2026-09-03 (round 38): the 'home-improvement liens contracted in writing' exception is not self-executing. Tex. Const. art. XVI, § 50(a)(5) requires the contract to be in writing, signed by BOTH spouses if the owner is married, executed before any work is performed or material furnished, and (for homesteads) to satisfy the cooling-off and closing-location formalities; a defectively executed contract does not create an enforceable lien against the homestead. Defective execution is the most common defense in these disputes. [SOURCE PENDING: named but not live-fetched this session; screening flag, not a verified quotation.]

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**abstract_of_judgment_title_cloud_note**

ADDED 2026-09-03 (round 38): 'the homestead is exempt' does not mean an old recorded abstract of judgment is harmless -- it clouds title and title companies commonly refuse to close a sale until it is addressed. The mechanism is the homestead affidavit as release of judgment lien under Tex. Prop. Code § 52.0012 (notice to the judgment creditor, 30-day objection window). A seller should be told about this procedure, not just that the equity is protected.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**urban_rural_test_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: the 10-acre (urban) versus 100/200-acre (rural) caps turn on a STATUTORY test, not on the owner's sense of the place. Prop. Code 41.002(c): the homestead is URBAN if, when designated, it is (1) inside a municipality, its extraterritorial jurisdiction, or a platted subdivision, AND (2) served by police protection, paid or volunteer fire protection, and at least three of electric, natural gas, sewer, storm sewer, and water provided by or under contract to a municipality. Both prongs are required; a property outside city limits can still be urban if it is inside the ETJ or a platted subdivision and has the services. On a 12-acre ETJ tract with city water, sewer and electric, the homestead is 10 acres and the remaining 2 (the debtor chooses which, if severable) are reachable by a judgment creditor. Checklist item 2 rewritten to collect the 41.002(c) facts.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**lien_attached_before_homestead_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json; GLOSS-FOR-COUNSEL. Homestead protection is measured as of the time the creditor's lien ATTACHED. A judgment lien that validly attached (abstract recorded, Prop. Code 52.001 et seq.; NAMED) while the property was NON-exempt -- a rental duplex the debtor did not live in -- is not divested when the debtor later moves in and impresses homestead character; the later homestead is subject to the earlier lien. The exceptions list in this node is a list of debts that can reach a homestead; this is a different mechanism (the property was not a homestead when the lien attached). The 52.0012 affidavit route in abstract_of_judgment_title_cloud_note is for a lien that never attached because the property WAS homestead at recording; it does not clear a lien that attached first. Texas case law is consistent on the attachment-timing rule but no single statute states it; encode as a screening question and refer. Checklist item added.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. Whether the property is the debtor's actual residence and qualifies as urban or rural under § 41.002's definitions  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. Acreage, AND the Prop. Code 41.002(c) urban/rural facts: is the property inside a city, its extraterritorial jurisdiction, or a platted subdivision, and does it have police and fire protection plus at least three of municipal electric, natural gas, sewer, storm sewer, and water? If so it is URBAN and capped at 10 acres regardless of how rural it feels  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. Whether the creditor's claim is one of the enumerated exceptions (purchase-money, tax, contracted-in-writing improvement lien, etc.) rather than an ordinary unsecured debt  (dispositive)  [ ] keep  [ ] change  [ ] drop
4. Whether the homeowner is filing (or considering) bankruptcy, and if so, when the current homestead equity was acquired relative to the 1,215-day/~40-month lookback window (11 U.S.C. § 522(p) caps equity acquired in that window even though Texas state law has no cap) -- and, for the 522(p) cap, whether equity in the current home was rolled over from a PREVIOUS Texas principal residence acquired before the 1,215-day window (excluded from the cap, 522(p)(2)(B)) or is new equity added inside the window  (dispositive)  [ ] keep  [ ] change  [ ] drop
5. Whether the creditor is the IRS/federal government (federal tax liens and restitution/forfeiture judgments override the Texas homestead exemption) or a homeowners' association pursuing an assessment lien (case-specific, not a clean statutory exception)  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. If the matter is a BANKRUPTCY: how long has the debtor been domiciled in Texas? Fewer than 730 days means Texas exemptions are unavailable and the prior state's (or federal) exemptions apply (11 U.S.C. 522(b)(3)(A)) -- separate from the 1,215-day equity cap  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. If the debtor is not currently living in the home: is the absence temporary with intent to return (homestead retained), or has the debtor acquired a new homestead elsewhere (protection lost)?  (dispositive)  [ ] keep  [ ] change  [ ] drop
8. Who holds title -- the debtor individually, a revocable/qualifying trust (exempt, Prop. Code 41.0021), or an LLC/corporation/non-qualifying trust (not exempt)?  (dispositive)  [ ] keep  [ ] change  [ ] drop
9. If the claim is a home-improvement (mechanic's) lien: was the written contract signed by both spouses and executed BEFORE work began, with the art. XVI 50(a)(5) formalities? A defective contract does not create an enforceable homestead lien  (dispositive)  [ ] keep  [ ] change  [ ] drop
10. If the homeowner is trying to SELL and an abstract of judgment is recorded: has the Prop. Code 52.0012 homestead affidavit / release procedure been used to clear title?  (dispositive)  [ ] keep  [ ] change  [ ] drop
11. WHEN did the creditor's lien attach relative to when the property became the debtor's homestead? An abstract of judgment recorded while the property was a non-exempt rental (before the debtor moved in) attached to it, and the later homestead is subject to that lien -- refer (lien_attached_before_homestead_note)  (dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | Tex. Prop. Code § 41.001(a) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/PR/htm/PR.41.htm |
| 2 | Tex. Prop. Code § 41.002(a)-(b) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/PR/htm/PR.41.htm |
| 3 | 11 U.S.C. § 522(p), (o) | B | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/uscode/text/11/522 |
| 4 | 26 U.S.C. § 6321; United States v. Rodgers, 461 U.S. 677 (1983) | B | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/uscode/text/26/6321 |
| 5 | 11 U.S.C. § 522(b)(3)(A) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title11-section522&num=0&edition=prelim |
| 6 | Tex. Prop. Code § 41.0021(a)-(b) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/PR/htm/PR.41.htm |
| 7 | Tex. Prop. Code § 41.003 | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/PR/htm/PR.41.htm |
| 8 | Tex. Prop. Code § 52.0012(b)-(c) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/PR/htm/PR.52.htm |
| 9 | 11 U.S.C. § 522(p)(2)(B) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title11-section522&num=0&edition=prelim |
| 10 | Tex. Prop. Code § 41.002(c) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/PR/htm/PR.41.htm |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | yes | 730-day bankruptcy domicile rule | Note + checklist |
| 02 | FIXED-VERIFIED | yes | Abandonment vs. temporary absence | Note + checklist |
| 03 | FIXED-VERIFIED | yes | Trust / LLC title (41.0021) | Note + checklist |
| 04 | FIXED-SOURCE-NAMED | no | Mechanic's-lien formalities (art. XVI 50(a)(5)) | Note + checklist |
| 05 | FIXED-VERIFIED | no | Abstract of judgment clouds title (52.0012) | Note + checklist |
| 06 | FIXED-VERIFIED (node was WRONG) | yes | 522(p) rollover rule stated backwards | 522(p)(2)(B) pinned; bankruptcy_value_cap_note corrected; checklist |
| 07 | FIXED-VERIFIED | yes | 41.002(c) urban/rural test not encoded | 41.002(c) pinned; urban_rural_test_note; checklist item 2 rewritten |
| 08 | GLOSS-FOR-COUNSEL | yes | Lien attached before homestead character | lien_attached_before_homestead_note; checklist |

**Drafting revisions (author / date / summary):**

- 2026-08-30 — Added 11 U.S.C. § 522(p)/(o) bankruptcy value-cap and 26 U.S.C. § 6321/Rodgers federal-tax-lien-override derived_from entries; qualified the 'no dollar cap' statement with a bankruptcy caveat; added the federal tax lien exception to the exceptions list; added an explicitly-hedged HOA-lien caveat (no
- 2026-09-03 — Added bankruptcy-domicile (730-day), abandonment/temporary-absence, form-of-ownership (41.0021), mechanic's-lien formalities, and abstract-of-judgment title-cloud notes; 5 checklist questions. All 6 backlog findings (both runs) addressed; statutory text NOT pinned this session -- SOURCE PENDING.
- 2026-09-04 — Pinned 11 U.S.C. 522(b)(3)(A), Prop. Code 41.0021, 41.003, 52.0012; removed 3 SOURCE PENDING markers; temporary-absence note now statute-anchored. Mechanic's-lien formalities (Tex. Const. art. XVI 50(a)(5)) NOT pinned this session -- marker retained.
- 2026-09-05 — Round 46: 522(p)(2)(B) pinned and bankruptcy_value_cap_note corrected; 41.002(c) pinned + urban_rural_test_note + checklist item 2 rewritten; lien_attached_before_homestead_note (GLOSS) + checklist; bankruptcy checklist item extended.

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed True · material findings 3 (all dispositioned in round 46; see D)

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---
