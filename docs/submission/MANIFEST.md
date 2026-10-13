# NPL Submission Package — v1.0.0 (2026-10-13)

Complete submission set for *Neural Processing Letters* (Springer Nature).

**Manuscript:** *Coverage versus within-epoch repetition at matched dose in
transformer grokking*
**Author:** Chang Tan (Dalian University of Technology, Dalian, China)
**Corresponding author email:** aquars43@foxmail.com

## Contents

| File | Role |
|---|---|
| `main-sn.pdf` | Compiled manuscript (Springer Nature `sn-jnl` template, `pdflatex` class option; 20 pages) |
| `main-sn.tex` | LaTeX source of the manuscript |
| `references.bib` | BibTeX database (14 entries, each verified against the authoritative record on 2026-10-13) |
| `sn-jnl.cls`, `sn-basic.bst` | Springer Nature class file and numbered reference style |
| `figs/` | The six manuscript figures (vector PDF; Figs. 1-3 and the three Kaplan-Meier figures) |
| `COVER_LETTER.md` | Cover-letter text for the submission system |
| `MANIFEST.md` | This file |

## Compiling

```bash
tectonic main-sn.tex
# or the classic route:
pdflatex main-sn && bibtex main-sn && pdflatex main-sn && pdflatex main-sn
```

## Declarations (final, as submitted)

- **Funding:** No funding was received.
- **Competing interests:** The author has no competing interests.
- **Ethics approval and consent:** not applicable (purely computational study).
- **Data availability / Code availability:** public repository at
  https://github.com/43aquarius/NeuralProcessingLetters (tag `v1.0.0`);
  the repository is public at the time of submission.
- **Generative AI use:** declared in the manuscript's Declarations section
  (GLM assistant, Z.ai; stage-by-stage list included there).

## Remaining author-side items (checked in `docs/submission/` notes)

1. Add school/department and postal code to the affiliation if the NPL
   title-page format requires them (LaTeX comment in `main-sn.tex` marks
   the spot).
2. Confirm the `sn-article` template version against the current download
   from Springer Nature when the submission is actually entered.
3. Optional: name a Zenodo DOI in the availability statements after
   depositing the tagged release (see `PRE_RELEASE_CHECKLIST.md` in the
   repository root).
