import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logging
from dotenv import load_dotenv
load_dotenv()
from agents.orchestrator import handle_workflow_failure

# Configure terminal logging to show the real-time AI thought process
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

print("==========================================================")
print("[*] BOOTING ELITE ARCHITECTURE VERIFICATION")
print("==========================================================")
print("Target: Shubhamjkd01/AI_DevOps_X")
print("This completely bypasses the webserver to directly test features:\n")

try:
    # We trigger the orchestrator synchronously!
    pr_url = handle_workflow_failure("Shubhamjkd01/AI_DevOps_X", 9999)
    print("\n[+] ORCHESTRATOR COMPLETE!")
    if pr_url:
        print(f"[+] Pull Request Generated: {pr_url}")
    else:
        print("[!] Patch blocked by Sandbox Regression validation.")
except Exception as e:
    print(f"\n[-] PIPELINE EXCEPTION CAUGHT BY FAULT TOLERANCE: {e}")

print("==========================================================")
print("Verification complete. Check episodic_patch_memory.json to see the reward matrices!")
