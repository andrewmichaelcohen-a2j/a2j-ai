# Direction D — Continuous Improvement Roadmap

**Status:** ROADMAP-DEFINED. This document defines the shape and sequencing of D-2 through D-5. None of D-2–D-5 is being built by virtue of this document existing — each component starts building only when its own build trigger fires, per the sequencing below.

**D-1 (dev-set regression monitoring) is live and out of scope here** — it already ships (`rules/validation/scorer/dev_set_monitor.py`), fires on the noon dispatcher cadence, and is documented in `COWORK_DIRECTION_HOLDINGS_V3_REPORTING.md` and the ledger. This roadmap covers what comes after it.

**This is the engineering roadmap.** For the strategic map (breadth × depth, phases, gates, the Band 1/2/3 taxonomy), see `CJAC_ROADMAP.md` — that document defines *what* gets encoded and in what order; this one defines *how* the continuous-improvement machinery works. Read them together.

**Eviction-line status note (added 2026-08-25):** the eviction line is ON HOLD per Andy's Debt Defense Prototype priority directive (see `WORK_QUEUE.md`, `PROJECT_STATE_OF_RECORD.md`). Proposal 16/17 and the v0.4 cycle — the triggers D-2 and D-3 below were originally written against — are paused along with the rest of eviction work. D-2 (disagreement auto-triage) and D-3 (statute-and-case watch) are both proposed for shared build under the debt track's Phase A instead (see `DEBT_PROJECT_ARCHITECTURE_SPEC.md` §11) — if that happens, it builds these two components via a different trigger, not a reopening of eviction drafting. The sequencing diagram below is left as originally written (it's still correct *if and when* eviction resumes); treat it as suspended, not superseded.

**Build-trigger update (2026-08-26, "Phase A Unblock" directive item 6 — APPROVED, no longer just proposed):**
D-2 is **built** as of this date, as part of the debt track's grounded-corroboration runner
(`scripts/corroboration/run_corroboration.py`) — every model-vs-model disagreement, failed
citation check, or adversarial-generation finding auto-files to `docs/DEBT_DISAGREEMENT_QUEUE.md`
with evidence, same append-only pattern as this line's `HUMAN_REVIEW_QUEUE.md`. D-2's build
trigger is now confirmed as the debt track, not the eviction v0.4 cycle — eviction reopening is
**not required** for D-2 to exist or operate. D-3 (statute-and-case watch) remains proposed-not-
built, now explicitly slotted as a Phase A/B debt-track lane once the corpus has enough
statutory/case pins to make a watchlist worth generating automatically (see spec §4) — logged
here as HORIZON (`docs/WORK_QUEUE.md`), trigger = post-concept-demo, same discipline as the rest
of that round's deferrals.

## The invariant

> AI generates candidates and evidence continuously; nothing self-ratifies; every change lands as a proposal for named-attorney ratification; every applied change passes the dev-set regression gate; held-out sets are burned after one use.

Every component below is built and operated subject to this invariant without exception. None of D-2–D-5 is permitted to write a rules file, close a review-queue item, or advance a status label on its own — each produces proposals, evidence, or flags for the standing human-in-the-loop lanes (`HUMAN_REVIEW_QUEUE.md`, `MISSING_RULES_BACKLOG.md`, named-attorney ratification via `WORK_QUEUE.md`).

## D-2 — Disagreement auto-triage

**What it does:** every model-vs-rules or model-vs-model disagreement produced by any run (validation, scoring, or golden-set generation) auto-files into `HUMAN_REVIEW_QUEUE.md` with evidence attached: the item, both models' outputs, the rule(s) implicated, and a candidate classification (rule gap vs. ground-truth error vs. model error).

**Why:** the v0.3 held-out cycle proved disagreement is signal in both directions — C-18 was a genuine rule gap (became the v3 proposal), C-21/C-22 were ground-truth errors in the golden set itself (corrected by signed attorney errata). D-2 generalizes that pattern into a standing pipeline instead of a one-off manual autopsy.

**Build trigger:** the first v0.4 disagreement. D-2 is wired *before* the v0.4 scoring event so the event itself exercises it — this is the mechanism proposal 17 already requires (the v0.4 one-shot run needs somewhere for disagreements to land in real time, not a post-hoc write-up).

**Sequencing:** build starts alongside v0.4 drafting (proposal 17), must be live before the v0.4 scoring event fires.

## D-3 — Statute-and-case watch (automated freshness)

**What it does:** the watchlist generates itself from each rules file's statutory pins and case citations (no manually-maintained watch list). Scheduled checks against leginfo and CourtListener detect amendments, new session laws, or opinions touching a pinned authority. A hit produces a currency flag and a drafted amendment proposal, routed to Andy for ratification — it never edits a rules file directly.

**Why:** this is the literal meaning of "automated statute-watch" in the public two-pager. Two manual prototypes are already on record and inform the design: the SB 611 encoding and the SB 1103 §1946.1 catch (07-21, folded into proposal 16's scope).

**Build priority:** first Direction D component built after v0.4 scoring completes.

## D-4 — Standing adversarial self-critique

**What it does:** generalizes proposal 16's one-off self-critique pass into a scheduled lane. Models generate novel fact patterns targeting encoded rules' edges — thresholds, exemptions, compound defects, day-count boundaries — flag where the rules produce uncertain or conflicting outcomes, and file candidate golden-set items plus rule-gap hypotheses for review. This is the literal meaning of "AI-generated stress testing" in the public two-pager.

**Why:** proposal 16 already demonstrated the method works (§1946.2(a)(2) attachment-threshold pass, extended to the SB 1103 assessment) — D-4 is that method run on a cadence instead of once.

**Cadence:** proposal due with the build plan (not yet drafted — no cadence is set by this roadmap document).

## D-5 — CJaC-lift tracking across model generations

**What it does:** re-runs the ablation (rules vs. no rules, same items, same frozen ground truth) whenever a major new frontier model releases, and logs the resulting lift trend in `VALIDATION_METRICS_LEDGER.md`.

**Why:** measures what the rules file actually contributes on top of a raw model, tracked over time and across model generations — the empirical basis for the project's core claim.

**First data point:** the v0.4 ablation arm, already required by proposal 17 (same models/items/frozen ground truth, without the rules file). D-5 is what makes that a *tracked trend* rather than a single measurement.

## Direction E — Lower-bound testing (roadmap addition, 2026-07-24 directive)

**Status: ROADMAP-DEFINED**, per `docs/directives/COWORK_DIRECTION_DIRECTION_E_20260724.md`. Motivation (Lou & Shin, *Legal Reasoning Is Not Lawyering*, arXiv:2606.23716, 2026): expert-structured golden sets measure the *upper bound* of legal-AI performance; access to justice depends on the *lower bound* — noisy narratives, buried facts, omissions, folk-legal vocabulary — where models degrade and fail to abstain. CJaC's golden sets, by this taxonomy, are upper-bound tests. Direction E makes the lower bound measurable, and tests the structural hypothesis that completeness checklists (§2 of any CJaC rules-JSON) let a CJaC-grounded system *know what it doesn't know* rather than guess.

**Gate redirected 2026-08-25:** originally gated on the eviction v0.4 cycle completing. With the eviction line on hold, **Direction E's Tier 1/2 designs now apply to the debt track instead** — narrative rewrites and personas built on debt fact patterns, per `DEBT_PROJECT_ARCHITECTURE_SPEC.md` §5/§10/§11. This is the mechanism that unblocks the debt spec's demo-harness lane, which had been flagged as hard-blocked on this document not existing.

- **Tier 1 — Narrative-perturbation test class.** Frozen golden-set items rewritten as realistic pro se narratives (buried facts, folk-legal vocabulary, approximate quantities), scored end-to-end single-shot. Three perturbation tiers per item: P1 complete-but-messy, P2 omissions (correct behavior is flagging the gap, not guessing — confident-wrong on incomplete facts is scored as a new **lower-bound confident-wrong** metric), P3 folk-legal framing. Narrative rewrites are themselves frozen ground truth (drafted by a model outside the scoring consensus, attorney-reviewed, full defect sweep applies). Lower-bound scores are reported in their own ledger block, never blended with upper-bound scores — the *gap* between bounds is itself a tracked metric.
- **Tier 2 — Interactive elicitation harness.** A simulated-user harness, directly analogous to standardized-patient testing in medical AI evaluation. One model plays the pro se user (actor), seeded with a hidden fact sheet and a persona profile (truthful, lay terms, volunteers nothing unprompted, approximate answers); a different model family runs the pipeline-under-test (subject) and conducts the conversation. Actor and subject are separate model families; transcripts hashed and archived per house provenance style. Two-layer scoring: **elicitation coverage** (did the subject ask for/derive each dispositive fact on the completeness checklist — objective, transcript-auditable) and **outcome accuracy** (conclusion vs. frozen ground truth, with abstention credit). Persona tiers escalate realism: E1 cooperative → E4 wrong folk-legal conclusions + mild hostility. Each cycle, an attorney or clinic reviewer audits a sampled subset of transcripts for scoring fidelity and failure modes the checklist metric misses. **Known limitation, stated wherever results are reported:** simulated users are more coherent and cooperative than real people even at E4 — Tier 2 results are an *optimistic* lower bound, a bridge to real-human evidence (the BayLegal pilot design), not a substitute for it.
- **Build gates (as redirected):** Tier 1 prototyping begins once the debt track's thin-slice encoding (`DEBT_PROJECT_ARCHITECTURE_SPEC.md` §10 Phase A/B) has produced frozen items to rewrite. Tier 2 build follows a Tier 1 report and Andy's go, same as originally specified.

## Automation-leverage principles (Direction E Task 3, added 2026-07-24/2026-08-25)

Codifying the project's automation posture, applicable to both the eviction and debt lines:

1. **Purpose statement.** Automation exists to maximize the value density of every attorney-minute — absorbing everything up to the ratification moment (drafting, citation verification, consensus review, regression testing, statute/case watch, triage, evidence assembly) — and to shrink per-jurisdiction attorney load until part-time volunteer review is sufficient. **The ratification judgment itself is never automated; that boundary is what "validated" means.** Canonical illustration, on the record: the v0.3 errata cycle — AI consensus correctly flagged the C-21/C-22 disagreements; determining which side was legally correct required an attorney.
2. **Tracked metric — attorney-minutes per validated rule (AMPVR).** Estimated retrospectively for the v3 cycle as a baseline (estimation not yet performed — queued); logged prospectively per cycle in `VALIDATION_METRICS_LEDGER.md` going forward. The automation program's success criterion is a **falling AMPVR at constant-or-better validation quality** — not falling AMPVR alone, which could just mean corners cut.
3. **Tracked metric — ratification-queue health.** Open unratified proposals, their age distribution, and inflow/outflow rate. Generation capacity must not outrun ratification capacity — this is the standing queue-health discipline (`COWORK_DIRECTION_A_CADENCE_AUTONOMY.md`) applied specifically to the ratification lane. When the queue ages past a threshold (not yet proposed — a concrete number is a follow-up item), D-4-style generation throttles and triage sharpens rather than the unratified backlog silently growing. This is the same principle the debt spec's §11 execution model applies to multi-agent lane sizing ("size parallelism to what can be integrated and verified, not what can be generated").
4. **Triage automation (extends D-2).** Auto-rank queue items by (a) frequency-weighted impact of the underlying rule, (b) evidence strength, (c) staleness risk — so scarce attorney minutes land on the highest-value judgments first, rather than first-in-first-out.

## Sequencing summary

```
now         proposal 16 (self-critique + SB 1103 assessment)  — next session
   |
            proposal 17 (v0.4 drafting, ablation arm)          — after 16
            D-2 build (disagreement auto-triage)               — alongside 17, live before v0.4 scoring
   |
            Andy freeze session + v0.4 one-shot scoring         — D-2 wired and exercised live
   |
            D-3 build (statute-and-case watch)                  — first D component after v0.4 scoring
   |
            D-4 cadence proposal (standing self-critique)        — due with its own build plan
            D-5 (lift tracking)                                  — ongoing, first point = v0.4 ablation
```

Nothing here preempts proposal 16 or 17. Tasks in the 2026-07-23 Direction D directive that are documentation-level (roadmap definition, repository discoverability, cite-check, collateral versioning) run alongside; build items are slotted after the v0.4 cycle unless a component's own trigger fires earlier (as with D-2).

---

*Created 2026-07-23 per Andy's Direction D Build-Out & Open-Item Closeout directive, Task 1. No build work performed by this document — see individual component sections for build triggers.*
