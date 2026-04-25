"""Model definitions with pricing (per 1M tokens, as of April 2026)."""

MODELS = {
    # Cheap tier - use for simple tasks
    "gpt-4o-mini": {
        "provider": "openai",
        "input_cost": 0.15,   # $ per 1M input tokens
        "output_cost": 0.60,  # $ per 1M output tokens
        "tier": "cheap",
    },
    "claude-3-haiku": {
        "provider": "anthropic",
        "input_cost": 0.25,
        "output_cost": 1.25,
        "tier": "cheap",
    },
    
    # Mid tier - balanced cost/capability
    "gpt-4o": {
        "provider": "openai",
        "input_cost": 2.50,
        "output_cost": 10.00,
        "tier": "mid",
    },
    "claude-3.5-sonnet": {
        "provider": "anthropic",
        "input_cost": 3.00,
        "output_cost": 15.00,
        "tier": "mid",
    },
    
    # Expensive tier - use for complex reasoning
    "claude-3-opus": {
        "provider": "anthropic",
        "input_cost": 15.00,
        "output_cost": 75.00,
        "tier": "expensive",
    },
    "gpt-4-turbo": {
        "provider": "openai",
        "input_cost": 10.00,
        "output_cost": 30.00,
        "tier": "expensive",
    },
}


def get_models_by_tier(tier: str) -> list[str]:
    """Get all model names for a given tier."""
    return [name for name, info in MODELS.items() if info["tier"] == tier]


def get_cheapest_in_tier(tier: str, provider: str | None = None) -> str:
    """Get the cheapest model in a tier, optionally filtered by provider."""
    candidates = [
        (name, info) for name, info in MODELS.items()
        if info["tier"] == tier and (provider is None or info["provider"] == provider)
    ]
    if not candidates:
        raise ValueError(f"No models found for tier={tier}, provider={provider}")
    
    # Sort by total cost (input + output, assuming roughly equal)
    return min(candidates, key=lambda x: x[1]["input_cost"] + x[1]["output_cost"])[0]
