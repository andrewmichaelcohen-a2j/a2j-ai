# Validation Metrics & Evidence Ledger

**Civil Justice as Code · started June 18, 2026 · Andrew M. Cohen · Apache 2.0**

**Purpose.** A longitudinal, consistent record of validation outcomes across runs, modules, and (eventually) domains. The point is not any single number — it is the *trend across comparable runs*. Two claims this ledger is built to support, **only when the data warrants** (not before):

1. **Valid / reliable / safe** — the outputs are correct at a measured, improving rate, with errors caught by the process rather than reaching users.
2. **Repeatable** — the *same methodology*, applied to a new module or domain, reproduces comparable quality *without bespoke heroics*. Repeatability is demonstrated by the metric trend holding as scope expands — the method, not the person, carries the result.

**Discipline.** Log every run the same way, even when numbers are unflattering. A ledger that only records successes proves nothing; the error-catch and escalation rates are evidence *because* they're recorded honestly. Metrics describe process performance — they never advance a file's status (the ladder governs that). This ledger is descriptive evidence, not a validation gate.

---

## Core metrics (logged per run)

For each validation run, record:

| Metric | Definition | What it evidences |
|--------|------------|-------------------|
| **Coverage** | # units (states/claims) targeted ÷ # in scope | Completeness of the run |
| **Consensus-confirm rate** | % units where file + all models independently agree | Baseline corroboration |
| **Divergence rate** | % units flagged (citation/period/split) | How much the run surfaced |
| **AI-resolved rate** | % of divergences resolved by the tiered protocol w/o human | Automation leverage (the narrowing) |
| **Human-escalation rate** | % of units requiring genuine attorney judgment | Surgical-human load (lower = more leverage, *if* quality holds) |
| **Error-catch count** | # file claims found wrong (corrected) | The process catching real errors (safety evidence) |
| **Error-confirm outcome** | of human-reviewed items, # where AI proposal was correct vs. wrong | Whether AI resolution is *trustworthy*, not just frequent |
| **Cost** | $ spend for the run | Efficiency / scalability |
| **Throughput** | time or units/hour | Scalability evidence |

**The two most important for the thesis:** (a) **error-catch count** (proves the process finds real mistakes → safety) and (b) **human-escalation rate trend across modules** (proves automation narrows the human load *repeatably* → scale). Watch these across rows.

---

## Validation surface — what these metrics do and do NOT cover

**Honesty discipline: the metrics below cover a narrow slice of what the files assert.** L2 consensus to date validates one thing — the bright-line *notice period and citation* for the nonpayment claim. Each rules file asserts far more: which defenses apply and their elements, how modules interact, the procedural sequence, exceptions and their conditions, service methods, overlays. **Most of each file's claims have not been tested by any method yet.** A high consensus rate on notice periods is not evidence the file is correct; it is evidence the easiest, most deterministic layer is corroborated.

This ledger therefore tracks not just *rates* but *coverage* — what fraction of a file's claims any validation method has actually touched. The current validation surface is small and bright-line-weighted. Reading a confirm rate without its coverage overstates validation.

**The apex of the validation roadmap is outcome-based testing against known results.** Everything logged so far validates *inputs* (are the encoded rules correct?). The stronger, still-pending method validates *outputs*: a corpus of realistic fact-patterns, each tagged with an attorney-established (or adjudicated) known-correct outcome, run through the rules files and scored against ground truth. That tests the whole decision logic end-to-end rather than claim-by-claim, and it is the only method that demonstrates the files *deliver accurate results*. Its credibility depends entirely on the ground truth being human-anchored, not model-generated — otherwise the validation question merely moves back a step. Until outcome-testing exists, the validation surface remains partial, and the ledger says so plainly.

---

## Ledger

### Domain: Residential Eviction Defense

#### Module: Notice — claim type: pay_or_quit (nonpayment) period + citation

| Run | Date | Models | Units | Consensus-confirm | Divergence | AI-resolved | Human-escalated | Errors caught | Cost | Status |
|-----|------|--------|-------|-------------------|-----------|-------------|-----------------|---------------|------|--------|
| L2 Phase 1 (machine-assist flags) | 2026-06-18 | gpt-5.5 + gemini-2.5-pro | 8 | 3 (38%) | 5 (62%) | 3 | 2 (25%) | ≥3 (OH, MS citations; WV period) | <$0.10 | complete |
| L2 Phase 2 (remaining) + retry | 2026-06-18 | gpt-5.5 + gemini-2.5-pro | 43 | ~37 (86%)* | ~6 | 2 | ~4 | ≥2 (DE citation; NV period) | <$1 | complete |
| **Notice/pay_or_quit — combined (51)** | 2026-06-18 | gpt-5.5 + gemini-2.5-pro | **51** | **~41 (80%)** | **~10 (20%)** | **5** | **~5 (10%)** | **≥5** | **<$1.10** | **complete; review queue open** |

*\*Phase 2 raw run showed more apparent splits; most were GPT token-budget parse errors, not legal disagreement — retry resolved them to consensus. Logged here as a data-quality note: separate **technical** failures from **substantive** divergence (see Process-quality notes).*

**Proof point captured:** the tiered resolution protocol narrowed **8 Phase-1 discrepancies to 2 genuine human-judgment items** — the first recorded instance of the automation-narrows-human-load claim. To be tested for *repeatability* as the next modules run.

**Pending (fills in as Andy works the review queue):**
- Error-confirm outcome: of the AI-resolved items (WV, OH, MS, DE, NV), how many does attorney review confirm correct? *(This number is the real test of whether AI resolution is trustworthy. Log it as the queue is worked.)*
- Genuine-L7 outcomes (MO, ND, MD, VA, GA, SD): what the attorney determined, and whether the file or a model was right.

#### Module: Service — *(next instrumented run — service L2)*
| Run | Date | Models | Units | Consensus-confirm | Divergence | AI-resolved | Human-escalated | Errors caught | Cost | Status |
|-----|------|--------|-------|-------------------|-----------|-------------|-----------------|---------------|------|--------|
| L2 Service | *pending* | | 51 | | | | | | | not yet run |

> Service is the first run *designed to be instrumented from the start*. Specific hypothesis to test (from the readiness assessment): several states (AL, AK, CT) cite one statute for all 3 service methods — L2 will show whether that's correct (single provision) or an error (section header vs. subsections). Record the resolution.

#### Modules pending content work before L2
- **Procedural defects** — boilerplate 4-item template; needs jurisdiction-differentiation before L2 is meaningful. (Logged so the gap is on the record.)
- **Federal overlays (SCRA)** — absent from all 51; needs population pass. (Logged.)
- **State-protective overlays** — thin by design; L2 = citation check only.

---

## Repeatability view (the cross-module trend — the point of the ledger)

As each module/claim-type completes, add its combined row here so the *trend* is visible at a glance. Repeatability is evidenced if consensus, AI-resolved, and escalation rates stay in a comparable band — and if error-confirm outcomes show AI resolution is reliably correct — as scope widens.

| Module / claim | Units | Consensus | AI-resolved | Human-escalated | Error-confirm (AI correct %) | Date |
|----------------|-------|-----------|-------------|-----------------|------------------------------|------|
| Notice / pay_or_quit | 51 | ~80% | 5 | ~10% | *pending queue* | 2026-06-18 |
| Service | — | — | — | — | — | pending |
| *(future modules…)* | | | | | | |
| *(future DOMAINS — debt, family, benefits…)* | | | | | | |

**Reading the trend (when populated):** stable/improving consensus + stable-or-falling escalation + high error-confirm-correct % across rows = the methodology is *repeatable*, not bespoke to notice. A new *domain* holding the band is the strongest repeatability evidence.

---

## Process-quality notes (separate technical from substantive)

A safety/honesty practice: distinguish **substantive divergence** (real legal disagreement — the signal) from **technical failure** (parse errors, token-budget issues, path bugs — noise). Conflating them inflates the apparent error rate and obscures the real one.

- 2026-06-18: Phase 2 GPT parse errors from token-budget (fixed `max_completion_tokens` 2000→6000); WV path bug (underscore vs hyphen). These were **technical**, not legal — excluded from substantive divergence counts above.

---

## How to use this ledger
- Cowork appends a row per validation run with the core metrics; never edits prior rows' recorded outcomes.
- Andy fills the error-confirm outcomes as the review queue is worked — *this is the trust evidence*.
- Before outreach, the combined/repeatability views are the quantitative backbone of the "trustworthy at scale" demonstration framework — populated honestly, claimed only to the extent the data supports.

---

*Validation Metrics & Evidence Ledger · Civil Justice as Code · Copyright 2026 Andrew M. Cohen · Apache 2.0*
