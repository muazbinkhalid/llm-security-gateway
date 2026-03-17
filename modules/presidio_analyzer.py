from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Register custom recognizers (if any)
try:
    from custom_recognizers.api_key_recognizer import api_key_recognizer
except Exception:
    api_key_recognizer = None


analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

if api_key_recognizer is not None:
    try:
        analyzer.registry.add_recognizer(api_key_recognizer)
    except Exception:
        # If registration fails, continue — analyzer still works for built-ins
        pass


def detect_pii(text: str):
    """Return analyzer results for the given text."""
    if not text:
        return []

    results = analyzer.analyze(
        text=text,
        language="en",
    )

    # Simple context-aware boost example: if 'contact' near a phone number, bump score
    lower = text.lower()
    for r in results:
        if r.entity_type and "PHONE" in r.entity_type.upper():
            if "contact" in lower:
                # presidio's result objects are dataclasses; adjust score if possible
                try:
                    r.score = min(1.0, r.score + 0.2)
                except Exception:
                    pass

    return results


def mask_pii(text: str) -> str:
    """Return anonymized text according to detected PII entities."""
    results = detect_pii(text)

    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
    )

    return anonymized.text


def detect_sensitive_profile(text: str):
    """Detect composite entity: name + phone together -> 'SENSITIVE_PROFILE'.

    This function inspects analyzer results and returns True if a PERSON/NAME
    entity appears near a PHONE_NUMBER entity.
    """
    results = detect_pii(text)
    persons = [r for r in results if r.entity_type and r.entity_type.upper() in ("PERSON", "NAME")]
    phones = [r for r in results if r.entity_type and "PHONE" in r.entity_type.upper()]

    # If both present, check textual proximity (naive: index overlap by span)
    for p in persons:
        for ph in phones:
            # If spans exist, check distance
            try:
                if abs(p.start - ph.start) < 40:
                    return True
            except Exception:
                continue

    return False
