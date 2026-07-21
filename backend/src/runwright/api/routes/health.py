from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check() -> dict[str, str]:
    """Confirm that the Runwright API is running."""
    return {
        "status": "healthy",
        "service": "runwright-api",
        "version": "0.1.0",
    }