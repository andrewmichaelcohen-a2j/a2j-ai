# A2J AI — Project State of Record
**Ingest this file at the start of every Cowork session for full project context.**
**Generated:** June 15, 2026 · **Last updated:** 2026-07-16 (No-run cycle with a NEW anomaly: **the launchd dispatcher did not fire overnight** — no 07-16 entry in launchd_stdout.log [last write 07-15 ~2:24 AM], no new dispatch log. First dispatcher-side missed fire since the 06-25 FDA fix; all prior cadence anomalies were report-side. No substantive loss [queue was intentionally empty — Northgate retry #3 still HELD on the Gemini-DNS RED], but Andy should check machine power/launchctl before anything is re-queued; folded into the standing infrastructure RED. Report-side: fired on time at 8:00 AM. No new output, no rule changes, no metric movement since run 9ae49b97 [ingested 07-09]. State carried: VT 1 MV [Gokey] + 1 CI [Houle], module effectively complete; cumulative MV=26/CI=4/RC=6; two YELLOW fixes live-verified 07-09 [extended search backoff ladder; FLAG-generate-failed→PR routing]; Broaden Proof 1 still BLOCKED on Andy's v0.3 freeze [28 draft items].) · **Next update:** after v0.3 freeze, DNS/dispatcher diagnosis, or next overnight run

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
| Last commit | 2026-06-16 — overlays cleanup, coverage audit, L5 xstate check (pushed via GitHub Desktop); five-module build + L5 outlier resolution + MN/NJ corrections pending commit |

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
│       ├── l2/                              ← ✅ NEW (2026-06-18)
│       │   ├── l2_runner.py                ← L2 multi-model consensus runner (gpt-5.5 + gemini-2.5-pro)
│       │   ├── l2_reasoning_pass.py        ← L2 period-divergence reasoning pass; writes AI-resolved or L7 flags
│       │   ├── l2_phase2_runner.py         ← Phase 2 full 43-state runner (2026-06-18)
│       │   ├── l2_phase2_retry.py          ← Retry runner for GPT parse-error pseudo-splits (2026-06-18)
│       │   ├── l2_ga_straggler.py          ← GA targeted clean retry (conflict-framing artifact fix)
│       │   ├── add_interoperability.py     ← JusticeBench tagging pass (all 51 v2 files)
│       │   ├── l2_service_runner.py        ← ✅ NEW (2026-06-19) — Service module L2 runner (51 states)
│       │   ├── l2_service_reasoning.py     ← ✅ NEW (2026-06-19) — Service reasoning/tiebreaker/single-model-fallback
│       │   └── l2_service_l7_escalate.py   ← ✅ NEW (2026-06-19) — L7 escalation for DC/NM (API failure)
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
    ├── HUMAN_REVIEW_QUEUE.md                ← ✅ NEW — attorney review queue; append-only by runner; Andy owns resolution fields
    ├── L2_CONSENSUS_REPORT_2026-06-18.md   ← ✅ NEW — L2 Phase 1 results (8 states)
    ├── L2_CONSENSUS_REPORT_PHASE2_2026-06-18.md ← ✅ NEW — L2 Phase 2 + retry results (43 states + 9 retry)
    ├── VALIDATION_PHILOSOPHY.md             ← ✅ NEW — validation philosophy (for paper/deck)
    ├── L7_TRIAGE_LIST_2026-06-16.md        ← L7 triage (264 entries; substantive_defenses)
    ├── PROJECT_PLAN.md                      ← Master project plan (Claude does NOT edit)
    ├── PROJECT_STATE_OF_RECORD.md           ← This file (Claude updates each session)
    ├── PROJECT_STATUS_JUNE2026.md           ← Older; superseded by this file
    ├── Review_Slides_v0.1.pptx
    ├── Review_Slides_v0.2.pptx
    ├── REVIEWER_CHECKLIST.md
    ├── JUSTICEBENCH_ALIGNMENT_SPEC.md       ← ✅ NEW — JusticeBench alignment spec
    ├── JUSTICEBENCH_VERIFIED_CODES.md       ← ✅ NEW — confirmed FIPS/LIST/task-taxonomy codes (implement from here only)
    ├── SCHEMA_V2_DESIGN_SPEC.md            ← ✅ UPDATED (June 18) — Schema v2 additions: notice_required/exceptions/null days + interoperability block
    └── STATUS_LABELS.md                     ← ✅ UPDATED to v2 (module-level + guardrails)
```

---

## 3. Rules File Inventory — Eviction (51 Jurisdictions)

### v2 Summary (current)

**Schema:** `eviction-v2` · **5 modules per file:** `notice`, `service`, `overlays`, `substantive_defenses`, `procedural_defects`  
**Validation last run:** 2026-06-16 (MN + NJ corrections — library: **51 ACP / 0 DRAFT**); L2 Phase 1 run 2026-06-18 (8 machine-assist flag states — notice/pay_or_quit)  
**Layers run:** L1, L3, L5 fully · L2 partially (Phase 1: 8 states; notice module only) · L4/L6: `not_implemented`  
**file_status rule:** `min(module_status)` — enforced by `validate.py`

| Metric | Count |
|--------|-------|
| Total v2 files | 51 |
| L3 PASS | 51 / 51 |
| L1 retrieved (statutory text statutorily retrieved) | **51 / 51** (CA/TX/NY/FL Wave 0 + 40 Wave 1/2 + 7 Wave 3 — all complete) |
| file_status = AUTOMATED-CHECKS-PASSED | **51** (100% — MN +1 re-validation 2026-06-16; NJ +1 content correction 2026-06-16, attorney-confirmed Andrew Cohen) |
| file_status = DRAFT | **0** |
| Five-module build | **Complete (2026-06-16)** — 789 field updates across 51 files; 0 [VERIFY] remaining |
| L5 outlier resolution | **Complete (2026-06-16)** — Andrew Cohen attorney review of all 7 DRAFT states; 5 confirmed (DC, MA, TN, VT, WA) advanced to ACP; MN citation corrected + re-validated; NJ substantive correction implemented — all 51 now ACP |
| Schema v2 additions | `notice_required` (boolean) + `exceptions` array + null `days` support added 2026-06-16 — see `docs/SCHEMA_V2_DESIGN_SPEC.md` |
| JusticeBench interoperability tags | ✅ COMPLETE 2026-06-18. All 51 v2 files tagged: `fips_jurisdiction` (2-digit FIPS), `language` (["en"]), `task_taxonomy_ids` (TS-03-04/01-07/01-05/05-05/03-02/05-04 — confirmed from justicebench.org/task), `list_codes` (all 8 HO codes — confirmed from taxonomy.legal). Script: `rules/validation/l2/add_interoperability.py`. Tags are additive metadata — do not change decision logic or validation status. |
| LIST subcodes | ✅ ALL CONFIRMED. Subcodes -01 (Notice/Procedural), -02 (Disability/RA), -03 (Habitability), -04 (Military), -05 (Title) confirmed 2026-06-18 (Andy browser check at taxonomy.legal HO-02-04). No pending items. |
| L7 triage entries | **264** — all in substantive_defenses; grounding_gap / specialist_required (see `docs/L7_TRIAGE_LIST_2026-06-16.md`) |

**States at AUTOMATED-CHECKS-PASSED (49):**

| State | Key citation statutorily retrieved | Source |
|-------|------------------------------------|--------|
| CA | CCP §1161 | Prior session |
| TX | Tex. Prop. Code §24.005 | Prior session |
| NY | RPAPL §711 | Prior session; L5 flag present but ACP |
| FL | Fla. Stat. §83.56 | Prior session |
| AK | AS §34.03.220 | Justia |
| AL | Ala. Code §35-9A-421 | Justia |
| AZ | A.R.S. §33-1368 | Justia |
| CO | C.R.S. §13-40-104 | Justia |
| CT | Conn. Gen. Stat. §47a-23 | Justia |
| DE | Del. Code tit. 25 §5501 | Justia |
| GA | O.C.G.A. §44-7-50 | Justia |
| HI | HRS §521-68 | Justia |
| ID | Idaho Code §6-303 | Justia |
| IN | Ind. Code §32-31-1-6 | Justia |
| KS | K.S.A. §58-2564 | Justia |
| KY | KRS §383.660 | Justia |
| LA | La. C.C.P. Art. 4701 | Justia |
| MD | Md. Code, Real Prop. §8-401 | Justia |
| ME | 14 M.R.S. §6001 | Justia — machine-assist: pay-or-quit period in §6002; **L2 CONSENSUS-CONFIRM** (2026-06-18): both GPT + Gemini independently confirmed §6002, 7-day period — pending human confirmation |
| MI | MCL §554.134 | michigan.gov |
| MO | RSMo §441.050 | MO Revisor — machine-assist: §441.050 is termination statute; nonpayment in §535.020; **L2 PERIOD-DIVERGENCE → L7 ESCALATED** (2026-06-18): no model convergence — GPT says notice_required=false (§535.020.1), Gemini says notice_required=true (§535.020); attorney review required (is §535.020 demand a notice or just a precondition?) |
| MS | Miss. Code Ann. §89-7-23 | Justia — machine-assist: §89-7-23 excludes RLTA tenancies (§89-8 et seq.); **L2 CITATION-DIVERGENCE → AI-RESOLVED** (2026-06-18): corrected to §89-8-13(5)(a) (Chapter 8 RLTA — operative residential nonpayment provision; verified Justia); period 3d confirmed; pending human confirmation |
| MT | MCA §70-24-422 | Justia |
| NC | N.C. Gen. Stat. §42-3 | ncleg.gov |
| ND | NDCC §47-16-15 | FindLaw — machine-assist: §47-16-15 is termination statute; pay-or-quit authority unclear; **L2 MODEL-SPLIT → L7 ESCALATED** (2026-06-18): GPT says 3-day formal notice required (§47-32-02); Gemini says no notice required, landlord may file 3 days after rent due (§47-32-02) — genuine interpretive split on same statute; attorney must resolve whether 3-day period is a notice requirement or a ripening period |
| NE | Neb. Rev. Stat. §76-1431 | nebraskalegislature.gov |
| NH | RSA 540:3 | gencourt.state.nh.us |
| NM | NMSA §47-8-33 | Justia |
| NV | NRS §40.253 | nevada.public.law |
| OH | ORC §1923.02 | Justia — machine-assist: 3-day notice period in §1923.04; **L2 CITATION-DIVERGENCE → AI-RESOLVED** (2026-06-18): corrected to ORC §1923.04(A) (operative pre-filing notice provision; verified codes.ohio.gov); period 3d confirmed; pending human confirmation |
| OK | 41 O.S. §131 | Justia |
| OR | ORS §90.394 | oregon.public.law |
| RI | R.I. Gen. Laws §34-18-35 | FindLaw |
| VA | Va. Code §55.1-1245 | law.lis.virginia.gov |
| WI | Wis. Stat. §704.17 | Justia |
| WV | W. Va. Code §37-6-5 | Justia — machine-assist: §37-6-5 is termination statute; pay-or-quit authority unclear; **L2 PERIOD-DIVERGENCE → AI-RESOLVED** (2026-06-18): both models (high confidence) say notice_required=false, §55-3A-1 (summary eviction — no prior notice period); file corrected (days=null, statute=§55-3A-1); pending human confirmation |
| WY | Wyo. Stat. §1-21-1002 | Justia |
| DC | D.C. Code §42-3505.01(a-1)(1) | Confirmed by attorney review 2026-06-16 (Andrew Cohen) — 30-day nonpayment notice when rent owed ≥ $600 |
| MA | MGL c. 186 §11 | Confirmed by attorney review 2026-06-16 (Andrew Cohen) — 14-day; §12 parallel for tenancies-at-will |
| TN | TCA §66-28-505(a)(2) | Confirmed by attorney review 2026-06-16 (Andrew Cohen) — 14-day; URLTA counties >75k pop only |
| VT | 9 V.S.A. §4467(a) | Confirmed by attorney review 2026-06-16 (Andrew Cohen) — 14-day; H.772 pending (L6 monitor) |
| WA | RCW 59.12.030(3) + 59.18.057 | Confirmed by attorney review 2026-06-16 (Andrew Cohen) — 14-day pay-or-quit; 10-day cure_or_quit is lease-violation comply-or-vacate (L3 warning resolved false positive) |
| MN | Minn. Stat. §504B.321 subd. 1a | Citation corrected from §504B.285 → §504B.321 subd. 1a (Andrew Cohen, 2026-06-16); 14-day period confirmed; L5 flag marked resolved-confirmed; re-validated 2026-06-16 |
| NJ | N.J.S.A. §2A:18-61.1 + §2A:18-61.2 | No statutory nonpayment notice period (§2A:18-61.2 carve-out — immediate filing for market-rate); notice_required=false; days=null; exceptions[federally_subsidized_housing]=14 days; 30-day incorrect value removed. Content correction attorney-confirmed: Andrew Cohen, 2026-06-16. Note: §2A:18-56 (termination statute) carries L1-URL-NOT-RESOLVED flag — future verification item, not part of this correction. |
| AR | Ark. Code Ann. §18-17-701 | Justia (subtitle-2 path) — 5-day pay-or-quit |
| IA | Iowa Code §562A.27 | Justia (2022 with title-xiv path) — 3-day pay-or-quit |
| IL | 735 ILCS 5/9-207 | FindLaw — machine-assist: §9-207 is holdover/termination statute; pay-or-quit is §9-209 (unretrieval); **L2 CONSENSUS-CONFIRM** (2026-06-18): both models confirmed 5-day period under §9-209; pending human confirmation of statute identity |
| PA | 68 Pa. C.S. §250.501 | FindLaw (as 68 P.S. §250.501) — 10-day pay-or-quit |
| SC | SC Code §27-40-710 | Justia (2024) — 5-day pay-or-quit |
| SD | SDCL §21-16-1 | Justia (chapter-16 path) — machine-assist: FED grounds statute; nonpayment in subsection (4); **L2 CONSENSUS-CONFIRM** (2026-06-18): both models confirmed 3-day period under §21-16-1; pending human confirmation |
| UT | Utah Code §78B-6-802 | Justia (2020, part-8/section-802 path) — 3 business day pay-or-quit explicit in statute |

**States at DRAFT: 0** — all 51 jurisdictions are AUTOMATED-CHECKS-PASSED as of 2026-06-16.

**v1 files:** Still present alongside v2 files. v1 is notice-centric (pre-5-module schema). Do not delete.

---

## 4. Validation Harness Status

**Script:** `rules/validation/battery/validate.py` ← **UPDATED June 15, 2026 (v2-aware)**  
**Run command:** `python3 rules/validation/battery/validate.py [--state CA] [--no-writeback] [--report]`

### v2 Validation Architecture

| Layer | Name | Status | v2 Result (2026-06-15) |
|-------|------|--------|------------------------|
| **L1** | Statutory grounding | ✅ Operational | **51 pass / 0 fail** (Wave 3 complete 2026-06-15 — all 51 states retrieved) |
| **L2** | Multi-model consensus | ✅ Notice module COMPLETE (2026-06-18) · ✅ **Service module COMPLETE (2026-06-19/20)** | **Notice/pay_or_quit (51):** 41 CONFIRM · 5 AI-resolved (attorney-confirmed) · 4 L7-open (MO, ND, MD, GA) · 2 attorney-resolved (SD statute-repeal, VA time-versioned). **Service module (51):** 16 round-1 confirm · 32 AI-resolved (reasoning/tiebreaker/single-model) · 2 L7 (DC, NM — API failure, zero model data) · CA L6-RECENCY-WATCH. Runners: `l2_service_runner.py`, `l2_service_reasoning.py`, `l2_service_l7_escalate.py`. |
| **L3** | Internal consistency | ✅ Operational | 51/51 PASS · 0 errors · 2 warnings (NY, WA) |
| **L4** | Golden-set tests | ⚠️ not_implemented | — |
| **L5** | Cross-jurisdiction anomaly | ✅ Operational | **51 ACP / 0 DRAFT** (2026-06-16). L5 outlier resolution complete: 5 confirmed states (DC, MA, TN, VT, WA) advanced; MN re-validated (citation §504B.321 subd. 1a, flag resolved-confirmed); NJ content-corrected (no-notice-period pattern, days=null, notice_required=false, exceptions array). validate.py updated to suppress resolved-* flags and recognize notice_required=false. **L5-LOCAL-XSTATE sub-check**: all 51 states pass clean. NJ advance confirmed: Andrew Cohen, 2026-06-16. |
| **L6** | Temporal freshness | ⚠️ not_implemented | — |
| **L7** | Attorney review | 🔴 Not started | 0/51 modules attorney-reviewed · **triage list generated 2026-06-16** (264 entries, all substantive_defenses — see `docs/L7_TRIAGE_LIST_2026-06-16.md`) |

### Three enforced guardrails (new in v2)

1. **G1 — No auto-advance:** Any module at UNDER REVIEW/VALIDATED/CERTIFIED with `reviewer=null` is a hard validation FAIL. No automated process may advance past AUTOMATED-CHECKS-PASSED.
2. **G2 — file_status = min(module_status):** `validate.py` computes and writes back the correct `file_status` on every run. Never set directly.
3. **G3 — Option-A gate:** A module advances to AUTOMATED-CHECKS-PASSED only when all currently-implemented layers (today: L1, L3, L5) pass with no errors. `not_implemented` layers don't block. L2 AI-resolved items stay at ACP with a `pending-human-confirmation` flag; they never advance further via AI resolution alone.

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
**Status:** Script finalized; **recording complete — Loom: https://www.loom.com/share/8f1274d5a3d74a4bb4ca8a5181fde3dc**

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

**Demo link:** https://www.loom.com/share/8f1274d5a3d74a4bb4ca8a5181fde3dc — recorded and live. Slide 7 placeholder updated.

---

## 7. Changelog — Past Two Weeks (Cowork Activity)

**Source:** `git log` + this session · June 1–15, 2026

| Date | What changed |
|------|-------------|
| **2026-06-23** | **Holdings v3 runner built — generate-from-source (per direction doc)** |
| | **Runner:** `rules/validation/l2/retaliation_holdings_v3_runner.py` — NEW FILE (v2 preserved for CA provenance). |
| | **Architecture:** Sequential generate-then-verify. Model 1 (Gemini): generates holding characterization + candidate quote from retrieved opinion text only — does NOT see draft holding. Model 2 (GPT, different model): verifies Gemini's characterization against text, checks if quote is verbatim + on-point, reconciles against draft holding. C passes only if GPT confirms characterization as accurate/partially_accurate. D derived from C outputs — no additional LLM call. |
| | **Two-queue routing:** CONFIRM-INFERENCE (C=corroborated, D=INFERRED — cheap, delegable); RE-CHARACTERIZE (C=FLAG — source-generated holding carried to queue); WRONG-DOC (A=FLAG-citation-mismatch). |
| | **Independence:** `GENERATE_MODEL = "gemini:gemini-2.5-pro"` / `VERIFY_MODEL = "gpt:gpt-4o"` — different models, recorded per-case in output JSON. |
| | **Passing standard unchanged:** A=true + B=OK-machine + C=corroborated + D=STATED/STATED-single-model/INFERRED. Nothing promoted across attorney line. |
| | **Triage (Step 2) — 10 C=FLAG-inaccurate cases from batch 1 (d5444e58):** N=5 (50%), W=3 (30%), I=2 (20%). N-type (CL wrong doc): AZ DVM, AZ Visco, DC Edwards, DC Hosey, DC DeSzunyogh. W-type (wording artifact, recoverable by v3): DC Twyman, DC Robinson, IA Hillview. I-type (genuinely inaccurate draft): DC Gomez, IA Lewis. v3 should recover the W-types. N-types go to WRONG-DOC queue; I-types to RE-CHARACTERIZE with source-generated holding. |
| | **Ready to run.** See §8 for terminal commands. |
| **2026-06-22 (late)** | **33-state holdings run — FAILED (quota exhaustion)** |
| | **Run `a86b3598`:** 33 states, 102 cases, 0/102 machine-verified (0%). All cases returned `A=FLAG, B=UNVERIFIED-no-citator, C=FLAG, D=INFERRED` — CourtListener session quota was exhausted from the earlier CA canonical run. Every Check A search 429'd even with 3/6/12/24/48s retry. Not a runner bug — runner correctly marked all as needs-attorney. **Do not ingest `a86b3598`.** |
| | **Root cause:** Session quota depleted by morning CA runs. The 10s inter-case sleep prevents in-run exhaustion but does not reset session quota across back-to-back runs. |
| | **Fix:** Run the 33-state batch first thing tomorrow (fresh session quota). Optionally batch into 3 × ~11 states with 30-min gaps. Consider requesting higher CL rate limits or acquiring a second token for parallel runs. |
| | **Commit (Task #52) is next** before re-running. See commit list in §8. |
| **2026-06-21/22** | **Holdings verification layer — retaliation module (Step 2 holdings)** |
| | **Runner built:** `rules/validation/l2/retaliation_holdings_v2_runner.py` — 4-check authoritative-source verification (Check A: existence+citation via CourtListener search; Check B: currency via citing-opinion scan; Check C: holding characterization accuracy via two-model comparison against retrieved opinion text; Check D: control determination — STATED-with-quote vs. INFERRED). CourtListener REST API (`/api/rest/v4/`) used directly from Terminal with token. |
| | **Build-check B passed:** Fake cite `Orozco v. Casimiro, 12 Cal.5th 100 (2023)` correctly returned NOT FOUND / NOT VERIFIED — authoritative source fails closed on hallucinated citations. |
| | **CA test runs (6 retaliation cases):** Multiple runs executed. Best honest runner result: **2/6 machine-verified (33%)** in run `6a1788c6`. True machine-verified rate confirmed at **5/6 (83%)** via MCP supplemental verification (CourtListener MCP used to directly verify the 3 dropped cases). |
| | **Cases verified (MCP-supplemented):** Schweiger (1970) → needs-attorney (D=INFERRED — foundational case, no element enumeration; architecturally correct); S.P. Growers (1976) → machine-verified (citation fallback, 38 citing); Barela (1981) → machine-verified (55 citing); Drouet (2003) → machine-verified (STATED quote confirmed); Aweeka (1971) → machine-verified (STATED-single-model); Western Land (1985) → machine-verified (STATED, burden-shifting rule stated). |
| | **Root cause for runner gap:** `cl_get_opinion_id_for_cluster()` had no 429 retry — silently returned None on rate limit, leaving S.P. Growers/Barela/Western Land without opinion IDs → fell back to caption-only snippets → C=FLAG-inaccurate. **Fix applied:** 5-retry exponential backoff (3/6/12/24/48s), removed `oid != cluster_id` guard, added 1s breathing room before call. |
| | **Rate limiting issue (session-end blocker):** Final run (`96494b27`) got 0/6 — CourtListener quota exhausted from running multiple CA runs in one evening. Fix prepared: increase inter-case sleep from 3s → 10s in `verify_case()`. Re-run needed next session with fresh CL quota. |
| | **Fixes applied to runner (cumulative):** (1) `GEMINI_API_KEY` → fallback to `GOOGLE_API_KEY`; (2) `thinking_budget=0` → `512` (invalid for gemini-2.5-pro); (3) 5-retry exponential backoff on all CL search calls; (4) Citation-based fallback search strategy in `cl_search_case()` to handle wrong-case name returns (S.P. Growers) and persistent 429s; (5) `cl_get_opinion_id_for_cluster()` 429 retry; (6) Inter-case sleep increased to 3s (needs 10s next run). |
| | **Output files (do not overwrite — provenance):** Best run: `rules/validation/l2/output/retaliation_holdings_v2_1states_2026-06-22_6a1788c6.json` (2/6 MV, honest runner output). All prior runs preserved with unique UUIDs. |
| | **Canonical result (run ce5c9748, 2026-06-22):** 4/6 machine-verified (67%). MV: Schweiger (STATED-single-model), Barela (STATED), Drouet (STATED), Western Land (STATED). NA: S.P. Growers (C=FLAG — CL returned caption only, no opinion body), Aweeka (C=FLAG — CL text fetch returned empty this run; MCP confirms verifiable; true rate 5/6). Ingested to `ca_eviction_v2.json` + `VALIDATION_METRICS_LEDGER.md`. |
| | **Next:** (1) Commit (Task #52); (2) Re-run 33-state holdings fresh tomorrow morning; (3) Build audit sampler. |
| **2026-06-20** | **LSC baseline cross-check complete** |
| | **46/51 states (90%) corroborated** against LSC/Temple LawAtlas State Eviction Laws dataset (Jan 2021, inter-coder reliability, congressionally funded). 44 MATCH-PERIOD + 2 MATCH-NO-NOTICE (NJ, WV). |
| | **3 post-2021 divergences** (MN: 14d added by 2023 Housing Omnibus; SD: §21-16-2 repealed by SB 90 2024; VA: time-versioned 5d current/14d from 2026-07-01). CJaC reflects current law; LSC frozen at 2021. These demonstrate the recency advantage claim. |
| | **2 L7-corroborations** (GA: LSC="not specified" supports Gemini no-minimum L7 position; MD: LSC="not required" supports Gemini no-notice L7 position). Both corroborations fed to attorney review queue. |
| | **No unexplained divergences.** Zero cases of a confirmed wrong CJaC value not already flagged by the process. |
| | **New files:** `docs/LSC_CROSSCHECK_REPORT_2026-06-20.md`, `rules/validation/l2/lsc_crosscheck_runner.py`, `docs/LSC_BASELINE_CROSSCHECK_ASSESSMENT.md`. VALIDATION_METRICS_LEDGER.md updated. |
| **2026-06-19/20** | **Service module L2 complete — Task B1 complete** |
| | **51/51 states run** via full tiered protocol: initial 51-state runner → 17-state ERROR retry → reasoning pass (20 review states) → tiebreaker pass (`--retry-l7`, 8 states) → targeted single-state passes (VA, WI, AR, OR, IN via override queries) → L7 escalation (DC, NM). Total spend: ~$4.50. |
| | **Final distribution:** 16 round-1 consensus-confirmed (CT, FL, IL, KY, MD, ME, MI, MN, MS, NE, NY, OH, OK, RI, VT, WY) · 32 AI-resolved via reasoning/tiebreaker/single-model (AK, AL, AR, AZ, CO, DE, GA, HI, IA, ID, IN, KS, LA, MA, MO, MT, NC, ND, NH, NJ, NV, OR, PA, SC, SD, TN, TX, UT, VA, WA, WI, WV) · 2 L7 (DC, NM — persistent API failure, zero recoverable model data) · CA L6-SERVICE-RECENCY-WATCH. |
| | **New capabilities built:** (1) Single-model fallback — when one model errors but other is high-confidence, trust high-confidence model and flag as L2-SERVICE-SINGLE-MODEL-RESOLVED. Resolved VA, WI, AR, TN that would otherwise have been false L7s. (2) State-specific override queries — method-by-method subsection questions resolved IN (§32-31-1-9(b)(1)/(2)/(3)) after two failed generic tiebreaker passes. |
| | **New scripts:** `rules/validation/l2/l2_service_runner.py`, `l2_service_reasoning.py`, `l2_service_l7_escalate.py`. DC and NM written L7-SERVICE-ATTORNEY-REVIEW to rules files; queue updated. |
| | **VALIDATION_METRICS_LEDGER.md updated** with full service module table including process-quality notes. |
| **2026-06-19** | **Notice queue resolutions applied — Task B0 complete** |
| | **9 state files updated** per attorney confirmations (Andy Cohen). WV, OH, MS, DE, IL, ME: attorney-confirmed flags added; dispositions updated to `resolved-attorney-confirmed`. NV: count_method corrected from `calendar_days` to `calendar_days_excluding_weekends_holidays` (judicial days — weekends/holidays excluded per §40.253(1)(a)). SD: NJ-pattern rewrite — notice_required=false, days=null; §21-16-2 was repealed by SB 90 (2024); 3-day ripening period under §21-16-1(4); flag renamed L2-CITATION-AMBIGUOUS-ATTORNEY-RESOLVED. VA: time-versioned — tenancy_all.days=5 current law (§55.1-1245(F)); pending_amendment block added (effective_date=2026-07-01, new_days=14, authority=HB 15/SB 48); flag renamed L2-MODEL-SPLIT-ATTORNEY-RESOLVED. MO, ND, MD, GA: untouched (L7 still pending). |
| | **Error-confirm outcomes logged to VALIDATION_METRICS_LEDGER.md:** 4 AI-resolved items confirmed correct (100%), 2 CONFIRM items confirmed correct; NV count_method miss caught by attorney; SD statute-repeal catch (§21-16-2 non-operative since 2024); VA temporal split resolved. |
| | **Validate.py: 51/51 AUTOMATED-CHECKS-PASSED** — no regressions from all 9 file updates. |
| | **Missing doc:** `docs/STANDARDS_LANDSCAPE_ASSESSMENT.md` referenced in prior sessions but not in repo — needs to be created or Andy confirms not needed. LSC_CASE_STUDY.md and PRIOR_ART_MAP.md are present. |
| **2026-06-18** | **JusticeBench interoperability tags — all 51 v2 files** |
| | **Schema updated:** `interoperability` block added to `eviction_schema_v2.0.json` (after `provenance`, before `validation`). Four fields: `fips_jurisdiction` (string), `language` (array), `task_taxonomy_ids` (array), `list_codes` (array), plus `_list_pending_subcodes` note. Additive only. |
| | **All 51 files populated via `rules/validation/l2/add_interoperability.py`:** FIPS from verified federal table, language=["en"], 6 task taxonomy IDs (TS-03-04/01-07/01-05/05-05/03-02/05-04 — confirmed live from justicebench.org/task June 18), 5 LIST codes (HO-00-00-00-00/HO-02-00-00-00/HO-02-04-00-00/HO-02-04-02-00/HO-02-04-05-00 — confirmed from taxonomy.legal). 51/51 OK. |
| | **NJ trailing comma fixed** (artefact from prior L5 flag removal — `flags` array item 2 had trailing comma). Corrected before population pass. |
| | **3 LIST defense subcodes flagged for Andy's browser check:** "Notice and Procedural defenses," "Living conditions (habitability) defenses," "Military service-members' protections" — confirmed labels, unconfirmed exact child codes under HO-02-04. Tagged at parent interim. See `HUMAN_REVIEW_QUEUE.md`. |
| | **SCHEMA_V2_DESIGN_SPEC.md updated:** Canonical Pattern 3 (interoperability block) documented. Schema version history updated. |
| **2026-06-18** | **L2 Phase 2 Retry + straggler cleanup + queue rebuild** |
| | **Retry (9 states, ~$0.44):** DC, IA, KY, LA, MA → CONFIRM (GPT parse errors resolved with 6000-token budget). AR → CONFIRM on first retry pass (Jun 17 11:55 PM write persists). TN → CONFIRM (first retry pass + attorney-confirmed 14d §66-28-505(b)). |
| | **Genuine L7 from retry (2):** GA (reasoning-pass artifact — straggler script written); VA (GPT 5d vs Gemini 14d, §55.1-1245(F) — genuine interpretive split on tenancy type). |
| | **GA straggler (`l2_ga_straggler.py`):** Clean neutral 8000-token GPT retry script written and syntax-checked. Protocol: if both models agree on neutral query → AI-resolve directly (no reasoning pass); if genuinely disagree → L7. Andy must run from Terminal. |
| | **Queue rebuilt (`docs/HUMAN_REVIEW_QUEUE.md`):** Ownership changed to append-only (runner never touches resolution/status fields — Andy's exclusively). Stale Phase 2 pseudo-L7 entries removed. Final queue: 4 L7 (MO, ND, MD, VA) + 1 straggler pending (GA) + 5 pending-confirmation (WV, OH, MS, DE, NV) + 3 citation-review (SD ambiguous, IL confirmed, ME confirmed). |
| | **True final counts: 41 CONFIRM · 5 AI-resolved pending confirmation · 4 confirmed L7 · 1 straggler pending (GA) · 3 citation-review items.** |
| **2026-06-17** | **L2 Phase 2 run complete — 43 states, ~$0.94** |
| | **Results:** 31 CONSENSUS-CONFIRM · 1 CITATION-AI-RESOLVED (DE: §5501→§5502(a)) · 1 PERIOD-AI-RESOLVED (NV: 5d→7d §40.253(1)(a)) · 8 MODEL-SPLIT-L7-flagged · 2 ERROR |
| | **⚠️ Key finding:** 7 of 8 "model splits" are GPT parse errors (chain-of-thought fills token buffer → days=None, rationale=PARSE_ERROR), not genuine disagreements. Affected: AR, DC, KY, LA, MA, TN, VA. Gemini answered correctly for all 7. Pattern identical to SD Phase 1 (resolved by retry). MD is the only genuine split (GPT: 10d §8-401(b)(2)(i); Gemini: no notice §8-401). |
| | **Action needed:** Write `l2_phase2_retry.py` targeting 9 states (7 parse-error + GA + IA) with higher token budget before treating as L7. |
| | **Report:** `docs/L2_CONSENSUS_REPORT_PHASE2_2026-06-18.md` · **Queue:** 10 items appended to `docs/HUMAN_REVIEW_QUEUE.md` |
| **2026-06-17** | **L2 Phase 2 runner written + supporting docs** |
| | **`rules/validation/l2/l2_phase2_runner.py`:** Full 43-state Phase 2 runner with tiered resolution inline. Imports `call_openai`, `call_gemini`, `build_query`, `classify`, `extract_file_claim`, `load_all_v2_files`, `_extract_section_nums`, `_parse_json_response` from l2_runner.py. Resolution: CITATION-DIV → AI-resolve if models share section nums, else UNRESOLVED flag; PERIOD-DIV → GPT+Gemini reasoning pass (max_completion_tokens=8000), converge→AI-resolve, diverge→L7; MODEL-SPLIT → L7 directly. CLI: `--dry-run`, `--states X,Y,Z`. Skips Phase 1 states automatically. NEVER advances past ACP. |
| | **`docs/HUMAN_REVIEW_QUEUE.md` seeded:** Phase 1 items: MO (L7), ND (L7), WV/OH/MS/IL/ME/SD (pending-confirmation). Phase 2 items appended automatically when runner completes. |
| | **`docs/VALIDATION_PHILOSOPHY.md` created:** Full validation philosophy for paper/deck insertion. Covers: automation-for-coverage/surgical-human principle, tiered resolution protocol, hard guardrail (never blesses), Phase 1 proof point, why-it-advances-the-art, trustworthy-at-scale → A2J through-line. |
| | **IL/ME/SD citation pre-Phase-2 audit:** IL §9-209 confirmed (no change needed; L2-CITATION-CONFIRMED flag added). ME §6002 confirmed (stale error flag removed; L2-CITATION-CONFIRMED added). SD 3d confirmed but citation ambiguous (GPT: §21-16-1(2) vs Gemini: §21-16-2 — cannot auto-resolve; L2-CITATION-AMBIGUOUS flag added, human review required). |
| | **Ready for Andy to run Phase 2 from Terminal and commit all files.** |
| **2026-06-18** | **L2 Multi-Model Consensus — Phase 1 complete (8 machine-assist flag states)** |
| | **Models:** gpt-5.5 (OpenAI) + gemini-2.5-pro (Google) · **Scope:** notice/pay_or_quit · **Budget:** $20 cap (not reached) |
| | **Results:** CONFIRM:2 (ME 7d, IL 5d), CITATION-DIV:2 (OH, MS), PERIOD-DIV:2 (WV, MO), MODEL-SPLIT:2 (ND, SD→re-run→CONFIRM) · 0 ERRORs in final run |
| | **OH (citation AI-resolved):** Corrected ORC §1923.02 → ORC §1923.04(A) — verified from codes.ohio.gov. Both models identified §1923.04(A) as operative pre-filing notice provision. Period 3d confirmed. Pending human confirmation. |
| | **MS (citation AI-resolved):** Corrected §89-7-27 → §89-8-13(5)(a) — verified from Justia. Chapter 8 (RLTA) is operative for residential tenancies; Chapter 7 excluded. Period 3d confirmed. Pending human confirmation. |
| | **WV (period AI-resolved — convergent):** Both models high-confidence: notice_required=false, §55-3A-1 (summary eviction — no prior notice period). File corrected (days=null, statute=§55-3A-1, count_method=null). Pending human confirmation. |
| | **SD (CONFIRM after re-run):** Initial MODEL-SPLIT from GPT parse error (token limit). Re-run → CONSENSUS-CONFIRM (3d, §21-16-1). Stale error flags removed. |
| | **MO (L7 escalated):** AI reasoning pass — no convergence. GPT: notice_required=false (§535.020.1); Gemini: notice_required=true (§535.020). Attorney must resolve whether §535.020 demand constitutes a notice requirement or only a precondition. File's 10-day claim (§535.060) almost certainly wrong. |
| | **ND (L7 escalated):** Genuine interpretive model-split. Both cite §47-32-02 but disagree: GPT says 3-day formal notice required; Gemini says no notice, landlord may file 3 days after rent due. Attorney must resolve whether 3-day period is a notice-to-quit requirement or a ripening period. |
| | **New files:** `rules/validation/l2/l2_runner.py` (Phase 1 runner), `rules/validation/l2/l2_reasoning_pass.py` (reasoning pass for period-divergence) |
| | **Report:** `docs/L2_CONSENSUS_REPORT_2026-06-18.md` |
| | **Tiered resolution protocol established:** citation-divergence → AI-resolve; period-divergence → reasoning pass (converge=AI-resolve, diverge=L7); genuine-interpretation → L7 directly; parse-error → technical retry. AI resolution NEVER advances past ACP. |
| **2026-06-16** | **MN + NJ corrections — library reaches 51 ACP / 0 DRAFT** |
| | **MN (PART 1 — re-validation):** Citation already corrected to §504B.321 subd. 1a from prior session. L5 flag marked `resolved-confirmed` (Andrew Cohen, 2026-06-16): "14-day period confirmed per §504B.321 subd. 1a; citation corrected from §504B.285." validate.py re-run → MN notice module advances DRAFT → ACP. Library: 49 → 50 ACP. |
| | **NJ (PART 2 — substantive correction per blessed approach):** Attorney finding: NJ has no statutory notice period for nonpayment (§2A:18-61.2 carve-out). Content corrected: `notice_required: false`, `days: null`, `exceptions[federally_subsidized_housing: 14 days]`; 30-day value removed. L5 flag marked `resolved-corrected`. validate.py re-run → NJ notice module advances DRAFT → ACP. Library: 50 → 51 ACP. **Attorney-confirmed same session: Andrew Cohen, 2026-06-16** — notice_required=false, days=null (not 0), 14-day subsidy exception, 30-day removed, grounds kept distinct. NJ settled at ACP. Note: §2A:18-56 (termination) carries L1-URL-NOT-RESOLVED flag — separate future item. |
| | **Schema additions (minimal, additive):** `notice_required` (boolean) + `exceptions` array added to `pay_or_quit`; `notice_period.days` now allows null. validate.py L3 updated to suppress "cannot determine notice period" warning when `notice_required: false`. |
| | **New doc:** `docs/SCHEMA_V2_DESIGN_SPEC.md` created — documents `notice_required=false + exceptions[]` as canonical library-wide pattern for "no notice period / subsidy-conditional notice"; also documents `resolved-*` flag disposition semantics. |
| | **Result: 49 ACP → 51 ACP / 2 DRAFT → 0 DRAFT** |
| **2026-06-16** | **L5 outlier resolution — Andrew Cohen attorney review of all 7 DRAFT states** |
| | **PART 0 verification:** Confirmed L5 flags are on `pay_or_quit` field with matching values for all 7 states |
| | **PART A — 5 CONFIRMED states advanced (DC, MA, TN, VT, WA):** L5 flags marked `resolved-confirmed` with per-state attorney notes; notice module reviewer = "Andrew Cohen"; validate.py modified to suppress resolved-* flags; all 5 advanced DRAFT → ACP. WA: L3 cure_or_quit warning also marked `resolved-false-positive` (10-day period is lease-violation comply-or-vacate, not a notice inconsistency). |
| | **PART B — 2 MISMATCH states corrected (MN, NJ — both stay DRAFT):** MN: pay_or_quit statute corrected from §504B.285 to §504B.321 subd. 1a; L5 flag stays open. NJ: attorney finding recorded — NJ has NO statutory notice period for nonpayment (§2A:18-61.2); 30-day value flagged as incorrect; schema correction pending. |
| | **validate.py updated:** `layer5_cross_jurisdiction()` now accepts `existing_flags_map` and skips re-generating period flags for states where already `resolved-*`; `write_back_results` preserves all `resolved-*` dispositions. |
| | **Result: 44 ACP → 49 ACP / 7 DRAFT → 2 DRAFT** |
| **2026-06-16** | **Five-module build — all 4 under-built modules populated across all 51 v2 files** |
| | **Service (module 2):** 47 non-demo states — method_rules statutes filled from state RLTA/FED statutes (ARS §33-1313, ORC 1923.04, NRS 40.280, etc.); service_defect statutes filled. 0 [VERIFY] remaining in service module. |
| | **Overlays.state_protective (module 3):** 43 states — habitability warranty and anti-retaliation statutes filled from state RLTA (Ala. Code §35-9A-204, CRS §38-12-503, ORS 90.320, etc.). 0 [VERIFY] remaining. |
| | **Procedural_defects (module 5):** All 51 states — [VERIFY] placeholders replaced with state UD/FED procedure statutes (ARS §12-1171, 735 ILCS 5/9-201, M.G.L. c. 239 §1, etc.) and court jurisdiction citations. CA's existing AB 2347 entry preserved. |
| | **Substantive_defenses (module 4 — flag-don't-fabricate):** All 51 states — habitability and retaliation statutes filled; discrimination grounded to 42 U.S.C. §3604 + state fair housing act; breach_of_quiet_enjoyment and improper_rent_calculation marked grounding_gap; 9 just-cause states (CA, DC, MD, ME, NH, NJ, NY, OR, WA) filled with just-cause statute (Civ. Code §1946.2, NJSA 2A:18-61.1, ORS 90.427, etc.). All entries carry specialist_required. |
| | Ran validate.py → **44 ACP / 7 DRAFT — unchanged** (no regressions from build). 0 new L5 flags introduced. |
| | Generated L7 triage list → **264 entries** across 51 states, all substantive_defenses. Saved to `docs/L7_TRIAGE_LIST_2026-06-16.md`. |
| | **Total field updates: 789** across 51 files. **0 [VERIFY] entries remain in any module.** |
| **2026-06-16** | **Overlays local cleanup — cross-state contamination removed; local de-scoped to CA-only; L5 xstate check added** |
| | Coverage audit (`docs/COVERAGE_AUDIT_2026-06-16.md`) — full per-module content audit across all 51 v2 files; found 472 wrong-state local entries (cascading templating artifact) across 42 states |
| | Removed all 472 cross-state contamination entries from `overlays.local` across 47 affected files |
| | De-scoped local overlays to CA-only for Phase 1: CA's 7 clean in-state entries kept as-is; states with real-sourced correct-state entries (CO/IL/MN/NJ/NY/OR/TX/WA/WI) kept those; all remaining [VERIFY] and placeholder entries replaced with `OUT_OF_SCOPE_PHASE_1` marker |
| | Added `l5_local_xstate_check()` to `validate.py` L5 layer: flags any `overlays.local` entry whose jurisdiction belongs to a different state |
| | Re-ran `validate.py` → 51/51 L3 PASS, 51/51 L1 pass, 44 ACP, 7 DRAFT (unchanged), **0 L5-LOCAL-XSTATE flags** — clean |
| | Corrected stale State of Record items (see §6, §7, §8): demo Loom link added; paper (v0.7) and 2-pager (v13) status updated; June 15 commit pushed |
| **2026-06-15** | **L1 statutory retrieval pass — Wave 3 COMPLETE (7 previously unresolvable states; now 51/51 total)** |
| | Retrieved AR (§18-17-701 via Justia subtitle-2), SC (§27-40-710 via Justia 2024), SD (§21-16-1 via Justia chapter-16), IL (735 ILCS 5/9-207 via FindLaw), PA (68 P.S. §250.501 via FindLaw), IA (§562A.27 via Justia 2022 title-xiv), UT (§78B-6-802 via Justia 2020 part-8/section-802) |
| | IL and SD flagged L1-MACHINE-ASSIST: IL §9-207 is holdover/termination statute (pay-or-quit §9-209 unretrieval); SD §21-16-1 is FED grounds statute (nonpayment in subsection 4) |
| | URL structure discoveries: IA Justia requires `title-xiv` in path; UT Justia requires `part-8/section-802` (not `section-78b-6-802`); SC requires `/2024/` year prefix |
| | Ran `l1_update.py` → 47/47 L1=pass; ran `validate.py` → **51/51 L1=pass, 44 ACP, 7 DRAFT (L5-only)** |
| | Updated `docs/PROJECT_STATE_OF_RECORD.md` (this entry) |
| **2026-06-15** | **L1 statutory retrieval pass — COMPLETE Waves 1+2 (40 states; 44/51 total at that point)** |
| | Retrieved statutory text for 40 of 47 remaining states (Justia, FindLaw, state legislative sites) |
| | Sources used: Justia (primary), FindLaw (TN, RI, ND), nebraskalegislature.gov, michigan.gov, MO Revisor, gencourt.state.nh.us, ncleg.gov, nevada.public.law, oregon.public.law, law.lis.virginia.gov, code.dccouncil.gov, malegislature.gov |
| | Marked `retrieved=True` + URL in `provenance.statutory_sources` for all resolved citations |
| | Added machine-assist L1 flags for ME, OH, WV, MO, MS, ND (statute retrieved but not precisely the pay-or-quit authority) |
| | 7 states unresolvable (AR, IA, IL, PA, SC, SD, UT) — all sites JS-rendered or returned empty; flagged L1-URL-NOT-RESOLVED |
| | Re-ran `validate.py` → 37 states at AUTOMATED-CHECKS-PASSED; 14 remain DRAFT (7 L1-fail + 7 L5-flagged) |
| | Updated `docs/PROJECT_STATE_OF_RECORD.md` |
| **2026-06-15** | **L1 statutory retrieval pass — wave 1 (15 states; earlier this session)** |
| | Retrieved statutory text for 15 of 47 remaining states via Justia |
| | Re-ran `validate.py` → 14 new states at AUTOMATED-CHECKS-PASSED (total: 18 at that point) |
| **2026-06-15** | **v2 schema and rules library — full implementation (earlier this session)** |
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

June 15 work (v2 schema, 51 rules files, L1 retrieval, validate.py) committed and pushed 2026-06-16. June 16 work (overlays cleanup, coverage audit, L5 xstate check) ready to commit — Andy pushes via GitHub Desktop.

---

## 8. Open Issues / Known Defects

### Demo
- [x] **Demo recorded.** Loom: https://www.loom.com/share/8f1274d5a3d74a4bb4ca8a5181fde3dc
- [ ] **Scene 4 file decision:** Script says to attach `ca_eviction_rules_v0.1.json` (plugin-local demo file). The canonical v2 file is `rules/eviction/california/ca_eviction_v2.json`. Decide which to use in the demo before recording.
- [ ] **v2 files not yet reflected in widget.** `RulesComparisonWidget.html` still references v1 data. Consider updating or noting in the demo that v2 is the new library format.

### Repo — Cleanup Needed
- [ ] **`plugins/eviction-defense/LHC_Demo_Deck_v0.1.pptx`** still in repo. Old deck with LHC naming. Delete before next push.
- [ ] **README** does not mention v2 schema or 5-module structure. Update before next outreach push.
- [ ] **`ca_eviction_v1 copy.json`** — the "copy" naming is an artifact of a macOS Finder rename. Rename to `ca_eviction_v1.json` when convenient (original was accidentally deleted earlier).
- [ ] **Demo script canonical copy:** `plugins/eviction-defense/prompts/demo-script.md` may be stale vs. `demos/eviction/prompts/demo-script.md`. The `demos/` copy is canonical.

### Validation Pipeline
- [x] **L1 retrieval pass COMPLETE (2026-06-15 — all waves).** 51/51 states statutorily retrieved. 44 states at AUTOMATED-CHECKS-PASSED. Wave 3 resolved previously unresolvable states (AR, IA, IL, PA, SC, SD, UT) using corrected URL structures and FindLaw as alternative source. Machine-assist flags added for ME, OH, WV, MO, MS, ND (Waves 1/2) and IL, SD (Wave 3). L1 retrieval is **closed** — no further retrieval work needed.
- [x] **Overlays local cleanup complete (2026-06-16).** 472 cross-state contamination entries removed from 47 files. Local layer de-scoped to CA-only for Phase 1. L5-LOCAL-XSTATE check added to validate.py; all 51 states pass clean.
- [x] **Five-module build complete (2026-06-16).** Service, state_protective overlays, procedural_defects, and substantive_defenses populated across all 51 files. 789 field updates. 0 [VERIFY] remaining. L7 triage list (264 entries) saved to `docs/L7_TRIAGE_LIST_2026-06-16.md`. Validate: 44 ACP / 7 DRAFT — no regressions.
- [x] **L5 flags — all 7 DRAFT states resolved (2026-06-16).** DC, MA, TN, VT, WA: L5 flags confirmed by attorney (Andrew Cohen), marked `resolved-confirmed`, advanced to ACP. MN: citation corrected to §504B.321 subd. 1a, L5 flag marked `resolved-confirmed`, re-validated → ACP. NJ: substantive correction (no-notice-period pattern) per attorney finding, L5 flag marked `resolved-corrected`, advanced to ACP. Confirmed: Andrew Cohen, 2026-06-16.
- [x] **NJ advance confirmed (Andrew Cohen, 2026-06-16).** NJ notice module correction attorney-confirmed: `notice_required: false`, `days: null` (not 0), federally-subsidized exception (14 days), 30-day nonpayment value removed, grounds kept distinct (habitual late payment is a separate ground under §2A:18-61.2(b)). NJ is settled at ACP.
- [ ] **NJ backlog — §2A:18-56 L1 flag (future item, not urgent).** NJ file carries an L1-URL-NOT-RESOLVED flag on §2A:18-56 (termination statute). Not part of the nonpayment notice correction; flagged for future L7 attorney review or targeted retrieval pass.
- [x] **L2 (multi-model consensus) — Phase 1 complete (2026-06-18).** 8 machine-assist flag states run on notice/pay_or_quit. Runner: `rules/validation/l2/l2_runner.py`. Reasoning pass: `rules/validation/l2/l2_reasoning_pass.py`. Results: 4 states resolved (OH, MS, WV citations/period AI-corrected; SD confirmed clean); 2 states L7-escalated (MO, ND). See `docs/L2_CONSENSUS_REPORT_2026-06-18.md`.
- [x] **L2 Phase 2 complete (2026-06-17, ~$0.94 spent).** 43 states run. Report: `docs/L2_CONSENSUS_REPORT_PHASE2_2026-06-18.md`. Results:
  - **31 CONSENSUS-CONFIRM:** AK, AL, AZ, CA, CO, CT, FL, HI, ID, IN, KS, MI, MN, MT, NC, NE, NH, NJ, NM, NY, OK, OR, PA, RI, SC, TX, UT, VT, WA, WI, WY — all confirm existing file values; no human review needed.
  - **DE (CITATION-AI-RESOLVED):** §5501 → 25 Del. C. §5502(a); 5d confirmed; pending human confirmation.
  - **NV (PERIOD-AI-RESOLVED):** 5d → 7d, §40.253(1)(a); both models high-confidence; pending human confirmation.
  - **2 ERROR:** GA (GPT returned 0d — parse artifact), IA (Gemini errored). Need targeted retry.
  - **⚠️ 7 GPT-PARSE-ERROR pseudo-splits (NOT genuine L7):** AR, DC, KY, LA, MA, TN, VA — GPT returned `days=None, statute=None, rationale=PARSE_ERROR` (same token-limit artifact as SD Phase 1). Gemini answered for all 7. Currently flagged L7 but should be retried with higher `max_completion_tokens` before escalating to attorney. Retry runner needed.
  - **1 GENUINE MODEL-SPLIT (MD):** GPT says 10d notice required (§8-401(b)(2)(i)); Gemini says no notice period required (§8-401). Real interpretive disagreement → L7. Attorney must resolve.
- [x] **L2 Phase 2 retry complete (2026-06-18, ~$0.44).** `rules/validation/l2/l2_phase2_retry.py`. 9 states retried with GPT `max_completion_tokens=6000`. AR and TN confirmed CONFIRM on first retry pass (Jun 17 11:55 PM write persists in files). DC, IA, KY, LA, MA → CONFIRM via second retry. GA and VA remain flagged. VA → genuine L7. GA → straggler script pending.
- [x] **GA straggler retry complete (2026-06-18 17:12 UTC).** `l2_ga_straggler.py` run. Clean neutral query, 8000-token GPT budget. GPT: notice_required=True, days=3, §44-7-50(a). Gemini: notice_required=False, days=None, §44-7-50. Genuine split — models disagree on whether §44-7-50 imposes a formal pre-filing notice requirement. L7 flag updated in ga_eviction_v2.json. GA is genuine L7-ESCALATED (see queue entry [GA-L7-05]).
- [x] **HUMAN_REVIEW_QUEUE.md rebuilt (2026-06-18).** Queue ownership changed: runner append-only; Andy owns resolution fields. Stale Phase 2 entries removed. Queue now has only genuine review items.

**L2 COMPLETE — all 51 states. Consolidated final results (post-straggler-cleanup):**

| Outcome | Count | States |
|---------|-------|--------|
| ✅ CONSENSUS-CONFIRM | 41 | ME, IL, SD (P1) + AK,AL,AZ,CA,CO,CT,FL,HI,ID,IN,KS,MI,MN,MT,NC,NE,NH,NJ,NM,NY,OK,OR,PA,RI,SC,TX,UT,VT,WA,WI,WY (P2) + AR,DC,IA,KY,LA,MA,TN (retry — AR and TN confirmed on first retry pass) |
| ✅ CITATION-AI-RESOLVED → ATTORNEY-CONFIRMED | 3 | OH (§1923.04(A), 3d ✓), MS (§89-8-13(5)(a), 3d ✓), DE (§5502(a), 5d ✓) — confirmed Andy Cohen 2026-06-19 |
| ✅ PERIOD-AI-RESOLVED → ATTORNEY-CONFIRMED | 2 | WV (no notice, §55-3A-1 ✓), NV (7d ✓ but count_method corrected calendar→judicial days) — confirmed Andy Cohen 2026-06-19 |
| ✅ ATTORNEY-RESOLVED (substantive) | 2 | SD: §21-16-2 repealed SB 90 (2024) — NJ-pattern applied (notice_required=false, 3d ripening under §21-16-1(4)). VA: time-versioned — 5d current / 14d from 2026-07-01 (HB 15/SB 48), pending_amendment block added. |
| 🔴 L7-ESCALATED (open) | 4 | MO, ND, MD, GA — attorney review still pending |

**Notes on TN and AR (why they're CONFIRM not L7):**
- **TN:** First retry pass (11:55 PM Jun 17) wrote `L2_consensus=pass` CONSENSUS-CONFIRM (14d, §66-28-505(b)). File retains that first-pass write. TN also attorney-confirmed (Andrew Cohen, 2026-06-16). Status: CONFIRM.
- **AR:** First retry pass wrote `L2_consensus=pass` CONSENSUS-CONFIRM (3d, §18-60-304(a)(3)). Status: CONFIRM.

**L7 detail (5 genuine items):**
- **MO** — Is §535.020 demand a notice requirement (notice_required=true) or only a precondition (false)?
- **ND** — Is §47-32-02's 3-day period a formal notice-to-quit or a ripening period?
- **MD** — GPT: 10d notice required (§8-401(b)(2)(i)); Gemini: no notice period (§8-401)
- **VA** — Same statute (§55.1-1245(F)); GPT: 5d; Gemini: 14d — likely tenancy-type-dependent
- **GA** — Two clean neutral 8000-token retries (17:12 + 17:44 UTC): both models agree notice_required=True (demand required before filing). Split on days: GPT=3, Gemini=None. Narrowed question: must landlord wait 3 days after demand, or may landlord file immediately after demand is refused?
- [x] **L2 expansion — service module complete (2026-06-19/20).** 51/51 states run. 16 round-1 confirmed, 32 AI-resolved, 2 L7 (DC, NM). See `VALIDATION_METRICS_LEDGER.md` for full breakdown.
- [ ] **DC L7 attorney review (open — service module):** Persistent API failure (both GPT and Gemini, 3+ attempts). Zero model data. Service statute(s) for D.C. pay-or-quit notices require attorney verification.
- [ ] **NM L7 attorney review (open — service module):** Persistent API failure (both GPT and Gemini, 3+ attempts). Zero model data. Service statute(s) for N.M. pay-or-quit notices require attorney verification.
- ✅ **Holdings v3 runs complete (Batches 1–3 + NC-17 fresh + PR retry + Track B + Batch 4, as of 2026-06-28):**
  - Batch 3 (7e6fcf6d, 2026-06-25): 18 states, 23 units. MV=4 (CA), CI=2 (CA), RC=0, PR=0, NC=17. Method rate: 66.7%.
  - nc17_fresh_v2 (2026-06-26): 118 units, MV=6 (CA), CI=0, RC=3 (AK/CO/CT), PR=25, transient-fail=84. Method rate: 67%.
  - NC-17 fresh run (20f722c8, 2026-06-26): 17 NC states, 50 units. MV=0, CI=0, RC=2, PR=11, perm-fail=37. Method rate: 0%.
  - **PR retry (2026-06-27): PIPELINE FAILURE.** 14 states, 0 cases processed. `fresh=false` + no v1 draft candidates = permanent-failure for all. 82 transient-fail cases from nc17_fresh_v2 remain unretried. Fix: new runner that reads from nc17_fresh_v2 output JSON.
  - **Track B (2026-06-27): NY SUCCESS; KS/NV/SC GAP.**
    - NY: MV=5 (Wheeler v. D'Antonio 2025, Pena v. Lockenwitz, 339-347 E. 12th St. LLC v. Ling, MH Residential 1 v. Barrett, Graham Court v. Taylor 115 A.D.3d 50), CI=1 (Baer v. Huggins), PR=1 (Graham Court v. Kyle Taylor 24 N.Y.3d 742 wrong-doc). Method rate 83.3%. Ingested to ny_eviction_v2.json.
    - KS, NV, SC: CL fresh search returned 0 candidates. Track A candidates not indexed in CL. Next: Descrybe MCP verify OR fix load_draft_cases() to read v2 candidates[].
  - **Batch 4 NC states (fresh_nc_batch4_20260627, 2026-06-27): PARTIAL — CROSS-JURISDICTION BUG DETECTED.**
    - 11 states (AL, CT, HI, LA, MI, ND, NJ, NM, OK, VT, WV), 22 units. Harness-reported MV=3, but 2 are wrong-jurisdiction (Markese=NY County Courts, Robinson=DC Circuit — returned by NJ CL query). Valid NJ MV: 1 (Onderdonk v. Presbyterian Homes of NJ, 85 N.J. 171, 1981 NJ SC).
    - perm-fail=8 (AL, CT, HI, LA, ND, NM, OK, WV — genuinely no CL candidates).
    - MI: 8 PR — all cross-state contamination (CL returning non-MI cases for MI statute query).
    - VT: Atwood=PR (wrong doc — not a retaliation case; GREEN investigation ✅ RESOLVED 2026-07-02: replacement candidate **Gokey v. Bessette, 154 Vt. 560 (1990)** identified via CourtListener MCP — CL cluster 1539041, published, cited 17×; added to vt_eviction_v2.json candidates); Houle=CI ✅ [VT-HOLD-CI-01, cheap confirm lane] — two-model corroborated, D=INFERRED. Run 1153a763, 2026-07-02. **Gokey verification: runs c0a2df2d (2026-07-03) and c7bcdcff (2026-07-04) both FAILED on DNS to CourtListener at the recurring ~2:15–2:25 AM window; network-retry backoff added to `_run_search` 2026-07-05 (YELLOW). Run 57cf7b37 (2026-07-06) SUCCEEDED: Gokey → MV** (A=true cluster 1539041; B=OK-machine 13 citing; C=corroborated Gemini→GPT-4o; D=STATED verbatim §4465 burden-shifting quote). VT holdings: **1 MV (Gokey) + 1 CI (Houle), both VT Supreme Court — module effectively complete.** Northgate Hous. v. White → PR (generate DNS failure mid-run, retry lane); Vladyka v. Marsh → PR wrong-doc CLOSED. Note: run 57cf7b37's harness emitted 2 RC for Houle/Northgate — both were DNS artifacts (generate call failed), reclassified PR on ingestion; routing bug fixed in `protocols/retaliation_holdings_v3.py` (YELLOW). **Northgate generate retry (run e9222548, dispatched 2026-07-07): DNS failure again — both CL queries exhausted the full ~10-min backoff ladder; 0 candidates; nothing routed to attorney. Backoff ladder extended to ~66 min/query (2026-07-08, YELLOW); re-queued as `job_vt_northgate_generate_retry2_20260708` for 2026-07-09. Machine-sleep hypothesis flagged to Andy (15-hour wall-clock gap dispatch→processing).** **Retry #2 (run 9ae49b97, 2026-07-09): all 5 units → PR on Gemini-endpoint DNS failure; CL Checks A+B succeeded all night (extended ladder + PR-routing fix both live-verified ✅); machine-sleep hypothesis weakened — selective-DNS hypothesis primary; retry #3 held pending Andy's DNS diagnosis (RED-strategic). Northgate remains PR.**
    - Pipeline bug: CL statute query does not filter for court jurisdiction. Court-filter fix needed before next run.
    - nj_eviction_v2.json updated: Onderdonk added to machine_verified_cases; Markese/Robinson added to rejected_cross_jurisdiction.
  - **Cumulative MV (updated 2026-07-06):** 26 total (6 CA + 5 NY + 1 NJ + 2 AL + 3 CT + 2 HI + 2 LA + 1 ND + 1 NM + 1 WV + 1 CO + **1 VT [Gokey, run 57cf7b37]**). **Cumulative CI:** 4 (NY Baer v. Huggins, VT Houle v. Quenneville + 2 others). **Cumulative RC:** 6 (in HUMAN_REVIEW_QUEUE — unchanged; the 2 harness-RCs from run 57cf7b37 were DNS artifacts, reclassified PR, never entered the queue). **Unretried PR:** 82 (from nc17_fresh_v2) + CO/NY PR (8, from retry) + VT Northgate (generate retry).
  - RC cases → [NV-RET-HOLD-RC-01], [NY-RET-HOLD-RC-02], [AK-RET-HOLD-RC-01], [CO-RET-HOLD-RC-01], [CT-RET-HOLD-RC-01], [WV-RET-HOLD-RC-02 — Criss v. Salvation Army Residences, 319 S.E.2d 403 (WV SC 1984) — ADDED 2026-06-30].
  - CI cases (cheap confirm lane): [NY-HOLD-CI-01] Baer v. Huggins; [NM-HOLD-CI-01] Casa Blanca Mobile Home Park v. Hill (125 N.M. 465, ADDED 2026-06-30).
  - **New MV states (2026-06-30):** AL (Leeth, Tiller[Y]), CT (Holdmeyer, Correa, Presidential Village[Y]), HI (Windward Partners, Cedillos[Y]), LA (Capone[Y], Taylor[Y]), ND (Nelson[Y]), NM (Rickert[Y]), WV (Murphy), CO (W.W.G. Corp.[Y: doctrine undecided]).
  - **YELLOW flags (13 written this cycle):** See co/al/ct/hi/la/nd/nm/wv_eviction_v2.json validation_flags. Key: CO W.W.G. Corp. — court declined to decide if doctrine exists. LA Taylor — not appealed, local ordinance. ND Nelson — procedural only.
  - **KS/SC/NV confirmed CL gap:** Even with broad fallback, 0 in-state results. Next: Descrybe MCP or Track A.
  - **Cross-jurisdiction pipeline bug:** FIXED 2026-06-29 (Check E `_court_matches_state()` filter).

- ⚠️ **Task #52 — Commit pending (do this first, before running v3):**
  - Modified: `docs/PROJECT_STATE_OF_RECORD.md`, `docs/VALIDATION_METRICS_LEDGER.md`, `rules/eviction/california/ca_eviction_v2.json`, `rules/validation/l2/retaliation_holdings_v2_runner.py`
  - Deleted: `docs/VALIDATION_PHILOSOPHY_DRAFT.md` (superseded by `VALIDATION_PHILOSOPHY.md`)
  - New (untracked): `rules/validation/l2/output/retaliation_holdings_v2_1states_2026-06-22_96494b27.json` (quota-exhausted run — provenance), `rules/validation/l2/output/retaliation_holdings_v2_1states_2026-06-22_ce5c9748.json` (canonical CA run), `rules/validation/l2/output/retaliation_holdings_v2_33states_2026-06-22_a86b3598.json` (33-state quota fail — provenance), `rules/validation/l2/output/retaliation_holdings_v2_16states_2026-06-23_d5444e58.json` (batch 1 — 0/51 MV, triage source), `rules/validation/l2/retaliation_holdings_v3_runner.py` (NEW — generate-from-source runner), `docs/COWORK_DIRECTION_HOLDINGS_GENERATE_FROM_SOURCE.md` (direction doc)
  - **Commit message:** `Holdings v2/v3: CA canonical (4/6 MV), batch 1 triage (d5444e58), generate-from-source runner (v3), direction doc`
  - **How:** Open GitHub Desktop → confirm all items are staged → paste commit message → Commit to main → Push.
- ✅ **Holdings verification layer — CA complete (2026-06-22):**
  - Runner: `rules/validation/l2/retaliation_holdings_v2_runner.py` — stable. Build-check B passed.
  - Canonical run: `retaliation_holdings_v2_1states_2026-06-22_ce5c9748.json` — **4/6 machine-verified (67%)**.
  - MV: Schweiger (STATED-single-model), Barela (STATED), Drouet (STATED), Western Land (STATED).
  - NA: S.P. Growers (C=FLAG — CL returned caption-only for this cluster), Aweeka (C=FLAG — CL opinion text intermittent; MCP confirms verifiable; true rate 5/6 = 83%).
  - Ingested to `ca_eviction_v2.json` (validation_status: L2-HOLDINGS-V2-RUN-COMPLETE) and `VALIDATION_METRICS_LEDGER.md`.
  - **Next:** Commit (Task #52); re-run 33-state with fresh CL quota (tomorrow morning); build audit sampler.
- [x] **L2 expansion — procedural_defects module: COMPLETE for first full run (2026-06-25/26).**
  - Full 51-state × 4-defect run complete (204 units). CI=4, CC=31, NSR=6, MODEL-SPLIT=20, SM=120, ERROR=23. α_method=0.256.
  - 4 CONSENSUS-IMPROVE file updates applied (IA/NY/UT/WY summons). 20 MODEL-SPLIT → L7 [PROC-DEF-L7-01]–[PROC-DEF-L7-20].
  - failure_to_attach re-run complete (2026-06-26): NSR 6→28, SM −64%, ERROR −61%, α_method=0.470. CA file updated. 2 new L7s [PROC-DEF-L7-21, L7-22].
  - 9 network-timeout states (AL/IA/ME/MN/NH/NJ/NV/RI/VA) queued for retry tonight (`job_l2_attach_retry9_20260626.json`).
  - launchd overnight runs confirmed live via dispatch proof 2026-06-25 22:39 PT. Blocker closed.
- [ ] **L2 expansion — other modules (substantive_defenses, overlays):** not yet started. After procedural_defects pipeline proven at 51-state scale.
- [ ] **MO L7 attorney review (open):** Is §535.020 demand-for-rent a notice requirement (notice_required=true) or only a precondition to filing (notice_required=false)? File's 10-day §535.060 claim appears wrong; exact characterization and operative statute need attorney confirmation. L2-PERIOD-DIVERGENCE-L7-ESCALATED flag written.
- [ ] **ND L7 attorney review (open):** §47-32-02 — is the 3-day period a formal notice-to-quit requirement or a ripening period? GPT and Gemini split on same statute. L2-MODEL-SPLIT-L7 flag written.
- [ ] **L4 (golden sets):** not_implemented. 0/51 states have golden sets. Need at least CA and TX before outreach. See `test-cases/README.md`.
- [ ] **L6 (temporal freshness):** not_implemented. Needs legislative feed / CI hook.
- [ ] **L7 (attorney review):** Not started. CA is priority #1. Need one licensed CA tenant attorney to review CA's 5 modules. See `docs/REVIEWER_CHECKLIST.md`.
- [x] **MN and NJ corrections complete (2026-06-16).** MN: re-validated, ACP. NJ: no-notice-period pattern implemented, ACP. Confirmed: Andrew Cohen, 2026-06-16. Library: 51/51 ACP.
- [ ] **Re-run on L2/L4/L6 expansion:** When new layers come online, all AUTOMATED-CHECKS-PASSED modules must be re-run. Modules that fail revert to DRAFT per STATUS_LABELS v2.

### Strategic / Project Level
- [ ] **Formal paper:** In progress — v0.7 exists. Raw material in prior Cowork sessions.
- [ ] **2-pager:** In progress — v13 exists.
- [ ] **Substack / website:** Not set up.
- [ ] **Margaret/Stanford pitch:** Deck ready; 2-pager and paper not done. Send after paper.
- [ ] **Content identity decision:** Personal name vs. A2J project brand — decide before Substack/website.

---

## 9. How to Resume Work in a New Session

**Standard brief:** "Please read `docs/PROJECT_STATE_OF_RECORD.md` from the a2j-ai repo."

**If working on demo rehearsal / recording:**
> "Read the State of Record, then open `demos/eviction/prompts/demo-script.md` and help me run a rehearsal. I need to practice Scenes 3 and 4 especially."

**If working on attorney validation (L7):**
> "Read the State of Record. Let's prepare the CA v2 file for attorney review. Start with the notice module — generate a plain-language reviewer summary from ca_eviction_v2.json and the REVIEWER_CHECKLIST."

**If working on the paper or 2-pager:**
> "Read the State of Record. I want to start drafting the formal paper. The key source material is in our previous Cowork sessions — the AI layer vs. rules layer discussion, the certification maturity model, the liability architecture, and the LSC governance parallel."

---

*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*  
*State of Record last updated by Claude (Cowork) — June 21–22, 2026 (Holdings verification layer built: retaliation_holdings_v2_runner.py. Build-check B passed. Best runner result 2/6 MV; true rate 5/6 MCP-confirmed. CL rate limiting blocks clean full run — fix: 10s inter-case sleep. Previous: June 20 — LSC cross-check complete 46/51 (90%). Next: fresh-quota CA re-run → 5/6 output file; ingest; audit sampler; commit all work. Replace this file at the start of each session after significant work.)*
