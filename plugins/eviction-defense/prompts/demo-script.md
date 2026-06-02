# Eviction Defense Demo — Live Demo Script
## Pre-Written Prompts for Cowork Session

**How to use this document:**
Before the demo, open this file alongside Cowork. Each prompt below is a complete block of text — copy and paste it into Cowork at the right moment in the demo. Do not type live during the demo; paste from here.

---

## SETUP (do before audience arrives)

1. Open Cowork
2. Open this file in a separate window
3. Open three browser tabs:
   - Tab A: GitHub repo → `eviction-defense/jurisdictions/ca_eviction_v1.2.json` (the new v1.2 file)
   - Tab B: https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=1161.
   - Tab C: `eviction-defense/components/RulesComparisonWidget.html` — open this locally in Chrome (double-click the file). Pre-load with CA selected.
4. Open your slide deck (Google Slides or PowerPoint)
5. Arrange your screen: slides on the left half, Cowork on the right half

---

## DEMO BEAT 1 — Carlos receives Maria's notice
*(Slides 1–5 done. Switch to Cowork. Say: "Now let me show you what Carlos sees.")*

**PASTE THIS INTO COWORK:**

```
You are running the eviction-triage skill from the eviction defense plugin.

The jurisdiction rules file is: eviction-defense/jurisdictions/ca_eviction_rules_v0.1.json

Here are the intake facts for this case:

TENANT: Maria (restaurant worker)
JURISDICTION: Los Angeles, California
NOTICE TYPE: 3-Day Notice to Pay Rent or Quit
AMOUNT DEMANDED: $2,050 total — itemized as $1,850 unpaid rent + $200 late fees
TENANCY LENGTH: 3 years (36 months) in the same unit
BUILDING TYPE: Multi-unit apartment building
SERVICE METHOD: Notice handed directly to Maria at her door
DATE SERVED: [today's date]
REPAIR COMPLAINTS: None in the past 6 months
CODE ENFORCEMENT: No contact with code enforcement

Please:
1. Retrieve CCP Section 1161 via Legal Data Hunter to ground the analysis in the current live statute
2. Apply the CA rules file to screen for all defect triggers
3. Run the AB 1482 coverage screen (tenancy is 36 months)
4. Flag any applicable affirmative defenses
5. Produce the full triage report in the SKILL.md output format

Include confidence levels and live statute citations in the output.
```

---

## DEMO BEAT 2 — Show the live statute
*(After the triage report appears. Point to the CCP §1161 citation in the output.)*

**SAY:** "This is not a chatbot making things up. Let me show you where this comes from."

**ACTION:** Switch to browser Tab B (leginfo.legislature.ca.gov). Point to subdivision 2 of CCP §1161. Read aloud: *"...stating the amount that is due..."* — then point out that the notice demanded $200 in late fees on top of rent.

**SAY:** "That statute was retrieved in real time via Legal Data Hunter. Every AI tool before this was answering from training data that might be months or years out of date. This is categorically different."

---

## DEMO BEAT 3 — Transition to the rules layer (NEW — 4:00 mark)
*(Complete the statute moment. Then say:)*

**SAY:** "That was the law retrieved live. Now let me show you the second piece — what the system does with that law. This is where the rules file comes in."

---

## DEMO BEAT 3A — Open the CA rules file (NEW — 4:30 mark)
*(Switch to browser Tab A — GitHub — showing ca_eviction_v1.2.json)*

**SAY:** "Here is the California rules file. It's 45 lines of structured data. Walk through four fields: the notice type, the tenancy threshold, the defect trigger for late fees, and the local overlays for Los Angeles. I drafted this in hours. It needs attorney validation before production use — that is the community project. But the structure is complete."

**Point to the `_validation_flag` field. SAY:** "You'll notice it flags a specific legal question for attorney review — the 15-day notice period claim. That level of transparency about what still needs human expert review is built into the architecture. DRAFT files say what they don't know."

---

## DEMO BEAT 3B — Show the React comparison widget (NEW — 5:00 mark)
*(Switch to browser Tab C — RulesComparisonWidget.html in Chrome)*

**SAY nothing at first.** Let the audience see the two panels side by side. Give them 5–10 seconds to read.

**THEN SAY:** "Left panel: a capable AI model answering from training data. Confident. Plausible. Wrong — because the law includes a late fee prohibition and a notice period requirement that the model doesn't know about. Right panel: the same model grounded in the rules file. Deterministic. Cited. Correct. The difference is not the AI. It is the rules layer."

**Point to "DEFECTS FOUND: 0" on the left. Then "DEFECTS FOUND: 2" on the right.**

**SAY:** "Zero versus two. That difference is the one that matters when someone is about to be evicted."

---

## DEMO BEAT 3C — Switch to Texas (NEW — 5:20 mark)
*(Click the TX button in the jurisdiction switcher on the widget)*

**SAY:** "Now watch what happens when I switch to Texas."

*(Wait for the panels to re-render.)*

**SAY:** "The reasoning engine did not change. The rules file did. Texas has no just-cause requirement, simpler notice rules — the analysis is shorter because the law is simpler. That's what portability looks like. No team needs to encode notice periods again. Building and maintaining this library — with expert review, version control, and open access — is the most important infrastructure gap in A2J AI today. And nobody has built it yet."

---

## DEMO BEAT 3D — Return to demo flow (5:45 mark)
*(Close the widget. Return to slides — go to the Gaps slide.)*

**SAY:** "Let me be honest about what this doesn't do yet — because the gaps are where you come in."

---

## DEMO BEAT 4 — Texas portability (original — now REPLACED by 3C above)

*(This beat is superseded by Demo Beat 3C. The Texas Cowork prompt below is retained as a backup only — use it if the widget is unavailable.)*
*(Back to Cowork. Paste this:)*

**PASTE THIS INTO COWORK:**

```
Now run the same analysis using the Texas rules file instead:
eviction-defense/jurisdictions/tx_eviction_rules_v0.1.json

Same tenant facts — but now the property is in Houston, Texas.
The tenant was current on rent before this month.
The building receives Section 8 federal housing assistance.

Show how the analysis differs from California. Highlight:
- Whether Texas has a just cause requirement (it does not)
- Whether the SB 38 pay-or-vacate requirement applies
- Whether the CARES Act 30-day notice requirement applies given the Section 8 assistance
- What defenses are available vs. not available compared to California
```

---

## DEMO BEAT 5 — The portability moment
*(After Texas output appears.)*

**SAY:** "The reasoning engine did not change. The workflow logic did not change. Only the rules file changed — from California to Texas. That's what portability means. The Tenant Power Toolkit took 50 attorneys two years to build for California. This took a data file swap."

**SAY:** "Now imagine the the project coordinates teams across 50 states to validate 50 rules files. Every legal aid deployment, everywhere, gets the benefit. That's the compounding power of shared infrastructure."

---

## DEMO BEAT 6 — Switch back to slides
*(Return to slides — Slide 8: Gaps table)*

**SAY:** "Let me be honest about what this doesn't do yet — because the gaps are where you come in."

*(Walk through gaps slide. Then go to Slide 9: The Opportunity. Then Slide 10: The Ask.)*

---

## CONTINGENCY NOTES

**If Legal Data Hunter doesn't return the statute:**
Say: "The live retrieval connector is designed to pull the statute in real time — sometimes there's a brief delay. What you're seeing is the rules file analysis, which applies the decision logic directly. The live statute retrieval is an additional verification layer." Then manually paste the statute URL into the chat and continue.

**If the output is longer than expected:**
That's fine — it shows the depth of the analysis. Scroll to the DEFECT DETECTED section first, then come back to the full report.

**If someone asks "is this legal advice?":**
"No — and the tool says so explicitly in every output. This is legal information — what the law says — not advice about what a specific person should do. Every output refers the user to a licensed attorney. That distinction is built into the architecture."

**If someone asks "has a lawyer checked the rules?":**
"Great question — and that's exactly the honest gap I'm about to show you. The rules files are clearly marked DRAFT. Attorney validation is the first community project. The demo shows what's possible and what the community needs to build — not to claim the work is finished."

---

## TIMING GUIDE

| Beat | Content | Target Time |
|------|---------|-------------|
| Slides 1–5 | Setup, hook, problem, what changed, five things, Maria | 0:00–2:00 |
| Beat 1 | Paste CA prompt into Cowork, output appears | 2:00–3:30 |
| Beat 2 | Show live statute in browser (Tab B) | 3:30–4:00 |
| Beat 3 | Transition: "Now let me show you the rules layer" | 4:00–4:30 |
| Beat 3A | Open ca_eviction_v1.2.json on GitHub (Tab A) | 4:30–5:00 |
| Beat 3B | Open comparison widget in browser (Tab C), CA view | 5:00–5:20 |
| Beat 3C | Switch widget to TX — portability moment | 5:20–5:45 |
| Beat 3D | Return to slides — Gaps slide | 5:45–6:00 |
| Beat 6 | Gaps + Opportunity + Ask slides | 6:00–9:30 |
| Close | Questions | 9:30+ |

* Demo Script v0.1 · May 2026 · Not for distribution*


---

*Copyright 2026 Andrew M Cohen. Licensed under the [Apache License, Version 2.0](../LICENSE).*