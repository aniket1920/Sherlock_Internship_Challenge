"""Explanation engine for candidate predictions."""

from __future__ import annotations

from sherlock_candidate_identifier.models import SignalResult


class ExplanationEngine:
    """Build concise explanations from signal outputs."""

    def summarize(self, top_participant_id: str | None, signal_results: list[SignalResult]) -> str:
        """Explain the strongest positive evidence for a participant."""

        if top_participant_id is None:
            return "No participant can be selected yet."

        participant_results = [result for result in signal_results if result.participant_id == top_participant_id]
        participant_results.sort(key=lambda item: item.score * item.confidence, reverse=True)
        positive = [result for result in participant_results if result.score > 0][:3]
        if not positive:
            return "Top participant has no strong positive evidence yet."
        reasons = "; ".join(result.explanation for result in positive)
        return f"Top evidence for {top_participant_id}: {reasons}"
