# Debt-track grounded-corroboration runner

Per `DEBT_PROJECT_ARCHITECTURE_SPEC.md` §3(a)/(b)/(d) and the 2026-08-26 "Phase A Unblock" and
"Concept Demo First" directives. This is the tool that upgrades DRAFT-tier rules to
CORROBORATED-tier evidence — it needs live API keys, so **it runs on your machine, not Cowork's.**

## What it does, in plain terms

For every DRAFT-tier rule in `rules/debt/`, it asks three different AI companies' models
(Anthropic, OpenAI, Google) to independently work out the answer *using only the actual law
text already cited in that rule* — not from what they already "know." A fourth AI call then
judges whether those three answers substantively agree (same rule, same deadline, same dollar
amount — ignoring differences in phrasing or which examples each one picked). If they agree,
and a live fetch of the cited web page confirms the quoted text is really there, and a fifth
pass trying to find edge cases that break the rule doesn't find one — the rule passes cleanly.
Anything that doesn't clear all three checks gets written up automatically in
`docs/DEBT_DISAGREEMENT_QUEUE.md` for you to look at, with the evidence attached. **It never
edits any rule file itself and never changes a tier — it only produces evidence for you to act
on.**

*(Methodology note, 2026-08-26: earlier versions of this runner used a mechanical
numeric/citation-fingerprint comparison instead of an LLM judgment call for this agreement
check. That was replaced after it produced three separate false-positive patterns in live use
— citation-reference noise leaking into the fingerprint, the word "one" as in "no one" being
misread as the numeral 1, and subsection cross-references like "Paragraph (b)(2)(ii)" not being
recognized as citation-shaped. The numeric fingerprint is still computed and recorded in the run
output as a secondary diagnostic, but no longer gates pass/fail. Known limitation: the judge
call uses the same Anthropic model that's also one of the three being judged — anonymized
[the judge is never told which analysis came from which provider] as a standard mitigation, but
not a full fix for self-preference bias. Worth watching for in the disagreement queue over
time.)*

It also reports two numbers used to decide when the concept demo is ready to show anyone (per
the 2026-08-26 directive): what fraction of the demo-corpus rules passed cleanly, and what
fraction of the 5 prepared demo scenarios have all their underlying rules passing. Both need to
be at least 90% before the demo goes in front of anyone, even a friendly audience.

## One-time setup

```
cd ~/Developer/a2j-ai
pip install -r scripts/corroboration/requirements.txt --break-system-packages
cp .env.example .env
```

Then open `.env` in any text editor and replace the three placeholder lines with your real keys:

```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
```

Save the file. `.env` is already gitignored — it will never be committed, never leaves your
machine.

## Step 1 — dry run (do this first, costs nothing)

```
cd ~/Developer/a2j-ai
python3 scripts/corroboration/run_corroboration.py --dry-run --demo-corpus-only
```

This exercises the entire pipeline end to end with fake responses — no API keys needed, no
network calls, no cost. If it finishes and prints a `Demo-gate metrics` line with no Python
errors above it, the install is good and you're ready for a real run.

## Step 2 — first live batch (the demo corpus: federal + TX + CA)

```
cd ~/Developer/a2j-ai
python3 scripts/corroboration/run_corroboration.py --live --demo-corpus-only
```

This is the one on the critical path for the 2-3 week concept-demo target — the sooner this
runs, the sooner the schedule's one Andy-dependency clears. Takes a few minutes; prints progress
per node as it goes.

**Estimated cost: about $8 for the 18-node demo corpus** (federal spine + TX + CA), at roughly
$0.45/node — three grounded-derivation model calls, one agreement-judgment call, plus one
adversarial-generation call per node (bumped from $0.35 on 2026-08-26 to reflect the added judge
call). This is an estimate based on typical token counts for this kind of prompt, not a
guarantee; actual API pricing and your specific usage may vary. The script has a hard
`--budget-cap` (default $15) and will refuse to start a node that would push projected spend
over it — it stops cleanly rather than silently overspending.

## Step 3 — everything else (optional, once the demo corpus is corroborated)

```
python3 scripts/corroboration/run_corroboration.py --live
```

Runs all 37 DRAFT nodes (adds UT/AZ/NY). Estimated cost: about $17.

## Other useful flags

- `--nodes NODE-ID-1,NODE-ID-2` — spot-check one or a few specific rules instead of a whole batch.
- `--budget-cap 5.00` — lower or raise the hard spending cap for a run.
- `--skip-citation-check` — skip the live web-fetch citation check (offline testing only; don't
  use this for a real corroboration run, since citation verification is one of the three checks
  a rule needs to pass).

## What happens to the results

- A full JSON record of the run lands in `rules/debt/validation/runs/run_<timestamp>.json` —
  every model's raw answer, every citation check, every adversarial finding, timestamps, and the
  SHA256 of every file/node touched (so a run can always be traced back to the exact content it
  ran against).
- Anything flagged gets appended to `docs/DEBT_DISAGREEMENT_QUEUE.md`, same append-only pattern
  as the eviction line's `docs/HUMAN_REVIEW_QUEUE.md` — work through it top to bottom, fill in
  the Resolution/Resolved-by/Date fields, nothing else in that file gets touched automatically.
- Nothing is promoted from DRAFT to CORROBORATED automatically — that's still your call (or the
  next Cowork session's, once you've told it a run is done and you've reviewed the disagreement
  queue). The run's JSON output flags which nodes are clean-pass candidates for promotion.

## What this runner does *not* do (so nothing here overpromises)

- **Mutation testing** (spec §3c) isn't built into this yet — it's a separate, later pipeline
  stage. A node passing this runner cleanly has strong evidence behind it, but not literally
  every check the spec eventually calls for at full CORROBORATED rigor.
- **The statistical sampling audit / attorney certification** (Phase D, spec §3(e)-(g)) is a
  separate, later, human-driven stage — this runner produces machine evidence only.
- This runner never touches a rules file's content or tier field. All promotion decisions stay
  with you.

*Copyright 2026 Andrew M Cohen. Apache 2.0.*
