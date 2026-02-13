"""LLM API Client — communicates with the Groq API to get AI model responses.

Uses async HTTP requests (httpx) because network calls take time.
While waiting for Groq's response, the server can handle other requests.

Groq API Docs: https://console.groq.com/docs/api-reference#chat-create
"""

import os

import httpx
from dotenv import load_dotenv

# Load .env file into os.environ so we can read secrets like GROQ_API_KEY
load_dotenv()

# The Groq API endpoint for chat completions (same format as OpenAI)
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def get_api_key() -> str:
    """Read the Groq API key from environment variables.

    Returns:
        The API key string.

    Raises:
        RuntimeError: If GROQ_API_KEY is not set in the environment.
    """
    # Read the API key from environment variables (loaded from .env by dotenv)
    api_key = os.getenv("GROQ_API_KEY")
    # Fail early with a clear error if the key is missing
    if not api_key:
        raise RuntimeError("GROQ_API_KEY environment variable is not set.")
    return api_key


async def call_llm(model_id: str, prompt: str, max_tokens: int = 1024) -> dict:
    """Send a prompt to the Groq API and return the response.

    The Groq server returns JSON like this:

        {
          "choices": [
            {
              "message": {
                "content": "The AI response text..."  <-- we extract this
              }
            }
          ],
          "usage": {
            "prompt_tokens": 24,       <-- we extract this (input cost)
            "completion_tokens": 87    <-- we extract this (output cost)
          }
        }

    We only keep the 3 fields we need: content, input_tokens, output_tokens.

    Args:
        model_id: The model to use (e.g. "llama-3.3-70b-versatile").
        prompt: The user's message to send to the model.
        max_tokens: Maximum number of tokens the model may generate (default: 1024).

    Returns:
        Dict with "content", "input_tokens", "output_tokens".
    """
    # --- 1. Authentication: get the API key ---
    api_key = get_api_key()

    # --- 2. Headers: metadata sent with every request ---
    headers = {
        "Authorization": f"Bearer {api_key}",  # "Bearer" = standard prefix for API tokens
        "Content-Type": "application/json",     # tells the server we're sending JSON
    }

    # --- 3. Payload: the actual data we send (our "letter") ---
    payload = {
        "model": model_id,                                      # which AI model to use
        "messages": [{"role": "user", "content": prompt}],      # chat history (just 1 message)
        "max_tokens": max_tokens,                                # limit response length
    }

    # --- 4. Send the request and wait for the response ---
    # "async with" opens a connection and auto-closes it when done
    # "timeout=60.0" means: give up after 60 seconds if no response
    async with httpx.AsyncClient(timeout=60.0) as client:
        # "await" = pause here until the response arrives (non-blocking)
        response = await client.post(GROQ_API_URL, headers=headers, json=payload)
        # Raise an error if the server returned an error status (401, 500, etc.)
        response.raise_for_status()

        # --- 5. Parse the JSON response and extract what we need ---
        data = response.json()
        content = data["choices"][0]["message"]["content"]   # the AI's answer
        input_tokens = data["usage"]["prompt_tokens"]        # tokens used for our prompt
        output_tokens = data["usage"]["completion_tokens"]   # tokens the AI generated

        return {
            "content": content,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        }
