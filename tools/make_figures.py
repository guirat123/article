#!/usr/bin/env python3
"""Generate the vector figures for the LNCS manuscript.

Every number plotted here is taken verbatim from the supplied experimental
outputs (sections 5.2, 5.9 and the corpus description in 3.1/3.2).  Nothing is
interpolated or invented.

Output: figures/fig1_framework.pdf, figures/fig2_features_vs_mfcc.pdf,
        figures/fig3_perclass.pdf, figures/fig4_ablation.pdf,
        figures/fig5_balancing.pdf, figures/fig6_cross_riwayah.pdf
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman", "Times"],
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(OUT, exist_ok=True)

# Text width of the LNCS printing area: 12.2 cm
FULL_W = 12.2 / 2.54          # inches


# --------------------------------------------------------------------------
# Figure 1 -- Riwayah-aware processing framework
# --------------------------------------------------------------------------
def fig1_framework():
    fig = plt.figure(figsize=(FULL_W, 2.62))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 36)
    ax.axis("off")

    band_h = 9.2
    box_h = 5.8

    def band(y, label):
        ax.add_patch(FancyBboxPatch((0.4, y), 99.2, band_h,
                                    boxstyle="round,pad=0,rounding_size=0.8",
                                    facecolor="#f4f4f4", edgecolor="#9a9a9a",
                                    linewidth=0.6, zorder=0))
        ax.text(1.4, y + band_h - 1.0, label, fontsize=5.8, style="italic",
                color="#333333", va="top", ha="left", zorder=3)

    def box(x, y, w, text, fc="white", fs=5.0):
        ax.add_patch(FancyBboxPatch((x, y), w, box_h,
                                    boxstyle="round,pad=0,rounding_size=0.7",
                                    facecolor=fc, edgecolor="#222222",
                                    linewidth=0.7, zorder=2))
        ax.text(x + w / 2.0, y + box_h / 2.0, text, fontsize=fs, ha="center",
                va="center", zorder=3, linespacing=1.25)

    def arrow(x1, y1, x2, y2):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                     arrowstyle="-|>", mutation_scale=7,
                                     linewidth=0.7, color="#222222", zorder=4))

    # ---- band A : corpus construction
    yA = 25.6
    band(yA, "A.  Corpus construction (Sec. 4)")
    box(1.6, yA + 0.7, 21.5,
        "MP3Quran recordings\n3 riwayahs $\\times$ 5 reciters\nSurahs 78--114", fc="#e8eef7")
    box(27.5, yA + 0.7, 21.5,
        "Forced alignment\n(2 procedures)\nmanual reconciliation", fc="#e8eef7")
    box(53.4, yA + 0.7, 21.5,
        "7,998 ayah clips\n11.17 h $\\cdot$ mono 16 kHz\nJSON timestamps", fc="#e8eef7")
    box(78.3, yA + 0.7, 20.3,
        "Quality control\nrecording / boundary /\nintegrity checks", fc="#e8eef7")
    arrow(23.3, yA + 3.6, 27.3, yA + 3.6)
    arrow(49.2, yA + 3.6, 53.2, yA + 3.6)
    arrow(75.1, yA + 3.6, 78.1, yA + 3.6)

    # ---- band B : annotation
    yB = 13.9
    band(yB, "B.  Tajweed annotation (Sec. 5)")
    box(1.6, yB + 0.7, 21.5,
        "Rule specification\n(Tajweed references)", fc="#eef4ea")
    box(27.5, yB + 0.7, 21.5,
        "Automatic candidate\nextraction (Python)", fc="#eef4ea")
    box(53.4, yB + 0.7, 21.5,
        "Manual acoustic\nboundary annotation", fc="#eef4ea")
    box(78.3, yB + 0.7, 20.3,
        "Expert verification\n+ adjudication", fc="#eef4ea")
    arrow(23.3, yB + 3.6, 27.3, yB + 3.6)
    arrow(49.2, yB + 3.6, 53.2, yB + 3.6)
    arrow(75.1, yB + 3.6, 78.1, yB + 3.6)

    # ---- band C : analysis + modelling
    yC = 2.2
    band(yC, "C.  Analysis, modelling and evaluation (Secs. 6--9)")
    box(1.6, yC + 0.7, 21.5,
        "8 acoustic\ndescriptors (Sec. 6)", fc="#f7efe6")
    box(27.5, yC + 0.7, 21.5,
        "5-class task +\nimbalance handling", fc="#f7efe6")
    box(53.4, yC + 0.7, 21.5,
        "SVM $\\cdot$ RF $\\cdot$ KNN\nXGBoost $\\cdot$ MLP", fc="#f7efe6")
    box(78.3, yC + 0.7, 20.3,
        "Ablation, MFCC baseline,\ncross-riwayah, bootstrap", fc="#f7efe6")
    arrow(23.3, yC + 3.6, 27.3, yC + 3.6)
    arrow(49.2, yC + 3.6, 53.2, yC + 3.6)
    arrow(75.1, yC + 3.6, 78.1, yC + 3.6)

    # vertical links between bands
    for x in (12.3, 38.2, 64.1, 88.4):
        arrow(x, yA + 0.55, x, yB + band_h + 0.1)
        arrow(x, yB + 0.55, x, yC + band_h + 0.1)

    fig.savefig(os.path.join(OUT, "fig1_framework.pdf"))
    plt.close(fig)


# --------------------------------------------------------------------------
# Figure 2 -- Proposed representation vs. MFCC baseline (Macro-F1)
# --------------------------------------------------------------------------
def fig2_features_vs_mfcc():
    models = ["SVM", "Random\nForest", "KNN", "XGBoost", "MLP"]
    proposed = [0.6920, 0.6683, 0.6687, 0.6935, 0.6219]
    mfcc = [0.6473, 0.5335, 0.5351, 0.5744, 0.5646]
    gain = [p - m for p, m in zip(proposed, mfcc)]

    x = np.arange(len(models))
    w = 0.36
    fig, ax = plt.subplots(figsize=(FULL_W * 0.78, 2.05))
    b1 = ax.bar(x - w / 2, mfcc, w, label="MFCC + $\\Delta$ + $\\Delta\\Delta$",
                color="#b9c6d8", edgecolor="#33475f", linewidth=0.6)
    b2 = ax.bar(x + w / 2, proposed, w, label="Proposed descriptors",
                color="#4a6fa5", edgecolor="#22364f", linewidth=0.6)

    for rect, val in list(zip(b1, mfcc)) + list(zip(b2, proposed)):
        ax.text(rect.get_x() + rect.get_width() / 2, val + 0.005,
                f"{val:.4f}", ha="center", va="bottom", fontsize=6.0)
    for xi, g, p, m in zip(x, gain, proposed, mfcc):
        ax.text(xi, max(p, m) + 0.028, f"+{g:.4f}", ha="center", va="bottom",
                fontsize=5.8, color="#7a2b12", fontweight="bold")

    ax.set_ylabel("Macro-F1", fontsize=7.2)
    ax.set_ylim(0.45, 0.80)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=6.6)
    ax.tick_params(axis="y", labelsize=6.2)
    ax.yaxis.grid(True, linewidth=0.4, color="#cccccc")
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(fontsize=6.6, frameon=False, loc="lower center", ncol=2,
              bbox_to_anchor=(0.5, 1.02))
    fig.tight_layout(pad=0.35)
    fig.savefig(os.path.join(OUT, "fig2_features_vs_mfcc.pdf"))
    plt.close(fig)


# --------------------------------------------------------------------------
# Figure 3 -- Cross-riwayah generalisation (Macro-F1)
# --------------------------------------------------------------------------
def fig3_cross_riwayah():
    riw = ["Hafs", "Qalun", "Warsh"]
    # rows = training riwayah, cols = testing riwayah; Macro-F1 values exactly as
    # reported in Sec. 5.9 of the supplied results:
    #   Hafs->Qalun .6686, Hafs->Warsh .6602, Qalun->Hafs .6584,
    #   Qalun->Warsh .6718, Warsh->Hafs .6712, Warsh->Qalun .6626
    M = np.array([
        [np.nan, 0.6686, 0.6602],   # train Hafs
        [0.6584, np.nan, 0.6718],   # train Qalun
        [0.6712, 0.6626, np.nan],   # train Warsh
    ])

    fig, ax = plt.subplots(figsize=(FULL_W * 0.46, 1.95))
    masked = np.ma.masked_invalid(M)
    cmap = plt.get_cmap("YlGnBu").copy()
    cmap.set_bad("#ececec")
    im = ax.imshow(masked, cmap=cmap, vmin=0.655, vmax=0.675, aspect="auto")

    for i in range(3):
        for j in range(3):
            if np.isnan(M[i, j]):
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                           facecolor="#ececec",
                                           edgecolor="white", hatch="///",
                                           linewidth=0.8))
                ax.text(j, i, "not\nevaluated", ha="center", va="center",
                        fontsize=4.9, color="#666666", style="italic")
            else:
                ax.text(j, i, f"{M[i, j]:.4f}", ha="center", va="center",
                        fontsize=6.4,
                        color="white" if M[i, j] > 0.6685 else "#10233a")

    ax.set_xticks(range(3))
    ax.set_yticks(range(3))
    ax.set_xticklabels(riw, fontsize=6.6)
    ax.set_yticklabels(riw, fontsize=6.6)
    ax.set_xlabel("Test riwayah", fontsize=6.8)
    ax.set_ylabel("Training riwayah", fontsize=6.8)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=5.6, length=2)
    cbar.set_label("Macro-F1", fontsize=6.4)
    fig.tight_layout(pad=0.3)
    fig.savefig(os.path.join(OUT, "fig6_cross_riwayah.pdf"))
    plt.close(fig)



# --------------------------------------------------------------------------
# Figure 4 -- Feature ablation (XGBoost)
# --------------------------------------------------------------------------
def fig4_ablation():
    cfg = ["All\nfeatures", "Remove\nnasality", "Remove\nduration",
           "Remove depth\nmetric", "Remove\nspectral", "Nasality\nonly",
           "Depth+duration\nonly"]
    acc = [0.7202, 0.6964, 0.5798, 0.5571, 0.6905, 0.2393, 0.6571]
    bal = [0.6953, 0.6580, 0.5572, 0.5222, 0.6519, 0.2415, 0.6713]
    f1 = [0.6935, 0.6544, 0.5587, 0.5169, 0.6512, 0.2290, 0.6424]
    x = np.arange(len(cfg))
    w = 0.26
    fig, ax = plt.subplots(figsize=(FULL_W, 1.95))
    ax.bar(x - w, acc, w, label="Accuracy", color="#c9d3e0",
           edgecolor="#33475f", linewidth=0.5)
    ax.bar(x, bal, w, label="Balanced accuracy", color="#8fa8c8",
           edgecolor="#33475f", linewidth=0.5)
    ax.bar(x + w, f1, w, label="Macro-F1", color="#4a6fa5",
           edgecolor="#22364f", linewidth=0.5)
    ax.axhline(0.6935, color="#7a2b12", linewidth=0.7, linestyle=":")
    ax.text(len(cfg) - 0.4, 0.705, "full-set Macro-F1 = 0.6935",
            fontsize=6.0, color="#7a2b12", ha="right")
    ax.set_xticks(x)
    ax.set_xticklabels(cfg, fontsize=6.2)
    ax.set_ylabel("Score", fontsize=7.6)
    ax.set_ylim(0, 0.80)
    ax.tick_params(axis="y", labelsize=6.6)
    ax.yaxis.grid(True, linewidth=0.4, color="#cccccc")
    ax.set_axisbelow(True)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    ax.legend(fontsize=6.8, frameon=False, ncol=3, loc="upper center",
              bbox_to_anchor=(0.5, 1.16))
    fig.tight_layout(pad=0.35)
    fig.savefig(os.path.join(OUT, "fig4_ablation.pdf"))
    plt.close(fig)


# --------------------------------------------------------------------------
# Figure 5 -- Class-balancing configurations (XGBoost)
# --------------------------------------------------------------------------
def fig5_balancing():
    cfg = ["Original", "Class\nweighting", "SMOTE", "Borderline-\nSMOTE",
           "SMOTE +\nweighting"]
    acc = [0.7357, 0.7202, 0.7119, 0.7071, 0.7119]
    bal = [0.6617, 0.6953, 0.7121, 0.6899, 0.7121]
    f1 = [0.6592, 0.6935, 0.6951, 0.6812, 0.6951]
    rec = [0.0678, 0.3390, 0.4915, 0.3559, 0.4915]
    f1m = [0.1111, 0.3478, 0.3742, 0.3307, 0.3742]
    x = np.arange(len(cfg))
    w = 0.16
    fig, ax = plt.subplots(figsize=(FULL_W, 1.95))
    series = [("Accuracy", acc, "#c9d3e0"), ("Balanced accuracy", bal, "#8fa8c8"),
              ("Macro-F1", f1, "#4a6fa5"),
              ("Idgham bila-Ghunnah recall", rec, "#d9a441"),
              ("Idgham bila-Ghunnah F1", f1m, "#b0651a")]
    for i, (lab, vals, col) in enumerate(series):
        ax.bar(x + (i - 2) * w, vals, w, label=lab, color=col,
               edgecolor="#333333", linewidth=0.4)
    ax.set_xticks(x)
    ax.set_xticklabels(cfg, fontsize=6.4)
    ax.set_ylabel("Score", fontsize=7.6)
    ax.set_ylim(0, 0.82)
    ax.tick_params(axis="y", labelsize=6.6)
    ax.yaxis.grid(True, linewidth=0.4, color="#cccccc")
    ax.set_axisbelow(True)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    ax.legend(fontsize=6.2, frameon=False, ncol=3, loc="upper center",
              bbox_to_anchor=(0.5, 1.34))
    fig.tight_layout(pad=0.35)
    fig.savefig(os.path.join(OUT, "fig5_balancing.pdf"))
    plt.close(fig)


# --------------------------------------------------------------------------
# Figure 6 -- Per-class separability: recall spread and ROC-AUC (XGBoost)
# --------------------------------------------------------------------------
def fig6_perclass():
    classes = ["Idgham\nbi-Gh.", "Idgham\nbila-Gh.", "Qalqalah\nMushad.",
               "Qalqalah\nSughra", "Qalqalah\nWusta"]
    lo = [0.995, 0.017, 0.58, 0.55, 0.88]
    hi = [1.00, 0.49, 0.72, 0.55, 0.92]
    xgb = [1.00, 0.34, 0.68, 0.55, 0.91]
    auc = [1.00, 0.87, 0.89, 0.84, 0.99]
    x = np.arange(len(classes))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(FULL_W, 1.85),
                                 gridspec_kw={"width_ratios": [1.25, 1]})
    for xi, l, h, g in zip(x, lo, hi, xgb):
        a1.plot([xi, xi], [l, h], color="#4a6fa5", linewidth=5.0,
                solid_capstyle="butt", alpha=0.55, zorder=1)
        a1.plot([xi], [g], marker="D", markersize=3.4, color="#7a2b12",
                zorder=3, markeredgecolor="white", markeredgewidth=0.4)
    a1.plot([], [], color="#4a6fa5", linewidth=5.0, alpha=0.55,
            label="recall range over 5 classifiers")
    a1.plot([], [], marker="D", markersize=3.4, color="#7a2b12",
            linestyle="none", label="XGBoost recall")
    a1.set_xticks(x)
    a1.set_xticklabels(classes, fontsize=5.6)
    a1.set_ylabel("Recall", fontsize=7.4)
    a1.set_ylim(0, 1.06)
    a1.tick_params(axis="y", labelsize=6.6)
    a1.yaxis.grid(True, linewidth=0.4, color="#cccccc")
    a1.set_axisbelow(True)
    for s_ in ("top", "right"):
        a1.spines[s_].set_visible(False)
    a1.legend(fontsize=5.8, frameon=False, loc="lower center",
              bbox_to_anchor=(0.62, 0.0))
    a1.annotate("single reported value", xy=(3, 0.53), xytext=(1.62, 0.80),
                fontsize=5.4, color="#555555",
                arrowprops=dict(arrowstyle="-", linewidth=0.5,
                                color="#555555"))

    a2.bar(x, auc, 0.62, color="#8fa8c8", edgecolor="#33475f", linewidth=0.5)
    for xi, v in zip(x, auc):
        a2.text(xi, v + 0.012, f"{v:.2f}", ha="center", fontsize=6.0)
    a2.set_xticks(x)
    a2.set_xticklabels(["bi-Gh.", "bila-Gh.", "Mushad.", "Sughra", "Wusta"],
                       fontsize=5.0)
    a2.set_ylabel("ROC-AUC (XGBoost, OvR)", fontsize=7.0)
    a2.set_ylim(0.75, 1.045)
    a2.tick_params(axis="y", labelsize=6.6)
    a2.yaxis.grid(True, linewidth=0.4, color="#cccccc")
    a2.set_axisbelow(True)
    for s_ in ("top", "right"):
        a2.spines[s_].set_visible(False)
    fig.tight_layout(pad=0.4)
    fig.savefig(os.path.join(OUT, "fig3_perclass.pdf"))
    plt.close(fig)


if __name__ == "__main__":
    fig4_ablation()
    fig5_balancing()
    fig6_perclass()
    print("extra figures written")
