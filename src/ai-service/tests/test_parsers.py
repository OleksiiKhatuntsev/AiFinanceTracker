from datetime import date
from decimal import Decimal

import pytest

from parsers.abn_amro import AbnAmroParser, parse_european_amount


class TestParseEuropeanAmount:
    def test_simple(self):
        assert parse_european_amount("23,05") == Decimal("23.05")

    def test_thousands(self):
        assert parse_european_amount("1.234,56") == Decimal("1234.56")

    def test_empty(self):
        assert parse_european_amount("") is None

    def test_none(self):
        assert parse_european_amount(None) is None

    def test_integer(self):
        assert parse_european_amount("100,00") == Decimal("100.00")

    def test_whitespace(self):
        assert parse_european_amount("  42,50  ") == Decimal("42.50")

    def test_invalid(self):
        assert parse_european_amount("abc") is None


class TestAbnAmroParserIntegration:
    """Integration tests that require the sample PDF."""

    @pytest.fixture(autouse=True)
    def _parse(self, sample_pdf_path):
        if not sample_pdf_path.exists():
            pytest.skip("Sample PDF not available")
        parser = AbnAmroParser()
        self.metadata, self.transactions, self.raw_pages = parser.parse(sample_pdf_path)

    def test_extract_metadata_holder(self):
        assert self.metadata.holder == "Mr. O. Khatuntsev"

    def test_extract_metadata_account_number(self):
        assert self.metadata.number == "12.80.93.935"

    def test_extract_metadata_opening_balance(self):
        assert self.metadata.opening_balance == Decimal("889.59")

    def test_extract_metadata_closing_balance(self):
        assert self.metadata.closing_balance == Decimal("231.88")

    def test_extract_transactions_count(self):
        assert len(self.transactions) == 30

    def test_extract_transactions_types(self):
        debits = [t for t in self.transactions if t.type == "debit"]
        credits = [t for t in self.transactions if t.type == "credit"]
        assert len(debits) == 29
        assert len(credits) == 1

    def test_extract_transactions_totals(self):
        debits = [t for t in self.transactions if t.type == "debit"]
        credits = [t for t in self.transactions if t.type == "credit"]
        total_debited = sum(abs(t.amount) for t in debits)
        total_credited = sum(t.amount for t in credits)
        assert round(total_debited, 2) == Decimal("857.71")
        assert round(total_credited, 2) == Decimal("200.00")

    def test_transaction_dates_in_range(self):
        for tx in self.transactions:
            assert date(2026, 1, 31) <= tx.date <= date(2026, 2, 11)

    def test_raw_pages_extracted(self):
        assert len(self.raw_pages) == 2
        assert self.raw_pages[0]["page"] == 1
