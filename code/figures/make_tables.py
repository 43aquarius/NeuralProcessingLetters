"""Generate the LaTeX descriptives table from summary.csv.

Emits paper/table_descriptives.tex with one row per condition:
GrokTime median [IQR], censored k/5, MemTime median, final test acc median [IQR].
"""
import numpy as np
import pandas as pd
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAIN = REPO / "data"
OUT = REPO / "results" / "tables" / "table_descriptives.tex"
OUT.parent.mkdir(parents=True, exist_ok=True)  # create results/tables/ on first use
MAX_STEPS = 20_000

df = pd.read_csv(MAIN / "summary.csv")


def fmt_med_iqr(x, unit=""):
    if len(x) == 0:
        return "---"
    med, q1, q3 = np.median(x), np.percentile(x, 25), np.percentile(x, 75)
    return f"{med/1000:.1f}{unit} [{q1/1000:.1f}, {q3/1000:.1f}]"


def fmt_acc(x):
    if len(x) == 0:
        return "---"
    med, q1, q3 = np.median(x), np.percentile(x, 25), np.percentile(x, 75)
    return f"{med*100:.1f} [{q1*100:.1f}, {q3*100:.1f}]"


rows = []
order = []
for cov in (25, 35, 45, 55, 70, 85):
    for rep in (1, 2, 4, 8):
        for mode in ("blocked", "interleaved"):
            if rep == 1 and mode == "interleaved":
                continue                      # identical to blocked R=1
            q = df.query("coverage==@cov and repetition==@rep and mode==@mode")
            if len(q) == 0:
                continue
            label_mode = "blocked" if rep == 1 else mode
            order.append((cov, rep, label_mode))
            n_cens = int(q["grok_censored"].sum())
            rows.append(
                f"{cov} & {rep} & {label_mode} & "
                f"{fmt_med_iqr(q['grok_step_filled'])}k & "
                f"{n_cens}/{len(q)} & "
                f"{int(np.median(q['mem_step']))} & "
                f"{fmt_acc(q['final_test_acc'])} \\\\"
            )

header = r"""\begin{table}[t]
\centering
\caption{\textbf{Descriptive statistics by condition.} GrokTime (steps,
thousands) and final test accuracy are given as median [interquartile
range] across $n=5$ seeds; censored runs are counted at the budget
($20{,}000$ steps) in the GrokTime median. MemTime is the median step at
which training accuracy first reaches $95\%$. Mode is vacuous at $R=1$
(copies coincide); interleaved $R{=}1$ is identical to blocked $R{=}1$ and
omitted.}
\label{tab:descriptives}
\small
\begin{tabular}{rrlrrrr}
\toprule
Coverage (\%) & $R$ & Mode & GrokTime (k steps) & Cens. & MemTime & Final test acc. (\%) \\
\midrule
"""

footer = r"""\bottomrule
\end{tabular}
\end{table}
"""

OUT.write_text(header + "\n".join(rows) + "\n" + footer)
print(f"wrote {OUT} with {len(rows)} rows")
