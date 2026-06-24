# CJaC Work Queue

*Maintained by Cowork. Updated each morning report cycle. Cowork pulls from NEXT automatically when NOW completes — no prompt to Andy needed unless NEXT is empty or all remaining items are BLOCKED.*

**Last updated:** 2026-06-24 (Direction A bootstrap)

---

## NOW (executing)

**Direction A — Operating Cadence + Autonomy infrastructure**
- [x] Save A/B/C direction docs to docs/
- [x] Create WORK_QUEUE.md + DAILY_CHANGELOG.md
- [ ] Write regression tests for l2_procedural_defects_runner (mock-based, sandbox-runnable)
- [ ] Extend dispatch.py for L2 module job type
- [ ] Update morning report scheduled task to Direction A shape (GREEN log / YELLOW / RED / α / anti-default audit)
- [ ] Queue full 51-state procedural defects job for tonight's 2:15 AM run

---

## NEXT (queued, ready — Cowork pulls when NOW completes)

1. **Direction B — Golden set survey** *(parallel-early, Direction B Part 1)*
   Survey LSC/Temple eviction dataset, NCSC materials, academic A2J benchmarks, legal-aid clinic fact-pattern banks for adoptable ground truth. Report what exists and what's adoptable before generating candidates from scratch.
   *Dependency:* none — starts when regression tests are done (can run concurrently with A)

2. **Ingest third smoke-test run** (`l2_procedural_defects_20260624_1646.json`)
   Update STATE_OF_RECORD + METRICS_LEDGER with procedural defects L2 smoke test results.
   Results: 1 CONSENSUS-CONFIRM (TX/summons → Rule 510.4), 2 NO-SPECIFIC-RULE (TX/NY attach), 1 SM-GEMINI (NY/summons → RPAPL § 735), 1 MODEL-SPLIT (CA/summons: § 1167(a) vs § 415.45), 1 ERROR (CA/attach both empty).

3. **Overnight: full 51-state procedural defects run**
   Job file to be queued tonight. All 51 states × 4 defects = 204 units. Est. ~$3.
   *Dependency:* dispatch.py L2 extension complete (from NOW)

4. **Ingest overnight procedural defects results** (morning after run)
   Auto-scan output dir, ingest all new files, update docs.

5. **Direction B — Generate CA/TX notice + service golden set candidates**
   ~15–25 candidate fact patterns per module, with DRAFT correct answers + authority cited.
   Mark DRAFT/UNFROZEN. Route to Andy for attorney establishment (RED gate).
   *Dependency:* golden set survey complete (#1 above)

---

## BLOCKED (waiting on a named blocker)

| Item | Blocker | What unblocks it |
|------|---------|-----------------|
| Direction B golden set freeze | **RED — Andy (attorney) must establish answers** | Andy signs off on DRAFT candidates → they become FROZEN |
| Direction C self-optimization | **Hard gate — Direction B frozen golden sets must exist** | B complete with ≥1 frozen set, scorer working |
| CA/summons procedural defect | **RED-interpretive — genuine MODEL-SPLIT** | GPT: CCP § 1167(a) vs Gemini: CCP § 415.45. Both plausible. Needs attorney determination which governs UD summons service specifically. Route to HUMAN_REVIEW_QUEUE. |
| Batch 3 holdings run (18 states) | Runs tonight at 2:15 AM via launchd | Auto-resolved overnight |
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
