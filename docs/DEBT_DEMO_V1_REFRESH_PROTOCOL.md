# debt-demo-v1.0 -- quarterly re-verification (freshness) protocol

*Addendum 2026-09-05, s.4 (minimal manual refresh). Written 2026-09-14. Copyright 2026 Andrew M Cohen. Apache 2.0.*

**Commitment.** Every 90 days from the measurement-of-record date (2026-09-05), the citation checker is run
across every url-bearing citation pin in the frozen v1.0 corpus. Any pin that no longer verifies (page moved,
text changed, section renumbered) is recorded in `docs/POST_V1_BACKLOG.md` as a **FRESHNESS** row with the
diagnostics, and in the ledger as `BACKLOG-V1.1` (or the then-current backlog class). Nothing is edited in the
frozen release; a failed pin is a disclosure, not a fix. Due dates: **2026-12-04, 2027-03-04, 2027-06-02, ...**
(recorded in the manifest under `freshness_commitment`).

**Procedure (Andy runs; Cowork records).**

1. Calibration green: `python3 scripts/ci/check_corroboration_calibration.py`.
2. Run the checker across the demo corpus. *Runner note (flagged):* the runner has `--skip-citation-check`
   but no citation-only mode today. Until a `--citation-check-only` flag lands (a one-line runner round, held
   for the next runner window; the citation checker makes no model calls, so that mode costs $0 in API spend),
   the protocol is a full demo-corpus pass at the standing estimate (~$8.55) -- or, cheaper, a `--nodes` pass
   on the nodes whose pins are known to be fragile (statutes.capitol.texas.gov, leginfo multi-version
   sections). Command once the flag exists:
   `cd ~/Developer/a2j-ai && python3 scripts/corroboration/run_corroboration.py --live --demo-corpus-only --citation-check-only`
3. Send the JSON. Cowork writes the FRESHNESS rows, appends the run id and citation-verification percentage
   to the manifest's `freshness_commitment.history`, and notes it in the changelog.
4. A pin that fails for a permanent reason (site gone) is re-pinned in the next content release, never in v1.0.

**What it is not.** Not a statute-watch (D-3, HORIZON: a self-generating watchlist from the citation pins
that checks for amendments, not just reachability). This protocol proves the pinned text is still where the
release says it is; it does not detect that the law changed while the page stayed put. That gap is stated in
the certification statement's scope limitation.
