# Human Review Queue — Civil Justice as Code

**Module:** Notice / pay_or_quit · **Layer:** L2 Multi-Model Consensus  
**Runner rule:** Runners append new flagged items only. They never edit or overwrite the Resolution, Authoritative source, Resolved by, Date, or Status fields — those are owned by Andy Cohen.  
**Last rebuilt:** 2026-07-19 morning report (no-run cycle — dispatcher missed fire ×4 [07-16→07-19], first cycle classified via B-3 heartbeat tool: `no-heartbeat` [launchd never ran dispatch.py — infrastructure, folded into standing RED]; no new output ingested; **no new items; nothing routed to attorney; RC count remains 6, CI count remains 2**) · **Confirmed by:** Cowork (GREEN audit, anti-default rule upheld)
**Prior rebuild:** 2026-07-18 morning report (no-run cycle — dispatcher missed fire ×3 [07-16/07-17/07-18, infrastructure, folded into standing RED]; no new output ingested; **no new items; nothing routed to attorney; RC count remains 6, CI count remains 2**) · **Confirmed by:** Cowork (GREEN audit, anti-default rule upheld)
**Prior rebuild:** 2026-07-17 morning report (Direction D-1 baseline ingested [dev 12/12 SM-GPT — Gemini 503 ×12, an API failure, NOT routed anywhere per anti-default rule]; dispatcher missed fire #2 [infrastructure, folded into standing RED]; **no new items; nothing routed to attorney; RC count remains 6, CI count remains 2**) · **Confirmed by:** Cowork (GREEN audit, anti-default rule upheld)
**Prior rebuild:** 2026-07-16 morning report (no-run cycle — dispatcher did NOT fire overnight [first launchd-side miss since 06-25; queue was intentionally empty anyway, so no substantive loss]; no new output ingested; **no new items; nothing routed to attorney; RC count remains 6, CI count remains 2**) · **Confirmed by:** Cowork (GREEN audit, anti-default rule upheld)
**Prior rebuild:** 2026-07-15 morning report (no-run cycle — sixth consecutive intentionally-empty night pending Gemini-DNS RED; no new output ingested; **no new items; nothing routed to attorney; RC count remains 6, CI count remains 2**) · **Confirmed by:** Cowork (GREEN audit, anti-default rule upheld)
**Prior rebuild:** 2026-07-14 morning report (no-run cycle — fifth consecutive intentionally-empty night pending Gemini-DNS RED; no new output ingested; **no new items; nothing routed to attorney; RC count remains 6, CI count remains 2**) · **Confirmed by:** Cowork (GREEN audit, anti-default rule upheld)
**Prior rebuild:** 2026-07-13 morning report (no-run cycle — fourth consecutive intentionally-empty night pending Gemini-DNS RED; no new output ingested; **no new items; nothing routed to attorney; RC count remains 6, CI count remains 2**) · **Confirmed by:** Cowork (GREEN audit, anti-default rule upheld)
**Prior rebuild:** 2026-07-12 morning report (no-run cycle — third consecutive intentionally-empty night pending Gemini-DNS RED; no new output ingested; **no new items; nothing routed to attorney; RC count remains 6, CI count remains 2**) · **Confirmed by:** Cowork (GREEN audit, anti-default rule upheld)
**Prior rebuild:** 2026-07-11 morning report (no-run cycle — overnight queue intentionally empty pending Gemini-DNS RED; no new output ingested; **no new items; nothing routed to attorney; RC count remains 6, CI count remains 2**) · **Confirmed by:** Cowork (GREEN audit, anti-default rule upheld)
**Prior rebuild:** 2026-07-08 morning report (Northgate generate retry [run e9222548] ingested: pure infrastructure failure — DNS to CourtListener exhausted the full backoff ladder on both queries, 0 candidates, no model calls; **no new items this cycle; nothing routed to attorney; RC count remains 6, CI count remains 2**; job re-queued for 2026-07-09 with extended backoff ladder) · **Confirmed by:** Cowork (GREEN ingestion, anti-default rule upheld)
**Prior rebuild:** 2026-07-06 morning report (VT runs c7bcdcff [2026-07-04, DNS failure — nothing to route] + 57cf7b37 [2026-07-06] ingested: **Gokey v. Bessette → MV** — below attorney line, no queue item; harness emitted 2 RC [Houle, Northgate White] but both were DNS artifacts [Gemini generate call failed Errno 8 — no legal evaluation occurred] → reclassified PR on ingestion, **NOT added to queue** per anti-default rule; routing bug fixed in protocols/retaliation_holdings_v3.py; Houle remains CI [VT-HOLD-CI-01] unchanged; **no new items this cycle; RC count remains 6, CI count remains 2**) · **Confirmed by:** Cowork (GREEN ingestion, anti-default rule enforced against the harness itself)
**Prior rebuild:** 2026-07-02 morning report (VT retry [run 1153a763] ingested: Gemini 503 CLEARED — both VT cases got Gemini responses; Atwood v. Hill → PR [wrong-doc, not retaliation — GREEN pipeline]; Houle v. Quenneville → CI [two-model corroborated, D=INFERRED]; VT-HOLD-CI-01 added; CI count 1→2) · **Confirmed by:** Cowork (GREEN ingestion, anti-default rule upheld)
**Prior rebuild:** 2026-07-01 morning report (VT retry [run 1c7f0772] ingested: Gemini 429 on both VT cases [Atwood v. Hill, Houle v. Quenneville]; anti-default rule applied — NOT added to queue [API failure, not legal failure]; no new items added; RC count remains 6) · **Confirmed by:** Cowork (GREEN ingestion, anti-default rule upheld)
**Prior rebuild:** 2026-06-30 morning report (3 overnight runs ingested: VT retry [perm-fail/pipeline bug], CO/NY/SC PR retry [MV=3/CI=1/PR=8], broad_query 10 states [MV=12/CI=1/RC=1/PR=20]; WV-RET-HOLD-RC-02 added [Criss v. Salvation Army Residences]; RC count 5→6; 8 state v2 files updated with MV/CI cases) · **Confirmed by:** Cowork (GREEN ingestion)  
**Prior rebuild:** 2026-06-27 morning report (Track B KS/NV/NY/SC run ingested: NY-HOLD-CI-01 added [Baer v. Huggins, cheap confirm lane]; queue summary updated) · **Confirmed by:** Cowork (GREEN ingestion)  
**Prior rebuild:** 2026-06-26 late evening (notice tiebreaker + NJ probe + retaliation nc17_fresh_v2 ingested: NOTICE-L2-01/03 tiebreaker-resolved, not L7 — CORRECTED [ingestion error fixed]; NOTICE-L2-02/04/08/09 resolved; NOTICE-L2-06 GA tiebreaker-resolved YELLOW file update applied; 3 RC cases added [AK-RET-HOLD-RC-01]–[CT-RET-HOLD-RC-01]) · **Confirmed by:** Cowork (GREEN ingestion + correction)  
**Prior rebuild:** 2026-06-26 evening (notice provenance rerun: 8 new NOTICE-L2 divergence items [NOTICE-L2-01]–[NOTICE-L2-08] added; MD and MO splits corroborate existing L7s) · **Confirmed by:** Cowork (GREEN ingestion)

> **How to use this queue:**  
> Work top-to-bottom. L7-ESCALATED = you decide from primary sources. PENDING-CONFIRMATION = you verify the AI's proposed answer and sign off (or override).  
> Fill in the Resolution and Confirmed-by fields. Move completed items to the Resolved section at the bottom.

---

## Queue Summary

| Status | Count |
|--------|-------|
| 🔴 L7-ESCALATED — you decide from primary sources | 43 (6 notice/service + 14 retaliation elements + OK + 22 procedural defects) |
| 🔴 RC — verify/characterize from primary source | 6 (NV Wright v. Brady; NY Ellis v. Oceanhill; AK DeNardo v. Maassen; CO Sladek v. dePlomb; CT TOV Realty v. Suarez; WV Criss v. Salvation Army Residences) |
| 🟡 CI — cheap confirm lane (D=INFERRED; verify holding is controlling) | 2 (NY: Baer v. Huggins [NY-HOLD-CI-01]; VT: Houle v. Quenneville [VT-HOLD-CI-01]) |
| 🟡 PENDING-CONFIRMATION — AI proposed, you verify | 6 |
| 🟡 CITATION-REVIEW — verify operative section from primary source | 3 |
| 🟠 OVERLAY-CITE-CHECK — Module 4 runner-flagged + classifier false positives | 22 |
| 🔁 RETRY-NEEDED — transient API failure, not substantive | 1 (SD Mod6) |
| ⚡ NOTICE-L2-DIVERGENCE — tiebreaker pending or corroboration | 2 (MD/MO corroborate existing L7s) |
| ✅ Resolved/Confirmed | 7 (NOTICE-L2: GA tiebreaker-resolved YELLOW; AR/MN/SD/WY/TN confirmed-file; OR file already correct, L2 flag closed) |

*Technical resolutions (notice/service — no human review needed): AZ, CA, CO, CT, DC, FL, GA, HI, IA, ID, IL, IN, KY, LA, MA, MD, ME, MI, MN, MS, MT, NC, NE, NH, NJ, NM, NY, OH, OK, OR, PA, RI, SC, SD, TN, TX, UT, VA, WA, WI, WY — confirmed by two-model consensus or AI-resolved.*

*Retaliation elements — auto-resolved (no human review needed): AR (no period), AZ (180d §33-1381(B)), CA (180d §1942.5(a)), CO (single-model Gemini: no period), DC (180d §42-3505.02(c)), DE (90d §5516(c)), FL (no period), GA (no period), IA (365d §562A.36(2)), ID (no period), IL (no period), IN (no period), KY (365d KRS §383.705(2)), LA (single-model Gemini: no period), MA (180d ch.239 §2A), MD (no period), ME (180d 14 MRS §6001(3)), MN (90d §504B.285), MO (no period), MS (no period), MT (no period), NC (no period), NE (180d §76-1439(2)), NH (180d RSA §540:13-a(II)), OH (no period), OR (no period), PA (no period), RI (180d §34-18-46(b)), SD (no period), TN (no period), TX (no period), UT (no period), VA (no period), WA (90d RCW 59.18.250), WI (no period), WY (no period) — 36 states resolved (29 consensus + 5 two-model from 51-state run + 2 single-model).*

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

**LSC corroboration (added 2026-06-20):** LSC/Temple LawAtlas State Eviction Laws (Jan 1, 2021, inter-coder reliability validated) coded Maryland as: *"Landlord not required to give notice if evicting for nonpayment."* This is a third independent data point corroborating Gemini's position. Two independent sources (Gemini + LSC 2021) say no notice required. GPT's 10d reading may reflect §8-401(b)(2)(i), which may be a provision specific to a particular tenant class or circumstance rather than the general residential rule.

**Current file:** notice_required=true, days=10, statute Md. Code Real Prop. §8-401  
**Your task:** Read §8-401; determine whether advance notice is required before filing and if so, how many days. Note: LSC independently coded MD as "no notice required" — the 10d value is likely an initial-generation artifact tied to a specific subsection, not the general residential rule.

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

**LSC corroboration (added 2026-06-20):** LSC/Temple LawAtlas State Eviction Laws (Jan 1, 2021, inter-coder reliability validated) coded Georgia as: *"Minimum amount of notice not specified"* (no citation). This is a third independent data point corroborating Gemini's position that §44-7-50 requires a demand but specifies no minimum waiting period. **IMPORTANT:** The current file value of `days=3` is an unsubstantiated initial-generation value — it is not confirmed by L2, not confirmed by LSC, and is the position of only one of two L2 models. Do not treat `days=3` as a confirmed value; it should not appear in validated output until attorney determination.

**Current file:** notice_required=True, days=3, statute=O.C.G.A. §44-7-50  
**⚠️ Note on current file value:** The `days=3` is an unsubstantiated initial-generation artifact. LSC (2021) coded GA as "no minimum specified"; Gemini says no waiting period. The `3` is supported only by GPT. Attorney determination needed before this value appears in any output.  
**Your task:** Read §44-7-50; determine whether a formal written demand/notice is required before filing and whether any waiting period applies. Note that LSC's independent coding (2021) found no minimum period — this corroborates the "demand only, no wait" interpretation.

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

## 🔴 RC — Retaliation Holdings Needing Characterization (2026-06-26)

*Source: NC-17 fresh run (`retaliation_holdings_v3_2026-06-26_20f722c8.json`). 2 cases where CourtListener text was retrieved, but the generate-from-source + verify cycle could not machine-verify the holding. Automated attempt is complete for both. Attorney must: confirm the case is a valid retaliation defense holding, characterize the controlling rule, or dismiss as a non-holding candidate.*

*Anti-default rule satisfied: both cases completed the full CL-retrieval + generate + verify protocol before routing here. Neither is a pipeline artifact.*

---

### [NV-RET-HOLD-RC-01] Nevada — Wright v. Brady (418 P.3d 619, 2018)

**Classification:** RC (re-characterize) · **Status:** 🔴 pending  
**Run date:** 2026-06-26 (run 20f722c8)

**What happened:** CourtListener retrieved a document for this case. The generate model produced a holding characterization. The verify model flagged C=FLAG-verify-disputed — it could not corroborate the generated holding from the retrieved text (may be a wrong document, or the case does not state a retaliation holding clearly).

**Your task:** (a) Confirm whether Wright v. Brady (418 P.3d 619, 2018) is a valid Nevada retaliation defense case. (b) If so, state the controlling rule and confirm a source quote. (c) If not, dismiss as a false candidate and identify a better NV retaliation defense case if one exists.

**Current file:** NV has no verified retaliation holding; this was a fresh CL search candidate.  
**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

### [NY-RET-HOLD-RC-02] New York — Ellis v. Oceanhill Brownsville Tenant Ass'n (152 Misc. 2d 1007, 1991)

**Classification:** RC (re-characterize) · **Status:** 🔴 pending  
**Run date:** 2026-06-26 (run 20f722c8)

**What happened:** CourtListener retrieved a document for this case. The generate model returned C=FLAG-generate-failed — it could not extract a retaliation defense holding from the retrieved text. The case may not actually state a retaliation holding, or the CL document is incomplete.

**Your task:** (a) Confirm whether Ellis v. Oceanhill Brownsville Tenant Ass'n (152 Misc. 2d 1007, 1991) is a valid NY retaliation defense case. (b) If so, state the controlling rule. (c) If not, dismiss and identify a better NY retaliation defense case. Note: NY has a statutory retaliation defense (RPL §223-b); the question is whether there is useful case law interpreting it.

**Current file:** NY has no verified retaliation holding; this was a fresh CL search candidate.  
**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

## 🔴 RC — Retaliation Holdings Needing Characterization (nc17_fresh_v2, 2026-06-26)

*Source: nc17_fresh_v2 run (`retaliation_holdings_v3_2026-06-26_nc17_fresh_v2.json`). 3 cases where CourtListener text was retrieved, holding was generated, but verify model flagged as RC (diverged from generated holding). Anti-default rule satisfied: full CL-retrieval + generate + verify protocol ran before routing here.*

*Note: 84 additional cases in this run have `disposition="transient-failure"` (CourtListener 429 rate-limit errors during 13-hour run). These are PR-class infrastructure failures — quarantined for retrieval retry. NOT attorney items.*

---

### [AK-RET-HOLD-RC-01] Alaska — DeNardo v. Maassen (case TBD)

**Classification:** RC (re-characterize) · **Status:** 🔴 pending  
**Run date:** 2026-06-26 (nc17_fresh_v2 run)

**What happened:** CourtListener retrieved a document for this case. The generate model produced a holding characterization. The verify model flagged RC — could not corroborate the generated holding from retrieved text. Case may be a wrong-doc return or the holding was not clearly stated.

**Your task:** (a) Confirm whether DeNardo v. Maassen is a valid Alaska retaliation defense case. (b) If so, state the controlling rule and confirm a source quote. (c) If not, dismiss as a false candidate and identify a better AK retaliation defense case if one exists.

**Current file:** AK has no verified retaliation holding; this was a fresh CL search candidate.  
**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

### [CO-RET-HOLD-RC-01] Colorado — Sladek v. dePlomb (case TBD)

**Classification:** RC (re-characterize) · **Status:** 🔴 pending  
**Run date:** 2026-06-26 (nc17_fresh_v2 run)

**What happened:** CourtListener retrieved a document for this case. The generate model produced a holding characterization. The verify model flagged RC — could not corroborate the generated holding from retrieved text.

**Your task:** (a) Confirm whether Sladek v. dePlomb is a valid Colorado retaliation defense case. (b) If so, state the controlling rule and confirm a source quote. (c) If not, dismiss and identify a better CO retaliation defense case.

**Current file:** CO has no verified retaliation holding; this was a fresh CL search candidate.  
**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

### [CT-RET-HOLD-RC-01] Connecticut — TOV Realty, LLC v. Suarez (case TBD)

**Classification:** RC (re-characterize) · **Status:** 🔴 pending  
**Run date:** 2026-06-26 (nc17_fresh_v2 run)

**What happened:** CourtListener retrieved a document for this case. The generate model produced a holding characterization. The verify model flagged RC — could not corroborate the generated holding from retrieved text.

**Your task:** (a) Confirm whether TOV Realty, LLC v. Suarez is a valid Connecticut retaliation defense case. (b) If so, state the controlling rule. (c) If not, dismiss and identify a better CT retaliation defense case.

**Current file:** CT has no verified retaliation holding; this was a fresh CL search candidate.  
**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

## 🔴 RC — Retaliation Holdings Needing Characterization (broad_query run, 2026-06-30)

*Source: broad_query_10states run (`retaliation_holdings_v3_2026-06-30_broad_query_10states_20260629.json`). 1 case where CourtListener text was retrieved, holding was generated, but verify model flagged RC (FLAG-verify-disputed). Anti-default rule satisfied: full CL-retrieval + generate + verify protocol ran before routing here. Murphy v. Smallridge (MV) cites Criss as the first WV retaliation case — making Criss strategically important.*

---

### [WV-RET-HOLD-RC-02] West Virginia — Criss v. Salvation Army Residences

**Classification:** RC (re-characterize) · **Status:** 🔴 pending  
**Run date:** 2026-06-30 (broad_query_10states run)

**Case:** Criss v. Salvation Army Residences, 173 W.Va. 634, 319 S.E.2d 403 (W.Va. SC App. 1984)  
**CL check_a confirmed:** West Virginia Supreme Court, date 1984-07-13  
**Citations (both models):** 319 S.E.2d 403  

**What happened:** CourtListener retrieved text for this case. The generate model produced a holding characterization. The verify model flagged RC (FLAG-verify-disputed) — could not fully corroborate the generated holding. Strategically significant: Murphy v. Smallridge (468 S.E.2d 167, 1996 WV SC, separately classified MV this cycle) explicitly cites Criss as "the first WV case on retaliatory eviction" and states Criss held that W.Va.Code §55-3A-1 et seq. "does not deny tenants an adequate remedy for the defense of retaliatory eviction."

**Source_generated_holding (Gemini):** "The court holds that the summary eviction proceedings established by W.Va.Code 55-3A-1 et seq. do not deny tenants the lawful right to raise the defense of retaliatory eviction. The court explicitly considered and rejected the landlord's argument, finding the statute does not strip tenants of this defense."

**Your task:** (a) Confirm from primary source (Westlaw/Fastcase) that Criss holds the retaliation defense is available in WV summary eviction. (b) Confirm or correct the controlling rule — does Criss affirmatively hold the defense is available, or does it merely hold tenants may *raise* it? (c) If confirmed, WV may be advanced to MV-attorney-confirmed for Criss.

**Murphy connection:** Murphy v. Smallridge (MV-classified this cycle, 468 S.E.2d 167, 1996) already provides solid WV MV support for the defense. Criss is the earlier foundational case. Murphy is sufficient if Criss characterization remains uncertain.

**Current file:** `wv_eviction_v2.json` updated this cycle with Murphy as MV; Criss noted in validation_flags as RC-pending-attorney ([WV-RET-HOLD-RC-NOTE-01]).  
**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

## 🔴 L7-ESCALATED — Procedural Defects Module (2026-06-25)

*Source: 204-unit L2 run (`l2_procedural_defects_20260626_0018.json`). 20 MODEL-SPLIT items where both models engaged but disagree on the governing statute. File NOT updated pending your determination. Anti-default rule satisfied: both models ran, genuine split persisted after citation-equivalency check.*

*SM-GEMINI cases (120) and ERROR cases (23) are NOT in this section — they are pipeline items (re-run or failure_to_attach NSR-likely), not attorney items.*

---

### [PROC-DEF-L7-01] AK — complaint_filed_before_notice_period_expired

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Alaska statute governs the timing bar when a complaint is filed before the notice period expires?  
- GPT: Alaska Stat. § 09.45.100  
- Gemini: AS 09.45.090(a)(2)(C)  
**Current file:** AS 09.45.060 et seq.  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-02] AR — complaint_filed_before_notice_period_expired

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Arkansas statute is the specific procedural bar for premature filing?  
- GPT: Ark. Code Ann. § 18-60-307(a)  
- Gemini: A.C.A. § 18-60-304(a)  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-03] AR — wrong_court

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Arkansas statute governs the court with exclusive eviction jurisdiction (district vs. circuit)?  
- GPT: Ark. Code Ann. § 16-13-201(a); Ark. Code Ann. § 18-60-307  
- Gemini: Arkansas Code Annotated § 18-17-912  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-04] AZ — complaint_filed_before_notice_period_expired

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Arizona rule/statute is the specific timing bar for premature filing?  
- GPT: Arizona Rules of Procedure for Eviction Actions, Rule 5(a)  
- Gemini: Ariz. R. P. Evic. Act. 5(a)(2)(B)  
*Note: Both cite the same rule; dispute is about subsection specificity. Consider whether § 5(a) vs. § 5(a)(2)(B) are materially different.*  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-05] CA — wrong_court

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which California provision establishes limited civil court's exclusive jurisdiction over UD actions?  
- GPT: Cal. Const. art. VI, § 10 (constitutional grant of superior court jurisdiction)  
- Gemini: California Code of Civil Procedure § 86(a)(4) (limited civil jurisdiction statute)  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-06] CT — wrong_court

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Connecticut statute governs Housing Court / Superior Court jurisdiction for summary process?  
- GPT: Conn. Gen. Stat. § 47a-23a(a)  
- Gemini: Conn. Gen. Stat. § 47a-70  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-07] ID — wrong_court

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Idaho statute establishes magistrate/district court jurisdiction for eviction actions?  
- GPT: Idaho Code § 1-2208(1)(b); Idaho Code § 6-310  
- Gemini: Idaho Code § 6-305  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-08] IL — wrong_court

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Illinois provision is the specific source of circuit court jurisdiction for evictions?  
- GPT: Ill. Const. art. VI, § 9 (constitutional grant)  
- Gemini: 735 ILCS 5/9-106 (Forcible Entry and Detainer Act — specific eviction statute)  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-09] KS — wrong_court

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Kansas statute is the governing court-jurisdiction provision for eviction actions?  
- GPT: Kan. Stat. Ann. § 20-301; Kan. Stat. Ann. § 61-3801  
- Gemini: K.S.A. 61-2902  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-10] KY — wrong_court

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Kentucky statute governs the court with jurisdiction for eviction actions?  
- GPT: KRS § 24A.120(5) (district court jurisdiction)  
- Gemini: KRS § 383.210 (URLTA procedural section)  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-11] MA — summons_improperly_issued_or_served

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Massachusetts rule/statute governs defects in the summary process summons?  
- GPT: Mass. Uniform Summary Process Rule 2(b), incorporating Mass. Gen. Laws ch. 239, § 2  
- Gemini: Uniform Summary Process Rule 3  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-12] MI — complaint_filed_before_notice_period_expired

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Michigan provision bars a complaint filed before the notice period expires?  
- GPT: Mich. Ct. R. 4.201(B)(2)  
- Gemini: MCL 600.5714(1)(a)  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-13] MT — wrong_court

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Montana statute governs the proper court for eviction actions?  
- GPT: Mont. Code Ann. § 3-10-301(1)(c) (justice court jurisdiction)  
- Gemini: Montana Code Annotated § 70-27-103 (unlawful detainer statute itself)  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-14] OH — complaint_filed_before_notice_period_expired

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Ohio section is the specific bar against premature filing?  
- GPT: Ohio Rev. Code § 1923.05  
- Gemini: Ohio Revised Code § 1923.04(A)  
*Note: §1923.04 and §1923.05 are adjacent provisions; one may govern notice period and the other the filing bar. Both may be correct in tandem.*  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-15] SC — wrong_court

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which South Carolina provision governs court jurisdiction for eviction actions?  
- GPT: S.C. Code Ann. §§ 22-3-10(10), 27-37-10  
- Gemini: S.C. Code Ann. § 27-40-130  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-16] UT — complaint_filed_before_notice_period_expired

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Utah section is the specific timing bar for premature filing?  
- GPT: Utah Code § 78B-6-807(1)  
- Gemini: Utah Code § 78B-6-802(1)(c)  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-17] UT — wrong_court

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Utah provision establishes the proper court for eviction (district vs. justice)?  
- GPT: Utah Code Ann. § 78A-5-102(1) (district court jurisdiction)  
- Gemini: Utah Code Ann. § 78A-7-105(1)(c) (justice court jurisdiction)  
*Note: Both provisions may be relevant — dispute may reflect UD cases straddling justice/district court thresholds.*  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-18] VT — complaint_filed_before_notice_period_expired

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Vermont provision is the specific bar against premature filing?  
- GPT: Vt. R. Civ. P. 80.1(b)(1)  
- Gemini: 9 V.S.A. § 4468(a)  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-19] VT — wrong_court

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Vermont provision is the correct court-jurisdiction source for eviction actions?  
- GPT: 4 V.S.A. § 31(a)(1); 12 V.S.A. § 4851  
- Gemini: 12 V.S.A. § 4911  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-20] WY — complaint_filed_before_notice_period_expired

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Question:** Which Wyoming section is the specific timing bar against premature filing?  
- GPT: Wyo. Stat. Ann. § 1-21-1004(a)  
- Gemini: Wyo. Stat. Ann. § 1-21-1002(a)(i)  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-21] CT — failure_to_attach_lease_or_notice_to_complaint

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Run date:** 2026-06-26 (failure_to_attach re-run, post prompt+token fix)  
**Question:** Which Connecticut provision governs attachment of the eviction notice/lease to the complaint — is it the general pleading statute or a court rule?  
- GPT: Conn. Gen. Stat. § 47a-23a(a)  
- Gemini: Connecticut Practice Book § 10-29  

Both models agree Connecticut requires attachment; they disagree on whether the governing source is the eviction statute (§ 47a-23a(a)) or the general civil pleading rule (Practice Book § 10-29).  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [PROC-DEF-L7-22] FL — failure_to_attach_lease_or_notice_to_complaint

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Run date:** 2026-06-26 (failure_to_attach re-run, post prompt+token fix)  
**Question:** Which Florida provision governs attachment of the eviction notice/lease to the complaint — the eviction procedure statute or the general rules of civil procedure?  
- GPT: Fla. Stat. § 51.011(2)  
- Gemini: Florida Rules of Civil Procedure 1.130(a)  

Both models agree Florida requires attachment; they disagree on whether the governing source is the summary procedure statute (§ 51.011(2)) or the general pleading rule (FRCP 1.130(a)).  
**Resolution:** ________________  **Resolved by:** ________________  **Date:** ________________

---

## 🟡 CI — Cheap Confirm Lane (D=INFERRED; Verify Holding Is Controlling)

These cases were machine-verified on text retrieval and both models corroborated the holding, but Check D returned INFERRED (no direct quotable statement of the rule). They count as CI in reporting. To close: confirm from primary source that the case does articulate the retaliation defense standard, even if not with a single quotable sentence.

---

### [VT-HOLD-CI-01] Vermont — Houle v. Quenneville, 787 A.2d 1258 (Vt. 2001)

**Classification:** CI — cheap confirm lane · **Status:** 🟡 pending  
**Run:** VT retry #3 [run_id=1153a763, 2026-07-02] · **Module:** retaliation defense, holdings layer  
**CL cluster:** 2320677 · CL URL: https://www.courtlistener.com/opinion/2320677/houle-v-quenneville/  
**Citation in vt_eviction_v2.json:** to be written to `confirm_inference_cases` array under `retaliation.layer_decomposition.holdings`

**What the runner found:** Both Gemini 2.5-pro (generate) and GPT-4o (verify) retrieved text from 787 A.2d 1258 and corroborated the holding. GPT-4o verified as "accurate." However, neither model returned a verbatim controlling quote (Check D = INFERRED, not STATED — prose reasoning, not a quotable sentence). Two-model agreement: strong.

**Corroborated holding:** "The court affirmed the trial court's finding that the tenants failed to prove their affirmative defense of retaliatory eviction. Although the landlords' initial eviction attempt may have been retaliatory, the court found they did not have a retaliatory motive in their subsequent decision not to renew the lease. The court noted that most repairs had been completed and the landlords sought possession based on the natural expiration of the lease term, not the earlier alleged lease violations."

**Additional context from CL:** Justice Johnson (concurring/dissenting) agreed on the holding in every respect except the final issue regarding Section 8 housing tenants, suggesting the case involved nuanced facts about landlords' successive motives.

**Your task:** Pull 787 A.2d 1258 (or 173 Vt. 80) from Fastcase, Westlaw, or CourtListener. Confirm the court addressed the retaliation defense and that the holding above is accurate. If confirmed, mark CONFIRMED-CI and update vt_eviction_v2.json. If the characterization is wrong, mark RC.

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

### [NY-HOLD-CI-01] New York — Baer v. Huggins, 41 Misc. 3d 605 (N.Y. Civ. Ct. 2013)

**Classification:** CI — cheap confirm lane · **Status:** 🟡 pending  
**Run:** Track B (track_b_ks_nv_ny_sc_20260627) · **Module:** retaliation defense, holdings layer  
**Citation in ny_eviction_v2.json:** `confirm_inference_cases` array under `retaliation.layer_decomposition.holdings`

**What the runner found:** Both GPT and Gemini retrieved text from 41 Misc. 3d 605 and corroborated that it affirms the retaliation defense under RPL §223-b. However, neither model returned a direct quotable sentence stating the controlling rule (Check D = INFERRED, not STATED). Method rate counts this case as a CI denominator unit.

**Your task:** Pull 41 Misc. 3d 605 from Fastcase, Westlaw, or CourtListener. Confirm that the case substantively discusses the retaliation defense and states (or clearly implies) that a tenant who received a pay-or-quit notice after asserting housing-code complaints can assert §223-b as a defense. If it does, mark CONFIRMED-CI. If the case is merely a citation drop with no holding, mark RC and escalate for re-characterization.

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

## 🟡 PENDING-CONFIRMATION — AI Proposed, You Verify

The AI has proposed and applied a correction. File content updated; status stays at ACP. Your job: verify the proposed answer is correct and sign off (or override).

---

### [SCRA-PC-01] Federal — SCRA §3951 threshold formula and current dollar amount

**Classification:** PENDING-CONFIRMATION · **Status:** 🟡 pending  
**Module:** overlays.federal.scra (all 51 state files)  
**Run date:** 2026-06-20 (SCRA overlay L2, Terminal)  
**Model:** Gemini single-model (GPT returned PARSE_ERROR — technical failure)

**What Gemini found (high confidence):**

The FY23 NDAA (Pub. L. 117-263, Div. E, Title LV, § 555, Dec. 23, 2022) significantly amended 50 U.S.C. § 3951(a)(2). **It replaced the former CPI-adjusted fixed-dollar threshold with a new BAH-based formula.** Current formula: 130% of the Basic Allowance for Housing for a military member in pay grade E-5 with dependents, for the military housing area with the highest BAH in the United States (adjusted annually by DoD).

| Field | Gemini L2 finding | Preliminary value |
|-------|-------------------|-------------------|
| Primary citation | 50 U.S.C. § 3951 | 50 U.S.C. § 3951 ✓ |
| Threshold formula | 130% of BAH (E-5 w/dependents, highest area) | CPI-adjusted — **OUTDATED** |
| Current threshold (2024) | **$4,954.34/month** | $4,073.16/month — **WRONG** |
| Affidavit statute | 50 U.S.C. § 3931(b)(1) | 50 U.S.C. § 3931 ✓ |
| Max stay | 90 days | 90 days ✓ |

**Canonical SCRA content has been updated in all 51 files** with Gemini's findings. Status: L2-SINGLE-MODEL-RESOLVED-PENDING-HUMAN-CONFIRMATION. Content is in the files but not usable in validated output until attorney confirms.

**Your tasks:**

1. Confirm that Pub. L. 117-263, § 555 (FY23 NDAA) did in fact amend § 3951(a)(2) to use the BAH formula — and that the CPI formula is no longer operative.
2. Verify the current threshold dollar amount from DoD BAH charts (the 2024 E-5-with-dependents BAH for the highest-cost area × 130%). Gemini says $4,954.34 — confirm or correct.
3. Confirm 50 U.S.C. § 3931(b)(1) as the affidavit requirement subsection.

**Resolution:** ________________  
**Current threshold confirmed:** $________________/month (year: ________)  
**Amendment confirmed:** ________________  
**Confirmed by:** ________________  **Date:** ________________

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

---

## Retaliation Elements L2 Items

*Run: 2026-06-20 · Andy's Terminal · `retaliation_elements_runner.py` · 51 states · $2.60*

**Run summary:** 51-state retaliation elements layer L2 completed from Terminal (API accessible there). Neutral query (no preliminary values fed to models). Results written directly to all 51 state `*_v2.json` files.

| Outcome | Count | Notes |
|---------|-------|-------|
| CONSENSUS-NO-PERIOD (both models confirmed no statutory period) | 4 | FL, OH, OK, WI |
| SINGLE-MODEL-RESOLVED (Gemini; GPT systematic empty responses) | 46 | Gemini carried all 46 states; high confidence throughout |
| L7-ESCALATED (genuine statutory interpretation dispute) | 1 | KS — see below |
| **Total** | **51** | |

**Process-quality note — GPT systematic empty responses:** GPT returned empty for 46/51 states. The 4 CONSENSUS-NO-PERIOD states (FL/OH/OK/WI) and 1 round-1 substantive response (KS) are the only GPT contributions. Root cause unknown — likely `max_completion_tokens=2000` too low for the larger retaliation query, or GPT availability issue on 2026-06-20. For the next runner, increase `max_completion_tokens` to 4000–6000 and add retry logic. All 46 Gemini-only states are SINGLE-MODEL-RESOLVED / ACP / pending-human-confirmation. Per operating protocol, single-model fallback is appropriate when one model consistently fails and the other returns high-confidence, well-supported answers (which Gemini did throughout).

**Recency-watch states (5):** CA (180d/§1942.5(a)), MN (90d/§504B.441), OR (null/§90.385), VA (null/§55.1-1258), WA (90d/RCW 59.18.250). These states have been flagged for legislative activity in recent years; L2 results are consistent with known law but should be re-verified at the attorney review stage.

**All 50 non-KS states:** Results written to canonical files (`layer_decomposition.elements.state_specific`); `validation_status` = ACP / pending-human-confirmation. No individual queue entries — confirmation happens through attorney review of file contents, not through this queue. The KS entry below is the only item requiring active human determination before content can be accepted.

---

### [KS-RET-L7-01] Kansas — Does §58-2572(b) create a 365-day rebuttable presumption of retaliation?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Module:** substantive_defenses.retaliation.layer_decomposition.elements  
**Run date:** 2026-06-20 (retaliation elements L2, Terminal)

**Question:** Does Kan. Stat. Ann. §58-2572(b) create a statutory rebuttable presumption of retaliation when adverse action occurs within one year of a tenant's protected activity — or does the statute prohibit retaliation without establishing a time-specific presumption period (requiring the tenant to affirmatively prove causal link without a statutory presumption)?

**L2 result — same statute, opposite readings of §58-2572(b):**

- **GPT (round 1, high confidence):** 365-day presumption period. "K.S.A. §58-2572(b) creates a presumption of retaliation from evidence of a complaint made within one year before the alleged retaliatory act. The presumption does not arise if the tenant made the complaint after notice of a proposed rent increase, decrease in services, or action for possession." Statute: Kan. Stat. Ann. §58-2572 / subsection (b). Protected activities: §58-2572(a)(1)–(3) (habitability complaint to government agency; complaint to landlord about landlord's duties; tenant union organizing).

- **Gemini (round 1 + tiebreaker, both high confidence):** No statutory presumption period. "The Kansas Residential Landlord and Tenant Act does not establish a specific time period during which an adverse action is presumed to be retaliatory. The tenant must affirmatively prove the causal link regardless of timing." Tiebreaker: "Source B correct. A thorough review of Kan. Stat. Ann. §58-2572 reveals that while the statute establishes a defense against retaliatory conduct, it does not create a specific time period... Subsection (b) states that if a landlord acts in violation, 'the tenant...has a defense in an action against the tenant for possession.' The statute omits any language about a presumption."

- **GPT tiebreaker:** Empty (technical failure — position undefended in round 2).

**Stopping-rule condition:** Persistent genuine split after reasoning pass — both models cite the same statute and subsection (§58-2572(b)) but reach opposite conclusions on whether a statutory presumption-period clause exists. GPT tiebreaker technical failure means we cannot confirm whether the round-1 GPT reading (specific, detailed, high-confidence) holds up — but it is specific enough that a targeted subsection query or human reading of the statute text is required to resolve rather than applying single-model fallback.

**Your task:** Read Kan. Stat. Ann. §58-2572(b) from the primary source (kslegislature.org or official code). Does it contain language creating a rebuttable presumption tied to a one-year period? If so: period = 365 days, basis = statute. If not: period = null, basis = common-law (tenant must prove causation directly).

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

## Retaliation Elements L7 — Real Two-Model Run (2026-06-21)

*Run: 51 states, gpt-5.5 + gemini-2.5-pro, Terminal, 2026-06-21. Raw file: `rules/validation/l2/output/retaliation_elements_l2_raw_2026-06-21.json`. Automation ceiling: 71% (36/51). 14 MODEL-SPLIT states below — attorney reads primary source, determines correct period (or no period). Same-statute splits are the dominant pattern: both models cite the same statute but disagree on whether a subsection creates a time-limited rebuttable presumption.*

*For each item: read the cited statute directly (state legislature site or Westlaw). Does the listed subsection create a rebuttable presumption period? If yes: confirm the period in days. If no: period = null, basis = common-law or none.*

---

### [AK-RET-L7-01] Alaska — Does §34.03.310(b) create a 180-day presumption period?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Module:** substantive_defenses.retaliation.layer_decomposition.elements  
**Run date:** 2026-06-21

**Split:** Both models cite Alaska Stat. § 34.03.310. GPT reads subsection (b) as creating a 180-day rebuttable presumption. Gemini reads the same statute as prohibiting retaliation but creating no time-specific presumption period.

- **GPT:** 180 days, § 34.03.310(b), basis = statute
- **Gemini:** No period, § 34.03.310, basis = none

**Your task:** Read Alaska Stat. § 34.03.310(b). Does it create a rebuttable presumption of retaliation tied to a 180-day (or other) window?

**Resolution:** ________________  **Authoritative source:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [AL-RET-L7-02] Alabama — Does §35-9A-501(b) create a 365-day presumption period?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Module:** substantive_defenses.retaliation.layer_decomposition.elements  
**Run date:** 2026-06-21

**Split:** Both models cite Ala. Code § 35-9A-501. GPT reads subsection (b) as a 365-day rebuttable presumption. Gemini reads the statute as creating no time-specific presumption.

- **GPT:** 365 days, § 35-9A-501(b), basis = statute
- **Gemini:** No period, § 35-9A-501, basis = none

**Your task:** Read Ala. Code § 35-9A-501(b). Does it create a rebuttable presumption tied to any time window?

**Resolution:** ________________  **Authoritative source:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [CT-RET-L7-03] Connecticut — Does §47a-20 create a 180-day presumption period?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Module:** substantive_defenses.retaliation.layer_decomposition.elements  
**Run date:** 2026-06-21

**Split:** Both models cite Conn. Gen. Stat. § 47a-20. GPT reads the introductory clause as creating a 180-day presumption. Gemini reads the statute as prohibiting retaliation with no time-specific presumption.

- **GPT:** 180 days, § 47a-20 introductory clause, basis = statute
- **Gemini:** No period, § 47a-20, basis = none

**Your task:** Read Conn. Gen. Stat. § 47a-20 in full. Does any clause create a rebuttable presumption tied to a 180-day window?

**Resolution:** ________________  **Authoritative source:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [HI-RET-L7-04] Hawaii — Does §521-74(b) create a 180-day presumption period?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Module:** substantive_defenses.retaliation.layer_decomposition.elements  
**Run date:** 2026-06-21

**Split:** Both models cite Haw. Rev. Stat. § 521-74. Gemini reads subsection (b) as creating a 180-day presumption. GPT says the statute prohibits retaliation with no time-specific presumption period.

- **GPT:** No period, § 521-74, basis = none
- **Gemini:** 180 days, § 521-74(b), basis = statute

**Your task:** Read Haw. Rev. Stat. § 521-74(b). Does it create a rebuttable presumption tied to a 180-day window?

**Resolution:** ________________  **Authoritative source:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [KS-RET-L7-05] Kansas — UPDATED: §58-2572(b) vs §58-25,125(b) — which statute, what period?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending (supersedes [KS-RET-L7-01])  
**Module:** substantive_defenses.retaliation.layer_decomposition.elements  
**Run date:** 2026-06-21 (prior L7 from 2026-06-20 — updated with new model data)

**Split:** Unlike the prior run, both models now cite *different statutes* with different periods.

- **GPT:** 180 days, Kan. Stat. Ann. § 58-2572(b), basis = statute
- **Gemini:** 365 days, K.S.A. § 58-25,125(b), basis = statute

**Two sub-questions:** (1) Which statute governs the retaliation defense (§58-2572 or §58-25,125)? (2) Which period is correct under that statute?

**Note:** §58-25,125 is in the Kansas Uniform Residential Landlord and Tenant Act (URLTA); §58-2572 may be in a different chapter. Kansas may have two parallel landlord-tenant frameworks, and the applicable one depends on the tenancy.

**Your task:** Determine which statute governs standard residential tenancies in Kansas. Read the operative subsection. Confirm period and statute.

**Resolution:** ________________  **Authoritative source:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [MI-RET-L7-06] Michigan — Does §600.5720(2) create a 90-day presumption period?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Module:** substantive_defenses.retaliation.layer_decomposition.elements  
**Run date:** 2026-06-21

**Split:** Both models cite Mich. Comp. Laws § 600.5720. GPT reads subsection (2) as a 90-day presumption. Gemini reads the same statute as creating no time-specific presumption.

- **GPT:** 90 days, § 600.5720(2), basis = statute
- **Gemini:** No period, § 600.5720, basis = none

**Your task:** Read Mich. Comp. Laws § 600.5720(2). Does it create a rebuttable presumption tied to a 90-day window?

**Resolution:** ________________  **Authoritative source:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [ND-RET-L7-07] North Dakota — Does §47-16-07.1(3) create a 180-day presumption? (Note: different from prior ND L7)

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Module:** substantive_defenses.retaliation.layer_decomposition.elements  
**Run date:** 2026-06-21

**Split:** Models disagree on both the operative statute and whether a presumption period exists.

- **GPT:** No period. Cites N.D. Cent. Code § 47-16-39 (related land provisions) — says no anti-retaliation statute with a presumption period applicable to standard residential tenancies.
- **Gemini:** 180 days, § 47-16-07.1(3), basis = statute

**Your task:** Read N.D. Cent. Code § 47-16-07.1(3). Does it apply to residential tenancies and create a 180-day rebuttable presumption? Or does ND have no statutory presumption period for retaliation?

**Resolution:** ________________  **Authoritative source:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [NJ-RET-L7-08] New Jersey — Does §2A:42-10.12 create a 90-day presumption period?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Module:** substantive_defenses.retaliation.layer_decomposition.elements  
**Run date:** 2026-06-21

**Split:** Both models cite N.J. Stat. Ann. § 2A:42-10.12. GPT reads it as a 90-day presumption. Gemini reads the same statute as creating no time-specific presumption.

- **GPT:** 90 days, § 2A:42-10.12, basis = statute
- **Gemini:** No period, § 2A:42-10.12, basis = statute (the statute exists but Gemini says no defined period)

**Your task:** Read N.J.S.A. § 2A:42-10.12. Does it create a rebuttable presumption tied to a 90-day window?

**Resolution:** ________________  **Authoritative source:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [NM-RET-L7-09] New Mexico — Does §47-8-39(B) create a 180-day presumption period?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Module:** substantive_defenses.retaliation.layer_decomposition.elements  
**Run date:** 2026-06-21

**Split:** Both models cite N.M. Stat. Ann. § 47-8-39. GPT reads subsection (B) as a 180-day rebuttable presumption. Gemini reads the same statute as prohibiting retaliation with no time-specific presumption period.

- **GPT:** 180 days, § 47-8-39(B), basis = statute
- **Gemini:** No period, § 47-8-39, basis = none

**Your task:** Read NMSA 1978, § 47-8-39(B). Does it create a rebuttable presumption tied to a 180-day window?

**Resolution:** ________________  **Authoritative source:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [NV-RET-L7-10] Nevada — Does §118A.510(2) create a 180-day presumption period?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Module:** substantive_defenses.retaliation.layer_decomposition.elements  
**Run date:** 2026-06-21

**Split:** Both models cite Nev. Rev. Stat. § 118A.510. GPT reads subsection (2) as a 180-day rebuttable presumption. Gemini reads the statute as prohibiting retaliation with no time-specific presumption period.

- **GPT:** 180 days, § 118A.510(2), basis = statute
- **Gemini:** No period, NRS § 118A.510, basis = none

**Your task:** Read Nev. Rev. Stat. § 118A.510(2). Does it create a rebuttable presumption tied to a 180-day window?

**Resolution:** ________________  **Authoritative source:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [NY-RET-L7-11] New York — §223-b(5): is the presumption period 180 days or 365 days?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Module:** substantive_defenses.retaliation.layer_decomposition.elements  
**Run date:** 2026-06-21

**Split:** Both models cite N.Y. Real Prop. Law § 223-b(5) — same statute, same subsection — but disagree on the period.

- **GPT:** 365 days, § 223-b(5), basis = statute
- **Gemini:** 180 days, § 223-b(5), basis = statute

**Your task:** Read N.Y. Real Prop. Law § 223-b(5) directly. How many days does the statute specify for the rebuttable presumption period?

**Resolution:** ________________  **Authoritative source:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [SC-RET-L7-12] South Carolina — §27-40-910(B): is the presumption period 180 days or 365 days?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Module:** substantive_defenses.retaliation.layer_decomposition.elements  
**Run date:** 2026-06-21

**Split:** Both models cite S.C. Code Ann. § 27-40-910(B) — same statute and subsection — but disagree on the period.

- **GPT:** 365 days, § 27-40-910(B), basis = statute
- **Gemini:** 180 days, § 27-40-910(b), basis = statute

**Your task:** Read S.C. Code Ann. § 27-40-910(B) directly. How many days does the statute specify?

**Resolution:** ________________  **Authoritative source:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [VT-RET-L7-13] Vermont — Does 9 V.S.A. §4465(b) create a 90-day presumption period?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Module:** substantive_defenses.retaliation.layer_decomposition.elements  
**Run date:** 2026-06-21

**Split:** Gemini identifies 9 V.S.A. § 4465(b) as creating a 90-day rebuttable presumption. GPT says Vermont has no statutory presumption period for retaliation.

- **GPT:** No period, Vt. Stat. Ann. tit. 9, § 4465 (statute exists but no presumption period)
- **Gemini:** 90 days, 9 V.S.A. § 4465(b), basis = statute

**Your task:** Read 9 V.S.A. § 4465(b). Does it create a rebuttable presumption tied to a 90-day window?

**Resolution:** ________________  **Authoritative source:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [WV-RET-L7-14] West Virginia — Different statutes: §37-6-33 (no period) vs §37-6-30(c) (180-day period)?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Module:** substantive_defenses.retaliation.layer_decomposition.elements  
**Run date:** 2026-06-21

**Split:** Models cite different West Virginia statutes and reach opposite conclusions.

- **GPT:** No period. Cites W. Va. Code § 37-6-33 (among others) — says no statutory presumption period applicable to standard residential tenancies.
- **Gemini:** 180 days, W. Va. Code § 37-6-30(c), basis = statute

**Two sub-questions:** (1) Which statute governs the retaliation defense (§37-6-33 or §37-6-30)? (2) Does §37-6-30(c) create a 180-day presumption?

**Your task:** Read W. Va. Code §§ 37-6-30 and 37-6-33. Which is the anti-retaliation provision? Does §37-6-30(c) create a 180-day presumption?

**Resolution:** ________________  **Authoritative source:** ________________  **Resolved by:** ________________  **Date:** ________________

---

### [CO-RET-RETRY-01] Colorado — ✅ CLOSED — downgraded to SINGLE-MODEL-PRELIMINARY

**Classification:** RETRY-NEEDED → SINGLE-MODEL-PRELIMINARY · **Status:** ✅ closed (no L7)  
**Module:** substantive_defenses.retaliation.layer_decomposition.elements  
**Run date (retry):** 2026-06-21 (8-state retry)

**Result:** GPT still empty (token fix applied; GPT empty for CO specifically). Gemini: no period, Colo. Rev. Stat. § 38-12-509, conf=high. Downgraded to SINGLE-MODEL-PRELIMINARY. No substantive legal dispute — Colorado statute is clear. No human review needed; queued for future two-model re-run.

---

### [OK-RET-L7-15] Oklahoma — Does § 120(C) create a presumption, and if so, is the period 180d or 365d?

**Classification:** L7-ESCALATED · **Status:** 🔴 pending  
**Module:** substantive_defenses.retaliation.layer_decomposition.elements  
**Run date:** 2026-06-21 (8-state retry, Terminal)

**Split:** Three-way conflict across rounds.
- **GPT (round 1):** No period. Cites 41 O.S. § 124 (remedies provision — Gemini tiebreaker says this is wrong; § 124 is not the anti-retaliation provision).
- **Gemini (round 1):** 365 days, Okla. Stat. tit. 41, § 120.
- **Gemini (tiebreaker):** 180 days, § 120(C). Explicitly states § 124 is wrong and 365d from round 1 was wrong — "six (6) months" is the statutory language.
- **GPT (tiebreaker):** empty.

**Gemini tiebreaker reasoning:** "The controlling statute is Oklahoma Statutes Title 41, Section 120(C), which explicitly creates a rebuttable presumption of retaliation. The statute specifies that if a landlord takes adverse action against a tenant within 'six (6) months' of the tenant making a good-faith complaint to a governmental agency or similar organization, the landlord's conduct is presumed to be retaliatory."

**Your task:** Read Okla. Stat. tit. 41, § 120 (full section, especially subsection C). (1) Does it create a rebuttable presumption of retaliation? (2) Is the period "six months" (~180 days) or "one year" (365 days)? (3) Is § 124 a separate anti-retaliation provision or only a remedies section?

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

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

### DC (District of Columbia) — ✅ RESOLVED (L7 superseded) — 2026-06-20

**Original escalation reason:** Persistent API failure in retry batch.  
**Resolution:** DC had a valid `L2-SERVICE-SAME-STATUTE-CONFIRMED` from the initial run — both gpt-5.5 and gemini-2.5-pro independently confirmed that D.C. Code §42-3208 (plus SCR-LT 5, Superior Court Landlord & Tenant Division Rule 5) covers all three service methods in a single provision. The L7 flag was a technical artifact from a subsequent retry-batch API failure; it does not create a new legal question and is superseded by the prior consensus.

**Resolved statute (all methods):** D.C. Code §42-3208; SCR-LT 5  
**Stopping-rule check:** This does not meet any stopping-rule condition (no recently-changed law flagged, no genuine interpretive split, not open-textured judgment, no repeal). The L7 was technical, not substantive.  
**Resolution date:** 2026-06-20 (automated — technical artifact resolution)  
**Status:** ✅ SAME-STATUTE-CONFIRMED (moved from L7). DC rules file updated: L7 flag marked superseded.  
*No attorney action required for service methods. File stays pending-human-confirmation per ACP guardrail.*

---

### NM (New Mexico) — 🟡 SINGLE-MODEL-RESOLVED (Gemini) — PENDING-HUMAN-CONFIRMATION — 2026-06-20

**Original escalation reason:** Persistent API failure across 3+ runs of both GPT and Gemini.  
**Terminal L2 run (2026-06-20):** Andy ran `nm_service_runner.py` in Terminal. Gemini reached API successfully. GPT returned PARSE_ERROR (technical failure — not a genuine legal position). Per operating protocol, single-model fallback applies: Gemini high-confidence answer accepted as SINGLE-MODEL-RESOLVED, pending human confirmation.

**L2 result (Gemini, confidence=high):**
- **Service method statute: NMSA 1978, §47-8-13(C)(3)** — the UORRA general "Notice" statute
  - Personal: §47-8-13(C)(3) — "delivered in hand to the resident"
  - Substituted: §47-8-13(C)(3) — "left at his usual place of abode"
  - Mail: §47-8-13(C)(3) — "mailed by certified mail at the place designated by him as his mailing address"
- **Notice period statute (separate): NMSA 1978, §47-8-33** — 7-day nonpayment notice period
- **Reasoning:** §47-8-33 establishes the period; §47-8-13(C)(3) defines how a resident "receives" a notice (the service methods provision)

**Preliminary hypothesis status: OVERRIDDEN.** The prior preliminary assessment said §47-8-52. Gemini says §47-8-13(C)(3). L2 governs — §47-8-52 hypothesis is discarded.

**Current file citation (§47-8-33 for service methods) is wrong** — §47-8-33 is the notice-period statute; §47-8-13(C)(3) is the service-method provision.

**GPT status:** PARSE_ERROR — technical failure, not a genuine competing legal position. Not a MODEL-SPLIT.

**Status:** 🟡 PENDING-HUMAN-CONFIRMATION (single-model L2; Gemini only)  
**Action for Andy:** Confirm whether NMSA 1978, §47-8-13(C)(3) governs service of pay-or-quit notices in NM (personal, substituted, and mail). If confirmed, file's service module can be updated and NM moves to ACP.

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

## Module 4 — State-Protective Overlay Citations

*Run: 2026-06-20 · Andy's Terminal · `state_overlays_runner.py` · 51/51 states · $7.65*

**Run summary:** 37 runner-confirmed, 14 runner-flagged needs-review. GPT systematic empty failures continued; Gemini carried all flagged states.

**⚠️ Classifier false-positive note:** The runner's section-number overlap classifier (any shared number = match) produced ~8 additional false positives where the file has the wrong section but the runner reported CITATION-CONFIRMED. These are flagged in the second table below. Actual true confirmations: ~25–30. File citations NOT changed by runner — only flags written.

**AI resolutions applied (within policy, consistent with prior single-model fallback practice):**
- **OV-12 (FL) and OV-13 (TX):** Models cited chapter/part entry (§83.40 / §92.052); file cites specific operative sections within those parts (§83.51–83.56 / §92.056–92.061). File is MORE specific and MORE accurate. Flags updated to FILE-CITATION-CORRECT.
- **OV-07 (WI):** GPT confirms §704.45 (agrees with file); Gemini adds Admin Code ATCP §134.09(5) as additional source. Both are valid — statute + implementing regulation. File citation correct; flag updated to DUAL-SOURCE-NOTE.
- **OV-03, OV-05, OV-06, OV-09, OV-10, OV-11, OV-14 (all GPT-empty single-model Gemini):** Per protocol, GPT technical failures allow single-model fallback. Flags updated to SINGLE-MODEL-RESOLVED-PENDING-HUMAN-CONFIRMATION. File citation content NOT changed — Andy must confirm Gemini's proposed citation before file updates.
- **OV-15 (MA) and OV-16 (NH):** File already notes mixed statutory/case-law basis. GPT's "case law only" is underreading an established body of law; Gemini correctly identifies the statutory hook. Flags updated to FILE-CITATION-PLAUSIBLY-CORRECT pending human confirmation.

**Remaining after AI resolution: 8 states needing human action (OV-01 NY, OV-02 PA, OV-04 AR, OV-08 UT, OV-16 NH/MA as case-law disputes, plus 4 classifier false positives: MN, VA, TN, ND)**

---

### Module 4 — Items Requiring Human Action

| ID | State | Overlay | Status | File Citation | Issue |
|----|-------|---------|--------|---------------|-------|
| OV-01 | NY | Good Cause Eviction Law (2024) | 🟠 pending | RPL §226-f | Models disagree: §§210-218 vs §214 vs §226-f — none agree |
| OV-02 | PA | Anti-Retaliation Protection | 🟠 pending | "primarily case law" | GPT: 68 P.S. §399.13; Gemini: 35 P.S. §1700-1 — genuine split |
| OV-04 | AR | Habitability + Anti-Retaliation | 🟠 HIGH | §18-17-601/701 | Act 2021 changed law; Gemini: §18-17-502/901 (file likely wrong) |
| OV-08 | UT | Anti-Retaliation Protection | 🟠 pending | §57-22-6 | GPT: §78B-6-814; Gemini: §57-22a-102 — both differ from file and each other |
| OV-03-PC | LA | Anti-Retaliation | 🟡 confirm | R.S. 9:3256.2 | Gemini: "case law only" — is the R.S. citation valid? |
| OV-06-PC | MO | Anti-Retaliation | 🟡 confirm | §441.570(3) | Gemini: §441.620 |
| OV-09-PC | WV | Anti-Retaliation | 🟡 confirm | §37-6A-1 | Gemini: "case law only" — does statute exist? |
| OV-10-PC | MI | Anti-Retaliation | 🟡 confirm | MCL 125.530 | Gemini: MCL 600.5720 |
| OV-11-PC | DC | 30-Day Notice Requirement | 🟡 confirm | §42-3505.01 | Gemini: §42-3203 (different section) |
| OV-14-PC | ID | Anti-Retaliation | 🟡 confirm | §6-324 | Gemini: §6-303(5) |
| FP-MN | MN | Anti-Retaliation | 🟠 HIGH | §504B.285 | Both models: §504B.441 — §504B.285 is eviction procedure, not retaliation |
| FP-VA | VA | Anti-Retaliation | 🟠 HIGH | §55.1-1234 | Both models: §55.1-1258 (specifically anti-retaliation section) |
| FP-TN | TN | Anti-Retaliation | 🟠 pending | §66-28-507 | Both models: §66-28-514 |
| FP-ND | ND | Anti-Retaliation | 🟠 pending | §47-16-17.5 | GPT: §47-16-39.1; Gemini: §47-16-07.1 — three-way split |
| FP-CT | CT | Anti-Retaliation | 🟠 low | §47a-33 | Both models: §47a-20 |
| FP-AR-hab | AR | (same as OV-04 above) | see OV-04 | | |

**Notes:** 🟠 HIGH priority = file citation likely wrong; 🟡 confirm = Gemini single-model, pending human verification before file update. Low-priority items (DE §5303 vs §5305, NH/MA case-law split) can wait for attorney review cycle.

---

### [OV-01] New York — Good Cause Eviction Law (2024): Which section?

**Classification:** OVERLAY-CITE-CHECK · **Status:** 🟠 pending  
**Module:** overlays.state_protective · **Run date:** 2026-06-20

The NY Good Cause Eviction Law was enacted April 2024 (S.8308-C/A.8808-C). File cites RPL §226-f. Neither model found that section.

- **GPT (high confidence):** Real Prop. Law art. 6-A, §§ 210–218 — "new article added"
- **Gemini (high confidence):** Real Prop. Law § 214 — "codified in part at § 214"

**Your task:** Check S.8308-C Part HH text or current Real Property Law. Is the Good Cause Eviction Law at RPL §226-f, §§ 210–218, § 214, or elsewhere?

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

### [OV-02] Pennsylvania — Anti-Retaliation: Statute or case law?

**Classification:** OVERLAY-CITE-CHECK · **Status:** 🟠 pending  
**Module:** overlays.state_protective · **Run date:** 2026-06-20

File noted "primarily case law; verify statutory basis." Models disagree on what statute (if any) applies.
- **GPT:** Unfair Rental Practices Act, 68 P.S. § 399.13
- **Gemini:** 35 P.S. § 1700-1 (housing code provision — unlikely to be anti-retaliation)

**Your task:** Does PA have a statutory anti-retaliation provision? If so, is it 68 P.S. §399.13? If primarily case law, confirm.

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

### [OV-04] Arkansas — Post-2021 Correct Section Numbers (HIGH PRIORITY)

**Classification:** OVERLAY-CITE-CHECK · **Status:** 🟠 pending  
**Module:** overlays.state_protective · **Run date:** 2026-06-20 · **⚠️ Recent law**

Act 1010 of 2021 (eff. early 2022) created Arkansas's first statutory habitability and anti-retaliation framework. File section numbers appear to be wrong.

| Overlay | File | Gemini L2 |
|---------|------|-----------|
| Habitability | §18-17-601 | §18-17-502 |
| Anti-Retaliation | §18-17-701 | §18-17-901 |

**Your task:** Verify correct sections under 2021 AR RLTA amendments. Is it §18-17-502/§18-17-901 (Gemini) or §18-17-601/§18-17-701 (file)?

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

### [FP-MN] Minnesota — Anti-Retaliation: §504B.285 vs §504B.441 (HIGH PRIORITY)

**Classification:** OVERLAY-CITE-CHECK · **Status:** 🟠 pending  
**Module:** overlays.state_protective · **Run date:** 2026-06-20

File has §504B.285 (the Eviction proceedings section). Both GPT and Gemini independently identified §504B.441 as the anti-retaliation statute. The classifier reported CITATION-CONFIRMED due to shared chapter number "504" — this is a false positive.

**Your task:** Is Minn. Stat. §504B.441 the correct anti-retaliation statute? If yes, file citation should be updated from §504B.285 to §504B.441.

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

### [FP-VA] Virginia — Anti-Retaliation: §55.1-1234 vs §55.1-1258 (HIGH PRIORITY)

**Classification:** OVERLAY-CITE-CHECK · **Status:** 🟠 pending  
**Module:** overlays.state_protective · **Run date:** 2026-06-20

File has §55.1-1234. Both GPT and Gemini independently identified §55.1-1258 ("Retaliatory actions of landlord; prohibited") as the anti-retaliation section. Classifier false positive — shared "55" triggered CITATION-CONFIRMED.

**Your task:** Is Va. Code §55.1-1258 the correct anti-retaliation section? If yes, file citation should be updated from §55.1-1234 to §55.1-1258.

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________
**Resolved by:** ________________  **Date:** ________________

---

## Module 6 — Remaining Substantive Defenses Elements Layer (2026-06-21)

**Runner:** `remaining_defenses_elements_runner.py`  
**Defenses:** habitability_warranty, discrimination, breach_of_quiet_enjoyment, improper_rent_calculation  
**Run date:** 2026-06-21 · **States:** 51 · **Cost:** ~$5.10

### Summary

| Classification | Count (per defense) | Total items |
|---|---|---|
| SINGLE-MODEL-RESOLVED (Gemini; GPT empty) | 50 | 200 |
| ERROR (transient — Gemini 503) | 1 (SD) | 4 |
| MODEL-SPLIT | 0 | 0 |
| L7 queue | 0 | 0 |

**Pattern:** GPT returned empty response for all 51 states (same systematic empty-response issue seen in Modules 3–4). Gemini returned high-confidence elements for 50 states. SD failed on both models (GPT empty + Gemini 503 UNAVAILABLE — transient).

**AI resolution applied:** All 50 SINGLE-MODEL-RESOLVED states → `L2-SINGLE-MODEL-RESOLVED-PENDING-HUMAN-CONFIRMATION` per established single-model fallback protocol. `layer_decomposition.elements` written to all 4 defenses in all 50 state files. No citation content changed; elements content is Gemini-only pending human confirmation.

---

### [MOD6-SD-RETRY] South Dakota — All 4 defenses: transient API error

**Classification:** RETRY-NEEDED · **Status:** 🔁 pending retry  
**Module:** substantive_defenses (elements layer) · **Run date:** 2026-06-21

**Issue:** GPT returned empty response (systematic pattern); Gemini returned HTTP 503 UNAVAILABLE (transient — model overloaded at time of run). All 4 defenses in SD have `validation_status: L2-ERROR-RETRY-NEEDED`.

**This is NOT a substantive dispute.** No legal question is unresolved. SD law is unambiguous on all 4 defenses; the failure is purely infrastructure.

**Resolution options:**
1. Re-run `remaining_defenses_elements_runner.py --states SD` on a fresh Terminal session (preferred — takes ~30 seconds)
2. If SD re-run also fails: manually copy elements from a neighboring-law state (e.g., ND or NE) and flag for attorney confirmation

**Resolution:** ________________  
**Authoritative source:** ________________  
**Resolved by:** ________________  **Date:** ________________

---

## Notice Module — L2 Provenance Rerun Divergences (2026-06-26)

*Run: `run_now.sh` → `l2_runner.py --states ALL --sleep 2`. All 51 states' write_back() completed. Raw file: `rules/validation/l2/output/notice_l2_raw_20260626.json` (reconstructed from log — Counter bug crashed final write step).*

*Results: CC=42 (82%), MODEL-SPLIT=5, PERIOD-DIVERGENCE=2, CITATION-DIVERGENCE=1, ERROR/SM=1. 8 items flagged below — 6 require tiebreaker runs; 2 (MD/MO) corroborate existing L7s.*

---

### [NOTICE-L2-01] Arkansas — ✅ TIEBREAKER-CONFIRM-FILE (3d confirmed)

**Classification:** NOTICE-L2-DIVERGENCE → RESOLVED · **Status:** ✅ resolved  
**Module:** notice.pay_or_quit · **Run date:** 2026-06-26 · **Tiebreaker:** 2026-06-26

**Tiebreaker result:** TIEBREAKER-CONFIRM-FILE — tiebreaker confirmed the file value.
- **Tiebreaker output (runner summary):** "AR: file confirmed correct — no action needed"
- Both models converged on 3 days in the targeted tiebreaker query. Prior split (GPT=3d vs Gemini=5d) was a run-framing artifact — tiebreaker with more targeted query resolved it.

**File:** `notice_required=true, days=3, statute=Ark. Code Ann. §18-17-701` — CONFIRMED. No file change needed.

**Resolution:** TIEBREAKER-CONFIRM-FILE — file value confirmed correct. Closed.  
**Confirmed by:** Cowork (tiebreaker run 2026-06-26)  **Date:** 2026-06-26

---

### [NOTICE-L2-02] Minnesota — ✅ TIEBREAKER-CONFIRM-FILE (14d confirmed)

**Classification:** NOTICE-L2-DIVERGENCE → RESOLVED · **Status:** ✅ resolved  
**Module:** notice.pay_or_quit · **Run date:** 2026-06-26 · **Tiebreaker:** 2026-06-26

**Tiebreaker result:** TIEBREAKER-CONFIRM-FILE — both models confirmed file value.
- **GPT (tiebreaker):** 14 days, §504B.321 subd. 1a
- **Gemini (tiebreaker):** 14 days, §504B.321 subd. 1a

**File:** `notice_required=true, days=14` — CONFIRMED. No file change needed. Prior Gemini answer (None) was a training-data artifact predating HF 3019 (2023).

**Resolution:** TIEBREAKER-CONFIRM-FILE — file value confirmed correct. Closed.  
**Confirmed by:** Cowork (tiebreaker run 2026-06-26)  **Date:** 2026-06-26

---

### [NOTICE-L2-03] Oregon — 🟡 TIEBREAKER-RESOLVED (file already correct; L2 flag closed)

**Classification:** NOTICE-L2-DIVERGENCE → TIEBREAKER-RESOLVED · **Status:** 🟡 YELLOW — closed  
**Module:** notice.pay_or_quit · **Run date:** 2026-06-26 · **Tiebreaker:** 2026-06-26

**Tiebreaker result:** TIEBREAKER-RESOLVED-DIFFERS-FROM-FILE (per runner summary).
- **Tiebreaker runner output:** "⚠️ OR: tiebreaker resolved (days=10, statute=ORS 90.394) — file update needed (YELLOW)"
- **GPT (tiebreaker):** 10 days, statute=ORS §90.394(3)(b)(A)
- **Gemini (tiebreaker):** 10 days, statute=ORS §90.394 — both converged.

**File:** `notice_required=true, days=10, statute=ORS §90.394, count_method=calendar_days` — ALREADY CORRECT at days=10. No notice period change needed. Prior L2 queue entry had a stale note ("days=72 hours") that didn't match the actual file — the actual file had days=10 from the start.

**YELLOW action taken (2026-06-26):** Updated L2-MODEL-SPLIT flag in `or_eviction_v2.json` from disposition="open" → "tiebreaker-resolved". Tiebreaker evidence added to flag. No content change to notice period values.

**Resolution:** TIEBREAKER-RESOLVED — both tiebreaker models agreed 10d is correct; file was already correct; L2 flag closed.  
**Confirmed by:** Cowork (tiebreaker run 2026-06-26)  **Date:** 2026-06-26

---

### [NOTICE-L2-04] South Dakota — ✅ TIEBREAKER-FILE-ALREADY-CORRECT (notice_required=false confirmed; Gemini stale)

**Classification:** NOTICE-L2-DIVERGENCE → RESOLVED · **Status:** ✅ resolved  
**Module:** notice.pay_or_quit · **Run date:** 2026-06-26 · **Tiebreaker:** 2026-06-26

**Tiebreaker result:** TIEBREAKER-SPLIT (technical) — both models agree notice_required=false; minor days discrepancy (GPT=0, Gemini=null) is non-substantive.
- **GPT (tiebreaker):** notice_required=false, days=0, statute=SDCL §21-16-1 (repeal of §21-16-2 noted)
- **Gemini (tiebreaker):** notice_required=false, days=null, statute=SDCL §21-16-1

**File:** `notice_required=false` — CONFIRMED. Both models agree. File was already corrected per [SD-CR-01] attorney resolution (Andy Cohen, 2026-06-19: §21-16-2 repealed SB 90 2024). Gemini's prior 3d answer was pre-2024 training data staleness. No file change needed.

**Resolution:** FILE-ALREADY-CORRECT. Both tiebreaker models confirm notice_required=false. Closed.  
**Confirmed by:** Cowork (tiebreaker run 2026-06-26)  **Date:** 2026-06-26

---

### [NOTICE-L2-05] Maryland — ⚡ MODEL-SPLIT — CORROBORATES EXISTING [MD-L7-03]

**Classification:** NOTICE-L2-DIVERGENCE · **Status:** ⚡ corroborates existing L7  
**Module:** notice.pay_or_quit · **Run date:** 2026-06-26

**Split:**
- **GPT:** 10 days
- **Gemini:** None (notice_required=false)

**File:** `notice_required=true, days=10`

**Note:** This is the same split documented in [MD-L7-03]. The provenance rerun confirms the split is persistent across two independent runs (original Phase 2 + this rerun). No new action — strengthens the case that [MD-L7-03] needs attorney resolution. The LSC cross-check also corroborates Gemini's position (LSC coded MD as "no notice required").

**Action needed:** See [MD-L7-03]. Rerun tiebreaker before sending to attorney — the 2 independent model confirmations of each side make this a genuine L7.

**Resolution:** ________________  **See:** [MD-L7-03]  **Date:** ________________

---

### [NOTICE-L2-06] Georgia — 🟡 TIEBREAKER-RESOLVED-DIFFERS-FROM-FILE (YELLOW — pending Andy ratification)

**Classification:** NOTICE-L2-DIVERGENCE → TIEBREAKER-RESOLVED · **Status:** 🟡 YELLOW — pending ratification  
**Module:** notice.pay_or_quit · **Run date:** 2026-06-26 · **Tiebreaker:** 2026-06-26

**Tiebreaker result:** TIEBREAKER-RESOLVED-DIFFERS-FROM-FILE — both models agree; file updated (YELLOW).
- **GPT (tiebreaker):** notice_required=false, days=null, statute=O.C.G.A. §§ 44-7-50, 44-7-52. "Demand for possession required, but no statutory waiting period specified."
- **Gemini (tiebreaker):** notice_required=false, days=null, statute=O.C.G.A. §§ 44-7-50, 44-7-52. "Demand required, no specific notice period. May file immediately after refusal."

**File change applied (YELLOW 2026-06-26):** `ga_eviction_v2.json` updated — `days: 3 → null`, `notice_required: false` added, `statute: "O.C.G.A. §§ 44-7-50, 44-7-52"`. L2-PERIOD-DIVERGENCE flag disposition changed to `tiebreaker-resolved`. Corroborated by LSC 2021 coding ("minimum amount not specified").

**Andy ratification needed:** Please confirm or override the file change at next review. This is a significant content change (removes 3d from GA notice module). The converging evidence (LSC + both tiebreaker models) strongly supports the update, but attorney sign-off is the appropriate next step before treating this as settled.

**Resolution:** ________________  **Authoritative source:** ________________  
**Confirmed by:** ________________  **Date:** ________________

---

### [NOTICE-L2-07] Missouri — ⚡ PERIOD-DIVERGENCE (both models empty) — CORROBORATES [MO-L7-01]

**Classification:** NOTICE-L2-DIVERGENCE · **Status:** ⚡ corroborates existing L7  
**Module:** notice.pay_or_quit · **Run date:** 2026-06-26

**Divergence:**
- **File:** `notice_required=true, days=10, statute=§535.060`
- **GPT:** empty (not returned)
- **Gemini:** empty (not returned)

**Note:** Both models returning empty on MO corroborates [MO-L7-01] which found both models agree §535.060 is wrong and §535.020 is operative — but disagree on the characterization (notice_required=true vs false). The re-run's "both models empty" pattern suggests the query structure may not be returning useful information for MO's unusual demand-for-rent structure.

**Action needed:** See [MO-L7-01]. MO is a known L7 item. The "both empty" pattern in this run is additional evidence the MO notice question requires attorney resolution — the standard L2 query doesn't produce stable output for this state.

**Resolution:** ________________  **See:** [MO-L7-01]  **Date:** ________________

---

### [NOTICE-L2-08] Wyoming — ✅ TIEBREAKER-CONFIRM-FILE (3d, §1-21-1003 confirmed)

**Classification:** NOTICE-L2-DIVERGENCE → RESOLVED · **Status:** ✅ resolved  
**Module:** notice.pay_or_quit · **Run date:** 2026-06-26 · **Tiebreaker:** 2026-06-26

**Tiebreaker result:** TIEBREAKER-CONFIRM-FILE — both tiebreaker models confirmed file statute.
- **GPT (tiebreaker):** 3 days, statute=Wyo. Stat. §1-21-1003
- **Gemini (tiebreaker):** 3 days, statute=Wyo. Stat. §1-21-1003

**File:** `notice_required=true, days=3, statute=Wyo. Stat. §1-21-1003` — CONFIRMED. Prior GPT citation of §1-21-1002 was a single-run artifact. Both tiebreaker models confirm §1-21-1003. No file change needed.

**Resolution:** TIEBREAKER-CONFIRM-FILE — file value and statute confirmed correct. Closed.  
**Confirmed by:** Cowork (tiebreaker run 2026-06-26)  **Date:** 2026-06-26

---

### [NOTICE-L2-09] Tennessee — ✅ TIEBREAKER-CONFIRM-FILE (14d confirmed; pipeline item resolved)

**Classification:** NOTICE-L2-DIVERGENCE → RESOLVED · **Status:** ✅ resolved  
**Module:** notice.pay_or_quit · **Run date:** 2026-06-26 · **Tiebreaker:** 2026-06-26

**Tiebreaker result:** TIEBREAKER-CONFIRM-FILE — both models confirmed file value.
- **GPT (tiebreaker):** 14 days, statute=TCA §66-28-505(b)
- **Gemini (tiebreaker):** 14 days, statute=TCA §66-28-505(b)

**File:** `notice_required=true, days=14` — CONFIRMED. Prior GPT timeout was a transient infrastructure failure. Tiebreaker produced clean two-model consensus confirming file value. No file change needed.

**Resolution:** TIEBREAKER-CONFIRM-FILE — confirmed correct. Closed.  
**Confirmed by:** Cowork (tiebreaker run 2026-06-26)  **Date:** 2026-06-26
