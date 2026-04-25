# Sievellm

**Smart AI router — automatically routes to the right model.**

> 🚧 **Early Development** — Works, feedback welcome!

Stop overpaying for AI. Sievellm uses AI to detect query complexity and routes simple questions to cheap models, complex ones to capable models — saving you 40-80% on API costs.

![Sieve Demo](demo.gif)

## Why Sievellm?

| | LiteLLM | Sievellm |
|--|---------|----------|
| Setup | Docker, Postgres, YAML | `pip install sievellm` |
| Routing | Manual rules you configure | **AI auto-detects complexity** |
| Code | Proxy server + config | One line: `route("question")` |

## Installation

```bash
pip install sievellm
```

## Quick Start

```python
from sieve import route

# Simple query → automatically routes to cheap model (gpt-4o-mini)
response = route("What is 2+2?")
print(response)  # 4
print(f"Model: {response.model_used}")  # gpt-4o-mini
print(f"Cost: ${response.cost_usd:.6f}")  # ~$0.000007

# Complex query → automatically routes to capable model (gpt-4-turbo)
response = route("Explain the trade-offs between microservices and monoliths")
print(f"Model: {response.model_used}")  # gpt-4-turbo
```

## Setup

```bash
export OPENAI_API_KEY="sk-..."
```

## How It Works

1. **AI Classification** — Uses GPT-4o-mini to rate query complexity (costs ~$0.00001)
2. **Smart Routing** — Routes to cheap/mid/expensive tier based on complexity
3. **Cost Tracking** — Returns actual cost per request

## Options

```python
from sieve import Router

router = Router(
    smart_routing=True,   # AI-powered (default) or keyword-based
    force_tier="cheap",   # Force a specific tier (optional)
)
```

## Roadmap

- [x] AI-powered complexity detection
- [ ] Anthropic Claude support
- [ ] Multi-provider routing (cheapest across OpenAI + Anthropic + Google)
- [ ] Streaming responses
- [ ] Budget limits & alerts

## License

MIT
