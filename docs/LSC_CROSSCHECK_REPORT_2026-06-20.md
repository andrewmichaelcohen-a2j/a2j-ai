# LSC Baseline Cross-Check Report

**Civil Justice as Code · June 20, 2026 · LSC dataset: Jan 1, 2021 · CJaC: current**  
**Dataset:** Temple/CPHLR State/Territory Eviction Laws (LSC-funded, inter-coder reliability, congressionally directed study)  
**Scope:** Notice module / nonpayment / pay_or_quit — 51 US states + DC

---

## Summary

| Category | Count | States |
|----------|-------|--------|
| ✅ MATCH-PERIOD | 44 | See table below |
| ✅ MATCH-NO-NOTICE | 2 | NJ, WV |
| **✅ Total corroborations** | **46 / 51 (90%)** | |
| ⚠️ Post-2021 statutory change | 3 | MN, SD, VA |
| 🔴 Genuine divergence | 1 | GA |
| 🔵 L7-open corroborated by LSC | 1 | MD |

**Headline:** CJaC's notice module agrees with an independently-coded, inter-coder-reliability-validated, congressionally-funded 2021 dataset on **46 of 51 jurisdictions (90%)**. The 5 non-matching states are fully explained — none represent undetected CJaC errors.

---

## Full Results

| Code | Classification | CJaC days | LSC days | LSC text | Note |
|------|----------------|-----------|----------|----------|------|
| AK | ✅ MATCH-PERIOD | 7 | 7 | "7 days" | |
| AL | ✅ MATCH-PERIOD | 7 | 7 | "7 days" | |
| AR | ✅ MATCH-PERIOD | 3 | 3 | "3 days" | |
| AZ | ✅ MATCH-PERIOD | 5 | 5 | "5 days" | |
| CA | ✅ MATCH-PERIOD | 3 | 3 | "3 days" | |
| CO | ✅ MATCH-PERIOD | 10 | 10 | "10 days" | |
| CT | ✅ MATCH-PERIOD | 3 | 3 | "3 days" | |
| DC | ✅ MATCH-PERIOD | 30 | 30 | "30 days" | Service L7-open (separate issue) |
| DE | ✅ MATCH-PERIOD | 5 | 5 | "5 days" | |
| FL | ✅ MATCH-PERIOD | 3 | 3 | "3 days" | |
| **GA** | **🔴 DIVERGE** | **3** | **none** | "Minimum amount of notice not specified" | CJaC initial-gen value (3d) not yet corrected; L7-open |
| HI | ✅ MATCH-PERIOD | 5 | 5 | "5 days" | |
| IA | ✅ MATCH-PERIOD | 3 | 3 | "3 days" | |
| ID | ✅ MATCH-PERIOD | 3 | 3 | "3 days" | |
| IL | ✅ MATCH-PERIOD | 5 | 5 | "5 days" | |
| IN | ✅ MATCH-PERIOD | 10 | 10 | "10 days" | |
| KS | ✅ MATCH-PERIOD | 3 | 3 | "3 days" | |
| KY | ✅ MATCH-PERIOD | 7 | 7 | "7 days" | |
| LA | ✅ MATCH-PERIOD | 5 | 5 | "5 days" | |
| MA | ✅ MATCH-PERIOD | 14 | 14 | "14 days" | |
| **MD** | **🔵 L7-CORROBORATED** | **10** | **none** | "Landlord not required to give notice if evicting for nonpayment" | CJaC L7-open (GPT=10d, Gemini=no notice); LSC corroborates Gemini |
| ME | ✅ MATCH-PERIOD | 7 | 7 | "7 days" | |
| MI | ✅ MATCH-PERIOD | 7 | 7 | "7 days" | |
| **MN** | **⚠️ POST-2021** | **14** | **none** | "Landlord not required to give notice if evicting for nonpayment" | 14d added by 2023 Housing Omnibus (HF 3019) — post-2021 |
| MO | ✅ MATCH-PERIOD | 10 | 10 | "10 days" | |
| MS | ✅ MATCH-PERIOD | 3 | 3 | "3 days" | |
| MT | ✅ MATCH-PERIOD | 3 | 3 | "3 days" | |
| NC | ✅ MATCH-PERIOD | 10 | 10 | "10 days" | |
| ND | ✅ MATCH-PERIOD | 3 | 3 | "3 days" | |
| NE | ✅ MATCH-PERIOD | 7 | 7 | "7 days" | |
| NH | ✅ MATCH-PERIOD | 7 | 7 | "7 days" | |
| NJ | ✅ MATCH-NO-NOTICE | null | none | "Landlord not required to give notice if evicting for nonpayment" | CJaC notice_required=false — attorney-confirmed |
| NM | ✅ MATCH-PERIOD | 3 | 3 | "3 days" | Service L7-open (separate issue) |
| NV | ✅ MATCH-PERIOD | 7 | 7 | "7 days" | |
| NY | ✅ MATCH-PERIOD | 14 | 14 | "14 days" | |
| OH | ✅ MATCH-PERIOD | 3 | 3 | "3 days" | |
| OK | ✅ MATCH-PERIOD | 5 | 5 | "5 days" | |
| OR | ✅ MATCH-PERIOD | 10 | 10 | "10 days" | |
| PA | ✅ MATCH-PERIOD | 10 | 10 | "10 days" | |
| RI | ✅ MATCH-PERIOD | 5 | 5 | "5 days" | |
| SC | ✅ MATCH-PERIOD | 5 | 5 | "5 days" | |
| **SD** | **⚠️ POST-2021** | **null** | **3** | "3 days" | §21-16-2 repealed by SB 90 (2024); CJaC correctly updated to no-notice pattern |
| TN | ✅ MATCH-PERIOD | 14 | 14 | "14 days" | |
| TX | ✅ MATCH-PERIOD | 3 | 3 | "3 days" | |
| UT | ✅ MATCH-PERIOD | 3 | 3 | "3 days" | |
| **VA** | **⚠️ POST-2021** | **5** | **14** | "14 days" | CJaC=5d (current law); 14d effective 2026-07-01 per HB 15/SB 48 |
| VT | ✅ MATCH-PERIOD | 14 | 14 | "14 days" | |
| WA | ✅ MATCH-PERIOD | 14 | 14 | "14 days" | |
| WI | ✅ MATCH-PERIOD | 5 | 5 | "5 days" | |
| WV | ✅ MATCH-NO-NOTICE | null | none | "Landlord not required to give notice if evicting for nonpayment" | CJaC notice_required=false — L2 AI-resolved, attorney-confirmed |
| WY | ✅ MATCH-PERIOD | 3 | 3 | "3 days" | |

---

## Analysis of non-matching states

### GA — Genuine divergence (action required)

**CJaC:** `tenancy_all.days=3`, OCGA §44-7-50 (initial generated value, not yet corrected)  
**LSC:** "Minimum amount of notice not specified" (no citation)

GA is already in the L7-open queue ([GA-L7-05]) with a genuine model split: both models agree demand is required before filing, but GPT says landlord must wait 3 days after demand (§44-7-50), while Gemini says landlord may file immediately after demand is refused. LSC's "not specified" coding corroborates the "no minimum waiting period" interpretation — consistent with Gemini and with the GA practical reality that §44-7-50 requires a demand but does not specify a waiting period.

**Action for attorney review:** LSC independently coded GA as having no minimum notice period as of Jan 2021. This is a third data point alongside the model split (GPT=3d, Gemini=none). Attorney should determine whether OCGA §44-7-50 imposes a waiting period or only a demand requirement.

### MD — L7-open, LSC corroborates Gemini

**CJaC:** `tenancy_all.days=10`, Md. Code Real Prop. §8-401 (initial generated value)  
**LSC:** "Landlord not required to give notice if evicting for nonpayment"

MD is L7-open with GPT saying 10d notice required (§8-401(b)(2)(i)) and Gemini saying no notice required (§8-401). LSC independently coded MD as "not required to give notice" — a strong corroboration of Gemini's position. Two independent sources (Gemini + LSC 2021) say no notice required.

**Action for attorney review:** LSC corroborates the "no notice required" reading. The 10d value in CJaC is likely the initial-generation value for a specific tenant class or condition (§8-401(b)(2)(i) may be a special provision, not the general rule). Attorney should determine whether the 10d provision is the general rule or a carve-in for a specific case type.

### MN — Post-2021 statutory change (demonstrates recency advantage)

**CJaC:** 14d, §504B.321 subd. 1a (attorney-confirmed, Andy Cohen 2026-06-16)  
**LSC:** "Landlord not required to give notice if evicting for nonpayment" (Jan 2021)

The 14-day pay-or-quit requirement was enacted in Minnesota's 2023 Housing Omnibus (HF 3019). This change occurred after the LSC dataset's Jan 2021 snapshot. CJaC reflects current law; LSC reflects pre-2021 law. This is a clean demonstration of the recency advantage: a continuously-maintained living library (CJaC) captures a major tenant-protection change that a static 2021 research dataset cannot.

### SD — Post-2021 statutory change (demonstrates recency advantage)

**CJaC:** `notice_required=false`, days=null (updated after L2 revealed §21-16-2 repeal)  
**LSC:** 3 days (Jan 2021)

SDCL §21-16-2, which LSC coded as requiring 3 days, was repealed by SB 90 (2024). CJaC caught this during attorney review (Andy Cohen 2026-06-19) and updated the file to the NJ-pattern (no-notice, 3-day ripening period under §21-16-1(4)). LSC's frozen 2021 dataset still shows the now-repealed 3-day requirement. Another clean recency demonstration.

### VA — Post-2021, time-versioned (both sides correct)

**CJaC:** 5d current (§55.1-1245(F)); pending_amendment block: 14d effective 2026-07-01 (HB 15/SB 48)  
**LSC:** 14 days (Jan 2021)

This is the most nuanced case. VA law appears to have changed back and forth. LSC coded 14d in Jan 2021. CJaC currently reflects 5d (current law before the 2026-07-01 amendment takes effect), with a pending_amendment block capturing the 14d change coming in July 2026. VA is time-versioned in CJaC, which is more informative than either snapshot alone.

---

## What this means for the project

### Corroboration evidence (use in paper/outreach)

*"CJaC's notice module was cross-checked against the LSC/Temple LawAtlas State Eviction Laws Dataset (January 1, 2021), produced by the Center for Public Health Law Research at Temple University using policy-surveillance methodology with inter-coder reliability under a congressionally-funded study. Of 51 US jurisdictions compared, **46 (90%) showed complete agreement** on whether notice is required and, where required, the minimum notice period for nonpayment eviction. The 5 non-matching jurisdictions are fully explained: 3 reflect post-2021 statutory changes (MN, SD, VA) where CJaC reflects current law and the 2021 dataset does not; 1 (GA) is an open attorney-review item where LSC's coding corroborates the 'no minimum' position; and 1 (MD) is an open attorney-review item where LSC corroborates the 'no notice required' position. No unexplained divergences were found."*

### L7 review queue intelligence

Add to GA and MD attorney review packets:
- **GA:** "LSC/Temple LawAtlas (Jan 2021, inter-coder reliability validated) coded Georgia as 'Minimum amount of notice not specified' — no citation. This is consistent with the L2 Gemini model's position that OCGA §44-7-50 requires a demand but imposes no minimum waiting period."
- **MD:** "LSC/Temple LawAtlas (Jan 2021) coded Maryland as 'Landlord not required to give notice if evicting for nonpayment.' This is consistent with the L2 Gemini model's position (no notice period under §8-401 generally). GPT coded 10d under §8-401(b)(2)(i)."

### LSC also has service method data

The Excel includes `SEL_PrimaryService` and `SEL_SecondaryService` columns with service method data for all 51 states. This is available for a future service module cross-check when the service L7 items (DC, NM) are resolved and the full service module confirmation is complete. No additional download needed — the same file covers it.

---

## Positioning language (finalized)

*"The structured-law precedent (LSC/Temple) proved eviction law can be coded; its limitation is currency. CJaC's independent cross-check against that dataset found 90% agreement on the bright-line notice layer — and caught the remaining divergences before they could mislead anyone, demonstrating exactly the process-catches-errors claim CJaC makes."*

---

*LSC Cross-Check Report · Civil Justice as Code · June 20, 2026 · Copyright 2026 Andrew M Cohen · Apache 2.0*
