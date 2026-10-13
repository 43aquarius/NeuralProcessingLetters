"""stats_core.py -- self-contained statistical routines for the grokking analysis.

Dependencies: numpy, scipy, pandas only (no seaborn, no lifelines).
Every function declares its method, tails, and conventions in the docstring.
All randomness flows through numpy Generator objects created by the caller
(`rng_for`), so results are exactly reproducible from the master seed plus a
documented offset.

Conventions used throughout
---------------------------
* Two-sample contrasts are always (x, y) = (first-named group, second-named
  group); "median difference" = median(x) - median(y).
* U1 is the Mann-Whitney U statistic of the FIRST-named group
  (U1 = #{x_i > y_j} + 0.5 #{x_i == y_j} computed via midranks);
  U1 + U2 = n1*n2.
* Rank-biserial r = 1 - 2*U1/(n1*n2).  r = +1 means the first-named group
  takes (weakly) SMALLER values than the second; r = -1 means it takes larger
  values.  Note r therefore has the opposite sign of the median difference.
* All permutation p-values are two-sided unless the function name/docstring
  says otherwise, and they include the observed assignment (p >= 1/n_assign).
"""
from __future__ import annotations

import itertools
import math
import warnings

import numpy as np
import pandas as pd
from scipy import stats as sps

EPS = 1e-9


def rng_for(master_seed: int, offset: int) -> np.random.Generator:
    """Deterministic RNG for one analysis; offsets are documented in analyze.py."""
    return np.random.default_rng(master_seed + offset)


def midranks(v) -> np.ndarray:
    """Midranks (average ranks) of a 1-D sample, ties share the mean rank."""
    return sps.rankdata(np.asarray(v, dtype=float), method="average")


# =====================================================================
# Task 1 -- exact permutation Mann-Whitney + effect sizes + bootstrap
# =====================================================================

def _assignment_index_matrices(n1: int, n2: int, max_enumerate: int,
                               n_mc: int, rng: np.random.Generator | None):
    """Return (subsets, method_string).

    subsets is an (P, n1) integer array; each row is the set of pooled-sample
    indices assigned to group 1 ("x").  Either all C(N, n1) assignments are
    enumerated, or P Monte-Carlo draws are used (declared in method_string).
    """
    N = n1 + n2
    n_comb = math.comb(N, n1)
    if n_comb <= max_enumerate:
        subsets = np.array(list(itertools.combinations(range(N), n1)), dtype=int)
        method = f"exact enumeration of all {n_comb} C({N},{n1}) label assignments"
        return subsets, method
    if rng is None:
        raise ValueError("Monte-Carlo permutations require an rng")
    # vectorised random distinct subsets: random permutations, take first n1
    perms = rng.permuted(np.tile(np.arange(N), (n_mc, 1)), axis=1)
    subsets = perms[:, :n1]
    method = f"Monte-Carlo permutation with {n_mc} random label assignments"
    return subsets, method


def exact_mw_permutation(x, y, max_enumerate: int = 20_000, n_mc: int = 100_000,
                         rng: np.random.Generator | None = None) -> dict:
    """Exact permutation test of the Mann-Whitney U statistic with midranks.

    Enumerates all C(n1+n2, n1) label assignments of the pooled sample (with
    midranks fixed at their observed values), so ties are handled exactly the
    way the permutation principle requires.  Two-sided p-value:
        p = #{ |U - n1*n2/2| >= |U_obs - n1*n2/2| } / n_assign
    Returns U1 (U of x), U2, exact p, and the method string.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n1, n2 = len(x), len(y)
    N = n1 + n2
    ranks = midranks(np.concatenate([x, y]))
    U1_obs = ranks[:n1].sum() - n1 * (n1 + 1) / 2.0

    subsets, method = _assignment_index_matrices(n1, n2, max_enumerate, n_mc, rng)
    us = ranks[subsets].sum(axis=1) - n1 * (n1 + 1) / 2.0
    half = n1 * n2 / 2.0
    dev_obs = abs(U1_obs - half)
    p = float((np.abs(us - half) >= dev_obs - EPS).mean())
    return dict(U1=float(U1_obs), U2=float(n1 * n2 - U1_obs),
                p_exact=p, method=method, n_assign=int(len(us)))


def scipy_mw_asymptotic(x, y) -> dict:
    """scipy's asymptotic tie-corrected two-sided Mann-Whitney p (continuity
    corrected).  This is what scipy falls back to when ties are present, and
    is the method behind several p-values in the archived manuscript."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    with warnings.catch_warnings(record=True) as wlist:
        warnings.simplefilter("always")
        res = sps.mannwhitneyu(x, y, alternative="two-sided", method="asymptotic")
    msgs = [str(w.message) for w in wlist]
    return dict(U1=float(res.statistic), p_asymptotic=float(res.pvalue), scipy_warnings=msgs)


def rank_biserial(U1: float, n1: int, n2: int) -> float:
    """r = 1 - 2*U1/(n1*n2); r = +1 means group x (first-named) is entirely
    smaller than y; r = -1 means x is entirely larger."""
    return 1.0 - 2.0 * U1 / (n1 * n2)


def hodges_lehmann(x, y) -> float:
    """Two-sample Hodges-Lehmann location estimate: median of all pairwise
    differences x_i - y_j."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    return float(np.median(x[:, None] - y[None, :]))


def bootstrap_median_diff_ci(x, y, rng: np.random.Generator, B: int = 10_000,
                             alpha: float = 0.05) -> dict:
    """Percentile bootstrap CI of median(x) - median(y); resampling within
    each group with replacement.  With 5 tied values per group the number of
    distinct resampled medians is tiny, so this CI is coarse by construction."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n1, n2 = len(x), len(y)
    mx = np.median(x[rng.integers(0, n1, size=(B, n1))], axis=1)
    my = np.median(y[rng.integers(0, n2, size=(B, n2))], axis=1)
    d = mx - my
    lo, hi = np.quantile(d, [alpha / 2, 1 - alpha / 2])
    return dict(ci_lo=float(lo), ci_hi=float(hi), B=B,
                method=f"percentile bootstrap, {B} resamples, within-group resampling")


def holm(pvals) -> np.ndarray:
    """Holm step-down adjusted p-values (family-wise error controlled at the
    alpha of the raw p-values).  Returns an array aligned with the input."""
    p = np.asarray(pvals, dtype=float)
    m = len(p)
    order = np.argsort(p)
    ranked = p[order] * (m - np.arange(m))
    ranked = np.maximum.accumulate(ranked)  # enforce monotonicity
    out = np.empty(m)
    out[order] = np.minimum(ranked, 1.0)
    return out


# =====================================================================
# Task 2 -- survival analysis (manual implementations)
# =====================================================================

def km_table(times, events) -> pd.DataFrame:
    """Kaplan-Meier estimate with correct handling of tied event/censoring
    times (censoring at the same time as events is removed after the events).
    Returns a DataFrame: time, n_at_risk, events, censored, survival."""
    times = np.asarray(times, dtype=float)
    events = np.asarray(events, dtype=bool)
    etimes = np.unique(times[events])
    rows = []
    S = 1.0
    for t in etimes:
        n = int((times >= t).sum())
        d = int(((times == t) & events).sum())
        c = int(((times == t) & ~events).sum())
        S *= 1.0 - d / n
        rows.append(dict(time=float(t), n_at_risk=n, events=d, censored=c,
                         survival=float(S)))
    return pd.DataFrame(rows, columns=["time", "n_at_risk", "events", "censored", "survival"])


def rmst_from_km(times, events, horizon: float, grid: float) -> float:
    """Restricted mean survival time on [0, horizon] from the KM curve.

    S(u) = P(T > u) is a right-continuous step function that only changes at
    event times; RMST = int_0^horizon S(u) du is computed exactly on the
    evaluation grid (times are multiples of `grid`): sum over grid intervals
    of grid * S(left endpoint).  A run with an event at time t contributes
    exactly t units of survival time."""
    times = np.asarray(times, dtype=float)
    events = np.asarray(events, dtype=bool)
    et = np.unique(times[events])
    if len(et) == 0:
        return float(horizon)
    ks = np.arange(0.0, horizon, grid)  # left endpoints
    # survival just after each event time
    S_ev = np.empty(len(et))
    S = 1.0
    for i, t in enumerate(et):
        n = (times >= t).sum()
        d = ((times == t) & events).sum()
        S *= 1.0 - d / n
        S_ev[i] = S
    # S(u) for u in [et[j], next event): S_ev[j]; find S at each grid point
    pos = np.searchsorted(et, ks, side="right") - 1  # last event <= grid point
    Sgrid = np.ones(len(ks))
    ok = pos >= 0
    Sgrid[ok] = S_ev[pos[ok]]
    return float(grid * Sgrid.sum())


def rmst_batch(times, events, idx_matrix, horizon: float, grid: float) -> np.ndarray:
    """Vectorised RMST for many within-group resamples of the same data.

    times/events: (n,) observed event/censoring data.
    idx_matrix: (B, n) index matrix; row b is resample b.
    Returns (B,) RMST values.
    """
    times = np.asarray(times, dtype=float)
    events = np.asarray(events, dtype=bool)
    et = np.unique(times[events])
    t = times[idx_matrix]              # (B, n)
    e = events[idx_matrix]             # (B, n)
    if len(et) == 0:
        return np.full(idx_matrix.shape[0], float(horizon))
    eq = (t[:, :, None] == et[None, None, :]) & e[:, :, None]   # (B, n, T)
    ge = (t[:, :, None] >= et[None, None, :])                   # (B, n, T)
    d = eq.sum(axis=1)                                            # (B, T)
    nrisk = ge.sum(axis=1)                                       # (B, T)
    S = np.cumprod(1.0 - d / np.maximum(nrisk, 1), axis=1)      # (B, T)
    ks = np.arange(0.0, horizon, grid)
    pos = np.searchsorted(et, ks, side="right") - 1
    Sgrid = np.ones((idx_matrix.shape[0], len(ks)))
    ok = pos >= 0
    Sgrid[:, ok] = S[:, pos[ok]]
    return grid * Sgrid.sum(axis=1)


def rmst_bootstrap_diff(t1, e1, t2, e2, rng: np.random.Generator, horizon: float,
                        grid: float, B: int = 10_000) -> dict:
    """Bootstrap 95% CI of RMST(group1) - RMST(group2); stratified
    (within-group) resampling of runs, B resamples."""
    t1 = np.asarray(t1, dtype=float); e1 = np.asarray(e1, dtype=bool)
    t2 = np.asarray(t2, dtype=float); e2 = np.asarray(e2, dtype=bool)
    i1 = rng.integers(0, len(t1), size=(B, len(t1)))
    i2 = rng.integers(0, len(t2), size=(B, len(t2)))
    r1 = rmst_batch(t1, e1, i1, horizon, grid)
    r2 = rmst_batch(t2, e2, i2, horizon, grid)
    d = r1 - r2
    lo, hi = np.quantile(d, [0.025, 0.975])
    return dict(rmst1=float(rmst_from_km(t1, e1, horizon, grid)),
                rmst2=float(rmst_from_km(t2, e2, horizon, grid)),
                diff=float(rmst_from_km(t1, e1, horizon, grid)
                           - rmst_from_km(t2, e2, horizon, grid)),
                ci_lo=float(lo), ci_hi=float(hi), B=B)


def logrank_batch(times, events, label_matrix, n_groups: int) -> np.ndarray:
    """Log-rank statistic for every row of `label_matrix`.

    times, events: (N,) observed data (event = grokked).
    label_matrix: (P, N) integer group labels in {0..n_groups-1}.
    Statistic: the standard k-sample log-rank chi-square with df = k-1
    (groups 1..k-1 against the last group), hypergeometric variance with
    correct tie handling, exactly the `survival::survdiff` construction.
    Returns (P,) chi-square values.
    """
    times = np.asarray(times, dtype=float)
    events = np.asarray(events, dtype=bool)
    P, N = label_matrix.shape
    k = n_groups
    et = np.unique(times[events])                                   # (T,)
    ev_at = (times[:, None] == et[None, :]) & events[:, None]       # (N, T)
    risk_at = times[:, None] >= et[None, :]                         # (N, T)
    onehot = np.eye(k, dtype=float)[label_matrix]                   # (P, N, k)
    d = np.einsum("pnk,nt->ptk", onehot, ev_at.astype(float))       # (P, T, k)
    nr = np.einsum("pnk,nt->ptk", onehot, risk_at.astype(float))    # (P, T, k)
    d_tot = ev_at.sum(axis=0)                                       # (T,)
    n_tot = nr.sum(axis=2)                                          # (P, T)
    E = d_tot[None, :, None] * nr / np.maximum(n_tot[:, :, None], 1.0)
    z = (d - E)[:, :, : k - 1].sum(axis=1)                          # (P, k-1)
    with np.errstate(divide="ignore", invalid="ignore"):
        cf = np.where(n_tot > 1,
                      d_tot[None, :] * (n_tot - d_tot) / (n_tot - 1), 0.0)
    pg = nr / np.maximum(n_tot[:, :, None], 1.0)                    # (P, T, k)
    pg = pg[:, :, : k - 1]
    outer = pg[:, :, :, None] * pg[:, :, None, :]
    diag = np.eye(k - 1)[None, None] * pg[:, :, None, :]
    V = (cf[:, :, None, None] * (diag - outer)).sum(axis=1)         # (P, k-1, k-1)
    if k == 2:
        denom = np.maximum(V[:, 0, 0], 1e-300)
        return z[:, 0] ** 2 / denom
    try:
        Vinv = np.linalg.inv(V)
    except np.linalg.LinAlgError:
        Vinv = np.linalg.pinv(V)
    return np.einsum("pi,pij,pj->p", z, Vinv, z)


def logrank_test(times, events, labels, rng: np.random.Generator,
                 n_mc: int = 10_000, max_enumerate: int = 20_000) -> dict:
    """Log-rank test with permutation p-value.

    Two-sample: if C(N, n1) <= max_enumerate all assignments are enumerated,
    else n_mc Monte-Carlo permutations (declared in `method`).  k-sample:
    Monte-Carlo permutations.  The asymptotic chi-square p-value is reported
    alongside (`p_chi2`), but the permutation p is the declared one.
    """
    times = np.asarray(times, dtype=float)
    events = np.asarray(events, dtype=bool)
    labels = np.asarray(labels, dtype=int)
    k = len(np.unique(labels))
    obs = float(logrank_batch(times, events, labels[None, :], k)[0])
    p_chi2 = float(sps.chi2.sf(obs, k - 1))
    if k == 2:
        n1 = int((labels == 0).sum())
        subsets, method = _assignment_index_matrices(n1, int((labels == 1).sum()),
                                                     max_enumerate, n_mc, rng)
        lab = np.ones((len(subsets), len(labels)), dtype=int)
        lab[np.arange(len(subsets))[:, None], subsets] = 0
    else:
        # permute the label vector itself; each row is one random assignment
        lab = rng.permuted(np.tile(labels, (n_mc, 1)), axis=1)
        method = f"Monte-Carlo permutation with {n_mc} random label assignments"
    stats = logrank_batch(times, events, lab, k)
    p = float((stats >= obs - EPS).mean())
    return dict(chi2=obs, df=k - 1, p_perm=p, p_chi2=p_chi2, method=method,
                n_perm=int(len(stats)))


def fisher_exact_2x2(k1, n1, k2, n2) -> dict:
    """Two-sided Fisher exact test on [[k1, n1-k1], [k2, n2-k2]]."""
    table = [[int(k1), int(n1 - k1)], [int(k2), int(n2 - k2)]]
    res = sps.fisher_exact(table, alternative="two-sided")
    return dict(OR=float(res.statistic), p=float(res.pvalue))


def clopper_pearson(k: int, n: int, alpha: float = 0.05):
    """Exact (Clopper-Pearson) binomial CI for a proportion."""
    k, n = int(k), int(n)
    lo = 0.0 if k == 0 else float(sps.beta.ppf(alpha / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(sps.beta.ppf(1 - alpha / 2, k + 1, n - k))
    return lo, hi


def cox_stratified(times, events, z, strata, max_iter: int = 60,
                   tol: float = 1e-9, beta_max: float = 10.0) -> dict:
    """Stratified Cox model with a single binary covariate and Breslow ties,
    fitted by Newton-Raphson on the partial likelihood.

    z = 1 must denote the index group (e.g. blocked repetition), z = 0 the
    reference (R = 1).  Monotone likelihood (events in a stratum occurring
    only in one covariate group) drives |beta| to infinity; we stop at
    beta_max and report non-convergence honestly.
    """
    times = np.asarray(times, dtype=float)
    events = np.asarray(events, dtype=bool)
    z = np.asarray(z, dtype=float)
    strata = np.asarray(strata)
    beta = 0.0
    converged = False
    note = ""
    for it in range(max_iter):
        score = 0.0
        info = 0.0
        for s in np.unique(strata):
            m = strata == s
            ts, es, zs = times[m], events[m], z[m]
            for t in np.unique(ts[es]):
                risk = ts >= t
                w = np.exp(beta * zs[risk])
                zbar = float((w * zs[risk]).sum() / w.sum())
                d_t = int(((ts == t) & es).sum())
                score += zs[(ts == t) & es].sum() - d_t * zbar
                info += d_t * float((w * (zs[risk] - zbar) ** 2).sum() / w.sum())
        if info < 1e-12:
            note = "observed information collapsed (monotone likelihood)"
            break
        step = score / info
        # step halving for stability
        b_new = beta + step
        halved = False
        while abs(b_new) > beta_max and abs(step) > 1e-12:
            step /= 2.0
            b_new = beta + step
            halved = True
        if halved and abs(b_new) > 0.999 * beta_max:
            # the full Newton step wants to escape the cap: monotone
            # likelihood, the MLE diverges
            beta = b_new
            note = (f"|beta| pinned at the cap {beta_max} "
                    "(monotone-likelihood behaviour; estimate diverges)")
            break
        if abs(b_new - beta) < tol:
            beta = b_new
            converged = True
            note = f"converged after {it + 1} Newton steps"
            break
        if abs(b_new) >= beta_max:
            beta = b_new
            note = (f"|beta| reached the cap {beta_max} "
                    "(monotone-likelihood behaviour; estimate diverges)")
            break
        beta = b_new
    se = float(1.0 / math.sqrt(info)) if info > 1e-12 else float("inf")
    z95 = sps.norm.ppf(0.975)
    return dict(beta=float(beta), se=se, HR=float(math.exp(beta)),
                ci_lo=float(math.exp(beta - z95 * se)) if np.isfinite(se) else float("nan"),
                ci_hi=float(math.exp(beta + z95 * se)) if np.isfinite(se) else float("nan"),
                converged=converged, iterations=it + 1, note=note)


# =====================================================================
# Task 3 -- equivalence testing (TOST)
# =====================================================================

def _perm_mean_diff_dist(x, y, max_enumerate: int = 20_000, n_mc: int = 100_000,
                         rng: np.random.Generator | None = None):
    """Permutation distribution of D = mean(x_S) - mean(x_notS).

    Returns (D_perm, t_intersect, method, n_assign) where t_intersect[i] is
    the number of pooled elements from group x inside assignment i.  Because a
    margin shift only adds a known constant to each assignment's statistic
    (data shift, fixed ranks of the shift), the same enumeration serves every
    margin:  shifting x by +m changes assignment i's statistic by
    m * (t_i/n1 - (n1-t_i)/n2).
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n1, n2 = len(x), len(y)
    N = n1 + n2
    pooled = np.concatenate([x, y])
    subsets, method = _assignment_index_matrices(n1, n2, max_enumerate, n_mc, rng)
    sums = pooled[subsets].sum(axis=1)          # (P,)
    total = pooled.sum()
    D_perm = sums / n1 - (total - sums) / n2
    t_ix = subsets >= n1                        # pooled index >= n1 => element of y
    t = (subsets < n1).sum(axis=1)              # number of x-elements in assignment
    return D_perm, t, method, len(subsets)


def tost_permutation(x, y, margin: float, max_enumerate: int = 20_000,
                     n_mc: int = 100_000, rng: np.random.Generator | None = None) -> dict:
    """Permutation-based TOST on the difference of means.

    H01: delta <= -margin and H02: delta >= +margin, tested by shifting the
    data to each null boundary and permuting group labels:
      p1 = P(D_perm(shift x by +m) >= D_obs + m)
      p2 = P(D_perm(shift y by +m) <= D_obs - m)
    (assignment i's shifted statistic = D_perm_i + m * (t_i/n1 - (n1-t_i)/n2)
    for the x-shift, analogously for the y-shift.)  Equivalence at alpha iff
    max(p1, p2) < alpha.  Also returns the 90% permutation CI of the mean
    difference by test inversion (percentile-inversion of the permutation
    distribution), which is coarse at n=5 vs 5 (252 assignments).
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n1, n2 = len(x), len(y)
    D_obs = float(x.mean() - y.mean())
    D_perm, t, method, n_assign = _perm_mean_diff_dist(x, y, max_enumerate, n_mc, rng)
    ax = t / n1 - (n1 - t) / n2                 # shift-on-x adjustment
    ay = (n1 - t) / n1 - (n2 - (n1 - t)) / n2   # shift-on-y adjustment
    p1 = float((D_perm + margin * ax >= D_obs + margin - EPS).mean())
    p2 = float((D_perm + margin * ay <= D_obs - margin + EPS).mean())
    q05, q95 = np.quantile(D_perm, [0.05, 0.95])
    ci = (float(D_obs - q95), float(D_obs - q05))   # percentile-inversion CI
    return dict(D_obs=D_obs, p1=p1, p2=p2, p_max=max(p1, p2), ci90_lo=ci[0],
                ci90_hi=ci[1], method=method + " (shifted-null TOST)", n_assign=n_assign)


def tost_welch(x, y, margin: float) -> dict:
    """Welch t-based TOST on the difference of means (two one-sided tests,
    Satterthwaite df, 90% CI)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n1, n2 = len(x), len(y)
    D_obs = float(x.mean() - y.mean())
    v1, v2 = x.var(ddof=1), y.var(ddof=1)
    se = math.sqrt(v1 / n1 + v2 / n2)
    if se == 0:
        return dict(D_obs=D_obs, se=0.0, p1=0.0 if D_obs + margin > 0 else 1.0,
                    p2=0.0 if D_obs - margin < 0 else 1.0, p_max=None,
                    ci90_lo=D_obs, ci90_hi=D_obs, df=None,
                    note="zero within-group variance; degenerate")
    df = (v1 / n1 + v2 / n2) ** 2 / ((v1 / n1) ** 2 / (n1 - 1) + (v2 / n2) ** 2 / (n2 - 1))
    p1 = float(sps.t.sf((D_obs + margin) / se, df))     # H0: delta = -margin
    p2 = float(sps.t.cdf((D_obs - margin) / se, df))     # H0: delta = +margin
    t90 = sps.t.ppf(0.95, df)
    return dict(D_obs=D_obs, se=float(se), p1=p1, p2=p2, p_max=max(p1, p2),
                ci90_lo=float(D_obs - t90 * se), ci90_hi=float(D_obs + t90 * se),
                df=float(df), note="")


def tost_power_sim(sd: float, margins, true_log_ratios, n_per_group: int = 5,
                   B: int = 2_000, rng: np.random.Generator | None = None) -> pd.DataFrame:
    """Simulation-based power of the permutation TOST for 5-vs-5 normal data
    with the observed within-cell SD (NOT a pre-study power analysis).

    For each true log10 ratio in `true_log_ratios` and each margin, B datasets
    are simulated (group means 0 and -delta on the log10 scale) and the exact
    252-assignment permutation TOST is evaluated (vectorised).  Also returns
    the power of the two-sided permutation test of the mean difference.
    """
    if rng is None:
        rng = np.random.default_rng(0)
    n = n_per_group
    N = 2 * n
    subsets = np.array(list(itertools.combinations(range(N), n)), dtype=int)
    P = len(subsets)
    rows = []
    for delta in true_log_ratios:
        data = rng.normal(0.0, sd, size=(B, N))
        data[:, n:] -= delta                      # group y mean = -delta
        sums = data[:, subsets].sum(axis=2)       # (B, P)
        total = data.sum(axis=1, keepdims=True)    # (B, 1)
        D_perm = sums / n - (total - sums) / n    # (B, P)
        t = (subsets < n).sum(axis=1)              # (P,)
        ax = t / n - (n - t) / n                  # (P,)
        ay = (n - t) / n - (n - (n - t)) / n      # (P,)
        D_obs = data[:, :n].mean(1) - data[:, n:].mean(1)  # (B,)
        # two-sided permutation p of the mean difference
        mu = D_perm.mean(axis=1, keepdims=True)            # (B, 1)
        pperm = (np.abs(D_perm - mu) >= np.abs(D_obs[:, None] - mu) - EPS).mean(axis=1)
        rows.append(dict(true_log10_ratio=delta, true_ratio=10 ** delta,
                         power_permtest_diff=float((pperm < 0.05).mean())))
        for m in margins:
            p1 = (D_perm + m * ax[None, :] >= (D_obs + m)[:, None] - EPS).mean(1)
            p2 = (D_perm + m * ay[None, :] <= (D_obs - m)[:, None] + EPS).mean(1)
            power = float((np.maximum(p1, p2) < 0.05).mean())
            rows.append(dict(true_log10_ratio=delta, true_ratio=10 ** delta,
                             margin_ratio=10 ** m, power_tost=power))
    return pd.DataFrame(rows)


# =====================================================================
# Task 4 -- secondary analyses
# =====================================================================

def jt_statistic(groups) -> float:
    """Jonckheere-Terpstra statistic for ordered groups g1 < g2 < ... < gk:
    J = sum_{j<l} sum_{x in g_j, y in g_l} [ I(x<y) + 0.5 I(x==y) ]."""
    J = 0.0
    for j in range(len(groups)):
        for l in range(j + 1, len(groups)):
            a = np.asarray(groups[j], dtype=float)
            b = np.asarray(groups[l], dtype=float)
            J += ((a[:, None] < b[None, :]).sum() + 0.5 * (a[:, None] == b[None, :]).sum())
    return float(J)


def jt_permutation_p(groups, rng: np.random.Generator, n_mc: int = 10_000) -> dict:
    """One-sided permutation p-value (increasing alternative) for the JT
    statistic; labels are randomly permuted across the pooled sample."""
    groups = [np.asarray(g, dtype=float) for g in groups]
    J_obs = jt_statistic(groups)
    pooled = np.concatenate(groups)
    sizes = [len(g) for g in groups]
    count = 0
    for _ in range(n_mc):
        perm = pooled[rng.permutation(len(pooled))]
        pieces, i = [], 0
        for s in sizes:
            pieces.append(perm[i:i + s]); i += s
        if jt_statistic(pieces) >= J_obs - EPS:
            count += 1
    return dict(J=J_obs, p_one_sided=(count + 1) / (n_mc + 1), n_mc=n_mc,
                method=f"Monte-Carlo permutation, {n_mc} draws, one-sided (increasing)")


def spearman_permutation(x, y, rng: np.random.Generator, n_mc: int = 10_000) -> dict:
    """Spearman rho with a two-sided permutation p-value (permute y), plus
    scipy's default asymptotic p for comparison."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    res = sps.spearmanr(x, y)
    rho = float(res.statistic)
    count = 0
    for _ in range(n_mc):
        r = sps.spearmanr(x, y[rng.permutation(len(y))]).statistic
        if abs(r) >= abs(rho) - EPS:
            count += 1
    return dict(rho=rho, p_asymptotic=float(res.pvalue),
                p_perm=(count + 1) / (n_mc + 1), n_mc=n_mc, n=len(x))
