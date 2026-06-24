# Cowork Direction C — Self-Optimization Loop (eval-driven, immutability-bounded)

**For:** Cowork · **From:** Andy (planning with Claude) · **Date:** 2026-06-23
**Hard prerequisite:** Direction B is live — frozen golden sets exist, train/held-out split sealed, scorer working. **Do NOT build or run any part of C until B's golden sets exist.** An optimization loop with no frozen ground truth optimizes against nothing and will drift while looking productive.
**Runs under:** Direction A's autonomy rule. Tuning runs are GREEN/YELLOW; the immutables below are RED.

**Purpose:** Move improvement from hand-tuning-in-chat (the slow loop Andy is frustrated by — one fix, one smoke test, wait) to **eval-driven optimization**: the system automatically tries variations of its own prompts, model routing, and resolution logic, scores each against the frozen golden set, and keeps what wins — validated on held-out so the wins are real. This is how the leading labs and serious legal-AI groups actually improve, and it directly serves Andy's "deliver faster validation, less defaulting to attorney review" goal: the automated resolution rate climbs against frozen truth, shrinking the attorney queue to only the genuinely interpretive residue — *provably*, because the held-out score confirms it.

**Standard basis (name it, it's citable):** this is the method behind **DSPy** (Stanford NLP), **GEPA**, and **MIPROv2** — automated prompt/program optimization against an eval set. The train/validation/held-out split is literal standard practice; DSPy's own docs warn that **"prompt-based optimizers often overfit to small training sets"** and therefore select on held-out performance. CJaC's held-out immutability guard (Part 3) is exactly that standard, applied. (Intellectual coherence bonus: DSPy and RegLab are both Stanford — the optimization layer and the hallucination evidence share a lineage.)

Andy's specific intuition is the target: models react to certain words/structures in unexpected ways; let the system find and tune those automatically instead of discovering them one painful smoke-test at a time.

---

## PART 1 — WHAT MAY BE OPTIMIZED vs. WHAT IS IMMUTABLE

### MAY be optimized (the tuning surface):
- **Prompt phrasing/structure** for the model calls (the SM-Gemini / empty-response / section-number issues are all symptoms that prompt+routing tuning addresses).
- **Model routing:** which model(s) for which module/step; when to use a second model; tie-break order; single-model fallback policy.
- **Resolution logic:** reasoning-pass parameters, token budgets, retry/backoff thresholds, consensus thresholds *upward only* (never loosened — see immutables).
- **Input shaping:** how much statute/opinion text to pass, passage selection, formatting.

### IMMUTABLE (never touched by the optimizer — RED):
1. **Ground truth.** Golden-set answers are read-only (Direction B). The optimizer may read TRAIN inputs/answers to score; it may NEVER edit an answer. Editing the grader to raise the score is the cardinal failure mode and is structurally blocked.
2. **The held-out set.** The optimizer has no read access to held-out. Held-out is touched only by the final scorer.
3. **The attorney line.** Optimization raises the `machine-verified` rate; it never promotes machine output to `validated`. Crossing that line requires a named human, always.
4. **The passing standard / provenance rules.** Two-model-or-it-isn't-`machine-verified`, STATED vs INFERRED tagging, single-model→`single-model-preliminary` downgrade, two-rate reporting (method vs retrieval-gated). The optimizer may make the pipeline *better at meeting* the standard; it may never *lower* the standard to score higher. Consensus thresholds may move up, never down.
5. **No self-modification of the guards.** The optimizer may not edit the immutability checks, the integrity/hash checks, or its own escalation rules.

**If a proposed optimization can only improve the score by touching an immutable, that is not an improvement — it is the system learning to cheat. Reject and log it RED.**

**Why these immutables are non-negotiable (the evidence):** automated prompt optimization has been shown in the research literature to *degrade safety* and even produce jailbreaks when pointed at the wrong objective — optimizers are powerful and will exploit whatever they can reach. This is **Goodhart's Law** in code form: when a measure becomes a target, it ceases to be a good measure. An optimizer that can edit its grader, see the held-out set, lower the standard, or promote its own output across the attorney line will "improve" its score while getting *worse* at the real task. Every immutable above exists to keep the optimizer's gains tied to genuinely better legal encoding, proven on data it never saw.

---

## PART 2 — THE LOOP

For each optimization cycle, against a chosen module (start: CA/TX notice — bright-line, where golden truth is solid):

1. **Baseline:** score the current pipeline config on TRAIN. Record config version + score (by difficulty band).
2. **Propose variations:** generate candidate changes to the tuning surface (Part 1) — e.g. N prompt variants, an alternate routing, a different fallback policy.
3. **Score each variant on TRAIN.** Rank by golden-set correctness. (Cost-bounded — cap variants/cycle.)
4. **Held-out gate (the overfitting guard):** take the top TRAIN candidate(s) and score on HELD-OUT.
   - Improves on BOTH train and held-out → **promote** (it's a real improvement). Version it, make it the new config, log the score delta. This is GREEN/YELLOW (reversible, versioned).
   - Improves on train but NOT held-out → **reject as overfit.** Log it (the rejection is itself useful signal about model quirks).
5. **Version + provenance:** every config is versioned; every score records which config produced it. Promotions are reversible — keep the prior config so any regression rolls back instantly.
6. **Report the delta** in the morning report's metrics section: golden-set score this cycle vs last, train and held-out both, by difficulty band.

---

## PART 3 — GUARDS THAT MAKE IT SAFE TO RUN UNATTENDED

- **Integrity check before every cycle:** verify golden-set hashes (Direction B). Mismatch → halt, report RED.
- **Held-out access control:** the optimizer process literally cannot read held-out (enforced in code/paths, not by convention). If it can, failed build.
- **Monotonic-standard check:** a config that scores higher only because a threshold was loosened or a provenance rule weakened is auto-rejected. Score gains must come from the tuning surface, not from lowering the bar. Spell out, in the report, *why* a promoted config scored higher.
- **Rollback on regression:** if a promoted config later underperforms on a fresh scoring run, auto-revert to the prior version and report.
- **Cost ceiling:** cap spend per optimization cycle (YELLOW above threshold → log; RED above a hard cap).
- **Open-textured caution:** for open-textured modules (retaliation, habitability), a high golden score does NOT upgrade the honesty label. "Structurally checked, not substantively blessed" stands regardless of optimizer performance. The optimizer can improve structural resolution; it cannot earn substantive blessing — only the attorney line does that.

---

## PART 4 — HOW THIS SHRINKS THE ATTORNEY QUEUE (the payoff, measured honestly)

The point is fewer cases defaulting to attorney review — *earned*, not assumed:
- As the golden-set score climbs (confirmed on held-out), the rate at which the pipeline correctly auto-resolves cases rises, so fewer cases hit the attorney lane for non-interpretive reasons.
- The morning report's anti-default audit (Direction A) should show the RED-attorney count *falling over time* as optimization absorbs the wording-artifact / prompt-sensitivity / routing failures that were previously masquerading as "needs a human."
- What remains in the attorney queue converges on the genuinely interpretive residue (the MD/MO/ND-type splits). That residue is the *real* attorney line — and now you can prove it's real, because everything else was handled by a system measured against frozen truth and held-out validation.

This is the honest version of "less defaulting to attorney review": not lowering the bar, but raising the machine until only genuine judgment is left — and showing the held-out score to prove the machine actually got better rather than learned to look better.

---

## REPORT BACK (per optimization cycle, folded into the morning report)
1. Module optimized, baseline vs best config, scores on TRAIN and HELD-OUT, by difficulty band.
2. What changed in the promoted config (which prompt/routing/logic change) and *why it scored higher* (must be a tuning-surface reason, not a loosened standard).
3. Rejected-overfit candidates (train-up/held-out-flat) — these reveal model quirks worth knowing.
4. Attorney-queue trend: RED-attorney count this cycle vs prior, tied to the anti-default audit.
5. Integrity confirmation: golden hashes verified, held-out never exposed, no immutable touched.

## WHAT WOULD MAKE THIS A FAILED BUILD/RUN
- Any optimization run before Direction B golden sets exist.
- The optimizer reading or tuning on held-out.
- A score gain produced by editing ground truth, loosening a threshold, or weakening a provenance rule.
- The optimizer editing its own guards, the grader, or the attorney line.
- A promoted config with no version record or no held-out confirmation.
- An open-textured "structurally checked" label upgraded to "blessed" by optimizer score.

A self-improving loop that can touch its own grader doesn't get smarter — it gets better at fooling you. Every guard here exists to keep improvement honest: gains must come from the machine doing the real task better, proven on data it never saw.

---

*Cowork Direction C — Self-Optimization Loop · CJaC · 2026-06-23 · Optimize the tuning surface against frozen truth; confirm on held-out; never touch an immutable. Build only after B. Improvement that can edit its own grader is not improvement.*
