# Cowork Direction — Holdings v3 Reporting: Separate Retrieval Failure from Verification Result

**For:** Cowork · **From:** Andy (planning with Claude) · **Date:** 2026-06-23
**Applies to:** the v3 generate-from-source holdings run now executing, and its morning report + doc updates.

**Purpose:** The triage of the v2 batch-1 failures came back **N (no-text) = 50%, W (wording-artifact) = 30%, I (inaccurate) = 20%.** That changes how the v3 result must be reported. Generate-from-source can recover W cases and resolve INFERRED control, but it **cannot** fix N cases — if CourtListener never returns the opinion text, there is nothing to characterize from. A single blended "machine-verified rate" computed over a population that is 50% retrieval-failed will **understate the true method rate** and invites the false read that "the method doesn't generalize beyond CA." The record already shows this exact effect: CA's *Aweeka* was machine-verifiable; CL returned caption-only that run, so 4/6 understated the true 5/6. This direction makes the runner and report tell the truth in both directions.

> **This does not change any passing standard.** It changes *measurement and routing only*. The bar to reach `machine-verified` is unchanged. We are separating "we couldn't get the text" from "we got the text and the holding failed verification," because those are different facts and must not be averaged into one misleading number.

---

## REQUIREMENT 1 — Classify every case by outcome bucket (not pass/fail)

Each case in the v3 run must be tagged with exactly one terminal bucket:

- **MV — machine-verified.** Text retrieved; two independent models corroborated the holding from source; control tagged STATED or INFERRED. (Standard unchanged.)
- **CI — confirm-inference.** Text retrieved; holding corroborated by two models; `control: INFERRED`, no controlling quote (the AZ / *Thomas v. Goudreault* / *Schweiger* pattern). Routes to the cheap confirm-inference lane, NOT re-characterization.
- **RC — re-characterize.** Text retrieved; source-generated holding diverged from the draft → genuine inaccuracy. Routes to attorney re-characterization. (This is the true-defect residue; triage predicts ~20%.)
- **PR — pending-retrieval.** Text NOT retrievable (caption-only, intermittent, wrong document, or CL throttle/empty). **This is an infrastructure outcome, not a verification outcome.** Does NOT route to attorney. Quarantined for a retrieval retry pass. (Triage predicts ~50%.)
- **SM — single-model-preliminary.** Only one model genuinely answered (GPT empty / API failure with no real second model). Never `machine-verified`. Flag and hold.

**The PR bucket is the key addition.** A case is PR if the failure is retrieval, full stop. Do not let a retrieval failure masquerade as a verification failure, and do not send a PR case to any attorney lane.

---

## REQUIREMENT 2 — Report TWO rates, never one blended number

The morning report must state both, explicitly labeled, with denominators shown:

1. **Method rate (the real measure of the method):**
   `MV ÷ (text-retrievable cases) = MV ÷ (MV + CI + RC)`
   — i.e., among cases where text actually came back, how often did generate-from-source reach machine-verified. CI may be reported as MV-or-CI if useful, but show MV alone too.

2. **Overall rate (gated by retrieval):**
   `MV ÷ (all attempted cases, including PR)`
   — the end-to-end rate as it stands today, bottlenecked by CourtListener.

State plainly, in one sentence: *"The gap between the method rate and the overall rate is the CourtListener retrieval bottleneck (PR cases), not a limitation of the verification method."* If the method rate is materially higher than the overall rate, that IS the finding — say so.

Put the CA result alongside both, so convergence (or not) between CA and non-CA **on the method rate** is visible. The honest comparison is non-CA method rate vs. CA method rate — NOT non-CA overall vs. CA, which would re-introduce the retrieval confound.

---

## REQUIREMENT 3 — Provenance per case (unchanged but enforced in the report)

For every MV/CI/RC case, the report must show which model GENERATED the holding from source and which DIFFERENT model VERIFIED it. If generate and verify were the same model, the case is invalid (single-model with extra steps) → downgrade to SM. A method rate without the per-case generate/verify split is treated as not-done.

Also confirm in the report whether the **GPT empty-response prerequisite** was actually resolved in the v3 runner. If C ran single-model on any case, that case is SM, and the report must say how many — because a method rate inflated by single-model passes is not trustworthy.

---

## REQUIREMENT 4 — Quarantine PR cases for a retrieval retry, separate from validation

Write the PR cases to their own list (e.g. `holdings_v3_pending_retrieval.json`) with, per case: the cite, what CL returned (caption-only / empty / wrong-doc / throttle), and whether the MCP or an alternate path confirmed the opinion *exists and is verifiable* (the *Aweeka* pattern). Do NOT advance, fail, or attorney-route these. They are waiting on text, and they are the direct evidence for the CourtListener ask:

- If Free Law Project grants a higher rate limit or bulk data, the PR list is the re-run target and the retrieval architecture shifts from live-API to local dataset.
- The size of the PR list IS the public-interest number for the CL request: "holdings verification for a 50-state A2J library is bottlenecked on opinion-text retrieval — N of M cases could not be checked because text wasn't served."

Report the PR count and how many of them MCP/alternate-path confirms are *verifiable-but-unserved* (true retrieval artifacts) vs. genuinely not-in-CL.

---

## REQUIREMENT 5 — Morning report shape (what Andy reads)

Keep it short and decision-oriented. In order:

1. **Two rates**, labeled, with denominators (Requirement 2), CA alongside.
2. **Bucket counts:** MV / CI / RC / PR / SM, with the W-recovery callout — did the wording-artifact cases (triage said ~30%) actually recover under generate-from-source? That is the direct test of whether v3 worked.
3. **The one-sentence honest read** of method-rate vs. overall-rate (retrieval bottleneck named).
4. **Queues:** RC count (attorney re-characterization — expect small, ~20%), CI count (cheap confirm lane), PR count (pending retrieval — the CL ask).
5. **Provenance line:** generate/verify split confirmed per case; SM count (single-model) called out.
6. **Anything genuinely needing Andy** — kept to real decisions, not status.

Then update `VALIDATION_METRICS_LEDGER.md` and the State of Record with the **method rate and overall rate both**, never a single blended figure. Any external-facing number (paper, deck, one-pager) must be the method rate with the retrieval caveat stated, OR the overall rate explicitly labeled as retrieval-gated — never an unlabeled blend.

---

## WHAT WOULD MAKE THIS A FAILED REPORT (state if any occurred)

- A single blended machine-verified rate reported without the two-rate split.
- Any PR (no-text) case routed to an attorney lane.
- A retrieval failure counted as a verification failure (PR folded into RC).
- A method rate quoted without per-case generate/verify provenance.
- SM (single-model) cases counted toward the method rate.

A number that understates the method because retrieval failed is just as dishonest as one that overstates it. Both directions matter. When unsure, show the denominator and let the reader see exactly what was measured.

---

*Cowork Direction — Holdings v3 Reporting · CJaC · 2026-06-23 · Separate "couldn't get the text" from "the holding failed." Two rates, never one blend. No-text waits on retrieval; it never goes to a lawyer.*
