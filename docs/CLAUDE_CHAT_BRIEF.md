# CJaC — Claude Chat Rolling Brief

**Generated:** 2026-06-28 morning report · Rolling handoff for Claude Chat — orientation only, canonical docs are authoritative.  
**OS state:** Direction A live · Direction B survey in progress (50 DRAFT candidates, unfrozen) · Direction C not started.  
**Right now:** Batch 4 NC states ingested. Cross-jurisdiction pipeline bug detected — CL statute queries returning non-state cases classified as MV. 2 wrong-jurisdiction "NJ" cases rejected. Cumulative corrected MV = 16 (10 CA + 5 NY + 1 NJ). Queue empty tonight; court-filter fix and VT retry proposed as YELLOW.

---

## 1. WHERE WE ARE

The 51 v2 eviction rules files (all states + DC) are structurally complete. Overnight dispatcher is live (launchd firing at 2:15 AM).

**Notice module:** 51-state provenance rerun + tiebreaker complete. GA notice updated (YELLOW — notice_required=false, days=null, O.C.G.A. §§ 44-7-50/52 — awaiting Andy ratification). All other tiebreaker states confirmed-file.

**Procedural defects:** Full 204-unit run + failure_to_attach re-run complete. α_method=0.256 full run; 0.470 attach-only post-fix. NJ failure_to_attach resolved. 22 L7s in attorney queue.

**Retaliation holdings v3 — current state:**
- **CA:** 10 MV, 2 CI. Ingested to ca_eviction_v2.json. COMPLETE at Track B level.
- **NY:** 5 MV + 1 CI + 1 PR. Ingested to ny_eviction_v2.json. TRACK-B-RUN-COMPLETE.
- **NJ:** 1 MV (Onderdonk v. Presbyterian Homes of NJ, 85 N.J. 171, NJ SC 1981). 2 harness-MV cases rejected as wrong-jurisdiction (Markese=NY County, Robinson=DC Cir). Ingested to nj_eviction_v2.json.
- **KS, NV, SC:** 0 CL candidates in Track B. Model-suggested Track A candidates not indexed.
- **AL, CT, HI, LA, ND, NM, OK, WV:** permanent-failure — no CL candidates under fresh=true statute-targeted search.
- **MI:** 8 PR cases from CL — all cross-state contamination (non-MI cases returned for MI statute query). 0 valid MI candidates.
- **VT:** Houle v. Quenneville (cluster_id=2320677) transient-failure (CL 429). Retry proposed.
- **82 cases:** transient-failure from nc17_fresh_v2 — unretried.
- **5 RC cases:** AK/CO/CT/NV(Wright)/NY(Ellis) — in HUMAN_REVIEW_QUEUE.

**Pipeline bug (YELLOW — new):** CL statute-targeted queries do not filter for court jurisdiction. Runner accepts cases from any jurisdiction that CL returns. Fix: add court-jurisdiction validation after CL search. Proposal in WORK_QUEUE NEXT #1.

**Attorney queue: ~82 open items** (43 L7/RC + 1 CI + 6 PENDING-CONFIRM + others).

**Direction B:** 50 DRAFT golden-set candidates in golden_sets/. RED gate — Andy must freeze. Direction C blocked on B.

---

## 2. DECISIONS WAITING ON ANDY (RED LIST)

**YELLOW awaiting ratification (both new this cycle):**

- **Cross-jurisdiction rejection (YELLOW):** Markese v. Cooper (NY County Courts) and Lena Robinson v. Diamond Housing Corp. (D.C. Circuit) were harness-MV for NJ but are non-NJ courts. Cowork has rejected them from nj_eviction_v2.json. Please ratify the rejection. Proposed fix: court-jurisdiction filter in runner (YELLOW pipeline change).

- **VT Houle retry (YELLOW):** Houle v. Quenneville (cluster_id=2320677) failed with CL 429. Known valid VT candidate. Propose single-state VT fresh=true job. Awaiting Andy's go-ahead to queue.

- **[NOTICE-L2-06] GA — notice_required=false file update (carried YELLOW):** Both tiebreaker models confirmed notice_required=false, days=null (O.C.G.A. §§ 44-7-50, 44-7-52). File updated. Please ratify or override.

- **[YELLOW] Graham Court v. Taylor (115 A.D.3d 50) — MV with caution (carried):** Runner classified MV but model summary notes court didn't engage with merits. Review when examining NY holdings.

**RED-interpretive — Retaliation holdings RC (5 open):**
- [AK-RET-HOLD-RC-01] DeNardo v. Maassen — characterize AK retaliation holding
- [CO-RET-HOLD-RC-01] Sladek v. dePlomb — characterize CO holding
- [CT-RET-HOLD-RC-01] TOV Realty, LLC v. Suarez — characterize CT holding
- [NV-RET-HOLD-RC-01] Wright v. Brady — characterize NV holding
- [NY-RET-HOLD-RC-02] Ellis v. Oceanhill Brownsville — characterize NY holding

**RED-interpretive — Carried notice L7s (3 open):** MO §535.020 [MO-L7-01]; ND §47-32-02 [ND-L7-02]; MD §8-401 [MD-L7-03].

**RED-interpretive — Retaliation elements L7s (14 open):** [AK-RET-L7-01]–[WV-RET-L7-14]. See HUMAN_REVIEW_QUEUE.

**RED-interpretive — Procedural defects L7s (22 open):** [PROC-DEF-L7-01]–[PROC-DEF-L7-22].

**RED-strategic:**
- **Direction B freeze** — 50 DRAFT candidates need attorney sign-off. Hard gate for Direction C.

---

## 3. WHAT EXECUTED SINCE LAST BRIEF (GREEN DIGEST)

**2026-06-28 morning report (this cycle):**
- **Batch 4 ingested:** fresh_nc_batch4_20260627 completed 2026-06-27 19:24 UTC. 22 units, 11 states. 8 perm-fail, 11 PR, 3 harness-MV → 1 valid (Onderdonk NJ), 2 rejected (cross-jurisdiction).
- **nj_eviction_v2.json updated:** Onderdonk added to machine_verified_cases. Markese/Robinson added to rejected_cross_jurisdiction. Scofield to pr_cases.
- **Cross-jurisdiction pipeline bug flagged (YELLOW):** MI CL query and NJ CL query both returning non-state cases. Corrected NJ MV count: 1. Corrected cumulative MV: 16.
- **All living docs updated:** METRICS_LEDGER (Batch 4 entry + cross-batch table update), PROJECT_STATE_OF_RECORD, WORK_QUEUE (NEXT reprioritized, NOW cleared), DAILY_CHANGELOG.

**YELLOW awaiting ratification:** Cross-jurisdiction rejection (Markese/Robinson). VT Houle retry proposal. GA notice file change (carried).

---

## 4. METRICS MOVEMENT

**Batch 4 NC states (2026-06-28, ingested):**
- Harness method rate: MV÷(MV+CI+RC) = 3÷3 = 100% ⚠️ inflated by 2 wrong-jurisdiction cases
- Corrected method rate: 1÷1 = 100% (n=1, statistically meaningless)
- Overall rate: 3÷22 = 14% (bottlenecked by perm-fail + PR)
- α: n/a (D_e=0 — all 3 dual-model cases AGREE; n=3, statistically meaningless)

**Cumulative holdings v3 (corrected):**
- 16 MV total (10 CA + 5 NY + 1 NJ) · 3 CI · 5 RC · 82 unretried PR-class

**Procedural defects α trend:** Smoke (n=4): 0.333 → Full (n=61): 0.256 → Attach re-run (n=33): 0.470. Rising α reflects prompt + token fixes.

---

## 5. QUEUE SNAPSHOT

**NOW:** Queue empty tonight (2026-06-28 at 2:15 AM). Dispatcher will idle.

**NEXT (8 items, priority order):**
1. Cross-jurisdiction runner fix (YELLOW — court filter after CL search)
2. VT Houle retry (YELLOW — single-state job, Andy approval needed)
3. PR retry runner v2 (GREEN — 82 unretried transient-failure cases)
4. KS/NV/SC — Descrybe verify or load_draft_cases() fix
5. Baer v. Huggins confirm (CI lane — attorney)
6. Direction B attorney freeze (RED gate — Andy)
7. NJ failure_to_attach reformulated retry
8. Terminal cleanup (low priority)

**BLOCKED:** Direction B (Andy sign-off); Direction C (B required); CourtListener coverage for KS/NV/SC; VT Houle retry (Andy approval needed).

---

## 6. POINTERS

For depth, open/upload:
- `docs/HUMAN_REVIEW_QUEUE.md` — all open attorney items with full question detail
- `docs/VALIDATION_METRICS_LEDGER.md` — run-by-run metrics, α computations
- `docs/PROJECT_STATE_OF_RECORD.md` — full module-by-module validation status
- `docs/WORK_QUEUE.md` — full queue
- `rules/eviction/new-jersey/nj_eviction_v2.json` — Batch 4 NJ results (including rejected_cross_jurisdiction)
- `rules/eviction/new-york/ny_eviction_v2.json` — Track B NY results
- Stable uploads (in Claude Project): CLAUDE.md, Direction A/B/C docs, COWORK_HANDOFF_ABC.md, reporting direction

---

*Derived from canonical docs as of 2026-06-28 morning report. Canonical docs win on any conflict. Copyright 2026 Andrew M Cohen. Apache 2.0.*
