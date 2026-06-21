#!/usr/bin/env python3
"""Collect raw Uzbek Wikipedia text for corpus construction."""

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
    api_url: str = "https://uz.wikipedia.org/w/api.php"
    output_path: Path = Path("dataset/raw/uzbek_wikipedia_raw.txt")
    batch_size: int = 10
    max_pages: int | None = None
    sleep_seconds: float = 2
    timeout_seconds: int = 30
    user_agent: str = "uzbek-spell-checker-paper/0.1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-url", default=WikipediaCollectionConfig.api_url)
    parser.add_argument(
        "--output",
        type=Path,
        default=WikipediaCollectionConfig.output_path,
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=WikipediaCollectionConfig.batch_size,
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=WikipediaCollectionConfig.max_pages,
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=WikipediaCollectionConfig.sleep_seconds,
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=WikipediaCollectionConfig.timeout_seconds,
    )
    parser.add_argument(
        "--user-agent",
        default=WikipediaCollectionConfig.user_agent,
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
    )
    return parser.parse_args()


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


def fetch_json(
    config: WikipediaCollectionConfig,
    params: dict[str, Any],
) -> dict[str, Any]:
    url = f"{config.api_url}?{urlencode(params)}"

    request = Request(
        url,
        headers={"User-Agent": config.user_agent},
    )

    try:
        with urlopen(request, timeout=config.timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"Failed to fetch Wikipedia data: {exc}") from exc


def fetch_page_titles(
    config: WikipediaCollectionConfig,
    continuation: str | None,
) -> dict[str, Any]:
    params = {
        "action": "query",
        "format": "json",
        "list": "allpages",
        "apnamespace": 0,
        "aplimit": config.batch_size,
    }

    if continuation:
        params["apcontinue"] = continuation

    return fetch_json(config, params)


def fetch_extract(
    config: WikipediaCollectionConfig,
    title: str,
) -> str:
    params = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "prop": "extracts",
        "titles": title,
        "explaintext": 1,
        "exsectionformat": "plain",
    }

    payload = fetch_json(config, params)

    pages = payload.get("query", {}).get("pages", [])

    if not pages:
        return ""

    return pages[0].get("extract", "").strip()


def iter_wikipedia_extracts(
    config: WikipediaCollectionConfig,
) -> tuple[int, list[str]]:
    continuation: str | None = None
    collected_pages = 0
    extracts: list[str] = []

    while config.max_pages is None or collected_pages < config.max_pages:
        payload = fetch_page_titles(config, continuation)

        pages = payload.get("query", {}).get("allpages", [])

        if not pages:
            LOGGER.info("No more pages returned.")
            break

        for page in pages:
            if (
                config.max_pages is not None
                and collected_pages >= config.max_pages
            ):
                break

            title = page["title"]

            try:
                extract = fetch_extract(config, title)

                if extract:
                    extracts.append(f"# {title}\n{extract}")
                    collected_pages += 1

            except Exception as exc:
                LOGGER.warning(
                    "Failed to collect '%s': %s",
                    title,
                    exc,
                )

            time.sleep(config.sleep_seconds)

        LOGGER.info("Collected %s pages.", collected_pages)

        continuation = payload.get("continue", {}).get("apcontinue")

        if not continuation:
            break

    return collected_pages, extracts


def write_raw_corpus(
    output_path: Path,
    extracts: list[str],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        "\n\n".join(extracts) + "\n",
        encoding="utf-8",
    )


def main() -> None:
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

    LOGGER.info("Starting Uzbek Wikipedia collection")

    page_count, extracts = iter_wikipedia_extracts(config)

    write_raw_corpus(config.output_path, extracts)

    LOGGER.info(
        "Finished collection: %s pages, %s extracts written.",
        page_count,
        len(extracts),
    )


if __name__ == "__main__":
    main()
