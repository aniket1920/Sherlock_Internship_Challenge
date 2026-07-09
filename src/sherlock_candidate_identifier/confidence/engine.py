"""Evidence-fusion confidence engine."""

from __future__ import annotations

import math
from collections import defaultdict

from sherlock_candidate_identifier.config import DEFAULT_SIGNAL_WEIGHTS, EngineSettings
from sherlock_candidate_identifier.models import (
    Evidence,
    EvidenceType,
    MeetingState,
    ParticipantPrediction,
    Prediction,
    PredictionStatus,
    SignalResult,
)


class ConfidenceEngine:
    """Combine independent signal results into calibrated participant probabilities."""

    def __init__(
        self,
        settings: EngineSettings | None = None,
        signal_weights: dict[EvidenceType, float] | None = None,
    ) -> None:
        self.settings = settings or EngineSettings()
        self.signal_weights = signal_weights or DEFAULT_SIGNAL_WEIGHTS

    def predict(self, state: MeetingState, signal_results: list[SignalResult], explanation: str) -> Prediction:
        """Create a ranked prediction for the current meeting state."""

        if not state.participants:
            return Prediction(
                meeting_id=state.meeting_id,
                status=PredictionStatus.NO_PARTICIPANTS,
                selected_participant_id=None,
                selected_display_name=None,
                confidence=0,
                participant_predictions=[],
                explanation="No participants are present.",
            )

        grouped = self._group_results(signal_results)
        combined_scores = {
            participant_id: self._combined_score(results)
            for participant_id, results in grouped.items()
        }
        probabilities = self._softmax(combined_scores)
        participant_predictions = [
            ParticipantPrediction(
                participant_id=participant_id,
                display_name=state.participants[participant_id].display_name,
                probability=round(probabilities[participant_id], 4),
                combined_score=round(combined_scores[participant_id], 4),
                evidence=[result.to_evidence() for result in grouped[participant_id]],
            )
            for participant_id in state.participants
        ]
        participant_predictions.sort(key=lambda item: item.probability, reverse=True)

        top = participant_predictions[0]
        runner_up_probability = participant_predictions[1].probability if len(participant_predictions) > 1 else 0
        margin = top.probability - runner_up_probability
        status = (
            PredictionStatus.IDENTIFIED
            if top.probability >= self.settings.identification_threshold and margin >= self.settings.minimum_margin
            else PredictionStatus.UNCERTAIN
        )

        return Prediction(
            meeting_id=state.meeting_id,
            status=status,
            selected_participant_id=top.participant_id if status == PredictionStatus.IDENTIFIED else None,
            selected_display_name=top.display_name if status == PredictionStatus.IDENTIFIED else None,
            confidence=top.probability,
            participant_predictions=participant_predictions,
            explanation=explanation,
        )

    def _combined_score(self, results: list[SignalResult]) -> float:
        total = 0.0
        for result in results:
            weight = self.signal_weights.get(result.evidence_type, 1.0)
            total += result.score * result.confidence * weight
        return total

    @staticmethod
    def _group_results(results: list[SignalResult]) -> dict[str, list[SignalResult]]:
        grouped: dict[str, list[SignalResult]] = defaultdict(list)
        for result in results:
            grouped[result.participant_id].append(result)
        return dict(grouped)

    @staticmethod
    def _softmax(scores: dict[str, float]) -> dict[str, float]:
        max_score = max(scores.values())
        exponentials = {participant_id: math.exp(score - max_score) for participant_id, score in scores.items()}
        total = sum(exponentials.values())
        return {participant_id: value / total for participant_id, value in exponentials.items()}
