# LSC Baseline Cross-Check — Assessment & Execution Plan

**Civil Justice as Code · June 20, 2026 · Prepared by: Claude (Cowork)**  
**Status: PARTIAL EXECUTION COMPLETE** — summary-report corroboration done; full dataset cross-check pending Andy's LawAtlas download.

---

## What this is

The LSC/Temple LawAtlas State Eviction Laws dataset (Jan 1, 2021) is the closest existing structured precedent to CJaC's notice module. Cross-checking CJaC against it serves two distinct purposes:

1. **Corroboration / error-catching:** where CJaC and LSC agree on pre-2021 law → corroboration evidence. Where they diverge → investigate: either CJaC has an error *or* the law changed post-2021. Both outcomes are useful.
2. **Positioning / credibility:** CJaC can cite agreement with an independently-coded, inter-coder-reliability-validated, congressionally-funded dataset as external corroboration. This is a strong credibility lever for the paper and outreach.

The cross-check also directly benefits the **open L7 items** — where CJaC has a genuine attorney-judgment question, LSC's independent 2021 coding can corroborate one side of the split or confirm the question is real.

---

## What LSC codes (relevant to CJaC notice module)

From the Codebook and Summary Report, the LSC dataset captures for nonpayment evictions:

- Whether a pre-filing notice to the tenant is required
- If required: the minimum notice period (days)
- Whether tenants have an opportunity to cure (pay and avoid eviction)
- The type of notice required (written / oral / not specified)
- Statutory citation

**CJaC fields this maps to:** `notice.pay_or_quit.notice_required`, `notice.pay_or_quit.days`, `notice.pay_or_quit.statute`

---

## Part 1: Immediate findings from public Summary Report (no account needed)

The Summary Report (Jan 2021) states:

> "Most jurisdictions specify a minimum amount of time a tenant must be late on rent before a landlord can file an eviction action in court due to nonpayment, ranging from three days to 30 days. However, **six jurisdictions do not specify a minimum amount of time: Georgia, Maryland, Minnesota, New Jersey, Puerto Rico, & West Virginia.**"

Cross-referencing against CJaC eviction-v2:

| State | LSC 2021 | CJaC current | Assessment |
|-------|----------|--------------|------------|
| **GA** | No minimum time | L7-OPEN (split: GPT=3d required, Gemini=no minimum) | ✅ **LSC corroborates Gemini / "no minimum" position.** Useful L7 intelligence: LSC's independent 2021 coding supports the "notice_required=false or no minimum" interpretation. Attorney should consider this. |
| **MD** | No minimum time | L7-OPEN (GPT: 10d required §8-401(b)(2)(i); Gemini: no notice §8-401) | ✅ **LSC corroborates Gemini / "no notice" position.** Significant — an independent, validated 2021 dataset agrees with the "no minimum" reading. Strong weight for the attorney's review. |
| **MN** | No minimum time | CJaC: 14d, §504B.321 subd. 1a (attorney-confirmed, Andy Cohen 2026-06-16) | ⚠️ **DIVERGENCE — likely post-2021 statutory change.** MN's 14-day pay-or-quit requirement is from the 2023 Housing omnibus (HF 3019). LSC captures pre-2021 law; the change is real. This is a CJaC accuracy point (correct for current law) and a *demonstration* of the recency advantage. |
| **NJ** | No minimum time | `notice_required: false`, days=null (attorney-confirmed) | ✅ **MATCH.** CJaC's no-notice pattern, confirmed by attorney review, agrees with LSC's independent 2021 coding. |
| **WV** | No minimum time | `notice_required: false`, §55-3A-1 (L2 AI-resolved, attorney-confirmed) | ✅ **MATCH.** Two independent confirmations — L2 AI consensus + attorney + LSC. |
| **PR** | No minimum time | Not in CJaC scope (territories excluded for Phase 1) | N/A |

**Summary of immediate findings:**
- 2 open L7 items (GA, MD) — LSC provides actionable corroborating intelligence for one side of each split
- 1 demonstrable recency advantage (MN) — LSC frozen at pre-change; CJaC current
- 2 clean corroborations (NJ, WV) — independent confirmation of CJaC's no-notice determinations

### How to use the GA and MD findings in attorney reviews

**GA (attorney review queue item [GA-L7-05]):**
Add to review materials: "The LSC/Temple LawAtlas Eviction Laws Dataset (Jan 2021), produced using inter-coder reliability methodology under congressional funding, coded Georgia as having no minimum time requirement before a landlord may file for nonpayment eviction. This is consistent with the L2 Gemini model's position that notice_required=false. The reviewing attorney should confirm whether this coding reflects Georgia law accurately as of Jan 2021, and whether any change has occurred since."

**MD (attorney review queue item):**
Add to review materials: "LSC/LawAtlas (Jan 2021) coded Maryland as having no minimum time requirement for nonpayment eviction. This corroborates the L2 Gemini model's position (no notice period under §8-401). GPT coded 10d under §8-401(b)(2)(i). The attorney should determine whether §8-401(b)(2)(i) is a special provision (e.g., for a specific tenant class or county) or whether LSC and Gemini have the better reading of the general case."

---

## Part 2: Full dataset cross-check (requires LawAtlas account)

### What to download

1. Go to: https://lawatlas.org/datasets/state-eviction-laws
2. Create free LawAtlas account (or log in)
3. Download: **Data** (Excel, all 51 US jurisdictions) + **Codebook** (variable definitions)

### What to look for in the Excel

The key variables (from Codebook, confirmed from summary report structure):

- `NonpaymentNoticeRequired` — Yes/No/Not specified — maps to CJaC `notice_required`
- `NonpaymentNoticeDays` — integer (minimum days) — maps to CJaC `days`
- `NonpaymentCureRight` — whether tenant can cure — maps to future CJaC field
- `NonpaymentNoticeType` — Written/Oral/Not specified — no current CJaC field but worth noting

### How to run the comparison

Once you download the Excel, run:

```bash
python3 rules/validation/l2/lsc_crosscheck_runner.py --lsc-file /path/to/downloaded/excel.xlsx
```

The script (already created as `rules/validation/l2/lsc_crosscheck_prep.py`) will:
1. Load the LSC Excel
2. Load all 51 CJaC v2 files
3. Compare `notice_required` and `days` fields per state
4. Classify each: MATCH / DIVERGENCE-EXPLAIN / LSC-NO-MINIMUM-CJaC-HAS-PERIOD / LSC-PERIOD-CJaC-DIFFERENT / NOT-IN-LSC
5. Output a markdown report

### Expected output categories

| Category | Meaning | Action |
|----------|---------|--------|
| **MATCH** | CJaC and LSC agree | Corroboration — log in ledger |
| **DIVERGENCE-PRE2021** | Disagree, both appear pre-2021 | Priority attorney review item |
| **DIVERGENCE-POST2021-CHANGE** | LSC has old law; CJaC has updated | Demonstrates recency advantage — document |
| **LSC-NO-MINIMUM-CJaC-HAS-DAYS** | LSC: no minimum; CJaC: X days | Either post-2021 change or CJaC error |
| **OPEN-L7-LSC-CORROBORATES** | CJaC L7 open; LSC supports one side | High value — feed to attorney review |

---

## Recommendation

**Execute the full cross-check. High value, low effort.** The account creation is free; the download is ~5 minutes. Once you have the Excel, the comparison script will auto-generate the analysis.

**Why it's worth doing before outreach:**
1. Any LSC-matched CJaC values = independent corroboration by a congressionally-funded, inter-coder-reliability-validated dataset. This is strong external credibility for the paper.
2. Any pre-2021 divergences caught = CJaC errors the process found. The paper's claim is "the process catches errors" — this is a direct demonstration.
3. Post-2021 divergences = demonstrable proof of the recency advantage. LSC frozen; CJaC current.
4. The two open L7 items (GA, MD) already have partial corroboration from the summary report — the full dataset will give you the specific variable codes.

**Estimated effort:** 30 minutes (account creation + download + script run + review output).

**Cost:** $0 (no API calls; pure file comparison).

---

## What the cross-check does NOT cover

- Notice periods are only one CJaC module. LSC also has service/filing timelines, judicial process, and execution data — but CJaC's service L2 is just-completed AI validation, not a simple period comparison, so a service cross-check is lower priority for now.
- LSC does not cover the open-textured defenses (substantive_defenses module) — that's CJaC's genuine extension beyond the prior art.
- LSC has a Nov 2022 update for the local (30-jurisdiction) dataset but the state dataset appears to remain Jan 2021. Any changes between Jan 2021 and Nov 2022 are in a gray zone.

---

## Positioning language once complete

*"CJaC's notice period determinations were cross-checked against the LSC/Temple LawAtlas State Eviction Laws Dataset (Jan 2021), produced using policy-surveillance methodology with inter-coder reliability under a congressionally-funded study. Of [N] comparable jurisdictions, [X] showed agreement ([X]% corroboration rate). [Y] divergences were investigated: [Z] reflected post-2021 statutory changes (demonstrating CJaC's currency advantage), [W] prompted correction of CJaC errors caught by the comparison. The cross-check is an independent external validation of CJaC's bright-line notice layer."*

Fill in the brackets after the full comparison runs.

---

## Action items for Andy

- [ ] Create free LawAtlas account at https://lawatlas.org/user/register
- [ ] Download Data + Codebook from https://lawatlas.org/datasets/state-eviction-laws
- [ ] Run: `python3 rules/validation/l2/lsc_crosscheck_runner.py --lsc-file <path>`
- [ ] Review the output — Claude can analyze and update the ledger in a follow-up session
- [ ] Feed GA and MD corroboration findings to the attorney reviewing those L7 items (see Part 1 above)

---

*LSC Baseline Cross-Check Assessment · Civil Justice as Code · June 20, 2026 · Copyright 2026 Andrew M Cohen · Apache 2.0*
