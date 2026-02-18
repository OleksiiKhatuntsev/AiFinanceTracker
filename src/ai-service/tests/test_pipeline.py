from decimal import Decimal
from pathlib import Path

import pytest

from pipeline import run


@pytest.fixture
def pipeline_result(sample_pdf_path):
    if not sample_pdf_path.exists():
        pytest.skip("Sample PDF not available")
    return run(sample_pdf_path)


class TestPipelineOutputStructure:
    def test_top_level_keys(self, pipeline_result):
        assert "sql" in pipeline_result
        assert "vector" in pipeline_result

    def test_sql_keys(self, pipeline_result):
        sql = pipeline_result["sql"]
        assert "account" in sql
        assert "summary" in sql
        assert "transactions_by_date" in sql

    def test_vector_has_chunks(self, pipeline_result):
        assert "chunks" in pipeline_result["vector"]


class TestSqlOutput:
    def test_account_holder(self, pipeline_result):
        assert pipeline_result["sql"]["account"]["holder"] == "Mr. O. Khatuntsev"

    def test_transaction_count(self, pipeline_result):
        summary = pipeline_result["sql"]["summary"]
        assert summary["debit_count"] == 29
        assert summary["credit_count"] == 1

    def test_transaction_totals(self, pipeline_result):
        summary = pipeline_result["sql"]["summary"]
        assert summary["total_debited"] == 857.71
        assert summary["total_credited"] == 200.00


class TestVectorOutput:
    def test_chunk_count(self, pipeline_result):
        chunks = pipeline_result["vector"]["chunks"]
        # 1 account + 11 daily + 30 tx + 2 raw page = 44
        assert len(chunks) == 44

    def test_all_chunks_have_ids(self, pipeline_result):
        for chunk in pipeline_result["vector"]["chunks"]:
            assert chunk["id"]
            assert isinstance(chunk["id"], str)
            assert len(chunk["id"]) > 0


class TestBalanceReconciliation:
    def test_balance_reconciliation(self, pipeline_result):
        account = pipeline_result["sql"]["account"]
        summary = pipeline_result["sql"]["summary"]
        opening = Decimal(str(account["opening_balance"]))
        closing = Decimal(str(account["closing_balance"]))
        debited = Decimal(str(summary["total_debited"]))
        credited = Decimal(str(summary["total_credited"]))
        assert opening - debited + credited == closing
