#!/usr/bin/env python3
"""Collect raw Uzbek Wikipedia text for corpus construction.

The script uses the public MediaWiki API instead of a browser scrape. It queries
Uzbek Wikipedia pages in deterministic title order and writes plain-text extracts
into a single UTF-8 text file for later preprocessing.
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class WikipediaCollectionConfig:
    """Reproducible configuration for Uzbek Wikipedia collection."""

    api_url: str = "https://uz.wikipedia.org/w/api.php"
    output_path: Path = Path("dataset/raw/uzbek_wikipedia_raw.txt")
    batch_size: int = 50
    max_pages: int | None = None
    sleep_seconds: float = 0.2
    timeout_seconds: int = 30
    user_agent: str = "uzbek-spell-checker-paper/0.1 (research corpus collection)"


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Collect plain-text extracts from Uzbek Wikipedia."
    )
    parser.add_argument(
        "--api-url",
        default=WikipediaCollectionConfig.api_url,
        help="MediaWiki API endpoint to query.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=WikipediaCollectionConfig.output_path,
        help="Destination UTF-8 text file for collected raw text.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=WikipediaCollectionConfig.batch_size,
        help="Number of pages requested per API call. Use <= 50 for anonymous requests.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=WikipediaCollectionConfig.max_pages,
        help="Optional cap for reproducible small collection runs.",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=WikipediaCollectionConfig.sleep_seconds,
        help="Delay between API requests to avoid overloading the public endpoint.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=WikipediaCollectionConfig.timeout_seconds,
        help="HTTP timeout for API calls.",
    )
    parser.add_argument(
        "--user-agent",
        default=WikipediaCollectionConfig.user_agent,
        help="User-Agent header sent to the MediaWiki API.",
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


def build_query(config: WikipediaCollectionConfig, continuation: dict[str, str] | None) -> dict[str, str | int]:
    """Build a deterministic MediaWiki API query for article extracts."""

    query: dict[str, str | int] = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "generator": "allpages",
        "gapnamespace": "0",
        "gaplimit": config.batch_size,
        "prop": "extracts",
        "explaintext": "1",
        "exsectionformat": "plain",
        "redirects": "1",
    }
    if continuation:
        query.update(continuation)
    return query


def fetch_json(config: WikipediaCollectionConfig, query: dict[str, str | int]) -> dict[str, Any]:
    """Fetch one JSON response from the MediaWiki API."""

    url = f"{config.api_url}?{urlencode(query)}"
    request = Request(url, headers={"User-Agent": config.user_agent})
    try:
        with urlopen(request, timeout=config.timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"Failed to fetch Wikipedia data: {exc}") from exc


def iter_wikipedia_extracts(config: WikipediaCollectionConfig) -> tuple[int, list[str]]:
    """Collect page extracts from Uzbek Wikipedia.

    Returns a tuple containing the number of processed pages and a list of raw
    page texts. Keeping extraction separate from writing makes small test runs
    easy and keeps output encoding decisions in one place.
    """

    continuation: dict[str, str] | None = None
    collected_pages = 0
    extracts: list[str] = []

    while config.max_pages is None or collected_pages < config.max_pages:
        query = build_query(config, continuation)
        payload = fetch_json(config, query)
        pages = payload.get("query", {}).get("pages", [])

        if not pages:
            LOGGER.info("No more pages returned by the API.")
            break

        for page in pages:
            if config.max_pages is not None and collected_pages >= config.max_pages:
                break
            title = page.get("title", "")
            extract = page.get("extract", "").strip()
            if extract:
                extracts.append(f"# {title}\n{extract}")
            collected_pages += 1

        LOGGER.info("Collected %s pages so far.", collected_pages)
        continuation = payload.get("continue")
        if not continuation:
            break
        time.sleep(config.sleep_seconds)

    return collected_pages, extracts


def write_raw_corpus(output_path: Path, extracts: list[str]) -> None:
    """Write collected extracts to a UTF-8 text file."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n\n".join(extracts) + "\n", encoding="utf-8")


def main() -> None:
    """Run the Wikipedia collection pipeline."""

    args = parse_args()
    configure_logging(args.log_level)
    config = WikipediaCollectionConfig(
        api_url=args.api_url,
        output_path=args.output,
        batch_size=args.batch_size,
        max_pages=args.max_pages,
        sleep_seconds=args.sleep_seconds,
        timeout_seconds=args.timeout_seconds,
        user_agent=args.user_agent,
    )

    LOGGER.info("Starting Uzbek Wikipedia collection with config: %s", config)
    page_count, extracts = iter_wikipedia_extracts(config)
    write_raw_corpus(config.output_path, extracts)
    LOGGER.info(
        "Finished collection: %s pages, %s extracts written to %s.",
        page_count,
        len(extracts),
        config.output_path,
    )


if __name__ == "__main__":
    main()
