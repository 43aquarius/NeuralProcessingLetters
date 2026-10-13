# Part C — Final Text Pass: Remaining Author Actions (ranked)

## 1. References (flag-only; nothing changed)
- **Ref. 14** (Zhang et al., *Understanding deep learning requires rethinking generalization*): fourth author appears as "O. Recht" — likely a typo for **B. Recht**. Check the original paper.
- **Ref. 9** (Nanda et al., *Progress measures for grokking via mechanistic interpretability*) and **Ref. 12** (Varma et al., *Explaining grokking through circuit efficiency*): author lists and years need verification against the actual papers ("J. Lindsey" and "M. Willi" in particular).
- Replace "et al." with full author lists (Springer style): refs. Hoffmann (3), Kaplan (4), Muennighoff (8), Vaswani (11), Varma (12).
- Add volume, pages, and DOIs for all entries (e.g., Lee et al., ACL 2022, pp. 1935–1952; arXiv DOIs for preprint-only entries).

## 2. Figure defects to fix in the files
- Fig. 2: clipped panel letters.
- Fig. 1c: overlapping "5/5 3/5" censored-run labels.
- Fig. 3a: legend overlapping the curves.
- Fig. 3b: overlapping x-tick labels and the "Spearman rho" annotation colliding with data.

## 3. Reproducibility and deposit
- Re-run the archived pipeline on the final data and confirm it reproduces every reported number (TODO retained in Methods 3.4).
- Deposit code and data in a public repository; fill in the two DOI TODOs (Data/Code availability). The sentence "The repository is public at the time of submission" is stored inside those TODOs — add it only if true at submission.

## 4. TOST TODO (Methods 3.4)
List the margins actually run and confirm no equivalence claim is made. For your reference: the archived pipeline was run with margins 0.10, 0.25, 0.50 (i.e., ratio bands 1.10, 1.25, 1.50) — confirm against your final run configuration and delete the TODO once recorded.

## 5. MemTime maximum (Sect. 4.1, wording now asserts "never exceeds 500")
Verify the maximum MemTime (500) in runs.csv before submission. For your reference: the archived runs.csv shows max = exactly 500 (value counts 58×100, 62×200, 10×300, 5×500; the 85%/R=8/blocked cell has all five seeds at exactly 500), so the sentence is supported by the archived data.

## 6. Weight-norm H4 TODO (Methods 3.4)
Confirm the internal design document lists the weight norm as exploratory outcome H4 (it does in the archived STUDY_DESIGN.md — outcome 4, hypothesis H4, plus planned exploratory Spearman/trend analyses), then delete the TODO. The "pre-specified exploratory outcome" wording in Methods and the Fig. 3 caption rests on this.

## 7. Title decision
Choose between the current title and the three alternatives now listed in a LaTeX comment above `\title`. Remove the comment (and the unused titles) before submission.

## 8. p-value bounds in Sect. 4.3 (rounding subtleties)
- New mode log-rank bound "all $p \geq 0.32$": the strict archived minimum is 0.31731 (C55 R8 blocked-vs-interleaved 0.39683 is the next). 0.317 rounds to 0.32 at two decimals, so the statement is true only under that rounding convention. If you want strictly true bounds, use "all $p \geq 0.31$" or "all $p \geq 0.317$".
- Exact-rank bound "all $p \geq 0.24$" (same sentence): the archived minimum is 0.2381, which is **strictly below 0.24** (it rounds to 0.24). I did not change it (rule 1). Suggest "all $p \geq 0.238$" or "all $p > 0.2$" if you want strict truth.

## 9. −75.5 vs table medians (task 10 instruction: report, do not change)
The extreme contrast in Sect. 4.4 is reported as −75.5 percentage points, but Table 2's rounded medians give 21.2 − 96.6 = −75.4. The −75.5 comes from the unrounded medians (pipeline exact value −0.7548). Text unchanged; anticipate a reviewer query — a one-line footnote ("computed from unrounded medians") would pre-empt it.

## 10. "Single percentage points" in the last sentence of Sect. 4.4
"repetition shifts sub-critical accuracy by single percentage points" — the shift is 7.8–8.3 pp, i.e., single-digit percentage points. The current phrase could be misread as "one percentage point". Not changed (number-adjacent wording); consider "by single-digit percentage points".

## 11. Reviewed-but-kept borderline sentences (for your awareness)
- Discussion, speculative ¶: "at matched step budget, uniform repetition behaves like training on the unique subset" — kept because the paragraph is labeled speculative and introduced by "The results are compatible with…". Soften further only if you wish.
- Abstract "it delays memorization" vs Introduction "it slightly delays memorization" — optional to align (Abstract could take "slightly").

## 12. Export and template conversion
- Export a clean PDF without any "AI generated" mark (verified: none in the current source or PDF text layer; re-check after any export tool is used).
- Convert to the Springer Nature template (sn-jnl.cls) and check the current NPL author guidelines (reference style, title-page format, declarations layout, and whether school/postal code are needed — see also the LaTeX comment above the author block).
- Remaining TODOs to resolve before submission: funding; competing interests; data and code DOIs; AI-tool inventory; Cox-specification confirmation; gradient-noise reference (or keep as explicit hypothesis); pipeline re-run confirmation; deviation-log verification (items iii–v); affiliation details.
