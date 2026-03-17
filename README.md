# LLM Security Gateway

This project implements a security gateway for Large Language Models.

Features:

- Prompt injection detection
- PII detection using Presidio
- Custom recognizer for API keys
- Context-aware scoring
- Composite entity detection
- Policy engine (Allow / Mask / Block)
- Latency measurement
- Ollama LLM integration

## Installation

pip install -r requirements.txt

## Run

python main.py

## Project Structure

modules/
custom_recognizers/
main.py
requirements.txt

## Architecture

See architecture.png

## Author

Muaz
