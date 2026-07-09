"""Meeting event models used by the simulator and evidence engine."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class EventType(StrEnum):
    """Supported live meeting event types."""

    PARTICIPANT_JOINED = "participant_joined"
    PARTICIPANT_LEFT = "participant_left"
    CAMERA_ON = "camera_on"
    CAMERA_OFF = "camera_off"
    DISPLAY_NAME_CHANGED = "display_name_changed"
    SPEAKING_STARTED = "speaking_started"
    SPEAKING_STOPPED = "speaking_stopped"
    SCREEN_SHARE_STARTED = "screen_share_started"
    SCREEN_SHARE_ENDED = "screen_share_ended"
    TRANSCRIPT_RECEIVED = "transcript_received"
    VIDEO_ANALYZED = "video_analyzed"
    AUDIO_ANALYZED = "audio_analyzed"


class MeetingEvent(BaseModel):
    """Generic meeting event for state updates and simulator replay."""

    timestamp_seconds: float = Field(ge=0)
    event_type: EventType
    participant_id: str
    display_name: str | None = None
    email: str | None = None
    duration_seconds: float = Field(default=0, ge=0)
    text: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class TranscriptEvent(BaseModel):
    """Speaker-attributed transcript event."""

    timestamp_seconds: float = Field(ge=0)
    participant_id: str
    text: str
    duration_seconds: float = Field(default=0, ge=0)


class VideoEvent(BaseModel):
    """Video-analysis event produced by a future webcam model."""

    timestamp_seconds: float = Field(ge=0)
    participant_id: str
    camera_on: bool
    face_count: int = Field(default=0, ge=0)
    webcam_activity_score: float = Field(default=0, ge=0, le=1)


class AudioEvent(BaseModel):
    """Audio-analysis event produced by a future speech or voice model."""

    timestamp_seconds: float = Field(ge=0)
    participant_id: str
    speaking: bool
    duration_seconds: float = Field(default=0, ge=0)
    voice_activity_score: float = Field(default=0, ge=0, le=1)
