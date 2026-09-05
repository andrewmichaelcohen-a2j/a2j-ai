# debt-demo-v1.0 census audit -- index and hours estimate

*Phase LOCK item 4 (2026-09-05). Copyright 2026 Andrew M Cohen. Apache 2.0.*

Three audit books, in review order: [federal spine](DEBT_DEMO_V1_AUDIT_federal.md) (6 nodes) ->
[California](DEBT_DEMO_V1_AUDIT_california.md) (7) -> [Texas](DEBT_DEMO_V1_AUDIT_texas.md) (6). Each node sheet has
five parts: **A** logic in full with a per-field correct/wrong box, **B** checklist with keep/change/drop, **C** every
citation with source tier and verification status, **D** disposition history (ledger + drafting revisions + last-run
result), **E** sign-off and tier decision. The books are generated from the frozen files; regenerate with the script in
the DAILY_CHANGELOG entry for this date if the ledger changes.

## What the auditor actually has to read

| | words | notes |
|---|---|---|
| Logic (section A, all 19 nodes) | 27,086 | the content being certified; read in full |
| Checklists (B) | 9,294 | read in full |
| Cited text (C, quoted_text) | 33,677 | NOT read in full -- 114 of 166 entries are live-verified by the checker against the source; the auditor spot-checks the rest |

**Citation verification status at freeze (166 entries):** 114 LIVE-VERIFIED in `run_20260904T221748Z`;
36 MANUAL (`manual_verification` recorded by Cowork, not yet re-confirmed by Andy -- these are the ones to open);
12 added in round 46 after the last run (will be live-checked by the measurement-of-record run; treat as
MANUAL until then); 4 doctrine entries with no url by design.

## Hours -- honest estimate

- Reading A + B critically (36,400 words at ~120 words/min for dense legal text with judgment stops): **~5 h**.
- Citation spot-checks: 48 MANUAL/added rows at ~3 min each (open url, find the quoted text, judge the
  pin): **~2.4 h**. Live-verified rows need only a glance at the cite label.
- Disposition history and last-run results (D), 19 nodes: **~1 h**.
- Sign-off decisions and notes (E), including DD backlog rows: **~1 h**.

**Census audit total: ~10-11 hours**, realistically 3-4 sessions of 2.5-3 h (federal spine ~4 h, California ~3.5 h,
Texas ~3 h). The counsel-queue session (`DEBT_COUNSEL_QUEUE_V1.md`, 27 items) is separate: **~2-3 h**. Both must
finish before any tier promotion (Phase LOCK item 5), so the all-in cost of CJaC's first VALIDATED release is
**~13-14 attorney hours** for 19 nodes -- roughly 40 minutes per node, which is the first AMPVR data point for the
debt track (spec section 3).

## Ground rules during the audit

1. v1.0 is frozen. A wrong field is recorded in the sheet and in `POST_V1_BACKLOG.md`; it is not fixed in place.
2. A node with any DD (dangerous-direction) row open in the backlog is not promoted to VALIDATED by default; if you
   promote it anyway, write why on the sheet.
3. MANUAL citation rows are Cowork's word until you open them. Opening them is the point of the audit.
4. Tier decisions are yours alone. The sheets never suggest one.
