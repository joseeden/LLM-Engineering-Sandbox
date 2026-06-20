import json
import os
from typing import Any, Optional, Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class SearxNGSearchInput(BaseModel):
    """Input schema for SearxNGSearchTool."""

    query: str = Field(..., description="Search query to send to the local SearXNG instance.")
    count: int = Field(
        5,
        ge=1,
        le=10,
        description="Maximum number of search results to return.",
    )
    time_range: Optional[str] = Field(
        None,
        description="Optional SearXNG time range, such as day, week, month, or year.",
    )


class SearxNGSearchTool(BaseTool):
    name: str = "Search the web with SearXNG"
    description: str = (
        "Searches the web using a local SearXNG instance and returns titles, URLs, "
        "and short descriptions for relevant results."
    )
    args_schema: Type[BaseModel] = SearxNGSearchInput

    def _run(
        self,
        query: str,
        count: int = 5,
        time_range: Optional[str] = None,
    ) -> str:
        searxng_url = os.getenv("SEARXNG_URL", "http://localhost:8080").rstrip("/")
        params: dict[str, Any] = {
            "q": query,
            "format": "json",
            "categories": "general",
        }

        if time_range:
            params["time_range"] = time_range

        try:
            response = requests.get(
                f"{searxng_url}/search",
                params=params,
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException as error:
            return (
                "SearXNG search failed. Make sure the local SearXNG container is "
                f"running and SEARXNG_URL is correct. Details: {error}"
            )
        except ValueError as error:
            return f"SearXNG returned a non-JSON response. Details: {error}"

        results = []
        for result in payload.get("results", [])[:count]:
            url = result.get("url")
            if not url:
                continue

            results.append(
                {
                    "title": result.get("title", "Untitled result"),
                    "url": url,
                    "content": result.get("content") or result.get("description", ""),
                }
            )

        if not results:
            return f"No SearXNG results found for query: {query}"

        return json.dumps(results, indent=2)
