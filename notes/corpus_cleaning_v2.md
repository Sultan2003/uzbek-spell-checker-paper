# Corpus cleaning v2

This note documents the second-pass corpus-quality filters applied before any spell-error generation. The goal is to keep sentence-like Uzbek text and remove crawl artifacts that would teach downstream models web noise rather than spelling behavior.

## New filtering rules

1. **Mojibake detection and repair**
   - Detects visible encoding artifacts such as `вЂ`, `В«`, `В»`, `Ð`, `Ñ`, `Ã`, replacement characters, and mixed Cyrillic mojibake fragments such as `Рµ`.
   - Attempts conservative repairs by round-tripping likely single-byte decodings back to UTF-8.
   - Keeps repaired text only when the mojibake marker score decreases; otherwise rejects the candidate as `mojibake_removed`.

2. **Title aggregation removal**
   - Removes rows with excessive comma-separated short title fragments.
   - Targets crawl rows where multiple headlines were merged into one pseudo-sentence.
   - Uses comma count, number of segments, segment length, and punctuation structure to avoid removing normal prose lists.

3. **Song-title / lyric-page removal**
   - Removes page-title rows containing `qo'shiq matni`, `lyrics`, or `текст песни`.
   - These rows usually identify a lyrics page rather than a natural sentence.

4. **Directory and catalog removal**
   - Removes contact/catalog rows containing terms such as `manzil:`, `telefon`, `kontakt`, `katalog`, and `yellow pages`.
   - Existing breadcrumb/path-like filters remain in place for navigation fragments.

5. **Legal and web boilerplate removal**
   - Removes rows containing `foydalanish shartlari`, `copyright`, `privacy policy`, `all rights reserved`, cookie-policy text, and related rights-reserved boilerplate.

## Reporting

`filtering_report.json` now includes a `new_filter_counts` section with:

- `mojibake_removed`
- `directory_removed`
- `song_page_removed`
- `title_aggregation_removed`
- `boilerplate_removed`
- `mojibake_repaired`

The existing detailed rejection counters are still preserved under `counts` as `rejected_<reason>` keys.

## Manual inspection samples

Run the sampler after generating `clean_sentences.csv`:

```bash
python experiments/data_preparation/sample_clean_corpus.py
```

It writes reproducible random samples to:

- `dataset/processed/samples/random_100.csv`
- `dataset/processed/samples/random_500.csv`
