from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration loaded from environment variables or a local .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: Literal["development", "test", "production"] = "development"

    llm_provider: Literal["disabled", "openrouter"] = "disabled"
    openrouter_api_key: SecretStr | None = None
    openrouter_model: str | None = None


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings."""

    return Settings()