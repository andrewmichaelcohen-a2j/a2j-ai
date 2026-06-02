# A2J AI Project — Status Document
*Andrew M Cohen · June 2, 2026 · For reference and continuity*

---

## I. GitHub Desktop Repo Structure

Your local repo is at:
`/Users/andrewcohen/Documents/GitHub/a2j-claude-legal-plugins/`

It is connected to GitHub.com at:
`https://github.com/andrewmichaelcohen-a2j/a2j-ai`

The folder structure is:

```
a2j-claude-legal-plugins/   ← local folder name (can rename later if desired)
│
├── plugins/                ← Deployable Claude plugins
│   ├── eviction-defense/   ← Full eviction triage plugin (skill, prompts, rules)
│   └── consumer-debt/      ← Debt collection plugin (skeleton only)
│
├── rules/                  ← Rules / decision logic layer
│   ├── schema/             ← JSON schema (eviction_schema_v1.0.json)
│   ├── eviction/           ← 51 DRAFT rules files (50 states + DC)
│   └── validation/         ← Automated validation battery + reports
│
├── demos/                  ← Demo materials
│   └── eviction/
│       ├── slides/         ← Demo_Deck_v0.2.pptx
│       ├── prompts/        ← demo-script.md (live demo script)
│       └── widget/         ← RulesComparisonWidget.html + .jsx
│
├── playbooks/              ← Deployment guides (stub — content TBD)
│
├── docs/                   ← Project documentation
│   ├── STATUS_LABELS.md
│   ├── DISCLAIMER.md
│   ├── CONTRIBUTING.md
│   ├── REVIEWER_CHECKLIST.md
│   └── PROJECT_STATUS_JUNE2026.md  ← this file
│
├── README.md               ← Project overview
├── LICENSE                 ← Apache 2.0
├── CONTRIBUTING.md
└── NOTICE
```

---

## II. What Content Is in Your Repo Right Now

### Plugins
| Item | Location | Status |
|------|----------|--------|
| Eviction triage SKILL.md | `plugins/eviction-defense/skills/eviction-triage/SKILL.md` | Complete |
| Eviction intake workflow | `plugins/eviction-defense/prompts/demo-script.md` | Complete |
| CA/TX/NY jurisdiction rules (demo versions) | `plugins/eviction-defense/jurisdictions/` | DRAFT |
| Consumer debt skill | `plugins/consumer-debt/skills/` | Skeleton only |

### Rules Layer
| Item | Location | Status |
|------|----------|--------|
| JSON schema | `rules/schema/eviction_schema_v1.0.json` | Complete |
| 51 state rules files | `rules/eviction/{state}/` | DRAFT — not attorney validated |
| Validation battery | `rules/validation/battery/validate.py` | Running (51/51 L3 pass) |
| Validation report | `rules/validation/reports/validation_report_latest.json` | Current |

**Statutory retrieval performed for:** CA, TX, NY (via Legal Data Hunter), FL (via Florida Legislature website).
**Remaining 47 states:** flagged `statutory_retrieval_performed: false` — need attorney review.

### Demos
| Item | Location | Notes |
|------|----------|-------|
| Slide deck (10 slides) | `demos/eviction/slides/Demo_Deck_v0.2.pptx` | Clean — no org attribution |
| Live demo script | `demos/eviction/prompts/demo-script.md` | Pre-written Cowork prompts + timing |
| Rules Comparison Widget | `demos/eviction/widget/RulesComparisonWidget.html` | Open in Chrome — no server needed |
| React widget version | `demos/eviction/widget/RulesComparisonWidget.jsx` | For embedding |

### Google Drive (NOT in GitHub — separate)
| Item | Location |
|------|----------|
| LHC_Eviction_Demo_Architecture_v0.2 | Google Drive (your working doc) |
| LHC Workflow Guide v0.1 | Google Drive (process reference) |

---

## III. Steps to Publish Publicly on GitHub

**Before you can push/publish, complete these steps in order:**

### Step 1 — Finish the current commit (if not done)
In GitHub Desktop:
- Summary: `Restructure repo: plugins/, rules/, demos/; 51-state rules library; clean attribution`
- Commit to main → Push origin

### Step 2 — Clean up one remaining file
Delete `plugins/eviction-defense/LHC_Demo_Deck_v0.1.pptx` — old deck with incorrect naming still sitting in the plugin folder. Do in Finder, then commit: `Remove old LHC-named deck`

### Step 3 — Do the demo rehearsal
Run the full 10-minute demo end-to-end in Cowork using the demo script. Confirm the triage output looks clean before going public.

### Step 4 — Make the repo public on GitHub.com
1. Go to `github.com/andrewmichaelcohen-a2j/a2j-ai`
2. Settings → Danger Zone → Change repository visibility → Make public
3. Confirm

**The repo is safe to make public now** — all files are labeled DRAFT, the DISCLAIMER.md is in place, and there's no personal client data anywhere.

### Optional Step 5 — Rename the local folder
The local folder is still called `a2j-claude-legal-plugins` even though the GitHub repo is `a2j-ai`. This doesn't affect anything functionally, but if you want consistency: quit GitHub Desktop, rename the folder in Finder to `a2j-ai`, reopen GitHub Desktop, and use File → Add Local Repository to reconnect.

---

## IV. All Content Created — Complete Inventory

### Cowork-Built Files (now in repo)
| File | What it does |
|------|-------------|
| `Demo_Deck_v0.2.pptx` | 10-slide pitch deck: problem → infrastructure → demo → gaps → opportunity → ask |
| `demo-script.md` | Pre-written demo prompts for Cowork, beat-by-beat script, timing guide, contingency notes |
| `RulesComparisonWidget.html` | Side-by-side: raw LLM (wrong) vs. rules-grounded (correct) — CA/TX/NY switcher |
| `eviction-triage/SKILL.md` | Full intake-to-output workflow instructions for the eviction triage skill |
| `ca_eviction_v1.json` + v1.2 | California rules (live statutory retrieval confirmed) |
| `tx_eviction_v1.json` + v0.1 | Texas rules (live statutory retrieval confirmed) |
| `ny_eviction_v1.json` | New York rules (live statutory retrieval confirmed) |
| `fl_eviction_v1.json` | Florida rules (web retrieval of §83.56 confirmed) |
| 47 additional state files | All 50 states + DC — model knowledge, flagged for attorney retrieval |
| `eviction_schema_v1.0.json` | JSON Schema locking the rules file format |
| `validate.py` | Layers 1–6 automated validation battery |
| `validation_report_latest.json` | Current validation run — 51/51 L3 pass |
| `README.md` (root) | Project overview, architecture description, contribution ask |
| `docs/STATUS_LABELS.md` | DRAFT/VALIDATED/CERTIFIED definitions |
| `docs/DISCLAIMER.md` | Legal information not legal advice framing |
| `docs/REVIEWER_CHECKLIST.md` | Standard for attorney validation |
| `docs/CONTRIBUTING.md` | How to contribute rules, golden sets, playbooks |

### In Google Drive (not in repo)
| File | Purpose |
|------|---------|
| LHC_Eviction_Demo_Architecture_v0.2 | Full strategic spec — Maria persona, demo script, gaps, roadmap |
| LHC Workflow Guide v0.1 | How Cowork + GitHub Desktop work together; session workflow |

---

## V. Project Checklist — Done and Left To Do

### ✅ Done
- [x] Eviction defense SKILL.md (intake → analysis → output workflow)
- [x] CA, TX, NY rules files with live statutory retrieval
- [x] FL rules file with retrieved §83.56
- [x] 51-state DRAFT rules library (all states + DC)
- [x] JSON schema for rules files
- [x] Automated validation battery (Layers 1–6) — 51/51 L3 pass
- [x] Rules Comparison Widget (CA/TX/NY switcher, browser-ready)
- [x] 10-slide pitch deck v0.2 (clean, no org attribution)
- [x] Live demo script with pre-written Cowork prompts
- [x] Repo restructure: plugins/ rules/ demos/ playbooks/ docs/
- [x] All LHC / Legal Help Commons attribution removed — copyright Andrew M Cohen only
- [x] Remote URL updated to a2j-ai
- [x] Apache 2.0 license, NOTICE, DISCLAIMER in place

### 🔲 Immediate Next Steps (this week)
- [ ] Commit + push current changes (GitHub Desktop)
- [ ] Delete old LHC_Demo_Deck_v0.1.pptx from plugins/eviction-defense/
- [ ] Run full demo rehearsal in Cowork — time it, confirm output is clean
- [ ] Make repo public on GitHub.com (after rehearsal)

### 🔲 Near-Term (before first live audience demo)
- [ ] Record 60-second widget interaction clip for the deck
- [ ] Add demo recording (Loom) after rehearsal
- [ ] Build test cases / golden set for CA (rules/validation/golden_sets/)
- [ ] Write attorney validation outreach email/template
- [ ] Contact at least one CA tenant attorney for rules validation

### 🔲 Phase 1 (1–3 months)
- [ ] Playbooks: legal aid intake deployment guide
- [ ] 50-state attorney validation coordination (recruit reviewers)
- [ ] Publish validated CA rules file (first VALIDATED status file)
- [ ] Second A2J workflow: debt collection or benefits appeals
- [ ] Outreach to Anthropic and Stanford/law school partners

---

*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*
*Generated June 2, 2026 — update after each major session.*
