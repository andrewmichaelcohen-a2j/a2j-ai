# Test cases

This folder holds **fully fabricated** client fact patterns used to validate the skills in this plugin. They are the regression suite: when a skill changes, re-run it against these cases and confirm the output is still correct.

## Rules

- **Every fact pattern is fabricated.** No real names, dates, locations, amounts, or creditors. This is non-negotiable.
- Each test case pairs a fact pattern with an **attorney-reviewed expected analysis**, so correctness can be checked objectively.
- Cover a range of defense theories. Suggested starting set:
  - **Time-barred debt** — the statute of limitations has expired.
  - **Broken chain of title** — the plaintiff cannot document that it owns the debt.
  - **FDCPA violation** — a defective validation notice or other statutory violation.

## Format (suggested)

Each test case is a markdown file with: a fabricated fact pattern, the jurisdiction, the expected defense theories the skill should identify, and the reviewing attorney plus review date.


---

*Copyright 2026 Andrew M Cohen. Licensed under the [Apache License, Version 2.0](../LICENSE).*