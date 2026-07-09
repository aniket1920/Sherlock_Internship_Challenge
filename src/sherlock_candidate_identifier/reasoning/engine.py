"""Orchestrates signals, explanations, and confidence fusion."""

from __future__ import annotations

from sherlock_candidate_identifier.confidence import ConfidenceEngine
from sherlock_candidate_identifier.explainability import ExplanationEngine
from sherlock_candidate_identifier.models import MeetingEvent, MeetingState, Prediction, SignalResult
from sherlock_candidate_identifier.signals import (
    BehaviorSignal,
    CandidateSignal,
    LLMSignal,
    MetadataSignal,
    NameSignal,
    TranscriptSignal,
    VideoSignal,
)


class CandidateEvidenceEngine:
    """Continuously identify the candidate from live meeting evidence."""

    def __init__(
        self,
        state: MeetingState,
        signals: list[CandidateSignal] | None = None,
        confidence_engine: ConfidenceEngine | None = None,
        explanation_engine: ExplanationEngine | None = None,
    ) -> None:
        self.state = state
        self.signals = signals or [
            NameSignal(),
            MetadataSignal(),
            TranscriptSignal(),
            BehaviorSignal(),
            VideoSignal(),
            LLMSignal(),
        ]
        self.confidence_engine = confidence_engine or ConfidenceEngine()
        self.explanation_engine = explanation_engine or ExplanationEngine()

    def ingest(self, event: MeetingEvent) -> Prediction:
        """Apply one event and return the latest prediction."""

        self.state.apply_event(event)
        return self.predict()

    def predict(self) -> Prediction:
        """Evaluate all signals and combine them into a prediction."""

        signal_results = self.evaluate_signals()
        top_participant_id = self._top_raw_participant(signal_results)
        explanation = self.explanation_engine.summarize(top_participant_id, signal_results)
        return self.confidence_engine.predict(self.state, signal_results, explanation)

    def evaluate_signals(self) -> list[SignalResult]:
        """Run every signal against every participant."""

        results: list[SignalResult] = []
        for participant in self.state.participants.values():
            for signal in self.signals:
                results.append(signal.evaluate(participant, self.state))
        return results

    @staticmethod
    def _top_raw_participant(signal_results: list[SignalResult]) -> str | None:
        totals: dict[str, float] = {}
        for result in signal_results:
            totals[result.participant_id] = totals.get(result.participant_id, 0) + result.score * result.confidence
        if not totals:
            return None
        return max(totals, key=totals.get)
