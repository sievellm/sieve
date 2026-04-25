#!/usr/bin/env python3
"""Sievellm demo with live responses."""
from sieve import route

print("\033[1;36m╭" + "─" * 58 + "╮\033[0m")
print("\033[1;36m│\033[0m  \033[1mSIEVELLM\033[0m - Smart AI Router (OpenAI + Anthropic)" + "      \033[1;36m│\033[0m")
print("\033[1;36m╰" + "─" * 58 + "╯\033[0m")

queries = [
    ("What does HTTP 429 mean?", "🟢 Simple"),
    ("Convert 'snake_case' to 'camelCase' in Python", "🟢 Simple"),
    ("Explain race conditions in async code", "🟡 Medium"),
    ("Review this auth code for OWASP vulnerabilities", "🔴 Complex"),
]

total_cost = 0
gpt4_cost = 0

for query, badge in queries:
    r = route(query)
    total_cost += r.cost_usd
    # Estimate GPT-4 cost (~5x more expensive)
    gpt4_cost += r.cost_usd * 5
    
    print(f"\n\033[1m{badge}  {query}\033[0m")
    print(f"  \033[2m→ Routed to: \033[36m{r.model_used}\033[0m \033[2m(${r.cost_usd:.5f})\033[0m")
    
    # Show truncated response
    response = r.content.replace("\n", " ").strip()
    if len(response) > 80:
        response = response[:77] + "..."
    print(f"  \033[2m💬 {response}\033[0m")

print("\n\033[1;32m" + "═" * 60 + "\033[0m")
savings = (1 - total_cost/gpt4_cost) * 100
print(f"\033[1m📊 Cost Summary\033[0m")
print(f"   Sievellm:    \033[1;32m${total_cost:.4f}\033[0m")
print(f"   Always GPT-4: \033[1;31m${gpt4_cost:.4f}\033[0m")
print(f"   \033[1;33m💰 Saved {savings:.0f}%\033[0m")
print("\033[1;32m" + "═" * 60 + "\033[0m\n")
