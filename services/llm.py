import os
import logging
from openai import OpenAI
import groq
import google.generativeai as genai

logger = logging.getLogger(__name__)

def get_client() -> OpenAI:
    """
    Returns an OpenAI client configured for the Hugging Face router.
    """
    api_key = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
    if not api_key:
        return None
    return OpenAI(api_key=api_key, base_url=base_url)

def get_embedding(text: str) -> list[float]:
    # We bypass semantic search embedding strictly for OpenEnv Hackathon
    return [0.0] * 768

def query_llm(prompt: str, llm_priority: str = None) -> str:
    """
    Primary inference call using the Hugging Face router and OpenAI SDK.
    """
    if llm_priority == "Offline / Failover Mode":
        return get_fallback_fix(prompt)

    api_key = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
    model_name = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

    if not api_key:
        logger.warning("No HF_TOKEN or API Key found, returning mock LLM response.")
        return get_mock_response(prompt)

    try:
        logger.info(f"Querying Hugging Face Router (Model: {model_name})...")
        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"HF Router LLM call failed: {e}")
        return get_fallback_fix(prompt)

# LangSmith Observability Wrapper
if os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true":
    from langsmith import traceable
    query_llm = traceable(run_type="llm", name="Groq/OpenAI Inference")(query_llm)
