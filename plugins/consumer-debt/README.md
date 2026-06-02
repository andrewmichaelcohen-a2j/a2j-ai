# Consumer Debt Plugin

Access-to-justice workflows for **consumer debt collection defense**.

When a consumer is sued by a debt buyer or original creditor, several common defenses may apply: the debt may be time-barred, the plaintiff may not be able to prove it owns the debt (chain of title), or the collector may have violated the federal Fair Debt Collection Practices Act (FDCPA) or state consumer protection law. This plugin helps screen a matter for these issues.

## Skills

| Skill | Status | Purpose |
|-------|--------|---------|
| `consumer-debt-validation` | v0.1.0 — draft | Screen a consumer debt collection matter for common defenses and produce a plain-language analysis with citations. |

## Jurisdictions

Jurisdiction-specific data (statutes of limitations, citations, court forms) lives in [`jurisdictions/`](jurisdictions/). Initial target jurisdiction: **Los Angeles County, California**. Additional jurisdictions may be added once the first is validated.

## Scope and limits

This plugin **assists** with screening and analysis. It does not provide legal advice or practice law. Output is intended for review by a supervising attorney before being relied upon. See the skill's own scope and out-of-scope statements.

## Status

Draft (v0.1.0). Not yet validated. Do not rely on output until the skill has been attorney-reviewed and the version reaches v1.0 for your jurisdiction.


---

*Copyright 2026 Andrew M Cohen. Licensed under the [Apache License, Version 2.0](../LICENSE).*