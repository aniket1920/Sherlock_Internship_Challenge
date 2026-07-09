"""Common signal interface."""

from __future__ import annotations

from typing import Protocol

from sherlock_candidate_identifier.models import MeetingState, Participant, SignalResult


class CandidateSignal(Protocol):
    """Protocol implemented by all evidence-producing signals."""

    signal_name: str

    def evaluate(self, participant: Participant, state: MeetingState) -> SignalResult:
        """Evaluate one participant against the current meeting state."""
