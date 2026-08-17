from sqlalchemy.orm import Session

from runwright.db.repositories import get_or_create_repository
from runwright.schemas.analysis import AnalyzeLogRequest, AnalyzeLogResponse
from runwright.services.triage_engine import analyze_log


def analyze_ci_failure(
    session: Session,
    payload: AnalyzeLogRequest,
) -> AnalyzeLogResponse:
    """Analyze a CI failure and persist its repository context."""

    get_or_create_repository(session, payload.repository)

    result = analyze_log(payload.log_text)

    session.commit()

    return result