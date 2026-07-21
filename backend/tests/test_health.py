from fastapi.testclient import TestClient

from runwright.main import app

client = TestClient(app)

def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "runwright-api",
        "version": "0.1.0",
    }