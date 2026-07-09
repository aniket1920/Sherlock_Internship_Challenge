"""Metadata signal using candidate email, calendar, and interviewer names."""

from __future__ import annotations

from sherlock_candidate_identifier.models import EvidenceType, MeetingState, Participant, SignalResult
from sherlock_candidate_identifier.utils import email_local_part, normalize_text, text_similarity


class MetadataSignal:
    """Evaluate external metadata evidence for a participant."""

    signal_name = "metadata_signal"

    def evaluate(self, participant: Participant, state: MeetingState) -> SignalResult:
        metadata = state.metadata
        candidate_email = normalize_text(metadata.candidate_email)
        participant_email = normalize_text(participant.email)
        interviewer_similarity = max(
            [text_similarity(participant.display_name, name) for name in metadata.interviewer_names],
            default=0.0,
        )

        if candidate_email and participant_email and candidate_email == participant_email:
            score = 1.0
            confidence = 0.98
            explanation = "Participant email exactly matches the scheduled candidate email."
        elif interviewer_similarity >= 0.85:
            score = -1.0
            confidence = 0.95
            explanation = "Participant matches a known interviewer and should be excluded."
        else:
            local_name_score = text_similarity(email_local_part(participant.email), metadata.candidate_name)
            calendar_score = text_similarity(metadata.calendar_title, metadata.candidate_name)
            score = max(local_name_score, calendar_score * 0.25)
            confidence = 0.55 if score > 0 else 0.25
            explanation = "Metadata provides weak or indirect candidate evidence."

        return SignalResult(
            participant_id=participant.participant_id,
            signal_name=self.signal_name,
            evidence_type=EvidenceType.METADATA,
            score=round(score, 4),
            confidence=round(confidence, 4),
            explanation=explanation,
        )
