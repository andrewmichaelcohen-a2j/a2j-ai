---
name: consumer-debt-validation
description: "Screen a consumer debt collection matter for common defenses and produce a plain-language, cited analysis. Use when a consumer has been contacted or sued by a debt collector or debt buyer and needs to understand potential defenses such as time-barred debt, wage-garnishment exposure, FDCPA validation/dispute rights, or a discretionary judgment call like a default-judgment set-aside. Assists screening and analysis only; does not provide legal advice or practice law."
---

# Consumer Debt Validation

> **STATUS: CONCEPT-DEMO scaffold (2026-08-26). NOT ATTORNEY-VALIDATED.**
> This skill's logic is now wired to `rules/debt/` (the schema-validated, tier-labeled node
> corpus built under `docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md`), superseding this file's original
> plan to hand-author jurisdiction data as plain markdown in `../../jurisdictions/`. See
> "Reconciliation note" below — flagged rather than silently resolved, since this skeleton
> predates the current architecture by several build phases and the two were never reconciled
> until now.
>
> **Every node this skill can currently draw on is DRAFT tier** (federal + TX + CA + Band-3
> discretionary node) or DRAFT tier awaiting grounded-corroboration (UT/AZ/NY, visible but not
> relied upon by any scenario below). No node here is CORROBORATED or VALIDATED yet — that
> requires `scripts/corroboration/run_corroboration.py` to actually run against real API keys
> (Andy's environment) and, later, Phase D's attorney census audit. **Any live showing of this
> skill, to any audience, must open with the framing sentence in "Claims discipline" below and
> keep tier labels visible throughout — no exceptions, per spec §8's CONCEPT-DEMO row.**

## Skill metadata

- **Version:** 0.3.0-concept-demo (adds HOW_TO_RUN.md and CLAIM_LANGUAGE_CARD.md, round 14)
- **Corpus:** `rules/debt/federal/` (5 nodes) + `rules/debt/state/texas/` (6 nodes, including the
  Band 3 discretionary node) + `rules/debt/state/california/` (7 nodes) = 18 nodes in the
  concept-demo corpus. `rules/debt/state/{utah,arizona,new_york}/` exist as fully-drafted DRAFT
  content (ahead of the "visible stub" minimum) but are explicitly out of demo-reliance scope —
  visible in the tree, tier-labeled, not used by any scenario below.
- **Last reviewed:** not yet reviewed — no CORROBORATED or VALIDATED node exists in this corpus yet.
- **Supervising attorney:** Andrew M Cohen.
- **Legal frameworks:** FDCPA (15 U.S.C. §1692 et seq.) + Regulation F (12 C.F.R. §1006) + FCRA
  furnisher-dispute duties (15 U.S.C. §1681s-2(b)); Texas and California statutes of limitations,
  wage-garnishment/exemption law, and civil-answer-deadline rules; Craddock v. Sunshine Bus Lines
  (Tex. 1939) and Tex. R. Civ. P. 329b for the Band 3 default-judgment scenario. Full citations
  live in each node's `grounded_derivation.derived_from`, not duplicated here.

## Reconciliation note (2026-08-26)

This file originally planned to source jurisdiction data as hand-authored markdown in
`../../jurisdictions/` (still empty except its own README). That approach was superseded in
practice by the schema-validated JSON node system built under `rules/debt/` starting 2026-08-25
(`rules/schema/debt_schema_v1.0.json`), which adds per-node tier labeling, grounded-derivation
provenance, and a corroboration pipeline that the plain-markdown plan never specified. Rather than
build a second, parallel skill from scratch, this file is updated in place to point at the real
corpus. `jurisdictions/` and `test-cases/` are left as-is (not deleted) — `test-cases/`'s fabricated
fact-pattern discipline is still the right model for eventual frozen golden-set items under
Direction E, once that workstream reaches debt (see spec §5); it just isn't populated yet.

## Important scope statement

This skill **assists** a self-represented litigant or a supervising attorney by screening a
consumer debt matter and organizing a plain-language, cited analysis. It does **not** provide
legal advice, does not establish an attorney-client relationship, and does not practice law. All
output must be reviewed by a supervising attorney before being relied upon or shared with a
client — doubly true at CONCEPT-DEMO status, where nothing is even CORROBORATED yet.

## Out of scope

- Bankruptcy strategy and filings.
- Counterclaims or affirmative litigation beyond defensive screening.
- Jurisdictions outside the current corpus (TX, CA for reliance; UT/AZ/NY visible DRAFT only).
- Predicting the outcome of any genuinely discretionary judicial determination (Band 3 — see the
  default-judgment scenario below; the system names the factors a court weighs and never
  forecasts the result).
- Any situation flagged for escalation below.

## 1. When to use this skill

Triggered by a consumer describing: being served with (or fearing) a debt-collection lawsuit;
receiving pre-suit collector calls or letters; facing or already subject to wage garnishment; or
already having a default judgment entered against them and wanting to know if it can be reopened.

## 2. Intake

Elicited conversationally, per each relevant node's `completeness_checklist` (not asked as a
rigid form) — e.g., which state, whether a lawsuit has been filed and when served, the debt type
and last-payment/default date, whether a debt-validation notice was ever sent, employment/income
facts if garnishment is in play, and — for the Band 3 scenario — the judgment date and the
person's own account of why they missed the deadline (collected as raw input; the system does
not characterize it).

## 3. Decision logic

Applies the matching node(s) from `rules/debt/`, tier label surfaced with every answer:
- SOL / time-bar check (`{TX,CA}-SOL-*`).
- Answer-deadline computation (`{TX,CA}-*-ANSWER-DEADLINE`; note `TX-JUSTICE-COURT-DEBT-ANSWER-DEADLINE`
  is `citation_verified: false` pending the corroboration runner — do not present it as
  citation-confirmed until that clears).
- Wage-garnishment exposure (`TX-WAGE-GARNISHMENT-PROHIBITION`, `CA-WAGE-GARNISHMENT-LIMIT`).
- FDCPA §1692g validation/dispute rights (`FDCPA-VALIDATION-NOTICE-1692g`), FDCPA conduct
  catalogs (`FDCPA-{FALSE-DECEPTIVE,UNFAIR-PRACTICES}-CATALOG`), FCRA furnisher-dispute duty.
- Band 3 boundary marker (`TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY`): names the Craddock
  three-factor test and the hard 30-day/75-day TRCP 329b deadlines, refuses to predict the
  court's discretionary call, and routes to attorney consultation for factors 1-2.

## 4. Output

Plain-language answer, the node(s) relied on with their tier and citation, and
`consequences_and_next_steps` from the node — deadlines flagged with urgency where
`deadline_type` is `fixed_date`/`relative_days`.

## 5. Claims discipline (per spec §8 CONCEPT-DEMO row — non-negotiable at this status)

Every showing opens with: *"This is a demonstration system. Its content is machine-corroborated
against cited law — three independent AI models, citations verified against live sources — and
not yet attorney-validated. The attorney-validation layer is designed and is what this project is
building toward."* Numbers only with basis attached in the same breath (e.g., "X% three-model
grounded agreement across the demo corpus," never a bare "X% accurate"). No "validated,"
"near-perfect," or reliability-target language. Audience: Andy-selected only — not press, not
consumers, not a public link.

**One-page reference:** `CLAIM_LANGUAGE_CARD.md` in this folder — what Andy may and may not say,
with each number's basis, formatted to keep beside him during a live showing rather than
re-deriving from this spec section each time.

## 6. Escalation triggers

Any Band 2/3 judgment call; any node below CORROBORATED tier being relied on for a real (not
demo) user's situation — currently every node in this corpus; any fact pattern outside TX/CA;
any sign the person needs immediate emergency legal help beyond what a citation-and-deadline
screen can offer.

## 7. Prepared demo scenarios

See `scripts/corroboration/scenarios.json` for the 5 prepared scenarios (TX SOL/answer, CA
SOL/answer, pre-suit validation rights, garnishment, Band 3 refusal-boundary) and their node
dependencies — the same file the corroboration runner uses to compute `scenario_pass_rate`. This
skill also supports a live unscripted ask against any corpus node, tier labels shown honestly
regardless of which path (prepared or unscripted) the conversation takes.

**Running a live showing:** see `HOW_TO_RUN.md` in this folder — a three-step, voice-mode-ready
note for Andy (not written for the AI's own operational logic, which is what the rest of this
file is for).

## 8. Jurisdiction data references

Superseded by `rules/debt/state/{texas,california}/` — see Reconciliation note above.
`../../jurisdictions/` is not populated and is not the active data source.

## 9. Test cases

Not yet built — `../../test-cases/`'s fabricated-fact-pattern format is still the intended model
for future frozen golden-set items (Direction E, spec §5), once that workstream reaches debt.
Not required for the concept demo, which uses the 5 prepared scenarios above instead of a scored
golden set (per the 2026-08-26 directive's "demo harness = the skill itself" framing).

---

*Copyright 2026 Andrew M Cohen. Licensed under the [Apache License, Version 2.0](../LICENSE).*
