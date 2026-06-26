# CJaC — Claude Chat Rolling Brief

**Generated:** 2026-06-26 (morning report cycle) · Rolling handoff for Claude Chat — orientation only, canonical docs are authoritative.  
**OS state:** Direction A live · Direction B survey in progress (50 DRAFT candidates, unfrozen) · Direction C not started.  
**Right now:** NC-17 fresh run complete (2 RC, 11 PR, 37 perm-fail); attach-retry-9 queued for tonight; NEXT queue is shallow — Andy approval needed on refill items.

---

## 1. WHERE WE ARE

The 50-state eviction rules library (51 files, v2 schema) is structurally complete. Two validation layers are fully run for the first time:

**Procedural defects (L2, 51×4 defects, Jun 25–26):** Full pipeline now live via launchd overnight runner. 204-unit run + failure_to_attach re-run complete. α_method rose from 0.256 → 0.470 after prompt fix + token fix. 22 MODEL-SPLIT cases in attorney queue [PROC-DEF-L7-01]–[PROC-DEF-L7-22]. 4 file updates auto-applied. 9 GPT-timeout states queued for retry tonight.

**Retaliation holdings v3 (Jun 22–26):** Batch 3 complete — CA has 4 MV, 2 CI cases (machine-verified, below attorney line). NC-17 fresh run completed 10:00 UTC today: 2 RC (NV, NY — attorney needed), 11 PR (wrong-doc CL returns, not attorney), 37 perm-fail (no CL candidates). ~15 states found zero retaliation case law via CL search — Andy's decision on next step.

**Attorney queue total: 45 L7/RC items open** (43 prior + 2 new RC from today). No items have been attorney-confirmed yet — Direction B freeze has not begun.

**Direction B:** 50 DRAFT golden-set candidates exist in `rules/validation/golden_sets/`. RED gate — Andy must freeze them to establish ground truth. Direction C (self-optimization) cannot start until B is frozen.

---

## 2. DECISIONS WAITING ON ANDY (RED LIST)

**RED-interpretive — NEW (2026-06-26):**

- **[NV-RET-HOLD-RC-01] Wright v. Brady (NV, 418 P.3d 619, 2018):** CL text retrieved; verify step could not corroborate the generated holding. Q: Is this case a valid NV retaliation defense holding? If so, state the controlling rule. If not, dismiss. Recorded in HUMAN_REVIEW_QUEUE.

- **[NY-RET-HOLD-RC-02] Ellis v. Oceanhill Brownsville Tenant Ass'n (NY, 152 Misc. 2d 1007, 1991):** CL text retrieved; generate step failed to extract a retaliation holding. Q: Valid NY retaliation case? If so, what's the holding? If not, dismiss — and does a better NY retaliation case exist? Recorded in HUMAN_REVIEW_QUEUE.

**RED-interpretive — Carried (attorney queue):**
- Notice module (4 open): MO §535.020 characterization, ND §47-32-02 ripening vs notice, MD §8-401 notice required or not, GA §44-7-50 days=3 vs none
- Retaliation elements (14 open): AK, AL, CT, HI, KS, MI, ND, NJ, NM, NV, NY, SC, VT, WV — presumption period disputes [AK-RET-L7-01]–[WV-RET-L7-14]
- Procedural defects (22 open): [PROC-DEF-L7-01]–[PROC-DEF-L7-22] — statute-vs-court-rule splits, cross-court-type disputes
- CA/summons split: GPT=CCP §1167(a) vs Gemini=CCP §415.45

**RED-strategic:**
- **Direction B freeze** — 50 DRAFT candidates need attorney sign-off to become ground truth. Hard gate for Direction C.
- **~15 NC states, no retaliation candidates** — CL search found nothing even with fresh=true. Options: (a) expand CL query; (b) manual identification; (c) accept as "no appellate case law." Andy's call.
- **CourtListener rate limit** — ongoing CL 429 backoff during overnight runs. External decision on higher quota/bulk-data access.

---

## 3. WHAT EXECUTED SINCE LAST BRIEF (GREEN DIGEST)

- **NC-17 fresh run ingested** (MV=0, CI=0, RC=2, PR=11, perm-fail=37). 2 RC cases → attorney queue. 11 PR cases diagnosed as wrong-doc CL returns (pipeline fix needed, not attorney). launchd first attempt failed at 05:17 (sandbox path, not an issue on Andy's Mac); retry succeeded 10:00 UTC.
- **attach-retry-9 job created and queued** — `job_l2_attach_retry9_20260626.json` for AL/IA/ME/MN/NH/NJ/NV/RI/VA. Fires tonight 2:15 AM. Expects mostly NSR.
- **All canonical docs updated** — METRICS_LEDGER, PROJECT_STATE_OF_RECORD, HUMAN_REVIEW_QUEUE, WORK_QUEUE, DAILY_CHANGELOG.
- *Prior cycle (early morning):* failure_to_attach re-run: NSR 6→28, SM −64%, ERROR −61%, α_method=0.470. CA file updated. L7s [PROC-DEF-L7-21, L7-22] added (CT, FL). Token fix (2000→8000) ratified and confirmed effective.

**YELLOW awaiting ratification:** None this cycle.

---

## 4. METRICS MOVEMENT

**NC-17 fresh run (run 20f722c8, 2026-06-26):**
- Method rate: MV÷(MV+CI+RC) = 0÷2 = 0% | Overall: 0÷50 = 0%
- α_method = n/a (n=2 text-retrievable, all RC; D_e=0, undefined)
- ⚠️ Note: 0% reflects wrong-doc returns + generate failures for 2 cases, not absence of NV/NY retaliation law

**Procedural defects α_method trend:**
- Smoke test (n=4): 0.333 — too small to interpret
- Full 4-defect run (n=61): 0.256 — first real estimate; 70% SM from GPT token stall
- attach re-run (n=33): 0.470 — post-fix; NSR pattern confirmed for this defect

α rising reflects both fix validation (more dual-model coverage) and the cleaner NSR pattern for failure_to_attach — most states have no separate attachment rule.

---

## 5. QUEUE SNAPSHOT

- **NOW:** attach-retry-9 (AL/IA/ME/MN/NH/NJ/NV/RI/VA) — fires tonight 2:15 AM
- **NEXT (depth: 2, one blocked):**
  1. Ingest attach-retry-9 results (GREEN — when done)
  2. Direction B attorney freeze (RED gate — Andy)
- ⚠️ **NEXT is shallow.** Proposed refill (Andy to approve): notice module re-run (provenance; ~$1.10); NV/NY PR-case CL query improvement; attorney queue session (work MO, ND, MD, GA notice L7s).
- **BLOCKED:** Direction B golden-set freeze (Andy); Direction C (hard gate on B); CourtListener higher rate limit (external)

---

## 6. POINTERS

For depth, open/upload:
- `docs/HUMAN_REVIEW_QUEUE.md` — all 45 open attorney items with full question detail
- `docs/VALIDATION_METRICS_LEDGER.md` — run-by-run metrics, α computations, per-defect breakdowns
- `docs/PROJECT_STATE_OF_RECORD.md` — full module-by-module validation status
- `docs/WORK_QUEUE.md` — full queue with proposed refill items

---

*Derived from canonical docs as of 2026-06-26 morning report. If this brief and a canonical doc disagree, the canonical doc wins. Copyright 2026 Andrew M Cohen. Apache 2.0.*
