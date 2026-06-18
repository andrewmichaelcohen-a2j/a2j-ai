# L2 Stragglers Retry + Queue Ownership — Cowork Direction

**For:** Cowork · **From:** Andy (planning with Claude) · **Date:** June 18, 2026
**Goal:** Before Andy's attorney review, strip technical noise from the L2 queue (retry the states that flagged only due to model/parse errors), and adjust the review-queue ownership so Andy's resolutions can't be overwritten. **Two discrete tasks.**

> **Session start:** read `PROJECT_STATE_OF_RECORD.md`, `PROJECT_PLAN.md`, `HUMAN_REVIEW_QUEUE.md`, `L2_CONSENSUS_REPORT_PHASE2_2026-06-18.md`.

---

## Task 1 — Retry the technical stragglers (do before Andy's review)

Several Phase 2 states flagged as MODEL-SPLIT / ERROR not because of genuine legal disagreement but because of model output errors (GPT chain-of-thought exhausting the token budget; Gemini ERR). The retry run already resolved most; a few remain noisy. **Re-run L2 cleanly on the residual error/straggler states so Andy only spends attorney time on genuine legal questions.**

- **Residual stragglers to retry:** **GA** (period-divergence / error pattern), **TN** (Gemini ERR on retry; note Andy already confirmed TN = 14 days in the L5 outlier review — likely resolves to consensus). Plus any other state still classified ERROR or carrying a PARSE_ERROR artifact rather than a substantive divergence.
- Use `max_completion_tokens=6000` (or higher if needed) so GPT's reasoning model produces JSON output cleanly. Confirm both models actually return answers (no PARSE_ERROR / ERR) before classifying.
- **Re-classify** each retried state under the tiered protocol. If it resolves to CONSENSUS-CONFIRM or AI-resolved, remove it from the L7-escalated list and update its status.
- **Distinguish technical from genuine:** a state should only remain L7-escalated if, with both models answering cleanly, they genuinely disagree on a legal question (period or characterization). A state flagged only because a model errored is NOT a legal escalation — resolve it.

**Report:** which stragglers resolved to consensus/AI-resolved vs. which remain genuine L7 items. This gives Andy a clean queue of real legal questions.

## Task 2 — Change queue ownership (single-writer protection for Andy's resolutions)

`HUMAN_REVIEW_QUEUE.md` is Andy's working document — it records his attorney determinations. Protect those from being overwritten by future runner passes.

- Change the queue header from "auto-updated by runner" to: **"Appended-to by runner (new flagged items only); resolution/status fields owned by Andy Cohen."**
- **Runner write rule going forward:** the L2 runner may only **append new flagged items** to the queue. It must **never edit or overwrite** the `Resolution`, `Authoritative source`, `Resolved by`, `Date`, or `Status` fields of existing items — those are Andy's to write.
- Update the queue (and the runner, if it auto-writes the queue) to enforce this: new items appended below; existing items' resolution fields never touched by automation.
- After Task 1, update the queue to reflect the cleaned-up state: remove stragglers that resolved, leaving only genuine L7 items + pending-confirmation items.

---

## Output / close

1. Stragglers retried; genuine-vs-technical sorted; queue reflects only real review items.
2. Queue ownership changed; runner restricted to append-only on the queue.
3. Update `PROJECT_STATE_OF_RECORD.md`: note the straggler retry results and the queue-ownership rule.
4. Commit and push. Verify on GitHub.com.

## Guardrails
- Do NOT write content corrections to rules files for the genuine L7 items yet — those wait on Andy's review.
- Do NOT touch Andy's resolution fields in the queue.
- Nothing advances past AUTOMATED-CHECKS-PASSED.

---

*L2 Stragglers Retry + Queue Ownership · June 18, 2026 · Clean the queue of technical noise before attorney review; protect Andy's resolution fields.*
