# Prompt 4 — Figure Fix Report

Script: `scripts/make_figures.py` (single source of all three figures; regenerated
and re-embedded in `main.pdf`). Vector PDF plus 300 dpi PNG saved for every
figure (`figs/`, `figs/png300/`). No plotted data, statistics, colour meaning,
or axis ranges were changed — only the defect fixes below.

## Fig. 1c — censoring labels "5/5" and "3/5" overlapped (FIXED)

- **Defect (confirmed at 300 dpi with VLM):** the two censoring labels at 25%
  ("5/5") and 35% ("3/5") coverage were centred above their arrow heads and
  visually merged into "5/53/5"; they also sat close to the median diamonds.
- **Fix:** each label is now placed to the right of its arrow shaft at
  mid-arrow height (`ax.text(cov + 1.8, 1.06 × budget, ha="left")`), so the two
  labels cannot collide at the panel width; arrows, markers, and data are
  untouched.
- **Post-fix VLM check:** labels clearly separated, no collision with arrows,
  markers, or points; panels a, b, d unchanged and clean.
- The caption needs no change (it says "`k/5` gives censored runs of five"
  without specifying label position; the dashed budget line it mentions is
  drawn by the code).

## Fig. 2 — panel letters clipped at the top (NOT PRESENT in current PDF)

- High-resolution inspection of the current PDF (300 dpi crop of the top strip,
  plus a full-panel VLM check) shows the bold panel letters a–d fully visible
  with clear padding from the top edge; no text touches the figure border.
  This defect had already been fixed in an earlier visual-QA round (the
  letters are placed at `y = 1.06` axes coordinates with `constrained_layout`).
- **No change made** — reporting per the rule that nothing else be modified.

## Fig. 3a — legend overlapped the curves (FIXED)

- **Defect (confirmed with a 3×3 grid overlay):** the 2×2 legend anchored
  `lower left` extended into the lower-centre region, and the flat 25%
  (no-grok) curve ran directly through the legend box.
- **Fix:** legend moved to the empty upper-right corner (`loc="upper right"`)
  — at late steps only the low 25% curve exists, so that corner is free of
  data; nothing else in the panel changed.
- **Post-fix VLM check:** legend in a clear area, no curve or band passes
  through it, no text clipped.

## Fig. 3b — x-tick labels overlapped (FIXED); Spearman annotation (NO COLLISION)

- **Defect (confirmed):** matplotlib's automatic log-scale minor-tick labels
  (2×10³, 3×10³, 10⁴ …) crowded together near the panel bottom, with
  inconsistent formatting.
- **Fix:** explicit ticks at 2×10³, 5×10³, 10⁴, 2×10⁴ (evenly spaced in log),
  minor ticks disabled — consistent formatting and clear separation.
- **Spearman ρ annotation:** grid-overlay inspection shows the annotation sits
  above all data points and does not touch any marker in the current PDF
  (this had already been addressed in an earlier round), so per the rules it
  was left untouched.

## Fig. 3c — unchanged (legend clean, no collision found).

## Fig. 4 and Fig. 5 (Kaplan–Meier) — no visual change; budget-line report

- **The KM figure code (`grokking-stats/task_survival.py`) does NOT draw a
  dashed budget line.** The only horizontal references are the natural axis;
  censoring is marked with "|" tick markers, and the x-axis is extended to
  20,500 steps so the censoring ticks at the 20,000-step budget are fully
  visible.
- The manuscript captions for Figs. 4 and 5 therefore contain no "dashed
  budget line" wording (verified — any such wording was removed in an earlier
  pass), which matches the code.

## Greyscale / colour-vision report (no colours changed)

Panel colour assignments are unchanged: Fig. 1/3 coverage colours use a
viridis ramp, Fig. 3 repetition colours use Okabe–Ito palette entries, and
modes are distinguished by solid vs dashed lines plus distinct markers.
Okabe–Ito and viridis are colour-blind-safe palettes, and the mode contrast
does not rely on hue alone (line style + marker differ), so distinguishability
in greyscale and for colour-blind readers is expected to be preserved. One
residual risk, reported without change: in Fig. 3a the 25% curve (magenta-red
"#BB5566") and the 55% curve (Okabe–Ito orange "#E69F00") can look similar in
deuteranopia simulations; they are separated in the plot (25% stays flat and
high, 55% drops early), so the panels remain readable, but the author may
request a colour change if a reviewer raises it.

## Files

- Updated script: `code/figures/make_figures.py` (3 targeted edits,
  commented at the edit sites)
- Regenerated outputs: the figure PDFs and 300-dpi PNGs in
  `results/figures/` (the PDF set used by the manuscript is also under
  `docs/manuscript-revised/figs/`).
- Manuscript recompiled (`main.pdf`, 14 pages, no new warnings).
