# Automatic Recognition of Quranic Tajweed Rules Across Riwayat

Conference-ready manuscript (Springer LNCS) assembled from the supplied
section documents. See **CHANGES.md** for the editorial summary and page
estimation, and **OPEN_ITEMS.md** for the 11 marked gaps plus the bibliography
work stream.

## Repository layout

| Path | Purpose |
|---|---|
| `paper.tex` | the manuscript (authoritative source) |
| `refs.bib` | placeholder bibliography — replace key-by-key with the real `.bib` |
| `llncs.cls`, `splncs04.bst` | Springer LNCS class v2.24 and bibliography style |
| `figures/fig1_framework.pdf` | pipeline schematic (vector) |
| `figures/fig2_features_vs_mfcc.pdf` | proposed descriptors vs MFCC baseline (vector) |
| `figures/fig3_cross_riwayah.pdf` | cross-riwayah Macro-F1 matrix (vector) |
| `tools/make_figures.py` | regenerates the three figures from the reported numbers |
| `tools/render_preview.py` | LNCS-geometry page-count proof renderer (no TeX needed) |
| `article.pdf` | paginated proof used for the page estimate |
| `build/pagecount.txt` | current proxy page count |
| `build/manuscript_editable.docx` | Word export for line editing |
| `*.docx` (root) | the original supplied section documents (input material) |

## Compiling

```bash
pdflatex paper && bibtex paper && pdflatex paper && pdflatex paper
```

Only `amsmath`, `amssymb`, `graphicx`, `xcolor`, `url` and `microtype` are
required; the file contains no Arabic script and no Unicode beyond UTF-8
punctuation, so plain pdfLaTeX suffices. Page limit: **17 pages including
references, tables and figures**; the current content is estimated at **16**.

## Page-count proof without a TeX installation

```bash
python3 tools/render_preview.py     # writes article.pdf + pagecount.txt
```

The renderer reproduces the LNCS printing area (12.2 × 19.3 cm on A4), the LNCS
heading hierarchy, caption placement and bibliography size, and typesets all
mathematics with a real math engine. Its frame is 0.2 cm narrower than LNCS on
purpose, so the reported count errs on the safe side.

## Regenerating figures

```bash
python3 tools/make_figures.py
```

Every plotted value is taken verbatim from the supplied experimental outputs;
the scripts contain no fitted or interpolated data.
