from __future__ import annotations

from typing import Any, Protocol

from models import AccountMetadata, Transaction, VectorChunk


class ChunkBuilder(Protocol):
    def build(
        self,
        metadata: AccountMetadata,
        transactions: list[Transaction],
        *,
        raw_pages: list[dict[str, Any]] | None = None,
    ) -> list[VectorChunk]: ...
