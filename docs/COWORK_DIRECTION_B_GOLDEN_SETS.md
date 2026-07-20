# Cowork Direction B — Golden Sets: the frozen ground truth (build before any self-optimization)

**For:** Cowork · **From:** Andy (planning with Claude) · **Date:** 2026-06-23
**Depends on:** Direction A (autonomy rule). **Required before:** Direction C (self-optimization). **Runs under:** the RED rule — golden-set *answers* are immutable and may only be set/changed by a named attorney.

**Purpose:** The project has zero golden sets today (L4 = not_implemented, 0/51). That is the long pole for everything Andy wants next: you cannot let a system improve itself, or prove it works, without a frozen target of known-correct answers. This direction stands up the first golden sets — attorney-established, versioned, and **read-only to every automated process** — so that (a) we can finally measure whether outputs are *correct* (the apex test), not just internally consistent, and (b) Direction C has a fixed target to optimize against without being able to cheat.

> **The single most important property:** the golden-set answers are GROUND TRUTH and are IMMUTABLE to automation. No runner, optimizer, or agent may create, edit, or delete a golden answer. Only a named attorney establishes them. A self-improving system that can edit its own grader will "improve" by gaming the grader — this rule is what prevents that. (See Direction C.)

---

## PART 0 — VALIDATION-TIER LADDER + ATTORNEY-SCOPE (read first; this reframes what "validated" means)

CJaC's bar for validation stays HIGH. What changes is recognizing that "attorney-validated" is not the only honest validation tier, and that funneling every element to element-by-element attorney sign-off is both unnecessary and fatal to the project's reach. There are **three tiers**, each with a defined, citable basis:

1. **`machine-verified`** — encoded and internally checked (schema/L3, statutory grounding, multi-model consensus, cross-jurisdiction consistency). A draft grade. Basis: defense-in-depth + inter-coder reliability.
2. **`convergence-validated`** *(NEW tier — the attorney-scope refinement)* — the element is corroborated by **N independent authoritative sources converging**: authoritative statutory text + case verification (CourtListener) + independent agency/dataset agreement (e.g. LSC/Temple) + multi-model consensus. When convergence meets an **attorney-set threshold**, the element is validated *without a lawyer re-reading it individually*. Basis: **triangulation** (research methodology) + **convergent validity** (psychometrics) — multiple independent measures of the same construct agreeing is stronger than any one alone.
3. **`attorney-validated`** — a named attorney established or confirmed it. Reserved for: (a) establishing ground truth and the convergence thresholds themselves, and (b) genuinely interpretive / open-textured residue.

**The attorney's role (scope):** validator and ground-truth establisher, NOT line-by-line coder. This mirrors the recognized literature (LCDSS, ScienceDirect 2025: "the human expert shifts from manual coder of rules to validator of machine-generated candidates") and is what makes attorney validation *tractable* via structural isomorphism (each rule maps 1:1 to its source, so units are independently reviewable — Morris/Blawx, OpenFisca).

**Why this is raising the bar, not lowering it:** an element validated by four independent authoritative sources converging under an attorney-set rule, scored against frozen golden truth, is *more* defensible than one lawyer's unaided read — and it scales. The honesty discipline is unchanged: open-textured elements that can't reach convergence stay `attorney-validated` or labeled "structurally checked, not substantively blessed." The convergence threshold for each module/difficulty band is itself golden-tested and attorney-set.

**Critical caveat (keep honest):** multi-model consensus alone is NOT convergence — models share training data and can converge on the same wrong answer (Stanford RegLab). `convergence-validated` REQUIRES agreement across *independent* source types (statute + case + agency-dataset), not just multiple models agreeing. Consensus is one input to convergence, never the whole of it.

---

## PART 1 — WHAT A GOLDEN CASE IS

A golden case is a frozen, attorney-validated unit of ground truth: a realistic legal fact pattern + the correct answer + the authority, against which the pipeline's end-to-end output is scored. Each golden case record contains:

- `id`, `jurisdiction`, `module` (notice / service / retaliation / etc.), `version`.
- `fact_pattern`: the realistic scenario (plain facts a tenant situation would present).
- `question`: what the pipeline must determine (e.g. "Is this pay-or-quit notice valid? If not, why?").
- `correct_answer`: the attorney-established right answer — structured (e.g. `valid: false`, `defect: late_fees_included`, `days_required: 3`, `controlling_authority: CCP §1161(2); Schweiger`).
- `attorney`: named human who established it + date.
- `basis`: the bright-line statute/holding the answer rests on.
- `difficulty`: `bright_line` vs `open_textured` (so scoring can be read separately — see Part 4).
- `immutable: true` and a content hash, so any automated edit is detectable.

**Start where the law is bright-line and already validated**, so the first golden answers are easy to establish with high confidence: CA and TX notice + service. These modules are already L2-complete and attorney-touched. Expand to retaliation (open-textured) only after the bright-line set works end-to-end.

**PARALLEL TASK — find existing golden sets before generating from scratch.** Run this concurrently with candidate generation (it's faster and yields *independent* ground truth Andy didn't author, which is more credible than self-built sets):
- **LSC/Temple eviction dataset** — already a partial external ground truth (CJaC is at ~90% agreement with it); assess whether portions can be adopted as golden cases with attorney confirmation.
- **Academic A2J benchmarks**, **NCSC** (National Center for State Courts) materials, and **legal-aid clinic fact-pattern banks** — survey for reusable, attorney-grade fact patterns with known outcomes.
- For any imported set: record provenance/source, confirm it's appropriately licensed/usable, and still route the *answers* through attorney confirmation before freezing (imported ≠ automatically golden). Report what exists and what's adoptable before generating redundant candidates.

---

## PART 2 — BUILD SEQUENCE (Cowork drafts, attorney freezes)

**Cowork's role is to PREPARE candidate golden cases for attorney sign-off — never to set the answer.** Sequence:

1. **Generate candidate fact patterns** for CA + TX notice and service (target ~15–25 per module to start). Draw from the encoded rules to construct scenarios that exercise the key defects and the valid baseline (e.g. for CA notice: clean valid notice; notice with late fees included → void; 2-day instead of 3-day; defective service variants).
2. **Draft the proposed correct answer + authority for each** — clearly marked DRAFT/UNFROZEN, with the bright-line basis cited, for attorney review. **Full-defect-declaration requirement (added 2026-07-19, per errata-cycle directive Task 5, ratified via `docs/ERRATA_MEMO_v0_3_20260719.docx` §3):** each candidate item must declare every defect class its facts implicate, not only the defect class it was drafted to test — the drafter's note must state which other encoded defect classes were considered and found not to apply, not merely the target defect's analysis.
3. **Route to Andy (named attorney) for establishment.** Andy confirms or corrects each answer. On his sign-off, the case is FROZEN: `immutable: true`, attorney + date recorded, content hash written. **Full-defect-sweep requirement (added 2026-07-19, per errata-cycle directive Task 5, ratified via `docs/ERRATA_MEMO_v0_3_20260719.docx` §3 — root cause: the 2026-07-16 v0.3 freeze session reviewed CA-NOT-C-21/C-22 only through the single defect class they were drafted to test, missing an independently applicable defect [§1946.1(b)/(c) notice-period], later corrected by attorney errata):** every candidate item must be reviewed against **every encoded defect class in the module**, not only the class it was drafted to test. The ratified defect list in the rules file (`notice.notice_defects` and equivalent per-module lists) serves as the sweep checklist — an explicit per-item pass/fail against each defect class is required before freezing, not just against the target defect. **Model outputs may not be consulted during ground-truth review** (ground truth must be independent of what the pipeline would produce, to avoid the loop where scoring simply confirms whatever the model already says).
4. **Split into TRAIN and HELD-OUT** (see Part 3) — Cowork proposes the split; once frozen, the held-out portion is sealed.
5. **Store** under `rules/validation/golden/<module>/` with a manifest listing hashes. Commit so the frozen set is in version control and reproducible.

This is a RED workflow at the establishment step: the *answers* require the attorney. Everything around it (generating candidates, structuring records, computing hashes, wiring the scorer) is GREEN.

---

## PART 3 — TRAIN / HELD-OUT SPLIT (the overfitting guard)

Split every golden set into two sealed portions:

- **TRAIN:** the portion Direction C's optimizer may see and optimize against.
- **HELD-OUT:** a portion the optimizer NEVER sees, used only to confirm that improvements on TRAIN are real and not gaming of specific cases.

Rules:
- The held-out portion is sealed at freeze time; the optimizer has no read access to it. Only the final scoring harness touches held-out, and only to produce a score.
- A change that improves TRAIN but not HELD-OUT is overfitting → rejected (enforced in Direction C).
- Held-out cases are never used to tune anything. If held-out is ever exposed to the optimizer, it is burned and must be replaced with fresh attorney-established cases.

Suggested split: ~70% train / ~30% held-out, but keep enough held-out cases per difficulty band to be meaningful.

---

## PART 4 — THE SCORER (how end-to-end correctness gets measured)

**Standard basis:** this is **eval-driven development** (the lab-standard way LLM systems are improved) and the **NIST AI RMF "Measure"/TEVV** function — outcome testing against frozen ground truth is the apex measure. Internal consistency ≠ correctness; only scoring against known-correct answers proves the system works rather than merely agrees with itself.

Build a scoring harness that runs a golden case end-to-end through the actual pipeline and compares the pipeline's output to the frozen `correct_answer`. Requirements:

- **Scores correctness, not consistency.** This is the apex test the project has been pointing at: does the pipeline produce the *right* answer, not merely a self-consistent one.
- **Reports by difficulty band separately:** bright-line score and open-textured score never blended into one number. We expect (and want) bright-line to score high and open-textured to score lower — blending hides the real picture and would let a high bright-line rate paper over weak interpretive performance.
- **Provenance:** every score run records the pipeline config/version that produced it (ties into Direction C versioning).
- **The scorer is read-only to ground truth.** It reads frozen answers; it never writes them.
- **The attorney line is unaffected.** A high golden-set score raises confidence in `machine-verified`; it does NOT promote anything to `validated`. Crossing that line still requires a named human. Golden-set scoring measures the machine; it does not replace the attorney.

---

## PART 5 — IMMUTABILITY ENFORCEMENT (make cheating detectable)

- Each frozen golden case carries a content hash; the manifest carries the set hash. A pre-run integrity check verifies hashes before any optimization or scoring run; a mismatch halts the run and is reported RED.
- No automated process has write access to `rules/validation/golden/`. If any code path could write there, that is a failed build — flag it.
- Changes to golden answers appear in version control as attorney-authored commits only. An automated commit touching a golden answer is a violation and must be surfaced.

---

## REPORT BACK
1. Candidate counts generated per module (CA/TX notice + service) and the DRAFT answers ready for Andy's establishment.
2. The frozen manifest (once Andy signs off) with hashes, train/held-out split, attorney + dates.
3. The scorer built, with a first end-to-end score on the bright-line set (by difficulty band, with config provenance).
4. Confirmation: golden directory is read-only to automation; integrity check in place; held-out sealed.

## WHAT WOULD MAKE THIS A FAILED BUILD
- Any automated process able to write/edit a golden answer.
- Held-out cases visible to the optimizer (Direction C).
- A blended golden score that hides the bright-line vs open-textured split.
- A golden answer set by anything other than a named attorney.
- Golden-set scoring used to promote output across the `validated` line.

---

*Cowork Direction B — Golden Sets · CJaC · 2026-06-23 · Frozen, attorney-established ground truth, read-only to automation. Train/held-out split. This is the foundation self-optimization stands on — build it first, or Direction C optimizes against nothing.*
