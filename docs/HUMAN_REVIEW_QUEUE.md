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

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

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

**Your review:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [OH-PC-02] Ohio — Confirm §1923.04(A), 3 days

**Classification:** PENDING-CONFIRMATION · **Status:** 🟡 pending  
**AI proposed:** statute ORC §1923.04(A), days=3 (period unchanged)  
**Prior file statute:** §1923.02; §5321.17 (citation only — period was correct)

**Question to confirm:** Is ORC §1923.04(A) the operative pre-filing notice provision for nonpayment evictions in Ohio (3-day notice to quit)?

**Reasoning:** §1923.04(A) states a party desiring to commence an FED action "shall notify the adverse party to leave the premises three or more days before beginning the action." Both GPT and Gemini independently identified §1923.04(A). Verified from codes.ohio.gov.

**Your review:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [MS-PC-03] Mississippi — Confirm §89-8-13(5)(a), 3 days

**Classification:** PENDING-CONFIRMATION · **Status:** 🟡 pending  
**AI proposed:** statute §89-8-13(5)(a), days=3 (period unchanged)  
**Prior file statute:** §89-7-27

**Question to confirm:** Is Miss. Code Ann. §89-8-13(5)(a) (RLTA, Chapter 8) the operative residential nonpayment notice provision — not §89-7-27 (Chapter 7, general/commercial tenancies)?

**Reasoning:** §89-7-27 is in Chapter 7, which explicitly excludes residential tenancies governed by Chapter 8 (RLTA). §89-8-13(5)(a) is the operative residential provision: landlord may give 3-day written notice.

**Your review:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [DE-PC-04] Delaware — Confirm §5502(a), 5 days

**Classification:** PENDING-CONFIRMATION · **Status:** 🟡 pending  
**AI proposed:** statute 25 Del. C. §5502(a), days=5 (period unchanged)  
**Prior file statute:** 25 Del. C. §5501

**Question to confirm:** Is 25 Del. C. §5502(a) (not §5501) the operative nonpayment notice section for Delaware?

**Reasoning:** Both GPT and Gemini cited §5502(a) independently. §5501 is likely the general jurisdiction/applicability provision.

**Your review:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [NV-PC-05] Nevada — Confirm 7-day period, §40.253(1)(a)

**Classification:** PENDING-CONFIRMATION · **Status:** 🟡 pending  
**AI proposed:** notice_required=true, days=7, statute NRS §40.253(1)(a)  
**Prior file:** notice_required=true, days=5, statute NRS §40.253

**Question to confirm:** Is the correct Nevada nonpayment notice period 7 days (not 5), under NRS §40.253(1)(a)?

**GPT confidence:** high · **Gemini confidence:** high

**Your review:** ________________  
**Confirmed by:** ________________  **Date:** ________________

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

**Resolution:** ________________  
**Authoritative source:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [IL-CR-02] Illinois — Confirm 735 ILCS 5/9-209 (citation already correct in file)

**Classification:** CITATION-REVIEW · **Status:** 🟡 pending  
**Period:** 5 days (confirmed) · **Current file statute:** 735 ILCS 5/9-209 (already correct)

**Question:** Routine confirmation. Both models confirmed §9-209. File was already corrected from §9-207 (holdover/termination) to §9-209 (nonpayment). Verify §9-209 is the operative pay-or-quit provision.

**Your review:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [ME-CR-03] Maine — Confirm 14 M.R.S. §6002 (citation already correct in file)

**Classification:** CITATION-REVIEW · **Status:** 🟡 pending  
**Period:** 7 days (confirmed) · **Current file statute:** 14 M.R.S. §6002 (already correct)

**Question:** Routine confirmation. GPT cited §§6001, 6002(1-A)(D); Gemini cited §6002(1). Both confirm §6002 is operative (§6001 is the availability-of-remedy statute). File already has §6002. Verify.

**Your review:** ________________  
**Confirmed by:** ________________  **Date:** ________________

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
