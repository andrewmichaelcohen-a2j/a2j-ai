# A2J AI — Project State of Record
**Ingest this file at the start of every Cowork session for full project context.**
**Generated:** June 15, 2026 · **Next update:** after each significant session

> **How to use:** At the start of a new Cowork session, say: "Please read `docs/PROJECT_STATE_OF_RECORD.md` from the a2j-ai repo to brief yourself." Connect the `a2j-ai` folder when prompted (`/Users/andrewcohen/Documents/GitHub/a2j-ai`). This file replaces `docs/PROJECT_STATUS_JUNE2026.md` as the primary session-start brief.

---

## 1. Repo Identity

| Field | Value |
|-------|-------|
| GitHub URL | `https://github.com/andrewmichaelcohen-a2j/a2j-ai` |
| Local path | `/Users/andrewcohen/Documents/GitHub/a2j-ai/` |
| Visibility | **Public** (confirmed) |
| License | Apache 2.0 |
| Active branch | `main` |
| Last commit | 2026-06-11 — `update ca rules json file` (v2 changes not yet pushed — see §7) |

---

## 2. Repo Tree

```
a2j-ai/
├── README.md                              ← Project overview (see Section 5)
├── CONTRIBUTING.md
├── LICENSE
├── NOTICE
│
├── plugins/
│   ├── eviction-defense/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── README.md
│   │   ├── components/
│   │   │   ├── RulesComparisonWidget.html   ← Demo widget (canonical copy here)
│   │   │   └── RulesComparisonWidget.jsx
│   │   ├── jurisdictions/
│   │   │   ├── README.md
│   │   │   ├── ca_eviction_rules_v0.1.json  ← Plugin-local CA file (demo version)
│   │   │   ├── ca_eviction_v1.2.json        ← Older CA file; superseded by rules/
│   │   │   ├── ny_eviction_rules_v0.1.json
│   │   │   ├── tx_eviction_rules_v0.1.json
│   │   │   └── tx_eviction_v0.1.json
│   │   ├── prompts/
│   │   │   └── demo-script.md               ← Demo script (older copy; canonical is demos/)
│   │   ├── skills/
│   │   │   └── eviction-triage/SKILL.md
│   │   └── test-cases/README.md
│   │   └── LHC_Demo_Deck_v0.1.pptx          ← ⚠️ OLD — delete before next public push
│   │
│   └── consumer-debt/                        ← Skeleton only; work paused
│       ├── .claude-plugin/plugin.json
│       ├── README.md
│       ├── jurisdictions/README.md
│       ├── skills/consumer-debt-validation/SKILL.md
│       └── test-cases/README.md
│
├── rules/
│   ├── README.md
│   ├── schema/
│   │   ├── eviction_schema_v1.0.json        ← v1 schema (notice-centric; still used by v1 files)
│   │   └── eviction_schema_v2.0.json        ← ✅ NEW — v2 schema (5-module full-defense scope)
│   ├── eviction/                             ← 51 jurisdictions; each has v1 + v2 files
│   │   ├── alabama/
│   │   │   ├── al_eviction_v1.json          ← v1 (notice-centric; DRAFT)
│   │   │   └── al_eviction_v2.json          ← ✅ NEW v2 (5 modules; DRAFT — L1 not retrieved)
│   │   ├── alaska/ak_eviction_v1.json + ak_eviction_v2.json
│   │   ├── ... [all 50 states + DC; same pattern]
│   │   ├── california/
│   │   │   ├── ca_eviction_v1 copy.json     ← ⚠️ Source v1 (original was deleted; copy is canonical)
│   │   │   └── ca_eviction_v2.json          ← ✅ NEW v2 · AUTOMATED-CHECKS-PASSED (all 5 modules)
│   │   ├── florida/fl_eviction_v2.json      ← ✅ NEW v2 · AUTOMATED-CHECKS-PASSED (all 5 modules)
│   │   ├── new_york/ny_eviction_v2.json     ← ✅ NEW v2 · AUTOMATED-CHECKS-PASSED (all 5 modules)
│   │   └── texas/tx_eviction_v2.json        ← ✅ NEW v2 · AUTOMATED-CHECKS-PASSED (all 5 modules)
│   └── validation/
│       ├── battery/validate.py              ← ✅ UPDATED — v2-aware; enforces 3 guardrails
│       └── reports/
│           ├── validation_report_20260601_232614.json   ← v1 report (archive)
│           ├── validation_report_latest.json            ← v1 latest (archive)
│           ├── validation_report_v2_20260615_223422.json ← ✅ NEW v2 report
│           └── validation_report_v2_latest.json         ← ✅ NEW v2 latest
│
├── demos/
│   ├── README.md
│   └── eviction/
│       ├── prompts/
│       │   └── demo-script.md               ← CANONICAL demo script v5 (see Section 6)
│       ├── slides/
│       │   ├── Demo_Deck_v0.2.pdf
│       │   ├── Demo_Deck_v0.2.pptx
│       │   └── Demo_Deck_v0.4.pptx          ← Latest deck version
│       └── widget/
│           ├── RulesComparisonWidget.html   ← Open in Chrome for demo (no server needed)
│           └── RulesComparisonWidget.jsx
│
├── playbooks/README.md                      ← Stub; content TBD
│
└── docs/
    ├── CONTRIBUTING.md
    ├── Decision_Logic_Briefing_for_Claude.md
    ├── DISCLAIMER.md
    ├── PROJECT_PLAN.md                      ← Master project plan (Claude does NOT edit)
    ├── PROJECT_STATE_OF_RECORD.md           ← This file (Claude updates each session)
    ├── PROJECT_STATUS_JUNE2026.md           ← Older; superseded by this file
    ├── Review_Slides_v0.1.pptx
    ├── Review_Slides_v0.2.pptx
    ├── REVIEWER_CHECKLIST.md
    └── STATUS_LABELS.md                     ← ✅ UPDATED to v2 (module-level + guardrails)
```

---

## 3. Rules File Inventory — Eviction (51 Jurisdictions)

### v2 Summary (current)

**Schema:** `eviction-v2` · **5 modules per file:** `notice`, `service`, `overlays`, `substantive_defenses`, `procedural_defects`  
**Validation last run:** 2026-06-15T22:34Z (v2)  
**Layers run:** L1, L3, L5 · L2/L4/L6: `not_implemented`  
**file_status rule:** `min(module_status)` — enforced by `validate.py`

| Metric | Count |
|--------|-------|
| Total v2 files | 51 |
| L3 PASS | 51 / 51 |
| L1 retrieved (statutory text confirmed) | 4 (CA, TX, NY, FL) |
| file_status = AUTOMATED-CHECKS-PASSED | **4** (CA, TX, NY, FL — all 5 modules) |
| file_status = DRAFT | 47 (L1 not retrieved) |
| L5 flags (notice period outliers) | ~8 states (see below) |

**Per-module status for AUTOMATED-CHECKS-PASSED states:**

| State | notice | service | overlays | substantive_defenses | procedural_defects | file_status |
|-------|--------|---------|----------|----------------------|--------------------|-------------|
| CA | ACP† | ACP† | ACP† | ACP† | ACP† | **AUTOMATED-CHECKS-PASSED** |
| TX | ACP† | ACP† | ACP† | ACP† | ACP† | **AUTOMATED-CHECKS-PASSED** |
| NY | ACP† | ACP† | ACP† | ACP† | ACP† | **AUTOMATED-CHECKS-PASSED** |
| FL | ACP† | ACP† | ACP† | ACP† | ACP† | **AUTOMATED-CHECKS-PASSED** |

†ACP = AUTOMATED-CHECKS-PASSED · coverage = L1,L3,L5 · reviewer = null

All 47 remaining states: all 5 modules DRAFT · file_status = DRAFT (L1 statutory retrieval not performed).

**L5 flags from v2 run** (notice period outliers — likely correct but need attorney confirmation):
- TN, VT, WA: L5 notice period flag (period >2× library median)

**v1 files:** Still present alongside v2 files. v1 is notice-centric (pre-5-module schema). v1 files are the source for v2 migration — do not delete.

---

## 4. Validation Harness Status

**Script:** `rules/validation/battery/validate.py` ← **UPDATED June 15, 2026 (v2-aware)**  
**Run command:** `python3 rules/validation/battery/validate.py [--state CA] [--no-writeback] [--report]`

### v2 Validation Architecture

| Layer | Name | Status | v2 Result (2026-06-15) |
|-------|------|--------|------------------------|
| **L1** | Statutory grounding | ✅ Operational | 4 pass / 47 not_run |
| **L2** | Multi-model consensus | ⚠️ not_implemented | — |
| **L3** | Internal consistency | ✅ Operational | 51/51 PASS · 0 errors · 0 warnings |
| **L4** | Golden-set tests | ⚠️ not_implemented | — |
| **L5** | Cross-jurisdiction anomaly | ✅ Operational | PASS for most; ~8 notice-period flags |
| **L6** | Temporal freshness | ⚠️ not_implemented | — |
| **L7** | Attorney review | 🔴 Not started | 0/51 modules attorney-reviewed |

### Three enforced guardrails (new in v2)

1. **G1 — No auto-advance:** Any module at UNDER REVIEW/VALIDATED/CERTIFIED with `reviewer=null` is a hard validation FAIL. No automated process may advance past AUTOMATED-CHECKS-PASSED.
2. **G2 — file_status = min(module_status):** `validate.py` computes and writes back the correct `file_status` on every run. Never set directly.
3. **G3 — Option-A gate:** A module advances to AUTOMATED-CHECKS-PASSED only when all currently-implemented layers (today: L1, L3, L5) pass with no errors. `not_implemented` layers don't block.

### Write-back behavior

On each run, `validate.py` writes results back to each v2 file:
- Updates `validation.automated_layers` (L1/L3/L5 results)
- Advances DRAFT modules to AUTOMATED-CHECKS-PASSED if Option-A gate passes
- Recomputes and writes `file_status = min(module_status)`
- Appends open flags to `validation.flags`

Use `--no-writeback` to run read-only (report only, no file updates).

---

## 5. README (Current Contents)

> Source: `README.md` · Last committed: 2026-06-02

```
# A2J AI — Open Infrastructure for Access to Justice

Open-source plugins, rules, skills, and playbooks that make AI genuinely 
useful for the tens of millions of people who can't afford an attorney.

Built by: Andrew M Cohen
License: Apache 2.0
Status: Active development · v0.1 · June 2026

## The problem this solves

Every A2J organization that has tried to build AI legal tools faces the 
same compounding problem: no shared infrastructure, no shared rules layer, 
no portability across jurisdictions. Each team reinvents what others already 
built — for a single jurisdiction, in isolation, with no path to scale.

This repository is the shared foundation that ends that pattern.

## Repository structure

  plugins/     ← Deployable Claude plugins (one per A2J workflow)
  rules/       ← Rules / decision logic layer (portable across AI models)
    schema/    ← JSON schemas (one per workflow)
    eviction/  ← 50 states + DC (DRAFT)
    validation/← Automated validation battery (Layers 1–6)
  demos/       ← Demo materials by workflow
  playbooks/   ← Deployment guides for legal aid orgs, courts, clinics
  docs/        ← Project documentation, status labels, disclaimer

## The architecture in one paragraph

Anthropic's plugin and MCP connector framework provides the infrastructure 
layer: Claude as the reasoning engine, Legal Data Hunter and CourtListener 
as live statutory retrieval connectors. This repository contributes the 
content layer: jurisdiction-specific rules files encoding A2J decision logic, 
workflow skills, and deployment playbooks. The rules layer is designed to be 
portable to any AI model — not locked to Claude or Anthropic.

## How to contribute

The highest-value contribution is attorney validation of the rules files. 
Every DRAFT file needs one licensed attorney per state to verify statutory 
citations and sign off. See docs/CONTRIBUTING.md and docs/REVIEWER_CHECKLIST.md.

## Important disclaimers

All rules files are DRAFT status — AI-generated, not attorney-reviewed. 
Nothing here constitutes legal advice. See docs/DISCLAIMER.md.
```

**Known gap in README:** Does not mention the v2 schema or 5-module structure. Should be updated before next outreach push.

---

## 6. Demo Script (Current Version)

**File:** `demos/eviction/prompts/demo-script.md`  
**Version:** v5 (as of 2026-06-10 commits)  
**Format:** Loom recording script — ~6:00–6:30 minutes  
**Status:** Script finalized; **recording not yet made**

**Scene structure:**

| Scene | Content | Target Time |
|-------|---------|-------------|
| 1 | Setup — Maria Garcia's story, 3-day notice received | 0:00–0:35 |
| 2 | Live statute retrieval — CCP §1161 via Legal Data Hunter | 0:35–1:30 |
| 3 | Case law gap — Orozco v. Casimiro (2004), late fees void | 1:30–2:20 |
| 4 | Live rules file analysis — attach ca_eviction_rules_v0.1.json, run Maria's notice → defect found | 2:20–3:15 |
| 5 | Comparison Widget — left panel (no rules) vs. right panel (rules → INVALID + Orozco cite) | 3:15–3:55 |
| 6 | Rules file on GitHub — show the notice_defects entry, explain DRAFT label | 3:55–4:35 |
| 7 | Portability — switch widget to TX, then NY | 4:35–5:15 |
| 8 | Bridge/close — non-engineer attorney, 3 days, the question is rigor not capability | 5:15–6:00 |

**Key demo assets needed open before recording:**
- Tab A: `demos/eviction/widget/RulesComparisonWidget.html` — preloaded on CA
- Tab B: GitHub → `rules/eviction/california/ca_eviction_v1.json` → `notice_defects` section
- Cowork: blank session, ready
- File ready to drag into Scene 4: `plugins/eviction-defense/jurisdictions/ca_eviction_rules_v0.1.json`

**Demo link:** Not yet recorded. Will be a Loom URL. Placeholder: `[ link to demo ]` on Slide 7 of Demo_Deck_v0.4.pptx.

---

## 7. Changelog — Past Two Weeks (Cowork Activity)

**Source:** `git log` + this session · June 1–15, 2026

| Date | What changed |
|------|-------------|
| **2026-06-15** | **v2 schema and rules library — full implementation (this session)** |
| | Created `rules/schema/eviction_schema_v2.0.json` (5-module full-defense schema) |
| | Generated all 51 `*_eviction_v2.json` files (v1-migration + stub-expansion) |
| | Updated `validate.py` to v2-aware: per-module L3/L5, 3 guardrails, write-back |
| | Ran full v2 validation: 51/51 L3 PASS; CA/TX/NY/FL → AUTOMATED-CHECKS-PASSED |
| | Overwrote `docs/STATUS_LABELS.md` with v2 (module-level granularity, guardrail language) |
| | Updated `docs/PROJECT_PLAN.md` + `docs/PROJECT_STATE_OF_RECORD.md` |
| 2026-06-11 | `update ca rules json file` — CA eviction rules file updated |
| 2026-06-10 | `update demo` (×2) — Demo assets updated |
| 2026-06-10 | `Update demo-script.md` — Demo script v5 |
| 2026-06-10 | `Update RulesComparisonWidget.html` — Widget HTML updated |
| 2026-06-09 | `demo updates` (×3) + `process updates` + `update eviction notice widget for demo` |
| 2026-06-08 | `Update demo-script.md` + `updated eviction prototype demo script` |
| 2026-06-04 | `fixes to address file name changes and slight demo flow updates` |
| 2026-06-02 | `project checklist` + `Restructure repo: plugins/, rules/, demos/; 51-state rules library; attribution` |

**⚠️ Pending commit:** All June 15 v2 work is local-only. Needs commit + push via GitHub Desktop.

---

## 8. Open Issues / Known Defects

### Demo — Blocking for Recording
- [ ] **Demo rehearsal not completed.** Full 6-scene flow needs one clean end-to-end run in Cowork before recording. Scenes 3–4 (Orozco + live rules attachment) are highest-risk.
- [ ] **Demo not yet recorded.** No Loom link exists. Slide 7 placeholder `[ link to demo ]` not yet filled.
- [ ] **Scene 4 file decision:** Script says to attach `ca_eviction_rules_v0.1.json` (plugin-local demo file). The canonical v2 file is `rules/eviction/california/ca_eviction_v2.json`. Decide which to use in the demo before recording.
- [ ] **v2 files not yet reflected in widget.** `RulesComparisonWidget.html` still references v1 data. Consider updating or noting in the demo that v2 is the new library format.

### Repo — Cleanup Needed
- [ ] **`plugins/eviction-defense/LHC_Demo_Deck_v0.1.pptx`** still in repo. Old deck with LHC naming. Delete before next push.
- [ ] **README** does not mention v2 schema or 5-module structure. Update before next outreach push.
- [ ] **`ca_eviction_v1 copy.json`** — the "copy" naming is an artifact of a macOS Finder rename. Rename to `ca_eviction_v1.json` when convenient (original was accidentally deleted earlier).
- [ ] **Demo script canonical copy:** `plugins/eviction-defense/prompts/demo-script.md` may be stale vs. `demos/eviction/prompts/demo-script.md`. The `demos/` copy is canonical.

### Validation Pipeline
- [ ] **L1 retrieval needed for 47 states.** Only CA, TX, NY, FL have `L1_grounding = pass`. Remaining 47 are DRAFT because L1 fails. Next priority: run Legal Data Hunter retrieval for remaining states to advance them.
- [ ] **L2 (multi-model consensus):** not_implemented. Needs a runner that queries a second model and compares outputs.
- [ ] **L4 (golden sets):** not_implemented. 0/51 states have golden sets. Need at least CA and TX before outreach. See `test-cases/README.md`.
- [ ] **L6 (temporal freshness):** not_implemented. Needs legislative feed / CI hook.
- [ ] **L7 (attorney review):** Not started. CA is priority #1. Need one licensed CA tenant attorney to review CA's 5 modules. See `docs/REVIEWER_CHECKLIST.md`.
- [ ] **L5 notice-period flags (TN, VT, WA and others):** Likely correct outliers but need attorney confirmation during L7 review.
- [ ] **Re-run on L2/L4/L6 expansion:** When new layers come online, all AUTOMATED-CHECKS-PASSED modules must be re-run. Modules that fail revert to DRAFT per STATUS_LABELS v2.

### Strategic / Project Level
- [ ] **Formal paper:** Not started. Raw material in prior Cowork sessions.
- [ ] **2-pager:** Not started.
- [ ] **Substack / website:** Not set up.
- [ ] **Margaret/Stanford pitch:** Deck ready; 2-pager and paper not done. Send after paper.
- [ ] **Content identity decision:** Personal name vs. A2J project brand — decide before Substack/website.

---

## 9. How to Resume Work in a New Session

**Standard brief:** "Please read `docs/PROJECT_STATE_OF_RECORD.md` from the a2j-ai repo."

**If working on demo rehearsal / recording:**
> "Read the State of Record, then open `demos/eviction/prompts/demo-script.md` and help me run a rehearsal. I need to practice Scenes 3 and 4 especially."

**If working on L1 retrieval (advancing 47 states):**
> "Read the State of Record. Let's run L1 statutory retrieval for [state] using Legal Data Hunter, update the v2 file, and re-run validate.py to advance it to AUTOMATED-CHECKS-PASSED."

**If working on attorney validation (L7):**
> "Read the State of Record. Let's prepare the CA v2 file for attorney review. Start with the notice module — generate a plain-language reviewer summary from ca_eviction_v2.json and the REVIEWER_CHECKLIST."

**If working on the paper or 2-pager:**
> "Read the State of Record. I want to start drafting the formal paper. The key source material is in our previous Cowork sessions — the AI layer vs. rules layer discussion, the certification maturity model, the liability architecture, and the LSC governance parallel."

---

*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*  
*State of Record generated by Claude (Cowork) — June 15, 2026. Replace this file at the start of each session after significant work.*
