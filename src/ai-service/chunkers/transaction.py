from __future__ import annotations

import hashlib
from itertools import groupby
from typing import Any

from models import AccountMetadata, Transaction, VectorChunk
from parsers.merchant import classify_merchant


def _deterministic_hash(text: str) -> str:
    """Return a stable 8-digit hex hash for chunk IDs."""
    return hashlib.md5(text.encode()).hexdigest()[:8]


class TransactionChunkBuilder:
    """One semantic chunk per transaction."""

    def build(
        self,
        metadata: AccountMetadata,
        transactions: list[Transaction],
        *,
        raw_pages: list[dict[str, Any]] | None = None,
    ) -> list[VectorChunk]:
        account = metadata.number or ""
        chunks: list[VectorChunk] = []

        for tx in transactions:
            merchant = classify_merchant(tx.description)
            date_human = tx.date.strftime("%B %d, %Y")
            abs_amount = abs(tx.amount)

            if tx.type == "debit":
                sentence = (
                    f"On {date_human}, a debit of \u20ac{abs_amount:.2f} was made "
                    f"to {merchant}."
                )
            else:
                sentence = (
                    f"On {date_human}, a credit of \u20ac{abs_amount:.2f} was received "
                    f"from {merchant}."
                )

            chunk_id = f"tx-{tx.date.isoformat()}-{_deterministic_hash(tx.description)}"

            chunks.append(
                VectorChunk(
                    id=chunk_id,
                    text=sentence,
                    metadata={
                        "source": "bank_statement",
                        "account": account,
                        "date": tx.date.isoformat(),
                        "amount": float(tx.amount),
                        "type": tx.type,
                        "merchant": merchant,
                        "raw_description": tx.description,
                    },
                )
            )

        return chunks


class DailySummaryChunkBuilder:
    """One chunk per day summarising that day's activity."""

    def build(
        self,
        metadata: AccountMetadata,
        transactions: list[Transaction],
        *,
        raw_pages: list[dict[str, Any]] | None = None,
    ) -> list[VectorChunk]:
        account = metadata.number or ""
        chunks: list[VectorChunk] = []

        sorted_txns = sorted(transactions, key=lambda t: t.date)
        for date_val, group_iter in groupby(sorted_txns, key=lambda t: t.date):
            group = list(group_iter)
            debits = [t for t in group if t.type == "debit"]
            credits = [t for t in group if t.type == "credit"]
            total_out = round(sum(abs(t.amount) for t in debits), 2)
            total_in = round(sum(t.amount for t in credits), 2)
            date_human = date_val.strftime("%B %d, %Y")
            date_iso = date_val.isoformat()

            parts = [f"Daily summary for {date_human}:"]
            if debits:
                merchants = [classify_merchant(t.description) for t in debits]
                parts.append(
                    f"{len(debits)} debit(s) totalling \u20ac{total_out:.2f} "
                    f"at {', '.join(merchants)}."
                )
            if credits:
                merchants = [classify_merchant(t.description) for t in credits]
                parts.append(
                    f"{len(credits)} credit(s) totalling \u20ac{total_in:.2f} "
                    f"from {', '.join(merchants)}."
                )

            chunks.append(
                VectorChunk(
                    id=f"daily-{date_iso}",
                    text=" ".join(parts),
                    metadata={
                        "source": "bank_statement",
                        "account": account,
                        "date": date_iso,
                        "type": "daily_summary",
                        "total_debited": float(total_out),
                        "total_credited": float(total_in),
                    },
                )
            )

        return chunks


class AccountSummaryChunkBuilder:
    """Single chunk describing the statement period."""

    def build(
        self,
        metadata: AccountMetadata,
        transactions: list[Transaction],
        *,
        raw_pages: list[dict[str, Any]] | None = None,
    ) -> list[VectorChunk]:
        debits = [t for t in transactions if t.type == "debit"]
        credits = [t for t in transactions if t.type == "credit"]
        total_debited = round(sum(abs(t.amount) for t in debits), 2)
        total_credited = round(sum(t.amount for t in credits), 2)

        date_from_human = metadata.date_from.strftime("%B %d, %Y")
        date_to_human = metadata.date_to.strftime("%B %d, %Y")

        text = (
            f"Bank statement for account {metadata.number} "
            f"held by {metadata.holder}, "
            f"covering {date_from_human} to {date_to_human}. "
            f"Opening balance: \u20ac{metadata.opening_balance:.2f}, "
            f"closing balance: \u20ac{metadata.closing_balance:.2f}. "
            f"{len(debits)} debit transaction(s) "
            f"totalling \u20ac{total_debited:.2f} and "
            f"{len(credits)} credit transaction(s) "
            f"totalling \u20ac{total_credited:.2f}."
        )

        return [
            VectorChunk(
                id=f"stmt-{metadata.date_from.isoformat()}-{metadata.date_to.isoformat()}",
                text=text,
                metadata={
                    "source": "bank_statement",
                    "account": metadata.number,
                    "date_from": metadata.date_from.isoformat(),
                    "date_to": metadata.date_to.isoformat(),
                    "type": "account_summary",
                },
            )
        ]


class RawPageChunkBuilder:
    """One chunk per raw PDF page."""

    def build(
        self,
        metadata: AccountMetadata,
        transactions: list[Transaction],
        *,
        raw_pages: list[dict[str, Any]] | None = None,
    ) -> list[VectorChunk]:
        if not raw_pages:
            return []

        account = metadata.number or ""
        return [
            VectorChunk(
                id=f"raw-page-{p['page']}",
                text=p["text"],
                metadata={
                    "source": "bank_statement",
                    "account": account,
                    "type": "raw_page",
                    "page": p["page"],
                },
            )
            for p in raw_pages
        ]
