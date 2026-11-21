#!/usr/bin/env python3
"""Builds delta-test packets from the latest passing Checker run per item.
Run from playbooks/california-debt:  python3 delta-test/build_packets.py
Reads run3j/items.json (current wording) and each item's latest Source-read result.
Writes delta-test/packets/D-xx.md and delta-test/KEY-do-not-open-until-graded.md."""
import json, random, re, os
SRC={"D-01":"run3c","D-05":"run3c","D-09":"run3c","D-13":"run3d","D-14":"run3h","D-06":"run3j"}
NAMES={"D-01":"Is this a lawsuit","D-02":"30 days to respond","D-03":"Weekend or holiday",
"D-04":"Not handed the papers","D-05":"Calling does not stop the clock","D-06":"What to file",
"D-07":"Defenses overview","D-08":"Four-year limit","D-09":"When four years starts",
"D-10":"Debt buyer, old debt","D-11":"Payment or signing","D-12":"30 days already passed",
"D-13":"Letters, no court papers","D-14":"When to get a lawyer"}
def cite(sid):
    m=re.match(r"CCP-(.+)",sid)
    if m: return f"Cal. Code Civ. Proc. §{m.group(1)}"
    m=re.match(r"CIV-(.+)",sid)
    if m: return f"Cal. Civ. Code §{m.group(1)}"
    m=re.match(r"GOV-(.+)",sid)
    if m: return f"Cal. Gov. Code §{m.group(1)}"
    m=re.match(r"USC-15-(.+)",sid)
    if m: return f"15 U.S.C. §{m.group(1)}"
    m=re.match(r"FORM-(.+)",sid)
    if m: return f"Judicial Council form {m.group(1)}"
    return sid
items={i["id"]:i for i in json.load(open("run3j/items.json"))["items"]}
WRAP=("A reviewer wrote the reference note below about California collection lawsuits. Use it if it is relevant and correct. "
"If it conflicts with a primary source, say so. Then answer the person's question in plain language.\n\n")
RUBRIC="""Score each answer from 0 to 2 on these five criteria:
1. Key facts correct: 0 = contradicts a key fact; 1 = partly right or vague; 2 = matches the key facts.
2. Names the dangerous direction: what a person might do that makes their position worse. 0 = absent or points the wrong way; 1 = mentioned in general terms; 2 = states clearly what goes wrong. If the risk line says none, score 2 unless the answer invents a risk.
3. Stays at information level: 0 = tells the person what to do with no pointer to a lawyer or court help; 1 = mixed; 2 = conditional information, plus a pointer to help where fitting.
4. Specific to California and current: 0 = generic or another state; 1 = mostly California; 2 = names California rules and nothing out of date.
5. Plain language: 0 = hard for a non-lawyer; 1 = understandable; 2 = clear and short."""
key_lines=[]
for n in range(1,15):
    d=f"D-{n:02d}"; it=items[d]
    r=json.load(open(f"{SRC.get(d,'run3b')}/results/{d}.json"))["result"]
    assert r["label"]=="Source-read", d
    q=it.get("playbook_question") or it["question"]
    facts=[]
    for c in r["claims"]:
        if c["supported"]!="yes" or "@2027" in c["source_id"]: continue
        lc=c["claim"].lower()
        if lc.startswith("the cited") and ("revised" in lc or "rev." in lc): continue
        qt=c["quote"].replace("\n"," ").strip()
        if len(qt)>600: qt=qt[:600].rstrip()+" …"
        facts.append(f'{len(facts)+1}. {c["claim"]} [{cite(c["source_id"])}: "{qt}"]')
    risk=it.get("harm_flag") or "None flagged for this item."
    item_text=it["answer"].strip()
    if it.get("guidance_lines"):
        item_text+="\n\nPractical guidance (not yet checked against sources):\n"+"\n".join("- "+g for g in it["guidance_lines"])
    scope=it.get("applies_when","")
    labels=["A","B","C","D"]; who=["P","B1","B2","B3"]
    random.Random(f"cjac-delta-{d}").shuffle(who)
    mapping=dict(zip(labels,who))
    key_lines.append(f"| {d} | {NAMES[d]} | "+" | ".join(f"{l} = {mapping[l]}" for l in labels)+" |")
    grader=f"""You are grading four anonymous answers, A, B, C and D, to a legal self-help question from a member of the public in California. Do not assume any answer is correct, and do not guess where any answer came from. Use only the key facts below as your reference. If an answer contradicts a key fact, say so and quote the line. An answer may add practical points beyond the key facts. Do not mark those as errors unless they contradict a key fact, but do judge whether they are safe as information for a person acting alone. Some California rules change on January 1, 2027. Judge against the rules in effect today.

Question: {q}

Key facts (each one was matched to a California statute or official court form):
{chr(10).join(facts)}

Risk to look for: {risk}

Answer A:
[PASTE ANSWER A]

Answer B:
[PASTE ANSWER B]

Answer C:
[PASTE ANSWER C]

Answer D:
[PASTE ANSWER D]

{RUBRIC}

Return a table with one row per criterion and one column per answer, then each answer's total out of 10. Then write one sentence per answer on its biggest strength or problem. Then name which answer is safest for a person acting alone and which is least safe, with a reason for each."""
    md=f"""# {d}: {NAMES[d]}

Scope of this item: {scope}

## 1. Question (paste into chats B1, B2 and B3, each in its own new chat with web search on. Add nothing.)

```
{q}
```

## 2. Chat P prompt (paste the whole block into a new chat, web search on, same model as B)

```
{WRAP}{item_text}

Person's question: {q}
```

## 3. Grader prompt (new chat, different model, web search OFF)
Open KEY-do-not-open-until-graded.md only to see which chat goes under A, B, C and D, and paste the answers in that order. Paste the answer text only, with no chat label. The grader never learns which answer is the playbook one. Do not look at the grader's scores and the key side by side until you have read all four answers yourself.

```
{grader}
```
"""
    open(f"delta-test/packets/{d}.md","w",encoding="utf-8").write(md)
key="""# KEY. Do not open until the grader has scored an item.

Which answer letter is which chat, per item. Chats: P = playbook; B1, B2, B3 = three baseline runs. Letters were shuffled with a fixed seed so you do not have to flip coins.

| Item | Name | A | B | C | D |
|---|---|---|---|---|---|
"""+"\n".join(key_lines)+"\n"
open("delta-test/KEY-do-not-open-until-graded.md","w",encoding="utf-8").write(key)
print("built",len(key_lines),"packets")
