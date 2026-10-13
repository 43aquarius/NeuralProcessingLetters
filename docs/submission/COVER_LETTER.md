# Prompt 9 — Cover Letter and Reviewer-Suggestion Notes

---

## Cover letter (to be pasted into the submission system; edit the bracketed
fields)

Dear Editors,

Please find enclosed our manuscript, "**Coverage versus within-epoch
repetition at matched dose in transformer grokking**," which we submit for
consideration as an original research article in *Neural Processing Letters*.

The paper asks a question that training-data practice forces but grokking
research has not isolated: when a fixed optimization budget is spent on a
small transformer learning modular addition, does it matter how often each
unique training example is shown, or in what arrangement those exposures
arrive? We separate the two data decisions practitioners make — how many
distinct examples (coverage) and how many passes over them (repetition) — in
a 27-condition, five-seed, partially crossed design (135 runs) whose
continuous batching scheme holds the expected per-example dose constant
across repetition levels. We analyze the outcome with exact permutation
tests and censoring-aware survival methods, since runs that never generalize
are right-censored rather than missing.

Within this fixed budget and at matched per-example dose, coverage governs
the transition from memorization to generalization and repetition does not
detectably change its timing in either arrangement (blocked or interleaved),
with every confidence interval including zero; repetition does leave
measurable traces on memorization speed, sub-critical accuracy, and weight
norms below the coverage boundary. The main limitation, stated in the
manuscript, is that the conclusion is specific to one small task and
architecture, five seeds per condition, and the matched-dose regime — it does
not speak to the unmatched-dose setting in which more repetition buys more
updates. On novelty: the coverage dependence we measure reproduces known
results on dataset size in grokking; the new contribution is the matched-dose
decomposition of repetition from coverage, the blocked-versus-interleaved
arrangement contrast, and the censoring-aware statistical treatment, which we
hope is useful for small-sample machine-learning experiments generally.

We believe the work fits the journal's scope in machine learning methodology
and the empirical study of generalization, and will be of interest to its
readers working on data-constrained training and the science of grokking.

We confirm that this manuscript is original, has not been published
previously, and is not under consideration by any other journal. All authors
have approved the submission. Generative-AI use in the preparation of the
manuscript is declared in the Declarations section, in accordance with
Springer Nature's policy.

Thank you for your consideration.

Sincerely,
Chang Tan
Dalian University of Technology, Dalian, China
aquars43@foxmail.com

---

## Suggested reviewers — areas, not names (find and verify real people; do
not use the names below as reviewers — they are search profiles)

1. **Grokking and delayed generalization (mechanistic or empirical):**
   authors of experimental or mechanistic grokking papers who routinely
   train small transformers on modular arithmetic — the people best placed
   to judge whether the matched-dose construction is sound.
2. **Data-constrained language-model training:** authors of the
   repeated-epochs / data-constrained scaling literature (the paper's
   pretraining-scale counterpart), who can judge the framing of the
   practical motivation.
3. **Statistics for small-sample machine-learning experiments:** researchers
   who write about permutation tests, equivalence testing (TOST), or
   censoring-aware analysis in ML evaluation — the paper's statistical
   choices are its most unusual feature.
4. **Curriculum / data-ordering effects:** authors of curricula studies in
   deep learning, since the blocked-versus-interleaved contrast is an
   ordering manipulation.
5. **Deduplication and memorization:** authors of training-data deduplication
   or memorization-measurement studies, for the sub-critical-accuracy and
   memorization-speed findings.
6. **Loss-landscape / implicit-regularization analyses of grokking:**
   researchers working on weight-norm explanations, for Sect. 4.5's
   exploratory weight-norm results.
7. **Reproducibility in ML:** researchers active in artifact evaluation, for
   whom the 135-run archive with a claim-verification script will be a
   feature rather than a burden.
8. *(Optional)* **Scaling-laws researchers:** if the editors prefer a
   broader empirical perspective on coverage/size trade-offs.

How to find them: start from the papers you actually read and cite (the
manuscript's reference list), check recent NPL/NeurIPS/ICLR author lists for
the areas above, and verify each candidate's affiliation and email on their
current institutional page before entering them in the system.

## Conflict-of-interest points to check before naming any reviewer

- No co-authors (trivially satisfied: sole author).
- No one at your current institution.
- No collaborators from the last [TODO-AUTHOR: your field's convention —
  commonly 3–5] years (check co-authorship on all your papers, including
  non-archived preprints).
- No one with whom you have a personal or advisor/advisee relationship.
- [TODO-AUTHOR: also declare any editorial-board or reviewer-relationship
  you think the editors should know about.]

## Submission-system fields to check on the NPL site

- [ ] Article type: "Original research" (vs. Letter/Review — confirm the
      current NPL taxonomy; "Letter" article types exist in some Nature
      Portfolio journals, not NPL).
- [ ] Abstract word limit (current abstract 246 words, within the NPL
      150-250 range) and whether structured abstracts are required (they
      are not, for NPL — confirm).
- [ ] Keyword count and whether keywords must come from a controlled list.
- [ ] Whether the journal requires line numbering for review (add the
      `lineno` class option if so).
- [ ] Cover-letter length limits in the submission system field.
- [ ] Whether reviewer suggestions are entered in the system vs. the letter
      (usually both possible).
- [ ] Data-availability statement: the system may require choosing from a
      preset list — match it to the repository DOI once deposited.
- [ ] AI-use declaration: check whether NPL wants it in a specific system
      field in addition to the manuscript.
- [ ] Optional open-access charges: choose the standard subscription
      (non-OA) route and decline the optional open-access fee, per your
      decision; confirm current terms on the journal's site.
- [ ] ORCID linkage for the corresponding author.
