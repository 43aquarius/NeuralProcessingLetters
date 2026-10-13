"""Aggregate grid results into a tidy table and compute pre-specified statistics.

Outputs:
  results/main/summary.csv     one row per run (summary outcomes)
  results/main/history.csv     one row per (run, eval point) for curves
  results/main/stats.json      pre-specified tests, effect sizes, CIs
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

# reads the per-run JSONs from data/raw and writes summary.csv and
# history.csv to data/ (paths are repo-relative)
DATA = Path(__file__).resolve().parents[2] / "data"
MAIN = DATA / "raw"  # per-run JSON logs
MAX_STEPS = 20_000

# ---------------------------------------------------------------------------
# Load runs
# ---------------------------------------------------------------------------

rows, hist_rows = [], []
for f in sorted(MAIN.glob("main*_s*.json")):
    d = json.loads(f.read_text())
    s = d["summary"]
    c = s["config"]
    rows.append(dict(
        file=f.name,
        coverage=int(c["coverage"] * 100), repetition=c["repetition"],
        mode=c["mode"], seed=c["seed"],
        grok_step=s["grok_step"], grok_censored=s["grok_step"] is None,
        grok_step_filled=s["grok_step"] if s["grok_step"] is not None else MAX_STEPS,
        mem_step=s["mem_step"],
        final_train_acc=s["final_train_acc"], final_test_acc=s["final_test_acc"],
        final_wnorm=s["final_wnorm"], steps_run=s["steps_run"],
        wall_seconds=s["wall_seconds"],
    ))
    for h in d["history"]:
        hist_rows.append(dict(
            coverage=int(c["coverage"] * 100), repetition=c["repetition"],
            mode=c["mode"], seed=c["seed"], **h))

df = pd.DataFrame(rows)
df.to_csv(DATA / "summary.csv", index=False)
hist_df = pd.DataFrame(hist_rows)
hist_df.to_csv(DATA / "history.csv", index=False)

print(f"runs loaded: {len(df)}")
print(df.groupby(["mode", "coverage", "repetition"]).size().to_string())

# ---------------------------------------------------------------------------
# Descriptive table
# ---------------------------------------------------------------------------

desc = df.groupby(["mode", "coverage", "repetition"]).agg(
    n=("grok_step", "size"),
    grok_med=("grok_step_filled", "median"),
    grok_q1=("grok_step_filled", lambda x: x.quantile(0.25)),
    grok_q3=("grok_step_filled", lambda x: x.quantile(0.75)),
    n_censored=("grok_censored", "sum"),
    mem_med=("mem_step", "median"),
    test_acc_med=("final_test_acc", "median"),
    wnorm_med=("final_wnorm", "median"),
).reset_index()
desc.to_csv(MAIN / "descriptives.csv", index=False)
print("\n", desc.to_string(index=False))

# ---------------------------------------------------------------------------
# Statistics helpers
# ---------------------------------------------------------------------------

def mw_exact(a, b):
    """Exact Mann-Whitney + rank-biserial effect size + bootstrap CI of median diff."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    if len(a) == 0 or len(b) == 0:
        return dict(U=None, p=None, rank_biserial=None, median_diff=None,
                    ci95=[None, None], n_a=len(a), n_b=len(b))
    U, p = stats.mannwhitneyu(a, b, alternative="two-sided")
    rbc = 1 - 2 * U / (len(a) * len(b))          # rank-biserial (b vs a)
    rng = np.random.default_rng(20260922)
    diffs = []
    for _ in range(10_000):
        da = rng.choice(a, size=len(a), replace=True)
        db = rng.choice(b, size=len(b), replace=True)
        diffs.append(np.median(db) - np.median(a))
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return dict(U=float(U), p=float(p), rank_biserial=float(rbc),
                median_diff=float(np.median(b) - np.median(a)),
                ci95=[float(lo), float(hi)])


def perm_test_medians(a, b, n_perm=10_000):
    a = np.asarray(a, float); b = np.asarray(b, float)
    obs = np.median(b) - np.median(a)
    pool = np.concatenate([a, b])
    rng = np.random.default_rng(20260922)
    count = 0
    for _ in range(n_perm):
        rng.shuffle(pool)
        pa, pb = pool[:len(a)], pool[len(a):]
        if abs(np.median(pb) - np.median(pa)) >= abs(obs) - 1e-9:
            count += 1
    return dict(observed=float(obs), p=(count + 1) / (n_perm + 1))


def sel(mode, cov, rep, col="grok_step_filled"):
    q = f"mode=='{mode}' and coverage=={cov} and repetition=={rep}"
    return df.query(q)[col].to_numpy()


def holm(pvals):
    order = np.argsort(pvals)
    m = len(pvals)
    adj = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        val = (m - rank) * pvals[idx]
        running = max(running, val)
        adj[idx] = min(1.0, running)
    return adj


out = {"n_runs": int(len(df)), "max_steps": MAX_STEPS}

# Family 1 (H1): coverage effect on GrokTime (R=1)
fam1 = {
    "85 vs 45": mw_exact(sel("blocked", 45, 1), sel("blocked", 85, 1)),
    "85 vs 25": mw_exact(sel("blocked", 25, 1), sel("blocked", 85, 1)),
}
fam1_perm = {
    "85 vs 45": perm_test_medians(sel("blocked", 45, 1), sel("blocked", 85, 1)),
    "85 vs 25": perm_test_medians(sel("blocked", 25, 1), sel("blocked", 85, 1)),
}
p1 = [v["p"] for v in fam1.values() if v["p"] is not None]
for key, adjp in zip(fam1, holm(p1)):
    if fam1[key]["p"] is not None:
        fam1[key]["p_holm"] = float(adjp)

# Family 2 (H2b): repetition effect on GrokTime within coverage (blocked)
fam2 = {}
for cov in (35, 55, 85):
    fam2[f"C{cov}: R1 vs R4"] = mw_exact(sel("blocked", cov, 1), sel("blocked", cov, 4))
    fam2[f"C{cov}: R1 vs R8"] = mw_exact(sel("blocked", cov, 1), sel("blocked", cov, 8))
p2 = [v["p"] for v in fam2.values() if v["p"] is not None]
for key, adjp in zip(fam2, holm(p2)):
    if fam2[key]["p"] is not None:
        fam2[key]["p_holm"] = float(adjp)

# Family 3 (H3): final test accuracy, extreme contrast
fam3 = {
    "C25 R8 vs C55 R1 (test acc)": mw_exact(
        df.query("coverage==55 and repetition==1 and mode=='blocked'")["final_test_acc"].to_numpy(),
        df.query("coverage==25 and repetition==8 and mode=='blocked'")["final_test_acc"].to_numpy()),
    "C25 R8 vs C85 R1 (test acc)": mw_exact(
        df.query("coverage==85 and repetition==1 and mode=='blocked'")["final_test_acc"].to_numpy(),
        df.query("coverage==25 and repetition==8 and mode=='blocked'")["final_test_acc"].to_numpy()),
}
p3 = [v["p"] for v in fam3.values() if v["p"] is not None]
for key, adjp in zip(fam3, holm(p3)):
    if fam3[key]["p"] is not None:
        fam3[key]["p_holm"] = float(adjp)

# Mode contrast (exploratory): blocked vs interleaved at same (C, R)
mode_contrast = {}
for cov, reps in ((25, (8,)), (35, (2, 4, 8)), (55, (2, 4, 8)), (85, (2, 4, 8))):
    for rep in reps:
        a = sel("interleaved", cov, rep)
        b = sel("blocked", cov, rep)
        if len(a) and len(b):
            mode_contrast[f"C{cov} R{rep}"] = mw_exact(a, b)

# Exploratory: weight norm correlations
grokked = df[df["grok_censored"] == False]
spearman_wn = stats.spearmanr(grokked["grok_step_filled"], grokked["final_wnorm"]) \
    if len(grokked) > 2 else None

# H4 (exploratory): weight norm at a fixed pre-transition step (1000) across R
# (avoids the early-stop confound: grokked runs stop at GrokTime)
h4 = {}
for cov in (35, 55, 85):
    for mode in ("blocked", "interleaved"):
        vals_r = {}
        for rep in [1, 2, 4, 8]:
            m = "blocked" if rep == 1 else mode
            q = hist_df.query("coverage==@cov and repetition==@rep and mode==@m and step==1000")
            if len(q):
                vals_r[rep] = q["wnorm"].tolist()
        h4[f"C{cov} {mode}"] = {f"R{r}": dict(median=float(np.median(v)), n=len(v))
                                for r, v in vals_r.items()}
out["h4_wnorm_at_1000_exploratory"] = h4

# Grokked vs censored final norm at matched coverage 35 (stop-time caveat applies)
g35 = df.query("coverage==35 and repetition==1 and mode=='blocked'")
out["c35_grok_vs_cens_wnorm"] = dict(
    grokked_final_wnorm=g35.query("grok_censored==False")["final_wnorm"].tolist(),
    censored_final_wnorm=g35.query("grok_censored==True")["final_wnorm"].tolist())

out["family1_coverage"] = fam1
out["family1_permutation"] = fam1_perm
out["family2_repetition"] = fam2
out["family3_finalacc"] = fam3
out["mode_contrast_exploratory"] = mode_contrast
out["wnorm_spearman_exploratory"] = (
    dict(rho=float(spearman_wn.statistic), p=float(spearman_wn.pvalue), n=int(len(grokked)))
    if spearman_wn is not None else None)

# Memory speed across R (H2a)
mem_effect = {}
for cov in (35, 55, 85):
    mem_effect[f"C{cov} R1 vs R8 memtime"] = mw_exact(
        df.query(f"coverage=={cov} and repetition==1 and mode=='blocked'")["mem_step"].dropna().to_numpy(),
        df.query(f"coverage=={cov} and repetition==8 and mode=='blocked'")["mem_step"].dropna().to_numpy())
out["memory_speed_H2a"] = mem_effect

(MAIN / "stats.json").write_text(json.dumps(out, indent=1))
print("\nstats written to", MAIN / "stats.json")

# Print compact tables
def _fmt(v, spec):
    return "n/a" if v is None or (isinstance(v, list) and any(x is None for x in v)) \
        else format(v, spec)


def _pline(label, v):
    if v.get("p") is None:
        print(f"{label}: n/a (missing runs)")
        return
    print(f"{label}: p={v['p']:.4g} (Holm {v.get('p_holm', float('nan')):.4g}), "
          f"rbc={v['rank_biserial']:+.2f}, diff={v['median_diff']:.3f} "
          f"[{v['ci95'][0]:.3f},{v['ci95'][1]:.3f}]")


print("\n--- Family 1 (coverage, R=1) ---")
for k, v in fam1.items():
    _pline(k, v)
print("\n--- Family 2 (repetition blocked) ---")
for k, v in fam2.items():
    _pline(k, v)
print("\n--- Family 3 (final test acc) ---")
for k, v in fam3.items():
    _pline(k, v)
print("\n--- Mode contrast (exploratory) ---")
for k, v in mode_contrast.items():
    _pline(k, v)
if out["wnorm_spearman_exploratory"]:
    w = out["wnorm_spearman_exploratory"]
    print(f"\nwnorm~groktime Spearman rho={w['rho']:+.3f} p={w['p']:.3g} n={w['n']}")
