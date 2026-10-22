# ---------- The automated test file ----------
# Purpose: This file checks whether our API behaves as expected without requiring us to test everything manually.

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

# this is the healthcheck point which cheaks weather api is available or not

def test_health_check():                # pytest automatically discovers functions whose names start with test_
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "project": "NovaDesk AI",
    }

# it Accepts a question and sends it to the RAG pipeline end point

def test_ask_rejects_blank_question():   # blank question condition / it checks whether the API correctly rejects the blank question
    response = client.post(
        "/ask",
        json={"question": "   "},
    )

    assert response.status_code == 422

def test_ask_rejects_missing_question():   # blank missing/empty question condition / it checks whether the API correctly rejects the missing.empty question
    response = client.post(
        "/ask",
        json={},
    )

    assert response.status_code == 422

# it's a mock, a temporary substitute that returns a predictable answer

def test_ask_returns_answer(monkeypatch):
    question = "How many casual leave days do employees get?"
    expected_answer = "Employees receive 12 casual leave days per year."

    def fake_ask(user_question: str) -> str:
        assert user_question == question
        return expected_answer

    class FakeRAGPipeline:
        def ask(self, user_question: str) -> str:
            return fake_ask(user_question)

    monkeypatch.setattr(
    "src.api.main.get_rag_pipeline",
    lambda: FakeRAGPipeline(),
)

    response = client.post(
        "/ask",
        json={"question": question},
    )

    assert response.status_code == 200
    assert response.json() == {
        "question": question,
        "answer": expected_answer,
    }

def test_ask_handles_unexpected_error(monkeypatch):
    class FakeRAGPipeline:
        def ask(self, user_question: str) -> str:
            raise RuntimeError("Intentional test failure")

    monkeypatch.setattr(
        "src.api.main.get_rag_pipeline",
        lambda: FakeRAGPipeline(),
    )

    response = client.post(
        "/ask",
        json={"question": "How many casual leave days do employees get?"},
    )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "An internal error occurred while processing your question."
    }


# Note :: TestClient sends the request, assert checks the result, and pytest runs the test and reports whether it passed.
