# Prompt 7 — Springer Nature Template Conversion: change log and manual steps

## Template used

- Class: `sn-jnl.cls` from the official Springer Nature "sn-article" LaTeX
  template package (retrieved 2026-10-12 from a public mirror of the
  Springer Nature template distribution; the user manual `user-manual.pdf`
  ships with the same package). [TODO-AUTHOR: re-download the template from
  Springer Nature's LaTeX author support page when you prepare the submission,
  and confirm the version date shown in the file header.]
- Class options: `[pdflatex,sn-basic,Numbered]`
  - `sn-basic` — Basic Springer Nature reference style (numbered via the
    `Numbered` option; loads natbib with `numbers,sort&compress`).
    This matches the manuscript's existing numbered citations.
  - `pdflatex` — prevents the class from loading `breakurl`, whose
    PostScript-level URL hooks (`\pdf@box`) are undefined under the XeTeX
    engine used by tectonic. Under pdfLaTeX on your machine this option is
    also the documented pdflatex usage of the template. XeLaTeX breaks URLs
    natively, so nothing is lost. [TODO-AUTHOR: if you compile with pdfLaTeX
    locally, keep the option as the template's pdflatex examples show.]

## Files

- `download/paper-package-sn/main-sn.tex` — the converted manuscript.
- `download/paper-package-sn/references.bib` — the verified bibliography,
  keys renamed to match the manuscript's `\citep` keys (zero text changes).
- `sn-jnl.cls`, `sn-basic.bst` — copied from the template package.
- `figs/` — the same (fixed) figures as the working package.
- Output: `main-sn.pdf` — 21 pages, compiles with tectonic with warnings only.

## What changed (conversion only; no content changes)

| Item | Before (neurips_lite) | After (sn-jnl) |
|---|---|---|
| Class | `article` + `neurips_lite.sty` | `sn-jnl` with options above |
| Title | `\title{...}` | `\title[short]{full}` (running-head short title added) |
| Author | `\author{Chang Tan\\ ...}` | `\author*[1]{\fnm{Chang} \sur{Tan}}\email{...}` |
| Affiliation | plain text line | `\affil*[1]{\orgname{...}, \orgaddress{\city{Dalian}, \country{China}}}` |
| Abstract | `abstract` env after `\maketitle` | `\abstract{...}` before `\maketitle` (template order) |
| Keywords | `\noindent\textbf{Keywords:} ...` | `\keywords{...}` |
| Citations | `\citep` (numbered) | unchanged `\citep` (natbib numbers via class) |
| Bibliography | manual `thebibliography` (14 bibitems) | `\bibliography{references}` → sn-basic.bst (same 14 verified entries) |
| Declarations | before bibliography | after `\backmatter`, `\section*{Declarations}` (template order) |
| Appendices | `\appendix` + sections | `\begin{appendices}` ... `\end{appendices}` (appendix package, `[title]` option as loaded by the class) |
| Appendix numbering | A, B, C, D sections; Table 2/Fig. 5 unnumbered per main sequence | Tables/figures inside appendices numbered "Table C1", "Figure D1" etc.; all `\ref`s update automatically |
| Packages | neurips_lite, hyperref | class loads hyperref itself; kept amsmath/amssymb, booktabs, graphicx, xcolor, microtype |

Not changed: all text, equations, tables, figure environments, labels,
citations, the 7 remaining `[TODO-AUTHOR]` items, and the figure files.

## Compile check (tectonic, XeTeX)

- Compiles to completion; 21 pages.
- Residual warnings, all layout-level:
  - several `Underfull \vbox (badness 10000) while \output is active` —
    from the class's page-building with `\raggedbottom` under XeTeX; these do
    not affect correctness. If they bother you locally, they usually vanish
    under pdfLaTeX.
  - `Object @table.1 already defined` / `@figure.1` — benign hyperref
    duplicate-destination notices caused by the appendix counter restart;
    rendered numbering is consistent (Table 1 in main text; Table C1 etc. in
    appendices).
- Verified in the PDF: title block with corresponding author, abstract,
  keywords, numbered citations `[1]`–`[14]`, all 14 reference entries in
  sn-basic format, Declarations section in template order, Appendices A–D,
  figure references, and the 7 TODO-AUTHOR markers preserved.

## Remaining manual steps for you

1. Confirm the template version you download from Springer Nature matches
   (the site occasionally updates the package); replace `sn-jnl.cls` /
   `.bst` files with the downloaded ones if the version differs.
2. Confirm on the NPL author instructions page: reference style option
   (`sn-basic` numbered is the standard for NPL; some instructions mention
   `sn-mathphys-num`), abstract word limit (current abstract ≈ 254 words),
   keyword count (currently 6), and whether line numbering is required for
   submission (if yes, add the `lineno` class option).
3. Fill the affiliation detail (department, postcode) if required — a
   TODO-AUTHOR comment marks the spot.
4. Decide whether the short title used for running heads is acceptable.
5. Compile locally with pdfLaTeX (the journal's production workflow) and
   check that the bibliography and figures render identically.
6. The 7 TODO-AUTHOR items (declarations, DOIs, Cox/pipeline confirmations)
   must be resolved before submission, as in the working package.
7. If NPL asks for separate title-page files (for double-anonymized review),
   split the title block into a separate file per the submission system's
   instructions — note NPL's current anonymization policy determines this.
