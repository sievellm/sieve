#!/usr/bin/env python3
"""Advanced demo showing real developer scenarios with cost savings."""
from sieve import route
from sieve.models import MODELS

print("=" * 60)
print("  SIEVELLM v0.3.0 - Multi-Provider AI Router")
print("  Supports: OpenAI + Anthropic Claude")
print("=" * 60)

queries = [
    "What does HTTP 429 mean?",
    "Format this date: 2024-01-15",
    "Convert SQL JOIN to Python dict lookup",
    "Review this auth flow for OWASP vulnerabilities",
    "Refactor recursive function to iterative with memoization",
]

total_smart = 0
total_always_premium = 0
gpt4_per_token = (MODELS["gpt-4-turbo"]["input_cost"] +
                  MODELS["gpt-4-turbo"]["output_cost"]) / 2_000_000

print(f"\n{'Query':<42}{'Model':>16}")
print("-" * 60)

for query in queries:
    r = route(query)
    total_smart += r.cost_usd
    total_always_premium += (r.input_tokens + r.output_tokens) * gpt4_per_token

    display = query[:39] + "..." if len(query) > 42 else query
    print(f"{display:<42}{r.model_used:>16}")

print("-" * 60)
savings = (1 - total_smart/total_always_premium) * 100
print(f"\nWith Sievellm:    ${total_smart:.4f}")
print(f"Always GPT-4:     ${total_always_premium:.4f}")
print(f"You saved:        {savings:.0f}%")
print(f"\nWorks with Claude too: pip install 'sievellm[anthropic]'")
