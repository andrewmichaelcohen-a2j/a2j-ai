# CJaC ↔ Legal Design Lab / JusticeBench — Standards Alignment & Leverage Spec

**Date:** June 18, 2026 · **Context:** Aligning CJaC with the data standards, taxonomies, and datasets published by Stanford Legal Design Lab (Margaret Hagan) on JusticeBench / legalhelpcommons.org (per her June 18, 2026 article "Data Standards and Datasets for Legal Help R&D").

**Strategic frame:** CJaC occupies Hagan's **Track 3 — legal workflows** (the applied, jurisdiction-specific decision logic she names as the scarce, high-value, least-captured layer). Aligning CJaC's schema and testing with her shared standards makes CJaC the **interoperable, executed reference implementation** of that layer — a contributor to the commons, not a competitor. Adopt her connective-tissue standards; keep CJaC's distinct contribution (validated decision logic) ours to execute.

> Validate exact field names / code formats against the live standards before implementing — pull from justicebench.org/#datasets, taxonomy.legal (LIST), and the FIPS list. The *content* below is the alignment intent; match their canonical formats.

---

## 1. Schema additions — interoperability tags (per rules file)

Add a standards-tagging block to `eviction_schema_v2.0.json` so every CJaC rules file is natively labelable in the shared ecosystem:

- **`list_codes`** — the LIST issue taxonomy code(s) for the matter (taxonomy.legal). Eviction/housing issue codes. Lets CJaC files be tagged and matched the same way as the rest of the field's content.
- **`fips_jurisdiction`** — FIPS code for the jurisdiction (state, and county where relevant), replacing/supplementing the current state-name structure. Hagan's standards use FIPS as the jurisdiction key; adopting it makes CJaC files natively compatible with JusticeBench and the Content Index / Org & Service standards.
- **`task_taxonomy_ids`** — the Legal Help Task Taxonomy IDs (JusticeBench, stable IDs like TS-01-xx) that each CJaC module maps to (e.g., Issue-Spotting, Deadline Calculator, Form Selection map onto notice/procedural modules). Slots CJaC's modules into the shared task framework.
- **`language`** — ISO language code (their standard).

These are **additive metadata** — they don't change CJaC's decision logic, they make it interoperable. Document the additions in `SCHEMA_V2_DESIGN_SPEC.md` and note the alignment to the JusticeBench standards.

## 2. Currency / freshness enum — adopt their vocabulary (for L6)

Hagan's Content Index standard uses a `currency status` enum: **current / aging / stale / unknown**, plus last-reviewed and revised dates. CJaC's L6 freshness layer should adopt this exact enum rather than inventing its own, so freshness status is expressed in the field-standard vocabulary. Add `currency_status` + `last_reviewed_date` to the validation metadata.

## 3. JusticeBench datasets → CJaC L4 golden sets

Hagan has published synthetic, PII-free, labeled query datasets directly usable as L4 test material:
- **High Risk Legal Help Queries** (failure-mode scenarios across 6 states) — highest relevance; purpose-built for the failure cases L4 should test.
- **L3Q** (3,300+ LIST-labeled legal-help questions), **Common-48**, **LHSQ115**, **Common Legal Help Questions** — synthetic, jurisdiction-tagged query sets.

**Action:** pull the eviction/housing-tagged subsets from these (filter by LIST housing codes) as seed inputs for CJaC's L4 golden sets — run CJaC's rules against them and check the rules produce correct outputs. Free, labeled, synthetic (no PII), purpose-built. This accelerates L4 substantially and aligns CJaC's testing with shared field datasets.

## 4. Rubric-as-eval — adopt the principle (methodological upgrade)

Hagan's deepest methodological point: **"The standard for doing the work and the standard for judging it are the same thing."** Her PII rubric is simultaneously the expert's checklist *and* the tool-evaluation test.

**Apply to CJaC:** unify the attorney **reviewer checklist** (the standard for *doing* validation) and the automated **L4 eval / golden-set test** (the standard for *judging* a rules file) into a **single artifact per module** — a rubric expressed so both a human reviewer and the automated layer apply the same criteria. The eviction-notice reviewer checklist *is* the notice-module eval. This tightens the validation story (no gap between what humans check and what machines test) and is exactly the kind of rigor that strengthens the "complete, correct, validated" claim. Restructure `REVIEWER_CHECKLIST.md` toward machine-applicable rubrics per module.

## 5. Per-step actor calibration (finer-grain confidence metadata — consider)

Hagan decides, per workflow step, whether it should be done by "a senior human, a junior human, deterministic rules-based code, a small lightweight model, or an intensive frontier model." This is a finer grain than CJaC's current module-level bright-line/open-textured calibration. **Consider** adding step/field-level `actor` or `assurance_tier` metadata where a module contains a mix of deterministic and judgment steps. Optional refinement; evaluate after the core alignment.

---

## Priority order

1. **LIST + FIPS + task-taxonomy tags** (schema addition) — highest interoperability payoff, low effort. Do first.
2. **JusticeBench datasets → L4 golden sets** — accelerates L4 with free, purpose-built data.
3. **Rubric-as-eval restructure** — deepest methodological upgrade; do as L4 is built so they're designed together.
4. **Currency-status enum** — small, fold into L6 design.
5. **Per-step actor calibration** — optional refinement, later.

## Guardrail

Adopting her standards aligns CJaC's *labeling and testing* with the field; it does not change CJaC's distinct contribution (validated decision logic) or its honesty discipline. Tagging a file with LIST/FIPS/task codes makes it interoperable; it does not make it validated. Status labels remain governed by CJaC's own ladder.

---

*CJaC ↔ JusticeBench Standards Alignment · June 18, 2026 · Adopt the connective-tissue standards; keep the validated-decision-logic execution as CJaC's contribution.*
