"""Prediction models returned by the confidence and reasoning engines."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

from sherlock_candidate_identifier.models.evidence import Evidence


class PredictionStatus(StrEnum):
    """Candidate-identification decision status."""

    NO_PARTICIPANTS = "no_participants"
    UNCERTAIN = "uncertain"
    IDENTIFIED = "identified"


class ParticipantPrediction(BaseModel):
    """Candidate probability and evidence for one participant."""

    participant_id: str
    display_name: str
    probability: float = Field(ge=0, le=1)
    combined_score: float
    evidence: list[Evidence]


class Prediction(BaseModel):
    """Full ranked prediction for the current meeting state."""

    meeting_id: str
    status: PredictionStatus
    selected_participant_id: str | None
    selected_display_name: str | None
    confidence: float = Field(ge=0, le=1)
    participant_predictions: list[ParticipantPrediction]
    explanation: str
