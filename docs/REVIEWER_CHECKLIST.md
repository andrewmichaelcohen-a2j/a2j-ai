# Attorney Reviewer Checklist

This checklist defines the standard that every attorney reviewer must meet before a file can advance from DRAFT to VALIDATED status.

Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.

---

## Who may review

Any attorney licensed and in good standing in the relevant jurisdiction. Tenant-side experience is strongly preferred but not required. The reviewing attorney's name and bar number will be recorded in the file's `reviewer` field and will remain in the file's history permanently.

## Before you begin

1. Read [STATUS_LABELS.md](STATUS_LABELS.md) — understand what VALIDATED means
2. Read [DISCLAIMER.md](DISCLAIMER.md) — understand the scope of this project
3. Pull the current version of the file from the repository
4. Retrieve the full text of every statute cited in `source_statutes` from the official state legislature website or LDH (Legal Data Hunter)

## The checklist

Sign off on each item before submitting a validation statement.

### Completeness
- [ ] All notice types available in this jurisdiction are represented (no significant omissions)
- [ ] Major population centers with local overlays are identified in `local_overlays`
- [ ] Affirmative defenses list covers the most common and significant defenses

### Accuracy — notice periods
- [ ] Notice period for nonpayment of rent is correct as of the `last_updated` date
- [ ] The day-counting method is correct (calendar days / business days / excludes weekends-holidays)
- [ ] Notice periods for curable lease violations are correct
- [ ] Notice periods for no-fault termination are correct (by tenancy length if applicable)

### Accuracy — defect rules
- [ ] All defect triggers in `notice_defects` accurately reflect current law
- [ ] Defect results (INVALID / POTENTIALLY_INVALID / VOIDABLE) correctly characterize consequences
- [ ] Statute citations in each defect rule have been verified against actual statutory text
- [ ] Case law interpretation (not just statutory text) has been considered for any disputed defects

### Accuracy — service requirements
- [ ] Service methods in `service_methods` are complete and correctly prioritized
- [ ] Days added for each service method are correct
- [ ] Any state-specific service requirements not captured in the standard template have been added

### Just cause and rent control
- [ ] `just_cause_required` correctly reflects current statewide law
- [ ] If `just_cause_required: true`, qualifying reasons are complete
- [ ] `statewide_rent_control` correctly reflects current law
- [ ] Any local rent control or stabilization in major cities is reflected in `local_overlays`

### Drafter notes
- [ ] All items in `ai_drafter_notes` flagged for attorney review have been addressed
- [ ] Unresolved items have been annotated with the reviewer's determination

### Testing
- [ ] File has been tested against at least 3 real-world notice scenarios — output matches what an experienced tenant attorney would conclude
- [ ] Test scenarios are documented in `validation/golden_sets/{state}_golden_set.json`

### Final
- [ ] `last_updated` date reflects the date of this review
- [ ] `reviewer` field updated with your name and bar number
- [ ] `validation_status` updated to "VALIDATED"
- [ ] A brief validation statement has been submitted (open a PR with these changes)

## Submitting your review

Submit a pull request with:
1. The updated JSON file (status VALIDATED, reviewer populated, last_updated updated)
2. Your golden set test cases in `validation/golden_sets/`
3. A brief comment in the PR describing any significant changes made and any open issues identified

Your contribution is permanent, attributed, and deeply appreciated.

---

* REVIEWER_CHECKLIST.md v0.1 · June 2026*
