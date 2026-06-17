# Eviction Schema v2 — Design Spec & Canonical Patterns

**File:** `docs/SCHEMA_V2_DESIGN_SPEC.md`  
**Schema:** `rules/schema/eviction_schema_v2.0.json`  
**Last updated:** June 16, 2026 — added no-notice-period pattern (NJ correction)  
*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*

---

## Purpose

This file documents design decisions, canonical patterns, and field semantics for the eviction-v2 schema. When a new schema addition establishes a library-wide convention, it is recorded here. Reviewers and future contributors should read this file before extending the schema or encoding edge-case jurisdictions.

---

## Canonical Pattern 1: No Notice Period + Subsidy-Conditional Exception

**Added:** June 16, 2026 (NJ correction — Andrew Cohen attorney review)  
**Applies to:** Any state where no statutory notice is required before filing for a given ground (e.g., nonpayment), except for federally subsidized or other conditional properties.

### The Problem

Standard schema representation assumes a `days` integer in `tenancy_all`. Some states have no notice period for a given ground at all — filing is permitted immediately. Using `days: 0` is wrong (implies "same-day notice required"). Using `days: 1` is wrong (implies one day required). The field must be explicitly absent.

### The Solution

Use these three fields together on the `pay_or_quit` (or other notice type) object:

```json
"pay_or_quit": {
  "notice_required": false,
  "exceptions": [
    {
      "condition": "federally_subsidized_housing",
      "notice_required": true,
      "notice_period_days": 14,
      "authority": "federal subsidy program rules; cf. [state statute carve-out]"
    }
  ],
  "tenancy_all": {
    "days": null,
    "statute": "[statute establishing the ground + statute establishing no notice required]",
    "count_method": "calendar_days"
  }
}
```

**Field semantics:**

| Field | Value | Meaning |
|-------|-------|---------|
| `notice_required` | `false` | No statutory notice required for this ground before filing (market-rate tenancy) |
| `tenancy_all.days` | `null` | No period — not 0, not 1. Absence is explicit. |
| `exceptions[].condition` | `"federally_subsidized_housing"` | Machine-readable condition identifier |
| `exceptions[].notice_required` | `true` | Notice IS required for this sub-category |
| `exceptions[].notice_period_days` | `14` | Days required under the exception |
| `exceptions[].authority` | string | Statutory / regulatory authority for the exception |

### Why not `days: 0`?

`0` would be misread as "a notice is required but must be served on the same day." The legal rule is that no notice is required at all — the landlord may file the summary dispossess action immediately. `null` + `notice_required: false` is the only machine-readable encoding that is accurate.

### validate.py behavior

- L3: When `notice_required: false`, the "cannot determine notice period" warning is suppressed (updated June 16, 2026).
- L5: When `tenancy_all.days = null`, the state is excluded from the cross-jurisdiction period comparison (L5 period outlier check compares only integer values).
- Both checks pass cleanly without spurious flags.

### Current implementations in the library

| State | Ground | Rule | Exception |
|-------|--------|------|-----------|
| NJ | Nonpayment of rent | §2A:18-61.2 — nonpayment excluded from notice-to-quit; immediate filing | Federally subsidized housing: 14 days |

### When to use this pattern

Use this pattern when:
1. A state statute expressly excludes a ground from any notice-to-quit requirement, AND
2. The correct answer is "no notice needed" for the base case (not merely "period unknown"), AND
3. There is at least one conditional exception (subsidy, property type, tenancy type) where notice IS required.

If the period is simply unknown or unverified, do NOT use `notice_required: false`. Instead, leave the days field with the best available estimate and add an attorney-verification note. Use `notice_required: false` only when the legal rule is confirmed as "no notice."

---

## Canonical Pattern 2: Resolved-* Flag Dispositions

**Added:** June 16, 2026 (L5 outlier resolution — validate.py update)

The `validation.flags[].disposition` field supports values beyond the schema's declared enum (`"open"`, `"acknowledged"`, `"resolved"`). Specifically, `resolved-*` variants are in use:

| Disposition | Meaning |
|-------------|---------|
| `"open"` | Flag not yet reviewed |
| `"acknowledged"` | Known/accepted; not blocking |
| `"resolved"` | Fixed (generic) |
| `"resolved-confirmed"` | Attorney confirmed the flagged value is correct law |
| `"resolved-false-positive"` | Flag was a false positive; L3/L5 logic does not apply here |
| `"resolved-corrected"` | Content was corrected; the original flagged value is gone |

**validate.py behavior:** All dispositions that `startswith("resolved")` are preserved across runs (not overwritten by fresh flag generation). This prevents re-opening attorney-reviewed flags on each run.

---

## Schema Version History

| Version | Date | Key additions |
|---------|------|---------------|
| v2.0 | 2026-06-15 | Initial v2 (5-module: notice, service, overlays, substantive_defenses, procedural_defects) |
| v2.0 (patch) | 2026-06-16 | Added `notice_required` (boolean) and `exceptions` array to `pay_or_quit`; allowed `notice_period.days` to be null; validate.py L3 updated to recognize `notice_required: false` |

---

*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*
