#!/usr/bin/env python3
"""Advanced demo showing cost savings."""
from sieve import route
from sieve.models import MODELS

print("=" * 55)
print("  SIEVELLM - Smart AI Router Demo")
print("=" * 55)

queries = [
    ("What is 2+2?", "Simple math"),
    ("Define API", "Simple definition"),
    ("Translate 'hello' to Spanish", "Simple translation"),
    ("Explain how OAuth2 authentication flow works step by step", "Complex explanation"),
    ("Debug: why does recursive fib(n) have O(2^n) complexity?", "Complex analysis"),
]

total_smart = 0
total_always_gpt4 = 0
gpt4_cost_per_1k = (MODELS["gpt-4-turbo"]["input_cost"] + MODELS["gpt-4-turbo"]["output_cost"]) / 2000

print("\n{:<45} {:>8}".format("Query", "Model"))
print("-" * 55)

for query, desc in queries:
    r = route(query)
    total_smart += r.cost_usd
    # Estimate what GPT-4 would have cost
    tokens = r.input_tokens + r.output_tokens
    gpt4_cost = tokens * gpt4_cost_per_1k
    total_always_gpt4 += gpt4_cost
    
    # Truncate query for display
    display = query[:42] + "..." if len(query) > 45 else query
    print(f"{display:<45} {r.model_used}")

print("-" * 55)
print(f"\n📊 COST COMPARISON:")
print(f"   With Sievellm:      ${total_smart:.4f}")
print(f"   Always GPT-4:       ${total_always_gpt4:.4f}")
savings = (1 - total_smart/total_always_gpt4) * 100 if total_always_gpt4 > 0 else 0
print(f"   💰 You saved:        {savings:.0f}%")
print()
