"""Unit tests for the analysis pipeline (run directly: python tests/test_analyze.py,
or via pytest).  Synthetic data appear ONLY here, clearly labelled."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import stats_core as sc  # noqa: E402

MASTER_SEED = 20260922


def test_exact_mw_perfect_separation():
    """Perfect separation of two groups of 5 must give p = 2/252 = 0.00794."""
    x = [10.0, 20.0, 30.0, 40.0, 50.0]     # synthetic
    y = [100.0, 200.0, 300.0, 400.0, 500.0]
    r = sc.exact_mw_permutation(x, y)
    assert abs(r["p_exact"] - 2.0 / 252.0) < 1e-12, r
    assert r["n_assign"] == 252
    assert r["method"].startswith("exact enumeration")


def test_exact_mw_symmetry():
    """Swapping the groups keeps the two-sided p and exchanges U1/U2."""
    rng = np.random.default_rng(0)
    x = rng.normal(0, 1, 5)
    y = rng.normal(0.7, 1, 5)
    a = sc.exact_mw_permutation(x, y)
    b = sc.exact_mw_permutation(y, x)
    assert abs(a["p_exact"] - b["p_exact"]) < 1e-12
    assert abs(a["U1"] - b["U2"]) < 1e-12
    assert abs(a["U1"] + a["U2"] - 25.0) < 1e-12
    # ties handled identically
    a = sc.exact_mw_permutation([1, 1, 2, 2, 3], [2, 2, 3, 3, 3])
    b = sc.exact_mw_permutation([2, 2, 3, 3, 3], [1, 1, 2, 2, 3])
    assert abs(a["p_exact"] - b["p_exact"]) < 1e-12


def test_holm():
    assert np.allclose(sc.holm([0.01, 0.04]), [0.02, 0.04])
    assert np.allclose(sc.holm([0.02, 0.03]), [0.04, 0.04])
    assert np.allclose(sc.holm([0.03, 0.01, 0.9]), [0.06, 0.03, 0.9])


def test_km_hand_computed():
    """Hand-computed KM: times (1,2,3+,4), events (1,1,0,1).
    S(1)=3/4, S(2)=1/2, S(4)=0; RMST on [0,6] with unit grid = 2.75."""
    times = np.array([1.0, 2.0, 3.0, 4.0])
    events = np.array([True, True, False, True])
    tab = sc.km_table(times, events)
    assert list(tab["time"]) == [1.0, 2.0, 4.0]
    assert list(tab["n_at_risk"]) == [4, 3, 1]
    assert list(tab["events"]) == [1, 1, 1]
    assert np.allclose(tab["survival"], [0.75, 0.5, 0.0])
    assert abs(sc.rmst_from_km(times, events, 6.0, 1.0) - 2.75) < 1e-12
    # batch version with the identity resample reproduces the point estimate
    rm = sc.rmst_batch(times, events, np.arange(4)[None, :], 6.0, 1.0)
    assert abs(rm[0] - 2.75) < 1e-12


def test_logrank_hand_computed():
    """Hand-computed two-sample log-rank: A times (1,3,4+), B times (2,5+,5+).
    At-risk: t=1 n=6 (3/3), t=2 n=5 (2/3), t=3 n=4 (2/2);
    O_A=2, E_A=1.4, V=0.74, chi2=0.36/0.74=0.486486..."""
    times = np.array([1.0, 3.0, 4.0, 2.0, 5.0, 5.0])
    events = np.array([True, True, False, True, False, False])
    labels = np.array([0, 0, 0, 1, 1, 1])
    chi2 = sc.logrank_batch(times, events, labels[None, :], 2)[0]
    assert abs(chi2 - 0.36 / 0.74) < 1e-9, chi2
    rng = sc.rng_for(MASTER_SEED, 999)
    res = sc.logrank_test(times, events, labels, rng, n_mc=2000)
    assert abs(res["chi2"] - 0.36 / 0.74) < 1e-9
    assert 0.2 < res["p_perm"] < 0.8
    assert abs(res["p_chi2"] - 0.4854) < 0.01


def test_tost_sanity_identical_groups():
    """Identical groups with a wide margin must give small one-sided p's
    (equivalence declared at both the permutation and Welch TOST)."""
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])   # synthetic
    y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    m = 3.0                                    # ratio 10^3 -- deliberately wide
    tp = sc.tost_permutation(x, y, m)
    tw = sc.tost_welch(x, y, m)
    assert tp["p_max"] < 0.05, tp
    assert tw["p_max"] < 0.05, tw
    # a margin far below the noise must NOT be declared equivalent
    tp_small = sc.tost_permutation(x, y, 0.05)
    assert tp_small["p_max"] > 0.05, tp_small


def test_bootstrap_reproducibility():
    x = np.array([1.0, 2.0, 2.0, 5.0, 7.0])
    y = np.array([2.0, 3.0, 3.0, 4.0, 9.0])
    a = sc.bootstrap_median_diff_ci(x, y, sc.rng_for(MASTER_SEED, 101))
    b = sc.bootstrap_median_diff_ci(x, y, sc.rng_for(MASTER_SEED, 101))
    c = sc.bootstrap_median_diff_ci(x, y, sc.rng_for(MASTER_SEED, 102))
    assert a == b
    assert a["B"] == 10_000 and c["B"] == 10_000


def test_clopper_pearson_edges():
    lo, hi = sc.clopper_pearson(0, 5)
    assert lo == 0.0 and 0 < hi < 0.6
    lo, hi = sc.clopper_pearson(5, 5)
    assert hi == 1.0 and 0.4 < lo < 1.0
    lo, hi = sc.clopper_pearson(2, 5)
    assert 0.05 < lo < 0.6 and 0.1 < hi < 0.9


def test_jt_perfect_ordering():
    groups = [np.array([1.0, 1.0, 1.0]), np.array([2.0, 2.0, 2.0]),
              np.array([3.0, 3.0, 3.0])]
    assert sc.jt_statistic(groups) == 27.0
    rng = sc.rng_for(MASTER_SEED, 401)
    res = sc.jt_permutation_p(groups, rng, n_mc=1000)
    assert res["p_one_sided"] < 0.01, res


def test_cox_convergence_and_monotone_likelihood():
    times = np.array([1.0, 2.0, 3.0, 4.0])
    ev = np.ones(4, dtype=bool)
    # alternating covariate: converges
    r = sc.cox_stratified(times, ev, np.array([0.0, 1.0, 0.0, 1.0]),
                          np.zeros(4, dtype=int))
    assert r["converged"] and abs(r["beta"]) < 10
    # perfectly separated covariate: monotone likelihood, must be flagged
    r = sc.cox_stratified(times, ev, np.array([0.0, 0.0, 1.0, 1.0]),
                          np.zeros(4, dtype=int))
    assert not r["converged"] and ("cap" in r["note"] or "monotone" in r["note"])


def test_permutation_tost_shift_identity():
    """The shifted-null adjustment must be exact: permuting explicitly shifted
    data must reproduce the analytic-shift p-values."""
    rng = np.random.default_rng(7)
    x = rng.normal(0, 1, 5)
    y = rng.normal(0.2, 1, 5)
    m = 0.6
    tp = sc.tost_permutation(x, y, m)
    # brute-force reimplementation for cross-check
    pooled = np.concatenate([x, y])
    n1 = n2 = 5
    import itertools
    subsets = np.array(list(itertools.combinations(range(10), 5)))
    p1 = p2 = 0
    D_obs = x.mean() - y.mean()
    for S in subsets:
        S = np.array(S)
        v = pooled.copy()
        # shift x (indices 0..4) by +m
        v[:5] += m
        d1 = v[S].mean() - v[np.setdiff1d(np.arange(10), S)].mean()
        if d1 >= D_obs + m - 1e-12:
            p1 += 1
        v2 = pooled.copy()
        v2[5:] += m
        d2 = v2[S].mean() - v2[np.setdiff1d(np.arange(10), S)].mean()
        if d2 <= D_obs - m + 1e-12:
            p2 += 1
    assert abs(p1 / 252 - tp["p1"]) < 1e-9, (p1 / 252, tp["p1"])
    assert abs(p2 / 252 - tp["p2"]) < 1e-9, (p2 / 252, tp["p2"])


def main():
    tests = [(n, f) for n, f in sorted(globals().items())
             if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"PASS {name}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {name}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} tests passed")
    return failed


if __name__ == "__main__":
    sys.exit(main())
