"""Model selection algorithm based on task type, budget, and quality."""

from backend.budget_guard import check_budget
from backend.model_config import MODELS, QUALITY_THRESHOLDS


def select_model(
    prompt: str, task_type: str, budget: float, quality: str
) -> tuple[str, str]:
    """Select the best model based on task type, budget, and quality.

    Filters models by quality threshold and budget, scores them by
    quality (with a +15 bonus for task-type match), and returns the
    highest-scoring affordable model. Falls back to the cheapest
    affordable model if no candidate meets the quality threshold.

    Args:
        prompt: The user prompt.
        task_type: Task category (e.g. "general", "code", "email", "summarize").
        budget: Maximum budget in USD.
        quality: Desired quality level ("low", "medium", "high").

    Returns:
        Tuple of (model_id, reason).

    Raises:
        ValueError: If no model fits within the given budget.
    """
    min_quality_score = QUALITY_THRESHOLDS[quality]
    candidates = []

    for model_id, config in MODELS.items():
        if config["quality_score"] < min_quality_score:
            continue
        is_affordable, estimated_cost = check_budget(model_id, prompt, budget)
        if not is_affordable:
            continue
        score = config["quality_score"]
        if task_type in config["strengths"]:
            score += 15

        candidates.append((model_id, score, estimated_cost))

    if not candidates:
        # Fallback: find the cheapest affordable model ignoring quality
        affordable_models = []
        for model_id, config in MODELS.items():
            is_affordable, estimated_cost = check_budget(model_id, prompt, budget)
            if is_affordable:
                affordable_models.append((model_id, estimated_cost))
        if not affordable_models:
            raise ValueError("No model fits within the given budget.")
        affordable_models.sort(key=lambda c: c[1])
        return (affordable_models[0][0], "Fallback: only model within budget")

    # Best score first; cheapest first on tie
    candidates.sort(key=lambda c: (-c[1], c[2]))
    best_model_id = candidates[0][0]
    model_name = MODELS[best_model_id]["name"]
    score = candidates[0][1]
    estimated_cost = candidates[0][2]
    reason = f"Best match: {model_name} (score {score:.0f}, est. cost ${estimated_cost:.8f})"
    return (best_model_id, reason)