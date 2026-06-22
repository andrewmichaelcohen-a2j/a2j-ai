# Cowork Direction — Holdings-Verification Layer (AI-maximal, audit-gated)

**For:** Cowork · **From:** Andy (planning with Claude) · **Date:** 2026-06-21

**Purpose:** Build the automated holdings-verification layer that lets AI do the *checkable* case-law verification — against an authoritative source, not model memory — so attorney spend collapses onto the genuinely-interpretive residue plus an audit sample. This is the highest-leverage build remaining: it converts holdings from the dominant cost line into a manageable one.

**Governing principle (non-negotiable):** Leverage AI as far as it can go *before* spending on attorneys — bounded by zero loss of validation, proof-of-validation, or repeatability. The machine may be **aggressive in attempting**, but it may **never promote its own output to `validated`**. `machine-verified` is a draft grade *below* the attorney line. The line between machine and attorney is **found by testing and moved by evidence**, not assumed.

> Execution reminder (unchanged): API/connector calls run from Andy's **Terminal**, not the Cowork sandbox. Cowork PREPARES the runner + gives Andy exact commands; Andy runs; Cowork INGESTS. Provenance rule still applies: a result is only real if a raw output file from a real run exists; state provenance with every "done."

---

## STEP 0 — Verify what authoritative source the runner can actually reach (do this FIRST)

Do not assume any specific legal database is wired in. Before building, determine — empirically, from Andy's Terminal environment — which authoritative case-law source(s) the runner can actually call for **US state case law**:
- **CourtListener API** (free, public; has a **citator** showing subsequent treatment — the good-law signal; near-real-time). Check whether it's reachable and whether it needs an API token.
- **Legal Data Hunter** `resolve_reference` / `get_document` (resolves a citation to an exact document; returns nothing rather than guess — a good hallucination filter). Confirm its US-state-case coverage empirically; it may skew international.
- **Google Scholar / Justia / Casetext-style** open sources as fallback for existence + opinion text.

Report which source(s) resolve US state cases reliably, what each returns (existence? citation? subsequent-treatment/citator? full opinion text?), and any auth needed. **The runner is built to whatever actually resolves — not to an assumed tool.** If the citator (treatment) data isn't reachable from any free source, say so plainly: currency-checking then partly falls back to multi-model + text and gets a lower trust grade until a real citator is wired in. Do not fake a currency check.

---

## STEP 1 — Build the holdings-verification runner

For every candidate holding/case produced by the holdings draft step, the runner performs these checks and records the **basis/evidence** for each (not just a yes/no):

**Check A — Existence + citation correctness.**
Resolve the citation against the authoritative source from Step 0. Resolves to exactly one real case with matching cite → `exists: true`. Fails to resolve / ambiguous → `exists: FLAG` (likely hallucinated) — never asserted, routes to human.

**Check B — Currency ("still good law").**
Pull subsequent treatment (citator) for the case. No negative treatment → `currency: OK-machine` (record the source/as-of date). Any overruled/abrogated/superseded/"distinguished-into-oblivion" signal → `currency: NEGATIVE-FLAG` → routes to human. If no citator source is reachable (per Step 0), mark `currency: UNVERIFIED-no-citator` — explicitly NOT OK, queued until a citator exists.

**Check C — Holding characterization accuracy.**
Both models independently state what the case held on the point; the runner compares them to **each other and to the actual opinion text retrieved from the source** (not model memory). Agreement + text support → `holding: corroborated`. Disagreement, or characterization unsupported by retrieved text → `holding: FLAG` → human.

**Check D — Control determination, classified by basis (the key one).**
Does the case control the question the rule turns on? The runner must classify and capture evidence:
- `control: STATED` — the opinion (or binding authority) states the controlling relationship; **capture the supporting quote + pin cite.** This is verification.
- `control: INFERRED` — no court squarely addressed this question; control would have to be analogized or predicted. **No quote available.** This is prediction, not verification.
Do not let the model assert INFERRED control as if STATED. The honesty of this layer lives in this distinction — the model must show the quote for STATED, or mark INFERRED.

**Disposition (auto):**
- `machine-verified` = exists ✓ + citation ✓ + currency OK ✓ + holding corroborated ✓ + control STATED-with-quote ✓.
- `needs-attorney` = any check FLAG/NEGATIVE, currency UNVERIFIED, control INFERRED, or any interpretive residue.
Every disposition stores its **basis tags and evidence** (the resolving record, the citator result + as-of date, the holding text support, the control quote-or-"none") so the audit can measure reliability per category.

**Labeling discipline:** `machine-verified` is a **draft grade below the attorney line.** Nothing here is `validated`. A category becomes eligible for `validated` only when (a) an attorney clears the item, or (b) that category's audit (Step 3) has earned it.

---

## STEP 2 — Run it (Terminal), test-first

Per standing practice:
1. **Single-state test** (e.g., CA — case-heavy, good stress test), ~$0.10–0.25. Confirm the authoritative source resolves real cases, the citator returns treatment, and both models return holdings. Inspect a few dispositions by hand: do the STATED-control quotes actually say what's claimed? Is any "exists" a hallucination that slipped through?
2. **Full run** across the consensus-elements states only (the 33–34 with genuine two-model elements consensus; do NOT run holdings on the elements-L7 or single-model states — their elements disputes come first).
3. Raw output file to a **uniquely-named path** (include state-count + date + a UUID/suffix — last time an 8-state run overwrote the 51-state raw file; don't repeat that). Provenance: record models, source(s) used, environment, file path.

---

## STEP 3 — The audit harness (this is what makes AI-leverage honest)

The runner's output is not trusted on faith — it is **measured.** Build the audit step so Andy (or an attorney) can:
1. Pull a **random sample within each basis category** (`exists`, `currency OK`, `holding corroborated`, `control STATED`) — e.g., N per category per batch.
2. For each sampled item, a human checks **two things**: was the machine's *determination* right, and was its *basis self-classification* right (e.g., is a `control: STATED` actually stated, with the quote really supporting it)?
3. Record per-category accuracy in the ledger — **same discipline as the L2 metrics.** This is the proof-of-validation for the machine layer.

**The audit moves the line:**
- Category audits clean (high accuracy) → it stays machine-verified; the audit record is the documented proof. Over time, a proven category can be promoted toward `validated`-eligible on machine + audit basis.
- Category audits weak → it routes to humans, threshold tightens, or the check is redesigned. That's a finding, not a failure.
This is how we "take real risk now without excessive downstream risk": broad machine attempt, measured trust, promotion only on evidence. Worst case is "machine over-claimed, audit caught it, those route to humans" — a tuning cost, never a corrupted validated corpus.

---

## STEP 4 — Ledger + reporting

Append a holdings-verification section to the metrics ledger with:
- Per-state and total counts by disposition (machine-verified vs. needs-attorney) and by basis tag.
- The **machine-verified rate** — the headline leverage number (how much the attorney load shrank).
- The **audit results per category** (sampled N, accuracy) — the proof the machine layer can be trusted.
- Provenance (source(s) used, models, file path, as-of dates for currency).
- Honest gaps: any `currency: UNVERIFIED-no-citator` count, any source-coverage limitations from Step 0.

Report to Andy: the machine-verified rate, the audit accuracy per category, the size of the residual attorney queue, and any honesty caveats (esp. if no citator was reachable).

---

## What this is NOT allowed to do (guardrails)

- Do **not** mark anything `validated` on machine output alone. `machine-verified` is the ceiling for the machine.
- Do **not** assert a case exists, is current, or controls without the authoritative-source evidence recorded. No model-memory assertions.
- Do **not** classify INFERRED control as STATED. If there's no quote, it's INFERRED, full stop.
- Do **not** fake a currency check if no citator is reachable — mark it UNVERIFIED and queue it.
- Do **not** overwrite raw output files — unique paths always.

---

## Sequence

Holdings-verification runs on the **elements-consensus states only**. The elements-L7 states (AK, AL, CT, HI, KS, MI, ND, NJ, NM, NV, NY, OK, SC, VT, WV) and single-model states (LA, CO) need their elements disputes resolved first. Best-practices layer comes after holdings. Module 6 (other defenses) replicates this whole pattern once retaliation proves the full cycle end-to-end.

**Commits:** Andy handles commits + GitHub verification. Prepare files, list changes, don't assume a commit happened. Do not commit this direction doc.

---

## One-line summary for Cowork

**Verify case law against an authoritative source (existence, citation, currency, holding-text, and control-IF-stated-with-quote); auto-disposition to machine-verified vs. needs-attorney; record the basis evidence; and build the per-category audit that measures where the machine can be trusted — because the machine attempts aggressively but never promotes itself to validated.**

---

*Cowork Direction — Holdings-Verification Layer · CJaC · 2026-06-21 · Authoritative source not model memory; STATED-with-quote vs. INFERRED; machine-verified is a draft below the attorney line; the audit moves the line.*
