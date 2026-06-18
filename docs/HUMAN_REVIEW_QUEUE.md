# Human Review Queue — Civil Justice as Code

**Module:** Notice / pay_or_quit · **Layer:** L2 Multi-Model Consensus  
**Maintained by:** Cowork (auto-updated by l2_phase2_runner.py) · **Confirmed by:** Andy Cohen  
**Last seeded:** 2026-06-18 (Phase 1) · **Phase 2 items appended automatically by runner**

> **How to use this queue:**  
> Work top-to-bottom. Each item has a classification (L7-ESCALATED = you decide from scratch; PENDING-CONFIRMATION = you confirm/reject the AI's proposed answer), the specific question, and a status field.  
> Update status to `confirmed` (AI answer accepted) or `resolved` (you provided the authoritative answer).  
> When resolved, note the authoritative answer in the "Resolution" field.

---

## Queue Summary

| Status | Count |
|--------|-------|
| 🔴 L7-ESCALATED (you decide) | 2 |
| 🟡 PENDING-CONFIRMATION (AI proposed, you confirm) | 6 |
| ✅ Resolved/Confirmed | 0 |

*Phase 2 items will be appended below when the runner completes.*

---

## L7-ESCALATED — Attorney Review Required

These items could not be resolved by AI reasoning. Attorney review of primary sources is required before any status change. Nothing advances past ACP until resolved.

---

### [MO-L7-01] Missouri — Notice / pay_or_quit — PERIOD-DIVERGENCE → L7

**Classification:** L7-ESCALATED  
**Status:** 🔴 pending  
**Run date:** 2026-06-18

**Question:** Is Missouri's §535.020 demand-for-rent requirement a formal *notice requirement* (notice_required=true, notice type: demand) before filing eviction, or only a *precondition to filing* that does not constitute a notice period (notice_required=false)?

**Background:** The file originally had 10 days under RSMo §535.060 (almost certainly wrong). Both models agree §535.020 is the operative provision, but split on its characterization:
- GPT (gpt-5.5): notice_required=false, days=null, statute §535.020.1 — "§535.020 requires demand for rent but specifies no waiting period. A landlord may file immediately after demand is refused."
- Gemini (gemini-2.5-pro): notice_required=true, days=null, statute §535.020 — "§535.020 requires a demand for payment of rent before filing, making it effectively a notice precondition."

Both models agree §535.060 is the wrong statute, and that no specific number of days is specified. They disagree only on whether the demand constitutes a "notice" or merely a condition precedent.

**Current file content:** notice_required=true (original), days=10 (original §535.060 — needs correction regardless of resolution)  
**Proposed content (pending your determination):** statute=§535.020 (confirmed by both models); days=null; notice_required=? (your call)

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

### [ND-L7-02] North Dakota — Notice / pay_or_quit — MODEL-SPLIT → L7

**Classification:** L7-ESCALATED  
**Status:** 🔴 pending  
**Run date:** 2026-06-18

**Question:** Under NDCC §47-32-02, is the 3-day period a *formal notice-to-quit requirement* (landlord must serve written notice; notice_required=true, days=3) or a *ripening period* (landlord may file after rent has been unpaid for 3 days; notice_required=false, days=null)?

**Background:** Both models cite §47-32-02 as the operative statute but reach opposite conclusions:
- GPT (gpt-5.5): notice_required=true, days=3 — "§47-32-02 requires landlord to give tenant a 3-day written notice to pay or quit before filing."
- Gemini (gemini-2.5-pro): notice_required=false, days=null — "§47-32-02 establishes that a landlord may bring an eviction action when rent is unpaid; the 3-day period is a ripening period before the landlord can file, not a notice requirement."

Both models agree §47-16-15 (the original file citation) is wrong. The genuine question is textual: does §47-32-02 require service of a notice, or does it simply set a waiting period?

**Current file content:** notice_required=true, days=3, statute=NDCC §47-16-15 (wrong — needs update to §47-32-02 regardless)  
**Proposed content (pending your determination):** statute=§47-32-02 (confirmed); period/notice_required=your call

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

## PENDING-CONFIRMATION — AI Proposed, You Confirm

These items have been AI-resolved: content corrected, reasoning recorded, status stays at ACP. Your job is to review the proposed answer and mark it confirmed (or override if wrong). Nothing changes until you sign off.

---

### [WV-PC-01] West Virginia — Notice / pay_or_quit — PERIOD-DIVERGENCE → AI-Resolved

**Classification:** PENDING-CONFIRMATION  
**Status:** 🟡 pending  
**Run date:** 2026-06-18

**Question to confirm:** Is it correct that West Virginia landlords may file an eviction action for nonpayment *without prior notice* to the tenant, under W. Va. Code §55-3A-1?

**AI proposed answer:** notice_required=false, days=null, statute=W. Va. Code §55-3A-1  
**Confidence:** HIGH (both models)  

**GPT reasoning:** "W. Va. Code §55-3A-1 governs summary eviction and allows a landlord to petition for immediate relief when a tenant is in arrears of rent without any prior notice period requirement. §37-6-5 addresses notice to quit for periodic tenancies, not the nonpayment eviction action itself."  
**Gemini reasoning:** "§55-3A-1 is the summary eviction statute for nonpayment and permits filing without prior notice. §37-6-5 applies to termination of periodic tenancies, a separate situation."

**File correction applied:** notice_required=false, days=null, statute=§55-3A-1, count_method=null  
**Prior file claim:** 5 days, §37-6-5

**Your review:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [OH-PC-02] Ohio — Notice / pay_or_quit — CITATION-DIVERGENCE → AI-Resolved

**Classification:** PENDING-CONFIRMATION  
**Status:** 🟡 pending  
**Run date:** 2026-06-18

**Question to confirm:** Is ORC §1923.04(A) the operative pre-filing notice provision for nonpayment evictions in Ohio (3-day notice to quit)?

**AI proposed answer:** statute=ORC §1923.04(A), days=3  
**Confidence:** HIGH (both models) · **Verified from:** codes.ohio.gov

**Reasoning:** §1923.04(A) states a party desiring to commence an FED action "shall notify the adverse party to leave the premises three or more days before beginning the action." §1923.02 governs who may bring an FED action; §5321.17 governs lease termination for periodic tenancy (referenced in §1923.04(B) only as an alternative satisfaction method). Both GPT and Gemini independently identified §1923.04(A).

**File correction applied:** statute §1923.02; §5321.17 → §1923.04(A) (period 3d unchanged)  

**Your review:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [MS-PC-03] Mississippi — Notice / pay_or_quit — CITATION-DIVERGENCE → AI-Resolved

**Classification:** PENDING-CONFIRMATION  
**Status:** 🟡 pending  
**Run date:** 2026-06-18

**Question to confirm:** Is Miss. Code Ann. §89-8-13(5)(a) the operative residential nonpayment notice provision in Mississippi (3-day notice)?

**AI proposed answer:** statute=§89-8-13(5)(a), days=3  
**Confidence:** HIGH (both models) · **Verified from:** law.justia.com

**Reasoning:** §89-7-27 is in Chapter 7 (general/commercial tenancies) and explicitly excludes residential tenancies governed by Chapter 8 (RLTA). §89-8-13(5)(a) (Residential Landlord and Tenant Act) is the operative residential provision: "the landlord may deliver a written notice specifying the rental agreement will terminate if payment is not made within three (3) days." Both GPT and Gemini identified §89-8-13.

**File correction applied:** statute §89-7-27 → §89-8-13(5)(a) (period 3d unchanged)  

**Your review:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [IL-PC-04] Illinois — Notice / pay_or_quit — CITATION-CONFIRMED

**Classification:** PENDING-CONFIRMATION  
**Status:** 🟡 pending  
**Run date:** 2026-06-18

**Question to confirm:** Is 735 ILCS 5/9-209 the correct operative statute for Illinois 5-day pay-or-quit notices for nonpayment?

**AI proposed answer:** statute=735 ILCS 5/9-209, days=5 (already in file)  
**Confidence:** HIGH (both models agree)

**Reasoning:** Both gpt-5.5 and gemini-2.5-pro independently cited 735 ILCS 5/9-209 as the operative provision. §9-207 (originally retrieved by L1) governs holdover tenancy termination; §9-209 specifically covers nonpayment. File was already corrected to §9-209 before L2 ran; L2 confirmed this is correct.

**No content change needed** — file already correct. This is a citation-confirmation item.  

**Your review:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [ME-PC-05] Maine — Notice / pay_or_quit — CITATION-CONFIRMED

**Classification:** PENDING-CONFIRMATION  
**Status:** 🟡 pending  
**Run date:** 2026-06-18

**Question to confirm:** Is 14 M.R.S. §6002 the correct operative statute for Maine 7-day pay-or-quit notices for nonpayment?

**AI proposed answer:** statute=14 M.R.S. §6002, days=7 (already in file)  
**Confidence:** HIGH (both models agree)

**Reasoning:** GPT cited 14 M.R.S. §§6001, 6002(1-A)(D); Gemini cited 14 M.R.S. §6002(1). Both confirm §6002 as the operative notice section (§6001 is the FED availability-of-remedy statute). File already has §6002; L2 run confirmed.

**No content change needed** — file already correct. This is a citation-confirmation item.  

**Your review:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [SD-PC-06] South Dakota — Notice / pay_or_quit — CITATION-AMBIGUOUS

**Classification:** PENDING-CONFIRMATION (citation only; period confirmed)  
**Status:** 🟡 pending  
**Run date:** 2026-06-18

**Question to confirm:** Period (3 days) is confirmed by both models. But which citation is correct: SDCL §21-16-1 (current file), §21-16-1(2) (GPT), or §21-16-2 (Gemini)?

**Background:** Both models confirmed 3-day period. But they disagree on the specific section:
- GPT: SDCL §21-16-1(2) (subsection 2)
- Gemini: SDCL §21-16-2 (separate section)
- L1 note: §21-16-1 is the FED grounds statute; subsection (4) covers nonpayment
- Current file: SDCL §21-16-1 (entire section)

Models disagree → cannot auto-resolve. Human must check primary source.

**Proposed correction (pending your determination):** Update to whichever section is the operative 3-day notice provision. GPT's §21-16-1(2) seems inconsistent with L1's note (L1 says subsection (4) covers nonpayment). Gemini's §21-16-2 may be the notice provision (separate from the grounds statute §21-16-1).

**Your review:** ________________  
**Authoritative source:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

## Phase 2 Items

*Phase 2 run: 2026-06-18*

### [VA-RETRY-02] VA (Virginia) — 🔴 L7-ESCALATED

**L2 classification:** MODEL-SPLIT  
**Resolution:** L7-ESCALATED  
**Status:** 🔴 pending  
**Run date:** 2026-06-18

**Question:** Attorney must determine the correct notice requirement for Virginia nonpayment evictions.

**L2 result:** Models disagreed.
- GPT: 5d, Va. Code § 55.1-1245(F) — For nonpayment of rent, the landlord must serve written notice stating that rent is unpaid and that the rental agreement will terminate if the rent is not paid within five days. Only after the tenant 
- Gemini: 14d, Va. Code Ann. § 55.1-1245(F) — If rent is unpaid when due, the landlord must serve the tenant with a 14-day written notice informing the tenant of the nonpayment and the landlord's intent to terminate the rental agreement. The land
- File: 5d, Va. Code §55.1-1245

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---



*Phase 2 run: 2026-06-18*

### [AR-RETRY-01] AR (Arkansas) — 🔴 L7-ESCALATED

**L2 classification:** MODEL-SPLIT  
**Resolution:** L7-ESCALATED  
**Status:** 🔴 pending  
**Run date:** 2026-06-18

**Question:** Attorney must determine the correct notice requirement for Arkansas nonpayment evictions.

**L2 result:** Models disagreed.
- GPT: 3d, Ark. Code Ann. § 18-60-304(3) — For nonpayment of rent, Arkansas defines unlawful detainer to include a tenant who fails or refuses to pay rent when due and, after three days’ written notice to quit and demand for possession, refuse
- Gemini: 5d, A.C.A. § 18-60-304(d) — Before filing a civil eviction (unlawful detainer) action, a landlord must provide written notice to the tenant that an eviction will be filed if the overdue rent is not paid within five days from the
- File: 3d, Ark. Code Ann. §18-17-701

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [VA-RETRY-03] VA (Virginia) — 🔴 L7-ESCALATED

**L2 classification:** MODEL-SPLIT  
**Resolution:** L7-ESCALATED  
**Status:** 🔴 pending  
**Run date:** 2026-06-18

**Question:** Attorney must determine the correct notice requirement for Virginia nonpayment evictions.

**L2 result:** Models disagreed.
- GPT: 5d, Va. Code § 55.1-1245(F) — For nonpayment of rent, the tenant must fail to pay within five days after written notice of nonpayment and the landlord’s intent to terminate if rent is not paid. Only after that five-day notice peri
- Gemini: 14d, Va. Code Ann. § 55.1-1245(F) — For nonpayment of rent, a landlord must provide the tenant with a 14-day written notice to pay the amount due before the landlord can file an unlawful detainer action. This notice gives the tenant an 
- File: 5d, Va. Code §55.1-1245

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---



*Phase 2 run: 2026-06-18*

### [AR-P2-01] AR (Arkansas) — 🔴 L7-ESCALATED

**L2 classification:** MODEL-SPLIT  
**Resolution:** L7-ESCALATED  
**Status:** 🔴 pending  
**Run date:** 2026-06-18

**Question:** Attorney must determine the correct notice requirement for Arkansas nonpayment evictions.

**L2 result:** Models disagreed.
- GPT: Noned, None — PARSE_ERROR: 
- Gemini: 3d, A.C.A. § 18-60-304(d)(1) — Arkansas law requires a landlord to provide a residential tenant with a written notice allowing at least three days to vacate the property for failure to pay rent. This notice must be delivered before
- File: 3d, Ark. Code Ann. §18-17-701

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [DC-P2-02] DC (District of Columbia) — 🔴 L7-ESCALATED

**L2 classification:** MODEL-SPLIT  
**Resolution:** L7-ESCALATED  
**Status:** 🔴 pending  
**Run date:** 2026-06-18

**Question:** Attorney must determine the correct notice requirement for District of Columbia nonpayment evictions.

**L2 result:** Models disagreed.
- GPT: Noned, None — PARSE_ERROR: 
- Gemini: 30d, D.C. Code § 42-3505.01(a-1) — The statute requires a landlord to provide a tenant with a written notice of intent to file an eviction complaint for nonpayment of rent. This notice must inform the tenant that they have at least 30 
- File: 30d, DC Code §42-3505.01

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [DE-P2-03] DE (Delaware) — 🟡 PENDING-CONFIRMATION

**L2 classification:** CITATION-DIVERGENCE  
**Resolution:** CITATION-AI-RESOLVED  
**Status:** 🟡 pending  
**Run date:** 2026-06-18

**Question to confirm:** Citation corrected by AI consensus. Please verify the operative section.

**AI proposed statute:** 25 Del. C. § 5502(a) (both models agree)
**Prior file statute:** 25 Del. C. §5501
**Period:** 5d (confirmed)

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [KY-P2-04] KY (Kentucky) — 🔴 L7-ESCALATED

**L2 classification:** MODEL-SPLIT  
**Resolution:** L7-ESCALATED  
**Status:** 🔴 pending  
**Run date:** 2026-06-18

**Question:** Attorney must determine the correct notice requirement for Kentucky nonpayment evictions.

**L2 result:** Models disagreed.
- GPT: Noned, None — PARSE_ERROR: 
- Gemini: 7d, KRS § 383.660(2) — A landlord must provide a tenant with seven days' written notice of nonpayment and the intent to terminate the rental agreement if the rent is not paid. The landlord may only terminate the agreement a
- File: 7d, KRS §383.660

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [LA-P2-05] LA (Louisiana) — 🔴 L7-ESCALATED

**L2 classification:** MODEL-SPLIT  
**Resolution:** L7-ESCALATED  
**Status:** 🔴 pending  
**Run date:** 2026-06-18

**Question:** Attorney must determine the correct notice requirement for Louisiana nonpayment evictions.

**L2 result:** Models disagreed.
- GPT: Noned, None — PARSE_ERROR: 
- Gemini: 5d, La. Code Civ. Proc. art. 4701 — When a tenant fails to pay rent, the landlord must deliver a written notice to vacate the premises. The law requires that this notice give the tenant at least five days from the date of delivery to le
- File: 5d, La. R.S. §9:3259; La. C.C.P. Art. 4701

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [MA-P2-06] MA (Massachusetts) — 🔴 L7-ESCALATED

**L2 classification:** MODEL-SPLIT  
**Resolution:** L7-ESCALATED  
**Status:** 🔴 pending  
**Run date:** 2026-06-18

**Question:** Attorney must determine the correct notice requirement for Massachusetts nonpayment evictions.

**L2 result:** Models disagreed.
- GPT: Noned, None — PARSE_ERROR: 
- Gemini: 14d, Mass. Gen. Laws ch. 186, § 11 — The statute specifies that upon a tenant's failure to pay rent due under a written lease, a 14-day written notice to quit from the landlord is sufficient to terminate the tenancy. This notice must be 
- File: 14d, MGL c. 186 §11

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [MD-P2-07] MD (Maryland) — 🔴 L7-ESCALATED

**L2 classification:** MODEL-SPLIT  
**Resolution:** L7-ESCALATED  
**Status:** 🔴 pending  
**Run date:** 2026-06-18

**Question:** Attorney must determine the correct notice requirement for Maryland nonpayment evictions.

**L2 result:** Models disagreed.
- GPT: 10d, Md. Code Ann., Real Prop. § 8-401(b)(2)(i) — For a residential tenancy, the landlord must provide the tenant a written notice of intent to file a complaint for summary ejectment at least 10 days before filing a nonpayment-of-rent eviction action
- Gemini: Noned, Md. Code, Real Prop. § 8-401 — The statute does not mandate a notice period before filing an action for nonpayment of rent. A landlord may file a written complaint with the District Court to begin the repossession process immediate
- File: 10d, Md. Code Real Prop. §8-401

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [NV-P2-08] NV (Nevada) — 🟡 PENDING-CONFIRMATION

**L2 classification:** PERIOD-DIVERGENCE  
**Resolution:** PERIOD-AI-RESOLVED  
**Status:** 🟡 pending  
**Run date:** 2026-06-18

**Question to confirm:** AI reasoning converged. Please verify the proposed answer is correct.

**AI proposed:** notice_required=True, days=7, statute=NRS § 40.253(1)(a)
**GPT reasoning:** Nevada’s nonpayment-of-rent eviction statute is NRS § 40.253, which requires a written notice demanding either payment of rent or surrender of the premises before the tenant is guilty of unlawful detainer for nonpayment. For residential premises, the current statutory period is 7 judicial days after
**Gemini reasoning:** Under NRS § 40.253(1), a tenant who defaults on rent is guilty of unlawful detainer only after being served with a written notice and continuing in possession for 7 judicial days. This statute was amended in 2019, changing the period from 5 days to 7 judicial days, which resolves the conflict betwee
**Prior file claim:** days=5, statute=NRS §40.253

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [TN-P2-09] TN (Tennessee) — 🔴 L7-ESCALATED

**L2 classification:** MODEL-SPLIT  
**Resolution:** L7-ESCALATED  
**Status:** 🔴 pending  
**Run date:** 2026-06-18

**Question:** Attorney must determine the correct notice requirement for Tennessee nonpayment evictions.

**L2 result:** Models disagreed.
- GPT: Noned, None — PARSE_ERROR: 
- Gemini: 14d, Tenn. Code Ann. § 66-28-505(b) — This statute provides the general remedy for a tenant's noncompliance with the rental agreement, which includes the nonpayment of rent. It requires the landlord to provide a written notice of terminat
- File: 14d, TCA §66-28-505

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [VA-P2-10] VA (Virginia) — 🔴 L7-ESCALATED

**L2 classification:** MODEL-SPLIT  
**Resolution:** L7-ESCALATED  
**Status:** 🔴 pending  
**Run date:** 2026-06-18

**Question:** Attorney must determine the correct notice requirement for Virginia nonpayment evictions.

**L2 result:** Models disagreed.
- GPT: Noned, None — PARSE_ERROR: 
- Gemini: 5d, Va. Code Ann. § 55.1-1245(F) — If rent is unpaid when due, the landlord must serve the tenant with a written notice stating that the tenant has five days to pay the rent or the rental agreement will be terminated. This notice is a 
- File: 5d, Va. Code §55.1-1245

**Resolution:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---



*Will be appended automatically when `l2_phase2_runner.py` completes.*

---

## Resolved Items

*Move entries here once confirmed or resolved, with the authoritative answer noted.*

---

*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*  
*Queue auto-updated by `rules/validation/l2/l2_phase2_runner.py`. Manual entries also permitted.*  
*Status values: 🔴 pending · 🟡 pending (confirmation) · ✅ confirmed · 🟢 resolved*
