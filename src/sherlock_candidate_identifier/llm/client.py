"""Provider-only Gemini client with structured output and retries."""

import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel


class GeminiClient:
    """Small provider adapter containing no Sherlock domain logic."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gemini-2.5-flash",
        max_attempts: int = 3,
        retry_delay_seconds: float = 0.5,
    ) -> None:
        load_dotenv()
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        self.max_attempts = max(1, max_attempts)
        self.retry_delay_seconds = max(0.0, retry_delay_seconds)
        self._client: genai.Client | None = None

    def generate_structured(self, prompt: str, response_schema: type[BaseModel]) -> str:
        """Generate schema-constrained JSON, retrying provider failures."""

        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        if self._client is None:
            self._client = genai.Client(api_key=self.api_key)

        last_error: Exception | None = None
        for attempt in range(self.max_attempts):
            try:
                response = self._client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=response_schema,
                    ),
                )
                if not response.text:
                    raise ValueError("Gemini returned an empty response")
                return response.text
            except Exception as error:
                last_error = error
                if attempt + 1 < self.max_attempts:
                    time.sleep(self.retry_delay_seconds * (2**attempt))

        raise RuntimeError("Gemini request failed after retries") from last_error
