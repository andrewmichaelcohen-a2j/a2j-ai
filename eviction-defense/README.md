# Eviction Defense Plugin

**Status:** v0.1.0 — DRAFT. Jurisdiction rules files not yet attorney-validated.

An access-to-justice plugin that screens eviction notices for procedural defects and affirmative defenses. Built to demonstrate the Legal Help Commons (LHC) model: a non-engineer attorney built this in days using Anthropic's plugin/MCP infrastructure, at essentially $0 cost.

## What this plugin does

Given an eviction notice and basic facts about the tenancy, this plugin:

1. Identifies the notice type and required notice period for the jurisdiction
2. Screens for common procedural defects (e.g., impermissible late fees in CA, improper service, CARES Act violations in TX)
3. Flags applicable affirmative defenses (habitability, retaliation, discrimination, just cause)
4. Retrieves the live statute text via Legal Data Hunter MCP connector — not static training data
5. Produces a plain-language triage report with citations and confidence levels
6. Directs the user to local legal aid resources

## Primary use case: Legal aid intake (Carlos persona)

The primary near-term deployment is for **legal aid intake workers** — paralegals and intake staff who screen 20-30 tenant calls per day. The tool helps them quickly identify which cases have strong procedural defenses, flagging them for attorney follow-up.

A direct-to-tenant deployment (the "Maria persona") requires additional validation and attorney oversight design before production use.

## Jurisdictions covered

| Jurisdiction | Rules File | Status |
|-------------|-----------|--------|
| California | `jurisdictions/ca_eviction_rules_v0.1.json` | DRAFT — attorney validation pending |
| Texas | `jurisdictions/tx_eviction_rules_v0.1.json` | DRAFT — attorney validation pending |
| New York | `jurisdictions/ny_eviction_rules_v0.1.json` | DRAFT — attorney validation pending |

## Folder structure

```
eviction-defense/
├── .claude-plugin/plugin.json     ← Plugin metadata
├── README.md                      ← This file
├── jurisdictions/                 ← JSON rules files (one per state)
│   ├── README.md
│   ├── ca_eviction_rules_v0.1.json
│   ├── tx_eviction_rules_v0.1.json
│   └── ny_eviction_rules_v0.1.json
├── skills/
│   └── eviction-triage/
│       └── SKILL.md               ← The workflow instruction file
└── test-cases/
    └── README.md
```

## MCP connectors used

- **Legal Data Hunter** — live statute retrieval (CCP §1161, AB 1482, etc.)
- **CourtListener** — case law citation verification

## The LHC model

This plugin is a demonstration of what the A2J community can build when it uses shared infrastructure rather than starting from scratch. The rules files are the community-maintained content layer — structured, versioned, human-reviewable data that any attorney can validate and any deployment can use.

LHC is not a legal services provider. Every output of this plugin directs users to licensed attorneys and local legal aid organizations.

## Validation needed

**Before any rules file is used in a production deployment advising real tenants, a licensed attorney in the relevant jurisdiction must review and sign off.** See `jurisdictions/README.md` for the validation checklist.

If you are a licensed tenant attorney and can contribute validation, please open an issue or submit a pull request.

## License

Apache License 2.0. Free to use, modify, and adapt to other jurisdictions with attribution.
