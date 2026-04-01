import os
import sys
from dotenv import load_dotenv

load_dotenv(override=True)

from agents.orchestrator import handle_workflow_failure
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
fh = logging.FileHandler("real_debug_log.txt", "w", encoding="utf-8")
logger.addHandler(fh)

repo = "Shubhamjkd01/AI_DevOps_X"
run_id = 22222

try:
    url = handle_workflow_failure(repo, run_id)
except Exception as e:
    pass
