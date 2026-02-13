"""FastAPI application — ties all backend modules together into a web API.

Provides three endpoints:
- GET  /health  — simple health check
- POST /route   — route a prompt to the best model and return the LLM response
- GET  /stats   — return usage statistics

Run with: uvicorn backend.app:app --reload
API docs: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.cost_estimator import calculate_actual_cost, estimate_cost, estimate_tokens, estimate_output_tokens
from backend.llm_client import call_llm
from backend.logging_service import get_stats, log_request
from backend.routing import select_model
from backend.schemas import HealthResponse, RouteRequest, RouteResponse, StatsResponse
from backend.model_config import MODELS

app = FastAPI(title="AI Model Budget Router")

# Allow the Streamlit frontend (different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health():
   """Return a simple status check to verify the server is running."""
   return HealthResponse(status="ok")


@app.post("/route", response_model=RouteResponse)
async def route(request: RouteRequest):
   """Main endpoint: select a model, call the LLM, and return the response.

   Flow:
   1. Pick the best model for the given task, budget, and quality level.
   2. Estimate cost upfront so we can reject requests that exceed the budget.
   3. Call the Groq API and get the actual response.
   4. Calculate the real cost based on actual token usage.
   5. Log the request for the /stats endpoint.
   6. Return the response with cost and routing details.
   """
   # Step 1: Select the best model — raises ValueError if nothing fits the budget
   try:
      model_id, routing_reason = select_model(request.prompt, request.task_type, request.budget, request.quality)
   except ValueError as e:
      raise HTTPException(status_code=400, detail=str(e))

   # Step 2: Estimate tokens and cost before calling the API
   input_tokens_est = estimate_tokens(request.prompt)
   output_tokens_est = estimate_output_tokens(input_tokens_est, request.task_type, MODELS[model_id]["max_tokens"])
   cost_est = estimate_cost(model_id, input_tokens_est, output_tokens_est)

   # Safety check: reject if estimated cost exceeds the user's budget
   if cost_est > request.budget:
      raise HTTPException(status_code=400, detail=f"Estimated cost ${cost_est} exceeds budget ${request.budget}.")

   # Step 3: Call the Groq API — RuntimeError means missing API key, other errors are upstream failures
   try:
      llm_response = await call_llm(model_id, request.prompt, max_tokens=output_tokens_est)
   except RuntimeError as e:
      raise HTTPException(status_code=500, detail=str(e))
   except Exception as e:
      raise HTTPException(status_code=502, detail=f"Error calling LLM: {str(e)}")

   # Step 4: Calculate actual cost using the real token counts from the API response
   actual_cost = calculate_actual_cost(model_id, llm_response["input_tokens"], llm_response["output_tokens"])

   # Step 5: Log the request so /stats can aggregate it later
   log_request({
      "model": model_id,
      "input_tokens": llm_response["input_tokens"],
      "output_tokens": llm_response["output_tokens"],
      "actual_cost": actual_cost,
      "routing_reason": routing_reason,
   })

   # Step 6: Build and return the response
   return RouteResponse(
      model=model_id,
      response=llm_response["content"],
      estimated_cost=cost_est,
      actual_cost=actual_cost,
      tokens_used=llm_response["input_tokens"] + llm_response["output_tokens"],
      routing_reason=routing_reason,
   )


@app.get("/stats", response_model=StatsResponse)
async def stats():
   """Return aggregated usage statistics (total requests, costs, model usage)."""
   return StatsResponse(**get_stats())
