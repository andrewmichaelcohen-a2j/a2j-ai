# CJaC Work Queue

*Maintained by Cowork. Updated each morning report cycle. Cowork pulls from NEXT automatically when NOW completes — no prompt to Andy needed unless NEXT is empty or all remaining items are BLOCKED.*

**Last updated:** 2026-06-24 (morning report cycle)

---

## NOW (executing)

**Morning report — 2026-06-24**
- [x] Scan overnight output / launchd logs
- [x] Read WORK_QUEUE, DAILY_CHANGELOG, METRICS_LEDGER, HUMAN_REVIEW_QUEUE
- [x] Produce morning report
- [x] Ingest smoke test run 3 → METRICS_LEDGER
- [x] Update all living docs (this file, DAILY_CHANGELOG, STATE_OF_RECORD)

**Direction A — COMPLETE (all items done)**
- [x] Save A/B/C direction docs to docs/
- [x] Create WORK_QUEUE.md + DAILY_CHANGELOG.md
- [x] Write regression tests for l2_procedural_defects_runner (30/30 pass — confirmed 2026-06-24)
- [x] Extend dispatch.py for L2 module job type
- [x] Update morning report scheduled task to Direction A shape (GREEN log / YELLOW / RED / α / anti-default audit)
- [x] Queue full 51-state procedural defects job (`job_l2_procedural_defects_20260624.json`)

---

## NEXT (queued, ready — Cowork pulls when NOW completes)

1. **Direction B — Golden set survey** *(parallel-early, Direction B Part 1)*
   Survey LSC/Temple eviction dataset, NCSC materials, academic A2J benchmarks, legal-aid clinic fact-pattern banks for adoptable ground truth. Report what exists and what's adoptable before generating candidates from scratch.
   *Dependency:* none

2. **Full 51-state procedural defects run** — job queued (`job_l2_procedural_defects_20260624.json`)
   All 51 states × 4 defects = 204 units. Est. ~$3. **BLOCKED on launchd FDA fix (RED-strategic).**
   When unblocked: fires automatically at next 2:15 AM.

3. **Ingest overnight procedural defects results** (morning after run)
   Auto-scan output dir, ingest all new files, update docs.
   *Dependency:* item 2 must complete.

4. **Full retaliation holdings v3 Batch 3** — job queued (`job_batch3_20260623.json`)
   18 remaining states. **BLOCKED on launchd FDA fix (same as #2).**

5. **Direction B — Generate CA/TX notice + service golden set candidates**
   ~15–25 candidate fact patterns per module, with DRAFT correct answers + authority cited.
   Mark DRAFT/UNFROZEN. Route to Andy for attorney establishment (RED gate).
   *Dependency:* golden set survey complete (#1 above)

---

## BLOCKED (waiting on a named blocker)

| Item | Blocker | What unblocks it |
|------|---------|-----------------|
| launchd overnight runner (both queued jobs) | **RED-strategic — macOS TCC Full Disk Access.** Launchd agent cannot read `dispatch.py`. Error: `[Errno 1] Operation not permitted`. | Andy: System Settings → Privacy & Security → Full Disk Access → add python3. Or: approve Cowork writing a shell wrapper script (GREEN fix). |
| Direction B golden set freeze | **RED — Andy (attorney) must establish answers** | Andy signs off on DRAFT candidates → they become FROZEN |
| Direction C self-optimization | **Hard gate — Direction B frozen golden sets must exist** | B complete with ≥1 frozen set, scorer working |
| CA/summons procedural defect | **RED-interpretive — genuine MODEL-SPLIT** | GPT: CCP § 1167(a) vs Gemini: CCP § 415.45. In HUMAN_REVIEW_QUEUE. |
| CourtListener bulk-data / higher rate limit | External — CL/Free Law Project outreach | Andy's decision on timing |

---

## HORIZON (planned, not yet fully specified)

- **Direction B — Scorer build**: end-to-end scoring harness once first golden set is frozen (attorney gate)
- **Krippendorff's α in harness**: update harness.py to report α instead of raw agreement % across all protocols (YELLOW — changes existing behavior, log for ratification)
- **Full retaliation holdings run (Batch 3 results)**: ingest + update metrics after tonight's overnight run
- **L2 overlays + defenses runners**: extend L2 pattern to warranty of habitability, SCRA, discrimination once procedural defects pipeline is proven at full 51-state scale
- **PR (pending-retrieval) retry pass**: once CourtListener rate-limit situation is known, build bulk-retry job for all PR-quarantined holdings cases
- **Direction C**: build ONLY after B golden sets exist and scorer is working. Estimated: 1–2 weeks after B gate.

---

## Queue rules (Direction A)

- Cowork works NOW → pulls NEXT → keeps going. Only stops if NEXT is empty or all remaining items are BLOCKED.
- Each morning report proposes items to refill NEXT/HORIZON so the queue stays deep.
- When a RED decision is resolved, the unblocked item moves to NEXT automatically.
- Cowork may re-order within NEXT for efficiency (YELLOW), logging why.
- An item may NOT move to attorney review (RED-interpretive) without recorded evidence it survived a genuine automated attempt AND couldn't reach convergence-validated. "The model returned empty" is a pipeline problem, not an attorney item.

---

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
