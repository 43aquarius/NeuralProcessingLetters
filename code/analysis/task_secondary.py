"""task_secondary.py -- Task 4: secondary outcomes.

All analyses in this module are exploratory and are labelled as such in the
output: MemTime repetition contrasts and trend, sub-critical final test
accuracy at 25% and 35% coverage, final L2 norm at 25% coverage, weight norm
at the matched step 1,000 (coverage 55), and the Spearman correlation
between final L2 norm and GrokTime among grokked runs.
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


def _lab(cov, R, mode=None):
    return f"C{cov} R{R}" if R == 1 else f"C{cov} R{R} {mode}"


def _exact_row(family, outcome, label, x, y, rng):
    e = sc.exact_mw_permutation(x, y)
    s = sc.scipy_mw_asymptotic(x, y)
    r = sc.rank_biserial(e["U1"], len(x), len(y))
    md = float(np.median(x) - np.median(y))
    hl = sc.hodges_lehmann(x, y)
    boot = sc.bootstrap_median_diff_ci(x, y, rng, B=10_000)
    return dict(family=family, outcome=outcome, contrast=label,
                n1=len(x), n2=len(y), U1=e["U1"], p_exact=round(e["p_exact"], 5),
                p_scipy_asymptotic=round(s["p_asymptotic"], 5),
                rank_biserial=round(r, 3), median_diff=round(md, 4),
                hodges_lehmann=round(hl, 4),
                boot_ci_lo=round(boot["ci_lo"], 4), boot_ci_hi=round(boot["ci_hi"], 4),
                direction=("first group smaller" if r > 0 else
                           "first group larger" if r < 0 else "no rank difference"),
                method=e["method"])


def exact_family(runs, family, outcome, contrasts, seed):
    """Run one Holm family of exact tests.  `contrasts` is a list of
    (label, selectorA, selectorB); x = first-named group."""
    rng = sc.rng_for(seed, 101)
    rows = []
    for label, sa, sb in contrasts:
        x = _cell(runs, *sa)[outcome].values.astype(float)
        y = _cell(runs, *sb)[outcome].values.astype(float)
        rows.append(_exact_row(family, outcome, label, x, y, rng))
    df = pd.DataFrame(rows)
    if len(df):
        df["p_holm"] = np.round(sc.holm(df["p_exact"].values), 5)
    return df


def memtime_section(runs, seed):
    """M1: R1 vs R4 / R1 vs R8 at coverage 35/55/85, blocked (Holm family).
    M2: exact permutation Jonckheere-Terpstra trend across R in {1,2,4,8}
    at each coverage (Holm family, one-sided increasing)."""
    contrasts = []
    for cov in (35, 55, 85):
        for R in (4, 8):
            contrasts.append((f"C{cov} blocked: R1 vs R{R} (MemTime)",
                              (cov, 1, None), (cov, R, "blocked")))
    m1 = exact_family(runs, "M1_memtime", "mem_time", contrasts, seed)
    rng = sc.rng_for(seed, 401)
    rows = []
    for cov in (35, 55, 85):
        groups = [_cell(runs, cov, R, "blocked")["mem_time"].values.astype(float)
                  for R in (1, 2, 4, 8)]
        res = sc.jt_permutation_p(groups, rng, n_mc=10_000)
        rows.append(dict(family="M2_memtrend", outcome="mem_time",
                         contrast=f"C{cov} blocked: trend across R in (1,2,4,8)",
                         J=res["J"], p_one_sided=round(res["p_one_sided"], 5),
                         method=res["method"]))
    m2 = pd.DataFrame(rows)
    if len(m2):
        m2["p_holm"] = np.round(sc.holm(m2["p_one_sided"].values), 5)
    return m1, m2


def counts_correct(runs, cov, R, mode):
    g = _cell(runs, cov, R, mode)
    n_test = int(g["n_test"].iloc[0])
    corr = g["final_test_acc"] * n_test
    ok = np.allclose(corr, np.round(corr), atol=1e-6)
    med = float(np.median(g["final_test_acc"]))
    return dict(n_test=n_test, granularity_pct=100.0 / n_test,
                median_correct=int(round(med * n_test)), exact=ok,
                median_acc=med)


def subcritical_section(runs, seed):
    """S1: final test accuracy at 25% coverage.  S2: final L2 norm at 25%.
    S3: blocked vs interleaved final accuracy at 35% coverage."""
    c25 = [("C25 blocked: R1 vs R4 (final acc)", (25, 1, None), (25, 4, "blocked")),
           ("C25 blocked: R1 vs R8 (final acc)", (25, 1, None), (25, 8, "blocked")),
           ("C25 R8: blocked vs interleaved (final acc)",
            (25, 8, "blocked"), (25, 8, "interleaved"))]
    s1 = exact_family(runs, "S1_c25_finalacc", "final_test_acc", c25, seed)
    for i, (label, sa, sb) in enumerate(c25):
        ca, cb = counts_correct(runs, *sa), counts_correct(runs, *sb)
        s1.loc[i, "n_correct_1"] = f"{ca['median_correct']}/{ca['n_test']}"
        s1.loc[i, "n_correct_2"] = f"{cb['median_correct']}/{cb['n_test']}"
    s1["granularity_note"] = ("1 correct answer = "
                              f"{counts_correct(runs, 25, 1, None)['granularity_pct']:.3f} "
                              "percentage points (n_test = 397)")

    c25w = [(l.replace("final acc", "final L2 norm"), a, b) for l, a, b in c25]
    s2 = exact_family(runs, "S2_c25_wnorm", "final_l2_norm", c25w, seed)

    c35 = [(f"C35 R{R}: blocked vs interleaved (final acc)",
            (35, R, "blocked"), (35, R, "interleaved")) for R in (2, 4, 8)]
    s3 = exact_family(runs, "S3_c35_mode_finalacc", "final_test_acc", c35, seed)
    g35 = counts_correct(runs, 35, 1, None)
    s3["granularity_note"] = ("1 correct answer = "
                              f"{g35['granularity_pct']:.3f} percentage "
                              "points (n_test = 344)")
    for i, (label, sa, sb) in enumerate(c35):
        ca, cb = counts_correct(runs, *sa), counts_correct(runs, *sb)
        s3.loc[i, "n_correct_1"] = f"{ca['median_correct']}/{ca['n_test']}"
        s3.loc[i, "n_correct_2"] = f"{cb['median_correct']}/{cb['n_test']}"
    return s1, s2, s3


def wnorm1000_section(runs, history, seed, step=1000, coverage=55):
    """Weight-norm at matched step 1,000, coverage 55: equivalence-style
    summary (median difference with a 90% percentile-bootstrap CI), replacing
    the manuscript's 'statistically indistinguishable' phrasing."""
    h = history[history["step"] == step].copy()
    h = h[h["coverage"] == coverage]
    rng = sc.rng_for(seed, 701)
    rows = []

    def val(cov, R, mode):
        m = (h["R"] == R)
        if R > 1:
            m &= h["mode"] == mode
        return m

    def get(R, mode=None):
        m = val(coverage, R, mode)
        g = h[m].sort_values("seed")
        assert len(g) == 5, f"expected 5 runs at C{coverage} R{R} {mode}"
        return g["l2_norm"].values.astype(float)

    contrasts = [(f"C{coverage} blocked: R1 vs R{R} (wnorm@{step})",
                  get(1), get(R, "blocked")) for R in (2, 4, 8)]
    contrasts += [(f"C{coverage} R{R}: blocked vs interleaved (wnorm@{step})",
                  get(R, "blocked"), get(R, "interleaved")) for R in (2, 4, 8)]
    for label, x, y in contrasts:
        d = x - y
        B = 10_000
        idx_x = rng.integers(0, len(x), size=(B, len(x)))
        idx_y = rng.integers(0, len(y), size=(B, len(y)))
        boots = np.median(x[idx_x], axis=1) - np.median(y[idx_y], axis=1)
        lo, hi = np.quantile(boots, [0.05, 0.95])
        rows.append(dict(family="W1_wnorm1000", outcome=f"l2_norm@step{step}",
                         contrast=label,
                         median_1=round(float(np.median(x)), 3),
                         median_2=round(float(np.median(y)), 3),
                         median_diff=round(float(np.median(d)), 3),
                         ci90_lo=round(float(lo), 3), ci90_hi=round(float(hi), 3),
                         mean_diff=round(float(d.mean()), 3),
                         note=("difference of medians with 90% percentile-bootstrap CI "
                               "(10,000 resamples, within-group); descriptive equivalence-"
                               "style summary, no p-value claimed")))
    return pd.DataFrame(rows)


def spearman_section(runs, seed):
    """Spearman rho between final L2 norm and GrokTime among grokked runs,
    overall and stratified by coverage, with permutation p-values."""
    rng = sc.rng_for(seed, 501)
    g = runs[~runs["censored"].astype(bool)]
    rows = []
    res = sc.spearman_permutation(g["final_l2_norm"].values,
                                  g["grok_time"].values.astype(float), rng)
    rows.append(dict(stratum="all grokked runs", n=res["n"],
                     rho=round(res["rho"], 4),
                     p_perm=round(res["p_perm"], 5),
                     p_scipy_asymptotic=round(res["p_asymptotic"], 5),
                     method=f"two-sided permutation, {res['n_mc']} draws"))
    for cov in sorted(runs["coverage"].unique()):
        s = g[g["coverage"] == cov]
        if len(s) < 3:
            rows.append(dict(stratum=f"coverage {cov}%", n=len(s), rho=np.nan,
                             p_perm=np.nan, p_scipy_asymptotic=np.nan,
                             method="skipped (fewer than 3 grokked runs)"))
            continue
        res = sc.spearman_permutation(s["final_l2_norm"].values,
                                      s["grok_time"].values.astype(float), rng,
                                      n_mc=10_000)
        rows.append(dict(stratum=f"coverage {cov}%", n=len(s), rho=round(res["rho"], 4),
                         p_perm=round(res["p_perm"], 5),
                         p_scipy_asymptotic=round(res["p_asymptotic"], 5),
                         method=f"two-sided permutation, {res['n_mc']} draws"))
    df = pd.DataFrame(rows)
    return df


def run(runs, history, cfg):
    m1, m2 = memtime_section(runs, cfg["MASTER_SEED"])
    s1, s2, s3 = subcritical_section(runs, cfg["MASTER_SEED"])
    w1 = wnorm1000_section(runs, history, cfg["MASTER_SEED"])
    sp = spearman_section(runs, cfg["MASTER_SEED"])
    return dict(memtime=m1, memtrend=m2, c25_finalacc=s1, c25_wnorm=s2,
                c35_mode_finalacc=s3, wnorm1000=w1, spearman=sp)
