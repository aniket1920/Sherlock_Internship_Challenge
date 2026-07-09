"""Default signal weights for evidence fusion."""

from __future__ import annotations

from sherlock_candidate_identifier.models import EvidenceType

DEFAULT_SIGNAL_WEIGHTS: dict[EvidenceType, float] = {
    EvidenceType.NAME: 1.4,
    EvidenceType.METADATA: 1.6,
    EvidenceType.TRANSCRIPT: 1.0,
    EvidenceType.BEHAVIOR: 1.1,
    EvidenceType.VIDEO: 1.0,
    EvidenceType.LLM: 1.2,
}
