# Debt-track Disagreement Queue

**Module:** Debt Defense Prototype (all states/federal) - **Layer:** grounded-corroboration + adversarial-generation
**Runner rule:** `scripts/corroboration/run_corroboration.py` appends new flagged items only. It never edits or
overwrites the Resolution, Resolved by, or Date fields -- those belong to Andy / the certifying attorney.
Built per DEBT_PROJECT_ARCHITECTURE_SPEC.md S3(d), generalizing Direction D-2 (`docs/DIRECTION_D_ROADMAP.md`) into
the debt track, per the 2026-08-26 Phase-A-Unblock direction item 6.

> **How to use this queue:** work top-to-bottom. Each entry has a candidate classification (rule gap / model error /
> citation-aggregator error) computed mechanically by the runner as a *hint*, not a determination -- the runner does
> not and cannot decide which side is legally correct. Fill in Resolution and Resolved-by, then move to Resolved.

---
## Open

### [TX-EXEMPT-PERSONAL-PROPERTY] ADVERSARIAL-GAP -- run run_20260830T111412Z, 2026-08-30T11:35:11Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': 'A single adult with a $180,000 401(k) rollover IRA and $30,000 of household goods and a paid-off truck asks whether creditors on a defaulted credit card judgment can reach his property. He is told his aggregate personal property must be valued against the $50,000 cap.', 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'exposes_gap': True, 'gap_description': "The encoding omits Tex. Prop. Code § 42.0021 (and Ins. Code § 1108.051), which exempt qualified retirement plans, IRAs, and life-insurance/annuity proceeds in unlimited amounts 'in addition to' the § 42.001 aggregate cap. Retirement accounts are among the largest and most commonly held assets of judgment debtors; treating them as inside (or outside the listed unlimited categories) would badly misstate exposure."}, {'scenario': 'A family with a $70,000 total of household goods, tools, and two paid-off cars also owns $35,000 in jewelry and a third and fourth vehicle (only two family members are licensed drivers). Aggregate net value is under $100,000, so they are told everything is exempt.', 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'exposes_gap': True, 'gap_description': 'The encoding captures only the aggregate dollar cap and ignores the item-category limits inside § 42.002(a): jewelry capped at 25% of the aggregate limit ($25,000/$12,500), two-wheeled/four-wheeled vehicles limited to one per licensed family member (or per member relying on another to drive), two firearms, and numeric livestock/fowl limits. A debtor under the dollar cap can still have non-exempt property, so the answer is affirmatively wrong.'}, {'scenario': 'A single adult who owes $60,000 in back federal income taxes and has an IRS notice of levy on his paid-off vehicle and tools of trade asks whether the Texas personal-property exemption protects them; his total listed property is $28,000 net of liens.', 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'exposes_gap': True, 'gap_description': "The encoding's only override is voluntary liens/security interests. It omits that Texas exemptions do not defeat federal tax liens/levies (26 U.S.C. §§ 6321, 6334) and, under § 42.005, do not apply to child-support liens or (per § 42.004) property acquired via fraudulent transfer. Telling an IRS or child-support debtor the property is exempt is materially wrong for a common creditor type."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under Tex. Prop. Code § 42.001(a), the personal property listed in § 42.002 is exempt from garnishment, attachment, execution, or other seizure up to an aggregate fair market value of $100,000 for property provided for a family, or $50,000 for a single adult who is not a family member, in each case excluding liens, security interests, or other encumbrances. Section 42.002(a) identifies the covered categories, including home furnishings and heirlooms, food provisions, farm/ranch vehicles and implements, trade tools and equipment (including boats and motor vehicles used in a trade or profession), clothing, jewelry (capped at 25% of the aggregate limit), two firearms, athletic and sporting equipment, one motor vehicle per licensed family member or single adult (or a non-licensed person who relies on another to drive), specified numbers of livestock and fowl with forage, and household pets. Section 42.001(b) exempts certain property entirely outside the dollar caps: current wages for personal services (except for court-ordered child support enforcement), professionally prescribed health aids, alimony/support/separate maintenance, and a religious bible or sacred-writings book (except when seized by a landlord exercising rights after a lease breach or abandonment).'
  - gpt-5.5: grounded=True, error=None, summary='Texas exempts certain personal property from garnishment, attachment, execution, or other seizure if it is property described in Section 42.002 and its aggregate fair market value does not exceed $100,000 for a family or $50,000 for a single adult who is not a family member, excluding liens and other charges. Some property—such as current wages, prescribed health aids, support payments, and certain sacred writings—is exempt from seizure and does not count toward those aggregate limits. Section 42.002 lists exempt categories including home furnishings, provisions, work tools and vehicles, apparel, limited jewelry, firearms, sporting equipment, certain motor vehicles, specified livestock, and household pets.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Texas, certain personal property is exempt from seizure by creditors up to an aggregate fair market value of $100,000 for a family or $50,000 for a single adult, exclusive of any liens. The types of property subject to this limit include home furnishings, tools of a trade, motor vehicles, and certain animals. Additionally, some property like current wages, professionally prescribed health aids, and alimony is completely exempt from seizure and does not count toward these aggregate value limits.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-HOMESTEAD-EXEMPTION] ADVERSARIAL-GAP -- run run_20260830T111412Z, 2026-08-30T11:34:09Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': 'A family relocated from California to Texas 18 months ago, bought a $900,000 Dallas home with the equity from their prior residence, and now files Chapter 7 after a business failure. They ask whether creditors can reach the house.', 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'gap_description': "The rule flatly states there is 'no dollar-value cap.' In bankruptcy, 11 U.S.C. § 522(p) caps the homestead exemption (roughly $190K–$215K, adjusted triennially) for equity in property acquired within 1,215 days before filing, and § 522(o) reduces it for equity from converted nonexempt assets. Texas's massive in-migration makes recent-purchase debtors extremely common; telling such a debtor the exemption is uncapped is materially wrong and could cost hundreds of thousands in equity.", 'exposes_gap': True}, {'scenario': 'A homeowner owes $150,000 in unpaid federal income taxes and receives a Notice of Intent to Levy; the IRS threatens to seek judicial sale of the residence. Separately, a client asks about a federal criminal restitution order entered against him.', 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'gap_description': "The exception list includes only 'property tax liens,' implying ad valorem taxes. Federal tax liens under 26 U.S.C. § 6321 and federal restitution/forfeiture claims override state homestead exemptions by supremacy (United States v. Rodgers). IRS debt is very common; the encoded rule would tell such a person their homestead is protected when it is not.", 'exposes_gap': True}, {'scenario': "A homeowner in a subdivision falls behind $6,000 on HOA assessments; the association posts the home for a nonjudicial foreclosure sale under the recorded declaration's assessment lien. The owner asks whether the homestead exemption blocks the sale.", 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'gap_description': "HOA assessment liens created by restrictive covenants recorded before the homestead attached are enforceable against a Texas homestead (Inwood N. Homeowners' Ass'n v. Harris), as are pre-existing consensual liens generally. The exception list omits this entirely, so the rule would tell a Texas HOA member facing foreclosure that the home is exempt — a wrong and potentially home-losing answer, and HOA foreclosures are a frequent occurrence in Texas.", 'exposes_gap': True}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Tex. Prop. Code § 41.001(a), a homestead — plus one or more lots used as a burial place — is exempt from seizure to satisfy creditors' claims, with the sole stated exception being encumbrances properly fixed on the homestead property. Section 41.002 sets the size limits of the protected homestead: an urban homestead (for a family or a single adult) may be up to 10 acres in one or more contiguous lots, together with improvements. A rural homestead may be up to 200 acres for a family, or up to 100 acres for a single adult person. The text does not address other matters, such as value caps or the procedure for asserting the exemption."
  - gpt-5.5: grounded=True, error=None, summary='A Texas homestead is exempt from seizure for creditor claims, except for encumbrances properly fixed on the homestead property. The protected homestead is limited to not more than 10 acres for an urban home, not more than 200 acres for a rural family homestead, and not more than 100 acres for a rural homestead of a single adult person.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Texas, a homestead and burial lots are generally exempt from seizure by creditors, except for encumbrances properly fixed on the property. The size of the protected homestead depends on its location. An urban homestead can be up to 10 acres, while a rural homestead can be up to 200 acres for a family or 100 acres for a single adult.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-BANK-ACCOUNT-EXEMPTION] ADVERSARIAL-GAP -- run run_20260830T111412Z, 2026-08-30T11:27:22Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': "A retiree's only bank account receives direct-deposited Social Security and SSI benefits, and a credit card judgment creditor levies the account holding about $6,000. The debtor asks how much of the account is safe.", 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'exposes_gap': True, 'gap_description': 'The rule encodes only the CCP §704.220 automatic minimum exemption and would tell the debtor that only the (roughly $2,000) W&IC §11452 figure is automatically protected. CCP §704.080 automatically exempts a far larger amount of directly deposited public benefits/Social Security ($5,250 for one depositor, $7,875 for two or more, and potentially the full traced amount), and federal law independently protects two months of directly deposited benefits. The encoded answer materially understates the protection for a very common fact pattern.'}, {'scenario': 'A debtor holds a checking account with $1,800 and a savings account with $1,500 at two different banks; a judgment creditor levies both simultaneously.', 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'exposes_gap': True, 'gap_description': "The checklist expressly flags CCP §704.220's aggregation/allocation rules as 'not separately encoded' and marks the multiple-account fact as non-dispositive. It is dispositive: the minimum exemption is a single aggregate amount across all accounts, not per account. As encoded the rule would suggest each account is separately protected up to the figure, roughly doubling the protection the debtor actually has — a materially wrong answer in a very ordinary multi-account situation."}, {'scenario': "A small business owner is served with a bank levy on the LLC's operating account, which holds $2,500, to satisfy a judgment entered against the LLC on an unpaid vendor contract.", 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'exposes_gap': True, 'gap_description': "The rule never conditions the automatic exemption on the judgment debtor being a natural person. Under CCP §703.020 the exemptions (including §704.220) are available only to natural persons, so no part of the entity's account is exempt. As encoded, the rule would wrongly tell an entity debtor that a minimum balance is automatically protected from levy."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.220(a), money in a judgment debtor's deposit account is automatically exempt — with no need to file an exemption claim — up to an amount equal to the minimum basic standard of adequate care for a family of four for Region 1, as set by Welfare and Institutions Code § 11452 and annually adjusted by the State Department of Social Services under § 11453. The statute does not state a fixed dollar figure; the amount is whatever that adjusted standard is. Per § 704.220(c)(1), this automatic exemption does not apply when the levy is to satisfy a judgment for wages owed (including damages and penalties), child support, or spousal support."
  - gpt-5.5: grounded=True, error=None, summary='California exempts, without the debtor making a claim, money in a judgment debtor’s deposit account up to the amount equal to the minimum basic standard of adequate care for a family of four for Region 1, as established and annually adjusted under the cited Welfare and Institutions Code provisions. This automatic exemption does not apply when the levy is to satisfy a judgment for wages owed, child support, or spousal support; “wages owed” includes damages and penalties.'
  - gemini-2.5-pro: grounded=True, error=None, summary="An amount of money in a judgment debtor's deposit account is automatically exempt from collection without the debtor needing to file a claim. This exempt amount is equal to or less than the minimum basic standard of adequate care for a family of four, as determined annually by the State Department of Social Services. However, this exemption does not apply if the money is being levied to satisfy a judgment for owed wages, child support, or spousal support."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-VEHICLE-EXEMPTION] ADVERSARIAL-GAP -- run run_20260830T111412Z, 2026-08-30T11:26:20Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': "A self-employed drywall contractor's work pickup (worth about $18,000, owned free and clear) is levied on by a judgment creditor. He uses the truck exclusively to haul tools and materials to job sites, and he also owns an old sedan he drives personally.", 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'exposes_gap': True, 'gap_description': "The encoding ignores CCP § 704.060 (tools of trade), under which a motor vehicle reasonably necessary to and actually used in the debtor's trade can be claimed at the higher tools-of-trade amount (and the § 704.010 vehicle exemption can apply to a separate personal vehicle). Telling this debtor only $7,500 of the truck's equity is protected materially understates his protection and could lead him not to claim the correct exemption."}, {'scenario': 'A debtor filing a Chapter 7 bankruptcy owns one car with $12,000 of equity and no homestead (she rents). She asks how much of the car is protected from the trustee/creditors.', 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'exposes_gap': True, 'gap_description': 'The checklist and logic cover only the § 704 series and omit the alternative bankruptcy-only exemption set in CCP § 703.140(b), where a renter can combine the (b)(2) vehicle exemption with the large (b)(5) wildcard (unused homestead) to shield far more than $7,500 of vehicle equity. The rule would wrongly tell her roughly $4,500 of equity is reachable.'}, {'scenario': "A debtor's only car was totaled and the insurer paid a $9,000 settlement, which he deposited in his checking account. Five months later a judgment creditor levies the account; he claims the funds are exempt as vehicle insurance proceeds.", 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'exposes_gap': True, 'gap_description': 'CCP § 704.010(b) exempts execution-sale and insurance/indemnification proceeds only for 90 days after receipt. The encoding states the exemption applies to such proceeds with no time limit and the checklist never asks when the proceeds were received, so it would wrongly advise that $7,500 of long-since-received proceeds is protected.'}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.010(a), a judgment debtor may exempt up to $7,500 in any combination of the aggregate equity in motor vehicles, the proceeds of an execution sale of a motor vehicle, and insurance or other indemnification proceeds for a motor vehicle's loss, damage, or destruction. Subdivision (d) adds that if the debtor owns only one motor vehicle and it is sold at an execution sale, $7,500 of the sale proceeds is exempt automatically, without the debtor having to file a claim; the levying officer may rely on DMV records to confirm the debtor has only one vehicle. In that single-vehicle situation, the subdivision (a) exemption is not additionally available."
  - gpt-5.5: grounded=True, error=None, summary='California exempts up to $7,500 in any combination of aggregate equity in motor vehicles, proceeds from an execution sale of a motor vehicle, and insurance or indemnification proceeds for loss, damage, or destruction of a motor vehicle. If the judgment debtor has only one motor vehicle and it is sold at an execution sale, $7,500 of the sale proceeds is exempt without making a claim, and the subdivision (a) exemption is not available in that situation.'
  - gemini-2.5-pro: grounded=True, error=None, summary='Under California law, a judgment debtor has a motor vehicle exemption of seven thousand five hundred dollars ($7,500). This exemption applies to the combined equity in motor vehicles, the proceeds from an execution sale, or insurance proceeds for loss or damage. If a debtor has only one motor vehicle that is sold at an execution sale, the $7,500 exemption for the proceeds is automatic and does not require a claim to be made.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-ORAL-CONTRACT-DEBT] ADVERSARIAL-GAP -- run run_20260830T111412Z, 2026-08-30T11:22:54Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': "A consumer is sued by a debt buyer over an old store credit card / revolving retail account. She never signed anything she can find, so she answers 'no written contract' and the node returns a 2-year period; her last payment was 3 years ago and she concludes the suit is time-barred.", 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'exposes_gap': True, 'gap_description': "Credit card and revolving retail accounts are the single most common CA consumer-debt scenario, and they are almost always governed by the 4-year period (CCP 337(a) written contract or 337(b)/(2) open book account), not the 2-year oral period of CCP 339. The node has no rule for book accounts or accounts stated at all -- it offers only a written/oral binary and punts the classification to a 'threshold fact question,' so a user with a card account who lacks a signed agreement will be routed to the wrong 2-year answer and may wrongly forgo defending or wrongly assert an SOL defense."}, {'scenario': 'Debtor defaulted on a verbal loan in 2021, then moved to Nevada for two years before returning to California; the creditor sues in 2024, more than two years after the last payment.', 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'exposes_gap': True, 'gap_description': "CCP 351 tolls the limitations period while the defendant is absent from California, and other tolling/suspension rules (bankruptcy stay under 11 U.S.C. 362/108, COVID Emergency Rule 9) can also apply. The node encodes no tolling and its checklist does not even ask whether the debtor left the state or filed bankruptcy, so it will confidently report 'expired' on a claim that is in fact timely."}, {'scenario': "A consumer is served in month 26 after default with a collection complaint that was actually filed in month 22. Using today's date, the node computes accrual + 2 years < today and reports the claim as time-barred.", 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'exposes_gap': True, 'gap_description': "The determination compares 'today' to accrual + 2 years, but the operative date under CCP 350 is the date the action was commenced (filed), not the current date; service commonly lags filing by weeks or months, and consumers first learn of the suit at service. Neither the logic nor the checklist captures the complaint's filing date, so a timely-filed suit can be misreported as expired -- the exact error most likely to cause a defendant to default or to plead a losing defense."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under Cal. Code Civ. Proc. § 339(1), a lawsuit on a contract, obligation, or liability that is not founded upon a written instrument — such as an oral or otherwise unwritten consumer debt — must be brought within two years. The statute carves out exceptions for actions governed by Commercial Code section 2725 and Code of Civil Procedure section 337(2). The same two-year period also applies to claims evidenced by a certificate, abstract, or guaranty of title to real property or a title insurance policy, though those claims do not accrue until the aggrieved party discovers the loss or damage.'
  - gpt-5.5: grounded=True, error=None, summary='An action upon a contract, obligation, or liability that is not founded upon a written instrument must be brought within two years, subject to the exceptions stated in the statute. The excerpt does not provide a separate rule specific to consumer debt, but it does state the limitations period for an unwritten/oral contract action.'
  - gemini-2.5-pro: grounded=True, error=None, summary='The statute of limitations is two years for an action upon a contract, obligation, or liability that is not founded upon an instrument of writing. The provided text establishes this two-year period as the general rule for unwritten contracts. The text also notes that exceptions exist in other code sections, but does not provide the content of those exceptions.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-WRITTEN-CONTRACT-DEBT] ADVERSARIAL-GAP -- run run_20260830T111412Z, 2026-08-30T11:21:53Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': 'A debt buyer sues a California resident on a Chase or Citibank credit-card account whose cardmember agreement contains a Delaware (3-year) or other out-of-state choice-of-law clause, and the account was opened and charged off while the consumer lived out of state. Default was 3.5 years ago.', 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'gap_description': "The node applies a flat 4-year period and never asks about the contract's choice-of-law clause or CCP § 361 (California's borrowing statute). Nearly every major card agreement designates Delaware, South Dakota, Utah, Virginia, etc., and California courts routinely enforce those clauses or borrow the shorter foreign period for claims arising elsewhere. A consumer with a 3-year-stale Delaware-law account would be told the claim is timely and that no defense exists, when a valid and dispositive SOL defense is available.", 'exposes_gap': True}, {'scenario': "A consumer's car is repossessed and sold at auction; the lender sues 4.5 years after the consumer's last payment but only 3 years after the post-sale deficiency notice, seeking the deficiency balance on the signed retail installment contract.", 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'gap_description': "The node encodes accrual as 'date of default/breach or last payment,' but for a secured installment contract the deficiency cause of action accrues on the disposition/deficiency date (and installment obligations can accrue installment-by-installment absent acceleration). Applied literally, the node tells the consumer the suit is time-barred and that the creditor was statutorily barred from even filing, when the claim is actually timely — a wrong answer that could lead to a default judgment.", 'exposes_gap': True}, {'scenario': 'A collector calls a consumer about a credit-card charge-off from 6 years ago and persuades him to make a single $25 debit-card payment; the collector then sues, and the consumer wants to know if the SOL defense is gone.', 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'gap_description': "The node's accrual rule keys off 'date of last payment' without distinguishing a payment made before the period ran (which can restart it) from a payment made after the debt was already time-barred. Under CCP § 360 a barred obligation is not revived absent a signed written acknowledgment or new promise, and § 337(d)'s bar on initiating suit had already attached. Applied as written, the node computes four years from the $25 payment and tells the consumer the claim is timely, destroying a complete defense in a scenario collectors deliberately engineer.", 'exposes_gap': True}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 337(a), an action on any contract, obligation, or liability founded upon a written instrument must be brought within four years (subject to the exception in Section 336a, and a special three-month limit for deficiency-type money judgments after a trustee's sale under a deed of trust or mortgage with power of sale). Section 337(d) adds that once that four-year period has run, a person may not bring suit or initiate arbitration or other legal proceedings to collect the debt. The limitations period can be extended only as provided in Section 360."
  - gpt-5.5: grounded=True, error=None, summary='An action founded on a written contract, obligation, or liability must be brought within four years. After that period has run, a person may not bring a lawsuit, arbitration, or other legal proceeding to collect the debt, and the period can be extended only as provided in Section 360.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-WRITTEN-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260830T111412Z, 2026-08-30T11:21:53Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['3', '4'], OpenAI=['4'], Gemini=[] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 337(a), an action on any contract, obligation, or liability founded upon a written instrument must be brought within four years (subject to the exception in Section 336a, and a special three-month limit for deficiency-type money judgments after a trustee's sale under a deed of trust or mortgage with power of sale). Section 337(d) adds that once that four-year period has run, a person may not bring suit or initiate arbitration or other legal proceedings to collect the debt. The limitations period can be extended only as provided in Section 360."
  - gpt-5.5: grounded=True, error=None, summary='An action founded on a written contract, obligation, or liability must be brought within four years. After that period has run, a person may not bring a lawsuit, arbitration, or other legal proceeding to collect the debt, and the period can be extended only as provided in Section 360.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] MODEL-DISAGREEMENT -- run run_20260830T111412Z, 2026-08-30T11:20:17Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['30', '5'], OpenAI=['30', '5'], Gemini=['30'] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="A notice is compliant only if the debt collector, in the initial communication or within five days after it (12 C.F.R. § 1006.34(a)(1); 15 U.S.C. § 1692g(a)), gave the consumer all required content: the amount of the debt, the name of the creditor, the statement that the debt is assumed valid unless disputed within 30 days of receipt, the written-dispute/verification statement, and the original-creditor-request statement — plus, under Reg F, the collector communication disclosure, the itemized debt information, the consumer-protection information including the dispute-window end date, and the consumer-response prompts and addresses (12 C.F.R. § 1006.34(c)). If any of those elements is missing or the notice was late, the notice is not compliant. On timing, the dispute window (the 'validation period') runs from the date the validation information is provided until 30 days after the consumer receives or is assumed to receive it, and the collector may assume receipt on any date at least five business days (excluding Saturdays, Sundays, and legal public holidays) after it provided the notice (12 C.F.R. § 1006.34(b)(5)). So the consumer is still within the window if today's date falls on or before that 30-day end date; a written dispute or original-creditor request sent within it requires the collector to cease collection until verification or the creditor's name and address is mailed (15 U.S.C. § 1692g(b)). The provided text supplies the standard, but the actual dates of the initial communication and notice are needed to fix the exact window."
  - gpt-5.5: grounded=False, error=None, summary='The text states that a debt collector must provide required validation information in the initial communication, within five days after it, or orally in the initial communication. A compliant notice must include the listed debt, creditor, consumer-protection, dispute, verification, original-creditor, and response information; the validation period runs from when that information is provided until 30 days after the consumer receives or is assumed to receive it. However, the source text provides no facts about what notice was actually given, when it was given, or when the consumer received it, so it is not possible to determine whether a compliant notice was provided or whether the consumer remains within the dispute window.'
  - gemini-2.5-pro: grounded=False, error=None, summary="The provided legal texts describe the required contents of a debt validation notice and establish a 30-day dispute window that begins upon the consumer's receipt of the notice. However, these texts do not contain any specific facts about a notice that was actually sent or received. Therefore, it is impossible to determine from the text alone whether a compliant notice was provided or if the consumer is still within their dispute window."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] ADVERSARIAL-GAP -- run run_20260830T111412Z, 2026-08-30T11:17:54Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': 'A consumer bounced a check and the collector\'s letter states: "You have committed check fraud, a criminal offense, and we will report your criminal conduct to your employer and neighbors." The consumer wants to know if this violates §1692e.', 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'exposes_gap': True, 'gap_description': "The catalog claims to encode 16 items but omits §1692e(6) (false implication that transfer/sale of the debt will cause loss of claims or defenses) and §1692e(7) (falsely representing or implying that the consumer committed a crime or other conduct in order to disgrace the consumer). A crime-accusation/disgrace fact pattern is the paradigm (7) case and is common in bounced-check and 'fraud' collection scripts; the encoded catalog forces it into the (10) catch-all or misses it entirely, understating or mis-citing the violation."}, {'scenario': "A small-business owner is contacted by the in-house collections department of the bank that originally extended a commercial line of credit; the department uses the name 'Asset Recovery Group' and never gives a mini-Miranda disclosure.", 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'exposes_gap': True, 'gap_description': "Neither the logic nor the checklist requires any threshold facts about whether the entity is a 'debt collector' under §1692a(6) (original creditors collecting their own debts in their own name are generally excluded) or whether the obligation is a consumer debt for personal, family, or household purposes under §1692a(5). Applied as encoded, the node would find independent (11) and (14) violations for a commercial debt collected by an exempt original creditor, telling the user they have an FDCPA claim when the statute does not apply at all."}, {'scenario': 'A collection law firm files a summons and complaint in state court to collect a credit card debt; the pleadings themselves contain no statement that the communication is from a debt collector, and the consumer asks whether that is a §1692e(11) violation.', 'realistic_and_common': True, 'would_cause_wrong_answer': True, 'exposes_gap': True, 'gap_description': "§1692e(11) expressly exempts 'a formal pleading made in connection with a legal action,' and Reg F §1006.18(e)(3) carries the exception forward. The checklist's dispositive item ('whether the collector disclosed in EACH subsequent communication that it was a debt collector') contains no pleading carve-out, so the node would report a violation where none exists — a common scenario since most consumers encountering collectors in litigation receive pleadings without mini-Miranda language."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means to collect a debt, and then lists specific violations without limiting that general ban: falsely claiming government affiliation or bonding; misstating the character, amount, or legal status of a debt or of services/compensation; falsely implying attorney involvement; threatening arrest, imprisonment, seizure, garnishment, attachment, or sale of property or wages when such action is unlawful or not intended; threatening any action that cannot legally be taken or is not intended; communicating credit information known to be false, including failing to note a debt is disputed; simulating court or agency documents; using false or deceptive means to collect or obtain consumer information; failing to give the required debt-collector disclosures; falsely claiming accounts were sold to innocent purchasers; misrepresenting whether documents are legal process or require consumer action; using a name other than the collector's true name; and falsely implying the collector is a consumer reporting agency. The 'mini-Miranda' duty in § 1692e(11) is now implemented by Regulation F, 12 C.F.R. § 1006.18(e): the initial communication must state the collector is attempting to collect a debt and that information obtained will be used for that purpose (repeated in the first written communication if the first contact was oral), each subsequent communication must disclose it is from a debt collector, and no disclosure is required in a formal pleading in a legal action."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use any false, deceptive, or misleading representation or means in connection with collecting a debt. The statute lists prohibited conduct including falsely implying government affiliation, misrepresenting the debt’s character/amount/legal status, implying communications are from an attorney, threatening unlawful or unintended action, reporting known false credit information, using fake court/agency documents, using deceptive means to collect, misusing business names, and misrepresenting legal process or consumer-reporting-agency status. The regulation further requires the debt collector to disclose in initial communications that it is attempting to collect a debt and that information obtained will be used for that purpose, and in later communications that the communication is from a debt collector, except for formal pleadings in legal actions.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector may not use any false, deceptive, or misleading representation to collect a debt. Prohibited conduct includes misrepresenting the amount or legal status of a debt, falsely implying affiliation with the government, threatening arrest or seizure of property unless lawful and intended, and falsely claiming to be an attorney. Collectors must also disclose in an initial communication that they are attempting to collect a debt and, in subsequent communications, that the message is from a debt collector.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-JUSTICE-COURT-DEBT-ANSWER-DEADLINE] ADVERSARIAL-GAP -- run run_20260830T103213Z, 2026-08-30T10:53:32Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': 'The creditor could not locate the debtor for in-person delivery, so the justice court authorized service by posting the citation on the door under Rule 501.2(e) (or substituted service under Rule 106). The petition was posted on March 3 and the debtor found it March 10.', 'exposes_gap': True, 'gap_description': "Both the logic ('deadline_computed_from: date of service (delivery by constable or process server)') and the checklist assume personal delivery. They provide no trigger date for alternative service methods (posting, mailing, publication, Rule 106(b) substituted service), where the operative date is the date of posting/mailing/publication rather than actual receipt, and where some methods carry a different answer window entirely. The rule as encoded either fails to fire or silently uses the wrong start date."}, {'scenario': "A debt buyer sues in justice court for $19,400 in principal but the petition also demands $1,800 in contractual pre-judgment interest and $2,500 in attorney's fees, for a total prayer of $23,700. The user answers the checklist question 'amount claimed in the suit' with $23,700.", 'exposes_gap': True, 'gap_description': "The checklist asks for 'amount claimed' without specifying that the $20,000 justice-court ceiling is measured exclusive of interest and costs (and with contested treatment of attorney's fees). A user reporting the gross prayer will be told justice court doesn't apply even though it does. The node also has no branch for what happens when the ceiling genuinely is exceeded — the county/district court answer deadline is materially different (Monday after 20 days from service), so the rule fails open with no fallback."}, {'scenario': 'The 14th day after service falls on a Friday when the county courthouse is closed under a local four-day-workweek order (or closed for an ice storm), which is not a state legal holiday. The defendant files the following Monday.', 'exposes_gap': True, 'gap_description': "The logic's extension trigger is 'weekend or court holiday,' which is broader and vaguer than TRCP 4's actual trigger ('Saturday, Sunday, or legal holiday'). Texas has no express clerk's-office-inaccessibility extension analogous to FRCP 6(a)(3), so the encoded rule may wrongly tell a defendant a locally-closed day is auto-extended. Conversely the checklist collects no fact about court closures or local holiday calendars, so the extension branch cannot be evaluated at all from the listed inputs."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under the cited text, a defendant's answer in a Texas justice court debt case is due 14 days after the date of service. If that 14th day lands on a weekend or a court holiday, the deadline rolls to the next business day. The same text notes that justice courts handle debt claims valued up to $20,000."
  - gpt-5.5: grounded=True, error=None, summary='In a Texas justice court debt-collection lawsuit, the defendant’s Answer is due 14 days after the date they are served. If the 14th day is a weekend or court holiday, the deadline extends to the next business day.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In a Texas justice court debt lawsuit, the answer is due 14 days after the date the defendant was served. If that 14th day falls on a weekend or a court holiday, the deadline is extended to the next business day. These rules apply to debt lawsuits worth up to $20,000 in Texas Justice Courts.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-EXEMPT-PERSONAL-PROPERTY] ADVERSARIAL-GAP -- run run_20260830T103213Z, 2026-08-30T10:52:27Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': "A single adult with no family, holding a valid driver's license, owns six unencumbered pickup trucks with a combined fair market value of $45,000 and no other personal property. The creditor levies on four of the trucks; the debtor claims all six are exempt because the aggregate is under the $50,000 cap.", 'exposes_gap': True, 'gap_description': 'The encoding treats the aggregate dollar cap as the only quantitative constraint, but § 42.002(a) contains item-specific numeric sub-limits — e.g., one motor vehicle per licensed family member (or per single adult, plus a non-licensed member who relies on another to drive), two firearms, 12 head of cattle, 60 head of other livestock, 120 fowl, two horses/mules/donkeys with tack. Property can fall well under the aggregate cap and still be non-exempt for exceeding a category count. Neither the logic nor the checklist asks how many units of each enumerated category the debtor owns.'}, {'scenario': "A family debtor's § 42.002(a) household goods, tools, and vehicles net out to $95,000, and the debtor also holds a $900,000 rollover IRA and a § 529 college savings plan for a child. The judgment creditor argues the IRA pushes the debtor past the $100,000 family cap, so the excess must be turned over.", 'exposes_gap': True, 'gap_description': "Retirement plans and IRAs are exempt without dollar limit under § 42.0021, and college savings/ABLE accounts under § 42.0022, entirely outside the § 42.002(a) aggregate cap. The 'unlimited_categories_outside_the_cap' list omits them, and the checklist's second dispositive fact ('aggregate FMV of § 42.002(a)-listed property') gives no instruction on classifying assets that are exempt under other § 42 provisions, inviting either erroneous inclusion in the cap or a false conclusion of non-exemption."}, {'scenario': 'Two weeks after a $400,000 judgment is signed, a single adult sells a nonexempt $48,000 brokerage account and uses the proceeds to buy jewelry, tools of the trade, and athletic equipment, keeping the total under $50,000. The creditor seeks turnover, alleging the conversion was made to defraud.', 'exposes_gap': True, 'gap_description': "Section 42.004 strips the exemption from personal property acquired by using nonexempt assets with intent to defraud, delay, or hinder a creditor (with tracing to the proceeds and a two-year limitations period). The encoding's only exemption-defeating condition is a pre-existing valid lien; the checklist collects no facts about the timing, source of funds, or intent behind the acquisition of the claimed-exempt property, so a fraudulent-conversion case would be resolved as fully exempt."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under Tex. Prop. Code § 42.001(a), the personal property listed in § 42.002 is exempt from garnishment, attachment, execution, or other seizure up to an aggregate fair market value of $100,000 for property provided for a family, or $50,000 for a single adult who is not a member of a family, in each case excluding liens, security interests, or other encumbrances. Section 42.002(a) lists the qualifying categories, including home furnishings and heirlooms, provisions for consumption, farm/ranch vehicles and implements, tools and books used in a trade or profession, clothing, jewelry (capped at 25 percent of the aggregate limit), two firearms, athletic and sporting equipment, one motor vehicle per licensed family member (or non-licensed person who relies on another driver), specified numbers of livestock and fowl with their forage, and household pets. Section 42.001(b) exempts additional property that does not count toward the aggregate caps: current wages for personal services (except for court-ordered child support enforcement), professionally prescribed health aids, alimony/support/separate maintenance, and a religious bible or book of sacred writings (except when seized by a landlord exercising rights after a lease breach or abandonment).'
  - gpt-5.5: grounded=True, error=None, summary='Texas exempts the personal property listed in Section 42.002 from garnishment, attachment, execution, or other seizure up to an aggregate fair market value of $100,000 for a family or $50,000 for a single adult who is not a family member, excluding liens and similar encumbrances. Certain items—such as current wages, prescribed health aids, support payments, and certain sacred religious writings—are exempt from seizure and are not counted toward those aggregate limits.'
  - gemini-2.5-pro: grounded=True, error=None, summary='Texas law exempts certain personal property from creditor seizure up to an aggregate fair market value of $100,000 for a family or $50,000 for a single adult, exclusive of liens. The types of property subject to this value cap include home furnishings, vehicles, tools of a trade, and two firearms. Some specific assets, such as current wages for personal services and professionally prescribed health aids, are exempt from seizure and are not included in these aggregate value limitations.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-HOMESTEAD-EXEMPTION] ADVERSARIAL-GAP -- run run_20260830T103213Z, 2026-08-30T10:51:30Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': 'A judgment debtor owns a 150-acre rural tract that he has occupied as his residence since 2015. He was married when the judgment was entered but was divorced (no children living with him) before the creditor levied on the land, so at the time of the levy he is a single adult.', 'exposes_gap': True, 'gap_description': "The checklist asks only for acreage and urban/rural status, never for the debtor's family status — yet the rule's own logic makes rural acreage turn on family (200) vs. single adult (100). It also gives no rule for the timing question (family status measured at designation, judgment, levy, or filing) or for what happens to the 50 excess acres (partial exemption plus debtor's right to designate the exempt portion under § 41.005/§ 41.0021 is entirely absent)."}, {'scenario': 'A debtor relocated to Texas 18 months ago, liquidated $3M of non-exempt securities, and paid cash for an urban 1-acre home; he then files Chapter 7, and separately the IRS has recorded a federal tax lien and a federal court has entered a criminal restitution order against him.', 'exposes_gap': True, 'gap_description': "The node flatly asserts 'NO dollar-value cap' and lists only state-law exceptions. It omits 11 U.S.C. § 522(p)'s ~$1.145M cap on homestead equity acquired within 1,215 days of a bankruptcy filing, § 522(o)'s reduction for equity from fraudulently converted nonexempt assets, and the supremacy-based override of Texas homestead by federal tax liens (26 U.S.C. § 6321) and federal criminal restitution/forfeiture (18 U.S.C. §§ 3613, 3664). The checklist never asks whether the claim is federal or when the property was acquired."}, {'scenario': 'A debtor sells her homestead, deposits the $400,000 in a segregated account, and closes on a replacement homestead five months later while an unsecured judgment creditor tries to garnish the account in month four.', 'exposes_gap': True, 'gap_description': 'The proceeds rule is stated but the checklist contains no proceeds-related fact at all — no sale date, no tracing/commingling inquiry, no question whether the funds were reinvested. A rule-applier following the three-item checklist would never gather the facts needed to run the § 41.001(c) branch the node itself contains.'}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Tex. Prop. Code § 41.001(a), a homestead — plus one or more lots used as a burial place — is exempt from seizure to satisfy creditors' claims, with the sole exception stated being encumbrances properly fixed on the homestead property. Section 41.002 caps the size of the protected homestead: an urban homestead (for a family or a single adult) may be no more than 10 acres, which may consist of one or more contiguous lots together with improvements. A rural homestead may be up to 200 acres for a family, or up to 100 acres for a single adult person."
  - gpt-5.5: grounded=True, error=None, summary='A Texas homestead is exempt from seizure for creditor claims, except for encumbrances properly fixed on the homestead property. The protected homestead is limited to not more than 10 acres for an urban home, not more than 200 acres for a rural family home, and not more than 100 acres for a rural home of a single adult person.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Texas, a homestead and burial lots are exempt from seizure by creditors, except for properly fixed encumbrances on the homestead. An urban homestead consists of up to 10 acres of land for a family or single adult. A rural homestead consists of up to 200 acres for a family or up to 100 acres for a single adult.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-WAGE-GARNISHMENT-PROHIBITION] ADVERSARIAL-GAP -- run run_20260830T103213Z, 2026-08-30T10:50:32Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': 'A Texas resident defaults on a federally guaranteed student loan and the Department of Education issues an administrative wage garnishment order to her Texas employer for 15% of disposable pay; separately the IRS serves a continuous levy on the same wages for unpaid income tax.', 'exposes_gap': True, 'gap_description': "The rule treats 'ordinary debt' vs. child support/spousal maintenance as the only axis. It omits federal-law garnishments (Dept. of Education AWG under 20 U.S.C. 1095a, IRS levies under 26 U.S.C. 6331, federal criminal restitution under the MVRA, and federal-court judgments under the FDCPA of 1990), which preempt the Texas constitutional exemption via the Supremacy Clause. The checklist would lead a user to conclude these garnishments are unconstitutional when they are fully enforceable in Texas."}, {'scenario': 'A judgment debtor works as a 1099 real-estate agent paid pure commissions by a Texas brokerage, and also receives quarterly distributions from an LLC he owns; the creditor serves a writ of garnishment on the brokerage and the LLC to capture amounts owed to him.', 'exposes_gap': True, 'gap_description': "The protection covers 'current wages for personal services' from an employer-employee relationship. Texas case law generally holds that independent-contractor compensation, commissions owed to non-employees, LLC/partnership distributions, rents, and certain bonuses are NOT current wages and can be garnished. The checklist's binary 'wages vs. bank account vs. support' framing has no slot for characterizing the payer-payee relationship or the nature of the payment, so it wrongly protects non-wage earned income."}, {'scenario': "A Texas-domiciled debtor is employed by a Nevada company; the creditor domesticates its Texas judgment in Nevada and serves a wage garnishment writ there on the employer's Nevada payroll office, garnishing 25% of pay under Nevada law before the funds are remitted to the debtor.", 'exposes_gap': True, 'gap_description': "The rule states no choice-of-law or jurisdictional predicate. The Texas exemption is generally applied by Texas courts and depends on where garnishment is sought and which state's exemption law the forum applies; a sister state may apply its own procedural/exemption law. The checklist never asks where the employer, payroll situs, or garnishment forum is, so it overstates the protection as if it followed the debtor everywhere."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under the Texas Constitution, current wages for personal service can never be garnished, with only two express exceptions: court-ordered child support payments and court-ordered spousal maintenance. Because ordinary consumer debts (e.g., credit cards, medical bills, personal loans) fall outside those two exceptions, a creditor holding such a debt cannot garnish a Texan's current wages. Note the protection as written covers 'current wages for personal service'; the text does not address other property or funds that are no longer current wages."
  - gpt-5.5: grounded=True, error=None, summary='Texas law provides that current wages for personal service are not subject to garnishment. The only listed exceptions are for enforcement of court-ordered child support payments or spousal maintenance, so the text supports that wage garnishment for ordinary consumer debt is constitutionally prohibited.'
  - gemini-2.5-pro: grounded=True, error=None, summary='The Texas Constitution states that current wages for personal services can never be subject to garnishment. The only exceptions to this rule are for court-ordered child support payments and spousal maintenance. Since ordinary consumer debt is not one of these specified exceptions, the constitutional prohibition on wage garnishment applies to it.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-SOL-CONSUMER-DEBT] ADVERSARIAL-GAP -- run run_20260830T103213Z, 2026-08-30T10:49:31Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': "A consumer defaulted on a credit card in 2015 and made no payments until 2022, when a collector persuaded her to make a $25 'goodwill' payment by phone with no signed writing. The collector sues in 2024, arguing the 2022 payment is the 'date of last payment' and thus the accrual date.", 'exposes_gap': True, 'gap_description': "The checklist treats 'date of last payment' as the dispositive accrual fact without distinguishing payments made before expiration (which may extend/restart accrual) from payments made after the period has already run. Texas Civ. Prac. & Rem. Code § 16.065 bars revival of a barred claim by acknowledgment unless it is in writing and signed by the debtor, and the interaction of unsigned partial payments with revival is unaddressed. Revival/acknowledgment is a distinct doctrine from tolling, so it is not captured by the tolling flag either."}, {'scenario': 'A Texas resident opened a credit card with a Delaware-chartered bank; the cardholder agreement contains a Delaware choice-of-law clause (3-year limitations period), and the debtor defaulted in 2021 while living and working in Delaware before moving to Texas in 2022. The Texas collection suit is filed in 2025.', 'exposes_gap': True, 'gap_description': "The node hard-codes a 4-year Texas period and never asks where the cause of action accrued, the debtor's residence at accrual, or whether a contractual choice-of-law clause applies. Texas's borrowing statute (§ 16.067) can import a shorter foreign limitations period for claims accruing outside Texas against a then-nonresident, and Texas courts have enforced foreign choice-of-law provisions on limitations in card cases. Applying the 4-year default would wrongly declare a time-barred claim live."}, {'scenario': 'A consumer signed a 60-month retail installment contract with an optional (non-automatic) acceleration clause, stopped paying in 2018, and the creditor never sent a notice of intent to accelerate or notice of acceleration; the creditor sues in 2024 for all remaining installments. Alternatively, the creditor obtained a default judgment on the same debt in 2016 and is now suing to collect on that judgment.', 'exposes_gap': True, 'gap_description': "The checklist assumes a single accrual date, but installment obligations accrue separately as each payment comes due, so some installments may be barred while others are timely; and optional acceleration requires notice of intent and notice of acceleration before the full balance accrues, making the 'date of default' fact insufficient. The node also fails to screen for whether the debt was already reduced to judgment, which shifts the analysis to the 10-year judgment-dormancy/revival regime (§§ 34.001, 31.006) rather than § 16.004."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under the cited provision, a suit on a "debt" is among the listed actions that must be filed no later than four years after the day the cause of action accrues. So a Texas lawsuit to collect a consumer debt is subject to a four-year limitations period running from accrual of the claim. The text lists debt alongside specific performance of a real-property conveyance contract, penal-clause bond claims, fraud, and breach of fiduciary duty, but it does not define "debt" or say when a debt claim accrues.'
  - gpt-5.5: grounded=True, error=None, summary='The cited statute says a person must bring suit on an action for “debt” no later than four years after the day the cause of action accrues. The text does not separately define or mention “consumer debt,” but it provides a four-year limitations period for debt actions.'
  - gemini-2.5-pro: grounded=True, error=None, summary='According to the provided Texas statute, a person must bring a lawsuit for debt no later than four years after the day the cause of action accrues. The text explicitly lists "debt" as one of the actions subject to this four-year limitations period.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY] ADVERSARIAL-GAP -- run run_20260830T103213Z, 2026-08-30T10:48:29Z

**File:** `rules/debt/state/texas/tx_debt_band3_discretionary_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': "A defendant learns of the default judgment 55 days after it was signed because the clerk mailed notice to a stale address; under TRCP 306a(4)-(5) the post-judgment deadlines run from the date of actual knowledge (up to 90 days after signing), provided a sworn 306a motion is filed. The checklist's second item would classify her as past the 30-day gate and tell her the path is foreclosed.", 'exposes_gap': True, 'gap_description': "The 'deterministic' 30-day gate is stated as running from the signing date with no exception. It omits TRCP 306a(4)-(5)'s late-notice rule, which restarts the clock from the date the party first received notice or acquired actual knowledge. The checklist never asks when the person learned of the judgment, only when it was signed, so the one Band 1 element in the node can produce a confidently wrong 'foreclosed' answer in exactly the fact pattern (defendant never got notice) most common in default cases."}, {'scenario': "A defendant was never validly served — the process server left citation with a neighbor and the return is defective — and he discovers the judgment eight months later. Under Peralta v. Heights Medical Center and Texas law on void judgments, Craddock's three factors (including the meritorious-defense showing) do not apply to a defendant who was not served, and other vehicles remain available (restricted appeal within six months, bill of review within four years, or a collateral attack on a void judgment).", 'exposes_gap': True, 'gap_description': "Neither the logic nor the checklist asks whether service of process was valid, and the node treats the 30-day motion-for-new-trial window as the exclusive path ('missing the 30-day window forecloses this path entirely'). It therefore (a) applies the Craddock framework to a class of cases where Texas law says Craddock does not govern, and (b) risks telling a defendant with a void judgment that nothing can be done, when the more consequential and largely deterministic questions — was service valid, and are the restricted-appeal/bill-of-review windows open — are never surfaced."}, {'scenario': 'A tenant receives a default judgment from a justice court in an eviction/small-claims suit and asks whether it can be reopened. Justice court practice is governed by TRCP 500-510, where a motion to set aside a default or for new trial is due within 14 days of the judgment (Rule 505.3), and an eviction appeal bond is due within 5 days — not the 30-day TRCP 329b window.', 'exposes_gap': True, 'gap_description': "The checklist never asks which court entered the judgment. The node hard-codes TRCP 329b's 30/75-day framework, which does not apply in justice courts (Rule 500.3(b) expressly excludes most of Part II of the rules), and in evictions the far shorter appeal-bond deadline is the operative gate. Giving a JP-court defendant a '30 days' figure is affirmatively harmful in the one component the node claims is deterministic and safe to state."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Craddock, a default judgment should be set aside and a new trial granted whenever three conditions are met: (1) the defendant's failure to answer before judgment was not intentional or the result of conscious indifference, but due to mistake or accident; (2) the motion for new trial sets up a meritorious defense; and (3) the motion is filed at a time when granting it will cause no delay or other injury to the plaintiff. The text frames this as a structured three-element test — if all three are satisfied the judgment 'should be set aside' — rather than as open-ended discretion, though elements like 'conscious indifference' and 'meritorious defense' require case-specific judgment. Procedurally, the motion must be filed within thirty days after the judgment is signed (Rule 329b(a)), and if not ruled on by written order within seventy-five days after the judgment was signed, it is overruled by operation of law (Rule 329b(c))."
  - gpt-5.5: grounded=True, error=None, summary='Under Craddock, a Texas default judgment should be set aside and a new trial ordered when the defendant’s failure to answer was not intentional or due to conscious indifference, but resulted from mistake or accident, and the motion sets up a meritorious defense and can be granted without delay or injury to the plaintiff. The motion for new trial must be filed before or within 30 days after judgment, and if not decided by signed written order within 75 days after judgment, it is overruled by operation of law. The quoted rule is a multi-condition standard, but the text says the judgment “should” be set aside when those conditions are met rather than describing an open-ended discretionary determination.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A Texas default judgment should be set aside if the motion for new trial meets a three-part test. First, the defendant's failure to answer must have been due to a mistake or accident, not intentional or the result of conscious indifference. Second, the motion must set up a meritorious defense. Finally, the motion must be filed at a time when granting it will not cause delay or injure the plaintiff."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-CIVIL-ANSWER-DEADLINE] ADVERSARIAL-GAP -- run run_20260830T103213Z, 2026-08-30T10:47:12Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': "The process server left the summons with the defendant's adult roommate at the defendant's home on March 1 and mailed a copy to the same address on March 3 (substituted service under CCP 415.20). The defendant calculates the answer deadline as March 31, 30 days after the papers were handed to the roommate.", 'exposes_gap': True, 'gap_description': "The checklist asks only for 'the date the summons was actually served,' but under California law the service date depends on the method: substituted service is deemed complete on the 10th day after mailing, service by publication on the 28th day after first publication, service via the Secretary of State on a corporation 10 days after delivery, and mail service with acknowledgment on the date the acknowledgment is signed. The node has no field for method of service and no rule for computing the constructive service date, so it will systematically under-count the deadline for every non-personal service."}, {'scenario': 'The defendant is personally served on October 25, making day 30 fall on a Saturday that is followed by a court holiday on Monday. The defendant files an answer on the following Tuesday.', 'exposes_gap': True, 'gap_description': "The determination 'date_of_service + 30 days' contains no weekend/holiday rollover. CCP 12, 12a and 12b extend a deadline falling on a Saturday, Sunday, or judicial holiday (including days the clerk's office is closed) to the next court day. The node would tell this timely defendant they defaulted, and would also miss the fact that the first day is excluded from the count."}, {'scenario': "Within 30 days of service, the defendant files a demurrer challenging the debt buyer's failure to plead the chain of title, and separately the parties sign a stipulation under CRC 3.110(d) granting a 15-day extension to respond. No 'answer' is ever filed within 30 days.", 'exposes_gap': True, 'gap_description': "The logic treats 'answer' as the only responsive filing and assumes default follows automatically if none is filed. In fact any responsive pleading under CCP 585/586 -- demurrer, motion to quash, motion to strike, motion to transfer -- prevents default, and the deadline is routinely extended by stipulation (up to 15 days) or by court order under CCP 1054 (up to 30 days). The checklist captures no fact about the type of response filed or any extension/stipulation, so it will wrongly report a default risk."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 412.20(a)(3), the summons must direct the defendant to file a written pleading responding to the complaint within 30 days after the summons is served on the defendant. Subdivision (a)(6) reinforces this with the warning that the court may decide against the defendant without a hearing unless they respond within 30 days. If the defendant does not respond, subdivision (a)(4) provides that a default may be entered on the plaintiff's application and the plaintiff may obtain the relief demanded, which could include garnishment of wages or taking of money or property. The text states a general summons requirement and does not set out any rule specific to debt-collection suits."
  - gpt-5.5: grounded=True, error=None, summary='A defendant must file a written pleading responding to the complaint within 30 days after the summons is served. If the defendant does not respond within that time, default may be entered and the plaintiff may seek the relief demanded in the complaint.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A defendant must file a written pleading in response to a complaint within 30 days after the summons is served on them. The summons must include a notice explicitly stating that the person has been sued and must respond within 30 days to avoid a default judgment. Failure to respond can result in the plaintiff applying for relief, which may include garnishment of wages or the taking of money or property.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-BANK-ACCOUNT-EXEMPTION] ADVERSARIAL-GAP -- run run_20260830T103213Z, 2026-08-30T10:46:13Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': "A former employee obtains a single judgment against her ex-employer for $80,000, of which $12,000 is expressly unpaid wages and $68,000 is emotional-distress and punitive damages on a wrongful-termination claim. She levies the employer-debtor's bank account for the full amount.", 'exposes_gap': True, 'gap_description': "The rule treats the carve-out as a binary classification of the judgment ('ordinary debt judgment vs. wages/support judgment'), but judgments are frequently mixed. Nothing in the logic or checklist addresses apportionment: whether the exemption is defeated entirely, defeated only as to the wage portion of the levy, or preserved because the levy is not solely 'to satisfy a judgment for wages owed.' A related unaddressed sub-question is whether a Labor Commissioner ODA entered as a judgment, or a wage/support judgment later assigned to a third-party debt buyer, retains its carve-out character."}, {'scenario': 'The judgment debtor is one of two signatories on a joint checking account he shares with his non-debtor adult daughter, whose paychecks fund roughly 80% of the balance; the creditor levies the entire account. The debtor also has a second account at a different bank.', 'exposes_gap': True, 'gap_description': "The checklist's non-dispositive multi-account item points to CCP §704.220(e) aggregation/allocation but the node never encodes the co-ownership dimension: whether the automatic exemption amount is per-debtor, per-account, or multiplied where multiple depositors are on one account, and how a non-debtor co-owner's tracing/ownership claim interacts with an exemption that by design 'applies without the debtor filing a claim.' Treating a fact flagged as dispositive-adjacent (aggregation across accounts) as 'not dispositive' also risks under-protecting a debtor whose funds are split across institutions."}, {'scenario': "The debtor's only funds are $2,000 of direct-deposited Social Security benefits sitting in a credit union share draft account, plus $600 loaded on a prepaid payroll debit card issued by a fintech program bank; the creditor levies both.", 'exposes_gap': True, 'gap_description': "The node defines the protected res only as 'money in the debtor's deposit account' without defining 'deposit account' (e.g., credit union share accounts, prepaid card/fintech custodial pooled accounts, brokerage cash sweeps, safe-deposit cash, funds in transit), and it is silent on stacking: whether this automatic exemption is additive to or subsumed by CCP §704.080's automatic exemption for directly deposited public benefits and §704.070 paid earnings. The determination's single-cap framing could cause a user to cap a Social Security depositor at the §11452 figure when a larger or independent exemption applies. Separately, the node instructs the user to pull the 'current' figure but never fixes the operative date (levy date, claim-of-exemption date, or hearing date), which matters when the §11453 adjustment lands mid-levy."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.220(a), money in a judgment debtor's deposit account is automatically exempt — with no claim of exemption required — up to an amount equal to the minimum basic standard of adequate care for a family of four for Region 1, as set by Welfare and Institutions Code section 11452 and annually adjusted by the State Department of Social Services under section 11453. The statute states the exemption as a formula rather than a fixed dollar figure, so the actual amount depends on the current annual adjustment. This automatic exemption does not apply, however, to money levied upon to satisfy a judgment for wages owed (including damages and penalties), child support, or spousal support, per § 704.220(c)(1)."
  - gpt-5.5: grounded=True, error=None, summary='Money in a judgment debtor’s deposit account is automatically exempt, without the debtor making a claim, up to an amount equal to the minimum basic standard of adequate care for a family of four for Region 1, as established and annually adjusted under the cited Welfare and Institutions Code provisions. This automatic exemption does not apply when the money is levied to satisfy a judgment for wages owed, child support, or spousal support; “wages owed” includes damages and penalties.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-BANK-ACCOUNT-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260830T103213Z, 2026-08-30T10:46:13Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['1', '4'], OpenAI=['1', '4'], Gemini=[] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.220(a), money in a judgment debtor's deposit account is automatically exempt — with no claim of exemption required — up to an amount equal to the minimum basic standard of adequate care for a family of four for Region 1, as set by Welfare and Institutions Code section 11452 and annually adjusted by the State Department of Social Services under section 11453. The statute states the exemption as a formula rather than a fixed dollar figure, so the actual amount depends on the current annual adjustment. This automatic exemption does not apply, however, to money levied upon to satisfy a judgment for wages owed (including damages and penalties), child support, or spousal support, per § 704.220(c)(1)."
  - gpt-5.5: grounded=True, error=None, summary='Money in a judgment debtor’s deposit account is automatically exempt, without the debtor making a claim, up to an amount equal to the minimum basic standard of adequate care for a family of four for Region 1, as established and annually adjusted under the cited Welfare and Institutions Code provisions. This automatic exemption does not apply when the money is levied to satisfy a judgment for wages owed, child support, or spousal support; “wages owed” includes damages and penalties.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-VEHICLE-EXEMPTION] ADVERSARIAL-GAP -- run run_20260830T103213Z, 2026-08-30T10:44:47Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': "The debtor's only car is sold at execution sale in January; the levying officer pays the debtor $7,500 automatically, and the debtor deposits it in a general checking account already holding wages and Social Security deposits. Eleven months later a second creditor levies on that bank account, and the debtor claims the funds are still exempt vehicle proceeds.", 'exposes_gap': True, 'gap_description': 'The node and checklist ignore the temporal and tracing limits on proceeds. CCP § 704.010(b) exempts execution-sale and insurance/indemnification proceeds only for 90 days after receipt, and exempt status generally requires the funds be traceable and not commingled. The checklist collects only FMV, encumbrances, and vehicle count — nothing about the date proceeds were received, the date of the new levy, or commingling — so the rule would wrongly protect stale, untraceable funds.'}, {'scenario': "A creditor levies on the debtor's vehicle in June 2025. The debtor's equity is $8,900. The rule returns $7,500 exempt and $1,400 reachable, without reference to the triennial cost-of-living adjustment published by the Judicial Council under CCP § 703.150 that took effect April 1, 2025.", 'exposes_gap': True, 'gap_description': 'The $7,500 figure is hard-coded and the checklist omits the dispositive fact of the levy/valuation date. CCP § 703.150 requires triennial CPI adjustment of § 704.010 amounts, so the correct exemption depends on when the exemption is asserted. The rule will silently produce an under-inclusive (or, after a future amendment, over-inclusive) exemption.'}, {'scenario': 'A married couple are both judgment debtors on the same judgment. They own two vehicles as community property with combined equity of $14,000, and each spouse claims a separate $7,500 exemption, arguing the household is entitled to $15,000 total.', 'exposes_gap': True, 'gap_description': "The checklist captures no facts about the debtor's marital status, whether both spouses are judgment debtors, or the character of the vehicles as community versus separate property. CCP § 703.110 governs how exemptions apply to married judgment debtors and community property, and whether § 704.010 can be doubled is a distinct legal question the node's 'combined, not stacked' language addresses only for a single debtor's multiple vehicles."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.010(a), a judgment debtor may exempt up to $7,500 in any combination of the aggregate equity in motor vehicles, the proceeds of an execution sale of a motor vehicle, and insurance or other indemnification proceeds for a vehicle's loss, damage, or destruction. Subdivision (d) adds that if the debtor owns only one motor vehicle and it is sold at an execution sale, $7,500 of the sale proceeds is automatically exempt without the debtor having to file a claim, with the levying officer permitted to rely on Department of Motor Vehicles records to verify sole ownership. In that single-vehicle situation, the separate subdivision (a) exemption is not also available."
  - gpt-5.5: grounded=True, error=None, summary='California exempts up to $7,500 for any combination of aggregate equity in motor vehicles, proceeds from an execution sale of a motor vehicle, and insurance or indemnification proceeds for loss, damage, or destruction of a motor vehicle. If the judgment debtor has only one motor vehicle and it is sold at an execution sale, $7,500 of the sale proceeds is exempt without making a claim; in that situation, the subdivision (a) exemption is not available.'
  - gemini-2.5-pro: grounded=True, error=None, summary="Under California law, a person's aggregate equity in motor vehicles is exempt from creditors up to seven thousand five hundred dollars ($7,500). This exemption amount also applies to the proceeds from an execution sale or from insurance for the loss or damage of a motor vehicle. If a person has only one motor vehicle and it is sold, the $7,500 exemption is applied to the proceeds automatically without a claim being made."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-HOMESTEAD-EXEMPTION] ADVERSARIAL-GAP -- run run_20260830T103213Z, 2026-08-30T10:43:46Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': "A judgment creditor holding a judgment for unpaid child and spousal support arrears (or a lender enforcing a consensual deed of trust, or the FTB enforcing a tax lien) moves to force sale of the debtor's occupied dwelling. The debtor claims the full computed exemption amount.", 'exposes_gap': True, 'gap_description': "The checklist never asks what kind of obligation the judgment enforces. The homestead exemption does not defeat consensual liens (mortgages/deeds of trust), mechanics' liens, tax liens, or (under CCP § 703.070 and related law) support obligations, which are subject to special treatment. The determination text says 'ordinary money judgment' but no dispositive fact captures whether the claim is ordinary, so the node can be applied to a claim it does not govern."}, {'scenario': "A creditor recorded an abstract of judgment creating a judgment lien on the debtor's home in 2018, when the exemption was $75,000–$175,000; the forced sale is sought now under the post-2021 formula, and the debtor's equity is $400,000.", 'exposes_gap': True, 'gap_description': "The checklist omits the date the judgment lien attached (and the date of the judgment/levy), which is dispositive in disputes over whether the 2021 amendment applies retroactively to liens that attached earlier, and over which year's 'prior calendar year' median and inflation adjustment apply (the year the exemption is claimed vs. the year of levy or lien attachment)."}, {'scenario': 'Two spouses are both judgment debtors on the same judgment and co-own the dwelling; each files a homestead declaration and each claims the full computed exemption, and one spouse also owns and occupies a second dwelling in a different, higher-median county.', 'exposes_gap': True, 'gap_description': "The encoded formula and checklist are silent on the statutory one-exemption-per-married-couple limit (CCP § 704.730(b)) and on co-ownership/apportionment among multiple owners or debtors. They also say 'debtor's county' rather than the county where the homestead is located, and give no rule for selecting among multiple dwellings or for counties lacking published median sale-price data."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.730(a), a judgment debtor's homestead exemption equals the greater of (1) the countywide median sale price for a single-family home in the calendar year before the year the exemption is claimed, capped at $600,000, or (2) a floor of $300,000. So the protected amount is never less than $300,000 and never more than $600,000 based on local median home prices. Subdivision (b) provides that both figures adjust annually for inflation starting January 1, 2022, using the change in the annual California Consumer Price Index for All Urban Consumers published by the Department of Industrial Relations for the most recent one-year period ending December 31 before the adjustment, rounded to the nearest $25. The excerpt sets the exemption amount only; it does not describe the forced-sale procedure itself."
  - gpt-5.5: grounded=True, error=None, summary="The homestead exemption amount is the greater of either the prior calendar year's countywide median sale price for a single-family home, capped at $600,000, or $300,000. Beginning January 1, 2022, those amounts adjust annually for inflation based on the California CPI for All Urban Consumers, rounded to the nearest $25."
  - gemini-2.5-pro: grounded=True, error=None, summary="The California homestead exemption is the greater of two amounts: $300,000, or the county's median sale price for a single-family home in the prior calendar year. However, the median sale price amount cannot exceed $600,000. These amounts are adjusted annually for inflation based on the California Consumer Price Index."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-WAGE-GARNISHMENT-LIMIT] ADVERSARIAL-GAP -- run run_20260830T103213Z, 2026-08-30T10:42:20Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': "A judgment creditor obtained a judgment on a personal guaranty the debtor signed for his failed LLC's equipment lease, and serves an earnings withholding order. The employer applies the 20%/40% formula. The creditor objects that CCP § 706.050's enhanced protection applies only to judgments on 'consumer debt' as defined in § 706.011, and a commercial guaranty judgment is still capped at the older 25%-of-disposable / 30x-minimum-wage federal-conforming formula.", 'exposes_gap': True, 'gap_description': "The checklist never asks the threshold characterization fact — whether the underlying judgment is on a 'consumer debt' within the meaning of CCP § 706.011/706.050. That fact is dispositive of whether this node's formula applies at all, yet a user could satisfy every listed fact and still apply the wrong cap to a commercial, tort, tax, restitution, or family-support judgment."}, {'scenario': "A part-time debtor in a city with a $19.36 local minimum wage has $700 in weekly disposable earnings. 48 x $19.36 = $929.28, so prong two is 40% of (-$229.28) = -$91.71, while prong one is $140. Taking 'the lesser of the two prongs' literally yields a negative maximum garnishment, and the employer's payroll system withholds nothing but the creditor argues the negative result should be read as an offset or that prong one controls.", 'exposes_gap': True, 'gap_description': "The formula has no floor at zero and no stated rule for when disposable earnings fall at or below 48x the applicable minimum wage. The determination language ('the lesser of the two prongs') produces a mathematically negative garnishment amount rather than the legally correct result of zero withholding, and the node gives no instruction to clamp the result."}, {'scenario': 'A fully remote debtor lives in Fresno (state minimum wage), her employer is headquartered in Seattle, and her formal work location on file is a co-working desk in West Hollywood (higher local minimum wage) that she visits twice a month; her biweekly pay period runs December 24 to January 6, straddling a January 1 state and local minimum wage increase.', 'exposes_gap': True, 'gap_description': "Two uncovered ambiguities: (1) 'where the debtor works' is undefined for remote, multi-jurisdiction, or itinerant workers, so the checklist's 'applicable local minimum wage' fact cannot be reliably ascertained; (2) 'in effect when earnings are payable' is not reconciled with pay periods that straddle a wage-rate change, and the checklist treats pay period as non-dispositive even though here it drives which minimum wage figure — and thus which dollar cap — governs."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 706.050(a), and unless the chapter provides otherwise, the amount of an individual judgment debtor's disposable earnings for any workweek that can be taken under an earnings withholding order is capped at the lesser of (1) 20% of that week's disposable earnings, or (2) 40% of the amount by which those disposable earnings exceed 48 times the applicable minimum hourly wage. If the debtor works where a local minimum wage exceeds the state minimum wage, the higher local rate is used in the second calculation. This version of the section became operative September 1, 2023 (§ 706.050(c)). Note that the quoted text states a general rule for individual judgment debtors and does not itself set out a separate rule specific to consumer debts."
  - gpt-5.5: grounded=True, error=None, summary='Operative September 1, 2023, the maximum disposable earnings subject to levy under an earnings withholding order for an individual judgment debtor in a workweek is the lesser of: 20% of that week’s disposable earnings, or 40% of the amount by which that week’s disposable earnings exceed 48 times the applicable minimum hourly wage. The state minimum wage is used unless the debtor works where a higher local minimum wage applies, in which case the local minimum wage is used.'
  - gemini-2.5-pro: grounded=True, error=None, summary="Effective September 1, 2023, the maximum amount of an individual's disposable earnings that can be garnished for a workweek is the lesser of two amounts. The first is 20% of the individual's disposable earnings for that week. The second is 40% of the amount by which the weekly disposable earnings exceed 48 times the applicable state or local minimum hourly wage."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-ORAL-CONTRACT-DEBT] ADVERSARIAL-GAP -- run run_20260830T103213Z, 2026-08-30T10:40:54Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': 'A consumer is sued by a retailer on a revolving store account with no signed credit agreement; the parties agree there is no written contract, and the last purchase/payment was 3 years before suit. The retailer produces a running ledger of charges, payments and balances and pleads it as an open book account.', 'exposes_gap': True, 'gap_description': "The node treats the universe as binary (written = 4 years, not-written = 2 years), but CCP 337(b) gives open book accounts a 4-year period even though they are not 'founded on a written instrument,' and account stated is separately analyzed. A confirmed 'not written' answer on the checklist would push this to 2 years and produce a wrong 'expired' determination. The checklist has no fact for whether the obligation qualifies as a book account or account stated."}, {'scenario': "A debt buyer filed suit on a verbal loan 22 months after the borrower's last payment, but the case has been pending for two years due to service and discovery delays, and the borrower now raises the statute of limitations at trial.", 'exposes_gap': True, 'gap_description': "The determination compares 'today' to accrual + 2 years, but the operative date under CCP 350 is the date the action was commenced (complaint filed), not the date of adjudication. The checklist collects no filing/commencement date, so a timely-filed suit would be mislabeled 'expired.' Relation-back of amended complaints adding new claims or Doe defendants is likewise uncaptured."}, {'scenario': "Three years after defaulting on an oral loan, the debtor emails the lender: 'I know I still owe you the $8,000 and I'll pay it when I can,' signs the email, but makes no payment. The lender sues one year later.", 'exposes_gap': True, 'gap_description': "CCP 360 revives/restarts the period on a new promise or acknowledgment in a signed writing (and separately on part payment). The checklist captures only 'date of last payment' and would return 'expired' here, missing written acknowledgment as an independent accrual-restarting fact. Related uncaptured tolling facts include defendant's absence from the state (CCP 351), bankruptcy stay, minority/incapacity, and the borrowing statute (CCP 361) for out-of-state claims."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under California Code of Civil Procedure § 339(1), an action on a contract, obligation, or liability that is NOT founded upon a written instrument — such as an oral or implied consumer debt agreement — must be brought within two years. The text carves out exceptions governed by Commercial Code § 2725 and Code of Civil Procedure § 337(2), which are covered by their own limitations rules. The same two-year period also applies to claims evidenced by a certificate, abstract, or guaranty of title to real property or a title insurance policy, except that those causes of action do not accrue until the aggrieved party discovers the loss or damage.'
  - gpt-5.5: grounded=True, error=None, summary='An action on a contract, obligation, or liability that is not founded upon a written instrument must be brought within two years. The text provides exceptions for certain Commercial Code or other specified provisions, but the general limitations period stated for an unwritten contract is two years.'
  - gemini-2.5-pro: grounded=True, error=None, summary='The statute of limitations for an action on a contract, obligation, or liability that is not founded on a written instrument is two years. The text provides that this rule has exceptions, such as those found in Section 2725 of the Commercial Code or subdivision 2 of Section 337, but does not describe them.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] MODEL-DISAGREEMENT -- run run_20260830T103213Z, 2026-08-30T10:38:11Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['30', '5'], OpenAI=['30', '5'], Gemini=['30'] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 15 U.S.C. § 1692g(a) and 12 C.F.R. § 1006.34(a)(1), a notice is compliant only if the debt collector conveyed the validation information in the initial communication (orally under the Reg F option) or sent/provided it within five days of that initial communication, and the content includes all required items: the amount of the debt, the creditor to whom it is owed, the 30-day dispute/assumption-of-validity statement, the written-dispute verification statement, and the original-creditor-request statement — plus, under 12 C.F.R. § 1006.34(c), the collector communication disclosure, itemization details, the dispute-window end date, the CFPB website statement, and consumer-response prompts and addresses. The dispute window runs 30 days from the consumer's receipt of the notice (§ 1692g(a)(3)); under 12 C.F.R. § 1006.34(b)(5) the validation period starts when the information is provided and ends 30 days after actual or assumed receipt, with receipt assumable on any date at least five days (excluding legal public holidays, Saturdays, and Sundays) after it was provided. If a written dispute or original-creditor request arrives within that period, § 1692g(b) requires the collector to cease collection of the disputed portion until it mails verification, a judgment copy, or the original creditor's name and address; otherwise collection activity may continue during the 30 days. The excerpt supplies this framework but contains no facts about any particular notice or date, so whether a specific consumer received a compliant notice or remains within the window cannot be determined from this text alone."
  - gpt-5.5: grounded=False, error=None, summary='The cited provisions state what a compliant validation notice must include and when it must be provided: in the initial communication, within five days after it, or orally in the initial communication under the regulation. The dispute/validation period runs from when validation information is provided and ends 30 days after the consumer receives or is assumed to receive it, with an assumption of receipt at least five business days after provision. However, the text provides no facts about what notice was actually sent, when it was sent or received, or what it contained, so whether a compliant notice was provided and whether the consumer is still within the dispute window cannot be determined from the excerpt alone.'
  - gemini-2.5-pro: grounded=False, error=None, summary="The provided legal texts establish the requirements for a compliant debt validation notice, including its content and timing. The texts also define the consumer's dispute window as 30 days from the receipt of this notice, and provide a method for calculating the date of receipt. However, because the texts do not contain any specific facts about whether a notice was actually sent in this case or when it was sent, it is impossible to determine compliance or the status of the dispute window."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] ADVERSARIAL-GAP -- run run_20260830T103213Z, 2026-08-30T10:36:54Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': 'A collector induces the consumer to write a postdated check, then tells her that if the check is dishonored it will refer the matter for criminal bad-check prosecution. The collector never deposits the check early and in fact gives proper 3-10 day advance written notice before depositing it on its date.', 'exposes_gap': True, 'gap_description': "Catalog item (3) (soliciting a postdated instrument for the purpose of threatening or instituting criminal prosecution) has no corresponding entry in the completeness checklist. The checklist's postdated-check fact asks only whether the instrument was deposited early or without proper notice — both answered 'no' here — so a fact-gatherer working the checklist would close the file despite a facially complete item (3) violation."}, {'scenario': "A collector repeatedly places collect (reverse-charge) calls to the debtor and sends premium-rate SMS messages, identifying itself only as 'M.J. Associates re: your account' without disclosing that the calls concern debt collection, causing the debtor to incur roughly $80 in charges.", 'exposes_gap': True, 'gap_description': "Catalog item (5) (causing charges for communications by concealing the true purpose) is entirely absent from the completeness checklist; none of the four checklist facts asks about communication charges or concealment of purpose. The checklist is therefore under-inclusive relative to the node's own catalog, and it also does not address whether modern reverse-charge/data-charge media count as the 'collect call or telegram' analogues."}, {'scenario': 'A collector, seeking payment on a time-barred and bankruptcy-discharged debt, sues the consumer in a county 200 miles from her residence and simultaneously tells her adult children that she is a deadbeat, but collects no unauthorized amount, uses no postdated check, threatens no repossession, and mails only sealed, unmarked envelopes.', 'exposes_gap': True, 'gap_description': "The node's determination treats the eight enumerated items as the universe of §1692f liability ('any single catalog item, if the facts match, is an independent violation'), but §1692f's prefatory clause independently prohibits any 'unfair or unconscionable means' — the list is expressly non-exhaustive. Neither the logic nor the checklist captures residual-clause conduct, and the checklist provides no catch-all fact prompting inquiry into other unfair practices."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692f broadly bars debt collectors from using unfair or unconscionable means to collect a debt, and then lists specific violations without limiting that general ban. These include: collecting any amount (interest, fees, charges, expenses) not expressly authorized by the agreement creating the debt or permitted by law; accepting a check postdated more than five days without written notice of intent to deposit sent 3-10 business days before deposit; soliciting postdated instruments to threaten or institute criminal prosecution; depositing or threatening to deposit a postdated instrument early; causing a person to incur communication charges by concealing the communication's true purpose; and taking or threatening nonjudicial dispossession or disablement of property where there is no present right to possession through an enforceable security interest, no present intention to take possession, or the property is legally exempt. It also prohibits communicating with a consumer about a debt by post card and using any language or symbol other than the collector's address on mail or telegram envelopes, though a business name may be used if it does not indicate the debt collection business."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect or attempt to collect a debt. The statute lists violations including collecting unauthorized amounts, mishandling or abusing postdated payment instruments, causing communication charges by concealing the communication’s purpose, taking or threatening certain improper nonjudicial property actions, communicating by postcard, and using prohibited language or symbols on envelopes.'
  - gemini-2.5-pro: grounded=True, error=None, summary='Unfair or unconscionable debt collection practices include attempting to collect any amount, such as interest or fees, not expressly authorized by the agreement or permitted by law. The statute also forbids specific actions related to postdated checks, such as depositing one early or soliciting one to threaten prosecution. Other prohibited conduct includes taking nonjudicial action to dispossess property without a right to do so, communicating about a debt by postcard, or using revealing language or symbols on an envelope.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] ADVERSARIAL-GAP -- run run_20260830T103213Z, 2026-08-30T10:35:50Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': 'A collector\'s letter tells the consumer, "Your refusal to pay this bill constitutes theft of services and check fraud," and adds that once the account is sold to a purchaser next month the consumer "will lose any right to dispute or assert defenses." The consumer sues under §1692e.', 'exposes_gap': True, 'gap_description': 'The catalog omits §1692e(6) (falsely representing that a sale/transfer of the debt will cause the consumer to lose a claim or defense, or become subject to prohibited practices) and §1692e(7) (falsely representing that the consumer committed a crime or other conduct to disgrace the consumer). The list jumps from (5) to (8), so a pattern squarely within the statute has no matching item; only the residual (10) catch-all could be strained to reach it, and the completeness checklist never asks about accusations of criminality or representations about the effect of transferring the debt.'}, {'scenario': 'A collection law firm files a state-court complaint against the consumer to collect the debt. The complaint and the summons contain no statement that the sender is a debt collector, and no prior letter had been sent; the consumer claims a §1692e(11) mini-Miranda violation.', 'exposes_gap': True, 'gap_description': 'The checklist treats the mini-Miranda disclosure as dispositive in the initial and every subsequent communication, but §1692e(11) expressly exempts "a formal pleading made in connection with a legal action," and Reg F §1006.18(e)(3) carries forward that exclusion. No checklist item captures the communication\'s form or litigation context (pleading vs. dunning letter), so the encoded rule would generate a false positive. Relatedly, the checklist never asks who received the communication (consumer vs. court, employer, or credit bureau), which also matters for which subsections apply.'}, {'scenario': 'A dunning letter correctly states the balance and creditor but misidentifies the original creditor\'s corporate suffix ("ABC Bank, N.A." instead of "ABC Bank, FSB") and overstates accrued interest by $0.03. The consumer concedes she understood exactly who was collecting and what she owed, but sues under §1692e(2)(A) and (10).', 'exposes_gap': True, 'gap_description': 'The catalog\'s "any single item, if the facts match, is an independent violation" framing has no materiality filter and no articulation of the objective standard (least sophisticated / unsophisticated consumer) that most circuits apply to §1692e. The checklist asks only for exact wording, not whether the falsehood was material or capable of influencing a consumer\'s decision, so literal but trivial inaccuracies would be scored as violations. The checklist also omits the §1692k(c) bona fide error defense and threshold coverage facts (whether the actor is a \'debt collector\' and the obligation a \'consumer debt\').'}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means to collect a debt, and then lists specific violations: falsely implying government affiliation or bonding; misstating the character, amount, or legal status of a debt or the services/compensation involved; posing as an attorney or sending communications falsely appearing to be from one; threatening arrest, imprisonment, or seizure/garnishment/attachment/sale of property or wages when such action is unlawful or not intended; threatening any action that cannot legally be taken or is not intended; communicating credit information known to be false, including failing to note that a debt is disputed; simulating court or agency documents; using false representations or deceptive means to collect or to obtain consumer information; failing to give the 'mini-Miranda' disclosures; falsely claiming accounts were sold to innocent purchasers; falsely representing that documents are (or are not) legal process; using a name other than the collector's true name; and falsely implying the collector operates or is employed by a consumer reporting agency. Under Regulation F, the disclosure duty of § 1692e(11) now operates through 12 C.F.R. § 1006.18(e): the collector must state in the initial communication that it is attempting to collect a debt and that information obtained will be used for that purpose (repeating it in the initial written communication if the first contact was oral), and must disclose in each subsequent communication that it is from a debt collector. These disclosures are not required in a formal pleading made in connection with a legal action."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use false, deceptive, or misleading representations or means in collecting a debt. The prohibited conduct includes, among other things, falsely claiming government affiliation, misstating a debt’s character, amount, or legal status, falsely implying an attorney is involved, threatening unlawful or unintended action, communicating false credit information, using fake court or official documents, using a name other than the true name, and falsely implying documents are or are not legal process. The text also requires debt collectors to disclose in initial communications that they are attempting to collect a debt and that information obtained will be used for that purpose, and in later communications that the communication is from a debt collector, with an exception for formal pleadings in legal actions.'
  - gemini-2.5-pro: grounded=True, error=None, summary='Debt collectors may not use any false, deceptive, or misleading representations to collect a debt. Prohibited conduct includes misrepresenting the amount or legal status of a debt, falsely implying affiliation with the government, or pretending to be an attorney. Collectors also may not threaten actions they cannot legally take or do not intend to take, and they must disclose in initial communications that they are attempting to collect a debt and in subsequent communications that the message is from a debt collector.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] ADVERSARIAL-GAP -- run run_20260830T103213Z, 2026-08-30T10:34:42Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': "A collector places 10 calls in five days about one debt; three ring with no answer because the consumer's number was out of service, and two are answered by an automated carrier message rather than the subscriber. The consumer sues, pointing to the call log showing 10 attempts.", 'exposes_gap': True, 'gap_description': "The logic excludes 'calls not connected to the dialed number,' but the completeness checklist asks only for 'dates/times of all calls' and never asks whether each call actually connected, went to voicemail, or was a limited-content message. Without per-call connection status, the dispositive facts collected are insufficient to compute the count the rule requires, and no fact element distinguishes a connected voicemail (counts) from an unconnected attempt (does not)."}, {'scenario': 'The consumer telephones the collector on Monday to discuss the debt and, during that conversation, asks the collector to call her back Wednesday after she speaks with her spouse. The collector calls Wednesday, well inside the 7-day post-conversation window, and again Friday when she asks for a payoff figure by phone.', 'exposes_gap': True, 'gap_description': "The node's cooldown fires on any 'telephone conversation about that debt' and the checklist only asks whether conversations occurred and when. It captures neither (a) who initiated the call/conversation nor (b) whether the consumer requested the subsequent contact — the regulatory exclusion for calls placed in response to a request from the person is not encoded, so a consumer-requested callback would be flagged presumptively unlawful."}, {'scenario': 'One hospital stay generates a single balance that the creditor splits into four line-item accounts (facility, radiology, lab, anesthesia) and places with a single collection agency, which also uses two affiliated calling vendors; each account receives 6 calls in one week from each vendor, for 48 total calls to the consumer.', 'exposes_gap': True, 'gap_description': "The checklist asks only 'one debt or multiple debts,' treating that as a clean binary, and asks only about calls 'from this collector.' It supplies no facts for determining what constitutes a 'particular debt' where a creditor subdivides a single obligation, and no facts about affiliated entities, vendors, or successor collectors calling on the same debt — so per-debt and per-collector aggregation questions that drive the count are unresolvable on the collected facts."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the harassment prohibition in § 1006.14(b)(1) and FDCPA § 806(5) if it places no more than seven telephone calls within seven consecutive days to a particular person about a particular debt, and places no call within seven consecutive days after actually having a telephone conversation with that person about that debt (the conversation date counts as day one). Exceeding either of those frequencies flips the presumption: under § 1006.14(b)(2)(ii), the collector is presumed to violate § 1006.14(b)(1) and FDCPA § 806(5). Both presumptions are subject to the call-type exclusions in paragraph (b)(3). Because the limits are applied per 'particular debt,' § 1006.14(b)(4) clarifies that each debt in collection is counted separately, except that student loan debts serviced under a single account number when obtained by the collector are treated as one particular debt."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is presumed to comply if, for a particular person and a particular debt, it does not place more than seven calls within seven consecutive days and does not call within seven consecutive days after having a telephone conversation with that person about that debt. The date of the telephone conversation counts as the first day of that seven-day period. A debt collector is presumed to violate the rule if it exceeds either of those call-frequency limits. For this rule, a “particular debt” means each debt in collection, except that student loan debts serviced under a single account number when obtained by the debt collector are treated together as one particular debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to violate the law if they call a person about a particular debt more than seven times within a seven-consecutive-day period. A violation is also presumed if the debt collector calls a person within seven consecutive days after having a telephone conversation with them about that debt. This rule applies to each of a consumer's debts individually, unless they are student loan debts that were serviced under a single account number."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY] MODEL-DISAGREEMENT -- run run_20260830T094127Z, 2026-08-30T09:58:17Z

**File:** `rules/debt/state/texas/tx_debt_band3_discretionary_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: All three state the same three-part Craddock test (no intentional/consciously indifferent failure to answer, meritorious defense set up, and no delay or injury to plaintiff). However, Analyses 1 and 2 also state the procedural deadlines (motion for new trial filed within 30 days of judgment; overruled by operation of law if no signed order within 75 days), which Analysis 3 omits entirely. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['1', '2', '3', '30', '75'], OpenAI=['30', '75'], Gemini=['3'] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Craddock, a default judgment should be set aside and a new trial ordered whenever three things concur: (1) the defendant's failure to answer before judgment was not intentional or the result of conscious indifference, but was due to mistake or accident; (2) the motion for new trial sets up a meritorious defense; and (3) the motion is filed at a time when granting it will cause no delay or other injury to the plaintiff. Notably, the text phrases this as a standard the court 'should' apply 'in any case' where the elements are met, so it operates as a structured test rather than an open-ended discretionary weighing. Timing matters: the motion must be filed before or within thirty days after the judgment is signed (Rule 329b(a)), and if no written order is signed within seventy-five days of the judgment, the motion is overruled by operation of law (Rule 329b(c))."
  - gpt-5.5: grounded=True, error=None, summary='Under the provided text, a Texas default judgment should be set aside and a new trial ordered if the defendant’s failure to answer was not intentional or due to conscious indifference, but was caused by mistake or accident. The motion must set up a meritorious defense and be filed when granting it will not delay or injure the plaintiff; a motion for new trial must be filed within 30 days after judgment, and if not decided by signed written order within 75 days, it is overruled by operation of law.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A default judgment should be set aside and a new trial ordered when three conditions are met. First, the defendant's failure to answer was not intentional or the result of conscious indifference, but was due to a mistake or accident. Second, the motion for a new trial must set up a meritorious defense. Finally, the motion must be filed at a time when granting it will not cause delay or otherwise harm the plaintiff."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-VEHICLE-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260830T094127Z, 2026-08-30T09:55:20Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: All three agree on the core rule: a $7,500 California motor-vehicle exemption covering aggregate equity, execution-sale proceeds, and insurance/indemnification proceeds, with the $7,500 in sale proceeds automatically exempt (no claim required) when the debtor owns only one vehicle. Analysis 3 differs by omitting the substantive limitation stated in Analyses 1 and 2 that the subdivision (a) exemption is not also available in that single-vehicle execution-sale situation; Analysis 1 additionally notes the levying officer may rely on DMV records, a minor procedural detail. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['$7500', '1'], OpenAI=['$7500', '1'], Gemini=['$7500', '1', '105', '7'] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.010(a), a judgment debtor may exempt up to $7,500 in any combination of the aggregate equity in motor vehicles, the proceeds of an execution sale of a motor vehicle, and proceeds of insurance or other indemnification for a vehicle's loss, damage, or destruction. Subdivision (d) provides that if the debtor owns only one motor vehicle and it is sold at an execution sale, $7,500 of the sale proceeds is automatically exempt without the debtor having to make a claim, and the levying officer may consult and rely on Department of Motor Vehicles records to determine whether the debtor has only one vehicle. In that situation, the subdivision (a) exemption is not also available."
  - gpt-5.5: grounded=True, error=None, summary='California exempts up to $7,500 in any combination of aggregate equity in motor vehicles, proceeds from an execution sale of a motor vehicle, and insurance or indemnification proceeds for loss, damage, or destruction of a motor vehicle. If the judgment debtor has only one motor vehicle and it is sold at an execution sale, $7,500 of the sale proceeds is exempt without making a claim, and the subdivision (a) exemption is not also available in that situation.'
  - gemini-2.5-pro: grounded=True, error=None, summary='Under California law, a debtor is entitled to an exemption of seven thousand five hundred dollars ($7,500) for motor vehicles. This exemption can apply to the aggregate equity in the vehicle(s), the proceeds from an execution sale of a vehicle, or insurance proceeds for a lost or damaged vehicle. If a debtor has only one motor vehicle sold at an execution sale, the $7,500 exemption for the proceeds is automatic and does not require a claim.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-WRITTEN-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260830T094127Z, 2026-08-30T09:49:19Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: All three agree on the core rule: a four-year limitations period under CCP § 337 for actions on a written contract, obligation, or liability, and a bar on suits, arbitration, or other proceedings to collect after that period. However, Analysis 1 alone adds substantive qualifications — the § 336a exception and the special three-month deadline for deficiency-type money judgments after a trustee's/power-of-sale sale — and Analysis 3 alone omits the § 360 extension mentioned by Analyses 1 and 2. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['3', '4'], OpenAI=['4'], Gemini=['4'] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 337(a), an action on any contract, obligation, or liability founded on a written instrument must be brought within four years (subject to the exception in Section 336a, and a special three-month limit for deficiency-type money judgments after a trustee's/mortgage power-of-sale sale). Section 337(d) adds that once that four-year period has run, a person may not bring suit or initiate arbitration or any other legal proceeding to collect the debt. The limitations period can be extended only as provided in Section 360."
  - gpt-5.5: grounded=True, error=None, summary='An action on a contract, obligation, or liability founded on a written instrument must be brought within four years. Once that period has run, a person may not bring a lawsuit, arbitration, or other legal proceeding to collect the debt, and the period may be extended only under Section 360.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In California, the statute of limitations for an action on a written contract is four years. This time limit applies to any lawsuit on a "contract, obligation or liability founded upon an instrument in writing." Once this period has run, a person is prohibited from bringing a suit or other legal proceeding to collect the debt.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] MODEL-DISAGREEMENT -- run run_20260830T094127Z, 2026-08-30T09:48:16Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['30', '5'], OpenAI=['30', '5'], Gemini=['30', '5'] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 15 U.S.C. § 1692g(a) and 12 C.F.R. § 1006.34(a)(1), a notice is compliant only if the debt collector conveyed the required validation information — the amount of the debt, the creditor's name, the assumption-of-validity statement, the written-dispute/verification statement, and the original-creditor-request statement, plus the fuller itemization, consumer-protection, and response information listed in § 1006.34(c) — either in the initial communication or in a writing sent within five days of it. The dispute window runs 30 days from the consumer's receipt (or assumed receipt) of that information; under § 1006.34(b)(5) the collector may assume receipt on any date at least five business days (excluding Saturdays, Sundays, and legal public holidays) after it provides the notice. So the consumer is still within the window if fewer than 30 days have passed since actual or assumed receipt, and a timely written dispute or original-creditor request triggers the § 1692g(b) duty to cease collection until verification is mailed. The supplied text gives the compliance and timing test but contains no facts about the particular notice or dates, so the actual answer turns on applying these elements to the notice's contents and delivery/receipt dates."
  - gpt-5.5: grounded=False, error=None, summary='A compliant validation notice must provide the required validation information in the initial communication, within five days after the initial communication, or orally in the initial communication under the regulation; the statutory notice includes the debt amount, creditor name, and required statements about disputing the debt, verification, and original-creditor information. The dispute/validation period starts when the validation information is provided and ends 30 days after the consumer receives or is assumed to receive it; receipt may be assumed at least five business days after it is provided. The provided text does not include the actual notice contents, the date of initial communication, the date validation information was provided, or the date of receipt, so it is not possible to determine whether a compliant notice was actually provided or whether the consumer is still within the dispute window.'
  - gemini-2.5-pro: grounded=False, error=None, summary='The provided texts lay out the legal rules for what a compliant debt validation notice must contain and when it must be sent. Specifically, a debt collector must provide a notice with certain disclosures within five days of the initial communication. The texts also establish that a consumer has a 30-day period after receiving the notice to dispute the debt. However, the provided text contains no facts about a specific notice, so it is impossible to determine whether a compliant notice was actually provided or if a consumer is still within their dispute window.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] MODEL-DISAGREEMENT -- run run_20260830T094127Z, 2026-08-30T09:47:20Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['1', '10', '2', '3', '4', '5', '6', '7', '8'], OpenAI=[], Gemini=[] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692f imposes a general ban on debt collectors using unfair or unconscionable means to collect a debt, and then lists specific violations without limiting that general rule. The enumerated practices are: (1) collecting amounts (including interest, fees, charges, or incidental expenses) not expressly authorized by the debt agreement or permitted by law; (2) accepting a check or payment instrument postdated more than five days without written notice of intent to deposit given 3-10 business days beforehand; (3) soliciting postdated instruments to threaten or institute criminal prosecution; (4) depositing or threatening to deposit a postdated instrument early; (5) causing a person to be charged for communications by concealing the communication's true purpose; (6) taking or threatening nonjudicial dispossession or disablement of property where there is no present right to possession under an enforceable security interest, no present intention to take possession, or the property is legally exempt; (7) communicating with a consumer about a debt by post card; and (8) using any language or symbol other than the collector's address on mail/telegram envelopes, though a business name may be used if it does not indicate the debt collection business."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect or attempt to collect a debt. The statute lists violations including collecting unauthorized amounts; mishandling postdated checks; causing communication charges by concealing the communication’s purpose; improper nonjudicial repossession or disablement actions; communicating by postcard; and using improper language or symbols on envelopes.'
  - gemini-2.5-pro: grounded=None, error=Gemini API timed out after 60s, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] MODEL-DISAGREEMENT -- run run_20260830T094127Z, 2026-08-30T09:45:21Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: All three agree on the core rule of § 1692e — a blanket ban on false, deceptive, or misleading representations, illustrated by a non-exhaustive list (government affiliation, character/amount/legal status of the debt, attorney implications, unlawful or unintended threats, false credit information, simulated legal process, false names, CRA affiliation) — and on the § 1692e(11) disclosure duties for initial and subsequent communications. Analyses 1 and 2 both state the express exception for formal pleadings made in connection with a legal action, which Analysis 3 omits entirely; Analysis 1 alone adds the Regulation F citation (12 C.F.R. § 1006.18(e)) and the requirement to repeat the disclosure in the initial written communication when the first contact was oral. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=[], OpenAI=[], Gemini=[] (fingerprint_agreement=True).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means to collect a debt, and then lists specific violations without limiting that general ban: falsely claiming government affiliation or bonding; misrepresenting the character, amount, or legal status of a debt or services/compensation; posing as an attorney or sending attorney-sourced communications; threatening arrest, imprisonment, seizure, garnishment, attachment, or sale of property or wages that is unlawful or not actually intended; threatening any action that cannot legally be taken or is not intended; communicating credit information known to be false, including failing to report that a debt is disputed; using documents simulating court or agency process; using false representations or deceptive means to collect or to obtain consumer information; failing to give the required debt-collector disclosures; falsely implying accounts were sold to innocent purchasers for value; falsely calling documents legal process (or denying that they are); using a name other than the collector's true name; and falsely implying the collector is or works for a consumer reporting agency. On the disclosure point, Regulation F at 12 C.F.R. § 1006.18(e) implements § 1692e(11): the collector must state in the initial communication that it is attempting to collect a debt and that information obtained will be used for that purpose, repeat that disclosure in the initial written communication if the first contact was oral, and disclose in every later communication that it is from a debt collector. The only stated exception is that these disclosures are not required in a formal pleading made in connection with a legal action."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use any false, deceptive, or misleading representation or means in connection with collecting a debt. The text lists violations including falsely claiming government affiliation, misrepresenting the debt’s character, amount, or legal status, implying an attorney involvement, threatening unlawful or unintended action, communicating false credit information, using documents that falsely appear official or legal, using a false business name, and falsely implying affiliation with a consumer reporting agency. Debt collectors also must give the required disclosure that they are attempting to collect a debt and that information obtained will be used for that purpose in initial communications, and must identify subsequent communications as from a debt collector, with an exception for formal pleadings in legal actions.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector is broadly prohibited from using any false, deceptive, or misleading representations to collect a debt. Prohibited conduct includes, but is not limited to, misrepresenting the amount or legal status of the debt, falsely implying an affiliation with the government, or threatening to take any action that cannot legally be taken or is not intended to be taken. Collectors must also disclose in their initial communication that they are attempting to collect a debt and must identify themselves as a debt collector in subsequent communications.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-EXEMPT-PERSONAL-PROPERTY] MODEL-DISAGREEMENT -- run run_20260829T180029Z, 2026-08-29T18:19:41Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: All three agree on the core rule: personal property listed in Tex. Prop. Code § 42.002 is exempt up to an aggregate fair market value of $100,000 for a family or $50,000 for a single adult (excluding encumbrances), with wages, prescribed health aids, and support payments exempt without counting toward the cap. However, Analysis 1 states substantive sub-rules the others omit entirely — the 25%-of-aggregate cap on jewelry, the child-support exception to the current-wages exemption, and the landlord-seizure exception to the sacred-text exemption; Analysis 3 also omits the sacred-book exemption altogether. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['$100000', '$50000', '1', '2', '25%'], OpenAI=['$100000', '$50000'], Gemini=['$100000', '$50000'] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under Tex. Prop. Code § 42.001(a), the personal property listed in § 42.002 is exempt from garnishment, attachment, execution, or other seizure up to an aggregate fair market value of $100,000 for property provided for a family, or $50,000 for a single adult who is not a family member, in each case excluding liens, security interests, or other encumbrances. Section 42.002(a) lists the qualifying items, including home furnishings and heirlooms, provisions for consumption, farm/ranch vehicles and implements, tools and books of a trade, clothing, jewelry (capped at 25% of the aggregate limit), two firearms, athletic equipment, one motor vehicle per licensed family member (or non-licensed person who relies on a driver), specified animals and forage, and household pets. Separately, § 42.001(b) exempts certain property without counting it toward those dollar caps: current wages for personal services (except for court-ordered child support enforcement), professionally prescribed health aids, alimony/support/separate maintenance, and a bible or other sacred text (except when seized by a landlord exercising seizure rights after a lease breach or abandonment).'
  - gpt-5.5: grounded=True, error=None, summary='Texas exempts the personal property listed in Section 42.002 from garnishment, attachment, execution, or other seizure up to an aggregate fair market value of $100,000 for property provided for a family, or $50,000 for property owned by a single adult who is not a member of a family, excluding liens and similar encumbrances. Certain items—such as current wages, prescribed health aids, support payments, and certain sacred religious books—are exempt from seizure and do not count toward those aggregate limits.'
  - gemini-2.5-pro: grounded=True, error=None, summary='Texas law exempts personal property from creditor seizure up to an aggregate fair market value of $100,000 for a family or $50,000 for a single adult. This value cap applies to a specific list of property types, including home furnishings, vehicles, tools of the trade, certain animals, and jewelry. Other specific property, such as current wages, professionally prescribed health aids, and alimony, is also exempt from seizure and does not count toward these aggregate value limitations.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY] MODEL-DISAGREEMENT -- run run_20260829T180029Z, 2026-08-29T18:16:04Z

**File:** `rules/debt/state/texas/tx_debt_band3_discretionary_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: All three state the identical three-prong Craddock test (no intentional/consciously indifferent failure to answer, meritorious defense set up, and no delay or injury to plaintiff). However, Analyses 1 and 2 additionally state the procedural deadlines under Rule 329b — filing within 30 days of judgment and overruling by operation of law if not ruled on within 75 days — which Analysis 3 omits entirely. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['1', '2', '3', '30', '75'], OpenAI=['3', '30', '75'], Gemini=['3'] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Craddock, a Texas default judgment should be set aside and a new trial granted when three conditions are met: (1) the defendant's failure to answer before judgment was not intentional or the result of conscious indifference, but was due to mistake or accident; (2) the motion for new trial sets up a meritorious defense; and (3) the motion is filed at a time when granting it will cause no delay or other injury to the plaintiff. Procedurally, the motion must be filed before or within thirty days after the judgment is signed (Rule 329b(a)), and if it is not ruled on by written order within seventy-five days after the judgment was signed, it is overruled by operation of law (Rule 329b(c)). Because the outcome turns on the court's assessment of the defendant's state of mind, the asserted defense, and prejudice to the plaintiff, the determination is a fact-bound, multi-factor one rather than a purely mechanical rule."
  - gpt-5.5: grounded=True, error=None, summary='Under the quoted rule from Craddock, a Texas default judgment should be set aside and a new trial ordered when three conditions are met: the failure to answer was not intentional or due to conscious indifference but resulted from mistake or accident; the motion sets up a meritorious defense; and granting the motion will not delay or otherwise injure the plaintiff. The motion for new trial must be filed before or within 30 days after the judgment is signed, and if it is not determined by written order within 75 days after judgment, it is overruled by operation of law.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A Texas default judgment should be set aside through a motion for new trial if three conditions are met. First, the defendant's failure to answer was not intentional or the result of conscious indifference, but was due to a mistake or accident. Second, the motion must set up a meritorious defense. Third, the motion must be filed at a time when granting it will not cause delay or otherwise harm the plaintiff."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-CIVIL-ANSWER-DEADLINE] MODEL-DISAGREEMENT -- run run_20260829T180029Z, 2026-08-29T18:14:49Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['30', '4', '6'], OpenAI=['30'], Gemini=[] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under Cal. Code Civ. Proc. § 412.20(a)(3), the summons must direct the defendant to file a written pleading in response to the complaint within 30 days after the summons is served, and subdivision (a)(6) repeats this in the notice warning that the court may decide against the defendant without a hearing unless they respond within 30 days. If the defendant does not respond, subdivision (a)(4) provides that the plaintiff may apply for entry of default and for the relief demanded, which could include garnishment of wages or the taking of money or property. The text states this deadline for complaints generally and does not carve out any different rule for debt-collection suits.'
  - gpt-5.5: grounded=True, error=None, summary='The summons must direct the defendant to file a written pleading responding to the complaint within 30 days after the summons is served. It also warns that if the defendant does not respond within 30 days, the court may decide against them and their default may be entered, allowing the plaintiff to seek the relief demanded in the complaint.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-HOMESTEAD-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260829T180029Z, 2026-08-29T18:11:35Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['$25', '$300000', '$600000', '1', '2', '2022', '31'], OpenAI=['$25', '$300000', '$600000', '1', '2', '2022'], Gemini=[] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.730(a), a judgment debtor's homestead exemption equals the greater of (1) the countywide median sale price for a single-family home in the calendar year before the year the exemption is claimed, capped at $600,000, or (2) $300,000. So the floor is $300,000 and the ceiling is $600,000, with the actual figure depending on the county's prior-year median home price. Subdivision (b) provides that these dollar amounts adjust annually for inflation starting January 1, 2022, using the change in the annual California Consumer Price Index for All Urban Consumers (published by the Department of Industrial Relations) for the most recent one-year period ending December 31 before the adjustment, rounded to the nearest $25. The excerpt states only the exemption amounts and their indexing; it does not set out the procedures governing a creditor's forced sale."
  - gpt-5.5: grounded=True, error=None, summary='The California homestead exemption amount is the greater of: (1) the countywide median sale price for a single-family home in the prior calendar year, capped at $600,000; or (2) $300,000. These amounts are adjusted annually for inflation beginning January 1, 2022, using the California CPI for All Urban Consumers and rounded to the nearest $25.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-WRITTEN-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260829T180029Z, 2026-08-29T18:08:35Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['3', '4'], OpenAI=['4'], Gemini=[] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 337(a), an action upon any contract, obligation, or liability founded upon a written instrument must be brought within four years (subject to the exception in Section 336a, and a special three-month limit for deficiency-type money judgments after a trustee's sale under a deed of trust or mortgage with power of sale). Section 337(d) adds that once that four-year period has run, a person may not bring suit or initiate arbitration or other legal proceedings to collect the debt. The limitations period may be extended only pursuant to Section 360."
  - gpt-5.5: grounded=True, error=None, summary='An action on a contract, obligation, or liability founded on a written instrument must be brought within four years. Once that period has run, a person may not bring suit, initiate arbitration, or start another legal proceeding to collect the debt, and the period can be extended only under Section 360.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] CITATION-CHECK-FAILED -- run run_20260829T180029Z, 2026-08-29T18:07:11Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 5 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 104703, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0, 'retry_attempt': 2, 'longest_matching_prefix_chars': 112, 'text_at_break_point': ': (1) de', 'raw_html_context_at_break': 'lidation information required</em> —</p>\n<div id="p-1006.34(a)(1)">\n<p class="indent-2" data-title="1006.34(a)(1)"><span class="paragraph-hierarchy"><span class="paren">(</span>1<span class="paren">)</span></span> <em class="paragraph-heading">In gen'}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="A notice is compliant only if, in the initial communication or within five days after it, the collector provided the required validation information — the amount of the debt, the name of the creditor, the statement that the debt is assumed valid unless disputed within 30 days of receipt, the written-dispute/verification statement, and the original-creditor-request statement (15 U.S.C. § 1692g(a)); Regulation F adds further required content, including the collector communication disclosure, itemization details, the dispute-window end date, and consumer-response information (12 C.F.R. § 1006.34(a)(1), (c)). If any of these items is missing or was not delivered in the required time frame, the notice is not compliant. The dispute window runs from the date the validation information is provided until 30 days after the consumer receives (or is assumed to receive) it, and the collector may assume receipt on any date at least five business days — excluding Saturdays, Sundays, and legal public holidays — after providing it (12 C.F.R. § 1006.34(b)(5)); so the consumer is still within the window if that 30-day period has not yet run. If the consumer disputes in writing within that period, the collector must cease collection of the disputed portion until it mails verification or the original creditor's name and address (15 U.S.C. § 1692g(b)). The text supplies the standard but no facts about the particular notice or dates, so the actual compliance and timeliness conclusions depend on applying these rules to the specific mailing and dispute dates."
  - gpt-5.5: grounded=False, error=None, summary='The cited provisions state that a debt collector must provide required validation information in the initial communication or within five days afterward, and the notice must include specified debt, creditor, dispute-right, verification, and original-creditor information. The dispute/validation period runs until 30 days after the consumer receives or is assumed to receive the validation information, with receipt assumable at least five business days after it is provided. The excerpt does not provide facts about what notice was actually sent, when it was sent or received, or today’s date, so it is insufficient to determine whether a compliant notice was provided or whether the consumer is still within the dispute window.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A compliant debt validation notice must be provided either orally in the initial communication or in writing within five days of it. The notice must contain specific information, including the debt amount, creditor name, and statements about the consumer\'s rights. The consumer is within the dispute window if they are within the "validation period," which ends 30 days after the consumer receives or is assumed to have received the validation information.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] MODEL-DISAGREEMENT -- run run_20260829T180029Z, 2026-08-29T18:07:11Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['30', '5'], OpenAI=['30', '5'], Gemini=['30', '5'] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="A notice is compliant only if, in the initial communication or within five days after it, the collector provided the required validation information — the amount of the debt, the name of the creditor, the statement that the debt is assumed valid unless disputed within 30 days of receipt, the written-dispute/verification statement, and the original-creditor-request statement (15 U.S.C. § 1692g(a)); Regulation F adds further required content, including the collector communication disclosure, itemization details, the dispute-window end date, and consumer-response information (12 C.F.R. § 1006.34(a)(1), (c)). If any of these items is missing or was not delivered in the required time frame, the notice is not compliant. The dispute window runs from the date the validation information is provided until 30 days after the consumer receives (or is assumed to receive) it, and the collector may assume receipt on any date at least five business days — excluding Saturdays, Sundays, and legal public holidays — after providing it (12 C.F.R. § 1006.34(b)(5)); so the consumer is still within the window if that 30-day period has not yet run. If the consumer disputes in writing within that period, the collector must cease collection of the disputed portion until it mails verification or the original creditor's name and address (15 U.S.C. § 1692g(b)). The text supplies the standard but no facts about the particular notice or dates, so the actual compliance and timeliness conclusions depend on applying these rules to the specific mailing and dispute dates."
  - gpt-5.5: grounded=False, error=None, summary='The cited provisions state that a debt collector must provide required validation information in the initial communication or within five days afterward, and the notice must include specified debt, creditor, dispute-right, verification, and original-creditor information. The dispute/validation period runs until 30 days after the consumer receives or is assumed to receive the validation information, with receipt assumable at least five business days after it is provided. The excerpt does not provide facts about what notice was actually sent, when it was sent or received, or today’s date, so it is insufficient to determine whether a compliant notice was provided or whether the consumer is still within the dispute window.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A compliant debt validation notice must be provided either orally in the initial communication or in writing within five days of it. The notice must contain specific information, including the debt amount, creditor name, and statements about the consumer\'s rights. The consumer is within the dispute window if they are within the "validation period," which ends 30 days after the consumer receives or is assumed to have received the validation information.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] CITATION-CHECK-FAILED -- run run_20260829T180029Z, 2026-08-29T18:05:58Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692f', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 35834, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0, 'retry_attempt': 2, 'longest_matching_prefix_chars': 101, 'text_at_break_point': '. without limiting ', 'raw_html_context_at_break': None}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692f imposes a general prohibition: a debt collector may not use unfair or unconscionable means to collect or attempt to collect any debt. The statute then lists non-exhaustive examples of violations, including collecting any amount (interest, fees, charges, expenses) not expressly authorized by the debt agreement or permitted by law; accepting a check postdated more than five days without written notice of intent to deposit sent 3–10 business days beforehand; soliciting postdated instruments to threaten or institute criminal prosecution; depositing or threatening to deposit a postdated instrument early; causing a person to be charged for communications by concealing the communication's true purpose; and taking or threatening nonjudicial repossession or disablement of property where there is no present right to possession through an enforceable security interest, no present intention to take possession, or the property is exempt by law. It also bars communicating with a consumer about a debt by post card and using any language or symbol other than the collector's address on mail or telegram envelopes, except a business name that does not indicate the debt collection business."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect or attempt to collect a debt. The listed violations include collecting amounts not authorized by the debt agreement or law, improper handling or solicitation of postdated checks, causing communication charges by concealing the communication’s purpose, certain improper nonjudicial repossession or disablement actions, communicating by postcard, and using prohibited language or symbols on mailed envelopes or telegrams.'
  - gemini-2.5-pro: grounded=True, error=None, summary='The statute forbids debt collectors from using unfair or unconscionable methods to collect a debt. Prohibited actions include collecting amounts not authorized by the debt agreement or law, and improperly handling postdated checks, such as depositing them without proper notice or before their date. Other forbidden practices include repossessing property without a present right to do so, communicating about a debt via postcard, or using envelopes that reveal the debt-collection purpose of the communication.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] CITATION-CHECK-FAILED -- run run_20260829T180029Z, 2026-08-29T18:04:24Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.18', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 74851, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0, 'retry_attempt': 2, 'longest_matching_prefix_chars': 4, 'text_at_break_point': 'initial communications. a debt collector', 'raw_html_context_at_break': None}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means to collect a debt, then lists non-exhaustive examples: falsely implying government affiliation or bonding (1); misrepresenting the character, amount, or legal status of a debt or the services/compensation involved (2); falsely implying attorney status or attorney-sourced communications (3); threatening arrest, imprisonment, seizure, garnishment, attachment, or sale of property unless that action is lawful and actually intended (4); threatening any action that cannot legally or will not be taken (5); communicating credit information known to be false, including failing to note a debt is disputed (8); using documents that simulate court or agency papers (9) or falsely represent that documents are or are not legal process (13, 15); any false or deceptive means to collect or to obtain consumer information (10); failing to give the 'mini-Miranda' disclosures (11); falsely implying accounts went to innocent purchasers for value (12); using a business name other than the true name (14); and falsely implying the collector operates or is employed by a consumer reporting agency (16). Reg F now implements the §1692e(11) disclosure duty: the collector must state in the initial communication that it is attempting to collect a debt and that information obtained will be used for that purpose (repeating it in the first written communication if the initial contact was oral), must state in every later communication that the communication is from a debt collector, and need not make these disclosures in a formal pleading in a legal action."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use false, deceptive, or misleading representations or means in collecting a debt. The prohibited conduct includes, among other things, falsely implying government affiliation, misrepresenting a debt’s character/amount/legal status, falsely implying attorney involvement, threatening unlawful or unintended actions, communicating false credit information, using fake court or agency documents, using deceptive means to collect or get consumer information, failing to give required debt-collector disclosures, using a false business name, and falsely implying documents are or are not legal process. Initial and subsequent communications must include specified debt-collection disclosures, except for formal pleadings in legal actions.'
  - gemini-2.5-pro: grounded=None, error=Gemini API timed out after 60s, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] MODEL-DISAGREEMENT -- run run_20260829T180029Z, 2026-08-29T18:04:24Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['1', '10', '11', '12', '13', '14', '15', '16', '2', '3', '4', '5', '8', '9'], OpenAI=[], Gemini=[] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means to collect a debt, then lists non-exhaustive examples: falsely implying government affiliation or bonding (1); misrepresenting the character, amount, or legal status of a debt or the services/compensation involved (2); falsely implying attorney status or attorney-sourced communications (3); threatening arrest, imprisonment, seizure, garnishment, attachment, or sale of property unless that action is lawful and actually intended (4); threatening any action that cannot legally or will not be taken (5); communicating credit information known to be false, including failing to note a debt is disputed (8); using documents that simulate court or agency papers (9) or falsely represent that documents are or are not legal process (13, 15); any false or deceptive means to collect or to obtain consumer information (10); failing to give the 'mini-Miranda' disclosures (11); falsely implying accounts went to innocent purchasers for value (12); using a business name other than the true name (14); and falsely implying the collector operates or is employed by a consumer reporting agency (16). Reg F now implements the §1692e(11) disclosure duty: the collector must state in the initial communication that it is attempting to collect a debt and that information obtained will be used for that purpose (repeating it in the first written communication if the initial contact was oral), must state in every later communication that the communication is from a debt collector, and need not make these disclosures in a formal pleading in a legal action."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use false, deceptive, or misleading representations or means in collecting a debt. The prohibited conduct includes, among other things, falsely implying government affiliation, misrepresenting a debt’s character/amount/legal status, falsely implying attorney involvement, threatening unlawful or unintended actions, communicating false credit information, using fake court or agency documents, using deceptive means to collect or get consumer information, failing to give required debt-collector disclosures, using a false business name, and falsely implying documents are or are not legal process. Initial and subsequent communications must include specified debt-collection disclosures, except for formal pleadings in legal actions.'
  - gemini-2.5-pro: grounded=None, error=Gemini API timed out after 60s, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] CITATION-CHECK-FAILED -- run run_20260829T180029Z, 2026-08-29T18:02:39Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 75544, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0, 'retry_attempt': 2, 'longest_matching_prefix_chars': 4, 'text_at_break_point': 'subject to the exclusions in paragraph (', 'raw_html_context_at_break': None}}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 75544, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0, 'retry_attempt': 2, 'longest_matching_prefix_chars': 34, 'text_at_break_point': ', particular debt means each of a consum', 'raw_html_context_at_break': None}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the harassment prohibition (and FDCPA § 806(5)) if it places no more than seven calls to a particular person about a particular debt within seven consecutive days, and places no call within the seven consecutive days following a telephone conversation with that person about that debt (the conversation date counts as day one). Under (b)(2)(ii), exceeding either of those frequencies creates a presumption that the collector violated the rule and FDCPA § 806(5). Both presumptions are subject to the call-type exclusions in paragraph (b)(3). Per (b)(4), the limits are applied per 'particular debt' — each debt in collection separately — except that student loan debts serviced under a single account number when obtained by the collector are treated as one particular debt."
  - gpt-5.5: grounded=True, error=None, summary='Subject to the stated exclusions, a debt collector is presumed to violate the rule if, for a particular person and a particular debt, it places calls more than seven times within seven consecutive days, or places a call within seven consecutive days after having had a telephone conversation with that person about that debt. The date of the telephone conversation counts as the first day of the seven-day period. A “particular debt” means each debt in collection, except that certain student loan debts serviced under a single account number are treated together as one particular debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector is presumed to have engaged in unlawful conduct if, in connection with a particular debt, they call a person more than seven times within seven consecutive days. A presumption of a violation also arises if the debt collector calls a person within seven consecutive days after having had a telephone conversation with them about that debt.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] MODEL-DISAGREEMENT -- run run_20260829T180029Z, 2026-08-29T18:02:39Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: All three state the same core thresholds: a presumed violation when a debt collector places more than seven calls to a person about a particular debt in seven consecutive days, or any call within seven consecutive days after a telephone conversation about that debt. However, Analysis 3 omits substantive elements the others include — that the conversation date counts as day one and that 'particular debt' means each debt separately with an exception treating student loans serviced under a single account number as one debt. Analysis 1 alone also states the converse safe-harbor compliance presumption under § 1006.14(b)(2)(i). (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['1', '2', '3', '4', '7'], OpenAI=['1', '7'], Gemini=['7'] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the harassment prohibition (and FDCPA § 806(5)) if it places no more than seven calls to a particular person about a particular debt within seven consecutive days, and places no call within the seven consecutive days following a telephone conversation with that person about that debt (the conversation date counts as day one). Under (b)(2)(ii), exceeding either of those frequencies creates a presumption that the collector violated the rule and FDCPA § 806(5). Both presumptions are subject to the call-type exclusions in paragraph (b)(3). Per (b)(4), the limits are applied per 'particular debt' — each debt in collection separately — except that student loan debts serviced under a single account number when obtained by the collector are treated as one particular debt."
  - gpt-5.5: grounded=True, error=None, summary='Subject to the stated exclusions, a debt collector is presumed to violate the rule if, for a particular person and a particular debt, it places calls more than seven times within seven consecutive days, or places a call within seven consecutive days after having had a telephone conversation with that person about that debt. The date of the telephone conversation counts as the first day of the seven-day period. A “particular debt” means each debt in collection, except that certain student loan debts serviced under a single account number are treated together as one particular debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector is presumed to have engaged in unlawful conduct if, in connection with a particular debt, they call a person more than seven times within seven consecutive days. A presumption of a violation also arises if the debt collector calls a person within seven consecutive days after having had a telephone conversation with them about that debt.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY] MODEL-DISAGREEMENT -- run run_20260829T173643Z, 2026-08-29T17:39:28Z

**File:** `rules/debt/state/texas/tx_debt_band3_discretionary_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['1', '2', '3', '30', '75'], OpenAI=['30', '75'], Gemini=[] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under Craddock, a Texas default judgment should be set aside and a new trial granted when the defendant shows three things: (1) the failure to answer before judgment was not intentional or the result of conscious indifference, but was due to mistake or accident; (2) the motion for new trial sets up a meritorious defense; and (3) the motion is filed at a time when granting it will cause no delay or other injury to the plaintiff. Procedurally, the motion must be filed before or within thirty days after the judgment is signed (Rule 329b(a)), and if the court does not sign a written order deciding it within seventy-five days of the judgment, it is overruled by operation of law (Rule 329b(c)). Because each element turns on the particular facts the movant presents, the outcome is a case-by-case judicial determination rather than an automatic result.'
  - gpt-5.5: grounded=True, error=None, summary='Under the provided text, a Texas default judgment should be set aside and a new trial ordered when the defendant’s failure to answer was not intentional or due to conscious indifference, but resulted from mistake or accident, so long as the motion sets up a meritorious defense and granting it will not delay or injure the plaintiff. A motion for new trial must be filed within thirty days after judgment, and if not ruled on by written order within seventy-five days after judgment, it is overruled by operation of law. The text frames the result as dependent on specified conditions, not as an unrestricted discretionary determination.'
  - gemini-2.5-pro: grounded=None, error=Gemini API timed out after 60s, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-SOL-CONSUMER-DEBT] CITATION-CHECK-FAILED -- run run_20260829T114209Z, 2026-08-29T11:45:10Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://statutes.capitol.texas.gov/Docs/CP/htm/CP.16.htm', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 250874, 'content_type': 'text/html', 'word_overlap_ratio': 0.053, 'retry_attempt': 2, 'longest_matching_prefix_chars': 1, 'text_at_break_point': ' person must bring suit on the following'}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Tex. Civ. Prac. & Rem. Code § 16.004(a)(3), a suit on a 'debt' must be filed no later than four years after the day the cause of action accrues. So a collection lawsuit on a consumer debt is subject to a four-year limitations period running from accrual. The provision sets the same four-year deadline for specific performance of real-property conveyance contracts, penal-clause bond claims, fraud, and breach of fiduciary duty, but it does not itself define when a debt claim accrues."
  - gpt-5.5: grounded=True, error=None, summary='A lawsuit for debt must be brought no later than four years after the day the cause of action accrues. The provided text does not separately define consumer debt, but it expressly covers actions for “debt.”'
  - gemini-2.5-pro: grounded=True, error=None, summary='Under the provided Texas statute, a lawsuit must be brought on a debt no later than four years after the day the cause of action accrues. The text explicitly lists "debt" as one of the actions subject to this four-year limitations period. This four-year timeframe would therefore apply to a lawsuit for debt collection.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY] CITATION-CHECK-FAILED -- run run_20260829T114209Z, 2026-08-29T11:44:18Z

**File:** `rules/debt/state/texas/tx_debt_band3_discretionary_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 3 cited source(s) could not be mechanically verified live: [{'url': 'https://www.courtlistener.com/opinion/4172687/craddock-v-sunshine-bus-lines-inc/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 202, 'content_length': 2006, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.176, 'retry_attempt': 2, 'longest_matching_prefix_chars': 2, 'text_at_break_point': 'default judgment should be set aside and'}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Craddock, a default judgment should be set aside and a new trial granted when three things are shown: (1) the defendant's failure to answer before judgment was not intentional or the result of conscious indifference, but was due to mistake or accident; (2) the motion for new trial sets up a meritorious defense; and (3) it is filed at a time when granting it will cause no delay or other injury to the plaintiff. The rules add hard timing constraints: the motion must be filed before or within thirty days after the judgment is signed, and if it is not decided by written order within seventy-five days after the judgment was signed, it is overruled by operation of law. So the outcome turns on a fact-bound, multi-factor weighing of the defendant's excuse, the strength of the defense, and prejudice to the plaintiff, but only if the deadlines are met."
  - gpt-5.5: grounded=True, error=None, summary='Under the quoted rule, a Texas default judgment should be set aside and a new trial ordered when the defendant’s failure to answer was not intentional or due to conscious indifference, but resulted from mistake or accident; the motion sets up a meritorious defense; and granting it will not delay or otherwise injure the plaintiff. The motion for new trial must be filed before or within 30 days after the judgment is signed, and if it is not determined by signed written order within 75 days after judgment, it is overruled by operation of law.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY] MODEL-DISAGREEMENT -- run run_20260829T114209Z, 2026-08-29T11:44:18Z

**File:** `rules/debt/state/texas/tx_debt_band3_discretionary_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['1', '2', '3', '30', '75'], OpenAI=['30', '75'], Gemini=[] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Craddock, a default judgment should be set aside and a new trial granted when three things are shown: (1) the defendant's failure to answer before judgment was not intentional or the result of conscious indifference, but was due to mistake or accident; (2) the motion for new trial sets up a meritorious defense; and (3) it is filed at a time when granting it will cause no delay or other injury to the plaintiff. The rules add hard timing constraints: the motion must be filed before or within thirty days after the judgment is signed, and if it is not decided by written order within seventy-five days after the judgment was signed, it is overruled by operation of law. So the outcome turns on a fact-bound, multi-factor weighing of the defendant's excuse, the strength of the defense, and prejudice to the plaintiff, but only if the deadlines are met."
  - gpt-5.5: grounded=True, error=None, summary='Under the quoted rule, a Texas default judgment should be set aside and a new trial ordered when the defendant’s failure to answer was not intentional or due to conscious indifference, but resulted from mistake or accident; the motion sets up a meritorious defense; and granting it will not delay or otherwise injure the plaintiff. The motion for new trial must be filed before or within 30 days after the judgment is signed, and if it is not determined by signed written order within 75 days after judgment, it is overruled by operation of law.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-JUSTICE-COURT-DEBT-ANSWER-DEADLINE] CITATION-CHECK-FAILED -- run run_20260828T220708Z, 2026-08-28T22:26:12Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://texaslawhelp.org/guide/how-to-answer-a-debt-collection-case-in-justice-court', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 120178, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.353, 'retry_attempt': 2, 'longest_matching_prefix_chars': 0, 'text_at_break_point': '[secondary-source corroboration, not ind'}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under the cited material, a defendant in a Texas justice court debt-collection suit must file an Answer within 14 days after the date of service. If that 14th day falls on a weekend or a court holiday, the deadline rolls to the next business day. The same source notes that Texas justice courts hear debt claims valued up to $20,000. Caveat: this deadline comes from a secondary legal-aid summary (TexasLawHelp.org) attributed to Tex. R. Civ. P. 502.5 rather than from the rule's own text, which was not reproduced here."
  - gpt-5.5: grounded=True, error=None, summary='In a Texas justice-court debt lawsuit, the answer is due 14 days after the date the defendant is served. If the 14th day falls on a weekend or court holiday, the answer is due the next business day.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In a Texas justice court debt lawsuit, the answer is due 14 days after the date the defendant is served. If that 14th day falls on a weekend or a court holiday, the deadline is extended to the following business day.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-EXEMPT-PERSONAL-PROPERTY] CITATION-CHECK-FAILED -- run run_20260828T220708Z, 2026-08-28T22:25:05Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 3 of 3 cited source(s) could not be mechanically verified live: [{'url': 'https://statutes.capitol.texas.gov/Docs/PR/htm/PR.42.htm', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 250874, 'content_type': 'text/html', 'word_overlap_ratio': 0.083, 'retry_attempt': 2, 'longest_matching_prefix_chars': 3, 'text_at_break_point': 'sonal property, as described in section '}}, {'url': 'https://statutes.capitol.texas.gov/Docs/PR/htm/PR.42.htm', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 250874, 'content_type': 'text/html', 'word_overlap_ratio': 0.214, 'retry_attempt': 2, 'longest_matching_prefix_chars': 2, 'text_at_break_point': 'e following personal property is exempt '}}, {'url': 'https://statutes.capitol.texas.gov/Docs/PR/htm/PR.42.htm', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 250874, 'content_type': 'text/html', 'word_overlap_ratio': 0.231, 'retry_attempt': 2, 'longest_matching_prefix_chars': 2, 'text_at_break_point': 'e following personal property is exempt '}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under Tex. Prop. Code § 42.001(a), the personal property listed in § 42.002 is shielded from garnishment, attachment, execution, or other seizure up to an aggregate fair market value of $100,000 for property provided for a family, or $50,000 for a single adult who is not part of a family, in each case excluding the amount of any liens, security interests, or other encumbrances. The property covered by that cap is enumerated in § 42.002(a) and includes home furnishings and heirlooms, provisions for consumption, farm/ranch vehicles and implements, trade tools and equipment (including boats and motor vehicles used in a trade or profession), clothing, jewelry (capped at 25% of the aggregate limit), two firearms, athletic and sporting equipment, one motor vehicle per licensed family member or single adult (or a non-licensed person who relies on another driver), specified numbers of livestock and fowl with their forage, and household pets. Section 42.001(b) exempts certain items entirely and outside the aggregate cap: current wages for personal services (except for court-ordered child support enforcement), professionally prescribed health aids for the debtor or a dependent, alimony/support/separate maintenance, and a religious bible or other sacred writings (except when seized by a landlord exercising rights after a lease breach or abandonment).'
  - gpt-5.5: grounded=True, error=None, summary='Texas exempts the personal property listed in Section 42.002 from garnishment, attachment, execution, or other seizure up to an aggregate fair market value of $100,000 for a family or $50,000 for a single adult who is not a family member, excluding liens and similar encumbrances. Certain items are exempt and do not count toward those limits, including current wages for personal services, prescribed health aids, support payments, and certain sacred religious writings. Section 42.002 lists covered property such as home furnishings, provisions, tools and trade equipment, clothing, limited jewelry, two firearms, sporting equipment, certain vehicles, specified animals, and household pets.'
  - gemini-2.5-pro: grounded=True, error=None, summary='Texas law exempts certain personal property from creditor seizure up to an aggregate fair market value of $100,000 for a family or $50,000 for a single adult, exclusive of any liens. The property subject to this dollar limit includes a specific list of items such as home furnishings, tools of a trade, vehicles, and household pets. Other property, including current wages, professionally prescribed health aids, and alimony, is also exempt from seizure and is not counted toward these aggregate value limits.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-HOMESTEAD-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260828T220708Z, 2026-08-28T22:23:48Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://statutes.capitol.texas.gov/Docs/PR/htm/PR.41.htm', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 250874, 'content_type': 'text/html', 'word_overlap_ratio': 0.053, 'retry_attempt': 2, 'longest_matching_prefix_chars': 1, 'text_at_break_point': ' homestead and one or more lots used for'}}, {'url': 'https://statutes.capitol.texas.gov/Docs/PR/htm/PR.41.htm', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 250874, 'content_type': 'text/html', 'word_overlap_ratio': 0.143, 'retry_attempt': 2, 'longest_matching_prefix_chars': 0, 'text_at_break_point': '(a) if used for the purposes of an urban'}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Tex. Prop. Code § 41.001(a), a homestead—and one or more lots used as a burial place—is exempt from seizure to satisfy creditors' claims, with the only stated exception being encumbrances properly fixed on the homestead property. Section 41.002 caps the size of the protected homestead: an urban homestead may be no more than 10 acres, in one or more contiguous lots, plus improvements. A rural homestead may be up to 200 acres for a family or up to 100 acres for a single adult person. The text does not address other limits (such as value) or what counts as a properly fixed encumbrance."
  - gpt-5.5: grounded=True, error=None, summary='A Texas homestead is exempt from seizure for creditor claims, except for encumbrances properly fixed on the homestead property. The protected homestead size is limited to up to 10 acres for an urban home, up to 200 acres for a rural family homestead, and up to 100 acres for a rural homestead of a single adult person.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Texas, a homestead and burial lots are exempt from being seized by creditors. This exemption does not apply, however, to encumbrances properly fixed on the homestead property. An urban homestead can be up to 10 acres, while a rural homestead can be up to 200 acres for a family or 100 acres for a single adult.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-WAGE-GARNISHMENT-PROHIBITION] ADVERSARIAL-GAP -- run run_20260828T220708Z, 2026-08-28T22:22:39Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': 'The U.S. Department of Education initiates administrative wage garnishment against a Texas resident for a defaulted federal student loan, and the IRS separately serves a levy on the same paycheck for unpaid federal income tax. The employer asks whether the Texas constitutional protection blocks both.', 'exposes_gap': True, 'gap_description': "The exception list is limited to child support and spousal maintenance and omits federal-law garnishments (federal student loan AWG under 20 U.S.C. 1095a, IRS levies under 26 U.S.C. 6331, federal criminal restitution/FDCPA judgments, and federal court judgments), which override the state constitutional protection under the Supremacy Clause. The checklist's single dispositive fact never asks whether the creditor or the underlying obligation arises under federal law."}, {'scenario': "A judgment debtor works as an independent contractor doing 1099 delivery work and also receives quarterly commission checks from a former employer for closed sales; the creditor serves a writ of garnishment on both payors, arguing these are not 'current wages for personal service.'", 'exposes_gap': True, 'gap_description': "The rule treats 'wages' as a self-evident binary category, but Texas case law distinguishes 'current wages for personal service' (protected) from independent contractor payments, earned-but-unpaid commissions, distributions to an owner-operator, severance, and retirement or disability payments — several of which courts have held fall outside the constitutional exemption or are protected only by separate Property Code provisions. The checklist provides no test for classifying the payment or the payor-payee relationship."}, {'scenario': "A creditor with a judgment obtained in Oklahoma serves a garnishment writ on the Texas debtor's employer, a national retailer with its payroll office and registered agent in Oklahoma, in an Oklahoma court; the debtor lives and works in Texas.", 'exposes_gap': True, 'gap_description': "The rule assumes a Texas forum and Texas law apply, but says nothing about choice of law, situs of the debt, or the fact that the Texas exemption is generally treated as procedural/forum-specific — a sister-state court may apply its own garnishment law to a Texas resident's wages when it has jurisdiction over the employer. The checklist omits any fact about where the judgment was rendered, where the garnishment action is filed, or the employer's location."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Article XVI, Section 28 of the Texas Constitution states that current wages for personal service can never be garnished, carving out only two exceptions: court-ordered child support payments and court-ordered spousal maintenance. Because ordinary consumer debt (such as credit card or medical bills) is not among those two exceptions, a creditor holding such a debt cannot garnish a debtor's current wages in Texas. The protection is framed as absolute ('shall ever be subject to') for everything outside those enumerated family-support obligations. Note the text protects 'current wages for personal service' specifically, and does not address other forms of property or funds."
  - gpt-5.5: grounded=True, error=None, summary='The Texas Constitution states that current wages for personal service are not subject to garnishment except to enforce court-ordered child support or spousal maintenance. Because ordinary consumer debt is not listed as an exception, the text supports that such wages cannot be garnished for ordinary consumer debt.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-WAGE-GARNISHMENT-PROHIBITION] CITATION-CHECK-FAILED -- run run_20260828T220708Z, 2026-08-28T22:22:39Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://statutes.capitol.texas.gov/Docs/CN/htm/CN.16.htm', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 250874, 'content_type': 'text/html', 'word_overlap_ratio': 0.0, 'retry_attempt': 2, 'longest_matching_prefix_chars': 2, 'text_at_break_point': ' current wages for personal service shal'}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Article XVI, Section 28 of the Texas Constitution states that current wages for personal service can never be garnished, carving out only two exceptions: court-ordered child support payments and court-ordered spousal maintenance. Because ordinary consumer debt (such as credit card or medical bills) is not among those two exceptions, a creditor holding such a debt cannot garnish a debtor's current wages in Texas. The protection is framed as absolute ('shall ever be subject to') for everything outside those enumerated family-support obligations. Note the text protects 'current wages for personal service' specifically, and does not address other forms of property or funds."
  - gpt-5.5: grounded=True, error=None, summary='The Texas Constitution states that current wages for personal service are not subject to garnishment except to enforce court-ordered child support or spousal maintenance. Because ordinary consumer debt is not listed as an exception, the text supports that such wages cannot be garnished for ordinary consumer debt.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-WAGE-GARNISHMENT-PROHIBITION] MODEL-DISAGREEMENT -- run run_20260828T220708Z, 2026-08-28T22:22:39Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['2'], OpenAI=[], Gemini=[] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Article XVI, Section 28 of the Texas Constitution states that current wages for personal service can never be garnished, carving out only two exceptions: court-ordered child support payments and court-ordered spousal maintenance. Because ordinary consumer debt (such as credit card or medical bills) is not among those two exceptions, a creditor holding such a debt cannot garnish a debtor's current wages in Texas. The protection is framed as absolute ('shall ever be subject to') for everything outside those enumerated family-support obligations. Note the text protects 'current wages for personal service' specifically, and does not address other forms of property or funds."
  - gpt-5.5: grounded=True, error=None, summary='The Texas Constitution states that current wages for personal service are not subject to garnishment except to enforce court-ordered child support or spousal maintenance. Because ordinary consumer debt is not listed as an exception, the text supports that such wages cannot be garnished for ordinary consumer debt.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-SOL-CONSUMER-DEBT] CITATION-CHECK-FAILED -- run run_20260828T220708Z, 2026-08-28T22:21:53Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://statutes.capitol.texas.gov/Docs/CP/htm/CP.16.htm', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 250874, 'content_type': 'text/html', 'word_overlap_ratio': 0.053, 'retry_attempt': 2, 'longest_matching_prefix_chars': 1, 'text_at_break_point': ' person must bring suit on the following'}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Tex. Civ. Prac. & Rem. Code § 16.004(a), a suit on a 'debt' is among the actions listed in subsection (3) that must be brought no later than four years after the day the cause of action accrues. So a collection lawsuit on a consumer debt is subject to a four-year limitations period running from accrual. The provision quoted does not define when a debt cause of action accrues, so that point cannot be resolved from this text alone."
  - gpt-5.5: grounded=True, error=None, summary='A suit on a debt must be brought no later than four years after the day the cause of action accrues. The text lists “debt” among the actions subject to this four-year limitations period.'
  - gemini-2.5-pro: grounded=True, error=None, summary="According to the provided text, a person must bring a suit on a debt not later than four years after the day the cause of action accrues. The statute explicitly lists 'debt' as one of the actions subject to this four-year limitations period."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY] CITATION-CHECK-FAILED -- run run_20260828T220708Z, 2026-08-28T22:21:00Z

**File:** `rules/debt/state/texas/tx_debt_band3_discretionary_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 3 cited source(s) could not be mechanically verified live: [{'url': 'https://www.courtlistener.com/opinion/4172687/craddock-v-sunshine-bus-lines-inc/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 202, 'content_length': 2006, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.176, 'retry_attempt': 2, 'longest_matching_prefix_chars': 2, 'text_at_break_point': 'default judgment should be set aside and'}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Craddock, a default judgment should be set aside and a new trial granted when three things are shown: (1) the defendant's failure to answer before judgment was not intentional or the result of conscious indifference, but was due to a mistake or accident; (2) the motion for new trial sets up a meritorious defense; and (3) the motion is filed at a time when granting it will cause no delay or other injury to the plaintiff. Because each element turns on the particular facts — e.g., whether the excuse amounts to mere mistake versus conscious indifference, whether the defense asserted is 'meritorious,' and whether the plaintiff would be injured — the outcome is a multi-factor judgment call rather than a mechanical rule. The motion itself must be filed before or within thirty days after the judgment is signed, and if no written order ruling on it is signed within seventy-five days after the judgment, it is overruled by operation of law."
  - gpt-5.5: grounded=True, error=None, summary='A Texas default judgment should be set aside and a new trial ordered when the defendant’s failure to answer was not intentional or due to conscious indifference, but resulted from mistake or accident; the motion sets up a meritorious defense; and granting it will not delay or injure the plaintiff. The motion for new trial must be filed within 30 days after the judgment is signed, and if not determined by signed written order within 75 days, it is overruled by operation of law. The provided text supplies a multi-factor standard, but it does not characterize the determination as genuinely discretionary.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A default judgment should be set aside when the defendant's failure to answer was not intentional or the result of conscious indifference, but was instead due to a mistake or accident. The motion for new trial must also set up a meritorious defense. Finally, granting the motion must not cause delay or otherwise injure the plaintiff."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY] MODEL-DISAGREEMENT -- run run_20260828T220708Z, 2026-08-28T22:21:00Z

**File:** `rules/debt/state/texas/tx_debt_band3_discretionary_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: All three state the same three-element Craddock test (no intentional/consciously indifferent failure to answer, meritorious defense set up, and no delay or injury to plaintiff). However, Analyses 1 and 2 additionally state the procedural deadlines — the motion for new trial must be filed within 30 days of the signed judgment and is overruled by operation of law if not ruled on by signed order within 75 days — which Analysis 3 omits entirely. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['1', '2', '3', '30', '75'], OpenAI=['30', '75'], Gemini=[] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Craddock, a default judgment should be set aside and a new trial granted when three things are shown: (1) the defendant's failure to answer before judgment was not intentional or the result of conscious indifference, but was due to a mistake or accident; (2) the motion for new trial sets up a meritorious defense; and (3) the motion is filed at a time when granting it will cause no delay or other injury to the plaintiff. Because each element turns on the particular facts — e.g., whether the excuse amounts to mere mistake versus conscious indifference, whether the defense asserted is 'meritorious,' and whether the plaintiff would be injured — the outcome is a multi-factor judgment call rather than a mechanical rule. The motion itself must be filed before or within thirty days after the judgment is signed, and if no written order ruling on it is signed within seventy-five days after the judgment, it is overruled by operation of law."
  - gpt-5.5: grounded=True, error=None, summary='A Texas default judgment should be set aside and a new trial ordered when the defendant’s failure to answer was not intentional or due to conscious indifference, but resulted from mistake or accident; the motion sets up a meritorious defense; and granting it will not delay or injure the plaintiff. The motion for new trial must be filed within 30 days after the judgment is signed, and if not determined by signed written order within 75 days, it is overruled by operation of law. The provided text supplies a multi-factor standard, but it does not characterize the determination as genuinely discretionary.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A default judgment should be set aside when the defendant's failure to answer was not intentional or the result of conscious indifference, but was instead due to a mistake or accident. The motion for new trial must also set up a meritorious defense. Finally, granting the motion must not cause delay or otherwise injure the plaintiff."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-VEHICLE-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260828T220708Z, 2026-08-28T22:17:45Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['$7500', '1'], OpenAI=['$7500', '1'], Gemini=[] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.010(a), a judgment debtor may exempt up to $7,500 in any combination of aggregate equity in motor vehicles, proceeds of an execution sale of a motor vehicle, and proceeds of insurance or other indemnification for a vehicle's loss, damage, or destruction. Subdivision (d) provides that if the debtor owns only one motor vehicle and it is sold at an execution sale, the $7,500 of sale proceeds is automatically exempt without the debtor having to make a claim, and the levying officer may consult and rely on Department of Motor Vehicles records to confirm the debtor has only one vehicle. In that single-vehicle situation, the subdivision (a) exemption is not additionally available."
  - gpt-5.5: grounded=True, error=None, summary='California exempts up to $7,500 in any combination of aggregate equity in motor vehicles, proceeds from an execution sale of a motor vehicle, and insurance or indemnification proceeds for loss, damage, or destruction of a motor vehicle. If the judgment debtor has only one motor vehicle and it is sold at an execution sale, $7,500 of the sale proceeds is exempt without making a claim, and the subdivision (a) exemption is not available in that situation.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-WRITTEN-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260828T220708Z, 2026-08-28T22:13:56Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: All three agree on the core rule: a four-year limitations period for actions on written contracts, and a bar on suit, arbitration, or other collection proceedings once it expires. However, Analysis 3 omits the rule that the period may be extended only under Section 360 (stated by both 1 and 2), and Analysis 1 alone adds the Section 336a exception and the special three-month deadline for deficiency-type money judgments after a trustee's/power-of-sale sale, which Analyses 2 and 3 omit entirely. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['3', '4'], OpenAI=['4'], Gemini=['4'] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 337(a), an action on any contract, obligation, or liability founded on a written instrument must be brought within four years (subject to the exception in Section 336a, and a special three-month rule for deficiency-type money judgments after a trustee's or mortgage power-of-sale sale). Section 337(d) adds that once that four-year period has run, a person may not bring suit or initiate arbitration or any other legal proceeding to collect the debt. The limitations period may be extended only as provided in Section 360."
  - gpt-5.5: grounded=True, error=None, summary='An action on a contract, obligation, or liability founded on a written instrument must be brought within four years. Once that period has run, a person may not bring suit, initiate arbitration, or start another legal proceeding to collect the debt, and the period may be extended only under Section 360.'
  - gemini-2.5-pro: grounded=True, error=None, summary='The statute of limitations for an action upon a contract founded upon an instrument in writing is four years. The provided text establishes this four-year period for bringing such a lawsuit. Once this time period has expired, a person is prohibited from bringing a suit, arbitration, or other legal proceeding to collect the debt.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] CITATION-CHECK-FAILED -- run run_20260828T220708Z, 2026-08-28T22:12:49Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 5 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 104703, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0, 'retry_attempt': 2, 'longest_matching_prefix_chars': 112, 'text_at_break_point': ': (1) de'}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=False, error=None, summary="The cited text supplies the compliance test but no facts about any particular notice or consumer, so the ultimate yes/no cannot be determined here. Under 15 U.S.C. § 1692g(a) a notice is compliant only if, in the initial communication or in writing within five days after it, the collector states the amount of the debt, the creditor's name, and the three required statements about the 30-day dispute window, verification, and the original creditor's name and address; 12 C.F.R. § 1006.34(a)(1) and (c) add that the validation information may be given orally in the initial communication or by a validation notice sent in or within five days of it, and must include the collection-communication disclosure, itemized debt information, consumer-protection disclosures (including the dispute-window end date), and response prompts. As to timing, § 1006.34(b)(5) defines the validation period as running from the date the information is provided until 30 days after the consumer receives (or is assumed to receive) it, with receipt assumable five business days after provision; § 1692g(a)(3)-(5) likewise keys the window to 30 days after receipt. Applying those dates to the actual notice date would answer whether the window is still open, and under § 1692g(b) a written dispute within that period requires the collector to cease collection until verification is mailed."
  - gpt-5.5: grounded=False, error=None, summary='The text provides the requirements for a compliant validation notice: it must be given in the initial communication, within five days after it, or orally in the initial communication, and must include specified debt, creditor, dispute-right, verification, original-creditor, and consumer-response information. The dispute/validation period starts when the validation information is provided and ends 30 days after the consumer receives or is assumed to receive it; receipt may be assumed at least five business days after provision. However, the excerpt gives no facts about what notice was provided, when it was provided or received, or what it contained, so compliance and whether the consumer is still within the window cannot be determined.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A compliant debt validation notice must be provided either in the initial communication or within five days after. The notice must contain specific information about the debt and inform the consumer of their right to dispute the debt within 30 days of receiving the notice. This 30-day dispute window, or "validation period," ends 30 days after the consumer receives the information, and for calculation purposes, receipt can be assumed to occur five business days after the collector sends it.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] MODEL-DISAGREEMENT -- run run_20260828T220708Z, 2026-08-28T22:12:49Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['3', '30', '5'], OpenAI=['30', '5'], Gemini=['30', '5'] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=False, error=None, summary="The cited text supplies the compliance test but no facts about any particular notice or consumer, so the ultimate yes/no cannot be determined here. Under 15 U.S.C. § 1692g(a) a notice is compliant only if, in the initial communication or in writing within five days after it, the collector states the amount of the debt, the creditor's name, and the three required statements about the 30-day dispute window, verification, and the original creditor's name and address; 12 C.F.R. § 1006.34(a)(1) and (c) add that the validation information may be given orally in the initial communication or by a validation notice sent in or within five days of it, and must include the collection-communication disclosure, itemized debt information, consumer-protection disclosures (including the dispute-window end date), and response prompts. As to timing, § 1006.34(b)(5) defines the validation period as running from the date the information is provided until 30 days after the consumer receives (or is assumed to receive) it, with receipt assumable five business days after provision; § 1692g(a)(3)-(5) likewise keys the window to 30 days after receipt. Applying those dates to the actual notice date would answer whether the window is still open, and under § 1692g(b) a written dispute within that period requires the collector to cease collection until verification is mailed."
  - gpt-5.5: grounded=False, error=None, summary='The text provides the requirements for a compliant validation notice: it must be given in the initial communication, within five days after it, or orally in the initial communication, and must include specified debt, creditor, dispute-right, verification, original-creditor, and consumer-response information. The dispute/validation period starts when the validation information is provided and ends 30 days after the consumer receives or is assumed to receive it; receipt may be assumed at least five business days after provision. However, the excerpt gives no facts about what notice was provided, when it was provided or received, or what it contained, so compliance and whether the consumer is still within the window cannot be determined.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A compliant debt validation notice must be provided either in the initial communication or within five days after. The notice must contain specific information about the debt and inform the consumer of their right to dispute the debt within 30 days of receiving the notice. This 30-day dispute window, or "validation period," ends 30 days after the consumer receives the information, and for calculation purposes, receipt can be assumed to occur five business days after the collector sends it.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] CITATION-CHECK-FAILED -- run run_20260828T220708Z, 2026-08-28T22:11:21Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692f', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 35834, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0, 'retry_attempt': 2, 'longest_matching_prefix_chars': 101, 'text_at_break_point': '. without limiting '}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692f imposes a general ban on debt collectors using unfair or unconscionable means to collect a debt, then lists specific violations without limiting that general rule. These include: collecting any amount (interest, fees, charges, expenses) not expressly authorized by the debt agreement or permitted by law; accepting a check postdated more than five days without written notice of intent to deposit sent 3-10 business days beforehand; soliciting postdated instruments to threaten or institute criminal prosecution; depositing or threatening to deposit a postdated instrument early; causing a person to incur communication charges by concealing the communication's true purpose; taking or threatening nonjudicial dispossession/disablement of property when there is no present right to possession through an enforceable security interest, no present intent to take possession, or the property is legally exempt. It also bars communicating with a consumer about a debt by post card and using any language or symbol on mail envelopes other than the collector's address, though a business name may be used if it does not reveal the debt collection business."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect or attempt to collect a debt. The statute lists violations including collecting unauthorized amounts, certain misuse of postdated checks or payment instruments, concealing the purpose of communications to cause charges, improper nonjudicial dispossession or disablement of property, communicating by postcard, and using prohibited language or symbols on envelopes.'
  - gemini-2.5-pro: grounded=True, error=None, summary='Unfair or unconscionable debt collection practices include collecting any amount, such as interest or fees, not expressly authorized by the agreement or permitted by law. It is also a violation to improperly handle postdated checks, such as depositing them without proper notice or soliciting them to threaten criminal prosecution. Other prohibited acts include taking property without a present right to possession, communicating about a debt via postcard, and using envelopes that reveal the communication is from a debt collector.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] CITATION-CHECK-FAILED -- run run_20260828T220708Z, 2026-08-28T22:10:15Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.18', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 74851, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0, 'retry_attempt': 2, 'longest_matching_prefix_chars': 4, 'text_at_break_point': 'initial communications. a debt collector'}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means to collect a debt, and then lists non-exhaustive examples: falsely claiming government affiliation or bonding; misrepresenting the character, amount, or legal status of a debt or services/compensation; falsely implying an attorney is involved; threatening arrest, imprisonment, seizure, garnishment, attachment, or sale of property when such action is unlawful or not intended; threatening any action that cannot legally or will not be taken; communicating known-false credit information (including failing to note a debt is disputed); using documents simulating court or agency process or falsely claiming/denying that documents are legal process; using any false or deceptive means to collect or to obtain consumer information; failing to give the required debt-collector disclosures; falsely implying accounts were sold to innocent purchasers; using a name other than the collector's true name; and falsely implying the collector is or works for a consumer reporting agency. As to the disclosure item (§ 1692e(11)), Regulation F's operative version requires the collector to state in the initial communication that it is attempting to collect a debt and that information obtained will be used for that purpose (repeated in the first written communication if the initial contact was oral), and to disclose in each subsequent communication that it is from a debt collector. That disclosure is not required in a formal pleading made in connection with a legal action."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use any false, deceptive, or misleading representation or means in connection with collecting a debt. The prohibited conduct includes falsely implying government affiliation, misstating the debt’s character/amount/legal status, falsely implying attorney involvement or legal process, threatening unlawful or unintended action, communicating false credit information, using deceptive documents or names, and using any false representation or deceptive means to collect a debt or obtain consumer information. Debt collectors also must give the required debt-collection disclosures in initial and subsequent communications, except that those disclosures are not required in a formal pleading made in connection with a legal action.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] MODEL-DISAGREEMENT -- run run_20260828T220708Z, 2026-08-28T22:10:15Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=[], OpenAI=[], Gemini=[] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means to collect a debt, and then lists non-exhaustive examples: falsely claiming government affiliation or bonding; misrepresenting the character, amount, or legal status of a debt or services/compensation; falsely implying an attorney is involved; threatening arrest, imprisonment, seizure, garnishment, attachment, or sale of property when such action is unlawful or not intended; threatening any action that cannot legally or will not be taken; communicating known-false credit information (including failing to note a debt is disputed); using documents simulating court or agency process or falsely claiming/denying that documents are legal process; using any false or deceptive means to collect or to obtain consumer information; failing to give the required debt-collector disclosures; falsely implying accounts were sold to innocent purchasers; using a name other than the collector's true name; and falsely implying the collector is or works for a consumer reporting agency. As to the disclosure item (§ 1692e(11)), Regulation F's operative version requires the collector to state in the initial communication that it is attempting to collect a debt and that information obtained will be used for that purpose (repeated in the first written communication if the initial contact was oral), and to disclose in each subsequent communication that it is from a debt collector. That disclosure is not required in a formal pleading made in connection with a legal action."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use any false, deceptive, or misleading representation or means in connection with collecting a debt. The prohibited conduct includes falsely implying government affiliation, misstating the debt’s character/amount/legal status, falsely implying attorney involvement or legal process, threatening unlawful or unintended action, communicating false credit information, using deceptive documents or names, and using any false representation or deceptive means to collect a debt or obtain consumer information. Debt collectors also must give the required debt-collection disclosures in initial and subsequent communications, except that those disclosures are not required in a formal pleading made in connection with a legal action.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] CITATION-CHECK-FAILED -- run run_20260828T220708Z, 2026-08-28T22:09:22Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 75544, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0, 'retry_attempt': 2, 'longest_matching_prefix_chars': 4, 'text_at_break_point': 'subject to the exclusions in paragraph ('}}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 75544, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0, 'retry_attempt': 2, 'longest_matching_prefix_chars': 34, 'text_at_break_point': ', particular debt means each of a consum'}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2), a debt collector is presumed to comply with the prohibition on repeated/continuous calls (and FDCPA § 806(5)) if it places calls to a particular person about a particular debt no more than seven times in seven consecutive days, and does not call within seven consecutive days after having had a telephone conversation with that person about that debt (the conversation date counts as day one of that seven-day period). Exceeding either of those frequency limits creates a presumption that the collector violated the rule and FDCPA § 806(5). Both presumptions are subject to the exclusions in paragraph (b)(3). For counting purposes, 'particular debt' means each separate debt in collection, except that student loan debts serviced under a single account number when obtained by the collector are treated as one particular debt."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is presumed to violate the rule if, subject to the stated exclusions, it calls a particular person about a particular debt more than seven times within seven consecutive days, or calls within seven consecutive days after having a telephone conversation with that person about that debt. The date of the telephone conversation counts as the first day of the seven-day period. A “particular debt” means each debt in collection, except that student loan debts serviced under a single account number when obtained by the debt collector are treated together as one particular debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to have acted unlawfully if they call a person about a particular debt more than seven times within seven consecutive days. A violation is also presumed if the collector calls within seven consecutive days after having a telephone conversation with the person about that debt. This rule applies to each of a consumer's debts individually, except for student loans, where all debts under a single account number are treated as a single debt for this purpose."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b] MODEL-DISAGREEMENT -- run run_20260828T220708Z, 2026-08-28T22:08:14Z

**File:** `rules/debt/federal/fcra_furnisher_dispute_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: Skipped -- not all three models returned a grounded, error-free result. (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=[], OpenAI=[], Gemini=[] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Once a furnisher receives notice from a credit reporting agency that a consumer disputes the completeness or accuracy of information the furnisher supplied, § 1681s-2(b)(1) requires it to investigate the disputed item, review all relevant information the credit bureau forwarded with the notice, and report the investigation's results back to that bureau. If the investigation shows the information is incomplete or inaccurate, the furnisher must also report that to all other nationwide consumer reporting agencies it supplied, and must promptly modify, delete, or permanently block reporting of any item found inaccurate, incomplete, or unverifiable. Under § 1681s-2(b)(2), all of these investigations, reviews, and reports must be completed within the same time period that § 1681i(a)(1) gives the consumer reporting agency to complete its own reinvestigation."
  - gpt-5.5: grounded=True, error=None, summary='After receiving notice from a consumer reporting agency of a dispute about the completeness or accuracy of information the person furnished, the furnisher must investigate the disputed information, review all relevant information provided by the agency, and report the investigation results to the agency. If the information is found incomplete, inaccurate, or cannot be verified, the furnisher must take appropriate action such as modifying, deleting, or permanently blocking reporting of the item, and must report certain results to other nationwide consumer reporting agencies to which it furnished the information. The furnisher must complete the required investigations, reviews, and reports before the expiration of the period in which the consumer reporting agency must complete its required actions regarding the information.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


*(No open entries below this line — see "Archived" section. New entries from the next live run land here.)*

---

## Archived -- Pre-Fix Diagnostic Runs (archived 2026-08-28)

**Why archived, not resolved:** every entry below comes from live corroboration runs (`run_20260826T171949Z` through
`run_20260826T202441Z`, all 2026-08-26 evening) that predate this project's Round 12-15 citation and tooling fixes:
the User-Agent fix and eCFR/FindLaw/Justia normalization work (Round 11), the CA re-pin to leginfo.legislature.ca.gov
and eCFR ellipsis fix (Round 12), the TX re-pin to statutes.capitol.texas.gov + Craddock re-pin to CourtListener plus
retry-on-flake logic (Round 13), and the FDCPA (b)(4) diagnostic pinpoint (Round 14). Nearly every CITATION-CHECK-FAILED
entry below traces to a since-fixed cause: a 403 from a bot-blocking secondary aggregator (FindLaw/Justia -- now re-pinned
to primary/Tier-A sources for CA and TX; AZ/UT/NY re-pins are still open work), a stale User-Agent, or an eCFR
normalization edge case. Nearly every MODEL-DISAGREEMENT entry below rests solely on the numeric/citation-fingerprint
heuristic, which Round 11 demoted to a secondary, non-gating diagnostic in favor of LLM-judged semantic agreement --
so a fingerprint mismatch alone, on its own, is no longer this project's disagreement signal.

None of this is an attorney-level resolution and none of these entries are being asserted correct -- they are being
moved out of the Open lane because the pipeline conditions that produced them no longer reflect the current rule
files or runner. Per the append-only discipline, nothing is deleted: every entry, its per-model derivations, and its
blank Resolution/Resolved-by/Date fields are preserved verbatim below. If the upcoming full-corpus live run reproduces
any of the same MODEL-DISAGREEMENT findings under the current LLM-judge, or a genuine (non-pipeline) CITATION-CHECK-FAILED
persists after the AZ/UT/NY re-pins land, it will re-file as a fresh entry in the Open section above, on its own
merits, under current tooling.

**Archived by:** Claude (Cowork) -- **Date:** 2026-08-28 -- per Andy's 2026-08-26 evening directive item 3
("confirmation that the disagreement queue is clean of runs 1-2 artifacts so the new flags land in an empty lane").

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] CITATION-CHECK-FAILED -- run run_20260826T202441Z, 2026-08-26T20:25:47Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 75544, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0}}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 75544, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the prohibition on repeated/continuous calls (and FDCPA § 806(5)) if, as to a particular person and a particular debt, it places no more than seven calls within seven consecutive days and places no call within the seven consecutive days following a telephone conversation with that person about that debt (the conversation date counts as day one). Under § 1006.14(b)(2)(ii), exceeding either of those frequencies creates a presumption that the collector violated the rule and FDCPA § 806(5). Both presumptions are subject to the exclusions in paragraph (b)(3). Per § 1006.14(b)(4), the counts run separately for each debt in collection, except that student loan debts serviced under a single account number when obtained by the collector are treated as one 'particular debt.'"
  - gpt-5.5: grounded=True, error=None, summary='Subject to listed exclusions not provided here, a debt collector is presumed to comply if, for a particular person and a particular debt, it does not call more than seven times within seven consecutive days and does not call within seven consecutive days after having a telephone conversation with that person about that debt. The date of the telephone conversation counts as the first day of that seven-day period. A debt collector is presumed to violate the rule if it exceeds either of those call-frequency limits; “particular debt” generally means each debt in collection, with a special grouping rule for certain student loan debts serviced under one account number.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to violate the law if, in connection with a particular debt, they call a person more than seven times within seven consecutive days. A violation is also presumed if a collector calls within seven consecutive days after having a telephone conversation with that person about the debt. This frequency limit applies to each of a consumer's debts individually, except for student loans, where all loans under a single account number are treated as one debt."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-WRITTEN-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T201346Z, 2026-08-26T20:15:36Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/codes/california/code-ccp/part-2/title-2/chapter-3/section-337/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5999, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}, {'url': 'https://law.justia.com/codes/california/code-ccp/part-2/title-2/chapter-3/section-337/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5999, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 337(a), an action upon any contract, obligation, or liability founded upon a written instrument must be brought within four years (subject to the exception in Section 336a, and a special three-month limit for deficiency-type money judgments after a trustee's/mortgage power-of-sale sale). Subsection (d) adds that once that four-year period has run, a person may not file suit or start an arbitration or other legal proceeding to collect the debt. The only way the period may be extended is pursuant to Section 360."
  - gpt-5.5: grounded=True, error=None, summary='An action on a contract, obligation, or liability founded on a written instrument must be brought within four years. Once that limitations period has run, a person may not bring a lawsuit, arbitration, or other legal proceeding to collect the debt, and the period may be extended only under Section 360.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In California, the statute of limitations for an action upon a contract founded upon a written instrument is four years. There is a specific exception for actions for a money judgment after a power of sale on real property, which must be brought within three months. Once the applicable time period has run, a person is barred from bringing a suit or other legal proceeding to collect the debt.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-WRITTEN-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T201346Z, 2026-08-26T20:15:36Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: All three agree on the core rule: a four-year limitations period for actions on a written contract, with suit/arbitration barred once it runs. However, Analysis 2 omits the three-month exception for money judgments after a power-of-sale foreclosure (stated by Analyses 1 and 3), and Analysis 3 omits that the period may be extended only under Section 360 (stated by Analyses 1 and 2). (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['3', '4'], OpenAI=['4'], Gemini=['3', '4'] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 337(a), an action upon any contract, obligation, or liability founded upon a written instrument must be brought within four years (subject to the exception in Section 336a, and a special three-month limit for deficiency-type money judgments after a trustee's/mortgage power-of-sale sale). Subsection (d) adds that once that four-year period has run, a person may not file suit or start an arbitration or other legal proceeding to collect the debt. The only way the period may be extended is pursuant to Section 360."
  - gpt-5.5: grounded=True, error=None, summary='An action on a contract, obligation, or liability founded on a written instrument must be brought within four years. Once that limitations period has run, a person may not bring a lawsuit, arbitration, or other legal proceeding to collect the debt, and the period may be extended only under Section 360.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In California, the statute of limitations for an action upon a contract founded upon a written instrument is four years. There is a specific exception for actions for a money judgment after a power of sale on real property, which must be brought within three months. Once the applicable time period has run, a person is barred from bringing a suit or other legal proceeding to collect the debt.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] CITATION-CHECK-FAILED -- run run_20260826T201346Z, 2026-08-26T20:14:43Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 75544, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0}}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 75544, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the harassment prohibition in § 1006.14(b)(1) and FDCPA § 806(5) if it places calls to a particular person about a particular debt neither more than seven times in seven consecutive days, nor within seven consecutive days after having had a telephone conversation with that person about that debt. Conversely, under (b)(2)(ii), exceeding either of those frequencies creates a presumption of violation. The counts are applied per 'particular debt,' meaning each individual debt in collection, except that for student loans all debts serviced under a single account number when obtained by the collector count as one debt (§ 1006.14(b)(4))."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is presumed to comply if, for a particular person and a particular debt, it does not place more than seven calls within seven consecutive days and does not call within seven consecutive days after having had a telephone conversation with that person about that debt. A debt collector is presumed to violate the rule if it exceeds either of those call-frequency limits. For this purpose, a “particular debt” generally means each debt in collection, with a special rule grouping certain student loan debts serviced under a single account number.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to have violated the law if, in connection with a particular debt, they call a person more than seven times within seven consecutive days. A violation is also presumed if a collector calls within seven consecutive days after having a telephone conversation with that person about the debt. This rule applies to each of a consumer's individual debts, except for student loans, where all loans under a single account number are treated as one debt."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-JUSTICE-COURT-DEBT-ANSWER-DEADLINE] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:24:12Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://texaslawhelp.org/guide/how-to-answer-a-debt-collection-case-in-justice-court', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 120175, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.353}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Based on the supplied text, a defendant in a Texas justice court debt-collection suit must file an answer within 14 days after the date of service; if that 14th day lands on a weekend or court holiday, the deadline rolls to the next business day. The same excerpt notes that Texas justice courts hear debt claims valued up to $20,000. Caveat: this comes from a secondary-source (TexasLawHelp.org) restatement rather than the primary Rule 502.5 text, so the exact rule language and any additional timing mechanics (e.g., how the day of service is counted or filing cutoff time) are not verified here.'
  - gpt-5.5: grounded=True, error=None, summary='In a Texas justice-court debt-collection lawsuit, the defendant’s Answer is due 14 days after the date they were served. If the 14th day falls on a weekend or court holiday, the Answer is due on the next business day.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-JUSTICE-COURT-DEBT-ANSWER-DEADLINE] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:24:12Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['$20000', '14'], OpenAI=['14'], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Based on the supplied text, a defendant in a Texas justice court debt-collection suit must file an answer within 14 days after the date of service; if that 14th day lands on a weekend or court holiday, the deadline rolls to the next business day. The same excerpt notes that Texas justice courts hear debt claims valued up to $20,000. Caveat: this comes from a secondary-source (TexasLawHelp.org) restatement rather than the primary Rule 502.5 text, so the exact rule language and any additional timing mechanics (e.g., how the day of service is counted or filing cutoff time) are not verified here.'
  - gpt-5.5: grounded=True, error=None, summary='In a Texas justice-court debt-collection lawsuit, the defendant’s Answer is due 14 days after the date they were served. If the 14th day falls on a weekend or court holiday, the Answer is due on the next business day.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-EXEMPT-PERSONAL-PROPERTY] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:23:25Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 3 of 3 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/tx/property-code/prop-sect-42-001/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5616, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}, {'url': 'https://codes.findlaw.com/tx/property-code/prop-sect-42-001/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5616, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.071}}, {'url': 'https://codes.findlaw.com/tx/property-code/prop-sect-42-002/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5616, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under Tex. Prop. Code § 42.001(a), personal property of the kinds listed in § 42.002 is exempt from garnishment, attachment, execution, or other seizure up to an aggregate fair market value of $100,000 for property provided for a family, or $50,000 for a single adult who is not a member of a family. The qualifying categories in § 42.002(a) include home furnishings, provisions for consumption, farm/ranch vehicles and implements, tools and books of a trade or profession, clothing, jewelry (capped at 25 percent of the aggregate limit), two firearms, athletic and sporting equipment, one motor vehicle per licensed family member or single adult, specified livestock and fowl, and household pets. Separately, § 42.001(b) exempts certain property entirely outside the dollar caps: current wages for personal services (except for court-ordered child support enforcement), professionally prescribed health aids, alimony/support/separate maintenance, and a bible or other sacred writings.'
  - gpt-5.5: grounded=True, error=None, summary='Texas exempts certain personal property from garnishment, attachment, execution, or other seizure. For property listed in Section 42.002(a), the exemption applies up to an aggregate fair market value of $100,000 for a family or $50,000 for a single adult not in a family. Certain items, including current wages for personal services, prescribed health aids, support payments, and religious sacred writings, are exempt and are not counted toward those aggregate limits.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Texas, certain personal property is exempt from seizure by creditors up to an aggregate value of $100,000 for a family or $50,000 for a single adult. The categories of property subject to this limit include home furnishings, vehicles, tools of a trade, and household pets. Some specific property, such as current wages and professionally prescribed health aids, is also exempt and is not counted toward these dollar limits.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-EXEMPT-PERSONAL-PROPERTY] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:23:25Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['$100000', '$50000', '1', '2', '25'], OpenAI=['$100000', '$50000'], Gemini=['$100000', '$50000'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under Tex. Prop. Code § 42.001(a), personal property of the kinds listed in § 42.002 is exempt from garnishment, attachment, execution, or other seizure up to an aggregate fair market value of $100,000 for property provided for a family, or $50,000 for a single adult who is not a member of a family. The qualifying categories in § 42.002(a) include home furnishings, provisions for consumption, farm/ranch vehicles and implements, tools and books of a trade or profession, clothing, jewelry (capped at 25 percent of the aggregate limit), two firearms, athletic and sporting equipment, one motor vehicle per licensed family member or single adult, specified livestock and fowl, and household pets. Separately, § 42.001(b) exempts certain property entirely outside the dollar caps: current wages for personal services (except for court-ordered child support enforcement), professionally prescribed health aids, alimony/support/separate maintenance, and a bible or other sacred writings.'
  - gpt-5.5: grounded=True, error=None, summary='Texas exempts certain personal property from garnishment, attachment, execution, or other seizure. For property listed in Section 42.002(a), the exemption applies up to an aggregate fair market value of $100,000 for a family or $50,000 for a single adult not in a family. Certain items, including current wages for personal services, prescribed health aids, support payments, and religious sacred writings, are exempt and are not counted toward those aggregate limits.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Texas, certain personal property is exempt from seizure by creditors up to an aggregate value of $100,000 for a family or $50,000 for a single adult. The categories of property subject to this limit include home furnishings, vehicles, tools of a trade, and household pets. Some specific property, such as current wages and professionally prescribed health aids, is also exempt and is not counted toward these dollar limits.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-HOMESTEAD-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:22:07Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://statutes.capitol.texas.gov/Docs/PR/htm/PR.41.htm', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 250874, 'content_type': 'text/html', 'word_overlap_ratio': 0.053}}, {'url': 'https://statutes.capitol.texas.gov/Docs/PR/htm/PR.41.htm', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 250874, 'content_type': 'text/html', 'word_overlap_ratio': 0.143}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Tex. Prop. Code § 41.001(a), a homestead—along with one or more lots used as a burial place—is exempt from seizure to satisfy creditors' claims, with the only stated exception being encumbrances properly fixed on the homestead property. Section 41.002 caps the size of the protected homestead: an urban homestead (for a family or a single adult) may be no more than 10 acres, which may consist of one or more contiguous lots plus improvements. A rural homestead may be up to 200 acres for a family or up to 100 acres for a single adult. The text does not address other limits (such as value caps) or how urban versus rural status is determined beyond the stated use."
  - gpt-5.5: grounded=True, error=None, summary='Texas law exempts a homestead from seizure for creditors’ claims, except for encumbrances properly fixed on the homestead property. The protected homestead may be up to 10 acres for an urban home, up to 200 acres for a rural family homestead, or up to 100 acres for a rural homestead of a single adult person.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Texas, a homestead is exempt from seizure to satisfy creditor claims, except for encumbrances that are properly fixed on the property. The size of the protected homestead depends on its location. An urban homestead for a family or single adult may not exceed 10 acres, while a rural homestead may not exceed 200 acres for a family or 100 acres for a single adult.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-HOMESTEAD-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:22:07Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '10', '100', '200'], OpenAI=['10', '100', '200'], Gemini=['10', '100', '200'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Tex. Prop. Code § 41.001(a), a homestead—along with one or more lots used as a burial place—is exempt from seizure to satisfy creditors' claims, with the only stated exception being encumbrances properly fixed on the homestead property. Section 41.002 caps the size of the protected homestead: an urban homestead (for a family or a single adult) may be no more than 10 acres, which may consist of one or more contiguous lots plus improvements. A rural homestead may be up to 200 acres for a family or up to 100 acres for a single adult. The text does not address other limits (such as value caps) or how urban versus rural status is determined beyond the stated use."
  - gpt-5.5: grounded=True, error=None, summary='Texas law exempts a homestead from seizure for creditors’ claims, except for encumbrances properly fixed on the homestead property. The protected homestead may be up to 10 acres for an urban home, up to 200 acres for a rural family homestead, or up to 100 acres for a rural homestead of a single adult person.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Texas, a homestead is exempt from seizure to satisfy creditor claims, except for encumbrances that are properly fixed on the property. The size of the protected homestead depends on its location. An urban homestead for a family or single adult may not exceed 10 acres, while a rural homestead may not exceed 200 acres for a family or 100 acres for a single adult.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-WAGE-GARNISHMENT-PROHIBITION] ADVERSARIAL-GAP -- run run_20260826T190724Z, 2026-08-26T19:21:21Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': 'A Texas resident defaults on a federally guaranteed student loan and the Department of Education issues an administrative wage garnishment order to her employer; separately, the IRS serves a continuous levy on her paycheck for unpaid income taxes. Neither is child support nor spousal maintenance, and both target current wages.', 'exposes_gap': True, 'gap_description': 'The rule treats the Texas constitutional protection as absolute except for two family-law exceptions, but federal law (Supremacy Clause) permits garnishment/levy of Texas wages for federal student loans, federal taxes, and other federal debts. The exceptions list and the checklist omit any federal-debt or preemption inquiry, so the node would wrongly declare a lawful federal garnishment unconstitutional.'}, {'scenario': 'A judgment debtor is a 1099 independent contractor paid monthly commissions by a company, and separately is the sole owner of an S-corp from which he takes periodic distributions rather than a salary. The creditor serves a writ of garnishment on the paying company for amounts owed to him.', 'exposes_gap': True, 'gap_description': "The checklist's dispositive fact is only 'wages vs. bank account vs. support obligation,' but Texas courts limit the protection to 'current wages for personal service' from an employer-employee relationship; independent contractor payments, corporate distributions, rents, and similar income are generally garnishable. The rule provides no test for what qualifies as 'current wages' or whether an employment relationship exists."}, {'scenario': "A Texas-domiciled debtor works remotely for an employer headquartered in Georgia; the creditor domesticates its judgment in Georgia and garnishes the employer there under Georgia law. In a variant, the debtor's employer already issued the paycheck and it sits uncashed in the payroll office, or the wages were direct-deposited yesterday into his account.", 'exposes_gap': True, 'gap_description': "The rule assumes a single Texas forum and a clean wages/bank-account binary. It does not address choice of law or forum where an out-of-state court garnishes an out-of-state employer of a Texas debtor, nor the temporal boundary at which 'current wages' cease to be current (paid but undelivered, or freshly deposited funds that may retain exempt character under Tex. Prop. Code 42.001(d))."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under the Texas Constitution, current wages earned for personal service can never be garnished, with only two exceptions: court-ordered child support payments and court-ordered spousal maintenance. Because ordinary consumer debt (such as credit card or medical bills) falls outside those two enumerated exceptions, a creditor holding such a debt cannot garnish a debtor's current wages. The prohibition is absolute as to current wages for personal service; the text says nothing about other property or funds that are no longer current wages."
  - gpt-5.5: grounded=True, error=None, summary='Texas prohibits garnishment of current wages for personal service, except to enforce court-ordered child support or spousal maintenance. Because ordinary consumer debt is not one of the listed exceptions, the text supports that such wages cannot be garnished for ordinary consumer debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary='The Texas Constitution states that no current wages for personal service shall ever be subject to garnishment. The only exceptions provided in the text are for court-ordered child support payments or spousal maintenance. Because ordinary consumer debt does not fall into either of these specified exceptions, the general prohibition against wage garnishment applies.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-WAGE-GARNISHMENT-PROHIBITION] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:21:21Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/constitution/texas/sections/cn001600-002800.html', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5677, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under the Texas Constitution, current wages earned for personal service can never be garnished, with only two exceptions: court-ordered child support payments and court-ordered spousal maintenance. Because ordinary consumer debt (such as credit card or medical bills) falls outside those two enumerated exceptions, a creditor holding such a debt cannot garnish a debtor's current wages. The prohibition is absolute as to current wages for personal service; the text says nothing about other property or funds that are no longer current wages."
  - gpt-5.5: grounded=True, error=None, summary='Texas prohibits garnishment of current wages for personal service, except to enforce court-ordered child support or spousal maintenance. Because ordinary consumer debt is not one of the listed exceptions, the text supports that such wages cannot be garnished for ordinary consumer debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary='The Texas Constitution states that no current wages for personal service shall ever be subject to garnishment. The only exceptions provided in the text are for court-ordered child support payments or spousal maintenance. Because ordinary consumer debt does not fall into either of these specified exceptions, the general prohibition against wage garnishment applies.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-WAGE-GARNISHMENT-PROHIBITION] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:21:21Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['2'], OpenAI=['1'], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under the Texas Constitution, current wages earned for personal service can never be garnished, with only two exceptions: court-ordered child support payments and court-ordered spousal maintenance. Because ordinary consumer debt (such as credit card or medical bills) falls outside those two enumerated exceptions, a creditor holding such a debt cannot garnish a debtor's current wages. The prohibition is absolute as to current wages for personal service; the text says nothing about other property or funds that are no longer current wages."
  - gpt-5.5: grounded=True, error=None, summary='Texas prohibits garnishment of current wages for personal service, except to enforce court-ordered child support or spousal maintenance. Because ordinary consumer debt is not one of the listed exceptions, the text supports that such wages cannot be garnished for ordinary consumer debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary='The Texas Constitution states that no current wages for personal service shall ever be subject to garnishment. The only exceptions provided in the text are for court-ordered child support payments or spousal maintenance. Because ordinary consumer debt does not fall into either of these specified exceptions, the general prohibition against wage garnishment applies.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-SOL-CONSUMER-DEBT] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:20:40Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/codes/texas/civil-practice-and-remedies-code/title-2/subtitle-b/chapter-16/subchapter-a/section-16-004/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5906, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under the cited provision, a suit on a 'debt' must be filed no later than four years after the cause of action accrues. So a Texas consumer-debt collection lawsuit is subject to a four-year limitations period, measured from the date the claim accrues. The excerpt does not define when accrual occurs or address tolling, so those points cannot be determined from this text alone."
  - gpt-5.5: grounded=True, error=None, summary='A lawsuit on a debt must be brought no later than four years after the day the cause of action accrues. The text does not separately address consumer debt, but it expressly applies to actions for “debt.”'
  - gemini-2.5-pro: grounded=True, error=None, summary='A lawsuit on a debt must be brought no later than four years after the day the cause of action accrues. The provided statute explicitly lists "debt" as an action that is subject to this four-year time limit.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:19:56Z

**File:** `rules/debt/state/texas/tx_debt_band3_discretionary_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '2', '3', '30', '75'], OpenAI=['30', '75'], Gemini=['3'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Craddock, a default judgment 'should be set aside and a new trial ordered in any case in which' three conditions are met: (1) the defendant's failure to answer was not intentional or the result of conscious indifference, but due to mistake or accident; (2) the motion sets up a meritorious defense; and (3) it is filed at a time when granting it will cause no delay or other injury to the plaintiff. So the outcome is not purely open-ended discretion — the text makes relief mandatory in form ('should be set aside ... in any case in which') once the three elements are established, though each element requires a fact-specific evaluation. Timing is fixed by rule: the motion must be filed within thirty days after the judgment is signed (Rule 329b(a)), and if no written order is signed within seventy-five days of the judgment, the motion is overruled by operation of law (Rule 329b(c))."
  - gpt-5.5: grounded=True, error=None, summary='A Texas default judgment should be set aside and a new trial ordered when the defendant’s failure to answer was not intentional or due to conscious indifference, but resulted from mistake or accident. The motion must also set up a meritorious defense and be filed at a time when granting it will not delay or otherwise injure the plaintiff; a motion for new trial must be filed within thirty days after the judgment is signed, and if not ruled on by written order within seventy-five days, it is overruled by operation of law.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A Texas default judgment should be set aside on a motion for new trial if three conditions are met. First, the defendant's failure to answer was not intentional or the result of conscious indifference, but was due to a mistake or accident. Second, the motion for new trial must set up a meritorious defense. Third, the motion must be filed at a time when granting it will not cause delay or otherwise injure the plaintiff."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-CIVIL-ANSWER-DEADLINE] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:19:02Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-412-20/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5643, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}, {'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-412-20/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5643, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 412.20(a)(3), the summons must direct the defendant to file a written pleading responding to the complaint within 30 days after the summons is served. Subdivision (a)(6) repeats this in the required notice language: the court may decide against you unless you respond within 30 days. If the defendant does not respond, subdivision (a)(4) provides that a default may be entered on the plaintiff's application and the plaintiff may obtain the relief demanded, which could include wage garnishment or the taking of money or property. The text states a general summons rule and does not set a separate deadline specific to debt-collection suits."
  - gpt-5.5: grounded=True, error=None, summary='The summons must direct the defendant to file a written pleading responding to the complaint within 30 days after the summons is served. It also warns that if the defendant does not respond within 30 days, the court may decide against them and default may be entered, potentially leading to relief such as wage garnishment or taking money or property.'
  - gemini-2.5-pro: grounded=True, error=None, summary='According to the provided text, a defendant must file a written pleading in response to the complaint within 30 days after the summons is served. The summons itself must provide notice that a failure to respond within 30 days may result in the court deciding against the defendant without them being heard. If the defendant does not respond, a default may be entered against them, which could lead to garnishment of wages or the taking of property.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-CIVIL-ANSWER-DEADLINE] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:19:02Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['30', '4', '6'], OpenAI=['30'], Gemini=['30'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 412.20(a)(3), the summons must direct the defendant to file a written pleading responding to the complaint within 30 days after the summons is served. Subdivision (a)(6) repeats this in the required notice language: the court may decide against you unless you respond within 30 days. If the defendant does not respond, subdivision (a)(4) provides that a default may be entered on the plaintiff's application and the plaintiff may obtain the relief demanded, which could include wage garnishment or the taking of money or property. The text states a general summons rule and does not set a separate deadline specific to debt-collection suits."
  - gpt-5.5: grounded=True, error=None, summary='The summons must direct the defendant to file a written pleading responding to the complaint within 30 days after the summons is served. It also warns that if the defendant does not respond within 30 days, the court may decide against them and default may be entered, potentially leading to relief such as wage garnishment or taking money or property.'
  - gemini-2.5-pro: grounded=True, error=None, summary='According to the provided text, a defendant must file a written pleading in response to the complaint within 30 days after the summons is served. The summons itself must provide notice that a failure to respond within 30 days may result in the court deciding against the defendant without them being heard. If the defendant does not respond, a default may be entered against them, which could lead to garnishment of wages or the taking of property.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-BANK-ACCOUNT-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:18:15Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-704-220/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5668, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}, {'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-704-220/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5668, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.220(a), money in a judgment debtor's deposit account is automatically exempt — without the debtor having to file any exemption claim — up to an amount equal to the minimum basic standard of adequate care for a family of four for Region 1, as established by Welfare and Institutions Code section 11452 and adjusted annually by the State Department of Social Services under section 11453. The statute thus ties the protected minimum to that annually adjusted figure rather than stating a fixed dollar amount. Subdivision (c)(1) carves out an exception: the automatic exemption does not apply to money levied upon to satisfy a judgment for wages owed (including damages and penalties), child support, or spousal support."
  - gpt-5.5: grounded=True, error=None, summary='California exempts, without requiring a claim, money in a judgment debtor’s deposit account up to an amount equal to or less than the minimum basic standard of adequate care for a family of four for Region 1, as adjusted annually by the State Department of Social Services. This automatic exemption does not apply when the money is levied to satisfy a judgment for wages owed, child support, or spousal support; “wages owed” includes damages and penalties.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-BANK-ACCOUNT-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:18:15Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '4'], OpenAI=['1', '4'], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.220(a), money in a judgment debtor's deposit account is automatically exempt — without the debtor having to file any exemption claim — up to an amount equal to the minimum basic standard of adequate care for a family of four for Region 1, as established by Welfare and Institutions Code section 11452 and adjusted annually by the State Department of Social Services under section 11453. The statute thus ties the protected minimum to that annually adjusted figure rather than stating a fixed dollar amount. Subdivision (c)(1) carves out an exception: the automatic exemption does not apply to money levied upon to satisfy a judgment for wages owed (including damages and penalties), child support, or spousal support."
  - gpt-5.5: grounded=True, error=None, summary='California exempts, without requiring a claim, money in a judgment debtor’s deposit account up to an amount equal to or less than the minimum basic standard of adequate care for a family of four for Region 1, as adjusted annually by the State Department of Social Services. This automatic exemption does not apply when the money is levied to satisfy a judgment for wages owed, child support, or spousal support; “wages owed” includes damages and penalties.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-VEHICLE-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:17:15Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-704-010/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5668, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.010(a), a judgment debtor may exempt up to $7,500 in any combination of aggregate equity in motor vehicles, proceeds of an execution sale of a motor vehicle, and proceeds of insurance or other indemnification for a vehicle's loss, damage, or destruction. Subdivision (d) adds that if the debtor owns only one motor vehicle and it is sold at an execution sale, the sale proceeds are automatically exempt up to $7,500 without the debtor having to file a claim, with the levying officer permitted to rely on Department of Motor Vehicles records to confirm the debtor has only one vehicle. In that single-vehicle situation, the subdivision (a) exemption is not separately available."
  - gpt-5.5: grounded=True, error=None, summary='California exempts up to $7,500 for any combination of aggregate equity in motor vehicles, proceeds from an execution sale of a motor vehicle, and insurance or indemnification proceeds for loss, damage, or destruction of a motor vehicle. If the judgment debtor has only one motor vehicle and it is sold at an execution sale, $7,500 of the sale proceeds is exempt without making a claim, and the subdivision (a) exemption is not available in that case.'
  - gemini-2.5-pro: grounded=True, error=None, summary="California law provides a $7,500 exemption for a person's equity in motor vehicles. This exemption applies to the aggregate equity in motor vehicles, proceeds from an execution sale, or insurance proceeds from loss or damage. If a debtor has only one motor vehicle that is sold, the proceeds from that sale are automatically exempt up to $7,500 without a claim being made."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-HOMESTEAD-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:16:31Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-704-730/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5668, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.730(a), a judgment debtor's homestead exemption equals the greater of (1) the countywide median sale price for a single-family home in the calendar year before the year the exemption is claimed, capped at $600,000, or (2) a $300,000 floor. So the exemption is never less than $300,000 and never more than $600,000 under the baseline figures. Subdivision (b) provides that both figures adjust annually for inflation starting January 1, 2022, using the change in the annual California Consumer Price Index for All Urban Consumers published by the Department of Industrial Relations for the most recent one-year period ending December 31 before the adjustment, rounded to the nearest $25."
  - gpt-5.5: grounded=True, error=None, summary="The homestead exemption amount is the greater of either the prior calendar year's countywide median sale price for a single-family home, capped at $600,000, or $300,000. These amounts adjust annually for inflation beginning January 1, 2022, based on the California CPI for All Urban Consumers, rounded to the nearest $25."
  - gemini-2.5-pro: grounded=True, error=None, summary="The California homestead exemption is the greater of two amounts: either the county's median sale price for a single-family home from the prior year (up to a maximum of $600,000), or a baseline of $300,000. This means the exemption will always be at least $300,000. The law also states that these specified dollar amounts are adjusted annually for inflation based on the California Consumer Price Index."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-HOMESTEAD-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:16:31Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['$25', '$300000', '$600000', '1', '2', '2022', '31'], OpenAI=['$25', '$300000', '$600000', '1', '2022'], Gemini=['$300000', '$600000', '2'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.730(a), a judgment debtor's homestead exemption equals the greater of (1) the countywide median sale price for a single-family home in the calendar year before the year the exemption is claimed, capped at $600,000, or (2) a $300,000 floor. So the exemption is never less than $300,000 and never more than $600,000 under the baseline figures. Subdivision (b) provides that both figures adjust annually for inflation starting January 1, 2022, using the change in the annual California Consumer Price Index for All Urban Consumers published by the Department of Industrial Relations for the most recent one-year period ending December 31 before the adjustment, rounded to the nearest $25."
  - gpt-5.5: grounded=True, error=None, summary="The homestead exemption amount is the greater of either the prior calendar year's countywide median sale price for a single-family home, capped at $600,000, or $300,000. These amounts adjust annually for inflation beginning January 1, 2022, based on the California CPI for All Urban Consumers, rounded to the nearest $25."
  - gemini-2.5-pro: grounded=True, error=None, summary="The California homestead exemption is the greater of two amounts: either the county's median sale price for a single-family home from the prior year (up to a maximum of $600,000), or a baseline of $300,000. This means the exemption will always be at least $300,000. The law also states that these specified dollar amounts are adjusted annually for inflation based on the California Consumer Price Index."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-WAGE-GARNISHMENT-LIMIT] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:15:21Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-706-050/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5668, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}, {'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-706-050/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5668, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under § 706.050(a), unless another provision of the chapter says otherwise, the maximum amount of a judgment debtor's disposable earnings that may be levied under an earnings withholding order in any workweek is the lesser of (1) 20% of that week's disposable earnings, or (2) 40% of the amount by which that week's disposable earnings exceed 48 times the applicable minimum hourly wage. The applicable wage is the state minimum hourly wage in effect when the earnings are payable, or the local minimum wage if the debtor works where the local minimum is higher. This version of the section became operative September 1, 2023. Note: the quoted text states a general garnishment cap and does not itself contain a separate rule specific to consumer-debt judgments, which could appear elsewhere in the chapter under the 'except as otherwise provided' clause."
  - gpt-5.5: grounded=True, error=None, summary='As of September 1, 2023, the maximum disposable earnings of an individual judgment debtor subject to an earnings withholding order for a workweek is the lesser of: 20% of that week’s disposable earnings, or 40% of the amount by which that week’s disposable earnings exceed 48 times the applicable minimum hourly wage. The state minimum wage is used unless the debtor works where the local minimum wage is higher, in which case the local minimum wage is used.'
  - gemini-2.5-pro: grounded=True, error=None, summary="As of September 1, 2023, the maximum amount of an individual's weekly disposable earnings that can be garnished is the lesser of two figures. The first is 20% of the individual's disposable earnings for that week. The second is 40% of the amount by which the weekly earnings exceed 48 times the applicable state or local minimum wage."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-WAGE-GARNISHMENT-LIMIT] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:15:21Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '2', '20%', '2023', '40%', '48'], OpenAI=['1', '20%', '2023', '40%', '48'], Gemini=['1', '2', '20%', '2023', '40%', '48'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under § 706.050(a), unless another provision of the chapter says otherwise, the maximum amount of a judgment debtor's disposable earnings that may be levied under an earnings withholding order in any workweek is the lesser of (1) 20% of that week's disposable earnings, or (2) 40% of the amount by which that week's disposable earnings exceed 48 times the applicable minimum hourly wage. The applicable wage is the state minimum hourly wage in effect when the earnings are payable, or the local minimum wage if the debtor works where the local minimum is higher. This version of the section became operative September 1, 2023. Note: the quoted text states a general garnishment cap and does not itself contain a separate rule specific to consumer-debt judgments, which could appear elsewhere in the chapter under the 'except as otherwise provided' clause."
  - gpt-5.5: grounded=True, error=None, summary='As of September 1, 2023, the maximum disposable earnings of an individual judgment debtor subject to an earnings withholding order for a workweek is the lesser of: 20% of that week’s disposable earnings, or 40% of the amount by which that week’s disposable earnings exceed 48 times the applicable minimum hourly wage. The state minimum wage is used unless the debtor works where the local minimum wage is higher, in which case the local minimum wage is used.'
  - gemini-2.5-pro: grounded=True, error=None, summary="As of September 1, 2023, the maximum amount of an individual's weekly disposable earnings that can be garnished is the lesser of two figures. The first is 20% of the individual's disposable earnings for that week. The second is 40% of the amount by which the weekly earnings exceed 48 times the applicable state or local minimum wage."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-ORAL-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:14:31Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/codes/california/code-ccp/part-2/title-2/chapter-3/section-339/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5743, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under Cal. Code Civ. Proc. § 339(1), an action on a contract, obligation, or liability that is not founded upon a written instrument must be brought within two years. So a consumer-debt suit based on an oral or otherwise unwritten agreement is subject to a two-year limitations period. The text carves out exceptions for matters governed by Commercial Code section 2725 and section 337(2), and it separately covers claims evidenced by title certificates, abstracts, guaranties, or title insurance policies, for which the cause of action does not accrue until the loss or damage is discovered.'
  - gpt-5.5: grounded=True, error=None, summary='An action upon a contract, obligation, or liability that is not founded upon a written instrument must be brought within two years. The excerpt does not separately address consumer debt, but it does state the limitations period for unwritten contracts generally.'
  - gemini-2.5-pro: grounded=True, error=None, summary='According to the provided text, the statute of limitations for a lawsuit based on a contract that is not in writing is two years. The text refers to this as "an action upon a contract, obligation or liability not founded upon an instrument of writing." The statute mentions that exceptions to this rule may exist in other sections of the law, but does not describe them.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-WRITTEN-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:13:44Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/codes/california/code-ccp/part-2/title-2/chapter-3/section-337/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5743, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}, {'url': 'https://law.justia.com/codes/california/code-ccp/part-2/title-2/chapter-3/section-337/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5743, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 337(a), an action on a contract, obligation, or liability founded on a written instrument must be brought within four years (with an exception referencing Section 336a, and a special three-month limit for deficiency-type money judgments after a trustee's/mortgage power-of-sale sale). Section 337(d) adds that once that period has run, no one may file suit or initiate arbitration or other legal proceedings to collect the debt. The limitations period may be extended only as provided in Section 360."
  - gpt-5.5: grounded=True, error=None, summary='An action on a contract, obligation, or liability founded on a written instrument must be brought within four years. Once that limitations period has run, a person may not sue, initiate arbitration, or start another legal proceeding to collect the debt, and the period may be extended only under Section 360.'
  - gemini-2.5-pro: grounded=True, error=None, summary='An action upon a contract founded on a written instrument must be commenced within four years. The text specifies a much shorter three-month limitation for lawsuits seeking a money judgment on a debt that was secured by a deed of trust or mortgage on real property after that property has been sold. Once the applicable time period has run, a person is prohibited from bringing a suit or other legal proceeding to collect the debt.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-WRITTEN-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:13:44Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '3', '4'], OpenAI=['4'], Gemini=['3', '4'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 337(a), an action on a contract, obligation, or liability founded on a written instrument must be brought within four years (with an exception referencing Section 336a, and a special three-month limit for deficiency-type money judgments after a trustee's/mortgage power-of-sale sale). Section 337(d) adds that once that period has run, no one may file suit or initiate arbitration or other legal proceedings to collect the debt. The limitations period may be extended only as provided in Section 360."
  - gpt-5.5: grounded=True, error=None, summary='An action on a contract, obligation, or liability founded on a written instrument must be brought within four years. Once that limitations period has run, a person may not sue, initiate arbitration, or start another legal proceeding to collect the debt, and the period may be extended only under Section 360.'
  - gemini-2.5-pro: grounded=True, error=None, summary='An action upon a contract founded on a written instrument must be commenced within four years. The text specifies a much shorter three-month limitation for lawsuits seeking a money judgment on a debt that was secured by a deed of trust or mortgage on real property after that property has been sold. Once the applicable time period has run, a person is prohibited from bringing a suit or other legal proceeding to collect the debt.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:12:51Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 3 of 5 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 10596, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 0.286}}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 10596, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 0.25}}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 10596, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 0.333}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="A notice is compliant only if, within five days of the initial communication (or in that communication itself), the collector provides the consumer the amount of the debt, the name of the creditor owed, and the three statements about the 30-day dispute window, verification upon written dispute, and the right to request the original creditor's name and address (15 U.S.C. § 1692g(a)); under Regulation F the notice must also contain the full validation information in 12 C.F.R. § 1006.34(c), including the debt-collector communication disclosure, itemization details, dispute-window end date, and response prompts, delivered as required by § 1006.34(a)(1). The consumer is still within the dispute window if fewer than 30 days have passed since receipt of the validation information, measured from the date the information was provided to 30 days after actual or assumed receipt, with receipt presumed no earlier than five business days (excluding Saturdays, Sundays, and legal public holidays) after it was sent (12 C.F.R. § 1006.34(b)(5)). A timely written dispute or original-creditor request triggers § 1692g(b): the collector must cease collection of the disputed portion until verification, a judgment copy, or the original creditor's name and address is mailed to the consumer; otherwise collection may continue during the 30 days. The excerpt supplies the governing standard and timing rules but contains no facts about the particular notice or dates, so the ultimate yes/no answer depends on applying these elements to the actual notice and mailing/receipt dates."
  - gpt-5.5: grounded=False, error=None, summary='The text states that a debt collector must provide validation information in the initial communication, within five days after it, or orally in the initial communication, and the required content includes debt information, consumer-protection statements, and response information. The consumer’s validation/dispute period runs from when the validation information is provided until 30 days after the consumer receives or is assumed to receive it, with receipt assumable at least five business days after provision. However, the provided text contains no facts about what notice was sent, what it contained, when it was provided, or when the consumer received it, so compliance and whether the dispute window remains open cannot be determined.'
  - gemini-2.5-pro: grounded=True, error=None, summary='The provided texts do not contain facts to determine if a compliant notice was provided in a specific case, but they outline the legal requirements. A debt collector must provide a validation notice with specific information either orally in the initial communication or in writing within five days of it. The consumer has a 30-day "validation period" to dispute the debt, which ends 30 days after the consumer receives the notice; the collector may assume receipt occurs five business days after providing it.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:12:51Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['3', '30', '5'], OpenAI=['30', '5'], Gemini=['30', '5'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="A notice is compliant only if, within five days of the initial communication (or in that communication itself), the collector provides the consumer the amount of the debt, the name of the creditor owed, and the three statements about the 30-day dispute window, verification upon written dispute, and the right to request the original creditor's name and address (15 U.S.C. § 1692g(a)); under Regulation F the notice must also contain the full validation information in 12 C.F.R. § 1006.34(c), including the debt-collector communication disclosure, itemization details, dispute-window end date, and response prompts, delivered as required by § 1006.34(a)(1). The consumer is still within the dispute window if fewer than 30 days have passed since receipt of the validation information, measured from the date the information was provided to 30 days after actual or assumed receipt, with receipt presumed no earlier than five business days (excluding Saturdays, Sundays, and legal public holidays) after it was sent (12 C.F.R. § 1006.34(b)(5)). A timely written dispute or original-creditor request triggers § 1692g(b): the collector must cease collection of the disputed portion until verification, a judgment copy, or the original creditor's name and address is mailed to the consumer; otherwise collection may continue during the 30 days. The excerpt supplies the governing standard and timing rules but contains no facts about the particular notice or dates, so the ultimate yes/no answer depends on applying these elements to the actual notice and mailing/receipt dates."
  - gpt-5.5: grounded=False, error=None, summary='The text states that a debt collector must provide validation information in the initial communication, within five days after it, or orally in the initial communication, and the required content includes debt information, consumer-protection statements, and response information. The consumer’s validation/dispute period runs from when the validation information is provided until 30 days after the consumer receives or is assumed to receive it, with receipt assumable at least five business days after provision. However, the provided text contains no facts about what notice was sent, what it contained, when it was provided, or when the consumer received it, so compliance and whether the dispute window remains open cannot be determined.'
  - gemini-2.5-pro: grounded=True, error=None, summary='The provided texts do not contain facts to determine if a compliant notice was provided in a specific case, but they outline the legal requirements. A debt collector must provide a validation notice with specific information either orally in the initial communication or in writing within five days of it. The consumer has a 30-day "validation period" to dispute the debt, which ends 30 days after the consumer receives the notice; the collector may assume receipt occurs five business days after providing it.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:11:40Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692f', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 35834, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692f imposes a general ban on a debt collector's use of unfair or unconscionable means to collect a debt, then lists non-exhaustive examples of violations. These include collecting any amount (interest, fees, charges, expenses) not expressly authorized by the debt agreement or permitted by law; accepting a check postdated more than five days without written notice of intent to deposit given 3-10 business days beforehand; soliciting postdated instruments to threaten or institute criminal prosecution; depositing or threatening to deposit a postdated instrument early; causing a person to incur communication charges by concealing the communication's true purpose; and taking or threatening nonjudicial dispossession or disablement of property where there is no present enforceable right to possession, no present intent to take possession, or the property is exempt by law. It also bars communicating with a consumer about a debt by post card and using any language or symbol on a mailed envelope other than the collector's address, though a business name may be used if it does not indicate the debt collection business."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect or attempt to collect any debt. The listed violations include collecting unauthorized amounts; certain improper handling or solicitation of postdated checks; causing communication charges by concealing the purpose of a communication; improper nonjudicial repossession or disablement actions; communicating about a debt by postcard; and using prohibited language or symbols on mailed envelopes or telegrams.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect a debt, which includes a number of specific, prohibited actions. These forbidden acts include collecting any amount not authorized by the agreement or law, misusing postdated checks, and taking or threatening to take property without a present right to do so. Other prohibited practices are communicating about a debt via postcard and using any language or symbol on an envelope, other than an address, that indicates the communication is from a debt collector.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:11:40Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['10', '3', '5'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692f imposes a general ban on a debt collector's use of unfair or unconscionable means to collect a debt, then lists non-exhaustive examples of violations. These include collecting any amount (interest, fees, charges, expenses) not expressly authorized by the debt agreement or permitted by law; accepting a check postdated more than five days without written notice of intent to deposit given 3-10 business days beforehand; soliciting postdated instruments to threaten or institute criminal prosecution; depositing or threatening to deposit a postdated instrument early; causing a person to incur communication charges by concealing the communication's true purpose; and taking or threatening nonjudicial dispossession or disablement of property where there is no present enforceable right to possession, no present intent to take possession, or the property is exempt by law. It also bars communicating with a consumer about a debt by post card and using any language or symbol on a mailed envelope other than the collector's address, though a business name may be used if it does not indicate the debt collection business."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect or attempt to collect any debt. The listed violations include collecting unauthorized amounts; certain improper handling or solicitation of postdated checks; causing communication charges by concealing the purpose of a communication; improper nonjudicial repossession or disablement actions; communicating about a debt by postcard; and using prohibited language or symbols on mailed envelopes or telegrams.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect a debt, which includes a number of specific, prohibited actions. These forbidden acts include collecting any amount not authorized by the agreement or law, misusing postdated checks, and taking or threatening to take property without a present right to do so. Other prohibited practices are communicating about a debt via postcard and using any language or symbol on an envelope, other than an address, that indicates the communication is from a debt collector.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:10:10Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.18', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 10596, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 0.143}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means to collect a debt, and then lists non-exhaustive examples that violate it: falsely claiming government affiliation/bonding (1); misstating the character, amount, or legal status of a debt or the services or compensation involved (2); falsely implying an attorney is involved (3); threatening arrest, imprisonment, seizure, garnishment, attachment, or sale of property or wages when such action is unlawful or not intended (4); threatening any action that cannot legally be or is not intended to be taken (5); communicating credit information known to be false, including failing to note a debt is disputed (8); using documents simulating court or agency papers (9) or falsely representing documents to be, or not to be, legal process (13, 15); any false or deceptive means to collect or to obtain consumer information (10); failing to give the required 'attempting to collect a debt' disclosures (11); falsely implying accounts were sold to innocent purchasers for value (12); using a name other than the collector's true name (14); and falsely implying the collector is or works for a consumer reporting agency (16)."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use any false, deceptive, or misleading representation or means in connection with collecting a debt. The statute lists prohibited conduct including false claims about government affiliation, the debt’s character/amount/legal status, attorney involvement, legal consequences of nonpayment, threats of actions that are illegal or unintended, false credit reporting, simulated official documents, deceptive collection means, false legal-process statements, use of a non-true business name, and false claims of affiliation with a consumer reporting agency. Debt collectors also must give the required debt-collection disclosure in initial and subsequent consumer communications, with an exception for formal pleadings in legal actions.'
  - gemini-2.5-pro: grounded=True, error=None, summary="Debt collectors are broadly prohibited from using any false, deceptive, or misleading representations. This includes misrepresenting a debt's amount or status, threatening actions they cannot or do not intend to take like arrest, falsely implying they are an attorney or affiliated with the government, or using documents that look like official court papers. Collectors must also disclose in their initial communication that they are attempting to collect a debt and, in subsequent communications, that the message is from a debt collector, unless it is a formal legal pleading."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:10:10Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '10', '11', '12', '13', '14', '15', '16', '2', '3', '4', '5', '8', '9'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means to collect a debt, and then lists non-exhaustive examples that violate it: falsely claiming government affiliation/bonding (1); misstating the character, amount, or legal status of a debt or the services or compensation involved (2); falsely implying an attorney is involved (3); threatening arrest, imprisonment, seizure, garnishment, attachment, or sale of property or wages when such action is unlawful or not intended (4); threatening any action that cannot legally be or is not intended to be taken (5); communicating credit information known to be false, including failing to note a debt is disputed (8); using documents simulating court or agency papers (9) or falsely representing documents to be, or not to be, legal process (13, 15); any false or deceptive means to collect or to obtain consumer information (10); failing to give the required 'attempting to collect a debt' disclosures (11); falsely implying accounts were sold to innocent purchasers for value (12); using a name other than the collector's true name (14); and falsely implying the collector is or works for a consumer reporting agency (16)."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use any false, deceptive, or misleading representation or means in connection with collecting a debt. The statute lists prohibited conduct including false claims about government affiliation, the debt’s character/amount/legal status, attorney involvement, legal consequences of nonpayment, threats of actions that are illegal or unintended, false credit reporting, simulated official documents, deceptive collection means, false legal-process statements, use of a non-true business name, and false claims of affiliation with a consumer reporting agency. Debt collectors also must give the required debt-collection disclosure in initial and subsequent consumer communications, with an exception for formal pleadings in legal actions.'
  - gemini-2.5-pro: grounded=True, error=None, summary="Debt collectors are broadly prohibited from using any false, deceptive, or misleading representations. This includes misrepresenting a debt's amount or status, threatening actions they cannot or do not intend to take like arrest, falsely implying they are an attorney or affiliated with the government, or using documents that look like official court papers. Collectors must also disclose in their initial communication that they are attempting to collect a debt and, in subsequent communications, that the message is from a debt collector, unless it is a formal legal pleading."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:09:17Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 10596, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 0.25}}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 10596, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 0.214}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the harassment prohibition in § 1006.14(b)(1) and FDCPA § 806(5) if it places calls to a particular person about a particular debt neither more than seven times in seven consecutive days, nor within seven consecutive days after having had a telephone conversation with that person about that debt. Paragraph (b)(2)(ii) flips the presumption: exceeding either of those two frequencies creates a presumption that the collector violated (b)(1) and FDCPA § 806(5). The limits are applied per 'particular debt,' meaning each individual debt in collection, except that multiple student loan debts serviced under a single account number when obtained by the collector count as one particular debt (§ 1006.14(b)(4))."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is presumed to comply if, for a particular person and a particular debt, it does not place more than seven calls within seven consecutive days and does not call within seven consecutive days after having a telephone conversation with that person about that debt. A debt collector is presumed to violate the rule if it exceeds either of those call-frequency limits. For this purpose, a “particular debt” generally means each debt in collection, with a special rule grouping certain student loan debts serviced under one account number.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to have violated the law if they place a telephone call to a person about a particular debt more than seven times within seven consecutive days. This presumption also applies if the collector calls within seven consecutive days after having a telephone conversation with that person regarding the debt. For this rule, each debt is generally treated separately, but all student loans serviced under a single account number are treated as a single 'particular debt'."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:09:17Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '2', '7'], OpenAI=['1', '7'], Gemini=['7'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the harassment prohibition in § 1006.14(b)(1) and FDCPA § 806(5) if it places calls to a particular person about a particular debt neither more than seven times in seven consecutive days, nor within seven consecutive days after having had a telephone conversation with that person about that debt. Paragraph (b)(2)(ii) flips the presumption: exceeding either of those two frequencies creates a presumption that the collector violated (b)(1) and FDCPA § 806(5). The limits are applied per 'particular debt,' meaning each individual debt in collection, except that multiple student loan debts serviced under a single account number when obtained by the collector count as one particular debt (§ 1006.14(b)(4))."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is presumed to comply if, for a particular person and a particular debt, it does not place more than seven calls within seven consecutive days and does not call within seven consecutive days after having a telephone conversation with that person about that debt. A debt collector is presumed to violate the rule if it exceeds either of those call-frequency limits. For this purpose, a “particular debt” generally means each debt in collection, with a special rule grouping certain student loan debts serviced under one account number.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to have violated the law if they place a telephone call to a person about a particular debt more than seven times within seven consecutive days. This presumption also applies if the collector calls within seven consecutive days after having a telephone conversation with that person regarding the debt. For this rule, each debt is generally treated separately, but all student loans serviced under a single account number are treated as a single 'particular debt'."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:08:28Z

**File:** `rules/debt/federal/fcra_furnisher_dispute_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Once a furnisher receives notice from a consumer reporting agency under § 1681i(a)(2) that a consumer disputes the completeness or accuracy of information it supplied, the furnisher must investigate the disputed information, review all relevant information the agency provided with the notice, and report the investigation's results back to that agency. If the investigation shows the information is incomplete or inaccurate, the furnisher must also report those results to all other nationwide consumer reporting agencies it furnished the information to, and must promptly modify, delete, or permanently block reporting of any item found inaccurate, incomplete, or unverifiable. All of these investigations, reviews, and reports must be completed within the same time period § 1681i(a)(1) gives the credit bureau to complete its reinvestigation."
  - gpt-5.5: grounded=True, error=None, summary='After receiving notice from a consumer reporting agency that a consumer disputes the completeness or accuracy of information the person furnished, the furnisher must investigate the disputed information, review all relevant information provided by the agency, and report the investigation results back to the agency. If the information is found incomplete, inaccurate, or cannot be verified, the furnisher must take appropriate reporting action by modifying, deleting, or permanently blocking the item, and in some cases report results to other nationwide consumer reporting agencies to which it furnished the information. The furnisher must complete the required investigations, reviews, and reports within the time period that applies to the consumer reporting agency’s required actions under section 1681i(a)(1).'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [PURGE NOTE 2026-08-26] 72 entries removed -- auth-artifact run, not real disagreements

**Removed:** all 72 entries filed under `run run_20260826T171949Z` (2026-08-26 17:19-17:24 PT). Andy confirmed this run used malformed API keys (his own key-formatting error, not the runner's or the models'): all three providers returned authentication failures on every single node (Anthropic `401 invalid x-api-key`, OpenAI `401 invalid_api_key`, Gemini `400 API_KEY_INVALID`). Since every node in that run failed identically on auth, the resulting `MODEL-DISAGREEMENT` and `CITATION-CHECK-FAILED` entries filed by the runner carried no legal-content signal whatsoever -- purging them per Andy's explicit instruction, logged here (not silently) per the append-only discipline. **Entries from `run_20260826T174558Z` and `run_20260826T175559Z` (Andy's run 3, valid keys, real 200-level API responses) are untouched below** -- those are the genuine findings this queue exists to hold.

---

### [AZ-HOMESTEAD-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T18:04:32Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-33-property/az-rev-st-sect-33-1101/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/az/title-33-property/az-rev-st-sect-33-1101/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under A.R.S. § 33-1101(A), any Arizona resident aged eighteen or older, whether married or single, may hold a homestead exempt from attachment, execution, and forced sale up to $400,000 in value. The exemption covers one of the following: an interest in real property in one compact body with a dwelling house in which the person resides, an interest in a condominium or cooperative in which the person resides, a mobile home in which the person resides, or such a mobile home plus the land it sits on. Under subsection (C), the exemption (up to the same value, as adjusted by subsection D) automatically attaches to identifiable cash proceeds from a voluntary or involuntary sale of the property, and continues for eighteen months after the sale or until a new homestead is established with the proceeds, whichever is shorter.'
  - gpt-5.5: grounded=True, error=None, summary='An Arizona resident who is at least eighteen, whether married or single, may hold a homestead exempt from attachment, execution, and forced sale up to $400,000 in value. The exemption may apply to the person’s residence interest in real property with a dwelling, a condominium or cooperative, a mobile home, or a mobile home plus the land where it is located. The exemption also automatically attaches to identifiable cash proceeds from a voluntary or involuntary sale, continuing for eighteen months after sale or until a new homestead is established with the proceeds, whichever is shorter.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-HOMESTEAD-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T18:04:32Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['$400000', '1101', '33'], OpenAI=['$400000'], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under A.R.S. § 33-1101(A), any Arizona resident aged eighteen or older, whether married or single, may hold a homestead exempt from attachment, execution, and forced sale up to $400,000 in value. The exemption covers one of the following: an interest in real property in one compact body with a dwelling house in which the person resides, an interest in a condominium or cooperative in which the person resides, a mobile home in which the person resides, or such a mobile home plus the land it sits on. Under subsection (C), the exemption (up to the same value, as adjusted by subsection D) automatically attaches to identifiable cash proceeds from a voluntary or involuntary sale of the property, and continues for eighteen months after the sale or until a new homestead is established with the proceeds, whichever is shorter.'
  - gpt-5.5: grounded=True, error=None, summary='An Arizona resident who is at least eighteen, whether married or single, may hold a homestead exempt from attachment, execution, and forced sale up to $400,000 in value. The exemption may apply to the person’s residence interest in real property with a dwelling, a condominium or cooperative, a mobile home, or a mobile home plus the land where it is located. The exemption also automatically attaches to identifiable cash proceeds from a voluntary or involuntary sale, continuing for eighteen months after sale or until a new homestead is established with the proceeds, whichever is shorter.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-WAGE-GARNISHMENT-LIMIT] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T18:03:31Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-33-property/az-rev-st-sect-33-1131/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/az/title-33-property/az-rev-st-sect-33-1131/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under A.R.S. § 33-1131(B), for an ordinary (non-support) judgment such as a consumer debt, a creditor may garnish no more than the lesser of (1) 10% of the debtor's disposable earnings for the workweek, or (2) the amount by which those weekly disposable earnings exceed 60 times the applicable minimum hourly wage at the time the earnings are payable. The 'applicable minimum hourly wage' is whichever of the federal, state, or local minimum wage is highest. The only stated exception is subsection C, which applies to orders for support of a person (where one-half of disposable earnings per pay period is exempt) and thus does not govern consumer-debt judgments."
  - gpt-5.5: grounded=True, error=None, summary='Except for support orders, the maximum disposable earnings subject to process for any workweek is the lesser of: (1) ten percent of disposable earnings for that week, or (2) the amount by which that week’s disposable earnings exceed sixty times the highest applicable federal, state, or local minimum hourly wage. Support orders are treated differently, with one-half of disposable earnings for any pay period exempt from process.'
  - gemini-2.5-pro: grounded=True, error=None, summary="For a consumer debt, the maximum part of a debtor's disposable earnings that can be garnished for any workweek is the lesser of two amounts. The first amount is ten percent of the disposable earnings for that week. The second is the amount by which those disposable earnings exceed sixty times the highest applicable federal, state, or local minimum hourly wage. This cap does not apply to orders for the support of a person."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-WAGE-GARNISHMENT-LIMIT] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T18:03:31Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '10%', '1131', '2', '33', '60'], OpenAI=['1', '2'], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under A.R.S. § 33-1131(B), for an ordinary (non-support) judgment such as a consumer debt, a creditor may garnish no more than the lesser of (1) 10% of the debtor's disposable earnings for the workweek, or (2) the amount by which those weekly disposable earnings exceed 60 times the applicable minimum hourly wage at the time the earnings are payable. The 'applicable minimum hourly wage' is whichever of the federal, state, or local minimum wage is highest. The only stated exception is subsection C, which applies to orders for support of a person (where one-half of disposable earnings per pay period is exempt) and thus does not govern consumer-debt judgments."
  - gpt-5.5: grounded=True, error=None, summary='Except for support orders, the maximum disposable earnings subject to process for any workweek is the lesser of: (1) ten percent of disposable earnings for that week, or (2) the amount by which that week’s disposable earnings exceed sixty times the highest applicable federal, state, or local minimum hourly wage. Support orders are treated differently, with one-half of disposable earnings for any pay period exempt from process.'
  - gemini-2.5-pro: grounded=True, error=None, summary="For a consumer debt, the maximum part of a debtor's disposable earnings that can be garnished for any workweek is the lesser of two amounts. The first amount is ten percent of the disposable earnings for that week. The second is the amount by which those disposable earnings exceed sixty times the highest applicable federal, state, or local minimum hourly wage. This cap does not apply to orders for the support of a person."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-ORAL-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T18:02:38Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-12-courts-and-civil-proceedings/az-rev-st-sect-12-543/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under A.R.S. § 12-543, a lawsuit on a debt that is not evidenced by a written contract, or on a stated or open account, must be filed within three years after the cause of action accrues, and not afterward. For stated or open accounts, the statute adds that no item of the account is barred so long as any item on it was incurred within the three years immediately before the action is brought. The three-year period also covers claims for relief based on fraud or mistake, which do not accrue until the aggrieved party discovers the facts constituting the fraud or mistake; mutual and current merchant-to-merchant trade accounts are excluded from the open-account category.'
  - gpt-5.5: grounded=True, error=None, summary='An action for debt not evidenced by a written contract must be commenced and prosecuted within three years after the cause of action accrues. Actions on stated or open accounts are also subject to a three-year period, and no item of a stated or open account is barred if any item was incurred within the three years immediately before the action is brought.'
  - gemini-2.5-pro: grounded=True, error=None, summary='According to the provided text, a lawsuit must be started within three years after the cause of action accrues for a debt that is not based on a written contract. This three-year time limit also applies to actions on open accounts. The statute does not differentiate between consumer and other types of debt, applying this rule generally.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-ORAL-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T18:02:38Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['12', '543'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under A.R.S. § 12-543, a lawsuit on a debt that is not evidenced by a written contract, or on a stated or open account, must be filed within three years after the cause of action accrues, and not afterward. For stated or open accounts, the statute adds that no item of the account is barred so long as any item on it was incurred within the three years immediately before the action is brought. The three-year period also covers claims for relief based on fraud or mistake, which do not accrue until the aggrieved party discovers the facts constituting the fraud or mistake; mutual and current merchant-to-merchant trade accounts are excluded from the open-account category.'
  - gpt-5.5: grounded=True, error=None, summary='An action for debt not evidenced by a written contract must be commenced and prosecuted within three years after the cause of action accrues. Actions on stated or open accounts are also subject to a three-year period, and no item of a stated or open account is barred if any item was incurred within the three years immediately before the action is brought.'
  - gemini-2.5-pro: grounded=True, error=None, summary='According to the provided text, a lawsuit must be started within three years after the cause of action accrues for a debt that is not based on a written contract. This three-year time limit also applies to actions on open accounts. The statute does not differentiate between consumer and other types of debt, applying this rule generally.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-WRITTEN-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T18:01:55Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-12-courts-and-civil-proceedings/az-rev-st-sect-12-548/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/az/title-12-courts-and-civil-proceedings/az-rev-st-sect-12-548/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under A.R.S. § 12-548(A), a debt action must be filed within six years after the cause of action accrues when the debt is evidenced by or founded on a written contract executed in Arizona, or on a credit card as defined in § 13-2101(3)(a). After that six-year period, the action may not be brought. Subsection (B) adds that if another jurisdiction's limitations period conflicts with Arizona's for such a debt action, this Arizona six-year statute controls."
  - gpt-5.5: grounded=True, error=None, summary='A debt action must be commenced and prosecuted within six years after the cause of action accrues if the debt is evidenced by or founded on a written contract executed in Arizona or on a credit card. If another jurisdiction’s statute of limitations conflicts with Arizona’s for such a debt action, Arizona’s six-year statute applies.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Arizona, a lawsuit for debt must be filed within six years after the cause of action accrues. This time limit applies if the debt is based on a written contract executed within the state. The six-year limit also applies to debt founded on a credit card.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-WRITTEN-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T18:01:55Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['12', '13', '2101', '3', '548'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under A.R.S. § 12-548(A), a debt action must be filed within six years after the cause of action accrues when the debt is evidenced by or founded on a written contract executed in Arizona, or on a credit card as defined in § 13-2101(3)(a). After that six-year period, the action may not be brought. Subsection (B) adds that if another jurisdiction's limitations period conflicts with Arizona's for such a debt action, this Arizona six-year statute controls."
  - gpt-5.5: grounded=True, error=None, summary='A debt action must be commenced and prosecuted within six years after the cause of action accrues if the debt is evidenced by or founded on a written contract executed in Arizona or on a credit card. If another jurisdiction’s statute of limitations conflicts with Arizona’s for such a debt action, Arizona’s six-year statute applies.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Arizona, a lawsuit for debt must be filed within six years after the cause of action accrues. This time limit applies if the debt is based on a written contract executed within the state. The six-year limit also applies to debt founded on a credit card.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T18:01:11Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 5 of 5 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692g', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.law.cornell.edu/uscode/text/15/1692g', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 15 U.S.C. § 1692g(a) and 12 C.F.R. § 1006.34(a)(1), a notice is compliant only if the collector conveyed the required validation information — the amount of the debt, the creditor's name, the assumption-of-validity statement, the written-dispute/verification statement, and the original-creditor-request statement (plus the fuller Reg F items in § 1006.34(c)) — either in the initial communication (orally or in writing) or in a written notice sent within five days of it; a missing item or late sending defeats compliance. The dispute window runs 30 days from the consumer's receipt (or assumed receipt) of that information, and § 1006.34(b)(5) lets the collector assume receipt on any date at least five business days (excluding weekends and legal public holidays) after it provides the information, so the consumer is still timely if the written dispute is sent before that 30-day period ends. A timely written dispute (or original-creditor request) under § 1692g(b) obliges the collector to cease collection of the disputed portion until verification, a judgment copy, or the original creditor's name and address is mailed; otherwise collection may continue during the 30 days. The excerpt supplies only this standard — applying it to a particular consumer requires the actual notice content and the sending/receipt dates, which the text does not provide."
  - gpt-5.5: grounded=False, error=None, summary='A compliant validation notice must be provided in the initial communication or within five days after it, unless the required information was already in the initial communication or the consumer paid the debt. The notice/validation information must include the debt amount, creditor information, required dispute and verification statements, original-creditor request rights, and the Regulation F validation information; the dispute/validation period runs until 30 days after the consumer receives or is assumed to receive the validation information. The provided text does not state what notice was actually sent, what it contained, when it was provided, or when the consumer received it, so it is insufficient to determine whether a compliant notice was provided or whether the consumer is still within the dispute window.'
  - gemini-2.5-pro: grounded=False, error=None, summary='The provided legal texts outline the specific information a debt collector must include in a validation notice and establish that a consumer has 30 days after receiving this notice to dispute the debt. However, the texts do not contain any factual information about what notice was actually sent or when it was sent in a specific case. Therefore, it is impossible to determine from the text alone whether a compliant notice was provided or if the consumer is still within their dispute window.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T18:01:11Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '1006.34', '12', '15', '1692', '30', '5'], OpenAI=['30'], Gemini=['30'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 15 U.S.C. § 1692g(a) and 12 C.F.R. § 1006.34(a)(1), a notice is compliant only if the collector conveyed the required validation information — the amount of the debt, the creditor's name, the assumption-of-validity statement, the written-dispute/verification statement, and the original-creditor-request statement (plus the fuller Reg F items in § 1006.34(c)) — either in the initial communication (orally or in writing) or in a written notice sent within five days of it; a missing item or late sending defeats compliance. The dispute window runs 30 days from the consumer's receipt (or assumed receipt) of that information, and § 1006.34(b)(5) lets the collector assume receipt on any date at least five business days (excluding weekends and legal public holidays) after it provides the information, so the consumer is still timely if the written dispute is sent before that 30-day period ends. A timely written dispute (or original-creditor request) under § 1692g(b) obliges the collector to cease collection of the disputed portion until verification, a judgment copy, or the original creditor's name and address is mailed; otherwise collection may continue during the 30 days. The excerpt supplies only this standard — applying it to a particular consumer requires the actual notice content and the sending/receipt dates, which the text does not provide."
  - gpt-5.5: grounded=False, error=None, summary='A compliant validation notice must be provided in the initial communication or within five days after it, unless the required information was already in the initial communication or the consumer paid the debt. The notice/validation information must include the debt amount, creditor information, required dispute and verification statements, original-creditor request rights, and the Regulation F validation information; the dispute/validation period runs until 30 days after the consumer receives or is assumed to receive the validation information. The provided text does not state what notice was actually sent, what it contained, when it was provided, or when the consumer received it, so it is insufficient to determine whether a compliant notice was provided or whether the consumer is still within the dispute window.'
  - gemini-2.5-pro: grounded=False, error=None, summary='The provided legal texts outline the specific information a debt collector must include in a validation notice and establish that a consumer has 30 days after receiving this notice to dispute the debt. However, the texts do not contain any factual information about what notice was actually sent or when it was sent in a specific case. Therefore, it is impossible to determine from the text alone whether a compliant notice was provided or if the consumer is still within their dispute window.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T18:00:00Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692f', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692f imposes a general prohibition: a debt collector may not use unfair or unconscionable means to collect or attempt to collect any debt. The statute then lists non-exhaustive examples of violations, including collecting amounts (interest, fees, charges, expenses) not authorized by the debt agreement or permitted by law; accepting checks postdated more than five days without written notice of intent to deposit given 3-10 business days beforehand; soliciting postdated instruments to threaten or institute criminal prosecution; depositing or threatening to deposit a postdated instrument early; causing a person to be charged for communications by concealing the communication's true purpose; and taking or threatening nonjudicial dispossession or disablement of property where there is no present right to possession through an enforceable security interest, no present intention to take possession, or the property is exempt by law. It also bars communicating with a consumer about a debt by post card and using any language or symbol other than the collector's address on mail/telegram envelopes, though a business name may be used if it does not indicate the collection business."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect or attempt to collect a debt. The statute lists violations including collecting unauthorized amounts, improper handling or solicitation of postdated checks, causing communication charges by concealing the communication’s purpose, improper nonjudicial dispossession or disablement of property, communicating by postcard, and using prohibited language or symbols on envelopes.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector is prohibited from using any unfair or unconscionable means to collect a debt. Prohibited actions include collecting amounts not expressly authorized by the agreement or law, and misusing postdated checks by depositing them without proper notice or before their date. It is also a violation to threaten to take property without a present right to it, communicate about a debt via postcard, or use revealing language on an envelope that indicates it is from a debt collector.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T18:00:00Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['10', '1692', '3'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692f imposes a general prohibition: a debt collector may not use unfair or unconscionable means to collect or attempt to collect any debt. The statute then lists non-exhaustive examples of violations, including collecting amounts (interest, fees, charges, expenses) not authorized by the debt agreement or permitted by law; accepting checks postdated more than five days without written notice of intent to deposit given 3-10 business days beforehand; soliciting postdated instruments to threaten or institute criminal prosecution; depositing or threatening to deposit a postdated instrument early; causing a person to be charged for communications by concealing the communication's true purpose; and taking or threatening nonjudicial dispossession or disablement of property where there is no present right to possession through an enforceable security interest, no present intention to take possession, or the property is exempt by law. It also bars communicating with a consumer about a debt by post card and using any language or symbol other than the collector's address on mail/telegram envelopes, though a business name may be used if it does not indicate the collection business."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect or attempt to collect a debt. The statute lists violations including collecting unauthorized amounts, improper handling or solicitation of postdated checks, causing communication charges by concealing the communication’s purpose, improper nonjudicial dispossession or disablement of property, communicating by postcard, and using prohibited language or symbols on envelopes.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector is prohibited from using any unfair or unconscionable means to collect a debt. Prohibited actions include collecting amounts not expressly authorized by the agreement or law, and misusing postdated checks by depositing them without proper notice or before their date. It is also a violation to threaten to take property without a present right to it, communicate about a debt via postcard, or use revealing language on an envelope that indicates it is from a debt collector.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T17:59:15Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692e', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.18', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means in connection with collecting a debt, and then lists non-exhaustive examples: falsely claiming government affiliation/bonding (1); misrepresenting the character, amount, or legal status of a debt or of services rendered or compensation (2); falsely implying attorney status or attorney-sourced communications (3); threatening arrest, imprisonment, seizure, garnishment, attachment, or sale of property or wages when such action is unlawful or not intended (4); threatening any action that cannot legally be or is not intended to be taken (5); communicating credit information known or that should be known to be false, including failing to report a debt as disputed (8); simulating court/official/agency documents (9); using any false representation or deceptive means to collect a debt or obtain consumer information (10); failing to give the required debt-collector disclosures (11); falsely implying accounts were sold to innocent purchasers for value (12); falsely implying documents are (13) or are not (15) legal process; using a name other than the true business name (14); and falsely implying the collector is or works for a consumer reporting agency (16).'
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is prohibited from using any false, deceptive, or misleading representation or means in connection with collecting a debt. The listed violations include falsely implying government affiliation, misrepresenting the debt or attorney involvement, threatening unlawful or unintended actions, communicating false credit information, using fake court or agency documents, using a name other than the true name, and omitting required debt-collector disclosures. The regulation further specifies that the initial communication must state that the debt collector is attempting to collect a debt and that information obtained will be used for that purpose, later communications must state they are from a debt collector, and these disclosures are not required in a formal pleading in a legal action.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector may not use any false, deceptive, or misleading representations. Prohibited conduct includes misrepresenting the character, amount, or legal status of a debt; falsely implying an affiliation with the government or that an individual is an attorney; and threatening to take any action that cannot legally be taken or is not intended to be taken. A debt collector must also disclose in an initial communication that they are attempting to collect a debt and, in subsequent communications, must disclose that the communication is from a debt collector, unless it is a formal legal pleading.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T17:59:15Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '10', '11', '12', '13', '14', '15', '16', '1692', '2', '3', '4', '5', '8', '9'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means in connection with collecting a debt, and then lists non-exhaustive examples: falsely claiming government affiliation/bonding (1); misrepresenting the character, amount, or legal status of a debt or of services rendered or compensation (2); falsely implying attorney status or attorney-sourced communications (3); threatening arrest, imprisonment, seizure, garnishment, attachment, or sale of property or wages when such action is unlawful or not intended (4); threatening any action that cannot legally be or is not intended to be taken (5); communicating credit information known or that should be known to be false, including failing to report a debt as disputed (8); simulating court/official/agency documents (9); using any false representation or deceptive means to collect a debt or obtain consumer information (10); failing to give the required debt-collector disclosures (11); falsely implying accounts were sold to innocent purchasers for value (12); falsely implying documents are (13) or are not (15) legal process; using a name other than the true business name (14); and falsely implying the collector is or works for a consumer reporting agency (16).'
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is prohibited from using any false, deceptive, or misleading representation or means in connection with collecting a debt. The listed violations include falsely implying government affiliation, misrepresenting the debt or attorney involvement, threatening unlawful or unintended actions, communicating false credit information, using fake court or agency documents, using a name other than the true name, and omitting required debt-collector disclosures. The regulation further specifies that the initial communication must state that the debt collector is attempting to collect a debt and that information obtained will be used for that purpose, later communications must state they are from a debt collector, and these disclosures are not required in a formal pleading in a legal action.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector may not use any false, deceptive, or misleading representations. Prohibited conduct includes misrepresenting the character, amount, or legal status of a debt; falsely implying an affiliation with the government or that an individual is an attorney; and threatening to take any action that cannot legally be taken or is not intended to be taken. A debt collector must also disclose in an initial communication that they are attempting to collect a debt and, in subsequent communications, must disclose that the communication is from a debt collector, unless it is a formal legal pleading.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T17:57:44Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the harassment-by-repeated-calls prohibition (and FDCPA § 806(5)) if it calls a particular person about a particular debt neither more than seven times in seven consecutive days, nor at all within seven consecutive days after having had a telephone conversation with that person about that debt. Conversely, under (b)(2)(ii), exceeding either of those limits creates a presumption that the collector violated the rule. Section 1006.14(b)(4) clarifies that the limits apply per 'particular debt' — i.e., each of the consumer's debts in collection counted separately — except that student loan debts serviced under a single account number when obtained by the collector are treated as one particular debt."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is presumed to comply if, for a particular debt, it does not call a particular person more than seven times within seven consecutive days and does not call within seven consecutive days after having a telephone conversation with that person about that debt. A debt collector is presumed to violate the rule if it places calls in excess of either of those frequencies. “Particular debt” means each debt in collection, except that student loan debts serviced under a single account number when obtained by the collector are treated together as one particular debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to have violated the law if they place a telephone call to a person more than seven times within seven consecutive days in connection with a particular debt. It is also a presumed violation to call a person within seven days after having had a telephone conversation with them about that debt. These call frequency limits apply on a per-debt basis, although all of a consumer's student loans serviced under a single account number are considered a single debt for this purpose."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T17:57:44Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1006.14', '12', '2', '4', '5', '806'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the harassment-by-repeated-calls prohibition (and FDCPA § 806(5)) if it calls a particular person about a particular debt neither more than seven times in seven consecutive days, nor at all within seven consecutive days after having had a telephone conversation with that person about that debt. Conversely, under (b)(2)(ii), exceeding either of those limits creates a presumption that the collector violated the rule. Section 1006.14(b)(4) clarifies that the limits apply per 'particular debt' — i.e., each of the consumer's debts in collection counted separately — except that student loan debts serviced under a single account number when obtained by the collector are treated as one particular debt."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is presumed to comply if, for a particular debt, it does not call a particular person more than seven times within seven consecutive days and does not call within seven consecutive days after having a telephone conversation with that person about that debt. A debt collector is presumed to violate the rule if it places calls in excess of either of those frequencies. “Particular debt” means each debt in collection, except that student loan debts serviced under a single account number when obtained by the collector are treated together as one particular debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to have violated the law if they place a telephone call to a person more than seven times within seven consecutive days in connection with a particular debt. It is also a presumed violation to call a person within seven days after having had a telephone conversation with them about that debt. These call frequency limits apply on a per-debt basis, although all of a consumer's student loans serviced under a single account number are considered a single debt for this purpose."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T17:56:47Z

**File:** `rules/debt/federal/fcra_furnisher_dispute_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1681s-2', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.law.cornell.edu/uscode/text/15/1681s-2', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Once a furnisher receives notice from a credit reporting agency under § 1681i(a)(2) that a consumer disputes the completeness or accuracy of information it supplied, it must investigate the disputed information, review all relevant information the agency provided with the notice, and report the investigation's results back to that agency. If the investigation shows the information is incomplete or inaccurate, the furnisher must also report that to all other nationwide consumer reporting agencies it furnished the information to, and if the item is found inaccurate, incomplete, or unverifiable, it must promptly modify, delete, or permanently block reporting of that item. All of these investigations, reviews, and reports must be completed within the same time period § 1681i(a)(1) gives the consumer reporting agency to complete its own reinvestigation."
  - gpt-5.5: grounded=True, error=None, summary='After receiving notice from a consumer reporting agency of a dispute about the completeness or accuracy of information it furnished, the furnisher must investigate the disputed information, review relevant information from the agency, and report the investigation results back to the agency. If the information is incomplete, inaccurate, or cannot be verified, the furnisher must take appropriate action such as modifying, deleting, or permanently blocking reporting of the item, and must report certain results to other nationwide consumer reporting agencies to which it furnished the information. These investigations, reviews, and reports must be completed within the time period applicable to the consumer reporting agency’s required actions under section 1681i(a)(1).'
  - gemini-2.5-pro: grounded=True, error=None, summary='After receiving notice of a dispute from a consumer reporting agency, a furnisher of information must conduct an investigation, review all relevant information provided by the agency, and report the results back to that agency. If the investigation finds the information is inaccurate or incomplete, the furnisher must also report those results to all other nationwide consumer reporting agencies it uses. Finally, if information is found to be inaccurate, incomplete, or unverifiable, the furnisher must promptly modify, delete, or permanently block the reporting of that item.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T17:56:47Z

**File:** `rules/debt/federal/fcra_furnisher_dispute_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '1681', '2'], OpenAI=['1', '1681'], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Once a furnisher receives notice from a credit reporting agency under § 1681i(a)(2) that a consumer disputes the completeness or accuracy of information it supplied, it must investigate the disputed information, review all relevant information the agency provided with the notice, and report the investigation's results back to that agency. If the investigation shows the information is incomplete or inaccurate, the furnisher must also report that to all other nationwide consumer reporting agencies it furnished the information to, and if the item is found inaccurate, incomplete, or unverifiable, it must promptly modify, delete, or permanently block reporting of that item. All of these investigations, reviews, and reports must be completed within the same time period § 1681i(a)(1) gives the consumer reporting agency to complete its own reinvestigation."
  - gpt-5.5: grounded=True, error=None, summary='After receiving notice from a consumer reporting agency of a dispute about the completeness or accuracy of information it furnished, the furnisher must investigate the disputed information, review relevant information from the agency, and report the investigation results back to the agency. If the information is incomplete, inaccurate, or cannot be verified, the furnisher must take appropriate action such as modifying, deleting, or permanently blocking reporting of the item, and must report certain results to other nationwide consumer reporting agencies to which it furnished the information. These investigations, reviews, and reports must be completed within the time period applicable to the consumer reporting agency’s required actions under section 1681i(a)(1).'
  - gemini-2.5-pro: grounded=True, error=None, summary='After receiving notice of a dispute from a consumer reporting agency, a furnisher of information must conduct an investigation, review all relevant information provided by the agency, and report the results back to that agency. If the investigation finds the information is inaccurate or incomplete, the furnisher must also report those results to all other nationwide consumer reporting agencies it uses. Finally, if information is found to be inaccurate, incomplete, or unverifiable, the furnisher must promptly modify, delete, or permanently block the reporting of that item.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-ORAL-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T174558Z, 2026-08-26T17:51:57Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-12-courts-and-civil-proceedings/az-rev-st-sect-12-543/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under A.R.S. § 12-543, a lawsuit on a debt that is not evidenced by a written contract (an oral debt) or on a stated or open account must be filed within three years after the cause of action accrues, and not afterward. For stated or open accounts, the statute adds that no item of the account is barred so long as any item on that account was incurred within the three years immediately before the action is brought. An exception exists for mutual and current accounts concerning the trade of merchandise between merchants or their factors/agents, which are excluded from this open-account provision.'
  - gpt-5.5: grounded=True, error=None, summary='An action for debt not evidenced by a written contract must be commenced and prosecuted within three years after the cause of action accrues. An action on a stated or open account must also be brought within three years, and no item of the account is barred so long as any item was incurred within the three years immediately before the action is brought.'
  - gemini-2.5-pro: grounded=True, error=None, summary='According to the provided text, a lawsuit must be commenced and prosecuted within three years after the cause of action accrues. This three-year time limit applies to actions for debt where the indebtedness is not based on a contract in writing. The statute also applies this three-year limit to lawsuits based upon stated or open accounts.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-ORAL-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T174558Z, 2026-08-26T17:51:57Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['12', '543'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under A.R.S. § 12-543, a lawsuit on a debt that is not evidenced by a written contract (an oral debt) or on a stated or open account must be filed within three years after the cause of action accrues, and not afterward. For stated or open accounts, the statute adds that no item of the account is barred so long as any item on that account was incurred within the three years immediately before the action is brought. An exception exists for mutual and current accounts concerning the trade of merchandise between merchants or their factors/agents, which are excluded from this open-account provision.'
  - gpt-5.5: grounded=True, error=None, summary='An action for debt not evidenced by a written contract must be commenced and prosecuted within three years after the cause of action accrues. An action on a stated or open account must also be brought within three years, and no item of the account is barred so long as any item was incurred within the three years immediately before the action is brought.'
  - gemini-2.5-pro: grounded=True, error=None, summary='According to the provided text, a lawsuit must be commenced and prosecuted within three years after the cause of action accrues. This three-year time limit applies to actions for debt where the indebtedness is not based on a contract in writing. The statute also applies this three-year limit to lawsuits based upon stated or open accounts.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-WRITTEN-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T174558Z, 2026-08-26T17:51:13Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-12-courts-and-civil-proceedings/az-rev-st-sect-12-548/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/az/title-12-courts-and-civil-proceedings/az-rev-st-sect-12-548/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under A.R.S. § 12-548(A), a debt action must be filed within six years after the cause of action accrues if the indebtedness is evidenced by or founded on either a written contract executed in Arizona or a credit card as defined in § 13-2101(3)(a). After that six-year period, the action may not be brought. Subsection (B) adds that if another jurisdiction's limitations period for such a debt action conflicts with Arizona's, this Arizona six-year provision controls."
  - gpt-5.5: grounded=True, error=None, summary='An Arizona action for debt must be commenced and prosecuted within six years after the cause of action accrues if the debt is based on a written contract executed in Arizona or on a credit card as defined by the cited statute. If another jurisdiction has a conflicting limitations period for such a debt action, Arizona’s six-year rule applies.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Arizona, a lawsuit for debt must be commenced within six years after the cause of action accrues. This six-year statute of limitations applies if the debt is based on a written contract executed within the state. The six-year limit also applies to debts founded on a credit card.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-WRITTEN-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T174558Z, 2026-08-26T17:51:13Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['12', '13', '2101', '3', '548'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under A.R.S. § 12-548(A), a debt action must be filed within six years after the cause of action accrues if the indebtedness is evidenced by or founded on either a written contract executed in Arizona or a credit card as defined in § 13-2101(3)(a). After that six-year period, the action may not be brought. Subsection (B) adds that if another jurisdiction's limitations period for such a debt action conflicts with Arizona's, this Arizona six-year provision controls."
  - gpt-5.5: grounded=True, error=None, summary='An Arizona action for debt must be commenced and prosecuted within six years after the cause of action accrues if the debt is based on a written contract executed in Arizona or on a credit card as defined by the cited statute. If another jurisdiction has a conflicting limitations period for such a debt action, Arizona’s six-year rule applies.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Arizona, a lawsuit for debt must be commenced within six years after the cause of action accrues. This six-year statute of limitations applies if the debt is based on a written contract executed within the state. The six-year limit also applies to debts founded on a credit card.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] CITATION-CHECK-FAILED -- run run_20260826T174558Z, 2026-08-26T17:50:32Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 5 of 5 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692g', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.law.cornell.edu/uscode/text/15/1692g', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 15 U.S.C. § 1692g(a) and 12 C.F.R. § 1006.34(a)(1), a notice is compliant only if the collector conveyed the validation information in the initial communication (in writing, or orally under the regulation) or sent a written validation notice within five days of that initial communication, and the notice contained the required content: the debt amount, the creditor's name, the 30-day assumption-of-validity statement, the written-dispute/verification statement, and the original-creditor-request statement (§ 1692g(a)(1)-(5)), plus Reg F's items in § 1006.34(c) (collector communication disclosure, itemization and current amount, dispute-window end date, original-creditor right, CFPB website statement, and response prompts/addresses). The dispute window runs from the date the validation information was provided and ends 30 days after the consumer receives or is assumed to receive it; the collector may assume receipt on any date at least five days (excluding Saturdays, Sundays, and legal public holidays) after it provides the information (12 C.F.R. § 1006.34(b)(5)). If a written dispute or original-creditor request is made within that 30-day period, § 1692g(b) requires the collector to cease collection of the disputed portion until verification, a judgment copy, or the original creditor's name and address is mailed; other collection may continue during the 30 days absent a written dispute. The excerpt supplies only this framework — applying it to a particular consumer requires the specific dates and notice contents, which are not in the text."
  - gpt-5.5: grounded=False, error=None, summary='The text states that a debt collector must provide validation information in the initial communication or within five days after it, and the notice must include debt details, creditor information, dispute rights, verification/original-creditor rights, and related consumer-response information. The dispute/validation period runs for 30 days after the consumer receives or is assumed to receive the validation information, with assumed receipt permitted at least five business days after it is provided. However, the provided text does not include facts about what notice was sent, when it was provided, or when the consumer received it, so it is not possible to determine whether a compliant notice was actually provided or whether the consumer is still within the dispute window.'
  - gemini-2.5-pro: grounded=False, error=None, summary='The provided texts describe the required contents of a debt validation notice and the rules for calculating the 30-day dispute window. However, the texts do not contain any facts about a specific notice that was sent or received. Without knowing the contents of a notice and the date it was provided to the consumer, it is impossible to determine if it was compliant or if the dispute window is still open.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] MODEL-DISAGREEMENT -- run run_20260826T174558Z, 2026-08-26T17:50:32Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '1006.34', '12', '15', '1692', '30', '5'], OpenAI=['30'], Gemini=['30'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 15 U.S.C. § 1692g(a) and 12 C.F.R. § 1006.34(a)(1), a notice is compliant only if the collector conveyed the validation information in the initial communication (in writing, or orally under the regulation) or sent a written validation notice within five days of that initial communication, and the notice contained the required content: the debt amount, the creditor's name, the 30-day assumption-of-validity statement, the written-dispute/verification statement, and the original-creditor-request statement (§ 1692g(a)(1)-(5)), plus Reg F's items in § 1006.34(c) (collector communication disclosure, itemization and current amount, dispute-window end date, original-creditor right, CFPB website statement, and response prompts/addresses). The dispute window runs from the date the validation information was provided and ends 30 days after the consumer receives or is assumed to receive it; the collector may assume receipt on any date at least five days (excluding Saturdays, Sundays, and legal public holidays) after it provides the information (12 C.F.R. § 1006.34(b)(5)). If a written dispute or original-creditor request is made within that 30-day period, § 1692g(b) requires the collector to cease collection of the disputed portion until verification, a judgment copy, or the original creditor's name and address is mailed; other collection may continue during the 30 days absent a written dispute. The excerpt supplies only this framework — applying it to a particular consumer requires the specific dates and notice contents, which are not in the text."
  - gpt-5.5: grounded=False, error=None, summary='The text states that a debt collector must provide validation information in the initial communication or within five days after it, and the notice must include debt details, creditor information, dispute rights, verification/original-creditor rights, and related consumer-response information. The dispute/validation period runs for 30 days after the consumer receives or is assumed to receive the validation information, with assumed receipt permitted at least five business days after it is provided. However, the provided text does not include facts about what notice was sent, when it was provided, or when the consumer received it, so it is not possible to determine whether a compliant notice was actually provided or whether the consumer is still within the dispute window.'
  - gemini-2.5-pro: grounded=False, error=None, summary='The provided texts describe the required contents of a debt validation notice and the rules for calculating the 30-day dispute window. However, the texts do not contain any facts about a specific notice that was sent or received. Without knowing the contents of a notice and the date it was provided to the consumer, it is impossible to determine if it was compliant or if the dispute window is still open.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] CITATION-CHECK-FAILED -- run run_20260826T174558Z, 2026-08-26T17:49:32Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692f', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692f imposes a general ban on a debt collector using any unfair or unconscionable means to collect or attempt to collect a debt, then lists specific non-exhaustive examples of violations. These include: collecting amounts (interest, fees, charges, expenses) not expressly authorized by the debt agreement or permitted by law; accepting a check postdated more than five days without written notice of intent to deposit sent 3-10 business days beforehand; soliciting postdated instruments to threaten or institute criminal prosecution; depositing or threatening to deposit a postdated instrument early; causing a person to incur communication charges by concealing the communication's true purpose; taking or threatening nonjudicial dispossession or disablement of property where there is no present enforceable right or intent to take possession, or the property is exempt; communicating with a consumer about a debt by post card; and using any language or symbol other than the collector's address on mail envelopes or telegrams (a business name may be used only if it does not indicate the debt collection business). Because the list is expressly stated 'without limiting the general application of the foregoing,' conduct beyond these eight items can still violate the section."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect or attempt to collect a debt. The statute lists violations including collecting unauthorized amounts, certain improper handling or solicitation of postdated payment instruments, causing communication charges by concealing the communication’s true purpose, improper nonjudicial repossession or disablement actions, communicating about a debt by postcard, and using prohibited language or symbols on mailed envelopes or telegrams.'
  - gemini-2.5-pro: grounded=True, error=None, summary='Unfair or unconscionable debt collection practices include collecting any amount, such as interest or fees, not expressly authorized by the agreement or law. The statute also prohibits various misuses of postdated checks, such as depositing them early or soliciting them to threaten criminal prosecution. Additionally, debt collectors cannot threaten to take property if they have no right or intent to do so, communicate about a debt via postcard, or use revealing language on an envelope.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] MODEL-DISAGREEMENT -- run run_20260826T174558Z, 2026-08-26T17:49:32Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['10', '1692', '3'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692f imposes a general ban on a debt collector using any unfair or unconscionable means to collect or attempt to collect a debt, then lists specific non-exhaustive examples of violations. These include: collecting amounts (interest, fees, charges, expenses) not expressly authorized by the debt agreement or permitted by law; accepting a check postdated more than five days without written notice of intent to deposit sent 3-10 business days beforehand; soliciting postdated instruments to threaten or institute criminal prosecution; depositing or threatening to deposit a postdated instrument early; causing a person to incur communication charges by concealing the communication's true purpose; taking or threatening nonjudicial dispossession or disablement of property where there is no present enforceable right or intent to take possession, or the property is exempt; communicating with a consumer about a debt by post card; and using any language or symbol other than the collector's address on mail envelopes or telegrams (a business name may be used only if it does not indicate the debt collection business). Because the list is expressly stated 'without limiting the general application of the foregoing,' conduct beyond these eight items can still violate the section."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect or attempt to collect a debt. The statute lists violations including collecting unauthorized amounts, certain improper handling or solicitation of postdated payment instruments, causing communication charges by concealing the communication’s true purpose, improper nonjudicial repossession or disablement actions, communicating about a debt by postcard, and using prohibited language or symbols on mailed envelopes or telegrams.'
  - gemini-2.5-pro: grounded=True, error=None, summary='Unfair or unconscionable debt collection practices include collecting any amount, such as interest or fees, not expressly authorized by the agreement or law. The statute also prohibits various misuses of postdated checks, such as depositing them early or soliciting them to threaten criminal prosecution. Additionally, debt collectors cannot threaten to take property if they have no right or intent to do so, communicate about a debt via postcard, or use revealing language on an envelope.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] CITATION-CHECK-FAILED -- run run_20260826T174558Z, 2026-08-26T17:48:46Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692e', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.18', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means in connection with collecting a debt, and then lists specific violations without limiting that general rule. These include falsely implying government affiliation or that the collector is a consumer reporting agency; misrepresenting the character, amount, or legal status of a debt or the services/compensation involved; falsely implying a person is an attorney or a communication is from one; threatening arrest, imprisonment, seizure, garnishment, attachment, or sale unless lawful and actually intended; threatening any action that cannot legally be taken or is not intended; communicating known-false credit information (including failing to note a debt is disputed); simulating court or agency documents; falsely claiming documents are or are not legal process; claiming accounts went to innocent purchasers for value; using a name other than the collector's true name; and using any false representation or deceptive means to collect a debt or obtain consumer information. Paragraph (11) requires the 'mini-Miranda' disclosure, whose current operative form is 12 C.F.R. § 1006.18(e): the initial communication must state the collector is attempting to collect a debt and that information obtained will be used for that purpose (repeated in the initial written communication if the first contact was oral), each subsequent communication must disclose that it is from a debt collector, and neither disclosure is required in a formal pleading made in connection with a legal action."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use false, deceptive, or misleading representations or means in connection with collecting a debt. The statute lists prohibited conduct including misrepresenting government affiliation, the character/amount/legal status of a debt, attorney involvement, legal consequences of nonpayment, threats of unlawful or unintended action, false credit reporting, fake court/agency documents, false or deceptive collection means, use of a name other than the true name, and false implications about legal process or consumer reporting agency status. The regulation also requires debt collectors to make the initial and subsequent debt-collector disclosures, with an exception for formal pleadings in legal actions.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector is broadly prohibited from using any false, deceptive, or misleading representation when collecting a debt. This includes falsely representing the character, amount, or legal status of a debt, or falsely implying an affiliation with the government or that an individual is an attorney. It is also a violation to threaten any action that cannot legally be taken or is not intended to be taken, or to fail to disclose in communications that the communication is from a debt collector attempting to collect a debt.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] MODEL-DISAGREEMENT -- run run_20260826T174558Z, 2026-08-26T17:48:46Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1006.18', '11', '12', '1692'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means in connection with collecting a debt, and then lists specific violations without limiting that general rule. These include falsely implying government affiliation or that the collector is a consumer reporting agency; misrepresenting the character, amount, or legal status of a debt or the services/compensation involved; falsely implying a person is an attorney or a communication is from one; threatening arrest, imprisonment, seizure, garnishment, attachment, or sale unless lawful and actually intended; threatening any action that cannot legally be taken or is not intended; communicating known-false credit information (including failing to note a debt is disputed); simulating court or agency documents; falsely claiming documents are or are not legal process; claiming accounts went to innocent purchasers for value; using a name other than the collector's true name; and using any false representation or deceptive means to collect a debt or obtain consumer information. Paragraph (11) requires the 'mini-Miranda' disclosure, whose current operative form is 12 C.F.R. § 1006.18(e): the initial communication must state the collector is attempting to collect a debt and that information obtained will be used for that purpose (repeated in the initial written communication if the first contact was oral), each subsequent communication must disclose that it is from a debt collector, and neither disclosure is required in a formal pleading made in connection with a legal action."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use false, deceptive, or misleading representations or means in connection with collecting a debt. The statute lists prohibited conduct including misrepresenting government affiliation, the character/amount/legal status of a debt, attorney involvement, legal consequences of nonpayment, threats of unlawful or unintended action, false credit reporting, fake court/agency documents, false or deceptive collection means, use of a name other than the true name, and false implications about legal process or consumer reporting agency status. The regulation also requires debt collectors to make the initial and subsequent debt-collector disclosures, with an exception for formal pleadings in legal actions.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector is broadly prohibited from using any false, deceptive, or misleading representation when collecting a debt. This includes falsely representing the character, amount, or legal status of a debt, or falsely implying an affiliation with the government or that an individual is an attorney. It is also a violation to threaten any action that cannot legally be taken or is not intended to be taken, or to fail to disclose in communications that the communication is from a debt collector attempting to collect a debt.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] CITATION-CHECK-FAILED -- run run_20260826T174558Z, 2026-08-26T17:47:52Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the prohibition on repeated/continuous calls (and FDCPA § 806(5)) if, as to a particular person and a particular debt, it places no more than seven calls within seven consecutive days and does not call within seven consecutive days after having had a telephone conversation with that person about that debt. Conversely, under (b)(2)(ii), exceeding either of those frequencies creates a presumption that the collector violated the rule and FDCPA § 806(5). The limits are applied per 'particular debt,' which § 1006.14(b)(4) defines as each of a consumer's debts in collection, except that all student loan debts serviced under a single account number when obtained by the collector count as one particular debt."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is presumed to comply if, for a particular person and a particular debt, it does not place more than seven calls within seven consecutive days and does not call within seven consecutive days after having a telephone conversation with that person about that debt. A debt collector is presumed to violate the rule if it exceeds either of those call-frequency limits. For these purposes, a “particular debt” generally means each debt in collection, except that certain student loan debts serviced under one account number are treated together as one particular debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to have violated the law if they call a person about a particular debt more than seven times within seven consecutive days. It is also a presumed violation for a debt collector to place a call within seven consecutive days after having had a telephone conversation with that person about the debt. These frequency limits apply to each of a consumer's individual debts, although multiple student loans serviced under a single account number are treated as one debt."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] MODEL-DISAGREEMENT -- run run_20260826T174558Z, 2026-08-26T17:47:52Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1006.14', '12', '2', '4', '5', '806'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the prohibition on repeated/continuous calls (and FDCPA § 806(5)) if, as to a particular person and a particular debt, it places no more than seven calls within seven consecutive days and does not call within seven consecutive days after having had a telephone conversation with that person about that debt. Conversely, under (b)(2)(ii), exceeding either of those frequencies creates a presumption that the collector violated the rule and FDCPA § 806(5). The limits are applied per 'particular debt,' which § 1006.14(b)(4) defines as each of a consumer's debts in collection, except that all student loan debts serviced under a single account number when obtained by the collector count as one particular debt."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is presumed to comply if, for a particular person and a particular debt, it does not place more than seven calls within seven consecutive days and does not call within seven consecutive days after having a telephone conversation with that person about that debt. A debt collector is presumed to violate the rule if it exceeds either of those call-frequency limits. For these purposes, a “particular debt” generally means each debt in collection, except that certain student loan debts serviced under one account number are treated together as one particular debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to have violated the law if they call a person about a particular debt more than seven times within seven consecutive days. It is also a presumed violation for a debt collector to place a call within seven consecutive days after having had a telephone conversation with that person about the debt. These frequency limits apply to each of a consumer's individual debts, although multiple student loans serviced under a single account number are treated as one debt."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b] CITATION-CHECK-FAILED -- run run_20260826T174558Z, 2026-08-26T17:47:02Z

**File:** `rules/debt/federal/fcra_furnisher_dispute_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1681s-2', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.law.cornell.edu/uscode/text/15/1681s-2', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 15 U.S.C. § 1681s-2(b)(1), a furnisher's duties are triggered only once it receives notice of the dispute from the consumer reporting agency under § 1681i(a)(2) (not from the consumer directly). Upon that notice, the furnisher must investigate the disputed information, review all relevant information the CRA supplied, and report the investigation's results back to the CRA; if the information is found incomplete or inaccurate, it must also report those results to all other nationwide CRAs to which it furnished the information. If the disputed item is found inaccurate or incomplete, or cannot be verified, the furnisher must promptly modify, delete, or permanently block reporting of that item. Under § 1681s-2(b)(2), all of these investigations, reviews, and reports must be completed within the same time period the CRA has to complete its reinvestigation under § 1681i(a)(1)."
  - gpt-5.5: grounded=True, error=None, summary='After receiving notice from a consumer reporting agency of a dispute about the completeness or accuracy of information the person furnished, the furnisher must investigate the disputed information, review all relevant information provided by the agency, and report the investigation results back to the agency. If the information is found incomplete, inaccurate, or cannot be verified, the furnisher must, as appropriate, promptly modify, delete, or permanently block reporting of the item, and must report certain incomplete or inaccurate results to other nationwide consumer reporting agencies to which it furnished the information. The furnisher must complete the required investigations, reviews, and reports before the deadline by which the consumer reporting agency must complete its related actions.'
  - gemini-2.5-pro: grounded=True, error=None, summary="After receiving notice of a dispute from a consumer reporting agency, the furnisher of the information must conduct an investigation and report the results back to that agency. If the investigation finds the information is incomplete or inaccurate, the furnisher must also report those results to all other nationwide consumer reporting agencies. The furnisher must then promptly modify, delete, or permanently block the reporting of any information found to be inaccurate, incomplete, or unverifiable. These actions must all be completed before the credit bureau's own deadline to complete its investigation expires."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b] MODEL-DISAGREEMENT -- run run_20260826T174558Z, 2026-08-26T17:47:02Z

**File:** `rules/debt/federal/fcra_furnisher_dispute_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '15', '1681', '2'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 15 U.S.C. § 1681s-2(b)(1), a furnisher's duties are triggered only once it receives notice of the dispute from the consumer reporting agency under § 1681i(a)(2) (not from the consumer directly). Upon that notice, the furnisher must investigate the disputed information, review all relevant information the CRA supplied, and report the investigation's results back to the CRA; if the information is found incomplete or inaccurate, it must also report those results to all other nationwide CRAs to which it furnished the information. If the disputed item is found inaccurate or incomplete, or cannot be verified, the furnisher must promptly modify, delete, or permanently block reporting of that item. Under § 1681s-2(b)(2), all of these investigations, reviews, and reports must be completed within the same time period the CRA has to complete its reinvestigation under § 1681i(a)(1)."
  - gpt-5.5: grounded=True, error=None, summary='After receiving notice from a consumer reporting agency of a dispute about the completeness or accuracy of information the person furnished, the furnisher must investigate the disputed information, review all relevant information provided by the agency, and report the investigation results back to the agency. If the information is found incomplete, inaccurate, or cannot be verified, the furnisher must, as appropriate, promptly modify, delete, or permanently block reporting of the item, and must report certain incomplete or inaccurate results to other nationwide consumer reporting agencies to which it furnished the information. The furnisher must complete the required investigations, reviews, and reports before the deadline by which the consumer reporting agency must complete its related actions.'
  - gemini-2.5-pro: grounded=True, error=None, summary="After receiving notice of a dispute from a consumer reporting agency, the furnisher of the information must conduct an investigation and report the results back to that agency. If the investigation finds the information is incomplete or inaccurate, the furnisher must also report those results to all other nationwide consumer reporting agencies. The furnisher must then promptly modify, delete, or permanently block the reporting of any information found to be inaccurate, incomplete, or unverifiable. These actions must all be completed before the credit bureau's own deadline to complete its investigation expires."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


