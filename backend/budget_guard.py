"""Budget validation for model requests."""

from backend.cost_estimator import estimate_cost, estimate_output_tokens, estimate_tokens
from backend.model_config import MODELS


def check_budget(
    model_id: str, prompt: str, budget: float, task_type: str = "general"
) -> tuple[bool, float]:
    """Check whether estimated costs for a model fit within the budget.

    Estimates input tokens from the prompt, derives output tokens using
    task-type-aware heuristics, and compares the resulting cost against
    the budget.

    Args:
        model_id: The model identifier.
        prompt: The user prompt.
        budget: Maximum budget in USD.
        task_type: Task category (e.g. "general", "code", "email", "summarize").

    Returns:
        Tuple of (is_affordable, estimated_cost).
    """
    input_tokens = estimate_tokens(prompt)
    output_tokens = estimate_output_tokens(
        input_tokens, task_type, MODELS[model_id]["max_tokens"]
    )
    estimated_cost = estimate_cost(model_id, input_tokens, output_tokens)
    return (estimated_cost <= budget, estimated_cost)