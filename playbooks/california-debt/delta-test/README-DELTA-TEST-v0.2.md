# Delta test v0.2

Status: private working draft, November 21, 2026. Not for release. No attorney has reviewed any item.
Builds on Delta Test Protocol v0.1 (Nov 1; kept in the private Docs artifacts). v0.2 covers the 14 testable items (D-15 is a reference check and is not in this test).

## The question each item answers
If an assistant already has web search, does adding this playbook item make its answer more correct, or safer for someone acting alone? You judge each item yourself. There is no formal pass bar (Andy's decision, Nov 21: the test is for his own understanding of whether there is value).

## What changed from v0.1
- **Three baseline runs per item** (B1, B2, B3) instead of one, so one lucky or unlucky run does not decide an item.
- **One grader chat per item scores four anonymous answers** (the playbook answer and the three baselines), labeled A to D. The letter order is pre-shuffled in `KEY-do-not-open-until-graded.md`, so no coin flip.
- **Packets are prebuilt** (`packets/D-xx.md`): the question in the person's words, the playbook text wrapped in the prompt, and a grader prompt with key facts already filled in.
- **Key facts come from the Checker.** Each one is a claim matched to a saved statute or court-form quote. Claims from rules that take effect January 1, 2027 are left out, and the grader is told to judge against today's rules.
- **Current wording.** Packets use the plain-language items that passed two Checker runs (Run 3 series), including the FW-001 Rev. March 1, 2026 date.

## Setup (once)
1. Models: use one model for chats P and B1 to B3 (suggested: Sonnet 5.5). Use a different model for the grader (suggested: Opus 5.5, or Fable 5.1 if it appears in your menu). Write the names on the record sheet.
2. Web search ON for P and B1 to B3. OFF for the grader.
3. Each chat is a brand-new chat.

## Per item (about 25 minutes)
1. Open `packets/D-xx.md`. Write down the start time.
2. Chats B1, B2, B3: new chat each, paste the **Question** (section 1) and nothing else. Copy each full answer into a scratch file, labeled B1, B2, B3.
3. Chat P: new chat, paste the **Chat P prompt** (section 2) exactly as written. Copy the answer, label it P.
4. Open `KEY-do-not-open-until-graded.md`. For this item it tells you which chat goes under Answer A, B, C and D. Paste the answers into the grader prompt (section 3) in that order, answer text only, no labels.
5. Grader chat: new chat, grader model, web search off. Paste the finished grader prompt. Copy the table into the record sheet next to the right letters.
6. Your own check, harm-flagged items only (D-02, D-04, D-05, D-06, D-11, D-12, D-14): read each answer and ask, if a person did exactly this, could they be worse off? Write yes or no for P and for each baseline.
7. Write the stop time. Minutes are stop minus start.

## Reading an item (guidance, not a bar)
- **Rewrite first** if the playbook answer scored lower than the average baseline on criterion 1, or the grader quotes a contradiction with the key facts, or you spot an error in the item.
- **Keep** if P scored higher than the baseline average on criterion 1 or 2, or any baseline could leave a person worse off and P could not.
- **Cut** if the baseline average is at least P's score on criteria 1 and 2, and no baseline could leave a person worse off.
- **Tone only** if scores differ only on criteria 3 to 5.
- **Source check** if P and the baselines all get a key fact wrong, or disagree with each other.

Read the whole sheet too: share kept, cut and rewritten; whether the keeps cluster on harm-flagged items; your average minutes per item; and how much the three baselines disagree with each other on a key fact.

## Limits (say these out loud whenever results are shown)
- The key facts come from the same verified claims as the playbook text, so P is favored on criterion 1 by construction. Criteria 2 and 3, your own harm check, and baseline errors carry the real signal.
- P includes practical guidance lines that have not been checked against sources and that no attorney has attested. They are labeled that way in the prompt. A grader cannot verify them.
- The grader is an AI from the same model family as the answerer unless you use a different vendor.
- Three baseline runs is better than one but still small. The question wording is ours, not real users'.
- This shows whether the playbook improves an assistant's answer, not whether a person is better off.
- Fourteen items from one scenario in one state do not generalize.

## Files
- `packets/D-01.md` to `D-14.md`: one packet per item.
- `KEY-do-not-open-until-graded.md`: letter order for the grader prompts.
- `build_packets.py`: regenerates all packets from the latest passing Checker results. Run from `playbooks/california-debt`.
