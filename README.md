# Civil Justice as Code (CJaC)

**Open, machine-readable legal decision logic for civil justice — starting with 50-state residential eviction defense.**

Apache 2.0 · Model-agnostic · Built for institutional stewardship — not a product, not a company.

---

## What this is

The civil-justice AI ecosystem can already *retrieve* what statutes say. What has not been built and openly validated is the layer encoding what the law *requires* — the if/then decision logic, jurisdiction by jurisdiction, in a form both people and machines can use, audit, and trust.

**Civil Justice as Code builds that layer.** It is a library of open-source, machine-readable rules files that encode the decision logic of residential eviction defense across all 50 states and the District of Columbia — the notice rules, service requirements, overlays, substantive defenses, and procedural defects that determine whether an eviction is lawful — validated with the discipline of safety-critical software plus expert legal review.

This is the applied **legal-workflow / decision-logic layer**: the part the legal-help field has identified as the scarcest and least-captured, because it is the knowledge that usually lives only in an experienced attorney's head. CJaC writes it down, structures it, validates it, and publishes it openly so it can be built on, localized, and trusted.

> **Why it matters.** The goal is *trustworthy at scale*. Reliable, free legal information in front of the millions of people who face eviction without a lawyer — for whom the alternative is nothing, or confidently-wrong free content. Trustworthiness is what makes scale a good thing rather than a harmful one: the people this serves can least afford a wrong answer.

---

## Honest status

CJaC publishes its work *with honest status labels at every stage* rather than waiting for perfection. **Nothing here is presented as more validated than it is.**

**Current status (June 2026):** All 51 jurisdictions are at **AUTOMATED-CHECKS-PASSED** for the core notice module — drafted and passing all currently-implemented automated validation layers. **This is not the same as attorney-validated.** Expert human validation (the layer that makes "validated" mean what a lawyer would mean) is in progress, beginning with a California flagship.

### The status ladder

```
DRAFT → AUTOMATED-CHECKS-PASSED → UNDER REVIEW → VALIDATED → CERTIFIED
                               ↑ no automated process crosses this line
```

- **DRAFT** — generated, not yet passing all automated checks.
- **AUTOMATED-CHECKS-PASSED** — passes all implemented automated layers (statutory retrieval, consistency, anomaly detection, multi-model consensus). *Corroborated, not validated.*
- **UNDER REVIEW / VALIDATED** — a named, licensed attorney has reviewed and validated the content.
- **CERTIFIED** — second independent attorney + advisory board (stewardship phase).

**No automated process advances a file past AUTOMATED-CHECKS-PASSED.** "Validated" always means a human lawyer.

---

## Results, open questions, and roadmap — the whole record, in order

Start with [`docs/A2J_STACK_AND_CJAC_SCOPE.md`](docs/A2J_STACK_AND_CJAC_SCOPE.md) for what this project is and isn't — the front door to everything below. Then [`docs/VALIDATION_README.md`](docs/VALIDATION_README.md) for the validation record itself: scores (always dual-reported if corrected — see below), the signed errata, and the raw scorer output, each one or two clicks from here. Then read [`docs/OPEN_QUESTIONS_AND_LIMITATIONS.md`](docs/OPEN_QUESTIONS_AND_LIMITATIONS.md) — the eleven things we haven't proven yet, published deliberately, each with its planned test. Then [`docs/CJAC_ROADMAP.md`](docs/CJAC_ROADMAP.md) for where the project is headed on both axes that matter (more jurisdictions and practice areas; deeper into judgment-dependent law) and what has to be true before each step. Outreach collateral (two-pager, pitch deck) lives in [`collateral/`](collateral/), versioned like everything else. That's the whole record — validation record, open questions, roadmap, collateral — in the order a skeptical reader should walk it.

---

## How it's validated

CJaC's method is **automation for coverage and triage; human expertise, surgically, for judgment.** Full detail in [`docs/VALIDATION_PHILOSOPHY.md`](docs/VALIDATION_PHILOSOPHY.md).

- **Brute-force automation** retrieves every governing statute, checks internal consistency, detects cross-jurisdiction anomalies, monitors for legal change, and assesses the published corpus in structured form.
- **Smart automation** (multi-model consensus across independent frontier models) corroborates each claim and, more importantly, *flags divergence* — where models disagree with the file or each other is where a human should look.
- **A tiered resolution protocol** routes each flagged discrepancy to the lightest sufficient resolution: mechanical/citation issues are AI-resolved; substantive-but-resolvable disagreements get an AI reasoning pass; genuine interpretive questions go to an attorney. This narrows mandatory human review to true legal-judgment questions without lowering the labeling standard.
- **Surgical human review** spends scarce attorney expertise only on what survives that narrowing.

The labeling discipline is fixed throughout: **automation improves content and raises confidence; it never crosses the validation line.**

CJaC's validation program is designed to align with recognized standards — the NIST AI Risk Management Framework, enterprise software testing discipline, and certified-performance-under-defined-conditions standards from safety-critical software — without claiming formal certification against any of them.

---

## Scope: five modules per jurisdiction

Residential eviction defense is encoded as five rules modules, ordered bright-line → open-textured:

1. **Notice** — validity of the eviction notice: pay-or-quit, cure-or-quit, termination; periods; defects that void it.
2. **Service** — how the notice/summons must be served; service defects.
3. **Overlays** — federal (CARES Act), state-protective (e.g., just-cause statutes), and local rules.
4. **Substantive defenses** — retaliation, habitability, discrimination, quiet enjoyment.
5. **Procedural defects** — flaws in the eviction filing itself.

Each module carries **confidence-calibration metadata** (`openness`, `review_weight`) recording how much automated assurance its status reflects — so a passed open-textured module is never read as more validated than a passed bright-line one.

---

## Interoperability

CJaC adopts widely-used legal-help data standards so its outputs can plug into the broader ecosystem rather than forming a silo: **LIST** legal-issue codes, **FIPS** jurisdiction codes, the **Legal Help Task Taxonomy**, and ISO language codes. CJaC is designed to be the interoperable, executed reference implementation of the decision-logic layer.

---

## Repository structure

```
rules/        Machine-readable eviction rules files (JSON), per state, schema v2 (5 modules)
  schema/     The rules schema
  validation/ The automated validation battery (L1–L6 layers, multi-model consensus)
docs/         Project plan, validation philosophy, status records, schema spec, review queue
demos/        Demonstration application (eviction notice validator)
plugins/      Claude legal plugins
playbooks/    Legal workflow playbooks
```

Key documents:
- [`docs/A2J_STACK_AND_CJAC_SCOPE.md`](docs/A2J_STACK_AND_CJAC_SCOPE.md) — **start here:** where CJaC sits in the larger access-to-justice problem, what it deliberately does and doesn't do, and why
- [`docs/VALIDATION_README.md`](docs/VALIDATION_README.md) — the results: scores, corrections, and where every piece of evidence lives, in plain English
- [`docs/OPEN_QUESTIONS_AND_LIMITATIONS.md`](docs/OPEN_QUESTIONS_AND_LIMITATIONS.md) — the eleven things we haven't proven, published on purpose
- [`docs/CJAC_ROADMAP.md`](docs/CJAC_ROADMAP.md) — the strategic map: jurisdictions/practice areas × depth of judgment, phases, gates
- [`docs/GLOSSARY.md`](docs/GLOSSARY.md) — shared vocabulary (the Band 1/2/3 taxonomy and other recurring terms)
- [`docs/VALIDATION_PHILOSOPHY.md`](docs/VALIDATION_PHILOSOPHY.md) — the methodology
- [`docs/STATUS_LABELS.md`](docs/STATUS_LABELS.md) — the status ladder and advancement rules
- [`docs/DISCLAIMER.md`](docs/DISCLAIMER.md) — legal information, not legal advice

---

## Important: legal information, not legal advice

The files in this repository are **legal information** — a structured representation of publicly available statutory requirements. They are **not legal advice**, do not create an attorney-client relationship, and should not be relied upon without verification by a licensed attorney. Files at DRAFT or AUTOMATED-CHECKS-PASSED status are not attorney-reviewed. See [`docs/DISCLAIMER.md`](docs/DISCLAIMER.md) for deployment requirements. Do not use non-VALIDATED files to advise a real person about their legal rights.

---

## License & contact

Licensed under the Apache License, Version 2.0. Copyright 2026 Andrew M. Cohen.

Contributions, pressure-testing, and collaboration are welcome — this work is meant to be used, checked, and built on. Contact: andrewmichaelcohen@gmail.com
