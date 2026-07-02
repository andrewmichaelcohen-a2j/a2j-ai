# CJaC — Architecture

**Version:** 1.0  
**Date:** 2026-07-01  
**Directive:** `docs/CJaC_Playbook_Architecture_Directive_20260701.md`  
**Status:** Playbook architecture active; Stage 1 (registry + specs) in progress

---

## 1. What CJaC is

CJaC (Civil Justice as Code) is a **validated rules layer** for legal AI — not a predictor, not a search engine, not a chatbot. It encodes how law applies to specific facts, in machine-readable form, validated through a multi-layer process involving automated retrieval, multi-model consensus, and human attorney review.

The pipeline output for any fact pattern is:

> "Under [jurisdiction]'s law, [element] is [result], because [encoded rule / bounded-reasoning conclusion with anchor]."

Every claim is traceable. Every claim is auditable. Honesty discipline is non-negotiable: the system returns UNCERTAIN when it cannot give a grounded answer, rather than guessing.

---

## 2. The three-tier infrastructure

| Tier | Layer | Role |
|------|-------|------|
| **Tier 1** | AI foundation | Translation, reasoning, drafting (Claude — predictive) |
| **Tier 2** | Legal & safety layer | MCP connectors to live law; validation tooling; skills |
| **Tier 3** | Decision logic / rules layer | Machine-readable, auditable rules encoding how law applies to specific facts — CJaC's contribution |

CJaC's work is Tier 3. The AI (Tier 1) and connectors (Tier 2) serve the rules layer — not the other way around.

---

## 3. One pipeline, playbook units

### 3.1 One pipeline

There is **one pipeline** for all claim types. CA notice, CA retaliation, TX notice, NM service defects — all run through the same architecture. The pipeline does not branch by claim type; it operates on **playbooks**, and playbooks are what differ.

### 3.2 The playbook unit

A **playbook** is the unit of encoding. It answers one legal question for one claim type in one jurisdiction. Examples:

- CA pay-or-quit notice playbook
- CA §1942.5 retaliation defense playbook
- LA RSO overlay playbook (layers on CA state-law playbooks)
- TX 3-day notice playbook

Playbooks compose: a CA notice scenario in Los Angeles invokes the CA notice playbook AND the LA RSO overlay playbook, with the more-protective/more-specific layer controlling on conflict.

### 3.3 Elements

Each playbook is decomposed into **elements** — the discrete legal questions that must be answered to resolve the claim. Elements are the atomic unit of encoding and validation.

Each element has:
- A **name** and **description** (human-readable)
- A **strategy tag** (`determinate` or `open_textured`) — set at encoding time by a human attorney
- A **known/unknown flag** per jurisdiction
- A **source hierarchy** (which sources govern for this element)
- The **encoded rule** (for determinate elements) OR a **bounded-reasoning procedure** (for open-textured elements)

---

## 4. Strategy tags

### 4.1 `determinate`

The element has a specific, codeable answer under current law. The model looks up and applies the encoded rule. No discretion is exercised. Output is deterministic.

**Examples:**
- Notice period for tenancy ≥ 1 year (60 days under Civ. Code §1946.1(b)) — the answer is in the statute
- Payee ID required in pay-or-quit (CCP §1161(2)) — mandatory content requirement, binary
- SFH exemption from AB 1482 just-cause (Civ. Code §1946.2(e)(8)) — specific statutory carve-out

**Output:** Tier A confidence (rule text directly supports result).

### 4.2 `open_textured`

The element requires legal judgment that cannot be fully codified. The element specifies:
- The **citation anchor** — the source the model must reason from
- The **analytical framework** — the legal test the element applies (e.g., McDonnell Douglas for retaliation burden-shifting)
- Acceptable **confidence tiers** (A/B/C — see Section 5)

The model executes a **bounded-reasoning procedure**: reasons from the anchor, applies the framework, and returns a structured assessment.

**Examples:**
- Whether a landlord's action constitutes retaliation (temporal proximity + pretext analysis)
- Whether a partial payment acceptance waives a notice defect (fact-specific, doctrine-governed)
- Whether a tenant has a warranty-of-habitability defense (habitability standard application)

**Key:** open_textured ≠ "anything goes." The anchor and framework constrain the analysis. The tag is a human attorney's judgment that this element requires reasoning, not lookup.

---

## 5. Confidence tiers

| Tier | Meaning | Typical source |
|------|---------|---------------|
| **A** | Determinate: encoded rule directly controls; no discretion. OR: open-textured, citation text directly + unambiguously supports conclusion | Encoded JSON rule / retrieved statute text |
| **B** | Open-textured: bounded-reasoning conclusion; anchor retrieved and applied; conclusion plausible and well-supported but involves judgment | Case law / statutory interpretation |
| **C** | Open-textured: anchor unavailable or insufficient to support a conclusion; explicit uncertainty warranted | No controlling authority retrieved |

A Tier C output is a correct, honest result — not a failure. The system's job is to be right, not to always have an answer.

---

## 6. Known/unknown flag

Every element in every playbook carries a **`known`/`unknown`** flag for each jurisdiction:

- **`known`** — the rule is encoded (determinate) or the bounded-reasoning procedure is specified (open_textured). The system can give a grounded answer.
- **`unknown`** — the element exists in this jurisdiction but the answer is not yet encoded. Pipeline output: "This element has not been encoded for [jurisdiction]. A definitive answer is not available."

Unknown elements are **never silently omitted or defaulted.** They surface explicitly. "Withhold rather than guess" is the safety default.

---

## 7. Jurisdiction-resolution architecture

Jurisdiction resolution **precedes** rule application. See `docs/Decision_Logic_Briefing_for_Claude.md` Section 9 for the canonical principle.

In brief: eviction law is a stack — state → county → city → rent-control zone. The more-protective/more-specific layer controls on conflict. Un-encoded local jurisdictions are flagged, never silently defaulted to state-only.

Three required components:
1. **Jurisdiction-detection gate** — resolve which local ordinances attach before applying substantive rules
2. **Explicit conflict/override semantics in JSON** — each rule must express whether a local layer can override it and in which direction
3. **Known-unknown flag for un-encoded jurisdictions** — surface gaps explicitly

Roadmap: CA (LA RSO + JCO, SF, Oakland) first.

---

## 8. Validation pipeline (seven layers)

| Layer | What it checks |
|-------|---------------|
| **L1** | Schema compliance — rules file structure matches `eviction_schema_v2.0.json` |
| **L2** | Multi-model consensus — two independent models corroborate each holding |
| **L3** | Internal consistency — cross-element and cross-jurisdiction logical consistency |
| **L4** | Golden-set scoring — Direction B outcome-based testing against attorney-frozen fact patterns |
| **L5** | Cross-jurisdiction sanity — compare rules across states; flag outliers |
| **L6** | Currency / freshness — statute/case law dates; stale-law flag |
| **L7** | Human review — genuine legal-interpretive judgment; attorney line |

L4 (golden-set scoring) is where the playbook architecture is validated. The held-out score is the honesty metric. See `docs/COWORK_DIRECTION_B_GOLDEN_SETS.md`.

---

## 9. Bucket taxonomy (validation output classification)

All validation results use this taxonomy — never blended rates:

| Bucket | Meaning |
|--------|---------|
| **MV** | Machine-verified: text retrieved, two independent models corroborated holding |
| **CI** | Confirm-inference: corroborated but control=INFERRED; routes to cheap confirm lane |
| **RC** | Re-characterize: text retrieved, holding diverged; genuine inaccuracy → attorney re-characterization |
| **PR** | Pending-retrieval: text NOT retrievable (infrastructure failure, not verification failure). Never routes to attorney. |
| **SM** | Single-model-preliminary: only one model answered. Never machine-verified. |

For outcome-based testing (Direction B / L4): results are `correct` / `incorrect` / `uncertain` per item, with held-out and non-held-out reported separately.

---

## 10. Staged proof sequence (per Playbook Architecture Directive)

| Stage | What | Gate |
|-------|------|------|
| **0** | Close pilot honestly | ✅ COMPLETE (2026-07-01) |
| **1** | Build registry + confirm skills/tools | In progress (2026-07-01) |
| **2** | PROOF 1: CA notice as deterministic proof | Unlocked after Stage 1 |
| **3** | PROOF 2: CA retaliation as bounded-reasoning proof | After Stage 2 score ≥90% |
| **4** | Scale decision | Andy signs off after both proofs |

---

## 11. Source hierarchy

Every playbook element has a source hierarchy. For CA eviction:

1. **CA statute text** (primary — retrieved live via Legal Data Hunter MCP)
2. **CA case law** (primary — retrieved via CourtListener MCP; Descrybe for hard-to-find cases)
3. **CA Judicial Council UD Benchguide** (third corroborating source — corroborates only; statute/case remains primary; currency check required)
4. **LSNC Eviction Guide / practitioner materials** (secondary — synthesized, not cited directly)
5. **Multi-model consensus** (verification mechanism, not a source)

See `docs/VALIDATED_RESOURCES_REGISTRY.md` for the full registry with reliability ratings.

---

## 12. Reasoning engine — decision and rationale

**Decision (2026-07-01):** Claude's native legal-reasoning capability is the reasoning engine for all open-textured element evaluation, element decomposition, determinacy tagging proposals, and bounded-reasoning procedure execution.

**What this means:**
- When a `determinate` element is evaluated: the model looks up the encoded rule in JSON and applies it. No external skill needed.
- When an `open_textured` element is evaluated: the model reasons from the specified citation anchor, applies the analytical framework, and returns a structured confidence-tiered assessment. This uses Claude's native legal analysis capability directly.
- Element decomposition proposals (proposing which elements belong in a playbook and which strategy tag to apply) use Claude's native capability, subject to attorney ratification.

**`legal:*` plugin skills — NOT adopted wholesale:**
The `legal:*` plugin skills (brief, review-contract, risk-assessment, triage-nda, etc.) are designed for corporate/contract/compliance legal workflows and do not directly map to eviction-defense element encoding. These skills are NOT wired into the CJaC pipeline. Use a `legal:*` skill only if a specific, narrow task (e.g., structured contract risk flagging) cleanly maps to one — and document the decision. Otherwise, rely on Claude's native capability, which the 7-layer validation stack already wraps and checks.

**Rationale:** The 7-layer stack (L1–L7) with multi-model consensus and attorney review IS the validation that wraps the model's native legal reasoning. Adding intermediary skill layers between the model and the pipeline would add complexity without adding validation rigor. The bottleneck is completeness and accuracy of encoding — not the reasoning capability itself.

**Lawvable MCP:** Available in the environment (`lawvable_search_skills`); not yet explored for eviction-specific legal skills. Stage 1 carry-over research task. May be evaluated for specific narrow use cases if it surfaces skills purpose-built for eviction law or defense-element decomposition.

---

## 13. Key files

| File | Location | Purpose |
|------|----------|---------|
| Playbook spec | `docs/PLAYBOOK_SPEC.md` | Schema for a playbook unit (elements, tags, procedures) |
| Validated Resources Registry | `docs/VALIDATED_RESOURCES_REGISTRY.md` | Living catalog of sources |
| Architecture directive | `docs/CJaC_Playbook_Architecture_Directive_20260701.md` | The 2026-07-01 directive from Andy |
| JSON schema | `rules/schema/eviction_schema_v2.0.json` | v2 rules file schema |
| Decision logic briefing | `docs/Decision_Logic_Briefing_for_Claude.md` | Accurate characterization of the decision logic layer |
| Work queue | `docs/WORK_QUEUE.md` | NOW/NEXT/BLOCKED/HORIZON |
| Direction B | `docs/COWORK_DIRECTION_B_GOLDEN_SETS.md` | Golden-set discipline |

---

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
