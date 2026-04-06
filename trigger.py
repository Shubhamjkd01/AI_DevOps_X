import requests
import random
import sys

fail_type = sys.argv[1] if len(sys.argv) > 1 else "syntax"

# Single Repo Target
selected_repo = "Shubhamjkd01/Nursesycn"

print("\n--- AI DevOps Webhook Simulator ---")
print(f"Auto-targeting repository: {selected_repo}\n")

url = "http://localhost:7860/api/v1/webhook/github"
headers = {"X-GitHub-Event": "workflow_run"}
run_id = random.randint(10000, 99999)

data = {
    "action": "completed",
    "workflow_run": {
        "id": run_id,
        "status": "completed",
        "conclusion": "failure",
        "logs": "Error: IndentationError in main.py line 42\n    def process_request(req)\n    ^\nIndentationError: expected an indented block"
    },
    "repository": {
        "full_name": selected_repo
    },
    "mock_fail_type": fail_type # Custom payload for local simulator
}

try:
    response = requests.post(url, headers=headers, json=data)
    print("Status:", response.status_code)
    print(f"Triggered Fix for: {fail_type.upper()} Error")
    print("Response:", response.text)
except requests.exceptions.ConnectionError:
    print("Error: The server is not running on http://localhost:7860 yet.")
