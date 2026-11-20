# California debt playbook: start here

*Front door for people and for Claude sessions. Last updated November 19, 2026 (evening). Keep this file short; link out instead of adding detail.*

## What this is

An open, extensible civil-justice playbook. The first slice is **"Served with a collection lawsuit in California: the first 30 days."** It is written for a person who cannot afford a lawyer, and it is also meant to be usable by legal aid staff and checkable by attorneys.

North star: reduce the access-to-justice gap by putting free, accurate, honestly labeled legal help in front of people who need it.

This is general legal information, not legal advice. No attorney has reviewed any item yet, so nothing is labeled Attested.

## Where things stand (November 19, 2026, late evening)

- A 15-item prototype exists (items D-01 to D-15). It is kept privately for now.
- Six AI check runs happened on November 19 (Run 1, 2a, 2b, 2c, 2d, 2e; the Checker is OpenAI, a different vendor from the drafter). Both planted errors were caught every time.
- Rule statements (not the plain-language wording, and not the practical guidance) matched saved source text in two agreeing runs for 7 items: D-02, D-03, D-08, D-10, D-11, D-12, D-14. Five more passed one run (D-01, D-04, D-06, D-07, D-09). D-05 and D-13 still carry small flags. D-15 is a reference check, held until a person spot-checks two web pages.
- Two California statutes change on January 1, 2027: section 415.20 (service by mail) and section 473 (relief from default). Both new versions are saved in `sources/`.
- AI spend so far: about $5.98 of the $100 cap (ledger: `run1/spend-log.tsv`).
- For the run-by-run detail and the next steps, read the newest file in `sessions/`. Run folders: `run1`, `run2`, `run2b`, `run2c`, `run2d`, `run2e`, `run2f` (prepared, not yet run).

## How the work is labeled

- A four-band assurance framework (bands 1 and 2 are the statutory and rule text that can be looked up and quoted; see the framework spec for all four).
- Four strength labels: **Source-read**, **Lawyers differ**, **Not yet checked**, **Attested**.
- Every item that states law cites a source read in full, with the date it was read. Nothing is stated from memory.
- Open question: how these four labels map onto the repo's status ladder (DRAFT, AUTOMATED-CHECKS-PASSED, UNDER REVIEW, VALIDATED, CERTIFIED). Default: the ladder is the backbone and the labels sit on top.

## Rules for any session working here

1. Read the law from a retrieved source, not from memory. If a source cannot be retrieved, mark the item Not yet checked.
2. Never write advice aimed at a specific person. Keep real people's facts out of this folder.
3. Estimate cost before any AI run and report spend after. The pilot cap is $100.
4. Log every AI step in a TSV decision log (ts, phase, decision, why, evidence, result).
5. Do not change `rules/` or the old validation pipeline unless asked. Do not rewrite `docs/`.
6. Andy is the named owner and initial reviewer. Anything that needs a legal judgment call goes to him.
7. Private strategy, messaging drafts and funding material are not kept in this repo. If a task needs something that is not here, ask.
8. Start of every session: read the newest file in `sessions/`, then tell Andy in five lines or fewer where things stand and what is next. End of every working day (or when Andy says "wrap up"): write a new dated file in `sessions/` with where things stand, what happened, decisions made, next steps and watch-outs. Keep it free of keys and private strategy.

## The pilot plan, in short

Single-job agents, run in Claude: Scout (finds sources), Drafter (writes cited answers), Checker (reads each source in full and assigns the strength label; runs on OpenAI), Red-team (finds errors; cannot fix), Plain-language editor. Andy reviews, then a delta test compares the playbook against asking an AI directly. Revision cap: two rounds, then the item is parked as Not yet checked.

- Run 0: design step, awaiting Andy's review.
- Run 1: seeded-error check.
- Run 2: clear the open flags.
- Run 3: extend with up to five new items (list not yet confirmed).

## Older work in this repo

`rules/`, `docs/` and `review/` hold the earlier codified-rules and validation work on eviction and consumer debt. It answers a different question (does codifying rules beat asking an AI directly) and is historical context for this playbook. Its methods are still useful: frozen test items, paired comparison, and logging errors openly.
