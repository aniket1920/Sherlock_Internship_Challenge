from __future__ import annotations

from pathlib import Path

from sherlock_candidate_identifier.simulator import MeetingReplay


def test_meeting_replay_loads_and_runs_sample_scenario() -> None:
    replay = MeetingReplay.from_json(Path("data/scenarios/basic_interview.json"))
    timeline = replay.run()

    assert timeline
    assert timeline[-1]["selected_participant_id"] == replay.meeting.expected_candidate_participant_id
