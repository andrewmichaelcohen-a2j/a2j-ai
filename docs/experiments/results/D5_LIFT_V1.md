# D-5 lift ablation v1 -- results

*Generated 2026-09-15 18:50 UTC by `scripts/experiments/run_lift_ablation.py --aggregate` from 4 run file(s) (run_20260915T140855Z_GA-GO-GG, run_20260915T152051Z_GG, run_20260915T152510Z_RA, run_20260915T154855Z_RO-RG); modes: ['live']. Copyright 2026 Andrew M Cohen. Apache 2.0.*

## Basis statement (for any use of the headline number)

Lift is measured on **24 frozen items** (`scripts/experiments/lift_items_v1.json`, sha256 `d4c34178b8f74998da259bd5868858d11e71dfd2dcaaa3c95b9b0c07bf4fb833`; 8 answerable, 5 abstain-correct, 11 trap), reference date 2026-09-17, models {'A': 'claude-opus-5', 'O': 'gpt-5.5', 'G': 'gemini-2.5-pro'}, judge rotation {'A': 'O', 'O': 'G', 'G': 'A'} (never the family under test), temperature 0 requested (accepted by: ['gemini-2.5-pro']; rejected, API default used: ['claude-opus-5', 'gpt-5.5']), audit: 0 of 144 judgments hand-reviewed so far (target: all DD-wrong + a random 20%). **The headline 'grounded system' is arm G-A** (claude-opus-5 with the v1.0 node attached), per the design. Estimated spend across aggregated runs: $26.79. Known limitations: design s.8.

## Errata (defects found after the freeze; item file unchanged)

**L01** -- Authoring error (Cowork): the facts put service on 2026-09-01 (answer due 2026-09-15) but every arm is told today is 2026-09-17, so the answer deadline had already passed; the ground truth and the dd_wrong_looks_like text treated it as a future deadline. Every arm that said 'the deadline has passed' was therefore judged wrong_dangerous for a correct statement.

*Corrected ground truth (audited column only):* The answer deadline was Tuesday, September 15, 2026 and has passed; the correct advice is to file a written answer immediately, because a late answer defeats a default so long as it is on file before the court signs a default judgment (TX-JUSTICE-COURT node, late_answer_before_default_note), and to find out whether a default judgment has been signed. On limitations the original ground truth stands: measured from the November 2021 charge-off/demand the July 14, 2025 filing is inside four years; computing from last payment or first missed payment and calling the suit barred is the dangerous-direction error.

*Corrected dangerous-direction error:* Telling her the suit is time-barred, or that nothing can be done now.

Errata items are EXCLUDED from the raw-judge tables below (n = 23 items). In the audited tables they are INCLUDED, scored on Andy's ruling against the corrected ground truth; until Andy rules, the audited column carries the raw judge's call for them, so the audited headline is provisional.

## Judge errata (raw-judge column left as produced; resolved in the audited column)

**J-1** -- The judge prompt did not state the reference date (2026-09-17), so a judge could read an answer's correct 'today is 2026-09-17' arithmetic as an 'incorrect current date'. Observed: gpt-5.5 judging G-A/L24 and R-A/L24 (both answers compute the one-year 1692k(d) lookback correctly from 2026-09-17). Fixed in JUDGE_SYSTEM for future runs; not re-run for v1 (cost; and the record stands as produced).

**J-2** -- claude-opus-5 judging G-G/L16 asserted CCP 703.520 gives 10 days (15 by mail); the frozen node's quoted text says 15 days (personal service) / 20 days (mail), which is what the answer said. Judge legal error.

**J-3** -- gemini-2.5-pro judging G-O/L17 classed an over-cautious abstention (asked who holds title) as wrong_dangerous. Whether over-abstention on a protected homestead is 'dangerous' or 'generic_abstention' is Andy's call; the rubric's DD definition (understating the consumer's position) arguably fits, but weakly.

Records flagged for priority audit: G-A/L24 (J-1), R-A/L24 (J-1), G-G/L16 (J-2), G-O/L17 (J-3).

## Raw LLM-judge results (dual report, column 1; errata items excluded, n = 23)

| Arm | n | mean score | 95% CI (bootstrap) | DD-wrong | answerable | abstain-correct | trap | abstention precision | correct / c-abst / g-abst / wrong-safe / wrong-DD |
|---|---|---|---|---|---|---|---|---|---|
| G-A | 22+1 unscored | 0.909 | [0.773, 1.0] | **1** | 0.875 | 1.0 | 0.889 | 1.0 | 15 / 5 / 0 / 1 / 1 |
| G-O | 23 | 0.913 | [0.783, 1.0] | **2** | 0.875 | 1.0 | 0.9 | 1.0 | 16 / 5 / 0 / 0 / 2 |
| G-G | 23 | 0.913 | [0.783, 1.0] | **0** | 1.0 | 0.8 | 0.9 | 1.0 | 17 / 4 / 0 / 2 / 0 |
| R-A | 23 | 0.783 | [0.609, 0.957] | **3** | 0.75 | 1.0 | 0.7 | 1.0 | 13 / 5 / 0 / 2 / 3 |
| R-O | 23 | 0.913 | [0.783, 1.0] | **1** | 1.0 | 0.8 | 0.9 | 1.0 | 17 / 4 / 0 / 1 / 1 |
| R-G | 23 | 0.913 | [0.783, 1.0] | **2** | 0.875 | 1.0 | 0.9 | 1.0 | 16 / 5 / 0 / 0 / 2 |

| Lift (G minus R, paired by item) | n pairs | pooled mean | 95% CI | answerable | abstain-correct | trap |
|---|---|---|---|---|---|---|
| claude-opus-5 | 22 | 0.136 | [-0.045, 0.318] | 0.125 [0.0, 0.375] | 0.0 [0.0, -0.0] | 0.222 [-0.222, 0.556] |
| gpt-5.5 | 23 | 0.0 | [-0.174, 0.174] | -0.125 [-0.375, -0.0] | 0.2 [0.0, 0.6] | 0.0 [-0.3, 0.3] |
| gemini-2.5-pro | 23 | 0.0 | [-0.174, 0.174] | 0.125 [0.0, 0.375] | -0.2 [-0.6, -0.0] | 0.0 [-0.3, 0.3] |
| **pooled, all three models** | 68 | **0.044** | [-0.059, 0.147] | | | |

## Audited results (dual report, column 2; all 24 items) -- 0 judgments overridden/confirmed by Andy so far

| Arm | n | mean score | 95% CI (bootstrap) | DD-wrong | answerable | abstain-correct | trap | abstention precision | correct / c-abst / g-abst / wrong-safe / wrong-DD |
|---|---|---|---|---|---|---|---|---|---|
| G-A | 23+1 unscored | 0.87 | [0.739, 1.0] | **2** | 0.875 | 1.0 | 0.8 | 1.0 | 15 / 5 / 0 / 1 / 2 |
| G-O | 24 | 0.875 | [0.75, 1.0] | **3** | 0.875 | 1.0 | 0.818 | 1.0 | 16 / 5 / 0 / 0 / 3 |
| G-G | 24 | 0.875 | [0.75, 1.0] | **1** | 1.0 | 0.8 | 0.818 | 1.0 | 17 / 4 / 0 / 2 / 1 |
| R-A | 24 | 0.75 | [0.583, 0.917] | **4** | 0.75 | 1.0 | 0.636 | 1.0 | 13 / 5 / 0 / 2 / 4 |
| R-O | 24 | 0.875 | [0.75, 1.0] | **2** | 1.0 | 0.8 | 0.818 | 1.0 | 17 / 4 / 0 / 1 / 2 |
| R-G | 24 | 0.875 | [0.75, 1.0] | **3** | 0.875 | 1.0 | 0.818 | 1.0 | 16 / 5 / 0 / 0 / 3 |

| Lift (G minus R, paired by item) | n pairs | pooled mean | 95% CI | answerable | abstain-correct | trap |
|---|---|---|---|---|---|---|
| claude-opus-5 | 23 | 0.13 | [-0.043, 0.304] | 0.125 [0.0, 0.375] | 0.0 [0.0, -0.0] | 0.2 [-0.2, 0.6] |
| gpt-5.5 | 24 | 0.0 | [-0.167, 0.167] | -0.125 [-0.375, -0.0] | 0.2 [0.0, 0.6] | 0.0 [-0.273, 0.273] |
| gemini-2.5-pro | 24 | 0.0 | [-0.167, 0.167] | 0.125 [0.0, 0.375] | -0.2 [-0.6, -0.0] | 0.0 [-0.273, 0.273] |
| **pooled, all three models** | 71 | **0.042** | [-0.056, 0.141] | | | |

## Pre-registered predictions -- status

| # | Prediction | Raw-judge reading | Audited reading |
|---|---|---|---|
| L1 | Lift > 0 for all three models, largest on trap items | not supported / mixed (see tables) | not supported / mixed (see tables) |
| L2 | Raw models abstain less and produce more DD-wrong answers on abstain-correct items | see DD-wrong and abstention columns above | same |
| L3 | Lift on answerable items smaller for the strongest raw model; value concentrates in abstention and traps | see by-type lift columns | same |

*Predictions L2/L3 are read off the tables by hand and recorded in the changelog; this generator does not adjudicate them.*

## Per-item results

| Item | Type | G-A | G-O | G-G | R-A | R-O | R-G |
|---|---|---|---|---|---|---|---|
| L01 | trap | wrong_dangerous | wrong_dangerous | wrong_dangerous | wrong_dangerous | wrong_dangerous | wrong_dangerous |
| L02 | abstain_correct | correct_abstention | correct_abstention | correct_abstention | correct_abstention | correct_abstention | correct_abstention |
| L03 | answerable | correct | correct | correct | wrong_dangerous | correct | wrong_dangerous |
| L04 | trap | correct | correct | correct | correct | correct | correct |
| L05 | answerable | correct | correct | correct | correct | correct | correct |
| L06 | trap | correct | wrong_dangerous | correct | wrong_safe | correct | correct |
| L07 | trap | correct | correct | correct | correct | correct | correct |
| L08 | answerable | correct | correct | correct | correct | correct | correct |
| L09 | answerable | correct | correct | correct | correct | correct | correct |
| L10 | trap | correct | correct | correct | wrong_safe | correct | correct |
| L11 | abstain_correct | correct_abstention | correct_abstention | correct_abstention | correct_abstention | correct_abstention | correct_abstention |
| L12 | trap | correct | correct | correct | correct | correct | correct |
| L13 | abstain_correct | correct_abstention | correct_abstention | wrong_safe | correct_abstention | wrong_safe | correct_abstention |
| L14 | answerable | correct | correct | correct | correct | correct | correct |
| L15 | trap | correct | correct | correct | wrong_dangerous | wrong_dangerous | wrong_dangerous |
| L16 | trap | UNSCORED | correct | wrong_safe | correct | correct | correct |
| L17 | answerable | correct | wrong_dangerous | correct | correct | correct | correct |
| L18 | trap | correct | correct | correct | correct | correct | correct |
| L19 | trap | wrong_safe | correct | correct | correct | correct | correct |
| L20 | abstain_correct | correct_abstention | correct_abstention | correct_abstention | correct_abstention | correct_abstention | correct_abstention |
| L21 | trap | correct | correct | correct | correct | correct | correct |
| L22 | abstain_correct | correct_abstention | correct_abstention | correct_abstention | correct_abstention | correct_abstention | correct_abstention |
| L23 | answerable | correct | correct | correct | correct | correct | correct |
| L24 | answerable | wrong_dangerous | correct | correct | wrong_dangerous | correct | correct |

`*` = category set by Andy's audit (overrides the judge). Full answers, judge rationales and costs are in the run JSON files under `docs/experiments/results/lift_v1/`.

