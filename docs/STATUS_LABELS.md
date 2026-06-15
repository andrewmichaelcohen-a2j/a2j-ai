# Status Labels

Every file in this library carries a `validation_status` field. The meaning of each label is defined here and is binding.

Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.

---

| Status | Meaning | Permitted use |
|--------|---------|---------------|
| **DRAFT** | AI-generated; automated validation checks not yet complete | Development and inspection only — **NOT for advising real people**. |
| **AUTOMATED-CHECKS-PASSED** | All six automated validation layers (L1–L6) passed; not yet attorney-reviewed | Development and internal testing only — **NOT for advising real people**. Marks readiness for attorney review queue. |
| **UNDER REVIEW** | Assigned to a named attorney reviewer; review in progress | Testing only — not for deployment |
| **VALIDATED** | Reviewed and signed by 1 licensed attorney in the relevant jurisdiction; all automated layers passed | Attorney-supervised deployments only (attorney reviews all output before acting) |
| **CERTIFIED** | Two independent licensed attorney reviewers; advisory board approved; annual re-verification schedule in place | Direct-to-public deployments with appropriate AI guardrails |
| **NEEDS UPDATE** | A cited statute has been amended or repealed, or validation has expired (>12 months since last verification) | Suspended — do not use until updated and re-validated |

## Advancement rules

- **DRAFT → AUTOMATED-CHECKS-PASSED**: An automated process may advance a file when all six validation layers (L1 statutory grounding, L2 multi-model consensus, L3 internal consistency, L4 golden-set tests, L5 cross-jurisdiction anomaly check, L6 temporal freshness) pass with no errors. Warnings must be documented but do not block advancement.
- **AUTOMATED-CHECKS-PASSED → UNDER REVIEW**: A file may advance only when a named licensed attorney in the relevant jurisdiction agrees to review it.
- **UNDER REVIEW → VALIDATED**: A file may advance only when the reviewing attorney completes the [REVIEWER_CHECKLIST.md](REVIEWER_CHECKLIST.md) and submits a signed validation statement.
- **VALIDATED → CERTIFIED**: A file may advance only after a second independent licensed attorney review and advisory board approval.
- **No automated process may advance a file beyond AUTOMATED-CHECKS-PASSED.** Only a named human attorney can do this.
- A file automatically reverts to **NEEDS UPDATE** when its cited statutes change, as detected by Layer 6 monitoring.

## Why this matters

The status label is the difference between a research artifact and a tool that could harm a real person. A tenant who acts on incorrect legal information could waive a valid defense, miss a deadline, or face wrongful eviction. The status system exists to make that risk transparent and manageable — not to discourage use, but to ensure appropriate oversight at each stage.
