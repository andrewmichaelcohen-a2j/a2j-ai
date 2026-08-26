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


### [UT-CIVIL-ANSWER-DEADLINE] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:21:21Z

**File:** `rules/debt/state/utah/ut_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRkAYFwfkDxSnsxp2HQA'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [UT-PERSONAL-PROPERTY-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:21:15Z

**File:** `rules/debt/state/utah/ut_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ut/title-78b-judicial-code/ut-code-sect-78b-5-506/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/ut/title-78b-judicial-code/ut-code-sect-78b-5-506/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRkATC6MEZmifUgMq2fX'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [UT-PERSONAL-PROPERTY-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:21:15Z

**File:** `rules/debt/state/utah/ut_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRkATC6MEZmifUgMq2fX'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [UT-HOMESTEAD-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:21:14Z

**File:** `rules/debt/state/utah/ut_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ut/title-78b-judicial-code/ut-code-sect-78b-5-503/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/ut/title-78b-judicial-code/ut-code-sect-78b-5-503/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRkANAUQHibcqVG7JjRt'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [UT-HOMESTEAD-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:21:14Z

**File:** `rules/debt/state/utah/ut_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRkANAUQHibcqVG7JjRt'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [UT-WAGE-GARNISHMENT-LIMIT] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:21:13Z

**File:** `rules/debt/state/utah/ut_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ut/title-70c-utah-consumer-credit-code/ut-code-sect-70c-7-103/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/ut/title-70c-utah-consumer-credit-code/ut-code-sect-70c-7-103/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRkAHF4M7TP6Wfz9SoSt'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [UT-WAGE-GARNISHMENT-LIMIT] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:21:13Z

**File:** `rules/debt/state/utah/ut_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRkAHF4M7TP6Wfz9SoSt'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [UT-SOL-ORAL-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:21:12Z

**File:** `rules/debt/state/utah/ut_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ut/title-78b-judicial-code/ut-code-sect-78b-2-307/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRkACSLFrhyxp38MhAJU'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [UT-SOL-ORAL-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:21:12Z

**File:** `rules/debt/state/utah/ut_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRkACSLFrhyxp38MhAJU'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [UT-SOL-WRITTEN-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:21:11Z

**File:** `rules/debt/state/utah/ut_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ut/title-78b-judicial-code/ut-code-sect-78b-2-309/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/ut/title-78b-judicial-code/ut-code-sect-78b-2-309/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRkA7Vg6R3Pcj9zFxgXN'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [UT-SOL-WRITTEN-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:21:11Z

**File:** `rules/debt/state/utah/ut_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRkA7Vg6R3Pcj9zFxgXN'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-JUSTICE-COURT-DEBT-ANSWER-DEADLINE] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:21:09Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://texaslawhelp.org/guide/how-to-answer-a-debt-collection-case-in-justice-court', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk9nA5toKpZ1mq3TbFC'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-JUSTICE-COURT-DEBT-ANSWER-DEADLINE] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:21:09Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk9nA5toKpZ1mq3TbFC'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-EXEMPT-PERSONAL-PROPERTY] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:21:05Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 3 of 3 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/tx/property-code/prop-sect-42-001/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/tx/property-code/prop-sect-42-001/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/tx/property-code/prop-sect-42-002/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk9ggRZ7FB19s2QRUXi'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-EXEMPT-PERSONAL-PROPERTY] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:21:05Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk9ggRZ7FB19s2QRUXi'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-HOMESTEAD-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:21:04Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://statutes.capitol.texas.gov/Docs/PR/htm/PR.41.htm', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://statutes.capitol.texas.gov/Docs/PR/htm/PR.41.htm', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk9Ke9PfamVkQie2hwL'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-HOMESTEAD-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:21:04Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk9Ke9PfamVkQie2hwL'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-WAGE-GARNISHMENT-PROHIBITION] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:59Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/constitution/texas/sections/cn001600-002800.html', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk9FRPdtWP9EWmtmL7x'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-WAGE-GARNISHMENT-PROHIBITION] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:59Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk9FRPdtWP9EWmtmL7x'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-SOL-CONSUMER-DEBT] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:58Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/codes/texas/civil-practice-and-remedies-code/title-2/subtitle-b/chapter-16/subchapter-a/section-16-004/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk99GJqgERwbb8xzdWU'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-SOL-CONSUMER-DEBT] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:58Z

**File:** `rules/debt/state/texas/tx_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk99GJqgERwbb8xzdWU'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:56Z

**File:** `rules/debt/state/texas/tx_debt_band3_discretionary_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk8GU7rEAg85fSzxYkS'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [NY-CIVIL-ANSWER-DEADLINE] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:44Z

**File:** `rules/debt/state/new_york/ny_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ny/civil-practice-law-and-rules/cvpny-cplr-rule-320/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk8CL5VYquCCyEyuthQ'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [NY-CIVIL-ANSWER-DEADLINE] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:44Z

**File:** `rules/debt/state/new_york/ny_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk8CL5VYquCCyEyuthQ'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [NY-PERSONAL-PROPERTY-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:43Z

**File:** `rules/debt/state/new_york/ny_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/codes/new-york/cvp/article-52/5205/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.dfs.ny.gov/industry_guidance/exemption_from_judgments', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk87KSyg98yQybDyaXH'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [NY-PERSONAL-PROPERTY-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:43Z

**File:** `rules/debt/state/new_york/ny_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk87KSyg98yQybDyaXH'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [NY-VEHICLE-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:42Z

**File:** `rules/debt/state/new_york/ny_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/codes/new-york/cvp/article-52/5205/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.dfs.ny.gov/industry_guidance/exemption_from_judgments', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk82MZ2fbh2HAqQ9bo5'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [NY-VEHICLE-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:42Z

**File:** `rules/debt/state/new_york/ny_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk82MZ2fbh2HAqQ9bo5'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [NY-HOMESTEAD-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:41Z

**File:** `rules/debt/state/new_york/ny_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/codes/new-york/cvp/article-52/5206/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.dfs.ny.gov/industry_guidance/exemption_from_judgments', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk7gUxwAoodN4sM8PMj'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [NY-HOMESTEAD-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:41Z

**File:** `rules/debt/state/new_york/ny_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk7gUxwAoodN4sM8PMj'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [NY-INCOME-EXECUTION-LIMIT] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:37Z

**File:** `rules/debt/state/new_york/ny_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/codes/new-york/cvp/article-52/5231/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk7bNt7sjiZhyoqaMHC'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [NY-INCOME-EXECUTION-LIMIT] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:37Z

**File:** `rules/debt/state/new_york/ny_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk7bNt7sjiZhyoqaMHC'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [NY-SOL-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:35Z

**File:** `rules/debt/state/new_york/ny_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/codes/new-york/cvp/article-2/213/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk7X5RLvGgyMb29YsfZ'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [NY-SOL-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:35Z

**File:** `rules/debt/state/new_york/ny_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk7X5RLvGgyMb29YsfZ'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-CIVIL-ANSWER-DEADLINE] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:34Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-412-20/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-412-20/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk7SLugh2b3rdDbQcY9'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-CIVIL-ANSWER-DEADLINE] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:34Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk7SLugh2b3rdDbQcY9'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-BANK-ACCOUNT-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:33Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-704-220/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-704-220/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk7MRzDhK5jspYBuD8D'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-BANK-ACCOUNT-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:33Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk7MRzDhK5jspYBuD8D'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-VEHICLE-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:32Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-704-010/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk7GtPmRZujWaexWESj'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-VEHICLE-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:32Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk7GtPmRZujWaexWESj'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-HOMESTEAD-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:31Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-704-730/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk7CR1Yj3Gnc68tmFQB'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-HOMESTEAD-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:31Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk7CR1Yj3Gnc68tmFQB'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-WAGE-GARNISHMENT-LIMIT] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:30Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-706-050/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/ca/code-of-civil-procedure/ccp-sect-706-050/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk77bHwQ2ZXUCd4RLoU'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-WAGE-GARNISHMENT-LIMIT] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:30Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk77bHwQ2ZXUCd4RLoU'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-ORAL-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:29Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/codes/california/code-ccp/part-2/title-2/chapter-3/section-339/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk72uGZWfWTbrK9N89s'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-ORAL-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:29Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk72uGZWfWTbrK9N89s'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-WRITTEN-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:28Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://law.justia.com/codes/california/code-ccp/part-2/title-2/chapter-3/section-337/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://law.justia.com/codes/california/code-ccp/part-2/title-2/chapter-3/section-337/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk6vLczjP3d5mgKpyhm'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [CA-SOL-WRITTEN-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:28Z

**File:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk6vLczjP3d5mgKpyhm'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-CIVIL-ANSWER-DEADLINE] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:26Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://www.courtrules.net/arizona/arizona-civil-procedure/rule-12', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk6aifedHqUVqZDnfw3'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-CIVIL-ANSWER-DEADLINE] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:26Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk6aifedHqUVqZDnfw3'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-TOOLS-OF-TRADE-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:22Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-33-property/az-rev-st-sect-33-1130/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk6WGmtiWQsrsRNLW8w'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-TOOLS-OF-TRADE-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:22Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk6WGmtiWQsrsRNLW8w'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-VEHICLE-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:21Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-33-property/az-rev-st-sect-33-1125/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk6S3HJdKz4jMgQvJE9'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-VEHICLE-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:21Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk6S3HJdKz4jMgQvJE9'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-HOMESTEAD-EXEMPTION] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:20Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-33-property/az-rev-st-sect-33-1101/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/az/title-33-property/az-rev-st-sect-33-1101/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk6Lp19QhPfRLQbF5eS'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-HOMESTEAD-EXEMPTION] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:20Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk6Lp19QhPfRLQbF5eS'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-WAGE-GARNISHMENT-LIMIT] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:18Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-33-property/az-rev-st-sect-33-1131/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/az/title-33-property/az-rev-st-sect-33-1131/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk6FYFaz32UGkBbST9e'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-WAGE-GARNISHMENT-LIMIT] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:18Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk6FYFaz32UGkBbST9e'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-ORAL-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:17Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-12-courts-and-civil-proceedings/az-rev-st-sect-12-543/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk6BH2Ci1xCo2woc4wk'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-ORAL-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:17Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk6BH2Ci1xCo2woc4wk'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-WRITTEN-CONTRACT-DEBT] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:16Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://codes.findlaw.com/az/title-12-courts-and-civil-proceedings/az-rev-st-sect-12-548/', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://codes.findlaw.com/az/title-12-courts-and-civil-proceedings/az-rev-st-sect-12-548/', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk5qsTfdYKucEBrvH6L'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [AZ-SOL-WRITTEN-CONTRACT-DEBT] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:16Z

**File:** `rules/debt/state/arizona/az_debt_state_layer_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk5qsTfdYKucEBrvH6L'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:12Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 5 of 5 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692g', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.law.cornell.edu/uscode/text/15/1692g', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.34', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk5YvzEhZSeUASVC1ga'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-VALIDATION-NOTICE-1692g] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:12Z

**File:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk5YvzEhZSeUASVC1ga'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:08Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 1 of 1 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692f', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk5TRqojX2XZGMDFN6A'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-UNFAIR-PRACTICES-CATALOG-1692f] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:08Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk5TRqojX2XZGMDFN6A'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:06Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1692e', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.18', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk5JcGSu6BBLSqfWZZv'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-FALSE-DECEPTIVE-CATALOG-1692e] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:06Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk5JcGSu6BBLSqfWZZv'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:20:04Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.ecfr.gov/current/title-12/chapter-X/part-1006/subpart-B/section-1006.14', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk4ex74VfG1bauTjJVy'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FDCPA-REGF-CALL-FREQUENCY-1006.14b] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:20:04Z

**File:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk4ex74VfG1bauTjJVy'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b] CITATION-CHECK-FAILED -- run run_20260826T171949Z, 2026-08-26T17:19:55Z

**File:** `rules/debt/federal/fcra_furnisher_dispute_v1.json`
**Classification hint (mechanical, not authoritative):** CITATION-CHECK-FAILED
**Evidence:** 2 of 2 cited source(s) could not be mechanically verified live: [{'url': 'https://www.law.cornell.edu/uscode/text/15/1681s-2', 'verified': False, 'method': 'live', 'error': None}, {'url': 'https://www.law.cornell.edu/uscode/text/15/1681s-2', 'verified': False, 'method': 'live', 'error': None}]

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk4CTenGBnAvjqJabAv'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


### [FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b] MODEL-DISAGREEMENT -- run run_20260826T171949Z, 2026-08-26T17:19:55Z

**File:** `rules/debt/federal/fcra_furnisher_dispute_v1.json`
**Classification hint (mechanical, not authoritative):** MODEL-DISAGREEMENT
**Evidence:** Numeric/citation fingerprints did not match across all three models (or one/more model reported ungrounded). Anthropic=[], OpenAI=[], Gemini=[].

**Per-model derivation results:**
  - claude-opus-5: grounded=None, error=Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}, 'request_id': 'req_011CeRk4CTenGBnAvjqJabAv'}, summary=None
  - gpt-5.5: grounded=None, error=Error code: 401 - {'error': {'message': 'Incorrect API key provided: (sk-proj**********************************************************************************************************************************************************EEA). You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}, summary=None
  - gemini-2.5-pro: grounded=None, error=400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'API key not valid. Please pass a valid API key.'}]}}, summary=None

**Resolution:** ________________
**Resolved by:** ________________  **Date:** ________________

---


