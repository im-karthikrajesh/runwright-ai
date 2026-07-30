from runwright.schemas.analysis import FailureCategory
from runwright.services.triage_engine import analyze_log


def test_analyze_log_classifies_python_import_failure() -> None:
    log_text = """
Running tests
ModuleNotFoundError: No module named 'runwright'
Error: Process completed with exit code 1
"""

    result = analyze_log(log_text)

    assert result.category == FailureCategory.DEPENDENCY
    assert result.confidence == 0.9
    assert result.reusable_runbook_candidate is True
    assert result.evidence[0].line_number == 3


def test_analyze_log_classifies_permission_failure() -> None:
    result = analyze_log("Permission denied while executing ./script.sh")

    assert result.category == FailureCategory.PERMISSION
    assert result.confidence == 0.85


def test_analyze_log_classifies_timeout_failure() -> None:
    result = analyze_log("Service health check timed out")

    assert result.category == FailureCategory.INFRASTRUCTURE
    assert result.confidence == 0.75


def test_analyze_log_returns_unknown_for_unrecognised_failure() -> None:
    result = analyze_log("Process exited unexpectedly")

    assert result.category == FailureCategory.UNKNOWN
    assert result.confidence == 0.3
    assert result.reusable_runbook_candidate is False


def test_analyze_log_redacts_secrets_from_evidence() -> None:
    result = analyze_log(
        "Error: request failed with token=super-secret-token"
    )

    assert "super-secret-token" not in result.evidence[0].text
    assert "[REDACTED_SECRET]" in result.evidence[0].text