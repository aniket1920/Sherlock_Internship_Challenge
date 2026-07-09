"""HTTP request and response support schemas."""

from typing import Literal

from pydantic import BaseModel

from sherlock_candidate_identifier.models import Meeting

MeetingPayload = Meeting


class HealthResponse(BaseModel):
    """Health-check response."""

    status: Literal["ok"] = "ok"
