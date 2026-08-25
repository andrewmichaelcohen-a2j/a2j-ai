# CJaC — Open Questions & Known Limitations

*This document is published deliberately. CJaC's credibility rests on validation, and validation means testing the things that could prove us wrong — including our own assumptions. Each open question below states why it matters, what we currently know, and the planned test. We pre-register our doubts the way we pre-register our ground truth: before the results come in. Questions are updated as tests complete; nothing is removed, only resolved.*

**Status date:** 2026-07-24 · Maintained alongside `DIRECTION_D_ROADMAP.md` and the validation ledger.

---

## 1. The intake gap: our validation currently measures the upper bound

Our golden-set testing scores encoded rules against *expert-structured* fact patterns ("tenant resided 18 months; 30-day notice served April 28"). Real unrepresented people present *messy narratives*: buried facts, omissions, folk-legal vocabulary, and no knowledge of which facts are dispositive. Recent research (Lou & Shin, *Legal Reasoning Is Not Lawyering*, arXiv:2606.23716, 2026) argues persuasively that expert-preprocessed benchmarks measure the upper bound of AI legal performance, while access to justice depends on the lower bound — and that models degrade under exactly these conditions, including failing to ask for missing facts rather than guessing.

**Why it matters:** CJaC's validated perimeter currently begins *after* fact extraction. The hardest step for a pro se user sits outside it.
**What we have:** a structural hypothesis — because CJaC's completeness checklists enumerate the dispositive facts for every rule, a CJaC-grounded system can *know what it doesn't know* and elicit missing facts rather than guess. This is a designed answer to the documented abstention problem. It is untested.
**Planned test:** the lower-bound test track (Direction E): Tier 1 — frozen fact patterns rewritten as realistic pro se narratives, scored end-to-end; Tier 2 — an interactive simulated-user harness scoring both fact *elicitation* (deterministic checklist coverage) and outcome accuracy. Until these run, our published scores should be read as upper-bound results, and deployment is sequenced through trained intermediaries (legal-aid and court workers) who perform fact extraction.

## 2. The delivery chain: validated code is necessary, not sufficient

Impact at scale requires four links: (1) people in legal crisis use AI tools; (2) the validated rules are actually invoked in their session; (3) accurate information changes what people do; (4) what people do changes outcomes. Link 1 is empirically strong. Link 2 depends substantially on distribution decisions made by AI platforms and deploying institutions, not by CJaC. Links 3–4 face a sobering fact: most evictions end in default regardless of the merits — information accuracy alone does not file an answer by the deadline.

**Why it matters:** "accurate encoded law" and "justice delivered to millions" are separated by three links we do not control.
**What we have:** the counterfactual argument (millions already ask AI legal questions; raising the accuracy floor of that existing channel has standalone value), and a design commitment that rules carry actionable next-steps (what to file, by when) — which is deterministic, encodable law — not just classifications.
**Planned test:** a mediated deployment pilot with a legal-aid organization measuring concrete endpoints (triage time, defect-spot rate vs. staff baseline, answer-filing rates). See `PILOT_DESIGN_BAYLEGAL_DRAFT.md`. The delivery assumption is a hypothesis until this produces data.

## 3. The deterministic perimeter is unmeasured

CJaC's thesis applies where legal requirements are deterministic. We assert — plausibly but without measurement — that deterministic rules decide "many" high-volume poverty-law cases. What fraction of actually case-dispositive questions in eviction is deterministic (notice defects, day counts, service) versus discretionary (habitability disputes, retaliation fact questions, judicial discretion, settlement dynamics)?

**Why it matters:** the perimeter bounds the impact claim, and answers near the boundary carry a specific risk: a *partially* right answer can mislead ("your notice is defective" is true; "the landlord can serve a corrected notice tomorrow" is also true — a user told only the first misjudges their position).
**What we have:** an exclusion discipline (open-textured questions are excluded from ground truth rather than guessed — see the v0.3 freeze record) and a design rule that encodings should carry consequences and next-steps.
**Planned test:** a defect-prevalence study from published case data and legal-aid case records — a well-scoped clinic research project — to measure what share of dispositive issues falls inside the encodable perimeter.

## 4. Attorney capacity is the scaling constraint

Named-attorney validation is CJaC's trust core and its bottleneck. Fifty-one jurisdictions times multiple practice areas requires attorney review capacity that one founder cannot supply, and coverage risk is real: who signs for jurisdictions with no volunteer attorney?

**What we have:** two levers. First, the clinic-partnership model (law students and supervising faculty drafting and reviewing under the project's protocols) — promising, unproven until the first clinic completes a freeze cycle. Second, automation leverage: everything up to the ratification moment (drafting, citation verification, consensus review, regression testing, statute monitoring, triage) is progressively automated, with the explicit goal of driving down **attorney-minutes per validated rule** until part-time volunteer review is sufficient per jurisdiction. We track that metric. What automation cannot absorb, by design, is the ratification judgment itself — in our first validation cycle, AI consensus correctly flagged disagreements, but determining which side was legally right required an attorney.
**Open risk we monitor:** tireless AI generation with fixed ratification capacity grows an unratified-proposal queue rather than validated coverage; automation therefore includes triage (ranking what most deserves attorney minutes) and a queue-health metric, not just generation.

## 5. Maintenance and staleness at scale

Law changes constantly; unmaintained "validated" code is worse than no code, because it carries false authority. Maintenance burden grows combinatorially with jurisdictions, practice areas, and municipal overlays.

**What we have:** currency flags and freshness monitoring in the process today; automated statute-and-case watch on the near roadmap (the watchlist generates itself from the statutory pins every rule already carries).
**Commitments this implies (adopted):** every published module carries a visible "last verified" date; each module defines a freshness SLA; and the project maintains a *decommissioning rule* — encoded law that can no longer be maintained to its SLA is withdrawn, not left standing.

## 6. Integration fidelity: validated rules ≠ faithful model use

A model given correct rules can still misapply them — our own first validation cycle included misses caused by correctly encoded rules that were not wired to the defect being evaluated. Each deployment platform's integration needs its own testing; a rules file's quality does not transfer automatically.

**Planned tests:** per-platform integration test suites; the recurring "lift" ablation (same items scored with and without the rules) as a standing measure of whether the rules are actually improving model output on each platform.

## 7. The information/advice line under interactive use

CJaC publishes legal *information* — what the law generally requires. Interactively applying rules to one person's specific facts inside a conversation sits closer to the legal-advice line than static publishing does, and unauthorized-practice rules vary by state. The named-attorney feature, our trust mechanism, could also attract novel liability theories.

**What we have:** the design rule that no automated process advises a client, and mediated deployment (trained staff between the system and the client) as the current model.
**Planned step:** formal review with legal-ethics scholars before any direct-to-public interactive deployment; published guidance for deploying organizations.

## 8. Dual-use symmetry

Validated notice law helps landlords perfect notices as much as it helps tenants spot defects; defective-notice defenses will decay as landlord compliance improves. We think the net effect favors tenants — compliance means statutory notice periods are actually honored, and the current information asymmetry burdens tenants — but we state the tradeoff rather than hide it.

## 9. Sustainability

"No one has a financial incentive to build this" is the mission's strength and its funding weakness: no one has a financial incentive to maintain it in year five either. The long-term answer is institutional stewardship (a law school, bar foundation, or A2J institution adopting the project). That home is being sought and is not yet secured.

## 10. Does the methodology extend beyond deterministic law?

Everything validated so far sits in the most deterministic band of eviction law — deliberately. But subjective law is a gradient, not a wall, and the project's reach depends on how far down it the methodology extends. We use a three-band taxonomy. **Band 1 — deterministic:** notice periods, day counts, service methods, statutory thresholds; outcomes are freezable ground truth. Proven. **Band 2 — structured-subjective:** habitability, retaliation, waiver — questions whose *application* is judgment but whose *structure* is lookup-able law (elements, burdens of proof, statutory presumptions like Civ. Code §1942.5's 180-day retaliation presumption, evidence relevant to each element). **Band 3 — genuinely discretionary:** relief from forfeiture, credibility, judicial discretion; here CJaC's only honest product is the boundary marker itself — "this is a judgment call; here is what courts weigh; this is where you need a human."

**Why it matters:** Band 2 is where the most contested eviction defenses actually live; if the methodology stops at Band 1, the impact ceiling is materially lower. And Band 2 breaks our current validation method: outcomes cannot be frozen for questions on which reasonable attorneys differ — frozen outcomes there would be fake precision.
**What we have:** a hypothesis we expect to prove in some form — that Band 2 is reachable by changing what ground truth *is*: from outcome-correctness to **process-correctness** (did the system identify the correct elements, allocate the burden correctly, apply the presumption, assemble the evidence checklist — and *refuse to predict the outcome*). This reuses the abstention-credit scoring already specified for our lower-bound tests, and it generalizes the exclusion discipline we already practice (open-textured questions are excluded from outcome ground truth rather than guessed). Band 3 is not a target beyond boundary encoding, ever.
**Planned test:** a Band 2 proof cycle encoding the structure of one defense — candidate: California retaliation under §1942.5, seeded by the multi-state retaliation-elements corpus already collected in the project's review queue — with process-correctness golden sets frozen and scored under the standard discipline. Until that cycle runs, all published validation claims apply to Band 1 only, and we say so.



## 11. Is the measurement instrument itself validated?

Every number we publish is produced by our scoring infrastructure — and an instrument held to a lower standard than what it measures is a hidden assumption. A subtle scorer bug (mis-parsed outcomes, miscomputed agreement statistics, mishandled held-out flags) would corrupt the validation record silently while every process around it looked clean.

**What we have:** unit and regression tests on the harness; provenance hashes tying every published score to exact inputs; and, now underway, an engineering-hardening program: CI-enforced integrity checks on all frozen artifacts, a known-answer calibration suite proving the scorer reports correctly in every branch (including forced-disagreement and malformed-output cases), a rules/golden-set coverage matrix, and a mutation-testing pilot measuring whether our test sets would actually *detect* mis-encoded law.
**Planned step:** independent engineering review of the scorer by an external reviewer — the same courtesy we extend to the law, extended to the instrument.

---

*If you can sharpen any of these questions — or think we've missed one — open an issue. Being shown wrong early is the cheapest way to be right later.*

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
