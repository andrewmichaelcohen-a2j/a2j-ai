# Validation Summary — retaliation_holdings_v3
**Run ID:** 9ae49b97  
**Completed:** 2026-07-09 15:38 UTC  
**Elapsed:** 343.4 min  
**Raw output:** `/Users/andrewcohen/Documents/GitHub/a2j-ai/rules/validation/l2/output/retaliation_holdings_v3_2026-07-09_9ae49b97.json`  
**PR list:** `/Users/andrewcohen/Documents/GitHub/a2j-ai/rules/validation/l2/output/retaliation_holdings_v3_PR_9ae49b97.json`  
**Log:** `/Users/andrewcohen/Documents/GitHub/a2j-ai/rules/validation/logs/retaliation_holdings_v3_20260709_0954.log`  

## Rates — TWO rates, never one blended number

**Method rate** (text-retrievable cases only):  MV ÷ (MV+CI+RC) = 0 ÷ 0 = **n/a**
**Overall rate** (all cases, retrieval-gated):  MV ÷ all = 0 ÷ 5 = **0%**

*The gap between method rate and overall rate is the CourtListener retrieval bottleneck (PR cases), not a limitation of the verification method.*

## Bucket Counts

| Bucket | Count | % of total | Meaning |
|--------|-------|------------|---------|
| MV — machine-verified | 0 | 0% | Two-model corroborated; below attorney line |
| CI — confirm-inference | 0 | 0% | Corroborated; D=INFERRED; cheap confirm lane |
| RC — re-characterize | 0 | 0% | Text retrieved; holding failed → attorney |
| PR — pending-retrieval | 5 | 100% | No usable text from CL; retrieval retry only |
| SM — single-model-preliminary | 0 | 0% | Only one model answered; not machine-verified |
| Other (failure/unknown) | 0 | 0% | See raw output |

## Provenance

- machine-verified is BELOW the attorney line. Nothing here is `validated`.
- Per-case generate_model + verify_model recorded in raw output JSON.
- SM count: 0. If SM > 0, those cases inflated no rate (harness enforces this).

## Attorney Queues

- **RC (re-characterize):** 0 cases — source-generated holding → attorney review
- **CI (confirm-inference):** 0 cases — cheap delegable confirms
- **PR (pending-retrieval):** 5 cases — retrieval retry only, NOT attorney lane

## RC Cases (What Needs Attorney Review)

- None.

## SM Cases (Single-Model — Flag for Investigation)

- None.
