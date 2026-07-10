# Sherlock Candidate Identifier
### AI-Powered Real-Time Interview Candidate Identification System

> Submission for the **Sherlock Internship Challenge**

## Overview

Sherlock is an AI platform that detects fraud during online interviews. Before any fraud detection can happen, Sherlock must first identify **which participant is actually the interview candidate**.

This project is a production-oriented prototype that automatically identifies the interview candidate in real time by combining multiple independent evidence sources instead of relying on a single rule.

The system continuously evaluates every participant, assigns confidence scores, explains every prediction, and gracefully handles ambiguous situations such as:

- Candidate joins as **"MacBook Pro"**
- Candidate joins using a nickname
- Incorrect participant names
- Multiple interviewers
- Silent observers
- Missing metadata

---

# Demo Video

🎥 **Project Walkthrough**

https://www.loom.com/share/b1d5664ec700434898065043b94b67f5

The walkthrough includes:

- Problem statement
- Architecture
- AI approach
- Live FastAPI demonstration
- Trade-offs
- Future improvements

---

# Features

- Multi-signal evidence fusion
- Confidence score for every participant
- Explainable predictions
- Gemini-powered semantic reasoning
- FastAPI REST API
- Interactive Swagger documentation
- Modular architecture
- Notebook-driven development
- Automated unit tests

---

# Architecture

This project follows a modular evidence-fusion architecture where multiple independent AI signals evaluate each participant before a confidence engine produces the final prediction.

📄 **Detailed Architecture:** [docs/architecture.md](docs/architecture.md)

The documentation includes:

- Complete system architecture
- Evidence flow
- Signal pipeline
- Confidence fusion
- Explainability engine
- Design decisions

# AI Signals

The system evaluates every participant using multiple independent signals.

| Signal | Purpose |
|---------|---------|
| Name Signal | Fuzzy matching against expected candidate name |
| Metadata Signal | Candidate email, calendar information, interviewer names |
| Transcript Signal | Rule-based conversational cues |
| Behavior Signal | Speaking duration and interaction patterns |
| Video Signal | Camera status, face count, webcam activity |
| Gemini LLM Signal | Semantic reasoning over transcript and participant context |

No single signal determines the final prediction.

Instead, all evidence is fused into one confidence score.

---

# Explainability

Unlike black-box classifiers, every prediction includes human-readable reasoning.

Example:

- Metadata matches scheduled candidate
- Transcript describes personal implementation work
- Speaking behavior resembles interview candidate
- Gemini classified participant as candidate

---

# Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- uv

### AI

- Google Gemini 2.5 Flash
- Rule-based Evidence Signals
- Confidence Fusion Engine

### Testing

- Pytest
- Jupyter Notebook Validation

---

# Project Structure

```
src/
└── sherlock_candidate_identifier/
    ├── api/
    ├── confidence/
    ├── config/
    ├── explainability/
    ├── llm/
    ├── models/
    ├── reasoning/
    ├── signals/
    ├── simulator/
    └── utils/

tests/
notebooks/
data/
docs/
```

---

# Installation

Clone the repository

```bash
git clone github.com/aniket1920/Sherlock_Internship_Challenge
cd sherlock-candidate-identifier
```

Install dependencies

```bash
uv sync --extra dev
```

Create environment file

```
.env
```

Add your Gemini API key

```
GEMINI_API_KEY=YOUR_API_KEY
```

---

# Running the Project

Start FastAPI

```bash
uv run uvicorn sherlock_candidate_identifier.api.main:app --reload
```

Open Swagger

```
http://127.0.0.1:8000/docs
```

Endpoints

### GET

```
/health
```

Returns

```json
{
    "status":"ok"
}
```

### POST

```
/predict
```

Accepts a meeting JSON payload and returns:

- Identified candidate
- Confidence score
- Ranked participant probabilities
- Evidence from every signal
- Final explanation

---

# Running Tests

Run all automated tests

```bash
uv run pytest
```

Current Status

```
12 tests passed
```

---

# Notebook Workflow

Each notebook validates one module independently.

| Notebook | Purpose |
|-----------|----------|
| 01 | Meeting Replay |
| 02 | Name Signal |
| 03 | Metadata Signal |
| 04 | Transcript Signal |
| 05 | Behavior Signal |
| 06 | Video Signal |
| 07 | Gemini LLM Integration |
| 08 | Confidence Engine |
| 09 | Full Pipeline |

---

# Testing & Evaluation

The project was evaluated using:

- Unit tests
- Notebook verification
- FastAPI API testing
- Swagger integration
- End-to-end replay scenarios

Example scenarios include:

- Candidate joins as **MacBook Pro**
- Multiple interviewers
- Missing metadata
- Transcript-based identification
- Candidate explanation generation

---

# Trade-offs

The current prototype assumes structured meeting information (participant metadata, transcripts, webcam state, etc.) is already available, as specified in the challenge statement.

Instead of building a meeting platform integration, the project focuses entirely on the candidate identification problem.

Gemini is used as **one evidence source** rather than making the final decision directly, allowing deterministic confidence fusion and explainability.

---

# Future Improvements

- Direct Google Meet / Zoom integration
- Real-time event streaming
- Better conversational behavior modeling
- Historical learning from previous interviews
- Confidence smoothing across long meetings
- Additional real-world evaluation scenarios

---

# Why This Approach?

Rather than relying on a single heuristic, this system combines multiple weak evidence sources to produce a robust and explainable prediction.

This closely aligns with Sherlock's stated evaluation criteria:

- Multi-signal reasoning
- Confidence estimation
- Explainability
- Real-time updates
- Graceful handling of ambiguity

---

# Author

**Aniket Singh**

GitHub: https://github.com/aniket1920/

Submission for the Sherlock Internship Challenge.
