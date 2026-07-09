from __future__ import annotations

from sherlock_candidate_identifier.models import MeetingMetadata, MeetingState, Participant
from sherlock_candidate_identifier.signals import NameSignal


def test_name_signal_scores_close_display_name() -> None:
    state = MeetingState(
        meeting_id="test",
        metadata=MeetingMetadata(candidate_name="Nisha Rao"),
        participants={},
    )
    participant = Participant(participant_id="p1", display_name="Nisha R")

    result = NameSignal().evaluate(participant, state)

    assert result.score > 0.7
    assert result.confidence == 0.9
