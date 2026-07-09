"""Load and replay meetings from JSON scenario files."""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

from sherlock_candidate_identifier.models import Meeting, MeetingEvent, MeetingState
from sherlock_candidate_identifier.reasoning import CandidateEvidenceEngine


class MeetingReplay:
    """Replay a meeting fixture into the candidate evidence engine."""

    def __init__(self, meeting: Meeting):
        self.meeting = meeting

    @classmethod
    def from_json(cls, path: str | Path) -> "MeetingReplay":
        """Load a replayable meeting from JSON."""

        with Path(path).open("r", encoding="utf-8") as file:
            payload = json.load(file)
        return cls(Meeting.model_validate(payload))

    def events(self) -> Iterator[MeetingEvent]:
        """Yield events in timestamp order."""

        yield from sorted(self.meeting.events, key=lambda event: event.timestamp_seconds)

    def run(self) -> list[dict[str, object]]:
        """Replay all events and return a prediction timeline."""

        state = MeetingState(meeting_id=self.meeting.meeting_id, metadata=self.meeting.metadata)
        engine = CandidateEvidenceEngine(state)
        timeline: list[dict[str, object]] = []
        for event in self.events():
            prediction = engine.ingest(event)
            timeline.append(
                {
                    "timestamp_seconds": event.timestamp_seconds,
                    "event_type": event.event_type.value,
                    "participant_id": event.participant_id,
                    "status": prediction.status.value,
                    "selected_participant_id": prediction.selected_participant_id,
                    "confidence": prediction.confidence,
                    "explanation": prediction.explanation,
                }
            )
        return timeline
