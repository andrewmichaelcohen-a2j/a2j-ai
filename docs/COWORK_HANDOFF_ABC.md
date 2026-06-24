# Cowork Handoff — A/B/C Operating System: build order, what waits on Andy, what must not start early

**For:** Cowork · **From:** Andy · **Date:** 2026-06-24

This hands you three new directions (A, B, C) that together form CJaC's operating system. **Build them in the order below — do NOT start them all at once.** Standing up one cleanly, then the next, is the whole point; three half-built systems is the start/stop churn we're trying to escape. Two other docs you may hear about (the Standards Crosswalk and the Operating-Model deck) are Andy's reference/strategy artifacts — they are NOT instructions for you and you don't need them to execute.

---

## What's already in flight (keep it running underneath all of this)
These continue as the "current module on the conveyor" while A/B/C build the system around them — don't pause them to build A/B/C:
- **v3 generate-from-source holdings run** + **v3 two-rate reporting** (method rate vs. retrieval-gated rate; no-text cases quarantined to pending-retrieval, never auto-routed to attorney).
- **Background validation runner / scheduler** (overnight, unattended, provenance-complete).

If the background runner isn't fully stood up yet, finish that BEFORE layering on B and C — continuous execution first, then more architecture.

---

## Build order (sequential — confirm each before starting the next)

### 1. Direction A — Cadence + Autonomy  *(start now; foundational)*
The operating rule everything else runs under. Stand this up first:
- Implement the GREEN / YELLOW / RED decision-rule. GREEN executes and logs (no approval); YELLOW executes and flags; RED stops and escalates — only RED reaches Andy.
- Create and maintain `docs/WORK_QUEUE.md` kept several days deep (NOW / NEXT / BLOCKED / HORIZON).
- Produce the once-daily morning report in the specified shape, including the **anti-default audit** (no case goes to attorney review without recorded evidence it survived a genuine automated attempt AND couldn't reach convergence-validated).
- Report consensus as **Krippendorff's α**, not raw %.
**Gate before moving on:** the morning-report cadence is actually running and Andy is only seeing RED items.

### 2. Direction B — Golden Sets  *(the foundation; build after A is running)*
Frozen, attorney-set ground truth — the prerequisite for C.
- **PARALLEL, EARLY:** survey for existing golden sets (LSC/Temple, academic A2J benchmarks, NCSC, clinic fact-pattern banks) *before* generating from scratch. Report what's adoptable.
- Generate candidate golden cases for CA + TX notice + service. Build the train/held-out split and the scorer.
- **⛔ HUMAN-GATED STEP — this WILL pause and wait for Andy:** you DRAFT candidate answers; only Andy (named attorney) FREEZES them. Do not set, edit, or self-approve any golden answer. Mark candidates DRAFT/UNFROZEN and route to Andy. The pause is by design — flag it in the morning report and move other queued work forward while waiting.
- Enforce immutability: golden directory read-only to automation; integrity/hash check; held-out sealed.
**Gate before moving on:** at least the CA/TX bright-line golden sets are FROZEN by Andy and the scorer produces a first end-to-end score.

### 3. Direction C — Self-Optimization  *(build/run ONLY after B's golden sets exist)*
- **⛔ DO NOT BUILD OR RUN ANY PART OF C UNTIL FROZEN GOLDEN SETS EXIST (Direction B).** An optimizer with no frozen ground truth optimizes against nothing and drifts while looking productive. This is the one thing that quietly breaks the whole design.
- When B is ready: run the eval-driven loop (baseline → vary → held-out gate → promote/reject), versioned, held-out-confirmed.
- The five immutables are absolute and outside the optimizer's reach: (1) ground truth, (2) held-out set, (3) the attorney line, (4) the passing standard (only moves up), (5) the guards themselves. A score gain that requires touching any of these is cheating, not improvement — reject and log RED.

---

## The one rule that spans all three
**The system may change HOW it reaches an answer — never WHAT the right answer is.** Ground truth is attorney-set and read-only; the attorney line stays absolute; the bar only moves up. Every guard in B and C exists to enforce this. When in doubt, downgrade and surface it — a false "validated" while running unattended is the worst outcome.

---

## Quick checklist for Andy's handoff
- [ ] Confirm background runner is stood up (or stand it up first).
- [ ] Hand over **Direction A** → confirm cadence is running before proceeding.
- [ ] Hand over **Direction B** → expect a pause at the attorney-freeze step.
- [ ] Hand over **Direction C** → with explicit "do not start until B's golden sets are frozen."
- [ ] Keep the Standards Crosswalk and Operating-Model deck for yourself — not for Cowork.

*One operating system, built in order: A makes execution continuous, B makes improvement measurable, C makes it self-improving — all bounded by an immutable, attorney-set ground truth.*
