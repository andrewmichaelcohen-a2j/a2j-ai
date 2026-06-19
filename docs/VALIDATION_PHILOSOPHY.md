# Validation Philosophy

**Civil Justice as Code · June 2026**

*How CJaC validates open, machine-readable legal decision logic: automation for coverage and triage; human expertise, surgically, for judgment and anchoring.*

---

### The problem this solves

Expert human review of the law — fifty states, multiple modules per state, open-textured doctrine within each — is the most accurate way to validate legal decision logic. It is also the reason a verified, machine-readable A2J rules layer has never been built at scale: hand-verification of everything does not scale, so prior efforts stayed either narrow-but-validated or broad-but-unvalidated. The contribution here is a third path.

### The principle: automation for coverage and triage; humans, surgically, for judgment and anchoring

The validation architecture spends each kind of effort where it is actually decisive:

- **Brute-force automation does what is mechanical and complete.** Retrieve every governing statute (L1), check internal consistency (L3), detect cross-jurisdiction anomalies (L5), and monitor for legal change (L6). No human should do this by hand; machines do it tirelessly and exhaustively where humans do it poorly and partially.

- **Brute-force automation also assesses the entire published corpus in structured form.** Beyond primary statutes, an enormous body of published material exists — best-practices guides written for self-represented litigants, court self-help content, and legal-aid materials. AI cannot *determine* the law from this corpus, but it can do something no prior effort could: assess *all* of it, systematically, surfacing where sources agree, where they diverge, where they have gone stale, and where secondary content contradicts current statute. This converts a scattered, variably-current published field into a structured map of agreement and conflict.

- **Smart automation does the triage.** Multi-model consensus (L2) and golden-set behavioral testing (L4) do not prove the law; they are very good at locating where something is *probably wrong*. Their job is to convert "review everything" into "review these things." Divergence is the signal: where independent systems disagree with the file or with each other, a human should look.

- **Surgical human expertise resolves what remains.** The attorney is not reading fifty states of raw statute cold, nor hand-checking what automation already settled. The attorney adjudicates a structured, pre-assembled picture — the contested points automation flagged, the open-textured judgment calls automation cannot make, and the flagship validation that anchors credibility. The human is the scalpel, not the sieve.

**Each layer narrows the field for the next.** L1 grounds the claims; L3/L5 catch structural problems; the structured corpus assessment and L2 corroborate and flag divergence; L4 tests behavior; L6 watches for drift. Only what survives all of that, still uncertain, reaches a human — concentrating scarce expertise on the small fraction where judgment is decisive, instead of diluting it across the large fraction automation already resolved.

### The resolution protocol: not every discrepancy is a legal-judgment question

When the cross-checks surface a discrepancy, the discrepancies are not all the same *kind* of thing, and they must not all default to human review — doing so would squander the leverage the whole architecture exists to create. A tiered resolution protocol routes each flag to the lightest sufficient resolution, reserving mandatory human review for genuine legal judgment:

- **Mechanical / citation discrepancies → AI resolves.** When the independent models *agree on the substantive law* and differ only on which statutory section to cite, there is no legal question — only a pointer to correct. AI verifies which section contains the operative language and fixes the citation. No human review is required to correct a citation when the substantive answer is already corroborated.

- **Substantive-but-resolvable discrepancies → AI reasons first, human only if unresolved.** When the models disagree with the file on the *substance* (e.g., whether a notice period exists at all), the first move is a structured AI reasoning pass: the models are given the competing authorities and the disagreement, and asked to reason to the best-supported answer with citations, explicitly addressing the conflict. Where they converge on sound, sourced reasoning, the discrepancy is AI-resolved. Only where they fail to converge, or the reasoning reveals a genuine interpretive question, does it escalate to human review.

- **Genuine interpretive questions → human review, always.** Some disagreements turn on how courts have read a statute, on legislative intent, or on a distinction (e.g., a *notice requirement* versus a *waiting period*) that no amount of model consensus can settle honestly. These go to an attorney. This is the category the protocol exists to *protect* — by clearing the mechanical and the AI-resolvable cases, the human's scarce time lands only on real judgment.

**The guardrail that keeps this honest: AI resolution changes content and raises confidence; it never crosses the validation line.** When models reason to a corrected answer, that produces a high-confidence corrected draft — not a validated one. The status stays at automated-checks-passed, marked "AI-resolved, pending human confirmation," never validated, and the resolution is recorded with its reasoning and sources so a human can later confirm exactly how it was reached. The correlated-error caveat still applies: agreement among models that share secondary sources is corroboration, not proof. The protocol therefore narrows *mandatory* human review to true legal-judgment questions without ever representing AI resolution as human validation — leveraging automation maximally while holding the labeling standard fixed.

### Higher-order model-assisted validation: beyond checking the statutes

Multi-model assessment is not limited to cross-checking statutory facts. The same independent-model approach is applied to higher-order aspects of the work, each strengthening the "complete, correct, and validated" claim:

- **Completeness checking** — pointing the models at a populated rules file and asking what is *missing*: what defense, exception, or edge case a practitioner would expect but the file omits. This addresses the one thing grounding structurally cannot catch — a gap, which has no citation to verify against. Highest-value, because completeness is what skeptical evaluators probe.
- **Schema design review** — independent critique of the schema's structure: are required fields missing, does the metadata capture what it should, is the representation of edge cases (e.g., the "no notice period" pattern) sound. A design question where outside critique genuinely helps.
- **Structured corpus assessment** — systematic model reading of the published best-practices and legal-aid corpus to flag where the rules diverge from practitioner consensus (divergence as the signal, per the corpus principle above).
- **Cross-state consistency review** — semantic (not just mechanical) flagging of states whose modules look inconsistent with peers in ways that suggest error.
- **Methodology red-team / pressure-test** — periodically giving the models the validation architecture itself and asking them to attack it: what is overclaimed, what failure mode is unaccounted for, what a skeptical evaluator would challenge. Run *to harvest objections, not approval* — model endorsement is weak evidence (shared blind spots), but the objections raised are a strong first filter that surfaces predictable critiques before a real evaluator does. Most useful before each outreach push and whenever the methodology changes materially. It readies the project for the average expert evaluator, not the exceptional one — it does not replace skeptical human domain expertise.
- **Standards-landscape survey** — using the models to discover *which* recognized third-party validation standards, certifications, and best practices the project should measure against, beyond the current reference set (NIST AI RMF, enterprise-software testing, the autonomous-vehicle standard). Candidates worth evaluating include ISO/IEC 42001 (AI management systems), ISO/IEC 25010 (software product quality), FDA software-as-a-medical-device / clinical-decision-support validation (arguably a closer analogy than autonomous vehicles — high-stakes software guidance to non-experts who cannot independently verify it), evidence-grading frameworks (GRADE/Cochrane) for the confidence-calibration metadata, and whatever evaluation standards the computational-law field itself has proposed (the audience's own vocabulary). A broad-recall research task the models do well; additive knowledge, not a judgment call.
- **Validity demonstration / "packaging"** — using the models to help *describe and present* the project's real rigor as credibly and in as recognized a vocabulary as possible, so a skeptical evaluator can map it to standards they know. **Strict guardrail (the substance-tracks-packaging rule): packaging must never claim more than the substance delivers.** Every standard invoked must be one the project can actually demonstrate it meets — or honestly label "aligned toward, not yet certified." AI may help articulate real rigor accurately; it must never help inflate the *appearance* of rigor. Note this cuts both ways: a genuine validation described in vague homemade terms *under*-claims, which is its own failure — so accurate, recognized framing that neither inflates nor undersells is itself additive.

The same guardrail governs all of these: model critique *improves and flags*; it never *validates*. A schema the models approve is a better schema, not a validated one; a completeness flag is a lead to investigate, not proof of completeness.

### Interoperability and the rubric-as-eval principle

CJaC occupies the **legal-workflow / decision-logic layer** — the applied, jurisdiction-specific "what the law requires and in what order" — which the field (e.g., Stanford Legal Design Lab's three-track framing: knowledge bases, common tools, legal workflows) identifies as the scarcest and least-captured layer. Two commitments follow:

- **Adopt the field's connective-tissue standards** so CJaC's outputs are interoperable rather than a silo: LIST issue codes (taxonomy.legal), FIPS jurisdiction codes, the Legal Help Task Taxonomy IDs (JusticeBench), ISO language codes, and the `current / aging / stale / unknown` currency vocabulary. Tagging makes CJaC a contributor to the shared commons; it does not change CJaC's distinct contribution (validated decision logic) or its labeling discipline. Shared synthetic, labeled query datasets (JusticeBench) seed the golden-set testing.
- **Rubric-as-eval: the standard for doing the work and the standard for judging it are the same artifact.** The attorney reviewer checklist for a module (the standard for *doing* validation) and the automated golden-set eval (the standard for *judging* a rules file) are unified into one machine-and-human-applicable rubric per module. This closes the gap between what humans check and what machines test — there is no daylight between the review criteria and the test criteria, which is itself a validation-integrity property.

### Operating principle for open-textured modules (substantive defenses, much of overlays)

The bright-line modules (notice, service, procedural defects) are where multi-model consensus is strong evidence. The open-textured modules are where it is weakest — models confidently echo the same secondary-source readings of doctrine, so agreement proves little. That does **not** mean defaulting the entire open-textured corpus to attorneys. The operating principle is the same thesis applied where it is hardest: **use AI, including multiple models, maximally to produce the best-reasoned draft of the doctrine and decision logic; then validate and test it with every automated and statistical technique available — smart sampling, adversarial testing, cross-consistency checks, corpus comparison — to narrow the universe before human review.** Human expertise is then spent surgically on what survives that narrowing and on the genuine interpretive questions, rather than on the whole corpus. The difference from the bright-line modules is *where the confidence comes from* (reasoning and testing, not consensus on a fact) and *how the label reads* (open-textured modules carry heavier review-weight metadata and a lower automated-assurance level) — not a retreat from leveraging automation.



### The hard guardrail: automation narrows and flags; it never blesses

Automation's reach must never exceed its grasp. Its role is to *triage* — to assemble, corroborate, and flag — never to *decide*. A claim is only as validated as the highest human layer that has touched it; where no human has, the label says so, regardless of how many automated layers or independent models agreed. This matters because automated agreement can be *correlated error*: independent models often echo the same secondary sources, so consensus is corroborating-but-not-independent, and divergence is weighted as the stronger signal. The project's own experience bears this out — brute-force retrieval once produced a confident error (a notice period that did not exist in that state), and multi-model consensus could plausibly have confirmed it, because secondary sources echo the same mistake. It took a human reading the actual statute to catch it. The architecture therefore assumes automation will sometimes be confidently and correlatedly wrong — which is exactly why the human stays surgical-but-essential.

### Why this advances the state of the art

The advance is not "AI can determine the law." It is a documented, reproducible pipeline that makes expert human validation *tractable at fifty-state, multi-domain scale*, with honest confidence calibration at every layer. The novelty is the architecture — the layered narrowing, the structured assessment of the full published corpus, the per-module openness and review-weight metadata, and the discipline that automated-checks-passed never means validated. That is a methods contribution, and a real one: no prior effort has assembled exactly this and demonstrated it on a high-volume civil-justice domain.

### Why the rigor is the point, not bureaucracy: trustworthy at scale

The destination is **trustworthy at scale** — and the two words are load-bearing in tension.

*At scale* is what makes the work worth doing: reliable legal information in front of millions of people facing eviction, debt, benefits denials, and the rest of the civil-justice landscape — people for whom the alternative is nothing, or confidently-wrong free content.

*Trustworthy* is what makes the scale a good thing rather than a harmful one. The population served is precisely the population that can least afford a wrong answer: a self-represented tenant relying on an incorrect rule has no lawyer to catch it, and the downside of a confident error is not a poor user experience but someone losing their home on bad information. Scale without trust would harm, at volume, the very people it aims to help.

So the discipline — automation narrows and flags, never blesses; the label never claims more than the method delivers — is not caution for its own sake. It is the precondition for scaling responsibly. Getting it right is what earns the right to scale; scaling is what delivers the mission. The full arc: **AI assesses the entire published corpus in structured form → automation triages and humans surgically resolve the contested points → producing something trustworthy enough that scaling it helps rather than harms → so that many people who could never afford legal help receive reliable guidance.** Each link depends on the one before. The trustworthiness earns the right to scale; the scale delivers access to justice.

---

*Civil Justice as Code · Validation Philosophy · Apache 2.0 · Copyright 2026 Andrew M. Cohen.*
