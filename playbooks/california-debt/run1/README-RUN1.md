# Run 1: seeded-error check (Checker)

Purpose: test whether a second-vendor model, reading only the saved source text, catches two planted errors (D-06-SEEDED and D-11-SEEDED) and does not give a Source-read label to anything its sources do not support. Plan and pass criteria are in the Agent Roster and Pilot Plan.

Files
- `checker.py`: the Checker. Python 3 standard library only. With no flags it only estimates cost.
- `setup-key.sh`: saves your OpenAI key to a private file, `~/.config/cjac/openai_key` (outside the repo, readable only by you).
- `items.json`: the 15 prototype items plus 2 seeded first-draft wordings. The model sees blinded references and cannot tell which are seeded.
- `../sources/`: saved statute text with official links and dates read. The Checker sees only this text.
- `results/`, `spend-log.tsv`, `decision-log.tsv`: written by the script.

One-time setup (works from any folder; copy each line exactly)
1. Create a key at platform.openai.com/api-keys ("Create new secret key", name it cjac-pilot). Click its copy button.
2. `bash ~/Developer/a2j-ai/playbooks/california-debt/run1/setup-key.sh` then paste the key and press Return.
3. `python3 ~/Developer/a2j-ai/playbooks/california-debt/run1/checker.py --check-key`  (free; prints OpenAI's reason if it rejects the key)

Run
4. `python3 ~/Developer/a2j-ai/playbooks/california-debt/run1/checker.py`  (free dry run with cost estimate)
5. `python3 ~/Developer/a2j-ai/playbooks/california-debt/run1/checker.py --run --only D-11-SEEDED`  (one real call, about 25 cents)
6. `python3 ~/Developer/a2j-ai/playbooks/california-debt/run1/checker.py --run`  (full run, about $3 to $4 expected, hard stop at the budget)
7. `open ~/Developer/a2j-ai/playbooks/california-debt/run1/results/RESULTS.md`

Never put the key in the repo. Prices in the script are third-party reports of OpenAI's Nov 17, 2026 prices; verify them on OpenAI's pricing page.
