# Part B — Revision Log (Round 2: statistical pipeline integration)

Manuscript: `main.tex` — *Coverage, not repetition: data diversity gates the emergence of generalization in transformer grokking*
Target journal: Neural Processing Letters (Springer).
Round 2 incorporates the recomputed statistics from the exact, reproducible pipeline in `../grokking-stats/` (`analyze.py`, runs 2026-10-11; sanity checks 26/26 PASS) and the author information provided on 2026-10-12. Every value below is traceable to `grokking-stats/results/results_report.md` and its CSV tables.

## B.1 Author and declarations

| # | Location | Change |
|---|----------|--------|
| 1 | Title page | Author block filled: **Chang Tan**, Dalian University of Technology, Dalian, China; corresponding email **aquars43@foxmail.com** (sole author; sole and corresponding author). A LaTeX comment notes that school/department and postal code may be added if the NPL title-page format requires them. |
| 2 | Declarations — Ethics | Stated: purely computational study, no human/animal subjects, no approval or consent required (was TODO). |
| 3 | Declarations — Author contributions | CRediT-style single-author statement added (was TODO). |
| 4 | Declarations — Generative AI use | Honest draft added: GLM assistant (Z.ai) used as programming/writing aid under the author's direction; author takes full responsibility. Kept a confirmation TODO (Springer Nature policy). |
| 5 | Declarations — Data/Code availability | Expanded to name the concrete artifacts (135 per-run JSON logs, `runs.csv`, `history.csv`, analysis outputs, full pipeline). DOI/URL still TODO. |

## B.2 Corrected statistics (old draft value → recomputed value)

Cause: (a) scipy's `mannwhitneyu` silently substitutes the asymptotic tie-corrected method when ties are present — several p-values labelled "exact" were asymptotic; (b) the archived bootstrap resampled only ONE group, making every median-difference CI too narrow (the archived code reproduces every draft CI byte-for-byte, confirming the diagnosis); (c) sign convention unified.

| # | Quantity | Old (draft) | New (manuscript) | Source table |
|---|----------|-------------|------------------|--------------|
| 6 | 85 vs 45 GrokTime MW p | 0.008 ("exact") | 0.008 (= 2/252 exact) | exact_tests |
| 7 | 85 vs 25 GrokTime MW p | 0.0075 (asymptotic, mislabelled exact) | **0.0079** (exact; 2/252) | exact_tests |
| 8 | Family 1 Holm p | 0.015 | **0.016** (0.01588) | exact_tests |
| 9 | 85 vs 45 median-diff CI | [-6,900, -6,000] | **[-11,600, -4,000]** | exact_tests |
| 10 | Family 2 p-values (55: R1vR4 / R1vR8; 85: R1vR4 / R1vR8) | 0.68 / 0.83 / 0.67 / 0.53 (asymptotic) | **0.65 / 0.79 / 0.67 / 0.56** (exact) | exact_tests |
| 11 | Family 2 CIs (same order) | [-1,200, 2,600]; [-1,600, 1,500]; [-200, 500]; [-300, 400] | **[-2,600, +2,000]; [-1,500, +2,600]; [-500, +700]; [-400, +700]** (two-group bootstrap) | exact_tests |
| 12 | Sec 4.2 bounds (85, R8) | "17% earlier / 22% later" | **"22% earlier / 39% later"** (wider CI) | derived |
| 13 | Sec 4.2 bounds (55) | "about one third" | **"one third earlier / one half later"** | derived |
| 14 | Mode contrast CI (55, R2, +700) | [-400, 4,300] | **[-5,300, +4,300]** | exact_tests |
| 15 | Family 3 extreme-contrast p / Holm p | 0.012 / 0.021 (asymptotic; Holm over 2 contrasts) | **0.0079 / 0.0079** (exact; single-contrast family) | exact_tests |
| 16 | Family 3 CI | [-77.2, -72.2] pp | **[-78.8, -72.2] pp** | exact_tests |
| 17 | Rank-biserial sign convention | inconsistent (-1.0 in some places, +1.0 in others) | unified: r = 1 - 2U1/(n1n2), U1 = first-named-larger pairs; r = +1 means first-named entirely smaller; declared in Methods | exact_tests |
| 18 | Median-difference sign convention | second-minus-first (opposite of wording) | first-named minus second-named, matching the wording | exact_tests |
| 19 | Median-diff permutation sensitivity (p=0.051 / 0.168) | reported | **removed** — superseded by Kaplan-Meier / log-rank / RMST (the censoring-aware analyses the earlier TODO requested) | logrank, rmst |
| 20 | MemTime R1-vs-R8 p (35/55/85) | not tested (descriptive only) | **exact p = 0.008 each, Holm 0.048; JT trend Holm p ≤ 0.0003** (exploratory) | secondary_tests |
| 21 | 25% sub-critical acc R1 vs R4/R8 | "not tested" (TODO) | **p = 0.008, Holm 0.024; diff 8.3 pp, CI [4.5, 11.3]; 53→86 of 397 correct** | secondary_tests |
| 22 | wnorm@1000 "statistically indistinguishable" | claimed | **replaced with equivalence-style summary** (max median diff 0.7; 5 of 6 90% CIs include 0; exception +0.53 [0.15, 1.02]) | secondary_tests |
| 23 | Spearman norm vs GrokTime p | 0.56 (asymptotic) | **0.55 (permutation)**; stratified rho added (-0.60 at 85%, +0.29 at 55%) with stopping-time caveat | secondary_tests |
| 24 | C25 final L2 norm tests | p=0.016 / 0.008 (unadjusted) | same values, now with **Holm-adjusted 0.032 / 0.024**; blocked-vs-interleaved R8 added (p=0.032) | secondary_tests |

## B.3 New analyses added (absent from the previous draft)

| # | Analysis | Where | Key numbers |
|---|----------|-------|------------|
| 25 | Kaplan-Meier estimates | New Fig. 4 (R=1 by coverage) + Fig. 5 (repetition arms, Appendix D) | — |
| 26 | Permutation log-rank tests | Sec 4.1-4.4 | 85v45: p=0.008; 85v25: p=0.008; 6-coverage joint: chi2=63.1, df=5, p<1e-4; all repetition/mode contrasts ns (p ≥ 0.32) |
| 27 | RMST (horizon 20,000) | Sec 4.1, 4.2, 4.3 | 1,920 (85) / 2,660 (70) / 4,340 (55) / 8,900 (45) / 18,360 (35) / 20,000 (25); R1-vs-R8 blocked: +280 [-1,260, +1,700] (55), +160 [-200, +520] (85) |
| 28 | Stratified Cox model | Sec 4.2 | HR 0.96 [0.48, 1.94], Breslow ties, coverage strata; fragility caveat (3/43 events in 35% stratum) |
| 29 | Fisher exact + Clopper-Pearson | Sec 4.4 | 25%: 0/5 per cell, CP 95% CI [0, 0.52]; 35%: all p ≥ 0.44 |
| 30 | TOST equivalence testing | Sec 4.2 + Methods | At ±25% margin 1 of 12 within-mode contrasts reaches equivalence; smallest declarable margins 1.21-1.87; 80% power only for ~2x ratios. Margin choice left as [TODO-AUTHOR] by design |
| 31 | TOST power/MDE simulation | Sec 4.2 + Limitations | 80% power at true ratio ≥ ~1.995 (observed pooled SD, log10 scale) |

## B.4 Methods / Appendix updates

| # | Location | Change |
|---|----------|--------|
| 32 | Methods (Sect. 3.4) | Rewritten: exact permutation MW (252 assignments, midranks), declared families ("differ from the internal plan... declared rather than pre-specified"), sign conventions, survival analyses, Fisher/CP, exploratory secondary families, TOST, seed statement (20260922 + offsets), pipeline reproducibility statement. Removed the four statistical TODOs (all resolved). |
| 33 | Appendix A, Statistical software | Rewritten to describe the pipeline (was: scipy-based description with the silent-switch caveat). |
| 34 | Appendix B, deviation log | Added item (v): the exact-test replacement and the two-group bootstrap recomputation; no data/stopping-rule/family changes. TODO updated to verify items (iii)-(v). |
| 35 | Appendix D | New: KM estimates for the repetition arms (Fig. 5). |
| 36 | Limitations | Third limitation rewritten: equivalence tests now exist but are conditional on a post-hoc margin; design separates only ~2x effects at defensible margins. |

## B.5 Wording and consistency

| # | Change |
|---|--------|
| 37 | "pre-specified contrasts" → "declared family contrasts" / "declared extreme contrast" wherever the families were chosen post hoc (consistent with deviation-log item iii). The R=1 coverage-arm contrasts remain describable as pre-specified in spirit, but the text no longer claims it. |
| 38 | Abstract / Introduction / Contribution updated with the corrected p-values, the log-rank agreement, and the corrected CI. |
| 39 | "statistically indistinguishable" (wnorm@1000) → equivalence-style summary (see item 22). |
| 40 | Kept all 2 [SUGGESTED - AUTHOR MUST VERIFY] citation slots unchanged. |

No numbers were changed anywhere without a recomputed source; nothing was silently overwritten — every change above is logged here.
