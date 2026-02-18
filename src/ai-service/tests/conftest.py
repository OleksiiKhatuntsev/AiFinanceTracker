from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from models import AccountMetadata, Transaction


@pytest.fixture
def sample_pdf_path():
    return Path(__file__).parent.parent / "samples" / "example_1.pdf"


@pytest.fixture
def sample_metadata():
    return AccountMetadata(
        holder="Mr. O. Khatuntsev",
        number="12.80.93.935",
        date_from=date(2026, 2, 1),
        date_to=date(2026, 2, 11),
        opening_balance=Decimal("889.59"),
        closing_balance=Decimal("231.88"),
    )


@pytest.fixture
def sample_transactions():
    """A small list of 3 known transactions for unit tests."""
    return [
        Transaction(
            date=date(2026, 1, 31),
            description="BEA, Apple Pay Albert Heijn 1276,PAS541",
            amount=Decimal("-23.05"),
            type="debit",
        ),
        Transaction(
            date=date(2026, 1, 31),
            description="BEA, Apple Pay Bolo Doner,PAS541",
            amount=Decimal("-10.50"),
            type="debit",
        ),
        Transaction(
            date=date(2026, 2, 8),
            description="/TRTP/SEPA OVERBOEKING/IBAN/NL13ABNA/BIC/ABNANL2A/NAME/AAB INZ TIKKIE/REMI/test",
            amount=Decimal("200.00"),
            type="credit",
        ),
    ]
