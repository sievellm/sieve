# Sievellm

**Smart AI router — automatically routes to the right model across providers.**

> 🚧 **Early Development** — Works, feedback welcome!

Stop overpaying for AI. Sievellm uses AI to detect query complexity and routes between OpenAI and Anthropic — saving you 40-80% on API costs.

![Sieve Demo](demo.gif?v=5)

## Why Sievellm?

| | LiteLLM | Sievellm |
|--|---------|----------|
| Setup | Docker, Postgres, YAML | `pip install sievellm` |
| Routing | Manual rules you configure | **AI auto-detects complexity** |
| Code | Proxy server + config | One line: `route("question")` |
| Providers | Many | OpenAI + Anthropic |

## Installation

```bash
pip install sievellm                  # OpenAI only
pip install "sievellm[anthropic]"     # + Anthropic Claude
```

## Quick Start

```python
from sieve import route

# Simple query → routes to cheap model (gpt-4o-mini)
response = route("What does HTTP 403 mean?")
print(response.model_used)  # gpt-4o-mini
print(response.cost_usd)    # ~$0.000007

# Complex query → routes to capable model (gpt-4-turbo)
response = route("Review this auth code for security vulnerabilities")
print(response.model_used)  # gpt-4-turbo
```

## Setup

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."  # optional
```

## How It Works

1. **AI Classification** — Uses GPT-4o-mini to rate query complexity (~$0.00001)
2. **Smart Routing** — Routes to cheap/mid/expensive tier based on complexity
3. **Multi-Provider** — Choose OpenAI or Anthropic models
4. **Cost Tracking** — Returns actual cost per request

## Options

```python
from sieve import Router

router = Router(
    default_provider="anthropic",  # Use Claude by default
    smart_routing=True,            # AI-powered (default) or keyword-based
    force_tier="cheap",            # Force a specific tier (optional)
)
```

## Roadmap

- [x] AI-powered complexity detection
- [x] Anthropic Claude support
- [ ] Multi-provider routing (cheapest across providers)
- [ ] Streaming responses
- [ ] Budget limits & alerts

## License

MIT
