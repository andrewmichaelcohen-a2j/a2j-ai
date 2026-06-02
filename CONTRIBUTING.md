# Contributing

Thank you for your interest in contributing to A2J Claude Legal Plugins. This project builds shared, reusable legal-aid infrastructure. The guidelines below keep the work correct, portable, and safe.

## Rule zero: no real client data, ever

**Nothing identifying about a real person belongs in this repository.** All examples, fact patterns, and test cases must be fully fabricated. If you adapt from a real matter, change every identifying detail — names, dates, locations, dollar amounts, employer and creditor names. When in doubt, leave it out.

## This software assists; it does not practice law

Every skill must be clear that it assists a user or attorney rather than providing legal advice or practicing law. Each skill states what it does and what it explicitly will not do. Outputs are intended to be reviewed by a supervising attorney before reaching a client.

## Portability principles

These choices keep skills valuable regardless of which AI model, platform, or jurisdiction runs them:

1. **Separate logic from jurisdiction data.** Keep procedural logic in the skill; keep state-specific facts, citations, and forms in the `jurisdictions/` folder. Porting to a new jurisdiction should be a data change, not a rewrite.
2. **Write outputs to a structured schema.** Define the sections and fields every output should contain, so results are consumable regardless of which AI produced them.
3. **Require citations to authoritative sources.** Every legal conclusion cites a statute, regulation, rule, or case. Citations make outputs verifiable and auditable.
4. **Avoid platform-specific features in skill content.** Write skills as protocols a competent paralegal could follow. If a human can follow it, any capable AI can.
5. **Maintain a test set with expected outputs.** Each skill has fabricated fact patterns in `test-cases/` with attorney-reviewed expected analyses. This is the regression suite.
6. **Version skills like legal forms.** Use semantic versioning. Record the last-reviewed date, jurisdictions covered, and supervising attorney in the header of each `SKILL.md`.
7. **Document scope and out-of-scope.** Every skill states its boundaries explicitly. The out-of-scope statement protects users from misuse and harm.

## How to suggest a change

1. Open an issue describing the problem or proposed skill.
2. For substantive legal content, identify the supervising attorney who has reviewed it.
3. Submit changes as a pull request referencing the issue.
4. Skills affecting legal analysis require attorney review before merge.

## Versioning

- `v0.x` means early and changeable.
- `v1.0` means stable and validated for the listed jurisdictions.
- Bump the version and update the last-reviewed date whenever legal content changes.


---

*Copyright 2026 Andrew M Cohen. Licensed under the [Apache License, Version 2.0](LICENSE).*