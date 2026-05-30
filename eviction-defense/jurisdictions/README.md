# Jurisdiction Rules Files

This folder contains the JSON rules files that encode eviction notice decision logic for each supported jurisdiction.

## What these files are

Each JSON rules file encodes **decision logic** — the structured if/then reasoning that applies statutory text to specific facts. This is distinct from the statutes themselves, which are retrieved live via the Legal Data Hunter MCP connector.

The reasoning engine reads the appropriate rules file based on the jurisdiction. To add a new state: create a new `{state_code}_eviction_rules_v0.1.json` following the same schema. The skill logic does not change — only the data file changes.

## Validation status

| File | Jurisdiction | Statutes Covered | AI-Drafted | Attorney-Validated | Validated By | Date |
|------|-------------|-----------------|-----------|-------------------|-------------|------|
| `ca_eviction_rules_v0.1.json` | California | CCP §1161, §1162; Civ. Code §1941, §1942.5, §1946.2 (AB 1482, amended by AB 1529) | ✅ | ❌ | — | — |
| `tx_eviction_rules_v0.1.json` | Texas | Prop. Code §24.005, §91.001; SB 38 (2026); CARES Act §4024 | ✅ | ❌ | — | — |
| `ny_eviction_rules_v0.1.json` | New York | RPAPL §711, §735; RPL §226-c, §232-a/b, §235-b; HSTPA 2019; Good Cause Eviction Law (2024) | ✅ | ❌ | — | — |

**⚠️ All files are DRAFT. Do not use in any deployment advising real tenants until attorney-validated.**

## Statutory retrieval log

CA rules verified against live statute text retrieved via Legal Data Hunter on 2026-05-30:
- CCP §1161: https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=1161.
- Civil Code §1946.2 (AB 1482): https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1946.2.

**Important note:** Civil Code §1946.2 (AB 1482) was amended by AB 1529 (Stats. 2025, eff. Jan 1, 2026) and is **repealed as of January 1, 2030** unless extended by the legislature. Monitor for renewal.

## Attorney validation checklist

For each rules file, a validating attorney should confirm:

- [ ] All notice types and required periods are correct
- [ ] All defect triggers accurately reflect the law (no over-inclusion or under-inclusion)
- [ ] Affirmative defenses list is complete for the jurisdiction
- [ ] Service requirements are accurate
- [ ] Local overlay flags (rent control cities, etc.) are correctly identified
- [ ] Statutes cited are current and not superseded
- [ ] Any recent legislative changes are reflected
- [ ] Output templates are appropriate (not legal advice)

## Schema

Each rules file follows this structure:

```json
{
  "_metadata": { "jurisdiction", "version", "status", "statutes", "validation_note" },
  "notice_periods": { ... defect_triggers per notice type ... },
  "service_requirements": { ... defect_triggers ... },
  "[jurisdiction_specific_law]": { ... },
  "affirmative_defenses": [ ... ],
  "intake_questions": { ... },
  "output_templates": { ... }
}
```

## Adding a new jurisdiction

1. Copy an existing rules file as a template
2. Update all jurisdiction-specific fields
3. Retrieve the current statutes via Legal Data Hunter for verification
4. Mark status as `DRAFT`
5. Submit a PR — and if possible, identify an attorney in that jurisdiction to validate
