# A2J AI — Open Infrastructure for Access to Justice

Open-source plugins, rules, skills, and playbooks that make AI genuinely useful for the tens of millions of people who can't afford an attorney.

**Built by:** Andrew M Cohen  
**License:** Apache 2.0 — free to use, modify, and deploy in any context, on any AI model, with attribution  
**Status:** Active development · v0.1 · June 2026

---

## The problem this solves

Every A2J organization that has tried to build AI legal tools faces the same compounding problem: no shared infrastructure, no shared rules layer, no portability across jurisdictions. Each team reinvents what others already built — for a single jurisdiction, in isolation, with no path to scale.

This repository is the shared foundation that ends that pattern.

---

## Repository structure

```
a2j-ai-claude/
├── plugins/            ← Deployable Claude plugins (one per A2J workflow)
│   ├── eviction-defense/
│   └── consumer-debt/
├── rules/              ← Rules / decision logic layer (portable across AI models)
│   ├── schema/         ← JSON schemas (one per workflow)
│   ├── eviction/       ← 50 states + DC (DRAFT)
│   └── validation/     ← Automated validation battery (Layers 1–6)
├── demos/              ← Demo materials by workflow
│   └── eviction/
├── playbooks/          ← Deployment guides for legal aid orgs, courts, clinics
└── docs/               ← Project documentation, status labels, disclaimer
```

### `/plugins` — Workflow Plugins
Deployable Claude plugin packages. Each plugin bundles the skills, prompt logic, and intake workflows for a specific A2J use case. Plugins read from the `/rules` layer — they do not embed the rules directly.

→ [plugins/README.md](plugins/README.md)

### `/rules` — Rules / Decision Logic Layer
Machine-readable JSON files encoding A2J legal decision logic by jurisdiction and workflow. Organized by workflow category, covering all 50 states + DC per workflow. Designed to be portable across AI models — the rules are data, not code.

Currently covers: **eviction notice triage** (51 jurisdictions, DRAFT)  
Planned: debt collection defense, benefits denial appeals, expungement

→ [rules/README.md](rules/README.md)

### `/demos` — Demo Materials
Slides, live demo scripts, and the Rules Comparison Widget showing the difference between raw-LLM legal answers and rules-grounded answers.

→ [demos/README.md](demos/README.md)

### `/playbooks` — Deployment Playbooks
Step-by-step guides for legal aid organizations, courts, and law school clinics deploying these tools.

→ [playbooks/README.md](playbooks/README.md)

---

## The architecture in one paragraph

Anthropic's plugin and MCP connector framework provides the infrastructure layer: Claude as the reasoning engine, Legal Data Hunter and CourtListener as live statutory retrieval connectors. This repository contributes the **content layer**: jurisdiction-specific rules files encoding A2J decision logic, workflow skills, and deployment playbooks. The rules layer is designed to be portable to any AI model — not locked to Claude or Anthropic.

## How to contribute

The highest-value contribution is **attorney validation of the rules files**. Every DRAFT file needs one licensed attorney per state to verify statutory citations and sign off. See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) and [docs/REVIEWER_CHECKLIST.md](docs/REVIEWER_CHECKLIST.md).

## Important disclaimers

All rules files are DRAFT status — AI-generated, not attorney-reviewed. Nothing here constitutes legal advice. See [docs/DISCLAIMER.md](docs/DISCLAIMER.md).

---

*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*
