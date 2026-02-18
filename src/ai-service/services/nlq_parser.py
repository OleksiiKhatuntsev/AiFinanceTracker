from __future__ import annotations

from datetime import date
from typing import Protocol

from schemas import NlqParseResponse


class NlqParser(Protocol):
    async def parse(self, question: str) -> NlqParseResponse: ...


class GeminiNlqParser:
    def __init__(self, chain) -> None:
        self._chain = chain

    async def parse(self, question: str) -> NlqParseResponse:
        return await self._chain.ainvoke(
            {
                "question": question,
                "current_date": date.today().isoformat(),
            }
        )
