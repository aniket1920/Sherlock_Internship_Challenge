"""Transcript signal with deterministic role-reasoning placeholders."""

from __future__ import annotations

from sherlock_candidate_identifier.models import EvidenceType, MeetingState, Participant, SignalResult
from sherlock_candidate_identifier.utils import normalize_text


class TranscriptSignal:
    """Infer participant role from speaker-attributed transcript content."""

    signal_name = "transcript_signal"
    _candidate_phrases = ("i built", "my project", "my experience", "i worked", "i implemented")
    _interviewer_phrases = ("tell me about", "can you explain", "next question", "we are hiring")

    def evaluate(self, participant: Participant, state: MeetingState) -> SignalResult:
        del state
        text = normalize_text(" ".join(participant.transcript_text))
        if not text:
            score = 0.0
            confidence = 0.0
            explanation = "No transcript is available for this participant yet."
        else:
            candidate_hits = sum(phrase.replace(" ", "") in text.replace(" ", "") for phrase in self._candidate_phrases)
            interviewer_hits = sum(phrase.replace(" ", "") in text.replace(" ", "") for phrase in self._interviewer_phrases)
            score = max(-1.0, min(1.0, (candidate_hits - interviewer_hits) * 0.35))
            confidence = min(0.85, 0.35 + 0.15 * (candidate_hits + interviewer_hits))
            explanation = "Transcript contains candidate-like responses." if score > 0 else "Transcript does not yet add strong candidate evidence."

        return SignalResult(
            participant_id=participant.participant_id,
            signal_name=self.signal_name,
            evidence_type=EvidenceType.TRANSCRIPT,
            score=round(score, 4),
            confidence=round(confidence, 4),
            explanation=explanation,
        )
