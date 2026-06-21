# Corpus Collection Plan

## Primary local corpus

The project now uses `dataset/raw/uz.txt` as the primary raw corpus. This file is a large local Uzbek web-text corpus of roughly 744 MB containing heterogeneous material such as news, government pages, educational text, sports articles, forums, directories, and other web content. The file must remain outside Git; GitHub should contain only source code, documentation, and reproducible instructions.

## Processing-first strategy

Because the corpus already exists locally, the immediate research priority is preprocessing and audit rather than additional crawling. The canonical cleaning command is:

```bash
python experiments/data_preparation/process_uz_corpus.py
```

The processor reads `dataset/raw/uz.txt` and writes sentence-level output to:

```text
dataset/processed/clean_sentences.csv
```

## Optional supplemental sources

Uzbek Wikipedia and other open sources may still be useful later for coverage analysis or controlled comparisons, but they are no longer the primary corpus source. Any supplemental collection should be stored separately with source metadata, access date, license notes, and preprocessing assumptions.

## Corpus inclusion criteria

- Text is primarily Uzbek, including both Latin and Cyrillic Uzbek where licensing allows processing.
- Content is natural prose or sentence-like text useful for spell-checking evaluation and model training.
- Documents can be stored and processed as UTF-8 text.
- Source provenance, collection date, and preprocessing configuration can be documented when available.

## Corpus exclusion criteria

- Raw corpora, compressed corpora, trained models, checkpoints, and large generated datasets must not be committed.
- Text with unclear, restrictive, or incompatible redistribution terms should not be released publicly.
- Private, personal, sensitive, or access-controlled content should be excluded.
- Machine-generated spam, navigation menus, boilerplate-heavy pages, pages dominated by tables/code, and duplicated mirrors should be filtered where possible.

## Licensing considerations

The raw `uz.txt` corpus should be treated as a local research input unless redistribution rights are verified. Released artifacts should avoid exposing raw source text beyond small, policy-compliant examples and should document that users must provide their own local `dataset/raw/uz.txt` file to reproduce preprocessing.

## Expected corpus size

The raw file is approximately 744 MB. The final cleaned sentence count depends on boilerplate prevalence, duplicate rate, and filtering thresholds. Corpus statistics should be generated after each preprocessing run with `experiments/data_preparation/analyze_corpus.py` and reported alongside the command configuration.
