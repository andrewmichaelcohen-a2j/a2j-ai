# Status Labels

Every file in this library carries a `validation_status` field. The meaning of each label is defined here and is binding.

Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.

---

| Status | Meaning | Permitted use |
|--------|---------|---------------|
| **DRAFT** | AI-generated; not attorney-reviewed | Development and inspection only — **NOT for advising real people**. All files in this release are DRAFT. |
| **UNDER REVIEW** | Assigned to a named attorney reviewer; review in progress | Testing only — not for deployment |
| **VALIDATED** | Reviewed and signed by 1 licensed attorney in the relevant jurisdiction; all automated layers passed | Attorney-supervised deployments only (attorney reviews all output before acting) |
| **CERTIFIED** | Two independent licensed attorney reviewers; advisory board approved; annual re-verification schedule in place | Direct-to-public deployments with appropriate AI guardrails |
| **NEEDS UPDATE** | A cited statute has been amended or repealed, or validation has expired (>12 months since last verification) | Suspended — do not use until updated and re-validated |

## Advancement rules

- A file may advance from DRAFT to UNDER REVIEW only when a named attorney agrees to review it.
- A file may advance from UNDER REVIEW to VALIDATED only when the reviewing attorney completes the [REVIEWER_CHECKLIST.md](REVIEWER_CHECKLIST.md) and submits a signed validation statement.
- A file may advance to CERTIFIED only after a second independent review and advisory board approval.
- **No automated process may advance a file beyond DRAFT.** Only a named human attorney can do this.
- A file automatically reverts to NEEDS UPDATE when its cited statutes change, as detected by Layer 6 monitoring.

## Why this matters

The status label is the difference between a research artifact and a tool that could harm a real person. A tenant who acts on incorrect legal information could waive a valid defense, miss a deadline, or face wrongful eviction. The status system exists to make that risk transparent and manageable — not to discourage use, but to ensure appropriate oversight at each stage.
