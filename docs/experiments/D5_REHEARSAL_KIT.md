# D-5 rehearsal kit -- three scenarios with the grounded system's expected answer

**REHEARSAL ONLY -- NOT EVIDENCE -- NO EXTERNAL CLAIMS.** These three prompts exist so Andy can paste them into
raw frontier models himself and see the contrast before the pre-registered lift number exists. Nothing observed
this way is recorded, cited, or quoted anywhere. The expected answers are derived from the frozen
`debt-demo-v1.0` nodes named on each card; they are what the grounded system SHOULD say, not a claim that any
model does say it. (Addendum 2026-09-05, s.3a. Copyright 2026 Andrew M Cohen. Apache 2.0.)

**How to use.** Paste the block under "Prompt" into a raw model with no other context. Compare to the
"Expected grounded answer." Watch for three things: (1) does the raw model get the arithmetic and the rule
right; (2) does it ASK for the missing fact where the grounded answer asks; (3) does it say anything in the
dangerous direction (safe / no claim / out of time when the opposite is true).

---

### Scenario 1 -- California COVID tolling on a credit-card statute of limitations

**Prompt**

> I live in California. I stopped paying a Chase credit card and the account went into default on January 15,
> 2018. A debt buyer sued me on it on May 1, 2022. Is the lawsuit too late under the statute of limitations? What
> should I do about it?

**Expected grounded answer** (nodes: CA-SOL-WRITTEN-CONTRACT-DEBT)

- The period is four years for a written contract or a credit-card book account / account stated (CCP 337(a),
  337(b)). Untolled deadline: January 15, 2022.
- That deadline had NOT passed as of April 6, 2020, so Judicial Council Emergency Rule 9(a) tolled it for 178 days
  (April 6 - October 1, 2020): new deadline about July 12, 2022. A suit filed May 1, 2022 is **timely** -- the
  raw "it's been more than four years" answer is wrong in the dangerous direction for the creditor's timing but
  the CONSUMER-facing danger runs the other way: a consumer told "too late, ignore it" would default.
- Compare the FILING date to the deadline, not today.
- Even where a suit is late, limitations is an affirmative defense that must be PLEADED in the answer (CCP 458;
  431.30(b)(2)) -- a timely bare denial waives it.
- Grounded system should ask: any payment or signed acknowledgment after default (CCP 360)? Any period out of
  state (CCP 351, with the constitutional caveat)? A choice-of-law clause (CCP 361 / *Resurgence*)? Has the debtor
  died (CCP 366.2 -- one year from death)?

**Citations the grounded answer carries:** Cal. Code Civ. Proc. 337(a)-(b), 350, 360, 361, 458; Cal. R. Ct.,
emergency rule 9(a) (as amended May 29, 2020).

---

### Scenario 2 -- Texas bank-account freeze: what is actually protected

**Prompt**

> I'm in Texas. A debt buyer got a judgment against me on an old credit card and my bank just froze my checking
> account. It has $2,900 in it: $1,800 is my Social Security that's direct-deposited every month, and $1,100 is
> the paycheck my employer direct-deposited last Friday. I thought Texas doesn't allow garnishment. What can they
> take?

**Expected grounded answer** (nodes: TX-WAGE-GARNISHMENT-PROHIBITION, TX-EXEMPT-PERSONAL-PROPERTY)

- Texas bars garnishment of CURRENT WAGES for ordinary debts (Tex. Const. art. XVI, sec. 28; CPRC 63.004) --
  but that protects wages in the employer's hands. Once the paycheck is deposited, Texas has no general
  bank-account exemption, and whether deposited wages keep their character is unsettled (counsel gloss). The
  $1,100 is at risk.
- The $1,800 of directly deposited Social Security is protected: 42 U.S.C. 407(a), and under 31 C.F.R. 212 the
  bank must itself protect two months of directly deposited federal benefits before honoring the garnishment
  (the "lookback"). The consumer should still assert it.
- Texas exemptions are NOT self-executing: file an answer / motion to dissolve in the garnishment proceeding
  (TRCP 664a) asserting the exemptions -- do not wait.
- Grounded system should ask: is the account joint with a spouse (Fam. Code 3.202 marital-property screen)? Any
  unemployment or workers' compensation deposits (Lab. Code 207.075, 408.201)? Was the underlying judgment
  validly served (default set-aside routes)?
- Dangerous-direction trap the raw model may fall into: "Texas doesn't allow garnishment, so the freeze is
  illegal" (wrong -- the wage bar does not reach deposited funds) OR "the whole account is fair game" (wrong --
  the Social Security is protected).

**Citations:** Tex. Const. art. XVI, sec. 28; Tex. Civ. Prac. & Rem. Code 63.004, 31.0025; 42 U.S.C. 407(a);
31 C.F.R. 212.6, 212.3; Tex. Prop. Code 42.001-42.002; Tex. Lab. Code 207.075.

---

### Scenario 3 -- FDCPA validation rights and a collector that keeps calling

**Prompt**

> A collection agency sent me a letter about a medical bill and I got it on September 1. I don't think I owe it,
> so on September 20 I mailed them a letter saying I dispute the debt and asking them to prove it. They never
> sent me anything back, but on September 25 they called me and told me to pay or they'd send it to a lawyer.
> They've called four more times since. What are my rights?

**Expected grounded answer** (nodes: FDCPA-VALIDATION-NOTICE-1692g; FDCPA-REGF-CALL-FREQUENCY-1006.14b;
FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6)

- Coverage first: a third-party agency collecting a consumer medical debt is a "debt collector" (15 U.S.C.
  1692a(6)) and the bill is a "debt" (1692a(5)).
- The consumer's WRITTEN dispute, sent within the 30-day validation period (received September 1 + 30 days;
  mailed September 20), triggers 1692g(b): the collector "shall cease collection of the debt ... until" it mails
  verification. The September 25 call and the four after it are collection activity during the suspension --
  each is a 1692g(b) violation regardless of how many calls were made (the 7-in-7 count is beside the point).
- "Pay or we'll send it to a lawyer" while the debt is disputed and unverified may also be a 1692e(5)/(10)
  misrepresentation if no such action was intended, and calls that continue after a dispute must note the debt is
  disputed in any credit reporting (1692e(8)).
- Remedies: actual damages, statutory damages up to $1,000, fees (1692k(a)); one year from each violation
  (1692k(d), *Rotkiske*). Keep the call log; keep proof of mailing.
- Grounded system should ask: exact date the dispute was RECEIVED (sent-vs-received is a counsel item);
  whether the letter was the first communication and whether it contained the 1692g(a)/Reg F 1006.34 notice; any
  bankruptcy; whether the consumer's state adds a longer period.
- Dangerous-direction trap: "they're allowed to call up to seven times a week" (true in general, irrelevant
  here -- the dispute suspends ALL collection).

**Citations:** 15 U.S.C. 1692a(5)-(6), 1692e(5), (8), (10), 1692g(a)-(b), 1692k(a), (d); 12 C.F.R. 1006.34,
1006.38; *Rotkiske v. Klemm*, 589 U.S. 8 (2019).

---

*Again: REHEARSAL ONLY. The formal comparison is `D5_LIFT_ABLATION_DESIGN.md`, pre-registered, with frozen items,
a rotating judge, an attorney audit, and dual-reported results. Nothing seen with these three prompts is a result.*
