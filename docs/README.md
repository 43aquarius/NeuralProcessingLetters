# Documentation

This folder holds the manuscript-related material of the repository. The
research artifact itself (training code, raw run logs, statistical pipeline,
figures, verification) lives at the repository root; see the top-level
`README.md` for its structure and usage.

## Folder guide

- **`submission/`** — the journal-submission working documents:
  the cover letter, the submission-package manifest, the release notes used
  for the GitHub release, notes on the declarations, and notes on the
  conversion to the Springer Nature `sn-jnl` template.
- **`manuscript-revised/`** — the preprint-style working version of the
  manuscript (`main.tex` + compiled `main.pdf`, 14 pages, with figures and
  bibliography). This is the version in which all revisions, audits, and
  text passes were carried out. The journal-submission version (Springer
  Nature `sn-jnl` format, 20 pages) is archived in the repository's
  [Releases](https://github.com/43aquaris/NeuralProcessingLetters/releases).
- **`reports/`** — the audit and QA trail produced while preparing the
  manuscript: reference verification, figure QA, revision changelogs, author
  action lists, the internal referee report, and the session index.

## Which manuscript version is which

| Version | Format | Location |
|---|---|---|
| Journal submission (v1.0.0, 2026-10-13) | Springer Nature `sn-jnl`, 20 pages | [Release v1.0.0](https://github.com/43aquaris/NeuralProcessingLetters/releases) — PDF + LaTeX source |
| Preprint-style working version | custom article class, 14 pages | `docs/manuscript-revised/` |

Both versions have identical scientific content (same text, numbers, figures,
and references); they differ only in template, pagination, and appendix
lettering.

## Upload record

See `submission/UPLOAD_RECORD.md` for the record of the initial repository
upload and the v1.0.0 release (2026-10-13).
