# Part C — Final Cleanup Pass: Author Action List (ranked by importance)

## Critical — factual accuracy

**1. Sect. 4.3 claims "all p ≥ 0.40" for the mode permutation log-rank tests — this appears to be wrong.**
The archived pipeline (`grokking-stats/results/logrank.csv`, mode family) gives: C35/R2 blocked-vs-interleaved p = 0.317, C55/R2 = 0.754, C55/R4 = 0.865, C55/R8 = 0.397, C85/R2 = 0.683, C85/R4 = 0.994, C85/R8 = 0.952 (C35/R4, C35/R8, C25/R8 skipped — zero events). Two values are below 0.40. Suggested fix after you confirm from the repository copy: "all p ≥ 0.32". I did not change it because the corrected bound is not derivable from numbers already in the manuscript (your rule 1). Related, minor: "exact rank tests: all p ≥ 0.24" in the same sentence rests on the archived minimum 0.2381, which rounds to 0.24 but is strictly below it; consider "all p ≥ 0.238" or "all p > 0.2".

**2. Reference details you must check against the original papers (nothing was changed):**
- **Ref. 14 (Zhang et al., Understanding deep learning…)**: fourth author appears as "O. Recht" — presumably a typo for **B. Recht** (Benjamin Recht).
- **Ref. 9 (Nanda et al., Progress measures for grokking…)**: the author list and year need verification — the published ICLR 2024 paper may have three authors (Nanda, Lee, Wattenberg); "J. Lindsey" needs checking.
- **Ref. 12 (Varma et al., Explaining grokking through circuit efficiency)**: "M. Willi" may be "M. Willis"; check the full author list and year.
- **Refs. 3, 4, 8, 11, 12 (Hoffmann; Kaplan; Muennighoff; Vaswani; Varma)** use "et al." — Springer requires full author lists before submission.
- **All entries** are missing volume/page/DOI details that Springer production will request (e.g., Lee et al., ACL 2022, pp. 1935–1952; arXiv DOIs for the preprint-only entries). The list is already in a consistent numbered style, so completing the details is the remaining work.

**3. Cox model details (Methods 3.4 + Appendix A).** I added the specification exactly as implemented in the archived pipeline (strata = coverage 35/55/85; binary covariate blocked R∈{2,4,8} vs R=1; Breslow ties; Newton–Raphson; Wald CI; pure-NumPy implementation) plus a `[TODO-AUTHOR: confirm … against the analysis code]`. Please confirm each detail against the final repository copy before removing the TODO.

**4. TOST margin (Methods 3.4).** Choose and justify the equivalence margin as a ratio (e.g., ±25%) on substantive grounds, or state explicitly that no equivalence claim is made. The margin must be argued before looking at the results, and the argument written into the paper.

**5. MemTime maximum (Sect. 4.1).** The TODO asks you to report the maximum MemTime over all 135 runs from runs.csv. For your information: the archived runs.csv shows a maximum of **exactly 500** (value counts: 58×100, 62×200, 10×300, 5×500; the 85%/R=8/blocked cell has all five seeds at exactly 500). If you confirm this against the final data, the original stronger sentence "never exceeds 500 steps" is in fact supported and may be restored.

## High — figures

**6. Kaplan–Meier figures and the budget line (Figs. 4–5).** Captions were reworded to remove "the dashed line marks the 20,000-step budget" + a TODO was added. The archived figure script draws no such line (only step curves and censoring ticks, with the x-axis extended to 20,500). Either confirm the line is drawn and restore the clause, or keep the reworded captions. Do not ship the TODO into submission.

**7. Visual defects you listed, to fix in the figure files:**
- Fig. 2: clipped panel letters.
- Fig. 1c: the overlapping "5/5 3/5" censored-run labels.
- Fig. 3a: legend overlapping the curves.
- Fig. 3b: overlapping x-tick labels, and the "Spearman rho" annotation colliding with data points.

## Medium — framing and positioning

**8. Title.** Current title kept as instructed. Alternatives that include the matched-dose qualifier and "within-epoch repetition":
- "Coverage versus within-epoch repetition at matched dose in transformer grokking"
- "Data coverage, not within-epoch repetition, gates grokking at matched per-example dose"
- "Unique coverage gates generalization in transformer grokking: within-epoch repetition shows no detectable effect at matched dose"

**9. Removed "[SUGGESTED …]" citation candidates (Related Work, Positioning).** Optional, verify before adding any:
- A dedicated study of critical data fractions in grokking, if one exists — none was confirmed during revision.
- "How much can language models memorize?" (arXiv:2505.24832, 2025) — verify authors and venue.
- "Data mixing laws" (Ye et al., arXiv:2403.16952, 2024) — addresses mixture composition rather than repetition; probably not needed.
Do not add any of these without checking the original papers.

**10. Declarations to complete (all marked `[TODO-AUTHOR]` in the text):** funding; competing interests; data-repository DOI/URL and the sentence "The repository is public at the time of submission" (add only if true); code-repository DOI/URL and the same sentence; the AI-tool inventory (list every AI tool used at any stage — code generation, analysis scripts, prompt-assisted revision, language editing — and what each did); re-run of the archived pipeline to confirm it reproduces every reported statistic on the final data.

**11. Deviation log (Appendix B).** Verify items (iii), (iv), and (v) against the internal design document and extend the log if further deviations are found; the published description of the families must match this log. Also verify the affiliation note in the LaTeX comment above the author block (school/department and postal code within Dalian University of Technology, if the NPL title page requires them).

## Lower priority

**12. Weight-norm pre-specification status (informational).** The internal design document lists WeightNorm as outcome 4 with exploratory hypothesis H4 (higher R → higher steady-state norm) and planned exploratory analyses (Spearman with GrokTime; monotone trend across R). This supports the Fig. 3 caption and Methods 3.4 wording "pre-specified exploratory outcome", which I therefore kept; the mode contrast and the step-1,000 norm comparisons are not in the design document and are described as exploratory only. Please verify this reading against the design document; if in doubt, downgrade the caption to "(exploratory outcome)".

**13. Family 3 point estimate vs table medians (informational, no action required).** The extreme-contrast median difference −75.5 pp is the pipeline's exact value (medians 21.2% and 96.6% are themselves rounded to one decimal; 21.2 − 96.6 = −75.4). A reviewer cross-checking the table may notice the 0.1 discrepancy; it is a rounding artifact, and the CI [−78.8, −72.2] is unaffected.

**14. Verified clean — no action needed.** No "AI generated" watermark text exists in the source; cross-references (Sect./Fig./Table/Appendix) all point to the right targets; all repeated numbers (83 grokked runs, 3 of 35, 8,400 vs 1,800, −6,600 [−11,600, −4,000], Holm-adjusted p 0.016/0.048/0.024/0.032, RMST values, Fisher/Clopper–Pearson values, Cox 0.96 [0.48, 1.94], TOST margins 1.21–1.87, "one of twelve" at ±25%, 80% power at ratio ≈ 2, rank-biserial signs, and the 55%-blocked log-rank range 0.47–0.67) are identical everywhere they appear and match the archived pipeline outputs, except the two items in action 1 above.
