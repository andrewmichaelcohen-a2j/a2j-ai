# CJaC Work Queue

*Maintained by Cowork. Updated each morning report cycle. Cowork pulls from NEXT automatically when NOW completes — no prompt to Andy needed unless NEXT is empty or all remaining items are BLOCKED.*

**Last updated:** 2026-06-27 session (Batch 4 NC job queued; golden-set scorer harness build started)

---

## NOW (executing)

**Overnight job queued for tonight (2026-06-28 at 2:15 AM):**
- `job_fresh_nc_batch4_20260627.json` — Batch 4: 11 NC states (AL, CT, HI, LA, MI, ND, NJ, NM, OK, VT, WV), `fresh=true`, statute-targeted CL queries, sleep=15s. These states have zero MV/CI results to date. `live_verified: true`. Est. 8–14 hours.

**Direction B attorney freeze** (RED gate — Andy's action required):
- 50 DRAFT golden-set candidates in `rules/validation/golden_sets/`. Andy must personally sign off → items become FROZEN. Scorer harness being built in parallel (no attorney gate on the harness itself).

---

## Completed Today

**2026-06-27 morning report** ✅ DONE
- PR retry run ingested: all 14 states perm-fail. Root cause: `fresh=false` + no v1 draft candidates. 82 cases remain unretried. Pipeline bug logged — GREEN fix required.
- Track B (KS/NV/NY/SC) run ingested: NY — 5 MV + 1 CI + 1 PR. KS/NV/SC — perm-fail (0 CL candidates). Method rate: 83.3%. Overall rate: 45.5%.
- ny_eviction_v2.json updated: 5 MV cases + 1 CI + 1 PR under `holdings.machine_verified_cases / confirm_inference_cases / pr_cases`. validation_status → TRACK-B-RUN-COMPLETE.
- HUMAN_REVIEW_QUEUE updated: NY-HOLD-CI-01 added (Baer v. Huggins, cheap confirm lane).
- VALIDATION_METRICS_LEDGER updated: PR Retry + Track B entries added; cross-batch table updated.
- All living docs updated (WORK_QUEUE, DAILY_CHANGELOG, PROJECT_STATE_OF_RECORD, CLAUDE_CHAT_BRIEF regenerated).
- YELLOW logged for Andy: Graham Court v. Taylor (115 A.D.3d 50) classified MV by runner but court may not have stated merits.

**2026-06-27 session continuation** ✅ DONE
- Batch 3 (7e6fcf6d): ingested into METRICS_LEDGER (was already written in prior session); DAILY_CHANGELOG updated.
- NJ failure_to_attach: CONSENSUS-IMPROVE resolved; N.J. Ct. R. 6:3-4(c); nj_eviction_v2.json auto-updated. 4-run ERROR streak closed.
- PR retry job enabled: `job_retaliation_pr_retry_20260626.json` → `live_verified: true`. Andy authorized.
- Track B job created: `job_track_b_ks_nv_ny_sc_20260627.json` (KS/NV/NY/SC, fresh=true, candidates confirmed in all 4 v2 files).
- Queue hygiene: nj_attach_probe + notice_tiebreaker copied to done/ (already had live_verified=false; safe in queue/).
- Terminal cleanup note for Andy: `rm rules/validation/queue/job_nj_attach_probe_20260626.json rules/validation/queue/job_notice_tiebreaker_20260626.json` (not urgent — dispatcher skips them).

**Track A + pipeline prep (session continuation)** ✅ DONE — 2026-06-26 session.
- harness.py: `bucket: "PR"` now written for transient-failure dispositions (fixes 82-case bucket gap from nc17_fresh_v2).
- `nj_attach_retry_20260626.py`: GPT 120s timeout + consequence-framing Gemini query. Ready for Andy to run from Terminal.
- `l2_procedural_defects_runner.py`: `--output-suffix` arg added (YELLOW). Test runs write `*_suffix.json`, no live collision.
- `job_retaliation_pr_retry_20260626.json`: queued at `live_verified=false`. 14 states, 82 PR-class cases, sleep=15s. BLOCKED on Andy's call on CL timing.
- `retaliation_holdings_v3_runner.py`: statute-targeted CL queries added (`_STATE_RETALIATION_STATUTES` dict; 51 states). Next fresh run uses `NRS 118A.510 retaliation tenant landlord residential` style.
- `nv_eviction_v2.json`: Paullin v. Sutton candidate status updated to UNVERIFIED-NEEDS-CL-VERIFICATION; Track A routing added to holdings section.
- `ny_eviction_v2.json`: Track A routing added to holdings section (no leading CoA case; RPL §223-b).
- `track_a_statute_runner.py`: new runner for KS/NV/NY/SC statute-direct verification (no CL). Andy runs from Terminal; Cowork ingests output.

**NV/VT case_law_candidates added** ✅ DONE — 2026-06-26 evening.
- NV: Paullin v. Sutton (1986) added to `nv_eviction_v2.json` holdings.candidates.
- VT: Houle v. Quenneville (2001) added to `vt_eviction_v2.json` holdings.candidates. CL cluster_id=2320677.
- Both UNVERIFIED; ready for holdings v3 runner on next run.

**Notice tiebreaker + NJ probe scripts run + ingested** ✅ DONE — 2026-06-26 late evening.
- `notice_tiebreaker_20260626.py`: GA=TIEBREAKER-RESOLVED-DIFFERS-FROM-FILE (YELLOW file update applied); AR=TIEBREAKER-CONFIRM-FILE (3d confirmed correct); OR=TIEBREAKER-RESOLVED (days=10 confirmed; file already had days=10; L2 flag closed); MN/WY/TN=CONFIRM-FILE; SD=file-already-correct. **CORRECTED 2026-06-26: prior ingestion had AR/OR as L7-ESCALATED in error — actual runner output confirmed neither required L7 escalation.**
- `nj_attach_probe_20260626.py`: 3 probes all got content from Gemini; GPT timed out all 3. Classification=SM-GEMINI. NJ failure_to_attach not ERROR/NSR — needs reformulated GPT retry.
- All queue items updated in HUMAN_REVIEW_QUEUE; METRICS_LEDGER updated.

**nc17_fresh_v2 retaliation holdings run ingested** ✅ DONE — 2026-06-26 late evening.
- MV=6, CI=0, RC=3 (AK/CO/CT), PR=25, SM=0, transient-failure=84 (PR-class, harness bug: no bucket key).
- Method rate: 67%. Overall rate: 5%. Elapsed: 13.3 hours (CourtListener 429 rate-limiting).
- 3 RC cases added to HUMAN_REVIEW_QUEUE. METRICS_LEDGER updated with full run detail.

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

1. **PR retry runner v2 — design and build** (GREEN pipeline fix): The existing PR retry approach (`fresh=false` + v1 draft file) cannot reach the 82 transient-failure cases from nc17_fresh_v2. Build a dedicated runner that reads from `nc17_fresh_v2`'s output JSON (`rules/validation/l2/output/retaliation_holdings_v3_*.json`) and re-runs only the transient-failure entries with `fresh=true`. Alternative: queue a new 14-state `fresh=true` job (same design as Track B) covering the 14 states from the failed PR retry job. Simpler path — no runner changes needed. Cowork can build and queue tonight.

2. **KS/NV/SC — plan next step for zero-CL states** (YELLOW — 3 paths): (a) Use Descrybe MCP to verify model-suggested Track A candidates (Stephens v. Ludy/KS, Anvui/NV, Wadell/SC) — if verified, add to MV-class; (b) Fix `load_draft_cases()` to also read from v2 files' `holdings.candidates[]` array, so runner finds the candidates already logged there; (c) Accept Track A (statute-only) for these states. Path (b) is cleanest long-term. YELLOW because it changes existing runner behavior.

3. **Baer v. Huggins confirm** (CI cheap confirm lane) — see HUMAN_REVIEW_QUEUE [NY-HOLD-CI-01]. Attorney pull from Fastcase/Westlaw to confirm D=INFERRED case is substantive.

4. **Direction B attorney freeze** (RED gate — Andy's action required) — 50 DRAFT golden-set candidates. Must be frozen by Andy before Direction C can start.

5. **NJ failure_to_attach reformulated retry** (GREEN pipeline) — see prior entries. SM-GEMINI, needs reformulated GPT query.

6. **Terminal cleanup** (optional, low priority) — `rm rules/validation/queue/job_nj_attach_probe_20260626.json rules/validation/queue/job_notice_tiebreaker_20260626.json` from Andy's Terminal. Already in done/; live_verified=false so dispatcher skips. No urgency.

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
- **L2 overlays + defenses runners**: extend L2 pattern to warranty of habitability, SCRA, discrimination once procedural defects pipeline is proven at full 51-state scale
- **Full holdings coverage expansion**: after Track B + PR retry close KS/NV/NY/SC and 14-state PR class, remaining NC states (no candidates) need manual case research or CL bulk-data strategy
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
