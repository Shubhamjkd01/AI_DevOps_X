"""
AIDEVOPS — 1-Command Local Laptop Runner
Starts both the FastAPI Webhook Backend and the Streamlit Dashboard concurrently.

Usage:
    python run_local.py
"""

import sys
import os
import subprocess
import time
import signal

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Check if .env exists
env_path = os.path.join(BASE_DIR, ".env")
example_path = os.path.join(BASE_DIR, ".env.example")
if not os.path.exists(env_path) and os.path.exists(example_path):
    import shutil
    shutil.copy2(example_path, env_path)
    print("[*] Created .env from .env.example template.")

print("=" * 60)
print("⚡ AIDEVOPS — Starting Autonomous Self-Healing Stack")
print("=" * 60)
print("  Backend API:         http://localhost:7860")
print("  Interactive UI:      http://localhost:8501")
print("  Swagger API Docs:    http://localhost:7860/docs")
print("=" * 60)
print("Press Ctrl+C at any time to stop both servers.\n")

processes = []

try:
    # 1. Start FastAPI Backend Server
    backend_cmd = [
        sys.executable, "-m", "uvicorn", "server.app:app",
        "--host", "0.0.0.0", "--port", "7860"
    ]
    p_backend = subprocess.Popen(backend_cmd, cwd=BASE_DIR)
    processes.append(p_backend)
    print("[*] FastAPI Webhook Backend started (PID: {})".format(p_backend.pid))

    # Give backend 1.5 seconds to bind port
    time.sleep(1.5)

    # 2. Start Streamlit Dashboard UI
    dashboard_cmd = [
        sys.executable, "-m", "streamlit", "run", "dashboard.py",
        "--server.port", "8501", "--server.headless", "true"
    ]
    p_dashboard = subprocess.Popen(dashboard_cmd, cwd=BASE_DIR)
    processes.append(p_dashboard)
    print("[*] Streamlit Dashboard UI started (PID: {})".format(p_dashboard.pid))
    print("\n>>> Open your browser at: http://localhost:8501 <<<\n")

    # Monitor processes
    while True:
        time.sleep(1)
        for p in processes:
            if p.poll() is not None:
                print(f"[!] Process {p.pid} terminated unexpectedly with code {p.returncode}")
                sys.exit(p.returncode)

except KeyboardInterrupt:
    print("\n[*] Shutting down servers gracefully...")
    for p in processes:
        try:
            p.terminate()
            p.wait(timeout=3)
        except Exception:
            p.kill()
    print("[*] Both servers stopped cleanly. Goodbye!")
