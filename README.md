# Sievellm

**Smart AI router — automatically picks the right model for each query.**

Stop overpaying for AI. Sievellm uses AI to detect query complexity and routes between OpenAI and Anthropic — saving you 40-80% on API costs.

![Sieve Demo](demo.gif?v=8)

## Why Sievellm?

| | LiteLLM | Sievellm |
|--|---------|----------|
| Setup | Docker, Postgres, YAML | `pip install sievellm` |
| Routing | Manual rules you configure | AI auto-detects complexity |
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

# Simple query → routes to cheap model
response = route("What does HTTP 403 mean?")
print(response.model_used)  # gpt-4o-mini

# Complex query → routes to capable model
response = route("Review this auth code for security vulnerabilities")
print(response.model_used)  # gpt-4-turbo
```

## Setup

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."  # optional
```

## Options

```python
from sieve import Router

router = Router(
    default_provider="anthropic",  # Use Claude
    smart_routing=True,            # AI-powered classification
    force_tier="cheap",            # Force a tier (optional)
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
