# Sieve

**Smart AI router — filters requests to the right model.**

Stop overpaying for AI. Sieve automatically routes simple queries to cheap models and complex ones to capable models, saving you 40-80% on API costs.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from sieve import route

# Simple query → routes to cheap model
response = route("What is 2+2?")
print(response)  # 4
print(f"Cost: ${response.cost_usd:.6f}")  # ~$0.000001

# Complex query → routes to capable model  
response = route("Analyze the trade-offs between microservices and monoliths")
print(f"Cost: ${response.cost_usd:.4f}")  # ~$0.02
```

## How It Works

1. **Analyzes** your prompt for complexity signals
2. **Routes** to the cheapest model that can handle it
3. **Tracks** actual cost per request

## Try It

```bash
python3 chat.py
```

## License

MIT
