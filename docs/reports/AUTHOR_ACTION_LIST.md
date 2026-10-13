# Part C — Author Action List

Ordered by importance for a Neural Processing Letters submission. Items 1-4 are decisions only you can make; items 5-8 are verifications. All [TODO-AUTHOR] markers in `main.tex` correspond to entries here.

## Decisions required

1. **TOST equivalence margin (Methods, Sect. 3.4; affects Sec 4.2 wording).**
   The pipeline (`../grokking-stats/results/tost.csv`, `tost_smallest_margin.csv`) reports margins 10% / 25% / 50% as ratios on log10 GrokTime. You must either (a) pick and justify a margin on substantive grounds — e.g., "a repetition effect smaller than ±25% of median GrokTime would be practically negligible because coverage shifts are 4-5x larger" — and then state which contrasts reach equivalence at that margin, or (b) keep the current wording that makes no equivalence claim. Do NOT choose the margin by looking at which one gives significance.

2. **Funding statement (Declarations).** State grant numbers or "No funding was received".

3. **Competing interests (Declarations).** State none or declare.

4. **Repository DOIs (Data & Code availability).** Suggested deposit: Zenodo figshare, or an OSF project with data + code components. The code component should include `grokking-stats/` (the exact statistical pipeline) — its `results_report.md` is the audit trail for every number in the paper.

## Verifications required

5. **AI-use statement (Declarations).** A draft is in place describing the GLM assistant as a programming/writing aid under your direction, with you taking full responsibility. Read it, correct it to match your actual workflow, and check Springer Nature's current policy (AI cannot be an author; disclosure is expected in Methods or Declarations).

6. **Two citation slots (Related work, "Positioning" paragraph).** [SUGGESTED - AUTHOR MUST VERIFY] for (a) a dedicated critical-data-fraction study in grokking, and (b) "How much can language models memorize?" (arXiv:2505.24832) / "Data mixing laws" (arXiv:2403.16952). Either verify and format them, or delete the slots — the paragraph stands without them.

7. **Deviation log items (iii)-(v) (Appendix B).** The families were re-declared post hoc (item iii), arm D was added mid-study (item iv), and the statistical procedure was corrected during revision (item v). Re-read and confirm against your internal records; extend if anything else deviated.

8. **Affiliation completeness.** Title page currently reads "Dalian University of Technology, Dalian, China". Add school/department + postal code (e.g., School of X, Dalian 116024) if the NPL title-page format requires them.

## Smaller items (optional but recommended before submission)

9. **Springer format.** The manuscript is compiled with a NeurIPS-lite style for readability. For actual submission, transfer the content into Springer's `sn-jnl.cls` (NPL template) — the text, tables, and figures port directly; watch the natbib style (currently numeric).
10. **Cover letter.** Suggested angle: seed-level, censoring-aware statistics (exact permutation tests, Kaplan-Meier/log-rank/RMST) applied to the coverage-vs-repetition question at matched dose; all code and per-run data available.
11. **Figure 3b annotation.** The Spearman rho annotated inside the figure (0.065) matches the text; the permutation p (0.55) is now the declared one — no figure change needed, just awareness if you regenerate figures.
12. **Sanity spot-check.** `../grokking-stats/results/sanity_checks.csv` reproduces 26/26 structural checks against the manuscript's descriptive claims (135 runs, 27 conditions, n_test per coverage, Table A3 rows). If you regenerate anything, re-run `python analyze.py --runs runs.csv --history history.csv --out results --margins 0.10 0.25 0.50` and confirm the report is unchanged (deterministic seeds: 20260922 + offsets).

## Where things are

- Revised manuscript (this round): `main.tex`, `main.pdf` (11 pp, compiles with tectonic)
- Statistical pipeline + full results report: `../grokking-stats/` (see `results/results_report.md`, especially sections (c) "Manuscript sentences" and (d) "Things that contradict the current manuscript")
- Round-1 revision (pre-pipeline): superseded values documented in `REVISION_LOG.md`
- Raw data: `../paper-package/data/` (135 run JSONs in `raw_runs.zip`, `history.csv`, `summary.csv`)
