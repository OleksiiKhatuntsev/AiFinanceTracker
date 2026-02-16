from __future__ import annotations

import logging
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

import pdfplumber

from models import AccountMetadata, Transaction

logger = logging.getLogger(__name__)


def parse_european_amount(text: str | None) -> Decimal | None:
    """Convert European-format amount like '23,05' or '1.234,56' to Decimal."""
    if not text or not text.strip():
        return None
    cleaned = text.strip().replace(".", "").replace(",", ".")
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None


def _parse_date(text: str) -> datetime:
    """Parse a dd-mm-yyyy date string."""
    return datetime.strptime(text, "%d-%m-%Y")


def _extract_metadata(page_text: str) -> AccountMetadata:
    """Extract account metadata from the first page text."""
    holder_match = re.search(r"Account holder name\s+(.+?)(?:\n)", page_text)
    account_match = re.search(r"Personal Account\s+([\d.]+)", page_text)
    interval_match = re.search(
        r"Date interval\s+(\d{2}-\d{2}-\d{4})\s+until\s+(\d{2}-\d{2}-\d{4})",
        page_text,
    )
    opening_match = re.search(r"Balance \d{2}-\d{2}-\d{4}\s+€\s+([\d.,]+)", page_text)
    closing_matches = re.findall(r"Balance \d{2}-\d{2}-\d{4}\s+€\s+([\d.,]+)", page_text)

    if not all([holder_match, account_match, interval_match, opening_match]):
        logger.warning("Could not extract all metadata fields from first page")

    date_from = _parse_date(interval_match.group(1)).date() if interval_match else None
    date_to = _parse_date(interval_match.group(2)).date() if interval_match else None

    return AccountMetadata(
        holder=holder_match.group(1).strip() if holder_match else "",
        number=account_match.group(1) if account_match else "",
        date_from=date_from,
        date_to=date_to,
        opening_balance=parse_european_amount(opening_match.group(1)) if opening_match else Decimal(0),
        closing_balance=(
            parse_european_amount(closing_matches[1])
            if closing_matches and len(closing_matches) > 1
            else Decimal(0)
        ),
    )


def _extract_transactions(pdf: pdfplumber.PDF) -> list[Transaction]:
    """Extract all transactions from all pages."""
    transactions: list[Transaction] = []

    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            header_idx = None
            for i, row in enumerate(table):
                cells = [c.strip() if c else "" for c in row]
                if "Date" in cells and "Description" in cells:
                    header_idx = i
                    break

            if header_idx is None:
                continue

            header = [c.strip() if c else "" for c in table[header_idx]]
            date_col = header.index("Date")
            desc_col = header.index("Description")

            debit_col = next(
                (i for i, h in enumerate(header) if "debited" in h.lower()),
                None,
            )
            credit_col = next(
                (i for i, h in enumerate(header) if "credited" in h.lower()),
                None,
            )

            if debit_col is None or credit_col is None:
                logger.warning(
                    "Could not find debit/credit columns in header: %s", header
                )
                continue

            for row in table[header_idx + 1:]:
                cells = [c.strip() if c else "" for c in row]
                date_str = cells[date_col] if date_col < len(cells) else ""
                if not re.match(r"\d{2}-\d{2}-\d{4}", date_str):
                    continue

                description = cells[desc_col] if desc_col < len(cells) else ""
                debit_str = cells[debit_col] if debit_col < len(cells) else ""
                credit_str = cells[credit_col] if credit_col < len(cells) else ""

                debit_amount = parse_european_amount(debit_str)
                credit_amount = parse_european_amount(credit_str)

                if debit_amount is not None:
                    amount = -debit_amount
                    tx_type = "debit"
                elif credit_amount is not None:
                    amount = credit_amount
                    tx_type = "credit"
                else:
                    logger.debug("Skipping row with no amount: %s", cells)
                    continue

                description = " ".join(description.split())

                transactions.append(
                    Transaction(
                        date=_parse_date(date_str).date(),
                        description=description,
                        amount=amount,
                        type=tx_type,
                    )
                )

    return transactions


def _extract_raw_pages(pdf: pdfplumber.PDF) -> list[dict]:
    """Extract raw text from each PDF page with page number metadata."""
    pages = []
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ""
        pages.append({"page": i + 1, "text": text})
    return pages


class AbnAmroParser:
    """Parser for ABN AMRO PDF bank statements."""

    def parse(
        self, pdf_path: Path
    ) -> tuple[AccountMetadata, list[Transaction], list[dict]]:
        with pdfplumber.open(pdf_path) as pdf:
            metadata = _extract_metadata(pdf.pages[0].extract_text())
            transactions = _extract_transactions(pdf)
            raw_pages = _extract_raw_pages(pdf)
        return metadata, transactions, raw_pages
