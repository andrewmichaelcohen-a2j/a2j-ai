# Cowork Direction A — Revision 2: Continuous Parallel Execution

**For:** Cowork · **From:** Andy (planning with Claude) · **Date:** 2026-06-25
**Supersedes:** the single-job-per-night / 2:15am-only execution model in Direction A and the dispatcher.
**Lane:** Mostly GREEN to build (it's execution-engine plumbing), but the *throughput model change* is YELLOW — execute and flag in the morning report so Andy sees the new cadence working.

**Why this exists:** Today proved the failure mode. Under the existing model the dispatcher fires once at 2:15am, picks ONE job, and if anything blocks it (a permission wall, a bug), the entire project stalls until the next 2:15am — and nothing else runs in the meantime even though independent work was sitting ready. The pipeline itself was fine the whole time; it only ran today because Andy launched it by hand. **Execution must not depend on a single scheduled moment, on one-job-at-a-time, or on Andy initiating it manually.** This revision makes execution continuous, parallel where work is independent, and self-verifying before it queues.

> **The bar does not move.** Parallelism and continuous execution are throughput changes ONLY. Every job still clears the same validation standard, provenance rules, two-rate reporting, and the attorney line. Speed comes from running independent work concurrently and from removing external throttles — never from lowering a standard. (See "What does NOT change.")

---

## CHANGE 1 — Continuous queue draining (not one-job-at-2:15am)

Replace "fire once nightly, run one job" with **drain the queue continuously**:
- The dispatcher runs as a persistent loop (or re-fires on a short interval, e.g. every few minutes) rather than once a day. When it finishes a job, it immediately picks the next eligible job and starts it. It only idles when the queue has no eligible work.
- **Target cadence:** work ~around the clock, with a **daily review window** (~the morning report cycle) as the one synchronous pause for Andy. Andy's earlier framing is the goal: ~20+ hours/day of execution, a few-hour window each morning for report + review + queue refill, then back to draining.
- Keep `caffeinate` wrapping each run so the Mac stays awake while work is in flight (already working — visible in today's run).
- The 2:15am scheduled fire can remain as a *safety net* (in case the loop dies), but it is no longer the primary execution path. Execution is continuous.

## CHANGE 2 — Parallel execution of INDEPENDENT jobs

One-job-at-a-time was a self-imposed constraint, not a technical one. Independent jobs touch different modules/files/data and have no shared dependency — they can run concurrently.
- **Run in parallel when jobs are independent.** E.g. right now: holdings v3 (CourtListener-bound) + 51-state procedural defects (different module, no CourtListener) + Direction B golden-set survey (pure research, no pipeline) are mutually independent and could all run at once.
- **Define a simple dependency/independence check:** a job may run in parallel if it shares no output target and no rate-limited external resource with a currently-running job. Two CourtListener-heavy jobs should NOT run in parallel (they'd compete for the same throttled quota) — serialize those. A CourtListener job and a non-CourtListener job CAN run in parallel.
- **Cap concurrency** at a sane number (e.g. 2–3 simultaneous jobs) to avoid resource thrash, and respect per-resource limits (only one CourtListener-bound job at a time because of the rate limit).
- Tag each job in the queue with its resource needs (`uses: courtlistener` / `uses: openai+gemini` / `uses: none`) so the dispatcher can decide what's safe to parallelize.

## CHANGE 3 — Mandatory live-run check BEFORE queuing (the anti-"fixed-but-never-run" rule)

This is the fix for what cost the last several days. **A job is not eligible for the queue until it has been run live for one real cycle and seen to start cleanly.**
- Before any new/changed protocol or runner is queued for unattended execution, Cowork runs it once in a real invocation (small scope — a few units is enough) and confirms it actually starts processing without error.
- "AST parse clean," "import test passed," or "tests pass in sandbox" do NOT satisfy this. The sandbox cannot reach the APIs; a green sandbox check has repeatedly masked real-world failures (FDA wall, Python-version mismatch). **The check is: it ran, in the real environment, and produced output.**
- Cowork records the live-run proof (timestamp, first lines of real output, no error) in the changelog before marking the job queue-eligible.
- **Nothing is reported as "fixed" or "ready" until it has been run and the output seen.** A change that hasn't been run is a change, not a fix. State it that way in reports.

## CHANGE 4 — Self-monitoring + auto-recovery (so a stall surfaces immediately, not next morning)

- If the dispatcher loop dies or a job crashes, Cowork detects it on the next cycle and either retries (transient) or surfaces it RED immediately if it blocks all execution — it does NOT silently wait for the next scheduled window.
- **A total-execution blocker (something halting ALL jobs) is escalated as the FIRST and ONLY headline of the next report, with exact fix steps, and repeated every cycle until resolved.** Today's lesson: a blocker that only Andy can clear must be loud and unmissable, not item 3 in a tidy report. After one cycle unresolved, the report leads with nothing else.
- Heartbeat: the morning report states plainly whether execution actually ran in the last cycle (jobs completed > 0) or stalled, so "nothing ran" can never hide inside a clean-looking report again.

---

## WHAT DOES NOT CHANGE (state in every report that these held)
- Every job clears the same validation standard. Parallelism does not relax any threshold.
- Two-model-or-it-isn't-`machine-verified`; SM downgrade; STATED/INFERRED tagging; two-rate (method vs. retrieval-gated) reporting; Krippendorff's α.
- The attorney line stays absolute. `machine-verified` is below `validated`; only a named human crosses it.
- The anti-default rule: no case to attorney review without recorded evidence it survived a genuine automated attempt AND couldn't reach convergence-validated.
- The five immutables (ground truth, held-out, attorney line, passing standard, the guards).
- CourtListener stays the holdings source (right primary-law source); the throughput fix for holdings is bulk data, NOT a different/looser source. **Assume no change from Free Law Project until Andy confirms otherwise** — do not block other work waiting on it; the holdings throttle only affects holdings jobs, and everything else runs in parallel regardless.

---

## IMMEDIATE ACTIONS (today, in parallel)
1. **Let the running holdings v3 Batch 3 finish** (launched manually today — first real results coming). Ingest when done.
2. **Start the 51-state procedural defects run** — independent of holdings, no CourtListener; run it in parallel now, don't wait for tonight.
3. **Start the Direction B golden-set survey** — pure research, no dependency; pull into NOW.
4. **Build the shell wrapper** so the *scheduled* path also works as a safety net (Andy approved); live-run-verify it per Change 3 before trusting it.
5. Re-architect the dispatcher to the continuous-drain + parallel model (Changes 1–2) with the resource tags and concurrency cap.

## REPORT BACK
- Confirm the dispatcher now drains continuously and runs independent jobs in parallel (with the resource-tag/concurrency logic).
- Confirm the live-run-before-queue check is enforced, with an example proof entry.
- Confirm the heartbeat ("did execution actually run this cycle?") is in the morning report.
- Show: how many jobs completed in the last 24h (the throughput number — this is how we'll know it's working).

---

## WHAT WOULD MAKE THIS A FAILED BUILD
- Execution that still depends on a single scheduled moment or on Andy launching jobs by hand.
- Two CourtListener-bound jobs run in parallel (competing for the throttled quota).
- A job queued for unattended run without a live-run proof (repeating the "fixed but never run" failure).
- A total-execution stall that doesn't headline the next report.
- Any parallelism that bypasses a validation standard, provenance rule, or the attorney line to go faster.

---

*Cowork Direction A — Revision 2 · CJaC · 2026-06-25 · Execution is continuous and parallel, never waiting on a single 2am fire or a manual launch. Verify live before queuing. Speed from concurrency and removing throttles — never from lowering the bar.*
