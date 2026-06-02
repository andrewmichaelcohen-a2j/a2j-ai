# Plugins

Deployable Claude plugin packages — one per A2J workflow.

Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.

---

## What a plugin is

Each plugin bundles the skills, intake prompts, and workflow logic for a specific A2J use case. Plugins are the "how to reason about this legal task" layer — they read from the `/rules` decision-logic layer but do not embed the rules directly. This separation means:

- Rules can be validated independently and shared across plugins
- Plugins can be updated without touching the rules
- The same rules can power different plugins for different audiences (e.g., a legal-aid-intake version and a self-represented-litigant version of the same workflow)

## Current plugins

| Plugin | Workflow | Status |
|--------|---------|--------|
| `eviction-defense/` | Eviction notice triage — defect detection, affirmative defenses, referral | v0.1 DRAFT |
| `consumer-debt/` | Consumer debt collection defense — FDCPA, SOL, chain-of-title | v0.1 skeleton |

## Adding a new plugin

1. Create a new folder: `plugins/{workflow-name}/`
2. Add `.claude-plugin/plugin.json` — plugin metadata
3. Add `skills/{skill-name}/SKILL.md` — the workflow instruction file
4. Reference the appropriate rules files from `/rules/{workflow}/`
5. Add intake prompts, test cases, and a README

New plugins should read their jurisdiction rules from `/rules/{workflow}/` — not embed copies of the rules files.

---

*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*
