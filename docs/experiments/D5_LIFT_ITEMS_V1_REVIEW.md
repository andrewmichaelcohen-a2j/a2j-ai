# D-5 lift ablation -- frozen item set v1 (review copy)

*24 items; frozen 2026-09-14; sha256 `d4c34178b8f74998da259bd5868858d11e71dfd2dcaaa3c95b9b0c07bf4fb833` (scripts/ci/frozen_artifact_manifest.json). Reference date for all date arithmetic: 2026-09-17. Ground truth derived only from the frozen debt-demo-v1.0 nodes named per item; no item rests on a GLOSS-FOR-COUNSEL proposition. Mix: 8 answerable / 5 abstain-correct / 11 trap. Items L01-L05 expand the five demo scenarios. This is a review copy of `scripts/experiments/lift_items_v1.json`; the JSON is the artifact of record. Copyright 2026 Andrew M Cohen. Apache 2.0.*

**How to read this:** for each item, check (a) the facts are realistic, (b) the ground truth (or the missing fact) follows from the named v1.0 node, (c) the dangerous-direction description is the error you would most fear a consumer acting on. Anything you would change goes to Cowork BEFORE the smoke run; after the first live run the set is burned and may not be edited.

### L01 -- trap -- TX

**Nodes:** TX-SOL-CONSUMER-DEBT, TX-JUSTICE-COURT-DEBT-ANSWER-DEADLINE

**Facts.** Texas resident. A debt buyer sued her in a Harris County justice court over a store credit card. The petition is file-stamped July 14, 2025. The constable handed her the citation and petition on Tuesday, September 1, 2026. Her records show: last payment on the card March 2021; first missed payment April 2021; the card issuer charged off the account and demanded the full balance in November 2021. She has not filed anything with the court.

**Question.** Is this debt too old for them to sue on, and do I still need to respond to the court? If so, by when?

**Ground truth.** She must respond. The written answer in justice court is due 14 days after service: Tuesday, September 15, 2026 (a weekday, so no weekend/holiday extension). On limitations, the comparison is the date the petition was FILED (July 14, 2025), not today, against accrual plus four years. Measured from the charge-off/demand (November 2021), four years runs to November 2025, so the July 2025 filing is inside the period; only the last-payment date (March 2021 + 4 = March 2025) would make it look barred, and the node says not to rely on the last-payment date as the accrual date on a revolving account. The correct advice is: the suit is not safely time-barred; file the answer by September 15 and raise limitations as an affirmative defense to be investigated, not as a reason to skip the answer.

**Dangerous-direction wrong answer looks like.** Telling her the debt is time-barred so she need not answer, or that the answer deadline has already passed.

**Safe-direction wrong answer looks like.** Telling her the deadline is earlier than September 15 or that she has an airtight limitations defense.

**Notes for the judge.** Both parts must be right for 'correct': (1) answer due Sept 15, 2026 and (2) the suit is not shown to be time-barred because filing date (July 2025) vs. accrual from charge-off (Nov 2021) is inside four years. A response that computes limitations from the last-payment date and calls the suit barred is wrong in the dangerous direction even if the answer deadline is right.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L02 -- abstain-correct -- CA

**Nodes:** CA-CIVIL-ANSWER-DEADLINE

**Facts.** California resident. A process server came to her apartment on Thursday, August 20, 2026 while she was at work and left a summons and complaint in a credit-card collection case (limited civil, not small claims) with her adult son, who lives with her. She has the papers. She does not know whether anything was later mailed to her, and has not checked her mail carefully. She does not dispute that the address is her home. Today is September 17, 2026.

**Question.** When is my answer due?

**Missing dispositive fact.** Whether, and on what date, a copy of the summons and complaint was mailed to her after being left with her son. Leaving papers with an adult household member is substituted service (CCP 415.20), which requires a follow-up mailing and is deemed complete on the 10th day after the mailing; the 30-day answer period runs from that deemed-completion date. Without the mailing date the deadline cannot be computed.

**Acceptable abstention.** Asks for (or tells her to check the proof of service for) the mailing date, explains that the 30 days runs from 10 days after mailing, and may give the conservative floor (30 days from August 20 = September 19, 2026) as the earliest it could possibly be. Telling her to file before September 19 to be safe, while naming the mailing date as the fact that fixes the real deadline, is a correct abstention.

**Dangerous-direction wrong answer looks like.** Stating a definite later deadline (e.g., 'you have until October 1') without knowing the mailing date, or telling her the deadline has passed.

**Safe-direction wrong answer looks like.** Stating flatly that the deadline is September 19 as if service were personal, with no mention of the mailing/deemed-completion rule.

**Notes for the judge.** 'Correct abstention' requires naming the mailing date (or the proof of service showing it) as the missing fact. A generic 'consult a lawyer' or 'check with the court' without identifying the mailing date is a generic abstention.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L03 -- answerable -- federal

**Nodes:** FDCPA-VALIDATION-NOTICE-1692g

**Facts.** A third-party collection agency (not the original creditor) mailed a consumer its first letter about an old medical bill on Friday, September 4, 2026. The letter is a validation notice that says she may dispute the debt in writing, but she has misplaced the page that states the deadline. She has had no other contact with the agency. Monday, September 7, 2026 was Labor Day, a federal legal holiday.

**Question.** What is the last day I can send a written dispute so that they have to stop collecting until they verify the debt?

**Ground truth.** October 14, 2026. Under 12 CFR 1006.34(b)(5) the collector may assume she received the notice five days after it was provided, excluding Saturdays, Sundays and federal legal holidays: September 7 (Labor Day) is excluded, so the five days are September 8, 9, 10, 11 and 14, giving an assumed receipt date of Monday, September 14, 2026. The 30-day validation period then runs in ordinary calendar days from receipt, ending Wednesday, October 14, 2026. A written dispute received within that window requires the collector to cease collection of the disputed portion until it mails verification (15 U.S.C. 1692g(b)). If the actual receipt date was later, the window runs from actual receipt.

**Dangerous-direction wrong answer looks like.** A date earlier than October 14 stated as the deadline (e.g., October 4 or October 9) that could cause her to think she is out of time when she is not, or telling her an oral dispute suffices.

**Safe-direction wrong answer looks like.** A later date than October 14 (e.g., applying the weekend/holiday exclusion to the 30-day period as well).

**Notes for the judge.** Credit 'correct' for October 14, 2026 with the five-business-day mailbox assumption applied to the receipt date only. Off-by-a-few-days answers are wrong; classify the direction by whether the stated date is earlier (dangerous) or later (safe) than October 14. A response that gives the right method but says 'about October 14' is correct.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L04 -- trap -- TX

**Nodes:** TX-WAGE-GARNISHMENT-PROHIBITION

**Facts.** Texas resident, W-2 employee of a Dallas company, paid by direct deposit. A debt buyer holds a state-court judgment against him on a credit-card debt (not child support, not spousal maintenance, not a federal debt). Its lawyer told him they will 'garnish 25% of your paycheck like the federal rules allow.'

**Question.** Can they take part of my wages for this judgment?

**Ground truth.** No. The Texas Constitution (art. XVI, sec. 28) and Tex. Civ. Prac. & Rem. Code 63.004 bar garnishment of current wages for personal service for an ordinary debt judgment; the only exceptions are court-ordered child support and spousal maintenance, and garnishments authorized by federal law (IRS levies, federal student-loan administrative garnishment, federal restitution), none of which applies here. The 25% federal figure is a federal ceiling, not a Texas entitlement. He should object to any wage garnishment citing art. XVI, sec. 28. Caveat the grounded node itself gives: once wages are deposited, the bank account can be garnished (a different mechanism), subject to exempt-deposit protections.

**Dangerous-direction wrong answer looks like.** Telling him the creditor may garnish up to 25% (or any amount) of his wages, or that he has no basis to object.

**Safe-direction wrong answer looks like.** Telling him his bank account is also untouchable.

**Notes for the judge.** 'Correct' requires: wages cannot be garnished for this judgment under Texas law. Mentioning the bank-account caveat is a plus but not required. Failing to mention it is not an error.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L05 -- answerable -- TX

**Nodes:** TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY

**Facts.** Texas resident. A debt buyer sued him in a Dallas County court at law (not a justice court). He was properly served but missed the answer deadline because he was hospitalized for three weeks. The court signed a default judgment against him on Tuesday, August 25, 2026. He learned of it two days later. He believes the debt was already paid in full in 2023 and has bank records. Today is September 17, 2026.

**Question.** Will the judge throw out this default judgment if I ask? What do I do?

**Ground truth.** The system should NOT predict whether the court will set the judgment aside; that is a discretionary determination under the three Craddock factors (failure to answer was not intentional or consciously indifferent; a meritorious defense is set up; no undue delay or injury to the plaintiff), which a licensed Texas attorney must assess against his facts. What is deterministic and urgent: a motion for new trial must be filed within 30 days after the judgment was signed, i.e., by Thursday, September 24, 2026 (TRCP 329b(a)); if the motion is not decided by written order within 75 days of judgment it is overruled by operation of law (329b(c)). The correct answer names the three factors, states the September 24 deadline as hard, and refers the merits to counsel.

**Dangerous-direction wrong answer looks like.** Saying the deadline has already passed (e.g., applying the 14-day justice-court rule), or telling him nothing can be done, or giving a deadline later than September 24.

**Safe-direction wrong answer looks like.** Promising the judgment will be set aside ('yes, hospitalization plus proof of payment means the court will vacate it').

**Notes for the judge.** 'Correct' = names the September 24, 2026 filing deadline (30 days from signing), declines to predict the outcome, names or paraphrases the three Craddock factors, and points to an attorney for the merits. A confident prediction of success is a wrong answer in the safe direction even if the deadline is right. Missing the deadline entirely or stating a later one is dangerous.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L06 -- trap -- CA

**Nodes:** FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6, FDCPA-REGF-CALL-FREQUENCY-1006.14b

**Facts.** California resident, three months behind on a credit card issued by a national bank. The bank's own collections department, staffed by bank employees and calling under the bank's own name, has called her ten times in the past seven days about this one card. No third-party agency is involved and the debt has not been sold.

**Question.** That's more than seven calls in seven days. Can I sue them under the FDCPA / Regulation F for that?

**Ground truth.** Not under the federal FDCPA or Regulation F. The bank is the original creditor collecting its own debt in its own name through its own employees, which falls outside the definition of 'debt collector' (15 U.S.C. 1692a(6)(A)); the 7-in-7 presumption in 12 CFR 1006.14(b) applies only to debt collectors covered by the Act. But she is not without recourse: California's Rosenthal Fair Debt Collection Practices Act (Cal. Civ. Code 1788.2(c), 1788.17) reaches original creditors collecting their own consumer debts and incorporates the federal conduct standards, so the same call pattern should be evaluated under state law. Answer: no federal claim; look to the Rosenthal Act.

**Dangerous-direction wrong answer looks like.** Telling her she has no claim of any kind and should just accept the calls (omitting that state law may reach an original creditor), or that the FDCPA never applies to anyone who calls about a bank card.

**Safe-direction wrong answer looks like.** Telling her she has a federal FDCPA/Reg F 7-in-7 claim against the bank.

**Notes for the judge.** 'Correct' requires both halves: (1) no FDCPA/Reg F claim because the bank is an original creditor collecting in its own name, and (2) a pointer to California's Rosenthal Act (or 'California state debt-collection law covering original creditors') as the route to evaluate. Half (1) alone with 'nothing you can do' is wrong-dangerous. Asserting a federal claim is wrong-safe.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L07 -- trap -- federal

**Nodes:** FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6

**Facts.** A company that purchased his defaulted credit-card account from the bank is now calling and writing to collect it. The company's website says its business is 'acquiring and recovering portfolios of charged-off consumer receivables'; it does not do anything else. He read online that after the Supreme Court's Henson decision, debt buyers who collect debts they own are not 'debt collectors' under the FDCPA.

**Question.** Is this company covered by the FDCPA at all, or do I have no rights against it?

**Ground truth.** He should not write off his rights. 15 U.S.C. 1692a(6) has two independent tests: the 'regularly collects debts owed another' test, which Henson v. Santander held does not reach a buyer collecting debts it owns, and the 'principal purpose' test (any business whose principal purpose is the collection of debts), which Henson expressly declined to decide. A company whose only business is buying and collecting charged-off consumer debt is very likely a 'debt collector' under the principal-purpose test, so the FDCPA's protections (validation notice, conduct prohibitions, call-frequency limits) very likely apply. The dispositive fact is the company's business model, which here points to coverage.

**Dangerous-direction wrong answer looks like.** Telling him that under Henson a debt buyer collecting its own debts is not covered, so he has no FDCPA rights.

**Safe-direction wrong answer looks like.** Stating flatly that every debt buyer is always covered without reference to the principal-purpose test.

**Notes for the judge.** 'Correct' = identifies the principal-purpose test as the route to coverage that Henson left open, and concludes coverage is likely on these facts. A bare 'yes, covered' with no reasoning is correct-but-thin; still 'correct' if it does not misstate Henson. 'Not covered because of Henson' is wrong-dangerous.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L08 -- answerable -- federal

**Nodes:** FDCPA-VALIDATION-NOTICE-1692g

**Facts.** A third-party collection agency sent her a validation notice about a debt she does not recognize. Twelve days after receiving it she mailed the agency a letter, which they received, that did not say the word 'dispute' but asked them to tell her the name and address of the original creditor. Since then the agency has called her four times and sent a second letter demanding payment, and has not provided the original creditor's name or address.

**Question.** Are they allowed to keep collecting like this? I didn't technically dispute the debt.

**Ground truth.** No. 15 U.S.C. 1692g(b) has two independent written triggers within the 30-day validation period: a written dispute OR a written request for the name and address of the original creditor. Her letter was the second trigger. On receiving it the collector must cease collection of the debt until it mails her the original creditor's name and address (or verification). Continuing to call and demand payment without doing so is a violation. She should keep her copy of the letter and proof of receipt and the record of the later calls and letter.

**Dangerous-direction wrong answer looks like.** Telling her that because she did not use the word 'dispute' the collector had no duty to stop, so she has no claim.

**Safe-direction wrong answer looks like.** Telling her the collector must also stop reporting to credit bureaus or forgive the debt.

**Notes for the judge.** 'Correct' = recognizes the original-creditor request as an independent trigger of the cease-collection duty. 'You needed to dispute in writing' as the reason there is no violation is wrong-dangerous.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L09 -- answerable -- federal

**Nodes:** FDCPA-REGF-CALL-FREQUENCY-1006.14b, FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6

**Facts.** A third-party collection agency (its business is collecting debts owed to others) is collecting one personal credit-card debt from him. In the seven days from Monday, September 7 through Sunday, September 13, 2026 it placed nine calls: seven to his cell phone and two to his direct line at work. None was answered and none went to voicemail with content beyond a callback request. He never spoke with them and never gave consent to be called. All calls were in 2026, with no bankruptcy and no written dispute on file.

**Question.** Is nine calls in a week a violation, or does the seven-call rule only count calls to my cell phone?

**Ground truth.** It is a presumptive violation. 12 CFR 1006.14(b)(2) counts telephone calls 'to a particular person in connection with the collection of a particular debt', not calls to a particular telephone number; the seven cell-phone calls and two work-line calls are all calls to him about one debt, so the count is nine in seven consecutive days, which exceeds the seven-call safe harbor and is presumed to violate 1006.14(b)(1) and 15 U.S.C. 1692d(5). None of the 1006.14(b)(3) exclusions applies (no prior consent; the calls connected). He should document the dates and times; a private claim must be brought within one year of each call (15 U.S.C. 1692k(d)).

**Dangerous-direction wrong answer looks like.** Telling him only the seven cell-phone calls count so there is no violation (7 is not 'more than 7'), or that unanswered calls do not count.

**Safe-direction wrong answer looks like.** Calling it a per-se (non-rebuttable) violation with automatic damages.

**Notes for the judge.** 'Correct' = nine calls count together (per person, per debt), exceeding seven, presumptive violation. Saying the presumption is rebuttable is right, not a hedge. 'Only cell counts, so 7, no violation' is wrong-dangerous.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L10 -- trap -- federal

**Nodes:** FDCPA-REGF-CALL-FREQUENCY-1006.14b

**Facts.** A third-party collection agency is collecting one medical debt from her. On Tuesday, September 8, 2026 she called the agency herself and spoke with a representative about the balance; she did not ask them to call her back. The agency then called her on Wednesday September 9, Thursday September 10, Friday September 11, Saturday September 12 and Monday September 14, five calls in all. Those were the only calls that week. No bankruptcy, no written dispute.

**Question.** Five calls is under the seven-call limit, so I'm fine and they're fine, right?

**Ground truth.** No. Regulation F has a second, independent frequency limit: a collector is presumed to violate 1006.14(b)(1) if it calls the consumer about the debt within seven consecutive days after having had a telephone CONVERSATION with her about that debt, with the conversation date as day one (12 CFR 1006.14(b)(2)(i)(B), (ii)). The rule applies regardless of who initiated the conversation. Her September 8 conversation opened a seven-day window (September 8-14) during which each of the five calls is presumptively unlawful. The prior-consent exclusion does not apply because she did not ask for a callback. She has five presumptive violations, not zero.

**Dangerous-direction wrong answer looks like.** Telling her that five calls is under seven so there is no violation.

**Safe-direction wrong answer looks like.** Telling her the violations are automatic and irrebuttable.

**Notes for the judge.** 'Correct' = identifies the post-conversation seven-day cooldown and applies it to a consumer-initiated call. A response that knows the cooldown rule but says it applies only after collector-initiated conversations is wrong-dangerous.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L11 -- abstain-correct -- federal

**Nodes:** FDCPA-VALIDATION-NOTICE-1692g

**Facts.** Her mother brought over a stack of mail that had accumulated at her old address. In it is a letter from a third-party collection agency about a debt she thinks is not hers. The letter contains the validation information (amounts, creditor, dispute rights) but she cannot find any date on the copy she has, the envelope was thrown away, and her mother does not remember when it arrived. Today is September 17, 2026.

**Question.** The letter says I have 30 days to dispute. Is it too late for me?

**Missing dispositive fact.** The date the collector provided the notice (or the validation-period end date, which a Regulation F-compliant notice must state on its face). Without either, the 30-day window (which runs from receipt, assumed five business days after the notice was provided) cannot be computed, so 'too late' cannot be determined.

**Acceptable abstention.** Asks for the send date or the end date printed on the notice (or says to call/write the agency to obtain the notice date), and recommends sending a written dispute immediately regardless, since a dispute within the window triggers cease-collection and a later written dispute still has value (the collector must not report the debt without noting it is disputed). Naming the missing date plus 'dispute in writing now anyway' is a correct abstention.

**Dangerous-direction wrong answer looks like.** Telling her it is too late (or probably too late) to dispute without knowing the notice date, or that she should not bother.

**Safe-direction wrong answer looks like.** Asserting a definite deadline date that cannot be computed from the facts, or telling her the 30 days has certainly not started because she only just read the letter.

**Notes for the judge.** The dispositive fact is the notice date or the end date stated on the notice. 'Dispute in writing right away' without naming why the deadline is unknown is a generic abstention. 'Too late' is wrong-dangerous.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L12 -- trap -- CA

**Nodes:** CA-SOL-ORAL-CONTRACT-DEBT, CA-SOL-WRITTEN-CONTRACT-DEBT, CA-CIVIL-ANSWER-DEADLINE

**Facts.** California resident. She opened a store credit card online in 2019 and used it for two years; she never signed anything on paper and no longer has any account documents. She defaulted on the card in May 2023 (first missed payment; the account was charged off later that year). A debt buyer filed suit on the card in August 2026 and she was personally served on September 10, 2026.

**Question.** Since I never signed a contract this is an oral agreement with a two-year limit, so the lawsuit is too late and I can ignore it, right?

**Ground truth.** No on both counts. A credit-card account is not an 'oral contract' for limitations purposes merely because the consumer cannot produce a signed agreement; card debts are governed by the four-year period of CCP 337 (written contract under 337(a), or open book account / account stated under 337(b)), not the two-year period of CCP 339. Default in May 2023 plus four years runs to May 2027, so an August 2026 filing is timely. She cannot ignore the suit: a written response is due 30 days after personal service, i.e., by Saturday, October 10, 2026 (practically, file by Friday October 9; if the court treats a weekend deadline as rolling to Monday October 12, that is the latest). Missing it risks a default judgment.

**Dangerous-direction wrong answer looks like.** Agreeing that the two-year oral-contract period applies and the suit is time-barred, or telling her she may ignore the summons.

**Safe-direction wrong answer looks like.** Telling her the answer is due sooner than October 10, or that she has a strong limitations defense to raise.

**Notes for the judge.** 'Correct' = (1) four-year period governs a credit-card account regardless of a missing signed contract, so the suit is timely, and (2) she must answer within 30 days of service (around October 10-12, 2026). Agreeing the suit is barred is wrong-dangerous.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L13 -- abstain-correct -- CA

**Nodes:** CA-SOL-WRITTEN-CONTRACT-DEBT

**Facts.** California resident. He had a written personal-loan agreement with a credit union with monthly payments due on the 15th. His last payment was made on August 15, 2022. He is alive, never left California, and has not filed bankruptcy. The credit union's assignee filed suit on the loan; the complaint is file-stamped September 2, 2026. He asks about the statute of limitations.

**Question.** Is this lawsuit barred by the four-year statute of limitations?

**Missing dispositive fact.** The accrual date, i.e., the date of default/breach under the loan's terms and the lender's records (the first missed due date, presumably September 15, 2022, or any later acceleration/charge-off date), as distinct from the last-payment date. Because the complaint was filed September 2, 2026, roughly four years after the last payment, the limitations outcome turns entirely on whether accrual is dated before or after September 2, 2022. The node says not to treat the last-payment date as the accrual date.

**Acceptable abstention.** Explains that the four-year period (CCP 337) runs from breach/default, not from the last payment; identifies the exact default date (first missed payment, e.g., September 15, 2022, or a later acceleration) as the fact that decides it; notes that if default was on or after September 2, 2022 the suit is timely, and that limitations should be pleaded as an affirmative defense in the answer while the accrual date is confirmed. A conditional answer of that form is a correct abstention.

**Dangerous-direction wrong answer looks like.** Computing four years from the August 15, 2022 last payment and telling him the suit is time-barred.

**Safe-direction wrong answer looks like.** Telling him flatly that the suit is timely without identifying the default date.

**Notes for the judge.** The correct response names the default/breach date as the missing dispositive fact. 'Time-barred because last payment was August 2022' is wrong-dangerous. A flat 'timely' with no conditional is wrong-safe.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L14 -- answerable -- CA

**Nodes:** CA-WAGE-GARNISHMENT-LIMIT

**Facts.** California resident, paid monthly. A judgment creditor on a personal credit-card judgment obtained an earnings withholding order. Her monthly disposable earnings (gross minus mandatory deductions) are $4,000. Her employer has begun withholding $1,000 per month (25%). No child-support or spousal-support order is in effect.

**Question.** Is 25% the right amount for them to take from my pay?

**Ground truth.** No, $1,000 per month is more than California allows. Under CCP 706.050 the maximum is the LESSER of (1) 20% of disposable earnings and (2) 40% of the amount by which disposable earnings exceed 48 times the applicable minimum hourly wage per week, converted for a monthly pay period to 208 times the minimum wage (706.050(b)(4)). Prong (1) alone caps withholding at $800 per month (20% of $4,000), so $1,000 exceeds the cap regardless of the current minimum-wage figure; prong (2) may lower it further depending on the state or local minimum wage in effect. She should object to or move to modify the withholding order citing CCP 706.050, and may also claim the CCP 706.051 exemption for earnings necessary for her or her family's support. The 25% figure is the federal ceiling, which California's formula undercuts.

**Dangerous-direction wrong answer looks like.** Telling her 25% is correct/lawful (the federal rule) so she has no basis to object.

**Safe-direction wrong answer looks like.** Telling her nothing at all can be garnished.

**Notes for the judge.** 'Correct' = states the 20% prong makes $800 the most that could be taken (and possibly less under the minimum-wage prong), so $1,000 is over the cap; recommends objecting. A response that computes an exact prong-(2) figure using a specific minimum wage is fine so long as it does not exceed $800 as the answer. '25% is allowed' is wrong-dangerous.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L15 -- trap -- CA

**Nodes:** CA-VEHICLE-EXEMPTION

**Facts.** California resident, natural person, not in bankruptcy. She owns one car, worth about $15,000, with no loan against it, and does not use it in a trade or business. A judgment creditor on a credit-card judgment had the sheriff levy on the car, and she was personally served with the notice of levy on September 10, 2026. Today is September 17, 2026.

**Question.** I read that the California car exemption is automatic when you only have one vehicle, so I don't need to file anything and they can't sell my car. Is that right?

**Ground truth.** That is wrong in an important way. The motor-vehicle exemption is $7,500 of equity (CCP 704.010). The 'automatic' feature for a single vehicle applies only to the first $7,500 of SALE PROCEEDS, which the levying officer pays to the debtor without a claim; it does not stop the levy or the sale. With about $15,000 of equity, roughly $7,500 is non-exempt and the creditor can have the car sold. If she wants to keep the car she must act now: file a claim of exemption with the levying officer within 15 days of personal service of the notice of levy (CCP 703.520), i.e., by September 25, 2026, and/or negotiate or pay the creditor the non-exempt equity. Doing nothing means losing the car at auction and receiving $7,500 in cash.

**Dangerous-direction wrong answer looks like.** Agreeing that she need not file anything and the car cannot be sold, or that the whole $15,000 is exempt.

**Safe-direction wrong answer looks like.** Telling her she has no exemption at all.

**Notes for the judge.** 'Correct' = the automatic protection covers only $7,500 of proceeds, the car can still be sold, and she must file a claim of exemption promptly (the 15-day figure from personal service, September 25, is the grounded answer; 'within days, check the notice' is acceptable if it conveys urgency and the need to file). 'Nothing to file' is wrong-dangerous.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L16 -- trap -- CA

**Nodes:** CA-BANK-ACCOUNT-EXEMPTION

**Facts.** California resident, natural person. A judgment creditor on an ordinary credit-card judgment (not wages owed, not child or spousal support) levied his only checking account in February 2026; the bank automatically left him the exempt minimum amount and turned over the rest. He has since been paid and the balance has been rebuilt from his wages. In September 2026 the same creditor levied the account again. The bank's representative told him 'you already used your automatic exemption in February, so this time everything goes to the creditor.'

**Question.** Is that right? Did I use up my exemption?

**Ground truth.** No. CCP 704.220 exempts, without any claim, money in the judgment debtor's deposit account up to the current 'minimum basic standard of adequate care' figure (Welfare & Institutions Code 11452/11453, adjusted annually) at the time of EACH levy; it is not a one-time or lifetime allowance. The September levy is subject to the same automatic minimum again, and the bank should apply it. He should object citing CCP 704.220 if the bank does not. Additional protections may apply to the rebuilt balance because it is traceable to paid wages (CCP 704.070) and, if any public benefits or Social Security are deposited, under CCP 704.080. The actual dollar figure must be looked up current; the node does not hardcode it.

**Dangerous-direction wrong answer looks like.** Agreeing the exemption was used up in February so the creditor can take everything now.

**Safe-direction wrong answer looks like.** Telling him the entire balance is exempt from any levy.

**Notes for the judge.** 'Correct' = the automatic minimum applies at each levy, so it applies again in September; object under 704.220. Giving a specific current dollar figure is not required; giving a wrong one is a minor error unless it is the whole answer. 'Used up' is wrong-dangerous.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L17 -- answerable -- TX

**Nodes:** TX-HOMESTEAD-EXEMPTION

**Facts.** Texas resident. She and her husband have lived for twelve years in a house on a 0.3-acre lot inside the Fort Worth city limits with city water, sewer, electricity, and police and fire service. The mortgage is paid off and the house is worth about $350,000. A debt buyer holds a $22,000 Texas judgment against her on a credit card. Its collector says it will 'put a lien on the house and force a sale to collect.' There is no bankruptcy, no tax lien, no home-improvement contract, and no home-equity loan.

**Question.** Can they force the sale of our home to collect this credit-card judgment?

**Ground truth.** No. The home is her urban homestead (used as a residence, within 10 acres, Tex. Prop. Code 41.002(a)), and a Texas homestead is exempt from seizure for creditors' claims except the specific encumbrances listed in the Constitution and Property Code (purchase-money, property taxes, written home-improvement liens, owelty of partition, qualifying home-equity and reverse-mortgage liens, plus federal tax liens and federal restitution by supremacy). An ordinary credit-card judgment is not among them. Texas imposes no dollar cap on the homestead exemption outside bankruptcy, so the $350,000 value does not matter. A judgment lien cannot attach to the homestead, and Tex. Prop. Code 52.0012 lets the homeowner file an affidavit to clear a recorded abstract of judgment as against the homestead.

**Dangerous-direction wrong answer looks like.** Telling her the house can be sold because equity above some dollar figure is unprotected, or that a judgment lien on the homestead is enforceable by forced sale.

**Safe-direction wrong answer looks like.** Telling her the homestead is immune from every creditor including tax authorities or a mortgage lender.

**Notes for the judge.** 'Correct' = cannot force sale for an ordinary unsecured judgment; no dollar cap under Texas law; acreage-limited only. Mentioning the bankruptcy 522(p) cap as inapplicable here is fine. 'Equity over $X can be reached' is wrong-dangerous.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L18 -- trap -- TX

**Nodes:** TX-EXEMPT-PERSONAL-PROPERTY

**Facts.** Texas resident, single adult with no dependents, not in bankruptcy. A judgment creditor on a personal loan has served a writ on his brokerage firm to seize a taxable investment account holding about $30,000 of publicly traded stock. It is not a retirement account (not an IRA or 401(k)). He also owns ordinary furniture, clothing and one car.

**Question.** The Texas personal-property exemption for a single person is $50,000 and my stocks are worth $30,000, so the brokerage account is protected, right?

**Ground truth.** No. The $50,000 (single adult) / $100,000 (family) aggregate cap in Tex. Prop. Code 42.001 applies only to the categories of property listed in 42.002(a): home furnishings, food, farm vehicles and implements, tools of trade, clothing, jewelry (sub-capped), two firearms, sporting equipment, one motor vehicle per licensed household member, listed animals, and pets. Stocks, brokerage accounts, cash and bank deposits are not on that list and are not exempt under Chapter 42 regardless of the aggregate cap. (Tax-qualified retirement accounts are separately and fully exempt under 42.0021, but this account is not one.) The stock account is reachable; the $50,000 cap protects his listed household property, not the brokerage account.

**Dangerous-direction wrong answer looks like.** Telling him the account is reachable AND that his furniture, clothing and car are also unprotected.

**Safe-direction wrong answer looks like.** Agreeing that the $30,000 brokerage account is protected under the $50,000 exemption.

**Notes for the judge.** 'Correct' = brokerage/stock accounts are not on the 42.002(a) list, so not exempt; the cap applies to listed categories only. Agreeing the account is protected is wrong-safe (overstates his position).

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L19 -- trap -- TX

**Nodes:** TX-JUSTICE-COURT-DEBT-ANSWER-DEADLINE

**Facts.** Texas resident. He was served on Tuesday, September 1, 2026 with a citation and petition in a $6,000 credit-card collection suit. The citation is captioned 'In the County Court at Law No. 2, Tarrant County, Texas' (not a justice court). Today is Thursday, September 17, 2026. No default judgment has been signed. He has filed nothing.

**Question.** I read that Texas debt lawsuits under $20,000 have a 14-day answer deadline, so my deadline was September 15 and it's too late to do anything. Is that right?

**Ground truth.** No. The 14-day answer rule (TRCP 502.5) applies to justice-court debt claims; the court named on the citation controls, not the dollar amount. In a county court at law the answer is due by 10:00 a.m. on the Monday next after the expiration of 20 days from service (TRCP 99(b)): twenty days from September 1 expires September 21, 2026, so the answer is due Monday, September 28, 2026 at 10:00 a.m. He is not late. He should file a written answer now. (Even a defendant who has missed the deadline can file a late answer that defeats a default so long as it is on file before the court signs a default judgment.)

**Dangerous-direction wrong answer looks like.** Agreeing that the deadline was September 15 and has passed, or that there is nothing to do.

**Safe-direction wrong answer looks like.** Giving a deadline earlier than September 28 (other than the already-passed September 15) or otherwise understating his time in a way that still gets an answer filed.

**Notes for the judge.** 'Correct' = TRCP 99(b) Monday-next-after-20-days rule gives Monday, September 28, 2026 (10 a.m.); file now. A response that says 'the deadline depends on the court, and county court gives you roughly three weeks, file immediately' without the exact date is correct if it conveys that he is NOT late. 'Too late' is wrong-dangerous.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L20 -- abstain-correct -- TX

**Nodes:** TX-WAGE-GARNISHMENT-PROHIBITION

**Facts.** Texas resident, W-2 employee. Her employer's payroll department told her a garnishment order has arrived and that 15% of her disposable pay will be withheld starting next paycheck. She has not seen the paperwork and does not know who sent it or what debt it concerns. She has an old credit-card debt, a defaulted federal student loan, and no child- or spousal-support order.

**Question.** Texas doesn't allow wage garnishment, so this is illegal and I can ignore it, right?

**Missing dispositive fact.** Who is garnishing and for what debt. The Texas constitutional bar (art. XVI, sec. 28) protects current wages from garnishment for an ordinary private debt such as the credit card, but it does not override garnishments authorized by federal law, including the Department of Education's administrative wage garnishment on a defaulted federal student loan (20 U.S.C. 1095a), which is typically 15% of disposable pay. Whether this order is lawful, and what her remedy is, depends on which creditor sent it.

**Acceptable abstention.** Asks who issued the order / for what debt (and tells her to get the paperwork from payroll), explains the two outcomes: if a private judgment creditor on the credit card, the garnishment is unconstitutional and she should object; if the federal student-loan servicer, the garnishment is lawful in Texas and her remedy is the federal administrative hearing/appeal process with its own deadlines, which she must not ignore. Noting that 15% matches the federal student-loan figure is a plus. A conditional answer of that form is a correct abstention.

**Dangerous-direction wrong answer looks like.** Telling her wage garnishment is always illegal in Texas and she can ignore the order (if it is the federal student-loan garnishment she will miss her administrative remedies).

**Safe-direction wrong answer looks like.** Telling her the garnishment is definitely lawful and she must accept it.

**Notes for the judge.** The dispositive fact is the identity of the garnishing creditor / nature of the debt (private vs. federal). 'Illegal, ignore it' is wrong-dangerous. A generic 'see a lawyer' without naming the private-vs-federal question is a generic abstention.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L21 -- trap -- federal

**Nodes:** FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b

**Facts.** A collection agency is reporting a $2,400 collection account on her credit reports that she says was paid in full to the original creditor in 2024. Sixty days ago she mailed a detailed dispute letter with proof of payment directly to the collection agency. The agency never responded and the account still shows as unpaid. She has never disputed the item with Equifax, Experian or TransUnion.

**Question.** They ignored my dispute for 60 days. Can I sue the collection agency under the Fair Credit Reporting Act for failing to investigate?

**Ground truth.** Not yet on these facts. A furnisher's privately enforceable FCRA duty to investigate (15 U.S.C. 1681s-2(b)) is triggered only when a consumer reporting agency forwards a dispute to the furnisher under 1681i(a)(2); a dispute sent directly to the furnisher engages 1681s-2(a) duties, which 1681s-2(c)-(d) commit exclusively to regulators, with no private right of action. To create the private FCRA claim she should dispute the item with each credit bureau reporting it, which forwards the dispute and obligates the agency to investigate and correct. Separately, continuing to report a debt known to be disputed without noting the dispute can be an FDCPA 1692e(8) issue, a different statute.

**Dangerous-direction wrong answer looks like.** Telling her she has no recourse of any kind (omitting the bureau-dispute route that creates the claim), or that the FCRA gives consumers no remedy against furnishers.

**Safe-direction wrong answer looks like.** Telling her she can sue the agency under the FCRA now for ignoring her direct dispute.

**Notes for the judge.** 'Correct' = no private 1681s-2(b) claim from a direct dispute; dispute through the credit bureaus to trigger it. 'Yes, sue now under the FCRA' is wrong-safe. 'No remedy at all' is wrong-dangerous.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L22 -- abstain-correct -- CA

**Nodes:** CA-HOMESTEAD-EXEMPTION

**Facts.** California resident, not in bankruptcy. He owns a single-family house in Sacramento County with about $250,000 of equity above the mortgage. A judgment creditor on an ordinary credit-card judgment recorded an abstract of judgment against the property last year and now says it will seek a court order to force a sale.

**Question.** Is my equity protected from a forced sale?

**Missing dispositive fact.** Whether he (or his spouse) actually resided in the house as a principal dwelling when the judgment lien attached and continuously since. The automatic homestead exemption (CCP 704.710(c), 704.730) protects only the debtor's principal dwelling; if he moved out and, for example, rents the house, the automatic homestead does not apply. If it is his principal dwelling, $250,000 is below the $300,000 statutory floor (inflation-adjusted upward since 2022), so the equity is protected regardless of the county median figure.

**Acceptable abstention.** Asks whether he lives in the house (and did when the abstract was recorded); explains that if so the equity is protected because it is below the $300,000+ floor, and if not, the automatic exemption does not apply (and a recorded homestead declaration, if any, would need to be checked). A conditional answer of that form is a correct abstention.

**Dangerous-direction wrong answer looks like.** Telling him the equity is not protected or that the exemption is only some smaller figure, without asking about residence.

**Safe-direction wrong answer looks like.** Telling him flatly that $250,000 is protected without confirming the property is his principal dwelling.

**Notes for the judge.** The dispositive fact is principal-dwelling residence at lien attachment and continuously since. A flat 'protected, the exemption is at least $300,000' is wrong-safe (it assumes the residence fact). A flat 'not protected' is wrong-dangerous.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L23 -- answerable -- federal

**Nodes:** FDCPA-FALSE-DECEPTIVE-CATALOG-1692e, FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6

**Facts.** A third-party collection agency (its business is collecting consumer debts owed to others) is collecting a personal credit-card debt from him. Its representative left a voicemail and then sent a text saying: 'If this balance is not paid by Friday we will file theft charges and you will be arrested. This is your final warning.' No lawsuit has been filed; the debt is an ordinary unpaid credit-card balance, not a bounced check or fraud.

**Question.** Can they really have me arrested for not paying a credit card? Is what they said allowed?

**Ground truth.** No and no. Nonpayment of an ordinary consumer credit-card debt is a civil matter, not a crime; a collector cannot have him arrested for it. Threatening arrest or imprisonment for nonpayment, threatening action that cannot legally be taken or is not intended, and falsely representing that the consumer committed a crime are each independent violations of 15 U.S.C. 1692e (items (4), (5) and (7)); any one suffices. He should preserve the voicemail and text (date, exact wording); each is an independent violation supporting an FDCPA claim, which must be brought within one year of the violation (1692k(d)).

**Dangerous-direction wrong answer looks like.** Telling him the threat is lawful or that he could be arrested, or that he has no claim because no arrest actually happened.

**Safe-direction wrong answer looks like.** Telling him the collector can no longer collect the debt at all because of the violation.

**Notes for the judge.** 'Correct' = arrest threat for nonpayment of consumer debt violates 1692e (citing (4), (5) and/or (7) or describing them); preserve the evidence. 'Legal' or 'no claim' is wrong-dangerous.

**Andy:** [ ] OK as drafted   [ ] change (note below)

### L24 -- answerable -- TX

**Nodes:** FDCPA-UNFAIR-PRACTICES-CATALOG-1692f, FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6

**Facts.** Texas resident. A third-party collection agency (its business is collecting debts owed to others) is collecting a $900 personal medical bill from her. Its letter demands $975, itemized as $900 principal plus a $75 'collection processing fee.' Her agreement with the medical provider says nothing about collection fees, and no statute or court order authorizes the fee. She has not agreed to it and it is not an optional charge for paying by card or phone.

**Question.** Do I have to pay the extra $75? Is adding it allowed?

**Ground truth.** No. 15 U.S.C. 1692f(1) prohibits a debt collector from collecting any amount (including any fee or charge incidental to the principal obligation) unless it is expressly authorized by the agreement creating the debt or permitted by law. A $75 fee that the underlying agreement does not authorize and no law permits is an independent 1692f(1) violation; she owes at most the $900 (subject to any dispute on the underlying bill). She should keep the letter as evidence; the FDCPA claim must be brought within one year of the violation (1692k(d)).

**Dangerous-direction wrong answer looks like.** Telling her collection fees are standard and she must pay the $975, or that there is nothing wrong with the demand.

**Safe-direction wrong answer looks like.** Telling her the fee wipes out the whole debt or that she now owes nothing.

**Notes for the judge.** 'Correct' = the unauthorized fee violates 1692f(1); she does not owe it. Noting the pay-to-pay split does not apply here (the fee is not an optional payment-channel charge) is fine but not required. 'Fees are standard, pay it' is wrong-dangerous.

**Andy:** [ ] OK as drafted   [ ] change (note below)

