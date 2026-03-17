from modules.injection_detector import detect_injection
from modules.presidio_analyzer import detect_pii, mask_pii, detect_sensitive_profile
from modules.policy_engine import policy_decision
from modules.latency import measure_latency
import subprocess
import shutil


def call_ollama(prompt: str):
    """Call Ollama if available. Returns stdout string or a message explaining it's missing."""
    if shutil.which("ollama") is None:
        return "Ollama not found on PATH. Install Ollama or run the model locally."

    # Run ollama and pass prompt via stdin
    try:
        resp = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt,
            capture_output=True,
            text=True,
            check=False,
        )
        return resp.stdout + (resp.stderr or "")
    except Exception as e:
        return f"Error running Ollama: {e}"


def main():
    prompt = input("Enter prompt: ")

    score = detect_injection(prompt)

    pii_results, pii_latency = measure_latency(detect_pii, prompt)

    decision = policy_decision(score, pii_results)

    print("Injection Score:", score)
    print("PII Entities:", pii_results)
    print("Decision:", decision)
    print(f"PII detection latency: {pii_latency:.2f} ms")

    if decision == "BLOCK":
        print("Request Blocked")
        return

    if decision == "MASK":
        prompt = mask_pii(prompt)
        print("Masked Prompt:", prompt)

    # Show composite detection example
    if detect_sensitive_profile(prompt):
        print("Composite sensitive profile detected (Name + Phone).")

    # If allowed, call Ollama (if installed)
    output = call_ollama(prompt)
    print("Model output (or message):\n", output)


if __name__ == "__main__":
    main()
