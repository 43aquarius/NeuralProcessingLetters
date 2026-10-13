# Session deliverables index (2026-10-12)

Completion of the Part 1–3 plan (prompts 1–9) on the NPL manuscript
"Coverage versus within-epoch repetition at matched dose in transformer
grokking". Paths below are those of the preparation workspace; in this
repository the corresponding material lives under `docs/` (see
`docs/README.md`), and the journal-submission manuscript is archived in the
[Releases](https://github.com/43aquaris/NeuralProcessingLetters/releases).

## 1. Manuscript (working package) — `paper-package-revised/`

| File | What it is |
|---|---|
| `main.tex` / `main.pdf` | Current manuscript, 14 pages; all Prompt 1 edits + reference corrections + AI-use declaration update + fixed figures |
| `references.bib` | Verified bibliography (14 entries, manuscript cite keys) |
| `REFERENCE_VERIFICATION.md` | Prompt 2 report: 14-entry verification table with sources, 6 corrections (Muennighoff authors, Nanda authors+year, Varma authors+venue, B. Recht, Allen-Zhu ICLR 2025, pages/volumes), citation-claim check, related-work gap check (Zhu et al. 2024 recommended) |
| `FIGURE_FIXES.md` | Prompt 4 report: Fig 1c labels, Fig 3a legend, Fig 3b ticks fixed; Fig 2 already clean; KM budget-line report |
| `DECLARATIONS_NOTES.md` | Prompt 6: declarations state + Springer-policy double-check list |
| `REFEREE_REPORT.md` | Prompt 8: simulated referee report, 10 ranked criticisms with dispositions, minor issues, response shells |
| `COVER_LETTER.md` | Prompt 9: cover letter draft, reviewer-area profiles (no invented names), COI checks, submission-system fields |
| `figs/`, `figs/png300/` | Manuscript figures (PDF + 300 dpi PNG), regenerated with fixes |
| Prior round documents | `FINAL_*_CHANGELOG.md`, `*_ACTION_LIST.md`, `REVISION_LOG.md`, backups `main_backup_round*.tex` |

## 2. Springer template package — `paper-package-sn/`

| File | What it is |
|---|---|
| `main-sn.tex` / `main-sn.pdf` | sn-jnl conversion (sn-basic numbered style), 21 pages, compiles clean; BibTeX bibliography |
| `references.bib`, `sn-jnl.cls`, `sn-basic.bst` | Template + verified bibliography |
| `CONVERSION_NOTES.md` | Change table, compile warnings, remaining manual steps (NPL option checks, line numbering, affiliation detail) |

## 3. Verification pipeline — `grokking-stats/`

| File | What it is |
|---|---|
| `verify_manuscript.py` | Prompt 3 script: unit tests + all 353 manuscript claims recomputed from runs.csv/history.csv |
| `verification_report.csv` | Final run: **353/353 PASS, 0 FAIL** |
| `VERIFY_README.md` | Column assumptions, seeds, tolerance policy, claims that cannot be checked from files |

## 4. Public repository (pre-deposit) — `public-repo/`

| File | What it is |
|---|---|
| `README.md` | Purpose, structure, installation, one-run/grid/analysis/verification instructions, table-and-figure provenance, seeds |
| `requirements.txt` | Exact pinned versions (torch 2.14.0, numpy 2.1.3, scipy 1.14.1, pandas 2.2.3, matplotlib 3.9.2) |
| `CITATION.cff`, `.zenodo.json` | With [TODO-AUTHOR] placeholders (title/DOI/licence/dates) |
| `PRE_RELEASE_CHECKLIST.md` | Licence options (MIT vs Apache-2.0; CC-BY-4.0 vs CC0) with trade-offs, deposit steps |
| `code/`, `data/`, `results/` | Path-parameterized scripts (smoke-tested end-to-end: runs.csv rebuilds byte-identical), 135 raw run logs, canonical tables, all result CSVs and figures |

## Manuscript TODO count (all author-decision items)

8 in-text TODO-AUTHOR items remain: Cox-specification confirmation, pipeline
re-run confirmation, funding, competing interests, data DOI, code DOI, AI-tool
list completion, deviation-log verification — plus the affiliation comment
and the commented title alternatives (delete before submission).

## Remaining for the author (Part 1 items only you can do)

1. Funding and competing interests (facts).
2. Complete the AI-tool list in the declaration.
3. Create the public repository, get the Zenodo DOI (checklist provided).
4. Check current NPL author guidelines (abstract limit ≈ 254 words now;
   template options; line numbering; OA route).
5. Decide on Prompt 10 extra experiments (second modulus or more seeds at
   35–45% recommended; pre-run analysis plan not yet drafted — ask if wanted).
