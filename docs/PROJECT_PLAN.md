# A2J AI — Master Project Plan
**Working Document | Last Updated: June 3, 2026**
**Owner: Andrew Cohen**

---

## Overview

This document tracks all workstreams for the A2J AI / Legal Help Commons project. It is intended as a living working doc — upload to Google Docs and update regularly. Cross-reference with the GitHub repo (`github.com/andrewmichaelcohen-a2j/a2j-ai`) and Cowork sessions for build activity.

**Core thesis:** A shared open-source infrastructure layer ("Legal Help Commons") — built on verified legal rules, AI-assisted intake/comprehension, and a structured certification framework — can dramatically close the access-to-justice gap at scale, with the rigor and trust required for adoption by legal aid organizations, courts, and funders.

---

## Workstream 1: Publications & Content

### 1A. Formal Paper

**Purpose:** Establish intellectual credibility; primary vehicle for Margaret/Stanford pitch and broader thought-leadership. To be reviewed by friendly expert relationships before sending to Margaret or publicizing.

| Task | Status | Notes |
|------|--------|-------|
| Develop thesis and outline | 🟡 In Progress | Architecture conversations across multiple sessions provide raw material; AI layer vs. rules layer framing is well-developed |
| Draft paper | 🔴 Not Started | Raw material exists in Cowork conversations (LHC architecture, certification framework, governance model, liability architecture) |
| Internal review — friendly experts | 🔴 Not Started | Identify reviewers; send before Margaret or public distribution |
| Iterate and finalize | 🔴 Not Started | |
| Publish / distribute | 🔴 Not Started | See Workstream 4 for sequencing with outreach |

**Key source material already developed:**
- Two structural tensions + three design layers (free-rider problem, contribution-confidence problem)
- AI layer vs. rules layer boundary analysis (with workflow examples: debt, eviction, record sealing, benefits, license reinstatement)
- Four-level certification maturity model (L1 Technical → L2 Process → L3 Legal Accuracy → L4 Outcome Quality)
- Liability architecture (direct harm, outdated law, UPL exposure) + strategic leverage mechanisms
- LSC governance model as structural parallel
- Three governance model options + hard due-diligence questions

---

### 1B. 2-Pager

**Purpose:** Concise executive summary for outreach conversations; shareable without requiring someone to read the full paper.

| Task | Status | Notes |
|------|--------|-------|
| Draft 2-pager | 🔴 Not Started | Distill from paper + LHC deck |
| Iterate and finalize | 🔴 Not Started | |
| Publish / share | 🔴 Not Started | Use in Margaret pitch and other outreach |

---

### 1C. Deck

**Purpose:** Visual presentation of the LHC pitch and A2J AI vision. Supports outreach meetings and conference presentations.

| Task | Status | Notes |
|------|--------|-------|
| Core LHC pitch deck | ✅ Done | `Legal_Help_Commons_Deck.pptx` — 17 slides, iterated multiple times. Includes cascade problem, three governance models, certification framework, liability architecture, ask slide |
| Demo deck (eviction-specific) | 🟡 In Progress | Eviction demo built; demo rehearsal pending |
| Iterate and finalize | 🟡 In Progress | Deck is strong; may need tailoring for specific audiences (Stanford vs. funders vs. legal aid orgs) |
| Due diligence guide | ✅ Done | Six sections, Section H (Governance & Certification Specialists) added; scoring rubric in Appendix B |
| Expert review before distributing | 🔴 Not Started | Same reviewers as paper |

---

## Workstream 2: Cowork Builds

### 2A. Eviction Defense Demo

**Purpose:** Concrete demonstration of the LHC concept in action; primary vehicle for showing (not just telling) what the platform does.

| Task | Status | Notes |
|------|--------|-------|
| Build eviction demo (functional app) | ✅ Done | Built and committed to `a2j-ai` GitHub repo (`demos/` folder). Standalone HTML + React app. |
| Commit and push to GitHub | ✅ Done | Committed to main branch, `a2j-ai` repo |
| Make repo public | 🔴 Not Started | Repo exists; needs to be set to public on GitHub.com |
| Demo rehearsal | 🟡 In Progress | Full 10-minute flow scripted; rehearsal not yet completed |
| Record demo video | 🔴 Not Started | Record after rehearsal is clean |
| Publish demo video | 🔴 Not Started | YouTube, GitHub repo, possibly embedded on website/Substack |
| Write demo write-up / README | 🔴 Not Started | Explain what the demo shows, how to run it, what's next |

---

### 2B. 50-State JSON Rules Library (starting with Eviction)

**Purpose:** Open-source, verified, machine-readable legal rules layer that is the technical foundation of LHC. Published under clear versioning with transparent validation labeling.

**Labeling philosophy:** Rules published immediately with clear stage labels (Draft → Automated Validation → Attorney Review → Validated). This makes progress visible and invites contribution without waiting for perfection.

| Task | Status | Notes |
|------|--------|-------|
| Build initial rules library | ✅ Done | 51-state rules library built and committed to `a2j-ai` (`rules/` folder) |
| Eviction rules — all 50 states | ✅ Done | Committed; review status unclear |
| Label rules by validation stage | 🔴 Not Started | Add metadata: Draft / Automated-Validated / Attorney-Reviewed / Certified |
| Make repo public | 🔴 Not Started | Same step as 2A above |
| Define roadmap for additional A2J rule sets | 🔴 Not Started | Candidates: debt defense (SOL by state/debt type), record sealing, benefits eligibility, license reinstatement |
| Design automated validation pipeline (Layers 1–6) | 🔴 Not Started | Six layers: statutory citation check, cross-reference consistency, jurisdictional coverage, date/currency, format schema validation, test case suite |
| Initiate Layer 7 — attorney validation project | 🔴 Not Started | Recruit attorneys by state; structured review protocol; track status publicly |
| Publish validation status publicly | 🔴 Not Started | Live dashboard or GitHub table showing per-state, per-rule status |
| Publish results of each validation layer as completed | 🔴 Not Started | Transparency as a feature; builds trust with legal aid org evaluators |

---

## Workstream 3: Additional Content

**Purpose:** Build audience, thought leadership, and inbound interest over time. Lower-stakes than formal paper; can publish more freely and frequently.

**Channels:** Personal website, Substack, LinkedIn. Video content on YouTube.

| Task | Status | Notes |
|------|--------|-------|
| Set up Substack | 🔴 Not Started | Recommended as primary channel for longer-form updates |
| Set up personal website | 🔴 Not Started | Can be simple; links to GitHub, Substack, key papers |
| Write introductory post (LHC concept) | 🔴 Not Started | Adapt from 2-pager; good first Substack piece |
| Social posts about demo launch | 🔴 Not Started | LinkedIn-first; link to GitHub + demo video |
| Brief update posts (ongoing) | 🔴 Not Started | Short LinkedIn posts as milestones hit (rules published, states validated, etc.) |
| Video content | 🔴 Not Started | Demo recording is first; explainer videos later |
| Paper promotion post (on publication) | 🔴 Not Started | After expert review and finalization |

**Sequencing note:** Don't start heavy content production until there's something real to point to. The demo video + GitHub publication is the right first content anchor. Paper/2-pager launch should be sequenced with outreach (Workstream 4).

---

## Workstream 4: Strategic Outreach

**Sequencing principle:** Get real content published (or ready to publish) before reaching out. An ask is much stronger with a demo, a live GitHub repo, and a draft paper in hand. Articulate a clear, concrete ask before initiating each relationship.

### 4A. Margaret / Stanford (Renewed LHC Pitch)

| Task | Status | Notes |
|------|--------|-------|
| Initial Stanford/Courts call | ✅ Done | Zoom call with Courts + Stanford Legal Design Lab group (April 2026). Positive. |
| Finalize LHC pitch materials (deck + 2-pager) | 🟡 In Progress | Deck strong; 2-pager not yet drafted |
| Paper review by friendly experts | 🔴 Not Started | Before sending to Margaret |
| Send Margaret the renewed pitch | 🔴 Not Started | Sequence after paper review + 2-pager ready |
| Follow-up / next steps | 🔴 Not Started | |

**Ask to articulate:** Stanford partnership or endorsement; connection to the LASC/Stanford project; access to their existing rules/IP; potential research collaboration or co-publication.

---

### 4B. University of Michigan Law

| Task | Status | Notes |
|------|--------|-------|
| Identify the right contacts | 🔴 Not Started | Who at U of M law is working on A2J / legal technology? |
| Prepare outreach materials | 🔴 Not Started | 2-pager + demo link |
| Initial outreach | 🔴 Not Started | After demo published and paper in draft |
| Articulate ask | 🔴 Not Started | Research collaboration? Clinical partnership for attorney validation (Layer 7)? |

---

### 4C. Other Leaders in the Space

| Task | Status | Notes |
|------|--------|-------|
| Map the landscape | 🔴 Not Started | Who are the key players? LSC, Learned Hands, Suffolk LIT Lab, Self-Help Support, state court A2J programs, law school clinics |
| Identify where LHC has clear value prop vs. existing efforts | 🔴 Not Started | Position LHC as infrastructure/commons, not a competitor |
| Prioritize outreach targets | 🔴 Not Started | Sequence by: (a) those who can validate/endorse, (b) those who can contribute rules/attorneys, (c) funders |
| Outreach | 🔴 Not Started | After content is published and ask is clear |

**Contacts already active:**
- Tien Tzuo: exchange completed (May 2026), positive
- Luca: Zoom call (April 2026)

---

## GitHub Repo Status

**Repo:** `github.com/andrewmichaelcohen-a2j/a2j-ai`
**Local path:** `/Users/andrewcohen/Documents/GitHub/a2j-ai/`

| Folder | Contents | Status |
|--------|----------|--------|
| `rules/` | 51-state eviction rules (JSON) | ✅ Committed; not yet public |
| `demos/` | Eviction defense demo (HTML/React) | ✅ Committed; not yet public |
| `plugins/` | A2J Claude plugins | ✅ Committed; not yet public |
| `playbooks/` | Legal workflow playbooks | ✅ Committed; not yet public |
| `docs/` | PROJECT_STATUS_JUNE2026.md, architecture notes | ✅ Committed; not yet public |

**Immediate action needed:** Set repo visibility to **Public** on GitHub.com to publish all content.

---

## Key Decisions / Open Questions

1. **Paper scope:** Is this an academic paper, a practitioner white paper, or both? Who is the primary audience — legal aid executives, funders, academics, court administrators?

2. **LHC entity structure:** Has a formal entity (nonprofit, LLC) been determined? This affects how the rules library and certification framework are governed publicly.

3. **Attorney validation network:** How will Layer 7 attorneys be recruited and compensated? Law school clinics (U of M, Stanford, others) as partners? LSC-connected organizations?

4. **Certification body:** Who ultimately certifies rules as Validated? This is the hardest governance question and should be addressed before publishing the certification framework publicly.

5. **Demo tech stack:** The current demo is a standalone HTML app. Is there a plan for a live hosted version, or will the demo stay as a local/GitHub download?

6. **Content identity:** Will you publish under your personal name, under "Legal Help Commons," or both? This affects website/Substack setup.

---

## Logical Sequencing (Recommended Order)

1. **Publish the repo (public)** — flip the switch on GitHub. Zero effort, maximum credibility gain.
2. **Complete demo rehearsal + record demo video** — first concrete shareable artifact.
3. **Draft 2-pager** — can be done quickly using existing deck + conversations.
4. **Draft paper** — longer effort; use all the raw material from architecture conversations.
5. **Expert review of paper** — before sending to Margaret or publicizing.
6. **Send Margaret the full pitch** (deck + 2-pager + paper + live demo link).
7. **Launch Substack / website + first posts** — timed with or just after GitHub goes public.
8. **Initiate rules validation pipeline** (Layers 1–6 automated; recruit Layer 7 attorneys).
9. **U of M Law outreach** — by this point you have the paper, demo, and a clear ask (clinical partnership for attorney validation).
10. **Broader landscape outreach** — once LHC has real published content and some early validation.

---

## Collateral Inventory

| Item | Location | Status |
|------|----------|--------|
| LHC Pitch Deck (17 slides) | `a2j-ai/` + Cowork session (LSC governance) | ✅ Done |
| LHC Due Diligence Guide | Cowork session (LSC governance) | ✅ Done |
| LHC Architecture Doc (v0.2) | Google Drive | ✅ Done (needs minor update for new folder structure) |
| Eviction Defense Demo (HTML app) | `a2j-ai/demos/` | ✅ Done |
| Legal-Help-Commons.html (web prototype) | Documents/Legal Commons/A2J (saved by user) | ✅ Done |
| 51-State Eviction Rules (JSON) | `a2j-ai/rules/` | ✅ Done |
| PROJECT_STATUS_JUNE2026.md | `a2j-ai/docs/` | ✅ Done (session-level checklist; superseded by this doc) |
| LHC Meeting Brief (debt collection experts) | Cowork session (debt collection) | ✅ Done |
| Formal Paper | — | 🔴 Not Started |
| 2-Pager | — | 🔴 Not Started |
| Demo Video | — | 🔴 Not Started |
| Substack / Website | — | 🔴 Not Started |

---

*Last updated by Claude (Cowork) — June 3, 2026. Update this doc after each significant session or milestone.*
