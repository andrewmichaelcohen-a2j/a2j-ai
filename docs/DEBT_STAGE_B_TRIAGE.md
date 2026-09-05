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

**Round 41 (2026-09-04) -- first findings under the disposition-aware gate.** Smoke run `run_20260904T184830Z`
(3 nodes) produced 3 material findings, all on FDCPA-REGF-CALL-FREQUENCY-1006.14b, which had no ledger entries
(it was clean in round 38), so all three were correctly NEW; the other two nodes produced no material findings.
Dispositions (ledger ids `D-FDCPA-REGF-CALL-FREQUENCY-1006.14b-01..04`):

| Node | Finding | Class | DD | What changed |
|---|---|---|---|---|
| FDCPA-REGF-CALL-FREQUENCY | One agency, five accounts, ~28 calls/week called "presumptively compliant" | FIXED-VERIFIED (node was RIGHT on the presumption) | yes | Official Interpretation comment 14(b)(4)-2.i confirms per-debt counting; added the rebuttal factors (comment 14(b)(2)(i)-2) as a note, a presumption_type rewrite, and two checklist items |
| FDCPA-REGF-CALL-FREQUENCY | Consumer's own inbound call never started the 7-day cooldown | FIXED-VERIFIED | yes | Comments 14(b)(2)(i)-1.ii and 14(b)(4)-1.ii pinned; checklist item 2 + cooldown_rule reworded |
| FDCPA-REGF-CALL-FREQUENCY | Spouse treated as a 1692c(b) third party | FIXED-VERIFIED | no | 1692c(d) + 12 CFR 1006.6(a) pinned; note corrected |
| FDCPA-REGF-CALL-FREQUENCY | (bonus) unconnected-call exclusion scope | FIXED-VERIFIED | -- | Round-33 UNVERIFIED marker closed from comment 14(b)(3)(ii)-1 |

Source note: the CFPB Official Interpretations (Supplement I to part 1006) are fetchable from the Cornell LII
eCFR mirror (`law.cornell.edu/cfr/text/12/appendix-Supplement_I_to_part_1006`) even though consumerfinance.gov's
interpretation pages 403. That unblocks several earlier "interp unverifiable" markers corpus-wide; only this
node's were closed this round.

Citation-side, the same run confirmed two permanent 403s: mass.gov (940 CMR 7.04 -- re-pinned to the Cornell
state-regulations mirror) and www4.courts.ca.gov (emergency rule 9 -- PDF-only, so `manual_verification`; the
checker has no PDF extractor). Stage B parse failure on FDCPA-COVERAGE (empty completion at max_tokens, the
dominant Stage B failure signature in every run since 09-01) is a runner matter, handled in round 42.

**Round 43 (2026-09-04) -- re-smoke `run_20260904T212407Z` (rounds 41+42 applied).** Stage B parse 100% (round 42's
retry recovered the node that had failed every run since 09-01; the diagnostics proved the cause -- content blocks
`['thinking','text']`, the model's reasoning consuming the output budget). The run reported 6 material findings,
**0 matched to existing dispositions -- and correctly so**: none overlaps the 7 ledger entries on those two nodes.
Reading the JSON by hand found **3 more** on CA-SOL-WRITTEN that the runner had silently treated as non-material
because the model omitted the `exposes_gap` field while setting both `realistic_and_common` and
`would_cause_wrong_answer` true (runner fix: round 44 derives materiality from those two flags, per the ratified
definition). All 9 dispositioned (ledger ids `-05..-07` on the call-frequency node, `-04..-06` on coverage,
`-05..-07` on CA-SOL-WRITTEN):

| Node | Finding | Class | DD | What changed |
|---|---|---|---|---|
| FDCPA-REGF-CALL-FREQUENCY | Written validation dispute (1692g(b)) suspends all calls; node counted anyway | FIXED-VERIFIED | yes | independent_bars_note + threshold checklist; 1692g(b) pinned |
| FDCPA-REGF-CALL-FREQUENCY | Bankruptcy stay / discharge not screened | FIXED-VERIFIED | yes | same note + checklist; 11 U.S.C. 362(a)(6), 524(a)(2) pinned; registered GLOBAL |
| FDCPA-REGF-CALL-FREQUENCY | Count not stated per debt collector | FIXED-VERIFIED | no (wrong defendant) | unit_of_count + determination corrected; checklist |
| FDCPA-COVERAGE | White-label vendor routed to exclusion (A) by the NAME on the letter | FIXED-VERIFIED | yes | checklist item 1 tests the actor; note clarified |
| FDCPA-COVERAGE | (B) affiliate exclusion missing the principal-business condition in the checklist | FIXED-VERIFIED | yes | checklist item 5 rewritten |
| FDCPA-COVERAGE | Government-origin consumer accounts (municipal utility, EMS) treated as non-debts | FIXED-VERIFIED + GLOSS | yes | note corrected on the 1692a(5) transaction test; Pollice, Piper named for counsel |
| CA-SOL-WRITTEN | Deceased debtor: CCP 366.2 one year from death (dropped finding) | FIXED-VERIFIED | yes | deceased_debtor_note + threshold checklist; 366.2 pinned |
| CA-SOL-WRITTEN | "Never signed anything" routed card debt to the 2-year oral period; 337(b) book account / account stated omitted (dropped) | FIXED-VERIFIED | yes | note + checklist item 2; 337(b) pinned |
| CA-SOL-WRITTEN | Sister-state judgment treated under 683.020 (dropped) | FIXED-VERIFIED + GLOSS | yes | judgment_enforcement_note corrected; 337.5(b) pinned; TX dormancy copied; enforceable-where-rendered = counsel |

**Structural note (for Andy).** Two of the nine are cross-cutting themes (bankruptcy; validation-dispute cease)
that will surface on every conduct node in turn. The ledger now has a `_global` section (four entries: bankruptcy,
1692g(b) cease, 1692c bars, state overlays) that round 44 makes the runner append to every node's prompt, so a
corpus-wide theme is tagged once rather than re-found node by node. That is a stop-gap for the design question
already on the HORIZON list -- shared gate nodes for cross-cutting overlays (a BANKRUPTCY-OVERLAY node, a state
mini-FDCPA node). The global entry is deliberately narrow: it tells the model to report only where a node's own
text is WRONG about the theme, not merely silent.

**Counsel additions this round (3):** Pollice v. National Tax Funding (3d Cir. 2000) and Piper v. Portnoff (3d Cir.
2005) on municipal utility obligations as "debts"; the enforceable-where-rendered requirement for sister-state
judgments (full-faith-and-credit case law); 366.2's interaction with a timely probate creditor's claim.

**Round 46 (2026-09-05) -- first full run under the disposition-aware gate, `run_20260904T221748Z` (19 nodes).**
Stage A 100%; citations 94.7% (one permanent 403, re-pinned); Stage B parse 84.2% (three losses to a round-44
runner regression, fixed in round 45). 47 material findings: 1 correctly matched to the cross-cutting
`G-BANKRUPTCY` disposition (FCRA), 46 new across 16 nodes. Read one by one, they are real -- the corpus is
young and a strong adversarial model keeps finding real gaps; this is the standing generator working, not
padding. All 46 dispositioned in three content patches (46a federal, 46b California, 46c Texas), ledger ids
per node in `stage_b_dispositions.json` (120 node-specific entries). Sources fetched and pinned where a
statute governs; case law recorded as GLOSS-FOR-COUNSEL; sections not fetched this round recorded as
FIXED-SOURCE-NAMED for a follow-up pinning round.

**Classification tally (46):** FIXED-VERIFIED 22 · FIXED-SOURCE-NAMED 12 · GLOSS-FOR-COUNSEL 8 · HORIZON 1 ·
NOT-A-GAP 2 (some rows carry two classes; counted by the primary). **Dangerous-direction: 30 of 46.**

**Three findings checked against the source and found WRONG as stated** (the discipline paying for itself):
CPRC 16.066 is not a borrowing statute for contract choice-of-law clauses -- it governs foreign judgments
(pinned for that purpose; the clause point is a counsel gloss); a justice-court venue motion is due 21 days
AFTER the answer, not before it (TRCP 502.4(d), pinned; venue note added anyway); and calls to a relative
placed to reach the consumer do not count against the consumer's 7-in-7 bucket (Reg F text and comment
14(b)(2)(i)-1.iii). Each is recorded NOT-A-GAP with its reasoning in the node.

**Where the node itself was affirmatively wrong (fixed):** 1692f said time-barred and discharged-debt
collection violate 1692f per se (Midland Funding; Walls split); TX-HOMESTEAD stated the 522(p) rollover rule
backwards (522(p)(2)(B) excludes same-state rollover equity); TX-SOL compared today to accrual instead of the
filing date, and used last payment as the accrual date; CA-SOL-ORAL used last payment as accrual (CCP 360
forbids it for unwritten debts); TX-DEFAULT-JUDGMENT applied 306a and the restricted appeal to justice court;
CA-BANK's aggregation note read as a one-time exemption; TX-WAGE said support withholding has 'no protection'
(Fam. Code 158.009: 50% cap).

**Cross-node duplicates handled once:** TRCP 506.1 de novo appeal (pinned on both TX-DEFAULT-JUDGMENT and
TX-JUSTICE-COURT); Texas deposited-benefit exemptions (207.075 pinned on TX-WAGE, cross-referenced on
TX-EXEMPT-PP); bankruptcy discharge on 1692f (node text was wrong, so reported -- correct behaviour under the
G- rule).

**For counsel (this round's additions, 8):** Avila / Chuway / Taylor on static balances; Jerman scope of the
bona fide error defense; Walls / Simon / Randolph on FDCPA claims for discharge-injunction violations; the
revival-misrepresentation theory on time-barred debts (Buchanan, Pantoja); California demand-loan accrual
(Civ. Code 1657); Texas choice-of-law clauses and limitations; Texas revolving-account accrual date; Texas
lien-attached-before-homestead timing; Fam. Code 910/911 spouse-account interplay; Fin. Code 864 setoff
figures; bill of review from a justice-court judgment.

**Named-but-not-fetched this round (pinning backlog, 12):** UCC 9-609(b)(2) (Cal. Com. Code 9609 / Tex. Bus.
& Com. Code 9.609); 47 U.S.C. 227(b)(1)(A)(iii); 20 U.S.C. 1095a; 26 U.S.C. 6331/6334; CCP 706.070-.084,
706.023; CCP 697.310, 704.950; CCP 704.740-704.800; CCP 720.110; CCP 703.010, Fin. Code 864; Fam. Code 910/911;
CCP 431.30(b)(2), 458; CCP 430.10, 435-436, 472a(b); Tex. Lab. Code 408.201; TRCP 664a; TRCP 500.3(e);
TRAP 26.1(a), 26.3; TRCP 329b(e); Fam. Code 3.102, 8.106, 158.003-.004; Civ. Code 1657.

**Structural observation.** Every parsed node returned exactly 3 material findings. That is the prompt asking
for edge cases and a capable model supplying them; the gate will not reach zero until the generator's marginal
finding is not material, and this round's findings say we are not there yet. Suggest the next runner round
ask for a severity rank and a "would a careful legal-aid attorney consider this a must-fix" flag rather than
three yes/no fields, so the count becomes informative rather than saturated. Spec decision for Andy.

**v1.0 MEASUREMENT OF RECORD -- `run_20260905T175137Z` (2026-09-05), frozen corpus, runner at round 45.**
Smoke `run_20260905T110123Z` (3 nodes) passed every precondition. Full run: **Stage A 100% · citation verification
100% · Stage B parse 100%** (first run ever with all three at 100; the streaming transport and every round-46 pin
held). Stage B: 54 material findings, 2 correctly matched to existing dispositions, **52 new -- all carried to
`POST_V1_BACKLOG.md` (rows 2-53) and the ledger as BACKLOG-V1.1; no v1.0 content changed.** 35 of 52 are
dangerous-direction as frozen; the worst: TX-EXEMPT-PP says boats are not exempt when 42.002(a)(4) exempts
boats used in a trade; TX-HOMESTEAD omits refinance liens from the exceptions; CA-SOL-WRITTEN grants a flat
+178 COVID days to claims that accrued inside the window, and says judgment renewal is automatic; 1692f's
threshold excludes repossession agencies that 1692a(6) covers for item (6); Obduskey generalized beyond
nonjudicial foreclosure. These are recorded, not fixed.

**Gate, dual-reported.** Raw JSON: `internal_gate_met` = **False** (third leg: 52 undispositioned).
Backlog-dispositioned reading: all 52 classified the same day, third leg met on paper -- Andy decides which
reading the claim card uses (`DEBT_DEMO_V1_MEASUREMENT_OF_RECORD.md`). What is true on either reading: 174
adversarial findings surfaced across rounds 38-46 and the record run; 120 dispositioned into content before
the freeze; 52 carried to v1.1, dangerous-direction first.

**Would-be classes of the 52:** FIXED-VERIFIED (source already pinned; text/checklist change) 13 ·
FIXED-SOURCE-NAMED 18 · FIXED (note/checklist, no new source) 8 · GLOSS-FOR-COUNSEL 9 · COVERED elsewhere
(cross-reference) 6 (some rows carry two). Convergence signal: the round-46 fixes did NOT recur -- the model
found the next layer, not the same layer; 2 findings were matched rather than re-reported.

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
