# CJaC Work Queue

*Maintained by Cowork. Updated each morning report cycle. Cowork pulls from NEXT automatically when NOW completes — no prompt to Andy needed unless NEXT is empty or all remaining items are BLOCKED.*

**Last updated:** 2026-06-25 (late night — SM diagnostic complete; launchd wrapper updated; YELLOW fix proposed)

---

## NOW (executing)

*Nothing active — overnight jobs queued for 2:15 AM.*

---

## Completed Today

**NC-17 retaliation holdings v3 (run 21c5b706)** ✅ DONE — ingested 2026-06-25 late evening
- All 17 NC states → `__no_cases__` → permanent-failure. MV=CI=RC=PR=SM=0.
- Root cause: `fresh=true` was a no-op. `load_draft_cases()` doesn't search CL. Bug queued for fix.
- NC states remain NC pending `load_draft_cases()` fix + re-run.

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

1. **Andy: ratify YELLOW — max_completion_tokens 2000 → 8000** — YELLOW gate
   SM diagnostic confirmed: GPT-5.5 empty content on 119/120 SM cases = token-budget stall. Fix: raise `max_completion_tokens` to 8000 in `call_openai()` (`l2_runner.py` line 130). Expected: 70–90% SM reduction. Cowork will implement + run live sample (10 states × 1 defect, before/after measurement) once ratified.

3. **NC-17 re-run with fresh=True fix** (GREEN — runs automatically via dispatcher tonight if launchd blocker closed)
   Job queued: `queue/job_nc17_fresh_20260625.json`. Or run manually:
   ```
   cd ~/Documents/GitHub/a2j-ai && python3 rules/validation/run_protocol.py \
     --protocol retaliation_holdings_v3 \
     --states AK,AL,CO,CT,HI,KS,LA,MI,ND,NJ,NM,NV,NY,OK,SC,VT,WV \
     --fresh --run-id nc17_fresh_v2
   ```

4. **Ingest failure_to_attach overnight re-run** (GREEN — auto when done)
   Job queued: `queue/job_l2_attach_rerun_20260625.json`. Fires via dispatcher when launchd runs. Or manually: `python3 rules/validation/l2/l2_procedural_defects_runner.py --defects attach`.

5. **Direction B attorney freeze** (RED gate — needs Andy)
   50 DRAFT candidates in `rules/validation/golden_sets/`. Only frozen items become ground truth.

---

## BLOCKED (waiting on a named blocker)

| Item | Blocker | What unblocks it |
|------|---------|-----------------|
| ~~launchd overnight runner~~ | ✅ **CLOSED 2026-06-25 22:39 PT.** Live proof: `launchctl start` fired dispatcher → `[dispatch] 🚀 Launching: job_20260625_nc17_fresh` → caffeinate subprocess started → log written at `dispatch_retaliation_holdings_v3_20260626_0539.log`. `/usr/bin/python3` (CLT Python) has FDA; plist updated to call it directly. NC-17 fresh run running now. | — closed — |
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
