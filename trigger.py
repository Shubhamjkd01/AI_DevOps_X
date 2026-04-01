import requests
import random
import sys

fail_type = sys.argv[1] if len(sys.argv) > 1 else "syntax"

# Multi-Repo Testing List
REPOS = [
    "Shubhamjkd01/Nursesycn",
    "Shubhamjkd01/Edusential_collabration",
    "Shubhamjkd01/edusentinel-v3"
]

print("\n--- AI DevOps Webhook Simulator ---")
print("Select target repository to simulate a CI failure on:")
for i, repo in enumerate(REPOS):
    print(f"[{i+1}] {repo}")
print("[0] Random Repository")

choice = input("Enter your choice (0-3) [default: 0]: ").strip()

if choice.isdigit() and 1 <= int(choice) <= len(REPOS):
    selected_repo = REPOS[int(choice)-1]
else:
    selected_repo = random.choice(REPOS)
    print(f"Randomly auto-selected: {selected_repo}\n")

url = "http://localhost:8080/api/v1/webhook/github"
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
    print("Error: The server is not running on http://localhost:8080 yet.")
