"""FastAPI routes wrapping the existing replay and reasoning pipeline."""

from fastapi import APIRouter

from sherlock_candidate_identifier.api.schemas import HealthResponse, MeetingPayload
from sherlock_candidate_identifier.models import MeetingState, Prediction
from sherlock_candidate_identifier.reasoning import CandidateEvidenceEngine
from sherlock_candidate_identifier.simulator import MeetingReplay

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Report service availability."""

    return HealthResponse()


@router.post("/predict", response_model=Prediction)
def predict(meeting: MeetingPayload) -> Prediction:
    """Replay one meeting payload and return its final existing prediction."""

    replay = MeetingReplay(meeting)
    state = MeetingState(meeting_id=meeting.meeting_id, metadata=meeting.metadata)
    engine = CandidateEvidenceEngine(state)
    prediction = engine.predict()
    for event in replay.events():
        prediction = engine.ingest(event)
    return prediction
