"""Budget validation for model requests."""

from backend.cost_estimator import estimate_cost, estimate_tokens
from backend.model_config import MODELS


def check_budget(model_id: str, prompt: str, budget: float) -> tuple[bool, float]:
    """Check whether estimated costs for a model fit within the budget.

    Estimates input tokens from the prompt, assumes output tokens as 2x
    input tokens (capped at the model's max_tokens), and compares the
    resulting cost against the budget.

    Args:
        model_id: The model identifier.
        prompt: The user prompt.
        budget: Maximum budget in USD.

    Returns:
        Tuple of (is_affordable, estimated_cost).
    """
    input_tokens = estimate_tokens(prompt)
    output_tokens = min(input_tokens * 2, MODELS[model_id]["max_tokens"])
    estimated_cost = estimate_cost(model_id, input_tokens, output_tokens)
    return (estimated_cost <= budget, estimated_cost)