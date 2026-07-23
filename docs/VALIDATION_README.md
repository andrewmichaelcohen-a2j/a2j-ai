# Validated Results — A Guide to This Repository's Evidence

*Written for law professors, legal-aid staff, and anyone else checking our work — not just engineers. If you came here from the two-pager's promise of "full methodology, scores, and correction records," this page is the map.*

## The short version

We publish everything: what we tested, what we got right, what we got wrong, and how errors got fixed — including errors in our own ground truth, not just in the model outputs being measured against it. Nothing is deleted or quietly rewritten; corrections are dated and layered on top of the original record.

## The one number that matters, reported honestly

The v0.3 held-out benchmark — a one-time, never-to-be-repeated test against a golden set the system had never seen — scored:

**23/26 = 88.5% as originally scored, or 25/26 = 96.2% after a signed attorney correction to two ground-truth answers that were themselves wrong.**

We report both numbers, every time, everywhere this result appears. We do not pick the flattering one. The two items that moved were the golden set's own errors (Civil Code §1946.1(b)/*Stancil* is independent of the AB 1482 just-cause requirement — the original ground truth conflated them), corrected by a licensed attorney's signed errata memo, not by us deciding our own model was right.

## Where everything lives

**Start here if you want the numbers:**
- [`VALIDATION_METRICS_LEDGER.md`](VALIDATION_METRICS_LEDGER.md) — the full scoring history for every module and jurisdiction, including the v0.3 held-out result, the dev-set regression gate history, and the citation corrections made at freeze.
- [`../rules/validation/scorer/output/ca_notice_score_2026-07-19_held-out.json`](../rules/validation/scorer/output/ca_notice_score_2026-07-19_held-out.json) — the raw scorer output for the v0.3 held-out run: per-item results, model outputs, rules-file SHA256, and golden-set SHA256, so the result can be checked against the exact file versions it was run against.

**Start here if you want to see what went wrong and how it was fixed:**
- [`AUTOPSY_v0_3_MISSES_20260719.md`](AUTOPSY_v0_3_MISSES_20260719.md) — the miss-by-miss analysis of the three v0.3 held-out items that didn't score clean: which were genuine rule gaps versus golden-set ground-truth errors, and how each was classified.
- [`ERRATA_MEMO_v0_3_20260719.docx`](ERRATA_MEMO_v0_3_20260719.docx) *(authoritative — signed)* / [`.md`](ERRATA_MEMO_v0_3_20260719.md) *(reading copy)* — the signed correction instrument for the two golden-set ground-truth errors found by the autopsy.
- [`RULE_PROPOSAL_1946_2a_ATTACHMENT_20260719.md`](RULE_PROPOSAL_1946_2a_ATTACHMENT_20260719.md) and [`WIRING_DETERMINATION_1946_2e_20260719.md`](WIRING_DETERMINATION_1946_2e_20260719.md) — the ratified pair that turned the one genuine rule gap the autopsy found (the §1946.2(a) attachment threshold) into an actual rules-file change, reviewed and ratified before it was applied.

**Start here if you want the methodology itself:**
- [`VALIDATION_PHILOSOPHY.md`](VALIDATION_PHILOSOPHY.md) — how automation and human review divide the work, and why nothing automated ever crosses the line into "attorney-validated."
- [`STATUS_LABELS.md`](STATUS_LABELS.md) — the status ladder every file is labeled against.

## A first-time visitor's actual path

Starting from the README, a reader following the "full methodology, scores, and correction records" claim clicks through: `README.md` → **this page** → `VALIDATION_METRICS_LEDGER.md` for the numbers, or `AUTOPSY_v0_3_MISSES_20260719.md` → `ERRATA_MEMO_v0_3_20260719.docx` for how a specific correction was made, start to finish, with the signed instrument itself one click away. No step requires already knowing repository internals or file-naming conventions — every link above is a plain path from this page.

## Two things every reader should know before reading a number

1. **Dual-reporting on v0.3.** Any place a v0.3 score appears, both the as-scored and post-errata numbers are given together (23/26 / 25/26). If you see a single number cited for v0.3 without both, flag it — that's a documentation bug, not an intended simplification.
2. **What "multi-model consensus" means here.** One model drafts or reviews; a *second, independent* model must independently agree before a result counts as consensus-validated. Tri-model consensus is on the roadmap, not yet in use. Single-model results are always labeled as such, not folded into consensus numbers.

---

*Created 2026-07-23 (Direction D directive, Task 2 — repository discoverability pass). If a link above breaks or a file moves, that's a bug — [open an issue or contact andrewmichaelcohen@gmail.com](../README.md#license--contact).*
