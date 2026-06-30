# Validation Summary — retaliation_holdings_v3
**Run ID:** broad_query_10states_20260629  
**Completed:** 2026-06-30 03:21 UTC  
**Elapsed:** 119.9 min  
**Raw output:** `/Users/andrewcohen/Documents/GitHub/a2j-ai/rules/validation/l2/output/retaliation_holdings_v3_2026-06-30_broad_query_10states_20260629.json`  
**PR list:** `/Users/andrewcohen/Documents/GitHub/a2j-ai/rules/validation/l2/output/retaliation_holdings_v3_PR_broad_query_10states_20260629.json`  
**Log:** `/Users/andrewcohen/Documents/GitHub/a2j-ai/rules/validation/logs/retaliation_holdings_v3_20260630_0121.log`  

## Rates — TWO rates, never one blended number

**Method rate** (text-retrievable cases only):  MV ÷ (MV+CI+RC) = 12 ÷ 14 = **86%**
**Overall rate** (all cases, retrieval-gated):  MV ÷ all = 12 ÷ 35 = **34%**

*The gap between method rate and overall rate is the CourtListener retrieval bottleneck (PR cases), not a limitation of the verification method.*

## Bucket Counts

| Bucket | Count | % of total | Meaning |
|--------|-------|------------|---------|
| MV — machine-verified | 12 | 34% | Two-model corroborated; below attorney line |
| CI — confirm-inference | 1 | 3% | Corroborated; D=INFERRED; cheap confirm lane |
| RC — re-characterize | 1 | 3% | Text retrieved; holding failed → attorney |
| PR — pending-retrieval | 20 | 57% | No usable text from CL; retrieval retry only |
| SM — single-model-preliminary | 0 | 0% | Only one model answered; not machine-verified |
| Other (failure/unknown) | 1 | 3% | See raw output |

## Provenance

- machine-verified is BELOW the attorney line. Nothing here is `validated`.
- Per-case generate_model + verify_model recorded in raw output JSON.
- SM count: 0. If SM > 0, those cases inflated no rate (harness enforces this).

## Attorney Queues

- **RC (re-characterize):** 1 cases — source-generated holding → attorney review
- **CI (confirm-inference):** 1 cases — cheap delegable confirms
- **PR (pending-retrieval):** 20 cases — retrieval retry only, NOT attorney lane

## RC Cases (What Needs Attorney Review)

- **Criss v. Salvation Army Residences** (WV): RC: text retrieved, holding failed verification. Flagged: C=FLAG-verify-disputed, D=FLAG. Source-generated holding → attorney.

## SM Cases (Single-Model — Flag for Investigation)

- None.
