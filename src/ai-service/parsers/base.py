from __future__ import annotations

from pathlib import Path
from typing import Protocol

from models import AccountMetadata, Transaction


class StatementParser(Protocol):
    def parse(self, pdf_path: Path) -> tuple[AccountMetadata, list[Transaction]]: ...
