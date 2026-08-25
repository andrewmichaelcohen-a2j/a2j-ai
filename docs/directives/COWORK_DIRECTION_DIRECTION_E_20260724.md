# Cowork Change Directive — Roadmap Additions: Direction E (Lower-Bound Testing) & Automation-Leverage Principles

**Date:** 2026-07-24
**Approved by:** Andrew M. Cohen (Andy)
**Companion docs:** `OPEN_QUESTIONS_AND_LIMITATIONS.md` (commit alongside — Task 0), `DIRECTION_D_ROADMAP.md` (amend per Task 3), `PILOT_DESIGN_BAYLEGAL_DRAFT.md` (commit as DRAFT — status PRELIMINARY, not for execution).
**Motivation:** Lou & Shin, *Legal Reasoning Is Not Lawyering* (arXiv:2606.23716, 2026): expert-structured benchmarks measure the upper bound of legal-AI performance; access to justice depends on the lower bound (noisy narratives, buried facts, omissions, folk-legal vocabulary), where models degrade and fail to abstain. CJaC's golden sets are, by this taxonomy, upper-bound tests. Direction E makes the lower bound measurable — and tests CJaC's structural hypothesis that completeness checklists enable elicitation where raw models guess.
**Sequencing:** documentation tasks (0, 3) execute now. Direction E builds are gated: Tier 1 prototyping may begin only after the v0.4 cycle completes (drafting through one-shot scoring); Tier 2 build follows a Tier 1 report and Andy's go. Nothing here preempts proposal 16 → 17 → v0.4.

---

## Task 0 — Commit companion docs (GREEN — execute now)

Commit `OPEN_QUESTIONS_AND_LIMITATIONS.md` at repo root or `docs/`, linked prominently from the README (it is outreach-facing: expect cold visitors from Wave 1). Commit the pilot draft with DRAFT/PRELIMINARY banners intact. Log both in DAILY_CHANGELOG.

## Task 1 — Direction E, Tier 1: Narrative-perturbation test class (define now; build after v0.4)

**Concept:** take frozen golden-set items and rewrite each as a realistic pro se narrative — facts buried in story, dispositive facts omitted unless implied, folk-legal vocabulary ("he evicted me" = served a notice; "the paper on my door"), approximate quantities ("about a year and a half"), irrelevant detail included. Score the pipeline end-to-end, single-shot: given only the narrative, does it reach the frozen outcome — and critically, does it *identify which dispositive facts are missing* rather than assuming them?

**Design requirements:**
1. Source items: v0.4 frozen set (never the burned v0.3 for scored runs; v0.3 items may seed *development* of the rewriting method only).
2. Perturbation tiers per item, each a separate scored variant: P1 complete-but-messy (all dispositive facts present, buried); P2 omissions (1–2 dispositive facts absent — correct behavior is to flag the gap or ask, NOT to answer); P3 folk-legal framing (narrative asserts a wrong legal conclusion; facts as given).
3. Scoring: P1 → outcome vs. frozen ground truth; P2 → **abstention/elicitation credit**: full credit only for identifying the specific missing fact(s) per the completeness checklist; any confident outcome on incomplete facts scores as confident-wrong (a new B-block metric: lower-bound confident-wrong). P3 → outcome despite the folk framing.
4. Narrative rewrites are drafted by a model NOT in the scoring consensus, then attorney-reviewed before freeze (a narrative rewrite is ground truth and freezes like any other item — full defect sweep applies; the narrative must not accidentally change the legal answer).
5. Ledger reporting: lower-bound scores reported in a separate block, never blended with upper-bound scores; the gap between bounds is itself a tracked metric (per Lou & Shin, that gap is the finding).

## Task 2 — Direction E, Tier 2: Interactive elicitation harness (define now; build after Tier 1 report)

**Concept (Andy-originated):** the strongest lower-bound test is interactive — does the CJaC-grounded system *ask the right questions*? Architecture: a simulated-user harness, directly analogous to standardized-patient testing in medical AI evaluation.

**Design requirements:**
1. **Actor:** one model plays the pro se user, seeded with (a) a hidden fact sheet derived from a frozen item and (b) a persona profile. The actor answers truthfully but in lay terms, volunteers nothing unprompted, and gives approximate answers ("about a year and a half") that require pinning down when a threshold is at stake.
2. **Subject:** the pipeline-under-test conducts the conversation and produces a conclusion (or a statement of what remains unknown).
3. **Model separation:** actor and subject from different model families; actor prompts and fact sheets never exposed to the subject; transcripts hashed and archived per house provenance style.
4. **Two-layer deterministic scoring:** (i) **Elicitation coverage** — for each dispositive fact on the item's completeness checklist, did the subject ask for it (or correctly derive it)? Objective percentage, auditable from the transcript. (ii) **Outcome accuracy** — final conclusion vs. frozen ground truth, with abstention credit when the persona was constructed to withhold a fact irrecoverably.
5. **Persona tiers** (realism escalation): E1 cooperative; E2 rambling/disorganized; E3 date- and quantity-confused; E4 asserts wrong folk-legal conclusions and mild hostility to questions. Report scores per tier.
6. **Human validation loop:** each cycle, the attorney (or clinic reviewers) audits a sampled subset of transcripts for scoring fidelity and for failure modes the checklist metric misses (tone, comprehensibility, harmful framing). Simulated-user results are a bridge to, not a substitute for, real-human evidence (the BayLegal pilot).
7. **Known limitation to state in the doc:** simulated users are more coherent and cooperative than real people even at E4; results are an *optimistic* lower bound. Say so wherever reported.
8. **Research note:** to our knowledge no interactive lower-bound legal benchmark exists; flag as a candidate methodology publication / Stanford collaboration once first results land.

## Task 3 — Automation-leverage principles (amend DIRECTION_D_ROADMAP.md; GREEN — execute now)

Add a principles section codifying the project's automation posture:

1. **Purpose statement:** automation exists to maximize the value density of every attorney-minute — absorbing everything up to the ratification moment (drafting, citation verification, consensus review, regression testing, statute/case watch, triage, evidence assembly) — and to shrink per-jurisdiction attorney load until part-time volunteer review is sufficient. The ratification judgment itself is never automated; that boundary is what "validated" means. (Record the v0.3 errata as the canonical illustration: AI consensus flagged the disagreements; determining which side was legally correct required an attorney.)
2. **New tracked metric — attorney-minutes per validated rule (AMPVR):** estimate retrospectively for the v3 cycle as a baseline; log prospectively per cycle in the METRICS_LEDGER. The automation program's success is a falling AMPVR at constant-or-better validation quality.
3. **New tracked metric — ratification-queue health:** open unratified proposals, age distribution, and inflow/outflow rate. Generation capacity must not outrun ratification capacity; when the queue ages past a threshold (propose one), D-4 generation throttles and triage sharpens rather than inventory growing.
4. **Triage automation (extends D-2):** auto-rank queue items by (a) frequency-weighted impact of the underlying rule, (b) evidence strength, (c) staleness risk — so scarce attorney minutes land on the highest-value judgments first.

## Reporting

Fold Tasks 0 and 3 into the next morning report; Direction E definitions logged as ROADMAP-DEFINED with their gates. No metrics change this cycle.

**Definition of done:** companion docs committed and README-linked; Direction E Tiers 1–2 specified in the roadmap doc with gates; automation principles section committed with AMPVR baseline estimation queued; changelog updated.

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
