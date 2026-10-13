# Prompt 8 — Simulated Peer Review and Response Shells

*Referee simulation on the final manuscript (main.pdf / main-sn.pdf content).
It is not a substitute for real reviewers; it finds weak points early. Every
criticism below is grounded in the manuscript text; nothing about the
literature is asserted beyond what the manuscript itself cites.*

---

## Referee report

### Summary of the paper

The authors study a two-layer transformer (1.04 × 10^5 parameters) learning
modular addition (p = 23; 529 problems) under a 27-condition, 5-seed,
partially crossed design (135 runs) that separates **coverage** (25–85% of the
problem space) from **within-epoch repetition** (R ∈ {1,2,4,8}) and from the
**arrangement** of repeats (blocked vs interleaved), while a continuous
batching scheme holds the expected per-example dose constant across R.
Coverage gates whether and when grokking occurs (medians fall from 8,400
steps at 45% to 1,800 at 85%; below ~35% generalization is unreliable; at 25%
absent within the 20,000-step budget), whereas repetition shows no detectable
effect on GrokTime at matched dose in either arrangement (all intervals
include zero), with detectable traces on secondary outcomes: delayed
memorization, higher sub-critical accuracy at 25%, and larger final weight
norms there. The analysis is unusually careful for a small-scale ML paper:
exact permutation Mann–Whitney tests, censoring-aware Kaplan–Meier/log-rank/
RMST, a stratified Cox model, Fisher exact tests with Clopper–Pearson
intervals, declared (not pre-registered) families with Holm correction, and a
post hoc TOST sensitivity analysis that explicitly declines to claim
equivalence.

### Novelty relative to known results

The coverage dependence itself is a seed-level replication of known results
(Power et al. on dataset fractions; Liu et al. Omnigrok; circuit-efficiency
accounts). The genuinely new elements are (i) the factorial decomposition of
coverage from repetition *at matched per-example dose*, (ii) the
blocked-versus-interleaved arrangement contrast, and (iii) the censoring-aware
statistical treatment of grokking times, which most grokking studies lack.
The novelty is therefore methodological and design-centric rather than
phenomenon-centric. For a journal like NPL this is defensible, but the paper
will be judged on whether the decomposition is executed convincingly, and the
answer is mostly yes, with the limitations the authors state.

### Experimental design

The matched-dose construction is the paper's core contribution and is well
explained (Sect. 3.2), including the honest statement that interleaved
repetition approximates sampling with replacement (so a repetition-count
effect is expected to be small in that arm) and that the blocked arm mainly
tests temporal clustering and within-batch duplication. The partially
crossed design is documented in Table 1 with the deviation log (Appendix B)
disclosing family redefinitions. The design has known gaps, all acknowledged:
five seeds per cell, a single task and modulus, no unmatched-dose arm, and no
batch-size control separating within-batch diversity from temporal
clustering (Sect. 3.2 states a batch-size control would be needed; the
Discussion flags it again).

### Statistics

The strongest part of the paper. Exact enumeration of all 252 assignments
with midranks is the right test at n = 5 with heavy ties; the 2/252 floor on
two-sided p-values is correctly internalized throughout. Right-censoring is
treated natively rather than by ad hoc imputation. Multiplicity is handled
within declared families, and the families' post hoc origin is disclosed
(deviation-log item iii). The equivalence analysis is appropriately demoted
to a post hoc sensitivity analysis with no equivalence claim at any margin.
Weaknesses: five seeds per contrast is fundamentally low power for the null
claims (the TOST analysis itself shows 80% power only for true ratios of
roughly 1.7–2); the "all p ≥" bounds are coarse; and the median-difference
bootstrap CIs over five tied values are, as the authors say, indicative. The
stratified Cox model is fit but appropriately not leaned on (3 of 43 events
in one stratum).

### Claims versus evidence

Consistent throughout: "no detectable effect at matched dose" is used
carefully with bounds, the abstract carries the qualifiers, and the
Conclusion says "did not detectably rescue." The one loose end this reviewer
notices: the TOST-power sentence "80% power only for true ratios of about two
or larger" is slightly conservative against the pipeline's own simulated
crossing (~1.78 on the archived grid); harmless but imprecise.

### Clarity and reproducibility

Well written; terminology (GrokTime, MemTime, coverage, repetition,
arrangement) is defined and used consistently; figures carry per-panel
statistics. Reproducibility is exemplary for this venue: seeds, exact
statistical methods, deviation log, and a verification script that re-derives
all 353 claimed statistics from the archived logs. The repository is
promised with DOIs (pending at submission time).

---

## Ten most likely major criticisms (ranked by rejection risk)

1. **Limited novelty: the headline finding (coverage gates grokking) is
   known.** Already addressed in text: Sects. 1–2 position the contribution
   as the matched-dose decomposition plus censoring-aware statistics, not
   the coverage effect itself. A text change cannot create novelty; only the
   second modulus / more seeds experiments (Part 3, Prompt 10) would add
   substance. *Verdict: text already handles; new experiments would help.*
2. **Five seeds per condition is too few for the null claims.** Addressed:
   exact tests with the 2/252 floor stated, interval-based bounds given,
   power analysis in Sect. 4.2, limitations in the Discussion. Only more
   seeds (35–45% coverage especially) would strengthen it. *Verdict: text
   already handles; new experiments would help.*
3. **A single task (mod p = 23) and a single architecture; generalization of
   conclusions is unclear.** Addressed: Discussion explicitly calls the
   extrapolation speculation and quantifies the boundary as regime-specific.
   A second modulus or task is the clean answer. *Verdict: text already
   handles; new experiments would help.*
4. **The unmatched-dose regime — the practically relevant one (more
   repetition buys more updates) — is not tested.** Addressed: Sect. 3.2
   states the exclusion by construction and the Discussion interprets the
   null as regime-specific. A text change cannot fix this; an unmatched-dose
   arm would. *Verdict: text already handles; new experiments would help.*
5. **The blocked-versus-interleaved contrast conflates within-batch
   diversity with temporal clustering (no batch-size control).** Addressed:
   Sect. 3.2 states a batch-size control would be needed and the Discussion
   repeats it. *Verdict: text already handles; new experiments would help.*
6. **The interleaved arm approximates sampling with replacement, so its null
   is close to designed-in.** Addressed: Sect. 3.2 says exactly this and
   states that the blocked arm carries the clustering test; the paper does
   not overclaim. *Verdict: text already handles.*
7. **Families were redefined after seeing arm-A data (deviation-log items
   iii–iv); risk of analyst degrees of freedom.** Addressed: Appendix B
   discloses each deviation; the families are labelled "declared," Holm is
   within-family, and the secondary analyses are labelled exploratory.
   *Verdict: text already handles.*
8. **Sub-critical accuracy at 35% shows an unexplained blocked/interleaved
   asymmetry (opposite direction to the clustering hypothesis).** Addressed:
   Sect. 4.3 reports it as an observation, not an established difference,
   with non-significant tests. *Verdict: text already handles; more seeds
   would resolve.*
9. **Weight-norm/correlation analyses mix stopping times (grokked runs stop
   early), so the Spearman correlations are confounded.** Addressed: Sect. 4.5
   states the confound explicitly twice and declines to interpret the
   stratified correlations. *Verdict: text already handles.*
10. **The 75.5 vs 75.4 discrepancy (text −75.5 pp vs table medians 75.4).**
    Addressed in passing: the text uses the unrounded-median difference,
    which is the correct estimator; a one-sentence footnote would remove the
    apparent inconsistency. *Verdict: small text change would help
    [TODO-AUTHOR: optional footnote].*

## Minor issues (wording, figures, references)

- Abstract is ≈ 254 words; check the NPL limit (commonly 250) and trim if
  needed.
- TOST-power phrasing "about two or larger" vs the pipeline's ~1.78 crossing
  (see claims-vs-evidence above).
- The three title alternatives are commented above `\title` — delete before
  submission.
- The affiliation line lacks department/postcode if the journal requires them.
- Reference list: NeurIPS entries lack page ranges (acceptable in the style;
  add if the journal insists).
- Fig. 3a's 25% (magenta-red) and 55% (orange) curves are close for some
  colour-vision conditions (they are separated by trajectory shape; see
  FIGURE_FIXES.md) — acceptable, but be ready to adjust if raised.
- "single percentage points" phrasing in Sect. 4.4 could read as "single
  digits" — consider "a few percentage points."

## Recommendation

**Major revision.** The paper is honest, statistically careful, and fully
reproducible, but its contribution is deliberately narrow (a decomposition
result on one small system), and its main risks — novelty, sample size,
single task — are intrinsic to the design rather than to the writing. A
reviewer who values methodological rigor will push for acceptance after
revision; one who values broad impact may still lean reject. The highest-value
additions, if the authors can afford them, are more seeds at 35–45% coverage
and a second modulus, both pre-specified as new confirmatory analyses.

---

## Response shells (one per major criticism; [TODO-AUTHOR] where only you
can fill in)

**R1 (novelty).** We thank the reviewer for this assessment. As stated in
Sects. 1–2, we do not claim the coverage dependence as a new finding; our
contribution is (i) the within-coverage manipulation of repetition count and
arrangement at matched per-example dose, which to our knowledge has not been
isolated before in grokking studies, and (ii) the censoring-aware,
exact-inference treatment of grokking times, which we hope is useful to
small-sample ML studies beyond this task. We have revised the Introduction
to make the positioning still more explicit [TODO-AUTHOR: point to the exact
revision]. [TODO-AUTHOR: if you ran the Prompt 10 experiments, add: "We have
additionally added a second modulus / additional seeds at 35–45% coverage
(Sect. X), which reproduces the pattern."]

**R2 (five seeds).** We agree that power is limited and have framed all
repetition findings as "no detectable effect" with interval-based bounds
rather than as demonstrated equivalence (Sects. 3.4, 4.2). The exact
two-sided p-value floor at n = 5 versus 5 is 2/252 ≈ 0.008, and the TOST
power analysis (Sect. 4.2) quantifies which true ratios the design could
detect. [TODO-AUTHOR: if you added seeds, state the new n and the updated
result; otherwise: "Increasing the number of seeds, particularly at 35–45%
coverage, is the single most valuable extension and is left as future
work."]

**R3 (single task).** The limitation is stated in the Discussion. All
quantitative statements are regime-specific (one modulus, one architecture,
one budget). [TODO-AUTHOR: if you ran the second modulus, describe it and its
pre-run analysis plan; otherwise decline to extrapolate and cite the
transition-zone variability as the reason the single-task caveat matters.]

**R4 (unmatched dose).** We agree this is the practically central regime and
we deliberately excluded it: at matched steps, our design isolates the
arrangement effect; buying more updates with repetition is a different
question (Sect. 3.2). [TODO-AUTHOR: if you ran the unmatched-dose arm, report
it as a pre-specified confirmatory analysis; otherwise: "We now state more
explicitly in the Discussion that the matched-dose null does not speak to
the unmatched-dose regime, and we have added the missing sentence at [X]."]

**R5 (batch-size control).** As noted in Sect. 3.2, the blocked arm tests
temporal clustering and within-batch duplication jointly; separating them
requires a batch-size control (e.g., batch 256 at R=1 versus batch 32 at
R=8), which we have marked as the design extension we would run first.
[TODO-AUTHOR: if you ran it, report; otherwise confirm the text already
contains the statement and cite the paragraph.]

**R6 (interleaved null is designed-in).** We state this in Sect. 3.2
("interleaved repetition is close to sampling with replacement ... an effect
of repetition count per se is expected to be small in this arm") and
accordingly base the clustering test on the blocked arm and the mode
contrasts. The reviewer's reading is exactly our intended framing.

**R7 (families).** Every deviation from the internal design document is
disclosed in Appendix B with its rationale and timing; the families are
labelled "declared" rather than pre-registered, Holm correction is applied
within family, and the secondary-outcome families are labelled exploratory
throughout. No data, stopping rule, or exclusion was changed.

**R8 (35% asymmetry).** We report the blocked/interleaved asymmetry at 35%
coverage as an observation with non-significant exploratory tests (Holm
p ≥ 0.67) and explicitly decline to interpret it (Sect. 4.3). Its direction
is opposite to the clustering hypothesis, which we state.

**R9 (stopping-time confound).** Sect. 4.5 states the confound twice and
declines to interpret the stratified correlations; the only norm comparison
with matched stopping times is at 25% coverage, where all runs reach the
budget.

**R10 (75.5 vs 75.4).** The text value is the difference of the unrounded
medians (−75.48 pp → −75.5), while the table displays the medians rounded to
one decimal (21.2 − 96.6 = −75.4). [TODO-AUTHOR: consider adding this
one-sentence footnote to the table caption to pre-empt the question.]

---

## Notes on using this document

- The recommendation and rankings are a simulation, not a prediction; actual
  reviewers may weight novelty or scale differently.
- Every "text already handles" verdict cites the section that does the work —
  during revision, double-check that those passages survived the final edit.
- The response shells must not promise experiments you have not run; the
  [TODO-AUTHOR] slots exist precisely to keep them honest.
