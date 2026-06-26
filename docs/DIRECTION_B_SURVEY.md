# Direction B — Golden Set Survey
## Adoptable Ground Truth for Eviction Defense Modules

*Completed: 2026-06-25 · Cowork autonomous (GREEN)*
*Purpose: Survey existing public datasets before generating candidates from scratch.*

---

## Bottom Line

**No existing public dataset provides ready-made annotated fact-pattern/answer pairs for our specific modules** (notice, service, procedural defects, retaliation). We must generate candidates from scratch. The survey did surface two useful secondary resources and one methodology reference.

---

## Sources Surveyed

### 1. LSC/Temple Eviction Laws Database (LawAtlas)

**What it is:** 50-state + DC + territories legal map of eviction laws in effect as of January 1, 2021. Structured data on pre-filing notice requirements, judicial procedures, and post-judgment rights. Built by Temple University Center for Public Health Law Research in partnership with the Legal Services Corporation.

**URL:** https://lawatlas.org/page/state-territorial-and-local-eviction-laws-database

**What it is NOT:** Annotated fact-pattern/answer pairs. It encodes statutory requirements (e.g., "notice period = X days"), not "given this fact pattern, what is the correct answer."

**Adoption potential — SECONDARY USE ONLY:** The database is valuable as a cross-reference for our statutory holdings validation. When our v2 rules files say "notice must be X days," we can check against LawAtlas to confirm. Notable caveat: data is as of Jan 1, 2021 — five years old. Any state with legislative changes since 2021 (many have made COVID-era reforms permanent) would require currency verification before we rely on it.

**Verdict:** Not adoptable as golden-set source. Useful as a spot-check layer for our MV holdings.

---

### 2. LegalBench (Stanford, NeurIPS 2023)

**What it is:** 162 open benchmark tasks for legal reasoning, collaboratively designed by lawyers and researchers. Six reasoning categories: rule application, case comparison, statutory interpretation, rule conclusion, rule recall, interpretation. Available at https://hazyresearch.stanford.edu/legalbench/

**What it has for housing/eviction:** Limited. The benchmark includes some eviction-adjacent tasks via the Learned Hands integration (legal issue spotting — "is this a housing law problem?"), but the task type is classification ("does this issue type apply?"), not rule application ("given this notice period and these facts, is the notice legally sufficient?"). The IRAC structure (Issue → Rule → Application → Conclusion) in LegalBench is aligned with our fact-pattern design.

**Adoption potential — METHODOLOGY TEMPLATE:** The LegalBench IRAC structure is a good methodology reference for how to design our golden-set fact patterns. The actual tasks are not directly adoptable for our use case.

**Verdict:** Methodology reference. Not adoptable as golden-set content.

---

### 3. Learned Hands (Stanford Legal Design Lab + Suffolk LIT Lab)

**What it is:** Crowdsourced legal issue labeling game. Players read Reddit stories and classify whether legal issue types are present (housing? eviction? notice defect?). Produces labeled datasets for issue-spotting classifiers.

**URL:** https://learnedhands.law.stanford.edu/

**Why not adoptable:** The task is "is this legal issue present in this narrative?" Our golden-set task is "given this fact pattern and these jurisdiction-specific facts, is the notice legally sufficient, and which statute governs?" These are structurally different. Learned Hands data is also sourced from self-reported Reddit posts, not structured attorney-reviewed scenarios.

**Verdict:** Not adoptable.

---

### 4. JusticeBench (Stanford Legal Design Lab, 2025)

**What it is:** New R&D platform for A2J AI benchmarks, still under active development (explicitly flagged as 🚧 under construction). Hosts LegalBench and some eviction-specific tools (e.g., California jury instruction generator). Covers eviction, debt, custody, government benefits domains.

**URL:** https://www.justicebench.org/

**Adoption potential:** Too early. Platform is not yet stable. Worth monitoring as a future publication venue for our own golden sets.

**Verdict:** Monitor. Not adoptable now.

---

### 5. Stanford AI+A2J (Gates Foundation, Jan 2025)

**What it is:** Initiative to build AI co-pilots for eviction defense (with Legal Aid Foundation of LA) and re-entry debt (with Legal Aid Services of Oklahoma). Intake agent prototype completed March 2025.

**Why not adoptable:** Outputs are proprietary prototypes in partnership with specific legal aid organizations. Not public datasets. The work validates that the problem space is right but does not release training/eval data.

**Verdict:** Awareness only. Not adoptable.

---

### 6. Eviction Lab (Princeton)

**What it is:** 80M+ court eviction records, demographic and geographic analysis. Core output: eviction rate statistics.

**Why not adoptable:** This is court outcome data (was an eviction filed/granted?), not annotated legal reasoning data (was the notice legally sufficient?). Completely different layer.

**Verdict:** Not adoptable.

---

### 7. NCSC/New America Court Data Standards

**What it is:** Effort to standardize eviction court data fields across jurisdictions. About data collection, not legal reasoning annotation.

**Verdict:** Not adoptable.

---

## Recommended Path Forward

Since no existing dataset is adoptable for golden sets, generate candidates from scratch per the Direction B design (docs/COWORK_DIRECTION_B_GOLDEN_SETS.md).

**Phased approach (DRAFT — for Andy's ratification):**

**Phase 1 — CA notice + CA service (pilot pair, ~15–25 each)**
- Start with CA because it has the most attorney capacity (LAFLA partnership context), the most case law, and our v2 files already have validated L2 holdings for notice and service modules.
- Generate fact patterns that exercise the full decision tree: sufficient vs. defective notice, edge cases (partial compliance, cure provisions, waiver), method-of-service variations.
- Mark all DRAFT/UNFROZEN. Route to Andy (attorney gate — RED).

**Phase 2 — TX notice + TX service**
- Second pilot after CA is frozen. TX is common law jurisdiction with high volume. Good contrast with CA's code-heavy approach.

**Phase 3 — Broaden to other modules**
- After notice + service golden sets are frozen and scorer is working: add procedural defects and retaliation modules.

**LSC/Temple cross-reference layer:** Once CA/TX candidates are drafted, cross-check notice requirements against LawAtlas as a consistency check (not determinative — attorney still establishes ground truth).

---

## What This Survey Unlocks

- Confirmed: no existing dataset to adopt → proceed directly to candidate generation
- LSC/Temple: worth a one-time manual cross-check against our CA/TX notice holdings to confirm currency (5-year-old data)
- LegalBench IRAC structure: adopt as fact-pattern design methodology
- JusticeBench: flag as potential future publication venue for our work

---

*This survey satisfies the Direction B prerequisite step. Next action: generate CA/TX notice + service candidates (~30–50 fact patterns across both states). Requires Cowork execution; attorney gate (RED) for freeze.*

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
