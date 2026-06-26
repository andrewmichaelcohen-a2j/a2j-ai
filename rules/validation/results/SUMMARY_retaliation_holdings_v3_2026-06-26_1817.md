# Validation Summary — retaliation_holdings_v3
**Run ID:** nc17_fresh_v2  
**Completed:** 2026-06-26 18:17 UTC  
**Elapsed:** 796.9 min  
**Raw output:** `/Users/andrewcohen/Documents/GitHub/a2j-ai/rules/validation/l2/output/retaliation_holdings_v3_2026-06-26_nc17_fresh_v2.json`  
**PR list:** `/Users/andrewcohen/Documents/GitHub/a2j-ai/rules/validation/l2/output/retaliation_holdings_v3_PR_nc17_fresh_v2.json`  
**Log:** `/Users/andrewcohen/Documents/GitHub/a2j-ai/rules/validation/logs/retaliation_holdings_v3_20260626_0500.log`  

## Rates — TWO rates, never one blended number

**Method rate** (text-retrievable cases only):  MV ÷ (MV+CI+RC) = 6 ÷ 9 = **67%**
**Overall rate** (all cases, retrieval-gated):  MV ÷ all = 6 ÷ 118 = **5%**

*The gap between method rate and overall rate is the CourtListener retrieval bottleneck (PR cases), not a limitation of the verification method.*

## Bucket Counts

| Bucket | Count | % of total | Meaning |
|--------|-------|------------|---------|
| MV — machine-verified | 6 | 5% | Two-model corroborated; below attorney line |
| CI — confirm-inference | 0 | 0% | Corroborated; D=INFERRED; cheap confirm lane |
| RC — re-characterize | 3 | 3% | Text retrieved; holding failed → attorney |
| PR — pending-retrieval | 25 | 21% | No usable text from CL; retrieval retry only |
| SM — single-model-preliminary | 0 | 0% | Only one model answered; not machine-verified |
| Other (failure/unknown) | 84 | 71% | See raw output |

## Provenance

- machine-verified is BELOW the attorney line. Nothing here is `validated`.
- Per-case generate_model + verify_model recorded in raw output JSON.
- SM count: 0. If SM > 0, those cases inflated no rate (harness enforces this).

## Attorney Queues

- **RC (re-characterize):** 3 cases — source-generated holding → attorney review
- **CI (confirm-inference):** 0 cases — cheap delegable confirms
- **PR (pending-retrieval):** 25 cases — retrieval retry only, NOT attorney lane

## RC Cases (What Needs Attorney Review)

- **DeNardo v. Maassen** (AK): RC: text retrieved, holding failed verification. Flagged: C=FLAG-verify-disputed, D=FLAG. Source-generated holding → attorney.
- **Sladek v. dePlomb** (CO): RC: text retrieved, holding failed verification. Flagged: C=FLAG-generate-failed, D=FLAG. Source-generated holding → attorney.
- **TOV Realty, LLC v. Suarez** (CT): RC: text retrieved, holding failed verification. Flagged: C=FLAG-generate-failed, D=FLAG. Source-generated holding → attorney.

## SM Cases (Single-Model — Flag for Investigation)

- None.
