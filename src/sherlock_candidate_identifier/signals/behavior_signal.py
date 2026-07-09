"""Behavior signal based on speaking duration, frequency, and response patterns."""

from __future__ import annotations

from sherlock_candidate_identifier.models import EvidenceType, MeetingState, Participant, SignalResult


class BehaviorSignal:
    """Estimate candidate likelihood from conversational behavior."""

    signal_name = "behavior_signal"

    def evaluate(self, participant: Participant, state: MeetingState) -> SignalResult:
        total_speaking = sum(p.speaking_duration_seconds for p in state.participants.values())
        if total_speaking <= 0:
            return SignalResult(
                participant_id=participant.participant_id,
                signal_name=self.signal_name,
                evidence_type=EvidenceType.BEHAVIOR,
                score=0,
                confidence=0,
                explanation="No speaking behavior has been observed yet.",
            )

        speaking_share = participant.speaking_duration_seconds / total_speaking
        turn_count = participant.speaking_turn_count + participant.transcript_turn_count
        if 0.18 <= speaking_share <= 0.78 and turn_count > 0:
            score = min(1.0, speaking_share * 1.4)
            explanation = "Speaking share and turn count look candidate-like."
        elif speaking_share > 0.88:
            score = -0.45
            explanation = "Participant dominates the conversation, which can be interviewer-like."
        else:
            score = -0.2
            explanation = "Participant has limited speaking activity so far."

        return SignalResult(
            participant_id=participant.participant_id,
            signal_name=self.signal_name,
            evidence_type=EvidenceType.BEHAVIOR,
            score=round(score, 4),
            confidence=0.75,
            explanation=explanation,
        )
