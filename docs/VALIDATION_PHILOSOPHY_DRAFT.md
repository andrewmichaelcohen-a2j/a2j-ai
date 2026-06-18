# Validation Philosophy — draft section

**For insertion into `PROJECT_PLAN.md` (next pass), and to seed the deck and working paper.**
*Drafted June 16, 2026.*

---

## Validation Philosophy

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

*Draft Validation Philosophy · June 16, 2026 · For the Plan, deck, and working paper. Captures the automation-for-coverage / surgical-human / never-blesses architecture and the trustworthy-at-scale → A2J through-line.*
