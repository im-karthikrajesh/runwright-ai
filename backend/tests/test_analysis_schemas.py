import pytest
from pydantic import ValidationError

from runwright.schemas.analysis import (
    AnalyzeLogRequest,
    AnalyzeLogResponse,
    EvidenceItem,
    FailureCategory,
)


def test_analyze_log_request_accepts_valid_data() -> None:
    request = AnalyzeLogRequest(
        repository="im-karthikrajesh/runwright-ai",
        workflow_name="Backend CI",
        job_name="Python 3.14",
        log_text="ModuleNotFoundError: No module named 'runwright'",
    )

    assert request.repository == "im-karthikrajesh/runwright-ai"
    assert request.workflow_name == "Backend CI"
    assert request.job_name == "Python 3.14"


def test_analyze_log_request_rejects_empty_log() -> None:
    with pytest.raises(ValidationError):
        AnalyzeLogRequest(
            repository="im-karthikrajesh/runwright-ai",
            workflow_name="Backend CI",
            job_name="Python 3.14",
            log_text="",
        )


def test_analyze_log_response_rejects_invalid_confidence() -> None:
    with pytest.raises(ValidationError):
        AnalyzeLogResponse(
            category=FailureCategory.APPLICATION,
            summary="The application failed during import.",
            likely_root_cause="A required Python module was unavailable.",
            confidence=1.5,
            evidence=[
                EvidenceItem(
                    line_number=10,
                    text="ModuleNotFoundError: No module named 'runwright'",
                )
            ],
            suggested_fix="Install the package before running the tests.",
            reusable_runbook_candidate=True,
        )