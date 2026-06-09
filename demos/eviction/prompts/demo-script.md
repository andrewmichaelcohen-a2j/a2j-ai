# Eviction Demo — Recording Script
## Civil Justice as Code · 5:15–6:00 minute Loom recording

*This is a recording guide, not a live session script. You're recording alone — no audience watching in real time. Speak naturally; this is a polished but conversational walkthrough.*

---

## SETUP — Do before hitting Record

Open and arrange these on your screen before you start:

| Tab / Window | What it is |
|-------------|-----------|
| **Cowork** | Active session, blank chat ready |
| **Browser Tab A** | Paste into Chrome address bar: `file:///Users/andrewcohen/Documents/GitHub/a2j-ai/demos/eviction/widget/RulesComparisonWidget.html` — pre-load on **CA** |
| **Browser Tab B** | Paste into Chrome address bar: `file:///Users/andrewcohen/Documents/GitHub/a2j-ai/rules/eviction/california/ca_eviction_v1.json` — or open on GitHub.com |

Record your **full screen** in Loom (Screen + Camera is recommended — your face in the corner adds warmth).

Have this script open on a **second monitor or device** — not on your recorded screen.

---

## THE SCRIPT

---

### SCENE 1 — The Setup (0:00–0:35)
*Start on Cowork. Camera briefly on your face if using face cam, then share screen.*

**SAY:**
"I'm going to show you a working eviction-defense tool — built in three days, for essentially zero dollars, by a non-engineer attorney. Not a prototype in name only. A real tool. And I want to walk you through the specific things that made it possible — because understanding how it was built is the whole point."

"Let's start with Maria. It's 10pm. She just found this taped to her door."

*Type or paste into Cowork — visible on screen:*

> Maria Garcia. Los Angeles, California. She's lived in her apartment for 3 years. Tonight she received a 3-Day Notice to Pay Rent or Quit demanding $2,050 — $1,850 in rent, plus $200 in late fees. She has no lawyer. She has no idea whether this notice is even valid.

**SAY:**
"This is one of 3.6 million eviction filings a year. 95% of those tenants have no attorney."

---

### SCENE 2 — Live Statute Retrieval (0:35–1:35)
*Still in Cowork. Paste the demo prompt.*

*Paste into Cowork:*
```
Use Legal Data Hunter to retrieve the current text of California Code of 
Civil Procedure Section 1161 — specifically the requirement for a 3-Day 
Pay or Quit notice for nonpayment of rent. Show me the key statutory language 
and the source URL.
```

*This is a short retrieval call — output will appear in 15–30 seconds. While it loads:*

**SAY:**
"What's happening right now is the tool is making a live call to retrieve the actual current text of California Code of Civil Procedure Section 1161 — from the California Legislature's website. Not from AI training data. Not a paraphrase the model memorized months ago. The current statute."

*When the output appears, point your cursor at the leginfo.legislature.ca.gov URL:*

**SAY:**
"That's leginfo.legislature.ca.gov — the California Legislature's own website. That URL is real. Past legal AI tools guessed the law from memory and might be wrong or out of date. This one reads it. That's what the infrastructure changed — from predictive to deterministic."

"And I want to mention: I didn't build this from scratch. I used existing skills and plugins from Anthropic's legal infrastructure — reusable modules built by others that I connected in three days."

*Pause briefly — let the statute text be visible on screen for 5 seconds.*

**SAY:**
"But here's what I discovered when I actually built this — reading the statute isn't enough."

---

### SCENE 3 — The Gap Moment (1:35–2:45)
*Switch to Browser Tab A — the Comparison Widget, CA selected.*

**SAY:**
"Now here's the most important thing I learned building this. I want to show it to you directly."

*Point to the LEFT panel ("Without Rules File"):*

**SAY:**
"Left panel: the AI just read the live statute — CCP §1161. It retrieved the current text, the same text you just saw in Cowork. And it returned this answer: the notice appears valid. No defects found. Zero."

*Pause. Let them read.*

**SAY:**
"This answer is wrong. The notice is almost certainly void under California law. A good attorney would catch it in sixty seconds. But the AI — even with the live statute — missed it."

*Point to the RIGHT panel ("With Rules File"):*

**SAY:**
"Right panel. Two defects found. The notice is flagged as likely invalid, with specific citations."

*Pause.*

**SAY:**
"Same AI model. Same live statute. Completely different result. Why?"

"The statute says the notice must state 'the amount that is due.' What it doesn't encode is this: California courts have interpreted that to mean rent only — late fees are prohibited, and including them voids the notice. That's legal doctrine — the synthesis of statutory text and judicial interpretation. An AI reading the statute text alone doesn't have that. The rules file encodes it as explicit, auditable logic: if the notice includes late fees, the result is INVALID under §1161(2). That's the layer that was missing."

*Point to the safety disclaimer in the right panel output:*

**SAY:**
"And notice: the right panel says clearly — this is legal information, not legal advice, verify with an attorney. That's not a disclaimer bolted on at the end. It's built into the architecture."

---

### SCENE 4 — The Rules File (2:45–3:45)
*Switch to Browser Tab B — GitHub showing ca_eviction_v1.json. Scroll to the `notice_defects` section.*

**SAY:**
"Here's the file that made the difference."

*Pause on the `includes_late_fees` entry.*

**SAY:**
"Here's the file that made the difference. Forty-five lines of JSON. Look at this entry: defect — 'includes late fees.' Result — INVALID. Statute — CCP §1161(2)."

"This rule didn't come from reading the statute in isolation. It came from synthesizing the statute, how California courts have interpreted it, and how practitioners apply it. The AI encoded that synthesis as explicit, auditable logic: if this fact is present, this legal consequence follows."

"That's what's new here. Not statute lookup. Not AI predicting an answer. AI encoding legal doctrine — the accumulated interpretation of the law — as structured rules that can be inspected, tested, and validated."

"I drafted this file in a few hours. A licensed California attorney needs to confirm the synthesis is accurate — that the encoded doctrine reflects how the law actually applies. That's the first item on the validation roadmap, and it's the reason attorney review is genuinely required, not just a formality."

---

### SCENE 5 — Portability (3:45–4:30)
*Switch back to Browser Tab A — Comparison Widget. Click the TX button.*

**SAY:**
"Watch what happens when I switch to Texas."

*Let both panels re-render.*

**SAY:**
"Same AI model. Same structure. Different rules file. Texas has no just-cause requirement — the analysis is shorter because the law is simpler. That's what portability looks like. Not 50 separate tools. One reasoning engine, 50 rules files."

---

### SCENE 6 — The Bridge (4:30–5:15)
*Face cam if using it, or stay on screen.*

**SAY:**
"Let me summarize what you just saw."

"One non-engineer attorney. Three days. No software budget. A working multi-state eviction defense tool — with live statutory retrieval, structured decision logic, safety guardrails, and citations."

"That was possible because the infrastructure exists. Anthropic built it. I connected it."

"What doesn't exist yet — at any scale — is the validated rules library. The decision-logic layer that makes the difference between zero defects found and two defects found. For eviction. For debt collection. For benefits appeals. Across all 50 states. That's what Civil Justice as Code is building."

"The question isn't whether it can be done. I just showed you it can. The question is whether we build it with rigor — validated, open-source, with published accuracy standards — so that when Maria uses a tool like this, she can trust the answer."

*Stop recording.*

---

## TIMING GUIDE

| Scene | Content | Target |
|-------|---------|--------|
| 1 | Setup + Maria | 0:00–0:35 |
| 2 | Live statute retrieval | 0:35–1:35 |
| 3 | The gap moment (widget) | 1:35–2:45 |
| 4 | The rules file (GitHub) | 2:45–3:45 |
| 5 | Portability (TX switch) | 3:45–4:30 |
| 6 | Bridge / close | 4:30–5:15 |
| **Total** | | **~5:15–6:00** |

Allow up to 6:00 for natural pauses and Cowork output loading time.

---

## RECORDING TIPS

- **Don't rush Scene 3.** The gap moment is the payload. Protect the time here.
- **Point explicitly** at what's on screen. Your audience is watching a recording; use your cursor and verbal cues to direct attention.
- **Let the Cowork output load in real time** during Scene 2 — don't cut. Watching it retrieve the live statute is part of the demo.
- **Scene 6 is the hardest to deliver naturally.** Practice it separately a few times before recording.
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
*Demo recording script v2 — June 2026. Replaces prior live-session script.*
