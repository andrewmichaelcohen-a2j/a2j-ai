# Status Labels & Advancement Rules

**Civil Justice as Code · a2j-ai repo · v2 — June 15, 2026**

Governs how every rules file (and every module within it) is labeled and advanced. This file is authoritative; `validate.py` and the schema enforce it in code.

*Read with:* `PROJECT_PLAN.md` (the map) and `PROJECT_STATE_OF_RECORD.md` (the dashboard). The advancement guardrail here is the project's core credibility discipline — drafted, automatically checked, and attorney-validated are three different states, and nothing is ever presented as more validated than it is.

Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.

---

## The ladder

```
DRAFT → AUTOMATED-CHECKS-PASSED → UNDER REVIEW → VALIDATED → CERTIFIED
                                          ↑
                             guardrail line: no automated process
                             may cross this line — only a named attorney
```

Plus one off-ladder state:

| Status | Meaning | How triggered |
|--------|---------|---------------|
| **NEEDS UPDATE** | A cited statute changed (detected by Layer 6). The file's accuracy can no longer be assumed. | automated (L6) |

---

## Module-level granularity

Status is tracked **per module**, not just per file. A file's modules — `notice`, `service`, `overlays`, `substantive_defenses`, `procedural_defects` — each carry their own status. This matches how validation actually proceeds: notice validity (bright-line) clears the automated layers and reaches attorney review long before substantive defenses (open-textured) do.

**File status is derived, not set directly:**

> `file_status = the minimum status across all of the file's modules.`

A file is only as validated as its least-validated module. A file whose `notice` module is VALIDATED but whose `substantive_defenses` module is still DRAFT has `file_status = DRAFT`. This makes overclaiming structurally impossible: the file-level label can never outrun the weakest module.

Each module records, in the schema's `validation.module_status`:
- its current status
- the reviewer of record (or `null`)
- `reviewed_date` (or `null`)
- `coverage_level` — which layers were applied (e.g., `"L1,L3,L5"`)

Each file records, in `validation.automated_layers`, the per-layer result (`pass` / `fail` / `warning` / `not_implemented` / `not_run`).

---

## Advancement rules

### DRAFT → AUTOMATED-CHECKS-PASSED *(automated; Option A — "all implemented layers")*

An automated process may advance a module when all **currently-implemented** validation layers pass with no errors. The six layers are: L1 statutory grounding · L2 multi-model consensus · L3 internal consistency · L4 golden-set tests · L5 cross-jurisdiction anomaly check · L6 temporal freshness.

- Advancement requires passing every layer that is **currently operational**. Layers that are not yet implemented are recorded as `not_implemented` and do not block advancement.
- The module's metadata records its **coverage level** — which layers were applied and which are not yet operational. The label always means "passed everything we can currently check," never "passed all six" unless all six are in fact operational.
- Warnings must be documented (in `validation.flags`) but do not block advancement.
- **Re-run on expansion:** as additional layers come online, all AUTOMATED-CHECKS-PASSED modules are re-run against the newly-operational layer. A module that fails the new layer reverts to DRAFT.

*(Today's operational layers: L1, L3, L5. L2, L4, L6 are scaffolded and recorded as `not_implemented`. A module passing L1/L3/L5 today is AUTOMATED-CHECKS-PASSED at coverage level `"L1,L3,L5"`.)*

### AUTOMATED-CHECKS-PASSED → UNDER REVIEW *(named attorney only)*

A module may advance only when a named, licensed attorney in the relevant jurisdiction agrees to review it. No automated process may make this move.

### UNDER REVIEW → VALIDATED *(named attorney only)*

A module may advance only when the reviewing attorney completes `REVIEWER_CHECKLIST.md` and submits a signed validation statement. The reviewer of record is named in the module's metadata.

### VALIDATED → CERTIFIED *(advisory board only)*

A module may advance only after a second independent licensed-attorney review and advisory-board approval. *(The advisory board is to be constituted at the stewardship phase; until then, CERTIFIED is defined but unreachable, by design.)*

---

## The guardrail *(enforced in validate.py)*

**No automated process may advance any module beyond AUTOMATED-CHECKS-PASSED.** UNDER REVIEW, VALIDATED, and CERTIFIED require a named human reviewer. A status at these levels with `reviewer = null` is invalid and must fail validation.

`validate.py` enforces three things in code:

1. The no-auto-advance rule above.
2. `file_status = min(module_status)`.
3. AUTOMATED-CHECKS-PASSED requires all implemented layers green; warnings allowed, errors not.

---

## NEEDS UPDATE — entry and re-entry

**Entry:** Layer 6 monitors every cited statute. When a citation changes, the affected module is flagged NEEDS UPDATE automatically, regardless of its prior status.

**Re-entry path:**

- A NEEDS UPDATE module re-enters the ladder at DRAFT and must re-clear the automated layers from the bottom.
- If it had been VALIDATED or CERTIFIED, the reviewer of record (and, for CERTIFIED, the advisory board) is notified, and the prior human status is **suspended** pending re-review — not silently retained. A statute change must never leave a file labeled VALIDATED on superseded law; stale-but-VALIDATED is the one state an A2J tool must never present.
- The file's `file_status` recomputes as the minimum across modules, so a single NEEDS UPDATE module pulls the whole file's status down until resolved.

---

## The precise external claim

> "50 states drafted; all 50 pass the automated checks currently implemented (L1/L3/L5), with coverage recorded per file; the flagship state and a stratified sample are attorney-VALIDATED, with a measured error rate on the validated set."

Never "we validated a 50-state library" when what exists is automated-only. To a lawyer those are different claims; conflating them is the overclaim that loses a sophisticated audience.

---

*Status Labels v2 · June 15, 2026 · Authoritative. Enforced by `validate.py` and the `eviction-v2` schema. Maintained in the repo; update with care — this is the project's core credibility discipline.*
