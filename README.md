# Coverage versus within-epoch repetition at matched dose in transformer grokking

Code and data for the study of how unique-data **coverage** and within-epoch
**repetition** contribute to grokking (delayed generalization) in a small
transformer trained on modular addition, with the per-example dose held
constant across repetition levels.

Manuscript: *Coverage versus within-epoch repetition at matched dose in
transformer grokking* (submitted to Neural Processing Letters). The
submission package (PDF and LaTeX source) is archived in this repository's
[Releases](https://github.com/43aquarius/NeuralProcessingLetters/releases);
the published DOI will be added here once available.

## What is here

```
code/
  train/
    grok_lib.py         experiment framework: task, model, data stream, training
    run_one.py          run a single training condition (one seed)
    run_grid.py         the frozen 135-run grid (2 parallel workers, resume-safe)
    pilot.py            the four pilot-calibration conditions
    aggregate_runs.py   rebuild summary.csv + history.csv from the raw JSON logs
  analysis/
    make_runs_table.py  build the canonical per-run table runs.csv (cross-validates
                        every field of summary.csv against the raw JSONs)
    analyze.py          the statistical pipeline (exact permutation tests,
                        Kaplan-Meier/log-rank/RMST, stratified Cox, Fisher,
                        TOST, Jonckheere-Terpstra, permutation Spearman, Holm)
    stats_core.py       the statistical implementations (hand-written, NumPy)
    task_survival.py    KM/log-rank/RMST/Cox orchestration + KM figures
    task_equivalence.py TOST orchestration
    task_secondary.py   secondary-outcome orchestration
    verify_manuscript.py  re-verifies every statistic claimed in the manuscript
    tests/              unit tests for the statistical primitives
  figures/
    make_figures.py     Figures 1-3 of the manuscript
    make_tables.py      descriptive-statistics table (manuscript Table 2 source)
data/
  raw/                  135 per-run JSON logs (the primary data)
  summary.csv           one row per run (built by aggregate_runs.py)
  history.csv           one row per (run, evaluation step)
  runs.csv              canonical analysis table (built by make_runs_table.py)
results/
  stats/                every table/statistic CSV produced by analyze.py, plus
                        the verification report and the environment log
  figures/              manuscript figures (PDF + 300 dpi PNG)
  tables/               descriptive table (LaTeX + CSV)
docs/
  submission/           cover letter, submission-package manifest, release notes
  manuscript-revised/   preprint-style working version of the manuscript (LaTeX + PDF)
  reports/              the audit/QA trail (verification reports, changelogs,
                        action lists, internal referee report)
```

## Installation

Python 3.12 with the exact package versions in `requirements.txt`
(PyTorch 2.14, NumPy 2.1, SciPy 1.14, pandas 2.2, matplotlib 3.9 — no other
dependencies):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Everything runs on CPU. A censored 20,000-step run takes about 8.5 minutes
(one torch thread); runs that generalize earlier finish sooner (1-10 minutes
per run overall).

## Running one training condition

```bash
cd code/train
python run_one.py --coverage 0.55 --repetition 4 --mode blocked --seed 0
# -> one_<...>.json with the same schema as data/raw/
```

`--max-steps` (default 20,000) and the output directory (`--out <dir>/<name>.json`,
default: current directory) are optional. The seed jointly controls parameter
initialization, the choice of the unique training subset, and the data order.

## Running the full 135-run grid

The grid is frozen: coverage {25, 35, 45, 55, 70, 85}% at R=1 (arm A),
blocked and interleaved repetition R ∈ {2, 4, 8} at coverage {35, 55, 85}%
(arms B, C), and R ∈ {4, 8} blocked plus R=8 interleaved at 25% coverage
(arm D), five seeds (0-4) per condition, 20,000-step budget, evaluation every
100 steps.

```bash
cd code/train
python run_grid.py list            # show pending jobs
python run_grid.py worker 0 &     # two workers, round-robin
python run_grid.py worker 1 &
```

Jobs write incremental JSON logs into `data/raw/` and are resume-safe
(a `.done` marker per completed run). Two workers on a two-core CPU reproduce
the study in roughly 10-12 hours.

## Rebuilding the analysis from the raw logs

```bash
# 1. aggregate the raw JSONs
python code/train/aggregate_runs.py            # -> data/summary.csv, data/history.csv
# 2. canonical per-run table (cross-validates summary.csv against the raw JSONs)
python code/analysis/make_runs_table.py \
    --summary data/summary.csv --rundir data/raw --out data/runs.csv
# 3. full statistical pipeline (about 1 minute)
cd code/analysis
python analyze.py --runs ../../data/runs.csv --history ../../data/history.csv \
    --out ../../results/stats --margins 0.10 0.25 0.50
# 4. figures
cd ../figures
python make_figures.py
python make_tables.py
# 5. verify every manuscript statistic against a fresh recomputation
cd ../analysis
python verify_manuscript.py --runs ../../data/runs.csv \
    --history ../../data/history.csv --out ../../results/stats/verification_report.csv
```

Step 2 rebuilds `data/runs.csv` byte-identically from the raw JSONs
(sha256-verified). Step 5 runs the unit tests first (exact Mann-Whitney
perfect-separation p = 2/252, Kaplan-Meier against a hand-worked example,
bootstrap reproducibility) and then re-checks all 353 claimed statistics;
the final report is `results/stats/verification_report.csv`.

## Where each manuscript number, table, and figure comes from

| Manuscript item | Source |
|---|---|
| Figs. 1-3 (coverage, repetition, weight norms) | `code/figures/make_figures.py` -> `results/figures/` |
| Figs. 4-5 (Kaplan-Meier) | `code/analysis/task_survival.py` via `analyze.py` -> `results/stats/figures/` |
| Table 1 (design) | authored from the frozen design; cells cross-checked by `analyze.py` Task 0 |
| Table 2 (descriptives) | `code/figures/make_tables.py` + `analyze.py` -> `results/stats/descriptives.csv` |
| All exact/Wilcoxon-type tests, Holm | `results/stats/exact_tests.csv`, `secondary_tests.csv` |
| Log-rank, KM, RMST, Cox | `results/stats/logrank.csv`, `km_tables.csv`, `rmst*.csv`, `cox.csv` |
| Fisher / Clopper-Pearson | `results/stats/fisher.csv` |
| TOST equivalence tables | `results/stats/tost*.csv` |
| Manuscript-vs-recomputation audit | `results/stats/contradictions.csv`, `verification_report.csv` |
| Environment and seed log | `results/stats/env_log.txt` |

## Seeds

- Training: seeds 0-4 per condition. Each seed jointly controls parameter
  initialization, the unique-subset choice, and the data order.
- Analysis: master seed 20260922 with `numpy.random.default_rng` and the
  documented per-analysis offsets (101 bootstrap, 201 log-rank MC, 301 RMST,
  401 Jonckheere-Terpstra, 501 Spearman, 601 power simulation, 701
  wnorm@1000); deterministic enumerations consume no randomness. See
  `results/stats/env_log.txt` for the machine-readable record.

## Licence

Code is licensed under the [MIT License](LICENSE). Data files (everything
under `data/` and `results/`) and the manuscript figures are licensed under
[Creative Commons Attribution 4.0 International (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/).
If you reuse the data or figures, please cite the manuscript and this
repository. (Alternatives were considered in `PRE_RELEASE_CHECKLIST.md`;
swap them by editing `LICENSE`, `CITATION.cff`, `.zenodo.json`, and this
section if a different choice is preferred.)
