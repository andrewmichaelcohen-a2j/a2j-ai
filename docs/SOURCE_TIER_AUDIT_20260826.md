# Debt-track source-tier audit — 2026-08-26

Per Andy's ratified four-tier source hierarchy (replaces the earlier binary primary-only rule):

- **A — official government source.** Default anchor, required where machine-accessible.
- **B — recognized noncommercial republisher** (e.g. Cornell LII, CourtListener). Anchor only where the official source is machine-hostile; `tier_rationale` required.
- **C — commercial aggregator** (e.g. FindLaw, Justia). Corroborating signal only, never the sole anchor.
- **D — legal-help / case-brief content.** Corroboration only, same restriction as C.

`source_tier` (and `tier_rationale`) added to `rules/schema/debt_schema_v1.0.json` as optional fields on each `grounded_derivation.derived_from[]` entry. Backfilled corpus-wide this round by domain classification — every existing citation in the 9 debt rules files now carries a tier.

## Tier distribution, corpus-wide (63 source entries across 37 nodes)

| File | A | B | C | D |
|---|---|---|---|---|
| `federal/fcra_furnisher_dispute_v1.json` | 0 | 2 | 0 | 0 |
| `federal/fdcpa_conduct_prohibitions_v1.json` | 3 | 2 | 0 | 0 |
| `federal/fdcpa_validation_notice_v1.json` | 3 | 2 | 0 | 0 |
| `state/arizona/az_debt_state_layer_v1.json` | 0 | 0 | 10 | 0 |
| `state/california/ca_debt_state_layer_v1.json` | 0 | 0 | 11 | 0 |
| `state/new_york/ny_debt_state_layer_v1.json` | 3 | 0 | 6 | 0 |
| `state/texas/tx_debt_band3_discretionary_v1.json` | 0 | 0 | 2 | 1 |
| `state/texas/tx_debt_state_layer_v1.json` | 2 | 0 | 5 | 1 |
| `state/utah/ut_debt_state_layer_v1.json` | 1 | 0 | 9 | 0 |
| **Total** | **12** | **6** | **43** | **2** |

**Federal spine: clean.** Every federal node anchors on eCFR (A) and/or Cornell LII (B, with rationale: Cornell LII is the field-standard noncommercial republisher for the U.S. Code, no machine-hostility issue found). No violations.

**State layers: not clean.** 27 of the corpus's 30 state-layer nodes have no A or B source at all — Tier C (mostly FindLaw, some Justia) is the *sole* anchor, which the ratified hierarchy treats as a sourcing-discipline violation, not a data point to publish as-is:

| State | Nodes | Violations (C/D-only) |
|---|---|---|
| Arizona | 7 | **7 of 7** |
| California | 7 | **7 of 7** |
| Utah | 6 | **5 of 6** (answer-deadline node is clean — legacy.utcourts.gov, A) |
| Texas | 6 | **4 of 6** (homestead is clean via statutes.capitol.texas.gov, A) |
| New York | 6 | **3 of 6** (homestead/vehicle/personal-property are clean via NY DFS, A) |

## AZ re-pin attempt — result: blocked, not silently downgraded

Andy's direction was to re-pin AZ to azleg.gov (Tier A) with FindLaw retained as Tier-C corroboration. Attempted this round; **the primary source turned out to be machine-hostile, confirmed directly, not assumed:**

- Direct fetch of `azleg.gov/ars/12/00548.htm` and `azleg.gov/ars/12/00543.htm` returned "You are being redirected... Javascript is required" — no statute text reachable without a JS-executing browser, which this session's tools don't have.
- Checked for a Tier B fallback: Cornell LII's Arizona page (`law.cornell.edu/states/arizona`) does **not** host Arizona statute text itself — it only links back to azleg.gov. No other "recognized noncommercial republisher" covering full AZ statute text was found.
- Attempted the Wayback Machine as a way to reach an already-rendered archived copy of the same official page — blocked at the tool level (`web.archive.org` is on this session's fetch blocklist).
- Re-tested a few `statutes.capitol.texas.gov` chapter-level URLs for the *Texas* violations while investigating this (opportunistic, since that domain is already a confirmed-working Tier A source for one TX node) — they returned the site's navigation shell, not chapter text, suggesting that source may also be JS-rendered for some URL patterns. Not resolved this round.

**Result:** AZ's 7 nodes remain Tier-C-anchored (FindLaw) — an honest, unresolved gap, not a relabeled A or B. This is flagged rather than papered over. **Practical next step:** since the blocker is JS execution, not missing effort, the fastest real fix is either (a) Andy fetching the azleg.gov text himself in a real browser and pasting it back for a genuine Tier-A re-pin, or (b) a future session with browser-automation tooling available. Logged as HORIZON, not closed.

## Not yet attempted this round (queued, not silently deferred)

CA (7 violations), UT (5), NY (3), and TX's remaining (4) — the domain audit above is complete for all of them, but the actual re-pin research (finding and confirming a fetchable Tier A or B source, same process as AZ) was not run this round given time spent on the AZ investigation and the corroboration-runner bugs (see `DAILY_CHANGELOG.md`). Recommended order for the next pass: **UT and NY first** (each already has one confirmed-working Tier A domain in this corpus — `legacy.utcourts.gov` and `dfs.ny.gov` respectively — so the remaining gaps may be reachable via the same domains' statute-hosting sections rather than a fresh domain hunt), then CA, then the TX/AZ JS-gated cases last (likely need the browser-automation path).

---

*No rules file content, tier, or citation was silently altered — every `source_tier` value added this round is a domain classification of an existing, already-cited URL; no citation was removed, and the AZ investigation above is reported as attempted-and-blocked, not claimed as done.*

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
