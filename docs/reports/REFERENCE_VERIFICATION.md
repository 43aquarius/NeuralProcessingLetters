# Prompt 2 — Reference Verification Report

Manuscript: *Coverage versus within-epoch repetition at matched dose in transformer grokking*
Date: 2026-10-12. Every entry below was checked against an opened, authoritative source (arXiv metadata page, OpenReview, ACL Anthology, Crossref, NeurIPS virtual site, publisher/OpenReview PDF). No field was filled from memory.

## Part 1 — Verification table

| # | Key | Current entry (as in main.tex before this pass) | Verified entry | Source URL used | Discrepancies | Status |
|---|-----|--------------------------------------------------|----------------|-----------------|---------------|--------|
| 1 | allen-zhu2024physics | Z. Allen-Zhu and Y. Li. … Part 3.3, knowledge capacity scaling laws. **ICML, 2024.** arXiv:2404.05405 | Zeyuan Allen-Zhu; Yuanzhi Li. **ICLR 2025** (poster, extended abstract); arXiv:2404.05405 (Apr 2024) | https://openreview.net/pdf?id=FxNNiUgtfa (camera-ready header: "Published as a conference paper at ICLR 2025 … [EXTENDED ABSTRACT]"); https://iclr.cc/virtual/poster (2025 Poster listing) | Venue and year wrong: ICML 2024 → ICLR 2025 (extended abstract) | **CORRECTED** |
| 2 | bengio2009curriculum | Y. Bengio, J. Louradour, R. Collobert, and J. Weston. Curriculum learning. ICML, 2009 | Yoshua Bengio; Jérôme Louradour; Ronan Collobert; Jason Weston. Proc. 26th Int. Conf. on Machine Learning (ICML '09), ACM, **pages 41–48**, 2009. DOI 10.1145/1553374.1553380 | https://api.crossref.org/works/10.1145/1553374.1553380 ; https://dl.acm.org/doi/10.1145/1553374.1553380 | Authors and venue OK; pages added (41–48). Note: one secondary source (bibbase) showed "pages 1–8"; the Crossref/ACM record (41–48) is authoritative | OK (pages added) |
| 3 | hoffmann2022training | J. Hoffmann, S. Borgeaud, A. Mensch, et al. Training compute-optimal large language models. NeurIPS, 2022 | 22 authors (Hoffmann, Borgeaud, Mensch, Buchatskaya, Cai, Rutherford, de Las Casas, Hendricks, Welbl, Clark, Hennigan, Noland, Millican, van den Driessche, Damoc, Guy, Osindero, Simonyan, Elsen, Rae, Vinyals, Sifre). Advances in NeurIPS **35** (NeurIPS 2022); arXiv:2203.15556 | https://arxiv.org/abs/2203.15556 ; https://proceedings.neurips.cc (36th Conf., 2022) | First three named authors correct; volume 35 added. Page range not verified (not required in NPL style) | OK |
| 4 | kaplan2020scaling | J. Kaplan, S. McCandlish, T. Henighan, et al. Scaling laws for neural language models. arXiv:2001.08361, 2020 | 10 authors (Kaplan, McCandlish, Henighan, Brown, Chess, Child, Gray, Radford, Wu, Amodei). arXiv preprint arXiv:2001.08361 (Jan 2020); never published at a venue | https://arxiv.org/abs/2001.08361 | None | OK |
| 5 | lee2022deduplicating | K. Lee, D. Ippolito, A. Nystrom, C. Zhang, D. Eck, C. Callison-Burch, and N. Carlini. … ACL, 2022 | Katherine Lee; Daphne Ippolito; Andrew Nystrom; Chiyuan Zhang; Douglas Eck; Chris Callison-Burch; Nicholas Carlini. Proc. 60th ACL, **pages 8424–8445**, 2022. DOI 10.18653/v1/2022.acl-long.577 | https://aclanthology.org/2022.acl-long.577/ ; https://arxiv.org/abs/2107.06499 ("Accepted to ACL 2022") | None; full venue name and pages added | OK |
| 6 | liu2023omnigrok | Z. Liu, E. J. Michaud, and M. Tegmark. Omnigrok … ICLR, 2023 | Ziming Liu; Eric J. Michaud; Max Tegmark. ICLR 2023, notable top 25%; arXiv:2210.01117 | https://api.openreview.net/notes/search (record zDiHoIWa0q1: "ICLR 2023 notable top 25%") ; https://arxiv.org/abs/2210.01117 | None | OK |
| 7 | loshchilov2019decoupled | I. Loshchilov and F. Hutter. Decoupled weight decay regularization. ICLR, 2019 | Ilya Loshchilov; Frank Hutter. ICLR 2019; arXiv:1711.05101 | https://arxiv.org/abs/1711.05101 (comments: "Published as a conference paper at ICLR 2019") | None | OK |
| 8 | muennighoff2023scaling | N. Muennighoff, **H. Kapoor, P. Wang,** et al. … NeurIPS, 2023 | 9 authors: Niklas Muennighoff; **Alexander M. Rush; Boaz Barak;** Teven Le Scao; Aleksandra Piktus; Nouamane Tazi; Sampo Pyysalo; Thomas Wolf; Colin Raffel. NeurIPS 2023 (poster); Advances in NeurIPS 36; arXiv:2305.16264 | https://arxiv.org/abs/2305.16264 ; https://neurips.cc/virtual/2023/poster | **Author list wrong**: 2nd and 3rd named authors were invented (H. Kapoor, P. Wang do not appear on this paper). Corrected to A. Rush, B. Barak | **CORRECTED** |
| 9 | nanda2024progress | **N. Nanda, A. Lee, M. Wattenberg, and J. Lindsey.** … **ICLR, 2024** | 5 authors: **Neel Nanda; Lawrence Chan; Tom Lieberum; Jess Smith; Jacob Steinhardt. ICLR 2023, notable top 25%**; arXiv:2301.05217 | https://api.openreview.net/notes/search (record 9XFSbDPmdW: "ICLR 2023 notable top 25%", full author list) ; https://arxiv.org/abs/2301.05217 | **Author list completely wrong** (only first author correct; "A. Lee, M. Wattenberg, J. Lindsey" are not authors) **and year wrong** (ICLR 2023, not 2024) | **CORRECTED** |
| 10 | power2022grokking | A. Power, Y. Burda, H. Edwards, I. Babuschkin, and V. Misra. Grokking … arXiv:2201.02177, 2022 | Alethea Power; Yuri Burda; Harri Edwards; Igor Babuschkin; Vedant Misra. arXiv preprint arXiv:2201.02177 (Jan 2022); no formal venue found | https://arxiv.org/abs/2201.02177 | None (arXiv-only citation is correct) | OK |
| 11 | vaswani2017attention | A. Vaswani, N. Shazeer, N. Parmar, et al. Attention is all you need. NeurIPS, 2017 | 8 authors (Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin). Advances in NeurIPS **30** (NIPS 2017); arXiv:1706.03762 | https://arxiv.org/abs/1706.03762 | None; volume 30 added | OK |
| 12 | varma2024explaining | **V. Varma, B. R. Chughtai, M. Willi, et al.** … **ICLR, 2024** | 5 authors: **Vikrant Varma; Rohin Shah; Zachary Kenton; János Kramár; Ramana Kumar.** **arXiv preprint arXiv:2309.02390, 2023** — NOT published at a venue | https://arxiv.org/abs/2309.02390 ; OpenReview forum 7Zbg38nA0J (venue "Submitted to ICLR 2024", i.e., not accepted); DBLP shows CoRR only | **Author list completely wrong** (Chughtai/Willi are not authors of this paper) **and venue wrong** (submitted to ICLR 2024 but not accepted; arXiv-only) | **CORRECTED** |
| 13 | wu2021curricula | X. Wu, E. Dyer, and B. Neyshabur. When do curricula work? ICLR, 2021 | Xiaoxia Wu; Ethan Dyer; Behnam Neyshabur. ICLR 2021 (**Oral**); arXiv:2012.03107 | https://api.openreview.net/notes/search (record tW4QEInpni: "ICLR 2021 Oral") ; https://arxiv.org/abs/2012.03107 | None | OK |
| 14 | zhang2017understanding | C. Zhang, S. Bengio, M. Hardt, **O. Recht,** and O. Vinyals. … ICLR, 2017 | Chiyuan Zhang; Samy Bengio; Moritz Hardt; **Benjamin Recht**; Oriol Vinyals. ICLR 2017; arXiv:1611.03530 | https://arxiv.org/abs/1611.03530 (author list) ; arXiv comments "Published in ICLR 2017" | Fourth author initial wrong: O. Recht → **B. Recht** (Benjamin Recht) | **CORRECTED** |

Summary: 14 entries checked → 8 OK (3 with pages/volume added), **6 CORRECTED**. The three most serious defects — invented author lists in refs. 8 (Muennighoff) and 12 (Varma) and the wrong-author + wrong-year entry for ref. 9 (Nanda) — are exactly the kind of error the plan flagged as highest-risk for AI-assisted bibliographies. All six corrections have been applied to `main.tex` in this pass.

## Part 2 — Verified reference list (Springer Nature numbered style, alphabetical by first author, as currently ordered in the manuscript)

1. Z. Allen-Zhu, Y. Li: Physics of language models: Part 3.3, knowledge capacity scaling laws. In: International Conference on Learning Representations (ICLR) (2025). Extended abstract; arXiv:2404.05405
2. Y. Bengio, J. Louradour, R. Collobert, J. Weston: Curriculum learning. In: Proceedings of the 26th International Conference on Machine Learning (ICML), pp. 41–48 (2009). DOI 10.1145/1553374.1553380
3. J. Hoffmann, S. Borgeaud, A. Mensch, et al.: Training compute-optimal large language models. In: Advances in Neural Information Processing Systems (NeurIPS), vol. 35 (2022). arXiv:2203.15556
4. J. Kaplan, S. McCandlish, T. Henighan, et al.: Scaling laws for neural language models. arXiv preprint arXiv:2001.08361 (2020)
5. K. Lee, D. Ippolito, A. Nystrom, C. Zhang, D. Eck, C. Callison-Burch, N. Carlini: Deduplicating training data makes language models better. In: Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (ACL), pp. 8424–8445 (2022). DOI 10.18653/v1/2022.acl-long.577
6. Z. Liu, E. J. Michaud, M. Tegmark: Omnigrok: Grokking beyond algorithmic data. In: International Conference on Learning Representations (ICLR) (2023). arXiv:2210.01117
7. I. Loshchilov, F. Hutter: Decoupled weight decay regularization. In: International Conference on Learning Representations (ICLR) (2019). arXiv:1711.05101
8. N. Muennighoff, A. Rush, B. Barak, et al.: Scaling data-constrained language models. In: Advances in Neural Information Processing Systems (NeurIPS), vol. 36 (2023). arXiv:2305.16264
9. N. Nanda, L. Chan, T. Lieberum, J. Smith, J. Steinhardt: Progress measures for grokking via mechanistic interpretability. In: International Conference on Learning Representations (ICLR) (2023). arXiv:2301.05217
10. A. Power, Y. Burda, H. Edwards, I. Babuschkin, V. Misra: Grokking: Generalization beyond overfitting on small algorithmic datasets. arXiv preprint arXiv:2201.02177 (2022)
11. A. Vaswani, N. Shazeer, N. Parmar, et al.: Attention is all you need. In: Advances in Neural Information Processing Systems (NeurIPS), vol. 30 (2017). arXiv:1706.03762
12. V. Varma, R. Shah, Z. Kenton, J. Kramár, R. Kumar: Explaining grokking through circuit efficiency. arXiv preprint arXiv:2309.02390 (2023)
13. X. Wu, E. Dyer, B. Neyshabur: When do curricula work? In: International Conference on Learning Representations (ICLR) (2021). arXiv:2012.03107
14. C. Zhang, S. Bengio, M. Hardt, B. Recht, O. Vinyals: Understanding deep learning requires rethinking generalization. In: International Conference on Learning Representations (ICLR) (2017). arXiv:1611.03530

The same entries are provided in `references.bib` (same directory). Unverified optional fields are marked `TODO-AUTHOR: add pages` there (NeurIPS proceedings page ranges for refs. 3, 8, 11 were not verified from an authoritative source; NPL's numbered style does not require them for NeurIPS).

## Part 3 — Citation-claim check (every sentence containing a citation, checked against the cited paper's abstract)

| Manuscript sentence (paraphrased) | Cited | Supported by abstract? |
|---|---|---|
| Transformer fits training set in a few hundred steps; test accuracy near chance for thousands of steps before abrupt transition | power2022grokking | Yes — abstract describes grokking: generalization from chance to perfect long after overfitting on algorithmic datasets |
| Deduplication / repetition / data-constrained pretraining as practical questions | lee2022deduplicating, muennighoff2023scaling, allen-zhu2024physics | Yes — each abstract is directly on one of these topics |
| Grokking appears only within a range of dataset fractions | power2022grokking | Yes — the paper's core finding (abstract + body) |
| Grokking varies strongly with the number of unique training items | liu2023omnigrok | Plausible — abstract addresses grokking's cause via loss landscapes; dataset-size dependence is in the paper body |
| Circuit-efficiency accounts predict a sufficient supply of unique examples is needed | varma2024explaining | Yes — abstract: task must admit a generalising vs memorising solution, generalising is more efficient |
| Grokking explained through loss-landscape geometry and weight norms | liu2023omnigrok | Yes — abstract: loss-landscape analysis, weight-norm mechanism (LU mechanism) |
| Mechanistic progress measures change smoothly before test accuracy jumps | nanda2024progress | Yes — abstract: continuous progress measures underlying discontinuous changes |
| Generalizing solutions parameter-efficient but slower to learn | varma2024explaining | Yes — abstract states this verbatim in substance |
| Repeating a corpus up to ~4 epochs changes loss little; more epochs degrade returns | muennighoff2023scaling | Yes — abstract: large set of experiments varying extent of data repetition |
| Compute-optimal scaling laws allocate budget between model size and tokens | kaplan2020scaling, hoffmann2022training | Yes — both abstracts are exactly this |
| Networks can fit random labels | zhang2017understanding | Yes — the paper's famous result |
| Knowledge capacity scales with parameters and repeats | allen-zhu2024physics | Yes — abstract: knowledge bits stored, controlled datasets (repeats covered in body/title scope) |
| Deduplication reduces verbatim recall | lee2022deduplicating | Yes — abstract topic |
| Curricula have mixed consequences; benefits in noisy or time-varying regimes | wu2021curricula, bengio2009curriculum | Yes — Wu's abstract studies when curricula help (noise regimes); Bengio 2009 introduced curriculum learning |
| Two-layer causal transformer; AdamW | vaswani2017attention, loshchilov2019decoupled | Yes — architectural/optimizer citations |
| Standard two-layer-transformer arithmetic setup; configuration under which delayed generalization was characterized | power2022grokking, nanda2024progress | Yes — both use this setup |
| Norm trajectory motivated by loss-landscape analyses | liu2023omnigrok | Yes |
| Circuit-efficiency reading: memorization consumes weight norm; weight decay tilts balance | varma2024explaining, liu2023omnigrok | Yes — abstract supports the competition + norm mechanism |

No citation-claim mismatch found. No text changes were needed for this part.

## Part 4 — Related-work gap check (papers actually opened)

(a) Critical dataset size / data fraction in grokking:

1. **Zhu, X., Fu, Y., Zhou, B., Lin, Z.: "Critical Data Size of Language Models from a Grokking Perspective." arXiv:2401.10463 (2024).** https://arxiv.org/abs/2401.10463 — Formalizes a "Data Efficiency Hypothesis": a critical data size marks the shift from memorization to generalization, with insufficiency/sufficiency/surplus regimes; shows generalization occurs only above the critical size. **Recommendation: CITE (and one clause of discussion).** This is the closest prior work on critical data size from a grokking perspective; the manuscript's "coverage determines whether and when generalization emerges" and its ~40% boundary at 20,000 steps sit directly on this line. Suggested sentence for Related work (author decision): "Critical data size has recently been formalized as a phase boundary between memorization and generalization in language models [Zhu et al. 2024]; the present design measures the analogous boundary at seed level while additionally separating repetition from coverage at matched dose."
2. **Clauw, K., Stramaglia, S., Marinazzo, D.: "Information-Theoretic Progress Measures reveal Grokking is an Emergent Phase Transition." arXiv:2408.08944 (2024).** https://arxiv.org/abs/2408.08944 — Higher-order mutual information identifies phases before grokking. **Recommendation: IGNORE** (the manuscript makes no information-theoretic claims; Nanda et al. already covers progress measures).

(b) Repeated data in language-model training:

3. **Muennighoff, N., Rush, A., Barak, B., et al.: "Scaling Data-Constrained Language Models." NeurIPS 2023.** (already cited) — the central prior work; no change.
4. **Hägele, A., Bakouch, E., Kosson, A., Ben Allal, L., Von Werra, L., Jaggi, M.: "Scaling Laws and Compute-Optimal Training Beyond Fixed Training Durations." NeurIPS 2024 (spotlight). arXiv:2405.18392.** https://arxiv.org/abs/2405.18392 — Constant-LR-with-cooldowns enables retraining/uptraining across durations; about training-length scaling rather than repetition per se. **Recommendation: OPTIONAL — ignore unless the author wants a second scaling-law citation for multi-duration/multi-epoch training.** (Note: a web search mislabeled this paper as "Hernandez et al." on one aggregator; the arXiv author list above is authoritative.)

No paper doing a coverage × repetition factorial decomposition at matched per-example dose with seed-level statistics was found (searches: 13 in the original literature pass, plus 6 in this pass). The novelty claim in Sect. 1–2 ("What prior work does not isolate is repetition as a separate factor") remains defensible as of this check.

## Part 5 — Open problems for the author

1. [TODO-AUTHOR: decide whether to add Zhu et al. 2024 (arXiv:2401.10463) to Related work — recommended; a drafted sentence is provided in Part 4(a).]
2. [TODO-AUTHOR: confirm the ICLR 2025 "extended abstract" designation for Allen-Zhu & Li is acceptable to cite as ICLR 2025 rather than as arXiv:2404.05405; both forms are defensible, the applied form names the venue plus the arXiv full version.]
3. Page ranges for the three NeurIPS entries (Hoffmann 2022, Muennighoff 2023, Vaswani 2017) were not verified; NPL numbered style does not require them. TODO-AUTHOR: add pages if the final journal style demands them.
4. The manuscript cites "nanda2024progress" and "varma2024explaining" as internal LaTeX keys although both entries are now dated 2023; keys do not render, but renaming them during Springer template conversion is a free opportunity (cosmetic only).
5. Varma et al. is arXiv-only; if a future version is published (the OpenReview record shows an ICLR 2024 submission), update the entry before submission. Same for any of the other preprints.
