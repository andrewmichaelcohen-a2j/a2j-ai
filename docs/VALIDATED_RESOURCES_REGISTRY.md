# CJaC Validated Resources Registry

**Version:** 1.0 (seed)  
**Date:** 2026-07-01  
**Maintained by:** Cowork (updates each time a new source is confirmed or a source's status changes)  
**Purpose:** Living catalog of every source CJaC relies on. Every playbook element cites a source ID from this registry. If a source isn't here, it isn't usable.

---

## Reliability rubric

| Tier | Description |
|------|-------------|
| **P1** | Primary, authoritative, live-retrieved — statute text from official source; highest trust |
| **P2** | Primary, authoritative, retrieved but may have currency lag — case law from legal databases |
| **S1** | Secondary, high-quality, regularly updated — official court/judicial council guides |
| **S2** | Secondary, reputable, may lag — practitioner guides, legal aid publications |
| **DS** | Standards dataset — synthetic or research-grade, labeled, purpose-built for eval/testing |
| **TL** | Tool/connector — the mechanism, not the source; reliability depends on underlying data |
| **SK** | Skill/capability — reasoning or analysis capability; not a primary source |

Currency risk:
- **Low** — statutory text updates tracked via official source; currency is managed
- **Medium** — source updated periodically; currency check required at use
- **High** — source may not reflect recent legislative changes; use with explicit date verification

---

## Primary Legal Sources

### `ca_civil_code_live`
- **Name:** California Civil Code (live retrieval)
- **Access:** Legal Data Hunter MCP (`mcp__legal_data_hunter`)
- **Tier:** P1
- **Currency risk:** Low (retrieves current statutory text)
- **Coverage:** CA Civil Code — full coverage; key sections: §1946.1, §1946.2, §1940–1954.05
- **Limitations:** MCP requires connected session; connector must be authenticated
- **Use for:** CA tenancy termination rules, AB 1482 just-cause, relocation assistance, habitability
- **Status:** ✅ Confirmed accessible (used in prior validation runs)

### `ca_ccp_live`
- **Name:** California Code of Civil Procedure (live retrieval)
- **Access:** Legal Data Hunter MCP (`mcp__legal_data_hunter`)
- **Tier:** P1
- **Currency risk:** Low
- **Coverage:** CA CCP — full coverage; key sections: §1161, §1161a, §1167, §415.45, §415.46
- **Limitations:** MCP requires connected session
- **Use for:** CA notice content requirements, service requirements, summons rules, UD procedure
- **Status:** ✅ Confirmed accessible

### `courtlistener_mcp`
- **Name:** CourtListener — case law retrieval
- **Access:** CourtListener MCP (`mcp__ce0d1a6b-7e3a-4838-bed4-3f193fe71d77__*`)
- **Tier:** P2
- **Currency risk:** Medium (CL has excellent CA coverage; some small-state gaps documented — KS, SC, NV perm-fail confirmed 2026-06-30)
- **Coverage:** Federal courts + all states; CA coverage excellent. Known gaps: KS (Stephens v. Ludy not indexed), NV (Paullin v. Sutton not indexed), SC (Wadell not indexed).
- **Limitations:** Rate limits (429 frequent during batch runs; sleep=15–20s required); some lower-court opinions not indexed
- **Use for:** Holdings verification, Multi-model corroboration (Check B/C in retaliation holdings v3)
- **Status:** ✅ Confirmed accessible (active in validation pipeline)
- **Notes:** Two-rate reporting required: method rate = MV÷(MV+CI+RC); overall rate = MV÷all (including PR)

### `descrybe_mcp`
- **Name:** Descrybe — hard-to-find legal cases
- **Access:** Descrybe MCP (requires authentication — `plugin:legal:descrybe`)
- **Tier:** P2
- **Currency risk:** Medium
- **Coverage:** Specializes in cases not well-indexed in major databases; particularly useful for small-state/lower-court holdings
- **Limitations:** Requires MCP authentication. **⚠️ NOT YET AUTHENTICATED in current session.** See BLOCKED section.
- **Use for:** KS/NV/SC/VT cases not found via CourtListener; hard-to-find state court opinions
- **Status:** ⚠️ Unauthenticated — pending (YELLOW — Andy call on KS/SC/NV strategy)

### `legal_data_hunter_mcp`
- **Name:** Legal Data Hunter MCP
- **Access:** `plugin:legal:legal data hunter` (requires authentication)
- **Tier:** TL (tool — wraps statute retrieval)
- **Currency risk:** Low (retrieves live)
- **Coverage:** CA, TX, NY, FL statutes confirmed; 50-state coverage expected
- **Status:** ✅ Confirmed accessible (used for CA/TX/NY in prior runs)

---

## Secondary Sources

### `ca_benchguide_ud`
- **Name:** California Judicial Council — Unlawful Detainer Benchguide (BG 31, 2015 edition)
- **Access:** PDF confirmed at: http://www.sblawlibrary.org/uploads/7/3/1/1/7311175/bg31_2015.pdf and https://www2.courtinfo.ca.gov/protem/pubs/bg31.pdf
- **Tier:** S1
- **Edition confirmed:** 2015 — covers case law through 58 C4th, 236 CA4th, legislation to 1/1/2015
- **Currency risk:** ⚠️ HIGH — 2015 edition is materially outdated for CJaC purposes. AB 1482 (2019), SB 567 (2024 eff. 4/1/2024), SB 611 (2025 eff. 2/1/2025), and Stancil v Superior Court (2021) are ALL absent. A newer edition (reportedly 2020) may exist but was not accessible.
- **Coverage:** CA UD law — notice content requirements, cure vs. unconditional quit, 30/60-day distinction, overstatement, waiver doctrine, service methods, procedural checklist. Authoritative for pre-2015 core rules.
- **Limitations:** Does not cover AB 1482 just cause, §1946.2 exemptions, relocation assistance (§1946.2(d)), or the SB 611 court-days amendment to CCP §1161. Must NOT be cited as authority for any post-2015 rule without live primary source cross-check.
- **Key hypotheticals extracted:** See `docs/CA_UD_BENCHGUIDE_BG31_EXTRACT.md` — website URL notice defect (§31.16, Foster v Williams), overstatement scenarios (§31.20), wrong-notice-type (§31.2(7)), premature filing (§31.25), partial payment waiver (§31.26(2))
- **Use for:** (1) Independent source of fact patterns for golden set v0.2 construction (pre-2015 core rules); (2) Third corroborating source for CA notice/service validation runs — corroborates only; statute/case controls.
- **Intended authority role:** Benchguide corroborates. If benchguide conflicts with statute, statute controls. If benchguide conflicts with case law, flag for attorney review.
- **Status:** ✅ LOCATED + CONFIRMED (2026-07-01). YELLOW-REG-01 RESOLVED with currency warning. Extracted to `docs/CA_UD_BENCHGUIDE_BG31_EXTRACT.md`.
- **Status:** ⚠️ Pending — research task in WORK_QUEUE NEXT (Stage 1)

### `lsnc_eviction_2026`
- **Name:** LSNC (Lawyers for Civil Justice) Eviction Guide 2026 / LSNC CA eviction defense materials
- **Access:** LSNC website / practitioner network
- **Tier:** S2
- **Currency risk:** Medium (annual updates; confirm edition before citing)
- **Coverage:** CA-focused; strong on notice and procedural defects
- **Limitations:** Secondary source only; not directly citable; synthesizes attorney practice knowledge
- **Use for:** Synthesizing practitioner understanding of doctrine; identifying open-textured elements and interaction patterns
- **Status:** ⚠️ Referenced in prior work; not formally confirmed current edition

---

## Standards Datasets

### `justicebench_stanford`
- **Name:** JusticeBench / Stanford Legal Design Lab (Margaret Hagan)
- **Access:** justicebench.org / legalhelpcommons.org; public datasets
- **Tier:** DS
- **Currency risk:** Medium (datasets published; verify publication date)
- **Coverage:** Synthetic, PII-free, labeled legal-help query datasets. CA and multi-state. Formats: High Risk Legal Help Queries, L3Q, Common-48, LHSQ115.
- **Alignment:** CJaC aligns with JusticeBench at LIST + FIPS + task-taxonomy tags. See `docs/JUSTICEBENCH_ALIGNMENT_SPEC.md`.
- **Limitations:** Purpose-built for query/issue classification, not specifically for CA eviction notice outcome testing. Filter by LIST housing codes to get relevant subset.
- **Use for:** Seeding L4 golden-set candidates; aligning CJaC's testing with shared field datasets; rubric-as-eval methodology (Hagan principle: the standard for doing the work = the standard for judging it)
- **Status:** ✅ Confirmed (alignment spec complete; not yet integrated into L4 golden sets — pending Direction B expansion)

### `lsc_temple_dataset`
- **Name:** LSC / Temple — synthetic legal aid evaluation datasets
- **Access:** Research network; confirm current source
- **Tier:** DS
- **Currency risk:** Medium
- **Coverage:** Multi-jurisdiction; eviction and consumer debt scenarios
- **Limitations:** ⚠️ Survey of existing golden sets is Direction B item (Task #78 — pending). Exact dataset contents and availability not yet confirmed.
- **Use for:** Direction B golden-set seeding (if eviction-relevant items can be isolated)
- **Status:** ⚠️ Pending survey — Direction B Task #78

---

## Skills and Capabilities

### `claude_native_legal`
- **Name:** Claude (frontier model) — native legal analysis capability
- **Access:** Claude model in use (claude-sonnet-4-6 as of 2026-07-01; architecture is model-agnostic)
- **Tier:** SK
- **Role in pipeline:** **PRIMARY reasoning engine** for open-textured element evaluation, element decomposition proposals, bounded-reasoning procedure execution, and issue-spotting for unknown elements
- **Decision (2026-07-01):** Adopted as the CJaC reasoning engine by directive. The 7-layer validation stack (L1–L7) with multi-model consensus and attorney review is the validation that wraps the model's native reasoning. Adding intermediary skill layers would add complexity without adding rigor.
- **Limitations:** Model is not a lawyer; not a source of ground truth; outputs require validation. "Machine-verified" is below the attorney line.
- **Use for:** Open-textured element evaluation; bounded-reasoning procedure execution; element decomposition proposals (subject to attorney ratification); text interpretation; issue-spotting for unknown elements
- **Status:** ✅ Active — confirmed as reasoning engine (2026-07-01 directive); in use throughout pipeline

### `legal_plugin_skills`
- **Name:** `legal:*` plugin skills (Cowork legal plugin)
- **Skills available:** `legal:brief`, `legal:compliance-check`, `legal:legal-risk-assessment`, `legal:review-contract`, `legal:triage-nda`, `legal:legal-response`, `legal:meeting-briefing`, `legal:vendor-check`, `legal:signature-request`
- **Tier:** SK
- **Decision (2026-07-01):** NOT adopted wholesale. These skills are designed for corporate/contract/compliance legal workflows, not eviction-defense element encoding. The directive confirmed no skills named "legal-analysis" or "issue-spotting" exist by those names. Use a `legal:*` skill only if a specific, narrow task cleanly maps to one — and document the use.
- **Use for:** Potentially: structured contract-risk frameworks adapted for element-level legal risk scoring (evaluate case-by-case)
- **Status:** ✅ Available in environment; ❌ NOT integrated into CJaC pipeline (by decision, 2026-07-01). YELLOW-REG-02 RESOLVED.
- **Notes:** No named "legal-analysis" or "issue-spotting" skill exists. Native Claude capability is the engine.

### `lawvable_mcp`
- **Name:** Lawvable MCP — legal skills search/execution
- **Access:** `mcp__bce93016-1013-47ce-a3d8-82250e5d6b93__*` tools (search_skills, get_skill_manifest, list_filters, call_tool)
- **Tier:** SK + TL
- **Role in pipeline:** ❌ No eviction/housing skills found in marketplace (searched 2026-07-01).
- **Limitations:** Marketplace is corporate/compliance-oriented (EU data law, legal ops, billing, arbitration). No housing-law or residential-tenancy category. 189 skills total; US jurisdiction = 20 skills (sanctions screening, employment, customs, privacy, CT divorce, trademark) — none relevant to eviction-defense encoding.
- **Use for:** Not applicable to CJaC eviction-defense encoding. Potentially relevant if CJaC expands to commercial/corporate law domains.
- **Status:** ✅ EXPLORED 2026-07-01 — YELLOW-REG-03 RESOLVED. CJaC eviction-defense encoding is novel territory not covered by any existing Lawvable skill. Native Claude capability + CJaC-built pipeline is the correct architecture.

---

## Multi-Model Consensus (Methodology)

### `multi_model_consensus`
- **Name:** Multi-model consensus protocol (GPT-5.5 + Gemini 2.5 Pro)
- **Models:** `gpt-5.5` (OpenAI) + `gemini-2.5-pro` (Google)
- **Role:** Verification mechanism — two independent models must corroborate a holding to reach MV status
- **Not a source:** Multi-model consensus is a verification method, not a primary legal source. Consensus of two models ≠ correctness; it increases confidence and catches obvious errors.
- **Consensus-operative gate (2026-07-01):** A run is only consensus-validated when BOTH models return non-empty responses on ALL scored items. A run where either model returns empty is classified as single-model (SM-GPT, SM-GEMINI, PARTIAL-CONSENSUS) and flagged as NOT consensus-validated. The scorer now enforces this with a loud banner and `consensus_status` field in the JSON. GPT has also returned empty on non-notice modules historically — consensus integrity must be confirmed per-run, not assumed.
- **Limitations:** Gemini returning 503 UNAVAILABLE (capacity — not credits) on most calls as of 2026-07-01 evening. Credits confirmed restored (CA-NOT-08 returned AGREE). Capacity issue expected to be temporary; VT retry overnight will confirm.
- **Status:** ⚠️ PARTIAL-CONSENSUS. Credits restored. Stage 2 encoding run achieved PARTIAL-CONSENSUS (1/11 dual-model). Cannot cite as consensus-validated until Gemini 503 clears and a clean DUAL-MODEL-CONSENSUS run completes.

---

## Source Status Summary

| Source ID | Type | Status | Confirmed |
|-----------|------|--------|-----------|
| `ca_civil_code_live` | P1 | ✅ Active | Yes |
| `ca_ccp_live` | P1 | ✅ Active | Yes |
| `courtlistener_mcp` | P2 | ✅ Active (rate-limited) | Yes |
| `descrybe_mcp` | P2 | ⚠️ Unauthenticated | No |
| `legal_data_hunter_mcp` | TL | ✅ Active | Yes |
| `ca_benchguide_ud` | S1 | ✅ Located — 2015 ed. (pre-AB 1482; currency warning) | Partial |
| `lsnc_eviction_2026` | S2 | ⚠️ Not confirmed current | Partial |
| `justicebench_stanford` | DS | ✅ Alignment complete | Yes |
| `lsc_temple_dataset` | DS | ⚠️ Pending survey | No |
| `claude_native_legal` | SK | ✅ Active | Yes |
| `legal_plugin_skills` | SK | ⚠️ Available; not integrated | Partial |
| `lawvable_mcp` | SK+TL | ✅ Explored — no relevant skills | No (N/A) |
| `multi_model_consensus` | Methodology | ⚠️ PARTIAL-CONSENSUS (Gemini 503 capacity; credits restored) | Partial |

---

## YELLOW flags

**YELLOW-REG-01:** ✅ RESOLVED WITH CURRENCY WARNING (2026-07-01). BG 31 located and extracted (2015 edition only — legislation through 1/1/2015). Currency risk HIGH: AB 1482, SB 567, SB 611, Stancil all absent. Use for independent fact patterns (golden set v0.2) and pre-2015 rule corroboration only. No post-2015 rule may be cited from this source without live primary-source cross-check. Extraction at `docs/CA_UD_BENCHGUIDE_BG31_EXTRACT.md`. Newer 2020 edition reportedly exists — not yet located.

**YELLOW-REG-02:** ✅ RESOLVED (2026-07-01). No skills named "legal-analysis" or "issue-spotting" exist. Claude's native legal-reasoning capability confirmed as the CJaC reasoning engine. `legal:*` plugins NOT adopted wholesale. Decision documented in ARCHITECTURE.md Section 12.

**YELLOW-REG-03:** ✅ RESOLVED (2026-07-01). Lawvable MCP fully searched — no eviction/housing/tenant-landlord skills exist in the marketplace. 189 skills across 20 categories; corporate/compliance focus. CJaC is novel territory. Native Claude capability + CJaC pipeline confirmed as correct architecture.

**YELLOW-REG-04:** Descrybe MCP — unauthenticated. KS/SC/NV strategy depends on whether Descrybe can surface cases CL cannot. Andy's call on whether to authenticate and attempt retrieval.

---

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
