# Part B — Final Cleanup Pass: Change Log

Location | Before | After | Reason

## 1. Direction of the "bound" sentences (Sect. 4.2, task 1)

| # | Location | Before | After | Reason |
|---|----------|--------|-------|--------|
| 1 | Abstract | `(rank-biserial $r=1.0$, …)` | `(rank-biserial $r=+1.0$, …)` | Sign-format consistency with the stated definition (r = +1 means every first-named run is smaller); "+" makes the direction explicit everywhere. |
| 2 | Sect. 1, para. 3 | `rank-biserial $r=1.0$` | `rank-biserial $r=+1.0$` | Same as #1. |
| 3 | Sect. 1, contributions | `Holm $p=0.016$` | `Holm-adjusted $p=0.016$` | Uniform "Holm-adjusted p" style (task 12). |
| 4 | Sect. 4.1 | `rank-biserial $r=1.0$` | `rank-biserial $r=+1.0$` | Same as #1. |
| 5 | Sect. 4.4 | `rank-biserial $r=1.0$` | `rank-biserial $r=+1.0$` | Same as #1. |
| 6 | **Sect. 4.2, bound sentence (85%)** | "at 85% coverage the $R=8$ interval $[-400,+700]$ steps excludes repetition-induced shifts larger than roughly **22% earlier or 39% later** than the $R=1$ median of 1,800 steps" | "at 85% coverage the $R=1$-versus-$R=8$ interval $[-400,+700]$ steps excludes repetition-induced shifts larger than roughly **700 steps earlier (about 39% of the $R=1$ median of 1,800 steps) or 400 steps later (about 22%)**" | **Direction was reversed.** Derivation: the CI is on the median difference d = median(R1) − median(R8) (first-named minus second-named). d ∈ [−400, +700] ⇒ the shift of R=8 relative to R=1 is s = −d ∈ [−700, +400], i.e. at most 700 steps earlier or 400 steps later. Percentages: 700/1,800 = 0.389 → 39% earlier; 400/1,800 = 0.222 → 22% later. Verified against the archived pipeline (F2 row: C85 R1 vs R8, median_diff = +100, CI [−400, +700]). |
| 7 | **Sect. 4.2, bound sentence (55%)** | "at 55% the interval $[-1,500,+2,600]$ excludes shifts larger than roughly **one third earlier or one half later** than the 4,700-step median" | "at 55% the interval $[-1,500,+2,600]$ excludes shifts larger than roughly **2,600 steps earlier (about 55% of the 4,700-step median) or 1,500 steps later (about 32%)**" | **Direction was reversed.** Derivation: d = median(R1) − median(R8) ∈ [−1,500, +2,600] ⇒ shift of R=8 is s = −d ∈ [−2,600, +1,500]: at most 2,600 steps earlier or 1,500 later. Percentages: 2,600/4,700 = 0.553 → 55% earlier; 1,500/4,700 = 0.319 → 32% later. |
| 8 | Search for same reversal elsewhere | — | — | None found: the Abstract does not state the bounds; Discussion says only "point estimates of a few hundred steps in either direction" (direction-neutral); Limitations does not mention them. Only Sect. 4.2 carried the reversal. |

## 2. Sign convention consistency (task 2)

| # | Location | Before | After | Reason |
|---|----------|--------|-------|--------|
| 9 | Methods 3.4 | (unchanged) | (unchanged) | The convention was already stated once, correctly: "the median difference is reported as first-named minus second-named condition" and "r = +1 indicates that every first-named run is smaller than every second-named run". No edit needed. |
| 10 | **Sect. 4.2 (sub-critical accuracy)** | "blocked $R=1$ versus $R=4$: median difference **8.3** percentage points, 95% CI **[4.5, 11.3]**" | "…median difference **−8.3** percentage points, 95% CI **[−11.3, −4.5]**" | Under the stated convention the difference is first-named (R=1) minus second-named (R=4) = 13.4 − 21.7 = **−8.3**; the CI endpoints swap signs with it. The archived pipeline value is median_diff = −0.0831, CI [−0.1134, −0.0453]. The following text ("a shift from a median of 53 to 86 correct answers") already had the correct direction and needed no change. |
| 11 | Sect. 4.3 (mode contrasts) | "median differences within ±300 steps, except one at +700 steps with CI [−5,300, +4,300]" | "median differences **(blocked minus interleaved)** within ±300 steps, except **+700 steps at (55%, R=2)** with CI [−5,300, +4,300]" | The direction of the mode contrasts was not stated, so the sign of +700 could not be determined from the text. Made explicit; derivation from Table 2 medians: 55%/R=2 blocked 4,200 vs interleaved 3,500 ⇒ blocked − interleaved = +700. (Matches the archived pipeline.) |
| 12 | Other signed differences audited | — | — | Verified against the convention and the archived pipeline, no changes needed: F1 85v45 = −6,600 [−11,600, −4,000] (first-named smaller); F2 +300/+900/+100/+100 (R=1 later); RMST +280 (55%), +160 (85%) (R=1 larger); F3 −75.5 (first-named smaller); weight norm at step 1,000: +0.53 (R=1 larger than R=2: 23.95 vs 23.35, archived medians). MemTime and final-norm effects are stated as "rises from X to Y" (no signed values). All r = +1.0 values are consistent with the stated definition in their direction (first-named group is the smaller one in every case). |

## 3. Cox model description (task 3)

| # | Location | Before | After | Reason |
|---|----------|--------|-------|--------|
| 13 | Methods 3.4 (survival paragraph) | No description of the Cox model anywhere in Methods or Appendix. | Added two sentences + TODO: stratification variable = coverage level (35, 55, 85%); covariate = single binary indicator (blocked R ∈ {2,4,8} = 1 vs shared R=1 baseline = 0); 60 runs, 43 events; Breslow tie handling; Newton–Raphson partial-likelihood fit; Wald 95% CI; implemented in NumPy in the archived pipeline (no external survival-analysis package); `\todo{confirm the Cox specification … against the analysis code}` | The model appears in the Introduction and Sect. 4.2 but was never described. All details were read from the archived analysis code (stats_core.py, `cox_stratified`) — none guessed — but a TODO asks the author to confirm them, since the manuscript itself did not state them. |
| 14 | Appendix A, "Statistical software" | Cox model absent. | Added one sentence with the same specification (binary covariate, stratified by coverage, Breslow ties, Newton–Raphson, Wald CIs, NumPy implementation). | Same reason; the same author-confirmation TODO in Methods covers it. |

## 4. MemTime maximum (task 4)

| # | Location | Before | After | Reason |
|---|----------|--------|-------|--------|
| 15 | Sect. 4.1 | "across all 135 runs in the design, \memtime{} **never exceeds 500 steps** (median 200)" | "across all 135 runs in the design, **median \memtime{} is at most 500 steps in every condition** (overall median 200) `\todo{report the maximum MemTime over all 135 runs from runs.csv}`" | Table 2 shows a median of exactly 500 for 85%/R=8/blocked, so the maximum of that cell cannot be inferred from the table; the stronger claim is replaced by the median-level claim plus a TODO, as instructed. |

## 5. "Pre-specified" / "declared" / "unplanned" wording (task 5)

| # | Location | Before | After | Reason |
|---|----------|--------|-------|--------|
| 16 | Sect. 3.3 (Design) | "omit a cell required by the **pre-specified** extreme contrast" | "omit a cell required by the **declared** extreme contrast" | The three primary families are "declared" (they differ from the internal plan, deviation-log item iii). |
| 17 | Sect. 3.4 | "The statistical plan was **pre-specified** in an internal design document; … deviations are logged in Appendix B." | "The analysis was **planned** in an internal design document; there is no public registry entry, and the deviations from that plan are listed in Appendix B." | Given deviation-log items (iii)–(v), "pre-specified" overstates; reworded as instructed. |
| 18 | Sect. 4.2 (end) | "These secondary-outcome families were **not pre-specified** and are exploratory." | "These secondary-outcome families are exploratory." | Secondary-outcome families are "exploratory"; the pre-specification claim is dropped. |
| 19 | Sect. 4.5 | "**The one clear effect** is below the coverage boundary" | "**The most consistent difference** is below the coverage boundary" | Neutral wording as instructed. |
| 20 | Sect. 4.5 (end) | "These comparisons were not part of the pre-specified families; we report them as **unplanned** and exploratory." | "These comparisons are not part of the declared confirmation families; they are exploratory and are Holm-corrected only within their own small family." | Reconciles with the Fig. 3 caption and Methods 3.4, which call the weight-norm trajectory a "pre-specified exploratory outcome": the internal design document lists WeightNorm as a (exploratory) outcome with hypothesis H4 and planned exploratory analyses, so "unplanned" was wrong for the R-contrasts; "not part of the declared confirmation families" is accurate for all of them. See Part C item 13 for the author-verification note. |
| 21 | Fig. 3 caption; Methods 3.4 ("pre-specified exploratory outcome") | (unchanged) | (unchanged) | Kept: the internal design document (STUDY_DESIGN.md, outcome 4 + H4) supports "pre-specified **exploratory** outcome", and the deviation log records no deviation for it. Flagged in Part C for author verification. |
| 22 | Audit of remaining occurrences | — | — | Kept as accurate: "no margin was pre-specified" (Methods 3.4) and "a margin that was not pre-specified" (Limitations) are negative statements about the TOST margin and are correct. Deviation-log items (iii)/(iv) legitimately use "pre-specified" when describing what the internal document specified. No "pre-registered" occurs anywhere. |

## 6. Citation–claim mismatch (task 6)

| # | Location | Before | After | Reason |
|---|----------|--------|-------|--------|
| 23 | Discussion, "Interpretation" | "…are consistent with within-batch duplicates perturbing gradient noise without shifting the mean dynamics `\citep{wu2021curricula}`." | "…are consistent with **the hypothesis that** within-batch duplicates perturb gradient noise without shifting the mean dynamics `\todo{add a suitable reference on gradient noise and batch composition, or retain the sentence as an explicit hypothesis}`." | Wu et al. (When do curricula work?) does not support this claim as worded. Rewritten as an explicitly uncited hypothesis; no replacement reference invented. Wu et al. remains cited (correctly) in Related Work for curricula. All other citations were checked against their claims; no other clear mismatch found (doubtful ones listed in Part C). |

## 7. References and Positioning paragraph (task 7)

| # | Location | Before | After | Reason |
|---|----------|--------|-------|--------|
| 24 | Related Work, "Positioning" | Two bracketed `[SUGGESTED …]` notes inline (critical-data-fraction reference; "How much can language models memorize?" / "Data mixing laws" candidates). | Removed; paragraph kept as clean prose citing only references already in the list. | Bracketed suggestions removed from the text as instructed; the candidates are preserved in Part C item 4. |
| 25 | Bibliography | (unchanged) | (unchanged) | Flag-only task: nothing changed in the reference list. See Part C items 2–5 for the verification list. |

## 8. Process residue removed (task 8)

| # | Location | Before | After | Reason |
|---|----------|--------|-------|--------|
| 26 | Appendix A, "Statistical software" | "…when ties are present --- **several p-values in an earlier draft were produced by that substitution and have been replaced by the enumerated values**." | "…when ties are present, and the substituted p-values can fall below the attainable exact minimum of 2/252 = 0.0079." | Draft-history phrase removed; the factual method statement kept. |
| 27 | Appendix A, "Statistical software" | "…documented per-analysis offsets; **the archived pipeline reproduces every number in this paper from the raw logs**." | "…documented per-analysis offsets." | Unverified reproduction claim removed here (see #30 for the Methods counterpart). |
| 28 | Appendix B, deviation (v) | "(v) **during revision, the two-sample procedure was replaced by** the enumerated exact permutation Mann–Whitney test (**an earlier draft used** values produced by SciPy's asymptotic tie-corrected method, …), and the bootstrap CIs **were recomputed with two-group within-group resampling after a defect in the archived code (resampling one group only, yielding too-narrow intervals) was found**; no data, stopping rule, or family definition changed in this correction." | "(v) the two-sample rank test is the enumerated exact permutation Mann–Whitney procedure, adopted in place of SciPy's asymptotic tie-corrected method because the library substitutes that method silently in the presence of ties and it can yield p-values below the attainable exact minimum of 2/252; and the bootstrap confidence intervals of median differences resample within each group, since resampling one group only yields too-narrow intervals. No data, stopping rule, or family definition was affected." | Kept the full factual content (exact method replaces asymptotic because of the SciPy tie fallback; bootstrap uses within-group resampling for both groups; nothing else changed), phrased as a neutral methods note with no story about drafts, revisions, or code defects. Deviations (i)–(iv) untouched. |
| 29 | Appendix C (descriptives) | "**It moved to the appendix in revision because** the main text reports the subset needed for each argument." | "The main text reports the subset needed for each argument." | Revision-history phrase removed, meaning kept. |
| 30 | Bracketed TODO audit | 8 pre-existing TODOs | Same 8 kept (TOST margin, funding, competing interests, data DOI, code DOI, AI-use, deviation-log verification, affiliation comment) + 4 new ones (Cox details, MemTime maximum, dashed-line confirmation, pipeline re-run) | All retained/added TODOs are author-decision or author-data items per the task's keep-list; all use the single `\todo{…}` format. |

## 9. Title and framing (task 9)

| # | Location | Before | After | Reason |
|---|----------|--------|-------|--------|
| 31 | Title | "Coverage, not repetition: …" | (unchanged in Part A) | Kept as instructed; three matched-dose alternatives proposed in Part C item 12. |
| 32 | Conclusion | "…was gated by the coverage of the training distribution rather than by repeated exposure." | "…rather than by repeated exposure **at matched per-example dose**." | Softens the only unqualified "rather than" sentence; the Abstract, Introduction, and Discussion were already qualified ("at matched dose", "in this regime"). |

## 10. Figures and captions (task 10)

| # | Location | Before | After | Reason |
|---|----------|--------|-------|--------|
| 33 | Fig. 4 caption | "ticks mark right-censored runs, **the dashed line marks the 20,000-step budget**, and legend entries give grokked runs of five." | "ticks mark right-censored runs and legend entries give grokked runs of five." + `\todo{confirm whether the Kaplan–Meier figures … draw a dashed line at the 20,000-step budget; if not, keep the reworded captions, and if they do, restore the clause}` | The caption must not describe elements that may not be shown. Note: the archived figure script (task_survival.py) draws only KM step curves and censoring ticks — no budget line — so the reworded caption matches the current figures. |
| 34 | Fig. 5 caption | Same clause. | Same removal. | Same reason (one TODO covers both figures). Fig. 1c's budget line was not flagged and its caption was left unchanged. |

## 11. Declarations (task 11)

| # | Location | Before | After | Reason |
|---|----------|--------|-------|--------|
| 35 | Methods 3.4 | "The archived analysis pipeline … **reproduces every reported statistic from the raw logs** and is available with the code." | "The archived analysis pipeline … is available with the code (Declarations) `\todo{re-run the archived pipeline on the final data and confirm that it reproduces every reported statistic}`." | Reproduction claim removed pending a confirmed re-run, as instructed. |
| 36 | Data availability TODO | "provide the DOI or URL of the data repository." | "…; once public, add the sentence 'The repository is public at the time of submission'." | The sentence is added only as a TODO-AUTHOR item. |
| 37 | Code availability TODO | "provide the DOI or URL of the code repository." | Same extension as #36. | Same reason. |
| 38 | AI-use TODO | "confirm that this AI-use statement accurately reflects your actual workflow…" | "list every AI tool used at any stage, including code generation, analysis scripts, prompt-assisted revision, and language editing, describe honestly what each did, and confirm the statement complies with Springer Nature's current disclosure policy." | Required AI-tool inventory added; the author-responsibility sentence itself is untouched. No "AI generated" watermark text exists anywhere in the source (verified). |

## 12. Language and format (task 12)

| # | Location | Before | After | Reason |
|---|----------|--------|-------|--------|
| 39 | Sect. 4.2 | "(medians 36\% and 44.5\%)" | "(medians 36.0\% and 44.5\%)" | Decimal consistency with Table 2 (36.0). |
| 40 | Sect. 4.3 | "versus 41.3\%, 36\%, 44.5\%" | "versus 41.3\%, 36.0\%, 44.5\%" | Same. |
| 41 | Sect. 4.2 | "(all adjusted p = 1.0)" | "(all Holm-adjusted p = 1.0)" | Uniform "Holm-adjusted p" style. |
| 42 | Limitations | "pre-specified --- at defensible margins … larger --- so" | "pre-specified (at defensible margins … larger), so" | Em-dash chain reduced to a parenthesis. |
| 43 | Author contributions | "writing --- original draft, and writing --- review and editing" | "writing -- original draft, and writing -- review and editing" | CRediT role names conventionally take an en dash. |
| 44 | Preamble | (no emergencystretch) | `\setlength{\emergencystretch}{1em}` | Typographic robustness; no content change. |
| 44b | Appendix A, "Statistical software" | "two-sided $p$-value **the proportion with** $|U - n_1 n_2/2|$ at least as large as observed" | "two-sided $p$-value **the proportion of assignments with** $|U - n_1 n_2/2|$ at least as large as observed" | Pre-existing overfull line (9.8pt): the unbreakable formula could not fit; inserting "of assignments" (mirroring the Methods 3.4 phrasing "the proportion of assignments whose…") gives a break point. Compile is now warning-free. |
| 45 | Cross-references and repeated numbers | — | — | Verified: Sect./Fig./Table/Appendix references all point to the right targets; 83 grokked runs, 3 of 35, 8,400/1,800, −6,600 [−11,600, −4,000], Holm 0.016/0.048/0.024/0.032, RMST values, Fisher/CP values, Cox 0.96 [0.48, 1.94], TOST 1.21–1.87, and all other statistics are identical everywhere they appear and match the archived pipeline outputs. The two items that could not be confirmed from the manuscript alone are flagged in Part C (items 1 and 14). |
