"""Pydantic request and response models for the API."""

from pydantic import BaseModel, Field


class RouteRequest(BaseModel):
    """Incoming routing request.

    Attributes:
        prompt: The user's text prompt (1–10 000 chars).
        task_type: Task category — "general", "code", "email", or "summarize".
        budget: Maximum budget in USD (must be > 0).
        quality: Desired quality level (default "medium").
    """
    prompt: str = Field(..., min_length=1, max_length=10000)
    task_type: str = Field(..., pattern="^(general|code|email|summarize)$")
    budget: float = Field(..., gt=0)
    quality: str = Field(default="medium")


class RouteResponse(BaseModel):
    """Response after successful routing.

    Attributes:
        model: ID of the selected model.
        response: The LLM-generated answer.
        estimated_cost: Pre-call cost estimate in USD.
        actual_cost: Actual cost after the API call in USD.
        tokens_used: Total number of tokens consumed.
        routing_reason: Explanation for the model choice.
    """
    model: str
    response: str
    estimated_cost: float
    actual_cost: float
    tokens_used: int
    routing_reason: str


class HealthResponse(BaseModel):
    """Health check response.

    Attributes:
        status: Service status, e.g. "ok".
    """
    status: str


class StatsResponse(BaseModel):
    """Usage statistics response.

    Attributes:
        total_requests: Total number of requests served.
        total_cost: Cumulative cost in USD.
        average_cost: Mean cost per request in USD.
        model_usage: Request count per model ID.
    """

    total_requests: int
    total_cost: float
    average_cost: float
    model_usage: dict[str, int]