# AI Service — Bank Statement Parser

Parses ABN AMRO PDF bank statements into two outputs:

- **SQL output** — structured JSON with account metadata, summary, and transactions grouped by date
- **Vector output** — semantic text chunks for a vector database (account summary, daily summaries, per-transaction chunks, raw page text)

## Setup

```bash
conda env create -f environment.yml
conda activate family-finance
```

If the environment already exists, install the required packages manually:

```bash
conda run -n family-finance pip install pdfplumber pytest
```

## Quick start

### CLI

```bash
# Parse the bundled sample
python -m pipeline

# Parse any ABN AMRO PDF
python -m pipeline /path/to/statement.pdf
```

Output is JSON printed to stdout. Redirect to a file if needed:

```bash
python -m pipeline statement.pdf > result.json
```

### Python API

```python
from pathlib import Path
from pipeline import run

result = run(Path("samples/example_1.pdf"))

# result["sql"]    — account info, summary, transactions by date
# result["vector"] — {"chunks": [{"id": ..., "text": ..., "metadata": {...}}, ...]}
```

## Output structure

### `result["sql"]`

```json
{
  "account": {
    "holder": "Mr. O. Khatuntsev",
    "number": "12.80.93.935",
    "date_from": "2026-02-01",
    "date_to": "2026-02-11",
    "opening_balance": 889.59,
    "closing_balance": 231.88
  },
  "summary": {
    "total_debited": 857.71,
    "total_credited": 200.0,
    "debit_count": 29,
    "credit_count": 1
  },
  "transactions_by_date": {
    "2026-01-31": [
      {"description": "BEA, Apple Pay Albert Heijn ...", "amount": -23.05, "type": "debit"}
    ]
  }
}
```

### `result["vector"]`

Each chunk has an `id`, human-readable `text`, and a `metadata` dict:

| Chunk type | ID pattern | Count per statement |
|---|---|---|
| Account summary | `stmt-{from}-{to}` | 1 |
| Daily summary | `daily-{date}` | 1 per unique date |
| Transaction | `tx-{date}-{hash}` | 1 per transaction |
| Raw page | `raw-page-{n}` | 1 per PDF page |

## Customising the pipeline

### Using a different parser

Implement the `StatementParser` protocol and pass it to `run()`:

```python
from pathlib import Path
from parsers.base import StatementParser
from models import AccountMetadata, Transaction

class RabobankParser:
    def parse(self, pdf_path: Path) -> tuple[AccountMetadata, list[Transaction], list[dict]]:
        # your parsing logic here
        ...

result = run(Path("rabobank.pdf"), parser=RabobankParser())
```

### Using custom chunk builders

Implement the `ChunkBuilder` protocol to add new chunk types or replace existing ones:

```python
from chunkers.base import ChunkBuilder
from models import AccountMetadata, Transaction, VectorChunk

class MonthlySummaryChunkBuilder:
    def build(self, metadata, transactions, *, raw_pages=None) -> list[VectorChunk]:
        # your logic here
        ...

result = run(
    Path("statement.pdf"),
    chunk_builders=[
        AccountSummaryChunkBuilder(),
        DailySummaryChunkBuilder(),
        TransactionChunkBuilder(),
        MonthlySummaryChunkBuilder(),  # your custom builder
    ],
)
```

### Adding merchant patterns

Edit `parsers/merchant.py` and append to the `PATTERNS` list:

```python
PATTERNS: list[tuple[re.Pattern[str], int]] = [
    (re.compile(r"(?:BEA|eCom),\s*(?:Apple Pay|Betaalpas)\s+(.+?)(?:,PAS|\*)"), 1),
    (re.compile(r"/NAME/([^/]+)", re.IGNORECASE), 1),
    # add new patterns here:
    (re.compile(r"iDEAL\s+(.+?)(?:\s+\d)"), 1),
]
```

## Running tests

```bash
pytest tests/ -v
```

Tests cover: data models, European amount parsing, PDF metadata/transaction extraction, merchant classification, chunk building, and end-to-end pipeline with balance reconciliation.

## Project structure

```
ai-service/
├── models.py              # Dataclasses: Transaction, AccountMetadata, VectorChunk
├── pipeline.py            # Orchestration + CLI entry point
├── parsers/
│   ├── base.py            # StatementParser protocol
│   ├── abn_amro.py        # ABN AMRO PDF parsing
│   └── merchant.py        # Merchant name extraction (pattern registry)
├── chunkers/
│   ├── base.py            # ChunkBuilder protocol
│   └── transaction.py     # Transaction, daily, account summary, raw page builders
├── tests/
│   ├── conftest.py        # Shared fixtures
│   ├── test_models.py
│   ├── test_parsers.py
│   ├── test_merchant.py
│   ├── test_chunkers.py
│   └── test_pipeline.py
├── samples/
│   └── example_1.pdf
├── environment.yml
└── pytest.ini
```
