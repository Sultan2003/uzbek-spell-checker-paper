#!/usr/bin/env python3
"""Stream-clean the local Uzbek web corpus into a sentence-level CSV.

The primary raw corpus is expected at ``dataset/raw/uz.txt``.  The file can be
hundreds of megabytes or larger, so this script processes it line by line and
keeps only a set of normalized sentence hashes for exact deduplication.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import logging
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

LOGGER = logging.getLogger(__name__)

URL_RE = re.compile(r"(?:https?://|ftp://|www\.)\S+", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
TAG_RE = re.compile(r"<[^>]+>")
HTML_ENTITY_RE = re.compile(r"&(?:[a-zA-Z][a-zA-Z0-9]+|#[0-9]+|#x[0-9a-fA-F]+);")
WHITESPACE_RE = re.compile(r"\s+")
SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[.!?…])\s+|[\r\n]+")
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿĀ-žА-Яа-яЁёЎўҚқҒғҲҳʼ'`ʻ’‘-]+", re.UNICODE)
LETTER_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿĀ-žА-Яа-яЁёЎўҚқҒғҲҳ]", re.UNICODE)

APOSTROPHE_TRANSLATION = str.maketrans(
    {
        "‘": "'",
        "’": "'",
        "ʼ": "'",
        "`": "'",
        "´": "'",
        "ʹ": "'",
        "ʻ": "'",
        "＇": "'",
        "ꞌ": "'",
        "\u02bc": "'",
    }
)

METADATA_PATTERNS = (
    re.compile(r"^(?:id|url|date|time|author|source|title|category|tags?)\s*[:=]", re.IGNORECASE),
    re.compile(r"^(?:copyright|all rights reserved|barcha huquqlar himoyalangan)\b", re.IGNORECASE),
    re.compile(r"^\d{4}[-/.]\d{1,2}[-/.]\d{1,2}(?:\s+\d{1,2}:\d{2}(?::\d{2})?)?$"),
    re.compile(r"^\d{1,2}:\d{2}(?::\d{2})?$"),
)

NAVIGATION_TERMS = {
    "asosiy", "bosh sahifa", "yangiliklar", "aloqa", "biz haqimizda", "sayt xaritasi",
    "ro'yxatdan o'tish", "kirish", "chiqish", "menyu", "reklama", "izlash", "qidirish",
    "keyingi", "oldingi", "batafsil", "ko'proq", "читать далее", "главная", "поиск",
}

DIRECTORY_RE = re.compile(r"^(?:[\w .'-]+\s*[|/›>•·-]\s*){2,}[\w .'-]+$", re.UNICODE)
REPEATED_PUNCT_RE = re.compile(r"([!?.\-|_=*#])\1{3,}")


@dataclass(frozen=True)
class CorpusProcessingConfig:
    """Configuration for streaming Uzbek corpus processing."""

    input_path: Path = Path("dataset/raw/uz.txt")
    output_path: Path = Path("dataset/processed/clean_sentences.csv")
    min_chars: int = 25
    max_chars: int = 500
    min_words: int = 4
    max_non_letter_ratio: float = 0.35
    encoding: str = "utf-8"


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""

    parser = argparse.ArgumentParser(
        description="Stream-clean dataset/raw/uz.txt into dataset/processed/clean_sentences.csv."
    )
    parser.add_argument("--input", type=Path, default=CorpusProcessingConfig.input_path)
    parser.add_argument("--output", type=Path, default=CorpusProcessingConfig.output_path)
    parser.add_argument("--min-chars", type=int, default=CorpusProcessingConfig.min_chars)
    parser.add_argument("--max-chars", type=int, default=CorpusProcessingConfig.max_chars)
    parser.add_argument("--min-words", type=int, default=CorpusProcessingConfig.min_words)
    parser.add_argument("--max-non-letter-ratio", type=float, default=CorpusProcessingConfig.max_non_letter_ratio)
    parser.add_argument("--encoding", default=CorpusProcessingConfig.encoding)
    parser.add_argument("--log-every", type=int, default=250_000, help="Raw-line logging interval.")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
    )
    return parser.parse_args()


def configure_logging(level: str) -> None:
    """Configure process logging."""

    logging.basicConfig(level=getattr(logging, level), format="%(asctime)s %(levelname)s %(message)s")


def normalize_text(text: str) -> str:
    """Normalize apostrophes, remove web artifacts, and collapse whitespace."""

    text = html.unescape(text)
    text = URL_RE.sub(" ", text)
    text = EMAIL_RE.sub(" ", text)
    text = TAG_RE.sub(" ", text)
    text = HTML_ENTITY_RE.sub(" ", text)
    text = text.translate(APOSTROPHE_TRANSLATION)
    return WHITESPACE_RE.sub(" ", text).strip()


def split_sentences(line: str) -> Iterator[str]:
    """Yield conservative sentence candidates from one normalized line."""

    for candidate in SENTENCE_BOUNDARY_RE.split(line):
        candidate = candidate.strip(" \t\n\r\"“”«»")
        if candidate:
            yield candidate


def looks_like_metadata(text: str) -> bool:
    """Return True for obvious source metadata or boilerplate rows."""

    lowered = text.casefold().strip()
    if any(pattern.search(text) for pattern in METADATA_PATTERNS):
        return True
    if lowered in NAVIGATION_TERMS:
        return True
    if lowered.startswith(("cookie", "javascript", "var ", "function ")):
        return True
    return False


def looks_like_directory_entry(text: str) -> bool:
    """Return True for breadcrumb, menu, or directory-style rows."""

    if DIRECTORY_RE.match(text) and len(WORD_RE.findall(text)) <= 10:
        return True
    separators = sum(text.count(sep) for sep in ("|", "/", "›", "•", "·"))
    return separators >= 3 and len(text) < 120


def is_quality_sentence(text: str, config: CorpusProcessingConfig) -> bool:
    """Apply deterministic quality thresholds to a sentence candidate."""

    if len(text) < config.min_chars or len(text) > config.max_chars:
        return False
    if looks_like_metadata(text) or looks_like_directory_entry(text):
        return False
    if REPEATED_PUNCT_RE.search(text):
        return False

    words = WORD_RE.findall(text)
    if len(words) < config.min_words:
        return False
    letters = len(LETTER_RE.findall(text))
    if letters == 0:
        return False
    non_letter_ratio = (len(text) - letters) / max(len(text), 1)
    if non_letter_ratio > config.max_non_letter_ratio:
        return False

    avg_word_len = sum(len(word.strip("'-")) for word in words) / len(words)
    if avg_word_len < 2.0:
        return False
    return True


def dedupe_key(sentence: str) -> str:
    """Create a stable exact-deduplication key for a normalized sentence."""

    normalized = WHITESPACE_RE.sub(" ", sentence.casefold()).strip()
    return hashlib.blake2b(normalized.encode("utf-8"), digest_size=16).hexdigest()


def process_corpus(config: CorpusProcessingConfig, log_every: int) -> Counter[str]:
    """Stream the raw corpus, clean candidates, and write the output CSV."""

    if not config.input_path.exists():
        raise FileNotFoundError(f"Input corpus file does not exist: {config.input_path}")

    config.output_path.parent.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    counts: Counter[str] = Counter()

    with config.input_path.open("r", encoding=config.encoding, errors="replace") as source, config.output_path.open(
        "w", encoding="utf-8", newline=""
    ) as target:
        writer = csv.writer(target)
        writer.writerow(["id", "sentence"])
        next_id = 1

        for raw_line in source:
            counts["raw_lines"] += 1
            normalized_line = normalize_text(raw_line)
            if not normalized_line:
                counts["empty_or_artifact_lines"] += 1
                continue
            for sentence in split_sentences(normalized_line):
                counts["sentence_candidates"] += 1
                if not is_quality_sentence(sentence, config):
                    counts["low_quality_candidates"] += 1
                    continue
                key = dedupe_key(sentence)
                if key in seen:
                    counts["duplicate_candidates"] += 1
                    continue
                seen.add(key)
                writer.writerow([next_id, sentence])
                next_id += 1
                counts["retained_sentences"] += 1

            if log_every > 0 and counts["raw_lines"] % log_every == 0:
                LOGGER.info("Processed %s raw lines; retained %s sentences.", counts["raw_lines"], counts["retained_sentences"])

    LOGGER.info("Finished corpus processing: %s", dict(counts))
    return counts


def main() -> None:
    """Run the command-line corpus processor."""

    args = parse_args()
    configure_logging(args.log_level)
    config = CorpusProcessingConfig(
        input_path=args.input,
        output_path=args.output,
        min_chars=args.min_chars,
        max_chars=args.max_chars,
        min_words=args.min_words,
        max_non_letter_ratio=args.max_non_letter_ratio,
        encoding=args.encoding,
    )
    process_corpus(config, args.log_every)


if __name__ == "__main__":
    main()
