"""Evidence and signal result models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class EvidenceType(StrEnum):
    """Signal families that can contribute evidence."""

    NAME = "name"
    METADATA = "metadata"
    TRANSCRIPT = "transcript"
    BEHAVIOR = "behavior"
    VIDEO = "video"
    LLM = "llm"


class Evidence(BaseModel):
    """Single explainable evidence item."""

    evidence_type: EvidenceType
    signal_name: str
    score: float = Field(ge=-1, le=1)
    confidence: float = Field(ge=0, le=1)
    explanation: str


class SignalResult(BaseModel):
    """Output contract for every signal module."""

    participant_id: str
    signal_name: str
    evidence_type: EvidenceType
    score: float = Field(ge=-1, le=1)
    confidence: float = Field(ge=0, le=1)
    explanation: str

    def to_evidence(self) -> Evidence:
        """Convert a signal result into a generic evidence item."""

        return Evidence(
            evidence_type=self.evidence_type,
            signal_name=self.signal_name,
            score=self.score,
            confidence=self.confidence,
            explanation=self.explanation,
        )
