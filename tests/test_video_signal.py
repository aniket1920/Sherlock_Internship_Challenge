from __future__ import annotations

from sherlock_candidate_identifier.models import MeetingMetadata, MeetingState, Participant
from sherlock_candidate_identifier.signals import VideoSignal


def test_video_signal_scores_camera_and_single_face() -> None:
    state = MeetingState(meeting_id="test", metadata=MeetingMetadata())
    participant = Participant(participant_id="p1", display_name="Guest", camera_on=True, face_count=1)

    result = VideoSignal().evaluate(participant, state)

    assert result.score > 0.5
