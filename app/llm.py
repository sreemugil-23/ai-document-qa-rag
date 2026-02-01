import subprocess

MODEL_NAME = "tinyllama:1.1b"  # or llama3.2:3b if available


def ask_llm(prompt):
    result = subprocess.run(
        ["ollama", "run", MODEL_NAME, prompt],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    output = result.stdout.decode("utf-8", errors="ignore").strip()
    error_output = result.stderr.decode("utf-8", errors="ignore").strip()

    return output if output else error_output
