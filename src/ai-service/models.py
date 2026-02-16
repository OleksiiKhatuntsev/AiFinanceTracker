from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Any, Literal


@dataclass
class Transaction:
    date: date
    description: str
    amount: Decimal
    type: Literal["debit", "credit"]


@dataclass
class AccountMetadata:
    holder: str
    number: str
    date_from: date
    date_to: date
    opening_balance: Decimal
    closing_balance: Decimal


@dataclass
class VectorChunk:
    id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)
