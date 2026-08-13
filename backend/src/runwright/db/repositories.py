from sqlalchemy import select
from sqlalchemy.orm import Session

from runwright.models import Repository


def get_repository_by_full_name(
    session: Session,
    full_name: str,
) -> Repository | None:
    """Return a repository matching its unique full name."""

    statement = select(Repository).where(Repository.full_name == full_name)

    return session.scalar(statement)


def create_repository(
        session: Session,
        full_name: str,
) -> Repository:
    """Create a repository and make its generated fields available."""

    repository = Repository(full_name=full_name)

    session.add(repository)
    session.flush()

    return repository


def get_or_create_repository(
    session: Session,
    full_name: str,
) -> Repository:
    """Return an existing repository or create it within the current transaction."""

    repository = get_repository_by_full_name(session, full_name)

    if repository is not None:
        return repository

    return create_repository(session, full_name)
