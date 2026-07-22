from enum import StrEnum

from pydantic import BaseModel, Field


class FailureCategory(StrEnum):
    """High-level categories used to classify CI failures."""

    APPLICATION = "application"
    TEST = "test"
    DEPENDENCY = "dependency"
    CONFIGURATION = "configuration"
    PERMISSION = "permission"
    INFRASTRUCTURE = "infrastructure"
    FLAKY = "flaky"
    UNKNOWN = "unknown"


class AnalyzeLogRequest(BaseModel):
    """Information required to analyze a failed CI job."""

    repository: str = Field(
        min_length=1,
        examples=["im-karthikrajesh/runwright-ai"],
    )
    workflow_name: str = Field(
        min_length=1,
        examples=["Backend CI"],
    )
    job_name: str = Field(
        min_length=1,
        examples=["Python 3.14"],
    )
    log_text: str = Field(
        min_length=1,
        description="Raw log output from the failed CI job.",
    )


class EvidenceItem(BaseModel):
    """A relevant piece of evidence extracted from the CI log."""
    line_number: int | None = Field(default=None, ge=1)
    text: str = Field(min_length=1)


class AnalyzeLogResponse(BaseModel):
    """Structured diagnosis returned after analyzing a CI failure."""

    category: FailureCategory
    summary: str = Field(min_length=1)
    likely_root_cause: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: list[EvidenceItem]
    suggested_fix: str = Field(min_length=1)
    reusable_runbook_candidate: bool