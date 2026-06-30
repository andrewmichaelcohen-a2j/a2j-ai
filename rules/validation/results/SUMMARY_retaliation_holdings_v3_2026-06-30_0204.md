# Validation Summary — retaliation_holdings_v3
**Run ID:** pr_retry_co_ny_sc_20260629  
**Completed:** 2026-06-30 02:04 UTC  
**Elapsed:** 47.9 min  
**Raw output:** `/Users/andrewcohen/Documents/GitHub/a2j-ai/rules/validation/l2/output/retaliation_holdings_v3_2026-06-30_pr_retry_co_ny_sc_20260629.json`  
**PR list:** `/Users/andrewcohen/Documents/GitHub/a2j-ai/rules/validation/l2/output/retaliation_holdings_v3_PR_pr_retry_co_ny_sc_20260629.json`  
**Log:** `/Users/andrewcohen/Documents/GitHub/a2j-ai/rules/validation/logs/retaliation_holdings_v3_20260630_0116.log`  

## Rates — TWO rates, never one blended number

**Method rate** (text-retrievable cases only):  MV ÷ (MV+CI+RC) = 3 ÷ 4 = **75%**
**Overall rate** (all cases, retrieval-gated):  MV ÷ all = 3 ÷ 13 = **23%**

*The gap between method rate and overall rate is the CourtListener retrieval bottleneck (PR cases), not a limitation of the verification method.*

## Bucket Counts

| Bucket | Count | % of total | Meaning |
|--------|-------|------------|---------|
| MV — machine-verified | 3 | 23% | Two-model corroborated; below attorney line |
| CI — confirm-inference | 1 | 8% | Corroborated; D=INFERRED; cheap confirm lane |
| RC — re-characterize | 0 | 0% | Text retrieved; holding failed → attorney |
| PR — pending-retrieval | 8 | 62% | No usable text from CL; retrieval retry only |
| SM — single-model-preliminary | 0 | 0% | Only one model answered; not machine-verified |
| Other (failure/unknown) | 1 | 8% | See raw output |

## Provenance

- machine-verified is BELOW the attorney line. Nothing here is `validated`.
- Per-case generate_model + verify_model recorded in raw output JSON.
- SM count: 0. If SM > 0, those cases inflated no rate (harness enforces this).

## Attorney Queues

- **RC (re-characterize):** 0 cases — source-generated holding → attorney review
- **CI (confirm-inference):** 1 cases — cheap delegable confirms
- **PR (pending-retrieval):** 8 cases — retrieval retry only, NOT attorney lane

## RC Cases (What Needs Attorney Review)

- None.

## SM Cases (Single-Model — Flag for Investigation)

- None.
