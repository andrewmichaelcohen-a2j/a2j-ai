# CJaC Work Queue

*Maintained by Cowork. Updated each morning report cycle. Cowork pulls from NEXT automatically when NOW completes — no prompt to Andy needed unless NEXT is empty or all remaining items are BLOCKED.*

**Last updated:** 2026-06-26 evening (attach-retry-9 and notice rerun completed via run_now.sh; Counter bug fixed; Track B research done; 8 NOTICE-L2 divergences added to queue; living docs updated)

---

## NOW (executing)

*No overnight jobs queued for 2026-06-27 2:15 AM. Queue items below are for next Cowork session or next night.*

---

## Completed Today

**NV/VT case_law_candidates added** ✅ DONE — 2026-06-26 evening.
- NV: Paullin v. Sutton (1986) added to `nv_eviction_v2.json` holdings.candidates.
- VT: Houle v. Quenneville (2001) added to `vt_eviction_v2.json` holdings.candidates. CL cluster_id=2320677.
- Both UNVERIFIED; ready for holdings v3 runner on next run.

**Notice tiebreaker + NJ probe scripts queued** ✅ DONE — 2026-06-26 evening.
- `rules/validation/l2/notice_tiebreaker_20260626.py` — syntax-OK, queued, in run_now.sh.
- `rules/validation/l2/nj_attach_probe_20260626.py` — syntax-OK, queued, in run_now.sh.
- Completed jobs moved to done/. Queue refreshed.

**attach-retry-9 (failure_to_attach × 9 states)** ✅ DONE — run 2026-06-26 ~16:18 UTC, completed ~16:51.
- NSR=4 (AL, IA, RI, VA), SM=4 (ME/MN/NH=SM-GPT; NV=SM-GEMINI), ERROR=1 (NJ, persistent — 3rd failure).
- Output reconstructed from log: `validation/l2/output/l2_procedural_defects_attach_retry9_20260626.json`.
- METRICS_LEDGER updated. NJ ERROR needs pipeline investigation.

**notice provenance rerun (51 states)** ✅ DONE — run 2026-06-26 ~16:18 UTC; write_back completed all 51 states; crashed at summary (Counter bug, now fixed).
- CC=42, MODEL-SPLIT=5, PERIOD-DIVERGENCE=2, CITATION-DIVERGENCE=1, SM=1.
- 8 divergences added to HUMAN_REVIEW_QUEUE [NOTICE-L2-01]–[NOTICE-L2-09]. MD/MO corroborate existing L7s.
- GA CRITICAL: GPT says no notice required (file says 3d). Tiebreaker needed.
- Output reconstructed from log: `rules/validation/l2/output/notice_l2_raw_20260626.json`.
- Counter bug fixed: `from collections import Counter` added to l2_runner.py module-level imports.

**Track B case research (NV, NY, OK, SC, VT)** ✅ DONE — 2026-06-26 afternoon.
- NV: Paullin v. Sutton, 724 P.2d 749 (Nev. 1986) identified via Justia.
- VT: Houle v. Quenneville, 173 Vt. 80, 787 A.2d 1258 (2001) identified via Justia.
- OK: §120 confirmed wrong citation; L7-ESCALATED [OK-RET-L7-15] is correct lane.
- SC: No leading appellate case found; statute-direct (Track A) approach appropriate.
- NY: RPL §223-b solid; no Court of Appeals leading case found via web search.

**NC-17 fresh run (20f722c8)** ✅ DONE — ingested 2026-06-26 morning report.
- 50 units across 17 NC states (fresh=true CL search). MV=0, CI=0, RC=2, PR=11, perm-fail=37.
- 2 RC cases → HUMAN_REVIEW_QUEUE [NV-RET-HOLD-RC-01, NY-RET-HOLD-RC-02].
- 11 PR cases (NV/NY/OK): wrong-doc returns from CL. Need better search queries.
- 37 perm-fail: no CL candidates found for remaining states.
- First attempt failed 05:17 (sandbox path); retry succeeded 10:00 UTC (241.6 min).

**failure_to_attach re-run** ✅ DONE — ingested 2026-06-26 early morning. NSR 6→28, SM 22→8, ERROR 23→9. Both fixes validated. 2 new L7s (CT, FL). CA file updated.

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

1. **Notice tiebreaker pass — 6 states** (GREEN-AUTO → may surface YELLOWs) — run tiebreaker queries for [NOTICE-L2-01]–[NOTICE-L2-06]: AR (3d vs 5d), MN (14d vs None — post-2023 query), OR (10d vs 3d), SD (confirm repeal still good law), GA (CRITICAL: 0d vs 3d), WY (citation §1-21-1002 vs §1-21-1003). Queue TN retry (--states TN). If any tiebreaker resolves → GREEN file update. If split persists → escalate to L7.

2. **NJ failure_to_attach persistent ERROR investigation** (GREEN pipeline) — 3rd consecutive failure on NJ. Investigate: is it a network timeout? A query issue? Try manual `call_openai` / `call_gemini` for NJ failure_to_attach. If infrastructure → retry. If "no specific rule" → NSR. Anti-default: this stays pipeline until proven otherwise.

3. **NC states / retaliation holdings Track A** (GREEN — statute-direct) — 12 `__no_cases__` states + SC/NY Track A candidates. All have statutes; verify statute citations directly against primary sources. Skip CL (daily read limit constraints). This is the statute-direct path for states with no appellate case law.

4. **NV/NY Track B — add candidate cases to v2 files** (GREEN-AUTO) — Paullin v. Sutton (NV) and Houle v. Quenneville (VT) identified this session. Add as `case_law_candidates` to `nv_eviction_v2.json` and `vt_eviction_v2.json` so the next holdings v3 run has cases to verify. Prep improved CL queries for the 11 PR cases (better search terms for NV, NY, OK retaliation holdings).

5. **Direction B attorney freeze** (RED gate — needs Andy) — 50 DRAFT candidates in `rules/validation/golden_sets/`. Only frozen items become ground truth.

6. **Add `--output-suffix` option to l2_procedural_defects_runner** (YELLOW — prevents future sandbox/live collision) — add optional `--output-suffix TEXT` arg so test runs write to `*_test.json` and don't collide with live output filenames.

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
