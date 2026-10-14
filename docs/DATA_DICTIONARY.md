# Data dictionary

This file documents the column names, units, and meaning of every tabular
file in `data/`. The per-run JSON logs in `data/raw/` are the primary
record; every table below is derived from them and can be rebuilt with the
commands in the README (aggregate -> `make_runs_table.py` -> `runs.csv`,
byte-identical, sha256-verified).

## `data/raw/*.json` — per-run training logs (the primary data)

One JSON file per run, named `main<Arm>_C<coverage>_R<repetition>_<mode>_s<seed>.json`
(e.g. `mainB_C55_R4_blocked_s2.json`), containing:

| Field | Type | Meaning |
|---|---|---|
| `summary.config` | object | the frozen run configuration: `p` (modulus, 23), `d_model` (64), `n_layers` (2), `n_heads` (4), `lr` (1e-3), `weight_decay` (1.0), `batch_size` (256), `max_steps` (20,000), `eval_every` (100), `coverage` (fraction 0-1), `repetition` (integer R), `mode` (`blocked`/`interleaved`), `seed` (0-4), `grok_threshold` (0.95), `mem_threshold` (0.95), `tag` (arm label A-D) |
| `summary.n_train_unique` | int | number of unique training problems (`round(coverage * p^2)`) |
| `summary.n_test` | int | number of held-out test problems (the complement) |
| `summary.grok_step` | int or null | first evaluated step with test accuracy >= 0.95; null if the run never reached the criterion within the budget |
| `summary.mem_step` | int | first evaluated step with training accuracy >= 0.95 |
| `summary.final_train_acc`, `final_test_acc` | float in [0,1] | accuracies at the stopping step (grok step for grokked runs, budget for censored runs) |
| `summary.final_wnorm` | float | parameter L2 norm at the stopping step |
| `summary.steps_run` | int | number of optimization steps actually executed |
| `summary.wall_seconds` | float | wall-clock duration of the run (CPU) |
| `history` | list of objects | one record per evaluation step (steps 1, 100, 200, ...), each with `step`, `train_loss`, `train_acc`, `test_acc`, `wnorm` (same units as above) |

## `data/summary.csv` — one row per run (built by `aggregate_runs.py`)

| Column | Type | Meaning |
|---|---|---|
| `file` | string | raw JSON file name |
| `coverage` | int (%) | training-set coverage, 25/35/45/55/70/85 |
| `repetition` | int | within-epoch repetition R, 1/2/4/8 |
| `mode` | string | `blocked` or `interleaved` (vacuous at R=1) |
| `seed` | int | random seed 0-4 |
| `grok_step` | int or empty | GrokTime: first evaluated step with test accuracy >= 95%; empty if censored |
| `grok_censored` | bool | true if the run never generalized within the 20,000-step budget |
| `grok_step_filled` | int | `grok_step` with censored runs filled at the budget 20,000 (used for ranks; censored = worst) |
| `mem_step` | int | MemTime: first evaluated step with training accuracy >= 95% |
| `final_train_acc` | float [0,1] | training accuracy at the stopping step |
| `final_test_acc` | float [0,1] | test accuracy at the stopping step (censored runs: at budget exhaustion) |
| `final_wnorm` | float | final parameter L2 norm at the stopping step |
| `steps_run` | int | steps actually executed |
| `wall_seconds` | float | wall-clock duration in seconds |

## `data/history.csv` — one row per (run, evaluation step)

| Column | Type | Meaning |
|---|---|---|
| `coverage` | int (%) | as above |
| `repetition` | int | as above (R) |
| `mode` | string | as above |
| `seed` | int | as above |
| `step` | int | evaluation step (1, then every 100 up to the stopping step) |
| `train_loss` | float | mean cross-entropy on the batches consumed since the previous evaluation |
| `train_acc` | float [0,1] | training accuracy at this step |
| `test_acc` | float [0,1] | test accuracy on the full held-out complement |
| `wnorm` | float | parameter L2 norm at this step |

## `data/runs.csv` — the canonical analysis table (built by `make_runs_table.py`)

One row per run; every field is cross-validated against the raw JSONs during
the build. Differs from `summary.csv` in column names and in the censoring
encoding:

| Column | Type | Meaning |
|---|---|---|
| `run_id` | string | run identifier (= raw file stem) |
| `coverage` | int (%) | as above |
| `R` | int | repetition (renamed from `repetition`) |
| `mode` | string | as above |
| `seed` | int | as above |
| `grok_time` | int or empty | GrokTime; empty if censored |
| `censored` | bool | GrokTime censoring indicator |
| `mem_time` | int | MemTime |
| `final_train_acc` | float [0,1] | as above |
| `final_test_acc` | float [0,1] | as above |
| `final_l2_norm` | float | as above (renamed from `final_wnorm`) |
| `stop_step` | int | as above (renamed from `steps_run`) |
| `n_test` | int | held-out test-set size (79/159/238/291/344/397 by coverage) |
| `n_train_unique` | int | unique training problems (132/185/238/291/370/450 by coverage) |

## Derived outputs

`results/stats/*.csv` and `results/figures/` are produced by `analyze.py`,
`task_*.py`, `make_figures.py`, and `make_tables.py`; each file's meaning is
given in the README's "Where each manuscript number, table, and figure comes
from" table, and the full audit trail is `results/stats/verification_report.csv`
(353 claimed statistics re-derived from these files).

`results/stats/stats.json` is a compact per-condition summary of the
pre-registered-style exploratory statistics (per-cell medians of the weight
norm at step 1,000, family tests, mode contrasts, and the Spearman
exploration) written by `code/train/aggregate_runs.py` when the raw logs are
aggregated. It is a derived convenience summary, not primary data.
