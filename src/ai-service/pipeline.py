from __future__ import annotations

import json
import sys
from collections import OrderedDict
from dataclasses import asdict
from itertools import groupby
from pathlib import Path

from chunkers import (
    AccountSummaryChunkBuilder,
    ChunkBuilder,
    DailySummaryChunkBuilder,
    RawPageChunkBuilder,
    TransactionChunkBuilder,
)
from models import AccountMetadata, Transaction, VectorChunk
from parsers import AbnAmroParser, StatementParser


def _group_by_date(transactions: list[Transaction]) -> OrderedDict:
    """Group transactions by date, preserving order."""
    grouped: OrderedDict[str, list[dict]] = OrderedDict()
    sorted_txns = sorted(transactions, key=lambda t: t.date)
    for date_val, group_iter in groupby(sorted_txns, key=lambda t: t.date):
        date_iso = date_val.isoformat()
        grouped[date_iso] = [
            {
                "description": t.description,
                "amount": float(t.amount),
                "type": t.type,
            }
            for t in group_iter
        ]
    return grouped


def _build_sql_output(
    metadata: AccountMetadata, transactions: list[Transaction]
) -> dict:
    """Build the SQL-oriented output dict."""
    debits = [t for t in transactions if t.type == "debit"]
    credits = [t for t in transactions if t.type == "credit"]

    summary = {
        "total_debited": float(round(sum(abs(t.amount) for t in debits), 2)),
        "total_credited": float(round(sum(t.amount for t in credits), 2)),
        "debit_count": len(debits),
        "credit_count": len(credits),
    }

    account_dict = {
        "holder": metadata.holder,
        "number": metadata.number,
        "date_from": metadata.date_from.isoformat(),
        "date_to": metadata.date_to.isoformat(),
        "opening_balance": float(metadata.opening_balance),
        "closing_balance": float(metadata.closing_balance),
    }

    return {
        "account": account_dict,
        "summary": summary,
        "transactions_by_date": _group_by_date(transactions),
    }


def run(
    pdf_path: Path,
    parser: StatementParser | None = None,
    chunk_builders: list[ChunkBuilder] | None = None,
) -> dict:
    """Parse a bank statement PDF and produce SQL + vector output."""
    if parser is None:
        parser = AbnAmroParser()

    if chunk_builders is None:
        chunk_builders = [
            AccountSummaryChunkBuilder(),
            DailySummaryChunkBuilder(),
            TransactionChunkBuilder(),
            RawPageChunkBuilder(),
        ]

    metadata, transactions, raw_pages = parser.parse(pdf_path)

    sql_output = _build_sql_output(metadata, transactions)

    chunks: list[VectorChunk] = []
    for builder in chunk_builders:
        chunks.extend(builder.build(metadata, transactions, raw_pages=raw_pages))

    return {
        "sql": sql_output,
        "vector": {
            "chunks": [asdict(c) for c in chunks],
        },
    }


def main() -> None:
    if len(sys.argv) < 2:
        pdf_path = Path(__file__).parent / "samples" / "example_1.pdf"
    else:
        pdf_path = Path(sys.argv[1])

    result = run(pdf_path)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
