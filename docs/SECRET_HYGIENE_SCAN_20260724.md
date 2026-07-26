# Secret Hygiene Scan — 2026-07-24

**Directive:** `COWORK_DIRECTION_ENG_HARDENING_20260724.md`, Task 1. Executed same-day on receipt, ahead of the docs-final gate on other pending work, per the directive's own urgency marking.

## Scope

Full repository, full git history (all 131 commits on `main` at scan time, not just HEAD) — the repo is public and the scorer runs with real API keys, so a leak at any point in history is live risk even if the current HEAD looks clean.

## Method — two independent tools plus a manual sweep

1. **trufflehog3** (v3.0.10), run against a fresh clone with `--depth 200` (exceeds the 131-commit total, so full history is covered), pattern checks and entropy checks both enabled, all branches.
2. **Manual regex sweep** across the complete `git log -p --all` output (333,306 lines), independently written, checking for: Anthropic keys (`sk-ant-`), OpenAI-style keys (`sk-`), Google API keys (`AIza`), GitHub tokens (`ghp_`, `gho_`, `github_pat_`), Slack tokens (`xox[baprs]-`), AWS access keys (`AKIA`), PEM/private-key blocks (`-----BEGIN ... PRIVATE KEY-----`), and database connection strings with embedded credentials (`mongodb://`, `postgres://` with a `user:pass@` segment).
3. **File-presence check**: `git log --all --diff-filter=A --name-only` filtered for `.env`, `secrets.*`, `credentials`, `id_rsa`, `.pem`, `.key` — i.e., was a secret-shaped *file* ever added, even if later deleted (deletion doesn't remove it from history).

## Results

**Zero real credentials found**, across all three checks.

- trufflehog3: 247 findings, **all** `high-entropy` / MEDIUM severity, **zero** pattern-rule (HIGH severity) hits. Manually sampled and confirmed: every flagged string is a legitimate SHA256 hash the project generates on purpose — rules-file hashes (e.g. vProof1 `cc0cfab63ae1591e2b88…`, v3 `65f1d9a4…947c7d`), golden-set hashes, and per-row `_row_hash` values in scorer output JSON. High-entropy hex strings are exactly what a hash-verified-transparency project is supposed to be full of; none of the 247 is a credential.
- Manual regex sweep: **0 matches** for any of the credential-shaped patterns above.
- File-presence check: **no** `.env`, secrets, credentials, or private-key file has ever been added to the repository at any commit.

## What's already in place

- `.gitignore` already lists `.env` (confirmed current).
- Every API key reference in the codebase (`harness.py`, `ca_notice_scorer.py`, `gemini_health_check.py`) goes through `os.getenv` / `os.environ.get` — no hardcoded key ever found in current code, consistent with the history scan.

## What this scan adds

- `scripts/git-hooks/pre-commit` — a versioned pre-commit hook blocking the same credential patterns above from being staged. **Requires one-time activation per local clone:** `git config core.hooksPath scripts/git-hooks`. Not automatic from being committed — git doesn't run hooks from a tracked directory unless `core.hooksPath` points there.
- `SECURITY.md` — states the posture and how to report a future finding.

## What Andy still needs to do (cannot be done from a commit)

**Enable GitHub secret scanning and push protection** — this is a repo setting in the GitHub web UI, not something a commit can turn on:
1. Go to `https://github.com/andrewmichaelcohen-a2j/a2j-ai/settings/security_analysis`
2. Under "Secret scanning," click **Enable**.
3. Under "Push protection," click **Enable**.

That's it — two toggles, a couple of minutes. Once on, GitHub scans every future push automatically and can block a push containing a detectable secret pattern before it ever reaches history — a second, platform-level backstop on top of the local pre-commit hook.

## Rotation

Not applicable — nothing was found. If a future scan (or GitHub's own scanning, once enabled) finds something, the standing rule is: rotate the credential first, report, then remove from current files — never just delete-and-move-on, since git history retains the old value regardless.

---

*No rules file, golden set, or held-out data was touched by this scan — read-only investigation of git history and current files only.*
