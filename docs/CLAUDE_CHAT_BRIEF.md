# CJaC — Rolling Handoff for Claude Chat

**Generated:** 2026-07-21 (evening regeneration — dispatcher RED closed, proposals 16/17/18 ratified) — orientation only; canonical docs are authoritative. If this brief and a canonical doc disagree, the canonical doc wins.
**OS state:** Direction A live · Direction B: Broaden Proof 1 COMPLETE · Direction C not started · Direction D-1 live (**v3 regression gate PASSED 07-20** — v3 is the fully active rules version).
**Most important thing right now:** No open RED-strategic Andy action. The overnight dispatcher outage (six missed fires, 07-16→07-21) is closed — root cause was a macOS TCC block on background-agent access to `~/Documents`, not a config error; fix was relocating the repo to `~/Developer/a2j-ai` and reinstalling the LaunchAgent via modern `bootstrap`/`bootout`. Confirmed via `launchctl kickstart` (exit code 0, full heartbeat chain) and a live noon fire. Proposals 16 and 17 are ratified and **execute next session** (16 first, then 17 per sequencing); 18 is ratified log-only, no drafting yet.

---

## 1. Where We Are

The errata-cycle directive is closed end-to-end and **`ca_eviction_v3.json` is the fully active, gate-passed rules version**: Andy ran the live dev-set regression 07-20 10:31 PT — **12/12 = 100%, `newly_failing=0`, DUAL-MODEL-CONSENSUS, α = 1.000** — with the output's rules SHA confirmed = v3 exactly. vProof1 (`ca_eviction_v2.json`) stays byte-frozen as the v0.3 held-out anchor. The v0.3 held-out result stands dual-reported: **23/26 = 88.5% as-scored / 25/26 = 96.2% post-errata** (signed attorney errata for C-21/C-22; ground-truth error rate 2/26 = 7.7%). Scope honesty: the gate verified dev-set non-regression; the C-18 fix itself isn't re-measured against C-18-type facts until v0.4 candidates exist (v0.3 is burned, by design). Holdings unchanged: MV=26, CI=4, RC=6.

**Evening update (07-21 ~7:30 PM):** the dispatcher RED is closed (see below); Andy ratified proposals 16 (self-critique pass, scope extended to include an SB 1103 §1946.1 assessment), 17 (v0.4 golden-set candidate drafting — GO, with a new mandatory ablation arm requirement), and 18 (§1946.1(d) sale-exception — ratified source text logged, still draft-nothing-until-needed). A separate housekeeping error was also corrected: the "last commit 2026-06-16, five weeks uncommitted" note below was itself stale — the repo has in fact been committed/pushed continuously; that note only looked true because the housekeeping audit read a copy of the repo left at the old, pre-relocation path.

## 2. Decisions Waiting on Andy (RED list)

**RED-strategic / Andy actions:**
1. **Refill proposals 16–18 — RATIFIED 07-21 evening, no longer waiting.** 16 = self-critique pass over `just_cause_attachment_threshold` incl. §1946.2(a)(2) live-source verification, scope extended to an SB 1103 (eff. 1/1/2025) §1946.1 assessment; executes next session. 17 = v0.4 golden-set candidate drafting — GO; must include a second ablation arm (same models/items/frozen ground truth, without the rules file) to measure the CJaC lift; sequenced to begin after 16 completes. 18 = §1946.1(d) 30-day sale exception — ratified attorney-sourced statutory text now logged in `MISSING_RULES_BACKLOG.md`; still log-only, draft nothing until an item needs it.
2. **B-4 plist hardening proposal** (`docs/DISPATCHER_PLIST_PROPOSAL.md`): AbandonProcessGroup recommended.
3. **KS/NV/SC CL coverage gap:** Descrybe MCP before accepting Track A as ceiling — Andy's call or GREEN autonomous?
4. **CourtListener bulk-data / rate-limit outreach:** timing is Andy's decision.
5. **Direction C:** still gated — stable score trend + Andy's strategic sign-off.

**RED-interpretive (attorney judgment):**
1. **§1946.2(a)(2) variant verification:** Andy independently verified the trigger text against the statute on 07-20; ratified encoding confirmed outcome-equivalent. Proposal 16's live-source pass (next session) will complete the standing-discipline check and correct the citation label to "§1946.2(a), second sentence, prongs (1)–(2)" at the next version cut.
2. **§1946.1(d) 30-day sale exception:** ratified source text now on file (see item 1 above); still draft-only-on-Andy's-direction.
3. **HUMAN_REVIEW_QUEUE standing items:** 43 L7-ESCALATED, 6 RC, 2 CI cheap-confirm (Baer, Houle), CA/summons MODEL-SPLIT (§1167(a) vs §415.45). No new items this cycle.
4. **Direction B remaining DRAFT freezes:** CA service ×15, TX notice ×15.
5. **CO W.W.G. Corp. YELLOW:** review before citing CO as having MV holdings support.

**BLOCKED:** Direction C (on B trend + sign-off). Overnight lane and automatic D-1 cadence are **unblocked** as of 07-21 evening.

## 3. What Executed Since Last Brief (GREEN digest)

- **07-20 ~10:31 PT (Andy, Terminal):** live v3 regression gate — 12/12, newly_failing=0, DUAL-MODEL-CONSENSUS, α=1.000, trigger-fired and consumed.
- **07-20 late-morning session:** gate output verified against raw JSON (rules SHA = v3); PENDING→PASSED corrections in ledger/PSOR/proposal doc; errata-cycle directive closed end-to-end.
- **07-21 daytime:** dispatcher outage root-caused via control-test methodology (trivial `/tmp`-based LaunchAgent succeeded, identical `~/Documents`-based job failed → macOS TCC block on background-agent access to protected folders, not a config or permissions-toggle issue). Fix: repo relocated to `~/Developer/a2j-ai`, plist paths updated, LaunchAgent reinstalled via `launchctl bootstrap`/`bootout`. Confirmed via `launchctl kickstart` (exit 0, full heartbeat chain) and a live noon fire — six-fire outage (07-16→07-21) closed.
- **07-21 evening:** Andy ratified proposals 16 (scope-extended), 17 (GO + ablation-arm requirement), 18 (source text logged, log-only); stale housekeeping note corrected; `WORK_QUEUE.md`, `PROJECT_STATE_OF_RECORD.md`, `DAILY_CHANGELOG.md`, `MISSING_RULES_BACKLOG.md` updated to reflect all of the above; this brief regenerated.

## 4. Metrics Movement

- **Dev set (07-20 gate):** 12/12 = 100%, α = 1.000, newly_failing=0 — first fully consensus-validated dev run since the 07-16 SM-GPT baseline (converts it to consensus).
- **B2 confident-wrong = 1** (C-18 class; v3 encodes the fix, dev-gate-passed; direct re-test lands in v0.4). **B3:** newly_failing=0 (07-20); no rule change since. **B4:** §1946.2(a)(2) flag carried; Andy's independent verification logged 07-20/21, live-source pass still scheduled (proposal 16).
- **v0.3 held-out (BURNED, standing):** 88.5% as-scored / 96.2% post-errata, α=1.000 (n=26), dual-reported.
- **Holdings:** MV=26/CI=4/RC=6 unchanged since 07-06.
- **Dispatcher:** outage closed 07-21; overnight (2:30 AM) and noon fires both active again as of this evening.

## 5. Queue Snapshot

- **NOW:** empty going into next session's start — proposal 16 execution (self-critique pass + SB 1103 assessment) is the queued first item.
- **NEXT:** proposal 17 (v0.4 golden-set drafting + ablation arm) after 16 completes; 18 remains log-only; carried: 12 (per-call backoff), 14 (Northgate #3, held).
- **BLOCKED:** Direction C only.

## 6. Pointers (for depth)

- `VALIDATION_METRICS_LEDGER.md` — v3 version record (gate row), 07-21/07-20 cycle entries, v0.3 writeup + errata
- `ERRATA_MEMO_v0_3_20260719.docx` (authoritative) / `.md` — the signed correction instrument
- `RULE_PROPOSAL_1946_2a_ATTACHMENT_20260719.md` / `WIRING_DETERMINATION_1946_2e_20260719.md` — the ratified pair
- `PROJECT_STATE_OF_RECORD.md` · `HUMAN_REVIEW_QUEUE.md` · `WORK_QUEUE.md` · `DAILY_CHANGELOG.md`

---

*Regenerated every morning-report cycle (and ad hoc after major evening decisions/fixes, as here). Canonical docs win.*
