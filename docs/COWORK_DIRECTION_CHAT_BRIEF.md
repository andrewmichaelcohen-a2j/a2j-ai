# Cowork Direction — CLAUDE_CHAT_BRIEF.md (the one-file handoff to Claude Chat)

**For:** Cowork · **From:** Andy (planning with Claude) · **Date:** 2026-06-24
**Lane:** GREEN (build + maintain). It's a derived/concatenated artifact from docs Cowork already writes — no new judgment, no immutables touched.

**Purpose:** Claude Chat cannot read the repo or any of Cowork's files automatically — each chat session starts fresh and sees only what Andy uploads. Today that means Andy hand-picks several living docs every session. This direction collapses that to **one file, one filename, always current**: a rolling brief Cowork regenerates each morning so Andy's entire Claude-Chat handoff is a single upload (on top of the stable docs that live in the Claude Project).

> This brief is a *handoff/orientation* artifact, NOT a new source of truth. It is concatenated/summarized from the canonical living docs; those remain authoritative. If the brief and a canonical doc ever disagree, the canonical doc wins and the brief is regenerated.

---

## OUTPUT
- **Path:** `docs/CLAUDE_CHAT_BRIEF.md`
- **Filename never changes** (so Andy always grabs the same file; no "which version?").
- **Regenerated:** every morning-report cycle (8 AM task), immediately AFTER the canonical docs are updated — so the brief always reflects the just-finished cycle.
- **Length cap:** target ≤ ~1,200 words / ≤ ~2 pages. It's an orientation layer, not a re-dump. Link/point to canonical docs for depth rather than pasting them whole.

---

## CONTENTS (in this order)

**0. Header (3 lines)**
- Generated timestamp; "Rolling handoff for Claude Chat — orientation only, canonical docs are authoritative."
- Current OS state one-liner (e.g. "Direction A live · B survey in progress · C not started").
- The single most important thing right now (one sentence — e.g. "Overnight runs BLOCKED on macOS FDA grant").

**1. WHERE WE ARE (≤150 words)**
A plain-language status paragraph: what's complete, what's actively running, what's the current frontier. Pulled/summarized from PROJECT_STATE_OF_RECORD. No tables here — prose, so Claude Chat can orient in 20 seconds.

**2. DECISIONS WAITING ON ANDY (the RED list — most important section)**
Every open RED item, each as: the question + the options + where it's recorded. Split:
- **RED-interpretive** (genuine legal judgment — for the attorney/Claude-strategy discussion)
- **RED-strategic** (project/process forks, blockers needing an Andy action)
Include current BLOCKED items with their named blocker + what unblocks them. If none, say "No open REDs."

**3. WHAT EXECUTED SINCE LAST BRIEF (the GREEN digest, ≤200 words)**
Terse bullet digest of the last cycle's DAILY_CHANGELOG GREEN actions — what ran, what was fixed, tests passing. Skimmable; not the full changelog. Note anything YELLOW awaiting ratification.

**4. METRICS MOVEMENT (≤120 words)**
Key numbers this cycle vs. last, from VALIDATION_METRICS_LEDGER: latest validation rates (two-rate where applicable: method vs. overall), Krippendorff's α with n (and an explicit "statistically unreliable below n≈X" note when small), golden-set score once it exists. Just the deltas that matter.

**5. QUEUE SNAPSHOT (≤120 words)**
NOW / depth of NEXT / what's BLOCKED — condensed from WORK_QUEUE. Enough that Claude Chat knows what's coming without opening the full queue.

**6. POINTERS (not contents — just where to look)**
A short list: "For depth, upload/open: PROJECT_STATE_OF_RECORD (full status), VALIDATION_METRICS_LEDGER (run-by-run), HUMAN_REVIEW_QUEUE (RED-interpretive detail)." So Andy knows the *next* file to grab if a session goes deep — without bloating the brief.

---

## RULES
- **Derive, don't invent.** Every line traces to a canonical doc. The brief adds orientation/summary, never new facts or decisions.
- **Honesty carries through.** Small-n caveats, two-rate splits, single-model (SM) flags, "process credibility not proven outputs" — these survive summarization. Never let compression inflate a claim (e.g. don't round an α up, don't drop the n).
- **RED items are never dropped for brevity.** Section 2 is complete even if it pushes length; trim sections 3–5 first.
- **Stable docs are NOT included.** Direction A/B/C, the handoff, CLAUDE.md, reporting direction — those live in the Claude Project (uploaded once, persistent). The brief covers only what *changes*. Don't paste the directions in.
- **Regeneration is idempotent.** Overwrite the same file each cycle; no dated copies pile up.

---

## REPORT BACK (first build)
1. Confirm `docs/CLAUDE_CHAT_BRIEF.md` is generated at the end of the 8 AM cycle, after canonical docs update.
2. Paste the first generated brief into the morning report so Andy sees the format and can adjust length/sections.
3. Confirm length is within cap and all open REDs are present.

---

*Cowork Direction — CLAUDE_CHAT_BRIEF.md · CJaC · 2026-06-24 · One file, one name, always current. Orientation layer over the canonical docs — Andy's entire Claude-Chat handoff in a single upload.*
