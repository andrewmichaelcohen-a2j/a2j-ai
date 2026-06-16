# Civil Justice as Code — Project Plan

**Version 3.0 (full rebuild) · June 16, 2026 · Andrew M. Cohen · Pro bono / Apache 2.0**

**This is the MAP** — what we're doing, in what order, and why. Its companion `PROJECT_STATE_OF_RECORD.md` is the DASHBOARD — where things stand right now. **Read both at the start of every session; update the relevant one at the end.**

**Rebuild note:** This version fully replaces the prior `PROJECT_PLAN.md` (last genuinely updated June 3, 2026, under the retired "Legal Help Commons / LHC" framing). That file had fallen badly out of sync — it predated the v2 schema, the five-module scope, L1 retrieval, and the Civil Justice as Code reframing. Trust this file and the State of Record; discard the June-3 content. The State of Record (Cowork-maintained) has remained reliable and is the authority for live status.

---

## Document System & Session Ritual

**The repo is the single source of truth — not any chat, not any AI's memory.**

| File | Role | Sole writer |
| :---- | :---- | :---- |
| `PROJECT_PLAN.md` (this file) | The map: scope, sequencing, decisions, open items | Andy \+ Claude (planning/chat) |
| `PROJECT_STATE_OF_RECORD.md` | The dashboard: live per-module/per-state status | Cowork |

**Single-writer rule:** one writer per file, to prevent silent overwrites. **Session ritual (manual, not automatic):** start by reading both files; end by updating the relevant one and committing. AI memory is a convenience on top of the files — never a substitute.

**Lesson logged (June 16):** the prior Plan drifted because Cowork's reported "updated the Plan" edits never actually landed in the repo file. Mitigation: the Plan is maintained only in the planning surface; when updated, the full file is regenerated and pushed via GitHub Desktop, then visually confirmed in the repo. Do not rely on a reported update without confirming the file changed.

---

## Thesis

The civil-justice AI ecosystem can already *retrieve* what statutes say. What no one has built and validated is the layer encoding what the law *requires* — the if/then decision logic — in open, machine-readable, jurisdiction-specific form. **Civil Justice as Code (CJaC)** builds that layer as open-source legal plugins, starting with 50-state **residential eviction defense**, validated with the discipline of safety-critical software plus expert legal review. Output is Apache-2.0, model-agnostic, and intended for institutional stewardship — not a product, not a company.

---

## Scope: Residential Eviction Defense \= Five Modules

"Residential eviction defense" is operationalized as five rules modules per jurisdiction, ordered bright-line \-\> open-textured:

1. **Notice** — validity of the eviction notice itself: pay-or-quit, cure-or-quit, termination; periods; content defects that void it. *Bright-line. Built out and automated-checked across 51 jurisdictions.*  
2. **Service** — how the notice/summons must be served; method rules (e.g., CCP §1013 mail add-on days); service defects. *Bright-line.*  
3. **Overlays** — federal (CARES Act), state-protective (e.g., CA AB 1482 just-cause), and local (rent control, just-cause, moratoria) rules layered on base state law. *Federal/state bright-line; the local layer is poorly digitized — see de-scope below.*  
4. **Substantive defenses** — retaliation, habitability/warranty, discrimination, quiet enjoyment. *Case-law-dependent, open-textured. Automated layers check structure, not substance; specialist L7 required.*  
5. **Procedural defects** — flaws in the unlawful-detainer filing itself. *Bright-line.*

**Phase-selection principle (every phase and module):** chosen by **prevalence × harm × rule-governability**, never by ease of encoding.

**Confidence calibration:** modules carry `openness` (bright\_line / fact\_dependent / open\_textured) and `review_weight` (automated\_ok / human\_required / specialist\_required) metadata. A passed open-textured module carries **less automated assurance** than a passed bright-line module — same label, but the metadata records the difference honestly. A passed substantive-defense module is *structurally checked, not substantively blessed.*

**Local-overlay de-scope (DECIDED June 16):** local-ordinance coverage is **California-only for Phase 1\.** Local law is poorly digitized; CA is the only clean state. Other states carry an honest OUT\_OF\_SCOPE marker. Building local broadly now would create overclaiming risk. Revisit at a later phase.

---

## Status Labels & Advancement

Authoritative source: `docs/STATUS_LABELS.md` (v2). Ladder:

DRAFT \-\> AUTOMATED-CHECKS-PASSED \-\> UNDER REVIEW \-\> VALIDATED \-\> CERTIFIED

                                 ^ guardrail: no automated process crosses this line

Tracked **per module**; `file_status = min(module_status)` (a file is only as validated as its weakest module). **Option-A gate:** a module reaches AUTOMATED-CHECKS-PASSED when all *currently-implemented* layers pass (today L1/L3/L5); `not_implemented` layers don't block; coverage recorded. **No automated process advances past AUTOMATED-CHECKS-PASSED** — VALIDATED requires a named attorney; CERTIFIED requires a second independent attorney \+ advisory board (board to be constituted at stewardship). NEEDS UPDATE (L6 statute change) re-enters at DRAFT; prior human status suspended pending re-review.

**Precise external claim:** "50 states drafted; all pass the implemented automated checks; the flagship state and a stratified sample are attorney-VALIDATED, with a measured error rate." Never "we validated a 50-state library" when it's automated-only.

---

## Current Status (as of June 16, 2026\)

Live detail in the State of Record. Summary:

- **Schema v2** (5 modules) implemented; all 51 files migrated.  
- **L1 statutory retrieval: complete, 51/51 retrieved.** 44 states AUTOMATED-CHECKS-PASSED; 7 DRAFT held only by L5 notice-period outlier flags (DC, MA, MN, NJ, TN, VT, WA — retrieved, awaiting confirmation). 8 states carry L1-MACHINE-ASSIST flags (ME, OH, WV, MO, MS, ND, IL, SD) — retrieval reached an adjacent statute, not squarely the pay-or-quit authority; first verification targets.  
- **L3** 51/51 PASS. **L5** operational. **L2/L4/L6** `not_implemented`.  
- **Coverage audit (June 16):** notice complete; service \+ state-protective overlays structurally present but ungrounded for non-demo states; procedural\_defects \+ substantive\_defenses skeleton-only. **Contamination finding (fixed):** 244 local-overlay entries across 42 states named wrong-state cities — removed in the June 16 cleanup; L5 extended with a jurisdiction-consistency check so it can't recur.  
- **Demo:** recorded; Loom link [https://www.loom.com/share/8f1274d5a3d74a4bb4ca8a5181fde3dc](https://www.loom.com/share/8f1274d5a3d74a4bb4ca8a5181fde3dc) ; on Slide 7\.  
- **Collateral:** deck (v3 \+ scope slides pending), working paper v0.7, 2-pager v13 — all in draft with tracked changes; not yet finalized/published.  
- **Repo:** public; Apache 2.0; `andrewmichaelcohen-a2j/a2j-ai`.

---

## Validation Roadmap (summary)

Full detail: `docs/VALIDATION_ROADMAP.md`.

**Organizing truth:** automated layers (L1–L6) cost under \~$200 total; L2 multi-model consensus \~$20–70 in API tokens. **L7 attorney review is the entire cost and timeline.**

- **L2 subscriptions (specific):** pay-as-you-go **API** access (not consumer chat plans) — OpenAI (GPT-5.4, \~$2.50/$15 per 1M) and Google Gemini (3.1 Pro, \~$2/$12 per 1M); \~$20–50 load each; Batch API (50% off).  
- **L2 as the machine-assist fix:** L2 is the right *automated* next step for the 8 L1-machine-assist flags — independent re-check by two other model families resolves the clear cases, sharpens the rest, before any L7 spend. Cheap pre-step: targeted re-retrieval of the specific provision a flag already names (e.g., IL §9-209).  
- **L7 sourcing: PAID flagship (conservative baseline).** Pay expert CA tenant attorney(s) to get California to VALIDATED fast — \~20–50 hrs, \~$6K mid placeholder (not a quote). Donate for breadth via law-school partners thereafter. Andy (licensed attorney) self-clears bright-line outlier gates (\<2 hrs); open-textured review wants a specialist alongside him.

---

## Standards

Three reference standards, all in the messaging: **NIST AI RMF** (process), **enterprise software testing** (validate before release), **autonomous-vehicle standard** (certified performance under defined conditions, openly measured — not perfection).

**NIST AI RMF — staged, proactive (do not wait to be asked):**

- **Now:** lightweight RMF *mapping* (seven layers \-\> Govern/Map/Measure/Manage, honest per-function status). Guides the work; few hours.  
- **Downstream:** full evidenced *self-assessment*, after L2/L4/L6 \+ flagship L7, when it reflects a process that genuinely meets the standard. Legitimate because timed to when the work exists, not to hide gaps.  
- **ISO/IEC 42001:** formal certification candidate at the stewardship phase, with an institutional host.

Tense discipline: NIST \= "aligned to" (now) · academic evaluation \= substantive accuracy (Phase 1\) · ISO \= "candidate for" (Phase 3).

---

## Build Sequence (current)

1. **Overlays cleanup** *(in progress, Cowork)* — remove cross-state contamination, de-scope local to CA, add L5 jurisdiction check, fix stale State-of-Record items. *Run and confirm before the build.*  
2. **Five-module build** *(next, Cowork; direction ready)* — tier-ordered with two disciplines: **push-to-100%** on bright-line modules (service, state-protective overlays, procedural defects); **flag-don't-fabricate** on open-textured (substantive defenses). One concentrated effort; validate the whole library in one pass (no per-module multiplier). Local overlays NOT built.  
3. **L1-flag review \+ outlier confirmations** — Andy clears the 7 bright-line L5 outliers (\<2 hrs); the 8 machine-assist flags route to L2 then residual L7.  
4. **L2 / L4 / L6** — automated layers; L2 prioritized (attacks machine-assist flags); L4 golden sets (CA-\>TX-\>NY); L6 freshness.  
5. **Flagship L7** — California to VALIDATED (paid), with published error rate.  
6. **Docs pass \+ outreach** — see below.

**Gating:** scope/scaffolding (1–2) completes before the flag review and L2/L4/L6, so those run against a stable library.

---

## Working with Cowork: completion discipline

Observed failure mode: Cowork declares completion prematurely (L1 at \~60%, again \~90%) on completable tasks. Directions counter this, **scoped by module risk:**

- **Bright-line modules:** completion \= 100% of states, no exceptions; retry failed retrievals with alternate sources / corrected URLs; "I can't get this one" \= try harder before flagging.  
- **Open-textured modules:** the opposite — populate only what can be grounded; **flag-don't-fabricate**; a confident uncited answer is a failure (this discipline's absence caused the contamination). Record gaps via `review_weight: specialist_required` \+ `grounding_gap`.

Also: Cowork's reported doc updates must be **confirmed in the file**, not trusted on report (see the Plan-drift lesson above).

---

## Collateral

| Item | Version | Status |
| :---- | :---- | :---- |
| Pitch deck (Civil Justice as Code) | v3 \+ scope slides pending | Draft; demo embedded |
| Working paper | v0.7 | Draft, tracked changes |
| 2-pager | v13 | Draft, tracked changes |
| Demo (Loom) | v5 script | Recorded & linked |

**Lifecycle:** draft in Mac/Google Docs \+ A2J project chat \-\> finalize (accept changes) \-\> publish clean paper/2-pager to repo (deck optional, often kept as controlled link). Not in Cowork; not in public repo while in tracked-change draft.

**OPEN ITEM — deferred docs pass (do not lose):** the local de-scope and the contamination finding are intentionally **not** in the paper/deck/2-pager now (de-scope is below the docs' architectural altitude; contamination is a *conversational* trust asset, not a written claim). **Trigger:** after the five-module build lands, the docs need a pass anyway to reflect populated modules — fold any scope-language tightening into that single pass. Recorded here so it survives in the repo, not in memory.

**Contamination as narrative asset:** "our audit caught confident-wrong data, we removed it, and we hardened the validation layer so it can't recur" — use conversationally if a partner probes rigor. Evidence the discipline works.

---

## Outreach

**Sequence (holds):** **law schools first \-\> institutions/funders \-\> Anthropic.** Each conversation uses the same kit: deck \+ live demo link \+ validation report. Gate on demo recorded (done) \+ validation report published \+ at least the flagship state genuinely VALIDATED, so every conversation is show, not tell.

**Targets:**

- **Stanford** — Legal Design Lab (human-centered A2J / human-review layer), RegLab (AI with agencies/courts), liftlab (industry prototyping), CodeX (computational-law tradition). Co-author/independent-evaluate the validation methodology.  
- **University of Michigan Law** — A2J / legal-tech faculty; potential clinical partnership for L7 attorney validation.  
- **Anthropic** — legal team \+ product leaders; the rules layer as the complement that makes the A2J axis of Claude for Legal deliver.  
- **Broader landscape** (later) — LSC, Suffolk LIT Lab, court A2J programs, law-school clinics; positioned as commons/infrastructure, not competitor.

*(Individual contacts intentionally omitted from this plan; tracked separately.)*

---

## Phases

- **Phase 1 — Eviction defense, proven (now \-\> \~3 mo):** five modules populated; 50-state automated checks; CA \+ a stratified sample attorney-VALIDATED with a published error rate; collateral finalized; first institutional conversations.  
- **Phase 2 — Conditional expansion:** a second domain (likely consumer-debt defense or benefits appeals), chosen by prevalence × harm × rule-governability; broaden attorney validation via partners.  
- **Phase 3 — Stewardship:** institutional home; recognition (LSC, state bars); ISO/IEC 42001; coverage extension through the partner network.

---

## Open Decisions

- **L7 flagship sourcing:** paid baseline set; confirm budget appetite / specific reviewer.  
- **Content identity:** personal name vs. project brand — gates Substack/website.  
- **Long-term institutional home:** Stanford / LSC / foundation; and when to open the handoff conversation.  
- **Funding posture:** Andy pro bono confirmed; decide whether L7 is donated (clinics) or underwritten via an institutional host.  
- **Loose-file cleanup:** a stale `PROJECT_PLAN.md` copy exists in `Documents/` (outside the repo) — delete/rename so only the repo copy remains.

---

## Out of Scope (explicit)

- Not a business or product. Not competing with existing A2J tools (complementary).  
- No automated advancement past AUTOMATED-CHECKS-PASSED.  
- No broad local-overlay build (CA-only, Phase 1).  
- No L2/L6 infrastructure build until scope/scaffolding is stable.

---

*Civil Justice as Code · Project Plan v3.0 · June 16, 2026 · Maintained by Andy \+ Claude (planning surface). Companion: PROJECT\_STATE\_OF\_RECORD.md (Cowork). Replaces the retired June-3 LHC-era plan.*  
