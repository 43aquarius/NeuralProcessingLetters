# NPL Submission Package — Release v1.0.0

**Manuscript:** *Coverage versus within-epoch repetition at matched dose in
transformer grokking*
**Author:** Chang Tan (Dalian University of Technology)
**Target journal:** Neural Processing Letters (Springer Nature)
**Date:** 2026-10-13

## Assets

- **`NPL-submission-package-v1.0.0.zip`** — the complete journal submission
  set:
  - `main-sn.pdf` — the compiled manuscript (Springer Nature `sn-jnl`
    template, 20 pages)
  - `main-sn.tex`, `references.bib`, `sn-jnl.cls`, `sn-basic.bst`, `figs/` —
    the full LaTeX source; compiles with `tectonic main-sn.tex`
  - `COVER_LETTER.md` — the cover letter for the submission system
  - `MANIFEST.md` — content listing and compile instructions
- **`manuscript-sn-v1.0.0.pdf`** — the manuscript PDF alone, for quick
  download

## Code and data

The complete research artifact — training code, the 135 raw run logs, the
exact-permutation statistical pipeline, and the verification script that
re-derives every reported statistic (353/353 checks pass) — is in this
repository's root directory.

Licences: code under MIT; data files and figures under CC-BY-4.0.

## Declarations snapshot (as in the manuscript)

- Funding: No funding was received.
- Competing interests: The author has no competing interests.
- Data / code availability: public repository
  (https://github.com/43aquarius/NeuralProcessingLetters, tag `v1.0.0`);
  the repository is public at the time of submission.
- Generative AI use: declared in the manuscript (GLM assistant, Z.ai;
  stage-by-stage list in the Declarations section).

## Study summary

A two-layer transformer learns modular addition (p = 23; 529 unique
problems) with training-set coverage (25-85%), within-epoch repetition
(R in {1,2,4,8}), and the arrangement of repeated copies (blocked versus
interleaved) manipulated in a partially crossed design (27 conditions,
5 seeds each, 135 runs), while a continuous batching scheme holds the
expected per-example dose identical across repetition levels. Coverage
gates the transition from memorization to generalization; repetition at
matched per-example dose shows no detectable effect on its timing, while
leaving measurable traces on memorization speed, sub-critical accuracy,
and weight norms. Analysis uses exact permutation tests and
censoring-aware survival methods.
