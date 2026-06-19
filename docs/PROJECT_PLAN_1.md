# Civil Justice as Code — Project Plan

**Version 3.1 · June 18, 2026 · Andrew M. Cohen · Pro bono / Apache 2.0**
*(v3.1 adds the Validation Philosophy section incl. the tiered resolution protocol; records L2 Phase 1 results. v3.0 was the full rebuild, June 16.)*

> **This is the MAP** — what we're doing, in what order, and why. Its companion `PROJECT_STATE_OF_RECORD.md` is the DASHBOARD — where things stand right now.
> **Read both at the start of every session; update the relevant one at the end.**
>
> **Rebuild note:** This version fully replaces the prior `PROJECT_PLAN.md` (last genuinely updated June 3, 2026, under the retired "Legal Help Commons / LHC" framing). That file had fallen badly out of sync — it predated the v2 schema, the five-module scope, L1 retrieval, and the Civil Justice as Code reframing. Trust this file and the State of Record; discard the June-3 content. The State of Record (Cowork-maintained) has remained reliable and is the authority for live status.

---

## Document System & Session Ritual

**The repo is the single source of truth — not any chat, not any AI's memory.**

| File | Role | Sole writer |
|------|------|-------------|
| `PROJECT_PLAN.md` (this file) | The map: scope, sequencing, decisions, open items | Andy + Claude (planning/chat) |
| `PROJECT_STATE_OF_RECORD.md` | The dashboard: live per-module/per-state status | Cowork |

**Single-writer rule:** one writer per file, to prevent silent overwrites. **Session ritual (manual, not automatic):** start by reading both files; end by updating the relevant one and committing. AI memory is a convenience on top of the files — never a substitute.

> **Lesson logged (June 16):** the prior Plan drifted because Cowork's reported "updated the Plan" edits never actually landed in the repo file. Mitigation: the Plan is maintained only in the planning surface; when updated, the full file is regenerated and pushed via GitHub Desktop, then visually confirmed in the repo. Do not rely on a reported update without confirming the file changed.

---

## Thesis

The civil-justice AI ecosystem can already *retrieve* what statutes say. What no one has built and validated is the layer encoding what the law *requires* — the if/then decision logic — in open, machine-readable, jurisdiction-specific form. **Civil Justice as Code (CJaC)** builds that layer as open-source legal plugins, starting with 50-state **residential eviction defense**, validated with the discipline of safety-critical software plus expert legal review. Output is Apache-2.0, model-agnostic, and intended for institutional stewardship — not a product, not a company.

---

## Validation Philosophy

Full articulation: `docs/VALIDATION_PHILOSOPHY.md` (for the paper/deck). In brief:

**The problem this solves.** Full human review of fifty states × multiple modules × open-textured doctrine is the most accurate path *and* the reason a verified A2J rules layer has never been built at scale. The contribution is a third path: **automation for coverage and triage; humans, surgically, for judgment and anchoring.**

- **Brute-force automation** does the mechanical and complete work (retrieve every statute, check consistency, detect anomalies, monitor change) — and assesses the *entire published corpus* (best-practices guides, legal-aid materials, court self-help content) in structured form, surfacing where sources agree, diverge, or have gone stale. AI cannot *determine* the law from this corpus, but it can hold the whole field in view at once, which no prior effort could.
- **Smart automation** does triage (multi-model consensus, golden-set testing): it locates where something is probably wrong. Divergence is the signal.
- **Surgical human expertise** resolves what remains — the open-textured calls and the genuine interpretive questions automation flags.

**Each layer narrows the field for the next**, concentrating scarce expertise on the small fraction where judgment is decisive.

### The resolution protocol (tiered — narrows mandatory human review to true legal judgment)

When the cross-checks surface a discrepancy, route it to the lightest sufficient resolution:
1. **Mechanical / citation discrepancies → AI resolves.** Models agree on the law but differ on which section to cite → AI verifies the operative section and corrects the citation. No human review needed.
2. **Substantive-but-resolvable → AI reasons first, human only if unresolved.** Models disagree on substance → an AI reasoning pass gives them the competing authorities and asks them to converge with citations. Converge with sound reasoning → AI-resolved. Fail to converge, or a genuine interpretive question emerges → escalate to human.
3. **Genuine interpretive questions → human, always.** Disagreements turning on how courts read a statute, legislative intent, or doctrinal distinctions (e.g., notice requirement vs. ripening period) — an attorney decides.

**Guardrail: AI resolution changes content and raises confidence; it never crosses the validation line.** AI-resolved items stay at AUTOMATED-CHECKS-PASSED, marked `pending-human-confirmation`, never VALIDATED, with reasoning and sources recorded for human audit. Consensus among models that share secondary sources is corroboration, not proof.

**Proof point (L2 Phase 1, 2026-06-18):** across the 8 machine-assist flag states, the protocol narrowed 8 automated discrepancies to **2 genuine human-judgment items** (MO, ND) — 3 confirmed, 2 citation-fixes AI-resolved, 1 substantive disagreement (WV) AI-resolved by reasoning. The labeling discipline held throughout.

---

## Scope: Residential Eviction Defense = Five Modules

"Residential eviction defense" is operationalized as five rules modules per jurisdiction, ordered bright-line -> open-textured:

1. **Notice** — validity of the eviction notice itself: pay-or-quit, cure-or-quit, termination; periods; content defects that void it. *Bright-line. Built out and automated-checked across 51 jurisdictions.*
2. **Service** — how the notice/summons must be served; method rules (e.g., CCP §1013 mail add-on days); service defects. *Bright-line.*
3. **Overlays** — federal (CARES Act), state-protective (e.g., CA AB 1482 just-cause), and local (rent control, just-cause, moratoria) rules layered on base state law. *Federal/state bright-line; the local layer is poorly digitized — see de-scope below.*
4. **Substantive defenses** — retaliation, habitability/warranty, discrimination, quiet enjoyment. *Case-law-dependent, open-textured. Automated layers check structure, not substance; specialist L7 required.*
5. **Procedural defects** — flaws in the unlawful-detainer filing itself. *Bright-line.*

**Phase-selection principle (every phase and module):** chosen by **prevalence × harm × rule-governability**, never by ease of encoding.

**Confidence calibration:** modules carry `openness` (bright_line / fact_dependent / open_textured) and `review_weight` (automated_ok / human_required / specialist_required) metadata. A passed open-textured module carries **less automated assurance** than a passed bright-line module — same label, but the metadata records the difference honestly. A passed substantive-defense module is *structurally checked, not substantively blessed.*

**Local-overlay de-scope (DECIDED June 16):** local-ordinance coverage is **California-only for Phase 1.** Local law is poorly digitized; CA is the only clean state. Other states carry an honest OUT_OF_SCOPE marker. Building local broadly now would create overclaiming risk. Revisit at a later phase.

---

## Status Labels & Advancement

Authoritative source: `docs/STATUS_LABELS.md` (v2). Ladder:

```
DRAFT -> AUTOMATED-CHECKS-PASSED -> UNDER REVIEW -> VALIDATED -> CERTIFIED
                                 ^ guardrail: no automated process crosses this line
```

Tracked **per module**; `file_status = min(module_status)` (a file is only as validated as its weakest module). **Option-A gate:** a module reaches AUTOMATED-CHECKS-PASSED when all *currently-implemented* layers pass (today L1/L3/L5); `not_implemented` layers don't block; coverage recorded. **No automated process advances past AUTOMATED-CHECKS-PASSED** — VALIDATED requires a named attorney; CERTIFIED requires a second independent attorney + advisory board (board to be constituted at stewardship). NEEDS UPDATE (L6 statute change) re-enters at DRAFT; prior human status suspended pending re-review.

**Precise external claim:** "50 states drafted; all pass the implemented automated checks; the flagship state and a stratified sample are attorney-VALIDATED, with a measured error rate." Never "we validated a 50-state library" when it's automated-only.

---

## Current Status (as of June 18, 2026)

Live detail in the State of Record. Summary:

- **Schema v2** (5 modules) implemented; all 51 files migrated. Five-module build complete (789 field updates; 0 placeholders).
- **Library: 51 ACP / 0 DRAFT.** L1 retrieval complete (51/51). L3 51/51 PASS. L5 operational (incl. local-jurisdiction cross-state check).
- **L5 outlier resolution complete (June 16):** attorney review (Andrew Cohen) of all 7 DRAFT states — 5 confirmed → ACP (DC, MA, TN, VT, WA); MN citation corrected (§504B.321 subd. 1a); NJ substantively corrected (no-notice-period pattern: `days=null`, `notice_required=false`, federally-subsidized exception). NJ correction attorney-confirmed from file content.
- **L2 Phase 1 complete (June 18):** 8 machine-assist flag states run (notice/pay_or_quit), models gpt-5.5 + gemini-2.5-pro. Results via the tiered resolution protocol: ME/IL/SD confirmed; OH/MS citations AI-resolved; WV period AI-resolved (no notice required); **MO + ND escalated to L7** (genuine interpretive questions). AI-resolved items marked `pending-human-confirmation`, held at ACP. `l2_runner.py` + `l2_reasoning_pass.py` in repo. **L2 Phase 2 (all 51 states) not yet run.**
- **Coverage audit (June 16):** notice complete; service + state-protective overlays grounded in the build; substantive_defenses open-textured (264 L7-triage entries); local overlays de-scoped to CA Phase 1.
- **Demo:** recorded; Loom link https://www.loom.com/share/8f1274d5a3d74a4bb4ca8a5181fde3dc ; on Slide 7.
- **Collateral:** deck (v3 + scope slides pending), working paper v0.7, 2-pager v13 — draft with tracked changes; not finalized/published. Deferred docs pass pending (incl. resolution protocol as a pitch asset).
- **Repo:** public; Apache 2.0; `andrewmichaelcohen-a2j/a2j-ai`.

**Open human-judgment queue (from L2):** MO and ND L7-escalated (statutory-interpretation questions Andy can likely resolve). AI-resolved items (OH, MS, WV, + Phase-2 output) await human spot-check confirmation.

---

## Validation Roadmap (summary)

Full detail: `docs/VALIDATION_ROADMAP.md`.

**Organizing truth:** automated layers (L1–L6) cost under ~$200 total; L2 multi-model consensus ~$20–70 in API tokens. **L7 attorney review is the entire cost and timeline.**

- **L2 subscriptions (specific):** pay-as-you-go **API** access (not consumer chat plans) — OpenAI (GPT-5.4, ~$2.50/$15 per 1M) and Google Gemini (3.1 Pro, ~$2/$12 per 1M); ~$20–50 load each; Batch API (50% off).
- **L2 as the machine-assist fix:** L2 is the right *automated* next step for the 8 L1-machine-assist flags — independent re-check by two other model families resolves the clear cases, sharpens the rest, before any L7 spend. Cheap pre-step: targeted re-retrieval of the specific provision a flag already names (e.g., IL §9-209).
- **L7 sourcing: PAID flagship (conservative baseline).** Pay expert CA tenant attorney(s) to get California to VALIDATED fast — ~20–50 hrs, ~$6K mid placeholder (not a quote). Donate for breadth via law-school partners thereafter. Andy (licensed attorney) self-clears bright-line outlier gates (<2 hrs); open-textured review wants a specialist alongside him.

**L2 scope — it is a grid of (module × claim-type), not a single pass.** "L2 done" must not be read as "L2 complete." What has run: the **notice module's `pay_or_quit` (nonpayment) period**, across all 51 states (Phase 1 = 8 machine-assist states; Phase 2 = the other 43). That is roughly one cell of the grid. Remaining L2 work, organized by *rule type* rather than module:
- **One consolidated bright-line L2 campaign** (run together, all states): the remaining notice types (`cure_or_quit`, `termination`), **service**, **procedural defects**, and the bright-line **overlay** claims. These are deterministic statutory facts where multi-model consensus is strong evidence — batch them as one campaign rather than module-by-module.
- **A separate, differently-designed pass for open-textured modules** (substantive defenses, much of overlays): consensus is weak evidence here, so these follow the open-textured operating principle (AI drafts maximally; validate via sampling/adversarial/consistency testing; narrow before human review) rather than a bright-line consensus run.

**Higher-order model-assisted validation (beyond statutes):** the same multi-model infrastructure also runs **completeness checks** (what's missing from a file), **schema design review**, **structured corpus assessment**, **cross-state consistency review**, and a periodic **methodology red-team** (harvest objections before outreach). All improve-and-flag only; none advance past ACP. See `VALIDATION_PHILOSOPHY.md`.

---

## Standards

Three reference standards, all in the messaging: **NIST AI RMF** (process), **enterprise software testing** (validate before release), **autonomous-vehicle standard** (certified performance under defined conditions, openly measured — not perfection).

**NIST AI RMF — staged, proactive (do not wait to be asked):**
- **Now:** lightweight RMF *mapping* (seven layers -> Govern/Map/Measure/Manage, honest per-function status). Guides the work; few hours.
- **Downstream:** full evidenced *self-assessment*, after L2/L4/L6 + flagship L7, when it reflects a process that genuinely meets the standard. Legitimate because timed to when the work exists, not to hide gaps.
- **ISO/IEC 42001:** formal certification candidate at the stewardship phase, with an institutional host.

Tense discipline: NIST = "aligned to" (now) · academic evaluation = substantive accuracy (Phase 1) · ISO = "candidate for" (Phase 3).

---

## Build Sequence (current)

1. **Overlays cleanup** *(in progress, Cowork)* — remove cross-state contamination, de-scope local to CA, add L5 jurisdiction check, fix stale State-of-Record items. *Run and confirm before the build.*
2. **Five-module build** *(next, Cowork; direction ready)* — tier-ordered with two disciplines: **push-to-100%** on bright-line modules (service, state-protective overlays, procedural defects); **flag-don't-fabricate** on open-textured (substantive defenses). One concentrated effort; validate the whole library in one pass (no per-module multiplier). Local overlays NOT built.
3. **L1-flag review + outlier confirmations** — Andy clears the 7 bright-line L5 outliers (<2 hrs); the 8 machine-assist flags route to L2 then residual L7.
4. **L2 / L4 / L6** — automated layers; L2 prioritized (attacks machine-assist flags); L4 golden sets (CA->TX->NY); L6 freshness.
5. **Flagship L7** — California to VALIDATED (paid), with published error rate.
6. **Docs pass + outreach** — see below.

**Gating:** scope/scaffolding (1–2) completes before the flag review and L2/L4/L6, so those run against a stable library.

---

## Working with Cowork: completion discipline

Observed failure mode: Cowork declares completion prematurely (L1 at ~60%, again ~90%) on completable tasks. Directions counter this, **scoped by module risk:**
- **Bright-line modules:** completion = 100% of states, no exceptions; retry failed retrievals with alternate sources / corrected URLs; "I can't get this one" = try harder before flagging.
- **Open-textured modules:** the opposite — populate only what can be grounded; **flag-don't-fabricate**; a confident uncited answer is a failure (this discipline's absence caused the contamination). Record gaps via `review_weight: specialist_required` + `grounding_gap`.

Also: Cowork's reported doc updates must be **confirmed in the file**, not trusted on report (see the Plan-drift lesson above).

---

## Collateral

| Item | Version | Status |
|------|---------|--------|
| Pitch deck (Civil Justice as Code) | v3 + scope slides pending | Draft; demo embedded |
| Working paper | v0.7 | Draft, tracked changes |
| 2-pager | v13 | Draft, tracked changes |
| Demo (Loom) | v5 script | Recorded & linked |

**Lifecycle:** draft in Mac/Google Docs + A2J project chat -> finalize (accept changes) -> publish clean paper/2-pager to repo (deck optional, often kept as controlled link). Not in Cowork; not in public repo while in tracked-change draft.

**OPEN ITEM — deferred docs pass (do not lose):** the local de-scope and the contamination finding are intentionally **not** in the paper/deck/2-pager now (de-scope is below the docs' architectural altitude; contamination is a *conversational* trust asset, not a written claim). **Trigger:** after the five-module build lands, the docs need a pass anyway to reflect populated modules — fold any scope-language tightening into that single pass. Recorded here so it survives in the repo, not in memory.

**Contamination as narrative asset:** "our audit caught confident-wrong data, we removed it, and we hardened the validation layer so it can't recur" — use conversationally if a partner probes rigor. Evidence the discipline works.

---

## Outreach

**Sequence (holds):** **law schools first -> institutions/funders -> Anthropic.** Each conversation uses the same kit: deck + live demo link + validation report. Gate on demo recorded (done) + validation report published + at least the flagship state genuinely VALIDATED, so every conversation is show, not tell.

**Targets:**
- **Stanford** — Legal Design Lab (human-centered A2J / human-review layer), RegLab (AI with agencies/courts), liftlab (industry prototyping), CodeX (computational-law tradition). Co-author/independent-evaluate the validation methodology.
- **University of Michigan Law** — A2J / legal-tech faculty; potential clinical partnership for L7 attorney validation.
- **Anthropic** — legal team + product leaders; the rules layer as the complement that makes the A2J axis of Claude for Legal deliver.
- **Broader landscape** (later) — LSC, Suffolk LIT Lab, court A2J programs, law-school clinics; positioned as commons/infrastructure, not competitor.

*(Individual contacts intentionally omitted from this plan; tracked separately.)*

---

## Phases

- **Phase 1 — Eviction defense, proven (now -> ~3 mo):** five modules populated; 50-state automated checks; CA + a stratified sample attorney-VALIDATED with a published error rate; collateral finalized; first institutional conversations.
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

## Field Alignment & Publication Priority (June 18, 2026)

**Standards alignment (Stanford Legal Design Lab / JusticeBench).** Per Hagan's June 18 "Data Standards and Datasets" article, CJaC sits in the **legal-workflow / decision-logic layer** the field names as scarcest and least-captured. Align CJaC to the field's connective-tissue standards so it's the interoperable, executed reference implementation of that layer (full spec: `JUSTICEBENCH_ALIGNMENT_SPEC.md`): adopt **LIST** issue codes, **FIPS** jurisdiction codes, **Legal Help Task Taxonomy** IDs, ISO language codes, and the **currency-status enum** (current/aging/stale/unknown); pull **JusticeBench synthetic query datasets** (esp. High Risk Legal Help Queries) to seed L4 golden sets; adopt the **rubric-as-eval** principle (reviewer checklist = automated eval, one artifact per module). Guardrail: alignment changes labeling/testing interoperability, not CJaC's validation discipline.

**Publication priority — establish CJaC as the executed, citable reference implementation.** The field's framing ("rules-heavy, lightest-sufficient-tool, write-the-logic-down-and-own-it") is converging with CJaC's thesis; priority goes to whoever publishes the *built, working artifact*, not the framing. Get the executed artifact and methodology public, honestly labeled, soon:
- **README rewrite (highest leverage)** — turn the public repo from a file pile into a clear statement of what CJaC is, its scope, status labels, and validation methodology. The thing a link resolves to.
- **Publish `VALIDATION_PHILOSOPHY.md`** — stakes the methodology claim publicly.
- **Finalize + publish working paper / 2-pager** (accept tracked changes first).
- **Do NOT** escalate the rules files' claim ahead of validation — they're public at ACP with honest labels; that's correct. Establish via *visible rigorous execution*, not premature "validated" claims.

---

## Out of Scope (explicit)

- Not a business or product. Not competing with existing A2J tools (complementary).
- No automated advancement past AUTOMATED-CHECKS-PASSED.
- No broad local-overlay build (CA-only, Phase 1).
- No L2/L6 infrastructure build until scope/scaffolding is stable.

---

*Civil Justice as Code · Project Plan v3.1 · June 18, 2026 · Maintained by Andy + Claude (planning surface). Companion: PROJECT_STATE_OF_RECORD.md (Cowork). Replaces the retired June-3 LHC-era plan.*
