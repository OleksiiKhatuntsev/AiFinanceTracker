from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

# TODO: подключить парсинг выписок когда pipeline будет интегрирован с API
# from pipeline import run

app = FastAPI(title="AI Finance Service")


class NlqRequest(BaseModel):
    question: str


class NlqResponse(BaseModel):
    category: str
    date_from: str
    date_to: str
    aggregation: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/nlq/parse", response_model=NlqResponse)
def nlq_parse(request: NlqRequest):
    return NlqResponse(
        category="магазины",
        date_from="2026-01-01",
        date_to="2026-01-31",
        aggregation="sum",
    )
