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
Execution status: **ALL SIX ARMS RUN 2026-09-15** (section 11); results provisional pending Andy's audit.

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

## 11. Execution record and provisional results (2026-09-15; pre-audit)

**Runs (all Andy's):** smoke `run_20260915T005504Z` (3 items x 6 arms, $3.54 est.); grounded batch
`run_20260915T140855Z` (G-A 24, G-O 24, G-G 17 -- halted at the $15 per-run cap, $15.11); G-G completion
`run_20260915T152051Z` (7 items, $0.59); R-A `run_20260915T152510Z` (~$8); R-O + R-G `run_20260915T154855Z`
($3.46). **Estimated spend $26.79 + smoke $3.54 = ~$30.3** (runner's price table; the design's ~$20 estimate assumed
900-token answers -- the models wrote 2-3x that, and claude-opus-5's thinking tokens count as output). Andy approved
the overage ("budget approved") before the raw arms ran. Envelope after this experiment: ~$195 of $250.

**Errata found after the freeze (item file untouched; hash unchanged):**
- **L01 (item):** the facts put service on 2026-09-01 (answer due 09-15) but the reference date is 2026-09-17, so the
  deadline had already passed; my ground truth treated it as future and the rubric listed "deadline has passed" as the
  dangerous error. Every arm was judged wrong_dangerous for a correct statement. Excluded from the raw-judge headline
  (n = 23); scored in the audited column on Andy's ruling against the corrected ground truth (results doc, Errata).
- **J-1 (judge prompt):** the judge was not told the reference date, so gpt-5.5 read the L24 answers' correct
  "today is 2026-09-17" arithmetic as an error (G-A/L24, R-A/L24 both marked wrong_dangerous). Fixed in the judge
  prompt for future runs; v1's raw-judge column stands as produced and the audit resolves it.
- **J-2 (judge legal error):** claude-opus-5 judging G-G/L16 asserted a 10-day CCP 703.520 deadline; the node's quoted
  text says 15/20 days, which is what the answer said.
- **J-3 (classification):** gemini judging G-O/L17 classed an over-cautious abstention as wrong_dangerous; Andy's call.
- **G-A/L16:** the model's answer JSON had an unescaped quote and did not parse, so no judgment was made; the answer is
  intact in `answer_raw` and is recovered by `--rejudge` (~$0.10) with a lenient parser now used on the live path too.

**Provisional raw-judge results (n = 23, L01 excluded, before the audit and before the G-A/L16 re-judge):**

| Arm | mean score (95% CI) | DD-wrong | answerable / abstain-correct / trap |
|---|---|---|---|
| G-A (headline grounded system) | 0.909 [0.773, 1.0] (22 scored) | 1 | 0.875 / 1.0 / 0.889 |
| G-O | 0.913 [0.783, 1.0] | 2 | 0.875 / 1.0 / 0.9 |
| G-G | 0.913 [0.783, 1.0] | 0 | 1.0 / 0.8 / 0.9 |
| R-A | 0.783 [0.609, 0.957] | 3 | 0.75 / 1.0 / 0.7 |
| R-O | 0.913 [0.783, 1.0] | 1 | 1.0 / 0.8 / 0.9 |
| R-G | 0.913 [0.783, 1.0] | 2 | 0.875 / 1.0 / 0.9 |

Paired lift (G minus R): claude-opus-5 **+0.136 [-0.045, +0.318]**; gpt-5.5 0.0 [-0.174, +0.174]; gemini-2.5-pro 0.0
[-0.174, +0.174]; pooled **+0.044 [-0.059, +0.147]**. DD-wrong: grounded 3 vs raw 6.

**Reading (provisional; the audited column is the column of record once Andy has ruled):**
- **L1 (lift > 0 for all three, largest on traps): NOT SUPPORTED.** Only the claude pair shows a positive point estimate,
  and its interval includes zero. gpt-5.5 and gemini-2.5-pro raw score the same as grounded on this set.
- **L2 (raw models abstain less / more DD-wrong on abstain-correct items): NOT SUPPORTED on abstention** -- every arm
  handled 4-5 of the 5 abstain-correct items; **weakly supported on DD-wrong overall** (6 vs 3, small counts, several
  of them judge-disputed).
- **L3 (value concentrates in abstention and traps): PARTLY.** Where the corpus demonstrably mattered, it was
  precise-rule items, not folk-legal traps: **L15** (CA single-vehicle "automatic" exemption -- all three raw arms gave a
  wrong 10-day deadline or denied the automatic proceeds rule; all three grounded arms right), **L03** (Reg F five-business-
  day mailbox assumption -- two raw arms early; all grounded right), and **L01** on the limitations half (two raw arms
  computed from last/first-missed payment and called the suit barred; all grounded arms computed from charge-off). The
  folk-legal traps (Henson, "never signed = 2-year", brokerage under the $50k cap, county-court-vs-JP) did not trap
  current frontier models at all.
- **Honest headline for the messaging, pending audit:** "On 23 frozen consumer-debt items, attaching CJaC's v1.0 rules to
  claude-opus-5 raised its score from 0.78 to 0.91 and halved dangerous-direction errors across models (6 to 3), but the
  pooled lift is +0.04 with a confidence interval that includes zero; the demonstrable value is on precise-rule items
  (deadline computation, statutory dollar/day figures) where raw models were confidently wrong." That is the claim the
  data supports; nothing stronger.
- **Lesson for a v2 item set (POST_V1_BACKLOG):** traps must be calibrated against what current frontier models
  actually get wrong (deadline arithmetic, statutory figures, rule-specific mechanics), not against folk-legal errors;
  every item must be date-checked against the reference date mechanically; the judge prompt must carry the reference
  date (done).

**Next:** Andy runs `--rejudge` (G-A/L16) and `--aggregate --live-only`, commits, then rules on the audit sample
(`review/D5_LIFT_AUDIT_SAMPLE.pdf`: 41 entries = all DD-wrong + errata + judge-flagged + a seeded random 20%). Cowork
enters the rulings as `audited_category`, re-aggregates, and the audited column becomes the column of record.

