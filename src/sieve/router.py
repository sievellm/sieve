"""Main routing logic with multi-provider support."""

import os
from dataclasses import dataclass

from openai import OpenAI

from .complexity import estimate_complexity, complexity_to_tier, estimate_complexity_keywords
from .models import MODELS, get_cheapest_in_tier

# Anthropic is optional
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


@dataclass
class RouterResponse:
    """Response from a routed request."""
    content: str
    model_used: str
    provider: str
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
    Supports OpenAI and Anthropic.
    
    Example:
        router = Router()
        response = router.route("What is 2+2?")
    """
    
    def __init__(
        self,
        openai_api_key: str | None = None,
        anthropic_api_key: str | None = None,
        default_provider: str = "openai",
        force_tier: str | None = None,
        smart_routing: bool = True,
    ):
        """
        Initialize the router.
        
        Args:
            openai_api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            anthropic_api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            default_provider: Preferred provider ("openai" or "anthropic")
            force_tier: Force a specific tier ("cheap", "mid", "expensive")
            smart_routing: Use AI to classify complexity
        """
        # OpenAI setup
        self.openai_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_key:
            raise ValueError(
                "OpenAI API key required. Pass openai_api_key or set OPENAI_API_KEY env var."
            )
        self.openai_client = OpenAI(api_key=self.openai_key)
        
        # Anthropic setup (optional)
        self.anthropic_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.anthropic_client = None
        if self.anthropic_key and ANTHROPIC_AVAILABLE:
            self.anthropic_client = Anthropic(api_key=self.anthropic_key)
        
        self.default_provider = default_provider
        self.force_tier = force_tier
        self.smart_routing = smart_routing
    
    def _call_openai(self, model: str, messages: list, system_prompt: str | None):
        """Call OpenAI API."""
        msgs = []
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        msgs.extend(messages)
        
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=msgs,
        )
        return {
            "content": response.choices[0].message.content,
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
        }
    
    def _call_anthropic(self, model: str, messages: list, system_prompt: str | None):
        """Call Anthropic API."""
        if not self.anthropic_client:
            raise ValueError(
                "Anthropic client not configured. Set ANTHROPIC_API_KEY or install: pip install anthropic"
            )
        
        # Map our model names to Anthropic's actual names
        model_map = {
            "claude-3-haiku": "claude-3-haiku-20240307",
            "claude-3.5-sonnet": "claude-3-5-sonnet-20241022",
            "claude-3-opus": "claude-3-opus-20240229",
        }
        anthropic_model = model_map.get(model, model)
        
        kwargs = {
            "model": anthropic_model,
            "max_tokens": 1024,
            "messages": messages,
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        
        response = self.anthropic_client.messages.create(**kwargs)
        return {
            "content": response.content[0].text,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
    
    def route(
        self,
        prompt: str,
        system_prompt: str | None = None,
        force_model: str | None = None,
    ) -> RouterResponse:
        """Route a prompt to the optimal model."""
        # Determine complexity
        if self.smart_routing:
            complexity = estimate_complexity(prompt, client=self.openai_client, use_ai=True)
        else:
            complexity = estimate_complexity_keywords(prompt)
        
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
        
        # Determine provider
        provider = MODELS.get(model, {}).get("provider", "openai")
        
        # Make API call based on provider
        messages = [{"role": "user", "content": prompt}]
        
        if provider == "anthropic":
            result = self._call_anthropic(model, messages, system_prompt)
        else:
            result = self._call_openai(model, messages, system_prompt)
        
        # Calculate cost
        model_info = MODELS.get(model, {"input_cost": 0, "output_cost": 0})
        cost = (
            (result["input_tokens"] / 1_000_000) * model_info["input_cost"] +
            (result["output_tokens"] / 1_000_000) * model_info["output_cost"]
        )
        
        return RouterResponse(
            content=result["content"],
            model_used=model,
            provider=provider,
            tier=tier,
            complexity_score=complexity,
            input_tokens=result["input_tokens"],
            output_tokens=result["output_tokens"],
            cost_usd=cost,
        )


# Convenience function
_default_router: Router | None = None


def route(prompt: str, **kwargs) -> RouterResponse:
    """Route a prompt to the optimal model (convenience function)."""
    global _default_router
    if _default_router is None:
        _default_router = Router()
    return _default_router.route(prompt, **kwargs)
