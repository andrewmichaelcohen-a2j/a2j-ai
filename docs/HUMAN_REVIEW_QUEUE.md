# Human Review Queue — Civil Justice as Code

**Module:** Notice / pay_or_quit · **Layer:** L2 Multi-Model Consensus  
**Runner rule:** Runners append new flagged items only. They never edit or overwrite the Resolution, Authoritative source, Resolved by, Date, or Status fields — those are owned by Andy Cohen.  
**Last rebuilt:** 2026-06-18 (post-straggler-retry cleanup; GA straggler result: genuine L7) · **Confirmed by:** Andy Cohen

> **How to use this queue:**  
> Work top-to-bottom. L7-ESCALATED = you decide from primary sources. PENDING-CONFIRMATION = you verify the AI's proposed answer and sign off (or override).  
> Fill in the Resolution and Confirmed-by fields. Move completed items to the Resolved section at the bottom.

---

## Queue Summary

| Status | Count |
|--------|-------|
| 🔴 L7-ESCALATED — you decide from primary sources | 5 |
| 🟡 PENDING-CONFIRMATION — AI proposed, you verify | 5 |
| 🟡 CITATION-REVIEW — verify operative section from primary source | 3 |
| ✅ Resolved/Confirmed | 0 |

*Technical resolutions (states confirmed by both models with no legal question — 39 states total): AK, AL, AR, AZ, CA, CO, CT, DC, FL, HI, IA, ID, IL (citation confirmed), IN, KS, KY, LA, MA, ME (citation confirmed), MI, MN, MS (AI-resolved), MT, NC, NE, NH, NJ, NM, NY, OH (AI-resolved), OK, OR, PA, RI, SC, TN, TX, UT, VT, WA, WI, WY — no human review needed.*

---

## 🔴 L7-ESCALATED — Attorney Review Required

These items could not be resolved by AI. Both models gave clean answers but genuinely disagree on a legal question. Attorney review of primary sources required before any content change.

---

### [MO-L7-01] Missouri — Is §535.020 demand a notice requirement or a precondition?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Run date:** 2026-06-18 (Phase 1 reasoning pass)

**Question:** Is Missouri's §535.020 demand-for-rent requirement a formal *notice requirement* (notice_required=true) before filing eviction, or only a *precondition to filing* that does not constitute a notice period (notice_required=false)?

**L2 result — models disagree on characterization, agree on statute:**
- GPT (gpt-5.5): notice_required=false, days=null, statute §535.020.1 — "§535.020 requires demand for rent but specifies no waiting period. A landlord may file immediately after demand is refused."
- Gemini (gemini-2.5-pro): notice_required=true, days=null, statute §535.020 — "§535.020 requires a demand for payment of rent before filing, making it effectively a notice precondition."

Both models agree §535.060 (original file citation, 10d) is wrong. Both agree §535.020 is operative. They disagree only on whether the demand constitutes a "notice requirement" or a "condition precedent."

**Current file:** notice_required=true, days=10, statute §535.060 *(both are almost certainly wrong — §535.060 is wrong regardless)*  
**Your task:** Determine whether §535.020 makes notice_required=true or false; confirm days=null; confirm statute=§535.020.

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

### [ND-L7-02] North Dakota — Is §47-32-02's 3-day period a formal notice or a ripening period?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Run date:** 2026-06-18 (Phase 1 model-split)

**Question:** Under NDCC §47-32-02, is the 3-day period a *formal notice-to-quit requirement* (notice_required=true, days=3) or a *ripening period* (landlord may file after 3 days without serving notice; notice_required=false)?

**L2 result — both cite §47-32-02 but reach opposite conclusions:**
- GPT: notice_required=true, days=3 — "§47-32-02 requires landlord to give tenant a 3-day written notice to pay or quit before filing."
- Gemini: notice_required=false, days=null — "§47-32-02 establishes that a landlord may bring an eviction action when rent is unpaid; the 3-day period is a ripening period before the landlord can file, not a notice requirement."

Both agree §47-16-15 (original file citation) is wrong. Dispute is purely textual: does §47-32-02 require *service* of a notice, or merely set a waiting period?

**Current file:** notice_required=true, days=3, statute NDCC §47-16-15 *(citation almost certainly wrong regardless)*  
**Your task:** Read §47-32-02; determine notice_required and operative period; confirm correct citation.

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

### [MD-L7-03] Maryland — Does §8-401 require pre-filing notice or not?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Run date:** 2026-06-18 (Phase 2 genuine model-split)

**Question:** Under Md. Code Real Prop. §8-401, must a residential landlord give a tenant written notice before filing a complaint for summary ejectment (failure to pay rent), and if so, how many days?

**L2 result — same statute, opposite conclusions:**
- GPT: notice_required=true, days=10, statute §8-401(b)(2)(i) — "For a residential tenancy, the landlord must provide the tenant a written notice of intent to file a complaint for summary ejectment at least 10 days before filing."
- Gemini: notice_required=false, days=null, statute §8-401 — "The statute does not mandate a notice period before filing an action for nonpayment of rent. A landlord may file a written complaint with the District Court directly."

**Current file:** notice_required=true, days=10, statute Md. Code Real Prop. §8-401  
**Your task:** Read §8-401; determine whether advance notice is required before filing and if so, how many days.

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

### [VA-L7-04] Virginia — Is the notice period 5 days or 14 days under §55.1-1245(F)?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Run date:** 2026-06-18 (Phase 2 retry genuine model-split)

**Question:** Under Va. Code §55.1-1245(F), how many days notice must a landlord give a tenant before filing for eviction for nonpayment of rent — 5 days or 14 days?

**L2 result — same statute, different periods:**
- GPT: notice_required=true, days=5, statute Va. Code § 55.1-1245(F)
- Gemini: notice_required=true, days=14, statute Va. Code Ann. § 55.1-1245(F)

Note: The discrepancy may reflect different tenancy types (month-to-month vs. week-to-week) or a 2019-era amendment. Both models cite the same section; the period dispute is likely fact-specific or context-dependent.

**Current file:** notice_required=true, days=5, statute Va. Code §55.1-1245  
**Your task:** Read §55.1-1245(F); determine the correct notice period for a standard residential nonpayment notice. Note any tenancy-type-dependent variations.

**Resolution:** _ Both are determined to be correct - the current notice period is 5 days under Va. Code § 55.1-1245(F); however, effective, July 1, 2026, under §55.1-1245(F); amendment = HB 15/SB 48 (2026), the new notice period will be 14 days. _______________  
**Authoritative source:** __VA Code and VA Legislative Information System (LIS)______________  
**Resolved by:** __Andrew Cohen______________  **Date:** ___June 19, 2026_____________

---

### [GA-L7-05] Georgia — Does §44-7-50 require formal notice before filing, or can landlord file immediately?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Run date:** 2026-06-18 (straggler retry — clean neutral query, 8000-token GPT budget)

**Question:** Under O.C.G.A. §44-7-50, both L2 models agree a demand for possession is required before filing. The unresolved question: after making the demand, must the landlord wait a minimum number of days before filing (GPT: 3 days), or may the landlord file immediately after demand is refused (Gemini: no waiting period)?

**L2 result — two clean neutral runs; models agree notice is required but disagree on waiting period:**
- GPT (gpt-5.5): notice_required=True, days=3, statute=O.C.G.A. § 44-7-50(a),(b) — "§44-7-50(a) requires the landlord to demand possession before filing a dispossessory affidavit."
- Gemini (gemini-2.5-pro): notice_required=True, days=None, statute=O.C.G.A. § 44-7-50 — "Georgia law requires a landlord to first make a demand for possession. This demand is a prerequisite to filing — but no statutory waiting period is specified."

The legal question is therefore narrower than the initial flag suggested: **both models agree a demand/notice is required before filing.** The dispute is whether §44-7-50 also imposes a mandatory waiting period (GPT: 3 days; Gemini: demand required but no waiting period — file immediately after demand refused).

Note: This straggler was run three times. The reasoning pass (first run) was a framing artifact. Two subsequent clean neutral runs (17:12 UTC and 17:44 UTC) both produced the same result: notice_required=True on both models; days split (3 vs None).

**Current file:** notice_required=True, days=3, statute=O.C.G.A. §44-7-50  
**Your task:** Read §44-7-50; determine whether a formal written demand/notice is required before filing and whether any waiting period applies.

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

## 🟡 PENDING-CONFIRMATION — AI Proposed, You Verify

The AI has proposed and applied a correction. File content updated; status stays at ACP. Your job: verify the proposed answer is correct and sign off (or override).

---

### [WV-PC-01] West Virginia — Confirm notice_required=false, §55-3A-1

**Classification:** PENDING-CONFIRMATION · **Status:** 🟡 pending  
**AI proposed:** notice_required=false, days=null, statute W. Va. Code §55-3A-1  
**Prior file claim:** notice_required=true, days=5, statute §37-6-5

**Question to confirm:** Is it correct that West Virginia landlords may file a summary eviction action for nonpayment *without prior notice* to the tenant, under §55-3A-1?

**GPT reasoning:** "W. Va. Code §55-3A-1 governs summary eviction and allows a landlord to petition for immediate relief when a tenant is in arrears of rent without any prior notice period requirement. §37-6-5 addresses notice to quit for periodic tenancies, not the nonpayment eviction action itself."  
**Gemini reasoning:** "§55-3A-1 is the summary eviction statute for nonpayment and permits filing without prior notice. §37-6-5 applies to termination of periodic tenancies, a separate situation."

**Your review:** __confirm notice_required=false, days=null______________  
**Confirmed by:** _Andrew Cohen_______________  **Date:** ___June 19, 2026_____________
Note: 2 different WV Code provisions that are adjacent but do not contain applicable notice periods: §37-6-5 governs periodic-tenancy termination; and §37-6-23 requires service and tenant can pay before trial.

---

### [OH-PC-02] Ohio — Confirm §1923.04(A), 3 days

**Classification:** PENDING-CONFIRMATION · **Status:** 🟡 pending  
**AI proposed:** statute ORC §1923.04(A), days=3 (period unchanged)  
**Prior file statute:** §1923.02; §5321.17 (citation only — period was correct)

**Question to confirm:** Is ORC §1923.04(A) the operative pre-filing notice provision for nonpayment evictions in Ohio (3-day notice to quit)?

**Reasoning:** §1923.04(A) states a party desiring to commence an FED action "shall notify the adverse party to leave the premises three or more days before beginning the action." Both GPT and Gemini independently identified §1923.04(A). Verified from codes.ohio.gov.

**Your review:** __Confirmed______________  
**Confirmed by:** Andrew Cohen________________  **Date:** _June 19, 2026_______________
Note: statutory language is "3 or more days"; and different notice periods may apply in narrow adjacent circumstances (termination of lease; deceased tenant in a rented mobile home). 
---

### [MS-PC-03] Mississippi — Confirm §89-8-13(5)(a), 3 days

**Classification:** PENDING-CONFIRMATION · **Status:** 🟡 pending  
**AI proposed:** statute §89-8-13(5)(a), days=3 (period unchanged)  
**Prior file statute:** §89-7-27

**Question to confirm:** Is Miss. Code Ann. §89-8-13(5)(a) (RLTA, Chapter 8) the operative residential nonpayment notice provision — not §89-7-27 (Chapter 7, general/commercial tenancies)?

**Reasoning:** §89-7-27 is in Chapter 7, which explicitly excludes residential tenancies governed by Chapter 8 (RLTA). §89-8-13(5)(a) is the operative residential provision: landlord may give 3-day written notice.

**Your review:** __Confirmed______________  
**Confirmed by:** __Andrew Cohen______________  **Date:** _June 19, 2026_______________

---

### [DE-PC-04] Delaware — Confirm §5502(a), 5 days

**Classification:** PENDING-CONFIRMATION · **Status:** 🟡 pending  
**AI proposed:** statute 25 Del. C. §5502(a), days=5 (period unchanged)  
**Prior file statute:** 25 Del. C. §5501

**Question to confirm:** Is 25 Del. C. §5502(a) (not §5501) the operative nonpayment notice section for Delaware?

**Reasoning:** Both GPT and Gemini cited §5502(a) independently. §5501 is likely the general jurisdiction/applicability provision.

**Your review:** ____Confirmed____________  
**Confirmed by:** __Andrew Cohen______________  **Date:** __June 19, 2026______________

---

### [NV-PC-05] Nevada — Confirm 7-day period, §40.253(1)(a)

**Classification:** PENDING-CONFIRMATION · **Status:** 🟡 pending  
**AI proposed:** notice_required=true, days=7, statute NRS §40.253(1)(a)  
**Prior file:** notice_required=true, days=5, statute NRS §40.253

**Question to confirm:** Is the correct Nevada nonpayment notice period 7 days (not 5), under NRS §40.253(1)(a)?

**GPT confidence:** high · **Gemini confidence:** high

**Your review:** __Confirmed 7 (judicial) days, not 5 days - judicial days means that weekend days are not counted for purposes of the notice______________  
**Confirmed by:** __Andrew Cohen______________  **Date:** __June 19, 2026______________

---

## 🟡 CITATION-REVIEW — Verify Operative Section from Primary Source

---

### [SD-CR-01] South Dakota — Which section is operative: §21-16-1, §21-16-1(2), or §21-16-2?

**Classification:** CITATION-REVIEW · **Status:** 🟡 pending  
**Period:** 3 days (confirmed by both models)  
**Current file:** SDCL §21-16-1

**Question:** The 3-day period is confirmed. But models disagree on the specific section:
- GPT: SDCL §21-16-1(2)
- Gemini: SDCL §21-16-2 (separate section)
- L1 note: §21-16-1 is the grounds statute; subsection (4) covers nonpayment; §21-16-2 may be the notice provision

**Your task:** Check primary source; determine which section is the operative nonpayment *notice* provision (vs. the grounds-for-eviction statute).

**Resolution:** __Not confirmed. Here the proper statement of the current notice law in SD: there is a 3 day waiting period under section 21-16-1 (tenant must fail to pay rent for 3 days after it is due before cause of action triggers), but there is no express notice period for a notice to pay or quit, as section 21-16-2 was repealed by Senate bill 90 in 2024.______________  
**Authoritative source:** _Sdlegislature.gov/statutes/21-16_______________  
**Confirmed by:** _Andrew Cohen_______________  **Date:** ___June 19, 2026_____________

---

### [IL-CR-02] Illinois — Confirm 735 ILCS 5/9-209 (citation already correct in file)

**Classification:** CITATION-REVIEW · **Status:** 🟡 pending  
**Period:** 5 days (confirmed) · **Current file statute:** 735 ILCS 5/9-209 (already correct)

**Question:** Routine confirmation. Both models confirmed §9-209. File was already corrected from §9-207 (holdover/termination) to §9-209 (nonpayment). Verify §9-209 is the operative pay-or-quit provision.

**Your review:** __Confirmed______________  
**Confirmed by:** __Andrew Cohen______________  **Date:** ___June 19, 2026_____________

---

### [ME-CR-03] Maine — Confirm 14 M.R.S. §6002 (citation already correct in file)

**Classification:** CITATION-REVIEW · **Status:** 🟡 pending  
**Period:** 7 days (confirmed) · **Current file statute:** 14 M.R.S. §6002 (already correct)

**Question:** Routine confirmation. GPT cited §§6001, 6002(1-A)(D); Gemini cited §6002(1). Both confirm §6002 is operative (§6001 is the availability-of-remedy statute). File already has §6002. Verify.

**Your review:** __Confirmed______________  
**Confirmed by:** _Andrew Cohen_______________  **Date:** _June 19, 2026_______________
Note: there is a 7 day waiting period (tenant must be 7 days in arrears on the rent before landlord can serve the (7 day) notice. 

---

## ✅ Resolved Items

*Move entries here once confirmed or resolved, with the authoritative answer noted.*

---

## Technical Resolutions (No Human Review Required)

The following states resolved to CONSENSUS-CONFIRM via L2 multi-model consensus and require no attorney review. Documented here for audit trail.

| State | Period | Statute | Resolved by | Run |
|-------|--------|---------|-------------|-----|
| AK | 7d | AS §34.03.220(b) | L2 consensus | Phase 2 |
| AL | 7d | Ala. Code §35-9A-421(b) | L2 consensus | Phase 2 |
| AR | 3d | Ark. Code Ann. §18-60-304(a)(3) | L2 retry | Retry |
| AZ | 5d | A.R.S. §33-1368(B) | L2 consensus | Phase 2 |
| CA | 3d | CCP §1161(2) | L2 consensus | Phase 2 |
| CO | 10d | CRS §13-40-104(1)(d) | L2 consensus | Phase 2 |
| CT | 3d | CGS §47a-23(a) | L2 consensus | Phase 2 |
| DC | 30d | D.C. Code §42-3505.01(a-1) | L2 retry | Retry |
| FL | 3d | Fla. Stat. §83.56(3) | L2 consensus | Phase 2 |
| HI | 5d | HRS §521-68(a) | L2 consensus | Phase 2 |
| IA | 3d | Iowa Code §562A.27(2) | L2 retry | Retry |
| ID | 3d | Idaho Code §6-303(2) | L2 consensus | Phase 2 |
| IL | 5d | 735 ILCS 5/9-209 | L2 consensus (P1) | Phase 1 |
| IN | 10d | IC 32-31-1-6 | L2 consensus | Phase 2 |
| KS | 3d | KSA §58-2564(b) | L2 consensus | Phase 2 |
| KY | 7d | KRS §383.660(2) | L2 retry | Retry |
| LA | 5d | La. C.C.P. art. 4701 | L2 retry | Retry |
| MA | 14d | MGL c. 186 §11 | L2 retry | Retry |
| ME | 7d | 14 M.R.S. §6002 | L2 consensus (P1) | Phase 1 |
| MI | 7d | MCL §600.5714(1)(a) | L2 consensus | Phase 2 |
| MN | 14d | Minn. Stat. §504B.321 subd. 1a | L2 consensus | Phase 2 |
| MT | 3d | MCA §70-24-422(2) | L2 consensus | Phase 2 |
| NC | 10d | NC Gen Stat §42-3 | L2 consensus | Phase 2 |
| NE | 7d | Neb. Rev. Stat. §76-1431(2) | L2 consensus | Phase 2 |
| NH | 7d | RSA §540:3 | L2 consensus | Phase 2 |
| NJ | none | N.J.S.A. §2A:18-61.2 | L2 consensus + attorney (P1) | Phase 2 |
| NM | 3d | NMSA §47-8-33(D) | L2 consensus | Phase 2 |
| NY | 14d | RPAPL §711(2) | L2 consensus | Phase 2 |
| OK | 5d | 41 O.S. §131(B) | L2 consensus | Phase 2 |
| OR | 10d | ORS §90.394(2)(a) | L2 consensus | Phase 2 |
| PA | 10d | 68 P.S. §250.501(b) | L2 consensus | Phase 2 |
| RI | 5d | RI Gen Laws §34-18-35(b) | L2 consensus | Phase 2 |
| SC | 5d | SC Code §27-40-710(B) | L2 consensus | Phase 2 |
| SD | 3d | SDCL §21-16-1 (citation pending) | L2 consensus | Phase 1 |
| TN | 14d | TCA §66-28-505(b) | L2 retry + L5 attorney confirmation | Retry |
| TX | 3d | Tex. Prop. Code §24.005(a) | L2 consensus | Phase 2 |
| UT | 3d | Utah Code §78B-6-802(1)(c) | L2 consensus | Phase 2 |
| VT | 14d | 9 VSA §4467(b)(1) | L2 consensus | Phase 2 |
| WA | 14d | RCW §59.12.030(3) | L2 consensus | Phase 2 |
| WI | 5d | Wis. Stat. §704.17(1)(a) | L2 consensus | Phase 2 |
| WY | 3d | Wyo. Stat. §1-21-1002 | L2 consensus | Phase 2 |

---

*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*  
*Runner rule: Runners append new flagged items to the "Phase 2 Items" section only. Resolution, Authoritative source, Resolved by, Date, and Status fields are owned by Andy Cohen and must never be modified by automated runners.*  
*Status values: 🔴 pending (L7) · ⏳ retry pending · 🟡 pending (confirmation/citation) · ✅ confirmed · 🟢 resolved*

## Service L2 Items

*Service L2 run: 2026-06-20*

### [NV-SVC-01] NV (Nevada) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['NRS 40.280(1)(b)', 'NRS 40.280(1)(c)', 'NRS 40.280(1)(a)']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- personal: NRS 40.280(1)(a)
- substituted: NRS 40.280(1)(b)
- posting_and_mailing: NRS 40.280(1)(c)

**Gemini:**
- personal: NRS 40.280(1)(a)
- substituted: NRS 40.280(1)(b)
- posting_and_mailing: NRS 40.280(1)(c)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [TN-SVC-02] TN (Tennessee) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['TCA §66-28-505(a)(1)', 'TCA §66-28-505(a)(3)', 'TCA §66-28-505(a)(2)']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- personal: Tenn. Code Ann. § 66-28-107(d)(3)
- mail: Tenn. Code Ann. §§ 66-28-107(d)(3), 66-28-505(b)(1)

**Gemini:**
- personal: T.C.A. § 66-28-105(c)(3)
- mail: T.C.A. § 66-28-105(c)(3)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---



*Service L2 run: 2026-06-20*

### [DE-SVC-01] DE (Delaware) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['25 Del. C. §5104(c)', '25 Del. C. §5104(a)', '25 Del. C. §5104(b)']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- personal: 25 Del. C. § 5113(a)(1)
- substituted: 25 Del. C. § 5113(a)(2)
- mail: 25 Del. C. § 5113(a)(3); 25 Del. C. § 5113(b)

**Gemini:**
- personal: 25 Del. C. § 5113(a)
- substituted_and_mail: 25 Del. C. § 5113(a)
- posting_and_mail: 25 Del. C. § 5113(b)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [GA-SVC-02] GA (Georgia) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['OCGA §44-7-50; OCGA §9-11-4', 'OCGA §44-7-50']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- not_statutorily_specified: O.C.G.A. § 44-7-50(a)

**Gemini:**
- personal: O.C.G.A. § 44-7-50(a)
- substituted: O.C.G.A. § 44-7-50(a)
- mail: O.C.G.A. § 44-7-50(a)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [KS-SVC-03] KS (Kansas) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['KSA 58-2563; KSA 61-3804', 'KSA 58-2563']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- personal: K.S.A. 58-2564(b)
- substituted: K.S.A. 58-2564(b)
- mail: K.S.A. 58-2564(b)

**Gemini:**
- personal: K.S.A. 58-2510a(a)
- substituted: K.S.A. 58-2510a(b)
- mail: K.S.A. 58-2510a(c)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [LA-SVC-04] LA (Louisiana) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['La. C.C.P. art. 4702', 'La. C.C.P. art. 4703']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- personal: La. Code Civ. Proc. art. 4703(A)(1)
- substituted: La. Code Civ. Proc. art. 4703(A)(2)
- posting: La. Code Civ. Proc. art. 4703(A)(3)
- mail: La. Code Civ. Proc. art. 4703(A)(4); La. Code Civ. Proc. art. 4703(B)

**Gemini:**
- personal: La. Code Civ. Proc. Ann. art. 4703
- posting: La. Code Civ. Proc. Ann. art. 4703

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [ND-SVC-05] ND (North Dakota) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['NDCC 47-32-01', 'NDCC 47-32-01; 47-32-02']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- personal: N.D. Cent. Code § 47-16-17(1)
- substituted: N.D. Cent. Code § 47-16-17(2)
- posting_and_mail: N.D. Cent. Code § 47-16-17(3)

**Gemini:**
- personal: N.D.C.C. § 47-32-02
- substituted: N.D.C.C. § 47-32-02
- mail: N.D.C.C. § 47-32-02

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [NJ-SVC-06] NJ (New Jersey) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['NJSA 2A:18-53', 'NJSA 2A:18-53; R. 6:3-3']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- personal: N.J. Stat. Ann. § 2A:18-56
- substituted: N.J. Stat. Ann. § 2A:18-56
- mail: N.J. Stat. Ann. § 2A:18-56

**Gemini:**
- personal: N.J.S.A. 2A:18-61.2
- substituted: N.J.S.A. 2A:18-61.2
- mail: N.J.S.A. 2A:18-61.2

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [SD-SVC-07] SD (South Dakota) — 🟡 CITATION-DIVERGENCE

**Module:** service.method_rules  
**Status:** 🟡 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['SDCL 21-16-2']  
**File same-statute pattern:** True  

**Issue:** Models agree with each other but differ from file.

**GPT citations:**
- personal: S.D. Codified Laws § 21-16-2(1)
- substituted: S.D. Codified Laws § 21-16-2(2)
- posting_and_mailing: S.D. Codified Laws § 21-16-2(3)

**Gemini citations:**
- personal: SDCL 21-16-2
- substituted: SDCL 21-16-2
- posting_and_mail: SDCL 21-16-2

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---



*Service L2 run: 2026-06-20*

### [AR-SVC-01] AR (Arkansas) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['Ark. Code Ann. §18-60-301; §18-17-703', 'Ark. Code Ann. §18-17-703', 'Ark. Code Ann. §18-60-301']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- personal: Ark. Code Ann. § 18-17-105(c)(3)
- mail: Ark. Code Ann. § 18-17-105(c)(3)

**Gemini:**
- personal_or_substituted: A.C.A. § 18-60-304(d)(1)
- posting: A.C.A. § 18-60-304(d)(2)
- mail: A.C.A. § 18-60-304(d)(3)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [GA-SVC-02] GA (Georgia) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['OCGA §44-7-50', 'OCGA §44-7-50; OCGA §9-11-4']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- not_statutorily_specified: O.C.G.A. § 44-7-50(a)

**Gemini:**
- personal: O.C.G.A. § 44-7-50(a)
- substituted: None
- mail: O.C.G.A. § 44-7-50(a)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [NJ-SVC-03] NJ (New Jersey) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['NJSA 2A:18-53', 'NJSA 2A:18-53; R. 6:3-3']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**

**Gemini:**
- personal: N.J.S.A. 2A:18-61.2(a)
- substituted: N.J.S.A. 2A:18-61.2(a)
- mail: N.J.S.A. 2A:18-61.2(a)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---



*Service L2 run: 2026-06-20*

### [AK-SVC-01] AK (Alaska) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['AS 34.03.220', 'AS 34.03.220; AS 09.45.070']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- personal: Alaska Stat. § 09.45.100(a)(1)
- substituted: Alaska Stat. § 09.45.100(a)(2)
- mail: Alaska Stat. § 09.45.100(a)(3); Alaska Stat. § 09.45.100(b)

**Gemini:**
- personal: AS 34.03.310(b)
- mail: AS 34.03.310(b)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [AL-SVC-02] AL (Alabama) — 🟡 CITATION-DIVERGENCE

**Module:** service.method_rules  
**Status:** 🟡 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['Ala. Code §35-9A-301']  
**File same-statute pattern:** True  

**Issue:** Models agree with each other but differ from file.

**GPT citations:**
- personal: Ala. Code § 35-9A-141(c)(3); Ala. Code § 35-9A-421(b)
- substituted: Ala. Code § 35-9A-141(c)(1); Ala. Code § 35-9A-421(b)
- mail: Ala. Code § 35-9A-141(c)(3); Ala. Code § 35-9A-421(b)

**Gemini citations:**
- personal: Ala. Code § 35-9A-105(c)(3)
- substituted: Ala. Code § 35-9A-105(c)(3)
- mail: Ala. Code § 35-9A-105(c)(3)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [AZ-SVC-03] AZ (Arizona) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['ARS §33-1313(A)(1)', 'ARS §33-1313(A)(2)', 'ARS §33-1313(A)(3)']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- personal: A.R.S. § 33-1313(C)(3)
- mail: A.R.S. § 33-1313(C)(3); A.R.S. § 33-1313(D)

**Gemini:**
- personal: A.R.S. § 33-1313(B)
- mail: A.R.S. § 33-1313(B)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [CO-SVC-04] CO (Colorado) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['CRS §13-40-108(1)(b)', 'CRS §13-40-108(1)(a)', 'CRS §13-40-108(1)(c)']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- personal: Colo. Rev. Stat. § 13-40-106(2)(a)
- substituted: Colo. Rev. Stat. § 13-40-106(2)(b)
- posting_and_mail: Colo. Rev. Stat. § 13-40-106(2)(c), (3), (4)

**Gemini:**
- personal: C.R.S. § 13-40-108
- substituted: C.R.S. § 13-40-108
- posting: C.R.S. § 13-40-108
- electronic: C.R.S. § 38-12-510

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [HI-SVC-05] HI (Hawaii) — 🟡 CITATION-DIVERGENCE

**Module:** service.method_rules  
**Status:** 🟡 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['HRS §521-71(e)']  
**File same-statute pattern:** True  

**Issue:** Models agree with each other but differ from file.

**GPT citations:**
- personal: Haw. Rev. Stat. § 521-8(a)
- substituted: Haw. Rev. Stat. § 521-8(a)
- mail: Haw. Rev. Stat. § 521-8(a)
- posting: Haw. Rev. Stat. § 521-68(a)

**Gemini citations:**
- personal: HRS § 521-10(a)(1)
- substituted: HRS § 521-10(a)(2)
- mail: HRS § 521-10(b)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [IA-SVC-06] IA (Iowa) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['Iowa Code §562A.12']  
**File same-statute pattern:** True  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- acknowledged_delivery: Iowa Code § 562A.29A(1)(a)
- personal_service: Iowa Code § 562A.29A(1)(b)
- posting_and_mailing: Iowa Code § 562A.29A(1)(c)

**Gemini:**
- personal: Iowa Code § 562A.29A(1)
- substituted: Iowa Code § 562A.29A(1)
- mail: Iowa Code § 562A.29A(2)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [ID-SVC-07] ID (Idaho) — 🟡 SUBSECTION-FOUND

**Module:** service.method_rules  
**Status:** 🟡 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['Idaho Code §6-303']  
**File same-statute pattern:** True  

**Issue:** File cites parent statute for all methods; both models found method-specific subsections. Verify whether subsection-level citations are required.

**GPT subsections:**
- personal: Idaho Code § 6-304(1)
- substituted: Idaho Code § 6-304(2)
- posting_and_mailing: Idaho Code § 6-304(3)

**Gemini subsections:**
- personal: Idaho Code § 6-304(1)
- substituted: Idaho Code § 6-304(2)
- post_and_mail: Idaho Code § 6-304(3)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [IN-SVC-08] IN (Indiana) — 🟡 CITATION-DIVERGENCE

**Module:** service.method_rules  
**Status:** 🟡 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['Ind. Code §32-31-1-6']  
**File same-statute pattern:** True  

**Issue:** Models agree with each other but differ from file.

**GPT citations:**
- personal: Ind. Code § 32-31-1-9(b)(1)
- substituted: Ind. Code § 32-31-1-9(b)(2)
- mail: Ind. Code § 32-31-1-9(b)(3)

**Gemini citations:**
- personal: IC 32-31-1-9(a)
- substituted: IC 32-31-1-9(a)
- posting: IC 32-31-1-9(b)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [MA-SVC-09] MA (Massachusetts) — 🟡 CITATION-DIVERGENCE

**Module:** service.method_rules  
**Status:** 🟡 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['M.G.L. c. 186, §12']  
**File same-statute pattern:** True  

**Issue:** Models agree with each other but differ from file.

**GPT citations:**
- personal: Mass. Gen. Laws ch. 186, § 11
- substituted: Mass. Gen. Laws ch. 186, § 11
- mail: Mass. Gen. Laws ch. 186, § 11

**Gemini citations:**
- mail: M.G.L. c. 186, § 31
- personal: Uniform Summary Process Rule 2(b)
- substituted: Uniform Summary Process Rule 2(b)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [MO-SVC-10] MO (Missouri) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['Mo. Rev. Stat. §441.060; §535.030', 'Mo. Rev. Stat. §535.030']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- personal: Mo. Rev. Stat. § 441.060
- substituted: Mo. Rev. Stat. § 441.060
- posting: Mo. Rev. Stat. § 441.060

**Gemini:**
- personal: Mo. Rev. Stat. § 535.020.1
- substituted: Mo. Rev. Stat. § 535.020.1
- mail: Mo. Rev. Stat. § 535.020.1

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [MT-SVC-11] MT (Montana) — 🟡 CITATION-DIVERGENCE

**Module:** service.method_rules  
**Status:** 🟡 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['MCA §70-24-202']  
**File same-statute pattern:** True  

**Issue:** Models agree with each other but differ from file.

**GPT citations:**
- personal: Mont. Code Ann. § 70-27-110(1)
- substituted: Mont. Code Ann. § 70-27-110(2)
- posting_and_mail: Mont. Code Ann. § 70-27-110(3)

**Gemini citations:**
- personal: MCA § 70-24-108(2)(c)
- mail: MCA § 70-24-108(2)(c)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [NC-SVC-12] NC (North Carolina) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['NCGS §42-3; §1A-1, Rule 4', 'NCGS §42-3']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- not_statutorily_specified: N.C. Gen. Stat. § 42-3

**Gemini:**
- personal: N.C. Gen. Stat. § 42-3
- substituted: N.C. Gen. Stat. § 42-3
- mail: N.C. Gen. Stat. § 42-3

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [NH-SVC-13] NH (New Hampshire) — 🟡 CITATION-DIVERGENCE

**Module:** service.method_rules  
**Status:** 🟡 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['RSA 540:5']  
**File same-statute pattern:** True  

**Issue:** Models agree with each other but differ from file.

**GPT citations:**
- personal: RSA 540:5, I(a)
- substituted: RSA 540:5, I(b)
- mail: RSA 540:5, I(c); RSA 540:5, II

**Gemini citations:**
- personal: RSA 540:5
- substituted: RSA 540:5
- mail: RSA 540:5

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [OR-SVC-14] OR (Oregon) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['ORS 90.255(1)(a)', 'ORS 90.255(1)(c)', 'ORS 90.255(1)(b)']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- personal: Or. Rev. Stat. § 90.155(1)(a)
- first_class_mail: Or. Rev. Stat. § 90.155(1)(b); additional time under Or. Rev. Stat. § 90.155(2)
- first_class_mail_and_attachment: Or. Rev. Stat. § 90.155(1)(c)

**Gemini:**
- personal: ORS 90.155(1)(a)
- substituted: ORS 90.155(1)(b)
- mail_and_attachment: ORS 90.155(1)(c)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [PA-SVC-15] PA (Pennsylvania) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['68 P.S. §250.501; Pa. R.C.P. 1009', '68 P.S. §250.501']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- personal: 68 P.S. § 250.501(f)
- leaving_at_principal_building: 68 P.S. § 250.501(f)
- posting: 68 P.S. § 250.501(f)

**Gemini:**
- personal: 68 P.S. § 250.501(g)
- substituted: 68 P.S. § 250.501(g)
- posting: 68 P.S. § 250.501(g)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [SC-SVC-16] SC (South Carolina) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['SC Code §27-40-710(c)', 'SC Code §27-40-710(a)', 'SC Code §27-40-710(b)']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- personal: S.C. Code Ann. § 27-40-130(C)(3)
- mail: S.C. Code Ann. § 27-40-130(C)(3)

**Gemini:**
- personal: S.C. Code Ann. § 27-40-240(B)(3)
- mail: S.C. Code Ann. § 27-40-240(B)(3)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [TX-SVC-17] TX (Texas) — 🟡 CITATION-DIVERGENCE

**Module:** service.method_rules  
**Status:** 🟡 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['Tex. Prop. Code §24.005(f)']  
**File same-statute pattern:** True  

**Issue:** Models agree with each other but differ from file.

**GPT citations:**
- personal: Tex. Prop. Code § 24.005(f)
- inside-door posting: Tex. Prop. Code § 24.005(f)
- mail: Tex. Prop. Code § 24.005(f)
- outside-door alternative: Tex. Prop. Code § 24.005(f-1)

**Gemini citations:**
- personal_substituted: Texas Property Code § 24.005(f)
- affixing_inside: Texas Property Code § 24.005(f)
- mail: Texas Property Code § 24.005(f)
- affixing_outside_with_mail: Texas Property Code § 24.005(f)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [UT-SVC-18] UT (Utah) — 🟡 CITATION-DIVERGENCE

**Module:** service.method_rules  
**Status:** 🟡 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['Utah Code §78B-6-802']  
**File same-statute pattern:** True  

**Issue:** Models agree with each other but differ from file.

**GPT citations:**
- personal: Utah Code § 78B-6-805(1)
- mail: Utah Code § 78B-6-805(2)
- substituted: Utah Code § 78B-6-805(3)
- posting: Utah Code § 78B-6-805(4)

**Gemini citations:**
- personal: Utah Code Ann. § 78B-6-805(1)(a)
- substituted: Utah Code Ann. § 78B-6-805(1)(b)
- posting: Utah Code Ann. § 78B-6-805(1)(c)
- mail: Utah Code Ann. § 78B-6-805(3)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [WA-SVC-19] WA (Washington) — 🔴 MODEL-SPLIT

**Module:** service.method_rules  
**Status:** 🔴 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['RCW 59.12.040(3)', 'RCW 59.12.040(2)', 'RCW 59.12.040(1)']  
**File same-statute pattern:** False  

**Issue:** Models disagree with each other — attorney review required.

**GPT:**
- personal: RCW 59.12.040(1)
- substituted: RCW 59.12.040(2)
- posting_and_mailing: RCW 59.12.040(3)

**Gemini:**
- personal: RCW 59.12.040(1)
- substituted: RCW 59.12.040(2)
- posting and mailing: RCW 59.12.040(3)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [WV-SVC-20] WV (West Virginia) — 🟡 CITATION-DIVERGENCE

**Module:** service.method_rules  
**Status:** 🟡 pending-human-verification  
**Run date:** 2026-06-20

**File unique statutes:** ['WV Code §37-6-1']  
**File same-statute pattern:** True  

**Issue:** Models agree with each other but differ from file.

**GPT citations:**
- personal: W. Va. Code § 37-6-30
- substituted: W. Va. Code § 37-6-30
- posting: W. Va. Code § 37-6-30

**Gemini citations:**
- personal: W. Va. Code § 56-2-1(a) (as incorporated by W. Va. Code § 55-3A-1(c))
- substituted: W. Va. Code § 56-2-1(b) and (c) (as incorporated by W. Va. Code § 55-3A-1(c))
- mail: W. Va. Code § 55-3A-1(c)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---


## Service L7 Items

### DC (District of Columbia) — L7-SERVICE-ATTORNEY-REVIEW
- Date: 2026-06-20
- Reason: Persistent API failure across 3+ runs of both GPT and Gemini. No model data recoverable. Service statute(s) for D.C. pay-or-quit notices require attorney verification.
- Action needed: Identify correct service statute(s) for pay-or-quit notice

### NM (New Mexico) — L7-SERVICE-ATTORNEY-REVIEW
- Date: 2026-06-20
- Reason: Persistent API failure across 3+ runs of both GPT and Gemini. No model data recoverable. Service statute(s) for N.M. pay-or-quit notices require attorney verification.
- Action needed: Identify correct service statute(s) for pay-or-quit notice
