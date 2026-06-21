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
import json
import logging
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

LOGGER = logging.getLogger(__name__)
REPO_ROOT = Path(__file__).resolve().parents[2]

URL_RE = re.compile(r"(?:https?://|ftp://|www\.)\S+", re.IGNORECASE)
LEADING_NUMERIC_RE = re.compile(r"^\d+\s+")
FLOATING_SCORE_RE = re.compile(r"(?:^|\s)\d+\.\d{2,6}(?:\s|$)")
RANKING_ENTRY_RE = re.compile(r"^(?:№|#)?\s*\d{1,4}[.):-]?\s+\S+")
ENCODING_CORRUPTION_RE = re.compile(r"(?:�|Ã.|Ð.|Ñ.|â[€™€œ€“]|\?\?+)")
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
    "home", "about", "contact", "login", "logout", "register", "search", "news",
    "sitemap", "rss", "print", "share", "comments", "categories", "archive",
}

DIRECTORY_RE = re.compile(r"^(?:[\w .'-]+\s*[|/›>•·-]\s*){2,}[\w .'-]+$", re.UNICODE)
PATHLIKE_RE = re.compile(r"^(?:[A-Za-z0-9_.-]+/){2,}[A-Za-z0-9_.-]*/?$")
REPEATED_PUNCT_RE = re.compile(r"([!?.\-|_=*#])\1{3,}")


@dataclass(frozen=True)
class CorpusProcessingConfig:
    """Configuration for streaming Uzbek corpus processing."""

    input_path: Path = REPO_ROOT / "dataset" / "raw" / "uz.txt"
    output_path: Path = REPO_ROOT / "dataset" / "processed" / "clean_sentences.csv"
    report_path: Path = REPO_ROOT / "dataset" / "processed" / "filtering_report.json"
    min_chars: int = 25
    max_chars: int = 500
    min_words: int = 4
    max_non_letter_ratio: float = 0.35
    max_digits_ratio: float = 0.15
    max_separator_count: int = 2
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
    parser.add_argument("--report", type=Path, default=CorpusProcessingConfig.report_path)
    parser.add_argument("--max-non-letter-ratio", type=float, default=CorpusProcessingConfig.max_non_letter_ratio)
    parser.add_argument("--max-digits-ratio", type=float, default=CorpusProcessingConfig.max_digits_ratio)
    parser.add_argument("--max-separator-count", type=int, default=CorpusProcessingConfig.max_separator_count)
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
    if LEADING_NUMERIC_RE.search(text) or FLOATING_SCORE_RE.search(text) or RANKING_ENTRY_RE.search(text):
        return True
    if lowered in NAVIGATION_TERMS:
        return True
    if lowered.startswith(("cookie", "javascript", "var ", "function ", "document.", "window.")):
        return True
    return False


def looks_like_directory_entry(text: str) -> bool:
    """Return True for breadcrumb, menu, or directory-style rows."""

    if PATHLIKE_RE.match(text):
        return True
    if DIRECTORY_RE.match(text) and len(WORD_RE.findall(text)) <= 10:
        return True
    separators = sum(text.count(sep) for sep in ("|", "/", "›", "•", "·"))
    return separators > 2 and len(text) < 120


def filtering_reason(text: str, config: CorpusProcessingConfig) -> str | None:
    """Return the first deterministic rejection reason for a sentence candidate."""

    if len(text) < config.min_chars:
        return "too_short"
    if len(text) > config.max_chars:
        return "too_long"
    if URL_RE.search(text) or EMAIL_RE.search(text):
        return "url_or_email"
    if ENCODING_CORRUPTION_RE.search(text):
        return "encoding_corruption"
    if looks_like_metadata(text):
        return "metadata_or_ranking"
    if looks_like_directory_entry(text):
        return "directory_or_navigation"
    if REPEATED_PUNCT_RE.search(text):
        return "repeated_punctuation"

    words = WORD_RE.findall(text)
    if len(words) < config.min_words:
        return "too_few_words"
    letters = len(LETTER_RE.findall(text))
    if letters == 0:
        return "no_letters"
    non_letter_ratio = (len(text) - letters) / max(len(text), 1)
    if non_letter_ratio > config.max_non_letter_ratio:
        return "high_non_letter_ratio"
    digits_ratio = sum(ch.isdigit() for ch in text) / max(len(text), 1)
    if digits_ratio > config.max_digits_ratio:
        return "high_digit_ratio"
    separator_count = sum(text.count(sep) for sep in ("|", "/", "›", "•", "·", "\\"))
    if separator_count > config.max_separator_count:
        return "too_many_separators"

    avg_word_len = sum(len(word.strip("'-")) for word in words) / len(words)
    if avg_word_len < 2.0:
        return "low_average_word_length"
    return None


def is_quality_sentence(text: str, config: CorpusProcessingConfig) -> bool:
    """Apply deterministic quality thresholds to a sentence candidate."""

    return filtering_reason(text, config) is None


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
                reason = filtering_reason(sentence, config)
                if reason is not None:
                    counts["low_quality_candidates"] += 1
                    counts[f"rejected_{reason}"] += 1
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

    report = {
        "input_path": str(config.input_path),
        "output_path": str(config.output_path),
        "thresholds": {
            "min_chars": config.min_chars,
            "max_chars": config.max_chars,
            "min_words": config.min_words,
            "max_non_letter_ratio": config.max_non_letter_ratio,
            "max_digits_ratio": config.max_digits_ratio,
            "max_separator_count": config.max_separator_count,
        },
        "counts": dict(counts),
    }
    config.report_path.parent.mkdir(parents=True, exist_ok=True)
    config.report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    LOGGER.info("Wrote filtering report to %s", config.report_path)
    LOGGER.info("Finished corpus processing: %s", dict(counts))
    return counts


def main() -> None:
    """Run the command-line corpus processor."""

    args = parse_args()
    configure_logging(args.log_level)
    config = CorpusProcessingConfig(
        input_path=args.input,
        output_path=args.output,
        report_path=args.report,
        min_chars=args.min_chars,
        max_chars=args.max_chars,
        min_words=args.min_words,
        max_non_letter_ratio=args.max_non_letter_ratio,
        max_digits_ratio=args.max_digits_ratio,
        max_separator_count=args.max_separator_count,
        encoding=args.encoding,
    )
    process_corpus(config, args.log_every)


if __name__ == "__main__":
    main()
