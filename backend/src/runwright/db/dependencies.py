from collections.abc import Generator

from sqlalchemy.orm import Session

from runwright.db.session import SessionLocal


def get_database_session() -> Generator[Session, None, None]:
    """Provide a database session and always close it after use."""

    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()