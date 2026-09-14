# A2JRAG -- assessment and recommendation

*Addendum 2026-09-05, s.5, landscape task 1. Written 2026-09-14 from the publisher's announcement and the project
site; the paper itself is served by a client-rendered site that returned no text to Cowork's fetch tool, so the
paper's body was NOT read. Every statement below is sourced to the announcement unless marked. Copyright 2026
Andrew M Cohen. Apache 2.0.*

## What it is

**A method paper with a demonstration, not a dataset or a benchmark.** *A2JRAG: Process-Aware
Retrieval-Augmented Generation for Public Legal Information Systems*, by Tom Martin (CEO, LawDroid; Adjunct
Professor, Suffolk University Law School) and Scheree Gilchrist (Chief Innovation Officer, Legal Aid of North
Carolina), presented at the AIDA2J Workshop at ICAIL 2026 (Singapore, June 8, 2026) and announced June 10, 2026
(LawSites press release, 2026-06-10). The site (a2jrag.org) describes "A2JRAG vs Baseline RAG -- process-aware
retrieval for North Carolina eviction self-help, with an evaluation dashboard."

**The problem it names:** "procedural relevance" -- a RAG system retrieves information that is legally accurate
and topically related but applies to a DIFFERENT STAGE of the legal process (post-judgment appeal information
shown to a tenant who just received a notice). **The mechanism:** a *Procedural State Graph* -- stages,
transitions, contextual factors, guardrails, escalation triggers -- used to estimate the user's stage and
condition retrieval on it. **The demonstration:** North Carolina eviction self-help, A2JRAG vs. baseline RAG,
with an evaluation dashboard. Whether the evaluation item set is published and reusable is NOT stated in the
announcement and could not be confirmed from the site text.

## How it relates to CJaC

Orthogonal layers, not competitors. A2JRAG addresses *which* information to retrieve given procedural stage;
CJaC addresses whether the *rule content* is correct, sourced, and verified. A2JRAG's Procedural State Graph is
structurally close to CJaC's completeness checklists and node dependencies (the demo scenarios already declare
`depends_on_node_ids`; the TX-JUSTICE-COURT node's "what kind of case is this" threshold is a procedural-state
question). A grounded CJaC corpus is a natural retrieval TARGET for an A2JRAG-style front end; A2JRAG is a natural
stage-selection layer over CJaC. Same ecosystem cell as LawDroid's Legal Aid Plugin (workflow layer).

## Feasibility and cost of scoring CJaC against it

- **Blocking question:** is there a public evaluation set? If not, there is nothing to score against and the
  right move is a conversation with the authors, not a run.
- **Jurisdiction mismatch:** the demonstration is North Carolina eviction. CJaC's verified content is California
  eviction (vProof1, frozen) and the federal/TX/CA debt corpus (v1.0). A scoring run on NC items would measure
  CJaC's retrieval format against content it does not have -- meaningless. A re-targeted set (their scoring
  rubric applied to CA eviction items) would measure something real.
- **If a public item set exists and can be re-targeted:** cost is small -- on the order of one lift-ablation
  tranche (~$20-30) plus item-mapping time (Cowork, ~half a session) plus Andy's audit of the scoring rubric
  (~1 h). It would be the first EXTERNAL scoring instrument applied to CJaC output.

## Recommendation

1. **Flag as a candidate external-validation event, conditional.** Condition: a published, reusable item set
   with a stated rubric. Until confirmed, it is a method paper we cite as adjacent work, not a benchmark we run.
2. **Ask the authors** (LawDroid: david@lawdroid.com is the listed media contact; Tom Martin as author) whether
   the evaluation set and rubric are available, and whether a California-eviction re-targeting would interest
   them. Andy's call whether that outreach happens before or after the demo.
3. **Ecosystem map:** place A2JRAG in the workflow/retrieval layer next to the Legal Aid Plugin; CJaC below it
   as verified rule content.

Sources: LawSites press release, June 10, 2026 (lawnext.com/2026/06/context-matters-a2jrag-brings-procedural-awareness-and-better-answers-to-legal-ai.html);
a2jrag.org (site description text only).
