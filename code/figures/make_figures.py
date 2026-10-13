"""Publication figures for the coverage/repetition grokking study.

Figure contracts (per qinyan-nature-figures):

Figure 1 — Coverage (main evidence)
  Conclusion: at a matched optimization budget, unique-example coverage
  determines whether and when test accuracy transitions, whereas training
  accuracy saturates within ~500 steps at every coverage.
  Panel map: (a) test acc vs steps, R=1, six coverages; (b) train acc vs
  steps, same; (c) GrokTime vs coverage, individual seeds + median,
  right-censored runs marked at 20k with arrows; (d) final test acc vs
  coverage, individual seeds + median.
  Statistics contract: median lines across 5 seeds; no inference panels.
  Encoding: viridis (colorblind-safe) sequential for coverage, identical
  across panels.

Figure 2 — Repetition (secondary evidence)
  Conclusion: blocked repetition accelerates the transition at sufficient
  coverage and cannot rescue insufficient coverage; interleaved repetition
  is close to the no-repetition baseline.
  Panel map: (a) test acc vs steps at C=55 for R in {1,2,4,8}, blocked;
  (b) GrokTime vs R for blocked, three coverages, seeds + medians;
  (c) GrokTime vs R for interleaved, three coverages; (d) final test acc
  vs R, both modes, three coverages.
  Encoding: Okabe-Ito colors fixed per coverage; mode encoded by marker
  and line style (solid/blocked, open/interleaved).

Figure 3 — Weight norm (exploratory)
  Conclusion: weight-norm trajectories separate grokked from censored
  runs; final norm correlates with GrokTime across grokked runs.
  Panel map: (a) weight norm vs steps for R=1 at C in {25,55,85};
  (b) final weight norm vs GrokTime scatter (grokked runs, all conditions),
  Spearman rho annotated; (c) weight norm vs steps at C=55 for blocked
  R in {1,2,4,8}.

Export contract: PDF vector for LaTeX inclusion + 300 dpi PNG raster check;
all plotted values exported as source-data CSVs; fixed random seeds; fonts
DejaVu Sans; 5.5 in text width; min 7 pt final font; lines >= 0.8 pt.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
          "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
    try:
        fm.fontManager.addfont(f)
    except Exception:
        pass
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

plt.rcParams.update({
    "font.sans-serif": ["DejaVu Sans"],
    "font.family": "sans-serif",
    "font.size": 7,
    "axes.labelsize": 7.5,
    "axes.titlesize": 7.5,
    "xtick.labelsize": 6.5,
    "ytick.labelsize": 6.5,
    "legend.fontsize": 6.3,
    "axes.linewidth": 0.6,
    "lines.linewidth": 1.0,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "legend.frameon": False,
    "pdf.fonttype": 42,
})

REPO = Path(__file__).resolve().parents[2]
MAIN = REPO / "data"
FIG = REPO / "results" / "figures"
FIG.mkdir(parents=True, exist_ok=True)
MAX_STEPS = 20_000

df = pd.read_csv(MAIN / "summary.csv")
hist = pd.read_csv(MAIN / "history.csv")

COVS_ALL = [25, 35, 45, 55, 70, 85]
COVS_R = [25, 35, 55, 85]
REPS = [2, 4, 8]
SEEDS = [0, 1, 2, 3, 4]

cov_cmap = plt.cm.viridis(np.linspace(0.12, 0.9, len(COVS_ALL)))
COV_COLOR = dict(zip(COVS_ALL, cov_cmap))
RC = {25: "#8C6D31", 35: "#0072B2", 55: "#E69F00", 85: "#009E73"}   # Okabe-Ito
REP_SHADE = {1: "#666666", 2: "#0072B2", 4: "#D55E00", 8: "#CC79A7"}


def letter(ax, s):
    ax.text(-0.16, 1.06, s, transform=ax.transAxes,
            fontsize=9, fontweight="bold", va="top")


def median_curve(ax, cov, rep, mode, col, seeds=SEEDS, color=None, label=None,
                 lw=1.2, alpha=0.22, ls="-"):
    vals = []
    for s in seeds:
        q = hist.query("coverage==@cov and repetition==@rep and mode==@mode and seed==@s")
        vals.append(q.sort_values("step")[col].to_numpy())
    n = min(len(v) for v in vals)
    arr = np.column_stack([v[:n] for v in vals])
    med = np.median(arr, axis=1)
    steps = q.sort_values("step")["step"].to_numpy()[:n]
    lo, hi = np.percentile(arr, [25, 75], axis=1)
    ax.fill_between(steps, lo, hi, color=color, alpha=alpha, lw=0)
    ax.plot(steps, med, color=color, label=label, lw=lw, ls=ls)
    return steps, med


# ===========================================================================
# Figure 1 — coverage
# ===========================================================================
fig, axes = plt.subplots(1, 4, figsize=(5.5, 2.05), constrained_layout=True)

ax = axes[0]
for cov in COVS_ALL[::-1]:
    median_curve(ax, cov, 1, "blocked", "test_acc", color=COV_COLOR[cov],
                 label=f"{cov}%")
ax.set_xscale("log")
ax.set_xlim(100, MAX_STEPS)
ax.set_ylim(-0.02, 1.05)
ax.set_xlabel("Optimization steps")
ax.set_ylabel("Test accuracy")
ax.axhline(0.95, color="0.75", lw=0.5, ls=":")
ax.legend(ncol=2, loc="upper left", bbox_to_anchor=(0.0, 1.02),
          handlelength=1.0, columnspacing=0.7, labelspacing=0.32,
          borderaxespad=0.0, handletextpad=0.4)
letter(ax, "a")

ax = axes[1]
for cov in COVS_ALL[::-1]:
    median_curve(ax, cov, 1, "blocked", "train_acc", color=COV_COLOR[cov])
ax.set_xscale("log")
ax.set_xlim(100, MAX_STEPS)
ax.set_ylim(-0.02, 1.05)
ax.set_xlabel("Optimization steps")
ax.set_ylabel("Training accuracy")
letter(ax, "b")

ax = axes[2]
for cov in COVS_ALL:
    q = df.query("coverage==@cov and repetition==1 and mode=='blocked'")
    y = q["grok_step_filled"].to_numpy()
    cens = q["grok_censored"].to_numpy()
    n_ok = int((~cens).sum())
    if n_ok:
        xj = cov + np.linspace(-1.6, 1.6, n_ok)
        ax.scatter(xj, y[~cens], s=10, color=COV_COLOR[cov], zorder=3, clip_on=False)
    med = np.median(y)
    ax.plot([cov], [med], marker="D", ms=4, color=COV_COLOR[cov],
            mec="black", mew=0.5, zorder=4, clip_on=False)
    if cens.any():
        ax.annotate("", xy=(cov, MAX_STEPS * 1.32), xytext=(cov, MAX_STEPS * 0.78),
                    arrowprops=dict(arrowstyle="-|>", color=COV_COLOR[cov], lw=1.3))
        n_str = f"{cens.sum()}/{len(cens)}"
        # placed to the right of the arrow shaft (not stacked above the arrow
        # heads), so adjacent censoring labels (25%: 5/5, 35%: 3/5) cannot
        # merge into one another at the narrow panel width
        ax.text(cov + 1.8, MAX_STEPS * 1.06, n_str, fontsize=5.5, va="center",
                color="0.35", ha="left")
ax.set_yscale("log")
ax.set_ylim(500, MAX_STEPS * 2.4)
ax.set_xlim(20, 90)
ax.set_xlabel("Coverage (%)")
ax.set_ylabel("GrokTime (steps)")
ax.axhline(MAX_STEPS, color="0.85", lw=0.5, ls="--")
letter(ax, "c")

ax = axes[3]
for cov in COVS_ALL:
    q = df.query("coverage==@cov and repetition==1 and mode=='blocked'")
    acc = q["final_test_acc"].to_numpy()
    x = cov + np.linspace(-1.4, 1.4, len(acc))
    ax.scatter(x, acc, s=10, color=COV_COLOR[cov], zorder=3)
    ax.plot([cov], [np.median(acc)], marker="D", ms=4, color=COV_COLOR[cov],
            mec="black", mew=0.5, zorder=4)
ax.set_ylim(-0.02, 1.05)
ax.set_xlabel("Coverage (%)")
ax.set_ylabel("Final test accuracy")
ax.axhline(0.95, color="0.75", lw=0.5, ls=":")
letter(ax, "d")

fig.savefig(FIG / "fig1_coverage.pdf")
fig.savefig(FIG / "fig1_coverage.png", dpi=300)
plt.close(fig)

# source data
sd = df.query("repetition==1 and mode=='blocked'")[
    ["coverage", "seed", "grok_step_filled", "grok_censored",
     "final_test_acc", "mem_step", "final_wnorm"]]
sd.to_csv(FIG / "fig1_sourcedata.csv", index=False)

# ===========================================================================
# Figure 2 — repetition
# ===========================================================================
fig, axes = plt.subplots(1, 4, figsize=(5.5, 2.55))
fig.subplots_adjust(left=0.088, right=0.995, top=0.97, bottom=0.15, wspace=0.52)

ax = axes[0]
for rep in (1, 2, 4, 8):
    mode = "blocked"
    median_curve(ax, 55, rep, mode, "test_acc", color=REP_SHADE[rep],
                 label=f"R={rep}")
ax.set_xscale("log")
ax.set_xlim(100, MAX_STEPS)
ax.set_ylim(-0.02, 1.05)
ax.set_xlabel("Optimization steps")
ax.set_ylabel("Test accuracy")
ax.axhline(0.95, color="0.75", lw=0.5, ls=":")
ax.legend(ncol=2, loc="upper left", handlelength=1.2, columnspacing=0.8,
          labelspacing=0.25)
letter(ax, "a")

for ax, mode, lab in ((axes[1], "blocked", "b"), (axes[2], "interleaved", "c")):
    for cov in COVS_R:
        for rep in [1] + REPS:
            m = "blocked" if rep == 1 else mode
            if rep not in (1, 2, 4, 8):
                continue
            if cov == 25 and not (rep == 1 or (mode == "blocked" and rep in (4, 8)) or
                                 (mode == "interleaved" and rep == 8)):
                continue   # only existing D-arm cells
            q = df.query("coverage==@cov and repetition==@rep and mode==@m")
            if not len(q):
                continue
            y = q["grok_step_filled"].to_numpy()
            cens = q["grok_censored"].to_numpy()
            x = rep + (cov - 55) * 0.06
            if (~cens).any():
                ax.scatter(np.full((~cens).sum(), x) + np.linspace(-0.25, 0.25, (~cens).sum()),
                           y[~cens], s=10, color=RC[cov], zorder=3)
            if cens.any():
                ax.annotate("", xy=(x, MAX_STEPS * 1.5), xytext=(x, MAX_STEPS * 0.75),
                            arrowprops=dict(arrowstyle="-|>", color=RC[cov], lw=1.3))
            med = np.median(y)
            mk = "o" if (rep == 1 or mode == "blocked") else "s"
            fc = RC[cov] if (rep == 1 or mode == "blocked") else "white"
            ax.plot([x], [med], marker=mk, ms=4.5, mfc=fc, mec=RC[cov], mew=0.8,
                    zorder=4, clip_on=False, ls="none")
    ax.set_xscale("log", base=2)
    ax.set_xticks([1, 2, 4, 8])
    ax.set_xticklabels(["1", "2", "4", "8"])
    ax.set_xlim(0.85, 9.2)
    ax.set_ylim(500, MAX_STEPS * 2.6)
    ax.set_xlabel("Repetition R")
    ax.set_ylabel("GrokTime (steps)" if lab == "b" else "")
    ax.axhline(MAX_STEPS, color="0.88", lw=0.5, ls="--")
    letter(ax, lab)

ax = axes[3]
for cov in COVS_R:
    xs, ys, ms, fcs = [], [], [], []
    for mode in ("blocked", "interleaved"):
        for rep in [1] + REPS:
            m = "blocked" if rep == 1 else mode
            if cov == 25 and not (rep == 1 or (mode == "blocked" and rep in (4, 8)) or
                                 (mode == "interleaved" and rep == 8)):
                continue   # only existing D-arm cells
            q = df.query("coverage==@cov and repetition==@rep and mode==@m")
            if not len(q):
                continue
            acc = q["final_test_acc"].to_numpy()
            for i, a in enumerate(acc):
                xs.append(rep + (cov - 55) * 0.05 + (-0.12 if mode == "interleaved" else 0.12))
                ys.append(a)
    xs, ys = np.array(xs), np.array(ys)
    ax.scatter(xs, ys, s=8, color=RC[cov], zorder=3)
    for rep in [1] + REPS:
        m = "blocked"
        q = df.query("coverage==@cov and repetition==@rep and mode==@m")
        if len(q):
            ax.plot([rep + (cov - 55) * 0.05], [np.median(q["final_test_acc"])],
                    marker="D", ms=3.5, color=RC[cov], mec="black", mew=0.4, zorder=4)
ax.set_xscale("log", base=2)
ax.set_xticks([1, 2, 4, 8])
ax.set_xticklabels(["1", "2", "4", "8"])
ax.set_xlim(0.85, 9.2)
ax.set_ylim(-0.02, 1.05)
ax.set_xlabel("Repetition R")
ax.set_ylabel("Final test accuracy")
ax.axhline(0.95, color="0.75", lw=0.5, ls=":")
letter(ax, "d")

fig.savefig(FIG / "fig2_repetition.pdf")
fig.savefig(FIG / "fig2_repetition.png", dpi=300)
plt.close(fig)

sd2 = df[["mode", "coverage", "repetition", "seed", "grok_step_filled",
          "grok_censored", "final_test_acc", "mem_step"]]
sd2.to_csv(FIG / "fig2_sourcedata.csv", index=False)

# ===========================================================================
# Figure 3 — weight norm (exploratory)
# ===========================================================================
fig, axes = plt.subplots(1, 3, figsize=(5.5, 1.95), constrained_layout=True)

ax = axes[0]
for cov in COVS_R:
    if cov == 25:
        median_curve(ax, cov, 1, "blocked", "wnorm", color="#BB5566", label="25% (no grok)")
        continue
    median_curve(ax, cov, 1, "blocked", "wnorm", color=RC[cov], label=f"{cov}%")
ax.set_xscale("log")
ax.set_xlim(100, MAX_STEPS)
ax.set_xlabel("Optimization steps")
ax.set_ylabel(r"Weight $\ell_2$ norm")
# legend moved to the empty upper-right corner: the 25% (no-grok) curve runs
# flat through the lower-left/lower-center region where the legend used to sit
ax.legend(ncol=2, loc="upper right", handlelength=1.2, columnspacing=0.8,
          labelspacing=0.25)
letter(ax, "a")

ax = axes[1]
g = df[df["grok_censored"] == False]
for mode, cov, rep in [("blocked", 55, 1), ("blocked", 85, 1), ("blocked", 35, 4),
                       ("blocked", 55, 4), ("blocked", 85, 4), ("interleaved", 55, 4)]:
    q = g.query("mode==@mode and coverage==@cov and repetition==@rep")
    ax.scatter(q["grok_step_filled"], q["final_wnorm"], s=10, color=RC.get(cov, "0.4"),
               marker="o" if mode == "blocked" else "s", zorder=3)
rho = stats.spearmanr(g["grok_step_filled"], g["final_wnorm"])
ax.set_xscale("log")
# explicit, evenly spaced (in log) ticks replace matplotlib's auto minor
# labels (2x10^3, 3x10^3, 10^4 crowded together near the panel bottom)
ax.set_xticks([2e3, 5e3, 1e4, 2e4])
ax.set_xticklabels([r"$2{\times}10^{3}$", r"$5{\times}10^{3}$",
                    r"$10^{4}$", r"$2{\times}10^{4}$"])
ax.minorticks_off()
ax.set_xlabel("GrokTime (steps, grokked runs)")
ax.set_ylabel(r"Final weight $\ell_2$ norm")
ax.text(0.04, 0.95, f"Spearman $\\rho$ = {rho.statistic:.2f}",
        transform=ax.transAxes, va="top", fontsize=6.5)
letter(ax, "b")

ax = axes[2]
median_curve(ax, 25, 1, "blocked", "wnorm", color=REP_SHADE[1], label="R=1")
median_curve(ax, 25, 4, "blocked", "wnorm", color=REP_SHADE[4], label="R=4")
median_curve(ax, 25, 8, "blocked", "wnorm", color=REP_SHADE[8], label="R=8")
median_curve(ax, 25, 8, "interleaved", "wnorm", color="#336699", ls="--",
             label="R=8 intl.")
ax.set_xscale("log")
ax.set_xlim(100, MAX_STEPS)
ax.set_xlabel("Optimization steps")
ax.set_ylabel(r"Weight $\ell_2$ norm")
ax.legend(ncol=2, loc="upper left", handlelength=1.2, columnspacing=0.8,
          labelspacing=0.25)
letter(ax, "c")

fig.savefig(FIG / "fig3_wnorm.pdf")
fig.savefig(FIG / "fig3_wnorm.png", dpi=300)
plt.close(fig)

sd3 = g[["mode", "coverage", "repetition", "seed", "grok_step_filled", "final_wnorm"]]
sd3.to_csv(FIG / "fig3_sourcedata.csv", index=False)

print("figures written to", FIG)
