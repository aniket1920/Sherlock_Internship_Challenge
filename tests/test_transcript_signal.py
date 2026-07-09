from __future__ import annotations

from sherlock_candidate_identifier.models import MeetingMetadata, MeetingState, Participant
from sherlock_candidate_identifier.signals import TranscriptSignal


def test_transcript_signal_detects_candidate_language() -> None:
    state = MeetingState(meeting_id="test", metadata=MeetingMetadata())
    participant = Participant(
        participant_id="p1",
        display_name="Guest",
        transcript_text=["I built the service and my project used streaming features."],
    )

    result = TranscriptSignal().evaluate(participant, state)

    assert result.score > 0
