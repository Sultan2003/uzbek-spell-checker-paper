#!/usr/bin/env python3
"""Export random samples from the cleaned Uzbek sentence corpus.

The samples are intended for manual corpus-quality inspection after running
``process_uz_corpus.py`` and before generating synthetic spelling errors.
"""

from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = REPO_ROOT / "dataset" / "processed" / "clean_sentences.csv"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "dataset" / "processed" / "samples"
SAMPLE_SIZES = (100, 500)


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""

    parser = argparse.ArgumentParser(description="Create random manual-review samples from clean_sentences.csv.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Clean sentence CSV to sample.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for sample CSV files.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducible samples.")
    return parser.parse_args()


def reservoir_samples(input_path: Path, seed: int) -> tuple[list[str], dict[int, list[dict[str, str]]]]:
    """Return CSV field names and reproducible reservoir samples for each configured size."""

    rng = random.Random(seed)
    samples: dict[int, list[dict[str, str]]] = {sample_size: [] for sample_size in SAMPLE_SIZES}

    with input_path.open("r", encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None:
            raise ValueError(f"Clean corpus file has no CSV header: {input_path}")
        fieldnames = reader.fieldnames
        for row_number, row in enumerate(reader, start=1):
            for sample_size, sample in samples.items():
                if len(sample) < sample_size:
                    sample.append(row)
                    continue
                replacement_index = rng.randrange(row_number)
                if replacement_index < sample_size:
                    sample[replacement_index] = row

    return fieldnames, samples


def export_samples(input_path: Path, output_dir: Path, seed: int) -> None:
    """Write random_100.csv and random_500.csv for manual inspection."""

    if not input_path.exists():
        raise FileNotFoundError(f"Clean corpus file does not exist: {input_path}")

    fieldnames, samples = reservoir_samples(input_path, seed)
    if not any(samples.values()):
        raise ValueError(f"Clean corpus file is empty: {input_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    for sample_size, sample in samples.items():
        with (output_dir / f"random_{sample_size}.csv").open("w", encoding="utf-8", newline="") as target:
            writer = csv.DictWriter(target, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sample)


def main() -> None:
    """Run the sampler."""

    args = parse_args()
    export_samples(args.input, args.output_dir, args.seed)


if __name__ == "__main__":
    main()
