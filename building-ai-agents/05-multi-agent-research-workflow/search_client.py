import os
from typing import Any

import requests


SEARXNG_URL = os.getenv("SEARXNG_URL", "http://localhost:8080")


def search_searx(
    search_term: str, time_range: str | None = None, count: int = 10
) -> list[dict[str, Any]]:
    params = {
        "q": search_term,
        "format": "json",
        "categories": "general",
    }

    if time_range:
        params["time_range"] = time_range

    response = requests.get(f"{SEARXNG_URL.rstrip('/')}/search", params=params, timeout=30)
    response.raise_for_status()

    payload = response.json()
    results = []

    for result in payload.get("results", [])[:count]:
        url = result.get("url")

        if not url:
            continue

        results.append(
            {
                "search_term": search_term,
                "url": url,
                "description": result.get("content") or result.get("title", ""),
            }
        )

    return results
