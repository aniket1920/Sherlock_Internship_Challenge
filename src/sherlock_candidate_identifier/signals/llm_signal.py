"""Gemini-powered participant-role reasoning signal."""

from __future__ import annotations

import hashlib
from typing import Protocol

from pydantic import BaseModel

from sherlock_candidate_identifier.llm import (
    GeminiClient,
    GeminiRoleResponse,
    build_participant_prompt,
    parse_gemini_response,
)
from sherlock_candidate_identifier.models import EvidenceType, MeetingState, Participant, SignalResult


class StructuredLLMClient(Protocol):
    """Provider contract used to inject a mocked client in tests."""

    def generate_structured(self, prompt: str, response_schema: type[BaseModel]) -> str: ...


class LLMSignal:
    """Use Gemini to assess one participant while preserving the signal contract."""

    signal_name = "llm_signal"

    def __init__(self, client: StructuredLLMClient | None = None) -> None:
        self.client = client or GeminiClient()
        self._cache: dict[tuple[str, str], SignalResult] = {}

    def evaluate(self, participant: Participant, state: MeetingState) -> SignalResult:
        transcript_hash = hashlib.sha256(
            "\n".join(participant.transcript_text).encode("utf-8")
        ).hexdigest()
        cache_key = (participant.participant_id, transcript_hash)
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            prompt = build_participant_prompt(participant, state)
            raw_response = self.client.generate_structured(prompt, GeminiRoleResponse)
            assessment = parse_gemini_response(raw_response)
            evidence = "; ".join(assessment.evidence)
            explanation = f"Gemini classified role as {assessment.role}: {assessment.reason}"
            if evidence:
                explanation = f"{explanation} Evidence: {evidence}"
            result = SignalResult(
                participant_id=participant.participant_id,
                signal_name=self.signal_name,
                evidence_type=EvidenceType.LLM,
                score=assessment.score,
                confidence=assessment.confidence,
                explanation=explanation,
            )
        except Exception as error:
            result = SignalResult(
                participant_id=participant.participant_id,
                signal_name=self.signal_name,
                evidence_type=EvidenceType.LLM,
                score=0,
                confidence=0,
                explanation=f"Gemini signal unavailable: {type(error).__name__}: {error}",
            )

        self._cache[cache_key] = result
        return result
