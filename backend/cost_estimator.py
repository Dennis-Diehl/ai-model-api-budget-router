"""Token estimation and cost calculation utilities."""

from backend.model_config import MODELS


def estimate_tokens(text: str) -> int:
    """Estimate the number of tokens for a given text.

    Uses a simple heuristic of ~4 characters per token.

    Args:
        text: The text to estimate tokens for.

    Returns:
        Estimated token count (minimum 1).
    """
    return max(1, len(text) // 4)


def estimate_cost(model_id: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate estimated cost for a model based on token counts.

    Computes input and output costs from per-token prices, rounded to
    8 decimal places.

    Args:
        model_id: The model identifier (key in MODELS).
        input_tokens: Number of input tokens.
        output_tokens: Number of output tokens.

    Returns:
        Estimated cost in USD.
    """
    model_config = MODELS[model_id]
    input_cost = input_tokens * model_config["input_price_per_token"]
    output_cost = output_tokens * model_config["output_price_per_token"]
    total_cost = input_cost + output_cost
    return round(total_cost, 8)


def calculate_actual_cost(
    model_id: str, input_tokens: int, output_tokens: int
) -> float:
    """Calculate actual cost after an API call.

    Currently delegates to ``estimate_cost``; can be extended with
    provider-specific billing logic.

    Args:
        model_id: The model identifier.
        input_tokens: Actual number of input tokens.
        output_tokens: Actual number of output tokens.

    Returns:
        Actual cost in USD.
    """
    return estimate_cost(model_id, input_tokens, output_tokens)
