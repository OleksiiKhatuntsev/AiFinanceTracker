from __future__ import annotations

import os
from functools import lru_cache

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from schemas import NlqParseResponse

_SYSTEM_PROMPT = """\
You are a financial assistant that parses natural language questions into structured search queries.
Today's date is {current_date}.

Classify the question into one of two search types:
- "structured": the question asks for specific transaction data answerable by filtering \
(by category, date range, merchant, or requires an aggregation like a total or count).
- "semantic": the question is broad, asks about patterns, habits, or requires deeper meaning \
beyond simple filtering.

If search_type is "structured", extract the following fields (set to null if not present):
- category: transaction category (e.g. "Shopping", "Restaurant", "Transport", "Web")
- date_from: start date in ISO format YYYY-MM-DD (resolve relative terms like "last month" \
using today's date)
- date_to: end date in ISO format YYYY-MM-DD
- merchant: specific merchant name
- aggregation: one of "sum", "count", "avg", "min", "max"

If search_type is "semantic", set structured_filter to null.
"""

_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", _SYSTEM_PROMPT),
        ("human", "{question}"),
    ]
)


@lru_cache(maxsize=5)
def build_chain():
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        google_api_key=os.environ.get("GOOGLE_API_KEY", ""),
        temperature=0,
    )
    return _prompt | llm.with_structured_output(NlqParseResponse)
