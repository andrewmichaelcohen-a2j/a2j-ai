# A2J Project — Session Context for Claude/Cowork

This file is read automatically by Cowork at session start. It carries the key context needed to work on this project without re-deriving it each session.

*Last updated: June 24, 2026 · Andrew M Cohen*

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

## Operating system (Direction A/B/C — read first)

The project runs under a three-direction operating system established June 24, 2026. **Read these docs at session start before doing any work:**

| Doc | Location | Purpose |
|-----|----------|---------|
| Handoff + build order | `docs/COWORK_HANDOFF_ABC.md` | Sequential build order; what waits on Andy |
| Direction A | `docs/COWORK_DIRECTION_A_CADENCE_AUTONOMY.md` | GREEN/YELLOW/RED autonomy rule; morning report; work queue |
| Direction B | `docs/COWORK_DIRECTION_B_GOLDEN_SETS.md` | Frozen attorney-established ground truth; train/held-out split |
| Direction C | `docs/COWORK_DIRECTION_C_SELF_OPTIMIZATION.md` | Eval-driven self-optimization — DO NOT BUILD until B's golden sets exist |

**Current OS state:** Direction A is live. Direction B survey in progress. Direction C not started.

### GREEN/YELLOW/RED rule (always enforce)
- **GREEN:** Execute and log in DAILY_CHANGELOG.md — no approval needed. Bug fixes, pipeline runs, test-verified changes, retry passes, queue management.
- **YELLOW:** Execute and flag in morning report for ratification (reversible). Engineering choices between two approaches, config changes that affect metrics.
- **RED:** Stop and escalate. Genuine legal-interpretive judgment, immutables (ground truth, attorney line, passing standard), strategy, external-facing decisions. Only REDs reach Andy.
- **Anti-default rule:** A case may NOT go to attorney review (RED) without recorded evidence it survived a genuine automated attempt AND couldn't reach convergence-validated. "Model returned empty" = GREEN pipeline fix, never an attorney item.

### Work queue
`docs/WORK_QUEUE.md` — always populated several days deep (NOW / NEXT / BLOCKED / HORIZON). Cowork pulls from NEXT automatically when NOW completes. Read this at every session start to know what to do next.

### Daily changelog
`docs/DAILY_CHANGELOG.md` — log every GREEN action taken. Andy audits without having watched.

---

## Validation pipeline architecture

### Overnight automation
- **launchd scheduler:** `~/Library/LaunchAgents/com.cjac.validation.plist` fires `dispatch.py` at **2:15 AM** nightly.
- **dispatch.py:** `rules/validation/dispatch.py` — picks one job from `queue/`, runs it, moves to `done/` or `failed/`. Supports two job types:
  - `protocol` — runs `run_protocol.py` (holdings validation)
  - `l2_module` — runs L2 module runners (e.g. `l2_procedural_defects_runner.py`)
- **Morning report:** Cowork scheduled task fires at **8 AM** daily. Posts Direction A report (GREEN log, YELLOW, RED, Krippendorff's α, queue health, anti-default audit). Updates STATE_OF_RECORD, METRICS_LEDGER, HUMAN_REVIEW_QUEUE, WORK_QUEUE, DAILY_CHANGELOG.

### Job queue
`rules/validation/queue/` — drop `.json` job files here. Dispatcher picks the oldest one per night.

Currently queued for tonight (2026-06-25 at 2:15 AM):
- `job_batch3_20260623.json` — Batch 3: 18 states, retaliation holdings v3
- `job_l2_procedural_defects_20260624.json` — Full 51 states × 4 defects, L2 procedural defects

### Bucket taxonomy (MV/CI/RC/PR/SM)
All validation results use this classification — never a blended rate:
- **MV** — machine-verified: text retrieved, two independent models corroborated holding
- **CI** — confirm-inference: corroborated but control=INFERRED; routes to cheap confirm lane
- **RC** — re-characterize: text retrieved, holding diverged; genuine inaccuracy → attorney re-characterization
- **PR** — pending-retrieval: text NOT retrievable (infrastructure failure, not verification failure). **Never routes to attorney.** Quarantined for retrieval retry.
- **SM** — single-model-preliminary: only one model answered. Never machine-verified.

### Two-rate reporting (holdings protocol — never blend)
- **Method rate:** `MV ÷ (MV+CI+RC)` — among text-retrievable cases
- **Overall rate:** `MV ÷ all` — including PR (retrieval-gated)
- Report Krippendorff's α, not raw agreement %.

### L2 module classification (procedural defects, overlays, etc.)
- **CONSENSUS-IMPROVE** — both models agree on a more specific citation → auto-update statute
- **CONSENSUS-CONFIRM** — both models confirm current citation
- **NO-SPECIFIC-RULE** — both models agree no separate rule exists
- **MODEL-SPLIT** — genuine disagreement → L7 flag, routes to HUMAN_REVIEW_QUEUE
- **SM-GEMINI / SM-GPT** — one model empty, other has valid answer → preserve as `l2_sm_statute`, flag for re-run. NOT attorney lane.
- **ERROR** — both models empty → log, investigate pipeline

---

## Key validation runners

| Runner | Location | Purpose |
|--------|----------|---------|
| Holdings protocol | `rules/validation/protocols/retaliation_holdings_v3.py` | Generate-from-source holdings validation; MV/CI/RC/PR/SM buckets |
| Harness | `rules/validation/harness.py` | Shared reliability layer; enforce provenance; two-rate summary |
| Dispatcher | `rules/validation/dispatch.py` | Overnight job runner (protocol + l2_module types) |
| L2 runner base | `rules/validation/l2/l2_runner.py` | Base model calls (call_openai, call_gemini, load_all_v2_files) |
| L2 procedural defects | `rules/validation/l2/l2_procedural_defects_runner.py` | Multi-model consensus on procedural_defects module |
| Regression tests | `rules/validation/tests/test_l2_procedural_defects.py` | 30/30 tests pass; run before any overnight queue |

**Critical API note:** `call_openai(query: str)` and `call_gemini(query: str)` each take **one string argument**. SYSTEM_PROMPT is baked inside those functions. They return an already-parsed dict (not a raw string). The `_raw` key holds the raw response; `error` key holds any failure message.

---

## Repo structure

```
a2j-ai/
├── plugins/             ← Claude plugins (eviction-defense, consumer-debt)
├── rules/
│   ├── schema/          ← JSON schema (eviction_schema_v2.0.json)
│   ├── eviction/        ← 51 v2 rules files (50 states + DC)
│   └── validation/
│       ├── dispatch.py          ← Overnight job dispatcher
│       ├── harness.py           ← Shared validation reliability layer
│       ├── run_protocol.py      ← CLI entrypoint for protocol jobs
│       ├── validate.py          ← L1-L5 schema/consistency checks
│       ├── protocols/           ← Protocol adapters (retaliation_holdings_v3.py)
│       ├── l2/                  ← L2 multi-model runners
│       │   ├── l2_runner.py
│       │   ├── l2_procedural_defects_runner.py
│       │   └── output/          ← L2 run output JSON files
│       ├── queue/               ← Pending job files (dispatcher picks from here)
│       ├── done/                ← Completed job records
│       ├── failed/              ← Failed job records
│       ├── results/             ← SUMMARY_*.md from protocol runs
│       ├── logs/                ← Dispatcher log files
│       └── tests/               ← Regression tests (test_l2_procedural_defects.py)
├── demos/
│   └── eviction/
│       ├── slides/       ← Demo_Deck_v0.2.pptx
│       ├── prompts/      ← demo-script.md
│       └── widget/       ← RulesComparisonWidget.html
├── validation/
│   └── l2/output/        ← L2 output files (note: also in rules/validation/l2/output/)
├── playbooks/
└── docs/                 ← All project documentation
```

---

## Key documents (read at session start)

| Document | Location | Purpose |
|----------|----------|---------|
| **Work queue** | `docs/WORK_QUEUE.md` | NOW/NEXT/BLOCKED/HORIZON — read first |
| **Daily changelog** | `docs/DAILY_CHANGELOG.md` | GREEN action log |
| Project state | `docs/PROJECT_STATE_OF_RECORD.md` | Full validation status |
| Metrics ledger | `docs/VALIDATION_METRICS_LEDGER.md` | Run-by-run metrics with α |
| Human review queue | `docs/HUMAN_REVIEW_QUEUE.md` | RED-interpretive items for attorney |
| Direction A | `docs/COWORK_DIRECTION_A_CADENCE_AUTONOMY.md` | Operating cadence |
| Direction B | `docs/COWORK_DIRECTION_B_GOLDEN_SETS.md` | Golden sets |
| Direction C | `docs/COWORK_DIRECTION_C_SELF_OPTIMIZATION.md` | Self-optimization (not started) |
| Handoff | `docs/COWORK_HANDOFF_ABC.md` | Build order |
| Reporting direction | `docs/COWORK_DIRECTION_HOLDINGS_V3_REPORTING.md` | Two-rate reporting rules |
| Validation philosophy | `docs/VALIDATION_PHILOSOPHY.md` | Why the method works |
| Schema spec | `docs/SCHEMA_V2_DESIGN_SPEC.md` | v2 schema design |

---

## Validation status (as of June 24, 2026)

- **51 v2 rules files:** all states + DC, schema v2, interoperability tags, procedural_defects grounded
- **Notice module (L2):** complete — 32/35 AI-resolved, 3 attorney-routed (genuine)
- **Service module (L2):** complete — 51 states validated
- **Procedural defects (L2):** smoke test complete (CA/TX/NY); full 51-state run queued for tonight
- **Retaliation holdings (v3):** Batch 1 (33 states) + Batch 2 (all 51) run; Batch 3 (18 remaining) queued for tonight
- **Remaining defenses (Module 6):** complete
- **Golden sets (L4):** not_implemented — Direction B in progress
- **Self-optimization (Direction C):** not started — blocked on B

---

## Immutables (never crossed by automation)

1. Ground truth — golden-set answers are read-only; only a named attorney sets them
2. The held-out set — the optimizer never sees it
3. The attorney line — machine-verified is below validated; crossing requires a named human
4. Passing standard — thresholds only move up, never down
5. The guards themselves — no self-modification of immutability checks or escalation rules

---

## For Claude Chat sessions (not Cowork)

When working on the pitch deck in Claude Chat, upload:
1. The current deck PPTX
2. `docs/Decision_Logic_Briefing_for_Claude.md`
3. This CLAUDE.md file (or paste its contents)

Claude Chat does not auto-read this file — it must be uploaded manually.

---

*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*
