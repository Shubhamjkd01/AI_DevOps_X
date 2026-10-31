import os
import base64

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img_path = os.path.join(BASE_DIR, "developer.png")
if os.path.exists(img_path):
    with open(img_path, "rb") as f:
        dev_img_b64 = base64.b64encode(f.read()).decode("utf-8")
else:
    dev_img_b64 = ""

COMMON_HEAD = """
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #07090E;
            --purple: #8B5CF6;
            --cyan: #06B6D4;
            --pink: #EC4899;
            --emerald: #10B981;
            --amber: #F59E0B;
            --text-main: #F1F5F9;
            --text-muted: #94A3B8;
            --glass-bg: rgba(13, 17, 28, 0.75);
            --glass-border: rgba(255, 255, 255, 0.08);
        }
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        body {
            background-color: var(--bg-base);
            color: var(--text-main);
            background: 
                radial-gradient(circle at 10% 20%, rgba(139, 92, 246, 0.22) 0%, transparent 40%),
                radial-gradient(circle at 90% 30%, rgba(6, 182, 212, 0.2) 0%, transparent 42%),
                radial-gradient(circle at 85% 85%, rgba(236, 72, 153, 0.2) 0%, transparent 40%),
                var(--bg-base);
            background-attachment: fixed;
            line-height: 1.6;
            overflow-x: hidden;
        }
        .container {
            max-width: 1250px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }
        /* Navbar */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.9rem 1.6rem;
            margin: 1.5rem auto 3rem auto;
            background: rgba(13, 17, 28, 0.7);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 9999px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            position: sticky;
            top: 1rem;
            z-index: 100;
        }
        .nav-logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-weight: 800;
            font-size: 1.15rem;
            letter-spacing: -0.02em;
            color: #FFFFFF;
            text-decoration: none;
        }
        .nav-logo-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
            clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.6);
            font-size: 0.9rem;
        }
        .nav-links {
            display: flex;
            gap: 1.8rem;
            align-items: center;
        }
        .nav-links a {
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            transition: color 0.2s ease;
        }
        .nav-links a:hover, .nav-links a.active {
            color: #38BDF8;
        }
        .nav-btn {
            background: linear-gradient(135deg, #EC4899 0%, #A855F7 100%);
            color: #FFFFFF !important;
            padding: 0.55rem 1.4rem;
            border-radius: 9999px;
            font-weight: 700;
            font-size: 0.82rem;
            letter-spacing: 0.04em;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 18px rgba(236, 72, 153, 0.45);
            transition: all 0.2s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
        }
        .nav-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 24px rgba(236, 72, 153, 0.6);
        }
        @media (max-width: 900px) {
            .nav-links { display: none; }
        }

        /* Typography & Badges */
        .pill {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.35rem 0.95rem;
            border-radius: 9999px;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        .pill-cyan {
            background: rgba(6, 182, 212, 0.12);
            border: 1px solid rgba(6, 182, 212, 0.35);
            color: #22D3EE;
        }
        .pill-emerald {
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.35);
            color: #34D399;
        }
        .pill-purple {
            background: rgba(139, 92, 246, 0.12);
            border: 1px solid rgba(139, 92, 246, 0.35);
            color: #C084FC;
        }
        .pill-amber {
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid rgba(245, 158, 11, 0.35);
            color: #FBBF24;
        }

        .section-header {
            text-align: center;
            margin-bottom: 3.5rem;
        }
        .section-title {
            font-size: 2.3rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: #FFFFFF;
            margin: 0.6rem 0;
        }
        .section-desc {
            font-size: 1.05rem;
            color: var(--text-muted);
            max-width: 700px;
            margin: 0 auto;
        }

        /* Glass Cards */
        .card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
        }
        .card-cyan::before { background: linear-gradient(90deg, #06B6D4, transparent); }
        .card-purple::before { background: linear-gradient(90deg, #8B5CF6, transparent); }
        .card-emerald::before { background: linear-gradient(90deg, #10B981, transparent); }
        .card-amber::before { background: linear-gradient(90deg, #F59E0B, transparent); }
        .card-pink::before { background: linear-gradient(90deg, #EC4899, transparent); }

        /* Code & Terminal Blocks */
        pre {
            background: #06090F;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.1rem 1.3rem;
            font-family: 'Fira Code', monospace;
            font-size: 0.85rem;
            color: #38BDF8;
            overflow-x: auto;
            margin: 0.9rem 0;
            line-height: 1.55;
            position: relative;
        }
        code {
            font-family: 'Fira Code', monospace;
            background: rgba(255, 255, 255, 0.06);
            padding: 0.2rem 0.45rem;
            border-radius: 6px;
            font-size: 0.88em;
            color: #38BDF8;
        }
        .copy-btn {
            position: absolute;
            top: 0.6rem;
            right: 0.8rem;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #94A3B8;
            font-size: 0.72rem;
            font-weight: 600;
            padding: 0.25rem 0.65rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .copy-btn:hover {
            background: rgba(56, 189, 248, 0.2);
            color: #38BDF8;
        }

        /* Buttons */
        .btn-primary {
            background: linear-gradient(135deg, #EC4899 0%, #A855F7 100%);
            color: #FFFFFF !important;
            padding: 0.75rem 1.8rem;
            border-radius: 9999px;
            font-weight: 700;
            font-size: 0.9rem;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            box-shadow: 0 4px 20px rgba(236, 72, 153, 0.4);
            transition: all 0.2s ease;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 26px rgba(236, 72, 153, 0.6);
        }
        .btn-secondary {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #F1F5F9 !important;
            padding: 0.75rem 1.8rem;
            border-radius: 9999px;
            font-weight: 700;
            font-size: 0.9rem;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.2s ease;
        }
        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: translateY(-2px);
        }

        /* Tables */
        .styled-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.2rem 0;
            font-size: 0.88rem;
        }
        .styled-table th {
            text-align: left;
            padding: 0.75rem 1rem;
            background: rgba(255, 255, 255, 0.03);
            color: #94A3B8;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            border-bottom: 1px solid var(--glass-border);
        }
        .styled-table td {
            padding: 0.9rem 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            color: var(--text-main);
        }
        .styled-table tr:hover {
            background: rgba(255, 255, 255, 0.02);
        }

        /* Grid */
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.8rem;
        }
        .grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.8rem;
        }
        @media (max-width: 850px) {
            .grid-2, .grid-3 { grid-template-columns: 1fr; }
        }

        /* Step timeline */
        .step-row {
            display: flex;
            gap: 1.25rem;
            margin-bottom: 1.8rem;
        }
        .step-number {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            flex-shrink: 0;
            background: linear-gradient(135deg, #EC4899 0%, #A855F7 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 0.95rem;
            box-shadow: 0 0 15px rgba(236, 72, 153, 0.5);
        }
        .step-number.cyan {
            background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%);
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.5);
        }
        .step-body {
            flex: 1;
        }
        .step-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 0.35rem;
        }
        .step-desc {
            color: var(--text-muted);
            font-size: 0.92rem;
            line-height: 1.6;
        }

        /* Footer */
        footer {
            border-top: 1px solid var(--glass-border);
            padding: 3rem 0;
            margin-top: 5rem;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.85rem;
        }
    </style>
"""

def get_navbar(active_page="home"):
    return f"""
    <div class="navbar">
        <a class="nav-logo" href="index.html">
            <div class="nav-logo-icon">⚡</div>
            <div>
                <div>AIDEVOPS</div>
                <div style="font-size: 0.62rem; color: #64748B; font-weight: 600; margin-top: -3px;">Self-Healing CI/CD</div>
            </div>
        </a>
        <div class="nav-links">
            <a href="index.html" class="{'active' if active_page == 'home' else ''}">HOME</a>
            <a href="docs.html" class="{'active' if active_page == 'docs' else ''}">DOCUMENTATION & LAPTOP SETUP</a>
            <a href="security.html" class="{'active' if active_page == 'security' else ''}">DATA & CODE SECURITY</a>
            <a href="index.html#about-author">ABOUT DEVELOPER</a>
        </div>
        <div>
            <a class="nav-btn" href="https://github.com/Shubhamjkd01/AI_DevOps_X" target="_blank">
                ⭐ GITHUB REPO
            </a>
        </div>
    </div>
    """

# =========================================================================
# 1. GENERATE DOCS.HTML (LAPTOP SETUP & WHERE TO CHANGE WHAT)
# =========================================================================
docs_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>Documentation & Laptop Setup Guide — AIDEVOPS</title>
    {COMMON_HEAD}
</head>
<body>
<div class="container">
    {get_navbar('docs')}

    <div class="section-header">
        <div class="pill pill-cyan">DEVELOPER ONBOARDING MANUAL</div>
        <h1 class="section-title">Laptop Setup & Customization Guide</h1>
        <p class="section-desc">
            Complete step-by-step instructions to clone, configure, customize, and run AIDEVOPS locally on your personal laptop or development workstation.
        </p>
    </div>

    <!-- QUICK OVERVIEW SUMMARY CARD -->
    <div class="card card-purple">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; margin-bottom: 1.2rem;">
            <h3 style="font-size: 1.25rem; color: #FFFFFF;">💻 What You Need on Your Laptop (Prerequisites)</h3>
            <span class="pill pill-emerald">SETUP TIME: ~4 MINUTES</span>
        </div>
        <p style="color: var(--text-muted); font-size: 0.92rem; margin-bottom: 1rem;">
            Before starting, make sure you have the following installed on your machine:
        </p>
        <div class="grid-3">
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--glass-border); border-radius: 12px; padding: 1rem;">
                <div style="font-weight: 700; color: #38BDF8; margin-bottom: 0.3rem;">🐍 Python 3.10+</div>
                <div style="font-size: 0.85rem; color: #94A3B8;">Check with <code>python --version</code>. Recommended: Python 3.10, 3.11, or 3.12.</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--glass-border); border-radius: 12px; padding: 1rem;">
                <div style="font-weight: 700; color: #C084FC; margin-bottom: 0.3rem;">🐙 Git & GitHub Account</div>
                <div style="font-size: 0.85rem; color: #94A3B8;">For cloning repo, setting up webhooks, and pushing automated fix PRs.</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--glass-border); border-radius: 12px; padding: 1rem;">
                <div style="font-weight: 700; color: #34D399; margin-bottom: 0.3rem;">🔑 Google Gemini Key</div>
                <div style="font-size: 0.85rem; color: #94A3B8;">Free API key from <a href="https://aistudio.google.com" target="_blank" style="color: #34D399;">Google AI Studio</a>.</div>
            </div>
        </div>
    </div>

    <!-- WHERE TO CHANGE WHAT (THE CORE HIGHLIGHT) -->
    <div class="card card-pink" id="where-to-change">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; margin-bottom: 1.5rem;">
            <div>
                <div class="pill pill-pink" style="margin-bottom: 0.5rem;">CRITICAL REFERENCE</div>
                <h2 style="font-size: 1.5rem; color: #FFFFFF;">📁 Where to Change & What to Edit on Your Laptop</h2>
            </div>
            <span class="pill pill-amber">READ THIS FIRST</span>
        </div>
        <p style="color: var(--text-muted); font-size: 0.95rem; margin-bottom: 1.5rem;">
            When you run this on your laptop, here are the <strong>only 4 files</strong> you ever need to touch or modify based on your requirements:
        </p>

        <table class="styled-table">
            <thead>
                <tr>
                    <th style="width: 25%;">File Path</th>
                    <th style="width: 30%;">What to Change in it</th>
                    <th style="width: 45%;">Why & When to Change It</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>.env</code><br><span style="font-size: 0.72rem; color: #EC4899; font-weight: 700;">★ MOST IMPORTANT</span></td>
                    <td>
                        <code>GEMINI_API_KEY</code><br>
                        <code>GITHUB_TOKEN</code><br>
                        <code>GITHUB_WEBHOOK_SECRET</code>
                    </td>
                    <td>
                        Paste your Google Gemini API key, your GitHub Personal Access Token (PAT), and your webhook secret password. <strong>Never commit this file to git!</strong>
                    </td>
                </tr>
                <tr>
                    <td><code>server/config.py</code></td>
                    <td>
                        <code>MODEL_NAME = "gemini-2.5-pro"</code><br>
                        <code>TEMPERATURE = 0.2</code><br>
                        <code>DEFAULT_PORT = 7860</code>
                    </td>
                    <td>
                        Change this if you want to switch AI models (e.g. <code>gemini-1.5-flash</code> for 3x faster fixes or <code>gemini-2.5-pro</code> for deeper multi-file reasoning), or change local port.
                    </td>
                </tr>
                <tr>
                    <td><code>github_agent/agent.py</code></td>
                    <td>
                        <code>BRANCH_PREFIX = "fix/ci-failure-"</code><br>
                        <code>AST_CHECK_ENABLED = True</code>
                    </td>
                    <td>
                        Change this if your team uses a custom branch naming policy (e.g., <code>hotfix/ci-</code> or <code>bot/fix-</code>) or if you want to tune commit PR descriptions.
                    </td>
                </tr>
                <tr>
                    <td><code>server/app.py</code></td>
                    <td>
                        <code>/webhook/github</code> route<br>
                        Custom Slack / Discord hooks
                    </td>
                    <td>
                        Only modify if you want to forward webhook notifications to your company Slack, Microsoft Teams, or Discord channels after a fix PR is created.
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- STEP BY STEP INSTALLATION TIMELINE -->
    <div class="card card-cyan">
        <h2 style="font-size: 1.45rem; color: #FFFFFF; margin-bottom: 2rem;">🚀 Step-by-Step Laptop Setup Walkthrough</h2>

        <!-- STEP 1 -->
        <div class="step-row">
            <div class="step-number cyan">1</div>
            <div class="step-body">
                <div class="step-title">Clone the Repository to Your Laptop</div>
                <div class="step-desc">Open PowerShell, CMD, or Terminal on your laptop and clone the official project repository:</div>
                <pre><code>git clone https://github.com/Shubhamjkd01/AI_DevOps_X.git
cd AI_DevOps_X/github_agent_backend</code></pre>
            </div>
        </div>

        <!-- STEP 2 -->
        <div class="step-row">
            <div class="step-number cyan">2</div>
            <div class="step-body">
                <div class="step-title">Create a Virtual Environment & Install Dependencies</div>
                <div class="step-desc">Isolate your dependencies to keep your system clean:</div>
                <pre><code># On Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1

# On macOS / Linux:
python3 -m venv venv
source venv/bin/activate

# Install all required libraries:
pip install -r requirements.txt</code></pre>
            </div>
        </div>

        <!-- STEP 3 -->
        <div class="step-row">
            <div class="step-number cyan">3</div>
            <div class="step-body">
                <div class="step-title">Configure Your Secret Keys in <code>.env</code></div>
                <div class="step-desc">
                    Create a file named <code>.env</code> in the <code>github_agent_backend</code> folder (you can copy <code>.env.example</code> if present):
                </div>
                <pre><code># 1. Get free Gemini Key from: https://aistudio.google.com
GEMINI_API_KEY="AIzaSyYourGeminiApiKeyHere"

# 2. Get GitHub Token from: GitHub -> Settings -> Developer Settings -> Personal Access Tokens
# Permissions required: "Actions: Read" and "Pull Requests: Read & Write"
GITHUB_TOKEN="ghp_YourGitHubPersonalAccessToken"

# 3. Create any random secret string (e.g. 16+ chars)
GITHUB_WEBHOOK_SECRET="super_secret_webhook_passphrase_987"

# 4. Local Server Ports
SERVER_PORT=7860
DASHBOARD_PORT=8501</code></pre>
            </div>
        </div>

        <!-- STEP 4 -->
        <div class="step-row">
            <div class="step-number cyan">4</div>
            <div class="step-body">
                <div class="step-title">Expose Your Laptop Port to GitHub (Ngrok / Cloudflare)</div>
                <div class="step-desc">
                    Because your laptop is behind your home Wi-Fi or router, GitHub's cloud servers cannot directly ping <code>localhost:7860</code>. Use <strong>ngrok</strong> (free) or <strong>localtunnel</strong> to create a secure bridge:
                </div>
                <pre><code># Install ngrok from ngrok.com (or via choco / brew)
# In a new terminal window, run:
ngrok http 7860</code></pre>
                <div class="step-desc" style="margin-top: 0.5rem;">
                    Ngrok will give you a public Forwarding URL like: <code>https://3a1b-103-21-54-1.ngrok-free.app</code>.<br>
                    Your GitHub Webhook URL will be: <code>https://3a1b-103-21-54-1.ngrok-free.app/webhook/github</code>
                </div>
            </div>
        </div>

        <!-- STEP 5 -->
        <div class="step-row">
            <div class="step-number cyan">5</div>
            <div class="step-body">
                <div class="step-title">Connect GitHub Webhook to Your Repository</div>
                <div class="step-desc">
                    Go to your repository on GitHub:
                    <ol style="margin-left: 1.5rem; margin-top: 0.5rem; color: #CBD5E1;">
                        <li>Click <strong>Settings</strong> &rarr; <strong>Webhooks</strong> &rarr; <strong>Add Webhook</strong></li>
                        <li><strong>Payload URL:</strong> Paste your ngrok URL with <code>/webhook/github</code> (e.g. <code>https://your-ngrok.ngrok-free.app/webhook/github</code>)</li>
                        <li><strong>Content type:</strong> Select <code>application/json</code></li>
                        <li><strong>Secret:</strong> Enter the exact same secret you put in your <code>.env</code> file (<code>GITHUB_WEBHOOK_SECRET</code>)</li>
                        <li><strong>Which events would you like to trigger this webhook?</strong> Select <em>"Let me select individual events"</em> &check; Check <strong>"Workflow runs"</strong>.</li>
                        <li>Click <strong>Add Webhook</strong> (Active green checkmark appears).</li>
                    </ol>
                </div>
            </div>
        </div>

        <!-- STEP 6 -->
        <div class="step-row">
            <div class="step-number cyan">6</div>
            <div class="step-body">
                <div class="step-title">Launch Backend Server & Interactive Dashboard</div>
                <div class="step-desc">Open two terminal tabs on your laptop to run both the API and the UI:</div>
                <pre><code># Terminal 1: Run FastAPI Webhook Receiver Agent
python -m uvicorn server.app:app --host 0.0.0.0 --port 7860 --reload

# Terminal 2: Run Streamlit Analytics Dashboard
python -m streamlit run dashboard.py --server.port 8501</code></pre>
                <div class="step-desc" style="margin-top: 0.5rem;">
                    Your dashboard is now live at <code>http://localhost:8501</code> and ready to receive and heal CI failures in real-time!
                </div>
            </div>
        </div>

        <!-- STEP 7 -->
        <div class="step-row">
            <div class="step-number cyan">7</div>
            <div class="step-body">
                <div class="step-title">Test Your Laptop Setup (Instant Dry-Run)</div>
                <div class="step-desc">
                    You don't need to wait for a real GitHub failure to verify everything works! We included a built-in mock failure generator:
                </div>
                <pre><code># In a new terminal tab, run:
python scripts/test_webhook_local.py</code></pre>
                <div class="step-desc" style="margin-top: 0.5rem;">
                    Watch Terminal 1 parse the error, consult episodic memory, invoke Gemini with AST checks, and log the autonomous patch.
                </div>
            </div>
        </div>
    </div>

    <!-- DOCKER ALTERNATIVE -->
    <div class="card card-emerald">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; margin-bottom: 1rem;">
            <h3 style="font-size: 1.25rem; color: #FFFFFF;">🐳 Prefer Docker on Your Laptop? (1-Command Run)</h3>
            <span class="pill pill-emerald">DOCKER COMPOSE READY</span>
        </div>
        <p style="color: var(--text-muted); font-size: 0.92rem; margin-bottom: 1rem;">
            If you have Docker Desktop installed, you can skip Python virtualenvs and run the entire stack with a single command:
        </p>
        <pre><code># 1. Populate your .env file with your GEMINI_API_KEY and GITHUB_TOKEN
# 2. Start all services in the background:
docker compose up -d --build

# 3. View live logs:
docker compose logs -f</code></pre>
    </div>

    <!-- TROUBLESHOOTING FAQ -->
    <div class="card card-amber">
        <h3 style="font-size: 1.25rem; color: #FFFFFF; margin-bottom: 1.2rem;">🔧 Laptop Setup Troubleshooting & FAQ</h3>
        <div class="grid-2">
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--glass-border); border-radius: 12px; padding: 1.2rem;">
                <div style="font-weight: 700; color: #F59E0B; margin-bottom: 0.4rem;">❌ Webhook returns "401 Unauthorized"</div>
                <div style="font-size: 0.88rem; color: #94A3B8;">
                    <strong>Fix:</strong> The secret you typed in GitHub Webhooks does not match the <code>GITHUB_WEBHOOK_SECRET</code> inside your <code>.env</code> file. Update both so they are identical strings.
                </div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--glass-border); border-radius: 12px; padding: 1.2rem;">
                <div style="font-weight: 700; color: #F59E0B; margin-bottom: 0.4rem;">❌ GitHub PR creation fails with "403 Forbidden"</div>
                <div style="font-size: 0.88rem; color: #94A3B8;">
                    <strong>Fix:</strong> Your Personal Access Token is missing permissions. Go to GitHub Token settings and ensure <code>Pull Requests: Read & Write</code> and <code>Contents: Read & Write</code> are checked.
                </div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--glass-border); border-radius: 12px; padding: 1.2rem;">
                <div style="font-weight: 700; color: #F59E0B; margin-bottom: 0.4rem;">❌ "Address already in use" on port 7860 or 8501</div>
                <div style="font-size: 0.88rem; color: #94A3B8;">
                    <strong>Fix:</strong> Another process is occupying the port. Either kill the previous python process or change <code>--port 7861</code> or <code>--server.port 8502</code>.
                </div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--glass-border); border-radius: 12px; padding: 1.2rem;">
                <div style="font-weight: 700; color: #F59E0B; margin-bottom: 0.4rem;">❌ ngrok session expires after 2 hours</div>
                <div style="font-size: 0.88rem; color: #94A3B8;">
                    <strong>Fix:</strong> Create a free account at ngrok.com to get a permanent authtoken and static free domain, or deploy the backend to a cloud VPS like DigitalOcean or HuggingFace.
                </div>
            </div>
        </div>
    </div>

    <!-- CTA BAR -->
    <div style="text-align: center; margin: 4rem 0 2rem 0;">
        <h3 style="font-size: 1.5rem; color: #FFFFFF; margin-bottom: 1rem;">Ready to See How Your Code Remains Safe?</h3>
        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
            <a href="security.html" class="btn-primary">🛡️ View Data & Code Security Guarantees &rarr;</a>
            <a href="https://github.com/Shubhamjkd01/AI_DevOps_X" target="_blank" class="btn-secondary">⭐ Star on GitHub</a>
        </div>
    </div>

    <footer>
        <p>AIDEVOPS — Open Source Autonomous DevOps Platform created by <strong style="color: #FFFFFF;">Shubham</strong> (@Shubhamjkd01).</p>
        <p style="margin-top: 0.4rem;">Licensed under Apache 2.0 / MIT. Built for developers and enterprise engineering teams.</p>
    </footer>
</div>
</body>
</html>
"""

# =========================================================================
# 2. GENERATE SECURITY.HTML (ENTERPRISE DATA & REPO CODE PRIVACY GUARANTEE)
# =========================================================================
security_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>Data & Code Security Guarantees — AIDEVOPS</title>
    {COMMON_HEAD}
</head>
<body>
<div class="container">
    {get_navbar('security')}

    <div class="section-header">
        <div class="pill pill-emerald">DATA PRIVACY & INTEGRITY GUARANTEE</div>
        <h1 class="section-title">How Your Code & Data Remains 100% Safe</h1>
        <p class="section-desc">
            Zero code retention. Zero unauthorized repository access. Cryptographic webhook verification. Complete peace of mind for developers, startups, and enterprises.
        </p>
    </div>

    <!-- ZERO-TRUST SUMMARY CARD -->
    <div class="card card-emerald">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; margin-bottom: 1.5rem;">
            <div>
                <span class="pill pill-emerald" style="margin-bottom: 0.5rem;">OUR GUARANTEE TO ORGANIZATIONS</span>
                <h2 style="font-size: 1.5rem; color: #FFFFFF;">🔒 4 Inviolable Security Pillars</h2>
            </div>
            <span class="pill pill-cyan">ZERO-TRUST COMPLIANT</span>
        </div>
        <p style="color: var(--text-muted); font-size: 0.95rem; margin-bottom: 1.8rem;">
            If an organization or developer gives their repository webhook to AIDEVOPS, they must have 100% assurance that their proprietary codebase, secrets, and customer data can never be compromised, leaked, or stolen. Here is mathematically and architecturally how that is guaranteed:
        </p>

        <div class="grid-2">
            <!-- PILLAR 1 -->
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--glass-border); border-radius: 16px; padding: 1.5rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.8rem;">
                    <div style="font-size: 1.6rem;">🔒</div>
                    <div>
                        <h3 style="font-size: 1.15rem; color: #FFFFFF; margin: 0;">1. One-Way Outbound Webhook</h3>
                        <div style="font-size: 0.75rem; color: #34D399; font-weight: 700;">ZERO INBOUND CODE ACCESS</div>
                    </div>
                </div>
                <p style="color: var(--text-muted); font-size: 0.88rem; line-height: 1.6;">
                    • <strong>Webhooks do not give repository read permissions:</strong> A GitHub Webhook is strictly a one-way notification sent from GitHub's servers to the agent.<br>
                    • <strong>Contains metadata only:</strong> The payload only informs that "Workflow #142 failed on branch staging". It contains <em>zero source code files</em> and cannot clone private repositories.<br>
                    • <strong>HMAC SHA-256 Signatures:</strong> Every incoming payload is validated using GitHub's <code>X-Hub-Signature-256</code>. Forged or unauthenticated requests are rejected with HTTP 401.
                </p>
            </div>

            <!-- PILLAR 2 -->
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--glass-border); border-radius: 16px; padding: 1.5rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.8rem;">
                    <div style="font-size: 1.6rem;">🚫</div>
                    <div>
                        <h3 style="font-size: 1.15rem; color: #FFFFFF; margin: 0;">2. Ephemeral In-Memory Processing</h3>
                        <div style="font-size: 0.75rem; color: #38BDF8; font-weight: 700;">ZERO PERSISTENT CODE STORAGE</div>
                    </div>
                </div>
                <p style="color: var(--text-muted); font-size: 0.88rem; line-height: 1.6;">
                    • <strong>No Code Databases:</strong> Your source code is never saved to external hard drives, persistent SQL databases, or central cloud storage.<br>
                    • <strong>Never Used for AI Model Training:</strong> Google Gemini processes stack traces strictly in isolated RAM buffers solely to synthesize the AST diff. Your code is never used to train or fine-tune models.<br>
                    • <strong>Garbage Collected Instantly:</strong> As soon as the pull request diff is generated, memory pointers are released and cleaned up.
                </p>
            </div>

            <!-- PILLAR 3 -->
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--glass-border); border-radius: 16px; padding: 1.5rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.8rem;">
                    <div style="font-size: 1.6rem;">🔑</div>
                    <div>
                        <h3 style="font-size: 1.15rem; color: #FFFFFF; margin: 0;">3. Granular Least-Privilege Scoping</h3>
                        <div style="font-size: 0.75rem; color: #C084FC; font-weight: 700;">NO ADMIN & NO SECRET ACCESS</div>
                    </div>
                </div>
                <p style="color: var(--text-muted); font-size: 0.88rem; line-height: 1.6;">
                    • <strong>Fine-Grained Personal Access Tokens (PAT):</strong> AIDEVOPS only requires 2 minimal permissions:<br>
                    &nbsp;&nbsp;&nbsp;&bull; <code>Actions: Read</code> (to read failure logs)<br>
                    &nbsp;&nbsp;&nbsp;&bull; <code>Pull Requests: Read & Write</code> (to open automated fix PRs)<br>
                    • <strong>Zero Access to Sensitive Areas:</strong> The agent has NO access to organization billing, repository secrets, production deployment environments, or team administration.<br>
                    • <strong>Instant 1-Click Revocation:</strong> You can revoke the token at any second directly in GitHub settings.
                </p>
            </div>

            <!-- PILLAR 4 -->
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--glass-border); border-radius: 16px; padding: 1.5rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.8rem;">
                    <div style="font-size: 1.6rem;">🛡️</div>
                    <div>
                        <h3 style="font-size: 1.15rem; color: #FFFFFF; margin: 0;">4. AST Syntax Guard & Human Review</h3>
                        <div style="font-size: 0.75rem; color: #EC4899; font-weight: 700;">NO DIRECT PUSH TO PRODUCTION</div>
                    </div>
                </div>
                <p style="color: var(--text-muted); font-size: 0.88rem; line-height: 1.6;">
                    • <strong>AST Malicious Code Blocker:</strong> Every fix proposed by the AI is passed through an Abstract Syntax Tree (AST) validator. Any illegal calls (e.g. <code>os.system</code>, <code>eval()</code>, network exfiltration) are blocked and discarded immediately.<br>
                    • <strong>Zero Direct Pushes to <code>main</code>:</strong> The agent is programmatically restricted from ever pushing directly to <code>main</code> or <code>production</code> branches.<br>
                    • <strong>Mandatory Human Approval:</strong> The agent only opens an isolated Pull Request (e.g. <code>fix/ci-failure-142</code>). A human engineer must review and merge the code.
                </p>
            </div>
        </div>
    </div>

    <!-- COMPARISON TABLE: AIDEVOPS VS TRADITIONAL SAAS -->
    <div class="card card-cyan">
        <h2 style="font-size: 1.4rem; color: #FFFFFF; margin-bottom: 1.5rem;">⚖️ Security Architecture Comparison</h2>
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Security Dimension</th>
                    <th>Standard 3rd-Party SaaS Tools</th>
                    <th style="color: #34D399;">AIDEVOPS Open-Source Engine</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Repository Access</strong></td>
                    <td style="color: #F87171;">Requires Full OAuth / Admin Read & Write</td>
                    <td style="color: #34D399; font-weight: 700;">Strictly Least-Privilege (Actions + PRs only)</td>
                </tr>
                <tr>
                    <td><strong>Source Code Storage</strong></td>
                    <td style="color: #F87171;">Stored on vendor's central cloud database</td>
                    <td style="color: #34D399; font-weight: 700;">Zero code stored. Processed ephemerally in RAM</td>
                </tr>
                <tr>
                    <td><strong>AI Model Training</strong></td>
                    <td style="color: #F87171;">Often used to train proprietary vendor models</td>
                    <td style="color: #34D399; font-weight: 700;">Never trained on. Zero retention policy</td>
                </tr>
                <tr>
                    <td><strong>Deployment Isolation</strong></td>
                    <td style="color: #F87171;">Multi-tenant shared cloud server</td>
                    <td style="color: #34D399; font-weight: 700;">100% Self-Hostable in your own VPC / Laptop / Air-Gapped</td>
                </tr>
                <tr>
                    <td><strong>Push Permissions</strong></td>
                    <td style="color: #F87171;">May push directly to protected branches</td>
                    <td style="color: #34D399; font-weight: 700;">PR only. Human review & sign-off mandatory</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- AIR-GAPPED & VPC HOSTING -->
    <div class="card card-purple">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; margin-bottom: 1.2rem;">
            <div>
                <h3 style="font-size: 1.25rem; color: #FFFFFF;">🏢 Enterprise Air-Gapped & Private VPC Deployment</h3>
                <p style="color: var(--text-muted); font-size: 0.88rem; margin-top: 0.3rem;">For banks, healthcare providers, and high-security defense contractors.</p>
            </div>
            <span class="pill pill-purple">ON-PREM & VPC READY</span>
        </div>
        <p style="color: var(--text-muted); font-size: 0.92rem; line-height: 1.6; margin-bottom: 1rem;">
            Because AIDEVOPS is 100% open source, your enterprise does not need to connect to any external third-party server. You can run the entire container stack inside your own private AWS VPC, Google Cloud Project, Microsoft Azure tenant, or air-gapped on-premise Kubernetes cluster.
        </p>
        <div class="grid-3">
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--glass-border); border-radius: 12px; padding: 1.1rem;">
                <div style="font-weight: 700; color: #C084FC; margin-bottom: 0.4rem;">🔐 Private VPC Boundaries</div>
                <div style="font-size: 0.85rem; color: #94A3B8;">Webhooks stay within your internal VPC subnet or via AWS PrivateLink / GCP Service Directory.</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--glass-border); border-radius: 12px; padding: 1.1rem;">
                <div style="font-weight: 700; color: #38BDF8; margin-bottom: 0.4rem;">🧠 Private Model Hosting</div>
                <div style="font-size: 0.85rem; color: #94A3B8;">Compatible with Google Cloud Vertex AI private endpoints or local open-weights Ollama/vLLM runners.</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--glass-border); border-radius: 12px; padding: 1.1rem;">
                <div style="font-weight: 700; color: #34D399; margin-bottom: 0.4rem;">📋 Full Audit Trail</div>
                <div style="font-size: 0.85rem; color: #94A3B8;">Every event, patch diff, and AST inspection is recorded into local immutable audit logs.</div>
            </div>
        </div>
    </div>

    <!-- SECURITY FAQ -->
    <div class="card card-pink">
        <h3 style="font-size: 1.25rem; color: #FFFFFF; margin-bottom: 1.5rem;">❓ Frequently Asked Security Questions</h3>
        
        <div style="margin-bottom: 1.3rem;">
            <div style="font-weight: 700; color: #EC4899; font-size: 1rem; margin-bottom: 0.3rem;">Q: If I give you my repository webhook, can you steal my proprietary code?</div>
            <div style="color: var(--text-muted); font-size: 0.9rem;">
                <strong>A: Absolutely NOT.</strong> A GitHub webhook does not give the receiver any access to your repository. It only delivers an outbound HTTP POST alerting that a workflow run has failed. To read the failure log or submit a PR, the agent uses <em>your own</em> token configured in <em>your own</em> environment. No outside entity ever has access.
            </div>
        </div>

        <div style="margin-bottom: 1.3rem;">
            <div style="font-weight: 700; color: #EC4899; font-size: 1rem; margin-bottom: 0.3rem;">Q: Does the AI agent ever push code straight to production or master?</div>
            <div style="color: var(--text-muted); font-size: 0.9rem;">
                <strong>A: Never.</strong> The agent is hard-coded to only create isolated feature branches (e.g. <code>fix/ci-failure-142</code>) and submit an official GitHub Pull Request with a full diff breakdown. A human engineer on your team must review, test, and approve the PR before it is ever merged.
            </div>
        </div>

        <div>
            <div style="font-weight: 700; color: #EC4899; font-size: 1rem; margin-bottom: 0.3rem;">Q: Where are my API keys and tokens stored?</div>
            <div style="color: var(--text-muted); font-size: 0.9rem;">
                <strong>A: Only on your machine.</strong> Your <code>GEMINI_API_KEY</code> and <code>GITHUB_TOKEN</code> stay strictly on your local machine inside your local <code>.env</code> file. They are never transmitted to any external analytics, monitoring, or third-party servers.
            </div>
        </div>
    </div>

    <!-- CTA BAR -->
    <div style="text-align: center; margin: 4rem 0 2rem 0;">
        <h3 style="font-size: 1.5rem; color: #FFFFFF; margin-bottom: 1rem;">Ready to Install on Your Laptop?</h3>
        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
            <a href="docs.html" class="btn-primary">📘 Go to Laptop Setup & Customization Guide &rarr;</a>
            <a href="https://github.com/Shubhamjkd01/AI_DevOps_X" target="_blank" class="btn-secondary">⭐ View GitHub Source Code</a>
        </div>
    </div>

    <footer>
        <p>AIDEVOPS — Open Source Autonomous DevOps Platform created by <strong style="color: #FFFFFF;">Shubham</strong> (@Shubhamjkd01).</p>
        <p style="margin-top: 0.4rem;">Zero-Trust Architecture. Built for developers and enterprise engineering teams.</p>
    </footer>
</div>
</body>
</html>
"""

# =========================================================================
# 3. GENERATE INDEX.HTML (HOMEPAGE WITH PROMINENT CARDS & DEV PROFILE)
# =========================================================================
index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>AIDEVOPS — Autonomous CI/CD Self-Healing Engine</title>
    {COMMON_HEAD}
</head>
<body>
<div class="container">
    {get_navbar('home')}

    <!-- HERO SECTION -->
    <div style="display: grid; grid-template-columns: 1.1fr 1fr; gap: 3.5rem; align-items: center; margin-bottom: 5rem;">
        <div>
            <div class="pill pill-cyan" style="margin-bottom: 1.2rem;">
                <span style="width: 8px; height: 8px; background: #00F2FE; border-radius: 50%; box-shadow: 0 0 8px #00F2FE;"></span>
                AUTONOMOUS CI/CD AGENT & PLATFORM
            </div>
            <h1 style="font-size: 3.4rem; font-weight: 800; line-height: 1.1; letter-spacing: -0.03em; margin-bottom: 1.25rem;">
                Turn CI/CD Failures into <span style="background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 50%, #EC4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Instant Pull Requests</span>
            </h1>
            <p style="font-size: 1.15rem; color: var(--text-muted); margin-bottom: 2rem; max-width: 580px;">
                Open-source self-healing engine powered by Google Gemini. Catches broken GitHub Actions runs, isolates stack traces, synthesizes AST-verified patches, and opens tested PRs in seconds.
            </p>
            <div style="display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;">
                <a href="docs.html" class="btn-primary">
                    📘 Laptop Setup Guide &rarr;
                </a>
                <a href="security.html" class="btn-secondary">
                    🛡️ Security & Privacy
                </a>
            </div>
        </div>

        <!-- HERO TERMINAL PREVIEW -->
        <div class="card card-cyan" style="padding: 1.5rem; margin-bottom: 0;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div style="display: flex; gap: 6px;">
                    <span style="width: 10px; height: 10px; border-radius: 50%; background: #EF4444; display: inline-block;"></span>
                    <span style="width: 10px; height: 10px; border-radius: 50%; background: #F59E0B; display: inline-block;"></span>
                    <span style="width: 10px; height: 10px; border-radius: 50%; background: #10B981; display: inline-block;"></span>
                </div>
                <div style="font-family: 'Fira Code', monospace; font-size: 0.75rem; color: #64748B;">agent://active-pipeline</div>
            </div>
            <pre style="margin: 0; font-size: 0.8rem; line-height: 1.6;"><code>[17:30:12] <span style="color:#F87171;">WEBHOOK: workflow_run #184 FAILED on main</span>
[17:30:13] <span style="color:#38BDF8;">ISOLATING: ModuleNotFoundError: No module named 'yaml'</span>
[17:30:14] <span style="color:#C084FC;">AI AGENT: Synthesizing patch via Gemini 2.5 Pro...</span>
[17:30:16] <span style="color:#34D399;">AST GUARD: Patch verified safe. (0 dangerous calls)</span>
[17:30:17] <span style="color:#FBBF24;">GIT: Created branch fix/ci-failure-184</span>
[17:30:18] <span style="color:#34D399;">SUCCESS: Pull Request #42 opened for human review! 🚀</span></code></pre>
        </div>
    </div>

    <!-- 2 MAIN FEATURE HUBS: DOCS & SECURITY -->
    <div class="grid-2" style="margin-bottom: 4rem;">
        <!-- CARD 1: DOCS & LAPTOP SETUP -->
        <div class="card card-purple" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div class="pill pill-purple" style="margin-bottom: 0.8rem;">STEP-BY-STEP MANUAL</div>
                <h2 style="font-size: 1.6rem; color: #FFFFFF; margin-bottom: 0.6rem;">📖 Documentation & Laptop Setup</h2>
                <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.2rem;">
                    Full developer guide showing <strong>where to change</strong> your <code>.env</code>, <code>server/config.py</code>, and how to connect GitHub Webhooks directly to your laptop using Ngrok or Docker.
                </p>
                <ul style="color: #CBD5E1; font-size: 0.88rem; margin-left: 1.2rem; line-height: 1.8; margin-bottom: 1.5rem;">
                    <li>Where to edit keys and configuration files</li>
                    <li>Connecting GitHub webhooks to localhost</li>
                    <li>Running FastAPI & Streamlit in parallel</li>
                    <li>Dry-run simulator command</li>
                </ul>
            </div>
            <a href="docs.html" class="btn-primary" style="align-self: flex-start;">
                Explore Laptop Setup Guide &rarr;
            </a>
        </div>

        <!-- CARD 2: SECURITY & DATA GUARANTEE -->
        <div class="card card-emerald" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div class="pill pill-emerald" style="margin-bottom: 0.8rem;">ENTERPRISE SAFETY</div>
                <h2 style="font-size: 1.6rem; color: #FFFFFF; margin-bottom: 0.6rem;">🛡️ Data & Code Security Guarantee</h2>
                <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.2rem;">
                    Wondering if your private repository code is safe? Read our formal zero-trust privacy guarantee: <strong>zero code retention</strong>, outbound-only webhooks, AST safety parsing, and 100% self-hostable.
                </p>
                <ul style="color: #CBD5E1; font-size: 0.88rem; margin-left: 1.2rem; line-height: 1.8; margin-bottom: 1.5rem;">
                    <li>Why webhooks grant zero repository code access</li>
                    <li>Ephemeral memory: code is never stored or trained on</li>
                    <li>Least-privilege fine-grained GitHub token scoping</li>
                    <li>Air-gapped and VPC self-hosting architecture</li>
                </ul>
            </div>
            <a href="security.html" class="btn-primary" style="align-self: flex-start; background: linear-gradient(135deg, #10B981 0%, #06B6D4 100%); box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4);">
                Read Security Guarantees &rarr;
            </a>
        </div>
    </div>

    <!-- ABOUT DEVELOPER SECTION -->
    <div class="card card-pink" id="about-author" style="margin-bottom: 4rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; margin-bottom: 1.5rem;">
            <div>
                <div class="pill pill-pink" style="margin-bottom: 0.5rem;">CREATOR SPOTLIGHT</div>
                <h2 style="font-size: 1.6rem; color: #FFFFFF; margin: 0;">👨‍💻 About the Developer</h2>
            </div>
            <span class="pill pill-cyan">OPEN SOURCE ARCHITECT</span>
        </div>

        <div style="display: grid; grid-template-columns: 200px 1fr; gap: 2.5rem; align-items: center;">
            <div style="text-align: center;">
                <div style="position: relative; width: 170px; height: 170px; margin: 0 auto;">
                    <img src="data:image/png;base64,{dev_img_b64}" alt="Shubham" style="width: 170px; height: 170px; border-radius: 50%; object-fit: cover; border: 3px solid #8B5CF6; box-shadow: 0 0 25px rgba(139, 92, 246, 0.6);" />
                    <span style="position: absolute; bottom: 8px; right: 12px; width: 18px; height: 18px; background: #10B981; border-radius: 50%; border: 3px solid #0D111C; box-shadow: 0 0 10px #10B981;"></span>
                </div>
                <div style="margin-top: 0.8rem; font-weight: 800; font-size: 1.15rem; color: #FFFFFF;">Shubham</div>
                <div style="color: #38BDF8; font-size: 0.82rem; font-weight: 600;">@Shubhamjkd01</div>
            </div>

            <div>
                <h3 style="font-size: 1.3rem; color: #FFFFFF; margin-bottom: 0.6rem;">Hey! I'm Shubham 👋</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1rem;">
                    I engineered <strong>AIDEVOPS</strong> to solve one of the most frustrating bottlenecks in software engineering: waiting hours for failed CI/CD pipelines and manually diagnosing repetitive syntax errors, missing packages, and broken Docker builds.
                </p>
                <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.2rem;">
                    By combining Google Gemini's reasoning with AST safety checks and GitHub webhooks, this engine autonomously heals build failures while guaranteeing <strong>complete code privacy and zero vendor lock-in</strong>.
                </p>
                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1.5rem;">
                    <span class="pill pill-purple">AI / ML Systems</span>
                    <span class="pill pill-cyan">DevOps & CI/CD</span>
                    <span class="pill pill-emerald">FastAPI & Python</span>
                    <span class="pill pill-pink">Open Source</span>
                </div>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <a href="https://github.com/Shubhamjkd01" target="_blank" class="btn-primary">
                        🐙 Follow on GitHub
                    </a>
                    <a href="https://github.com/Shubhamjkd01/AI_DevOps_X" target="_blank" class="btn-secondary">
                        ⭐ Star AI_DevOps_X Repo
                    </a>
                </div>
            </div>
        </div>
    </div>

    <footer>
        <p>AIDEVOPS — Open Source Autonomous DevOps Platform created by <strong style="color: #FFFFFF;">Shubham</strong> (@Shubhamjkd01).</p>
        <p style="margin-top: 0.4rem;">Zero-Trust Architecture. Built for developers and enterprise engineering teams.</p>
    </footer>
</div>
</body>
</html>
"""

# Write all three files
with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)
print("SUCCESS: Generated index.html")

with open(os.path.join(BASE_DIR, "docs.html"), "w", encoding="utf-8") as f:
    f.write(docs_html)
print("SUCCESS: Generated docs.html")

with open(os.path.join(BASE_DIR, "security.html"), "w", encoding="utf-8") as f:
    f.write(security_html)
print("SUCCESS: Generated security.html")
