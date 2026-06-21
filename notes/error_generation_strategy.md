# Error Generation Strategy

This document defines a controlled synthetic-error strategy for an Uzbek spell-checking dataset. The goal is not to model every possible spelling mistake, but to create a transparent and reproducible benchmark that covers both general edit-distance errors and Uzbek-specific orthographic phenomena.

Suggested frequencies are starting points for dataset construction. They should be adjusted after manual inspection and, if available, comparison with naturally occurring Uzbek spelling errors.

## Error Category Distribution

| Error category | Suggested frequency |
| --- | ---: |
| Character deletion | 15% |
| Character insertion | 10% |
| Character substitution | 15% |
| Character transposition | 10% |
| Apostrophe omission | 12% |
| Apostrophe confusion | 8% |
| Uzbek Latin character confusion | 12% |
| Keyboard proximity errors | 10% |
| Mixed-script errors (Latin/Cyrillic) | 8% |
| **Total** | **100%** |

## Character Deletion

### Description

A valid character is omitted from a word. This models accidental skipped keystrokes and common fast-typing errors.

### Examples

- `kitob` -> `ktob`
- `maktab` -> `matab`
- `o'qituvchi` -> `o'qtuvchi`

### Generation Rules

- Select a token with at least four characters after excluding punctuation-only tokens.
- Delete one internal character when possible; avoid deleting the only vowel in very short words.
- Do not delete whitespace for this category.
- Preserve the original casing pattern unless the deleted character changes it naturally.

### Suggested Frequency Percentage

15% of generated error pairs.

## Character Insertion

### Description

An extra character is inserted into a word. This models accidental repeated keystrokes or unintended nearby keystrokes.

### Examples

- `kitob` -> `kiitob`
- `maktab` -> `makttab`
- `talaba` -> `talabba`

### Generation Rules

- Select a token with at least three alphabetic characters.
- Insert either a duplicate of a neighboring character or a plausible Uzbek Latin alphabet character.
- Prefer internal insertion positions over word boundaries.
- Avoid generating another valid common word when this would make the correction ambiguous.

### Suggested Frequency Percentage

10% of generated error pairs.

## Character Substitution

### Description

One character is replaced by another. This models mistyping, uncertainty about spelling, or visually similar character selection.

### Examples

- `kitob` -> `kitab`
- `maktab` -> `maktib`
- `shahar` -> `shaxar`

### Generation Rules

- Select one alphabetic character inside a token.
- Replace it with another Uzbek Latin character.
- Prefer substitutions involving vowels or consonants that produce plausible-looking nonwords.
- Keep substitutions separate from the more specific Uzbek Latin character confusion and keyboard proximity categories when assigning labels.

### Suggested Frequency Percentage

15% of generated error pairs.

## Character Transposition

### Description

Two adjacent characters are swapped. This models common typing-order errors.

### Examples

- `kitob` -> `ktiob`
- `maktab` -> `maktba`
- `talaba` -> `tlaaba`

### Generation Rules

- Select a token with at least four characters.
- Swap two adjacent internal characters.
- Avoid swapping identical characters because the resulting token would be unchanged.
- Avoid crossing apostrophe boundaries in this category; apostrophe errors are handled separately.

### Suggested Frequency Percentage

10% of generated error pairs.

## Apostrophe Omission

### Description

The apostrophe in an Uzbek Latin word is omitted. This is a central Uzbek orthographic error because apostrophes distinguish letters and word forms such as `o'`, `g'`, and glottal-marked forms.

### Examples

- `o'qituvchi` -> `oqituvchi`
- `g'isht` -> `gisht`
- `ma'no` -> `mano`

### Generation Rules

- Select tokens containing a canonical apostrophe character.
- Remove the apostrophe without changing neighboring letters.
- Apply only one omission per generated example unless multi-error examples are explicitly introduced in a later dataset version.
- Record the error as apostrophe omission even if the resulting word resembles another valid form.

### Suggested Frequency Percentage

12% of generated error pairs.

## Apostrophe Confusion

### Description

The correct apostrophe symbol is replaced with another apostrophe-like mark or spacing form. This models inconsistent input conventions across keyboards, fonts, and platforms.

### Examples

- `o'qituvchi` -> `o‘qituvchi`
- `g'oya` -> `gʼoya`
- `ma'lumot` -> `ma’lumot`

### Generation Rules

- Select tokens containing the canonical apostrophe representation used in the cleaned corpus.
- Replace it with a typographic apostrophe-like character such as `‘`, `’`, `ʼ`, or backtick-like variants.
- Keep surrounding letters unchanged.
- Normalize all source text before generation so this category represents an injected error rather than leftover source noise.

### Suggested Frequency Percentage

8% of generated error pairs.

## Uzbek Latin Character Confusion

### Description

A specific Uzbek Latin character or digraph-like orthographic unit is confused with a simpler or related form. This captures errors involving Uzbek-specific letters and combinations such as `o'`, `g'`, `sh`, `ch`, and `ng`.

### Examples

- `o'zbek` -> `ozbek`
- `g'alla` -> `galla`
- `shahar` -> `sahar`
- `chiroyli` -> `ciroyli`

### Generation Rules

- Target Uzbek-specific orthographic units, including `o'`, `g'`, `sh`, `ch`, and contextually important multicharacter sequences.
- Replace the target with a simplified, incomplete, or commonly confused form.
- Keep this category distinct from apostrophe omission when the intended phenomenon is broader orthographic-unit confusion rather than only removing punctuation.
- Avoid examples where the transformation creates a proper noun or highly ambiguous valid word unless ambiguity is part of a planned challenge subset.

### Suggested Frequency Percentage

12% of generated error pairs.

## Keyboard Proximity Errors

### Description

A character is replaced by a nearby key on a common keyboard layout. This models motor errors during typing.

### Examples

- `kitob` -> `kiyob` (`t` replaced by nearby `y`)
- `maktab` -> `majtab` (`k` replaced by nearby `j`)
- `salom` -> `xalom` (`s` replaced by nearby `x`)

### Generation Rules

- Define an explicit keyboard-neighbor map for the selected keyboard layout before generation.
- Select one alphabetic character and replace it with one of its neighboring keys.
- Use the same keyboard layout consistently within an experiment, or label layout-specific subsets separately.
- Exclude substitutions already assigned to Uzbek Latin character confusion when the Uzbek-specific orthographic issue is the primary phenomenon.

### Suggested Frequency Percentage

10% of generated error pairs.

## Mixed-Script Errors (Latin/Cyrillic)

### Description

A word or character sequence in Uzbek Latin text contains Cyrillic characters, or a Cyrillic-looking equivalent is inserted into otherwise Latin text. This models script interference and copy-paste inconsistencies in Uzbek digital writing.

### Examples

- `salom` -> `сalom` (Cyrillic `с` replacing Latin `s`)
- `kitob` -> `kitоb` (Cyrillic `о` replacing Latin `o`)
- `o'zbek` -> `o'zbеk` (Cyrillic `е` replacing Latin `e`)

### Generation Rules

- Start from Uzbek Latin source text unless creating a separate Cyrillic-to-Latin benchmark.
- Replace one visually similar Latin character with a Cyrillic homoglyph where available.
- Do not transliterate the entire sentence for this category; the error should be a mixed-script anomaly.
- Validate that the incorrect text contains at least one character from the Cyrillic Unicode block and at least one Latin character.

### Suggested Frequency Percentage

8% of generated error pairs.

## Multi-Error Policy

The initial benchmark should contain one primary error type per row to support controlled analysis. Multi-error examples can be added in a later extension, but they should be clearly labeled and evaluated separately because they change task difficulty and complicate error attribution.

## Human Review Recommendations

A stratified sample from every category should be manually reviewed by Uzbek speakers or trained annotators. Reviewers should check whether the correct text is valid, whether the incorrect text is plausible, and whether the assigned error label matches the transformation.
