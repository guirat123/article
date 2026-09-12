#!/usr/bin/env python3
"""LNCS page-count proof renderer.

No TeX engine can be installed in this sandbox, so this tool renders
paper.tex with the *exact* Springer LNCS page geometry (printing area
12.2 x 19.3 cm on A4; 10 pt body on 12 pt leading; 12 pt bold section heads;
10 pt bold subsection heads; run-in third-level heads; table captions above;
figure captions below; 9 pt bibliography) using ReportLab, and typesets every
mathematics fragment with matplotlib's mathtext engine.

article.pdf (repository root) is therefore a pagination-faithful proxy: its
page count is the page-count estimate reported to the authors.  The
authoritative deliverable remains paper.tex compiled with llncs.cls.

Usage:  python3 tools/render_preview.py
"""
import os
import re
import hashlib

import matplotlib
matplotlib.use("Agg")
from matplotlib import mathtext
import pymupdf
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                Paragraph, Spacer, Image, Table, TableStyle,
                                KeepTogether)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "build", "mathtext")
os.makedirs(CACHE, exist_ok=True)

PAGE_W, PAGE_H = A4
TEXT_W = 12.2 * cm
TEXT_H = 19.3 * cm
# ReportLab Times is a few percent narrower than Computer Modern; shave
# 0.2 cm off the measure so the estimate stays conservative.
FRAME_W = TEXT_W - 0.2 * cm
BODY, LEAD = 10.0, 12.0
INLINE_MATH = re.compile(r"\$(.+?)\$", re.S)


# ---------------------------------------------------------------- mathtext
_PARSER = None


def _parser():
    global _PARSER
    if _PARSER is None:
        from matplotlib.mathtext import MathTextParser
        _PARSER = MathTextParser("path")
    return _PARSER


def _dollars(tex):
    tex = tex.strip()
    return tex if tex.startswith("$") else f"${tex}$"


def math_metrics(tex, fontsize=BODY):
    from matplotlib.font_manager import FontProperties
    w, h, depth = _parser().parse(_dollars(tex), dpi=72,
                                  prop=FontProperties(size=fontsize))[:3]
    return float(w), float(h), float(depth)


def math_image(tex, fontsize=BODY):
    key = hashlib.md5((tex + f"|{fontsize}").encode()).hexdigest()[:16]
    png = os.path.join(CACHE, key + ".png")
    meta = os.path.join(CACHE, key + ".size")
    w, h, depth = math_metrics(tex, fontsize)
    if not os.path.exists(meta):
        from matplotlib.font_manager import FontProperties
        from PIL import Image
        dpi = 300
        raw = png + ".raw.png"
        mathtext.math_to_image(_dollars(tex), raw,
                               prop=FontProperties(size=fontsize),
                               dpi=dpi, color="black")
        im = Image.open(raw).convert("L")
        mask = im.point(lambda v: 255 if v < 245 else 0)
        bbox = mask.getbbox()
        if bbox:
            pad = 1
            bbox = (max(0, bbox[0] - pad), max(0, bbox[1] - pad),
                    min(im.width, bbox[2] + pad), min(im.height, bbox[3] + pad))
            Image.open(raw).crop(bbox).save(png)
        else:
            Image.open(raw).save(png)
        os.remove(raw)
        with open(meta, "w") as fh:
            fh.write(f"{w:.3f} {h:.3f} {depth:.3f}")
    return png, w, h, depth


SY = lambda n: f'<font face="Symbol">&#x{n:02X};</font>'
TEXTMATH = {
    r"^\dagger": "<super>&#8224;</super>",
    r"\dagger": "&#8224;",
    r"\rightarrow": SY(0xAE),
    r"\approx": SY(0xBB),
    r"+": "+",
    r"k": "<i>k</i>",
    r"\mu_j": SY(0x6D) + "<sub>j</sub>",
    r"\sigma_j": SY(0x73) + "<sub>j</sub>",
    r"[0.6604, 0.7240]": "[0.6604, 0.7240]",
    r"+0.1348": "+0.1348",
    r"+0.1336": "+0.1336",
    r"+0.1191": "+0.1191",
    r"+42.4": "+42.4",
    r"-0.1766": "-0.1766",
    r"-0.1348": "-0.1348",
}


def escape_markup(text):
    s = text
    s = s.replace("\\%", "%").replace("\\&", "&amp;").replace("\\#", "#")
    s = s.replace("\\_", "_").replace("\\{", "{").replace("\\}", "}")
    s = s.replace("\\textapprox", "approx.")
    s = s.replace("{,}", ",")
    s = s.replace("~", " ")
    s = s.replace("\\,", " ").replace("\\;", " ").replace("\\!", "")
    s = re.sub(r"\\ ([a-zA-Z])", r" \1", s)
    s = s.replace("---", "\u2014").replace("--", "\u2013")
    s = s.replace("``", "\u201c").replace("''", "\u201d")
    s = re.sub(r"\\textbf\{([^}]*)\}", r"<b>\1</b>", s)
    s = re.sub(r"\\emph\{([^}]*)\}", r"<i>\1</i>", s)
    s = re.sub(r"\\textit\{([^}]*)\}", r"<i>\1</i>", s)
    s = re.sub(r"\\texttt\{([^}]*)\}", r'<font face="Courier">\1</font>', s)
    s = re.sub(r"\\todo\{([^}]*)\}",
               r'<font color="#cc0000"><b>[TODO: \1]</b></font>', s)
    s = re.sub(r"\\orcidID\{([^}]*)\}", r"<super>[\1]</super>", s)
    s = re.sub(r"\\inst\{([^}]*)\}", r"<super>\1</super>", s)
    s = re.sub(r"\\email\{([^}]*)\}", r"<i>\1</i>", s)
    s = re.sub(r"\\url\{([^}]*)\}", r"\1", s)
    s = s.replace("\\centering", "")
    return s


DAGGER = {r"^\dagger": "<super>&#8224;</super>", r"\dagger": "&#8224;"}


def render_inline(text):
    out, pos = [], 0
    for m in INLINE_MATH.finditer(text):
        out.append(escape_markup(text[pos:m.start()]))
        if m.group(1).strip() in TEXTMATH:
            out.append(TEXTMATH[m.group(1).strip()])
            pos = m.end()
            continue
        tex = (m.group(1)
               .replace(r"\sum_{t=1}^{T}", r"\sum_t")
               .replace(r"\sum_{j=1}^{5}", r"\sum_j")
               .replace(r"\sum_{i=1}^{N}", r"\sum_i"))
        png, w, h, depth = math_image(tex)
        if h > 13.5:                      # keep inline math inside the line box
            f = 13.5 / h
            w, h, depth = w * f, 13.5, depth * f
        out.append(f'<img src="{png}" width="{w:.2f}" height="{h:.2f}" '
                   f'valign="-{depth:.2f}"/>')
        pos = m.end()
    out.append(escape_markup(text[pos:]))
    return "".join(out)


# ---------------------------------------------------------------- styles
def styles():
    st = {}
    st["title"] = ParagraphStyle("title", fontName="Times-Bold", fontSize=14,
                                 leading=17, alignment=TA_CENTER,
                                 spaceAfter=14)
    st["author"] = ParagraphStyle("author", fontName="Times-Roman", fontSize=11,
                                  leading=14, alignment=TA_CENTER,
                                  spaceAfter=6)
    st["institute"] = ParagraphStyle("institute", fontName="Times-Roman",
                                     fontSize=9, leading=11.5,
                                     alignment=TA_CENTER, spaceAfter=16)
    st["abstract"] = ParagraphStyle("abstract", fontName="Times-Roman",
                                    fontSize=9, leading=11,
                                    alignment=TA_JUSTIFY, spaceAfter=8)
    st["body"] = ParagraphStyle("body", fontName="Times-Roman", fontSize=BODY,
                                leading=LEAD, alignment=TA_JUSTIFY)
    st["bodyi"] = ParagraphStyle("bodyi", parent=st["body"],
                                 firstLineIndent=15)
    st["sec"] = ParagraphStyle("sec", fontName="Times-Bold", fontSize=12,
                               leading=14, spaceBefore=18, spaceAfter=12)
    st["subsec"] = ParagraphStyle("subsec", fontName="Times-Bold",
                                  fontSize=BODY, leading=LEAD,
                                  spaceBefore=18, spaceAfter=8)
    st["runin"] = ParagraphStyle("runin", fontName="Times-Roman", fontSize=BODY,
                                 leading=LEAD, alignment=TA_JUSTIFY,
                                 spaceBefore=18)
    st["tablecap"] = ParagraphStyle("tablecap", fontName="Times-Roman",
                                    fontSize=9, leading=11,
                                    alignment=TA_JUSTIFY, spaceBefore=2,
                                    spaceAfter=4)
    st["figcap"] = ParagraphStyle("figcap", fontName="Times-Roman", fontSize=9,
                                  leading=11, alignment=TA_JUSTIFY,
                                  spaceBefore=4, spaceAfter=7)
    st["ref"] = ParagraphStyle("ref", fontName="Times-Roman", fontSize=9,
                               leading=10.6, alignment=TA_JUSTIFY,
                               leftIndent=12, firstLineIndent=-12,
                               spaceAfter=2)
    st["cell"] = ParagraphStyle("cell", fontName="Times-Roman", fontSize=8.7,
                                leading=10.4)
    st["eq"] = ParagraphStyle("eq", fontName="Times-Roman", fontSize=BODY,
                              leading=LEAD, alignment=TA_CENTER)
    return st


# ---------------------------------------------------------------- pre-pass
def collect_labels(body):
    labels = {}
    sec = sub = tab = fig = eq = 0
    ctx, cur = None, None
    for m in re.finditer(r"\\section(\*?)\{|\\subsection\{|\\begin\{table\}|"
                         r"\\begin\{figure\}|\\begin\{equation\}|"
                         r"\\end\{table\}|\\end\{figure\}|\\end\{equation\}|"
                         r"\\label\{([^}]*)\}", body):
        t = m.group(0)
        if t.startswith("\\section"):
            if not m.group(1):
                sec += 1
                sub = 0
                ctx, cur = "sec", str(sec)
            else:
                ctx, cur = None, None
        elif t.startswith("\\subsection"):
            sub += 1
            ctx, cur = "sub", f"{sec}.{sub}"
        elif t == "\\begin{table}":
            tab += 1
            ctx, cur = "tab", str(tab)
        elif t == "\\begin{figure}":
            fig += 1
            ctx, cur = "fig", str(fig)
        elif t == "\\begin{equation}":
            eq += 1
            ctx, cur = "eq", str(eq)
        elif t.startswith("\\end{"):
            ctx, cur = None, None
        else:
            if ctx is not None:
                labels[m.group(2)] = cur
    return labels


def collect_citations(body):
    order = []
    for m in re.finditer(r"\\cite\{([^}]*)\}", body):
        for key in (k.strip() for k in m.group(1).split(",")):
            if key not in order:
                order.append(key)
    return {k: i + 1 for i, k in enumerate(order)}


def parse_bib(path):
    entries = {}
    src = open(path).read()
    for m in re.finditer(r"@\w+\{([^,]+),", src):
        key, start = m.group(1).strip(), m.end()
        depth, i = 1, start
        while i < len(src) and depth:
            depth += src[i] == "{"
            depth -= src[i] == "}"
            i += 1
        entries[key] = src[start:i - 1]
    return entries


def bib_field(chunk, field):
    m = re.search(field + r"\s*=\s*\{([^}]*)\}", chunk) or \
        re.search(field + r"\s*=\s*\"([^\"]*)\"", chunk)
    return m.group(1).strip() if m else ""


def bib_text(chunk):
    authors = re.sub(r"\s+and\s+", ", ", bib_field(chunk, "author"))
    title = bib_field(chunk, "title")
    book = bib_field(chunk, "booktitle")
    jour = bib_field(chunk, "journal")
    note = bib_field(chunk, "note")
    parts = []
    if authors:
        parts.append(authors + ":")
    parts.append(title + ".")
    if book:
        parts.append("In: " + book + ".")
    elif jour:
        parts.append(jour + ".")
    if note:
        parts.append("(" + note + ")")
    return " ".join(parts)


def parse_tabular(block):
    m = re.search(r"\\begin\{tabular\}\{([^}]*)\}", block)
    ncol = len([c for c in m.group(1) if c in "lcr"])
    inner = block[m.end():block.rfind("\\end{tabular}")]
    rows, rules = [], []
    for raw in inner.split("\n"):
        line = raw.strip()
        if not line:
            continue
        if line == "\\hline":
            rules.append(len(rows))
            continue
        line = line.rstrip("\\").strip()
        if line.endswith("\\\\"):
            line = line[:-2]
        if not line:
            continue
        cells = [c.strip() for c in line.split("&")]
        cells += [""] * (ncol - len(cells))
        rows.append(cells[:ncol])
    return rows, rules, ncol


# ---------------------------------------------------------------- floats
def add_figure(blk, flow, st, markup, figmap):
    w = re.search(r"\\includegraphics\[width=([0-9.]*)\\?textwidth?\]\{([^}]*)\}",
                  blk)
    frac = float(w.group(1)) if w.group(1) else 1.0
    path = os.path.join(ROOT, "figures", w.group(2))
    d = pymupdf.open(path)
    pr = d[0].rect
    png = path.replace(".pdf", "_prev.png")
    if not os.path.exists(png):
        d[0].get_pixmap(dpi=400).save(png)
    width = FRAME_W * frac
    height = width * pr.height / pr.width
    cap = re.search(r"\\caption\{(.*?)\}\s*\\label\{([^}]*)\}", blk, re.S)
    num = figmap.get(cap.group(2), "?")
    flow.append(Spacer(1, 3))
    flow.append(Image(png, width=width, height=height, hAlign="CENTER"))
    flow.append(Paragraph(f"<b>Fig. {num}.</b>&nbsp; " + markup(cap.group(1)),
                          st["figcap"]))


def add_table(blk, flow, st, markup, tabmap):
    cap = re.search(r"\\caption\{(.*?)\}\s*\\label\{([^}]*)\}", blk, re.S)
    rows, rules, ncol = parse_tabular(blk)
    num = tabmap.get(cap.group(2), "?")
    data = [[Paragraph(markup(c), st["cell"]) if c else "" for c in r]
            for r in rows]
    t = Table(data, hAlign="CENTER")
    cmds = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 1.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]
    for rl in rules:
        cmds.append(("LINEABOVE", (0, rl), (-1, rl), 0.6, colors.black))
    t.setStyle(TableStyle(cmds))
    flow.append(KeepTogether([
        Paragraph(f"<b>Table {num}.</b>&nbsp; " + markup(cap.group(1)),
                  st["tablecap"]),
        t, Spacer(1, 8)]))


def add_equation(blk, flow, st, eqmap):
    tex = blk.replace("\\begin{equation}", "").replace("\\end{equation}", "")
    lbl = re.search(r"\\label\{([^}]*)\}", tex)
    tex = re.sub(r"\\label\{[^}]*\}", "", tex).strip()
    png, w, h, depth = math_image(tex, BODY)
    num = eqmap.get(lbl.group(1), "?") if lbl else "?"
    maxw = FRAME_W - 70
    if w > maxw:
        h *= maxw / w
        w = maxw
    inner = Table([[Image(png, width=w, height=h, hAlign="CENTER"), "",
                    Paragraph(f"({num})", st["eq"])]],
                  colWidths=[FRAME_W - 64, 24, 40])
    inner.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (2, 0), (2, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    flow.append(inner)


# ---------------------------------------------------------------- build
def build():
    src = open(os.path.join(ROOT, "paper.tex")).read()
    src = re.sub(r"(?<!\\)%[^\n]*", "", src)
    body = src[src.find("\\begin{document}") + len("\\begin{document}"):
                 src.rfind("\\end{document}")]
    body_par = body.replace("\n\n", "\n@\n")

    labels = collect_labels(body)
    cites = collect_citations(body)
    bib = parse_bib(os.path.join(ROOT, "refs.bib"))
    tabmap, figmap, eqmap = {}, {}, {}
    tab = fig = eq = 0
    env = None
    for m in re.finditer(r"\\begin\{(table|figure|equation)\}|"
                         r"\\end\{(table|figure|equation)\}|"
                         r"\\label\{([^}]*)\}", body):
        if m.group(1):
            env = m.group(1)
            if env == "table":
                tab += 1
            elif env == "figure":
                fig += 1
            else:
                eq += 1
        elif m.group(2):
            env = None
        elif env == "table":
            tabmap[m.group(3)] = str(tab)
        elif env == "figure":
            figmap[m.group(3)] = str(fig)
        elif env == "equation":
            eqmap[m.group(3)] = str(eq)

    st = styles()
    flow = []
    state = {"sec": 0, "sub": 0}

    def sub(text):
        text = re.sub(r"\\cite\{([^}]*)\}",
                      lambda m: "[" + ", ".join(
                          str(cites.get(k.strip(), "?"))
                          for k in m.group(1).split(",")) + "]", text)
        text = re.sub(r"\\ref\{([^}]*)\}",
                      lambda m: labels.get(m.group(1), "?"), text)
        return text

    def markup(text):
        return render_inline(sub(text.replace("\n", " ")))

    # ---- front matter
    title = re.search(r"\\title\{(.*?)\}\s*\\titlerunning", body, re.S)
    flow.append(Paragraph(markup(title.group(1)), st["title"]))
    author = re.search(r"\\author\{(.*?)\}\s*\\authorrunning", body, re.S)
    flow.append(Paragraph(markup(author.group(1).replace("\\and", "&nbsp;&nbsp;&nbsp;")),
                          st["author"]))
    inst = re.search(r"\\institute\{(.*?)\}\s*\\maketitle", body, re.S)
    flow.append(Paragraph(markup(inst.group(1).replace("\\and", "<br/>")
                                 .replace("\\\\", "<br/>")), st["institute"]))
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}",
                         body, re.S).group(1)
    kw = re.search(r"\\keywords\{(.*?)\}\s*$", abstract, re.S)
    abst = (abstract[:kw.start()] if kw else abstract).strip()
    flow.append(Paragraph("<b>Abstract.</b>&nbsp; " + markup(abst),
                          st["abstract"]))
    if kw:
        flow.append(Paragraph("<b>Keywords:</b>&nbsp; " +
                              markup(kw.group(1).replace("\\and", ", ")),
                              st["abstract"]))
    flow.append(Spacer(1, 4))

    # ---- body walk
    main = body_par[body_par.find("\\end{abstract}") + len("\\end{abstract}"):]
    first = True
    blocks = main.split("\n@\n")
    i = 0
    while i < len(blocks):
        blk = blocks[i].strip()
        i += 1
        if not blk:
            continue
        m = re.match(r"\\section(\*?)\{(.*?)\}(.*)$", blk, re.S)
        if m and not blk.startswith("\\subsection"):
            head, rest = m.group(2), m.group(3)
            if not m.group(1):
                state["sec"] += 1
                state["sub"] = 0
                prefix = f"{state['sec']}&nbsp;&nbsp;"
            else:
                prefix = ""
            flow.append(Paragraph(f"<b>{prefix}{markup(head)}</b>", st["sec"]))
            rest = re.sub(r"\\label\{[^}]*\}", "", rest).strip()
            first = True
            if rest:
                blocks.insert(i, rest)
            continue
        m = re.match(r"\\subsection\{(.*?)\}(.*)$", blk, re.S)
        if m:
            head, rest = m.group(1), m.group(2)
            state["sub"] += 1
            prefix = f"{state['sec']}.{state['sub']}&nbsp;&nbsp;"
            flow.append(Paragraph(f"<b>{prefix}{markup(head)}</b>",
                                  st["subsec"]))
            rest = re.sub(r"\\label\{[^}]*\}", "", rest).strip()
            first = True
            if rest:
                blocks.insert(i, rest)
            continue
        m = re.match(r"\\subsubsection\{(.*?)\}(.*)$", blk, re.S)
        if m:
            head, rest = m.group(1), m.group(2).strip()
            flow.append(Paragraph(f"<b>{markup(head)}</b>&nbsp; " +
                                  markup(rest), st["runin"]))
            first = False
            continue
        if blk.startswith("\\begin{figure}"):
            add_figure(blk, flow, st, markup, figmap)
            first = True
            continue
        if blk.startswith("\\begin{table}"):
            add_table(blk, flow, st, markup, tabmap)
            first = True
            continue
        if "\\begin{equation}" in blk:
            parts = re.split(r"(\\begin\{equation\}.*?\\end\{equation\})",
                             blk, flags=re.S)
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                if part.startswith("\\begin{equation}"):
                    add_equation(part, flow, st, eqmap)
                else:
                    part = re.sub(r"\\label\{[^}]*\}", "", part).strip()
                    if part:
                        flow.append(Paragraph(markup(part),
                                              st["body"] if first
                                              else st["bodyi"]))
                first = False
            continue
        if blk.startswith("\\bibliograph"):
            continue
        blk = re.sub(r"\\label\{[^}]*\}", "", blk).strip()
        if not blk:
            continue
        flow.append(Paragraph(markup(blk), st["body"] if first else st["bodyi"]))
        first = False

    # ---- references
    for key, num in sorted(cites.items(), key=lambda kv: kv[1]):
        chunk = bib.get(key)
        txt = bib_text(chunk) if chunk else f"MISSING ENTRY: {key}"
        txt = txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        flow.append(Paragraph(f"{num}.&nbsp; {txt}", st["ref"]))
    return flow


def main():
    flow = build()
    out = os.path.join(ROOT, "article.pdf")
    doc = BaseDocTemplate(out, pagesize=A4,
                          leftMargin=(PAGE_W - FRAME_W) / 2,
                          rightMargin=(PAGE_W - FRAME_W) / 2,
                          topMargin=(PAGE_H - TEXT_H) / 2,
                          bottomMargin=(PAGE_H - TEXT_H) / 2,
                          title="Automatic Recognition of Quranic Tajweed Rules")
    frame = Frame((PAGE_W - FRAME_W) / 2, (PAGE_H - TEXT_H) / 2,
                  FRAME_W, TEXT_H, leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0, id="main")
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame])])
    doc.build(flow)
    n = pymupdf.open(out).page_count
    open(os.path.join(ROOT, "build", "pagecount.txt"), "w").write(f"{n}\n")
    print(f"pages: {n} (limit 17)")


if __name__ == "__main__":
    main()
