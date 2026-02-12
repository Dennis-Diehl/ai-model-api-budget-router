"""Available model definitions and pricing configuration."""

MODELS: dict = {
    "llama-3.3-70b-versatile": {
        "name": "LLaMA 3.3 70B Versatile",
        "input_price_per_token": 0.00000059,
        "output_price_per_token": 0.00000079,
        "quality_score": 85,
        "strengths": ["general", "code", "summarize"],
        "max_tokens": 32768,
    },
    "llama-3.1-8b-instant": {
        "name": "LLaMA 3.1 8B Instant",
        "input_price_per_token": 0.00000005,
        "output_price_per_token": 0.00000008,
        "quality_score": 60,
        "strengths": ["general"],
        "max_tokens": 8192,
    },
    "gemma2-9b-it": {
        "name": "Gemma 2 9B IT",
        "input_price_per_token": 0.00000020,
        "output_price_per_token": 0.00000020,
        "quality_score": 65,
        "strengths": ["general", "email"],
        "max_tokens": 8192,
    },
    "mixtral-8x7b-32768": {
        "name": "Mixtral 8x7B 32768",
        "input_price_per_token": 0.00000024,
        "output_price_per_token": 0.00000024,
        "quality_score": 75,
        "strengths": ["code", "summarize", "email"],
        "max_tokens": 32768,
    },
}


QUALITY_THRESHOLDS: dict = {
    "low": 0,
    "medium": 60,
    "high": 75,
}
