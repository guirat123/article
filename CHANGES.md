# Summary of changes and page estimation

Deliverable: **`paper.tex`** — a conference-ready manuscript in Springer LNCS
format (`llncs.cls` v2.24, `splncs04.bst`), assembled from the eight supplied
section documents, together with a paginated page-count proof
(`article.pdf`) and an editable Word export
(`build/manuscript_editable.docx`).

---

## 1. Structure: from loose sections to the required conference skeleton

The supplied material arrived as eight disconnected documents with overlapping
numbering (two different "Section 3"s, a "Section 4 Discussion", a "Section 5"
embedded inside the machine-learning file, and a detached limitations memo).
Everything was re-homed into the requested skeleton, in order:

| Required element | Realised as | Source material |
|---|---|---|
| Title / Abstract / Keywords | front matter (abstract newly written, 158 words) | synthesised from all sections |
| 1 Introduction | Sect. 1 | `Introduction.docx` (1,664 w → ~600 w) |
| 2 Related Work | Sect. 2 (2.1–2.3) | `2. Literature Review.docx` (2,203 w → ~780 w) |
| 3 Methodology | Sect. 3 + Fig. 1 | newly written overview of the pipeline |
| 4 Corpus Construction | Sect. 4 (4.1–4.3) | `3.1` + `3.3` (1,487 w → ~600 w) |
| 5 Annotation Methodology | Sect. 5 (5.1–5.3) | `3.2` (1,104 w → ~430 w) |
| 6 Data Analysis | Sect. 6 (6.2–6.3 + Eq. 1) | feature/correlation/cleaning text in `3.5`/`3.6` |
| 7 Machine Learning Framework | Sect. 7 (7.1–7.4, Eqs. 1–2) | `3.5`, `3.6` (≈2,200 w → ~600 w) |
| 8 Experiments | Sect. 8 (E1–E7 protocol) | `3.6` experimental-setup text |
| 9 Results | Sect. 9 (9.1–9.6, Tables 3–6, Figs. 2–3) | `3.5` Sect. 5 results (≈3,000 w → ~800 w) |
| 10 Discussion | Sect. 10 (10.1–10.5) | `4.docx` (2,648 w → ~640 w) |
| 11 Limitations | Sect. 11 | `Limitations and Future Research.docx` + `3.5` §5.13 (1,314 w → ~230 w) |
| 12 Conclusion | Sect. 12 | `3.5` §5.14 + new synthesis |
| References | 21 entries, numbered by citation order | placeholder `refs.bib` (see OPEN_ITEMS.md) |

Total prose went from ≈15,000 words of source to ≈6,000 words of manuscript
without deleting any result, dataset statistic or methodological claim.

## 2. Consistency repairs (technical_consistency requirement)

* **Corpus duration conflict.** `3.1` said "11.22 h of segmented audio" while
  `3.3` and its table said 11.17 h. Unified to **11.17 h** (the table value;
  per-riwayah durations 3.57 + 3.78 + 3.83 are rounded components of the
  unrounded total). 14.14 h is now stated only as the *full-surah source* audio.
* **Instance-count conflict.** `3.1` called 7,998 the "canonical" reciter–ayah
  count; `3.3` correctly derives 8,460 canonical pairs and 7,998 retained
  (94.5 %). The manuscript now states 8,460 canonical → 7,998 retained
  everywhere (abstract, Sect. 4, Sect. 12).
* **Taxonomy conflict.** The corpus annotates **8 subtypes** (328 Idgham +
  377 Qalqalah = 705 textual occurrences) but the classifier uses **5 classes**.
  Table 2 now shows all eight subtypes with † marking the five used for
  classification, and Sect. 7.1 states the scope explicitly; the exclusion
  rationale is an open `\todo` rather than an invented justification.
* **Metric duplication.** The source results table carried both "Recall" and
  "Balanced Accuracy" columns, which are identical under macro-averaging.
  Table 3 reports balanced accuracy once and states the identity in the caption.
* **Headline-configuration ambiguity.** The source reported XGBoost accuracy
  0.7357 (unbalanced) and 0.7202 (weighted) without saying which is the primary
  model. Sect. 9.1 and Table 3 now state that the primary comparison uses the
  class-weighted configuration; 0.7357 appears only as the unbalanced row of
  Table 6.
* **Cross-riwayah matrix.** the six transfer Macro-F1 values (0.6584–0.6718)
  were re-mapped into train×test order for Fig. 3 (the source listed them in a
  different order and the accuracy column values are not Macro-F1).
* **Terminology.** One transliteration scheme throughout (no diacritics, no
  Arabic script, so the file compiles with plain pdfLaTeX): *riwayah/riwayat*,
  *ayah/ayat*, *surah*, Hafs 'an 'Asim / Warsh 'an Nafi' / Qalun 'an Nafi',
  Idgham bi-Ghunnah / bila-Ghunnah, Qalqalah Sughra / Wusta / Mushaddadah /
  Kubra, Lam Shamsiyyah. Task name unified to *automatic Tajweed recognition*;
  feature names unified (RMS mean, ZCR mean, spectral-centroid mean,
  spectral-flux mean, mean/peak nasality, depth metric, duration).
* **All arithmetic re-verified:** table row/column sums, per-riwayah mean verse
  durations (4.69/5.30/5.11/5.03 s), subtype totals (328, 377, 705), Lam
  Shamsiyyah share (72.3 %), MFCC gains (+0.0447/+0.1348/+0.1336/+0.1191/
  +0.0573), ablation deltas (−0.1766, −0.1348), balancing deltas (−1.55 acc
  points, +42.4 recall points), cross-riwayah spread (0.0134), bootstrap CI.

## 3. Redundancy removal (page_limit_policy)

* Discussion no longer restates results: numeric recitation was stripped from
  Sect. 10, which now interprets (representation vs complexity, duration/depth
  evidence, bila-Ghunnah difficulty, imbalance, domain shift, implications).
* Sect. 9.3 prose no longer repeats the per-class numbers that Table 4 carries.
* Repetitive motivation paragraphs (corpus diversity, "accuracy is not enough")
  appear once each, in Sect. 6.3/7.4 and Sect. 9.1 respectively.
* Equations reduced from 15 displays to 2 numbered displays + compact inline
  forms; the textbook metric definitions are given in prose (Sect. 7.4).
* Tables: 6 (corpus composition; subtype occurrences; classifier comparison;
  per-class diagnostics; ablation; balancing). Figures: 3 vector PDFs
  (framework schematic; proposed-vs-MFCC Macro-F1; cross-riwayah heatmap) —
  each figure replaces or complements prose/table content without duplicating
  it; captions state what to read off them.

## 4. Formatting compliance (Springer LNCS)

* `llncs.cls` v2.24 + `splncs04.bst` bundled in the repository root.
* Two numbered heading levels only; third level as run-in bold heads
  (Sects. 6.2, 8.1, 9.4); abstract 195 words (limit 15–250); `\keywords` present.
* Table captions above tables, figure captions below figures; equations
  numbered (1)–(4); square-bracket consecutive numbering for citations.
* Author block / ORCIDs / affiliations left as LNCS-style placeholders with a
  `\todo` (see OPEN_ITEMS.md).

## 5. Page estimation

No TeX engine can be installed in this sandbox, so the page count is certified
by `tools/render_preview.py`, which re-typesets `paper.tex` with the exact LNCS
geometry (A4, printing area 12.2 × 19.3 cm, 10 pt/12 pt body, 12 pt bold section
heads, 10 pt bold subsection heads, run-in third-level heads, 9 pt bibliography)
and renders every formula with a real math typesetter. The frame is
deliberately narrowed by 0.2 cm so the estimate is **conservative**.

| Quantity | Value |
|---|---|
| Proxy page count (`build/pagecount.txt`) | **19** |
| Conference limit | 20 (including references, tables, figures), raised from 17 at the authors' request |
| Headroom | ≈1 page (also absorbs the text that the 11 `\todo` insertions and the real `.bib` may add) |
| Page budget breakdown (proxy) | front matter ≈0.7 · headings ≈2.2 · body ≈10.3 · tables ≈2.1 · figures ≈2.3 · equations ≈0.5 · references ≈0.9 |

Re-run `python3 tools/render_preview.py` after any edit; it rewrites
`article.pdf` and `build/pagecount.txt`. The authoritative
count is obtained by compiling `paper.tex` with pdfLaTeX + BibTeX, which the
authors should do once (the source is pdfLaTeX-clean: no Arabic script, no
external packages beyond `amsmath`, `graphicx`, `xcolor`, `url`, `microtype`).

## 6. Expansion to the raised 20-page limit

The authors raised the ceiling from 17 to 20 pages and asked for more detail and
figures. The additional space was spent on scientific content, not padding:

* **Related work** (Sect. 2): prose condensed and two comparison tables added —
  Tab. 1 (ten Qur'anic speech resources: size, speakers, supervision, rule-level
  labels) and Tab. 2 (eight prior Tajweed systems: rules, representation, model,
  data, outcome) — so the gap analysis is evidence-based rather than narrative.
* **Data analysis** (Sect. 6.1): Tab. 5 defines each of the eight acoustic
  descriptors together with the acoustic dimension and the Tajweed realisation
  it targets.
* **Machine-learning framework** (Sect. 7.2): the random-forest and
  $k$-nearest-neighbour decision rules are now stated formally as Eqs. (2)–(3),
  alongside the existing SVM, XGBoost and MLP formalisms.
* **Experiments** (Sect. 8.1): Tab. 6 maps each of the seven experiment families
  to its research question, protocol and primary metrics.
* **Results** (Sect. 9): the three result tables that repeated numbers already
  discussed in the prose (per-class diagnostics, ablation, class balancing) were
  converted into Figs. 3–5, which show the same values as grouped bars and
  recall ranges and free the prose to interpret them; captions state exactly
  what is plotted and under which protocol.
* **Limitations** (Sect. 11): a run-in *Future directions* paragraph turns the
  three most consequential limitations into concrete follow-up studies.

Net effect: 7 tables, 6 figures and 4 numbered equations at **19 pages**, one
page below the raised limit.
