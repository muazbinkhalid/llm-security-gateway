# LLM Security Gateway (minimal)

Installation and quick run instructions

1) Create and activate a Python virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Install Python requirements (Presidio analyzer + anonymizer):

```bash
pip install -r requirements.txt
```

Note: Ollama (the local model runner) is not a Python package in many installs. To install Ollama on macOS you can use Homebrew:

```bash
brew install ollama
```

Alternatively, follow instructions at https://ollama.com/docs for your platform.

3) Run the main pipeline:

```bash
python3 main.py
```

This will ask for a prompt, run injection detection, PII detection/masking, apply policy, and — if Ollama is installed — run the `llama3` model.

Files created:
- `modules/injection_detector.py` — simple rule-based injection scoring
- `modules/presidio_analyzer.py` — wraps Presidio analyzer & anonymizer, registers custom recognizer
- `modules/policy_engine.py` — simple policy decision function
- `modules/latency.py` — helper to measure latency
- `custom_recognizers/api_key_recognizer.py` — example API key recognizer
- `main.py` — pipeline runner
