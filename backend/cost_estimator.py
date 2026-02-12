"""Token estimation and cost calculation utilities."""

from backend.model_config import MODELS


def estimate_tokens(text: str) -> int:
    """Estimate the number of tokens based on text characteristics.

    Uses content-aware heuristics: code (~3 chars/token), technical/long-word
    text (~5 chars/token), and normal English (~4 chars/token). Adjusts for
    high whitespace ratio.

    Args:
        text: The text to estimate tokens for.

    Returns:
        Estimated token count (minimum 1).
    """
    if not text.strip():
        return 1

    length = len(text)

    code_indicators = sum(1 for c in text if c in '{}();=<>[]')
    code_ratio = code_indicators / max(length, 1)

    whitespace_ratio = sum(1 for c in text if c.isspace()) / max(length, 1)

    words = text.split()
    avg_word_len = sum(len(w) for w in words) / max(len(words), 1)

    if code_ratio > 0.05:
        chars_per_token = 3.0
    elif avg_word_len > 7:
        chars_per_token = 5.0
    else:
        chars_per_token = 4.0

    if whitespace_ratio > 0.3:
        chars_per_token *= 0.9

    return max(1, int(length / chars_per_token))


OUTPUT_MULTIPLIERS = {
    "summarize": 0.3,
    "email": 0.8,
    "code": 2.5,
    "general": 1.5,
}

MIN_OUTPUT_TOKENS = {
    "summarize": 100,
    "email": 200,
    "code": 300,
    "general": 150,
}


def estimate_output_tokens(input_tokens: int, task_type: str, model_max_tokens: int) -> int:
    """Estimate output tokens based on task type and input length.

    Uses task-specific multipliers and minimum output floors. Result is
    capped at the model's max_tokens.

    Args:
        input_tokens: Estimated input token count.
        task_type: Task category (e.g. "general", "code", "email", "summarize").
        model_max_tokens: Maximum tokens the model can generate.

    Returns:
        Estimated output token count.
    """
    multiplier = OUTPUT_MULTIPLIERS.get(task_type, 1.5)
    min_output = MIN_OUTPUT_TOKENS.get(task_type, 150)

    estimated = max(min_output, int(input_tokens * multiplier))
    return min(estimated, model_max_tokens)


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
