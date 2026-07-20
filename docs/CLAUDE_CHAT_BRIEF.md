# CJaC — Rolling Handoff for Claude Chat

**Generated:** 2026-07-20 (morning report, fired on time at ~8:00 AM) — orientation only; canonical docs are authoritative. If this brief and a canonical doc disagree, the canonical doc wins.
**OS state:** Direction A live · Direction B: **Broaden Proof 1 COMPLETE end-to-end** (v0.3 held-out burned 07-19) · Direction C not started · Direction D-1 live, next run = v3 regression gate (trigger armed).
**Most important thing right now:** Two Andy actions close the loop. (1) The plist reinstall + launchctl reload (unchanged command) — dispatcher has now missed **five consecutive fires (07-16→07-20)**, still `no-heartbeat`; reinstalling also activates the noon fire, whose first drain **auto-runs the armed v3 dev-set regression gate**. (2) Or run the gate directly: `python3 rules/validation/scorer/dev_set_monitor.py` (real keys, 09:00–23:00 PT, no --force). **v3 is not treated as active until it passes 12/12 with newly_failing=0** — any regression reverts to vProof1.

---

## 1. Where We Are

Broaden Proof 1 finished end-to-end since the last brief. Andy froze the v0.3 held-out set (26 items) on 07-18 and burned the one-shot score on 07-19: **23/26 = 88.5% as-scored** (95% CI [71.0, 96.0]), DUAL-MODEL-CONSENSUS, **α = 1.000** (n=26, perfect model-pair agreement). A signed attorney errata the same day found the frozen ground truth for C-21/C-22 was wrong (§1946.1(b)/*Stancil* governs notice length independently of AB 1482 exemptions — the models were right): **post-errata 25/26 = 96.2%** (CI [81.1, 99.3]), dual-reported, neither number superseded; ground-truth error rate 2/26 = 7.7% logged as its own validation finding. The miss autopsy confirmed exactly one genuine coverage gap (C-18, the §1946.2(a) 12-month just-cause attachment threshold); Andy ratified the rule proposal and **`ca_eviction_v3.json` was cut 07-20** (vProof1 stays byte-frozen as the v0.3 anchor). The regression trigger is armed — the next dev-set run is the gate. Dispatcher-side: still dark (miss ×5). Holdings unchanged: MV=26, CI=4, RC=6.

## 2. Decisions Waiting on Andy (RED list — complete)

**RED-strategic / Andy actions:**
1. **Overnight machine environment — dispatcher miss ×5, `no-heartbeat` (blocks all overnight runs):** `cp rules/validation/com.cjac.validation.plist ~/Library/LaunchAgents/com.cjac.validation.plist` → `launchctl unload` → `launchctl load` → `launchctl list | grep cjac`. Also activates the noon fire → first drain auto-runs the v3 regression gate. Northgate retry #3 (item 14) held until resolved.
2. **v3 dev-set regression gate (new, required):** `python3 rules/validation/scorer/dev_set_monitor.py` — real keys, daytime window. Must be 12/12, newly_failing=0; else Cowork reverts `ACTIVE_RULES_FILE` to vProof1 and reports RED. Until it passes, v3 is ratified-but-unverified.
3. **v0.4 golden-set go/no-go:** next held-out measurement; first batch under the amended freeze protocol (full defect-class sweep per item; no model consultation during ground-truth review). Refill proposal 17.
4. **B-4 plist hardening proposal** (`docs/DISPATCHER_PLIST_PROPOSAL.md`): AbandonProcessGroup recommended; hold pmset-repeat in reserve.
5. **KS/NV/SC CL coverage gap:** Descrybe MCP before accepting Track A as ceiling — Andy's call or GREEN autonomous?
6. **CourtListener bulk-data / rate-limit outreach:** timing is Andy's decision.
7. **Direction C:** still gated — stable score trend + Andy's strategic sign-off.

**RED-interpretive (attorney judgment):**
1. **§1946.2(a)(2) variant verification (carried B4 flag):** ratified from attorney-supplied text, NOT independently verified against verbatim statute text — confirm at next self-critique pass (refill proposal 16).
2. **§1946.1(d) 30-day sale exception:** sole MISSING_RULES_BACKLOG entry — draft only on Andy's direction with attorney-sourced escrow-condition text.
3. **HUMAN_REVIEW_QUEUE standing items:** 43 L7-ESCALATED, 6 RC re-characterizations, 2 CI cheap-confirm (Baer, Houle), CA/summons MODEL-SPLIT (§1167(a) vs §415.45). **No new items this cycle.**
4. **Direction B remaining DRAFT freezes:** CA service ×15, TX notice ×15.
5. **CO W.W.G. Corp. YELLOW:** review before citing CO as having MV holdings support.

**BLOCKED:** overnight runs + automatic D-1 cadence (RED-strategic 1); v3 active status (RED-strategic 2); Direction C (on B trend).

## 3. What Executed Since Last Brief (GREEN digest)

- **07-19 afternoon:** held-out score ingested + verified (provenance SHAs clean); B2 cluster analysis; miss autopsy (C-18 gap CONFIRMED absent; C-21/C-22 hypothesis DISCONFIRMED — exemptions present, correctly scoped); Task 3 correctly stopped per directive.
- **07-19 evening:** signed errata ingested; metrics dual-reported everywhere; corrective freeze protocol adopted (v0.4 forward); Direction B doc amended.
- **07-19 late/night:** rule proposal drafted ratification-ready (attachment threshold, per-tenant inputs, C-19 non-regression check); wiring determination recorded as companion doc; backlog entry created.
- **07-20 ~07:32:** Andy ratified → v3 cut (SHA `65f1d9a4…947c7d`); scorer `ACTIVE_RULES_FILE` updated; 15/15 tests + dry-run wiring clean; trigger armed.
- **This cycle (07-20 report):** overnight scan (miss ×5, no-heartbeat); ledger cycle entry; queue closed out Broaden Proof 1; refills 16–18 proposed; anti-default audit clean.

## 4. Metrics Movement

- **v0.3 held-out (one-shot, BURNED):** 23/26 = **88.5%** as-scored → **96.2%** post-errata (25/26), dual-reported. α = **1.000** (n=26). vs. v0.2 held-out 5/5 = 100% (n=5, directional only) — v0.3 is the first statistically meaningful held-out result.
- **B2 confident-wrong: 3 → 1** post-errata (C-18 only; v3 encodes the fix, unverified until the gate passes). **B3: PENDING-REQUIRED** (first rule change since vProof1). Ground-truth error rate: 2/26 = 7.7% (new metric).
- **Holdings:** MV=26/CI=4/RC=6 unchanged since 07-06; no runs (dispatcher dark).

## 5. Queue Snapshot

- **NOW:** v3 regression gate — armed, waiting on Andy's live run (or plist reinstall → noon auto-run).
- **NEXT:** proposals 16 (self-critique pass over the new element incl. (a)(2) live-source check), 17 (v0.4 drafting, RED-gated), 18 (backlog grooming); carried: 12 (per-call backoff), 14 (Northgate #3, held).
- **BLOCKED:** overnight lane (agent reload); Direction C.

## 6. Pointers (for depth)

- `VALIDATION_METRICS_LEDGER.md` — v0.3 result writeup, errata annotations, v3 version record, cycle entries
- `ERRATA_MEMO_v0_3_20260719.docx` (authoritative) / `.md` — the signed correction instrument
- `AUTOPSY_v0_3_MISSES_20260719.md` — per-item miss analysis + addenda
- `RULE_PROPOSAL_1946_2a_ATTACHMENT_20260719.md` / `WIRING_DETERMINATION_1946_2e_20260719.md` — the ratified pair
- `PROJECT_STATE_OF_RECORD.md` · `HUMAN_REVIEW_QUEUE.md` · `WORK_QUEUE.md` · `DAILY_CHANGELOG.md`

---

*Regenerated every morning-report cycle. Canonical docs win.*
