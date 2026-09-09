import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
#MODEL = "gemma4:12b"
MODEL = "qwen2.5:3b"
def ask_model(prompt):
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    })
    response.raise_for_status()
    return response.json()["response"]