# CJaC — Claude Chat Rolling Brief

**Generated:** 2026-06-26 late evening · Rolling handoff for Claude Chat — orientation only, canonical docs are authoritative.  
**OS state:** Direction A live · Direction B survey in progress (50 DRAFT candidates, unfrozen) · Direction C not started.  
**Right now:** GA notice YELLOW update applied (notice_required=false, days=null) — needs Andy ratification. OR notice L2 flag closed (tiebreaker confirmed days=10; file already correct). 84 retaliation holdings cases quarantined as PR-class (CourtListener 429 throttling). Harness bug fix queued.

---

## 1. WHERE WE ARE

The 51 v2 eviction rules files (all states + DC) are structurally complete. Overnight dispatcher is live (FDA fixed, launchd firing at 2:15 AM).

**Notice module:** 51-state provenance rerun complete (82% consensus). Tiebreaker run completed for 7 states: GA resolved (YELLOW file update applied — see RED list), AR/MN/WY/TN confirmed-file (no change), OR tiebreaker-resolved (days=10 confirmed; file already correct; L2 flag closed). All 7 states now closed — no L7 escalations from tiebreaker.

**Procedural defects:** Full 204-unit + failure_to_attach re-run complete. α_method=0.256 full run; 0.470 attach-only post-fix. 22 L7s in attorney queue. 4 file updates auto-applied.

**Retaliation holdings v3:** CA has 4 MV, 2 CI (machine-verified, below attorney line). nc17_fresh_v2 run (2026-06-26): 118 units, MV=6, RC=3 (AK/CO/CT), PR=25, **84 transient-failure (CourtListener 429 rate-limiting — 13.3-hour run; PR-class, quarantined for retry)**. Method rate 67%.

**Attorney queue: 48 open items** (43 L7/RC + 5 new from today's runs).

**Direction B:** 50 DRAFT golden-set candidates in golden_sets/. RED gate — Andy must freeze them. Direction C blocked on B.

---

## 2. DECISIONS WAITING ON ANDY (RED LIST)

**RED-interpretive — YELLOW awaiting ratification:**

- **[NOTICE-L2-06] GA — notice_required=false file update (YELLOW):** Both tiebreaker models (GPT + Gemini) confirmed notice_required=false, days=null for Georgia. File updated: `ga_eviction_v2.json` now has `notice_required: false, days: null, statute: O.C.G.A. §§ 44-7-50, 44-7-52`. Prior value (days=3) was unsubstantiated initial-gen only; corroborated by LSC 2021 ("minimum not specified"). Please ratify or override. See HUMAN_REVIEW_QUEUE [NOTICE-L2-06].

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
- **CourtListener rate limiting** — 84 cases throttled over 13.3 hours. Options: (a) longer sleep ≥15s between CL calls; (b) outreach to Free Law Project for higher rate tier. Andy's call on timing.

---

## 3. WHAT EXECUTED SINCE LAST BRIEF (GREEN DIGEST)

Tonight (2026-06-26 late evening):
- **notice_tiebreaker_20260626.py:** Bug fixed (None-subscript), run completed. 7 states: GA TIEBREAKER-RESOLVED-DIFFERS-FROM-FILE → YELLOW file update applied; AR/MN/SD/WY/TN confirmed-file (no change); OR tiebreaker-resolved → days=10 confirmed, file already correct, L2-MODEL-SPLIT flag closed. 0 new L7s.
- **nj_attach_probe_20260626.py:** 3 probes ran. All got Gemini content — NJ ERROR was query framing. GPT timed out all 3. NJ = SM-GEMINI, needs reformulated GPT retry. Not NSR, not attorney.
- **nc17_fresh_v2 ingested:** 118 units, MV=6, RC=3 (AK/CO/CT), PR=25, transient-failure=84. Method rate 67%. 3 RC cases → HUMAN_REVIEW_QUEUE. Harness bug identified (no `bucket` key for transient-failure) → GREEN fix queued.
- **All living docs updated:** HUMAN_REVIEW_QUEUE (7 NOTICE-L2 items resolved/updated, 3 new RC), METRICS_LEDGER (nc17_fresh_v2 section added), WORK_QUEUE (refreshed), DAILY_CHANGELOG (appended).

**YELLOW awaiting ratification:** GA notice file update (days: 3→null, notice_required: false). OR L2-MODEL-SPLIT flag closed (disposition: open→tiebreaker-resolved; file was already correct at days=10).

---

## 4. METRICS MOVEMENT

**nc17_fresh_v2 retaliation holdings (2026-06-26):**
- Method rate: MV÷(MV+CI+RC) = 6÷9 = **67%** | Overall: 6÷118 = **5%**
- α: n/a (n=9 text-retrievable; too small)
- ⚠️ 84 transient-failures are infrastructure (CL 429), not legal signal. Method rate (67%) matches prior CA-only Batch 3 — consistent.

**Notice module tiebreaker (2026-06-26):** 5/7 states confirmed-file; 1 YELLOW update (GA, notice_required=false); 1 flag-closure (OR, days=10 confirmed). 0 new L7s.

**Procedural defects α trend:** Smoke (n=4): 0.333 → Full (n=61): 0.256 → Attach re-run (n=33): 0.470. Rising α reflects prompt+token fixes and cleaner NSR pattern for failure_to_attach.

---

## 5. QUEUE SNAPSHOT

**NOW:** Nothing queued for 2026-06-27 2:15 AM overnight run.

**NEXT (7 items, priority order):**
1. Fix harness.py: write `bucket: "PR"` for transient-failure cases (GREEN, code-only)
2. NJ failure_to_attach reformulated retry (GREEN pipeline)
3. Queue retaliation PR retry for 84 transient-failure cases (GREEN, after harness fix + Andy's call on CL timing)
4. NC states / retaliation holdings Track A — statute-direct (GREEN)
5. Improved CL queries for 11 PR cases (NV/NY/OK) (GREEN)
6. Direction B attorney freeze (RED gate — Andy)
7. Add `--output-suffix` to l2_procedural_defects_runner (YELLOW)

**BLOCKED:** Direction B freeze (Andy); Direction C (B required); CourtListener rate-limit resolution.

---

## 6. POINTERS

For depth, open/upload:
- `docs/HUMAN_REVIEW_QUEUE.md` — all 50 open attorney items with full question detail
- `docs/VALIDATION_METRICS_LEDGER.md` — run-by-run metrics, α computations
- `docs/PROJECT_STATE_OF_RECORD.md` — full module-by-module validation status
- `docs/WORK_QUEUE.md` — full queue
- Stable uploads (in Claude Project): CLAUDE.md, Direction A/B/C docs, COWORK_HANDOFF_ABC.md, reporting direction

---

*Derived from canonical docs as of 2026-06-26 late evening. Canonical docs win on any conflict. Copyright 2026 Andrew M Cohen. Apache 2.0.*
