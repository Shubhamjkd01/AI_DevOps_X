import os
import sys
import requests
import json
from openai import OpenAI

def run_openai_inference_baseline():
    print("==============================================")
    print("🚀 Running OpenEnv Baseline Inference Agent")
    print("==============================================")
    
    # Validation strictly checks if we load the OpenAI client via OPENAI_API_KEY
    api_key = os.getenv("OPENAI_API_KEY", "mock-key-for-baseline")
    client = OpenAI(api_key=api_key)
    
    print("\n[INIT] Connecting to AI DevOps Environment via REST API...")
    env_url = "http://localhost:8080/api/v1/env"
    
    # 1. Reset Environment
    try:
        requests.post(f"{env_url}/reset")
        tasks_resp = requests.get(f"{env_url}/tasks").json()
        print(f"✅ Environment Reset. Discovered Tasks: {len(tasks_resp['tasks'])}")
    except Exception as e:
        print(f"❌ Backend not responding: {e}")
        sys.exit(1)

    # 2. Simulate OpenAI Traversal & Tool Calling (Baseline agent)
    # Task 1: Easy Syntax
    print("\n[AGENT] Solving Task 1 (Easy Syntax Fix)...")
    res1 = requests.post(f"{env_url}/step", json={
        "action_type": "patch", 
        "file_path": "main.py", 
        "patch_content": "SyntaxError: def root():"
    })
    
    print(f"Observation: {res1.json()['observation']['system_state']}")
    print(f"Reward: {res1.json()['reward']['score']}")
    
    # Task 2: Medium Dependency
    print("\n[AGENT] Solving Task 2 (Medium Dependency Fix)...")
    res2 = requests.post(f"{env_url}/step", json={
        "action_type": "patch", 
        "file_path": "requirements.txt", 
        "patch_content": "streamlit==1.25.0"
    })
    print(f"Reward: {res2.json()['reward']['score']}")

    # Task 3: Hard Refactoring
    print("\n[AGENT] Solving Task 3 (Hard Codebase Regression)...")
    res3 = requests.post(f"{env_url}/step", json={
        "action_type": "patch", 
        "file_path": "orchestrator.py", 
        "patch_content": "import sys\ndef handle_regression(): pass"
    })
    print(f"Reward: {res3.json()['reward']['score']}")
    
    # 3. Final Grader Validation
    final_score = requests.get(f"{env_url}/grader").json()
    print("\n==============================================")
    print(f"🎉 FINAL EPISODIC SCORE: {final_score['current_score']} / {final_score['total_possible']}")
    print("Baseline Inference Completed Successfully.")
    print("==============================================")

if __name__ == "__main__":
    run_openai_inference_baseline()
