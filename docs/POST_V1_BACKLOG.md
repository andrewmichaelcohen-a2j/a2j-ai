# POST_V1_BACKLOG -- improvement candidates for debt-demo-v1.0 nodes

*Opened 2026-09-05 under the LOCK directive (Phase LOCK item 1). Copyright 2026 Andrew M Cohen. Apache 2.0.*

**Rule.** As of the `debt-demo-v1.0` freeze, the 19 demo-corpus nodes are immutable (CI-enforced via
`scripts/ci/frozen_artifact_manifest.json`; per-node hashes in
`rules/debt/validation/debt_demo_v1.0_manifest.json`). Every Stage B finding, citation failure, or improvement
candidate that touches a v1.0 node is recorded HERE -- materiality-classified, dangerous-direction flagged --
and is otherwise untouched. Nothing in this file is applied to v1.0. It is the v1.1 work queue.

**What still changes:** `rules/debt/validation/stage_b_dispositions.json` (the runner's ledger -- a backlog
entry is recorded there too, classification `BACKLOG-V1.1`, so later runs tag a repeat finding instead of
re-reporting it); the docs; the runner (one-variable rule); non-v1.0 rules files (UT/AZ/NY stubs).

**Classification key** (same as `DEBT_STAGE_B_TRIAGE.md`, plus one): FIXED-VERIFIED / FIXED-SOURCE-NAMED /
GLOSS-FOR-COUNSEL / COVERED / HORIZON / NOT-A-GAP describe what the fix WOULD be; **BACKLOG-V1.1** is the
status of every row here until a v1.1 release opens. **DD** = dangerous direction (the node as frozen would
tell a consumer they are safe / have no claim / are out of time when the opposite is true).

**Escalation.** A BACKLOG row marked DD = yes on a v1.0 node is a known dangerous-direction error in a frozen
release. It does not unfreeze the node; it is surfaced to Andy in the morning report the day it is recorded
and listed in the counsel queue for the promotion decision (Phase LOCK item 5). Promotion to VALIDATED with an
open DD row is Andy's call, made explicitly, never by default.

## Backlog (newest first)

| # | Date | Node | Finding | Would-be class | DD | Source run / origin | Notes |
|---|---|---|---|---|---|---|---|
| (none yet -- the measurement-of-record run populates this table) | | | | | | | |

## Pinning backlog carried into v1.1 (from round 46 -- named, not fetched)

These are `FIXED-SOURCE-NAMED` provisions already encoded as notes in v1.0 nodes whose text was not fetched
and pinned before the freeze. Pinning them is a v1.1 content change (it adds `derived_from` entries), so it
waits here: UCC 9-609(b)(2) (Cal. Com. Code 9609 / Tex. Bus. & Com. Code 9.609); 47 U.S.C. 227(b)(1)(A)(iii);
20 U.S.C. 1095a; 26 U.S.C. 6331/6334; CCP 706.070-.084, 706.023; CCP 697.310, 704.950; CCP 704.740-704.800;
CCP 720.110; CCP 703.010, Fin. Code 864; Fam. Code 910/911; CCP 431.30(b)(2), 458; CCP 430.10, 435-436,
472a(b); Tex. Lab. Code 408.201; TRCP 664a; TRCP 500.3(e); TRAP 26.1(a), 26.3; TRCP 329b(e); Fam. Code
3.102, 8.106, 158.003-.004; Civ. Code 1657; Gov. Code 70611/68631; Tex. Const. art. XVI 50(a)(5).

## HORIZON nodes (not v1.0 scope; recorded so the gate node design question stays visible)

BANKRUPTCY-OVERLAY gate; state mini-FDCPA (Rosenthal / Tex. Fin. Code ch. 392 / 940 CMR 7.00); TCPA
(47 U.S.C. 227) overlay; Reg F electronic-communication rules (1006.6(b), 1006.14(h), 1006.22(f)).
