from typing import Literal

from pydantic import BaseModel, Field


class SearchConfig(BaseModel):
    search_terms: list[str]
    time_range: Literal["day", "month", "year"] | None = Field(
        default=None,
        description=(
            "Optional SearxNG time range for the web search results. "
            "Use day, month, year, or null when no time filter is needed."
        ),
    )
