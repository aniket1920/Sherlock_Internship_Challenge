"""Runtime settings for candidate identification."""

from __future__ import annotations

from pydantic import BaseModel, Field


class EngineSettings(BaseModel):
    """Decision thresholds and calibration settings."""

    identification_threshold: float = Field(default=0.62, ge=0, le=1)
    minimum_margin: float = Field(default=0.12, ge=0, le=1)
    candidate_join_window_seconds: float = Field(default=420, ge=0)
