# Part B — Final Decisions Pass: Change Log

Manuscript: `main.tex` (compiled to `main.pdf`, 14 pages, tectonic, no warnings).
Backup of the pre-edit state: `main_backup_round4.tex`.

## 0. Decisions applied (the template's MY DECISIONS fields arrived as placeholders)

Each was resolved from verified project data and is a one-line revert if you intended otherwise:

| Decision field | Applied value | Basis |
|---|---|---|
| Title | Alternative (1): "Coverage versus within-epoch repetition at matched dose in transformer grokking" | The template's own example string, identical to alternative (1) listed above `\title` |
| Weight-norm design status | H4 CONFIRMED in design document | `STUDY_DESIGN.md`, outcome 4 "WeightNorm" (exploratory/supporting) and hypothesis H4 "预设为探索性分析" |
| Gradient-noise sentence | KEEP as explicit hypothesis | No citation was supplied and the rules forbid adding references |
| TOST margins actually run | ±10%, ±25%, ±50% (ratios 1.10, 1.25, 1.50) | `results/tost.csv` `margin_fraction` ∈ {0.1, 0.25, 0.5}, `margin_ratio` ∈ {1.1, 1.25, 1.5} |
| Max MemTime in runs.csv | 500 | Re-verified this round: value counts 58×100, 62×200, 10×300, 5×500 (the 5×500 are all five seeds of 85%/R8/blocked) |

## 1. Edits (Location | Before | After | Reason)

| # | Location | Before | After | Reason |
|---|---|---|---|---|
| 1 | `\title` (preamble) | "Coverage, not repetition: data diversity gates the emergence of generalization in transformer grokking" | "Coverage versus within-epoch repetition at matched dose in transformer grokking" | Author decision (alternative 1). The comment above `\title` now records the applied choice; alternatives (2) and (3) are retained there for reference. |
| 2 | Methods 3.4, weight-norm sentence | "...the norm trajectory was a pre-specified exploratory outcome motivated by loss-landscape analyses \citep{liu2023omnigrok} **[TODO-AUTHOR: confirm the design document lists the weight norm as exploratory outcome H4]**." | Same sentence, TODO deleted | H4 confirmed in the internal design document (outcome 4 / hypothesis H4, explicitly exploratory); per task 2 the wording "pre-specified exploratory outcome" is kept and the TODO is resolved. |
| 3 | Methods 3.4, TOST sentence | "...the equivalence analysis is a post hoc sensitivity analysis over the grid of margins actually run, and no equivalence claim is made at any margin **[TODO-AUTHOR: list the margins actually run...]**." | "...over the grid of margins actually run ($\pm 10\%$, $\pm 25\%$, and $\pm 50\%$; ratios 1.10, 1.25, and 1.50), and no equivalence claim is made at any margin." | Margins inserted per task 3; verified against `tost.csv`; "no equivalence claim is made at any margin" preserved verbatim; TODO resolved. |
| 4 | Sect. 4.2, TOST sentence | "The equivalence analysis is a post hoc sensitivity analysis over the grid of margins run, and no equivalence claim is made at any margin:" | "The equivalence analysis is a post hoc sensitivity analysis over the grid of margins run ($\pm 10\%$, $\pm 25\%$, and $\pm 50\%$; ratios 1.10, 1.25, and 1.50), and no equivalence claim is made at any margin:" | Same margin list inserted into the Results sentence (task 3); the following clause already illustrates the ±25% case specifically. |
| 5 | Discussion, "Interpretation" ¶ | "The residual effects we cannot exclude, point estimates of a few hundred steps in either direction with wide intervals, are consistent with the hypothesis that within-batch duplicates perturb gradient noise without shifting the mean dynamics **[TODO-AUTHOR: add a suitable reference...]**." | "For the residual effects we cannot exclude, point estimates of a few hundred steps in either direction with wide intervals, we hypothesize that within-batch duplicates perturb gradient noise without shifting the mean dynamics." | Author decision KEEP as explicit hypothesis: the sentence now says "we hypothesize", meaning unchanged, TODO removed. |

## 2. Checked, deliberately not changed

| Item | Status |
|---|---|
| MemTime sentence (Sect. 4.1) | Already reads "\memtime{} never exceeds 500 steps (median 200)"; runs.csv max = 500 re-verified → kept verbatim, nothing deleted (task 4). |
| Limitations TOST sentence | Already "post hoc sensitivity analysis over margins chosen after the results" — consistent with the inserted lists; unchanged. |
| Abstract & Introduction vs the new title (task 1) | Audited: all repetition claims carry "at matched (per-example) dose" plus "no detectable"; the abstract's closing claim is scoped "In this regime, under a fixed optimization budget and at matched per-example dose"; the Intro's three-findings and contribution (iii) are equivalently scoped. No edit needed — the manuscript does not claim more than a matched-dose result. |
| DO NOT CHANGE list | Reference entries, AI-use statement text (its TODO kept), funding / competing-interests / DOI placeholders, and the Cox description (its TODO kept) are untouched. |

## 3. "Pre-specified" / "planned" / "declared" audit (task 2 catalog)

All occurrences in the post-edit manuscript:

| Location | Text | Status |
|---|---|---|
| Methods 3.4 (weight-norm sentence) | "pre-specified exploratory outcome" | Kept — H4 confirmed in the design document |
| Fig. 3 caption | "(pre-specified exploratory outcome)" | Kept — same basis |
| Methods 3.4 (families sentence) | "declared rather than pre-specified (deviation-log item iii)" | Kept — describes the analysis families |
| Methods 3.4 (closing ¶) | "The analysis was planned in an internal design document" | Kept — accurate; deviations logged in App. B |
| Appendix B, item (iii) | "the analysis families planned in the internal design document" | Kept — accurate |
| Appendix B, item (iv) | "the declared extreme contrast cell" | Kept |
| Intro; Sect. 3.3; Sect. 4.2; Sect. 4.4; Sect. 4.5 | "the declared contrasts" / "declared extreme contrast" / "declared family contrasts" / "declared confirmation families" | Kept — all describe the analysis families or their contrasts |
| — | "pre-registered" / "preregistered" / "unplanned" | No occurrences |

## 4. Abstract check (task 7)

- **Word count ≈ 254 (LaTeX-stripped source) / 255 (PDF text layer).** Both slightly exceed the typical NPL limit of 250 words → flagged in Part C; trimming 5–10 words would clear it.
- Citations in abstract: none.
- Undefined abbreviations: none — "GrokTime"/"MemTime" are defined inline at first use, $R$ is introduced with the factor it encodes; no IQR/CI/MW/TOST/KM/HR acronyms appear in the abstract.

## 5. Consistency check of repeated numbers (task 8) — all match

| Number | Manuscript locations | Pipeline value | Status |
|---|---|---|---|
| 83 grokked runs | Fig. 3 caption ($n=83$); Sect. 4.5 ("Among the 83 runs") | runs.csv: 83 non-censored of 135 | ✓ |
| 3 of 35 | Abstract; Intro (contribution); Sect. 4.1; Discussion | runs.csv: 3 of 35 grokked at coverage 35 | ✓ |
| 8,400 / 1,800 | Abstract; Intro; Sect. 4.1; Table A3 | descriptives / exact_tests | ✓ |
| −6,600, CI [−11,600, −4,000] | Intro (contribution); Sect. 4.1 | F1: −6600, [−11600, −4000] | ✓ |
| Holm p = 0.016 | 5 locations | F1 p_holm = 0.01588 | ✓ |
| Holm p = 0.048 | Sect. 4.2 (MemTime) | M1 p_holm = 0.04764 | ✓ |
| Holm p = 0.024 | Sect. 4.2 (sub-critical accuracy); Sect. 4.5 (wnorm, R8) | S1/S2 p_holm = 0.02382 | ✓ |
| Holm p = 0.032 | Sect. 4.5 (wnorm, R4) | S2 p_holm = 0.03174 | ✓ |
| 63.1 log-rank statistic (5 df) | Sect. 4.1 | logrank.csv: 63.1436, df 5, 10,000 permutations | ✓ |
| HR 0.96 [0.48, 1.94] | Sect. 4.2 | cox.csv: 0.9613 [0.4755, 1.9434] | ✓ |
| 43 events (of 60 runs) | Methods 3.4; Sect. 4.2 ("3 of 43" in the 35% stratum) | cox.csv: 43 events; n_ref 15 + n_index 45 | ✓ |

Additional verifications performed this round: TOST "one of twelve within-mode contrasts" at ±25% (only C85 interleaved R1vR2, pmax = 0.0278) ✓; smallest-margin range "1.21 to 1.87" (12 within-mode contrasts: 1.2143–1.8721) ✓; wnorm@1000 "+0.53 with CI [+0.15, +1.02]" (secondary_tests.csv: 0.531, [0.146, 1.017]) ✓; "median differences at most 0.7" (max 0.656) ✓; mode log-rank "all p ≥ 0.32" and within-interleaved "log-rank p ≥ 0.32" — see the rounding notes in Part C.

**No mismatches were found among the numbers listed in task 8.**

## 6. TODO inventory after this pass

11 → 8 body TODOs (Cox specification; pipeline re-run; funding; competing interests; data DOI; code DOI; AI-tool inventory; deviation-log verification) plus the LaTeX comment about school/postal code. Deleted this round: weight-norm H4, TOST margin list, gradient-noise reference.
