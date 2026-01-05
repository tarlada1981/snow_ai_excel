import subprocess

def ask_ollama(prompt):
    result = subprocess.run(
        ["ollama", "run", "llama3.1"],
        input=prompt,
        text=True,
        capture_output=True
    )
    return result.stdout.strip()
