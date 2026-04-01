import sys
import traceback
import logging

logging.basicConfig(level=logging.INFO)
try:
    from agents.orchestrator import handle_workflow_failure
    handle_workflow_failure("Shubhamjkd01/Nursesycn", 12345, "syntax")
except Exception as e:
    traceback.print_exc()
