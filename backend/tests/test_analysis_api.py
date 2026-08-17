from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from runwright.db.base import Base
from runwright.db.dependencies import get_database_session
from runwright.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    session_factory = sessionmaker(
        bind=engine,
        class_=Session,
        autoflush=False,
        expire_on_commit=False,
    )

    def override_database_session() -> Generator[Session, None, None]:
        with session_factory() as session:
            yield session

    app.dependency_overrides[get_database_session] = override_database_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    engine.dispose()


def test_analyze_ci_log_returns_structured_diagnosis(
    client: TestClient,
) -> None:
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


def test_analyze_ci_log_rejects_empty_log(
    client: TestClient,
) -> None:
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
