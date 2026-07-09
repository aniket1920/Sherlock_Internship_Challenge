import json
from pathlib import Path

from fastapi.testclient import TestClient

from sherlock_candidate_identifier.api.main import app

client = TestClient(app)


def test_health() -> None:
    assert client.get("/health").json() == {"status": "ok"}


def test_predict_accepts_replay_json() -> None:
    payload = json.loads(Path("data/scenarios/basic_interview.json").read_text(encoding="utf-8"))

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    prediction = response.json()
    assert prediction["meeting_id"] == payload["meeting_id"]
    assert prediction["selected_participant_id"] == "p-candidate"
