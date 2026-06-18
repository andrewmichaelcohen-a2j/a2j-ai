# L2 Multi-Model Consensus Report — Phase 1 — Machine-Assist Flag States

**Run date:** 2026-06-18  
**Models:** OpenAI `gpt-5.5` · Google `gemini-2.5-pro`  
**Target:** Notice module — `pay_or_quit` nonpayment notice period and statutory citation  
**States run:** 8 (ME, OH, WV, MO, MS, ND, IL, SD) — all L1-MACHINE-ASSIST flag states  

> **Interpretation caveat:** Model consensus partly reflects shared secondary sources,
> so agreement is corroborating-but-not-independent. **Divergence is the stronger
> signal** — where the file and the two models disagree, that is where a human should
> look. Do not treat unanimous agreement as proof of correctness.

---

## Summary

| Classification | Count | States |
|---------------|-------|--------|
| ✅ CONSENSUS-CONFIRM | 3 | ME, IL, SD |
| ⚠️ CITATION-DIVERGENCE → AI-resolved | 2 | OH, MS |
| 🔴 PERIOD-DIVERGENCE → AI-resolved (convergent) | 1 | WV |
| 🔴 PERIOD-DIVERGENCE → L7 escalated | 1 | MO |
| ⚠️ MODEL-SPLIT → L7 escalated | 1 | ND |
| ❌ ERROR | 0 | — |

**AI-resolved (pending human confirmation):** OH, MS, WV  
**L7 escalated (attorney review required):** MO, ND

---

## Per-State Results

| State | MA flag | File days | File statute | GPT days | GPT statute | Gemini days | Gemini statute | Result |
|-------|---------|-----------|-------------|---------|------------|------------|---------------|--------|
| ME | L1-MA | 7 | 14 M.R.S. §6001 | 7 | 14 M.R.S. §6002 | 7 | 14 M.R.S. §6002 | ✅ CONSENSUS-CONFIRM |
| OH | L1-MA | 3 | ORC §1923.02; §5321.17 | 3 | ORC §1923.04(A) | 3 | ORC §1923.04(A) | ⚠️ CITATION-DIVERGENCE → AI-resolved |
| WV | L1-MA | 5 | W. Va. Code §37-6-5 | null | W. Va. Code §55-3A-1 | null | W. Va. Code §55-3A-1 | 🔴 PERIOD-DIVERGENCE → AI-resolved |
| MO | L1-MA | 10 | RSMo §535.060 | null | Mo. Rev. Stat. §535.020.1 | null (notice=true) | Mo. Rev. Stat. §535.020 | 🔴 PERIOD-DIVERGENCE → L7 escalated |
| MS | L1-MA | 3 | Miss. Code Ann. §89-7-27 | 3 | Miss. Code Ann. §89-8-13 | 3 | Miss. Code Ann. §89-8-13(5)(a) | ⚠️ CITATION-DIVERGENCE → AI-resolved |
| ND | L1-MA | 3 | NDCC §47-16-15 | 3 (notice req.) | NDCC §47-32-02 | null (no notice) | NDCC §47-32-02 | ⚠️ MODEL-SPLIT → L7 escalated |
| IL | L1-MA | 5 | 735 ILCS 5/9-207 | 5 | 735 ILCS 5/9-209 | 5 | 735 ILCS 5/9-209 | ✅ CONSENSUS-CONFIRM |
| SD | L1-MA | 3 | SDCL §21-16-1 | 3 | S.D. Codified Laws §21-16-1(2) | 3 | SDCL §21-16-2 | ✅ CONSENSUS-CONFIRM |

*Note: SD initially showed MODEL-SPLIT due to GPT PARSE_ERROR (insufficient token limit). Re-run after fix → CONSENSUS-CONFIRM.*

---

## Divergence Details

### OH — Citation Divergence → AI-Resolved

**File claim:** ORC §1923.02; ORC §5321.17  
**Both models identified:** ORC §1923.04(A) as the operative pre-filing notice provision

**Resolution:** ORC §1923.04(A) states a party desiring to commence a FED action "shall notify the adverse party to leave the premises three or more days before beginning the action." §1923.02 governs who may bring the action; §5321.17 governs lease termination and is referenced in §1923.04(B) only as an alternative. Verified from codes.ohio.gov.

**Status:** File corrected to §1923.04(A); period 3d confirmed; `L2-CITATION-DIVERGENCE` flag → `resolved-ai-corrected`; `pending-human-confirmation`.

---

### WV — Period Divergence → AI-Resolved (Convergent)

**File claim:** 5 days, W. Va. Code §37-6-5  
**Both models:** notice_required=false, W. Va. Code §55-3A-1 (high confidence)

**GPT reasoning:** W. Va. Code §55-3A-1 governs summary eviction and allows a landlord to petition for immediate relief when a tenant is in arrears of rent without any prior notice period requirement. §37-6-5 addresses notice to quit for periodic tenancies, not the nonpayment eviction action itself.

**Gemini reasoning:** §55-3A-1 is the summary eviction statute for nonpayment and permits filing without prior notice. §37-6-5 applies to termination of periodic tenancies, a separate situation.

**Status:** File corrected (notice_required=false, days=null, statute=§55-3A-1, count_method=null); `L2-PERIOD-DIVERGENCE` → `resolved-ai-corrected`; `pending-human-confirmation`.

---

### MS — Citation Divergence → AI-Resolved

**File claim:** Miss. Code Ann. §89-7-27  
**Both models identified:** Miss. Code Ann. §89-8-13(5)(a)

**Resolution:** §89-7-27 is in Chapter 7 (general/commercial tenancies) and explicitly excludes residential tenancies governed by Chapter 8 (RLTA). §89-8-13(5)(a) (RLTA — Miss. Residential Landlord and Tenant Act) is the operative residential nonpayment provision: "the landlord may deliver a written notice specifying the rental agreement will terminate if payment is not made within three (3) days." Verified from law.justia.com.

**Status:** File corrected to §89-8-13(5)(a); period 3d confirmed; `L2-CITATION-DIVERGENCE` → `resolved-ai-corrected`; `pending-human-confirmation`.

---

### MO — Period Divergence → L7 Escalated (No Convergence)

**File claim:** 10 days, RSMo §535.060  
**GPT:** notice_required=false, days=null, Mo. Rev. Stat. §535.020.1  
**Gemini:** notice_required=true, days=null, Mo. Rev. Stat. §535.020

**GPT reasoning:** §535.020 requires demand for rent but specifies no waiting period. A landlord may file immediately after demand is refused. §535.060 covers unlawful detainer but does not impose a mandatory notice period before filing.

**Gemini reasoning:** §535.020 requires a demand for payment of rent before filing, making it effectively a notice precondition. While no specific number of days is stated, the demand requirement means notice_required=true.

**Legal question for L7:** Is §535.020's demand-for-rent requirement a formal notice (notice_required=true) or merely a condition precedent that does not constitute a "notice period" (notice_required=false)? The models' substantive disagreement on this characterization — both citing §535.020 but reaching different conclusions — is the core question. The file's 10-day claim under §535.060 is almost certainly incorrect regardless.

**Status:** `L2-PERIOD-DIVERGENCE-L7-ESCALATED` flag written; attorney review required.

---

### ND — Model Split → L7 Escalated (Genuine Interpretive Question)

**File claim:** 3 days, NDCC §47-16-15  
**GPT:** notice_required=true, days=3, NDCC §47-32-02 — 3-day written notice required  
**Gemini:** notice_required=false, days=null, NDCC §47-32-02 — no notice required; landlord may file 3 days after rent is due

**GPT reasoning:** §47-32-02 requires landlord to give tenant a 3-day written notice to pay or quit before filing for eviction for nonpayment of rent.

**Gemini reasoning:** §47-32-02 establishes that a landlord may bring an eviction action when rent is unpaid, and the 3-day period is a ripening period (time after rent due before action can be filed), not a notice requirement.

**Legal question for L7:** The two models read the same statute (§47-32-02) as either (a) requiring a 3-day notice-to-quit or (b) creating a 3-day ripening period before the landlord can file. This is a genuine interpretive question requiring statutory text analysis and potentially case law review. Note: both models agree §47-16-15 (the file's citation) is wrong — they both cite §47-32-02.

**Status:** `L2-MODEL-SPLIT-L7` flag written; attorney review required.

---

### IL — Citation Note (Confirm with caveat)

**File claim:** 5 days, 735 ILCS 5/9-207  
**Both models:** 5 days, 735 ILCS 5/9-209

Models agree the period is 5 days but identify the operative statute as §9-209 (not §9-207 as retrieved by L1). §9-207 governs holdover tenancy termination; §9-209 is the specific nonpayment notice provision. L1 retrieved §9-207 because §9-209 was unresolvable via the retrieval path used. The statute in the file currently reflects §9-207 (the L1 retrieval), not the L2-identified §9-209. This may warrant a citation correction similar to OH/MS — flagged for human review.

---

## Technical Notes

- **Token limit issue (resolved):** gpt-5.5 is a reasoning model and uses chain-of-thought tokens before producing output. Initial run with `max_completion_tokens=350` caused PARSE_ERROR for 7/8 states. Fix: increased to `max_completion_tokens=2000` in l2_runner.py. Reasoning pass uses `max_completion_tokens=8000`.
- **No `temperature` parameter:** gpt-5.5 does not support `temperature`; removed from both scripts.
- **`max_tokens` vs `max_completion_tokens`:** gpt-5.5 requires `max_completion_tokens`; `max_tokens` returns 400 error.
- **WV path bug (fixed):** l2_reasoning_pass.py previously used `west_virginia` (underscore) in the file path; corrected to `west-virginia` (hyphen) to match actual directory name.
- **Gemini API key format:** Keys from Google AI Studio start with `AQ.` (not `AIzaSy...`). This is expected as of June 2026.

---

*L2 corroborates and flags. It never blesses and never auto-edits content.*  
*AI-resolved items update content and raise confidence but NEVER advance past AUTOMATED-CHECKS-PASSED.*  
*All reasoning is recorded so a human can audit and confirm each resolution.*  
*L7 escalations require attorney review before any status change.*

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
