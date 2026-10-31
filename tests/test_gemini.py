import os
from dotenv import load_dotenv
load_dotenv(override=True)
from google import genai

key = os.getenv("GEMINI_API_KEY")
print("Key length:", len(key) if key else 0)

try:
    client = genai.Client(api_key=key)
    print("Testing gemini-pro...")
    response = client.models.generate_content(
        model="gemini-pro",
        contents="Say exactly 'SUCCESS'"
    )
    print("gemini-pro SUCCESS! Response:", response.text)
except Exception as e:
    print("gemini-pro FAILED:", str(e))

try:
    print("Testing gemini-1.5-pro...")
    response = client.models.generate_content(
        model="gemini-1.5-pro",
        contents="Say exactly 'SUCCESS'"
    )
    print("gemini-1.5-pro SUCCESS! Response:", response.text)
except Exception as e:
    print("gemini-1.5-pro FAILED:", str(e))
