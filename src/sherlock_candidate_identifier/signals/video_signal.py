"""Video signal based on camera state, face count, and webcam activity."""

from __future__ import annotations

from sherlock_candidate_identifier.models import EvidenceType, MeetingState, Participant, SignalResult


class VideoSignal:
    """Estimate candidate likelihood from webcam behavior."""

    signal_name = "video_signal"

    def evaluate(self, participant: Participant, state: MeetingState) -> SignalResult:
        del state
        score = 0.0
        explanations: list[str] = []

        if participant.camera_on:
            score += 0.45
            explanations.append("camera is on")
        else:
            score -= 0.15
            explanations.append("camera is off")

        if participant.face_count == 1:
            score += 0.35
            explanations.append("exactly one face detected")
        elif participant.face_count and participant.face_count > 1:
            score -= 0.25
            explanations.append("multiple faces detected")

        if participant.webcam_activity_score is not None:
            score += (participant.webcam_activity_score - 0.5) * 0.3
            explanations.append("webcam activity analyzed")

        return SignalResult(
            participant_id=participant.participant_id,
            signal_name=self.signal_name,
            evidence_type=EvidenceType.VIDEO,
            score=round(max(-1, min(1, score)), 4),
            confidence=0.65 if participant.camera_on or participant.face_count is not None else 0.35,
            explanation="Video evidence: " + ", ".join(explanations) + ".",
        )
