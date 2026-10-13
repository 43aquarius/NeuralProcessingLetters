"""task_survival.py -- Task 2: survival analysis of GrokTime (right-censored at 20,000).

Manual Kaplan-Meier, manual log-rank (permutation p-values), restricted mean
survival time with bootstrap CIs, Fisher exact + Clopper-Pearson for
low-event cells, and one stratified Cox model.  No lifelines.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import stats_core as sc


def _cond(runs, cov, R, mode=None):
    """Select the runs of one cell; R=1 is the shared baseline (mode vacuous)."""
    m = (runs["coverage"] == cov) & (runs["R"] == R)
    if R > 1 and mode is not None:
        m &= runs["mode"] == mode
    return runs[m].sort_values("seed")


def _times_events(df, horizon):
    t = np.where(df["censored"], horizon, df["grok_time"]).astype(float)
    e = (~df["censored"].astype(bool)).values
    return t, e


def _cond_label(cov, R, mode=None):
    if R == 1:
        return f"C{cov} R1"
    return f"C{cov} R{R} {mode}"


def km_section(runs, horizon):
    """KM table for each of the 27 conditions + per-condition RMST."""
    rows = []
    rmst_rows = []
    for (cov, R, mode), g in runs.groupby(["coverage", "R", "mode"], sort=True):
        lab = _cond_label(cov, R, mode)
        t, e = _times_events(g, horizon)
        tab = sc.km_table(t, e)
        tab.insert(0, "condition", lab)
        tab.insert(1, "coverage", cov)
        tab.insert(2, "R", R)
        tab.insert(3, "mode", mode)
        rows.append(tab)
        rmst_rows.append(dict(
            condition=lab, coverage=cov, R=R, mode=mode, n=len(g),
            events=int(e.sum()), censored=int((~e).sum()),
            rmst=sc.rmst_from_km(t, e, horizon, 100.0)))
    return pd.concat(rows, ignore_index=True), pd.DataFrame(rmst_rows)


def _plot_km(ax, t, e, label, color, horizon):
    tab = sc.km_table(t, e)
    ts = np.concatenate([[0.0], tab["time"].values, [horizon]])
    ss = np.concatenate([[1.0], tab["survival"].values, [tab["survival"].iloc[-1] if len(tab) else 1.0]])
    ax.step(ts, ss, where="post", color=color, label=label, linewidth=1.6,
            zorder=3)
    cens = t[~e]
    if len(cens):
        tick_x, tick_y = [], []
        for c in np.unique(cens):
            s = 1.0
            for _, r in tab.iterrows():
                if r["time"] <= c:
                    s = r["survival"]
            tick_x.append(c)
            tick_y.append(s)
        ax.plot(tick_x, tick_y, linestyle="none", marker="|",
                markersize=10, markeredgewidth=1.5, color=color, zorder=4)


def make_figures(runs, outdir, horizon):
    figs = []
    cov_palette = {25: "#882255", 35: "#CC6677", 45: "#DDCC77", 55: "#117733",
                   70: "#6699CC", 85: "#332288"}
    r_palette = {1: "#000000", 2: "#882255", 4: "#CC6677", 8: "#44AA99"}

    def _style(ax):
        ax.set_xlabel("Optimization steps")
        ax.set_ylabel("Fraction not yet grokked")
        ax.set_xlim(0, 20500)      # slightly past the budget so censoring ticks
        ax.set_ylim(-0.02, 1.05)  # at 20,000 are fully inside the axes
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])

    # (a) R = 1 curves by coverage (legend outside, below the axes)
    fig, ax = plt.subplots(figsize=(5.6, 4.5), constrained_layout=True)
    for cov in sorted(runs["coverage"].unique()):
        g = runs[(runs["coverage"] == cov) & (runs["R"] == 1)]
        t, e = _times_events(g, horizon)
        _plot_km(ax, t, e, f"{cov}% ({int(e.sum())}/5 grokked)", cov_palette[cov], horizon)
    _style(ax)
    handles, labels_ = ax.get_legend_handles_labels()
    fig.legend(handles, labels_, title="Coverage at $R=1$", fontsize=8,
               frameon=False, loc="outside lower center", ncol=3)
    for ext in ("pdf", "png"):
        p = outdir / f"figures/fig_km_a_R1_by_coverage.{ext}"
        fig.savefig(p, dpi=300 if ext == "png" else None)
        figs.append(p)
    plt.close(fig)

    # (b) blocked and (c) interleaved: R in {1,2,4,8} at coverage 35/55/85
    # (one shared legend below the panels)
    for mode, tag in (("blocked", "b"), ("interleaved", "c")):
        fig, axes = plt.subplots(1, 3, figsize=(10.5, 4.0), sharey=True,
                                 constrained_layout=True)
        handles, labels_ = None, None
        for k, (ax, cov) in enumerate(zip(axes, (35, 55, 85))):
            for R in (1, 2, 4, 8):
                g = _cond(runs, cov, R, mode if R > 1 else None)
                t, e = _times_events(g, horizon)
                _plot_km(ax, t, e, f"$R$={R} ({int(e.sum())}/5 grokked)",
                         r_palette[R], horizon)
            _style(ax)
            if k > 0:               # shared y-axis: label only the left panel
                ax.set_ylabel("")
            ax.set_title(f"{cov}% coverage, {mode}", fontsize=10)
            if handles is None:
                handles, labels_ = ax.get_legend_handles_labels()
        fig.legend(handles, labels_, fontsize=8, ncol=4, frameon=False,
                   loc="outside lower center")
        for ext in ("pdf", "png"):
            p = outdir / f"figures/fig_km_{tag}_{mode}.{ext}"
            fig.savefig(p, dpi=300 if ext == "png" else None)
            figs.append(p)
        plt.close(fig)
    return figs


def logrank_section(runs, horizon, seed, n_mc, max_enum):
    rng = sc.rng_for(seed, 201)
    rows = []

    def add(family, contrast, sub, note=""):
        if len(sub) == 0 or sub["censored"].all():
            rows.append(dict(family=family, contrast=contrast, n=len(sub),
                             events=int((~sub["censored"]).sum()), chi2=np.nan,
                             df=np.nan, p_perm=np.nan, p_chi2=np.nan,
                             method="skipped", note=note or "no runs / no events"))
            return False
        t, e = _times_events(sub, horizon)
        if len(np.unique(sub["group"])) == 2:
            labels = sub["group"].values
        else:
            levels = sorted(sub["group"].unique())
            labels = np.searchsorted(levels, sub["group"].values)
        res = sc.logrank_test(t, e, labels, rng, n_mc=n_mc, max_enumerate=max_enum)
        rows.append(dict(family=family, contrast=contrast, n=len(sub),
                         events=int(e.sum()), chi2=round(res["chi2"], 4),
                         df=res["df"], p_perm=round(res["p_perm"], 5),
                         p_chi2=round(res["p_chi2"], 5), method=res["method"],
                         note=note))
        return True

    base = runs.copy()
    base["group"] = 0

    # (i) coverage levels at R = 1
    sub = base[base["R"] == 1].copy()
    sub["group"] = sub["coverage"].values
    add("coverage_R1", "k-sample across coverage (25..85) at R=1", sub)
    for a, b in ((85, 45), (85, 25)):
        sub = base[(base["R"] == 1) & (base["coverage"].isin([a, b]))].copy()
        sub["group"] = (sub["coverage"] == a).astype(int)
        add("coverage_R1", f"{a}% vs {b}% at R=1", sub)

    # (ii) R=1 vs R in {2,4,8} within coverage, blocked and interleaved
    for mode in ("blocked", "interleaved"):
        for cov in (35, 55, 85):
            r1 = base[(base["R"] == 1) & (base["coverage"] == cov)].copy()
            r1["group"] = 0
            for R in (2, 4, 8):
                rr = _cond(base, cov, R, mode).copy()
                rr["group"] = 1
                sub = pd.concat([r1, rr])
                add(f"rep_{mode}", f"C{cov} {mode}: R1 vs R{R}", sub)
            # k-sample across R within (coverage, mode)
            parts = [r1]
            for R in (2, 4, 8):
                p = _cond(base, cov, R, mode).copy()
                p["group"] = R
                parts.append(p)
            add(f"rep_{mode}", f"C{cov} {mode}: k-sample across R (1,2,4,8)",
                pd.concat(parts))

    # (iii) blocked vs interleaved at matched (coverage, R)
    pairs = [(c, r) for c in (35, 55, 85) for r in (2, 4, 8)] + [(25, 8)]
    for cov, R in pairs:
        blk = _cond(base, cov, R, "blocked").copy(); blk["group"] = 0
        itl = _cond(base, cov, R, "interleaved").copy(); itl["group"] = 1
        add("mode", f"C{cov} R{R}: blocked vs interleaved", pd.concat([blk, itl]),
            note="" if (~pd.concat([blk, itl])["censored"].astype(bool)).any()
            else "zero events in both groups; time-based test degenerate")

    return pd.DataFrame(rows)


def rmst_section(runs, horizon, seed, n_boot):
    rng = sc.rng_for(seed, 301)
    _, per_cond = km_section(runs, horizon)  # cheap; recomputed per-condition RMST
    rows = []
    specs = ([("rep_blocked", c, R) for c in (35, 55, 85) for R in (2, 4, 8)]
             + [("rep_interleaved", c, R) for c in (35, 55, 85) for R in (2, 4, 8)]
             + [("mode", c, R) for c in (35, 55, 85) for R in (2, 4, 8)] + [("mode", 25, 8)])
    for fam, cov, R in specs:
        if fam == "mode":
            a = _cond(runs, cov, R, "blocked"); b = _cond(runs, cov, R, "interleaved")
            lab = f"C{cov} R{R}: blocked vs interleaved"
        else:
            a = _cond(runs, cov, 1); b = _cond(runs, cov, R, fam.split("_")[1])
            lab = f"C{cov} {fam.split('_')[1]}: R1 vs R{R}"
        t1, e1 = _times_events(a, horizon)
        t2, e2 = _times_events(b, horizon)
        r = sc.rmst_bootstrap_diff(t1, e1, t2, e2, rng, horizon, 100.0, B=n_boot)
        if e1.sum() + e2.sum() == 0:
            note = ("no events in either group: RMST equals the horizon by "
                    "construction and the bootstrap CI is degenerate [0, 0]; "
                    "see the Fisher exact table instead")
        else:
            note = ("bootstrap 95% CI of RMST difference (within-group "
                    "resampling); diff = RMST(first-named) - RMST(second-named)")
        rows.append(dict(family=fam, contrast=lab,
                         n1=len(a), events1=int(e1.sum()), n2=len(b),
                         events2=int(e2.sum()), rmst1=round(r["rmst1"], 1),
                         rmst2=round(r["rmst2"], 1), diff=round(r["diff"], 1),
                         ci_lo=round(r["ci_lo"], 1), ci_hi=round(r["ci_hi"], 1),
                         B=r["B"], note=note))
    return per_cond, pd.DataFrame(rows)


def fisher_section(runs, horizon):
    rows = []

    def one(cov, la, lb):
        a = _cond(runs, *la); b = _cond(runs, *lb)
        k1, n1 = int((~a["censored"]).sum()), len(a)
        k2, n2 = int((~b["censored"]).sum()), len(b)
        f = sc.fisher_exact_2x2(k1, n1, k2, n2)
        lo1, hi1 = sc.clopper_pearson(k1, n1)
        lo2, hi2 = sc.clopper_pearson(k2, n2)
        rows.append(dict(
            coverage=cov,
            contrast=f"{_cond_label(*la)} vs {_cond_label(*lb)}",
            k1=k1, n1=n1, k2=k2, n2=n2,
            p_fisher=round(f["p"], 5), OR=(None if f["OR"] == np.inf else round(f["OR"], 3)),
            cp1_lo=round(lo1, 4), cp1_hi=round(hi1, 4),
            cp2_lo=round(lo2, 4), cp2_hi=round(hi2, 4),
            note="two-sided Fisher exact; Clopper-Pearson 95% CIs per group"))

    for R in (2, 4, 8):
        one(35, (35, 1, None), (35, R, "blocked"))
        one(35, (35, 1, None), (35, R, "interleaved"))
        one(35, (35, R, "blocked"), (35, R, "interleaved"))
    one(25, (25, 1, None), (25, 4, "blocked"))
    one(25, (25, 1, None), (25, 8, "blocked"))
    one(25, (25, 8, "blocked"), (25, 8, "interleaved"))
    return pd.DataFrame(rows)


def cox_section(runs, horizon):
    a = runs[(runs["coverage"].isin([35, 55, 85])) & (runs["R"] == 1)].copy()
    b = runs[(runs["coverage"].isin([35, 55, 85])) & (runs["R"] > 1)
             & (runs["mode"] == "blocked")].copy()
    d = pd.concat([a, b])
    t, e = _times_events(d, horizon)
    z = np.concatenate([np.zeros(len(a)), np.ones(len(b))])
    s = d["coverage"].values
    return sc.cox_stratified(t, e, z, s), dict(
        n_ref=len(a), n_index=len(b), strata="coverage in {35,55,85}",
        index="blocked repetition R in {2,4,8} (z=1) vs R=1 (z=0)",
        events=int(e.sum()))


def run(runs, outdir, cfg):
    km_tables, per_cond = km_section(runs, cfg["HORIZON"])
    figs = make_figures(runs, outdir, cfg["HORIZON"])
    logrank = logrank_section(runs, cfg["HORIZON"], cfg["MASTER_SEED"],
                               cfg["N_PERM_MC"], cfg["MAX_ENUMERATE"])
    rmst_cond, rmst_diff = rmst_section(runs, cfg["HORIZON"], cfg["MASTER_SEED"],
                                         cfg["N_BOOT"])
    fisher = fisher_section(runs, cfg["HORIZON"])
    cox, cox_info = cox_section(runs, cfg["HORIZON"])
    return dict(km_tables=km_tables, rmst_per_condition=rmst_cond,
                rmst=rmst_diff, logrank=logrank, fisher=fisher,
                cox=cox, cox_info=cox_info, figures=figs)
