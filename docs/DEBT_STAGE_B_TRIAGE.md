# Debt track -- Stage B adversarial backlog triage (round 38, 2026-09-03)

**Purpose.** After rounds 35-37 cleared the citation/Stage A plumbing, 11 of 19 demo-corpus nodes were flagged
*only* by Stage B adversarial findings -- and comparing two consecutive runs on identical content
(`run_20260902T185148Z`, `run_20260903T174510Z`) showed the findings are **stable and reproducible**, not
generator noise. This document dispositions every one of them, offline, without further live runs.

**Classification key**
- **FIXED-VERIFIED** -- corrected in round 38 using statutory text already live-verified in this corpus.
- **FIXED-PENDING-SOURCE** -- corrected in round 38 (logic note + checklist question), but the governing text
  is *named, not quoted*: web-fetch tooling was down for the entire round, so no new citation was pinned.
  Every such note carries a `[SOURCE PENDING ...]` marker inside the rules file. Round 39 pins them.
- **GLOSS-FOR-COUNSEL** -- case-law point encoded as a source_tier C note; needs Andy's confirmation.
- **COVERED** -- already addressed elsewhere; cross-reference added or nothing needed.
- **HORIZON** -- real, but belongs in a node that does not exist yet.

**Dangerous-direction (DD)** = as previously encoded, the node would tell a consumer they are safe / have no
claim / are out of time when the opposite is true. These were prioritized.

| Node | Finding (both runs unless noted) | Class | DD | What changed / what's pending |
|---|---|---|---|---|
| FDCPA-COVERAGE-1692a6 | "Is it a debt" gate excludes phantom/identity-theft debts | FIXED-VERIFIED | yes | 1692a(5)/(3) already quoted say *alleged*; checklist item reworded + note |
| FDCPA-COVERAGE-1692a6 | Deceased obligor / surviving family treated as uncovered | FIXED-VERIFIED (+pending) | yes | 1692c(d) added (verified round 34); Reg F 1006.6(a)(1)(iv) pending |
| FDCPA-COVERAGE-1692a6 | "Regularly collects" element never tested (occasional lawyer/bookkeeper) | FIXED-VERIFIED | no | Element is in the quoted 1692a(6); determination step 4 + checklist |
| FDCPA-1692e | FDCPA's own 1-yr SOL (1692k(d)) never asked | FIXED-PENDING-SOURCE | yes | Note + checklist; Rotkiske v. Klemm gloss |
| FDCPA-1692e | Original creditor "not covered at all" ignores Rosenthal/TX ch. 392 | FIXED-PENDING-SOURCE + HORIZON | yes | Predicate softened to "under the federal Act"; state mini-FDCPA node is HORIZON |
| FDCPA-1692e | Article III standing for bare technical violations | GLOSS-FOR-COUNSEL | no | TransUnion/Spokeo note + checklist |
| FDCPA-1692f | 1-yr SOL (1692k(d)) | FIXED-PENDING-SOURCE | yes | Same as 1692e |
| FDCPA-1692f | Envelope-marking rule stated categorically (Douglass) ignores 8th Cir. benign-language + standing | GLOSS-FOR-COUNSEL | no | Catalog item (8) caveated |
| FDCPA-1692f | Pay-to-pay/convenience fees stated categorically; courts split | GLOSS-FOR-COUNSEL | no | Catalog item (1) caveated + checklist |
| FDCPA-1692g | Formal pleading treated as initial communication (1692g(d)) | FIXED-PENDING-SOURCE | yes | Note + checklist |
| FDCPA-1692g | Original-creditor-name request is a 2nd cease-collection trigger | FIXED-VERIFIED | yes | Already in the verified 1692g(b) quote; operationalized |
| FDCPA-1692g | Overshadowing never evaluable (no intra-window facts collected) | FIXED-VERIFIED | yes | Anti-overshadowing sentence is in the verified quote; note + checklist |
| FDCPA-1692g | Oral dispute treated as inert (1692e(8)/1006.38 credit-reporting duty) | FIXED-PENDING-SOURCE | yes | Note + checklist |
| FCRA-1681s-2b | Furnisher faulted for not reviewing docs the CRA never forwarded (e-OSCAR) | FIXED-VERIFIED | no (points at wrong defendant) | 1681i(a)(2)(A)-(B) added (verified round 37 fetch); checklist reworded |
| FCRA-1681s-2b | "Too old" dispute closed as no-claim; it's obsolescence (1681c) | FIXED-PENDING-SOURCE | yes | Note + checklist |
| FCRA-1681s-2b | 3rd finding truncated in both runs | -- | -- | unreadable; not addressed |
| CA-SOL-WRITTEN | Round-34 choice-of-law note over-corrected (Resurgence v. Chambers) | FIXED (logic) + GLOSS | yes | § 361 and a choice-of-law clause are two routes; both asked now |
| CA-SOL-WRITTEN | Revival note overstates § 360 payment proviso (promissory notes only) | FIXED-VERIFIED | yes | § 360 quote already in node; note rewritten |
| CA-SOL-WRITTEN | CCP § 351 absence tolling likely unconstitutional as applied | GLOSS-FOR-COUNSEL | yes | Abramson / Heritage caveat |
| CA-SOL-WRITTEN / ORAL / TX-SOL | "Expired" does not stop a default judgment; SOL must be pleaded | FIXED-PENDING-SOURCE | yes | Note + checklist on all three (CCP 458 / TRCP 94) |
| CA-SOL-ORAL | Post-expiration "good faith" payment treated as restarting accrual | FIXED-VERIFIED | yes | § 360 added from sibling node's verified entry |
| CA-SOL-ORAL | Installment continuous accrual | GLOSS-FOR-COUNSEL | partial | Mirrors written node's existing note |
| CA-WAGE-GARNISHMENT | Weekly formula applied to biweekly/monthly pay; pay period marked non-dispositive | FIXED-PENDING-SOURCE | yes | 706.050(b) note; pay period now dispositive |
| CA-WAGE-GARNISHMENT | Support-order priority ignored (706.030/.031/.052) | FIXED-PENDING-SOURCE | no (overstates creditor) | Note + checklist |
| CA-WAGE-GARNISHMENT | Necessaries exemption / claim procedure omitted (706.051/.105) | FIXED-PENDING-SOURCE | yes | Note + checklist |
| CA-HOMESTEAD | Bankruptcy overlay: 730-day rule, § 522(p) cap, § 703.140(b) election | FIXED-PENDING-SOURCE | yes | Note + checklist |
| CA-HOMESTEAD | Support judgments / consensual liens not blocked (703.070) | FIXED-PENDING-SOURCE | yes | Note + checklist |
| CA-HOMESTEAD | Forced-sale mechanics (704.800 minimum bid; FMV + senior liens) | FIXED-PENDING-SOURCE | yes | Note + checklist |
| CA-HOMESTEAD | Sale proceeds protected 6 months (704.720(b)) | FIXED-PENDING-SOURCE | yes | Note + checklist |
| CA-VEHICLE | Claim-of-exemption 10-day deadline (703.520) | FIXED-PENDING-SOURCE | yes | Note + checklist |
| CA-VEHICLE | Vehicle-dwelling is a homestead (704.710) | FIXED-PENDING-SOURCE | yes | Note + checklist |
| CA-VEHICLE | IRS levy / secured-party repossession / support not bound by § 704 | FIXED-PENDING-SOURCE | yes | Note + checklist |
| CA-VEHICLE | Married debtors / community property (703.110) | FIXED-PENDING-SOURCE | no | Note + checklist |
| CA-BANK | Claim-of-exemption deadline (703.520) | FIXED-PENDING-SOURCE | yes | Note + checklist |
| CA-BANK | IRS / FTB administrative levies not governed by § 704 | FIXED-PENDING-SOURCE | yes | Note + checklist |
| CA-BANK | Other traceable exempt deposits (704.115/.120/.130/.140-.160) | FIXED-PENDING-SOURCE | yes | Note + checklist |
| CA-CIVIL-ANSWER | § 415.30 notice-and-acknowledgment service omitted | FIXED-PENDING-SOURCE | yes | Note + checklist |
| CA-CIVIL-ANSWER | Late answer before default entered still works (585 / 473(b)) | FIXED-PENDING-SOURCE | yes | Note + checklist |
| CA-CIVIL-ANSWER | Filing fee / fee waiver required with answer | FIXED-PENDING-SOURCE | yes | Note + checklist |
| TX-DEFAULT-JUDGMENT | Eviction defaults: TRCP 510, no MNT, 5-day appeal | FIXED-PENDING-SOURCE | yes (case-ending) | Threshold checklist + note |
| TX-DEFAULT-JUDGMENT | Restricted appeal / bill of review not limited to service defects | GLOSS-FOR-COUNSEL | yes | Note + checklist |
| TX-SOL | Post-expiration payment (16.065 / Fin. Code 392.307) | FIXED-PENDING-SOURCE | yes | Note + checklist |
| TX-SOL | Installment separate accrual | GLOSS-FOR-COUNSEL | partial | Note + checklist |
| TX-SOL | Judgment already entered -> 10-yr renewable (34.001/31.006) | FIXED-PENDING-SOURCE | yes | Note + checklist |
| TX-WAGE-GARNISHMENT | "Bank accounts CAN be frozen" ignores federal-benefit deposits (42 USC 407; 31 CFR 212) | FIXED-PENDING-SOURCE | yes | Note qualified + checklist |
| TX-WAGE-GARNISHMENT | Turnover orders / receivership (CPRC 31.002) mislabeled unconstitutional | FIXED-PENDING-SOURCE | yes (contempt risk) | Note + checklist |
| TX-WAGE-GARNISHMENT | Employer deductions / wage assignments are not garnishment (Lab. Code 61.018) | FIXED-PENDING-SOURCE | no | Note + checklist |
| TX-WAGE-GARNISHMENT | Contractual alimony vs. Ch. 8 maintenance | GLOSS-FOR-COUNSEL | no | Note + checklist |
| TX-HOMESTEAD | 730-day bankruptcy domicile rule | FIXED-PENDING-SOURCE | yes | Note + checklist |
| TX-HOMESTEAD | Abandonment vs. temporary absence | GLOSS-FOR-COUNSEL | yes | Note + checklist |
| TX-HOMESTEAD | Trust / LLC title (41.0021) | FIXED-PENDING-SOURCE | yes | Note + checklist |
| TX-HOMESTEAD | Mechanic's-lien formalities (art. XVI 50(a)(5)) | FIXED-PENDING-SOURCE | no | Note + checklist |
| TX-HOMESTEAD | Abstract of judgment clouds title (52.0012) | FIXED-PENDING-SOURCE | no | Note + checklist |
| TX-EXEMPT-PERSONAL-PROPERTY | **Everything under the cap treated as exempt; cash/bank/brokerage/boats are not listed** | FIXED-VERIFIED | **yes -- the worst one** | § 42.002(a) already quoted; threshold checklist item inserted at position 1 |
| TX-EXEMPT-PERSONAL-PROPERTY | Federal benefits in bank accounts | FIXED-PENDING-SOURCE | yes | Note + checklist |
| TX-EXEMPT-PERSONAL-PROPERTY | Student-loan AWG / spousal maintenance reach wages | COVERED | -- | Already in TX-WAGE-GARNISHMENT's federal_override_note; cross-reference added |
| TX-EXEMPT-PERSONAL-PROPERTY | Independent-contractor receivables are not "current wages" | GLOSS-FOR-COUNSEL | yes | Note + checklist |
| TX-EXEMPT-PERSONAL-PROPERTY | 730-day bankruptcy domicile rule | FIXED-PENDING-SOURCE | yes | Note + checklist |
| TX-JUSTICE-COURT-ANSWER | Dollar amount used as proxy for court; county/district = TRCP 99 | FIXED-PENDING-SOURCE | yes | Checklist item replaced |
| TX-JUSTICE-COURT-ANSWER | Late answer before default signed still works | FIXED-PENDING-SOURCE | yes | Note + checklist |

**Totals (round 38):** 58 findings dispositioned. FIXED-VERIFIED 9 · FIXED-PENDING-SOURCE 37 · GLOSS-FOR-COUNSEL 11 ·
COVERED 1 · unreadable 1.

**Round 39 update (2026-09-04, sources pinned):** of the 37 FIXED-PENDING-SOURCE rows, **34 are now FIXED-VERIFIED**
(statutory/regulatory text quoted verbatim from a fetched source). Still named-only (3): CA filing fee / fee
waiver (Gov. Code 70611, 68631); TX mechanic's-lien homestead formalities (Tex. Const. art. XVI § 50(a)(5)); TX
late-answer-before-default (practice rule, no single text). Of the 11 GLOSS-FOR-COUNSEL rows, **5 are now
statute- or Supreme-Court-anchored** and drop off the counsel list: TransUnion (quoted), Rotkiske (quoted), TX
temporary-absence (Prop. Code 41.003), TX turnover of paid wages (CPRC 31.0025), Rosenthal reach (Civ. Code
1788.2/1788.17). **Remaining for counsel (6):** Resurgence v. Chambers (CA choice-of-law clauses); Abramson /
Heritage (CCP 351); 8th-Cir. envelope split; pay-to-pay fee split; contractual alimony vs. Ch. 8; TX
restricted-appeal scope; independent-contractor receivables; installment accrual (CA/TX). Pinning also caught
**six errors in round 38's own notes**, each now corrected in the file: CCP 703.520's claim-of-exemption deadline
is 15/20 days, not 10; CCP 706.050(b)'s multipliers are statutory (96/104/208 hours), not Judicial-Council;
Fin. Code 392.307 is debt-buyer-specific; a Texas judgment goes dormant without a writ within 10 years, it is not
'renewable indefinitely'; Reg F 1006.38 keys disputes to a writing (the oral-dispute point rests on 1692e(8)
alone); CCP 704.720(b) covers forced-sale/insurance proceeds, voluntary-sale proceeds are the declared-homestead
rule. Plus one carve-out: Rosenthal does not reach original creditors for 1692e(11)/1692g. (Some rows bundle the same finding across two runs or three nodes.)

**Round 40 (2026-09-04, runner):** this table now has a machine-readable twin at `rules/debt/validation/stage_b_dispositions.json` (one entry per row per node, ids `D-<node_id>-NN`, classifications as updated by round 39: FIXED-VERIFIED 48 · GLOSS-FOR-COUNSEL 9 · FIXED-SOURCE-NAMED 3 · COVERED 1; the unreadable row is omitted). The corroboration runner feeds a node's entries into Stage B and counts only findings the model cannot map to one of them. New findings from future runs get dispositioned here first, then added to the ledger. Keep the two in sync.

**What "pending source" means for you.** Every pending item is a screening *question* the system now asks
plus a note that names the governing provision. None of them quotes statutory text as verified. They change
what the system asks before it answers, which is the safe direction; they do not assert new law as confirmed.
Round 39's job is mechanical: fetch each named provision, pin the `derived_from` entry, remove the marker.

**For your legal review specifically** -- the GLOSS-FOR-COUNSEL rows are the ones where I encoded a
case-law proposition without a primary statutory anchor: Resurgence v. Chambers (CA choice-of-law clauses),
Abramson/Heritage (CCP 351), TransUnion/Spokeo standing, the 8th-Circuit envelope split, pay-to-pay fees,
Texas abandonment doctrine, contractual alimony, independent-contractor wages, TX restricted-appeal scope,
and installment accrual in both states. Please confirm or strike.

**Structural note.** These findings were stable across two runs because they are real. After round 38 the
next live run should produce a materially different (smaller, and different) Stage B list. If it instead
produces a new list of similar size on the corrected nodes, that is evidence the "zero gaps" CLEAN-PASS
criterion cannot converge and the gate should become "Stage B findings dispositioned by counsel" -- a spec
decision for Andy, not something this round changes.
