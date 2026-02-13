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
  dashboard.py       # Usage Dashboard (Implemented)
```

## Frontend Features

### Chat Interface (app.py)
- Interactive chat UI with Streamlit
- Sidebar configuration (task_type, budget, quality)
- Real-time integration with backend /route endpoint
- Display of:
  - AI Response
  - Selected model with emoji indicator
  - Costs (estimated vs actual)
  - Tokens used
  - Routing reason
- Session state for chat history
- Error handling for backend connection

### Dashboard (dashboard.py)
- Usage statistics display
- Total requests, costs, average cost
- Model usage breakdown (pie chart)
- Auto-refresh every 5 seconds
- Real-time data from logs/requests.jsonl

## Commands

- **Backend starten**: `uvicorn backend.app:app --reload`
- **Frontend starten**: `streamlit run frontend/app.py`
- **Tests**: `pytest` (aktuell keine Tests vorhanden)
- **Virtual Environment**: `.venv` verwenden

## Routing-Algorithmus

Der Score besteht aus:
- `quality_score` des Modells
- `+15` Bonus wenn `task_type` in den `strengths` des Modells ist
- Fallback auf günstigstes bezahlbares Modell wenn kein Kandidat die Qualitätsschwelle erreicht

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
