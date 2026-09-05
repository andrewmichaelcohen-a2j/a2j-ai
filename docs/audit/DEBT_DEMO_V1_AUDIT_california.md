# DEBT-DEMO-V1.0 CENSUS AUDIT — CALIFORNIA

*Generated 2026-09-05 from the frozen v1.0 files, `stage_b_dispositions.json`, and `run_20260904T221748Z.json`. Phase LOCK item 4. Copyright 2026 Andrew M Cohen. Apache 2.0.*

Read order is the order below. Each sheet: A logic (full text), B checklist, C citations with tier and verification status, D disposition history, E sign-off. Nothing here edits v1.0; findings go to `POST_V1_BACKLOG.md`.

---

## 1. CA-SOL-WRITTEN-CONTRACT-DEBT

**Title:** California statute of limitations on a written-contract consumer-debt lawsuit  
**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `bf31aed13a348688ef06726e7d02597adbfc3cd37d5bc0612be4aefbd6f0c224`

**Reading load:** logic 2,869 words · checklist 862 · cited text 2,982 · 14 citations · 17 checklist items · 9 drafting revisions

### A. Logic (read in full; this is the content being certified)

**limitations_period_years**

4

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**applies_to**

actions on a contract/obligation founded on a written instrument -- most credit-card cardmember agreements and signed loan/retail-installment contracts

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**accrual**

Generally the date of default/breach, a fact question this node does not itself resolve -- NOT necessarily the date of last payment, though last-payment date is often used as a practical proxy and the two coincide in many cases. CORRECTED 2026-09-01 (round 34): this node's own checklist previously framed 'date of last payment' as the default answer and treated 'date of default/breach' as relevant only 'if no payments were made,' which both overstates last-payment date's reliability and contradicts this note's own fact-question hedge. On a revolving account, breach/default can postdate the last payment by weeks or months (e.g., a missed minimum payment followed by a contractual cure period, or a charge-off/acceleration event), so last-payment date should not be treated as interchangeable with the accrual date without confirming which the creditor's own records and contract terms actually establish. CAUTION: for a deficiency claim after repossession/foreclosure sale of secured collateral, accrual is frequently measured from the disposition/deficiency date, not the last payment date or breach date -- applying a flat 'last payment' or 'breach' accrual rule to a secured installment contract can understate the time remaining and produce a false 'time-barred' conclusion. Flagged as a fact-sensitive distinction this node does not fully resolve; a dedicated secured-transactions SOL node is HORIZON work.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**affirmative_bar_note**

subdivision (d) is notable and California-specific: once the period has run, a creditor is statutorily barred from even INITIATING suit or arbitration to collect -- this is stronger than a mere affirmative defense the debtor must raise, though the debtor should still plead it.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**determination**

expired_if [complaint-filing date, or today if no complaint has yet been filed] > (accrual_date + 4 years + 178 days IF (accrual_date < October 1, 2020) AND (accrual_date + 4 years >= April 6, 2020) per Cal. R. Ct. emergency rule 9(a); otherwise + 0 days -- see covid_emergency_rule_9_tolling_note for why BOTH conditions are required, not just the deadline-side one), subject to: (a) the federal-student-loan threshold question above (if yes, this node's SOL analysis does not apply at all -- there is no limitations period); (b) the bankruptcy screening question above (a discharge is a complete bar regardless of this determination; a live or recently-ended bankruptcy without discharge of this debt may extend the deadline under 11 U.S.C. 108(c) beyond what this formula alone computes); and (c) any other tolling not yet encoded (e.g., CCP 351 debtor's-absence tolling). CRITICAL: this determination is NOT the right question at all once a lawsuit has already been filed or a judgment already exists -- see filing_date_vs_today_note and judgment_enforcement_note.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**choice_of_law_note**

CORRECTED 2026-09-01 (round 34): this note and the corresponding checklist item previously required BOTH that the underlying contract designate another state's law AND that the claim arose there before CCP § 361 (California's borrowing statute) could apply -- that added requirement is not in the statute. § 361's own text requires only that 'a cause of action has arisen in another State ... and by the laws thereof an action thereon cannot there be maintained ... by reason of the lapse of time' -- i.e., the claim accrued in another state AND is already time-barred under that state's (shorter) limitations period. Nothing in the statute requires the contract to designate that state's law; a contract that is silent on choice of law, or that designates California, does not take the claim outside § 361's borrowing rule if the claim in fact arose elsewhere and is already barred there. Where the claim arose is itself a fact question (e.g., where the consumer resided and used the account when the debt was incurred/defaulted) that this node does not resolve. CLARIFIED 2026-09-03 (round 38): the round-34 correction above fixed § 361's elements but over-stated the conclusion -- a contractual choice-of-law clause is NOT irrelevant. § 361 (the borrowing statute) and a choice-of-law clause are two SEPARATE routes to a shorter period: § 361 applies where the claim AROSE elsewhere and is barred there, with or without a clause; independently, California courts have enforced a credit agreement's out-of-state choice-of-law clause to import that state's shorter limitations period even where the claim arose in California (e.g., Resurgence Financial, LLC v. Chambers (2009) 173 Cal.App.4th Supp. 1, applying Delaware's 3-year period). Because nearly every national card agreement designates DE, SD, UT, or VA law, this is the modal case. Ask BOTH questions. Resurgence is a case-law gloss (source_tier C) flagged for counsel confirmation, not live-verified this session.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**revival_note**

CORRECTED 2026-09-03 (round 38): CCP § 360 (quoted above) has TWO parts and this note previously collapsed them. (1) The general rule: no acknowledgment or promise takes a case out of the statute unless it is 'contained in some writing, signed by the party to be charged.' (2) The payment proviso -- that a payment of principal or interest stops the running of the period -- is by its terms limited to payments 'due on any promissory NOTE'; it does not on its face reach a revolving credit-card balance. So for the credit-card debt this node most often meets, a collector-solicited $50 phone payment is NOT a 'restart' under § 360's payment proviso, and any extension would have to rest on a signed writing (or on a separate open-book-account theory under § 337(b), not encoded here -- flagged). And regardless of instrument type, § 360's closing clause is explicit that 'no payment of itself shall revive a cause of action once barred' -- a payment made AFTER the period expired never revives the claim. This node previously stated flatly that any pre-expiration payment 'restarts the clock,' which overstates the proviso and, for card debt, runs in the dangerous direction (telling a consumer a stale claim is live).

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**filing_date_vs_today_note**

If a complaint has already been filed (or a default judgment already entered), the relevant comparison for whether the SUIT was timely is accrual-plus-4-years against the date the COMPLAINT WAS FILED, not against today's date. A consumer sued in 2022 on a 2019 default, who asks in 2026 whether the case is time-barred, should NOT be told the suit is expired merely because today is more than 4 years past accrual -- the suit was timely when filed in 2022, and the SOL question is now moot as to that filing (whatever other defenses may exist). Applying today's-date logic to an already-filed or already-judgment case produces a materially wrong answer.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**judgment_enforcement_note**

Once a judgment has actually been entered (including a default judgment), the ORIGINAL 4-year contract statute of limitations no longer governs anything -- the judgment itself is enforceable for 10 years from entry, renewable for additional 10-year periods without limit, under CCP § 683.020. A consumer with an old judgment against them should not be told the judgment is 'expired' or unenforceable based on the 4-year contract SOL; the judgment-enforcement clock is separate and starts over at entry (and again at each renewal). CORRECTED 2026-09-04 (round 43): the 10-years-renewable rule in CCP 683.020 governs CALIFORNIA judgments. An OUT-OF-STATE judgment a creditor is domesticating here (Sister State Money-Judgments Act, CCP 1710.10 et seq.) or suing on is different on two counts: (1) it must still be enforceable under the law of the state that rendered it -- a Texas judgment, for example, goes dormant if no writ issues within 10 years and can be revived only within 2 more (Tex. Civ. Prac. & Rem. Code 34.001, 31.006), so a 2013 Texas default judgment with no execution cannot be treated as live in 2026; some states run 20 years; (2) an independent California action on a sister-state judgment has its own 10-year limitation under CCP 337.5(b). Ask the consumer which state's court entered the judgment and when, and whether any execution or renewal ever issued there. GLOSS-FOR-COUNSEL: the proposition that the sister-state judgment must be enforceable where rendered before it can be entered here rests on full-faith-and-credit case law, not on a quoted statutory text; the 1710.40 motion to vacate is the procedural vehicle.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**installment_separate_accrual_note**

This node's single-accrual-date framing assumes the debt is due in full as of one date. For an INSTALLMENT obligation (e.g., a written personal loan or payment plan with scheduled periodic payments) where the creditor has NOT invoked an acceleration clause, California law runs the 4-year period separately on EACH missed installment as it comes due -- not from a single default or last-payment date. A creditor suing in 2026 on an installment loan where payments stopped in 2019 may still timely sue for installments that came due within the last 4 years, even though installments from 2019-2021 are barred. This node's single-accrual-date determination, applied to an unaccelerated installment obligation, would incorrectly declare the entire claim either wholly barred or wholly live rather than partially barred.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**covid_emergency_rule_9_tolling_note**

Cal. R. Ct., emergency rule 9(a) tolled ALL California civil statutes of limitations exceeding 180 days -- including this node's 4-year contract SOL -- for 178 days, from April 6, 2020 to October 1, 2020. Tolling only affects a claim whose limitations clock was actually RUNNING at some point during that window, so it requires BOTH: (1) the claim must have ACCRUED before October 1, 2020 (the day the tolling window closed) -- a claim that accrued on or after October 1, 2020 never had its clock running during the tolled window at all, so it gets ZERO additional days, no matter how the 'deadline had not already passed' test alone would read; and (2) the otherwise-applicable 4-year deadline must not have already passed before April 6, 2020 (i.e., the claim must still have been live going into the window). CORRECTED 2026-09-01 (round 32): this node's determination previously encoded only condition (2) and omitted condition (1) -- meaning ANY claim, including one that accrued well after October 2020 (e.g., a 2022 default), would trivially satisfy 'deadline had not already passed as of April 6, 2020' (there was no debt yet to have a deadline) and incorrectly receive the +178 days it was never entitled to. That error runs in the dangerous direction: it tells a creditor's target consumer a suit is timely 178 days longer than it actually is, or tells a consumer with a genuinely expired claim that it isn't. Practical range: claims that accrued roughly between mid-2016 and September 30, 2020 get the +178 days; claims accruing October 1, 2020 or later get none; claims that had already run out (accrual-plus-4-years fell before April 6, 2020) also get none, because the toll can't revive an already-dead claim.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**federal_student_loan_preemption_note**

This node's 4-year written-contract SOL does NOT apply at all to a federally-held or federally-guaranteed student loan (a Direct Loan, an FFEL loan after the guaranty agency has reimbursed the prior holder and is collecting, or a Perkins/institutional loan under 34 CFR part 674) -- 20 U.S.C. 1091a eliminates any limitations period for the enumerated federal actors' collection of such loans, including suit, judgment enforcement, offset, and garnishment. This is a THRESHOLD, case-dispositive distinction this node's checklist did not previously surface: applying the normal 4-year analysis to a federal student loan would incorrectly tell a consumer an old debt is time-barred when it is not, and it is easy to get wrong because a PRIVATE (non-federally-backed) student loan from the same borrower, same era, and same appearance to a layperson IS an ordinary written-contract debt fully subject to this node's normal 4-year SOL -- the federal/private distinction, not the mere fact that it's a 'student loan,' is what controls.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**bankruptcy_screening_note**

Bankruptcy affects this node's SOL analysis in two DIFFERENT ways that must be screened separately, not folded into the generic 'other statutory tolling' checklist item: (1) 11 U.S.C. 108(c) -- if the 4-year period had not yet run when a bankruptcy petition was filed and the automatic stay (or, for certain individual co-debtors, the section 1201/1301 stay) prevented the creditor from suing, the deadline is extended until 30 days after notice that the stay ended (case closed, dismissed, or stay otherwise lifted) -- a notice-triggered extension, not a flat number of days like Emergency Rule 9 above; and (2) 11 U.S.C. 524(a)(1)-(2) -- if the debt was actually DISCHARGED (most commonly in a completed Chapter 7 or Chapter 13 case), that is a COMPLETE, independent bar on collection regardless of the SOL: any judgment on the debt is void, and any suit or collection act is enjoined. A 'not expired' SOL determination on a debt that was actually discharged would be badly misleading -- it would suggest the consumer is exposed on a debt that in fact cannot be lawfully collected at all. The two are not interchangeable: a pending or recently-closed bankruptcy without a discharge of THIS debt calls for the section 108(c) extension analysis; a completed discharge calls for the section 524(a) bar analysis instead, and controls over any SOL conclusion this node would otherwise reach.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**scra_military_tolling_note**

ADDED 2026-09-01 (round 34): 50 U.S.C. § 3936(a) (Servicemembers Civil Relief Act) excludes the ENTIRE period of a servicemember's military service from this node's 4-year limitations period -- this is a full tolling (the clock simply does not run during service), not a fixed add-on like the Emergency Rule 9(a) COVID tolling above, and it can add years rather than months depending on the length of service. This is a THRESHOLD, case-dispositive fact this node's checklist did not previously surface: applying the ordinary 4-year analysis without asking about military service would incorrectly tell an active-duty or recently-separated servicemember-consumer (a common California population, given the state's large military presence) that a claim is time-barred when SCRA tolling in fact keeps it live. This node does not resolve exactly how much service-time to exclude in a given case -- that requires the servicemember's specific service dates.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**sol_is_an_affirmative_defense_note**

ADDED 2026-09-03 (round 38): an 'expired' output from this node does NOT make a filed lawsuit go away. The statute of limitations in California is an affirmative defense that must be raised by the defendant (by demurrer or in the answer -- CCP § 458 requires pleading the specific section); a defendant who does not appear will have a DEFAULT JUDGMENT entered on the time-barred debt, and that judgment is fully enforceable (see judgment_enforcement_note). Default is the outcome in most California consumer-debt suits. Every 'expired' answer must carry: 'you still have to file an answer and plead it.' § 337(d)'s bar on INITIATING suit is a separate protection (and a Rosenthal/1692e claim theory), but it does not self-execute in a case already filed. (CCP § 458's pleading-by-section-number requirement was NOT live-fetched this session; named-only.)

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**ccp_351_absence_tolling_caveat**

ADDED 2026-09-03 (round 38): the checklist flags CCP § 351 (tolling during the debtor's absence from California) as an open fact. Counsel should know the settled caveat: § 351 has been held unconstitutional under the dormant Commerce Clause AS APPLIED to a defendant who remained amenable to California service/long-arm jurisdiction while out of state (Abramson v. Brownstein (9th Cir. 1990) 897 F.2d 389; Heritage Marketing & Ins. Servs. v. Chrustawka (2008) 160 Cal.App.4th 754). Collectors routinely invoke § 351 against consumers who moved; the tolling argument often fails. Case-law gloss, source_tier C, flagged for counsel confirmation.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**deceased_debtor_note**

ADDED 2026-09-04 (round 43), from run_20260904T212407Z.json (a finding the runner had silently dropped; see drafting_revisions). If the DEBTOR HAS DIED, this node's 4-year computation does not govern. CCP 366.2(a): where a person dies before the applicable limitations period expires and the cause of action survives, 'an action may be commenced within one year after the date of death, and the limitations period that would have been applicable does not apply.' 366.2(b) forbids tolling or extension of that year except through the Probate Code creditor-claim procedures (Prob. Code 9000 et seq. for estates in administration; 19000 et seq. for revocable trusts). So a 2021-default card balance whose obligor died in 2023 was barred against the estate and any successor in 2024, even though accrual + 4 years would run to 2025 (plus any COVID tolling). Dangerous direction: the family would otherwise be told the claim is live. The mirror-image consumer question (the SURVIVING RELATIVE is being dunned personally for a debt only the decedent owed) is a coverage/liability question, not a limitations one -- see the FDCPA-COVERAGE node's deceased_consumer_note. GLOSS-FOR-COUNSEL: interaction of 366.2 with a timely-filed probate creditor's claim (Prob. Code 9100/9352 tolling) is not encoded.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**book_account_and_account_stated_note**

ADDED 2026-09-04 (round 43), from run_20260904T212407Z.json: 'no signed contract' does NOT mean 'oral contract, two years.' A revolving credit-card balance is routinely sued on as an OPEN BOOK ACCOUNT or an ACCOUNT STATED under CCP 337(b), each FOUR years, and the acknowledgment of an account stated 'need not be in writing.' Accrual for an account stated runs from the date of the last item. Debt buyers plead these counts precisely because the cardmember agreement is often unavailable. Do not route a card debt to the 2-year CA-SOL-ORAL node on the strength of 'I never signed anything'; the operative floor for card debt is four years on one theory or another. A consumer told 'time-barred' who therefore does not answer risks a default judgment on a live claim (see sol_is_an_affirmative_defense_note). Whether the plaintiff can PROVE a book account or account stated (records; a statement sent and not objected to) is a merits question for counsel.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. THRESHOLD: has the person who owed the debt DIED? If so, CCP 366.2 replaces this node's period: one year from the date of death, no tolling except through the Probate Code creditor-claim procedures -- obtain the date of death and whether an estate or trust administration was opened  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. Date the debt accrued (default/breach date) -- CORRECTED 2026-09-01 (round 34): do not default to 'date of last payment' as if it were interchangeable with the accrual date; on a revolving account, breach/default can postdate the last payment by weeks or months, and the two should be confirmed separately from the creditor's own records/contract terms  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. The legal theory the debt is (or would be) sued on -- not just written vs. oral: a written contract (337(a), 4 years); an OPEN BOOK ACCOUNT or ACCOUNT STATED (337(b), 4 years -- the usual theories for credit-card balances, and available even when no signed agreement can be produced); or a genuinely oral/unwritten obligation with no account records (339, 2 years -- see CA-SOL-ORAL-CONTRACT-DEBT). 'I never signed anything' does not by itself move a card debt to the 2-year period.  (dispositive)  [ ] keep  [ ] change  [ ] drop
4. Any facts suggesting tolling (e.g., debtor's absence from the state under CCP § 351, other statutory tolling) -- flagged, not resolved by this node  (dispositive)  [ ] keep  [ ] change  [ ] drop
5. Two SEPARATE questions (clarified 2026-09-03, round 38): (a) where the claim actually AROSE and whether it is already time-barred there -- CCP § 361's borrowing statute applies regardless of any choice-of-law clause; AND (b) whether the contract contains an out-of-state choice-of-law clause (DE/SD/UT/VA are typical for card agreements) whose shorter limitations period California courts may enforce on its own (Resurgence v. Chambers line). Either can shorten the 4-year period; a California-law clause does not defeat (a)  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. Whether this is a deficiency claim following repossession or foreclosure sale of secured collateral (accrual may run from the disposition/deficiency date, not last payment)  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. If any payment was made after the last default, whether it was made before or after the 4-year period had already run (only a payment made before the bar restarts the clock; one made after does not revive it without a signed written acknowledgment)  (dispositive)  [ ] keep  [ ] change  [ ] drop
8. Whether a complaint has already been filed (compare filing date, not today, to accrual + 4 years) or a judgment already entered (the governing period becomes the 10-year CCP § 683.020 enforcement/renewal period, not the original 4-year contract SOL)  (dispositive)  [ ] keep  [ ] change  [ ] drop
9. Whether the obligation is an installment contract that was never accelerated -- if so, the 4-year period runs separately on each missed installment, not from a single accrual/last-payment date  (dispositive)  [ ] keep  [ ] change  [ ] drop
10. Whether the untolled 4-year deadline (accrual date + 4 years) had not yet passed as of April 6, 2020 -- if so, Cal. R. Ct. emergency rule 9(a) adds 178 days to the deadline, which can make an apparently-expired claim timely  (dispositive)  [ ] keep  [ ] change  [ ] drop
11. Whether the loan is federally-held or federally-guaranteed (Direct Loan, FFEL after guaranty-agency assignment, or Perkins/institutional loan under agreement with the Secretary) as opposed to a privately-held student loan -- 20 U.S.C. 1091a eliminates any SOL for the former; the latter remains subject to this node's normal 4-year analysis  (dispositive)  [ ] keep  [ ] change  [ ] drop
12. Whether the consumer has filed bankruptcy on this debt, and if so, whether the debt was actually DISCHARGED (a complete bar on collection under 11 U.S.C. 524(a), regardless of SOL) as opposed to merely subject to a pending or since-lifted automatic stay without discharge of this debt (which instead triggers the 11 U.S.C. 108(c) deadline-extension analysis)  (dispositive)  [ ] keep  [ ] change  [ ] drop
13. If relying on the Emergency Rule 9(a) COVID tolling: confirm the debt's ACCRUAL DATE fell before October 1, 2020 (not just that the 4-year deadline hadn't passed by April 6, 2020) -- a debt that accrued on or after October 1, 2020 gets zero tolling days regardless of when its deadline falls  (dispositive)  [ ] keep  [ ] change  [ ] drop
14. Whether the consumer is currently, or was during any part of the relevant period, on active-duty military service -- SCRA tolling (50 U.S.C. 3936(a)) excludes the entire service period from the 4-year limitations period and can make an apparently-expired claim timely  (dispositive)  [ ] keep  [ ] change  [ ] drop
15. Whether a lawsuit has been FILED and, if so, whether the consumer has answered and pleaded the limitations defense -- an expired period does not stop a default judgment on a time-barred debt; the defense is waived if not raised  (dispositive)  [ ] keep  [ ] change  [ ] drop
16. If the consumer made any payment after default: was the obligation a promissory NOTE (where § 360's payment proviso can stop the clock) or a revolving credit-card balance (where it does not on its face apply, and only a signed writing extends the period)?  (dispositive)  [ ] keep  [ ] change  [ ] drop
17. If a JUDGMENT exists: which state's court entered it, on what date, and whether any writ of execution, renewal, or revival issued in that state -- an out-of-state judgment must still be enforceable under the rendering state's law (e.g., Texas dormancy after 10 years without a writ), and a California action on it has its own 10-year period under CCP 337.5(b); CCP 683.020's renewal rule applies to California judgments  (dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | Cal. Code Civ. Proc. § 337(a) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=337. |
| 2 | Cal. Code Civ. Proc. § 337(d) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=337. |
| 3 | Cal. Code Civ. Proc. § 361 | B | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=361. |
| 4 | Cal. Code Civ. Proc. § 360 | B | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=360. |
| 5 | Cal. Code Civ. Proc. § 683.020 | B | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=683.020. |
| 6 | Cal. R. Ct., emergency rule 9(a) (as amended May 29, 2020) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://courts.ca.gov/system/files/rules-court/20-05-28-rules-effective-20-05-29.pdf |
| 7 | 20 U.S.C. § 1091a(a)(1)-(2) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title20-section1091a&num=0&edition=prelim |
| 8 | 11 U.S.C. § 108(c) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title11-section108&num=0&edition=prelim |
| 9 | 11 U.S.C. § 524(a)(1)-(2) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title11-section524&num=0&edition=prelim |
| 10 | 50 U.S.C. § 3936(a) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title50-section3936&num=0&edition=prelim |
| 11 | Cal. Code Civ. Proc. § 366.2(a)-(b) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=366.2. |
| 12 | Cal. Code Civ. Proc. § 337(b) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=337. |
| 13 | Cal. Code Civ. Proc. § 337.5(b) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=337.5. |
| 14 | Tex. Civ. Prac. & Rem. Code § 34.001(a)-(b); § 31.006 | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://statutes.capitol.texas.gov/Docs/CP/htm/CP.34.htm |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | GLOSS-FOR-COUNSEL | yes | Round-34 choice-of-law note over-corrected (Resurgence v. Chambers) | § 361 and a choice-of-law clause are two routes; both asked now |
| 02 | FIXED-VERIFIED | yes | Revival note overstates § 360 payment proviso (promissory notes only) | § 360 quote already in node; note rewritten |
| 03 | GLOSS-FOR-COUNSEL | yes | CCP § 351 absence tolling likely unconstitutional as applied | Abramson / Heritage caveat |
| 04 | FIXED-VERIFIED | yes | "Expired" does not stop a default judgment; SOL must be pleaded | Note + checklist on all three (CCP 458 / TRCP 94) |
| 05 | FIXED-VERIFIED | yes | Deceased debtor: CCP 366.2 one-year-from-death bar not screened (finding silently dropped by runner: exposes_gap omitted) | deceased_debtor_note + threshold checklist item; 366.2(a)-(b) pinned |
| 06 | FIXED-VERIFIED | yes | 'No signed contract' routed card debt to 2-year oral period; book account / account stated (337(b), 4 years) omitted (dropped finding) | book_account_and_account_stated_note; checklist item 2 rewritten; 337(b) pinned |
| 07 | FIXED-VERIFIED + GLOSS-FOR-COUNSEL | yes | Sister-state judgment treated under CCP 683.020; rendering-state dormancy and 337.5(b) ignored (dropped finding) | judgment_enforcement_note corrected + checklist item; 337.5(b) pinned; TX 34.001/31.006 copied; enforceable-where-rendered proposition GLOSS-FOR-COUNSEL |

**Drafting revisions (author / date / summary):**

- 2026-08-30 — Added CCP § 361 borrowing-statute and § 360 revival-timing derived_from entries; added choice_of_law_note, revised accrual note to flag the secured-deficiency-judgment exception, added revival_note; added 3 corresponding checklist items.
- 2026-08-30 — Fixed 'determination' to key off the complaint's filing date (not today) once a suit has been filed, and flagged that an existing judgment is governed by CCP 683.020's 10-year enforcement/renewal period rather than the original 4-year SOL at all; added filing_date_vs_today_note, judgment_enforcement
- 2026-09-01 — Added Cal. R. Ct. emergency rule 9(a) (178-day COVID-19 tolling, automatic/universal, not a fact the consumer would report), 20 U.S.C. 1091a (federal student loan SOL preemption -- a threshold, case-dispositive distinction from privately-held student loans), and 11 U.S.C. 108(c) + 524(a) (bankruptcy
- 2026-09-01 — Fixed the Emergency Rule 9(a) COVID tolling condition, which previously granted +178 days to any claim whose deadline 'had not already passed as of April 6, 2020' -- trivially true for essentially any claim, including ones that accrued well after the tolling window closed (e.g., a 2022 default). Add
- 2026-09-01 — Added SCRA (50 U.S.C. 3936(a)) military-service tolling as a new threshold checklist question (a servicemember's entire service period is excluded from the 4-year clock). Fixed the CCP 361 choice-of-law note and checklist item, which incorrectly required the contract to designate the other state's l
- 2026-09-03 — Fixed revival_note to track § 360's actual text (payment proviso limited to promissory notes; no post-bar revival); clarified the round-34 choice-of-law note -- § 361 and a choice-of-law clause are two separate routes, both must be asked; added affirmative-defense and § 351-constitutional caveats; 2
- 2026-09-04 — Round 39: affirmative-defense note marker removed; CCP 458 remains named-only. No other change.
- 2026-09-04 — Round 41: emergency rule 9(a) entry re-pinned to the Judicial Council's May 28, 2020 amendment order PDF with manual_verification (checker cannot read PDFs). No logic change.
- 2026-09-04 — Round 43: deceased_debtor_note + threshold checklist item (366.2 pinned); book_account_and_account_stated_note + checklist item 2 rewritten (337(b) pinned); judgment_enforcement_note corrected for out-of-state judgments + checklist item (337.5(b) pinned; Texas 34.001/31.006 copied from the TX node w

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed False · material findings 0 (all dispositioned in round 46; see D)

### D2. Provisions NAMED in this node's notes but NOT pinned as citations (Cowork's word only -- treat like MANUAL rows)

- none detected

> Auditor: [ ] each named provision checked against its text, or listed for the v1.1 pinning round

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---

## 2. CA-SOL-ORAL-CONTRACT-DEBT

**Title:** California statute of limitations on an oral/unwritten-contract consumer-debt lawsuit  
**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `7859304f3a83d1d4ea8e538583a9c4f5ea8f7590493082c79b53078298b1508a`

**Reading load:** logic 892 words · checklist 306 · cited text 849 · 5 citations · 8 checklist items · 4 drafting revisions

### A. Logic (read in full; this is the content being certified)

**limitations_period_years**

2

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**applies_to**

actions on a contract/obligation NOT founded on a written instrument

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**accrual**

generally the date of default/breach -- NOT the date of last payment. CORRECTED 2026-09-05 (round 46), from run_20260904T221748Z.json: an earlier version said 'default/breach or last payment.' For an UNWRITTEN obligation a payment after default does not restart the two years: CCP 360 requires a SIGNED WRITING for any acknowledgment or new promise, and its payment proviso is limited to promissory notes (see revival_and_post_bar_payment_note and the 360 entry). A voluntary $200 payment in 2023 on a loan that defaulted in March 2021 leaves the March 2023 bar date where it was; a June 2024 suit is late. For a loan with NO agreed repayment date, see demand_loan_accrual_note.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**note**

much shorter than the 4-year written-contract period (CA-SOL-WRITTEN-CONTRACT-DEBT) -- whether a specific debt (e.g., an open-book retail account, a verbal loan between individuals) counts as written or oral is itself a threshold fact question with real consequences and is not resolved by this node.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**determination**

expired_if (complaint filing date, per CCP § 350 -- NOT today's date) > (accrual_date + 2 years), subject to any tolling not yet encoded beyond the § 351 caveat above

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**classification_note**

Credit card and other revolving retail accounts are the single most common CA consumer-debt scenario, and the mere absence of a document the consumer can locate does NOT make the debt 'oral' for SOL purposes -- such accounts are usually governed by the 4-year period under CCP § 337 (written contract, or an open book account/account stated) rather than this node's 2-year period. A consumer who cannot find a signed agreement should NOT be assumed to be under this node without confirming there is genuinely no written cardmember agreement, account terms, or running book-account record -- see CA-SOL-WRITTEN-CONTRACT-DEBT. This node is for genuinely unwritten obligations (e.g., a purely verbal personal loan). CLARIFIED 2026-09-05 (round 46): the 337(b) OPEN BOOK ACCOUNT does not require any writing -- a running ledger of charges and credits on an oral services or supply arrangement (dentist, contractor, tutor, small supplier) is the textbook book account and carries FOUR years even though the underlying agreement was oral. The two-year period in this node is for a genuinely unwritten obligation with no account record: a verbal personal loan, an oral promise to pay a fixed sum. Checklist item 3 reworded.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**tolling_note**

CCP § 351 tolls the 2-year period while the debtor is absent from California, but courts have held it unconstitutional as applied to out-of-state defendants engaged in interstate commerce, and it does not apply to corporations, limited partnerships, or nonresident motorists (Abramson v. Brownstein, 897 F.2d 389 (9th Cir. 1990)). Do NOT apply a flat day-for-day tolling add-on without confirming the debtor's absence falls within § 351's actual, constitutionally-valid scope. Bankruptcy automatic-stay tolling (11 U.S.C. § 362/108) and emergency court-order tolling are separate mechanisms, also not yet encoded here.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**revival_and_post_bar_payment_note**

ADDED 2026-09-03 (round 38): this node's accrual definition ('date of default/breach or last payment') must not be applied to a payment made AFTER the 2-year period already expired. Under CCP § 360 (quoted above) a payment does not by itself revive a barred claim, and an oral obligation is not a 'promissory note' so the payment-stops-the-clock proviso does not apply at all; only a signed writing can create a new promise. As previously encoded, a 2024 $25 phone payment on a 2019 default would have reset accrual and reported a 2025 suit as timely -- the dangerous direction.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**installment_separate_accrual_note**

ADDED 2026-09-03 (round 38): for an ORAL obligation repayable in installments (e.g. '$300 a month') that has not been accelerated, California applies continuous accrual -- each missed installment carries its own 2-year period, so installments due within 2 years of filing remain actionable even though earlier ones are barred. This node's single-accrual-date, binary expired/not-expired output would report the whole claim dead (or whole claim live) when it is partially barred. Same doctrine already noted on the written-contract node; case-law gloss, source_tier C.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**sol_is_an_affirmative_defense_note**

ADDED 2026-09-03 (round 38): an 'expired' output does NOT excuse the consumer from answering a filed suit -- the limitations defense is waived if not pleaded (CCP § 458), and a default judgment on a time-barred oral debt is fully enforceable, including by wage garnishment. Always pair 'expired' with 'you must appear and plead it.' (CCP § 458's pleading-by-section-number requirement was NOT live-fetched this session; named-only.)

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**demand_loan_accrual_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json; GLOSS-FOR-COUNSEL. The paradigm case for this node -- 'pay me back when you can' -- has no default date to accrue from. California treats an obligation with no time fixed for performance as payable on demand or within a reasonable time (Civ. Code 1657, NAMED not quoted); for a loan payable on demand the general rule is that the cause of action accrues when the loan is made or, at the latest, when demand is made and refused, and courts have refused to let a lender postpone accrual indefinitely by never demanding. The consumer-facing consequence cuts both ways: a lender who waited three years to demand may already be barred (accrual at the loan), or the clock may run from the refusal (accrual at demand). Not encoded as a rule; the checklist now collects whether a repayment date was ever agreed and when any demand was made and refused. Please confirm the accrual rule to encode.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. Date of default/breach of the oral obligation (NOT the date of last payment -- a later payment on an unwritten debt does not restart the period, CCP 360); if no repayment date was ever agreed, the date the loan was made and the date any demand was made and refused (see demand_loan_accrual_note)  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. Confirmation the underlying obligation is genuinely NOT founded on a written instrument (vs. CA-SOL-WRITTEN-CONTRACT-DEBT)  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. Whether there is genuinely no written cardmember agreement, account terms, or book-account record for this debt (vs. simply not being able to locate one) -- credit card/revolving accounts are usually 4-year written-contract debts, not 2-year oral debts -- AND whether the creditor kept a running account of charges and payments (a ledger, invoices, statements): an open book account is FOUR years under CCP 337(b) even where the underlying arrangement was oral  (dispositive)  [ ] keep  [ ] change  [ ] drop
4. Whether the debtor was absent from California after the debt accrued, AND whether that absence falls within CCP § 351's actual scope (it does not apply to interstate-commerce defendants, corporations, LPs, or nonresident motorists)  (dispositive)  [ ] keep  [ ] change  [ ] drop
5. The date the collection complaint was actually FILED (not today's date, and not the service date, which often lags filing)  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. If the consumer made a payment after default: was it BEFORE or AFTER the 2-year period had already run? A post-expiration payment does not revive the claim (§ 360); only a signed writing can  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. Whether the oral agreement called for periodic installments and, if so, whether the lender ever accelerated -- unaccelerated installments accrue separately and may be only partially barred  (dispositive)  [ ] keep  [ ] change  [ ] drop
8. Whether a lawsuit has been filed and the consumer has answered and pleaded the limitations defense -- 'expired' does not prevent a default judgment if the consumer does not appear  (dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | Cal. Code Civ. Proc. § 339(1) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=339. |
| 2 | Cal. Code Civ. Proc. § 351 | B | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=351. |
| 3 | Cal. Code Civ. Proc. § 350 | B | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=350. |
| 4 | Cal. Code Civ. Proc. § 360 | B | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=360. |
| 5 | Cal. Code Civ. Proc. § 337(b) | A | ADDED AFTER last run (round 46) -- not yet live-checked | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=337. |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | yes | "Expired" does not stop a default judgment; SOL must be pleaded | Note + checklist on all three (CCP 458 / TRCP 94) |
| 02 | FIXED-VERIFIED | yes | Post-expiration "good faith" payment treated as restarting accrual | § 360 added from sibling node's verified entry |
| 03 | GLOSS-FOR-COUNSEL | partial | Installment continuous accrual | Mirrors written node's existing note |
| 04 | GLOSS-FOR-COUNSEL (Civ. Code 1657 named) | varies | No accrual rule for a no-due-date oral loan | demand_loan_accrual_note; checklist |
| 05 | FIXED-VERIFIED (node was WRONG) | no (overstates creditor) | 'Last payment' accrual contradicts CCP 360 for unwritten debts | accrual corrected; checklist item 1 rewritten |
| 06 | FIXED-VERIFIED | yes | Open book account on an oral arrangement routed to 2 years | 337(b) pinned; classification_note clarified; checklist |

**Drafting revisions (author / date / summary):**

- 2026-08-30 — Added CCP § 351 tolling and § 350 commencement-date derived_from entries (with the § 351 constitutional-limitation caveat preserved, not presented as a clean rule); added classification_note warning against defaulting credit-card/revolving debt into this 2-year node; fixed the determination formula 
- 2026-09-03 — Added § 360 (from the sibling node's verified entry) and a post-bar-payment note; added installment continuous-accrual and affirmative-defense notes; 3 checklist questions. All 3 backlog findings (run 185148Z) addressed.
- 2026-09-04 — Round 39: affirmative-defense note marker removed; CCP 458 remains named-only. No other change.
- 2026-09-05 — Round 46: accrual corrected (default/breach only); demand_loan_accrual_note (GLOSS, Civ. Code 1657 named); 337(b) pinned + classification_note clarified; two checklist items reworded.

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed True · material findings 3 (all dispositioned in round 46; see D)

### D2. Provisions NAMED in this node's notes but NOT pinned as citations (Cowork's word only -- treat like MANUAL rows)

- (demand_loan_accrual_note) ...Code 1657, NAMED not quoted)...

> Auditor: [ ] each named provision checked against its text, or listed for the v1.1 pinning round

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---

## 3. CA-CIVIL-ANSWER-DEADLINE

**Title:** California deadline to respond to a debt-collection lawsuit summons  
**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `5817757c4f6c099a1513ae424c4a4178284b169bb23e27279202dd60d7bbfa1c`

**Reading load:** logic 1,297 words · checklist 409 · cited text 2,323 · 10 citations · 10 checklist items · 6 drafting revisions

### A. Logic (read in full; this is the content being certified)

**answer_deadline_days**

30

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**trigger**

date the summons is served on the defendant

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**consequence_of_missing**

plaintiff may apply for entry of default and then seek the relief demanded, which can include wage garnishment or other collection remedies

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**applies_to**

the general unlimited/limited civil summons form; California small claims court does not use this summons/answer mechanism (no written answer -- the defendant simply appears on the hearing date) -- that is a separate, not-yet-built node.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**determination**

answer_due_date = date_of_service + 30 days

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**service_method_note**

The 30-day answer period runs from when service is DEEMED COMPLETE, which depends on the method: personal service is complete on the date of delivery, but substituted service (CCP § 415.20 -- leaving papers with a competent household member/co-worker plus a follow-up mailing) and out-of-state mail service (§ 415.40) are deemed complete 10 days AFTER the mailing. Service by publication (§ 415.50) is deemed complete per Government Code § 6064, not per a day-count stated in § 415.50 itself -- CORRECTED 2026-09-02 (round 36): this note previously asserted a flat '28th day after first publication' rule as if it were § 415.50's own text; that figure is a commonly cited functional result of Govt. Code § 6064's four-successive-week requirement in CA practice guides, but could not be independently re-verified against Govt. Code § 6064's primary text this round (see publication_completion_note) -- do not treat it as confirmed without a fresh fetch. Using the raw date papers were handed over (rather than the deemed-complete date) for substituted/mail/publication service UNDERSTATES the true deadline regardless.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**defective_service_alternative_note**

'File an answer' is not the only possible response, and is the WRONG one if the defendant disputes that service or personal jurisdiction were proper (e.g., papers left with someone at an address the defendant doesn't live at, or served on the wrong person). Such a defendant should instead move to quash service under CCP § 418.10 -- a special appearance that preserves the objection. Filing an answer first is a general appearance that WAIVES the service/jurisdiction defense entirely, even if the underlying service really was defective.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**publication_completion_note**

ADDED 2026-09-02 (round 36): service-by-publication's completion date is NOT stated directly in CCP § 415.50 -- that section cross-references Government Code § 6064's four-successive-week publication requirement. This node's prior encoding stated a specific '28th day after first publication' figure as if it came straight from § 415.50; that figure could not be independently re-verified against Government Code § 6064's primary text this round (repeated fetch timeouts). Treat the exact completion date for a publication-service case as UNVERIFIED pending a fresh fetch of Govt. Code § 6064, not as a confirmed 28-day rule.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**notice_and_acknowledgment_service_note**

ADDED 2026-09-03 (round 38): the service-method list omitted CCP § 415.30 -- in-state MAIL service with a Notice and Acknowledgment of Receipt (form POS-015), a routine low-cost method in consumer-debt cases. Under § 415.30(c) service is complete only on the date the defendant SIGNS and returns the acknowledgment; if it is never signed and returned, NO service has occurred and no answer clock starts (the plaintiff must serve another way). As encoded, the rule would start a 30-day clock from the postmark and tell an unserved defendant she is on a deadline or in default -- and filing an answer in that posture is a general appearance that forfeits the § 418.10 motion-to-quash route. Appeared in both backlog runs.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**past_deadline_before_default_note**

ADDED 2026-09-03 (round 38): the node computed only the forward-looking deadline and said missing it means the plaintiff 'may apply for entry of default.' For the very common caller who is ALREADY past day 30: an answer filed at any time before default is actually ENTERED is accepted and defeats the default request (CCP § 585 -- the clerk cannot enter default while an answer is on file); after entry, CCP § 473(b) allows relief for mistake/inadvertence/excusable neglect within six months, and §§ 473(d)/473.5 for void judgments or lack of actual notice. As encoded the rule read as though the door had closed. Appeared in both backlog runs.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**filing_fee_and_fee_waiver_note**

ADDED 2026-09-03 (round 38): a timely answer is rejected by the clerk unless it is accompanied by the first-appearance fee (Gov. Code §§ 70611, 70613 -- several hundred dollars, varying with limited/unlimited jurisdiction and amount) OR a fee-waiver application (form FW-001, Gov. Code § 68631) filed with it. A rejected answer does not stop default. For the low-income defendants who are this node's core audience, 'file by day 30' without 'with the fee or a fee waiver' can still produce the default the node warns about. [SOURCE PENDING: named but not live-fetched this session; screening flag, not a verified quotation.]

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**motion_to_quash_suspends_answer_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: a TIMELY 418.10 motion to quash (filed on or before the last day to plead) changes the deadline arithmetic. Under 418.10(b) the defendant's time to plead is extended until 15 days after service of written notice of entry of the order DENYING the motion (plus up to 20 more days for good cause), and under 418.10(d) no default may be entered before that time expires. So the defendant who filed on day 25 does not also have to answer by day 30; she answers within 15 days after the denial is noticed -- or, if she seeks writ review under 418.10(c), within 10 days after notice of the final judgment in the mandate proceeding. If the motion is GRANTED, service is quashed and the 30-day clock has not started; the plaintiff must serve again. Two traps: (i) the motion must be filed within the time to plead -- filed on day 35 it is untimely and the default risk is live; (ii) filing an answer or demurrer WITHOUT the motion (or before it) waives the service and jurisdiction objections (418.10(e)(3)). Checklist item added.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**answer_content_affirmative_defenses_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json, DANGEROUS DIRECTION: filing an answer on time is necessary, not sufficient. Under CCP 431.30(b)(2) (NAMED, not quoted this round) the answer must state 'any new matter constituting a defense,' and an affirmative defense not pleaded is waived -- the STATUTE OF LIMITATIONS above all (CCP 458 governs how it is pleaded; NAMED). A defendant sued by a debt buyer on a card whose last payment was seven years ago who files a bare general denial (PLD-050, no affirmative defenses listed) on day 28 has answered on time and thrown away the winning defense; the case proceeds to a judgment on a stale debt. The answer should plead, at minimum: statute of limitations (citing the section -- CCP 337 or 339), lack of standing/assignment (debt buyer cannot prove the chain of title), payment, failure to state a cause of action, and, where the facts fit, identity theft and the Rosenthal Act as a cross-claim. Judicial Council form PLD-050 has an affirmative-defenses section; use it. Route the limitations analysis itself to CA-SOL-WRITTEN-CONTRACT-DEBT / CA-SOL-ORAL-CONTRACT-DEBT, whose sol_is_an_affirmative_defense_note says the same thing from the other side. Checklist item added.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**demurrer_and_motion_to_strike_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: the node's universe of responses was 'answer' or 'motion to quash.' A DEMURRER (CCP 430.10; NAMED) or a MOTION TO STRIKE (435-436; NAMED) filed within the 30 days is itself a timely responsive pleading that stops the default clock -- the defendant need not also answer. If the demurrer is overruled, the time to answer runs from notice of the ruling: CCP 472a(b) (NAMED) provides that the court fixes the time, and in its absence the answer is due within 10 days after service of notice of the ruling. Debt-buyer complaints pleading a common count with no account documents, no assignment, and no date of last payment are routinely demurrable, and legal-aid defendants use the demurrer to force the plaintiff to plead facts. A defendant who demurs on day 27 has not defaulted on day 30. Checklist item added. All three sections FIXED-SOURCE-NAMED pending a fetch round.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. Date the summons and complaint were actually served on the defendant (not the filing date)  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. Whether the case is general civil (this node applies) vs. small claims (different procedure, not this node)  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. The method of service used (personal, substituted, mail, or publication) -- the 30-day period runs from the date service is DEEMED COMPLETE under that method, which can be 10-28 days after the physical service/mailing date for anything other than personal service  (dispositive)  [ ] keep  [ ] change  [ ] drop
4. Whether the defendant disputes that service was properly made or that the court has personal jurisdiction over them -- if so, the correct response is a motion to quash (CCP § 418.10), not an answer, since answering first waives the objection  (dispositive)  [ ] keep  [ ] change  [ ] drop
5. HOW was the defendant served -- personally, by substituted service, by out-of-state mail, by publication, or by in-state mail with a Notice and Acknowledgment of Receipt (CCP 415.30)? If the latter and the acknowledgment was never signed and returned, service is not complete and no deadline is running  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. If the 30 days have ALREADY passed: has default actually been ENTERED by the clerk? If not, an answer filed now still defeats the default (CCP 585); if so, is it within six months for § 473(b) relief?  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. Whether the defendant can pay the first-appearance filing fee or needs a fee waiver (FW-001) filed WITH the answer -- an answer submitted without either is rejected and does not stop default  (dispositive)  [ ] keep  [ ] change  [ ] drop
8. If a 418.10 MOTION TO QUASH was filed within the 30 days: the date of the order on it and of any written notice of entry -- a timely motion suspends the time to answer until 15 days after notice of DENIAL (418.10(b)) and bars default meanwhile (418.10(d)); if GRANTED, the clock never started  (dispositive)  [ ] keep  [ ] change  [ ] drop
9. If an ANSWER was or will be filed: does it PLEAD the statute of limitations and the other affirmative defenses (standing/assignment, payment, identity theft)? An unpleaded affirmative defense is waived (CCP 431.30(b)(2)); a timely bare denial on a stale debt is a timely surrender  (dispositive)  [ ] keep  [ ] change  [ ] drop
10. Was a DEMURRER or MOTION TO STRIKE filed within the 30 days instead of an answer? It is a timely response; if overruled, the answer is due within the time the court sets or 10 days after notice of the ruling (CCP 472a(b)), not by the original day 30  (dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | Cal. Code Civ. Proc. § 412.20(a)(3)-(4) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=412.20. |
| 2 | Cal. Code Civ. Proc. § 412.20(a)(6) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=412.20. |
| 3 | Cal. Code Civ. Proc. § 418.10 | B | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=418.10. |
| 4 | Cal. Code Civ. Proc. § 415.20(a) | B | MANUAL (note recorded; not yet re-confirmed by Andy) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=415.20. |
| 5 | Cal. Code Civ. Proc. § 415.40 | B | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=415.40. |
| 6 | Cal. Code Civ. Proc. § 415.50(c) | B | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=415.50. |
| 7 | Cal. Code Civ. Proc. § 415.30(c)-(d) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=415.30. |
| 8 | Cal. Code Civ. Proc. § 585(a) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=585. |
| 9 | Cal. Code Civ. Proc. § 473(b) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=473. |
| 10 | Cal. Code Civ. Proc. § 418.10(b), (d) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=418.10. |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | yes | § 415.30 notice-and-acknowledgment service omitted | Note + checklist |
| 02 | FIXED-VERIFIED | yes | Late answer before default entered still works (585 / 473(b)) | Note + checklist |
| 03 | FIXED-SOURCE-NAMED | yes | Filing fee / fee waiver required with answer | Note + checklist |
| 04 | FIXED-VERIFIED | yes | 418.10 motion's suspension of the answer deadline not stated | 418.10(b) pinned ((d) named); motion_to_quash_suspends_answer_note; checklist |
| 05 | FIXED-SOURCE-NAMED (CCP 431.30(b)(2), 458) | yes | Answer content -- unpleaded affirmative defenses (SOL) waived | answer_content_affirmative_defenses_note; checklist |
| 06 | FIXED-SOURCE-NAMED (CCP 430.10, 435-436, 472a(b)) | yes | Demurrer / motion to strike as timely responses omitted | demurrer_and_motion_to_strike_note; checklist |

**Drafting revisions (author / date / summary):**

- 2026-08-30 — Added CCP §§ 415.20/415.40/415.50 service-completion-date rules and § 418.10 motion-to-quash alternative (with the general-appearance waiver risk of answering first); added 2 checklist items.
- 2026-09-02 — Split the merged 3-citation entry into 3 clean, independently-cited entries. §415.20 re-verified and confirmed verbatim. §415.40 label removed but not independently re-verified this round (flagged). §415.50 corrected to its actual text (cross-references Govt. Code §6064 rather than stating a day-cou
- 2026-09-02 — Re-pinned 415.20 and 415.50 urls back to leginfo (runner-fetchable); verification provenance kept in tier_rationale.
- 2026-09-03 — Added notice-and-acknowledgment service (415.30), past-deadline-before-default (585/473(b)), and filing-fee/fee-waiver notes; 3 checklist questions. All 5 backlog findings (both runs) addressed; text NOT pinned this session -- SOURCE PENDING.
- 2026-09-04 — Pinned CCP 415.30(c)-(d), 585(a), 473(b); manual_verification on 415.20 (leginfo multi-version page). Filing-fee/fee-waiver (Gov. Code 70611/68631) NOT pinned -- marker retained.
- 2026-09-05 — Round 46: 418.10(b) pinned ((d) named) + motion_to_quash_suspends_answer_note + checklist; answer_content_affirmative_defenses_note (431.30(b)(2), 458 NAMED) + checklist; demurrer_and_motion_to_strike_note (430.10, 435-436, 472a(b) NAMED) + checklist.

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed True · material findings 3 (all dispositioned in round 46; see D)

### D2. Provisions NAMED in this node's notes but NOT pinned as citations (Cowork's word only -- treat like MANUAL rows)

- (filing_fee_and_fee_waiver_note) ...[SOURCE PENDING: named but not live-fetched this session...
- (answer_content_affirmative_defenses_note) ...30(b)(2) (NAMED, not quoted this round) the answer must state 'any new matter constituting a defense,' and an affirmative defense not pleaded is waived -- the STATUTE OF LIMITATIONS above all (CCP 458 governs how it is p...
- (answer_content_affirmative_defenses_note) ...NAMED)...
- (demurrer_and_motion_to_strike_note) ...NAMED) or a MOTION TO STRIKE (435-436...
- (demurrer_and_motion_to_strike_note) ...NAMED) filed within the 30 days is itself a timely responsive pleading that stops the default clock -- the defendant need not also answer...
- (demurrer_and_motion_to_strike_note) ...If the demurrer is overruled, the time to answer runs from notice of the ruling: CCP 472a(b) (NAMED) provides that the court fixes the time, and in its absence the answer is due within 10 days after service of notice of ...
- (demurrer_and_motion_to_strike_note) ...All three sections FIXED-SOURCE-NAMED pending a fetch round...

> Auditor: [ ] each named provision checked against its text, or listed for the v1.1 pinning round

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---

## 4. CA-WAGE-GARNISHMENT-LIMIT

**Title:** California cap on wage garnishment for a consumer-debt judgment  
**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `69085c123dbefae08ca88bffefb7cafa18fa2936fbac52462d222601bfeb846b`

**Reading load:** logic 951 words · checklist 317 · cited text 961 · 5 citations · 7 checklist items · 3 drafting revisions

### A. Logic (read in full; this is the content being certified)

**formula**

min(20% of weekly disposable earnings, 40% of (weekly disposable earnings - 48 x applicable minimum hourly wage))

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**applicable_minimum_wage**

the greater of the state minimum hourly wage or a higher local minimum wage where the debtor works, in effect when earnings are payable

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**effective_date**

2023-09-01 -- this is CA's post-SB 1477 formula, materially more debtor-protective than the pre-2023 25%-of-disposable-earnings federal-conforming formula and more protective than the federal CCPA floor

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**note_needs_current_figure**

this node encodes the FORMULA verbatim; it does NOT itself contain the current state or local minimum-hourly-wage figure needed to compute a dollar result -- that figure changes periodically (state minimum wage schedule, and per-locality ordinances) and must be pulled current at time of use, not hardcoded here.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**determination**

max_weekly_garnishment = the lesser of the two prongs above; anything withheld beyond that is unlawful

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**pay_period_conversion_note**

ADDED 2026-09-03 (round 38): the formula is stated in WEEKLY terms (48 x the applicable minimum wage), but most California employees are paid biweekly, semimonthly, or monthly. CCP § 706.050(b) (quoted above) sets the multipliers itself: multiply the applicable hourly minimum wage by 96 hours (biweekly), 104 hours (semimonthly), or 208 hours (monthly) in place of the weekly 48. CORRECTED 2026-09-04 (round 39): round 38 wrongly said the Judicial Council prescribes these. Applying the weekly subtrahend to a monthly paycheck understates the exempt floor and overstates lawful withholding by a large margin. The checklist previously marked pay period NON-dispositive; it is fully dispositive to the dollar result. Appeared in both backlog runs.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**support_order_priority_note**

ADDED 2026-09-03 (round 38): where a child- or spousal-support withholding order or wage assignment is already in place, it has PRIORITY and the consumer-debt earnings withholding order is subordinated (CCP §§ 706.030-706.031, 706.052) so that combined withholding stays within the cap -- often leaving little or nothing for the consumer creditor. The node previously computed the consumer creditor's amount off unreduced disposable earnings. Appeared in both backlog runs.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**necessaries_exemption_and_claim_procedure_note**

ADDED 2026-09-03 (round 38): the formula result is a CEILING, not the amount that will lawfully be taken. CCP § 706.051 exempts earnings 'necessary for the support of the judgment debtor or the judgment debtor's family,' and the § 706.105 claim-of-exemption procedure lets the debtor obtain a reduction below the formula amount or to zero. For the low-income single parent who is this node's typical user, the determination's 'anything withheld beyond that is unlawful' framing omitted her principal remedy. Appeared in both backlog runs. PINNED 2026-09-04 (round 39): § 706.051 is quoted above; note its exceptions -- the necessaries exemption is NOT available against a support withholding order, a state tax order, or a debt for an employee's personal services.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**disposable_earnings_definition_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: 'disposable earnings' is a DEFINED term -- CCP 706.011(a): earnings 'after deducting all amounts required to be withheld by law.' That is federal and state income tax, Social Security/Medicare, SDI, and mandatory public-retirement contributions. It is NOT net take-home pay. Voluntary deductions -- health and dental premiums, 401(k)/403(b) elective deferrals, union dues, charitable payroll deductions, a voluntary wage assignment, garnishment for another debt -- stay IN disposable earnings. A worker whose paystub shows $780 gross and $612 net after taxes, SDI, health premium and a 401(k) contribution has disposable earnings of $780 minus only the taxes and SDI; plugging in $612 understates what the creditor may take and can lead the consumer to challenge a lawful withholding or, worse, to accept an unlawful one computed by the employer on the wrong base. Checklist item 1 reworded to collect gross and each deduction.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**independent_contractor_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: the 20%/40% cap in 706.050 protects EARNINGS, defined as compensation 'payable by an employer to an employee' (706.011(b)), with 'employee' meaning a person whose employer controls 'both what shall be done and how it shall be done' (706.011(e)). A 1099 gig or rideshare worker's payments from a platform are, on the platform's own characterization, not employee earnings; a judgment creditor reaches them by a levy on the account receivable (writ of execution, CCP 699.510 et seq.; NAMED) or by an assignment order, and the earnings-withholding cap does not apply. Two escape routes to ask about: (i) misclassification -- if the worker is in fact an employee under the control test (or under Labor Code 2775's ABC test, NAMED), the cap applies and the levy was improper; (ii) the 704.220 minimum-basic-standard exemption and the 703.115/704.070 exemptions may still protect the funds once deposited (see CA-BANK-ACCOUNT-EXEMPTION). Dangerous direction as encoded: the node would have told a contractor that 75% of the platform payout is 'protected'. Checklist item added.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**federal_and_tax_garnishment_priority_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: the determination's 'anything withheld beyond that is unlawful' and the support-order carve-out are not the whole priority picture. Three families of withholding sit OUTSIDE the 706.050 cap and ahead of a consumer earnings withholding order: (1) federal ADMINISTRATIVE wage garnishment for defaulted federal student loans, up to 15% of disposable pay without a court judgment (20 U.S.C. 1095a(a)(1); NAMED, not quoted this round) and other federal agency debts (31 U.S.C. 3720D); (2) IRS levies on wages (26 U.S.C. 6331, with the 6334(d) exempt-amount table) and FTB earnings withholding orders for taxes (CCP 706.070-706.084, which have their own 25%/higher limits); (3) support orders (already noted). Where one of these is already in place, the consumer creditor's order is stacked behind it and may be reduced or deferred rather than 'unlawful' -- CCP 706.023 governs priority among orders (NAMED). The consumer-facing risk in the finding is real: a debtor already paying 15% under a Department of Education AWG who is told a further 20% is 'unlawful' may refuse to comply with a lawful stacked order. Checklist item added. All three families are FIXED-SOURCE-NAMED pending a fetch round.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. Debtor's weekly GROSS earnings and each payroll deduction, labeled MANDATORY (federal/state income tax, Social Security/Medicare, SDI, mandatory retirement) or VOLUNTARY (health/dental premium, 401(k), union dues, wage assignment, other garnishment) -- 'disposable earnings' under CCP 706.011(a) is gross minus the MANDATORY ones only; do not use net take-home  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. Current state minimum hourly wage, and any higher local minimum wage applicable where the debtor works, in effect at the time earnings are payable  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. Pay period (this node states the weekly formula; CCP § 706.050(b) has multiplier conversions for daily/biweekly/semimonthly/monthly periods not yet separately encoded) -- CORRECTED 2026-09-03 (round 38): DISPOSITIVE; the weekly 48x-minimum-wage subtrahend must be converted with the § 706.050(b) multipliers for biweekly/semimonthly/monthly pay  (dispositive)  [ ] keep  [ ] change  [ ] drop
4. Whether any child-support or spousal-support withholding order or wage assignment is ALREADY in effect against these earnings -- it has priority and reduces (often to zero) what the consumer creditor may take (CCP 706.030/706.031/706.052)  (dispositive)  [ ] keep  [ ] change  [ ] drop
5. Whether the debtor needs the earnings for the support of self or family -- the § 706.051 necessaries exemption and the § 706.105 claim-of-exemption procedure can reduce withholding BELOW the formula amount; the formula is a ceiling, not the answer  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. Is the debtor a W-2 EMPLOYEE (employer controls what is done and how, CCP 706.011(e)) or a 1099 independent contractor / gig worker? The 706.050 cap applies only to employee earnings; contractor receivables are reached by levy without the cap (unless the worker is misclassified) -- route to the bank-account exemption node for deposited funds  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. Is any OTHER withholding already in place -- federal student-loan administrative wage garnishment (up to 15%, no judgment needed), an IRS wage levy, an FTB tax withholding order, or a support order? These sit outside the 706.050 cap and ahead of a consumer creditor's order; the consumer order is stacked or reduced, not 'unlawful'  (dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | Cal. Code Civ. Proc. § 706.050(a) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=706.050. |
| 2 | Cal. Code Civ. Proc. § 706.050(c) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=706.050. |
| 3 | Cal. Code Civ. Proc. § 706.050(b) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=706.050. |
| 4 | Cal. Code Civ. Proc. § 706.051(b)-(c) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=706.051. |
| 5 | Cal. Code Civ. Proc. § 706.011(a), (b), (e) | A | ADDED AFTER last run (round 46) -- not yet live-checked | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=706.011. |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | yes | Weekly formula applied to biweekly/monthly pay; pay period marked non-dispositive | 706.050(b) note; pay period now dispositive |
| 02 | FIXED-VERIFIED | no (overstates creditor) | Support-order priority ignored (706.030/.031/.052) | Note + checklist |
| 03 | FIXED-VERIFIED | yes | Necessaries exemption / claim procedure omitted (706.051/.105) | Note + checklist |
| 04 | FIXED-VERIFIED | varies | 'Disposable earnings' undefined; net pay used | 706.011(a) pinned; disposable_earnings_definition_note; checklist item 1 rewritten |
| 05 | FIXED-VERIFIED | yes | Independent-contractor receivables treated as capped earnings | 706.011(b) pinned ((e) named); independent_contractor_note; checklist |
| 06 | FIXED-SOURCE-NAMED (20 U.S.C. 1095a; 26 U.S.C. 6331; CCP 706.070-.084, 706.023) | no | Federal AWG / IRS / FTB withholding priority omitted | federal_and_tax_garnishment_priority_note; checklist |

**Drafting revisions (author / date / summary):**

- 2026-09-03 — Added pay-period conversion (706.050(b)), support-order priority, and necessaries/claim-of-exemption notes; made pay period dispositive; 2 checklist questions. All 3 backlog findings (both runs, identical) addressed; text NOT pinned this session -- SOURCE PENDING.
- 2026-09-04 — Pinned CCP 706.050(b) (statutory multipliers -- correcting round 38) and 706.051(b)-(c). 706.030/.031/.052 (support priority) and 706.105 (claim procedure) NOT pinned -- named-only.
- 2026-09-05 — Round 46: 706.011(a)-(b) pinned; disposable_earnings_definition_note + checklist item 1 rewritten; independent_contractor_note + checklist; federal_and_tax_garnishment_priority_note (1095a, 3720D, 6331/6334, CCP 706.070-.084, 706.023 NAMED) + checklist.

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed True · material findings 3 (all dispositioned in round 46; see D)

### D2. Provisions NAMED in this node's notes but NOT pinned as citations (Cowork's word only -- treat like MANUAL rows)

- (independent_contractor_note) ...NAMED) or by an assignment order, and the earnings-withholding cap does not apply...
- (independent_contractor_note) ...Two escape routes to ask about: (i) misclassification -- if the worker is in fact an employee under the control test (or under Labor Code 2775's ABC test, NAMED), the cap applies and the levy was improper...
- (federal_and_tax_garnishment_priority_note) ...NAMED, not quoted this round) and other federal agency debts (31 U...
- (federal_and_tax_garnishment_priority_note) ...023 governs priority among orders (NAMED)...
- (federal_and_tax_garnishment_priority_note) ...All three families are FIXED-SOURCE-NAMED pending a fetch round...

> Auditor: [ ] each named provision checked against its text, or listed for the v1.1 pinning round

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---

## 5. CA-BANK-ACCOUNT-EXEMPTION

**Title:** California automatic exemption for a minimum amount in a debtor's bank account  
**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `2a1c93b9de5f25fe11a20c05d7227e6a7e77477bde592360802dc3a7612d338c`

**Reading load:** logic 1,316 words · checklist 520 · cited text 1,582 · 7 citations · 14 checklist items · 6 drafting revisions

### A. Logic (read in full; this is the content being certified)

**exemption_basis**

tied to the Welfare & Institutions Code §11452 'minimum basic standard of adequate care for a family of four, Region 1' figure, as annually adjusted under §11453

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**note_needs_current_figure**

this node encodes the FORMULA and cross-reference verbatim; the actual current dollar figure lives in Welfare & Institutions Code §11452/§11453, which this session did NOT independently pull -- must be looked up current at time of use, not assumed or hardcoded.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**automatic**

applies without the debtor filing a claim

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**exceptions**

does not apply to a levy to satisfy a judgment for wages owed, child support, or spousal support

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**determination**

money in the debtor's deposit account up to the current W&IC §11452/§11453 figure is automatically protected from an ordinary judgment-creditor levy (not from the carved-out wages/support judgment categories)

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**public_benefits_note**

If the levied account receives DIRECTLY DEPOSITED public benefits or Social Security payments, CCP § 704.080 provides a SEPARATE, larger automatic exemption specific to those funds (roughly $1,750-$2,600 for public benefits, $3,500-$5,250 for Social Security, depending on number of depositors, as most recently adjusted) -- this is in addition to, not instead of, the general § 704.220 minimum this node otherwise encodes. Federal law (31 C.F.R. Part 212) separately requires banks to automatically protect roughly two months' worth of certain federal benefit payments received by direct deposit, independent of any state exemption claim -- flagged as a related federal protection not yet independently encoded here.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**aggregation_note**

The § 704.220 automatic minimum exemption is a SINGLE aggregate amount across all of the judgment debtor's deposit accounts subject to levy, not a separate exemption per account. A debtor with multiple accounts levied at once (or in sequence) does not get the minimum multiplied by the number of accounts. CLARIFIED 2026-09-05 (round 46), from run_20260904T221748Z.json: 'or in sequence' above refers to a single enforcement effort against several accounts. It does NOT mean the debtor gets one lifetime minimum: 704.220 exempts money in the deposit account 'up to' the figure at the time of EACH levy, so a creditor who captured the non-exempt balance in February and levies the replenished account again in June faces the exemption again in June. A consumer told 'you already used your exemption' should be told that is wrong.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**natural_person_note**

This exemption -- and the CCP § 704 series generally -- is available only to a natural person (CCP § 703.020(a)). An LLC, corporation, partnership, or other entity judgment debtor has no automatic minimum-balance protection under this node.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**recent_wages_note**

If the levied funds are traceable to wages actually PAID to the debtor within the 30 days before levy, CCP § 704.070 separately exempts 75% of those paid earnings (100% if they were already subject to a wage withholding or support-assignment order before payment) -- this is typically far more protection than the § 704.220 automatic minimum alone, and is the most common real-world bank-levy scenario (a recent paycheck). This exemption requires a timely-filed claim, unlike the automatic § 704.220/§ 704.080 minimums.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**support_need_note**

On a filed claim, CCP § 704.225 exempts deposit-account money ABOVE the automatic minimum to the extent necessary for the support of the debtor and their spouse/dependents -- no fixed dollar cap, fact-specific. This is the routine follow-on claim once the automatic minimum is exhausted; this node should not be read to imply everything above the automatic minimum is unprotected.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**joint_account_note**

This node treats the levied account as simply 'the debtor's deposit account.' If the account is jointly held with a non-debtor (a spouse, family member, or other co-owner) and some or all of the funds are traceable to the co-owner's deposits, the co-owner may assert a third-party claim of ownership under CCP §§ 720.110 et seq. to recover funds that are not the debtor's -- separately, community-property rules can affect a non-debtor spouse's share differently. This node does not itself perform an ownership/tracing analysis. CORRECTED 2026-09-05 (round 46), from run_20260904T221748Z.json: for a MARRIED debtor the 720.110 third-party-claim route in this note is the wrong first answer. Under Family Code 910 (NAMED, not quoted this round) the community estate is liable for a debt incurred by either spouse during marriage (and, with exceptions, before), so wages of the debtor spouse deposited into an account in the NON-DEBTOR spouse's sole name are community property and reachable on a judgment against the debtor spouse alone -- the non-debtor spouse cannot recover them merely because the account is hers. The 704.220 minimum still applies to the levied account; CCP 703.020(b)(2) lets the non-debtor spouse claim community-property exemptions; and Family Code 911 (NAMED) shields the non-debtor spouse's OWN earnings from the other spouse's PREMARITAL debts if kept in an account the debtor spouse has no right to withdraw from. Ask when the debt was incurred relative to the marriage, whose earnings are in the account, and who can withdraw. GLOSS-FOR-COUNSEL on the Fam. Code 910/911 interplay.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**claim_of_exemption_deadline_note**

ADDED 2026-09-03 (round 38) -- THE MOST CONSEQUENTIAL PRACTICAL FACT in a bank-levy matter: the § 704.070 (recent wages) and § 704.225 (support-needed) protections this node conditions on a 'timely-filed claim' have a deadline the node never stated -- a claim of exemption (with financial statement where required) filed with the levying officer within 15 days after the notice of levy is personally served, or 20 days if served by mail (CCP § 703.520(a), quoted above -- CORRECTED 2026-09-04, round 39: NOT 10 days as the Stage B finding and the round-38 note said); for a 'personal debt' § 703.520(c) permits a later claim, but the officer may release the funds after day 20, followed by the creditor's 10-day opposition window (§ 703.550) and a hearing. A debtor who files three weeks later has forfeited the largest protections available. Only the § 704.220 minimum and directly-deposited § 704.080 benefits are protected without a claim. Appeared in both backlog runs.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**administrative_tax_levies_note**

ADDED 2026-09-03 (round 38): this node assumes a private judgment creditor. An IRS notice of levy (IRC § 6331; § 6334 provides no bank-account exemption), a Franchise Tax Board order to withhold (R&TC § 18670 et seq.), or federal administrative garnishment for defaulted student loans is NOT enforcement of a money judgment, and the CCP § 704 exemption scheme and claim procedure do not apply in the same way. Telling such a debtor the § 704.220 minimum is 'automatically protected' is wrong. Appeared in both backlog runs.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**other_traceable_exempt_deposits_note**

ADDED 2026-09-03 (round 38): the node encodes tracing protection only for directly-deposited public benefits/Social Security (§ 704.080) and recent wages (§ 704.070). Other exempt sources remain exempt after deposit to the extent traceable, several at 100%: private retirement plan and IRA funds (CCP § 704.115(b)-(d), plus ERISA anti-alienation), unemployment and disability benefits (§§ 704.120, 704.130), workers' compensation (§ 704.160), and personal-injury/wrongful-death proceeds (§§ 704.140-704.150). A retiree living on a private pension was told only the small automatic minimum applied when nearly the whole balance may be exempt. Appeared in both backlog runs.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**bank_setoff_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: the 704.220 minimum protects deposits from a judgment creditor's LEVY under the Enforcement of Judgments Law (CCP 703.010 limits the chapter to enforcement of money judgments; NAMED). It does not govern the depositary bank's own contractual or common-law right of SETOFF against a delinquent debt the customer owes that same bank -- the Wells Fargo checking account swept for the Wells Fargo card balance, before any lawsuit. The statute that does limit setoff is Financial Code 864 (NAMED, not fetched this round): as generally described, a bank may not set off against a consumer deposit account if the setoff would leave less than a stated floor (historically $1,000) and must give notice; it also prohibits setoff against directly-deposited public benefits and Social Security. The consumer with a swept account should be routed to Fin. Code 864 and to the deposit agreement, not told 704.220 was violated. GLOSS-FOR-COUNSEL on current Fin. Code 864 figures and on whether a setoff that violates 864 supports damages. Checklist item added.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. Current dollar amount of the W&IC §11452 'minimum basic standard of adequate care, Region 1, family of four' figure as most recently adjusted under §11453 -- NOT pulled this session  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. Whether the underlying judgment being levied is an ordinary debt judgment (exemption applies) vs. a wages/child-support/spousal-support judgment (carve-out, exemption does not apply)  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. Whether the debtor holds multiple accounts at one or more institutions (CCP § 704.220(e) has aggregation/allocation rules not separately encoded here)  (non-dispositive)  [ ] keep  [ ] change  [ ] drop
4. Whether the levied account receives directly-deposited public benefits or Social Security payments (a separate, typically larger exemption under CCP § 704.080 applies in addition to the general minimum, and federal law may independently protect ~2 months of certain federal benefit deposits)  (dispositive)  [ ] keep  [ ] change  [ ] drop
5. Whether the debtor holds more than one deposit account subject to levy (the automatic minimum is a single aggregate amount across all accounts, not per account)  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. Whether the judgment debtor is a natural person (this exemption does not protect an LLC, corporation, or other entity debtor's account at all)  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. Whether the levied funds are traceable to wages actually paid to the debtor within the 30 days before levy (CCP § 704.070 separately exempts 75-100% of those, on a timely claim -- likely the largest protection available for a typical wage earner)  (dispositive)  [ ] keep  [ ] change  [ ] drop
8. Whether the debtor needs the amount above the automatic minimum for their own or their dependents' support (a fact-specific CCP § 704.225 claim, not automatic)  (dispositive)  [ ] keep  [ ] change  [ ] drop
9. Whether the levied account is jointly held with a non-debtor whose funds are commingled in it (a co-owner may have an independent third-party ownership claim to part of the balance)  (dispositive)  [ ] keep  [ ] change  [ ] drop
10. PROCEDURAL: when was the notice of levy served, and has a claim of exemption (with financial statement) been filed with the levying officer within 15 days of personal service / 20 days of mailed service (CCP 703.520(a))? The § 704.070 and § 704.225 protections are forfeited if not claimed in time  (dispositive)  [ ] keep  [ ] change  [ ] drop
11. WHO levied -- a private judgment creditor (this node), or the IRS / Franchise Tax Board / a federal agency proceeding administratively (different rules; the § 704.220 minimum does not automatically apply)?  (dispositive)  [ ] keep  [ ] change  [ ] drop
12. The SOURCE of every deposit in the account -- private pension/IRA (704.115), unemployment/disability (704.120/704.130), workers' compensation (704.160), personal-injury proceeds (704.140-.150) are traceable and largely or fully exempt, beyond the public-benefits and wages categories this node encodes  (dispositive)  [ ] keep  [ ] change  [ ] drop
13. Was the money taken by a JUDGMENT CREDITOR'S LEVY, or by the DEBTOR'S OWN BANK setting off a debt owed to that bank (no lawsuit)? Setoff is governed by Financial Code 864 and the deposit agreement, not by the 704.220 levy exemption  (dispositive)  [ ] keep  [ ] change  [ ] drop
14. If the debtor is MARRIED: when was the debt incurred relative to the marriage, whose earnings are in the levied account, and can the debtor spouse withdraw from it -- community property (including the debtor's wages in the non-debtor spouse's account) is generally liable for either spouse's debt (Fam. Code 910), subject to the 911 premarital-debt shield  (dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | Cal. Code Civ. Proc. § 704.220(a) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=704.220. |
| 2 | Cal. Code Civ. Proc. § 704.220(c)(1) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=704.220. |
| 3 | Cal. Code Civ. Proc. § 704.080 | B | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=704.080. |
| 4 | Cal. Code Civ. Proc. § 703.020(a) | B | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=703.020. |
| 5 | Cal. Code Civ. Proc. § 704.070 | B | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=704.070. |
| 6 | Cal. Code Civ. Proc. § 704.225 | B | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=704.225. |
| 7 | Cal. Code Civ. Proc. § 703.520(a), (c) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=703.520. |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | yes | Claim-of-exemption deadline (703.520) | Note + checklist |
| 02 | FIXED-VERIFIED | yes | IRS / FTB administrative levies not governed by § 704 | Note + checklist |
| 03 | FIXED-VERIFIED | yes | Other traceable exempt deposits (704.115/.120/.130/.140-.160) | Note + checklist |
| 04 | FIXED-SOURCE-NAMED (CCP 703.010; Fin. Code 864) + GLOSS | yes | Bank setoff conflated with judgment levy | bank_setoff_note; checklist |
| 05 | FIXED-VERIFIED (clarified against 704.220 text already pinned) | yes | Aggregation note read as a one-time exemption | aggregation_note clarified (per levy) |
| 06 | FIXED-SOURCE-NAMED (Fam. Code 910, 911) + GLOSS | no (overstates protection) | Non-debtor spouse's account treated as recoverable; Fam. Code 910 ignored | joint_account_note corrected; checklist |

**Drafting revisions (author / date / summary):**

- 2026-08-30 — Added CCP § 704.080 public-benefits/Social-Security-deposit exemption (much larger than the general minimum this node previously encoded alone) and § 703.020 natural-person-only threshold as derived_from entries; added aggregation_note clarifying the minimum is a single amount across all accounts, n
- 2026-08-30 — Second pass: added CCP § 704.070 (75-100% recent-wage-deposit exemption), § 704.225 (need-based exemption above the automatic minimum), and a joint-account/third-party-claim note (CCP § 720.110); added 3 corresponding checklist items. First pass (round 21) already added § 704.080/§ 703.020 and the a
- 2026-09-02 — Fixed quote characters on 704.080/704.070; replaced 704.225's non-verbatim opening with the actual statutory text.
- 2026-09-03 — Added claim-of-exemption deadline, administrative tax-levy, and other-traceable-exempt-deposits notes; 3 checklist questions. All 6 backlog findings (both runs) addressed; text NOT pinned this session -- SOURCE PENDING.
- 2026-09-04 — Pinned CCP 703.520 with the corrected 15/20-day deadline; fixed the 704.070 comma transcription error the live run caught. Tax-levy (IRC 6334; R&TC 18670) and other-traceable-exemption sections (704.115 etc.) NOT pinned -- markers removed from notes but the tier_rationale flags them as named-only.
- 2026-09-05 — Round 46: bank_setoff_note (CCP 703.010, Fin. Code 864 NAMED; GLOSS) + checklist; aggregation_note clarified (per-levy); joint_account_note corrected (Fam. Code 910/911 NAMED; GLOSS) + checklist.

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed True · material findings 3 (all dispositioned in round 46; see D)

### D2. Provisions NAMED in this node's notes but NOT pinned as citations (Cowork's word only -- treat like MANUAL rows)

- (joint_account_note) ...Under Family Code 910 (NAMED, not quoted this round) the community estate is liable for a debt incurred by either spouse during marriage (and, with exceptions, before), so wages of the debtor spouse deposited into an acc...
- (joint_account_note) ...and Family Code 911 (NAMED) shields the non-debtor spouse's OWN earnings from the other spouse's PREMARITAL debts if kept in an account the debtor spouse has no right to withdraw from...
- (bank_setoff_note) ...NAMED)...
- (bank_setoff_note) ...The statute that does limit setoff is Financial Code 864 (NAMED, not fetched this round): as generally described, a bank may not set off against a consumer deposit account if the setoff would leave less than a stated flo...

> Auditor: [ ] each named provision checked against its text, or listed for the v1.1 pinning round

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---

## 6. CA-VEHICLE-EXEMPTION

**Title:** California motor-vehicle equity exemption from creditor levy  
**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `0d43c22ea4b819a093cf759e1c92eb4c30a2ce8cc7a0d2a848b35283f2784c01`

**Reading load:** logic 1,026 words · checklist 438 · cited text 1,264 · 6 citations · 12 checklist items · 5 drafting revisions

### A. Logic (read in full; this is the content being certified)

**exemption_amount_usd**

7500

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**applies_to**

aggregate equity across a debtor's motor vehicles, or execution-sale proceeds, or insurance/indemnification proceeds for a vehicle -- combined, not stacked separately

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**automatic_single_vehicle_case**

if the debtor has only one vehicle and it is sold at execution sale, the $7,500 exemption on the PROCEEDS applies automatically without the debtor filing a claim (704.010(d)). CLARIFIED 2026-09-05 (round 46), from run_20260904T221748Z.json: 'automatic' means the levying officer pays the first $7,500 of sale proceeds to the debtor without a claim -- it does NOT stop the levy or the sale. A single-car debtor with $12,000 of equity who reads 'no claim needed' and does nothing will lose the car at auction (subject to 704.800's minimum-bid rule) and receive $7,500 in cash; if she wants to keep the car she must act -- file a claim of exemption within the 703.520 deadline, negotiate, or pay the creditor the non-exempt equity. The deadline note's carve-out for the single-vehicle case has been narrowed accordingly.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**determination**

up to $7,500 of vehicle equity/proceeds is protected from levy; equity above that amount remains reachable

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**tools_of_trade_note**

If the vehicle is reasonably necessary to and actually used in the debtor's trade, business, or profession, CCP § 704.060 provides a separate tools-of-trade exemption (aggregate ~$8,725, with the motor vehicle portion capped lower, ~$4,850) that can apply INSTEAD of, or alongside, this node's general § 704.010 vehicle exemption for a separate personal vehicle -- but § 704.060 itself says a trade vehicle is not separately exempt under it if an adequate § 704.010 vehicle is already available. This node alone, applied to a work vehicle without checking § 704.060, can materially understate the debtor's protection.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**bankruptcy_alternative_note**

This $7,500 figure is the non-bankruptcy (CCP § 704 series) exemption. A debtor filing Chapter 7 bankruptcy may instead elect California's 'System 2' exemptions under CCP § 703.140(b), which includes a separate ~$8,625 vehicle exemption PLUS a wildcard (up to ~$1,950, plus any entirely-unused portion of the ~$36,750 homestead exemption -- e.g. a renter with no homestead claim) that can be stacked onto vehicle equity. System 2 is an all-or-nothing election in place of § 704, not a add-on to it. This node does not itself determine which system is more favorable for a given debtor.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**proceeds_time_limit_note**

The execution-sale/insurance-proceeds branch of this exemption (CCP § 704.010(b)) is exempt only for 90 days after the debtor actually receives the proceeds -- after that, the money loses this specific protection (though it may still be protected as exempt personal property or under another exemption depending on how it was used or where it is held).

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**claim_of_exemption_deadline_note**

ADDED 2026-09-03 (round 38) -- PROCEDURAL PREDICATE: the vehicle exemption is NOT self-executing (in the single-vehicle case of § 704.010(d) only the $7,500 of PROCEEDS is paid without a claim -- the sale itself still goes forward; CLARIFIED round 46). The debtor must file a claim of exemption with the levying officer within 15 days after the notice of levy is personally served, or 20 days if served by mail (CCP § 703.520(a), quoted above -- CORRECTED 2026-09-04, round 39: not 10 days), after which the creditor may oppose and a hearing follows; a debtor who reads '$7,500 is protected' and does nothing loses the exemption entirely when the vehicle is sold. Also relevant: § 704.800 bars sale unless a bid exceeds the exemption plus liens. Appeared in both backlog runs (and identically on CA-BANK-ACCOUNT-EXEMPTION).

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**who_is_the_creditor_note**

ADDED 2026-09-03 (round 38): the $7,500 figure binds an ordinary JUDGMENT CREDITOR's levy. It does NOT bind (a) a federal tax levy -- IRC § 6334 supplies its own, narrower exempt-property list with no general vehicle exemption -- or certain other federal collection; (b) a support-arrears enforcement subject to CCP § 703.070; or (c) a SECURED PARTY repossessing under its own lien (Com. Code § 9609) -- the exemption runs against enforcement of a money judgment, not against the finance company's contractual right to the collateral. Telling a debtor facing repossession that $7,500 of equity is protected is flatly wrong and may cause him to skip reinstatement/redemption options. Appeared in both backlog runs.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**vehicle_as_dwelling_note**

ADDED 2026-09-03 (round 38): a motorhome, van, or RV in which the debtor actually RESIDES is a 'dwelling' under CCP § 704.710(a) and may be claimed under the HOMESTEAD exemption (hundreds of thousands of dollars), not this $7,500 vehicle exemption. Route vehicle-dwelling debtors to CA-HOMESTEAD-EXEMPTION.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**community_property_spouses_note**

ADDED 2026-09-03 (round 38): for a MARRIED debtor, whether each spouse may claim a separate vehicle exemption against a judgment reaching community property is governed by CCP § 703.110; this node has no marital-property variable, so its single-debtor $7,500 figure may be off by a full exemption for a couple with two cars.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**natural_person_screen_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json, DANGEROUS DIRECTION: CCP 703.020(a) -- 'the exemptions provided by this chapter apply only to property of a natural person.' A judgment against an LLC, a corporation, or a partnership gets no vehicle exemption on property titled to the entity, and a sole proprietor who incorporated and titled the truck to the corporation is in the same position as to that truck. Ask first WHO the judgment debtor is and WHOSE name is on the title. (A sole proprietorship that never incorporated is the natural person, and the exemption applies; the tools-of-trade exemption in 704.060 may then matter more than 704.010.) Threshold checklist item added.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**co_owner_and_third_party_title_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: the node collected only FMV and liens, with no ownership variable. (1) If the vehicle is titled JOINTLY with a non-spouse (a parent who co-signed, an adult child), only the debtor's fractional interest is subject to the judgment, and the co-owner may file a THIRD-PARTY CLAIM with the levying officer under CCP 720.110 et seq. (NAMED) to protect her share; the exemption then applies to the debtor's equity in his share. (2) If the car is titled to someone else entirely but parked at the debtor's home, the true owner's remedy is the same third-party claim -- the debtor has no exemption to claim in property that is not his. (3) For a SPOUSE, community-property rules govern instead (already in community_property_spouses_note; CCP 703.110). Checklist item added; 720.110 is FIXED-SOURCE-NAMED this round.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. THRESHOLD: is the judgment debtor a NATURAL PERSON, and is the vehicle titled to that person? A judgment against an LLC/corporation/partnership, or a vehicle titled to such an entity, gets NO exemption (CCP 703.020(a)); the answer is zero, not $7,500  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. Fair market value of the debtor's motor vehicle(s) (per used-car price guides customarily used by CA dealers, per CCP § 704.010(c))  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. Amount owed against the vehicle(s) (to compute equity)  (dispositive)  [ ] keep  [ ] change  [ ] drop
4. Whether the debtor has only one vehicle (triggers the automatic no-claim-needed exemption under subdivision (d)) -- and make clear that 'automatic' covers only the first $7,500 of SALE PROCEEDS; the levy and sale proceed unless the debtor files a claim of exemption or otherwise acts  (non-dispositive)  [ ] keep  [ ] change  [ ] drop
5. Whether the vehicle is reasonably necessary to and actually used in the debtor's trade, business, or profession (may qualify for the separate, differently-capped CCP § 704.060 tools-of-trade exemption)  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. Whether the debtor is filing (or could file) Chapter 7 bankruptcy and would benefit from electing the CCP § 703.140(b) 'System 2' vehicle + wildcard exemptions instead of the § 704 series  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. If the claimed exemption is for insurance or execution-sale proceeds rather than the vehicle itself, the date those proceeds were actually received (the exemption only lasts 90 days from receipt)  (dispositive)  [ ] keep  [ ] change  [ ] drop
8. PROCEDURAL: has the debtor been served with a notice of levy, and has a claim of exemption been filed with the levying officer within 15 days of personal service / 20 days of mailed service (CCP 703.520(a))? Outside the single-vehicle automatic case, the exemption is forfeited if not claimed in time  (dispositive)  [ ] keep  [ ] change  [ ] drop
9. WHO is seizing the vehicle -- an ordinary judgment creditor (this node applies), the IRS/a federal agency (IRC 6334 governs; no general vehicle exemption), a support obligee (CCP 703.070), or the auto lender/finance company enforcing its own lien (exemption does not apply to a secured party's repossession)?  (dispositive)  [ ] keep  [ ] change  [ ] drop
10. Does the debtor LIVE in the vehicle (motorhome/van/RV)? If so it may be a 'dwelling' under CCP 704.710 claimable under the far larger homestead exemption instead  (dispositive)  [ ] keep  [ ] change  [ ] drop
11. Is the debtor married and is the judgment being enforced against community property? Whether each spouse gets a separate vehicle exemption is a CCP 703.110 question  (dispositive)  [ ] keep  [ ] change  [ ] drop
12. Exactly whose name(s) are on the title -- if a non-spouse co-owner or a third party holds title (in whole or part), the creditor reaches only the debtor's interest and the co-owner/true owner files a third-party claim (CCP 720.110 et seq.); the exemption applies to the debtor's share  (dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | Cal. Code Civ. Proc. § 704.010(a), (d) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=704.010. |
| 2 | Cal. Code Civ. Proc. § 704.060(a), (c) | B | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=704.060. |
| 3 | Cal. Code Civ. Proc. § 703.140(b)(1), (2), (5) | B | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=703.140. |
| 4 | Cal. Code Civ. Proc. § 704.010(b) | B | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=704.010. |
| 5 | Cal. Code Civ. Proc. § 703.520(a), (c) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=703.520. |
| 6 | Cal. Code Civ. Proc. § 703.020(a) | A | ADDED AFTER last run (round 46) -- not yet live-checked | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=703.020. |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | yes | Claim-of-exemption 10-day deadline (703.520) | Note + checklist |
| 02 | FIXED-VERIFIED | yes | Vehicle-dwelling is a homestead (704.710) | Note + checklist |
| 03 | FIXED-VERIFIED | yes | IRS levy / secured-party repossession / support not bound by § 704 | Note + checklist |
| 04 | FIXED-VERIFIED | no | Married debtors / community property (703.110) | Note + checklist |
| 05 | FIXED-VERIFIED | yes | 'Automatic' single-vehicle language read as 'no action needed' | automatic_single_vehicle_case and deadline note clarified; checklist reworded |
| 06 | FIXED-SOURCE-NAMED (CCP 720.110) | varies | No title/ownership variable (co-owner, third-party owner) | co_owner_and_third_party_title_note; checklist |
| 07 | FIXED-VERIFIED | yes | Entity judgment debtor given an exemption (703.020(a)) | 703.020(a) pinned; natural_person_screen_note; threshold checklist |

**Drafting revisions (author / date / summary):**

- 2026-08-30 — Added CCP § 704.060 tools-of-trade, § 703.140(b) bankruptcy-System-2, and § 704.010(b) 90-day proceeds-limit derived_from entries; added 3 corresponding logic notes and 3 checklist items.
- 2026-09-02 — Fixed 704.010(b) wording to verbatim.
- 2026-09-03 — Added claim-of-exemption deadline, who-is-the-creditor (IRS/support/secured party), vehicle-as-dwelling, and community-property notes; 4 checklist questions. All 6 backlog findings (both runs) addressed; text NOT pinned this session -- SOURCE PENDING.
- 2026-09-04 — Pinned CCP 703.520 (15/20 days, corrected). IRC 6334, Com. Code 9609, CCP 704.710 and 703.110 NOT pinned this session -- notes retained as named-only screening flags.
- 2026-09-05 — Round 46: automatic_single_vehicle_case and deadline note clarified; 703.020(a) pinned + natural_person_screen_note + threshold checklist; co_owner_and_third_party_title_note (720.110 NAMED) + checklist; single-vehicle checklist item reworded.

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed True · material findings 3 (all dispositioned in round 46; see D)

### D2. Provisions NAMED in this node's notes but NOT pinned as citations (Cowork's word only -- treat like MANUAL rows)

- (co_owner_and_third_party_title_note) ...(NAMED) to protect her share...
- (co_owner_and_third_party_title_note) ...110 is FIXED-SOURCE-NAMED this round...

> Auditor: [ ] each named provision checked against its text, or listed for the v1.1 pinning round

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---

## 7. CA-HOMESTEAD-EXEMPTION

**Title:** California homestead exemption from creditor forced sale of a residence  
**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `c572581907e76da718b0433d427cce13253ee39d2f973abaf3979dfddaf58f96`

**Reading load:** logic 929 words · checklist 368 · cited text 777 · 4 citations · 9 checklist items · 3 drafting revisions

### A. Logic (read in full; this is the content being certified)

**exemption_amount**

greater of (countywide median single-family home sale price in the prior calendar year, capped at $600,000) or $300,000, both figures inflation-adjusted annually from a 2022 base

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**note_needs_current_figure**

this node encodes the FORMULA verbatim; the actual dollar floor/cap for the current year (inflation-adjusted from the 2022 base, plus the debtor's specific county's median sale price) must be pulled current at time of use, not hardcoded here.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**determination**

equity in the judgment debtor's homestead up to the computed exemption amount is protected from a forced sale to satisfy an ordinary money judgment

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**bankruptcy_overlay_note**

ADDED 2026-09-03 (round 38): in BANKRUPTCY the California figure is not the end of the analysis: 11 U.S.C. § 522(b)(3)(A)'s 730-day domicile rule can force use of another state's exemptions; § 522(p) caps homestead equity acquired within 1,215 days of filing (roughly $190k-$215k, inflation-adjusted) regardless of California's larger figure; and the debtor must choose between the CCP § 704 set and the § 703.140(b) alternative set (whose homestead component is far smaller). A recent transplant or recent purchaser told '$600,000+ is protected' would be badly misinformed. Appeared in both backlog runs.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**support_judgment_and_lien_exceptions_note**

ADDED 2026-09-03 (round 38): the exemption does not protect equally against every claimant. Under CCP § 703.070 a court may order otherwise-exempt property, including homestead equity, applied to a child/family/spousal SUPPORT judgment; and the homestead gives no protection against consensual deeds of trust, mechanics' liens, or federal tax liens. The checklist never asked what kind of debt underlies the judgment. Appeared in both backlog runs.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**forced_sale_mechanics_note**

ADDED 2026-09-03 (round 38): 'your equity up to the exemption is protected' does NOT mean the house cannot be sold. A judgment creditor may force a sale of a home whose equity exceeds liens plus the exemption; CCP § 704.800 bars the sale only if no bid exceeds liens plus the exemption amount, and the debtor receives the exemption amount from the proceeds, with § 704.720(b) protecting those proceeds for six months for reinvestment. The two facts that decide whether a sale can occur -- current fair market value and senior lien balances -- were absent from the checklist.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**sale_proceeds_and_declared_homestead_note**

ADDED 2026-09-03 (round 38), CORRECTED 2026-09-04 (round 39): two different proceeds rules. CCP § 704.720(b) (quoted above) exempts proceeds for six months after a FORCED sale under the enforcement division (or insurance/condemnation proceeds). Proceeds of a VOLUNTARY sale are protected for six months only for a DECLARED homestead (recorded homestead declaration) under CCP § 704.960 -- not pinned this session; named-only. So the debtor who voluntarily sold four months ago and is holding the proceeds is protected only if she had recorded a declared homestead. The round-38 version conflated the two; the 'occupied dwelling' checklist question still must not produce a flat 'no protection' answer without asking about a recorded declaration.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**continuous_residence_requirement_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: the automatic homestead protects the PRINCIPAL DWELLING in which the debtor or spouse (1) resided when the judgment lien attached and (2) 'resided continuously thereafter' until the court's homestead determination (CCP 704.710(c)). A debtor who relocated for work, moved in with an adult child, or entered assisted living and now rents the house out does not meet (2); 'I still call it my home' and an intent to return do not substitute for residence, although temporary absences (hospitalization, a short deployment) are generally tolerated by case law (GLOSS-FOR-COUNSEL: the line between a temporary absence and an abandonment). The dangerous direction is telling that debtor the equity is 'protected.' Separately, a DECLARED homestead (a recorded declaration, CCP 704.910-704.995; NAMED) has different rules and is not encoded here. Checklist item 1 reworded to collect the move-out facts.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**judgment_lien_survives_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: the exemption is a shield against FORCED SALE (704.740-704.850), not an erasure of the lien. A recorded abstract of judgment attaches to the debtor's interest in the dwelling (CCP 697.310, NAMED) and stays there: on a voluntary sale or refinance the title company will require it to be paid or released, and interest accrues at 10% meanwhile. The debtor with $250,000 of equity under the exemption is protected from being sold out, not from the lien. The partial statutory relief is 704.950 (NAMED): a judgment lien on a DECLARED homestead attaches only to surplus over the exemption plus senior liens, and a buyer's or refinancer's escrow can proceed on that basis -- which is the practical reason to record a declaration before selling. Consumers should be told 'no forced sale' and 'the lien will have to be dealt with when you sell,' not 'your home is safe.' Both sections FIXED-SOURCE-NAMED pending a fetch round; checklist item added.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**forced_sale_procedure_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: the exemption is asserted in a PROCEEDING, and the debtor has a job to do in it. A judgment creditor who wants to sell the dwelling must apply to the court for an order of sale (CCP 704.740) and obtain an order to show cause (704.750-704.770); the court determines whether the dwelling is a homestead, the exemption amount, and fair market value, and no sale may be ordered unless a bid exceeds the exemption plus senior liens (704.800). The debtor should FILE A RESPONSE to the application before the hearing asserting the homestead and the exemption amount, appear, and contest the creditor's appraisal (the court may appoint an appraiser; the debtor may offer her own). A debtor who assumes the exemption is 'automatic' and stays home risks a hearing at which only the creditor's numbers are before the court. Sections 704.740-704.800 are FIXED-SOURCE-NAMED this round (the forced_sale_mechanics_note already covers the 704.800 arithmetic). Checklist item added.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. Whether the property is the debtor's or spouse's PRINCIPAL dwelling both (1) on the date the judgment lien attached (abstract recorded) and (2) CONTINUOUSLY since -- if the debtor has moved out (relocation, moved in with family, assisted living) and especially if the house is rented, the automatic homestead does not apply (CCP 704.710(c)); collect move-out date, reason, and whether a homestead DECLARATION was ever recorded  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. Debtor's county, to look up the current countywide median single-family home sale price for the prior calendar year  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. Current inflation-adjusted dollar figures for the $300,000 floor and $600,000 cap  (dispositive)  [ ] keep  [ ] change  [ ] drop
4. Whether the matter is a BANKRUPTCY, and if so: how long has the debtor been domiciled in California (730-day rule), when was the current equity acquired (1,215-day § 522(p) cap), and which exemption set (§ 704 vs. § 703.140(b)) is being elected?  (dispositive)  [ ] keep  [ ] change  [ ] drop
5. The NATURE of the judgment or claim -- a child/family/spousal support judgment (CCP 703.070), a consensual deed of trust, a mechanic's lien, or a federal tax lien is not blocked by the homestead exemption the way an ordinary money judgment is  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. Current fair market value and the balance of all senior liens -- these, not the exemption figure alone, determine whether a forced sale can occur (CCP 704.800 minimum-bid rule)  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. If the home was recently SOLD: the sale date and where the proceeds are -- proceeds are exempt for six months (CCP 704.720(b)) even though there is no longer an occupied dwelling  (dispositive)  [ ] keep  [ ] change  [ ] drop
8. Is the consumer facing a FORCED SALE (creditor's application for order of sale / order to show cause), or only a recorded abstract of judgment? The exemption blocks the sale but does not remove the lien, which must be paid or released on any voluntary sale or refinance (CCP 697.310; 704.950 for a declared homestead)  (dispositive)  [ ] keep  [ ] change  [ ] drop
9. If an application for order of sale has been served: the hearing date, whether the debtor has filed a written response asserting the homestead and exemption amount, and whether she has her own valuation evidence -- the exemption must be asserted in the 704.740-704.800 proceeding, not assumed  (dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | Cal. Code Civ. Proc. § 704.730(a)-(b) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=704.730. |
| 2 | 11 U.S.C. § 522(b)(3)(A) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title11-section522&num=0&edition=prelim |
| 3 | Cal. Code Civ. Proc. § 704.720(a)-(b) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=704.720. |
| 4 | Cal. Code Civ. Proc. § 704.710(c) | A | ADDED AFTER last run (round 46) -- not yet live-checked | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=704.710. |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | yes | Bankruptcy overlay: 730-day rule, § 522(p) cap, § 703.140(b) election | Note + checklist |
| 02 | FIXED-VERIFIED | yes | Support judgments / consensual liens not blocked (703.070) | Note + checklist |
| 03 | FIXED-VERIFIED | yes | Forced-sale mechanics (704.800 minimum bid; FMV + senior liens) | Note + checklist |
| 04 | FIXED-VERIFIED | yes | Sale proceeds protected 6 months (704.720(b)) | Note + checklist |
| 05 | FIXED-SOURCE-NAMED (CCP 697.310, 704.950) | yes | Judgment lien survives the exemption; must be dealt with on sale/refinance | judgment_lien_survives_note; checklist |
| 06 | FIXED-VERIFIED | yes | 704.710(c) attachment-and-continuous-residence test not applied | 704.710(c) pinned; continuous_residence_requirement_note; checklist item 1 rewritten |
| 07 | FIXED-SOURCE-NAMED (CCP 704.740-704.800) | yes | Forced-sale procedure and the debtor's duty to respond omitted | forced_sale_procedure_note; checklist |

**Drafting revisions (author / date / summary):**

- 2026-09-03 — Added bankruptcy overlay (522(b)(3)(A)/522(p)/703.140(b)), support-judgment and lien exceptions (703.070), forced-sale mechanics (704.800), and sale-proceeds (704.720(b)) notes; 4 checklist questions. All 6 backlog findings (both runs) addressed; text NOT pinned this session -- SOURCE PENDING.
- 2026-09-04 — Pinned 11 U.S.C. 522(b)(3)(A) and CCP 704.720(a)-(b); corrected the sale-proceeds note (704.720(b) is forced-sale/insurance proceeds; voluntary-sale proceeds are the declared-homestead rule, 704.960). 703.070, 704.800, 703.140(b) NOT pinned -- named-only.
- 2026-09-05 — Round 46: 704.710(c) pinned + continuous_residence_requirement_note + checklist item 1 rewritten; judgment_lien_survives_note (697.310, 704.950 NAMED) + checklist; forced_sale_procedure_note (704.740-704.800 NAMED) + checklist.

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed True · material findings 3 (all dispositioned in round 46; see D)

### D2. Provisions NAMED in this node's notes but NOT pinned as citations (Cowork's word only -- treat like MANUAL rows)

- (continuous_residence_requirement_note) ...NAMED) has different rules and is not encoded here...
- (judgment_lien_survives_note) ...310, NAMED) and stays there: on a voluntary sale or refinance the title company will require it to be paid or released, and interest accrues at 10% meanwhile...
- (judgment_lien_survives_note) ...950 (NAMED): a judgment lien on a DECLARED homestead attaches only to surplus over the exemption plus senior liens, and a buyer's or refinancer's escrow can proceed on that basis -- which is the practical reason to recor...
- (judgment_lien_survives_note) ...' Both sections FIXED-SOURCE-NAMED pending a fetch round...
- (forced_sale_procedure_note) ...800 are FIXED-SOURCE-NAMED this round (the forced_sale_mechanics_note already covers the 704...

> Auditor: [ ] each named provision checked against its text, or listed for the v1.1 pinning round

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---
