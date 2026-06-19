# L2 Readiness Assessment — Non-Notice Modules
**Date:** June 18, 2026 · **Author:** Andrew M Cohen (Cowork analysis)  
**Scope:** Service, procedural_defects, overlays (federal + state_protective) across all 51 v2 files  
**Purpose:** Determine which non-notice modules are populated well enough to be meaningful L2 multi-model consensus targets before scheduling a validation run.

*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*

---

## Method

Python scan of all 51 `*_v2.json` files. For each module: checked presence, statute coverage, structural uniformity, and whether a neutral L2 query could produce informative signal (i.e., divergence between model answer and file claim would be meaningful, not just noise from a boilerplate template).

---

## Summary

| Module | L2 ready? | Priority | Blocker (if not ready) |
|--------|-----------|----------|------------------------|
| Service | ✅ Yes | **#1** | None |
| State protective overlays | ⚠️ Viable | #2 (lower) | Module is thin by design; citation verification only |
| Procedural defects | ⛔ No | — | 4-item boilerplate template; needs differentiation pass first |
| Federal overlays (SCRA) | ⛔ No | — | SCRA missing from all 51 files; needs population pass first |

---

## Service Module — Ready ✅

### Data
- **method_rules present:** 51/51 with state-specific statutes
- **All methods statuted:** 51/51
- **Method count:** 50/51 files have 3 methods (personal, substituted, certified_mail or nail_and_mail); FL has 2
- **service_defects:** 51/51 populated

### Quality signal
Statutes are jurisdiction-specific throughout. Representative sample:

| State | personal | substituted | mail/other |
|-------|----------|-------------|------------|
| AZ | §33-1313(A)(1) | §33-1313(A)(2) | §33-1313(A)(3) |
| CO | §13-40-108(1)(a) | §13-40-108(1)(b) | §13-40-108(1)(c) |
| CA | CCP §1162(a)(1) | CCP §1162(a)(2) | CCP §1162(a)(3) |
| AR | §18-60-301; §18-17-703 | §18-60-301 | §18-17-703 |

**Testable hypothesis for L2:** Several states (AL, AK, CT and others) cite the same statute for all 3 service methods rather than method-specific subsections. This could mean (a) the state's service statute covers all methods in a single provision — correct; or (b) the AI pulled the section header rather than the specific subsections — an error L2 would surface. This is exactly the kind of claim L2 is designed to test.

### Proposed L2 query pattern
> "In [state], what are the legally permitted methods for serving a pay-or-quit notice on a residential tenant prior to filing an eviction action? For each permitted method, cite the specific statutory authority."

Models can answer this confidently. Divergence on subsection numbers or method availability would be actionable signal.

### Verdict
**Strongest non-notice L2 candidate.** Real state variation, real statutes to verify, and a specific testable hypothesis. Run this first.

---

## State Protective Overlays — Conditionally Viable ⚠️

### Data
- **Items present:** 51/51 with statutes
- **Item count:** 48/51 files have exactly 2 items; 2 files have 4; 1 file has 3
- **Uniform pattern:** implied warranty of habitability + anti-retaliation statute (all states); CA additionally has AB 1482 just cause + rent cap

### Quality signal
The 2-item pattern is real and grounded — these are genuine statutory protections that exist in every state. Statutes are state-specific. The module is accurate as far as it goes.

**The limitation is coverage, not correctness.** The module makes no attempt to capture just-cause protections in cities like NYC, Chicago, or Seattle, or state-level rent stabilization beyond CA. This is a known scope decision (local overlays were explicitly de-scoped in the overlays cleanup pass). L2 can verify what's claimed but cannot flag what's absent.

### Proposed L2 query pattern (if run)
> "Does [state] have a statutory implied warranty of habitability for residential tenants? What is the governing statute?"  
> "Does [state] have a landlord anti-retaliation statute protecting tenants from eviction for asserting housing rights? What is the governing statute?"

Both are high-confidence queries where models are reliable. This would be a citation verification pass, not a content completeness check.

### Verdict
**Viable for citation verification; lower priority than service.** The more impactful investment here may be a coverage-expansion pass (adding SCRA, just-cause cities, rent stabilization where applicable) rather than L2 on the existing thin base.

---

## Procedural Defects — Not Ready ⛔

### Data
- **Items present:** 51/51 with statutes
- **Item count:** 50/51 files have exactly 4 defects; 1 file has 5

### Critical finding: boilerplate template
The same 4 defect types appear in virtually every file:

| Defect | Count (of 51) |
|--------|--------------|
| `complaint_filed_before_notice_period_expired` | 51 |
| `wrong_court` | 51 |
| `failure_to_attach_lease_or_notice_to_complaint` | 51 |
| `summons_improperly_issued_or_served` | 51 |

These are universal procedural defects that apply in every jurisdiction. The statutes attached to them are state-specific, but the defects themselves are a template. The module was populated with a common-floor content set, not jurisdiction-differentiated doctrine.

### Why L2 would be uninformative
L2 queries models neutrally on jurisdiction-specific procedural defects. Models would return approximately these same 4 universal defects — confirming the template, not validating jurisdiction-specific claims. Agreement would be near-certain and meaningless. L2 produces signal from divergence between models and file claims; when the file claims are boilerplate, there is nothing to diverge on.

### What the module needs first
A differentiation pass to add jurisdiction-specific procedural defects: state-specific filing fee requirements, mandatory form statutes, local court rules that invalidate complaints on technical grounds, timing rules for summons issuance, verification/signature requirements on complaints, etc. Once those are encoded, L2 becomes valuable.

### Verdict
**Skip for L2 now. Needs a jurisdiction-differentiation content pass first.**

---

## Federal Overlays (SCRA) — Not Ready ⛔

### Data
- **Federal items present:** 51/51 files, all with exactly 1 item: CARES Act §4024
- **SCRA present:** 0/51 files

### Finding
All 51 files have identical CARES Act §4024 content (expired 2021 moratorium). This is historically accurate and appropriate to retain as reference, but it is not current actionable law.

**SCRA is completely absent from all 51 files.** The Servicemembers Civil Relief Act is the universal federal eviction defense that matters in current practice: active-duty servicemembers are entitled to a 90-day stay, courts must inquire about military status, and landlords must comply with federal notice requirements regardless of state law. This belongs in every file and is missing from all of them.

### What the module needs first
An SCRA population pass — a single well-structured federal item added to all 51 files with the operative provisions (50 U.S.C. §§3951–3953), the trigger conditions (active duty + notice to landlord), and the protections (court stay, income protection, lease termination rights). This is uniform federal law, so the content is identical across all 51 states; the pass itself is straightforward.

Once SCRA is in, a focused L2 query ("What federal protections apply to active-duty servicemembers facing eviction?") would verify that each file correctly captures the federal overlay before state-specific overlays are layered on.

### Verdict
**Needs SCRA population pass first. Not an L2 target until SCRA is present.**

---

## Recommended Sequencing

### Immediate (pre-L2 work already done)
- Notice module: L2 complete (41 CONFIRM, 5 AI-resolved, 5 L7, 3 citation-review)

### Next: Service L2
The runner pattern from `l2_phase2_runner.py` can be adapted. New query targets the service module specifically. Likely to be a cleaner run than notice — service statutes are more discrete and model-verifiable.

### After service L2
**Option A — More L2:** State protective overlays citation verification (quick, low-risk).  
**Option B — Content passes:** SCRA population (all 51 files, uniform content) + procedural defects differentiation (harder, jurisdiction-specific research). These make the remaining modules L2-ready and more valuable.

**Option B is likely higher leverage.** The service and notice modules will be the most-used in a triage tool; the federal overlays and procedural defects modules are the next highest-value additions for real-world defense coverage. Getting SCRA into all 51 files closes a significant gap before any further L2 passes.

---

## Open Items After This Assessment

| Item | Type | Notes |
|------|------|-------|
| Run L2 on service module | Validation | Design query, build runner, ~$1 budget estimate |
| SCRA population pass | Content | Uniform federal content, all 51 files — low effort, high value |
| Procedural defects differentiation | Content | Jurisdiction-specific research needed; significant lift |
| State protective expansion | Content | Local just-cause cities, rent stabilization; out of scope for v1 |

---

*L2 Module Readiness Assessment · June 18, 2026 · Civil Justice as Code · Copyright 2026 Andrew M Cohen · Apache 2.0*
