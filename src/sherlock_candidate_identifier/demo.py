from __future__ import annotations

from pathlib import Path

from sherlock_candidate_identifier.simulator import MeetingReplay


def main() -> None:
    scenario_path = Path("data/scenarios/basic_interview.json")
    replay = MeetingReplay.from_json(scenario_path)
    timeline = replay.run()
    print(timeline[-1])
