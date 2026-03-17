def policy_decision(injection_score, pii_entities):

    if injection_score >= 5:
        return "BLOCK"

    if len(pii_entities) > 0:
        return "MASK"

    return "ALLOW"
