from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from runwright.core.config import get_settings


def create_database_engine() -> Engine:
    """Create a SQLAlchemy engine from Runwright configuration."""

    settings = get_settings()

    if settings.database_url is None:
        raise RuntimeError("DATABASE_URL must be configured to use the database.")

    return create_engine(
        settings.database_url.get_secret_value(),
        pool_pre_ping=True,
    )


@lru_cache
def get_database_engine() -> Engine:
    """Return the shared application database engine."""

    return create_database_engine()


@lru_cache
def get_session_factory() -> sessionmaker[Session]:
    """Return the shared SQLAlchemy session factory."""

    return sessionmaker(
        bind=get_database_engine(),
        class_=Session,
        autoflush=False,
        expire_on_commit=False,
    )
