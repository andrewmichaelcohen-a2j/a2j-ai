# Contributing

Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.

All contributions are welcome. The most valuable contributions are attorney validations — but there are many ways to help.

---

## Ways to contribute

### 1. Validate a state file (highest value)
If you are a licensed tenant attorney, review a DRAFT file and advance it to VALIDATED. See [REVIEWER_CHECKLIST.md](REVIEWER_CHECKLIST.md). Priority: CA, TX, NY, FL, IL, GA, OH, PA, NC, MI.

### 2. Add or improve golden set test cases
For any state (especially priority states), create fabricated test scenarios with known-correct answers. Format: `validation/golden_sets/{state_code}_golden_set.json`. Test cases must use entirely fabricated facts — no real client information.

### 3. Correct a statutory error
If you find an error in a DRAFT file (wrong notice period, missing defect, incorrect statute citation), open an issue or submit a PR. Label it `statutory-correction`. Include the correct statutory text and citation.

### 4. Add a missing jurisdiction or local overlay
Open an issue proposing the addition, with the statutory source. For new local overlays (city/county ordinances), include the ordinance citation and a brief description of the protection.

### 5. Improve the validation battery
Contributions to `validation/battery/validate.py` — additional Layer 3 checks, Layer 4 golden-set test runners, Layer 6 legislative tracking integration — are welcome.

### 6. Translate
A2J tools need to serve non-English speakers. Contributions to multilingual output templates are welcome.

## Licensing of contributions

All contributions are licensed under Apache 2.0. By submitting a contribution, you agree that your contribution may be used, modified, and redistributed under the terms of the Apache License, Version 2.0, by anyone, including in paid services and on non-Anthropic AI models.

## Attribution

Every file records contributor attribution in metadata:
- AI drafter: recorded in `ai_drafter_notes`
- Primary reviewer: recorded in `reviewer` field (permanent)
- Additional reviewers: recorded in `additional_reviewers` field

Attribution is permanent. Your name stays in the file's history even if the file is later updated.

## No real client data

Contributions must never introduce real client information. All examples and test cases must use entirely fabricated names, addresses, and facts. This is a hard rule with no exceptions.

## Code of conduct

This project is committed to respectful, constructive collaboration in service of the A2J mission. Contributions that are disrespectful, discriminatory, or off-mission will not be accepted.

---

* CONTRIBUTING.md v0.1 · June 2026*
