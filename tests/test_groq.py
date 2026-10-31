import requests

groq_key = "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"
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {groq_key}",
    "Content-Type": "application/json"
}
data = {
    "model": "llama-3.1-8b-instant",
    "messages": [{"role": "user", "content": "print exactly 'SUCCESS'"}]
}
response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())
