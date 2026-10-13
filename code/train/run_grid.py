"""Grid runner: 2 parallel workers, resume-safe, incremental JSON results.

Grid (frozen, see paper/STUDY_DESIGN.md):
  Arm A (coverage):   R=1, C in {25,35,45,55,70,85} x seeds 0-4
  Arm B (blocked):    C in {35,55,85} x R in {2,4,8} x seeds 0-4
  Arm C (interleaved):C in {35,55,85} x R in {2,4,8} x seeds 0-4
All runs: max_steps=20000, eval_every=100, batch 256, AdamW lr 1e-3 wd 1.0.

Usage:
  python3 run_grid.py list          # show pending jobs
  python3 run_grid.py worker <id>   # run jobs with worker=<id> (0 or 1)
"""
import json
import sys
import time
from pathlib import Path

import torch

from grok_lib import Config, run_training, save_result

torch.set_num_threads(1)

RESULTS = Path(__file__).resolve().parents[2] / "data" / "raw"
DONE = RESULTS / ".done"


def jobs():
    out = []
    for c in (0.25, 0.35, 0.45, 0.55, 0.70, 0.85):
        for seed in range(5):
            out.append(("A", dict(coverage=c, repetition=1, mode="blocked", seed=seed)))
    for c in (0.35, 0.55, 0.85):
        for r in (2, 4, 8):
            for seed in range(5):
                out.append(("B", dict(coverage=c, repetition=r, mode="blocked", seed=seed)))
    for c in (0.35, 0.55, 0.85):
        for r in (2, 4, 8):
            for seed in range(5):
                out.append(("C", dict(coverage=c, repetition=r, mode="interleaved", seed=seed)))
    # D arm (added after design audit): repetition below the critical coverage,
    # required by the pre-registered Family 3 contrast (C25 R8).
    for r, mode in ((4, "blocked"), (8, "blocked"), (8, "interleaved")):
        for seed in range(5):
            out.append(("D", dict(coverage=0.25, repetition=r, mode=mode, seed=seed)))
    return out


def name_for(arm, kw):
    return f"{arm}_C{int(kw['coverage']*100)}_R{kw['repetition']}_{kw['mode']}_s{kw['seed']}"


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        pending = [n for n in (name_for(a, k) for a, k in jobs())
                   if not (DONE / n).exists()]
        print(f"total={len(jobs())} pending={len(pending)}")
        for n in pending[:10]:
            print(" ", n)
        return

    if cmd == "worker":
        wid = int(sys.argv[2])
        DONE.mkdir(parents=True, exist_ok=True)
        RESULTS.mkdir(parents=True, exist_ok=True)
        all_jobs = jobs()
        my_jobs = [j for i, j in enumerate(all_jobs) if i % 2 == wid]  # round-robin
        for arm, kw in my_jobs:
            n = name_for(arm, kw)
            if (DONE / n).exists():
                continue
            t0 = time.time()
            cfg = Config(tag=f"main{arm}", max_steps=20_000, **kw)
            out = run_training(cfg)
            save_result(RESULTS, out)
            (DONE / n).write_text("ok")
            s = out["summary"]
            print(f"[w{wid}] {n}: grok={s['grok_step']} test={s['final_test_acc']} "
                  f"({time.time()-t0:.0f}s)", flush=True)
        print(f"[w{wid}] all jobs finished", flush=True)


if __name__ == "__main__":
    main()
