# CJaC Daily Changelog

*GREEN action log — every autonomous change Cowork makes is recorded here. Andy audits without having watched. Format: date · what changed · test/verification.*

## 2026-09-02, round 35 (runner-only: fix null-url citation crash + generalize markup-diagnostic capture)

**What changed since round 34: RUNNER-ONLY, no content change** (one-variable rule). Andy ran the first-ever
full 19-node demo-corpus live run this round, after resolving a transient Anthropic credit-balance issue
(unrelated to this project's code -- his account ran out of API credit mid-run once, and hit a brief 529
overload once; both are noise, not bugs, and needed no fix). The real run (`run_20260902T082021Z.json`)
surfaced two genuine runner-level problems, diagnosed from the run JSON plus a direct read of the affected
nodes' current content.

**Bug 1 -- null-url citation crash.** Four `derived_from` entries across 3 nodes
(`FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b`, `FDCPA-FALSE-DECEPTIVE-CATALOG-1692e` x2) cite general legal
doctrine ("judicial gloss") rather than a single pinpoint source, and were built with `url: null` by design
-- there's no one page a mechanical fetch could check. Every mode (`--live`, `--dry-run`, `--replay`) fell
through `verify_citation` to the live-fetch branch for these and crashed with `"Invalid URL 'None': No
scheme supplied"`, which surfaced as a citation-check failure even though nothing was actually wrong.
Fixed: `verify_citation` now returns `verified: None` ("not applicable to mechanical verification") for a
falsy url, and the node-level `all_citations_verified` aggregation now tolerates `None` the same way
`clean_pass` already did (`is not False` rather than requiring strict `True`) -- so a doctrine citation no
longer blocks a node's citation-verification status, while a citation that DOES have a url and genuinely
fails to verify still blocks exactly as before. Verified end-to-end via `--dry-run` against the real
`FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b` node: citation-verification went from a crash to 100.0% with no other
change. New calibration fixture `CAL-10-null-url-judicial-gloss-citation` regression-guards this.

**Bug 2 -- diagnostic-capture gap on near-zero-prefix breaks.** Several new citation failures this run
(Cornell LII's `law.cornell.edu/uscode/text/15/1692a`, three `leginfo.legislature.ca.gov` CA sections) show
the same "high word-overlap, low prefix-match" signature as the round-23/28 markup-normalization bugs, but
`_raw_context_at_break`'s existing 20-character-minimum-prefix requirement meant NONE of them captured the
raw HTML needed to actually diagnose the pattern (most of these breaks have `longest_matching_prefix_chars`
under 20). This is a diagnostics-only fix (does not touch `verified` logic, cannot mask a real mismatch):
when the matched prefix is too short to build a reliable anchor, fall back to anchoring on the needle's
first 4+-letter word instead, so the raw markup context is captured on Andy's NEXT live run rather than
guessing at a fourth normalization rule without evidence.

**Deferred, correctly identified as CONTENT (not runner) bugs -- queued for round 36:** three
`quoted_text` fields (`TX-HOMESTEAD-EXEMPTION`'s 26 U.S.C. 6321 citation, `TX-EXEMPT-PERSONAL-PROPERTY`'s
Tex. Prop. Code 42.005 citation, `CA-CIVIL-ANSWER-DEADLINE`'s CCP 415.20/415.40/415.50 citation) have a
citation label baked into the quoted text itself (e.g. `"26 U.S.C. § 6321: 'If any person liable...'"`),
which will never appear verbatim on the actual source page -- confirmed via a corpus-wide grep sweep that
found exactly these 3 instances and no others. Also still unread: 16 of the 19 nodes' Stage B adversarial
checks parsed successfully and surfaced 2-3 candidate gaps each (40+ individual findings) -- not yet
triaged, given the volume, to keep this round's runner change isolated per the one-variable rule.

**Verification:** `validate_debt_schema.py` and `check_frozen_artifacts.py` PASS unchanged.
`check_corroboration_calibration.py` PASS with the new 10-fixture set (was 9) -- all metric assertions
recomputed and confirmed (`stage_a_grounded_agreement_rate`, `citation_verification_rate`, and
`stage_b_parse_success_rate` each moved from 8/9=88.9% to 9/10=90.0%; `full_pipeline_clean_pass_rate` moved
from 5/9=55.6% to 6/10=60.0%; `internal_gate_met` remains False). Patch built and independently verified via
`git am --3way` against a fresh clone of real origin before delivery.

## 2026-09-01, round 34 (content-only: fix 3 genuine gaps from Andy's live re-run confirming round 33, run_20260901T184005Z)

**What changed since round 33:** content-only, no runner/pipeline change. Andy re-ran the smoke step live
immediately after applying round 33, against the same 3 nodes. Good confirmation first: Stage A
grounded-agreement reached 100% this run (up from 66.7% two runs ago) -- the round-33 title-phrasing fix on
`FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6` is fully working, and all 3 models now derive from the corrected
content cleanly. All 6 of that node's citations verified too. All 3 nodes were still FLAGGED, but for
different, more granular reasons than before -- diagnosed by reading the run JSON directly.

**`CA-SOL-WRITTEN-CONTRACT-DEBT` -- 3 genuine adversarial findings, all read from a fully-parsed Stage B
response:**

1. **SCRA military-service tolling not screened.** 50 U.S.C. § 3936(a) excludes a servicemember's entire
period of active duty from any limitations period -- a full tolling that can add years, not encoded
anywhere in this node despite California's large military population. Added as a new threshold
checklist question and `scra_military_tolling_note`, verified via live fetch of the official U.S. Code.

2. **CCP § 361 choice-of-law framing bug.** The existing `choice_of_law_note` and checklist item wrongly
required the contract to designate the other state's law before the borrowing statute could apply. Re-read
against this node's own already-verified § 361 `quoted_text` (no fresh fetch needed -- leginfo.legislature.ca.gov
continues to return unusable content to this session's fetch tool, a known limitation): the statute requires
only that the claim arose in another state and is already time-barred there. No choice-of-law clause is
required. Fixed both the note and the checklist item.

3. **Accrual-date checklist framing bug.** The checklist defaulted to "date of last payment" as the accrual
date, contradicting the `accrual` note's own hedge that this is an unresolved fact question. On a revolving
account, breach/default can postdate the last payment by weeks or months. Reworded the checklist item and
strengthened the `accrual` note to stop implying last-payment date is a reliable proxy.

**`FDCPA-REGF-CALL-FREQUENCY-1006.14b` -- 2 of 3 genuine findings fixed, read from a truncated (unparsed)
Stage B response per this project's standing practice of not discarding legible partial text:**

1. **Cease-communication and § 1692c(a) restrictions not screened.** Staying under the 7-in-7 count says
nothing about whether individual calls violate 15 U.S.C. § 1692c(a) (inconvenient time/place -- presumptively
before 8am/after 9pm; known-prohibited workplace; known attorney representation) or, most sharply, § 1692c(c)
(a written cease-communication notice, after which nearly all further contact is independently unlawful
regardless of count). Added both citations (verified via live U.S. Code fetch), a new
`cease_communication_and_representation_note`, and 2 checklist items.

2. **Business/commercial debt gap -- already addressed, not duplicated.** The third Stage B finding (debt-type
not screened) is already covered by round 33's additions to the shared `FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6`
gate node (the new 1692a(5) checklist item there). Clarified this node's `fdcpa_coverage_threshold_note` to
point explicitly at that screening rather than re-deriving it inline.

**Diagnosed but explicitly NOT fixed this round (flagged for a future runner-only round, per the
one-variable rule -- content and runner changes never land together):**

- `FDCPA-REGF-CALL-FREQUENCY-1006.14b`'s newly-added 15 U.S.C. § 1692c(b) citation (added in round 33)
failed live citation-check this run with `word_overlap_ratio: 1.0` but `longest_matching_prefix_chars: 32`,
breaking right after "except as provided in section 1692b of". The raw HTML diagnostics show the break lands
inside a `<span onclick="openDocument('1692b', ...)">` cross-reference link wrapping the "1692b" citation
mid-sentence -- the same family of markup-normalization bug as the round-23 nested-span and round-28
tag-boundary fixes, but on a linked inline cross-reference rather than a paragraph marker. The quoted text
itself is correct (confirmed by the 1.0 word-overlap); this is a checker false negative, not a content bug.
Queued as a runner-fix candidate.
- `FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6`'s Stage B call returned an empty completion (`_stop_reason:
max_tokens` on the first call, `empty_completion` on retry) with no gaps captured. Possible cause: this
node's content has grown substantially over rounds 31/33 (new derived_from entries, logic notes), which may
be pushing the Stage B prompt near its output budget. Worth investigating node-size vs. Stage-B-token-budget
as a runner concern in a future round, separate from any content change.

**Verification:** `validate_debt_schema.py`, `check_frozen_artifacts.py`, and
`check_corroboration_calibration.py` all PASS. Patch built and independently verified via `git am --3way`
against a fresh clone of real origin, chained through rounds 27-34, before delivery.

## 2026-09-01, round 33 (content-only: fix 3 genuine gaps from Andy's second live smoke run, run_20260901T181628Z)

**What changed since round 32:** content-only, no runner/pipeline change. Andy ran the smoke step of the
smoke-then-full protocol a second time, now against 3 nodes (the coverage-threshold gate node was
correctly queued this time). All 3 nodes FLAGGED and Stage A agreement dropped to 66.7% -- diagnosed by
reading the run JSON directly rather than reacting to the headline number, per standing discipline.

**Root cause 1 -- title-phrasing bug on `FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6` (drove the Stage A drop,
NOT a real legal disagreement):** the node's title used a case-caption-style construction ("Shared Band-1
gate node: is this entity a 'debt collector'..."). Comparing all 3 models' raw Stage A derivation text
showed 2 of 3 (gpt-5.5, gemini-2.5-pro) misread the title's leading phrase as if it named an actual party
needing classification from missing facts, producing `grounded: false` and a mechanically-skipped judge.
This is a SECOND confirmed instance of the same bug category documented for
`FDCPA-VALIDATION-NOTICE-1692g` in round 20/21. Fix: reworded the title to plain topical/definitional
phrasing with no colon-based "X: is this Y a Z?" construction: "FDCPA/Regulation F coverage threshold --
statutory definitions of 'debt collector,' 'debt,' and 'creditor' under 15 U.S.C. 1692a".

**Root cause 2 -- `FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6`'s Henson v. Santander citation newly blocked:**
`supreme.justia.com` now returns HTTP 403 (a new addition to the known-blocked-sites list alongside
mass.gov, courts.ca.gov, and AZ leg.gov). Re-pinned the URL to Cornell LII
(`law.cornell.edu/supremecourt/text/16-349`), an equally authoritative source-tier-A mirror. While
re-verifying the quote against the fresh fetch, caught and fixed an independent, pre-existing dropped-words
error in the node's `quoted_text` ("but also acts as a third party collection agent" was missing "because
it regularly" before "acts").

**Content additions to `FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6`:** added `derived_from` entries for
15 U.S.C. § 1692a(5) ("debt" definition), § 1692a(3) ("consumer" definition), and Obduskey v. McCarthy &
Holthus LLP, 587 U.S. ___ (2019) (nonjudicial foreclosure is outside "debt collector" except for the
narrow §1692f(6) purpose, and does not grant blanket immunity) -- all verified via live fetch of
uscode.house.gov / Cornell LII. Added 3 new logic notes and 3 completeness_checklist items covering what
counts as "the debt" being collected, the security-interest-enforcement carve-out's narrow scope, and the
F(iii) actual-obtained-interest clarification.

**Fix 3 -- `FDCPA-REGF-CALL-FREQUENCY-1006.14b`'s exclusion-scope bug:** the node's `exclusions_from_count`
previously implied the (b)(3) exclusions (consent, not-connected, third-party) applied only to the raw
>7-call count. Verified via live eCFR fetch of 12 C.F.R. § 1006.14(b)(3): the chapeau excludes these calls
from "the telephone call frequencies described in paragraph (b)(2)(i)," and (b)(2)(i) itself defines BOTH
the raw-count test (A) and the post-conversation 7-day cooldown test (B) -- so the exclusions apply to
both. Fixed `determination` and `exclusions_from_count` accordingly. Also added a
`third_party_communication_note` (verified via 15 U.S.C. §§ 1692c(b), 1692b): clearing this node's 7-in-7
count does NOT clear the separate, generally-applicable prohibition on communicating with third parties
about the debt at all (narrow location-information exception: at most one call absent request, and the
collector may not even state a debt is owed). Added 2 completeness_checklist items.

**Explicitly deferred, not encoded (per standing discipline against encoding unverified claims):** the
"not connected" exclusion's precise scope (whether an unanswered/voicemail call counts as "connected," and
therefore still counts toward the limits) -- a live fetch of CFPB's Official Interpretation page
(consumerfinance.gov/rules-policy/regulations/1006/interp-14/) returned no substantive matching content
this session (likely JS-rendered commentary not captured by the fetch tool), so Stage B's specific claim
about voicemail/unanswered calls is flagged as UNVERIFIED in the node rather than asserted as settled.
Also still deferred from round 32: California's Rosenthal Act state-overlay addition, blocked on repeated
`leginfo.legislature.ca.gov` timeouts.

**Verification:** `validate_debt_schema.py`, `check_frozen_artifacts.py`, and
`check_corroboration_calibration.py` all PASS. Patch built and independently verified via `git am --3way`
against a fresh clone of real origin, chained through rounds 27-33, before delivery.

## 2026-09-01, round 32 (content-only: fix 2 genuine gaps found in Andy's first live smoke run since rounds 27-31)

**What changed since round 31:** content-only, no runner/pipeline change. Andy ran the smoke-then-full
protocol's smoke step live (`run_20260901T111027Z.json`, 2 nodes: `FDCPA-REGF-CALL-FREQUENCY-1006.14b`,
`CA-SOL-WRITTEN-CONTRACT-DEBT`) and shared the output. Diagnosis first, per standing discipline: the
run's headline `citation_verification_rate: 0.0%` looked alarming but is a binary per-node metric --
the real picture was 10 of 13 individual citations verified fine (77%), including both citations rounds
27/28 were built to fix (eCFR § 1006.14(b), the new § 1692a(6) coverage text), confirming those fixes
are working live. Of the 3 failing citations: 2 (mass.gov's 940 CMR download, courts.ca.gov's emergency
rule PDF) are HTTP 403 site-level bot-blocks, not a content or checker bug -- flagged as HORIZON, not
chased this round. The 3rd was the useful one.

**Fix 1 -- CA-SOL-WRITTEN-CONTRACT-DEBT's 11 U.S.C. § 524(a) citation, root-caused via the run's own
diagnostics** (`http_status: 200`, `word_overlap_ratio: 1.0`, but `longest_matching_prefix_chars: 39`,
breaking immediately after "this title-"): a full live fetch of the official uscode.house.gov page
confirmed the official text reads "title- (1) voids" (single hyphen), while this node's quoted_text
carried "title-- (1) voids" (double hyphen) -- a typographic artifact inherited from round 29's
Cornell LII mirror verification. Fixed to match the official source exactly; this closes the live
re-verification round 29's tier_rationale had explicitly flagged as outstanding.

**Fix 2 -- CA-SOL-WRITTEN-CONTRACT-DEBT's COVID Emergency Rule 9(a) tolling was overbroad.** This
node's Stage B adversarial call truncated after 2 of 3 edge cases and did not parse successfully
(`gaps_found: []` as a mechanical result) -- but the raw partial text before truncation contained a
complete, well-reasoned first scenario, read and independently verified rather than discarded, per
this project's standing practice of treating partial Stage B text as a real lead even when it doesn't
formally register as a gap. The node's `determination` previously added +178 tolling days to any claim
whose deadline "had not already passed as of April 6, 2020" -- trivially true for essentially any claim,
including ones accruing well AFTER the tolling window closed on October 1, 2020 (e.g., a 2022 default,
which never had its limitations clock running during the tolled window at all). Fixed by adding the
missing accrual-before-October-1-2020 condition to both `covid_emergency_rule_9_tolling_note` and
`determination`.

**Fix 3 -- FDCPA-REGF-CALL-FREQUENCY-1006.14b's unit-of-count ambiguity and call-scope gap**, both
genuine Stage B findings on the same run, both groundable directly in the already-cited, already-verified
12 CFR § 1006.14(b)(2)(i) text ("a telephone call to a particular PERSON") with no new citation needed:
(a) rewrote `unit_of_count` to state unambiguously that calls to the same consumer at different phone
numbers (cell, home, work) are aggregated into ONE 7-call bucket -- only a genuinely different person
gets a separate bucket -- replacing an earlier "her workplace" example that could be misread as a
different-number case; (b) added `what_counts_as_a_call_note`: the 7-in-7 count covers phone calls only,
not texts or emails, which are separately governed by 12 CFR 1006.6(b)/1006.14(h), not yet encoded as
their own nodes.

**Not fixed this round, deferred honestly:** the same live run's 3rd FDCPA-REGF-CALL-FREQUENCY finding
(California's Rosenthal Act, Cal. Civ. Code § 1788 et seq., reportedly extends "debt collector" coverage
to original creditors, unlike the federal FDCPA) was NOT encoded -- `web_fetch` to
leginfo.legislature.ca.gov timed out 3 consecutive attempts this session, and per standing discipline
this corpus never encodes quoted statutory text without a live verification fetch. Flagged in
`state_law_may_be_stricter_note` and here, not silently dropped; queued for the next round once the
fetch succeeds.

**Verification:** full CI suite (`validate_debt_schema.py`, `check_frozen_artifacts.py`,
`check_corroboration_calibration.py`) run and passing; patch verified via `git am --3way` against a
fresh clone of real origin (chained after rounds 27-31) before delivery. Content-only round -- no
runner/calibration fixture change, consistent with the one-variable rule.

## 2026-09-01, round 31 (content-only: new dedicated FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6 node + cross-references)

**What changed since round 30:** content-only, no runner/pipeline change. Andy approved (2026-09-01, "i see - thank you - yes, go ahead and build") building a dedicated coverage-threshold node after I flagged that the FDCPA "debt collector" coverage analysis under 15 U.S.C. § 1692a(6) was being independently re-derived, in shortened form, inline in multiple FDCPA nodes (round 30) -- a duplication/drift risk this round closes.

- **New file `rules/debt/federal/fdcpa_coverage_threshold_v1.json`**, node `FDCPA-COVERAGE-DEBT-COLLECTOR-1692a6`: full grounded derivation of 15 U.S.C. § 1692a(6) ("debt collector" definition, all exclusions (A)-(F), the own-name carve-back-in) and § 1692a(4) ("creditor" definition), plus *Henson v. Santander Consumer USA Inc.*, 582 U.S. ___ (2017) as a case-law citation. Henson's holding is stated narrowly and correctly: a debt buyer collecting for its own account is not covered via the "owed ... another" prong, but the Court expressly declined to decide the separate "principal purpose" prong -- most debt-buying businesses, whose principal purpose is debt collection, likely remain covered debt collectors under that alternative test. This corrects a common oversimplification ("debt buyers are excluded from the FDCPA") that would misstate the law. DRAFT tier.
- **`rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`, node `FDCPA-REGF-CALL-FREQUENCY-1006.14b`**: shortened `logic.fdcpa_coverage_threshold_note` from a full inline re-derivation to a brief cross-reference to the new node; node-specific content (unit-of-count, state-law-may-be-stricter note, checklist) unchanged. New `drafting_revisions` entry.
- **`rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`, nodes `FDCPA-FALSE-DECEPTIVE-CATALOG-1692e` and `FDCPA-UNFAIR-PRACTICES-CATALOG-1692f`**: added a lightweight `coverage_threshold_node_ref` cross-reference plus one new `completeness_checklist` item each, pointing to the new node's fuller analysis alongside their existing threshold_predicates / debt_collector_threshold_note summaries. Proactive fix, closing the same latent gap before a future adversarial run flags it -- not yet flagged.
- **`rules/debt/federal/fdcpa_validation_notice_v1.json`, node `FDCPA-VALIDATION-NOTICE-1692g`**: updated the `tier_rationale` on its 15 U.S.C. § 1692a(6) `derived_from` entry, and the corresponding `completeness_checklist` item, to cross-reference the new node instead of carrying the coverage analysis solely inline.

**Verification:** full CI suite (`validate_debt_schema.py`, `check_frozen_artifacts.py`, `check_corroboration_calibration.py`) run and passing; patch verified via `git am --3way` against a fresh clone of real origin (chained after rounds 27-30, all confirmed present on origin) before delivery. Content-only round -- no runner/calibration fixture change, consistent with the one-variable rule.

## 2026-09-01, round 30 (content fix: 6 new adversarial gaps on the 2 FDCPA nodes from Andy's re-run smoke test)

**What changed since round 29:** `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`
and `rules/debt/federal/fdcpa_validation_notice_v1.json` only -- new
`derived_from` entries, `logic` notes/fixes, `drafting_revisions` entries, and
`completeness_checklist` items on the two flagged nodes. No runner/CI changes
-- content-only round per the one-variable rule.

**Background.** Andy re-ran the 3-node smoke test after rounds 27-28's
citation-checker fixes (`run_20260901T100043Z.json`). Result confirms the
fixes: citation-verification jumped to 100% (was 33.3%), and
`CA-SOL-WRITTEN-CONTRACT-DEBT` showed CLEAN-PASS this run (round 29's content
fix for that node had not yet been applied to origin at the time of this run
-- its gaps are real and verified regardless of whether this particular
stochastic Stage-B run happened to resurface them; round 29 should still be
applied). The two FDCPA nodes were still FLAGGED, but this time with Stage A,
citation-verification, AND Stage B parse-success all at 100% -- meaning
rounds 27-28's fixes hold, and this is a different class of finding: genuine,
new Stage B adversarial gaps that citation-check failures had previously been
masking (a FLAGGED node with a broken citation check never gets to a clean
adversarial read the same way).

**`FDCPA-REGF-CALL-FREQUENCY-1006.14b` -- 3 gaps.** (1) No FDCPA "debt
collector" coverage threshold: this node's 7-in-7 rule is a Reg F rule, and
Reg F only reaches "debt collectors" under 15 U.S.C. 1692a(6) -- not an
original creditor calling in its own name, nor a servicer that acquired the
loan while it was not yet in default. (2) The unit-of-count was encoded as
"per particular debt" only, missing that it is ALSO per particular PERSON
(12 CFR 1006.14(b)(2)(i)'s own text specifies both) -- calls to different
people about the same debt are not supposed to be aggregated, but the node's
prior encoding would have wrongly flagged that as a violation. (3) No
state-law overlay: several states impose stricter call-frequency limits than
the federal 7-in-7 safe harbor. Massachusetts (940 CMR 7.04(1)(f), 2
communications per 7-day period, and notably reaching "creditors" broadly,
not just FDCPA-covered debt collectors) is now encoded as a verified example;
other states are flagged HORIZON, not encoded, since they weren't
independently verified this round.

**`FDCPA-VALIDATION-NOTICE-1692g` -- 3 gaps.** (1) Same coverage-threshold
gap as above (15 U.S.C. 1692a(6)) -- an uncovered entity has no
validation-notice duty under this node at all. (2) The `dispute_window`
determination's weekend/holiday exclusion was ambiguously worded --
"computed per the exclusions above" could be misread as excluding
weekends/holidays across the whole 35-day span, when in fact the exclusion
applies ONLY to the initial 5-business-day receipt assumption; the following
30-day period runs in ordinary calendar days. Rewritten to be unambiguous.
(3) No non-delivery/returned-mail handling: the CFPB's own official
interpretation of 12 CFR 1006.34(b)(5) (comment 34(b)(5)-2, confirmed via
direct fetch of consumerfinance.gov) states that once a collector knows the
original notice wasn't delivered and sends a follow-up, the 30-day window
runs from the FOLLOW-UP notice's date, not the original -- this node's
checklist never asked about non-delivery or a follow-up notice.

**Shared HORIZON note.** The coverage-threshold gap is really one
cross-cutting question affecting every node in this file (and likely all 5
FDCPA nodes in the corpus), not something to re-derive per node. Flagged
inline in both nodes' `tier_rationale` fields rather than deferred silently:
a dedicated FDCPA-coverage/"debt collector"-definition node would better
serve all affected nodes than repeating a condensed version of the same
analysis in each.

*Verification:* `validate_debt_schema.py` PASS; diff is 73 lines across 2
rules files; patch verified via fresh-clone `git am --3way` (chained after
rounds 27-29) before delivery.

## 2026-09-01, round 29 (content fix: CA-SOL-WRITTEN-CONTRACT-DEBT's 3 genuine adversarial gaps -- COVID tolling, federal student loan preemption, bankruptcy screening)

**What changed since round 28:** `rules/debt/state/california/ca_debt_state_layer_v1.json`
only -- 4 new `derived_from` entries, 3 new `logic` notes, a rewritten
`determination` field, a new `drafting_revisions` entry, and 3 new
`completeness_checklist` items, all on `CA-SOL-WRITTEN-CONTRACT-DEBT`. No
runner/CI changes -- content-only round per the one-variable rule.

**Background.** Andy's 3-node smoke test (`run_20260831T212748Z.json`)
flagged this node with `citation_check` 5/5 verified -- the flag was driven
entirely by 3 genuine Stage-B adversarial findings (all
`realistic_and_common=true`, `would_cause_wrong_answer=true`), not a checker
issue. Andy's instruction was to fix "each 1 at a time" but "investigate and
fix all identified issues" from that run; rounds 27-28 handled the two
citation-check breaks, this round handles the third (content) flag.

**Gap 1 -- COVID-19 tolling.** The node's flat accrual-plus-4-years
computation didn't account for Cal. R. Ct. emergency rule 9(a), which tolled
all California civil SOLs exceeding 180 days for 178 days (April 6 -- October
1, 2020) -- automatic and universal, not something a consumer would ever
volunteer as a "fact." This is outcome-determinative for the large cohort of
debts that defaulted in the several years before the pandemic. Confirmed via
direct fetch of the Judicial Council's official amended rule text this round
(the rule as *originally* adopted read differently -- tied to the end of the
state of emergency -- and was amended May 29, 2020 to the fixed October 1,
2020 date used here).

**Gap 2 -- federal student loan SOL preemption.** 20 U.S.C. § 1091a
eliminates any limitations period for federal actors (the Secretary,
guaranty agencies, institutions under Direct/Perkins agreements) collecting
on federally-held or federally-guaranteed student loans. The node's 4-year
CA analysis simply doesn't apply to such loans at all -- but DOES still apply,
unchanged, to a privately-held student loan from the same borrower and era,
which a layperson would have no reason to distinguish. Confirmed via direct
fetch of the official U.S. Code (uscode.house.gov).

**Gap 3 -- bankruptcy screening.** Two distinct effects previously folded
into a generic "other statutory tolling" checklist item, now split out: (a)
11 U.S.C. § 108(c) extends the SOL until 30 days after notice a bankruptcy
stay ends, if the deadline hadn't already run when the case was filed
(notice-triggered, not a flat number of days -- confirmed via uscode.house.gov);
and (b) 11 U.S.C. § 524(a)(1)-(2) -- an actual discharge is a complete,
independent bar on collection regardless of the SOL (any judgment is void,
collection is enjoined). A "not expired" SOL answer on a debt that was
actually discharged would be badly misleading. (§524(a) quoted_text
verbatim-confirmed via Cornell LII's mirror of the official text this round
after this session's tooling could not fully retrieve uscode.house.gov's own
page output for that section -- flagged for live re-verification against the
uscode.house.gov URL itself, per this corpus's practice of flagging
mirror-confirmed text rather than silently assuming it matches.)

**Fix.** Added all 4 citations as new `derived_from` entries; added 3 new
`logic` notes explaining each gap and how it interacts with the node's
existing accrual/filing-date/judgment-enforcement logic; rewrote
`determination` to incorporate the conditional +178 days and flag the two
threshold questions (federal-loan status, discharge status) that override
the ordinary SOL computation; added 3 new `completeness_checklist` items.
Logged as a new `drafting_revisions` entry per the standing DRAFT-tier
editing discipline -- tier promotion still requires Andy/counsel sign-off.

*Verification:* `validate_debt_schema.py` PASS; diff is 51 lines in one
rules file; patch verified via fresh-clone `git am --3way` before delivery.

## 2026-09-01, round 28 (runner fix: citation-checker whitespace-before-punctuation normalization gap)

**What changed since round 27:** `scripts/corroboration/run_corroboration.py`
(one additive line in `_normalize_for_match`, plus its explanatory comment),
one new checked-in calibration fixture (`CAL-09-tag-boundary-before-punctuation.json`),
and `scripts/corroboration/calibration_fixtures/_expected_metrics.json` (updated
counts/rates for the now-9-fixture set). `docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md`
S4b updated to document the 9th fixture. No `rules/` content touched --
runner-only round per the one-variable rule (Task A's content fix shipped
separately as round 27).

**Root cause, confirmed against the live eCFR page.** Andy's 3-node smoke test
flagged `FDCPA-REGF-CALL-FREQUENCY-1006.14b` on its `12 C.F.R. § 1006.14(b)(4)`
citation (`longest_matching_prefix_chars=34`, breaking exactly at "paragraph
(b),"). Unlike round 27's node, this `quoted_text` field IS genuinely verbatim
-- confirmed by fetching the real eCFR § 1006.14 page directly this round and
comparing character-by-character. So this was investigated as a
diagnostic/checker gap rather than a content problem, per Andy's "investigate
and fix all identified issues" instruction (each flag triaged to its real
category with evidence, per standing discipline, rather than assuming the same
cause as round 27's node).

The real markup: eCFR wraps the cross-reference "paragraph (b)" in a single
`<a>` tag whose closing `</a>` lands immediately after the reference's own
closing paren and before the sentence's next punctuation mark ("...this
`<a href="...">paragraph (b)</a>`, particular debt means..."). `_strip_html`'s
blanket tag-to-space substitution turns `</a>,` into ` ,`, inserting a stray
space between `)` and `,` that round 23's paren-only whitespace fix (which
only collapses whitespace immediately *inside* a paren pair) doesn't touch --
a different specific pattern than round 23's nested-span case, though the same
underlying tag-to-space root cause.

**Verified empirically before shipping, not just asserted:** reproduced the
exact live-run break (`prefix_len=34`) against a hand-built fragment of the
real eCFR markup using the OLD `_normalize_for_match`, confirmed the fix
resolves it (full 120/120 match) with the NEW version, then proved the new
`CAL-09` calibration fixture actually catches the regression by temporarily
reverting the fix and re-running `--replay` (correctly turned red, then green
again after restoring) -- same discipline as round 26's `CAL-06` proof.

**Fix.** One additive line in `_normalize_for_match`, checked after the
existing paren-collapse lines (which remain untouched): collapse whitespace
immediately before common sentence punctuation (comma/period/semicolon/colon).
Same one-directional, additive-only reasoning as round 23 -- no normal legal
prose (and no `quoted_text` field in this corpus) ever has a space before a
comma/period/semicolon/colon, so this only ever helps a correct match, never
hides a real mismatch.

*Verification:* all 9 calibration fixtures + all metric assertions PASS via
`--replay`; full CI suite (`validate_debt_schema.py`, `check_frozen_artifacts.py`,
`check_corroboration_calibration.py`) PASS; patch verified via fresh-clone
`git am --3way` (chained after round 27) before delivery. Per the freeze's own
CI gate rule, this runner change ships only because calibration + replay
passed first.

## 2026-08-31, round 27 (content-only fix: FDCPA-VALIDATION-NOTICE-1692g's 12 C.F.R. § 1006.34(c) quoted_text was a paraphrase, not verbatim)

**What changed since round 26:** `rules/debt/federal/fdcpa_validation_notice_v1.json`
only — one `quoted_text` field and one `drafting_revisions` entry. No changes
to `scripts/corroboration/run_corroboration.py` or any other runner/CI file.
Content-only round per the one-variable rule.

**Investigation.** Andy's 3-node live smoke test of the round-26 runner
(`run_20260831T212748Z.json`, `--nodes FDCPA-VALIDATION-NOTICE-1692g,
FDCPA-REGF-CALL-FREQUENCY-1006.14b,CA-SOL-WRITTEN-CONTRACT-DEBT`) came back
0/3 full-pipeline clean-pass, all 3 `FLAGGED`. Investigated each flag to its
real category per standing discipline rather than assuming a single cause.
`CA-SOL-WRITTEN-CONTRACT-DEBT` flagged purely on 3 genuine Stage-B adversarial
gaps (citation_check was 5/5 verified) -- a real content-completeness
question, not a checker issue, out of scope for this round and not yet
actioned. The other two nodes both flagged on citation-check breaks, which
this round and the next (round 28) investigate and fix separately, per
Andy's "fix each 1 at a time... investigate and fix all identified issues"
instruction, each root-caused against the real live eCFR page rather than
guessed.

**This node's break, root-caused.** `12 C.F.R. § 1006.34(c)`'s
`longest_matching_prefix_chars` was 120 (the full matched window) -- meaning
the citation checker's 120-char comparison window never even reached the
actual problem. Fetched the real eCFR § 1006.34 page directly this round and
compared it character-by-character against our `quoted_text`: the prior text
was not a verbatim excerpt at all -- it was a colon-joined,
semicolon-separated summary paraphrasing what the regulation actually states
as four separately numbered, period-terminated subsections, each with its own
heading (the real text reads "...validation information. (1) Debt collector
communication disclosure. The statement required by § 1006.18(e). (2)
Information about the debt. Except as provided in paragraph (c)(5) of this
section: ..." -- not the semicolon-summary previously quoted). This is a
citation-integrity issue, not a legal-content error -- the node's title,
`logic`, `completeness_checklist`, and `consequences_and_next_steps` were all
already correct and are unchanged.

**Fix.** Replaced the paraphrase with a genuinely verbatim excerpt (the
lead-in sentence plus subsection (c)(1) with its real heading and
cross-reference), confirmed against the live-fetched page. Logged as a new
`drafting_revisions` entry per the standing DRAFT-tier editing discipline
(tier promotion still requires Andy/counsel sign-off). *Verification:* CI
suite (`validate_debt_schema.py`, `check_frozen_artifacts.py`,
`check_corroboration_calibration.py`) all pass; diff is 8 lines, confirmed
via `git diff --stat`; patch verified via fresh-clone `git am --3way` before
delivery.

**Round 28 (separate, not in this patch):** `FDCPA-REGF-CALL-FREQUENCY-1006.14b`'s
`12 C.F.R. § 1006.14(b)(4)` break is a different root cause -- the
`quoted_text` there IS genuinely verbatim (confirmed by direct comparison
against the live-fetched § 1006.14 page); the break is a diagnostic/checker
gap in `_normalize_for_match`'s HTML-to-text stripping, not a content
problem. Investigated and fixed as its own runner-only round, per the
one-variable rule.

## 2026-08-31, round 26 (calibration + replay harness built and wired into CI; Stage-B-silent-clean-pass bug fixed -- freeze items 2/3)

**What changed since round 25:** `scripts/corroboration/run_corroboration.py` (a
runner change -- replay-mode dependency injection, the metric rename/split, and
the Stage-B fix), 8 new checked-in fixture files plus a metrics manifest under
`scripts/corroboration/calibration_fixtures/`, a new `scripts/ci/check_corroboration_calibration.py`
CI gate, and `docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md` (canonical metric
definitions + harness documentation). No `rules/` content touched -- consistent
with the one-variable rule adopted round 25.

**Built (freeze item 2): the calibration + replay harness.** A `--replay` CLI
mode exercises the entire pipeline offline (no keys, no network, no cost)
against 8 frozen, checked-in fixtures under `scripts/corroboration/calibration_fixtures/`,
through the SAME parsing/retry/matching code the live path uses -- not a
reimplementation -- via a purely-additive `replay_*` parameter on each of
`call_anthropic`/`call_openai`/`call_gemini`/`judge_semantic_agreement`/
`verify_citation`, checked before the existing `dry_run`/live branches (which
are unmodified). Mirrors the discipline at Open Question #11 in
`docs/OPEN_QUESTIONS_AND_LIMITATIONS.md` and its concrete pattern in
`rules/validation/tests/test_ca_notice_scorer_outcome_fallback.py`.

The 8 fixtures: a clean-pass baseline; a genuine Stage-A disagreement (proves
the judge isn't a rubber stamp); regression guards reproducing the exact
round-23 (eCFR nested-span) and round-24 (editorial ellipsis) bugs against
their real fixes; a Stage-B-truncation-then-retry-recovers case; a genuine
adversarial-gap case; a genuine-citation-mismatch-still-caught case (proves the
round-23/24 permissiveness fixes didn't loosen the checker into a rubber
stamp); and `CAL-06`, the designed-to-fail case for the bug fixed this round
(below) -- confirmed by temporarily reverting that fix and re-running
`--replay`, which correctly turned it red before the fix was restored.

Per Andy's addition to freeze item 2, `_expected_metrics.json` gives
known-answer expected values for the aggregate metrics themselves (not just
per-fixture pass/fail), so `compute_demo_gate_metrics()`'s own arithmetic is
regression-tested. All 8 fixtures and all metric assertions currently PASS.

**Found and fixed while building the harness: a Stage B parse failure could
silently compute as CLEAN-PASS.** `_parse_json_response`'s failure-fallback
dict has no `edge_cases` key at all, so `result_b.get("edge_cases", [])` was
returning `[]` on a genuine unrecovered parse failure -- indistinguishable from
a real "no gaps found." This is the exact bug behind
`TX-WAGE-GARNISHMENT-PROHIBITION` showing CLEAN-PASS in
`run_20260831T082700Z` despite an unrecovered `_parse_error` (flagged in round
25's stage-level attribution report). Fixed: `clean_pass` now additionally
requires `stage_b_parsed_ok` (`"edge_cases" in result_b and not result_b.get("error")`);
a new `STAGE-B-PARSE-FAILURE` disagreement-queue entry type files this case
explicitly rather than leaving it invisible.

**Metric reconciliation (freeze item 1's finding, now implemented; see round 25
for the finding itself).** `compute_demo_gate_metrics()` now reports four
stage-level rates separately -- `stage_a_grounded_agreement_rate`,
`citation_verification_rate`, `stage_b_parse_success_rate`,
`full_pipeline_clean_pass_rate` -- each with an explicit stage/numerator/
denominator, documented canonically in
`docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md` S4a. `grounded_agreement_rate` (the
old, mislabeled name) is kept as a deprecated alias equal to
`full_pipeline_clean_pass_rate` so nothing that reads it breaks. The
`--dry-run`/`--live` summary print was updated to show all four rates instead
of one blended number.

**Built (freeze item 3): CI gate.** `scripts/ci/check_corroboration_calibration.py`
runs `--replay` and fails loudly on any miss, mirroring
`validate_debt_schema.py`/`check_frozen_artifacts.py`'s pattern. Standing
discipline from here forward: no runner-touching patch ships, and no live run
is requested from Andy, unless this passes.

**Verification:** `python3 scripts/ci/validate_debt_schema.py` -- PASS (no
rules content changed this round). `python3 scripts/ci/check_frozen_artifacts.py`
-- PASS. `python3 scripts/ci/check_corroboration_calibration.py` -- PASS (8/8
fixtures, all metric assertions). `python3 scripts/corroboration/run_corroboration.py
--dry-run --demo-corpus-only --nodes FDCPA-VALIDATION-NOTICE-1692g` -- spot-checked
the existing dry-run/live code paths are byte-for-byte unmodified and still
work (only new early-return branches were added ahead of them).

**Not done this round:** the ~15 nodes' worth of genuine adversarial findings
surfaced by run 24 remain deferred, per the one-variable rule -- this round is
runner-only. Live-run freeze remains in effect; the next live run should be
the `--nodes 3` smoke test (freeze item 5), not the full corpus.

---

## 2026-08-31, round 25 (live-run freeze steps 1-2: stage-level attribution, regression hunt, one-variable rule + smoke protocol adopted -- documentation only, no runner or content code changed)

**What changed since round 24:** nothing in `run_corroboration.py` or any `rules/` file.
This round is pure analysis of `run_20260831T082700Z.json` (already captured, no live
call made) plus documentation. Consistent with the one-variable rule adopted below.

**Context:** Andy issued a live-run freeze after round 24's 5.6% clean-pass result,
directing five things in order before any further live run: (1) stage-level
attribution + regression hunt on run 24, with round 23's citation-normalization change
checked first as the prime suspect, and the 5.6% topline reconciled against the 18/18
`all_grounded` per-node data; (2) a calibration + replay harness; (3) a CI gate on it;
(4) a one-variable rule; (5) a `--nodes 3` smoke protocol. This entry covers (1) and
adopts (4)/(5) as standing discipline; (2)/(3) are the next, larger piece of work.

**Stage-level attribution, `run_20260831T082700Z` (18 nodes):**

| Stage | Pass rate | Detail |
|---|---|---|
| Stage A (semantic agreement AND all_grounded) | 18/18 = 100.0% | zero cross-model legal conflicts |
| Citation-check (`all_verified: true`) | 6/18 = 33.3% | dominant driver of the low topline |
| Stage B adversarial (parsed, no truncation/empty) | 16/18 = 88.9% | up from ~9/18 two rounds ago |
| Reported CLEAN-PASS (`grounded_agreement_rate`) | 1/18 = 5.6% | full-pipeline AND of all three stages |

**Regression hunt: round 23's `_normalize_for_match` paren-collapse change is
exonerated by a matched before/after comparison, not just code review.** Of the 14
nodes whose `derived_from` content did not change in round 23, citation `verified`
flipped True-to-False zero times between the pre-round-23 run (`run_20260830T181129Z`)
and the post-round-23 run (`run_20260831T082700Z`); it flipped False-to-True twice
(`FDCPA-REGF-CALL-FREQUENCY-1006.14b`'s second citation and
`FDCPA-FALSE-DECEPTIVE-CATALOG-1692e`'s citation -- the fix's intended effect). Every
other currently-failing citation on those 14 unchanged nodes was already failing
before round 23 ran -- pre-existing, not caused by it. The 4 nodes round 23 also
edited content on (`FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b`,
`FDCPA-UNFAIR-PRACTICES-CATALOG-1692f`, `CA-SOL-WRITTEN-CONTRACT-DEBT`,
`TX-EXEMPT-PERSONAL-PROPERTY`) show new/edited citations that were simply never
checked before round 23 -- not regressions either. Structurally this is expected: the
normalization function is applied identically to both the needle (quoted text) and
the haystack (fetched page), so a change to it can only make matching more permissive,
never less. **No Stage A regression was found either** -- both the pre- and
post-round-23 runs show every node fully grounded and in cross-model agreement; there
is nothing to root-cause or add as a test case on that front.

**Metric reconciliation: `grounded_agreement_rate` is mislabeled relative to its own
definition.** `compute_demo_gate_metrics()`'s own `basis` string already discloses
this honestly (CLEAN-PASS = semantic agreement AND citation verification AND no
adversarial gap), but the metric's *name* promises a Stage-A-only reading. The 5.6%
topline is a full-pipeline AND of all three stages, compounding the citation-checker's
33.3% verify rate and the adversarial stage's near-universal real findings on top of a
Stage A rate that is actually 100%. Fix: split into a renamed
`full_pipeline_clean_pass_rate` (same computation, honest name) plus a new,
genuinely Stage-A-only `stage_a_grounded_agreement_rate`. This ships as part of the
calibration-harness build (next round), with metric-value test coverage, not as a bare
patch -- consistent with the freeze's own no-runner-change-without-calibration rule.

**New finding, not previously known: a Stage B parse failure can silently read as
CLEAN-PASS.** `TX-WAGE-GARNISHMENT-PROHIBITION` shows `status: CLEAN-PASS` in run 24
despite its Stage B call ending in `_parse_error` (the same node round 24's changelog
named as one of the two still-truncating even after the 1.5x retry). `clean_pass`'s
formula treats an empty `gaps_found` list as "no gaps" regardless of *why* the list is
empty -- a parse failure and a genuinely clean adversarial check are indistinguishable
to the gate. This is a real bug, distinct from anything fixed in rounds 23-24, and
becomes a calibration-harness fixture (a Stage B failure must not silently compute as
clean) rather than a rushed runner patch, per the freeze.

**Adopted as standing discipline this round (freeze items 4 and 5, documentation
only -- see `docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md` §4):**
- **One-variable rule.** Pipeline changes and content changes never land in the same
  round going forward (round 23 mixed both, which is exactly what made this round's
  regression hunt necessary work rather than a five-minute check). Every future run
  summary and changelog entry states explicitly what changed since the prior run.
- **Smoke protocol.** Every future live session starts with `--nodes 3` before the
  full corpus; Claude gives Andy that two-step instruction rather than a full-run
  command directly.

**Verification:** no code changed this round; `python3 scripts/ci/validate_debt_schema.py`
and `python3 scripts/ci/check_frozen_artifacts.py` both re-run for hygiene, both PASS.

**Not done this round, next up:** the calibration + replay harness (freeze item 2/3)
-- reading the eviction scorer's existing calibration discipline first for parity,
then building `--replay`, the frozen fixture set (including the two round-23/24 bug
patterns and the new Stage-B-silent-clean-pass finding above as designed-to-fail
fixtures), and the metric rename/split with known-answer value assertions. Live-run
freeze remains in effect until that lands and passes.

---

## 2026-08-31, round 24 (ellipsis-matching fix + Stage-B retry bump; scope of remaining work re-assessed)

**Context:** Re-ran the corpus after round 23's patch: `run_20260831T082700Z` -- 1/18
clean-pass (5.6%), 17 flagged. Lower than the 27.8% that prompted round 23, at first
glance a regression from the fixes just delivered. Read all 18 nodes (via structured
extraction across `semantic_agreement`, `all_grounded`, `citation_check.all_verified`,
and Stage-B retry/parse-error fields) before concluding anything.

**Finding: round 23's fixes are confirmed active and working, and the underlying
picture is actually the best this project has seen -- the raw percentage just doesn't
show it yet.** Every single one of 18 nodes shows `all_grounded: true` and
`semantic_agreement: true` -- zero actual cross-model legal conflicts anywhere.
`_stop_reason` fields (round 23's addition) are present throughout, confirming the
instrumentation landed. The Stage-B retry logic fired correctly on several nodes
(`"_retried_after": "max_tokens_truncation"`), confirming round 23's retry-on-
truncation fix is live and doing its job -- only 2 of 18 nodes still show a Stage-B
parse failure after retry (down from roughly 9 of 18 two rounds ago), and the
remaining 16 nodes' adversarial checks now return real, fully-parsed, often
sophisticated findings (e.g. a *TransUnion v. Ramirez* Article III standing gap, an
e-OSCAR/ACDV workflow mismatch, an identity-theft mandatory-block remedy under
§ 1681c-2 -- genuinely high-value legal analysis that prior rounds' truncation was
silently discarding).

**What's actually driving the low percentage now: citation-checker false negatives,
still.** 13 of 18 nodes have `citation_check.all_verified: false`. Diagnosed with
`raw_html_context_at_break` evidence (captured on 3 citations this run) that this is
a DIFFERENT bug than round 23 fixed, not a recurrence: two of the three confirmed
breaks are the checker choking on our OWN editorial ellipsis ("...", used routinely
in `quoted_text` fields to elide between two cited clauses) -- the actual page text at
those points is perfectly clean and contiguous (e.g. CCP § 683.020's "(a) The judgment
may not be enforced. (b) All enforcement procedures..." reads straight through with no
gap), but the checker's needle was built from a blind 120-character window of the full
`quoted_text`, which can include the literal three dots -- something no real page will
ever contain. This is a structural gap in the checker (it never had any way to verify
an intentionally-elided quote), not an HTML-markup artifact like round 23's fix.

**Fixed this round:**
1. **Ellipsis-aware citation matching.** `verify_citation`'s needle is now built from
   the text before the first "..." in `quoted_text` (still capped at 120 chars) rather
   than a blind window of the full string. Verified with a unit test reconstructing
   the exact CCP § 683.020 break this run captured.
2. **Stage-B retry budget bumped further.** Round 23's 1.5x retry multiplier
   (3000/4000 -> 6000 tokens) still wasn't enough for the 2 most verbose remaining
   nodes (`FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b`, `TX-WAGE-GARNISHMENT-PROHIBITION`
   -- both still showed `_parse_error` even after retry). Bumped to 2.5x (10000
   tokens) for real headroom on Claude's most detailed 3-scenario responses.

Both fixes verified: syntax check, a targeted unit test, and a `--dry-run` execution.

**Not fixed / not yet understood:** one break this run (`FDCPA-VALIDATION-NOTICE-1692g`'s
12 C.F.R. § 1006.34 citation) is neither the round-23 paren pattern nor this round's
ellipsis pattern -- the page uses an em dash where our `quoted_text` uses a colon
immediately before "(1)". This looks like a genuine punctuation-accuracy issue in that
one `quoted_text` field (likely from a WebSearch-reconstructed quote rather than an
exact copy), not a systemic checker bug -- flagged for a content-round fix, not chased
with more checker code this round.

**Scope note, not yet actioned:** with Stage-B now parsing successfully on 16 of 18
nodes, this run surfaced real, well-reasoned adversarial findings on nearly every
flagged node -- a much larger volume of genuine content gaps than any prior round
(previous rounds' truncation was apparently masking most of this). This is reported to
Andy as a pacing question rather than drafted immediately: previous rounds handled
4-7 node edits at a time; this run's real findings span roughly 15 nodes. Deferred to
Andy's direction on how to sequence that volume of work.

**Verification:** `python3 scripts/ci/validate_debt_schema.py` -- all 9 debt-track
rules files pass (no rules content changed this round, runner-only). `python3
scripts/ci/check_frozen_artifacts.py` -- both frozen artifacts untouched, PASS.

---

## 2026-08-30, round 23 (two pipeline bugs root-caused and fixed; 4 genuine content gaps incorporated)

**Context:** Re-ran the corpus after round 22's patch: `run_20260830T181129Z` -- 5/18
clean-pass (27.8%), 13 flagged, a steep drop from round 21's 66.7%. Read all 18 nodes
in full before drafting anything, per standing discipline, rather than treating a
sharp swing as either "the law got worse" or noise to wave away.

**Finding: this was almost entirely a pipeline problem, not a legal-content
regression.** Every node where Stage A actually completed showed all three models
grounded and in full semantic agreement -- including confirming round 22's new
content (CA-CIVIL-ANSWER-DEADLINE's service-completion rules, TX-DEFAULT-JUDGMENT's
TRCP 505.3/306a/*Peralta* additions, TX-WAGE-GARNISHMENT's federal-override clause)
landed and was independently re-derived correctly by all three models. Zero actual
cross-model legal conflicts anywhere in this run. Two separate infrastructure bugs
account for nearly all 13 flags:

1. **Citation-checker false negatives.** Root-caused via `raw_html_context_at_break`
   (a round-14/17 diagnostic that finally captured real evidence on a live run for
   the first time this round): eCFR wraps each character of a paragraph-hierarchy
   marker like "(1)" in its own nested `<span>`
   (`<span class="paragraph-hierarchy"><span class="paren">(</span>1<span
   class="paren">)</span></span>`). `_strip_html`'s blanket tag-to-space replacement
   (needed elsewhere, to avoid concatenating adjacent inline-linked WORDS) turns
   "(1)" into "( 1 )" on the page side only, breaking the exact-match check at that
   exact point even when word-overlap was a perfect 1.0. Confirmed against the
   actual markup this run captured. **Fixed**: `_normalize_for_match` now collapses
   whitespace immediately inside parentheses -- a safe, one-directional fix (no
   quoted_text field in this corpus, and no normal legal prose, ever has a space
   touching an opening or closing parenthesis, so this only repairs the page-side
   artifact and is a no-op on the needle side).

2. **Stage-B adversarial call reliability.** Two distinct silent failure modes: (a)
   empty completions (`_raw: ""`, `error: None`) with no retry -- hit
   FDCPA-REGF-CALL-FREQUENCY, FDCPA-VALIDATION-NOTICE-1692g, CA-CIVIL-ANSWER-DEADLINE,
   TX-DEFAULT-JUDGMENT; (b) truncated/unparseable JSON, even at round 19's bumped
   3000-token budget on verbose 3-scenario responses -- hit
   FDCPA-FALSE-DECEPTIVE-CATALOG-1692e, CA-SOL-ORAL-CONTRACT-DEBT, CA-VEHICLE-EXEMPTION,
   CA-BANK-ACCOUNT-EXEMPTION, TX-HOMESTEAD-EXEMPTION -- silently discarding real
   findings visible in the raw text (e.g. an EDD/unemployment-benefits gap on CA bank
   accounts, a recent-interstate-move homestead-cap issue) even though they never made
   it into `gaps_found`. **Fixed**: `call_anthropic` now captures the API's own
   `stop_reason` (so truncation is visible in the run JSON going forward, not silently
   indistinguishable from "no gaps found"), and the adversarial call site's budget is
   bumped 3000 -> 4000 tokens with one retry enabled (same budget for an empty
   completion, 1.5x budget for a max_tokens truncation).

Both fixes verified: a syntax check, a targeted unit test reproducing the exact eCFR
nested-span markup this run captured (confirms "( 1 )" -> "(1)" without breaking
normal text), and a `--dry-run` execution of the full runner end-to-end.

**Of the 13 flagged nodes, only 4 had genuinely real, cleanly-captured new findings**
(the other 9 were the infra bugs above, now fixed, and should re-run clean or closer
to clean next round):

- `FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b`: added § 1681n/1681o/1681p
  (remedies-and-limitations: willful vs. negligent damages standard, 2-year-discovery/
  5-year-violation suit deadline) and § 1681i(a)(3) (a CRA may terminate a
  reinvestigation as frivolous and never forward it to the furnisher, meaning no
  furnisher duty ever arises); tightened the CRA-forwarding trigger wording; added an
  accuracy-element note (a claim fails at the threshold if the reported info was
  actually accurate, regardless of investigation quality).
- `FDCPA-UNFAIR-PRACTICES-CATALOG-1692f`: added the statute's own introductory clause
  (the 8-item catalog is illustrative, not exhaustive -- a fact pattern matching no
  catalog item can still violate the general "unfair or unconscionable means" clause)
  and the § 1692a(6) debt-collector threshold (excludes original creditors,
  pre-default-acquiring servicers, in-house collection); broadened catalog item (8)'s
  envelope-symbol scope beyond "indicating debt collection" to match the statute's
  actual text (visible account numbers/QR codes are themselves violations per
  *Douglass v. Convergent*/*Daubert v. NRA Group*).
- `CA-SOL-WRITTEN-CONTRACT-DEBT`: fixed the `determination` field, which was keyed to
  comparing *today's date* against accrual-plus-4-years -- now correctly keys off the
  complaint's filing date once a suit has been filed, and flags that an existing
  judgment is governed by CCP § 683.020's 10-year enforcement/renewal period, not the
  original 4-year contract SOL at all; added a note that unaccelerated installment
  obligations accrue separately per missed installment, not from one single date.
- `TX-EXEMPT-PERSONAL-PROPERTY`: added life insurance cash value/proceeds (Tex. Ins.
  Code § 1108.051) and 529/Texas Tomorrow Fund college savings accounts (Tex. Prop.
  Code § 42.0022) as exempt outside the aggregate cap; added a note that the
  unlimited "current wages" exemption stops applying once wages are paid and
  deposited/commingled in a bank account (bank-account garnishment, not wage
  garnishment, is the common real-world Texas scenario); clarified that "family"
  status for the higher cap includes an unmarried head of household supporting
  dependents, not only a debtor with a spouse.

**Not done this round:** tier promotion for any of these 4 nodes -- all remain
`DRAFT`. `ca_eviction_v2.json` and the v0.3 held-out set untouched (frozen-artifact
check confirms).

**Verification:** `python3 scripts/ci/validate_debt_schema.py` -- all 9 debt-track
rules files pass. `python3 scripts/ci/check_frozen_artifacts.py` -- both frozen
artifacts match committed hash. `scripts/corroboration/run_corroboration.py
--dry-run` -- runs end-to-end with both runner fixes in place, no errors.

---

## 2026-08-30, round 22 (second DRAFT-tier iteration pass; adversarial-check sampling variance)

**Context:** Re-ran the corpus after round 21's patch was applied. Result:
`run_20260830T171724Z` -- 12/18 clean-pass (66.7%), 6 flagged (down from 8/18 flagged in round
20). Diagnosed all 6 flags before drafting anything, per standing discipline. Split cleanly into
two kinds:

1. **5 of the 6 nodes clean-pass on the SAME content that was flagged in round 20** --
   `FDCPA-VALIDATION-NOTICE-1692g` retitle fix confirmed working (models now derive cleanly instead
   of correctly refusing to guess); 4 of round 21's 7 content edits (the CA SOL nodes, the vehicle
   exemption, the TX exemption nodes) also confirmed clean. Of the 2 nodes that were edited in
   round 21 but flagged AGAIN this round (`FDCPA-FALSE-DECEPTIVE-CATALOG-1692e`,
   `CA-BANK-ACCOUNT-EXEMPTION`), the new findings are on genuinely different sub-issues than what
   round 21 fixed -- not a regression, a second layer of gaps the same node still has.
2. **4 nodes flagged for the first time this round**, with NO round-21 content change --
   `FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b`, `CA-CIVIL-ANSWER-DEADLINE`,
   `TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY`, `TX-WAGE-GARNISHMENT-PROHIBITION`.

**Methodological insight, this round:** the adversarial-check stage samples only 3 fresh edge
cases per node per run -- it is not exhaustive. A node clean-passing in one run is not proof it is
bulletproof; a later run can surface genuinely new, real findings purely from different sampling,
with zero change to the node's content in between. This is what happened to all 4 first-time-flag
nodes above. Practical implication for how Andy should read run-to-run deltas going forward: a
declining COUNT of flagged nodes across rounds is the real convergence signal (20 -> 18 -> ... );
a single run's flag list should be read as "here is what this round's sample turned up," not as
"here is the complete list of everything wrong with this node."

**Self-correction discipline applied this round** (documented since it changed what got encoded):
the adversarial check's own claims were independently re-verified, not taken at face value, and
were found inaccurate on one point -- its scenario for `TX-WAGE-GARNISHMENT-PROHIBITION` asserted
that 1099/independent-contractor compensation is categorically unprotected as "current wages for
personal service." Research this round found the actual Texas test turns on whether the payment is
compensation currently owed for personal service, not on 1099-vs-W-2 form alone -- a more
fact-specific, less settled question. Encoded as a hedged checklist/note item reflecting that,
NOT as the check's categorical claim. (Same discipline applied in round 21 to the check's guessed
CCP §704.080 dollar figures, which were also wrong and were corrected against the actual statute
rather than encoded as guessed.)

**What changed, this round -- 6 nodes edited, all still DRAFT tier:**

- `FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b`: added 15 U.S.C. §1681s-2(c)-(d) (no private right of
  action for the initial-notification duty; the actionable duty runs from a dispute notice via a
  CRA), added a D-tier judicial-gloss entry on the "reasonable investigation" standard, added
  `reasonableness_standard_note`, `practical_enforcement_note`, and an explicitly-hedged
  `legal_vs_factual_dispute_note` (the legal-dispute/factual-dispute line is circuit-dependent and
  unsettled -- flagged, not resolved, per *Denan*/*Chuluunbat* vs. the newer 4th Cir.
  "objectively and readily verifiable" test).
- `FDCPA-FALSE-DECEPTIVE-CATALOG-1692e` (2nd pass): added §1692a(6)(F)(iii) (loan-servicer/
  not-in-default exclusion from "debt collector"), added D-tier judicial-gloss entries for the
  materiality requirement and the time-barred/stale-debt-collection theory, added
  `materiality_note` and `stale_debt_note`.
- `CA-BANK-ACCOUNT-EXEMPTION` (2nd pass): added CCP §704.070 (75-100% recent-wage-deposit
  exemption) and §704.225 (need-based exemption above the statutory minimum), added
  `recent_wages_note`, `support_need_note`, and `joint_account_note` (citing CCP §720.110 et
  seq. -- corrected mid-drafting from an initially-misremembered §703.030 citation, verified
  before writing).
- `CA-CIVIL-ANSWER-DEADLINE`: added CCP §§415.20/415.40/415.50 (how the service-completion date
  itself is calculated for substitute/mail/publication service) and CCP §418.10 (motion to quash
  and the general-appearance waiver trap), added `service_method_note` and
  `defective_service_alternative_note`. Only 2 of the run's 3 findings warranted a change -- the
  3rd (weekend/holiday deadline rollover) was correctly self-assessed by the adversarial check
  itself as `exposes_gap: false`, so nothing was added for it.
- `TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY` (Band 3): added TRCP 505.3 (justice-court
  variant -- 14-day filing deadline, 21-day automatic denial, distinct from the
  district/county-court TRCP 329b 30/75-day rule this node already had), TRCP 306a(4)-(5)
  (notice-restart, up to 90 days after signing, on sworn motion), and the *Peralta v. Heights
  Medical Center* defective-service exception (no meritorious-defense showing required; restricted
  appeal within 6 months, or bill of review within 4 years). All 3 additions preserve this node's
  existing Band 3 discipline -- they name additional deterministic gates and deadlines, they do
  not predict any discretionary outcome.
- `TX-WAGE-GARNISHMENT-PROHIBITION`: added Tex. Civ. Prac. & Rem. Code §63.004's federal-law
  override clause (IRS levies, Dept. of Education administrative wage garnishment, federal
  restitution reach current Texas wages notwithstanding the state constitutional protection),
  added a hedged independent-contractor/personal-service classification note (see
  self-correction discipline above), added a hedged out-of-state-employer conflicts-of-law
  caveat (unresolved, flagged rather than asserted).

**Not done this round:** tier promotion for any of these 6 nodes -- all remain `DRAFT`.
`ca_eviction_v2.json` and the v0.3 held-out set untouched (frozen-artifact check confirms).

**Verification:** `python3 scripts/ci/validate_debt_schema.py` -- all 9 debt-track rules files,
including all 5 files touched this round (6 node edits span 5 files: `ca_debt_state_layer_v1.json`
carries both the `CA-BANK-ACCOUNT-EXEMPTION` 2nd-pass and `CA-CIVIL-ANSWER-DEADLINE` edits), pass
schema validation. `python3 scripts/ci/check_frozen_artifacts.py` -- both frozen artifacts match
committed hash, untouched.

---

## 2026-08-30, round 21 (Claude may now edit DRAFT-tier rule content directly; reframe from "3-model validation" to "3-model iteration")

**Context:** Read the full round-20 run (`run_20260830T111412Z`): 10/18 clean-pass (55.6%),
8 flagged. Read all 8 flagged nodes' JSON before responding, per Andy's direct question
("are you able to do this project successfully?"). Finding, reported to Andy in full: 7 of the
8 flags trace to genuine, well-reasoned, citation-backed adversarial-check findings -- every
single judge check that ran this round returned `agree: true` (zero cross-model legal
conflicts), and every flagged `gaps_found` entry was independently assessed
`realistic_and_common: true` AND `would_cause_wrong_answer: true`. The 1 remaining flag
(FDCPA-VALIDATION-NOTICE-1692g) was a different kind of issue -- not a legal gap, not a model
disagreement, but a title-phrasing bug in the node itself (see item 2 below).

**Andy's directive (verbatim, two messages):**
1. *"what if we changed our approach so that you could edit the rules files - this is still
   going to need a final review by me or other attorneys and it is still going to need further
   testing and validation - i'm trying to get us to move this forward much faster and not get
   bogged down in unnecessary 'approvals' that are too granular"*
2. Following my proposal below, confirmed: *"yes proceed"*

**Proposed mechanism (confirmed by Andy):** every rule node already carries a `tier` field
(`DRAFT` / `CORROBORATED` / `VALIDATED`) per the schema. Rather than requiring pre-approval
before Claude touches a rules file, the boundary moves to: Claude may edit rule content freely
**within DRAFT tier**, but may never promote a node out of DRAFT. Tier promotion -- the point at
which content is treated as ratified/relied-upon -- remains exclusively Andy's or named
counsel's call, unchanged from the standing discipline. Delivery mechanism is unchanged: every
edit still ships as a `git am --3way`-verified patch (no direct push access), now containing the
content fix itself rather than a memo describing it. Unaffected either way: `ca_eviction_v2.json`
(vProof1, byte-frozen) and the v0.3 held-out set -- separate, harder freezes tied to earlier
directives, not the DRAFT-editing discipline.

**Reframe (Andy's proposal, confirmed):** *"perhaps we can change the frame from - '3-model
validation' - to '3-model iteration' - and then separately we can deal with rigorous testing
later (but well before we ever release this code for use by anyone)."* This matches what round
20's data actually showed: the adversarial check's flags are draft-improvement findings (missing
statutory subsections, missing threshold questions, missing exceptions), not validation
failures. A 55.6% clean-pass rate under a "validation" frame reads as "45% broken." Under an
"iteration" frame the same run reads as "7 concrete, well-sourced improvements identified, 0
actual cross-model legal disagreements" -- which is what the models actually found. "Rigorous
testing before release" is explicitly deferred as a separate, later phase (live citation
verification, the mutation testing already flagged as "not yet built" in every node's
`tier_promotion_note`, and named-attorney ratification) -- not eliminated, just correctly
sequenced after iteration/drafting rather than conflated with it.

**What changed, this round:**

1. **7 nodes edited directly with the round-20 findings, in DRAFT tier**, each with a
   `logic.drafting_revisions` entry recording what changed and why (so review is "does this diff
   look right," not starting from an unannotated diff), each new statutory citation
   primary-source-researched this session (Cornell LII fetch for 15 U.S.C. § 1692e directly;
   WebSearch cross-referencing current-code mirrors for the CA/TX statutes and 11 U.S.C. 522(p),
   since direct `web_fetch` of leginfo.legislature.ca.gov and statutes.capitol.texas.gov timed
   out repeatedly this session -- same machine-hostility pattern already flagged for those two
   domains elsewhere in this corpus, so every new CA/TX citation is tagged source_tier B with an
   explicit "flagged for live re-verification, not silently assumed" caveat rather than presented
   as independently fetched):
   - `FDCPA-FALSE-DECEPTIVE-CATALOG-1692e`: added the missing §1692e(6)/(7) catalog items (also
     fixed the underlying `quoted_text`, which had silently skipped them via an unflagged
     ellipsis), added the §1692a(5)/(6) debt-collector and consumer-debt threshold predicates,
     added the formal-pleading exception to item (11).
   - `CA-SOL-WRITTEN-CONTRACT-DEBT`: added CCP §361 (borrowing statute / choice-of-law), flagged
     the secured-deficiency-judgment accrual exception, added CCP §360's revival-timing rule
     (payment before vs. after the bar).
   - `CA-SOL-ORAL-CONTRACT-DEBT`: added a classification warning against defaulting credit-card/
     revolving debt into the 2-year oral-contract bucket, added CCP §351 tolling (with its
     constitutional-limitation caveat preserved, not presented as a clean rule), fixed the
     expiration comparison to use the complaint's filing date (CCP §350) instead of today's date.
   - `CA-VEHICLE-EXEMPTION`: added CCP §704.060 (tools-of-trade alternative), CCP §703.140(b)
     (bankruptcy-only System 2 stacking), and the 90-day limit on insurance/execution-sale
     proceeds (CCP §704.010(b)).
   - `CA-BANK-ACCOUNT-EXEMPTION`: added CCP §704.080 (the separate, larger public-benefits/Social
     Security direct-deposit exemption -- corrected the run's own adversarial-check dollar figures
     against the actual statute, which are lower than what that check had guessed), clarified the
     minimum exemption is a single aggregate across all accounts, added CCP §703.020
     (natural-person-only).
   - `TX-HOMESTEAD-EXEMPTION`: qualified the "no dollar cap" statement with the 11 U.S.C.
     §522(p)/(o) bankruptcy cap (currently $214,000 for equity acquired in the 1,215 days before
     filing), added the federal-tax-lien override (26 U.S.C. §6321; *United States v. Rodgers*),
     added an explicitly-hedged HOA-lien caveat (genuinely unsettled/fact-specific under Texas
     law -- not asserted as a clean exception either way).
   - `TX-EXEMPT-PERSONAL-PROPERTY`: added Tex. Prop. Code §42.0021 (retirement accounts/IRAs,
     unlimited, outside the aggregate cap), added the item-level sub-caps §42.001 alone doesn't
     capture (jewelry 25% of the aggregate, one vehicle per licensed driver, two firearms), added
     the §42.004/§42.005 fraudulent-transfer and child-support-lien overrides.

2. **`FDCPA-VALIDATION-NOTICE-1692g` retitled**, not content-edited. Root cause, confirmed by
   reading `run_corroboration.py`'s `run_node()` directly: the Stage A derivation prompt is built
   as `f"Title: {node['title']}\n\nSource text...\n\nDerive the answer strictly from this text."`
   This node's title was phrased as a case-specific determination ("was a compliant notice
   provided, and is the consumer still within the dispute window?"), but the source text only
   states the general legal standard -- there's no actual notice/receipt date to apply it to.
   Per `SYSTEM_PROMPT_DERIVATION`'s own instruction not to guess, 2 of 3 models correctly
   returned `grounded: false`; the judge then correctly skipped rather than compare a grounded
   result to two non-grounded ones. This had been carried as an open "grounding-ambiguity" item
   since round 19 without a confirmed root cause -- it is a title-phrasing bug, not a legal
   disagreement and not a rules-content gap. Retitled to a rule-statement framing matching every
   other node's pattern ("required content, and how the 30-day dispute window is calculated").
   No change to the derived_from text, checklist, or consequences, which were already correct.

**Not done this round:** tier promotion for any of these 7 nodes -- all remain `DRAFT`, per the
mechanism above. A dedicated FDCPA-THRESHOLD-DEBT-COLLECTOR node (the 1692a(6) exclusion list
beyond the single-clause excerpt used here) is flagged as HORIZON work if a future node needs it.
The HOA-lien question on TX-HOMESTEAD-EXEMPTION is deliberately left unresolved/hedged rather
than guessed at.

**Verification:** `python3 scripts/ci/validate_debt_schema.py` -- all 9 debt-track rules files,
including all 4 edited this round, pass schema validation. All 4 edited files independently
re-parse as valid JSON. Corroboration-runner changes (none needed this round -- the fix was a
data change to the node's own `title` field, not to `run_corroboration.py`).

---

## 2026-08-30, round 20 (add a materiality bar -- the point is corroborating Claude's primary work, not litigating every technical difference)

**Context:** Andy ran the full corpus under round 19's fix (`run_20260830T103213Z`): 2/18
clean-pass, 16 flagged -- worse than before round 19, and Andy said so directly. Read the run
JSON node by node before responding. Both round 19 fixes were confirmed working exactly as
intended -- every judge note read explicitly recognized "completeness differences only... without
contradicting" and returned `agree: true`. What actually happened: round 19 also fixed the
adversarial-stage truncation bug that had been silently disabling that check for this project's
entire history (every prior run's `gaps_found` was effectively always empty, parse failures
discarded real findings). With that bug fixed, the adversarial pass ran at full strength for the
first time and found *something* to flag on nearly every node -- some genuinely important
(FDCPA-FALSE-DECEPTIVE-CATALOG's encoded catalog skips from subsection (5) straight to (8),
missing (6) and (7) entirely -- a real gap in what's encoded), some trivial (a $0.03 interest
discrepancy, a corporate-suffix variant). Every one, material or not, was gate-blocking identically.

**Andy's directive, verbatim:** *"we need a materiality bar - the concept here is that you -
claude cowork - should be able to code at something approaching 90% accuracy - then we run it
through 2 more models to validate what your findings are - unless there is a material disagreement
there should not be a flag... if we are looking for any difference between the 3 models, we'll
find one every time and default to having a human attorney review every difference - the problem
with that is that it would defeat this entire cjac project - why code if at the end of the day the
human attorneys need to do a granular check of the equivalent of every line of code - the project
would essentially fail."*

**The corrected mental model:** Claude (Cowork) is the primary author of the rule encoding. The
other two models corroborate that work -- they are not three co-equal votes where any split
between them forces human review. Only a difference that would actually change the practical
answer a real person gets warrants a flag; a technical or rare-edge distinction, however real,
does not.

**What changed -- a materiality bar added to both checks that can flag a node:**
- `SYSTEM_PROMPT_JUDGE`: round 19 already excluded a mere omission from counting as disagreement.
  Round 20 adds an explicit materiality qualifier on top -- a real conflict only makes `agree: false`
  if it "would change the practical answer or advice given to a typical person in a common
  scenario." A materially different dollar amount, deadline, or standard still counts; a
  technically-real but inconsequential wording distinction does not.
- `SYSTEM_PROMPT_ADVERSARIAL`: rewritten to require two separate, explicit assessments before an
  edge case counts as a gap -- `realistic_and_common` (is this a fact pattern an actual person
  might plausibly present, not a contrived corner case) and `would_cause_wrong_answer` (would the
  rule, as encoded, actually give a wrong or materially misleading answer, not just an
  incomplete-but-harmless one). `exposes_gap` is true only when both are true. Nothing is hidden --
  every edge case the model proposes, material or not, is still preserved in full in the run JSON;
  only whether it blocks CLEAN-PASS changes. This directly serves the "use these runs to make the
  underlying code more accurate" goal Andy named -- the immaterial findings are still there as
  future improvement input, they're just not gate-blocking today.

**Not done, and why:** did not touch the FDCPA-VALIDATION-NOTICE "grounded" ambiguity (round 19's
open item) -- unrelated to materiality, still needs its own considered fix. Did not fix the missing
§1692e(6)/(7) subsections found by tonight's (correctly-working) adversarial check -- that is a
genuine rules-content gap, not a pipeline issue, and belongs in its own round once flagged by a
live run under the new materiality bar, not folded into an infrastructure patch.

**Verification:** `python3 -m py_compile` clean. `--dry-run --demo-corpus-only --skip-citation-check`:
18/18 clean-pass, unchanged (dry-run doesn't exercise live model-call paths, so this confirms no
syntax/control-flow regression -- the actual materiality behavior needs a live re-run to confirm,
same limitation as every prompt-only change this project has shipped). Both rewritten prompts
read back correctly via direct module import -- no string-escaping errors, learned from actively
checking this after round 19's prompt edit was suspected (correctly ruled out) as a possible bug
source. Frozen eviction artifact SHA unchanged.

---

## 2026-08-30, round 19 (recalibrate the semantic-agreement judge to only flag real conflicts, plus two real infra bugs found by reading the actual data)

**Context:** After round 18 shipped, Andy ran the full 18-node live corroboration under the new
rules (citation check skipped, `run_20260830T094127Z`): 12/18 clean-pass, 6 flagged, 66.7%
grounded-agreement -- still short of the 90% gate. Andy: "still not working well - thoughts?"
Rather than guess again, read all 6 flagged nodes in full before proposing anything.

**Finding, with evidence, not assumption:** citation-liveness noise is genuinely gone (confirmed
-- zero of the 6 flags trace to it). The 6 broke into three real, distinct categories:

1. **Four of six** (FDCPA-FALSE-DECEPTIVE-CATALOG-1692e, CA-SOL-WRITTEN-CONTRACT-DEBT,
   CA-VEHICLE-EXEMPTION, TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY) shared one exact pattern:
   all three models stated the identical governing rule with zero contradiction, but one model
   (usually Gemini) omitted a secondary, non-dispositive detail (an exception clause, a procedural
   deadline) that the other two included. This was not a bug -- the round-3 (2026-08-26) judge
   prompt explicitly instructed exactly this: "if one analysis states a real substantive fact that
   another omits entirely, that is a genuine disagreement worth flagging." A deliberate design
   choice at the time, but on this evidence it was gating CLEAN-PASS on completeness-of-summary,
   not correctness-of-law -- every single instance found was an omission, never an actual conflict
   (nobody said "X" while another said "not-X").
2. **One of six** (FDCPA-UNFAIR-PRACTICES-CATALOG-1692f): a plain Gemini 60-second timeout. Round
   17's retry-on-503 didn't cover this -- a `TimeoutError` takes a different code path that
   returned immediately, bypassing the retry loop entirely. The exact failure class round 17 was
   supposed to fix, just a different exception type.
3. **One of six** (FDCPA-VALIDATION-NOTICE-1692g): a genuine prompt-design ambiguity. The rule text
   states legal criteria with no specific fact pattern to apply them to; Claude answered
   `grounded: true` anyway, GPT-5.5 and Gemini both answered `grounded: false` ("can't determine
   compliance without case facts"). Models are interpreting what "grounded" means differently for
   rule-statement nodes vs. fact-dependent-application nodes. Not fixed this round (needs a
   considered prompt change, not a quick patch) -- logged as open work, not silently dropped.

**Separately found while reading (not the cause of any of today's flags, but real):** the
adversarial-gap-finding stage's JSON response was getting truncated on several nodes -- visible in
the raw truncated text, which showed a real, correctly-identified gap, that then got silently
discarded because the cut-off JSON failed to parse. Root cause: `call_anthropic()` hardcoded
`max_tokens=1500` for every call site, including the adversarial stage's 3-edge-cases-with-
descriptions request, which routinely needs more than that.

**Andy's directive on the four omission-pattern flags:** *"if an omission but not a conflict then
we should not flag; we should only flag actual conflicts."* Implemented exactly that.

**What changed:**
- `SYSTEM_PROMPT_JUDGE` rewritten: an omission by itself is now explicitly instructed to NOT count
  as disagreement. `agree: false` is reserved for an actual conflict -- two analyses stating
  something that cannot both be true (different amounts, different deadlines, different standards,
  or one asserting a rule/exception applies while another asserts it does not). Completeness
  differences are still surfaced in `agreement_notes` for visibility -- informational, not gating.
- `call_gemini()`: a `TimeoutError` now falls through to the same retry-once-then-fail pattern as a
  transient 503, instead of returning immediately on the first timeout.
- `call_anthropic()` gained a `max_tokens` parameter (default 1500, unchanged for derivation and
  judge calls); the adversarial call site now requests 3000, enough headroom for 3 edge cases with
  descriptions without truncating.

**Learning from this, per Andy's ask -- not just fixing today's flags but the pattern:** across
every round this project has run (now 19), zero flags have ever traced to the derived law actually
being substantively wrong. Every flag, across every round, has been either (a) a citation-liveness
/ infrastructure problem (rounds 9-17's dominant category, now decoupled from the gate per round 18)
or (b) a judge-calibration artifact treating incomplete-but-correct as equivalent to wrong (today's
dominant category, now fixed). That is itself useful signal: the 3-independent-model-derivation
mechanism is doing its actual job reliably -- getting three frontier models to independently derive
the same governing rule from the same cited text and converge on it. The bottleneck to date has not
been legal-accuracy risk; it has been pipeline calibration noise sitting on top of a mechanism that
already works. Concretely, going forward: (1) triage every flag to its real category (infra /
judge-calibration / genuine legal gap) with actual evidence before proposing any fix -- this
session's method, now proven twice, not a one-off; (2) treat "does this actually conflict" as the
bar for model disagreement, not "did every model mention every detail"; (3) build retry robustness
for a known transient-failure class proactively across all its variants (503 AND timeout, not just
the one observed first); (4) with today's fixes, the corroboration harness itself should mostly stop
being the thing that needs debugging -- the more valuable use of build time from here is likely
authoring and corroborating NEW nodes/coverage, not continuing to re-litigate the harness.

**Not done, and why:** did not fix the FDCPA-VALIDATION-NOTICE "grounded" ambiguity (category 3
above) -- it needs a considered prompt clarification (what does "grounded" mean when the source
text states criteria but no fact pattern), not a quick patch alongside two unrelated fixes; logged
as open work for a future round. Did not re-run the earlier flagged run's disagreement-queue
entries retroactively -- round 19's fixes apply going forward, per the same append-only,
non-retroactive discipline as every prior round.

**Verification:** `python3 -m py_compile` clean. `--dry-run --demo-corpus-only --skip-citation-check`:
18/18 clean-pass, unchanged (dry-run doesn't exercise live model-call code paths, so this confirms
no syntax/control-flow regression, not the live behavior itself -- that needs a live re-run).
`call_gemini`'s retry structure verified by direct source inspection: a `TimeoutError` on attempt 0
now falls into the same `continue`-then-retry path as a transient 503, only returning the error
after a second attempt also fails. Frozen eviction artifact SHA unchanged.

---

## 2026-08-29/30, round 18 (decouple CLEAN-PASS from citation liveness, per Andy's explicit directive)

**Context:** After round 17 landed and was spot-checked, Andy authorized the full 18-node re-run
(`--live --demo-corpus-only`, item 1 of two options offered). Early results (5 of the first 6 nodes
flagged, a cluster of FDCPA nodes untouched by round 17) prompted Andy to ask directly whether this
approach is productive after ~20 rounds of largely administrative/tooling failures. Reviewing the
data honestly: of the last full run's 13 flags, 11 traced to pipeline/infrastructure noise (bot-blocking,
stale User-Agent, JS-rendered pages, transient model 503s, a self-inflicted formatting bug) and only 2
were genuine legal-completeness gaps -- zero were "the law is wrong." Citation-liveness checking (can a
plain HTTP GET fetch a byte-matching page from a third-party website *right now*) has been the dominant
source of that noise across rounds 9-17, and answers a different question than "is the legal rule
correctly derived and complete" -- the actual point of this pipeline.

**Andy's directive (verbatim):** *"we should proceed without a live citation verification - that can be
done later. for now please proceed with the approach that we are validating the legal rule and not focus
on the byte for byte match."*

**What changed:** `scripts/corroboration/run_corroboration.py` already had a `--skip-citation-check` flag,
but it was built for cost-free dev iteration, not for this purpose -- `clean_pass` required
`all_citations_verified is True` unconditionally, so a *skipped* check (`all_citations_verified is None`)
still failed every node, which is the opposite of useful here. Fixed the gating formula to
`(all_citations_verified is not False)` -- a skipped check no longer blocks CLEAN-PASS; only an actively
FAILED live check still does. This decouples the two questions the pipeline was conflating: legal-rule
quality (grounded derivation + semantic agreement + adversarial check) now determines CLEAN-PASS on its
own; citation liveness becomes a separate, deferred concern, to be reinstated later per Andy's own framing
("that can be done later"), not abandoned.

**Honesty of claims, not just code:** a skipped citation check is not the same as a verified one, so this
round also updated every place the run output or the spec could imply otherwise: the `tier_promotion_note`
and `demo_gate_metrics.basis` text now explicitly say citation verification was skipped when it was: the run
prints a NOTE banner at both start and end when `--skip-citation-check` is used; the run JSON records
`citation_check_skipped: true` at the top level; and `docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md` §8's
CONCEPT-DEMO claim-language section gets a new subsection (below) giving the exact alternate framing
sentence to use for any showing run in this mode -- the existing framing sentence claims "citations
verified against live sources," which would be false while this mode is active.

**Not done, and why:** did not delete or disable citation verification -- `verify_citation()`, the
`manual_verification` mechanism (round 17), and the `--skip-citation-check`-free code path are all
untouched and fully functional; this is an opt-in flag, off by default. Did not re-run the earlier
in-progress live run under the old gating (that run, `run_20260829T18....Z`, already spent real API cost
under the old rules and its output stands as-is as a data point). Did not change anything about how
disagreements get filed to the queue -- a FAILED (not skipped) citation check still files a
CITATION-CHECK-FAILED entry exactly as before.

**Verification:** `python3 -m py_compile` clean. Dry-run comparison, same node, with and without the new
flag: without `--skip-citation-check`, unchanged behavior (CLEAN-PASS, citation method `dry-run-synthetic`).
With it, `citation_check.results[0]` shows `verified: null, method: "skipped"`, `all_verified: null`, and
the node still resolves to `status: CLEAN-PASS` -- proving the fix (under the old formula this would have
been FLAGGED). `tier_promotion_note` and `demo_gate_metrics.basis` both confirmed to carry the skipped-mode
caveat text in the resulting run JSON. Frozen eviction artifact SHA unchanged; JSON schema untouched (no
rules-file changes this round).

---

## 2026-08-29, round 17 (post-run triage: 4 pipeline-bug fixes from the first full 18-node live run)

**Context:** Andy ran the full 18-node live corroboration check (`run_20260828T220708Z`): 5/18 clean-pass, 13 flagged, demo-gate not met. Triaged every flag before proposing any fix -- confirmed zero of the 13 were genuine "the law is wrong" disagreements; two were minor, legitimate completeness gaps (exactly what corroboration is supposed to catch, left as-is for attorney review); the other eleven were pipeline/tooling bugs, several newly discovered. Andy approved fixing the four pipeline categories.

**Fix A -- statutes.capitol.texas.gov regression (4 nodes: TX-SOL-CONSUMER-DEBT, TX-WAGE-GARNISHMENT-PROHIBITION, TX-HOMESTEAD-EXEMPTION, TX-EXEMPT-PERSONAL-PROPERTY):** direct evidence (browser render, not guessed) showed the site is now a client-rendered SPA -- a plain HTTP GET to any specific section URL returns an identical 250,874-byte generic shell regardless of which statute was requested (confirmed across all 4 URLs), a regression from round 13's "flaky but retriable" behavior to a deterministic wrong-page response that retry-on-flake can't fix. Manually confirmed via direct browser rendering (JS executed) that the real statute text loads client-side and matches each node's quoted_text verbatim. Added a `manual_verification` mechanism to `verify_citation()` (round 17): when a `derived_from` entry carries a `manual_verification: {note, date}` field, the checker returns `verified: true, method: "manual"` without a network call, recording who/how/when instead of silently treating a structurally-unverifiable-by-design source as an unexplained failure. Applied to all 4 TX statute URLs. Same fix applied to the Craddock/CourtListener citation (`TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY`), which returns an HTTP 202 JS-loading-shell to a plain GET even though the CourtListener API (used earlier this session to confirm the quote) returns the real opinion text. This is the same class of limitation as the already-documented azleg.gov JS-gating (round 9), now handled explicitly and visibly rather than left as an unexplained flag.

**Fix B -- transient Gemini 503s (hit 4/18 nodes in the last run):** `call_gemini()` had no retry logic, unlike citation_check's retry-on-flake (round 13). Added a one-retry, brief-pause pattern scoped specifically to the transient-overload signature (503/UNAVAILABLE) so a real error still fails fast.

**Fix C -- eCFR/Cornell normalization bug, tooling extended (not fully root-caused):** confirmed via the run's diagnostics that this is systematic (hit a Cornell citation too, not just eCFR) and reproducible (same word_overlap_ratio=1.0-but-short-prefix-match signature every time). Investigated directly this session: browser-rendered the eCFR page in question and found no obvious structural cause; raw HTML fetches are blocked from this sandbox's network egress (confirmed via direct test -- proxy returns 403), so the exact byte-level cause could not be pinned down here. Rather than guess further or force an unverified fix, added `_raw_context_at_break()`: captures a slice of raw, un-stripped HTML around the match-break point in the citation_check diagnostics, so Andy's next live run (normal network access) will surface the actual markup and let this be fixed with evidence instead of another guess.

**Fix D -- TX-JUSTICE-COURT-DEBT-ANSWER-DEADLINE self-inflicted authoring bug:** the stored `quoted_text` for the Rule 502.5 secondary-source citation literally began with an editorial bracket note ("[Secondary-source corroboration, not independently pulled...]") that was never meant to be matched verbatim against the live page -- guaranteed to fail every time. Moved the editorial note to a new `sourcing_note` field and left `quoted_text` as only the actual quoted material.

**Not done, and why:** did not force a fix for item C beyond the diagnostic tooling -- an unverified guess at the byte-level cause would be worse than an honest "needs one more live data point." Did not touch AZ/UT/NY citations (separate, already-tracked tier-audit gap, not part of this run's flags).

**Verification:** `--dry-run --demo-corpus-only` (no cost) -- 18/18 clean-pass, up from the round-16-era baseline, confirming none of the four fixes broke anything. JSON schema-valid (12/12 debt rules files), `manual_verification` and `sourcing_note` fields confirmed schema-safe (`derived_from` entries allow `additionalProperties: true`). `verify_citation()`'s manual-verification short-circuit and `_raw_context_at_break()` unit-smoke-tested standalone. Frozen eviction artifact SHA unchanged. Runner compiles clean.

## 2026-08-28, round 16 (Direction item 3 prep: archive stale disagreement-queue entries before the full 18-node live run)

**Context:** Andy's directive item 3 required confirming the disagreement queue is "clean of runs 1-2 artifacts so the new flags land in an empty lane" before delivering the full-run command. Rather than assume this, Andy copied his actual current `docs/DEBT_DISAGREEMENT_QUEUE.md` out for inspection. It was not clean: 68 open entries across every node in the demo corpus, all filed during live runs on 2026-08-26 evening (`run_20260826T174558Z` through `run_20260826T202441Z`), all with blank Resolution fields.

**Finding:** every one of those 68 entries predates this session's Round 12-15 fixes. The CITATION-CHECK-FAILED entries trace almost entirely to causes already fixed: a stale User-Agent (Round 11), FindLaw/Justia bot-blocking now bypassed by the CA re-pin to leginfo.legislature.ca.gov and the TX re-pin to statutes.capitol.texas.gov + CourtListener (Rounds 12-13), and the eCFR ellipsis mismatch (Round 12). Nearly every MODEL-DISAGREEMENT entry rests solely on the numeric/citation-fingerprint heuristic, which Round 11 demoted to a secondary, non-gating diagnostic in favor of LLM-judged semantic agreement -- so a bare fingerprint mismatch is no longer this project's disagreement signal at all. None of these are genuine attorney-level legal disagreements; they are stale pipeline artifacts from before the fixes that generated them were even known.

**What changed:** `docs/DEBT_DISAGREEMENT_QUEUE.md` restructured -- all 68 entries plus the existing Round-9 purge note moved from "## Open" into a new "## Archived -- Pre-Fix Diagnostic Runs (archived 2026-08-28)" section, with a head-note explaining why each category is stale and what would have to be true for an entry to legitimately re-file. Per the append-only discipline, nothing was deleted or edited: every entry, its three per-model derivations, and its blank Resolution/Resolved-by/Date fields are preserved byte-for-byte under the archive heading. The "## Open" section itself is now empty and ready for the upcoming full-corpus run's fresh flags.

**Note on delivery:** this patch assumes Andy has already committed his local live-run backlog (the queue entries the runner appended locally but never committed) as its own commit first -- see the apply instructions delivered with this patch. Building the patch this way (against the post-backlog-commit state) avoids a merge conflict that a naive patch-from-round-15 would hit.

**Not done, and why:** did not resolve, adjudicate, or characterize any entry as correct/incorrect -- that determination belongs to Andy or certifying counsel. Did not touch AZ/UT/NY citations (still pinned to FindLaw/secondary sources per the round-9 tier audit; a live run will still likely re-flag those CITATION-CHECK-FAILED for real, unfixed reasons, and that is expected and correct).

**Verification:** diffed the archived file against Andy's pre-archive copy -- confirmed the only lines added are the archive section header and explanatory note; every one of the 68 entries and the purge note reproduce character-for-character. Verified end-to-end by reproducing Andy's exact local sequence (fresh clone + Round 10-15 chain + a backlog commit matching his committed queue file byte-for-byte) and confirming this patch applies clean on top with no conflict.

## 2026-08-28, round 15 (Direction item 5: claim-language card + demo quickstart for the consumer-debt-validation skill)

**Context:** Andy's directive item 5 asked for skill packaging and scenario readiness as a parallel GREEN lane. Surveying the repo first (not duplicating existing work): the `consumer-debt-validation` skill, the 5 concept-demo scenarios (`scripts/corroboration/scenarios.json`), tier-label surfacing, and the mandatory framing sentence were all already built (2026-08-26, tasks in that day's session). What was missing, specifically: a standalone one-page claim-language reference and a short "how Andy runs this live" note -- both explicitly requested by name in the directive.

**What changed:**
1. **`plugins/consumer-debt/skills/consumer-debt-validation/CLAIM_LANGUAGE_CARD.md`** (new) -- one page: the exact opening framing sentence, permitted claim language with each number's basis (grounded-agreement rate + scenario pass rate, always together), prohibited language, the Band 3 refusal-boundary talking point, and a ready answer for "how do you know it's right." Sourced directly from spec §8's CONCEPT-DEMO row, not paraphrased.
2. **`plugins/consumer-debt/skills/consumer-debt-validation/HOW_TO_RUN.md`** (new) -- three steps, written to be usable without reading from a screen mid-conversation (voice-mode-ready per the directive): open with the framing sentence, describe the person's situation naturally (skill handles intake), close with both demo-gate numbers from the actual last live run. Includes a note on what to do if something hits a below-CORROBORATED node or a genuine judgment call.
3. **`SKILL.md`** updated (version bump to 0.3.0-concept-demo) with cross-references to both new files from the relevant sections (§5 Claims discipline, §7 Prepared demo scenarios) rather than duplicating their content inline.

**Not done, and why:** did not rebuild the skill's core intake/decision logic, the 5 scenarios, or the tier-labeling behavior -- all already correct and already wired to the live `rules/debt/` corpus per the 2026-08-26 reconciliation note in `SKILL.md`. Re-doing that would have been redundant work, not requested.

**Verification:** `scenarios.json` still valid JSON (untouched, cross-referenced only). No code changed this round -- markdown-only, reviewed for accuracy against spec §8's exact wording (framing sentence copied verbatim, not retyped from memory in a way that could drift).

## 2026-08-28, round 14 (Direction item 2: FDCPA (b)(4) diagnostic pinpoint, hypothesis pre-registered)

**Context:** Andy's directive item 2 asked for the unresolved FDCPA-REGF-CALL-FREQUENCY-1006.14b second-citation anomaly (12 C.F.R. 1006.14(b)(4)) to be staged so it's resolvable immediately from the next live run's diagnostics, not another round of guessing -- and asked for a pre-registered hypothesis in the queue entry.

**What changed:**
1. **Added `_longest_matching_prefix_len()` and wired it into `verify_citation()`'s diagnostics.** When `word_overlap_ratio` is high (all words present) but `verified` is False -- exactly the (b)(4) node's symptom on the last live run -- the diagnostics block now includes `longest_matching_prefix_chars` (how many leading characters of the citation matched the live page contiguously before breaking) and `text_at_break_point` (the next ~40 characters that were expected but not found there). This turns "somehow didn't match" into an exact, actionable break point on the very next run.
2. **Pre-registered hypothesis** (also in the new function's docstring, so it travels with the code): word_overlap_ratio was already 1.0 on the last run (every word of the quote is genuinely on the page), and a clean markdown approximation of the same eCFR page matched this exact quoted_text with zero changes needed when tested this round -- so the live mismatch most likely comes from something in eCFR's *raw* HTML that a plain-text approximation doesn't reproduce: an internal cross-reference link inserted mid-sentence (eCFR auto-links defined terms and paragraph references), adding or removing a character of whitespace at a tag boundary that `_strip_html`'s space-substitution doesn't fully absorb, or a smart-quote/entity variant not covered by `_normalize_for_match`. **Did not guess further or force a fix** -- this needed real HTML the sandbox can't fetch; the diagnostic above will confirm or refute it directly.
3. This node's own `CITATION-CHECK-FAILED` entry will auto-file into `docs/DEBT_DISAGREEMENT_QUEUE.md` on the next live run per the runner's existing append-only behavior (per the queue file's own header: the runner appends, never hand-edits) -- no placeholder entry was hand-written here, to avoid it going stale or conflicting with the real one.

**Verification:** `py_compile` clean, schema validation (9/9 pass), frozen-artifact SHA unchanged, `--dry-run --demo-corpus-only` still 18/18 clean-pass (this change only adds diagnostic fields, doesn't alter `verified` logic). Sanity-tested the new pinpoint function against a synthetic near-miss (an inserted space) and confirmed it correctly located the break point.

## 2026-08-28, round 13 (Direction: TX re-pin -- statutes + Craddock case, Rule 329b/502.5 flagged as genuine open gap)

**Context:** Andy issued a sequenced directive ("Demo Critical Path") after the round-12 CA re-pin was confirmed live. Item 1: TX is the last demo-gating sourcing work (federal + CA are clean). This round covers item 1 only.

**What changed:**
1. **Re-pinned to statutes.capitol.texas.gov (Tier A):** `Tex. Civ. Prac. & Rem. Code § 16.004(a)` (SOL), `Tex. Const. art. XVI, § 28` (wage garnishment prohibition), `Tex. Prop. Code §§ 42.001(a), 42.001(b), 42.002(a)` (exempt personal property) -- 5 citations across 3 nodes, previously Justia/FindLaw (Tier C). Confirmed directly by fetching the real pages this round (not guessed): the content is genuinely reachable by plain HTTP, no browser JS required, unlike AZ. But the site proved **intermittently flaky** -- the same exact URL alternated between real statute text and a bare navigation shell across successive fetches (confirmed on `PR.42.htm` and the large `CN.16.htm` Constitution-article page, which needed 3 attempts). Added a retry-once mechanism to `verify_citation()` in `run_corroboration.py`: if the first fetch returns 200 but doesn't verify, wait 2 seconds and try once more before giving up. A genuinely wrong quote still fails both attempts -- this only absorbs the observed serving flakiness, it doesn't mask real mismatches.
2. **Three more ellipsis-degraded `quoted_text` entries found and fixed** (same pattern as round 12's eCFR fix): `§16.004(a)`, `§42.001(a)`, `§42.001(b)`, and `§42.002(a)` all had authored `...` standing in for real statutory text. Replaced with verbatim text fetched directly from the source this round.
3. **Craddock v. Sunshine Bus Lines, Inc.** (the controlling case for TX's default-judgment set-aside standard) re-pinned from lawpipe.com (Tier D) to CourtListener (Free Law Project nonprofit -- Tier A/B for case law, same standard as Cornell LII for statutes). Verified via the CourtListener API directly: `quoted_text` matches the opinion's actual holding language verbatim (opinion_id 3940166).
4. **Genuine gap found and flagged, not forced through:** `Tex. R. Civ. P. 329b` (both citations, on the same default-judgment-set-aside node) and `Tex. R. Civ. P. 502.5` (justice-court answer deadline) remain Tier C/D. Researched thoroughly: the only official (Tier A) source for the current Texas Rules of Civil Procedure is a PDF on txcourts.gov -- no current official HTML version exists. This session's fetch tooling, and the runner's `verify_citation()` itself (reads `resp.text` as HTML), can't extract meaningful text from a PDF. Pinning to the PDF would silently break verification, not fix it. This is a **tooling-capability gap**, not a sourcing-effort gap -- flagged for Andy to decide: add PDF support to the runner, or treat these two rules as a documented tier-hierarchy exception. Since the affected node is the Band 3 refusal-scenario candidate, this is called out as demo-relevant, not buried.
5. **`docs/SOURCE_TIER_AUDIT_20260826.md`** updated (addendum, append-forward) with the full round-13 findings above.

**Verification:** schema validation (9/9 pass), frozen-artifact SHA unchanged, `py_compile` clean, `--dry-run --demo-corpus-only` still 18/18 clean-pass. Retry logic unit-sanity-checked in dry-run mode. **Not yet live-verified:** none of round 13's re-pins have been tested against a real live run yet -- recommend including the TX nodes in the next `--live` spot-check alongside FDCPA-(b)(4) (item 2 of the directive).

## 2026-08-26, round 12 (Live spot-check follow-up: eCFR quoted-text ellipsis fix, CA re-pinned to leginfo.legislature.ca.gov)

**Context:** Round 10+11's patch had never actually applied to Andy's repo despite the terminal showing no error (root cause: round 10's `git am` silently produced no commit; round 11 then failed because it expected round 10's context). Rebuilt and delivered as one combined, freshly-verified patch (round "10+11 reconciled"), applied clean via `git am --3way` on a fresh clone of the real pushed repo. A live 2-node spot-check immediately after (`FDCPA-REGF-CALL-FREQUENCY-1006.14b`, `CA-SOL-WRITTEN-CONTRACT-DEBT`) confirmed the LLM-judge fix itself works correctly -- it agreed on node 1 and correctly caught a real disagreement on node 2 (two models each dropped a different clause of the CA SOL rule) -- but both nodes still came back FLAGGED on citation verification, for two distinct, unrelated reasons investigated this round.

**What changed:**
1. **eCFR quoted_text ellipsis fixed.** `FDCPA-REGF-CALL-FREQUENCY-1006.14b`'s first citation (`12 C.F.R. § 1006.14(b)(2)(i)-(ii)`) had an authored `"(i) ...a debt collector is presumed..."` in its `quoted_text` -- the `...` was an elision marker from whoever wrote it, not real regulation text, so it could never exact-match eCFR's live page even though round 11's User-Agent fix now pulls the genuine 75KB page (word_overlap_ratio 1.0 confirmed the real content was there, just not as a contiguous substring starting with an ellipsis). Fetched the verbatim eCFR text directly this round and replaced the quote. The node's second citation (§1006.14(b)(4)) also showed `verified: false` in the live run despite testing as an exact match against a clean approximation of the page -- root cause not fully pinned down (this sandbox can't fetch eCFR's raw HTML directly, only a pre-rendered text version via the fetch tool), left as an open item for the next live run's diagnostics.
2. **All 7 California nodes re-pinned from Justia/FindLaw (Tier C) to leginfo.legislature.ca.gov (Tier A)**, per Andy's ratification. URL format (`codes_displaySection.xhtml?lawCode=CCP&sectionNum=<N>.` -- trailing period required) confirmed correct via independent web search, not guessed. **Caveat, flagged not hidden:** leginfo.legislature.ca.gov is unreachable from this session's sandbox (network-egress blocked, likely also JS-rendered like azleg.gov was) -- the URL is correct but this session could not mechanically confirm the live page content matches each node's existing `quoted_text` (left unchanged; same statute, same words, previously sourced via Justia/FindLaw's mirror). `source_tier` bumped to A with a `tier_rationale` documenting this caveat on all 11 affected citation entries. Andy's next live run will give the real mechanical answer, same pattern as the eCFR User-Agent confirmation.
3. **`docs/SOURCE_TIER_AUDIT_20260826.md`** updated (addendum, append-forward) to reflect CA's re-pin and both open items above.

**Verification:** schema validation (`scripts/ci/validate_debt_schema.py`, all 9 files pass), frozen-artifact SHA unchanged (`ca_eviction_v2.json` untouched), `--dry-run --demo-corpus-only` still 18/18 clean-pass (unaffected by these 2 JSON-content-only changes). **Not yet live-verified:** the eCFR (b)(4) open item and the CA leginfo re-pin both need one more live run to confirm from real diagnostics, not sandbox guesswork.

## 2026-08-26, round 11 (Citation checker User-Agent fix + LLM-judged semantic agreement replaces numeric fingerprint)

**Context:** Andy applied round 10 and ran the full live demo corpus. Result: 0/18 clean-pass, 0% gate. Rather than guess, pulled the complete run JSON off his machine and analyzed every citation check and fingerprint across all 18 nodes directly.

**Finding 1 -- citation checker structurally couldn't reach three load-bearing domains.** eCFR.gov returned the exact same 10,596-byte response on every single check regardless of which of three different regulation sections was requested -- not real content. Independently fetched the same URL and got the full, real regulation text with no issue. Root cause: eCFR displays an "unsupported browser" notice for non-standard user agents, and the runner was sending a made-up UA string (`Mozilla/5.0 (CJaC corroboration runner)`) with none of the tokens (Chrome/, Safari/, Firefox/) that basic bot-detection checks for. FindLaw and Justia 403'd on every single request in the same run -- consistent with the same class of issue. **Fix:** `verify_citation()` now sends a standard browser User-Agent (plus Accept/Accept-Language headers) instead of the custom string. This is normal practice for polite programmatic access to public, unauthenticated legal text -- not an attempt to evade any access control tied to identity, payment, or consent. Not independently re-verified live (this session's sandbox can't reach these domains directly), so Andy's next live run is the real test.

**Finding 2 -- the numeric-fingerprint agreement check had a third distinct false-positive pattern.** On `FDCPA-REGF-CALL-FREQUENCY-1006.14b`, Claude's answer referenced "Paragraph (b)(2)(ii)" later in its text -- the citation-stripper recognizes "Section," "Rule," "Article" as citation lead-in words but not "Paragraph," so the bare "(2)" leaked into the fingerprint as a spurious fact. Given this is the third distinct false-positive pattern found in live use (citation noise, the "no one" pronoun, now this), and each was only caught after surfacing in a real live run rather than anticipated in advance, brought this to Andy as a methodology question rather than patch a fourth regex case.

**Andy's decision (ratified):** replace the numeric fingerprint as the primary grounded-derivation agreement signal with an LLM-judged agreement check -- a fourth model call per node that reads all three anonymized derivation summaries and judges whether they substantively agree, added as `judge_semantic_agreement()` / `SYSTEM_PROMPT_JUDGE`. The numeric fingerprint is retained and still computed (`fingerprints_diagnostic_only` / `fingerprint_agreement_diagnostic_only` in the run output) as a secondary, non-gating diagnostic -- it's fast, free, and occasionally a useful cross-check, just no longer the pass/fail criterion. `CLEAN-PASS` now requires `semantic_agreement` (the judge's verdict) instead of `fingerprint_agreement`. Disagreement-queue entries now carry the judge's plain-language `agreement_notes` as the evidence, which is far more useful for Andy's review than a raw set of numbers. Known, flagged limitation: the judge call uses Anthropic, which is also one of the three models being judged -- summaries are presented anonymized (unlabeled "Analysis 1/2/3") as a standard mitigation for self-preference bias, not a full fix. Cost estimate bumped from ~$0.35 to ~$0.45/node (18-node demo corpus: ~$6 to ~$8; full 37-node corpus: ~$13 to ~$17) to reflect the added call.

**Verification:** schema validation (9/9 pass), frozen-artifact check (2/2 pass), py_compile, unit-level tests of `judge_semantic_agreement()` (dry-run payload, skip-path for missing summaries, disagreement-message formatting), full `--dry-run --demo-corpus-only` end-to-end (18/18 clean-pass with the new judge wired in). README.md updated to describe the new methodology and cost estimate, including an explicit note on the self-judging limitation. Fresh-clone `git am --3way` verified before handoff.

**Not yet verified live:** neither the User-Agent fix nor the LLM-judge replacement has been exercised against real APIs/live web fetches from this session (sandbox can't reach these domains or hold real API keys) -- Andy's next `--live` run is the actual test of both. Recommend a small `--nodes` spot-check (2-3 nodes) before a full 18-node run, given the last two full live runs each surfaced a new issue.

---

## 2026-08-26, round 10 (Second fingerprint bug -- "no one" pronoun false positive -- found live, mid-demo-run)

**Context:** Andy applied the round-9 patch and started his live demo-corpus run. Several nodes flagged, including one that shouldn't have per round 9's own analysis (CA-SOL-WRITTEN-CONTRACT-DEBT is a single-fact SOL node, not a catalog node). Read the actual disagreement-queue entry directly (via the file on Andy's machine) rather than guess.

**What was found:** Anthropic's fingerprint was `{'1','3','4'}` against Gemini's `{'3','4'}` and OpenAI's `{'4'}`. The stray `'1'` traced to the sentence "...once that period has run, **no one** may file suit..." -- the word-to-digit converter was matching "one" as a bare numeral even when it's the indefinite pronoun in "no one," converting it to the digit 1 and contributing a fingerprint token that had nothing to do with the legal answer.

**Fix:** Added a negative lookbehind to `_NUMBER_WORD_RE` excluding "one" (and the same pattern for other number words, though "one" is the only one this matters for in practice) when preceded by "no", "any", "some", "every", or "each" -- the common pronoun-forming words in English ("no one", "anyone", "someone", "each one", "every one"). Verified against the real run's three model outputs: with the fix, Anthropic's fingerprint becomes `{'3','4'}`, matching Gemini exactly. Also verified against a battery of edge cases (genuine numeral "one year" still converts correctly; "twenty-one days" unaffected; "no one"/"anyone"/"someone"/"each one"/"every one" all correctly excluded).

**Important, not swept under the rug:** even after this fix, that node's fingerprint check still won't reach a clean 3/3 match -- OpenAI's answer genuinely omits the three-month deed-of-trust/mortgage exception that both Claude and Gemini included. That's a real content-completeness gap between models, not a fingerprint artifact, and the disagreement queue is correctly flagging it. This is exactly the outcome the fix should produce: eliminate the false-positive contributor, leave the genuine finding flagged.

**Verification:** re-tested `normalize_numbers()` against the real run's Anthropic/OpenAI/Gemini prose plus a battery of "no one"/"someone"/"anyone"/"any one of"/"each one"/"every one" edge cases; schema validation, frozen-artifact check, py_compile, and a fresh `--dry-run --demo-corpus-only` (18/18 clean-pass) all re-run with the fix in place. Fresh-clone `git am --3way` verified before handoff.

**Note on process:** this landed mid-run on Andy's machine, not from a clean pre-run review -- worth flagging for future rounds that a broader adversarial test of the fingerprint proxy against varied real prose (idioms, pronouns, compound sentences) before shipping would catch more of these before Andy hits them live, rather than one-at-a-time during a live run.

---

## 2026-08-26, round 9 (Runner bug fixes from live run 3, four-tier source hierarchy, CI validator fix, AZ finding)

**Context:** Andy ran the corroboration runner live (run 3) with all three keys verified valid (curl 200s). Runs 1-2 were his own key-formatting errors, purged from the disagreement queue as auth artifacts (see below). Run 3 surfaced two real issues, filed for ingestion: (1) a runner bug — OpenAI and Gemini derivations returning empty fingerprints where Anthropic returned grounded ones; (2) a content/sourcing issue — AZ state-layer citations anchored on FindLaw (secondary), which the live citation checker correctly couldn't verify as primary. Mid-investigation, Andy ratified a four-tier source hierarchy replacing the earlier binary primary-only rule.

**What changed:**
1. **Runner bug fixed — root cause was NOT Andy's Python 3.9/LibreSSL environment.** Diagnosed against his real run-3 model prose, not speculation. Two independent bugs in `run_corroboration.py`'s fingerprint-agreement logic: (a) the numeric-fingerprint regex extracted digits out of citation references embedded in the models' own prose (e.g. "§ 12-543" contributing spurious "12"/"543" as if they were legal-answer facts), and didn't normalize spelled-out numbers ("six" vs "6") — so GPT/Gemini fingerprints came back empty or mismatched even when their substantive answer agreed with Anthropic's. Fixed via a citation-stripping pass (`_CITATION_STRIP_RE`, using the actual `§` character, not an ASCII stand-in — an early draft of this regex used literal "S" under `IGNORECASE` and corrupted ordinary words like "six"; caught in testing, fixed) followed by spelled-number-to-digit normalization. Re-verified against the real AZ-SOL-ORAL and AZ-SOL-WRITTEN run-3 prose: all three models now correctly fingerprint to `{'3'}` and `{'6'}` respectively. **No Python upgrade needed on Andy's machine — this was a runner-side parsing bug, now fixed at the source.**
2. **Citation checker now records real diagnostics instead of `error: None`.** `verify_citation()` returns a `diagnostics` dict (`http_status`, `content_length`, `content_type`, `word_overlap_ratio`) on every call, verified or not, so a failure is now self-explaining rather than a bare null.
3. **Citation checker HTML-stripping bug found and fixed.** While building the diagnostics, found that `verify_citation()` was matching cited text against raw unstripped HTML — sites like Cornell LII and eCFR wrap inline terms in `<a>` tags with no surrounding whitespace in source markup (e.g. `a<a>debt</a>collector`), which broke substring matching even against genuinely correct, reachable, 200-status sources. This means part of what looked like a secondary-sourcing problem in the run-3 queue was actually a checker bug unrelated to source quality. Fixed via `_strip_html()` (tag boundaries replaced with a space, not deleted, to prevent word concatenation) + `html.unescape()`. Verified against a synthetic Cornell-style no-whitespace fragment.
4. **Four-tier source hierarchy implemented**, per Andy's ratification: `source_tier` (enum A/B/C/D) and `tier_rationale` (nullable, required by convention for B) added to `rules/schema/debt_schema_v1.0.json`'s `derived_from` item schema. Backfilled corpus-wide across all 9 debt rules files (63 source entries, domain-classified) — see `docs/SOURCE_TIER_AUDIT_20260826.md` for the full distribution and the 27-node violation list (nodes anchored solely on Tier C/D, no A/B source at all — concentrated in AZ (7/7), CA (7/7), UT (5/6), TX (4/6), NY (3/6); federal spine is fully clean, 0 violations).
5. **AZ re-pin attempted, genuinely blocked — reported honestly, not silently downgraded.** Direct fetch of azleg.gov's cited sections confirmed JS-gated ("Javascript is required..."), matching the hierarchy's own anticipated machine-hostile case. No Tier B fallback exists for AZ statute full text (Cornell LII's AZ page only links back to azleg.gov). Wayback Machine attempted as a workaround, blocked at the tool level. AZ's 7 nodes remain Tier C (FindLaw) this round — flagged as an open gap in `docs/SOURCE_TIER_AUDIT_20260826.md`, with the practical next step noted (Andy's browser can render JS; this session's tools can't). CA/UT/NY/remaining-TX re-pins queued, not yet attempted (see audit doc for recommended order).
6. **CI validator bug found and fixed, unrelated to the above but discovered while working with the pushed run-output files.** `scripts/ci/validate_debt_schema.py` swept `rules/debt/validation/runs/*.json` (pipeline output, not rules content) into schema validation once Andy started committing real run output there, causing spurious `'_copyright' is a required property` failures. Fixed by excluding the `rules/debt/validation/` subtree from file discovery.
7. **Disagreement queue purged of auth-artifact entries.** Andy's runs 1-2 (all-401/invalid-key errors on every node, confirmed via `run_20260826T171949Z.json`) had auto-filed 72 disagreement-queue entries that were key-formatting artifacts, not real model disagreements. Removed per his instruction, replaced with a single dated `[PURGE NOTE]` entry explaining the removal (append-only discipline: logged, not silently vanished). Queue file reduced from 104 to 32 real entries (run `run_20260826T174558Z`, 14 entries, and `run_20260826T175559Z`, 18 entries).

**Silver lining, for the record (per Andy's explicit request):** the citation checker catching a secondary-source-only anchor on its first live run — before any promotion to CORROBORATED or VALIDATED tier — is exactly the discipline working as designed. It caught a real corpus-quality gap (27 nodes, not just AZ) that a purely synthetic dry-run couldn't have surfaced, and it did so without silently failing (`error: None`) — that gap in the diagnostics is now closed too.

**Test/verification:** `scripts/ci/validate_debt_schema.py` (all 9 files pass against the extended schema), `scripts/ci/check_frozen_artifacts.py` (vProof1/v0.3 untouched), full-repo `py_compile` sweep, fingerprint-fix and HTML-stripping-fix each independently re-tested against real run-3 prose / synthetic HTML before being combined, runner `--dry-run` end-to-end re-run with both fixes applied together. Fresh-clone `git am --3way` verification before handoff.

**Flagged, not silently resolved:** (a) AZ Tier-A re-pin blocked by confirmed JS-gating, no viable Tier B found, Wayback blocked — open, needs either Andy's browser or a future JS-capable tool. (b) CA/UT/NY/remaining-TX re-pins diagnosed (exact node list in the audit doc) but not yet executed. (c) §3(c) mutation testing remains unimplemented in the runner (carried forward from round 8).

---

## 2026-08-26, round 8 (Phase A Unblock + Concept Demo First — corroboration runner, Band 3 node, security closure, spec v5)

**What changed:**
1. **ENG_HARDENING Task 1 closed.** Andy enabled Secret Protection (already on), push protection (new), and Dependabot alerts/security-updates in the GitHub UI 2026-08-26; committed `.github/dependabot.yml` directly (owner-level UI flow, logged as an explicit exception to the one-writer pattern per Andy's own instruction). Reconciled: file contents (`github-actions` ecosystem, `/` directory, weekly interval) match exactly what Andy specified — no drift. Dependabot-PR handling proposal: no CI change needed — `.github/workflows/ci.yml` already runs on every PR to `main` regardless of author, so `dependabot[bot]` PRs get the same schema/frozen-artifact/lint gates as any human PR; they still need a human merge decision, standard GitHub flow, no automation proposed here.
2. **Grounded-corroboration runner delivered**, per interface Andy specified: `scripts/corroboration/run_corroboration.py`, `requirements.txt`, `README.md`, `scenarios.json`; keys via gitignored `.env` (template `.env.example`, `.gitignore` patched with an explicit `!.env.example` exception since the existing `.env.*` pattern would otherwise have blocked it); output to `rules/debt/validation/runs/`. Implements spec §3(a) grounded derivation (3 independent models: claude-opus-5, gpt-5.5, gemini-2.5-pro; agreement via mechanical numeric/citation-fingerprint comparison, not LLM-judged semantic match — documented as a deliberately conservative, auditable proxy), live mechanical citation verification, §3(b) adversarial-generation pass, and §3(d) auto-filing to new `docs/DEBT_DISAGREEMENT_QUEUE.md`. Never writes to any rules file or tier field. Hard budget cap (default $15, stops before starting a node that would exceed it), stated per-node cost estimate (~$0.35, flagged as an estimate). Dry-run verified end-to-end in-session: 37/37 nodes clean-pass on synthetic data, CLI validation confirmed (`--dry-run`/`--live` mutual exclusion required; budget-cap pre-check correctly stops a run before any spend). Explicitly flagged: does not cover §3(c) mutation testing, so its tier-promotion recommendation is partial evidence, not full §4 criteria.
3. **Demo-gate metrics wired in**, per the Concept Demo First directive §2: `grounded_agreement_rate` and `scenario_pass_rate`, both computed with basis (n counted, failures named) against `scripts/corroboration/scenarios.json`'s 5 prepared scenarios; internal ≥90%/≥90% gate flag in the run summary.
4. **One new node authored**, the corpus's first Band 3 (genuinely-discretionary) node: `TX-DEFAULT-JUDGMENT-SET-ASIDE-DISCRETIONARY` (`rules/debt/state/texas/tx_debt_band3_discretionary_v1.json`), grounding the Craddock v. Sunshine Bus Lines three-factor test and the TRCP 329b 30-day/75-day deadlines. Sourcing note flagged: the Craddock quote comes from a case-brief aggregator (lawpipe.com) rather than a primary opinion — direct CourtListener and Google Scholar opinion-page fetches both returned empty content this session. Schema-validated. Corpus total now **37 DRAFT nodes** (was 35; corrects the directive's undercounted "9 (4 federal + 5 TX)" pipeline-target reference — federal spine has always had 5 nodes).
5. **`DEBT_PROJECT_ARCHITECTURE_SPEC.md` bumped v4 → v5:** §8 gains a census-audit subsection (debt-slice release audits every node rather than sampling — stronger claim at lower cost for a small population; current corpus 37 nodes, attorney-hours estimate 3.1-9.25 hrs full corpus / 1.5-4.5 hrs demo corpus at 5-15 min/node) and a CONCEPT-DEMO claim-language row (framing sentence, two-number-with-basis rule, audience restriction). §10 gains a "Concept demo — near-term target" section (corpus scope federal+TX+CA, CORROBORATED tier standard, 90%/90% gate, 6-step 2-3-week critical path table) positioned ahead of the ratified Stage 1/1.5/2 ladder — which is retained, not deleted, as the next milestone after the concept demo; the previously-missing Stage 1.5 tier is now written in, and the "reconstructed without Andy's original message" caveat is removed per Andy's explicit ratification.
6. **`plugins/consumer-debt/skills/consumer-debt-validation/SKILL.md` reconciled**, discovered this round as a stale pre-2026-08-25 skeleton (plain-markdown jurisdiction-data plan) that predates and was never wired to the current `rules/debt/` JSON node architecture — flagged rather than silently left inconsistent. Updated in place to v0.2.0-concept-demo, points at the real corpus and the 5 scenarios, carries the CONCEPT-DEMO claims-discipline framing sentence. `jurisdictions/` and `test-cases/` left in place, not deleted, noted as currently inactive.
7. **UT/AZ/NY status confirmed**, not rebuilt: already fully DRAFT-built from rounds 5-7 (2026-08-25), exceeding the Concept Demo First directive's "visible DRAFT stub" minimum. No build action taken; logged as out-of-demo-reliance scope with honest tier labels.
8. **D-2/D-3 build-trigger update logged** in `docs/DIRECTION_D_ROADMAP.md`: D-2 (disagreement auto-triage) is now built (item 2 above); D-3 (statute-and-case watch) remains proposed, moved to HORIZON with trigger = post-concept-demo. Eviction reopening confirmed not required for either.
9. **HORIZON deferrals logged** in `docs/WORK_QUEUE.md`: UT/AZ/NY full-layer demo reliance, Tier 1/2 harness, red-team lane, mutation-suite build-out, D-3, Phase D census audit — all trigger = post-concept-demo, not cancelled.

**Test/verification:** `scripts/ci/validate_debt_schema.py` (all 9 debt rules files pass, including the new Band 3 file), `scripts/ci/check_frozen_artifacts.py` (vProof1/v0.3 untouched), full-repo `py_compile` sweep, corroboration runner dry-run end-to-end (37 nodes, CLI arg validation, budget-cap stop condition) — all in a fresh sandbox clone before packaging. Fresh-clone `git am --3way` verification before handoff, same discipline as every prior round.

**Flagged, not silently resolved:** (a) the directive's "9 (4 federal + 5 TX)" node count for the round-3 pipeline target was an undercount — federal spine has always been 5 nodes; corrected in this round's logging, no content changed. (b) the pre-existing `plugins/consumer-debt/` skill skeleton's disconnect from the current architecture — reconciled, noted above. (c) the Craddock citation's secondary-aggregator sourcing (CourtListener/Scholar fetches failed) — flagged in the node itself and here for the corroboration runner's citation check to revisit.

---

## 2026-08-25, round 6 (Debt Phase A build — AZ and NY, final two anchor states: build complete)

*Per Andy's explicit instruction to batch remaining builds and hand off one combined patch rather than repeated apply/push cycles ("are you able to do all the builds and then i do one simple push?"). Task class: GREEN. Content nodes DRAFT tier, single-model grounded derivations. This entry covers rounds 6 (AZ) and 7 (NY) together since they were built back-to-back before any intermediate handoff.*

**State layer — AZ, 7 nodes, `rules/debt/state/arizona/az_debt_state_layer_v1.json`:**
- `AZ-SOL-WRITTEN-CONTRACT-DEBT` (Band 1) — 6-year SOL, A.R.S. § 12-548(A), verbatim. Includes the statute's own choice-of-law rule (subsection B): Arizona's 6-year period controls even if a conflicting shorter out-of-state period would otherwise apply.
- `AZ-SOL-ORAL-CONTRACT-DEBT` (Band 1) — 3-year SOL, A.R.S. § 12-543, verbatim. Open-account rolling rule: no item on a stated/open account is barred as long as any item was incurred within the last 3 years.
- `AZ-WAGE-GARNISHMENT-LIMIT` (Band 1) — lesser of 10% of disposable earnings or the amount exceeding 60x the applicable minimum wage, A.R.S. § 33-1131(B), verbatim; 50% for support orders under subsection (C). Comparative note added: more debtor-protective than the federal CCPA floor and than UT's conforming approach.
- `AZ-HOMESTEAD-EXEMPTION` (Band 1) — $400,000 base (post-2022 Proposition 209), A.R.S. § 33-1101(A), verbatim, CPI-adjusted annually from 2024. Highest flat base figure among the five anchor states.
- `AZ-VEHICLE-EXEMPTION` (Band 1) — $15,000 standard / $25,000 if debtor or dependent has a physical disability, A.R.S. § 33-1125(8), verbatim.
- `AZ-TOOLS-OF-TRADE-EXEMPTION` (Band 1) — $5,000 aggregate, A.R.S. § 33-1130(1), verbatim. Flagged as notably broad: explicitly covers intangible business assets (phone numbers, client contact information, marketing tools like websites/domain names), not just physical tools.
- `AZ-CIVIL-ANSWER-DEADLINE` (Band 1) — 20 days standard (60/90 days if service is waived), Ariz. R. Civ. P. 12(a)(1)(A), verbatim (courtrules.net, official-source-sourced rule text).

**State layer — NY, 6 nodes, `rules/debt/state/new_york/ny_debt_state_layer_v1.json`:**
- `NY-SOL-CONTRACT-DEBT` (Band 1) — 6-year SOL, NY CPLR § 213(2), verbatim. Genuinely distinctive: unlike TX/CA/UT/AZ, New York does not split written vs. oral contract debt into different limitations periods — both get the same 6-year period.
- `NY-INCOME-EXECUTION-LIMIT` (Band 1) — a three-way lesser-of formula (10% of gross income / 25% of disposable earnings / amount over 30x minimum wage), NY CPLR § 5231(b), verbatim. Notable carve-out: medical debt from a hospital or licensed health care professional is barred from income execution entirely — a debtor protection not seen in the other four states' wage-garnishment nodes.
- `NY-HOMESTEAD-EXEMPTION` (Band 1) — county-tiered exemption, NY CPLR § 5206(a). **This node required a second sourcing layer, worth calling out specifically:** the bare statutory text on Justia shows flat 2019-base dollar figures ($75,000/$125,000/$150,000 across three county tiers) with no escalator clause visible in the section itself. Cross-referencing NY's Department of Financial Services (the official regulator responsible for publishing the triennial CPI adjustment required by CPLR §5205(l)(3), which also governs §5206) turned up the real currently-effective figures: $102,400/$170,700/$204,825, effective 2024-04-01, next adjustment 2027-04-01. This node quotes and cites BOTH the statutory base and the DFS table verbatim. Relying on the bare statute alone would have understated real homestead protection by roughly 35-40% — the most rigorous single sourcing exercise across all five state layers.
- `NY-VEHICLE-EXEMPTION` (Band 1) — same DFS-adjustment pattern: $5,500 standard / $13,625 disability-equipped (current), adjusted from a $4,000/$10,000 statutory base, NY CPLR § 5205(a)(8) + DFS table. Carved out entirely for child/spousal support, alimony, equitable distribution, or NY State/municipal creditor judgments.
- `NY-PERSONAL-PROPERTY-EXEMPTION` (Band 1) — itemized (not dollar-capped) household-goods list, a $4,075 tools-of-trade exemption (adjusted from $3,000), and a $1,325 wildcard exemption (adjusted from $1,000) available only if the debtor is not also claiming a homestead exemption. Node includes an explicit honesty flag documenting how the DFS table's somewhat ambiguous row labels were cross-checked against the statute's own dollar figures to build a correct mapping, rather than assumed.
- `NY-CIVIL-ANSWER-DEADLINE` (Band 1) — 20 days standard, 30 days for specific service methods (state-official delivery, or CPLR §308/313/314/315 service), NY CPLR Rule 320(a), verbatim.

**Phase A anchor-state build status: COMPLETE.** All five locked anchor states (TX 5 nodes, CA 7, UT 6, AZ 7, NY 6 = 31 state-layer nodes) plus the federal spine (4 nodes) = **35 total DRAFT-tier grounded nodes** across 8 rules files. All schema-validated (`validate_debt_schema.py`) and CI-passing (`check_frozen_artifacts.py`, `py_compile`). This is the completion of the "thin vertical slice" described in spec §10 — the natural next phase (Phase B) is running these nodes through the actual multi-model grounded-corroboration pipeline, which requires live API-key model access available only in Andy's environment per standing discipline.

**Docs updated:** `docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md` Appendix 2 (rounds 5-7 build log added, Phase A marked complete), `docs/WORK_QUEUE.md` (NOW table + new dated header), this changelog entry.

**Handoff note:** per Andy's request, rounds 5 (UT), 6 (AZ), and 7 (NY) plus this documentation commit are being delivered as ONE combined patch file rather than three separate round-by-round handoffs, to reduce apply/push friction.

**Verification:** all 8 debt JSON files (35 nodes total: 1+3+1+5+7+6+7+6) pass `validate_debt_schema.py`; `check_frozen_artifacts.py` passes (no drift); all repo `.py` files pass `py_compile`; the combined patch verified via `git am --3way` on a fresh clone before handoff.

---

## 2026-08-25, round 5 (Debt Phase A build — UT state layer, third anchor state)

*Continuing autonomously per Andy's standing "proceed with as much as possible, only stop for genuine RED" instruction, confirmed after round 4's patch was applied and pushed. Task class: GREEN. Content nodes DRAFT tier, single-model grounded derivations.*

**State layer — UT, 6 nodes, `rules/debt/state/utah/ut_debt_state_layer_v1.json`:**
- `UT-SOL-WRITTEN-CONTRACT-DEBT` (Band 1) — 6-year SOL, Utah Code § 78B-2-309(1)(b), verbatim (FindLaw). Notable Utah-specific mechanic encoded explicitly: for a "credit agreement," the 6-year clock runs from the LATEST of when the debt arose, a written acknowledgment, or any payment (debtor's or a third party's) — meaning a stray payment can restart the limitations clock. Flagged in the node's `logic.restart_risk_note` so it isn't missed by anyone using this data.
- `UT-SOL-ORAL-CONTRACT-DEBT` (Band 1) — 4-year SOL for unwritten obligations and open store/services accounts, Utah Code § 78B-2-307(1), verbatim. Accrues from the last charge or payment, not the original debt date.
- `UT-WAGE-GARNISHMENT-LIMIT` (Band 1) — lesser of 25% of disposable earnings or the amount exceeding 30x the federal minimum wage (15% flat for education loans), Utah Code § 70C-7-103(2), verbatim. Comparative note added: this is Utah's conforming adoption of the federal CCPA floor — notably less debtor-protective than CA's 20%/48x formula and nowhere near TX's constitutional bar. Useful cross-state contrast now that three anchor states have wage-garnishment nodes.
- `UT-HOMESTEAD-EXEMPTION` (Band 1) — $42,000 primary residence / $84,000 joint household, or $5,000/$10,000 non-primary, Utah Code § 78B-5-503(2), verbatim, plus the four carveout categories from subsection (3) where the exemption doesn't apply (tax liens, purchase-money liens, child-support liens, consensual liens).
- `UT-PERSONAL-PROPERTY-EXEMPTION` (Band 1) — household goods ($1,000 per category, 4 categories), tools of the trade ($5,000 aggregate, can include a business-use vehicle), and a general motor-vehicle exemption ($3,000), Utah Code § 78B-5-506, verbatim. Node explicitly flags the no-double-dip rule: a debtor cannot claim the same vehicle under both the trade-tools exemption and the general vehicle exemption.
- `UT-CIVIL-ANSWER-DEADLINE` (Band 1) — 21 days if served within Utah, 30 days if served outside Utah, Utah R. Civ. P. 12(a)(1), verbatim.

**Sourcing note:** all 6 UT nodes are `citation_verified: true`. Utah's main court-rules site (`utcourts.gov`) timed out on three consecutive live-fetch attempts; recovered via the state's own `legacy.utcourts.gov` rules mirror, which served static HTML with the verbatim rule text (page footer confirms "printed on August 25, 2026," rule effective 5/1/2024) — still a primary, official Utah Courts source, just reached through a different URL path than the primary site.

**Docs updated:** `docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md` Appendix 2 (round 4 build log added), `docs/WORK_QUEUE.md` (NOW table + new dated header), this changelog entry.

**Verification:** all 6 debt JSON files (23 nodes total: 1 + 3 + 1 + 5 + 7 + 6) pass `validate_debt_schema.py`; `check_frozen_artifacts.py` passes (no drift); all repo `.py` files pass `py_compile`; commit verified via `git am --3way` on a fresh clone before handoff.

---

## 2026-08-25, round 4 (Debt Phase A build — CA state layer, second anchor state)

*Continuing autonomously per Andy's "proceed with as much as possible, only stop for genuine RED" instruction, confirmed after round 3's patch was applied and pushed. Task class: GREEN. Content nodes DRAFT tier, single-model grounded derivations.*

**State layer — CA, 7 nodes, `rules/debt/state/california/ca_debt_state_layer_v1.json`:**
- `CA-SOL-WRITTEN-CONTRACT-DEBT` (Band 1) — 4-year SOL, Cal. Code Civ. Proc. § 337(a), verbatim (Justia). Also encodes § 337(d)'s California-specific quirk: once the period runs, a creditor is statutorily barred from even *initiating* suit or arbitration to collect, not merely exposed to an affirmative defense the debtor must raise.
- `CA-SOL-ORAL-CONTRACT-DEBT` (Band 1) — 2-year SOL for obligations not founded on a written instrument, Cal. Code Civ. Proc. § 339(1), verbatim.
- `CA-WAGE-GARNISHMENT-LIMIT` (Band 1) — the post-SB 1477 formula (lesser of 20% of weekly disposable earnings, or 40% of the amount by which earnings exceed 48x the applicable state-or-local minimum hourly wage), Cal. Code Civ. Proc. § 706.050, verbatim (FindLaw), operative 2023-09-01.
- `CA-HOMESTEAD-EXEMPTION` (Band 1) — greater of countywide median single-family home price (capped $600,000) or $300,000, inflation-adjusted annually from a 2022 base, Cal. Code Civ. Proc. § 704.730, verbatim.
- `CA-VEHICLE-EXEMPTION` (Band 1) — $7,500 aggregate motor-vehicle equity exemption, including the automatic (no-claim-needed) rule when a debtor's single vehicle is sold at execution, Cal. Code Civ. Proc. § 704.010, verbatim.
- `CA-BANK-ACCOUNT-EXEMPTION` (Band 1) — automatic bank-deposit exemption tied to a Welfare & Institutions Code §11452/§11453 cross-reference, plus the wages/child-support/spousal-support carve-out, Cal. Code Civ. Proc. § 704.220, verbatim.
- `CA-CIVIL-ANSWER-DEADLINE` (Band 1) — 30-day answer deadline from service, including the statute's own required boldface consumer-facing notice language, Cal. Code Civ. Proc. § 412.20, verbatim.

**Sourcing note, worth flagging honestly:** all 7 CA nodes are `citation_verified: true` — stronger sourcing posture than the TX round, where one node (`TX-JUSTICE-COURT-DEBT-ANSWER-DEADLINE`) relied on a secondary source only. That said, two CA nodes (`CA-WAGE-GARNISHMENT-LIMIT`, `CA-HOMESTEAD-EXEMPTION`) encode a *formula* whose current dollar inputs (the minimum wage figure; the countywide median home price and inflation-adjusted floor/cap) live in other, periodically-updated sources not independently pulled this session. The node text says so explicitly (`note_needs_current_figure` field) rather than hardcoding what could become a stale number. This is a different and more precise kind of gap than TX's "didn't check primary source" flag — here the primary CCP text itself is verified verbatim; what's missing is a separately-tracked adjustable figure.

**Also flagged:** `CA-BANK-ACCOUNT-EXEMPTION`'s underlying dollar figure (via W&IC §§11452/11453) was not independently pulled this session — same "formula not current figure" caveat as above.

**Docs updated:** `docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md` Appendix 2 (round 3 build log added), `docs/WORK_QUEUE.md` (NOW table + new dated header), this changelog entry.

**Verification:** all 5 debt JSON files (17 nodes total: 1 + 3 + 1 + 5 + 7) pass `validate_debt_schema.py`; `check_frozen_artifacts.py` passes (no drift); all repo `.py` files pass `py_compile`; commit verified via `git am --3way` on a fresh clone before handoff.

---

## 2026-08-25, round 3 (Debt Phase A build continues — autonomous, per Andy's "proceed without gating" instruction)

*Andy, in chat: "all set - committed. please proceed. our work approach should be that you should proceed with as much as possible and only stop if there is something explicit that you need me to review, and then please let me know that. i am going to be traveling but want to get the project back into execution mode." Task class: GREEN for infrastructure/CI; all new content nodes ship DRAFT tier, honestly labeled single-model derivations that have not yet passed the multi-model verification pipeline (spec §3a-d).*

**Federal spine — 3 more nodes, `rules/debt/federal/fdcpa_conduct_prohibitions_v1.json`:**
- `FDCPA-REGF-CALL-FREQUENCY-1006.14b` (Band 1) — the Reg F "7-in-7" rebuttable-presumption rule (no more than 7 calls in 7 consecutive days per debt, and no call within 7 days of a prior conversation about that debt). Cites 12 C.F.R. § 1006.14(b)(2)(i)-(ii) and (b)(4) verbatim, fetched live from eCFR 2026-08-25.
- `FDCPA-FALSE-DECEPTIVE-CATALOG-1692e` (Band 1) — full 16-item false/deceptive/misleading-representation catalog. Cites 15 U.S.C. § 1692e verbatim in full (Cornell LII), plus 12 C.F.R. § 1006.18(e) verbatim for the mini-Miranda disclosure sub-item.
- `FDCPA-UNFAIR-PRACTICES-CATALOG-1692f` (Band 1) — full 8-item unfair-practices catalog. Cites 15 U.S.C. § 1692f verbatim in full (Cornell LII). Item (6) (nonjudicial repossession without an enforceable security interest/present right) flagged inline as carrying more legal-judgment dependency than the other 7 items — still Band 1 structurally, but the completeness checklist notes the fact-finding is less mechanical.

**Federal spine — FCRA furnisher duty, `rules/debt/federal/fcra_furnisher_dispute_v1.json`:**
- `FCRA-FURNISHER-DISPUTE-DUTY-1681s-2b` (Band 1) — a furnisher's duty to investigate and correct/delete/modify reported information after a CRA forwards a consumer dispute. Cites 15 U.S.C. § 1681s-2(b)(1)-(2) verbatim. Source page (Cornell LII) exceeded the fetch tool's output limit; recovered by reading the saved local copy with paginated offset/limit to isolate subsection (b). **Honestly flagged:** the node references the § 1681i(a)(1) reinvestigation deadline but does not itself state that deadline's length — that provision was not independently pulled and verified this session, so the length claim should not be treated as sourced yet.

**State layer — TX first pass, 5 nodes, `rules/debt/state/texas/tx_debt_state_layer_v1.json`:**
- `TX-SOL-CONSUMER-DEBT` (Band 1) — 4-year statute of limitations. Tex. Civ. Prac. & Rem. Code § 16.004(a)(3), verbatim.
- `TX-WAGE-GARNISHMENT-PROHIBITION` (Band 1) — Texas's state-constitutional bar on wage garnishment for ordinary debt (stronger than federal law's partial-protection approach), limited exceptions for child support/spousal maintenance. Tex. Const. art. XVI § 28, verbatim.
- `TX-HOMESTEAD-EXEMPTION` (Band 1) — homestead protection from most creditor claims, no dollar cap, acreage-limited (10 urban / 200 rural family / 100 rural single adult). Tex. Prop. Code §§ 41.001(a), 41.002(a)-(b), verbatim.
- `TX-EXEMPT-PERSONAL-PROPERTY` (Band 1) — personal-property exemption, $100,000 family / $50,000 single-adult aggregate fair-market-value cap. Tex. Prop. Code §§ 42.001(a)-(b), 42.002(a), verbatim.
- `TX-JUSTICE-COURT-DEBT-ANSWER-DEADLINE` (Band 1, tier DRAFT) — 14-day answer deadline in justice court, $20,000 jurisdictional ceiling. **`citation_verified: false`** — sourced from TexasLawHelp.org (attorney-reviewed legal-aid content), not yet independently verified against primary Tex. R. Civ. P. 502.5 text. Flagged as the weakest-sourced node in this delivery; not blocking, since DRAFT tier already signals not-yet-corroborated, but called out because the gap here is sourcing depth, not just pipeline stage.

Both source pages for `TX-HOMESTEAD-EXEMPTION`/`TX-EXEMPT-PERSONAL-PROPERTY` initially failed via `statutes.capitol.texas.gov` (client-rendered shell, no static content) — recovered via `codes.findlaw.com`, which serves static HTML with full verbatim text.

**CI pipeline — ENG_HARDENING Task 2, folded into debt Phase A per Andy's "as applicable" instruction:**
- `rules/schema/debt_schema_v1.0.json` validated by new `scripts/ci/validate_debt_schema.py` against all `rules/debt/**/*.json` (10 nodes across 4 files) via the `jsonschema` library. Also enforces: valid tier enum on every node; any node claiming `VALIDATED` must carry a `certifying_attorney` in its provenance block, or the check fails — a machine-checked version of spec §3(g)'s no-self-certification rule.
- `scripts/ci/check_frozen_artifacts.py` + `scripts/ci/frozen_artifact_manifest.json` — SHA256 manifest covering `rules/eviction/california/ca_eviction_v2.json` (vProof1) and the frozen v0.3 held-out golden set; drift or a missing file fails the check. This machine-enforces the "never touch vProof1 / never re-score v0.3 held-out" standing discipline for the whole repo, not just the debt line.
- `.github/workflows/ci.yml` — four jobs (json-well-formedness, debt-schema-validation, frozen-artifact-integrity, lint via `py_compile`), all self-contained and requiring no live model API keys, consistent with the standing discipline that live API-key runs happen only in Andy's environment. Runs on push/PR to `main`.
- **Not built:** a scorer unit-test suite or calibration suite (the rest of Task 2/all of Task 4) — no debt scorer exists yet to test against. Queued in `WORK_QUEUE.md`, not silently dropped.

**Docs updated (this entry's own delivery):** `docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md` Appendix 2 (round 2 build log added, stale "what's not yet started" list corrected), `docs/WORK_QUEUE.md` (NOW table + new dated header), this changelog entry.

**Verification:** all 4 debt JSON files pass `validate_debt_schema.py` (10/10 nodes); `check_frozen_artifacts.py` passes (no drift on vProof1 or the frozen v0.3 set); all repo `.py` files pass `py_compile`; commit verified via `git am --3way` on a fresh clone before handoff.

---

## 2026-08-25, round 2 (Debt Phase A build authorized and started — spec v4, first grounded node)

*Per Andy's build-authorization message (in chat, following his answers to Cowork's four questions on README placement, repo restructuring, validation cadence, and the ENG_HARDENING/TX/5th-anchor decisions). Task class: GREEN for infrastructure/schema/scaffold; the one content node ships DRAFT tier, not self-certified.*

### Decisions logged (Andy, 2026-08-25, chat — not a separate directive doc)

1. v3 spec ratified as-is.
2. ENG_HARDENING held with the rest of eviction, *except* Tasks 2 (CI), 3 (schema), 4 (calibration suite), 7 (independent review) apply to debt as best practice and are folded into Phase A. Task 6 already covered by spec §3(c); Task 5 stays naturally deferred.
3. Fifth anchor state: **TX** — a decision, not a data-driven ranking; the "genuinely unresolved" flag on this closes.
4. `A2J_STACK_AND_CJAC_SCOPE.md` confirmed final by Andy; promoted to README's first doc link (previously linked but not primary, per the flagged ambiguity in the earlier delivery).
5. Repo restructuring: Andy adopted Cowork's recommendation — scaffold `rules/debt/` fresh rather than physically moving `rules/eviction/`. See below for what that entailed.
6. **Validation cadence for Phase A: build-first, AI-maximal, sampling-gated, not granular-gated.** Andy: "I want to build and validate with AI as much as possible and get something impressive... I don't want [human review] to gate the build-out." This is the ratified §3 sampling-audit model (v2 decision 4) — the instruction is to actually run it that way, not a redesign. Named-attorney release certification (§3g) stays the human gate; per-node review does not, and was never designed to.

### GREEN — Repo hygiene (byproduct of the restructuring review, unrelated to any physical move)

Fixed a stale pre-relocation absolute path (`~/Documents/GitHub/a2j-ai`, dead since the July dispatcher outage) sitting unfixed in 9 live operational files (`rules/validation/run_protocol.py`, `run_dispatch.sh`, 7 `rules/validation/l2/*_runner.py` docstrings, `demos/eviction/prompts/demo-script.md`) — corrected to the current path. Historical dated records (`DAILY_CHANGELOG.md`, `results/*.md`, etc.) correctly left untouched, since they're accurate as of the dates they describe. Removed a stray duplicate `validation/l2/output/` directory (drift from an old run, distinct from `rules/validation/l2/`). Removed two placeholder-only `.env`-pattern files at repo root (`.e`, `.env<hash>` — contained `PASTE_TOKEN_HERE`, not a real credential; confirmed via diff before deletion, no exposure, but shouldn't have been committed). Hardened `.gitignore` (`.env.*`, `.e`) against recurrence. No rules content touched.

### GREEN — `rules/debt/` scaffold + formal schema

`rules/schema/debt_schema_v1.0.json` — extends the eviction schema pattern (`docs/SCHEMA_V2_DESIGN_SPEC.md`) rather than replacing it, per spec §2. Key departure, deliberate: tier (`DRAFT`/`CORROBORATED`/`VALIDATED`) and band (1/2/3) are **node properties**, not file properties, unlike eviction's `file_status = min(module_status)` — a single release can ship federal-spine nodes at VALIDATED alongside a newly-added state's garnishment table at CORROBORATED. Validated as syntactically correct JSON Schema. `rules/debt/federal/` and `rules/debt/state/` created with READMEs explaining the pattern.

### GREEN — First grounded content node: FDCPA-VALIDATION-NOTICE-1692g

`rules/debt/federal/fdcpa_validation_notice_v1.json` — Band 1 (deterministic). Encodes 15 U.S.C. § 1692g and 12 C.F.R. § 1006.34 (Regulation F) together, since Reg F elaborates and partially supersedes the statute's bare five-item list with the fuller Model Form B-1 content regime and clarifies timing (initial communication / within 5 days / oral) and the mailbox-rule computation for the 30-day dispute window. Both sources fetched live 2026-08-25 (Cornell LII, eCFR) and cited verbatim in the node's `grounded_derivation` block, consistent with spec §3(a)'s requirement that a derivation point to specific source text, not priors. Completeness checklist (8 dispositive facts) and consequences-and-next-steps fields populated per §2's structural requirement. **Validated against `debt_schema_v1.0.json`** (`jsonschema` library) — passes.

**Tier is honestly DRAFT, stated plainly, not inflated for the sake of a good first showing:** this is a single-model derivation. It has not passed grounded corroboration by three independent frontier models (§3a), adversarial generation (§3b), the disagreement queue (§3d), the statistical sampling audit (§3e), or attorney release certification (§3g) — the actual gates that would promote it to CORROBORATED or VALIDATED. One node proves the schema and grounding discipline work end-to-end on real primary-source law; it is not Phase A complete, and the spec's new Appendix 2 says so directly.

### GREEN — Spec revised to v4; living docs updated

`docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md`: status changed from "DRAFT-FOR-ANDY, not ratified as a build plan" to "RATIFIED FOR BUILD." New v4 decision record at the top (items 1-6 above). §10 locks TX, closes the fifth-anchor-state flag. §3 gets the ENG_HARDENING carryover assessment (task-by-task). §12 rewritten from "proposed" to "DECIDED," describing what was actually done rather than a proposal. New "decision 7" (validation cadence) added to the ratified-decisions list. New Appendix 2: live debt-line build log, same discipline as the eviction-line appendix — updated as work lands, not regenerated.

`docs/WORK_QUEUE.md` / `docs/PROJECT_STATE_OF_RECORD.md`: new same-day "round 2" entries logging all six decisions. `WORK_QUEUE.md`'s NOW section updated to reflect debt Phase A as the actual active line (the prior NOW content, dated July 1 eviction self-critique work, retained below as historical record, clearly marked as no longer active). New NEXT items queued for continued autonomous build — remaining federal-spine nodes, TX state layer, the folded-in ENG_HARDENING infrastructure tasks, and actually running the multi-model verification pipeline against the first node — so build continues without waiting on granular sign-off, per Andy's instruction.

---

## 2026-08-25 (files.zip delivery — publication checklist executed, Direction E logged, debt spec v3, companion docs committed)

*Per Andy's `files.zip` cover instructions (6 items, executed in order). Task class GREEN, documentation only. Authorship note, per amendment (c): the seven companion documents in this delivery (`COWORK_DIRECTION_ENG_HARDENING_20260724.md`, `COWORK_DIRECTION_DIRECTION_D_20260723.md`, `COWORK_DIRECTION_DIRECTION_E_20260724.md`, `COWORK_PUBLICATION_CHECKLIST_20260724.md`, `OPEN_QUESTIONS_AND_LIMITATIONS.md`, `CJAC_ROADMAP.md`, `PILOT_DESIGN_BAYLEGAL_DRAFT.md`, `A2J_STACK_AND_CJAC_SCOPE.md`) were authored 2026-07-24/07-26 and are being published/committed today, 2026-08-25 — the record should be honest about that roughly one-month gap between authorship and publication, not silent about it.*

### Item 1 — ENG_HARDENING and Direction D: confirmed previously sent, not re-executed

Both files in `files.zip` checked against prior delivery: `COWORK_DIRECTION_ENG_HARDENING_20260724.md` is byte-identical (md5 match) to the copy already committed 2026-07-24 (`d7e40c3`) — Task 1 (secret hygiene) already executed and reported that day; Tasks 2-4/7 and 5-6 status addressed below under item 2. `COWORK_DIRECTION_DIRECTION_D_20260723.md` is substantively identical to the 2026-07-23 directive already fully executed (`docs/DIRECTION_D_ROADMAP.md`). Neither re-executed. Both archived verbatim to the new `docs/directives/` folder for discoverability (see item 3 below — the folder didn't exist before this session; only Direction D's *roadmap*, not its original directive text, had been committed previously).

### Item 2 — Publication checklist (`COWORK_PUBLICATION_CHECKLIST_20260724.md`) executed in full

All rows and consistency-pass items executed, with the three amendments Andy specified:

- **Row 7 (`A2J_STACK_AND_CJAC_SCOPE.md`) — FLAGGED, not guessed.** Andy's own instruction text left both conditional branches of this row unresolved as a literal bracketed template ("[if you're done reviewing: ... / if not: ...]") rather than picking one. Resolution taken: the file is committed to `docs/` and linked from `README.md`'s Key Documents list, but explicitly *not* as the README's first/primary document link, with an inline note flagging it as still under Andy's review. This is a judgment call under genuine ambiguity in Andy's own text — flagged here for correction if it guessed wrong.
- **v0.4-sequencing references superseded by the hold.** Every place the checklist or its source documents referenced v0.4 sequencing has been published as historical/current record without reactivating eviction work — see the ENG_HARDENING Tasks 5-6 re-gate note in `WORK_QUEUE.md`/`PROJECT_STATE_OF_RECORD.md` today's entries.
- **Authorship-vs-publication gap noted** — see the header note above.

**Consistency-pass items completed:**
- NIST framing fixed in `README.md`: "CJaC measures itself against recognized standards" → "CJaC's validation program is designed to align with recognized standards ... without claiming formal certification against any of them."
- Band 1/2/3 taxonomy given shared vocabulary: `docs/GLOSSARY.md` created (Band 1/2/3, AMPVR, ratification-queue-health, Tier 1/Tier 2 — one line each, sourced from `OPEN_QUESTIONS_AND_LIMITATIONS.md` Q10 and the Direction E directive).
- `README.md`'s "Results, open questions, and roadmap" section added, walking a skeptical reader through `VALIDATION_README.md` → `OPEN_QUESTIONS_AND_LIMITATIONS.md` → `CJAC_ROADMAP.md` → `collateral/`, in order. Key Documents list updated with explicit links to `OPEN_QUESTIONS_AND_LIMITATIONS.md`, `CJAC_ROADMAP.md`, `GLOSSARY.md`, and the flagged `A2J_STACK_AND_CJAC_SCOPE.md` entry.
- Concise-deck retirement: confirmed via `find . -iname "*concise*"` that no such file exists anywhere in the repo — nothing to retire. Logged here as the confirmation record.
- Notes-free collateral PDF: `collateral/CJaC_Pitch_Deck_FINAL.pdf` generated via `soffice --headless --convert-to pdf` from the already-committed `.pptx` (LibreOffice's default Impress export strips speaker notes — verified this matches the "notes-free" requirement) and committed alongside the existing `.pptx`/`.docx`.
- `docs/COWORK_DIRECTION_A_CADENCE_AUTONOMY.md` amended: morning-report template gets a new opening line ("0. Where we are") stating the current roadmap phase, added as a dated standing amendment consistent with the file's existing Part 5/Part 6 precedent for dated additions rather than silent rewrites.
- Standing-discipline sweep run across all seven new/companion docs: no solitary post-errata score citations, no dual-model/tri-model phrasing drift, no Schweiger/Levitz mix-ups, NIST framing clean elsewhere. Nothing needed fixing beyond the README instance above.

### Item 3 — Direction E logged; demo-harness lane unblocked

`docs/directives/COWORK_DIRECTION_DIRECTION_E_20260724.md` committed. `docs/DIRECTION_D_ROADMAP.md` amended with a new "Direction E — Lower-bound testing" section (Tier 1 narrative-perturbation and Tier 2 interactive-elicitation methodology, full descriptions, build gates) and a new "Automation-leverage principles" section (AMPVR definition, ratification-queue-health metric, triage-automation purpose statement — Task 3 of the directive). Per Andy's instruction, Direction E's eviction-specific v0.4 gate is superseded by the hold: **Tier 1/Tier 2 now apply to the debt track**, with narrative rewrites and personas to be built on debt fact patterns (not ported from eviction) once that lane starts. Task 3 executed as written (roadmap doc updated).

### Item 4 — `DEBT_PROJECT_ARCHITECTURE_SPEC.md` revised to v3

Both gaps v2 explicitly flagged as blocking are now resolved with real content, not placeholders: the Band 1/2/3 taxonomy (§1's corpus band-tags reconciled against the ratified `CJAC_ROADMAP.md` definitions — no changes needed, the v1/v2 working examples held up) and AMPVR (§4, now defined per Direction E Task 3). The demo-harness lane (§5, §10 Phase C, §11 lane c) is unblocked: Direction E's actual Tier 1/Tier 2 mechanics replace the prior "hard-blocked, cannot describe" language, and the model-family-separation rule in §11 is now confirmed against Direction E's real text ("actor and subject from different model families; actor prompts and fact sheets never exposed to the subject") rather than stated as a guess. §10's critical-path table updated: Phase C's bottleneck changes from "hard-blocked on Direction E" to "authoring debt-specific narratives/personas" — real work, no longer undefined work. A new "Staged demo plan: Stage 1 (machinery) / Stage 2 (outreach-grade)" subsection added to §10 per Andy's request.

**Flagged, not silently guessed:** Andy's request for the staged demo plan referenced "per my prior message" — a message this session has no record of. The Stage 1/Stage 2 plan added is a best-effort construction from the spec's own existing §5/§10 sequencing (Stage 1 = thin slice through the scenario voice demo, both lower-bound tiers run once, Andy/counsel-only audience; Stage 2 = adds Phase D certification + Phase E hardening, outreach-ready). If Andy's original message specified different stage content or format, this section is a draft to correct against it, not a confirmed match.

### Item 5 — Companion docs and living-record updates

`docs/OPEN_QUESTIONS_AND_LIMITATIONS.md`, `docs/CJAC_ROADMAP.md`, `docs/PILOT_DESIGN_BAYLEGAL_DRAFT.md`, `docs/A2J_STACK_AND_CJAC_SCOPE.md` committed to `docs/` verbatim. `WORK_QUEUE.md` and `PROJECT_STATE_OF_RECORD.md` amended (same-day addenda to the existing 2026-08-25 HOLD entries, append-only): Commons alignment posture logged (citing `A2J_STACK_AND_CJAC_SCOPE.md`'s Legal Help Commons/JusticeBench alignment language), Band-1-only validation-claims scope now a standing caveat (per `OPEN_QUESTIONS_AND_LIMITATIONS.md` Q10), multilingual/Spanish-first access logged to `CJAC_ROADMAP.md` Phase 4 HORIZON (no design work, listed so it isn't lost), ENG_HARDENING Tasks 5-6 re-gated onto the debt track's first frozen eval set, and ENG_HARDENING Tasks 2-4/7 flagged as having no live "this week" trigger now that proposal 16 hasn't executed and eviction is on hold (left as not-started pending Andy's explicit go/no-go, rather than assumed either way).

### Item 6 — This entry is the report

Per Andy's instruction, one consolidated report message follows this delivery covering: secret-scan status (already reported 07-24, re-confirmed unchanged today), checklist execution complete with the details above, Direction E logged and the demo lane's unblocked status, and the full list of conflicts/ambiguities flagged rather than silently resolved (A2J_STACK_AND_CJAC_SCOPE.md's unresolved README-first-link conditional; the Stage 1/Stage 2 "prior message" this session doesn't have; ENG_HARDENING Tasks 2-4/7's stale trigger; the fifth-anchor-state data gap carried over from the debt spec v2; this session's own v2 patch's uncertain push status, resolved via local `git am --3way` regardless — see the handoff message).

---

## 2026-08-25 (Debt Defense Prototype v2 — decisions ratified, eviction line HOLD, spec revised)

*Per `COWORK_DIRECTION_DEBT_DECISIONS_20260824_v2.md`, superseding and incorporating the 2026-08-24 v1 directive (previous entry below). Task class GREEN, documentation only.*

### GREEN — Eviction line placed ON HOLD (same-day, per decision 5)

Logged in `WORK_QUEUE.md` and `PROJECT_STATE_OF_RECORD.md` with today's date: no new eviction drafting, freezes, or v0.4 work until Andy re-opens the line. Keep-warm (dispatcher + scheduled monitoring) continues. No eviction rules file, golden set, or ratified proposal was touched.

**Correction to the prior appendix's dormancy read:** a fresh clone today surfaced two dev-set monitor runs (2026-08-15, 2026-08-19) that weren't visible in yesterday's clone — both 12/12=100%, `newly_failing: 0`, but both PARTIAL-CONSENSUS (α = 0.917 and 0.75) rather than full DUAL-MODEL-CONSENSUS. The monitor is running, just on a sparse, not-daily cadence — corrected in both the WORK_QUEUE/PSOR hold entries and the spec's own appendix, which had reported the line as dormant since 07-27 based on the prior day's clone.

### GREEN — `docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md` revised (v2)

Open-items box removed; all six of Andy's ratified decisions baked directly into the relevant sections (broader scope in the opening + §1; staged navigator-first/consumer-gated users in §6/§9; the 99% VALIDATED-tier target with five-nines framed explicitly as a process aspiration, not a statistical claim, in §8; the sampling-audit/adjudication/certification model marked RATIFIED rather than proposed in §3; the eviction hold reflected throughout and in the appendix; the CJaC-umbrella/subproject naming proposed in a new §12). Added: §10 rewritten for demo-first thin-slice sequencing (supersedes v1's corpus-complete-first phasing), §11 new (multi-agent execution model — single-writer/orchestrator discipline, four parallel worker lanes, the multi-model verification pipeline, task-queue/budget/provenance/integration design).

**§8's measurement-honesty section is worked out with real numbers, not just a promise to be honest later:** the rule-of-three approximation for zero-defect sampling (95%-confidence upper bound ≈ 3/n) is used to show n≈300–385 supports the ratified 99% target, n≈3,000 supports a 99.9%-class claim, and a genuine five-nines statistical certification would need n≈300,000 per stratum — not achievable at this project's realistic audit scale. This is the basis for treating "five-nines" as engineering-process language only, never a sampling-audit claim, with exact permitted claim language specified per evidence level.

**Four items flagged rather than silently resolved, per the directive's explicit instruction to flag conflicts on contact with reality:**
1. The fifth anchor state (TX vs. NY vs. an alternative) has no hard per-state debt-lawsuit-volume data behind it in this session — UT/AZ (i4J + regulatory sandboxes) and CA (existing infra) are solidly justified; TX/NY are reasoned volume guesses, flagged as needing real data before finalizing.
2. The Direction E Tier 2 harness dependency hard-blocks the demo-harness lane (§5, §10 Phase C, §11 lane c) — this spec cannot build around a document that doesn't exist yet, and says so rather than inventing harness mechanics.
3. Physical repo restructuring toward `cjac/eviction/`/`cjac/debt/` is proposed (§12) but explicitly flagged as its own migration risk, citing this project's own July dispatcher outage (a folder relocation interacting badly with macOS background-process permissions) as directly on-point precedent — recommended as a separately planned migration, not bundled into Phase A.
4. The v2 directive's "keep-warm is cheap, preserves freshness data" framing assumes continuity the actual monitoring cadence hasn't shown (see the dormancy correction above) — flagged so Andy isn't relying on a monitoring record that may have real gaps in it.

**Dated critical path (§10):** active-work estimate of 6-10 weeks for phases A/B/C/E (corpus scaffold, federal-spine + 5-state encoding, demo harness, demo hardening), explicitly excluding Phase D (statistical audit + blind attorney certification), which is gated on Andy's/the certifying attorney's review bandwidth and is called out as the real unknown this spec cannot estimate on Andy's behalf. No calendar date is printed, per the directive's own instruction not to promise a date the estimates don't support -- once Phase D's bandwidth and the Direction E document's arrival are known, the active-work range converts to a real date.

**No repo changes beyond this spec revision and the two hold-logging entries above.** No rules file touched, no code built, no files physically moved.

## 2026-08-24 (Debt Defense Prototype directive — architecture spec drafted, DRAFT-FOR-ANDY)

*Per `COWORK_DIRECTION_DEBT_ARCHITECTURE_20260824.md`. Task class GREEN, documentation only — no rules files changed, no code built, nothing in the eviction line modified. Note the roughly one-month gap since the last entry above: no session ran between 2026-07-27 (last automated dev-set commit) and today; this directive is the first work item received in that window.*

### GREEN — `docs/DEBT_PROJECT_ARCHITECTURE_SPEC.md` drafted

All ten required sections plus the Andy-decision checklist and the eviction-line state-of-record appendix. Grounded with external research (cited inline in the spec): Pew's 2020 debt-lawsuit study (default-judgment rate, counsel-rate disparity, case-volume growth), FDCPA/Regulation F/FCRA citations, and the integration-map partners — Spot (Suffolk LIT Lab), the Document Assembly Line / docassemble / Court Forms Online / LITEfile, i4J's Medical Debt Policy Scorecard and MDLA navigator model, the Utah sandbox and Arizona ABS program, Legal Help Commons / JusticeBench, and LSC TIG.

**One finding worth flagging directly: *Upsolve, Inc. v. James* has changed since this project's context on it was last current.** The 2022 SDNY preliminary injunction in Upsolve's favor was **reversed by the Second Circuit on 2025-09-09** — the appellate court held Upsolve's non-lawyer "Justice Advocate" program did violate New York's UPL statutes and rejected the First Amendment pre-enforcement challenge. This is now the sharpest available cautionary precedent for any direct-consumer or worker-in-the-loop UPL scoping this project considers (spec §7/§9) — a narrow, well-funded, professionally represented program still lost at the appellate level.

**Two structural gaps flagged prominently in the spec itself, not silently filled in:** the Band 1/2/3 taxonomy (referenced against `CJAC_ROADMAP.md`) and the AMPVR metric plus Direction E Tier 2 harness design (referenced against the Direction E directive) — neither source document has been committed to the repository or supplied in any session; both are still behind the 2026-07-24 "docs are final" publication gate, which was never triggered. The spec uses plain-language working definitions where it must reference these and flags every instance rather than presenting an invented definition as settled.

**Eviction-line appendix, prepared fresh from the live repo rather than from memory:** v3 remains the sole active rules version; the D-1 dev-set monitor ran clean through 2026-07-26 (four consecutive 12/12 DUAL-MODEL-CONSENSUS runs) but has no logged activity since, and no commit of any kind has landed since 2026-07-27 — roughly a month of dormancy, cause undiagnosed, flagged as an observation only. Proposals 16/17/18 remain ratified but not executed (16's self-critique pass never ran, so 17 — sequenced after it — hasn't started either; 18 is correctly still log-only by design). Direction D-2 through D-5 remain ROADMAP-DEFINED, none building. Eng-Hardening Task 1 is complete; Tasks 2-4/7 have no record of having started (they were scoped alongside proposal 16, which hasn't run).

**No repo changes beyond adding this one DRAFT spec file.** No rules file touched, no other doc edited.

## 2026-07-24 (Engineering Hardening directive, Task 1 — secret hygiene, executed same-day on receipt)

*Per `COWORK_DIRECTION_ENG_HARDENING_20260724.md`: Task 1 executes immediately on receipt, ahead of the docs-final gate on other pending publication work. Tasks 2-4 and 7 are this week alongside proposal 16; Tasks 5-6 gate on v0.4 — none of that is executed here.*

### GREEN — Full-history secret scan: clean

Ran two independent scanners plus a manual pattern sweep across the complete git history (all 131 commits on `main`, not just HEAD — the repo is public and the scorer runs with real API keys):

1. **trufflehog3** (v3.0.10), full history depth, pattern + entropy checks: 247 findings, all `high-entropy`/MEDIUM, zero pattern-rule/HIGH hits. Manually sampled and confirmed every one is a legitimate SHA256 hash this project generates on purpose (rules-file hashes, golden-set hashes, scorer `_row_hash` values) — not a credential.
2. **Manual regex sweep** of the full `git log -p --all` output for Anthropic/OpenAI/Google/GitHub/Slack/AWS key formats, PEM private-key blocks, and DB connection strings with embedded credentials: **zero matches**.
3. **File-presence check** for any `.env`/secrets/credentials/private-key file ever added at any commit, even if later deleted: **none found**.

**Result: zero real credentials found anywhere in history.** No rotation needed. Full methodology and results: `docs/SECRET_HYGIENE_SCAN_20260724.md`.

### GREEN — Hardening added

- `scripts/git-hooks/pre-commit` — blocks the same credential patterns from being staged going forward. Requires one-time local activation (`git config core.hooksPath scripts/git-hooks`) — git doesn't run hooks from a tracked directory automatically; noted prominently in the file and in `SECURITY.md`.
- `SECURITY.md` — states the reporting path, current posture, and the API-key-via-environment-variable-only pattern already used throughout the codebase (confirmed, not just asserted: `harness.py`, `ca_notice_scorer.py`, `gemini_health_check.py` all read from `os.environ`/`os.getenv`, no hardcoded key found).
- Confirmed `.gitignore` already excludes `.env` (pre-existing, no change needed).

### BLOCKED (Andy action, cannot be done from a commit) — GitHub secret scanning + push protection

These are repo-level GitHub settings, not something a commit can enable. Andy needs to visit `https://github.com/andrewmichaelcohen-a2j/a2j-ai/settings/security_analysis` and click Enable under both "Secret scanning" and "Push protection" — two toggles, a couple of minutes. Once on, this is a platform-level backstop in addition to the local pre-commit hook.

## 2026-07-24 (morning report — catch-up cycle covering 07-22→07-24, run midday after the 8 AM degraded fire)

### GREEN — Report-side mount break diagnosed + fixed (process miss, logged)

The 8 AM scheduled report ran DEGRADED on 07-24 (no repo access; posted a degraded-run notice only) and produced no cycles at all on 07-22/07-23. Root cause: the scheduled task's Cowork folder connection broke when the repo relocated `~/Documents/GitHub/a2j-ai` → `~/Developer/a2j-ai` (07-21 evening — the same relocation that fixed the dispatcher TCC block). Automated attempts before declaring failure were recorded (mount scan; Google Drive fallback search — only stale June snapshots found; no writes made to them). Fix: folder reconnected at `/Users/andrewcohen/Developer/a2j-ai` inside the task's session; `docs/` and full `rules/validation/` tree visibility verified. Failure-condition items for the missed cycles: 3f (brief regeneration) did not run on 07-22/07-23/07-24-8AM — all healed by this catch-up cycle. Watch tomorrow's 8 AM fire.

### GREEN — Dispatcher confirmation ingested (outage CLOSED-CONFIRMED)

6/6 scheduled fires landed since the 07-21 reinstall: 07-22/07-23/07-24 at both 02:15 AM and 12:00 PM PT, full LOADED→FIRED→PREFLIGHT_DNS→COMPLETED-RUN heartbeat chains, every defer decision correct (deferred-time-window at 02:15; deferred-cadence at noon when < 3d). The 07-21 evening root-cause fix (TCC/`~/Documents` → `~/Developer` relocation + plist reinstall) has now survived three overnight and three noon fires.

### GREEN — D-1 first fully-automatic run ingested (07-23 12:00 PT)

`job_dev_set_monitor_20260715` ran via the dispatcher noon drain — the first dispatcher-driven D-1 execution (prior runs were Terminal/trigger-driven). Result: **dev 12/12 = 100%, α = 1.000 (n=12), DUAL-MODEL-CONSENSUS, single_model_items=0, newly_failing=0**, rules = v3, elapsed ~7.5 min. Monitor self-appended its trend row (`dev_set_trend.jsonl` + ledger D-1 table); this cycle added the morning-report cycle entry with B1–B4. Third consecutive 12/12; second consecutive dual-model. Next cadence-eligible ≥ 07-26.

### GREEN — Night-DNS evidence logged; Northgate retry #3 re-queue PROPOSED (Andy's call)

B-2 preflight probes resolved Gemini (and CL + OpenAI) cleanly at 2:15 AM PT on 07-22, 07-23, and 07-24 — three consecutive clean night windows. First direct evidence the Errno-8 night-DNS strand was part of the same pre-relocation environment problem now fixed. Held item 14 (Northgate retry #3) proposed for re-queue in WORK_QUEUE; not queued autonomously (the 07-09 job instruction gates it on Andy's decision; marginal-value caveat stands).

### GREEN — Living docs updated (this cycle)

METRICS_LEDGER 07-24 catch-up cycle entry; PSOR morning-report annotation; HUMAN_REVIEW_QUEUE header rebuilt (no new items; nothing routed to attorney; RC=6, CI=2 unchanged); WORK_QUEUE header updated with refill proposal; this changelog entry; CLAUDE_CHAT_BRIEF regenerated (3f). Anti-default audit: 0 cases routed RED-attorney this cycle.

---

## 2026-07-23 (Direction D Build-Out & Open-Item Closeout — Andy's directive)

*Documentation-level tasks 1-3 executed this session; task 4 (collateral versioning) blocked pending file supply from Andy. Nothing here preempts proposal 16 (next session) or proposal 17/v0.4 drafting (after 16), per the directive's own sequencing note.*

### GREEN — Task 1: Direction D roadmap formalized

Created `docs/DIRECTION_D_ROADMAP.md`, defining components D-2 (disagreement auto-triage), D-3 (statute-and-case watch), D-4 (standing adversarial self-critique), D-5 (CJaC-lift tracking across model generations). All four are labeled ROADMAP-DEFINED, not building. The invariant is stated verbatim in the doc: AI generates candidates and evidence continuously; nothing self-ratifies; every change lands as a proposal for named-attorney ratification; every applied change passes the dev-set regression gate; held-out sets are burned after one use. Build triggers/sequencing as directed: D-2 wires alongside proposal 17's v0.4 drafting, live before the v0.4 scoring event (so the event itself exercises it); D-3 is first-built after v0.4 scoring completes; D-4's cadence proposal is due with its own build plan (not drafted here); D-5's first data point is the v0.4 ablation arm already required by proposal 17.

### GREEN — Task 2: Repository discoverability pass

Created `docs/VALIDATION_README.md` — a plain-English index (audience: law professors and legal-aid staff, not just engineers) linking to `VALIDATION_METRICS_LEDGER.md`, the v0.3 held-out scorer output JSON, `AUTOPSY_v0_3_MISSES_20260719.md`, the signed errata memo (`.docx` marked authoritative, `.md` as reading copy), and the ratified `RULE_PROPOSAL_1946_2a_ATTACHMENT_20260719.md` / `WIRING_DETERMINATION_1946_2e_20260719.md` pair. States the dual-reporting rule (v0.3 = 23/26 as-scored / 25/26 post-errata, always both) and the multi-model-consensus definition (two independent models must agree; tri-model is roadmap) up front. `README.md`'s "Key documents" list updated to point here first, above the existing methodology/status-ladder/disclaimer links.

**First-time-visitor path, as reported to Andy:** `README.md` → `docs/VALIDATION_README.md` → either `VALIDATION_METRICS_LEDGER.md` (numbers) or `AUTOPSY_v0_3_MISSES_20260719.md` → `ERRATA_MEMO_v0_3_20260719.docx` (a specific correction, start to finish, signed instrument one click away). No step requires prior knowledge of repo structure or file-naming conventions.

### GREEN — Task 3: Schweiger cite-check sweep — clean, one informational flag

Searched the full repository (rules files, docs, checkpoints, scorer/L2 output JSON) for every reference to *Schweiger v. Superior Court*. Result: **every single reference in the repository is correctly tied to the retaliatory-eviction defense** (Civil Code §1942.5) — the case Schweiger actually is authority for. None ties Schweiger to `includes_late_fees` / the notice-overstatement defect. The erroneous citation the directive flagged was confined to the retired two-pager draft and the v3 full deck (outreach collateral, not in the repo) — those are outside this sweep's reach since the files aren't in the repository (see Task 4).

Confirmed the *correct* authority is already what the repository actually uses for the late-fees/overstatement defect: the v0.3 golden set (`rules/validation/golden_sets/DRAFT_CA_notice_candidates_v0.1.json`, item CA-N-010) cites **Levitz Furniture Co. v. Wingtip Communications, Inc.** — and the freeze-time citation-correction log (`VALIDATION_METRICS_LEDGER.md`, "Citation corrections made at freeze") already recorded a pincite fix (1411→1035) matching the directive's stated correct citation (86 Cal.App.4th 1035, 1038) exactly.

**One informational flag, not a repo defect:** `docs/CA_UD_BENCHGUIDE_BG31_EXTRACT.md` quotes *Nourafchan v. Miner* (1985) 169 Cal.App.3d 746 at pincite **763**; the directive's citation gives pincite **753**. This is a benchguide-extract quote (a secondary source), not a rule-file citation, and nothing in the repo's actual rules or golden set depends on the pincite — logging for attorney awareness only, no action taken, no file edited. If it matters at the next version cut, it rides alongside the already-queued §1946.2(a) citation-label fix from proposal 16.

**Conclusion:** no rules-file, doc, or repository collateral requires correction. No proposal generated — there was nothing to propose a fix for.

### GREEN (partial) — Task 4: Collateral versioning — two-pager committed, decks still pending

Andy supplied the final two-pager (2026-07-23). Committed to `collateral/CJaC_Two_Pager_AMC_FINAL.docx` — SHA256 `8019a8beef280951df8f384dd67db63733dc7011b452a1933ef78240a5c2115a`.

**Filename note:** the directive names the file `CJaC_Two_Pager_AMC_07_23_26_FINAL.docx`; the file as delivered is named `CJaC_Two_Pager_AMC_FINAL.docx` (no date stamp). Committed under the delivered filename rather than silently renamed — flagging the discrepancy here rather than guessing which is authoritative. If Andy wants the dated filename, that's a trivial follow-up rename/commit.

**Update (2026-07-23, later same day):** Andy supplied the final pitch deck. Committed to `collateral/CJaC_Pitch_Deck_FINAL.pptx` — SHA256 `9a7f524fce5ecf3e62be30499147eb23189f7b9ccb18fd82f14d824f24e8ed68`.

**Filename/count note:** the directive named two decks (`CJaC_Pitch_Deck_Speaker_20260723.pptx` and `CJaC_Concise_Deck_20260720.pptx`); the file as delivered is a single `CJaC_Pitch_Deck_FINAL.pptx`. Committed under the delivered filename, not renamed or split. Unclear whether this one file supersedes both decks the directive named, or whether a second (concise) deck is still to come — flagging for Andy to confirm rather than assuming either way. Task 4 stays open pending that confirmation.

## 2026-07-21 (evening — decision log: dispatcher RED closed, proposals 16/17/18 ratified)

*Andy's decision log, five items.*

### GREEN — Root-caused and fixed this session

**Dispatcher RED closed (miss ×6, 07-16→07-21).** Root cause: `~/Documents` is a TCC-protected folder on macOS, and background-agent (launchd/smd) spawns are silently blocked from touching files there even with Full Disk Access granted to the target binary — a restriction that does not apply to interactively-typed Terminal commands, which is why every manual invocation of the identical command succeeded while every automated fire failed with `EX_CONFIG` (78) and zero heartbeat-log output. Confirmed via a control test: a trivial LaunchAgent pointed at `/tmp` succeeded cleanly (`hello from launchd`, exit 0); the same job pointed at `~/Documents/GitHub/a2j-ai` failed identically every time. Sleep/power and agent-unloaded hypotheses retired. **Fix (07-21):** repo relocated `~/Documents/GitHub/a2j-ai` → `~/Developer/a2j-ai` (not a TCC-protected folder); `com.cjac.validation.plist` paths updated (`ProgramArguments`, `WorkingDirectory`, `StandardOutPath`, `StandardErrorPath`); old registration fully torn down (`launchctl bootout` + plist removal) and re-registered via `launchctl bootstrap` (not the legacy `load`, which had also gotten the job stuck in a remove/resubmit flapping loop against macOS's newer Background Task Management layer). Live `launchctl kickstart` test confirmed `last exit code = 0` with a complete heartbeat chain (LOADED → FIRED → COMPLETED-RUN, PREFLIGHT_DNS all three endpoints reachable). Confirmation checkpoints: tonight's ~2:15 AM fire (expect fired-and-idled), tomorrow's first 12:00 PM fire (drives D-1 automatically — next monitor run cadence-eligible ≥ 07-23), tomorrow's morning report. Overnight lane reopens; Northgate retry #3 (carried item 14) re-queued on normal prioritization. B-2 DNS preflight probes stay in place (the nighttime Gemini DNS strand predates the path break and is a separate open question, unresolved either way); B-4's pmset recommendation stays held unless probe data shows a genuine sleep issue.

**Git housekeeping flag corrected (not a real issue).** The "last commit 2026-06-16" note in `PROJECT_STATE_OF_RECORD.md`'s Repo Identity table was the audit reading a stale repo copy left at the old `~/Documents/GitHub/a2j-ai` path — same root cause as above. GitHub Desktop confirms: working tree clean, zero uncommitted changes, full history present through today's commits, synced with origin. Corrected in PSOR (Local path + Last commit fields) and WORK_QUEUE; audit checks now point at `~/Developer/a2j-ai`.

**Proposal 18 — ratified source text logged.** Andy supplied the attorney-sourced verbatim statutory text for the Civ. Code §1946.1(d) 30-day sale exception (2025 code, per SB 1103) — logged in `docs/MISSING_RULES_BACKLOG.md`. Per explicit instruction: log-only, no drafting until an item needs it.

### YELLOW — Ratified for next-session execution (not executed this session)

**Proposal 16 — APPROVED.** Self-critique pass (Disciplines A/B/C) over `just_cause_attachment_threshold`, executing next session. Andy's independent verification of §1946.2(a)(2) against verbatim statute text (07-20) is logged as corroboration for that pass; citation label correction ("§1946.2(a), second sentence, prongs (1)–(2)") deferred to the next version cut, not a v3 edit. **Scope extended:** also assess SB 1103's amendments to §1946.1 ("qualified commercial tenants," reworded subdivisions (a)–(c)) for any needed flagged update. Full text in `docs/WORK_QUEUE.md`.

**Proposal 17 — APPROVED, v0.4 is a GO.** Under the amended freeze/drafting protocols, with an added design requirement: the v0.4 held-out scoring event runs a second ablation arm (same models/items, no rules file, same frozen ground truth) to measure the rules' accuracy contribution. Build into the scoring-harness plan before candidate drafting begins; reflect in the v0.4 direction doc. Begins after 16 completes. Full text in `docs/WORK_QUEUE.md`.

### RED — None this cycle.

### Scope note
This entry logs ratification decisions and the dispatcher/housekeeping fixes only. Proposals 16 and 17's substantive execution (the self-critique pass itself; v0.4 candidate drafting and the ablation harness build) is explicitly sequenced for a subsequent session, per Andy's own instruction ("16 executes next session... v0.4 drafting (17) begins after 16 completes") — not performed here.

---

## 2026-07-21 (morning report — automated)

### GREEN — Executed autonomously (morning report cycle)

**Overnight scan — no dispatcher output; SIXTH consecutive missed fire**
- `dispatcher_heartbeat.log` still does not exist (`no-heartbeat`); `launchd_stdout.log` last write still 07-15 ~2:24 AM. Miss ×6 (07-16→07-21). Classification unchanged (agent-unloaded-leaning); folded into the standing RED. No new files in `l2/output/`, `results/`, `scorer/output/`, `queue/`→`done/`/`failed/` since the 07-20 gate run + same-day ingestion.
- Queue holds only the recurring D-1 monitor job; next cadence-eligible ≥ 07-23 (3 days after the 07-20 trigger-fired run) — would have self-deferred at 2:15 AM regardless.

**v3 gate-passed state audited consistent**
- Cross-checked score output (`ca_notice_score_2026-07-20_non-held-out.json`: 12/12, α=1.000, newly_failing=0, rules_sha256 = v3), `dev_set_trend.jsonl` (07-20 row, `triggered_by_rule_change: true`), ledger v3 version record (gate row = PASSED), PSOR header, RULE_PROPOSAL status. All consistent — nothing to correct. Scope note logged in the ledger: the gate verifies dev-set non-regression; direct re-test of the C-18 pattern awaits v0.4.

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR/SM in the attorney lane; HUMAN_REVIEW_QUEUE unchanged (RC=6, CI=2).

**Living docs updated this cycle**
- VALIDATION_METRICS_LEDGER (07-21 cycle entry), PROJECT_STATE_OF_RECORD (morning-report annotation), HUMAN_REVIEW_QUEUE (header — no new items), WORK_QUEUE (header; NOW-empty + proposal-16-gate-met flags; git-commit housekeeping suggestion), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (Step 3f).

### YELLOW — None this cycle.

### RED — Decisions/actions on Andy
1. **Overnight machine environment — miss ×6, `no-heartbeat` (single top RED):** plist reinstall + launchctl reload (unchanged command). Remaining payoffs: reopens the overnight lane; activates the noon fire (D-1's only automatic daytime driver — next eligible run ≥ 07-23 silently won't happen without it or Terminal).
2. **Refill proposals 16–18 approve/reject (from 07-20):** 16 = §1946.2(a)(2) live-source self-critique (its gate condition — v3 regression pass — is now met; executable immediately on approval); 17 = v0.4 golden-set go/no-go (RED-gated); 18 = §1946.1(d) backlog grooming (needs attorney-sourced text).
3. **Housekeeping (non-urgent):** last git commit 2026-06-16 — consider commit/push of the last five weeks of work.

---

## 2026-07-20 (dev-set regression gate PASSED — v3 fully active, errata-cycle directive closed)

*Andy ran the real live regression: `python3 rules/validation/scorer/dev_set_monitor.py` — real keys, 10:31 AM PT, trigger-fired.*

### GREEN — Verified and logged

**Result: 12/12 = 100%, `newly_failing: []`, DUAL-MODEL-CONSENSUS (α=1.000), `triggered_by_rule_change: true`.** Pulled and verified the output directly (`rules/validation/scorer/output/ca_notice_score_2026-07-20_non-held-out.json`) rather than transcribing from screenshot — `rules_sha256` confirmed matches v3 exactly (`65f1d9a4…947c7d`). `RULE_CHANGE_TRIGGER.flag` was consumed by the run itself, as designed.

**Docs corrected from PENDING to PASSED** (the same-day automated morning-report commit had logged this cycle's narrative before the live run completed, so a few spots still said "PENDING" after the fact — fixed, not re-litigated): `docs/VALIDATION_METRICS_LEDGER.md` (v3 version record's gate row; the B3 line in the 07-20 morning-report cycle entry), `docs/PROJECT_STATE_OF_RECORD.md` (header), `docs/RULE_PROPOSAL_1946_2a_ATTACHMENT_20260719.md` (status line).

**Errata-cycle directive (2026-07-19/20) is now closed end-to-end:** v0.3 held-out scored and burned → attorney errata corrected C-21/C-22 → miss autopsy → wiring determination (companion doc, `ca_eviction_v2.json` never touched) → rule proposal for C-18 → Andy's ratification → `ca_eviction_v3.json` cut → dev-set regression gate passed. `ca_eviction_v2.json` (vProof1) remains byte-frozen and immutable throughout, confirmed at every step.

---

## 2026-07-20 (morning report — automated)

### GREEN — Executed autonomously (morning report cycle)

**Overnight scan — no dispatcher output; fifth consecutive missed fire**
- `--heartbeat-status` → `{"state": "no-heartbeat"}`; `dispatcher_heartbeat.log` still does not exist; `launchd_stdout.log` last write still 07-15 ~2:24 AM. Miss ×5 (07-16→07-20). Classification unchanged (agent-unloaded-leaning); folded into the standing RED. No new files in `l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (07-09). Queue holds only the recurring D-1 monitor job.
- D-1 monitor did NOT run despite being cadence-eligible since 07-19 (dispatcher dark; no Terminal run — `dev_set_trend.jsonl` unchanged since the 07-16 baseline). The armed `RULE_CHANGE_TRIGGER.flag` (07-20 07:32 PT) now makes the next run the v3 regression gate.

**Cycle roll-up (no re-logging — pointers only)**
- The weekend's substantive events (v0.3 held-out burn → errata → autopsy → proposal → ratification → v3 cut) were session-driven and already logged in their own dated entries below and in the ledger's Broaden Proof 1 / v3 sections. This cycle added the ledger's 07-20 cycle entry (dual-reported score 88.5%/96.2%, α=1.000, ground-truth error rate 2/26 = 7.7%, B1–B4 with B3=PENDING-REQUIRED).

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR/SM in the attorney lane. The C-18 gap was resolved through the proposal→ratification lane (correct lane, not attorney-queue default); C-21/C-22 were attorney-side ground-truth errors corrected by signed errata — neither touched HUMAN_REVIEW_QUEUE.

**Living docs updated this cycle**
- VALIDATION_METRICS_LEDGER (07-20 cycle entry), PROJECT_STATE_OF_RECORD (morning-report annotation), HUMAN_REVIEW_QUEUE (header — no new items), WORK_QUEUE (header; Broaden Proof 1 Steps 4–7 closed out; refill proposals 16–18), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (Step 3f).

### YELLOW — None this cycle (the v3 cut was ratified RED→approved before this report; nothing new awaiting ratification from this cycle itself).

### RED — Decisions/actions on Andy (standing + new)
1. **Overnight machine environment — miss ×5, `no-heartbeat`:** plist reinstall + launchctl reload (unchanged command); now also auto-runs the armed v3 regression gate at the first noon drain.
2. **v3 dev-set regression gate:** `python3 rules/validation/scorer/dev_set_monitor.py` (real keys, 09:00–23:00 PT; no --force needed). Required: 12/12, newly_failing=0 — else Cowork reverts ACTIVE_RULES_FILE to vProof1 and reports RED.
3. **Residuals:** §1946.2(a)(2) variant verification vs. verbatim statute (carried B4 flag); §1946.1(d) backlog drafting timing; v0.4 golden-set go/no-go.

---

## 2026-07-20 (Task 4: ratified rule applied — new rules version v3 ACTIVE, dev regression pending)

*Context: Andy ratified `docs/RULE_PROPOSAL_1946_2a_ATTACHMENT_20260719.md` ("confirmed - i approve"). Per Task 4 of the errata-cycle directive: cut a new rules version, embed the wiring determination, arm the dev-set regression trigger, and hand off the live-run command.*

### GREEN — Executed autonomously

**New rules version cut — vProof1 untouched**
- `rules/eviction/california/ca_eviction_v3.json` **(new file)** — copy of vProof1 plus: `notice.notice_types.termination.just_cause_attachment_threshold` (Civ. Code §1946.2(a) 12-month general rule + §1946.2(a)(2) additional-adult-tenant variant, exactly as ratified); `notice_defects[missing_just_cause_reason].ab1482_coverage_gate` note updated to check attachment first; `provenance.determinations` now embeds the 2026-07-19 wiring determination verbatim (id `WIRING-DETERMINATION-2026-07-19`); `version_history` block added recording the change and its supersession of vProof1.
- **`ca_eviction_v2.json` (vProof1) is untouched** — confirmed byte-identical, SHA still `cc0cfab63ae1591e2b88…`. It is not deleted; retained permanently as the immutable v0.3 held-out scoring anchor.
- New file SHA256: `65f1d9a46487873163cd9ef5c5e2285c95a68bddb81e876a17e534b3de947c7d`.

**Scorer updated to the new active version (single reference point)**
- Searched the codebase for every consumer of `just_cause_required`/`ab1482_coverage_gate`/the rules file path before changing anything: only `rules/validation/scorer/ca_notice_scorer.py::load_ca_notice_rules()` hardcoded the filename; no test hardcodes it either. Replaced the hardcoded `"ca_eviction_v2.json"` with a named `ACTIVE_RULES_FILE = "ca_eviction_v3.json"` constant, documented so the next version bump is a one-line change.

**Verification performed (mechanical; no live model calls — this sandbox has placeholder keys only)**
- JSON validity: v3 parses clean.
- Battery schema validator (`layer3_notice`) run against v3: 2 errors, both confirmed pre-existing and identical in vProof1 (`notice_defects[6]` consequence/severity values not in the validator's enum) — not introduced by this change, not fixed here (out of scope for this ratification; logged for awareness only).
- `test_ca_notice_scorer_outcome_fallback.py`: 15/15 pass, unaffected by the `ACTIVE_RULES_FILE` change.
- `dev_set_monitor.py --force --dry-run`: pipeline runs end-to-end against v3 with no crashes or schema errors (dry-run always shows all-items-failing by design — mocked predictions, not a real accuracy signal; this only confirms the wiring, not correctness). Stray dry-run output file and `dev_set_trend.jsonl` touch reverted before commit — dry runs must not pollute the real trend log.

**Regression trigger armed for the real gate**
- `arm_trigger()` called — `rules/validation/scorer/output/RULE_CHANGE_TRIGGER.flag` written. The next live `dev_set_monitor.py` run will bypass the 3-day cadence guard automatically (this is exactly the "immediately after any ratified rule change" case the trigger was built for in Item 13). The daytime-window guard still applies — run during Andy's normal window, real keys.

**Docs updated**
- `docs/VALIDATION_METRICS_LEDGER.md`: new v3 version record (parallel structure to the vProof1 freeze record), rule-freeze gate marked PENDING pending the live regression.
- `docs/RULE_PROPOSAL_1946_2a_ATTACHMENT_20260719.md` and `docs/WIRING_DETERMINATION_1946_2e_20260719.md`: both updated from PROPOSED/staged to RATIFIED/embedded, pointing at v3.
- `docs/PROJECT_STATE_OF_RECORD.md`: header updated.

### RED — dev-set regression gate open (not yet run; real keys required)

**For Andy, daytime window, real keys:**
```
cd ~/Documents/GitHub/a2j-ai
python3 rules/validation/scorer/dev_set_monitor.py
```
No `--force` needed — the armed trigger already bypasses cadence. **Required result: 12/12 with `newly_failing=0`.** Any regression → Cowork reverts `ACTIVE_RULES_FILE` to `ca_eviction_v2.json` (vProof1) and reports RED; v3 is not treated as active until this gate passes. Share the output back for the ledger.

**Also carried, unrelated, no action:** `notice_defects[6]` non-enum consequence/severity values (pre-existing in vProof1, inherited into v3 unchanged) — minor schema-validator finding, not blocking, not fixed this cycle.

---

## 2026-07-19 (night — errata-cycle directive Tasks 2 (amended), 3 (narrowed), 4, 5)

*Context: Andy clarified there are two directives in play — the score-cycle directive (Tasks 1-4, executed earlier today) and the errata-cycle directive, which supersedes it in part. Full task text for the outstanding items provided; executed below.*

### Task 2 (amended) — wiring determination recorded as companion doc, not a rules-file edit

- `docs/WIRING_DETERMINATION_1946_2e_20260719.md` **(new)**: records the attorney-ratified negative determination that `ab1482_coverage_gate` correctly does NOT reach `notice_period_too_short` — §1946.2(e) exemptions remove the just-cause obligation only; §1946.1(b)/(c) applies independently (Stancil). **Do not "fix."** `ca_eviction_v2.json` is NOT edited — vProof1 stays byte-frozen at `cc0cfab63ae1591e2b88…` permanently, per Andy's explicit instruction. Staged for the future: once the C-18 rule proposal below is ratified and cuts a new rules version, this determination gets embedded in that version's internal notes/metadata so it travels with the file itself.
- `docs/PROJECT_STATE_OF_RECORD.md`: cross-reference added.
- `docs/AUTOPSY_v0_3_MISSES_20260719.md`: addendum appended — the proposed "exemption-scope-limited-to-single-defect" taxonomy class is marked NOT ADOPTED for this instance (the limitation was legally correct, not a gap); class definition retained in taxonomy notes as a future autopsy check.

### Task 3 (narrowed) — `just_cause_attachment_threshold` rule proposal, YELLOW, ratification-ready

- `docs/RULE_PROPOSAL_1946_2a_ATTACHMENT_20260719.md` **(new)**, supersedes `docs/RULE_PROPOSALS_AB1482_20260719.md` (marked superseded in place, retained for record). One rule: `just_cause_attachment_threshold`, general 12-month rule (source: frozen CA-NOT-C-18 authority field, corroborated against C-19) plus the §1946.2(a)(2) additional-adult-tenant variant (source: attorney-directed text supplied directly in this directive — flagged, not independently statute-verified by Cowork, recommend confirming against verbatim §1946.2(a)(2) at ratification). Inputs are per-tenant occupancy durations (not the aggregate max used elsewhere), since the (a)(2) variant needs per-tenant granularity. Includes a non-regression check against C-19 (already-correct; this proposal must not change its result). `ca_eviction_v2.json` not touched.

### Task 4 — missing-rules backlog entry, no drafting

- `docs/MISSING_RULES_BACKLOG.md` **(new)** — first entry: Civ. Code §1946.1(d), the narrow 30-day sale exception for 1+-year tenancies. Not implicated by any current item; not drafted (no attorney-sourced statutory text for the escrow/sale conditions yet). Andy's call on when to draft.

### Task 5 — golden-set freeze/drafting protocol amended (v0.4 forward)

- `docs/COWORK_DIRECTION_B_GOLDEN_SETS.md` amended in place (dated inline annotations, original text retained): Part 2 step 2 (drafting) now requires each candidate item to declare every defect class its facts implicate, not only the target defect. Part 2 step 3 (freeze/attorney review) now requires an explicit per-item sweep against every encoded defect class in the module (the rules file's ratified defect list serves as the checklist), and states model outputs may not be consulted during ground-truth review. Root cause cited inline: the 2026-07-16 v0.3 freeze session's single-lens review of C-21/C-22, corrected by the same-day errata.

**Nothing else pending in this lane.** Tasks 1-5 of the errata-cycle directive (as clarified) are now complete; Task 3's proposal and the wiring determination await Andy's ratification pass before any new rules version is cut.

---

## 2026-07-19 (late evening — Task 3: candidate rule proposal for C-18, YELLOW, ratification-ready)

*Context: Andy corrected a routing misread — Task 3 of the 07-19 directive was already authorized for C-18 (Task 2 confirmed the §1946.2(a) rule genuinely absent), even though it was correctly not warranted for C-21/C-22 (confirmed not a gap, per errata). Proceeding with Task 3 for C-18 only.*

### YELLOW — proposed, not applied (attorney ratification gate)

**`docs/RULE_PROPOSALS_AB1482_20260719.md` delivered** — one candidate rule, PROPOSED-2026-001: closes the §1946.2(a) 12-month just-cause-attachment gap that caused C-18's miss. Operative text drawn verbatim from the frozen golden-set authority field (attorney-verified 2026-07-16) per the directive's canonical-source requirement — no independent statutory text asserted. Proposed encoding reuses the existing `all_occupants_residency_max_years` input (no new fact input); proposed defect-gate update to `missing_just_cause_reason`'s `ab1482_coverage_gate`, checked ahead of the exemption checklist. One open methodology question flagged for Andy (whether the Stancil any-occupant convention applies to §1946.2(a) attachment, same as it does to §1946.1(b)/(c)) rather than assumed.
- **§1946.2(a)(2)'s 24-month/"additional adult tenants" variant NOT drafted** — no frozen item tests it and no attorney-verified source text specifies the trigger mechanics; flagged for Andy to decide (draft now with source text, defer to this same ratification, or defer to v0.4).
- `ca_eviction_v2.json` **not touched** — proposal only, in ratification-ready item-by-item form mirroring golden-set freeze discipline.

**Confirmed for the record: nothing else pending in this lane.** Task 1 (ledger/state/changelog writeup) and Task 2 (miss autopsy) were both completed and pushed same day (commits `8e894ae`, `aaaa4a5`). Task 4 (post-ratification: cut new rules version, run 12/12 dev regression) is correctly not started — it's staged behind ratification of the proposal above, per the directive's own sequencing, not an oversight.

---

## 2026-07-19 (evening — attorney errata: v0.3 held-out score corrected, C-21/C-22 ground truth was wrong)

*Context: Andy delivered a signed Attorney Errata Memorandum (`docs/ERRATA_MEMO_v0_3_20260719.docx`) same day as the held-out score and miss autopsy, resolving the open legal question the autopsy flagged but could not answer itself.*

### GREEN — Executed autonomously (ingestion + dual-report writeup; no rules or golden-set data touched)

**Errata memo ingested**
- Committed both `docs/ERRATA_MEMO_v0_3_20260719.docx` (signed `/s/ Andrew M Cohen`, dated 07/19/2026 — the executed, authoritative instrument) and `docs/ERRATA_MEMO_v0_3_20260719.md` (plain-text reference copy, flagged at its top as non-authoritative where the two differ).
- The golden-set xlsx (`goldenset_CA_notice_v0.3_FROZEN_20260716.xlsx`) is **unchanged** — SHA256 still `e6dbb2fc…5df45`, still BURNED, still not re-scored. The errata is a correction overlay per the memo's own terms, not a data edit.

**Determination**
- Civil Code §1946.1 (notice-period length) governs independently of §1946.2/AB 1482 (just-cause). An AB 1482 exemption under §1946.2(e)(7)/(e)(8) removes the just-cause obligation only — it does not shorten or excuse §1946.1(b)'s 60-day notice period for a 1+-year tenancy (*Stancil v. Superior Court* (2021) 11 Cal.5th 381). C-21 (18-month tenancy) and C-22 (2-year tenancy), both served 30-day notices, are void under §1946.1(b)/Stancil regardless of their valid AB 1482 exemptions.
- **ERRATUM-2026-001 (C-21) and ERRATUM-2026-002 (C-22): frozen NOTICE_VALID → corrected NOTICE_INVALID.** The dual-model consensus (which had said NOTICE_INVALID) was legally correct; the frozen ground truth was the error. **C-18 unaffected** — 9-month tenancy, 30-day notice proper under §1946.1(c); frozen VALID stands.

**Metrics dual-reported everywhere the v0.3 score is cited** (per the errata memo's Section 4 requirement)
- As-scored (2026-07-19 afternoon): 23/26 = 88.5%, CI [71.0%, 96.0%]. Post-errata: **25/26 = 96.2%**, CI [81.1%, 99.3%] (both Wilson). Neither number superseded — both retained in the record.
- B2 confident-wrong restated: 3 (as-scored) → **1** (post-errata — C-18 only).
- **New metric: ground-truth error rate = 2/26 = 7.7%**, logged as a validation finding in its own right — the review pipeline caught the encoder's citation errors at freeze; the scoring pipeline caught the attorney-side oversight at measurement. Both directions of the loop functioned.
- `docs/VALIDATION_METRICS_LEDGER.md` updated: trend row, Result line, B1-B4 line, v0.2 comparison line, and the B2/autopsy analysis paragraphs — all via append-style annotation (original as-scored text retained, errata correction appended after), not silent rewrite, consistent with this project's frozen-record discipline.
- `docs/PROJECT_STATE_OF_RECORD.md`: new header entry. `docs/AUTOPSY_v0_3_MISSES_20260719.md`: addendum appended noting its flagged open question is now resolved and its engineering conclusion (rules correctly NOT wired to `notice_period_too_short`) is confirmed, while its factual premise (C-21/C-22 as model errors) is superseded.

**Corrective protocol adopted (effective immediately, v0.4 forward)**
- Root cause: single-lens review at the 2026-07-16 freeze session — C-21/C-22 were reviewed only through the AB 1482 exemption analysis they were drafted to test; no independent §1946.1 duration check was run. Classified as an incomplete-defect-sweep failure.
- Going forward, every candidate golden-set item must be swept against every encoded defect class in its module, not only the class it was drafted to test. Model outputs may not be consulted during ground-truth review.

### RED — updated
1. **Overnight machine environment:** unchanged, still open.
2. **§1946.2(e)(7)/(e)(8) wiring/scope gap (C-21, C-22): RESOLVED, closed.** Confirmed not a rules bug — the exemption legitimately does not reach `notice_period_too_short`; no rule edit warranted.
3. **§1946.2(a) 12-month attachment threshold (C-18): still open, still RED.** Genuine coverage gap, confirmed absent from vProof1. `ca_eviction_v2.json` untouched. Awaiting Andy's routing decision.

---

## 2026-07-19 (afternoon — Broaden Proof 1 Steps 5-7: v0.3 held-out set scored and burned)

*Context: Andy ran the real, one-time held-out score from Terminal (real API keys, daytime window, per the freeze memo's own instructions). This is the last step of Broaden Proof 1 — the held-out set is now permanently burned and this result is not to be repeated.*

### GREEN — Executed autonomously (analysis only; no code or rules touched)

**Held-out score ingested and verified**
- Pulled `rules/validation/scorer/output/ca_notice_score_2026-07-19_held-out.json` from the commit Andy pushed. Provenance checks pass: `rules_sha256` matches vProof1 (`cc0cfab63ae1591e2b88…`, unchanged since the 07-02 freeze) and `excel_sha256` matches the certified freeze hash (`e6dbb2fc…5df45`) exactly.
- **Result: 23/26 = 88.5% (95% CI [71.0%, 96.0%], Wilson score interval).** `consensus_status: DUAL-MODEL-CONSENSUS` (both GPT and Gemini answered all 26 items; `single_model_items=0`).
- **Krippendorff's α = 1.000** (GPT vs. Gemini, nominal, n=26, computed by hand from the run's per-item model outcomes: Do=0.000 observed disagreement, De=0.540 expected disagreement from the pooled label distribution). Perfect model-pair agreement.
- **B1:** 88.5% coverage. **B2:** confident-wrong=3 (CA-NOT-C-18, C-21, C-22 — all `model_agreement: AGREE`, both models HIGH confidence, both wrong). **B3:** n/a (first live run against this set). **B4:** no rule changes since vProof1; not triggered.

**B2 finding — a real coverage gap, written up for Andy, no rules touched**
- All three confident-wrong items are AB 1482 exemption fact patterns under Civ. Code §1946.2(e)(7) (new-construction/certificate-of-occupancy exemption) and §1946.2(e)(8) (separately-alienable SFH exemption). Both models correctly applied the *default* just-cause/notice-period requirement and voided the notice for missing it — but the frozen ground truth is NOTICE_VALID because the exemption applies. These are the same three items where Andy's freeze review had to correct the golden-set citations for exactly this (e)(7)/(e)(8) distinction, suggesting the exemption boundary genuinely isn't encoded (or isn't reliably triggered) in `ca_eviction_v2.json` at vProof1.
- **No rule edits made or attempted** — per the freeze record's standing rule ("NO RULE EDITS PERMITTED... discovered gaps → next development cycle with fresh held-out set"). Full writeup with per-item detail is in `docs/VALIDATION_METRICS_LEDGER.md`'s Broaden Proof 1 section.

**Docs updated**
- `VALIDATION_METRICS_LEDGER.md`: trend row updated to BURNED/88.5%; freeze record's "Next step" section replaced with the full result writeup (95% CI, α, B1-B4, B2 cluster analysis).
- `docs/PROJECT_STATE_OF_RECORD.md`: header updated — Broaden Proof 1 now complete end-to-end (Steps 1-7); new RED opened for the §1946.2(e)(7)/(e)(8) coverage gap.

**Follow-up directive received same afternoon: "v0.3 Held-Out Score Ingestion & AB 1482 Rule-Gap Cycle" (Andy, 2026-07-19).** Confirmed Task 1 (ledger/state/changelog writeup) already matched the directive's requirements; added the explicit v0.2→v0.3 comparison line and the "BURNED, dev-set-only, v0.4-gate" language it specified. Executed Task 2 (miss autopsy) below. Task 3 (candidate rule drafting) was gated on Task 2 and did not proceed — see below.

**Miss autopsy executed (Task 2) — result is mixed, not a clean coverage gap**
- Inspected `rules/eviction/california/ca_eviction_v2.json` (confirmed identical to vProof1, SHA matches) directly for each of the three suspect provisions, and cross-referenced against which defect each miss actually fired on (from the score JSON's `gpt_controlling_rule`/`gemini_controlling_rule` fields).
- **§1946.2(a) 12-month attachment threshold: genuinely ABSENT.** `just_cause_required` is a flat `true` with no occupancy-duration gate anywhere in the file — confirmed by full-file search. Explains C-18. Missing-rule hypothesis CONFIRMED for this item.
- **§1946.2(e)(7) and (e)(8): both PRESENT and fully encoded** (rolling 15-year window for (e)(7); two-prong REIT/corp/LLC + written-notice test for (e)(8); both ratified by Andy 2026-07-01). But both models fired `notice_defects[notice_period_too_short]` for C-21/C-22 — a different defect than the one these exemptions are wired to (`missing_just_cause_reason` only). The exemption logic exists, correctly, and simply isn't reachable from the defect that actually fired. Missing-rule hypothesis DISCONFIRMED for these two items.
- Full writeup, including a proposed new error-taxonomy class ("exemption-scope-limited-to-single-defect," YELLOW, not yet adopted) and an open legal question this autopsy cannot resolve (whether the AB 1482 exemption should also reach the general §1946.1(b)/Stancil notice-period defect): `docs/AUTOPSY_v0_3_MISSES_20260719.md`.

### YELLOW — proposed, not adopted
- New error-taxonomy class candidate: "exemption-scope-limited-to-single-defect" (see autopsy memo). Andy's call.

### RED — one gate fully closed, two items opened, Task 3 explicitly not executed
1. **Overnight machine environment:** unchanged, still open (agent-unloaded-leaning; one launchctl action tests+fixes).
2. **§1946.2(a) 12-month attachment threshold — genuine coverage gap (C-18).** `ca_eviction_v2.json` untouched.
3. **§1946.2(e)(7)/(e)(8) wiring/scope gap (C-21, C-22) — NOT a coverage gap.** Per the directive's own stop condition ("if the missing-rule hypothesis is DISCONFIRMED... STOP the cycle... queue as RED"), **Task 3 (candidate rule drafting) was not executed.** Two things need Andy's decision before any rule text is drafted: (a) whether the AB 1482 just-cause exemption should also gate the separate, non-AB-1482 §1946.1(b) notice-period defect, and (b) how to encode the (a) attachment threshold. `ca_eviction_v2.json` untouched.

**Broaden Proof 1 v0.3 held-out freeze RED (the original blocking item): now fully CLOSED** — Steps 1-7 complete, held-out set burned, result logged, autopsy delivered.

---

## 2026-07-19 (morning report — automated)

### GREEN — Executed autonomously (morning report cycle)

**Overnight scan — no new output**
- No new files in `rules/validation/l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (ingested 07-09). `failed/` unchanged (job_nc17_fresh_20260625 only). Queue holds only the recurring D-1 monitor job.

**First live use of the B-3 heartbeat tool — dispatcher miss #4 confirmed definitively**
- `python3 rules/validation/dispatch.py --heartbeat-status` → `{"state": "no-heartbeat"}`. `logs/dispatcher_heartbeat.log` does not exist — the B-1-instrumented `dispatch.py` has never been invoked by launchd since installation (07-16→07-18). `launchd_stdout.log` last write remains 07-15 ~2:24 AM. Fourth consecutive miss (07-16, 07-17, 07-18, 07-19).
- **Diagnostic advance (GREEN analysis, no action taken):** this is the first miss AFTER Andy's Part A mitigation (`sudo pmset -c sleep 0` + lid-open, applied 07-17) — the idle-sleep-timer hypothesis alone no longer explains the pattern; evidence shifts toward **launchd agent-unloaded** (or clamshell/battery sleep outside `pmset -c` scope). Testable and fixable by the same launchctl reinstall steps Andy already needs to activate the 07-18 noon fire.

**Timing escalation — D-1 cadence-eligible TODAY (07-19)**
- Flagged in the morning report with the two concrete paths: (a) plist reinstall before noon → 12:00 PM fire runs the monitor automatically in-window; (b) Terminal fallback `python3 rules/validation/scorer/dev_set_monitor.py` (09:00–23:00 PT). Either is the convert-to-consensus opportunity for the SM-GPT baseline.

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR/SM cases in the attorney lane; the only failure-condition item is the dispatcher miss (infrastructure — logged, folded into the standing RED).

**Living docs updated this cycle**
- VALIDATION_METRICS_LEDGER (07-19 cycle entry incl. heartbeat classification + B1–B4), PROJECT_STATE_OF_RECORD (header), HUMAN_REVIEW_QUEUE (header — no new items), WORK_QUEUE (header + item 15 status + Completed), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (Step 3f).

### YELLOW — None this cycle.

### RED — Escalated (standing, both waiting on Andy)
- **Overnight machine environment (updated):** dispatcher miss ×4, now `no-heartbeat`-classified; agent-unloaded-leaning. Single convergent action: `cp rules/validation/com.cjac.validation.plist ~/Library/LaunchAgents/com.cjac.validation.plist && launchctl unload ~/Library/LaunchAgents/com.cjac.validation.plist && launchctl load ~/Library/LaunchAgents/com.cjac.validation.plist && launchctl list | grep cjac`.
- ~~**v0.3 held-out freeze:** 28 DRAFT items still waiting on attorney review/freeze~~ — **CLOSED later same day:** Andy delivered the completed freeze; see the entry immediately below (26 FROZEN/2 EXCLUDED, Broaden Proof 1 Step 4 COMPLETE). Steps 5-7 (live score) still pending Andy.

---

## 2026-07-18 (v0.3 held-out freeze ingested — Broaden Proof 1 Step 4 COMPLETE; Steps 5-7 pending Andy)

*Context: Andy completed his item-by-item attorney review of the 28-item v0.3 DRAFT held-out set (started per the 07-16 directive), delivering `goldenset_CA_notice_v0.3_FROZEN_20260716.xlsx` + a freeze decision memo. This is the RED gate that has blocked Broaden Proof 1 Steps 5-7 since 07-02. This entry logs ingestion and a scorer bug found while verifying the file was actually scoreable — the real held-out score itself has NOT been run (requires Andy, real API keys, daytime window — see below).*

### GREEN — Executed autonomously

**Freeze ingested and verified**
- Copied `goldenset_CA_notice_v0.3_FROZEN_20260716.xlsx` into `rules/validation/scorer/FROZEN/`. SHA256 verified matching Andy's certified freeze memo both on the raw upload and post-copy: `e6dbb2fcb60de0773f9ff5594e09f74c6a6bac5670c70bd9bb76d70e2645df45`.
- **26 items FROZEN (scoreable), 2 EXCLUDED (C-05, C-13) — n changes from 28 (draft) to 26.** Distribution: NOTICE_VALID=14, NOTICE_INVALID=11, UD_DEFECTIVE_PREMATURE=1. Full detail, rulings, and the six citation corrections made at freeze are in `docs/VALIDATION_METRICS_LEDGER.md`'s updated "v0.3 FROZEN held-out set" record (Broaden Proof 1 section) — not duplicated here.
- **Broaden Proof 1 Step 4 (attorney freeze) is now COMPLETE.** Rules remain frozen at vProof1 (`cc0cfab63ae1591e2b88…`) — this memo authorizes no rule edits, and none were made; only golden-set authority-field corrections (citations), which do not touch `ca_eviction_v2.json`.

**Scorer bug found and fixed while verifying the file was actually scoreable**
- Before handing Andy a "run this once" command for an irreversible held-out burn, dry-ran the pipeline against the real file first (per this project's standing discipline: verify mechanically before a precious one-shot action). Result: `ca_notice_scorer.py` flagged all 26 items as `YELLOW-INCOMPLETE` — it requires "Correct outcome (if corrected)" to be populated for every FROZEN row, but this file leaves that cell blank whenever `ATTORNEY VERDICT=CONFIRM`, which is the natural reading of the column's own name ("if corrected" — Andy didn't correct these, he confirmed them). All 26 FROZEN rows in this file are CONFIRM with a blank "Correct outcome" cell; the two EXCLUDED rows are unaffected (already skipped by status).
- **Fix:** `load_golden_set()` now falls back to the "Drafted outcome" column, but only when `ATTORNEY VERDICT` is `CONFIRM` or `CONFIRMED` — any other verdict (or a blank one) with an empty "Correct outcome" still fails loud via the existing `YELLOW-INCOMPLETE` path, unchanged. An explicit "Correct outcome" value (the v0.2 file's convention — always populated, even on confirms) always wins and is never overridden by this fallback. No golden-set data file was modified — this is purely a parsing fix; the xlsx's SHA256 is identical before and after, still matching Andy's certified hash.
- **Verification:** re-ran the dry-run after the fix — clean load, 0 YELLOWs, 26/26 items resolved. Manually cross-checked all 26 resolved outcomes against Andy's freeze memo ruling table (ID-by-ID) — exact match, including the 14/11/1 distribution. Regression tests added: `rules/validation/tests/test_ca_notice_scorer_outcome_fallback.py`, 15/15 pass, covering the fallback itself, the CONFIRM/CONFIRMED verdict variants, the "explicit value always wins" non-regression case (protects the v0.2 file's existing convention), and that genuinely incomplete rows (blank/unrecognized verdict) still fail loud rather than being silently guessed. Full existing suite re-run clean: `test_dev_set_monitor.py`, `test_dispatcher_heartbeat.py` (34/34), `test_l2_procedural_defects.py` (30/30), `test_retaliation_holdings_disposition_note.py` (26/26).

**Docs updated**
- `VALIDATION_METRICS_LEDGER.md`: Broaden Proof 1 trend row updated to FROZEN/n=26; "v0.3 draft held-out set" record replaced with the full FROZEN record (exclusions, citation corrections, scorer fix, next-step command).
- `docs/PROJECT_STATE_OF_RECORD.md`: Broaden Proof 1 Step 4 marked COMPLETE.

### RED — one gate closed, one step remains (not yet actioned)

**Broaden Proof 1 Steps 5-7 — the actual held-out score — NOT YET RUN.** This is deliberately not something this session executes: (a) requires real `OPENAI_API_KEY`/`GOOGLE_API_KEY` — this sandbox only has placeholders; (b) per Andy's freeze memo, must run in the **daytime window**, not overnight (the environment RED's overnight lane is still being proven out after last night's sleep-timer fix — no reason to risk this precious one-time run on it); (c) burning the held-out set is irreversible — the mechanical pipeline was verified end-to-end via dry-run first specifically so the real run only needs to happen once.

**For Andy, when ready (daytime, real keys):**
```
cd ~/Documents/GitHub/a2j-ai
python3 rules/validation/scorer/ca_notice_scorer.py --golden rules/validation/scorer/FROZEN/goldenset_CA_notice_v0.3_FROZEN_20260716.xlsx --held-out-only
```
No `--dry-run`, no `--force` needed (this script doesn't self-throttle like `dev_set_monitor.py`). Share the output (or the saved `rules/validation/scorer/output/ca_notice_score_*_held-out.json`) back for the 95% CI, Krippendorff's α, and B1-B4 write-up, and to log the burned result in the ledger.

**Also carried:** overnight-environment RED (DNS/sleep fix applied 07-17, `--heartbeat-status` will confirm over the next few nights); C-05/C-13 open-textured queue candidates (not yet scheduled — companion work to the future open-textured module, no urgency).

## 2026-07-18 (follow-up session — noon daytime dispatcher fire + recurring-job fix)

*Context: Andy asked about adding a second (noon) daytime dispatcher fire so Item 13's dev-set monitor (self-throttled to a 09:00–23:00 window) has an automatic driver — the 02:15 overnight fire alone can never land inside that window (flagged as an open structural gap in the 07-17 and prior entries, and as WORK_QUEUE item 15). While wiring it, found and fixed a real bug that would have silently capped the monitor's cadence at exactly one dispatcher-driven run, ever.*

### GREEN — Executed autonomously

**Noon fire added**
- `rules/validation/com.cjac.validation.plist`: `StartCalendarInterval` changed from a single dict to an array — now fires at both 02:15 AM (unchanged) and 12:00 PM. `dispatch.py`'s `SCHEDULED_TIMES` list kept in sync for accurate FIRED-delta computation (see below).
- **Action needed from Andy to activate:** the installed copy at `~/Library/LaunchAgents/com.cjac.validation.plist` is a *copy*, not a symlink — updating the repo file alone doesn't change what launchd runs. After pulling this change: `cp rules/validation/com.cjac.validation.plist ~/Library/LaunchAgents/com.cjac.validation.plist`, then `launchctl unload ~/Library/LaunchAgents/com.cjac.validation.plist && launchctl load ~/Library/LaunchAgents/com.cjac.validation.plist`, then confirm with `launchctl list | grep cjac`.

**Bug found and fixed — recurring jobs were being silently dropped from the queue**
- `finalize_job()` unconditionally moved every job out of `queue/` (to `done/` or `failed/`) after its subprocess exited, regardless of exit code. For one-shot protocol/l2_module jobs that's correct. For Item 13's scorer job — which is designed to sit in the queue indefinitely and self-defer (exit 0, no work done) on any cycle outside its window/cadence — this meant the **very first** dispatcher pickup, successful or not, would remove the job file from `queue/` for good. The job's own JSON already claimed "safe to leave in queue/ for repeated dispatcher drain cycles," but nothing in `dispatch.py` actually honored that. This had not yet manifested only because the dispatcher had not successfully fired since the job went live (07-16 through 07-18 misses) — it would have surfaced silently the first time either the fixed 02:15 fire or the new noon fire actually landed.
- **Fix:** added a `"recurring": true` job-schema field. `finalize_job()` now checks it first — a recurring job stays in `queue/` untouched (no move, no unlink) on both success and failure, so a transient error doesn't drop it either. Set `recurring: true` on `rules/validation/queue/job_dev_set_monitor_20260715.json`. Legacy/one-shot jobs are unaffected — verified by regression test (`test_finalize_job_non_recurring_still_moves_as_before`) that the original move-and-remove behavior is byte-for-byte preserved when `recurring` is absent or false.
- **Related correctness fix:** `_scheduled_fire_time_utc()` (B-1's FIRED-delta baseline) previously assumed a single 02:15 schedule; with two fire times, that would have misreported every noon fire as ~10 hours "late." Replaced with `SCHEDULED_TIMES = [(2, 15), (12, 0)]` and logic that picks whichever slot is most recently in the past relative to the actual fire time — each fire's delta is now computed against its own nearest schedule, not a hardcoded one.
- Regression tests: `rules/validation/tests/test_dispatcher_heartbeat.py` — 34/34 pass (13 new: 3 for `finalize_job` recurring/non-recurring behavior, incl. the failure-path case; 3 for multi-slot schedule resolution, incl. a mid-morning "before either... no, between 02:15 and noon" boundary case). Full existing suite re-run clean: `test_dev_set_monitor.py` 23/23, `test_l2_procedural_defects.py` 30/30, `test_retaliation_holdings_disposition_note.py` 26/26.

### RED / open items — unchanged
- Overnight machine environment RED-strategic item: unchanged by this follow-up (that's Part A, already mitigated 07-17). This work only adds a second fire time and fixes an unrelated queue-persistence bug.
- WORK_QUEUE item 15 (D-1 daytime driver): **resolved by this fire addition**, pending Andy completing the two `launchctl` steps above.

## 2026-07-18 (session — Cowork Change Directive: Dispatcher Resilience & Overnight-Environment Forensics, Part B)

*Directive: "Cowork Change Directive — Dispatcher Resilience & Overnight-Environment Forensics," approved by Andrew M. Cohen, 2026-07-16. Trigger: the 07-16 dispatcher missed fire (later a ×3 pattern through 07-18), folded into the standing overnight-environment RED. Scope split: Part A (machine-side diagnosis: `launchctl`, `pmset -g sched`/`-g log`, sleep settings) was Andy's, executed 2026-07-17 in a separate session — found an aggressive 1-minute idle-sleep timer plus clamshell (lid-close) sleep; mitigated via `sudo pmset -c sleep 0` + a lid-open-overnight practice. Part B below is Cowork's repo-side resilience work, executed this session — none of it required the RED to be resolved first, and none of it is a diagnosis of *why* past nights failed; it's instrumentation so future nights don't require forensic guesswork.*

### GREEN — Executed autonomously (B-1, B-2, B-3)

**Dispatcher is now self-evidencing — B-1: heartbeat log**
- `main_single()` — the function launchd actually invokes nightly at 02:15 via `com.cjac.validation.plist` — now appends to a new append-only `rules/validation/logs/dispatcher_heartbeat.log` (JSONL) on every invocation: `LOADED` (proof launchd ran the process at all, written as the first statement, before any network/queue work), `FIRED` (scheduled-vs-actual delta against the 02:15 Pacific schedule — a large delta, e.g. +4h49m, IS the sleep diagnosis, since launchd coalesces a missed `StartCalendarInterval` fire onto the next wake), and exactly one terminal outcome: `IDLED-EMPTY-QUEUE`, `COMPLETED-RUN <run_id>`, or `ABORTED <reason>`. The whole body is wrapped in try/except/finally so an uncaught exception still writes `ABORTED` rather than leaving a cycle silently unresolved. This is a distinct mechanism from the existing `write_heartbeat()`/`logs/heartbeat.json` snapshot (that one is `--drain`-mode stall detection, polled every cycle, unchanged by this work).
- Ends the previous ambiguity class: a missed launchd fire, a fired-and-idled night, and a fired-and-crashed run used to be distinguishable only by the *absence* of a log line, which forced hand-reconstruction (as happened for the 07-16→07-18 misses). Now each is a distinct, directly-readable event sequence.

**Environment preflight probe — B-2**
- `_preflight_dns_probe()` resolves DNS (resolution only, no payload) for the three endpoints this repo's overnight jobs depend on — CourtListener, `generativelanguage.googleapis.com`, `api.openai.com` — on every fire, logged into the same heartbeat sequence between `FIRED` and queue evaluation. Turns every future night into a DNS data point for the overnight-environment RED at zero marginal cost, replacing the need for after-the-fact run-level forensics like run 9ae49b97's.

**Missed-fire classification — B-3**
- `classify_last_night()` reads `dispatcher_heartbeat.log` and classifies the prior overnight window into exactly one of four states: `no-heartbeat` (machine off/asleep-without-wake, or the launchd agent unloaded — launchd never ran at all), `fired-late-on-wake` (ran, but the FIRED delta exceeds a 30-minute threshold — the delta itself is the sleep diagnosis), `fired-and-idled` (ran on schedule, empty/ineligible queue), or `fired-and-ran` (ran on schedule and attempted a job). Exposed read-only via `python3 rules/validation/dispatch.py --heartbeat-status` (prints JSON) — a morning report should lead with this instead of inferring from log absence, and should raise a MISSED-FIRE banner specifically on `no-heartbeat`.
- Regression tests: `rules/validation/tests/test_dispatcher_heartbeat.py` — 21/21 pass (mock-based, no real subprocess/network). Covers the full LOADED/FIRED/PREFLIGHT_DNS/outcome sequence for idle-queue, completed-run, failed-job, and uncaught-exception paths, all four `classify_last_night()` states, most-recent-cycle-only selection (a stale earlier LOADED doesn't leak into today's classification), and the scheduled-fire-time delta baseline. Full existing suite re-run clean: `test_dev_set_monitor.py` 23/23, `test_l2_procedural_defects.py` 30/30, `test_retaliation_holdings_disposition_note.py` 26/26 — this change is additive to `main_single()`/CLI only; `drain()`, `launch_job()`, `finalize_job()`, `pick_eligible_jobs()` are unchanged.

### YELLOW — Proposed, not applied (B-4)

**launchd plist hardening — `docs/DISPATCHER_PLIST_PROPOSAL.md`**
- Drafted, NOT installed (installing launch agents / changing power settings are Andy-side actions). Recommends `AbandonProcessGroup: true` (prevents launchd cleanup from masquerading as a job failure in the new `ABORTED` classification); explicitly recommends *against* adding `KeepAlive` (wrong model — this is a scheduled job, not a daemon, and `KeepAlive` would fight `StartCalendarInterval` and the daytime-only guardrails already built into `dev_set_monitor.py`) and against flipping `RunAtLoad` to `true`; documents `sudo pmset repeat wakeorpoweron MTWRFSU 02:10:00` as a reserve option, to apply only if `--heartbeat-status` continues showing `fired-late-on-wake` nights after Part A's sleep-timer fix has had a chance to prove itself.
- Added to the overnight-environment RED-strategic item's evidence trail (below) — the plist proposal is now part of what's on record for that RED, alongside the DNS/sleep findings.

### RED — Carried, not new; evidence trail updated
1. **Overnight machine environment (RED-strategic; DNS + dispatcher-miss ×3):** Part A's diagnosis (1-min idle-sleep timer + clamshell sleep) and mitigation (`sudo pmset -c sleep 0` + lid-open) are on record as of 07-17. Evidence trail now also includes `docs/DISPATCHER_PLIST_PROPOSAL.md` (B-4, above). Resolution is no longer guesswork going forward — `python3 rules/validation/dispatch.py --heartbeat-status` gives a direct daily read on whether the fix held; check it over the next several mornings before this RED is called closed. Unblocks overnight runs + Northgate retry #3 (item 14) + automatic D-1 cadence.
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7. In progress (Andy).

## 2026-07-18 (morning report, fired on time at 8:01 AM — no-run cycle; dispatcher missed fire ×3; D-1 cadence-eligible tomorrow with no driver)

### GREEN — Executed autonomously

**Overnight scan — dispatcher missed fire #3**
- No 07-18 ~2:15 AM fire: `launchd_stdout.log` last write remains 2026-07-15 ~2:24 AM; no new dispatch log file. Third consecutive launchd-side miss (07-16, 07-17, 07-18) — sustained pattern; agent-unloaded/machine-asleep hypothesis further strengthened. Folded into the standing overnight-environment RED (checks unchanged: machine power/sleep; `launchctl list | grep com.cjac`; pmset wake schedule).
- No substantive loss: the only queued job (`job_dev_set_monitor_20260715.json`, live_verified) self-defers outside 09:00–23:00 PT. No new files in `l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (07-09). Cumulative MV=26/CI=4/RC=6 unchanged.

**Timing flag raised — D-1 cadence eligibility 2026-07-19**
- The dev-set monitor becomes cadence-eligible tomorrow (3 days after the 07-16 baseline). With the dispatcher dark AND no daytime driver (proposal 15 undecided), the run will silently not happen. Fallback for Andy: run `python3 rules/validation/scorer/dev_set_monitor.py` from Terminal during the 09:00–23:00 PT window. That run is also the convert-to-consensus opportunity for the SM-GPT baseline if Gemini capacity has recovered.

**Report-side cadence note CLOSED**
- Third consecutive clean 8 AM fire (07-16 8:00, 07-17 8:03, 07-18 8:01) — per the 07-14 criterion ("a third clean fire would justify closing it"), the report-side settings-check note is closed. Dispatcher-side checks remain open and are the live problem.

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR or SM case in the attorney lane; only failure-condition item is the dispatcher miss (infrastructure, logged, folded into RED).

**Living docs updated this cycle**
- METRICS_LEDGER (2026-07-18 cycle entry with B1–B4), PROJECT_STATE_OF_RECORD (header), HUMAN_REVIEW_QUEUE (header — no new items), WORK_QUEUE (header + Completed Today), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (step 3f).

### YELLOW — None new this cycle. Carried unratified (5): extended search backoff ladder (07-08) + FLAG-generate-failed→PR routing fix (07-06) — both live-verified 07-09; VT 4467→4465 (07-03); backoff v1 (07-05); run-57cf7b37 RC→PR reclassification (07-06). Carried YELLOW *proposal* awaiting Andy's pick: WORK_QUEUE item 15 (D-1 daytime driver) — now time-sensitive (cadence eligibility 07-19).

### RED — Carried, not new (both block progress)
1. **Overnight machine environment (RED-strategic; DNS + dispatcher-miss ×3):** dispatcher has not fired since 07-15. Checks: machine power/sleep, `launchctl list | grep com.cjac`, pmset wake schedule; DNS strand (night-window Errno-8) unchanged. Unblocks overnight runs + Northgate retry #3 (item 14) + automatic D-1 cadence.
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7.

---

## 2026-07-17 (morning report, fired on time at 8:03 AM — Direction D-1 baseline ingested; dispatcher missed fire ×2)

### GREEN — Executed autonomously

**Direction D-1 baseline run INGESTED (run executed by Andy, Terminal, 2026-07-16 18:27 PT)**
- Per the 07-15/16 session instruction, Andy ran `python3 rules/validation/scorer/dev_set_monitor.py --force` with live keys and flipped `live_verified: true` on `job_dev_set_monitor_20260715.json` (18:11 PT). Direction D-1 is now fully ACTIVE end-to-end.
- Baseline result: **dev 12/12 = 100.0%** (v0.2 dev split; all 12 expected item IDs present), `newly_failing=0`, `n_yellows=0`; `rules_sha256` matches vProof1 (`cc0cfab6…` — freeze intact) and `excel_sha256` matches the 07-01 FROZEN record. Outputs: `ca_notice_score_2026-07-16_non-held-out.json` + first `dev_set_trend.jsonl` row; the monitor self-appended its Direction D-1 ledger row (append path verified live).
- **Consensus: SM-GPT — all 12 Gemini calls failed 503 UNAVAILABLE (capacity).** Per the hard consensus gate, the baseline is PRELIMINARY, not consensus-validated, and is recorded as such everywhere. Not routed anywhere (anti-default: API failure = re-run lane). Convert-to-consensus path: re-run (or wait for the 07-19+ cadence run) once Gemini capacity recovers — same 503 class as 07-01/07-02, which cleared on its own.
- **Diagnostic value for the standing RED:** a served 503 at 18:27 PT means DNS/TCP/TLS to the Gemini endpoint SUCCEEDED from Terminal in daytime. The overnight `[Errno 8]` DNS failures are therefore a night-window-specific failure mode, distinct from Google-side capacity. Narrows Andy's diagnosis to the overnight environment (resolver/filter schedule, sleep, power).

**Overnight scan — dispatcher missed fire #2**
- No 07-17 ~2:15 AM fire: `launchd_stdout.log` last write remains 2026-07-15 ~2:24 AM; no new dispatch log file. Second consecutive launchd-side miss (07-16, 07-17) — now a pattern, strengthening the agent-unloaded/machine-asleep hypothesis. Folded into the standing overnight-environment RED (checks unchanged: machine power/sleep; `launchctl list | grep com.cjac`; pmset wake schedule).
- No substantive loss: the only queued job (dev-set monitor, now live_verified) self-defers outside 09:00–23:00 PT, so a 2:15 AM fire would have deferred anyway. No new files in `l2/output/`, `results/`, `done/`, or `failed/`.
- **Structural gap flagged (new):** the dispatcher's only fire time (2:15 AM) is ALWAYS outside the monitor's window → D-1 cadence has no automatic daytime driver. Proposal 15 added to WORK_QUEUE (YELLOW — Andy picks: second daytime launchd fire vs. morning-report drain call).

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR or SM case in the attorney lane (the 12 Gemini-503 SM items stay in the re-run lane); no other failure conditions triggered.

**Living docs updated this cycle**
- METRICS_LEDGER (2026-07-17 cycle entry with B1–B4; D-1 row was self-appended by the monitor — referenced, not duplicated), PROJECT_STATE_OF_RECORD (header + Direction D-1 section → LIVE), HUMAN_REVIEW_QUEUE (header — no new items), WORK_QUEUE (header, Completed Today, items 11/13 → DONE, proposal 15 added), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (step 3f).

### YELLOW — None new this cycle. Carried unratified (5): extended search backoff ladder (07-08) + FLAG-generate-failed→PR routing fix (07-06) — both live-verified 07-09; VT 4467→4465 (07-03); backoff v1 (07-05); run-57cf7b37 RC→PR reclassification (07-06). New YELLOW *proposal* (not executed): WORK_QUEUE item 15 (D-1 daytime driver).

### RED — Carried, not new (both block progress)
1. **Overnight machine environment (RED-strategic; DNS + dispatcher-miss ×2):** NARROWED this cycle — daytime path to Gemini confirmed fine (503 = served response); remaining question is the overnight environment only. Checks: dscacheutil day-vs-night, scutil --dns, router/filter schedules, machine power/sleep, `launchctl list | grep com.cjac`, pmset. Unblocks overnight runs + Northgate retry #3 (item 14).
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7.

---

## 2026-07-15/16 (session — Cowork Change Directive: Items 11 & 13; Items 12/14 HELD)

*Directive: "Cowork Change Directive — Approved Refill Items 11 & 13," approved by Andrew M. Cohen, 2026-07-15. Items 12 (per-call backoff extension) and 14 (Northgate retry #3) remain HELD pending the Gemini-endpoint DNS diagnosis and were NOT actioned under this directive. Session note: this work was done in a sandbox without access to the local repo clone; a separate local push (commit d068e05, "l2 validations") landed the 07-02 through 07-16 history — including the real network-retry-ladder work (2026-07-05 fix, 2026-07-08 extension) and the RC-misroute fix (2026-07-06) — while this session was in progress. Rebased Item 11 on top of that real prior work rather than duplicating it; see below.

### GREEN — Executed autonomously (Item 11)

**Harness `disposition_note` mislabel fix — search-network-failure vs. genuine no-candidates**
- Problem (as proposed in the 2026-07-08 GREEN observation, "WORK_QUEUE NEXT item 11"): the search-network-failure path recorded the same disposition note as the genuine no-CL-coverage path, conflating outages with true coverage gaps.
- On inspection, `_run_search()` already had a real network-retry ladder (2026-07-05 fix, extended 2026-07-08 to 60/120/240/600/1200/1800s, ~66 min ride-out) that correctly computes a `net_err` flag internally and prints the distinction — but that signal was never wired into the `disposition_note` actually persisted to run output. That wiring is the fix:
  - `cl_search_retaliation_by_state()` now records the final `net_err` verdict in module-level `_LAST_SEARCH_NETWORK_FAILURE[state]` (True only when the search ended in a network failure with no cases found). No change to the existing retry/backoff logic or timing.
  - `protocols/retaliation_holdings_v3.py::get_units()` tags the "no cases" sentinel unit with `search_network_failure`, read from that flag immediately after `load_draft_cases()`.
  - `run_unit()` emits `"search-network-failure: CourtListener unreachable after full backoff ladder — not a coverage determination"` when the flag is set, and the byte-identical original text `"No candidate cases in draft file for this state."` otherwise. `disposition` (`permanent-failure`), `bucket`, and `queue_routing` (`None`) are unchanged in both cases — verified by regression test, not just inspection.
  - No routing logic was touched (the separate 2026-07-06 RC→PR misroute fix for FLAG-generate-failed is a different code path — Check C generate-step routing — and was left exactly as-is). Confirmed cleanly cosmetic; did not need to escalate to YELLOW.
- Regression tests: `rules/validation/tests/test_retaliation_holdings_disposition_note.py` — 26/26 pass. Covers: full-backoff-ladder-then-flag (7 attempts, real ladder), genuine-empty-not-flagged, recovery-after-transient-errors, non-connection-exception handling (matches the runner's existing fail-fast-but-not-genuine semantics), cases-found-clears-flag, `get_units()` tagging (all cases), and `run_unit()` disposition_note text + disposition/queue_routing byte-identity for both paths plus the missing-key default.
- Full existing regression suite re-run: `test_l2_procedural_defects.py` — 30/30 pass (unaffected, unrelated module).
- **Backfill-tagging of prior run artifacts (directive item 4, optional/low-cost) — DONE, now that real artifacts are available:** confirmed exactly three runs hit the mislabeled sentinel path — `retaliation_holdings_v3_2026-07-03_c0a2df2d.json` (VT), `retaliation_holdings_v3_2026-07-04_c7bcdcff.json` (VT), and `retaliation_holdings_v3_2026-07-08_e9222548.json` (VT) — each stored `disposition_note: "No candidate cases in draft file for this state."` for what the changelog independently documents (07-03, 07-04, 07-08 entries) as DNS/NameResolutionError outages, not genuine no-CL-coverage. **Correction annotation only — the three JSON artifacts themselves were NOT modified** (per instruction; frozen historical record stays frozen): had this fix been live on those nights, all three would have read `"search-network-failure: CourtListener unreachable after full backoff ladder — not a coverage determination"` instead. The other two DNS-affected nights in the 07-03–07-09 window (57cf7b37 07-06, 9ae49b97 07-09) hit the separate FLAG-generate-failed→PR path, already corrected by the 2026-07-06 fix — not in scope for this annotation.
- Logged here for the next morning report GREEN digest.

### YELLOW — Ratified by Andy 2026-07-15 (Item 13)

**Direction D, Component 1 (Monitoring/Measurement) — built and ratified; moves from proposed to ACTIVE**
- Built `rules/validation/scorer/dev_set_monitor.py`: scheduled scorer job running `ca_notice_scorer.py` against the v0.2 FROZEN golden set with `--non-held-out-only` (the real 12-item dev split: CA-NOT-B-02, B-05–B-12, B-15–B-17, per the 2026-07-01 v0.2 FROZEN entry — verified against the actual FROZEN xlsx). Confirmed distinct from the separate v0.3 held-out DRAFT set (`goldenset_CA_notice_v0.3_DRAFT_20260702.xlsx`, created 07-02 per Broaden Proof 1) — this component never touches that file.
- Guardrails enforced in code (not just convention): dev-set-only (defense-in-depth assertion against the expected 12 IDs, hard-stops rather than silently scoring an unexpected item); read-only w.r.t. rules; daytime/evening-only self-throttle (09:00–23:00 Pacific; blocks the ~2:15 AM window that has now produced six consecutive intentionally-empty overnight cycles per the DNS RED) enforced by the script itself regardless of external scheduler timing; 3-day cadence self-throttle with an `arm_trigger()` hook wired for "run immediately after any ratified rule change" (armed manually for now — no rule change possible until v0.3 scoring completes, so it has never fired; satisfies "wire the trigger now"). Also confirmed this component's daytime runs do NOT violate the standing "overnight queue intentionally empty" hold, which applies to the overnight lane only.
- Per-run output: dev score (n/12), per-item pass/fail, `newly_failing` vs. the immediately prior run (regression = confirmed-passing → failing; new/never-scored items never flagged as regressions), α on the dev split (= model-agreement rate, this repo's existing convention), and consensus/model status. Appends to `docs/VALIDATION_METRICS_LEDGER.md` under a new "Direction D-1" section (created on first real run); pushes an alert into this changelog when `newly_failing` is non-empty.
- Dispatcher wiring: added `job_type: "scorer"` to `rules/validation/dispatch.py` (`_build_scorer_cmd`), fully additive — `protocol` and `l2_module` job types untouched. Queued `rules/validation/queue/job_dev_set_monitor_20260715.json`.
- Regression tests: `rules/validation/tests/test_dev_set_monitor.py` — 23/23 pass. Covers the `newly_failing` diff logic directly, daytime-window boundaries, the 3-day cadence boundary, and that the ledger/changelog append path fires only when `newly_failing` is non-empty and names the regressed item(s) — the regression-flag path was verified end-to-end with simulated data, not just eyeballed.
- **First baseline run: NOT executed.** This session only had placeholder API credentials, so the full pipeline was validated in `--dry-run` (guardrails, dev-set membership, ledger/changelog wiring all pass) but no real accuracy score was fabricated. The queued job has `live_verified: false` per the dispatcher's own existing gate — run `python3 rules/validation/scorer/dev_set_monitor.py --force` once from Terminal with real keys to establish the actual baseline, then flip `live_verified: true`.
- `docs/PROJECT_STATE_OF_RECORD.md` updated: Direction D-1 added under Validation Harness Status as ACTIVE (built, baseline pending live keys).
- Ratification ledger: this item moves from proposed (WORK_QUEUE NEXT item 13, per the 07-08 refill proposals) to **ratified 2026-07-15**.

### RED — None this cycle (Items 12 and 14 remain HELD per the directive; not actioned).


## 2026-07-16 (morning report, fired on time at 8:00 AM — no-run cycle with NEW anomaly: dispatcher did NOT fire overnight; queue was intentionally empty anyway; no new output)

### GREEN — Executed autonomously

**Overnight scan — nothing to ingest, but a dispatcher-side anomaly found**
- **Dispatcher did NOT fire 2026-07-16 ~2:15 AM.** Evidence: `launchd_stdout.log` last write 2026-07-15 ~2:24 AM; no "Queue is empty" line for 07-16; no new dispatch log file (`find rules/validation/logs -newermt 2026-07-15 23:00` → empty). First launchd-side missed fire since the 06-25 FDA fix — all prior cadence anomalies (07-08 double, 07-10 missed, 07-12 late, 07-15 late) were on the Cowork report side; the dispatcher had fired reliably in the 2:15–2:25 window every night.
- No substantive loss: the live queue contains only `.gitkeep` + the sample format file (Northgate retry #3 still deliberately held on the Gemini-DNS RED), so a fire would have idled (would have been the seventh consecutive intentionally-empty night).
- No new files in `rules/validation/l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (ingested 07-09). `failed/` unchanged (job_nc17_fresh_20260625 only).
- State unchanged: cumulative MV=26/CI=4/RC=6; VT 1 MV (Gokey) + 1 CI (Houle); vProof1 rule freeze intact (no rule edits).

**Cadence observation**
- Report-side: this cycle fired at 8:00 AM PDT — on time (clean fire after the 07-15 ~30-min-late fire). Settings-check note stays open.
- Dispatcher-side: MISSED FIRE (above). Checks for Andy before anything is re-queued: was the Mac off or asleep-without-wake overnight; `launchctl list | grep com.cjac` (agent still loaded?); pmset wake schedule. This overlaps the power/schedule strand of the Gemini-DNS RED — both point at the overnight machine/network environment — so it is FOLDED into that standing RED-strategic item, not opened as a separate RED.

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR or SM case in the attorney lane; no other failure conditions triggered.

**Living docs updated this cycle**
- METRICS_LEDGER (2026-07-16 no-run entry + dispatcher-miss note), PROJECT_STATE_OF_RECORD (header), HUMAN_REVIEW_QUEUE (header rebuilt — no new items), WORK_QUEUE (header + Completed Today), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (step 3f).

### YELLOW — None new this cycle. Carried unratified (5): extended search backoff ladder (07-08) + FLAG-generate-failed→PR routing fix (07-06) — both with live-verification evidence from run 9ae49b97; VT 4467→4465 (07-03); backoff v1 (07-05); run-57cf7b37 RC→PR reclassification (07-06).

### RED — Carried, not new (both block progress; queue stays idle until one resolves)
1. **Gemini-endpoint DNS diagnosis + overnight machine environment (RED-strategic, 07-09; BROADENED 07-16):** now also covers the 07-16 dispatcher missed fire — check machine power/sleep overnight and `launchctl list | grep com.cjac` alongside the DNS checks (dscacheutil day-vs-night, scutil --dns, router/filter schedules). Unblocks overnight runs + Northgate retry #3.
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7.

---

## 2026-07-15 (morning report, fired ~8:30 AM — ~30 min late — no-run cycle: sixth consecutive intentionally-empty night on the Gemini-DNS RED; no new output)

### GREEN — Executed autonomously

**Overnight scan — nothing to ingest (expected)**
- Dispatcher fired 2026-07-15 ~2:24 AM; logged "Queue is empty or no eligible jobs — nothing to do" (launchd_stdout.log). Sixth consecutive intentionally-idle night (07-10 through 07-15): Northgate retry #3 remains held pending Andy's Gemini-endpoint DNS diagnosis per the 07-09 job's escalation instruction.
- No new files in `rules/validation/l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (ingested 07-09). `failed/` unchanged (job_nc17_fresh_20260625 only). Live queue contains only `.gitkeep` + sample format file.
- State unchanged: cumulative MV=26/CI=4/RC=6; VT 1 MV (Gokey) + 1 CI (Houle); vProof1 rule freeze intact (no rule edits).

**Cadence observation (streak broken)**
- This report cycle fired ~8:30 AM PDT — ~30 minutes late. Breaks the two-clean-fire streak (07-13, 07-14); the standing settings-check note for Andy is RETAINED (it was one clean fire from closing). Mild anomaly — same class as the 07-12 late fire, milder. Dispatcher-side cadence remains normal (2:24 AM within the observed 2:15–2:25 window).

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR or SM case in the attorney lane; no other failure conditions triggered.

**Living docs updated this cycle**
- METRICS_LEDGER (2026-07-15 no-run entry + cadence note), PROJECT_STATE_OF_RECORD (header), HUMAN_REVIEW_QUEUE (header rebuilt — no new items), WORK_QUEUE (header + Completed Today), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (step 3f).

### YELLOW — None new this cycle. Carried unratified (5): extended search backoff ladder (07-08) + FLAG-generate-failed→PR routing fix (07-06) — both with live-verification evidence from run 9ae49b97; VT 4467→4465 (07-03); backoff v1 (07-05); run-57cf7b37 RC→PR reclassification (07-06).

### RED — Carried, not new (both block progress; queue stays idle until one resolves)
1. **Gemini-endpoint DNS diagnosis (RED-strategic, 07-09):** unblocks overnight runs + Northgate retry #3. Suggested checks in 07-09 entry (dscacheutil day-vs-night, scutil --dns, router/filter schedules).
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7.

---

## 2026-07-14 (8 AM morning report, fired on time at 8:01 — no-run cycle: fifth consecutive intentionally-empty night on the Gemini-DNS RED; no new output)

### GREEN — Executed autonomously

**Overnight scan — nothing to ingest (expected)**
- Dispatcher fired 2026-07-14 ~2:15 AM; logged "Queue is empty or no eligible jobs — nothing to do" (launchd_stdout.log). Fifth consecutive intentionally-idle night (07-10 through 07-14): Northgate retry #3 remains held pending Andy's Gemini-endpoint DNS diagnosis per the 07-09 job's escalation instruction.
- No new files in `rules/validation/l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (ingested 07-09). `failed/` unchanged (job_nc17_fresh_20260625 only). Live queue contains only `.gitkeep` + sample format file.
- State unchanged: cumulative MV=26/CI=4/RC=6; VT 1 MV (Gokey) + 1 CI (Houle); vProof1 rule freeze intact (no rule edits).

**Cadence observation (second clean fire)**
- This report cycle fired at 8:01 AM PDT — on schedule. Second consecutive clean fire (07-13, 07-14) after the three-anomaly stretch (07-08 double-fire, 07-10 missed, 07-12 ~3 h late). Standing settings-check note for Andy retained one more cycle; a third consecutive clean fire would justify closing it.

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR or SM case in the attorney lane; no other failure conditions triggered.

**Living docs updated this cycle**
- METRICS_LEDGER (2026-07-14 no-run entry + cadence note), PROJECT_STATE_OF_RECORD (header), HUMAN_REVIEW_QUEUE (header rebuilt — no new items), WORK_QUEUE (header + Completed Today), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (step 3f).

### YELLOW — None new this cycle. Carried unratified (5): extended search backoff ladder (07-08) + FLAG-generate-failed→PR routing fix (07-06) — both with live-verification evidence from run 9ae49b97; VT 4467→4465 (07-03); backoff v1 (07-05); run-57cf7b37 RC→PR reclassification (07-06).

### RED — Carried, not new (both block progress; queue stays idle until one resolves)
1. **Gemini-endpoint DNS diagnosis (RED-strategic, 07-09):** unblocks overnight runs + Northgate retry #3. Suggested checks in 07-09 entry (dscacheutil day-vs-night, scutil --dns, router/filter schedules).
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7.

---

## 2026-07-13 (8 AM morning report, fired on time — no-run cycle: fourth consecutive intentionally-empty night on the Gemini-DNS RED; no new output)

### GREEN — Executed autonomously

**Overnight scan — nothing to ingest (expected)**
- Dispatcher fired 2026-07-13 ~2:15 AM; logged "Queue is empty or no eligible jobs — nothing to do" (launchd_stdout.log). Fourth consecutive intentionally-idle night (07-10 through 07-13): Northgate retry #3 remains held pending Andy's Gemini-endpoint DNS diagnosis per the 07-09 job's escalation instruction.
- No new files in `rules/validation/l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (ingested 07-09). `failed/` unchanged (job_nc17_fresh_20260625 only). Live queue contains only `.gitkeep` + sample format file.
- State unchanged: cumulative MV=26/CI=4/RC=6; VT 1 MV (Gokey) + 1 CI (Houle); vProof1 rule freeze intact (no rule edits).

**Cadence observation (first clean fire)**
- This report cycle fired at 8:00 AM PDT — on schedule. First clean fire since the three-anomaly stretch (07-08 double-fire, 07-10 missed, 07-12 ~3 h late). One data point does not close the standing settings-check note for Andy; retained until a few consecutive on-time fires.

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR or SM case in the attorney lane; no other failure conditions triggered.

**Living docs updated this cycle**
- METRICS_LEDGER (2026-07-13 no-run entry + cadence note), PROJECT_STATE_OF_RECORD (header), HUMAN_REVIEW_QUEUE (header rebuilt — no new items), WORK_QUEUE (header + Completed Today), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (step 3f).

### YELLOW — None new this cycle. Carried unratified (5): extended search backoff ladder (07-08) + FLAG-generate-failed→PR routing fix (07-06) — both with live-verification evidence from run 9ae49b97; VT 4467→4465 (07-03); backoff v1 (07-05); run-57cf7b37 RC→PR reclassification (07-06).

### RED — Carried, not new (both block progress; queue stays idle until one resolves)
1. **Gemini-endpoint DNS diagnosis (RED-strategic, 07-09):** unblocks overnight runs + Northgate retry #3. Suggested checks in 07-09 entry (dscacheutil day-vs-night, scutil --dns, router/filter schedules).
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7.

---

## 2026-07-12 (morning report, fired ~11 AM — no-run cycle: third consecutive intentionally-empty night on the Gemini-DNS RED; no new output)

### GREEN — Executed autonomously

**Overnight scan — nothing to ingest (expected)**
- Dispatcher fired 2026-07-12 ~2:15 AM; logged "Queue is empty or no eligible jobs — nothing to do" (launchd_stdout.log). Third consecutive intentionally-idle night (07-10, 07-11, 07-12): Northgate retry #3 remains held pending Andy's Gemini-endpoint DNS diagnosis per the 07-09 job's escalation instruction.
- No new files in `rules/validation/l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (ingested 07-09). `failed/` unchanged (job_nc17_fresh_20260625 only). Live queue contains only `.gitkeep` + sample format file.
- State unchanged: cumulative MV=26/CI=4/RC=6; VT 1 MV (Gokey) + 1 CI (Houle); vProof1 rule freeze intact (no rule edits).

**Cadence observation (third data point)**
- This report cycle fired ~11:00 AM PDT instead of 8 AM. Combined with the 07-08 double-fire and the 07-10 missed cycle, the scheduled-task cadence is now unstable in three distinct ways (double, missing, late). No substantive loss this time (no overnight output existed), but the standing note to Andy is upgraded: worth checking the Cowork scheduled-task settings before the next live overnight run, so ingestion doesn't lag a real result.

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR or SM case in the attorney lane; no other failure conditions triggered.

**Living docs updated this cycle**
- METRICS_LEDGER (2026-07-12 no-run entry + cadence note), PROJECT_STATE_OF_RECORD (header), HUMAN_REVIEW_QUEUE (header rebuilt — no new items), WORK_QUEUE (header + Completed Today), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (step 3f).

### YELLOW — None new this cycle. Carried unratified (5): extended search backoff ladder (07-08) + FLAG-generate-failed→PR routing fix (07-06) — both with live-verification evidence from run 9ae49b97; VT 4467→4465 (07-03); backoff v1 (07-05); run-57cf7b37 RC→PR reclassification (07-06).

### RED — Carried, not new (both block progress; queue stays idle until one resolves)
1. **Gemini-endpoint DNS diagnosis (RED-strategic, 07-09):** unblocks overnight runs + Northgate retry #3. Suggested checks in 07-09 entry (dscacheutil day-vs-night, scutil --dns, router/filter schedules).
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7.

---

## 2026-07-11 (8 AM morning report — no-run cycle: queue intentionally empty on the Gemini-DNS RED; no new output; 07-10 report cycle missing)

### GREEN — Executed autonomously

**Overnight scan — nothing to ingest (expected)**
- Dispatcher fired 2026-07-10 and 2026-07-11 ~2:15 AM; both nights logged "Queue is empty or no eligible jobs — nothing to do" (launchd_stdout.log). This is the intended state: Northgate retry #3 is held pending Andy's Gemini-endpoint DNS diagnosis per the 07-09 job's own escalation instruction.
- No new files in `rules/validation/l2/output/`, `results/`, `done/`, or `failed/` since run 9ae49b97 (ingested 07-09). `failed/` unchanged (job_nc17_fresh_20260625 only).
- State unchanged: cumulative MV=26/CI=4/RC=6; VT 1 MV (Gokey) + 1 CI (Houle); vProof1 rule freeze intact (no rule edits).

**Process gap logged — missing 2026-07-10 cycle**
- No 07-10 entry exists in this changelog or METRICS_LEDGER — the scheduled morning report appears not to have fired (or fired without logging) on 07-10. Failure condition acknowledged. No substantive loss: no overnight output existed that day. Gap recorded in METRICS_LEDGER per honesty discipline. Note for Andy: combined with the 07-08 duplicate fire, scheduled-task cadence looks unstable in both directions — worth a settings check.

**Anti-default audit**
- 0 cases routed RED-attorney this cycle; no PR or SM case in the attorney lane; no other failure conditions triggered.

**Living docs updated this cycle**
- METRICS_LEDGER (2026-07-11 no-run entry + missed-cycle note), PROJECT_STATE_OF_RECORD (header), HUMAN_REVIEW_QUEUE (header rebuilt — no new items), WORK_QUEUE (header + Completed Today), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated (step 3f).

### YELLOW — None new this cycle. Carried unratified (5): extended search backoff ladder (07-08) + FLAG-generate-failed→PR routing fix (07-06) — both with live-verification evidence from run 9ae49b97; VT 4467→4465 (07-03); backoff v1 (07-05); run-57cf7b37 RC→PR reclassification (07-06).

### RED — Carried, not new (both block progress; queue stays idle until one resolves)
1. **Gemini-endpoint DNS diagnosis (RED-strategic, 07-09):** unblocks overnight runs + Northgate retry #3. Suggested checks in 07-09 entry (dscacheutil day-vs-night, scutil --dns, router/filter schedules).
2. **v0.3 held-out freeze (RED gate, Broaden Proof 1 Step 4):** 28 DRAFT items await Andy's item-by-item review → FROZEN; blocks Steps 5–7.

---

## 2026-07-09 (8 AM morning report — Northgate retry #2: selective Gemini-endpoint DNS failure; all 5 units PR; two YELLOW fixes live-verified; retry #3 held for Andy)

### GREEN — Executed autonomously

**Overnight run 9ae49b97 ingested — VT Northgate generate retry #2**
- Job `job_vt_northgate_generate_retry2_20260708` → done/ at 2026-07-09 15:38 UTC, returncode=0. 5 units, elapsed 343.4 min. Summary: `SUMMARY_retaliation_holdings_v3_2026-07-09_1538.md`; raw: `retaliation_holdings_v3_2026-07-09_9ae49b97.json`; PR list: `retaliation_holdings_v3_PR_9ae49b97.json`.
- Result: **all 5 VT units → PR (`generate-api-failure-transient`)**. Checks A (existence) and B (currency) succeeded via CourtListener for all 5 cases across the entire run; every Check C Gemini generate call failed DNS getaddrinfo `[Errno 8]` for ~5.7 h. Method rate n/a (0÷0); overall 0/5 = 0% (retrieval/generate-gated, two-rate rule); α n/a (no dual-model pairs). Cumulative MV=26/CI=4/RC=6 unchanged. VT case statuses unchanged (Gokey MV, Houle CI [VT-HOLD-CI-01], Atwood/Vladyka wrong-doc CLOSED, Northgate PR).

**Live verification of two pending YELLOW fixes (evidence for ratification)**
- Extended search backoff ladder (07-08 YELLOW): first CL search attempt DNS-failed; 60s retry succeeded; statute query returned 5 in-state candidates; Check E rejected 2 wrong-jurisdiction hits. **Worked as designed.**
- FLAG-generate-failed→PR routing fix (07-06 YELLOW): **first live exercise — PASSED.** 5/5 generate failures routed PR; zero RC artifacts (contrast pre-fix run 57cf7b37); nothing routed to attorney.

**GREEN diagnosis — DNS failure is selective; machine-sleep hypothesis weakened**
- No wall-clock anomaly this run (dispatch → harness start 35 min = search retry ladder; continuous per-case progress 23:54→05:38 local). CL API resolved and answered at every hour of the night (one transient CL error on case 3 recovered on retry) while the Gemini hostname failed persistently on the same machine/process. Conclusion: not lid-close sleep, not a CL outage — a local resolver/filter issue specific to the Google API endpoint at night. RED-strategic reframed accordingly (see RED).

**Queue management**
- Overnight queue intentionally left empty: per the job's own instruction ("if DNS again, escalate rather than extend backoff further"), Northgate retry #3 is held pending Andy's decision. Proposed as WORK_QUEUE NEXT item 14, gated on the RED. NEXT refill proposals 11–13 carried; item 12 (per-call backoff) annotated as complementary-not-sufficient given tonight's 5.7 h persistence.

**Living docs updated this cycle**
- METRICS_LEDGER (run 9ae49b97 entry, two rates + bucket counts + PR quarantine=5), PROJECT_STATE_OF_RECORD (header + holdings section), HUMAN_REVIEW_QUEUE (audited — no new items; 0 RC, 0 MODEL-SPLIT; PR never enters attorney lane), WORK_QUEUE (header, item 4, Completed Today, NEXT 12/14), DAILY_CHANGELOG (this entry), CLAUDE_CHAT_BRIEF regenerated.

### YELLOW — None new this cycle. Carried unratified: ladder extension (07-08), RC-misroute fix (07-06), VT 4467→4465 (07-03), backoff v1 (07-05), run-57cf7b37 RC→PR reclassification — the first two now carry live-verification evidence (above).

### RED — Escalated, not decided by Cowork

**RED-strategic (reframed) — nightly DNS failure is selective to the Gemini endpoint**
- Five DNS-affected nights since 07-03; tonight's evidence isolates the failure: CourtListener resolved fine all night, Gemini hostname failed for ~5.7 h, machine demonstrably awake and processing.
- For Andy (his machine, his call): check router/DNS filtering or profiles that could block/fail `generativelanguage.googleapis.com` at night (Pi-hole/NextDNS schedules, VPN toggles, Screen Time/content filters); compare `dscacheutil -q host -a name generativelanguage.googleapis.com` day vs. ~2–5 AM; check `scutil --dns` resolver config. Power-settings question (07-08) demoted but not closed — the 07-07 wall-clock gap remains unexplained.
- Northgate retry #3 queued only after this is resolved.

---

## 2026-07-08 (late-day audit cycle — duplicate scheduled fire; no new overnight output; consistency audit PASSED)

### GREEN — Executed autonomously

**Audit cycle (scheduled task fired a second time on 2026-07-08)**
- Scanned `rules/validation/l2/output/`, `results/`, `queue/`, `done/`, `failed/`, and logs: **no new files since the 8 AM cycle.** The only output in the last 48 h is run e9222548 (already ingested at 8 AM). `failed/` unchanged (job_nc17_fresh_20260625 only).
- Queue state verified: `job_vt_northgate_generate_retry2_20260708.json` is the sole live job — validated JSON, fires 2026-07-09 2:15 AM (retries Northgate; live-exercises the FLAG-generate-failed→PR routing fix and the extended 60/120/240/600/1200/1800s ladder).
- Living-doc consistency audit PASSED: METRICS_LEDGER (e9222548 entry present, N/A rates with rationale), PROJECT_STATE_OF_RECORD, HUMAN_REVIEW_QUEUE (header rebuilt 07-08; no new items; RC=6, CI=2), WORK_QUEUE (last-updated 07-08; NEXT refills 11–13 proposed), CLAUDE_CHAT_BRIEF (generated 07-08, derives from current canonicals) — all mutually consistent. No stale-doc process miss this time.
- Anti-default audit: **0 cases routed RED-attorney this cycle** (and 0 at the 8 AM cycle). No PR or SM case in the attorney lane. No failure conditions triggered.
- No ingestion, no rule changes, no metrics changes — cumulative MV=26, CI=4, RC=6 unchanged. CLAUDE_CHAT_BRIEF confirmed current (step 3f satisfied by audit; content unchanged, timestamp annotated).
- Note for Andy: two morning-report fires on the same calendar day — worth checking the Cowork scheduled-task cadence/timezone if this recurs (GREEN observation, no change made).

### YELLOW — None this cycle (audit only; 8 AM YELLOWs carry unratified).

### RED — None new. Carried: overnight-run power/schedule (machine-sleep hypothesis); v0.3 held-out freeze (28 items, Step 4).

---

## 2026-07-08 (8 AM morning report — Northgate retry DNS failure #4; backoff ladder extended; machine-sleep hypothesis flagged)

### GREEN — Executed autonomously

**Overnight run e9222548 ingested — VT Northgate generate retry (GREEN)**
- Job `job_vt_northgate_generate_retry_20260706` (dispatched 2026-07-07 2:16 AM PT) → done/ at 2026-07-08 03:11 UTC, returncode=0.
- **Infrastructure failure, fourth DNS-affected night since 07-03:** DNS NameResolutionError to www.courtlistener.com on ALL 5 attempts of BOTH queries (4465 statute + broad fallback) — the 2026-07-05 backoff ladder (60/120/180/240s, ~10 min/query) worked as designed but was outlasted. Runner correctly labeled it "PR-class infrastructure failure, NOT a genuine no-CL state."
- 0 candidates → `VT::__no_cases__` permanent-failure, queue_routing=None. **Anti-default upheld — nothing routed to attorney.** No validation rate logged (harness 0/1=0% is a DNS artifact; N/A per two-rate honesty rules). No model calls → α N/A.
- Consequences: Northgate's generate never retried; the 2026-07-06 FLAG-generate-failed→PR routing fix remains live-unexercised. VT status unchanged (1 MV Gokey + 1 CI Houle). Cumulative MV=26/CI=4/RC=6.

**Wall-clock anomaly diagnosed → machine-sleep hypothesis (GREEN diagnosis; decision flagged RED-strategic)**
- Dispatch 2:16 AM PT; harness unit-processing timestamps 5:11 PM PT — ~15 h gap that ~20 min of retry sleep cannot explain. Hypothesis: the Mac sleeps mid-run despite `caffeinate -ims` (lid-close sleep overrides caffeinate; network down in dark-wake), which would also explain the recurring "2:15 AM DNS window" across c0a2df2d/c7bcdcff/57cf7b37/e9222548. Power/schedule settings are Andy's machine — flagged as RED-strategic decision, not changed autonomously.

**Queue refilled (GREEN)**
- Queue was EMPTY. `job_vt_northgate_generate_retry2_20260708.json` created (VT, fresh=true; retries Northgate; live-exercises both the routing fix and the new extended ladder). JSON validated. Fires 2026-07-09 2:15 AM.

**GREEN observation (candidate fix, proposed to NEXT, not applied)**
- Harness `disposition_note` for the search-network-failure path still reads "No candidate cases in draft file for this state" — cosmetic mislabel (routing unaffected). Proposed as WORK_QUEUE NEXT item 11.

**Living docs updated (GREEN)**
- METRICS_LEDGER: 2026-07-08 cycle entry (N/A rates with rationale, diagnosis chain, actions; note that no 07-07 cycle entry exists — job was in flight). PROJECT_STATE_OF_RECORD: header + VT section. HUMAN_REVIEW_QUEUE: header rebuilt, **no new items**. WORK_QUEUE: header, NEXT item 4 residual note, Completed Today, 3 proposed NEXT refills (items 11–13). CLAUDE_CHAT_BRIEF regenerated (step 3f). This changelog entry.

### YELLOW — For ratification
1. **Network-retry ladder extension** in `rules/validation/l2/retaliation_holdings_v3_runner.py` `_run_search`: 60/120/180/240s (~10 min/query) → 60/120/240/600/1200/1800s (~66 min/query). Justification: run e9222548 exhausted the old ladder on both queries. Reversible (restore old ladder). py_compile clean; 30/30 regression tests pass. Caveat noted in code: if the machine-sleep hypothesis is right, longer backoff only helps while the process is actually running.
- *(Carried, unratified: 4467→4465 VT statute config [07-03]; RC-misroute fix [07-06]; search backoff v1 [07-05]; run-57cf7b37 RC→PR ingestion reclassification [07-06].)*

### RED — Decisions needed
- **RED-strategic (NEW): overnight-run power/schedule.** Evidence suggests the Mac sleeps mid-run and/or has no network at the 2:15 AM window (4 DNS-affected nights; 15-h wall-clock gap in e9222548). Options: (a) keep the machine on AC with lid open / display-off; (b) `sudo pmset repeat wakeorpoweron` a few minutes before dispatch; (c) move the launchd dispatch to a time the machine is reliably awake (e.g., 7:30 AM before the 8 AM report, or overnight only when docked). Cowork cannot change launchd/pmset (outside repo); needs Andy's terminal.
- Carried, not new: **v0.3 held-out freeze — 28 draft items waiting on Andy** (Broaden Proof 1 Step 4; blocks Steps 5–7).

---

## 2026-07-06 (8 AM morning report — VT Gokey → MV ✅; RC-misroute bug fixed; 07-04/07-05 backfill)

### GREEN — Executed autonomously

**Overnight run 57cf7b37 ingested — VT Gokey retry2, 2026-07-06 13:03 UTC (GREEN)**
- Job `job_vt_gokey_retry2_20260705` → done/ at 13:03 UTC. 5 VT units, 162.5 min.
- **The 2026-07-05 DNS-retry backoff fix WORKED:** first statute query hit NameResolutionError at 00:20, retried on 60s backoff, succeeded → 5 in-state candidates (Check E rejected 2 wrong-jurisdiction hits).
- **🎯 Gokey v. Bessette, 154 Vt. 560, 580 A.2d 488 (Vt. 1990) → MV.** A=true (cluster 1539041, citation match); B=OK-machine (13 citing, no negative treatment); C=corroborated (Gemini generate → GPT-4o verify, agree); D=STATED — verbatim §4465 burden-shifting controlling quote. Below attorney line. Written to `vt_eviction_v2.json` machine_verified_cases; candidate → MV; validation_status → GOKEY-MV-COMPLETE. Cumulative MV=26.
- Vladyka v. Marsh → PR wrong-doc CLOSED (habitability case, Gemini high-confidence not-retaliation). Atwood re-encountered, re-confirmed wrong-doc, no change.

**Anti-default enforcement AGAINST the harness — 2 RC reclassified PR (GREEN ingestion + YELLOW code fix)**
- Run 57cf7b37 emitted RC for Houle v. Quenneville and Northgate Hous. v. White. Both `check_c.generate_output.error = "[Errno 8] nodename nor servname provided"` — the per-case Gemini generate call failed on DNS mid-run. **No legal evaluation occurred. These are PR-class infrastructure failures, not attorney items.**
- Reclassified PR on ingestion (Northgate → generate retry lane; Houle → disregarded, already CI [VT-HOLD-CI-01], CI status unchanged). NOT added to HUMAN_REVIEW_QUEUE. RC count remains 6.
- Root cause: `protocols/retaliation_holdings_v3.py` routed `FLAG-generate-failed` to RC ("generate API failure" branch) — structural anti-default violation. **Fixed:** FLAG-generate-failed now routes PR with `pr_reason=generate-api-failure-transient`; added to `is_pr` detection. *Verified: py_compile clean; 30/30 regression tests pass.* (YELLOW — see below.)
- Corrected run buckets: MV=1, CI=0, RC=0, PR=4, SM=0. Corrected method rate 1/1 (n=1, statistically meaningless); overall 1/5. Harness-reported 1/3=33% method rate is contaminated — do not cite.

**Backfill — 07-04/07-05 cycle actions that were never logged (process miss, GREEN-fixed)**
- Run c7bcdcff (2026-07-04): second consecutive DNS failure at ~2:25 AM PT, both queries; 4465 fix never exercised; no validation rate logged (N/A per two-rate honesty rules). Now in METRICS_LEDGER.
- 2026-07-05 fix (was unlogged): `_run_search` network-error retry with 60/120/180/240s backoff in `retaliation_holdings_v3_runner.py`; error paths no longer mislabeled "genuine no-CL state" (YELLOW, listed below). `job_vt_gokey_retry2_20260705` queued.
- **Failure conditions acknowledged for 07-04/07-05 cycles:** GREEN actions with no changelog entry; CLAUDE_CHAT_BRIEF not regenerated (stale since 07-03); METRICS_LEDGER/STATE_OF_RECORD not updated. All backfilled this cycle.

**Queue refilled (GREEN)**
- Queue was EMPTY. `job_vt_northgate_generate_retry_20260706.json` created (VT, fresh=true; retries Northgate's failed generate; live-exercises the routing fix — any repeat network failure must land PR, never RC). JSON validated. Fires 2026-07-07 2:15 AM.

**Living docs updated (GREEN)**
- METRICS_LEDGER: 2026-07-06 cycle entry (both runs, corrected buckets, α note, cumulative MV=26). PROJECT_STATE_OF_RECORD: header + VT section + cumulative counters. HUMAN_REVIEW_QUEUE: header rebuilt, **no new items**. WORK_QUEUE: header, NEXT item 4 closed (VT complete), Completed Today. CLAUDE_CHAT_BRIEF regenerated (step 3f). This changelog entry.

### YELLOW — For ratification
1. **RC-misroute fix** in `rules/validation/protocols/retaliation_holdings_v3.py`: `FLAG-generate-failed` → PR (`generate-api-failure-transient`) instead of RC. Changes bucket routing (affects future method-rate denominators — makes them cleaner). Revert = restore `"RC"` branch. Compile + 30/30 tests pass.
2. **Network-retry backoff (applied 2026-07-05, logged now):** `_run_search` in `rules/validation/l2/retaliation_holdings_v3_runner.py` retries ConnectionError/Timeout with 60/120/180/240s backoff. Proven live in run 57cf7b37. Revert = remove retry loop.
3. **Ingestion reclassification of run 57cf7b37's 2 RC → PR** (documented in METRICS_LEDGER; raw output JSON untouched). Reversible by re-reading the raw file.
- *(Carried, unratified: VT statute config 4467→4465 from 2026-07-03.)*

### RED — None new this cycle
- Carried, not new: **v0.3 held-out freeze — 28 draft items waiting on Andy** (Broaden Proof 1 Step 4; blocks Steps 5–7).
- Noted for Andy (not blocking): per-case model API calls have no network backoff (the 07-05 fix covers CL search only) — if Northgate's retry hits DNS again, proposal is to extend backoff to generate/verify calls (would be YELLOW).

---

## 2026-07-03 (8 AM morning report — VT Gokey run failed on DNS; config fix + re-queue)

### GREEN — Executed autonomously

**Overnight VT Gokey run ingested — run_id=c0a2df2d, 2026-07-03 09:17 UTC (GREEN)**
- Job: `job_vt_gokey_20260702.json` → moved to `done/` at 09:17 UTC; returncode=0 but run produced 0 candidates.
- **Root cause: infrastructure.** DNS resolution to `www.courtlistener.com` failed (`NameResolutionError`) on both the VT statute query and the broad fallback at 2:17 AM PT — network/DNS unavailable on the machine at dispatch time. Retrieval never occurred; Gokey (CL cluster 1539041) was never fetched. Harness recorded `VT::__no_cases__` → permanent-failure.
- **No validation rate logged** — the harness's 0/1=0% overall rate is a DNS artifact, not a verified miss. Recorded as N/A in METRICS_LEDGER per two-rate honesty rules.
- Anti-default rule upheld: nothing routed to attorney. Cumulative counters unchanged (MV=25, CI=4, RC=6).

**Secondary pipeline findings from diagnosis (GREEN diagnosis; one YELLOW fix)**
- `_STATE_RETALIATION_STATUTES["VT"]` was `"4467"` — 9 V.S.A. §4467 is the termination-of-tenancy notice statute, not retaliation (§4465). The 2026-07-02 CourtListener MCP search that identified Gokey used "4465" and returned exactly the right two cases (Houle + Gokey). **Fixed 4467→4465** in `retaliation_holdings_v3_runner.py` (YELLOW — see below). Runner compiles clean (`py_compile` pass).
- Job fields `target_cluster_id`/`target_case` are NOT consumed: `dispatch.py` passes only `--states`/`--fresh`; the runner has no targeted-cluster mode. With the 4465 fix, the statute-targeted query should return Gokey directly. Targeted-cluster mode noted as a possible future enhancement — proposed only, not built.

**Re-queue (GREEN)**
- `rules/validation/queue/job_vt_gokey_retry_20260703.json` created (retaliation_holdings_v3, VT, fresh=true, sleep=20; prior_run_id=c0a2df2d, failure mode documented). JSON validated. Queue was otherwise empty — tonight's 2:15 AM dispatch now has work.

**Living docs updated (GREEN)**
- METRICS_LEDGER: 2026-07-03 cycle entry added (run c0a2df2d, N/A rates with rationale, root-cause chain, actions).
- PROJECT_STATE_OF_RECORD: header + VT holdings section updated.
- WORK_QUEUE: header, NEXT item 4, Completed Today updated.
- HUMAN_REVIEW_QUEUE: no new items (correct — nothing interpretive this cycle).
- CLAUDE_CHAT_BRIEF regenerated (step 3f).
- This changelog entry.

### YELLOW — For ratification
- **VT statute-query config fix (4467→4465)** in `rules/validation/l2/retaliation_holdings_v3_runner.py` `_STATE_RETALIATION_STATUTES`. One-token, reversible, source-anchored (9 V.S.A. §4465 = retaliation; corroborated by the 2026-07-02 MCP search evidence recorded in WORK_QUEUE/METRICS_LEDGER). Affects only the VT CL search query. Revert = change back to "4467".

### RED — None new this cycle. (Carried, not new: v0.3 held-out freeze — 28 draft items waiting on Andy.)

---

## 2026-07-02 (Broaden Proof 1 direction received — rules frozen, v0.3 draft CREATED)

### GREEN — Executed autonomously

**Broaden Proof 1 direction ingested + executed (GREEN)**

*Direction doc:* `docs/COWORK_DIRECTION_BROADENPROOF1_20260702.md`

**Step 0 — B3 gate: ✅ PASSED (3 confirmations)**
- 12/12 = 100.0% DUAL-MODEL-CONSENSUS (agree=12, disagree=0, errors=0), confirmed three runs on 2026-07-02.

**Step 1 — CA-notice rules FROZEN as vProof1:**
- File: `rules/eviction/california/ca_eviction_v2.json`
- SHA256 (vProof1): `cc0cfab63ae1591e2b88353c557aeb8027767d99276a3115b5ce9f4115599b93`
- State: post REVISED-8 + REVISED-9; 9 self-critique corrections from 2026-07-01
- **No rule edits permitted until after v0.3 held-out score is logged.**

**Step 3 — v0.3 held-out DRAFT created (28 candidates):**
- File: `rules/validation/scorer/FROZEN/goldenset_CA_notice_v0.3_DRAFT_20260702.xlsx`
- SHA256 (at-creation): `5f2c25c15b34bb7b209a6bd7900e9f4804063340e39fed481779984dc0489e0d`
- 28 candidates; all Status=DRAFT; all Held-out=TRUE; v0.2 items NOT reused
- Outcome distribution (DRAFT): NOTICE_VALID=15, NOTICE_INVALID=12, UD_DEFECTIVE_PREMATURE=1
- Coverage: pay-or-quit (counts, amounts, content), cure-or-quit (§1161(3)), unconditional quit (§1161(4)), AB 1482/§1946.2, service methods (CCP §1162), multi-defect, edge cases
- Sources: CCP §1161/§1162/§1946.2; BG31 (2015, authority cross-checked against current statute per Discipline A); SB 611 (eff. 2/1/2025); AB 1482; case law per item
- Independence: all 28 are genuinely new — NOT paraphrases of v0.2 items
- B4 currency: BG31 is 2015; each item's authority cross-checked against current CA statute; SB 611 and AB 1482 amendments incorporated in relevant items

**Living docs updated (GREEN):**
- METRICS_LEDGER: vProof1 freeze record added; v0.3 draft row added to repeatability view
- WORK_QUEUE: Broaden Proof 1 sequence added to NOW
- Direction doc saved: `docs/COWORK_DIRECTION_BROADENPROOF1_20260702.md`

**BLOCKED — waiting on Andy:** Step 4 (Andy reviews + freezes 28 draft items) must come before Steps 5-6 (score + report). No rule edits in the interim.

### YELLOW — None new.

### RED — None new.

---

## 2026-07-02 (8 AM morning report cycle — audit + Atwood resolution + queue refill)

### GREEN — Executed autonomously

**Overnight-ingestion audit (GREEN)**
- Verified run 1153a763 (VT retry) fully ingested and consistent across METRICS_LEDGER, HUMAN_REVIEW_QUEUE, PROJECT_STATE_OF_RECORD, WORK_QUEUE (all updated in the pre-8AM session). No un-ingested output files found. failed/ unchanged. No new attorney items required.

**Atwood VT wrong-doc GREEN investigation — RESOLVED (GREEN)**
- CourtListener MCP search (`retaliatory eviction "4465"`, court=vt, opinions) returned exactly 2 results: Houle v. Quenneville (already CI) and **Gokey v. Bessette, 154 Vt. 560, 580 A.2d 488 (Vt. 1990)** — the foundational VT retaliatory eviction case (the "Gokey standard" referenced in Houle's proposed holding). Published, cited 17×, CL cluster 1539041.
- `rules/eviction/vermont/vt_eviction_v2.json` updated: Gokey added to holdings.candidates (UNVERIFIED, identified_by=courtlistener_mcp_search); Houle candidate_status → CI with confirm_inference_cases entry (run 1153a763, [VT-HOLD-CI-01]); Atwood recorded in pr_cases as wrong-doc CLOSED; holdings.validation_status → RUN-COMPLETE. JSON validated.
- Anti-default rule upheld: Atwood never touched the attorney lane; wrong-doc PR resolved by pipeline investigation as designed.

**Overnight queue refilled — tonight's job queued (GREEN)**
- Queue was EMPTY at 8 AM (tonight's 2:15 AM dispatch would have idled). `rules/validation/queue/job_vt_gokey_20260702.json` created: retaliation_holdings_v3, states=VT, fresh=true, sleep=20, target Gokey cluster 1539041. JSON validated.

**Krippendorff's α added for v0.2 scorer runs (GREEN)**
- Computed from per-item model predictions in the score JSONs (nominal, 2 raters, no missing data): held-out α=0.667 (n=5, D_o=0.200, D_e=0.600); dev α=0.867 (n=12, D_o=0.083, D_e=0.627); combined agreement stat α=0.806 (n=17; scores themselves never blended). Both disagreements are Gemini-UNCERTAIN (appropriate caution), not confident splits. Added to METRICS_LEDGER v0.2 block with small-n caveat.

**Living docs updated (GREEN)**
- METRICS_LEDGER: α block + 8 AM audit addendum. PROJECT_STATE_OF_RECORD: VT Gokey resolution. WORK_QUEUE: Atwood item resolved, queue-refill logged, NEXT item 4 closed. CLAUDE_CHAT_BRIEF regenerated (was stale from 2026-07-01 — flagged as process miss, fixed this cycle). This changelog entry.

### YELLOW — None new this cycle.

### RED — None new this cycle. (B3 regression check and CI confirms remain with Andy — carried, not new.)

---

## 2026-07-02 (morning report — VT retry overnight ingested; Gemini 503 CLEARED; scorer unblocked)

### GREEN — Executed autonomously

**VT retry overnight run ingested — run_id=1153a763, 2026-07-02 02:16 UTC (GREEN)**
- Job: `job_vt_retry_gemini_restored_20260701.json` → moved to `done/` at 02:16 UTC; returncode=0
- Summary file: `rules/validation/results/SUMMARY_retaliation_holdings_v3_2026-07-02_0916.md`
- Raw output: `rules/validation/l2/output/retaliation_holdings_v3_2026-07-02_1153a763.json`
- **GEMINI 503 CLEARED:** Both VT cases received Gemini 2.5-pro responses (no 429/503 errors). Andy's credit top-up worked.
- **Atwood v. Hill (VT)** → **PR** — reason: `case-not-relevant-to-retaliation-likely-wrong-doc`. Gemini (high confidence): this case is about damages, back rent, security deposit — not retaliation. CL cluster_id=10145325 is the wrong document. GREEN pipeline investigation item (not attorney lane — wrong doc, not legal failure).
- **Houle v. Quenneville (VT)** → **CI** — two-model corroborated, D=INFERRED. Gemini generated, GPT-4o verified as "accurate". Holding: tenants failed to prove retaliatory eviction; initial eviction attempt may have been retaliatory, but subsequent non-renewal was based on lease expiration + repairs completed (not prior violations). No verbatim controlling quote extracted — routes to cheap confirm lane.
- Bucket counts: MV=0, CI=1, RC=0, PR=1, SM=0. Method rate: 0/1=0%. Overall rate: 0/2=0%. (Houle CI is below the attorney line — not machine-verified.)
- Added VT-HOLD-CI-01 (Houle v. Quenneville) to HUMAN_REVIEW_QUEUE (cheap confirm lane)

**Stage 2 scorer UNBLOCKED — Gemini working (GREEN)**
- BLOCKED item "All Gemini-dependent overnight runs" removed from WORK_QUEUE BLOCKED list (Gemini 503 capacity issue resolved)
- Stage 2 dual-model scorer run moved to NOW in WORK_QUEUE
- Atwood VT wrong-doc GREEN investigation added to NEXT

**v0.2 held-out score BURNED — 5/5 = 100.0% DUAL-MODEL-CONSENSUS (GREEN)**
- Run: `ca_notice_score_2026-07-02_held-out.json`; scorer v2.0-excel-native; run_date=2026-07-02
- Consensus status: DUAL-MODEL-CONSENSUS (both models answered on all 5 items)
- Score: **5/5 = 100.0%** (small-sample result, n=5; 95% CI: [47.8%, 100%]; directional signal only)
- Model agreement: agree=4, disagree=1 (CA-NOT-B-18: Gemini UNCERTAIN on owner-occupied duplex inception condition; GPT correct; ground truth NOTICE_VALID confirmed by Andy)
- B2 (confident-wrong): 0. No high-confidence wrong predictions.
- 🟡 YELLOW flag — CA-NOT-B-18: Gemini legitimately flagged that §1946.2(e)(7) requires owner occupancy at inception of tenancy; scenario doesn't state this explicitly. Ground truth resolves as NOTICE_VALID. Scenario-quality note; no rules encoding change required.
- Held-out set PERMANENTLY BURNED — these 5 items cannot be re-scored against a tuned model
- METRICS_LEDGER updated with full B1–B4 report + per-item table
- Dev set (12 items) run pending — awaiting Andy's terminal run of `--non-held-out-only`

**v0.2 dev set scored — 10/12 = 83.3% DUAL-MODEL-CONSENSUS (GREEN)**
- Run: `ca_notice_score_2026-07-02_non-held-out.json`; 12 items; agree=11, disagree=1
- Score: **10/12 = 83.3%**; B2: confident-wrong=2 (B-02 and B-09 — both encoding issues)
- **Miss 1 — CA-NOT-B-02** (NOTICE_INVALID missed as NOTICE_VALID; DISAGREE): Encoding GAP. CCP §1161(2): when rent payable in person, notice MUST state "usual days and hours" when landlord is available; omission is fatal. The encoding has name/phone/address but not days_hours_for_in_person_payment. GPT HIGH confident wrong; Gemini correctly flagged UNCERTAIN. B2 severity: medium (split models).
- **Miss 2 — CA-NOT-B-09** (NOTICE_INVALID missed as NOTICE_VALID; AGREE): Encoding ERROR. Unauthorized subletting classified as §1161(4) incurable conduct (unconditional quit). WRONG: per CCP §1161(3), subletting is a curable lease covenant breach; tenant has statutory right to remove subtenant within 3 days. §1161(4) covers nuisance/waste/unlawful use — subletting is NOT listed. Both models HIGH confident wrong. B2 severity: HIGH (both-model AGREE, both HIGH confidence, both wrong). GREEN encoding fix required.
- Encoding fixes queued: (1) Add §1161(2) days_hours_for_in_person_payment to mandatory content; (2) Move unauthorized subletting from §1161(4) to §1161(3) curable category.
- METRICS_LEDGER updated with full B1–B4 analysis, per-item miss triage, and combined v0.2 summary.

**Living docs updated (GREEN)**
- HUMAN_REVIEW_QUEUE: VT-HOLD-CI-01 added (Houle v. Quenneville CI)
- VALIDATION_METRICS_LEDGER: VT run 1153a763 row added; cumulative CI updated (+1 Houle)
- WORK_QUEUE: Gemini blocker removed; scorer moved to NOW; Atwood investigation added
- PROJECT_STATE_OF_RECORD: VT status updated (Houle→CI, Atwood→PR wrong-doc)
- This DAILY_CHANGELOG entry

**GREEN encoding fixes applied to ca_eviction_v2.json — 2026-07-02 (REVISED-8, REVISED-9)**

*Fix 1 — B-02 (REVISED-8): Added `days_hours_for_in_person_payment` to `notice.notice_types.pay_or_quit.mandatory_content`*
- Source anchor: CCP §1161(2) — "if the address at which rent may be paid is set forth in the notice, the notice shall also set forth the usual days and hours that the landlord is available at such address to receive payment"
- Encodes: `required_when: rent_payable_in_person_at_stated_address`, `fatal_if_omitted: true`
- Rationale: Golden-set CA-NOT-B-02 miss confirmed this element was absent from the encoding. GPT HIGH confident wrong; Gemini correctly UNCERTAIN.
- Discipline C: change grounded in retrieved CCP §1161(2) statutory text; source_anchor included in element.

*Fix 2 — B-09 (REVISED-9): Moved unauthorized subletting from §1161(4) unconditional_quit → §1161(3) cure_or_quit*
- Removed from `unconditional_quit.bright_line_qualifying_conduct`: "Unauthorized assignment or subletting of premises contrary to lease covenants"
- Added to `cure_or_quit.bright_line_qualifying_conduct`: "Unauthorized assignment or subletting contrary to lease covenants (CCP §1161(3) — express statutory curable breach; tenant has right to remove subtenant/assignee within 3 court days)"
- Updated `unconditional_quit.description` and `cure_or_quit.description` to reflect corrected classification
- Source anchor: CCP §1161(3) expressly names "covenant not to assign or sublet" as performable within 3 days; CCP §1161(4) enumerated categories (nuisance, waste, unlawful use) do NOT include subletting
- Rationale: B2 HIGH severity — both models AGREE, both HIGH confidence, both wrong. Encoding error, not legal ambiguity.
- Discipline C: change grounded in CCP §1161(3)/(4) statutory text; source_anchor included in both elements.

**B3 regression check COMPLETE — 12/12 = 100.0% (Andy terminal run 2026-07-02)**
- Output: `rules/validation/scorer/output/ca_notice_score_2026-07-02_non-held-out.json` (overwrites pre-fix run)
- **B-02 ✅ FIXED** — NOTICE_INVALID, AGREE. Encoding fix confirmed effective.
- **B-09 ✅ FIXED** — NOTICE_INVALID correct. Run 1: GEMINI-EMPTY (transient). Run 2 (confirmation, 1:22 PM): **AGREE — DUAL-MODEL-CONSENSUS** (agree=12, disagree=0). B-09 transient flag cleared. Full consensus confirmed.
- **newly_failing = 0** — no regressions from REVISED-8 or REVISED-9 changes. All 10 previously-correct items remain correct.
- B2 confident-wrong: 0 (down from 2 pre-fix). B2 HIGH item (B-09 both-wrong) is resolved.
- Rules SHA256: `cc0cfab63ae1591e2b88…` (reflects REVISED-8 + REVISED-9)
- METRICS_LEDGER updated: B3 block added; repeatability view updated; combined v0.2 summary updated to reflect post-fix 12/12 DUAL-MODEL-CONSENSUS (B-09 transient flag cleared by run 2).

### YELLOW — None new.

### RED — None new.

---

## 2026-07-01 (session 8 — v0.2 golden set FROZEN: 17 items, held-out split locked)

### GREEN — Executed autonomously

**Golden set v0.2 FROZEN — Task #23 COMPLETE (GREEN)**

**Drop B-04 (near-duplicate):**
- CA-NOT-B-04 (30-day to 14-month tenant) dropped per Andy's direction — re-tests the same determinate rule as v0.1 CA-NOT-03 (§1946.1(b): tenancy ≥1yr → 60-day required) with only duration varied. Leaves 17 items.

**Freeze 17 items:**
- All 17: Status=FROZEN, ATTORNEY VERDICT=CONFIRMED, Correct outcome = Drafted outcome (Andy confirmed all as-drafted), Reviewed by=Andrew M. Cohen, Date=2026-07-01
- File: `rules/validation/scorer/FROZEN/goldenset_CA_notice_v0.2_20260701.xlsx`
- SHA256: `f65c4240e3ec3c4f7f370d805de906b024e7d3e4f51df92b76197eed1962fa83`
- Scorer validation: 0 YELLOW flags (schema exact match; all KNOWN_OUTCOMES; all FROZEN items complete)

**Held-out split — LOCKED:**
- Method: hybrid — Python `random.sample`, seed=20260701, within leakage-aware pool
- Leakage-aware pool (6 items NOT re-testing any of the 6 self-critique corrections): CA-NOT-B-01, B-02, B-03, B-13, B-14, B-18
- The six corrections: §1946.1(b)/(c) tier+Stancil, SFH two-prong, residential/commercial waiver, day-count/SB 611, §1161(3)/(4) gate, SB 567 relocation
- Draw (5 of 6): CA-NOT-B-01, CA-NOT-B-03, CA-NOT-B-13, CA-NOT-B-14, CA-NOT-B-18 → Held-out=TRUE
- CA-NOT-B-02 (not drawn from pool) → Development=FALSE
- All 11 correction-re-testers (B-05, B-06, B-07, B-08, B-09, B-10, B-11, B-12, B-15, B-16, B-17) → Development=FALSE
- Per protocol rule 4: held-out flags LOCKED — never adjusted after this point

**Leakage guard — CONFIRMED PASSED:**
1. No held-out item is verbatim/near-verbatim of any v0.1 frozen item ✅
2. All 5 held-out items are NOVEL (none re-tests one of the 6 corrections) ✅
3. Held-out set spans outcomes: NOTICE_VALID (B-13, B-18) + NOTICE_INVALID (B-01, B-03, B-14) ✅
4. Held-out set is NOT composed solely of correction re-testers ✅

**VALIDATION_METRICS_LEDGER.md updated (GREEN)**
- v0.2 FROZEN block added with full provenance, SHA256, split, guard confirmation
- Repeatability view row added: v0.2 FROZEN — awaiting dual-model score

**WORK_QUEUE.md updated (GREEN)**
- v0.2 FROZEN gate row ✅ with SHA256 and held-out IDs
- Stage 2 dual-model score gate remains open; NEXT ACTION: Andy runs scorer from terminal once Gemini 503 clears

**SHA256 re-serialization note added (GREEN)**
- Recorded hash `f65c4240…` is the openpyxl at-freeze binary; Excel Desktop re-serializes on open/save → different binary, identical legal content.
- Integrity check should compare canonical fields (ID, Correct outcome, Held-out flag), not binary hash.
- Note added to METRICS_LEDGER v0.2 block and WORK_QUEUE next-action item.

**Small-sample caveat added to all reporting surfaces (GREEN)**
- Held-out n=5: 95% CI is wide (5/5→[47.8%,100%]; 4/5→[28.4%,99.5%]). Result is directional signal, not precision rate.
- Framing: "N of 5 held-out items correct — small-sample result; interpret as directional signal only."
- Caveat added to METRICS_LEDGER (v0.2 block + next-run-target) and WORK_QUEUE.

### YELLOW — None new.

### RED — None new.

---

## 2026-07-01 (session 7 — Golden set v0.2 DRAFT created: 18 candidates, independent source)

### GREEN — Executed autonomously

**Golden set v0.2 DRAFT Excel created — Task #21 + #22 COMPLETE (GREEN)**
- File: `rules/validation/scorer/DRAFT/goldenset_CA_notice_v0.2_DRAFT_20260701.xlsx`
- 18 DRAFT candidates, two-sheet workbook (Candidates + Notes)
- Headers: exact match to `EXPECTED_COLUMNS` in `ca_notice_scorer.py`; scorer will correctly skip all DRAFT rows
- All 18: Status=DRAFT, ATTORNEY VERDICT=blank, Correct outcome=blank, Held-out=blank (Andy fills)

**Independence constraint satisfied:**
- Group A (7 items): sourced from CJER BG 31 (2015 ed.) embedded hypotheticals — §§31.2(7), 31.16, 31.17, 31.20, 31.26(2). IDs: CA-NOT-B-01, B-02, B-03, B-06, B-07, B-08, B-09.
- Group B (11 items): sourced from primary statutory text — CCP §1161 (SB 611 court-day counting), Civ. Code §1946.1(b) (30/60-day), §1946.2(d) (SB 567 relocation), §1946.2(e)(6)/(7)/(8) (exemptions), Stancil v. Superior Court (2021). IDs: CA-NOT-B-04, B-05, B-10 through B-18.
- Zero candidates derived from the rules-writing pass or self-critique pass.

**No v0.1 reuse:** All 18 candidates confirmed distinct from the 16 frozen v0.1 items. CA-NOT-B-04 (30-day to 14-month tenant) tests the same legal rule as CA-NOT-03 but with a different tenancy duration; flagged in the Notes sheet for Andy's review.

**Outcome distribution:** NOTICE_VALID=5 (B-08, B-11, B-13, B-16, B-18), NOTICE_INVALID=12 (B-01 through B-07 excl. B-08, plus B-09, B-12, B-14, B-15, B-17), UD_DEFECTIVE_PREMATURE=1 (B-10).

**WORK_QUEUE.md updated (GREEN)**
- Stage 2 gate v0.2 DRAFT row marked ✅
- "Andy reviews + freezes v0.2" marked as NEXT ACTION FOR ANDY

### YELLOW — None new.

### RED — None new.

---

## 2026-07-01 (session 6 — Stage 2 encoding validation; Lawvable explored; VT retry queued)

### GREEN — Executed autonomously

**Stage 2 non-held-out scorer run — 11/11 = 100% (SM-GPT PARTIAL-CONSENSUS) (GREEN — encoding verified)**
- Andy ran `ca_notice_scorer.py --non-held-out-only` from his terminal after Gemini credits restored.
- Result: 11/11 = 100.0% on non-held-out partition. All 6 pilot gaps closed by self-critique encoding.
- Consensus status: PARTIAL-CONSENSUS (1/11 dual-model). Gemini error: 503 UNAVAILABLE (capacity, not credits). CA-NOT-08 confirmed AGREE — credits working, capacity transient.
- B1 Coverage: 11/11 = 100% known; Accuracy (known): 100%; Overall: 100%.
- B2 Confident-wrong: 0. ZERO.
- B3 Regression check: newly_failing = 0. Prior 7/11 → current 11/11. 4 newly correct: CA-NOT-08, CA-NOT-12, CA-NOT-14, CA-NOT-20.
- B4 Currency: ✅ (self-critique pass this session).
- Run NOT consensus-operative. No held-out burn. Cannot cite as consensus-validated.
- Output: `rules/validation/scorer/output/ca_notice_score_2026-07-01_non-held-out.json`

**VT retry job queued for tonight (GREEN — pipeline re-queue, anti-default rule applied)**
- New job: `rules/validation/queue/job_vt_retry_gemini_restored_20260701.json`
- Prior run (1c7f0772) showed RC=2 with C=FLAG-generate-failed due to Gemini 429. Anti-default rule applied: NOT routed to attorney. Re-queue with credits restored.
- Gemini 503 capacity issue (not credits) means overnight timing improves chances. Will confirm Gemini API status for Stage 2 DUAL-MODEL-CONSENSUS gate.

**Lawvable MCP explored — YELLOW-REG-03 RESOLVED (GREEN — confirmed no relevant skills)**
- Searched `lawvable_search_skills` for "eviction housing tenant landlord notice" + US jurisdiction filter.
- Result: 0 eviction, housing, tenant-landlord, or residential-tenancy skills in Lawvable marketplace.
- 189 total skills; 20 categories; no housing-law or residential-tenancy category.
- US jurisdiction (20 skills): sanctions screening, employment law, customs trade, privacy, CT divorce, trademark. None relevant to CJaC eviction-defense encoding.
- **Conclusion**: Lawvable is a corporate/compliance-oriented marketplace. CJaC is novel territory — no existing skill infrastructure for eviction defense. YELLOW-REG-03 closed.

**VALIDATION_METRICS_LEDGER.md updated (GREEN)**
- Stage 2 v1 row added to CA-notice pilot runs table with full B1-B4 breakdown.
- Miss triage table updated with Stage 2 encoding status for each of the 6 pilot gaps.
- Repeatability view row added.

**WORK_QUEUE.md updated (GREEN)**
- Stage 2 gate table updated: gates 3+credits ✅, encoding validation ✅; DUAL-MODEL-CONSENSUS + v0.2 golden set + held-out score still open.
- Lawvable row → RESOLVED.

### YELLOW — Flagged for Andy

**Gemini 503 UNAVAILABLE (YELLOW — capacity, not credits)**
- 10/11 items returned Gemini 503 despite credits being restored. One item (CA-NOT-08) got through, confirming credits work.
- Not a blocker for tonight's VT retry (overnight low-traffic). If persistent after tonight: may need to downgrade from gemini-2.5-pro to gemini-2.5-flash or adjust retry logic in scorer.
- Stage 2 DUAL-MODEL-CONSENSUS gate remains open until Gemini runs clean.

### RED — None new.

---

## 2026-07-01 (session 5 — Ratification round; 4 FLAGGED → RESOLVED; Stage 2 gate 3 closed)

### GREEN — Executed autonomously

**RESOLVED-1: Stancil any-occupant rule → machine-checkable encoding (GREEN — Andy ratified)**
- `ca_eviction_v2.json`: `termination.tenancy_1yr_plus` now has `condition: "all_occupants_residency_max_years >= 1"` and `stancil_any_occupant_rule.machine_checkable_input: "max_occupant_residency_years"`.
- PLAYBOOK_SPEC §9 `notice_period_termination_no_fault`: conditions updated to use `max_occupant_residency_years` per Stancil; `source_anchor` = "Stancil v. Superior Court (2021) 11 Cal.5th 381; Civ. Code §1946.1(b)".
- Source anchor: Stancil v. Superior Court (2021) 11 Cal.5th 381; Civ. Code §1946.1(b).

**RESOLVED-2: Full AB 1482 exemption matrix — all 8 §1946.2(e) categories encoded (GREEN — Andy ratified)**
- `ca_eviction_v2.json`: `termination.exemptions` expanded from 1 entry (SFH non-entity) to 5 structured entries covering all 8 §1946.2(e) categories:
  - `sfh_non_entity_owner` (§1946.2(e)(8)) — two-prong: owner not REIT/corp/LLC + written exemption notice
  - `sfh_owner_occupied` (§1946.2(e)(5)) — owner occupies ≤2-unit building
  - `owner_occupied_duplex` (§1946.2(e)(6)) — owner-occupied duplex
  - `new_construction_15yr` (§1946.2(e)(7)) — COO within 15 years of notice date, rolling basis
  - `institutional_uses` (§1946.2(e)(1)–(4)) — transient/tourist hotel, institutional, dormitory, shared kitchen/bath with owner
- PLAYBOOK_SPEC §9: New `ab1482_exemption_matrix` element added encoding all 8 categories as machine-checkable conditions; default = AB1482_COVERED.
- Source anchor: Civ. Code §1946.2(e)(1)–(8).

**RESOLVED-3: §1161(3)/(4) bright-line gate encoded (GREEN — Andy ratified)**
- `ca_eviction_v2.json`: `unconditional_quit.bright_line_qualifying_conduct` list defined (physical waste, nuisance per §3482.8/§3485(c)/§3486(c), unlawful use, unauthorized assignment/subletting). `open_textured_conduct` list for ambiguous cases (repeated disturbances, unauthorized smoking, noise complaints).
- `cure_or_quit.bright_line_qualifying_conduct` list defined (failure to maintain premises, unauthorized pet if curable, unauthorized occupant if curable, etc.).
- PLAYBOOK_SPEC §9 interactions: `cure_or_quit_vs_unconditional_quit` gate added — determinate routing for bright-line conduct; open-textured path for ambiguous.
- Source anchor: CCP §1161(3); CCP §1161(4); Civ. Code §§3482.8, 3485(c), 3486(c).

**RESOLVED-4: `missing_just_cause_reason` defect scoped to AB1482-covered units (GREEN — Andy ratified, follow RESOLVED-2)**
- `ca_eviction_v2.json`: `notice_defects.missing_just_cause_reason` updated with `applies_to: "AB1482_covered_units_only"` and `ab1482_coverage_gate` block listing all 8 §1946.2(e) exemption categories. Defect only fires after machine checks that the unit is NOT exempt.
- Source anchor: Civ. Code §1946.2(e)(1)–(8); AB 1482 (Stats. 2019, c. 597).

**`docs/CA_NOTICE_SELF_CRITIQUE_REPORT_20260701.md` — FLAGGED items updated to RESOLVED (GREEN)**
- All 4 FLAGGED items updated to RESOLVED status with Andy ratification date, encoding decisions, and source anchors.
- Stage 2 gate table updated: Gate 3 ✅ CLOSED.

**`docs/WORK_QUEUE.md` updated (GREEN)**
- NOW block updated: 4 FLAGGED → 4 RESOLVED items with status table.
- Stage 2 gate status: Gate 3 ✅ (Andy ratified). Gates 1, 4, 5 remain open (Gemini credits blocker).

### YELLOW — None new this session.

### RED — None new. (Existing RED: Gemini credits. Andy action required to unblock Stage 2 dual-model run.)

---

## 2026-07-01 (session 4 — Self-critique pass + structural addendum; all CA-notice rules revised)

### GREEN — Executed autonomously

**CA-notice self-critique pass complete (GREEN — source-anchored, three disciplines)**
- Produced `docs/CA_NOTICE_SELF_CRITIQUE_REPORT_20260701.md`: 9 REVISED / 3 CONFIRMED / 4 FLAGGED (attorney residual)
- Sources: frozen golden set `goldenset_CA_notice_v0.1` (Part 1 anchor) + WebSearch live retrieval (CCP §1161 SB 611 eff. 2/1/2025 confirmed; CCP §1162 confirmed)

**`rules/eviction/california/ca_eviction_v2.json` — notice section updated (GREEN)**
- REVISED-1: Added `termination.tenancy_1yr_plus` (60d, §1946.1(b)); corrected `tenancy_under_1yr.statute` → §1946.1(c)
- REVISED-2: Added `termination.exemptions[sfh_non_entity_owner]` with two-prong test (§1946.2(e)(8)(A)+(B)); removed incorrect owner-occupancy encoding
- REVISED-3: Added `payee_id_missing` defect (CCP §1161(2); Lynch & Freytag + Eshagian)
- REVISED-4: Added `relocation_assistance_missing` defect (Civ. Code §1946.2(d); SB 567 eff. 4/1/2024)
- REVISED-5: Added `waiver_rules.partial_payment_waiver` with determinate core + open-textured exception; excluded CCP §1161.1 (commercial only per §1161.1(d))
- REVISED-6: Added `unconditional_quit` notice type (CCP §1161(4)); added `wrong_instrument_incurable_conduct` defect
- REVISED-7: Fixed `pay_or_quit.tenancy_under_1yr` and `tenancy_over_1yr` count_method: `calendar_days` → `calendar_days_excluding_weekends_holidays` (CCP §1161 SB 611 eff. 2/1/2025)
- REVISED-8: Filled `improper_service_method.statute` from null → `CCP §1162`
- REVISED-9: Filled `notice_period_too_short.statute` from null → `CCP §1161(2),(3),(4); Civ. Code §1946.1(b),(c)`
- Added `mandatory_content` block to pay_or_quit with payee name/phone/address requirements
- Updated `module_status.notice.status` → `SELF-CRITIQUE-COMPLETE` with report cross-reference
- Updated `per_module_sources.notice` with 15 authorities (was 5)

**`docs/PLAYBOOK_SPEC.md` structural updates (GREEN)**
- §3: Added `source_anchor`, `flagged`, `flagged_reason` fields to element schema
- §9 `notice_period_termination_no_fault`: fixed subsection citations — §1946.1(c) for <1yr, §1946.1(b) for ≥1yr (was citing (b) for both). Added missing DEFECTIVE condition for <1yr. Added `source_anchor`.
- §9 `sfh_ab1482_exemption`: replaced `not_owner_occupied = true` with mandatory two-prong (§1946.2(e)(8)(A)+(B)). Added `source_anchor`.
- §9 `partial_payment_waiver`: restructured from wholly `open_textured` to `determinate` with open-textured exception path. Added `source_anchor`. Tier cap changed A/determinate (core) + B (exception).
- §10: Added SELF-CRITIQUE as standing step 2 in validation workflow (DRAFT → SELF-CRITIQUE → YELLOW/attorney residual → ratification → auto-checks → golden-set → attorney → VALIDATED). Added L1 gate note for `source_anchor`.
- §11 (NEW): Four measurement directives (B1 coverage, B2 confident-wrong, B3 regression, B4 currency) as permanent requirements.

**`CLAUDE.md` — standing disciplines added (GREEN)**
- Added "Self-critique disciplines (STANDING OPERATING RULES)" section: Disciplines A/B/C as permanent session-start rules, not dated directives
- Added "Measurement standards (STANDING)" section: B1-B4 as permanent requirements
- Updated "Last updated" stamp to 2026-07-01

**`docs/COWORK_DIRECTION_A_CADENCE_AUTONOMY.md` — Parts 5–6 added (GREEN)**
- Part 5: Self-critique disciplines (Disciplines A/B/C — permanent)
- Part 6: Measurement directives (B1-B4 — permanent)

**`docs/WORK_QUEUE.md` updated (GREEN)**
- Self-critique pass marked COMPLETE with item-level results table
- 4 FLAGGED items listed for Andy ratification
- Stage 2 gate status updated post-self-critique

### YELLOW — Flagged for Andy ratification

**FLAGGED-1: Stancil "any occupant" nuance (YELLOW)**
- `Stancil v. Superior Court (2021) 11 Cal.5th 381`: 60d requirement attaches once ANY occupant has resided ≥1yr, not just named tenant.
- Question: encode as machine-checkable condition (requiring all occupants' tenancy durations as input) or notes-only treatment?
- Action needed: Andy/attorney call. No encoding change made pending ratification.

**FLAGGED-2: AB 1482 exemptions beyond SFH (YELLOW — scope)**
- §1946.2(e) has multiple exemption categories: new construction (<15yr), condos, luxury housing, ADUs — none encoded.
- Question: does this pass encode SFH-only (current state) or expand to full exemption matrix?
- Action needed: Andy ratifies scope.

**FLAGGED-3: Cure-or-quit / unconditional-quit interaction gate (YELLOW)**
- §1161(3) vs. §1161(4) interaction not encoded as an explicit gate. Propose bright-line enumerated conduct list (waste/nuisance → §1161(4); covenant breach → §1161(3)); ambiguous categories to attorney line.
- Action needed: Andy ratifies approach.

**FLAGGED-4: `missing_just_cause_reason` defect scope (follow-on to FLAGGED-2)**
- Blanket `just_cause_required: true` partially resolved by SFH exemption but other exemptions (FLAGGED-2) leave gaps.
- Action needed: Resolve after FLAGGED-2.

### RED — Escalated to Andy

*(No new REDs this session. Existing REDs unchanged: Gemini credits, Direction B freeze, 6 RC, attorney queue.)*

---

## 2026-07-01 (session 3 — Skills decision; consensus-operative gate; JusticeBench alignment)

### GREEN — Executed autonomously

**Reasoning-engine decision documented (GREEN)**
- ARCHITECTURE.md: Added Section 12 — Claude native legal-reasoning is the CJaC reasoning engine. `legal:*` plugins NOT adopted wholesale (designed for corporate/contract workflows, not eviction-defense encoding). Lawvable MCP to be explored as carry-over task.
- VALIDATED_RESOURCES_REGISTRY.md: `claude_native_legal` updated to PRIMARY reasoning engine (confirmed). `legal_plugin_skills` updated as NOT integrated (by decision). YELLOW-REG-02 resolved.

**Consensus-operative gate implemented in `ca_notice_scorer.py` v2.1 (GREEN pipeline fix)**
- Per Andy direction: a run where either model returns empty is NOT consensus-validated and must be flagged loudly.
- Changes: `consensus_valid: true/false` per item; `_consensus_status()` classifier (DUAL-MODEL-CONSENSUS / SM-GPT / SM-GEMINI / PARTIAL-CONSENSUS / SM-BOTH-ERROR); `⛔` banner in console report when not consensus-operative; `⚠SM` tag on per-item lines; `consensus_status`, `single_model_items`, `consensus_note` in run metadata; `single_model_items` count in summary stats.
- Syntax check: ✅ passes `python3 -m py_compile`
- Note: v1 pilot run (2026-07-01) would have shown SM-GPT banner under this protocol; score was 3/5=60% SM-GPT — correctly labeled PRELIMINARY.

**WORK_QUEUE updated — consensus gate (GREEN)**
- Added hard gate block before Stage 2 scoring: `consensus_status == "DUAL-MODEL-CONSENSUS"` required before any held-out score can be cited. Gate is now explicit and prominent.

**VALIDATED_RESOURCES_REGISTRY.md updated — consensus-operative gate (GREEN)**
- `multi_model_consensus` entry updated with gate definition, history note (GPT has also gone empty on non-notice modules), and Stage 2 blocker note.

### YELLOW — Flagged for Andy ratification

**JusticeBench actor-calibration alignment (YELLOW — architecture note, no action needed)**
- Identified while reviewing JUSTICEBENCH_ALIGNMENT_SPEC.md: Hagan's per-step actor calibration framework (senior human / junior human / deterministic rules-code / small model / frontier model) is the academic parallel to CJaC's `determinate`/`open_textured` strategy tagging.
  - `determinate` ↔ Hagan's "deterministic rules-based code"
  - `open_textured` (bounded reasoning) ↔ Hagan's "intensive frontier model"
- This validates the architectural choice independently. Can cite Hagan's framework as external validation of the playbook architecture's design logic.
- YELLOW because it's an architectural note with potential reporting implications (strengthens the "validated rules layer" thesis for public-facing materials). No immediate action — log in next session context.

### RED — None new this session

---

## 2026-07-01 (session 2 — Playbook Architecture Directive; Stage 1 in progress)

### GREEN — Executed autonomously

**Playbook Architecture Directive saved (GREEN)**
- `docs/CJaC_Playbook_Architecture_Directive_20260701.md` — Andy's July 1 architectural change directive filed to docs/
- Covers: thesis anchor; what stays; playbook-as-unit architecture; bounded-reasoning; Validated Resources Registry; staged execution (Stages 0–4); success metric

**`docs/ARCHITECTURE.md` created (GREEN)**
- Documents one-pipeline playbook architecture: three-tier infrastructure, playbook unit, element decomposition, `determinate`/`open_textured` strategy tags, confidence tiers (A/B/C), known/unknown flag, jurisdiction-resolution, seven-layer validation stack, bucket taxonomy, staged proof sequence, source hierarchy
- Key files table links to PLAYBOOK_SPEC, VALIDATED_RESOURCES_REGISTRY, and directive

**`docs/PLAYBOOK_SPEC.md` created (GREEN)**
- Full playbook unit schema: playbook (top-level), element, strategy tag definitions (`determinate`/`open_textured`), known/unknown, confidence tiers, interaction schema, source IDs, partial CA pay-or-quit example (4 elements: notice_period_nonpayment, notice_period_termination_no_fault, sfh_ab1482_exemption, partial_payment_waiver), validation workflow
- Example encodes 4 of 6 pilot gaps as DRAFT elements

**`docs/VALIDATED_RESOURCES_REGISTRY.md` created (GREEN — seed)**
- 13 sources catalogued: `ca_civil_code_live`, `ca_ccp_live`, `courtlistener_mcp`, `descrybe_mcp`, `legal_data_hunter_mcp`, `ca_benchguide_ud`, `lsnc_eviction_2026`, `justicebench_stanford`, `lsc_temple_dataset`, `claude_native_legal`, `legal_plugin_skills`, `lawvable_mcp`, `multi_model_consensus`
- Each source: tier, currency risk, coverage, limitations, status, use-for notes
- 4 YELLOW flags raised (REG-01 through REG-04)
- Status summary table included

**WORK_QUEUE updated (GREEN)**
- NOW: Stage 1 progress table (4 of 6 items ✅; 2 pending research)
- NEXT: Stage 1 carry-overs (Benchguide research, Lawvable exploration), Stage 2 plan (6 items including element encoding table with revised classification — item 6 is `open_textured`, not purely deterministic)

### YELLOW — Flagged for Andy ratification

**Skills/tools status (YELLOW-REG-02, YELLOW-REG-03)**
- No skills named "legal-analysis" or "issue-spotting" found in environment
- `legal:*` plugin skills (brief, risk-assessment, review-contract, triage-nda) available but NOT integrated into CJaC pipeline
- Lawvable MCP (`lawvable_search_skills`) available but not yet searched for eviction/housing legal skills
- **Andy: direction needed** — integrate `legal:*` skills into playbook element analysis? Explore Lawvable for legal-analysis skills?

**Strategy tag ratification needed for Stage 2 (RED gate)**
- PLAYBOOK_SPEC.md defines `determinate`/`open_textured` tags as set by human attorney at encoding time
- Draft element strategy tags proposed for CA pay-or-quit playbook (4 elements in PLAYBOOK_SPEC example)
- Andy must ratify strategy tags before Stage 2 encoding proceeds

### RED — None new this session

---

## 2026-07-01 (session — CA-notice pilot run complete; architecture memo ingested)

### GREEN — Executed autonomously

**Fixed dotenv path bug in `ca_notice_scorer.py` (GREEN bug fix)**
- `parents[4]` → `parents[3]` in dotenv loader — scorer was looking for `.env` at `GitHub/.env` instead of `a2j-ai/.env`; API keys were never loaded; all API calls returned "missing credentials"
- Fix: single-character change; verified correct path matches `REPO_ROOT` (also `parents[3]`)

**CA-notice pilot live run — first real score (GREEN run; SM-GPT; Gemini 429 depleted)**
- Output: `rules/validation/scorer/output/ca_notice_score_2026-07-01.json`
- SHA256 (golden set): `b87791ecda032fa718df027da47a07774c03eb940354321a3c9d0d77ba0fc7e9`
- SHA256 (rules file): `8cc0b3e51fa57ad211c9976753dd96575401eb47daa54b7759e2bcda1efb4101`
- **Held-out score: 3/5 = 60.0%** ← headline (held-out set now burned)
- Non-held-out score: 7/11 = 63.6%
- Overall (all frozen): 10/16 = 62.5%
- GPT-only run (Gemini 429 RESOURCE_EXHAUSTED on all 16 items — credits depleted)
- Zero YELLOWs (schema clean; all outcome enums recognized)

**Triage of 6 misses — all are rules-gap (not model-wrong):**
- CA-NOT-03 (held-out): 60-day termination notice for tenancies ≥ 1yr not encoded (Civ. Code 1946.1(b))
- CA-NOT-08 (non-held-out): SFH AB 1482 exemption not encoded (1946.2(e)(8)); GPT correctly returned INVALID given encoded rules (missing rule, not wrong reasoning)
- CA-NOT-12 (non-held-out): Payee ID requirement not encoded (CCP 1161(2) mandatory content)
- CA-NOT-14 (non-held-out): Relocation assistance for no-fault termination not encoded (Civ. Code 1946.2(d))
- CA-NOT-16 (held-out): Partial rent acceptance / waiver doctrine not encoded (EDC Associates v. Gutierrez)
- CA-NOT-20 (non-held-out): CCP 1161(4) unconditional quit for incurable conduct not encoded

**4 excluded items logged as downstream work (GREEN)**
- CA-NOT-09 → open-textured queue (utilities-as-"additional-rent" ambiguity)
- CA-NOT-15 → retaliation module golden set (§1942.5 retaliatory eviction)
- CA-NOT-17 → service module golden set (§1161 subtenant-service; §415.46)
- CA-NOT-19 → LA local-overlay golden set (LAMC §151.09 — FMR threshold, bedroom statement, LAHD filing)

**Architecture memo saved to docs/ (GREEN)**
- `docs/CJaC_Architecture_and_Roadmap_Memo_20260701.md` — canonical architecture direction post-pilot
- Section 5 items actioned (see below)

**Section 5 Cowork-actionable items executed (GREEN):**
- Item 1: Jurisdiction-resolution principle added to `docs/Decision_Logic_Briefing_for_Claude.md` (new Section 9)
- Item 2: Benchguide source lane note added to `docs/VALIDATION_METRICS_LEDGER.md` (pending-source-class note)
- Item 3: Direction D logged in WORK_QUEUE HORIZON (3 components; ethical signal-source constraint recorded as non-negotiable)
- Item 4: Reporting scope note added to VALIDATION_METRICS_LEDGER pilot-score section
- Item 5: LA RSO+JCO overlay golden set logged in WORK_QUEUE HORIZON as first local-overlay build

**Living documents updated (GREEN)**
- `docs/VALIDATION_METRICS_LEDGER.md` — Direction B pilot-score section added; repeatability row added; reporting scope note per memo Section 4
- `docs/PROJECT_STATE_OF_RECORD.md` — L4/Direction B status updated to reflect first pilot run
- `docs/WORK_QUEUE.md` — NOW replaced with post-pilot state; 6 rules-gap items added to NEXT; exclusions logged; Direction D + LA overlay in HORIZON
- `docs/CLAUDE_CHAT_BRIEF.md` — Regenerated with first held-out score
- `docs/Decision_Logic_Briefing_for_Claude.md` — Jurisdiction-resolution principle added (Section 9)

### YELLOW — Flagged for Andy ratification

**First held-out score (60.0%) — 6 rules gaps identified (YELLOW)**
- Held-out set is now burned. Score: 3/5 = 60%.
- All 6 misses are rules-gap, not model-wrong. Encoding the 6 missing rules is the direct fix.
- YELLOW: This is an engineering choice (which rules to add first, in what order) with downstream metrics impact. Andy ratify / provide direction before next scorer run.
- Proposed next step: encode all 6 missing rules in `ca_eviction_v2.json`, re-run scorer with fresh golden set (or non-held-out only for iteration), report new score.

**Gemini credits still depleted (YELLOW-carry)**
- Live run confirmed Gemini still 429. Re-run with two-model consensus requires credits restoration.

### RED — Decisions needed from Andy

None new this session (scoring direction is YELLOW, not RED — encoding the missing rules is an engineering task, not a legal-interpretive judgment).

---

## 2026-07-01 (morning report — VT retry Gemini 429 blocker; no metrics movement)

### GREEN — Executed autonomously

**Overnight run 1c7f0772 ingested (VT retry, `job_vt_retry_fresh_20260630`)**
- 2 units: Atwood v. Hill (VT Superior Court 2024, CL cluster 10145325) + Houle v. Quenneville (VT SC 2001, CL cluster 2320677)
- Check A ✅ both cases (text retrieved from CL), Check B ✅ both (no negative treatment)
- Check C ❌ both — Gemini 429 RESOURCE_EXHAUSTED (prepayment credits depleted)
- Harness classified RC; anti-default rule applied — NOT added to HUMAN_REVIEW_QUEUE
- Both cases quarantined for re-queue once Gemini credits restored

**Anti-default rule enforced — 0 cases routed to attorney lane**
- Gemini 429 = API billing infrastructure failure. "Model returned empty" rule applies.
- Cases will be re-queued once credits restored; no attorney review warranted at this time.

**Living documents updated (GREEN)**
- `docs/VALIDATION_METRICS_LEDGER.md` — 2026-07-01 morning report entry added; Gemini 429 blocker noted; cumulative counters unchanged (MV=25, CI=3, RC=6)
- `docs/PROJECT_STATE_OF_RECORD.md` — Last updated stamp + VT retry result logged
- `docs/HUMAN_REVIEW_QUEUE.md` — Header updated (no new items; anti-default rule confirmed)
- `docs/WORK_QUEUE.md` — Gemini credits blocker added to BLOCKED; VT re-queue note in NEXT; "Completed Today" updated
- `docs/DAILY_CHANGELOG.md` — This entry
- `docs/CLAUDE_CHAT_BRIEF.md` — Regenerated (step 3f)

### YELLOW — Flagged for Andy ratification

**None this cycle.**

### RED — Decisions needed from Andy

**Gemini API prepayment credits depleted (RED-strategic)**
- All overnight runs using Gemini are blocked
- Andy must top up at [AI Studio](https://aistudio.google.com/projects) → billing
- Once restored: Cowork will re-queue VT retry same night (fresh=true, both cases have text already retrieved)

---

## 2026-07-01 (session — Direction B scorer harness built; dry-run passed)

### GREEN — Executed autonomously

**`ca_notice_scorer.py` built — Excel-native Direction B scorer (GREEN build)**
- New file: `rules/validation/scorer/ca_notice_scorer.py` (v2.0-excel-native, ~340 lines)
- Reads directly from `goldenset.xlsx` (attorney-reviewed Excel); no JSON intermediary
- Schema validation at load time: checks all 13 expected columns; raises YELLOW on any missing
- Outcome enum: `NOTICE_VALID | NOTICE_INVALID | UD_DEFECTIVE_PREMATURE | UD_NOT_SUSTAINABLE`
- Dual-model pipeline: GPT generates, Gemini verifies; agreement/disagreement tracked per item
- Custom system prompt (scorer-specific — does not reuse l2_runner.py's baked notice-days prompt)
- No answer leakage: model receives only facts + encoded CA-notice rules JSON; correct outcome never included
- Held-out isolation: held-out and non-held-out scores computed and reported separately; no auto-tuning wiring
- Integrity: SHA256 of Excel file + SHA256 of rules file + per-item row hash all logged with every run
- YELLOW surface: schema mismatch, unknown outcome enum, unmapped model output all raise YELLOW with proposed mapping; never silently guesses
- Dry-run mode (`--dry-run`): validates schema, computes hashes, previews queries for first 2 items, mocks all predictions — no API calls needed
- Partitioning flags: `--held-out-only`, `--non-held-out-only`, or run all (default)
- Output: console report + JSON to `rules/validation/scorer/output/`

**Dry-run passed — 13 frozen items, zero YELLOWs (GREEN)**
- All 13 FROZEN items loaded correctly: CA-NOT-01 through CA-NOT-14 (CA-NOT-09 EXCLUDED correctly skipped)
- All DRAFT items (CA-NOT-15-20, CA-SVC-*, TX-NOT-*) silently dropped — correct
- Outcome enum clean: all 4 values (`NOTICE_VALID`, `NOTICE_INVALID`, `UD_DEFECTIVE_PREMATURE`, `UD_NOT_SUSTAINABLE`) present and in known enum
- No schema YELLOWs — all 13 expected columns present
- SHA256 computed: Excel=`3e9550461989c758fb58…`, Rules=`8cc0b3e51fa57ad211c9…`
- Output: `rules/validation/scorer/output/ca_notice_score_2026-07-01_dryrun.json`

**FROZEN/ directory created — provenance copy**
- `rules/validation/scorer/FROZEN/goldenset_CA_notice_v0.1_20260630.xlsx` — SHA256: `3e9550461989c758fb58f0d5159547207e5cd6dd02b4b79bb3eccb8c091ea116`
- This is the reviewed file as of 2026-06-30. Andy will overwrite when final 20-item freeze is complete.

**Note on current frozen set:** All 13 currently frozen items have `Held-out=FALSE`. The held-out score will remain "no held-out items" until Andy sets `Held-out=TRUE` for the selected items in the final 20-item review. The scorer handles this correctly — no code change needed.

### YELLOW — Flagged for Andy ratification

**Scorer `--held-out-only` ready to burn when Andy confirms:**
Once the full 20-item set is frozen and held-out flags are set, running `--held-out-only` permanently burns the held-out score. Andy should confirm readiness before Cowork runs that flag.

---

## 2026-06-30 (session — Task #104 completed; VT job format fix)

### GREEN — Executed autonomously

**VT retry job format fixed — GREEN pipeline correction**
- `rules/validation/queue/job_vt_retry_fresh_20260630.json` had `states`/`fresh`/`sleep` nested under a `config` key — dispatch.py reads those as top-level keys, so the nested format would have caused the job to run with `states=ALL` defaults.
- Fixed: moved `states`, `fresh`, `sleep` to top-level; also set `live_verified: true` so dispatcher picks it up tonight.
- Verified: `python3 -c` check confirms `live_verified=True`, `states='VT'`, `fresh=True`, `job_type='protocol'` — valid per dispatch.py schema.
- VT Houle retry will fire at 2:15 AM 2026-07-01.

**Task #104 confirmed complete**
- All 3 run outputs (VT perm-fail, CO/NY/SC PR retry, 10-state broad query) ingested by morning report.
- 8 state v2 files updated (AL, CT, HI, LA, ND, NM, WV, CO). WV Criss → HUMAN_REVIEW_QUEUE [WV-RET-HOLD-RC-02].
- METRICS_LEDGER confirmed current: 25 MV cumulative, 3 CI, 6 RC.

---

## 2026-06-30 (morning report — 3 overnight runs completed; 8 state files updated)

### GREEN — Executed autonomously

**Overnight runs scanned — 3 jobs completed**
- `job_vt_houle_retry_20260629.json` → done/. VT: perm-fail. Root cause: `fresh=false` reads v1 draft file; Houle in v2 file → `__no_cases__`. GREEN pipeline bug. Re-queued with `fresh=true` (see below).
- `job_pr_retry_co_ny_sc_20260629.json` → done/. 14 units (CO×5, NY×8, SC×1 perm-fail). Buckets: MV=3 (CO×1, NY×2), CI=1 (NY), PR=8. Method rate: 75%. Overall rate: 23%. NY MV cases (339-347 E. 12th St. LLC v. Ling, MH Residential 1 LLC v. Barrett) already ingested in ny_eviction_v2.json from Track B — no file conflict.
- `job_broad_query_10states_20260629.json` → done/. 35 units (AL,CT,HI,KS,LA,ND,NM,NV,OK,WV). Buckets: MV=12, CI=1 (NM Casa Blanca), RC=1 (WV Criss), PR=20, KS perm-fail. Method rate: 85.7% (12/14). Overall rate: 34.3% (12/35). Krippendorff's α_method ≈ 0.470 (n=18 combined text-retrievable, all runs this cycle).

**8 state v2 files updated — retaliation holdings (GREEN file update)**
- `rules/eviction/alabama/al_eviction_v2.json` — 2 MV (Leeth, Tiller[YELLOW]). 1 YELLOW flag (Tiller: adverse outcome).
- `rules/eviction/connecticut/ct_eviction_v2.json` — 3 MV (Holdmeyer, Correa, Presidential Village[YELLOW]). 1 YELLOW flag (Presidential Village: quote quality).
- `rules/eviction/hawaii/hi_eviction_v2.json` — 2 MV (Windward Partners, Cedillos[YELLOW]). 1 YELLOW flag (Cedillos: scope uncertain).
- `rules/eviction/louisiana/la_eviction_v2.json` — 2 MV (Capone[YELLOW], Taylor v. Joseph[YELLOW]). 2 YELLOW flags (Capone: adverse outcome; Taylor: no reporter + not appealed + local ordinance).
- `rules/eviction/north-dakota/nd_eviction_v2.json` — 1 MV (Nelson v. Johnson[YELLOW]). 1 YELLOW flag (Nelson: procedural-only, no merits).
- `rules/eviction/new-mexico/nm_eviction_v2.json` — 1 MV (Rickert[YELLOW]) + 1 CI (Casa Blanca). 1 YELLOW flag (Rickert: adverse outcome + single-model).
- `rules/eviction/west-virginia/wv_eviction_v2.json` — 1 MV (Murphy v. Smallridge). 1 RC note flag (Criss: RC-pending-attorney, in HUMAN_REVIEW_QUEUE).
- `rules/eviction/colorado/co_eviction_v2.json` — 1 MV (W.W.G. Corp.[YELLOW]). 1 YELLOW flag (W.W.G.: court declined to decide if doctrine exists in CO).
- All 8 files: validation_status → L2-HOLDINGS-V3-RUN-COMPLETE; last_run → 2026-06-30. All cases remain below attorney line.

**VT retry re-queued — GREEN pipeline fix**
- Root cause: `fresh=false` + Houle in v2 file → `load_draft_cases()` returns nothing → perm-fail.
- Fix: new job `rules/validation/queue/job_vt_retry_fresh_20260630.json` with `fresh=true`. CL broad fallback should retrieve Houle v. Quenneville (cluster_id=2320677).
- Queued for tonight (2026-07-01 at 2:15 AM).

**HUMAN_REVIEW_QUEUE updated**
- Added [WV-RET-HOLD-RC-02]: Criss v. Salvation Army Residences (319 S.E.2d 403, WV SC 1984). RC: FLAG-verify-disputed. Anti-default satisfied: full CL-retrieval + generate + verify ran. Murphy v. Smallridge (MV) cites Criss as first WV retaliation case. RC count: 5 → 6.

**All living docs updated (GREEN)**
- VALIDATION_METRICS_LEDGER.md — 3 new run entries (VT retry, CO/NY/SC retry, broad_query_10states).
- PROJECT_STATE_OF_RECORD.md — holdings v3 status updated; MV cumulative now 28.
- HUMAN_REVIEW_QUEUE.md — WV-RET-HOLD-RC-02 added; header/summary updated.
- WORK_QUEUE.md — NOW cleared (3 done jobs + VT pipeline fix); NEXT updated; VT re-queued.
- DAILY_CHANGELOG.md — this entry.
- CLAUDE_CHAT_BRIEF.md — regenerated (Step 3f).

### YELLOW — Flagged for Andy ratification

**CO W.W.G. Corp. v. Hughes (960 P.2d 720, Colo. Ct. App. 1998) — MV classification with significant caveat:**
Court reversed trial court's retaliation finding WITHOUT deciding whether the doctrine exists in Colorado. Case is adverse precedent AND does not establish the defense. Flag written to co_eviction_v2.json. Andy: should CO remain "doctrine existence uncertain" pending a case that affirmatively establishes it?

**NY CO/NY/SC retry — new MV cases already in file:**
339-347 E. 12th St. LLC v. Ling and MH Residential 1 LLC v. Barrett were already in ny_eviction_v2.json from Track B run. Baer v. Huggins (CI) also already in file. The CO/NY/SC retry confirmed the Track B ingestion was correct; no file changes needed for NY this cycle.

**KS/SC/NV — CL coverage gap confirmed:**
Broad fallback also returned 0 for KS. KS, SC, NV have no CL-indexed retaliation defense cases. Next options: (a) Descrybe MCP case lookup (GREEN autonomous if Andy approves); (b) Accept Track A ceiling for these 3 states. **Andy: direction needed.**

**YELLOW items carried from prior cycles (pending Andy ratification):**
- Cross-jurisdiction rejection (Markese/Robinson) — ratify or redirect.
- GA notice file change [NOTICE-L2-06] — ratify or override.
- Graham Court v. Taylor (115 A.D.3d 50) MV-with-caution — noted for NY review.

### RED — None new this cycle

All RED items carried from prior cycles in HUMAN_REVIEW_QUEUE.

---

## 2026-06-29 (morning report — overnight queue empty; no new runs)

### GREEN — Executed autonomously

**Overnight scan — queue empty, no runs**
- Dispatcher log (`launchd_stdout.log`, 2026-06-29 09:29) confirms: "Queue is empty or no eligible jobs — nothing to do." (fired twice, both idle).
- No new l2/output files since 2026-06-27 19:24 UTC. No new SUMMARY files.
- All output from last cycle (Batch 4 NC) was already ingested in 2026-06-28 morning report.

**Living docs updated (all GREEN — date/state pass)**
- `docs/WORK_QUEUE.md` — "Last updated" advanced to 2026-06-29; NOW section confirmed empty; NEXT queue unchanged (8 items).
- `docs/VALIDATION_METRICS_LEDGER.md` — No new run entry (no overnight run). Carry-forward note appended.
- `docs/PROJECT_STATE_OF_RECORD.md` — No new validation results. State unchanged.
- `docs/HUMAN_REVIEW_QUEUE.md` — No new items this cycle. Existing queue unchanged.
- `docs/CLAUDE_CHAT_BRIEF.md` — Regenerated (Step 3f). Timestamp advanced to 2026-06-29.

### YELLOW — None this cycle (carried from prior cycle)

**Carried YELLOWs awaiting Andy ratification (no new ones this cycle):**
- Cross-jurisdiction rejection (Markese/Robinson) — ratify or redirect
- VT Houle retry — queue or hold
- GA notice file change [NOTICE-L2-06] — ratify or override
- Graham Court v. Taylor (115 A.D.3d 50) MV-with-caution flag — noted for Andy's NY review

### RED — None new this cycle

All RED items carried from prior cycles (see HUMAN_REVIEW_QUEUE and the RED list in CLAUDE_CHAT_BRIEF).

---

## 2026-06-29 (session 2 — Check E + broad fallback built; 3 jobs queued)

### GREEN — Executed autonomously

**Check E jurisdiction filter + broad CL fallback — built and verified (Andy ratified 2026-06-29)**
- File modified: `rules/validation/l2/retaliation_holdings_v3_runner.py`
- Added `_court_matches_state(court_name, state_abbr)`: checks if CL-returned court name contains the target state's full name. Conservative: federal circuit courts (no state name) are rejected by default.
- Added `_build_case_from_hit(hit)`: extracted helper to avoid code duplication.
- Refactored `cl_search_retaliation_by_state()`: now uses `_run_search()` inner function that applies `_court_matches_state()` to every CL hit before accepting it. Logs rejected wrong-jurisdiction hits.
- Broad fallback: if statute-targeted query returns 0 in-state results, runner automatically tries `retaliatory eviction {state_name} landlord tenant`; same Check E filter applied. Cases from broad fallback tagged `_source: "cl_fresh_search_broad_fallback"`.
- Syntax check: import OK. Protocol adapter import OK (no API calls required for check).
- Unit tests (inline): 10 court-matching scenarios, all pass (AK court rejected for AL, CT court accepted for CT, NJ federal district accepted for NJ, D.C. Circuit rejected for NJ, etc.).

**3 batch jobs queued (dispatch order: tonight → tomorrow → night after)**
- **Tonight (oldest):** `job_pr_retry_co_ny_sc_20260629.json` — CO/NY/SC, sleep=30, fresh=true. Already queued before runner update; will use updated runner (fresh CL search path).
- **Tomorrow night:** `job_broad_query_10states_20260629.json` — AL/CT/HI/KS/LA/ND/NM/NV/OK/WV, sleep=20, fresh=true. First run with broad fallback + Check E.
- **Night after:** `job_vt_houle_retry_20260629.json` — VT only, sleep=20, fresh=false. Houle v. Quenneville (cluster_id=2320677); Andy approved.

**DAILY_CHANGELOG and WORK_QUEUE updated** (this entry).

### YELLOW — Ratified this session (now GREEN-executed)

- **Check E jurisdiction filter:** YELLOW from 2026-06-28 → ratified by Andy 2026-06-29 → implemented.
- **Broad CL fallback query for 10 no-results states:** YELLOW from 2026-06-29 → ratified by Andy 2026-06-29 → implemented.
- **VT Houle retry:** YELLOW from 2026-06-28 → ratified by Andy 2026-06-29 → job queued.

### RED — None this session

---

## 2026-06-29 (session — PR retry v2 queued; no-candidates diagnosis; WORK_QUEUE updated)

### GREEN — Executed autonomously

**PR retry v2 job built and queued for tonight**
- File: `rules/validation/queue/job_pr_retry_co_ny_sc_20260629.json`
- States: CO (3 transient cases), NY (7 transient cases), SC (4 transient cases)
- All three states had real CL 429 transient failures in nc17_fresh_v2 and were NOT covered by Batch 4 (Batch 4 covered AL, CT, HI, LA, MI, ND, NJ, NM, OK, VT, WV).
- `sleep=30` (doubled from 15) to reduce 429 rate.
- Post-run: manual jurisdiction review required (wrong-jurisdiction contamination risk; same pattern as NJ/MI in Batch 4).
- NY note: Track B cases (Wheeler, Pena, 339-347, MH Residential, Graham Court/Taylor) already ingested as MV this session. Any new MV from tonight's run would be CL-search-found cases, not the Track B set.

**`__no_cases__` root-cause diagnosis — corrected understanding**
- Prior session characterization: "fresh=true was a no-op / no-candidates bug." Updated: `cl_search_retaliation_by_state()` IS being called via the `fresh=True` path for AL, CT, HI, KS, LA, ND, NM, NV, OK, WV.
- Root cause: CL free-tier search returns 0 results for those states' statute-targeted queries. Examples: WV `37-6A-1`, OK `41-120`, ND `47-16-17.5` — no indexed precedential opinions found.
- This is a **data coverage gap** (CL free tier), NOT a code bug. A fallback to a broader state-name query might find cases but would increase wrong-jurisdiction contamination risk.
- Documented in WORK_QUEUE NEXT #2 (revised). No code change today — this is YELLOW; flagging for Andy's direction on query strategy vs. Track A for these 8 states.

**WORK_QUEUE.md and DAILY_CHANGELOG.md updated** (this entry).

### YELLOW — Flagged for Andy ratification

**Broader CL query fallback (previously mislabeled as code bug):**
- For AL, CT, HI, LA, ND, NM, OK, WV: statute-targeted CL queries return 0 results. A broader query (state name + "retaliatory eviction" + "landlord tenant") would likely find cases but introduces same wrong-jurisdiction risk as Batch 4 MI (non-state cases passing the 4-check protocol).
- Options: (a) Add broad fallback query + jurisdiction filter (YELLOW — runner change); (b) Research these states via Justia/Scholar as Track B candidates; (c) Accept Track A for all 8.
- **Andy: direction on how to handle these 8 states (Track A / Justia research / improved CL query)?**

**Cross-jurisdiction fix (carried from 2026-06-28):** NEXT #1. Runner court-filter still needed. Not implemented today.

**VT Houle retry (carried from 2026-06-28):** Still awaiting Andy's go-ahead.

### RED — None this session

---

## 2026-06-28 (morning report — Batch 4 NC ingested; cross-jurisdiction bug flagged)

### GREEN — Executed autonomously

**Batch 4 NC states (fresh_nc_batch4_20260627) — ingested**
- Run completed 2026-06-27 19:24 UTC (21.4 min). States: AL, CT, HI, LA, MI, ND, NJ, NM, OK, VT, WV. 22 units.
- Harness-reported: MV=3, PR=11, perm-fail=8, SM=0. Method rate: 100%. Overall rate: 14%.
- Corrected MV (after cross-jurisdiction audit): 1 (Onderdonk only). 2 harness-MV rejected.
- perm-fail (8 states): AL, CT, HI, LA, ND, NM, OK, WV — genuinely no CL candidates under fresh=true statute-targeted search.
- VT: Atwood v. Hill (wrong-doc PR), Houle v. Quenneville (CL 429 transient-failure, reclassified PR — retry candidate).
- All source JSON archived at: `rules/validation/l2/output/retaliation_holdings_v3_2026-06-27_fresh_nc_batch4_20260627.json`.

**nj_eviction_v2.json updated (GREEN)**
- `holdings.machine_verified_cases`: Onderdonk v. Presbyterian Homes of NJ (85 N.J. 171, NJ SC 1981) added.
- `holdings.rejected_cross_jurisdiction`: Markese v. Cooper (NY County Courts, not NJ) and Lena Robinson v. Diamond Housing Corp. (D.C. Circuit, not NJ) written with rejection reason.
- `holdings.pr_cases`: Scofield v. Berman & Sons (MA case, wrong-doc).
- `holdings.validation_status`: BATCH4-MV-PARTIAL.

**VALIDATION_METRICS_LEDGER.md updated**
- New run entry: Batch 4 NC states (fresh_nc_batch4_20260627), full metric table with YELLOW cross-jurisdiction flag.
- Cross-batch summary table updated: Batch 4 row added, cumulative MV corrected to 16.

**PROJECT_STATE_OF_RECORD.md updated**
- Holdings v3 section: Batch 4 results added; cross-jurisdiction pipeline bug noted; cumulative MV updated to 16 (10 CA + 5 NY + 1 NJ).
- Last-updated header updated.

**WORK_QUEUE.md updated**
- NOW: Batch 4 moved to Completed; queue empty tonight; VT Houle retry proposed as YELLOW for Andy approval.
- NEXT: cross-jurisdiction runner fix (#1, YELLOW) + VT Houle retry (#2, YELLOW) added ahead of existing items.

**CLAUDE_CHAT_BRIEF.md regenerated** (Step 3f — see below).

### YELLOW — Flagged for Andy ratification

**Cross-jurisdiction contamination in Batch 4 harness MV bucket:**
- Runner accepted 2 non-NJ cases as NJ MV (Markese=NY County Courts, Robinson=DC Circuit). Root cause: CL statute-targeted query for NJ Anti-Reprisal Act returned cases from other jurisdictions that discuss the same statutory framework. Same pattern explains all 8 MI PR cases (non-MI cases returned for MI statute query).
- **Corrective action taken:** Markese and Robinson rejected from nj_eviction_v2.json; written to `rejected_cross_jurisdiction` with reason. No file-level validation status impact (NJ remains BATCH4-MV-PARTIAL).
- **Fix needed:** Add court-jurisdiction filter to runner's CL results (YELLOW — changes runner behavior). Proposal in WORK_QUEUE NEXT #1.
- **Andy: ratify the rejection of Markese/Robinson and the proposed jurisdiction filter fix, or redirect.**

**VT Houle retry proposal:**
- Houle v. Quenneville (cluster_id=2320677) is a known valid candidate; transient-failure from CL 429 in Batch 4. A single-state VT fresh=true job would likely succeed. Proposed — not queued pending Andy's go-ahead (YELLOW).

### RED — None this cycle

---

## 2026-06-27 (session continuation 3 — Batch 4 NC job queued; golden-set scorer harness built)

### GREEN — Executed autonomously

**Batch 4 NC states job queued for tonight**
- File: `rules/validation/queue/job_fresh_nc_batch4_20260627.json`
- States: AL, CT, HI, LA, MI, ND, NJ, NM, OK, VT, WV (11 states — all with zero MV/CI results to date)
- Excludes: NY (Track B complete), KS/NV/SC (Track B confirmed NC), AK (RC already attorney-routed)
- fresh=true, statute-targeted CL queries, sleep=15s, live_verified=true
- Will run tonight 2:15 AM via launchd dispatcher. Est. 8–14 hours.

**Golden-set scorer harness built (Direction B)**
- `rules/validation/scorer/golden_set_scorer.py` — end-to-end scorer. Runs DRAFT or FROZEN golden-set fact patterns through the pipeline (rules file + GPT-4o + Gemini), compares to correct_answer, scores by difficulty band (bright_line / open_textured — never blended). SHA256 integrity check for frozen candidates. Read-only to ground truth. Writes output to `scorer/output/score_<run_id>.json`.
- `rules/validation/scorer/freeze.py` — freeze utility for Andy to run interactively. Prompts for FREEZE/EDIT/SKIP per candidate, computes SHA256 content hash, proposes 70/30 train/held-out split, writes to `golden_sets/FROZEN/<module>/`. Seals held-out partition at freeze time.
- Syntax validated: both files parse clean.
- Ready to use the moment Andy freezes first CA notice candidates.

**WORK_QUEUE updated** — NOW section now shows Batch 4 NC job; scorer build reflected in NEXT; last_updated timestamp.

### YELLOW — none this cycle

---

## 2026-06-27 (session continuation 2 — Task #96 completed: ny_eviction_v2.json updated with Track B NY cases)

### GREEN — Executed autonomously

**ny_eviction_v2.json updated — Track B NY cases added to candidates[]**
- Prior session claimed this was done; actual file had not been updated (candidates[] still had only 2 track-a-model-suggested entries). Completed now.
- Added 7 Track B cases to `holdings.candidates[]` in `rules/eviction/new-york/ny_eviction_v2.json`:
  - **MV ×5:** Wheeler v. D'Antonio (2025 NY Slip Op 25196), Pena v. Lockenwitz (53 Misc. 3d 428), 339-347 E. 12th St. LLC v. Ling (35 Misc. 3d 30), MH Residential 1 v. Barrett (41 Misc. 3d 24), Graham Court v. Taylor (115 A.D.3d 50, attorney-verify-recommended)
  - **CI ×1:** Baer v. Huggins (41 Misc. 3d 605) — D=INFERRED, cheap confirm lane [NY-HOLD-CI-01]
  - **PR ×1:** Graham Court v. Kyle Taylor (24 N.Y.3d 742) — wrong-doc, not attorney lane
- Each case carries: cl_cluster_id, cl_url, controlling_quote (where available), check_d_control, bucket, run_id, disposition_note.
- `validation_flags`: TRACK-B-NY-MV-CASES-INGESTED added.
- Total candidates[]: 9 (2 track-a-model-suggested + 5 MV + 1 CI + 1 PR).
- Verification: `python3 -c "..."` confirmed 9 unique candidates by cl_cluster_id/case_name, no duplicates.

---

## 2026-06-27 (session continuation — Batch 3 ingested; NJ retry resolved; PR retry enabled; Track B queued)

### GREEN — Executed autonomously

**Batch 3 (7e6fcf6d) ingested into VALIDATION_METRICS_LEDGER.md**
- Run date: 2026-06-25. 18 states (AK, AL, CA, CO, CT, HI, KS, LA, MI, ND, NJ, NM, NV, NY, OK, SC, VT, WV). 23 units.
- Bucket results: MV=4 (CA: S. P. Growers Assn., Barela, Drouet, Aweeka), CI=2 (CA: Schweiger, Western Land Office), RC=0, PR=0 (429s transient — recovered), NC=17 (non-CA states: `__no_cases__` in v2 files, `fresh=false` → no CL retrieval attempted).
- Method rate: 66.7% (4/6 text-retrievable CA cases). Overall rate: 17.4% (4/23, diluted by 17 NC states).
- NC=17 is NOT a retrieval failure — no candidates existed in those files at the time of the run. NOT attorney lane. Addressed by Track A (statute-direct) and Track B (CL fresh run) pipeline.
- METRICS_LEDGER: detailed section + cross-batch table row added. Repeatability view: no new row added (holdings v3 is cross-batch; detailed cross-batch table is the canonical record).

**NJ failure_to_attach retry — CONSENSUS-IMPROVE; file auto-updated**
- Run: `nj_attach_retry_20260626.py` (reformulated GPT retry with 120s timeout + consequence-framing query). Run date: 2026-06-27.
- Output: `rules/validation/l2/output/nj_attach_retry_20260626.json`.
- Both models returned content: GPT confidence=medium; Gemini confidence=high. Both agreed: N.J. Ct. R. 6:3-4(c).
- Classified: CONSENSUS-IMPROVE — more specific than stale "NJSA 2A:18-51 et seq. (pleading requirements)".
- File updated automatically: `rules/eviction/new-jersey/nj_eviction_v2.json` → `statute: "N.J. Ct. R. 6:3-4(c)"`, `validation_flags: ["L2-PROCEDURAL-CONFIRMED"]`, `l2_note: "[RETRY 2026-06-26] CONSENSUS-IMPROVE: N.J. Ct. R. 6:3-4(c)"`.
- Resolves 4-run persistent ERROR streak. NJ failure_to_attach: CLOSED as L2-PROCEDURAL-CONFIRMED.
- Anti-default audit: GPT had timed out on 3 prior runs (60s limit). Fix was 120s timeout + reformulated query — a pipeline fix, not attorney escalation. Anti-default rule satisfied.

**Track B CL verification job created for KS/NV/NY/SC**
- File: `rules/validation/queue/job_track_b_ks_nv_ny_sc_20260627.json`
- Targets KS, NV, NY, SC with `fresh=true` (CL fresh opinion search + generate-from-source verification).
- Candidates confirmed in all 4 v2 files:
  - KS: Stephens v. Ludy, 42 Kan. App. 2d 531, 214 P.3d 718 (2009) [track-a-model-suggested, Gemini; cl_cluster_id=null]
  - NV: Anvui, LLC v. G.L., 133 Nev. 711, 405 P.3d 667 (2017 Nev. SC) [track-a-model-suggested, Gemini; cl_cluster_id=null]
  - NY: Domen Holding Co. v. Aranovich, 1 N.Y.3d 117 (2003 NY CoA) [GPT] + 601 West 160th St. Corp. v. Henry (App. Term 2001) [Gemini]
  - SC: Wadell v. U.S. Bank Nat'l Ass'n, 399 S.C. 541, 732 S.E.2d 523 (Ct. App. 2012) [track-a-model-suggested, Gemini; cl_cluster_id=null]
- sleep=15s (CL rate-limit management). `live_verified: true` (job ready for dispatcher).
- Note: KS/NV/SC candidates are single-model-suggested (Gemini only). CL retrieval may fail to find these cases if cluster IDs are unknown. Outcome: MV if retrieved + corroborated; PR if CL can't retrieve; SM if only one model returns holding.

**Queue hygiene — nj_attach_probe + notice_tiebreaker copied to done/**
- Both jobs already had `live_verified: false` (dispatcher skips them — no re-run risk).
- Copied to `rules/validation/done/` as completed records. Originals remain in `queue/` (deletion requires Terminal — sandbox cannot delete macOS-mounted files).
- Action for Andy: `rm rules/validation/queue/job_nj_attach_probe_20260626.json rules/validation/queue/job_notice_tiebreaker_20260626.json` from Terminal when convenient. No urgency — dispatcher ignores them.

### YELLOW — Logged for ratification

**PR retry job enabled (live_verified: false → true)**
- File: `rules/validation/queue/job_retaliation_pr_retry_20260626.json`
- Change: `live_verified: false` → `live_verified: true`.
- Basis: Andy authorized with "do 2-6" (item 4 = enable PR retry). YELLOW because this queues a 13+ hour CL run.
- Job targets 14 states (AL, CO, CT, HI, LA, MI, ND, NJ, NM, NY, OK, SC, VT, WV): 82 transient-failure PR-class cases from nc17_fresh_v2. sleep=15s.
- Will run tonight at 2:15 AM via launchd dispatcher (or first night dispatcher picks it, after Track B job — check ordering by creation timestamp).
- Risk: CL rate limits may still produce 429s. Harness now correctly writes `bucket: "PR"` for these. If run fails badly, move job back to queue/ with `live_verified: false` and retry with longer sleep.
- Dispatcher ordering: sorts queue by mtime ascending (oldest first). PR retry mtime=Jun 26 22:29 UTC; Track B mtime=Jun 27 00:50 UTC. **PR retry runs tonight (2026-06-27 at 2:15 AM); Track B runs the following night.** PR retry est. ~13 hours; Track B (4 states, fresh=true) est. ~2-4 hours.

---

## 2026-06-27 (morning report — PR retry + Track B overnight runs ingested)

### GREEN — Executed autonomously

**PR retry run ingested — pipeline failure diagnosed**
- Run: `pr_retry_20260626` (fired 2026-06-27 ~01:00 UTC via launchd). Output: `rules/validation/l2/output/retaliation_holdings_v3_2026-06-27_pr_retry_20260626.json`.
- Result: 14 states, ALL perm-fail. MV=CI=RC=PR=SM=0. No CL calls made.
- Root cause: `fresh=false` + `load_draft_cases()` reads v1 draft file only; 82 transient-failure cases from nc17_fresh_v2 were never persisted to v1 draft file. All 14 states returned `__no_cases__`.
- Classified: GREEN pipeline bug. 82 cases remain unretried.
- Anti-default audit: PR retry returned 0 cases. This is an infrastructure failure (bad job config) — not attorney escalation. Fix needed: new runner that reads from nc17_fresh_v2 output JSON, or re-queue with `fresh=true`.
- METRICS_LEDGER: PR retry entry added (method_rate=n/a, overall_rate=0%, perm-fail=14).

**Track B run (KS/NV/NY/SC) ingested — NY success; KS/NV/SC CL gap confirmed**
- Run: `track_b_ks_nv_ny_sc_20260627` (fired 2026-06-27 ~09:15 UTC via launchd). Output: `rules/validation/l2/output/retaliation_holdings_v3_2026-06-27_track_b_ks_nv_ny_sc_20260627.json`. Elapsed: 433s (~7.2 min).
- NY: 8 CL candidates found. MV=5, CI=1, PR=1. Method rate: 83.3% (5/6). NY Track B: COMPLETE.
- KS, NV, SC: 0 CL candidates. All perm-fail. Track A candidates (Stephens, Anvui, Wadell) not indexed in CL.
- overall_rate: 45.5% (5/11, diluted by 3 perm-fail + 1 PR).
- METRICS_LEDGER: Track B entry added with full bucket breakdown.

**ny_eviction_v2.json updated with Track B results**
- File: `rules/eviction/new-york/ny_eviction_v2.json`. Updated via Python script.
- Added `holdings.track_b_run` block, `machine_verified_cases` array (5 MV cases), `confirm_inference_cases` array (Baer v. Huggins CI), `pr_cases` array (Graham Court v. Kyle Taylor PR).
- `validation_status`: TRACK-A-PENDING → TRACK-B-RUN-COMPLETE.
- `validation_flags`: TRACK-B-RUN-COMPLETE added.
- `last_updated`: 2026-06-27.

**HUMAN_REVIEW_QUEUE updated — NY-HOLD-CI-01 added**
- Item: [NY-HOLD-CI-01] Baer v. Huggins, 41 Misc. 3d 605 (N.Y. Civ. Ct. 2013). CI cheap confirm lane.
- D=INFERRED: both models corroborated holding from retrieved text, but no directly quotable sentence. Attorney to confirm case is substantive, not citation-drop.

**VALIDATION_METRICS_LEDGER updated — two new entries + cross-batch table row**
- PR retry entry added under holdings v3 section.
- Track B entry added with full breakdown (KS/NV/SC perm-fail, NY bucket detail, method/overall rates).
- Cross-batch combined table updated with both new rows.

**Living docs updated (WORK_QUEUE, PROJECT_STATE_OF_RECORD, DAILY_CHANGELOG)**
- WORK_QUEUE: NOW updated (no jobs queued tonight); NEXT refreshed (PR retry v2, KS/NV/SC path decision, Baer confirm, Direction B); Completed Today updated.
- PROJECT_STATE_OF_RECORD: holdings v3 section updated with PR retry + Track B results; last_updated updated.
- DAILY_CHANGELOG: this entry.

**CLAUDE_CHAT_BRIEF.md regenerated (final step)**
- Updated to reflect 2026-06-27 morning report cycle.

### YELLOW — Logged for ratification

**Graham Court v. Taylor (115 A.D.3d 50) — MV classification with caution flag**
- Classified MV by runner (both models cited same citation + corroborated holding). But model summary notes court "does not discuss the substantive merits of retaliatory eviction" — outcome-only affirmance, no rule articulated.
- Logged in ny_eviction_v2.json `validation_flags` and `machine_verified_cases[4].note`.
- Andy should review when examining NY holdings: this case may not usefully state a controlling holding.

---

## 2026-06-26 (session continuation — pipeline prep + Track A runner)

### GREEN — Executed autonomously

**harness.py: `bucket: "PR"` added for transient-failure dispositions**
- Bug: the `except TransientError` block in `harness.py` wrote `disposition="transient-failure"` results with no `bucket` key, making 82 nc17_fresh_v2 cases invisible to bucket-based reporting.
- Fix: added `"bucket": "PR"` to the transient-failure result dict with comment: "PR-class: infrastructure failure, not verification failure."
- Next run will correctly classify transient-failure cases as PR. Historical nc17_fresh_v2 output file unchanged (bucket gap was pre-fix).

**`nj_attach_retry_20260626.py` — NJ failure_to_attach reformulated retry runner built**
- GPT timeout increased to 120s (prior runs failed at 60s default).
- Gemini uses consequence-framing query (worked best in probe P3 — all 3 probes got Gemini content).
- Auto-classifies: CONSENSUS-IMPROVE / CONFIRM / NO-SPECIFIC-RULE / MODEL-SPLIT / SM-GEMINI / SM-GPT / ERROR.
- If CONSENSUS-IMPROVE: updates `nj_eviction_v2.json` failure_to_attach item; removes stale L2-PROCEDURAL-ERROR flag.
- Output: `rules/validation/l2/output/nj_attach_retry_20260626.json`
- **Status: ready for Andy to run from Terminal. Cowork ingests output.**

**`l2_procedural_defects_runner.py`: `--output-suffix` arg added** *(YELLOW — see below)*

**`job_retaliation_pr_retry_20260626.json` — PR retry job queued at `live_verified=false`**
- Targets 14 states (AL, CO, CT, HI, LA, MI, ND, NJ, NM, NY, OK, SC, VT, WV): 82 PR-class transient-failure cases from nc17_fresh_v2.
- `live_verified: false` — intentional. BLOCKED on Andy's call on CL timing.
- sleep=15s (increased from 10s — 429 severity in prior 13.3-hour run).

**`retaliation_holdings_v3_runner.py`: statute-targeted CL search queries**
- Added `_STATE_RETALIATION_STATUTES` dict (51 states → statute citation).
- `cl_search_retaliation_by_state()` now uses `"{statute} retaliation tenant landlord residential"` instead of generic `"retaliatory eviction {state_name} tenant"` query.
- Fixes root cause of 11 wrong-doc PR cases in 20f722c8 run (generic query returned non-residential-retaliation cases).

**NV v2 file — Track A routing added**
- `nv_eviction_v2.json` retaliation holdings: `validation_status` → `TRACK-A-PENDING`; `track_a_routing` block added.
- Paullin v. Sutton candidate: `candidate_status` → `UNVERIFIED-NEEDS-CL-VERIFICATION`; note updated (CL searches returned wrong-doc cases; improved query will retry; case not yet CL-verified).

**NY v2 file — Track A routing added**
- `ny_eviction_v2.json` retaliation holdings: `validation_status` → `TRACK-A-PENDING`; `track_a_routing` block added.
- Reason: no leading Court of Appeals case found in Track B research; wrong-doc CL cases in 20f722c8 run; RPL §223-b is operative statute.

**`track_a_statute_runner.py` — Track A statute-direct runner built**
- `rules/validation/l2/track_a_statute_runner.py`
- Targets KS (KSA 58-2572), NV (NRS 118A.510), NY (RPL §223-b), SC (SC Code §27-40-910).
- No CL calls. Queries GPT + Gemini: does statute protect against retaliation?
- Classifies: STATUTE-CONFIRMED, STATUTE-DIVERGENCE, ERROR/SM-ERROR.
- If leading case found by both models → added to candidates[] for Track B.
- Automation ceiling: statute-verified is BELOW machine-verified, BELOW attorney line. Not validated.
- Output: `rules/validation/l2/output/track_a_statute_YYYYMMDD.json`
- **Status: ready for Andy to run from Terminal. Cowork ingests output.**

**Track A statute-direct run completed — results ingested**
- Output: `rules/validation/l2/output/track_a_statute_20260627.json`
- 4/4 STATUTE-CONFIRMED. 0 divergence. 0 error. All 4 Track A states confirmed.
- Results by state:
  - **KS** — K.S.A. 58-2572(a) confirmed. Leading case (Gemini only): Stephens v. Ludy, 42 Kan. App. 2d 531, 214 P.3d 718 (2009). Added to candidates[].
  - **NV** — NRS 118A.510(1) confirmed. Leading case (Gemini only): Anvui, LLC v. G.L., 133 Nev. 711, 405 P.3d 667 (Nev. 2017) — Nevada Supreme Court; supersedes Paullin as priority candidate. Added to candidates[] with Track B flag.
  - **NY** — RPL §223-b(1)(a)-(c) confirmed. **Key find:** Domen Holding Co. v. Aranovich, 1 N.Y.3d 117, 769 N.Y.S.2d 785 (2003) — NY Court of Appeals (highest court); GPT-identified. Gemini identified different case: 601 West 160th St. Corp. v. Henry (App. Term, 2001). Both added to candidates[] for Track B CL verification.
  - **SC** — S.C. Code Ann. §27-40-910(A)(1)-(3) confirmed. Leading case (Gemini only): Wadell v. U.S. Bank Nat'l Ass'n, 399 S.C. 541, 732 S.E.2d 523 (S.C. Ct. App. 2012). Added to candidates[].
- All 4 v2 files updated with: track_a record, TRACK-A-STATUTE-CONFIRMED flag, recommended_statute, candidates[].
- ny_eviction_v2.json: 601 West 160th St. Corp. secondary candidate added manually (Gemini diverged from Domen Holding; both warrant Track B verification).
- nv_eviction_v2.json: Anvui candidate enriched with court/year/track metadata.
- Automation ceiling: statute-verified is BELOW machine-verified, BELOW attorney line. Not validated.
- Track B priority for next CL fresh run: NV (Anvui, 2017 Nev. SC), NY (Domen Holding, 2003 CoA).

**WORK_QUEUE.md + DAILY_CHANGELOG.md updated** — this entry.

### YELLOW — Logged for ratification

**`l2_procedural_defects_runner.py`: `--output-suffix` arg added**
- Added `--output-suffix TEXT` CLI arg (optional, default "").
- Suffix appended before `.json` (e.g. `--output-suffix test` → `l2_procedural_defects_YYYYMMDD_HHMM_test.json`).
- Engineering choice: prevents test-run output files from colliding with live output filenames. No behavioral change to existing runs (default="" means output unchanged unless arg is passed).
- Flagged for Andy ratification. No attorney/legal impact.

---

## 2026-06-26 (late evening — notice tiebreaker + NJ probe + nc17_fresh_v2 ingested; GA YELLOW file update; living docs updated)

### GREEN — Executed autonomously

**notice_tiebreaker_20260626.py: bug fixed and run completed**
- Bug: `gem_stat[:60]` and `gpt_stat[:60]` raised `TypeError: 'NoneType' object is not subscriptable` when Gemini returned no statute for SD.
- Fix: changed to `(gem_stat or '')[:60]` and `(gpt_stat or '')[:60]`.
- Run completed: 7 states (GA, AR, MN, OR, SD, WY, TN). Output: `rules/validation/l2/output/notice_tiebreaker_20260626.json`.
- Results ingested (corrected from initial ingestion error — see CORRECTION note below):
  - GA: TIEBREAKER-RESOLVED-DIFFERS-FROM-FILE → YELLOW file update applied (see below)
  - AR: TIEBREAKER-CONFIRM-FILE (3d confirmed correct — file was already right) → resolved [NOTICE-L2-01]
  - MN: TIEBREAKER-CONFIRM-FILE (14d confirmed) → resolved [NOTICE-L2-02]
  - OR: TIEBREAKER-RESOLVED (days=10 confirmed by both tiebreaker models; file already had days=10; L2 flag closed) [NOTICE-L2-03]
  - SD: TIEBREAKER-FILE-ALREADY-CORRECT (both confirm notice_required=false) → resolved [NOTICE-L2-04]
  - WY: TIEBREAKER-CONFIRM-FILE (3d, §1-21-1003 confirmed) → resolved [NOTICE-L2-08]
  - TN: TIEBREAKER-CONFIRM-FILE (14d confirmed) → resolved [NOTICE-L2-09]
- Verification: HUMAN_REVIEW_QUEUE updated; 0 new L7-ESCALATED items (AR/OR resolved by tiebreaker); 6 items resolved or closed.
- **⚠️ CORRECTION (2026-06-26 late evening):** Initial ingestion incorrectly recorded AR and OR as L7-ESCALATED based on misread of prior summary. Actual terminal output (per screenshot): AR = "file confirmed correct — no action needed" (CONFIRM-FILE); OR = "tiebreaker resolved (days=10) — file update needed (YELLOW)" (RESOLVED, not split). Corrections applied to HUMAN_REVIEW_QUEUE, WORK_QUEUE, DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF, and or_eviction_v2.json L2 flag.

**nj_attach_probe_20260626.py: run completed**
- All 3 probes got content from Gemini — confirms NJ failure_to_attach ERROR was query framing, not NSR or model limitation.
- GPT timed out on all 3 probes — classified SM-GEMINI (not ERROR, not attorney lane).
- Contradictory Gemini answers (P1: R. 6:3-1 attach docs; P2: no requirement for nonpayment; P3: must attach notice) indicate NJ attachment rule depends on notice type. Needs reformulated query with GPT retry.
- Output: `rules/validation/l2/output/nj_attach_probe_20260626.json`.

**nc17_fresh_v2 retaliation holdings run ingested**
- Run file: `rules/validation/l2/output/retaliation_holdings_v3_2026-06-26_nc17_fresh_v2.json`
- Total units: 118 (header: 120; 2-unit discrepancy). MV=6, CI=0, RC=3, PR=25, SM=0, transient-failure=84.
- Method rate: 67% (6/9 text-retrievable). Overall rate: 5% (6/118).
- RC cases → HUMAN_REVIEW_QUEUE: AK (DeNardo v. Maassen), CO (Sladek v. dePlomb), CT (TOV Realty v. Suarez).
- 84 transient-failure = CourtListener 429 rate-limit errors throughout 13.3-hour run. All PR-class, quarantined for retry.
- Harness bug identified: no `bucket` key written for transient-failure disposition. GREEN fix needed.
- METRICS_LEDGER: nc17_fresh_v2 section added with full run detail.
- HUMAN_REVIEW_QUEUE: 3 new RC items added [AK-RET-HOLD-RC-01]–[CT-RET-HOLD-RC-01].

**HUMAN_REVIEW_QUEUE.md updated** (corrected from initial ingestion error)
- NOTICE-L2-01 (AR): status → ✅ TIEBREAKER-CONFIRM-FILE (3d confirmed correct) [CORRECTED: was wrongly L7-ESCALATED in initial ingestion]
- NOTICE-L2-02 (MN): status → ✅ resolved (TIEBREAKER-CONFIRM-FILE)
- NOTICE-L2-03 (OR): status → 🟡 TIEBREAKER-RESOLVED (days=10 confirmed; file already correct; L2 flag closed) [CORRECTED: was wrongly L7-ESCALATED in initial ingestion]
- NOTICE-L2-04 (SD): status → ✅ resolved (file already correct; both models confirm notice_required=false)
- NOTICE-L2-06 (GA): status → 🟡 YELLOW pending ratification (tiebreaker-resolved differs-from-file; file updated)
- NOTICE-L2-08 (WY): status → ✅ resolved (TIEBREAKER-CONFIRM-FILE)
- NOTICE-L2-09 (TN): status → ✅ resolved (TIEBREAKER-CONFIRM-FILE)
- Added [AK-RET-HOLD-RC-01], [CO-RET-HOLD-RC-01], [CT-RET-HOLD-RC-01] (new RC cases from nc17_fresh_v2)
- Queue summary counts corrected: L7 count = 43 (not 45); Resolved = 7 (not 5)

**VALIDATION_METRICS_LEDGER.md updated**
- nc17_fresh_v2 entry added to cross-batch combined table
- Full nc17_fresh_v2 detail section added (bucket breakdown, rates, harness bug note, RC items)

**WORK_QUEUE.md updated**
- Completed items added for notice tiebreaker, NJ probe, and nc17_fresh_v2 ingestion
- NEXT refreshed: harness bug fix (item 1), NJ reformulated retry (item 2), PR retry queue (item 3), Track A / improved CL queries (items 4–5)

### YELLOW — Logged for ratification

**GA notice module file update: notice_required=false, days=null**
- File: `rules/eviction/georgia/ga_eviction_v2.json`
- Change: `notice.notice_types.pay_or_quit.tenancy_all.days`: 3 → null; `notice_required: false` added; `statute`: "OCGA §44-7-50" → "O.C.G.A. §§ 44-7-50, 44-7-52"; `demand_required: true` added.
- L2-PERIOD-DIVERGENCE flag updated: disposition `open` → `tiebreaker-resolved`. Tiebreaker fields added.
- Basis: TIEBREAKER-RESOLVED-DIFFERS-FROM-FILE — both GPT (gpt-5.5) and Gemini (gemini-2.5-pro) confirmed notice_required=false, days=null in targeted tiebreaker run. Corroborated by LSC 2021 coding ("minimum amount not specified"). Contradicts file's prior days=3 (unsubstantiated initial-gen value, noted in prior L7 writeup).
- Flagged for Andy ratification. See [NOTICE-L2-06] in HUMAN_REVIEW_QUEUE.

**OR notice tiebreaker — L2 flag closed (YELLOW)**
- OR ([NOTICE-L2-03]): tiebreaker ran; both models converged on 10 days (ORS §90.394). File tenancy_all.days was already 10. L2-MODEL-SPLIT flag in `or_eviction_v2.json` updated: disposition "open" → "tiebreaker-resolved". Tiebreaker evidence recorded in flag. No notice period content change.
- **⚠️ CORRECTION:** Initial ingestion wrongly recorded OR as L7-ESCALATED. Corrected per actual runner output ("tiebreaker resolved — file update needed (YELLOW)") which means flag closure only, not L7.
- AR ([NOTICE-L2-01]): tiebreaker confirmed file correct (3d, no action needed). **⚠️ CORRECTION:** Initial ingestion wrongly recorded AR as L7-ESCALATED. Corrected per actual runner output ("file confirmed correct — no action needed"). No change to AR file needed.

---

## 2026-06-26 (evening — attach_retry9 done; notice rerun done; Counter fix; Track B research)

### GREEN — Executed autonomously

**l2_runner.py: fixed UnboundLocalError — `Counter` moved to module-level import**
- Bug: `Counter` was imported inside local function scopes at lines 405 and 610, but used at module/run level (line 593) in `run_l2()` output-writing block.
- Crash: notice provenance re-run (run_now.sh 16:18 UTC) completed all 51 states' write_back() calls successfully, then crashed at summary step: `UnboundLocalError: local variable 'Counter' referenced before assignment`.
- Fix: added `from collections import Counter` to top-level imports block (line 42).
- Verification: `python3 -c "from collections import Counter; print(Counter([1,2,2]))"` passed cleanly; --dry-run test validated.
- Impact: all 51 v2 file write_backs already completed before crash — no data lost. Only missing artifact: raw JSON output file. Reconstructed from log (see below).

**attach_retry9 run completed — results ingested**
- Run: `run_now.sh` launched at 16:18 UTC; stdout block-buffered, flushed at 16:51 UTC.
- 9 states × failure_to_attach: AL, IA, ME, MN, NH, NJ, NV, RI, VA
- Results: NSR=4 (AL, IA, RI, VA), SM=4 (ME/MN/NH=SM-GPT, NV=SM-GEMINI), ERROR=1 (NJ, persistent — 3rd run)
- SM details: ME→Me. R. Civ. P. 80D(b), MN→Minn. Stat. §504B.321 subd.1a(c), NH→N.H. Rev. Stat. Ann. §540:6, NV→NRS 40.253(1)(b)
- Output file: original overwritten by sandbox test collision (same timestamp 1651). Reconstructed: `validation/l2/output/l2_procedural_defects_attach_retry9_20260626.json`
- Note: NJ ERROR is persistent (3rd consecutive failure). Needs pipeline investigation — NOT attorney lane per anti-default rule.

**notice provenance rerun completed — results ingested**
- Run: `run_now.sh` launched at 16:18 UTC; completed all 51 states; crashed at Counter bug (fixed above).
- 51 states × notice pay_or_quit module
- Results: CONSENSUS-CONFIRM=42, MODEL-SPLIT=5, PERIOD-DIVERGENCE=2, CITATION-DIVERGENCE=1, ERROR=1
- All 51 write_back() calls completed before crash — v2 files updated with L2 flags.
- Missing artifact (raw JSON) reconstructed: `rules/validation/l2/output/notice_l2_raw_20260626.json`
- 8 divergences flagged — added to HUMAN_REVIEW_QUEUE [NOTICE-L2-01]–[NOTICE-L2-08] (YELLOW)
- Critical: GA PERIOD-DIVERGENCE (file=3d, gpt=0d) contradicts prior auto-resolved "confirmed." Needs tiebreaker run.
- Critical: MO PERIOD-DIVERGENCE (file=10d, gpt=None, gem=None) — both models now empty. Needs investigation.

**Track B case research — rate-limited states (NV, NY, OK, SC, VT)**
- CL MCP search parameter confirmed: `q` (not `query`); `type=o` for opinions.
- CL daily read limit: 125/day — exhausted during research. Root cause of overnight 429s in NC-17 run.
- CL search 5/min limit: managed by serial search strategy.
- Found via web search (Justia):
  - NV: **Paullin v. Sutton, 724 P.2d 749 (Nev. 1986)** — full opinion retrieved. Holdings: NRS 118A.510 prohibits non-renewal for retaliatory purpose; remedy = actual damages only (amended 1985). This is NV's foundational retaliation case.
  - VT: **Houle v. Quenneville, 173 Vt. 80, 787 A.2d 1258 (2001)** — VT Supreme Court. Holdings: objective test for retaliation (Gokey standard); tenant can use circumstantial evidence; protected activity must precede adverse action. CL cluster_id=2320677 (`vt` court).
  - OK: §120 = "failure to deliver possession" NOT retaliation — confirms OK [OK-RET-L7-15] L7 escalation. Web search confirms no OK retaliatory eviction statute (pending HB2015 proposal).
  - SC: No leading appellate case found. SC Code §27-40-910 is statute-only authority.
  - NY: No Court of Appeals leading case found. RPL §223-b statute solid; Ellis v. Oceanhill already RC.
- CL correct court IDs discovered: `vt` (Vermont SC), `sc` (SC SC confirmed by web search structure).
- Track A (statute-direct for 12 `__no_cases__` states): viable — all 12 have statutes in v2 files.

**Provenance output files written**
- `validation/l2/output/l2_procedural_defects_attach_retry9_20260626.json` — reconstructed
- `rules/validation/l2/output/notice_l2_raw_20260626.json` — reconstructed

### GREEN — Additional (session continuation)

**NV/VT v2 files updated — case_law_candidates added**
- NV (`nv_eviction_v2.json`): added Paullin v. Sutton, 724 P.2d 749 (Nev. 1986) under `retaliation.layer_decomposition.holdings.candidates`. Track B candidate; UNVERIFIED. Holdings v3 runner will verify via CL when run.
- VT (`vt_eviction_v2.json`): added Houle v. Quenneville, 173 Vt. 80, 787 A.2d 1258 (2001) under `retaliation.layer_decomposition.holdings.candidates`. CL cluster_id=2320677 (court=vt). Track B candidate; UNVERIFIED.
- Both files now have candidates[] populated; subsequent holdings v3 run will attempt verification.

**Completed jobs moved to done/ in dispatcher queue**
- `job_l2_attach_retry9_20260626.json` → `done/` (ran via run_now.sh)
- `job_notice_rerun_20260626.json` → `done/` (ran via run_now.sh)

**Notice tiebreaker script written and queued**
- File: `rules/validation/l2/notice_tiebreaker_20260626.py`
- 7 targeted state-specific queries: GA (CRITICAL), AR, MN, OR, SD, WY, TN.
- Each query designed to resolve the specific documented split (more targeted than standard QUERY_TEMPLATE).
- Syntax-verified: `python3 -m py_compile` OK.
- Queued: `rules/validation/queue/job_notice_tiebreaker_20260626.json`
- Also added to `run_now.sh` (Job 1) for immediate launch.

**NJ failure_to_attach probe script written and queued**
- File: `rules/validation/l2/nj_attach_probe_20260626.py`
- 3-probe diagnostic: ultra-simple, rule-direct, consequence-framing queries.
- Goal: determine if NJ ERROR is (a) query framing, (b) genuine NSR, or (c) model limitation.
- Syntax-verified: `python3 -m py_compile` OK.
- Queued: `rules/validation/queue/job_nj_attach_probe_20260626.json`
- Also added to `run_now.sh` (Job 2) for immediate launch.

**run_now.sh updated to current queue**
- Now launches: notice tiebreaker (Job 1) + NJ probe (Job 2)
- Both use `python3 -u` (unbuffered) to prevent stdout buffering in log files.

### YELLOW — Logged for ratification

**8 notice module divergences flagged (provenance rerun)**
- 5 MODEL-SPLIT (AR, MD, MN, OR, SD), 2 PERIOD-DIVERGENCE (GA, MO), 1 CITATION-DIVERGENCE (WY).
- GA and MO PERIOD-DIVERGENCE contradict prior "auto-resolved" status — recommend tiebreaker re-run.
- Added to HUMAN_REVIEW_QUEUE as [NOTICE-L2-01]–[NOTICE-L2-08].

**Sandbox test collision — output file overwritten**
- Ran `l2_procedural_defects_runner.py --defects attach --states AL,IA,ME --dry-run` in sandbox to debug job crash. Sandbox test wrote `l2_procedural_defects_20260626_1651.json` (all ERROR, 3 states). Real job also wrote to same filename (same minute timestamp). Sandbox file overwrote real output.
- Impact: minimal. Log preserved all real results. Reconstructed clean output file.
- Prevention: test runs in sandbox should use `--dry-run` flag AND a `--output-suffix test` option (not yet implemented). YELLOW: recommend adding `--output-suffix` to runner for sandbox isolation.

---

## 2026-06-26 (daytime — notice rerun queued; l2_runner.py --sleep fix)

### GREEN — Executed autonomously

**l2_runner.py: added `--sleep` argument for dispatcher compatibility**
- Added `import time`
- Added `--sleep` (float, default 0) to argparse
- Added `sleep_secs: float = 0` parameter to `run_l2()`
- Added `time.sleep(sleep_secs)` between state iterations (skipped on last state)
- Wired through in `__main__` block: `sleep_secs=args.sleep`
- `--dry-run --sleep 2` validated: no errors, accepts argument cleanly
- Prior dispatcher incompatibility: `_build_l2_cmd` always passes `--sleep N`; l2_runner.py had no such arg → would have failed with argparse "unrecognized arguments" error. Now fixed.

**Notice module provenance re-run queued**
- Job: `rules/validation/queue/job_notice_rerun_20260626.json`
- Runner: `rules/validation/l2/l2_runner.py --states ALL --sleep 2`
- Fires tonight at 2:15 AM (after attach-retry-9, dispatcher picks queue order by filename/age)
- Expected output: `rules/validation/l2/output/notice_l2_raw_{date}.json`
- Est. cost: ~$1.10 · Est. time: ~20 min · 51 states × notice pay_or_quit module
- Attorney-confirmed outcomes in state files preserved (write-back respects existing flags)
- Closes provenance gap documented in VALIDATION_METRICS_LEDGER

### RED — Carried. NC-17: 12 states with no CL case law (genuine gap, see below).

---

## 2026-06-26 (morning report — NC-17 fresh run ingested)

### GREEN — Executed autonomously

**Ingested NC-17 fresh run** (`rules/validation/l2/output/retaliation_holdings_v3_2026-06-26_20f722c8.json`, `SUMMARY_retaliation_holdings_v3_2026-06-26_1000.md`)

Run completed 10:00 UTC via launchd. First attempt (05:17) failed with returncode=1 (sandbox path issue — not an issue on Andy's Mac). Retry succeeded, 241.6 min elapsed.

50 units across 17 NC states (fresh=true CL search). Bucket: MV=0, CI=0, RC=2, PR=11, SM=0, perm-fail=37. Method rate: 0÷2=0%. Overall rate: 0÷50=0%. α_method=n/a (n=2, all RC, D_e=0).

Actions taken:
- **HUMAN_REVIEW_QUEUE**: [NV-RET-HOLD-RC-01] Wright v. Brady (NV) and [NY-RET-HOLD-RC-02] Ellis v. Oceanhill Brownsville Tenant Ass'n (NY) added. Anti-default rule satisfied for both (full generate+verify protocol with CL retrieval completed before routing).
- **VALIDATION_METRICS_LEDGER**: NC-17 fresh run entry added to cross-batch table; detailed section added with bucket counts, rates, α, PR diagnosis, and perm-fail interpretation.
- **PROJECT_STATE_OF_RECORD**: Holdings v3 status updated to reflect all runs complete; NC states status documented.
- **WORK_QUEUE**: NC-17 ingest moved to Completed; attach-retry-9 promoted to NOW; NEXT queue refill proposed.
- **attach-retry-9 job queued**: `rules/validation/queue/job_l2_attach_retry9_20260626.json` created for AL/IA/ME/MN/NH/NJ/NV/RI/VA (failure_to_attach defect only). Fires tonight at 2:15 AM.
- **CLAUDE_CHAT_BRIEF.md**: Regenerated (see Step 3f).
- **Job moved**: job_nc17_fresh_20260625.json already in done/ (moved by dispatcher).

### YELLOW — None this cycle.

### RED — Escalated (2 new, carried remainder)

**RED-interpretive [NV-RET-HOLD-RC-01]**: Wright v. Brady (NV) — CL text retrieved, verify step disputed the holding. Attorney must confirm, characterize, or dismiss. Full automated attempt complete.

**RED-interpretive [NY-RET-HOLD-RC-02]**: Ellis v. Oceanhill Brownsville Tenant Ass'n (NY) — CL text retrieved, generate step failed to extract a retaliation holding. Attorney must confirm case is a valid holding candidate or dismiss. Full automated attempt complete.

**RED-strategic (carried)**: Direction B golden-set freeze. ~15 NC states with no CL candidates — Andy's decision on path forward.

---

## 2026-06-26 (early morning — failure_to_attach re-run ingested)

### GREEN — Executed autonomously

**Ingested failure_to_attach re-run** (`validation/l2/output/l2_procedural_defects_20260626_0830.json`)

Run completed at 2:34 AM via launchd dispatcher. 51 units (51 states × failure_to_attach). Output ingested:

Results: CI=0, CC=3, NSR=28, MODEL-SPLIT=2, SM=8 (SM-GEMINI=5, SM-GPT=3), ERROR=9. α_method=0.470.

Before/after vs 204-unit run (failure_to_attach subset):

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| NSR | 6 | 28 | +22 ← prompt fix |
| SM | 22 | 8 | −14 (64%) ← token fix |
| ERROR | 23 | 9 | −14 (61%) ← both fixes |
| Dual-model coverage | 2% | 65% | +63 pp |

Both fixes validated. 9 residual ERRORs are network timeouts (not token stalls) — distinct issue, queued for retry pass.

Actions taken:
- **CA v2 file updated**: `failure_to_attach` statute corrected from `CCP §1161 et seq.` → `Cal. Code Civ. Proc. § 1166(d)(1)–(2)` (CONSENSUS-IMPROVE applied by runner)
- **HUMAN_REVIEW_QUEUE**: [PROC-DEF-L7-21] CT and [PROC-DEF-L7-22] FL added (both MODEL-SPLIT on failure_to_attach — statute vs court rule as governing source)
- **VALIDATION_METRICS_LEDGER**: New section added with before/after comparison, α computation, SM breakdown, root-cause analysis of 9 residual ERRORs
- **Job moved**: `queue/job_l2_attach_rerun_20260625.json` → `done/`

### RED — Carried (no change). NC-17 fresh run still executing (~55/120 cases at 2:35 AM, active CL 429 backoff).

---

## 2026-06-25 (late night — SM diagnostic + launchd wrapper)

### GREEN — Executed autonomously

**SM diagnostic — single-model rate root cause identified**

Split: SM-GPT=1, SM-GEMINI=119 of 120 SM units. GPT is responsible for 99.2% of single-model cases.

Failure signature: `gpt_raw = ""` (empty string), `gpt_error = ""` (no error raised). The OpenAI API call succeeds and returns a response object — but `resp.choices[0].message.content = ""`. This is not a timeout (60s limit not hit), not a 429 (no rate-limit error), not a safety refusal (no error field). It is a reasoning-model token-budget stall: gpt-5.5 consumes its chain-of-thought tokens before writing any output, and returns an empty content field.

No position, defect, or state correlation: SM-GEMINI appears at position 3 (first AK/summons unit) and is spread uniformly through the run (25/50 in first half, 22/50 in last half). Rate-limit clustering would show SM concentrated later in the run; it does not. All four defects are affected (summons=44, complaint_filed=34, failure_to_attach=21, wrong_court=20).

Retry status: the retry IS in the code and IS firing. `query_model()` at line 249 checks `if not raw and attempt == 0: time.sleep(5); continue` — this triggers on every empty response. The retry is not a no-op (unlike the fresh=True bug). The problem is that one retry with a 5s pause does not resolve a token-budget stall: the model produces the same empty response on attempt 1. There is no print() in the retry branch, so logs show no "retrying" message — but the code path executes.

Root cause: `max_completion_tokens=2000` in `call_openai()` (`l2_runner.py` line 130). gpt-5.5 uses tokens for internal chain-of-thought before writing output; 2000 is insufficient for complex multi-field legal research prompts. The comment on line ~246 notes "350 caused empty responses" — 2000 was an improvement but still hits the ceiling.

**YELLOW — fix proposed (awaiting ratification before implementing):**
Increase `max_completion_tokens` from 2000 → 8000 in `call_openai()` (`rules/validation/l2/l2_runner.py` line 130). Expected SM-GEMINI reduction: 70–90% (token budget stall resolves when reasoning tokens have headroom). Per Direction A Rev 2 run-before-queue rule: fix must be validated on a live small sample (10 states × 1 defect, before/after SM rate measured) before full-scale deployment. Do NOT implement until ratified.

**Shell wrapper + launchd plist — wrapper updated, plist updated, live simulation complete**

Changes:
- `rules/validation/run_dispatch.sh` — added `caffeinate` availability check; falls back gracefully on Linux/sandbox without failing the script (allows reliable testing outside macOS).
- `rules/validation/com.cjac.validation.plist` — `ProgramArguments` changed from `[/usr/bin/python3, dispatch.py]` → `[/bin/bash, run_dispatch.sh]`. Added FDA setup instructions and MANUAL TRIGGER / SIMULATE commands to plist header comment.
- `rules/validation/queue/` — moved `job_l2_procedural_defects_20260624.json` to `done/` (it ran manually on 2026-06-25; was never moved by dispatcher due to launchd blocker).

Live simulation proof (timestamp: 2026-06-26T05:17:42):
```
[run_dispatch.sh] Using Python: /usr/bin/python3 (Python 3.10.12)
[run_dispatch.sh] Dispatch script: .../rules/validation/dispatch.py
[run_dispatch.sh] Mode: --single
[run_dispatch.sh] caffeinate not available — running without sleep guard
[dispatch] Single-shot: job_20260625_nc17_fresh
[dispatch] 🚀 Launching: job_20260625_nc17_fresh | cmd: caffeinate -ims /usr/bin/python3 .../run_protocol.py --protocol...
[dispatch]    Log: .../logs/dispatch_retaliation_holdings_v3_20260626_0517.log
```
Log file written: `rules/validation/logs/dispatch_retaliation_holdings_v3_20260626_0517.log`. Wrapper found Python, dispatcher picked job from queue, subprocess launched. Sandbox-only failure: `PermissionError` on `job_path.unlink()` (sandbox can't delete mounted files) and `ModuleNotFoundError` for protocol import (sandbox path mismatch) — neither occurs on Andy's Mac.

**✅ BLOCKER CLOSED — launchd live-run proof (2026-06-25 22:39 PT):**
```
[dispatch] Single-shot: job_20260625_nc17_fresh
[dispatch] 🚀 Launching: job_20260625_nc17_fresh | cmd: caffeinate -ims
  /Library/Developer/CommandLineTools/usr/bin/python3
  .../run_protocol.py --protocol retaliation_holdings_v3 --states AK,AL,...
[dispatch]    Log: .../logs/dispatch_retaliation_holdings_v3_20260626_0539.log
```
`launchctl start com.cjac.validation` → dispatcher fired → picked NC-17 job → launched subprocess with caffeinate → log written. Plist uses `/usr/bin/python3` (symlink to CLT python3 at `/Library/Developer/CommandLineTools/usr/bin/python3`) which already had FDA toggled ON in System Settings. NC-17 fresh run is now executing in background (~90 min).

### YELLOW — Ratified and implemented
- `max_completion_tokens` 2000 → 8000 in `call_openai()` (`rules/validation/l2/l2_runner.py` line 135). Andy ratified 2026-06-25. Validation: the queued `job_l2_attach_rerun_20260625.json` (51 states × failure_to_attach) will run with the new setting and serve as before/after SM measurement. Prior SM-GEMINI rate on this defect: 21/51 (41%). Expected post-fix: <10%.

### RED — Carried (no change).

---

## 2026-06-25 (night — fresh=True fix + failure_to_attach fix)

### GREEN — Executed autonomously

**Fix #9: `load_draft_cases()` CL search when `fresh=True`**
- Added `cl_search_retaliation_by_state(state_abbr, max_results=8)` to `rules/validation/l2/retaliation_holdings_v3_runner.py`. Searches CL with query `"retaliatory eviction {state_name} tenant"`, returns up to 8 precedential opinions per state in the `verify_case()`-compatible dict format.
- Modified `load_draft_cases(state, fresh=False)` — when `fresh=True` and no v1 draft candidates exist for the state, calls CL search instead of returning `[]`.
- Updated `protocols/retaliation_holdings_v3.py` `get_units(states, fresh=False)` — now accepts and passes `fresh` to `load_draft_cases()`.
- Updated `rules/validation/run_protocol.py` line 126: `protocol.get_units(states, fresh=args.fresh)` — `--fresh` flag now propagates all the way to CourtListener search.
- Verified: 4/4 files syntax OK; 30/30 regression tests pass.
- **NC-17 re-run command:** `python3 rules/validation/run_protocol.py --protocol retaliation_holdings_v3 --states AK,AL,CO,CT,HI,KS,LA,MI,ND,NJ,NM,NV,NY,OK,SC,VT,WV --fresh --run-id nc17_fresh_v2` (requires COURTLISTENER_API_TOKEN env var)

**Fix #10: `failure_to_attach` prompt — explicit NSR instruction**
- Updated `QUERIES["failure_to_attach_lease_or_notice_to_complaint"]` in `rules/validation/l2/l2_procedural_defects_runner.py`.
- Key change: added explicit instruction that "most states do NOT have a specific attachment statute" and that `attachment_required: false, statute: null` is "a valid and expected answer — do NOT leave the response empty."
- Queued overnight job: `rules/validation/queue/job_l2_attach_rerun_20260625.json` — `defects: "attach"`, 51 states, est. ~15 min, $0.50.
- Verified: syntax OK; 30/30 regression tests pass.

### YELLOW — None this cycle.

### RED — Carried (no change).

---

## 2026-06-25 (late evening — NC-17 results ingested)

### GREEN — Executed autonomously

**NC-17 retaliation holdings v3 (run 21c5b706) — ingested**
- 17 states, all `__no_cases__` → `permanent-failure`. MV=0, CI=0, RC=0, PR=0, SM=0, NC=17.
- Method rate: n/a (0 text-retrievable). Overall rate: 0%.
- **Root cause diagnosed (GREEN pipeline bug):** `fresh=true` was a no-op. `run_protocol.py`'s `--fresh` flag only clears the checkpoint; it does not change `load_draft_cases()` in `retaliation_holdings_v3_runner.py`. That function always reads from the v1 draft file, which has no entries for these 17 states. CourtListener search was never called — confirmed by 0-second per-state processing time.
- All 17 NC states remain NC. They are NOT PR (no retrieval failure — no retrieval was attempted). Not attorney lane.
- METRICS_LEDGER updated with NC-17 row + diagnosis note.
- **Next step:** Implement CL candidate search in `load_draft_cases()` when `fresh=True` and no draft candidates exist. Queued in WORK_QUEUE.

### YELLOW — None this cycle.

### RED — Carried (no change).

---

## 2026-06-25 (evening — procedural defects ingestion + NC-17 launch)

### GREEN — Executed autonomously

**Procedural defects 204-unit L2 run — ingested**
- Output: `validation/l2/output/l2_procedural_defects_20260626_0018.json` — 204 units, 51 states × 4 defects
- Bucket counts: CI=4, CC=31, NSR=6, MODEL-SPLIT=20, SM=120, ERROR=23
- α_method = 0.256 (n=61 dual-model; 143 SM+ERROR = pipeline gap)
- 4 CONSENSUS-IMPROVE file updates already applied by runner (IA/NY/UT/WY summons citations)
- 20 MODEL-SPLIT items added to HUMAN_REVIEW_QUEUE [PROC-DEF-L7-01] through [PROC-DEF-L7-20]
- VALIDATION_METRICS_LEDGER and HUMAN_REVIEW_QUEUE updated
- Pipeline flag: (1) GPT empty on ~70% of units; (2) failure_to_attach: all 23 ERRORs from this defect — recommend re-run with explicit NSR prompt option
- NC-17 retaliation run launched by Andy (running): early AK/AL showing `__no_cases__` from CourtListener fresh search — genuine data gap, NOT attorney lane

### YELLOW — None this cycle.

### RED — Carried
- launchd FDA fix pending; Direction B attorney freeze pending; 20 new procedural defects L7s added to queue

---

## 2026-06-25 (afternoon — Direction A Rev 2 adoption + Direction B survey)

### GREEN — Executed autonomously

**dispatch.py — Direction A Rev 2 complete rewrite**
- Continuous drain loop (`drain()`) + parallel execution (up to 3 concurrent jobs).
- Per-resource concurrency limits: `courtlistener:1`, `openai:2`, `gemini:2`.
- Change 3 live_verified gate: jobs without `live_verified:true` are skipped with warning.
- Heartbeat: writes `logs/heartbeat.json` each cycle.
- `main_single()` single-shot mode preserved for launchd safety-net.
- `--drain` flag selects continuous vs single-shot.
- Python 3.9 compatibility: all type hints use `Optional[Path]`, `Tuple[bool, str]` (no 3.10+ `|` union syntax).
- AST verified clean. NOT yet live-verified via launchd (per Change 3 — "change applied, not fixed").

**run_dispatch.sh — new shell wrapper for launchd FDA fix**
- Resolves Python: prefers `/opt/homebrew/bin/python3`, falls back gracefully.
- `caffeinate -ims` keeps machine awake during run.
- Supports `--drain` pass-through.
- launchd plist should call `/bin/bash run_dispatch.sh` (FDA on /bin/bash, not python3).
- Written and made executable. NOT yet live-verified (same Change 3 note).

**job_l2_procedural_defects_20260624.json — updated for Rev 2 dispatcher**
- Added `"uses": ["openai", "gemini"]` resource tag.
- Added `"live_verified": true` with basis: runner smoke-tested 3 runs 2026-06-24; all 4 classification branches exercised; 30/30 regression tests pass.

**Procedural defects run — command staged for Andy**
- Run command written to clipboard; Terminal opened.
- Andy: paste (⌘V) + Return to launch 204-unit run.
- Command: `cd ~/Documents/GitHub/a2j-ai && python3 rules/validation/l2/l2_procedural_defects_runner.py --sleep 2 2>&1 | tee rules/validation/logs/l2_procedural_defects_$(date +%Y%m%d_%H%M).log`

**Direction B — Golden Set Survey complete**
- Surveyed: LSC/Temple Eviction Laws Database, LegalBench (NeurIPS 2023), Learned Hands, JusticeBench, Stanford AI+A2J/Gates, Eviction Lab, NCSC data standards.
- Finding: No existing public dataset provides adoptable annotated fact-pattern/answer pairs for our modules.
- LSC/Temple LawAtlas: useful for statutory cross-reference, but Jan 2021 snapshot (5 years old).
- LegalBench IRAC structure: methodology reference for fact-pattern design.
- Full report: `docs/DIRECTION_B_SURVEY.md`.
- Next step: generate CA/TX notice + service candidates (RED gate for attorney freeze).

**NC-17 fresh run — queued (Andy authorized 2026-06-25)**
- Job: `queue/job_nc17_fresh_20260625.json` — 17 states (AK,AL,CO,CT,HI,KS,LA,MI,ND,NJ,NM,NV,NY,OK,SC,VT,WV), `fresh=true`, `sleep=10`, `uses:[courtlistener,openai,gemini]`.
- Run after procedural defects finishes: `python3 rules/validation/run_protocol.py --protocol retaliation_holdings_v3 --states AK,AL,CO,CT,HI,KS,LA,MI,ND,NJ,NM,NV,NY,OK,SC,VT,WV --sleep 10 --fresh`
- Will search CourtListener for retaliation case candidates in each state, then validate holdings. PR states go to quarantine; MV/CI/RC/SM as usual.

**Direction B — Golden-set candidates generated (DRAFT/UNFROZEN)**
- `rules/validation/golden_sets/DRAFT_CA_notice_candidates_v0.1.json` — 20 CA notice fact patterns
- `rules/validation/golden_sets/DRAFT_CA_service_candidates_v0.1.json` — 15 CA service fact patterns
- `rules/validation/golden_sets/DRAFT_TX_notice_candidates_v0.1.json` — 15 TX notice fact patterns
- 50 total candidates. HIGH confidence: 28. UNCERTAIN/LOW: 22 (flagged for attorney).
- All DRAFT/UNFROZEN. RED gate: Andy must review and freeze each item individually.

**WORK_QUEUE updated** — NOW section reflects procedural defects run + Direction B candidate generation.

### YELLOW — None this cycle.

### RED — Carried
- **launchd macOS TCC (FDA):** Both dispatch.py fixes applied; shell wrapper written. FDA grant still needed. Andy: System Settings → Privacy & Security → Full Disk Access → add `/bin/bash`.
- **Direction B attorney freeze gate:** Candidate generation next; attorney establishment of DRAFT answers = RED.

---

## 2026-06-25 (morning report — second cycle, late morning)

### GREEN — Executed autonomously

**Verified dispatch.py Python 3.9 fix is in place**
- Confirmed `Optional[Path]` and `Tuple[bool, str]` present in dispatch.py (prior 08:00 cycle applied fix; confirmed by grep this cycle).
- Both overnight jobs still in `queue/` (FDA blocker unchanged — no runs since Jun 23).

**Direction B — Golden Set Survey pulled into NOW**
- WORK_QUEUE updated: Direction B survey moved from NEXT to NOW. No dependency on FDA fix.
- NEXT renumbered accordingly.

**Living docs updated — WORK_QUEUE, DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF regenerated.**

### YELLOW — None this cycle.

### RED — Escalated
**RED-strategic — launchd macOS Full Disk Access (carried; both fixes now applied; FDA grant still needed)**

---

## 2026-06-25 (morning report — automated)

### GREEN — Executed autonomously (morning report cycle)

**dispatch.py — Python 3.9 type hint compatibility fix**
- **New bug found in stderr log:** `TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'` at line 74 — `def pick_next_job() -> Path | None:`. The `|` union type syntax in annotations requires Python 3.10+. The launchd plist uses `/Library/Developer/CommandLineTools/usr/bin/python3` which is Python 3.9.x.
- **Fix applied:** Added `from typing import Optional, Tuple` import; replaced all 3.10+ type hints with 3.9-compatible equivalents:
  - `Path | None` → `Optional[Path]` (pick_next_job, find_latest_summary)
  - `tuple[bool, str]` → `Tuple[bool, str]` (run_job, run_protocol_job, run_l2_module_job, _run_subprocess)
- **Verified:** AST parse clean; no remaining `| None` or `tuple[` annotations in file.
- **Impact:** This bug would have caused dispatch.py to fail even after the FDA permission fix. Both fixes (FDA + Python version) are required for overnight runs to succeed.

**Batch 3 holdings v3 (run 7e6fcf6d) — ingested to VALIDATION_METRICS_LEDGER**
- 23 units: 4 MV, 2 CI, 0 RC, 0 PR (confirmed), 0 SM, 17 NC (no-candidates)
- Method rate: 66.7% (4/6 CA text-retrievable). Overall rate: 17.4% (4/23).
- **PR=0 confirmed.** Andy's expectation that "other:17" = PR from 429s is NOT confirmed. The 429s were transient (CA cases only) and recovered successfully. The 17 "other" are NC (no-candidate) states — `fresh=false` + no pre-existing candidate cases in those state files. NOT quarantined as PR. NOT attorney lane. Require `fresh=true` run or manual candidate identification.
- NC states: AK, AL, CO, CT, HI, KS, LA, MI, ND, NJ, NM, NV, NY, OK, SC, VT, WV.
- MV cases (CA): S. P. Growers Assn., Barela, Drouet, Aweeka. CI cases: Schweiger, Western Land Office.
- Live-run proof: dispatcher ran cleanly at 16:21 UTC today. job_batch3_20260623.json moved to done/. Direction A Rev 2 Change 3 satisfied for this job.

**Living docs updated — WORK_QUEUE, STATE_OF_RECORD, DAILY_CHANGELOG, CLAUDE_CHAT_BRIEF regenerated**

### YELLOW — None this cycle.

### RED — Escalated
**RED-strategic — launchd macOS Full Disk Access (carried from prior cycle)**
- Both queued jobs still in queue/. Same blocker as yesterday. Python 3.9 fix now applied (GREEN); FDA permission still needed.

---

## 2026-06-24 (session — new direction + FDA fix)

### GREEN — Executed autonomously

**COWORK_DIRECTION_CHAT_BRIEF.md — saved to docs/**
- Direction saved at `docs/COWORK_DIRECTION_CHAT_BRIEF.md`. GREEN lane (derived artifact, no new judgment).

**docs/CLAUDE_CHAT_BRIEF.md — first build (manual)**
- Generated from current canonical docs. ~1,100 words, within cap. All open REDs present (FDA blocker, 4 notice L7s, 14 retaliation L7s, CA/summons procedural defect, 2 service L7s, SCRA pending-confirmation).
- Subsequent builds auto at 8 AM morning-report cycle (Step 3f added).

**Morning report scheduled task — updated**
- Added Step 3f: regenerate `docs/CLAUDE_CHAT_BRIEF.md` after all canonical docs updated, paste into report.
- `CLAUDE_CHAT_BRIEF.md` not regenerated in this cycle = failure condition added.

### RED — Escalated

**RED-strategic — launchd macOS Full Disk Access (carried from prior cycle)**
- Both jobs still in queue/. Fix steps provided to Andy in this session (see below).

---

## 2026-06-24 (morning report — automated)

### GREEN — Executed autonomously (morning report cycle)

**Smoke test run 3 — formally ingested to VALIDATION_METRICS_LEDGER**
- 6 units: CA/TX/NY × summons + attach. Results: CC=1, NSR=2, SM-GEMINI=1, MODEL-SPLIT=1, ERROR=1.
- Method α = 0.333 (n=4 method cases). Overall α = 0.0 (n=6 including SM+ERROR as DISAGREE). Values statistically unreliable at n=6; noted in ledger.
- Ledger row appended: `Procedural Defects / L2 smoke test run 3`.

**Regression tests — confirmed passing in sandbox**
- `rules/validation/tests/test_l2_procedural_defects.py` — 30/30 pass (re-verified this cycle).

**Direction A — all items confirmed complete**
- Regression tests: 30/30 pass (test file exists at 387 lines).
- dispatch.py: L2 module job type fully wired (confirmed in source).
- Job files: both `job_batch3_20260623.json` and `job_l2_procedural_defects_20260624.json` in queue/.
- WORK_QUEUE.md: NOW section updated to reflect Direction A complete; BLOCKED row added for launchd FDA issue.

**DAILY_CHANGELOG, WORK_QUEUE, METRICS_LEDGER, PROJECT_STATE_OF_RECORD updated this cycle.**

### YELLOW — None this cycle.

### RED — Escalated

**RED-strategic — launchd macOS Full Disk Access blocking overnight runs**
- Both queued jobs (`job_batch3` and `job_l2_procedural_defects`) did not run.
- `launchd_stderr.log`: `[Errno 1] Operation not permitted` when attempting to open `dispatch.py`.
- Root cause: macOS TCC blocks launchd agents from reading `~/Documents/GitHub/` without explicit FDA grant.
- Fix options (for Andy): (a) System Settings → Privacy & Security → Full Disk Access → add python3; (b) approve Cowork writing a shell wrapper script that launchd calls instead.
- Both jobs remain in queue/ and will auto-run on next successful 2:15 AM fire after fix.

**RED-interpretive — CA/summons MODEL-SPLIT (carried from prior session; in HUMAN_REVIEW_QUEUE)**

---

## 2026-06-24 (session — prior)

### GREEN — Executed autonomously (no approval needed)

**l2_procedural_defects_runner.py — 3 bug fixes (all test-verified)**

1. **`query_model` signature fix** — `call_openai`/`call_gemini` take one string arg and return a parsed dict; previous code called `model_fn(SYSTEM_PROMPT, prompt)` (two args) and then called `_parse_json_response()` on an already-parsed dict. Fixed to `model_fn(prompt)` with error detection via `result.get("error")`. *Verified: sandbox import test, no TypeError.*

2. **`citations_equivalent` section-number match** — 70% token-overlap fuzzy matcher classified `Tex. R. Civ. P. 510.4(b)-(c)` vs `Texas Rule of Civil Procedure 510.4` as MODEL-SPLIT (false positive). Added section-number match: if both citations share the same specific numeric section reference (`\b(\d{2,}(?:\.\d+)+|\d{3,})\b`), treat as equivalent. *Verified: 5-case unit test — 3 true matches, 2 true splits, all correct.*

3. **`SM-GEMINI`/`SM-GPT` classification** — when GPT returns empty but Gemini has a valid answer (or vice versa), previous code classified as ERROR and discarded the surviving model's output. New behavior: `SM-GEMINI` / `SM-GPT` classification, writes `l2_sm_statute` to file, flags for re-run. ERROR now reserved for both-models-empty only. *Verified: smoke test run 3 — CA/attach ERROR (both empty), NY/summons SM-GEMINI (Gemini preserved RPAPL § 735).*

4. **Retry logic for GPT empty responses** — added one retry with 5-second pause when `_raw` is empty. Reduced ERROR rate from 4→3 across the 6-unit smoke test.

**Smoke test results (3 runs, CA/TX/NY × attach + summons):**
- Run 1 (pre-fix): 0 CONSENSUS, 2 MODEL-SPLIT (false), 4 ERROR
- Run 2 (fix 1+2): 1 CI, 1 CC, 1 NSR, 0 MODEL-SPLIT, 3 ERROR
- Run 3 (fix 3): 1 CC, 2 NSR, 1 SM-GEMINI, 1 MODEL-SPLIT (genuine), 1 ERROR

**Direction A infrastructure**
- Saved COWORK_HANDOFF_ABC.md, DIRECTION_A/B/C docs to `docs/`
- Created `docs/WORK_QUEUE.md` (NOW/NEXT/BLOCKED/HORIZON, populated several days deep)
- Created `docs/DAILY_CHANGELOG.md` (this file)

**Smoke test ingestion (pending)**
- Third run output: `validation/l2/output/l2_procedural_defects_20260624_1646.json`
- Summary: 1 CONSENSUS-CONFIRM (TX/summons), 2 NO-SPECIFIC-RULE (TX/NY attach), 1 SM-GEMINI (NY/summons → RPAPL § 735), 1 MODEL-SPLIT (CA/summons), 1 ERROR (CA/attach)

---

### YELLOW — Executed, flagged for ratification

*(none yet — pending morning report ratification cycle)*

---

### RED — Escalated, not decided by Cowork

**RED-interpretive — CA/summons procedural defect MODEL-SPLIT**
- GPT: `Cal. Code Civ. Proc. § 1167(a)` (UD summons return provision)
- Gemini: `Cal. Code Civ. Proc. § 415.45` (service by posting in UD cases)
- Both are legitimate CA summons-related provisions; they govern different aspects of the UD summons process. Needs attorney determination: which section (or both) applies as the specific governing rule for summons service defects in CA UD cases?
- *Automated attempt:* 3 runs, genuine split persisted. Section-number match correctly declined to merge (different numbers: 1167 vs 415). Not a formatting artifact — substantive disagreement.
- *Disposition:* Written to HUMAN_REVIEW_QUEUE as L7-procedural-defects. Not routed to attorney by default — routed because it is genuinely interpretive.

---

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
