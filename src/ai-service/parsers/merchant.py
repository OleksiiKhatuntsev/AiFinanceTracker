from __future__ import annotations

import re

PATTERNS: list[tuple[re.Pattern[str], int]] = [
    (re.compile(r"(?:BEA|eCom),\s*(?:Apple Pay|Betaalpas)\s+(.+?)(?:,PAS|\*)"), 1),
    (re.compile(r"/NAME/([^/]+)", re.IGNORECASE), 1),
]


def classify_merchant(description: str) -> str:
    """Derive a short merchant name from the raw transaction description."""
    for pattern, group in PATTERNS:
        m = pattern.search(description)
        if m:
            return m.group(group).strip()
    return description[:60]
