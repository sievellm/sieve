"""Complexity detection for routing decisions."""

import re

# Keywords that suggest complex reasoning is needed
COMPLEX_KEYWORDS = [
    # Analysis
    "analyze", "analyse", "evaluate", "assess", "compare", "contrast",
    # Step-by-step
    "step by step", "step-by-step", "explain how", "walk me through",
    "break down", "detailed explanation",
    # Reasoning
    "why does", "why is", "reason", "reasoning", "logic", "deduce",
    "infer", "conclude", "implications",
    # Code
    "debug", "refactor", "optimize", "implement", "architecture",
    "design pattern", "algorithm",
    # Math
    "prove", "derive", "calculate complex", "solve for",
    # Writing
    "write a detailed", "comprehensive", "in-depth", "thorough",
]

# Keywords suggesting simple tasks
SIMPLE_KEYWORDS = [
    "what is", "define", "list", "name", "when was", "who is",
    "translate", "convert", "format", "summarize briefly",
    "yes or no", "true or false",
]


def estimate_complexity(prompt: str) -> float:
    """
    Estimate query complexity on a 0-1 scale.
    
    Returns:
        float: 0.0 = very simple, 1.0 = very complex
    """
    prompt_lower = prompt.lower()
    score = 0.5  # Start neutral
    
    # Length factor (longer prompts tend to be more complex)
    word_count = len(prompt.split())
    if word_count < 10:
        score -= 0.15
    elif word_count > 100:
        score += 0.15
    elif word_count > 50:
        score += 0.1
    
    # Check for complex keywords
    for keyword in COMPLEX_KEYWORDS:
        if keyword in prompt_lower:
            score += 0.12
    
    # Check for simple keywords
    for keyword in SIMPLE_KEYWORDS:
        if keyword in prompt_lower:
            score -= 0.1
    
    # Question marks suggest simpler Q&A (usually)
    question_count = prompt.count("?")
    if question_count == 1 and word_count < 20:
        score -= 0.1
    
    # Code blocks suggest technical complexity
    if "```" in prompt or re.search(r'def |function |class |import ', prompt):
        score += 0.15
    
    # Multiple parts/requirements
    if re.search(r'\d+\.\s|\d+\)\s|first.*second.*third', prompt_lower):
        score += 0.1
    
    # Clamp to 0-1 range
    return max(0.0, min(1.0, score))


def complexity_to_tier(complexity: float) -> str:
    """Convert complexity score to model tier."""
    if complexity < 0.35:
        return "cheap"
    elif complexity < 0.65:
        return "mid"
    else:
        return "expensive"
