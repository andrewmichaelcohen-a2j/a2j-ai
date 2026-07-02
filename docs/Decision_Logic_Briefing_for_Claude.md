# Briefing: Decision Logic Layer — Accurate Characterization
## For use in future Claude sessions on the Civil Justice as Code project
*Andrew M Cohen · June 9, 2026*

---

## Purpose

This document corrects and sharpens the characterization of the decision logic layer — what it is, where it comes from, and how to describe it accurately. An earlier version of the demo narrative was imprecise. This document is the authoritative framing. Use it to update any project materials that describe the rules layer.

---

## 1. What the decision logic layer is — precisely

The rules files (JSON) encode **AI-synthesized legal doctrine**: the structured encoding of how law applies to specific facts, drawing on statutory text, judicial interpretation, and practitioner knowledge.

This is distinct from:
- **Statutory transcription** — statutes state what the law says; the rules layer encodes how the law applies to specific facts
- **AI prediction / hallucination** — the rules are derived from identifiable legal sources and are fully auditable; every rule can be inspected and challenged
- **Document assembly** (A2J Author, HotDocs) — document assembly helps users fill out forms; the rules layer determines whether a legal instrument (e.g., an eviction notice) is legally valid or defective

---

## 2. The three source types the AI draws on

When generating the rules files, the AI synthesized across:

1. **Statutory text** — retrieved live via Legal Data Hunter (MCP connector) for CA, TX, NY, FL; used from training knowledge for remaining states
2. **Judicial interpretation** — how courts have applied the statutory language to specific fact patterns (case law)
3. **Practitioner knowledge** — the accumulated understanding encoded in legal aid guides, bar publications, tenant rights resources, and practitioner consensus materials

The AI cannot produce a discrete citation list for sources 2 and 3 — this is how large language models work. The synthesis happens across training data, not from discrete retrievable lookups. This is a key reason attorney validation is required.

---

## 3. The California late-fee example (use this to make it concrete)

CCP §1161(2) says an eviction notice must state "the amount that is due" in the context of a rent default. It does not explicitly say "late fees are prohibited." The rule that including late fees voids the notice comes from:
- Reading the statute in context (it governs rent default, so the amount due means rent)
- California courts confirming this interpretation in decisions applying §1161(2)
- Decades of practitioner application in CA eviction defense

The rules file encodes this as: IF notice includes late fees → THEN result = INVALID (CCP §1161(2)). The statute is the anchor. The judicial and practitioner interpretation is what makes the rule specific enough to apply to a specific notice.

---

## 4. Why this requires attorney validation — precisely

We are NOT asking attorneys to check whether the AI copied the statute correctly. We are asking them to confirm whether the AI's **synthesis of legal doctrine** — its encoding of how courts and practitioners have applied the statute — is accurate for each jurisdiction. That requires:
- Current jurisdiction-specific knowledge
- Ability to identify where the AI's synthesis may be wrong, incomplete, or outdated
- Professional judgment on contested or ambiguous interpretations

This is a genuine legal task, not a clerical check. It is the reason "attorney review" is the final and highest-stakes validation layer.

---

## 5. The demo narrative — corrected

**Old (imprecise):** "The rules file adds decision logic from the statute."

**Correct:** "The statute states what the law says. The rules file encodes how the law applies to Maria's specific facts — drawing on the statutory text, judicial interpretation, and practitioner knowledge synthesized by AI. That synthesis is what catches the defect. Without it, even live statute retrieval is insufficient."

**The comparison widget** shows this contrast: left panel = AI + live statute retrieval, no rules file → 0 defects found (wrong). Right panel = AI + live statute + encoded legal doctrine → 2 defects found (correct).

---

## 6. Demo scope vs. project scope

**Demo shows:** Pre-filing eviction notice triage (one slice of one workflow) — notice type identification, procedural defect detection, affirmative defense screening. Three states: CA (full), TX/NY (portability demonstration).

**Project builds:** Complete eviction decision logic for all 50 states + DC, covering the full range of decisions an unrepresented tenant needs to navigate — from notice receipt through court resolution. Then: consumer debt defense → benefits denial appeals → record sealing → DV/immigration (highest stakes last).

The demo is proof of concept for the method. The project is systematic buildout of the full library.

---

## 7. Current status of the rules files

- **CA** (`rules/eviction/california/ca_eviction_v1.json`): Best-developed. Statutory text retrieved live. Most likely to be accurate. Attorney validation is the immediate priority.
- **TX, NY, FL**: Statutory text retrieved live for TX and NY; FL retrieved via Florida Legislature website. Reasonably grounded.
- **Remaining 47 states**: Generated from AI training knowledge. Each file is flagged `statutory_retrieval_performed: false`. All require attorney review before any production use.
- **All files**: Labeled DRAFT. Not for use in advising real people.

---

## 8. Files updated in this session (June 9, 2026)

- `demos/eviction/prompts/demo-script.md` — Scene 3 and Scene 4 language updated to use accurate "AI-synthesized legal doctrine" framing
- `demos/eviction/widget/RulesComparisonWidget.html` — Left panel updated from "Based on training data" to "AI + live statute retrieval / no rules file"
- `docs/Review_Slides_v0.1.pptx` — Two review slides created: Demo Scope vs. Project Scope; What Decision Logic Is and Where It Comes From

---

## 9. Jurisdiction-resolution architecture (added 2026-07-01 — Architecture Memo Section 1)

**Canonical principle:**
> *Jurisdiction resolution precedes rule application. The operative rule for any fact pattern is the composition of applicable state/county/city layers, with the more-protective/more-specific layer controlling on conflict. Un-encoded local jurisdictions must be flagged, never silently defaulted to state-only.*

**Why this matters:** Eviction law is a stack — state → county → city → (sometimes) rent-control zone. In high-need urban markets (LA, SF, Oakland), local ordinances layer on top of state law with stricter, often outcome-changing tenant protections. A state-only rule in these jurisdictions can produce a confidently wrong answer that runs against the tenant. Example: under LAMC §151.09(A)(1), a tenant in an LA RSO unit who owes $1,500 on a 1-bedroom has no nonpayment eviction exposure because the amount owed is below one month's HUD Fair Market Rent (~$2,081). A state-only rule says the pay-or-quit is valid. That is a false negative on a defense the tenant actually has — worse than "I don't know."

**Three required components:**
1. **Jurisdiction-detection gate:** Before applying substantive rules, resolve which local ordinances attach (driven by address/city and property characteristics: build date, unit count, owner type). Withhold a determinate answer for jurisdiction-sensitive questions until jurisdiction is resolved. "Withhold rather than guess" is the safety default.
2. **Explicit conflict/override semantics in JSON:** Each rule must represent whether a local layer can override it and in which direction. The schema must express "local layer adds elements / narrows availability / changes the notice-validity test" — not merely "different number."
3. **Known-unknown flag for un-encoded jurisdictions:** When an address is in a jurisdiction with local ordinances not yet encoded, output: "this unit may be subject to local [City] ordinances not yet in this dataset; a state-only answer may be incomplete." Converts a silent gap into a visible, honest limitation.

**Roadmap:** Start with 2-3 highest-need CA cities: LA (RSO + JCO), SF, Oakland. See `docs/CJaC_Architecture_and_Roadmap_Memo_20260701.md` for full spec.

---

*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*
