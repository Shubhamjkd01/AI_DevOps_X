import os
import logging
from google import genai

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

def get_embedding(text: str) -> list[float]:
    if not client:
        return [0.0] * 768
    try:
        response = client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )
        return response.embeddings[0].values
    except Exception as e:
        logger.error(f"Embedding error: {e}")
        return [0.0] * 768

def query_llm(prompt: str) -> str:
    """
    Queries Google Gemini's API. If no key is provided, falls back to a mock for testing.
    """
    if not client:
        logger.warning("No GEMINI_API_KEY found, returning mock LLM response.")
        if "Analyzer" in prompt or "root cause" in prompt.lower():
            return "Root cause: Syntax error in app/main.py at line 42 due to missing colon."
        elif "Fix" in prompt or "corrected code" in prompt.lower():
            return "def fixed_function():\n    pass # added colon"
        elif "PR" in prompt or "Pull Request" in prompt.lower():
            return "Fix syntax error in app/main.py"
        return "LLM Mock Response"

    logger.info("Querying Google Gemini API...")
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        return "Error calling LLM"
