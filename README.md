# Sieve

**Smart AI router — filters requests to the right model.**

> 🚧 **Early Development** — Works, but evolving. Feedback welcome!

Stop overpaying for AI. Sieve automatically routes simple queries to cheap models and complex ones to capable models, saving you 40-80% on API costs.

![Sieve Demo](demo.gif)

## Installation

```bash
pip install sievellm
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

## Setup

Set your OpenAI API key:
```bash
export OPENAI_API_KEY="sk-..."
```

## How It Works

1. **Analyzes** your prompt for complexity signals
2. **Routes** to the cheapest model that can handle it
3. **Tracks** actual cost per request

## Try It

```bash
git clone https://github.com/krymsnax/sieve
cd sieve
pip install -e .
python3 chat.py
```

## Roadmap

- [ ] Anthropic Claude support
- [ ] Streaming responses
- [ ] Budget limits
- [ ] ML-based complexity detection

## License

MIT
