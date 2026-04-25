"""Main routing logic."""

import os
from dataclasses import dataclass

from openai import OpenAI

from .complexity import estimate_complexity, complexity_to_tier
from .models import MODELS, get_cheapest_in_tier


@dataclass
class RouterResponse:
    """Response from a routed request."""
    content: str
    model_used: str
    tier: str
    complexity_score: float
    input_tokens: int
    output_tokens: int
    cost_usd: float
    
    def __str__(self) -> str:
        return self.content


class Router:
    """
    AI request router that selects models based on query complexity.
    
    Example:
        router = Router()
        response = router.route("What is 2+2?")
        print(response.content)  # "4"
        print(response.cost_usd)  # 0.000001
    """
    
    def __init__(
        self,
        openai_api_key: str | None = None,
        default_provider: str = "openai",
        force_tier: str | None = None,
    ):
        """
        Initialize the router.
        
        Args:
            openai_api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            default_provider: Preferred provider ("openai" or "anthropic")
            force_tier: Force a specific tier ("cheap", "mid", "expensive")
        """
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Pass openai_api_key or set OPENAI_API_KEY env var."
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.default_provider = default_provider
        self.force_tier = force_tier
    
    def route(
        self,
        prompt: str,
        system_prompt: str | None = None,
        force_model: str | None = None,
    ) -> RouterResponse:
        """
        Route a prompt to the optimal model and get a response.
        
        Args:
            prompt: The user's prompt
            system_prompt: Optional system prompt
            force_model: Force a specific model (bypasses routing)
            
        Returns:
            RouterResponse with content, model used, and cost info
        """
        # Determine complexity
        complexity = estimate_complexity(prompt)
        
        # Select model
        if force_model:
            model = force_model
            tier = MODELS.get(model, {}).get("tier", "unknown")
        elif self.force_tier:
            tier = self.force_tier
            model = get_cheapest_in_tier(tier, self.default_provider)
        else:
            tier = complexity_to_tier(complexity)
            model = get_cheapest_in_tier(tier, self.default_provider)
        
        # Build messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Make API call
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )
        
        # Extract usage
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        
        # Calculate cost
        model_info = MODELS.get(model, {"input_cost": 0, "output_cost": 0})
        cost = (
            (input_tokens / 1_000_000) * model_info["input_cost"] +
            (output_tokens / 1_000_000) * model_info["output_cost"]
        )
        
        return RouterResponse(
            content=response.choices[0].message.content,
            model_used=model,
            tier=tier,
            complexity_score=complexity,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
        )


# Convenience function for simple usage
_default_router: Router | None = None


def route(prompt: str, **kwargs) -> RouterResponse:
    """
    Route a prompt to the optimal model (convenience function).
    
    Uses a default Router instance. For more control, create a Router directly.
    
    Example:
        from simple_router import route
        
        response = route("What is the capital of France?")
        print(response)  # Paris
        print(f"Cost: ${response.cost_usd:.6f}")
    """
    global _default_router
    if _default_router is None:
        _default_router = Router()
    return _default_router.route(prompt, **kwargs)
