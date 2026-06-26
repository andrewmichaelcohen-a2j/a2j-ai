# CLAUDE_CHAT_BRIEF — CJaC Rolling Handoff

**Generated:** 2026-06-25 (morning report cycle — late morning) · Rolling handoff for Claude Chat — orientation only, canonical docs are authoritative.
**OS state:** Direction A live · Direction B survey NOW (just pulled in) · Direction C not started.
**Most important right now:** Overnight runs BLOCKED — macOS TCC FDA grant needed from Andy. Both Python fix + dispatch fix are done; FDA is the only remaining blocker.

---

## 1. WHERE WE ARE

All 51 v2 rules files exist (50 states + DC), schema v2. Six validation modules have been L2-run:

**Complete:** Notice/pay-or-quit (L2, 51 states), Service/method-rules (L2, 51 states), Retaliation elements (L2, 51 states — 15 L7-open), State-protective overlays (L2, 51 states — 16 items pending human action), Remaining 4 defenses/elements (L2, 51 states — single-model-preliminary), Retaliation holdings v2 CA proof-of-concept (6 cases, 4/6 MV).

**In queue for next 2:15 AM fire (BLOCKED — see RED below):**
- Batch 3 retaliation holdings v3 — 18 remaining states (AK, AL, CA, CO, CT, HI, KS, LA, MI, ND, NJ, NM, NV, NY, OK, SC, VT, WV)
- Full 51-state × 4-defect L2 procedural defects run (204 units, est. $3)

**Active NOW:** Direction B — golden set survey (no FDA dependency; can proceed immediately).

**Not started:** Direction B golden set freeze/candidates (blocked on survey + attorney gate), Direction C self-optimization (blocked on B).

---

## 2. DECISIONS WAITING ON ANDY

### RED-strategic

**[BLOCKER] macOS TCC Full Disk Access — overnight dispatcher cannot run**
Both queued jobs remain in `rules/validation/queue/`. Launchd fires at 2:15 AM but gets `[Errno 1] Operation not permitted` trying to open `dispatch.py`. Two bugs are now fixed (GREEN): Python 3.9 type hint incompatibility resolved in 08:00 morning cycle. The only remaining blocker is the FDA grant.
- **To unblock:** System Settings → Privacy & Security → Full Disk Access → add `/Library/Developer/CommandLineTools/usr/bin/python3`. OR approve Cowork writing a shell wrapper script (GREEN lane).
- **Once unblocked:** both jobs auto-run at next 2:15 AM fire.

### RED-interpretive (attorney review — all in HUMAN_REVIEW_QUEUE)

**Notice module (4 open L7s):** MO, ND, MD, GA. MD and GA corroborated by LSC in the Gemini direction (no-notice / no-minimum). Each is a read-the-statute task.

**Service module (~19 items):** NV-SVC-01, TN-SVC-02 (genuine model splits — different statutes cited). Plus ~17 citation-divergence items where models agree with each other but differ from the file.

**Retaliation elements (15 open L7s):** AK, AL, CT, HI, KS, MI, ND, NJ, NM, NV, NY, SC, VT, WV, OK. Pattern: same or similar statute, genuine split on whether a time-specific rebuttable presumption clause exists. Task: read the cited subsection directly from state legislature site.

**Procedural defects (1 open L7):** CA/summons — GPT: CCP § 1167(a) vs Gemini: CCP § 415.45. Three automated runs, genuine split persisted. Both are real CA UD summons provisions governing different aspects of the process.

**Pending confirmation (2 items):**
- [SCRA-PC-01] FY23 NDAA BAH formula amendment to 50 U.S.C. § 3951 — verify $4,954.34/month threshold from DoD BAH charts.
- [NM-SVC] Service statute §47-8-52 (AI preliminary) vs file's §47-8-33 — verify from primary source.

---

## 3. WHAT EXECUTED SINCE LAST BRIEF

**2026-06-25 late-morning cycle (this cycle):**
- Verified Python 3.9 fix present in dispatch.py (grep confirmed `Optional[Path]`, `Tuple[bool,str]` in place).
- Confirmed both overnight jobs still in queue/ — no runs since Jun 23.
- Direction B golden set survey pulled into NOW (WORK_QUEUE updated).
- Living docs updated: WORK_QUEUE, DAILY_CHANGELOG, STATE_OF_RECORD, CLAUDE_CHAT_BRIEF.

**2026-06-25 08:00 cycle:**
- dispatch.py Python 3.9 fix applied: `Path|None` → `Optional[Path]`; `tuple[bool,str]` → `Tuple[bool,str]` (7 function signatures). AST parse clean. Second bug blocking overnight runs resolved.
- Living docs updated; CLAUDE_CHAT_BRIEF first regenerated this cycle.

**2026-06-24 prior cycles:**
- Smoke test run 3 ingested to METRICS_LEDGER (6 units, CA/TX/NY × summons + attach).
- 3 bug fixes to l2_procedural_defects_runner.py; 30/30 regression tests pass.
- Direction A infrastructure complete; both overnight jobs placed in queue.
- dispatch.py extended for L2 module job type.

YELLOW: None open.

---

## 4. METRICS MOVEMENT

**No new runs this cycle.** Both jobs blocked on macOS FDA.

**Most recent data — procedural defects smoke test (2026-06-24, n=6):**
- Method α = **0.333** (n=4; ⚠️ statistically unreliable — pipeline test, not a sample)
- Overall α = **0.0** (n=6 including SM-GEMINI + ERROR as DISAGREE; expected — smoke test included edge cases intentionally)
- Buckets: CC=1, NSR=2, SM-GEMINI=1, MODEL-SPLIT=1 (→ L7, CA/summons), ERROR=1

**Prior module metrics unchanged** — see VALIDATION_METRICS_LEDGER for run-by-run detail. Two-rate reporting (method_rate, overall_rate) will apply to holdings once Batch 3 lands.

---

## 5. QUEUE SNAPSHOT

**NOW:** Direction B — golden set survey (no dependency; active immediately)
**NEXT (3 items):**
1. Full procedural defects run (51 × 4 = 204 units) — blocked on FDA; auto-fires after grant
2. Retaliation holdings v3 Batch 3 (18 states) — blocked on FDA; auto-fires after grant
3. Direction B — generate CA/TX golden set candidates (blocked on survey + attorney gate)

**BLOCKED:** Overnight runner on macOS FDA (RED-strategic, Andy); B golden set freeze on attorney sign-off; C on B frozen sets.

**NEXT depth adequate** (3 items). Direction B survey in NOW can proceed without any blocker.

---

## 6. POINTERS

For depth, open:
- `docs/PROJECT_STATE_OF_RECORD.md` — full module-by-module validation status
- `docs/VALIDATION_METRICS_LEDGER.md` — run-by-run metrics with provenance table and repeatability view
- `docs/HUMAN_REVIEW_QUEUE.md` — all RED-interpretive items with full L7 detail and automated-attempt evidence
- `docs/WORK_QUEUE.md` — full NOW/NEXT/BLOCKED/HORIZON

---

*Copyright 2026 Andrew M Cohen. Apache 2.0. Orientation layer — canonical docs are authoritative.*
