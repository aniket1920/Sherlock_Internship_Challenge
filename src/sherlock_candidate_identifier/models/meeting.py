"""Meeting, participant, metadata, and mutable meeting-state models."""

from __future__ import annotations

from pydantic import BaseModel, Field

from sherlock_candidate_identifier.models.events import EventType, MeetingEvent


class Participant(BaseModel):
    """Current known state for a participant."""

    participant_id: str
    display_name: str
    email: str | None = None
    joined_at_seconds: float | None = None
    left_at_seconds: float | None = None
    camera_on: bool = False
    screen_sharing: bool = False
    speaking_duration_seconds: float = 0
    speaking_turn_count: int = 0
    transcript_turn_count: int = 0
    face_count: int | None = None
    webcam_activity_score: float | None = None
    transcript_text: list[str] = Field(default_factory=list)


class MeetingMetadata(BaseModel):
    """External metadata available before or during an interview."""

    candidate_name: str | None = None
    candidate_email: str | None = None
    calendar_title: str | None = None
    interview_schedule_start: str | None = None
    interviewer_names: list[str] = Field(default_factory=list)
    interviewer_emails: list[str] = Field(default_factory=list)


class Meeting(BaseModel):
    """Replayable meeting fixture loaded from JSON."""

    meeting_id: str
    metadata: MeetingMetadata
    events: list[MeetingEvent]
    expected_candidate_participant_id: str | None = None


class MeetingState(BaseModel):
    """Mutable aggregate state updated by live meeting events."""

    meeting_id: str
    metadata: MeetingMetadata
    participants: dict[str, Participant] = Field(default_factory=dict)
    current_time_seconds: float = 0

    def apply_event(self, event: MeetingEvent) -> None:
        """Update participant state from one event."""

        self.current_time_seconds = max(self.current_time_seconds, event.timestamp_seconds)
        participant = self._ensure_participant(event)

        if event.display_name:
            participant.display_name = event.display_name
        if event.email:
            participant.email = event.email

        if event.event_type == EventType.PARTICIPANT_JOINED and participant.joined_at_seconds is None:
            participant.joined_at_seconds = event.timestamp_seconds
        elif event.event_type == EventType.PARTICIPANT_LEFT:
            participant.left_at_seconds = event.timestamp_seconds
        elif event.event_type == EventType.CAMERA_ON:
            participant.camera_on = True
        elif event.event_type == EventType.CAMERA_OFF:
            participant.camera_on = False
        elif event.event_type == EventType.SCREEN_SHARE_STARTED:
            participant.screen_sharing = True
        elif event.event_type == EventType.SCREEN_SHARE_ENDED:
            participant.screen_sharing = False
        elif event.event_type == EventType.SPEAKING_STARTED:
            participant.speaking_turn_count += 1
        elif event.event_type == EventType.SPEAKING_STOPPED:
            participant.speaking_duration_seconds += event.duration_seconds
        elif event.event_type == EventType.TRANSCRIPT_RECEIVED:
            participant.transcript_turn_count += 1
            participant.speaking_duration_seconds += event.duration_seconds
            if event.text:
                participant.transcript_text.append(event.text)
        elif event.event_type == EventType.VIDEO_ANALYZED:
            participant.face_count = event.payload.get("face_count")
            participant.webcam_activity_score = event.payload.get("webcam_activity_score")

    def _ensure_participant(self, event: MeetingEvent) -> Participant:
        if event.participant_id not in self.participants:
            self.participants[event.participant_id] = Participant(
                participant_id=event.participant_id,
                display_name=event.display_name or event.participant_id,
                email=event.email,
                joined_at_seconds=event.timestamp_seconds
                if event.event_type == EventType.PARTICIPANT_JOINED
                else None,
            )
        return self.participants[event.participant_id]
