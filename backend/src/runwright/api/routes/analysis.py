from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from runwright.db.dependencies import get_database_session
from runwright.schemas.analysis import AnalyzeLogRequest, AnalyzeLogResponse
from runwright.services.analysis_service import analyze_ci_failure

router = APIRouter()

DatabaseSession = Annotated[Session, Depends(get_database_session)]


@router.post("/analysis/logs", response_model=AnalyzeLogResponse)
def analyze_ci_log(
    payload: AnalyzeLogRequest,
    session: DatabaseSession,
) -> AnalyzeLogResponse:
    """Analyze a failed CI log and return a structured diagnosis."""

    return analyze_ci_failure(session, payload)
