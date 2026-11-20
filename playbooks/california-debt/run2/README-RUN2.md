# Run 2: clear what Run 1 found

Status: set up November 19, 2026. Not yet run.
Owner and initial reviewer: Andy. Run 1 results are kept as they were in `../run1/results/`.

## What Run 1 showed

- The Checker caught both planted errors (D-06-SEEDED and D-11-SEEDED). It also found real wording problems in unplanted items.
- No item reached Source-read (59 flags across 15 items). Two causes:
  1. Source gaps: some sources I had saved were not mapped to the items that need them.
  2. Item design: each item mixes legal rules with practical instructions ("get help now", "keep copies"). No statute supports an instruction.

## Step 2a: re-check with the source mapping fixed (about $1)

`run2/items.json` is Run 1's items with the source mapping corrected. The wording is unchanged on purpose.
Changes: D-02, D-04 (add CCP 12, 412.20), D-03 (add CCP 135, 12b, Gov. Code 6700), D-06, D-08 (add CCP 360, 431.30), D-11 (add CCP 337), D-13 (add 15 U.S.C. 1692g, Civ. Code 1788.17), D-14 (add CCP 85, 431.30, 473).
Purpose: separate the flags that were source gaps from the flags that need rewriting. This is a diagnostic, not a pass.

Command (from any folder):

    python3 ~/Developer/a2j-ai/playbooks/california-debt/run1/checker.py --run --dir ~/Developer/a2j-ai/playbooks/california-debt/run2

## Step 2a result (run November 19, 2026, about $0.84)

Fixing the source mapping raised the supported claims a little (D-02 2 to 3 of 4, D-03 1 to 3 of 7, D-04 1 to 4 of 11, D-13 0 to 3 of 8) but left the flags at 59. Flag types barely moved: gap 18 to 19, overbroad 14 to 13, advice-like 13 to 13, harm risk 11 to 11. So the flags are mostly a wording and design problem. The Checker also gives slightly different claim counts between runs (D-01 had 7 claims, then 6), so one run is a signal, not a verdict. Plan: a Source-read label needs two agreeing runs.
New real finding in 2a: D-13 presents "the debt having been with a different company first" as a coverage test for California's parallel law, with no support. Rewritten in 2b.

## Step 2b: rewrite, then re-check

`run2b/items.json` holds the rewrite: `answer` is rule statements only, written to stay inside the saved sources. `guidance_lines` and `claims_needing_a_source` are stored in the same file but are not sent to the Checker. The two seeded controls are unchanged. The rewrite is a drafter's pass, written in statute-close wording; a plain-language edit comes after it passes, then gets re-checked.

Command:

    python3 ~/Developer/a2j-ai/playbooks/california-debt/run1/checker.py --run --dir ~/Developer/a2j-ai/playbooks/california-debt/run2b

Pass criteria for 2b: both seeded controls still caught; any item with all claims supported and no flags is a Source-read candidate and is run a second time before it earns the label.

## How each kind of line is handled


Each item is split into three kinds of line. Each kind gets the check that fits it.

| Kind of line | Example | Automated check | Label it can earn |
| --- | --- | --- | --- |
| Rule | "General limit is 4 years for a written contract." | Checker matches each statement to saved source text; code verifies quotes word for word | Source-read |
| Guidance | "Talk to a lawyer before signing." | AI checks harm direction and consistency with the rules; no source can support it | Attested by the named reviewer |
| Reference | form PLD-050, LawHelpCA, a phone number | AI looks the name, form number or link up on the official page when the playbook is built | Source-read if it matches the official page |

## Checks the pipeline should run on every item (build status)

| Check | Status |
| --- | --- |
| Claim-by-claim match to saved source (different vendor from the drafter) | Built (Checker) |
| Quotes verified word for word in code | Built |
| Deadline arithmetic in tested code, rule version chosen by service date | Built (calculator) |
| Date-change flags (rules that change January 1, 2027) | Built (Checker flags them) |
| Reference check against official pages (forms, links, organizations) | To build |
| Consistency across items (for example D-08 vs D-09 vs D-11 on the four-year period) | To build |
| Red-team pass (a second model tries to break the item) | Planned |
| Plain-language edit that must not change meaning (checked by the Checker again) | Planned |

## Still missing as saved source text

- Judicial Council forms SUM-100, PLD-050, FW-001. The official pages could not be saved word for word through my tools, so claims about them stay Not yet checked. Fix: save the three PDFs into `playbooks/california-debt/sources/forms/` (instructions to Andy in chat) and I will extract the text.
- Civil Code 1788.50 to 1788.66 (debt buyer act), the Rosenthal Act sections, and Regulation F.
- Resource directories (D-15): needs the reference check, not a statute.

## Reminder on what an AI check means

It shows where a draft is weak or unsupported. It does not show the law is right, and it is not attorney review.

## Run 2c, 2d, 2e results (November 19, 2026; $5.98 spent in total)

- 2c (about $1.06): clean D-03, D-09, D-10, D-15; the rest had 1 to 4 flags, mostly omitted statute parts.
- 2d (about $1.24): after adding the omitted text and narrowing scopes, clean D-02, D-03, D-05, D-08, D-10, D-11, D-12 (date-change note only), D-14, D-15.
- 2e (about $1.20): fixes for six 2d flags. Clean D-01, D-02, D-03, D-04 (date-change note only), D-06, D-07, D-08, D-09, D-10, D-11, D-12 (date-change note only), D-14, D-15. Flagged: D-05 (omitted the SUM-100 "copy served on the plaintiff" sentence), D-13 ("a copy of a judgment" omitted "against the consumer").
- Two agreeing runs on the same text: D-02, D-03, D-08, D-10, D-11, D-12, D-14 (D-15 also, but held for a human spot-check). D-09 shows the variation: clean, flagged, clean.
- Both planted errors (D-06-SEEDED, D-11-SEEDED) were caught in every run.
- 2f (prepared): D-05 and D-13 fixed; run D-01, D-04, D-05, D-06, D-07, D-09, D-13 for a same-text second run:

      python3 ~/Developer/a2j-ai/playbooks/california-debt/run1/checker.py --run --dir ~/Developer/a2j-ai/playbooks/california-debt/run2f --only D-01,D-04,D-05,D-06,D-07,D-09,D-13
