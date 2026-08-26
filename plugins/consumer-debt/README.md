# Consumer Debt Plugin

Access-to-justice workflows for **consumer debt collection defense**.

When a consumer is sued by a debt buyer or original creditor, several common defenses may apply: the debt may be time-barred, the plaintiff may not be able to prove it owns the debt (chain of title), or the collector may have violated the federal Fair Debt Collection Practices Act (FDCPA) or state consumer protection law. This plugin helps screen a matter for these issues.

## Skills

| Skill | Status | Purpose |
|-------|--------|---------|
| `consumer-debt-validation` | v0.2.0 — CONCEPT-DEMO | Screen a consumer debt collection matter for common defenses and produce a plain-language analysis with citations, tier labels visible throughout. |

## Jurisdictions

**Superseded 2026-08-26** by the schema-validated node corpus in `../../rules/debt/` (federal
spine + TX/CA for demo reliance; UT/AZ/NY exist as visible DRAFT content, not yet relied on). The
original plan to hand-author jurisdiction data as plain markdown in [`jurisdictions/`](jurisdictions/)
was never executed and is now inactive — see the skill's own "Reconciliation note." The folder is
left in place rather than deleted.

## Scope and limits

This plugin **assists** with screening and analysis. It does not provide legal advice or practice law. Output is intended for review by a supervising attorney before being relied upon. See the skill's own scope, claims-discipline, and out-of-scope statements.

## Status

CONCEPT-DEMO (v0.2.0), per the 2026-08-26 "Concept Demo First" directive. Every underlying node is
DRAFT tier pending `scripts/corroboration/run_corroboration.py`; none is CORROBORATED or VALIDATED.
Do not rely on output, and see the skill's claims-discipline section before any live showing.


---

*Copyright 2026 Andrew M Cohen. Licensed under the [Apache License, Version 2.0](../LICENSE).*