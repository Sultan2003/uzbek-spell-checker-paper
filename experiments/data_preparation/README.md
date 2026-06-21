# Corpus Collection and Preprocessing

This directory contains the data preparation stage for the Uzbek spell-checking framework. It collects raw Uzbek Wikipedia text and converts raw text into a deduplicated sentence-level CSV corpus.

## 1. Collect Uzbek Wikipedia text

Run a small reproducible smoke test:

```bash
python experiments/data_preparation/collect_wikipedia.py --max-pages 25
```

Run a full collection:

```bash
python experiments/data_preparation/collect_wikipedia.py
```

By default, the collector writes UTF-8 text to:

```text
dataset/raw/uzbek_wikipedia_raw.txt
```

Useful options:

- `--max-pages`: cap the number of pages for repeatable development runs.
- `--batch-size`: number of pages requested per MediaWiki API call.
- `--sleep-seconds`: polite delay between API requests.
- `--output`: override the raw corpus destination.
- `--log-level`: change logging verbosity.

## 2. Clean the corpus

After collection, run:

```bash
python experiments/data_preparation/clean_corpus.py
```

By default, the cleaner reads:

```text
dataset/raw/uzbek_wikipedia_raw.txt
```

and writes:

```text
dataset/processed/clean_sentences.csv
```

The output CSV has two columns:

```text
id,sentence
```

The cleaner removes empty lines, URLs, and HTML artifacts; normalizes whitespace and apostrophe variants; splits text into coarse sentence candidates; and removes duplicate sentences while preserving first-seen order.
