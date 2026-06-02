# LHC Eviction Rules Library

**⚠️ ALL FILES IN THIS RELEASE ARE DRAFT STATUS — AI-GENERATED AND NOT REVIEWED BY A LICENSED ATTORNEY.**

This library is published openly for transparency and community validation, not for use in advising real people. See [DISCLAIMER.md](DISCLAIMER.md) and [STATUS_LABELS.md](docs/STATUS_LABELS.md).

---

## What this is

A machine-readable library of residential eviction notice rules for all 50 US states plus the District of Columbia. Each file encodes jurisdiction-specific eviction decision logic as structured JSON data — notice periods, procedural defects, affirmative defenses, and local overlays.

This is **Layer 3** of the LHC A2J AI architecture: the rules data layer that grounds AI reasoning in explicit, auditable, statutory logic rather than in opaque training-data inference.

**The library is a community infrastructure project.** AI drafts the files. Licensed attorneys validate them. The community maintains them. Every validated file benefits every A2J deployment that uses it.

## Current status

| Metric | Value |
|--------|-------|
| Jurisdictions covered | 51 (50 states + DC) |
| Files with DRAFT status | 51 |
| Files with attorney validation | 0 |
| Statutory retrieval performed | 4 (CA, TX, NY, FL) |
| Automated validation (L3) | 51/51 PASS |

**This is v0.1 — the first public release of the DRAFT corpus.** Attorney validation (Layer 7) has not begun. We are actively seeking licensed tenant attorneys in each state to serve as reviewers.

## Repository structure

```
eviction-rules-library/
├── README.md                    ← This file
├── LICENSE                      ← Apache 2.0
├── NOTICE                       ← Attribution
├── schema/
│   └── eviction_schema_v1.0.json    ← JSON Schema for all rules files
├── rules/
│   ├── california/
│   │   └── ca_eviction_v1.json      ← DRAFT
│   ├── texas/
│   │   └── tx_eviction_v1.json      ← DRAFT
│   └── ... (51 jurisdictions)
├── validation/
│   ├── battery/
│   │   └── validate.py              ← Layers 1–6 automated battery
│   ├── golden_sets/                 ← L4 test cases (to be authored)
│   └── reports/
│       └── validation_report_latest.json
├── demo/
│   ├── RulesComparisonWidget.jsx    ← React comparison widget
│   └── RulesComparisonWidget.html   ← Standalone browser version
└── docs/
    ├── STATUS_LABELS.md
    ├── CONTRIBUTING.md
    ├── REVIEWER_CHECKLIST.md
    └── DISCLAIMER.md
```

## Why this matters

Before this library existed, every A2J AI tool either (a) encoded eviction rules in training data — opaque, stale, not auditable — or (b) reinvented the rules from scratch for each deployment. Neither scales.

This library is the shared content layer that makes the Anthropic plugin/MCP infrastructure actually useful for A2J: one team validates California's rules once; every deployment everywhere benefits forever.

## The validation roadmap

**Automated layers (built, running):**
- Layer 1: Statutory grounding check (4/51 retrieved, 47 pending)
- Layer 3: Internal consistency (~40 checks per file) — 51/51 PASS
- Layer 5: Cross-jurisdiction anomaly detection — running

**Community layers (needed):**
- Layer 7: Licensed attorney review — **this is the critical gap**

Each state needs at least one licensed tenant attorney to review the DRAFT file, verify all statutory citations against current law, and sign a validation statement. See [REVIEWER_CHECKLIST.md](docs/REVIEWER_CHECKLIST.md).

## We need attorney reviewers

If you are a licensed tenant attorney and can validate the rules file for your state, please open an issue or submit a pull request. You will receive permanent attribution in the file's metadata.

Priority states (highest eviction volume): **California, Texas, New York, Florida, Illinois, Georgia, Ohio, Pennsylvania, North Carolina, Michigan.**

## License

Copyright 2026 Andrew M Cohen. Licensed under the [Apache License, Version 2.0](LICENSE).

Free to use, modify, and redistribute — including in paid services and other AI models — with attribution. Chosen specifically so A2J deployments can use these files in any context without restriction.

---

* eviction-rules-library v0.1 · June 2026*
