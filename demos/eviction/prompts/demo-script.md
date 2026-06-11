# Eviction Demo — Recording Script v4
## Civil Justice as Code · ~5:30–6:00 minute Loom recording

*This is a recording guide, not a live session script. You're recording alone — no audience watching in real time. Speak naturally; this is a polished but conversational walkthrough.*

---

## SETUP — Do before hitting Record

Open and arrange these on your screen before you start:

| Tab / Window | What it is |
|-------------|-----------|
| **Cowork** | Active session, blank chat ready |
| **Browser Tab A** | Widget: `file:///Users/andrewcohen/Documents/GitHub/a2j-ai/demos/eviction/widget/RulesComparisonWidget.html` — pre-load on **CA** |
| **Browser Tab B** | GitHub: `rules/eviction/california/ca_eviction_v1.json` — open to the `notice_defects` section |

Record your **full screen** in Loom (Screen + Camera recommended — face in the corner adds warmth).

Have this script open on a **second monitor or device** — not on your recorded screen.

> **⚠️ IMPORTANT:** Scene 1 — do NOT type Maria's scenario into Cowork. Just narrate it. The first thing you type is the Scene 2 statute retrieval prompt.

---

## THE SCRIPT

---

### SCENE 1 — The Setup (0:00–0:35)
*Start on Cowork. Cowork is open and blank — nothing typed yet.*

**SAY:**
"I'm going to show you a working eviction-defense tool — built in three days, for essentially zero dollars, by a non-engineer attorney. And I want to walk you through the specific things that made it possible — because understanding how it was built is the whole point."

"Let's start with Maria. It's 10pm. She just found this taped to her door."

**SAY:**
"Maria Garcia. Los Angeles, California. She's lived in her apartment for 3 years. Tonight she received a 3-Day Notice to Pay Rent or Quit demanding $2,050 — $1,850 in rent, plus $200 in late fees. She has no lawyer. She has no idea whether this notice is valid."

"This is one of 3.6 million eviction filings a year. 95% of those tenants have no attorney."

---

### SCENE 2 — Live Statute Retrieval (0:35–1:30)
*Type or paste into Cowork:*
```
Use Legal Data Hunter to retrieve the current text of California Code of
Civil Procedure Section 1161 — specifically the requirements for a 3-Day
Pay or Quit notice for nonpayment of rent. Show me the key statutory language
and the source URL.
```

*While it loads:*

**SAY:**
"What's happening right now is the tool is making a live call to the California Legislature's website to retrieve the actual current text of CCP §1161. Not AI training data from months ago. The current statute."

*When output appears, point at the leginfo.legislature.ca.gov URL:*

**SAY:**
"That's leginfo.legislature.ca.gov — the Legislature's own website. That's what the infrastructure changed: from predictive to deterministic. Past AI guessed the law from memory. This one reads it live."

*Pause — let the statute be visible for 5 seconds.*

**SAY:**
"But here's what I discovered when I actually built this. Reading the statute isn't enough."

---

### SCENE 3 — The Case Law Gap (1:30–2:30)
*Stay in Cowork. Open a new chat or continue — then type:*
```
What does Orozco v. Casimiro, 121 Cal. App. 4th Supp. 7 (2004) hold about
late fees in California pay-or-quit eviction notices? What does that holding
mean for a notice demanding $1,850 rent plus $200 in late fees?
```

*While it loads:*

**SAY:**
"CCP §1161 says the notice must state 'the amount that is due.' But the statute text alone doesn't tell you whether late fees are included or prohibited. That answer comes from how California courts have interpreted the statute — specifically, a 2004 California appellate case called Orozco v. Casimiro."

*When output appears:*

**SAY:**
"Orozco held that late fees are void as liquidated damages under California law — and that including them in the demanded amount makes the entire notice defective. A good attorney would know this. But the AI, reading only the statute, would miss it."

"So I had a choice: I could reference this case in every query, every time. Or I could encode it — capture the doctrine as structured logic so the tool applies it automatically, deterministically, every time."

"That's the decision-logic rules layer. And that's where Civil Justice as Code starts."

---

### SCENE 4 — The Comparison Widget (2:30–3:30)
*Switch to Browser Tab A — the Comparison Widget, CA selected.*

**SAY:**
"I built a comparison tool that makes this concrete. Same notice, two approaches, side by side."

*Point to the LEFT panel:*

**SAY:**
"Left panel: AI with live statute retrieval — the same §1161 you just saw — but no rules file. No encoded doctrine. Result: no defects found. Zero."

*Pause.*

**SAY:**
"Right panel: same AI, same statute, plus the decision-logic rules file — with Orozco encoded as explicit if-then logic. Result: one defect found. The notice is flagged as INVALID, with the citation right there."

*Point to the statute citation showing Orozco:*

**SAY:**
"That's the difference. The statute tells the AI what the law says. The decision logic — built from cases like Orozco — tells it what the law requires."

*Point to the safety disclaimer:*

**SAY:**
"And notice: 'legal information, not legal advice — verify with an attorney.' That's not a disclaimer added at the end. It's built into the architecture."

---

### SCENE 5 — The Rules File (3:30–4:15)
*Switch to Browser Tab B — GitHub showing ca_eviction_v1.json, scrolled to the `notice_defects` section.*

**SAY:**
"Here's the file that made the difference."

*Pause on the `includes_late_fees` entry with the Orozco citation.*

**SAY:**
"This entry: defect — includes late fees. Result — INVALID. Statute — CCP §1161(2), see Orozco v. Casimiro."

"This rule didn't come from reading the statute in isolation. It came from synthesizing the statute with how California courts have interpreted it. The AI encoded that synthesis as auditable logic: if the notice includes late fees, the result is INVALID."

"I drafted this file in a few hours. A licensed California tenant attorney needs to confirm the synthesis is accurate — that the encoded doctrine reflects how the law actually applies. That attorney review is the first item on the validation roadmap, and it's the reason the file carries a DRAFT watermark."

---

### SCENE 6 — Portability (4:15–4:55)
*Switch back to Browser Tab A — Comparison Widget. Click the TX button.*

**SAY:**
"Watch what happens when I switch to Texas."

*Let both panels re-render.*

**SAY:**
"Same AI model. Same structure. Different rules file. Texas has no just-cause requirement, so the analysis is shorter — the law is simpler. That's what portability looks like. Not 50 separate tools reinvented from scratch. One reasoning engine, 50 rules files."

*Click NY.*

**SAY:**
"New York: 14-day notice requirement under RPAPL §711(2), amended by the Housing Stability and Tenant Protection Act of 2019. Different law, same architecture. Maria's situation, across three states, from one tool."

---

### SCENE 7 — The Bridge / Close (4:55–5:45)
*Face cam if using it, or stay on screen.*

**SAY:**
"Let me summarize what you just saw."

"One non-engineer attorney. Three days. No software budget. A working multi-state eviction defense tool — with live statutory retrieval, case-law-grounded decision logic, safety guardrails, and citations."

"That was possible because the infrastructure exists. Anthropic built it. I connected it."

"What doesn't exist yet — at any scale — is the validated rules library. The decision-logic layer that captures not just what statutes say, but what courts and practitioners have determined they require. For eviction. For debt collection. For benefits appeals. Across all 50 states."

"The question isn't whether it can be built. I just showed you it can. The question is whether we build it with rigor — validated, open-source, with published accuracy standards — so that when Maria uses a tool like this, she can trust the answer."

*Stop recording.*

---

## TIMING GUIDE

| Scene | Content | Target |
|-------|---------|--------|
| 1 | Setup + Maria | 0:00–0:35 |
| 2 | Live statute retrieval | 0:35–1:30 |
| 3 | Case law gap (Orozco) | 1:30–2:30 |
| 4 | Comparison widget | 2:30–3:30 |
| 5 | Rules file (GitHub) | 3:30–4:15 |
| 6 | Portability (TX + NY) | 4:15–4:55 |
| 7 | Bridge / close | 4:55–5:45 |
| **Total** | | **~5:30–6:00** |

---

## COWORK PROMPTS (copy-paste ready)

**Scene 2 — Statute retrieval:**
```
Use Legal Data Hunter to retrieve the current text of California Code of
Civil Procedure Section 1161 — specifically the requirements for a 3-Day
Pay or Quit notice for nonpayment of rent. Show me the key statutory language
and the source URL.
```

**Scene 3 — Case law gap:**
```
What does Orozco v. Casimiro, 121 Cal. App. 4th Supp. 7 (2004) hold about
late fees in California pay-or-quit eviction notices? What does that holding
mean for a notice demanding $1,850 rent plus $200 in late fees?
```

---

## RECORDING TIPS

- **Scene 1: Do NOT type into Cowork.** Narrate only. First thing you type is Scene 2.
- **Scene 3 is the payload** — the case law beat is the discovery story. Don't rush it. Let Orozco land before you move to the widget.
- **Point explicitly** at what's on screen. Your audience is watching a recording — use your cursor and verbal cues to direct attention.
- **Let Cowork load in real time** during Scenes 2 and 3 — don't cut. Watching live retrieval is part of the demo.
- **Scene 7 is hardest to deliver naturally.** Practice it separately before recording.
- **Plan for 2–3 takes.** First take is rarely the best.
- **Loom setup:** Screen + Camera, record full screen, trim start/end before sharing.

---

## AFTER RECORDING

1. Trim in Loom (cut dead time at start/end)
2. Copy the Loom share link
3. Paste into the `[ link to demo ]` placeholder on **Slide 7** of the deck
4. Fill GitHub link placeholders on **Slides 12–13**: `github.com/andrewmichaelcohen-a2j/a2j-ai`

---

*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*
*Demo recording script v4 — June 2026. Key change from v3: Added Scene 3 (case law / Orozco beat) as the discovery story bridge between statute retrieval and the comparison widget. This is the narrative arc for Option (ii): statute → gap → case law → decision logic.*
