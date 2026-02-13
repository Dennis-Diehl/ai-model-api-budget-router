# AI Model Budget Router

A web app that routes AI prompts to the best LLM based on budget, task type, and quality level. Uses the Groq API for fast inference.

## Demo

> **Screenshot coming soon** - Run the app locally to see the interactive Streamlit UI with chat interface, real-time routing details, and usage dashboard.

## Why This Project?

This project demonstrates:
- **Full-Stack Development** - FastAPI backend + Streamlit frontend
- **API Integration** - Groq LLM API with proper error handling and retry logic
- **Cost Optimization** - Smart routing algorithm that balances quality and budget constraints
- **Production-Ready Code** - Pydantic validation, structured logging, clean architecture
- **Real-World Problem Solving** - Managing AI API costs is a real challenge for startups and developers

## Features

- **Smart Routing** - Selects the optimal model based on task type (code, Email, analysis, general), quality requirements, and budget constraints
- **Budget Guard** - Prevents requests that would exceed your specified budget before making API calls
- **Cost Tracking** - Logs every request with estimated and actual costs in JSONL format for analysis
- **Interactive Chat UI** - Streamlit-based interface with real-time routing details and cost breakdown
- **Usage Dashboard** - Live statistics on model usage, total spending, and request patterns
- **Multiple Quality Tiers** - Choose between high, medium, and low quality based on your needs
- **Task-Specific Optimization** - Models are scored higher for tasks they excel at (e.g., LLaMA 3.3 70B for code)

## Tech Stack

**Backend**:
- FastAPI - Modern Python web framework with automatic OpenAPI docs
- Pydantic - Data validation and settings management
- HTTPX - Async HTTP client for LLM API requests
- uvicorn - Lightning-fast ASGI server

**Frontend**:
- Streamlit - Interactive web UI with real-time updates
- Requests - HTTP client for backend communication

**LLM API**:
- Groq - Ultra-fast inference API (up to 750 tokens/sec)
- Models: LLaMA 3.3 70B, Mixtral 8x7B, Gemma 2 9B, LLaMA 3.1 8B

## Prerequisites

- **Python 3.13** — Python 3.14 is not supported due to `pydantic-core` incompatibility
- **Groq API Key** — Get a free key at [console.groq.com](https://console.groq.com)

## Setup

### 1. Clone & install dependencies

```bash
git clone https://github.com/YOUR_USERNAME/ai-model-api-budget-router.git
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

## Example Output

When you send a prompt, the router returns detailed information about the selected model and costs:

```json
{
  "model": "llama-3.3-70b-versatile",
  "response": "Quicksort is a divide-and-conquer sorting algorithm that works by selecting a 'pivot' element...",
  "estimated_cost": 0.0045,
  "actual_cost": 0.0042,
  "tokens_used": 523,
  "routing_reason": "Best quality match for code tasks within budget"
}
```

The chat UI displays this information in a user-friendly format with:
- Model indicator with emoji (🚀 for high-quality, ⚡ for fast/cheap)
- Cost breakdown (estimated vs actual)
- Token usage
- Routing explanation

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
| Mixtral 8x7B | 75 | Code, Summarize, Email|
| Gemma 2 9B | 65 | General, Email |
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
