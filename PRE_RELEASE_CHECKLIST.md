# Pre-release checklist — public repository

Work through every item before making the repository public. Items marked
[TODO-AUTHOR] need your decision or your account.

## Licence choice (decision needed)

**Code — suggested: MIT**
Simple and maximally permissive: anyone may reuse, modify, and redistribute
with attribution and without further obligations.
Trade-off: no explicit patent grant (Apache-2.0 adds one, at the cost of a
longer licence text that some readers never read).

**Code — alternative: Apache-2.0**
Same permissiveness plus an explicit patent licence and contribution terms.
Trade-off: considerably longer text; more legal weight than this small
scientific codebase needs.

**Data (JSON logs, CSVs, figures) — suggested: CC-BY-4.0**
Lets others reuse and redistribute the data freely as long as they credit you,
which protects the citation.
Trade-off: attribution is required, so purely "public-domain" reusers must
still cite you (CC0 would remove even that requirement).

**Data — alternative: CC0**
No conditions at all; maximally frictionless reuse.
Trade-off: you lose the legal hook that asks reusers to cite the work.

Zenodo allows one licence per record; if you want different licences for code
and data, deposit them as two linked records or state both in the record
description (mark the split in `README.md` and `CITATION.cff` too).

## Content checks

- [x] No absolute personal paths: all five scripts that carried development
  paths (`run_grid.py`, `aggregate_runs.py`, `make_tables.py`,
  `make_figures.py`) have been re-pointed to repo-relative locations; verified
  by re-running the aggregation + table + verification chain in place.
- [x] No credentials, API keys, or personal information beyond the author
  name/affiliation/email (grep for `key`, `token`, `secret`, `password`
  before upload: none present).
- [x] Raw per-run logs included: `data/raw/` contains the 135 main-run JSONs
  (the pilot JSONs are excluded from the analysis by design and are not part
  of the frozen grid; `data/archived_stats.json` is the legacy first-pass
  statistics file kept for the record).
- [x] `runs.csv` rebuilt byte-identically from the raw JSONs
  (sha256 `95052c36…` matches the archived analysis input; recorded in
  `results/stats/env_log.txt`).
- [x] `results/` reproducible: `aggregate_runs.py` → `make_runs_table.py` →
  `analyze.py` → `make_figures.py` → `verify_manuscript.py` all run from the
  repo with the pinned versions; the verification passes 353/353 claims.
- [x] Seeds documented: training seeds 0-4 per condition (init + unique subset
  + data order); analysis master seed 20260922 with the seven documented
  offsets (see `results/stats/env_log.txt`).
- [x] Software environment pinned in `requirements.txt` and logged in
  `results/stats/env_log.txt`.
- [x] Licence filled (2026-10-13): code MIT (`LICENSE`), data and figures
  CC-BY-4.0 (stated in `README.md`, `CITATION.cff`, `.zenodo.json`). Swap by
  editing those four places if a different choice is preferred.
- [x] Release date (2026-10-13) and repository URL
  (https://github.com/43aquaris/NeuralProcessingLetters) filled in
  `CITATION.cff` / `.zenodo.json` / `README.md`. The manuscript DOI is
  [ ] still pending — [TODO-AUTHOR] add it to all three places once the
  paper is published.
- [ ] [TODO-AUTHOR] Confirm the email address that should be public in
  `CITATION.cff` (currently the corresponding-author address).

## Deposit and release

- [x] Public repository created and pushed as the root
  (https://github.com/43aquaris/NeuralProcessingLetters, tag `v1.0.0`).
- [ ] [TODO-AUTHOR] Deposit the tagged release on Zenodo (flip the
  GitHub integration on, or upload the zip directly) to obtain the DOI.
- [ ] [TODO-AUTHOR] Paste the DOI into the manuscript's Data availability /
  Code availability declarations and in `CITATION.cff` / `.zenodo.json`.
- [x] Repository is public before submission (visibility confirmed via the
  GitHub API on 2026-10-13).
- [x] Final grep for `/home/` and local usernames in all committed files
  before the first push (re-run 2026-10-13 on the final staged tree: clean;
  see the upload record in `docs/submission/`).
- [ ] [TODO-AUTHOR] After deposit, re-run `verify_manuscript.py` once on the
  downloaded-from-Zenodo copy and store the report with the release.
