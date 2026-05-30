# A2J Claude Legal Plugins

Open-source [Claude](https://claude.com) plugins and skills for **access to justice (A2J)** — reusable, attorney-authored workflows that help legal aid organizations, law clinics, and self-represented litigants navigate common civil legal problems.

## What this is

This repository is a **plugin marketplace**. Each plugin bundles one or more *skills* — structured, plain-language protocols that an AI assistant follows to perform a specific legal task (intake, screening, analysis, or drafting). Lawyers author the skills; the AI runs them; supervising attorneys review the output.

## Plugins in this marketplace

| Plugin | Status | Description |
|--------|--------|-------------|
| `eviction-defense` | v0.1.0 — DRAFT, attorney validation pending | Eviction notice defect screening and defense identification for CA, TX, and NY. Uses live statute retrieval via MCP connectors. |
| `consumer-debt` | v0.1.0 — in development | Consumer debt collection defense screening and validation. |

More plugins (public benefits screening, expungement, and others) may be added over time.

## Who this is for

- **Legal aid attorneys and paralegals** who want to serve more clients per hour.
- **Law school clinics and pro bono programs** authoring and contributing skills.
- **Court self-help centers** supporting self-represented litigants.
- **A2J coordinating bodies** (such as the Legal Help Commons) curating and validating shared infrastructure.

## Important: this software assists, it does not practice law

Nothing in this repository constitutes legal advice or the practice of law. Every skill is designed to **assist** a person or attorney, not replace professional judgment. Outputs should be reviewed by a supervising attorney before being relied upon or provided to a client. See each skill's scope and out-of-scope statements.

## No client data

This repository contains **no real client information**, and contributions must not introduce any. All examples and test cases are fully fabricated. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Installing

These plugins are installable through Claude Code's plugin marketplace system. Installation instructions will be finalized once the first plugin is validated. (Roughly: add this repository as a marketplace, then install the `consumer-debt` plugin.)

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE). You are free to use, modify, and redistribute, including for adaptation to other jurisdictions, with attribution.

## Status

This is an early-stage project (v0.x). Structure and content will change. Feedback from the A2J community is welcome and encouraged.
