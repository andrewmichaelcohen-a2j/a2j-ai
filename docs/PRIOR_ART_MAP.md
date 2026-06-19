# Prior-Art Map — Civil Justice as Code

**Date:** June 18, 2026 · **Prepared by:** Claude (live-verified focused sweep) · **For:** Andy **Purpose:** A *focused, deliberate* map of prior and concurrent efforts relevant to CJaC — so model/scope decisions are made against the whole landscape at once, not incrementally as prior art surfaces piecemeal.

**Honesty on completeness:** This is a strong map, not a guaranteed-complete one. My retrieval has a knowledge cutoff and the field is fragmented across silos (public-health-law, legal-aid, computational-law, civic-tech, academia) that don't cross-cite well — the field's own literature calls this the "civil justice data gap." Treat this as a high-confidence map of the *major* efforts, with a standing note to re-run periodically. Confidence flagged per entry.

---

## Why prior art surfaced incrementally (and the fix)

Earlier searches were *reactive* (triggered by specific names: JusticeBench, then LSC). This is the first *systematic* sweep searching by **category of effort** rather than by name — which is what catches peers neither of us has named. The fix going forward: treat this map as a living doc, re-run the category sweep before each major outreach, and log new entries here so prior art is never "discovered" mid-pitch.

---

## The landscape, in four layers

CJaC's exact position \= **current \+ validated \+ machine-readable decision logic \+ explicit validation methodology \+ open \+ multi-domain-intended.** No single effort occupies all of that. Here's who occupies what:

### Layer 1 — Eviction LAW, structured (the closest "prior art" to CJaC's content)

**1A. LSC / Temple LawAtlas Eviction Laws Database** — *\[HIGH relevance, HIGH confidence\]*

- Structured, statute-linked eviction law (notice, timelines, causes, post-judgment), 50 states \+ DC \+ territories \+ 30 localities. Policy-surveillance method, inter-coder reliability. Law-as-of Jan 2021 (one update Nov 2022). Free (account required), Excel-downloadable. **Detailed in `LSC_CASE_STUDY.md`.**  
- **What it means for CJaC:** the closest content precedent; proves the method; differentiator \= currency \+ maintenance model \+ AI economics \+ open-textured extension. Use as corroboration baseline. Borrow "policy surveillance" \+ "inter-coder reliability" credibility framing.

**1B. Consumer legal-info 50-state surveys** (Nolo, Justia, FindLaw, AAOA) — *\[LOW relevance, HIGH confidence\]*

- Human-written 50-state landlord-tenant summaries. **Unstructured** (prose, not machine-readable data), commercially maintained, not validated/citable as data, not open. These are the *status quo CJaC improves on* — the "confidently-readable but unstructured, unvalidated, non-machine-usable" baseline. Useful only as: a content cross-reference, and a foil ("the existing alternative is prose on commercial sites").

### Layer 2 — Rules-as-Code METHODOLOGY with AI (the closest "prior art" to CJaC's *approach*)

**2A. Policy2Code Challenge / Rules as Code Community of Practice (RaC CoP)** — *\[HIGH relevance, HIGH confidence\] — THE KEY METHODOLOGICAL PEER*

- Run by **Georgetown's Digital Benefits Network (Beeck Center) \+ Massive Data Institute.** 12 US/Canada teams, June–Sept 2024, published findings Oct 2024–Feb 2025\. Used **multiple LLMs** to translate **public-benefits policy (SNAP, Medicaid) across 7 states** into plain-language logic \+ code. Active community of practice ([rulesascode@georgetown.edu](mailto:rulesascode@georgetown.edu)).  
- **Their findings independently validate CJaC's core design choices** (this is gold for your methodology credibility):  
  - *"LLMs require external knowledge and human oversight within an iterative process for any policies containing complex logic"* → your automation-narrows-humans-validate thesis, confirmed by an independent multi-team study.  
  - *"LLMs struggle when they have to synthesize end-to-end logic for complex, multi-step tasks"* → your bright-line vs. open-textured distinction, confirmed.  
  - *"Modular design is particularly important in LLM workflows"* → your five-module decomposition, confirmed.  
  - *"A structured test suite would enable more systematic validation"* → your golden-set / outcome-testing roadmap, confirmed as the recognized need.  
  - RAG \+ re-ranking to fight "needle in haystack" / "information scattering across sections" → directly relevant to your L1 retrieval design.  
- **What it means for CJaC:**  
  - **Position CJaC as the eviction-domain, validated, *productized* instance of what RaC CoP is exploring as method.** They run *experiments and prototypes*; CJaC builds a *validated, maintained library*. Different maturity, same family.  
  - **This is a natural community to join and cite.** It's the organized home of exactly CJaC's methodology. Engaging it (a) gives CJaC peer-community standing, (b) is a citation source that makes CJaC legible, (c) is a venue/audience. **Strongly consider engaging the RaC CoP** — it's the single most aligned community found.  
  - **Note the domain difference:** they focus on *public benefits eligibility*; CJaC is *eviction defense*. Adjacent civil-justice domains, same method. (And benefits is a natural CJaC roadmap domain — they're prior art for *that* future module too.)  
  - **Their honest limitation findings protect you:** you can cite an independent multi-team study showing LLMs need human oversight — strengthening your never-overclaim discipline with external evidence.

**2B. Rules-as-code tooling/engines** (OpenFisca, Blawx, Suffolk Docassemble/AssemblyLine, DMN, MIT Blawx) — *\[MEDIUM relevance, HIGH confidence\]*

- Open-source legal-rules encoding \+ delivery tools. OpenFisca (gov-grade, UNDP/OECD). Suffolk \= closest *delivery* layer (CourtFormsOnline). DMN \= decision-logic standard.  
- **What it means:** these are *engines/formats*, not validated rule libraries. CJaC's decision logic could potentially *target* these (e.g., be expressible in DMN, or power a Docassemble interview) — interoperability/delivery options, not competitors. Adopt the "separate rules from interview/presentation logic" principle (Suffolk). Park DMN-expressibility as a future interoperability question.

### Layer 3 — AI legal-aid TOOLS for eviction (concurrent, application layer)

**3A. Stanford Legal Design Lab — AI & Access to Justice / AI co-pilots for eviction defense** — *\[HIGH relevance, HIGH confidence\]*

- Margaret Hagan's lab is *actively building AI co-pilots for eviction defense \+ intake/screening*, partnering with legal aid orgs (San Bernardino, San Diego, Oklahoma), Winter 2026 studio. Plus JusticeBench/LIST standards (already adopting). Co-organizing AI4A2J@ICAIL 2025 workshop.  
- **What it means for CJaC:** Stanford operates at the *application/tool \+ standards* layer; CJaC at the *validated decision-logic* layer that such tools *need underneath*. **Complementary, not competitive** — their co-pilots need exactly CJaC's validated rules as a trustworthy backend. This *strengthens* the collaboration thesis: CJaC is the validated-rules layer for the tools the field (including Stanford) is building. (Also: confirms the attribution dynamic is moot — they're tool-building, you're rules-building; align.)

**3B. Stanford Legal Aid Intake/Screening AI experiments** — *\[MEDIUM relevance, HIGH confidence\]*

- Their own writeups candidly note the limitation: *"LLM is not a legal expert and can't be updated like a database without re-training... might not capture local nuances... latest California-specific procedural rules."* **This is the exact gap CJaC fills** — a current, updatable, validated knowledge layer the LLM tools lack. Their stated limitation is CJaC's value proposition, in their own words.

### Layer 4 — Eviction/civil-justice DATA (filing counts, not law) — context, not prior art

**4A. Princeton Eviction Lab · 4B. LSC Civil Court Data Initiative · 4C. Georgetown Civil Justice Data Commons · 4D. NCSC NODS** — *\[LOW-MEDIUM relevance, HIGH confidence\]*

- Court-filing data, case-level court-data standards (NODS). **Different layer** (what happened in cases, not what the law requires). Context, messaging, awareness, possible future court-data interop (NODS). Not prior art for CJaC's rules content.

---

## What this map changes for CJaC's model decisions

**1\. One genuinely important addition to engage: the Rules as Code Community of Practice (Georgetown DBN/MDI).** This is the organized methodological home of CJaC's approach. It's not a competitor — it's the peer community \+ citation source \+ validation-of-method \+ future-domain prior art (benefits). *Decision to consider: engage/join/cite it.* It also gives you independent external evidence for your never-overclaim discipline.

**2\. No prior effort forces a scope change — the landscape confirms CJaC's niche is real and unoccupied.** Nobody is doing current \+ validated \+ machine-readable \+ open \+ methodology-explicit eviction decision logic. The pieces exist in separate layers; CJaC integrates them. This is reassuring against the scope-creep worry: the focused sweep did NOT surface a "you must now also do X" — it surfaced *corroboration* and *allies*.

**3\. The positioning sharpens to a precise sentence:**

*"The structured-law precedent (LSC/Temple) proved eviction law can be coded but isn't maintained current. The methodology community (Georgetown Rules-as-Code) is proving AI can assist policy-to-code translation but at experiment/prototype stage. The tool-builders (Stanford) are building AI eviction co-pilots that need a trustworthy rules layer underneath. CJaC is the missing piece all three imply: a current, validated, open, machine-readable eviction decision-logic library, built with the methodology the field is converging on. It doesn't compete with any of them — it's the validated substrate they each need."*

**4\. Three concrete alliance/citation targets** (all confirmed active, all complementary): **Georgetown DBN/MDI Rules-as-Code CoP** (method peer/community), **Stanford Legal Design Lab** (tools \+ standards, already aligning), **LSC/Temple LawAtlas** (content precedent/baseline). Engaging these positions CJaC inside the field's existing fabric rather than as an outsider.

**5\. Independent validation of CJaC's design choices** (cite these — they're external, recent, multi-team):

- Modular decomposition: validated by Policy2Code.  
- Human-oversight-required / automation-can't-bless: validated by Policy2Code \+ the hallucination-reliability literature.  
- Bright-line vs. complex-logic distinction: validated by Policy2Code.  
- Structured test suites / outcome testing as the validation frontier: named by Policy2Code as the needed next step.  
- Currency/maintenance as the unsolved problem: demonstrated by LSC's staleness.

---

## Standing process (to prevent incremental prior-art surprises)

- This map is a **living repo doc**. Re-run the category sweep before each major outreach.  
- Categories to sweep: (a) structured eviction/landlord-tenant law datasets; (b) rules-as-code \+ AI for law/policy; (c) AI legal-aid tools for housing; (d) legal-data standards bodies; (e) civil-justice data commons/court data.  
- Log any new entry here with relevance \+ confidence \+ "what it means for CJaC."  
- **Before outreach, this map \+ the methodology red-team together \= your "we know the landscape and have answered the obvious challenges" preparation.**

---

*Prior-Art Map · June 18, 2026 · Focused category sweep, live-verified. Strong but not guaranteed-complete; re-run before outreach. Relevance/confidence and positioning judgments are Claude's; decisions are Andy's.*  
