"""Available model definitions and pricing configuration."""

MODELS: dict = {
    "llama-3.3-70b-versatile": {
        "name": "LLaMA 3.3 70B Versatile",
        "input_price_per_token": 0.00000059,
        "output_price_per_token": 0.00000079,
        "quality_score": 88,
        "strengths": ["general", "code", "summarize"],
        "max_tokens": 32768,
    },
    "llama-3.1-8b-instant": {
        "name": "LLaMA 3.1 8B Instant",
        "input_price_per_token": 0.00000005,
        "output_price_per_token": 0.00000008,
        "quality_score": 55,
        "strengths": ["general"],
        "max_tokens": 131072,
    },
    "openai/gpt-oss-120b": {
        "name": "GPT-OSS 120B",
        "input_price_per_token": 0.00000015,
        "output_price_per_token": 0.00000060,
        "quality_score": 85,
        "strengths": ["general", "code", "email"],
        "max_tokens": 65536,
    },
    "openai/gpt-oss-20b": {
        "name": "GPT-OSS 20B",
        "input_price_per_token": 0.000000075,
        "output_price_per_token": 0.00000030,
        "quality_score": 68,
        "strengths": ["general", "email"],
        "max_tokens": 65536,
    },
}


QUALITY_THRESHOLDS: dict = {
    "low": 0,
    "medium": 60,
    "high": 75,
}
