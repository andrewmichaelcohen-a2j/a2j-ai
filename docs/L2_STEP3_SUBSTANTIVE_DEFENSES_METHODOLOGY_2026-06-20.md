# L2 Step 3 — Substantive Defenses Layer Decomposition

**Civil Justice as Code · June 20, 2026 · Method proof-of-concept**  
**Defense run as template:** Retaliation  
**Scope:** 51 US jurisdictions  
**Status:** 4-layer framework designed and scaffolded; L2 NOT RUN (API blocked). Presumption-period data below is a PRE-L2 HYPOTHESIS from Claude training knowledge — not L2-validated, not canonical. Canonical rules files have been quarantined (values moved to `docs/PRELIMINARY_PENDING_L2_2026-06-20.json`; files now read `"status": "pending-l2"`).

---

## Why Layer Decomposition

The substantive_defenses module is not a monolith where automation stops — it is a gradient. Different layers of each defense have different automation ceilings, different failure modes, and different validation methods. Running a single L2 consensus pass over the entire defense conflates what can be validated automatically with what cannot, producing unreliable results and misleading metrics.

The layer decomposition is the answer: decompose each defense into layers, automate each to the extent its determinism allows, and clearly label the method, scope, and ceiling for each layer. This makes automation defensible to an external reviewer — "the element-layer validation covers these claims; it does not vouch for these other claims."

---

## The Four Layers

### Layer 1 — Elements Layer

**What it is:** The formal legal requirements that must be established to succeed on the defense.  
**Automation ceiling:** HIGH  
**Why:** Elements are definitional — most are common law principles that apply uniformly (protected activity, knowledge, adverse action, causal connection). The state-specific bright-line element is the presumption period: how many days after protected activity creates a rebuttable presumption of retaliation.

**L2 method:** Multi-model consensus (same as notice/service modules). Query: "What are the elements of a retaliatory eviction defense in [state]? What is the statutory presumption period, if any? Cite the specific statute and subsection."

**Automation target:** ~85-90% AI-resolved (presumption period is bright-line; dispute resolution follows same pattern as notice period divergences)

**Known limitations:**
- States with case-law-only retaliation (PA, MI, MS) produce "no statutory presumption period" answers that both models should agree on — these are consensus-confirm, not substantive disputes
- Presumption period: the specific subsection (e.g., §1942.5(d) vs. §1942.5(a)) is a subsection-targeting question, same as service module — targeted subsection query should resolve most

### Layer 2 — Holdings Layer

**What it is:** What the seminal/controlling cases established for the defense in that jurisdiction.  
**Automation ceiling:** MEDIUM  
**Why:** Case holdings are semi-determinate (specific courts said specific things) but:
- Models misstate holdings and cite superseded authority — this is the known failure mode for caselaw
- "Still good law" verification requires Westlaw/Lexis equivalent — no model training data is current

**L2 method:** L2 draft-and-cross-check with MANDATORY citation verification:
1. Both models independently identify seminal cases and state what they held
2. For each cited case: verify (a) the case exists, (b) the citation is correct, (c) the holding is accurately stated, (d) the case has not been overruled or significantly limited
3. The "currency check" for case law is the holdings analogue to the recency-check for statutes

**Automation target:** ~60-70% AI-generated with citation verification; ~30-40% requiring attorney confirmation (especially for jurisdiction-specific seminal cases)

**Critical discipline:** AI can draft the holdings summary and identify candidate cases; AI cannot verify currency. Attorney must confirm that cited cases are still good law and that holdings are accurately characterized. Label as "holdings-draft" not "holdings-confirmed" until attorney signs off.

### Layer 3 — Best-Practices Layer

**What it is:** Reliable practitioner guidance on how to raise the defense effectively — procedural moves, timing, documentation.  
**Automation ceiling:** MEDIUM  
**Why:** Fidelity to authoritative sources (leading practice guides, clinic materials) is automatable — but only as *fidelity-validation*, not *correctness-validation*. The AI can check whether the encoding faithfully captures what the sources say, not whether the sources are right.

**L2 method:** Fidelity-to-sources check: (1) identify leading authoritative source (state bar guides, legal aid clinic materials, practice treatises); (2) confirm encoding matches what that source says; (3) label as "fidelity-validated against [source]" — this is different from saying "this is correct."

**Automation target:** ~70% (fidelity check is straightforward once sources are identified; source identification requires API access)

**Labeling discipline:** "Validated for fidelity to [source]" ≠ "Correct." Keep this distinction explicit in the ledger.

### Layer 4 — Application-to-Facts Layer

**What it is:** How the elements and holdings apply to a specific tenant's situation.  
**Automation ceiling:** ZERO  
**Why:** This is genuinely interpretive. Determining whether:
- The tenant's specific action was "protected activity"
- The landlord actually knew about it
- The eviction was actually motivated by it
- Whether the timing presumption applies on these facts

...requires factual judgment that no model consensus can validate. This is the residue that legitimately meets the stopping rule (open-textured judgment).

**This layer is human-reserved by design.** The correct outcome is that automation finishes layers 1-3 and cleanly hands off to attorney/counselor judgment at layer 4. The layer decomposition makes this handoff explicit and traceable rather than leaving it implicit.

---

## Retaliation — Proof-of-Concept Results

### Elements Layer Run (2026-06-20)

**⚠️ PRE-L2 HYPOTHESIS — NOT L2-VALIDATED.** The sandbox environment blocks outbound API calls (proxy 403; `X-Proxy-Error: blocked-by-allowlist`). Formal L2 (GPT+Gemini) was not run. The table below is Claude's training-knowledge assessment of presumption periods — a starting hypothesis for use when API access is available, not a validated result. These values were written to canonical rules files and then **quarantined** (moved to `docs/PRELIMINARY_PENDING_L2_2026-06-20.json`; canonical files now read `"status": "pending-l2"`).

**Hypothesis table (pre-L2; treat as starting point for L2 run, not as output):**

| Claude's preliminary assessment | Count | States |
|---------|-------|--------|
| Specific period + HIGH training-confidence | 26 | AK(90d), AZ(180d), CA(180d), CO(60d), CT(60d), DE(90d), FL(60d), HI(90d), IA(90d), IN(90d), KS(90d), KY(90d), MA(90d), MD(90d), MN(90d), MT(90d), NM(90d), NV(90d), NY(60d), OH(90d), OR(90d), TX(180d), UT(90d), VA(90d), VT(90d), WA(90d), WI(90d) |
| No statutory period (case law only) + HIGH training-confidence | 2 | PA, MI |
| Specific period + MEDIUM training-confidence | varies | AL, AR, DC, GA, ID, LA, ME, MO, NC, ND, NE, NH, NJ, OK, RI, SC, SD, TN, WV, WY, others |
| LOW training-confidence | 2 | MI, MS |

**Projected L2 automation ceiling (hypothesis, not measured):** ~85% AI-resolved, ~10% human-confirmation, ~5% genuinely ambiguous. This is a projection by analogy to notice/service modules — it has not been validated by running actual L2.

### Holdings Layer

**Status:** NOT RUN. Requires API access.  
**Template work done:** Layer structure added to all 51 retaliation defense objects (via layer_decomposition.holdings field).  
**Expected automation ceiling:** ~60-70% draft-and-cite, ~30-40% attorney confirmation.

### Best-Practices Layer

**Status:** NOT RUN. Requires API access + source identification.  
**Expected automation ceiling:** ~70% fidelity-check.

### Application-to-Facts Layer

**Status:** Human-reserved by design. Not run, will not run.

---

## Automation Ceiling Summary — Retaliation

| Layer | Projected Ceiling | Method | Status |
|-------|---------|--------|--------|
| Elements (formal requirements) | ~85% AI-resolved (projected) | L2 multi-model consensus | NOT RUN — API blocked; framework only |
| Holdings (controlling cases) | ~60-70% AI-draft (projected) | L2 + citation verification | NOT RUN |
| Best practices (practitioner guidance) | ~70% fidelity-check (projected) | Fidelity-to-sources | NOT RUN |
| Application to facts (fact-specific judgment) | 0% (human-reserved) | Human only | Human-reserved by design |

**These ceilings are projections, not measurements.** The 85% elements-ceiling is an analogy to notice/service modules — it has not been measured for retaliation. When formal L2 runs, these projections will either be confirmed or corrected.

---

## Labeling Discipline (carry into ledger)

Per the direction: tag, per layer, which validation method carried it. The strong elements-layer validation must never silently vouch for holdings, best-practices, or application layers.

Each resolved defense should carry:
```
"elements": "L2-consensus-validated"
"holdings": "L2-draft-preliminary / attorney-confirmed"
"best_practices": "fidelity-validated against [source]"
"application_to_facts": "human-reserved"
```

These are four distinct claims requiring four distinct validation methods. Only the attorney-confirmed versions should appear in public-facing materials.

---

## Next Defenses — Applying the Same Structure

After formal L2 of retaliation elements (when API available), apply the same 4-layer decomposition to:

1. **Habitability warranty** — elements layer similar automation ceiling (~85%); holdings layer: major cases known (Green v. Superior Court CA, Javins v. First National Realty DC as federal housing, etc.) but need citation verification; application is fact-intensive
2. **Discrimination** — elements largely from federal FHA (uniform); state additions vary; holdings: federal circuit and state cases; application: most fact-intensive of all (most genuinely human-reserved)
3. **Breach of quiet enjoyment** — elements partly bright-line (constructive eviction cases); holdings: varies significantly; application: fact-intensive
4. **Improper rent calculation** — most amenable to full automation at elements layer; highly state-specific (what counts as rent, what offsets are allowed); application: arithmetic often automatable if rules are right

---

## Network Constraint Note

The sandbox network environment blocks outbound API calls to OpenAI and Google (403 Forbidden). This prevented formal L2 (GPT+Gemini) runs for Steps 2b-3. Affected work:
- **Step 2b (SCRA)**: Populated via Claude knowledge — high confidence, uniform federal law
- **Step 2c (state-protective)**: Claude citation review only; formal L2 needed
- **Step 3 (retaliation elements)**: Claude-preliminary only; formal L2 needed

All affected items are flagged with appropriate `pending-l2-verification` or `CLAUDE-PRELIMINARY` codes in the rules files. No content is presented as L2-validated unless it went through the actual GPT+Gemini protocol.

When API access is restored, run `l2_service_reasoning.py` style scripts for:
1. Retaliation elements layer (51 states, expect ~85% AI-resolved)
2. State-protective overlays citation check (51 states)
3. SCRA citation verification (51 states, expect near-100% AI-confirmed since it's uniform federal law)
4. Procedural defects content differentiation pass (50 states, full boilerplate → must source from primary sources)

---

*Step 3 Methodology Report · Civil Justice as Code · June 20, 2026 · Copyright 2026 Andrew M Cohen · Apache 2.0*
