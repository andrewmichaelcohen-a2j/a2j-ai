# Security

## Reporting a credential leak or vulnerability

If you find a leaked credential, a security vulnerability, or anything that looks like it shouldn't be public in this repository, email andrewmichaelcohen@gmail.com directly rather than opening a public issue. If it's a live credential, assume it's compromised the moment it's visible in a public repo's history — the fix is rotation, not just removal (git history retains old commits regardless of later deletions).

## What's in place

- **`.gitignore`** excludes `.env` and common local-secret file patterns.
- **`scripts/git-hooks/pre-commit`** blocks common credential patterns (API key formats for Anthropic, OpenAI, Google, GitHub, Slack, AWS; PEM private-key blocks; database connection strings with embedded credentials) from being staged. Activate once per local clone: `git config core.hooksPath scripts/git-hooks`.
- **GitHub secret scanning and push protection** — repo-level settings enabled via the GitHub UI (Settings → Code security and analysis), providing a platform-level backstop independent of the local hook.
- **Full-history secret scan** — see `docs/SECRET_HYGIENE_SCAN_20260724.md` for the most recent full-repository, full-history scan (two independent tools plus a manual pattern sweep; zero credentials found as of that date).

## API keys used by this project

The validation harness and scorer (`rules/validation/harness.py`, `rules/validation/scorer/ca_notice_scorer.py`, `rules/validation/scorer/gemini_health_check.py`) call the Anthropic, OpenAI, and Google Gemini APIs using keys read from environment variables (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`) only — never hardcoded. These run only in Andy's local environment with real keys; nothing in CI or automation should ever need a real key committed anywhere.

## Scope note

This repository is **legal information, not legal advice**, and its rules files are validated against the discipline described in `docs/VALIDATION_PHILOSOPHY.md`. This SECURITY.md concerns the *engineering* posture (secrets, infrastructure) — see `docs/COWORK_DIRECTION_ENG_HARDENING_20260724.md`-descended work for the broader hardening effort (CI, schema validation, scorer calibration).
