import requests
import json
import os
import sys

print("=== 1. Checking OpenEnv API ===")
try:
    resp = requests.post("http://localhost:8080/api/v1/env/reset")
    print(f"/reset Response ({resp.status_code}):", json.dumps(resp.json(), indent=2))
except Exception as e:
    print(f"Error calling /reset: {e}")

print("=== 2. Checking Fast API Root ===")
try:
    resp = requests.post("http://localhost:8080/reset")
    print(f"Root /reset Response ({resp.status_code}):", json.dumps(resp.json(), indent=2))
except Exception as e:
    print(f"Error calling root /reset: {e}")

print("=== 3. Testing Hugging Face LLM Interface directly ===")
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
    api_key = os.getenv("HF_TOKEN")
    base_url = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
    model_name = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
    
    if not api_key:
        print("HF_TOKEN is missing!")
    else:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=base_url)
        print(f"Calling OpenAI SDK with model {model_name} on {base_url}...")
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Reply with exactly the word: PING"}],
            temperature=0.2
        )
        print("LLM Response:", response.choices[0].message.content)
except Exception as e:
    print(f"Error calling LLM directly: {e}")
