# DEBT-DEMO-V1.0 CENSUS AUDIT — FEDERAL SPINE

*Generated 2026-09-05 from the frozen v1.0 files, `stage_b_dispositions.json`, and `run_20260904T221748Z.json`. Phase LOCK item 4. Copyright 2026 Andrew M Cohen. Apache 2.0.*

Read order is the order below. Each sheet: A logic (full text), B checklist, C citations with tier and verification status, D disposition history, E sign-off. Nothing here edits v1.0; findings go to `POST_V1_BACKLOG.md`.

---

## 1. FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6

**Title:** FDCPA/Regulation F coverage threshold -- statutory definitions of 'debt collector,' 'debt,' and 'creditor' under 15 U.S.C. 1692a  
**File:** `rules/debt/federal/fdcpa_coverage_threshold_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `a92db481c4fc00245c6f42749b806a51a82a8a70f07edb87f35d0ebf3fd88387`

**Reading load:** logic 2,177 words · checklist 627 · cited text 1,629 · 8 citations · 10 checklist items · 4 drafting revisions

### A. Logic (read in full; this is the content being certified)

**note_re_purpose**

This is a shared BAND-1 GATE node -- every other FDCPA/Regulation F node in this corpus (the 7-in-7 call-frequency rule, the validation-notice requirement, the false/deceptive-practices catalog, the unfair-practices catalog, and any future FDCPA node) presupposes that the entity being complained about is a 'debt collector' covered by the Act. That is NOT always true, and getting it wrong in either direction produces a materially wrong answer: telling a consumer their original creditor's own in-house collectors are FDCPA-covered when they are not gives false comfort; telling a consumer a debt buyer is categorically NOT covered (a common oversimplification of the Henson case, see below) can wrongly write off a real claim. This node exists so every other FDCPA node can gate on ONE threshold analysis instead of re-deriving it.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**two_independent_tests**

15 U.S.C. 1692a(6) defines 'debt collector' with TWO independent tests -- meeting EITHER one is enough to trigger coverage (subject to the exclusions below): (1) the PRINCIPAL PURPOSE test -- any business whose principal purpose is the collection of debts, regardless of whether it collects debts it owns or debts owed to others; or (2) the REGULARLY-COLLECTS-FOR-ANOTHER test -- any person who regularly collects or attempts to collect debts owed or due to someone ELSE (not to themselves).

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**own-name_creditor_exclusion**

Exclusion (A): an officer or employee of a creditor, collecting debts for that creditor IN THE CREDITOR'S OWN NAME, is not a debt collector. This is the most common real-world exclusion -- it covers a credit card issuer's or original lender's own in-house collections department. IMPORTANT carve-BACK-IN, from the statute's own second sentence: if a creditor collecting its own debt uses ANY NAME OTHER THAN ITS OWN that would indicate a third person is collecting the debt (e.g. operating an in-house department under a name that sounds like an independent agency), the creditor becomes a covered debt collector despite exclusion (A)/(F) -- Congress anticipated and closed this evasion specifically. CLARIFIED 2026-09-04 (round 43), from run_20260904T212407Z.json: exclusion (A) is about WHO the actor is, not what name the communication bears. It covers 'any officer or employee of a creditor' -- the creditor's own staff. A third-party vendor that generates the letters and places the calls under the creditor's brand (white-label or 'first-party' outsourcing, common in card, auto and utility portfolios) is not the creditor's officer or employee; it regularly collects debts owed to another and is a covered debt collector. The consumer's answer 'it was the bank, in its own name' is therefore not dispositive -- ask who actually performed the work. (The separate 1692j 'flat-rating' prohibition addresses the mirror image -- a form designed to make a creditor's own collection look like a third party's -- and is not implicated by a genuine vendor.)

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**current_vs_defaulted_servicer_exclusion**

Exclusion (F)(iii): a person collecting a debt owed to another is NOT a covered debt collector to the extent the debt was NOT IN DEFAULT at the time that person obtained it. This is the key distinction for loan servicers: a servicer that acquired/began servicing a loan while it was current (not yet in default) is excluded, even if the loan later defaults on that servicer's watch. A servicer or assignee that acquired the debt AFTER it was already in default does NOT get this exclusion and is a covered debt collector (assuming it is collecting for 'another' -- i.e. it does not itself own the debt outright; if it purchased the debt outright after default, see the debt-buyer note below instead).

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**debt_buyer_note_henson**

A company that PURCHASES a defaulted debt and then collects it for its OWN account (not on behalf of anyone else) does NOT trigger FDCPA coverage under the 'regularly collects ... debts owed ... another' test -- Henson v. Santander Consumer USA Inc., 582 U.S. ___ (2017) (unanimous). This is a narrow, frequently overstated holding: Henson decided ONLY that prong of the definition. The Supreme Court EXPRESSLY declined to decide whether such a debt buyer could still be covered under the SEPARATE 'principal purpose' test (1692a(6)'s first clause) -- and post-Henson lower-court decisions have held that a business whose principal purpose IS debt collection remains a covered debt collector under that alternative test even when collecting debts it purchased and owns outright. Practical upshot: do NOT tell a consumer 'debt buyers are never covered by the FDCPA' -- that overclaims a narrow holding. The correct question for a debt buyer is whether debt collection is the PRINCIPAL PURPOSE of that buyer's business (most dedicated debt-buying/collection companies would likely satisfy this), not simply whether it purchased the debt.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**other_exclusions_B_through_E**

(B) a person acting as a debt collector only for commonly-owned/affiliated entities, if collecting debts is not that person's principal business; (C) a government officer/employee collecting in the performance of official duties; (D) a person serving or attempting to serve legal process in connection with judicial enforcement of a debt (process servers); (E) a bona fide nonprofit consumer-credit-counseling organization that receives and distributes consumer payments to creditors at the consumer's request. CLARIFIED 2026-09-04 (round 43): the (B) affiliate exclusion has TWO conjunctive conditions in the quoted text -- collects only for related/affiliated persons AND its principal business is not the collection of debts. The checklist question previously asked only the first. A dedicated collections affiliate of a lender or debt buyer typically fails the second and is covered.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**other_F_exclusions**

(F)(i) activity incidental to a bona fide fiduciary obligation or bona fide escrow arrangement; (F)(ii) a debt the person ORIGINATED itself (as opposed to acquiring from someone else); (F)(iv) a debt obtained as a secured party in a commercial credit transaction involving the creditor.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**determination**

COVERED as a 'debt collector' if EITHER (a) the person's business's principal purpose is debt collection (regardless of whose debts, including debts it owns after purchase), OR (b) the person regularly collects debts owed to ANOTHER (not to itself) -- UNLESS an exclusion (A)-(F) applies. In practice, check in this order for a typical consumer fact pattern: (1) is this the original creditor calling/writing in its own actual name? -> excluded under (A), UNLESS it used a name suggesting a third party. (2) Is this a servicer/assignee that acquired the loan while current (not yet in default)? -> excluded under (F)(iii). (3) Is this an entity that bought the debt outright (owns it) and is collecting only for itself? -> not covered under the 'owed another' prong per Henson, BUT may still be covered under the principal-purpose prong -- do not assume 'not covered' without checking whether debt collection is that entity's principal business. (4) Otherwise (a third-party agency collecting on behalf of a creditor it doesn't own the debt from, a debt buyer whose principal business is debt collection, etc.) -> covered, apply the FDCPA/Reg F nodes in this corpus -- BUT, CORRECTED 2026-09-03 (round 38), only if the 'REGULARLY collects or attempts to collect' element of prong (b) is actually met (or prong (a)'s principal-purpose test is): the quoted 1692a(6) text requires regularity, and a person who collects for others only occasionally or incidentally (a general-practice lawyer who sends a couple of demand letters a year for an HOA or landlord client, a bookkeeper, a one-off demand) may fall outside coverage. 'Regularly' is a contested, fact-intensive element courts resolve against coverage in exactly these small-volume situations; this node names it as a threshold fact and does not resolve it.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**state_law_reminder**

This node addresses FEDERAL coverage only. Many states have their own debt-collection statutes ('mini-FDCPAs') that reach entities the federal Act excludes -- for example, Massachusetts's 940 CMR 7.00 (see FDCPA-REGF-CALL-FREQUENCY-1006.14b's state-overlay note) defines 'creditor' broadly and regulates original creditors directly, not just federally-defined 'debt collectors.' An entity excluded here may still be regulated under state law -- always check the relevant state-layer nodes in this corpus.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**what_is_being_collected_note**

ADDED 2026-09-01 (round 33): this node's other notes address WHO the entity is (the 1692a(6) test). That is necessary but NOT sufficient -- the FDCPA also gates on WHAT is being collected. Under 1692a(5), the FDCPA applies only to a 'debt': an obligation of a 'consumer' (1692a(3), a NATURAL PERSON) arising from a transaction primarily for PERSONAL, FAMILY, or HOUSEHOLD purposes. A business/commercial obligation -- a small-business loan, an equipment lease, a commercial line of credit -- is entirely outside the Act, no matter how squarely the collecting entity fits the 1692a(6) 'debt collector' test. This is a genuinely common, easy-to-miss threshold: a sole proprietor or small-business owner contacted by an aggressive third-party collection agency about a business debt has NO FDCPA claim at all, even though the calling pattern may look identical to a covered consumer-debt collection call. Similarly, most government fines, tickets, tolls, taxes, and other non-transactional obligations are not 'debts' under this definition either. CORRECTED 2026-09-04 (round 43), from run_20260904T212407Z.json: the sentence about 'government fines, tickets, tolls, taxes, and other non-transactional obligations' must not be read as 'government-origin obligations are not debts.' The 1692a(5) test is whether the obligation arises 'out of a transaction' whose subject is 'primarily for personal, family, or household purposes' -- the identity of the creditor is irrelevant. A municipal water/sewer account, a public-hospital or city ambulance bill, public-university tuition, or a government-held student loan is an obligation for services or credit the household actually consumed and IS a 'debt' when a third party collects it; only obligations that are not consensual transactions (a parking fine, a tax assessment, a criminal restitution order, and some tolls/penalties) fall outside. Government-referred medical and utility accounts are among the most commonly collected consumer debts. GLOSS-FOR-COUNSEL (case names, not quoted): Pollice v. National Tax Funding, L.P., 225 F.3d 379 (3d Cir. 2000) (municipal water/sewer and property-tax obligations -- water/sewer held to be debts, taxes not); Piper v. Portnoff Law Associates, 396 F.3d 227 (3d Cir. 2005) (municipal water and sewer bill a 'debt').

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**security_interest_enforcement_note**

ADDED 2026-09-01 (round 33): 1692a(6)'s third sentence gives security-interest enforcers (repossession agents, nonjudicial foreclosure firms) a special, LIMITED inclusion -- they are 'debt collectors' ONLY for purposes of 1692f(6) (the prohibition on wrongful nonjudicial dispossession/disablement of property). Obduskey v. McCarthy & Holthus LLP, 587 U.S. ___ (2019) (unanimous) holds that a firm whose ONLY role is enforcing a security interest through nonjudicial foreclosure is NOT a covered 'debt collector' for the Act's other purposes -- no validation-notice duty, no 7-in-7 call-frequency presumption, no general false/deceptive or unfair-practices catalog liability -- even though it is 'regularly collecting debts owed another' in the ordinary sense. This is a genuinely surprising result to a layperson and a common real fact pattern (nonjudicial foreclosure, and by extension vehicle repossession firms). CAUTION, per the Court's own express limit (and Justice Sotomayor's concurrence): this narrow non-coverage extends ONLY to steps actually required by state law to enforce the security interest -- conduct going beyond that (e.g., abusive collection tactics unrelated to the required legal notices) is not immunized and can still trigger full 'debt collector' status if the entity's activity crosses into ordinary debt collection.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**F_iii_scope_clarification_note**

ADDED 2026-09-01 (round 33): exclusion (F)(iii) (a person who 'obtained' a debt that was NOT in default at the time) is written to exclude servicers/assignees who acquired an OWNERSHIP or SERVICING interest in the debt while it was current. It does NOT exclude a third-party collection agency that was merely RETAINED/HIRED by the original creditor to work a delinquent account without any transfer of ownership or servicing rights -- such an agency never 'obtained' the debt within the meaning of (F) at all, regardless of when in the debt's life it was retained, and is independently covered from day one under the main 'regularly collects... debts owed... another' prong (or the principal-purpose prong). A common real fact pattern this distinction resolves: a bank's 'early-out' recovery vendor calling on an account only 45 days past due, before formal charge-off -- being retained EARLY does not exempt a hired collection agency the way (F)(iii) exempts a servicer who actually acquired the loan while it was current.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**alleged_obligation_note**

ADDED 2026-09-03 (round 38): the 'is it a debt' gate must not be applied as 'did this person actually incur a consumer obligation' -- both quoted definitions above use 'alleged' (1692a(5): 'any obligation or alleged obligation'; 1692a(3): 'obligated or allegedly obligated'). A collector pursuing a consumer for an account she never opened, a paid-off balance, or someone else's debt is collecting an ALLEGED consumer debt and is fully within the FDCPA. The prior checklist wording could route the single most common consumer complaint ("this isn't my debt") to 'not covered.'

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**deceased_consumer_note**

ADDED 2026-09-03 (round 38): collection against a deceased person's estate or surviving family is COVERED, not outside the gate. The obligation was incurred by a natural person for personal/family/household purposes and remains a 'debt'; 1692c(d) (quoted above) treats the executor or administrator as the 'consumer' for communication purposes, and Regulation F, 12 CFR 1006.6(a)(1)(iv), does the same for the estate's personal representative A surviving relative who is NOT the executor/administrator and did not co-sign is a THIRD PARTY -- implying she is personally liable, or discussing the debt with her, is governed by the third-party-communication restrictions (1692c(b)/1692b), not a reason to treat the debt as uncovered.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. WHO ACTUALLY performs the collection work -- not whose name appears on the letter or caller ID. Is the person writing/calling an OFFICER OR EMPLOYEE of the original creditor, collecting in the creditor's own name (exclusion (A))? An outside vendor or agency the creditor hired to work delinquent accounts under the creditor's brand is NOT the creditor's officer or employee: it collects debts 'owed or due another' and is a covered debt collector even though every communication carries the bank's name. Ask: who signs their paycheck, and is the caller at the creditor or at a firm the creditor retained?  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. If it is the original creditor (or its employee) using a different name -- does that name suggest a third party is collecting the debt? (Would defeat the own-name exclusion.)  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. If this is a servicer or assignee collecting on behalf of someone else: did it acquire/begin servicing the debt BEFORE or AFTER the debt went into default?  (dispositive)  [ ] keep  [ ] change  [ ] drop
4. If this entity purchased the debt and owns it outright: is debt collection the PRINCIPAL PURPOSE of that entity's business? (Determines coverage under the alternative test Henson did not foreclose, even though the 'owed another' test does not apply to a debt it owns.)  (dispositive)  [ ] keep  [ ] change  [ ] drop
5. Does any of the narrower exclusions (B)-(E) apply? For (B), BOTH statutory conditions must be met: the entity collects ONLY for persons related to it by common ownership or corporate control, AND 'the principal business of such person is not the collection of debts.' A captive collections subsidiary whose principal business IS collecting the family's accounts fails the second condition and is a covered debt collector despite the affiliation. (C) government officer/employee in official duties; (D) process server; (E) bona fide nonprofit credit counselor.  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. Is the obligation a 'debt' under 15 U.S.C. 1692a(5) -- owed OR ALLEGED to be owed by a NATURAL PERSON, arising (or alleged to arise) from a transaction primarily for PERSONAL, FAMILY, or HOUSEHOLD purposes? CORRECTED 2026-09-03 (round 38): the statute reaches 'any obligation or alleged obligation' and a 'consumer' is anyone 'obligated or allegedly obligated' (1692a(3)) -- a phantom debt, mistaken-identity, or identity-theft account the person never actually incurred is squarely COVERED (attempts to collect debts that are not owed are the core of 1692e/1692g claims), not excluded for lack of a real transaction. A business/commercial obligation remains outside the Act.  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. Is the entity's role limited to enforcing a security interest (nonjudicial foreclosure, repossession) through steps actually required by state law? If so, it is a 'debt collector' ONLY for 1692f(6) purposes -- the validation-notice, call-frequency, and general practices nodes in this corpus do not apply to it.  (dispositive)  [ ] keep  [ ] change  [ ] drop
8. If a servicer/assignee's (F)(iii) not-in-default-when-obtained exclusion is being considered, confirm the entity actually took an OWNERSHIP or SERVICING interest in the debt (not merely retained as a collection agency without any transfer of rights) -- a hired collection agency does not get this exclusion no matter when it was retained.  (dispositive)  [ ] keep  [ ] change  [ ] drop
9. If the entity is a third party collecting for someone else (not the original creditor, not a debt buyer): does it collect debts for others REGULARLY (volume, frequency, whether collection is a recurring part of its business), or only occasionally/incidentally? 'Regularly' is an element of 1692a(6)'s second prong, not a given -- a low-volume or one-off collector may not be covered  (dispositive)  [ ] keep  [ ] change  [ ] drop
10. If the person the collector is contacting is not the original obligor: has the obligor died, and is the contacted person the estate's executor/administrator (treated as the 'consumer' under 1692c(d)) or merely a surviving relative (a third party protected by 1692c(b))? A deceased obligor does NOT take the debt outside the FDCPA  (dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | 15 U.S.C. § 1692a(6) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692a&num=0&edition=prelim |
| 2 | 15 U.S.C. § 1692a(4) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692a&num=0&edition=prelim |
| 3 | Henson v. Santander Consumer USA Inc., 582 U.S. ___ (2017) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/supremecourt/text/16-349 |
| 4 | 15 U.S.C. § 1692a(5) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692a&num=0&edition=prelim |
| 5 | 15 U.S.C. § 1692a(3) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692a&num=0&edition=prelim |
| 6 | Obduskey v. McCarthy & Holthus LLP, 587 U.S. ___ (2019) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/supremecourt/text/17-1307 |
| 7 | 15 U.S.C. § 1692c(d) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692c&num=0&edition=prelim |
| 8 | 12 C.F.R. § 1006.6(a) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.6 |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | yes | "Is it a debt" gate excludes phantom/identity-theft debts | 1692a(5)/(3) already quoted say *alleged*; checklist item reworded + note |
| 02 | FIXED-VERIFIED | yes | Deceased obligor / surviving family treated as uncovered | 1692c(d) added (verified round 34); Reg F 1006.6(a)(1)(iv) pending |
| 03 | FIXED-VERIFIED | no | "Regularly collects" element never tested (occasional lawyer/bookkeeper) | Element is in the quoted 1692a(6); determination step 4 + checklist |
| 04 | FIXED-VERIFIED | yes | White-label vendor collecting under the creditor's brand routed to exclusion (A) | checklist item 1 rewritten to test the actor, not the name; own-name note clarified |
| 05 | FIXED-VERIFIED | yes | Exclusion (B) checklist question dropped the principal-business condition | checklist item 5 rewritten with both conjunctive conditions |
| 06 | FIXED-VERIFIED (statute) + GLOSS-FOR-COUNSEL (cases) | yes | Government-origin consumer-transaction obligations (municipal utility, EMS, public hospital) treated as non-debts | what_is_being_collected_note corrected on the 1692a(5) transaction test; Pollice / Piper named as GLOSS-FOR-COUNSEL |

**Drafting revisions (author / date / summary):**

- 2026-09-01 — Reworded title to a plain topical description (no case-caption-style phrasing) to fix the Stage-A misreading. Added 15 U.S.C. 1692a(5)/(3) (the 'debt'/'consumer' definitions -- this node previously gated only on WHO is collecting, never on WHAT is being collected or FROM WHOM) and Obduskey v. McCart
- 2026-09-03 — Fixed the 'is it a debt' gate to cover ALLEGED obligations (phantom/mistaken-identity/identity-theft debts); added the 'regularly collects' element to determination step (4) plus a checklist question; added 1692c(d) and a deceased-consumer note + checklist question. All three findings appeared in bo
- 2026-09-04 — Pinned 12 CFR 1006.6(a)(4); removed the SOURCE PENDING marker on the deceased-consumer note.
- 2026-09-04 — Round 43: checklist items 1 and 5 rewritten; own-name, (B)-(E) and what-is-being-collected notes clarified/corrected. All anchored in the node's existing verified 1692a(5)/(6) text; the two Third Circuit cases are named as GLOSS-FOR-COUNSEL, not quoted.

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed False · material findings 0 (all dispositioned in round 46; see D)

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---

## 2. FDCPA-VALIDATION-NOTICE-1692g

**Title:** Debt validation notice — required content, and how the 30-day dispute window is calculated  
**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `0aa94bd358959d65f325955e56854bd949b0b51176421307fc1ae49eb422e758`

**Reading load:** logic 856 words · checklist 470 · cited text 1,739 · 11 citations · 15 checklist items · 7 drafting revisions

### A. Logic (read in full; this is the content being certified)

**note_re_scope**

Reg F (effective 2021-11-30) elaborates and partially supersedes the statute's bare five-item list with a fuller content/format regime (Model Form B-1 safe harbor) and clarifies timing (initial communication OR within 5 days OR oral-in-initial-communication) and the mailbox-rule assumption for computing the dispute deadline. Both sources are encoded together because Reg F does not repeal §1692g — a compliant notice must satisfy both; this node treats Reg F's fuller list as the operative content standard and the statute as the underlying five-item floor, consistent with 12 CFR 1006.34(d)(2)'s Model Form B-1 safe-harbor design.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**notice_timing_requirement**

- {"trigger": "initial_communication_with_consumer_re_debt_collection", "compliant_options": ["validation_information_in_initial_communication_written_or_electronic", "validation_notice_sent_within_5_days_of_initial_communication", "validation_information_provided_orally_in_initial_communication"], "exception": "not_required_if_consumer_paid_debt_before_the_5_day_deadline_would_run"}

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**required_content_checklist_ref**

see completeness_checklist below — mirrors 12 CFR 1006.34(c)(1)-(4)

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**dispute_window**

- {"length_days": 30, "starts": "date_consumer_receives_or_is_assumed_to_receive_validation_information", "mailbox_rule_assumption_days": 5, "mailbox_rule_excludes": ["Saturdays", "Sundays", "federal_legal_holidays"], "determination": "dispute_window_open_if today <= (assumed_or_actual_receipt_date + 30 calendar days), where assumed_or_actual_receipt_date = validation_info_provided_date + 5 days, counting only days that are NOT a Saturday, Sunday, or federal legal holiday (per 12 CFR 1006.34(b)(5) -- i.e. 5 BUSINESS days, not 5 calendar days). CRITICAL, previously ambiguous in this field: the Saturday/Sunday/holiday exclusion applies ONLY to computing the 5-day assumed-receipt date -- the 30-day period that follows runs in ordinary CALENDAR days, with no further weekend/holiday exclusion. Do not apply the exclusion to the whole 35-day span."}

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**consequence_if_disputed_in_writing_within_window**

- {"collector_must": "cease_collection_of_disputed_portion_until_verification_or_judgment_copy_mailed_to_consumer", "collection_activity_during_window_before_dispute": "permitted_if_otherwise_lawful_and_does_not_overshadow_or_contradict_the_dispute_right", "SECOND_TRIGGER_original_creditor_request": "CORRECTED 2026-09-03 (round 38): the cease-collection duty in 1692g(b) (quoted above) has TWO independent written triggers -- a written dispute, OR a written request for 'the name and address of the original creditor.' A timely written original-creditor request obligates the collector to stop collection until it mails that name and address, even if the letter never says the debt is disputed. This node previously captured only the dispute trigger."}

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**consequence_if_no_compliant_notice_sent**

- {"flag": "potential_1692g_violation — cross-reference to a separate FDCPA-enforcement node (statutory damages under 15 U.S.C. § 1692k) not yet encoded; this node determines the validation-notice fact pattern only, does not itself compute damages exposure."}

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**non_delivery_returned_mail_note**

The 5-day receipt assumption in 12 CFR 1006.34(b)(5) is what a debt collector may use WHILE it does not yet know whether the consumer actually received the notice -- and per the CFPB's own official interpretation (comment 34(b)(5)-1), the collector may keep using that assumed date even if it LATER learns the consumer received it on a different day. But this only holds while the collector doesn't yet know delivery failed. If mail is returned as undeliverable (or the collector otherwise learns the consumer never received the notice) and the collector sends a SUBSEQUENT validation notice, the 30-day window must be calculated from the SUBSEQUENT notice's assumed-or-actual receipt date, not the original mailing date (comment 34(b)(5)-2). This node's checklist did not previously ask whether the original notice was returned/non-delivered or whether a follow-up notice was ever sent -- a consumer who never actually got a validation notice (mail returned, no follow-up sent) may not have had a validation period start running at all under this framework, a materially different answer than 'the 30-plus-5-day window from the original mailing has already closed.'

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**overshadowing_note**

ADDED 2026-09-03 (round 38): 1692g(b)'s final sentence (quoted above) forbids collection activity during the 30-day window that 'overshadow[s] or [is] inconsistent with' the dispute-rights disclosure. A demand for payment within a period SHORTER than the 30-day window ('pay in full within 10 days to avoid further action'), or calls urging immediate payment, is the single most litigated species of 1692g(b) claim -- and it can occur even when the notice itself contains every required content item. The checklist previously collected no facts about the content, tone, or deadlines of intra-window collection activity, so the 'does not overshadow' condition in this node's own logic could never actually be evaluated.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**formal_pleading_not_initial_communication_note**

ADDED 2026-09-03 (round 38): 15 U.S.C. 1692g(d) provides that a communication in the form of a formal pleading in a civil action is NOT an 'initial communication' for validation-notice purposes (Regulation F, 12 CFR 1006.34(b)(2), mirrors this and also excludes location-information communications under 1692b). A consumer whose first contact from the collector was a summons and complaint should NOT be told the 5-day validation clock ran from service, and the 30-day dispute window runs from the later actual validation notice. Suit-first collection is very common.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**oral_dispute_note**

ADDED 2026-09-03 (round 38), CORRECTED 2026-09-04 (round 39): a dispute made ORALLY (by phone) within the window does not trigger 1692g(b)'s cease-collection duty, which by its text requires a writing (quoted above), and Regulation F's 1006.38 likewise keys its cease-collection and duplicative-dispute rules to disputes 'submitted by the consumer in writing' -- the round-38 version of this note wrongly said 1006.38 defines a dispute without a writing requirement; it does not. But an oral dispute is not legally inert: 15 U.S.C. 1692e(8) (quoted above) prohibits communicating credit information 'which is known or which should be known to be false, including the failure to communicate that a disputed debt is disputed,' and nothing in that text limits 'disputed' to written disputes. A collector who keeps calling after an oral dispute is likely lawful as to cease-collection; a collector who reports the account to a credit bureau without a dispute flag after an oral dispute is exposed under 1692e(8). Tell the consumer both halves.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. Date of the debt collector's initial communication with the consumer about this debt  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. Whether a validation notice (written or electronic) was included in that initial communication, or sent within 5 days after it, or the validation information was given orally during that initial communication  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. Whether the consumer had already paid the debt before any 5-day notice deadline would have run  (dispositive)  [ ] keep  [ ] change  [ ] drop
4. Whether the notice included: collector name/address for disputes; consumer name/address; current creditor name; itemization date; amount of debt at itemization date; itemization of current amount; current amount of debt  (dispositive)  [ ] keep  [ ] change  [ ] drop
5. Whether the notice stated the dispute-window end date and the consequences of disputing vs. not disputing (assumption-of-validity, cease-collection-until-verification, original-creditor-request right)  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. Date the consumer received (or is deemed to have received) the validation notice  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. Whether, and when, the consumer notified the collector IN WRITING that the debt (or a portion) is disputed  (dispositive)  [ ] keep  [ ] change  [ ] drop
8. Whether collection activity continued after a written dispute was sent, before verification was provided  (dispositive)  [ ] keep  [ ] change  [ ] drop
9. Whether the entity sending the notice (or failing to) is a covered 'debt collector' under 15 U.S.C. 1692a(6) -- see the dedicated FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6 node for the full coverage analysis (an original creditor collecting its own debt, or a servicer that acquired the debt while it was not yet in default, has no validation-notice duty under this node at all)  (dispositive)  [ ] keep  [ ] change  [ ] drop
10. Whether the original validation notice was returned as undeliverable, or the collector otherwise learned the consumer did not receive it, and if so whether a SUBSEQUENT validation notice was sent -- the 30-day window runs from the subsequent notice's (assumed) receipt date, not the original mailing date  (dispositive)  [ ] keep  [ ] change  [ ] drop
11. When computing the 30-day dispute deadline: confirm the Saturday/Sunday/federal-holiday exclusion was applied ONLY to the initial 5-day receipt assumption, not to the 30-day period that follows it  (dispositive)  [ ] keep  [ ] change  [ ] drop
12. What was the FORM of the initial communication -- a letter/call/email, or a summons and complaint in a lawsuit? A formal pleading is not an 'initial communication' (1692g(d)) and does not start the 5-day validation clock  (dispositive)  [ ] keep  [ ] change  [ ] drop
13. Whether, and when, the consumer sent a WRITTEN request for the name and address of the ORIGINAL creditor (a second, independent cease-collection trigger under 1692g(b), even without a dispute)  (dispositive)  [ ] keep  [ ] change  [ ] drop
14. The content, tone, and any deadlines of collection communications sent DURING the 30-day window before any dispute -- did any demand payment within fewer than 30 days, threaten action before the window closed, or otherwise overshadow/contradict the dispute right?  (dispositive)  [ ] keep  [ ] change  [ ] drop
15. If the consumer disputed only ORALLY: did the collector subsequently report the account to a consumer reporting agency without noting it as disputed (1692e(8) / 12 CFR 1006.38), separate from the written-dispute cease-collection analysis  (dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | 15 U.S.C. § 1692g(a) | B | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/uscode/text/15/1692g |
| 2 | 15 U.S.C. § 1692g(b) | B | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/uscode/text/15/1692g |
| 3 | 12 C.F.R. § 1006.34(a)(1) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34 |
| 4 | 12 C.F.R. § 1006.34(b)(5) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34 |
| 5 | 12 C.F.R. § 1006.34(c) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34 |
| 6 | 15 U.S.C. § 1692a(6) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692a&num=0&edition=prelim |
| 7 | 12 C.F.R. § 1006.34(b)(5), Official Interpretation, comment 34(b)(5)-2 | A | ADDED AFTER last run (round 46) -- not yet live-checked | https://www.law.cornell.edu/cfr/text/12/appendix-Supplement_I_to_part_1006 |
| 8 | 15 U.S.C. § 1692g(d) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692g&num=0&edition=prelim |
| 9 | 15 U.S.C. § 1692g(b) (final sentence) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692g&num=0&edition=prelim |
| 10 | 12 C.F.R. § 1006.38(b)(1), (c) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.38 |
| 11 | 15 U.S.C. § 1692e(8) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692e&num=0&edition=prelim |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | yes | Formal pleading treated as initial communication (1692g(d)) | Note + checklist |
| 02 | FIXED-VERIFIED | yes | Original-creditor-name request is a 2nd cease-collection trigger | Already in the verified 1692g(b) quote; operationalized |
| 03 | FIXED-VERIFIED | yes | Overshadowing never evaluable (no intra-window facts collected) | Anti-overshadowing sentence is in the verified quote; note + checklist |
| 04 | FIXED-VERIFIED | yes | Oral dispute treated as inert (1692e(8)/1006.38 credit-reporting duty) | Note + checklist |

**Drafting revisions (author / date / summary):**

- 2026-08-30 — Retitled from an outcome-determination framing ('Debt validation notice — was a compliant notice provided, and is the consumer still within the dispute window?') to a rule-statement framing, matching every other node's pattern. Root cause: the corroboration runner's Stage A prompt uses the node titl
- 2026-08-31 — Replaced the non-verbatim 12 C.F.R. § 1006.34(c) quoted_text (a paraphrased summary of all four subsections) with a genuinely verbatim excerpt confirmed against the live eCFR page (the lead-in sentence plus the first numbered subsection, (c)(1), with its actual heading and cross-reference to § 1006.
- 2026-09-01 — Rewrote dispute_window.determination to remove the ambiguity between the 5-day mailbox-assumption exclusion (business days) and the 30-day validation period itself (calendar days, no exclusion) -- the prior phrasing 'computed per the exclusions above' could be misread as applying the weekend/holiday
- 2026-09-01 — Updated the tier_rationale on the 15 U.S.C. 1692a(6) derived_from entry, and the coverage-related completeness_checklist item, to cross-reference the new standalone FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6 node instead of carrying the coverage analysis solely inline.
- 2026-09-03 — Encoded 1692g(b)'s second trigger (original-creditor request) and its anti-overshadowing sentence -- both already in this node's verified 1692g(b) quote but never operationalized; added formal-pleading (1692g(d)) and oral-dispute (1692e(8)/1006.38) notes; 4 checklist questions. All from the backlog,
- 2026-09-04 — Pinned 1692g(d), 1692g(b)'s anti-overshadowing sentence, 12 CFR 1006.38(b)(1)/(c), and 1692e(8). Corrected the round-38 oral-dispute note, which mis-described 1006.38 (its dispute rules require a writing); the oral-dispute point now rests on 1692e(8) alone.
- 2026-09-05 — Round 46: comment 34(b)(5)-2 entry re-pinned to the Cornell LII Supplement I mirror. No logic change.

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified False · Stage B parsed False · material findings 0 (all dispositioned in round 46; see D)

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---

## 3. FDCPA-REGF-CALL-FREQUENCY-1006.14b

**Title:** Presumptively unlawful call frequency (the '7-in-7' rule)  
**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `19e1f452d56f1293165a3d710d27f17e3c1f9c441a881e7f74d238e47d682228`

**Reading load:** logic 3,079 words · checklist 952 · cited text 3,610 · 19 citations · 19 checklist items · 9 drafting revisions

### A. Logic (read in full; this is the content being certified)

**presumption_type**

rebuttable -- a presumption of compliance or violation, not an absolute rule. CLARIFIED 2026-09-04 (round 41) from the Official Interpretation, comments 14(b)(2)(i)-2 and 14(b)(2)(ii)-2: the presumption of COMPLIANCE is rebutted on proof that the collector nevertheless called 'repeatedly or continuously with intent to annoy, abuse, or harass' (intent is assumed from the natural consequence of the conduct), weighing non-exhaustive factors -- rapid-succession or highly concentrated calls (two calls within five minutes; seven in one day), the voicemail pattern, what the consumer previously told the collector (do not call / I refuse to pay / I do not owe this / a cease-communication or no-calls request), and the collector's own prior conduct. The presumption of VIOLATION is rebutted by, e.g., a call required by law, a call tied to active litigation, a call answering the consumer's own information request where the consent exclusion did not fit, or a time-critical call that let the consumer avoid a harm outside the collector's control. See multi_debt_aggregate_volume_note.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**safe_harbor_count**

no more than 7 calls within any 7 consecutive days, per particular debt

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**cooldown_rule**

no call within 7 consecutive days after an actual telephone CONVERSATION about that debt (the conversation date is day 1 of that 7-day window) — distinct from the raw count limit and can be more restrictive CLARIFIED 2026-09-04 (round 41): the conversation that starts the window may be one the CONSUMER initiated -- the Official Interpretation's own example (comment 14(b)(2)(i)-1.ii) starts the seven days from a consumer's inbound call, and comment 14(b)(4)-1.ii applies the rule 'regardless of which party initiated the discussion about the particular debt.' A consumer who phones to dispute the balance on Monday and is then called Wednesday, Thursday and Friday without having asked for a call-back has three presumptive violations. (If she DID ask for a call-back, the prior-consent exclusion in 1006.14(b)(3)(i) applies for up to seven days, but comment 14(b)(3)(i)-2 says that consent ends once the collector has the conversation.)

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**unit_of_count**

Per 'particular PERSON' AND per 'particular debt' together -- the regulatory text itself (12 CFR 1006.14(b)(2)(i)) counts 'a telephone call to a particular PERSON in connection with the collection of a particular debt,' not a telephone NUMBER. CORRECTED 2026-09-01 (round 32): calls to the SAME consumer at DIFFERENT numbers she can be reached at (her cell phone, her home line, her direct line at work) all count toward the SAME 7-call bucket for that person and that debt -- which number the collector dials does not create a separate count. This is distinct from calls to a genuinely DIFFERENT person (e.g., the consumer's mother, or a co-signer) about the same debt, which DO get their own separate 7-call bucket, since they are a different 'particular person' under the rule -- not because they were reached at a different number, but because they are a different individual. (An earlier version of this note used 'her workplace' as an example of a different person and could be misread as meaning a work phone number; it has been replaced below with an unambiguous same-person, different-number example.) Each separate debt in collection is also counted separately (special aggregation rule for student loans serviced under a single account number, see 12 CFR 1006.14(b)(4)). CORRECTED 2026-09-04 (round 43): the count is ALSO per DEBT COLLECTOR. 1006.14(b)(2)(i) measures calls 'the debt collector places' -- each collector has its own 7-in-7 bucket for a given person and debt. When the same charged-off account is worked by two entities in one week (a debt buyer's in-house staff, then the outside agency it placed the file with), 6 calls from each is 12 calls to the consumer but under the ceiling as against EACH collector; the presumption of violation does not arise against either. The consumer's theory in that pattern is the rebuttable 1006.14(a)/(b)(1) and 1692d(5) aggregate-harassment analysis (see presumption_type and multi_debt_aggregate_volume_note), pleaded against the collector whose own conduct supports it -- not a 7-in-7 presumption aggregated across defendants. Note the in-house staff of a debt BUYER may themselves be covered (principal-purpose prong; see FDCPA-COVERAGE node), so both entities may be defendants, each on its own count. NOT CHANGED 2026-09-05 (round 46) despite a Stage B finding in run_20260904T221748Z.json that calls to the consumer's MOTHER placed in an effort to reach the consumer are 'plausibly' calls to the consumer: the regulation counts calls 'to a particular person,' the Official Interpretation's own example (comment 14(b)(2)(i)-1.iii) applies the 7-in-7 count separately to a third party called for location information, and nothing in the text aggregates a relative's calls with the consumer's. The mother's calls are governed by the location-information rules (one contact absent a request or reasonable belief the earlier answer was wrong, no mention of the debt: 1692b(1)-(3), 1006.10) -- which six calls plainly exceed -- and the aggregate pattern is a rebuttal factor under 1006.14(a). The node already routes there (third_party_communication_note). Classified NOT-A-GAP with this reasoning recorded.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**exclusions_from_count**

- calls made with the person's prior consent given directly to the debt collector, within 7 days of that consent -- CORRECTED 2026-09-01 (round 33): this exclusion (and the two below) apply to BOTH the raw >7-count test AND the post-conversation 7-day cooldown test, per the regulatory chapeau ('do not count toward the telephone call frequencies described in paragraph (b)(2)(i)', and (b)(2)(i) covers both tests). A consumer-requested callback within the cooldown window (e.g., 'call me back Thursday') is therefore NOT a presumptive violation if made with her prior consent given directly to the collector -- this node previously implied the cooldown test had no consent carve-out at all.
- calls not connected to the dialed number -- VERIFIED 2026-09-04 (round 41) against the CFPB's Official Interpretation, comment 14(b)(3)(ii)-1: a call is 'not connected' only if, e.g., the collector gets a busy signal or a not-in-service indication. A call that is answered (even if it then drops), that rings unanswered, or that reaches voicemail or a recorded message (even if no message can be left) IS connected and counts toward the 7-in-7 frequencies. Do NOT treat unanswered or voicemail calls as excluded. (Replaces the round-33 UNVERIFIED note, whose reading is now confirmed.)
- calls to certain third parties under §1006.6(d)(1)(ii)-(vi), not encoded in this node

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**determination**

presumptively_unlawful under FEDERAL law if call_count_in_trailing_7_days > 7 for the same debt AND same recipient AND placed by the SAME debt collector (per-collector bucket, corrected round 43), OR a call is placed within 7 days after a conversation about that same debt with that same recipient -- SUBJECT TO: (a) the FDCPA coverage threshold above (if the caller is not a covered 'debt collector', this node's federal presumption does not apply at all); (b) the (b)(3) exclusions (see exclusions_from_count -- CORRECTED 2026-09-01: these exclusions apply to BOTH the raw >7 count AND the post-conversation cooldown, not just the raw count); and (c) any stricter state-law limit (see state_law_may_be_stricter_note) that may render the same conduct unlawful even where the federal 7-in-7 presumption is not triggered.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**fdcpa_coverage_threshold_note**

This node's 7-in-7 rule is a Regulation F rule and only applies to covered 'debt collectors' under 15 U.S.C. 1692a(6) -- it does NOT apply to an original creditor collecting its own debt in its own name, or a servicer that acquired the debt while it was not yet in default. See the dedicated FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6 node for the full two-test coverage analysis (principal-purpose test vs. regularly-collects-for-another test), the (A)-(F) exclusions, and the Henson v. Santander debt-buyer nuance -- do not re-derive coverage inline here. CLARIFIED 2026-09-01 (round 34): the dedicated gate node's coverage analysis now also screens whether the underlying obligation is a 'debt' under 15 U.S.C. 1692a(5) at all (i.e., a consumer, personal/family/household-purpose obligation) -- a business/commercial debt is outside the FDCPA and this node's Reg F rule entirely, no matter how squarely the caller fits the 'debt collector' definition. Confirm coverage on BOTH dimensions (who is calling, and what is being collected) at the gate node before applying this node's 7-in-7 analysis.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**state_law_may_be_stricter_note**

This node encodes only the FEDERAL Reg F 7-in-7 safe harbor. Several states impose stricter call-frequency or communication-frequency limits under their own debt collection statutes/regulations -- e.g. Massachusetts (940 CMR 7.04(1)(f)) limits creditors (not just FDCPA 'debt collectors' -- a broader class) to two telephone communications per 7-day period, per debt, well below the federal 7-call ceiling. A call pattern that is presumptively lawful under this node's federal analysis can still be unlawful under a stricter state law. This node's checklist did not previously ask for the consumer's state -- a genuine, easy-to-miss gap for any consumer in a stricter-state jurisdiction. Only Massachusetts is currently encoded with a verified primary-source citation; other states' limits are flagged as HORIZON, not encoded. DEFERRED 2026-09-01 (round 32): a Stage B live-run finding also flagged California's Rosenthal Fair Debt Collection Practices Act (Cal. Civ. Code § 1788 et seq.) as a likely second state example -- unlike the federal FDCPA, the Rosenthal Act's 'debt collector' definition is reported to reach original creditors collecting their own consumer debts, which would mean this node's coverage-threshold gate (see FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6) does not fully exclude California in-house creditor calling campaigns from state-law exposure even where it excludes them federally. NOT yet encoded here: live verification of the exact statutory text failed this session (leginfo.legislature.ca.gov timed out 3 times) and per standing discipline this corpus does not encode quoted statutory text without a live fetch. Flagged for a follow-up round, not silently assumed true.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**what_counts_as_a_call_note**

ADDED 2026-09-01 (round 32): the 7-in-7 count in 12 CFR 1006.14(b)(2)(i) is limited to 'telephone call[s]' -- it does NOT include text messages or emails, even though Regulation F separately treats texts and emails as electronic communications subject to their own rules. A fact pattern mixing channels (e.g., several phone calls plus several texts about the same debt in one week) is NOT simply added together into one 7-count bucket, and staying under 7 phone calls does not mean the overall contact pattern is lawful: text messages and emails are separately governed by 12 CFR 1006.6(b) (time/place-of-communication limits, which apply regardless of channel), 12 CFR 1006.14(h) (unusual or inconvenient communication methods, and the electronic-communication opt-out right), and the general FDCPA § 806/1692d harassment standard, which is not satisfied merely by staying under the 7-call phone count. This node encodes only the phone-call-specific 7-in-7 safe harbor; a text/email-heavy fact pattern needs those other provisions, not yet separately encoded as their own nodes (HORIZON).

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**third_party_communication_note**

ADDED 2026-09-01 (round 33): this node's unit_of_count note states that a genuinely different person (e.g., the consumer's mother) gets her own separate 7-call bucket FOR PURPOSES OF THIS NODE'S 7-IN-7 COUNT. That is true but incomplete on its own: 15 U.S.C. 1692c(b) SEPARATELY AND GENERALLY PROHIBITS a debt collector from communicating with any third party about the debt at all, subject only to narrow exceptions (the consumer's own prior consent, court permission, certain post-judgment remedies, or the location-information exception in 1692b). Even the location-information exception is itself narrow: at most ONE call to that person absent a request or a reasonable belief the prior answer was wrong (1692b(3)), and the collector may NOT even state that a debt is owed (1692b(2)). A pattern of repeated calls to a relative that mention the debt -- even if well under 7 calls, and even though this node's own 7-in-7 count would treat those calls as presumptively lawful in isolation -- is very likely a separate, more direct FDCPA violation under 1692c(b)/1692b. This node's 7-in-7 rule and the third-party-communication rules are DIFFERENT, BOTH-APPLICABLE bodies of law, not alternatives -- clearing one does not clear the other. CORRECTED 2026-09-04 (round 41): the sentence above about 'a relative' is too broad. Under 15 U.S.C. 1692c(d), for every rule in section 1692c -- including the (b) third-party bar -- 'consumer' INCLUDES the consumer's spouse, the parent of a minor consumer, a guardian, executor, or administrator (Reg F 1006.6(a) adds a confirmed successor in interest). Calls to the consumer's HUSBAND or WIFE that mention the debt are therefore NOT third-party communications under 1692c(b) and are not per se unlawful on that ground. They are still subject to (i) this node's 7-in-7 count -- the spouse is a different 'particular person,' so those calls get their own bucket and four calls in a week to him is under the ceiling; (ii) 1692c(a)'s time/place/attorney limits; (iii) any cease-communication notice; and (iv) 1692d/1006.14(a) generally. The 1692c(b)/1692b analysis in this note applies to relatives OUTSIDE the 1692c(d) list -- a sibling, an adult child, a parent of an adult consumer, a roommate -- for whom the 'relative' warning stands as written.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**cease_communication_and_representation_note**

ADDED 2026-09-01 (round 34): this node's 7-in-7 safe harbor answers only ONE question -- call volume/frequency. It does NOT clear a call pattern that otherwise violates 15 U.S.C. § 1692c(a) or (c), which apply independently of how many calls were placed: (1) § 1692c(a)(1) -- calls at an unusual or inconvenient time/place; absent contrary knowledge, before 8am or after 9pm local to the consumer is presumptively inconvenient; (2) § 1692c(a)(2) -- any call to a consumer the collector knows (or can readily ascertain) is represented by an attorney on this debt, once that attorney has been given a reasonable chance to respond; (3) § 1692c(a)(3) -- calls to the consumer's workplace once the collector knows or has reason to know the employer prohibits such calls; and (4) most sharply, § 1692c(c) -- once a consumer sends a WRITTEN cease-communication notice (or a written refusal to pay), the collector must stop calling almost entirely, subject only to narrow exceptions (terminating collection efforts, or notifying of specific remedies about to be invoked). A call pattern well under 7 calls in 7 days can still be a clear, independent violation under any of these four provisions -- this node's 'presumptively compliant' output must never be read as clearing them.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**multi_debt_aggregate_volume_note**

ADDED 2026-09-04 (round 41), from the first live run under the disposition-aware gate (run_20260904T184830Z): a single agency holding SEVERAL of one consumer's accounts (five medical accounts, a telecom and two retail-card debts, etc.) may lawfully make up to 7 calls per debt per 7 days -- the Bureau's own example (comment 14(b)(4)-2.i) blesses 21 calls in a week across three debts. So this node's per-debt count is CORRECT as the presumption, and it will call a 28-calls-a-week pattern across five accounts 'presumptively compliant' under 1006.14(b)(2)(i). That is not the end of the analysis: (1) the presumption of compliance is rebuttable, and the aggregate 'frequency and pattern of telephone calls the debt collector places to a person, including the intervals between them' is the FIRST listed rebuttal factor (comment 14(b)(2)(i)-2.i) -- a consumer receiving four calls a day from one collector has a factual case that the natural consequence is harassment under 1006.14(a)/(b)(1) and 15 U.S.C. 1692d(5) even though no single debt's count exceeds 7; (2) a call that mentions more than one debt counts against EACH of them (comment 14(b)(4)-1.i), and a conversation touching several debts starts the 7-day cooldown for each (comment 14(b)(4)-1.ii); (3) stricter state law (e.g., Massachusetts, two per 7 days 'for each debt') applies its own per-debt count. Output 'presumptively compliant -- presumption rebuttable on aggregate pattern; refer for review' rather than a bare 'compliant' whenever the aggregate exceeds 7 per week across the collector's accounts.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**independent_bars_note**

ADDED 2026-09-04 (round 43), from run_20260904T212407Z.json: two further bars that make the CALL COUNT IRRELEVANT and that this node did not screen for, both dangerous-direction (the node would say 'presumptively compliant' to a consumer with a clean, independent claim). (1) VALIDATION DISPUTE, 15 U.S.C. 1692g(b): if within the 30-day validation window the consumer sent a WRITTEN dispute or a written request for the original creditor's name and address, the collector 'shall cease collection of the debt' -- every collection call included -- until it mails verification (or the original creditor's name and address). One call during that suspension is a 1692g(b) violation regardless of frequency; four a week is four violations. A consumer's written dispute is neither a 1692c(c) cease-communication notice nor merely a 'rebuttal factor'; it is its own bar. See FDCPA-VALIDATION-NOTICE-1692g for the window mechanics. (2) BANKRUPTCY: a pending case makes each collection call on a pre-petition debt an 'act to collect' stayed by 11 U.S.C. 362(a)(6); after discharge, 524(a)(2) enjoins any 'act, to collect' the discharged debt as a personal liability. Remedies run through the bankruptcy court (contempt; damages under 362(k) for a willful stay violation), and a call that represents the debt as owed may also be a 1692e(2)(A) misrepresentation; a debtor with bankruptcy counsel is also 'represented' for 1692c(a)(2). Notice to the collector matters for willfulness and damages, not for whether the stay applies. Both are screened in the checklist; either one, if present, is the answer -- do not reach the 7-in-7 count first.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**temporal_screen_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: ask WHEN the calls occurred. The private right of action under 15 U.S.C. 1692k(d) must be brought 'within one year from the date on which the violation occurs' -- per call, from the call date, not from discovery (Rotkiske v. Klemm). A pattern from 16 months ago may still be relevant as evidence of a course of conduct, as a complaint to the CFPB or a state regulator (no private limitations period), or under a state statute with a longer period (e.g., the Rosenthal Act's one year under Cal. Civ. Code 1788.30(f), Tex. Fin. Code ch. 392 -- check), but the federal claim itself is gone. Reg F (effective November 30, 2021) also does not reach calls made before that date; pre-Reg F call patterns are analyzed under 1692d(5) case law alone. Threshold checklist item added.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**tcpa_overlay_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json; HORIZON. Six calls in a week to a cell phone is under this node's federal ceiling, but if the calls used a PRERECORDED OR ARTIFICIAL VOICE (or, for older patterns, an autodialer as narrowed by Facebook v. Duguid, 592 U.S. 395 (2021)) and were placed without the called party's prior express consent, each call may be a separate violation of the Telephone Consumer Protection Act, 47 U.S.C. 227(b)(1)(A)(iii), carrying $500 statutory damages per call ($1,500 if willful) -- independent of the FDCPA and of the 7-in-7 count. Consent given to the original creditor on the application generally carries to its collector; revocation by any reasonable means cuts it off. NOT encoded as a rule here (statute named, not fetched this round; a TCPA node is on the HORIZON list); the checklist now asks whether the calls were live, prerecorded, or ringless voicemail so the referral is not missed.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. WHEN did the calls occur? The private FDCPA/Reg F claim must be filed within ONE YEAR of each call (15 U.S.C. 1692k(d), from the violation, not discovery); calls before November 30, 2021 predate Reg F's 7-in-7 presumption entirely. Older patterns: regulator complaint, course-of-conduct evidence, or a state claim with a longer period  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. THRESHOLD, before counting anything: (a) is the consumer in a pending bankruptcy case, or was this debt discharged in one (11 U.S.C. 362(a)(6) / 524(a)(2) -- every collection call is barred, count irrelevant); (b) did the consumer send a WRITTEN dispute or original-creditor request within 30 days of the validation notice, and has the collector mailed verification since (15 U.S.C. 1692g(b) -- all collection, calls included, must stop until it does)?  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. Which ENTITY placed each call -- the 7-in-7 count is per debt collector, per person, per debt; calls from two different collectors working the same account in the same week are counted separately, and a combined total over 7 is analyzed as rebuttable aggregate harassment (1006.14(a)/1692d(5)), not as a 7-in-7 presumption  (dispositive)  [ ] keep  [ ] change  [ ] drop
4. Dates/times of all calls from this collector regarding this specific debt over the relevant period  (dispositive)  [ ] keep  [ ] change  [ ] drop
5. Whether any telephone CONVERSATION about the debt occurred between the consumer and the collector in the period -- regardless of who placed that call (a consumer's own inbound call to dispute the balance counts; comment 14(b)(2)(i)-1.ii) -- and its date: it opens a 7-day window in which any collector-placed call about that debt is presumptively unlawful absent the consumer's prior consent to be called back  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. Whether the consumer gave prior consent to more frequent contact, and when  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. Whether this is one debt or multiple debts (each counted separately, except aggregated student loans under one account number)  (dispositive)  [ ] keep  [ ] change  [ ] drop
8. If the same collector holds MORE THAN ONE of this consumer's debts: the per-debt counts (each up to 7 per 7 days) AND the aggregate -- total calls per week and per day, shortest interval between calls, whether any call or conversation mentioned more than one debt (it counts against each). A per-debt count under 7 is only a presumption; a concentrated aggregate pattern (e.g., four calls a day from one agency) is the first listed factor that can rebut it (comment 14(b)(2)(i)-2.i)  (dispositive)  [ ] keep  [ ] change  [ ] drop
9. Whether the consumer had previously told this collector not to call, that she refuses to pay, or that she does not owe the debt, or sent a cease-communication or no-telephone-calls request -- prior-communication content is a rebuttal factor against the presumption of compliance even when the count stays under 7 (comment 14(b)(2)(i)-2.iii)  (dispositive)  [ ] keep  [ ] change  [ ] drop
10. Whether the caller is a covered 'debt collector' under 15 U.S.C. 1692a(6) -- an original creditor collecting its own debt in its own name, or a servicer that acquired the debt while it was not yet in default, is NOT covered by this node's Reg F analysis at all  (dispositive)  [ ] keep  [ ] change  [ ] drop
11. Whether calls to different people (e.g. the consumer, a family member, the workplace) about the same debt are being wrongly added together -- the 7-call count is per person AND per debt, not aggregated across different call recipients  (dispositive)  [ ] keep  [ ] change  [ ] drop
12. The consumer's state -- some states (e.g. Massachusetts, 940 CMR 7.04(1)(f)) impose stricter call-frequency limits than the federal 7-in-7 safe harbor, and can reach original creditors that Reg F's 'debt collector' definition would exclude  (dispositive)  [ ] keep  [ ] change  [ ] drop
13. If the consumer was called at more than one number (cell, home, work) about the same debt within the same window, confirm those calls were aggregated into ONE 7-call count for that person+debt, not treated as separate counts per number  (dispositive)  [ ] keep  [ ] change  [ ] drop
14. If the contact pattern includes text messages or emails in addition to phone calls, confirm this node's phone-only 7-in-7 count is not being used as the sole answer -- texts/emails are governed by separate Reg F provisions (1006.6(b), 1006.14(h)) not yet encoded here  (dispositive)  [ ] keep  [ ] change  [ ] drop
15. If relying on the prior-consent exclusion for a call placed during the post-conversation 7-day cooldown (not just the raw count), confirm the consent was given directly to the collector and the call falls within 7 days of that consent  (dispositive)  [ ] keep  [ ] change  [ ] drop
16. If any of the calls in question were placed to someone OTHER than the consumer: first check whether that person is the consumer's spouse, the parent of a minor consumer, a guardian, executor or administrator (15 U.S.C. 1692c(d); 12 CFR 1006.6(a)) -- if so, they ARE the 'consumer' for section 1692c and the third-party bar does not apply; if not (sibling, adult child, parent of an adult, roommate, employer), separately check 1692c(b)/1692b's third-party-communication restrictions -- clearing this node's 7-in-7 analysis does not clear that separate, generally-prohibitive rule  (dispositive)  [ ] keep  [ ] change  [ ] drop
17. Whether the consumer has sent the collector a WRITTEN notice refusing to pay or demanding the collector cease communication (15 U.S.C. 1692c(c)) -- if so, nearly all further contact about this debt is independently unlawful regardless of the 7-in-7 count  (dispositive)  [ ] keep  [ ] change  [ ] drop
18. Whether any of the calls were placed at an unusual/inconvenient time or place (before 8am/after 9pm local to the consumer, presumptively), to a known-prohibited workplace, or to a consumer the collector knows is represented by an attorney on this debt (15 U.S.C. 1692c(a)) -- each is independently unlawful regardless of the 7-in-7 count  (dispositive)  [ ] keep  [ ] change  [ ] drop
19. Were the calls LIVE, PRERECORDED/artificial-voice, or ringless voicemail, to a CELL phone, and had the consumer ever consented (on the credit application or since) or revoked consent? Prerecorded-voice calls to a cell without consent are a separate TCPA matter (47 U.S.C. 227(b)(1)(A)(iii)) regardless of the 7-in-7 count -- refer, not encoded here  (non-dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | 12 C.F.R. § 1006.14(b)(2)(i)-(ii) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14 |
| 2 | 12 C.F.R. § 1006.14(b)(4) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14 |
| 3 | 15 U.S.C. § 1692a(6) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692a&num=0&edition=prelim |
| 4 | 940 CMR 7.04(1)(f) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/regulations/massachusetts/940-CMR-7-04 |
| 5 | 12 C.F.R. § 1006.14(b)(3) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14 |
| 6 | 15 U.S.C. § 1692c(b) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692c&num=0&edition=prelim |
| 7 | 15 U.S.C. § 1692b(2)-(3) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692b&num=0&edition=prelim |
| 8 | 15 U.S.C. § 1692c(a) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692c&num=0&edition=prelim |
| 9 | 15 U.S.C. § 1692c(c) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692c&num=0&edition=prelim |
| 10 | 15 U.S.C. § 1692c(d) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692c&num=0&edition=prelim |
| 11 | 12 C.F.R. § 1006.6(a) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.6 |
| 12 | 12 C.F.R. pt. 1006, Supp. I, comment 14(b)(4)-2.i (Official Interpretations) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/cfr/text/12/appendix-Supplement_I_to_part_1006 |
| 13 | 12 C.F.R. pt. 1006, Supp. I, comment 14(b)(2)(i)-2 and -2.i (Official Interpretations) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/cfr/text/12/appendix-Supplement_I_to_part_1006 |
| 14 | 12 C.F.R. pt. 1006, Supp. I, comment 14(b)(2)(i)-1.ii (Official Interpretations) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/cfr/text/12/appendix-Supplement_I_to_part_1006 |
| 15 | 12 C.F.R. pt. 1006, Supp. I, comment 14(b)(3)(ii)-1 (Official Interpretations) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/cfr/text/12/appendix-Supplement_I_to_part_1006 |
| 16 | 15 U.S.C. § 1692g(b) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692g&num=0&edition=prelim |
| 17 | 11 U.S.C. § 362(a)(6) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title11-section362&num=0&edition=prelim |
| 18 | 11 U.S.C. § 524(a)(2) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title11-section524&num=0&edition=prelim |
| 19 | 15 U.S.C. § 1692k(d) | A | ADDED AFTER last run (round 46) -- not yet live-checked | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692k&num=0&edition=prelim |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | yes | Multiple accounts with one collector: per-debt count treats ~28 calls/week as presumptively compliant | Per-debt counting CONFIRMED correct by Official Interpretation comment 14(b)(4)-2.i (21 calls/3 debts/7 days presumed compliant); added multi_debt_aggregate_volume_note, rebuttal-factor checklist items and presumption_type rewrite from comment 14(b)(2)(i)-2 so the aggregate pattern is surfaced as a rebuttal case rather than a bare 'compliant' |
| 02 | FIXED-VERIFIED | yes | Consumer-initiated telephone conversation not treated as starting the 7-day cooldown; checklist gathered outbound calls only | Checklist item 2 reworded; cooldown_rule clarified; comments 14(b)(2)(i)-1.ii and 14(b)(4)-1.ii pinned ('regardless of which party initiated') |
| 03 | FIXED-VERIFIED | no (over-warns the consumer; misdirects the claim) | Spouse (and parent of minor / guardian / executor / administrator) treated as a 1692c(b) third party | 1692c(d) and 12 CFR 1006.6(a) pinned; third_party_communication_note corrected; checklist item reworded to test 1692c(d) status first |
| 04 | FIXED-VERIFIED | n/a (pre-existing marker closed) | 'Not connected to the dialed number' exclusion scope (unanswered / voicemail calls count) | Round-33 UNVERIFIED reading confirmed and pinned from comment 14(b)(3)(ii)-1 |
| 05 | FIXED-VERIFIED | yes | Written validation dispute (1692g(b)) suspends all collection incl. calls; node counted calls anyway | independent_bars_note + threshold checklist item; 1692g(b) pinned |
| 06 | FIXED-VERIFIED | yes | Pending bankruptcy / discharge not screened (362(a)(6), 524(a)(2)) | independent_bars_note + threshold checklist item; 362(a)(6) and 524(a)(2) pinned; also registered as a GLOBAL disposition |
| 07 | FIXED-VERIFIED | no (overstates claim, wrong defendant) | 7-in-7 count not stated as per debt collector; two collectors' calls aggregated into one presumption | unit_of_count and determination corrected; checklist item on which entity placed each call |
| 08 | FIXED-VERIFIED | no (overstates claim) | No temporal screen; 1692k(d) one-year limit | 1692k(d) pinned; temporal_screen_note + threshold checklist |
| 09 | HORIZON (statute named; TCPA node) | yes | TCPA overlay for prerecorded calls to cell phones | tcpa_overlay_note + checklist; 47 U.S.C. 227(b)(1)(A)(iii) named |
| 10 | NOT-A-GAP (node correct; reason recorded) | n/a | Calls to a relative seeking the consumer counted against the consumer's bucket | Reg text counts calls 'to a particular person'; comment 14(b)(2)(i)-1.iii; 1692b governs the relative's calls -- recorded in unit_of_count |

**Drafting revisions (author / date / summary):**

- 2026-09-01 — Added 15 U.S.C. 1692a(6) (FDCPA 'debt collector' coverage threshold -- this node's rule doesn't reach original creditors or servicers of then-current loans) and 940 CMR 7.04(1)(f) (Massachusetts state-law overlay, stricter than the federal 7-in-7 safe harbor, as a verified example) as new derived_fr
- 2026-09-01 — Shortened this node's fdcpa_coverage_threshold_note from a full inline re-derivation of 15 U.S.C. 1692a(6) coverage to a brief cross-reference to the new standalone FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6 node, which now carries the full two-test analysis, all statutory exclusions, and the Henson v. Sa
- 2026-09-01 — Rewrote unit_of_count to unambiguously state that calls to the same consumer at different phone numbers are aggregated into one 7-call bucket (only a genuinely different person gets a separate bucket), replacing an ambiguous 'her workplace' example that could be misread as a different-number case. A
- 2026-09-01 — Corrected exclusions_from_count to state the consent/not-connected/third-party exclusions apply to BOTH the raw >7 count and the post-conversation cooldown. Added third_party_communication_note (1692c(b) generally prohibits contacting third parties about the debt; the narrow 1692b location-informati
- 2026-09-01 — Added 15 U.S.C. 1692c(a) (inconvenient time/place, workplace, attorney-representation restrictions) and 1692c(c) (written cease-communication notice) derived_from entries and a new cease_communication_and_representation_note explaining these apply independently of the 7-in-7 count. Added 2 completen
- 2026-09-02 — Dropped the subsection heading from the 1692c(b) quoted_text so it starts at the verbatim body text.
- 2026-09-04 — Round 41: (1) NOT a content error -- comment 14(b)(4)-2.i confirms per-debt counting (21 calls/3 debts/7 days presumed compliant); added multi_debt_aggregate_volume_note + two checklist items surfacing the rebuttal factors in comment 14(b)(2)(i)-2 and rewrote presumption_type from the Official Inter
- 2026-09-04 — Round 43: independent_bars_note + threshold checklist item (1692g(b) pinned from the validation node; 11 U.S.C. 362(a)(6) and 524(a)(2) pinned from official fetches); unit_of_count and determination corrected to per-collector; new checklist item on which entity placed each call; comment 14(b)(3)(ii)
- 2026-09-05 — Round 46: 1692k(d) pinned + temporal_screen_note + threshold checklist; tcpa_overlay_note (HORIZON, statute named) + checklist; the relative-calls finding classified NOT-A-GAP with the regulatory basis recorded in unit_of_count.

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed True · material findings 3 (all dispositioned in round 46; see D)

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---

## 4. FDCPA-FALSE-DECEPTIVE-CATALOG-1692e

**Title:** Catalog: false, deceptive, or misleading representations prohibited in debt collection  
**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `363bdaac3427c4cb8895d2597bb17386bd67aacaf1c527d3eb3745c5b1b2ad42`

**Reading load:** logic 1,630 words · checklist 627 · cited text 2,882 · 13 citations · 17 checklist items · 7 drafting revisions

### A. Logic (read in full; this is the content being certified)

**note_re_scope**

16 statutory items encoded as a checklist-style catalog; item (11)'s 'mini-Miranda' disclosure duty is elaborated by Reg F §1006.18(e), included alongside the statute per the same both-sources discipline as the validation-notice node. Item (11)'s mini-Miranda duty (and Reg F §1006.18(e)) does not apply to a formal pleading made in connection with a legal action -- see the exception clause in both the statute and regulation text above.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**catalog_items**

- (1) falsely claiming government affiliation/vouching
- (2)(A) falsely representing the character, amount, or legal status of the debt
- (2)(B) falsely representing services rendered or lawful compensation
- (3) falsely claiming to be, or to communicate from, an attorney
- (4) threatening arrest/imprisonment or unlawful/unintended property seizure for nonpayment
- (5) threatening any action that cannot legally be taken or isn't intended
- (6)(A)-(B) falsely implying a sale/referral/transfer of any interest in the debt will cause the consumer to lose a claim or defense, or become subject to a new violation of this subchapter
- (7) falsely representing/implying the consumer committed a crime or other conduct in order to disgrace the consumer
- (8) communicating known-or-should-be-known-false credit information, including failing to note a debt is disputed
- (9) using or distributing simulated/falsely-represented court or official documents
- (10) any other false representation or deceptive means to collect or obtain consumer information
- (11) failing the mini-Miranda disclosure (see Reg F §1006.18(e) above)
- (12) falsely claiming accounts were sold to an innocent purchaser for value
- (13) falsely representing documents as legal process
- (14) using a business name other than the collector's true name
- (15) falsely representing that documents are not legal process / require no action
- (16) falsely claiming to operate or be employed by a consumer reporting agency

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**determination**

any single catalog item, if the facts match, is an independent §1692e violation — items are not cumulative requirements, each stands alone

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**threshold_predicates**

- The contacting entity must be a 'debt collector' under 15 U.S.C. § 1692a(6) -- an original creditor collecting its own debt in its own name is generally excluded (see derived_from above); this catalog does not apply to that entity at all UNDER THE FEDERAL ACT -- but see state_law_reaches_original_creditors_note: state analogs (e.g. California's Rosenthal Act, Texas Fin. Code ch. 392) may cover the identical conduct by an original creditor.
- The obligation must be a 'debt' under 15 U.S.C. § 1692a(5) -- incurred primarily for personal, family, or household purposes, not a business/commercial obligation.
- Even a third-party servicer or assignee is NOT a 'debt collector' under § 1692a(6)(F)(iii) if it obtained the debt BEFORE it went into default (e.g., a mortgage servicer that began servicing while the loan was current). This is a separate, narrower exclusion from the general original-creditor exclusion above -- a servicer/assignee is neither 'original creditor' nor a covered third-party collector in that scenario.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**materiality_note**

This catalog's determination ('any single catalog item, if the facts match, is an independent violation') omits the materiality floor courts read into § 1692e: a technically-false statement that could not plausibly influence a consumer's response to the debt (e.g., a trivial date or one-cent amount error unrelated to what the consumer would actually decide or do) is generally not actionable. This node does not itself apply a materiality filter to a catalog-item match.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**stale_debt_note**

Filing or threatening suit on a debt outside the applicable statute of limitations (see the state-layer SOL nodes, e.g. CA-SOL-WRITTEN-CONTRACT-DEBT / TX-SOL-CONSUMER-DEBT) is a core, high-volume § 1692e theory under (2)(A) and (5) -- and, in some circuits, even a dunning letter alone without a litigation threat can violate § 1692e if it could mislead a consumer about a time-barred debt's enforceability. Neither the catalog gloss nor the prior checklist asked about the debt's age or the applicable limitations period.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**coverage_threshold_node_ref**

For the full FDCPA 'debt collector' coverage analysis underlying threshold_predicates[0] and [2] above (the two independent coverage tests, all statutory exclusions (A)-(F), and the Henson v. Santander nuance on debt buyers), see the dedicated FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6 node.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**fdcpa_claim_limitations_note**

ADDED 2026-09-03 (round 38): this catalog answers whether conduct VIOLATED the section; it does not by itself mean the consumer still has a live private claim. 15 U.S.C. 1692k(d) gives a ONE-YEAR limitations period for FDCPA private actions, running from the date the violation occurs -- the Supreme Court held in Rotkiske v. Klemm (2019) (both now quoted in derived_from) that this is occurrence-based, not discovery-based (absent equitable doctrines). Consumers very commonly surface old dunning letters only after later credit damage or litigation; a letter more than a year old matches the catalog but the federal claim is presumptively time-barred. The checklist asks about the STATE limitations period on the underlying debt but previously never asked about the federal limitations period on the CLAIM.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**state_law_reaches_original_creditors_note**

ADDED 2026-09-03 (round 38): the original-creditor exclusion in the threshold predicates is a FEDERAL-only conclusion. Several state debt-collection statutes reach creditors collecting their own debts and incorporate the federal conduct standards by reference -- most prominently California's Rosenthal Fair Debt Collection Practices Act (Cal. Civ. Code 1788.2(c) defines 'debt collector' to include a creditor collecting in its own name; 1788.17 incorporates 1692b-1692j), and Texas Finance Code ch. 392 likewise applies to creditors as well as third-party collectors. A consumer told 'this catalog does not apply at all' because the caller was her own bank may have a strong STATE claim for the identical conduct (arrest threats, misstated balances). No state mini-FDCPA node exists in this corpus yet (HORIZON); until one does, treat 'original creditor -> not covered' as 'not covered under the FEDERAL Act -- check the consumer's state.' PINNED 2026-09-04 (round 39): both Rosenthal provisions are now quoted in derived_from. Carve-out to note: § 1788.17 excludes 1692e(11) (mini-Miranda) and 1692g (validation notice) as against original creditors and their employees -- so a Rosenthal claim against a creditor collecting its own debt lies for arrest threats, misstated balances, and the rest of 1692e, but NOT for a missing mini-Miranda or a missing validation notice.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**article_iii_standing_note**

ADDED 2026-09-03 (round 38): a catalog match establishes a statutory violation, but a private suit in FEDERAL court also requires Article III standing -- a concrete injury. After TransUnion LLC v. Ramirez (2021) and Spokeo v. Robins (2016), federal courts routinely dismiss 'bare procedural' FDCPA claims (a missing disclosure the consumer read, recognized, and ignored with no confusion, reliance, or detrimental action; an envelope marking no third party saw) for lack of standing, and the circuits differ on which intangible harms qualify. TransUnion's holding is now quoted in derived_from (source_tier A); which FDCPA harms count as 'concrete' remains circuit-dependent and is the part flagged for counsel; it does not change whether conduct is unlawful, only whether a federal-court claim is viable, and state-court standing rules may differ.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**limited_content_message_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: a voicemail that says only a non-collection business name, a request to call back, a natural person's name, and a callback number (plus optional salutation, date/time, suggested reply times, and a 'you may speak to any representative' line) is a LIMITED-CONTENT MESSAGE under 12 CFR 1006.2(j). Reg F treats it as an 'attempt to communicate' (1006.2(b)) but NOT a 'communication' (1006.2(d), 'conveying of information regarding a debt'), so the 1692e(11) initial/subsequent-communication disclosure duty (and the 1006.18(e) mini-Miranda) does not attach to it, and its silence about the debt is not a 1692e(11) violation. Six such voicemails in two weeks are lawful under THIS node; whether they are lawful under the 7-in-7 call-frequency rule is the FDCPA-REGF-CALL-FREQUENCY node's question (a limited-content message counts as a call placed, comment 14(b)(4)-1.i). A voicemail that says ANYTHING more -- the collector's real name if it signals collection, the word 'debt', an account number, an amount -- is not limited-content and the disclosure duty applies in full. Checklist item on subsequent-communication disclosure reworded to screen for this first.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**accurate_but_misleading_balance_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json; GLOSS-FOR-COUNSEL. Catalog item (2)(A) ('false representation of the character, amount, or legal status') is not limited to a balance that is numerically wrong on the day of the letter. A line of authority beginning with Avila v. Riexinger & Associates, LLC, 817 F.3d 72 (2d Cir. 2016), holds that stating a 'current balance' without disclosing that interest or fees are accruing can mislead the least sophisticated consumer into believing that paying the stated figure will satisfy the debt -- and offers a safe harbor (state that the balance may increase due to interest and fees, or that the amount stated will be accepted in full satisfaction if paid by a date). Other circuits have declined to require the disclosure where no interest is in fact accruing (e.g., Chuway v. National Action Financial Services, 362 F.3d 944 (7th Cir. 2004), on the other side of the ledger; and see Taylor v. Financial Recovery Services, 886 F.3d 212 (2d Cir. 2018), no violation where the collector was not adding interest). This is case law, not encoded as a rule; the checklist now collects whether interest or fees were accruing and whether the letter said so. Please confirm or strike.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**bona_fide_error_defense_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: the determination is a statement of what VIOLATES 1692e, not of what a consumer will RECOVER. 15 U.S.C. 1692k(c) gives the collector a complete defense on proof, by a preponderance, that the violation 'was not intentional and resulted from a bona fide error notwithstanding the maintenance of procedures reasonably adapted to avoid any such error.' A $900 overstatement traceable to a creditor's mis-mapped payment file, from a collector with documented intake-reconciliation procedures, is the paradigm case. Limits (GLOSS-FOR-COUNSEL, Jerman v. Carlisle (2010)): the defense reaches clerical and factual mistakes, not mistakes of law about what the FDCPA requires; and the burden is the collector's. A consumer should still be told a violation occurred and that the claim exists -- with the caveat that recovery may turn on the collector's procedures, a discovery question.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. Whether the entity contacting the consumer is collecting its own debt, in its own name, as the original creditor (generally exempt from the FDCPA entirely) vs. a third-party collector or debt buyer  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. Whether the obligation is a personal/family/household debt (covered) vs. a business or commercial debt (not covered)  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. Exact wording of any written communication (letters, texts, emails) from the collector  (dispositive)  [ ] keep  [ ] change  [ ] drop
4. Content of any phone conversations with the collector — what was said, by whom, when (recordings, notes, or memory)  (dispositive)  [ ] keep  [ ] change  [ ] drop
5. Whether the collector disclosed (in the initial communication, and again if the initial contact was oral) that it was attempting to collect a debt and that info would be used for that purpose  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. For each subsequent contact: FIRST, was it a limited-content voicemail (12 CFR 1006.2(j): non-collection business name, request to call back, a person's name, a callback number, nothing else)? If so it is not a 'communication' and the disclosure duty does not apply to it. Otherwise: whether the collector disclosed in EACH subsequent communication that it was a debt collector  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. Any threats made (legal action, arrest, wage/property seizure) and whether the collector actually intended or was legally able to carry them out  (dispositive)  [ ] keep  [ ] change  [ ] drop
8. Whether the communication at issue is a formal pleading filed in a legal action (the item (11) mini-Miranda duty doesn't apply to those)  (dispositive)  [ ] keep  [ ] change  [ ] drop
9. If the entity is a servicer or assignee rather than the original creditor, whether it obtained the debt before or after it went into default (obtained-before-default generally exempts it entirely under § 1692a(6)(F)(iii))  (dispositive)  [ ] keep  [ ] change  [ ] drop
10. The age of the debt and date of last payment/default, and whether the applicable state statute of limitations has run (relevant to whether threatening or filing suit, or even dunning without a threat, violates § 1692e(2)(A)/(5)/(10))  (dispositive)  [ ] keep  [ ] change  [ ] drop
11. Whether the specific false/deceptive statement or omission found is material -- i.e., could plausibly influence how a consumer responds to the debt -- as opposed to a trivial, inconsequential inaccuracy  (dispositive)  [ ] keep  [ ] change  [ ] drop
12. Confirm the contacting entity's covered-'debt collector' status via the full analysis in FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6, not solely the summary in threshold_predicates above  (dispositive)  [ ] keep  [ ] change  [ ] drop
13. Date of the communication or conduct at issue, relative to today -- FDCPA private claims must be filed within ONE YEAR of the violation (15 U.S.C. 1692k(d), occurrence-based); a catalog match on conduct more than a year old is presumptively time-barred as a federal claim  (dispositive)  [ ] keep  [ ] change  [ ] drop
14. The consumer's state -- if the collector is the original creditor (excluded federally), does the state's own debt-collection statute reach creditors (e.g. CA Rosenthal Act, TX Fin. Code ch. 392)? The federal 'not covered' answer is not the end of the analysis  (dispositive)  [ ] keep  [ ] change  [ ] drop
15. What concrete effect the communication had on the consumer (confusion, a payment or other action taken in reliance, a third party who actually saw it, emotional distress) -- relevant to Article III standing for a federal-court suit; a purely technical violation the consumer noticed and ignored may not support a federal claim  (dispositive)  [ ] keep  [ ] change  [ ] drop
16. For any stated balance: was interest, or were fees, accruing on the account at the time, and did the communication say so (or state that the figure would be accepted in full satisfaction)? A static balance on an accruing account is a GLOSS-FOR-COUNSEL misrepresentation theory (Avila line), not a per se violation  (non-dispositive)  [ ] keep  [ ] change  [ ] drop
17. If a misstatement was clerical or factual (wrong balance from the creditor's data, wrong date): what procedures did the collector maintain to catch it -- the 15 U.S.C. 1692k(c) bona fide error defense may defeat recovery even where a catalog item is met (it does not cover mistakes of law)  (non-dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | 15 U.S.C. § 1692e | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/uscode/text/15/1692e |
| 2 | 12 C.F.R. § 1006.18(e) (the 'mini-Miranda' disclosure — Reg F's current operative version of §1692e(11)) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.18 |
| 3 | 15 U.S.C. § 1692a(5) | B | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692a&num=0&edition=prelim |
| 4 | 15 U.S.C. § 1692a(6) | B | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692a&num=0&edition=prelim |
| 5 | 15 U.S.C. § 1692a(6)(F) | B | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692a&num=0&edition=prelim |
| 6 | Materiality requirement (judicial gloss on § 1692e) | D | n/a (doctrine entry, no url by design) | — |
| 7 | Time-barred/stale-debt collection theory (judicial gloss on § 1692e(2)(A), (5), (10)) | D | n/a (doctrine entry, no url by design) | — |
| 8 | 15 U.S.C. § 1692k(d) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692k&num=0&edition=prelim |
| 9 | TransUnion LLC v. Ramirez, 594 U.S. ___ (2021) (syllabus) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/supremecourt/text/20-297 |
| 10 | Cal. Civ. Code § 1788.2(c) (Rosenthal Act) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1788.2. |
| 11 | Cal. Civ. Code § 1788.17 (Rosenthal Act) | A | MANUAL (note recorded; not yet re-confirmed by Andy) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1788.17. |
| 12 | 12 C.F.R. § 1006.2(j) | A | ADDED AFTER last run (round 46) -- not yet live-checked | https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-A/section-1006.2 |
| 13 | 15 U.S.C. § 1692k(c) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692k&num=0&edition=prelim |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | yes | FDCPA's own 1-yr SOL (1692k(d)) never asked | Note + checklist; Rotkiske v. Klemm gloss |
| 02 | FIXED-VERIFIED | yes | Original creditor "not covered at all" ignores Rosenthal/TX ch. 392 | Predicate softened to "under the federal Act"; state mini-FDCPA node is HORIZON |
| 03 | FIXED-VERIFIED | no | Article III standing for bare technical violations | TransUnion/Spokeo note + checklist |
| 04 | FIXED-VERIFIED | no (overstates claim) | Limited-content message (1006.2(j)) treated as a 1692e(11) violation | 1006.2(j) pinned; limited_content_message_note; checklist reworded |
| 05 | GLOSS-FOR-COUNSEL | no | Accurate-but-misleading static balance (Avila line) | accurate_but_misleading_balance_note; checklist |
| 06 | FIXED-VERIFIED + GLOSS (Jerman) | no | Bona fide error defense (1692k(c)) omitted | 1692k(c) pinned; bona_fide_error_defense_note; checklist |

**Drafting revisions (author / date / summary):**

- 2026-08-30 — Added missing catalog items (6) [debt-sale/transfer loss-of-defense misrepresentation] and (7) [false crime/disgrace accusation]; added the 1692a(5)/(6) debt-collector and consumer-debt threshold predicates; noted the formal-pleading exception to item (11). Also corrected the derived_from quoted_tex
- 2026-08-30 — Second pass: added § 1692a(6)(F)(iii) servicer/not-in-default exclusion, the materiality requirement, and the time-barred/stale-debt collection theory; added 3 corresponding checklist items. First pass (round 21) already fixed the (6)/(7) catalog omission and the general 1692a(5)/(6) threshold predi
- 2026-09-01 — Added a lightweight cross-reference (coverage_threshold_node_ref) and one completeness_checklist item pointing to the new FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6 node, so its more complete coverage analysis (principal-purpose test, all exclusions, Henson nuance) is available alongside this node's exist
- 2026-09-02 — Fixed quote characters to match the official text, removed the editorial bracket, re-pinned 1692a(5), 1692a(6), 1692a(6)(F) to uscode.house.gov.
- 2026-09-03 — Added three cross-cutting notes + checklist questions from the backlog (both runs): the FDCPA's own one-year limitations period (1692k(d)), state mini-FDCPA coverage of original creditors (Rosenthal / TX ch. 392), and Article III standing for bare technical violations. Threshold predicate [0] soften
- 2026-09-04 — Pinned 1692k(d) (+Rotkiske), TransUnion, and Cal. Civ. Code 1788.2(c)/1788.17; added the 1788.17 carve-out (no Rosenthal liability for original creditors on 1692e(11)/1692g). Removed 3 SOURCE PENDING markers; standing note now statute/case-anchored.
- 2026-09-05 — Round 46: 1006.2(j) pinned + limited_content_message_note + checklist reword; accurate_but_misleading_balance_note (GLOSS: Avila/Chuway/Taylor) + checklist; 1692k(c) pinned + bona_fide_error_defense_note (Jerman named) + checklist.

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed True · material findings 3 (all dispositioned in round 46; see D)

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---

## 5. FDCPA-UNFAIR-PRACTICES-CATALOG-1692f

**Title:** Catalog: unfair or unconscionable debt-collection practices  
**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `672536815e10ca12293209ce722da673ae776c805dfe4e5728d53acebbfc1c3e`

**Reading load:** logic 1,475 words · checklist 441 · cited text 1,240 · 6 citations · 11 checklist items · 6 drafting revisions

### A. Logic (read in full; this is the content being certified)

**note_re_item_6**

Item (6)'s sub-elements (whether an 'enforceable security interest' exists giving a 'present right to possession') can require legal judgment on the underlying security agreement — flagged as the one catalog item here with more fact/legal-judgment dependency than the others, though the ultimate determination (was nonjudicial repossession threatened/taken without the right to do so) remains a yes/no outcome once that judgment is made.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**catalog_items**

- (1) collecting any amount not expressly authorized by the debt agreement or permitted by law (e.g., unauthorized fees/interest) -- CAVEAT added 2026-09-03 (round 38): 'pay-to-pay' / convenience fees for paying by card or phone that the consumer affirmatively opts into at the time of payment are among the most litigated 1692f(1) fact patterns and courts are split on whether an optional, separately-agreed payment-channel fee is an 'amount' collected 'incidental to the principal obligation' -- do not present that sub-case as a categorical violation; ask whether the fee was optional, disclosed, and agreed to at payment
- (2) depositing a check postdated >5 days without the required 3-10 business day advance written notice
- (3) soliciting a postdated check/instrument to threaten or institute criminal prosecution
- (4) depositing or threatening to deposit a postdated check/instrument before its date
- (5) causing communication charges via concealment of the communication's true purpose (e.g., collect calls, telegram fees)
- (6) threatening/taking nonjudicial repossession without a present enforceable right, without present intent, or where the property is legally exempt
- (7) communicating about the debt by postcard
- (8) using any language or symbol on an envelope or in the address on any envelope (other than the collector's address, and a business name that does not indicate the business is in debt collection) -- NOT limited to symbols that expressly 'indicate debt collection': visible account numbers, scannable barcodes/QR codes, and other identifying marks through a windowed envelope are themselves catalog-item (8) violations even if nothing on the envelope literally says 'debt' or 'collection' (Douglass v. Convergent Outsourcing; Daubert v. NRA Group -- among the most heavily litigated § 1692f fact patterns) -- CAVEAT added 2026-09-03 (round 38): the visible-account-number/barcode rule is a Third Circuit line; the Eighth Circuit (Strand v. Diversified Collection Serv.) and courts following it recognize a 'benign language' exception under which markings that do not indicate debt collection are not violations, and post-TransUnion many envelope-marking claims are dismissed for lack of concrete harm where no third party saw or decoded the marking. Venue matters; this node does not resolve which line the consumer's circuit follows (case-law gloss, source_tier C, flagged for counsel)

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**determination**

any single catalog item, if the facts match, is an independent §1692f violation

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**general_clause_note**

The catalog above is expressly ILLUSTRATIVE, not exhaustive -- § 1692f's own text states the enumerated items apply 'without limiting the general application' of the broader ban on 'unfair or unconscionable means.' A fact pattern that matches none of the 8 catalog items can still violate § 1692f under the general clause -- common examples include garnishing or freezing funds known to be exempt, splitting a single claim into multiple suits to increase fees, or other abusive collection-litigation conduct. This node's 'determination' should not be read as a closed list requiring an item-by-item match -- absence of a catalog-item match does NOT by itself mean no § 1692f violation occurred. CORRECTED 2026-09-05 (round 46), from run_20260904T221748Z.json: an earlier version of this note listed 'continuing to collect a debt known to be discharged in bankruptcy or time-barred' as a general-clause violation. Both were stated too categorically -- see time_barred_debt_note and discharged_debt_note.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**debt_collector_threshold_note**

This entire node applies only if the entity is a 'debt collector' under § 1692a(6) collecting a consumer 'debt.' It does NOT apply to: an original creditor collecting its own debt; a servicer who acquired the loan before it went into default; an in-house collection unit collecting for its own company; or a business/commercial obligation rather than a consumer debt. A very common real fact pattern -- a mortgage servicer or credit-card issuer itself (not a third-party collector) adding an unauthorized fee -- falls outside this node's scope entirely, regardless of how clearly the fee matches catalog item (1); this threshold question should be resolved before applying any catalog item.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**coverage_threshold_node_ref**

For the full FDCPA 'debt collector' coverage analysis underlying debt_collector_threshold_note above (the two independent coverage tests, all statutory exclusions (A)-(F), and the Henson v. Santander nuance on debt buyers), see the dedicated FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6 node.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**fdcpa_claim_limitations_note**

ADDED 2026-09-03 (round 38): this catalog answers whether conduct VIOLATED the section; it does not by itself mean the consumer still has a live private claim. 15 U.S.C. 1692k(d) gives a ONE-YEAR limitations period for FDCPA private actions, running from the date the violation occurs -- the Supreme Court held in Rotkiske v. Klemm (2019) (both now quoted in derived_from) that this is occurrence-based, not discovery-based (absent equitable doctrines). Consumers very commonly surface old dunning letters only after later credit damage or litigation; a letter more than a year old matches the catalog but the federal claim is presumptively time-barred. The checklist asks about the STATE limitations period on the underlying debt but previously never asked about the federal limitations period on the CLAIM.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**article_iii_standing_note**

ADDED 2026-09-03 (round 38): a catalog match establishes a statutory violation, but a private suit in FEDERAL court also requires Article III standing -- a concrete injury. After TransUnion LLC v. Ramirez (2021) and Spokeo v. Robins (2016), federal courts routinely dismiss 'bare procedural' FDCPA claims (a missing disclosure the consumer read, recognized, and ignored with no confusion, reliance, or detrimental action; an envelope marking no third party saw) for lack of standing, and the circuits differ on which intangible harms qualify. TransUnion's holding is now quoted in derived_from (source_tier A); which FDCPA harms count as 'concrete' remains circuit-dependent and is the part flagged for counsel; it does not change whether conduct is unlawful, only whether a federal-court claim is viable, and state-court standing rules may differ.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**time_barred_debt_note**

ADDED 2026-09-05 (round 46): collecting a TIME-BARRED debt is not, by itself, 'unfair or unconscionable.' The Supreme Court held in Midland Funding, LLC v. Johnson, 581 U.S. 224 (2017), that filing an accurate proof of claim on a time-barred debt in a Chapter 13 case violates neither 1692e nor 1692f, and most courts treat non-litigation collection of a time-barred debt (letters, calls, settlement offers) the same way so long as nothing misrepresents that the debt is enforceable in court. What IS prohibited: 12 CFR 1006.26(b) -- a debt collector 'must not bring or threaten to bring a legal action against a consumer to collect a time-barred debt' (strict liability; bankruptcy proofs of claim excepted), and any communication that states or implies the debt can be sued on, or that a partial payment will not revive it where state law says it will (a 1692e(2)(A)/(5)/(10) theory; see FDCPA-FALSE-DECEPTIVE-CATALOG-1692e stale_debt_note). Some states go further and require a time-barred-debt disclosure in every collection letter (e.g., Cal. Civ. Code 1788.14(d), Tex. Fin. Code 392.307(e) for debt buyers) -- state overlays, not this node. GLOSS-FOR-COUNSEL: the 'partial payment revives' misrepresentation theory (Buchanan v. Northland Group, 776 F.3d 393 (6th Cir. 2015); Pantoja v. Portfolio Recovery Associates, 852 F.3d 679 (7th Cir. 2017)).

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**discharged_debt_note**

ADDED 2026-09-05 (round 46): collecting a debt DISCHARGED in bankruptcy is unlawful, but the remedy is not reliably the FDCPA. The discharge injunction (11 U.S.C. 524(a)(2)) is enforced by contempt in the bankruptcy court. Whether the SAME conduct also supports an FDCPA claim is a circuit split: the Ninth Circuit holds the Bankruptcy Code precludes an FDCPA claim premised on a discharge-injunction violation (Walls v. Wells Fargo Bank, 276 F.3d 502 (9th Cir. 2002)), and several courts follow it; the Third and Seventh Circuits allow FDCPA claims alongside the Code (Simon v. FIA Card Services, 732 F.3d 259 (3d Cir. 2013); Randolph v. IMBS, Inc., 368 F.3d 726 (7th Cir. 2004)). A California consumer (Ninth Circuit) should be routed to the bankruptcy court, not told she has a 1692f claim; a Texas consumer (Fifth Circuit) sits in unsettled territory. GLOSS-FOR-COUNSEL for the circuit map; the statutory anchor is 524(a)(2), pinned on the sibling call-frequency node.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**repossession_breach_of_peace_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: catalog item (6) asks whether the collector had a 'present right to possession.' A secured party's self-help repossession right exists only if it can be exercised WITHOUT BREACH OF THE PEACE -- UCC 9-609(b)(2) as enacted in every state (Cal. Com. Code 9609(b)(2); Tex. Bus. & Com. Code 9.609(b)(2)). Cutting a lock, entering a closed garage or fenced yard, proceeding over the debtor's contemporaneous objection, or using or threatening force is the classic breach; a repossession accomplished that way is one the party had no present right to make in that manner, and the item (6) analysis should not stop at 'was the loan in default.' Statute NAMED, not quoted (FIXED-SOURCE-NAMED): the state UCC enactments were not fetched this round. Checklist item added.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. Whether the entity is a 'debt collector' under § 1692a(6) (excludes original creditors, pre-default-acquiring servicers, and in-house collection units) and the obligation is a consumer 'debt' rather than a business/commercial one -- this node does not apply if either threshold fails  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. Whether any collected amount (fees, interest, charges) beyond principal was authorized by the original debt agreement or by law  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. Whether a postdated check/payment was deposited early, or without proper advance written notice  (dispositive)  [ ] keep  [ ] change  [ ] drop
4. Any threats or actions regarding repossession of property, and whether the collector had a present legal right and intent to repossess (or whether the property is exempt — cross-reference the relevant state exemption node) -- AND, for a self-help repossession, HOW it was carried out: a lock cut, a closed garage or fenced area entered, the debtor's on-the-spot objection overridden, or force used or threatened is a breach of the peace that defeats the secured party's right to repossess in that manner (UCC 9-609(b)(2))  (dispositive)  [ ] keep  [ ] change  [ ] drop
5. Whether any communication was sent by postcard, or an envelope revealed debt-collection purpose  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. Whether the facts, even if they match no catalog item, otherwise amount to an unfair or unconscionable collection practice under § 1692f's general clause (e.g., collecting a known-discharged or known-time-barred debt, seizing known-exempt funds, claim-splitting) -- the catalog is illustrative, not exhaustive  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. Confirm the contacting entity's covered-'debt collector' status via the full analysis in FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6, not solely the summary in debt_collector_threshold_note above  (dispositive)  [ ] keep  [ ] change  [ ] drop
8. Date of the conduct at issue, relative to today -- FDCPA private claims must be filed within ONE YEAR of the violation (15 U.S.C. 1692k(d)); conduct more than a year old is presumptively time-barred as a federal claim  (dispositive)  [ ] keep  [ ] change  [ ] drop
9. For a convenience/pay-to-pay fee: was it optional, disclosed, and affirmatively agreed to by the consumer at the time of payment (contested whether that is an 'amount' under item (1))? For an envelope marking: which federal circuit, and did any third party actually see or decode it?  (dispositive)  [ ] keep  [ ] change  [ ] drop
10. If the debt is TIME-BARRED: was suit filed or threatened (12 CFR 1006.26(b), strict liability), or did any communication state or imply the debt is enforceable in court or that a payment will not revive it? Collection by letter or call on a time-barred debt is not itself a 1692f violation (Midland Funding v. Johnson)  (dispositive)  [ ] keep  [ ] change  [ ] drop
11. If the debt was DISCHARGED in bankruptcy: the consumer's state/circuit -- in the Ninth Circuit (California) the remedy is contempt in the bankruptcy court, not an FDCPA claim (Walls v. Wells Fargo); elsewhere both may be available  (dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | 15 U.S.C. § 1692f | B | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/uscode/text/15/1692f |
| 2 | 15 U.S.C. § 1692f (introductory clause) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/uscode/text/15/1692f |
| 3 | 15 U.S.C. § 1692a(6) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692a&num=0&edition=prelim |
| 4 | 15 U.S.C. § 1692k(d) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1692k&num=0&edition=prelim |
| 5 | TransUnion LLC v. Ramirez, 594 U.S. ___ (2021) (syllabus) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/supremecourt/text/20-297 |
| 6 | 12 C.F.R. § 1006.26(b) | A | ADDED AFTER last run (round 46) -- not yet live-checked | https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.26 |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | yes | 1-yr SOL (1692k(d)) | Same as 1692e |
| 02 | GLOSS-FOR-COUNSEL | no | Envelope-marking rule stated categorically (Douglass) ignores 8th Cir. benign-language + standing | Catalog item (8) caveated |
| 03 | GLOSS-FOR-COUNSEL | no | Pay-to-pay/convenience fees stated categorically; courts split | Catalog item (1) caveated + checklist |
| 04 | FIXED-VERIFIED (node was WRONG) | no (overstates claim) | Time-barred debt collection stated as a per se 1692f violation | general_clause_note corrected; 1006.26(b) pinned; time_barred_debt_note (Midland Funding); checklist |
| 05 | FIXED (note) + GLOSS-FOR-COUNSEL | yes (wrong forum in 9th Cir.) | Discharged-debt collection stated as a per se 1692f violation (Walls split) | discharged_debt_note (Walls / Simon / Randolph); checklist |
| 06 | FIXED-SOURCE-NAMED (UCC 9-609(b)(2)) | yes | Breach-of-the-peace condition on self-help repossession omitted | repossession_breach_of_peace_note; item (6) checklist extended |

**Drafting revisions (author / date / summary):**

- 2026-08-30 — Added § 1692f introductory-clause (illustrative-not-exhaustive) and § 1692a(6) debt-collector-definition derived_from entries; added general_clause_note and debt_collector_threshold_note; broadened catalog item (8)'s envelope-symbol scope beyond 'indicating debt collection' per Douglass/Daubert; add
- 2026-09-01 — Added a lightweight cross-reference (coverage_threshold_node_ref) and one completeness_checklist item pointing to the new FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6 node, so its more complete coverage analysis (principal-purpose test, all exclusions, Henson nuance) is available alongside this node's exist
- 2026-09-02 — Fixed quote characters to match the official text, removed the editorial bracket, re-pinned 1692a(6) to uscode.house.gov.
- 2026-09-03 — Added the 1692k(d) one-year note + checklist question and the Article III standing note; softened catalog items (1) (pay-to-pay fees) and (8) (envelope markings) from categorical to venue/consent-dependent with case-law caveats. From the backlog (run 185148Z). 1692k(d) text NOT pinned this session -
- 2026-09-04 — Pinned 1692k(d) (+Rotkiske) and TransUnion. Envelope-marking and pay-to-pay caveats remain circuit-split glosses for counsel.
- 2026-09-05 — Round 46: general_clause_note corrected; time_barred_debt_note (1006.26(b) pinned; Midland Funding; state disclosure overlays; GLOSS on revival misrepresentation); discharged_debt_note (Walls / Simon / Randolph circuit split, GLOSS); repossession_breach_of_peace_note (UCC 9-609(b)(2) named); three c

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed True · material findings 3 (all dispositioned in round 46; see D)

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---

## 6. FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b

**Title:** A debt furnisher's duties after a consumer disputes credit-report information through a credit bureau  
**File:** `rules/debt/federal/fcra_furnisher_dispute_v1.json`  
**Band / tier at freeze:** 1 / DRAFT  
**node_sha256 (v1.0):** `0f84c2fa534603542990f735d67341a6370bcf4e7d66211a9a28d9fb1f09fdbd`

**Reading load:** logic 1,262 words · checklist 491 · cited text 1,960 · 9 citations · 10 checklist items · 6 drafting revisions

### A. Logic (read in full; this is the content being certified)

**trigger**

furnisher receives notice of a consumer dispute FORWARDED BY a consumer reporting agency (CRA) under § 1681i(a)(2) — this is distinct from a dispute sent directly to the furnisher (a separate duty under § 1681s-2(a)(8), not encoded in this node)

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**furnisher_duties_on_receiving_a_CRA-forwarded_dispute**

- investigate the disputed information
- review all relevant information the CRA provided
- report investigation results back to the CRA
- if inaccurate/incomplete: report that finding to every other nationwide CRA the furnisher furnished the information to
- if inaccurate, incomplete, or unverifiable after reinvestigation: modify, delete, or permanently block that item for CRA-reporting purposes

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**deadline**

tied to the CRA's own § 1681i(a)(1) reinvestigation period — this node does not itself state that period's length (commonly cited as 30 days, extendable to 45 in some circumstances, but NOT independently verified against primary text this session; flagged rather than asserted)

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**relationship_to_debt_collection**

relevant when a debt collector or the original creditor is also furnishing information to credit bureaus about the disputed debt — a consumer disputing a debt's validity with the COLLECTOR under FDCPA §1692g (see FDCPA-VALIDATION-NOTICE-1692g) is a related but legally separate track from disputing the same debt's appearance on a CREDIT REPORT under FCRA (this node) — both may need to happen.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**reasonableness_standard_note**

The statute's bare text ('investigate,' 'review all relevant information') does not itself say the investigation must be 'reasonable,' but courts have consistently read that requirement in. A furnisher that only re-checks its own internal records without examining supporting documents the consumer submitted (a 'data conformity' review) is generally NOT treated as having satisfied § 1681s-2(b) even though it technically 'investigated' and 'reported back' on time. This node's bare trigger/duties list, applied literally, would find such a furnisher compliant -- flagged here so that determination is not made without considering whether the investigation was substantive.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**practical_enforcement_note**

The direct-dispute route flagged elsewhere in this node ('a separate duty under § 1681s-2(a)(8), not encoded in this node') is NOT privately enforceable -- § 1681s-2(c)-(d) commits subsection (a) enforcement exclusively to federal/state regulators, unlike subsection (b), which does carry a private right of action. Practically, a consumer who wants a private FCRA remedy against a furnisher needs to dispute through a CRA (triggering subsection (b)), not directly with the furnisher alone.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**legal_vs_factual_dispute_note**

Some circuits have held a furnisher has no § 1681s-2(b) duty to resolve purely LEGAL disputes (e.g., whether a debt buyer legally owns the debt, or whether it is time-barred) as opposed to FACTUAL inaccuracies (e.g., wrong balance, wrong dates) -- only a court can finally resolve legal validity questions. Other, more recent circuit decisions have moved away from that legal/factual line toward an 'objectively and readily verifiable' test, under which even some legal-sounding disputes can trigger a duty if they are readily checkable. This is a genuinely unsettled, circuit-dependent question this node does not resolve -- flagged rather than asserted either way.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**accuracy_element_note**

A § 1681s-2(b) claim requires more than a poor-quality investigation -- the consumer must also show the furnished information was actually inaccurate or materially misleading. If the reported balance, dates, and status are accurate and the consumer's real objection is that the debt 'shouldn't be there' for equitable reasons (hardship, a dispute about whether it should have been charged at all), the claim fails at the accuracy element regardless of how cursory the furnisher's investigation was. This is one of the most common ways furnisher-dispute claims are dismissed, and this node's dispositive investigation-quality checklist item should not be read to mean a shoddy investigation alone establishes a violation.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**remedies_and_limitations_note**

Even where a § 1681s-2(b) violation is established, what the consumer recovers depends on the violation's culpability: negligent violations (§ 1681o) require proof of actual damages (economic or emotional-distress); only WILLFUL violations (§ 1681n) open the door to statutory damages ($100-$1,000) without proof of actual loss, plus possible punitive damages. Suit must be brought within 2 years of the consumer discovering the violation, or 5 years of the violation occurring, whichever is earlier (§ 1681p) -- this is an outside limit regardless of when discovered. A consumer with no quantifiable damages and a negligence-only theory, or one outside this window, should not be told she has a straightforwardly viable claim.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**cra_forwarding_trigger_note**

The dispositive trigger for this node is not merely that the consumer disputed an item with a CRA -- it is that the CRA forwarded that dispute to the furnisher as required by § 1681i(a)(2). A CRA may instead terminate a reinvestigation and never forward the dispute if it reasonably determines the dispute is frivolous or irrelevant under § 1681i(a)(3) (notifying the consumer of that determination) -- common with template or duplicate disputes, including those generated by credit-repair services. Where that happened, no § 1681s-2(b) furnisher duty ever arose, and this node should not be applied as though it did. QUALIFIED 2026-09-05 (round 46), from run_20260904T221748Z.json: the phrase 'common with template or duplicate disputes' must not be read as 'a second dispute is frivolous.' 1681i(a)(3)(A) lets a CRA terminate only on a REASONABLE determination that the dispute is frivolous or irrelevant, and the statute's own example is a failure to provide sufficient information -- a repeat dispute that supplies NEW material (bank statements, a paid-in-full letter, a police report) is not frivolous, the CRA must forward it, and the furnisher's 1681s-2(b) duty arises again on that new dispute. If the CRA nonetheless closed it, (a)(3)(B) requires written notice to the consumer within 5 business days stating the reasons; absence of that notice is evidence the CRA did forward or should have. Checklist item 1 reworded so a second dispute with new evidence is not screened out at the gate.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**cra_did_not_forward_documents_note**

ADDED 2026-09-03 (round 38): distinguish two failures that look alike from the consumer's side. (1) The CRA forwarded the consumer's documents and the furnisher ignored them -> furnisher liability under 1681s-2(b). (2) The CRA sent only a coded summary and never forwarded the documents (the ordinary e-OSCAR practice) -> the furnisher reviewed 'all relevant information provided by the CRA' and the failure is the CRA's under 1681i(a)(2). The checklist previously framed (2) as a furnisher violation. What the CRA actually transmitted is usually discoverable only from the furnisher's ACDV records.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**obsolescence_is_a_separate_claim_note**

ADDED 2026-09-03 (round 38): a dispute that the item is 'too old to be on my report' is NOT an accuracy dispute this node resolves as 'accurate reporting the consumer objects to for other reasons.' Reporting a collection or charge-off beyond the FCRA's obsolescence period (generally 7 years from the original delinquency, 15 U.S.C. 1681c(a)(4) and (c)(1)) is a distinct FCRA violation -- primarily the CRA's, and potentially the furnisher's if it reports a false date of first delinquency (1681s-2(a)(5)). Route this fact pattern to an obsolescence analysis rather than closing it as 'no claim.'

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

**identity_theft_block_note**

ADDED 2026-09-05 (round 46), from run_20260904T221748Z.json: when the consumer's position is 'this account is not mine -- someone opened it in my name,' route to the identity-theft BLOCK before, or alongside, the reinvestigation dispute. Under 15 U.S.C. 1681c-2(a) the CRA must block the information within 4 BUSINESS DAYS of receiving proof of identity, a copy of an identity theft report (an FTC IdentityTheft.gov report or a police report qualifies), identification of the item, and the consumer's statement that it does not relate to any transaction by her; under (b) the CRA must notify the furnisher, and under 1681s-2(a)(6)(B) a furnisher so notified may not re-furnish the blocked information. A CRA that ignores a proper block request faces its own 1681n/1681o liability -- the defendant is the CRA, not the furnisher, and the 30-day reinvestigation clock is beside the point. Checklist item added.

> Auditor: [ ] correct as stated  [ ] correct, wording change: ________  [ ] WRONG (note): ________

### B. Completeness checklist

1. THRESHOLD: is the consumer's claim that the account is NOT HERS AT ALL (identity theft)? If so, has she sent the CRA an identity-theft report with proof of identity and a statement that the item does not relate to any transaction by her (15 U.S.C. 1681c-2(a)) -- which obligates the CRA to BLOCK the item within 4 business days and notify the furnisher, a separate and faster remedy than the 30-day reinvestigation  (dispositive)  [ ] keep  [ ] change  [ ] drop
2. Whether the consumer disputed the item with a credit bureau (CRA) AND the CRA actually forwarded the dispute to the furnisher (1681i(a)(2)) -- including for a SECOND or later dispute that supplied new evidence, which a CRA may not treat as frivolous merely because it repeats an earlier one; if the CRA closed the dispute as frivolous, did it send the 5-business-day written notice required by 1681i(a)(3)(B)?  (dispositive)  [ ] keep  [ ] change  [ ] drop
3. Date the CRA notified the furnisher of the dispute  (dispositive)  [ ] keep  [ ] change  [ ] drop
4. Whether the furnisher reported back to the CRA within the applicable reinvestigation window (window length not encoded in this node — flagged gap)  (dispositive)  [ ] keep  [ ] change  [ ] drop
5. What the furnisher's investigation concluded, and whether it modified/deleted/blocked the item accordingly if inaccurate/incomplete/unverifiable  (dispositive)  [ ] keep  [ ] change  [ ] drop
6. Whether the furnisher's investigation went beyond checking its own internal records to actually reviewing ALL RELEVANT INFORMATION THE CRA FORWARDED with the dispute notice (1681s-2(b)(1)(B)) -- CORRECTED 2026-09-03 (round 38): the duty runs to what the CRA provided, not to documents the consumer sent the CRA that the CRA never passed along. If the consumer submitted documents and the furnisher received only a coded ACDV summary, the failure to forward is the CRA's under 1681i(a)(2)(A)-(B), and the consumer's claim against the furnisher on that theory is weak -- point at the right defendant  (dispositive)  [ ] keep  [ ] change  [ ] drop
7. Whether the consumer's dispute is a factual claim (wrong amount, wrong dates, mistaken identity) or a legal claim about the debt's validity/ownership/enforceability (e.g., statute of limitations, chain of title) -- courts differ, by circuit, on whether the latter triggers a furnisher duty at all  (dispositive)  [ ] keep  [ ] change  [ ] drop
8. Whether the information the furnisher reported was actually inaccurate, incomplete, or materially misleading -- as opposed to accurate reporting the consumer objects to for other (e.g. equitable or hardship) reasons, which does not support a § 1681s-2(b) claim regardless of investigation quality  (dispositive)  [ ] keep  [ ] change  [ ] drop
9. What damages (if any) the consumer actually suffered, and whether the violation was willful (opening statutory/punitive damages under § 1681n) or merely negligent (requiring proof of actual damages under § 1681o); and whether suit is being brought within 2 years of discovery / 5 years of the violation (§ 1681p)  (dispositive)  [ ] keep  [ ] change  [ ] drop
10. If the consumer's complaint is that the item is TOO OLD (not that its contents are wrong): what is the date of first delinquency the furnisher reported, and has 7 years passed? This is an obsolescence question (1681c / 1681s-2(a)(5)), not an accuracy dispute under this node  (dispositive)  [ ] keep  [ ] change  [ ] drop

### C. Citations (every derived_from entry: source tier, verification status)

| # | Cite | Tier | Verification | URL |
|---|---|---|---|---|
| 1 | 15 U.S.C. § 1681s-2(b)(1) | B | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/uscode/text/15/1681s-2 |
| 2 | 15 U.S.C. § 1681s-2(b)(2) | B | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/uscode/text/15/1681s-2 |
| 3 | 15 U.S.C. § 1681s-2(c), (d) | B | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/uscode/text/15/1681s-2 |
| 4 | Reasonable-investigation standard (judicial gloss on § 1681s-2(b)(1)(A)) | D | n/a (doctrine entry, no url by design) | — |
| 5 | 15 U.S.C. § 1681n(a); § 1681o(a); § 1681p | A | LIVE-VERIFIED (run_20260904T221748Z) | https://www.law.cornell.edu/uscode/text/15/1681n |
| 6 | 15 U.S.C. § 1681i(a)(1)(A), (a)(3)(A)-(B) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1681i&num=0&edition=prelim |
| 7 | 15 U.S.C. § 1681i(a)(2)(A)-(B) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1681i&num=0&edition=prelim |
| 8 | 15 U.S.C. § 1681c(a)(4), (c)(1) | A | LIVE-VERIFIED (run_20260904T221748Z) | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1681c&num=0&edition=prelim |
| 9 | 15 U.S.C. § 1681c-2(a) | A | ADDED AFTER last run (round 46) -- not yet live-checked | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1681c-2&num=0&edition=prelim |

> Auditor spot-check: for each MANUAL or 'added after last run' row, open the url and confirm the quoted_text (in the JSON file) appears verbatim. [ ] all spot-checks done

### D. Disposition history (Stage B findings on this node, oldest first)

| id | class | DD | theme | what changed |
|---|---|---|---|---|
| 01 | FIXED-VERIFIED | no (points at wrong defendant) | Furnisher faulted for not reviewing docs the CRA never forwarded (e-OSCAR) | 1681i(a)(2)(A)-(B) added (verified round 37 fetch); checklist reworded |
| 02 | FIXED-VERIFIED | yes | "Too old" dispute closed as no-claim; it's obsolescence (1681c) | Note + checklist |
| 03 | FIXED-VERIFIED | yes | Identity-theft block track (1681c-2) not offered | 1681c-2(a) pinned; identity_theft_block_note + threshold checklist |
| 04 | FIXED-VERIFIED | yes | Repeat dispute with new evidence screened out as 'frivolous' | cra_forwarding_trigger_note qualified per 1681i(a)(3); checklist item 1 reworded |

**Drafting revisions (author / date / summary):**

- 2026-08-30 — Added the enforcement-exclusivity caveat for the (a)(8) direct-dispute route (not privately enforceable), the reasonable-investigation judicial gloss (rejects mere records-parroting), and the legal-vs-factual dispute distinction (flagged as genuinely unsettled/circuit-dependent rather than asserted 
- 2026-08-30 — Added § 1681n/1681o/1681p remedies-and-limitations derived_from entry and § 1681i(a)(3) frivolous-dispute-termination derived_from entry; added accuracy_element_note, remedies_and_limitations_note, and cra_forwarding_trigger_note; tightened checklist item 1's CRA-forwarding trigger wording and added
- 2026-09-02 — Relabeled cite to (a)(1)(A)/(a)(3)(A)-(B), made post-ellipsis text verbatim, re-pinned to uscode.house.gov.
- 2026-09-03 — Added 1681i(a)(2)(A)-(B) (verified) and corrected checklist item on 'reviewing the consumer's documents' to track the actual duty ('all relevant information provided by the CRA'); added the CRA-did-not-forward note and an obsolescence-is-a-separate-claim note + checklist question. From the backlog's
- 2026-09-04 — Pinned 1681c(a)(4)/(c)(1); removed the SOURCE PENDING marker.
- 2026-09-05 — Round 46: 1681c-2(a) pinned + identity_theft_block_note + threshold checklist; cra_forwarding_trigger_note qualified per 1681i(a)(3)(A)-(B) + checklist item 1 reworded.

**Last full run (run_20260904T221748Z):** Stage A agreement True · citations all verified True · Stage B parsed True · material findings 3 (all dispositioned in round 46; see D)

### E. Sign-off

- [ ] Logic reviewed in full (section A)
- [ ] Checklist reviewed (B)
- [ ] Citations spot-checked per C
- [ ] Open counsel items for this node ruled (see DEBT_COUNSEL_QUEUE_V1.md)
- [ ] Open POST_V1_BACKLOG rows for this node reviewed (DD rows require an explicit decision)

**Tier decision:** [ ] remain DRAFT  [ ] CORROBORATED  [ ] VALIDATED   **Signed:** ______________  **Date:** __________

---
