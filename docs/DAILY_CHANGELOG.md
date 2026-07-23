# CJaC Daily Changelog

*GREEN action log — every autonomous change Cowork makes is recorded here. Andy audits without having watched. Format: date · what changed · test/verification.*

---

## 2026-07-23 (Direction D Build-Out & Open-Item Closeout — Andy's directive)

*Documentation-level tasks 1-3 executed this session; task 4 (collateral versioning) blocked pending file supply from Andy. Nothing here preempts proposal 16 (next session) or proposal 17/v0.4 drafting (after 16), per the directive's own sequencing note.*

### GREEN — Task 1: Direction D roadmap formalized

Created `docs/DIRECTION_D_ROADMAP.md`, defining components D-2 (disagreement auto-triage), D-3 (statute-and-case watch), D-4 (standing adversarial self-critique), D-5 (CJaC-lift tracking across model generations). All four are labeled ROADMAP-DEFINED, not building. The invariant is stated verbatim in the doc: AI generates candidates and evidence continuously; nothing self-ratifies; every change lands as a proposal for named-attorney ratification; every applied change passes the dev-set regression gate; held-out sets are burned after one use. Build triggers/sequencing as directed: D-2 wires alongside proposal 17's v0.4 drafting, live before the v0.4 scoring event (so the event itself exercises it); D-3 is first-built after v0.4 scoring completes; D-4's cadence proposal is due with its own build plan (not drafted here); D-5's first data point is the v0.4 ablation arm already required by proposal 17.

### GREEN — Task 2: Repository discoverability pass

Created `docs/VALIDATION_README.md` — a plain-English index (audience: law professors and legal-aid staff, not just engineers) linking to `VALIDATION_METRICS_LEDGER.md`, the v0.3 held-out scorer output JSON, `AUTOPSY_v0_3_MISSES_20260719.md`, the signed errata memo (`.docx` marked authoritative, `.md` as reading copy), and the ratified `RULE_PROPOSAL_1946_2a_ATTACHMENT_20260719.md` / `WIRING_DETERMINATION_1946_2e_20260719.md` pair. States the dual-reporting rule (v0.3 = 23/26 as-scored / 25/26 post-errata, always both) and the multi-model-consensus definition (two independent models must agree; tri-model is roadmap) up front. `README.md`'s "Key documents" list updated to point here first, above the existing methodology/status-ladder/disclaimer links.

**First-time-visitor path, as reported to Andy:** `README.md` → `docs/VALIDATION_README.md` → either `VALIDATION_METRICS_LEDGER.md` (numbers) or `AUTOPSY_v0_3_MISSES_20260719.md` → `ERRATA_MEMO_v0_3_20260719.docx` (a specific correction, start to finish, signed instrument one click away). No step requires prior knowledge of repo structure or file-naming conventions.

### GREEN — Task 3: Schweiger cite-check sweep — clean, one informational flag

Searched the full repository (rules files, docs, checkpoints, scorer/L2 output JSON) for every reference to *Schweiger v. Superior Court*. Result: **every single reference in the repository is correctly tied to the retaliatory-eviction defense** (Civil Code §1942.5) — the case Schweiger actually is authority for. None ties Schweiger to `includes_late_fees` / the notice-overstatement defect. The erroneous citation the directive flagged was confined to the retired two-pager draft and the v3 full deck (outreach collateral, not in the repo) — those are outside this sweep's reach since the files aren't in the repository (see Task 4).

Confirmed the *correct* authority is already what the repository actually uses for the late-fees/overstatement defect: the v0.3 golden set (`rules/validation/golden_sets/DRAFT_CA_notice_candidates_v0.1.json`, item CA-N-010) cites **Levitz Furniture Co. v. Wingtip Communications, Inc.** — and the freeze-time citation-correction log (`VALIDATION_METRICS_LEDGER.md`, "Citation corrections made at freeze") already recorded a pincite fix (1411→1035) matching the directive's stated correct citation (86 Cal.App.4th 1035, 1038) exactly.

**One informational flag, not a repo defect:** `docs/CA_UD_BENCHGUIDE_BG31_EXTRACT.md` quotes *Nourafchan v. Miner* (1985) 169 Cal.App.3d 746 at pincite **763**; the directive's citation gives pincite **753**. This is a benchguide-extract quote (a secondary source), not a rule-file citation, and nothing in the repo's actual rules or golden set depends on the pincite — logging for attorney awareness only, no action taken, no file edited. If it matters at the next version cut, it rides alongside the already-queued §1946.2(a) citation-label fix from proposal 16.

**Conclusion:** no rules-file, doc, or repository collateral requires correction. No proposal generated — there was nothing to propose a fix for.

### BLOCKED — Task 4: Collateral versioning

Cannot execute without the three files: `CJaC_Two_Pager_AMC_07_23_26_FINAL.docx`, `CJaC_Pitch_Deck_Speaker_20260723.pptx`, `CJaC_Concise_Deck_20260720.pptx`. None exist in this session's uploads or in the repository — they live only on Andy's machine. **Andy action needed:** supply the three files (chat upload is sufficient); once received they'll be committed to a `collateral/` folder with a DAILY_CHANGELOG version-log entry, per the directive.

## 2026-07-21 (evening — decision log: dispatcher RED closed, proposals 16/17/18 ratified)

*Andy's decision log, five items.*

### GREEN — Root-caused and fixed this session

**Dispatcher RED closed (miss ×6, 07-16→07-21).** Root cause: `~/Documents` is a TCC-protected folder on macOS, and background-agent (launchd/smd) spawns are silently blocked from touching files there even with Full Disk Access granted to the target binary — a restriction that does not apply to interactively-typed Terminal commands, which is why every manual invocation of the identical command succeeded while every automated fire failed with `EX_CONFIG` (78) and zero heartbeat-log output. Confirmed via a control test: a trivial LaunchAgent pointed at `/tmp` succeeded cleanly (`hello from launchd`, exit 0); the same job pointed at `~/Documents/GitHub/a2j-ai` failed identically every time. Sleep/power and agent-unloaded hypotheses retired. **Fix (07-21):** repo relocated `~/Documents/GitHub/a2j-ai` → `~/Developer/a2j-ai` (not a TCC-protected folder); `com.cjac.validation.plist` paths updated (`ProgramArguments`, `WorkingDirectory`, `StandardOutPath`, `StandardErrorPath`); old registration fully torn down (`launchctl bootout` + plist removal) and re-registered via `launchctl bootstrap` (not the legacy `load`, which had also gotten the job stuck in a remove/resubmit flapping loop against macOS's newer Background Task Management layer). Live `launchctl kickstart` test confirmed `last exit code = 0` with a complete heartbeat chain (LOADED → FIRED → COMPLETED-RUN, PREFLIGHT_DNS all three endpoints reachable). Confirmation checkpoints: tonight's ~2:15 AM fire (expect fired-and-idled), tomorrow's first 12:00 PM fire (drives D-1 automatically — next monitor run cadence-eligible ≥ 07-23), tomorrow's morning report. Overnight lane reopens; Northgate retry #3 (carried item 14) re-queued on normal prioritization. B-2 DNS preflight probes stay in place (the nighttime Gemini DNS strand predates the path break and is a separate open question, unresolved either way); B-4's pmset recommendation stays held unless probe data shows a genuine sleep issue.

**Git housekeeping flag corrected (not a real issue).** The "last commit 2026-06-16" note in `PROJECT_STATE_OF_RECORD.md`'s Repo Identity table was the audit reading a stale repo copy left at the old `~/Documents/GitHub/a2j-ai` path — same root cause as above. GitHub Desktop confirms: working tree clean, zero uncommitted changes, full history present through today's commits, synced with origin. Corrected in PSOR (Local path + Last commit fields) and WORK_QUEUE; audit checks now point at `~/Developer/a2j-ai`.

**Proposal 18 — ratified source text logged.** Andy supplied the attorney-sourced verbatim statutory text for the Civ. Code §1946.1(d) 30-day sale exception (2025 code, per SB 1103) — logged in `docs/MISSING_RULES_BACKLOG.md`. Per explicit instruction: log-only, no drafting until an item needs it.

### YELLOW — Ratified for next-session execution (not executed this session)

**Proposal 16 — APPROVED.** Self-critique pass (Disciplines A/B/C) over `just_cause_attachment_threshold`, executing next session. Andy's independent verification of §1946.2(a)(2) against verbatim statute text (07-20) is logged as corroboration for that pass; citation label correction ("§1946.2(a), second sentence, prongs (1)–(2)") deferred to the next version cut, not a v3 edit. **Scope extended:** also assess SB 1103's amendments to §1946.1 ("qualified commercial tenants," reworded subdivisions (a)–(c)) for any needed flagged update. Full text in `docs/WORK_QUEUE.md`.

**Proposal 17 — APPROVED, v0.4 is a GO.** Under the amended freeze/drafting protocols, with an added design requirement: the v0.4 held-out scoring event runs a second ablation arm (same models/items, no rules file, same frozen ground truth) to measure the rules' accuracy contribution. Build into the scoring-harness plan before candidate drafting begins; reflect in the v0.4 direction doc. Begins after 16 completes. Full text in `docs/WORK_QUEUE.md`.

### RED — None this cycle.

### Scope note
This entry logs ratification decisions and the dispatcher/housekeeping fixes only. Proposals 16 and 17's substantive execution (the self-critique pass itself; v0.4 candidate drafting and the ablation harness build) is explicitly sequenced for a subsequent session, per Andy's own instruction ("16 executes next session... v0.4 drafting (17) begins after 16 completes") — not performed here.

---

## 2026-07-21 (morning report — automated)

### GREEN — Executed autonomously (morning report cycle)

**Overnight scan — no dispatcher output; SIXTH consecutive missed fire**
- `dispatcher_heartbeat.log` still does not exist (`no-heartbeat`); `launchd_stdout.log` last write still 07-15 ~2:24 AM. Miss ×6 (07-16→07-21). Classification unchanged (agent-unloaded-leaning); folded into the standing RED. No new files in `l2/output/`, `results/`, `scorer/output/`, `queue/`→`done/`/`failed/` since the 07-20 gate run + same-day ingestion.
- Queue holds only the recurring D-1 monitor job; next cadence-eligible ≥ 07-23 (3 days after the 07-20 trigger-fired run) — would have self-deferred at 2:15 AM regardless.

**v3 gate-passed state audited consistent**
- Cross-checked score output (`ca_notice_score_2026-07-20_non-held-out.json`: 12/12, α=1.000, newly_failing=0, rules_sha256 = v3), `dev_set_trend.jsonl` (07-20 row, `triggered_by_rule_change: true`), ledger v3 version record (gate row = PASSED), PSOR header, RULE_PROPOSAL status. All consistent — nothing to correct. Scope note logged in the ledger: the gate verifies dev-set non-regression; direct re-test of the C-18 pattern awaits v0.4.

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR/SM in the attorney lane; HUMAN_REVIEW_QUEUE unchanged (RC=6, CI=2).

**Living docs updated this cycle**
- VALIDATION_METRICS_LEDGER (07-21 cycle entry), PROJECT_STATE_OF_RECORD (morning-report annotation), HUMAN_REVIEW_QUEUE (header — no new items), WORK_QUEUE (header; NOW-empty + proposal-16-gate-met flags; git-commit housekeeping suggestion), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (Step 3f).

### YELLOW — None this cycle.

### RED — Decisions/actions on Andy
1. **Overnight machine environment — miss ×6, `no-heartbeat` (single top RED):** plist reinstall + launchctl reload (unchanged command). Remaining payoffs: reopens the overnight lane; activates the noon fire (D-1's only automatic daytime driver — next eligible run ≥ 07-23 silently won't happen without it or Terminal).
2. **Refill proposals 16–18 approve/reject (from 07-20):** 16 = §1946.2(a)(2) live-source self-critique (its gate condition — v3 regression pass — is now met; executable immediately on approval); 17 = v0.4 golden-set go/no-go (RED-gated); 18 = §1946.1(d) backlog grooming (needs attorney-sourced text).
3. **Housekeeping (non-urgent):** last git commit 2026-06-16 — consider commit/push of the last five weeks of work.

---

## 2026-07-20 (dev-set regression gate PASSED — v3 fully active, errata-cycle directive closed)

*Andy ran the real live regression: `python3 rules/validation/scorer/dev_set_monitor.py` — real keys, 10:31 AM PT, trigger-fired.*

### GREEN — Verified and logged

**Result: 12/12 = 100%, `newly_failing: []`, DUAL-MODEL-CONSENSUS (α=1.000), `triggered_by_rule_change: true`.** Pulled and verified the output directly (`rules/validation/scorer/output/ca_notice_score_2026-07-20_non-held-out.json`) rather than transcribing from screenshot — `rules_sha256` confirmed matches v3 exactly (`65f1d9a4…947c7d`). `RULE_CHANGE_TRIGGER.flag` was consumed by the run itself, as designed.

**Docs corrected from PENDING to PASSED** (the same-day automated morning-report commit had logged this cycle's narrative before the live run completed, so a few spots still said "PENDING" after the fact — fixed, not re-litigated): `docs/VALIDATION_METRICS_LEDGER.md` (v3 version record's gate row; the B3 line in the 07-20 morning-report cycle entry), `docs/PROJECT_STATE_OF_RECORD.md` (header), `docs/RULE_PROPOSAL_1946_2a_ATTACHMENT_20260719.md` (status line).

**Errata-cycle directive (2026-07-19/20) is now closed end-to-end:** v0.3 held-out scored and burned → attorney errata corrected C-21/C-22 → miss autopsy → wiring determination (companion doc, `ca_eviction_v2.json` never touched) → rule proposal for C-18 → Andy's ratification → `ca_eviction_v3.json` cut → dev-set regression gate passed. `ca_eviction_v2.json` (vProof1) remains byte-frozen and immutable throughout, confirmed at every step.

---

## 2026-07-20 (morning report — automated)

### GREEN — Executed autonomously (morning report cycle)

**Overnight scan — no dispatcher output; fifth consecutive missed fire**
- `--heartbeat-status` → `{"state": "no-heartbeat"}`; `dispatcher_heartbeat.log` still does not exist; `launchd_stdout.log` last write still 07-15 ~2:24 AM. Miss ×5 (07-16→07-20). Classification unchanged (agent-unloaded-leaning); folded into the standing RED. No new files in `l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (07-09). Queue holds only the recurring D-1 monitor job.
- D-1 monitor did NOT run despite being cadence-eligible since 07-19 (dispatcher dark; no Terminal run — `dev_set_trend.jsonl` unchanged since the 07-16 baseline). The armed `RULE_CHANGE_TRIGGER.flag` (07-20 07:32 PT) now makes the next run the v3 regression gate.

**Cycle roll-up (no re-logging — pointers only)**
- The weekend's substantive events (v0.3 held-out burn → errata → autopsy → proposal → ratification → v3 cut) were session-driven and already logged in their own dated entries below and in the ledger's Broaden Proof 1 / v3 sections. This cycle added the ledger's 07-20 cycle entry (dual-reported score 88.5%/96.2%, α=1.000, ground-truth error rate 2/26 = 7.7%, B1–B4 with B3=PENDING-REQUIRED).

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR/SM in the attorney lane. The C-18 gap was resolved through the proposal→ratification lane (correct lane, not attorney-queue default); C-21/C-22 were attorney-side ground-truth errors corrected by signed errata — neither touched HUMAN_REVIEW_QUEUE.

**Living docs updated this cycle**
- VALIDATION_METRICS_LEDGER (07-20 cycle entry), PROJECT_STATE_OF_RECORD (morning-report annotation), HUMAN_REVIEW_QUEUE (header — no new items), WORK_QUEUE (header; Broaden Proof 1 Steps 4–7 closed out; refill proposals 16–18), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (Step 3f).

### YELLOW — None this cycle (the v3 cut was ratified RED→approved before this report; nothing new awaiting ratification from this cycle itself).

### RED — Decisions/actions on Andy (standing + new)
1. **Overnight machine environment — miss ×5, `no-heartbeat`:** plist reinstall + launchctl reload (unchanged command); now also auto-runs the armed v3 regression gate at the first noon drain.
2. **v3 dev-set regression gate:** `python3 rules/validation/scorer/dev_set_monitor.py` (real keys, 09:00–23:00 PT; no --force needed). Required: 12/12, newly_failing=0 — else Cowork reverts ACTIVE_RULES_FILE to vProof1 and reports RED.
3. **Residuals:** §1946.2(a)(2) variant verification vs. verbatim statute (carried B4 flag); §1946.1(d) backlog drafting timing; v0.4 golden-set go/no-go.

---

## 2026-07-20 (Task 4: ratified rule applied — new rules version v3 ACTIVE, dev regression pending)

*Context: Andy ratified `docs/RULE_PROPOSAL_1946_2a_ATTACHMENT_20260719.md` ("confirmed - i approve"). Per Task 4 of the errata-cycle directive: cut a new rules version, embed the wiring determination, arm the dev-set regression trigger, and hand off the live-run command.*

### GREEN — Executed autonomously

**New rules version cut — vProof1 untouched**
- `rules/eviction/california/ca_eviction_v3.json` **(new file)** — copy of vProof1 plus: `notice.notice_types.termination.just_cause_attachment_threshold` (Civ. Code §1946.2(a) 12-month general rule + §1946.2(a)(2) additional-adult-tenant variant, exactly as ratified); `notice_defects[missing_just_cause_reason].ab1482_coverage_gate` note updated to check attachment first; `provenance.determinations` now embeds the 2026-07-19 wiring determination verbatim (id `WIRING-DETERMINATION-2026-07-19`); `version_history` block added recording the change and its supersession of vProof1.
- **`ca_eviction_v2.json` (vProof1) is untouched** — confirmed byte-identical, SHA still `cc0cfab63ae1591e2b88…`. It is not deleted; retained permanently as the immutable v0.3 held-out scoring anchor.
- New file SHA256: `65f1d9a46487873163cd9ef5c5e2285c95a68bddb81e876a17e534b3de947c7d`.

**Scorer updated to the new active version (single reference point)**
- Searched the codebase for every consumer of `just_cause_required`/`ab1482_coverage_gate`/the rules file path before changing anything: only `rules/validation/scorer/ca_notice_scorer.py::load_ca_notice_rules()` hardcoded the filename; no test hardcodes it either. Replaced the hardcoded `"ca_eviction_v2.json"` with a named `ACTIVE_RULES_FILE = "ca_eviction_v3.json"` constant, documented so the next version bump is a one-line change.

**Verification performed (mechanical; no live model calls — this sandbox has placeholder keys only)**
- JSON validity: v3 parses clean.
- Battery schema validator (`layer3_notice`) run against v3: 2 errors, both confirmed pre-existing and identical in vProof1 (`notice_defects[6]` consequence/severity values not in the validator's enum) — not introduced by this change, not fixed here (out of scope for this ratification; logged for awareness only).
- `test_ca_notice_scorer_outcome_fallback.py`: 15/15 pass, unaffected by the `ACTIVE_RULES_FILE` change.
- `dev_set_monitor.py --force --dry-run`: pipeline runs end-to-end against v3 with no crashes or schema errors (dry-run always shows all-items-failing by design — mocked predictions, not a real accuracy signal; this only confirms the wiring, not correctness). Stray dry-run output file and `dev_set_trend.jsonl` touch reverted before commit — dry runs must not pollute the real trend log.

**Regression trigger armed for the real gate**
- `arm_trigger()` called — `rules/validation/scorer/output/RULE_CHANGE_TRIGGER.flag` written. The next live `dev_set_monitor.py` run will bypass the 3-day cadence guard automatically (this is exactly the "immediately after any ratified rule change" case the trigger was built for in Item 13). The daytime-window guard still applies — run during Andy's normal window, real keys.

**Docs updated**
- `docs/VALIDATION_METRICS_LEDGER.md`: new v3 version record (parallel structure to the vProof1 freeze record), rule-freeze gate marked PENDING pending the live regression.
- `docs/RULE_PROPOSAL_1946_2a_ATTACHMENT_20260719.md` and `docs/WIRING_DETERMINATION_1946_2e_20260719.md`: both updated from PROPOSED/staged to RATIFIED/embedded, pointing at v3.
- `docs/PROJECT_STATE_OF_RECORD.md`: header updated.

### RED — dev-set regression gate open (not yet run; real keys required)

**For Andy, daytime window, real keys:**
```
cd ~/Documents/GitHub/a2j-ai
python3 rules/validation/scorer/dev_set_monitor.py
```
No `--force` needed — the armed trigger already bypasses cadence. **Required result: 12/12 with `newly_failing=0`.** Any regression → Cowork reverts `ACTIVE_RULES_FILE` to `ca_eviction_v2.json` (vProof1) and reports RED; v3 is not treated as active until this gate passes. Share the output back for the ledger.

**Also carried, unrelated, no action:** `notice_defects[6]` non-enum consequence/severity values (pre-existing in vProof1, inherited into v3 unchanged) — minor schema-validator finding, not blocking, not fixed this cycle.

---

## 2026-07-19 (night — errata-cycle directive Tasks 2 (amended), 3 (narrowed), 4, 5)

*Context: Andy clarified there are two directives in play — the score-cycle directive (Tasks 1-4, executed earlier today) and the errata-cycle directive, which supersedes it in part. Full task text for the outstanding items provided; executed below.*

### Task 2 (amended) — wiring determination recorded as companion doc, not a rules-file edit

- `docs/WIRING_DETERMINATION_1946_2e_20260719.md` **(new)**: records the attorney-ratified negative determination that `ab1482_coverage_gate` correctly does NOT reach `notice_period_too_short` — §1946.2(e) exemptions remove the just-cause obligation only; §1946.1(b)/(c) applies independently (Stancil). **Do not "fix."** `ca_eviction_v2.json` is NOT edited — vProof1 stays byte-frozen at `cc0cfab63ae1591e2b88…` permanently, per Andy's explicit instruction. Staged for the future: once the C-18 rule proposal below is ratified and cuts a new rules version, this determination gets embedded in that version's internal notes/metadata so it travels with the file itself.
- `docs/PROJECT_STATE_OF_RECORD.md`: cross-reference added.
- `docs/AUTOPSY_v0_3_MISSES_20260719.md`: addendum appended — the proposed "exemption-scope-limited-to-single-defect" taxonomy class is marked NOT ADOPTED for this instance (the limitation was legally correct, not a gap); class definition retained in taxonomy notes as a future autopsy check.

### Task 3 (narrowed) — `just_cause_attachment_threshold` rule proposal, YELLOW, ratification-ready

- `docs/RULE_PROPOSAL_1946_2a_ATTACHMENT_20260719.md` **(new)**, supersedes `docs/RULE_PROPOSALS_AB1482_20260719.md` (marked superseded in place, retained for record). One rule: `just_cause_attachment_threshold`, general 12-month rule (source: frozen CA-NOT-C-18 authority field, corroborated against C-19) plus the §1946.2(a)(2) additional-adult-tenant variant (source: attorney-directed text supplied directly in this directive — flagged, not independently statute-verified by Cowork, recommend confirming against verbatim §1946.2(a)(2) at ratification). Inputs are per-tenant occupancy durations (not the aggregate max used elsewhere), since the (a)(2) variant needs per-tenant granularity. Includes a non-regression check against C-19 (already-correct; this proposal must not change its result). `ca_eviction_v2.json` not touched.

### Task 4 — missing-rules backlog entry, no drafting

- `docs/MISSING_RULES_BACKLOG.md` **(new)** — first entry: Civ. Code §1946.1(d), the narrow 30-day sale exception for 1+-year tenancies. Not implicated by any current item; not drafted (no attorney-sourced statutory text for the escrow/sale conditions yet). Andy's call on when to draft.

### Task 5 — golden-set freeze/drafting protocol amended (v0.4 forward)

- `docs/COWORK_DIRECTION_B_GOLDEN_SETS.md` amended in place (dated inline annotations, original text retained): Part 2 step 2 (drafting) now requires each candidate item to declare every defect class its facts implicate, not only the target defect. Part 2 step 3 (freeze/attorney review) now requires an explicit per-item sweep against every encoded defect class in the module (the rules file's ratified defect list serves as the checklist), and states model outputs may not be consulted during ground-truth review. Root cause cited inline: the 2026-07-16 v0.3 freeze session's single-lens review of C-21/C-22, corrected by the same-day errata.

**Nothing else pending in this lane.** Tasks 1-5 of the errata-cycle directive (as clarified) are now complete; Task 3's proposal and the wiring determination await Andy's ratification pass before any new rules version is cut.

---

## 2026-07-19 (late evening — Task 3: candidate rule proposal for C-18, YELLOW, ratification-ready)

*Context: Andy corrected a routing misread — Task 3 of the 07-19 directive was already authorized for C-18 (Task 2 confirmed the §1946.2(a) rule genuinely absent), even though it was correctly not warranted for C-21/C-22 (confirmed not a gap, per errata). Proceeding with Task 3 for C-18 only.*

### YELLOW — proposed, not applied (attorney ratification gate)

**`docs/RULE_PROPOSALS_AB1482_20260719.md` delivered** — one candidate rule, PROPOSED-2026-001: closes the §1946.2(a) 12-month just-cause-attachment gap that caused C-18's miss. Operative text drawn verbatim from the frozen golden-set authority field (attorney-verified 2026-07-16) per the directive's canonical-source requirement — no independent statutory text asserted. Proposed encoding reuses the existing `all_occupants_residency_max_years` input (no new fact input); proposed defect-gate update to `missing_just_cause_reason`'s `ab1482_coverage_gate`, checked ahead of the exemption checklist. One open methodology question flagged for Andy (whether the Stancil any-occupant convention applies to §1946.2(a) attachment, same as it does to §1946.1(b)/(c)) rather than assumed.
- **§1946.2(a)(2)'s 24-month/"additional adult tenants" variant NOT drafted** — no frozen item tests it and no attorney-verified source text specifies the trigger mechanics; flagged for Andy to decide (draft now with source text, defer to this same ratification, or defer to v0.4).
- `ca_eviction_v2.json` **not touched** — proposal only, in ratification-ready item-by-item form mirroring golden-set freeze discipline.

**Confirmed for the record: nothing else pending in this lane.** Task 1 (ledger/state/changelog writeup) and Task 2 (miss autopsy) were both completed and pushed same day (commits `8e894ae`, `aaaa4a5`). Task 4 (post-ratification: cut new rules version, run 12/12 dev regression) is correctly not started — it's staged behind ratification of the proposal above, per the directive's own sequencing, not an oversight.

---

## 2026-07-19 (evening — attorney errata: v0.3 held-out score corrected, C-21/C-22 ground truth was wrong)

*Context: Andy delivered a signed Attorney Errata Memorandum (`docs/ERRATA_MEMO_v0_3_20260719.docx`) same day as the held-out score and miss autopsy, resolving the open legal question the autopsy flagged but could not answer itself.*

### GREEN — Executed autonomously (ingestion + dual-report writeup; no rules or golden-set data touched)

**Errata memo ingested**
- Committed both `docs/ERRATA_MEMO_v0_3_20260719.docx` (signed `/s/ Andrew M Cohen`, dated 07/19/2026 — the executed, authoritative instrument) and `docs/ERRATA_MEMO_v0_3_20260719.md` (plain-text reference copy, flagged at its top as non-authoritative where the two differ).
- The golden-set xlsx (`goldenset_CA_notice_v0.3_FROZEN_20260716.xlsx`) is **unchanged** — SHA256 still `e6dbb2fc…5df45`, still BURNED, still not re-scored. The errata is a correction overlay per the memo's own terms, not a data edit.

**Determination**
- Civil Code §1946.1 (notice-period length) governs independently of §1946.2/AB 1482 (just-cause). An AB 1482 exemption under §1946.2(e)(7)/(e)(8) removes the just-cause obligation only — it does not shorten or excuse §1946.1(b)'s 60-day notice period for a 1+-year tenancy (*Stancil v. Superior Court* (2021) 11 Cal.5th 381). C-21 (18-month tenancy) and C-22 (2-year tenancy), both served 30-day notices, are void under §1946.1(b)/Stancil regardless of their valid AB 1482 exemptions.
- **ERRATUM-2026-001 (C-21) and ERRATUM-2026-002 (C-22): frozen NOTICE_VALID → corrected NOTICE_INVALID.** The dual-model consensus (which had said NOTICE_INVALID) was legally correct; the frozen ground truth was the error. **C-18 unaffected** — 9-month tenancy, 30-day notice proper under §1946.1(c); frozen VALID stands.

**Metrics dual-reported everywhere the v0.3 score is cited** (per the errata memo's Section 4 requirement)
- As-scored (2026-07-19 afternoon): 23/26 = 88.5%, CI [71.0%, 96.0%]. Post-errata: **25/26 = 96.2%**, CI [81.1%, 99.3%] (both Wilson). Neither number superseded — both retained in the record.
- B2 confident-wrong restated: 3 (as-scored) → **1** (post-errata — C-18 only).
- **New metric: ground-truth error rate = 2/26 = 7.7%**, logged as a validation finding in its own right — the review pipeline caught the encoder's citation errors at freeze; the scoring pipeline caught the attorney-side oversight at measurement. Both directions of the loop functioned.
- `docs/VALIDATION_METRICS_LEDGER.md` updated: trend row, Result line, B1-B4 line, v0.2 comparison line, and the B2/autopsy analysis paragraphs — all via append-style annotation (original as-scored text retained, errata correction appended after), not silent rewrite, consistent with this project's frozen-record discipline.
- `docs/PROJECT_STATE_OF_RECORD.md`: new header entry. `docs/AUTOPSY_v0_3_MISSES_20260719.md`: addendum appended noting its flagged open question is now resolved and its engineering conclusion (rules correctly NOT wired to `notice_period_too_short`) is confirmed, while its factual premise (C-21/C-22 as model errors) is superseded.

**Corrective protocol adopted (effective immediately, v0.4 forward)**
- Root cause: single-lens review at the 2026-07-16 freeze session — C-21/C-22 were reviewed only through the AB 1482 exemption analysis they were drafted to test; no independent §1946.1 duration check was run. Classified as an incomplete-defect-sweep failure.
- Going forward, every candidate golden-set item must be swept against every encoded defect class in its module, not only the class it was drafted to test. Model outputs may not be consulted during ground-truth review.

### RED — updated
1. **Overnight machine environment:** unchanged, still open.
2. **§1946.2(e)(7)/(e)(8) wiring/scope gap (C-21, C-22): RESOLVED, closed.** Confirmed not a rules bug — the exemption legitimately does not reach `notice_period_too_short`; no rule edit warranted.
3. **§1946.2(a) 12-month attachment threshold (C-18): still open, still RED.** Genuine coverage gap, confirmed absent from vProof1. `ca_eviction_v2.json` untouched. Awaiting Andy's routing decision.

---

## 2026-07-19 (afternoon — Broaden Proof 1 Steps 5-7: v0.3 held-out set scored and burned)

*Context: Andy ran the real, one-time held-out score from Terminal (real API keys, daytime window, per the freeze memo's own instructions). This is the last step of Broaden Proof 1 — the held-out set is now permanently burned and this result is not to be repeated.*

### GREEN — Executed autonomously (analysis only; no code or rules touched)

**Held-out score ingested and verified**
- Pulled `rules/validation/scorer/output/ca_notice_score_2026-07-19_held-out.json` from the commit Andy pushed. Provenance checks pass: `rules_sha256` matches vProof1 (`cc0cfab63ae1591e2b88…`, unchanged since the 07-02 freeze) and `excel_sha256` matches the certified freeze hash (`e6dbb2fc…5df45`) exactly.
- **Result: 23/26 = 88.5% (95% CI [71.0%, 96.0%], Wilson score interval).** `consensus_status: DUAL-MODEL-CONSENSUS` (both GPT and Gemini answered all 26 items; `single_model_items=0`).
- **Krippendorff's α = 1.000** (GPT vs. Gemini, nominal, n=26, computed by hand from the run's per-item model outcomes: Do=0.000 observed disagreement, De=0.540 expected disagreement from the pooled label distribution). Perfect model-pair agreement.
- **B1:** 88.5% coverage. **B2:** confident-wrong=3 (CA-NOT-C-18, C-21, C-22 — all `model_agreement: AGREE`, both models HIGH confidence, both wrong). **B3:** n/a (first live run against this set). **B4:** no rule changes since vProof1; not triggered.

**B2 finding — a real coverage gap, written up for Andy, no rules touched**
- All three confident-wrong items are AB 1482 exemption fact patterns under Civ. Code §1946.2(e)(7) (new-construction/certificate-of-occupancy exemption) and §1946.2(e)(8) (separately-alienable SFH exemption). Both models correctly applied the *default* just-cause/notice-period requirement and voided the notice for missing it — but the frozen ground truth is NOTICE_VALID because the exemption applies. These are the same three items where Andy's freeze review had to correct the golden-set citations for exactly this (e)(7)/(e)(8) distinction, suggesting the exemption boundary genuinely isn't encoded (or isn't reliably triggered) in `ca_eviction_v2.json` at vProof1.
- **No rule edits made or attempted** — per the freeze record's standing rule ("NO RULE EDITS PERMITTED... discovered gaps → next development cycle with fresh held-out set"). Full writeup with per-item detail is in `docs/VALIDATION_METRICS_LEDGER.md`'s Broaden Proof 1 section.

**Docs updated**
- `VALIDATION_METRICS_LEDGER.md`: trend row updated to BURNED/88.5%; freeze record's "Next step" section replaced with the full result writeup (95% CI, α, B1-B4, B2 cluster analysis).
- `docs/PROJECT_STATE_OF_RECORD.md`: header updated — Broaden Proof 1 now complete end-to-end (Steps 1-7); new RED opened for the §1946.2(e)(7)/(e)(8) coverage gap.

**Follow-up directive received same afternoon: "v0.3 Held-Out Score Ingestion & AB 1482 Rule-Gap Cycle" (Andy, 2026-07-19).** Confirmed Task 1 (ledger/state/changelog writeup) already matched the directive's requirements; added the explicit v0.2→v0.3 comparison line and the "BURNED, dev-set-only, v0.4-gate" language it specified. Executed Task 2 (miss autopsy) below. Task 3 (candidate rule drafting) was gated on Task 2 and did not proceed — see below.

**Miss autopsy executed (Task 2) — result is mixed, not a clean coverage gap**
- Inspected `rules/eviction/california/ca_eviction_v2.json` (confirmed identical to vProof1, SHA matches) directly for each of the three suspect provisions, and cross-referenced against which defect each miss actually fired on (from the score JSON's `gpt_controlling_rule`/`gemini_controlling_rule` fields).
- **§1946.2(a) 12-month attachment threshold: genuinely ABSENT.** `just_cause_required` is a flat `true` with no occupancy-duration gate anywhere in the file — confirmed by full-file search. Explains C-18. Missing-rule hypothesis CONFIRMED for this item.
- **§1946.2(e)(7) and (e)(8): both PRESENT and fully encoded** (rolling 15-year window for (e)(7); two-prong REIT/corp/LLC + written-notice test for (e)(8); both ratified by Andy 2026-07-01). But both models fired `notice_defects[notice_period_too_short]` for C-21/C-22 — a different defect than the one these exemptions are wired to (`missing_just_cause_reason` only). The exemption logic exists, correctly, and simply isn't reachable from the defect that actually fired. Missing-rule hypothesis DISCONFIRMED for these two items.
- Full writeup, including a proposed new error-taxonomy class ("exemption-scope-limited-to-single-defect," YELLOW, not yet adopted) and an open legal question this autopsy cannot resolve (whether the AB 1482 exemption should also reach the general §1946.1(b)/Stancil notice-period defect): `docs/AUTOPSY_v0_3_MISSES_20260719.md`.

### YELLOW — proposed, not adopted
- New error-taxonomy class candidate: "exemption-scope-limited-to-single-defect" (see autopsy memo). Andy's call.

### RED — one gate fully closed, two items opened, Task 3 explicitly not executed
1. **Overnight machine environment:** unchanged, still open (agent-unloaded-leaning; one launchctl action tests+fixes).
2. **§1946.2(a) 12-month attachment threshold — genuine coverage gap (C-18).** `ca_eviction_v2.json` untouched.
3. **§1946.2(e)(7)/(e)(8) wiring/scope gap (C-21, C-22) — NOT a coverage gap.** Per the directive's own stop condition ("if the missing-rule hypothesis is DISCONFIRMED... STOP the cycle... queue as RED"), **Task 3 (candidate rule drafting) was not executed.** Two things need Andy's decision before any rule text is drafted: (a) whether the AB 1482 just-cause exemption should also gate the separate, non-AB-1482 §1946.1(b) notice-period defect, and (b) how to encode the (a) attachment threshold. `ca_eviction_v2.json` untouched.

**Broaden Proof 1 v0.3 held-out freeze RED (the original blocking item): now fully CLOSED** — Steps 1-7 complete, held-out set burned, result logged, autopsy delivered.

---

## 2026-07-19 (morning report — automated)

### GREEN — Executed autonomously (morning report cycle)

**Overnight scan — no new output**
- No new files in `rules/validation/l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (ingested 07-09). `failed/` unchanged (job_nc17_fresh_20260625 only). Queue holds only the recurring D-1 monitor job.

**First live use of the B-3 heartbeat tool — dispatcher miss #4 confirmed definitively**
- `python3 rules/validation/dispatch.py --heartbeat-status` → `{"state": "no-heartbeat"}`. `logs/dispatcher_heartbeat.log` does not exist — the B-1-instrumented `dispatch.py` has never been invoked by launchd since installation (07-16→07-18). `launchd_stdout.log` last write remains 07-15 ~2:24 AM. Fourth consecutive miss (07-16, 07-17, 07-18, 07-19).
- **Diagnostic advance (GREEN analysis, no action taken):** this is the first miss AFTER Andy's Part A mitigation (`sudo pmset -c sleep 0` + lid-open, applied 07-17) — the idle-sleep-timer hypothesis alone no longer explains the pattern; evidence shifts toward **launchd agent-unloaded** (or clamshell/battery sleep outside `pmset -c` scope). Testable and fixable by the same launchctl reinstall steps Andy already needs to activate the 07-18 noon fire.

**Timing escalation — D-1 cadence-eligible TODAY (07-19)**
- Flagged in the morning report with the two concrete paths: (a) plist reinstall before noon → 12:00 PM fire runs the monitor automatically in-window; (b) Terminal fallback `python3 rules/validation/scorer/dev_set_monitor.py` (09:00–23:00 PT). Either is the convert-to-consensus opportunity for the SM-GPT baseline.

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR/SM cases in the attorney lane; the only failure-condition item is the dispatcher miss (infrastructure — logged, folded into the standing RED).

**Living docs updated this cycle**
- VALIDATION_METRICS_LEDGER (07-19 cycle entry incl. heartbeat classification + B1–B4), PROJECT_STATE_OF_RECORD (header), HUMAN_REVIEW_QUEUE (header — no new items), WORK_QUEUE (header + item 15 status + Completed), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (Step 3f).

### YELLOW — None this cycle.

### RED — Escalated (standing, both waiting on Andy)
- **Overnight machine environment (updated):** dispatcher miss ×4, now `no-heartbeat`-classified; agent-unloaded-leaning. Single convergent action: `cp rules/validation/com.cjac.validation.plist ~/Library/LaunchAgents/com.cjac.validation.plist && launchctl unload ~/Library/LaunchAgents/com.cjac.validation.plist && launchctl load ~/Library/LaunchAgents/com.cjac.validation.plist && launchctl list | grep cjac`.
- ~~**v0.3 held-out freeze:** 28 DRAFT items still waiting on attorney review/freeze~~ — **CLOSED later same day:** Andy delivered the completed freeze; see the entry immediately below (26 FROZEN/2 EXCLUDED, Broaden Proof 1 Step 4 COMPLETE). Steps 5-7 (live score) still pending Andy.

---

## 2026-07-18 (v0.3 held-out freeze ingested — Broaden Proof 1 Step 4 COMPLETE; Steps 5-7 pending Andy)

*Context: Andy completed his item-by-item attorney review of the 28-item v0.3 DRAFT held-out set (started per the 07-16 directive), delivering `goldenset_CA_notice_v0.3_FROZEN_20260716.xlsx` + a freeze decision memo. This is the RED gate that has blocked Broaden Proof 1 Steps 5-7 since 07-02. This entry logs ingestion and a scorer bug found while verifying the file was actually scoreable — the real held-out score itself has NOT been run (requires Andy, real API keys, daytime window — see below).*

### GREEN — Executed autonomously

**Freeze ingested and verified**
- Copied `goldenset_CA_notice_v0.3_FROZEN_20260716.xlsx` into `rules/validation/scorer/FROZEN/`. SHA256 verified matching Andy's certified freeze memo both on the raw upload and post-copy: `e6dbb2fcb60de0773f9ff5594e09f74c6a6bac5670c70bd9bb76d70e2645df45`.
- **26 items FROZEN (scoreable), 2 EXCLUDED (C-05, C-13) — n changes from 28 (draft) to 26.** Distribution: NOTICE_VALID=14, NOTICE_INVALID=11, UD_DEFECTIVE_PREMATURE=1. Full detail, rulings, and the six citation corrections made at freeze are in `docs/VALIDATION_METRICS_LEDGER.md`'s updated "v0.3 FROZEN held-out set" record (Broaden Proof 1 section) — not duplicated here.
- **Broaden Proof 1 Step 4 (attorney freeze) is now COMPLETE.** Rules remain frozen at vProof1 (`cc0cfab63ae1591e2b88…`) — this memo authorizes no rule edits, and none were made; only golden-set authority-field corrections (citations), which do not touch `ca_eviction_v2.json`.

**Scorer bug found and fixed while verifying the file was actually scoreable**
- Before handing Andy a "run this once" command for an irreversible held-out burn, dry-ran the pipeline against the real file first (per this project's standing discipline: verify mechanically before a precious one-shot action). Result: `ca_notice_scorer.py` flagged all 26 items as `YELLOW-INCOMPLETE` — it requires "Correct outcome (if corrected)" to be populated for every FROZEN row, but this file leaves that cell blank whenever `ATTORNEY VERDICT=CONFIRM`, which is the natural reading of the column's own name ("if corrected" — Andy didn't correct these, he confirmed them). All 26 FROZEN rows in this file are CONFIRM with a blank "Correct outcome" cell; the two EXCLUDED rows are unaffected (already skipped by status).
- **Fix:** `load_golden_set()` now falls back to the "Drafted outcome" column, but only when `ATTORNEY VERDICT` is `CONFIRM` or `CONFIRMED` — any other verdict (or a blank one) with an empty "Correct outcome" still fails loud via the existing `YELLOW-INCOMPLETE` path, unchanged. An explicit "Correct outcome" value (the v0.2 file's convention — always populated, even on confirms) always wins and is never overridden by this fallback. No golden-set data file was modified — this is purely a parsing fix; the xlsx's SHA256 is identical before and after, still matching Andy's certified hash.
- **Verification:** re-ran the dry-run after the fix — clean load, 0 YELLOWs, 26/26 items resolved. Manually cross-checked all 26 resolved outcomes against Andy's freeze memo ruling table (ID-by-ID) — exact match, including the 14/11/1 distribution. Regression tests added: `rules/validation/tests/test_ca_notice_scorer_outcome_fallback.py`, 15/15 pass, covering the fallback itself, the CONFIRM/CONFIRMED verdict variants, the "explicit value always wins" non-regression case (protects the v0.2 file's existing convention), and that genuinely incomplete rows (blank/unrecognized verdict) still fail loud rather than being silently guessed. Full existing suite re-run clean: `test_dev_set_monitor.py`, `test_dispatcher_heartbeat.py` (34/34), `test_l2_procedural_defects.py` (30/30), `test_retaliation_holdings_disposition_note.py` (26/26).

**Docs updated**
- `VALIDATION_METRICS_LEDGER.md`: Broaden Proof 1 trend row updated to FROZEN/n=26; "v0.3 draft held-out set" record replaced with the full FROZEN record (exclusions, citation corrections, scorer fix, next-step command).
- `docs/PROJECT_STATE_OF_RECORD.md`: Broaden Proof 1 Step 4 marked COMPLETE.

### RED — one gate closed, one step remains (not yet actioned)

**Broaden Proof 1 Steps 5-7 — the actual held-out score — NOT YET RUN.** This is deliberately not something this session executes: (a) requires real `OPENAI_API_KEY`/`GOOGLE_API_KEY` — this sandbox only has placeholders; (b) per Andy's freeze memo, must run in the **daytime window**, not overnight (the environment RED's overnight lane is still being proven out after last night's sleep-timer fix — no reason to risk this precious one-time run on it); (c) burning the held-out set is irreversible — the mechanical pipeline was verified end-to-end via dry-run first specifically so the real run only needs to happen once.

**For Andy, when ready (daytime, real keys):**
```
cd ~/Documents/GitHub/a2j-ai
python3 rules/validation/scorer/ca_notice_scorer.py --golden rules/validation/scorer/FROZEN/goldenset_CA_notice_v0.3_FROZEN_20260716.xlsx --held-out-only
```
No `--dry-run`, no `--force` needed (this script doesn't self-throttle like `dev_set_monitor.py`). Share the output (or the saved `rules/validation/scorer/output/ca_notice_score_*_held-out.json`) back for the 95% CI, Krippendorff's α, and B1-B4 write-up, and to log the burned result in the ledger.

**Also carried:** overnight-environment RED (DNS/sleep fix applied 07-17, `--heartbeat-status` will confirm over the next few nights); C-05/C-13 open-textured queue candidates (not yet scheduled — companion work to the future open-textured module, no urgency).

## 2026-07-18 (follow-up session — noon daytime dispatcher fire + recurring-job fix)

*Context: Andy asked about adding a second (noon) daytime dispatcher fire so Item 13's dev-set monitor (self-throttled to a 09:00–23:00 window) has an automatic driver — the 02:15 overnight fire alone can never land inside that window (flagged as an open structural gap in the 07-17 and prior entries, and as WORK_QUEUE item 15). While wiring it, found and fixed a real bug that would have silently capped the monitor's cadence at exactly one dispatcher-driven run, ever.*

### GREEN — Executed autonomously

**Noon fire added**
- `rules/validation/com.cjac.validation.plist`: `StartCalendarInterval` changed from a single dict to an array — now fires at both 02:15 AM (unchanged) and 12:00 PM. `dispatch.py`'s `SCHEDULED_TIMES` list kept in sync for accurate FIRED-delta computation (see below).
- **Action needed from Andy to activate:** the installed copy at `~/Library/LaunchAgents/com.cjac.validation.plist` is a *copy*, not a symlink — updating the repo file alone doesn't change what launchd runs. After pulling this change: `cp rules/validation/com.cjac.validation.plist ~/Library/LaunchAgents/com.cjac.validation.plist`, then `launchctl unload ~/Library/LaunchAgents/com.cjac.validation.plist && launchctl load ~/Library/LaunchAgents/com.cjac.validation.plist`, then confirm with `launchctl list | grep cjac`.

**Bug found and fixed — recurring jobs were being silently dropped from the queue**
- `finalize_job()` unconditionally moved every job out of `queue/` (to `done/` or `failed/`) after its subprocess exited, regardless of exit code. For one-shot protocol/l2_module jobs that's correct. For Item 13's scorer job — which is designed to sit in the queue indefinitely and self-defer (exit 0, no work done) on any cycle outside its window/cadence — this meant the **very first** dispatcher pickup, successful or not, would remove the job file from `queue/` for good. The job's own JSON already claimed "safe to leave in queue/ for repeated dispatcher drain cycles," but nothing in `dispatch.py` actually honored that. This had not yet manifested only because the dispatcher had not successfully fired since the job went live (07-16 through 07-18 misses) — it would have surfaced silently the first time either the fixed 02:15 fire or the new noon fire actually landed.
- **Fix:** added a `"recurring": true` job-schema field. `finalize_job()` now checks it first — a recurring job stays in `queue/` untouched (no move, no unlink) on both success and failure, so a transient error doesn't drop it either. Set `recurring: true` on `rules/validation/queue/job_dev_set_monitor_20260715.json`. Legacy/one-shot jobs are unaffected — verified by regression test (`test_finalize_job_non_recurring_still_moves_as_before`) that the original move-and-remove behavior is byte-for-byte preserved when `recurring` is absent or false.
- **Related correctness fix:** `_scheduled_fire_time_utc()` (B-1's FIRED-delta baseline) previously assumed a single 02:15 schedule; with two fire times, that would have misreported every noon fire as ~10 hours "late." Replaced with `SCHEDULED_TIMES = [(2, 15), (12, 0)]` and logic that picks whichever slot is most recently in the past relative to the actual fire time — each fire's delta is now computed against its own nearest schedule, not a hardcoded one.
- Regression tests: `rules/validation/tests/test_dispatcher_heartbeat.py` — 34/34 pass (13 new: 3 for `finalize_job` recurring/non-recurring behavior, incl. the failure-path case; 3 for multi-slot schedule resolution, incl. a mid-morning "before either... no, between 02:15 and noon" boundary case). Full existing suite re-run clean: `test_dev_set_monitor.py` 23/23, `test_l2_procedural_defects.py` 30/30, `test_retaliation_holdings_disposition_note.py` 26/26.

### RED / open items — unchanged
- Overnight machine environment RED-strategic item: unchanged by this follow-up (that's Part A, already mitigated 07-17). This work only adds a second fire time and fixes an unrelated queue-persistence bug.
- WORK_QUEUE item 15 (D-1 daytime driver): **resolved by this fire addition**, pending Andy completing the two `launchctl` steps above.

## 2026-07-18 (session — Cowork Change Directive: Dispatcher Resilience & Overnight-Environment Forensics, Part B)

*Directive: "Cowork Change Directive — Dispatcher Resilience & Overnight-Environment Forensics," approved by Andrew M. Cohen, 2026-07-16. Trigger: the 07-16 dispatcher missed fire (later a ×3 pattern through 07-18), folded into the standing overnight-environment RED. Scope split: Part A (machine-side diagnosis: `launchctl`, `pmset -g sched`/`-g log`, sleep settings) was Andy's, executed 2026-07-17 in a separate session — found an aggressive 1-minute idle-sleep timer plus clamshell (lid-close) sleep; mitigated via `sudo pmset -c sleep 0` + a lid-open-overnight practice. Part B below is Cowork's repo-side resilience work, executed this session — none of it required the RED to be resolved first, and none of it is a diagnosis of *why* past nights failed; it's instrumentation so future nights don't require forensic guesswork.*

### GREEN — Executed autonomously (B-1, B-2, B-3)

**Dispatcher is now self-evidencing — B-1: heartbeat log**
- `main_single()` — the function launchd actually invokes nightly at 02:15 via `com.cjac.validation.plist` — now appends to a new append-only `rules/validation/logs/dispatcher_heartbeat.log` (JSONL) on every invocation: `LOADED` (proof launchd ran the process at all, written as the first statement, before any network/queue work), `FIRED` (scheduled-vs-actual delta against the 02:15 Pacific schedule — a large delta, e.g. +4h49m, IS the sleep diagnosis, since launchd coalesces a missed `StartCalendarInterval` fire onto the next wake), and exactly one terminal outcome: `IDLED-EMPTY-QUEUE`, `COMPLETED-RUN <run_id>`, or `ABORTED <reason>`. The whole body is wrapped in try/except/finally so an uncaught exception still writes `ABORTED` rather than leaving a cycle silently unresolved. This is a distinct mechanism from the existing `write_heartbeat()`/`logs/heartbeat.json` snapshot (that one is `--drain`-mode stall detection, polled every cycle, unchanged by this work).
- Ends the previous ambiguity class: a missed launchd fire, a fired-and-idled night, and a fired-and-crashed run used to be distinguishable only by the *absence* of a log line, which forced hand-reconstruction (as happened for the 07-16→07-18 misses). Now each is a distinct, directly-readable event sequence.

**Environment preflight probe — B-2**
- `_preflight_dns_probe()` resolves DNS (resolution only, no payload) for the three endpoints this repo's overnight jobs depend on — CourtListener, `generativelanguage.googleapis.com`, `api.openai.com` — on every fire, logged into the same heartbeat sequence between `FIRED` and queue evaluation. Turns every future night into a DNS data point for the overnight-environment RED at zero marginal cost, replacing the need for after-the-fact run-level forensics like run 9ae49b97's.

**Missed-fire classification — B-3**
- `classify_last_night()` reads `dispatcher_heartbeat.log` and classifies the prior overnight window into exactly one of four states: `no-heartbeat` (machine off/asleep-without-wake, or the launchd agent unloaded — launchd never ran at all), `fired-late-on-wake` (ran, but the FIRED delta exceeds a 30-minute threshold — the delta itself is the sleep diagnosis), `fired-and-idled` (ran on schedule, empty/ineligible queue), or `fired-and-ran` (ran on schedule and attempted a job). Exposed read-only via `python3 rules/validation/dispatch.py --heartbeat-status` (prints JSON) — a morning report should lead with this instead of inferring from log absence, and should raise a MISSED-FIRE banner specifically on `no-heartbeat`.
- Regression tests: `rules/validation/tests/test_dispatcher_heartbeat.py` — 21/21 pass (mock-based, no real subprocess/network). Covers the full LOADED/FIRED/PREFLIGHT_DNS/outcome sequence for idle-queue, completed-run, failed-job, and uncaught-exception paths, all four `classify_last_night()` states, most-recent-cycle-only selection (a stale earlier LOADED doesn't leak into today's classification), and the scheduled-fire-time delta baseline. Full existing suite re-run clean: `test_dev_set_monitor.py` 23/23, `test_l2_procedural_defects.py` 30/30, `test_retaliation_holdings_disposition_note.py` 26/26 — this change is additive to `main_single()`/CLI only; `drain()`, `launch_job()`, `finalize_job()`, `pick_eligible_jobs()` are unchanged.

### YELLOW — Proposed, not applied (B-4)

**launchd plist hardening — `docs/DISPATCHER_PLIST_PROPOSAL.md`**
- Drafted, NOT installed (installing launch agents / changing power settings are Andy-side actions). Recommends `AbandonProcessGroup: true` (prevents launchd cleanup from masquerading as a job failure in the new `ABORTED` classification); explicitly recommends *against* adding `KeepAlive` (wrong model — this is a scheduled job, not a daemon, and `KeepAlive` would fight `StartCalendarInterval` and the daytime-only guardrails already built into `dev_set_monitor.py`) and against flipping `RunAtLoad` to `true`; documents `sudo pmset repeat wakeorpoweron MTWRFSU 02:10:00` as a reserve option, to apply only if `--heartbeat-status` continues showing `fired-late-on-wake` nights after Part A's sleep-timer fix has had a chance to prove itself.
- Added to the overnight-environment RED-strategic item's evidence trail (below) — the plist proposal is now part of what's on record for that RED, alongside the DNS/sleep findings.

### RED — Carried, not new; evidence trail updated
1. **Overnight machine environment (RED-strategic; DNS + dispatcher-miss ×3):** Part A's diagnosis (1-min idle-sleep timer + clamshell sleep) and mitigation (`sudo pmset -c sleep 0` + lid-open) are on record as of 07-17. Evidence trail now also includes `docs/DISPATCHER_PLIST_PROPOSAL.md` (B-4, above). Resolution is no longer guesswork going forward — `python3 rules/validation/dispatch.py --heartbeat-status` gives a direct daily read on whether the fix held; check it over the next several mornings before this RED is called closed. Unblocks overnight runs + Northgate retry #3 (item 14) + automatic D-1 cadence.
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7. In progress (Andy).

## 2026-07-18 (morning report, fired on time at 8:01 AM — no-run cycle; dispatcher missed fire ×3; D-1 cadence-eligible tomorrow with no driver)

### GREEN — Executed autonomously

**Overnight scan — dispatcher missed fire #3**
- No 07-18 ~2:15 AM fire: `launchd_stdout.log` last write remains 2026-07-15 ~2:24 AM; no new dispatch log file. Third consecutive launchd-side miss (07-16, 07-17, 07-18) — sustained pattern; agent-unloaded/machine-asleep hypothesis further strengthened. Folded into the standing overnight-environment RED (checks unchanged: machine power/sleep; `launchctl list | grep com.cjac`; pmset wake schedule).
- No substantive loss: the only queued job (`job_dev_set_monitor_20260715.json`, live_verified) self-defers outside 09:00–23:00 PT. No new files in `l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (07-09). Cumulative MV=26/CI=4/RC=6 unchanged.

**Timing flag raised — D-1 cadence eligibility 2026-07-19**
- The dev-set monitor becomes cadence-eligible tomorrow (3 days after the 07-16 baseline). With the dispatcher dark AND no daytime driver (proposal 15 undecided), the run will silently not happen. Fallback for Andy: run `python3 rules/validation/scorer/dev_set_monitor.py` from Terminal during the 09:00–23:00 PT window. That run is also the convert-to-consensus opportunity for the SM-GPT baseline if Gemini capacity has recovered.

**Report-side cadence note CLOSED**
- Third consecutive clean 8 AM fire (07-16 8:00, 07-17 8:03, 07-18 8:01) — per the 07-14 criterion ("a third clean fire would justify closing it"), the report-side settings-check note is closed. Dispatcher-side checks remain open and are the live problem.

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR or SM case in the attorney lane; only failure-condition item is the dispatcher miss (infrastructure, logged, folded into RED).

**Living docs updated this cycle**
- METRICS_LEDGER (2026-07-18 cycle entry with B1–B4), PROJECT_STATE_OF_RECORD (header), HUMAN_REVIEW_QUEUE (header — no new items), WORK_QUEUE (header + Completed Today), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (step 3f).

### YELLOW — None new this cycle. Carried unratified (5): extended search backoff ladder (07-08) + FLAG-generate-failed→PR routing fix (07-06) — both live-verified 07-09; VT 4467→4465 (07-03); backoff v1 (07-05); run-57cf7b37 RC→PR reclassification (07-06). Carried YELLOW *proposal* awaiting Andy's pick: WORK_QUEUE item 15 (D-1 daytime driver) — now time-sensitive (cadence eligibility 07-19).

### RED — Carried, not new (both block progress)
1. **Overnight machine environment (RED-strategic; DNS + dispatcher-miss ×3):** dispatcher has not fired since 07-15. Checks: machine power/sleep, `launchctl list | grep com.cjac`, pmset wake schedule; DNS strand (night-window Errno-8) unchanged. Unblocks overnight runs + Northgate retry #3 (item 14) + automatic D-1 cadence.
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7.

---

## 2026-07-17 (morning report, fired on time at 8:03 AM — Direction D-1 baseline ingested; dispatcher missed fire ×2)

### GREEN — Executed autonomously

**Direction D-1 baseline run INGESTED (run executed by Andy, Terminal, 2026-07-16 18:27 PT)**
- Per the 07-15/16 session instruction, Andy ran `python3 rules/validation/scorer/dev_set_monitor.py --force` with live keys and flipped `live_verified: true` on `job_dev_set_monitor_20260715.json` (18:11 PT). Direction D-1 is now fully ACTIVE end-to-end.
- Baseline result: **dev 12/12 = 100.0%** (v0.2 dev split; all 12 expected item IDs present), `newly_failing=0`, `n_yellows=0`; `rules_sha256` matches vProof1 (`cc0cfab6…` — freeze intact) and `excel_sha256` matches the 07-01 FROZEN record. Outputs: `ca_notice_score_2026-07-16_non-held-out.json` + first `dev_set_trend.jsonl` row; the monitor self-appended its Direction D-1 ledger row (append path verified live).
- **Consensus: SM-GPT — all 12 Gemini calls failed 503 UNAVAILABLE (capacity).** Per the hard consensus gate, the baseline is PRELIMINARY, not consensus-validated, and is recorded as such everywhere. Not routed anywhere (anti-default: API failure = re-run lane). Convert-to-consensus path: re-run (or wait for the 07-19+ cadence run) once Gemini capacity recovers — same 503 class as 07-01/07-02, which cleared on its own.
- **Diagnostic value for the standing RED:** a served 503 at 18:27 PT means DNS/TCP/TLS to the Gemini endpoint SUCCEEDED from Terminal in daytime. The overnight `[Errno 8]` DNS failures are therefore a night-window-specific failure mode, distinct from Google-side capacity. Narrows Andy's diagnosis to the overnight environment (resolver/filter schedule, sleep, power).

**Overnight scan — dispatcher missed fire #2**
- No 07-17 ~2:15 AM fire: `launchd_stdout.log` last write remains 2026-07-15 ~2:24 AM; no new dispatch log file. Second consecutive launchd-side miss (07-16, 07-17) — now a pattern, strengthening the agent-unloaded/machine-asleep hypothesis. Folded into the standing overnight-environment RED (checks unchanged: machine power/sleep; `launchctl list | grep com.cjac`; pmset wake schedule).
- No substantive loss: the only queued job (dev-set monitor, now live_verified) self-defers outside 09:00–23:00 PT, so a 2:15 AM fire would have deferred anyway. No new files in `l2/output/`, `results/`, `done/`, or `failed/`.
- **Structural gap flagged (new):** the dispatcher's only fire time (2:15 AM) is ALWAYS outside the monitor's window → D-1 cadence has no automatic daytime driver. Proposal 15 added to WORK_QUEUE (YELLOW — Andy picks: second daytime launchd fire vs. morning-report drain call).

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR or SM case in the attorney lane (the 12 Gemini-503 SM items stay in the re-run lane); no other failure conditions triggered.

**Living docs updated this cycle**
- METRICS_LEDGER (2026-07-17 cycle entry with B1–B4; D-1 row was self-appended by the monitor — referenced, not duplicated), PROJECT_STATE_OF_RECORD (header + Direction D-1 section → LIVE), HUMAN_REVIEW_QUEUE (header — no new items), WORK_QUEUE (header, Completed Today, items 11/13 → DONE, proposal 15 added), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (step 3f).

### YELLOW — None new this cycle. Carried unratified (5): extended search backoff ladder (07-08) + FLAG-generate-failed→PR routing fix (07-06) — both live-verified 07-09; VT 4467→4465 (07-03); backoff v1 (07-05); run-57cf7b37 RC→PR reclassification (07-06). New YELLOW *proposal* (not executed): WORK_QUEUE item 15 (D-1 daytime driver).

### RED — Carried, not new (both block progress)
1. **Overnight machine environment (RED-strategic; DNS + dispatcher-miss ×2):** NARROWED this cycle — daytime path to Gemini confirmed fine (503 = served response); remaining question is the overnight environment only. Checks: dscacheutil day-vs-night, scutil --dns, router/filter schedules, machine power/sleep, `launchctl list | grep com.cjac`, pmset. Unblocks overnight runs + Northgate retry #3 (item 14).
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7.

---

## 2026-07-15/16 (session — Cowork Change Directive: Items 11 & 13; Items 12/14 HELD)

*Directive: "Cowork Change Directive — Approved Refill Items 11 & 13," approved by Andrew M. Cohen, 2026-07-15. Items 12 (per-call backoff extension) and 14 (Northgate retry #3) remain HELD pending the Gemini-endpoint DNS diagnosis and were NOT actioned under this directive. Session note: this work was done in a sandbox without access to the local repo clone; a separate local push (commit d068e05, "l2 validations") landed the 07-02 through 07-16 history — including the real network-retry-ladder work (2026-07-05 fix, 2026-07-08 extension) and the RC-misroute fix (2026-07-06) — while this session was in progress. Rebased Item 11 on top of that real prior work rather than duplicating it; see below.

### GREEN — Executed autonomously (Item 11)

**Harness `disposition_note` mislabel fix — search-network-failure vs. genuine no-candidates**
- Problem (as proposed in the 2026-07-08 GREEN observation, "WORK_QUEUE NEXT item 11"): the search-network-failure path recorded the same disposition note as the genuine no-CL-coverage path, conflating outages with true coverage gaps.
- On inspection, `_run_search()` already had a real network-retry ladder (2026-07-05 fix, extended 2026-07-08 to 60/120/240/600/1200/1800s, ~66 min ride-out) that correctly computes a `net_err` flag internally and prints the distinction — but that signal was never wired into the `disposition_note` actually persisted to run output. That wiring is the fix:
  - `cl_search_retaliation_by_state()` now records the final `net_err` verdict in module-level `_LAST_SEARCH_NETWORK_FAILURE[state]` (True only when the search ended in a network failure with no cases found). No change to the existing retry/backoff logic or timing.
  - `protocols/retaliation_holdings_v3.py::get_units()` tags the "no cases" sentinel unit with `search_network_failure`, read from that flag immediately after `load_draft_cases()`.
  - `run_unit()` emits `"search-network-failure: CourtListener unreachable after full backoff ladder — not a coverage determination"` when the flag is set, and the byte-identical original text `"No candidate cases in draft file for this state."` otherwise. `disposition` (`permanent-failure`), `bucket`, and `queue_routing` (`None`) are unchanged in both cases — verified by regression test, not just inspection.
  - No routing logic was touched (the separate 2026-07-06 RC→PR misroute fix for FLAG-generate-failed is a different code path — Check C generate-step routing — and was left exactly as-is). Confirmed cleanly cosmetic; did not need to escalate to YELLOW.
- Regression tests: `rules/validation/tests/test_retaliation_holdings_disposition_note.py` — 26/26 pass. Covers: full-backoff-ladder-then-flag (7 attempts, real ladder), genuine-empty-not-flagged, recovery-after-transient-errors, non-connection-exception handling (matches the runner's existing fail-fast-but-not-genuine semantics), cases-found-clears-flag, `get_units()` tagging (all cases), and `run_unit()` disposition_note text + disposition/queue_routing byte-identity for both paths plus the missing-key default.
- Full existing regression suite re-run: `test_l2_procedural_defects.py` — 30/30 pass (unaffected, unrelated module).
- **Backfill-tagging of prior run artifacts (directive item 4, optional/low-cost) — DONE, now that real artifacts are available:** confirmed exactly three runs hit the mislabeled sentinel path — `retaliation_holdings_v3_2026-07-03_c0a2df2d.json` (VT), `retaliation_holdings_v3_2026-07-04_c7bcdcff.json` (VT), and `retaliation_holdings_v3_2026-07-08_e9222548.json` (VT) — each stored `disposition_note: "No candidate cases in draft file for this state."` for what the changelog independently documents (07-03, 07-04, 07-08 entries) as DNS/NameResolutionError outages, not genuine no-CL-coverage. **Correction annotation only — the three JSON artifacts themselves were NOT modified** (per instruction; frozen historical record stays frozen): had this fix been live on those nights, all three would have read `"search-network-failure: CourtListener unreachable after full backoff ladder — not a coverage determination"` instead. The other two DNS-affected nights in the 07-03–07-09 window (57cf7b37 07-06, 9ae49b97 07-09) hit the separate FLAG-generate-failed→PR path, already corrected by the 2026-07-06 fix — not in scope for this annotation.
- Logged here for the next morning report GREEN digest.

### YELLOW — Ratified by Andy 2026-07-15 (Item 13)

**Direction D, Component 1 (Monitoring/Measurement) — built and ratified; moves from proposed to ACTIVE**
- Built `rules/validation/scorer/dev_set_monitor.py`: scheduled scorer job running `ca_notice_scorer.py` against the v0.2 FROZEN golden set with `--non-held-out-only` (the real 12-item dev split: CA-NOT-B-02, B-05–B-12, B-15–B-17, per the 2026-07-01 v0.2 FROZEN entry — verified against the actual FROZEN xlsx). Confirmed distinct from the separate v0.3 held-out DRAFT set (`goldenset_CA_notice_v0.3_DRAFT_20260702.xlsx`, created 07-02 per Broaden Proof 1) — this component never touches that file.
- Guardrails enforced in code (not just convention): dev-set-only (defense-in-depth assertion against the expected 12 IDs, hard-stops rather than silently scoring an unexpected item); read-only w.r.t. rules; daytime/evening-only self-throttle (09:00–23:00 Pacific; blocks the ~2:15 AM window that has now produced six consecutive intentionally-empty overnight cycles per the DNS RED) enforced by the script itself regardless of external scheduler timing; 3-day cadence self-throttle with an `arm_trigger()` hook wired for "run immediately after any ratified rule change" (armed manually for now — no rule change possible until v0.3 scoring completes, so it has never fired; satisfies "wire the trigger now"). Also confirmed this component's daytime runs do NOT violate the standing "overnight queue intentionally empty" hold, which applies to the overnight lane only.
- Per-run output: dev score (n/12), per-item pass/fail, `newly_failing` vs. the immediately prior run (regression = confirmed-passing → failing; new/never-scored items never flagged as regressions), α on the dev split (= model-agreement rate, this repo's existing convention), and consensus/model status. Appends to `docs/VALIDATION_METRICS_LEDGER.md` under a new "Direction D-1" section (created on first real run); pushes an alert into this changelog when `newly_failing` is non-empty.
- Dispatcher wiring: added `job_type: "scorer"` to `rules/validation/dispatch.py` (`_build_scorer_cmd`), fully additive — `protocol` and `l2_module` job types untouched. Queued `rules/validation/queue/job_dev_set_monitor_20260715.json`.
- Regression tests: `rules/validation/tests/test_dev_set_monitor.py` — 23/23 pass. Covers the `newly_failing` diff logic directly, daytime-window boundaries, the 3-day cadence boundary, and that the ledger/changelog append path fires only when `newly_failing` is non-empty and names the regressed item(s) — the regression-flag path was verified end-to-end with simulated data, not just eyeballed.
- **First baseline run: NOT executed.** This session only had placeholder API credentials, so the full pipeline was validated in `--dry-run` (guardrails, dev-set membership, ledger/changelog wiring all pass) but no real accuracy score was fabricated. The queued job has `live_verified: false` per the dispatcher's own existing gate — run `python3 rules/validation/scorer/dev_set_monitor.py --force` once from Terminal with real keys to establish the actual baseline, then flip `live_verified: true`.
- `docs/PROJECT_STATE_OF_RECORD.md` updated: Direction D-1 added under Validation Harness Status as ACTIVE (built, baseline pending live keys).
- Ratification ledger: this item moves from proposed (WORK_QUEUE NEXT item 13, per the 07-08 refill proposals) to **ratified 2026-07-15**.

### RED — None this cycle (Items 12 and 14 remain HELD per the directive; not actioned).


## 2026-07-16 (morning report, fired on time at 8:00 AM — no-run cycle with NEW anomaly: dispatcher did NOT fire overnight; queue was intentionally empty anyway; no new output)

### GREEN — Executed autonomously

**Overnight scan — nothing to ingest, but a dispatcher-side anomaly found**
- **Dispatcher did NOT fire 2026-07-16 ~2:15 AM.** Evidence: `launchd_stdout.log` last write 2026-07-15 ~2:24 AM; no "Queue is empty" line for 07-16; no new dispatch log file (`find rules/validation/logs -newermt 2026-07-15 23:00` → empty). First launchd-side missed fire since the 06-25 FDA fix — all prior cadence anomalies (07-08 double, 07-10 missed, 07-12 late, 07-15 late) were on the Cowork report side; the dispatcher had fired reliably in the 2:15–2:25 window every night.
- No substantive loss: the live queue contains only `.gitkeep` + the sample format file (Northgate retry #3 still deliberately held on the Gemini-DNS RED), so a fire would have idled (would have been the seventh consecutive intentionally-empty night).
- No new files in `rules/validation/l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (ingested 07-09). `failed/` unchanged (job_nc17_fresh_20260625 only).
- State unchanged: cumulative MV=26/CI=4/RC=6; VT 1 MV (Gokey) + 1 CI (Houle); vProof1 rule freeze intact (no rule edits).

**Cadence observation**
- Report-side: this cycle fired at 8:00 AM PDT — on time (clean fire after the 07-15 ~30-min-late fire). Settings-check note stays open.
- Dispatcher-side: MISSED FIRE (above). Checks for Andy before anything is re-queued: was the Mac off or asleep-without-wake overnight; `launchctl list | grep com.cjac` (agent still loaded?); pmset wake schedule. This overlaps the power/schedule strand of the Gemini-DNS RED — both point at the overnight machine/network environment — so it is FOLDED into that standing RED-strategic item, not opened as a separate RED.

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR or SM case in the attorney lane; no other failure conditions triggered.

**Living docs updated this cycle**
- METRICS_LEDGER (2026-07-16 no-run entry + dispatcher-miss note), PROJECT_STATE_OF_RECORD (header), HUMAN_REVIEW_QUEUE (header rebuilt — no new items), WORK_QUEUE (header + Completed Today), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (step 3f).

### YELLOW — None new this cycle. Carried unratified (5): extended search backoff ladder (07-08) + FLAG-generate-failed→PR routing fix (07-06) — both with live-verification evidence from run 9ae49b97; VT 4467→4465 (07-03); backoff v1 (07-05); run-57cf7b37 RC→PR reclassification (07-06).

### RED — Carried, not new (both block progress; queue stays idle until one resolves)
1. **Gemini-endpoint DNS diagnosis + overnight machine environment (RED-strategic, 07-09; BROADENED 07-16):** now also covers the 07-16 dispatcher missed fire — check machine power/sleep overnight and `launchctl list | grep com.cjac` alongside the DNS checks (dscacheutil day-vs-night, scutil --dns, router/filter schedules). Unblocks overnight runs + Northgate retry #3.
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7.

---

## 2026-07-15 (morning report, fired ~8:30 AM — ~30 min late — no-run cycle: sixth consecutive intentionally-empty night on the Gemini-DNS RED; no new output)

### GREEN — Executed autonomously

**Overnight scan — nothing to ingest (expected)**
- Dispatcher fired 2026-07-15 ~2:24 AM; logged "Queue is empty or no eligible jobs — nothing to do" (launchd_stdout.log). Sixth consecutive intentionally-idle night (07-10 through 07-15): Northgate retry #3 remains held pending Andy's Gemini-endpoint DNS diagnosis per the 07-09 job's escalation instruction.
- No new files in `rules/validation/l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (ingested 07-09). `failed/` unchanged (job_nc17_fresh_20260625 only). Live queue contains only `.gitkeep` + sample format file.
- State unchanged: cumulative MV=26/CI=4/RC=6; VT 1 MV (Gokey) + 1 CI (Houle); vProof1 rule freeze intact (no rule edits).

**Cadence observation (streak broken)**
- This report cycle fired ~8:30 AM PDT — ~30 minutes late. Breaks the two-clean-fire streak (07-13, 07-14); the standing settings-check note for Andy is RETAINED (it was one clean fire from closing). Mild anomaly — same class as the 07-12 late fire, milder. Dispatcher-side cadence remains normal (2:24 AM within the observed 2:15–2:25 window).

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR or SM case in the attorney lane; no other failure conditions triggered.

**Living docs updated this cycle**
- METRICS_LEDGER (2026-07-15 no-run entry + cadence note), PROJECT_STATE_OF_RECORD (header), HUMAN_REVIEW_QUEUE (header rebuilt — no new items), WORK_QUEUE (header + Completed Today), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (step 3f).

### YELLOW — None new this cycle. Carried unratified (5): extended search backoff ladder (07-08) + FLAG-generate-failed→PR routing fix (07-06) — both with live-verification evidence from run 9ae49b97; VT 4467→4465 (07-03); backoff v1 (07-05); run-57cf7b37 RC→PR reclassification (07-06).

### RED — Carried, not new (both block progress; queue stays idle until one resolves)
1. **Gemini-endpoint DNS diagnosis (RED-strategic, 07-09):** unblocks overnight runs + Northgate retry #3. Suggested checks in 07-09 entry (dscacheutil day-vs-night, scutil --dns, router/filter schedules).
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7.

---

## 2026-07-14 (8 AM morning report, fired on time at 8:01 — no-run cycle: fifth consecutive intentionally-empty night on the Gemini-DNS RED; no new output)

### GREEN — Executed autonomously

**Overnight scan — nothing to ingest (expected)**
- Dispatcher fired 2026-07-14 ~2:15 AM; logged "Queue is empty or no eligible jobs — nothing to do" (launchd_stdout.log). Fifth consecutive intentionally-idle night (07-10 through 07-14): Northgate retry #3 remains held pending Andy's Gemini-endpoint DNS diagnosis per the 07-09 job's escalation instruction.
- No new files in `rules/validation/l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (ingested 07-09). `failed/` unchanged (job_nc17_fresh_20260625 only). Live queue contains only `.gitkeep` + sample format file.
- State unchanged: cumulative MV=26/CI=4/RC=6; VT 1 MV (Gokey) + 1 CI (Houle); vProof1 rule freeze intact (no rule edits).

**Cadence observation (second clean fire)**
- This report cycle fired at 8:01 AM PDT — on schedule. Second consecutive clean fire (07-13, 07-14) after the three-anomaly stretch (07-08 double-fire, 07-10 missed, 07-12 ~3 h late). Standing settings-check note for Andy retained one more cycle; a third consecutive clean fire would justify closing it.

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR or SM case in the attorney lane; no other failure conditions triggered.

**Living docs updated this cycle**
- METRICS_LEDGER (2026-07-14 no-run entry + cadence note), PROJECT_STATE_OF_RECORD (header), HUMAN_REVIEW_QUEUE (header rebuilt — no new items), WORK_QUEUE (header + Completed Today), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (step 3f).

### YELLOW — None new this cycle. Carried unratified (5): extended search backoff ladder (07-08) + FLAG-generate-failed→PR routing fix (07-06) — both with live-verification evidence from run 9ae49b97; VT 4467→4465 (07-03); backoff v1 (07-05); run-57cf7b37 RC→PR reclassification (07-06).

### RED — Carried, not new (both block progress; queue stays idle until one resolves)
1. **Gemini-endpoint DNS diagnosis (RED-strategic, 07-09):** unblocks overnight runs + Northgate retry #3. Suggested checks in 07-09 entry (dscacheutil day-vs-night, scutil --dns, router/filter schedules).
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7.

---

## 2026-07-13 (8 AM morning report, fired on time — no-run cycle: fourth consecutive intentionally-empty night on the Gemini-DNS RED; no new output)

### GREEN — Executed autonomously

**Overnight scan — nothing to ingest (expected)**
- Dispatcher fired 2026-07-13 ~2:15 AM; logged "Queue is empty or no eligible jobs — nothing to do" (launchd_stdout.log). Fourth consecutive intentionally-idle night (07-10 through 07-13): Northgate retry #3 remains held pending Andy's Gemini-endpoint DNS diagnosis per the 07-09 job's escalation instruction.
- No new files in `rules/validation/l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (ingested 07-09). `failed/` unchanged (job_nc17_fresh_20260625 only). Live queue contains only `.gitkeep` + sample format file.
- State unchanged: cumulative MV=26/CI=4/RC=6; VT 1 MV (Gokey) + 1 CI (Houle); vProof1 rule freeze intact (no rule edits).

**Cadence observation (first clean fire)**
- This report cycle fired at 8:00 AM PDT — on schedule. First clean fire since the three-anomaly stretch (07-08 double-fire, 07-10 missed, 07-12 ~3 h late). One data point does not close the standing settings-check note for Andy; retained until a few consecutive on-time fires.

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR or SM case in the attorney lane; no other failure conditions triggered.

**Living docs updated this cycle**
- METRICS_LEDGER (2026-07-13 no-run entry + cadence note), PROJECT_STATE_OF_RECORD (header), HUMAN_REVIEW_QUEUE (header rebuilt — no new items), WORK_QUEUE (header + Completed Today), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (step 3f).

### YELLOW — None new this cycle. Carried unratified (5): extended search backoff ladder (07-08) + FLAG-generate-failed→PR routing fix (07-06) — both with live-verification evidence from run 9ae49b97; VT 4467→4465 (07-03); backoff v1 (07-05); run-57cf7b37 RC→PR reclassification (07-06).

### RED — Carried, not new (both block progress; queue stays idle until one resolves)
1. **Gemini-endpoint DNS diagnosis (RED-strategic, 07-09):** unblocks overnight runs + Northgate retry #3. Suggested checks in 07-09 entry (dscacheutil day-vs-night, scutil --dns, router/filter schedules).
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7.

---

## 2026-07-12 (morning report, fired ~11 AM — no-run cycle: third consecutive intentionally-empty night on the Gemini-DNS RED; no new output)

### GREEN — Executed autonomously

**Overnight scan — nothing to ingest (expected)**
- Dispatcher fired 2026-07-12 ~2:15 AM; logged "Queue is empty or no eligible jobs — nothing to do" (launchd_stdout.log). Third consecutive intentionally-idle night (07-10, 07-11, 07-12): Northgate retry #3 remains held pending Andy's Gemini-endpoint DNS diagnosis per the 07-09 job's escalation instruction.
- No new files in `rules/validation/l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (ingested 07-09). `failed/` unchanged (job_nc17_fresh_20260625 only). Live queue contains only `.gitkeep` + sample format file.
- State unchanged: cumulative MV=26/CI=4/RC=6; VT 1 MV (Gokey) + 1 CI (Houle); vProof1 rule freeze intact (no rule edits).

**Cadence observation (third data point)**
- This report cycle fired ~11:00 AM PDT instead of 8 AM. Combined with the 07-08 double-fire and the 07-10 missed cycle, the scheduled-task cadence is now unstable in three distinct ways (double, missing, late). No substantive loss this time (no overnight output existed), but the standing note to Andy is upgraded: worth checking the Cowork scheduled-task settings before the next live overnight run, so ingestion doesn't lag a real result.

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR or SM case in the attorney lane; no other failure conditions triggered.

**Living docs updated this cycle**
- METRICS_LEDGER (2026-07-12 no-run entry + cadence note), PROJECT_STATE_OF_RECORD (header), HUMAN_REVIEW_QUEUE (header rebuilt — no new items), WORK_QUEUE (header + Completed Today), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (step 3f).

### YELLOW — None new this cycle. Carried unratified (5): extended search backoff ladder (07-08) + FLAG-generate-failed→PR routing fix (07-06) — both with live-verification evidence from run 9ae49b97; VT 4467→4465 (07-03); backoff v1 (07-05); run-57cf7b37 RC→PR reclassification (07-06).

### RED — Carried, not new (both block progress; queue stays idle until one resolves)
1. **Gemini-endpoint DNS diagnosis (RED-strategic, 07-09):** unblocks overnight runs + Northgate retry #3. Suggested checks in 07-09 entry (dscacheutil day-vs-night, scutil --dns, router/filter schedules).
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7.

---

## 2026-07-11 (8 AM morning report — no-run cycle: queue intentionally empty on the Gemini-DNS RED; no new output; 07-10 report cycle missing)

### GREEN — Executed autonomously

**Overnight scan — nothing to ingest (expected)**
- Dispatcher fired 2026-07-10 and 2026-07-11 ~2:15 AM; both nights logged "Queue is empty or no eligible jobs — nothing to do" (launchd_stdout.log). This is the intended state: Northgate retry #3 is held pending Andy's Gemini-endpoint DNS diagnosis per the 07-09 job's own escalation instruction.
- No new files in `rules/validation/l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (ingested 07-09). `failed/` unchanged (job_nc17_fresh_20260625 only).
- State unchanged: cumulative MV=26/CI=4/RC=6; VT 1 MV (Gokey) + 1 CI (Houle); vProof1 rule freeze intact (no rule edits).

**Process gap logged — missing 2026-07-10 cycle**
- No 07-10 entry exists in this changelog or METRICS_LEDGER — the scheduled morning report appears not to have fired (or fired without logging) on 07-10. Failure condition acknowledged. No substantive loss: no overnight output existed that day. Gap recorded in METRICS_LEDGER per honesty discipline. Note for Andy: combined with the 07-08 duplicate fire, scheduled-task cadence looks unstable in both directions — worth a settings check.

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR or SM case in the attorney lane; no other failure conditions triggered.

**Living docs updated this cycle**
- METRICS_LEDGER (2026-07-11 no-run entry + missed-cycle note), PROJECT_STATE_OF_RECORD (header), HUMAN_REVIEW_QUEUE (header rebuilt — no new items), WORK_QUEUE (header + Completed Today), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (step 3f).

### YELLOW — None new this cycle. Carried unratified (5): extended search backoff ladder (07-08) + FLAG-generate-failed→PR routing fix (07-06) — both with live-verification evidence from run 9ae49b97; VT 4467→4465 (07-03); backoff v1 (07-05); run-57cf7b37 RC→PR reclassification (07-06).

### RED — Carried, not new (both block progress; queue stays idle until one resolves)
1. **Gemini-endpoint DNS diagnosis (RED-strategic, 07-09):** unblocks overnight runs + Northgate retry #3. Suggested checks in 07-09 entry (dscacheutil day-vs-night, scutil --dns, router/filter schedules).
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7.

---

## 2026-07-09 (8 AM morning report — Northgate retry #2: selective Gemini-endpoint DNS failure; all 5 units PR; two YELLOW fixes live-verified; retry #3 held for Andy)

### GREEN — Executed autonomously

**Overnight run 9ae49b97 ingested — VT Northgate generate retry #2**
- Job `job_vt_northgate_generate_retry2_20260708` → done/ at 2026-07-09 15:38 UTC, returncode=0. 5 units, elapsed 343.4 min. Summary: `SUMMARY_retaliation_holdings_v3_2026-07-09_1538.md`; raw: `retaliation_holdings_v3_2026-07-09_9ae49b97.json`; PR list: `retaliation_holdings_v3_PR_9ae49b97.json`.
- Result: **all 5 VT units → PR (`generate-api-failure-transient`)**. Checks A (existence) and B (currency) succeeded via CourtListener for all 5 cases across the entire run; every Check C Gemini generate call failed DNS getaddrinfo `[Errno 8]` for ~5.7 h. Method rate n/a (0÷0); overall 0/5 = 0% (retrieval/generate-gated, two-rate rule); α n/a (no dual-model pairs). Cumulative MV=26/CI=4/RC=6 unchanged. VT case statuses unchanged (Gokey MV, Houle CI [VT-HOLD-CI-01], Atwood/Vladyka wrong-doc CLOSED, Northgate PR).

**Live verification of two pending YELLOW fixes (evidence for ratification)**
- Extended search backoff ladder (07-08 YELLOW): first CL search attempt DNS-failed; 60s retry succeeded; statute query returned 5 in-state candidates; Check E rejected 2 wrong-jurisdiction hits. **Worked as designed.**
- FLAG-generate-failed→PR routing fix (07-06 YELLOW): **first live exercise — PASSED.** 5/5 generate failures routed PR; zero RC artifacts (contrast pre-fix run 57cf7b37); nothing routed to attorney.

**GREEN diagnosis — DNS failure is selective; machine-sleep hypothesis weakened**
- No wall-clock anomaly this run (dispatch → harness start 35 min = search retry ladder; continuous per-case progress 23:54→05:38 local). CL API resolved and answered at every hour of the night (one transient CL error on case 3 recovered on retry) while the Gemini hostname failed persistently on the same machine/process. Conclusion: not lid-close sleep, not a CL outage — a local resolver/filter issue specific to the Google API endpoint at night. RED-strategic reframed accordingly (see RED).

**Queue management**
- Overnight queue intentionally left empty: per the job's own instruction ("if DNS again, escalate rather than extend backoff further"), Northgate retry #3 is held pending Andy's decision. Proposed as WORK_QUEUE NEXT item 14, gated on the RED. NEXT refill proposals 11–13 carried; item 12 (per-call backoff) annotated as complementary-not-sufficient given tonight's 5.7 h persistence.

**Living docs updated this cycle**
- METRICS_LEDGER (run 9ae49b97 entry, two rates + bucket counts + PR quarantine=5), PROJECT_STATE_OF_RECORD (header + holdings section), HUMAN_REVIEW_QUEUE (audited — no new items; 0 RC, 0 MODEL-SPLIT; PR never enters attorney lane), WORK_QUEUE (header, item 4, Completed Today, NEXT 12/14), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated.

### YELLOW — None new this cycle. Carried unratified: ladder extension (07-08), RC-misroute fix (07-06), VT 4467→4465 (07-03), backoff v1 (07-05), run-57cf7b37 RC→PR reclassification — the first two now carry live-verification evidence (above).

### RED — Escalated, not decided by Cowork

**RED-strategic (reframed) — nightly DNS failure is selective to the Gemini endpoint**
- Five DNS-affected nights since 07-03; tonight's evidence isolates the failure: CourtListener resolved fine all night, Gemini hostname failed for ~5.7 h, machine demonstrably awake and processing.
- For Andy (his machine, his call): check router/DNS filtering or profiles that could block/fail `generativelanguage.googleapis.com` at night (Pi-hole/NextDNS schedules, VPN toggles, Screen Time/content filters); compare `dscacheutil -q host -a name generativelanguage.googleapis.com` day vs. ~2–5 AM; check `scutil --dns` resolver config. Power-settings question (07-08) demoted but not closed — the 07-07 wall-clock gap remains unexplained.
- Northgate retry #3 queued only after this is resolved.

---

## 2026-07-08 (late-day audit cycle — duplicate scheduled fire; no new overnight output; consistency audit PASSED)

### GREEN — Executed autonomously

**Audit cycle (scheduled task fired a second time on 2026-07-08)**
- Scanned `rules/validation/l2/output/`, `results/`, `queue/`, `done/`, `failed/`, and logs: **no new files since the 8 AM cycle.** The only output in the last 48 h is run e9222548 (already ingested at 8 AM). `failed/` unchanged (job_nc17_fresh_20260625 only).
- Queue state verified: `job_vt_northgate_generate_retry2_20260708.json` is the sole live job — validated JSON, fires 2026-07-09 2:15 AM (retries Northgate; live-exercises the FLAG-generate-failed→PR routing fix and the extended 60/120/240/600/1200/1800s ladder).
- Living-doc consistency audit PASSED: METRICS_LEDGER (e9222548 entry present, N/A rates with rationale), PROJECT_STATE_OF_RECORD, HUMAN_REVIEW_QUEUE (header rebuilt 07-08; no new items; RC=6, CI=2), WORK_QUEUE (last-updated 07-08; NEXT refills 11–13 proposed), CLAUDE_CHAT_BRIEF (generated 07-08, derives from current canonicals) — all mutually consistent. No stale-doc process miss this time.
- Anti-default audit: **0 cases routed RED-attorney this cycle** (and 0 at the 8 AM cycle). No PR or SM case in the attorney lane. No failure conditions triggered.
- No ingestion, no rule changes, no metrics changes — cumulative MV=26, CI=4, RC=6 unchanged. CLAUDE_CHAT_BRIEF confirmed current (step 3f satisfied by audit; content unchanged, timestamp annotated).
- Note for Andy: two morning-report fires on the same calendar day — worth checking the Cowork scheduled-task cadence/timezone if this recurs (GREEN observation, no change made).

### YELLOW — None this cycle (audit only; 8 AM YELLOWs carry unratified).

### RED — None new. Carried: overnight-run power/schedule (machine-sleep hypothesis); v0.3 held-out freeze (28 items, Step 4).

---

## 2026-07-08 (8 AM morning report — Northgate retry DNS failure #4; backoff ladder extended; machine-sleep hypothesis flagged)

### GREEN — Executed autonomously

**Overnight run e9222548 ingested — VT Northgate generate retry (GREEN)**
- Job `job_vt_northgate_generate_retry_20260706` (dispatched 2026-07-07 2:16 AM PT) → done/ at 2026-07-08 03:11 UTC, returncode=0.
- **Infrastructure failure, fourth DNS-affected night since 07-03:** DNS NameResolutionError to www.courtlistener.com on ALL 5 attempts of BOTH queries (4465 statute + broad fallback) — the 2026-07-05 backoff ladder (60/120/180/240s, ~10 min/query) worked as designed but was outlasted. Runner correctly labeled it "PR-class infrastructure failure, NOT a genuine no-CL state."
- 0 candidates → `VT::__no_cases__` permanent-failure, queue_routing=None. **Anti-default upheld — nothing routed to attorney.** No validation rate logged (harness 0/1=0% is a DNS artifact; N/A per two-rate honesty rules). No model calls → α N/A.
- Consequences: Northgate's generate never retried; the 2026-07-06 FLAG-generate-failed→PR routing fix remains live-unexercised. VT status unchanged (1 MV Gokey + 1 CI Houle). Cumulative MV=26/CI=4/RC=6.

**Wall-clock anomaly diagnosed → machine-sleep hypothesis (GREEN diagnosis; decision flagged RED-strategic)**
- Dispatch 2:16 AM PT; harness unit-processing timestamps 5:11 PM PT — ~15 h gap that ~20 min of retry sleep cannot explain. Hypothesis: the Mac sleeps mid-run despite `caffeinate -ims` (lid-close sleep overrides caffeinate; network down in dark-wake), which would also explain the recurring "2:15 AM DNS window" across c0a2df2d/c7bcdcff/57cf7b37/e9222548. Power/schedule settings are Andy's machine — flagged as RED-strategic decision, not changed autonomously.

**Queue refilled (GREEN)**
- Queue was EMPTY. `job_vt_northgate_generate_retry2_20260708.json` created (VT, fresh=true; retries Northgate; live-exercises both the routing fix and the new extended ladder). JSON validated. Fires 2026-07-09 2:15 AM.

**GREEN observation (candidate fix, proposed to NEXT, not applied)**
- Harness `disposition_note` for the search-network-failure path still reads "No candidate cases in draft file for this state" — cosmetic mislabel (routing unaffected). Proposed as WORK_QUEUE NEXT item 11.

**Living docs updated (GREEN)**
- METRICS_LEDGER: 2026-07-08 cycle entry (N/A rates with rationale, diagnosis chain, actions; note that no 07-07 cycle entry exists — job was in flight). PROJECT_STATE_OF_RECORD: header + VT section. HUMAN_REVIEW_QUEUE: header rebuilt, **no new items**. WORK_QUEUE: header, NEXT item 4 residual note, Completed Today, 3 proposed NEXT refills (items 11–13). CLAUDE_CHAT_BRIEF regenerated (step 3f). This changelog entry.

### YELLOW — For ratification
1. **Network-retry ladder extension** in `rules/validation/l2/retaliation_holdings_v3_runner.py` `_run_search`: 60/120/180/240s (~10 min/query) → 60/120/240/600/1200/1800s (~66 min/query). Justification: run e9222548 exhausted the old ladder on both queries. Reversible (restore old ladder). py_compile clean; 30/30 regression tests pass. Caveat noted in code: if the machine-sleep hypothesis is right, longer backoff only helps while the process is actually running.
- *(Carried, unratified: 4467→4465 VT statute config [07-03]; RC-misroute fix [07-06]; search backoff v1 [07-05]; run-57cf7b37 RC→PR ingestion reclassification [07-06].)*

### RED — Decisions needed
- **RED-strategic (NEW): overnight-run power/schedule.** Evidence suggests the Mac sleeps mid-run and/or has no network at the 2:15 AM window (4 DNS-affected nights; 15-h wall-clock gap in e9222548). Options: (a) keep the machine on AC with lid open / display-off; (b) `sudo pmset repeat wakeorpoweron` a few minutes before dispatch; (c) move the launchd dispatch to a time the machine is reliably awake (e.g., 7:30 AM before the 8 AM report, or overnight only when docked). Cowork cannot change launchd/pmset (outside repo); needs Andy's terminal.
- Carried, not new: **v0.3 held-out freeze — 28 draft items waiting on Andy** (Broaden Proof 1 Step 4; blocks Steps 5–7).

---

## 2026-07-06 (8 AM morning report — VT Gokey → MV ✅; RC-misroute bug fixed; 07-04/07-05 backfill)

### GREEN — Executed autonomously

**Overnight run 57cf7b37 ingested — VT Gokey retry2, 2026-07-06 13:03 UTC (GREEN)**
- Job `job_vt_gokey_retry2_20260705` → done/ at 13:03 UTC. 5 VT units, 162.5 min.
- **The 2026-07-05 DNS-retry backoff fix WORKED:** first statute query hit NameResolutionError at 00:20, retried on 60s backoff, succeeded → 5 in-state candidates (Check E rejected 2 wrong-jurisdiction hits).
- **🎯 Gokey v. Bessette, 154 Vt. 560, 580 A.2d 488 (Vt. 1990) → MV.** A=true (cluster 1539041, citation match); B=OK-machine (13 citing, no negative treatment); C=corroborated (Gemini generate → GPT-4o verify, agree); D=STATED — verbatim §4465 burden-shifting controlling quote. Below attorney line. Written to `vt_eviction_v2.json` machine_verified_cases; candidate → MV; validation_status → GOKEY-MV-COMPLETE. Cumulative MV=26.
- Vladyka v. Marsh → PR wrong-doc CLOSED (habitability case, Gemini high-confidence not-retaliation). Atwood re-encountered, re-confirmed wrong-doc, no change.

**Anti-default enforcement AGAINST the harness — 2 RC reclassified PR (GREEN ingestion + YELLOW code fix)**
- Run 57cf7b37 emitted RC for Houle v. Quenneville and Northgate Hous. v. White. Both `check_c.generate_output.error = "[Errno 8] nodename nor servname provided"` — the per-case Gemini generate call failed on DNS mid-run. **No legal evaluation occurred. These are PR-class infrastructure failures, not attorney items.**
- Reclassified PR on ingestion (Northgate → generate retry lane; Houle → disregarded, already CI [VT-HOLD-CI-01], CI status unchanged). NOT added to HUMAN_REVIEW_QUEUE. RC count remains 6.
- Root cause: `protocols/retaliation_holdings_v3.py` routed `FLAG-generate-failed` to RC ("generate API failure" branch) — structural anti-default violation. **Fixed:** FLAG-generate-failed now routes PR with `pr_reason=generate-api-failure-transient`; added to `is_pr` detection. *Verified: py_compile clean; 30/30 regression tests pass.* (YELLOW — see below.)
- Corrected run buckets: MV=1, CI=0, RC=0, PR=4, SM=0. Corrected method rate 1/1 (n=1, statistically meaningless); overall 1/5. Harness-reported 1/3=33% method rate is contaminated — do not cite.

**Backfill — 07-04/07-05 cycle actions that were never logged (process miss, GREEN-fixed)**
- Run c7bcdcff (2026-07-04): second consecutive DNS failure at ~2:25 AM PT, both queries; 4465 fix never exercised; no validation rate logged (N/A per two-rate honesty rules). Now in METRICS_LEDGER.
- 2026-07-05 fix (was unlogged): `_run_search` network-error retry with 60/120/180/240s backoff in `retaliation_holdings_v3_runner.py`; error paths no longer mislabeled "genuine no-CL state" (YELLOW, listed below). `job_vt_gokey_retry2_20260705` queued.
- **Failure conditions acknowledged for 07-04/07-05 cycles:** GREEN actions with no changelog entry; CLAUDE_CHAT_BRIEF not regenerated (stale since 07-03); METRICS_LEDGER/STATE_OF_RECORD not updated. All backfilled this cycle.

**Queue refilled (GREEN)**
- Queue was EMPTY. `job_vt_northgate_generate_retry_20260706.json` created (VT, fresh=true; retries Northgate's failed generate; live-exercises the routing fix — any repeat network failure must land PR, never RC). JSON validated. Fires 2026-07-07 2:15 AM.

**Living docs updated (GREEN)**
- METRICS_LEDGER: 2026-07-06 cycle entry (both runs, corrected buckets, α note, cumulative MV=26). PROJECT_STATE_OF_RECORD: header + VT section + cumulative counters. HUMAN_REVIEW_QUEUE: header rebuilt, **no new items**. WORK_QUEUE: header, NEXT item 4 closed (VT complete), Completed Today. CLAUDE_CHAT_BRIEF regenerated (step 3f). This changelog entry.

### YELLOW — For ratification
1. **RC-misroute fix** in `rules/validation/protocols/retaliation_holdings_v3.py`: `FLAG-generate-failed` → PR (`generate-api-failure-transient`) instead of RC. Changes bucket routing (affects future method-rate denominators — makes them cleaner). Revert = restore `"RC"` branch. Compile + 30/30 tests pass.
2. **Network-retry backoff (applied 2026-07-05, logged now):** `_run_search` in `rules/validation/l2/retaliation_holdings_v3_runner.py` retries ConnectionError/Timeout with 60/120/180/240s backoff. Proven live in run 57cf7b37. Revert = remove retry loop.
3. **Ingestion reclassification of run 57cf7b37's 2 RC → PR** (documented in METRICS_LEDGER; raw output JSON untouched). Reversible by re-reading the raw file.
- *(Carried, unratified: VT statute config 4467→4465 from 2026-07-03.)*

### RED — None new this cycle
- Carried, not new: **v0.3 held-out freeze — 28 draft items waiting on Andy** (Broaden Proof 1 Step 4; blocks Steps 5–7).
- Noted for Andy (not blocking): per-case model API calls have no network backoff (the 07-05 fix covers CL search only) — if Northgate's retry hits DNS again, proposal is to extend backoff to generate/verify calls (would be YELLOW).

---

## 2026-07-03 (8 AM morning report — VT Gokey run failed on DNS; config fix + re-queue)

### GREEN — Executed autonomously

**Overnight VT Gokey run ingested — run_id=c0a2df2d, 2026-07-03 09:17 UTC (GREEN)**
- Job: `job_vt_gokey_20260702.json` → moved to `done/` at 09:17 UTC; returncode=0 but run produced 0 candidates.
- **Root cause: infrastructure.** DNS resolution to `www.courtlistener.com` failed (`NameResolutionError`) on both the VT statute query and the broad fallback at 2:17 AM PT — network/DNS unavailable on the machine at dispatch time. Retrieval never occurred; Gokey (CL cluster 1539041) was never fetched. Harness recorded `VT::__no_cases__` → permanent-failure.
- **No validation rate logged** — the harness's 0/1=0% overall rate is a DNS artifact, not a verified miss. Recorded as N/A in METRICS_LEDGER per two-rate honesty rules.
- Anti-default rule upheld: nothing routed to attorney. Cumulative counters unchanged (MV=25, CI=4, RC=6).

**Secondary pipeline findings from diagnosis (GREEN diagnosis; one YELLOW fix)**
- `_STATE_RETALIATION_STATUTES["VT"]` was `"4467"` — 9 V.S.A. §4467 is the termination-of-tenancy notice statute, not retaliation (§4465). The 2026-07-02 CourtListener MCP search that identified Gokey used "4465" and returned exactly the right two cases (Houle + Gokey). **Fixed 4467→4465** in `retaliation_holdings_v3_runner.py` (YELLOW — see below). Runner compiles clean (`py_compile` pass).
- Job fields `target_cluster_id`/`target_case` are NOT consumed: `dispatch.py` passes only `--states`/`--fresh`; the runner has no targeted-cluster mode. With the 4465 fix, the statute-targeted query should return Gokey directly. Targeted-cluster mode noted as a possible future enhancement — proposed only, not built.

**Re-queue (GREEN)**
- `rules/validation/queue/job_vt_gokey_retry_20260703.json` created (retaliation_holdings_v3, VT, fresh=true, sleep=20; prior_run_id=c0a2df2d, failure mode documented). JSON validated. Queue was otherwise empty — tonight's 2:15 AM dispatch now has work.

**Living docs updated (GREEN)**
- METRICS_LEDGER: 2026-07-03 cycle entry added (run c0a2df2d, N/A rates with rationale, root-cause chain, actions).
- PROJECT_STATE_OF_RECORD: header + VT holdings section updated.
- WORK_QUEUE: header, NEXT item 4, Completed Today updated.
- HUMAN_REVIEW_QUEUE: no new items (correct — nothing interpretive this cycle).
- CLAUDE_CHAT_BRIEF regenerated (step 3f).
- This changelog entry.

### YELLOW — For ratification
- **VT statute-query config fix (4467→4465)** in `rules/validation/l2/retaliation_holdings_v3_runner.py` `_STATE_RETALIATION_STATUTES`. One-token, reversible, source-anchored (9 V.S.A. §4465 = retaliation; corroborated by the 2026-07-02 MCP search evidence recorded in WORK_QUEUE/METRICS_LEDGER). Affects only the VT CL search query. Revert = change back to "4467".

### RED — None new this cycle. (Carried, not new: v0.3 held-out freeze — 28 draft items waiting on Andy.)

---

## 2026-07-02 (Broaden Proof 1 direction received — rules frozen, v0.3 draft CREATED)

### GREEN — Executed autonomously

**Broaden Proof 1 direction ingested + executed (GREEN)**

*Direction doc:* `docs/COWORK_DIRECTION_BROADENPROOF1_20260702.md`

**Step 0 — B3 gate: ✅ PASSED (3 confirmations)**
- 12/12 = 100.0% DUAL-MODEL-CONSENSUS (agree=12, disagree=0, errors=0), confirmed three runs on 2026-07-02.

**Step 1 — CA-notice rules FROZEN as vProof1:**
- File: `rules/eviction/california/ca_eviction_v2.json`
- SHA256 (vProof1): `cc0cfab63ae1591e2b88353c557aeb8027767d99276a3115b5ce9f4115599b93`
- State: post REVISED-8 + REVISED-9; 9 self-critique corrections from 2026-07-01
- **No rule edits permitted until after v0.3 held-out score is logged.**

**Step 3 — v0.3 held-out DRAFT created (28 candidates):**
- File: `rules/validation/scorer/FROZEN/goldenset_CA_notice_v0.3_DRAFT_20260702.xlsx`
- SHA256 (at-creation): `5f2c25c15b34bb7b209a6bd7900e9f4804063340e39fed481779984dc0489e0d`
- 28 candidates; all Status=DRAFT; all Held-out=TRUE; v0.2 items NOT reused
- Outcome distribution (DRAFT): NOTICE_VALID=15, NOTICE_INVALID=12, UD_DEFECTIVE_PREMATURE=1
- Coverage: pay-or-quit (counts, amounts, content), cure-or-quit (§1161(3)), unconditional quit (§1161(4)), AB 1482/§1946.2, service methods (CCP §1162), multi-defect, edge cases
- Sources: CCP §1161/§1162/§1946.2; BG31 (2015, authority cross-checked against current statute per Discipline A); SB 611 (eff. 2/1/2025); AB 1482; case law per item
- Independence: all 28 are genuinely new — NOT paraphrases of v0.2 items
- B4 currency: BG31 is 2015; each item's authority cross-checked against current CA statute; SB 611 and AB 1482 amendments incorporated in relevant items

**Living docs updated (GREEN):**
- METRICS_LEDGER: vProof1 freeze record added; v0.3 draft row added to repeatability view
- WORK_QUEUE: Broaden Proof 1 sequence added to NOW
- Direction doc saved: `docs/COWORK_DIRECTION_BROADENPROOF1_20260702.md`

**BLOCKED — waiting on Andy:** Step 4 (Andy reviews + freezes 28 draft items) must come before Steps 5-6 (score + report). No rule edits in the interim.

### YELLOW — None new.

### RED — None new.

---

## 2026-07-02 (8 AM morning report cycle — audit + Atwood resolution + queue refill)

### GREEN — Executed autonomously

**Overnight-ingestion audit (GREEN)**
- Verified run 1153a763 (VT retry) fully ingested and consistent across METRICS_LEDGER, HUMAN_REVIEW_QUEUE, PROJECT_STATE_OF_RECORD, WORK_QUEUE (all updated in the pre-8AM session). No un-ingested output files found. failed/ unchanged. No new attorney items required.

**Atwood VT wrong-doc GREEN investigation — RESOLVED (GREEN)**
- CourtListener MCP search (`retaliatory eviction "4465"`, court=vt, opinions) returned exactly 2 results: Houle v. Quenneville (already CI) and **Gokey v. Bessette, 154 Vt. 560, 580 A.2d 488 (Vt. 1990)** — the foundational VT retaliatory eviction case (the "Gokey standard" referenced in Houle's proposed holding). Published, cited 17×, CL cluster 1539041.
- `rules/eviction/vermont/vt_eviction_v2.json` updated: Gokey added to holdings.candidates (UNVERIFIED, identified_by=courtlistener_mcp_search); Houle candidate_status → CI with confirm_inference_cases entry (run 1153a763, [VT-HOLD-CI-01]); Atwood recorded in pr_cases as wrong-doc CLOSED; holdings.validation_status → RUN-COMPLETE. JSON validated.
- Anti-default rule upheld: Atwood never touched the attorney lane; wrong-doc PR resolved by pipeline investigation as designed.

**Overnight queue refilled — tonight's job queued (GREEN)**
- Queue was EMPTY at 8 AM (tonight's 2:15 AM dispatch would have idled). `rules/validation/queue/job_vt_gokey_20260702.json` created: retaliation_holdings_v3, states=VT, fresh=true, sleep=20, target Gokey cluster 1539041. JSON validated.

**Krippendorff's α added for v0.2 scorer runs (GREEN)**
- Computed from per-item model predictions in the score JSONs (nominal, 2 raters, no missing data): held-out α=0.667 (n=5, D_o=0.200, D_e=0.600); dev α=0.867 (n=12, D_o=0.083, D_e=0.627); combined agreement stat α=0.806 (n=17; scores themselves never blended). Both disagreements are Gemini-UNCERTAIN (appropriate caution), not confident splits. Added to METRICS_LEDGER v0.2 block with small-n caveat.

**Living docs updated (GREEN)**
- METRICS_LEDGER: α block + 8 AM audit addendum. PROJECT_STATE_OF_RECORD: VT Gokey resolution. WORK_QUEUE: Atwood item resolved, queue-refill logged, NEXT item 4 closed. CLAUDE_CHAT_BRIEF regenerated (was stale from 2026-07-01 — flagged as process miss, fixed this cycle). This changelog entry.

### YELLOW — None new this cycle.

### RED — None new this cycle. (B3 regression check and CI confirms remain with Andy — carried, not new.)

---

## 2026-07-02 (morning report — VT retry overnight ingested; Gemini 503 CLEARED; scorer unblocked)

### GREEN — Executed autonomously

**VT retry overnight run ingested — run_id=1153a763, 2026-07-02 02:16 UTC (GREEN)**
- Job: `job_vt_retry_gemini_restored_20260701.json` → moved to `done/` at 02:16 UTC; returncode=0
- Summary file: `rules/validation/results/SUMMARY_retaliation_holdings_v3_2026-07-02_0916.md`
- Raw output: `rules/validation/l2/output/retaliation_holdings_v3_2026-07-02_1153a763.json`
- **GEMINI 503 CLEARED:** Both VT cases received Gemini 2.5-pro responses (no 429/503 errors). Andy's credit top-up worked.
- **Atwood v. Hill (VT)** → **PR** — reason: `case-not-relevant-to-retaliation-likely-wrong-doc`. Gemini (high confidence): this case is about damages, back rent, security deposit — not retaliation. CL cluster_id=10145325 is the wrong document. GREEN pipeline investigation item (not attorney lane — wrong doc, not legal failure).
- **Houle v. Quenneville (VT)** → **CI** — two-model corroborated, D=INFERRED. Gemini generated, GPT-4o verified as "accurate". Holding: tenants failed to prove retaliatory eviction; initial eviction attempt may have been retaliatory, but subsequent non-renewal was based on lease expiration + repairs completed (not prior violations). No verbatim controlling quote extracted — routes to cheap confirm lane.
- Bucket counts: MV=0, CI=1, RC=0, PR=1, SM=0. Method rate: 0/1=0%. Overall rate: 0/2=0%. (Houle CI is below the attorney line — not machine-verified.)
- Added VT-HOLD-CI-01 (Houle v. Quenneville) to HUMAN_REVIEW_QUEUE (cheap confirm lane)

**Stage 2 scorer UNBLOCKED — Gemini working (GREEN)**
- BLOCKED item "All Gemini-dependent overnight runs" removed from WORK_QUEUE BLOCKED list (Gemini 503 capacity issue resolved)
- Stage 2 dual-model scorer run moved to NOW in WORK_QUEUE
- Atwood VT wrong-doc GREEN investigation added to NEXT

**v0.2 held-out score BURNED — 5/5 = 100.0% DUAL-MODEL-CONSENSUS (GREEN)**
- Run: `ca_notice_score_2026-07-02_held-out.json`; scorer v2.0-excel-native; run_date=2026-07-02
- Consensus status: DUAL-MODEL-CONSENSUS (both models answered on all 5 items)
- Score: **5/5 = 100.0%** (small-sample result, n=5; 95% CI: [47.8%, 100%]; directional signal only)
- Model agreement: agree=4, disagree=1 (CA-NOT-B-18: Gemini UNCERTAIN on owner-occupied duplex inception condition; GPT correct; ground truth NOTICE_VALID confirmed by Andy)
- B2 (confident-wrong): 0. No high-confidence wrong predictions.
- 🟡 YELLOW flag — CA-NOT-B-18: Gemini legitimately flagged that §1946.2(e)(7) requires owner occupancy at inception of tenancy; scenario doesn't state this explicitly. Ground truth resolves as NOTICE_VALID. Scenario-quality note; no rules encoding change required.
- Held-out set PERMANENTLY BURNED — these 5 items cannot be re-scored against a tuned model
- METRICS_LEDGER updated with full B1–B4 report + per-item table
- Dev set (12 items) run pending — awaiting Andy's terminal run of `--non-held-out-only`

**v0.2 dev set scored — 10/12 = 83.3% DUAL-MODEL-CONSENSUS (GREEN)**
- Run: `ca_notice_score_2026-07-02_non-held-out.json`; 12 items; agree=11, disagree=1
- Score: **10/12 = 83.3%**; B2: confident-wrong=2 (B-02 and B-09 — both encoding issues)
- **Miss 1 — CA-NOT-B-02** (NOTICE_INVALID missed as NOTICE_VALID; DISAGREE): Encoding GAP. CCP §1161(2): when rent payable in person, notice MUST state "usual days and hours" when landlord is available; omission is fatal. The encoding has name/phone/address but not days_hours_for_in_person_payment. GPT HIGH confident wrong; Gemini correctly flagged UNCERTAIN. B2 severity: medium (split models).
- **Miss 2 — CA-NOT-B-09** (NOTICE_INVALID missed as NOTICE_VALID; AGREE): Encoding ERROR. Unauthorized subletting classified as §1161(4) incurable conduct (unconditional quit). WRONG: per CCP §1161(3), subletting is a curable lease covenant breach; tenant has statutory right to remove subtenant within 3 days. §1161(4) covers nuisance/waste/unlawful use — subletting is NOT listed. Both models HIGH confident wrong. B2 severity: HIGH (both-model AGREE, both HIGH confidence, both wrong). GREEN encoding fix required.
- Encoding fixes queued: (1) Add §1161(2) days_hours_for_in_person_payment to mandatory content; (2) Move unauthorized subletting from §1161(4) to §1161(3) curable category.
- METRICS_LEDGER updated with full B1–B4 analysis, per-item miss triage, and combined v0.2 summary.

**Living docs updated (GREEN)**
- HUMAN_REVIEW_QUEUE: VT-HOLD-CI-01 added (Houle v. Quenneville CI)
- VALIDATION_METRICS_LEDGER: VT run 1153a763 row added; cumulative CI updated (+1 Houle)
- WORK_QUEUE: Gemini blocker removed; scorer moved to NOW; Atwood investigation added
- PROJECT_STATE_OF_RECORD: VT status updated (Houle→CI, Atwood→PR wrong-doc)
- This DAILY_CHANGELOG entry

**GREEN encoding fixes applied to ca_eviction_v2.json — 2026-07-02 (REVISED-8, REVISED-9)**

*Fix 1 — B-02 (REVISED-8): Added `days_hours_for_in_person_payment` to `notice.notice_types.pay_or_quit.mandatory_content`*
- Source anchor: CCP §1161(2) — "if the address at which rent may be paid is set forth in the notice, the notice shall also set forth the usual days and hours that the landlord is available at such address to receive payment"
- Encodes: `required_when: rent_payable_in_person_at_stated_address`, `fatal_if_omitted: true`
- Rationale: Golden-set CA-NOT-B-02 miss confirmed this element was absent from the encoding. GPT HIGH confident wrong; Gemini correctly UNCERTAIN.
- Discipline C: change grounded in retrieved CCP §1161(2) statutory text; source_anchor included in element.

*Fix 2 — B-09 (REVISED-9): Moved unauthorized subletting from §1161(4) unconditional_quit → §1161(3) cure_or_quit*
- Removed from `unconditional_quit.bright_line_qualifying_conduct`: "Unauthorized assignment or subletting of premises contrary to lease covenants"
- Added to `cure_or_quit.bright_line_qualifying_conduct`: "Unauthorized assignment or subletting contrary to lease covenants (CCP §1161(3) — express statutory curable breach; tenant has right to remove subtenant/assignee within 3 court days)"
- Updated `unconditional_quit.description` and `cure_or_quit.description` to reflect corrected classification
- Source anchor: CCP §1161(3) expressly names "covenant not to assign or sublet" as performable within 3 days; CCP §1161(4) enumerated categories (nuisance, waste, unlawful use) do NOT include subletting
- Rationale: B2 HIGH severity — both models AGREE, both HIGH confidence, both wrong. Encoding error, not legal ambiguity.
- Discipline C: change grounded in CCP §1161(3)/(4) statutory text; source_anchor included in both elements.

**B3 regression check COMPLETE — 12/12 = 100.0% (Andy terminal run 2026-07-02)**
- Output: `rules/validation/scorer/output/ca_notice_score_2026-07-02_non-held-out.json` (overwrites pre-fix run)
- **B-02 ✅ FIXED** — NOTICE_INVALID, AGREE. Encoding fix confirmed effective.
- **B-09 ✅ FIXED** — NOTICE_INVALID correct. Run 1: GEMINI-EMPTY (transient). Run 2 (confirmation, 1:22 PM): **AGREE — DUAL-MODEL-CONSENSUS** (agree=12, disagree=0). B-09 transient flag cleared. Full consensus confirmed.
- **newly_failing = 0** — no regressions from REVISED-8 or REVISED-9 changes. All 10 previously-correct items remain correct.
- B2 confident-wrong: 0 (down from 2 pre-fix). B2 HIGH item (B-09 both-wrong) is resolved.
- Rules SHA256: `cc0cfab63ae1591e2b88…` (reflects REVISED-8 + REVISED-9)
- METRICS_LEDGER updated: B3 block added; repeatability view updated; combined v0.2 summary updated to reflect post-fix 12/12 DUAL-MODEL-CONSENSUS (B-09 transient flag cleared by run 2).

### YELLOW — None new.

### RED — None new.

---

## 2026-07-01 (session 8 — v0.2 golden set FROZEN: 17 items, held-out split locked)

### GREEN — Executed autonomously

**Golden set v0.2 FROZEN — Task #23 COMPLETE (GREEN)**

**Drop B-04 (near-duplicate):**
- CA-NOT-B-04 (30-day to 14-month tenant) dropped per Andy's direction — re-tests the same determinate rule as v0.1 CA-NOT-03 (§1946.1(b): tenancy ≥1yr → 60-day required) with only duration varied. Leaves 17 items.

**Freeze 17 items:**
- All 17: Status=FROZEN, ATTORNEY VERDICT=CONFIRMED, Correct outcome = Drafted outcome (Andy confirmed all as-drafted), Reviewed by=Andrew M. Cohen, Date=2026-07-01
- File: `rules/validation/scorer/FROZEN/goldenset_CA_notice_v0.2_20260701.xlsx`
- SHA256: `f65c4240e3ec3c4f7f370d805de906b024e7d3e4f51df92b76197eed1962fa83`
- Scorer validation: 0 YELLOW flags (schema exact match; all KNOWN_OUTCOMES; all FROZEN items complete)

**Held-out split — LOCKED:**
- Method: hybrid — Python `random.sample`, seed=20260701, within leakage-aware pool
- Leakage-aware pool (6 items NOT re-testing any of the 6 self-critique corrections): CA-NOT-B-01, B-02, B-03, B-13, B-14, B-18
- The six corrections: §1946.1(b)/(c) tier+Stancil, SFH two-prong, residential/commercial waiver, day-count/SB 611, §1161(3)/(4) gate, SB 567 relocation
- Draw (5 of 6): CA-NOT-B-01, CA-NOT-B-03, CA-NOT-B-13, CA-NOT-B-14, CA-NOT-B-18 → Held-out=TRUE
- CA-NOT-B-02 (not drawn from pool) → Development=FALSE
- All 11 correction-re-testers (B-05, B-06, B-07, B-08, B-09, B-10, B-11, B-12, B-15, B-16, B-17) → Development=FALSE
- Per protocol rule 4: held-out flags LOCKED — never adjusted after this point

**Leakage guard — CONFIRMED PASSED:**
1. No held-out item is verbatim/near-verbatim of any v0.1 frozen item ✅
2. All 5 held-out items are NOVEL (none re-tests one of the 6 corrections) ✅
3. Held-out set spans outcomes: NOTICE_VALID (B-13, B-18) + NOTICE_INVALID (B-01, B-03, B-14) ✅
4. Held-out set is NOT composed solely of correction re-testers ✅

**VALIDATION_METRICS_LEDGER.md updated (GREEN)**
- v0.2 FROZEN block added with full provenance, SHA256, split, guard confirmation
- Repeatability view row added: v0.2 FROZEN — awaiting dual-model score

**WORK_QUEUE.md updated (GREEN)**
- v0.2 FROZEN gate row ✅ with SHA256 and held-out IDs
- Stage 2 dual-model score gate remains open; NEXT ACTION: Andy runs scorer from terminal once Gemini 503 clears

**SHA256 re-serialization note added (GREEN)**
- Recorded hash `f65c4240…` is the openpyxl at-freeze binary; Excel Desktop re-serializes on open/save → different binary, identical legal content.
- Integrity check should compare canonical fields (ID, Correct outcome, Held-out flag), not binary hash.
- Note added to METRICS_LEDGER v0.2 block and WORK_QUEUE next-action item.

**Small-sample caveat added to all reporting surfaces (GREEN)**
- Held-out n=5: 95% CI is wide (5/5→[47.8%,100%]; 4/5→[28.4%,99.5%]). Result is directional signal, not precision rate.
- Framing: "N of 5 held-out items correct — small-sample result; interpret as directional signal only."
- Caveat added to METRICS_LEDGER (v0.2 block + next-run-target) and WORK_QUEUE.

### YELLOW — None new.

### RED — None new.

---

## 2026-07-01 (session 7 — Golden set v0.2 DRAFT created: 18 candidates, independent source)

### GREEN — Executed autonomously

**Golden set v0.2 DRAFT Excel created — Task #21 + #22 COMPLETE (GREEN)**
- File: `rules/validation/scorer/DRAFT/goldenset_CA_notice_v0.2_DRAFT_20260701.xlsx`
- 18 DRAFT candidates, two-sheet workbook (Candidates + Notes)
- Headers: exact match to `EXPECTED_COLUMNS` in `ca_notice_scorer.py`; scorer will correctly skip all DRAFT rows
- All 18: Status=DRAFT, ATTORNEY VERDICT=blank, Correct outcome=blank, Held-out=blank (Andy fills)

**Independence constraint satisfied:**
- Group A (7 items): sourced from CJER BG 31 (2015 ed.) embedded hypotheticals — §§31.2(7), 31.16, 31.17, 31.20, 31.26(2). IDs: CA-NOT-B-01, B-02, B-03, B-06, B-07, B-08, B-09.
- Group B (11 items): sourced from primary statutory text — CCP §1161 (SB 611 court-day counting), Civ. Code §1946.1(b) (30/60-day), §1946.2(d) (SB 567 relocation), §1946.2(e)(6)/(7)/(8) (exemptions), Stancil v. Superior Court (2021). IDs: CA-NOT-B-04, B-05, B-10 through B-18.
- Zero candidates derived from the rules-writing pass or self-critique pass.

**No v0.1 reuse:** All 18 candidates confirmed distinct from the 16 frozen v0.1 items. CA-NOT-B-04 (30-day to 14-month tenant) tests the same legal rule as CA-NOT-03 but with a different tenancy duration; flagged in the Notes sheet for Andy's review.

**Outcome distribution:** NOTICE_VALID=5 (B-08, B-11, B-13, B-16, B-18), NOTICE_INVALID=12 (B-01 through B-07 excl. B-08, plus B-09, B-12, B-14, B-15, B-17), UD_DEFECTIVE_PREMATURE=1 (B-10).

**WORK_QUEUE.md updated (GREEN)**
- Stage 2 gate v0.2 DRAFT row marked ✅
- "Andy reviews + freezes v0.2" marked as NEXT ACTION FOR ANDY

### YELLOW — None new.

### RED — None new.

---

## 2026-07-01 (session 6 — Stage 2 encoding validation; Lawvable explored; VT retry queued)

### GREEN — Executed autonomously

**Stage 2 non-held-out scorer run — 11/11 = 100% (SM-GPT PARTIAL-CONSENSUS) (GREEN — encoding verified)**
- Andy ran `ca_notice_scorer.py --non-held-out-only` from his terminal after Gemini credits restored.
- Result: 11/11 = 100.0% on non-held-out partition. All 6 pilot gaps closed by self-critique encoding.
- Consensus status: PARTIAL-CONSENSUS (1/11 dual-model). Gemini error: 503 UNAVAILABLE (capacity, not credits). CA-NOT-08 confirmed AGREE — credits working, capacity transient.
- B1 Coverage: 11/11 = 100% known; Accuracy (known): 100%; Overall: 100%.
- B2 Confident-wrong: 0. ZERO.
- B3 Regression check: newly_failing = 0. Prior 7/11 → current 11/11. 4 newly correct: CA-NOT-08, CA-NOT-12, CA-NOT-14, CA-NOT-20.
- B4 Currency: ✅ (self-critique pass this session).
- Run NOT consensus-operative. No held-out burn. Cannot cite as consensus-validated.
- Output: `rules/validation/scorer/output/ca_notice_score_2026-07-01_non-held-out.json`

**VT retry job queued for tonight (GREEN — pipeline re-queue, anti-default rule applied)**
- New job: `rules/validation/queue/job_vt_retry_gemini_restored_20260701.json`
- Prior run (1c7f0772) showed RC=2 with C=FLAG-generate-failed due to Gemini 429. Anti-default rule applied: NOT routed to attorney. Re-queue with credits restored.
- Gemini 503 capacity issue (not credits) means overnight timing improves chances. Will confirm Gemini API status for Stage 2 DUAL-MODEL-CONSENSUS gate.

**Lawvable MCP explored — YELLOW-REG-03 RESOLVED (GREEN — confirmed no relevant skills)**
- Searched `lawvable_search_skills` for "eviction housing tenant landlord notice" + US jurisdiction filter.
- Result: 0 eviction, housing, tenant-landlord, or residential-tenancy skills in Lawvable marketplace.
- 189 total skills; 20 categories; no housing-law or residential-tenancy category.
- US jurisdiction (20 skills): sanctions screening, employment law, customs trade, privacy, CT divorce, trademark. None relevant to CJaC eviction-defense encoding.
- **Conclusion**: Lawvable is a corporate/compliance-oriented marketplace. CJaC is novel territory — no existing skill infrastructure for eviction defense. YELLOW-REG-03 closed.

**VALIDATION_METRICS_LEDGER.md updated (GREEN)**
- Stage 2 v1 row added to CA-notice pilot runs table with full B1-B4 breakdown.
- Miss triage table updated with Stage 2 encoding status for each of the 6 pilot gaps.
- Repeatability view row added.

**WORK_QUEUE.md updated (GREEN)**
- Stage 2 gate table updated: gates 3+credits ✅, encoding validation ✅; DUAL-MODEL-CONSENSUS + v0.2 golden set + held-out score still open.
- Lawvable row → RESOLVED.

### YELLOW — Flagged for Andy

**Gemini 503 UNAVAILABLE (YELLOW — capacity, not credits)**
- 10/11 items returned Gemini 503 despite credits being restored. One item (CA-NOT-08) got through, confirming credits work.
- Not a blocker for tonight's VT retry (overnight low-traffic). If persistent after tonight: may need to downgrade from gemini-2.5-pro to gemini-2.5-flash or adjust retry logic in scorer.
- Stage 2 DUAL-MODEL-CONSENSUS gate remains open until Gemini runs clean.

### RED — None new.

---

## 2026-07-01 (session 5 — Ratification round; 4 FLAGGED → RESOLVED; Stage 2 gate 3 closed)

### GREEN — Executed autonomously

**RESOLVED-1: Stancil any-occupant rule → machine-checkable encoding (GREEN — Andy ratified)**
- `ca_eviction_v2.json`: `termination.tenancy_1yr_plus` now has `condition: "all_occupants_residency_max_years >= 1"` and `stancil_any_occupant_rule.machine_checkable_input: "max_occupant_residency_years"`.
- PLAYBOOK_SPEC §9 `notice_period_termination_no_fault`: conditions updated to use `max_occupant_residency_years` per Stancil; `source_anchor` = "Stancil v. Superior Court (2021) 11 Cal.5th 381; Civ. Code §1946.1(b)".
- Source anchor: Stancil v. Superior Court (2021) 11 Cal.5th 381; Civ. Code §1946.1(b).

**RESOLVED-2: Full AB 1482 exemption matrix — all 8 §1946.2(e) categories encoded (GREEN — Andy ratified)**
- `ca_eviction_v2.json`: `termination.exemptions` expanded from 1 entry (SFH non-entity) to 5 structured entries covering all 8 §1946.2(e) categories:
  - `sfh_non_entity_owner` (§1946.2(e)(8)) — two-prong: owner not REIT/corp/LLC + written exemption notice
  - `sfh_owner_occupied` (§1946.2(e)(5)) — owner occupies ≤2-unit building
  - `owner_occupied_duplex` (§1946.2(e)(6)) — owner-occupied duplex
  - `new_construction_15yr` (§1946.2(e)(7)) — COO within 15 years of notice date, rolling basis
  - `institutional_uses` (§1946.2(e)(1)–(4)) — transient/tourist hotel, institutional, dormitory, shared kitchen/bath with owner
- PLAYBOOK_SPEC §9: New `ab1482_exemption_matrix` element added encoding all 8 categories as machine-checkable conditions; default = AB1482_COVERED.
- Source anchor: Civ. Code §1946.2(e)(1)–(8).

**RESOLVED-3: §1161(3)/(4) bright-line gate encoded (GREEN — Andy ratified)**
- `ca_eviction_v2.json`: `unconditional_quit.bright_line_qualifying_conduct` list defined (physical waste, nuisance per §3482.8/§3485(c)/§3486(c), unlawful use, unauthorized assignment/subletting). `open_textured_conduct` list for ambiguous cases (repeated disturbances, unauthorized smoking, noise complaints).
- `cure_or_quit.bright_line_qualifying_conduct` list defined (failure to maintain premises, unauthorized pet if curable, unauthorized occupant if curable, etc.).
- PLAYBOOK_SPEC §9 interactions: `cure_or_quit_vs_unconditional_quit` gate added — determinate routing for bright-line conduct; open-textured path for ambiguous.
- Source anchor: CCP §1161(3); CCP §1161(4); Civ. Code §§3482.8, 3485(c), 3486(c).

**RESOLVED-4: `missing_just_cause_reason` defect scoped to AB1482-covered units (GREEN — Andy ratified, follow RESOLVED-2)**
- `ca_eviction_v2.json`: `notice_defects.missing_just_cause_reason` updated with `applies_to: "AB1482_covered_units_only"` and `ab1482_coverage_gate` block listing all 8 §1946.2(e) exemption categories. Defect only fires after machine checks that the unit is NOT exempt.
- Source anchor: Civ. Code §1946.2(e)(1)–(8); AB 1482 (Stats. 2019, c. 597).

**`docs/CA_NOTICE_SELF_CRITIQUE_REPORT_20260701.md` — FLAGGED items updated to RESOLVED (GREEN)**
- All 4 FLAGGED items updated to RESOLVED status with Andy ratification date, encoding decisions, and source anchors.
- Stage 2 gate table updated: Gate 3 ✅ CLOSED.

**`docs/WORK_QUEUE.md` updated (GREEN)**
- NOW block updated: 4 FLAGGED → 4 RESOLVED items with status table.
- Stage 2 gate status: Gate 3 ✅ (Andy ratified). Gates 1, 4, 5 remain open (Gemini credits blocker).

### YELLOW — None new this session.

### RED — None new. (Existing RED: Gemini credits. Andy action required to unblock Stage 2 dual-model run.)

---

## 2026-07-01 (session 4 — Self-critique pass + structural addendum; all CA-notice rules revised)

### GREEN — Executed autonomously

**CA-notice self-critique pass complete (GREEN — source-anchored, three disciplines)**
- Produced `docs/CA_NOTICE_SELF_CRITIQUE_REPORT_20260701.md`: 9 REVISED / 3 CONFIRMED / 4 FLAGGED (attorney residual)
- Sources: frozen golden set `goldenset_CA_notice_v0.1` (Part 1 anchor) + WebSearch live retrieval (CCP §1161 SB 611 eff. 2/1/2025 confirmed; CCP §1162 confirmed)

**`rules/eviction/california/ca_eviction_v2.json` — notice section updated (GREEN)**
- REVISED-1: Added `termination.tenancy_1yr_plus` (60d, §1946.1(b)); corrected `tenancy_under_1yr.statute` → §1946.1(c)
- REVISED-2: Added `termination.exemptions[sfh_non_entity_owner]` with two-prong test (§1946.2(e)(8)(A)+(B)); removed incorrect owner-occupancy encoding
- REVISED-3: Added `payee_id_missing` defect (CCP §1161(2); Lynch & Freytag + Eshagian)
- REVISED-4: Added `relocation_assistance_missing` defect (Civ. Code §1946.2(d); SB 567 eff. 4/1/2024)
- REVISED-5: Added `waiver_rules.partial_payment_waiver` with determinate core + open-textured exception; excluded CCP §1161.1 (commercial only per §1161.1(d))
- REVISED-6: Added `unconditional_quit` notice type (CCP §1161(4)); added `wrong_instrument_incurable_conduct` defect
- REVISED-7: Fixed `pay_or_quit.tenancy_under_1yr` and `tenancy_over_1yr` count_method: `calendar_days` → `calendar_days_excluding_weekends_holidays` (CCP §1161 SB 611 eff. 2/1/2025)
- REVISED-8: Filled `improper_service_method.statute` from null → `CCP §1162`
- REVISED-9: Filled `notice_period_too_short.statute` from null → `CCP §1161(2),(3),(4); Civ. Code §1946.1(b),(c)`
- Added `mandatory_content` block to pay_or_quit with payee name/phone/address requirements
- Updated `module_status.notice.status` → `SELF-CRITIQUE-COMPLETE` with report cross-reference
- Updated `per_module_sources.notice` with 15 authorities (was 5)

**`docs/PLAYBOOK_SPEC.md` structural updates (GREEN)**
- §3: Added `source_anchor`, `flagged`, `flagged_reason` fields to element schema
- §9 `notice_period_termination_no_fault`: fixed subsection citations — §1946.1(c) for <1yr, §1946.1(b) for ≥1yr (was citing (b) for both). Added missing DEFECTIVE condition for <1yr. Added `source_anchor`.
- §9 `sfh_ab1482_exemption`: replaced `not_owner_occupied = true` with mandatory two-prong (§1946.2(e)(8)(A)+(B)). Added `source_anchor`.
- §9 `partial_payment_waiver`: restructured from wholly `open_textured` to `determinate` with open-textured exception path. Added `source_anchor`. Tier cap changed A/determinate (core) + B (exception).
- §10: Added SELF-CRITIQUE as standing step 2 in validation workflow (DRAFT → SELF-CRITIQUE → YELLOW/attorney residual → ratification → auto-checks → golden-set → attorney → VALIDATED). Added L1 gate note for `source_anchor`.
- §11 (NEW): Four measurement directives (B1 coverage, B2 confident-wrong, B3 regression, B4 currency) as permanent requirements.

**`CLAUDE.md` — standing disciplines added (GREEN)**
- Added "Self-critique disciplines (STANDING OPERATING RULES)" section: Disciplines A/B/C as permanent session-start rules, not dated directives
- Added "Measurement standards (STANDING)" section: B1-B4 as permanent requirements
- Updated "Last updated" stamp to 2026-07-01

**`docs/COWORK_DIRECTION_A_CADENCE_AUTONOMY.md` — Parts 5–6 added (GREEN)**
- Part 5: Self-critique disciplines (Disciplines A/B/C — permanent)
- Part 6: Measurement directives (B1-B4 — permanent)

**`docs/WORK_QUEUE.md` updated (GREEN)**
- Self-critique pass marked COMPLETE with item-level results table
- 4 FLAGGED items listed for Andy ratification
- Stage 2 gate status updated post-self-critique

### YELLOW — Flagged for Andy ratification

**FLAGGED-1: Stancil "any occupant" nuance (YELLOW)**
- `Stancil v. Superior Court (2021) 11 Cal.5th 381`: 60d requirement attaches once ANY occupant has resided ≥1yr, not just named tenant.
- Question: encode as machine-checkable condition (requiring all occupants' tenancy durations as input) or notes-only treatment?
- Action needed: Andy/attorney call. No encoding change made pending ratification.

**FLAGGED-2: AB 1482 exemptions beyond SFH (YELLOW — scope)**
- §1946.2(e) has multiple exemption categories: new construction (<15yr), condos, luxury housing, ADUs — none encoded.
- Question: does this pass encode SFH-only (current state) or expand to full exemption matrix?
- Action needed: Andy ratifies scope.

**FLAGGED-3: Cure-or-quit / unconditional-quit interaction gate (YELLOW)**
- §1161(3) vs. §1161(4) interaction not encoded as an explicit gate. Propose bright-line enumerated conduct list (waste/nuisance → §1161(4); covenant breach → §1161(3)); ambiguous categories to attorney line.
- Action needed: Andy ratifies approach.

**FLAGGED-4: `missing_just_cause_reason` defect scope (follow-on to FLAGGED-2)**
- Blanket `just_cause_required: true` partially resolved by SFH exemption but other exemptions (FLAGGED-2) leave gaps.
- Action needed: Resolve after FLAGGED-2.

### RED — Escalated to Andy

*(No new REDs this session. Existing REDs unchanged: Gemini credits, Direction B freeze, 6 RC, attorney queue.)*

---

## 2026-07-01 (session 3 — Skills decision; consensus-operative gate; JusticeBench alignment)

### GREEN — Executed autonomously

**Reasoning-engine decision documented (GREEN)**
- ARCHITECTURE.md: Added Section 12 — Claude native legal-reasoning is the CJaC reasoning engine. `legal:*` plugins NOT adopted wholesale (designed for corporate/contract workflows, not eviction-defense encoding). Lawvable MCP to be explored as carry-over task.
- VALIDATED_RESOURCES_REGISTRY.md: `claude_native_legal` updated to PRIMARY reasoning engine (confirmed). `legal_plugin_skills` updated as NOT integrated (by decision). YELLOW-REG-02 resolved.

**Consensus-operative gate implemented in `ca_notice_scorer.py` v2.1 (GREEN pipeline fix)**
- Per Andy direction: a run where either model returns empty is NOT consensus-validated and must be flagged loudly.
- Changes: `consensus_valid: true/false` per item; `_consensus_status()` classifier (DUAL-MODEL-CONSENSUS / SM-GPT / SM-GEMINI / PARTIAL-CONSENSUS / SM-BOTH-ERROR); `⛔` banner in console report when not consensus-operative; `⚠SM` tag on per-item lines; `consensus_status`, `single_model_items`, `consensus_note` in run metadata; `single_model_items` count in summary stats.
- Syntax check: ✅ passes `python3 -m py_compile`
- Note: v1 pilot run (2026-07-01) would have shown SM-GPT banner under this protocol; score was 3/5=60% SM-GPT — correctly labeled PRELIMINARY.

**WORK_QUEUE updated — consensus gate (GREEN)**
- Added hard gate block before Stage 2 scoring: `consensus_status == "DUAL-MODEL-CONSENSUS"` required before any held-out score can be cited. Gate is now explicit and prominent.

**VALIDATED_RESOURCES_REGISTRY.md updated — consensus-operative gate (GREEN)**
- `multi_model_consensus` entry updated with gate definition, history note (GPT has also gone empty on non-notice modules), and Stage 2 blocker note.

### YELLOW — Flagged for Andy ratification

**JusticeBench actor-calibration alignment (YELLOW — architecture note, no action needed)**
- Identified while reviewing JUSTICEBENCH_ALIGNMENT_SPEC.md: Hagan's per-step actor calibration framework (senior human / junior human / deterministic rules-code / small model / frontier model) is the academic parallel to CJaC's `determinate`/`open_textured` strategy tagging.
  - `determinate` ↔ Hagan's "deterministic rules-based code"
  - `open_textured` (bounded reasoning) ↔ Hagan's "intensive frontier model"
- This validates the architectural choice independently. Can cite Hagan's framework as external validation of the playbook architecture's design logic.
- YELLOW because it's an architectural note with potential reporting implications (strengthens the "validated rules layer" thesis for public-facing materials). No immediate action — log in next session context.

### RED — None new this session

---

## 2026-07-01 (session 2 — Playbook Architecture Directive; Stage 1 in progress)

### GREEN — Executed autonomously

**Playbook Architecture Directive saved (GREEN)**
- `docs/CJaC_Playbook_Architecture_Directive_20260701.md` — Andy's July 1 architectural change directive filed to docs/
- Covers: thesis anchor; what stays; playbook-as-unit architecture; bounded-reasoning; Validated Resources Registry; staged execution (Stages 0–4); success metric

**`docs/ARCHITECTURE.md` created (GREEN)**
- Documents one-pipeline playbook architecture: three-tier infrastructure, playbook unit, element decomposition, `determinate`/`open_textured` strategy tags, confidence tiers (A/B/C), known/unknown flag, jurisdiction-resolution, seven-layer validation stack, bucket taxonomy, staged proof sequence, source hierarchy
- Key files table links to PLAYBOOK_SPEC, VALIDATED_RESOURCES_REGISTRY, and directive

**`docs/PLAYBOOK_SPEC.md` created (GREEN)**
- Full playbook unit schema: playbook (top-level), element, strategy tag definitions (`determinate`/`open_textured`), known/unknown, confidence tiers, interaction schema, source IDs, partial CA pay-or-quit example (4 elements: notice_period_nonpayment, notice_period_termination_no_fault, sfh_ab1482_exemption, partial_payment_waiver), validation workflow
- Example encodes 4 of 6 pilot gaps as DRAFT elements

**`docs/VALIDATED_RESOURCES_REGISTRY.md` created (GREEN — seed)**
- 13 sources catalogued: `ca_civil_code_live`, `ca_ccp_live`, `courtlistener_mcp`, `descrybe_mcp`, `legal_data_hunter_mcp`, `ca_benchguide_ud`, `lsnc_eviction_2026`, `justicebench_stanford`, `lsc_temple_dataset`, `claude_native_legal`, `legal_plugin_skills`, `lawvable_mcp`, `multi_model_consensus`
- Each source: tier, currency risk, coverage, limitations, status, use-for notes
- 4 YELLOW flags raised (REG-01 through REG-04)
- Status summary table included

**WORK_QUEUE updated (GREEN)**
- NOW: Stage 1 progress table (4 of 6 items ✅; 2 pending research)
- NEXT: Stage 1 carry-overs (Benchguide research, Lawvable exploration), Stage 2 plan (6 items including element encoding table with revised classification — item 6 is `open_textured`, not purely deterministic)

### YELLOW — Flagged for Andy ratification

**Skills/tools status (YELLOW-REG-02, YELLOW-REG-03)**
- No skills named "legal-analysis" or "issue-spotting" found in environment
- `legal:*` plugin skills (brief, risk-assessment, review-contract, triage-nda) available but NOT integrated into CJaC pipeline
- Lawvable MCP (`lawvable_search_skills`) available but not yet searched for eviction/housing legal skills
- **Andy: direction needed** — integrate `legal:*` skills into playbook element analysis? Explore Lawvable for legal-analysis skills?

**Strategy tag ratification needed for Stage 2 (RED gate)**
- PLAYBOOK_SPEC.md defines `determinate`/`open_textured` tags as set by human attorney at encoding time
- Draft element strategy tags proposed for CA pay-or-quit playbook (4 elements in PLAYBOOK_SPEC example)
- Andy must ratify strategy tags before Stage 2 encoding proceeds

### RED — None new this session

---

## 2026-07-01 (session — CA-notice pilot run complete; architecture memo ingested)

### GREEN — Executed autonomously

**Fixed dotenv path bug in `ca_notice_scorer.py` (GREEN bug fix)**
- `parents[4]` → `parents[3]` in dotenv loader — scorer was looking for `.env` at `GitHub/.env` instead of `a2j-ai/.env`; API keys were never loaded; all API calls returned "missing credentials"
- Fix: single-character change; verified correct path matches `REPO_ROOT` (also `parents[3]`)

**CA-notice pilot live run — first real score (GREEN run; SM-GPT; Gemini 429 depleted)**
- Output: `rules/validation/scorer/output/ca_notice_score_2026-07-01.json`
- SHA256 (golden set): `b87791ecda032fa718df027da47a07774c03eb940354321a3c9d0d77ba0fc7e9`
- SHA256 (rules file): `8cc0b3e51fa57ad211c9976753dd96575401eb47daa54b7759e2bcda1efb4101`
- **Held-out score: 3/5 = 60.0%** ← headline (held-out set now burned)
- Non-held-out score: 7/11 = 63.6%
- Overall (all frozen): 10/16 = 62.5%
- GPT-only run (Gemini 429 RESOURCE_EXHAUSTED on all 16 items — credits depleted)
- Zero YELLOWs (schema clean; all outcome enums recognized)

**Triage of 6 misses — all are rules-gap (not model-wrong):**
- CA-NOT-03 (held-out): 60-day termination notice for tenancies ≥ 1yr not encoded (Civ. Code 1946.1(b))
- CA-NOT-08 (non-held-out): SFH AB 1482 exemption not encoded (1946.2(e)(8)); GPT correctly returned INVALID given encoded rules (missing rule, not wrong reasoning)
- CA-NOT-12 (non-held-out): Payee ID requirement not encoded (CCP 1161(2) mandatory content)
- CA-NOT-14 (non-held-out): Relocation assistance for no-fault termination not encoded (Civ. Code 1946.2(d))
- CA-NOT-16 (held-out): Partial rent acceptance / waiver doctrine not encoded (EDC Associates v. Gutierrez)
- CA-NOT-20 (non-held-out): CCP 1161(4) unconditional quit for incurable conduct not encoded

**4 excluded items logged as downstream work (GREEN)**
- CA-NOT-09 → open-textured queue (utilities-as-"additional-rent" ambiguity)
- CA-NOT-15 → retaliation module golden set (§1942.5 retaliatory eviction)
- CA-NOT-17 → service module golden set (§1161 subtenant-service; §415.46)
- CA-NOT-19 → LA local-overlay golden set (LAMC §151.09 — FMR threshold, bedroom statement, LAHD filing)

**Architecture memo saved to docs/ (GREEN)**
- `docs/CJaC_Architecture_and_Roadmap_Memo_20260701.md` — canonical architecture direction post-pilot
- Section 5 items actioned (see below)

**Section 5 Cowork-actionable items executed (GREEN):**
- Item 1: Jurisdiction-resolution principle added to `docs/Decision_Logic_Briefing_for_Claude.md` (new Section 9)
- Item 2: Benchguide source lane note added to `docs/VALIDATION_METRICS_LEDGER.md` (pending-source-class note)
- Item 3: Direction D logged in WORK_QUEUE HORIZON (3 components; ethical signal-source constraint recorded as non-negotiable)
- Item 4: Reporting scope note added to VALIDATION_METRICS_LEDGER pilot-score section
- Item 5: LA RSO+JCO overlay golden set logged in WORK_QUEUE HORIZON as first local-overlay build

**Living documents updated (GREEN)**
- `docs/VALIDATION_METRICS_LEDGER.md` — Direction B pilot-score section added; repeatability row added; reporting scope note per memo Section 4
- `docs/PROJECT_STATE_OF_RECORD.md` — L4/Direction B status updated to reflect first pilot run
- `docs/WORK_QUEUE.md` — NOW replaced with post-pilot state; 6 rules-gap items added to NEXT; exclusions logged; Direction D + LA overlay in HORIZON
- `docs/CLAUDE_CHAT_BRIEF.md` — Regenerated with first held-out score
- `docs/Decision_Logic_Briefing_for_Claude.md` — Jurisdiction-resolution principle added (Section 9)

### YELLOW — Flagged for Andy ratification

**First held-out score (60.0%) — 6 rules gaps identified (YELLOW)**
- Held-out set is now burned. Score: 3/5 = 60%.
- All 6 misses are rules-gap, not model-wrong. Encoding the 6 missing rules is the direct fix.
- YELLOW: This is an engineering choice (which rules to add first, in what order) with downstream metrics impact. Andy ratify / provide direction before next scorer run.
- Proposed next step: encode all 6 missing rules in `ca_eviction_v2.json`, re-run scorer with fresh golden set (or non-held-out only for iteration), report new score.

**Gemini credits still depleted (YELLOW-carry)**
- Live run confirmed Gemini still 429. Re-run with two-model consensus requires credits restoration.

### RED — Decisions needed from Andy

None new this session (scoring direction is YELLOW, not RED — encoding the missing rules is an engineering task, not a legal-interpretive judgment).

---

## 2026-07-01 (morning report — VT retry Gemini 429 blocker; no metrics movement)

### GREEN — Executed autonomously

**Overnight run 1c7f0772 ingested (VT retry, `job_vt_retry_fresh_20260630`)**
- 2 units: Atwood v. Hill (VT Superior Court 2024, CL cluster 10145325) + Houle v. Quenneville (VT SC 2001, CL cluster 2320677)
- Check A ✅ both cases (text retrieved from CL), Check B ✅ both (no negative treatment)
- Check C ❌ both — Gemini 429 RESOURCE_EXHAUSTED (prepayment credits depleted)
- Harness classified RC; anti-default rule applied — NOT added to HUMAN_REVIEW_QUEUE
- Both cases quarantined for re-queue once Gemini credits restored

**Anti-default rule enforced — 0 cases routed to attorney lane**
- Gemini 429 = API billing infrastructure failure. "Model returned empty" rule applies.
- Cases will be re-queued once credits restored; no attorney review warranted at this time.

**Living documents updated (GREEN)**
- `docs/VALIDATION_METRICS_LEDGER.md` — 2026-07-01 morning report entry added; Gemini 429 blocker noted; cumulative counters unchanged (MV=25, CI=3, RC=6)
- `docs/PROJECT_STATE_OF_RECORD.md` — Last updated stamp + VT retry result logged
- `docs/HUMAN_REVIEW_QUEUE.md` — Header updated (no new items; anti-default rule confirmed)
- `docs/WORK_QUEUE.md` — Gemini credits blocker added to BLOCKED; VT re-queue note in NEXT; "Completed Today" updated
- `docs/DAILY_CHANGELOG.md` — This entry
- `docs/CLAUDE_CHAT_BRIEF.md` — Regenerated (step 3f)

### YELLOW — Flagged for Andy ratification

**None this cycle.**

### RED — Decisions needed from Andy

**Gemini API prepayment credits depleted (RED-strategic)**
- All overnight runs using Gemini are blocked
- Andy must top up at [AI Studio](https://aistudio.google.com/projects) → billing
- Once restored: Cowork will re-queue VT retry same night (fresh=true, both cases have text already retrieved)

---

## 2026-07-01 (session — Direction B scorer harness built; dry-run passed)

### GREEN — Executed autonomously

**`ca_notice_scorer.py` built — Excel-native Direction B scorer (GREEN build)**
- New file: `rules/validation/scorer/ca_notice_scorer.py` (v2.0-excel-native, ~340 lines)
- Reads directly from `goldenset.xlsx` (attorney-reviewed Excel); no JSON intermediary
- Schema validation at load time: checks all 13 expected columns; raises YELLOW on any missing
- Outcome enum: `NOTICE_VALID | NOTICE_INVALID | UD_DEFECTIVE_PREMATURE | UD_NOT_SUSTAINABLE`
- Dual-model pipeline: GPT generates, Gemini verifies; agreement/disagreement tracked per item
- Custom system prompt (scorer-specific — does not reuse l2_runner.py's baked notice-days prompt)
- No answer leakage: model receives only facts + encoded CA-notice rules JSON; correct outcome never included
- Held-out isolation: held-out and non-held-out scores computed and reported separately; no auto-tuning wiring
- Integrity: SHA256 of Excel file + SHA256 of rules file + per-item row hash all logged with every run
- YELLOW surface: schema mismatch, unknown outcome enum, unmapped model output all raise YELLOW with proposed mapping; never silently guesses
- Dry-run mode (`--dry-run`): validates schema, computes hashes, previews queries for first 2 items, mocks all predictions — no API calls needed
- Partitioning flags: `--held-out-only`, `--non-held-out-only`, or run all (default)
- Output: console report + JSON to `rules/validation/scorer/output/`

**Dry-run passed — 13 frozen items, zero YELLOWs (GREEN)**
- All 13 FROZEN items loaded correctly: CA-NOT-01 through CA-NOT-14 (CA-NOT-09 EXCLUDED correctly skipped)
- All DRAFT items (CA-NOT-15-20, CA-SVC-*, TX-NOT-*) silently dropped — correct
- Outcome enum clean: all 4 values (`NOTICE_VALID`, `NOTICE_INVALID`, `UD_DEFECTIVE_PREMATURE`, `UD_NOT_SUSTAINABLE`) present and in known enum
- No schema YELLOWs — all 13 expected columns present
- SHA256 computed: Excel=`3e9550461989c758fb58…`, Rules=`8cc0b3e51fa57ad211c9…`
- Output: `rules/validation/scorer/output/ca_notice_score_2026-07-01_dryrun.json`

**FROZEN/ directory created — provenance copy**
- `rules/validation/scorer/FROZEN/goldenset_CA_notice_v0.1_20260630.xlsx` — SHA256: `3e9550461989c758fb58f0d5159547207e5cd6dd02b4b79bb3eccb8c091ea116`
- This is the reviewed file as of 2026-06-30. Andy will overwrite when final 20-item freeze is complete.

**Note on current frozen set:** All 13 currently frozen items have `Held-out=FALSE`. The held-out score will remain "no held-out items" until Andy sets `Held-out=TRUE` for the selected items in the final 20-item review. The scorer handles this correctly — no code change needed.

### YELLOW — Flagged for Andy ratification

**Scorer `--held-out-only` ready to burn when Andy confirms:**
Once the full 20-item set is frozen and held-out flags are set, running `--held-out-only` permanently burns the held-out score. Andy should confirm readiness before Cowork runs that flag.

---

## 2026-06-30 (session — Task #104 completed; VT job format fix)

### GREEN — Executed autonomously

**VT retry job format fixed — GREEN pipeline correction**
- `rules/validation/queue/job_vt_retry_fresh_20260630.json` had `states`/`fresh`/`sleep` nested under a `config` key — dispatch.py reads those as top-level keys, so the nested format would have caused the job to run with `states=ALL` defaults.
- Fixed: moved `states`, `fresh`, `sleep` to top-level; also set `live_verified: true` so dispatcher picks it up tonight.
- Verified: `python3 -c` check confirms `live_verified=True`, `states='VT'`, `fresh=True`, `job_type='protocol'` — valid per dispatch.py schema.
- VT Houle retry will fire at 2:15 AM 2026-07-01.

**Task #104 confirmed complete**
- All 3 run outputs (VT perm-fail, CO/NY/SC PR retry, 10-state broad query) ingested by morning report.
- 8 state v2 files updated (AL, CT, HI, LA, ND, NM, WV, CO). WV Criss → HUMAN_REVIEW_QUEUE [WV-RET-HOLD-RC-02].
- METRICS_LEDGER confirmed current: 25 MV cumulative, 3 CI, 6 RC.

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
