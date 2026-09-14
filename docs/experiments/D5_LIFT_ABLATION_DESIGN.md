# D-5 lift ablation -- CJaC-grounded vs. raw frontier models: pre-registration

*Phase EXPERIMENT item 7 of the 2026-09-05 LOCK directive; first D-5 data point per DIRECTION_D_ROADMAP.md.
DESIGN ONLY -- no execution until the item set is frozen and Andy approves the budget. Copyright 2026 Andrew M
Cohen. Apache 2.0.*

**Status:** PRE-REGISTERED 2026-09-05 (design); **PROMOTED to demo-gating and resequenced ahead of the configuration
ablation by the 2026-09-05 Addendum (s.3)**; amended 2026-09-14 (budget itemized per arm; grounded-system designation;
replay-first accounting). **APPROVED 2026-09-14 -- Andy: "i approve the $30 lift."** **ITEM SET FROZEN 2026-09-14:**
`scripts/experiments/lift_items_v1.json`, 24 items, sha256
`d4c34178b8f74998da259bd5868858d11e71dfd2dcaaa3c95b9b0c07bf4fb833`, recorded in `scripts/ci/frozen_artifact_manifest.json`
(CI-enforced) BEFORE any arm ran; the runner (`scripts/experiments/run_lift_ablation.py`) refuses `--live` if the hash
drifts. Review copy for Andy: **double-click `review/D5_LIFT_ITEMS_V1.pdf`** (one item per page, notes field).
Execution status: **awaiting Andy's smoke run** (section 10).

## 1. Question

On consumer-debt questions inside the v1.0 corpus's scope, how much better does a model answer WITH CJaC's
rules attached than the same model answers on its own -- and does the grounded system abstain correctly (ask
for the missing dispositive fact) where the raw model guesses?

## 2. Arms (6)

| Arm | System | Rules attached |
|---|---|---|
| G-A | claude-opus-5 | the relevant v1.0 node(s) as context, with the completeness checklist and the instruction to abstain and ask when a dispositive fact is missing |
| G-O | gpt-5.5 | same |
| G-G | gemini-2.5-pro | same |
| R-A | claude-opus-5 | none -- the question alone, same abstention instruction |
| R-O | gpt-5.5 | none |
| R-G | gemini-2.5-pro | none |

Same prompt shell, same temperature (0), same item text, model identifiers frozen at execution. Node
selection for the G arms is by the item's declared `depends_on_node_ids` (as in `scenarios.json`), not by
retrieval -- retrieval quality is a separate question and is held constant by construction.

## 3. Items

- The 5 existing demo scenarios (`scripts/corroboration/scenarios.json`), each expanded into a concrete fact
  pattern.
- A Cowork-drafted expanded set of **15-20 items** across the 19 nodes (AS FROZEN 2026-09-14: 19 new items + the 5
  expanded scenarios = 24 items covering all 19 nodes; mix 8 answerable / 5 abstain-correct / 11 trap -- traps
  over-weighted because predictions L1-L3 locate the value there; the answerable items are the control), three item types in fixed
  proportion: **(i) answerable** -- all dispositive facts given, one correct answer derived from v1.0 content;
  **(ii) abstain-correct** -- a dispositive fact deliberately withheld, the correct response is to identify and
  ask for it; **(iii) trap** -- a fact pattern where the folk-legal answer is wrong and the v1.0 node says why
  (drawn from the dangerous-direction ledger rows: e.g., "they never sent a signed contract so it's the 2-year
  period", "the judgment is 10 years old so it's dead", "single vehicle so nothing to file").
- Each item carries: facts, the question, the v1.0 node(s) it depends on, the ground-truth answer or the
  ground-truth missing fact, and the DD flag. Ground truth is derived ONLY from frozen v1.0 content; where
  the node's answer depends on a GLOSS-FOR-COUNSEL proposition, the item is excluded until the counsel ruling.
- **Freeze:** the item file is committed with its sha256 recorded here and in `frozen_artifact_manifest.json`
  BEFORE any arm runs. Items are burned after one use for headline reporting (house rule); re-use is allowed
  only for D-5 trend tracking against new model generations, stated as such.

## 4. Scoring (abstention-credit, house rules)

| Response | Answerable item | Abstain-correct item |
|---|---|---|
| Correct answer (matches ground truth) | 1 | -- |
| Correct abstention (names the missing dispositive fact) | 0.5 | 1 |
| Abstains without naming the fact / generic "see a lawyer" | 0.25 | 0.5 |
| Wrong answer, safe direction (overstates the consumer's position) | 0 | 0 |
| Wrong answer, DANGEROUS direction | 0, and counted separately | 0, counted separately |

Scored by an LLM judge from a family not under test for that item (rotating), with rubric and ground truth in
the judge prompt; **Andy audits 20% of judgments (all DD-wrong calls plus a random sample)**; results
dual-reported (raw judge, audited). The DD-wrong COUNT is reported alongside the score -- a system that scores
0.7 with zero dangerous-direction errors and one that scores 0.7 with six are not the same system.

## 5. Lift

Lift(model) = mean score(G-model) - mean score(R-model), per model and pooled, with 95% bootstrap intervals
over items; reported per item type. The headline "lift number" is the pooled figure with its basis stated in
the same sentence (n items, item mix, judge, audit rate, model versions, date). Also reported: DD-wrong counts
per arm; abstention precision (of abstentions, share that named the right fact); the per-item table.

## 6. Predictions (pre-registered)

L1. Lift > 0 for all three models, largest on trap items.
L2. Raw models abstain less and produce more DD-wrong answers on abstain-correct items.
L3. Lift on answerable items is smaller for the strongest raw model; the corpus's value concentrates in
abstention and traps.

## 7. Budget and gating (itemized per arm -- Addendum s.1 replay-first rule)

Nothing in this experiment can run on recorded fixtures: every arm requires fresh model output on items that
did not exist before. So every call below is live, itemized, and gated.

| Arm | Calls | Est. tokens/call (in+out) | Est. $ |
|---|---|---|---|
| G-A grounded claude-opus-5 | 25 | ~6K in (node context) + 1K out | ~$3.50 |
| G-O grounded gpt-5.5 | 25 | same | ~$3.00 |
| G-G grounded gemini-2.5-pro | 25 | same | ~$1.50 |
| R-A raw claude-opus-5 | 25 | ~0.5K in + 1K out | ~$2.00 |
| R-O raw gpt-5.5 | 25 | same | ~$1.50 |
| R-G raw gemini-2.5-pro | 25 | same | ~$0.75 |
| Judge (rotating family, 150 judgments) | 150 | ~3K in + 0.3K out | ~$6.00 |
| Smoke (3 items x 6 arms + judge) | 24 | -- | ~$2.00 |

**Total estimate ~$20; proposed cap $30 (APPROVED 2026-09-14)**. Runner's own pre-run estimate on the frozen 24-item set
(price table of record printed with every run; chars/4 input, 900-token answers, 350-token judgments): grounded batch
$11.33 (G-A 5.63, G-O 3.12, G-G 2.58), raw batch $6.25 (R-A 2.86, R-O 1.28, R-G 2.12), smoke $2.03; total **~$19.60** (single tranche; per-run cap $15 respected by running arms as two
batches of three). Runs are Andy's, smoke first. Preconditions: item file frozen with hash; calibration green;
measurement-of-record recorded (done 2026-09-05). **"The grounded system" for the headline** is arm G-A
(claude-opus-5 with the v1.0 node attached) -- the configuration the demo skill runs; G-O and G-G are reported
alongside as robustness checks, not as the headline.

## 8. Known limitations (stated wherever results are reported)

One corpus, two states plus the federal spine; items authored by the same team that authored the corpus
(mitigated by the trap design and the audit, not eliminated); LLM-judged with partial attorney audit; node
selection by declaration rather than retrieval; model versions of record only. Findings about v1.0 content
surfaced by this experiment go to `POST_V1_BACKLOG.md`.

## 9. Deliverable

`docs/experiments/results/D5_LIFT_V1.md`: the lift table, the DD-wrong counts, the per-item results, the
audit reconciliation, and the one-paragraph basis statement for the messaging.

## 10. Execution protocol (added 2026-09-14 on approval)

Runner: `scripts/experiments/run_lift_ablation.py` (reuses the corroboration runner's key loading, JSON parsing and
model identifiers; temperature 0 where the API accepts it; judge rotation A->O, O->G, G->A; scoring table of section 4
encoded; bootstrap CIs over items; dual-report writer; audit-sample export). Dry-run exercised end to end 2026-09-14
(144 synthetic judgments; no API calls). No corroboration-runner change in this round (one-variable rule holds).

Order, all runs Andy's, from the repo root, each under the $15 per-run cap:

1. `python3 scripts/experiments/run_lift_ablation.py --live --smoke` -- 3 items x 6 arms + 18 judgments, ~$2. Confirms
   keys, JSON parsing on all three families, judge parsing. Inspect the printed categories; if any arm returns
   `UNSCORED` for all three items, stop and report before spending more.
2. `python3 scripts/experiments/run_lift_ablation.py --live --batch grounded` -- G-A, G-O, G-G, 24 items, ~$11.
3. `python3 scripts/experiments/run_lift_ablation.py --live --batch raw` -- R-A, R-O, R-G, 24 items, ~$6.
4. `python3 scripts/experiments/run_lift_ablation.py --aggregate --live-only` -- writes
   `docs/experiments/results/D5_LIFT_V1.md` (raw-judge and audited columns) and
   `docs/experiments/results/lift_v1/AUDIT_SAMPLE.md` (every DD-wrong call + a seeded random 20%). Commit the run JSONs,
   the summary and the audit sample (GitHub Desktop).
5. Andy's audit: rule on each audit-sample entry (confirm / override); Cowork enters the rulings as `audited_category` /
   `audit_note` in the run JSON and re-runs step 4. The audited column is the column of record; the raw-judge column
   is always reported beside it.

The smoke run's records are excluded from aggregation by default (`--include-smoke` to override) so the headline is
computed on the full batches only. Smoke + batches use the same frozen items, so the three smoke items are answered
twice by each arm; the batch answer is the one of record.

Budget accounting: envelope $250; ~$165 spent through the measurement of record; this experiment ~$20 (cap $30) ->
~$185-195 after completion. The configuration ablation remains unfunded pending the trim decision.

