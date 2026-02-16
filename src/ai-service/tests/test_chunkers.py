from datetime import date
from decimal import Decimal

from chunkers.transaction import (
    AccountSummaryChunkBuilder,
    DailySummaryChunkBuilder,
    TransactionChunkBuilder,
)
from models import AccountMetadata, Transaction


class TestTransactionChunkBuilder:
    def test_debit_text(self, sample_metadata, sample_transactions):
        builder = TransactionChunkBuilder()
        chunks = builder.build(sample_metadata, [sample_transactions[0]])
        assert len(chunks) == 1
        assert "debit of \u20ac23.05" in chunks[0].text
        assert "Albert Heijn 1276" in chunks[0].text

    def test_credit_text(self, sample_metadata, sample_transactions):
        builder = TransactionChunkBuilder()
        chunks = builder.build(sample_metadata, [sample_transactions[2]])
        assert len(chunks) == 1
        assert "credit of \u20ac200.00" in chunks[0].text
        assert "received from" in chunks[0].text

    def test_metadata_keys(self, sample_metadata, sample_transactions):
        builder = TransactionChunkBuilder()
        chunks = builder.build(sample_metadata, [sample_transactions[0]])
        meta = chunks[0].metadata
        expected_keys = {"source", "account", "date", "amount", "type", "merchant", "raw_description"}
        assert set(meta.keys()) == expected_keys

    def test_chunk_ids_deterministic(self, sample_metadata, sample_transactions):
        builder = TransactionChunkBuilder()
        chunks1 = builder.build(sample_metadata, sample_transactions)
        chunks2 = builder.build(sample_metadata, sample_transactions)
        ids1 = [c.id for c in chunks1]
        ids2 = [c.id for c in chunks2]
        assert ids1 == ids2


class TestDailySummaryChunkBuilder:
    def test_chunk_count(self, sample_metadata, sample_transactions):
        builder = DailySummaryChunkBuilder()
        chunks = builder.build(sample_metadata, sample_transactions)
        # 3 transactions on 2 dates (Jan 31 and Feb 8)
        assert len(chunks) == 2

    def test_daily_totals(self, sample_metadata, sample_transactions):
        builder = DailySummaryChunkBuilder()
        chunks = builder.build(sample_metadata, sample_transactions)
        # First chunk is Jan 31 (2 debits)
        jan31 = next(c for c in chunks if "2026-01-31" in c.id)
        assert "\u20ac33.55" in jan31.text  # 23.05 + 10.50
        assert "2 debit(s)" in jan31.text


class TestAccountSummaryChunkBuilder:
    def test_summary_text(self, sample_metadata, sample_transactions):
        builder = AccountSummaryChunkBuilder()
        chunks = builder.build(sample_metadata, sample_transactions)
        assert len(chunks) == 1
        text = chunks[0].text
        assert "Mr. O. Khatuntsev" in text
        assert "12.80.93.935" in text
        assert "\u20ac889.59" in text
        assert "\u20ac231.88" in text
