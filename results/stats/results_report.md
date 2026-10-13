# Analysis report: grokking experiment (modular addition, p = 23)

Generated 2026-10-11 17:05 UTC by `analyze.py --runs runs.csv --history history.csv --out results --margins 0.1 0.25 0.5`

## 0. Scope, mapping, and declarations

Every number below was computed by this pipeline from the per-run table; no data were imputed or invented. Input files: `runs.csv` (SHA-256 `95052c36c4f662fc...`), `history.csv` (SHA-256 `ed8154262f177ae1...`).

Column mapping used: {"run_id": "run_id", "coverage": "coverage", "R": "R", "mode": "mode", "seed": "seed", "grok_time": "grok_time", "censored": "censored", "mem_time": "mem_time", "final_train_acc": "final_train_acc", "final_test_acc": "final_test_acc", "final_l2_norm": "final_l2_norm", "n_test": "n_test", "stop_step": "stop_step"}; history columns: {"R": "repetition", "l2_norm": "wnorm"} (history is keyed by coverage, R, mode, seed; evaluated at step 1 and every 100 steps).

**Please confirm**: `grok_time` is the first evaluation step with test accuracy >= 95% (empty if never within 20,000 steps), `censored` marks those runs, `mem_time` the first step with training accuracy >= 95%, `n_test` the held-out set size (79/159/238/291/344/397 for coverage 85/70/55/45/35/25), `stop_step` the run's last evaluation step.

Randomness: numpy `default_rng` seeded at 20260922 with documented per-analysis offsets {"task1 bootstrap_median_diff": 101, "task2 logrank_mc": 201, "task2 rmst_bootstrap": 301, "task4 jt_mc": 401, "task4 spearman_mc": 501, "task3 power_sim": 601, "task4 wnorm1000_boot": 701}. Deterministic enumerations consume no randomness.

Environment: Python 3.12.15, NumPy 2.1.3, SciPy 1.14.1, pandas 2.2.3, matplotlib 3.9.2. Full log: `env_log.txt`.

## (a) Sanity checks

| check | expected | observed | status | note |
|---|---|---|---|---|
| row count | 135 | 135 | PASS |  |
| condition count (27 cells x 5 seeds) | 27 | 27 | PASS |  |
| seeds per condition all == 5 | True | True | PASS |  |
| seeds are exactly {0,1,2,3,4} in every condition | True | True | PASS |  |
| arm A runs (R=1, six coverages) | 30 | 30 | PASS |  |
| arm B runs (blocked R in {2,4,8} at 35/55/85) | 45 | 45 | PASS |  |
| arm C runs (interleaved R in {2,4,8} at 35/55/85) | 45 | 45 | PASS |  |
| arm D runs (25%: blocked 4,8 + interleaved 8) | 15 | 15 | PASS |  |
| non-censored runs | 83 | 83 | PASS |  |
| censored at C35 R1 | 3/5 | 3/5 | PASS |  |
| grokked runs across the seven 35% conditions | 3 | 3 | PASS |  |
| C35 R1 grok steps | [14900, 16900] | [14900, 16900] | PASS |  |
| C35 R2 blocked grok steps | [11900] | [11900] | PASS |  |
| n_test per coverage | {25: 397, 35: 344, 45: 291, 55: 238, 70: 159, 85: 79} | {25: 397, 35: 344, 45: 291, 55: 238, 70: 159, 85: 79} | PASS | from per-run logs; equals 529 - round(coverage/100*529) |
| n_test == 529 - round(cov*529) for every run | True | True | PASS |  |
| grok times are multiples of 100 (no step-1 groks) | True | True | PASS |  |
| stop_step == grok_time (grokked) / 20,000 (censored) | True | True | PASS |  |
| censored <=> grok_time empty | True | True | PASS |  |
| mem_time present for all runs | True | True | PASS |  |
| manuscript claim: MemTime never exceeds 500 | max <= 500 | max = 500 | PASS | claim holds with equality |
| manuscript claim: median MemTime across 135 runs | 200 | 200 | PASS |  |
| final_test_acc * n_test is an integer for every run | True | True | PASS |  |
| history covers all 135 runs | 135 | 135 | PASS |  |
| history steps lie on the {1, 100, 200, ...} grid | True | True | PASS |  |
| history has a step-1000 row for every run | 135 | 135 | PASS |  |
| Table A3 descriptive rows reproduced | 27/27 | 27/27 | PASS | GrokTime medians count censored runs at the 20,000 budget |

**26 PASS / 0 FAIL**.

## 1. Exact two-sample tests (replacing the inconsistent 'exact' Mann-Whitney values)

Method: exact permutation test of the Mann-Whitney U statistic with midranks -- all C(10,5) = 252 label assignments enumerated (two-sided: p = proportion with |U - n1*n2/2| >= observed). scipy's asymptotic tie-corrected p is shown alongside, labelled as such; it is the method behind several archived p-values. Rank-biserial r = 1 - 2*U1/(n1*n2) with U1 the U statistic of the FIRST-named group (r = +1 means the first group is entirely smaller; r has the opposite sign of the median difference). Effect sizes: Hodges-Lehmann estimate and a 95% percentile bootstrap CI of the median difference (10,000 resamples, within-group resampling; with five tied 100-step values per group these CIs are coarse by construction).

Censoring policy for GrokTime rank tests: **budget** (censored runs enter at the 20,000-step budget = worst rank). Survival analyses in Section 2 handle censoring properly.

**Family definitions (declared here; NOT pre-specified -- the original plan's families differed, manuscript deviation-log item iii):**

- **F1_coverage_R1_groktime** (Coverage contrasts at R=1, GrokTime (steps)): C85 R1 vs C45 R1; C85 R1 vs C25 R1

- **F2_blocked_rep_groktime** (Blocked repetition at matched coverage, GrokTime (steps)): C55 R1 vs C55 R4 blocked; C55 R1 vs C55 R8 blocked; C85 R1 vs C85 R4 blocked; C85 R1 vs C85 R8 blocked

- **F3_extreme_finalacc** (Extreme contrast, final test accuracy (fraction)): C25 R8 blocked vs C55 R1

Holm correction is applied within each family.

| family | contrast | n1 | censored1 | n2 | censored2 | U1 | p_exact | p_scipy_asymptotic | rank_biserial | median_diff | hodges_lehmann | boot_ci_lo | boot_ci_hi | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F1_coverage_R1_groktime | C85 R1 vs C45 R1 (groktime) | 5 | 0 | 5 | 0 | 0 | 0.00794 | 0.01219 | 1 | -6600 | -6600 | -11600 | -4000 | 0.01588 |
| F1_coverage_R1_groktime | C85 R1 vs C25 R1 (groktime) | 5 | 0 | 5 | 5 | 0 | 0.00794 | 0.00749 | 1 | -18200 | -18200 | -18500 | -17600 | 0.01588 |
| F2_blocked_rep_groktime | C55 R1 vs C55 R4 blocked (groktime) | 5 | 0 | 5 | 0 | 10 | 0.65079 | 0.67517 | 0.2 | 300 | -300 | -2600 | 2000 | 1 |
| F2_blocked_rep_groktime | C55 R1 vs C55 R8 blocked (groktime) | 5 | 0 | 5 | 0 | 14 | 0.79365 | 0.83404 | -0.12 | 900 | 200 | -1500 | 2600 | 1 |
| F2_blocked_rep_groktime | C85 R1 vs C85 R4 blocked (groktime) | 5 | 0 | 5 | 0 | 15 | 0.6746 | 0.67329 | -0.2 | 100 | 100 | -500 | 700 | 1 |
| F2_blocked_rep_groktime | C85 R1 vs C85 R8 blocked (groktime) | 5 | 0 | 5 | 0 | 16 | 0.55556 | 0.52581 | -0.28 | 100 | 100 | -400 | 700 | 1 |
| F3_extreme_finalacc | C25 R8 blocked vs C55 R1 (final_test_acc) | 5 | 5 | 5 | 0 | 0 | 0.00794 | 0.01167 | 1 | -0.7548 | -0.7598 | -0.7884 | -0.7221 | 0.00794 |

## 2. Survival analysis of GrokTime (right-censored at 20,000)

Kaplan-Meier curves (manual implementation, tied discrete times handled exactly; censoring ticks marked): `figures/fig_km_a_R1_by_coverage.*` (R = 1 by coverage), `figures/fig_km_b_blocked.*` and `figures/fig_km_c_interleaved.*` (R in {1,2,4,8} at coverage 35/55/85). Full KM tables: `km_tables.csv`; per-condition RMST: `rmst_per_condition.csv`.

### 2.1 Log-rank tests

Manual log-rank with permutation p-values (10,000 Monte-Carlo permutations for k-sample tests; full enumeration of all 252 or 15,504 assignments for the 5-vs-5 and 5-vs-15 two-sample tests). The asymptotic chi-square p is reported for comparison; the permutation p is the declared one.

| family | contrast | n | events | chi2 | df | p_perm | p_chi2 | method | note |
|---|---|---|---|---|---|---|---|---|---|
| coverage_R1 | k-sample across coverage (25..85) at R=1 | 30 | 22 | 63.144 | 5 | 0 | 0 | Monte-Carlo permutation with 10000 random label assignments |  |
| coverage_R1 | 85% vs 45% at R=1 | 10 | 10 | 9.7007 | 1 | 0.00794 | 0.00184 | exact enumeration of all 252 C(10,5) label assignments |  |
| coverage_R1 | 85% vs 25% at R=1 | 10 | 5 | 9.7007 | 1 | 0.00794 | 0.00184 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_blocked | C35 blocked: R1 vs R2 | 10 | 3 | 0.2645 | 1 | 1 | 0.60707 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_blocked | C35 blocked: R1 vs R4 | 10 | 2 | 2.2422 | 1 | 0.44444 | 0.13429 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_blocked | C35 blocked: R1 vs R8 | 10 | 2 | 2.2422 | 1 | 0.44444 | 0.13429 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_blocked | C35 blocked: k-sample across R (1,2,4,8) | 20 | 3 | 3.9117 | 3 | 0.5596 | 0.27116 | Monte-Carlo permutation with 10000 random label assignments |  |
| rep_blocked | C55 blocked: R1 vs R2 | 10 | 10 | 0.6557 | 1 | 0.46825 | 0.41807 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_blocked | C55 blocked: R1 vs R4 | 10 | 10 | 0.2509 | 1 | 0.66667 | 0.61644 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_blocked | C55 blocked: R1 vs R8 | 10 | 10 | 0.4777 | 1 | 0.52381 | 0.48945 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_blocked | C55 blocked: k-sample across R (1,2,4,8) | 20 | 20 | 3.0494 | 3 | 0.4821 | 0.38407 | Monte-Carlo permutation with 10000 random label assignments |  |
| rep_blocked | C85 blocked: R1 vs R2 | 10 | 10 | 0.5267 | 1 | 0.54762 | 0.46798 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_blocked | C85 blocked: R1 vs R4 | 10 | 10 | 0.4198 | 1 | 0.56349 | 0.51701 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_blocked | C85 blocked: R1 vs R8 | 10 | 10 | 0.8211 | 1 | 0.46825 | 0.36486 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_blocked | C85 blocked: k-sample across R (1,2,4,8) | 20 | 20 | 1.2074 | 3 | 0.8081 | 0.75122 | Monte-Carlo permutation with 10000 random label assignments |  |
| rep_interleaved | C35 interleaved: R1 vs R2 | 10 | 2 | 2.2422 | 1 | 0.44444 | 0.13429 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_interleaved | C35 interleaved: R1 vs R4 | 10 | 2 | 2.2422 | 1 | 0.44444 | 0.13429 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_interleaved | C35 interleaved: R1 vs R8 | 10 | 2 | 2.2422 | 1 | 0.44444 | 0.13429 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_interleaved | C35 interleaved: k-sample across R (1,2,4,8) | 20 | 2 | 6.7004 | 3 | 0.2168 | 0.08208 | Monte-Carlo permutation with 10000 random label assignments |  |
| rep_interleaved | C55 interleaved: R1 vs R2 | 10 | 10 | 0.0004 | 1 | 0.98413 | 0.98471 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_interleaved | C55 interleaved: R1 vs R4 | 10 | 10 | 1.2209 | 1 | 0.31746 | 0.26918 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_interleaved | C55 interleaved: R1 vs R8 | 10 | 10 | 0.0266 | 1 | 0.88889 | 0.87055 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_interleaved | C55 interleaved: k-sample across R (1,2,4,8) | 20 | 20 | 0.3925 | 3 | 0.9581 | 0.94179 | Monte-Carlo permutation with 10000 random label assignments |  |
| rep_interleaved | C85 interleaved: R1 vs R2 | 10 | 10 | 0.0513 | 1 | 0.84127 | 0.82086 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_interleaved | C85 interleaved: R1 vs R4 | 10 | 10 | 0.6867 | 1 | 0.49206 | 0.40727 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_interleaved | C85 interleaved: R1 vs R8 | 10 | 10 | 0.5945 | 1 | 0.49206 | 0.44069 | exact enumeration of all 252 C(10,5) label assignments |  |
| rep_interleaved | C85 interleaved: k-sample across R (1,2,4,8) | 20 | 20 | 1.5912 | 3 | 0.7272 | 0.66138 | Monte-Carlo permutation with 10000 random label assignments |  |
| mode | C35 R2: blocked vs interleaved | 10 | 1 | 1 | 1 | 1 | 0.31731 | exact enumeration of all 252 C(10,5) label assignments |  |
| mode | C35 R4: blocked vs interleaved | 10 | 0 |  |  |  |  | skipped | zero events in both groups; time-based test degenerate |
| mode | C35 R8: blocked vs interleaved | 10 | 0 |  |  |  |  | skipped | zero events in both groups; time-based test degenerate |
| mode | C55 R2: blocked vs interleaved | 10 | 10 | 0.1281 | 1 | 0.75397 | 0.72046 | exact enumeration of all 252 C(10,5) label assignments |  |
| mode | C55 R4: blocked vs interleaved | 10 | 10 | 0.039 | 1 | 0.86508 | 0.84337 | exact enumeration of all 252 C(10,5) label assignments |  |
| mode | C55 R8: blocked vs interleaved | 10 | 10 | 1.0117 | 1 | 0.39683 | 0.31448 | exact enumeration of all 252 C(10,5) label assignments |  |
| mode | C85 R2: blocked vs interleaved | 10 | 10 | 0.3078 | 1 | 0.68254 | 0.57901 | exact enumeration of all 252 C(10,5) label assignments |  |
| mode | C85 R4: blocked vs interleaved | 10 | 10 | 0 | 1 | 1 | 0.99437 | exact enumeration of all 252 C(10,5) label assignments |  |
| mode | C85 R8: blocked vs interleaved | 10 | 10 | 0.0185 | 1 | 0.95238 | 0.89177 | exact enumeration of all 252 C(10,5) label assignments |  |
| mode | C25 R8: blocked vs interleaved | 10 | 0 |  |  |  |  | skipped | zero events in both groups; time-based test degenerate |

### 2.2 Restricted mean survival time (RMST, horizon 20,000 steps)

RMST per group with bootstrap 95% CIs for differences (10,000 within-group resamples). This is the main censoring-aware effect size for the repetition contrasts.

| family | contrast | events1 | events2 | rmst1 | rmst2 | diff | ci_lo | ci_hi |
|---|---|---|---|---|---|---|---|---|
| rep_blocked | C35 blocked: R1 vs R2 | 2 | 1 | 18360 | 18380 | -20 | -3060 | 3620 |
| rep_blocked | C35 blocked: R1 vs R4 | 2 | 0 | 18360 | 20000 | -1640 | -3680 | 0 |
| rep_blocked | C35 blocked: R1 vs R8 | 2 | 0 | 18360 | 20000 | -1640 | -3680 | 0 |
| rep_blocked | C55 blocked: R1 vs R2 | 5 | 5 | 4340 | 5260 | -920 | -2920 | 1040 |
| rep_blocked | C55 blocked: R1 vs R4 | 5 | 5 | 4340 | 4840 | -500 | -2160 | 1060 |
| rep_blocked | C55 blocked: R1 vs R8 | 5 | 5 | 4340 | 4060 | 280 | -1260 | 1700 |
| rep_blocked | C85 blocked: R1 vs R2 | 5 | 5 | 1920 | 1780 | 140 | -260 | 520 |
| rep_blocked | C85 blocked: R1 vs R4 | 5 | 5 | 1920 | 1800 | 120 | -260 | 480 |
| rep_blocked | C85 blocked: R1 vs R8 | 5 | 5 | 1920 | 1760 | 160 | -200 | 520 |
| rep_interleaved | C35 interleaved: R1 vs R2 | 2 | 0 | 18360 | 20000 | -1640 | -3680 | 0 |
| rep_interleaved | C35 interleaved: R1 vs R4 | 2 | 0 | 18360 | 20000 | -1640 | -3680 | 0 |
| rep_interleaved | C35 interleaved: R1 vs R8 | 2 | 0 | 18360 | 20000 | -1640 | -3680 | 0 |
| rep_interleaved | C55 interleaved: R1 vs R2 | 5 | 5 | 4340 | 4620 | -280 | -2920 | 1860 |
| rep_interleaved | C55 interleaved: R1 vs R4 | 5 | 5 | 4340 | 5200 | -860 | -2640 | 860 |
| rep_interleaved | C55 interleaved: R1 vs R8 | 5 | 5 | 4340 | 4560 | -220 | -1960 | 1360 |
| rep_interleaved | C85 interleaved: R1 vs R2 | 5 | 5 | 1920 | 1920 | -0 | -320 | 320 |
| rep_interleaved | C85 interleaved: R1 vs R4 | 5 | 5 | 1920 | 1820 | 100 | -220 | 440 |
| rep_interleaved | C85 interleaved: R1 vs R8 | 5 | 5 | 1920 | 1800 | 120 | -220 | 480 |
| mode | C35 R2: blocked vs interleaved | 1 | 0 | 18380 | 20000 | -1620 | -4860 | 0 |
| mode | C35 R4: blocked vs interleaved | 0 | 0 | 20000 | 20000 | 0 | 0 | 0 |
| mode | C35 R8: blocked vs interleaved | 0 | 0 | 20000 | 20000 | 0 | 0 | 0 |
| mode | C55 R2: blocked vs interleaved | 5 | 5 | 5260 | 4620 | 640 | -2260.5 | 3180 |
| mode | C55 R4: blocked vs interleaved | 5 | 5 | 4840 | 5200 | -360 | -2100 | 1480 |
| mode | C55 R8: blocked vs interleaved | 5 | 5 | 4060 | 4560 | -500 | -2080 | 960 |
| mode | C85 R2: blocked vs interleaved | 5 | 5 | 1780 | 1920 | -140 | -400 | 160 |
| mode | C85 R4: blocked vs interleaved | 5 | 5 | 1800 | 1820 | -20 | -280 | 280 |
| mode | C85 R8: blocked vs interleaved | 5 | 5 | 1760 | 1800 | -40 | -320 | 280 |
| mode | C25 R8: blocked vs interleaved | 0 | 0 | 20000 | 20000 | 0 | 0 | 0 |

### 2.3 Fisher exact tests (low-event cells)

At 35% and 25% coverage almost all runs are censored, so time-based inference is not meaningful; the table below reports the number of runs that grok per condition with two-sided Fisher exact tests and Clopper-Pearson 95% CIs. **These cells have too few events for time-based inference; only the event counts are interpretable.**

| coverage | contrast | k1 | n1 | k2 | n2 | p_fisher | cp1_lo | cp1_hi | cp2_lo | cp2_hi |
|---|---|---|---|---|---|---|---|---|---|---|
| 35 | C35 R1 vs C35 R2 blocked | 2 | 5 | 1 | 5 | 1 | 0.0527 | 0.8534 | 0.0051 | 0.7164 |
| 35 | C35 R1 vs C35 R2 interleaved | 2 | 5 | 0 | 5 | 0.44444 | 0.0527 | 0.8534 | 0 | 0.5218 |
| 35 | C35 R2 blocked vs C35 R2 interleaved | 1 | 5 | 0 | 5 | 1 | 0.0051 | 0.7164 | 0 | 0.5218 |
| 35 | C35 R1 vs C35 R4 blocked | 2 | 5 | 0 | 5 | 0.44444 | 0.0527 | 0.8534 | 0 | 0.5218 |
| 35 | C35 R1 vs C35 R4 interleaved | 2 | 5 | 0 | 5 | 0.44444 | 0.0527 | 0.8534 | 0 | 0.5218 |
| 35 | C35 R4 blocked vs C35 R4 interleaved | 0 | 5 | 0 | 5 | 1 | 0 | 0.5218 | 0 | 0.5218 |
| 35 | C35 R1 vs C35 R8 blocked | 2 | 5 | 0 | 5 | 0.44444 | 0.0527 | 0.8534 | 0 | 0.5218 |
| 35 | C35 R1 vs C35 R8 interleaved | 2 | 5 | 0 | 5 | 0.44444 | 0.0527 | 0.8534 | 0 | 0.5218 |
| 35 | C35 R8 blocked vs C35 R8 interleaved | 0 | 5 | 0 | 5 | 1 | 0 | 0.5218 | 0 | 0.5218 |
| 25 | C25 R1 vs C25 R4 blocked | 0 | 5 | 0 | 5 | 1 | 0 | 0.5218 | 0 | 0.5218 |
| 25 | C25 R1 vs C25 R8 blocked | 0 | 5 | 0 | 5 | 1 | 0 | 0.5218 | 0 | 0.5218 |
| 25 | C25 R8 blocked vs C25 R8 interleaved | 0 | 5 | 0 | 5 | 1 | 0 | 0.5218 | 0 | 0.5218 |

### 2.4 Stratified Cox model (pooled blocked repetition vs R = 1)

Cox partial likelihood with Breslow tie handling, single binary covariate (z = 1: blocked repetition R in {2,4,8}, n = 45; z = 0: R = 1, n = 15), coverage (35/55/85) as strata, 43 events. 
**beta = -0.040, SE = 0.359, HR = 0.961, 95% CI [0.475, 1.94]. Convergence: YES -- converged after 4 Newton steps.** 
Caveats: the 35% stratum contributes only 3 of the 43 events, so the common-hazard-ratio assumption is fragile across strata, and the HR and its wide CI should not be over-read; the implementation detects monotone-likelihood divergence (which would occur if events separated perfectly by covariate within a stratum) and reports it instead of returning a finite estimate. No Cox model was fitted in cells with zero events.

## 3. Equivalence testing for the repetition null (TOST)

Scale: log10 GrokTime, so the margin is a ratio. Applies to cells with no censoring (coverage 55 and 85; verified). Two versions are reported and compared: (i) permutation TOST on the difference in mean log10 GrokTime (252-assignment enumeration, shifted-null one-sided tests), and (ii) Welch t-based TOST.

> **THE MARGIN MUST BE JUSTIFIED ON SUBSTANTIVE GROUNDS BEFORE LOOKING AT THE RESULT, AND THAT JUSTIFICATION MUST BE WRITTEN INTO THE PAPER.** The tables below report every requested margin rather than choosing one; `--margins` is a user setting. Equivalence at alpha = 0.05 requires max(p1, p2) < 0.05 AND a margin you can defend.

| contrast | margin_fraction | margin_ratio | mean_log10_ratio | mean_ratio | perm_ci90_lo_ratio | perm_ci90_hi_ratio | perm_pmax | welch_ci90_lo_ratio | welch_ci90_hi_ratio | welch_pmax |
|---|---|---|---|---|---|---|---|---|---|---|
| C55 blocked: R1 vs R2 | 0.1 | 1.1 | -0.0758 | 0.84 | 0.581 | 1.214 | 0.62698 | 0.541 | 1.303 | 0.62743 |
| C55 blocked: R1 vs R2 | 0.25 | 1.25 | -0.0758 | 0.84 | 0.581 | 1.214 | 0.42857 | 0.541 | 1.303 | 0.42104 |
| C55 blocked: R1 vs R2 | 0.5 | 1.5 | -0.0758 | 0.84 | 0.581 | 1.214 | 0.16667 | 0.541 | 1.303 | 0.1782 |
| C55 blocked: R1 vs R4 | 0.1 | 1.1 | -0.053 | 0.885 | 0.649 | 1.208 | 0.55556 | 0.611 | 1.282 | 0.55188 |
| C55 blocked: R1 vs R4 | 0.25 | 1.25 | -0.053 | 0.885 | 0.649 | 1.208 | 0.31746 | 0.611 | 1.282 | 0.31214 |
| C55 blocked: R1 vs R4 | 0.5 | 1.5 | -0.053 | 0.885 | 0.649 | 1.208 | 0.10317 | 0.611 | 1.282 | 0.09603 |
| C55 blocked: R1 vs R8 | 0.1 | 1.1 | 0.0228 | 1.054 | 0.773 | 1.437 | 0.4127 | 0.73 | 1.52 | 0.41614 |
| C55 blocked: R1 vs R8 | 0.25 | 1.25 | 0.0228 | 1.054 | 0.773 | 1.437 | 0.21032 | 0.73 | 1.52 | 0.20494 |
| C55 blocked: R1 vs R8 | 0.5 | 1.5 | 0.0228 | 1.054 | 0.773 | 1.437 | 0.0754 | 0.73 | 1.52 | 0.05549 |
| C55 interleaved: R1 vs R2 | 0.1 | 1.1 | -0.0017 | 0.996 | 0.664 | 1.494 | 0.36905 | 0.609 | 1.628 | 0.36805 |
| C55 interleaved: R1 vs R2 | 0.25 | 1.25 | -0.0017 | 0.996 | 0.664 | 1.494 | 0.23016 | 0.609 | 1.628 | 0.21376 |
| C55 interleaved: R1 vs R2 | 0.5 | 1.5 | -0.0017 | 0.996 | 0.664 | 1.494 | 0.0873 | 0.609 | 1.628 | 0.08299 |
| C55 interleaved: R1 vs R4 | 0.1 | 1.1 | -0.0792 | 0.833 | 0.583 | 1.192 | 0.66667 | 0.559 | 1.243 | 0.65189 |
| C55 interleaved: R1 vs R4 | 0.25 | 1.25 | -0.0792 | 0.833 | 0.583 | 1.192 | 0.42857 | 0.559 | 1.243 | 0.42703 |
| C55 interleaved: R1 vs R4 | 0.5 | 1.5 | -0.0792 | 0.833 | 0.583 | 1.192 | 0.13492 | 0.559 | 1.243 | 0.16475 |
| C55 interleaved: R1 vs R8 | 0.1 | 1.1 | -0.0249 | 0.944 | 0.682 | 1.308 | 0.40873 | 0.647 | 1.379 | 0.42807 |
| C55 interleaved: R1 vs R8 | 0.25 | 1.25 | -0.0249 | 0.944 | 0.682 | 1.308 | 0.21825 | 0.647 | 1.379 | 0.21917 |
| C55 interleaved: R1 vs R8 | 0.5 | 1.5 | -0.0249 | 0.944 | 0.682 | 1.308 | 0.04762 | 0.647 | 1.379 | 0.06284 |
| C55 R2: blocked vs interleaved | 0.1 | 1.1 | 0.0741 | 1.186 | 0.735 | 1.914 | 0.59127 | 0.708 | 1.987 | 0.60387 |
| C55 R2: blocked vs interleaved | 0.25 | 1.25 | 0.0741 | 1.186 | 0.735 | 1.914 | 0.43651 | 0.708 | 1.987 | 0.4272 |
| C55 R2: blocked vs interleaved | 0.5 | 1.5 | 0.0741 | 1.186 | 0.735 | 1.914 | 0.23413 | 0.708 | 1.987 | 0.2106 |
| C55 R4: blocked vs interleaved | 0.1 | 1.1 | -0.0262 | 0.941 | 0.693 | 1.279 | 0.42857 | 0.653 | 1.357 | 0.43135 |
| C55 R4: blocked vs interleaved | 0.25 | 1.25 | -0.0262 | 0.941 | 0.693 | 1.279 | 0.21825 | 0.653 | 1.357 | 0.21535 |
| C55 R4: blocked vs interleaved | 0.5 | 1.5 | -0.0262 | 0.941 | 0.693 | 1.279 | 0.05952 | 0.653 | 1.357 | 0.05867 |
| C55 R8: blocked vs interleaved | 0.1 | 1.1 | -0.0476 | 0.896 | 0.667 | 1.203 | 0.54365 | 0.641 | 1.254 | 0.53067 |
| C55 R8: blocked vs interleaved | 0.25 | 1.25 | -0.0476 | 0.896 | 0.667 | 1.203 | 0.25397 | 0.641 | 1.254 | 0.27343 |
| C55 R8: blocked vs interleaved | 0.5 | 1.5 | -0.0476 | 0.896 | 0.667 | 1.203 | 0.06746 | 0.641 | 1.254 | 0.06997 |
| C85 blocked: R1 vs R2 | 0.1 | 1.1 | 0.0314 | 1.075 | 0.886 | 1.304 | 0.4246 | 0.871 | 1.327 | 0.42156 |
| C85 blocked: R1 vs R2 | 0.25 | 1.25 | 0.0314 | 1.075 | 0.886 | 1.304 | 0.10714 | 0.871 | 1.327 | 0.10949 |
| C85 blocked: R1 vs R2 | 0.5 | 1.5 | 0.0314 | 1.075 | 0.886 | 1.304 | 0.0119 | 0.871 | 1.327 | 0.00944 |
| C85 blocked: R1 vs R4 | 0.1 | 1.1 | 0.0258 | 1.061 | 0.883 | 1.274 | 0.37302 | 0.865 | 1.302 | 0.37507 |
| C85 blocked: R1 vs R4 | 0.25 | 1.25 | 0.0258 | 1.061 | 0.883 | 1.274 | 0.08333 | 0.865 | 1.302 | 0.08672 |
| C85 blocked: R1 vs R4 | 0.5 | 1.5 | 0.0258 | 1.061 | 0.883 | 1.274 | 0.0119 | 0.865 | 1.302 | 0.00704 |
| C85 blocked: R1 vs R8 | 0.1 | 1.1 | 0.0352 | 1.084 | 0.902 | 1.304 | 0.45635 | 0.886 | 1.328 | 0.44933 |
| C85 blocked: R1 vs R8 | 0.25 | 1.25 | 0.0352 | 1.084 | 0.902 | 1.304 | 0.11111 | 0.886 | 1.328 | 0.11348 |
| C85 blocked: R1 vs R8 | 0.5 | 1.5 | 0.0352 | 1.084 | 0.902 | 1.304 | 0.0119 | 0.886 | 1.328 | 0.00914 |
| C85 interleaved: R1 vs R2 | 0.1 | 1.1 | -0.005 | 0.989 | 0.858 | 1.139 | 0.19048 | 0.821 | 1.191 | 0.20607 |
| C85 interleaved: R1 vs R2 | 0.25 | 1.25 | -0.005 | 0.989 | 0.858 | 1.139 | 0.02778 | 0.821 | 1.191 | 0.0347 |
| C85 interleaved: R1 vs R2 | 0.5 | 1.5 | -0.005 | 0.989 | 0.858 | 1.139 | 0.00397 | 0.821 | 1.191 | 0.00335 |
| C85 interleaved: R1 vs R4 | 0.1 | 1.1 | 0.0187 | 1.044 | 0.896 | 1.217 | 0.30556 | 0.864 | 1.261 | 0.30587 |
| C85 interleaved: R1 vs R4 | 0.25 | 1.25 | 0.0187 | 1.044 | 0.896 | 1.217 | 0.05556 | 0.864 | 1.261 | 0.05671 |
| C85 interleaved: R1 vs R4 | 0.5 | 1.5 | 0.0187 | 1.044 | 0.896 | 1.217 | 0.00794 | 0.864 | 1.261 | 0.00473 |
| C85 interleaved: R1 vs R8 | 0.1 | 1.1 | 0.0256 | 1.061 | 0.892 | 1.261 | 0.37698 | 0.863 | 1.304 | 0.37532 |
| C85 interleaved: R1 vs R8 | 0.25 | 1.25 | 0.0256 | 1.061 | 0.892 | 1.261 | 0.09524 | 0.863 | 1.304 | 0.08814 |
| C85 interleaved: R1 vs R8 | 0.5 | 1.5 | 0.0256 | 1.061 | 0.892 | 1.261 | 0.0119 | 0.863 | 1.304 | 0.00725 |
| C85 R2: blocked vs interleaved | 0.1 | 1.1 | -0.0363 | 0.92 | 0.8 | 1.057 | 0.43651 | 0.782 | 1.081 | 0.44682 |
| C85 R2: blocked vs interleaved | 0.25 | 1.25 | -0.0363 | 0.92 | 0.8 | 1.057 | 0.05159 | 0.782 | 1.081 | 0.07273 |
| C85 R2: blocked vs interleaved | 0.5 | 1.5 | -0.0363 | 0.92 | 0.8 | 1.057 | 0.00397 | 0.782 | 1.081 | 0.00401 |
| C85 R4: blocked vs interleaved | 0.1 | 1.1 | -0.007 | 0.984 | 0.858 | 1.129 | 0.19841 | 0.843 | 1.149 | 0.18287 |
| C85 R4: blocked vs interleaved | 0.25 | 1.25 | -0.007 | 0.984 | 0.858 | 1.129 | 0.01587 | 0.843 | 1.149 | 0.01944 |
| C85 R4: blocked vs interleaved | 0.5 | 1.5 | -0.007 | 0.984 | 0.858 | 1.129 | 0.00397 | 0.843 | 1.149 | 0.00099 |
| C85 R8: blocked vs interleaved | 0.1 | 1.1 | -0.0096 | 0.978 | 0.845 | 1.132 | 0.23413 | 0.819 | 1.168 | 0.23202 |
| C85 R8: blocked vs interleaved | 0.25 | 1.25 | -0.0096 | 0.978 | 0.845 | 1.132 | 0.03571 | 0.819 | 1.168 | 0.03391 |
| C85 R8: blocked vs interleaved | 0.5 | 1.5 | -0.0096 | 0.978 | 0.845 | 1.132 | 0.00794 | 0.819 | 1.168 | 0.00192 |

Smallest margin (ratio) at which equivalence would be declared (grid 1.01-3.0):

| contrast | smallest_margin_ratio_perm | smallest_margin_ratio_welch |
|---|---|---|
| C55 blocked: R1 vs R2 | 1.8721 | 1.8549 |
| C55 blocked: R1 vs R4 | 1.6007 | 1.6456 |
| C55 blocked: R1 vs R8 | 1.5571 | 1.5287 |
| C55 interleaved: R1 vs R2 | 1.6305 | 1.6456 |
| C55 interleaved: R1 vs R4 | 1.821 | 1.8044 |
| C55 interleaved: R1 vs R8 | 1.5008 | 1.5571 |
| C55 R2: blocked vs interleaved | 2.0717 | 1.9967 |
| C55 R4: blocked vs interleaved | 1.5571 | 1.5428 |
| C55 R8: blocked vs interleaved | 1.5571 | 1.5715 |
| C85 blocked: R1 vs R2 | 1.3438 | 1.3314 |
| C85 blocked: R1 vs R4 | 1.3192 | 1.3071 |
| C85 blocked: R1 vs R8 | 1.3438 | 1.3314 |
| C85 interleaved: R1 vs R2 | 1.2143 | 1.2255 |
| C85 interleaved: R1 vs R4 | 1.2715 | 1.2715 |
| C85 interleaved: R1 vs R8 | 1.2952 | 1.3071 |
| C85 R2: blocked vs interleaved | 1.2599 | 1.2833 |
| C85 R4: blocked vs interleaved | 1.1812 | 1.1921 |
| C85 R8: blocked vs interleaved | 1.2255 | 1.2255 |

### 3.1 Simulation-based power / minimum detectable effect (5 vs 5)

Based on the observed pooled within-cell SD of log10 GrokTime (0.1164; cells at coverage 55 and 85). **This is NOT a pre-study power analysis** -- it conditions on the observed variance and on n = 5 per group. The two-sided permutation test of the mean difference has 80% power only for true ratios of about 1.995x or larger.

| margin_fraction | margin_ratio | power_at_true_ratio_1 | largest_true_ratio_with_power_ge_0p8 |
|---|---|---|---|
| 0.1 | 1.1 | 0 |  |
| 0.25 | 1.25 | 0.021 |  |
| 0.5 | 1.5 | 0.4145 |  |

Full power grid: `tost_power.csv`.

## 4. Secondary outcomes (exploratory unless stated otherwise)

### 4.1 MemTime (exploratory; families M1/M2)

| contrast | n1 | n2 | U1 | p_exact | p_scipy_asymptotic | rank_biserial | median_diff | hodges_lehmann | boot_ci_lo | boot_ci_hi | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C35 blocked: R1 vs R4 (MemTime) | 5 | 5 | 2.5 | 0.04762 | 0.01996 | 0.8 | -100 | -100 | -100 | 0 | 0.04764 |
| C35 blocked: R1 vs R8 (MemTime) | 5 | 5 | 0 | 0.00794 | 0.00398 | 1 | -100 | -100 | -100 | -100 | 0.04764 |
| C55 blocked: R1 vs R4 (MemTime) | 5 | 5 | 0 | 0.00794 | 0.00398 | 1 | -100 | -100 | -100 | -100 | 0.04764 |
| C55 blocked: R1 vs R8 (MemTime) | 5 | 5 | 0 | 0.00794 | 0.00398 | 1 | -200 | -200 | -200 | -200 | 0.04764 |
| C85 blocked: R1 vs R4 (MemTime) | 5 | 5 | 0 | 0.00794 | 0.00398 | 1 | -100 | -100 | -100 | -100 | 0.04764 |
| C85 blocked: R1 vs R8 (MemTime) | 5 | 5 | 0 | 0.00794 | 0.00398 | 1 | -300 | -300 | -300 | -300 | 0.04764 |

Jonckheere-Terpstra trend across R in {1,2,4,8} (blocked), one-sided (increasing), Holm within family M2:

| contrast | J | p_one_sided | p_holm |
|---|---|---|---|
| C35 blocked: trend across R in (1,2,4,8) | 122.5 | 0.0001 | 0.0003 |
| C55 blocked: trend across R in (1,2,4,8) | 137.5 | 0.0001 | 0.0003 |
| C85 blocked: trend across R in (1,2,4,8) | 137.5 | 0.0001 | 0.0003 |

### 4.2 Sub-critical final test accuracy at 25% coverage (family S1)

1 correct answer = 0.252 percentage points (n_test = 397); median correct counts are shown so the granularity is visible.

| contrast | n_correct_1 | n_correct_2 | U1 | p_exact | rank_biserial | median_diff | boot_ci_lo | boot_ci_hi | p_holm |
|---|---|---|---|---|---|---|---|---|---|
| C25 blocked: R1 vs R4 (final acc) | 53/397 | 86/397 | 0 | 0.00794 | 1 | -0.0831 | -0.1134 | -0.0453 | 0.02382 |
| C25 blocked: R1 vs R8 (final acc) | 53/397 | 84/397 | 0 | 0.00794 | 1 | -0.0781 | -0.1108 | -0.0378 | 0.02382 |
| C25 R8: blocked vs interleaved (final acc) | 84/397 | 69/397 | 20.5 | 0.11905 | -0.64 | 0.0378 | -0.0327 | 0.0705 | 0.11905 |

### 4.3 Final L2 norm at 25% coverage (family S2; unplanned/exploratory)

| contrast | U1 | p_exact | rank_biserial | median_diff | boot_ci_lo | boot_ci_hi | p_holm |
|---|---|---|---|---|---|---|---|
| C25 blocked: R1 vs R4 (final L2 norm) | 1 | 0.01587 | 0.92 | -1.9108 | -3.6246 | -0.3197 | 0.03174 |
| C25 blocked: R1 vs R8 (final L2 norm) | 0 | 0.00794 | 1 | -3.4921 | -6.4915 | -1.7569 | 0.02382 |
| C25 R8: blocked vs interleaved (final L2 norm) | 23 | 0.03175 | -0.84 | 2.6997 | 0.396 | 5.9123 | 0.03175 |

### 4.4 Blocked vs interleaved sub-critical final accuracy at 35% coverage (family S3; exploratory; n_test = 344)

| contrast | n_correct_1 | n_correct_2 | p_exact | rank_biserial | median_diff | boot_ci_lo | boot_ci_hi | p_holm |
|---|---|---|---|---|---|---|---|---|
| C35 R2: blocked vs interleaved (final acc) | 142/344 | 205/344 | 0.84127 | 0.12 | -0.1831 | -0.4826 | 0.3576 | 0.92064 |
| C35 R4: blocked vs interleaved (final acc) | 124/344 | 192/344 | 0.46032 | 0.32 | -0.1977 | -0.4506 | 0.064 | 0.92064 |
| C35 R8: blocked vs interleaved (final acc) | 153/344 | 261/344 | 0.22222 | 0.52 | -0.314 | -0.4535 | 0.1192 | 0.66666 |

### 4.5 Weight norm at the matched step 1,000, coverage 55 (family W1)

Equivalence-style summary: difference of medians with a 90% percentile-bootstrap CI, replacing 'statistically indistinguishable'.

| contrast | median_1 | median_2 | median_diff | ci90_lo | ci90_hi | mean_diff |
|---|---|---|---|---|---|---|
| C55 blocked: R1 vs R2 (wnorm@1000) | 23.953 | 23.354 | 0.531 | 0.146 | 1.017 | 0.557 |
| C55 blocked: R1 vs R4 (wnorm@1000) | 23.953 | 23.506 | 0.634 | -0.099 | 1.121 | 0.448 |
| C55 blocked: R1 vs R8 (wnorm@1000) | 23.953 | 23.868 | 0.206 | -0.394 | 0.47 | 0.011 |
| C55 R2: blocked vs interleaved (wnorm@1000) | 23.354 | 23.62 | -0.178 | -0.645 | 0.207 | -0.197 |
| C55 R4: blocked vs interleaved (wnorm@1000) | 23.506 | 23.392 | -0.048 | -0.341 | 0.633 | 0.06 |
| C55 R8: blocked vs interleaved (wnorm@1000) | 23.868 | 23.502 | 0.656 | -0.086 | 0.978 | 0.441 |

### 4.6 Spearman correlation, final L2 norm vs GrokTime (grokked runs)

| stratum | n | rho | p_perm | p_scipy_asymptotic |
|---|---|---|---|---|
| all grokked runs | 83 | 0.0648 | 0.55244 | 0.56034 |
| coverage 25% | 0 |  |  |  |
| coverage 35% | 3 | -1 | 0.33487 | 0 |
| coverage 45% | 5 | -0.9 | 0.08469 | 0.03739 |
| coverage 55% | 35 | 0.2906 | 0.09329 | 0.09035 |
| coverage 70% | 5 | 0.5 | 0.45095 | 0.391 |
| coverage 85% | 35 | -0.6009 | 0.0002 | 0.00014 |

**Caveat**: grokked runs stop at their GrokTime, so both variables depend on the stopping step; the correlation mixes stopping times and is not an independent-variables summary. Censored runs (which train the full budget) are excluded.

## (c) Manuscript sentences

Suggested wording for Methods and Results. Every number comes from the tables above; placeholders in [BRACKETS] are decisions the author must make. These sentences state what each test shows, not what it cannot.

### Methods (proposed wording)

> Two-sample comparisons use an exact permutation test of the Mann-Whitney U statistic with midranks (all 252 label assignments enumerated; two-sided p = proportion with |U - n1*n2/2| >= observed), with scipy's asymptotic tie-corrected p reported alongside for transparency. Multiplicity was controlled with Holm correction within declared families; the families differ from the internal plan (deviation-log item iii) and are therefore not pre-specified. Runs censored at the 20,000-step budget enter rank-based GrokTime comparisons at the budget (worst rank); Kaplan-Meier estimates, permutation log-rank tests, and restricted mean survival time up to 20,000 steps treat censoring natively. Cells with too few events are summarized by the number of runs that grok, with Fisher exact tests and Clopper-Pearson intervals. Equivalence of GrokTime under repetition at 55% and 85% coverage was assessed with two one-sided tests (TOST) on log10 GrokTime with a margin of [CHOOSE MARGIN]; [JUSTIFY MARGIN]. All resampling used numpy default_rng with master seed 20260922 and documented per-analysis offsets.

### Results (proposed wording)

> Median GrokTime fell from 8,400 steps at 45% coverage to 1,800 at 85% (exact permutation Mann-Whitney p = 0.00794, rank-biserial r = 1.0, Holm-adjusted p = 0.01588); the permutation log-rank test gives p = 0.00794. At 25% coverage all five R = 1 runs were censored at budget; with censored runs at the worst rank the exact p = 0.00794 (Holm 0.01588), and the log-rank permutation p = 0.00794.

> At matched per-example dose, none of the four blocked-repetition contrasts on GrokTime showed a detectable difference (exact p = 0.55556-0.79365, all Holm-adjusted p = 1.0), and every bootstrap CI of the median difference included zero. The censoring-aware RMST contrasts were +280 steps at 55% coverage (95% CI [-1260, 1700]) and +160 steps at 85% coverage (95% CI [-200, 520]). TOST at the [CHOOSE MARGIN] margin: see the equivalence table; at a +/-25% margin, [STATE WHICH CONTRASTS REACH EQUIVALENCE FROM tost.csv]. These are bounded nulls, not demonstrations of exact equivalence; with n = 5 per group the smallest margin at which equivalence is declarable is itself wide (see tost_smallest_margin.csv).

> The extreme contrast (25%, R = 8, blocked vs 55%, R = 1, final test accuracy) differs by -75.5 percentage points (exact p = 0.00794, rank-biserial r = 1.0); it varies coverage and repetition jointly and is a coverage contrast, not evidence that repetition rescues low coverage.

> Repetition delayed memorization: median MemTime rose from 100 to 300 steps at 55% coverage between R = 1 and R = 8 (exact p = 0.00794, Holm-adjusted p = 0.04764), with the same direction at 35% and 85% coverage and a positive Jonckheere-Terpstra trend at every coverage (all exploratory).

> Below the coverage boundary, repetition shifted sub-critical final accuracy from a median 53/397 to 86/397 held-out problems between R = 1 and R = 4 (blocked; exact p = 0.00794, Holm 0.02382) and to 84/397 at R = 8 (exact p = 0.00794); blocked and interleaved R = 8 did not differ detectably (exact p = 0.11905). Final weight norms at 25% coverage rose with repetition (median 17.5 at R = 1 vs 19.4 at R = 4, exact p = 0.01587; 21.0 at R = 8, exact p = 0.00794); these contrasts were unplanned and exploratory. Among the 83 runs that grokked, final norm and GrokTime were uncorrelated (Spearman rho = 0.0648, permutation p = 0.55244), noting that both variables depend on the stopping step.

## (d) Things that contradict the current manuscript

8 MISMATCH(es) and 9 values produced by a bug in the archived analysis code (all bootstrap CIs of median differences were computed by resampling only ONE group, which makes them too narrow; every draft CI in the list below is reproduced exactly by the archived algorithm, confirming the diagnosis). Nothing was overwritten silently.

| item | manuscript_value | recomputed_value | status | explanation |
|---|---|---|---|---|
| 85% vs 45% GrokTime MW p (draft: 'exact') | 0.008 | 0.00794 | CONSISTENT | exact 2/252 = 0.00794 rounds to the draft's 0.008; scipy asymptotic gives 0.01219, so the draft value can only be the exact one |
| 85% vs 25% GrokTime MW p (draft: 0.0075) | 0.0075 | 0.00794 | MISMATCH | 0.0075 is below the exact two-sided minimum 2/252 = 0.00794 for 5 vs 5; scipy's asymptotic tie-corrected method reproduces 0.00749, so the draft value is asymptotic but was labelled exact; with censored runs at the budget the exact permutation p is 0.00794 |
| Family 1 Holm-adjusted p | 0.015 | 0.01588 | MISMATCH | Holm over the exact p-values gives 0.01587; the draft's 0.015 came from Holm over the smaller asymptotic p (2 x 0.00749) |
| Family 3 MW p (25%/R8/blocked vs 55%/R1, final acc) | 0.012 | 0.00794 | MISMATCH | rank-biserial = -1 (perfect separation) makes the exact two-sided p 2/252 = 0.00794; scipy asymptotic reproduces 0.01167, matching the draft's 0.12 (asymptotic, mislabelled exact) |
| Family 3 Holm-adjusted p | 0.021 | 0.00794 | MISMATCH | with the single declared contrast the Holm p equals the raw exact p; the draft's 0.021 corresponds to Holm over TWO contrasts (the archived stats.json also tested 25%/R8/blocked vs 85%/R1) |
| Family 2 MW p: C55 R1 vs C55 R4 (blocked) | 0.68 | 0.65079 | MISMATCH | scipy asymptotic reproduces the draft value (0.67517); exact permutation p differs |
| Family 2 MW p: C55 R1 vs C55 R8 (blocked) | 0.83 | 0.79365 | MISMATCH | scipy asymptotic reproduces the draft value (0.83404); exact permutation p differs |
| Family 2 MW p: C85 R1 vs C85 R4 (blocked) | 0.67 | 0.67460 | MISMATCH | scipy asymptotic reproduces the draft value (0.67329); exact permutation p differs |
| Family 2 MW p: C85 R1 vs C85 R8 (blocked) | 0.53 | 0.55556 | MISMATCH | scipy asymptotic reproduces the draft value (0.52581); exact permutation p differs |
| F1 85% vs 45% median-difference bootstrap CI (draft [-6,900, -6,000]) | [-6900, -6000] | [-11600, -4000] | ARCHIVED-BUG | the archived code (scripts/analyze.py, mw_exact) computed median(resample(b)) - median(a_observed): only ONE group was resampled, so the CI is too narrow; reproducing that code gives (-6900.0, -6000.0) = the draft value; the correct two-group within-group percentile bootstrap gives the wider recomputed value |
| Family 2 median-difference bootstrap CI: C55 R1 vs C55 R4 | [-1200, 2600] (draft; R_repetition - R1) | [-2600, 2000] (this pipeline; R1 - R_repetition) | ARCHIVED-BUG | reproducing the archived one-group bootstrap gives (-1200.0, 2600.0) = the draft value; the correct two-group percentile bootstrap is wider; note also the opposite sign convention |
| Family 2 median-difference bootstrap CI: C55 R1 vs C55 R8 | [-1600, 1500] (draft; R_repetition - R1) | [-1500, 2600] (this pipeline; R1 - R_repetition) | ARCHIVED-BUG | reproducing the archived one-group bootstrap gives (-1600.0, 1500.0) = the draft value; the correct two-group percentile bootstrap is wider; note also the opposite sign convention |
| Family 2 median-difference bootstrap CI: C85 R1 vs C85 R4 | [-200, 500] (draft; R_repetition - R1) | [-500, 700] (this pipeline; R1 - R_repetition) | ARCHIVED-BUG | reproducing the archived one-group bootstrap gives (-200.0, 500.0) = the draft value; the correct two-group percentile bootstrap is wider; note also the opposite sign convention |
| Family 2 median-difference bootstrap CI: C85 R1 vs C85 R8 | [-300, 400] (draft; R_repetition - R1) | [-400, 700] (this pipeline; R1 - R_repetition) | ARCHIVED-BUG | reproducing the archived one-group bootstrap gives (-300.0, 400.0) = the draft value; the correct two-group percentile bootstrap is wider; note also the opposite sign convention |
| F3 median-difference bootstrap CI (draft [-77.2, -72.2] pp) | [-77.24, -72.21] pp | [-78.8, -72.2] pp | ARCHIVED-BUG | same one-group-bootstrap cause: reproducing the archived code gives (-77.2, -72.2) = the draft value |
| Manuscript sec. 4.2 bound statement: C85 R8 interval 'excludes shifts larger than roughly 17% earlier or 22% later than the 1,800-step median' | 17% earlier / 22% later | [-400, 700] steps around 1,800 = 22% earlier / 39% later | ARCHIVED-BUG | the bound was derived from the too-narrow archived CI [-300, +400]; with the correct CI the excluded shifts are wider |
| Manuscript sec. 4.2 bound statement: C55 interval 'excludes shifts larger than roughly one third of the 4,700-step median' | about one third | [-1500, 2600] steps around 4,700 = 32% earlier / 55% later | ARCHIVED-BUG | the bound was derived from the too-narrow archived CI [-1,600, +1,500] |
| Mode-contrast CI quoted in draft (C55 R2, +700 steps, [-400, 4,300]) | [-400, 4300] | [-5300, 4300] | ARCHIVED-BUG | reproducing the archived one-group bootstrap gives (-400.0, 4300.0) = the draft value; correct two-group percentile bootstrap shown |
| Family 2: 'every confidence interval includes zero' | True | True | CONSISTENT | holds for the recomputed CIs as well |
| Family 2: 'point estimates of at most 900 steps' | True | True | CONSISTENT | max /median difference/ = 900 steps |
| Family 2 median-difference sign convention | R_repetition - R1 | R1 - R_repetition (median of first-named minus second-named) | SIGN CONVENTION | the draft reports e.g. -300 steps for 'R=1 versus R=4' at 55% coverage, computed as median(R4) - median(R1) = 4400 - 4700; this pipeline reports median(R1) - median(R4) = +300; magnitudes agree, signs are opposite |
| C25 final L2 norm MW p: R1 vs R4 (blocked) | 0.016 | 0.01587 | CONSISTENT | draft values match the exact permutation p rounded to 3 decimals (2/252 = 0.00794 -> 0.008; 4/252 = 0.01587 -> 0.016) |
| C25 final L2 norm MW p: R1 vs R8 (blocked) | 0.008 | 0.00794 | CONSISTENT | draft values match the exact permutation p rounded to 3 decimals (2/252 = 0.00794 -> 0.008; 4/252 = 0.01587 -> 0.016) |
| Spearman rho, final norm vs GrokTime (83 grokked runs) | 0.065 | 0.0648 | CONSISTENT | permutation p = 0.5524 vs draft's 0.56 (scipy's asymptotic t approximation; the permutation p is the declared one) |
| Mode contrasts GrokTime: draft claims 'all p > 0.2' | True | min exact p = 0.2381 | CONSISTENT | recomputed with the exact permutation Mann-Whitney (censored runs at the 20,000 budget) |
| C35 median MemTime R1 -> R8 (blocked) | 100 -> 200 | 100 -> 200 | CONSISTENT |  |
| C55 median MemTime R1 -> R8 (blocked) | 100 -> 300 | 100 -> 300 | CONSISTENT |  |
| C85 median MemTime R1 -> R8 (blocked) | 200 -> 500 | 200 -> 500 | CONSISTENT |  |
| C25 median final test accuracy (R1) | 13.4% | 13.4% | CONSISTENT |  |
| C25 median final test accuracy (R4b) | 21.7% | 21.7% | CONSISTENT |  |
| C25 median final test accuracy (R8b) | 21.2% | 21.2% | CONSISTENT |  |
| C25 median final test accuracy (R8i) | 17.4% | 17.4% | CONSISTENT |  |
| C25 median final L2 norm (R1) | 17.5 | 17.473 | CONSISTENT | draft value is the recomputed median rounded to one decimal |
| C25 median final L2 norm (R4b) | 19.4 | 19.383 | CONSISTENT | draft value is the recomputed median rounded to one decimal |
| C25 median final L2 norm (R8b) | 21.0 | 20.965 | CONSISTENT | draft value is the recomputed median rounded to one decimal |
| C25 median final L2 norm (R8i) | 18.3 | 18.265 | CONSISTENT | draft value is the recomputed median rounded to one decimal |
| wnorm@1000 medians '23.1-24.3 in every cell' (C35/55/85, all R, both modes) | 23.1-24.3 | 23.1-24.3 | CONSISTENT | 21 cells |
| MemTime 'never exceeds 500 steps (median 200)' | max <= 500, median 200 | max = 500, median 200 | CONSISTENT | maximum is attained (85%/R8/blocked) |
| archived memtime test p (C55 R1 vs R8) | 0.00398 | 0.00794 (exact) | SUPERSEDED | 0.00398 is scipy's asymptotic tie-corrected p with within-group ties; it is below the exact minimum 2/252 = 0.00794; the exact permutation p is 0.00794 (see secondary_tests.csv) |
| archived memtime test p (C35 R1 vs R8) | 0.00398 | 0.00794 (exact) | SUPERSEDED | 0.00398 is scipy's asymptotic tie-corrected p with within-group ties; it is below the exact minimum 2/252 = 0.00794; the exact permutation p is 0.00794 (see secondary_tests.csv) |
| archived memtime test p (C85 R1 vs R8) | 0.00398 | 0.00794 (exact) | SUPERSEDED | 0.00398 is scipy's asymptotic tie-corrected p with within-group ties; it is below the exact minimum 2/252 = 0.00794; the exact permutation p is 0.00794 (see secondary_tests.csv) |

## Limitations of these analyses

- n = 5 seeds per condition; every interval and test is coarse, and the exact two-sided permutation p cannot fall below 2/252 = 0.00794 for 5 vs 5 contrasts.
- GrokTime and MemTime are discrete (multiples of 100 steps) and heavily tied within cells; medians of five such values, their bootstrap CIs, and rank tests all inherit this coarseness.
- The TOST margin is a user choice ([CHOOSE MARGIN]); no margin was pre-justified, so equivalence statements are conditional on a post-hoc margin that must be defended in print.
- Multiplicity: Holm was applied within each declared family, but the families themselves were chosen post hoc (deviation-log item iii), and several families (M1, M2, S1, S2, S3, W1) are exploratory; the family-wise error rate ACROSS families is not controlled.
- The sub-critical accuracy, weight-norm, and correlation analyses are unplanned; treat their p-values as descriptive.
- The power/MDE calculations condition on the observed within-cell variance and are not pre-study power analyses.

## Appendix: warnings captured during the run

- FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
- PyparsingDeprecationWarning: 'endQuoteChar' argument is deprecated, use 'end_quote_char'
- PyparsingDeprecationWarning: 'leaveWhitespace' deprecated - use 'leave_whitespace'
- PyparsingDeprecationWarning: 'oneOf' deprecated - use 'one_of'
- PyparsingDeprecationWarning: 'parseAll' argument is deprecated, use 'parse_all'
- PyparsingDeprecationWarning: 'parseString' deprecated - use 'parse_string'
- PyparsingDeprecationWarning: 'resetCache' deprecated - use 'reset_cache'
- PyparsingDeprecationWarning: 'setName' deprecated - use 'set_name'
- PyparsingDeprecationWarning: 'setParseAction' deprecated - use 'set_parse_action'
- PyparsingDeprecationWarning: 'unquoteResults' argument is deprecated, use 'unquote_results'
