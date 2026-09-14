# Ecosystem / puzzle-map dataset -- one page, for the messaging build

*Addendum 2026-09-05, s.5, landscape task 2. Cowork supplies names and facts; Claude drafts the visual. Each row
carries its verification status: **V** = verified by Cowork from a primary or publisher source this session or
earlier in the record; **D** = as stated in Andy's directive, not independently re-verified this session; **K** =
general knowledge, unverified here. Written 2026-09-14. Copyright 2026 Andrew M Cohen. Apache 2.0.*

| Layer (top = closest to the person) | Named parties | Role | Status |
|---|---|---|---|
| Pro se delivery / front doors | Courtroom5 | pro-se litigant guidance product | K |
| Intake (upstream) | Spot (Suffolk LIT Lab issue-spotter) | classifies a person's problem into legal issue codes (LIST taxonomy) | K |
| Workflow / retrieval layer | LawDroid Legal Aid Plugin (2026-05-20, open-source, a Claude for Legal plugin for civil legal aid, court self-help, public-interest providers) | orchestration over model + content | V (LawSites 2026-06-10 describes it as "a free and open-source Claude for Legal plugin"; date D) |
| Workflow / retrieval layer | A2JRAG (LawDroid + LANC Legal Innovation Lab; ICAIL AIDA2J, June 8, 2026) | process-aware retrieval; Procedural State Graph; NC eviction demo | V (announcement) |
| **Verified rule content -- CJaC's layer** | **Civil Justice as Code (this repo)**: eviction line (CA, vProof1) and debt track (federal spine + TX + CA, debt-demo-v1.0) | machine-readable, source-pinned, adversarially tested, attorney-certified rules with completeness checklists and tier labels | V (this record) |
| Model platforms | Claude for Legal (Anthropic, 2026-05-12: commercial practice areas plus clinic/student tools; attorney-responsibility disclaimer); other frontier models (OpenAI, Google) used in CJaC's tri-model corroboration | reasoning + generation | D (Claude for Legal date/scope per directive); V (models used, this record) |
| Primary sources | Cornell LII (U.S. Code, CFR, state regulations, Supreme Court), CourtListener / Free Law Project (case law, citation resolution -- used 2026-09-14), eCFR, uscode.house.gov, state legislatures (leginfo, statutes.capitol.texas.gov), Judicial Council of California | what CJaC pins to and the checker fetches | V (this record) |
| Standards | Legal Hackers Consortium / JusticeBench (evaluation alignment -- see docs/JUSTICEBENCH_ALIGNMENT_SPEC.md); LIST/NSMI issue taxonomy (via Spot) | shared evaluation and taxonomy | V (repo docs) / K |
| Downstream assembly + filing | Suffolk LIT Lab Assembly Line (Docassemble form interviews); court e-filing (Tyler/Odyssey, state portals) | turning an answer into a filed document | K |
| Regulatory venues | Utah Office of Legal Services Innovation (sandbox); Arizona Alternative Business Structure / Legal Paraprofessional programs | where non-lawyer and AI-delivered legal help is lawfully authorized | K |
| Legal frame for the whole map | *United States v. Heppner* (S.D.N.Y., Rakoff, J., Feb. 17, 2026): consumer-AI chats with Claude were not privileged (Claude "is not an attorney"; third-party platform terms; no work product) | reinforces CJaC's information-not-advice posture and why grounded, tier-labeled information matters | V (multiple firm summaries and Harvard Law Review blog, 2026-03; opinion date Feb. 17, 2026) |

**CJaC's cell, stated for the visual:** the verified-content layer between primary sources and the
workflow/model layers -- the only layer whose output carries a source pin, a verification date, a tier label, and
an attorney's certification of process. Everything above it consumes it; everything below it is what it cites.

**Landscape note additions (per Addendum s.5, bullet 3), recorded in the state of record:** Claude for Legal
(2026-05-12; commercial practice areas + clinic/student tools; attorney-responsibility disclaimer) [D]; LawDroid
Legal Aid Plugin (2026-05-20; open-source; workflow layer) [V/D]; *U.S. v. Heppner* (S.D.N.Y. 2026; no privilege in
consumer AI chats; reinforces information-not-advice) [V].
