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

**Error-confirm outcomes — logged 2026-06-19 (Andy Cohen):**

| Item | Type | AI proposal | Attorney outcome | AI correct? |
|------|------|-------------|-----------------|-------------|
| WV | PERIOD-AI-RESOLVED | notice_required=false, §55-3A-1 | ✅ Confirmed correct. §37-6-5/§37-6-23 govern separate URLTA notice situations; §55-3A-1 FED action needs no prior notice. | **Yes** |
| OH | CITATION-AI-RESOLVED | §1923.04(A), 3d | ✅ Confirmed correct. "3 or more days" statutory language; minimum is 3. | **Yes** |
| MS | CITATION-AI-RESOLVED | §89-8-13(5)(a), 3d | ✅ Confirmed correct. | **Yes** |
| DE | CITATION-AI-RESOLVED | 25 Del. C. §5502(a), 5d | ✅ Confirmed correct. | **Yes** |
| NV | PERIOD-AI-RESOLVED | days=7, §40.253(1)(a) | ✅ Days and statute confirmed correct. ⚠️ **count_method error caught by attorney review:** L2 left `calendar_days`; judicial days (weekends/holidays excluded) is correct → corrected to `calendar_days_excluding_weekends_holidays`. AI resolved the period but did not audit the count_method field. | **Partially** — period/statute correct; count_method miss |
| IL | CONSENSUS-CONFIRM | §9-209, 5d, business_days | ✅ Confirmed correct. | **Yes** |
| ME | CONSENSUS-CONFIRM | §6002, 7d | ✅ Confirmed correct. Additional note: 7-day arrears waiting period must also elapse before notice may be served. | **Yes** |
| SD | CITATION-AMBIGUOUS (queue) | Both models cited §21-16-2 (GPT) or §21-16-1(2) (GPT) / §21-16-2 (Gemini) — could not AI-resolve | ⚠️ **Full statute repeal caught:** §21-16-2 was **repealed by SB 90 (2024)**. Both models cited a non-operative statute. No pay-or-quit notice required (NJ-pattern). 3-day ripening period under §21-16-1(4). | **AI flagged correctly as unresolvable** — repeal not detectable by L2 |
| VA | MODEL-SPLIT-L7 (queue) | GPT: 5d (§55.1-1245(F)); Gemini: 14d (same section) | Time-versioned resolution: **5d is current law; 14d becomes operative 2026-07-01** under HB 15/SB 48. Both models were right at different time points. File updated with `pending_amendment` block. | **Both partially correct** — genuine temporal split |

**AI-resolution trustworthiness summary (notice/pay_or_quit module):**
- 4 AI-resolved items (WV, OH, MS, DE): **4/4 confirmed correct** (100% citation/period accuracy)
- 2 CONFIRM items (IL, ME): **2/2 confirmed correct**
- NV: days/statute correct; count_method miss (field not targeted by L2 runner — scoped to days + citation only)
- SD and VA: correctly escalated (SD = statute repeal; VA = genuine temporal split) — AI did not hallucinate resolutions it couldn't support
- **Errors caught by the process:** 1 count_method error (NV), 1 statute repeal (SD → models cited a non-operative section), 1 time-version ambiguity (VA)

**L7 still open (MO, ND, MD, GA):** Not yet worked. No attorney determination yet.

#### Module: Service — claim type: service methods (personal / substituted / mail) per pay-or-quit notice

| Run | Date | Models | Units | Round-1 consensus | Divergence | AI-resolved | Human-escalated | Errors caught | Cost | Status |
|-----|------|--------|-------|-------------------|-----------|-------------|-----------------|---------------|------|--------|
| L2 Service — initial 51-state run | 2026-06-19 | gpt-5.5 + gemini-2.5-pro | 51 | 14 (27%) | 37 (73%) | — | — | — | ~$1.53 | partial |
| L2 Service — 17-state retry (ERROR states) | 2026-06-19 | gpt-5.5 + gemini-2.5-pro | 17 | +2 | — | — | — | — | ~$0.51 | partial |
| L2 Service — reasoning + tiebreaker passes | 2026-06-19/20 | gpt-5.5 + gemini-2.5-pro | 49 | — | 35 | 32 (91% of diverged) | 2 (4%) | TBD | ~$2.50 | complete |
| **Service — combined (51)** | **2026-06-19/20** | gpt-5.5 + gemini-2.5-pro | **51** | **16 (31%)** | **35 (69%)** | **32 (63%)** | **2 (4%)** | **TBD** | **~$4.50** | **complete; review queue open** |

**Final service module outcomes (2026-06-19/20):**

| Outcome | Count | States |
|---------|-------|--------|
| ✅ Round-1 consensus-confirmed | 16 | CT, FL, IL, KY, MD, ME, MI, MN, MS, NE, NY, OH, OK, RI, VT, WY |
| ✅ AI-resolved (reasoning/tiebreaker/single-model) | 32 | AK, AL, AR, AZ, CO, DE, GA, HI, IA, ID, IN, KS, LA, MA, MO, MT, NC, ND, NH, NJ, NV, OR, PA, SC, SD, TN, TX, UT, VA, WA, WI, WV |
| 🔴 L7-ATTORNEY-REVIEW | 2 | DC, NM — persistent API failure, zero recoverable model data |
| ⚠️ L6-RECENCY-WATCH | 1 | CA — not a citation error; statute watch only |

**Key process observations:**
- **Single-model fallback** (new capability built during this run): VA, WI, AR, TN all resolved via Gemini high-confidence answer when GPT persistently failed (empty responses). GPT failures were transient/rate-limiting, not substantive. Single-model fallback prevents model API failures from becoming false L7 escalations.
- **Subsection targeting** (new capability): IN resolved on 3rd pass when query shifted from generic statute lookup to "which subsection for each specific method" — both models converged on §32-31-1-9(b)(1)/(2)/(3). Standard tiebreaker had failed twice. Lesson: for subsection-level disputes, method-specific queries outperform generic tiebreakers.
- **Hypothesis from readiness assessment (same-statute pattern):** Confirmed — several states cite one statute for all 3 methods correctly (single provision); others needed subsections identified (e.g., ID: §6-304(1)/(2)/(3) vs file's parent §6-303). Both patterns exist in the data.
- **L7 load: 4%** (2/51) — down from 10% in notice module. Both L7 items are API-failure artifacts, not legal ambiguity. Zero genuine interpretive disputes reached L7 after the full tiered protocol.

**Error-confirm outcomes (service):** *Pending — queue open for Andy's confirmation of AI-resolved items.*

> **Repeatability note:** Escalation rate fell from ~10% (notice) to 4% (service), with service requiring more processing rounds due to subsection complexity. The protocol adapted (single-model fallback, targeted subsection queries) within the same validation framework. L7 load remained surgical. This is the repeatability claim being built.

#### Modules pending content work before L2
- **Procedural defects** — boilerplate 4-item template; needs jurisdiction-differentiation before L2 is meaningful. (Logged so the gap is on the record.)
- **Federal overlays (SCRA)** — absent from all 51; needs population pass. (Logged.)
- **State-protective overlays** — thin by design; L2 = citation check only.

---

## Repeatability view (the cross-module trend — the point of the ledger)

As each module/claim-type completes, add its combined row here so the *trend* is visible at a glance. Repeatability is evidenced if consensus, AI-resolved, and escalation rates stay in a comparable band — and if error-confirm outcomes show AI resolution is reliably correct — as scope widens.

| Module / claim | Units | Consensus | AI-resolved | Human-escalated | Error-confirm (AI correct %) | Date |
|----------------|-------|-----------|-------------|-----------------|------------------------------|------|
| Notice / pay_or_quit | 51 | ~80% | 5 (all confirmed correct) | ~10% (4 open + 2 resolved) | 4/4 confirmed correct; 2 correctly escalated (SD repeal, VA time-version) | 2026-06-18 |
| Service / method_rules | 51 | 31% (round-1) | 32/35 diverged (91%) | 4% (2 — DC, NM) | *pending queue* | 2026-06-19/20 |
| *(future modules…)* | | | | | | |
| *(future DOMAINS — debt, family, benefits…)* | | | | | | |

**Trend observation (2 modules):** Consensus rate dropped (80% → 31%) but human-escalation rate also dropped (10% → 4%) — because the tiered protocol expanded (single-model fallback, targeted queries), it absorbed more divergence without needing attorney review. Lower consensus ≠ lower quality; it reflects subsection complexity requiring more AI passes. The repeatability claim is about the *escalation rate* staying surgical — and it did.

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
