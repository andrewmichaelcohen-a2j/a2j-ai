# CJAC_METHOD_V1 -- configuration ablation: pre-registration

*Phase EXPERIMENT item 6 of the 2026-09-05 LOCK directive. DESIGN ONLY -- no execution until Andy's go on the
live-call budget below. Copyright 2026 Andrew M Cohen. Apache 2.0.*

**Status:** PRE-REGISTERED 2026-09-05. Any change to arms, metrics, ground truth, or analysis after execution
begins is recorded as an amendment with its date and reason, never silently.

## 1. Question

Which stages of the corroboration pipeline earn their cost? Specifically: how much of the pipeline's ability to
surface real defects in a rules node comes from (i) multiple model families, (ii) a separate adversarial pass,
(iii) grounding (giving models only the cited source text) -- and what does each configuration cost in API
dollars and in human triage minutes per node?

## 2. Ground truth (fixed before any arm runs)

- **Defect ledger:** `rules/debt/validation/stage_b_dispositions.json` at the `debt-demo-v1.0` tag -- 120
  node-specific dispositions plus 4 cross-cutting. Each carries `classification` and `dangerous_direction`.
  A ledger entry is a **known real defect** if its classification begins with FIXED (VERIFIED or SOURCE-NAMED)
  or is GLOSS-FOR-COUNSEL; it is a **known non-defect** if NOT-A-GAP or COVERED; HORIZON entries are excluded
  from both sets (real but out of scope).
- **Test articles (defect-bearing corpus snapshots), SHA-preserved in git:**
  - **T38** = the 19 demo nodes at commit `27d5d44` (round 37, 2026-09-02) -- the content that carried the 58
    round-38 findings (ledger entries with source "round 38" / `run_20260903T174510Z`).
  - **T46** = the 19 demo nodes at commit `b3d95db` (round 45, 2026-09-05) -- the content that carried the 46
    round-46 findings (`run_20260904T221748Z`).
  Each test article's defect set is the ledger entries whose source run was performed on that content.
  T38: 58 entries (15 nodes). T46: 46 entries (16 nodes). Materiality weight: DD = yes -> 2, otherwise 1.
- **Calibration fixtures:** the 14 replay fixtures (CAL-01..14) are used to confirm each arm's code path
  parses and scores before any live call; they are not part of the catch-rate denominator.
- **Fixed-bug history:** `DAILY_CHANGELOG.md` rounds 9-45 -- used only for the cost-of-alignment estimate
  (section 5), not for scoring.

## 3. Arms

All arms run on the SAME test articles with the SAME adversarial output schema (the round-44 three-flag
schema; see 3.1) so findings are comparable. Model identifiers frozen at execution time and recorded.

| Arm | Derivation | Verification / adversarial | Grounding |
|---|---|---|---|
| **(a)** single + self-critique | claude-opus-5 grounded derivation | same model, structured self-critique prompt (the Stage B prompt addressed to its own derivation) | enforced |
| **(b)** single + cross-family adversarial | claude-opus-5 grounded derivation | gemini-2.5-pro runs the Stage B prompt | enforced |
| **(c)** two-model draft/verify | claude-opus-5 grounded derivation | gpt-5.5 grounded re-derivation + LLM judge + gpt-5.5 Stage B | enforced |
| **(d)** tri-model consensus (current pipeline) | 3 families grounded derivation + judge | claude-opus-5 Stage B | enforced |
| **(e)** ungrounded control | winner of (a)-(d), same models, source text WITHHELD (models answer from training knowledge given only the node's cite labels) | as winner | none |

**3.1 Finding-format variable (held round 47).** The pipeline currently asks for three yes/no flags per edge
case and every node returns three material findings. Arm (d) is additionally run once with the round-47
schema (severity rank 1-5 + "must-fix for a careful legal-aid attorney" flag) on T46 only, to measure whether
the format changes catch rate or false-flag rate. This is the only place round 47 enters before v1.1.

## 4. Metrics (per arm, per test article)

1. **Catch rate** = sum of weights of known real defects the arm reports / sum of weights of all known real
   defects. A defect is "reported" when a finding substantially overlaps the ledger entry's theme -- decided
   by an LLM matcher (a model family NOT used in the arm) given the finding and the ledger entry, with
   Cowork reviewing every match and every near-miss and Andy spot-checking 20% of matches. Matcher decisions
   are archived.
2. **False-flag rate** = findings that match a NOT-A-GAP/COVERED ledger entry, or that Cowork+Andy classify
   as non-material on review, / total findings. This is the alignment-cycle cost driver.
3. **New-defect yield** = material findings that match no ledger entry (reported, classified, and sent to
   `POST_V1_BACKLOG.md` -- v1.0 content untouched).
4. **API cost per node** from `_usage` tokens x published per-token prices at execution date, plus
   citation-check cost (zero) -- recorded per stage.
5. **Projected human minutes per node** = findings x observed triage minutes per finding (rounds 38-46:
   Cowork ~12 min/finding to source-pin and disposition; Andy's audit ~40 min/node from the census estimate)
   + fixed review overhead.
6. **Stage A agreement and citation verification** reported alongside for arms that have them.

Dual-reported: raw and after matcher review, per house rule.

## 5. Replay-first execution plan and budget

- **Zero-cost first:** arm (d) on T38 and T46 already exists as `run_20260903T174510Z` and
  `run_20260904T221748Z`. Their findings are matched to the ledger offline -> arm (d) catch and false-flag
  rates without a single new call. The matcher itself is the first live spend (~$3).
- **Snapshot loading:** runner gains `--corpus-ref <git-ref>` (reads node JSON from `git show <ref>:<path>`)
  and `--config a|b|c|d` and `--ungrounded`; all replay-tested against the 14 fixtures before live use
  (calibration must be green -- constraint).
- **Smoke:** each new arm on 3 nodes of T46 first (~$1 per arm).
- **Live budget proposal (cap):** arms (a), (b), (c), (e) x 2 test articles x 19 nodes at $0.20-0.35/node
  ≈ $45; arm (d) round-47 variant on T46 ≈ $9; matcher and judge calls ≈ $6. **Proposed cap: $70**, in
  four gated tranches (offline matcher $3 -> smoke $5 -> T46 arms $30 -> T38 arms $30), each needing Andy's
  go and run by Andy. Per-run estimates printed before every run as today.

## 6. Pre-registered predictions (so the result can disagree with us)

P1. Cross-family adversarial (b) catches materially more than self-critique (a) on the same model.
P2. The tri-model consensus stage (d vs c) adds little to CATCH rate (Stage A has been 100% for weeks) but is
what produces the citation-verified derivation record; its value is evidentiary, not defect-finding.
P3. The ungrounded arm (e) produces MORE findings and a HIGHER false-flag rate (it hallucinates rules and then
"finds" the node disagrees with them) and misses the citation-transcription defects entirely.
P4. The severity-rank format lowers false-flag rate without lowering catch rate on DD defects.
If P2 holds, the recommended scaling configuration is (b) or (c) for defect-finding with (d)'s derivation
record generated once per release, not per iteration.

## 7. Analysis and reporting

Per arm and test article: the four rates with n, cost per node, projected minutes per node, and the DD-only
catch rate. A single table, plus the cost curve: cumulative API dollars and human minutes per validated node
under each configuration. Results reported regardless of outcome; if an arm's code path fails, the failure is
the result for that arm and is reported as such.

**Deliverable:** `docs/CJAC_METHOD_V1.md` -- written for an external technical reader (a clinic, a lab, a
replicating team): the pipeline as a recipe (inputs, stages, prompts by reference, gate definitions), the
evidence table above ranking what each stage earns, the recommended configuration for scaling with its cost
per validated node, the known limitations (one corpus, one jurisdiction pair, model versions of record), and
the replication procedure (this repo, these commands, this budget).

## 8. Constraints restated

One-variable rule. No live runs by anyone but Andy; smoke first. v1.0 is immutable -- experiment findings about
v1.0 content go to `POST_V1_BACKLOG.md`. Calibration green before any experiment code runs live. Budget caps and
per-run estimates as above. This document is amended, never overwritten.
