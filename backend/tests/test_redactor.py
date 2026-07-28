from runwright.services.redactor import redact_secrets


def test_redact_secrets_hides_named_credentials() -> None:
    log_text = """
API_KEY=secret-value
password: secret
token=my-token-value
"""

    result = redact_secrets(log_text)

    assert "secret-value" not in result
    assert "secret" not in result
    assert "my-token-value" not in result
    assert result.count("[REDACTED_SECRET]") == 3


def test_redact_secrets_hides_github_tokens() -> None:
    log_text = """
Using token ghp_abcdefghijklmnopqrstuvwxyz123456
Using fine-grained token github_pat_abcdefghijklmnopqrstuvwxyz123456
"""

    result = redact_secrets(log_text)

    assert "ghp_" not in result
    assert "github_pat_" not in result
    assert result.count("[REDACTED_SECRET]") == 2


def test_redact_secrets_hides_bearer_tokens() -> None:
    log_text = "Authorization: Bearer abc.def.ghi"

    result = redact_secrets(log_text)

    assert "abc.def.ghi" not in result
    assert "[REDACTED_SECRET]" in result


def test_redact_secrets_preserves_normal_text() -> None:
    log_text = "Running tests\nAll tests passed"

    assert redact_secrets(log_text) == log_text