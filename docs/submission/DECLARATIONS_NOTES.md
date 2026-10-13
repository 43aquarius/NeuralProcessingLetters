# Prompt 6 — Declarations and AI-use statement: notes and verification list

The declarations section in `main.tex` (Funding, Competing interests, Ethics,
Data availability, Code availability, Author contributions, Generative AI use)
is drafted in plain factual language. Fields that depend on your facts remain
as `[TODO-AUTHOR]` placeholders — nothing was guessed.

## Current state (in main.tex)

1. **Funding** — placeholder (state sources + grant numbers, or "No funding
   was received").
2. **Competing interests** — placeholder (declare interests, or "The authors
   have no competing interests").
3. **Ethics** — stated: purely computational study, no human/animal subjects,
   no personal data, no ethics approval required.
4. **Data availability** — describes the deposit (135 per-run logs, runs.csv,
   history.csv, analysis outputs); DOI/URL placeholder.
5. **Code availability** — describes the deposit (training code, exact
   statistical pipeline, figure scripts); DOI/URL placeholder.
6. **Author contributions (CRediT)** — sole author, all fourteen roles
   collapsed to the relevant ones.
7. **Generative AI use** — now lists GLM (Z.ai) with the specific stages:
   experimental/analysis code drafting and refactoring; statistical planning;
   figure and table generation; manuscript drafting, revision, and language
   editing; the verification script that re-derives every reported
   statistic; bibliographic-record checking. Ends with the author-responsibility
   sentence and a TODO to complete/confirm the tool list.

## Consistency checks performed

- The Methods states the pipeline "is available with the code (Declarations)"
  — consistent with the Code availability paragraph.
- CRediT roles match a single-author study; the AI-use statement does not
  credit the AI tool with authorship (only with assistance), which is the
  policy-compliant framing.
- The AI-use statement's stage list matches the work record of this project
  (design, code, statistics, figures, drafting/revision, verification,
  reference checking). If any stage listed was NOT AI-assisted in your
  workflow, delete it — the TODO instructs exactly that.
- No AI tool appears in the reference list or is cited as an author.

## What you must double-check against Springer Nature's current policy

(Springer Nature/NPL author-instructions pages; do not rely on memory —
policies change.)

1. Whether NPL requires the AI-disclosure statement in a specific section,
   format, or wording (e.g., a dedicated "Declaration of Generative AI" vs. a
   footnote), and whether it must also cover figures generated with AI tools.
2. Whether AI-generated or AI-assisted figures need an explicit figure-level
   declaration (relevant if the journal counts code-generated scientific plots
   as AI output — most do not, but confirm).
3. The current definition of "large language model" assistance vs. "AI tool":
   whether niche tools (e.g., literature-search assistance) must be listed by
   name.
4. Whether the journal prohibits AI use in peer review of your own paper
   (irrelevant for the manuscript itself, but relevant if you use assistants
   to draft responses to reviewers — many publishers now allow editing but
   prohibit uploading reviewers' confidential comments into AI tools).
5. Data-availability policy details: whether a Zenodo DOI alone satisfies the
   "public at submission" requirement or whether the repository must be a
   specific type (generalist vs. domain).
6. Competing-interest definition: whether unpaid roles (reviewing, advisory
   boards) must be declared for a sole academic author.
7. The exact CRediT taxonomy version the submission system expects, and
   whether "sole author, all roles" needs explicit enumeration.
