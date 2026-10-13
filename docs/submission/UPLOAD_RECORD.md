# Upload record — initial repository upload and v1.0.0 release (2026-10-13)

## What was done

1. **Manuscript declarations finalized** (user-confirmed facts):
   - Funding: *No funding was received.*
   - Competing interests: *The author has no competing interests.*
   - Data availability / Code availability: repository URL filled in
     (`https://github.com/43aquarius/NeuralProcessingLetters`, tag `v1.0.0`),
     with the sentence "The repository is public at the time of submission"
     (visibility confirmed via the GitHub API before the release was
     packaged). Both manuscript versions (`main-sn.tex` and the
     preprint-style `main.tex`) were updated identically and recompiled
     (20 pages / 14 pages; no new warnings).
2. **Repository metadata finalized**:
   - Licence decision applied (the pre-release checklist's suggested
     defaults): code **MIT** (`LICENSE` added; copyright 2026 Chang Tan),
     data and figures **CC-BY-4.0** (stated in `README.md`, `CITATION.cff`,
     `.zenodo.json`). This choice is easy to change — edit those four
     places and push.
   - `CITATION.cff` / `.zenodo.json`: repository URL and release date
     (2026-10-13) filled; the manuscript DOI is deliberately left pending
     publication.
   - `README.md`: manuscript pointer now targets this repository's Releases
     page; `docs/` added to the folder tree.
3. **Repository content pushed** (branch `main`, tagged `v1.0.0`):
   - root: the research artifact (code, data, results) — 135 raw run logs,
     canonical tables, statistical pipeline, figures, verification report.
   - `docs/submission/`, `docs/manuscript-revised/`, `docs/reports/`:
     submission working documents, the preprint-style manuscript, and the
     full audit/QA trail.
   - Excluded on purpose: superseded first-draft package (contained numbers
     corrected during revision), internal `.tex` backups, and duplicate
     verification copies.
4. **Release `v1.0.0` created** with the complete submission package:
   `NPL-submission-package-v1.0.0.zip` (manuscript PDF + LaTeX source +
   figures + cover letter + manifest) and `manuscript-sn-v1.0.0.pdf`.
   Post-upload check: the PDF asset object was re-uploaded once
   (identical content, sha256-verified against the local file) after the
   freshly-created repository showed GitHub-side cache-propagation delays
   on the public download URLs; the repository itself, the release, and
   both assets are complete and verified through the API (asset states
   `uploaded`, byte-identical downloads).

## Pre-push safety checks (all on the final staged tree)

- No absolute personal paths (`/home/...`) in any committed file.
- No credentials, tokens, or API keys in any committed file (searched for
  the literal token strings used during the upload itself).
- `verify_manuscript.py` last full run on the archived pipeline: 353/353
  claims verified (report at `results/stats/verification_report.csv`).
- The release package compiles standalone from the zip contents
  (`tectonic main-sn.tex`).

## Still open for the author (also tracked in PRE_RELEASE_CHECKLIST.md)

- Zenodo deposit of the tagged release to obtain a citable DOI, if desired;
  then paste the DOI into the availability statements and `CITATION.cff` /
  `.zenodo.json` / `README.md`.
- Manuscript DOI everywhere, after acceptance.
- Confirm the public email address in `CITATION.cff`.
