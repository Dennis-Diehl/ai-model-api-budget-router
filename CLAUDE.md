# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ai-model-api-budget-router** is a Python project for routing AI model API requests based on budget constraints.

- **Language**: Python
- **License**: MIT
- **Author**: Dennis Diehl

## Project Structure

```
backend/             # FastAPI backend
  app.py             # API endpoints (FastAPI)
  routing.py         # Routing-Algorithmus (Modellauswahl)
  model_config.py    # Modell-Definitionen und Preise
  cost_estimator.py  # Kostenberechnung
  budget_guard.py    # Budget-Prüfung
  llm_client.py      # LLM API Client
  logging_service.py # Request-Logging
  schemas.py         # Pydantic Schemas
frontend/            # Streamlit frontend
  app.py             # Chat Interface (Implemented)
  dashboard.py       # Usage Dashboard (Placeholder only - NOT implemented)
```

## Frontend Features

### Chat Interface (app.py) ✓ FULLY IMPLEMENTED
- Interactive chat UI with Streamlit st.chat_message()
- **Sidebar controls**:
  - Task Type selector: general, code, email, summarize (matches backend validation)
  - Quality Level selector: low (0+), medium (60+), high (75+)
  - Budget slider: $0.0001 to $0.01
  - Session spending tracker
- **Backend integration**:
  - POST /route with prompt, task_type, budget, quality
  - 60-second timeout
- **Response display**:
  - AI response text
  - Expandable "Model Selection Details" (model name, routing reason)
  - Expandable "Cost Breakdown" (estimated, actual, delta %, tokens)
- **Session state**: Persistent chat history across reruns
- **Error handling**:
  - HTTP 400: Budget/validation errors with hints
  - Connection errors: Backend not running message
  - Timeout errors: Request took too long
  - Shows troubleshooting: "Run `uvicorn backend.app:app --reload`"

### Dashboard (dashboard.py) ✗ NOT IMPLEMENTED
- **Current state**: Single function `render_dashboard()` with only `pass`
- **Intended features** (from TODO comments):
  - Load stats from GET /stats
  - Display: Total Requests, Total Cost, Average Cost
  - Bar chart of model usage
  - Optional log table
- **Backend support ready**: GET /stats endpoint exists and returns StatsResponse

## Model Configuration

Four models configured in `backend/model_config.py`:

| Model ID | Quality | Input $/M | Output $/M | Strengths | Max Tokens |
|----------|---------|-----------|------------|-----------|-----------|
| llama-3.3-70b-versatile | 88 | 0.00059 | 0.00079 | general, code, summarize | 32,768 |
| openai/gpt-oss-120b | 85 | 0.00015 | 0.00060 | general, code, email | 65,536 |
| openai/gpt-oss-20b | 68 | 0.000075 | 0.00030 | general, email | 65,536 |
| llama-3.1-8b-instant | 55 | 0.00005 | 0.00008 | general | 131,072 |

**Quality Thresholds**:
- "low" = 0 (alle Modelle verfügbar)
- "medium" = 60 (LLaMA 8B wird ausgefiltert)
- "high" = 75 (nur 70B+ Modelle: LLaMA 70B, GPT-OSS 120B)

**Valid Task Types**: general, code, email, summarize (defined in schemas.py)

## Commands

- **Backend starten**: `uvicorn backend.app:app --reload`
- **Frontend starten**: `streamlit run frontend/app.py`
- **Tests**: `pytest` (aktuell keine Tests vorhanden)
- **Virtual Environment**: `.venv` verwenden

## Routing-Algorithmus

Der Routing-Algorithmus (backend/routing.py):

1. **Filtern nach Quality Threshold**:
   - "low" → alle Modelle (threshold 0)
   - "medium" → min quality 60
   - "high" → min quality 75

2. **Filtern nach Budget**:
   - Nutzt `check_budget()` aus budget_guard.py
   - Schätzt Input-Tokens (content-aware: code detection, word length analysis)
   - Schätzt Output-Tokens (task-specific: code 2.5x, summarize 0.3x, etc.)
   - Filtert unerschwingliche Modelle

3. **Scoring**:
   - Base Score = `quality_score` des Modells
   - **+15 Bonus** wenn `task_type` in `strengths` (z.B. "code" für LLaMA 70B)
   - Beispiel: LLaMA 70B (88) + code bonus (15) = 103

4. **Auswahl**:
   - Höchster Score gewinnt
   - Bei Gleichstand: günstigstes Modell

5. **Fallback**:
   - Wenn kein Modell Quality Threshold erreicht → günstigstes bezahlbares wählen
   - Wenn gar nichts bezahlbar → ValueError

## Technical Implementation Details

### Token Estimation (cost_estimator.py)
- **Content-aware input estimation**:
  - Code detection: checks for `{}();=<>[]` frequency → 3 chars/token
  - Technical text: avg word length >7 → 5 chars/token
  - Normal text: 4 chars/token
  - Whitespace correction: -10% if >30% whitespace
- **Task-specific output estimation**:
  - "summarize": 0.3x multiplier (min 100 tokens)
  - "email": 0.8x (min 200 tokens)
  - "code": 2.5x (min 300 tokens)
  - "general": 1.5x (min 150 tokens)
  - Capped at model's max_tokens

### LLM Client (llm_client.py)
- Async HTTP client using httpx
- Endpoint: `https://api.groq.com/openai/v1/chat/completions`
- 60-second timeout
- No retry logic (single attempt)
- No streaming support
- Error propagation: Network/API errors → handled in app.py as 502

### Logging (logging_service.py)
- Format: JSONL (newline-delimited JSON)
- Location: `logs/requests.jsonl`
- Tracked fields: timestamp (ISO 8601 UTC), model, tokens, cost, routing_reason
- No log rotation or size limits

## Deployment Notes

### Python Version Requirement
- **MUST use Python 3.13** - Python 3.14 is NOT supported
- Reason: `pydantic-core` does not have pre-built wheels for Python 3.14
- When deploying to platforms like Railway/Render, ensure Python 3.13 is specified in runtime config

### Environment Variables
- `GROQ_API_KEY` - Required for LLM API access (get from console.groq.com)
- `BACKEND_URL` - Frontend needs this in production (default: http://localhost:8000)

### Logging Considerations
- App logs to `logs/requests.jsonl` by default
- On ephemeral filesystems (Railway, Render), logs are lost on restart
- Consider database logging or external logging service for production
- Current implementation uses file-based JSONL for simplicity

### Security Considerations
- ⚠️ `.env` file contains actual API key and is tracked in git (security issue)
- Should create `.env.example` template without real key
- For production: Use environment variable injection (Railway, Render, etc.)

### Missing Features for Production
- No pytest test suite (only Jupyter notebooks in tests/)
- No Docker/containerization
- No CI/CD pipeline
- No rate limiting on API endpoints
- No request retry logic in LLM client
- No log rotation (logs grow indefinitely)
