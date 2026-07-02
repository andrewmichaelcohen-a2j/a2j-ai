# CJaC — Rolling Handoff for Claude Chat

**Generated:** 2026-07-01 (session 2 — Playbook Architecture Directive; Stage 1 in progress)  
**Orientation only — canonical docs are authoritative. If this brief and a canonical doc disagree, canonical doc wins.**  
**OS state:** Direction A live · Direction B: first pilot score 3/5=60% (held-out burned) · Direction C not started · Playbook Architecture Directive ACTIVE (Stage 1 in progress).  
**Most important thing right now:** Playbook Architecture Directive received (2026-07-01). Architectural response to 60% pilot score: restructure encoding around playbook-as-unit with `determinate`/`open_textured` strategy tags, bounded-reasoning procedures, and Validated Resources Registry. Stage 0 (pilot close) complete. Stage 1 (registry + docs) 4/6 items done this session — 2 pending research tasks. Andy needs to ratify strategy tags (RED gate) before Stage 2 encoding proceeds. Gemini credits still depleted.

---

## 1. Where We Are

All 51 v2 rules files are at AUTOMATED-CHECKS-PASSED (schema, L1 retrieval, L3 consistency, L5 cross-jurisdiction). The retaliation holdings (v3) pipeline has been the active overnight work; Direction B (golden-set scoring) has now produced its first real score.

**Completed modules:** Notice pay-or-quit (51 states, L2 complete — 4 L7 open: MO/ND/MD/GA). Service method-rules (51 states, L2 complete — 2 L7 open: DC/NM). Procedural defects (51 states × 4 defects — 22 L7 open). Remaining defenses elements (51 states — 0 L7). Retaliation elements (51 states — 15 L7 open). State overlays (22 cite-check items).

**Retaliation holdings (v3) — current frontier:** Cumulative MV = 25 cases across 11 states. CI = 3. RC = 6 in attorney queue. VT retry (run 1c7f0772) ran 2026-07-01 — both VT cases had text retrieved but Gemini 429 blocked Check C. KS, SC, NV: confirmed CL coverage gaps. 82 unretried transient-failure PR-class cases remain. All overnight runs blocked until Gemini credits restored.

**Direction B — CA-notice pilot v1 complete:**
- **Held-out score: 3/5 = 60.0%** (held-out set now burned — cannot re-score same items)
- Non-held-out: 7/11 = 63.6%. Overall: 10/16 = 62.5%.
- GPT-only run (Gemini 429 depleted on all items).
- All 6 misses are rules-gap, not model-wrong. Direct fix: encode 6 missing rules.
- Output: `rules/validation/scorer/output/ca_notice_score_2026-07-01.json`

**Architecture memo ingested (2026-07-01):** `docs/CJaC_Architecture_and_Roadmap_Memo_20260701.md`. Jurisdiction-resolution principle added to `Decision_Logic_Briefing_for_Claude.md` (Section 9). Direction D logged in WORK_QUEUE HORIZON. LA RSO+JCO overlay golden set queued as first local-overlay build.

---

## 2. Decisions Waiting on Andy (RED List)

### RED-strategic

**⚠️ Gemini API prepayment credits depleted — ALL overnight runs blocked**
- Top up at [AI Studio](https://aistudio.google.com/projects) → billing
- Once restored: Cowork re-queues VT retry (text already retrieved; only Check C needed)

**Strategy tag ratification (RED gate — Stage 2 cannot start without this)**
- PLAYBOOK_SPEC.md defines `determinate`/`open_textured` element tags as set by human attorney
- PLAYBOOK_SPEC.md section 9 includes DRAFT strategy tags for 4 CA notice elements
- 5 of 6 pilot gaps proposed as `determinate`; 1 (partial rent acceptance) proposed as `open_textured`
- **Andy must review and ratify these tags before Stage 2 encoding proceeds**
- PLAYBOOK_SPEC.md is the place to review and correct; flagged YELLOW for ratification

**Skills/tools decision (YELLOW — Andy's direction)**
- No "legal-analysis" or "issue-spotting" skills found by those names in environment
- `legal:*` plugin skills (risk-assessment, review-contract, etc.) available but not integrated into CJaC
- Lawvable MCP (`lawvable_search_skills`) unexplored — may have eviction legal skills
- **Andy: integrate `legal:*` skills into playbook element analysis workflow? Explore Lawvable?**

**KS/SC/NV CL gap strategy (YELLOW-carry):** No CL-indexed cases even with broad fallback. Options: (a) Descrybe MCP; (b) Track A (statute-direct). Andy's call.

### RED-interpretive (attorney/legal judgment needed)

**Retaliation holdings — 6 RC (re-characterize from primary source):**
[NV-RET-HOLD-RC-01] Wright v. Brady · [NY-RET-HOLD-RC-02] Ellis v. Oceanhill · [AK-RET-HOLD-RC-01] DeNardo v. Maassen · [CO-RET-HOLD-RC-01] Sladek v. dePlomb · [CT-RET-HOLD-RC-01] TOV Realty v. Suarez · [WV-RET-HOLD-RC-02] Criss v. Salvation Army Residences

**Notice module — 4 L7:** [MO] §535.020 notice or precondition? / [ND] §47-32-02 ripening or notice? / [MD] 10d vs. no notice / [GA] 3d after demand or file immediately?

**Service module — 2 L7:** DC and NM (persistent API failure).

**Procedural defects — 22 L7:** [PROC-DEF-L7-01]–[PROC-DEF-L7-22].

**Retaliation elements — 15 L7:** See HUMAN_REVIEW_QUEUE.

**CI cheap confirm lane:**
- [NY-HOLD-CI-01] Baer v. Huggins (41 Misc. 3d 605) — pull from Fastcase
- [NM-HOLD-CI-01] Casa Blanca Mobile Home Park v. Hill — pull from Fastcase

### YELLOW items awaiting ratification

- **6 CA-notice rules encoding** — proposed in WORK_QUEUE NEXT; Andy ratify order/scope
- CO W.W.G. Corp.: court declined to decide if retaliation doctrine exists — file flagged
- GA notice file change [NOTICE-L2-06]: days=3→null applied; ratify or override
- Cross-jurisdiction rejections (Markese/Robinson, Batch 4): ratify

---

## 3. What Executed Since Last Brief (GREEN Digest)

**Session 2 (Playbook Architecture Directive):**
- **Directive filed** — `docs/CJaC_Playbook_Architecture_Directive_20260701.md` reconstructed from Andy's message and saved to docs/
- **`docs/ARCHITECTURE.md` created** — one-pipeline playbook architecture; element decomposition; strategy tags; confidence tiers; jurisdiction-resolution; 7-layer stack; bucket taxonomy
- **`docs/PLAYBOOK_SPEC.md` created** — playbook unit schema with full element schema, tag definitions, confidence tiers, interaction schema, source IDs, and partial CA pay-or-quit example (4 elements encoding 4 of 6 pilot gaps)
- **`docs/VALIDATED_RESOURCES_REGISTRY.md` created** — 13 sources with tiers, currency risk, coverage, status; 4 YELLOW flags raised (Benchguide unlocated, `legal:*` skills unintegrated, Lawvable unexplored, Descrybe unauthenticated)
- **WORK_QUEUE updated** — Stage 1 progress table; Stage 2 plan in NEXT (element encoding table with `open_textured` correction for partial-payment item)
- **DAILY_CHANGELOG updated** — full Stage 1 GREEN/YELLOW entries

**Session 1 (pilot run):**
- **CA-notice pilot live run** — first real score: held-out 3/5=60%, non-held-out 7/11=63.6%. Output: `ca_notice_score_2026-07-01.json`. GPT-only (Gemini depleted). Plumbing bug fixed first (dotenv `parents[4]` → `parents[3]`).
- **Architecture memo ingested** — `docs/CJaC_Architecture_and_Roadmap_Memo_20260701.md`. Section 5 items actioned: jurisdiction-resolution principle added to Decision_Logic_Briefing; Direction D logged in HORIZON; LA RSO+JCO overlay golden set queued; reporting scope note added to METRICS_LEDGER; benchguide source lane noted.
- **4 excluded items logged** as downstream work: CA-NOT-09 (open-textured), CA-NOT-15 (retaliation), CA-NOT-17 (service), CA-NOT-19 (LA overlay).
- **VT retry (run 1c7f0772)** — both cases text-retrieved, Gemini 429 blocked Check C. Not attorney items. Re-queues when credits restored.

---

## 4. Metrics Movement

| Metric | Prior (2026-07-01 morning) | This cycle | Notes |
|--------|--------------------------|------------|-------|
| Cumulative retaliation MV | 25 | **25** | No change — Gemini blocked |
| Cumulative CI | 3 | **3** | No change |
| Cumulative RC (queue) | 6 | **6** | VT not added (API failure) |
| **Direction B held-out score** | n/a | **3/5 = 60.0%** | **First real score; SM-GPT; held-out burned** |
| Direction B non-held-out | n/a | **7/11 = 63.6%** | |
| Direction B overall | n/a | **10/16 = 62.5%** | |

---

## 5. Queue Snapshot

**NOW:** Stage 1 — 4/6 items done. 2 pending research (CA Benchguide locate; Lawvable MCP explore). Gemini credits depleted — no overnight jobs can run.

**NEXT (immediate — no API needed):**
1. CA Benchguide: locate, verify currency, add to registry (Stage 1 carry-over)
2. Lawvable MCP: `lawvable_search_skills` for eviction skills (Stage 1 carry-over)
3. Stage 2: Andy ratifies strategy tags in PLAYBOOK_SPEC → encoding begins
4. Encode 6 pilot-gap elements in CA notice playbook (5 `determinate` + 1 `open_textured`)
5. Draft fresh CA-notice golden set v0.2 → freeze → score

**BLOCKED:** Gemini credits (all overnight runs); Stage 2 encoding (RED gate — Andy ratifies strategy tags first); VT retry (Gemini credits).

**HORIZON:** LA RSO+JCO overlay golden set · Stage 3 (retaliation bounded-reasoning proof) · Direction D (3 components) · Jurisdiction-resolution architecture · Direction C (gates: stable score + Andy sign-off).

---

## 6. Where to Look for Depth

- `docs/ARCHITECTURE.md` — **NEW** one-pipeline playbook architecture (authoritative for architectural questions)
- `docs/PLAYBOOK_SPEC.md` — **NEW** playbook unit schema; element structure; strategy tag definitions; CA notice example
- `docs/VALIDATED_RESOURCES_REGISTRY.md` — **NEW** source catalog with reliability ratings and status
- `docs/CJaC_Playbook_Architecture_Directive_20260701.md` — **NEW** Andy's July 1 directive
- `docs/PROJECT_STATE_OF_RECORD.md` — full validation status
- `docs/VALIDATION_METRICS_LEDGER.md` — run-by-run metrics; Direction B pilot-score section
- `docs/HUMAN_REVIEW_QUEUE.md` — all RED items
- `docs/WORK_QUEUE.md` — full queue with blockers
- `docs/CJaC_Architecture_and_Roadmap_Memo_20260701.md` — jurisdiction-resolution, benchguide, Direction D
- `rules/validation/scorer/output/ca_notice_score_2026-07-01.json` — pilot run output

---

*CJaC · CLAUDE_CHAT_BRIEF.md · Rolling handoff — overwritten each morning report cycle. Copyright 2026 Andrew M Cohen. Apache 2.0.*
