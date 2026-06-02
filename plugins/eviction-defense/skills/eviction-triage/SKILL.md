---
name: eviction-triage
description: "Screen an eviction notice for procedural defects and affirmative defenses and produce a plain-language triage report with live statute citations. Use when a tenant has received an eviction notice and needs to understand whether it may be defective and what defenses may apply. Supports legal aid intake workers (primary use case) and self-represented tenants. Covers California, Texas, and New York. Assists screening only — does not provide legal advice or practice law."
---

# Eviction Triage Skill

> **STATUS: DRAFT (v0.1.0). NOT YET ATTORNEY-REVIEWED.**
> CA/TX/NY jurisdiction rules files are AI-generated drafts awaiting licensed attorney validation.
> Do not use output to advise real tenants until validation is complete.

## Skill metadata

- **Version:** 0.1.0 (draft)
- **Jurisdictions covered:** California (full), Texas (portability demo), New York (portability demo)
- **Primary use case:** Legal aid intake worker (Carlos persona) — not direct-to-tenant deployment
- **Last reviewed:** Not yet reviewed by supervising attorney
- **MCP connectors required:** Legal Data Hunter (statute retrieval), CourtListener (case law verification)
- **Rules files:** `../../jurisdictions/ca_eviction_rules_v0.1.json`, `tx_eviction_rules_v0.1.json`, `ny_eviction_rules_v0.1.json`

---

## Important scope statement

This skill **assists** a legal aid intake worker or supervising attorney by screening an eviction notice and producing a structured triage report. It does **not** provide legal advice, does not establish an attorney-client relationship, and does not practice law.

Every output includes: *"This is legal information, not legal advice. I am not a lawyer. Verify all findings with a licensed attorney before taking any action."*

For the near-term deployment: a supervising attorney reviews every output before it is shared with or acted upon by a tenant.

---

## Out of scope

- Legal advice or prediction of court outcomes
- Representation at hearing or drafting of court filings
- Jurisdictions other than CA, TX, NY (flag and stop if another state is presented)
- Cases where the tenant has already received a court summons (escalate immediately to attorney)
- Any situation flagged for escalation in Section 6 below

---

## 1. When to use this skill

Use this skill when:
- A tenant has received a written eviction notice (pay-or-quit, notice to cure, termination notice, or similar)
- The case has NOT yet proceeded to a court filing / unlawful detainer summons
- The jurisdiction is California, Texas, or New York

Do NOT use this skill when:
- The tenant has already been served with a court summons — escalate immediately
- The user is asking for legal advice on what to do in court
- The jurisdiction is outside CA/TX/NY — tell the user this skill does not yet cover their state and refer to local legal aid

---

## 2. Intake — what to collect

Ask the user the following questions. Collect all answers before running the analysis.

### Required
1. What **state** is the rental unit in? (If not CA, TX, or NY — stop and refer to local legal aid)
2. What **city** is the rental unit in?
3. What **type of notice** was served? (e.g., 3-day pay or quit, 30-day termination, etc. — ask them to read the title of the notice)
4. What is the **exact dollar amount** stated in the notice, if any?
5. Does the notice include any charges **other than unpaid rent**? (Ask specifically: late fees, utilities, other fees)
6. How **long has the tenant lived** in the unit? (Approximate is fine — months or years)
7. How was the notice **delivered**? (Handed directly / left with someone / posted on door / mailed)
8. What **date** was the notice served or received?

### Important follow-ups (ask based on initial answers)
9. **If CA and 12+ months tenancy:** Does the unit appear to be in a multi-unit building built before 2010? (AB 1482 coverage screen)
10. **If CA:** Has the landlord accepted any rent payment since serving the notice?
11. **If TX:** Was the tenant current on rent before the month they fell behind? (SB 38 question)
12. **If TX:** Does the tenant receive Section 8 or any federal housing assistance? (CARES Act screen)
13. **Any jurisdiction:** Has the tenant made any written complaints about repairs or habitability in the past 6 months?
14. **Any jurisdiction:** Has the tenant contacted code enforcement or any government agency about the unit in the past year?

---

## 3. Statute retrieval — run before analysis

Before applying the rules file, retrieve the current statute text for the key statutes in the jurisdiction. This grounds the analysis in the actual current law rather than training data.

**For California:**
- Use Legal Data Hunter to retrieve: CCP §1161 and Civil Code §1946.2
- Source: US/CA-Legislation
- Confirm the retrieved text matches the rules file citations. If there is a conflict, flag it and note the discrepancy in the output.

**For Texas:**
- Use Legal Data Hunter to retrieve: Texas Property Code §24.005
- Source: US/TX-Legislation (if available) — otherwise note that TX statutory text was not retrieved live and flag accordingly

**For New York:**
- Use Legal Data Hunter to retrieve: RPAPL §711
- Source: US/NY-Legislation (if available) — otherwise flag accordingly

**If Legal Data Hunter is unavailable:** Note in the output that live statute retrieval was not possible for this session and that the analysis is based on the rules file alone. Do not fabricate a statute URL.

---

## 4. Decision logic — how to apply the rules file

Load the appropriate rules file for the jurisdiction: `../../jurisdictions/{state_code}_eviction_rules_v0.1.json`

Work through the analysis in this order:

### Step 1 — Identify the notice type
Match the notice described by the user to the notice types in `notice_periods`. If the notice type is unclear, ask a clarifying question.

### Step 2 — Check notice period
Is the notice period stated in or implied by the notice consistent with what the rules file requires for that notice type and tenancy length? Flag if the period appears too short.

### Step 3 — Run defect triggers
Check every `defect_trigger` in the matched notice type AND in `service_requirements`. For each trigger:
- Does the intake information suggest this defect is present?
- If YES: flag as DEFECT DETECTED with the defect ID, description, statute, and confidence level
- If NO: note as checked and clear
- If UNKNOWN (insufficient information): flag as UNABLE TO DETERMINE and explain what additional information is needed

### Step 4 — Check jurisdiction-specific overlays
- **CA:** Run AB 1482 coverage screen if tenancy is 12+ months. Check local overlay flag list for the city.
- **TX:** Run CARES Act screen. Run SB 38 check.
- **NY:** Run Good Cause Eviction coverage screen. Check NYC rent stabilization flag if applicable.

### Step 5 — Screen affirmative defenses
Review each defense in `affirmative_defenses`. Based on intake answers, flag which defenses are:
- **Potentially applicable** — explain why and what documentation the tenant should gather
- **Not applicable based on available facts**
- **Unknown** — explain what additional information is needed

### Step 6 — Confidence calibration
For each finding, assign a confidence level:
- **HIGH** — the rules file is clear, the statutory basis is explicit, and the facts strongly support the conclusion
- **MEDIUM** — the rules file suggests this issue but the facts are ambiguous or additional information is needed
- **LOW / FLAG FOR ATTORNEY** — the issue requires legal judgment beyond what the rules file can definitively resolve

---

## 5. Output format

Produce the triage report in this structure:

```
EVICTION NOTICE TRIAGE REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ LEGAL INFORMATION ONLY — NOT LEGAL ADVICE
This analysis is based on publicly available law and a structured rules file.
It has not been reviewed by a licensed attorney. Verify all findings before acting.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NOTICE SUMMARY
• Jurisdiction: [state, city]
• Notice type: [type identified]
• Required notice period: [X days per rules file]
• Notice period given: [X days as stated/calculated]
• Date of service: [date provided]

DEFECT SCREENING RESULTS
[For each defect trigger checked:]
• [DEFECT ID] — [DEFECT DETECTED / CLEAR / UNABLE TO DETERMINE]
  Description: [plain-language explanation]
  Statute: [citation + live URL if retrieved]
  Confidence: [HIGH / MEDIUM / LOW]

AFFIRMATIVE DEFENSES TO EXPLORE
[For each potentially applicable defense:]
• [Defense name] — [Potentially applicable / Not applicable / Unknown]
  Why it may apply: [plain-language explanation]
  What to gather: [documentation list]

STATUTE RETRIEVAL
• CCP §1161 retrieved: [YES — URL / NO — flag]
• Civil Code §1946.2 retrieved: [YES — URL / NO — flag]
• Rules file version: [version number and DRAFT status]

NEXT STEPS
1. Contact a licensed attorney or legal aid organization immediately to review these findings.
2. Do not ignore the notice — deadlines are short.
3. Gather documentation for any defenses identified above.
4. [Jurisdiction-specific next step if applicable]

LOCAL LEGAL AID RESOURCES
[Insert from output_templates.attorney_referral in the rules file]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Rules file: {state_code}_eviction_rules_v0.1.json (DRAFT — attorney validation pending)
Skill version: eviction-triage v0.1.0 (DRAFT)
This output must be reviewed by a supervising attorney before being shared with a tenant.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 6. Escalation triggers — stop and refer to an attorney

Stop the analysis and immediately direct the user to a licensed attorney if:

- The tenant has already been served with a **court summons** (unlawful detainer complaint) — deadlines are typically 5 business days in CA, very short in TX; every hour matters
- The user describes **lockout, utility shutoff, or harassment** by the landlord — these may be illegal self-help evictions; different legal remedies apply
- The analysis reveals a **domestic violence** situation — Civil Code §1946.7 (CA) and equivalents apply; special protections exist
- The user describes a **mobile home** situation — different statutory framework applies in all three states
- The user is in a **jurisdiction outside CA/TX/NY** — this skill does not cover their state
- The facts are **highly ambiguous** and the confidence level on all findings is LOW — do not produce a triage report that could mislead; flag for attorney review instead
- The user appears to be in **immediate physical danger** — stop legal analysis and refer to emergency services

---

## 7. Jurisdiction data references

Rules files are in `../../jurisdictions/`:
- `ca_eviction_rules_v0.1.json` — California (full demo jurisdiction)
- `tx_eviction_rules_v0.1.json` — Texas (portability demonstration)
- `ny_eviction_rules_v0.1.json` — New York (portability demonstration)

---

## 8. Test cases

Fabricated test scenarios for validating this skill are in `../../test-cases/`. These will be added in the next build session. Each test case includes:
- A fabricated notice with known defects
- Expected triage output
- Pass/fail criteria for the skill

---

## 9. Demo script reference

This skill is the technical backbone of the Andrew M Cohen Eviction Defense Demo. The 10-minute demo script in the architecture document maps to this skill as follows:

| Demo beat | Skill component |
|-----------|----------------|
| Enter Maria's notice facts | Section 2 — Intake |
| Show defect flagged (late fees) | Step 3 — Defect triggers (CA-DEFECT-01) |
| Click through to live statute | Section 3 — Statute retrieval |
| Open the CA rules file | `../../jurisdictions/ca_eviction_rules_v0.1.json` |
| Switch to Texas | Load `tx_eviction_rules_v0.1.json` — same skill, different rules file |
| Show portability | TX output: no just cause flag, CARES Act check added |


---

*Copyright 2026 Andrew M Cohen. Licensed under the [Apache License, Version 2.0](../LICENSE).*