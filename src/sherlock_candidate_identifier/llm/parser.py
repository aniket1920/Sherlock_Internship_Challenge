"""Validation helpers for Gemini JSON responses."""

import json
from typing import Any

from sherlock_candidate_identifier.llm.schemas import GeminiRoleResponse


def parse_gemini_response(payload: str | bytes | dict[str, Any]) -> GeminiRoleResponse:
    """Parse JSON and validate it against the expected Pydantic schema."""

    data = json.loads(payload) if isinstance(payload, (str, bytes, bytearray)) else payload
    return GeminiRoleResponse.model_validate(data)
