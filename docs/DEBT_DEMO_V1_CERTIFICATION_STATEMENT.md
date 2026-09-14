# debt-demo-v1.0 -- Release Certification Statement (DRAFT for Andy's ratification)

*Governance Step 1 (Addendum 2026-09-05, s.6). Draft prepared by Cowork 2026-09-14. Not in force until signed.
Copyright 2026 Andrew M Cohen. Apache 2.0.*

## Certification

I, the undersigned attorney, certify as to the release of the Civil Justice as Code debt-track rules corpus
named **`debt-demo-v1.0`** (freeze commit `89da5bc`; no git tag) in the repository `github.com/andrewmichaelcohen-a2j/a2j-ai` (19 nodes; per-node
SHA-256 hashes in `rules/debt/validation/debt_demo_v1.0_manifest.json`), as verified on the dates recorded
in that manifest, that:

1. **Every node was audited against its cited primary sources** under the published census-audit protocol
   (`docs/audit/README.md`): the node's logic and completeness checklist were read in full; every citation
   carrying a url was either live-verified by the corroboration runner's citation checker or manually verified
   by me against the cited source; provisions named in notes but not pinned are listed on the node's sheet and
   were either checked or carried to the v1.1 backlog.
2. **Every material adversarial finding was dispositioned** as recorded in the disposition ledger
   (`rules/debt/validation/stage_b_dispositions.json`) and the triage record (`docs/DEBT_STAGE_B_TRIAGE.md`):
   fixed with a verified source, fixed with a named source, ruled on by me as counsel
   (`docs/DEBT_COUNSEL_QUEUE_V1.md`), recorded as covered elsewhere, or carried to `docs/POST_V1_BACKLOG.md`
   with its materiality and dangerous-direction classification. Any dangerous-direction row left open on a
   promoted node is identified on that node's sign-off sheet with my reason for promoting it.
3. **The metrics are as recorded** in the measurement-of-record entry of the manifest (run
   `run_20260905T175137Z`): Stage A three-model grounded agreement, citation verification, Stage B parse
   health, and the count of findings surfaced and dispositioned, reported raw and as dispositioned.
4. **Tier labels are mine.** Each node's `tier` (DRAFT / CORROBORATED / VALIDATED) at this release was set by
   me on the node's sign-off sheet after steps 1-3, and only nodes so signed carry a tier above DRAFT.

## What this certification does not do

- It **does not warrant any outcome in any individual matter.** The corpus encodes rules, thresholds, and
  screening questions; whether they apply to a person's facts, and what a court will do, is not certified.
- It **is not legal advice to any person**, and no attorney-client relationship is created by its use. Output
  derived from the corpus is legal information. Anyone relying on it for a decision should consult a lawyer.
- Its **scope is limited to the named release** (`debt-demo-v1.0`) and the verification dates in the manifest.
  Law changes; the release carries a freshness commitment (quarterly re-verification, manifest
  `freshness_commitment`) but no representation that a citation remains current after its verification date.
- It covers **process compliance**, not completeness: the corpus addresses the 19 nodes it contains, in the
  jurisdictions it names, and nothing else; known gaps are listed in `POST_V1_BACKLOG.md` and the HORIZON list.
- It is **an individual attorney's certification of process.** Co-certifiers, an editorial board, and
  institutional governance are out of scope for this release and are not implied.

## Signature

Certifying attorney: ______________________________  Bar: ______________

Signature: ______________________________  Date: __________

Release: `debt-demo-v1.0` (freeze commit `89da5bc`) · Manifest sha256 of `debt_demo_v1.0_manifest.json` at signing: ______________________________

*Cowork's note for ratification: the four attestations in the Certification section are worded to be true only
after the counsel session and the census audit are complete; signing before then would attest to something not
yet done. Wording changes are Andy's; nothing here is final until he says so.*
