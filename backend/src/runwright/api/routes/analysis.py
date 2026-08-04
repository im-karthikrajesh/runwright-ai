from fastapi import APIRouter

from runwright.schemas.analysis import AnalyzeLogRequest, AnalyzeLogResponse
from runwright.services.triage_engine import analyze_log

router = APIRouter()


@router.post("/analysis/logs", response_model=AnalyzeLogResponse)
def analyze_ci_log(payload: AnalyzeLogRequest) -> AnalyzeLogResponse:
    """Analyze a failed CI log and return a structured diagnosis."""

    return analyze_log(payload.log_text)