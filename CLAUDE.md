# A2J Project — Session Context for Claude/Cowork

This file is read automatically by Cowork at session start. It carries the key context needed to work on this project without re-deriving it each session.

*Last updated: June 9, 2026 · Andrew M Cohen*

---

## Project identity

**Name:** Civil Justice as Code (organized under "A2J project")  
**Repo:** github.com/andrewmichaelcohen-a2j/a2j-ai  
**Copyright:** Copyright 2026 Andrew M Cohen. Apache 2.0.  
**Do not use:** "LHC" or "Legal Help Commons" as an organizing frame anywhere in this project.

---

## What this project is

Infrastructure for access-to-justice legal AI. The thesis: as of May 2026, legal tech finally has common shareable building blocks — open-source plugins, skills, MCP connectors to live legal databases, and a new decision-logic rules layer. The project's first concrete deliverable is a 50-state eviction rules library, validated through a 7-layer process, published to GitHub.

**The three layers of the infrastructure:**
1. **Tier 1 — AI foundation:** Claude model (translation, reasoning, drafting — "predictive")
2. **Tier 2 — Legal & safety layer:** MCP connectors to authoritative law (live, deterministic), reusable skills/plugins, safety/validation tooling
3. **Tier 3 — Decision logic / rules layer:** Machine-readable, auditable rules encoding how law applies to specific facts (the project's contribution)

---

## Critical: what the decision logic layer IS and IS NOT

**What it is:** AI-synthesized legal doctrine — the structured encoding of how law applies to specific facts, drawing on statutory text, judicial interpretation, and practitioner knowledge. Not just what statutes say, but how courts and practitioners have applied them to specific fact patterns.

**What it is NOT:**
- Not hallucination — rules are derived from identifiable legal sources, fully auditable
- Not simple statutory transcription — statutes state what the law says; rules encode how it applies
- Not document assembly (A2J Author, HotDocs) — document assembly fills out forms; rules layer determines legal validity

**The CA late-fee example:** CCP §1161(2) says a notice must state "the amount that is due." Courts have interpreted this to mean rent only — late fees void the notice. The rules file encodes that interpretation as structured logic. The statute is the anchor; judicial and practitioner interpretation makes the rule specific enough to apply to a specific notice.

**Why attorney validation is genuinely required:** We are not asking attorneys to check if the AI copied the statute correctly. We are asking them to confirm whether the AI's synthesis of legal doctrine — its encoding of how courts and practitioners have applied the statute — is accurate. That requires real legal expertise.

---

## Demo scope vs. project scope

**Demo shows:** Pre-filing eviction notice triage (one slice) — notice types, defect detection, affirmative defenses. CA (full) + TX/NY (portability). Proof of concept for the method.

**Project builds:** Complete eviction decision logic for all 50 states + DC (including pre-filing, court procedure, hearing-stage defenses). Then: consumer debt → benefits appeals → record sealing → DV/immigration.

---

## Repo structure

```
a2j-ai/
├── plugins/          ← Claude plugins (eviction-defense, consumer-debt)
├── rules/            ← Decision logic layer
│   ├── schema/       ← JSON schema
│   ├── eviction/     ← 51 DRAFT rules files (50 states + DC)
│   └── validation/   ← Automated validation battery
├── demos/            ← Demo materials
│   └── eviction/
│       ├── slides/   ← Demo_Deck_v0.2.pptx
│       ├── prompts/  ← demo-script.md (recording script)
│       └── widget/   ← RulesComparisonWidget.html (open in Chrome)
├── playbooks/
└── docs/             ← Project documentation + briefing files
```

---

## Current demo status

- **Recording script:** `demos/eviction/prompts/demo-script.md` — v2, updated June 9. Recording guide for a 5:15–6:00 Loom recording. NOT a live session script.
- **Comparison widget:** `demos/eviction/widget/RulesComparisonWidget.html` — open via `file:///Users/andrewcohen/Documents/GitHub/a2j-ai/demos/eviction/widget/RulesComparisonWidget.html` in Chrome
- **Widget left panel:** Correctly shows "AI + live statute retrieval / no rules file" (updated June 9 — old version incorrectly said "training data")
- **Demo deck:** `demos/eviction/slides/Demo_Deck_v0.2.pptx` — 18-slide Civil Justice as Code deck. Demo recording link placeholder on Slide 7. GitHub links placeholder on Slides 12–13.

---

## Rules files status

- **CA** (`rules/eviction/california/ca_eviction_v1.json`): Best-developed. Statutory text retrieved live. Attorney validation is priority #1.
- **TX, NY, FL**: Live statutory retrieval performed.
- **Remaining 47 states**: `statutory_retrieval_performed: false`. Flagged for attorney review. DRAFT only.
- All files: Apache 2.0, `validation_status: DRAFT`, not for use advising real people.

---

## Key documents in this repo

| Document | Location | Purpose |
|----------|----------|---------|
| Project status | `docs/PROJECT_STATUS_JUNE2026.md` | Full status checklist |
| Decision logic briefing | `docs/Decision_Logic_Briefing_for_Claude.md` | Accurate framing of rules layer — read before working on deck or pitch materials |
| Demo recording script | `demos/eviction/prompts/demo-script.md` | Recording guide |
| Workflow guide | Check Google Drive | How Cowork + GitHub Desktop work together |

---

## For Claude Chat sessions (not Cowork)

When working on the **pitch deck** in Claude Chat, upload:
1. The current deck PPTX
2. `docs/Decision_Logic_Briefing_for_Claude.md`
3. This CLAUDE.md file (or paste its contents)

Claude Chat does not auto-read this file — it must be uploaded manually. Keep `Decision_Logic_Briefing_for_Claude.md` bookmarked in Google Drive for this purpose.

---

*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*
