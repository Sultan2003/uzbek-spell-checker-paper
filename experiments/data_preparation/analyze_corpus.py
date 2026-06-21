#!/usr/bin/env python3
"""Generate descriptive statistics for the cleaned Uzbek sentence corpus."""

from __future__ import annotations

import argparse
import csv
import json
import logging
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

LOGGER = logging.getLogger(__name__)
REPO_ROOT = Path(__file__).resolve().parents[2]
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿĀ-žА-Яа-яЁёЎўҚқҒғҲҳʼ']+", re.UNICODE)


@dataclass(frozen=True)
class AnalysisConfig:
    """Configuration for cleaned-corpus statistics."""

    input_path: Path = REPO_ROOT / "dataset" / "processed" / "clean_sentences.csv"
    output_path: Path | None = REPO_ROOT / "dataset" / "processed" / "corpus_statistics.json"
    top_k: int = 50


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""

    parser = argparse.ArgumentParser(description="Analyze cleaned Uzbek corpus statistics.")
    parser.add_argument("--input", type=Path, default=AnalysisConfig.input_path)
    parser.add_argument("--output", type=Path, default=AnalysisConfig.output_path)
    parser.add_argument("--top-k", type=int, default=AnalysisConfig.top_k)
    parser.add_argument("--no-output", action="store_true", help="Print statistics without writing JSON.")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
    )
    return parser.parse_args()


def configure_logging(level: str) -> None:
    """Configure process logging."""

    logging.basicConfig(level=getattr(logging, level), format="%(asctime)s %(levelname)s %(message)s")


def analyze_corpus(input_path: Path, top_k: int) -> dict[str, object]:
    """Stream the cleaned CSV and compute corpus-level statistics."""

    if not input_path.exists():
        raise FileNotFoundError(f"Cleaned corpus file does not exist: {input_path}")

    sentence_count = 0
    total_chars = 0
    total_words = 0
    min_chars: int | None = None
    max_chars = 0
    unique_sentences: set[str] = set()
    vocabulary: Counter[str] = Counter()

    with input_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames != ["id", "sentence"]:
            raise ValueError(f"Expected CSV header ['id', 'sentence'], found {reader.fieldnames}")
        for row in reader:
            sentence = row["sentence"].strip()
            if not sentence:
                continue
            sentence_count += 1
            unique_sentences.add(sentence.casefold())
            char_len = len(sentence)
            total_chars += char_len
            min_chars = char_len if min_chars is None else min(min_chars, char_len)
            max_chars = max(max_chars, char_len)
            words = [word.casefold() for word in WORD_RE.findall(sentence)]
            total_words += len(words)
            vocabulary.update(words)

    stats: dict[str, object] = {
        "retained_lines": sentence_count,
        "unique_sentences": len(unique_sentences),
        "duplicate_sentences_in_clean_csv": sentence_count - len(unique_sentences),
        "average_sentence_length_chars": round(total_chars / sentence_count, 2) if sentence_count else 0,
        "average_sentence_length_words": round(total_words / sentence_count, 2) if sentence_count else 0,
        "min_sentence_length_chars": min_chars or 0,
        "max_sentence_length_chars": max_chars,
        "total_tokens": total_words,
        "vocabulary_size_estimate": len(vocabulary),
        "top_tokens": vocabulary.most_common(top_k),
    }
    return stats


def main() -> None:
    """Run the command-line corpus analyzer."""

    args = parse_args()
    configure_logging(args.log_level)
    output_path = None if args.no_output else args.output
    stats = analyze_corpus(args.input, args.top_k)
    LOGGER.info("Corpus statistics:\n%s", json.dumps(stats, ensure_ascii=False, indent=2))
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        LOGGER.info("Wrote statistics to %s", output_path)


if __name__ == "__main__":
    main()
