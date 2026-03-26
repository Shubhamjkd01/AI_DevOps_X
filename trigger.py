import requests

url = "http://localhost:8080/api/v1/webhook/github"
headers = {"X-GitHub-Event": "workflow_run"}
import random
run_id = random.randint(10000, 99999)

data = {
    "action": "completed",
    "workflow_run": {
        "id": run_id,
        "status": "completed",
        "conclusion": "failure"
    },
    "repository": {
        "full_name": "Shubhamjkd01/AI_DevOps_X"
    }
}

try:
    response = requests.post(url, headers=headers, json=data)
    print("Status:", response.status_code)
    print("Response:", response.text)
except requests.exceptions.ConnectionError:
    print("Error: The server is not running on http://localhost:8080 yet.")
