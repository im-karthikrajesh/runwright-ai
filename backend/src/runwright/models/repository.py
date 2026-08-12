from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from runwright.db.base import Base


class Repository(Base):
    """A source-code repository known to Runwright."""

    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)