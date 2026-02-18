from __future__ import annotations

from functools import lru_cache

from dotenv import load_dotenv
from fastapi import Depends, FastAPI

from schemas import NlqParseResponse, NlqRequest
from services.chains import build_chain
from services.nlq_parser import GeminiNlqParser, NlqParser

# TODO: подключить парсинг выписок когда pipeline будет интегрирован с API
# from pipeline import run

load_dotenv()

app = FastAPI(title="AI Finance Service")


@lru_cache(maxsize=1)
def get_nlq_parser() -> NlqParser:
    return GeminiNlqParser(build_chain())


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/nlq/parse", response_model=NlqParseResponse)
async def nlq_parse(request: NlqRequest, parser: NlqParser = Depends(get_nlq_parser)):
    return await parser.parse(request.question)
