# CJaC Claude Chat Brief

**Generated:** 2026-06-24 (manual first build — subsequent builds auto at 8 AM morning-report cycle)
**Rolling handoff for Claude Chat — orientation only, canonical docs are authoritative.**
**OS state:** Direction A live · B survey in progress · C not started
**Most important right now:** Overnight validation runs BLOCKED — macOS Full Disk Access must be granted to python3 before tonight's 2:15 AM fire.

---

## 1. WHERE WE ARE

All 51 state v2 eviction rules files are complete and at AUTOMATED-CHECKS-PASSED (51/51). The validation pipeline has run through five layers: L1 (statutory retrieval — 51/51), L3 (internal consistency — 51/51), L5 (cross-jurisdiction anomaly — 51/51 resolved), and L2 multi-model consensus on three modules: notice/pay_or_quit (complete, 41 consensus-confirm, 5 AI-resolved attorney-confirmed, 4 open L7s), service methods (complete, 48 AI-resolved, 2 L7s), and retaliation elements (complete, 36 auto-resolved, 14 open L7s). The current frontier is procedural defects — a smoke test on CA/TX/NY is complete (30/30 regression tests pass) and a full 51-state × 4-defect overnight run is queued. Retaliation holdings v3 (generate-from-source, Batches 1+2 ingested) has Batch 3 (18 states) queued for tonight. Both overnight jobs are blocked on macOS FDA. Direction B (golden sets) is the next major build — attorney gate is required before any golden set is frozen.

---

## 2. DECISIONS WAITING ON ANDY

### RED-strategic (process/infrastructure — Andy action needed)

**macOS launchd Full Disk Access — BLOCKING both overnight jobs**
Both queued jobs (`job_batch3_20260623.json` and `job_l2_procedural_defects_20260624.json`) failed at the 2026-06-25 2:15 AM fire with `[Errno 1] Operation not permitted`. Root cause: macOS TCC blocks launchd agents from reading `~/Documents/GitHub/` without explicit FDA grant.

Fix (2 minutes): System Settings → Privacy & Security → Full Disk Access → unlock → click `+` → navigate to python3 binary (run `which python3` in Terminal first to find exact path) → add it → reload launchd (`launchctl unload ~/Library/LaunchAgents/com.cjac.validation.plist && launchctl load ~/Library/LaunchAgents/com.cjac.validation.plist`). Both jobs remain in `rules/validation/queue/` and will auto-run at next 2:15 AM fire.

**Direction B golden set freeze**
Survey of external ground-truth sources (LSC/Temple, NCSC, academic benchmarks) needs to run first (NEXT queue item #1). After survey, Cowork will generate ~15–25 DRAFT candidate fact-patterns for CA/TX. Andy must then establish authoritative answers → golden sets freeze. Only Andy (as named attorney) can set ground truth.

### RED-interpretive (legal judgment — attorney reads primary source)

**Notice module (4 open L7s)** — all in `docs/HUMAN_REVIEW_QUEUE.md`:
- MO [MO-L7-01]: Is §535.020 demand a notice requirement (notice_required=true) or a precondition (false)?
- ND [ND-L7-02]: Is §47-32-02's 3-day period a formal notice-to-quit or a ripening period?
- MD [MD-L7-03]: Does §8-401 require pre-filing notice? (LSC + Gemini say no; GPT says 10d — likely GPT artifact)
- GA [GA-L7-05]: Does §44-7-50 require a waiting period after demand, or can landlord file immediately? (LSC says no minimum; GPT: 3d; Gemini: no period)

**Retaliation elements (14 open L7s)** — all in HUMAN_REVIEW_QUEUE: AK, AL, CT, HI, KS (two statutes disputed), MI, ND, NJ, NM, NV, NY, SC, VT, WV. Dominant pattern: same statute, models split on whether a subsection creates a time-specific rebuttable presumption period. OK also has a pending L7 on period length. For each: read the cited subsection from state legislature site; confirm whether a statutory presumption period exists and if so, how many days.

**Procedural defects — CA/summons MODEL-SPLIT (1 item)**
CCP §1167(a) (GPT) vs §415.45 (Gemini) — genuine substantive split on which section governs summons service defects in CA UD cases. In HUMAN_REVIEW_QUEUE; first entry from the procedural defects module.

**Service module (2 L7s)** — DC and NM: persistent API failure (zero model data) on service method statutes. These are infrastructure-failure L7s, not interpretive splits. Once CourtListener access improves, a targeted retry can run; until then, attorney verification is the only path.

**SCRA pending confirmation [SCRA-PC-01]**: Gemini found FY23 NDAA amended §3951(a)(2) from CPI threshold to BAH-based formula (130% of E-5 BAH for highest-cost area = ~$4,954/month current). Updated in all 51 files. Andy needs to confirm the amendment and threshold dollar amount.

---

## 3. WHAT EXECUTED SINCE LAST BRIEF

- **l2_procedural_defects_runner.py — 3 bugs fixed** (query_model signature; citations_equivalent section-number match; SM-GEMINI/SM-GPT vs ERROR classification). All fixes test-verified.
- **Regression tests created** — `rules/validation/tests/test_l2_procedural_defects.py` — 30/30 pass. Run before any queue changes.
- **dispatch.py extended** — L2 module job type added; `job_l2_procedural_defects_20260624.json` queued (204 units, est. $3).
- **Batch 3 holdings job queued** — `job_batch3_20260623.json` (18 states, retaliation holdings v3).
- **Direction A infrastructure built** — WORK_QUEUE.md, DAILY_CHANGELOG.md, morning report updated to Direction A shape (GREEN/YELLOW/RED + Krippendorff's α).
- **CLAUDE.md updated** to June 24 with full OS state, pipeline architecture, bucket taxonomy, API notes.
- **Smoke test run 3 ingested** to VALIDATION_METRICS_LEDGER — 1CC/2NSR/1SM-GEMINI/1MODEL-SPLIT/1ERROR (n=6, α unreliable at this n).

YELLOW awaiting ratification: none this cycle.

---

## 4. METRICS MOVEMENT

**Procedural defects — L2 smoke test run 3 (n=6; CA/TX/NY × attach + summons):**
- Method α = 0.333 (n=4 method-eligible cases: CC + NSR + MODEL-SPLIT; excludes SM and ERROR)
- Overall α = 0.0 (n=6 including SM-GEMINI as DISAGREE, ERROR as DISAGREE)
- **Statistically unreliable at n=6** — these are process-validation numbers, not reliability claims. Full 51-state run (n=204) will yield meaningful α.

**Retaliation holdings v3 (most recent full run):** Batch 2 (all 51 states) ingested. Two-rate reporting: see VALIDATION_METRICS_LEDGER for MV/CI/RC/PR/SM breakdown. Batch 3 (18 states) tonight.

**Notice/pay_or_quit:** Complete. ~80% consensus-confirm (41/51). 4/4 AI-resolved items attorney-confirmed correct. See ledger for full breakdown.

No golden-set score — L4 not implemented; blocked on Direction B.

---

## 5. QUEUE SNAPSHOT

**NOW:** Direction A complete. Overnight jobs queued (BLOCKED on FDA fix).

**NEXT (5 items):**
1. Direction B golden set survey — LSC/Temple, NCSC, academic benchmarks (no blocker)
2. Full 51-state procedural defects run — auto-fires when FDA fixed
3. Ingest procedural defects results (morning after run)
4. Batch 3 holdings run — auto-fires when FDA fixed
5. Direction B — generate CA/TX golden set candidates (after survey)

**BLOCKED:** launchd FDA (both overnight jobs), Direction B freeze (attorney gate), Direction C (hard gate on B).

---

## 6. POINTERS

For depth on any of the above, open/upload these canonical docs:
- `docs/PROJECT_STATE_OF_RECORD.md` — full validation status, all layers, all 51 states
- `docs/VALIDATION_METRICS_LEDGER.md` — run-by-run metrics, error-confirm outcomes, α values
- `docs/HUMAN_REVIEW_QUEUE.md` — all open RED-interpretive items with full context for each
- `docs/WORK_QUEUE.md` — full NOW/NEXT/BLOCKED/HORIZON detail
- `docs/DAILY_CHANGELOG.md` — complete GREEN action log

---

*Copyright 2026 Andrew M Cohen. Apache 2.0. This brief is regenerated each morning-report cycle (8 AM) — always reflects the most recent completed cycle. Canonical docs are authoritative if any conflict.*
