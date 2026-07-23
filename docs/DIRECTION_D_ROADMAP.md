# Direction D — Continuous Improvement Roadmap

**Status:** ROADMAP-DEFINED. This document defines the shape and sequencing of D-2 through D-5. None of D-2–D-5 is being built by virtue of this document existing — each component starts building only when its own build trigger fires, per the sequencing below.

**D-1 (dev-set regression monitoring) is live and out of scope here** — it already ships (`rules/validation/scorer/dev_set_monitor.py`), fires on the noon dispatcher cadence, and is documented in `COWORK_DIRECTION_HOLDINGS_V3_REPORTING.md` and the ledger. This roadmap covers what comes after it.

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
