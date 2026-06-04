# A2J AI Project — Status Document
*Andrew M Cohen · Updated June 4, 2026 · For reference and continuity*

---

## SESSION CONTINUITY — How to Brief Claude at the Start of a New Session

Claude does not retain memory between sessions. At the start of each session, paste this into Cowork:

> "I'm Andy Cohen working on the A2J AI project. Please read `/Users/andrewcohen/Documents/GitHub/a2j-ai/docs/PROJECT_STATUS_JUNE2026.md` to get current context, then we can pick up where we left off."

Claude will then ask you to connect the `a2j-ai` folder (click the dialog, navigate to `Documents/GitHub/a2j-ai`, click Open), and it will read this file and be fully briefed.

**Key facts for fast re-orientation:**
- Repo: `github.com/andrewmichaelcohen-a2j/a2j-ai` — public but eviction files not yet pushed
- Local repo path: `/Users/andrewcohen/Documents/GitHub/a2j-ai/`
- GitHub username: `andrewmichaelcohen-a2j`
- Active focus: Eviction defense demo — consumer-debt is paused/deprioritized
- Widget: `demos/eviction/widget/RulesComparisonWidget.html` (open by double-clicking in Finder)
- Demo script: `demos/eviction/prompts/demo-script.md`
- Rules files: `rules/eviction/[state]/[state]_eviction_v1.json`

---

## STRATEGIC CONTEXT (updated June 4, 2026)

The project has evolved from a "plugin marketplace" framing to a more focused thesis:

**Eviction defense is the initial proof of concept for a larger project: building a "civil justice as code" rules layer** — structured, version-controlled, attorney-validated rules files covering A2J legal domains across all 50 states. The eviction demo shows what's currently possible with legal plugins; the 50-state rules library is the first community contribution ask.

The roadmap is: fully validate eviction rules → use that process as the template → expand to debt collection, benefits appeals, and other A2J domains. Consumer-debt work is on pause until eviction is validated and published.

**Phase sequencing:**
1. Finalize messaging content (overall deck, detailed project paper, 2-pager) — *in progress*
2. Finalize demo — script, slides, widget all confirmed working — *in progress*
3. Push to GitHub: eviction demo + slides + 50-state rules — *not yet done*
4. Update README and repo docs to reflect eviction-first / rules-as-infrastructure framing
5. Outreach and attorney validation recruitment

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

### ✅ Fixed June 4, 2026 (Cowork session)
- [x] All file references in `demo-script.md` corrected — old `ca_eviction_rules_v0.1.json`, `v1.2`, and `eviction-defense/jurisdictions/` paths replaced with actual filenames and `rules/eviction/[state]/` paths
- [x] `RulesComparisonWidget.html` (original in `demos/eviction/widget/`) fixed — stale filenames `ca_eviction_v1.2.json`, `tx_eviction_v0.1.json`, `ny_eviction_rules_v0.1.json` corrected to `v1.json` throughout; path footer corrected
- [x] Duplicate widget I accidentally created in `demos/eviction/prompts/` deleted
- [x] Pre-demo checklist added to top of `demo-script.md` with verifiable URLs for Tab A and Tab B
- [x] Setup section in `demo-script.md` updated with correct widget path (`demos/eviction/widget/`)
- [x] Repo confirmed public at `github.com/andrewmichaelcohen-a2j/a2j-ai`

### 🔲 Immediate Next Steps (before GitHub push)
- [ ] Finalize messaging content — overall deck, project paper, 2-pager
- [ ] Run full demo rehearsal in Cowork — time it, confirm triage output is clean
- [ ] Verify Tab A GitHub URL works once eviction files are pushed
- [ ] Delete old `LHC_Demo_Deck_v0.1.pptx` from `plugins/eviction-defense/` (pre-push cleanup)
- [ ] Commit + push all eviction files (GitHub Desktop): demo, slides, rules, widget
- [ ] Update README.md to reflect eviction-first / rules-as-infrastructure framing (not plugin marketplace)
- [ ] Confirm repo is public after push (it already is, just verify eviction files appear)

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
