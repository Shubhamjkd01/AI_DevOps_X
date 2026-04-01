import threading
import time
import subprocess
import uvicorn
import sys
from main import app

def run_server():
    # Run the server directly in this script so logs print to the same window!
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")

print("Starting the Backend Server... (You will see the logs below)")
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

print("Waiting 3 seconds for backend to fully boot up...")
time.sleep(3)

print("Triggering mock GitHub webhook failure...")
try:
    subprocess.run([sys.executable, "trigger.py"], check=True)
except Exception as e:
    print("Trigger failed:", e)

print("\n=======================================================")
print("The AI Agents are now processing the failure!")
print("Please watch the logs below as Gemini writes the code")
print("and the GitHub Agent creates the Pull Request...")
print("=======================================================\n")

# Wait a sufficient amount of time to let the AI process and print logs
time.sleep(20)
print("\nProcess finished! Please go check the Pull Requests tab on your GitHub repository.")
