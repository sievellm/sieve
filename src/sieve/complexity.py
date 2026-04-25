"""Complexity detection for routing decisions."""

import os
import re
from openai import OpenAI

# Classifier prompt for AI-powered complexity detection
CLASSIFIER_PROMPT = """Rate the complexity of answering this query on a scale of 1-5:
1 = Trivial (simple fact, definition, yes/no)
2 = Easy (short explanation, basic question)
3 = Medium (requires some reasoning or detail)
4 = Hard (multi-step reasoning, analysis, code)
5 = Very Hard (deep expertise, complex problem-solving)

Query: {query}

Respond with ONLY a single number 1-5, nothing else."""

# Fallback keywords for when AI classification is disabled
COMPLEX_KEYWORDS = [
    "analyze", "analyse", "evaluate", "compare", "step by step",
    "explain how", "debug", "refactor", "implement", "architecture",
    "prove", "derive", "comprehensive", "in-depth",
]

SIMPLE_KEYWORDS = [
    "what is", "define", "list", "when was", "who is",
    "translate", "yes or no", "true or false",
]


def estimate_complexity_ai(prompt: str, client: OpenAI) -> float:
    """
    Use AI to estimate query complexity (smarter but costs ~$0.00001 per call).
    
    Returns:
        float: 0.0 = very simple, 1.0 = very complex
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": CLASSIFIER_PROMPT.format(query=prompt[:500])}],
            max_tokens=1,
            temperature=0,
        )
        rating = int(response.choices[0].message.content.strip())
        # Convert 1-5 to 0-1 scale
        return (rating - 1) / 4.0
    except:
        # Fall back to keyword-based detection
        return estimate_complexity_keywords(prompt)


def estimate_complexity_keywords(prompt: str) -> float:
    """
    Estimate complexity using keywords (fast, free, less accurate).
    
    Returns:
        float: 0.0 = very simple, 1.0 = very complex
    """
    prompt_lower = prompt.lower()
    score = 0.5
    
    word_count = len(prompt.split())
    if word_count < 10:
        score -= 0.15
    elif word_count > 100:
        score += 0.15
    elif word_count > 50:
        score += 0.1
    
    for keyword in COMPLEX_KEYWORDS:
        if keyword in prompt_lower:
            score += 0.12
    
    for keyword in SIMPLE_KEYWORDS:
        if keyword in prompt_lower:
            score -= 0.1
    
    if "```" in prompt or re.search(r'def |function |class |import ', prompt):
        score += 0.15
    
    return max(0.0, min(1.0, score))


def estimate_complexity(prompt: str, client: OpenAI | None = None, use_ai: bool = True) -> float:
    """
    Estimate query complexity.
    
    Args:
        prompt: The query to analyze
        client: OpenAI client (required if use_ai=True)
        use_ai: If True, use AI classification (smarter). If False, use keywords (faster).
    
    Returns:
        float: 0.0 = very simple, 1.0 = very complex
    """
    if use_ai and client:
        return estimate_complexity_ai(prompt, client)
    return estimate_complexity_keywords(prompt)


def complexity_to_tier(complexity: float) -> str:
    """Convert complexity score to model tier."""
    if complexity < 0.35:
        return "cheap"
    elif complexity < 0.65:
        return "mid"
    else:
        return "expensive"
