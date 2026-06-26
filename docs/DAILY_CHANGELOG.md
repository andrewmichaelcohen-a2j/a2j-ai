# CJaC Daily Changelog

*GREEN action log — every autonomous change Cowork makes is recorded here. Andy audits without having watched. Format: date · what changed · test/verification.*

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
