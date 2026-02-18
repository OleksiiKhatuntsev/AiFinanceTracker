from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from main import app, get_nlq_parser
from schemas import NlqParseResponse, StructuredFilter

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    yield
    app.dependency_overrides.clear()


def _make_parser(response: NlqParseResponse) -> MagicMock:
    mock_parser = MagicMock()
    mock_parser.parse = AsyncMock(return_value=response)
    return mock_parser


class TestHealth:
    def test_returns_ok_status(self):
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestNlqParse:
    def test_structured_query_returns_structured_filter(self):
        expected = NlqParseResponse(
            search_type="structured",
            structured_filter=StructuredFilter(
                category="Groceries",
                date_from="2026-01-01",
                date_to="2026-01-31",
                aggregation="sum",
            ),
        )
        app.dependency_overrides[get_nlq_parser] = lambda: _make_parser(expected)

        response = client.post(
            "/nlq/parse",
            json={"question": "How much did I spend on groceries in January?"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["search_type"] == "structured"
        assert data["structured_filter"]["category"] == "Groceries"
        assert data["structured_filter"]["date_from"] == "2026-01-01"
        assert data["structured_filter"]["date_to"] == "2026-01-31"
        assert data["structured_filter"]["aggregation"] == "sum"
        assert data["structured_filter"]["merchant"] is None

    def test_semantic_query_returns_no_filter(self):
        expected = NlqParseResponse(search_type="semantic", structured_filter=None)
        app.dependency_overrides[get_nlq_parser] = lambda: _make_parser(expected)

        response = client.post(
            "/nlq/parse",
            json={"question": "What are my spending habits?"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["search_type"] == "semantic"
        assert data["structured_filter"] is None

    def test_structured_query_with_merchant_filter(self):
        expected = NlqParseResponse(
            search_type="structured",
            structured_filter=StructuredFilter(merchant="Netflix", aggregation="sum"),
        )
        app.dependency_overrides[get_nlq_parser] = lambda: _make_parser(expected)

        response = client.post(
            "/nlq/parse",
            json={"question": "How much did I pay Netflix this year?"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["structured_filter"]["merchant"] == "Netflix"
        assert data["structured_filter"]["aggregation"] == "sum"

    def test_response_has_required_fields(self):
        expected = NlqParseResponse(search_type="semantic")
        app.dependency_overrides[get_nlq_parser] = lambda: _make_parser(expected)

        response = client.post("/nlq/parse", json={"question": "Any question"})

        data = response.json()
        assert "search_type" in data
        assert "structured_filter" in data

    def test_parser_receives_the_question(self):
        mock_parser = _make_parser(NlqParseResponse(search_type="semantic"))
        app.dependency_overrides[get_nlq_parser] = lambda: mock_parser

        client.post("/nlq/parse", json={"question": "test question"})

        mock_parser.parse.assert_called_once_with("test question")

    def test_missing_question_returns_422(self):
        app.dependency_overrides[get_nlq_parser] = lambda: _make_parser(
            NlqParseResponse(search_type="semantic")
        )

        response = client.post("/nlq/parse", json={})

        assert response.status_code == 422

    def test_empty_question_is_accepted(self):
        expected = NlqParseResponse(search_type="semantic")
        app.dependency_overrides[get_nlq_parser] = lambda: _make_parser(expected)

        response = client.post("/nlq/parse", json={"question": ""})

        assert response.status_code == 200

    def test_invalid_content_type_returns_422(self):
        response = client.post("/nlq/parse", content="not json")

        assert response.status_code == 422
