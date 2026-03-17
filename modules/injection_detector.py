patterns = {
    "ignore previous instructions": 3,
    "reveal system prompt": 4,
    "bypass safety": 3,
    "act as developer": 2,
    "print hidden prompt": 4,
}

THRESHOLD = 5


def detect_injection(prompt: str) -> int:
    """Simple rule-based injection scoring.

    Returns an integer score. Higher means more likely an injection.
    """
    score = 0

    lower = (prompt or "").lower()

    for pattern, value in patterns.items():
        if pattern in lower:
            score += value

    return score
