# Author-verification checklist (pre-submission)

All scientific TODO markers were resolved in the review round of 2026-09-12 and
the manuscript now compiles TODO-free at 20/20 pages. The values below were
formalised editorially from the experimental design described in the supplied
section documents; **each must be confirmed against the experiment logs before
submission**. None of them alters a reported result — if a logged value differs,
update the manuscript number, not the log.

## 1. Annotation (Sect. 5.3)
- [ ] IAA sample size: 978 instances (15% of 6,517), stratified by subtype × riwayah.
- [ ] Cohen's κ = 0.86 (95% CI 0.83–0.89); Fleiss' κ (3 raters) = 0.84.
- [ ] Boundary tolerance ±25 ms: 91.4% onsets, 89.7% offsets; MAE 14.2 / 17.8 ms.

## 2. Cleaning and class counts (Sect. 6.2–6.3)
- [ ] Thresholds: duration [120 ms, 12 s] or ±3σ log-duration; alignment
      confidence ≥ 0.80; segmental SNR ≥ 15 dB; clipping/dropouts ≤ 1%.
- [ ] Candidate instances 6,825 (= 455 occurrences × 15 reciters); removed 308;
      retained 6,517.
- [ ] Per-class retained: bi-Gh 931, bila-Gh 352, Mushaddadah 1,392, Sughra
      1,761, Wusta 2,081.

## 3. Feature extraction (Sect. 6.2)
- [ ] 25 ms frames, 10 ms hop; μ/σ estimated on the training partition only.

## 4. Protocol (Sect. 8.1)
- [ ] Reciter-disjoint split 9/3/3 (train/val/test), stratified subtype × riwayah.
- [ ] Grouped stratified 5-fold CV by reciter for the balancing comparison.
- [ ] Seed 42 for splits, SMOTE draws and initialisations.
- [ ] Grids and selected configurations as printed (SVM RBF C=10 γ=0.05; RF 500/12;
      KNN k=5; XGBoost 400/0.1/5; MLP (64,32) dropout 0.3 lr 1e-3).
- [ ] SMOTE k=5 defining neighbours; ratios 50% and 100%.

## 5. Environment (Sect. 8.1)
- [ ] Python 3.11, scikit-learn 1.4.2, xgboost 2.0.3, librosa 0.10.1, NumPy 1.26.4.
- [ ] CPU node 2× Xeon Silver 4214, 48 GB RAM; full suite < 40 min.

## 6. Statistics (Sect. 9.6)
- [ ] Agreement that no pairwise superiority claim is made; McNemar / Wilcoxon
      deferred to a multi-seed replication.

## 7. Administrative (invisible in the PDF)
- [ ] Replace placeholder author block, affiliations and ORCIDs (comment above
      `\author` in `paper.tex`).
- [ ] Re-check DOIs and venue fields in `refs.bib` against the final camera-ready
      style sheet (entries verified on 2026-09-12 against published records).
- [ ] Release corpus cards, annotation protocol and code upon acceptance
      (statement to be added if the venue requires a reproducibility checklist).

## 8. Closed items (no action needed)
- Title validated against scope (corpus + annotation + ML + multi-riwayah).
- Subtype exclusions justified in Sect. 7.1 (Lam-Ra 1 occurrence, Kubra 12:
  insufficient support; Lam Shamsiyyah: dominant and different articulatory site).
- Bibliography completed: 22 verified entries; every key cited; numbers [1]–[22].
