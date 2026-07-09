from pydantic import BaseModel

from sherlock_candidate_identifier.models import MeetingMetadata, MeetingState, Participant
from sherlock_candidate_identifier.signals import LLMSignal


class MockGeminiClient:
    def __init__(self, response: str) -> None:
        self.response = response
        self.call_count = 0

    def generate_structured(self, prompt: str, response_schema: type[BaseModel]) -> str:
        assert "Guest" in prompt
        assert response_schema.__name__ == "GeminiRoleResponse"
        self.call_count += 1
        return self.response


def test_llm_signal_maps_valid_gemini_response() -> None:
    client = MockGeminiClient(
        '{"role":"candidate","score":0.82,"confidence":0.91,'
        '"reason":"Answers describe personal projects.","evidence":["first-person ownership"]}'
    )
    state = MeetingState(
        meeting_id="test",
        metadata=MeetingMetadata(candidate_name="Nisha Rao"),
    )
    participant = Participant(
        participant_id="p1",
        display_name="Guest",
        transcript_text=["I implemented the service."],
    )

    result = LLMSignal(client=client).evaluate(participant, state)

    assert result.score == 0.82
    assert result.confidence == 0.91
    assert "candidate" in result.explanation


def test_llm_signal_caches_unchanged_transcript() -> None:
    client = MockGeminiClient(
        '{"role":"unknown","score":0,"confidence":0.2,"reason":"Limited data","evidence":[]}'
    )
    signal = LLMSignal(client=client)
    state = MeetingState(meeting_id="test", metadata=MeetingMetadata())
    participant = Participant(participant_id="p1", display_name="Guest", transcript_text=["Hello"])

    first = signal.evaluate(participant, state)
    second = signal.evaluate(participant, state)

    assert first == second
    assert client.call_count == 1


def test_llm_signal_fails_closed_on_invalid_response() -> None:
    client = MockGeminiClient('{"not":"the expected schema"}')
    state = MeetingState(meeting_id="test", metadata=MeetingMetadata())
    participant = Participant(participant_id="p1", display_name="Guest")

    result = LLMSignal(client=client).evaluate(participant, state)

    assert result.score == 0
    assert result.confidence == 0
    assert "unavailable" in result.explanation
