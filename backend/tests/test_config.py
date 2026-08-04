from pathlib import Path

import pytest
from pydantic import ValidationError

from runwright.core.config import Settings

ENVIRONMENT_VARIABLES = (
    "ENVIRONMENT",
    "LLM_PROVIDER",
    "OPENROUTER_API_KEY",
    "OPENROUTER_MODEL",
)


def clear_runwright_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Remove Runwright settings variables for deterministic tests."""

    for variable_name in ENVIRONMENT_VARIABLES:
        monkeypatch.delenv(variable_name, raising=False)


def test_settings_use_safe_defaults(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    clear_runwright_environment(monkeypatch)
    monkeypatch.chdir(tmp_path)

    settings = Settings()

    assert settings.environment == "development"
    assert settings.llm_provider == "disabled"
    assert settings.openrouter_api_key is None
    assert settings.openrouter_model is None


def test_settings_load_openrouter_configuration(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    clear_runwright_environment(monkeypatch)
    monkeypatch.chdir(tmp_path)

    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("LLM_PROVIDER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-api-key")
    monkeypatch.setenv("OPENROUTER_MODEL", "openrouter/free")

    settings = Settings()

    assert settings.environment == "test"
    assert settings.llm_provider == "openrouter"
    assert settings.openrouter_api_key is not None
    assert settings.openrouter_api_key.get_secret_value() == "test-api-key"
    assert settings.openrouter_model == "openrouter/free"


def test_settings_reject_unknown_llm_provider(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    clear_runwright_environment(monkeypatch)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LLM_PROVIDER", "unsupported-provider")

    with pytest.raises(ValidationError):
        Settings()