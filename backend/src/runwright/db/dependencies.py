from collections.abc import Generator

from sqlalchemy.orm import Session

from runwright.db.session import get_session_factory


def get_database_session() -> Generator[Session, None, None]:
    """Provide a database session and always close it after use."""

    session_factory = get_session_factory()

    with session_factory() as session:
        yield session
