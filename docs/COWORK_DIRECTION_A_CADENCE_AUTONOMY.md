# Cowork Direction A — Operating Cadence + Autonomy Decision-Rule (the keystone)

**For:** Cowork · **From:** Andy (planning with Claude) · **Date:** 2026-06-23
**Status:** Foundational. Directions B (golden set) and C (self-optimization) run *under* the autonomy rule defined here. Read this first.

**Purpose:** Today the project moves through a slow synchronous loop: Cowork makes one incremental fix, runs a smoke test, and stops to wait for Andy to copy/paste a result and approve the next micro-step. The agent is fast; the *operating model* is the bottleneck. This direction changes what requires Andy's attention so Cowork executes continuously against a queue several days deep, resolves routine matters autonomously, and surfaces only genuine judgment — once a day, in a morning report.

**The goal cadence:** Cowork executes ~around the clock against a standing queue → writes a morning report → Andy (with Claude) makes only real judgment/strategy calls → the queue is refilled days ahead → no stops. Andy stops being the message bus.

---

## PART 1 — THE AUTONOMY DECISION-RULE (the core of this direction)

Every item Cowork encounters falls into exactly one of three lanes. **Cowork must self-classify every action into a lane and behave accordingly.**

### GREEN — Decide and execute autonomously. Log, do not ask.
Routine engineering and pipeline work where there is a correct answer and the test proves it. Cowork executes, verifies against a test, and records the change in the daily changelog. **No synchronous approval.** Examples:
- Bug fixes and classifier corrections caught by a test (e.g. the ERROR→SM-Gemini preservation fix — that should have just *happened*, verified by the test, logged).
- Prompt/parse/token-budget fixes for empty-response or parse-error artifacts.
- Retry passes, rate-limit pacing, retrieval re-attempts, checkpoint resumes.
- Running queued validation batches and writing provenance-complete outputs.
- Refactors, file moves, repo cleanup already listed in Open Issues.
- Anything whose success criterion is "a test passes" or "a checked output is produced."

**GREEN guardrail:** an action is only GREEN if its correctness is checkable by a test or a deterministic check. If success depends on a legal judgment, it is not GREEN.

### YELLOW — Execute, but log for morning review (reversible, judgment-informed but not legal-interpretive).
Cowork proceeds so execution never stalls, but flags the item in the report for Andy to ratify or reverse. Reversible by design. Examples:
- Choosing between two reasonable engineering approaches where one must be picked to keep moving.
- A method/config change that improves a metric but changes behavior (e.g. a new tie-break heuristic) — execute, A/B against the golden set (Direction C), log the result.
- Re-sequencing queue items for efficiency.
- De-scoping decisions already implied by the plan (e.g. Phase-1 CA-only local layer).

### RED — Stop and escalate. Do NOT decide. Surface in the report (or sooner if it blocks the queue).
Genuine legal-interpretive judgment, strategy, or anything touching an immutable. Only these reach Andy as decisions. Examples:
- **A genuine legal-interpretive split** — two models disagree on what a statute *means* or *requires* after a real resolution attempt (the MD 10-day-vs-none, MO §535.020 notice-vs-precondition, ND ripening-vs-notice items). These are the real attorney line.
- Any change to ground truth (golden-set answers), the attorney line, or a documented immutable (see Directions B/C).
- Strategic/project-level forks (outreach timing, content identity, partner approach, paper/deck claims).
- Anything that would let the machine promote its own output across the `machine-verified` → `validated` line.
- Spending above a set threshold, or anything irreversible/external-facing.

**The anti-default rule (critical — this is the "less defaulting to attorney review" instruction in force):** A case may NOT be routed to attorney review (RED) merely because the current automation didn't resolve it. Before any case is classified RED-attorney, Cowork must record that it survived a *genuine* automated attempt by the best available method **AND could not reach `convergence-validated`** (corroboration by N independent authoritative sources under the attorney-set threshold — see Direction B, Part 0). "The model returned empty / the prompt was ambiguous / retrieval failed" is a GREEN or pipeline problem to fix, NOT an attorney item. A case earns RED-attorney status by being genuinely interpretive (or open-textured beyond convergence), never by default. Distinguish in the report: **RED-interpretive** (truly needs a human), **convergence-validated** (resolved by independent-source agreement, no attorney needed), and **parked-pipeline** (automation/infra to fix first).

---

## PART 2 — THE STANDING WORK QUEUE (keep it days deep)

Maintain a `docs/WORK_QUEUE.md` ordered backlog, always populated several days ahead, so Cowork never hits "what next?" and stops. Structure:

- **NOW (executing):** the active batch/task.
- **NEXT (queued, ready):** fully specified, dependencies met — Cowork pulls from here automatically when NOW completes, no prompt to Andy.
- **BLOCKED (waiting on a RED decision or an external input):** with the specific blocker named (e.g. "waiting on CourtListener bulk-data reply," "needs Andy golden-set sign-off").
- **HORIZON (planned, not yet specified):** the days-ahead pipeline.

**Rules:**
- Cowork works NOW → pulls NEXT → keeps going. It only stops if NEXT is empty or the only remaining items are BLOCKED.
- Each morning report proposes items to refill NEXT/HORIZON so the queue stays deep. Andy/Claude approve the refill in one batched pass.
- When a RED decision is resolved, the unblocked item moves to NEXT automatically.
- Cowork may re-order within NEXT for efficiency (YELLOW), logging why.

The queue is the cure for start/stop. The decision-rule is what lets Cowork drain it without waiting on Andy for GREEN/YELLOW work.

---

## PART 3 — THE MORNING REPORT (the one synchronous touchpoint)

One report per cycle. Decision-oriented, skimmable, and it is where Andy + Claude spend their attention. Shape:

1. **Executed since last report (GREEN log):** terse changelog — what ran, what fixed, tests passing. Andy skims; no action needed.
2. **For ratification (YELLOW):** changes made that Andy can reverse — each one line + where to look.
3. **Decisions needed (RED):** the *only* items requiring Andy. Split clearly into **RED-interpretive** (real legal judgment — bring to Claude) vs. **strategic**. Each with the specific question and the options.
4. **Metrics movement:** key rates this cycle vs. last — including, once Directions B/C are live, the golden-set score and held-out score. Did automation improve? By how much? (This is how "are we getting faster/better" becomes visible instead of vibes.) **Report consensus as a chance-corrected coefficient (Krippendorff's α), not a raw agreement %** — α handles n models + missing data (e.g. GPT-empty cases) and has accepted thresholds (≥ 0.80 high-stakes; 0.67–0.79 tentative). Raw % overstates agreement by ignoring chance; α is the field standard and the more defensible number.
5. **Queue health:** NOW / depth of NEXT / what's BLOCKED and on what. If NEXT is shallow, say so and propose refill.
6. **Anti-default audit:** count of cases routed RED-attorney this cycle, each with its recorded automated-attempt evidence. If anything was routed to attorney without a genuine attempt, flag it as a process miss.

Andy + Claude respond once, batched: ratify YELLOWs, decide REDs, approve queue refill. Then Cowork runs the next cycle unattended.

---

## PART 4 — WHAT MAKES THIS WORK (and what would break it)

**Works when:** GREEN truly executes without asking; the queue stays deep; RED is reserved for real judgment; every autonomous change is test-verified and logged so Andy can audit without having watched.

**Failed cadence (call it out if it happens):**
- Cowork stops on a GREEN item to ask permission → defeats the purpose; it should have executed and logged.
- A case routed to attorney without recorded automated-attempt evidence → violates the anti-default rule.
- The queue runs dry and execution halts because NEXT wasn't refilled → planning miss, surface loudly.
- An autonomous change with no test and no changelog entry → unauditable; not allowed.
- A RED item (legal interpretation, immutable, strategy) executed without escalation → serious; these are the only things Cowork may NOT decide.

---

*Cowork Direction A — Operating Cadence + Autonomy Decision-Rule · CJaC · 2026-06-23 · GREEN executes and logs; YELLOW executes and flags; RED stops and escalates. Attorney review is earned by genuine interpretation, never reached by default. Keep the queue days deep.*
