"""
AIDEVOPS — Pre-flight Laptop Environment Doctor
Run this script to verify your laptop is 100% ready to run AIDEVOPS:
    python check_setup.py
"""

import sys
import os
import shutil

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ANSI Colors with safe fallback
if sys.platform == "win32" and "WT_SESSION" not in os.environ and "TERM" not in os.environ:
    GREEN = ""
    YELLOW = ""
    RED = ""
    CYAN = ""
    BOLD = ""
    RESET = ""
else:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

def print_header():
    print(f"\n{CYAN}{BOLD}[*] AIDEVOPS -- Pre-flight Laptop Environment Doctor{RESET}")
    print(f"{CYAN}{'='*58}{RESET}\n")

def check_python():
    v = sys.version_info
    print("1. Checking Python Version... ", end="")
    if v.major == 3 and v.minor >= 10:
        print(f"{GREEN}[PASS]{RESET} Python {v.major}.{v.minor}.{v.micro}")
        return True
    else:
        print(f"{RED}[FAIL]{RESET} Python {v.major}.{v.minor} detected. Python 3.10+ required.")
        return False

def check_env_file():
    print("2. Checking .env Configuration... ", end="")
    env_path = os.path.join(BASE_DIR, ".env")
    example_path = os.path.join(BASE_DIR, ".env.example")
    
    if os.path.exists(env_path):
        print(f"{GREEN}[PASS]{RESET} .env file found.")
        return True
    else:
        if os.path.exists(example_path):
            shutil.copy2(example_path, env_path)
            print(f"{YELLOW}[COPIED]{RESET} Created .env from .env.example. Please open .env and add your GEMINI_API_KEY!")
            return True
        else:
            print(f"{RED}[FAIL]{RESET} .env not found. Please create .env!")
            return False

def check_dependencies():
    print("3. Checking Python Dependencies... ", end="")
    required = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("requests", "requests"),
        ("dotenv", "python-dotenv"),
        ("pydantic", "pydantic"),
        ("github", "PyGithub"),
        ("streamlit", "streamlit"),
        ("pandas", "pandas"),
        ("google.generativeai", "google-generativeai")
    ]
    missing = []
    for mod, pkg in required:
        try:
            __import__(mod)
        except ImportError:
            missing.append(pkg)
            
    if not missing:
        print(f"{GREEN}[PASS]{RESET} All core dependencies installed.")
        return True
    else:
        print(f"{RED}[FAIL]{RESET} Missing: {', '.join(missing)}")
        print(f"   {YELLOW}Fix by running:{RESET} pip install -r requirements.txt")
        return False

def check_keys():
    print("4. Checking API Keys in .env... ", end="")
    env_path = os.path.join(BASE_DIR, ".env")
    gemini_key = ""
    gh_token = ""
    
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GEMINI_API_KEY="):
                    gemini_key = line.split("=", 1)[1].strip("'\"")
                elif line.startswith("GITHUB_TOKEN="):
                    gh_token = line.split("=", 1)[1].strip("'\"")

    issues = []
    if not gemini_key or "your_gemini" in gemini_key:
        issues.append("GEMINI_API_KEY (Get free key at: https://aistudio.google.com/)")
    if not gh_token or "your_github" in gh_token:
        issues.append("GITHUB_TOKEN (Personal Access Token from https://github.com/settings/tokens)")

    if not issues:
        print(f"{GREEN}[PASS]{RESET} Keys are configured.")
        return True
    else:
        print(f"{YELLOW}[NOTICE]{RESET}")
        for i in issues:
            print(f"   * Missing {i}")
        return False

def check_storage_files():
    print("5. Checking Local Storage / Memory Files... ", end="")
    files = [
        "episodic_patch_memory.json",
        "failure_patterns.json",
        "mastery_scores.json",
        "hot_zones.json"
    ]
    created = 0
    for f in files:
        p = os.path.join(BASE_DIR, f)
        if not os.path.exists(p):
            with open(p, "w", encoding="utf-8") as fp:
                fp.write("[]" if "memory" in f or "patterns" in f else "{}")
            created += 1
    print(f"{GREEN}[PASS]{RESET} Verified {len(files)} JSON storage files.")
    return True

def main():
    print_header()
    s1 = check_python()
    s2 = check_env_file()
    s3 = check_dependencies()
    s4 = check_storage_files()
    s5 = check_keys()
    
    print(f"\n{CYAN}{'='*58}{RESET}")
    if s1 and s2 and s3 and s4:
        print(f"{GREEN}{BOLD}>>> Your laptop environment is READY to run AIDEVOPS!{RESET}\n")
        print("To start everything:")
        print(f"  {BOLD}Option A (All-in-one):{RESET}  python run_local.py")
        print(f"  {BOLD}Option B (Separate):{RESET}")
        print("    Terminal 1 (Backend):    python -m uvicorn server.app:app --host 0.0.0.0 --port 7860 --reload")
        print("    Terminal 2 (Dashboard):  python -m streamlit run dashboard.py --server.port 8501")
        print(f"  {BOLD}Option C (Dry-run test):{RESET} python scripts/test_webhook_local.py\n")
    else:
        print(f"{YELLOW}{BOLD}Please fix the highlighted issues above to complete setup.{RESET}\n")

if __name__ == "__main__":
    main()
