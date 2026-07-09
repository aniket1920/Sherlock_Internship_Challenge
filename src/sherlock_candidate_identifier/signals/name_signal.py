"""Name-based candidate signal using fuzzy matching."""

from __future__ import annotations

from sherlock_candidate_identifier.models import EvidenceType, MeetingState, Participant, SignalResult
from sherlock_candidate_identifier.utils import text_similarity


class NameSignal:
    """Compare display names against the expected candidate name."""

    signal_name = "name_signal"

    def evaluate(self, participant: Participant, state: MeetingState) -> SignalResult:
        candidate_name = state.metadata.candidate_name
        similarity = text_similarity(participant.display_name, candidate_name)
        if similarity >= 0.85:
            explanation = f"Display name strongly matches candidate name '{candidate_name}'."
        elif similarity >= 0.45:
            explanation = f"Display name partially matches candidate name '{candidate_name}'."
        else:
            explanation = "Display name does not match the expected candidate name."
        return SignalResult(
            participant_id=participant.participant_id,
            signal_name=self.signal_name,
            evidence_type=EvidenceType.NAME,
            score=round(similarity, 4),
            confidence=0.9 if candidate_name else 0.0,
            explanation=explanation,
        )
