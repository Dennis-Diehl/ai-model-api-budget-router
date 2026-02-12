"""Schritt 6: LLM API Client.

Hier kommunizierst du mit der Groq API, um Antworten von Language Models zu erhalten.
Der Client ist asynchron (async/await), weil HTTP-Requests Zeit brauchen.

Lernziele:
- async/await in Python
- HTTP POST Requests mit httpx
- API-Authentifizierung mit Bearer Token
- Environment Variables fuer Secrets
- JSON Response parsen

Groq API Docs: https://console.groq.com/docs/api-reference#chat-create
"""

import os

import httpx
from dotenv import load_dotenv

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def get_api_key() -> str:
    """Hole den Groq API Key aus den Environment Variables.

    TODO:
    - Lies "GROQ_API_KEY" aus os.getenv()
    - Wenn nicht gesetzt: raise RuntimeError("GROQ_API_KEY environment variable is not set.")
    - Sonst: return den Key
    """
    raise NotImplementedError


async def call_llm(model_id: str, prompt: str, max_tokens: int = 1024) -> dict:
    """Sende einen Prompt an die Groq API und gib die Antwort zurueck.

    TODO:
    1. Hole den API Key mit get_api_key()
    2. Erstelle die Headers:
       - "Authorization": "Bearer {api_key}"
       - "Content-Type": "application/json"
    3. Erstelle den Payload (Body):
       {
           "model": model_id,
           "messages": [{"role": "user", "content": prompt}],
           "max_tokens": max_tokens,
       }
    4. Erstelle einen httpx.AsyncClient mit timeout=60.0
       -> async with httpx.AsyncClient(timeout=60.0) as client:
    5. Sende POST Request:
       -> response = await client.post(GROQ_API_URL, headers=headers, json=payload)
       -> response.raise_for_status()  # Wirft Exception bei Fehler
    6. Parse die JSON-Antwort:
       -> data = response.json()
       -> content = data["choices"][0]["message"]["content"]
       -> input_tokens = data["usage"]["prompt_tokens"]
       -> output_tokens = data["usage"]["completion_tokens"]
    7. Return ein Dictionary:
       {
           "content": content,
           "input_tokens": input_tokens,
           "output_tokens": output_tokens,
       }

    Args:
        model_id: Die ID des Modells (z.B. "llama-3.3-70b-versatile").
        prompt: Der User-Prompt.
        max_tokens: Maximale Anzahl Output-Tokens (default: 1024).

    Returns:
        Dict mit "content", "input_tokens", "output_tokens".
    """
    raise NotImplementedError
