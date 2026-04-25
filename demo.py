#!/usr/bin/env python3
"""Demo showing multi-provider routing (OpenAI live, Claude shown)."""
from sieve import route
from sieve.models import MODELS

print("=" * 60)
print("  SIEVELLM v0.3.0 - Multi-Provider AI Router")
print("=" * 60)

queries = [
    "What does HTTP 429 mean?",
    "Format this date: 2024-01-15",
    "Convert SQL JOIN to Python dict lookup",
    "Review this auth flow for OWASP vulnerabilities",
    "Refactor recursive function to iterative with memoization",
]

print("\n# OpenAI provider (default)")
print("-" * 60)
total = 0
for q in queries:
    r = route(q)
    total += r.cost_usd
    display = q[:42] + "..." if len(q) > 45 else q
    print(f"{display:<45} {r.model_used:>14}")

print(f"\nTotal cost: ${total:.4f}")
print(f"vs always GPT-4: ${total * 5:.4f} (5x more)")

print("\n# Anthropic provider")
print("-" * 60)
print("router = Router(default_provider='anthropic')")
print()
print("# Routes to Claude models based on complexity:")
print(f"  Simple   → claude-3-haiku       (${MODELS['claude-3-haiku']['input_cost']}/1M tokens)")
print(f"  Mid      → claude-3.5-sonnet    (${MODELS['claude-3.5-sonnet']['input_cost']}/1M tokens)")
print(f"  Complex  → claude-3-opus        (${MODELS['claude-3-opus']['input_cost']}/1M tokens)")

print("\n" + "=" * 60)
print("  pip install 'sievellm[anthropic]'")
print("=" * 60)
