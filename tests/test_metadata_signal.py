from __future__ import annotations

from sherlock_candidate_identifier.models import MeetingMetadata, MeetingState, Participant
from sherlock_candidate_identifier.signals import MetadataSignal


def test_metadata_signal_prefers_candidate_email() -> None:
    state = MeetingState(
        meeting_id="test",
        metadata=MeetingMetadata(candidate_email="nisha.rao@example.com", interviewer_names=["Priya Shah"]),
    )
    participant = Participant(participant_id="p1", display_name="Laptop", email="nisha.rao@example.com")

    result = MetadataSignal().evaluate(participant, state)

    assert result.score == 1.0
    assert result.confidence > 0.9
