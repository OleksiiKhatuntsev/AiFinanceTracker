from datetime import date
from decimal import Decimal

from models import AccountMetadata, Transaction, VectorChunk


def test_transaction_creation():
    tx = Transaction(
        date=date(2026, 1, 31),
        description="Test transaction",
        amount=Decimal("-23.05"),
        type="debit",
    )
    assert tx.date == date(2026, 1, 31)
    assert tx.amount == Decimal("-23.05")
    assert tx.type == "debit"


def test_account_metadata_creation(sample_metadata):
    assert sample_metadata.holder == "Mr. O. Khatuntsev"
    assert sample_metadata.number == "12.80.93.935"
    assert sample_metadata.opening_balance == Decimal("889.59")
    assert sample_metadata.closing_balance == Decimal("231.88")


def test_vector_chunk_creation():
    chunk = VectorChunk(
        id="test-001",
        text="Sample text",
        metadata={"source": "bank_statement", "type": "test"},
    )
    assert chunk.id == "test-001"
    assert chunk.text == "Sample text"
    assert chunk.metadata["source"] == "bank_statement"


def test_vector_chunk_default_metadata():
    chunk = VectorChunk(id="test-002", text="No metadata")
    assert chunk.metadata == {}
