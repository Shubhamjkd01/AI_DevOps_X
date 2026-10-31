import os
import logging
import hashlib
from typing import Optional, Tuple, Union
from dotenv import load_dotenv
load_dotenv(override=True)
from openai import OpenAI

logger = logging.getLogger(__name__)

# --- ACTIVE MODEL DEFINITIONS ---
DEFAULT_GEMMA4_MODEL = "models/gemma-4-26b-a4b-it"

# Only open-weight Gemma 4 models allowed
GEMMA4_CANDIDATES = [
    os.getenv("GEMMA_MODEL_NAME", DEFAULT_GEMMA4_MODEL),
    "models/gemma-4-26b-a4b-it",
    "models/gemma-4-31b-it",
    "gemma-4-26b-a4b-it",
    "gemma-4-31b-it",
]

# Open-weight fallbacks for secondary providers
FALLBACK_OPEN_MODELS = [
    "google/gemma-4-26b-it",
    "google/gemma-4-31b-it",
]

# --- CONTEXT OBJECT FOR TRACKING MODEL USAGE ---
class LLMContext:
    def __init__(self):
        self._last_model_used: Optional[str] = None

    def set_model_used(self, model: str):
        self._last_model_used = model

    def get_model_used(self) -> str:
        return self._last_model_used or os.getenv("GEMMA_MODEL_NAME", DEFAULT_GEMMA4_MODEL)

llm_context = LLMContext()

def get_last_model_used() -> str:
    """Returns the exact model identifier that answered the most recent LLM query."""
    return llm_context.get_model_used()

def get_active_model_name() -> str:
    """Returns the primary Gemma 4 model configured for the system."""
    return os.getenv("GEMMA_MODEL_NAME", DEFAULT_GEMMA4_MODEL)

class LLMResponse(str):
    """
    Subclass of str that preserves full backwards compatibility as a string,
    while also exposing .model_used attribute.
    """
    def __new__(cls, content: str, model_used: str):
        obj = super().__new__(cls, content)
        obj.model_used = model_used
        return obj

    def __init__(self, content: str, model_used: str):
        self.model_used = model_used


# --- UTILITIES ---

def get_mock_response(prompt: str) -> str:
    """Returns a deterministic, high-quality mock fix for offline testing."""
    if "Analyzer Agent" in prompt and "priority" in prompt.lower():
        return '{"priority": "HIGH", "confidence": 0.92, "file_path": "backend/main.py", "error": "SyntaxError: expected colon after function definition", "why": "Missing colon at the end of a function definition caused the parser to fail", "failure_category": "SyntaxError"}'
    
    if "JUDGE" in prompt.upper() and "score" in prompt.lower():
        return '{"score": 0.85, "explanation": "The patch correctly addresses the syntax error by adding the missing colon. The fix is minimal and targeted."}'
    
    if "Explain the changes" in prompt:
        return "Fixed the missing colon at the end of the function definition on the affected line to restore valid Python syntax."
    
    if "PR Agent" in prompt or "PR title" in prompt.lower():
        return "## Automated CI/CD Fix\n\nThis PR resolves a syntax error detected in the CI pipeline.\n\n**Root Cause:** Missing `:` after function signature\n**Impact:** Build failure / Import error\n**Resolution:** Added required colon"
    
    if "Predictor Agent" in prompt:
        return "Prediction: Safe\nReason: No obvious syntax errors or version mismatches detected in commit diff.\nConfidence: 85%"
    
    if "Self-Improvement" in prompt or "pipeline_bug" in prompt.lower():
        return '{"is_pipeline_bug": false, "description": "The failure is caused by code logic, not a pipeline infrastructure bug."}'
    
    if "Adversarial" in prompt:
        return '[{"title": "Compound Syntax + Import Error", "description": "Missing colon combined with circular import", "primary_failure": "SyntaxError in main.py", "secondary_failure": "ImportError in utils.py", "red_herring": "DeprecationWarning", "mock_logs": "SyntaxError: expected colon"}]'
    
    if "Fix Generator" in prompt or "corrected code" in prompt.lower() or "raw code" in prompt.lower():
        return (
            "from flask import Flask, jsonify, request\n"
            "import logging\n\n"
            "app = Flask(__name__)\n"
            "logger = logging.getLogger(__name__)\n\n"
            "def process_request(req):\n"
            "    \"\"\"Process incoming request and return result.\"\"\"\n"
            "    logger.info(f'Processing request: {req}')\n"
            "    return {'status': 'success', 'data': req}\n\n"
            "@app.route('/health')\n"
            "def health():\n"
            "    return jsonify({'status': 'ok'})\n\n"
            "if __name__ == '__main__':\n"
            "    app.run(host='0.0.0.0', port=5000)\n"
        )
    
    if "SyntaxError" in prompt or "main.py" in prompt:
        return (
            "from flask import Flask, jsonify, request\n"
            "import logging\n\n"
            "app = Flask(__name__)\n"
            "logger = logging.getLogger(__name__)\n\n"
            "def process_request(req):\n"
            "    return {'status': 'success', 'data': req}\n\n"
            "@app.route('/health')\n"
            "def health():\n"
            "    return jsonify({'status': 'ok'})\n\n"
            "if __name__ == '__main__':\n"
            "    app.run(host='0.0.0.0', port=5000)\n"
        )
    
    if "requirements.txt" in prompt:
        return "flask>=3.0.0\nrequests>=2.31.0\npydantic>=2.6.1\nnumpy>=1.24.0\n"
        
    return '{"action_type": "analyze", "file_path": "root", "patch_content": ""}'


def get_embedding(text: str) -> list:
    """Generate a deterministic pseudo-embedding based on text hash for FAISS L2 matching."""
    h = hashlib.sha256(text.encode()).hexdigest()
    embedding = []
    for i in range(0, min(len(h) * 2, 768)):
        char_idx = i % len(h)
        val = (int(h[char_idx], 16) - 8) / 8.0
        embedding.append(val)
    while len(embedding) < 768:
        embedding.append(0.0)
    return embedding[:768]


# --- PRIMARY GEMMA 4 INFERENCE VIA GEMINI API ---

def _try_gemma(prompt: str) -> Tuple[str, str]:
    """
    Primary inference using Google's open-weights Gemma 4 models via the Gemini API.
    Uses GEMMA_MODEL_NAME env var, then cascades through available Gemma 4 models.
    Does NOT use non-open models (no Gemini 1.5, no GPT).
    """
    gemini_key = os.getenv("GEMMA_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not gemini_key:
        raise ValueError("No GEMMA_API_KEY, GEMINI_API_KEY, or GOOGLE_API_KEY configured")

    import google.generativeai as genai
    genai.configure(api_key=gemini_key)

    configured_model = os.getenv("GEMMA_MODEL_NAME", DEFAULT_GEMMA4_MODEL)
    candidates = [configured_model] + [m for m in GEMMA4_CANDIDATES if m != configured_model]

    last_err = None
    for model_name in candidates:
        # Strict filter: only allow Gemma 4 models
        if "gemma-4" not in model_name.lower():
            logger.warning(f"Rejecting non-Gemma-4 candidate model: {model_name}")
            continue

        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            if response and response.text and response.text.strip():
                logger.info(f"LLM: Successfully generated content with Gemma 4 model ({model_name})")
                return response.text, model_name
        except Exception as e:
            last_err = e
            logger.warning(f"Gemma 4 model ({model_name}) failed: {e}. Trying next Gemma 4 candidate...")
            continue

    raise RuntimeError(f"All Gemma 4 models via Gemini API failed: {last_err}")


def _try_open_hf(client: OpenAI, model_name: str, prompt: str, timeout: float = 25.0) -> str:
    """Try an open-weight model via HF Router."""
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1024,
        timeout=timeout
    )
    content = response.choices[0].message.content
    if not content or not content.strip():
        raise ValueError("Empty response from model")
    return content


def _try_open_groq(prompt: str) -> Tuple[str, str]:
    """Try open-weight Gemma model via Groq."""
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        raise ValueError("No GROQ_API_KEY")
    import groq as groq_lib
    client = groq_lib.Groq(api_key=groq_key)
    model = os.getenv("GROQ_MODEL", "gemma-4-31b-it")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1024
    )
    return response.choices[0].message.content, f"Groq/{model}"


# --- MULTIMODAL SCREENSHOT TRIAGE ---

def analyze_screenshot_with_gemma(image_input, prompt: str = "Analyze this CI/CD failure screenshot and identify the root cause:") -> Tuple[str, str]:
    """
    Multimodal analysis of CI/CD failure screenshots using Gemma 4.
    Accepts PIL Image, bytes, or file path.
    """
    gemini_key = os.getenv("GEMMA_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not gemini_key:
        raise ValueError("No GEMMA_API_KEY configured for multimodal analysis")

    import google.generativeai as genai
    from PIL import Image
    import io

    genai.configure(api_key=gemini_key)
    model_name = os.getenv("GEMMA_MODEL_NAME", DEFAULT_GEMMA4_MODEL)
    model = genai.GenerativeModel(model_name)

    if isinstance(image_input, (bytes, bytearray)):
        image = Image.open(io.BytesIO(image_input))
    elif isinstance(image_input, str):
        image = Image.open(image_input)
    else:
        image = image_input

    response = model.generate_content([prompt, image])
    text = response.text if response and response.text else "Unable to extract text from screenshot."
    logger.info(f"LLM answered by: {model_name} (Multimodal Screenshot Analysis)")
    llm_context.set_model_used(model_name)
    return text, model_name


# --- CORE INFERENCE DISPATCHER ---

def query_llm(prompt: str, llm_priority: str = None, return_tuple: bool = False) -> Union[str, Tuple[str, str]]:
    """
    Primary verifiable inference dispatcher for Gemma 4.
    
    Logging guarantee:
    Logs 'LLM answered by: <model>' on every single call.
    
    Cascading policy:
    1. Google Gemma 4 (via Gemini API) - Primary verified engine.
    2. Open-weight Groq / Hugging Face fallback (strictly open-weights).
    3. Mock fallback ONLY if TEST_MODE=true or llm_priority=='Offline / Failover Mode'.
    4. If all fail and not in TEST_MODE, aborts without opening a PR.
    """
    test_mode = os.getenv("TEST_MODE", "false").lower() == "true"
    
    # Offline override (only in explicit offline mode or TEST_MODE)
    if llm_priority == "Offline / Failover Mode" or (test_mode and not os.getenv("GEMMA_API_KEY") and not os.getenv("GEMINI_API_KEY")):
        model_used = "mock-offline-deterministic"
        logger.info(f"LLM answered by: {model_used}")
        llm_context.set_model_used(model_used)
        resp_text = get_mock_response(prompt)
        return (resp_text, model_used) if return_tuple else LLMResponse(resp_text, model_used)

    # --- Cascade 1: Primary Google Gemma 4 via Gemini API ---
    if os.getenv("GEMMA_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
        try:
            logger.info("LLM Cascade [1/3]: Trying Google Gemma 4 via Gemini API...")
            text, model_used = _try_gemma(prompt)
            logger.info(f"LLM answered by: {model_used}")
            llm_context.set_model_used(model_used)
            return (text, model_used) if return_tuple else LLMResponse(text, model_used)
        except Exception as e:
            logger.error(f"LLM Cascade [1/3] FAILED (Gemma 4 via Gemini API): {e}")

    # --- Cascade 2: Open-weights Groq fallback ---
    if os.getenv("GROQ_API_KEY"):
        try:
            logger.info("LLM Cascade [2/3]: Trying open-weights Groq fallback...")
            text, model_used = _try_open_groq(prompt)
            logger.info(f"LLM answered by: {model_used}")
            llm_context.set_model_used(model_used)
            return (text, model_used) if return_tuple else LLMResponse(text, model_used)
        except Exception as e:
            logger.warning(f"LLM Cascade [2/3] FAILED (Groq): {e}")

    # --- Cascade 3: Open-weights Hugging Face Router ---
    api_key = os.getenv("HF_TOKEN")
    if api_key:
        base_url = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
        client = OpenAI(api_key=api_key, base_url=base_url)
        for model_name in FALLBACK_OPEN_MODELS:
            try:
                logger.info(f"LLM Cascade [3/3]: Trying open-weight HF model {model_name}...")
                text = _try_open_hf(client, model_name, prompt)
                model_used = f"HF/{model_name}"
                logger.info(f"LLM answered by: {model_used}")
                llm_context.set_model_used(model_used)
                return (text, model_used) if return_tuple else LLMResponse(text, model_used)
            except Exception as e:
                logger.warning(f"HF model {model_name} failed: {e}")

    # --- Abort or Mock (Strict Guard) ---
    if test_mode:
        model_used = "mock-test-mode"
        logger.warning("All LLM providers failed. TEST_MODE=true active: Using mock response.")
        logger.info(f"LLM answered by: {model_used}")
        llm_context.set_model_used(model_used)
        resp_text = get_mock_response(prompt)
        return (resp_text, model_used) if return_tuple else LLMResponse(resp_text, model_used)

    # ABORT RUN: Do not silently use a closed model and do not open a broken PR
    error_msg = "CRITICAL: All Gemma 4 open-model inference providers failed. Aborting pipeline without opening a PR."
    logger.error(error_msg)
    raise RuntimeError(error_msg)
