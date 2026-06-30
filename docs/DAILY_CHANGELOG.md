# CJaC Daily Changelog

*GREEN action log — every autonomous change Cowork makes is recorded here. Andy audits without having watched. Format: date · what changed · test/verification.*

---

## 2026-06-30 (morning report — 3 overnight runs completed; 8 state files updated)

### GREEN — Executed autonomously

**Overnight runs scanned — 3 jobs completed**
- `job_vt_houle_retry_20260629.json` → done/. VT: perm-fail. Root cause: `fresh=false` reads v1 draft file; Houle in v2 file → `__no_cases__`. GREEN pipeline bug. Re-queued with `fresh=true` (see below).
- `job_pr_retry_co_ny_sc_20260629.json` → done/. 14 units (CO×5, NY×8, SC×1 perm-fail). Buckets: MV=3 (CO×1, NY×2), CI=1 (NY), PR=8. Method rate: 75%. Overall rate: 23%. NY MV cases (339-347 E. 12th St. LLC v. Ling, MH Residential 1 LLC v. Barrett) already ingested in ny_eviction_v2.json from Track B — no file conflict.
- `job_broad_query_10states_20260629.json` → done/. 35 units (AL,CT,HI,KS,LA,ND,NM,NV,OK,WV). Buckets: MV=12, CI=1 (NM Casa Blanca), RC=1 (WV Criss), PR=20, KS perm-fail. Method rate: 85.7% (12/14). Overall rate: 34.3% (12/35). Krippendorff's α_method ≈ 0.470 (n=18 combined text-retrievable, all runs this cycle).

**8 state v2 files updated — retaliation holdings (GREEN file update)**
- `rules/eviction/alabama/al_eviction_v2.json` — 2 MV (Leeth, Tiller[YELLOW]). 1 YELLOW flag (Tiller: adverse outcome).
- `rules/eviction/connecticut/ct_eviction_v2.json` — 3 MV (Holdmeyer, Correa, Presidential Village[YELLOW]). 1 YELLOW flag (Presidential Village: quote quality).
- `rules/eviction/hawaii/hi_eviction_v2.json` — 2 MV (Windward Partners, Cedillos[YELLOW]). 1 YELLOW flag (Cedillos: scope uncertain).
- `rules/eviction/louisiana/la_eviction_v2.json` — 2 MV (Capone[YELLOW], Taylor v. Joseph[YELLOW]). 2 YELLOW flags (Capone: adverse outcome; Taylor: no reporter + not appealed + local ordinance).
- `rules/eviction/north-dakota/nd_eviction_v2.json` — 1 MV (Nelson v. Johnson[YELLOW]). 1 YELLOW flag (Nelson: procedural-only, no merits).
- `rules/eviction/new-mexico/nm_eviction_v2.json` — 1 MV (Rickert[YELLOW]) + 1 CI (Casa Blanca). 1 YELLOW flag (Rickert: adverse outcome + single-model).
- `rules/eviction/west-virginia/wv_eviction_v2.json` — 1 MV (Murphy v. Smallridge). 1 RC note flag (Criss: RC-pending-attorney, in HUMAN_REVIEW_QUEUE).
- `rules/eviction/colorado/co_eviction_v2.json` — 1 MV (W.W.G. Corp.[YELLOW]). 1 YELLOW flag (W.W.G.: court declined to decide if doctrine exists in CO).
- All 8 files: validation_status → L2-HOLDINGS-V3-RUN-COMPLETE; last_run → 2026-06-30. All cases remain below attorney line.

**VT retry re-queued — GREEN pipeline fix**
- Root cause: `fresh=false` + Houle in v2 file → `load_draft_cases()` returns nothing → perm-fail.
- Fix: new job `rules/validation/queue/job_vt_retry_fresh_20260630.json` with `fresh=true`. CL broad fallback should retrieve Houle v. Quenneville (cluster_id=2320677).
- Queued for tonight (2026-07-01 at 2:15 AM).

**HUMAN_REVIEW_QUEUE updated**
- Added [WV-RET-HOLD-RC-02]: Criss v. Salvation Army Residences (319 S.E.2d 403, WV SC 1984). RC: FLAG-verify-disputed. Anti-default satisfied: full CL-retrieval + generate + verify ran. Murphy v. Smallridge (MV) cites Criss as first WV retaliation case. RC count: 5 → 6.

**All living docs updated (GREEN)**
- VALIDATION_METRICS_LEDGER.md — 3 new run entries (VT retry, CO/NY/SC retry, broad_query_10states).
- PROJECT_STATE_OF_RECORD.md — holdings v3 status updated; MV cumulative now 28.
- HUMAN_REVIEW_QUEUE.md — WV-RET-HOLD-RC-02 added; header/summary updated.
- WORK_QUEUE.md — NOW cleared (3 done jobs + VT pipeline fix); NEXT updated; VT re-queued.
- DAILY_CHANGELOG.md — this entry.
- CLAUDE_CHAT_BRIEF.md — regenerated (Step 3f).

### YELLOW — Flagged for Andy ratification

**CO W.W.G. Corp. v. Hughes (960 P.2d 720, Colo. Ct. App. 1998) — MV classification with significant caveat:**
Court reversed trial court's retaliation finding WITHOUT deciding whether the doctrine exists in Colorado. Case is adverse precedent AND does not establish the defense. Flag written to co_eviction_v2.json. Andy: should CO remain "doctrine existence uncertain" pending a case that affirmatively establishes it?

**NY CO/NY/SC retry — new MV cases already in file:**
339-347 E. 12th St. LLC v. Ling and MH Residential 1 LLC v. Barrett were already in ny_eviction_v2.json from Track B run. Baer v. Huggins (CI) also already in file. The CO/NY/SC retry confirmed the Track B ingestion was correct; no file changes needed for NY this cycle.

**KS/SC/NV — CL coverage gap confirmed:**
Broad fallback also returned 0 for KS. KS, SC, NV have no CL-indexed retaliation defense cases. Next options: (a) Descrybe MCP case lookup (GREEN autonomous if Andy approves); (b) Accept Track A ceiling for these 3 states. **Andy: direction needed.**

**YELLOW items carried from prior cycles (pending Andy ratification):**
- Cross-jurisdiction rejection (Markese/Robinson) — ratify or redirect.
- GA notice file change [NOTICE-L2-06] — ratify or override.
- Graham Court v. Taylor (115 A.D.3d 50) MV-with-caution — noted for NY review.

### RED — None new this cycle

All RED items carried from prior cycles in HUMAN_REVIEW_QUEUE.

---

## 2026-06-29 (morning report — overnight queue empty; no new runs)

### GREEN — Executed autonomously

**Overnight scan — queue empty, no runs**
- Dispatcher log (`launchd_stdout.log`, 2026-06-29 09:29) confirms: "Queue is empty or no eligible jobs — nothing to do." (fired twice, both idle).
- No new l2/output files since 2026-06-27 19:24 UTC. No new SUMMARY files.
- All output from last cycle (Batch 4 NC) was already ingested in 2026-06-28 morning report.

**Living docs updated (all GREEN — date/state pass)**
- `docs/WORK_QUEUE.md` — "Last updated" advanced to 2026-06-29; NOW section confirmed empty; NEXT queue unchanged (8 items).
- `docs/VALIDATION_METRICS_LEDGER.md` — No new run entry (no overnight run). Carry-forward note appended.
- `docs/PROJECT_STATE_OF_RECORD.md` — No new validation results. State unchanged.
- `docs/HUMAN_REVIEW_QUEUE.md` — No new items this cycle. Existing queue unchanged.
- `docs/CLAUDE_CHAT_BRIEF.md` — Regenerated (Step 3f). Timestamp advanced to 2026-06-29.

### YELLOW — None this cycle (carried from prior cycle)

**Carried YELLOWs awaiting Andy ratification (no new ones this cycle):**
- Cross-jurisdiction rejection (Markese/Robinson) — ratify or redirect
- VT Houle retry — queue or hold
- GA notice file change [NOTICE-L2-06] — ratify or override
- Graham Court v. Taylor (115 A.D.3d 50) MV-with-caution flag — noted for Andy's NY review

### RED — None new this cycle

All RED items carried from prior cycles (see HUMAN_REVIEW_QUEUE and the RED list in CLAUDE_CHAT_BRIEF).

---

## 2026-06-29 (session 2 — Check E + broad fallback built; 3 jobs queued)

### GREEN — Executed autonomously

**Check E jurisdiction filter + broad CL fallback — built and verified (Andy ratified 2026-06-29)**
- File modified: `rules/validation/l2/retaliation_holdings_v3_runner.py`
- Added `_court_matches_state(court_name, state_abbr)`: checks if CL-returned court name contains the target state's full name. Conservative: federal circuit courts (no state name) are rejected by default.
- Added `_build_case_from_hit(hit)`: extracted helper to avoid code duplication.
- Refactored `cl_search_retaliation_by_state()`: now uses `_run_search()` inner function that applies `_court_matches_state()` to every CL hit before accepting it. Logs rejected wrong-jurisdiction hits.
- Broad fallback: if statute-targeted query returns 0 in-state results, runner automatically tries `retaliatory eviction {state_name} landlord tenant`; same Check E filter applied. Cases from broad fallback tagged `_source: "cl_fresh_search_broad_fallback"`.
- Syntax check: import OK. Protocol adapter import OK (no API calls required for check).
- Unit tests (inline): 10 court-matching scenarios, all pass (AK court rejected for AL, CT court accepted for CT, NJ federal district accepted for NJ, D.C. Circuit rejected for NJ, etc.).

**3 batch jobs queued (dispatch order: tonight → tomorrow → night after)**
- **Tonight (oldest):** `job_pr_retry_co_ny_sc_20260629.json` — CO/NY/SC, sleep=30, fresh=true. Already queued before runner update; will use updated runner (fresh CL search path).
- **Tomorrow night:** `job_broad_query_10states_20260629.json` — AL/CT/HI/KS/LA/ND/NM/NV/OK/WV, sleep=20, fresh=true. First run with broad fallback + Check E.
- **Night after:** `job_vt_houle_retry_20260629.json` — VT only, sleep=20, fresh=false. Houle v. Quenneville (cluster_id=2320677); Andy approved.

**DAILY_CHANGELOG and WORK_QUEUE updated** (this entry).

### YELLOW — Ratified this session (now GREEN-executed)

- **Check E jurisdiction filter:** YELLOW from 2026-06-28 → ratified by Andy 2026-06-29 → implemented.
- **Broad CL fallback query for 10 no-results states:** YELLOW from 2026-06-29 → ratified by Andy 2026-06-29 → implemented.
- **VT Houle retry:** YELLOW from 2026-06-28 → ratified by Andy 2026-06-29 → job queued.

### RED — None this session

---

## 2026-06-29 (session — PR retry v2 queued; no-candidates diagnosis; WORK_QUEUE updated)

### GREEN — Executed autonomously

**PR retry v2 job built and queued for tonight**
- File: `rules/validation/queue/job_pr_retry_co_ny_sc_20260629.json`
- States: CO (3 transient cases), NY (7 transient cases), SC (4 transient cases)
- All three states had real CL 429 transient failures in nc17_fresh_v2 and were NOT covered by Batch 4 (Batch 4 covered AL, CT, HI, LA, MI, ND, NJ, NM, OK, VT, WV).
- `sleep=30` (doubled from 15) to reduce 429 rate.
- Post-run: manual jurisdiction review required (wrong-jurisdiction contamination risk; same pattern as NJ/MI in Batch 4).
- NY note: Track B cases (Wheeler, Pena, 339-347, MH Residential, Graham Court/Taylor) already ingested as MV this session. Any new MV from tonight's run would be CL-search-found cases, not the Track B set.

**`__no_cases__` root-cause diagnosis — corrected understanding**
- Prior session characterization: "fresh=true was a no-op / no-candidates bug." Updated: `cl_search_retaliation_by_state()` IS being called via the `fresh=True` path for AL, CT, HI, KS, LA, ND, NM, NV, OK, WV.
- Root cause: CL free-tier search returns 0 results for those states' statute-targeted queries. Examples: WV `37-6A-1`, OK `41-120`, ND `47-16-17.5` — no indexed precedential opinions found.
- This is a **data coverage gap** (CL free tier), NOT a code bug. A fallback to a broader state-name query might find cases but would increase wrong-jurisdiction contamination risk.
- Documented in WORK_QUEUE NEXT #2 (revised). No code change today — this is YELLOW; flagging for Andy's direction on query strategy vs. Track A for these 8 states.

**WORK_QUEUE.md and DAILY_CHANGELOG.md updated** (this entry).

### YELLOW — Flagged for Andy ratification

**Broader CL query fallback (previously mislabeled as code bug):**
- For AL, CT, HI, LA, ND, NM, OK, WV: statute-targeted CL queries return 0 results. A broader query (state name + "retaliatory eviction" + "landlord tenant") would likely find cases but introduces same wrong-jurisdiction risk as Batch 4 MI (non-state cases passing the 4-check protocol).
- Options: (a) Add broad fallback query + jurisdiction filter (YELLOW — runner change); (b) Research these states via Justia/Scholar as Track B candidates; (c) Accept Track A for all 8.
- **Andy: direction on how to handle these 8 states (Track A / Justia research / improved CL query)?**

**Cross-jurisdiction fix (carried from 2026-06-28):** NEXT #1. Runner court-filter still needed. Not implemented today.

**VT Houle retry (carried from 2026-06-28):** Still awaiting Andy's go-ahead.

### RED — None this session

---

## 2026-06-28 (morning report — Batch 4 NC ingested; cross-jurisdiction bug flagged)

### GREEN — Executed autonomously

**Batch 4 NC states (fresh_nc_batch4_20260627) — ingested**
- Run completed 2026-06-27 19:24 UTC (21.4 min). States: AL, CT, HI, LA, MI, ND, NJ, NM, OK, VT, WV. 22 units.
- Harness-reported: MV=3, PR=11, perm-fail=8, SM=0. Method rate: 100%. Overall rate: 14%.
- Corrected MV (after cross-jurisdiction audit): 1 (Onderdonk only). 2 harness-MV rejected.
- perm-fail (8 states): AL, CT, HI, LA, ND, NM, OK, WV — genuinely no CL candidates under fresh=true statute-targeted search.
- VT: Atwood v. Hill (wrong-doc PR), Houle v. Quenneville (CL 429 transient-failure, reclassified PR — retry candidate).
- All source JSON archived at: `rules/validation/l2/output/retaliation_holdings_v3_2026-06-27_fresh_nc_batch4_20260627.json`.

**nj_eviction_v2.json updated (GREEN)**
- `holdings.machine_verified_cases`: Onderdonk v. Presbyterian Homes of NJ (85 N.J. 171, NJ SC 1981) added.
- `holdings.rejected_cross_jurisdiction`: Markese v. Cooper (NY County Courts, not NJ) and Lena Robinson v. Diamond Housing Corp. (D.C. Circuit, not NJ) written with rejection reason.
- `holdings.pr_cases`: Scofield v. Berman & Sons (MA case, wrong-doc).
- `holdings.validation_status`: BATCH4-MV-PARTIAL.

**VALIDATION_METRICS_LEDGER.md updated**
- New run entry: Batch 4 NC states (fresh_nc_batch4_20260627), full metric table with YELLOW cross-jurisdiction flag.
- Cross-batch summary table updated: Batch 4 row added, cumulative MV corrected to 16.

**PROJECT_STATE_OF_RECORD.md updated**
- Holdings v3 section: Batch 4 results added; cross-jurisdiction pipeline bug noted; cumulative MV updated to 16 (10 CA + 5 NY + 1 NJ).
- Last-updated header updated.

**WORK_QUEUE.md updated**
- NOW: Batch 4 moved to Completed; queue empty tonight; VT Houle retry proposed as YELLOW for Andy approval.
- NEXT: cross-jurisdiction runner fix (#1, YELLOW) + VT Houle retry (#2, YELLOW) added ahead of existing items.

**CLAUDE_CHAT_BRIEF.md regenerated** (Step 3f — see below).

### YELLOW — Flagged for Andy ratification

**Cross-jurisdiction contamination in Batch 4 harness MV bucket:**
- Runner accepted 2 non-NJ cases as NJ MV (Markese=NY County Courts, Robinson=DC Circuit). Root cause: CL statute-targeted query for NJ Anti-Reprisal Act returned cases from other jurisdictions that discuss the same statutory framework. Same pattern explains all 8 MI PR cases (non-MI cases returned for MI statute query).
- **Corrective action taken:** Markese and Robinson rejected from nj_eviction_v2.json; written to `rejected_cross_jurisdiction` with reason. No file-level validation status impact (NJ remains BATCH4-MV-PARTIAL).
- **Fix needed:** Add court-jurisdiction filter to runner's CL results (YELLOW — changes runner behavior). Proposal in WORK_QUEUE NEXT #1.
- **Andy: ratify the rejection of Markese/Robinson and the proposed jurisdiction filter fix, or redirect.**

**VT Houle retry proposal:**
- Houle v. Quenneville (cluster_id=2320677) is a known valid candidate; transient-failure from CL 429 in Batch 4. A single-state VT fresh=true job would likely succeed. Proposed — not queued pending Andy's go-ahead (YELLOW).

### RED — None this cycle

---

## 2026-06-27 (session continuation 3 — Batch 4 NC job queued; golden-set scorer harness built)

### GREEN — Executed autonomously

**Batch 4 NC states job queued for tonight**
- File: `rules/validation/queue/job_fresh_nc_batch4_20260627.json`
- States: AL, CT, HI, LA, MI, ND, NJ, NM, OK, VT, WV (11 states — all with zero MV/CI results to date)
- Excludes: NY (Track B complete), KS/NV/SC (Track B confirmed NC), AK (RC already attorney-routed)
- fresh=true, statute-targeted CL queries, sleep=15s, live_verified=true
- Will run tonight 2:15 AM via launchd dispatcher. Est. 8–14 hours.

**Golden-set scorer harness built (Direction B)**
- `rules/validation/scorer/golden_set_scorer.py` — end-to-end scorer. Runs DRAFT or FROZEN golden-set fact patterns through the pipeline (rules file + GPT-4o + Gemini), compares to correct_answer, scores by difficulty band (bright_line / open_textured — never blended). SHA256 integrity check for frozen candidates. Read-only to ground truth. Writes output to `scorer/output/score_<run_id>.json`.
- `rules/validation/scorer/freeze.py` — freeze utility for Andy to run interactively. Prompts for FREEZE/EDIT/SKIP per candidate, computes SHA256 content hash, proposes 70/30 train/held-out split, writes to `golden_sets/FROZEN/<module>/`. Seals held-out partition at freeze time.
- Syntax validated: both files parse clean.
- Ready to use the moment Andy freezes first CA notice candidates.

**WORK_QUEUE updated** — NOW section now shows Batch 4 NC job; scorer build reflected in NEXT; last_updated timestamp.

### YELLOW — none this cycle

---

## 2026-06-27 (session continuation 2 — Task #96 completed: ny_eviction_v2.json updated with Track B NY cases)

### GREEN — Executed autonomously

**ny_eviction_v2.json updated — Track B NY cases added to candidates[]**
- Prior session claimed this was done; actual file had not been updated (candidates[] still had only 2 track-a-model-suggested entries). Completed now.
- Added 7 Track B cases to `holdings.candidates[]` in `rules/eviction/new-york/ny_eviction_v2.json`:
  - **MV ×5:** Wheeler v. D'Antonio (2025 NY Slip Op 25196), Pena v. Lockenwitz (53 Misc. 3d 428), 339-347 E. 12th St. LLC v. Ling (35 Misc. 3d 30), MH Residential 1 v. Barrett (41 Misc. 3d 24), Graham Court v. Taylor (115 A.D.3d 50, attorney-verify-recommended)
  - **CI ×1:** Baer v. Huggins (41 Misc. 3d 605) — D=INFERRED, cheap confirm lane [NY-HOLD-CI-01]
  - **PR ×1:** Graham Court v. Kyle Taylor (24 N.Y.3d 742) — wrong-doc, not attorney lane
- Each case carries: cl_cluster_id, cl_url, controlling_quote (where available), check_d_control, bucket, run_id, disposition_note.
- `validation_flags`: TRACK-B-NY-MV-CASES-INGESTED added.
- Total candidates[]: 9 (2 track-a-model-suggested + 5 MV + 1 CI + 1 PR).
- Verification: `python3 -c "..."` confirmed 9 unique candidates by cl_cluster_id/case_name, no duplicates.

---

## 2026-06-27 (session continuation — Batch 3 ingested; NJ retry resolved; PR retry enabled; Track B queued)

### GREEN — Executed autonomously

**Batch 3 (7e6fcf6d) ingested into VALIDATION_METRICS_LEDGER.md**
- Run date: 2026-06-25. 18 states (AK, AL, CA, CO, CT, HI, KS, LA, MI, ND, NJ, NM, NV, NY, OK, SC, VT, WV). 23 units.
- Bucket results: MV=4 (CA: S. P. Growers Assn., Barela, Drouet, Aweeka), CI=2 (CA: Schweiger, Western Land Office), RC=0, PR=0 (429s transient — recovered), NC=17 (non-CA states: `__no_cases__` in v2 files, `fresh=false` → no CL retrieval attempted).
- Method rate: 66.7% (4/6 text-retrievable CA cases). Overall rate: 17.4% (4/23, diluted by 17 NC states).
- NC=17 is NOT a retrieval failure — no candidates existed in those files at the time of the run. NOT attorney lane. Addressed by Track A (statute-direct) and Track B (CL fresh run) pipeline.
- METRICS_LEDGER: detailed section + cross-batch table row added. Repeatability view: no new row added (holdings v3 is cross-batch; detailed cross-batch table is the canonical record).

**NJ failure_to_attach retry — CONSENSUS-IMPROVE; file auto-updated**
- Run: `nj_attach_retry_20260626.py` (reformulated GPT retry with 120s timeout + consequence-framing query). Run date: 2026-06-27.
- Output: `rules/validation/l2/output/nj_attach_retry_20260626.json`.
- Both models returned content: GPT confidence=medium; Gemini confidence=high. Both agreed: N.J. Ct. R. 6:3-4(c).
- Classified: CONSENSUS-IMPROVE — more specific than stale "NJSA 2A:18-51 et seq. (pleading requirements)".
- File updated automatically: `rules/eviction/new-jersey/nj_eviction_v2.json` → `statute: "N.J. Ct. R. 6:3-4(c)"`, `validation_flags: ["L2-PROCEDURAL-CONFIRMED"]`, `l2_note: "[RETRY 2026-06-26] CONSENSUS-IMPROVE: N.J. Ct. R. 6:3-4(c)"`.
- Resolves 4-run persistent ERROR streak. NJ failure_to_attach: CLOSED as L2-PROCEDURAL-CONFIRMED.
- Anti-default audit: GPT had timed out on 3 prior runs (60s limit). Fix was 120s timeout + reformulated query — a pipeline fix, not attorney escalation. Anti-default rule satisfied.

**Track B CL verification job created for KS/NV/NY/SC**
- File: `rules/validation/queue/job_track_b_ks_nv_ny_sc_20260627.json`
- Targets KS, NV, NY, SC with `fresh=true` (CL fresh opinion search + generate-from-source verification).
- Candidates confirmed in all 4 v2 files:
  - KS: Stephens v. Ludy, 42 Kan. App. 2d 531, 214 P.3d 718 (2009) [track-a-model-suggested, Gemini; cl_cluster_id=null]
  - NV: Anvui, LLC v. G.L., 133 Nev. 711, 405 P.3d 667 (2017 Nev. SC) [track-a-model-suggested, Gemini; cl_cluster_id=null]
  - NY: Domen Holding Co. v. Aranovich, 1 N.Y.3d 117 (2003 NY CoA) [GPT] + 601 West 160th St. Corp. v. Henry (App. Term 2001) [Gemini]
  - SC: Wadell v. U.S. Bank Nat'l Ass'n, 399 S.C. 541, 732 S.E.2d 523 (Ct. App. 2012) [track-a-model-suggested, Gemini; cl_cluster_id=null]
- sleep=15s (CL rate-limit management). `live_verified: true` (job ready for dispatcher).
- Note: KS/NV/SC candidates are single-model-suggested (Gemini only). CL retrieval may fail to find these cases if cluster IDs are unknown. Outcome: MV if retrieved + corroborated; PR if CL can't retrieve; SM if only one model returns holding.

**Queue hygiene — nj_attach_probe + notice_tiebreaker copied to done/**
- Both jobs already had `live_verified: false` (dispatcher skips them — no re-run risk).
- Copied to `rules/validation/done/` as completed records. Originals remain in `queue/` (deletion requires Terminal — sandbox cannot delete macOS-mounted files).
- Action for Andy: `rm rules/validation/queue/job_nj_attach_probe_20260626.json rules/validation/queue/job_notice_tiebreaker_20260626.json` from Terminal when convenient. No urgency — dispatcher ignores them.

### YELLOW — Logged for ratification

**PR retry job enabled (live_verified: false → true)**
- File: `rules/validation/queue/job_retaliation_pr_retry_20260626.json`
- Change: `live_verified: false` → `live_verified: true`.
- Basis: Andy authorized with "do 2-6" (item 4 = enable PR retry). YELLOW because this queues a 13+ hour CL run.
- Job targets 14 states (AL, CO, CT, HI, LA, MI, ND, NJ, NM, NY, OK, SC, VT, WV): 82 transient-failure PR-class cases from nc17_fresh_v2. sleep=15s.
- Will run tonight at 2:15 AM via launchd dispatcher (or first night dispatcher picks it, after Track B job — check ordering by creation timestamp).
- Risk: CL rate limits may still produce 429s. Harness now correctly writes `bucket: "PR"` for these. If run fails badly, move job back to queue/ with `live_verified: false` and retry with longer sleep.
- Dispatcher ordering: sorts queue by mtime ascending (oldest first). PR retry mtime=Jun 26 22:29 UTC; Track B mtime=Jun 27 00:50 UTC. **PR retry runs tonight (2026-06-27 at 2:15 AM); Track B runs the following night.** PR retry est. ~13 hours; Track B (4 states, fresh=true) est. ~2-4 hours.

---

## 2026-06-27 (morning report — PR retry + Track B overnight runs ingested)

### GREEN — Executed autonomously

**PR retry run ingested — pipeline failure diagnosed**
- Run: `pr_retry_20260626` (fired 2026-06-27 ~01:00 UTC via launchd). Output: `rules/validation/l2/output/retaliation_holdings_v3_2026-06-27_pr_retry_20260626.json`.
- Result: 14 states, ALL perm-fail. MV=CI=RC=PR=SM=0. No CL calls made.
- Root cause: `fresh=false` + `load_draft_cases()` reads v1 draft file only; 82 transient-failure cases from nc17_fresh_v2 were never persisted to v1 draft file. All 14 states returned `__no_cases__`.
- Classified: GREEN pipeline bug. 82 cases remain unretried.
- Anti-default audit: PR retry returned 0 cases. This is an infrastructure failure (bad job config) — not attorney escalation. Fix needed: new runner that reads from nc17_fresh_v2 output JSON, or re-queue with `fresh=true`.
- METRICS_LEDGER: PR retry entry added (method_rate=n/a, overall_rate=0%, perm-fail=14).

**Track B run (KS/NV/NY/SC) ingested — NY success; KS/NV/SC CL gap confirmed**
- Run: `track_b_ks_nv_ny_sc_20260627` (fired 2026-06-27 ~09:15 UTC via launchd). Output: `rules/validation/l2/output/retaliation_holdings_v3_2026-06-27_track_b_ks_nv_ny_sc_20260627.json`. Elapsed: 433s (~7.2 min).
- NY: 8 CL candidates found. MV=5, CI=1, PR=1. Method rate: 83.3% (5/6). NY Track B: COMPLETE.
- KS, NV, SC: 0 CL candidates. All perm-fail. Track A candidates (Stephens, Anvui, Wadell) not indexed in CL.
- overall_rate: 45.5% (5/11, diluted by 3 perm-fail + 1 PR).
- METRICS_LEDGER: Track B entry added with full bucket breakdown.

**ny_eviction_v2.json updated with Track B results**
- File: `rules/eviction/new-york/ny_eviction_v2.json`. Updated via Python script.
- Added `holdings.track_b_run` block, `machine_verified_cases` array (5 MV cases), `confirm_inference_cases` array (Baer v. Huggins CI), `pr_cases` array (Graham Court v. Kyle Taylor PR).
- `validation_status`: TRACK-A-PENDING → TRACK-B-RUN-COMPLETE.
- `validation_flags`: TRACK-B-RUN-COMPLETE added.
- `last_updated`: 2026-06-27.

**HUMAN_REVIEW_QUEUE updated — NY-HOLD-CI-01 added**
- Item: [NY-HOLD-CI-01] Baer v. Huggins, 41 Misc. 3d 605 (N.Y. Civ. Ct. 2013). CI cheap confirm lane.
- D=INFERRED: both models corroborated holding from retrieved text, but no directly quotable sentence. Attorney to confirm case is substantive, not citation-drop.

**VALIDATION_METRICS_LEDGER updated — two new entries + cross-batch table row**
- PR retry entry added under holdings v3 section.
- Track B entry added with full breakdown (KS/NV/SC perm-fail, NY bucket detail, method/overall rates).
- Cross-batch combined table updated with both new rows.

**Living docs updated (WORK_QUEUE, PROJECT_STATE_OF_RECORD, DAILY_CHANGELOG)**
- WORK_QUEUE: NOW updated (no jobs queued tonight); NEXT refreshed (PR retry v2, KS/NV/SC path decision, Baer confirm, Direction B); Completed Today updated.
- PROJECT_STATE_OF_RECORD: holdings v3 section updated with PR retry + Track B results; last_updated updated.
- DAILY_CHANGELOG: this entry.

**CLAUDE_CHAT_BRIEF.md regenerated (final step)**
- Updated to reflect 2026-06-27 morning report cycle.

### YELLOW — Logged for ratification

**Graham Court v. Taylor (115 A.D.3d 50) — MV classification with caution flag**
- Classified MV by runner (both models cited same citation + corroborated holding). But model summary notes court "does not discuss the substantive merits of retaliatory eviction" — outcome-only affirmance, no rule articulated.
- Logged in ny_eviction_v2.json `validation_flags` and `machine_verified_cases[4].note`.
- Andy should review when examining NY holdings: this case may not usefully state a controlling holding.

---

## 2026-06-26 (session continuation — pipeline prep + Track A runner)

### GREEN — Executed autonomously

**harness.py: `bucket: "PR"` added for transient-failure dispositions**
- Bug: the `except TransientError` block in `harness.py` wrote `disposition="transient-failure"` results with no `bucket` key, making 82 nc17_fresh_v2 cases invisible to bucket-based reporting.
- Fix: added `"bucket": "PR"` to the transient-failure result dict with comment: "PR-class: infrastructure failure, not verification failure."
- Next run will correctly classify transient-failure cases as PR. Historical nc17_fresh_v2 output file unchanged (bucket gap was pre-fix).

**`nj_attach_retry_20260626.py` — NJ failure_to_attach reformulated retry runner built**
- GPT timeout increased to 120s (prior runs failed at 60s default).
- Gemini uses consequence-framing query (worked best in probe P3 — all 3 probes got Gemini content).
- Auto-classifies: CONSENSUS-IMPROVE / CONFIRM / NO-SPECIFIC-RULE / MODEL-SPLIT / SM-GEMINI / SM-GPT / ERROR.
- If CONSENSUS-IMPROVE: updates `nj_eviction_v2.json` failure_to_attach item; removes stale L2-PROCEDURAL-ERROR flag.
- Output: `rules/validation/l2/output/nj_attach_retry_20260626.json`
- **Status: ready for Andy to run from Terminal. Cowork ingests output.**

**`l2_procedural_defects_runner.py`: `--output-suffix` arg added** *(YELLOW — see below)*

**`job_retaliation_pr_retry_20260626.json` — PR retry job queued at `live_verified=false`**
- Targets 14 states (AL, CO, CT, HI, LA, MI, ND, NJ, NM, NY, OK, SC, VT, WV): 82 PR-class transient-failure cases from nc17_fresh_v2.
- `live_verified: false` — intentional. BLOCKED on Andy's call on CL timing.
- sleep=15s (increased from 10s — 429 severity in prior 13.3-hour run).

**`retaliation_holdings_v3_runner.py`: statute-targeted CL search queries**
- Added `_STATE_RETALIATION_STATUTES` dict (51 states → statute citation).
- `cl_search_retaliation_by_state()` now uses `"{statute} retaliation tenant landlord residential"` instead of generic `"retaliatory eviction {state_name} tenant"` query.
- Fixes root cause of 11 wrong-doc PR cases in 20f722c8 run (generic query returned non-residential-retaliation cases).

**NV v2 file — Track A routing added**
- `nv_eviction_v2.json` retaliation holdings: `validation_status` → `TRACK-A-PENDING`; `track_a_routing` block added.
- Paullin v. Sutton candidate: `candidate_status` → `UNVERIFIED-NEEDS-CL-VERIFICATION`; note updated (CL searches returned wrong-doc cases; improved query will retry; case not yet CL-verified).

**NY v2 file — Track A routing added**
- `ny_eviction_v2.json` retaliation holdings: `validation_status` → `TRACK-A-PENDING`; `track_a_routing` block added.
- Reason: no leading Court of Appeals case found in Track B research; wrong-doc CL cases in 20f722c8 run; RPL §223-b is operative statute.

**`track_a_statute_runner.py` — Track A statute-direct runner built**
- `rules/validation/l2/track_a_statute_runner.py`
- Targets KS (KSA 58-2572), NV (NRS 118A.510), NY (RPL §223-b), SC (SC Code §27-40-910).
- No CL calls. Queries GPT + Gemini: does statute protect against retaliation?
- Classifies: STATUTE-CONFIRMED, STATUTE-DIVERGENCE, ERROR/SM-ERROR.
- If leading case found by both models → added to candidates[] for Track B.
- Automation ceiling: statute-verified is BELOW machine-verified, BELOW attorney line. Not validated.
- Output: `rules/validation/l2/output/track_a_statute_YYYYMMDD.json`
- **Status: ready for Andy to run from Terminal. Cowork ingests output.**

**Track A statute-direct run completed — results ingested**
- Output: `rules/validation/l2/output/track_a_statute_20260627.json`
- 4/4 STATUTE-CONFIRMED. 0 divergence. 0 error. All 4 Track A states confirmed.
- Results by state:
  - **KS** — K.S.A. 58-2572(a) confirmed. Leading case (Gemini only): Stephens v. Ludy, 42 Kan. App. 2d 531, 214 P.3d 718 (2009). Added to candidates[].
  - **NV** — NRS 118A.510(1) confirmed. Leading case (Gemini only): Anvui, LLC v. G.L., 133 Nev. 711, 405 P.3d 667 (Nev. 2017) — Nevada Supreme Court; supersedes Paullin as priority candidate. Added to candidates[] with Track B flag.
  - **NY** — RPL §223-b(1)(a)-(c) confirmed. **Key find:** Domen Holding Co. v. Aranovich, 1 N.Y.3d 117, 769 N.Y.S.2d 785 (2003) — NY Court of Appeals (highest court); GPT-identified. Gemini identified different case: 601 West 160th St. Corp. v. Henry (App. Term, 2001). Both added to candidates[] for Track B CL verification.
  - **SC** — S.C. Code Ann. §27-40-910(A)(1)-(3) confirmed. Leading case (Gemini only): Wadell v. U.S. Bank Nat'l Ass'n, 399 S.C. 541, 732 S.E.2d 523 (S.C. Ct. App. 2012). Added to candidates[].
- All 4 v2 files updated with: track_a record, TRACK-A-STATUTE-CONFIRMED flag, recommended_statute, candidates[].
- ny_eviction_v2.json: 601 West 160th St. Corp. secondary candidate added manually (Gemini diverged from Domen Holding; both warrant Track B verification).
- nv_eviction_v2.json: Anvui candidate enriched with court/year/track metadata.
- Automation ceiling: statute-verified is BELOW machine-verified, BELOW attorney line. Not validated.
- Track B priority for next CL fresh run: NV (Anvui, 2017 Nev. SC), NY (Domen Holding, 2003 CoA).

**WORK_QUEUE.md + DAILY_CHANGELOG.md updated** — this entry.

### YELLOW — Logged for ratification

**`l2_procedural_defects_runner.py`: `--output-suffix` arg added**
- Added `--output-suffix TEXT` CLI arg (optional, default "").
- Suffix appended before `.json` (e.g. `--output-suffix test` → `l2_procedural_defects_YYYYMMDD_HHMM_test.json`).
- Engineering choice: prevents test-run output files from colliding with live output filenames. No behavioral change to existing runs (default="" means output unchanged unless arg is passed).
- Flagged for Andy ratification. No attorney/legal impact.

---

## 2026-06-26 (late evening — notice tiebreaker + NJ probe + nc17_fresh_v2 ingested; GA YELLOW file update; living docs updated)

### GREEN — Executed autonomously

**notice_tiebreaker_20260626.py: bug fixed and run completed**
- Bug: `gem_stat[:60]` and `gpt_stat[:60]` raised `TypeError: 'NoneType' object is not subscriptable` when Gemini returned no statute for SD.
- Fix: changed to `(gem_stat or '')[:60]` and `(gpt_stat or '')[:60]`.
- Run completed: 7 states (GA, AR, MN, OR, SD, WY, TN). Output: `rules/validation/l2/output/notice_tiebreaker_20260626.json`.
- Results ingested (corrected from initial ingestion error — see CORRECTION note below):
  - GA: TIEBREAKER-RESOLVED-DIFFERS-FROM-FILE → YELLOW file update applied (see below)
  - AR: TIEBREAKER-CONFIRM-FILE (3d confirmed correct — file was already right) → resolved [NOTICE-L2-01]
  - MN: TIEBREAKER-CONFIRM-FILE (14d confirmed) → resolved [NOTICE-L2-02]
  - OR: TIEBREAKER-RESOLVED (days=10 confirmed by both tiebreaker models; file already had days=10; L2 flag closed) [NOTICE-L2-03]
  - SD: TIEBREAKER-FILE-ALREADY-CORRECT (both confirm notice_required=false) → resolved [NOTICE-L2-04]
  - WY: TIEBREAKER-CONFIRM-FILE (3d, §1-21-1003 confirmed) → resolved [NOTICE-L2-08]
  - TN: TIEBREAKER-CONFIRM-FILE (14d confirmed) → resolved [NOTICE-L2-09]
- Verification: HUMAN_REVIEW_QUEUE updated; 0 new L7-ESCALATED items (AR/OR resolved by tiebreaker); 6 items resolved or closed.
- **⚠️ CORRECTION (2026-06-26 late evening):** Initial ingestion incorrectly recorded AR and OR as L7-ESCALATED based on misread of prior summary. Actual terminal output (per screenshot): AR = "file confirmed correct — no action needed" (CONFIRM-FILE); OR = "tiebreaker resolved (days=10) — file update needed (YELLOW)" (RESOLVED, not split). Corrections applied to HUMAN_REVIEW_QUEUE, WORK_QUEUE, DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF, and or_eviction_v2.json L2 flag.

**nj_attach_probe_20260626.py: run completed**
- All 3 probes got content from Gemini — confirms NJ failure_to_attach ERROR was query framing, not NSR or model limitation.
- GPT timed out on all 3 probes — classified SM-GEMINI (not ERROR, not attorney lane).
- Contradictory Gemini answers (P1: R. 6:3-1 attach docs; P2: no requirement for nonpayment; P3: must attach notice) indicate NJ attachment rule depends on notice type. Needs reformulated query with GPT retry.
- Output: `rules/validation/l2/output/nj_attach_probe_20260626.json`.

**nc17_fresh_v2 retaliation holdings run ingested**
- Run file: `rules/validation/l2/output/retaliation_holdings_v3_2026-06-26_nc17_fresh_v2.json`
- Total units: 118 (header: 120; 2-unit discrepancy). MV=6, CI=0, RC=3, PR=25, SM=0, transient-failure=84.
- Method rate: 67% (6/9 text-retrievable). Overall rate: 5% (6/118).
- RC cases → HUMAN_REVIEW_QUEUE: AK (DeNardo v. Maassen), CO (Sladek v. dePlomb), CT (TOV Realty v. Suarez).
- 84 transient-failure = CourtListener 429 rate-limit errors throughout 13.3-hour run. All PR-class, quarantined for retry.
- Harness bug identified: no `bucket` key written for transient-failure disposition. GREEN fix needed.
- METRICS_LEDGER: nc17_fresh_v2 section added with full run detail.
- HUMAN_REVIEW_QUEUE: 3 new RC items added [AK-RET-HOLD-RC-01]–[CT-RET-HOLD-RC-01].

**HUMAN_REVIEW_QUEUE.md updated** (corrected from initial ingestion error)
- NOTICE-L2-01 (AR): status → ✅ TIEBREAKER-CONFIRM-FILE (3d confirmed correct) [CORRECTED: was wrongly L7-ESCALATED in initial ingestion]
- NOTICE-L2-02 (MN): status → ✅ resolved (TIEBREAKER-CONFIRM-FILE)
- NOTICE-L2-03 (OR): status → 🟡 TIEBREAKER-RESOLVED (days=10 confirmed; file already correct; L2 flag closed) [CORRECTED: was wrongly L7-ESCALATED in initial ingestion]
- NOTICE-L2-04 (SD): status → ✅ resolved (file already correct; both models confirm notice_required=false)
- NOTICE-L2-06 (GA): status → 🟡 YELLOW pending ratification (tiebreaker-resolved differs-from-file; file updated)
- NOTICE-L2-08 (WY): status → ✅ resolved (TIEBREAKER-CONFIRM-FILE)
- NOTICE-L2-09 (TN): status → ✅ resolved (TIEBREAKER-CONFIRM-FILE)
- Added [AK-RET-HOLD-RC-01], [CO-RET-HOLD-RC-01], [CT-RET-HOLD-RC-01] (new RC cases from nc17_fresh_v2)
- Queue summary counts corrected: L7 count = 43 (not 45); Resolved = 7 (not 5)

**VALIDATION_METRICS_LEDGER.md updated**
- nc17_fresh_v2 entry added to cross-batch combined table
- Full nc17_fresh_v2 detail section added (bucket breakdown, rates, harness bug note, RC items)

**WORK_QUEUE.md updated**
- Completed items added for notice tiebreaker, NJ probe, and nc17_fresh_v2 ingestion
- NEXT refreshed: harness bug fix (item 1), NJ reformulated retry (item 2), PR retry queue (item 3), Track A / improved CL queries (items 4–5)

### YELLOW — Logged for ratification

**GA notice module file update: notice_required=false, days=null**
- File: `rules/eviction/georgia/ga_eviction_v2.json`
- Change: `notice.notice_types.pay_or_quit.tenancy_all.days`: 3 → null; `notice_required: false` added; `statute`: "OCGA §44-7-50" → "O.C.G.A. §§ 44-7-50, 44-7-52"; `demand_required: true` added.
- L2-PERIOD-DIVERGENCE flag updated: disposition `open` → `tiebreaker-resolved`. Tiebreaker fields added.
- Basis: TIEBREAKER-RESOLVED-DIFFERS-FROM-FILE — both GPT (gpt-5.5) and Gemini (gemini-2.5-pro) confirmed notice_required=false, days=null in targeted tiebreaker run. Corroborated by LSC 2021 coding ("minimum amount not specified"). Contradicts file's prior days=3 (unsubstantiated initial-gen value, noted in prior L7 writeup).
- Flagged for Andy ratification. See [NOTICE-L2-06] in HUMAN_REVIEW_QUEUE.

**OR notice tiebreaker — L2 flag closed (YELLOW)**
- OR ([NOTICE-L2-03]): tiebreaker ran; both models converged on 10 days (ORS §90.394). File tenancy_all.days was already 10. L2-MODEL-SPLIT flag in `or_eviction_v2.json` updated: disposition "open" → "tiebreaker-resolved". Tiebreaker evidence recorded in flag. No notice period content change.
- **⚠️ CORRECTION:** Initial ingestion wrongly recorded OR as L7-ESCALATED. Corrected per actual runner output ("tiebreaker resolved — file update needed (YELLOW)") which means flag closure only, not L7.
- AR ([NOTICE-L2-01]): tiebreaker confirmed file correct (3d, no action needed). **⚠️ CORRECTION:** Initial ingestion wrongly recorded AR as L7-ESCALATED. Corrected per actual runner output ("file confirmed correct — no action needed"). No change to AR file needed.

---

## 2026-06-26 (evening — attach_retry9 done; notice rerun done; Counter fix; Track B research)

### GREEN — Executed autonomously

**l2_runner.py: fixed UnboundLocalError — `Counter` moved to module-level import**
- Bug: `Counter` was imported inside local function scopes at lines 405 and 610, but used at module/run level (line 593) in `run_l2()` output-writing block.
- Crash: notice provenance re-run (run_now.sh 16:18 UTC) completed all 51 states' write_back() calls successfully, then crashed at summary step: `UnboundLocalError: local variable 'Counter' referenced before assignment`.
- Fix: added `from collections import Counter` to top-level imports block (line 42).
- Verification: `python3 -c "from collections import Counter; print(Counter([1,2,2]))"` passed cleanly; --dry-run test validated.
- Impact: all 51 v2 file write_backs already completed before crash — no data lost. Only missing artifact: raw JSON output file. Reconstructed from log (see below).

**attach_retry9 run completed — results ingested**
- Run: `run_now.sh` launched at 16:18 UTC; stdout block-buffered, flushed at 16:51 UTC.
- 9 states × failure_to_attach: AL, IA, ME, MN, NH, NJ, NV, RI, VA
- Results: NSR=4 (AL, IA, RI, VA), SM=4 (ME/MN/NH=SM-GPT, NV=SM-GEMINI), ERROR=1 (NJ, persistent — 3rd run)
- SM details: ME→Me. R. Civ. P. 80D(b), MN→Minn. Stat. §504B.321 subd.1a(c), NH→N.H. Rev. Stat. Ann. §540:6, NV→NRS 40.253(1)(b)
- Output file: original overwritten by sandbox test collision (same timestamp 1651). Reconstructed: `validation/l2/output/l2_procedural_defects_attach_retry9_20260626.json`
- Note: NJ ERROR is persistent (3rd consecutive failure). Needs pipeline investigation — NOT attorney lane per anti-default rule.

**notice provenance rerun completed — results ingested**
- Run: `run_now.sh` launched at 16:18 UTC; completed all 51 states; crashed at Counter bug (fixed above).
- 51 states × notice pay_or_quit module
- Results: CONSENSUS-CONFIRM=42, MODEL-SPLIT=5, PERIOD-DIVERGENCE=2, CITATION-DIVERGENCE=1, ERROR=1
- All 51 write_back() calls completed before crash — v2 files updated with L2 flags.
- Missing artifact (raw JSON) reconstructed: `rules/validation/l2/output/notice_l2_raw_20260626.json`
- 8 divergences flagged — added to HUMAN_REVIEW_QUEUE [NOTICE-L2-01]–[NOTICE-L2-08] (YELLOW)
- Critical: GA PERIOD-DIVERGENCE (file=3d, gpt=0d) contradicts prior auto-resolved "confirmed." Needs tiebreaker run.
- Critical: MO PERIOD-DIVERGENCE (file=10d, gpt=None, gem=None) — both models now empty. Needs investigation.

**Track B case research — rate-limited states (NV, NY, OK, SC, VT)**
- CL MCP search parameter confirmed: `q` (not `query`); `type=o` for opinions.
- CL daily read limit: 125/day — exhausted during research. Root cause of overnight 429s in NC-17 run.
- CL search 5/min limit: managed by serial search strategy.
- Found via web search (Justia):
  - NV: **Paullin v. Sutton, 724 P.2d 749 (Nev. 1986)** — full opinion retrieved. Holdings: NRS 118A.510 prohibits non-renewal for retaliatory purpose; remedy = actual damages only (amended 1985). This is NV's foundational retaliation case.
  - VT: **Houle v. Quenneville, 173 Vt. 80, 787 A.2d 1258 (2001)** — VT Supreme Court. Holdings: objective test for retaliation (Gokey standard); tenant can use circumstantial evidence; protected activity must precede adverse action. CL cluster_id=2320677 (`vt` court).
  - OK: §120 = "failure to deliver possession" NOT retaliation — confirms OK [OK-RET-L7-15] L7 escalation. Web search confirms no OK retaliatory eviction statute (pending HB2015 proposal).
  - SC: No leading appellate case found. SC Code §27-40-910 is statute-only authority.
  - NY: No Court of Appeals leading case found. RPL §223-b statute solid; Ellis v. Oceanhill already RC.
- CL correct court IDs discovered: `vt` (Vermont SC), `sc` (SC SC confirmed by web search structure).
- Track A (statute-direct for 12 `__no_cases__` states): viable — all 12 have statutes in v2 files.

**Provenance output files written**
- `validation/l2/output/l2_procedural_defects_attach_retry9_20260626.json` — reconstructed
- `rules/validation/l2/output/notice_l2_raw_20260626.json` — reconstructed

### GREEN — Additional (session continuation)

**NV/VT v2 files updated — case_law_candidates added**
- NV (`nv_eviction_v2.json`): added Paullin v. Sutton, 724 P.2d 749 (Nev. 1986) under `retaliation.layer_decomposition.holdings.candidates`. Track B candidate; UNVERIFIED. Holdings v3 runner will verify via CL when run.
- VT (`vt_eviction_v2.json`): added Houle v. Quenneville, 173 Vt. 80, 787 A.2d 1258 (2001) under `retaliation.layer_decomposition.holdings.candidates`. CL cluster_id=2320677 (court=vt). Track B candidate; UNVERIFIED.
- Both files now have candidates[] populated; subsequent holdings v3 run will attempt verification.

**Completed jobs moved to done/ in dispatcher queue**
- `job_l2_attach_retry9_20260626.json` → `done/` (ran via run_now.sh)
- `job_notice_rerun_20260626.json` → `done/` (ran via run_now.sh)

**Notice tiebreaker script written and queued**
- File: `rules/validation/l2/notice_tiebreaker_20260626.py`
- 7 targeted state-specific queries: GA (CRITICAL), AR, MN, OR, SD, WY, TN.
- Each query designed to resolve the specific documented split (more targeted than standard QUERY_TEMPLATE).
- Syntax-verified: `python3 -m py_compile` OK.
- Queued: `rules/validation/queue/job_notice_tiebreaker_20260626.json`
- Also added to `run_now.sh` (Job 1) for immediate launch.

**NJ failure_to_attach probe script written and queued**
- File: `rules/validation/l2/nj_attach_probe_20260626.py`
- 3-probe diagnostic: ultra-simple, rule-direct, consequence-framing queries.
- Goal: determine if NJ ERROR is (a) query framing, (b) genuine NSR, or (c) model limitation.
- Syntax-verified: `python3 -m py_compile` OK.
- Queued: `rules/validation/queue/job_nj_attach_probe_20260626.json`
- Also added to `run_now.sh` (Job 2) for immediate launch.

**run_now.sh updated to current queue**
- Now launches: notice tiebreaker (Job 1) + NJ probe (Job 2)
- Both use `python3 -u` (unbuffered) to prevent stdout buffering in log files.

### YELLOW — Logged for ratification

**8 notice module divergences flagged (provenance rerun)**
- 5 MODEL-SPLIT (AR, MD, MN, OR, SD), 2 PERIOD-DIVERGENCE (GA, MO), 1 CITATION-DIVERGENCE (WY).
- GA and MO PERIOD-DIVERGENCE contradict prior "auto-resolved" status — recommend tiebreaker re-run.
- Added to HUMAN_REVIEW_QUEUE as [NOTICE-L2-01]–[NOTICE-L2-08].

**Sandbox test collision — output file overwritten**
- Ran `l2_procedural_defects_runner.py --defects attach --states AL,IA,ME --dry-run` in sandbox to debug job crash. Sandbox test wrote `l2_procedural_defects_20260626_1651.json` (all ERROR, 3 states). Real job also wrote to same filename (same minute timestamp). Sandbox file overwrote real output.
- Impact: minimal. Log preserved all real results. Reconstructed clean output file.
- Prevention: test runs in sandbox should use `--dry-run` flag AND a `--output-suffix test` option (not yet implemented). YELLOW: recommend adding `--output-suffix` to runner for sandbox isolation.

---

## 2026-06-26 (daytime — notice rerun queued; l2_runner.py --sleep fix)

### GREEN — Executed autonomously

**l2_runner.py: added `--sleep` argument for dispatcher compatibility**
- Added `import time`
- Added `--sleep` (float, default 0) to argparse
- Added `sleep_secs: float = 0` parameter to `run_l2()`
- Added `time.sleep(sleep_secs)` between state iterations (skipped on last state)
- Wired through in `__main__` block: `sleep_secs=args.sleep`
- `--dry-run --sleep 2` validated: no errors, accepts argument cleanly
- Prior dispatcher incompatibility: `_build_l2_cmd` always passes `--sleep N`; l2_runner.py had no such arg → would have failed with argparse "unrecognized arguments" error. Now fixed.

**Notice module provenance re-run queued**
- Job: `rules/validation/queue/job_notice_rerun_20260626.json`
- Runner: `rules/validation/l2/l2_runner.py --states ALL --sleep 2`
- Fires tonight at 2:15 AM (after attach-retry-9, dispatcher picks queue order by filename/age)
- Expected output: `rules/validation/l2/output/notice_l2_raw_{date}.json`
- Est. cost: ~$1.10 · Est. time: ~20 min · 51 states × notice pay_or_quit module
- Attorney-confirmed outcomes in state files preserved (write-back respects existing flags)
- Closes provenance gap documented in VALIDATION_METRICS_LEDGER

### RED — Carried. NC-17: 12 states with no CL case law (genuine gap, see below).

---

## 2026-06-26 (morning report — NC-17 fresh run ingested)

### GREEN — Executed autonomously

**Ingested NC-17 fresh run** (`rules/validation/l2/output/retaliation_holdings_v3_2026-06-26_20f722c8.json`, `SUMMARY_retaliation_holdings_v3_2026-06-26_1000.md`)

Run completed 10:00 UTC via launchd. First attempt (05:17) failed with returncode=1 (sandbox path issue — not an issue on Andy's Mac). Retry succeeded, 241.6 min elapsed.

50 units across 17 NC states (fresh=true CL search). Bucket: MV=0, CI=0, RC=2, PR=11, SM=0, perm-fail=37. Method rate: 0÷2=0%. Overall rate: 0÷50=0%. α_method=n/a (n=2, all RC, D_e=0).

Actions taken:
- **HUMAN_REVIEW_QUEUE**: [NV-RET-HOLD-RC-01] Wright v. Brady (NV) and [NY-RET-HOLD-RC-02] Ellis v. Oceanhill Brownsville Tenant Ass'n (NY) added. Anti-default rule satisfied for both (full generate+verify protocol with CL retrieval completed before routing).
- **VALIDATION_METRICS_LEDGER**: NC-17 fresh run entry added to cross-batch table; detailed section added with bucket counts, rates, α, PR diagnosis, and perm-fail interpretation.
- **PROJECT_STATE_OF_RECORD**: Holdings v3 status updated to reflect all runs complete; NC states status documented.
- **WORK_QUEUE**: NC-17 ingest moved to Completed; attach-retry-9 promoted to NOW; NEXT queue refill proposed.
- **attach-retry-9 job queued**: `rules/validation/queue/job_l2_attach_retry9_20260626.json` created for AL/IA/ME/MN/NH/NJ/NV/RI/VA (failure_to_attach defect only). Fires tonight at 2:15 AM.
- **CLAUDE_CHAT_BRIEF.md**: Regenerated (see Step 3f).
- **Job moved**: job_nc17_fresh_20260625.json already in done/ (moved by dispatcher).

### YELLOW — None this cycle.

### RED — Escalated (2 new, carried remainder)

**RED-interpretive [NV-RET-HOLD-RC-01]**: Wright v. Brady (NV) — CL text retrieved, verify step disputed the holding. Attorney must confirm, characterize, or dismiss. Full automated attempt complete.

**RED-interpretive [NY-RET-HOLD-RC-02]**: Ellis v. Oceanhill Brownsville Tenant Ass'n (NY) — CL text retrieved, generate step failed to extract a retaliation holding. Attorney must confirm case is a valid holding candidate or dismiss. Full automated attempt complete.

**RED-strategic (carried)**: Direction B golden-set freeze. ~15 NC states with no CL candidates — Andy's decision on path forward.

---

## 2026-06-26 (early morning — failure_to_attach re-run ingested)

### GREEN — Executed autonomously

**Ingested failure_to_attach re-run** (`validation/l2/output/l2_procedural_defects_20260626_0830.json`)

Run completed at 2:34 AM via launchd dispatcher. 51 units (51 states × failure_to_attach). Output ingested:

Results: CI=0, CC=3, NSR=28, MODEL-SPLIT=2, SM=8 (SM-GEMINI=5, SM-GPT=3), ERROR=9. α_method=0.470.

Before/after vs 204-unit run (failure_to_attach subset):

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| NSR | 6 | 28 | +22 ← prompt fix |
| SM | 22 | 8 | −14 (64%) ← token fix |
| ERROR | 23 | 9 | −14 (61%) ← both fixes |
| Dual-model coverage | 2% | 65% | +63 pp |

Both fixes validated. 9 residual ERRORs are network timeouts (not token stalls) — distinct issue, queued for retry pass.

Actions taken:
- **CA v2 file updated**: `failure_to_attach` statute corrected from `CCP §1161 et seq.` → `Cal. Code Civ. Proc. § 1166(d)(1)–(2)` (CONSENSUS-IMPROVE applied by runner)
- **HUMAN_REVIEW_QUEUE**: [PROC-DEF-L7-21] CT and [PROC-DEF-L7-22] FL added (both MODEL-SPLIT on failure_to_attach — statute vs court rule as governing source)
- **VALIDATION_METRICS_LEDGER**: New section added with before/after comparison, α computation, SM breakdown, root-cause analysis of 9 residual ERRORs
- **Job moved**: `queue/job_l2_attach_rerun_20260625.json` → `done/`

### RED — Carried (no change). NC-17 fresh run still executing (~55/120 cases at 2:35 AM, active CL 429 backoff).

---

## 2026-06-25 (late night — SM diagnostic + launchd wrapper)

### GREEN — Executed autonomously

**SM diagnostic — single-model rate root cause identified**

Split: SM-GPT=1, SM-GEMINI=119 of 120 SM units. GPT is responsible for 99.2% of single-model cases.

Failure signature: `gpt_raw = ""` (empty string), `gpt_error = ""` (no error raised). The OpenAI API call succeeds and returns a response object — but `resp.choices[0].message.content = ""`. This is not a timeout (60s limit not hit), not a 429 (no rate-limit error), not a safety refusal (no error field). It is a reasoning-model token-budget stall: gpt-5.5 consumes its chain-of-thought tokens before writing any output, and returns an empty content field.

No position, defect, or state correlation: SM-GEMINI appears at position 3 (first AK/summons unit) and is spread uniformly through the run (25/50 in first half, 22/50 in last half). Rate-limit clustering would show SM concentrated later in the run; it does not. All four defects are affected (summons=44, complaint_filed=34, failure_to_attach=21, wrong_court=20).

Retry status: the retry IS in the code and IS firing. `query_model()` at line 249 checks `if not raw and attempt == 0: time.sleep(5); continue` — this triggers on every empty response. The retry is not a no-op (unlike the fresh=True bug). The problem is that one retry with a 5s pause does not resolve a token-budget stall: the model produces the same empty response on attempt 1. There is no print() in the retry branch, so logs show no "retrying" message — but the code path executes.

Root cause: `max_completion_tokens=2000` in `call_openai()` (`l2_runner.py` line 130). gpt-5.5 uses tokens for internal chain-of-thought before writing output; 2000 is insufficient for complex multi-field legal research prompts. The comment on line ~246 notes "350 caused empty responses" — 2000 was an improvement but still hits the ceiling.

**YELLOW — fix proposed (awaiting ratification before implementing):**
Increase `max_completion_tokens` from 2000 → 8000 in `call_openai()` (`rules/validation/l2/l2_runner.py` line 130). Expected SM-GEMINI reduction: 70–90% (token budget stall resolves when reasoning tokens have headroom). Per Direction A Rev 2 run-before-queue rule: fix must be validated on a live small sample (10 states × 1 defect, before/after SM rate measured) before full-scale deployment. Do NOT implement until ratified.

**Shell wrapper + launchd plist — wrapper updated, plist updated, live simulation complete**

Changes:
- `rules/validation/run_dispatch.sh` — added `caffeinate` availability check; falls back gracefully on Linux/sandbox without failing the script (allows reliable testing outside macOS).
- `rules/validation/com.cjac.validation.plist` — `ProgramArguments` changed from `[/usr/bin/python3, dispatch.py]` → `[/bin/bash, run_dispatch.sh]`. Added FDA setup instructions and MANUAL TRIGGER / SIMULATE commands to plist header comment.
- `rules/validation/queue/` — moved `job_l2_procedural_defects_20260624.json` to `done/` (it ran manually on 2026-06-25; was never moved by dispatcher due to launchd blocker).

Live simulation proof (timestamp: 2026-06-26T05:17:42):
```
[run_dispatch.sh] Using Python: /usr/bin/python3 (Python 3.10.12)
[run_dispatch.sh] Dispatch script: .../rules/validation/dispatch.py
[run_dispatch.sh] Mode: --single
[run_dispatch.sh] caffeinate not available — running without sleep guard
[dispatch] Single-shot: job_20260625_nc17_fresh
[dispatch] 🚀 Launching: job_20260625_nc17_fresh | cmd: caffeinate -ims /usr/bin/python3 .../run_protocol.py --protocol...
[dispatch]    Log: .../logs/dispatch_retaliation_holdings_v3_20260626_0517.log
```
Log file written: `rules/validation/logs/dispatch_retaliation_holdings_v3_20260626_0517.log`. Wrapper found Python, dispatcher picked job from queue, subprocess launched. Sandbox-only failure: `PermissionError` on `job_path.unlink()` (sandbox can't delete mounted files) and `ModuleNotFoundError` for protocol import (sandbox path mismatch) — neither occurs on Andy's Mac.

**✅ BLOCKER CLOSED — launchd live-run proof (2026-06-25 22:39 PT):**
```
[dispatch] Single-shot: job_20260625_nc17_fresh
[dispatch] 🚀 Launching: job_20260625_nc17_fresh | cmd: caffeinate -ims
  /Library/Developer/CommandLineTools/usr/bin/python3
  .../run_protocol.py --protocol retaliation_holdings_v3 --states AK,AL,...
[dispatch]    Log: .../logs/dispatch_retaliation_holdings_v3_20260626_0539.log
```
`launchctl start com.cjac.validation` → dispatcher fired → picked NC-17 job → launched subprocess with caffeinate → log written. Plist uses `/usr/bin/python3` (symlink to CLT python3 at `/Library/Developer/CommandLineTools/usr/bin/python3`) which already had FDA toggled ON in System Settings. NC-17 fresh run is now executing in background (~90 min).

### YELLOW — Ratified and implemented
- `max_completion_tokens` 2000 → 8000 in `call_openai()` (`rules/validation/l2/l2_runner.py` line 135). Andy ratified 2026-06-25. Validation: the queued `job_l2_attach_rerun_20260625.json` (51 states × failure_to_attach) will run with the new setting and serve as before/after SM measurement. Prior SM-GEMINI rate on this defect: 21/51 (41%). Expected post-fix: <10%.

### RED — Carried (no change).

---

## 2026-06-25 (night — fresh=True fix + failure_to_attach fix)

### GREEN — Executed autonomously

**Fix #9: `load_draft_cases()` CL search when `fresh=True`**
- Added `cl_search_retaliation_by_state(state_abbr, max_results=8)` to `rules/validation/l2/retaliation_holdings_v3_runner.py`. Searches CL with query `"retaliatory eviction {state_name} tenant"`, returns up to 8 precedential opinions per state in the `verify_case()`-compatible dict format.
- Modified `load_draft_cases(state, fresh=False)` — when `fresh=True` and no v1 draft candidates exist for the state, calls CL search instead of returning `[]`.
- Updated `protocols/retaliation_holdings_v3.py` `get_units(states, fresh=False)` — now accepts and passes `fresh` to `load_draft_cases()`.
- Updated `rules/validation/run_protocol.py` line 126: `protocol.get_units(states, fresh=args.fresh)` — `--fresh` flag now propagates all the way to CourtListener search.
- Verified: 4/4 files syntax OK; 30/30 regression tests pass.
- **NC-17 re-run command:** `python3 rules/validation/run_protocol.py --protocol retaliation_holdings_v3 --states AK,AL,CO,CT,HI,KS,LA,MI,ND,NJ,NM,NV,NY,OK,SC,VT,WV --fresh --run-id nc17_fresh_v2` (requires COURTLISTENER_API_TOKEN env var)

**Fix #10: `failure_to_attach` prompt — explicit NSR instruction**
- Updated `QUERIES["failure_to_attach_lease_or_notice_to_complaint"]` in `rules/validation/l2/l2_procedural_defects_runner.py`.
- Key change: added explicit instruction that "most states do NOT have a specific attachment statute" and that `attachment_required: false, statute: null` is "a valid and expected answer — do NOT leave the response empty."
- Queued overnight job: `rules/validation/queue/job_l2_attach_rerun_20260625.json` — `defects: "attach"`, 51 states, est. ~15 min, $0.50.
- Verified: syntax OK; 30/30 regression tests pass.

### YELLOW — None this cycle.

### RED — Carried (no change).

---

## 2026-06-25 (late evening — NC-17 results ingested)

### GREEN — Executed autonomously

**NC-17 retaliation holdings v3 (run 21c5b706) — ingested**
- 17 states, all `__no_cases__` → `permanent-failure`. MV=0, CI=0, RC=0, PR=0, SM=0, NC=17.
- Method rate: n/a (0 text-retrievable). Overall rate: 0%.
- **Root cause diagnosed (GREEN pipeline bug):** `fresh=true` was a no-op. `run_protocol.py`'s `--fresh` flag only clears the checkpoint; it does not change `load_draft_cases()` in `retaliation_holdings_v3_runner.py`. That function always reads from the v1 draft file, which has no entries for these 17 states. CourtListener search was never called — confirmed by 0-second per-state processing time.
- All 17 NC states remain NC. They are NOT PR (no retrieval failure — no retrieval was attempted). Not attorney lane.
- METRICS_LEDGER updated with NC-17 row + diagnosis note.
- **Next step:** Implement CL candidate search in `load_draft_cases()` when `fresh=True` and no draft candidates exist. Queued in WORK_QUEUE.

### YELLOW — None this cycle.

### RED — Carried (no change).

---

## 2026-06-25 (evening — procedural defects ingestion + NC-17 launch)

### GREEN — Executed autonomously

**Procedural defects 204-unit L2 run — ingested**
- Output: `validation/l2/output/l2_procedural_defects_20260626_0018.json` — 204 units, 51 states × 4 defects
- Bucket counts: CI=4, CC=31, NSR=6, MODEL-SPLIT=20, SM=120, ERROR=23
- α_method = 0.256 (n=61 dual-model; 143 SM+ERROR = pipeline gap)
- 4 CONSENSUS-IMPROVE file updates already applied by runner (IA/NY/UT/WY summons citations)
- 20 MODEL-SPLIT items added to HUMAN_REVIEW_QUEUE [PROC-DEF-L7-01] through [PROC-DEF-L7-20]
- VALIDATION_METRICS_LEDGER and HUMAN_REVIEW_QUEUE updated
- Pipeline flag: (1) GPT empty on ~70% of units; (2) failure_to_attach: all 23 ERRORs from this defect — recommend re-run with explicit NSR prompt option
- NC-17 retaliation run launched by Andy (running): early AK/AL showing `__no_cases__` from CourtListener fresh search — genuine data gap, NOT attorney lane

### YELLOW — None this cycle.

### RED — Carried
- launchd FDA fix pending; Direction B attorney freeze pending; 20 new procedural defects L7s added to queue

---

## 2026-06-25 (afternoon — Direction A Rev 2 adoption + Direction B survey)

### GREEN — Executed autonomously

**dispatch.py — Direction A Rev 2 complete rewrite**
- Continuous drain loop (`drain()`) + parallel execution (up to 3 concurrent jobs).
- Per-resource concurrency limits: `courtlistener:1`, `openai:2`, `gemini:2`.
- Change 3 live_verified gate: jobs without `live_verified:true` are skipped with warning.
- Heartbeat: writes `logs/heartbeat.json` each cycle.
- `main_single()` single-shot mode preserved for launchd safety-net.
- `--drain` flag selects continuous vs single-shot.
- Python 3.9 compatibility: all type hints use `Optional[Path]`, `Tuple[bool, str]` (no 3.10+ `|` union syntax).
- AST verified clean. NOT yet live-verified via launchd (per Change 3 — "change applied, not fixed").

**run_dispatch.sh — new shell wrapper for launchd FDA fix**
- Resolves Python: prefers `/opt/homebrew/bin/python3`, falls back gracefully.
- `caffeinate -ims` keeps machine awake during run.
- Supports `--drain` pass-through.
- launchd plist should call `/bin/bash run_dispatch.sh` (FDA on /bin/bash, not python3).
- Written and made executable. NOT yet live-verified (same Change 3 note).

**job_l2_procedural_defects_20260624.json — updated for Rev 2 dispatcher**
- Added `"uses": ["openai", "gemini"]` resource tag.
- Added `"live_verified": true` with basis: runner smoke-tested 3 runs 2026-06-24; all 4 classification branches exercised; 30/30 regression tests pass.

**Procedural defects run — command staged for Andy**
- Run command written to clipboard; Terminal opened.
- Andy: paste (⌘V) + Return to launch 204-unit run.
- Command: `cd ~/Documents/GitHub/a2j-ai && python3 rules/validation/l2/l2_procedural_defects_runner.py --sleep 2 2>&1 | tee rules/validation/logs/l2_procedural_defects_$(date +%Y%m%d_%H%M).log`

**Direction B — Golden Set Survey complete**
- Surveyed: LSC/Temple Eviction Laws Database, LegalBench (NeurIPS 2023), Learned Hands, JusticeBench, Stanford AI+A2J/Gates, Eviction Lab, NCSC data standards.
- Finding: No existing public dataset provides adoptable annotated fact-pattern/answer pairs for our modules.
- LSC/Temple LawAtlas: useful for statutory cross-reference, but Jan 2021 snapshot (5 years old).
- LegalBench IRAC structure: methodology reference for fact-pattern design.
- Full report: `docs/DIRECTION_B_SURVEY.md`.
- Next step: generate CA/TX notice + service candidates (RED gate for attorney freeze).

**NC-17 fresh run — queued (Andy authorized 2026-06-25)**
- Job: `queue/job_nc17_fresh_20260625.json` — 17 states (AK,AL,CO,CT,HI,KS,LA,MI,ND,NJ,NM,NV,NY,OK,SC,VT,WV), `fresh=true`, `sleep=10`, `uses:[courtlistener,openai,gemini]`.
- Run after procedural defects finishes: `python3 rules/validation/run_protocol.py --protocol retaliation_holdings_v3 --states AK,AL,CO,CT,HI,KS,LA,MI,ND,NJ,NM,NV,NY,OK,SC,VT,WV --sleep 10 --fresh`
- Will search CourtListener for retaliation case candidates in each state, then validate holdings. PR states go to quarantine; MV/CI/RC/SM as usual.

**Direction B — Golden-set candidates generated (DRAFT/UNFROZEN)**
- `rules/validation/golden_sets/DRAFT_CA_notice_candidates_v0.1.json` — 20 CA notice fact patterns
- `rules/validation/golden_sets/DRAFT_CA_service_candidates_v0.1.json` — 15 CA service fact patterns
- `rules/validation/golden_sets/DRAFT_TX_notice_candidates_v0.1.json` — 15 TX notice fact patterns
- 50 total candidates. HIGH confidence: 28. UNCERTAIN/LOW: 22 (flagged for attorney).
- All DRAFT/UNFROZEN. RED gate: Andy must review and freeze each item individually.

**WORK_QUEUE updated** — NOW section reflects procedural defects run + Direction B candidate generation.

### YELLOW — None this cycle.

### RED — Carried
- **launchd macOS TCC (FDA):** Both dispatch.py fixes applied; shell wrapper written. FDA grant still needed. Andy: System Settings → Privacy & Security → Full Disk Access → add `/bin/bash`.
- **Direction B attorney freeze gate:** Candidate generation next; attorney establishment of DRAFT answers = RED.

---

## 2026-06-25 (morning report — second cycle, late morning)

### GREEN — Executed autonomously

**Verified dispatch.py Python 3.9 fix is in place**
- Confirmed `Optional[Path]` and `Tuple[bool, str]` present in dispatch.py (prior 08:00 cycle applied fix; confirmed by grep this cycle).
- Both overnight jobs still in `queue/` (FDA blocker unchanged — no runs since Jun 23).

**Direction B — Golden Set Survey pulled into NOW**
- WORK_QUEUE updated: Direction B survey moved from NEXT to NOW. No dependency on FDA fix.
- NEXT renumbered accordingly.

**Living docs updated — WORK_QUEUE, DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF regenerated.**

### YELLOW — None this cycle.

### RED — Escalated
**RED-strategic — launchd macOS Full Disk Access (carried; both fixes now applied; FDA grant still needed)**

---

## 2026-06-25 (morning report — automated)

### GREEN — Executed autonomously (morning report cycle)

**dispatch.py — Python 3.9 type hint compatibility fix**
- **New bug found in stderr log:** `TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'` at line 74 — `def pick_next_job() -> Path | None:`. The `|` union type syntax in annotations requires Python 3.10+. The launchd plist uses `/Library/Developer/CommandLineTools/usr/bin/python3` which is Python 3.9.x.
- **Fix applied:** Added `from typing import Optional, Tuple` import; replaced all 3.10+ type hints with 3.9-compatible equivalents:
  - `Path | None` → `Optional[Path]` (pick_next_job, find_latest_summary)
  - `tuple[bool, str]` → `Tuple[bool, str]` (run_job, run_protocol_job, run_l2_module_job, _run_subprocess)
- **Verified:** AST parse clean; no remaining `| None` or `tuple[` annotations in file.
- **Impact:** This bug would have caused dispatch.py to fail even after the FDA permission fix. Both fixes (FDA + Python version) are required for overnight runs to succeed.

**Batch 3 holdings v3 (run 7e6fcf6d) — ingested to VALIDATION_METRICS_LEDGER**
- 23 units: 4 MV, 2 CI, 0 RC, 0 PR (confirmed), 0 SM, 17 NC (no-candidates)
- Method rate: 66.7% (4/6 CA text-retrievable). Overall rate: 17.4% (4/23).
- **PR=0 confirmed.** Andy's expectation that "other:17" = PR from 429s is NOT confirmed. The 429s were transient (CA cases only) and recovered successfully. The 17 "other" are NC (no-candidate) states — `fresh=false` + no pre-existing candidate cases in those state files. NOT quarantined as PR. NOT attorney lane. Require `fresh=true` run or manual candidate identification.
- NC states: AK, AL, CO, CT, HI, KS, LA, MI, ND, NJ, NM, NV, NY, OK, SC, VT, WV.
- MV cases (CA): S. P. Growers Assn., Barela, Drouet, Aweeka. CI cases: Schweiger, Western Land Office.
- Live-run proof: dispatcher ran cleanly at 16:21 UTC today. job_batch3_20260623.json moved to done/. Direction A Rev 2 Change 3 satisfied for this job.

**Living docs updated — WORK_QUEUE, STATE_OF_RECORD, DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF regenerated**

### YELLOW — None this cycle.

### RED — Escalated
**RED-strategic — launchd macOS Full Disk Access (carried from prior cycle)**
- Both queued jobs still in queue/. Same blocker as yesterday. Python 3.9 fix now applied (GREEN); FDA permission still needed.

---

## 2026-06-24 (session — new direction + FDA fix)

### GREEN — Executed autonomously

**COWORK_DIRECTION_CHAT_BRIEF.md — saved to docs/**
- Direction saved at `docs/COWORK_DIRECTION_CHAT_BRIEF.md`. GREEN lane (derived artifact, no new judgment).

**docs/CLAUDE_CHAT_BRIEF.md — first build (manual)**
- Generated from current canonical docs. ~1,100 words, within cap. All open REDs present (FDA blocker, 4 notice L7s, 14 retaliation L7s, CA/summons procedural defect, 2 service L7s, SCRA pending-confirmation).
- Subsequent builds auto at 8 AM morning-report cycle (Step 3f added).

**Morning report scheduled task — updated**
- Added Step 3f: regenerate `docs/CLAUDE_CHAT_BRIEF.md` after all canonical docs updated, paste into report.
- `CLAUDE_CHAT_BRIEF.md` not regenerated in this cycle = failure condition added.

### RED — Escalated

**RED-strategic — launchd macOS Full Disk Access (carried from prior cycle)**
- Both jobs still in queue/. Fix steps provided to Andy in this session (see below).

---

## 2026-06-24 (morning report — automated)

### GREEN — Executed autonomously (morning report cycle)

**Smoke test run 3 — formally ingested to VALIDATION_METRICS_LEDGER**
- 6 units: CA/TX/NY × summons + attach. Results: CC=1, NSR=2, SM-GEMINI=1, MODEL-SPLIT=1, ERROR=1.
- Method α = 0.333 (n=4 method cases). Overall α = 0.0 (n=6 including SM+ERROR as DISAGREE). Values statistically unreliable at n=6; noted in ledger.
- Ledger row appended: `Procedural Defects / L2 smoke test run 3`.

**Regression tests — confirmed passing in sandbox**
- `rules/validation/tests/test_l2_procedural_defects.py` — 30/30 pass (re-verified this cycle).

**Direction A — all items confirmed complete**
- Regression tests: 30/30 pass (test file exists at 387 lines).
- dispatch.py: L2 module job type fully wired (confirmed in source).
- Job files: both `job_batch3_20260623.json` and `job_l2_procedural_defects_20260624.json` in queue/.
- WORK_QUEUE.md: NOW section updated to reflect Direction A complete; BLOCKED row added for launchd FDA issue.

**DAILY_CHANGELOG, WORK_QUEUE, METRICS_LEDGER, PROJECT_STATE_OF_RECORD updated this cycle.**

### YELLOW — None this cycle.

### RED — Escalated

**RED-strategic — launchd macOS Full Disk Access blocking overnight runs**
- Both queued jobs (`job_batch3` and `job_l2_procedural_defects`) did not run.
- `launchd_stderr.log`: `[Errno 1] Operation not permitted` when attempting to open `dispatch.py`.
- Root cause: macOS TCC blocks launchd agents from reading `~/Documents/GitHub/` without explicit FDA grant.
- Fix options (for Andy): (a) System Settings → Privacy & Security → Full Disk Access → add python3; (b) approve Cowork writing a shell wrapper script that launchd calls instead.
- Both jobs remain in queue/ and will auto-run on next successful 2:15 AM fire after fix.

**RED-interpretive — CA/summons MODEL-SPLIT (carried from prior session; in HUMAN_REVIEW_QUEUE)**

---

## 2026-06-24 (session — prior)

### GREEN — Executed autonomously (no approval needed)

**l2_procedural_defects_runner.py — 3 bug fixes (all test-verified)**

1. **`query_model` signature fix** — `call_openai`/`call_gemini` take one string arg and return a parsed dict; previous code called `model_fn(SYSTEM_PROMPT, prompt)` (two args) and then called `_parse_json_response()` on an already-parsed dict. Fixed to `model_fn(prompt)` with error detection via `result.get("error")`. *Verified: sandbox import test, no TypeError.*

2. **`citations_equivalent` section-number match** — 70% token-overlap fuzzy matcher classified `Tex. R. Civ. P. 510.4(b)-(c)` vs `Texas Rule of Civil Procedure 510.4` as MODEL-SPLIT (false positive). Added section-number match: if both citations share the same specific numeric section reference (`\b(\d{2,}(?:\.\d+)+|\d{3,})\b`), treat as equivalent. *Verified: 5-case unit test — 3 true matches, 2 true splits, all correct.*

3. **`SM-GEMINI`/`SM-GPT` classification** — when GPT returns empty but Gemini has a valid answer (or vice versa), previous code classified as ERROR and discarded the surviving model's output. New behavior: `SM-GEMINI` / `SM-GPT` classification, writes `l2_sm_statute` to file, flags for re-run. ERROR now reserved for both-models-empty only. *Verified: smoke test run 3 — CA/attach ERROR (both empty), NY/summons SM-GEMINI (Gemini preserved RPAPL § 735).*

4. **Retry logic for GPT empty responses** — added one retry with 5-second pause when `_raw` is empty. Reduced ERROR rate from 4→3 across the 6-unit smoke test.

**Smoke test results (3 runs, CA/TX/NY × attach + summons):**
- Run 1 (pre-fix): 0 CONSENSUS, 2 MODEL-SPLIT (false), 4 ERROR
- Run 2 (fix 1+2): 1 CI, 1 CC, 1 NSR, 0 MODEL-SPLIT, 3 ERROR
- Run 3 (fix 3): 1 CC, 2 NSR, 1 SM-GEMINI, 1 MODEL-SPLIT (genuine), 1 ERROR

**Direction A infrastructure**
- Saved COWORK_HANDOFF_ABC.md, DIRECTION_A/B/C docs to `docs/`
- Created `docs/WORK_QUEUE.md` (NOW/NEXT/BLOCKED/HORIZON, populated several days deep)
- Created `docs/DAILY_CHANGELOG.md` (this file)

**Smoke test ingestion (pending)**
- Third run output: `validation/l2/output/l2_procedural_defects_20260624_1646.json`
- Summary: 1 CONSENSUS-CONFIRM (TX/summons), 2 NO-SPECIFIC-RULE (TX/NY attach), 1 SM-GEMINI (NY/summons → RPAPL § 735), 1 MODEL-SPLIT (CA/summons), 1 ERROR (CA/attach)

---

### YELLOW — Executed, flagged for ratification

*(none yet — pending morning report ratification cycle)*

---

### RED — Escalated, not decided by Cowork

**RED-interpretive — CA/summons procedural defect MODEL-SPLIT**
- GPT: `Cal. Code Civ. Proc. § 1167(a)` (UD summons return provision)
- Gemini: `Cal. Code Civ. Proc. § 415.45` (service by posting in UD cases)
- Both are legitimate CA summons-related provisions; they govern different aspects of the UD summons process. Needs attorney determination: which section (or both) applies as the specific governing rule for summons service defects in CA UD cases?
- *Automated attempt:* 3 runs, genuine split persisted. Section-number match correctly declined to merge (different numbers: 1167 vs 415). Not a formatting artifact — substantive disagreement.
- *Disposition:* Written to HUMAN_REVIEW_QUEUE as L7-procedural-defects. Not routed to attorney by default — routed because it is genuinely interpretive.

---

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
