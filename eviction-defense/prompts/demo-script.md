# LHC Eviction Demo — Live Demo Script
## Pre-Written Prompts for Cowork Session

**How to use this document:**
Before the demo, open this file alongside Cowork. Each prompt below is a complete block of text — copy and paste it into Cowork at the right moment in the demo. Do not type live during the demo; paste from here.

---

## SETUP (do before audience arrives)

1. Open Cowork
2. Open this file in a separate window
3. Open two browser tabs:
   - Tab A: Your GitHub repo → `eviction-defense/jurisdictions/ca_eviction_rules_v0.1.json`
   - Tab B: https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=1161.
4. Open your slide deck (Google Slides or PowerPoint)
5. Arrange your screen: slides on the left half, Cowork on the right half

---

## DEMO BEAT 1 — Carlos receives Maria's notice
*(Slides 1–5 done. Switch to Cowork. Say: "Now let me show you what Carlos sees.")*

**PASTE THIS INTO COWORK:**

```
You are running the eviction-triage skill from the LHC eviction defense plugin.

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

**ACTION:** Switch to browser Tab B (the leginfo.legislature.ca.gov URL). Point to subdivision 2 of CCP §1161. Read the key sentence aloud: *"...stating the amount that is due..."* — then point out that the notice included $200 in late fees on top of the rent amount.

**SAY:** "That statute was retrieved in real time, right now, via Legal Data Hunter. One month ago this capability did not exist for A2J tools. Every AI tool before this was answering from training data that might be months or years out of date. This is categorically different."

---

## DEMO BEAT 3 — Show the rules file
*(Switch to browser Tab A — GitHub — showing ca_eviction_rules_v0.1.json)*

**SAY:** "Here is what made that analysis possible. This is the California rules file. It's 45 lines of structured data. It encodes the decision logic: *if the notice includes any amount other than unpaid rent, flag as defective.* It's not AI guessing — it's explicit, auditable, human-reviewable rules."

**Point to the DRAFT label in the metadata. SAY:** "You'll notice it says DRAFT. That means a licensed California tenant attorney has not yet validated this file. That validation process — coordinating the expert review, managing versions across 50 states — is exactly what the LHC is designed to do. Nobody is doing this systematically yet. This is the LHC's first major project."

**Then point to the TX rules file link. SAY:** "Here's the Texas version. Let me show you what portability looks like."

---

## DEMO BEAT 4 — Texas portability
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

**SAY:** "Now imagine the LHC coordinates teams across 50 states to validate 50 rules files. Every legal aid deployment, everywhere, gets the benefit. That's the compounding power of shared infrastructure."

---

## DEMO BEAT 6 — Switch back to slides
*(Return to slides — Slide 8: Gaps table)*

**SAY:** "Let me be honest about what this doesn't do yet — because the gaps are where you come in."

*(Walk through gaps slide. Then go to Slide 9: LHC Opportunity. Then Slide 10: The Ask.)*

---

## CONTINGENCY NOTES

**If Legal Data Hunter doesn't return the statute:**
Say: "The live retrieval connector is designed to pull the statute in real time — sometimes there's a brief delay. What you're seeing is the rules file analysis, which applies the decision logic directly. The live statute retrieval is an additional verification layer." Then manually paste the statute URL into the chat and continue.

**If the output is longer than expected:**
That's fine — it shows the depth of the analysis. Scroll to the DEFECT DETECTED section first, then come back to the full report.

**If someone asks "is this legal advice?":**
"No — and the tool says so explicitly in every output. This is legal information — what the law says — not advice about what a specific person should do. Every output refers the user to a licensed attorney. That distinction is built into the architecture."

**If someone asks "has a lawyer checked the rules?":**
"Great question — and that's exactly the honest gap I'm about to show you. The rules files are clearly marked DRAFT. Attorney validation is the first project the LHC is recruiting for. The demo is designed to show what's possible and what the community needs to build — not to claim the work is finished."

---

## TIMING GUIDE

| Beat | Content | Target Time |
|------|---------|-------------|
| Slides 1–5 | Setup, hook, problem, what changed, five things, Maria | 0:00–2:00 |
| Beat 1 | Paste CA prompt, output appears | 2:00–3:30 |
| Beat 2 | Show live statute in browser | 3:30–4:30 |
| Beat 3 | Show rules file on GitHub | 4:30–5:30 |
| Beat 4 | Paste TX prompt, output appears | 5:30–6:30 |
| Beat 5 | Portability moment | 6:30–7:15 |
| Beat 6 | Gaps + LHC Opportunity + Ask slides | 7:15–9:30 |
| Close | Questions | 9:30+ |

*Legal Help Commons · Demo Script v0.1 · May 2026 · Not for distribution*
