# A2J AI — Project State of Record
**Ingest this file at the start of every Cowork session for full project context.**
**Generated:** June 14, 2026 · **Next update:** after each significant session

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
| Last commit | 2026-06-11 — `update ca rules json file` |

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
│   │   └── eviction_schema_v1.0.json        ← Canonical schema
│   ├── eviction/                             ← 51 jurisdiction files (see Section 3)
│   │   ├── alabama/al_eviction_v1.json
│   │   ├── alaska/ak_eviction_v1.json
│   │   ├── ... [all 50 states + DC]
│   │   └── wyoming/wy_eviction_v1.json
│   └── validation/
│       ├── battery/validate.py               ← Layers 1–6 runner (see Section 4)
│       └── reports/
│           ├── validation_report_20260601_232614.json
│           └── validation_report_latest.json ← Most recent run
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
    ├── PROJECT_STATE_OF_RECORD.md           ← This file
    ├── PROJECT_STATUS_JUNE2026.md           ← Older; superseded by this file
    ├── Review_Slides_v0.1.pptx
    ├── Review_Slides_v0.2.pptx
    ├── REVIEWER_CHECKLIST.md
    └── STATUS_LABELS.md
```

---

## 3. Rules File Inventory — Eviction (51 Jurisdictions)

**Validation last run:** 2026-06-01T23:26:14Z  
**All 51 files:** `validation_status = DRAFT` · `reviewer = null` · `last_updated = 2026-06-01`  
**Schema version:** `eviction-v1` throughout  
**Library stats:** mean nonpayment notice period = 7.3 days · median = 5 days

| State | File | Statutory Retrieved? | L3 | L5 |
|-------|------|---------------------|----|----|
| AL | al_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| AK | ak_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| AZ | az_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| AR | ar_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| CA | ca_eviction_v1.json | ✅ RETRIEVED | ✅ PASS | ✅ PASS |
| CO | co_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| CT | ct_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| DC | dc_eviction_v1.json | ❌ PENDING | ✅ PASS | ⚠️ FLAG (30-day period >2× median) |
| DE | de_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| FL | fl_eviction_v1.json | ✅ RETRIEVED | ✅ PASS | ✅ PASS |
| GA | ga_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| HI | hi_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| ID | id_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| IL | il_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| IN | in_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| IA | ia_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| KS | ks_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| KY | ky_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| LA | la_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| ME | me_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| MD | md_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| MA | ma_eviction_v1.json | ❌ PENDING | ✅ PASS | ⚠️ FLAG (14-day period >2× median) |
| MI | mi_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| MN | mn_eviction_v1.json | ❌ PENDING | ✅ PASS | ⚠️ FLAG (14-day period >2× median) |
| MS | ms_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| MO | mo_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| MT | mt_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| NE | ne_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| NV | nv_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| NH | nh_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| NJ | nj_eviction_v1.json | ❌ PENDING | ✅ PASS | ⚠️ FLAG (30-day period >2× median) |
| NM | nm_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| NY | ny_eviction_v1.json | ✅ RETRIEVED | ✅ PASS | ⚠️ FLAG (14-day period >2× median) + L3 WARNING (cure_or_quit.days=10 < pay_or_quit.days=14) |
| NC | nc_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| ND | nd_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| OH | oh_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| OK | ok_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| OR | or_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| PA | pa_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| RI | ri_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| SC | sc_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| SD | sd_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| TN | tn_eviction_v1.json | ❌ PENDING | ✅ PASS | ⚠️ FLAG (14-day period >2× median) |
| TX | tx_eviction_v1.json | ✅ RETRIEVED | ✅ PASS | ✅ PASS |
| UT | ut_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| VT | vt_eviction_v1.json | ❌ PENDING | ✅ PASS | ⚠️ FLAG (14-day period >2× median) |
| VA | va_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| WA | wa_eviction_v1.json | ❌ PENDING | ✅ PASS | ⚠️ FLAG (14-day period >2× median) + L3 WARNING (cure_or_quit.days=10 < pay_or_quit.days=14) |
| WV | wv_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| WI | wi_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |
| WY | wy_eviction_v1.json | ❌ PENDING | ✅ PASS | ✅ PASS |

**Statutory retrieval confirmed for:** CA (CCP §1161; Civ. Code §1946.2), TX (Prop. Code §24.005; SB 38), NY (RPAPL §711, §735; HSTPA 2019; Good Cause Eviction Law 2024), FL (§83.56). All 4 via Legal Data Hunter or direct legislature website.  
**Note on L5 flags:** The 8 flagged states (DC 30 days, MA/MN/NJ 30 days, NY/TN/VT/WA 14 days) likely reflect genuine statutory outliers, not errors — but each needs attorney confirmation. DC and NJ 30-day periods are well-established; others require spot-check.

---

## 4. Validation Harness Status (Layers 1–6)

**Script:** `rules/validation/battery/validate.py`  
**Last run:** 2026-06-01T23:26:14Z · All 51 files  
**Run command:** `python3 rules/validation/battery/validate.py --report`

| Layer | Name | Implementation | Last-Run Results | Coverage |
|-------|------|---------------|-----------------|----------|
| **L1** | Statutory grounding | ✅ Implemented (checks `statutory_retrieved` flag; calls LDH if enabled) | 4 RETRIEVED / 47 PENDING | 8% (4/51) |
| **L2** | Multi-model consensus | ⚠️ Scaffolded — NOT RUN | 0/51 run (requires separate multi-model runner not yet built) | 0% |
| **L3** | Internal consistency | ✅ Fully implemented (~40 checks per file) | 51/51 PASS · 2 WARNINGS (NY, WA: cure_or_quit days < pay_or_quit days) · 0 ERRORS | 100% |
| **L4** | Golden set testing | ⚠️ Scaffolded — NOT RUN | 0/51 have golden sets (need authoring) | 0% |
| **L5** | Cross-jurisdiction | ✅ Implemented (outlier detection vs. library median) | 43/51 PASS · 8/51 FLAGS (L5-PERIOD-HIGH) · 0 ERRORS | 100% |
| **L6** | Temporal freshness | ⚠️ Scaffolded — NOT RUN | Requires legislative feed integration / CI hook | 0% |
| **L7** | Attorney review | 🔴 Not started | 0/51 validated | 0% |

**Summary:** L3 and L5 are fully operational. L1 partially runs (4 states have retrieval; 47 flagged for retrieval). L2, L4, L6 are scaffolded in the script but require additional infrastructure or data to run. L7 has not started.

**Divergence counts:** 0 L3 errors across 51 files. 2 L3 warnings (NY, WA). 8 L5 period-high flags.  
**Anomaly flags requiring follow-up:**
- NY: cure_or_quit.days (10) < pay_or_quit.days (14) — verify with RPAPL §711
- WA: cure_or_quit.days (10) < pay_or_quit.days (14) — verify with RCW 59.12.030

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

**Known gap in README:** The "repository structure" section still shows the old `a2j-ai-claude/` path. Actual root is `a2j-ai/`. Low priority but should be corrected before next major outreach push.

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

**Source:** `git log` · June 1–14, 2026

| Date | Commit | What changed |
|------|--------|-------------|
| 2026-06-11 | `update ca rules json file` | CA eviction rules file updated (exact changes not annotated in commit) |
| 2026-06-10 | `update demo` (×2) | Demo assets updated — likely widget or slide iteration |
| 2026-06-10 | `Update demo-script.md` | Demo script updated — v5 current |
| 2026-06-10 | `Update RulesComparisonWidget.html` | Widget HTML updated |
| 2026-06-10 | `demo updates` (×2) | Additional demo asset updates |
| 2026-06-09 | `demo updates` (×3) | Further demo iteration |
| 2026-06-09 | `process updates` | Process/workflow updates |
| 2026-06-09 | `update eviction notice widget for demo` | Widget update specifically for demo rehearsal |
| 2026-06-08 | `Update demo-script.md` | Demo script update |
| 2026-06-08 | `updated eviction prototype demo script` | Earlier demo script version |
| 2026-06-04 | `fixes to address file name changes and slight demo flow updates` | File reference cleanup |
| 2026-06-02 | `project checklist` | PROJECT_STATUS_JUNE2026.md created |
| 2026-06-02 | `Restructure repo: plugins/, rules/, demos/; 51-state rules library; attribution` | Major restructure commit |

**Net: Most recent work (June 8–11) has been demo iteration** — script, widget, and CA rules file refinements. The 51-state rules library and validation harness have not changed since June 1.

---

## 8. Open Issues / Known Defects

### Demo — Blocking for Recording
- [ ] **Demo rehearsal not completed.** Full 6-scene flow needs one clean end-to-end run in Cowork before recording. Scenes 3–4 (Orozco + live rules attachment) are highest-risk — practice these first.
- [ ] **Demo not yet recorded.** No Loom link exists. Slide 7 placeholder `[ link to demo ]` not yet filled.
- [ ] **Scene 4 file to attach:** The script says to attach `ca_eviction_rules_v0.1.json` — this is in `plugins/eviction-defense/jurisdictions/`. Confirm this file is still the one you want to use in the demo (vs. `rules/eviction/california/ca_eviction_v1.json`). The plugin-local file is the demo-purpose file; the `rules/` file is the canonical one. Decide which appears in the demo before recording.

### Repo — Cleanup Needed
- [ ] **`plugins/eviction-defense/LHC_Demo_Deck_v0.1.pptx`** still in repo. Old deck with LHC naming. Delete before next push.
- [ ] **README path error.** Shows `a2j-ai-claude/` as root; actual root is `a2j-ai/`.
- [ ] **Demo script canonical copy:** `plugins/eviction-defense/prompts/demo-script.md` and `demos/eviction/prompts/demo-script.md` may diverge. The `demos/` copy is canonical; the `plugins/` copy may be stale.

### Validation Pipeline — Not Blocking But Needs Work
- [ ] **L2 (multi-model consensus):** Not implemented. Needs a runner that queries a second model (e.g., GPT-4) on the same rules questions and compares outputs. Infrastructure not yet designed.
- [ ] **L4 (golden sets):** 0/51 states have golden sets. Need at least CA and TX for meaningful L4 testing before outreach. See `test-cases/README.md` for format.
- [ ] **L6 (temporal freshness):** Scaffolded but not runnable. Needs a legislative feed or scheduled check against the citing statute URLs.
- [ ] **L7 (attorney validation):** Not started. CA is the priority first state. Need to recruit one licensed CA tenant attorney. See `docs/REVIEWER_CHECKLIST.md` for the protocol.
- [ ] **NY and WA L3 warnings:** `cure_or_quit.days < pay_or_quit.days` — both 10 vs. 14. Likely correct (NY RPAPL requires shorter notice for lease violations vs. nonpayment) but needs attorney confirmation.
- [ ] **8 L5-PERIOD-HIGH flags** (DC, MA, MN, NJ, NY, TN, VT, WA): All are plausibly correct outliers given those states' tenant-protective laws, but each should be spot-checked by an attorney during L7 review.

### Strategic / Project Level
- [ ] **Formal paper:** Not started. Raw material exists in Cowork session transcripts.
- [ ] **2-pager:** Not started.
- [ ] **Substack / website:** Not set up.
- [ ] **Margaret/Stanford pitch:** Deck ready; 2-pager and paper not yet done. Send after paper review.
- [ ] **Content identity decision:** Personal name vs. A2J project brand — decide before Substack/website setup.

---

## 9. How to Resume Work in a New Session

**Standard brief:** "Please read `docs/PROJECT_STATE_OF_RECORD.md` from the a2j-ai repo."

**If working on demo rehearsal / recording:**
> "Read the State of Record, then open `demos/eviction/prompts/demo-script.md` and help me run a rehearsal. I need to practice Scenes 3 and 4 especially."

**If working on validation:**
> "Read the State of Record, then run `rules/validation/battery/validate.py --report` to see current validation status, and let's work on [L1 retrieval for TX / building L4 golden sets for CA / NY+WA L3 warnings]."

**If working on the paper or 2-pager:**
> "Read the State of Record. I want to start drafting the formal paper. The key source material is in our previous Cowork sessions — the AI layer vs. rules layer discussion, the certification maturity model, the liability architecture, and the LSC governance parallel."

---

*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*  
*State of Record generated by Claude (Cowork) — June 14, 2026. Replace this file at the start of each session after significant work.*
