from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class StructuredFilter(BaseModel):
    category: str | None = None
    date_from: str | None = None
    date_to: str | None = None
    merchant: str | None = None
    aggregation: Literal["sum", "count", "avg", "min", "max"] | None = None


class NlqRequest(BaseModel):
    question: str


class NlqParseResponse(BaseModel):
    search_type: Literal["structured", "semantic"]
    structured_filter: StructuredFilter | None = None
