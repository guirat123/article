# Open items before submission

The manuscript `paper.tex` is complete and internally consistent, but the source
material supplied for this project explicitly flagged several reproducibility
details as **not available in the supplied outputs**. Nothing has been invented
to fill those gaps: each one is carried in the manuscript as a visible red
marker produced by `\todo{...}` (11 markers in total). Resolve each marker,
delete the corresponding text, and — once all are gone — remove the `\todo`
macro definition on line 18 of `paper.tex`.

| # | Location (line, section) | Marker | What is needed |
|---|--------------------------|--------|----------------|
| 1 | 26, title | confirm final title | Author sign-off on the working title |
| 2 | 35, front matter | replace author block, affiliations and ORCIDs | Real names, affiliations, e-mails, ORCID iDs |
| 3 | 298, Table 2 caption | confirm subtype-exclusion criteria | Why Lam Shamsiyyah, Idgham Lam-Ra and Qalqalah Kubra are annotated but excluded from the five-class task (frequency threshold? acoustic definability?) |
| 4 | 366, Sect. 5.3 | quantitative inter-annotator agreement statistic | e.g. Cohen's kappa for rule identification and a boundary-overlap measure for temporal localisation |
| 5 | 402, Sect. 6.2 | exact normalisation implementation and frame-level extraction parameters | frame length/hop, window, pre-emphasis, silence handling, amplitude normalisation; confirmation that standardisation statistics come from the training split only |
| 6 | 406, Sect. 6.2 | exact pre-/post-cleaning class counts and cleaning criteria | the per-class instance counts before and after cleaning, and the filtering / duplicate-detection / corrupted-segment rules |
| 7 | 472, Sect. 7.3 | SMOTE neighbour count and sampling ratio | `k_neighbours`, sampling strategy; likewise for Borderline-SMOTE |
| 8 | 510, Sect. 8.2 | split strategy, proportion, stratification and seed | train/test ratio, splitting unit (segment / verse / surah / reciter), stratification, random seed — required to exclude speaker-level leakage |
| 9 | 512, Sect. 8.2 | hyperparameter search and final configurations | searched grids, selection criterion, final parameters for SVM, RF, KNN, XGBoost, MLP |
| 10 | 513, Sect. 8.2 | Python/library versions and compute environment | Python, scikit-learn, xgboost, imbalanced-learn, librosa/feature-extraction versions; CPU/GPU/RAM |
| 11 | 671, Sect. 9.6 | McNemar and Wilcoxon statistics and p-values | XGBoost vs SVM (McNemar); original vs SMOTE over 5-fold CV (Wilcoxon). Until these exist the paper deliberately makes **no** statistical-superiority claim |

## Bibliography (separate work stream)

`refs.bib` is a **placeholder bibliography**: the reference list was never
supplied with the manuscript sections. Every entry currently carries only the
information that the supplied Literature Review itself states (author surnames
as given there, plus a descriptive title) and a `note = {TODO...}` field. All 21
citation keys are cited in the text and every entry is cited (no orphans, no
duplicates).

When you send the real `.bib`:

1. Replace the entries key-by-key — the keys are stable, so no `\cite` in
   `paper.tex` needs to change.
2. Keys ↔ bracket numbers already used in your Literature Review draft:
   `khan2023tarteel` = [1], `smail2024aqqd` = [5], `mohammed2018madd` = [10],
   `alagrami2021smartajweed` = [11], `omran2023cnn` = [12],
   `alahjal2023lstm` = [13]. The remaining keys correspond to works named but
   not numbered in that draft (EveryAyah, Ar-DAD, QDAT, the crowdsourced
   Quranic audio corpus, the Quran Recitations ASR corpus, Quran-Ayah-Corpus,
   Riwaya-ID, the Qalqalah VQ and MLP studies, TajweedAI, MP3Quran) plus the
   method references (wav2vec 2.0, Whisper, SMOTE, XGBoost).
3. Re-run `python3 tools/render_preview.py` to re-check the page count: real
   entries are usually a little shorter than the placeholders, so the budget
   should not get tighter.

## Optional strengthening (not blocking)

* A comparison-with-prior-systems table was deliberately **not** fabricated:
  reported accuracies in the literature differ in class definitions, splits,
  speaker independence and metrics, so a naive table would be misleading.
  Once the bibliography is final, a qualitative positioning paragraph or a
  carefully caveated table can be added in Sect. 9 if space allows (≈0.4 page
  of headroom exists at the current 16-page count).
* Figures `fig2`/`fig3` encode exactly the numbers in Sect. 9; if reviewers ask
  for confusion-matrix or ROC/PR figures, there is room for one more half-page
  figure.
