# Run 3: plain-language versions, re-checked (Nov 21, 2026)

Purpose: the delta test pastes each item's text, so the text should be the final plain wording. Claude rewrote every `answer` in plain language. The Checker (OpenAI, a different vendor) re-reads each plain answer against the saved sources. An item keeps the Source-read label only if every claim is still supported.

Files
- `items.json`: the 15 items with plain `answer`; the original wording is kept in `answer_statute_close`. D-06-SEEDED and D-11-SEEDED are unchanged first-draft controls and should still be caught.
- `results/`: written by the Checker.

Reading level (rough Flesch-Kincaid grade, a heuristic that statute citations inflate): average 15.5 before, 11.0 after. The earlier target from the DC report is grades 3 to 6. Statute-based rule statements will not reach that; the reader-facing layer (short answer, what to do) will need its own wording. Not done yet.

Commands (copy each line exactly)
1. `python3 ~/Developer/a2j-ai/playbooks/california-debt/run1/checker.py --run --dir ~/Developer/a2j-ai/playbooks/california-debt/run3 --budget 25`  (about $3.92 expected)
2. `open ~/Developer/a2j-ai/playbooks/california-debt/run3/results/RESULTS.md`
3. For a second agreeing run: `mkdir -p ~/Developer/a2j-ai/playbooks/california-debt/run3b && cp ~/Developer/a2j-ai/playbooks/california-debt/run3/items.json ~/Developer/a2j-ai/playbooks/california-debt/run3b/items.json` then `python3 ~/Developer/a2j-ai/playbooks/california-debt/run1/checker.py --run --dir ~/Developer/a2j-ai/playbooks/california-debt/run3b --budget 25`

Pass criteria: both seeded controls caught; each plain item has all claims supported and no flags; any item that is not Source-read goes back to the plain-language editor (cap: two rounds, then Not yet checked).

## Run 3 result and Run 3b
Run 3: 11 of 15 items Source-read; D-01, D-09, D-13, D-14 not. Both seeded controls caught. The plain-language edit had introduced real meaning drift, which the Checker caught: (1) "plaintiff can ask the court to enter default" in place of the statute's "default will be entered upon application by the plaintiff" (D-01, D-14; the same drift sat in D-05, which passed, and was fixed too); (2) "additional language" for "additional foreign language" (D-01); (3) "in writing" not attached to the request for the original creditor's name in the 1692g(b) text (D-13). D-09's flag was a sentence about the whole saved source set, which the Checker cannot verify; moved to `scope_note`.
Run 3b (`run3b/items.json`) applies those fixes to D-01, D-05, D-09, D-13, D-14. Run all 17 for a second run of the unchanged items; then rerun only the five changed items: `--only D-01,D-05,D-09,D-13,D-14` in `run3c`.
