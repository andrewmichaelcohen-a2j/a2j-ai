# L2 Service Reasoning Pass Report

**Run date:** 2026-06-19/20
**Models:** OpenAI `gpt-5.5` · Google `gemini-2.5-pro`
**Target:** 35 states flagged by service L2 runner as CITATION-DIVERGENCE, MODEL-SPLIT, or ERROR (plus CA later reclassified as L6-RECENCY-WATCH only)
**Status:** Reconciled 2026-06-20 — per-unit resolved statutes extracted from rules files

---

## Summary

| Outcome | Count | States |
|---------|-------|--------|
| ✅ AI-RESOLVED (reasoning converged, incl. single-model fallback) | 31 | AK, AL, AR, AZ, CO, DE, GA, HI, IA, IN, KS, LA, MA, MO, MT, NC, ND, NH, NJ, NV, OR, PA, SC, SD, TN, TX, UT, VA, WA, WI, WV |
| ✅ AI-RESOLVED (subsection direct) | 1 | ID |
| ⚠️ L6-RECENCY-WATCH only (resolved, watch flag) | 1 | CA — CONSENSUS-CONFIRM + recency watch; AB 2347 (2022) |
| 🔴 L7-ATTORNEY-REVIEW | 2 | DC, NM — persistent API failure; per protocol, Step 4 re-runs these |
| **Total** | **35** | |

**Human review load after full tiered protocol:** 2 states (DC, NM — technical API failure artifacts, not substantive splits). Zero genuine interpretive disputes reached L7.

**Single-model fallback applied to:** AR, TN, VA, WI — GPT persistent empty responses; Gemini returned high-confidence, well-supported answers. Single-model fallback prevented model API failures from becoming false L7 escalations.

**Subsection targeting applied to:** IN (resolved on 3rd pass with method-specific subsection query after generic tiebreakers failed twice), ID (direct subsection confirmation).

---

## Step 0 Reconciliation Finding

**The ledger's claimed 32/35 AI-resolved (91%) is CORRECT and substantiated.**

Prior flag audit showed apparent discrepancy: scan categorized OR, VA, WA under L6-RECENCY-WATCH (primary open flag), obscuring their concurrent L2-SERVICE-REASONING-PASS-RESOLVED (closed) flags. Full audit confirms:
- OR, VA, WA: each has BOTH `L2-SERVICE-REASONING-PASS-RESOLVED` (closed, resolved) AND `L6-SERVICE-RECENCY-WATCH` (open, watch only)
- CA: has `L2-SERVICE-CONSENSUS-CONFIRM` (resolved) AND `L6-SERVICE-RECENCY-WATCH` — classified separately in ledger as 1-state L6-only row since it resolved differently from the 16 SAME-STATUTE-CONFIRMED round-1 states
- Actual count: 16 round-1 confirmed + 32 AI-resolved + 1 CA (L6 special) + 2 L7 = 51 ✓

---

## Per-State Results

| State | Original Flag | Resolution Method | Personal | Substituted | Mail | L6 Watch |
|-------|--------------|-------------------|----------|-------------|------|-----------|
| AK | L2-SERVICE-MODEL-SPLIT-L7 | reasoning-pass | AS 09.45.100(b)(1) | AS 09.45.100(b)(2) | AS 09.45.100(b)(3) | — |
| AL | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | Ala. Code § 35-9A-141(c)(3) | Not authorized by statute | Ala. Code § 35-9A-141(c)(3) | — |
| AR | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass (single-model fallback) | A.C.A. § 18-60-304(d)(1) | A.C.A. § 18-60-304(d)(1) | A.C.A. § 18-60-304(d)(2) | — |
| AZ | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | ARS § 33-1313(B)(1) | ARS § 33-1313(B)(3) | ARS § 33-1313(B)(2) | — |
| CO | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | Colo. Rev. Stat. § 13-40-108(1)(a) | Colo. Rev. Stat. § 13-40-108(1)(b) | Colo. Rev. Stat. § 13-40-108(1)(c) | — |
| DE | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | 25 Del. C. § 5113(a)(1) | 25 Del. C. § 5113(a)(2) | 25 Del. C. § 5113(a)(3), (a)(4) & (b) | — |
| GA | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | O.C.G.A. § 44-7-50(a) | O.C.G.A. § 44-7-50(a) | O.C.G.A. § 44-7-50(a) | — |
| HI | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | HRS § 521-10(b)(3) | HRS § 521-10(b) | HRS § 521-10(b)(3) | — |
| IA | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | Iowa Code § 562A.29A(1)(b) | Iowa Code § 562A.29A(1)(a); also § 562A.29A(1)(b) | Iowa Code § 562A.29A(1)(c) + § 562A.29A(2) | — |
| ID | L2-SERVICE-CITATION-DIVERGENCE | subsection-direct | Idaho Code § 6-304(1) | Idaho Code § 6-304(2) | Idaho Code § 6-304(3) | — |
| IN | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass (subsection-targeted, 3rd pass) | Ind. Code § 32-31-1-9(b)(1) | Ind. Code § 32-31-1-9(b)(2) | Ind. Code § 32-31-1-9(b)(3) | — |
| KS | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | K.S.A. 58-2564(b) | K.S.A. 58-2564(b) | Not authorized by statute | — |
| LA | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | La. Code Civ. Proc. art. 4703(A)(1) | La. Code Civ. Proc. art. 4703(A)(3) | La. Code Civ. Proc. art. 4703(A)(4); art. 4703(A)(5) | — |
| MA | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | M.G.L. c. 186, § 11 | M.G.L. c. 186, § 11 | M.G.L. c. 186, § 11 | — |
| MO | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | Mo. Rev. Stat. § 534.050 | Mo. Rev. Stat. § 534.050 | — (statute silent on mail) | — |
| MT | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | MCA § 70-24-108(2)(c) | MCA § 70-24-108(2)(c) | MCA § 70-24-108(2)(c) | — |
| NC | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | N.C. Gen. Stat. § 42-26(a) | N.C. Gen. Stat. § 42-26(a) | N.C. Gen. Stat. § 42-26(a) | — |
| ND | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | N.D. Cent. Code § 47-32-02 | N.D. Cent. Code § 47-32-02 | N.D. Cent. Code § 47-32-02 | — |
| NH | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | RSA 540:5, I(a) | RSA 540:5, I(b) | RSA 540:5, I(c); RSA 540:5, II | — |
| NJ | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | N.J.S.A. 2A:18-56(a) | N.J.S.A. 2A:18-56(b) | — (statute silent on mail) | — |
| NV | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | NRS 40.280(1)(a) | NRS 40.280(1)(b) | NRS 40.280(1)(c) | — |
| OR | L2-SERVICE-MODEL-SPLIT-L7 | reasoning-pass | ORS 90.155(1)(a) | ORS 90.155(1)(c) | ORS 90.155(1)(b) | ⚠️ SB 278 (2023) |
| PA | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | 68 P.S. § 250.501(g) | 68 P.S. § 250.501(g) | — (statute silent on mail) | — |
| SC | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | S.C. Code Ann. § 27-40-240(B)(3) | — (not addressed in statute) | S.C. Code Ann. § 27-40-240(B)(3) | — |
| SD | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | SDCL 21-16-2(1) | SDCL 21-16-2(2) | SDCL 21-16-2 | — |
| TN | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass (single-model fallback) | Tenn. Code Ann. § 66-28-107(c)(3) | — (not addressed by statute) | Tenn. Code Ann. § 66-28-107(c)(3) | — |
| TX | L2-SERVICE-MODEL-SPLIT-L7 | reasoning-pass | Tex. Prop. Code § 24.005(f) | Tex. Prop. Code § 24.005(f); § 24.005(f-1) | Tex. Prop. Code § 24.005(f) | — |
| UT | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | Utah Code § 78B-6-805(1)(a) | Utah Code § 78B-6-805(1)(b) | Utah Code § 78B-6-805(5) | — |
| VA | L2-SERVICE-ERROR | reasoning-pass (single-model fallback) | Va. Code Ann. § 55.1-1202(A)(1) | Va. Code Ann. § 55.1-1202(A)(2) | Va. Code Ann. § 55.1-1202(B) | ⚠️ HB 15/SB 48 (2026) |
| WA | L2-SERVICE-MODEL-SPLIT-L7 | reasoning-pass | RCW 59.12.040(1) via RCW 59.18.365 | RCW 59.12.040(2) via RCW 59.18.365 | RCW 59.12.040(2)/(3) + RCW 59.18.365 | ⚠️ RCW amended 2021–2023 |
| WI | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass (single-model fallback) | Wis. Stat. § 704.21(1)(a) | Wis. Stat. § 704.21(1)(a) | Wis. Stat. § 704.21(1)(d) | — |
| WV | L2-SERVICE-CITATION-DIVERGENCE | reasoning-pass | W. Va. Code § 55-3A-1(c) + W. Va. R. Civ. P. 4(d)(1)(A) | W. Va. Code § 55-3A-1(c) + W. Va. R. Civ. P. 4(d)(1)(B) | W. Va. Code § 55-3A-1(c) | — |

---

## L7 Escalated — Pending Step 4 Re-Run

| State | Original Flag | Escalation Reason | Step 4 Action |
|-------|--------------|-------------------|---------------|
| DC | L2-SERVICE-ERROR | Persistent API failure — zero recoverable model data. Not a substantive split. | Re-run with single-model fallback per Step 4 protocol |
| NM | L2-SERVICE-ERROR | Persistent API failure — zero recoverable model data. Not a substantive split. | Re-run with single-model fallback per Step 4 protocol |

Per operating protocol: technical failure (API/parse) ≠ genuine interpretive dispute. DC and NM are in L7 as artifacts only. They will be re-run in Step 4 (fresh calls, single-model fallback). Only if substantive divergence survives a clean run do they remain L7.

---

## Notes on Specific Resolutions

**SD:** Service module cites SDCL 21-16-2 for service methods. Note: SDCL 21-16-2 was repealed by SB 90 (2024) with respect to the *notice period* (nonpayment notice no longer required). The service method provision may be under a different subsection or statute. Attorney review of SD service methods is advisable alongside the notice module L7 item.

**AL:** Substituted service not authorized by statute under Ala. Code § 35-9A-141(c)(3). Personal delivery and mail only.

**KS:** Mail service not authorized by statute under K.S.A. 58-2564(b). Personal delivery and substituted only.

**MO, NJ, PA, SC, TN:** Statute silent on one or more service methods; resolved statutes reflect what the statute expressly addresses.

---

*All resolved items: `pending-human-confirmation`. Nothing advanced past ACP. Automation narrows; a named attorney crosses the validation line.*

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
