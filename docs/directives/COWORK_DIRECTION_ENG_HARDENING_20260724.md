# Cowork Change Directive — Engineering Hardening: CI, Secrets, and Instrument Validation

**Date:** 2026-07-24
**Approved by:** Andrew M. Cohen (Andy)
**Scope:** the validation *infrastructure* (scorer, harness, dispatcher, repo hygiene) — not the legal rules. Nothing here edits any rules version; vProof1 and v3 remain untouched. Motivation: an enterprise-practices audit found the rules pipeline meets or exceeds best practice (untrusted-output posture, small-batch integration, regression gating, risk-based review) while the infrastructure that *produces our published numbers* is held to a lower standard than what it measures. This directive closes that gap. All tasks GREEN unless noted; sequencing below keeps the v0.4 line undisturbed.

---

## Task 1 — Secret hygiene (URGENT — execute first, today)

1. Enable GitHub secret scanning and push protection on the repo.
2. **Full-history scan** for leaked credentials (API keys, tokens) using a standard scanner across all commits, not just HEAD — the repo is public and the scorer runs with real keys. If anything is found: rotate the affected keys immediately, then report; do not merely delete (history retains it).
3. Verify `.env` / key files are gitignored; add a pre-commit hook blocking common secret patterns.
4. Report completion and findings same-day.

## Task 2 — CI pipeline (this week, alongside proposal 16)

GitHub Actions workflow on every push/PR: (a) JSON well-formedness + schema validation for all rules files (schema per Task 3); (b) scorer unit-test suite; (c) **frozen-artifact integrity check** — recompute SHA256 of every frozen file (vProof1, v3, frozen golden sets, signed errata) against a committed manifest; any drift fails the build; (d) lint. This converts our existing gates from directive-invoked to structurally enforced: a push that breaks schema, tests, or frozen-file integrity cannot land quietly.

## Task 3 — Formal rules schema (this week)

Author a JSON Schema for the rules-file format: required fields, input contracts (e.g., `per_tenant_continuous_occupancy_years` as array-of-numbers), enum'd outcome values, required provenance blocks (statute pins, ratification metadata, determinations array). Validate v3 against it; fix nothing in v3 (if v3 fails the schema, adjust the *schema* to document reality and log the delta for the next version cut). Wire into CI.

## Task 4 — Scorer calibration suite (this week)

Known-answer testing for the measurement instrument: synthetic items with *forced* model outputs (bypassing live models) covering — correct/incorrect/mixed outcomes; consensus vs. disagreement vs. single-model; held-out vs. dev flag handling (verify the never-blend rule structurally); α computation against hand-computed values; malformed model output handling. The suite must prove the scorer reports what actually happened in every branch. Wire into CI. Rationale: a subtle scorer bug would silently corrupt the published record while every process around it looked clean; instruments get calibrated.

## Task 5 — Coverage matrix (after v0.4 freeze; analysis-only)

Map which encoded rules are exercised by which frozen golden-set items; report % of rules touched by ≥1 item, per module. Sources: v0.2 dev, v0.3 (analysis-only mapping — this is not a re-score and consumes nothing), v0.4 once frozen. Untested rules are logged as candidate items for future set drafting — v0.3's lesson in structured form: untested and unencoded look identical until a miss reveals the difference.

## Task 6 — Mutation-testing pilot (after v0.4 scoring; novel — report before any conclusions)

Method: perturb a **copy** of the active rules (flip a subsection reference, change a day count, invert a threshold — a catalog of ~10–15 legally meaningful mutations), run the scorer against the **dev set only** (never a burned held-out set; scored runs against v0.3 are prohibited), and measure the *detection rate*: what fraction of mutations does the test set catch? Undetected mutations are golden-set sensitivity gaps — log each as a candidate item. Deliver as a method-and-results report for Andy before anything is claimed; this tests whether our test sets have the statistical power to notice mis-encoded law, and to our knowledge has not been done for encoded legal rules (candidate methodology publication alongside the lower-bound benchmark work).

## Task 7 — Package the scorer for independent review (with Task 4)

Prepare `rules/validation/scorer/REVIEW_README.md`: what the scorer does, line count, how to run the calibration suite, known limitations, and the specific review questions (parsing correctness, α computation, held-out flag handling, failure modes). The reviewer will be external (a partner lab engineer or clinic-adjacent CS students — Andy's ask to make); this task makes that ask a 2-hour favor instead of a spelunking expedition.

## Sequencing & reporting

Task 1 today; 2–4 and 7 this week interleaved with proposal 16 (none touch the rules line); 5 after the v0.4 freeze; 6 after v0.4 scoring. Fold into morning reports; ledger note when CI goes live ("all published numbers from this date produced under CI-enforced integrity checks" — worth a line in the validation record).

**Definition of done:** secret scan complete with findings resolved; CI live and green; schema committed and enforced; calibration suite passing in CI; coverage matrix delivered; mutation pilot report delivered; scorer review package committed.

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
