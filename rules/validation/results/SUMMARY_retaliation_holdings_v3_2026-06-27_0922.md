# Validation Summary — retaliation_holdings_v3
**Run ID:** track_b_ks_nv_ny_sc_20260627  
**Completed:** 2026-06-27 09:22 UTC  
**Elapsed:** 7.2 min  
**Raw output:** `/Users/andrewcohen/Documents/GitHub/a2j-ai/rules/validation/l2/output/retaliation_holdings_v3_2026-06-27_track_b_ks_nv_ny_sc_20260627.json`  
**PR list:** `/Users/andrewcohen/Documents/GitHub/a2j-ai/rules/validation/l2/output/retaliation_holdings_v3_PR_track_b_ks_nv_ny_sc_20260627.json`  
**Log:** `/Users/andrewcohen/Documents/GitHub/a2j-ai/rules/validation/logs/retaliation_holdings_v3_20260627_0915.log`  

## Rates — TWO rates, never one blended number

**Method rate** (text-retrievable cases only):  MV ÷ (MV+CI+RC) = 5 ÷ 6 = **83%**
**Overall rate** (all cases, retrieval-gated):  MV ÷ all = 5 ÷ 10 = **50%**

*The gap between method rate and overall rate is the CourtListener retrieval bottleneck (PR cases), not a limitation of the verification method.*

## Bucket Counts

| Bucket | Count | % of total | Meaning |
|--------|-------|------------|---------|
| MV — machine-verified | 5 | 50% | Two-model corroborated; below attorney line |
| CI — confirm-inference | 1 | 10% | Corroborated; D=INFERRED; cheap confirm lane |
| RC — re-characterize | 0 | 0% | Text retrieved; holding failed → attorney |
| PR — pending-retrieval | 1 | 10% | No usable text from CL; retrieval retry only |
| SM — single-model-preliminary | 0 | 0% | Only one model answered; not machine-verified |
| Other (failure/unknown) | 3 | 30% | See raw output |

## Provenance

- machine-verified is BELOW the attorney line. Nothing here is `validated`.
- Per-case generate_model + verify_model recorded in raw output JSON.
- SM count: 0. If SM > 0, those cases inflated no rate (harness enforces this).

## Attorney Queues

- **RC (re-characterize):** 0 cases — source-generated holding → attorney review
- **CI (confirm-inference):** 1 cases — cheap delegable confirms
- **PR (pending-retrieval):** 1 cases — retrieval retry only, NOT attorney lane

## RC Cases (What Needs Attorney Review)

- None.

## SM Cases (Single-Model — Flag for Investigation)

- None.
