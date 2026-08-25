# Debt-defense rules

Per `docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md` (v4). Phase A build, started 2026-08-25.

- `federal/` — jurisdiction-agnostic spine (FDCPA, Regulation F, FCRA). One encoding, amortizes across all 50 states + DC.
- `state/<state>/` — state layer: SOL by claim type, answer deadlines, garnishment/post-judgment exemption amounts, service/default-judgment procedure. Anchor states per spec §10: TX (locked, decision 2026-08-25), CA, UT, AZ, NY.

Every file validates against `rules/schema/debt_schema_v1.0.json`. Tier (`DRAFT`/`CORROBORATED`/`VALIDATED`) and band (1/2/3) are **node properties**, not file properties — see the schema's description field and spec §2/§4 for why this differs from the eviction line's per-file `file_status`.

No node in this tree may be cited as `VALIDATED` until it clears the sampling-audit pipeline in spec §3 — see `docs/PROJECT_STATE_OF_RECORD.md` for the current state of any release certification.
