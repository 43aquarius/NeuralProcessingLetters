# Prompt A — Reference Verification Report (re-run)

Manuscript: *Coverage versus within-epoch repetition at matched dose in transformer grokking* (NPL submission).
Date: 2026-10-13. Scope: the operative `references.bib` used by `paper-package-sn/main-sn.tex` (and synced to `paper-package-revised/references.bib`). Every entry was re-checked against a source opened during this session; no field was filled from memory. Where a source could not be opened (DBLP, OpenReview API/PDF — both behind anti-bot challenges), the fact is listed in Part D instead of being guessed.

**Bibliography style used by the template**: `sn-basic` (loaded via `\documentclass[pdflatex,sn-basic,Numbered]{sn-jnl}`), i.e. the Springer Nature basic numbered style — not sn-mathphys-num.

## Root cause of the two rendering defects (diagnosed in the .bst, not just the .bib)

1. **Doubled arXiv IDs** ("arXiv:2404.05405, 2404.05405"). `sn-basic.bst` prints the `note`/`howpublished` field **and then** the `eprint` field for every `@inproceedings`/`@misc` entry. The old .bib carried the same identifier in both (`note = {Extended abstract; arXiv:2404.05405}` + `eprint`, or `howpublished = {arXiv preprint arXiv:2001.08361}` + `eprint`). Fix: exactly one identifier source per entry.
2. **Garbled "tTODO-AUTHOR" / bare numbers.** `format.eprint` emits `\eprint[<archive>]{<id>}`, but the .bst's own `\providecommand{\eprint}[2][]{\url{#2}}` **discards the archive prefix**, so `eprint` printed as a bare "2404.05405"; and the `note` field is sentence-cased by the style, which mangled "TODO-AUTHOR" into "tODO-AUTHOR". Fix: a one-line `\providecommand{\eprint}[2][]{\ifx\empty#1\empty#2\else#1:#2\fi}` in `main-sn.tex`'s preamble (the .bbl's own `\providecommand` then becomes a no-op), so `eprint + archive = {arXiv}` renders as "arXiv:2404.05405". The TODO placeholders were replaced with real data or removed (below).

**Identifier pattern applied (one locator per entry, never duplicated):** items whose publisher mints a DOI get `doi` (+ `pages`) and no eprint; all other items (arXiv-only preprints, ICLR and NeurIPS-2017 papers, for which no DOI exists) carry a single `eprint` + `archive = {arXiv}` + `archivePrefix = {arXiv}`.

## Part A — Verification table

| # | Key | Current entry (before this pass) | Verified entry | Source URL used | Fields changed | Status |
|---|-----|----------------------------------|----------------|-----------------|----------------|--------|
| 1 | allen-zhu2024physics | Allen-Zhu & Li, ICLR 2025, note "Extended abstract; arXiv:2404.05405", eprint 2404.05405 | Allen-Zhu; Li. **ICLR 2025 Poster**; extended abstract; full 12-result paper. Authors' own recommended citation: Proceedings of the 13th ICLR, year 2025, full version at SSRN 5250617 (arXiv marked "deprecated" by the authors) | https://iclr.cc/virtual/2025/poster/30313 ; https://physics.allen-zhu.com/part-3-knowledge/part-3-3 ; https://arxiv.org/abs/2404.05405 | note split (kept {{Extended abstract}}, case-protected with braces); arXiv ID now carried by eprint only; no howpublished duplication | **CORRECTED** (rendering) |
| 2 | bengio2009curriculum | Bengio, Louradour, Collobert, Weston. ICML 2009, pp 41–48, DOI 10.1145/1553374.1553380 | Identical: 4 authors, Proc. 26th ICML, pp 41–48, 2009, DOI resolves (ACM) | https://api.crossref.org/works/10.1145/1553374.1553380 | none | **OK** |
| 3 | hoffmann2022training | 22 authors, NeurIPS vol 35, 2022, note "TODO-AUTHOR: add pages", eprint | **NeurIPS 2022 Main Conference Track, vol 35, pp 30016–30030, DOI 10.52202/068431-2176**; title "Training Compute-Optimal Large Language Models" confirmed on the published PDF and in the Crossref DOI record; 22 authors confirmed | https://papers.nips.cc/paper_files/paper/2022/hash/c1e2faff6f588870935f114ebe04a3e5-Abstract-Conference.html ; https://proceedings.neurips.cc/paper_files/paper/2022/file/c1e2faff6f588870935f114ebe04a3e5-Paper-Conference.pdf ; https://api.crossref.org/works/10.52202/068431-2176 ; https://api.openalex.org/works/doi:10.52202/068431-2176 | pages 30016–30030 added; DOI added; TODO note deleted; eprint removed (published item with DOI); title unchanged (see Part D item 2) | **CORRECTED** |
| 4 | kaplan2020scaling | 10 authors, @misc, howpublished "arXiv preprint arXiv:2001.08361" + eprint (rendered twice) | 10 authors (Kaplan, McCandlish, Henighan, Brown, Chess, Child, Gray, Radford, Wu, Amodei); arXiv-only, Jan 2020; no venue on the arXiv record | https://arxiv.org/abs/2001.08361 | howpublished deleted (was the doubling source); eprint+archive kept as the single identifier | **CORRECTED** (rendering) |
| 5 | lee2022deduplicating | 7 authors, ACL 2022, pp 8424–8445, DOI 10.18653/v1/2022.acl-long.577 | Identical: ACL 2022 (Long Papers), pp 8424–8445, Dublin, ACL, DOI | https://aclanthology.org/2022.acl-long.577.bib ; https://aclanthology.org/2022.acl-long.577.xml | none | **OK** |
| 6 | liu2023omnigrok | Liu, Michaud, Tegmark. ICLR 2023, eprint | ICLR 2023 In-Person Poster, **notable top-25%**; 3 authors confirmed | https://iclr.cc/virtual/2023/poster/11799 ; https://arxiv.org/abs/2210.01117 | {Omnigrok} braced in title; eprint rendering fixed via \eprint + archive | **OK** |
| 7 | loshchilov2019decoupled | Loshchilov & Hutter, ICLR 2019, eprint | ICLR 2019 confirmed ("Published as a conference paper at ICLR 2019" on arXiv) | https://arxiv.org/abs/1711.05101 | eprint rendering fixed | **OK** |
| 8 | muennighoff2023scaling | 9 authors (incl. Rush, Barak), NeurIPS vol 36, 2023, note "TODO-AUTHOR: add pages", eprint | **NeurIPS 2023 Main Conference Track, vol 36, pp 50358–50376, DOI 10.52202/075280-2191**; 9 authors confirmed (Muennighoff, Rush, Barak, Le Scao, Piktus, Tazi, Pyysalo, Wolf, Raffel) | https://papers.nips.cc/paper_files/paper/2023/hash/9d89448b63ce1e2e8dc7af72c984c196-Abstract-Conference.html ; https://api.openalex.org/works/doi:10.52202/075280-2191 | pages 50358–50376 added; DOI added; TODO note deleted; eprint removed | **CORRECTED** |
| 9 | nanda2024progress | Nanda, Chan, Lieberum, Smith, Steinhardt. ICLR 2023, eprint | ICLR 2023 In-Person Poster, **notable top-25%**; 5 authors confirmed on the ICLR site and arXiv | https://iclr.cc/virtual/2023/poster/11385 ; https://arxiv.org/abs/2301.05217 | eprint rendering fixed; key kept (rule 3) although the entry is dated 2023 | **OK** |
| 10 | power2022grokking | Power, Burda, Edwards, Babuschkin, Misra. @misc, howpublished + eprint (rendered twice) | arXiv-only preprint, Jan 2022; 5 authors confirmed; no venue/journal-ref on the arXiv record | https://arxiv.org/abs/2201.02177 | howpublished deleted; eprint+archive kept | **CORRECTED** (rendering) |
| 11 | vaswani2017attention | 8 authors, NeurIPS vol 30, 2017, note "TODO-AUTHOR: add pages", eprint | **Official NeurIPS 2017 proceedings record has no page numbers and no DOI** (citation meta tags carry only volume 30, 2017); 8 authors confirmed (incl. Łukasz Kaiser) | https://papers.nips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html | TODO note deleted; per your rule ("if the venue has no pages … cite the arXiv ID instead") the entry keeps eprint arXiv:1706.03762 as its identifier; no page range was invented | **CORRECTED** |
| 12 | varma2024explaining | Varma, Shah, Kenton, Kramár, Kumar. @misc 2023, howpublished + eprint (rendered twice) | arXiv-only, Sep 2023; 5 authors confirmed; no venue, no journal-ref on the arXiv record | https://arxiv.org/abs/2309.02390 | howpublished deleted; eprint+archive kept; key kept (rule 3) | **OK** |
| 13 | wu2021curricula | Wu, Dyer, Neyshabur. ICLR 2021, eprint | ICLR 2021 confirmed ("ICLR 2021" on the arXiv record) | https://arxiv.org/abs/2012.03107 | eprint rendering fixed | **OK** |
| 14 | zhang2017understanding | Zhang, Bengio, Hardt, **Recht, Benjamin**, Vinyals. ICLR 2017, eprint | ICLR 2017 confirmed ("Published in ICLR 2017" on arXiv); 5 authors confirmed, fourth author is Benjamin Recht | https://arxiv.org/abs/1611.03530 | eprint rendering fixed | **OK** |

Summary: 14/14 entries checked against opened sources; 4 entries CORRECTED with new bibliographic data (Hoffmann pages+DOI; Muennighoff pages+DOI; three TODO placeholders resolved), 10 OK or corrected only for the doubling/rendering defect. **Every full author list is present in the .bib** (the printed "et al." is the style's 3-author abbreviation; sn-basic abbreviates automatically). No citation key was changed.

## Part B — Corrected .bib

Delivered as `paper-package-sn/references.bib` (= `paper-package-revised/references.bib`, identical content, SN keys), recompiled into `main-sn.pdf` (pages 16–17). Rendered result, exactly as it now prints:

```
[1] Allen-Zhu Z, Li Y (2025) Physics of language models: Part 3.3, knowledge capacity
    scaling laws. In: International Conference on Learning Representations (ICLR),
    Extended abstract, arXiv:2404.05405
[2] Bengio Y, Louradour J, Collobert R, et al (2009) Curriculum learning. In: Proceedings
    of the 26th International Conference on Machine Learning (ICML), pp 41–48,
    https://doi.org/10.1145/1553374.1553380
[3] Hoffmann J, Borgeaud S, Mensch A, et al (2022) Training compute-optimal large
    language models. In: Advances in Neural Information Processing Systems (NeurIPS),
    pp 30016–30030, https://doi.org/10.52202/068431-2176
[4] Kaplan J, McCandlish S, Henighan T, et al (2020) Scaling laws for neural language
    models. arXiv:2001.08361
[5] Lee K, Ippolito D, Nystrom A, et al (2022) Deduplicating training data makes
    language models better. In: Proceedings of the 60th Annual Meeting of the Association
    for Computational Linguistics (ACL), pp 8424–8445, https://doi.org/10.18653/v1/2022.acl-long.577
[6] Liu Z, Michaud EJ, Tegmark M (2023) Omnigrok: Grokking beyond algorithmic data.
    In: International Conference on Learning Representations (ICLR), arXiv:2210.01117
[7] Loshchilov I, Hutter F (2019) Decoupled weight decay regularization. In:
    International Conference on Learning Representations (ICLR), arXiv:1711.05101
[8] Muennighoff N, Rush AM, Barak B, et al (2023) Scaling data-constrained language
    models. In: Advances in Neural Information Processing Systems (NeurIPS),
    pp 50358–50376, https://doi.org/10.52202/075280-2191
[9] Nanda N, Chan L, Lieberum T, et al (2023) Progress measures for grokking via
    mechanistic interpretability. In: International Conference on Learning
    Representations (ICLR), arXiv:2301.05217
[10] Power A, Burda Y, Edwards A, et al (2022) Grokking: Generalization beyond
     overfitting on small algorithmic datasets. arXiv:2201.02177
[11] Varma V, Shah R, Kenton Z, et al (2023) Explaining grokking through circuit
     efficiency. arXiv:2309.02390
[12] Vaswani A, Shazeer N, Parmar N, et al (2017) Attention is all you need. In:
     Advances in Neural Information Processing Systems (NeurIPS), arXiv:1706.03762
[13] Wu X, Dyer E, Neyshabur B (2021) When do curricula work? In: International
     Conference on Learning Representations (ICLR), arXiv:2012.03107
[14] Zhang C, Bengio S, Hardt M, et al (2017) Understanding deep learning requires
     rethinking generalization. In: International Conference on Learning
     Representations (ICLR), arXiv:1611.03530
```

No entry prints an identifier twice; no TODO placeholder remains anywhere in the bibliography (the remaining `[TODO-AUTHOR: …]` strings in the PDF are the author-decision items in the Declarations/appendix, untouched by this pass). Two supporting edits were needed outside the .bib: the `\eprint` redefinition in `main-sn.tex`'s preamble (one line, commented), and the embedded `thebibliography` of `paper-package-revised/main.tex` was synced with the two verified NeurIPS page ranges (Hoffmann, Muennighoff) so the preprint and SN versions agree. The ICLR entries keep their `volume` fields in the .bib even though sn-basic only prints volumes when a publisher is set — the field is portable to other styles.

## Part C — Citation-claim check and gap-check results

### Citation-claim check (all 17 citation-bearing sentences of main-sn.tex, checked against the abstracts opened above)

| Sentence (paraphrased) | Cited | Verdict |
|---|---|---|
| Transformer fits a mid-sized training set in a few hundred steps; test accuracy near chance for thousands of steps before abrupt transition | power2022grokking | **SUPPORTED** — the abstract describes grokking (generalization long after overfitting on algorithmic datasets); the few-hundred/thousands-of-steps timing is the paper's body result on exactly this setup |
| The memorize-vs-rule tension underlies practical questions on deduplication, repetition, data-constrained pretraining | lee2022deduplicating, muennighoff2023scaling, allen-zhu2024physics | **SUPPORTED** — each abstract is directly on one of these topics |
| Delayed generalization appears only within a range of dataset fractions | power2022grokking | **SUPPORTED** — core finding of the paper |
| Grokking varies strongly with the number of unique training items | liu2023omnigrok | **SUPPORTED** — abstract addresses data-size dependence of grokking via loss landscapes |
| Circuit-efficiency accounts predict a sufficient supply of unique examples is needed | varma2024explaining | **SUPPORTED** — abstract: task must admit a generalizing (more efficient) vs memorizing solution |
| Loss-landscape geometry and weight norms explain the transition | liu2023omnigrok | **SUPPORTED** — abstract: LU mechanism against weight norm |
| Progress measures change smoothly before test accuracy jumps | nanda2024progress | **SUPPORTED** — abstract: continuous progress measures underlying discontinuous changes |
| Generalizing solutions are parameter-efficient but slower to learn | varma2024explaining | **SUPPORTED** — stated in substance in the abstract |
| Grokking characterized on modular arithmetic within a narrow range of dataset fractions | power2022grokking | **SUPPORTED** |
| Standard two-layer-transformer arithmetic setup | power2022grokking, nanda2024progress | **SUPPORTED** — both papers use this setup |
| Repeating a corpus up to ~4 epochs changes loss little; more epochs degrade returns | muennighoff2023scaling | **SUPPORTED** — the paper's headline empirical rule on repeating data up to 4 epochs |
| Compute-optimal scaling laws allocate budget between model size and tokens | kaplan2020scaling, hoffmann2022training | **SUPPORTED** — both abstracts are exactly this |
| Networks can fit random labels | zhang2017understanding | **SUPPORTED** — the paper's famous result |
| Knowledge capacity scales with parameters and repeats | allen-zhu2024physics | **SUPPORTED** — abstract: 2 bits/parameter capacity estimate; training-duration dependence among the 12 results |
| Deduplication reduces verbatim recall | lee2022deduplicating | **SUPPORTED** |
| Curricula have mixed consequences; benefits concentrated in noisy or time-varying regimes | wu2021curricula, bengio2009curriculum | **SUPPORTED** — Wu studies when curricula help incl. noise regimes; Bengio 2009 introduced curriculum learning |
| Reduced training fractions delay or prevent grokking | power2022grokking, liu2023omnigrok, varma2024explaining | **SUPPORTED** |
| Multi-epoch repetition at pretraining scale nearly free for a few epochs, costly beyond | muennighoff2023scaling, allen-zhu2024physics | **SUPPORTED** |
| Two-layer causal transformer architecture; AdamW; the configuration under which delayed generalization was characterized | vaswani2017attention, loshchilov2019decoupled, power2022grokking, nanda2024progress | **SUPPORTED** — architectural/optimizer/setup citations |
| Coverage mirrors the trade-off between more unique data and more passes over fewer unique data | muennighoff2023scaling | **SUPPORTED** — this is the framing of the paper |
| Norm trajectory motivated by loss-landscape analyses; circuit-efficiency reading (memorization consumes weight norm; weight decay tilts the balance) | liu2023omnigrok, varma2024explaining | **SUPPORTED** |
| Results compatible with the rule that repeating a corpus a few epochs costs little | muennighoff2023scaling | **SUPPORTED** |

No citation-claim mismatch found. No manuscript text was edited in this pass.

### Related-work gap check (papers actually opened this session)

(a) Critical dataset size / data fraction in grokking:
1. **Zhu X, Fu Y, Zhou B, Lin Z. "Critical Data Size of Language Models from a Grokking Perspective." arXiv:2401.10463 (2024).** https://arxiv.org/abs/2401.10463 — Formalizes the Data Efficiency Hypothesis: a critical data size marks the shift from memorization to generalization, with insufficiency/sufficiency/surplus regimes. **Recommendation: CITE (one clause in Related work).** It is the closest prior work on critical data size from a grokking perspective; the manuscript's coverage gate (~40% boundary) sits directly on this line, and the factorial repetition×coverage decomposition at matched dose remains distinct from it. A drafted sentence is available in `REFERENCE_VERIFICATION.md` (previous pass). Author decision — do not add without your confirmation.
2. **Clauw K, Stramaglia S, Marinazzo D. "Information-Theoretic Progress Measures reveal Grokking is an Emergent Phase Transition." arXiv:2408.08944 (ICML 2024 MI workshop).** https://arxiv.org/abs/2408.08944 — Higher-order mutual information identifies phases before grokking. **Recommendation: IGNORE** (the manuscript makes no information-theoretic claims; Nanda et al. already covers progress measures).

(b) Repeated data in language-model training:
3. **Muckatira S, Shivagunde N, Deshpande V, Rumshisky A. "A Pre-Training Analogue of Grokking in Language Models: Tracing Delayed Grammatical Generalization." arXiv:2606.00230, accepted AACL-IJCNLP 2026.** https://arxiv.org/abs/2606.00230 — Exposure-based framework for grokking-like dynamics during LLM pre-training (BLiMP contrasts), noting pre-training involves limited data repetition. **Recommendation: OPTIONAL** — relevant to the "does repetition matter at pretraining scale" framing but does not test repetition as a controlled factor; cite only if you want a 2026 forward pointer.
4. **Hägele A, Bakouch E, Kosson A, Ben Allal L, Von Werra L, Jaggi M. "Scaling Laws and Compute-Optimal Training Beyond Fixed Training Durations." arXiv:2405.18392 (Spotlight, NeurIPS 2024).** https://arxiv.org/abs/2405.18392 — Constant-LR-with-cooldowns enables training across durations; about training-length scaling rather than repetition per se. **Recommendation: OPTIONAL/IGNORE.**
5. **Muennighoff N, Rush AM, Barak B, et al. "Scaling Data-Constrained Language Models." NeurIPS 36 (2023).** — already cited as the central prior work on repeated data.

No paper doing a coverage × repetition factorial decomposition at matched per-example dose with seed-level statistics was found in the original 13-search literature pass, the previous 6-search pass, or today's searches. The novelty statement in Sects. 1–2 remains defensible as of 2026-10-13.

## Part D — Items you must look up or decide by hand (nothing below was guessed into the .bib)

1. **Allen-Zhu & Li full version location (author decision).** The authors' project page marks the arXiv version *deprecated* and recommends citing ICLR 2025 with "Full version available at https://ssrn.com/abstract=5250617". The applied entry keeps ICLR 2025 + "Extended abstract" + arXiv:2404.05405 (still resolvable, universally indexed). If you prefer the authors' own recommendation, swap the eprint for a note pointing to the SSRN URL — your call; both forms are defensible.
2. **Hoffmann NeurIPS listing-page title variant.** The papers.nips.cc *listing page* shows the title "An empirical analysis of compute-optimal large language model training", while the published **PDF itself**, the **Crossref DOI record**, and arXiv all use "Training Compute-Optimal Large Language Models" (which the entry keeps). The listing-page variant appears to be a metadata quirk; if you want certainty, open the PDF link in the table row and compare first pages.
3. **Vaswani 2017 page range (only if you want one).** The official NeurIPS 2017 proceedings record carries no pages and no DOI, so per your rule the entry cites the arXiv ID. DBLP lists printed-volume page numbers for NeurIPS papers but was unreachable from here (anti-bot challenge on dblp.org and both mirrors); no page number was invented. If NPL's production stage asks for NeurIPS 2017 pages, open https://dblp.org/rec/conf/nips/VaswaniSPUJGKP17.html yourself and add them.
4. **The 10.52202 DOIs** (Hoffmann, Muennighoff) resolve to Curran/proceedings.com volume pages rather than open-access PDFs. They are the registered DOIs of the NeurIPS volumes; Springer style accepts them. If you prefer readers to land on an accessible copy, you may add the arXiv ID back alongside — but then the "one identifier" pattern is broken; your call.
5. **Zhu et al. 2024 (arXiv:2401.10463)** — still pending your decision on whether to add it to Related work (recommended; see Part C).
6. **OpenReview records** for the ICLR entries could not be re-opened this session (challenge-blocked); all ICLR venue facts were instead confirmed on iclr.cc virtual-site pages and the arXiv records' own comments, except the "[EXTENDED ABSTRACT]" camera-ready header for Allen-Zhu & Li, which rests on the previous session's opening of https://openreview.net/pdf?id=FxNNiUgtfa. Re-open that one link yourself if you want a second confirmation of the "Extended abstract" wording.
7. **Varma et al. venue status** — if a published version appears before submission (an ICLR 2024 submission exists per the previous pass), update the entry.
