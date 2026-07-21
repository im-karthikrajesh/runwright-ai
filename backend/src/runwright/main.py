from fastapi import FastAPI

from runwright.api.router import api_router

app = FastAPI(
    title="Runwright API",
    description="AI-powered CI failure intelligence and reusable developer runbooks.",
    version="0.1.0",
)

app.include_router(api_router)