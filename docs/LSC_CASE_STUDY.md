# Case Study: The LSC Eviction Laws Database — Lessons for CJaC

**Date:** June 18, 2026 · **Prepared by:** Claude (live-verified research) · **For:** Andy **What this is:** A direct assessment of the closest existing precedent to CJaC — what they built, how, why it stopped where it did, whether it's used, and what CJaC should learn and how to position relative to it. **Where I'm inferring rather than confirming, I say so.**

---

## What it actually is (corrected from first impression)

The "LSC Eviction Laws Database" is more precisely: a dataset built by the **Center for Public Health Law Research (CPHLR) at Temple University's Beasley School of Law**, for the **Legal Services Corporation (LSC)**, hosted on Temple's **LawAtlas.org** platform, using a methodology called **policy surveillance**.

- **Scope:** Two datasets — (1) **State/Territory**: all 50 states \+ DC \+ 6 territories; (2) **Local**: 30 selected jurisdictions. Covers causes of eviction, **notice requirements**, filing timelines, the judicial process, and post-judgment/execution — each element **linked to the governing statute**. Downloadable as Excel, with a published **Codebook** and **Research Protocol**.  
- **Currency:** State dataset law-as-of **Jan 1, 2021**; Local dataset shows a **Nov 1, 2022** update. So it had at least one update cycle — **not a one-and-done**, but **not continuously maintained** either. As of today it is materially stale (misses SD 2024, GA 2024, VA 2026 — all of which you caught this morning).  
- **Access:** Free, but requires creating a LawAtlas account to download Data/Protocol/Codebook. Interactive map \+ downloadable structured data. **"Open source" in the data sense** (openly available, transparently documented, citable) — *not* a code repo you contribute to like CJaC's GitHub.

## Their methodology — "policy surveillance" (this is the important part)

Policy surveillance is a **mature, scientific legal-mapping discipline**, not an ad hoc effort. Worth understanding because it's a 15-year-refined version of what CJaC is doing, and it has a real validation model:

- **Process:** define/scope the legal question → systematically collect the law for each jurisdiction (like a systematic review) → **code the law** into structured variables → **quality assurance via inter-coder reliability checks** (multiple coders code independently; disagreements measured and reconciled).  
- **A key stated principle:** *"The goal of coding is to read, observe, and record the law, rather than to read and interpret the law."* — they deliberately stay at the **bright-line/observable** layer and avoid interpretation. (Directly parallel to CJaC's bright-line vs. open-textured distinction.)  
- **Two explicit rigor tiers:** **"policy surveillance"** (high rigor, inter-coder reliability, meant for evaluation) vs. **"sentinel surveillance"** (one coder \+ a supervisor, lighter QC, explicitly labeled *not* evaluation-grade, for fast-moving areas). **They tier their confidence and label it honestly** — exactly CJaC's status-ladder instinct.  
- **Longitudinal capability:** the method *can* capture law at multiple points in time (re-coded on each change) — so continuous maintenance was within their method; they just didn't fund it past the study.  
- **Validation model:** **human expert coders \+ inter-coder reliability**, no AI. Built/refined \~2009 onward under Robert Wood Johnson Foundation public-health-law funding; LawAtlas tech was even spun into a startup ("Legal Science Partners").

## Why it stopped at its snapshot (evidence \+ honest inference)

**Confirmed:** It was a **congressionally-directed study** — LSC's "Effect of State & Local Laws on Evictions." That framing matters enormously.

**My inference (flagged as inference):** It almost certainly didn't "stall" in the failure sense. It looks like a **funded study that delivered its deliverable** — a point-in-time (and one-update) authoritative dataset tied to a specific research question (how does legal variation affect eviction outcomes) — and then the *funded scope ended*. The Jan-1-2021 snapshot is a **study design choice** (a fixed legal baseline to correlate against outcome data), not a maintenance failure. Continuous currency wasn't the goal; a clean comparative baseline was. **This is a scoping/funding-model story, not a capability or validation failure.**

**Why this distinction matters for you:** the lesson is NOT "they failed and we'll succeed." It's "**they built an excellent point-in-time research artifact under a research-grant model; the unmet need is a *continuously-maintained, living* version — which is a different model (institutional stewardship), not a better dataset.**" That's CJaC's actual differentiator, and it's an honest one.

## Is it used? (partial answer)

- **Confirmed adjacent usage:** NLIHC explicitly points users to the LSC Eviction Laws Database as *the* comprehensive source for **pre-2021** tenant protections. LawAtlas data broadly is **cited 250+ times** in media/scholarship since 2014\. So the *platform* and *method* are well-used and respected.  
- **Couldn't confirm:** current operational use of the *eviction* dataset specifically by legal-aid tools or front-line providers. **Honest gap** — I found it cited as a research/reference source, not as a live engine inside help tools. (That it's 2021-frozen makes live front-line use unlikely now.)

---

## What CJaC should LEARN (the actionable part)

**1\. Adopt the policy-surveillance vocabulary and rigor concepts — they're a credibility gift.** This is a *recognized scientific discipline* for exactly what CJaC does. Framing CJaC's method partly in policy-surveillance terms (systematic collection, structured coding, inter-coder reliability) instantly makes it legible to the academic/A2J establishment and shows CJaC isn't reinventing the wheel naively. **Their two-tier rigor model (policy vs. sentinel surveillance) is essentially CJaC's status ladder** — cite the parallel.

**2\. Inter-coder reliability is a validation technique CJaC can adapt — and it reframes the multi-model consensus.** Their gold standard is *multiple independent human coders \+ measured agreement*. CJaC's L2 multi-model consensus is, in effect, **"inter-coder reliability with AI coders"** — same logic (independent coding, measure agreement, investigate divergence), with the same caveat they'd recognize (agreement ≠ correctness). This is a clean, established frame for what L2 is. **And it tells you the apex human-validation method: for VALIDATED status, consider genuine inter-coder reliability (two attorneys code independently, measure agreement) rather than single-attorney review** — that's the scientifically-recognized standard, and adopting it would make CJaC's "VALIDATED" tier rigorous by an established yardstick.

**3\. The "record, don't interpret" line is the bright-line/open-textured distinction — validated by a mature field.** Their explicit choice to stay at the observable layer and avoid interpretation confirms CJaC's core architectural instinct. Where CJaC goes *further* (deliberately tackling the open-textured layer with AI-draft-then-validate) is the genuine frontier — but the bright-line foundation is shared with a proven method.

**4\. The currency problem is real, structural, and unsolved by the grant model — which is precisely CJaC's opening.** Their snapshot-and-stop isn't laziness; it's what the research-grant funding model produces. **The unmet need is a living, continuously-validated layer** — which requires (a) a maintenance model (institutional stewardship, not one-time grant) and (b) automation to make continuous currency affordable. **This is exactly where modern AI changes the economics** (see \#5).

**5\. The AI-capability delta — assessed honestly, not assumed.** Your instinct to not assume is right. The honest assessment:

- **What AI genuinely changes:** the *cost and speed* of the systematic-collection and first-pass-coding steps. Policy surveillance is labor-intensive (human coders reading every statute); that labor cost is *why* continuous 50-state currency wasn't funded. AI can do the brute-force collection and draft-coding cheaply, making **continuous currency economically feasible for the first time.** That's the real, defensible delta.  
- **What AI does NOT change:** the validation requirement. The legal-AI literature is explicit that letting AI "check itself" is **not** a substitute for expert ground-truth (the hallucination-reliability research says self-checking pipelines are "not suitable" for legal correctness). So AI lowers the *coverage* cost but **not** the *validation* cost — which is exactly CJaC's thesis (automation for coverage/triage; humans for judgment). **The delta is in the economics of coverage, not in the elimination of human validation.** State this precisely; don't overclaim that "AI solves it."  
- **The honest synthesis:** *"Policy surveillance proved the method; the grant model couldn't sustain currency because human coding of 50 states continuously is too expensive. Modern AI changes that economics — it makes continuous coverage affordable — while the validation discipline (human expert sign-off, inter-coder reliability) stays necessary. CJaC \= policy surveillance's rigor \+ AI's coverage economics \+ a stewardship (not grant) maintenance model."* That's a precise, defensible, non-hype positioning.

---

## How to POSITION CJaC relative to LSC/LawAtlas

**Not as a competitor or a replacement — as the living successor that a new economic and institutional model makes possible.** Recommended framing:

*"The LSC/Temple Eviction Laws Database proved that the eviction process can be systematically coded into structured, statute-linked legal data across all 50 states — using policy surveillance, a rigorous scientific legal-mapping method with inter-coder reliability. Its limitation is not quality but currency: built as a congressionally-directed research study, it captures the law as of January 2021 and is not continuously maintained, because human coding of fifty jurisdictions on an ongoing basis is prohibitively expensive under a grant model. CJaC builds on that proven foundation with two additions the prior effort couldn't: (1) modern AI to make continuous, current coverage economically feasible, and (2) an institutional-stewardship maintenance model rather than a one-time study. The validation discipline — human expert sign-off, measured inter-coder reliability — is retained, because AI lowers the cost of coverage, not the requirement of verification. CJaC also extends past the bright-line layer the prior database deliberately stopped at, into the open-textured defenses, using AI-draft-then-validate."*

**Things this framing gets right (honesty checks):**

- Credits the precedent generously and accurately (no diminishing).  
- Names the real differentiator (currency \+ maintenance model \+ AI economics), not a vanity one.  
- Doesn't overclaim AI ("makes coverage affordable," not "solves validation").  
- Adopts their credibility (policy surveillance, inter-coder reliability) rather than reinventing.  
- Is verifiable — every claim about them is sourced.

**A collaboration angle worth considering:** Temple CPHLR / LawAtlas and LSC are natural *allies*, not rivals — CJaC could position as continuing/extending their work (with credit), potentially even using their 2021 dataset as a **corroboration baseline** (cross-check CJaC against LSC for pre-2021 law; divergences are either CJaC errors or post-2021 changes — the same recency discipline from today). This both validates CJaC and honors the lineage.

---

## Net lessons (summary)

1. **Borrow their credibility:** frame CJaC partly in policy-surveillance terms; it's the recognized scientific discipline for this work.  
2. **Adopt inter-coder reliability** as the frame for L2 (AI coders) and as the apex standard for VALIDATED (two independent attorneys, measured agreement).  
3. **Their "record don't interpret" confirms** CJaC's bright-line foundation; CJaC's open-textured work is the genuine extension.  
4. **The differentiator is currency \+ maintenance model \+ AI coverage-economics** — not "better data" and not "AI replaces humans."  
5. **Position as the living successor**, credit the precedent, consider using their dataset as a corroboration baseline, and explore Temple/LSC as allies.  
6. **State the AI delta precisely:** AI changes the *economics of coverage*, not the *necessity of validation*. This is both the honest truth and the strongest version of the argument.

---

*Case Study: LSC Eviction Laws Database · June 18, 2026 · Confirmed facts sourced; inferences flagged. Positioning judgments are Claude's; adoption is Andy's.*  
