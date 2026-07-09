from __future__ import annotations

from sherlock_candidate_identifier.models import MeetingMetadata, MeetingState, Participant
from sherlock_candidate_identifier.signals import BehaviorSignal


def test_behavior_signal_uses_speaking_share() -> None:
    state = MeetingState(
        meeting_id="test",
        metadata=MeetingMetadata(),
        participants={
            "candidate": Participant(
                participant_id="candidate",
                display_name="Candidate",
                speaking_duration_seconds=60,
                speaking_turn_count=3,
            ),
            "interviewer": Participant(participant_id="interviewer", display_name="Interviewer", speaking_duration_seconds=40),
        },
    )

    result = BehaviorSignal().evaluate(state.participants["candidate"], state)

    assert result.score > 0
    assert result.confidence > 0
