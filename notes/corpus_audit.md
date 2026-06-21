# Corpus Audit and Filtering Improvement Stage

The first inspection pass over `dataset/processed/clean_sentences.csv` showed that
sentence-level cleaning still admits web-corpus boilerplate and source metadata.
This note defines the audit stage added before any spelling-error generation.

## Quality issues to audit

The audit script flags these residual issue classes:

- **Numeric metadata rows**: source rows that begin with an integer identifier or
  include floating-point ranking scores, for example `154 Neimar Jahon futboli
  yulduzlari 0.0130`.
- **Ranking/list entries**: numbered catalogue, list, or search-result snippets
  that are not natural Uzbek sentences.
- **URL contamination**: raw URLs, host names, email-like web artifacts, or page
  references that survived normalization.
- **Encoding corruption**: replacement characters and mojibake-like fragments
  such as `Ã`, `Ð`, `Ñ`, or smart-quote corruption sequences.
- **Extremely short sentences**: fragments below the configured character
  threshold that tend to be labels, headings, or incomplete snippets.
- **Extremely long sentences**: candidates above the configured threshold that
  are likely concatenated pages, lists, or malformed rows.
- **Non-Uzbek character patterns**: Cyrillic or unexpected symbol-heavy rows in
  a Latin-script Uzbek corpus candidate set.
- **Directory/navigation content**: breadcrumbs, path-like strings, menu labels,
  and repeated separator-delimited page sections.

## Audit workflow

Run the audit after producing or updating the cleaned corpus:

```bash
python experiments/data_preparation/audit_corpus.py
```

By default it reads `dataset/processed/clean_sentences.csv`, uses a fixed random
seed, and exports two review files:

- `dataset/processed/audit_samples/audit_sample_500.csv`
- `dataset/processed/audit_samples/audit_sample_1000.csv`

Each exported row contains the original sentence plus semicolon-separated issue
labels.  The script also writes `dataset/processed/audit_samples/audit_summary.json`
with issue counts for each sample size.

## Filtering improvements

`experiments/data_preparation/process_uz_corpus.py` now rejects additional
non-sentence patterns before deduplication:

- rows beginning with an integer (`^[0-9]+\s`),
- rows containing floating-point score fields,
- ranking-style numbered entries,
- path-like and directory-style rows,
- navigation/menu labels,
- likely encoding-corruption artifacts,
- rows that exceed configurable digit, separator, non-letter, length, or word
  count thresholds.

The processor writes `dataset/processed/filtering_report.json` with the input and
output paths, threshold values, and rejection counters.  The report is generated
as a local processed artifact and should be reviewed together with the audit
samples before creating any generated spelling-error dataset.

## Important constraint

Do **not** generate spelling errors until the cleaned corpus passes this audit
stage and the residual issue counts are acceptable for the experiment design.
