# AI Model Budget Router

A web app that routes AI prompts to the best LLM based on budget, task type, and quality level. Uses the Groq API for fast inference.

## Features

- **Smart Routing** - Selects the optimal model based on task type, quality requirements, and budget
- **Budget Guard** - Ensures requests stay within your specified budget
- **Cost Tracking** - Logs every request with estimated and actual costs
- **Usage Dashboard** - View stats on model usage and spending

## Prerequisites

- **Python 3.13** — Python 3.14 is not supported due to `pydantic-core` incompatibility
- **Groq API Key** — Get a free key at [console.groq.com](https://console.groq.com)

## Setup

### 1. Clone & install dependencies

```bash
git clone https://github.com/yourusername/ai-model-api-budget-router.git
cd ai-model-api-budget-router
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure API key

```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

### 3. Run the backend

```bash
uvicorn backend.app:app --reload
```

The API will be available at `http://localhost:8000`. Check `http://localhost:8000/docs` for the interactive API documentation.

### 4. Run the frontend

```bash
streamlit run frontend/app.py
```

For the usage dashboard:

```bash
streamlit run frontend/dashboard.py
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/route` | POST | Route a prompt to the best model |
| `/stats` | GET | Get usage statistics |

### Example request

```bash
curl -X POST http://localhost:8000/route \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quicksort", "task_type": "code", "budget": 0.01, "quality": "high"}'
```

## Available Models (via Groq)

| Model | Quality Score | Strengths |
|-------|--------------|-----------|
| LLaMA 3.3 70B | 85 | General, Code, Analysis |
| Mixtral 8x7B | 75 | Code, Analysis, Creative |
| Gemma 2 9B | 65 | General, Creative |
| LLaMA 3.1 8B | 60 | General |

## Project Structure

```
backend/
  app.py              # FastAPI server
  routing.py          # Model selection logic
  model_config.py     # Model definitions and pricing
  cost_estimator.py   # Token estimation and cost calculation
  budget_guard.py     # Budget validation
  llm_client.py       # Groq API client
  logging_service.py  # JSONL request logging
  schemas.py          # Pydantic data models
frontend/
  app.py              # Streamlit main UI
  dashboard.py        # Usage dashboard
logs/                 # Request logs (JSONL)
```

## License

MIT
