from __future__ import annotations

from sherlock_candidate_identifier.models import EvidenceType, MeetingMetadata, MeetingState, Participant, SignalResult
from sherlock_candidate_identifier.confidence import ConfidenceEngine


def test_confidence_engine_identifies_highest_evidence_participant() -> None:
    state = MeetingState(
        meeting_id="test",
        metadata=MeetingMetadata(),
        participants={
            "p1": Participant(participant_id="p1", display_name="Candidate"),
            "p2": Participant(participant_id="p2", display_name="Interviewer"),
        },
    )
    results = [
        SignalResult(
            participant_id="p1",
            signal_name="test",
            evidence_type=EvidenceType.METADATA,
            score=1,
            confidence=1,
            explanation="strong candidate evidence",
        ),
        SignalResult(
            participant_id="p2",
            signal_name="test",
            evidence_type=EvidenceType.METADATA,
            score=-1,
            confidence=1,
            explanation="known interviewer",
        ),
    ]

    prediction = ConfidenceEngine().predict(state, results, "summary")

    assert prediction.selected_participant_id == "p1"
