# Part C — Final Decisions Pass: Remaining Author Actions (ranked)

## 1. Confirm the five applied decisions (placeholders arrived unfilled)
The MY DECISIONS fields in your instruction were empty, so I applied the values established in this project (each verified, each a one-line revert in `main.tex` or `main_backup_round4.tex`):
- **Title** = alternative (1), "Coverage versus within-epoch repetition at matched dose in transformer grokking" (your template's example). Alternatives (2)/(3) remain in a comment above `\title`.
- **Weight norm** = "H4 CONFIRMED" (the archived `STUDY_DESIGN.md` lists WeightNorm as outcome 4 and H4 as an explicitly exploratory hypothesis) → "pre-specified exploratory outcome" kept, its TODO deleted. If you do not want the internal document to serve as the pre-specification basis, revert and switch to "exploratory outcome".
- **Gradient noise** = KEEP as explicit hypothesis (no citation supplied) → now reads "we hypothesize". You may still add a reference later; nothing else in the sentence changed.
- **TOST margins** = ±10%, ±25%, ±50% (ratios 1.10/1.25/1.50), inserted in Methods 3.4 and Sect. 4.2; "no equivalence claim is made at any margin" retained. Confirm this matches your final run configuration.
- **Max MemTime** = 500 (re-verified in runs.csv: 58×100, 62×200, 10×300, 5×500; the five 500s are all seeds of 85%/R8/blocked) → "never exceeds 500 steps (median 200)" stands.

## 2. Abstract length
≈254 words (LaTeX-stripped) / 255 (PDF text layer) — marginally above the usual NPL limit of 250. Trim 5–10 words or confirm the limit in the current author guidelines. Candidate trims: "manipulated in a partially crossed design" parenthetical or the MemTime clause.

## 3. References (flag-only; nothing changed)
- **Ref. 14** (Zhang et al.): fourth author "O. Recht" is likely a typo for **B. Recht**.
- **Refs. 9 and 12** (Nanda et al.; Varma et al.): verify author lists and years ("J. Lindsey", "M. Willi" in particular).
- Replace "et al." with full author lists (Springer style): Hoffmann (3), Kaplan (4), Muennighoff (8), Vaswani (11), Varma (12).
- Add volume, pages, and DOIs for all entries (arXiv DOIs for preprint-only entries).

## 4. p-value bound refinements in Sect. 4.3 (rounding subtleties; unchanged per rule 1)
- Exact-rank bound "all $p \geq 0.24$": strict archived minimum **0.2381** (below 0.24; rounds to 0.24). If you want strict truth: "all $p \geq 0.238$" or "all $p > 0.2$".
- Mode log-rank "all $p \geq 0.32$": under the declared **permutation** log-rank tests the mode-family minimum is **0.397** (C55 R8), so the statement is true but conservative — you could tighten it to 0.39. (The 0.31731 cited in the previous action list is the asymptotic $\chi^2$ p for C35/R2, whose permutation p is 1.0.)
- Within-interleaved "log-rank $p \geq 0.32$": strict permutation minimum **0.31746** (C55 interleaved R1 vs R4) — holds only under two-decimal rounding; strictly true would be "$p \geq 0.31$".

## 5. −75.5 vs table medians (Sect. 4.4; task 6 — footnote NOT added)
The suggested wording "75.5 is the median of the paired differences" is **not confirmable**: the pipeline's median difference is the difference of the unrounded condition medians (0.211587 − 0.966387 = −0.7548 → −75.5), the median of seed-paired differences would be −76.0, and the table's one-decimal medians give 21.2 − 96.6 = −75.4. If you want a pre-empting parenthetical, the correct one is: "(the medians rounded to one decimal in Table~\ref{tab:descriptives} give 75.4; $-75.5$ is the difference of the unrounded medians)".

## 6. Figure defects to fix in the files (carried)
- Fig. 2: clipped panel letters.
- Fig. 1c: overlapping "5/5 3/5" censored-run labels.
- Fig. 3a: legend overlapping the curves.
- Fig. 3b: overlapping x-tick labels and the "Spearman rho" annotation colliding with data.

## 7. Reproducibility and deposit (carried; TODOs retained in the manuscript)
- Re-run the archived pipeline on the final data and confirm it reproduces every reported number (TODO in Methods 3.4).
- Deposit code and data in public repositories; fill the two DOI TODOs (Data/Code availability). The sentence "The repository is public at the time of submission" is stored inside those TODOs — add it only if true at submission.

## 8. Housekeeping before submission
- Delete the alternatives comment above `\title` (alternatives 2–3 are retained there for now).
- Resolve the school/postal-code comment above the author block if the NPL title page requires them.
- Remaining TODOs: funding; competing interests; data DOI; code DOI; AI-tool inventory (Springer disclosure policy); Cox-specification confirmation; pipeline re-run; deviation-log verification (items iii–v).
- Wording you may still want to touch (flagged, unchanged): "single percentage points" in the last sentence of Sect. 4.4 (the shift is 7.8–8.3 pp — consider "single-digit percentage points"); optionally align Abstract "it delays memorization" with the Intro's "slightly delays".

## 9. Estimator precision note (for your awareness; no manuscript change)
The wnorm@1000 point estimates in Sect. 4.5 ("median differences are at most 0.7"; the "+0.53" exception) are medians of **seed-paired differences** (`task_secondary.py`: `d = x − y`), while their 90% CIs bootstrap the **difference of medians**, and the CSV note says "difference of medians". The quoted values match the pipeline output and "at most 0.7" holds under either estimator (max 0.656 paired; 0.599 difference-of-medians), but if a reviewer probes the estimator, consider aligning the pipeline note or describing it precisely.

## 10. Export and template conversion (carried)
- Export a clean PDF without any "AI generated" mark (verified: none in the current source or PDF text layer; re-check after any export tool is used).
- Convert to the Springer Nature template (sn-jnl.cls) and check the current NPL author guidelines (reference style, title-page format, declarations layout, abstract word limit).
