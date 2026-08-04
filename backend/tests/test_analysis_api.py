from fastapi.testclient import TestClient

from runwright.main import app

client = TestClient(app)


def test_analyze_ci_log_returns_structured_diagnosis() -> None:
    response = client.post(
        "/analysis/logs",
        json={
            "repository": "im-karthikrajesh/runwright-ai",
            "workflow_name": "Backend CI",
            "job_name": "Python 3.14",
            "log_text": (
                "Running tests\n"
                "ModuleNotFoundError: No module named 'runwright'\n"
                "Error: Process completed with exit code 1"
            ),
        },
    )

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["category"] == "dependency"
    assert response_body["confidence"] == 0.9
    assert response_body["reusable_runbook_candidate"] is True
    assert response_body["evidence"][0]["line_number"] == 2


def test_analyze_ci_log_rejects_empty_log() -> None:
    response = client.post(
        "/analysis/logs",
        json={
            "repository": "im-karthikrajesh/runwright-ai",
            "workflow_name": "Backend CI",
            "job_name": "Python 3.14",
            "log_text": "",
        },
    )

    assert response.status_code == 422