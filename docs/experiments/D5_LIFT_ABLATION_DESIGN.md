# D-5 lift ablation -- CJaC-grounded vs. raw frontier models: pre-registration

*Phase EXPERIMENT item 7 of the 2026-09-05 LOCK directive; first D-5 data point per DIRECTION_D_ROADMAP.md.
DESIGN ONLY -- no execution until the item set is frozen and Andy approves the budget. Copyright 2026 Andrew M
Cohen. Apache 2.0.*

**Status:** PRE-REGISTERED 2026-09-05 (design). The item set is NOT yet drafted; it is frozen (committed with
hashes) before any arm runs, and this document is amended to record the freeze commit.

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
- A Cowork-drafted expanded set of **15-20 items** across the 19 nodes, three item types in fixed
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

## 7. Budget and gating

~25 items x 6 arms = 150 completions at ~$0.05-0.15 = ~$15; judge ~150 calls ≈ $6; **proposed cap $30**, run
by Andy, smoke first (3 items x 6 arms ≈ $2). Requires: item file frozen; calibration green; the measurement-
of-record run complete (so v1.0 is the ground truth of record).

## 8. Known limitations (stated wherever results are reported)

One corpus, two states plus the federal spine; items authored by the same team that authored the corpus
(mitigated by the trap design and the audit, not eliminated); LLM-judged with partial attorney audit; node
selection by declaration rather than retrieval; model versions of record only. Findings about v1.0 content
surfaced by this experiment go to `POST_V1_BACKLOG.md`.

## 9. Deliverable

`docs/experiments/results/D5_LIFT_V1.md`: the lift table, the DD-wrong counts, the per-item results, the
audit reconciliation, and the one-paragraph basis statement for the messaging.
