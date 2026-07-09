"""FastAPI application entry point."""

from fastapi import FastAPI

from sherlock_candidate_identifier.api.routers import router

app = FastAPI(
    title="Sherlock Candidate Identifier",
    description="HTTP wrapper for the existing candidate evidence pipeline.",
    version="0.1.0",
)
app.include_router(router)
