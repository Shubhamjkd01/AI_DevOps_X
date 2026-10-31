import os
from dotenv import load_dotenv
load_dotenv(override=True)
import google.generativeai as genai

key = os.getenv("GEMMA_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
print("Key length:", len(key) if key else 0)

if not key:
    print("No GEMMA_API_KEY found.")
else:
    try:
        genai.configure(api_key=key)
        model_name = os.getenv("GEMMA_MODEL_NAME", "models/gemma-4-26b-a4b-it")
        print(f"Testing Gemma ({model_name})...")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say exactly 'SUCCESS'")
        print("Gemma SUCCESS! Response:", response.text.strip())
    except Exception as e:
        print("Gemma FAILED:", str(e))
