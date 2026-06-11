# Eviction Demo — Recording Script v5
## Civil Justice as Code · ~6:00–6:30 minute Loom recording

*Recording guide, not a live script. Speak naturally — polished but conversational.*

---

## SETUP — Do before hitting Record

| Tab / Window | What it is |
|-------------|-----------|
| **Cowork** | Active session, blank chat ready |
| **Browser Tab A** | Widget: `file:///Users/andrewcohen/Documents/GitHub/a2j-ai/demos/eviction/widget/RulesComparisonWidget.html` — pre-load on **CA** |
| **Browser Tab B** | GitHub: `rules/eviction/california/ca_eviction_v1.json` — open to `notice_defects` section |
| **File ready to attach** | `ca_eviction_rules_v0.1.json` — have it ready in Finder to drag into Cowork for Scene 4 |

Record your **full screen** in Loom (Screen + Camera recommended).

Have this script open on a **second monitor or device** — not on your recorded screen.

> **⚠️ IMPORTANT:** Scene 1 — do NOT type anything into Cowork. Narrate only. The first thing you type is the Scene 2 prompt.

---

## THE SCRIPT

---

### SCENE 1 — The Setup (0:00–0:35)
*Cowork is open and blank.*

**SAY:**
"I'm going to show you a working eviction-defense tool — built in three days, for essentially zero dollars, by a non-engineer attorney. And I want to walk you through the specific things that made it possible — because understanding how it was built is the whole point."

"Let's start with Maria. It's 10pm. She just found this taped to her door."

**SAY:**
"Maria Garcia. Los Angeles, California. She's lived in her apartment for 3 years. Tonight she received a 3-Day Notice to Pay Rent or Quit demanding $2,050 — $1,850 in rent, plus $200 in late fees. She has no lawyer. No idea whether this notice is even valid."

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
"That's leginfo.legislature.ca.gov — the Legislature's own website. Past legal AI guessed the law from memory. This one reads it live. That's what the infrastructure changed: from predictive to deterministic."

*Pause 5 seconds — let the statute be visible.*

**SAY:**
"But here's what I discovered when I built this. Reading the statute isn't enough."

---

### SCENE 3 — The Case Law Gap (1:30–2:20)
*New chat in Cowork. Type or paste:*
```
What does Orozco v. Casimiro, 121 Cal. App. 4th Supp. 7 (2004) hold about
late fees in California pay-or-quit eviction notices? What does that holding
mean for a notice demanding $1,850 rent plus $200 in late fees?
```

*While it loads:*

**SAY:**
"CCP §1161 says the notice must state 'the amount that is due.' But the statute text alone doesn't tell you whether late fees are permitted or prohibited. That answer comes from how California courts have interpreted the statute — specifically a 2004 California appellate case, Orozco v. Casimiro."

*When output appears:*

**SAY:**
"Orozco held that late fees are void as liquidated damages under California law — and that including them in the demanded amount makes the entire notice defective. A good attorney would know this. But an AI reading only the statute would miss it."

"So I had a choice: reference this case in every query, manually, every time — or encode it. Capture the doctrine as structured logic so the tool applies it automatically, deterministically, every time. That's the decision-logic rules layer."

---

### SCENE 4 — Live Rules File Analysis (2:20–3:15)
*Stay in Cowork. Attach `ca_eviction_rules_v0.1.json` to your message — drag it into the chat. Then type:*
```
Using the attached CA eviction rules file, analyze this notice:

Tenant: Maria Garcia · Los Angeles, CA
Notice type: 3-Day Notice to Pay Rent or Quit
Amount demanded: $2,050 ($1,850 rent + $200 late fees)
Tenancy: 3 years
Service method: Post and mail (nail and mail)

What defects does this notice have, if any? Cite the relevant rule and statute.
```

*While it loads:*

**SAY:**
"I've attached the California eviction rules file — the decision-logic layer. Same AI model. Same live statute access. Now with the encoded doctrine. Let's see what it finds."

*When output appears — point at the defect result:*

**SAY:**
"One defect. INVALID. The notice includes late fees — CCP §1161(2), Orozco v. Casimiro. That's the answer Maria needs. And notice the citation is right there — auditable, verifiable, not a guess."

*Pause.*

**SAY:**
"Same notice. Without the rules file: no defects found. With it: one defect, flagged correctly, with a citation. That's the difference the decision-logic layer makes."

---

### SCENE 5 — The Comparison Widget (3:15–3:55)
*Switch to Browser Tab A — Comparison Widget, CA selected.*

**SAY:**
"I built this comparison widget to make that contrast visual. Left panel: AI with live statute only — no defects found. Right panel: AI with the rules file — one defect, INVALID, with the Orozco citation. Same scenario. Two very different answers."

*Point to the 'Why the difference?' section — click to expand it.*

**SAY:**
"The left panel isn't broken. It's a capable AI doing its best with what it has. The difference is the rules layer — explicit, auditable logic that encodes what courts have determined the statute requires."

---

### SCENE 6 — The Rules File (3:55–4:35)
*Switch to Browser Tab B — GitHub, ca_eviction_v1.json, notice_defects section.*

**SAY:**
"Here's the file. Look at this entry: defect — includes late fees. Result — INVALID. Statute — CCP §1161(2), see Orozco v. Casimiro."

"This rule didn't come from reading the statute in isolation. It came from synthesizing the statute with how California courts have interpreted it — and encoding that synthesis as structured, auditable logic."

"I drafted this in a few hours. A licensed California tenant attorney needs to validate that the synthesis is accurate. That attorney review is the first item on the validation roadmap, and it's why the file carries a DRAFT watermark."

---

### SCENE 7 — Portability (4:35–5:15)
*Switch back to Browser Tab A — Comparison Widget. Click TX.*

**SAY:**
"Watch what happens when I switch to Texas."

*Let panels re-render.*

**SAY:**
"Same AI, same structure, different rules file. Texas has no just-cause requirement — the analysis is shorter because the law is simpler. That's portability: not 50 tools reinvented from scratch. One reasoning engine, 50 rules files."

*Click NY.*

**SAY:**
"New York: 14-day notice requirement under RPAPL §711(2). Different law, same architecture. Maria's situation, across three states, from one tool."

---

### SCENE 8 — The Bridge / Close (5:15–6:00)
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
| 3 | Case law gap (Orozco) | 1:30–2:20 |
| 4 | Live rules file analysis | 2:20–3:15 |
| 5 | Comparison widget | 3:15–3:55 |
| 6 | Rules file on GitHub | 3:55–4:35 |
| 7 | Portability (TX + NY) | 4:35–5:15 |
| 8 | Bridge / close | 5:15–6:00 |
| **Total** | | **~6:00–6:30** |

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

**Scene 4 — Live rules file analysis (attach ca_eviction_rules_v0.1.json first):**
```
Using the attached CA eviction rules file, analyze this notice:

Tenant: Maria Garcia · Los Angeles, CA
Notice type: 3-Day Notice to Pay Rent or Quit
Amount demanded: $2,050 ($1,850 rent + $200 late fees)
Tenancy: 3 years
Service method: Post and mail (nail and mail)

What defects does this notice have, if any? Cite the relevant rule and statute.
```

---

## RECORDING TIPS

- **Scene 1: Do NOT type into Cowork.** Narrate only. First thing you type is Scene 2.
- **Scene 4 is the new centerpiece** — the moment you attach the file and the AI returns the correct answer. Give it room; don't rush through it.
- **Scene 3 sets up Scene 4** — the Orozco explanation is what makes Scene 4 land. Don't skip or compress Scene 3.
- **Point explicitly** at what's on screen. Use cursor and verbal cues to direct attention.
- **Let Cowork load in real time** — don't cut. Watching live retrieval is part of the demo.
- **Scene 8 is hardest to deliver naturally.** Practice it separately before recording.
- **Plan for 2–3 takes.**
- **Loom setup:** Screen + Camera, full screen, trim start/end before sharing.

---

## AFTER RECORDING

1. Trim in Loom (cut dead time at start/end)
2. Copy the Loom share link
3. Paste into `[ link to demo ]` on **Slide 7** of the deck
4. Fill GitHub link placeholders on **Slides 12–13**: `github.com/andrewmichaelcohen-a2j/a2j-ai`

---

*Copyright 2026 Andrew M Cohen. Licensed under the Apache License, Version 2.0.*
*Demo recording script v5 — June 2026. Key change from v4: Added Scene 4 (live rules file analysis in Cowork — attach ca_eviction_rules_v0.1.json and run Maria's notice). Widget moves to Scene 5 as visual summary. This makes the "with rules layer" result genuinely live, not just hardcoded in the widget.*
