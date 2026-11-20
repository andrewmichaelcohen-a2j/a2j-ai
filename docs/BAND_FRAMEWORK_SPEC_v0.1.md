# Band framework spec v0.1 (DRAFT, Nov 20, 2026)

**Status: DRAFT background note, not a working spec. Andy (Nov 20, 12:10): the bands are background framework for good playbook drafting, not something to iterate on; the pilot does not depend on the precise definitions. Do not build on or refine this without his say. Not attorney-reviewed.** The Oct 31 definition pack was not found, so this spec was written on Nov 20 from Andy's notes (Oct 29, Oct 31), the Nov 1 Framework Spec (which uses bands, particularity and release modes without defining them) and what the pilot already does. Items marked *(inferred)* are Claude's best reading and need Andy's confirmation. If the original pack turns up, compare and keep the better wording.

Three scales sit on every playbook item as metadata. They answer three different questions:

| Scale | Question it answers | Values |
| --- | --- | --- |
| Band | What kind of content is this, and so how can it be checked? | 1 to 4 |
| Particularity | How closely does the answer fit one person's facts? | P0 to P3 |
| Release mode | Who may see it, and under what conditions? | A, A*, B, C, Refer |

The strength label (Source-read, Lawyers differ, Not yet checked, Attested) is separate again. It is computed from the item's review history and never typed by hand (Framework Spec, item schema).

## 1. Bands: kind of content, and the assurance it can earn

| Band | What it is | Example | How it is checked | Strongest label it can earn |
| --- | --- | --- | --- | --- |
| 1. Deterministic | Fixed by rule text or arithmetic. | General limit of four years for a written contract; days to respond after service. | Checker matches each statement to saved source text; quotes verified word for word in code; calculators tested and refusing unclear inputs. | Source-read |
| 2. Structured | Elements, burdens, procedure, forms and where to file, readable from sources but applied to facts by the reader. | What a plaintiff must show; which form is the answer; what a default means. | As Band 1, plus adversarial review. Where sources or lawyers conflict, show both. | Source-read, or Lawyers differ |
| 3. Common-scenario guidance | Practical steps for typical situations that no single source states. | "Keep copies of everything." "Talk to a lawyer before signing." | No source can support it. AI checks harm direction and consistency with Bands 1 and 2; a named attorney attests. | Attested |
| 4. Particular-scenario judgment | Strategy and prediction for one person's case. | Settle or fight; bankruptcy; whether you will win. | Not answered. The item states the boundary and where to go. | None (Refer) |

Band 4 is a permanent boundary, never a target. This matches the old rule that the system never gives a Band 1 style answer to a Band 2 question, and extends it: it never gives a Band 2 style answer to a Band 4 question.

**Relation to the three-band docs** (GLOSSARY, CJAC_ROADMAP, OPEN_QUESTIONS_AND_LIMITATIONS, A2J_STACK_AND_CJAC_SCOPE): old Band 1 is now Band 1; old Band 2 is now Bands 2 and 3 *(inferred; the Oct 29 notes added a self-help "common scenario" category)*; old Band 3 is now Band 4.

**Relation to the pilot's line kinds:** Rule lines are Band 1 or 2. Guidance lines are Band 3. Reference lines (forms, links, phone numbers) take the band of the claim they support and are checked against the official page.

## 2. Particularity: how closely the answer fits one person

| Level | Meaning | Example |
| --- | --- | --- |
| P0 | General information about the law or process. No facts about the reader. | "A summons starts the clock on a response." |
| P1 | Conditional: "if your situation is X, then Y", stated across the common situations. | "If you were served by mail, the days run differently." |
| P2 | Applied to inputs the reader gives, only through tools that refuse unclear inputs. | A deadline calculator or personal dated checklist from a service date and method. |
| P3 | A recommendation for this person's case. | "You should settle." |

Rules: P0 to P2 may be released. P3 is never released (Framework Spec). The Oct 31 rule "stop at conditional guidance (level 2)" is read as P1, and P2 only for tools that refuse unclear inputs *(inferred; Andy to confirm what "level 2" meant)*.

## 3. Release modes: who may see an item, and under what conditions

| Mode | Meaning | Source |
| --- | --- | --- |
| A | Public information. | Framework Spec |
| A* | Public with conditions (stated limits, warnings, a named reviewer). | Framework Spec |
| B | Member-only, supervised use (for example legal aid staff). | Framework Spec |
| C | Internal only: drafts, tests, research. Not released to anyone outside the project. | *(inferred; Framework Spec lists C without defining it)* |
| Refer | No content released; the item is a hand-off to a lawyer or legal aid. | *(inferred)* |

A contributor sets a release ceiling per item. A public build may never include an item above its ceiling (Framework Spec, test T9).

## 4. Allowed combinations (the guardrail)

| Band | Highest particularity | Highest release | Needs before release above C |
| --- | --- | --- | --- |
| 1 | P2 (calculators) | A | Source-read; harm flag if it involves a deadline, waiver or signature |
| 2 | P1 | A | Source-read, adversarial review; conflicts shown as Lawyers differ |
| 3 | P1 | A* | Attested by a named attorney; conditional wording; harm flag |
| 4 | none | Refer | Nothing but the hand-off text |

Today's pilot: no attorney has reviewed any item, so nothing is Attested. Band 3 items are therefore not releasable beyond C, and the pilot's stance remains "ready to show, not ready to use".

## 5. Open questions for Andy
1. Does this match the Oct 31 intent, especially splitting old Band 2 into Bands 2 and 3?
2. What did "level 2" mean: P1, P2, or something else?
3. Are release modes C and Refer defined as above?
4. Should the three-band docs be updated, or kept as history with a pointer here?
5. Should I classify D-01 to D-15 by band, particularity and release mode as a first test of this spec?
