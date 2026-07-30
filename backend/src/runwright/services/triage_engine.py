from runwright.schemas.analysis import (
    AnalyzeLogResponse,
    EvidenceItem,
    FailureCategory,
)
from runwright.services.log_parser import extract_relevant_lines
from runwright.services.redactor import redact_secrets


def analyze_log(log_text: str) -> AnalyzeLogResponse:
    """Analyse a CI log using deterministic failure rules."""

    safe_log = redact_secrets(log_text)
    relevant_lines = extract_relevant_lines(safe_log)

    evidence = [
        EvidenceItem(line_number=line_number, text=text)
        for line_number, text in relevant_lines
    ]

    lowercase_log = safe_log.lower()

    if "modulenotfounderror" in lowercase_log or "importerror" in lowercase_log:
        return AnalyzeLogResponse(
            category=FailureCategory.DEPENDENCY,
            summary="The CI job failed because Python could not import a required module.",
            likely_root_cause=(
                "A dependency may be missing, or the project package may not have "
                "been installed before the tests ran."
            ),
            confidence=0.9,
            evidence=evidence,
            suggested_fix=(
                "Verify the dependency configuration and install the project package "
                "before running tests, for example with `python -m pip install -e .`."
            ),
            reusable_runbook_candidate=True,
        )

    if "permission denied" in lowercase_log:
        return AnalyzeLogResponse(
            category=FailureCategory.PERMISSION,
            summary="The CI job failed because an operation was not permitted.",
            likely_root_cause=(
                "The workflow may lack file permissions, executable permissions, "
                "or the required GitHub token permissions."
            ),
            confidence=0.85,
            evidence=evidence,
            suggested_fix=(
                "Check file permissions, executable flags, repository secrets, "
                "and the workflow's `permissions` configuration."
            ),
            reusable_runbook_candidate=True,
        )

    if "timed out" in lowercase_log:
        return AnalyzeLogResponse(
            category=FailureCategory.INFRASTRUCTURE,
            summary="The CI job failed after an operation exceeded its time limit.",
            likely_root_cause=(
                "A service, network request, test, or build step may have become "
                "unresponsive or taken longer than expected."
            ),
            confidence=0.75,
            evidence=evidence,
            suggested_fix=(
                "Inspect the timed-out step, check external service availability, "
                "and review whether the timeout or retry configuration is appropriate."
            ),
            reusable_runbook_candidate=True,
        )

    return AnalyzeLogResponse(
        category=FailureCategory.UNKNOWN,
        summary="The CI failure could not yet be classified.",
        likely_root_cause=(
            "The current rule-based analyser did not recognise a supported failure pattern."
        ),
        confidence=0.3,
        evidence=evidence,
        suggested_fix=(
            "Review the extracted evidence and add a new failure rule if this issue recurs."
        ),
        reusable_runbook_candidate=False,
    )