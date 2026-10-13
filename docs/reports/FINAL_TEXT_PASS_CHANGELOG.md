# Part B — Final Text Pass: Change Log

Location | Before | After | Reason

| # | Location | Before | After | Reason |
|---|----------|--------|-------|--------|
| 1 | Preamble (above `\title`) | (nothing) | LaTeX comment listing three alternative titles | Task 7. Current title kept; alternatives: (1) "Coverage versus within-epoch repetition at matched dose in transformer grokking"; (2) "Data coverage, not within-epoch repetition, gates grokking at matched per-example dose"; (3) "Unique coverage gates generalization in transformer grokking: within-epoch repetition shows no detectable effect at matched dose" |
| 2 | **Sect. 4.3** | "as are the corresponding permutation log-rank tests (all $p \geq 0.40$)" | "(all $p \geq 0.32$)" | Task 1 (exact value given). Archived values below 0.40 were 0.317 and 0.397. Note: 0.317 is the strict minimum and rounds to 0.32 at two decimals — see Part C item 8. |
| 3 | **Sect. 4.1** | "median \memtime{} is at most 500 steps in every condition (overall median 200 [TODO-AUTHOR: report the maximum MemTime over all 135 runs from runs.csv])" | "\memtime{} never exceeds 500 steps (median 200)" | Task 2 (exact replacement given); TODO deleted. Part C carries the verification item. |
| 4 | **Fig. 4 caption** | "…(Appendix~\ref{app:kmrep}). [TODO-AUTHOR: confirm whether the Kaplan–Meier figures (this figure and Fig.~\ref{fig:kmrep}) draw a dashed line at the 20,000-step budget; …]" | "…(Appendix~\ref{app:kmrep})." | Task 3. TODO deleted; caption wording otherwise kept. Fig. 1c's "the dashed line is the budget" left untouched (line is drawn there). |
| 5 | **Conclusion** | "…rather than by repeated exposure at matched per-example dose. At matched per-example dose, repetition, whether temporally clustered or uniformly spread, showed no detectable effect… and did not rescue sub-critical coverage within the $20{,}000$-step budget; it did leave…" | "…rather than by repeated exposure: at matched per-example dose, repetition, whether temporally clustered or uniformly spread, showed no detectable effect… and did not detectably rescue sub-critical coverage within the $20{,}000$-step budget; it did leave…" | Task 4: "at matched per-example dose" in two adjacent sentences did not read naturally, so the sentences were merged with a colon (qualifier kept exactly once, meaning unchanged). Task 9: "did not rescue" → "did not detectably rescue" (one-word hedge, aligning with the new Sect. 4.4 title). |
| 6 | **Appendix B, item (iii)** | "(iii) the pre-specified analysis families refer to…" | "(iii) the analysis families planned in the internal design document refer to…" | Task 5 (exact replacement given). |
| 7 | **Appendix B, item (iv)** | "the pre-specified extreme contrast cell (25\%, $R=8$)" | "the declared extreme contrast cell (25\%, $R=8$)" | Task 5 (exact replacement given). |
| 8 | **Methods 3.4 (outcomes)** | "…motivated by loss-landscape analyses \citep{liu2023omnigrok}." | "…\citep{liu2023omnigrok} [TODO-AUTHOR: confirm the design document lists the weight norm as exploratory outcome H4]." | Task 5. The wording "pre-specified exploratory outcome" itself kept (Methods 3.4 and Fig. 3 caption); the confirmation TODO is added once, in Methods, where the claim is made. |
| 9 | **Methods 3.4 (TOST)** | "…with the margin expressed as a ratio; no margin was pre-specified, so any equivalence statement is conditional on a margin chosen on substantive grounds and defended in print [TODO-AUTHOR: choose and justify the TOST margin as a ratio (e.g. ±25% of median GrokTime), or state explicitly that no equivalence claim is made]." | "…with the margin expressed as a ratio. The margins were not chosen before the results were seen, so the equivalence analysis is a post hoc sensitivity analysis over the grid of margins actually run, and no equivalence claim is made at any margin [TODO-AUTHOR: list the margins actually run and confirm that no equivalence claim is made]." | Task 8 (exact TODO wording given). Same facts (no pre-specification), now framed as post hoc sensitivity analysis; no numbers changed. |
| 10 | **Sect. 4.2 (TOST sentence)** | "Equivalence is not demonstrable at tight margins: on $\log_{10}$ \groktime{} in the uncensored cells, TOST at a $\pm 25\%$ margin (ratio 1.25) reaches it for one of twelve within-mode contrasts, …" | "The equivalence analysis is a post hoc sensitivity analysis over the grid of margins run, and no equivalence claim is made at any margin: on $\log_{10}$ \groktime{} in the uncensored cells, TOST at a $\pm 25\%$ margin (ratio 1.25) would declare equivalence for one of twelve within-mode contrasts, …" | Task 8. All numbers unchanged (1.25; one of twelve; 1.21–1.87; 80\% power; ratio ≈ two); only the framing and the subjunctive "would declare" (consistent with no claim being made). |
| 11 | **Limitations (third)** | "…and the equivalence tests are conditional on a margin that was not pre-specified (at defensible margins the design separates only effects of roughly twofold or larger), so…" | "…and the equivalence analysis is a post hoc sensitivity analysis over margins chosen after the results (at defensible margins the design separates only effects of roughly twofold or larger), so…" | Task 8. Parenthetical and the closing "bounded but not equivalence-demonstrating" kept. |
| 12 | **Sect. 4.4 title** | "Below the critical coverage: repetition does not rescue" | "Below the critical coverage: no detectable rescue by repetition" | Task 6 (exact title given). First sentence of the section is a factual count (no run generalizes, 0 of 5 per cell) and the last sentence explicitly warns the contrast "should be read as a coverage contrast, not as a test of whether repetition rescues low coverage" — neither claims more than the new title. One wording flag from the last sentence is in Part C (item 10). |

## Audit report: "pre-specified" / "pre-registered" / "planned" (task 5)

Occurrences in the final text, and their disposition:

| Location | Word | Disposition |
|---|---|---|
| Methods 3.4, outcomes ¶ | "pre-specified exploratory outcome" (weight norm) | **Kept**; confirmation TODO added (change #8) |
| Methods 3.4, families ¶ | "declared rather than pre-specified (deviation-log item iii)" | **Kept** — accurate contrastive statement about the primary families |
| Methods 3.4, plan ¶ | "The analysis was planned in an internal design document" | **Kept** — pre-existing, accurate |
| Fig. 3 caption | "(pre-specified exploratory outcome)" | **Kept** per task 5 (same claim as Methods; covered by the one TODO) |
| Appendix B (iii) | was "pre-specified analysis families" | **Changed** → "planned in the internal design document" (change #6) |
| Appendix B (iv) | was "pre-specified extreme contrast cell" | **Changed** → "declared" (change #7) |
| Methods 3.4, TOST | was "no margin was pre-specified" | **Changed** per task 8 → "The margins were not chosen before the results were seen" (change #9) |
| Limitations | was "a margin that was not pre-specified" | **Changed** per task 8 (change #11) |
| Anywhere | "pre-registered" | **None occurs** |
| Anywhere | "unplanned" | **None occurs** |

## Overclaim audit (task 9)

Sentences in the Abstract, Introduction, Discussion, and Conclusion stating that repetition "does not" change something were audited against the two qualifiers ("at matched per-example dose", "detectable"):

- Abstract: "Repetition shows no detectable effect on GrokTime at matched dose" — both qualifiers present. OK.
- Abstract (final sentence): "In this regime, under a fixed optimization budget and at matched per-example dose…" — qualified. OK.
- Introduction: "at matched per-example dose, repetition shows no detectable effect on GrokTime in either arrangement" — qualified. OK.
- Discussion (summary): "Repetition, at matched per-example dose, showed no detectable effect on GrokTime in either arrangement." — qualified. OK.
- Discussion (null reading): "no detectable effect on GrokTime at matched per-example dose within this design… not a claim that repetition is generally inert." — qualified. OK.
- Conclusion: "showed no detectable effect on the timing of the transition and did not rescue sub-critical coverage within the 20,000-step budget" — "did not rescue" lacked "detectably"; fixed with a one-word insert (change #5). "Within the 20,000-step budget" retained as the scope qualifier.
- Conclusion (final): "additional repetition at matched dose does not detectably change either" — qualified. OK.
- Reviewed, left unchanged (already hedged or factual): Discussion speculative ¶ "uniform repetition behaves like training on the unique subset" (under the "(speculative)" label, introduced by "The results are compatible with…" and scoped "at matched step budget"); "near-duplicates clustered in time are close to neutral at matched dose" ("suggests", "at matched dose"). Flagged for your awareness in Part C (item 11).
- Minor inconsistency noted, not changed: the Abstract says repetition "delays memorization" while the Introduction says "slightly delays" — optional to align (Part C, item 12).

## Consistency checks (task 10)

All repeated values verified identical everywhere they appear; no mismatch found:

| Value | Occurrences (line numbers of main.tex) | Result |
|---|---|---|
| 83 grokked runs | Fig. 3 caption ("$n=83$ non-censored runs"), Sect. 4.5 ("Among the 83 runs that generalize") | identical |
| 3 of 35 | Abstract, Introduction (findings ¶ and contributions), Discussion ("three of thirty-five"); Sect. 4.1 ("35 runs… three runs in total generalize") | identical |
| 8,400 / 1,800 | Abstract, Introduction, Sect. 4.1, Sect. 4.2 (bounds), Sect. 4.3 (interleaved medians) | identical |
| −6,600, CI [−11,600, −4,000] | Introduction (contributions), Sect. 4.1 | identical |
| Holm-adjusted p = 0.016 | Abstract, Introduction ×2, Sect. 4.1 ×2 | identical |
| Holm-adjusted p = 0.048 | Sect. 4.2 (MemTime) | single occurrence |
| Holm-adjusted p = 0.024 | Sect. 4.2 (sub-critical accuracy), Sect. 4.5 (weight norms) | identical |
| Holm-adjusted p = 0.032 | Sect. 4.5 (weight norms) | single occurrence |
| −75.5 pp extreme contrast | Sect. 4.4 only | see Part C item 9 (table medians give 75.4; text unchanged) |

Compile: tectonic, 14 pages, no warnings. No "AI generated" / "AI-generated" string anywhere in the source or the PDF text layer.
