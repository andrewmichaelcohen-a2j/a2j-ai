# How Andy Runs the Demo

*Three steps. Voice-mode-ready — no screen-reading required once the skill is loaded.*

## Before you start

Make sure `docs/DEBT_DISAGREEMENT_QUEUE.md` and the latest run under `rules/debt/validation/runs/` are current (run the live corroboration script yourself beforehand, or ask Claude to report the last run's numbers). You need real numbers in hand before you open your mouth — see the claim-language card.

## The three steps

**1. Open with the framing sentence.** Say it verbatim, out loud, before anything else:

> "This is a demonstration system. Its content is machine-corroborated against cited law — three independent AI models, citations verified against live sources — and not yet attorney-validated. The attorney-validation layer is designed and is what this project is building toward."

**2. Describe a person's situation, in plain language, to whoever's driving the conversation with Claude.** You don't need to name a scenario or a node ID — just describe the fact pattern naturally, the same way a person would describe it to you. The `consumer-debt-validation` skill picks up from there: it asks the same intake questions a person would actually be asked (state, whether they've been served, debt type, etc.), then answers with the applicable rule, its tier (DRAFT or CORROBORATED), and its citation. The five prepared scenarios in `scripts/corroboration/scenarios.json` are good starting points if you want a reliable path (TX or CA collection-suit SOL/answer, pre-suit FDCPA validation rights, wage garnishment, or the Band 3 default-judgment refusal-boundary case) — but any fact pattern touching the 18-node demo corpus works.

**3. Close with the numbers, both together, from the last real run.** "X% three-model grounded agreement across the demo corpus, and Y of Z scenarios passing against corroborated rules." Read them off the last live run's output, not from memory. If someone pushes on accuracy or reliability, redirect to the claim-language card's "how do you know it's right" answer — the mechanism, not a confidence number.

## If something goes off-script

If the skill hits a node below CORROBORATED tier, or a fact pattern outside TX/CA, or any genuinely discretionary judgment call (Band 3): let it say so plainly. That's the system working as designed, not a failure to paper over.

---
*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*
