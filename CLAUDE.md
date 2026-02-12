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
frontend/            # Streamlit frontend (Platzhalter)
  app.py             # Hauptanwendung (TODO)
  dashboard.py       # Usage Dashboard (TODO)
```

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
