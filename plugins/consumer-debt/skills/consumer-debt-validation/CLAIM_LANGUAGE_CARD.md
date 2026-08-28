# Concept-Demo Claim-Language Card

*One page, keep beside you during any showing. Per `docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md` §8's CONCEPT-DEMO row. Audience: Andy-selected only — not press, not consumers, not a public link.*

---

## Open every showing with this, verbatim

> "This is a demonstration system. Its content is machine-corroborated against cited law — three independent AI models, citations verified against live sources — and not yet attorney-validated. The attorney-validation layer is designed and is what this project is building toward."

Say it early, say it exactly. Don't paraphrase — "machine-corroborated" and "not yet attorney-validated" are the two load-bearing phrases.

## What you MAY say

Always both numbers, always with their basis, always in the same breath:

- **"X% three-model grounded agreement across the demo corpus."** (basis: `grounded_agreement_rate` from the runner's demo-gate metrics — three independent models derived the same answer from cited text alone)
- **"Y of Z scenarios passing against corroborated rules."** (basis: `scenario_pass_rate` — every node a scenario depends on hit CLEAN-PASS in that run)

Both numbers come from the same live run's JSON output (`rules/debt/validation/runs/run_<timestamp>.json`, `demo_gate_metrics` block) — never estimate or round from memory; read them off the actual last run.

Tier labels stay visible on every node you show: **DRAFT** or **CORROBORATED**. Never omit them, never soften them.

## What you may NOT say

- Any bare **"X% accurate"** (accuracy is not what these numbers measure)
- Anything implying **attorney validation** ("reviewed," "checked by a lawyer," "confirmed correct")
- Any **population-accuracy** claim ("this works for X% of cases")
- **"Validated," "near-perfect," five-nines, or 99%-target** language — that language only activates once Phase D (the attorney census audit) actually runs, which hasn't happened yet

## The one boundary case: Band 3 (discretionary judgment calls)

On the default-judgment set-aside scenario (`TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY`), the system deliberately **refuses to predict the outcome**. It names the Craddock three-factor test and the hard 30-day/75-day TRCP 329b filing deadlines, then routes to attorney consultation for the discretionary call. If someone asks "so will the judge grant it" — the honest answer is "the system won't guess, and neither should I; that's what the attorney-review step is for." That refusal is the demo working correctly, not a gap.

## If asked "how do you know it's right"

Answer with the mechanism, not a confidence number: three separately-prompted models derive an answer from the cited statute or regulation text alone (not from each other), an LLM judge checks whether their derivations substantively agree, and every citation is independently fetched and checked against the live government source. That's what "machine-corroborated" means — it is not the same thing as a lawyer having read and approved the output.

---
*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*
