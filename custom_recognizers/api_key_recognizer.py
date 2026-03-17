from presidio_analyzer import PatternRecognizer, Pattern


pattern = Pattern(
    name="api_key",
    regex=r"sk-[A-Za-z0-9]{20,}",
    score=0.85,
)

api_key_recognizer = PatternRecognizer(
    supported_entity="API_KEY",
    patterns=[pattern],
)
