from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():                # pytest automatically discovers functions whose names start with test_
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "project": "NovaDesk AI",
    }

def test_ask_rejects_blank_question():
    response = client.post(
        "/ask",
        json={"question": "   "},
    )

    assert response.status_code == 422

def test_ask_rejects_missing_question():
    response = client.post(
        "/ask",
        json={},
    )

    assert response.status_code == 422


# Note :: TestClient sends the request, assert checks the result, and pytest runs the test and reports whether it passed.