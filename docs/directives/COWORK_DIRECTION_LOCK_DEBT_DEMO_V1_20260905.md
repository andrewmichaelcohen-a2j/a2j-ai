# Cowork Direction — LOCK debt-demo-v1.0 + Methodology & Lift Experiments

**Date:** 2026-09-05 · **From:** Andy (planning with Claude) · **Supersedes:** open-ended content iteration on the demo corpus.
The strategic decision, ratified: the corpus does not lock itself — we lock it. Execution order below.

## Phase LOCK (first; mostly GREEN)

1. **Freeze:** the 19 demo-corpus nodes at their current SHAs. Tag `debt-demo-v1.0`. Record the SHA manifest in the ledger. From this moment, no content edits to v1.0 nodes — all future Stage B findings and improvement candidates route to `POST_V1_BACKLOG.md` (materiality-classified, dangerous-direction flagged, untouched otherwise).
2. **Measurement-of-record:** prepare my smoke-then-full run commands for one final live run against the frozen corpus under the ratified gate (zero undispositioned material findings + per-stage health). This run's JSON is the frozen evidentiary record for v1.0 — it goes in the ledger next to eviction Proof 1.
3. **Counsel queue packaging:** consolidate ALL open GLOSS-FOR-COUNSEL items (round 38's 11 + any added through round 46) into one document — each with the encoded proposition, the authority relied on, the risk posture if wrong, and a confirm/strike/modify checkbox. I will rule on these with Claude in one session; your job is packaging, not resolving.
4. **Census-audit package:** for my scheduled audit session, produce the per-node audit sheet — node content, every citation with source tier and verification status, disposition history, and a sign-off line — ordered for efficient review (federal spine first, then CA, then TX). Estimate my total hours honestly.
5. **Tier promotions:** upon (a) my gloss rulings applied and (b) census audit complete, v1.0 nodes promote per the rules — this produces CJaC's first VALIDATED release. Nothing promotes before both events.

## Phase EXPERIMENT (after LOCK items 1–2; design docs are GREEN, live spend needs my go)

6. **Configuration ablation** — the "how many models" question, answered with data.
   - Ground truth: the 120-finding disposition ledger + all calibration fixtures + the fixed-bug history. Use SHA-preserved pre-round-38 corpus snapshots as the defect-bearing test articles.
   - Configurations (minimum): (a) single model + structured self-critique; (b) single model + different-family adversarial pass; (c) two-model draft/verify; (d) full tri-model consensus; each with grounding enforced, plus one ungrounded arm on whichever config wins, to isolate grounding's contribution.
   - Metrics per configuration: known-real-defect catch rate (against the ledger, materiality-weighted); false-flag rate (alignment-cycle cost); API cost per node; projected human-minutes per node. Use replay/fixtures wherever possible; propose the minimal live-call budget and get my go before spending.
   - Deliverable: `CJAC_METHOD_V1.md` — the evidence-ranked pipeline recipe (what stages earn their cost), the recommended scaling configuration, and the cost curve per validated node. This document, not the debt corpus, is the thing that scales — write it for an external technical reader (a clinic, a lab, a replicating team).
7. **Lift ablation (D-5)** — the market question. CJaC-grounded system vs raw frontier models (each of the three, no rules attached), same five scenarios + a Cowork-drafted expanded scenario set (~15–20, frozen before any arm runs), scored against the v1.0 frozen content as ground truth, abstention-credit scoring per house rules. Pre-register the design (arms, items, scoring) in the repo before execution; propose budget; my go required for live spend. Deliverable: the lift number with dual-reported basis — the headline input to the new messaging.

## Constraints

One-variable rule continues. No live runs by anyone but me; smoke-first always. v1.0 content is immutable — experiment findings about v1.0 content go to the backlog, not into edits. Calibration must be green before any experiment code runs live. All experiment designs pre-registered in-repo before execution; results dual-reported regardless of outcome. Budget caps on every live phase; per-run estimates in advance.

## Reporting

Morning-report cadence per Direction A. LOCK items 1, 3, 4 same-session; item 2 command package when ready; experiment design docs before any execution. Flag conflicts rather than silently resolving — including anything in this directive that collides with repo reality.

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
