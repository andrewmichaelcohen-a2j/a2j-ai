# CJaC Work Queue

*Maintained by Cowork. Updated each morning report cycle. Cowork pulls from NEXT automatically when NOW completes — no prompt to Andy needed unless NEXT is empty or all remaining items are BLOCKED.*

**Last updated:** 2026-07-16 (morning report, fired on time at 8:00 AM — no-run cycle with a NEW anomaly: **the launchd dispatcher did not fire overnight** [no 07-16 entry in launchd_stdout.log; first dispatcher-side miss since the 06-25 FDA fix — all prior anomalies were report-side]. No substantive loss: queue was intentionally empty [would have been the seventh consecutive idle night — Northgate retry #3 still HELD on the Gemini-DNS RED]. Dispatcher-miss checks FOLDED into that standing RED [machine power/sleep overnight; `launchctl list | grep com.cjac`; pmset]. No new output, no metric movement; cumulative MV=26/CI=4/RC=6. Report-side cadence: clean fire — settings-check note retained [07-15 was ~30 min late]. **Both top REDs still waiting on Andy: (1) Gemini-DNS + overnight machine environment diagnosis [now also covers the dispatcher miss; unblocks overnight runs + retry #3], (2) v0.3 held-out freeze [unblocks Broaden Proof 1 Steps 5–7].** Autonomous NEXT depth remains shallow — refill proposals 11–14 stand; items 11 [disposition_note mislabel fix, GREEN] and 13 [Direction D monitoring, YELLOW] are executable without either RED.)

**Prior update:** 2026-07-15 (morning report, fired ~8:30 AM — ~30 min late: no-run cycle — sixth consecutive intentionally-empty night [dispatcher fired 07-15 ~2:24 AM, correctly idled]. Northgate retry #3 still HELD on the Gemini-DNS RED. No new output, no metric movement; cumulative MV=26/CI=4/RC=6. Cadence: the two-clean-fire streak [07-13, 07-14] is broken by today's ~30-min-late fire — settings-check note RETAINED [was one clean fire from closing]. **Both top REDs still waiting on Andy: (1) Gemini-endpoint DNS diagnosis [unblocks overnight runs + retry #3], (2) v0.3 held-out freeze [unblocks Broaden Proof 1 Steps 5–7].** Autonomous NEXT depth remains shallow — refill proposals 11–14 stand; items 11 [disposition_note mislabel fix, GREEN] and 13 [Direction D monitoring, YELLOW] are executable without either RED.)

**Prior update:** 2026-07-14 (8 AM report, fired on time at 8:01: no-run cycle — fifth consecutive intentionally-empty night [dispatcher fired 07-14 2:15 AM, correctly idled]. Northgate retry #3 still HELD on the Gemini-DNS RED. No new output, no metric movement; cumulative MV=26/CI=4/RC=6. Cadence: second consecutive on-schedule fire [07-13, 07-14] after the three-anomaly stretch — settings-check note retained one more cycle; a third clean fire would justify closing it. **Both top REDs still waiting on Andy: (1) Gemini-endpoint DNS diagnosis [unblocks overnight runs + retry #3], (2) v0.3 held-out freeze [unblocks Broaden Proof 1 Steps 5–7].** Autonomous NEXT depth remains shallow — refill proposals 11–14 stand; items 11 [disposition_note mislabel fix, GREEN] and 13 [Direction D monitoring, YELLOW] are executable without either RED.)

**Prior update:** 2026-07-13 (8 AM report, fired on time: no-run cycle — fourth consecutive intentionally-empty night [dispatcher fired 07-13 2:15 AM, correctly idled]. Northgate retry #3 still HELD on the Gemini-DNS RED. No new output, no metric movement; cumulative MV=26/CI=4/RC=6. Cadence: first on-schedule fire since the three-anomaly stretch [07-08 double, 07-10 missed, 07-12 late] — settings-check note stands until a few consecutive clean fires. **Both top REDs still waiting on Andy: (1) Gemini-endpoint DNS diagnosis [unblocks overnight runs + retry #3], (2) v0.3 held-out freeze [unblocks Broaden Proof 1 Steps 5–7].** Autonomous NEXT depth remains shallow — refill proposals 11–14 stand; items 11 [disposition_note mislabel fix, GREEN] and 13 [Direction D monitoring, YELLOW] are executable without either RED.)

**Prior update:** 2026-07-12 (morning report, fired ~11 AM: no-run cycle — third consecutive intentionally-empty night [dispatcher fired 07-12 2:15 AM, correctly idled]. Northgate retry #3 still HELD on the Gemini-DNS RED. No new output, no metric movement; cumulative MV=26/CI=4/RC=6. Cadence note upgraded: 07-08 double-fire + 07-10 missed + 07-12 ~3 h late — three distinct anomaly modes; Andy should check scheduled-task settings before the next live overnight run. **Both top REDs still waiting on Andy: (1) Gemini-endpoint DNS diagnosis [unblocks overnight runs + retry #3], (2) v0.3 held-out freeze [unblocks Broaden Proof 1 Steps 5–7].** Autonomous NEXT depth remains shallow — refill proposals 11–14 stand; items 11 [disposition_note mislabel fix, GREEN] and 13 [Direction D monitoring, YELLOW] are executable without either RED.)

**Prior update:** 2026-07-11 (8 AM report: no-run cycle — overnight queue intentionally empty both nights since 07-09 [dispatcher fired 07-10 + 07-11, correctly idled]. Northgate retry #3 still HELD on the Gemini-DNS RED. No new output, no metric movement; cumulative MV=26/CI=4/RC=6. Process note: no 07-10 report cycle was logged [gap noted in METRICS_LEDGER]. **Both top REDs now waiting on Andy: (1) Gemini-endpoint DNS diagnosis [unblocks overnight runs + retry #3], (2) v0.3 held-out freeze [unblocks Broaden Proof 1 Steps 5–7].** Autonomous NEXT depth remains shallow — refill proposals 11–14 stand; item 11 [disposition_note mislabel fix, GREEN] and item 13 [Direction D monitoring, YELLOW] are executable without either RED.)

**Prior update:** 2026-07-09 (8 AM report: Northgate retry #2 [run 9ae49b97] — all 5 VT units → PR on `generate-api-failure-transient`: CourtListener Checks A+B succeeded for all 5 cases throughout the ~5.7 h run, but EVERY Gemini generate call DNS-failed [Errno 8]. Fifth DNS-affected night — now shown SELECTIVE to the Gemini endpoint; machine-sleep hypothesis weakened [no wall-clock gap this run], local resolver/filter hypothesis primary. **Two YELLOW fixes live-verified ✅:** extended search backoff ladder [CL DNS blip recovered on 60s retry] and FLAG-generate-failed→PR routing fix [first live exercise: 5/5 → PR, zero RC artifacts, nothing to attorney]. Per the job's own instruction, NOT re-queued — overnight queue intentionally empty; Northgate retry #3 held pending Andy's DNS/power decision [RED-strategic, reframed]. VT status unchanged: 1 MV + 1 CI. Cumulative MV=26/CI=4/RC=6. Broaden Proof 1 still BLOCKED on Andy freeze of v0.3 held-out set.)

**Prior update:** 2026-07-08 (8 AM report: Northgate generate retry [run e9222548] failed on infrastructure — DNS to CourtListener exhausted the full 60/120/180/240s backoff ladder on BOTH queries [fourth DNS-affected night since 07-03]; 0 candidates; nothing routed to attorney; no validation rate logged. Backoff ladder extended to 60/120/240/600/1200/1800s [YELLOW, ~66 min ride-out/query]; 30/30 regression tests pass; re-queued as `job_vt_northgate_generate_retry2_20260708` for 2026-07-09 2:15 AM. **RED-strategic for Andy:** 15-hour wall-clock gap [dispatch 2:16 AM → harness processing 5:11 PM PT] suggests the Mac sleeps mid-run despite caffeinate -ims — needs Andy's power/schedule decision. VT status unchanged: 1 MV + 1 CI. Broaden Proof 1 still BLOCKED on Andy freeze of v0.3 held-out set.)

**Prior update:** 2026-07-06 (8 AM report: **VT Gokey → MV ✅** on third attempt [run 57cf7b37] — DNS-retry backoff fix worked; verbatim §4465 burden-shifting quote verified. Run c7bcdcff [2026-07-04 DNS failure] backfilled — 07-04/07-05 cycles had left living docs stale [process miss, fixed]. Harness RC-misroute bug [generate API failure → attorney lane] found + fixed [YELLOW]; 2 DNS-artifact RCs reclassified PR, nothing routed to attorney. Cumulative MV=26. Queue refilled: `job_vt_northgate_generate_retry_20260706` fires tonight. Broaden Proof 1 still BLOCKED on Andy freeze of v0.3 held-out set.)

---

## NOW (executing)

**Self-critique pass + ratification round — COMPLETE ✅**

| Item | Status | Notes |
|------|--------|-------|
| Run self-critique pass (3 disciplines) on all CA-notice rules | ✅ DONE | `docs/CA_NOTICE_SELF_CRITIQUE_REPORT_20260701.md` — 9 REVISED, 3 CONFIRMED, 4 FLAGGED |
| Update `ca_eviction_v2.json` notice section — self-critique revisions | ✅ DONE | 9 source-anchored revisions applied; module status → SELF-CRITIQUE-COMPLETE |
| Correct PLAYBOOK_SPEC §9 elements | ✅ DONE | Subsection citations fixed; SFH two-prong corrected; partial_payment restructured |
| Add `source_anchor` as required element schema field (§3) | ✅ DONE | `flagged: true` as alternative; L1 enforcement note in §10 |
| Add self-critique as standing workflow step (§10) | ✅ DONE | DRAFT → SELF-CRITIQUE → YELLOW → ratification → auto-checks → golden-set → attorney → VALIDATED |
| Add 4 measurement directives §11 (B1-B4) | ✅ DONE | Coverage, confident-wrong, regression, currency — added to PLAYBOOK_SPEC §11 |
| Write three disciplines into CLAUDE.md as standing rules | ✅ DONE | Disciplines A/B/C + B1-B4 in CLAUDE.md; also added to Direction A Parts 5–6 |
| Save self-critique direction to docs/ | ✅ DONE (prior session) | `docs/CJaC_Cowork_Direction_SelfCritique_20260701.md` |
| **RESOLVED-1:** Stancil any-occupant → machine-checkable encoding | ✅ DONE | Andy ratified 2026-07-01. `max_occupant_residency_years` input; Stancil condition on `tenancy_1yr_plus`. Applied to ca_eviction_v2.json + PLAYBOOK_SPEC §9 |
| **RESOLVED-2:** AB 1482 full exemption matrix (all 8 §1946.2(e) categories) | ✅ DONE | Andy ratified. All 8 exemptions encoded in `termination.exemptions`; `ab1482_exemption_matrix` PLAYBOOK_SPEC element added. Applied. |
| **RESOLVED-3:** §1161(3)/(4) bright-line gate | ✅ DONE | Andy ratified. Determinate conduct lists for (4); open-textured path for ambiguous. Applied to ca_eviction_v2.json `unconditional_quit.bright_line_qualifying_conduct` + PLAYBOOK_SPEC §9 interaction. |
| **RESOLVED-4:** `missing_just_cause_reason` defect scope | ✅ DONE | Andy ratified (follow RESOLVED-2). `ab1482_coverage_gate` block with all 8 exemptions; defect fires only for AB1482-covered units. Applied. |
| Update CA_NOTICE_SELF_CRITIQUE_REPORT — FLAGGED → RESOLVED | ✅ DONE | All 4 FLAGGED items updated to RESOLVED in report; Stage 2 gate updated |
| Update WORK_QUEUE + DAILY_CHANGELOG | ✅ DONE | This update |

**Stage 2 gate status post-encoding validation:**
- ✅ Self-critique pass complete
- ✅ Andy reviewed FLAGGED residual + ratified strategy tags (2026-07-01)
- ✅ Gemini credits restored (Andy 2026-07-01); 503 UNAVAILABLE = capacity (temporary)
- ✅ Encoding validation: 11/11=100% non-held-out (SM-GPT PARTIAL-CONSENSUS — not yet consensus-operative)
- ✅ Golden set v0.2 FROZEN (2026-07-01): 17 items; B-04 dropped (near-dup CA-NOT-03); held-out split locked (seed=20260701, leakage-aware pool)
  - File: `rules/validation/scorer/FROZEN/goldenset_CA_notice_v0.2_20260701.xlsx`
  - SHA256: `f65c4240e3ec3c4f7f370d805de906b024e7d3e4f51df92b76197eed1962fa83`
  - Held-out (5): CA-NOT-B-01, B-03, B-13, B-14, B-18 — all NOVEL, none re-testing a correction
  - Dev (12): B-02, B-05, B-06, B-07, B-08, B-09, B-10, B-11, B-12, B-15, B-16, B-17
  - Leakage guard: PASSED. Scorer validation: 0 YELLOW flags.
- ✅ **Gemini DUAL-MODEL-CONSENSUS unblocked** — Gemini 503 capacity issue CLEARED (VT retry run 1153a763, 2026-07-02 02:16 UTC)
- ✅ **v0.2 held-out score BURNED (2026-07-02): 5/5 = 100.0% DUAL-MODEL-CONSENSUS** — agree=4, disagree=1 (CA-NOT-B-18 YELLOW: Gemini UNCERTAIN on owner-occupied duplex inception condition; GPT correct; ground truth confirmed). B2: confident-wrong=0. Output: `ca_notice_score_2026-07-02_held-out.json`.
- ✅ **v0.2 dev set score COMPLETE (2026-07-02): 10/12 = 83.3% DUAL-MODEL-CONSENSUS** — 2 misses triaged to encoding gaps (B-02, B-09). Output: `ca_notice_score_2026-07-02_non-held-out.json`.
- ✅ **Encoding fix REVISED-8 applied (2026-07-02):** `days_hours_for_in_person_payment` added to `notice.notice_types.pay_or_quit.mandatory_content` (source: CCP §1161(2)). Fixes B-02 miss.
- ✅ **Encoding fix REVISED-9 applied (2026-07-02):** Unauthorized subletting moved from `unconditional_quit.bright_line_qualifying_conduct` (§1161(4)) to `cure_or_quit.bright_line_qualifying_conduct` (§1161(3)). Fixes B-09 miss (B2 HIGH).
- ✅ **B3 regression check COMPLETE (2026-07-02): 12/12 = 100.0% DUAL-MODEL-CONSENSUS** — newly_failing=0; B-02 ✅ fixed (AGREE); B-09 ✅ fixed (run 1 GEMINI-EMPTY transient; run 2 AGREE=12 confirmed). No regressions. B2 confident-wrong=0 (was 2 pre-fix).
- **Stage 2 v0.2 CA-notice encoding complete. All known encoding gaps resolved. Ready for next golden set batch or new module.**

---

**Stage 1 — Playbook Architecture Directive: Build registry + confirm skills/tools**

Directive: `docs/CJaC_Playbook_Architecture_Directive_20260701.md`

| Item | Status | Notes |
|------|--------|-------|
| Save directive to docs/ | ✅ DONE | `docs/CJaC_Playbook_Architecture_Directive_20260701.md` |
| Create `docs/ARCHITECTURE.md` | ✅ DONE | One-pipeline playbook architecture documented |
| Create `docs/PLAYBOOK_SPEC.md` | ✅ DONE | Playbook unit schema: element, strategy tags, tiers, known/unknown |
| Create `docs/VALIDATED_RESOURCES_REGISTRY.md` | ✅ DONE | Seed registry with 13 sources; 4 YELLOW flags raised |
| Confirm legal-analysis/issue-spotting skills | ✅ DONE | YELLOW-REG-02/03: no named skills found; `legal:*` available but unintegrated; Lawvable MCP unexplored |
| Research CA Judicial Council UD Benchguide | 🔄 PENDING | YELLOW-REG-01: not yet located; research task carries to NEXT |
| Explore Lawvable MCP for eviction skills | 🔄 PENDING | YELLOW-REG-03: not yet searched; carries to NEXT |

**Direction B — CA-notice pilot v1 COMPLETE ✅**

| Item | Status | Result |
|------|--------|--------|
| `ca_notice_scorer.py` | ✅ BUILT + RUN | Excel-native scorer; live run complete |
| `goldenset_CA_notice_v0.1_20260701.xlsx` | ✅ FROZEN | 16 items; SHA256: `b87791ec…` |
| First held-out score | ✅ BURNED | **3/5 = 60.0%** — held-out set permanently committed |
| Non-held-out score | ✅ SCORED | 7/11 = 63.6% |
| Miss triage | ✅ DONE | All 6 misses = missing rules (not model-wrong). See METRICS_LEDGER. |
| Architecture memo | ✅ INGESTED | `docs/CJaC_Architecture_and_Roadmap_Memo_20260701.md`; Section 5 actioned |

**⚠️ BLOCKED — Gemini API prepayment credits depleted.** Pilot ran GPT-only. Re-run with two-model consensus requires credits restoration at [AI Studio](https://aistudio.google.com/projects).

**VT retry results:**

| Night | Job | States | Result | Notes |
|-------|-----|--------|--------|-------|
| 2026-07-01 at 2:15 AM | `job_vt_retry_fresh_20260630.json` ✅ DONE | VT | ❌ Gemini 429 on both cases | Check A+B passed; Check C failed — API credits depleted. Re-queued. |
| **2026-07-02 at 2:15 AM** | `job_vt_retry_gemini_restored_20260701.json` ✅ DONE | VT | **Houle→CI ✅; Atwood→PR (wrong doc)** | **Gemini 503 CLEARED.** Houle: two-model corroborated (D=INFERRED) → CI, added to HUMAN_REVIEW_QUEUE [VT-HOLD-CI-01]. Atwood: wrong document (not a retaliation case) → PR, GREEN investigation. |

**VT Atwood — GREEN investigation ✅ RESOLVED (2026-07-02 8 AM report):** CourtListener MCP search (`retaliatory eviction "4465"`, court=vt) returned exactly 2 VT opinions: Houle (already CI) and **Gokey v. Bessette, 154 Vt. 560, 580 A.2d 488 (Vt. 1990)** — the foundational VT retaliatory eviction case (the "Gokey standard" Houle applies). Published, cited 17×, CL cluster 1539041. Actions taken: (1) Gokey added to `vt_eviction_v2.json` holdings.candidates (UNVERIFIED); (2) Atwood closed as wrong-doc in `pr_cases`; (3) Houle CI + run results written to VT file (validation_status → RUN-COMPLETE); (4) `job_vt_gokey_20260702.json` queued for tonight's 2:15 AM dispatch.

---

## Broaden Proof 1 — CA-notice held-out n≈30 (Direction: 2026-07-02)

*Direction doc:* `docs/COWORK_DIRECTION_BROADENPROOF1_20260702.md`

| Step | Status | Notes |
|------|--------|-------|
| Step 0: B3 gate | ✅ DONE | 12/12 = 100.0% DUAL-MODEL-CONSENSUS ×3 confirmations. newly_failing=0. |
| Step 1: Freeze CA-notice rules as vProof1 | ✅ DONE | `ca_eviction_v2.json` SHA256=`cc0cfab63ae1591e2b88353c557aeb8027767d99276a3115b5ce9f4115599b93`. **No rule edits until score logged.** |
| Step 2: Save direction doc | ✅ DONE | `docs/COWORK_DIRECTION_BROADENPROOF1_20260702.md` |
| Step 3: Draft 28 held-out candidates | ✅ DONE | `rules/validation/scorer/FROZEN/goldenset_CA_notice_v0.3_DRAFT_20260702.xlsx` — 28 items, Status=DRAFT, all Held-out=TRUE; NOTICE_VALID=15, NOTICE_INVALID=12, UD_DEFECTIVE_PREMATURE=1 |
| **Step 4: Andy reviews + freezes each item** | **🔲 BLOCKED — WAITING ON ANDY** | Andy opens the DRAFT Excel, reviews each fact pattern, confirms or corrects the Drafted outcome, sets Status=FROZEN, adds Reviewed by + Date. This is the attorney ground-truth step — immutable once set. |
| Step 5: Score once, dual-model | 🔲 Blocked on Step 4 | Run scorer after all items are Status=FROZEN. Require DUAL-MODEL-CONSENSUS. One-shot — burned after this run. Command: `python3 rules/validation/scorer/ca_notice_scorer.py --golden rules/validation/scorer/FROZEN/goldenset_CA_notice_v0.3_FROZEN_[date].xlsx --held-out-only` |
| Step 6: Report held-out rate + CI + B1-B4 + α | 🔲 Blocked on Step 5 | Format: "N/28 = X.X%, 95% CI [a, b]" + B1-B4 + Krippendorff α. Report scope note. |
| Step 7: Update collateral if robust | 🔲 Blocked on Step 6 | If result is clean → update CLAUDE_CHAT_BRIEF and project collateral to "demonstrated results"; plan Proof 2. |

---

## Completed Today

**2026-07-16 morning report (fired on time at 8:00 AM)** ✅ DONE
- No-run cycle with a NEW anomaly: **the launchd dispatcher did not fire overnight** (no 07-16 entry in launchd_stdout.log — last write 07-15 ~2:24 AM; no new dispatch log file). First dispatcher-side miss since the 06-25 FDA fix; all prior cadence anomalies were report-side. No substantive loss — queue was intentionally empty (Northgate retry #3 held on the Gemini-DNS RED), so a fire would have idled.
- Dispatcher-miss checks folded into the standing Gemini-DNS/overnight-environment RED: machine power/sleep overnight, `launchctl list | grep com.cjac`, pmset wake schedule — Andy should verify before anything is re-queued.
- State unchanged: cumulative MV=26/CI=4/RC=6; VT module effectively complete. Report-side cadence: clean 8:00 AM fire (settings-check note retained after the 07-15 late fire).
- Anti-default audit: 0 cases routed RED-attorney; no PR/SM in attorney lane; the only failure-condition item is the dispatcher miss (logged, folded into RED).
- All living docs updated (METRICS_LEDGER no-run entry + dispatcher-miss note, PROJECT_STATE_OF_RECORD header, HUMAN_REVIEW_QUEUE header [no new items], WORK_QUEUE, DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF regenerated).

**2026-07-15 morning report (fired ~8:30 AM, ~30 min late)** ✅ DONE
- No-run cycle: dispatcher fired 07-15 ~2:24 AM, queue intentionally empty (sixth consecutive night — Northgate retry #3 held on Gemini-DNS RED per 07-09 job instruction). No new output files anywhere in rules/validation since run 9ae49b97. State unchanged: cumulative MV=26/CI=4/RC=6; VT module effectively complete.
- Cadence: report fired ~8:30 AM — ~30 min late; breaks the two-clean-fire streak (07-13, 07-14). Settings-check note RETAINED (was one clean fire from closing). Dispatcher-side timing normal (2:24 AM within observed 2:15–2:25 window).
- Anti-default audit: 0 cases routed RED-attorney; no PR/SM in attorney lane; no failure conditions beyond the late fire.
- All living docs updated (METRICS_LEDGER no-run entry + cadence note, PROJECT_STATE_OF_RECORD header, HUMAN_REVIEW_QUEUE header [no new items], WORK_QUEUE, DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF regenerated).

**2026-07-14 8 AM morning report (fired on time at 8:01)** ✅ DONE
- No-run cycle: dispatcher fired 07-14 2:15 AM, queue intentionally empty (fifth consecutive night — Northgate retry #3 held on Gemini-DNS RED per 07-09 job instruction). No new output files anywhere in rules/validation since run 9ae49b97. State unchanged: cumulative MV=26/CI=4/RC=6; VT module effectively complete.
- Cadence: second consecutive on-schedule fire (07-13, 07-14). Settings-check note retained one more cycle; a third clean fire would justify closing it.
- Anti-default audit: 0 cases routed RED-attorney; no PR/SM in attorney lane; no failure conditions.
- All living docs updated (METRICS_LEDGER no-run entry + cadence note, PROJECT_STATE_OF_RECORD header, HUMAN_REVIEW_QUEUE header [no new items], WORK_QUEUE, DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF regenerated).

**2026-07-13 8 AM morning report (fired on time)** ✅ DONE
- No-run cycle: dispatcher fired 07-13 2:15 AM, queue intentionally empty (fourth consecutive night — Northgate retry #3 held on Gemini-DNS RED per 07-09 job instruction). No new output files anywhere in rules/validation since run 9ae49b97. State unchanged: cumulative MV=26/CI=4/RC=6; VT module effectively complete.
- Cadence: report fired at 8:00 AM PDT — first on-schedule fire since the three-anomaly stretch. One clean data point; standing settings-check note for Andy retained until a few consecutive clean fires.
- Anti-default audit: 0 cases routed RED-attorney; no PR/SM in attorney lane; no failure conditions.
- All living docs updated (METRICS_LEDGER no-run entry + cadence note, PROJECT_STATE_OF_RECORD header, HUMAN_REVIEW_QUEUE header [no new items], WORK_QUEUE, DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF regenerated).

**2026-07-12 morning report (fired ~11 AM)** ✅ DONE
- No-run cycle: dispatcher fired 07-12 2:15 AM, queue intentionally empty (third consecutive night — Northgate retry #3 held on Gemini-DNS RED per 07-09 job instruction). No new output files anywhere in rules/validation since run 9ae49b97. State unchanged: cumulative MV=26/CI=4/RC=6; VT module effectively complete.
- Cadence note upgraded to three anomaly modes: 07-08 double-fire, 07-10 missed cycle, 07-12 ~3 h late fire. No substantive loss (no output existed), but Andy should check scheduled-task settings before the next live overnight run so ingestion doesn't lag a real result.
- Anti-default audit: 0 cases routed RED-attorney; no PR/SM in attorney lane; no failure conditions beyond the cadence anomaly.
- All living docs updated (METRICS_LEDGER no-run entry + cadence note, PROJECT_STATE_OF_RECORD header, HUMAN_REVIEW_QUEUE header [no new items], WORK_QUEUE, DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF regenerated).

**2026-07-11 8 AM morning report** ✅ DONE
- No-run cycle: dispatcher fired 07-10 and 07-11, queue intentionally empty (Northgate retry #3 held on Gemini-DNS RED per 07-09 job instruction). No new output files anywhere in rules/validation since run 9ae49b97. State unchanged: cumulative MV=26/CI=4/RC=6; VT module effectively complete.
- Process gap logged: no 2026-07-10 report cycle in DAILY_CHANGELOG or METRICS_LEDGER — scheduled task appears not to have fired/logged that day. No substantive loss (no output existed); gap recorded per honesty discipline. Andy: worth checking the Cowork scheduled-task cadence (this follows the 07-08 duplicate-fire observation — cadence looks unstable in both directions).
- Anti-default audit: 0 cases routed RED-attorney; no PR/SM in attorney lane; no failure conditions beyond the missed-cycle gap.
- All living docs updated (METRICS_LEDGER no-run entry, PROJECT_STATE_OF_RECORD header, HUMAN_REVIEW_QUEUE header [no new items], WORK_QUEUE, DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF regenerated).

**2026-07-09 8 AM morning report** ✅ DONE
- Overnight run 9ae49b97 ingested (`job_vt_northgate_generate_retry2_20260708`, dispatched 2026-07-09 2:15 AM window, elapsed 343.4 min): all 5 VT units → PR (`generate-api-failure-transient`). CL Checks A+B succeeded for all 5 cases all night; every Gemini generate call DNS-failed for ~5.7 h. No two-model corroboration occurred; method rate n/a (0÷0), overall 0/5 = 0% (retrieval/generate-gated). Anti-default upheld — nothing routed to attorney.
- Live verification ✅ of both pending YELLOW fixes: extended search backoff ladder (07-08) and FLAG-generate-failed→PR routing (07-06) — the routing fix's first live exercise produced 5/5 PR and zero RC artifacts.
- GREEN diagnosis: DNS failure is selective to the Gemini endpoint (CL resolved fine on the same nights/hours); machine-sleep hypothesis weakened (no wall-clock gap; continuous per-case progress). RED-strategic reframed for Andy: diagnose local DNS/filtering for googleapis.com rather than power settings alone.
- Queue deliberately NOT refilled with Northgate retry #3 per the job's own escalation instruction — held pending Andy's decision (Northgate marginal: trial court; VT module effectively complete at 1 MV + 1 CI). Refill proposal recorded (see NEXT items 11–14).
- All living docs updated (METRICS_LEDGER, PROJECT_STATE_OF_RECORD, HUMAN_REVIEW_QUEUE [no new items], WORK_QUEUE, DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF regenerated).

**2026-07-08 8 AM morning report** ✅ DONE
- Overnight run e9222548 ingested (`job_vt_northgate_generate_retry_20260706`, dispatched 2026-07-07 2:16 AM PT): infrastructure failure — DNS NameResolutionError on ALL 5 attempts of BOTH CL queries; the ~10-min backoff ladder was outlasted. 0 candidates → `VT::__no_cases__` permanent-failure. Northgate's generate never retried; the FLAG-generate-failed→PR routing fix remains live-unexercised. No validation rate logged (N/A per two-rate honesty rules). Anti-default upheld — nothing routed to attorney.
- YELLOW: `_run_search` backoff ladder extended 60/120/180/240s → 60/120/240/600/1200/1800s (~66 min ride-out/query) in `retaliation_holdings_v3_runner.py`. py_compile clean; 30/30 regression tests pass.
- Queue refilled (was empty): `job_vt_northgate_generate_retry2_20260708.json` fires 2026-07-09 2:15 AM.
- RED-strategic flagged: machine-sleep hypothesis (15-hour dispatch→processing wall-clock gap; recurring "2:15 AM DNS window" may be the Mac asleep with network down, not CourtListener). Andy decision: keep machine awake (AC + lid / pmset wake schedule) or move dispatch time.
- GREEN observation (candidate fix, not applied): harness `disposition_note` for search-network-failure still reads "No candidate cases in draft file" — cosmetic mislabel; routing unaffected.
- All living docs updated (METRICS_LEDGER, PROJECT_STATE_OF_RECORD, HUMAN_REVIEW_QUEUE [no new items], WORK_QUEUE, DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF regenerated).

**2026-07-06 8 AM morning report** ✅ DONE
- Two overnight runs ingested: c7bcdcff (2026-07-04, second consecutive DNS failure — backfilled; 07-04/07-05 cycles had left living docs stale, flagged as process miss) and **57cf7b37 (2026-07-06): Gokey v. Bessette → MV** — the target, verified on third attempt after the 2026-07-05 network-retry backoff fix rode out the DNS window.
- Anti-default enforcement against the harness: run 57cf7b37 emitted 2 RC (Houle, Northgate White) that were pure DNS artifacts (Gemini generate call failed; no legal evaluation). Reclassified PR on ingestion; **routing bug fixed** in `protocols/retaliation_holdings_v3.py` (FLAG-generate-failed → PR, YELLOW); 30/30 regression tests pass. Nothing routed to attorney.
- `vt_eviction_v2.json` updated: Gokey → machine_verified_cases; Northgate/Vladyka → pr_cases; Houle CI note annotated; validation_status → GOKEY-MV-COMPLETE. Cumulative MV=26.
- Queue refilled: `job_vt_northgate_generate_retry_20260706.json` fires tonight (2026-07-07 2:15 AM).
- All living docs updated (METRICS_LEDGER incl. c7bcdcff backfill, PROJECT_STATE_OF_RECORD, HUMAN_REVIEW_QUEUE [no new items], WORK_QUEUE, DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF regenerated).

**2026-07-03 8 AM morning report** ✅ DONE
- Overnight VT Gokey run c0a2df2d ingested: infrastructure failure — DNS to www.courtlistener.com unresolvable at 2:17 AM PT on both statute query and broad fallback; 0 candidates; harness recorded permanent-failure. No validation rate logged (retrieval never occurred). Anti-default rule upheld — nothing routed to attorney.
- GREEN diagnosis surfaced config error: `_STATE_RETALIATION_STATUTES["VT"]` was "4467" (termination notice statute) instead of "4465" (retaliation). Fixed (YELLOW — flagged for ratification); runner compiles clean. Also noted: job `target_cluster_id` field is not consumed by dispatch/runner — statute-query fix makes it unnecessary for VT; targeted-cluster mode proposed as future enhancement only.
- `job_vt_gokey_retry_20260703.json` queued for tonight (2026-07-04 2:15 AM). Queue was otherwise empty — refilled.
- All living docs updated (METRICS_LEDGER, PROJECT_STATE_OF_RECORD, WORK_QUEUE, DAILY_CHANGELOG; HUMAN_REVIEW_QUEUE — no new items; CLAUDE_CHAT_BRIEF regenerated).

**2026-07-02 8 AM morning report** ✅ DONE
- Audit: overnight VT run 1153a763 confirmed fully ingested (pre-8AM session); ledger/HRQ/STATE_OF_RECORD/WORK_QUEUE all consistent.
- Atwood GREEN investigation resolved: Gokey v. Bessette (154 Vt. 560, CL cluster 1539041) identified via CourtListener MCP; VT file updated; `job_vt_gokey_20260702` queued (overnight queue was empty — refilled).
- Krippendorff's α computed for v0.2 scorer runs and added to METRICS_LEDGER: held-out α=0.667 (n=5), dev α=0.867 (n=12) — both disagreements are Gemini-UNCERTAIN, not confident splits.
- CLAUDE_CHAT_BRIEF regenerated (was stale from 2026-07-01).

**2026-07-01 morning report** ✅ DONE
- VT retry (run 1c7f0772) ingested: Gemini 429 infrastructure failure. Both VT cases (Atwood, Houle) quarantined for re-queue. Anti-default rule applied — NOT routed to attorney.
- Gemini prepayment credits blocker identified and logged as RED-strategic.
- All living docs updated (METRICS_LEDGER, PROJECT_STATE_OF_RECORD, WORK_QUEUE, HUMAN_REVIEW_QUEUE [no new items], DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF regenerated).

**2026-06-30 morning report** ✅ DONE
- 3 overnight runs ingested: VT Houle retry (perm-fail/pipeline bug), CO/NY/SC PR retry (MV=3,CI=1,PR=8), broad_query 10 states (MV=12,CI=1,RC=1,PR=20,KS perm-fail).
- 8 state v2 files updated with new MV/CI cases (AL×2,CT×3,HI×2,LA×2,ND×1,NM×1 MV+1 CI,WV×1,CO×1). 13 new YELLOW validation flags written.
- WV-RET-HOLD-RC-02 added to HUMAN_REVIEW_QUEUE (Criss v. Salvation Army Residences).
- VT retry re-queued with fresh=true (`job_vt_retry_fresh_20260630.json`).
- All living docs updated (METRICS_LEDGER, PROJECT_STATE_OF_RECORD, HUMAN_REVIEW_QUEUE, WORK_QUEUE, DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF).

**2026-06-29 Cowork session 2** ✅ DONE
- Check E jurisdiction filter + broad CL fallback built in `retaliation_holdings_v3_runner.py`. 10 unit tests pass.
- 3 jobs queued: CO/NY/SC (tonight), 10-state broad-query (tomorrow), VT Houle (night after).
- DAILY_CHANGELOG + WORK_QUEUE updated.

**2026-06-29 morning report** ✅ DONE
- Overnight scan: queue was empty, dispatcher idled. No new output files.
- No new runs to ingest — state unchanged from 2026-06-28 cycle.
- All living docs updated (WORK_QUEUE, DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF regenerated).

**2026-06-28 morning report** ✅ DONE
- Batch 4 (fresh_nc_batch4_20260627) ingested: 3 harness-MV / 2 rejected cross-jurisdiction (Markese=NY County, Robinson=DC Cir) / 1 valid NJ MV (Onderdonk). 8 states perm-fail. 11 PR (8 MI wrong-state docs, 2 VT, 1 NJ/MA).
- nj_eviction_v2.json updated: Onderdonk written to machine_verified_cases; Markese/Robinson written to rejected_cross_jurisdiction.
- YELLOW flag: cross-jurisdiction contamination in harness MV bucket (MI CL query, NJ CL query both returning non-state cases). Pipeline fix needed.
- VALIDATION_METRICS_LEDGER updated: Batch 4 entry added; cross-batch summary updated.
- All living docs updated (WORK_QUEUE, DAILY_CHANGELOG, PROJECT_STATE_OF_RECORD, CLAUDE_CHAT_BRIEF regenerated).

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

**[NEW — Stage 1 carry-overs] Research items from Stage 1 that need Andy's machine or external access:**

| Item | What | YELLOW flag | Status |
|------|------|------------|--------|
| CA Judicial Council UD Benchguide | Locate, verify currency, add to registry as `ca_benchguide_ud` | YELLOW-REG-01 | 🔄 PENDING |
| Lawvable MCP exploration | Search `lawvable_search_skills` for eviction/housing legal skills | YELLOW-REG-03 | ✅ **RESOLVED** — no eviction/housing skills in Lawvable. 189 skills across 20 categories; US jurisdiction = 20 skills (sanctions screening, employment, customs, privacy, CT divorce, trademark). No tenant-landlord, housing, or notice category exists. CJaC is novel territory. |

**[HARD GATE — Consensus-operative before Stage 2 scoring]**

A Stage 2 score CANNOT be cited as consensus-validated unless BOTH models return non-empty responses on ALL scored items. This is now enforced in `ca_notice_scorer.py` v2.1:
- `consensus_status` in run metadata: `DUAL-MODEL-CONSENSUS` | `SM-GPT` | `SM-GEMINI` | `PARTIAL-CONSENSUS (k/n)`
- `consensus_valid: true/false` per item
- Loud ⛔ banner when not consensus-operative
- SM items tagged `⚠SM` in per-item console output
- `single_model_items` count in summary stats

**Required before Stage 2 score is cited:** `consensus_status == "DUAL-MODEL-CONSENSUS"` on the held-out run. This means Gemini credits must be restored first.

**[NEW — Stage 2 (Proof 1): CA notice as deterministic proof] — Gate: Stage 1 complete + Andy ratification**

Stage 2 goal: restructure CA notice into playbook unit per PLAYBOOK_SPEC.md; close all 6 pilot gaps as complete `determinate` elements; produce fresh golden set; score ≥90% held-out.

| # | Item | Notes |
|---|------|-------|
| 1 | Restructure `ca_eviction_v2.json` notice module into playbook unit | Per PLAYBOOK_SPEC.md; element decomposition; strategy tags |
| 2 | Attorney ratification of strategy tags | RED gate — Andy signs off on `determinate`/`open_textured` tags before encoding |
| 3 | Encode 6 missing `determinate` elements with exceptions/interactions | See gap table below |
| 4 | Draft fresh CA-notice golden set (v0.2) | Prior held-out set burned; new items needed; Andy freezes |
| 5 | Re-run scorer (non-held-out only) to verify encoding | No held-out burn; validates encoding correctness |
| 6 | Andy freezes new golden set → run held-out score | Target ≥90% |

**6 missing `determinate` elements (from pilot miss triage):**

| # | Element | Statute | Pilot miss |
|---|---------|---------|------------|
| 1 | 60-day termination notice for tenancy ≥ 1yr | Civ. Code §1946.1(b) | CA-NOT-03 (held-out) |
| 2 | CCP §1161(4) unconditional quit for incurable conduct | CCP §1161(4) vs §1161(3) | CA-NOT-20 |
| 3 | Payee ID required in pay-or-quit | CCP §1161(2) mandatory content | CA-NOT-12 |
| 4 | SFH exemption from AB 1482 just-cause | Civ. Code §1946.2(e)(8) | CA-NOT-08 (confident-wrong) |
| 5 | Relocation assistance for no-fault termination | Civ. Code §1946.2(d); SB 567 | CA-NOT-14 |
| 6 | Partial rent acceptance / waiver doctrine | EDC Associates v. Gutierrez | CA-NOT-16 (held-out) |

Note: Items 6 (partial rent acceptance) is `open_textured` per PLAYBOOK_SPEC.md — requires bounded-reasoning procedure, not a coded rule. The other 5 are `determinate` (simple statutory conditions).

**[NEW — post-pilot] Encode 6 missing CA-notice rules in `ca_eviction_v2.json` (YELLOW — changes decision logic; Andy ratify before next scorer run)**

These 6 rules were identified as gaps by the pilot scorer. Encoding them is the direct fix to improve from 60%. Each needs attorney-confirmed statutory basis before encoding. Proposed order (simplest first):

| # | Missing rule | Statute | Complexity |
|---|-------------|---------|-----------|
| 1 | 60-day termination notice for tenancy ≥ 1yr | Civ. Code 1946.1(b) | Low |
| 2 | CCP 1161(4) unconditional quit for incurable conduct (waste, nuisance) | CCP 1161(4) vs 1161(3) | Low |
| 3 | Payee identification mandatory in pay-or-quit | CCP 1161(2) content requirements | Low |
| 4 | SFH exemption from AB 1482 just-cause | Civ. Code 1946.2(e)(8) | Medium |
| 5 | Relocation assistance for no-fault termination | Civ. Code 1946.2(d); SB 567 | Medium |
| 6 | Partial rent acceptance / waiver doctrine | EDC Associates v. Gutierrez + overstatement line | Medium |

**Excluded golden-set items — routed to downstream modules:**
- **CA-NOT-09** → open-textured queue: utilities-as-"additional-rent" ambiguity (not deterministic enough for current encoding)
- **CA-NOT-15** → retaliation module golden set: §1942.5 retaliatory eviction scenario
- **CA-NOT-17** → service module golden set: §1161 subtenant-service / §415.46 posting requirements
- **CA-NOT-19** → LA local-overlay golden set: LAMC §151.09 — FMR threshold, bedroom statement, LAHD filing (see HORIZON for LA overlay build)

**[NEW — post-pilot] Re-run scorer (non-held-out only) after encoding rules** — Validates encoding is correct before committing to next held-out burn. Command:
```bash
python3 rules/validation/scorer/ca_notice_scorer.py \
  --golden rules/validation/scorer/FROZEN/goldenset_CA_notice_v0.1_20260701.xlsx \
  --non-held-out-only --sleep 3
```

1. **Check E + broad fallback** ✅ DONE (2026-06-29): `retaliation_holdings_v3_runner.py` updated. Proved out in broad_query_10states run — 12 MV from 10 states.

2. **CO/NY/SC PR retry** ✅ DONE (overnight 2026-06-30): 3 MV (CO×1, NY×2), 1 CI (NY), 8 PR remaining. NY MV cases already in ny_eviction_v2.json from Track B — no file conflict.

3. **10-state broad-query run** ✅ DONE (overnight 2026-06-30): MV=12, CI=1, RC=1 (WV Criss), PR=20. 8 state v2 files updated. KS: perm-fail even with broad fallback — CL coverage gap confirmed.

4. **VT holdings — ✅ COMPLETE (2026-07-06): Gokey v. Bessette → MV** (run 57cf7b37; verbatim 9 V.S.A. §4465 burden-shifting quote; 13 citing opinions, no negative treatment). Saga: runs c0a2df2d (07-03) + c7bcdcff (07-04) both failed on the recurring ~2:15 AM DNS window; fixes en route: statute query 4467→4465 (07-03, YELLOW) + `_run_search` network-retry backoff 60/120/180/240s (07-05, YELLOW) — the backoff fix is what got run 57cf7b37 through. VT now: 1 MV (Gokey) + 1 CI (Houle), both VT Supreme Court. Residual: Northgate White generate retry — attempt 1 (run e9222548, 2026-07-07) failed on DNS (both queries exhausted backoff ladder); attempt 2 (run 9ae49b97, 2026-07-09, extended ladder) reached all 5 cases through Checks A+B but every Gemini generate call DNS-failed → all PR. Retry #3 held pending Andy's Gemini-endpoint DNS diagnosis (marginal — trial court).

5. **KS/SC/NV — alternative strategy needed** (YELLOW — confirmed CL gap):
   - **KS:** Broad fallback returned 0 in-state results. Stephens v. Ludy not in CL. Next option: Descrybe MCP lookup or Track A (statute §58-2572 already confirmed).
   - **SC:** Perm-fail in CO/NY/SC retry. Wadell not in CL. SC statute §27-40-910 confirmed Track A.
   - **NV:** Paullin v. Sutton not in CL. NV statute §118A.510 confirmed Track A. Bigelow v. Bullard also not retrievable.
   - **YELLOW:** Use Descrybe MCP to look up KS/NV/SC cases before accepting Track A as ceiling for these states. Andy: call or GREEN autonomous?

6. **CO W.W.G. Corp. YELLOW review** — Runner classified MV but court expressly declined to decide if retaliation doctrine exists in CO. Flag in co_eviction_v2.json. Andy should review before CO is cited as having MV holdings support.

7. **Baer v. Huggins confirm** (CI cheap confirm lane) — HUMAN_REVIEW_QUEUE [NY-HOLD-CI-01]. Attorney pull from Fastcase/Westlaw.

8. **Direction B attorney freeze** (RED gate — Andy's action required) — 50 DRAFT golden-set candidates. Must be frozen by Andy before Direction C can start.

9. **NJ failure_to_attach reformulated retry** (GREEN pipeline) — SM-GEMINI, needs reformulated GPT query.

10. **Terminal cleanup** (optional) — `rm rules/validation/queue/job_nj_attach_probe_20260626.json rules/validation/queue/job_notice_tiebreaker_20260626.json`. Already in done/; dispatcher skips them.

**Proposed NEXT refills (2026-07-08 morning report — autonomous-item depth is shallow; Andy approve/reject):**

11. **[PROPOSED — GREEN]** Fix harness `disposition_note` mislabel: search-network-failure path records "No candidate cases in draft file for this state" instead of a distinct network-failure note. Cosmetic (routing unaffected) but it makes run forensics slower and conflates genuine no-CL states with outages. Small change + regression tests.
12. **[PROPOSED — YELLOW]** Extend network backoff to per-case generate/verify model calls (the 07-05/07-08 fixes cover CL search only). Carried from 2026-07-06 report note. **2026-07-09 update: run 9ae49b97 is the proving case (search survived; generate calls failed) — BUT tonight's Gemini DNS failure persisted ~5.7 h, so a longer per-call ladder alone would NOT have saved the run. Diagnosis (RED item) comes first; this fix is complementary, not sufficient.**
13. **[PROPOSED — YELLOW]** Direction D component 1 (monitoring/measurement): scheduled scorer re-runs on the dev set with regression flagging. Gate was met 2026-07-01 (first pilot score published); low-risk, high-value per HORIZON. Does not touch held-out.
14. **[PROPOSED — GREEN, gated on RED decision]** Re-queue Northgate retry #3 (`job_vt_northgate_generate_retry3`) once Andy resolves the Gemini-endpoint DNS question. Held per job instruction — do not re-queue before the diagnosis. Marginal value (trial court; VT module effectively complete).

---

## BLOCKED (waiting on a named blocker)

| Item | Blocker | What unblocks it |
|------|---------|-----------------|
| ~~**All Gemini-dependent overnight runs**~~ | ~~Gemini API prepayment credits depleted (429 RESOURCE_EXHAUSTED, 2026-07-01)~~ | ✅ **CLOSED 2026-07-02.** Gemini 503 CLEARED — VT retry run 1153a763 confirmed Gemini 2.5-pro working. |
| ~~**VT retry (Atwood + Houle)**~~ | ~~Gemini credits (above)~~ | ✅ **CLOSED 2026-07-02.** Houle→CI; Atwood→PR wrong-doc (GREEN investigation). |
| ~~launchd overnight runner~~ | ✅ **CLOSED 2026-06-25 22:39 PT.** Live proof: `launchctl start` fired dispatcher → `[dispatch] 🚀 Launching: job_20260625_nc17_fresh` → caffeinate subprocess started → log written at `dispatch_retaliation_holdings_v3_20260626_0539.log`. `/usr/bin/python3` (CLT Python) has FDA; plist updated to call it directly. NC-17 fresh run running now. | — closed — |
| Direction B golden set freeze | **RED — Andy (attorney) must establish answers** | Andy signs off on DRAFT candidates → they become FROZEN |
| Direction C self-optimization | **Hard gate — Direction B frozen golden sets must exist** | B complete with ≥1 frozen set, scorer working |
| CA/summons procedural defect | **RED-interpretive — genuine MODEL-SPLIT** | GPT: CCP § 1167(a) vs Gemini: CCP § 415.45. In HUMAN_REVIEW_QUEUE. |
| CourtListener bulk-data / higher rate limit | External — CL/Free Law Project outreach | Andy's decision on timing |

---

## HORIZON (planned, not yet fully specified)

- **Direction B — Scorer build**: ✅ DONE (2026-07-01). First score: 3/5 held-out = 60%. Next: encode 6 missing rules → re-run non-held-out → verify → new held-out version when golden set expands.

- **LA RSO + JCO overlay golden set** — First local-overlay module build. Gate: CA state-law pilot produces first score (✅ UNLOCKED 2026-07-01). Elements per Architecture Memo Section 1: LAMC §151.09(A)(1) FMR-threshold; bedroom-count statement required in notice; LAHD 3-business-day filing. Include re-verification cadence (LA amended RSO Feb 2026; LA County doubled nonpayment threshold Apr 2026). Fed by CA-NOT-19 excluded item.

- **Direction D — Continuous Validation & Improvement Loop** (designed, do NOT build until first pilot score published; ✅ gate met 2026-07-01). Three separable components — build in this order:
  1. **Monitoring/measurement (build soon):** Agents re-run scorer on cadence; track held-out score over time; flag regressions. Low risk, high value.
  2. **Real-world input ingestion (medium risk):** New fact patterns + rule-inaccuracy signals from civil-justice sources. Each input passes same attorney-freeze gate as pilot.
  3. **Automated rule-tuning (highest risk = Direction C):** Agents PROPOSE rule changes; human RATIFIES; held-out stays untouchable. Hardest gate.
  - **ETHICAL CONSTRAINT (non-negotiable):** Improvement signal = evidence of legal INACCURACY, NOT litigation win/loss. Wiring win/loss as training signal would optimize toward "what wins" rather than "what the law requires" — impermissible.
  - Anti-gaming metric: held-out score over time PAIRED WITH coverage + regression count.

- **Benchguide source lane**: CA Judicial Council UD Benchguide as third corroborating source for notice + service module re-validation. Authority hierarchy: benchguide corroborates; statute/case remains primary. Currency check required.

- **Jurisdiction-resolution architecture**: Detection gate before rule application; more-protective/more-specific layer controls; un-encoded jurisdictions flagged (never defaulted to state-only). Start with LA (RSO + JCO), SF, Oakland. See `docs/CJaC_Architecture_and_Roadmap_Memo_20260701.md` Section 1.

- **Krippendorff's α in harness**: update harness.py to report α instead of raw agreement % across all protocols (YELLOW — changes existing behavior, log for ratification)
- **L2 overlays + defenses runners**: extend L2 pattern to warranty of habitability, SCRA, discrimination once procedural defects pipeline is proven at full 51-state scale
- **Full holdings coverage expansion**: after Track B + PR retry close KS/NV/NY/SC and 14-state PR class, remaining NC states (no candidates) need manual case research or CL bulk-data strategy
- **Direction C**: build ONLY after B golden sets exist, scorer working, and first score published. ✅ Prerequisite 1 (golden set) met. ✅ Prerequisite 2 (scorer working) met. Gate: stable score + Andy's strategic sign-off.

---

## Queue rules (Direction A)

- Cowork works NOW → pulls NEXT → keeps going. Only stops if NEXT is empty or all remaining items are BLOCKED.
- Each morning report proposes items to refill NEXT/HORIZON so the queue stays deep.
- When a RED decision is resolved, the unblocked item moves to NEXT automatically.
- Cowork may re-order within NEXT for efficiency (YELLOW), logging why.
- An item may NOT move to attorney review (RED-interpretive) without recorded evidence it survived a genuine automated attempt AND couldn't reach convergence-validated. "The model returned empty" is a pipeline problem, not an attorney item.

---

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
