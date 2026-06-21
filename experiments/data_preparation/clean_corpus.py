#!/usr/bin/env python3
"""Clean raw Uzbek text and export a sentence-level corpus CSV."""

from __future__ import annotations

import argparse
import csv
import html
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


LOGGER = logging.getLogger(__name__)
URL_RE = re.compile(r"https?://\S+|www\.\S+", flags=re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")
SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[.!?])\s+")
APOSTROPHE_TRANSLATION = str.maketrans({
    "‘": "'",
    "’": "'",
    "ʼ": "'",
    "`": "'",
    "´": "'",
    "ʹ": "'",
    "ʻ": "'",
    "＇": "'",
})


@dataclass(frozen=True)
class CleaningConfig:
    """Configuration for deterministic raw-corpus cleaning."""

    input_path: Path = Path("dataset/raw/uzbek_wikipedia_raw.txt")
    output_path: Path = Path("dataset/processed/clean_sentences.csv")
    min_chars: int = 2


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description="Clean raw Uzbek corpus text into CSV.")
    parser.add_argument(
        "--input",
        type=Path,
        default=CleaningConfig.input_path,
        help="Raw UTF-8 text file to clean.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=CleaningConfig.output_path,
        help="Destination CSV path with id,sentence columns.",
    )
    parser.add_argument(
        "--min-chars",
        type=int,
        default=CleaningConfig.min_chars,
        help="Minimum sentence length after cleaning.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
        help="Logging verbosity.",
    )
    return parser.parse_args()


def configure_logging(level: str) -> None:
    """Configure application logging."""

    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


def normalize_text(text: str) -> str:
    """Apply URL, HTML, apostrophe, and whitespace normalization."""

    text = html.unescape(text)
    text = URL_RE.sub(" ", text)
    text = TAG_RE.sub(" ", text)
    text = text.translate(APOSTROPHE_TRANSLATION)
    return WHITESPACE_RE.sub(" ", text).strip()


def split_sentences(line: str) -> Iterable[str]:
    """Split a normalized line into coarse sentence candidates."""

    # This conservative rule keeps abbreviations imperfect but avoids adding a
    # heavy NLP dependency before the modeling stage is introduced.
    for sentence in SENTENCE_BOUNDARY_RE.split(line):
        sentence = sentence.strip()
        if sentence:
            yield sentence


def clean_sentences(raw_text: str, min_chars: int) -> list[str]:
    """Remove empty lines, normalize text, and deduplicate sentences."""

    seen: set[str] = set()
    cleaned: list[str] = []

    for raw_line in raw_text.splitlines():
        normalized_line = normalize_text(raw_line)
        if not normalized_line:
            continue
        for sentence in split_sentences(normalized_line):
            if len(sentence) < min_chars:
                continue
            dedupe_key = sentence.casefold()
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            cleaned.append(sentence)

    return cleaned


def write_sentences_csv(output_path: Path, sentences: list[str]) -> None:
    """Write cleaned sentences to a UTF-8 CSV with stable integer IDs."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["id", "sentence"])
        for sentence_id, sentence in enumerate(sentences, start=1):
            writer.writerow([sentence_id, sentence])


def main() -> None:
    """Run the corpus cleaning pipeline."""

    args = parse_args()
    configure_logging(args.log_level)
    config = CleaningConfig(
        input_path=args.input,
        output_path=args.output,
        min_chars=args.min_chars,
    )

    if not config.input_path.exists():
        raise FileNotFoundError(f"Input corpus file does not exist: {config.input_path}")

    LOGGER.info("Reading raw corpus from %s.", config.input_path)
    raw_text = config.input_path.read_text(encoding="utf-8")
    sentences = clean_sentences(raw_text, config.min_chars)
    write_sentences_csv(config.output_path, sentences)
    LOGGER.info("Wrote %s unique cleaned sentences to %s.", len(sentences), config.output_path)


if __name__ == "__main__":
    main()
