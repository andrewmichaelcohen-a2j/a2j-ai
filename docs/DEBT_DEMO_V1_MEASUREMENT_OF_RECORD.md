# debt-demo-v1.0 -- measurement-of-record procedure

*Phase LOCK item 2 (2026-09-05). Copyright 2026 Andrew M Cohen. Apache 2.0.*

**Purpose.** One final live run of the corroboration pipeline against the frozen v1.0 corpus, under the ratified
gate (spec section 8: Stage A grounded agreement >= 90%, citation verification >= 90%, zero undispositioned
material Stage B findings; Stage B parse health reported alongside). The run's JSON is the frozen evidentiary
record for v1.0 and sits in the ledger next to eviction Proof 1.

**Fixed configuration for the record.** Runner at round 45 (streaming transport; 16000-token Stage B base;
materiality from the two flags; `_global` dispositions on). Content at the `debt-demo-v1.0` tag. Ledger at 120
node-specific + 4 cross-cutting entries. No runner change lands between the smoke and the full run (one-variable
rule); round 47 (severity ranking) is held until after this run and is folded into the EXPERIMENT phase.

## Step 0 -- preconditions (Andy)

1. Round 46 (four patches) and the LOCK patch series applied and pushed. `python3 scripts/ci/check_frozen_artifacts.py`
   prints `PASS: all 9 frozen artifact(s)`.
2. Tag the locking commit and push the tag (tag creation in terminal is fine; GitHub Desktop pushes tags with
   "Push origin" -- confirm on the repository's Tags page afterwards):

```
cd ~/Developer/a2j-ai && git tag -a debt-demo-v1.0 -m "debt-demo-v1.0: 19 demo-corpus nodes frozen 2026-09-05 per LOCK directive; manifest rules/debt/validation/debt_demo_v1.0_manifest.json"
```

3. Calibration green: `python3 scripts/ci/check_corroboration_calibration.py` prints PASS (14 fixtures).

## Step 1 -- smoke (3 nodes, ~$1.35)

```
cd ~/Developer/a2j-ai && python3 scripts/corroboration/run_corroboration.py --live --nodes FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6,CA-SOL-WRITTEN-CONTRACT-DEBT,TX-SOL-CONSUMER-DEBT
```

Pass condition to proceed: Stage A 100%, Stage B parse-success 100% (no "Streaming is required" or
max_tokens errors -- this is the first live exercise of the round-45 transport), citation verification 100% on
these three (COVERAGE and CA-SOL-WRITTEN carry manual-verification entries; TX-SOL carries the new 16.066 entry).
If any of those fail, stop and send the JSON; do not run the full corpus.

## Step 2 -- full run (19 nodes, ~$8.55)

```
cd ~/Developer/a2j-ai && python3 scripts/corroboration/run_corroboration.py --live --demo-corpus-only
```

Send the JSON. Do not re-run to "improve" it: the first complete run under the fixed configuration is the record.
(A run that fails for an infrastructure reason -- credits, 529s across many nodes -- is not a record; it is
re-run after the cause is fixed, and both JSONs are kept.)

## Step 3 -- recording (Cowork, same day)

1. The run JSON stays committed under `rules/debt/validation/runs/`. Its sha256, run_id, and the four gate
   numbers are appended to `rules/debt/validation/debt_demo_v1.0_manifest.json` under `measurement_of_record`,
   and the JSON path is added to `scripts/ci/frozen_artifact_manifest.json` (frozen like Proof 1).
2. Every material Stage B finding in the run is classified (materiality, dangerous direction) and recorded in
   `docs/POST_V1_BACKLOG.md` and in the ledger with classification `BACKLOG-V1.1`. No v1.0 content changes.
3. The record is written up in `DEBT_STAGE_B_TRIAGE.md` and the changelog with the gate reported TWO ways
   (see the conflict below), never one.

## Conflict flagged -- the gate's third leg on a saturating generator

The ratified gate requires **zero undispositioned material findings**. Every parsed node in the last full run
returned exactly three material findings, all real, and round 46 dispositioned them; the generator will very
likely return three more per node on the frozen corpus. Under the LOCK directive those go to the backlog
untouched. So the record's `internal_gate_met` will read **False** on the third leg even if Stage A and
citations clear 90%, and the backlog will hold ~40-50 rows the day it is created.

Two honest readings, and the record carries both:

- **Raw:** the JSON's own `internal_gate_met` and `undispositioned_material_findings.count`, as computed.
- **Backlog-dispositioned:** the same findings after Cowork classifies each into the backlog (which IS a
  disposition under the spec's definition -- "dispositioned by a human or by a content round as FIXED /
  GLOSS / COVERED / OUT-OF-SCOPE / HORIZON"; `BACKLOG-V1.1` is the OUT-OF-SCOPE-for-this-release class). On
  this reading the third leg is met on paper, not by a re-run.

**Andy decides which reading the v1.0 claim card uses.** Cowork's recommendation: dual-report, lead with the
raw number, and let the claim be "N findings surfaced and dispositioned, dangerous-direction first" with the
backlog count stated -- that sentence is true on both readings. What Cowork will NOT do is re-run the corpus
after backlog classification to manufacture a `True`; that would be a second measurement, not the record.

## Other conflicts flagged against repo reality

- **Freeze point.** Origin HEAD at the time of the directive is round 45; round 46's four patches (which
  disposition the last run's 46 findings) are delivered but unapplied. The LOCK series is built on top of 46.
  Freezing at 45 instead would put 46 known, fixed findings back into the record as undispositioned. The
  manifest hashes assume 46 is applied first.
- **Tier promotion vs. file freeze.** Promoting a node's `tier` field (item 5) edits a frozen file and will
  fail CI until the manifest hashes are updated. That is intended: promotion is a deliberate re-freeze by Andy,
  recorded with new hashes in the same commit.
- **Round 47.** The severity-rank prompt change Andy approved earlier today is held: landing it before the
  measurement run would change the measured configuration. It becomes configuration variable in the
  EXPERIMENT phase's ablation design.
