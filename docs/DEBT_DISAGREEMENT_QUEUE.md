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


