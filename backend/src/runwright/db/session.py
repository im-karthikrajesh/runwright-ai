from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from runwright.core.config import get_settings


def create_database_engine() -> Engine:
    settings = get_settings()

    if settings.database_url is None:
        raise RuntimeError("DATABASE_URL must be configured to use the database.")

    return create_engine(
        settings.database_url.get_secret_value(),
        pool_pre_ping=True,
    )


engine = create_database_engine()

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    expire_on_commit=False,
)
