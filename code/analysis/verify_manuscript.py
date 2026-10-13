#!/usr/bin/env python3
"""verify_manuscript.py -- verify every statistic claimed in the manuscript
against a fresh recomputation from runs.csv and history.csv.

WHAT THIS SCRIPT DOES
---------------------
1. Runs unit tests of the statistical primitives (exact permutation
   Mann-Whitney, Kaplan-Meier, bootstrap reproducibility).
2. Validates that runs.csv / history.csv have the expected columns
   (fails loudly, never guesses).
3. Recomputes every claim in the CLAIMS table below directly from the raw
   per-run table (never from previously computed result CSVs).
4. Prints a PASS/FAIL table and writes verification_report.csv.

COLUMN ASSUMPTIONS (CONFIRM BEFORE RUNNING; the script fails loudly if absent)
------------------------------------------------------------------------------
runs.csv     : run_id, coverage, R, mode, seed, grok_time, censored,
               mem_time, final_train_acc, final_test_acc, final_l2_norm,
               stop_step, n_test, n_train_unique
               (grok_time is empty for censored runs; censored is True/False)
history.csv  : coverage, repetition, mode, seed, step, train_loss, train_acc,
               test_acc, wnorm
               (one row per evaluation step; wnorm = parameter L2 norm)

SEED POLICY
-----------
All randomness uses numpy default_rng(20260922 + offset) with the offsets
below (mirroring the archived pipeline where the analysis is the same).
Resampling-based statistics (bootstrap CIs, Monte-Carlo p-values, power
simulations) are compared against the manuscript with a documented
tolerance and are marked SIM in the report; deterministic statistics
(exact enumeration tests, medians, event counts) are compared exactly.

Usage:
    python verify_manuscript.py --runs runs.csv --history history.csv \
        [--out verification_report.csv] [--test-only]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import stats_core as sc

MASTER_SEED = 20260922
OFFSET = {
    "bootstrap": 101,        # median-difference percentile bootstrap CIs
    "logrank_mc": 201,       # k-sample log-rank Monte-Carlo permutations
    "rmst_boot": 301,        # RMST difference bootstrap CIs
    "jt_mc": 401,            # Jonckheere-Terpstra permutation p
    "spearman_mc": 501,      # Spearman permutation p
    "power_sim": 601,        # TOST power simulation
    "wnorm1000_boot": 701,   # wnorm@1000 bootstrap CI
    "verify_extra": 901,     # any verify-only resampling
}
HORIZON = 20_000.0
BUDGET = 20_000

RUNS_COLUMNS = ["run_id", "coverage", "R", "mode", "seed", "grok_time",
                "censored", "mem_time", "final_train_acc", "final_test_acc",
                "final_l2_norm", "stop_step", "n_test", "n_train_unique"]
HISTORY_COLUMNS = ["coverage", "repetition", "mode", "seed", "step",
                   "train_loss", "train_acc", "test_acc", "wnorm"]


# --------------------------------------------------------------------------
# Unit tests of the statistical primitives
# --------------------------------------------------------------------------
def unit_tests():
    print("=" * 70)
    print("UNIT TESTS")
    print("=" * 70)
    ok = True

    # T1: exact permutation MW, perfect separation -> p = 2/252
    x = np.array([1.0, 2, 3, 4, 5])
    y = np.array([6.0, 7, 8, 9, 10])
    res = sc.exact_mw_permutation(x, y)
    expect = 2.0 / 252.0
    passed = abs(res["p_exact"] - expect) < 1e-12
    ok &= passed
    print(f"  T1 exact MW perfect separation p = {res['p_exact']:.6f} "
          f"(expected {expect:.6f})  ->  {'PASS' if passed else 'FAIL'}")

    # T1b: symmetry of the exact test
    res2 = sc.exact_mw_permutation(y, x)
    passed = abs(res2["p_exact"] - res["p_exact"]) < 1e-12
    ok &= passed
    print(f"  T1b symmetry p(x,y) = p(y,x)  ->  {'PASS' if passed else 'FAIL'}")

    # T2: Kaplan-Meier against a hand-worked toy example
    # times [1,2,3,4], events [1,1,0,1]:
    #   t=1: at risk 4, 1 event -> S = 3/4
    #   t=2: at risk 3, 1 event -> S = 3/4 * 2/3 = 1/2
    #   t=3: at risk 2, censored -> S stays 1/2 (no row: no event)
    #   t=4: at risk 1, 1 event -> S = 0
    # RMST(4) = 1*1 + 1*0.75 + 2*0.5 = 2.75
    km = sc.km_table(np.array([1.0, 2, 3, 4]), np.array([1, 1, 0, 1]))
    s_expect = {1.0: 0.75, 2.0: 0.50, 4.0: 0.0}
    passed = True
    for _, row in km.iterrows():
        t, s = float(row["time"]), float(row["survival"])
        if t in s_expect and abs(s - s_expect[t]) > 1e-12:
            passed = False
    rmst = sc.rmst_from_km(np.array([1.0, 2, 3, 4]), np.array([1, 1, 0, 1]),
                           horizon=4.0, grid=0.01)
    passed &= abs(rmst - 2.75) < 0.02
    ok &= passed
    print(f"  T2 KM toy survival + RMST = {rmst:.4f} (expected 2.75)"
          f"  ->  {'PASS' if passed else 'FAIL'}")

    # T3: bootstrap reproducibility under a fixed seed
    rng1 = sc.rng_for(MASTER_SEED, OFFSET["bootstrap"])
    rng1b = sc.rng_for(MASTER_SEED, OFFSET["bootstrap"])
    rng2 = sc.rng_for(MASTER_SEED, OFFSET["verify_extra"])
    a = np.array([0.31, 1.07, 2.23, 3.91, 7.13])
    b = np.array([0.05, 0.62, 1.48, 3.02, 5.77])
    c1 = sc.bootstrap_median_diff_ci(a, b, rng1, B=2000)
    c1b = sc.bootstrap_median_diff_ci(a, b, rng1b, B=2000)
    c2 = sc.bootstrap_median_diff_ci(a, b, rng2, B=2000)
    passed = (c1["ci_lo"] == c1b["ci_lo"] and c1["ci_hi"] == c1b["ci_hi"])
    ok &= passed
    print(f"  T3 bootstrap reproducibility: same seed "
          f"[{c1['ci_lo']:.3f}, {c1['ci_hi']:.3f}] == "
          f"[{c1b['ci_lo']:.3f}, {c1b['ci_hi']:.3f}] "
          f"(different seed: [{c2['ci_lo']:.3f}, {c2['ci_hi']:.3f}])"
          f"  ->  {'PASS' if passed else 'FAIL'}")

    # T4: Holm adjustment on a known example
    h = sc.holm([0.00794, 0.00794, 0.119])
    passed = (abs(h[0] - 0.02382) < 0.001 and abs(h[1] - 0.02382) < 0.001
              and abs(h[2] - 0.119) < 1e-9)
    ok &= passed
    print(f"  T4 Holm([0.00794,0.00794,0.119]) = {list(np.round(h,5))} "
          f"->  {'PASS' if passed else 'FAIL'}")

    if not ok:
        print("UNIT TESTS FAILED -- aborting.")
        sys.exit(1)
    print("All unit tests passed.\n")


# --------------------------------------------------------------------------
# Data loading and helpers
# --------------------------------------------------------------------------
def load_data(runs_path, history_path):
    runs = pd.read_csv(runs_path)
    missing = [c for c in RUNS_COLUMNS if c not in runs.columns]
    if missing:
        sys.exit(f"FATAL: runs.csv is missing expected columns: {missing}\n"
                 f"Found: {list(runs.columns)}\n"
                 "Edit RUNS_COLUMNS at the top of this script if the names "
                 "differ, then re-run.")
    hist = pd.read_csv(history_path)
    missing = [c for c in HISTORY_COLUMNS if c not in hist.columns]
    if missing:
        sys.exit(f"FATAL: history.csv is missing expected columns: {missing}\n"
                 f"Found: {list(hist.columns)}\n"
                 "Edit HISTORY_COLUMNS at the top of this script if the "
                 "names differ, then re-run.")
    return runs, hist


def cell(runs, cov, R, mode=None):
    m = (runs["coverage"] == cov) & (runs["R"] == R)
    if R > 1 and mode is not None:
        m &= runs["mode"] == mode
    return runs[m].sort_values("seed")


def gt_budget(g):
    """GrokTime with censored runs at the 20,000 budget (worst rank)."""
    return np.where(g["censored"].astype(bool), HORIZON,
                     g["grok_time"]).astype(float)


def pair(runs, sel_a, sel_b):
    a, b = cell(runs, *sel_a), cell(runs, *sel_b)
    return gt_budget(a), gt_budget(b)


def exact_pair(x, y, rng, B=10_000):
    """Exact MW + rank-biserial + bootstrap CI of the median difference."""
    res = sc.exact_mw_permutation(x, y)
    ci = sc.bootstrap_median_diff_ci(x, y, rng, B=B)
    rbc = sc.rank_biserial(res["U1"], len(x), len(y))
    return dict(p=res["p_exact"], r=rbc,
                med_diff=float(np.median(x) - np.median(y)),
                ci_lo=ci["ci_lo"], ci_hi=ci["ci_hi"])


def holm_apply(pvals):
    return sc.holm(pvals)


# --------------------------------------------------------------------------
# Main verification
# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs.csv")
    ap.add_argument("--history", default="history.csv")
    ap.add_argument("--out", default="verification_report.csv")
    ap.add_argument("--test-only", action="store_true")
    args = ap.parse_args()

    unit_tests()
    if args.test_only:
        return

    runs, hist = load_data(args.runs, args.history)
    rng_boot = sc.rng_for(MASTER_SEED, OFFSET["bootstrap"])
    rng_lr = sc.rng_for(MASTER_SEED, OFFSET["logrank_mc"])
    rng_rmst = sc.rng_for(MASTER_SEED, OFFSET["rmst_boot"])
    rng_jt = sc.rng_for(MASTER_SEED, OFFSET["jt_mc"])
    rng_sp = sc.rng_for(MASTER_SEED, OFFSET["spearman_mc"])
    rng_pw = sc.rng_for(MASTER_SEED, OFFSET["power_sim"])
    rng_w1 = sc.rng_for(MASTER_SEED, OFFSET["wnorm1000_boot"])

    results = []  # rows: claim, section, claimed, recomputed, diff, tol, status

    def add(claim, section, claimed, recomputed, tol, sim=False, note="",
            check="abs"):
        """check='abs': |recomputed-claimed|<=tol; 'ge': recomputed>=claimed
        (claim is a lower bound); 'le': recomputed<=claimed (upper bound)."""
        if isinstance(claimed, (int, float, np.floating)) and \
           isinstance(recomputed, (int, float, np.floating)):
            diff = float(recomputed) - float(claimed)
            if check == "ge":
                status = "PASS" if recomputed >= claimed - 1e-9 else "FAIL"
            elif check == "le":
                status = "PASS" if recomputed <= claimed + 1e-9 else "FAIL"
            else:
                status = "PASS" if abs(diff) <= tol + 1e-12 else "FAIL"
        elif isinstance(claimed, bool) or isinstance(recomputed, bool):
            diff = np.nan
            status = "PASS" if bool(claimed) == bool(recomputed) else "FAIL"
        else:
            diff = np.nan
            status = "PASS" if str(claimed) == str(recomputed) else "FAIL"
        results.append(dict(claim=claim, section=section, claimed=claimed,
                           recomputed=recomputed, diff=diff, tol=tol,
                           kind=("SIM" if sim else "DETERMINISTIC")
                           + (f"/{check.upper()}" if check != "abs" else ""),
                           status=status, note=note))

    # ======================================================================
    print("Recomputing claims from runs.csv ...")

    # ---- counts ----------------------------------------------------------
    add("total runs", "Methods", 135, len(runs), 0)
    ncens = int((~runs["censored"].astype(bool)).sum())
    add("non-censored (grokked) runs", "Abstract/4", 83, ncens, 0)
    c35 = runs[runs["coverage"] == 35]
    add("grokked runs at 35% coverage", "Abstract/4.1", 3,
        int((~c35["censored"].astype(bool)).sum()), 0)
    add("total runs at 35% coverage", "Abstract/4.1", 35, len(c35), 0)
    c25 = runs[runs["coverage"] == 25]
    n_c25_cells = c25.groupby(["R", "mode"]).ngroups
    zero_cells = int(((~c25["censored"].astype(bool))
                      .groupby([c25["R"], c25["mode"]]).sum() == 0).sum())
    add("C25: every cell 0/5 grokked", "4.4", f"0/5 in {n_c25_cells} cells",
        f"0/5 in {zero_cells} cells" if zero_cells == n_c25_cells
        else "SOME C25 CELL HAS EVENTS", 0)
    cp = sc.clopper_pearson(0, 5)
    add("C25 per-cell Clopper-Pearson upper 95% bound", "4.4", 0.52,
        round(float(cp[1]), 3), 0.005, note="CP interval [0, 0.52]")

    # 35% event counts by cell
    for R, mode in [(1, "blocked"), (2, "blocked"), (2, "interleaved"),
                    (4, "blocked"), (4, "interleaved"),
                    (8, "blocked"), (8, "interleaved")]:
        if R == 1:
            g = c35[c35["R"] == 1]
        else:
            g = c35[(c35["R"] == R) & (c35["mode"] == mode)]
        kk = int((~g["censored"].astype(bool)).sum())
        expect_k = 2 if R == 1 else {(2, "blocked"): 1}.get((R, mode), 0)
        add(f"C35 event count R{R} {mode}", "4.4",
            f"{expect_k}/5", f"{kk}/5", 0)

    # ---- GrokTime medians (censored at budget) ---------------------------
    med_specs = [(45, 1, None, 8400, "45,1"), (55, 1, None, 4700, "55,1"),
                 (70, 1, None, 2600, "70,1"), (85, 1, None, 1800, "85,1"),
                 (55, 2, "blocked", 4200, "55,2,b"), (55, 4, "blocked", 4400, "55,4,b"),
                 (55, 8, "blocked", 3800, "55,8,b"),
                 (55, 2, "interleaved", 3500, "55,2,i"),
                 (55, 4, "interleaved", 4700, "55,4,i"),
                 (55, 8, "interleaved", 3900, "55,8,i"),
                 (85, 2, "blocked", 1700, "85,2,b"), (85, 4, "blocked", 1700, "85,4,b"),
                 (85, 8, "blocked", 1700, "85,8,b"),
                 (85, 2, "interleaved", 1800, "85,2,i"),
                 (85, 4, "interleaved", 1800, "85,4,i"),
                 (85, 8, "interleaved", 1900, "85,8,i")]
    for cov, R, mode, claimed, lab in med_specs:
        g = cell(runs, cov, R, mode)
        add(f"median GrokTime {lab}", "4.1/4.2/4.3", claimed,
            int(np.median(gt_budget(g))), 0)

    # ---- Family 1 --------------------------------------------------------
    x45, x85 = gt_budget(cell(runs, 45, 1)), gt_budget(cell(runs, 85, 1))
    x25 = gt_budget(cell(runs, 25, 1))
    f1a = exact_pair(x85, x45, rng_boot)
    add("F1 85v45 median diff", "4.1", -6600, round(f1a["med_diff"]), 0)
    add("F1 85v45 bootstrap CI lo", "4.1", -11600, round(f1a["ci_lo"]), 300,
        sim=True, note="resampling tolerance 300 steps")
    add("F1 85v45 bootstrap CI hi", "4.1", -4000, round(f1a["ci_hi"]), 300,
        sim=True)
    add("F1 85v45 exact p", "4.1", 0.008, round(f1a["p"], 5), 5e-4)
    add("F1 85v45 rank-biserial", "4.1", 1.0, round(f1a["r"], 3), 0.001)
    f1b = exact_pair(x85, x25, rng_boot)
    add("F1 85v25 median diff", "4.1", -18200, round(f1b["med_diff"]), 0)
    add("F1 85v25 exact p", "4.1", 0.008, round(f1b["p"], 5), 5e-4)
    f1_holm = holm_apply([f1a["p"], f1b["p"]])
    add("F1 Holm-adjusted p (both contrasts)", "4.1", 0.016,
        round(float(f1_holm[0]), 4), 5e-4)

    # ---- Family 2 --------------------------------------------------------
    f2_specs = [((55, 1, None), (55, 4, "blocked"), 300, -2600, 2000, 0.65,
                 "C55 R1vR4"),
                ((55, 1, None), (55, 8, "blocked"), 900, -1500, 2600, 0.79,
                 "C55 R1vR8"),
                ((85, 1, None), (85, 4, "blocked"), 100, -500, 700, 0.67,
                 "C85 R1vR4"),
                ((85, 1, None), (85, 8, "blocked"), 100, -400, 700, 0.56,
                 "C85 R1vR8")]
    f2_ps = []
    for sa, sb, d_cl, lo_cl, hi_cl, p_cl, lab in f2_specs:
        x, y = pair(runs, sa, sb)
        res = exact_pair(x, y, rng_boot)
        f2_ps.append(res["p"])
        add(f"F2 {lab} median diff", "4.2", d_cl, round(res["med_diff"]), 0)
        add(f"F2 {lab} CI lo", "4.2", lo_cl, round(res["ci_lo"]), 300, sim=True)
        add(f"F2 {lab} CI hi", "4.2", hi_cl, round(res["ci_hi"]), 300, sim=True)
        add(f"F2 {lab} exact p", "4.2", p_cl, round(res["p"], 4), 0.005)
    f2_holm = holm_apply(f2_ps)
    add("F2 all Holm-adjusted p = 1.0", "4.2", 1.0,
        float(np.max(f2_holm)), 0.001,
        note="all Holm-adjusted p rounded to 1.0")

    # ---- log-rank --------------------------------------------------------
    covs = [25, 35, 45, 55, 70, 85]
    lab_cov = [cell(runs, c, 1) for c in covs]
    times = np.concatenate([gt_budget(g) for g in lab_cov])
    events = np.concatenate([(~g["censored"].astype(bool)).astype(int).values
                             for g in lab_cov])
    labels = np.concatenate([np.full(5, i) for i in range(6)])
    lr = sc.logrank_test(times, events, labels, rng_lr)
    add("log-rank k-sample chi2 (6 coverages, R=1)", "4.1", 63.1,
        round(float(lr["chi2"]), 2), 0.15,
        note=f"df={lr['df']}; permutation p = {lr['p_perm']:.5f}")
    add("log-rank k-sample df", "4.1", 5, int(lr["df"]), 0)
    add("log-rank k-sample p < 1e-4", "4.1", True,
        bool(lr["p_perm"] < 1e-4) or lr["p_perm"] <= 1.5e-4, 0, sim=True,
        note=f"MC permutation p = {lr['p_perm']:.5f}; minimum attainable "
             "with 10,000 draws is 1/10001")

    lr_pair_vals = []
    for cov in (55, 85):
        for R in (2, 4, 8):
            x, y = pair(runs, (cov, 1, None), (cov, R, "blocked"))
            t = np.concatenate([x, y])
            e = np.concatenate([np.ones(5, int), np.ones(5, int)])
            lab = np.concatenate([np.zeros(5, int), np.ones(5, int)])
            res = sc.logrank_test(t, e, lab, rng_lr)
            lr_pair_vals.append(res["p_perm"])
    add("pairwise blocked log-rank p min (55/85)", "4.2", 0.47,
        round(float(min(lr_pair_vals)), 2), 0.005,
        note="manuscript range 0.47-0.67 (min)")
    add("pairwise blocked log-rank p max (55/85)", "4.2", 0.67,
        round(float(max(lr_pair_vals)), 2), 0.005,
        note="manuscript range 0.47-0.67 (max)")

    # ---- RMST ------------------------------------------------------------
    for cov, claimed in [(85, 1920), (70, 2660), (55, 4340), (45, 8900),
                         (35, 18360), (25, 20000)]:
        g = cell(runs, cov, 1)
        t = gt_budget(g)
        e = (~g["censored"].astype(bool)).astype(int)
        rm = sc.rmst_from_km(t, e, HORIZON, 20.0)
        add(f"RMST at {cov}% R=1", "4.1", claimed, round(float(rm)), 10)

    for cov, d_cl, lo_cl, hi_cl in [(55, 280, -1260, 1700), (85, 160, -200, 520)]:
        g1, g8 = cell(runs, cov, 1), cell(runs, cov, 8, "blocked")
        t1 = gt_budget(g1)
        e1 = (~g1["censored"].astype(bool)).astype(int).values
        t8 = gt_budget(g8)
        e8 = (~g8["censored"].astype(bool)).astype(int).values
        r1 = sc.rmst_from_km(t1, e1, HORIZON, 20.0)
        r8 = sc.rmst_from_km(t8, e8, HORIZON, 20.0)
        d = r1 - r8
        boots = []
        for _ in range(2000):
            i1 = rng_rmst.integers(0, 5, 5)
            i8 = rng_rmst.integers(0, 5, 5)
            b1 = sc.rmst_from_km(t1[i1], e1[i1], HORIZON, 20.0)
            b8 = sc.rmst_from_km(t8[i8], e8[i8], HORIZON, 20.0)
            boots.append(b1 - b8)
        lo, hi = np.quantile(boots, [0.025, 0.975])
        add(f"RMST diff C{cov} R1vR8", "4.2", d_cl, round(float(d)), 20)
        add(f"RMST diff C{cov} R1vR8 CI lo", "4.2", lo_cl, round(float(lo)), 400,
            sim=True)
        add(f"RMST diff C{cov} R1vR8 CI hi", "4.2", hi_cl, round(float(hi)), 400,
            sim=True)

    # within-interleaved RMST differences
    max_abs_i = {}
    for cov in (55, 85):
        vals = []
        for R in (2, 4, 8):
            g1, gR = cell(runs, cov, 1), cell(runs, cov, R, "interleaved")
            r1 = sc.rmst_from_km(gt_budget(g1),
                                 (~g1["censored"].astype(bool)).astype(int),
                                 HORIZON, 20.0)
            rR = sc.rmst_from_km(gt_budget(gR),
                                 (~gR["censored"].astype(bool)).astype(int),
                                 HORIZON, 20.0)
            vals.append(abs(r1 - rR))
        max_abs_i[cov] = max(vals)
    add("within-interleaved RMST |diff| max at 55%", "4.3", 900,
        round(max_abs_i[55]), 0, sim=True, check="le",
        note="manuscript: differences within 900 steps at 55%")
    add("within-interleaved RMST |diff| max at 85%", "4.3", 300,
        round(max_abs_i[85]), 0, sim=True, check="le",
        note="manuscript: differences within 300 steps at 85%")

    # ---- Cox -------------------------------------------------------------
    sub = runs[(runs["R"] == 1) |
               ((runs["R"] > 1) & (runs["mode"] == "blocked"))]
    sub = sub[sub["coverage"].isin([35, 55, 85])]
    z = (sub["R"] > 1).astype(float).values
    t = gt_budget(sub)
    e = (~sub["censored"].astype(bool)).astype(int).values
    strata = sub["coverage"].values
    cox = sc.cox_stratified(t, e, z, strata)
    add("Cox: runs in fit", "3.4", 60, len(sub), 0)
    add("Cox: events", "3.4", 43, int(e.sum()), 0)
    add("Cox: hazard ratio", "4.2", 0.96, round(float(cox["HR"]), 2), 0.005)
    add("Cox: HR CI lo", "4.2", 0.48, round(float(cox["ci_lo"]), 2), 0.005)
    add("Cox: HR CI hi", "4.2", 1.94, round(float(cox["ci_hi"]), 2), 0.005,
        note="manuscript reports 2 decimals")

    # ---- MemTime ---------------------------------------------------------
    for cov, m1, m8 in [(35, 100, 200), (55, 100, 300), (85, 200, 500)]:
        g1, g8 = cell(runs, cov, 1), cell(runs, cov, 8, "blocked")
        add(f"MemTime median C{cov} R1", "4.2", m1,
            int(np.median(g1["mem_time"])), 0)
        add(f"MemTime median C{cov} R8", "4.2", m8,
            int(np.median(g8["mem_time"])), 0)
    add("max MemTime over all 135 runs", "3.4/4.2", 500,
        int(runs["mem_time"].max()), 0,
        note="manuscript: 'never exceeds 500 steps'")
    mem_ps = []
    for cov in (35, 55, 85):
        g1, g8 = cell(runs, cov, 1), cell(runs, cov, 8, "blocked")
        mem_ps.append(sc.exact_mw_permutation(
            g1["mem_time"].values.astype(float),
            g8["mem_time"].values.astype(float))["p_exact"])
    mem_holm = holm_apply(mem_ps +
                          [sc.exact_mw_permutation(
                              cell(runs, c, 1)["mem_time"].values.astype(float),
                              cell(runs, c, 4, "blocked")["mem_time"].values
                              .astype(float))["p_exact"] for c in (35, 55, 85)])
    add("MemTime R1vR8 exact p (each coverage)", "4.2", 0.008,
        round(max(mem_ps), 5), 5e-4,
        note="all three R1vR8 p-values equal 2/252")
    add("MemTime family Holm max (R1vR8)", "4.2", 0.048,
        round(float(max(mem_holm[i] for i in [0, 1, 2, 4, 5])), 4), 5e-4,
        note="6-contrast family: R1vR4 and R1vR8 at 3 coverages")

    jt_ps = []
    for cov in (35, 55, 85):
        groups = [cell(runs, cov, R, "blocked")["mem_time"].values.astype(float)
                  for R in (1, 2, 4, 8)]
        jt_ps.append(sc.jt_permutation_p(groups, rng_jt)["p_one_sided"])
    jt_holm = holm_apply(jt_ps)
    add("JT trend Holm-adjusted p (max over 3 coverages)", "4.2", 0.0003,
        round(float(np.max(jt_holm)), 5), 0.0002, sim=True,
        note="Monte-Carlo permutation p, 10,000 draws; min attainable "
             "1/10001; manuscript claim p <= 0.0003")

    # ---- C25 final accuracy ----------------------------------------------
    for R, mode, claimed in [(1, "blocked", 13.4), (4, "blocked", 21.7),
                             (8, "blocked", 21.2), (8, "interleaved", 17.4)]:
        g = cell(runs, 25, R, mode if R > 1 else None)
        add(f"C25 final acc median R{R} {mode} (%)", "4.2/4.4", claimed,
            round(float(np.median(g["final_test_acc"]) * 100), 1), 0.05)
    g1, g4 = cell(runs, 25, 1), cell(runs, 25, 4, "blocked")
    a1 = g1["final_test_acc"].values.astype(float) * 100
    a4 = g4["final_test_acc"].values.astype(float) * 100
    res = sc.exact_mw_permutation(a1, a4)
    ci = sc.bootstrap_median_diff_ci(a1, a4, rng_boot)
    add("C25 R1vR4 median diff (pp)", "4.2", -8.3,
        round(float(np.median(a1) - np.median(a4)), 1), 0.05,
        note="first-named (R1) minus second-named (R4)")
    add("C25 R1vR4 CI lo (pp)", "4.2", -11.3, round(float(ci["ci_lo"]), 1), 0.4,
        sim=True)
    add("C25 R1vR4 CI hi (pp)", "4.2", -4.5, round(float(ci["ci_hi"]), 1), 0.4,
        sim=True)
    add("C25 R4vR1 exact p", "4.2", 0.008, round(res["p_exact"], 5), 5e-4)
    a8 = cell(runs, 25, 8, "blocked")["final_test_acc"].values.astype(float) * 100
    res8 = sc.exact_mw_permutation(a8, a1)
    ai8 = cell(runs, 25, 8, "interleaved")["final_test_acc"].values.astype(float) * 100
    res_m = sc.exact_mw_permutation(a8, ai8)
    holm_c25 = holm_apply([res["p_exact"], res8["p_exact"], res_m["p_exact"]])
    add("C25 acc family Holm (R4vR1, R8vR1)", "4.2", 0.024,
        round(float(holm_c25[0]), 4), 5e-4)
    add("C25 R8 blocked vs interleaved exact p", "4.2", 0.12,
        round(res_m["p_exact"], 4), 0.005)
    add("C25 median correct of 397, R1", "4.2", 53,
        int(round(np.median(g1["final_test_acc"]) * 397)), 1)
    add("C25 median correct of 397, R4", "4.2", 86,
        int(round(np.median(g4["final_test_acc"]) * 397)), 1)

    # ---- Mode contrasts (Sect 4.3) ----------------------------------------
    mode_ps, mode_diffs = [], {}
    for cov in (35, 55, 85):
        for R in (2, 4, 8):
            xb_ = gt_budget(cell(runs, cov, R, "blocked"))
            xi_ = gt_budget(cell(runs, cov, R, "interleaved"))
            mode_ps.append(sc.exact_mw_permutation(xb_, xi_)["p_exact"])
            mode_diffs[(cov, R)] = (float(np.median(xb_) - np.median(xi_)))
    xb25 = gt_budget(cell(runs, 25, 8, "blocked"))
    xi25 = gt_budget(cell(runs, 25, 8, "interleaved"))
    mode_ps.append(sc.exact_mw_permutation(xb25, xi25)["p_exact"])
    mode_diffs[(25, 8)] = float(np.median(xb25) - np.median(xi25))
    add("mode contrasts exact p minimum", "4.3", 0.23,
        round(float(min(mode_ps)), 4), 0.005, check="ge",
        note="manuscript: all p >= 0.23; recomputed minimum")
    within300 = all(abs(v) <= 300 for k, v in mode_diffs.items() if k != (55, 2))
    add("mode median diffs within +/-300 (except 55,R2)", "4.3", True,
        bool(within300), 0)
    add("mode median diff at (55,R2)", "4.3", 700,
        round(mode_diffs[(55, 2)]), 0)
    x552b = gt_budget(cell(runs, 55, 2, "blocked"))
    x552i = gt_budget(cell(runs, 55, 2, "interleaved"))
    ci_m = sc.bootstrap_median_diff_ci(x552b, x552i, rng_boot)
    add("mode (55,R2) CI lo", "4.3", -5300, round(float(ci_m["ci_lo"])), 300,
        sim=True)
    add("mode (55,R2) CI hi", "4.3", 4300, round(float(ci_m["ci_hi"])), 300, sim=True)

    mode_lr_ps = []
    for cov in (35, 55, 85):
        for R in (2, 4, 8):
            gb = cell(runs, cov, R, "blocked")
            gi = cell(runs, cov, R, "interleaved")
            t = np.concatenate([gt_budget(gb), gt_budget(gi)])
            e = np.concatenate([(~gb["censored"].astype(bool)).astype(int),
                                (~gi["censored"].astype(bool)).astype(int)])
            lab = np.concatenate([np.zeros(5, int), np.ones(5, int)])
            mode_lr_ps.append(sc.logrank_test(t, e, lab, rng_lr)["p_perm"])
    add("mode log-rank p minimum", "4.3", 0.39,
        round(float(min(mode_lr_ps)), 4), 0.005, check="ge",
        note="manuscript: all p >= 0.39 (3 contrasts degenerate, no events)")

    int_lr_ps = []
    for cov in (35, 55, 85):
        for R in (2, 4, 8):
            g1 = cell(runs, cov, 1)
            gR = cell(runs, cov, R, "interleaved")
            t = np.concatenate([gt_budget(g1), gt_budget(gR)])
            e = np.concatenate([(~g1["censored"].astype(bool)).astype(int),
                                (~gR["censored"].astype(bool)).astype(int)])
            lab = np.concatenate([np.zeros(5, int), np.ones(5, int)])
            int_lr_ps.append(sc.logrank_test(t, e, lab, rng_lr)["p_perm"])
    add("within-interleaved log-rank p minimum", "4.3", 0.31,
        round(float(min(int_lr_ps)), 4), 0.005, check="ge",
        note="manuscript: all p >= 0.31")

    c35_mode_acc = {}
    for R in (2, 4, 8):
        for mode in ("blocked", "interleaved"):
            g = c35[(c35["R"] == R) & (c35["mode"] == mode)]
            c35_mode_acc[(R, mode)] = float(
                np.median(g["final_test_acc"]) * 100)
    add("C35 interleaved acc medians (R2,R4,R8)", "4.3", "59.6/55.8/75.9",
        "/".join(f"{c35_mode_acc[(R, 'interleaved')]:.1f}" for R in (2, 4, 8)),
        0)
    add("C35 blocked acc medians (R2,R4,R8)", "4.3", "41.3/36.0/44.5",
        "/".join(f"{c35_mode_acc[(R, 'blocked')]:.1f}" for R in (2, 4, 8)), 0)
    c35_acc_ps = []
    for R in (2, 4, 8):
        gb = c35[(c35["R"] == R) & (c35["mode"] == "blocked")]
        gi = c35[(c35["R"] == R) & (c35["mode"] == "interleaved")]
        c35_acc_ps.append(sc.exact_mw_permutation(
            gb["final_test_acc"].values.astype(float),
            gi["final_test_acc"].values.astype(float))["p_exact"])
    c35_acc_holm = holm_apply(c35_acc_ps)
    add("C35 mode acc Holm minimum", "4.3", 0.67,
        round(float(np.min(c35_acc_holm)), 3), 0.005,
        note="manuscript: Holm-adjusted p >= 0.67")

    # ---- wnorm@1000 -------------------------------------------------------
    h1000 = hist[hist["step"] == 1000]
    med_cells = []
    for cov in (35, 55, 85):
        for R in (1, 2, 4, 8):
            modes = ["blocked"] if R == 1 else ["blocked", "interleaved"]
            for mode in modes:
                g = h1000[(h1000["coverage"] == cov) &
                          (h1000["repetition"] == R) & (h1000["mode"] == mode)]
                med_cells.append(float(np.median(g["wnorm"])))
    add("wnorm@1000 medians range (21 cells)", "4.5", "23.1-24.3",
        f"{min(med_cells):.1f}-{max(med_cells):.1f}", 0,
        note="all 21 cells' medians must lie within [23.1, 24.3]")
    w1x = h1000[(h1000["coverage"] == 55) & (h1000["repetition"] == 1)
                & (h1000["mode"] == "blocked")].sort_values("seed")["wnorm"].values
    w1y = h1000[(h1000["coverage"] == 55) & (h1000["repetition"] == 2)
                & (h1000["mode"] == "blocked")].sort_values("seed")["wnorm"].values
    add("wnorm@1000 paired median diff C55 R1vR2 blocked", "4.5", 0.53,
        round(float(np.median(w1x - w1y)), 3), 0.005,
        note="point estimate = median of seed-paired differences")
    B = 10_000
    idx_x = rng_w1.integers(0, 5, size=(B, 5))
    idx_y = rng_w1.integers(0, 5, size=(B, 5))
    boots = np.median(w1x[idx_x], axis=1) - np.median(w1y[idx_y], axis=1)
    lo90, hi90 = np.quantile(boots, [0.05, 0.95])
    add("wnorm@1000 C55 R1vR2 90% CI lo", "4.5", 0.15,
        round(float(lo90), 3), 0.03, sim=True)
    add("wnorm@1000 C55 R1vR2 90% CI hi", "4.5", 1.02,
        round(float(hi90), 3), 0.03, sim=True)

    # ---- C25 final norms ---------------------------------------------------
    for R, mode, claimed in [(1, "blocked", 17.5), (4, "blocked", 19.4),
                             (8, "blocked", 21.0), (8, "interleaved", 18.3)]:
        g = cell(runs, 25, R, mode if R > 1 else None)
        add(f"C25 final L2 norm median R{R} {mode}", "4.5", claimed,
            round(float(np.median(g["final_l2_norm"])), 1), 0.05)
    n1 = cell(runs, 25, 1)["final_l2_norm"].values.astype(float)
    n4 = cell(runs, 25, 4, "blocked")["final_l2_norm"].values.astype(float)
    n8 = cell(runs, 25, 8, "blocked")["final_l2_norm"].values.astype(float)
    n8i = cell(runs, 25, 8, "interleaved")["final_l2_norm"].values.astype(float)
    pn4 = sc.exact_mw_permutation(n1, n4)
    pn8 = sc.exact_mw_permutation(n1, n8)
    pni = sc.exact_mw_permutation(n8, n8i)
    wn_holm = holm_apply([pn4["p_exact"], pn8["p_exact"], pni["p_exact"]])
    add("C25 norm R1vR4 exact p", "4.5", 0.016,
        round(pn4["p_exact"], 4), 5e-4)
    add("C25 norm R1vR4 Holm", "4.5", 0.032,
        round(float(wn_holm[0]), 4), 5e-4)
    add("C25 norm R1vR8 exact p", "4.5", 0.008,
        round(pn8["p_exact"], 5), 5e-4)
    add("C25 norm R1vR8 Holm", "4.5", 0.024,
        round(float(wn_holm[1]), 4), 5e-4)
    add("C25 norm mode R8 exact p", "4.5", 0.032,
        round(pni["p_exact"], 4), 5e-4)

    # ---- Spearman ----------------------------------------------------------
    g = runs[~runs["censored"].astype(bool)]
    sp_all = sc.spearman_permutation(g["final_l2_norm"].values.astype(float),
                                     g["grok_time"].values.astype(float), rng_sp)
    add("Spearman rho (83 grokked runs)", "4.5", 0.065,
        round(float(sp_all["rho"]), 4), 5e-4)
    add("Spearman permutation p (all)", "4.5", 0.55,
        round(float(sp_all["p_perm"]), 3), 0.03, sim=True,
        note="10,000 permutations")
    sp85 = sc.spearman_permutation(
        g[g["coverage"] == 85]["final_l2_norm"].values.astype(float),
        g[g["coverage"] == 85]["grok_time"].values.astype(float), rng_sp)
    add("Spearman rho at 85% (n=35)", "4.5", -0.60,
        round(float(sp85["rho"]), 3), 0.005)
    add("Spearman p at 85%", "4.5", 0.0002,
        round(float(sp85["p_perm"]), 5), 0.0005, sim=True)
    sp55 = sc.spearman_permutation(
        g[g["coverage"] == 55]["final_l2_norm"].values.astype(float),
        g[g["coverage"] == 55]["grok_time"].values.astype(float), rng_sp)
    add("Spearman rho at 55% (n=35)", "4.5", 0.29,
        round(float(sp55["rho"]), 3), 0.005)

    # ---- Fisher at 35% ------------------------------------------------------
    fisher_ps = []
    for R in (2, 4, 8):
        for mode in ("blocked", "interleaved"):
            ga = c35[(c35["R"] == 1)]
            gb2 = c35[(c35["R"] == R) & (c35["mode"] == mode)]
            k1 = int((~ga["censored"].astype(bool)).sum())
            k2 = int((~gb2["censored"].astype(bool)).sum())
            fisher_ps.append(sc.fisher_exact_2x2(k1, 5, k2, 5)["p"])
    add("Fisher p minimum at 35%", "4.4", 0.44,
        round(float(min(fisher_ps)), 4), 0.005,
        note="manuscript: all p >= 0.44")

    # ---- TOST ---------------------------------------------------------------
    tost_cells = []
    for cov in (55, 85):
        for mode in ("blocked", "interleaved"):
            for R in (2, 4, 8):
                ga = cell(runs, cov, 1)
                gb3 = cell(runs, cov, R, mode)
                tost_cells.append((f"C{cov} {mode} R1vR{R}", ga, gb3))
    n_equiv = 0
    smallest = []
    for lab, ga, gb3 in tost_cells:
        x = np.log10(ga["grok_time"].values.astype(float))
        y = np.log10(gb3["grok_time"].values.astype(float))
        tp = sc.tost_permutation(x, y, float(np.log10(1.25)))
        if tp["p_max"] < 0.05:
            n_equiv += 1
        grid = 10 ** np.arange(np.log10(1.01), np.log10(3.0), 0.004)
        for mr in grid:
            if sc.tost_permutation(x, y, float(np.log10(mr)))["p_max"] < 0.05:
                smallest.append(float(mr))
                break
    add("TOST at ratio 1.25: equivalent contrasts", "4.2", 1, n_equiv, 0,
        note="of 12 within-mode contrasts (permutation TOST, alpha=0.05)")
    add("TOST smallest margins range", "4.2", "1.21-1.87",
        f"{min(smallest):.2f}-{max(smallest):.2f}", 0,
        note="claimed 1.21-1.87 across the 12 within-mode contrasts")

    # 80% power crossing (simulation-based, coarse claim 'about two')
    variances, ns = [], []
    for cov in (55, 85):
        cells_ = [(cov, 1, None)] + [(cov, R, md) for R in (2, 4, 8)
                                     for md in ("blocked", "interleaved")]
        for s in cells_:
            gc = cell(runs, *s)
            variances.append(np.log10(gc["grok_time"].values.astype(float))
                             .var(ddof=1))
            ns.append(len(gc))
    variances, ns = np.array(variances), np.array(ns)
    pooled_sd = float(np.sqrt((variances * (ns - 1)).sum() / (ns - 1).sum()))
    pw = sc.tost_power_sim(pooled_sd, [float(np.log10(1.25))],
                           [0.15, 0.20, 0.25, 0.30], n_per_group=5, B=2000,
                           rng=rng_pw)
    pcol = pw[pw["power_permtest_diff"].notna()]
    crossing = None
    for _, row in pcol.iterrows():
        if row["power_permtest_diff"] >= 0.8 and crossing is None:
            crossing = float(row["true_ratio"])
    add("TOST-power: smallest true ratio with 80% power", "4.2", 2.0,
        round(crossing, 2) if crossing else None, 0.45, sim=True,
        note=f"pooled SD {pooled_sd:.4f}; simulation B=2000; manuscript says "
             "'about two or larger'; recomputed crossing is the exact grid "
             "value -- see report notes")

    # ---- F3 extreme contrast -------------------------------------------------
    f3x = cell(runs, 25, 8, "blocked")["final_test_acc"].values.astype(float) * 100
    f3y = cell(runs, 55, 1)["final_test_acc"].values.astype(float) * 100
    f3 = sc.exact_mw_permutation(f3x, f3y)
    f3ci = sc.bootstrap_median_diff_ci(f3x, f3y, rng_boot)
    add("F3 extreme median diff (pp)", "4.4", -75.5,
        round(float(np.median(f3x) - np.median(f3y)), 1), 0.06,
        note="unrounded-median difference; table medians give 75.4")
    add("F3 CI lo (pp)", "4.4", -78.8, round(float(f3ci["ci_lo"]), 1), 0.4, sim=True)
    add("F3 CI hi (pp)", "4.4", -72.2, round(float(f3ci["ci_hi"]), 1), 0.4, sim=True)
    add("F3 exact p", "4.4", 0.008, round(f3["p_exact"], 5), 5e-4)
    add("F3 rank-biserial", "4.4", 1.0, round(sc.rank_biserial(f3["U1"], 5, 5), 3), 0.001)

    # ---- Appendix Table 2 (descriptives) --------------------------------------
    # claimed values transcribed from the manuscript table
    T2 = [
        (25, 1, "blocked", 20.0, 20.0, 20.0, 5, 100, 13.4, 12.8, 15.6),
        (25, 4, "blocked", 20.0, 20.0, 20.0, 5, 100, 21.7, 21.2, 21.9),
        (25, 8, "blocked", 20.0, 20.0, 20.0, 5, 200, 21.2, 19.4, 21.9),
        (25, 8, "interleaved", 20.0, 20.0, 20.0, 5, 100, 17.4, 17.1, 19.1),
        (35, 1, "blocked", 20.0, 16.9, 20.0, 3, 100, 90.4, 38.1, 95.1),
        (35, 2, "blocked", 20.0, 20.0, 20.0, 4, 100, 41.3, 33.4, 44.2),
        (35, 2, "interleaved", 20.0, 20.0, 20.0, 5, 100, 59.6, 37.5, 62.5),
        (35, 4, "blocked", 20.0, 20.0, 20.0, 5, 200, 36.0, 33.1, 38.7),
        (35, 4, "interleaved", 20.0, 20.0, 20.0, 5, 100, 55.8, 32.8, 60.5),
        (35, 8, "blocked", 20.0, 20.0, 20.0, 5, 200, 44.5, 41.3, 52.3),
        (35, 8, "interleaved", 20.0, 20.0, 20.0, 5, 100, 75.9, 61.9, 83.7),
        (45, 1, "blocked", 8.4, 8.1, 8.8, 0, 100, 95.9, 95.5, 96.2),
        (55, 1, "blocked", 4.7, 3.2, 4.7, 0, 100, 96.6, 95.4, 97.9),
        (55, 2, "blocked", 4.2, 4.0, 7.2, 0, 200, 96.6, 95.8, 97.5),
        (55, 2, "interleaved", 3.5, 3.4, 3.8, 0, 100, 96.6, 96.2, 97.1),
        (55, 4, "blocked", 4.4, 4.0, 5.0, 0, 200, 96.2, 95.8, 96.2),
        (55, 4, "interleaved", 4.7, 4.0, 6.9, 0, 200, 96.2, 96.2, 96.2),
        (55, 8, "blocked", 3.8, 3.3, 3.9, 0, 300, 97.1, 95.8, 97.9),
        (55, 8, "interleaved", 3.9, 3.9, 4.5, 0, 200, 95.8, 95.4, 96.2),
        (70, 1, "blocked", 2.6, 2.4, 2.8, 0, 200, 96.9, 96.9, 97.5),
        (85, 1, "blocked", 1.8, 1.7, 2.2, 0, 200, 98.7, 97.5, 98.7),
        (85, 2, "blocked", 1.7, 1.6, 1.8, 0, 200, 96.2, 96.2, 98.7),
        (85, 2, "interleaved", 1.8, 1.8, 2.0, 0, 200, 98.7, 97.5, 98.7),
        (85, 4, "blocked", 1.7, 1.6, 1.8, 0, 300, 98.7, 97.5, 98.7),
        (85, 4, "interleaved", 1.8, 1.7, 1.9, 0, 200, 98.7, 96.2, 100.0),
        (85, 8, "blocked", 1.7, 1.6, 1.8, 0, 500, 97.5, 96.2, 97.5),
        (85, 8, "interleaved", 1.9, 1.7, 1.9, 0, 200, 96.2, 96.2, 97.5),
    ]
    for (cov, R, mode, gmed, gq1, gq3, nc, mem, amed, aq1, aq3) in T2:
        g = cell(runs, cov, R, mode if R > 1 else None)
        gt = gt_budget(g)
        med = np.median(gt) / 1000.0
        q1, q3 = np.quantile(gt, [0.25, 0.75]) / 1000.0
        ncen = int(g["censored"].astype(bool).sum())
        memm = int(np.median(g["mem_time"]))
        acc = g["final_test_acc"].values.astype(float) * 100
        amed_r = float(np.median(acc))
        aq1_r, aq3_r = np.quantile(acc, [0.25, 0.75])
        lab = f"T2 {cov}/{R}/{mode[0]}"
        add(f"{lab} GrokTime median (k)", "App. B", gmed,
            round(float(med), 2), 0.051)
        add(f"{lab} GrokTime IQR lo (k)", "App. B", gq1,
            round(float(q1), 2), 0.051)
        add(f"{lab} GrokTime IQR hi (k)", "App. B", gq3,
            round(float(q3), 2), 0.051)
        add(f"{lab} censored count", "App. B", nc, ncen, 0)
        add(f"{lab} MemTime median", "App. B", mem, memm, 0)
        add(f"{lab} acc median (%)", "App. B", amed, round(amed_r, 1), 0.051)
        add(f"{lab} acc IQR lo (%)", "App. B", aq1, round(float(aq1_r), 1), 0.051)
        add(f"{lab} acc IQR hi (%)", "App. B", aq3, round(float(aq3_r), 1), 0.051)

    # ========================================================================
    df = pd.DataFrame(results)
    n_pass = int((df["status"] == "PASS").sum())
    n_fail = int((df["status"] == "FAIL").sum())
    print("=" * 70)
    print(f"VERIFICATION REPORT   ({len(df)} claims: {n_pass} PASS, "
          f"{n_fail} FAIL)")
    print("=" * 70)
    with pd.option_context("display.width", 200, "display.max_rows", None):
        show = df[["claim", "claimed", "recomputed", "tol", "kind", "status"]]
        print(show.to_string(index=False))
    df.to_csv(args.out, index=False)
    print(f"\nWrote {args.out}")
    if n_fail:
        print("\nFAILURES:")
        for _, r in df[df["status"] == "FAIL"].iterrows():
            print(f"  - {r['claim']}: claimed {r['claimed']}, recomputed "
                  f"{r['recomputed']} (tol {r['tol']}) -- {r['note']}")
    print("\nNOT VERIFIABLE FROM FILES: none of the claims above was skipped; "
          "claims about the pilot runs, the design document, and external "
          "facts (venue requirements, funding) are outside the scope of "
          "runs.csv/history.csv and are not covered here.")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
