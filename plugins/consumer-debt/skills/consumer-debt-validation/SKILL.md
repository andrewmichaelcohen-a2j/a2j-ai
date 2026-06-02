---
name: consumer-debt-validation
description: "Screen a consumer debt collection matter for common defenses and produce a plain-language analysis with citations. Use when a consumer has been contacted or sued by a debt collector or debt buyer and needs to understand potential defenses such as time-barred debt, broken chain of title, or FDCPA violations. Assists screening and analysis only; does not provide legal advice or practice law."
---

# Consumer Debt Validation

> **STATUS: DRAFT (v0.1.0). NOT YET ATTORNEY-REVIEWED. DO NOT RELY ON OUTPUT.**
> This file is a skeleton. The substance is drafted in Phase 5 of the development plan.

## Skill metadata

- **Version:** 0.1.0 (draft)
- **Jurisdictions covered:** none validated yet — target: Los Angeles County, California
- **Last reviewed:** not yet reviewed
- **Supervising attorney:** Andrew M Cohen
- **Legal frameworks:** Fair Debt Collection Practices Act (FDCPA, 15 U.S.C. § 1692 et seq.); California statutes of limitations (e.g., Code of Civil Procedure § 337); Rosenthal Fair Debt Collection Practices Act (Cal. Civ. Code § 1788 et seq.); California Fair Debt Buying Practices Act (Cal. Civ. Code § 1788.50 et seq.); applicable California civil procedure rules.

## Important scope statement

This skill **assists** a self-represented litigant or a supervising attorney by screening a consumer debt matter and organizing a plain-language analysis. It does **not** provide legal advice, does not establish an attorney-client relationship, and does not practice law. All output must be reviewed by a supervising attorney before being relied upon or shared with a client.

## Out of scope

- Bankruptcy strategy and filings.
- Counterclaims or affirmative litigation beyond defensive screening.
- Matters outside the covered jurisdictions.
- Any situation flagged for escalation below.

---

## (Skeleton — sections to be drafted in Phase 5)

### 1. When to use this skill
_To be drafted: trigger conditions._

### 2. Intake
_To be drafted: the structured questions or document fields the skill gathers — e.g., who is suing, the original creditor, the alleged amount, the date of last payment/default, what documents the consumer has received, the date and method of service._

### 3. Decision logic
_To be drafted: the legal analysis applied to the intake, including:_
- _Statute of limitations check (using the jurisdiction data)._
- _Chain-of-title / standing analysis._
- _FDCPA and Rosenthal Act validation-notice and conduct analysis._
- _California Fair Debt Buying Practices Act screen._
- _Jurisdictional and procedural defenses._

### 4. Output
_To be drafted: a structured, plain-language analysis with citations, explicit next steps, and — where appropriate — a draft response using the jurisdiction's actual court forms._

### 5. Escalation triggers
_To be drafted: conditions under which the skill should stop and direct the user to a licensed attorney rather than continue._

### 6. Jurisdiction data references
_To be drafted: pointers to the relevant files in `../../jurisdictions/`._

### 7. Test cases
_To be drafted: references to the fabricated fact patterns in `../../test-cases/` used to validate this skill._


---

*Copyright 2026 Andrew M Cohen. Licensed under the [Apache License, Version 2.0](../LICENSE).*