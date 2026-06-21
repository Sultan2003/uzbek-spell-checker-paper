#!/usr/bin/env python3
"""Sample and audit cleaned Uzbek corpus rows for residual quality issues."""

from __future__ import annotations

import argparse
import csv
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = REPO_ROOT / "dataset" / "processed" / "clean_sentences.csv"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "dataset" / "processed" / "audit_samples"

URL_RE = re.compile(r"(?:https?://|ftp://|www\.|\b\S+\.(?:uz|com|org|net|ru)\b)", re.IGNORECASE)
NUMERIC_METADATA_RE = re.compile(r"^\d+\s+.*(?:\s\d+\.\d{2,6})?$")
FLOATING_SCORE_RE = re.compile(r"(?:^|\s)\d+\.\d{2,6}(?:\s|$)")
RANKING_RE = re.compile(r"^(?:№|#)?\s*\d{1,4}[.):-]?\s+\S+")
ENCODING_RE = re.compile(r"(?:�|Ã.|Ð.|Ñ.|â[€™€œ€“]|\?\?+)")
DIRECTORY_RE = re.compile(r"^(?:[\w .'-]+\s*[|/›>•·-]\s*){2,}[\w .'-]+$", re.UNICODE)
PATHLIKE_RE = re.compile(r"^(?:[A-Za-z0-9_.-]+/){2,}[A-Za-z0-9_.-]*/?$")
UZBEK_LATIN_RE = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿĀ-ž0-9\s.,!?;:'\"()\[\]{}%+\-–—/\\]+$", re.UNICODE)
CYRILLIC_RE = re.compile(r"[А-Яа-яЁёЎўҚқҒғҲҳ]")
NAVIGATION_TERMS = {
    "asosiy", "bosh sahifa", "yangiliklar", "aloqa", "biz haqimizda", "sayt xaritasi",
    "ro'yxatdan o'tish", "kirish", "chiqish", "menyu", "reklama", "izlash", "qidirish",
    "keyingi", "oldingi", "batafsil", "ko'proq", "home", "about", "contact", "login",
    "logout", "register", "search", "news", "sitemap", "rss", "print", "share",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export random corpus audit samples and issue reports.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--sample-sizes", type=int, nargs="+", default=[500, 1000])
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--short-threshold", type=int, default=25)
    parser.add_argument("--long-threshold", type=int, default=500)
    return parser.parse_args()


def detect_issues(sentence: str, short_threshold: int, long_threshold: int) -> list[str]:
    lowered = sentence.casefold().strip()
    issues: list[str] = []
    if NUMERIC_METADATA_RE.search(sentence) or FLOATING_SCORE_RE.search(sentence):
        issues.append("numeric_metadata")
    if RANKING_RE.search(sentence):
        issues.append("ranking_style")
    if URL_RE.search(sentence):
        issues.append("url_contamination")
    if ENCODING_RE.search(sentence):
        issues.append("encoding_corruption")
    if len(sentence) < short_threshold:
        issues.append("extremely_short")
    if len(sentence) > long_threshold:
        issues.append("extremely_long")
    if DIRECTORY_RE.search(sentence) or PATHLIKE_RE.search(sentence) or lowered in NAVIGATION_TERMS:
        issues.append("directory_or_navigation")
    if not UZBEK_LATIN_RE.match(sentence) or CYRILLIC_RE.search(sentence):
        issues.append("non_uzbek_character_pattern")
    return issues


def reservoir_sample(path: Path, sample_size: int, seed: int) -> list[dict[str, str]]:
    rng = random.Random(seed)
    sample: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        for index, row in enumerate(reader, start=1):
            if len(sample) < sample_size:
                sample.append(row)
            else:
                replacement = rng.randint(1, index)
                if replacement <= sample_size:
                    sample[replacement - 1] = row
    return sample


def write_sample(path: Path, rows: list[dict[str, str]], short_threshold: int, long_threshold: int) -> Counter[str]:
    issue_counts: Counter[str] = Counter()
    with path.open("w", encoding="utf-8", newline="") as target:
        fieldnames = ["id", "sentence", "issues"]
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            sentence = row.get("sentence", "")
            issues = detect_issues(sentence, short_threshold, long_threshold)
            issue_counts.update(issues)
            writer.writerow({"id": row.get("id", ""), "sentence": sentence, "issues": ";".join(issues)})
    return issue_counts


def main() -> None:
    args = parse_args()
    if not args.input.exists():
        raise FileNotFoundError(f"Input cleaned corpus does not exist: {args.input}")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    summary: dict[str, object] = {
        "input_path": str(args.input),
        "seed": args.seed,
        "thresholds": {"short_chars": args.short_threshold, "long_chars": args.long_threshold},
        "samples": {},
    }
    for size in args.sample_sizes:
        rows = reservoir_sample(args.input, size, args.seed + size)
        output_path = args.output_dir / f"audit_sample_{size}.csv"
        issue_counts = write_sample(output_path, rows, args.short_threshold, args.long_threshold)
        summary["samples"][str(size)] = {
            "path": str(output_path),
            "rows_exported": len(rows),
            "issue_counts": dict(issue_counts),
        }

    summary_path = args.output_dir / "audit_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
