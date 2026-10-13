"""Pilot: calibrate grokking timescale and wall-clock budget.

Four conditions, one seed each, max 15k steps, 1 torch thread per process.
Usage: python3 pilot.py <condition>  (c85, c45, c25, c85r8)
"""
import sys
import torch
from pathlib import Path
from grok_lib import Config, run_training, save_result

torch.set_num_threads(1)

PILOTS = {
    "c85":  dict(coverage=0.85, repetition=1, mode="blocked"),
    "c45":  dict(coverage=0.45, repetition=1, mode="blocked"),
    "c25":  dict(coverage=0.25, repetition=1, mode="blocked"),
    "c85r8": dict(coverage=0.85, repetition=8, mode="blocked"),
}

key = sys.argv[1]
cfg = Config(seed=0, max_steps=15_000, eval_every=100, tag="pilot", **PILOTS[key])
out = run_training(cfg)
path = save_result(Path(__file__).resolve().parents[2] / "results" / "pilot", out)
s = out["summary"]
print(f"[{key}] grok_step={s['grok_step']} mem_step={s['mem_step']} "
      f"final_test={s['final_test_acc']} final_train={s['final_train_acc']} "
      f"steps_run={s['steps_run']} wall={s['wall_seconds']}s -> {path}")
