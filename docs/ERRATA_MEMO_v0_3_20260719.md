# ATTORNEY ERRATA MEMORANDUM — Golden Set CA-Notice v0.3

> **This file is a plain-text reference copy for diffability and grep.** The **executed, authoritative instrument is `ERRATA_MEMO_v0_3_20260719.docx`** (signed `/s/ Andrew M Cohen`, dated 07/19/2026), in this same directory. Where the two differ in any way, the signed .docx controls.

**Erratum IDs:** ERRATUM-2026-001 (CA-NOT-C-21); ERRATUM-2026-002 (CA-NOT-C-22)
**Date of determination:** 2026-07-19
**Attorney of record:** Andrew M. Cohen
**Affected artifact:** `goldenset_CA_notice_v0.3_FROZEN_20260716.xlsx` (SHA256 `e6dbb2fcb60de0773f9ff5594e09f74c6a6bac5670c70bd9bb76d70e2645df45`) — file remains byte-identical and BURNED; this memorandum is the authoritative correction overlay and travels with the file wherever it is cited.
**Trigger:** v0.3 held-out scoring run of 2026-07-19 (scorer v2.0-excel-native) and the resulting miss autopsy (`AUTOPSY_v0_3_MISSES_20260719.md`), which surfaced dual-model-consensus disagreement with frozen ground truth on the two items corrected herein.

---

## 1. Determination of law

Civil Code §1946.1 governs the length of notice required to terminate a residential periodic tenancy, independently of and in addition to the just-cause requirements of Civil Code §1946.2 (AB 1482):

- **§1946.1(b):** an owner "shall give notice at least 60 days prior to the proposed date of termination."
- **§1946.1(c):** notwithstanding (b), 30 days' notice suffices only where no tenant or resident has resided in the dwelling for one year or more.
- **Stancil v. Superior Court (2021) 11 Cal.5th 381:** the 60-day requirement attaches once any tenant has resided continuously for one year or more.
- **§1946.1(d):** the sole path to a 30-day notice for a 1+-year tenancy is the sale exception (dwelling alienable separate from title; bona fide sale; escrow and related conditions) — not present in either item's facts.

An exemption from AB 1482 just cause under Civil Code §1946.2(e)(7) or (e)(8) removes the just-cause obligation of §1946.2 only. It does not shorten, displace, or excuse compliance with §1946.1's notice-period requirements. A 30-day termination notice served on a tenancy of one year or more is void under §1946.1(b) regardless of the property's AB 1482 exemption status.

## 2. Errata

**ERRATUM-2026-001 — CA-NOT-C-21.** Facts as frozen: condominium, C of O 2015, natural-person owner, tenant resident 18 months, 30-day no-cause termination notice. Frozen outcome NOTICE_VALID is **ERRONEOUS**. Corrected ground truth: **NOTICE_INVALID** — the tenancy exceeds one year, so §1946.1(b) requires 60 days' notice; the 30-day notice is void (Stancil). The frozen analysis of the §1946.2(e)(7) exemption (property exempt from just cause; rolling 15-year window correctly computed) remains correct as far as it goes, but is non-dispositive: the exemption does not cure the notice-period defect.

**ERRATUM-2026-002 — CA-NOT-C-22.** Facts as frozen: single-family home, qualifying natural-person owner, compliant exemption disclosure at inception, tenant resident 2 years, 30-day no-cause termination notice. Frozen outcome NOTICE_VALID is **ERRONEOUS**. Corrected ground truth: **NOTICE_INVALID** — same §1946.1(b)/Stancil analysis; the §1946.2(e)(8) exemption is validly established on the facts but non-dispositive. Noted additionally and also non-dispositive: the notice's self-citation to §1946.2(e)(7) is the wrong subsection for a single-family home (correct: (e)(8)), an irregularity mirroring the subsection swap corrected at freeze.

**Unaffected:** CA-NOT-C-18 (9-month tenancy; 30-day notice proper under §1946.1(c); frozen VALID stands). All other frozen items reviewed for the same defect pattern at the time of this memorandum: no other item pairs a 1+-year tenancy with a sub-60-day notice; no further errata.

## 3. Root cause and corrective protocol

Root cause: single-lens review at the freeze session of 2026-07-16. The facilitator presented C-21 and C-22 solely through the AB 1482 exemption analysis they were drafted to test; the independent §1946.1 duration check was not run against the stated tenancy lengths, and the attorney ruled on the framing presented. Classified under the standing error taxonomy as an incomplete-defect-sweep failure (kin to the incomplete multi-prong-test class).

Corrective protocol, adopted effective immediately for all future golden-set freezes (v0.4 forward): **every candidate item shall be reviewed against every encoded defect class in the module, not only the defect class the item was drafted to test.** The review checklist shall enumerate the module's defect classes and require an explicit per-item pass. The rules file's ratified defect list may be used as the sweep checklist; model outputs may not be consulted during ground-truth review.

## 4. Effect on reported metrics

The v0.3 held-out set remains BURNED. The frozen file is not edited. Metrics shall be dual-reported wherever the v0.3 score is cited:

- **As-frozen:** 23/26 = 88.5% (the score against ground truth as it stood at scoring).
- **Post-errata:** 25/26 = 96.2% (the score against corrected law). B2 confident-wrong restated 3 → 1 (C-18 only, the confirmed coverage gap).
- **Ground-truth error rate:** 2/26 = 7.7%, detected by dual-model-consensus disagreement — recorded as a validation finding in its own right: the review pipeline corrected the encoder's citation errors at freeze, and the scoring pipeline surfaced the attorney-side oversight at measurement. Both directions of the loop functioned.

Neither corrected item's outcome may be cited as machine-validated; the corrected ground truth in Section 2 is attorney-determined and crosses no attorney line.

## 5. Execution

This memorandum is effective upon the attorney's signature below and shall be committed alongside the frozen golden set, referenced in VALIDATION_METRICS_LEDGER, PROJECT_STATE_OF_RECORD, and DAILY_CHANGELOG, and incorporated by reference in any future citation of the v0.3 score.

**Determined and adopted:**

______________________________
Andrew M. Cohen, Attorney of Record
Date: ____________

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
