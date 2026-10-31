"""
Model Verification Script for Google Gemma 4 Hackathon Compliance.
Lists all available Gemma models for the configured API key and confirms active model.
"""
import os
import sys
from dotenv import load_dotenv

# Ensure parent directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(override=True)

def check_gemma_models():
    print("=" * 65)
    print("[*] GOOGLE GEMMA 4 MODEL VERIFICATION UTILITY")
    print("=" * 65)

    api_key = os.getenv("GEMMA_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("\n[!] ERROR: No API key found in .env!")
        print("Please set GEMMA_API_KEY in github_agent_backend/.env.")
        print("Get your free key from: https://aistudio.google.com/app/apikey\n")
        return False

    masked_key = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else "***"
    print(f"[*] API Key detected: {masked_key}")

    configured_model = os.getenv("GEMMA_MODEL_NAME", "models/gemma-4-26b-a4b-it")
    print(f"[*] Configured Target Model (GEMMA_MODEL_NAME): {configured_model}")

    print("\n[*] Querying Google AI Studio for available Gemma models...")
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        gemma_models = []
        for model in genai.list_models():
            if "gemma" in model.name.lower():
                gemma_models.append(model)

        if not gemma_models:
            print("[!] No Gemma models found for this API key.")
            return False

        print(f"\n[+] Found {len(gemma_models)} accessible Gemma model(s):\n")
        active_found = False
        for m in gemma_models:
            is_active = (m.name == configured_model) or (m.name.split("/")[-1] == configured_model.split("/")[-1])
            if is_active:
                active_found = True
                marker = "[ACTIVE PRIMARY]"
            else:
                marker = "[Available]     "

            methods = ", ".join(m.supported_generation_methods)
            multimodal = "Yes (Text + Image Input)" if "generateContent" in methods else "Text Only"
            print(f" {marker} {m.name}")
            print(f"     DisplayName: {m.display_name}")
            print(f"     Multimodal:  {multimodal}")
            print(f"     Methods:     {methods}\n")

        print("-" * 65)
        if active_found:
            print(f"[SUCCESS] Active model `{configured_model}` is ready and operational!")
        else:
            print(f"[INFO] Recommended Model: `{gemma_models[0].name}` (Update GEMMA_MODEL_NAME in .env)")
        print("=" * 65)
        return True

    except Exception as e:
        print(f"\n[!] Error connecting to Google AI Studio API: {e}")
        return False

if __name__ == "__main__":
    success = check_gemma_models()
    sys.exit(0 if success else 1)
