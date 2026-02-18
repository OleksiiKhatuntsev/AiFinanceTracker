from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestHealth:
    def test_returns_ok_status(self):
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestNlqParse:
    def test_returns_mock_response(self):
        response = client.post("/nlq/parse", json={"question": "how much was spent on groceries in January?"})

        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "Groceries"
        assert data["date_from"] == "2026-01-01"
        assert data["date_to"] == "2026-01-31"
        assert data["aggregation"] == "sum"

    def test_response_has_all_fields(self):
        response = client.post("/nlq/parse", json={"question": "Any question"})

        data = response.json()
        assert set(data.keys()) == {"category", "date_from", "date_to", "aggregation"}

    def test_missing_question_returns_422(self):
        response = client.post("/nlq/parse", json={})

        assert response.status_code == 422

    def test_empty_question_is_accepted(self):
        response = client.post("/nlq/parse", json={"question": ""})

        assert response.status_code == 200

    def test_invalid_content_type_returns_422(self):
        response = client.post("/nlq/parse", content="not json")

        assert response.status_code == 422
