import logging
logging.basicConfig(level=logging.INFO)
from dotenv import load_dotenv
load_dotenv()

from agents.orchestrator import handle_workflow_failure

print("Starting debug run...")
try:
    pr_url = handle_workflow_failure("Shubhamjkd01/Nursesycn", 1234)
    print("Debug run complete. PR URL:", pr_url)
except Exception as e:
    print("Debug run crashed:", e)
