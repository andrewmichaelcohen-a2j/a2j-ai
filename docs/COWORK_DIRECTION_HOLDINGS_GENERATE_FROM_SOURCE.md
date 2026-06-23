# Cowork Direction — Holdings Verification v3: Generate-From-Source (raise rigor, recover wording-artifact failures)

**For:** Cowork · **From:** Andy (planning with Claude) · **Date:** 2026-06-23

**Purpose:** The v2 multi-state run failed dominantly at Check C (`FLAG-inaccurate`) for non-CA states, while CA passed 4/6. CA is not legally special, so a near-total non-CA collapse is almost certainly an artifact of *how the non-CA draft holdings were written* and/or a single-model comparison, **not** a real machine-verification ceiling. This direction diagnoses that, then replaces "grade the draft" with "characterize the holding from the actual opinion text, then check it independently."

**This RAISES the bar, it does not lower it.** The threshold to reach `machine-verified` does not move. We are not making cases pass. We are (a) stopping wording-artifact failures from being miscounted as substantive failures, and (b) generating the holding from source rather than confirming a possibly-sloppy draft — which is *more* rigorous, not less. A case with a genuinely wrong holding must still fail exactly as it does today.

> **Execution reminder (unchanged):** API/connector calls run from Andy's **Terminal**, not the Cowork sandbox. Cowork PREPARES the runner and gives Andy exact commands; Andy runs; Cowork INGESTS. A result is only real if a raw output file from a real run exists. State provenance with every "done."

---

## GOVERNING CONSTRAINTS (non-negotiable — read before building)

1. **The passing standard does not change.** `machine-verified` still requires: case exists in the authoritative source (Check A), still good law (Check B), holding corroborated by retrieved opinion text under a real two-model comparison (Check C), and control basis tagged STATED vs. INFERRED (Check D). Do not relax any threshold, do not widen what counts as agreement, do not lower the consensus requirement. If anything, C gets stricter because the holding is now built from the text.

2. **Independence is mandatory — no model may grade its own work.** In generate-from-source, the model that *characterizes* the holding from the opinion text and the model(s) that *check* that characterization against the text MUST be different models. If the same model both generates and verifies, you have rebuilt a single-model pipeline with extra steps — that is a FAIL of this direction, not a pass. Record which model did which step for every case.

3. **The GPT empty-response issue is a prerequisite, not a side quest.** If GPT returns empty on retaliation, then v2's "two-model consensus" was single-model Gemini, and an unknown share of the C-failures may be one conservative model with no second opinion to balance it. Resolve this FIRST (Step 1). A generate-from-source rate computed on a single model is not trustworthy and will be treated as `single-model-preliminary`, never `machine-verified`.

4. **No promotion across the attorney line.** `machine-verified` remains a draft grade BELOW the attorney line. Nothing here promotes machine output to `validated`. Audit sampling still governs whether a category earns reduced attorney review over time.

---

## STEP 1 — Fix the two-model channel FIRST (prerequisite)

Before any re-run, resolve the GPT empty-response issue on non-notice modules so Check C is genuinely two-model.

- Diagnose the empty response: is it token truncation (prompt + opinion text exceeds the window), a formatting/parse failure (model replies but the runner can't extract it), a rate/quota 429, or a content-length cap on the returned JSON?
- Try, in order: (a) trimming the opinion text passed in to the relevant passages rather than the full opinion; (b) rephrasing the C prompt; (c) if GPT still fails, substitute a different second model (e.g., a second Gemini variant or Claude) so there are genuinely two independent models — and **record which two**.
- **Report:** the diagnosed cause, the fix applied, and a 2-case proof that both models now return parseable output on retaliation. Do not proceed to Step 3 until C is real two-model.

---

## STEP 2 — Triage read of the v2 C-failures (diagnose before re-running)

Do NOT re-run yet. First learn the real ratio of *inaccurate-holding* (should fail) to *wording-artifact* (should not). Pull **8–10 of the v2 C=FLAG-inaccurate cases** and for each output, side by side:

- the **draft holding characterization** (what v2 was grading),
- the **specific retrieved opinion passage(s)** it was compared against,
- a **one-line reason** for the mismatch, classified as exactly one of:
  - **(I) INACCURATE** — the draft asserts something the opinion does not hold (draft says X, opinion holds Y / opinion is about an adjacent issue). *Correct failure → attorney re-characterization queue.*
  - **(W) WORDING-ARTIFACT** — the opinion supports the proposition but uses different language, or the draft is broader/narrower than any single passage though the holding is present. *Recoverable by generate-from-source.*
  - **(N) NO-TEXT** — opinion not retrievable / retrieval returned the wrong document. *Infrastructure issue, separate fix.*

**Report the ratio** (how many I vs. W vs. N out of the sample). This number decides scope: if mostly W, generate-from-source should pull the non-CA rate toward CA's. If mostly I, the non-CA drafts genuinely need attorney work and we have an honest finding — do not force them through.

---

## STEP 3 — Build the generate-from-source variant (the rigor upgrade)

Replace "does this pre-written holding match the opinion?" with a generate-then-verify flow. For each case:

1. **Retrieve** the opinion text from the authoritative source (existing A/B checks unchanged).
2. **Generate (Model 1):** from the retrieved opinion text ONLY, characterize the holding relevant to the retaliation element, and extract a **candidate controlling quote** (verbatim span) if one exists. Model 1 does not see the draft holding at this stage — it works from the text, the way the CA pass effectively did.
3. **Verify (Model 2, different model):** independently check Model 1's characterization and candidate quote against the retrieved opinion text. Does the text support the characterization? Is the quote verbatim and on-point? Compare at the level of **legal proposition / element**, not surface wording.
4. **Reconcile against the draft:** compare the source-generated holding to the original v2 draft holding.
   - If source-generated and draft agree on the legal proposition → the draft was right; **C passes** (this recovers W-type cases without lowering the bar — the holding is now corroborated from text by two independent models).
   - If they diverge → the draft was inaccurate; **C fails → attorney re-characterization queue** (this is the I-type case failing correctly). Carry the source-generated characterization into the queue so the attorney is re-characterizing against text, not from scratch.
5. **Check D (control basis):** if Model 1 found a verbatim controlling quote that Model 2 confirms on-point → `control: STATED`. If the proposition is corroborated but no enumerated rule statement exists → `control: INFERRED` (the AZ / *Thomas v. Goudreault* / *Schweiger* pattern).

**Two independent models must agree for C to pass. Same threshold as v2 — the difference is the holding is now built from the source, and graded by a different model than built it.**

---

## STEP 4 — Route the residue into TWO queues, not one

Stop collapsing everything into a single "attorney queue." After Step 3, sort what didn't reach `machine-verified` into:

- **CONFIRM-INFERENCE lane (cheap, delegable):** corroborated holding, `control: INFERRED`, no controlling quote — the AZ pattern. The attorney is confirming an inference the two models already corroborated from text, not re-characterizing. This is the category audit-sampling is designed to graduate toward reduced review. Tag these distinctly.
- **RE-CHARACTERIZE lane (real attorney work):** the I-type cases where the source-generated holding diverged from the draft. These genuinely need a lawyer's judgment. The queue entry carries the opinion cite, the retrieved passage, and the source-generated characterization so the attorney starts from text.

Routing these differently is the point: it concentrates real attorney spend on real interpretive work and keeps the cheap confirmations cheap — without ever promoting machine output across the line.

---

## STEP 5 — Re-run, measure, report (provenance-complete)

Run the generate-from-source variant across the v2 states. **Still run Batch 2** to complete the survey. Then report ONE consolidated answer:

1. **Triage ratio** from Step 2 (I / W / N).
2. **The new multi-state machine-verified rate**, with the CA rate alongside for comparison — and an explicit statement of whether non-CA converged toward CA once holdings were generated from source. (If it did, that confirms the v2 collapse was artifact. If it didn't, that's the honest finding that these holdings need attorney judgment.)
3. **Provenance table:** for every case, which model GENERATED and which model VERIFIED (must differ), environment, raw output file path. A rate without the generate/verify model split per case is treated as not-done.
4. **Queue counts:** how many CONFIRM-INFERENCE vs. RE-CHARACTERIZE.
5. Confirmation that **no threshold was changed** — state the C pass condition you used verbatim and confirm it matches v2's bar.

---

## WHAT WOULD MAKE THIS A FAILED RUN (state if any occurred)

- Same model generated and verified any case → single-model, invalid.
- Any threshold loosened to raise the pass rate → invalid; this direction forbids it.
- C computed on a single model because the GPT issue wasn't resolved → `single-model-preliminary`, not `machine-verified`.
- A rate reported without per-case generate/verify provenance → not-done.

If any of these happened, downgrade and say so. A false "machine-verified" is far more costly than another Terminal run.

---

*Cowork Direction — Holdings Verification v3 (Generate-From-Source) · CJaC · 2026-06-23 · Build the holding from the source, grade it with a different model, change no threshold. Independence + provenance or it isn't machine-verified.*
