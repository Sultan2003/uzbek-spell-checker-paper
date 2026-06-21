# Corpus Collection Plan

## Uzbek Wikipedia collection strategy

Uzbek Wikipedia is the first corpus source because it is public, broad-domain, and available through reproducible interfaces. The collection script queries the MediaWiki API for main-namespace article extracts in deterministic title order and stores plain-text UTF-8 output in `dataset/raw/uzbek_wikipedia_raw.txt`. Development runs should use a fixed `--max-pages` value, while full runs can omit the cap and record the command, date, and script configuration used.

## Public text collection strategy

Additional public Uzbek text can be added after the Wikipedia baseline is stable. Suitable sources include openly licensed government publications, educational materials, public-domain books, open news datasets with redistribution permission, and institutional pages that explicitly permit research reuse. Each source should be collected into a separate raw file with source metadata, access date, license notes, and preprocessing assumptions.

## Corpus inclusion criteria

- Text is primarily Uzbek, including both Latin and Cyrillic Uzbek where licensing allows collection.
- The source has a clear license or terms that permit research use and derived corpus processing.
- Content is natural prose or sentence-like text useful for spell-checking evaluation and model training.
- Documents can be stored and processed as UTF-8 text.
- Source provenance, collection date, and preprocessing configuration can be documented.

## Corpus exclusion criteria

- Text with unclear, restrictive, or incompatible licensing terms.
- Private, personal, sensitive, or access-controlled content.
- Machine-generated spam, navigation menus, boilerplate-heavy pages, or pages dominated by tables and code.
- Duplicated mirrors of already collected sources unless needed for coverage analysis.
- Content that cannot be reliably decoded or normalized into sentence-level Uzbek text.

## Licensing considerations

Wikipedia-derived text must preserve attribution and comply with the applicable Creative Commons license used by Wikipedia content. Any released dataset or paper artifact should document that the Wikipedia portion is derived from Uzbek Wikipedia, include the collection date, and provide enough information to reproduce the extraction. For non-Wikipedia sources, license compatibility must be checked before inclusion, and redistribution should be avoided unless the source explicitly permits it.

## Expected corpus size

The initial Wikipedia-only corpus is expected to produce a medium-sized Uzbek text baseline suitable for preprocessing experiments and early spell-checking evaluation. Depending on the number of live articles and filtering decisions at collection time, the cleaned output is expected to contain tens to hundreds of thousands of unique sentence candidates. The target for the broader public-text corpus is a multi-source collection large enough to cover news, encyclopedic, educational, and formal prose domains while retaining strict licensing traceability.
