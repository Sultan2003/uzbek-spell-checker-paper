# Dataset Statistics Plan

After producing `dataset/processed/clean_sentences.csv`, collect descriptive statistics that make corpus construction auditable and reproducible.

## Required metrics

- **Raw lines:** number of physical lines streamed from `dataset/raw/uz.txt` during preprocessing.
- **Retained lines:** number of accepted sentence rows written to `dataset/processed/clean_sentences.csv`.
- **Removed lines/candidates:** counts for empty/artifact rows, low-quality candidates, and duplicate candidates.
- **Average sentence length:** mean sentence length in both characters and word tokens.
- **Vocabulary size estimate:** number of unique case-folded word tokens in the cleaned CSV.
- **Number of unique sentences:** case-folded unique sentence count in the cleaned CSV.

## Collection workflow

1. Run `experiments/data_preparation/process_uz_corpus.py` and save the terminal log so raw-line, candidate, rejection, duplicate, and retained counts are preserved.
2. Run `experiments/data_preparation/analyze_corpus.py` on `dataset/processed/clean_sentences.csv` to compute sentence length, token, vocabulary, and uniqueness statistics.
3. Record the exact command-line parameters used for both scripts.
4. Manually inspect a stratified sample of retained and rejected examples before using the corpus for spelling-error generation.

## Reporting recommendations

The paper should report both absolute counts and percentages where possible: retention rate relative to raw lines, duplicate rate among sentence candidates, and vocabulary size after normalization. If filtering thresholds change, regenerate the statistics and document the rationale.
