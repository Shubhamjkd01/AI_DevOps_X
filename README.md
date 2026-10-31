# ⚡ AIDEVOPS — Autonomous CI/CD Self-Healing Engine

[![Powered by Google Gemini / Gemma 4](https://img.shields.io/badge/AI%20Engine-Google%20Gemini%202.5%20%2F%20Gemma%204-blue.svg)](https://ai.google.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20Webhook-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit UI](https://img.shields.io/badge/Telemetry-Streamlit%20Dashboard-FF4B4B.svg)](https://streamlit.io/)
[![Zero-Trust Security](https://img.shields.io/badge/Security-Zero--Trust%20AST%20Guard-10B981.svg)](https://github.com/Shubhamjkd01/aidevops-portal)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An open-source, autonomous self-healing DevOps engine that intercepts **GitHub Actions CI/CD failures**, triages error logs using **Google Gemini 2.5 Pro / Gemma 4**, validates code safety with an **Abstract Syntax Tree (AST) Hallucination Guard**, consults **FAISS 768-dim episodic memory**, and automatically deploys tested, ready-to-merge **Pull Requests** in seconds.

---

## 🌐 Public Documentation & Guidance Portal

> Looking for the developer onboarding guide, security guarantees, and live architecture walkthrough?  
> Visit our dedicated documentation repository: **[aidevops-portal](https://github.com/Shubhamjkd01/aidevops-portal)**

---

## ⚡ 3-Minute Quickstart on Any Laptop (Windows / macOS / Linux)

### 1. Clone the Repository
```bash
git clone https://github.com/Shubhamjkd01/AI_DevOps_X.git
cd AI_DevOps_X/github_agent_backend
```

### 2. Create Virtual Environment & Install Dependencies
```bash
# Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux:
python3 -m venv venv
source venv/bin/activate

# Install requirements:
pip install -r requirements.txt
```

### 3. Configure `.env`
Copy the included template:
```bash
# Windows:
copy .env.example .env

# macOS / Linux:
cp .env.example .env
```
Edit `.env` and add:
- `GEMINI_API_KEY`: Get a free key from [Google AI Studio](https://aistudio.google.com/).
- `GITHUB_TOKEN`: A GitHub Personal Access Token (PAT) with `Actions: Read` and `Pull Requests: Read & Write`.
- `GITHUB_WEBHOOK_SECRET`: Any random password string (e.g. `secret123`).

### 4. Verify Your Environment (Pre-flight Doctor)
Run our built-in health check to confirm your laptop has everything installed:
```bash
python check_setup.py
```

### 5. Start the Stack (1 Command!)
```bash
# Option A: 1-Command All-in-One Runner (Starts both Backend & Dashboard)
python run_local.py

# Option B: Double-click launcher (Windows)
start.bat

# Option C: Shell script (macOS / Linux)
chmod +x start.sh && ./start.sh

# Option D: Run manually in 2 separate terminals:
# Terminal 1: python -m uvicorn server.app:app --host 0.0.0.0 --port 7860 --reload
# Terminal 2: python -m streamlit run dashboard.py --server.port 8501
```

Access your services:
* **Interactive Dashboard:** `http://localhost:8501`
* **FastAPI Webhook API:** `http://localhost:7860`
* **Swagger API Documentation:** `http://localhost:7860/docs`

---

## 🧪 Instant Dry-Run Verification (No GitHub setup required)

To test the entire AI reasoning, AST validator, and FAISS memory pipeline immediately without waiting for a real GitHub failure:
```bash
python scripts/test_webhook_local.py
```
Watch the engine intercept the crash, query Gemini, validate the AST syntax tree, and record the fix.

---

## 🔗 Connecting Your Laptop to GitHub Actions via Webhook

Because your laptop is behind local Wi-Fi, expose port `7860` to GitHub using **ngrok**:
```bash
ngrok http 7860
```
1. Copy the HTTPS URL: `https://xxxx.ngrok-free.app`
2. Add `/webhook/github` at the end: `https://xxxx.ngrok-free.app/webhook/github`
3. In your GitHub Repo &rarr; **Settings** &rarr; **Webhooks** &rarr; **Add Webhook**:
   - **Payload URL:** `https://xxxx.ngrok-free.app/webhook/github`
   - **Content type:** `application/json`
   - **Secret:** Match the `GITHUB_WEBHOOK_SECRET` in your `.env`
   - **Events:** Select "Workflow runs"
   - Click **Add Webhook**.

---

## 📁 Critical Files: Where to Change What

| File Path | What to Edit in It | Why & When to Edit |
|---|---|---|
| **`.env`** | `GEMINI_API_KEY`, `GITHUB_TOKEN`, `GITHUB_WEBHOOK_SECRET` | Set credentials. Never commit this file to Git! |
| **`server/config.py`** | `MODEL_NAME`, `TEMPERATURE`, `PORT` | Switch AI models (`gemini-2.5-pro` or `gemini-1.5-flash`), change port |
| **`github_agent/agent.py`** | `BRANCH_PREFIX`, `AST_CHECK_ENABLED` | Tune automated PR branch names or AST validation |
| **`server/app.py`** | `/webhook/github` route | Add team alerts (Slack / Discord / Teams) |

---

## 🛡️ Enterprise Zero-Trust & Code Safety Guarantees

* **Zero Code Retention:** Source code is never stored in databases or disks. Processed ephemerally in RAM.
* **Never Trained On:** Stack traces are never used to train or fine-tune AI models.
* **One-Way Webhooks:** Webhook payloads contain run metadata only; they have zero read/clone access to private repositories.
* **AST Safety Gate:** Every patch passes `ast.parse()` to block malicious system calls (`os.system`, `subprocess`, `eval`).
* **Human-in-the-Loop:** The agent **never pushes directly to `main`**; it only submits a Pull Request for human review and approval.

---

## 🐳 Docker Deployment (Optional 1-Click)

```bash
docker compose up -d --build
```

---

## 👨‍💻 Created by
**Shubham** ([@Shubhamjkd01](https://github.com/Shubhamjkd01))  
*Autonomous DevOps & AI Systems Architect*
