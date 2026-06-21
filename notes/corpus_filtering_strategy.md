# Uzbek Web Corpus Filtering Strategy

## Primary corpus source

The project now uses the local heterogeneous Uzbek web corpus at `dataset/raw/uz.txt` as the primary raw text source. The raw file is intentionally excluded from Git because it is large and may contain source-specific licensing constraints. Reproducible project artifacts should include only code, notes, configuration, and derived statistics that are safe to publish.

## Noise types expected in `uz.txt`

Because `uz.txt` aggregates broad web text, the processor assumes that useful Uzbek prose is mixed with several recurring noise classes:

- URLs, email addresses, and crawler residue.
- HTML tags, escaped HTML entities, and markup fragments.
- Navigation/menu strings such as home-page links, login labels, search labels, next/previous links, and advertisement markers.
- Metadata rows containing dates, times, source names, authors, categories, tags, IDs, or titles.
- Directory-style and breadcrumb entries with repeated separators such as `/`, `|`, `›`, `•`, and `·`.
- Very short snippets that are unlikely to be useful sentence-level training examples.
- Boilerplate, repeated punctuation, JavaScript/CSS fragments, cookie notices, and other low-language-content rows.
- Duplicate sentence candidates caused by mirrored pages, repeated templates, or syndication.

## Filtering rules

`experiments/data_preparation/process_uz_corpus.py` applies deterministic streaming filters:

1. Read the raw file line by line using UTF-8 with replacement for malformed byte sequences.
2. Decode HTML entities, remove URLs and email addresses, remove HTML tags, normalize apostrophe variants to ASCII `'`, and collapse whitespace.
3. Split normalized lines into conservative sentence candidates at terminal punctuation and line boundaries.
4. Remove empty candidates and obvious metadata rows.
5. Remove navigation/menu text and directory-style entries.
6. Keep only candidates within configurable length bounds.
7. Keep only candidates with a minimum number of word tokens.
8. Remove candidates with excessive non-letter content or repeated punctuation artifacts.
9. Deduplicate accepted sentences using a case-folded, whitespace-normalized hash key.
10. Write retained sentences to `dataset/processed/clean_sentences.csv` with `id,sentence` columns.

## Deduplication strategy

Deduplication is exact after light normalization rather than semantic. The key is computed from the case-folded sentence with normalized whitespace. This removes repeated copies of the same sentence while preserving the first observed surface form. It intentionally does not merge near-duplicates, paraphrases, or spelling variants because those may be useful for later error-analysis work.

## Quality thresholds

The default thresholds are conservative starting points for a noisy web corpus:

- Minimum sentence length: 25 characters.
- Maximum sentence length: 500 characters.
- Minimum sentence length: 4 word tokens.
- Maximum non-letter ratio: 0.35.
- Repeated punctuation sequences of four or more characters are rejected.

These values should be validated by sampling accepted and rejected lines before large-scale model training.

## Limitations

- The processor uses deterministic regex heuristics and does not perform full Uzbek language identification.
- Some valid short Uzbek sentences, headings, and list items will be removed.
- Some boilerplate may remain if it resembles prose.
- Sentence splitting is intentionally simple and may mishandle abbreviations, initials, decimal numbers, or web-specific punctuation.
- Exact deduplication does not remove near-duplicate syndicated text.
- The cleaned CSV should still be treated as an intermediate corpus that requires statistical reporting and qualitative audit before generating spelling-error datasets.
