# CJaC — Cowork Change Directive: Playbook Architecture

**Date:** 2026-07-01  
**From:** Andy (Andrew M Cohen)  
**Status:** ACTIVE — Stage 0 complete; Stage 1 in progress  
**Filed by Cowork:** 2026-07-01 session (post-pilot)

---

## Context

First Direction B pilot score: 3/5 = 60% held-out. All 6 misses are rules-gap (not model-wrong). This directive is Andy's architectural response to the pilot score — not just "encode 6 more rules" but a structural restructuring of how encoding works and how proofs are sequenced.

---

## Section 0 — Thesis anchor (read before any other section)

CJaC is a **validated rules LAYER** — not a predictor, not a search engine, not a chatbot. The pipeline output for any given fact pattern is:

> "Under [jurisdiction]'s law, [element] is [determinate result / open-textured assessment with confidence tier and citation], because [encoded rule / bounded-reasoning conclusion with anchor]."

Every claim is traceable. Every claim is auditable. The 60% pilot score is the system being honest: it correctly returned UNCERTAIN when rules were missing rather than guessing. That honesty is the design. The fix is completeness of encoding, not softening of standards.

---

## Section 1 — What stays the same

These are permanent fixtures. Nothing in this directive changes them:

1. **Seven-layer validation stack** (L1–L7) — the trust ladder is immutable
2. **Golden-set discipline** — held-out partition is sealed at freeze; optimizer never sees it; attorney establishes ground truth; immutables never crossed by automation
3. **Deterministic JSON encoding** — every determinate rule is encoded; every result is traceable to a statute or holding
4. **Repo / overnight / morning report rhythm** — Direction A operating cadence continues
5. **Honesty discipline** — "machine-verified" is below the attorney line; model-verified below attorney-validated; nothing is a claim until it has passed its gate
6. **Model-agnostic, open-source posture** — no lock-in; architecture must work with any frontier model

---

## Section 2 — New architecture: Playbook as unit of encoding

### 2.1 The playbook unit

A **playbook** is the unit of encoding going forward. A playbook answers one legal question for one claim type in one jurisdiction. The CA pay-or-quit notice playbook, the CA retaliation defense playbook, and the LA RSO overlay playbook are three separate playbooks that compose when the fact pattern requires it.

Each playbook is decomposed into **elements** — the discrete legal questions that must be answered to resolve the full claim. Each element is tagged AT ENCODING TIME by a human attorney as either:

- **`determinate`** — the element has a specific, codeable answer under current law. The model looks up and applies the encoded rule. Output: deterministic result + citation.
- **`open_textured`** — the element requires legal judgment that cannot be fully codified. The model executes a **bounded-reasoning procedure**: reasons from a citation anchor, applies the analytical framework encoded for this element, and returns a structured assessment with confidence tier.

The `determinate`/`open_textured` tag is a human attorney judgment, not an AI judgment. It encodes the attorney's view of how the law works for this element.

### 2.2 Bounded-reasoning procedure (for open_textured elements)

An open_textured element specifies:
- The **citation anchor** (the source the model must reason from — statute, regulation, or case holding)
- The **analytical framework** (the legal test the element applies — e.g., McDonnell Douglas for retaliation, notice-void doctrine for defective notices)
- The **known-unknown flag** — whether this jurisdiction's answer is encoded (`known`) or gap-flagged (`unknown`)
- Acceptable **confidence tiers** for the output: A (high confidence, text directly supports conclusion), B (medium confidence, plausible reading), C (low confidence, explicit uncertainty warranted)

### 2.3 Confidence-tiered output

All pipeline output carries a confidence tier per element:

| Tier | Meaning |
|------|---------|
| **A** | Determinate element with text anchor; result is fully specified by encoded rule |
| **B** | Open-textured element; bounded-reasoning conclusion; citation anchor retrieved and applied |
| **C** | Open-textured element; citation anchor unavailable or insufficient; explicit uncertainty |

A Tier C output is a correct, honest result. It is not a failure. The system's job is never to guess; Tier C is the system being honest about the limits of current encoding.

### 2.4 Known/unknown flag

Each element in each playbook carries a **`known`/`unknown` flag** for each jurisdiction:
- `known` — the rule is encoded (determinate) or the bounded-reasoning procedure is specified (open_textured)
- `unknown` — the element exists in this jurisdiction but the answer is not yet encoded. Pipeline output: "This element has not been encoded for [jurisdiction]. A definitive answer is not available."

Unknown elements are never silently omitted or defaulted. They are explicitly surfaced.

---

## Section 3 — Validated Resources Registry

A **Validated Resources Registry** (`docs/VALIDATED_RESOURCES_REGISTRY.md`) is the living catalog of sources CJaC relies on. Every source in the registry is:
- Identified by name + access method
- Classified by type (primary legal, secondary, standards dataset, tool/connector, skill)
- Rated for reliability and currency
- Notes any limitations (jurisdiction coverage, currency risk, access constraints)

The registry is the answer to "where did this come from?" for every element in every playbook.

**Seed entries per this directive:**
- Primary legal sources: CourtListener (MCP), Descrybe (MCP), Legal Data Hunter (MCP)
- Secondary sources: CA Judicial Council UD Benchguide, LSNC Eviction Guide 2026
- Standards datasets: JusticeBench / Stanford Legal Design Lab (Hagan), LSC/Temple
- Skills/tools: Claude native legal-analysis capability, `legal:*` plugin skills (brief, risk-assessment, review-contract, triage-nda)
- Methodology standards: 7-layer stack, multi-model consensus, Krippendorff's α

---

## Section 4 — Staged execution (two proofs required before scale)

### Stage 0 — Close the pilot honestly ✅ COMPLETE
- Steps 5–7 executed: living docs updated, misses triaged, memo ingested, exclusions logged
- Score stands: 3/5 = 60% held-out. Held-out set burned. GPT-only (Gemini depleted).

### Stage 1 — Build the registry + confirm skills/tools (NOW)
1. Create `docs/VALIDATED_RESOURCES_REGISTRY.md` — seed per Section 3; verify each entry exists and is accessible
2. Create `docs/ARCHITECTURE.md` — document the one-pipeline playbook architecture
3. Create `docs/PLAYBOOK_SPEC.md` — playbook unit schema spec: element structure, tag definitions, confidence tiers, known/unknown
4. Confirm whether the model's legal-analysis and issue-spotting skills (e.g., Lawvable, `legal:*` plugin) have been used to date; wire in if not
5. Research CA Judicial Council UD Benchguide: locate, verify currency, add to registry
6. Check Stanford LIST / JusticeBench for reusable defense-element decompositions

### Stage 2 — PROOF 1: CA notice as deterministic + playbook proof
- Restructure CA-notice module into a playbook unit per PLAYBOOK_SPEC.md
- Close all 6 pilot gaps as complete `determinate` elements, including exceptions and interactions
- Draft fresh CA-notice golden set (prior held-out set is burned; needs new items)
- Run scorer: target ≥90% held-out on CA notice
- This is the deterministic proof: shows the architecture works for clean, rule-codeable elements

### Stage 3 — PROOF 2: Retaliation as bounded-reasoning proof
- Restructure CA retaliation module into a playbook unit
- Tag retaliation elements as `open_textured`; specify bounded-reasoning procedures
- Build retaliation golden set (attorney-frozen)
- Run scorer: demonstrate bounded-reasoning produces correct outcomes on fact patterns with legal judgment required
- This is the open-textured proof: shows the architecture works for elements that require reasoning, not just lookup

### Stage 4 — Scale decision (gated on both proofs)
- Only after Stage 2 + Stage 3 complete, scores demonstrated, and Andy signs off
- Scale playbook architecture to remaining CA modules, then TX/NY, then full 50-state

---

## Section 5 — Documentation requirements

The following docs must be created or updated as part of Stage 1:

| Document | Status |
|----------|--------|
| `docs/ARCHITECTURE.md` | Create (Stage 1) |
| `docs/VALIDATED_RESOURCES_REGISTRY.md` | Create (Stage 1) |
| `docs/PLAYBOOK_SPEC.md` | Create (Stage 1) |
| `docs/WORK_QUEUE.md` | Update (Stage 1 NOW; Stage 2 NEXT) |
| `docs/DAILY_CHANGELOG.md` | Update (Stage 1 GREEN entries) |
| `docs/CLAUDE_CHAT_BRIEF.md` | Update (post-directive state) |

---

## Section 6 — Success metric

The success metric for this directive is a **substantially higher held-out score on CA notice**, targeting 90–95%+. The architecture is validated only when the held-out score demonstrates it works — not before.

Secondary metric: the retaliation bounded-reasoning proof demonstrates the architecture handles open-textured elements without collapsing to UNCERTAIN.

---

*Directive issued 2026-07-01 by Andy (Andrew M Cohen). Filed to docs/ by Cowork 2026-07-01 Stage 1.*  
*Copyright 2026 Andrew M Cohen. Apache 2.0.*
