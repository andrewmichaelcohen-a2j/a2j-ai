# Rules Layer

Machine-readable JSON files encoding A2J legal decision logic by jurisdiction and workflow.

**Status:** DRAFT — all files AI-generated, no attorney validation complete yet.

Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.

---

## What the rules layer is

The rules layer is the structured data that grounds AI legal reasoning in explicit statutory logic rather than training-data inference. Each file encodes the if/then decision logic for a specific legal workflow in a specific jurisdiction — notice periods, defect triggers, affirmative defenses, service requirements.

The reasoning engine (Claude + the plugin skills) reads these files and applies them deterministically. Change the rules file → change the jurisdiction. The engine doesn't change.

## Current contents

| Folder | Workflow | Jurisdictions | Status |
|--------|---------|---------------|--------|
| `eviction/` | Residential eviction notice triage | 50 states + DC | DRAFT |

## Structure

```
rules/
├── README.md               ← This file
├── schema/
│   └── eviction_schema_v1.0.json   ← JSON Schema (lock before generating files)
├── eviction/               ← One subfolder per state
│   ├── california/
│   │   └── ca_eviction_v1.json
│   ├── texas/
│   │   └── tx_eviction_v1.json
│   └── ... (51 jurisdictions)
└── validation/
    ├── battery/
    │   └── validate.py     ← Layers 1–6 automated checks
    ├── reports/
    │   └── validation_report_latest.json
    └── golden_sets/        ← L4 test cases (to be authored per state)
```

## Adding a new workflow

To add a new A2J workflow (e.g., debt collection, benefits appeals):

1. Define a JSON schema in `schema/{workflow}_schema_v1.0.json`
2. Create a `{workflow}/` subfolder with one directory per state
3. Generate DRAFT files using the schema as a template
4. Run the validation battery against all files
5. Recruit licensed attorneys to validate (see [../docs/REVIEWER_CHECKLIST.md](../docs/REVIEWER_CHECKLIST.md))

## Validation status

See `validation/reports/validation_report_latest.json` for the current automated validation report.

- **Layer 1** (live statutory grounding): 4/51 retrieved; 47 pending
- **Layer 3** (internal consistency): 51/51 PASS
- **Layer 7** (attorney review): 0/51 complete — **seeking reviewers**

Priority states for attorney review: CA, TX, NY, FL, IL, GA, OH, PA, NC, MI.

---

*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*
