from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from runwright.db.base import Base
from runwright.db.repositories import (
    create_repository,
    get_or_create_repository,
    get_repository_by_full_name,
)
from runwright.models import Repository


def test_get_repository_by_full_name_returns_repository() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = Repository(full_name="im-karthikrajesh/runwright-ai")
        session.add(repository)
        session.commit()

        result = get_repository_by_full_name(
            session,
            "im-karthikrajesh/runwright-ai",
        )

        assert result is not None
        assert result.full_name == "im-karthikrajesh/runwright-ai"


def test_get_repository_by_full_name_returns_none_when_missing() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        result = get_repository_by_full_name(
            session,
            "missing/repository",
        )

        assert result is None


def test_create_repository_returns_repository_with_generated_id() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = create_repository(
            session,
            "im-karthikrajesh/runwright-ai",
        )

        assert repository.id is not None
        assert repository.full_name == "im-karthikrajesh/runwright-ai"


def test_create_repository_does_not_commit_transaction() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        create_repository(
            session,
            "im-karthikrajesh/runwright-ai",
        )

        session.rollback()

        result = get_repository_by_full_name(
            session,
            "im-karthikrajesh/runwright-ai",
        )

        assert result is None


def test_get_or_create_repository_reuses_existing_repository() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        existing = create_repository(
            session,
            "im-karthikrajesh/runwright-ai",
        )

        result = get_or_create_repository(
            session,
            "im-karthikrajesh/runwright-ai",
        )

        assert result.id == existing.id


def test_get_or_create_repository_creates_missing_repository() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        result = get_or_create_repository(
            session,
            "im-karthikrajesh/runwright-ai",
        )

        assert result.id is not None
        assert result.full_name == "im-karthikrajesh/runwright-ai"
