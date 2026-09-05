# DEBT_COUNSEL_QUEUE_V1 -- every open GLOSS-FOR-COUNSEL item in debt-demo-v1.0

*Prepared 2026-09-05 under the LOCK directive, Phase LOCK item 3. Packaging only; nothing here is resolved.
Copyright 2026 Andrew M Cohen. Apache 2.0.*

**What this is.** Every proposition in the 19 frozen v1.0 nodes that rests on CASE LAW or practice rather than
on a quoted, live-verified statutory or regulatory text. Each was encoded as a `source_tier` C note during
rounds 38-46 and carries a GLOSS-FOR-COUNSEL classification in `rules/debt/validation/stage_b_dispositions.json`.
Items from round 38's original list of 11 that were later anchored to a quoted primary text (TransUnion,
Rotkiske, Texas temporary absence under Prop. Code 41.003, turnover of paid wages under CPRC 31.0025,
Rosenthal reach under Civ. Code 1788.2/1788.17) are NOT here -- they dropped off the counsel list in round 39.

**How to use it.** One ruling per item: **CONFIRM** (the proposition stands as encoded; the note is re-tagged
`counsel_confirmed` in v1.1), **STRIKE** (remove the proposition; the node reverts to "not encoded, refer"),
or **MODIFY** (write the corrected proposition in the box; it is encoded in v1.1). Because v1.0 is frozen, no
ruling changes v1.0 content; rulings are applied in the v1.1 content round that precedes tier promotion
(Phase LOCK item 5). Case citations are as recorded in the notes; none was fetched and read in full by Cowork
-- that is part of what a CONFIRM means.

**Risk posture key.** *If wrong, direction:* **DD** = the encoded proposition, if wrong, would tell a consumer
they are safe / have no claim / are out of time; **OC** = overstates the consumer's claim or protection (a
lawyer would catch it before filing); **N** = neutral / procedural.

**Count:** 26 items. Federal 9 · California 9 · Texas 8. Estimated session: 2-3 hours with Claude.

---

## FEDERAL

### F-1 · FDCPA-UNFAIR-PRACTICES-CATALOG-1692f · Envelope-marking rule (round 38, ledger -02)
**Encoded proposition.** Catalog item (8) -- any language or symbol on an envelope other than the collector's
address and, if not indicating collection, its business name -- is stated as the rule, with a caveat that the
Eighth Circuit reads a "benign language" exception into 1692f(8) (*Strand v. Diversified Collection Service*,
380 F.3d 316 (8th Cir. 2004)) while the Third Circuit applies the text literally (*Douglass v. Convergent
Outsourcing*, 765 F.3d 299 (3d Cir. 2014)), and that after *TransUnion* a bare visible account number may not
support Article III standing. The note also cites *Daubert v. NRA Group*, 861 F.3d 382 (3d Cir. 2017), with
*Douglass*.
**Authority relied on.** 15 U.S.C. 1692f(8) (quoted, verified); *Douglass*; *Daubert*; *Strand*; *TransUnion
v. Ramirez* (quoted syllabus).
**If wrong, direction:** OC (Third Circuit reading encoded as the default).
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### F-2 · FDCPA-UNFAIR-PRACTICES-CATALOG-1692f · Pay-to-pay / convenience fees (round 38, ledger -03)
**Encoded proposition.** Catalog item (1) (collection of any amount not expressly authorized by the agreement
or permitted by law) is caveated: courts are split on whether an optional, separately-agreed "convenience
fee" for paying by card or phone is an "amount ... incidental to the principal obligation" barred by
1692f(1); the node does not present it as a categorical violation and asks whether the fee was optional,
disclosed, and agreed at payment. The note names no case. For the session: the Fourth Circuit's *Alexander
v. Carrington Mortgage Services*, 23 F.4th 370 (4th Cir. 2022) (covered), and the CFPB's June 2022 advisory
opinion on pay-to-pay fees (covered; agency guidance) are the usual authorities on the "yes" side.
**Authority relied on.** 15 U.S.C. 1692f(1) (quoted); the split is asserted in the note without citation.
**If wrong, direction:** OC.
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### F-3 · FDCPA-UNFAIR-PRACTICES-CATALOG-1692f · Discharged-debt collection and the FDCPA (round 46, ledger -05)
**Encoded proposition.** Collecting a debt discharged in bankruptcy violates the discharge injunction (11
U.S.C. 524(a)(2), quoted), enforced by contempt in the bankruptcy court; whether the same conduct ALSO supports
an FDCPA claim is a circuit split -- the Ninth Circuit holds the Bankruptcy Code precludes it (*Walls v. Wells
Fargo Bank*, 276 F.3d 502 (9th Cir. 2002)), the Third and Seventh allow it (*Simon v. FIA Card Services*, 732
F.3d 259 (3d Cir. 2013); *Randolph v. IMBS*, 368 F.3d 726 (7th Cir. 2004)). A California consumer is routed to
the bankruptcy court; a Texas consumer is flagged "unsettled."
**Authority relied on.** 524(a)(2) (quoted); the three cases named.
**If wrong, direction:** DD for California if *Walls* has been narrowed or abrogated (consumer told she has no
FDCPA claim when she does).
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### F-4 · FDCPA-UNFAIR-PRACTICES-CATALOG-1692f · Time-barred debt: revival-misrepresentation theory (round 46, in time_barred_debt_note)
**Encoded proposition.** Collecting a time-barred debt by letter or call is not itself unfair (*Midland Funding
v. Johnson*, 581 U.S. 224 (2017), on proofs of claim; 12 CFR 1006.26(b), quoted, bars only suit or threat of
suit). A collection letter that invites a partial payment without disclosing that payment may revive the
limitations period under state law is a 1692e misrepresentation (*Buchanan v. Northland Group*, 776 F.3d 393
(6th Cir. 2015); *Pantoja v. Portfolio Recovery Associates*, 852 F.3d 679 (7th Cir. 2017)).
**Authority relied on.** 1006.26(b) (quoted); *Midland Funding*; *Buchanan*; *Pantoja*.
**If wrong, direction:** OC on the revival theory; DD if the Midland framing is read too broadly (a consumer
told "no claim" where a letter did misrepresent enforceability).
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### F-5 · FDCPA-UNFAIR-PRACTICES-CATALOG-1692f · Breach of the peace on self-help repossession (round 46, ledger -06)
**Encoded proposition.** Catalog item (6) (nonjudicial action to dispossess where there is no present right to
possession) is read to include a repossession carried out in breach of the peace -- lock cut, closed
garage or fenced yard entered, debtor's contemporaneous objection overridden, force used -- because UCC
9-609(b)(2) conditions the self-help right on proceeding without breach of the peace. The state enactments
are NAMED, not quoted.
**Authority relied on.** 1692f(6) (quoted); UCC 9-609(b)(2) as enacted (Cal. Com. Code 9609; Tex. Bus. & Com.
Code 9.609), named.
**If wrong, direction:** OC (a breach-of-the-peace repossession may be a state-law claim without being a
1692f(6) violation -- courts differ on whether "present right to possession" is lost by the manner of taking).
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### F-6 · FDCPA-FALSE-DECEPTIVE-CATALOG-1692e · Accurate-but-misleading static balance (round 46, ledger -05)
**Encoded proposition.** Stating a "current balance" on an account where interest or fees are accruing, without
saying so, can be a 1692e misrepresentation to the least sophisticated consumer (*Avila v. Riexinger &
Associates*, 817 F.3d 72 (2d Cir. 2016), with its safe-harbor language); no violation where nothing is in fact
accruing (*Taylor v. Financial Recovery Services*, 886 F.3d 212 (2d Cir. 2018); *Chuway v. National Action
Financial Services*, 362 F.3d 944 (7th Cir. 2004), on the other side of the ledger). Encoded as a screening
question, not a rule.
**Authority relied on.** 1692e(2)(A) (quoted); the three cases named.
**If wrong, direction:** OC.
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### F-7 · FDCPA-FALSE-DECEPTIVE-CATALOG-1692e · Scope of the bona fide error defense (round 46, ledger -06)
**Encoded proposition.** 15 U.S.C. 1692k(c) (quoted) is a complete defense on the collector's proof of an
unintentional violation resulting from a bona fide error despite procedures reasonably adapted to avoid it;
it reaches clerical and factual errors, not mistakes of law about what the FDCPA requires (*Jerman v.
Carlisle, McNellie, Rini, Kramer & Ulrich*, 559 U.S. 573 (2010)).
**Authority relied on.** 1692k(c) (quoted); *Jerman*.
**If wrong, direction:** N (a consumer is still told the violation occurred; only the recovery caveat changes).
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### F-8 · FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6 · Government-origin consumer obligations as "debts" (round 43, ledger -06)
**Encoded proposition.** A municipal water/sewer account, a public-hospital or city ambulance bill, or public
tuition is a "debt" under 1692a(5) when a third party collects it, because the obligation arises from a
consumer transaction; fines, taxes, and non-consensual assessments are not (*Pollice v. National Tax Funding*,
225 F.3d 379 (3d Cir. 2000) -- water/sewer yes, taxes no; *Piper v. Portnoff Law Associates*, 396 F.3d 227
(3d Cir. 2005)).
**Authority relied on.** 1692a(5) (quoted); *Pollice*; *Piper*.
**If wrong, direction:** OC (a consumer told she has a claim on a municipal obligation a court treats as non-transactional).
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### F-9 · FDCPA-REGF-CALL-FREQUENCY-1006.14b · One-year limitations period runs per call, from the call (round 46, in temporal_screen_note)
**Encoded proposition.** The 1692k(d) year (quoted) runs from each violation, not from discovery (*Rotkiske v.
Klemm*, 589 U.S. 8 (2019), quoted on the 1692e node), so a call pattern older than a year supports no private
federal claim; state statutes (Rosenthal, Tex. Fin. Code ch. 392) may carry longer periods. The Rosenthal
period is stated as one year under Civ. Code 1788.30(f) -- NAMED, not fetched.
**Authority relied on.** 1692k(d) (quoted); *Rotkiske* (quoted); Civ. Code 1788.30(f) (named).
**If wrong, direction:** DD if a longer state period exists and the node says "gone."
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

---

## CALIFORNIA

### C-1 · CA-SOL-WRITTEN-CONTRACT-DEBT · Contractual choice-of-law clauses and CCP 361 (round 38, ledger -01)
**Encoded proposition.** Two independent routes can shorten the four-year period for a card debt: (i) CCP 361
(quoted) -- a claim that arose in another state and is barred there is barred here (subject to the
California-citizen exception); (ii) a contractual choice-of-law clause selecting a state with a shorter
period, which California courts enforce for limitations purposes when the clause is broad enough
(*Resurgence Financial, LLC v. Chambers*, 173 Cal. App. 4th Supp. 1 (2009), applying Delaware's three years).
Both are asked; neither is applied automatically.
**Authority relied on.** CCP 361 (quoted); *Resurgence*.
**If wrong, direction:** DD if a shorter period actually applies and the node says four years; OC if
*Resurgence* is read too broadly.
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### C-2 · CA-SOL-WRITTEN-CONTRACT-DEBT · CCP 351 absence tolling, constitutionality (round 38, ledger -03)
**Encoded proposition.** CCP 351 (quoted) tolls limitations while the defendant is out of state, but the
tolling is likely unconstitutional as applied to a defendant whose absence was interstate travel or commerce
(Commerce Clause: *Abramson v. Brownstein*, 897 F.2d 389 (9th Cir. 1990); *Heritage Marketing & Insurance
Services v. Chrustawka*, 160 Cal. App. 4th 754 (2008)); encoded as a caveat, and the node does not add
absence days to the deadline automatically.
**Authority relied on.** CCP 351 (quoted); *Abramson*; *Heritage*.
**If wrong, direction:** DD (a creditor relying on 351 tolling could be timely where the node said expired).
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### C-3 · CA-SOL-WRITTEN-CONTRACT-DEBT · Sister-state judgments must be enforceable where rendered (round 43, ledger -07)
**Encoded proposition.** A sister-state judgment can be entered under the Sister State Money-Judgments Act
(CCP 1710.10 et seq., named) only if it remains enforceable under the rendering state's law (e.g., a Texas
judgment dormant under CPRC 34.001 with no revival under 31.006 -- both quoted); the California action on a
sister-state judgment has its own ten years under CCP 337.5(b) (quoted). The enforceable-where-rendered
requirement rests on full-faith-and-credit case law, not a quoted text; the 1710.40 motion to vacate is the
vehicle.
**Authority relied on.** 337.5(b), 34.001, 31.006 (quoted); 1710.10-1710.40 (named); full-faith-and-credit
doctrine (unnamed cases).
**If wrong, direction:** DD if California entertains a judgment that is dormant elsewhere.
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### C-4 · CA-SOL-WRITTEN-CONTRACT-DEBT · CCP 366.2 and a timely probate creditor's claim (round 43, in deceased_debtor_note)
**Encoded proposition.** The one-year-from-death bar (366.2, quoted) is not tolled except through the Probate
Code creditor-claim procedures listed in 366.2(b); the interaction with a timely-filed claim (Prob. Code 9100,
9352) is flagged, not encoded.
**Authority relied on.** 366.2(a)-(b) (quoted); Prob. Code 9000 et seq. (named).
**If wrong, direction:** DD if a filed claim keeps the action alive and the node says barred.
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### C-5 · CA-SOL-ORAL-CONTRACT-DEBT / CA-SOL-WRITTEN · Installment obligations accrue per installment (round 38, ledger ORAL -03; WRITTEN note)
**Encoded proposition.** Where an obligation is payable in installments and the creditor never accelerated,
limitations runs separately from each missed installment; the node asks whether acceleration occurred and
does not compute a single bar date for an un-accelerated installment contract.
**Authority relied on.** General California contract-limitations case law (no single case cited in the note).
**If wrong, direction:** partial -- DD for the oldest installments if the rule is stated too generously to
the debtor; OC otherwise.
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### C-6 · CA-SOL-ORAL-CONTRACT-DEBT · Accrual of a demand loan / loan with no repayment date (round 46, ledger -04)
**Encoded proposition.** A loan with no time fixed for repayment is payable on demand or within a reasonable
time (Civ. Code 1657, named); for a demand loan, accrual is at the making of the loan or, at the latest, at
demand and refusal, and a lender cannot postpone accrual indefinitely by never demanding. Encoded as a
screening question, not a computed rule.
**Authority relied on.** Civ. Code 1657 (named); case law unnamed.
**If wrong, direction:** varies -- DD if accrual is really at demand and the node's "at the loan" branch says expired.
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### C-7 · CA-BANK-ACCOUNT-EXEMPTION · Bank setoff vs. levy; Financial Code 864 (round 46, ledger -04)
**Encoded proposition.** The 704.220 minimum protects deposits from a JUDGMENT LEVY (CCP 703.010 limits the
chapter to enforcement of money judgments, named) and does not govern the depositary bank's own setoff; setoff
against a consumer deposit account is limited by Fin. Code 864 (named) -- a floor below which the bank may
not set off, notice, and a bar on setting off against directly-deposited public benefits and Social Security.
The current 864 figures and whether a violating setoff supports damages are not stated.
**Authority relied on.** 703.010, Fin. Code 864 (both named, not quoted).
**If wrong, direction:** DD (a swept account treated as unprotected when 864 gives a remedy).
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### C-8 · CA-BANK-ACCOUNT-EXEMPTION · Non-debtor spouse's account and Fam. Code 910/911 (round 46, ledger -06)
**Encoded proposition.** Community property -- including the debtor spouse's wages deposited in an account
in the non-debtor spouse's sole name -- is liable for a debt incurred by either spouse during marriage
(Fam. Code 910, named); the non-debtor spouse's own earnings are shielded from the other spouse's PREMARITAL
debts if kept in an account the debtor spouse cannot withdraw from (911, named); the 720.110 third-party
claim is not the first answer for a spouse. 703.020(b)(2) lets the spouse claim community exemptions.
**Authority relied on.** Fam. Code 910, 911 (named); CCP 703.020 (quoted on the vehicle node, (b)(2) named).
**If wrong, direction:** OC (overstates creditor reach) if 910 is narrower than stated.
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### C-9 · CA-HOMESTEAD-EXEMPTION · Temporary absence vs. loss of continuous residence (round 46, in continuous_residence_requirement_note)
**Encoded proposition.** 704.710(c) (quoted) requires residence at lien attachment and continuously
thereafter; a relocation, move to a relative's home, or entry into assisted living with the house rented out
defeats the automatic homestead, while short, temporary absences (hospitalization, brief deployment) are
tolerated by case law. A recorded DECLARED homestead (704.910 et seq., named) is treated differently and is not
encoded.
**Authority relied on.** 704.710(c) (quoted); case law on temporary absence (unnamed); 704.910 (named).
**If wrong, direction:** DD if the tolerance for absence is broader than stated (a debtor told the exemption is lost when it is not).
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

---

## TEXAS

### T-1 · TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY · Restricted appeal and bill of review scope (round 38, ledger -02)
**Encoded proposition.** A restricted appeal (Tex. R. App. P. 30, named) within six months and a bill of
review (four years) are not limited to defective-service cases; a restricted appeal reaches any error apparent
on the face of the record, and a bill of review reaches extrinsic fraud, official mistake, or lack of service,
each with its own showing. *Peralta v. Heights Medical Center*, 485 U.S. 80 (1988), for the no-service case.
**Authority relied on.** TRAP 30 (named); *Peralta*; bill-of-review case law (unnamed).
**If wrong, direction:** DD if a route is overstated (a defendant sent down a path that is closed).
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### T-2 · TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY · Justice court: no 306a restart, no restricted appeal; bill of review (round 46, ledger -04)
**Encoded proposition.** The general Rules of Civil Procedure apply in justice court only when the judge so
orders or a rule says so (TRCP 500.3(e), named), so TRCP 306a's late-notice restart does not apply; the
restricted appeal lies only from district and county court judgments; a justice-court defendant who learns of
the judgment after the 14-day motion and 21-day de novo appeal windows is left with equitable relief, and
whether and where a bill of review lies from a justice-court judgment is flagged for counsel.
**Authority relied on.** TRCP 500.3(e) (named); TRCP 505.3 and 506.1(a) (quoted); TRAP 30 (named).
**If wrong, direction:** DD (a justice-court defendant told both windows are closed when a restart exists).
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### T-3 · TX-SOL-CONSUMER-DEBT · Diligence in service after timely filing (round 46, ledger -05)
**Encoded proposition.** Limitations is measured to the FILING date (CPRC 16.004(a), quoted), provided the
plaintiff then exercises diligence in obtaining service; a long, unexplained gap between filing and service can
forfeit the filing date. Stated as a caveat; not computed.
**Authority relied on.** 16.004(a) (quoted); diligence-in-service case law (unnamed).
**If wrong, direction:** OC (the node defaults to "timely if filed in time").
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### T-4 · TX-SOL-CONSUMER-DEBT · Choice-of-law clauses and limitations (round 46, ledger -06)
**Encoded proposition.** Texas has no general borrowing statute for contract claims (the Stage B finding's
citation to CPRC 16.066 was checked and is the foreign-judgment rule); Texas courts traditionally treat
limitations as procedural and apply Texas's four years despite a substantive choice-of-law clause, though some
courts apply the chosen state's shorter period where the clause expressly reaches limitations. Encoded as:
default to four years, flag the clause, refer.
**Authority relied on.** 16.066(a)-(b) (quoted, for what it is NOT); procedural/substantive case law (unnamed).
**If wrong, direction:** DD if a shorter chosen-state period applies and the node says four years.
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### T-5 · TX-SOL-CONSUMER-DEBT · Accrual date on a revolving account (round 46, ledger -07)
**Encoded proposition.** On a credit card, limitations accrues at default/acceleration (charge-off or demand
for the full balance), not at the last payment; some courts fix it at the first missed payment. The node
collects all three dates and computes from each rather than choosing.
**Authority relied on.** 16.004(a) (quoted); accrual case law (unnamed).
**If wrong, direction:** DD if accrual is really at the first missed payment and the node's charge-off branch says timely.
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### T-6 · TX-SOL-CONSUMER-DEBT · Installment obligations accrue per installment (round 38, ledger -03)
**Encoded proposition.** Same proposition as C-5, for Texas.
**Authority relied on.** Texas contract-limitations case law (unnamed).
**If wrong, direction:** partial (see C-5).
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### T-7 · TX-WAGE-GARNISHMENT-PROHIBITION · Contractual alimony vs. Chapter 8 maintenance (round 38, ledger -04)
**Encoded proposition.** The constitutional exception to the wage-garnishment bar (Tex. Const. art. XVI,
sec. 28, quoted) for "spousal maintenance" reaches court-ordered maintenance under Family Code chapter 8;
purely CONTRACTUAL alimony agreed in a divorce decree but not ordered as chapter 8 maintenance is an ordinary
contract debt and does not qualify. Encoded as a screening question.
**Authority relied on.** art. XVI, sec. 28 (quoted); Fam. Code ch. 8 (named); case law on contractual alimony
(unnamed).
**If wrong, direction:** OC (a payor told wages cannot be garnished for contractual alimony when they can).
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### T-8 · TX-EXEMPT-PERSONAL-PROPERTY · Independent-contractor receivables are not "current wages" (round 38, ledger -04)
**Encoded proposition.** The "current wages for personal service" protection (Prop. Code 42.001(b)(1),
quoted) covers employee wages; payments owed to an independent contractor are accounts receivable, reachable
by garnishment or turnover, subject to the contractor's other exemptions. The employee/contractor line is
encoded as a screening question.
**Authority relied on.** 42.001(b)(1) (quoted); case law on the personal-service line (unnamed).
**If wrong, direction:** DD if Texas courts treat some contractor compensation as "current wages" and the
node says fully reachable.
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

### T-9 · TX-HOMESTEAD-EXEMPTION · Lien attached before homestead character (round 46, ledger -08)
**Encoded proposition.** Homestead protection is measured as of the time the creditor's lien attached; a
judgment lien that validly attached while the property was a non-exempt rental is not divested when the
debtor later moves in and impresses homestead character. Encoded as a screening question; the 52.0012
affidavit route does not clear such a lien.
**Authority relied on.** Prop. Code 52.001 et seq. (named); attachment-timing case law (unnamed).
**If wrong, direction:** OC (overstates the creditor's lien) if Texas treats a later homestead as superior.
**Ruling:** [ ] CONFIRM  [ ] STRIKE  [ ] MODIFY: ______________________________________________

---

## Not on this list, and why

- **TX-HOMESTEAD abandonment vs. temporary absence** (round 38): anchored to Prop. Code 41.003 in round 39.
- **Article III standing for technical violations** (round 38): anchored to the quoted *TransUnion* syllabus.
- **FDCPA one-year limitations from the violation** (round 38): anchored to the quoted *Rotkiske* holding
  (F-9 above is the narrower open question of the state-law periods).
- **Turnover of already-paid wages** (round 38): anchored to CPRC 31.0025(a).
- **Rosenthal Act reaches original creditors** (round 38): anchored to Civ. Code 1788.2(c)/1788.17.

## After the session

Rulings are transcribed into `rules/debt/validation/stage_b_dispositions.json` (a `counsel_ruling` field on
each gloss entry) and applied as v1.1 content edits in a single patch, which is the first of the two gates
for Phase LOCK item 5.
