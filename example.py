#!/usr/bin/env python3
"""Example usage of Sieve."""

from sieve import route, Router
from sieve.complexity import estimate_complexity

# --- Demo: Complexity Detection ---
print("=" * 50)
print("COMPLEXITY DETECTION DEMO")
print("=" * 50)

test_prompts = [
    "What is 2+2?",
    "Define photosynthesis",
    "Translate 'hello' to Spanish",
    "Explain step by step how neural networks learn",
    "Analyze the trade-offs between SQL and NoSQL databases for a high-traffic e-commerce platform",
    "Debug this code and explain why it's not working:\n```python\ndef fibonacci(n):\n    return fibonacci(n-1) + fibonacci(n-2)\n```",
]

for prompt in test_prompts:
    score = estimate_complexity(prompt)
    tier = "cheap" if score < 0.35 else "mid" if score < 0.65 else "expensive"
    print(f"\nPrompt: {prompt[:60]}...")
    print(f"  Complexity: {score:.2f} → Tier: {tier}")


# --- Demo: Actual Routing (requires API key) ---
print("\n" + "=" * 50)
print("ROUTING DEMO (requires OPENAI_API_KEY)")
print("=" * 50)

try:
    # Simple query - should route to cheap model
    print("\n[Simple Query]")
    response = route("What is the capital of France?")
    print(f"  Response: {response.content}")
    print(f"  Model: {response.model_used}")
    print(f"  Tier: {response.tier}")
    print(f"  Cost: ${response.cost_usd:.6f}")
    
    # Complex query - should route to expensive model
    print("\n[Complex Query]")
    response = route(
        "Explain step by step how to implement a binary search tree, "
        "including insertion, deletion, and balancing considerations."
    )
    print(f"  Response: {response.content[:200]}...")
    print(f"  Model: {response.model_used}")
    print(f"  Tier: {response.tier}")
    print(f"  Cost: ${response.cost_usd:.6f}")
    
except ValueError as e:
    print(f"\n  Skipping routing demo: {e}")
    print("  Set OPENAI_API_KEY environment variable to run this demo.")
