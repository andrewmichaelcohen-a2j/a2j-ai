# Standards & Content Landscape Assessment — for CJaC

**Date:** June 18, 2026 · **Prepared by:** Claude (research; live-verified June 18) · **For:** Andy
**Question:** What recognized standards, datasets, and methodological efforts in the A2J / legal-data field should CJaC leverage, validate against, or align with — across both eviction-specific and domain-general axes — and which findings warrant changes to schema/content/approach (gating L2) vs. additive interoperability (parallel)?

> **Triage discipline:** Each finding tagged **[T1]** = may change validated content or schema structure → could gate the relevant L2 run; or **[T2]** = additive interoperability/testing → proceeds in parallel, does not gate L2. The point is to capture value without scope-creeping the validation.

---

## Headline findings

1. **CJaC's specific contribution is confirmed as genuinely under-occupied.** Across the entire landscape, the orgs cluster into three layers — none of which is doing CJaC's exact thing (validated, current, machine-readable *decision logic* with an explicit validation methodology):
   - **Eviction *data*** (filing counts, rates, trends): Princeton Eviction Lab, LSC Civil Court Data Initiative, Georgetown CJDC. *Not law-content.*
   - **Eviction *law compilation*** (the closest): LSC Eviction Laws Database (Temple CPHLR). Structured, statute-linked, all-states — **but frozen as of Jan 1, 2021.**
   - **Rules-as-code *methodology/tooling*** (the closest on approach): Suffolk LIT Lab, Docassemble/AssemblyLine, OpenFisca, Blawx, DMN. Tools and encodings, not a validated 50-state eviction library.
   CJaC sits at the intersection none of them occupies: *current + validated + machine-readable decision logic + methodology.* This strengthens the durability/positioning thesis.

2. **The single most strategically important find: the LSC Eviction Laws Database is a partial precursor to CJaC — and its staleness is CJaC's clearest differentiator.** It covers notice requirements, filing timelines, causes, post-judgment, statute-linked, all 50 states + DC + territories. But it is **fixed at Jan 1, 2021.** Today's review alone found SD (2024 repeal), GA (2024 HB 404), VA (2026 amendment) — all *after* its cutoff. **This is concrete, citable proof of why a continuously-validated, freshness-tracked library is needed.** The LSC DB is simultaneously (a) a corroboration source for CJaC's pre-2021 baseline, (b) a structural model worth studying, and (c) the strongest argument for CJaC's currency value.

---

## Axis A — Eviction-specific sources

### A1. LSC Eviction Laws Database (Temple CPHLR) — **HIGH VALUE** [T1 + T2]
- **What:** Structured dataset of state/territory + 30 local jurisdictions' eviction laws — causes, notice requirements, filing timelines, post-judgment, each linked to the statute. Excel-downloadable. Codebook + research protocol published.
- **Authority:** Very high (LSC = federal A2J funder; Temple CPHLR = established legal-mapping group; congressionally-directed study).
- **Limitation:** Content as of **Jan 1, 2021** — now materially stale on recent changes.
- **[T1] Leverage as corroboration/gap-check:** Cross-check CJaC's notice/service/procedural content against the LSC dataset for the pre-2021 baseline — a second authoritative source to validate against (and where CJaC diverges, the divergence is often *because CJaC is more current* — which is the story). **This touches validated content, so do it as a validation input, ideally before/with the relevant module L2.**
- **[T2] Study its schema:** Its data structure (how it decomposes the eviction process into elements) is worth comparing to CJaC's five-module schema for completeness — may surface elements CJaC omits (e.g., post-judgment, bond-to-appeal, fee structures). Additive.
- **Action:** Pull the Excel dataset + codebook. Use as a validation corroboration source and schema-completeness check.

### A2. Princeton Eviction Lab — **AWARENESS / partner, not content** [T2]
- **What:** Eviction *filing data* (counts, rates, trends, 2000–present; modeled estimates v2.0). Not law-content.
- **Authority:** Very high (the authoritative eviction-data source).
- **Relevance:** Not incorporable into CJaC's rules content (different layer). Valuable as: context/impact framing for messaging; a potential validation *outcome* signal later (do CJaC-flagged high-risk jurisdictions correlate with high filing rates?); a respected name in the field to be aware of and aligned with. **Not a schema or content input.**

### A3. LSC Civil Court Data Initiative / Eviction Tracker — **AWARENESS** [T2]
- Court filing-count data, 1,250 counties. Same layer as Eviction Lab (data, not law). Awareness only.

---

## Axis B — Domain-general standards & methodology

### B1. LIST (Legal Issue Taxonomy) — **ALREADY ADOPTING** [T2] ✓
- Confirmed in prior work; CJaC already aligning (HO-02-04 eviction subcodes verified). This is the domain-general issue taxonomy — correct to adopt, and it spans all civil-justice domains (supports the repeatability/multi-domain roadmap, not just eviction). No new action beyond the in-flight tagging.

### B2. JusticeBench / Legal Help Task Taxonomy — **ALREADY ADOPTING** [T2] ✓
- Confirmed; task IDs verified. Domain-general. In-flight.

### B3. NODS (National Open Court Data Standards, NCSC/COSCA) — **AWARENESS, possible future alignment** [T2]
- **What:** Logical + technical standards for how *courts* collect/share case-level data; now mapped to NIEMOpen. Voluntary; adopted by many state courts. 7 case categories.
- **Authority:** Very high (NCSC/COSCA — the court-standards bodies).
- **Relevance to CJaC:** NODS standardizes *court case data* (the docket/filing layer), not *substantive law rules* — so it's not a direct schema input for CJaC's decision logic. BUT: (a) it's the dominant court-data standard, so if CJaC ever outputs case-screening or connects to court data, NODS-awareness matters; (b) NIEMOpen is the federal justice-data interchange standard — worth knowing as the technical lingua franca. **Awareness now; possible alignment point if CJaC extends toward court-data interaction. Not a current schema change.**

### B4. Rules-as-code methodology cousins (Suffolk LIT Lab, OpenFisca, Blawx, DMN, Docassemble) — **METHODOLOGICAL VALUE** [T2, one latent T1]
- **What:** The open-source legal-rules-encoding community. Suffolk LIT Lab (Docassemble/AssemblyLine, CourtFormsOnline) = closest *delivery* cousin. OpenFisca (gov-grade rules engine, UNDP/OECD-endorsed), Blawx (visual rules-as-code), DMN (Decision Model & Notation — a *standard* for expressing decision logic) = encoding approaches.
- **[T2] Key methodological principle worth adopting explicitly:** the **"separate the rules from the interview/presentation logic"** discipline (Suffolk) — keep the decision logic platform-independent and reusable, not entangled with any one app's UI. CJaC's schema already does this (rules as data, not app code), but it's worth *naming* this principle in the philosophy as deliberate alignment with rules-as-code best practice. Strengthens credibility with the computational-law audience.
- **[latent T1] DMN as a possible expression target:** DMN is an OMG *standard* for decision logic. Worth *evaluating* (not adopting now) whether CJaC's decision logic should be expressible in/exportable to DMN for interoperability with business-rules engines. This could eventually touch schema structure — flag as a research question, NOT a current change. Probably premature; note and move on.
- **Action:** Name the rules/presentation-separation principle in the philosophy [T2]. Park DMN as a future interoperability question.

### B5. Pew Charitable Trusts (civil justice modernization) — **AWARENESS** [T2]
- Funder/research on civil legal system modernization, eviction diversion. Context and potential funder-landscape awareness. Not a content/schema input.

---

## Triage summary

### [T1] — touches validated content/schema; sequence with relevant L2
1. **LSC Eviction Laws Database as a corroboration + completeness source.** Cross-check CJaC content against it (pre-2021 baseline); study its process-decomposition for schema-completeness gaps (post-judgment, bond, fees). *This is the one finding that genuinely informs validation and possibly schema — handle it as a validation input.*
   - **But note:** it does NOT block service L2. Service methods/statutes are core content the LSC DB would *corroborate*, not change. So service L2 still proceeds; the LSC cross-check is an *additional corroboration source*, valuable but not a gate.
2. **(Latent) DMN expressibility** — future research question, not a current change.

### [T2] — additive/interoperability/methodology; parallel, no L2 gate
- LIST + JusticeBench tagging (in flight ✓)
- Name the rules/presentation-separation principle in the philosophy
- Eviction Lab / CCDI / Pew / CJDC — awareness, messaging context, possible outcome-validation signal later
- NODS/NIEMOpen — awareness; alignment point only if CJaC extends to court-data interaction
- Study LSC DB schema structure for completeness ideas (the non-content-changing part)

---

## Does any of this change the answer on running L2 now?

**No material gate on service L2.** The only T1 finding (LSC DB cross-check) is a *corroboration source*, not a schema change — service methods are core content the LSC DB would validate, not alter. So:
- **Service L2 proceeds** as planned.
- **Add the LSC Eviction Laws Database as a second corroboration source** for the L2 runs generally — a high-authority cross-check alongside GPT/Gemini (esp. valuable because it's statute-linked). This *strengthens* L2 rather than delaying it. (One nuance: LSC is 2021-frozen, so where CJaC and LSC diverge, check whether it's a CJaC error OR a post-2021 legal change — the same recency discipline from today's review.)
- **The schema-completeness study** (does CJaC omit post-judgment/bond/fee elements the LSC DB includes?) is worth doing, but it concerns *future modules*, not the notice/service bright-line work — so it informs roadmap, not the current run.

**Net:** the research adds a valuable corroboration source and a couple of methodology/credibility points, surfaces a schema-completeness question for future modules, and confirms CJaC's positioning — without gating the service L2 run. Disciplined outcome: incorporate the additive value, note the one real schema-completeness question for the roadmap, proceed with L2.

---

*Standards & Content Landscape Assessment · June 18, 2026 · Live-verified. Authority/currency judgments are Claude's; adoption decisions are Andy's.*
