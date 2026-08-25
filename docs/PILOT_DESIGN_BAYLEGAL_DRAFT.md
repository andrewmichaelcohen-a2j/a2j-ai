# DRAFT — PRELIMINARY — Deployment Pilot Design: CJaC × Bay Area Legal Aid

**Status:** PRELIMINARY DRAFT for discussion only — not proposed to BayLegal, not approved by anyone, subject to complete revision. Prepared 2026-07-24.
**Purpose of the pilot:** empirically test the *delivery* links of CJaC's impact chain (Open Questions #2) in a mediated setting: does validated, encoded law in the hands of legal-aid staff measurably improve the speed and accuracy of eviction-notice triage — and downstream, does it move client action?

---

## 1. What is being piloted

The CA eviction-notice module (rules version current at pilot start, with its validation record), deployed as an AI-assisted triage aid for housing-unit intake staff and volunteers. Staff describe or paste the facts of an intake (notice type, dates, amounts, service method, tenancy details — no client identifiers); the tool applies the validated rules and returns: (a) defects identified with statutory/case authority; (b) facts still needed (completeness checklist); (c) deterministic next-step information (e.g., response deadlines) — clearly labeled as legal information for staff use, not client-facing advice.

**Explicitly out of scope for this pilot:** any client-facing automated output; any advice; any case-specific determination not reviewed by staff; any practice area beyond CA notice.

## 2. Design — three phases, each gated

**Phase 0 — Shadow mode (target 4–6 weeks).** The tool runs *alongside* normal intake with no influence on case handling. Staff (or a designated reviewer) run completed intakes through the tool after the fact. Measures: agreement rate between tool and staff determinations; every disagreement adjudicated by a supervising attorney and classified (tool wrong / staff wrong / facts ambiguous) — the same both-directions discipline as our validation cycles, now with real fact patterns. Shadow-mode disagreements feed the project's review queue as real-world test candidates (with all identifiers stripped; see §4).

**Phase 1 — Assisted mode (gated on Phase 0 results + BayLegal sign-off).** Staff use the tool live during triage; a supervising attorney reviews outputs per existing supervision practice. Measures: triage time per intake vs. baseline; defect-spot rate vs. historical baseline; staff-reported usability and trust; error reports.

**Phase 2 — Scope extension (gated on Phase 1 + mutual agreement).** Additional module (service of notice), additional intake channels, or additional measurement of client outcomes — only with fresh review.

## 3. Endpoints (pre-registered before Phase 0 begins)

- **Primary:** (1) defect-spot rate: defects correctly identified by tool-assisted review vs. staff-only baseline (shadow mode gives the paired comparison); (2) triage time per intake (Phase 1 vs. baseline).
- **Secondary:** (3) disagreement adjudication distribution (tool-wrong vs. staff-wrong vs. ambiguous — both-directions error data from real facts); (4) answer-filing rate among tenants whose intakes were tool-assisted, if BayLegal already tracks it (no new client data collection created for this); (5) staff confidence/usability survey; (6) count of rule gaps or errors surfaced (each one is validation value regardless of other results).
- **Pre-registered success criteria:** defined with BayLegal before launch — e.g., defect-spot parity-or-better with meaningful triage-time reduction, and a tool-wrong rate below an agreed threshold.
- **Pre-registered stop criteria:** any tool-wrong determination that would have materially harmed a client's position triggers immediate pause and review; a tool-wrong rate above threshold in shadow mode stops progression to Phase 1. *(Kill criteria are stated before the pilot starts, per project discipline.)*

## 4. Governance, ethics, and data — the non-negotiables

1. **Board-conflict hygiene:** the proposer is a BayLegal board member. The pilot proposal goes to the Executive Director and program staff for evaluation on the merits; the proposer takes no part in any board consideration of it, and the organization's decision processes run without board-side advocacy. This should be documented at proposal time.
2. **Professional responsibility:** all client-facing judgments remain with BayLegal staff under existing attorney supervision; the tool is a research/triage aid. BayLegal's own professional-responsibility review governs; CJaC provides the tool's validation record and limitations doc (including `OPEN_QUESTIONS_AND_LIMITATIONS.md`) as inputs.
3. **Client data:** no client PII enters the CJaC repository or any model prompt beyond what BayLegal's own AI-use policies permit; intake facts used for tool queries are de-identified; shadow-mode disagreement records are stripped to bare fact patterns before entering the project queue. Data-handling terms in writing before Phase 0.
4. **Consent & transparency:** handled per BayLegal policy; nothing in the pilot changes what clients are told or how they are counseled.
5. **Costs:** borne by the project (model usage is negligible); no BayLegal funds requested; staff time is the organization's real contribution and is measured, not assumed.

## 5. Sequencing and prerequisites

Not before: (a) v0.4 validation cycle complete (so the deployed rules carry a current, clean validation record); (b) Direction E Tier 1 results in hand (so we can honestly describe lower-bound behavior to BayLegal); (c) the legal-ethics review flagged in Open Questions #7, at least in initial form. Realistic earliest start: [TBD — likely 4–8 weeks out].

## 6. What each party gets

BayLegal: a measured answer to whether AI-assisted triage helps its housing practice, at no cost, under its own controls, with the option to stop at any gate. CJaC: the first real-world data on the delivery chain — real fact patterns, real disagreements adjudicated both directions, and the pilot report that every funder, law school, and platform will ask for.

## 7. Open design questions (for the BayLegal conversation)

Which intake channel(s) to shadow; what the historical defect-spot baseline actually is and whether it's measurable retrospectively; who adjudicates disagreements; whether answer-filing tracking exists at usable granularity; volume expectations (n needed for the primary endpoints to mean anything — to be computed once channel volume is known); union/staff consultation norms for workflow studies.

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
