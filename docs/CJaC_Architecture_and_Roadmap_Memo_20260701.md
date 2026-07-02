# CJaC — Post-Pilot Architecture & Roadmap Memo

**Author:** Andrew M. Cohen
**Date:** 2026-07-01
**Status:** Canonical architectural direction. Supersedes nothing; adds first-order requirements surfaced during the CA-notice golden-set freeze.
**Audience:** Andy (strategy), Claude (strategic advisor/chief of staff), Cowork (repo writes, validation runs).
**Purpose:** Capture four architectural/strategic requirements surfaced during the Proof-of-Validation Pilot so none is lost, and communicate the Cowork-actionable items. None of these expand the current CA-notice pilot; all are sequenced to begin AFTER the first held-out score.

---

## 0. Sequencing discipline (read first)

These are first-order requirements, but they are **next**, not now. The order is deliberate:

1. Finish the CA-notice state-law pilot → first honest held-out score (proves the METHOD on determinate state law).
2. Then build the jurisdiction layer and the other items below (proves the method extends to the layered reality where evictions actually happen).

Doing them in this order keeps each proof clean. Do not let any item below pull scope into the current pilot.

---

## 1. Jurisdiction resolution must precede rule application (FIRST-ORDER ARCHITECTURE REQUIREMENT)

### The problem
CJaC's CA rules currently answer as if "CA" is the operative jurisdiction. But eviction law is a **stack**: state → county → city → (sometimes) rent-control zone. In dense urban markets — LA, SF, Oakland, San Diego, Long Beach — local ordinances layer on top of state law with stricter, often outcome-changing tenant protections. These are exactly the jurisdictions where the access-to-justice gap is largest.

A state-only rule in these jurisdictions does not merely leave a gap — it can produce a **confidently wrong answer that runs against the tenant**, in the place where being wrong is most costly. Example surfaced in the pilot (CA-NOT-19, excluded): under LAMC 151.09(A)(1), a tenant in an LA RSO unit who owes $1,500 on a 1-bedroom is NOT evictable for nonpayment, because the amount owed is below one month's HUD Fair Market Rent (~$2,081). A state-only rule would say the pay-or-quit is valid and the tenant has no defense. That is a false negative on a defense the tenant actually has — worse than "I don't know," because it discourages a valid defense.

### The requirement
**Jurisdiction resolution must precede substantive rule application.** Concretely:

1. **Jurisdiction-detection gate.** Before applying substantive rules, resolve which local ordinances attach — driven by address/city and the property characteristics that trigger coverage (e.g., build date for RSO's pre-1978 line, unit count, owner type). Until jurisdiction is resolved, the system must WITHHOLD a determinate answer for jurisdiction-sensitive questions rather than default to state-only. "Withhold rather than guess" is the safety default.

2. **Explicit conflict/override semantics in the JSON.** Each rule must represent whether a local layer can override it and in which direction. The operative rule for any fact pattern is the COMPOSITION of applicable state/county/city layers, with the more-protective / more-specific layer controlling on conflict. The schema must express "local layer adds elements / narrows availability / changes the notice-validity test" — not merely "different number." (LA example: state permits a pay-or-quit for any unpaid rent; LA narrows availability to amount > FMR, adds a notice-content element [state bedroom count], and adds a procedural element [LAHD filing within 3 business days].)

3. **Known-unknown flag for un-encoded jurisdictions.** CJaC cannot encode every CA municipality at once. When an address is in a jurisdiction with local ordinances not yet encoded, the rule must say so: "this unit may be subject to local [City] ordinances not yet in this dataset; a state-only answer may be incomplete." This converts a silent gap into a visible, honest limitation — and feeds the improvement loop (un-encoded jurisdictions become a prioritized work queue).

### Roadmap
- Start with the 2-3 highest-need CA cities: **LA (RSO + JCO), SF, Oakland.** Do not boil the ocean.
- LA overlay golden items are ready to spec — elements captured from LAMC 151.09: FMR-threshold, bedroom-count statement in notice, LAHD 3-business-day filing.
- Each local-overlay item needs a re-verification cadence (see Section 3 — local ordinances are the most volatile part of the law).

---

## 2. Benchbooks / judicial benchguides as a first-class source class

### The insight
Judicial benchguides (e.g., the California Judicial Council **Landlord-Tenant Litigation (Unlawful Detainer) Benchguide**) are a distinct and high-value authority type. A statute states the black-letter rule; a case shows application to specific facts; a **benchguide states how judges are instructed to OPERATIONALIZE the law** — the checklist a judge runs, which defects are treated as fatal, the procedural sequence, where discretion lives. For a system encoding DETERMINISTIC law, this is the closest thing to a canonical "what the correct answer is in practice," authored by the neutral arbiter rather than an advocate.

### Three uses
1. **Validation cross-check.** Use benchguides as a third corroborating source alongside statute + case law. "Validated against statute, controlling case law, AND the Judicial Council benchguide" is a stronger credibility claim than another practitioner article, because it is the court's own operational standard.
2. **Golden-set candidate generation.** Benchguides contain the exact fact patterns and defect taxonomies judges are trained on — near-ideal raw material for determinate golden-set items (several pilot items would have been cleaner if drafted from benchguide framing).
3. **Capturing the statute-to-practice gloss.** Benchguides encode true-in-practice standards not obvious from statute alone (strict-compliance posture; residential/commercial distinctions) — exactly the layer where the pilot drafts most needed correction.

### Two cautions
- **Authority hierarchy.** A benchguide is secondary/persuasive, not binding. Frozen items must still cite the statute/case the benchguide relies on as PRIMARY authority, with the benchguide as corroboration — the same discipline applied to practitioner sources in the pilot.
- **Currency.** Benchguides update on a lag and may not yet reflect recent amendments (e.g., the Feb 1 2025 CCP 1161 court-day change; SB 567's 2024 changes — both outcome-relevant in the pilot). Use benchguide + a currency check on recent amendments.

### Scope note on federal resources
The FJC *Benchbook for U.S. District Courts* and the *Civil Litigation Management Manual* are largely OUT OF SCOPE — eviction/UD is overwhelmingly state law in state court. Prioritize STATE Judicial Council benchguides. Narrow federal touchpoints exist (federally subsidized housing, VAWA, CARES Act covered-property notice) and should be flagged where they intrude, but that is a small subset, not the FJC benchbook's domain.

---

## 3. Direction D — Continuous Validation & Improvement Loop (design, do not build yet)

### Concept
Turn CJaC from "validated once" into a living system that provably improves. The deepest form of the value proposition is not a single held-out score but a DEMONSTRATED IMPROVEMENT CURVE with an inspectable audit trail. This aligns with the "trust gap is CJaC's job" framing and generalizes the honesty discipline already in the pilot. (Conceptually parallel to Nadella's "learning loop / private evaluation" framing — the frozen golden sets are CJaC's private eval and its durable IP; models are swappable substrate beneath it.)

### The signal source — CRITICAL ETHICAL CONSTRAINT
The improvement signal is **evidence that an encoded JSON rule is INACCURATE as a statement of law** — NOT litigation win/loss. CJaC's "outcome" is whether a person has a fair opportunity through accurate access to the law (a level playing field), not whether any litigant prevails. Wiring case win/loss in as a training signal would optimize toward "what wins" rather than "what the law requires," on the backs of real tenants. The signal source must remain: attorney-validated correctness against frozen ground truth + real-world evidence of rule inaccuracy (new cases, statutory amendments, benchguide updates, legal-aid partner feedback, changed local ordinances).

### Three separable components (different risk profiles — build separately)
1. **Monitoring / measurement (low risk, high value):** agents re-run the scorer on a cadence; track held-out score over time; flag regressions. Build soon after the first pilot score. Nearly pure upside.
2. **Real-world input ingestion (medium risk):** new fact patterns and rule-inaccuracy signals from real civil-justice sources. Each input passes the SAME attorney-freeze gate as the pilot — no unreviewed real-world data becomes ground truth.
3. **Automated rule-tuning (highest risk = Direction C):** agents PROPOSE rule changes to improve scores; human RATIFIES; held-out set stays untouchable. Gate hardest. Extend the scorer's integrity constraints (immutability, held-out isolation, no answer leakage) to the improvement loop.

### Anti-gaming metric definition
"Continuously more accurate" needs a gaming-resistant definition. Headline = held-out score over time, PAIRED WITH: (a) coverage (modules/states/jurisdictions with frozen golden sets), and (b) regression count (did improving X break Y?). So "improvement" cannot be bought by narrowing scope. Local-ordinance changes are a clean, high-signal "rule now inaccurate" input for this loop.

---

## 4. Pilot-score reporting scope discipline

When reporting the CA-notice held-out score, always include a one-line scope statement:

> "This score measures state-law CA-notice encoding on determinate bright-line items. Local/municipal overlays and the open-textured defense modules (retaliation, habitability) are separate, in-progress layers and are not reflected in this number."

Rationale: a strong STATE score must not be allowed to imply JURISDICTION-COMPLETE correctness. This generalizes the exclusion discipline already applied in the pilot (4 of 20 CA-notice candidates excluded: open-textured, retaliation-module, service-module, and municipal-overlay).

---

## 5. Cowork-actionable items (communicate to Cowork)

1. **Add to the canonical architecture doc** the Section 1 principle verbatim: *"Jurisdiction resolution precedes rule application; the operative rule is the composition of applicable state/county/city layers, more-protective/more-specific controlling on conflict; un-encoded local jurisdictions must be flagged, never silently defaulted to state-only."* Add a `jurisdiction_resolution` design note to the rules schema roadmap covering the detection gate, override semantics, and known-unknown flag.

2. **Add a benchguide source lane** to the validation pipeline: for each module/jurisdiction, identify the controlling state Judicial Council benchguide and use it as a THIRD corroborating source (after statute + case law) in validation runs — with authority-hierarchy discipline (benchguide corroborates; statute/case remains primary) and a currency check against recent amendments. Start with the CA Judicial Council UD Benchguide for the notice + service modules.

3. **Log Direction D** in the work queue as a designed workstream (three components per Section 3), explicitly gated: monitoring after first score; ingestion behind the attorney-freeze gate; automated tuning = Direction C, hardest gate. Record the ethical signal-source constraint (Section 3) as a non-negotiable.

4. **Add the reporting scope note** (Section 4) to the pilot-score reporting template.

5. **Build the LA RSO + JCO overlay golden-set** as the first local-overlay module AFTER the state pilot produces its first score. Elements: LAMC 151.09(A)(1) FMR-threshold; bedroom-count notice statement; LAHD 3-business-day filing. Include a re-verification cadence (LA amended RSO Feb 2026; LA County doubled its nonpayment threshold Apr 2026).

**None of the above changes the current CA-notice pilot. All begin after the first held-out score.**

---

*CJaC · Architecture & Roadmap Memo · Copyright 2026 Andrew M Cohen. Apache 2.0.*
