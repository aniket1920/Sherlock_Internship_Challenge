# Evaluation

## Test Method

The test suite checks every signal independently and then replays a complete JSON scenario through the full pipeline.

Current coverage:

- Name signal fuzzy matching.
- Metadata candidate email and interviewer exclusion.
- Transcript role cues.
- Behavior speaking share.
- Video camera and face-count evidence.
- LLM placeholder output contract.
- Confidence engine probability fusion.
- Meeting simulator JSON replay.

## Current Result

Run:

```bash
uv run pytest
```

## Accuracy

The included sample scenario identifies the expected candidate. This is not a production accuracy claim; it validates the architecture and edge-case handling path.

Future accuracy should be measured against labeled real interview meetings with participant ground truth.

## Limitations

- No real Google Meet, Teams, or Zoom adapter yet.
- No real audio/video model inference yet.
- Signal weights are hand-tuned and should be calibrated on real labeled meetings.
- LLM signal is a structured placeholder.

## Next Improvements

- Add meeting-platform adapters.
- Add face and voice candidate enrollment signals.
- Add sentence-transformer transcript role embeddings.
- Add LLM transcript-role reasoning with strict JSON outputs.
- Store sessions and event streams in Redis/Postgres.
- Build FastAPI only after the AI engine and notebooks are stable.
