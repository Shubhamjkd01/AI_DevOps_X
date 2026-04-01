import os
from dotenv import load_dotenv
load_dotenv(override=True)
from google import genai

key = os.getenv("GEMINI_API_KEY")
try:
    client = genai.Client(api_key=key)
    for m in client.models.list_models():
        print(m.name)
except Exception as e:
    print("Failed to list models:", str(e))
