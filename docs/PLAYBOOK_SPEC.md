# CJaC Playbook Unit — Schema Specification

**Version:** 1.0  
**Date:** 2026-07-01  
**Directive:** `docs/CJaC_Playbook_Architecture_Directive_20260701.md`  
**Architecture doc:** `docs/ARCHITECTURE.md`

---

## 1. What a playbook is

A **playbook** is the unit of encoding. It encodes all the elements needed to answer one legal question for one claim type in one jurisdiction. It is the basic artifact of the CJaC rules layer.

Each playbook covers exactly one (claim type × jurisdiction) pair. Composition is explicit — an LA notice fact pattern invokes the CA-notice playbook AND the LA RSO overlay playbook; the overlay's rules control where they differ from state law.

---

## 2. Playbook schema (top-level structure)

```json
{
  "playbook_id": "<string: unique ID, e.g. 'ca_notice_pay_or_quit'>",
  "claim_type": "<string: e.g. 'eviction_notice_pay_or_quit'>",
  "jurisdiction": {
    "state": "<string: FIPS state code, e.g. 'CA'>",
    "county": "<string | null>",
    "city": "<string | null>",
    "overlay_of": "<playbook_id | null>",
    "fips_jurisdiction": "<string: FIPS code>"
  },
  "version": "<string: semver, e.g. '1.0.0'>",
  "last_updated": "<ISO date>",
  "attorney_reviewed": "<boolean>",
  "attorney_reviewer": "<string | null>",
  "validation_status": "<enum: DRAFT | AUTOMATED-CHECKS-PASSED | ATTORNEY-REVIEWED | VALIDATED>",
  "source_hierarchy": ["<source_id>", ...],
  "elements": [
    { ... }
  ],
  "interactions": [
    { ... }
  ],
  "notes": "<string | null>"
}
```

---

## 3. Element schema

Each element is one discrete legal question the playbook must answer.

```json
{
  "element_id": "<string: unique within playbook, e.g. 'notice_period'>",
  "name": "<string: human-readable name>",
  "question": "<string: the legal question this element answers>",
  "strategy": "<enum: 'determinate' | 'open_textured'>",
  "known": "<boolean: true if encoded for this jurisdiction>",
  "confidence_tier_cap": "<enum: 'A' | 'B' | 'C'>",

  "determinate_rule": {
    "result": "<string: the outcome when this element's conditions are met>",
    "conditions": [
      {
        "if": "<string: condition description>",
        "then": "<string: result>",
        "citation": "<string: statute/case citation>"
      }
    ],
    "default": "<string | null: result when no condition matches>"
  },

  "open_textured_procedure": {
    "citation_anchor": "<string: primary source the model reasons from>",
    "analytical_framework": "<string: legal test / doctrine the element applies>",
    "bounded_steps": [
      "<string: step 1 — what the model checks first>",
      "<string: step 2 — what the model checks next>",
      "..."
    ],
    "confidence_criteria": {
      "A": "<string: conditions under which Tier A confidence is warranted>",
      "B": "<string: conditions under which Tier B confidence is warranted>",
      "C": "<string: conditions under which Tier C is required>"
    }
  },

  "exceptions": ["<string: known exception descriptions>"],
  "interactions": ["<element_id: elements that interact with this one>"],
  "source_override": ["<source_id: sources that specifically govern this element, overriding playbook defaults>"],
  "source_anchor": "<string | null: specific statute subsection or case citation that grounds this element — REQUIRED for all determinate elements. Format: 'CCP §1161(2)' or 'EDC Associates v. Gutierrez (1984) 153 Cal.App.3d 167'. An element with strategy=determinate MUST have source_anchor populated or flagged=true.>",
  "flagged": "<boolean | null: true if source could not be retrieved for this element (Discipline A retrieval failure) or if grounding is contested. Flagged elements do not advance past DRAFT without attorney ratification.>",
  "flagged_reason": "<string | null: required if flagged=true. Describes the specific question and why human judgment is needed.>",
  "notes": "<string | null>"
}
```

---

## 4. Tag definitions

### 4.1 `determinate`

The element has a specific, codeable answer under current law. The model applies the encoded rule without exercising discretion.

**Criteria for tagging as `determinate`:**
- The rule is specified in statute or regulation with minimal interpretive space
- Courts have not significantly diverged from the statutory text
- The answer is binary or has a finite set of outcomes that can be enumerated
- An attorney can write the rule in if-then form that covers the relevant scenarios

**Output:** Tier A confidence (result is fully specified by encoded rule).

**Examples:**
- Notice period (30d / 60d) as a function of tenancy length — Civ. Code §1946.1(b)
- Payee ID required in pay-or-quit — CCP §1161(2) mandatory content
- SFH exemption from AB 1482 just-cause — Civ. Code §1946.2(e)(8)
- Unconditional quit notice for CCP §1161(4) incurable conduct

### 4.2 `open_textured`

The element requires legal judgment that cannot be fully codified. The model executes a bounded-reasoning procedure.

**Criteria for tagging as `open_textured`:**
- The determination requires applying a legal standard to facts (not just looking up a statutory number)
- Different courts have reached different outcomes on similar facts
- The answer is not binary or cannot be exhaustively enumerated
- The relevant legal test has multiple factors, not all of which point the same way

**Output:** Tier A/B/C depending on how clearly the citation anchor supports the conclusion.

**Examples:**
- Retaliation (temporal proximity + pretext analysis — CCP §1942.5)
- Warranty of habitability defense (habitability standard applied to conditions)
- Partial rent acceptance / waiver doctrine (equitable analysis, fact-specific)
- Utilities-as-"additional-rent" ambiguity (contractual interpretation)

---

## 5. Known/unknown flag

- **`known: true`** — the rule is encoded (`determinate`) or the procedure is specified (`open_textured`). The system gives a grounded answer.
- **`known: false`** — the element exists in this jurisdiction but is not yet encoded. Pipeline output must explicitly say so: "This element has not been encoded for [jurisdiction]."

Unknown elements are **never silently omitted or defaulted.** They are surfaced as gaps. "Withhold rather than guess" is the safety default.

---

## 6. Confidence tiers

| Tier | Meaning | When to assign |
|------|---------|---------------|
| **A** | Rule text directly controls; no discretion | All `determinate` elements; `open_textured` where citation text unambiguously supports conclusion |
| **B** | Bounded-reasoning conclusion; anchor retrieved and applied; plausible and well-supported | `open_textured` elements with anchor retrieved but conclusion requires interpretive judgment |
| **C** | Explicit uncertainty warranted | `open_textured` elements where anchor unavailable or insufficient; or where `determinate` rule has exception not yet encoded |

`confidence_tier_cap` on an element sets the maximum tier the model may report for that element. An element with `confidence_tier_cap: "B"` can return A or B but not claim A if the attorney has judged this element requires bounded reasoning.

---

## 7. Interaction schema

Some elements interact: the answer to one changes what the answer to another means. Interactions are encoded explicitly at the playbook level.

```json
{
  "interaction_id": "<string>",
  "elements": ["<element_id>", "<element_id>"],
  "type": "<enum: 'override' | 'modifier' | 'gate'>",
  "description": "<string: what this interaction means>",
  "rule": "<string: if [X] then [Y] changes to [Z]>"
}
```

**Interaction types:**
- **`override`** — element A's result overrides element B's result when a condition holds
- **`modifier`** — element A modifies (narrows/expands) the conclusion of element B
- **`gate`** — element A must be resolved first; its result determines whether element B applies

**Example:** The SFH exemption (`strategy: determinate`) gates the AB 1482 just-cause requirement. If SFH exemption applies → just-cause element is N/A (not required). If exemption does not apply → just-cause element must be evaluated.

---

## 8. Source identifiers

Source IDs used in `source_hierarchy` and `source_override` must appear in `docs/VALIDATED_RESOURCES_REGISTRY.md`. Canonical IDs:

| Source | ID |
|--------|-----|
| CA Civil Code (live via Legal Data Hunter) | `ca_civil_code_live` |
| CA Code of Civil Procedure (live) | `ca_ccp_live` |
| CourtListener (case law MCP) | `courtlistener_mcp` |
| Descrybe (hard-to-find cases MCP) | `descrybe_mcp` |
| CA Judicial Council UD Benchguide | `ca_benchguide_ud` |
| LSNC Eviction Guide 2026 | `lsnc_eviction_2026` |
| JusticeBench (Stanford) | `justicebench_stanford` |

---

## 9. Example: CA pay-or-quit notice playbook (partial — draft)

```json
{
  "playbook_id": "ca_notice_pay_or_quit_v1",
  "claim_type": "eviction_notice_pay_or_quit",
  "jurisdiction": {
    "state": "CA",
    "county": null,
    "city": null,
    "overlay_of": null,
    "fips_jurisdiction": "06"
  },
  "version": "1.0.0",
  "last_updated": "2026-07-01",
  "attorney_reviewed": false,
  "attorney_reviewer": null,
  "validation_status": "DRAFT",
  "source_hierarchy": ["ca_ccp_live", "ca_civil_code_live", "courtlistener_mcp", "ca_benchguide_ud"],
  "elements": [
    {
      "element_id": "notice_period_nonpayment",
      "name": "Notice period — nonpayment of rent",
      "question": "Is the notice period correct for a nonpayment pay-or-quit notice?",
      "strategy": "determinate",
      "known": true,
      "confidence_tier_cap": "A",
      "determinate_rule": {
        "result": "NOTICE_PERIOD_CORRECT | NOTICE_PERIOD_DEFECTIVE",
        "conditions": [
          {
            "if": "notice type = pay_or_quit AND days_given = 3",
            "then": "NOTICE_PERIOD_CORRECT",
            "citation": "CCP §1161(2)"
          },
          {
            "if": "notice type = pay_or_quit AND days_given ≠ 3",
            "then": "NOTICE_PERIOD_DEFECTIVE",
            "citation": "CCP §1161(2)"
          }
        ],
        "default": null
      },
      "open_textured_procedure": null,
      "exceptions": ["AB 1482 may require different notice for no-fault — see notice_type_classification element"],
      "interactions": ["notice_type_classification"],
      "source_override": null,
      "notes": null
    },
    {
      "element_id": "notice_period_termination_no_fault",
      "name": "Notice period — termination without fault by tenancy length",
      "question": "Is the termination notice period correct given the length of tenancy?",
      "strategy": "determinate",
      "known": true,
      "confidence_tier_cap": "A",
      "determinate_rule": {
        "result": "NOTICE_PERIOD_CORRECT | NOTICE_PERIOD_DEFECTIVE",
        "conditions": [
          {
            "if": "notice type = termination AND max_occupant_residency_years < 1 AND days_given = 30",
            "then": "NOTICE_PERIOD_CORRECT",
            "citation": "Civ. Code §1946.1(c); Stancil v. Superior Court (2021) 11 Cal.5th 381"
          },
          {
            "if": "notice type = termination AND max_occupant_residency_years < 1 AND days_given != 30",
            "then": "NOTICE_PERIOD_DEFECTIVE",
            "citation": "Civ. Code §1946.1(c)"
          },
          {
            "if": "notice type = termination AND max_occupant_residency_years >= 1 AND days_given = 60",
            "then": "NOTICE_PERIOD_CORRECT",
            "citation": "Civ. Code §1946.1(b); Stancil v. Superior Court (2021) 11 Cal.5th 381"
          },
          {
            "if": "notice type = termination AND max_occupant_residency_years >= 1 AND days_given < 60",
            "then": "NOTICE_PERIOD_DEFECTIVE",
            "citation": "Civ. Code §1946.1(b)"
          }
        ],
        "default": null
      },
      "open_textured_procedure": null,
      "exceptions": [
        "Stancil v. Superior Court (2021) 11 Cal.5th 381: threshold is MAX residency among ALL current occupants — not just named tenant. Input: max_occupant_residency_years. ENCODED as machine-checkable per Andy ratification 2026-07-01."
      ],
      "interactions": ["sfh_ab1482_exemption", "ab1482_exemption_matrix"],
      "source_override": null,
      "source_anchor": "Civ. Code §1946.1(b) (60d/≥1yr); Civ. Code §1946.1(c) (30d/<1yr); Stancil v. Superior Court (2021) 11 Cal.5th 381 (any-occupant rule)",
      "flagged": false,
      "flagged_reason": null,
      "notes": "REVISED (self-critique 2026-07-01) + Stancil any-occupant encoded (Andy ratification 2026-07-01): corrected subsection citations AND encoded Stancil machine-checkable — conditions now use max_occupant_residency_years (maximum tenure among all current occupants, not just named tenant). Encodes gap identified in pilot (CA-NOT-03 miss)."
    },
    {
      "element_id": "sfh_ab1482_exemption",
      "name": "Single-family home exemption from AB 1482 just-cause",
      "question": "Does the SFH exemption apply, removing AB 1482 just-cause requirements?",
      "strategy": "determinate",
      "known": true,
      "confidence_tier_cap": "A",
      "determinate_rule": {
        "result": "SFH_EXEMPTION_APPLIES | SFH_EXEMPTION_NOT_APPLICABLE",
        "conditions": [
          {
            "if": "property_type = single_family_home AND prong_a_owner_not_reit_corp_llc_with_corporate_member = true AND prong_b_written_exemption_notice_given = true",
            "then": "SFH_EXEMPTION_APPLIES",
            "citation": "Civ. Code §1946.2(e)(8)(A), (B)"
          }
        ],
        "default": "SFH_EXEMPTION_NOT_APPLICABLE"
      },
      "open_textured_procedure": null,
      "exceptions": [
        "Prong A: owner IS a REIT, corporation, or LLC-with-corporate-member → exemption does not apply regardless of occupancy",
        "Prong B: written exemption notice was NOT given to tenant → exemption does not apply even if Prong A satisfied",
        "Owner-occupancy is NOT the test — this was a prior encoding error (CA-NOT-08 confident-wrong)"
      ],
      "interactions": ["just_cause_requirement"],
      "source_override": null,
      "source_anchor": "Civ. Code §1946.2(e)(8)(A) (entity-type test); Civ. Code §1946.2(e)(8)(B) (written exemption notice)",
      "flagged": false,
      "flagged_reason": null,
      "notes": "REVISED (self-critique 2026-07-01): replaced incorrect not_owner_occupied condition with mandatory two-prong test: (A) owner entity type NOT REIT/corp/LLC-with-corporate-member, AND (B) written exemption notice given to tenant per §1946.2(e)(8)(B). Both prongs required. Encodes gap identified in pilot (CA-NOT-08 miss — prior encoding was confident-wrong)."
    },
    {
      "element_id": "partial_payment_waiver",
      "name": "Partial rent acceptance / waiver doctrine",
      "question": "Did acceptance of rent payment after notice waive the notice?",
      "strategy": "determinate",
      "known": true,
      "confidence_tier_cap": "A",
      "determinate_rule": {
        "result": "NOTICE_WAIVED | NOTICE_NOT_WAIVED | WAIVER_UNCERTAIN",
        "conditions": [
          {
            "if": "landlord_accepted_payment_after_notice = true AND payment_designated_as_rent = true AND landlord_expressly_reserved_rights = false",
            "then": "NOTICE_WAIVED (new notice required)",
            "citation": "EDC Associates v. Gutierrez (1984) 153 Cal.App.3d 167; CCP §1161(2) overstatement doctrine"
          },
          {
            "if": "landlord_accepted_no_payment_after_notice = true",
            "then": "NOTICE_NOT_WAIVED",
            "citation": "EDC Associates v. Gutierrez (1984) 153 Cal.App.3d 167"
          }
        ],
        "default": "WAIVER_UNCERTAIN — route to open-textured exception procedure"
      },
      "open_textured_procedure": {
        "citation_anchor": "EDC Associates v. Gutierrez (1984) 153 Cal.App.3d 167; CCP §1161(2)",
        "analytical_framework": "Waiver exception path — applies only when: (a) payment characterization as rent vs. other charges is ambiguous; OR (b) landlord gave express reservation of rights at time of acceptance; OR (c) partial payment of disputed portion with ongoing dispute. In these cases, apply equitable analysis.",
        "bounded_steps": [
          "Determine whether payment was clearly designated as rent or whether characterization is disputed",
          "Check for express reservation of rights in written or oral communications at time of acceptance",
          "If reservation exists: no waiver — NOTICE_NOT_WAIVED",
          "If characterization ambiguous: flag for attorney judgment"
        ],
        "confidence_criteria": {
          "A": "Clean determinate case — handled by determinate_rule above",
          "B": "Payment characterization ambiguous or partial-payment-only scenario",
          "C": "Express reservation given — outcome depends on exact language; attorney needed"
        }
      },
      "exceptions": [
        "CCP §1161.1 (commercial partial payment) expressly excludes residential dwelling units per §1161.1(d) — do NOT apply to residential tenancies",
        "Express reservation of rights at time of payment prevents waiver — route to open-textured exception path",
        "Payment of charges other than rent (late fees, utilities) does not trigger waiver doctrine"
      ],
      "interactions": [],
      "source_override": ["courtlistener_mcp"],
      "source_anchor": "EDC Associates v. Gutierrez (1984) 153 Cal.App.3d 167; CCP §1161(2) overstatement doctrine; CCP §1161.1(d) (commercial exclusion)",
      "flagged": false,
      "flagged_reason": null,
      "notes": "REVISED (self-critique 2026-07-01): restructured from wholly open_textured to determinate with open-textured exception path per ADDENDUM direction §5. Determinate core: acceptance + no reservation = waiver (Tier A). Open-textured exception: ambiguous characterization / express reservation (Tier B). CCP §1161.1 (commercial only) explicitly excluded. Encodes gap identified in pilot (CA-NOT-16 miss)."
    }
  ],
    {
      "element_id": "ab1482_exemption_matrix",
      "name": "AB 1482 just-cause exemption applicability — full §1946.2(e) matrix",
      "question": "Is this unit exempt from AB 1482 just-cause requirements under any §1946.2(e) exemption category?",
      "strategy": "determinate",
      "known": true,
      "confidence_tier_cap": "A",
      "determinate_rule": {
        "result": "AB1482_EXEMPT | AB1482_COVERED",
        "conditions": [
          {
            "if": "unit_type = transient_tourist_hotel per Civ. Code §1940(b)",
            "then": "AB1482_EXEMPT",
            "citation": "Civ. Code §1946.2(e)(1)"
          },
          {
            "if": "unit_type in [nonprofit_hospital, religious_facility, extended_care_facility, licensed_residential_care_elderly, adult_residential_facility]",
            "then": "AB1482_EXEMPT",
            "citation": "Civ. Code §1946.2(e)(2)"
          },
          {
            "if": "unit_type = dormitory AND owner = higher_education_institution OR k12_school",
            "then": "AB1482_EXEMPT",
            "citation": "Civ. Code §1946.2(e)(3)"
          },
          {
            "if": "tenant_shares_bathroom_or_kitchen_with_owner AND owner_principal_residence_at_property",
            "then": "AB1482_EXEMPT",
            "citation": "Civ. Code §1946.2(e)(4)"
          },
          {
            "if": "owner_principal_resident_at_sfh AND rentable_units_or_bedrooms_rented <= 2",
            "then": "AB1482_EXEMPT",
            "citation": "Civ. Code §1946.2(e)(5)"
          },
          {
            "if": "property_has_two_units_in_single_structure AND owner_occupied_one_unit_at_tenancy_start AND owner_continues_in_occupancy AND neither_unit_is_adu_or_jadu",
            "then": "AB1482_EXEMPT",
            "citation": "Civ. Code §1946.2(e)(6)"
          },
          {
            "if": "certificate_of_occupancy_date_within_15_years_of_notice_date AND unit_type != mobilehome",
            "then": "AB1482_EXEMPT",
            "citation": "Civ. Code §1946.2(e)(7)",
            "note": "15-year window is rolling — measured from notice date"
          },
          {
            "if": "unit_alienable_separately AND owner_not_reit_corp_llc_with_corporate_member AND written_exemption_notice_given_to_tenant",
            "then": "AB1482_EXEMPT",
            "citation": "Civ. Code §1946.2(e)(8)(A)+(B)"
          }
        ],
        "default": "AB1482_COVERED"
      },
      "open_textured_procedure": null,
      "exceptions": [
        "§1946.2(e)(7) new-construction exemption is rolling — a unit may become covered once it exceeds 15 years of age",
        "§1946.2(e)(6) duplex exemption requires owner to have occupied at tenancy START (not just currently) — retroactive owner move-in does not qualify",
        "§1946.2(e)(8) requires BOTH prongs — entity type alone or written notice alone is insufficient"
      ],
      "interactions": ["just_cause_requirement", "notice_period_termination_no_fault"],
      "source_override": null,
      "source_anchor": "Civ. Code §1946.2(e)(1)–(8) — live-source confirmed via WebSearch 2026-07-01 (FindLaw + leginfo.legislature.ca.gov + Mynd/Nolo summaries corroborating)",
      "flagged": false,
      "flagged_reason": null,
      "notes": "ADDED (Andy ratification 2026-07-01 — full exemption matrix). Encodes all 8 exemption categories in §1946.2(e). Default is AB1482_COVERED (just cause required) if none apply. See ca_eviction_v2.json termination.exemptions for corresponding field-level encoding."
    }
  ],
  "interactions": [
    {
      "interaction_id": "sfh_exemption_gates_just_cause",
      "elements": ["ab1482_exemption_matrix", "just_cause_requirement"],
      "type": "gate",
      "description": "Full AB 1482 exemption matrix must be resolved before just-cause requirement is evaluated",
      "rule": "If ab1482_exemption_matrix = AB1482_EXEMPT → just_cause_requirement = N/A (not required). If AB1482_COVERED → just_cause_requirement must be evaluated."
    },
    {
      "interaction_id": "cure_or_quit_vs_unconditional_quit",
      "elements": ["cure_or_quit_notice_type", "unconditional_quit_notice_type"],
      "type": "gate",
      "description": "Conduct type determines which notice instrument applies — §1161(3) vs. §1161(4). This must be resolved before notice type is selected.",
      "rule": "IF conduct_type in bright_line_1161_4_categories (waste, nuisance, unlawful use, unauthorized assignment/subletting per Civ. Code §3482.8/§3485(c)/§3486(c)) → use unconditional_quit (§1161(4)); no cure right. IF conduct_type in bright_line_1161_3_categories (curable covenant breach) → use cure_or_quit (§1161(3)); tenant has 3 court days to cure. IF conduct_type in open_textured_categories (disturbances, repeated violations, etc.) → open-textured analysis required (Tier B/C); route to attorney judgment.",
      "source_anchor": "CCP §1161(3); CCP §1161(4) (Justia 2025 text confirmed 2026-07-01)"
    }
  ],
  "notes": "DRAFT — self-critique complete (2026-07-01); ratified flagged items encoded (2026-07-01). Attorney review required before validation_status advances to ATTORNEY-REVIEWED. Full element set: notice periods, payee_id, SFH exemption (e)(8), full AB1482 exemption matrix, relocation assistance, partial payment waiver, unconditional quit, §1161(3)/(4) gate."
}
```

---

## 10. Validation workflow per playbook

This workflow is the standing lifecycle for every playbook element. No element advances past DRAFT without completing the self-critique step. This is a structural gate — not a per-session option.

1. **DRAFT** — playbook created with proposed element strategy tags and rules; `source_anchor` populated or `flagged: true` set for each element
2. **SELF-CRITIQUE** — mandatory pre-encoding pass (standing step added 2026-07-01 per CJaC_Cowork_Direction_SelfCritique_20260701.md):
   - Discipline A: Every element's citation checked against LIVE primary source text (ca_ccp_live, ca_civil_code_live, courtlistener_mcp). Retrieval failure → `flagged: true`, not confirmed.
   - Discipline B: Adversarial posture — hunt for wrong subsections, incomplete multi-prong tests, missed residential/commercial distinctions, missing day-count mechanics, wrong notice types, currency misses.
   - Discipline C: Source-anchored changes only; ungroundable items are FLAGGED, never guessed.
   - Output: REVISED/CONFIRMED/FLAGGED report. REVISED items auto-applied (each with source anchor). FLAGGED items routed to step 3.
3. **YELLOW / attorney residual** — FLAGGED residual from self-critique reviewed; attorney proposes corrections; strategy tags ratified
4. **Attorney ratification** — Andy signs off on strategy tags, flagged-item resolutions, and encoded rules (RED gate)
5. **AUTOMATED-CHECKS-PASSED** — L1–L3 run clean; `source_anchor` field present on all `determinate` elements (L1 validates this — missing source_anchor = schema failure)
6. **Golden-set score** — L4 scorer runs against frozen fact patterns; regression check run against non-held-out set
7. **ATTORNEY-REVIEWED** — attorney review of L4 misses and open-textured conclusions
8. **VALIDATED** — full 7-layer stack passed; attorney has reviewed

**Note on L1 gate (source_anchor enforcement):** As of 2026-07-01, `source_anchor` is a required field for all elements with `strategy: "determinate"`. An element missing `source_anchor` and `flagged: true` fails L1 schema validation. This enforces "source-anchored or flagged" structurally — the schema, not human memory, is the gate. (`validate.py` must be updated to enforce this — see §3 above.)

---

## 11. Measurement Standards (standing — added 2026-07-01)

These four measurement directives are permanent requirements, not per-session options. Every score report, regression run, and self-critique pass must apply them.

### B1 — Coverage metric (highest priority)

Track `known` vs. `unknown` elements per claim type. Every published score MUST pair accuracy WITH coverage.

**Format for every score report:**
```
Coverage: N_known / N_total = X% (known elements)
Accuracy (on known): C_correct / N_known = Y%
Overall accuracy (incl. unknown): C_correct / N_total = Z%
```

Unknown elements are never silently omitted. If the system cannot answer an element, that is a coverage gap — reported as such, not suppressed.

**Why:** A 90% accuracy score on 5 of 20 elements is worse than 75% on 18 of 20. Without coverage, accuracy scores are misleading.

### B2 — Confident-wrong as distinct higher-severity category

Confident-wrong answers are categorically more dangerous than UNCERTAIN answers. They produce false definitive guidance. Track as a separate metric in every scoring run.

**Classification:**
- `UNCERTAIN`: system says "I don't know" or returns low-confidence answer
- `CONFIDENT-WRONG`: system returns high-confidence definitive answer that is factually incorrect per the golden set

**Target:** Drive CONFIDENT-WRONG count to ZERO. An element that produces confident-wrong answers is more harmful than one producing no answer.

**Scoring note:** Confident-wrong items must be weighted more severely in any optimization pass. A rule encoding that reduces UNCERTAIN count but increases CONFIDENT-WRONG count is a regression, not an improvement.

### B3 — Regression check on every rule change

Any modification to a rule encoding (including REVISED items from a self-critique pass) must be followed by a regression check: re-run the full non-held-out golden set after the change and report newly failing items.

**Process:**
1. Before change: note the non-held-out baseline score
2. Apply REVISED change
3. Re-run non-held-out set
4. Report: newly_failing = items correct before change, incorrect after. If newly_failing > 0 → regression alert; escalate to YELLOW before committing change.

**Why:** A fix to one gap can silently break a previously passing item. Regression check catches this before the change is committed to encoding.

### B4 — Currency as standing check within self-critique

Every self-critique pass includes a currency check: verify each rule's governing authority for post-encoding amendments. Not a periodic L6 sweep alone — integrated into Discipline A.

**Minimum currency check per element:**
- Is the cited statute still in effect as cited (not repealed, amended, or superseded)?
- Are any known amendments since the encoding date material to the rule?
- For case law: is the cited case still good law (not overruled by subsequent authority)?

**Flag:** If a material amendment is found that changes the rule, classify as REVISED (if groundable) or FLAGGED (if attorney judgment required). "Statute effective date" and "amendment date" fields should be populated where known.

---

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
