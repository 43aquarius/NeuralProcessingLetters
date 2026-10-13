#!/usr/bin/env python3
"""Run a single training condition (one seed) and save the JSON log.

Thin convenience wrapper around grok_lib.run_training — identical
configuration knobs to run_grid.py, for one run instead of the grid.

Usage:
  python run_one.py --coverage 0.55 --repetition 4 --mode blocked --seed 0 \
                    [--max-steps 20000] [--out out.json]

Runtime on CPU: a censored 20,000-step run takes about 8.5 minutes
(one torch thread); runs that grok early finish sooner (1-10 minutes).
"""
import argparse
import time
from pathlib import Path

import torch

from grok_lib import Config, run_training, save_result

torch.set_num_threads(1)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--coverage", type=float, required=True,
                    help="fraction of the 529 problems in the unique set (e.g. 0.55)")
    ap.add_argument("--repetition", type=int, required=True,
                    help="within-epoch repetition factor R (1, 2, 4, or 8)")
    ap.add_argument("--mode", choices=["blocked", "interleaved"], default="blocked")
    ap.add_argument("--seed", type=int, required=True, help="0-4 in the grid")
    ap.add_argument("--max-steps", type=int, default=20_000)
    ap.add_argument("--out", default="run_out.json", help="output JSON path")
    args = ap.parse_args()

    t0 = time.time()
    cfg = Config(tag="one", max_steps=args.max_steps,
                 coverage=args.coverage, repetition=args.repetition,
                 mode=args.mode, seed=args.seed)
    out = run_training(cfg)
    out_dir = Path(args.out).resolve().parent
    save_result(out_dir, out)
    cfgd = out["summary"]["config"]
    name = (f"{cfgd['tag']}_C{int(cfgd['coverage']*100)}_R{cfgd['repetition']}_"
            f"{cfgd['mode']}_s{cfgd['seed']}.json")
    s = out["summary"]
    print(f"grok={s['grok_step']} mem={s['mem_step']} "
          f"final_test={s['final_test_acc']:.4f} "
          f"({time.time()-t0:.0f}s) -> {out_dir / name}")


if __name__ == "__main__":
    main()
