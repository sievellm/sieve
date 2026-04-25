#!/usr/bin/env python3
"""Demo for GIF recording."""
from sieve import route

print("=" * 50)
print("SIEVE DEMO")
print("=" * 50)

print("\n[Simple question → cheap model]")
r = route("What is 2+2?")
print(f"Answer: {r}")
print(f"Model: {r.model_used} | Cost: ${r.cost_usd:.6f}")

print("\n[Complex question → capable model]")
r = route("Explain briefly how quicksort works")
print(f"Answer: {r.content[:100]}...")
print(f"Model: {r.model_used} | Cost: ${r.cost_usd:.6f}")

print("\n✓ Save 40-80% on AI costs automatically!")
