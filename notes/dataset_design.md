# Dataset Design

## Research Dataset Objectives

The dataset is intended to support a publishable evaluation of Uzbek spell-checking methods that combine rule-based and transformer-based approaches. Its primary objective is to provide paired examples of correct Uzbek text and plausible misspelled variants so that systems can be trained, validated, and tested on controlled spelling-error phenomena.

The dataset should support the following research goals:

- Measure correction accuracy for common character-level spelling errors.
- Evaluate Uzbek-specific orthographic challenges, especially apostrophes, Latin characters with diacritics, and Latin/Cyrillic script interaction.
- Compare rule-based correction strategies with transformer-based contextual correction models under identical evaluation conditions.
- Analyze performance by error category rather than reporting only aggregate accuracy.
- Provide a reproducible benchmark that can be extended with naturally occurring errors in future work.

## Dataset Requirements

The dataset should contain sentence-level or short phrase-level examples with one or more controlled spelling errors. Each record should preserve the correct form, the generated incorrect form, and the error category responsible for the transformation.

Minimum requirements are:

- Text must be Uzbek or predominantly Uzbek.
- Each sample must include a correct reference text and an incorrect variant.
- Each incorrect variant must be assigned one primary `error_type`.
- Error labels must be consistent with the taxonomy defined in `notes/error_generation_strategy.md`.
- The dataset must include both general spelling errors and Uzbek-specific orthographic errors.
- Duplicate pairs should be removed unless they intentionally represent different contexts.
- The final benchmark split must prevent near-duplicate leakage across train, validation, and test sets.

The target schema is defined in `dataset/generated_errors/spell_dataset.csv`:

| Column | Description |
| --- | --- |
| `id` | Stable unique identifier for the example. |
| `correct_text` | Gold-standard Uzbek text before error injection. |
| `incorrect_text` | Text after applying a spelling-error transformation. |
| `error_type` | Primary error category assigned to the incorrect text. |

## Data Sources

Suitable source text should be collected from legally usable and clearly documented sources. Priority should be given to sources that represent contemporary Uzbek usage and multiple domains.

Recommended source categories:

- News articles and public information pages for formal written Uzbek.
- Educational materials, textbooks, and open learning resources for standardized spelling.
- Government or public-service documents for administrative and formal language.
- Public-domain or openly licensed literary texts for longer sentence structure.
- The local heterogeneous Uzbek web corpus at `dataset/raw/uz.txt`, supplemented only when needed by openly licensed sources for coverage analysis.
- User-facing public text such as FAQs, help pages, or community announcements when licensing permits reuse.

For publication, every source category should be recorded with license information, access date, collection method, and any exclusion criteria.

## Data Collection Process

The collection process should be staged and auditable:

1. Define the target domains and the desired number of clean sentences per domain.
2. Collect raw text only from sources with compatible licenses or explicit permission.
3. Store source metadata separately from generated examples, including URL or document identifier, domain, license, collection date, and preprocessing notes.
4. Segment documents into sentences or short text units.
5. Filter out text units that are too short, too long, mostly non-Uzbek, or dominated by tables, lists, markup, numbers, or named entities.
6. Normalize text according to a documented Uzbek Latin orthographic convention.
7. Apply controlled error generation to produce incorrect variants.
8. Assign each generated pair a stable identifier and error-type label.
9. Reserve a manually inspected subset for quality assurance and error-analysis reporting.

A recommended unit of analysis is a sentence of approximately 5--30 tokens. Single-word examples may be included for targeted orthographic phenomena, but sentence-level examples are preferable for transformer-based correction because they preserve context.

## Data Cleaning Process

Cleaning should occur before error generation so that injected errors are distinguishable from noise already present in the source text.

Recommended cleaning steps:

- Remove boilerplate such as navigation menus, advertisements, copyright blocks, and repeated headers or footers.
- Normalize whitespace, punctuation spacing, quotation marks, and Unicode encoding.
- Normalize Uzbek Latin apostrophe-like characters to a selected canonical representation before generating apostrophe-related errors.
- Remove or mark sentences containing extensive foreign-language content.
- Remove malformed text caused by encoding conversion, OCR artifacts, or broken markup.
- Deduplicate exact sentences and identify near duplicates using normalized text.
- Preserve named entities only when they do not dominate the sentence or introduce ambiguous spelling judgments.
- Exclude sentences whose correct spelling cannot be confidently verified.

All automatic cleaning rules should be documented, and a sample should be manually reviewed to estimate residual noise.

## Data Quality Checks

Quality checks should be performed before release and before every experimental run.

Recommended checks:

- Schema validation: confirm that every row contains `id`, `correct_text`, `incorrect_text`, and `error_type`.
- Identifier validation: confirm that `id` values are unique and stable.
- Pair validation: confirm that `correct_text` and `incorrect_text` are not identical.
- Label validation: confirm that `error_type` values belong to the approved taxonomy.
- Transformation validation: confirm that the observed edit pattern is compatible with the assigned error type.
- Duplicate validation: remove exact duplicate pairs and inspect near duplicates.
- Split leakage validation: ensure that the same source sentence or near-identical sentence does not appear in multiple splits.
- Distribution validation: compare observed error-type counts with the planned frequency distribution.
- Manual audit: inspect a stratified sample from each error category and each data source.

For publication-quality experiments, inter-annotator agreement should be reported for any manually labeled or manually corrected subset.

## Train/Validation/Test Split Methodology

The recommended split is source-aware and sentence-aware rather than purely random. Random splitting can overestimate performance if similar sentences from the same article or document appear in multiple splits.

Recommended split strategy:

- Use a 70/15/15 split for train, validation, and test data for large datasets.
- Use an 80/10/10 split for smaller pilot experiments if the test set would otherwise be too small.
- Split by source document when possible to reduce topical and lexical leakage.
- Stratify by `error_type` so that each split contains all major error categories.
- Preserve a held-out test set that is not used for prompt tuning, rule refinement, model selection, or threshold selection.
- If naturally occurring errors are added later, keep them in a separate evaluation subset or report them separately from synthetic errors.

The test set should include both frequent and Uzbek-specific error categories. For robust analysis, every major error category should have enough test examples to support per-category metrics.

## Recommended Dataset Sizes

The following sizes are realistic targets for a staged research program:

| Dataset stage | Recommended size | Purpose |
| --- | ---: | --- |
| Pilot dataset | 1,000--3,000 pairs | Validate the schema, taxonomy, generation rules, and preliminary model pipeline. |
| Research dataset | 25,000--75,000 pairs | Support systematic comparison of rule-based and transformer-based approaches with per-category analysis. |
| Publication-quality dataset | 150,000--500,000 pairs | Support robust training, ablation studies, domain analysis, and stronger statistical claims. |

The number of underlying clean sentences may be smaller than the number of generated pairs if multiple error variants are produced from each sentence. However, experiments should avoid placing variants of the same clean sentence in different splits.

## Reproducibility Considerations

Reproducibility should be addressed at the dataset, generation, and evaluation levels.

Recommended practices:

- Version all source lists, preprocessing rules, and error-generation rules.
- Store deterministic random seeds used for sampling and error injection.
- Keep a changelog of dataset revisions and schema changes.
- Record source metadata and licensing information.
- Preserve split files or split assignments rather than regenerating splits for every experiment.
- Report dataset statistics by domain, split, length, script, and error category.
- Use stable identifiers that do not change when rows are reordered.
- Document normalization decisions for apostrophes, Uzbek Latin letters, and Cyrillic transliteration.
- Separate raw, cleaned, and generated data artifacts in the repository or data release.

## Threats to Validity

### Synthetic Errors

Synthetic errors may not fully represent errors made by real Uzbek writers. Generated misspellings can be too regular, too isolated, or too easy for models to learn. This threat should be mitigated by using diverse error rules, manually auditing examples, and, when possible, evaluating on a smaller set of naturally occurring errors.

### Sampling Bias

If the clean corpus is sampled from a narrow set of sources, the benchmark may overrepresent particular vocabulary, writing styles, or topics. Sampling should be stratified across domains, and dataset statistics should be reported so that readers can interpret the scope of the benchmark.

### Domain Bias

A model trained mostly on formal news or administrative text may perform poorly on informal, educational, literary, or social-media-like Uzbek. Domain-level performance should be reported when enough data is available, and future versions should include broader text types.

### Evaluation Limitations

Exact-match correction metrics may penalize acceptable alternative spellings, punctuation variants, or normalization choices. Aggregate metrics may also hide poor performance on rare but linguistically important Uzbek-specific errors. Evaluation should therefore include per-category results, qualitative error analysis, and clear documentation of accepted reference forms.
