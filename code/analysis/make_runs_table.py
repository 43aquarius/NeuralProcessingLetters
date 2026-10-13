#!/usr/bin/env python3
"""Build the canonical per-run table `runs.csv` from the archived experiment outputs.

Sources (no data are invented; every field is copied from an archived file):
  1. summary.csv  -- one row per run, produced by the training pipeline.
  2. main*_*.json -- the raw per-run logs; used for n_test / n_train_unique and
                     to cross-validate every summary.csv field.

The output uses the canonical column names expected by analyze.py:
  run_id, coverage, R, mode, seed, grok_time (NaN if never grokked),
  censored, mem_time, final_train_acc, final_test_acc, final_l2_norm,
  n_train_unique, n_test, stop_step

Any cross-source mismatch is printed and aborts the build (nothing is
overwritten silently).

Usage:
  python make_runs_table.py --summary /path/to/summary.csv \
                            --rundir /path/to/main_run_jsons \
                            --out runs.csv
"""
import argparse
import json
import sys
from pathlib import Path

import pandas as pd


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--summary", required=True, help="path to summary.csv")
    ap.add_argument("--rundir", required=True, help="directory with the 135 main*_*.json run logs")
    ap.add_argument("--out", default="runs.csv")
    args = ap.parse_args()

    df = pd.read_csv(args.summary)
    rundir = Path(args.rundir)

    runs = pd.DataFrame(
        {
            "run_id": df["file"].str.replace(r"\.json$", "", regex=True),
            "coverage": df["coverage"].astype(int),
            "R": df["repetition"].astype(int),
            "mode": df["mode"].astype(str),
            "seed": df["seed"].astype(int),
            "grok_time": df["grok_step"],  # empty if never grokked
            "censored": df["grok_censored"].astype(bool),
            "mem_time": df["mem_step"].astype(int),
            "final_train_acc": df["final_train_acc"].astype(float),
            "final_test_acc": df["final_test_acc"].astype(float),
            "final_l2_norm": df["final_wnorm"].astype(float),
            "stop_step": df["steps_run"].astype(int),
        }
    )

    mismatches = []
    n_test_col, n_uniq_col = [], []
    for i, row in runs.iterrows():
        jpath = rundir / df["file"].iloc[i]
        if not jpath.exists():
            mismatches.append(f"missing run log: {jpath}")
            n_test_col.append(None)
            n_uniq_col.append(None)
            continue
        with open(jpath) as fh:
            s = json.load(fh)["summary"]
        cfg = s["config"]
        # cross-validate the design fields
        for canon, jsonval in [
            ("coverage", int(round(cfg["coverage"] * 100))),
            ("R", cfg["repetition"]),
            ("mode", cfg["mode"]),
            ("seed", cfg["seed"]),
        ]:
            if row[canon] != jsonval:
                mismatches.append(f"{row['run_id']}: {canon} summary={row[canon]} json={jsonval}")
        # cross-validate the outcome fields
        jgrok = s["grok_step"]
        sgrok = None if pd.isna(row["grok_time"]) else int(row["grok_time"])
        if jgrok != sgrok:
            mismatches.append(f"{row['run_id']}: grok_time summary={sgrok} json={jgrok}")
        if bool(s["steps_run"] > jgrok if jgrok is not None else False):
            mismatches.append(f"{row['run_id']}: steps_run={s['steps_run']} exceeds grok step")
        if (s["mem_step"] is None) or (int(s["mem_step"]) != int(row["mem_time"])):
            mismatches.append(f"{row['run_id']}: mem_time summary={row['mem_time']} json={s['mem_step']}")
        for canon, jkey in [
            ("final_train_acc", "final_train_acc"),
            ("final_test_acc", "final_test_acc"),
            ("final_l2_norm", "final_wnorm"),
            ("stop_step", "steps_run"),
        ]:
            if abs(float(row[canon]) - float(s[jkey])) > 1e-9:
                mismatches.append(f"{row['run_id']}: {canon} summary={row[canon]} json={s[jkey]}")
        # censoring flag consistency
        jcens = jgrok is None
        if bool(row["censored"]) != jcens:
            mismatches.append(f"{row['run_id']}: censored summary={row['censored']} json={jcens}")
        n_test_col.append(int(s["n_test"]))
        n_uniq_col.append(int(s["n_train_unique"]))

    runs["n_test"] = n_test_col
    runs["n_train_unique"] = n_uniq_col

    # n_test consistency with the documented construction rule (report only)
    rule = 529 - (runs["coverage"] / 100.0 * 529).round().astype(int)
    bad = runs["n_test"] != rule
    if bad.any():
        for _, r in runs[bad].iterrows():
            mismatches.append(f"{r['run_id']}: n_test={r['n_test']} disagrees with 529-round(cov*529)={int(rule[bad][r.name]) if False else int((529 - round(r['coverage'] / 100.0 * 529)))}")

    if len(runs) != 135:
        mismatches.append(f"expected 135 rows, found {len(runs)}")

    if mismatches:
        print("CROSS-VALIDATION FAILURES (runs.csv NOT written):")
        for m in mismatches:
            print("  -", m)
        sys.exit(1)

    runs.to_csv(args.out, index=False)
    print(f"wrote {args.out}: {len(runs)} runs, {runs.groupby(['coverage', 'R', 'mode']).ngroups} conditions")
    print("n_test per coverage:", runs.groupby("coverage")["n_test"].agg(["min", "max"]).to_dict("index"))


if __name__ == "__main__":
    main()
