# CJaC Work Queue

*Maintained by Cowork. Updated each morning report cycle. Cowork pulls from NEXT automatically when NOW completes — no prompt to Andy needed unless NEXT is empty or all remaining items are BLOCKED.*

**Last updated:** 2026-06-25 (evening — procedural defects ingested; NC-17 run underway)

---

## NOW (executing)

**NC-17 Retaliation Holdings v3 — fresh CourtListener run** *(launched 2026-06-25 ~5:22 PM)*
17 NC states: AK, AL, CO, CT, HI, KS, LA, MI, ND, NJ, NM, NV, NY, OK, SC, VT, WV. `fresh=true`, `sleep=10`. Early results: AK/AL → `__no_cases__` — CourtListener returned 0 results for these states even with fresh search. Others still running. Ingest when complete: say "ingest results."

---

## Completed Today

**Procedural defects 204-unit run** ✅ DONE — ingested 2026-06-25 evening
- CI=4, CC=31, NSR=6, MODEL-SPLIT=20, SM=120, ERROR=23. α_method=0.256 (n=61 dual-model)
- 4 file updates applied (IA/NY/UT/WY summons citations improved)
- 20 L7s added to HUMAN_REVIEW_QUEUE [PROC-DEF-L7-01]–[PROC-DEF-L7-20]

**Direction B — Golden-set candidate generation** ✅ DONE — 50 DRAFT candidates across 3 files (CA notice ×20, CA service ×15, TX notice ×15). All DRAFT/UNFROZEN. RED gate for attorney freeze.

**Morning report — 2026-06-25** ✅ Complete (two cycles: 08:00 + late-morning re-run)
- [x] Scan overnight output / launchd logs
- [x] Read WORK_QUEUE, DAILY_CHANGELOG, METRICS_LEDGER, HUMAN_REVIEW_QUEUE
- [x] Fix dispatch.py Python 3.9 incompatibility (`Path | None` → `Optional[Path]`) — done in 08:00 cycle; confirmed present in late-morning cycle
- [x] Produce morning report (both cycles)
- [x] Update all living docs

**Direction A — COMPLETE (all items done)**
- [x] Save A/B/C direction docs to docs/
- [x] Create WORK_QUEUE.md + DAILY_CHANGELOG.md
- [x] Write regression tests for l2_procedural_defects_runner (30/30 pass — confirmed 2026-06-24)
- [x] Extend dispatch.py for L2 module job type
- [x] Update morning report scheduled task to Direction A shape (GREEN log / YELLOW / RED / α / anti-default audit)
- [x] Queue full 51-state procedural defects job (`job_l2_procedural_defects_20260624.json`)

---

## NEXT (queued, ready — Cowork pulls when NOW completes)

1. **Ingest NC-17 retaliation results** — run in progress (Andy's Terminal)
   When complete: Cowork auto-ingests, updates METRICS_LEDGER, STATE_OF_RECORD, DAILY_CHANGELOG. Note: early AK/AL showing `__no_cases__` even with fresh=true — expect most NC states to return no CourtListener results. These will classify as NC (fresh-confirmed) in the taxonomy.

2. **failure_to_attach prompt fix + re-run** (GREEN — pipeline improvement)
   All 23 ERRORs in procedural defects run came from this defect — both models empty. Hypothesis: models can't return "none" unless explicitly permitted. Fix: update l2_procedural_defects_runner.py to add explicit "if no separate rule exists, return NO-SPECIFIC-RULE" instruction. Re-run failure_to_attach only (51 states, ~30 min). Expect ERRORs to convert to NSR. *No dependency.*

3. **Direction B attorney freeze** (RED gate — needs Andy)
   50 DRAFT candidates in `rules/validation/golden_sets/`. Review and freeze each item. Only frozen items become ground truth (immutable). No automation can proceed on B until ≥1 set is frozen.

4. **Update job queue for next overnight** (after NC-17 completes)
   Check what's in queue/ and line up next jobs for 2:15 AM. Likely: failure_to_attach re-run as l2_module job.

---

## BLOCKED (waiting on a named blocker)

| Item | Blocker | What unblocks it |
|------|---------|-----------------|
| launchd overnight runner (both queued jobs) | **RED-strategic — macOS TCC Full Disk Access.** Launchd agent cannot read `dispatch.py`. Error: `[Errno 1] Operation not permitted`. ✅ Second bug fixed (GREEN 2026-06-25): Python 3.9 type hint incompatibility in dispatch.py also fixed — `Optional[Path]`/`Tuple[bool,str]` replaces 3.10+ `Path\|None`/`tuple[bool,str]` syntax. Both fixes needed before overnight runs will succeed. | Andy: System Settings → Privacy & Security → Full Disk Access → add python3. Or: approve Cowork writing a shell wrapper script (GREEN fix). |
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
