# CJaC — Claude Chat Rolling Brief

**Generated:** 2026-06-27 morning report · Rolling handoff for Claude Chat — orientation only, canonical docs are authoritative.  
**OS state:** Direction A live · Direction B survey in progress (50 DRAFT candidates, unfrozen) · Direction C not started.  
**Right now:** Two overnight runs completed (2026-06-27). PR retry: pipeline failure — 14 states all perm-fail (fresh=false + no v1 draft candidates). Track B (KS/NV/NY/SC): NY success — 5 MV + 1 CI; KS/NV/SC — 0 CL candidates. ny_eviction_v2.json updated. Pipeline bugs diagnosed; fixes queued.

---

## 1. WHERE WE ARE

The 51 v2 eviction rules files (all states + DC) are structurally complete. Overnight dispatcher is live (launchd firing at 2:15 AM).

**Notice module:** 51-state provenance rerun + tiebreaker complete. GA notice updated (YELLOW — notice_required=false, days=null, O.C.G.A. §§ 44-7-50/52 — awaiting Andy ratification). OR tiebreaker resolved (days=10, file already correct, L2 flag closed). All other tiebreaker states confirmed-file.

**Procedural defects:** Full 204-unit run + failure_to_attach re-run complete. α_method=0.256 full run; 0.470 attach-only post-fix. NJ failure_to_attach resolved (CONSENSUS-IMPROVE → N.J. Ct. R. 6:3-4(c)); 4-run ERROR streak closed. 22 L7s in attorney queue.

**Retaliation holdings v3 — current state:**
- **CA:** 10 MV total (Batches 1–3 + nc17_fresh_v2). 2 CI. Ingested to ca_eviction_v2.json. CA holdings: COMPLETE at Track B level.
- **NY:** 5 MV (Wheeler v. D'Antonio 2025, Pena v. Lockenwitz, 339-347 E. 12th St., MH Residential 1 v. Barrett, Graham Court v. Taylor 115 A.D.3d 50⚠️) + 1 CI (Baer v. Huggins — cheap confirm lane) + 1 PR (Graham Court v. Kyle Taylor 24 N.Y.3d 742 wrong-doc). Method rate: 83.3%. Ingested to ny_eviction_v2.json. NY holdings: TRACK-B-RUN-COMPLETE.
- **KS, NV, SC:** 0 CL candidates in Track B. CL gap — model-suggested Track A candidates not indexed. Next: Descrybe verify OR fix load_draft_cases() to read v2 candidates[].
- **82 cases:** transient-failure from nc17_fresh_v2 — unretried. PR retry runner was broken (fresh=false). Fix needed before requeue.
- **5 RC cases:** AK/CO/CT/NV(Wright v. Brady)/NY(Ellis v. Oceanhill) — in HUMAN_REVIEW_QUEUE, attorney review pending.

**Attorney queue: ~82 open items** (43 L7/RC + 1 CI + 6 PENDING-CONFIRM + others).

**Direction B:** 50 DRAFT golden-set candidates in golden_sets/. RED gate — Andy must freeze them. Direction C blocked on B.

---

## 2. DECISIONS WAITING ON ANDY (RED LIST)

**RED-interpretive — YELLOW awaiting ratification:**

- **[NOTICE-L2-06] GA — notice_required=false file update (YELLOW):** Both tiebreaker models confirmed notice_required=false, days=null (O.C.G.A. §§ 44-7-50, 44-7-52). Prior value (days=3) was unsubstantiated. File updated. Please ratify or override.

- **[YELLOW] Graham Court v. Taylor (115 A.D.3d 50) — MV with caution:** Runner classified MV (both models corroborated), but model summary notes court didn't engage with merits of retaliatory eviction — outcome-only affirmance. Review when examining NY holdings: may not usefully state a controlling rule.

**RED-interpretive — Retaliation holdings RC (5 open — all need attorney):**
- [AK-RET-HOLD-RC-01] DeNardo v. Maassen — valid AK retaliation case? Characterize holding.
- [CO-RET-HOLD-RC-01] Sladek v. dePlomb — valid CO retaliation case?
- [CT-RET-HOLD-RC-01] TOV Realty, LLC v. Suarez — valid CT retaliation case?
- [NV-RET-HOLD-RC-01] Wright v. Brady — valid NV retaliation case?
- [NY-RET-HOLD-RC-02] Ellis v. Oceanhill Brownsville — valid NY retaliation case?

**RED-interpretive — Carried notice L7s (3 open):** MO §535.020 demand characterization [MO-L7-01]; ND §47-32-02 ripening vs notice [ND-L7-02]; MD §8-401 no-notice vs 10d [MD-L7-03].

**RED-interpretive — Retaliation elements L7s (14 open):** [AK-RET-L7-01]–[WV-RET-L7-14] — presumption period disputes. See HUMAN_REVIEW_QUEUE.

**RED-interpretive — Procedural defects L7s (22 open):** [PROC-DEF-L7-01]–[PROC-DEF-L7-22].

**RED-strategic:**
- **Direction B freeze** — 50 DRAFT candidates need attorney sign-off. Hard gate for Direction C.

---

## 3. WHAT EXECUTED SINCE LAST BRIEF (GREEN DIGEST)

**2026-06-27 morning report:**
- **PR retry (overnight):** `job_retaliation_pr_retry_20260626` fired at 2:15 AM. All 14 states perm-fail. Root cause: `fresh=false` + `load_draft_cases()` reads v1 draft file; 82 nc17_fresh_v2 cases were never persisted there. Pipeline bug — not CL rate limiting. 82 cases still unretried.
- **Track B (overnight):** `job_track_b_ks_nv_ny_sc_20260627` fired 2026-06-27. NY: 8 CL candidates found; 5 MV + 1 CI + 1 PR. KS/NV/SC: 0 CL candidates.
- **ny_eviction_v2.json updated:** 5 MV cases (Wheeler v. D'Antonio 2025 — confirms 1-year presumption period; Pena v. Lockenwitz; 339-347 E. 12th St. LLC v. Ling; MH Residential 1 LLC v. Barrett; Graham Court v. Taylor 115 A.D.3d 50) + 1 CI (Baer v. Huggins) + 1 PR (Graham Court v. Kyle Taylor 24 N.Y.3d 742).
- **HUMAN_REVIEW_QUEUE:** NY-HOLD-CI-01 added (Baer v. Huggins, cheap confirm lane).
- **All living docs updated:** METRICS_LEDGER (2 new entries), WORK_QUEUE (queue refreshed, NEXT populated), PROJECT_STATE_OF_RECORD (holdings v3 status updated), DAILY_CHANGELOG.

**YELLOW awaiting ratification:** GA notice file update (days: 3→null, notice_required: false). Graham Court v. Taylor MV flag (see RED list).

---

## 4. METRICS MOVEMENT

**Track B KS/NV/NY/SC (2026-06-27):**
- NY method rate: MV÷(MV+CI+RC) = 5÷6 = **83.3%** — best of any Track B run.
- Overall rate: 5÷11 = **45.5%** (diluted by 3 perm-fail + 1 PR).
- α: n=6 dual-model cases, all AGREE. Undefined (D_e=0). Statistically unreliable at n=6.

**PR retry (2026-06-27):** 0 cases processed. Not a signal — infrastructure failure.

**Cumulative holdings v3:** 15 MV total (10 CA + 5 NY), 3 CI (2 CA + 1 NY), 5 RC (attorney queue), 82 unretried PR-class.

**Procedural defects α trend:** Smoke (n=4): 0.333 → Full (n=61): 0.256 → Attach re-run (n=33): 0.470. Rising α reflects prompt + token fixes.

---

## 5. QUEUE SNAPSHOT

**NOW:** No jobs queued for tonight (2026-06-28 at 2:15 AM). Queue is empty.

**NEXT (6 items, priority order):**
1. PR retry runner v2 (GREEN pipeline) — new runner reading from nc17_fresh_v2 output JSON OR simple fresh=true requeue of 14 states
2. KS/NV/SC — Descrybe MCP verify Track A candidates OR fix load_draft_cases() to read v2 candidates[]
3. [NY-HOLD-CI-01] Baer v. Huggins — attorney cheap confirm (CI lane)
4. Direction B attorney freeze (RED gate — Andy)
5. NJ failure_to_attach reformulated retry — SM-GEMINI, needs reformulated GPT query
6. Terminal cleanup (low priority)

**BLOCKED:** Direction B freeze (Andy); Direction C (B required); CourtListener coverage for KS/NV/SC (Descrybe as alternative path).

---

## 6. POINTERS

For depth, open/upload:
- `docs/HUMAN_REVIEW_QUEUE.md` — all open attorney items with full question detail
- `docs/VALIDATION_METRICS_LEDGER.md` — run-by-run metrics, α computations
- `docs/PROJECT_STATE_OF_RECORD.md` — full module-by-module validation status
- `docs/WORK_QUEUE.md` — full queue
- `rules/eviction/new-york/ny_eviction_v2.json` — Track B results embedded
- Stable uploads (in Claude Project): CLAUDE.md, Direction A/B/C docs, COWORK_HANDOFF_ABC.md, reporting direction

---

*Derived from canonical docs as of 2026-06-27 morning report. Canonical docs win on any conflict. Copyright 2026 Andrew M Cohen. Apache 2.0.*
