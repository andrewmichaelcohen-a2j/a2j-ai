# Debt-track Disagreement Queue

**Module:** Debt Defense Prototype (all states/federal) - **Layer:** grounded-corroboration + adversarial-generation
**Runner rule:** `scripts/corroboration/run_corroboration.py` appends new flagged items only. It never edits or
overwrites the Resolution, Resolved by, or Date fields -- those belong to Andy / the certifying attorney.
Built per DEBT_PROJECT_ARCHITECTURE_SPEC.md S3(d), generalizing Direction D-2 (`docs/DIRECTION_D_ROADMAP.md`) into
the debt track, per the 2026-08-26 Phase-A-Unblock direction item 6.

> **How to use this queue:** work top-to-bottom. Each entry has a candidate classification (rule gap / model error /
> citation-aggregator error) computed mechanically by the runner as a *hint*, not a determination -- the runner does
> not and cannot decide which side is legally correct. Fill in Resolution and Resolved-by, then move to Resolved.

---
## Open

*(No open entries below this line — see "Archived" section. New entries from the next live run land here.)*

---

## Archived -- Pre-Fix Diagnostic Runs (archived 2026-08-28)

**Why archived, not resolved:** every entry below comes from live corroboration runs (`run_20260826T171949Z` through
`run_20260826T202441Z`, all 2026-08-26 evening) that predate this project's Round 12-15 citation and tooling fixes:
the User-Agent fix and eCFR/FindLaw/Justia normalization work (Round 11), the CA re-pin to leginfo.legislature.ca.gov
and eCFR ellipsis fix (Round 12), the TX re-pin to statutes.capitol.texas.gov + Craddock re-pin to CourtListener plus
retry-on-flake logic (Round 13), and the FDCPA (b)(4) diagnostic pinpoint (Round 14). Nearly every CITATION-CHECK-FAILED
entry below traces to a since-fixed cause: a 403 from a bot-blocking secondary aggregator (FindLaw/Justia -- now re-pinned
to primary/Tier-A sources for CA and TX; AZ/UT/NY re-pins are still open work), a stale User-Agent, or an eCFR
normalization edge case. Nearly every MODEL-DISAGREEMENT entry below rests solely on the numeric/citation-fingerprint
heuristic, which Round 11 demoted to a secondary, non-gating diagnostic in favor of LLM-judged semantic agreement --
so a fingerprint mismatch alone, on its own, is no longer this project's disagreement signal.

None of this is an attorney-level resolution and none of these entries are being asserted correct -- they are being
moved out of the Open lane because the pipeline conditions that produced them no longer reflect the current rule
files or runner. Per the append-only discipline, nothing is deleted: every entry, its per-model derivations, and its
blank Resolution/Resolved-by/Date fields are preserved verbatim below. If the upcoming full-corpus live run reproduces
any of the same MODEL-DISAGREEMENT findings under the current LLM-judge, or a genuine (non-pipeline) CITATION-CHECK-FAILED
persists after the AZ/UT/NY re-pins land, it will re-file as a fresh entry in the Open section above, on its own
merits, under current tooling.

**Archived by:** Claude (Cowork) -- **Date:** 2026-08-28 -- per Andy's 2026-08-26 evening directive item 3
("confirmation that the disagreement queue is clean of runs 1-2 artifacts so the new flags land in an empty lane").

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] CITATION-CHECK-FAILED -- run run_20260826T202441Z, 2026-08-26T20:25:47Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 75544, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0}}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 75544, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the prohibition on repeated/continuous calls (and FDCPA § 806(5)) if, as to a particular person and a particular debt, it places no more than seven calls within seven consecutive days and places no call within the seven consecutive days following a telephone conversation with that person about that debt (the conversation date counts as day one). Under § 1006.14(b)(2)(ii), exceeding either of those frequencies creates a presumption that the collector violated the rule and FDCPA § 806(5). Both presumptions are subject to the exclusions in paragraph (b)(3). Per § 1006.14(b)(4), the counts run separately for each debt in collection, except that student loan debts serviced under a single account number when obtained by the collector are treated as one 'particular debt.'"
  - gpt-5.5: grounded=True, error=None, summary='Subject to listed exclusions not provided here, a debt collector is presumed to comply if, for a particular person and a particular debt, it does not call more than seven times within seven consecutive days and does not call within seven consecutive days after having a telephone conversation with that person about that debt. The date of the telephone conversation counts as the first day of that seven-day period. A debt collector is presumed to violate the rule if it exceeds either of those call-frequency limits; “particular debt” generally means each debt in collection, with a special grouping rule for certain student loan debts serviced under one account number.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to violate the law if, in connection with a particular debt, they call a person more than seven times within seven consecutive days. A violation is also presumed if a collector calls within seven consecutive days after having a telephone conversation with that person about the debt. This frequency limit applies to each of a consumer's debts individually, except for student loans, where all loans under a single account number are treated as one debt."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-WRITTEN-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T201346Z, 2026-08-26T20:15:36Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/codes/california/code-ccp/part-2/title-2/chapter-3/section-337/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5999, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}, {'url': 'https://law.justia.com/codes/california/code-ccp/part-2/title-2/chapter-3/section-337/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5999, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 337(a), an action upon any contract, obligation, or liability founded upon a written instrument must be brought within four years (subject to the exception in Section 336a, and a special three-month limit for deficiency-type money judgments after a trustee's/mortgage power-of-sale sale). Subsection (d) adds that once that four-year period has run, a person may not file suit or start an arbitration or other legal proceeding to collect the debt. The only way the period may be extended is pursuant to Section 360."
  - gpt-5.5: grounded=True, error=None, summary='An action on a contract, obligation, or liability founded on a written instrument must be brought within four years. Once that limitations period has run, a person may not bring a lawsuit, arbitration, or other legal proceeding to collect the debt, and the period may be extended only under Section 360.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In California, the statute of limitations for an action upon a contract founded upon a written instrument is four years. There is a specific exception for actions for a money judgment after a power of sale on real property, which must be brought within three months. Once the applicable time period has run, a person is barred from bringing a suit or other legal proceeding to collect the debt.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-WRITTEN-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T201346Z, 2026-08-26T20:15:36Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** LLM-judged semantic agreement: All three agree on the core rule: a four-year limitations period for actions on a written contract, with suit/arbitration barred once it runs. However, Analysis 2 omits the three-month exception for money judgments after a power-of-sale foreclosure (stated by Analyses 1 and 3), and Analysis 3 omits that the period may be extended only under Section 360 (stated by Analyses 1 and 2). (judge model: claude-opus-5). Numeric-fingerprint diagnostic (secondary, not gating): Anthropic=['3', '4'], OpenAI=['4'], Gemini=['3', '4'] (fingerprint_agreement=False).

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 337(a), an action upon any contract, obligation, or liability founded upon a written instrument must be brought within four years (subject to the exception in Section 336a, and a special three-month limit for deficiency-type money judgments after a trustee's/mortgage power-of-sale sale). Subsection (d) adds that once that four-year period has run, a person may not file suit or start an arbitration or other legal proceeding to collect the debt. The only way the period may be extended is pursuant to Section 360."
  - gpt-5.5: grounded=True, error=None, summary='An action on a contract, obligation, or liability founded on a written instrument must be brought within four years. Once that limitations period has run, a person may not bring a lawsuit, arbitration, or other legal proceeding to collect the debt, and the period may be extended only under Section 360.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In California, the statute of limitations for an action upon a contract founded upon a written instrument is four years. There is a specific exception for actions for a money judgment after a power of sale on real property, which must be brought within three months. Once the applicable time period has run, a person is barred from bringing a suit or other legal proceeding to collect the debt.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] CITATION-CHECK-FAILED -- run run_20260826T201346Z, 2026-08-26T20:14:43Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 75544, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0}}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 75544, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the harassment prohibition in § 1006.14(b)(1) and FDCPA § 806(5) if it places calls to a particular person about a particular debt neither more than seven times in seven consecutive days, nor within seven consecutive days after having had a telephone conversation with that person about that debt. Conversely, under (b)(2)(ii), exceeding either of those frequencies creates a presumption of violation. The counts are applied per 'particular debt,' meaning each individual debt in collection, except that for student loans all debts serviced under a single account number when obtained by the collector count as one debt (§ 1006.14(b)(4))."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is presumed to comply if, for a particular person and a particular debt, it does not place more than seven calls within seven consecutive days and does not call within seven consecutive days after having had a telephone conversation with that person about that debt. A debt collector is presumed to violate the rule if it exceeds either of those call-frequency limits. For this purpose, a “particular debt” generally means each debt in collection, with a special rule grouping certain student loan debts serviced under a single account number.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to have violated the law if, in connection with a particular debt, they call a person more than seven times within seven consecutive days. A violation is also presumed if a collector calls within seven consecutive days after having a telephone conversation with that person about the debt. This rule applies to each of a consumer's individual debts, except for student loans, where all loans under a single account number are treated as one debt."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-JUSTICE-COURT-DEBT-ANSWER-DEADLINE] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:24:12Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://texaslawhelp.org/guide/how-to-answer-a-debt-collection-case-in-justice-court', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 120175, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.353}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Based on the supplied text, a defendant in a Texas justice court debt-collection suit must file an answer within 14 days after the date of service; if that 14th day lands on a weekend or court holiday, the deadline rolls to the next business day. The same excerpt notes that Texas justice courts hear debt claims valued up to $20,000. Caveat: this comes from a secondary-source (TexasLawHelp.org) restatement rather than the primary Rule 502.5 text, so the exact rule language and any additional timing mechanics (e.g., how the day of service is counted or filing cutoff time) are not verified here.'
  - gpt-5.5: grounded=True, error=None, summary='In a Texas justice-court debt-collection lawsuit, the defendant’s Answer is due 14 days after the date they were served. If the 14th day falls on a weekend or court holiday, the Answer is due on the next business day.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-JUSTICE-COURT-DEBT-ANSWER-DEADLINE] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:24:12Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['$20000', '14'], OpenAI=['14'], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Based on the supplied text, a defendant in a Texas justice court debt-collection suit must file an answer within 14 days after the date of service; if that 14th day lands on a weekend or court holiday, the deadline rolls to the next business day. The same excerpt notes that Texas justice courts hear debt claims valued up to $20,000. Caveat: this comes from a secondary-source (TexasLawHelp.org) restatement rather than the primary Rule 502.5 text, so the exact rule language and any additional timing mechanics (e.g., how the day of service is counted or filing cutoff time) are not verified here.'
  - gpt-5.5: grounded=True, error=None, summary='In a Texas justice-court debt-collection lawsuit, the defendant’s Answer is due 14 days after the date they were served. If the 14th day falls on a weekend or court holiday, the Answer is due on the next business day.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-EXEMPT-PERSONAL-PROPERTY] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:23:25Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 3 of 3 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/tx/property-code/prop-sect-42-001/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5616, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}, {'url': 'https://codes.findlaw.com/tx/property-code/prop-sect-42-001/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5616, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.071}}, {'url': 'https://codes.findlaw.com/tx/property-code/prop-sect-42-002/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5616, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under Tex. Prop. Code § 42.001(a), personal property of the kinds listed in § 42.002 is exempt from garnishment, attachment, execution, or other seizure up to an aggregate fair market value of $100,000 for property provided for a family, or $50,000 for a single adult who is not a member of a family. The qualifying categories in § 42.002(a) include home furnishings, provisions for consumption, farm/ranch vehicles and implements, tools and books of a trade or profession, clothing, jewelry (capped at 25 percent of the aggregate limit), two firearms, athletic and sporting equipment, one motor vehicle per licensed family member or single adult, specified livestock and fowl, and household pets. Separately, § 42.001(b) exempts certain property entirely outside the dollar caps: current wages for personal services (except for court-ordered child support enforcement), professionally prescribed health aids, alimony/support/separate maintenance, and a bible or other sacred writings.'
  - gpt-5.5: grounded=True, error=None, summary='Texas exempts certain personal property from garnishment, attachment, execution, or other seizure. For property listed in Section 42.002(a), the exemption applies up to an aggregate fair market value of $100,000 for a family or $50,000 for a single adult not in a family. Certain items, including current wages for personal services, prescribed health aids, support payments, and religious sacred writings, are exempt and are not counted toward those aggregate limits.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Texas, certain personal property is exempt from seizure by creditors up to an aggregate value of $100,000 for a family or $50,000 for a single adult. The categories of property subject to this limit include home furnishings, vehicles, tools of a trade, and household pets. Some specific property, such as current wages and professionally prescribed health aids, is also exempt and is not counted toward these dollar limits.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-EXEMPT-PERSONAL-PROPERTY] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:23:25Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['$100000', '$50000', '1', '2', '25'], OpenAI=['$100000', '$50000'], Gemini=['$100000', '$50000'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under Tex. Prop. Code § 42.001(a), personal property of the kinds listed in § 42.002 is exempt from garnishment, attachment, execution, or other seizure up to an aggregate fair market value of $100,000 for property provided for a family, or $50,000 for a single adult who is not a member of a family. The qualifying categories in § 42.002(a) include home furnishings, provisions for consumption, farm/ranch vehicles and implements, tools and books of a trade or profession, clothing, jewelry (capped at 25 percent of the aggregate limit), two firearms, athletic and sporting equipment, one motor vehicle per licensed family member or single adult, specified livestock and fowl, and household pets. Separately, § 42.001(b) exempts certain property entirely outside the dollar caps: current wages for personal services (except for court-ordered child support enforcement), professionally prescribed health aids, alimony/support/separate maintenance, and a bible or other sacred writings.'
  - gpt-5.5: grounded=True, error=None, summary='Texas exempts certain personal property from garnishment, attachment, execution, or other seizure. For property listed in Section 42.002(a), the exemption applies up to an aggregate fair market value of $100,000 for a family or $50,000 for a single adult not in a family. Certain items, including current wages for personal services, prescribed health aids, support payments, and religious sacred writings, are exempt and are not counted toward those aggregate limits.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Texas, certain personal property is exempt from seizure by creditors up to an aggregate value of $100,000 for a family or $50,000 for a single adult. The categories of property subject to this limit include home furnishings, vehicles, tools of a trade, and household pets. Some specific property, such as current wages and professionally prescribed health aids, is also exempt and is not counted toward these dollar limits.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-HOMESTEAD-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:22:07Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://statutes.capitol.texas.gov/Docs/PR/htm/PR.41.htm', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 250874, 'content_type': 'text/html', 'word_overlap_ratio': 0.053}}, {'url': 'https://statutes.capitol.texas.gov/Docs/PR/htm/PR.41.htm', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 250874, 'content_type': 'text/html', 'word_overlap_ratio': 0.143}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Tex. Prop. Code § 41.001(a), a homestead—along with one or more lots used as a burial place—is exempt from seizure to satisfy creditors' claims, with the only stated exception being encumbrances properly fixed on the homestead property. Section 41.002 caps the size of the protected homestead: an urban homestead (for a family or a single adult) may be no more than 10 acres, which may consist of one or more contiguous lots plus improvements. A rural homestead may be up to 200 acres for a family or up to 100 acres for a single adult. The text does not address other limits (such as value caps) or how urban versus rural status is determined beyond the stated use."
  - gpt-5.5: grounded=True, error=None, summary='Texas law exempts a homestead from seizure for creditors’ claims, except for encumbrances properly fixed on the homestead property. The protected homestead may be up to 10 acres for an urban home, up to 200 acres for a rural family homestead, or up to 100 acres for a rural homestead of a single adult person.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Texas, a homestead is exempt from seizure to satisfy creditor claims, except for encumbrances that are properly fixed on the property. The size of the protected homestead depends on its location. An urban homestead for a family or single adult may not exceed 10 acres, while a rural homestead may not exceed 200 acres for a family or 100 acres for a single adult.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-HOMESTEAD-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:22:07Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '10', '100', '200'], OpenAI=['10', '100', '200'], Gemini=['10', '100', '200'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Tex. Prop. Code § 41.001(a), a homestead—along with one or more lots used as a burial place—is exempt from seizure to satisfy creditors' claims, with the only stated exception being encumbrances properly fixed on the homestead property. Section 41.002 caps the size of the protected homestead: an urban homestead (for a family or a single adult) may be no more than 10 acres, which may consist of one or more contiguous lots plus improvements. A rural homestead may be up to 200 acres for a family or up to 100 acres for a single adult. The text does not address other limits (such as value caps) or how urban versus rural status is determined beyond the stated use."
  - gpt-5.5: grounded=True, error=None, summary='Texas law exempts a homestead from seizure for creditors’ claims, except for encumbrances properly fixed on the homestead property. The protected homestead may be up to 10 acres for an urban home, up to 200 acres for a rural family homestead, or up to 100 acres for a rural homestead of a single adult person.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Texas, a homestead is exempt from seizure to satisfy creditor claims, except for encumbrances that are properly fixed on the property. The size of the protected homestead depends on its location. An urban homestead for a family or single adult may not exceed 10 acres, while a rural homestead may not exceed 200 acres for a family or 100 acres for a single adult.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-WAGE-GARNISHMENT-PROHIBITION] ADVERSARIAL-GAP -- run run_20260826T190724Z, 2026-08-26T19:21:21Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** ADVERSARIAL-GAP
**Evidence:** 3 adversarial edge case(s) flagged as exposing a gap: [{'scenario': 'A Texas resident defaults on a federally guaranteed student loan and the Department of Education issues an administrative wage garnishment order to her employer; separately, the IRS serves a continuous levy on her paycheck for unpaid income taxes. Neither is child support nor spousal maintenance, and both target current wages.', 'exposes_gap': True, 'gap_description': 'The rule treats the Texas constitutional protection as absolute except for two family-law exceptions, but federal law (Supremacy Clause) permits garnishment/levy of Texas wages for federal student loans, federal taxes, and other federal debts. The exceptions list and the checklist omit any federal-debt or preemption inquiry, so the node would wrongly declare a lawful federal garnishment unconstitutional.'}, {'scenario': 'A judgment debtor is a 1099 independent contractor paid monthly commissions by a company, and separately is the sole owner of an S-corp from which he takes periodic distributions rather than a salary. The creditor serves a writ of garnishment on the paying company for amounts owed to him.', 'exposes_gap': True, 'gap_description': "The checklist's dispositive fact is only 'wages vs. bank account vs. support obligation,' but Texas courts limit the protection to 'current wages for personal service' from an employer-employee relationship; independent contractor payments, corporate distributions, rents, and similar income are generally garnishable. The rule provides no test for what qualifies as 'current wages' or whether an employment relationship exists."}, {'scenario': "A Texas-domiciled debtor works remotely for an employer headquartered in Georgia; the creditor domesticates its judgment in Georgia and garnishes the employer there under Georgia law. In a variant, the debtor's employer already issued the paycheck and it sits uncashed in the payroll office, or the wages were direct-deposited yesterday into his account.", 'exposes_gap': True, 'gap_description': "The rule assumes a single Texas forum and a clean wages/bank-account binary. It does not address choice of law or forum where an out-of-state court garnishes an out-of-state employer of a Texas debtor, nor the temporal boundary at which 'current wages' cease to be current (paid but undelivered, or freshly deposited funds that may retain exempt character under Tex. Prop. Code 42.001(d))."}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under the Texas Constitution, current wages earned for personal service can never be garnished, with only two exceptions: court-ordered child support payments and court-ordered spousal maintenance. Because ordinary consumer debt (such as credit card or medical bills) falls outside those two enumerated exceptions, a creditor holding such a debt cannot garnish a debtor's current wages. The prohibition is absolute as to current wages for personal service; the text says nothing about other property or funds that are no longer current wages."
  - gpt-5.5: grounded=True, error=None, summary='Texas prohibits garnishment of current wages for personal service, except to enforce court-ordered child support or spousal maintenance. Because ordinary consumer debt is not one of the listed exceptions, the text supports that such wages cannot be garnished for ordinary consumer debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary='The Texas Constitution states that no current wages for personal service shall ever be subject to garnishment. The only exceptions provided in the text are for court-ordered child support payments or spousal maintenance. Because ordinary consumer debt does not fall into either of these specified exceptions, the general prohibition against wage garnishment applies.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-WAGE-GARNISHMENT-PROHIBITION] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:21:21Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/constitution/texas/sections/cn001600-002800.html', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5677, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under the Texas Constitution, current wages earned for personal service can never be garnished, with only two exceptions: court-ordered child support payments and court-ordered spousal maintenance. Because ordinary consumer debt (such as credit card or medical bills) falls outside those two enumerated exceptions, a creditor holding such a debt cannot garnish a debtor's current wages. The prohibition is absolute as to current wages for personal service; the text says nothing about other property or funds that are no longer current wages."
  - gpt-5.5: grounded=True, error=None, summary='Texas prohibits garnishment of current wages for personal service, except to enforce court-ordered child support or spousal maintenance. Because ordinary consumer debt is not one of the listed exceptions, the text supports that such wages cannot be garnished for ordinary consumer debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary='The Texas Constitution states that no current wages for personal service shall ever be subject to garnishment. The only exceptions provided in the text are for court-ordered child support payments or spousal maintenance. Because ordinary consumer debt does not fall into either of these specified exceptions, the general prohibition against wage garnishment applies.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-WAGE-GARNISHMENT-PROHIBITION] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:21:21Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['2'], OpenAI=['1'], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under the Texas Constitution, current wages earned for personal service can never be garnished, with only two exceptions: court-ordered child support payments and court-ordered spousal maintenance. Because ordinary consumer debt (such as credit card or medical bills) falls outside those two enumerated exceptions, a creditor holding such a debt cannot garnish a debtor's current wages. The prohibition is absolute as to current wages for personal service; the text says nothing about other property or funds that are no longer current wages."
  - gpt-5.5: grounded=True, error=None, summary='Texas prohibits garnishment of current wages for personal service, except to enforce court-ordered child support or spousal maintenance. Because ordinary consumer debt is not one of the listed exceptions, the text supports that such wages cannot be garnished for ordinary consumer debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary='The Texas Constitution states that no current wages for personal service shall ever be subject to garnishment. The only exceptions provided in the text are for court-ordered child support payments or spousal maintenance. Because ordinary consumer debt does not fall into either of these specified exceptions, the general prohibition against wage garnishment applies.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-SOL-CONSUMER-DEBT] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:20:40Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/codes/texas/civil-practice-and-remedies-code/title-2/subtitle-b/chapter-16/subchapter-a/section-16-004/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5906, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under the cited provision, a suit on a 'debt' must be filed no later than four years after the cause of action accrues. So a Texas consumer-debt collection lawsuit is subject to a four-year limitations period, measured from the date the claim accrues. The excerpt does not define when accrual occurs or address tolling, so those points cannot be determined from this text alone."
  - gpt-5.5: grounded=True, error=None, summary='A lawsuit on a debt must be brought no later than four years after the day the cause of action accrues. The text does not separately address consumer debt, but it expressly applies to actions for “debt.”'
  - gemini-2.5-pro: grounded=True, error=None, summary='A lawsuit on a debt must be brought no later than four years after the day the cause of action accrues. The provided statute explicitly lists "debt" as an action that is subject to this four-year time limit.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:19:56Z

**File:** `rules/debt/state/texas/tx_debt_band3_discretionary_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '2', '3', '30', '75'], OpenAI=['30', '75'], Gemini=['3'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Craddock, a default judgment 'should be set aside and a new trial ordered in any case in which' three conditions are met: (1) the defendant's failure to answer was not intentional or the result of conscious indifference, but due to mistake or accident; (2) the motion sets up a meritorious defense; and (3) it is filed at a time when granting it will cause no delay or other injury to the plaintiff. So the outcome is not purely open-ended discretion — the text makes relief mandatory in form ('should be set aside ... in any case in which') once the three elements are established, though each element requires a fact-specific evaluation. Timing is fixed by rule: the motion must be filed within thirty days after the judgment is signed (Rule 329b(a)), and if no written order is signed within seventy-five days of the judgment, the motion is overruled by operation of law (Rule 329b(c))."
  - gpt-5.5: grounded=True, error=None, summary='A Texas default judgment should be set aside and a new trial ordered when the defendant’s failure to answer was not intentional or due to conscious indifference, but resulted from mistake or accident. The motion must also set up a meritorious defense and be filed at a time when granting it will not delay or otherwise injure the plaintiff; a motion for new trial must be filed within thirty days after the judgment is signed, and if not ruled on by written order within seventy-five days, it is overruled by operation of law.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A Texas default judgment should be set aside on a motion for new trial if three conditions are met. First, the defendant's failure to answer was not intentional or the result of conscious indifference, but was due to a mistake or accident. Second, the motion for new trial must set up a meritorious defense. Third, the motion must be filed at a time when granting it will not cause delay or otherwise injure the plaintiff."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-CIVIL-ANSWER-DEADLINE] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:19:02Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-412-20/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5643, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}, {'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-412-20/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5643, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 412.20(a)(3), the summons must direct the defendant to file a written pleading responding to the complaint within 30 days after the summons is served. Subdivision (a)(6) repeats this in the required notice language: the court may decide against you unless you respond within 30 days. If the defendant does not respond, subdivision (a)(4) provides that a default may be entered on the plaintiff's application and the plaintiff may obtain the relief demanded, which could include wage garnishment or the taking of money or property. The text states a general summons rule and does not set a separate deadline specific to debt-collection suits."
  - gpt-5.5: grounded=True, error=None, summary='The summons must direct the defendant to file a written pleading responding to the complaint within 30 days after the summons is served. It also warns that if the defendant does not respond within 30 days, the court may decide against them and default may be entered, potentially leading to relief such as wage garnishment or taking money or property.'
  - gemini-2.5-pro: grounded=True, error=None, summary='According to the provided text, a defendant must file a written pleading in response to the complaint within 30 days after the summons is served. The summons itself must provide notice that a failure to respond within 30 days may result in the court deciding against the defendant without them being heard. If the defendant does not respond, a default may be entered against them, which could lead to garnishment of wages or the taking of property.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-CIVIL-ANSWER-DEADLINE] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:19:02Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['30', '4', '6'], OpenAI=['30'], Gemini=['30'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 412.20(a)(3), the summons must direct the defendant to file a written pleading responding to the complaint within 30 days after the summons is served. Subdivision (a)(6) repeats this in the required notice language: the court may decide against you unless you respond within 30 days. If the defendant does not respond, subdivision (a)(4) provides that a default may be entered on the plaintiff's application and the plaintiff may obtain the relief demanded, which could include wage garnishment or the taking of money or property. The text states a general summons rule and does not set a separate deadline specific to debt-collection suits."
  - gpt-5.5: grounded=True, error=None, summary='The summons must direct the defendant to file a written pleading responding to the complaint within 30 days after the summons is served. It also warns that if the defendant does not respond within 30 days, the court may decide against them and default may be entered, potentially leading to relief such as wage garnishment or taking money or property.'
  - gemini-2.5-pro: grounded=True, error=None, summary='According to the provided text, a defendant must file a written pleading in response to the complaint within 30 days after the summons is served. The summons itself must provide notice that a failure to respond within 30 days may result in the court deciding against the defendant without them being heard. If the defendant does not respond, a default may be entered against them, which could lead to garnishment of wages or the taking of property.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-BANK-ACCOUNT-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:18:15Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-704-220/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5668, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}, {'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-704-220/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5668, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.220(a), money in a judgment debtor's deposit account is automatically exempt — without the debtor having to file any exemption claim — up to an amount equal to the minimum basic standard of adequate care for a family of four for Region 1, as established by Welfare and Institutions Code section 11452 and adjusted annually by the State Department of Social Services under section 11453. The statute thus ties the protected minimum to that annually adjusted figure rather than stating a fixed dollar amount. Subdivision (c)(1) carves out an exception: the automatic exemption does not apply to money levied upon to satisfy a judgment for wages owed (including damages and penalties), child support, or spousal support."
  - gpt-5.5: grounded=True, error=None, summary='California exempts, without requiring a claim, money in a judgment debtor’s deposit account up to an amount equal to or less than the minimum basic standard of adequate care for a family of four for Region 1, as adjusted annually by the State Department of Social Services. This automatic exemption does not apply when the money is levied to satisfy a judgment for wages owed, child support, or spousal support; “wages owed” includes damages and penalties.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-BANK-ACCOUNT-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:18:15Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '4'], OpenAI=['1', '4'], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.220(a), money in a judgment debtor's deposit account is automatically exempt — without the debtor having to file any exemption claim — up to an amount equal to the minimum basic standard of adequate care for a family of four for Region 1, as established by Welfare and Institutions Code section 11452 and adjusted annually by the State Department of Social Services under section 11453. The statute thus ties the protected minimum to that annually adjusted figure rather than stating a fixed dollar amount. Subdivision (c)(1) carves out an exception: the automatic exemption does not apply to money levied upon to satisfy a judgment for wages owed (including damages and penalties), child support, or spousal support."
  - gpt-5.5: grounded=True, error=None, summary='California exempts, without requiring a claim, money in a judgment debtor’s deposit account up to an amount equal to or less than the minimum basic standard of adequate care for a family of four for Region 1, as adjusted annually by the State Department of Social Services. This automatic exemption does not apply when the money is levied to satisfy a judgment for wages owed, child support, or spousal support; “wages owed” includes damages and penalties.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-VEHICLE-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:17:15Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-704-010/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5668, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.010(a), a judgment debtor may exempt up to $7,500 in any combination of aggregate equity in motor vehicles, proceeds of an execution sale of a motor vehicle, and proceeds of insurance or other indemnification for a vehicle's loss, damage, or destruction. Subdivision (d) adds that if the debtor owns only one motor vehicle and it is sold at an execution sale, the sale proceeds are automatically exempt up to $7,500 without the debtor having to file a claim, with the levying officer permitted to rely on Department of Motor Vehicles records to confirm the debtor has only one vehicle. In that single-vehicle situation, the subdivision (a) exemption is not separately available."
  - gpt-5.5: grounded=True, error=None, summary='California exempts up to $7,500 for any combination of aggregate equity in motor vehicles, proceeds from an execution sale of a motor vehicle, and insurance or indemnification proceeds for loss, damage, or destruction of a motor vehicle. If the judgment debtor has only one motor vehicle and it is sold at an execution sale, $7,500 of the sale proceeds is exempt without making a claim, and the subdivision (a) exemption is not available in that case.'
  - gemini-2.5-pro: grounded=True, error=None, summary="California law provides a $7,500 exemption for a person's equity in motor vehicles. This exemption applies to the aggregate equity in motor vehicles, proceeds from an execution sale, or insurance proceeds from loss or damage. If a debtor has only one motor vehicle that is sold, the proceeds from that sale are automatically exempt up to $7,500 without a claim being made."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-HOMESTEAD-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:16:31Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-704-730/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5668, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.730(a), a judgment debtor's homestead exemption equals the greater of (1) the countywide median sale price for a single-family home in the calendar year before the year the exemption is claimed, capped at $600,000, or (2) a $300,000 floor. So the exemption is never less than $300,000 and never more than $600,000 under the baseline figures. Subdivision (b) provides that both figures adjust annually for inflation starting January 1, 2022, using the change in the annual California Consumer Price Index for All Urban Consumers published by the Department of Industrial Relations for the most recent one-year period ending December 31 before the adjustment, rounded to the nearest $25."
  - gpt-5.5: grounded=True, error=None, summary="The homestead exemption amount is the greater of either the prior calendar year's countywide median sale price for a single-family home, capped at $600,000, or $300,000. These amounts adjust annually for inflation beginning January 1, 2022, based on the California CPI for All Urban Consumers, rounded to the nearest $25."
  - gemini-2.5-pro: grounded=True, error=None, summary="The California homestead exemption is the greater of two amounts: either the county's median sale price for a single-family home from the prior year (up to a maximum of $600,000), or a baseline of $300,000. This means the exemption will always be at least $300,000. The law also states that these specified dollar amounts are adjusted annually for inflation based on the California Consumer Price Index."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-HOMESTEAD-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:16:31Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['$25', '$300000', '$600000', '1', '2', '2022', '31'], OpenAI=['$25', '$300000', '$600000', '1', '2022'], Gemini=['$300000', '$600000', '2'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 704.730(a), a judgment debtor's homestead exemption equals the greater of (1) the countywide median sale price for a single-family home in the calendar year before the year the exemption is claimed, capped at $600,000, or (2) a $300,000 floor. So the exemption is never less than $300,000 and never more than $600,000 under the baseline figures. Subdivision (b) provides that both figures adjust annually for inflation starting January 1, 2022, using the change in the annual California Consumer Price Index for All Urban Consumers published by the Department of Industrial Relations for the most recent one-year period ending December 31 before the adjustment, rounded to the nearest $25."
  - gpt-5.5: grounded=True, error=None, summary="The homestead exemption amount is the greater of either the prior calendar year's countywide median sale price for a single-family home, capped at $600,000, or $300,000. These amounts adjust annually for inflation beginning January 1, 2022, based on the California CPI for All Urban Consumers, rounded to the nearest $25."
  - gemini-2.5-pro: grounded=True, error=None, summary="The California homestead exemption is the greater of two amounts: either the county's median sale price for a single-family home from the prior year (up to a maximum of $600,000), or a baseline of $300,000. This means the exemption will always be at least $300,000. The law also states that these specified dollar amounts are adjusted annually for inflation based on the California Consumer Price Index."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-WAGE-GARNISHMENT-LIMIT] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:15:21Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-706-050/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5668, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}, {'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-706-050/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5668, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under § 706.050(a), unless another provision of the chapter says otherwise, the maximum amount of a judgment debtor's disposable earnings that may be levied under an earnings withholding order in any workweek is the lesser of (1) 20% of that week's disposable earnings, or (2) 40% of the amount by which that week's disposable earnings exceed 48 times the applicable minimum hourly wage. The applicable wage is the state minimum hourly wage in effect when the earnings are payable, or the local minimum wage if the debtor works where the local minimum is higher. This version of the section became operative September 1, 2023. Note: the quoted text states a general garnishment cap and does not itself contain a separate rule specific to consumer-debt judgments, which could appear elsewhere in the chapter under the 'except as otherwise provided' clause."
  - gpt-5.5: grounded=True, error=None, summary='As of September 1, 2023, the maximum disposable earnings of an individual judgment debtor subject to an earnings withholding order for a workweek is the lesser of: 20% of that week’s disposable earnings, or 40% of the amount by which that week’s disposable earnings exceed 48 times the applicable minimum hourly wage. The state minimum wage is used unless the debtor works where the local minimum wage is higher, in which case the local minimum wage is used.'
  - gemini-2.5-pro: grounded=True, error=None, summary="As of September 1, 2023, the maximum amount of an individual's weekly disposable earnings that can be garnished is the lesser of two figures. The first is 20% of the individual's disposable earnings for that week. The second is 40% of the amount by which the weekly earnings exceed 48 times the applicable state or local minimum wage."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-WAGE-GARNISHMENT-LIMIT] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:15:21Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '2', '20%', '2023', '40%', '48'], OpenAI=['1', '20%', '2023', '40%', '48'], Gemini=['1', '2', '20%', '2023', '40%', '48'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under § 706.050(a), unless another provision of the chapter says otherwise, the maximum amount of a judgment debtor's disposable earnings that may be levied under an earnings withholding order in any workweek is the lesser of (1) 20% of that week's disposable earnings, or (2) 40% of the amount by which that week's disposable earnings exceed 48 times the applicable minimum hourly wage. The applicable wage is the state minimum hourly wage in effect when the earnings are payable, or the local minimum wage if the debtor works where the local minimum is higher. This version of the section became operative September 1, 2023. Note: the quoted text states a general garnishment cap and does not itself contain a separate rule specific to consumer-debt judgments, which could appear elsewhere in the chapter under the 'except as otherwise provided' clause."
  - gpt-5.5: grounded=True, error=None, summary='As of September 1, 2023, the maximum disposable earnings of an individual judgment debtor subject to an earnings withholding order for a workweek is the lesser of: 20% of that week’s disposable earnings, or 40% of the amount by which that week’s disposable earnings exceed 48 times the applicable minimum hourly wage. The state minimum wage is used unless the debtor works where the local minimum wage is higher, in which case the local minimum wage is used.'
  - gemini-2.5-pro: grounded=True, error=None, summary="As of September 1, 2023, the maximum amount of an individual's weekly disposable earnings that can be garnished is the lesser of two figures. The first is 20% of the individual's disposable earnings for that week. The second is 40% of the amount by which the weekly earnings exceed 48 times the applicable state or local minimum wage."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-ORAL-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:14:31Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/codes/california/code-ccp/part-2/title-2/chapter-3/section-339/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5743, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under Cal. Code Civ. Proc. § 339(1), an action on a contract, obligation, or liability that is not founded upon a written instrument must be brought within two years. So a consumer-debt suit based on an oral or otherwise unwritten agreement is subject to a two-year limitations period. The text carves out exceptions for matters governed by Commercial Code section 2725 and section 337(2), and it separately covers claims evidenced by title certificates, abstracts, guaranties, or title insurance policies, for which the cause of action does not accrue until the loss or damage is discovered.'
  - gpt-5.5: grounded=True, error=None, summary='An action upon a contract, obligation, or liability that is not founded upon a written instrument must be brought within two years. The excerpt does not separately address consumer debt, but it does state the limitations period for unwritten contracts generally.'
  - gemini-2.5-pro: grounded=True, error=None, summary='According to the provided text, the statute of limitations for a lawsuit based on a contract that is not in writing is two years. The text refers to this as "an action upon a contract, obligation or liability not founded upon an instrument of writing." The statute mentions that exceptions to this rule may exist in other sections of the law, but does not describe them.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-WRITTEN-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:13:44Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/codes/california/code-ccp/part-2/title-2/chapter-3/section-337/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5743, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}, {'url': 'https://law.justia.com/codes/california/code-ccp/part-2/title-2/chapter-3/section-337/', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 403, 'content_length': 5743, 'content_type': 'text/html; charset=UTF-8', 'word_overlap_ratio': 0.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 337(a), an action on a contract, obligation, or liability founded on a written instrument must be brought within four years (with an exception referencing Section 336a, and a special three-month limit for deficiency-type money judgments after a trustee's/mortgage power-of-sale sale). Section 337(d) adds that once that period has run, no one may file suit or initiate arbitration or other legal proceedings to collect the debt. The limitations period may be extended only as provided in Section 360."
  - gpt-5.5: grounded=True, error=None, summary='An action on a contract, obligation, or liability founded on a written instrument must be brought within four years. Once that limitations period has run, a person may not sue, initiate arbitration, or start another legal proceeding to collect the debt, and the period may be extended only under Section 360.'
  - gemini-2.5-pro: grounded=True, error=None, summary='An action upon a contract founded on a written instrument must be commenced within four years. The text specifies a much shorter three-month limitation for lawsuits seeking a money judgment on a debt that was secured by a deed of trust or mortgage on real property after that property has been sold. Once the applicable time period has run, a person is prohibited from bringing a suit or other legal proceeding to collect the debt.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-WRITTEN-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:13:44Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '3', '4'], OpenAI=['4'], Gemini=['3', '4'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under Cal. Code Civ. Proc. § 337(a), an action on a contract, obligation, or liability founded on a written instrument must be brought within four years (with an exception referencing Section 336a, and a special three-month limit for deficiency-type money judgments after a trustee's/mortgage power-of-sale sale). Section 337(d) adds that once that period has run, no one may file suit or initiate arbitration or other legal proceedings to collect the debt. The limitations period may be extended only as provided in Section 360."
  - gpt-5.5: grounded=True, error=None, summary='An action on a contract, obligation, or liability founded on a written instrument must be brought within four years. Once that limitations period has run, a person may not sue, initiate arbitration, or start another legal proceeding to collect the debt, and the period may be extended only under Section 360.'
  - gemini-2.5-pro: grounded=True, error=None, summary='An action upon a contract founded on a written instrument must be commenced within four years. The text specifies a much shorter three-month limitation for lawsuits seeking a money judgment on a debt that was secured by a deed of trust or mortgage on real property after that property has been sold. Once the applicable time period has run, a person is prohibited from bringing a suit or other legal proceeding to collect the debt.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:12:51Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 3 of 5 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 10596, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 0.286}}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 10596, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 0.25}}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 10596, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 0.333}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="A notice is compliant only if, within five days of the initial communication (or in that communication itself), the collector provides the consumer the amount of the debt, the name of the creditor owed, and the three statements about the 30-day dispute window, verification upon written dispute, and the right to request the original creditor's name and address (15 U.S.C. § 1692g(a)); under Regulation F the notice must also contain the full validation information in 12 C.F.R. § 1006.34(c), including the debt-collector communication disclosure, itemization details, dispute-window end date, and response prompts, delivered as required by § 1006.34(a)(1). The consumer is still within the dispute window if fewer than 30 days have passed since receipt of the validation information, measured from the date the information was provided to 30 days after actual or assumed receipt, with receipt presumed no earlier than five business days (excluding Saturdays, Sundays, and legal public holidays) after it was sent (12 C.F.R. § 1006.34(b)(5)). A timely written dispute or original-creditor request triggers § 1692g(b): the collector must cease collection of the disputed portion until verification, a judgment copy, or the original creditor's name and address is mailed to the consumer; otherwise collection may continue during the 30 days. The excerpt supplies the governing standard and timing rules but contains no facts about the particular notice or dates, so the ultimate yes/no answer depends on applying these elements to the actual notice and mailing/receipt dates."
  - gpt-5.5: grounded=False, error=None, summary='The text states that a debt collector must provide validation information in the initial communication, within five days after it, or orally in the initial communication, and the required content includes debt information, consumer-protection statements, and response information. The consumer’s validation/dispute period runs from when the validation information is provided until 30 days after the consumer receives or is assumed to receive it, with receipt assumable at least five business days after provision. However, the provided text contains no facts about what notice was sent, what it contained, when it was provided, or when the consumer received it, so compliance and whether the dispute window remains open cannot be determined.'
  - gemini-2.5-pro: grounded=True, error=None, summary='The provided texts do not contain facts to determine if a compliant notice was provided in a specific case, but they outline the legal requirements. A debt collector must provide a validation notice with specific information either orally in the initial communication or in writing within five days of it. The consumer has a 30-day "validation period" to dispute the debt, which ends 30 days after the consumer receives the notice; the collector may assume receipt occurs five business days after providing it.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:12:51Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['3', '30', '5'], OpenAI=['30', '5'], Gemini=['30', '5'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="A notice is compliant only if, within five days of the initial communication (or in that communication itself), the collector provides the consumer the amount of the debt, the name of the creditor owed, and the three statements about the 30-day dispute window, verification upon written dispute, and the right to request the original creditor's name and address (15 U.S.C. § 1692g(a)); under Regulation F the notice must also contain the full validation information in 12 C.F.R. § 1006.34(c), including the debt-collector communication disclosure, itemization details, dispute-window end date, and response prompts, delivered as required by § 1006.34(a)(1). The consumer is still within the dispute window if fewer than 30 days have passed since receipt of the validation information, measured from the date the information was provided to 30 days after actual or assumed receipt, with receipt presumed no earlier than five business days (excluding Saturdays, Sundays, and legal public holidays) after it was sent (12 C.F.R. § 1006.34(b)(5)). A timely written dispute or original-creditor request triggers § 1692g(b): the collector must cease collection of the disputed portion until verification, a judgment copy, or the original creditor's name and address is mailed to the consumer; otherwise collection may continue during the 30 days. The excerpt supplies the governing standard and timing rules but contains no facts about the particular notice or dates, so the ultimate yes/no answer depends on applying these elements to the actual notice and mailing/receipt dates."
  - gpt-5.5: grounded=False, error=None, summary='The text states that a debt collector must provide validation information in the initial communication, within five days after it, or orally in the initial communication, and the required content includes debt information, consumer-protection statements, and response information. The consumer’s validation/dispute period runs from when the validation information is provided until 30 days after the consumer receives or is assumed to receive it, with receipt assumable at least five business days after provision. However, the provided text contains no facts about what notice was sent, what it contained, when it was provided, or when the consumer received it, so compliance and whether the dispute window remains open cannot be determined.'
  - gemini-2.5-pro: grounded=True, error=None, summary='The provided texts do not contain facts to determine if a compliant notice was provided in a specific case, but they outline the legal requirements. A debt collector must provide a validation notice with specific information either orally in the initial communication or in writing within five days of it. The consumer has a 30-day "validation period" to dispute the debt, which ends 30 days after the consumer receives the notice; the collector may assume receipt occurs five business days after providing it.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:11:40Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692f', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 35834, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 1.0}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692f imposes a general ban on a debt collector's use of unfair or unconscionable means to collect a debt, then lists non-exhaustive examples of violations. These include collecting any amount (interest, fees, charges, expenses) not expressly authorized by the debt agreement or permitted by law; accepting a check postdated more than five days without written notice of intent to deposit given 3-10 business days beforehand; soliciting postdated instruments to threaten or institute criminal prosecution; depositing or threatening to deposit a postdated instrument early; causing a person to incur communication charges by concealing the communication's true purpose; and taking or threatening nonjudicial dispossession or disablement of property where there is no present enforceable right to possession, no present intent to take possession, or the property is exempt by law. It also bars communicating with a consumer about a debt by post card and using any language or symbol on a mailed envelope other than the collector's address, though a business name may be used if it does not indicate the debt collection business."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect or attempt to collect any debt. The listed violations include collecting unauthorized amounts; certain improper handling or solicitation of postdated checks; causing communication charges by concealing the purpose of a communication; improper nonjudicial repossession or disablement actions; communicating about a debt by postcard; and using prohibited language or symbols on mailed envelopes or telegrams.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect a debt, which includes a number of specific, prohibited actions. These forbidden acts include collecting any amount not authorized by the agreement or law, misusing postdated checks, and taking or threatening to take property without a present right to do so. Other prohibited practices are communicating about a debt via postcard and using any language or symbol on an envelope, other than an address, that indicates the communication is from a debt collector.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:11:40Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['10', '3', '5'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692f imposes a general ban on a debt collector's use of unfair or unconscionable means to collect a debt, then lists non-exhaustive examples of violations. These include collecting any amount (interest, fees, charges, expenses) not expressly authorized by the debt agreement or permitted by law; accepting a check postdated more than five days without written notice of intent to deposit given 3-10 business days beforehand; soliciting postdated instruments to threaten or institute criminal prosecution; depositing or threatening to deposit a postdated instrument early; causing a person to incur communication charges by concealing the communication's true purpose; and taking or threatening nonjudicial dispossession or disablement of property where there is no present enforceable right to possession, no present intent to take possession, or the property is exempt by law. It also bars communicating with a consumer about a debt by post card and using any language or symbol on a mailed envelope other than the collector's address, though a business name may be used if it does not indicate the debt collection business."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect or attempt to collect any debt. The listed violations include collecting unauthorized amounts; certain improper handling or solicitation of postdated checks; causing communication charges by concealing the purpose of a communication; improper nonjudicial repossession or disablement actions; communicating about a debt by postcard; and using prohibited language or symbols on mailed envelopes or telegrams.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect a debt, which includes a number of specific, prohibited actions. These forbidden acts include collecting any amount not authorized by the agreement or law, misusing postdated checks, and taking or threatening to take property without a present right to do so. Other prohibited practices are communicating about a debt via postcard and using any language or symbol on an envelope, other than an address, that indicates the communication is from a debt collector.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:10:10Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.18', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 10596, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 0.143}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means to collect a debt, and then lists non-exhaustive examples that violate it: falsely claiming government affiliation/bonding (1); misstating the character, amount, or legal status of a debt or the services or compensation involved (2); falsely implying an attorney is involved (3); threatening arrest, imprisonment, seizure, garnishment, attachment, or sale of property or wages when such action is unlawful or not intended (4); threatening any action that cannot legally be or is not intended to be taken (5); communicating credit information known to be false, including failing to note a debt is disputed (8); using documents simulating court or agency papers (9) or falsely representing documents to be, or not to be, legal process (13, 15); any false or deceptive means to collect or to obtain consumer information (10); failing to give the required 'attempting to collect a debt' disclosures (11); falsely implying accounts were sold to innocent purchasers for value (12); using a name other than the collector's true name (14); and falsely implying the collector is or works for a consumer reporting agency (16)."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use any false, deceptive, or misleading representation or means in connection with collecting a debt. The statute lists prohibited conduct including false claims about government affiliation, the debt’s character/amount/legal status, attorney involvement, legal consequences of nonpayment, threats of actions that are illegal or unintended, false credit reporting, simulated official documents, deceptive collection means, false legal-process statements, use of a non-true business name, and false claims of affiliation with a consumer reporting agency. Debt collectors also must give the required debt-collection disclosure in initial and subsequent consumer communications, with an exception for formal pleadings in legal actions.'
  - gemini-2.5-pro: grounded=True, error=None, summary="Debt collectors are broadly prohibited from using any false, deceptive, or misleading representations. This includes misrepresenting a debt's amount or status, threatening actions they cannot or do not intend to take like arrest, falsely implying they are an attorney or affiliated with the government, or using documents that look like official court papers. Collectors must also disclose in their initial communication that they are attempting to collect a debt and, in subsequent communications, that the message is from a debt collector, unless it is a formal legal pleading."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:10:10Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '10', '11', '12', '13', '14', '15', '16', '2', '3', '4', '5', '8', '9'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means to collect a debt, and then lists non-exhaustive examples that violate it: falsely claiming government affiliation/bonding (1); misstating the character, amount, or legal status of a debt or the services or compensation involved (2); falsely implying an attorney is involved (3); threatening arrest, imprisonment, seizure, garnishment, attachment, or sale of property or wages when such action is unlawful or not intended (4); threatening any action that cannot legally be or is not intended to be taken (5); communicating credit information known to be false, including failing to note a debt is disputed (8); using documents simulating court or agency papers (9) or falsely representing documents to be, or not to be, legal process (13, 15); any false or deceptive means to collect or to obtain consumer information (10); failing to give the required 'attempting to collect a debt' disclosures (11); falsely implying accounts were sold to innocent purchasers for value (12); using a name other than the collector's true name (14); and falsely implying the collector is or works for a consumer reporting agency (16)."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use any false, deceptive, or misleading representation or means in connection with collecting a debt. The statute lists prohibited conduct including false claims about government affiliation, the debt’s character/amount/legal status, attorney involvement, legal consequences of nonpayment, threats of actions that are illegal or unintended, false credit reporting, simulated official documents, deceptive collection means, false legal-process statements, use of a non-true business name, and false claims of affiliation with a consumer reporting agency. Debt collectors also must give the required debt-collection disclosure in initial and subsequent consumer communications, with an exception for formal pleadings in legal actions.'
  - gemini-2.5-pro: grounded=True, error=None, summary="Debt collectors are broadly prohibited from using any false, deceptive, or misleading representations. This includes misrepresenting a debt's amount or status, threatening actions they cannot or do not intend to take like arrest, falsely implying they are an attorney or affiliated with the government, or using documents that look like official court papers. Collectors must also disclose in their initial communication that they are attempting to collect a debt and, in subsequent communications, that the message is from a debt collector, unless it is a formal legal pleading."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] CITATION-CHECK-FAILED -- run run_20260826T190724Z, 2026-08-26T19:09:17Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 10596, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 0.25}}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None, 'diagnostics': {'http_status': 200, 'content_length': 10596, 'content_type': 'text/html; charset=utf-8', 'word_overlap_ratio': 0.214}}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the harassment prohibition in § 1006.14(b)(1) and FDCPA § 806(5) if it places calls to a particular person about a particular debt neither more than seven times in seven consecutive days, nor within seven consecutive days after having had a telephone conversation with that person about that debt. Paragraph (b)(2)(ii) flips the presumption: exceeding either of those two frequencies creates a presumption that the collector violated (b)(1) and FDCPA § 806(5). The limits are applied per 'particular debt,' meaning each individual debt in collection, except that multiple student loan debts serviced under a single account number when obtained by the collector count as one particular debt (§ 1006.14(b)(4))."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is presumed to comply if, for a particular person and a particular debt, it does not place more than seven calls within seven consecutive days and does not call within seven consecutive days after having a telephone conversation with that person about that debt. A debt collector is presumed to violate the rule if it exceeds either of those call-frequency limits. For this purpose, a “particular debt” generally means each debt in collection, with a special rule grouping certain student loan debts serviced under one account number.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to have violated the law if they place a telephone call to a person about a particular debt more than seven times within seven consecutive days. This presumption also applies if the collector calls within seven consecutive days after having a telephone conversation with that person regarding the debt. For this rule, each debt is generally treated separately, but all student loans serviced under a single account number are treated as a single 'particular debt'."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:09:17Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '2', '7'], OpenAI=['1', '7'], Gemini=['7'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the harassment prohibition in § 1006.14(b)(1) and FDCPA § 806(5) if it places calls to a particular person about a particular debt neither more than seven times in seven consecutive days, nor within seven consecutive days after having had a telephone conversation with that person about that debt. Paragraph (b)(2)(ii) flips the presumption: exceeding either of those two frequencies creates a presumption that the collector violated (b)(1) and FDCPA § 806(5). The limits are applied per 'particular debt,' meaning each individual debt in collection, except that multiple student loan debts serviced under a single account number when obtained by the collector count as one particular debt (§ 1006.14(b)(4))."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is presumed to comply if, for a particular person and a particular debt, it does not place more than seven calls within seven consecutive days and does not call within seven consecutive days after having a telephone conversation with that person about that debt. A debt collector is presumed to violate the rule if it exceeds either of those call-frequency limits. For this purpose, a “particular debt” generally means each debt in collection, with a special rule grouping certain student loan debts serviced under one account number.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to have violated the law if they place a telephone call to a person about a particular debt more than seven times within seven consecutive days. This presumption also applies if the collector calls within seven consecutive days after having a telephone conversation with that person regarding the debt. For this rule, each debt is generally treated separately, but all student loans serviced under a single account number are treated as a single 'particular debt'."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b] MODEL-DISAGREEMENT -- run run_20260826T190724Z, 2026-08-26T19:08:28Z

**File:** `rules/debt/federal/fcra_furnisher_dispute_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Once a furnisher receives notice from a consumer reporting agency under § 1681i(a)(2) that a consumer disputes the completeness or accuracy of information it supplied, the furnisher must investigate the disputed information, review all relevant information the agency provided with the notice, and report the investigation's results back to that agency. If the investigation shows the information is incomplete or inaccurate, the furnisher must also report those results to all other nationwide consumer reporting agencies it furnished the information to, and must promptly modify, delete, or permanently block reporting of any item found inaccurate, incomplete, or unverifiable. All of these investigations, reviews, and reports must be completed within the same time period § 1681i(a)(1) gives the credit bureau to complete its reinvestigation."
  - gpt-5.5: grounded=True, error=None, summary='After receiving notice from a consumer reporting agency that a consumer disputes the completeness or accuracy of information the person furnished, the furnisher must investigate the disputed information, review all relevant information provided by the agency, and report the investigation results back to the agency. If the information is found incomplete, inaccurate, or cannot be verified, the furnisher must take appropriate reporting action by modifying, deleting, or permanently blocking the item, and in some cases report results to other nationwide consumer reporting agencies to which it furnished the information. The furnisher must complete the required investigations, reviews, and reports within the time period that applies to the consumer reporting agency’s required actions under section 1681i(a)(1).'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [PURGE NOTE 2026-08-26] 72 entries removed -- auth-artifact run, not real disagreements

**Removed:** all 72 entries filed under `run run_20260826T171949Z` (2026-08-26 17:19-17:24 PT). Andy confirmed this run used malformed API keys (his own key-formatting error, not the runner's or the models'): all three providers returned authentication failures on every single node (Anthropic `401 invalid x-api-key`, OpenAI `401 invalid_api_key`, Gemini `400 API_KEY_INVALID`). Since every node in that run failed identically on auth, the resulting `MODEL-DISAGREEMENT` and `CITATION-CHECK-FAILED` entries filed by the runner carried no legal-content signal whatsoever -- purging them per Andy's explicit instruction, logged here (not silently) per the append-only discipline. **Entries from `run_20260826T174558Z` and `run_20260826T175559Z` (Andy's run 3, valid keys, real 200-level API responses) are untouched below** -- those are the genuine findings this queue exists to hold.

---

### [AZ-HOMESTEAD-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T18:04:32Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-33-property/az-rev-st-sect-33-1101/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/az/title-33-property/az-rev-st-sect-33-1101/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under A.R.S. § 33-1101(A), any Arizona resident aged eighteen or older, whether married or single, may hold a homestead exempt from attachment, execution, and forced sale up to $400,000 in value. The exemption covers one of the following: an interest in real property in one compact body with a dwelling house in which the person resides, an interest in a condominium or cooperative in which the person resides, a mobile home in which the person resides, or such a mobile home plus the land it sits on. Under subsection (C), the exemption (up to the same value, as adjusted by subsection D) automatically attaches to identifiable cash proceeds from a voluntary or involuntary sale of the property, and continues for eighteen months after the sale or until a new homestead is established with the proceeds, whichever is shorter.'
  - gpt-5.5: grounded=True, error=None, summary='An Arizona resident who is at least eighteen, whether married or single, may hold a homestead exempt from attachment, execution, and forced sale up to $400,000 in value. The exemption may apply to the person’s residence interest in real property with a dwelling, a condominium or cooperative, a mobile home, or a mobile home plus the land where it is located. The exemption also automatically attaches to identifiable cash proceeds from a voluntary or involuntary sale, continuing for eighteen months after sale or until a new homestead is established with the proceeds, whichever is shorter.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-HOMESTEAD-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T18:04:32Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['$400000', '1101', '33'], OpenAI=['$400000'], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under A.R.S. § 33-1101(A), any Arizona resident aged eighteen or older, whether married or single, may hold a homestead exempt from attachment, execution, and forced sale up to $400,000 in value. The exemption covers one of the following: an interest in real property in one compact body with a dwelling house in which the person resides, an interest in a condominium or cooperative in which the person resides, a mobile home in which the person resides, or such a mobile home plus the land it sits on. Under subsection (C), the exemption (up to the same value, as adjusted by subsection D) automatically attaches to identifiable cash proceeds from a voluntary or involuntary sale of the property, and continues for eighteen months after the sale or until a new homestead is established with the proceeds, whichever is shorter.'
  - gpt-5.5: grounded=True, error=None, summary='An Arizona resident who is at least eighteen, whether married or single, may hold a homestead exempt from attachment, execution, and forced sale up to $400,000 in value. The exemption may apply to the person’s residence interest in real property with a dwelling, a condominium or cooperative, a mobile home, or a mobile home plus the land where it is located. The exemption also automatically attaches to identifiable cash proceeds from a voluntary or involuntary sale, continuing for eighteen months after sale or until a new homestead is established with the proceeds, whichever is shorter.'
  - gemini-2.5-pro: grounded=None, error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-WAGE-GARNISHMENT-LIMIT] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T18:03:31Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-33-property/az-rev-st-sect-33-1131/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/az/title-33-property/az-rev-st-sect-33-1131/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under A.R.S. § 33-1131(B), for an ordinary (non-support) judgment such as a consumer debt, a creditor may garnish no more than the lesser of (1) 10% of the debtor's disposable earnings for the workweek, or (2) the amount by which those weekly disposable earnings exceed 60 times the applicable minimum hourly wage at the time the earnings are payable. The 'applicable minimum hourly wage' is whichever of the federal, state, or local minimum wage is highest. The only stated exception is subsection C, which applies to orders for support of a person (where one-half of disposable earnings per pay period is exempt) and thus does not govern consumer-debt judgments."
  - gpt-5.5: grounded=True, error=None, summary='Except for support orders, the maximum disposable earnings subject to process for any workweek is the lesser of: (1) ten percent of disposable earnings for that week, or (2) the amount by which that week’s disposable earnings exceed sixty times the highest applicable federal, state, or local minimum hourly wage. Support orders are treated differently, with one-half of disposable earnings for any pay period exempt from process.'
  - gemini-2.5-pro: grounded=True, error=None, summary="For a consumer debt, the maximum part of a debtor's disposable earnings that can be garnished for any workweek is the lesser of two amounts. The first amount is ten percent of the disposable earnings for that week. The second is the amount by which those disposable earnings exceed sixty times the highest applicable federal, state, or local minimum hourly wage. This cap does not apply to orders for the support of a person."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-WAGE-GARNISHMENT-LIMIT] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T18:03:31Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '10%', '1131', '2', '33', '60'], OpenAI=['1', '2'], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under A.R.S. § 33-1131(B), for an ordinary (non-support) judgment such as a consumer debt, a creditor may garnish no more than the lesser of (1) 10% of the debtor's disposable earnings for the workweek, or (2) the amount by which those weekly disposable earnings exceed 60 times the applicable minimum hourly wage at the time the earnings are payable. The 'applicable minimum hourly wage' is whichever of the federal, state, or local minimum wage is highest. The only stated exception is subsection C, which applies to orders for support of a person (where one-half of disposable earnings per pay period is exempt) and thus does not govern consumer-debt judgments."
  - gpt-5.5: grounded=True, error=None, summary='Except for support orders, the maximum disposable earnings subject to process for any workweek is the lesser of: (1) ten percent of disposable earnings for that week, or (2) the amount by which that week’s disposable earnings exceed sixty times the highest applicable federal, state, or local minimum hourly wage. Support orders are treated differently, with one-half of disposable earnings for any pay period exempt from process.'
  - gemini-2.5-pro: grounded=True, error=None, summary="For a consumer debt, the maximum part of a debtor's disposable earnings that can be garnished for any workweek is the lesser of two amounts. The first amount is ten percent of the disposable earnings for that week. The second is the amount by which those disposable earnings exceed sixty times the highest applicable federal, state, or local minimum hourly wage. This cap does not apply to orders for the support of a person."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-ORAL-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T18:02:38Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-12-courts-and-civil-proceedings/az-rev-st-sect-12-543/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under A.R.S. § 12-543, a lawsuit on a debt that is not evidenced by a written contract, or on a stated or open account, must be filed within three years after the cause of action accrues, and not afterward. For stated or open accounts, the statute adds that no item of the account is barred so long as any item on it was incurred within the three years immediately before the action is brought. The three-year period also covers claims for relief based on fraud or mistake, which do not accrue until the aggrieved party discovers the facts constituting the fraud or mistake; mutual and current merchant-to-merchant trade accounts are excluded from the open-account category.'
  - gpt-5.5: grounded=True, error=None, summary='An action for debt not evidenced by a written contract must be commenced and prosecuted within three years after the cause of action accrues. Actions on stated or open accounts are also subject to a three-year period, and no item of a stated or open account is barred if any item was incurred within the three years immediately before the action is brought.'
  - gemini-2.5-pro: grounded=True, error=None, summary='According to the provided text, a lawsuit must be started within three years after the cause of action accrues for a debt that is not based on a written contract. This three-year time limit also applies to actions on open accounts. The statute does not differentiate between consumer and other types of debt, applying this rule generally.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-ORAL-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T18:02:38Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['12', '543'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under A.R.S. § 12-543, a lawsuit on a debt that is not evidenced by a written contract, or on a stated or open account, must be filed within three years after the cause of action accrues, and not afterward. For stated or open accounts, the statute adds that no item of the account is barred so long as any item on it was incurred within the three years immediately before the action is brought. The three-year period also covers claims for relief based on fraud or mistake, which do not accrue until the aggrieved party discovers the facts constituting the fraud or mistake; mutual and current merchant-to-merchant trade accounts are excluded from the open-account category.'
  - gpt-5.5: grounded=True, error=None, summary='An action for debt not evidenced by a written contract must be commenced and prosecuted within three years after the cause of action accrues. Actions on stated or open accounts are also subject to a three-year period, and no item of a stated or open account is barred if any item was incurred within the three years immediately before the action is brought.'
  - gemini-2.5-pro: grounded=True, error=None, summary='According to the provided text, a lawsuit must be started within three years after the cause of action accrues for a debt that is not based on a written contract. This three-year time limit also applies to actions on open accounts. The statute does not differentiate between consumer and other types of debt, applying this rule generally.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-WRITTEN-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T18:01:55Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-12-courts-and-civil-proceedings/az-rev-st-sect-12-548/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/az/title-12-courts-and-civil-proceedings/az-rev-st-sect-12-548/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under A.R.S. § 12-548(A), a debt action must be filed within six years after the cause of action accrues when the debt is evidenced by or founded on a written contract executed in Arizona, or on a credit card as defined in § 13-2101(3)(a). After that six-year period, the action may not be brought. Subsection (B) adds that if another jurisdiction's limitations period conflicts with Arizona's for such a debt action, this Arizona six-year statute controls."
  - gpt-5.5: grounded=True, error=None, summary='A debt action must be commenced and prosecuted within six years after the cause of action accrues if the debt is evidenced by or founded on a written contract executed in Arizona or on a credit card. If another jurisdiction’s statute of limitations conflicts with Arizona’s for such a debt action, Arizona’s six-year statute applies.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Arizona, a lawsuit for debt must be filed within six years after the cause of action accrues. This time limit applies if the debt is based on a written contract executed within the state. The six-year limit also applies to debt founded on a credit card.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-WRITTEN-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T18:01:55Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['12', '13', '2101', '3', '548'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under A.R.S. § 12-548(A), a debt action must be filed within six years after the cause of action accrues when the debt is evidenced by or founded on a written contract executed in Arizona, or on a credit card as defined in § 13-2101(3)(a). After that six-year period, the action may not be brought. Subsection (B) adds that if another jurisdiction's limitations period conflicts with Arizona's for such a debt action, this Arizona six-year statute controls."
  - gpt-5.5: grounded=True, error=None, summary='A debt action must be commenced and prosecuted within six years after the cause of action accrues if the debt is evidenced by or founded on a written contract executed in Arizona or on a credit card. If another jurisdiction’s statute of limitations conflicts with Arizona’s for such a debt action, Arizona’s six-year statute applies.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Arizona, a lawsuit for debt must be filed within six years after the cause of action accrues. This time limit applies if the debt is based on a written contract executed within the state. The six-year limit also applies to debt founded on a credit card.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T18:01:11Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 5 of 5 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692g', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.law.cornell.edu/uscode/text/15/1692g', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 15 U.S.C. § 1692g(a) and 12 C.F.R. § 1006.34(a)(1), a notice is compliant only if the collector conveyed the required validation information — the amount of the debt, the creditor's name, the assumption-of-validity statement, the written-dispute/verification statement, and the original-creditor-request statement (plus the fuller Reg F items in § 1006.34(c)) — either in the initial communication (orally or in writing) or in a written notice sent within five days of it; a missing item or late sending defeats compliance. The dispute window runs 30 days from the consumer's receipt (or assumed receipt) of that information, and § 1006.34(b)(5) lets the collector assume receipt on any date at least five business days (excluding weekends and legal public holidays) after it provides the information, so the consumer is still timely if the written dispute is sent before that 30-day period ends. A timely written dispute (or original-creditor request) under § 1692g(b) obliges the collector to cease collection of the disputed portion until verification, a judgment copy, or the original creditor's name and address is mailed; otherwise collection may continue during the 30 days. The excerpt supplies only this standard — applying it to a particular consumer requires the actual notice content and the sending/receipt dates, which the text does not provide."
  - gpt-5.5: grounded=False, error=None, summary='A compliant validation notice must be provided in the initial communication or within five days after it, unless the required information was already in the initial communication or the consumer paid the debt. The notice/validation information must include the debt amount, creditor information, required dispute and verification statements, original-creditor request rights, and the Regulation F validation information; the dispute/validation period runs until 30 days after the consumer receives or is assumed to receive the validation information. The provided text does not state what notice was actually sent, what it contained, when it was provided, or when the consumer received it, so it is insufficient to determine whether a compliant notice was provided or whether the consumer is still within the dispute window.'
  - gemini-2.5-pro: grounded=False, error=None, summary='The provided legal texts outline the specific information a debt collector must include in a validation notice and establish that a consumer has 30 days after receiving this notice to dispute the debt. However, the texts do not contain any factual information about what notice was actually sent or when it was sent in a specific case. Therefore, it is impossible to determine from the text alone whether a compliant notice was provided or if the consumer is still within their dispute window.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T18:01:11Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '1006.34', '12', '15', '1692', '30', '5'], OpenAI=['30'], Gemini=['30'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 15 U.S.C. § 1692g(a) and 12 C.F.R. § 1006.34(a)(1), a notice is compliant only if the collector conveyed the required validation information — the amount of the debt, the creditor's name, the assumption-of-validity statement, the written-dispute/verification statement, and the original-creditor-request statement (plus the fuller Reg F items in § 1006.34(c)) — either in the initial communication (orally or in writing) or in a written notice sent within five days of it; a missing item or late sending defeats compliance. The dispute window runs 30 days from the consumer's receipt (or assumed receipt) of that information, and § 1006.34(b)(5) lets the collector assume receipt on any date at least five business days (excluding weekends and legal public holidays) after it provides the information, so the consumer is still timely if the written dispute is sent before that 30-day period ends. A timely written dispute (or original-creditor request) under § 1692g(b) obliges the collector to cease collection of the disputed portion until verification, a judgment copy, or the original creditor's name and address is mailed; otherwise collection may continue during the 30 days. The excerpt supplies only this standard — applying it to a particular consumer requires the actual notice content and the sending/receipt dates, which the text does not provide."
  - gpt-5.5: grounded=False, error=None, summary='A compliant validation notice must be provided in the initial communication or within five days after it, unless the required information was already in the initial communication or the consumer paid the debt. The notice/validation information must include the debt amount, creditor information, required dispute and verification statements, original-creditor request rights, and the Regulation F validation information; the dispute/validation period runs until 30 days after the consumer receives or is assumed to receive the validation information. The provided text does not state what notice was actually sent, what it contained, when it was provided, or when the consumer received it, so it is insufficient to determine whether a compliant notice was provided or whether the consumer is still within the dispute window.'
  - gemini-2.5-pro: grounded=False, error=None, summary='The provided legal texts outline the specific information a debt collector must include in a validation notice and establish that a consumer has 30 days after receiving this notice to dispute the debt. However, the texts do not contain any factual information about what notice was actually sent or when it was sent in a specific case. Therefore, it is impossible to determine from the text alone whether a compliant notice was provided or if the consumer is still within their dispute window.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T18:00:00Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692f', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692f imposes a general prohibition: a debt collector may not use unfair or unconscionable means to collect or attempt to collect any debt. The statute then lists non-exhaustive examples of violations, including collecting amounts (interest, fees, charges, expenses) not authorized by the debt agreement or permitted by law; accepting checks postdated more than five days without written notice of intent to deposit given 3-10 business days beforehand; soliciting postdated instruments to threaten or institute criminal prosecution; depositing or threatening to deposit a postdated instrument early; causing a person to be charged for communications by concealing the communication's true purpose; and taking or threatening nonjudicial dispossession or disablement of property where there is no present right to possession through an enforceable security interest, no present intention to take possession, or the property is exempt by law. It also bars communicating with a consumer about a debt by post card and using any language or symbol other than the collector's address on mail/telegram envelopes, though a business name may be used if it does not indicate the collection business."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect or attempt to collect a debt. The statute lists violations including collecting unauthorized amounts, improper handling or solicitation of postdated checks, causing communication charges by concealing the communication’s purpose, improper nonjudicial dispossession or disablement of property, communicating by postcard, and using prohibited language or symbols on envelopes.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector is prohibited from using any unfair or unconscionable means to collect a debt. Prohibited actions include collecting amounts not expressly authorized by the agreement or law, and misusing postdated checks by depositing them without proper notice or before their date. It is also a violation to threaten to take property without a present right to it, communicate about a debt via postcard, or use revealing language on an envelope that indicates it is from a debt collector.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T18:00:00Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['10', '1692', '3'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692f imposes a general prohibition: a debt collector may not use unfair or unconscionable means to collect or attempt to collect any debt. The statute then lists non-exhaustive examples of violations, including collecting amounts (interest, fees, charges, expenses) not authorized by the debt agreement or permitted by law; accepting checks postdated more than five days without written notice of intent to deposit given 3-10 business days beforehand; soliciting postdated instruments to threaten or institute criminal prosecution; depositing or threatening to deposit a postdated instrument early; causing a person to be charged for communications by concealing the communication's true purpose; and taking or threatening nonjudicial dispossession or disablement of property where there is no present right to possession through an enforceable security interest, no present intention to take possession, or the property is exempt by law. It also bars communicating with a consumer about a debt by post card and using any language or symbol other than the collector's address on mail/telegram envelopes, though a business name may be used if it does not indicate the collection business."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect or attempt to collect a debt. The statute lists violations including collecting unauthorized amounts, improper handling or solicitation of postdated checks, causing communication charges by concealing the communication’s purpose, improper nonjudicial dispossession or disablement of property, communicating by postcard, and using prohibited language or symbols on envelopes.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector is prohibited from using any unfair or unconscionable means to collect a debt. Prohibited actions include collecting amounts not expressly authorized by the agreement or law, and misusing postdated checks by depositing them without proper notice or before their date. It is also a violation to threaten to take property without a present right to it, communicate about a debt via postcard, or use revealing language on an envelope that indicates it is from a debt collector.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T17:59:15Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692e', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.18', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means in connection with collecting a debt, and then lists non-exhaustive examples: falsely claiming government affiliation/bonding (1); misrepresenting the character, amount, or legal status of a debt or of services rendered or compensation (2); falsely implying attorney status or attorney-sourced communications (3); threatening arrest, imprisonment, seizure, garnishment, attachment, or sale of property or wages when such action is unlawful or not intended (4); threatening any action that cannot legally be or is not intended to be taken (5); communicating credit information known or that should be known to be false, including failing to report a debt as disputed (8); simulating court/official/agency documents (9); using any false representation or deceptive means to collect a debt or obtain consumer information (10); failing to give the required debt-collector disclosures (11); falsely implying accounts were sold to innocent purchasers for value (12); falsely implying documents are (13) or are not (15) legal process; using a name other than the true business name (14); and falsely implying the collector is or works for a consumer reporting agency (16).'
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is prohibited from using any false, deceptive, or misleading representation or means in connection with collecting a debt. The listed violations include falsely implying government affiliation, misrepresenting the debt or attorney involvement, threatening unlawful or unintended actions, communicating false credit information, using fake court or agency documents, using a name other than the true name, and omitting required debt-collector disclosures. The regulation further specifies that the initial communication must state that the debt collector is attempting to collect a debt and that information obtained will be used for that purpose, later communications must state they are from a debt collector, and these disclosures are not required in a formal pleading in a legal action.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector may not use any false, deceptive, or misleading representations. Prohibited conduct includes misrepresenting the character, amount, or legal status of a debt; falsely implying an affiliation with the government or that an individual is an attorney; and threatening to take any action that cannot legally be taken or is not intended to be taken. A debt collector must also disclose in an initial communication that they are attempting to collect a debt and, in subsequent communications, must disclose that the communication is from a debt collector, unless it is a formal legal pleading.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T17:59:15Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '10', '11', '12', '13', '14', '15', '16', '1692', '2', '3', '4', '5', '8', '9'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means in connection with collecting a debt, and then lists non-exhaustive examples: falsely claiming government affiliation/bonding (1); misrepresenting the character, amount, or legal status of a debt or of services rendered or compensation (2); falsely implying attorney status or attorney-sourced communications (3); threatening arrest, imprisonment, seizure, garnishment, attachment, or sale of property or wages when such action is unlawful or not intended (4); threatening any action that cannot legally be or is not intended to be taken (5); communicating credit information known or that should be known to be false, including failing to report a debt as disputed (8); simulating court/official/agency documents (9); using any false representation or deceptive means to collect a debt or obtain consumer information (10); failing to give the required debt-collector disclosures (11); falsely implying accounts were sold to innocent purchasers for value (12); falsely implying documents are (13) or are not (15) legal process; using a name other than the true business name (14); and falsely implying the collector is or works for a consumer reporting agency (16).'
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is prohibited from using any false, deceptive, or misleading representation or means in connection with collecting a debt. The listed violations include falsely implying government affiliation, misrepresenting the debt or attorney involvement, threatening unlawful or unintended actions, communicating false credit information, using fake court or agency documents, using a name other than the true name, and omitting required debt-collector disclosures. The regulation further specifies that the initial communication must state that the debt collector is attempting to collect a debt and that information obtained will be used for that purpose, later communications must state they are from a debt collector, and these disclosures are not required in a formal pleading in a legal action.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector may not use any false, deceptive, or misleading representations. Prohibited conduct includes misrepresenting the character, amount, or legal status of a debt; falsely implying an affiliation with the government or that an individual is an attorney; and threatening to take any action that cannot legally be taken or is not intended to be taken. A debt collector must also disclose in an initial communication that they are attempting to collect a debt and, in subsequent communications, must disclose that the communication is from a debt collector, unless it is a formal legal pleading.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T17:57:44Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the harassment-by-repeated-calls prohibition (and FDCPA § 806(5)) if it calls a particular person about a particular debt neither more than seven times in seven consecutive days, nor at all within seven consecutive days after having had a telephone conversation with that person about that debt. Conversely, under (b)(2)(ii), exceeding either of those limits creates a presumption that the collector violated the rule. Section 1006.14(b)(4) clarifies that the limits apply per 'particular debt' — i.e., each of the consumer's debts in collection counted separately — except that student loan debts serviced under a single account number when obtained by the collector are treated as one particular debt."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is presumed to comply if, for a particular debt, it does not call a particular person more than seven times within seven consecutive days and does not call within seven consecutive days after having a telephone conversation with that person about that debt. A debt collector is presumed to violate the rule if it places calls in excess of either of those frequencies. “Particular debt” means each debt in collection, except that student loan debts serviced under a single account number when obtained by the collector are treated together as one particular debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to have violated the law if they place a telephone call to a person more than seven times within seven consecutive days in connection with a particular debt. It is also a presumed violation to call a person within seven days after having had a telephone conversation with them about that debt. These call frequency limits apply on a per-debt basis, although all of a consumer's student loans serviced under a single account number are considered a single debt for this purpose."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T17:57:44Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1006.14', '12', '2', '4', '5', '806'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the harassment-by-repeated-calls prohibition (and FDCPA § 806(5)) if it calls a particular person about a particular debt neither more than seven times in seven consecutive days, nor at all within seven consecutive days after having had a telephone conversation with that person about that debt. Conversely, under (b)(2)(ii), exceeding either of those limits creates a presumption that the collector violated the rule. Section 1006.14(b)(4) clarifies that the limits apply per 'particular debt' — i.e., each of the consumer's debts in collection counted separately — except that student loan debts serviced under a single account number when obtained by the collector are treated as one particular debt."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is presumed to comply if, for a particular debt, it does not call a particular person more than seven times within seven consecutive days and does not call within seven consecutive days after having a telephone conversation with that person about that debt. A debt collector is presumed to violate the rule if it places calls in excess of either of those frequencies. “Particular debt” means each debt in collection, except that student loan debts serviced under a single account number when obtained by the collector are treated together as one particular debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to have violated the law if they place a telephone call to a person more than seven times within seven consecutive days in connection with a particular debt. It is also a presumed violation to call a person within seven days after having had a telephone conversation with them about that debt. These call frequency limits apply on a per-debt basis, although all of a consumer's student loans serviced under a single account number are considered a single debt for this purpose."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b] CITATION-CHECK-FAILED -- run run_20260826T175559Z, 2026-08-26T17:56:47Z

**File:** `rules/debt/federal/fcra_furnisher_dispute_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1681s-2', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.law.cornell.edu/uscode/text/15/1681s-2', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Once a furnisher receives notice from a credit reporting agency under § 1681i(a)(2) that a consumer disputes the completeness or accuracy of information it supplied, it must investigate the disputed information, review all relevant information the agency provided with the notice, and report the investigation's results back to that agency. If the investigation shows the information is incomplete or inaccurate, the furnisher must also report that to all other nationwide consumer reporting agencies it furnished the information to, and if the item is found inaccurate, incomplete, or unverifiable, it must promptly modify, delete, or permanently block reporting of that item. All of these investigations, reviews, and reports must be completed within the same time period § 1681i(a)(1) gives the consumer reporting agency to complete its own reinvestigation."
  - gpt-5.5: grounded=True, error=None, summary='After receiving notice from a consumer reporting agency of a dispute about the completeness or accuracy of information it furnished, the furnisher must investigate the disputed information, review relevant information from the agency, and report the investigation results back to the agency. If the information is incomplete, inaccurate, or cannot be verified, the furnisher must take appropriate action such as modifying, deleting, or permanently blocking reporting of the item, and must report certain results to other nationwide consumer reporting agencies to which it furnished the information. These investigations, reviews, and reports must be completed within the time period applicable to the consumer reporting agency’s required actions under section 1681i(a)(1).'
  - gemini-2.5-pro: grounded=True, error=None, summary='After receiving notice of a dispute from a consumer reporting agency, a furnisher of information must conduct an investigation, review all relevant information provided by the agency, and report the results back to that agency. If the investigation finds the information is inaccurate or incomplete, the furnisher must also report those results to all other nationwide consumer reporting agencies it uses. Finally, if information is found to be inaccurate, incomplete, or unverifiable, the furnisher must promptly modify, delete, or permanently block the reporting of that item.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b] MODEL-DISAGREEMENT -- run run_20260826T175559Z, 2026-08-26T17:56:47Z

**File:** `rules/debt/federal/fcra_furnisher_dispute_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '1681', '2'], OpenAI=['1', '1681'], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Once a furnisher receives notice from a credit reporting agency under § 1681i(a)(2) that a consumer disputes the completeness or accuracy of information it supplied, it must investigate the disputed information, review all relevant information the agency provided with the notice, and report the investigation's results back to that agency. If the investigation shows the information is incomplete or inaccurate, the furnisher must also report that to all other nationwide consumer reporting agencies it furnished the information to, and if the item is found inaccurate, incomplete, or unverifiable, it must promptly modify, delete, or permanently block reporting of that item. All of these investigations, reviews, and reports must be completed within the same time period § 1681i(a)(1) gives the consumer reporting agency to complete its own reinvestigation."
  - gpt-5.5: grounded=True, error=None, summary='After receiving notice from a consumer reporting agency of a dispute about the completeness or accuracy of information it furnished, the furnisher must investigate the disputed information, review relevant information from the agency, and report the investigation results back to the agency. If the information is incomplete, inaccurate, or cannot be verified, the furnisher must take appropriate action such as modifying, deleting, or permanently blocking reporting of the item, and must report certain results to other nationwide consumer reporting agencies to which it furnished the information. These investigations, reviews, and reports must be completed within the time period applicable to the consumer reporting agency’s required actions under section 1681i(a)(1).'
  - gemini-2.5-pro: grounded=True, error=None, summary='After receiving notice of a dispute from a consumer reporting agency, a furnisher of information must conduct an investigation, review all relevant information provided by the agency, and report the results back to that agency. If the investigation finds the information is inaccurate or incomplete, the furnisher must also report those results to all other nationwide consumer reporting agencies it uses. Finally, if information is found to be inaccurate, incomplete, or unverifiable, the furnisher must promptly modify, delete, or permanently block the reporting of that item.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-ORAL-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T174558Z, 2026-08-26T17:51:57Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-12-courts-and-civil-proceedings/az-rev-st-sect-12-543/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under A.R.S. § 12-543, a lawsuit on a debt that is not evidenced by a written contract (an oral debt) or on a stated or open account must be filed within three years after the cause of action accrues, and not afterward. For stated or open accounts, the statute adds that no item of the account is barred so long as any item on that account was incurred within the three years immediately before the action is brought. An exception exists for mutual and current accounts concerning the trade of merchandise between merchants or their factors/agents, which are excluded from this open-account provision.'
  - gpt-5.5: grounded=True, error=None, summary='An action for debt not evidenced by a written contract must be commenced and prosecuted within three years after the cause of action accrues. An action on a stated or open account must also be brought within three years, and no item of the account is barred so long as any item was incurred within the three years immediately before the action is brought.'
  - gemini-2.5-pro: grounded=True, error=None, summary='According to the provided text, a lawsuit must be commenced and prosecuted within three years after the cause of action accrues. This three-year time limit applies to actions for debt where the indebtedness is not based on a contract in writing. The statute also applies this three-year limit to lawsuits based upon stated or open accounts.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-ORAL-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T174558Z, 2026-08-26T17:51:57Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['12', '543'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary='Under A.R.S. § 12-543, a lawsuit on a debt that is not evidenced by a written contract (an oral debt) or on a stated or open account must be filed within three years after the cause of action accrues, and not afterward. For stated or open accounts, the statute adds that no item of the account is barred so long as any item on that account was incurred within the three years immediately before the action is brought. An exception exists for mutual and current accounts concerning the trade of merchandise between merchants or their factors/agents, which are excluded from this open-account provision.'
  - gpt-5.5: grounded=True, error=None, summary='An action for debt not evidenced by a written contract must be commenced and prosecuted within three years after the cause of action accrues. An action on a stated or open account must also be brought within three years, and no item of the account is barred so long as any item was incurred within the three years immediately before the action is brought.'
  - gemini-2.5-pro: grounded=True, error=None, summary='According to the provided text, a lawsuit must be commenced and prosecuted within three years after the cause of action accrues. This three-year time limit applies to actions for debt where the indebtedness is not based on a contract in writing. The statute also applies this three-year limit to lawsuits based upon stated or open accounts.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-WRITTEN-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T174558Z, 2026-08-26T17:51:13Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-12-courts-and-civil-proceedings/az-rev-st-sect-12-548/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/az/title-12-courts-and-civil-proceedings/az-rev-st-sect-12-548/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under A.R.S. § 12-548(A), a debt action must be filed within six years after the cause of action accrues if the indebtedness is evidenced by or founded on either a written contract executed in Arizona or a credit card as defined in § 13-2101(3)(a). After that six-year period, the action may not be brought. Subsection (B) adds that if another jurisdiction's limitations period for such a debt action conflicts with Arizona's, this Arizona six-year provision controls."
  - gpt-5.5: grounded=True, error=None, summary='An Arizona action for debt must be commenced and prosecuted within six years after the cause of action accrues if the debt is based on a written contract executed in Arizona or on a credit card as defined by the cited statute. If another jurisdiction has a conflicting limitations period for such a debt action, Arizona’s six-year rule applies.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Arizona, a lawsuit for debt must be commenced within six years after the cause of action accrues. This six-year statute of limitations applies if the debt is based on a written contract executed within the state. The six-year limit also applies to debts founded on a credit card.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-WRITTEN-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T174558Z, 2026-08-26T17:51:13Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['12', '13', '2101', '3', '548'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under A.R.S. § 12-548(A), a debt action must be filed within six years after the cause of action accrues if the indebtedness is evidenced by or founded on either a written contract executed in Arizona or a credit card as defined in § 13-2101(3)(a). After that six-year period, the action may not be brought. Subsection (B) adds that if another jurisdiction's limitations period for such a debt action conflicts with Arizona's, this Arizona six-year provision controls."
  - gpt-5.5: grounded=True, error=None, summary='An Arizona action for debt must be commenced and prosecuted within six years after the cause of action accrues if the debt is based on a written contract executed in Arizona or on a credit card as defined by the cited statute. If another jurisdiction has a conflicting limitations period for such a debt action, Arizona’s six-year rule applies.'
  - gemini-2.5-pro: grounded=True, error=None, summary='In Arizona, a lawsuit for debt must be commenced within six years after the cause of action accrues. This six-year statute of limitations applies if the debt is based on a written contract executed within the state. The six-year limit also applies to debts founded on a credit card.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] CITATION-CHECK-FAILED -- run run_20260826T174558Z, 2026-08-26T17:50:32Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 5 of 5 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692g', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.law.cornell.edu/uscode/text/15/1692g', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 15 U.S.C. § 1692g(a) and 12 C.F.R. § 1006.34(a)(1), a notice is compliant only if the collector conveyed the validation information in the initial communication (in writing, or orally under the regulation) or sent a written validation notice within five days of that initial communication, and the notice contained the required content: the debt amount, the creditor's name, the 30-day assumption-of-validity statement, the written-dispute/verification statement, and the original-creditor-request statement (§ 1692g(a)(1)-(5)), plus Reg F's items in § 1006.34(c) (collector communication disclosure, itemization and current amount, dispute-window end date, original-creditor right, CFPB website statement, and response prompts/addresses). The dispute window runs from the date the validation information was provided and ends 30 days after the consumer receives or is assumed to receive it; the collector may assume receipt on any date at least five days (excluding Saturdays, Sundays, and legal public holidays) after it provides the information (12 C.F.R. § 1006.34(b)(5)). If a written dispute or original-creditor request is made within that 30-day period, § 1692g(b) requires the collector to cease collection of the disputed portion until verification, a judgment copy, or the original creditor's name and address is mailed; other collection may continue during the 30 days absent a written dispute. The excerpt supplies only this framework — applying it to a particular consumer requires the specific dates and notice contents, which are not in the text."
  - gpt-5.5: grounded=False, error=None, summary='The text states that a debt collector must provide validation information in the initial communication or within five days after it, and the notice must include debt details, creditor information, dispute rights, verification/original-creditor rights, and related consumer-response information. The dispute/validation period runs for 30 days after the consumer receives or is assumed to receive the validation information, with assumed receipt permitted at least five business days after it is provided. However, the provided text does not include facts about what notice was sent, when it was provided, or when the consumer received it, so it is not possible to determine whether a compliant notice was actually provided or whether the consumer is still within the dispute window.'
  - gemini-2.5-pro: grounded=False, error=None, summary='The provided texts describe the required contents of a debt validation notice and the rules for calculating the 30-day dispute window. However, the texts do not contain any facts about a specific notice that was sent or received. Without knowing the contents of a notice and the date it was provided to the consumer, it is impossible to determine if it was compliant or if the dispute window is still open.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] MODEL-DISAGREEMENT -- run run_20260826T174558Z, 2026-08-26T17:50:32Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '1006.34', '12', '15', '1692', '30', '5'], OpenAI=['30'], Gemini=['30'].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 15 U.S.C. § 1692g(a) and 12 C.F.R. § 1006.34(a)(1), a notice is compliant only if the collector conveyed the validation information in the initial communication (in writing, or orally under the regulation) or sent a written validation notice within five days of that initial communication, and the notice contained the required content: the debt amount, the creditor's name, the 30-day assumption-of-validity statement, the written-dispute/verification statement, and the original-creditor-request statement (§ 1692g(a)(1)-(5)), plus Reg F's items in § 1006.34(c) (collector communication disclosure, itemization and current amount, dispute-window end date, original-creditor right, CFPB website statement, and response prompts/addresses). The dispute window runs from the date the validation information was provided and ends 30 days after the consumer receives or is assumed to receive it; the collector may assume receipt on any date at least five days (excluding Saturdays, Sundays, and legal public holidays) after it provides the information (12 C.F.R. § 1006.34(b)(5)). If a written dispute or original-creditor request is made within that 30-day period, § 1692g(b) requires the collector to cease collection of the disputed portion until verification, a judgment copy, or the original creditor's name and address is mailed; other collection may continue during the 30 days absent a written dispute. The excerpt supplies only this framework — applying it to a particular consumer requires the specific dates and notice contents, which are not in the text."
  - gpt-5.5: grounded=False, error=None, summary='The text states that a debt collector must provide validation information in the initial communication or within five days after it, and the notice must include debt details, creditor information, dispute rights, verification/original-creditor rights, and related consumer-response information. The dispute/validation period runs for 30 days after the consumer receives or is assumed to receive the validation information, with assumed receipt permitted at least five business days after it is provided. However, the provided text does not include facts about what notice was sent, when it was provided, or when the consumer received it, so it is not possible to determine whether a compliant notice was actually provided or whether the consumer is still within the dispute window.'
  - gemini-2.5-pro: grounded=False, error=None, summary='The provided texts describe the required contents of a debt validation notice and the rules for calculating the 30-day dispute window. However, the texts do not contain any facts about a specific notice that was sent or received. Without knowing the contents of a notice and the date it was provided to the consumer, it is impossible to determine if it was compliant or if the dispute window is still open.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] CITATION-CHECK-FAILED -- run run_20260826T174558Z, 2026-08-26T17:49:32Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692f', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692f imposes a general ban on a debt collector using any unfair or unconscionable means to collect or attempt to collect a debt, then lists specific non-exhaustive examples of violations. These include: collecting amounts (interest, fees, charges, expenses) not expressly authorized by the debt agreement or permitted by law; accepting a check postdated more than five days without written notice of intent to deposit sent 3-10 business days beforehand; soliciting postdated instruments to threaten or institute criminal prosecution; depositing or threatening to deposit a postdated instrument early; causing a person to incur communication charges by concealing the communication's true purpose; taking or threatening nonjudicial dispossession or disablement of property where there is no present enforceable right or intent to take possession, or the property is exempt; communicating with a consumer about a debt by post card; and using any language or symbol other than the collector's address on mail envelopes or telegrams (a business name may be used only if it does not indicate the debt collection business). Because the list is expressly stated 'without limiting the general application of the foregoing,' conduct beyond these eight items can still violate the section."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect or attempt to collect a debt. The statute lists violations including collecting unauthorized amounts, certain improper handling or solicitation of postdated payment instruments, causing communication charges by concealing the communication’s true purpose, improper nonjudicial repossession or disablement actions, communicating about a debt by postcard, and using prohibited language or symbols on mailed envelopes or telegrams.'
  - gemini-2.5-pro: grounded=True, error=None, summary='Unfair or unconscionable debt collection practices include collecting any amount, such as interest or fees, not expressly authorized by the agreement or law. The statute also prohibits various misuses of postdated checks, such as depositing them early or soliciting them to threaten criminal prosecution. Additionally, debt collectors cannot threaten to take property if they have no right or intent to do so, communicate about a debt via postcard, or use revealing language on an envelope.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] MODEL-DISAGREEMENT -- run run_20260826T174558Z, 2026-08-26T17:49:32Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['10', '1692', '3'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692f imposes a general ban on a debt collector using any unfair or unconscionable means to collect or attempt to collect a debt, then lists specific non-exhaustive examples of violations. These include: collecting amounts (interest, fees, charges, expenses) not expressly authorized by the debt agreement or permitted by law; accepting a check postdated more than five days without written notice of intent to deposit sent 3-10 business days beforehand; soliciting postdated instruments to threaten or institute criminal prosecution; depositing or threatening to deposit a postdated instrument early; causing a person to incur communication charges by concealing the communication's true purpose; taking or threatening nonjudicial dispossession or disablement of property where there is no present enforceable right or intent to take possession, or the property is exempt; communicating with a consumer about a debt by post card; and using any language or symbol other than the collector's address on mail envelopes or telegrams (a business name may be used only if it does not indicate the debt collection business). Because the list is expressly stated 'without limiting the general application of the foregoing,' conduct beyond these eight items can still violate the section."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use unfair or unconscionable means to collect or attempt to collect a debt. The statute lists violations including collecting unauthorized amounts, certain improper handling or solicitation of postdated payment instruments, causing communication charges by concealing the communication’s true purpose, improper nonjudicial repossession or disablement actions, communicating about a debt by postcard, and using prohibited language or symbols on mailed envelopes or telegrams.'
  - gemini-2.5-pro: grounded=True, error=None, summary='Unfair or unconscionable debt collection practices include collecting any amount, such as interest or fees, not expressly authorized by the agreement or law. The statute also prohibits various misuses of postdated checks, such as depositing them early or soliciting them to threaten criminal prosecution. Additionally, debt collectors cannot threaten to take property if they have no right or intent to do so, communicate about a debt via postcard, or use revealing language on an envelope.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] CITATION-CHECK-FAILED -- run run_20260826T174558Z, 2026-08-26T17:48:46Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692e', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.18', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means in connection with collecting a debt, and then lists specific violations without limiting that general rule. These include falsely implying government affiliation or that the collector is a consumer reporting agency; misrepresenting the character, amount, or legal status of a debt or the services/compensation involved; falsely implying a person is an attorney or a communication is from one; threatening arrest, imprisonment, seizure, garnishment, attachment, or sale unless lawful and actually intended; threatening any action that cannot legally be taken or is not intended; communicating known-false credit information (including failing to note a debt is disputed); simulating court or agency documents; falsely claiming documents are or are not legal process; claiming accounts went to innocent purchasers for value; using a name other than the collector's true name; and using any false representation or deceptive means to collect a debt or obtain consumer information. Paragraph (11) requires the 'mini-Miranda' disclosure, whose current operative form is 12 C.F.R. § 1006.18(e): the initial communication must state the collector is attempting to collect a debt and that information obtained will be used for that purpose (repeated in the initial written communication if the first contact was oral), each subsequent communication must disclose that it is from a debt collector, and neither disclosure is required in a formal pleading made in connection with a legal action."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use false, deceptive, or misleading representations or means in connection with collecting a debt. The statute lists prohibited conduct including misrepresenting government affiliation, the character/amount/legal status of a debt, attorney involvement, legal consequences of nonpayment, threats of unlawful or unintended action, false credit reporting, fake court/agency documents, false or deceptive collection means, use of a name other than the true name, and false implications about legal process or consumer reporting agency status. The regulation also requires debt collectors to make the initial and subsequent debt-collector disclosures, with an exception for formal pleadings in legal actions.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector is broadly prohibited from using any false, deceptive, or misleading representation when collecting a debt. This includes falsely representing the character, amount, or legal status of a debt, or falsely implying an affiliation with the government or that an individual is an attorney. It is also a violation to threaten any action that cannot legally be taken or is not intended to be taken, or to fail to disclose in communications that the communication is from a debt collector attempting to collect a debt.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] MODEL-DISAGREEMENT -- run run_20260826T174558Z, 2026-08-26T17:48:46Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1006.18', '11', '12', '1692'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Section 1692e broadly bars a debt collector from using any false, deceptive, or misleading representation or means in connection with collecting a debt, and then lists specific violations without limiting that general rule. These include falsely implying government affiliation or that the collector is a consumer reporting agency; misrepresenting the character, amount, or legal status of a debt or the services/compensation involved; falsely implying a person is an attorney or a communication is from one; threatening arrest, imprisonment, seizure, garnishment, attachment, or sale unless lawful and actually intended; threatening any action that cannot legally be taken or is not intended; communicating known-false credit information (including failing to note a debt is disputed); simulating court or agency documents; falsely claiming documents are or are not legal process; claiming accounts went to innocent purchasers for value; using a name other than the collector's true name; and using any false representation or deceptive means to collect a debt or obtain consumer information. Paragraph (11) requires the 'mini-Miranda' disclosure, whose current operative form is 12 C.F.R. § 1006.18(e): the initial communication must state the collector is attempting to collect a debt and that information obtained will be used for that purpose (repeated in the initial written communication if the first contact was oral), each subsequent communication must disclose that it is from a debt collector, and neither disclosure is required in a formal pleading made in connection with a legal action."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector may not use false, deceptive, or misleading representations or means in connection with collecting a debt. The statute lists prohibited conduct including misrepresenting government affiliation, the character/amount/legal status of a debt, attorney involvement, legal consequences of nonpayment, threats of unlawful or unintended action, false credit reporting, fake court/agency documents, false or deceptive collection means, use of a name other than the true name, and false implications about legal process or consumer reporting agency status. The regulation also requires debt collectors to make the initial and subsequent debt-collector disclosures, with an exception for formal pleadings in legal actions.'
  - gemini-2.5-pro: grounded=True, error=None, summary='A debt collector is broadly prohibited from using any false, deceptive, or misleading representation when collecting a debt. This includes falsely representing the character, amount, or legal status of a debt, or falsely implying an affiliation with the government or that an individual is an attorney. It is also a violation to threaten any action that cannot legally be taken or is not intended to be taken, or to fail to disclose in communications that the communication is from a debt collector attempting to collect a debt.'

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] CITATION-CHECK-FAILED -- run run_20260826T174558Z, 2026-08-26T17:47:52Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the prohibition on repeated/continuous calls (and FDCPA § 806(5)) if, as to a particular person and a particular debt, it places no more than seven calls within seven consecutive days and does not call within seven consecutive days after having had a telephone conversation with that person about that debt. Conversely, under (b)(2)(ii), exceeding either of those frequencies creates a presumption that the collector violated the rule and FDCPA § 806(5). The limits are applied per 'particular debt,' which § 1006.14(b)(4) defines as each of a consumer's debts in collection, except that all student loan debts serviced under a single account number when obtained by the collector count as one particular debt."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is presumed to comply if, for a particular person and a particular debt, it does not place more than seven calls within seven consecutive days and does not call within seven consecutive days after having a telephone conversation with that person about that debt. A debt collector is presumed to violate the rule if it exceeds either of those call-frequency limits. For these purposes, a “particular debt” generally means each debt in collection, except that certain student loan debts serviced under one account number are treated together as one particular debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to have violated the law if they call a person about a particular debt more than seven times within seven consecutive days. It is also a presumed violation for a debt collector to place a call within seven consecutive days after having had a telephone conversation with that person about the debt. These frequency limits apply to each of a consumer's individual debts, although multiple student loans serviced under a single account number are treated as one debt."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] MODEL-DISAGREEMENT -- run run_20260826T174558Z, 2026-08-26T17:47:52Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1006.14', '12', '2', '4', '5', '806'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 12 C.F.R. § 1006.14(b)(2)(i), a debt collector is presumed to comply with the prohibition on repeated/continuous calls (and FDCPA § 806(5)) if, as to a particular person and a particular debt, it places no more than seven calls within seven consecutive days and does not call within seven consecutive days after having had a telephone conversation with that person about that debt. Conversely, under (b)(2)(ii), exceeding either of those frequencies creates a presumption that the collector violated the rule and FDCPA § 806(5). The limits are applied per 'particular debt,' which § 1006.14(b)(4) defines as each of a consumer's debts in collection, except that all student loan debts serviced under a single account number when obtained by the collector count as one particular debt."
  - gpt-5.5: grounded=True, error=None, summary='A debt collector is presumed to comply if, for a particular person and a particular debt, it does not place more than seven calls within seven consecutive days and does not call within seven consecutive days after having a telephone conversation with that person about that debt. A debt collector is presumed to violate the rule if it exceeds either of those call-frequency limits. For these purposes, a “particular debt” generally means each debt in collection, except that certain student loan debts serviced under one account number are treated together as one particular debt.'
  - gemini-2.5-pro: grounded=True, error=None, summary="A debt collector is presumed to have violated the law if they call a person about a particular debt more than seven times within seven consecutive days. It is also a presumed violation for a debt collector to place a call within seven consecutive days after having had a telephone conversation with that person about the debt. These frequency limits apply to each of a consumer's individual debts, although multiple student loans serviced under a single account number are treated as one debt."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b] CITATION-CHECK-FAILED -- run run_20260826T174558Z, 2026-08-26T17:47:02Z

**File:** `rules/debt/federal/fcra_furnisher_dispute_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1681s-2', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.law.cornell.edu/uscode/text/15/1681s-2', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 15 U.S.C. § 1681s-2(b)(1), a furnisher's duties are triggered only once it receives notice of the dispute from the consumer reporting agency under § 1681i(a)(2) (not from the consumer directly). Upon that notice, the furnisher must investigate the disputed information, review all relevant information the CRA supplied, and report the investigation's results back to the CRA; if the information is found incomplete or inaccurate, it must also report those results to all other nationwide CRAs to which it furnished the information. If the disputed item is found inaccurate or incomplete, or cannot be verified, the furnisher must promptly modify, delete, or permanently block reporting of that item. Under § 1681s-2(b)(2), all of these investigations, reviews, and reports must be completed within the same time period the CRA has to complete its reinvestigation under § 1681i(a)(1)."
  - gpt-5.5: grounded=True, error=None, summary='After receiving notice from a consumer reporting agency of a dispute about the completeness or accuracy of information the person furnished, the furnisher must investigate the disputed information, review all relevant information provided by the agency, and report the investigation results back to the agency. If the information is found incomplete, inaccurate, or cannot be verified, the furnisher must, as appropriate, promptly modify, delete, or permanently block reporting of the item, and must report certain incomplete or inaccurate results to other nationwide consumer reporting agencies to which it furnished the information. The furnisher must complete the required investigations, reviews, and reports before the deadline by which the consumer reporting agency must complete its related actions.'
  - gemini-2.5-pro: grounded=True, error=None, summary="After receiving notice of a dispute from a consumer reporting agency, the furnisher of the information must conduct an investigation and report the results back to that agency. If the investigation finds the information is incomplete or inaccurate, the furnisher must also report those results to all other nationwide consumer reporting agencies. The furnisher must then promptly modify, delete, or permanently block the reporting of any information found to be inaccurate, incomplete, or unverifiable. These actions must all be completed before the credit bureau's own deadline to complete its investigation expires."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b] MODEL-DISAGREEMENT -- run run_20260826T174558Z, 2026-08-26T17:47:02Z

**File:** `rules/debt/federal/fcra_furnisher_dispute_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=['1', '15', '1681', '2'], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=True, error=None, summary="Under 15 U.S.C. § 1681s-2(b)(1), a furnisher's duties are triggered only once it receives notice of the dispute from the consumer reporting agency under § 1681i(a)(2) (not from the consumer directly). Upon that notice, the furnisher must investigate the disputed information, review all relevant information the CRA supplied, and report the investigation's results back to the CRA; if the information is found incomplete or inaccurate, it must also report those results to all other nationwide CRAs to which it furnished the information. If the disputed item is found inaccurate or incomplete, or cannot be verified, the furnisher must promptly modify, delete, or permanently block reporting of that item. Under § 1681s-2(b)(2), all of these investigations, reviews, and reports must be completed within the same time period the CRA has to complete its reinvestigation under § 1681i(a)(1)."
  - gpt-5.5: grounded=True, error=None, summary='After receiving notice from a consumer reporting agency of a dispute about the completeness or accuracy of information the person furnished, the furnisher must investigate the disputed information, review all relevant information provided by the agency, and report the investigation results back to the agency. If the information is found incomplete, inaccurate, or cannot be verified, the furnisher must, as appropriate, promptly modify, delete, or permanently block reporting of the item, and must report certain incomplete or inaccurate results to other nationwide consumer reporting agencies to which it furnished the information. The furnisher must complete the required investigations, reviews, and reports before the deadline by which the consumer reporting agency must complete its related actions.'
  - gemini-2.5-pro: grounded=True, error=None, summary="After receiving notice of a dispute from a consumer reporting agency, the furnisher of the information must conduct an investigation and report the results back to that agency. If the investigation finds the information is incomplete or inaccurate, the furnisher must also report those results to all other nationwide consumer reporting agencies. The furnisher must then promptly modify, delete, or permanently block the reporting of any information found to be inaccurate, incomplete, or unverifiable. These actions must all be completed before the credit bureau's own deadline to complete its investigation expires."

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


