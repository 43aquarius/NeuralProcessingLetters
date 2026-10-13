"""task_equivalence.py -- Task 3: TOST equivalence testing for the repetition
null on log10 GrokTime, in cells with no censoring (coverage 55 and 85).

IMPORTANT: the equivalence margin must be justified on substantive grounds
BEFORE looking at the results, and that justification must be written into
the paper.  The margin is a user setting (--margins), never silently chosen.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import stats_core as sc


def _cell(runs, cov, R, mode=None):
    m = (runs["coverage"] == cov) & (runs["R"] == R)
    if R > 1 and mode is not None:
        m &= runs["mode"] == mode
    return runs[m].sort_values("seed")


def _contrasts():
    out = []
    for cov in (55, 85):
        for mode in ("blocked", "interleaved"):
            for R in (2, 4, 8):
                out.append((f"C{cov} {mode}: R1 vs R{R}", (cov, 1, None), (cov, R, mode)))
        for R in (2, 4, 8):
            out.append((f"C{cov} R{R}: blocked vs interleaved",
                        (cov, R, "blocked"), (cov, R, "interleaved")))
    return out


def tost_section(runs, margins, master_seed, n_boot_unused=None):
    """Run permutation TOST and Welch TOST for every contrast at every margin.

    `margins` are fractional deviations (e.g. 0.10 = +/-10%): the
    equivalence band on the GrokTime scale is the ratio interval
    (1/(1+f), 1+f), i.e. +/- log10(1+f) on the log10 scale.  The
    `margin_ratio` column reports the upper bound 1+f.  Equivalence at
    alpha=0.05 iff max(p1, p2) < 0.05.
    """
    rows = []
    small_rows = []
    for label, sa, sb in _contrasts():
        ga, gb = _cell(runs, *sa), _cell(runs, *sb)
        if ga["censored"].any() or gb["censored"].any():
            raise RuntimeError(f"contrast {label} has censored runs; TOST is "
                               "restricted to cells with no censoring")
        x = np.log10(ga["grok_time"].values.astype(float))
        y = np.log10(gb["grok_time"].values.astype(float))
        for f in margins:
            m = float(np.log10(1.0 + f))
            tp = sc.tost_permutation(x, y, m)
            tw = sc.tost_welch(x, y, m)
            rows.append(dict(
                contrast=label, margin_fraction=f, margin_ratio=round(1.0 + f, 4),
                mean_log10_ratio=round(tp["D_obs"], 4),
                mean_ratio=round(10 ** tp["D_obs"], 3),
                perm_ci90_lo_ratio=round(10 ** tp["ci90_lo"], 3),
                perm_ci90_hi_ratio=round(10 ** tp["ci90_hi"], 3),
                perm_p1=round(tp["p1"], 5), perm_p2=round(tp["p2"], 5),
                perm_pmax=round(tp["p_max"], 5),
                welch_ci90_lo_ratio=round(10 ** tw["ci90_lo"], 3),
                welch_ci90_hi_ratio=round(10 ** tw["ci90_hi"], 3),
                welch_p1=round(tw["p1"], 5), welch_p2=round(tw["p2"], 5),
                welch_pmax=(None if tw["p_max"] is None else round(tw["p_max"], 5)),
                method=("permutation TOST on mean log10 difference "
                        "(252-assignment enumeration; shifted-null one-sided tests) "
                        "and Welch t TOST; two-sided 90% CIs; margin f means "
                        "GrokTime ratio band (1/(1+f), 1+f)")))
        # smallest margin at which equivalence would be declared (both methods)
        grid = 10 ** np.arange(np.log10(1.01), np.log10(3.0), 0.004)
        sm_perm = sm_welch = None
        for mr in grid:
            m = float(np.log10(mr))
            tp = sc.tost_permutation(x, y, m)
            if tp["p_max"] < 0.05 and sm_perm is None:
                sm_perm = float(mr)
            tw = sc.tost_welch(x, y, m)
            if tw["p_max"] is not None and tw["p_max"] < 0.05 and sm_welch is None:
                sm_welch = float(mr)
            if sm_perm is not None and sm_welch is not None:
                break
        small_rows.append(dict(
            contrast=label,
            smallest_margin_ratio_perm=sm_perm,
            smallest_margin_ratio_welch=sm_welch,
            note=("smallest upper-ratio margin of the band (1/m, m), grid "
                  "1.01..3.0, at which max(p1,p2) < 0.05; None = equivalence "
                  "not declarable within the grid")))
    # pooled within-cell SD of log10 GrokTime in the no-censoring cells
    variances, ns = [], []
    for cov in (55, 85):
        cells = [(cov, 1, None)] + [(cov, R, md) for R in (2, 4, 8)
                                     for md in ("blocked", "interleaved")]
        for s in cells:
            g = _cell(runs, *s)
            variances.append(np.log10(g["grok_time"].values.astype(float)).var(ddof=1))
            ns.append(len(g))
    variances, ns = np.array(variances), np.array(ns)
    pooled_sd = float(np.sqrt((variances * (ns - 1)).sum() / (ns - 1).sum()))
    return pd.DataFrame(rows), pd.DataFrame(small_rows), pooled_sd


def power_section(pooled_sd, margins, master_seed, B=2000):
    """Simulation-based power / MDE for a 5-vs-5 comparison, using the
    observed pooled within-cell SD of log10 GrokTime (NOT a pre-study power
    analysis).  Returns (power_df, mde_rows)."""
    rng = sc.rng_for(master_seed, 601)
    deltas = [0.0, 0.02, 0.05, 0.08, 0.11, 0.15, 0.20, 0.25, 0.30]
    margin_logs = [float(np.log10(1.0 + f)) for f in margins]
    power = sc.tost_power_sim(pooled_sd, margin_logs, deltas, n_per_group=5,
                              B=B, rng=rng)
    mde_rows = []
    for f in margins:
        sub = power[(power["margin_ratio"] == round(1.0 + f, 10))
                    & power["power_tost"].notna()]
        ok = sub[sub["power_tost"] >= 0.8]
        largest = ok["true_log10_ratio"].max() if len(ok) else None
        pw0 = sub[np.isclose(sub["true_log10_ratio"], 0.0)]["power_tost"]
        mde_rows.append(dict(
            margin_fraction=f, margin_ratio=round(1.0 + f, 4),
            power_at_true_ratio_1=float(pw0.iloc[0]) if len(pw0) else np.nan,
            largest_true_ratio_with_power_ge_0p8=(None if largest is None
                                                 else round(10 ** largest, 3)),
            note=("largest true GrokTime ratio still declared equivalent with "
                  "power >= 0.8; based on observed pooled SD "
                  f"{pooled_sd:.4f} of log10 GrokTime")))
    # MDE of the two-sided permutation test of the difference
    pw_diff = power.groupby("true_log10_ratio")["power_permtest_diff"].first()
    det = pw_diff[pw_diff >= 0.8]
    mde_perm = round(10 ** det.index.max(), 3) if len(det) else None
    return power, pd.DataFrame(mde_rows), mde_perm


def run(runs, margins, cfg):
    tost, smallest, pooled_sd = tost_section(runs, margins, cfg["MASTER_SEED"])
    power, mde, mde_perm = power_section(pooled_sd, margins, cfg["MASTER_SEED"],
                                         B=cfg["N_POWER_SIM"])
    return dict(tost=tost, smallest=smallest, power=power, mde=mde,
                mde_perm=mde_perm, pooled_sd=pooled_sd)
