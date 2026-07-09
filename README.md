# Sherlock Candidate Identifier

Production-oriented Python project skeleton for the Sherlock Internship Challenge.

The goal is to continuously identify the interview candidate in an online meeting by combining many weak evidence sources. This is not a single-model project. It is an evidence engine that scores each participant, estimates confidence, and explains every prediction.

## Architecture

Core flow:

1. Meeting events update `MeetingState`.
2. Independent signals evaluate each participant.
3. Each signal returns `score`, `confidence`, and `explanation`.
4. `ConfidenceEngine` fuses evidence into probabilities.
5. `ExplanationEngine` summarizes why the current top participant was selected.

See [docs/architecture.md](docs/architecture.md).

## Folder Structure

```text
src/sherlock_candidate_identifier/
  config/          thresholds and signal weights
  models/          Pydantic domain models
  simulator/       JSON meeting replay
  signals/         name, metadata, transcript, behavior, video, LLM signals
  reasoning/       pipeline orchestration
  confidence/      evidence fusion
  explainability/  human-readable explanations
  utils/           shared helpers
tests/             pytest skeletons for every signal and engine
data/
  meetings/
  transcripts/
  metadata/
  scenarios/
notebooks/         notebook-driven verification
docs/              architecture and evaluation notes
```

## Setup

```bash
uv sync --extra dev
Copy `.env.example` to `.env` and set `GEMINI_API_KEY` to enable the Gemini signal.
```

## Run Tests

```bash
uv run pytest
```

Start the API:

```bash
uv run uvicorn sherlock_candidate_identifier.api.main:app --reload
```

Swagger is available at `http://127.0.0.1:8000/docs`. The `/predict` endpoint accepts
the same meeting JSON format as `MeetingReplay`. If Gemini is unavailable or no key
is configured, the LLM signal contributes zero score and confidence while the rest
of the pipeline continues normally.

## Run Demo

```bash
uv run sherlock-demo
```

## Notebook Workflow

Reusable logic lives in `src/`. Notebooks only import and verify modules.

- `01_meeting_simulator.ipynb`
- `02_name_signal.ipynb`
- `03_metadata_signal.ipynb`
- `04_transcript_signal.ipynb`
- `05_behavior_signal.ipynb`
- `06_video_signal.ipynb`
- `07_llm_reasoning.ipynb`
- `08_confidence_engine.ipynb`
- `09_full_pipeline.ipynb`

## How To Extend

- Add a new signal by implementing `evaluate(participant, state) -> SignalResult`.
- Add its weight in `config/signal_weights.py`.
- Add a notebook to inspect its behavior.
- Add a pytest file for deterministic checks.
- Add scenario JSON files under `data/scenarios/`.

FastAPI is a thin interface over the unchanged replay and evidence pipeline. Gemini
is isolated behind `llm/` and contributes only through the existing `LLMSignal`
contract.
