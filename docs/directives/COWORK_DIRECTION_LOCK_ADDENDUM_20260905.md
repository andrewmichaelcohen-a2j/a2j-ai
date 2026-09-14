# Cowork Direction — Addendum to LOCK & EXPERIMENTS (Cost Rules, Review Artifacts, Lift Priority, Refresh, Landscape)

**Date:** 2026-09-05 (evening) · **From:** Andy (planning with Claude) · **Effect:** Supplements COWORK_DIRECTION_LOCK_DEBT_DEMO_V1_20260905. Nothing there is rescinded; sequencing changes and additions below.

## 1. Standing cost-efficiency rules (effective immediately)
- Session batching: Cowork sessions run against a written agenda (a directive or a queued item list) and close when it's done — no open-ended exploration sessions. Consolidate small items into the next scheduled session rather than opening new ones.
- Replay-first is law for the EXPERIMENT phase: every ablation arm that can run on recorded fixtures runs on recorded fixtures. Live calls only where a configuration genuinely requires fresh model output, itemized in the pre-registered design with per-arm dollar estimates, Andy's go required before any live spend.
- Per-run caps stay ($15) and every requested Andy run comes with a cost estimate attached.
- Andy-side (for the record): console.anthropic.com → Usage reviewed weekly; monthly spend limit set; auto-reload threshold confirmed at Andy's comfort level.
- Budget envelope for the full LOCK+EXPERIMENT phase: pipeline spend target ≤ $250; flag before anything would exceed it.

## 2. Zero-cost Andy review artifacts (new standard, effective immediately)
Every document produced for Andy's personal review — the counsel queue, census-audit sheets, experiment designs awaiting his go, claim cards — is delivered as both the in-repo markdown and a formatted PDF, written to `review/` in the repo, with the changelog entry naming the exact file and a one-line open instruction ("double-click `review/DEBT_COUNSEL_QUEUE_V1.pdf`"). Andy must be able to read everything on his desktop with no AI session running and no cost. First deliverable under this rule: regenerate `DEBT_COUNSEL_QUEUE_V1` as a PDF now, formatted for reading (one item per page section: proposition · authority · risk-if-wrong · ruling line with confirm/strike/modify checkboxes and a notes field). Census-audit sheets follow the same standard when built (one PDF per node or one bound PDF, Andy's sign-off line on each sheet).

## 3. Lift ablation — PROMOTED to demo-gating (resequenced ahead of the configuration ablation)
Act 2 of the demo (raw model vs. CJaC-grounded, side by side) requires the pre-registered lift number. Therefore: pre-register the lift design first (arms: each of the three frontier models raw, no rules; vs. the grounded system; frozen scenario set of 15–20 expanded from the demo five, frozen before any arm runs; scoring against v1.0 ground truth with abstention credit; dual-reported). Deliver the design + budget for Andy's go immediately after the LOCK measurement-of-record. The configuration ablation follows the lift run.

**3a. Informal rehearsal kit** (deliver with the lift design; costs nothing to produce). Three scenario prompts — the CA COVID-tolling SOL scenario, the TX bank-account exemption trap, an FDCPA validation-rights fact pattern — each with the grounded system's expected answer and citations. Marked prominently: REHEARSAL ONLY — NOT EVIDENCE; NO EXTERNAL CLAIMS. Purpose: Andy can paste the prompts into raw models himself to see the contrast firsthand before the formal number exists.

## 4. Continuous-improvement loop — methodology-complete, minimally operated
- Method v1.0 document (EXPERIMENT deliverable) must include the full refresh/improvement loop as a designed component: D-3 statute-and-case watch (self-generating watchlist from citation pins), D-4 standing adversarial generation (live — the Stage B lane), telemetry-to-improvement queue (designed), with the cost model for operating each at scale. Honest labeling: designed vs. running.
- Minimal manual refresh protocol for v1.0 (new, cheap): a quarterly re-verification pass — one scheduled run of the citation checker across the frozen corpus's pins, results to the backlog, cost ≈ one smoke-scale run. Write the protocol into the v1.0 manifest so the certified release carries a freshness commitment from day one. D-3 automation build remains HORIZON (post-demo).

## 5. Landscape tasks (GREEN, fold into the next scheduled session)
- A2JRAG assessment: fetch the LawDroid/LANC A2JRAG publication; summarize what it is (dataset? benchmark? method paper?); assess feasibility and cost of scoring the CJaC-grounded system against it; recommendation memo to `review/` (md+PDF). If it's a usable objective benchmark, it becomes a candidate external-validation event — flag it as such.
- Ecosystem/puzzle map data: refresh the spec's integration map into a current one-page dataset for the messaging build — layers and named parties (model platforms/Claude for Legal; LawDroid workflow layer; Courtroom5 pro-se delivery; Spot/intake upstream; Assembly Line + e-filing downstream; LII/CourtListener/eCFR sources; LHC/JusticeBench standards; regulatory venues UT/AZ) with CJaC's layer marked. Claude drafts the visual; Cowork supplies verified names/facts only.
- Add to the landscape note in the record: Claude for Legal (2026-05-12, commercial practice areas + clinic/student tools, attorney-responsibility disclaimer), LawDroid Legal Aid Plugin (2026-05-20, open-source, workflow layer), U.S. v. Heppner (S.D.N.Y. 2026 — no privilege in consumer AI chats; reinforces information-not-advice posture).

## 6. Certification statement — governance Step 1 (GREEN draft for Andy approval)
Draft the precise v1.0 release-certification language for Andy's ratification: what the named-attorney signature attests (process compliance: every node audited against cited primary sources per the published protocol; all material findings dispositioned per the ledger; metrics as recorded in the measurement-of-record) and what it expressly does not (no warranty of outcome in any individual matter; not legal advice to any person; scope limited to the tagged release and its verification date). One page, md+PDF to `review/`. Co-certifier and institutional-governance structures are explicitly OUT of scope — messaging will present them as what sponsorship builds.

## 7. Sequencing summary (supersedes prior ordering where different)
1. Round 46 + LOCK patches applied → tag → measurement-of-record (Andy runs smoke + full, ~$10).
2. Item 2's counsel-queue PDF → Andy gloss session (with Claude) → rulings patch → re-freeze.
3. Lift ablation (design → Andy go → run) + rehearsal kit.
4. Census audit (sheets per item 2 standard → Andy's half-day) → tier promotions → first VALIDATED release.
5. Configuration ablation → Method v1.0 (incl. §4 refresh loop) → messaging build (Claude drafts).
6. Landscape tasks (§5) and certification statement (§6) fold into the earliest sessions without displacing 1–4.

Morning-report cadence, one-variable rule, flag-don't-silently-resolve — all standing.

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
