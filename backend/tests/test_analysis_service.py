from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from runwright.db.base import Base
from runwright.models import Repository
from runwright.schemas.analysis import AnalyzeLogRequest, FailureCategory
from runwright.services.analysis_service import analyze_ci_failure


def test_analyze_ci_failure_persists_repository_and_returns_diagnosis() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    payload = AnalyzeLogRequest(
        repository="im-karthikrajesh/runwright-ai",
        workflow_name="Backend CI",
        job_name="Python 3.14",
        log_text="ModuleNotFoundError: No module named 'runwright'",
    )

    with Session(engine) as session:
        result = analyze_ci_failure(session, payload)

        repository = session.scalar(
            select(Repository).where(
                Repository.full_name == "im-karthikrajesh/runwright-ai"
            )
        )

        assert repository is not None
        assert result.category == FailureCategory.DEPENDENCY
        assert result.confidence == 0.9