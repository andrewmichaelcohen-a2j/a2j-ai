#!/usr/bin/env python3
"""
md_to_pdf.py -- zero-cost Andy review artifacts (Addendum 2026-09-05, s.2).

Renders a repo markdown document to a formatted, printable PDF with reportlab.
No AI, no network. Supports headings, paragraphs, bullet/numbered lists, pipe
tables, bold/italic/code, horizontal rules, and "[ ]" checkboxes. Optional
--break-on "### " starts each level-3 section on a new page (one item per page
section for the counsel queue), and --notes adds a ruled Notes field after each
such section.

Usage: python3 scripts/review/md_to_pdf.py IN.md OUT.pdf [--break-on "### "] [--notes] [--title "..."]
"""
import re, sys, argparse, html
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable, KeepTogether)

def inline(md: str) -> str:
    s = html.escape(md, quote=False)
    s = re.sub(r"`([^`]+)`", r'<font face="Courier" size="8.5">\1</font>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    s = s.replace("[ ]", '<font face="Courier-Bold" size="10">[&nbsp;&nbsp;]</font>')
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'\1 <font size="7" color="#555555">(\2)</font>', s)
    return s

def build(md_text: str, out: str, break_on: str | None, notes: bool, title: str | None):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=13, spaceAfter=5)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10.5, textColor=colors.HexColor("#333333"))
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=19, spaceBefore=4, spaceAfter=8)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=12.5, leading=16, spaceBefore=12, spaceAfter=6)
    h3 = ParagraphStyle("h3", parent=ss["Heading3"], fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=10, spaceAfter=5, textColor=colors.HexColor("#1a3d6d"))
    bullet = ParagraphStyle("bullet", parent=body, leftIndent=14, bulletIndent=4)
    cell = ParagraphStyle("cell", parent=body, fontSize=7.8, leading=10, spaceAfter=0)
    story = []
    if title and not md_text.lstrip().startswith("# "):
        story += [Paragraph(inline(title), h1), Spacer(1, 6)]
    lines = md_text.splitlines()
    i = 0; para = []; first_h3 = True
    def flush_para():
        nonlocal para
        if para:
            story.append(Paragraph(inline(" ".join(para)), body)); para = []
    def notes_block():
        if notes:
            story.append(Spacer(1, 6)); story.append(Paragraph("<b>Notes</b>", body))
            for _ in range(5):
                story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#999999"), spaceBefore=11, spaceAfter=0))
    in_code = False
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith("```"):
            flush_para(); in_code = not in_code; i += 1; continue
        if in_code:
            story.append(Paragraph(html.escape(ln) or "&nbsp;", ParagraphStyle("code", parent=body, fontName="Courier", fontSize=7.8, leading=10, spaceAfter=0))); i += 1; continue
        if ln.startswith("# "):
            flush_para(); story.append(Paragraph(inline(ln[2:]), h1)); i += 1; continue
        if ln.startswith("## "):
            flush_para()
            if break_on == "## " and story: story.append(PageBreak())
            story.append(Paragraph(inline(ln[3:]), h2)); i += 1; continue
        if ln.startswith("### "):
            flush_para()
            if break_on == "### ":
                if not first_h3: notes_block(); story.append(PageBreak())
                first_h3 = False
            story.append(Paragraph(inline(ln[4:]), h3)); i += 1; continue
        if ln.strip() in ("---", "***"):
            flush_para(); story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#888888"), spaceBefore=6, spaceAfter=6)); i += 1; continue
        if ln.startswith("|"):
            flush_para(); rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells): rows.append(cells)
                i += 1
            if rows:
                ncol = max(len(r) for r in rows)
                data = [[Paragraph(inline(c), cell) for c in (r + [""] * (ncol - len(r)))] for r in rows]
                avail = 7.0 * inch; widths = [avail / ncol] * ncol
                t = Table(data, colWidths=widths, repeatRows=1)
                t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef5")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
                story.append(t); story.append(Spacer(1, 6))
            continue
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)", ln)
        if m:
            flush_para(); txt = m.group(3); i += 1
            while i < len(lines) and lines[i].startswith("  ") and not re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]) and lines[i].strip():
                txt += " " + lines[i].strip(); i += 1
            mark = "&bull;" if m.group(2) in ("-", "*") else m.group(2)
            story.append(Paragraph(inline(txt), bullet, bulletText=mark)); continue
        if ln.startswith(">"):
            flush_para(); story.append(Paragraph(inline(ln.lstrip("> ")), ParagraphStyle("q", parent=small, leftIndent=12, textColor=colors.HexColor("#444444")))); i += 1; continue
        if not ln.strip():
            flush_para(); i += 1; continue
        if ln.startswith("**") and para:
            flush_para()  # a bold-led line starts its own paragraph (label: text blocks)
        para.append(ln.strip()); i += 1
    flush_para()
    if break_on == "### " and not first_h3: notes_block()
    def footer(canvas, doc):
        canvas.saveState(); canvas.setFont("Helvetica", 7.5); canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawString(0.75 * inch, 0.5 * inch, (title or out.split("/")[-1]) + "  -  Copyright 2026 Andrew M Cohen. Apache 2.0.")
        canvas.drawRightString(letter[0] - 0.75 * inch, 0.5 * inch, f"page {doc.page}"); canvas.restoreState()
    doc = SimpleDocTemplate(out, pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch, topMargin=0.7 * inch, bottomMargin=0.8 * inch, title=title or "", author="CJaC / Cowork")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("inp"); ap.add_argument("out"); ap.add_argument("--break-on", default=None); ap.add_argument("--notes", action="store_true"); ap.add_argument("--title", default=None)
    a = ap.parse_args(); build(open(a.inp, encoding="utf-8").read(), a.out, a.break_on, a.notes, a.title); print("wrote", a.out)
