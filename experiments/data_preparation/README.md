# Corpus Processing and Analysis

This directory contains the data preparation stage for the Uzbek spell-checking framework. The primary input is the local heterogeneous Uzbek web corpus:

```text
dataset/raw/uz.txt
```

The raw corpus is large and must not be committed to Git. Keep only code, documentation, reproducible commands, and safe derived statistics in the repository.

## 1. Prepare the local raw corpus

Place the local corpus file at:

```text
dataset/raw/uz.txt
```

Do not rename it unless you also pass `--input` to the processing script. Do not commit `uz.txt`, `uz.txt.xz`, raw corpora, trained models, checkpoints, or large generated datasets.

## 2. Process the corpus

Run the streaming processor:

```bash
python experiments/data_preparation/process_uz_corpus.py
```

By default, the processor reads `dataset/raw/uz.txt` and writes:

```text
dataset/processed/clean_sentences.csv
```

The output CSV has two columns:

```text
id,sentence
```

Useful options:

- `--input`: override the raw corpus path.
- `--output`: override the cleaned CSV destination.
- `--min-chars`: minimum sentence length in characters.
- `--max-chars`: maximum sentence length in characters.
- `--min-words`: minimum number of word tokens.
- `--max-non-letter-ratio`: maximum allowed share of non-letter characters.
- `--log-every`: raw-line progress interval.
- `--log-level`: change logging verbosity.

The processor streams the file line by line, normalizes apostrophe variants, removes URLs and HTML artifacts, removes empty lines, filters obvious metadata/navigation/directory noise, normalizes whitespace, filters low-quality candidates, and removes duplicate sentences while preserving first-seen order.

## 3. Analyze the cleaned corpus

After processing, run:

```bash
python experiments/data_preparation/analyze_corpus.py
```

By default, the analyzer reads `dataset/processed/clean_sentences.csv` and writes:

```text
dataset/processed/corpus_statistics.json
```

The statistics include retained sentence count, unique sentence count, average sentence length, token count, vocabulary size estimate, and top tokens.

## Optional Wikipedia collector

`collect_wikipedia.py` remains in the repository as an optional supplemental-data utility for future coverage studies. It is not the primary corpus path for the current project direction.
