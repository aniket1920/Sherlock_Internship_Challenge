"""Structured response models for Gemini role reasoning."""

from pydantic import BaseModel, Field


class GeminiRoleResponse(BaseModel):
    """Validated participant-role assessment returned by Gemini."""

    role: str
    score: float = Field(ge=-1, le=1)
    confidence: float = Field(ge=0, le=1)
    reason: str
    evidence: list[str] = Field(default_factory=list)
