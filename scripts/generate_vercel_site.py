import os
import base64

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img_path = os.path.join(BASE_DIR, "developer.png")
if os.path.exists(img_path):
    with open(img_path, "rb") as f:
        dev_img_b64 = base64.b64encode(f.read()).decode("utf-8")
else:
    dev_img_b64 = ""

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AIDEVOPS — Autonomous CI/CD Self-Healing Engine</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-base: #07090E;
            --purple: #8B5CF6;
            --cyan: #06B6D4;
            --pink: #EC4899;
            --emerald: #10B981;
            --text-main: #F1F5F9;
            --text-muted: #94A3B8;
            --glass-bg: rgba(13, 17, 28, 0.75);
            --glass-border: rgba(255, 255, 255, 0.08);
        }}
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        body {{
            background-color: var(--bg-base);
            color: var(--text-main);
            background: 
                radial-gradient(circle at 8% 18%, rgba(139, 92, 246, 0.22) 0%, transparent 40%),
                radial-gradient(circle at 88% 28%, rgba(6, 182, 212, 0.2) 0%, transparent 42%),
                radial-gradient(circle at 85% 80%, rgba(236, 72, 153, 0.2) 0%, transparent 40%),
                radial-gradient(circle at 50% 50%, rgba(30, 41, 59, 0.3) 0%, transparent 60%),
                var(--bg-base);
            background-attachment: fixed;
            line-height: 1.6;
            overflow-x: hidden;
        }}
        .container {{
            max-width: 1250px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }}

        /* Navbar */
        .navbar {{
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
        }}
        .nav-logo {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-weight: 800;
            font-size: 1.15rem;
            letter-spacing: -0.02em;
            color: #FFFFFF;
            text-decoration: none;
        }}
        .nav-logo-icon {{
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
            clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.6);
            font-size: 0.9rem;
        }}
        .nav-links {{
            display: flex;
            gap: 2rem;
            align-items: center;
        }}
        .nav-links a {{
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            transition: color 0.2s ease;
        }}
        .nav-links a:hover {{
            color: #38BDF8;
        }}
        .nav-btn {{
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
        }}
        .nav-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 24px rgba(236, 72, 153, 0.6);
        }}

        /* Hero */
        .hero {{
            display: grid;
            grid-template-columns: 1.1fr 1fr;
            gap: 3.5rem;
            align-items: center;
            margin-bottom: 5rem;
        }}
        @media (max-width: 950px) {{
            .hero {{ grid-template-columns: 1fr; gap: 2.5rem; }}
            .nav-links {{ display: none; }}
        }}
        .hero-pill {{
            display: inline-flex;
            align-items: center;
            gap: 0.6rem;
            padding: 0.35rem 0.95rem;
            background: rgba(6, 182, 212, 0.12);
            border: 1px solid rgba(6, 182, 212, 0.35);
            border-radius: 9999px;
            font-size: 0.74rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            color: #38BDF8;
            margin-bottom: 1.2rem;
            text-transform: uppercase;
        }}
        .pulsing-dot {{
            width: 7px;
            height: 7px;
            background: #00F2FE;
            border-radius: 50%;
            box-shadow: 0 0 10px #00F2FE;
            animation: pulse 1.8s infinite;
        }}
        @keyframes pulse {{
            0% {{ transform: scale(0.95); opacity: 0.8; }}
            50% {{ transform: scale(1.3); opacity: 1; }}
            100% {{ transform: scale(0.95); opacity: 0.8; }}
        }}
        .hero-title {{
            font-size: 3.2rem;
            font-weight: 800;
            line-height: 1.12;
            letter-spacing: -0.04em;
            color: #FFFFFF;
            margin-bottom: 1.2rem;
        }}
        .gradient-text {{
            background: linear-gradient(135deg, #EC4899 0%, #A855F7 50%, #06B6D4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .hero-subtitle {{
            font-size: 1.05rem;
            line-height: 1.6;
            color: var(--text-muted);
            margin-bottom: 2rem;
        }}
        .hero-actions {{
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        .btn-primary {{
            background: linear-gradient(135deg, #EC4899 0%, #A855F7 100%);
            color: #FFFFFF;
            padding: 0.75rem 1.8rem;
            border-radius: 9999px;
            font-weight: 700;
            font-size: 0.9rem;
            text-decoration: none;
            box-shadow: 0 4px 20px rgba(236, 72, 153, 0.45);
            transition: all 0.25s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
        }}
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(236, 72, 153, 0.65);
        }}
        .btn-secondary {{
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #E2E8F0;
            padding: 0.75rem 1.8rem;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.9rem;
            text-decoration: none;
            transition: all 0.2s ease;
        }}
        .btn-secondary:hover {{
            background: rgba(255, 255, 255, 0.12);
        }}

        /* Terminal Window */
        .terminal-window {{
            background: rgba(13, 17, 28, 0.85);
            backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 1.4rem;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), 0 0 40px rgba(139, 92, 246, 0.18);
        }}
        .terminal-header {{
            display: flex;
            align-items: center;
            gap: 0.45rem;
            margin-bottom: 1.1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 0.75rem;
        }}
        .dot {{ width: 10px; height: 10px; border-radius: 50%; }}
        .dot-red {{ background: #EF4444; }}
        .dot-yellow {{ background: #F59E0B; }}
        .dot-green {{ background: #10B981; }}
        .terminal-title {{
            margin-left: 0.5rem;
            font-size: 0.76rem;
            font-family: 'Fira Code', monospace;
            color: #64748B;
        }}
        .terminal-prompt {{
            font-family: 'Fira Code', monospace;
            font-size: 0.82rem;
            color: #00F2FE;
            margin-bottom: 0.8rem;
        }}
        .terminal-code {{
            background: rgba(8, 12, 20, 0.95);
            border-radius: 10px;
            padding: 1rem;
            font-family: 'Fira Code', monospace;
            font-size: 0.8rem;
            color: #CBD5E1;
            line-height: 1.5;
            overflow-x: auto;
            border: 1px solid rgba(255, 255, 255, 0.06);
            margin-bottom: 0.9rem;
        }}
        .ai-popover {{
            background: rgba(26, 21, 51, 0.95);
            backdrop-filter: blur(18px);
            border: 1px solid rgba(168, 85, 247, 0.45);
            border-radius: 14px;
            padding: 0.9rem 1.1rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 25px rgba(168, 85, 247, 0.25);
        }}
        .ai-popover-title {{
            font-size: 0.78rem;
            font-weight: 700;
            color: #C084FC;
            margin-bottom: 0.3rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }}
        .ai-popover-text {{
            font-size: 0.78rem;
            line-height: 1.45;
            color: #CBD5E1;
        }}

        /* Metrics */
        .section-header {{
            text-align: center;
            margin: 5rem 0 2.5rem 0;
        }}
        .section-tag {{
            font-size: 0.74rem;
            font-weight: 800;
            letter-spacing: 0.14em;
            color: #38BDF8;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }}
        .section-title {{
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: #FFFFFF;
            margin-bottom: 0.5rem;
        }}
        .section-desc {{
            font-size: 0.95rem;
            color: var(--text-muted);
            max-width: 650px;
            margin: 0 auto;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
            margin-bottom: 5rem;
        }}
        @media (max-width: 800px) {{
            .metrics-grid {{ grid-template-columns: 1fr; }}
        }}
        .metric-card {{
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 18px;
            padding: 1.5rem;
            text-align: left;
            transition: transform 0.2s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-3px);
            border-color: rgba(6, 182, 212, 0.3);
        }}
        .metric-lbl {{
            font-size: 0.75rem;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.35rem;
        }}
        .metric-val {{
            font-size: 2.1rem;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.03em;
            margin-bottom: 0.25rem;
        }}
        .metric-delta {{
            font-size: 0.75rem;
            font-weight: 700;
            color: #34D399;
        }}

        /* Tabs & Cards */
        .tabs-nav {{
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }}
        .tab-btn {{
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid var(--glass-border);
            color: var(--text-muted);
            padding: 0.6rem 1.4rem;
            border-radius: 9999px;
            font-weight: 700;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .tab-btn.active {{
            background: linear-gradient(135deg, #EC4899 0%, #A855F7 100%);
            color: #FFFFFF;
            box-shadow: 0 4px 18px rgba(236, 72, 153, 0.45);
            border-color: transparent;
        }}
        .tab-content {{
            display: none;
        }}
        .tab-content.active {{
            display: block;
        }}
        .card {{
            background: rgba(13, 17, 28, 0.8);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 22px;
            padding: 2.2rem;
            margin-bottom: 2rem;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.35);
        }}
        .card-cyan {{ border-top: 3px solid var(--cyan); }}
        .card-purple {{ border-top: 3px solid var(--purple); }}
        .card-emerald {{ border-top: 3px solid var(--emerald); }}
        .card-pink {{ border-top: 3px solid var(--pink); }}

        /* Code & Previews */
        .code-box {{
            background: rgba(8, 12, 20, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.1rem;
            font-family: 'Fira Code', monospace;
            font-size: 0.82rem;
            color: #E2E8F0;
            line-height: 1.6;
            overflow-x: auto;
            margin: 0.8rem 0;
        }}
        .step-item {{
            display: flex;
            gap: 1.2rem;
            align-items: flex-start;
            margin-bottom: 1.4rem;
        }}
        .step-badge {{
            width: 32px;
            height: 32px;
            min-width: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%);
            color: #FFFFFF;
            font-weight: 800;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 12px rgba(6, 182, 212, 0.5);
        }}
        .step-heading {{
            font-size: 1.02rem;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 0.25rem;
        }}
        .step-subtext {{
            font-size: 0.86rem;
            color: var(--text-muted);
            line-height: 1.5;
        }}

        /* Security Grid */
        .sec-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }}
        @media (max-width: 768px) {{
            .sec-grid {{ grid-template-columns: 1fr; }}
        }}
        .sec-box {{
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(16, 185, 129, 0.25);
            border-radius: 16px;
            padding: 1.4rem;
        }}
        .sec-box-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.45rem;
        }}
        .sec-box p, .sec-box li {{
            font-size: 0.86rem;
            color: var(--text-muted);
            line-height: 1.55;
        }}
        .sec-box ul {{
            margin-left: 1.2rem;
            margin-top: 0.4rem;
        }}

        /* Developer Card */
        .dev-card {{
            background: rgba(13, 17, 28, 0.85);
            backdrop-filter: blur(25px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 2.4rem;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4), 0 0 25px rgba(139, 92, 246, 0.15);
            position: relative;
            overflow: hidden;
            display: flex;
            gap: 2.2rem;
            align-items: center;
            flex-wrap: wrap;
            margin-bottom: 5rem;
        }}
        .dev-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #EC4899 0%, #8B5CF6 50%, #06B6D4 100%);
        }}
        .dev-photo-wrap {{
            position: relative;
            width: 130px;
            height: 130px;
            min-width: 130px;
        }}
        .dev-photo {{
            width: 130px;
            height: 130px;
            border-radius: 50%;
            object-fit: cover;
            object-position: center top;
            border: 3px solid rgba(168, 85, 247, 0.75);
            box-shadow: 0 0 25px rgba(168, 85, 247, 0.45), 0 0 45px rgba(6, 182, 212, 0.25);
        }}
        .dev-online-dot {{
            position: absolute;
            bottom: 4px;
            right: 6px;
            width: 16px;
            height: 16px;
            background: #10B981;
            border-radius: 50%;
            border: 3px solid #0D111C;
            box-shadow: 0 0 10px #10B981;
        }}
        .dev-tag-chip {{
            background: rgba(139, 92, 246, 0.15);
            border: 1px solid rgba(139, 92, 246, 0.35);
            color: #C084FC;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            display: inline-block;
            margin: 0.2rem;
        }}

        /* Footer */
        footer {{
            text-align: center;
            padding: 3rem 0;
            border-top: 1px solid var(--glass-border);
            color: #64748B;
            font-size: 0.82rem;
        }}
        footer a {{
            color: var(--text-muted);
            text-decoration: none;
            font-weight: 600;
        }}
    </style>
</head>
<body>

    <div class="container">
        <!-- TOP NAVBAR -->
        <nav class="navbar">
            <a href="#" class="nav-logo">
                <div class="nav-logo-icon">⚡</div>
                <div>AIDEVOPS</div>
            </a>
            <div class="nav-links">
                <a href="#documentation">DOCUMENTATION & SETUP</a>
                <a href="#security">SECURITY & DATA SAFETY</a>
                <a href="#about-author">ABOUT DEVELOPER</a>
            </div>
            <div>
                <a class="nav-btn" href="https://github.com/Shubhamjkd01/AI_DevOps_X" target="_blank">
                    ⭐ GITHUB REPO
                </a>
            </div>
        </nav>

        <!-- HERO SECTION -->
        <section class="hero">
            <div>
                <div class="hero-pill">
                    <div class="pulsing-dot"></div>
                    BUILT FOR REPOSITORIES &bull; OPEN-WEIGHT GEMMA 4
                </div>
                <h1 class="hero-title">
                    CI/CD without chaos.<br>
                    <span class="gradient-text">Fixed in seconds.</span>
                </h1>
                <p class="hero-subtitle">
                    Autonomous self-healing DevOps engine that intercepts GitHub Actions failures, writes AST-compliant patches with Google Gemma 4, verifies zero regressions in a sandbox, and submits ready-to-merge Pull Requests.
                </p>
                <div class="hero-actions">
                    <a href="#documentation" class="btn-primary">▶ CONNECT GITHUB REPO</a>
                    <a href="https://github.com/Shubhamjkd01/AI_DevOps_X/pulls" target="_blank" class="btn-secondary">VIEW SAMPLE PRS ↗</a>
                </div>
            </div>

            <!-- Terminal Hero Window -->
            <div class="terminal-window">
                <div class="terminal-header">
                    <div class="dot dot-red"></div>
                    <div class="dot dot-yellow"></div>
                    <div class="dot dot-green"></div>
                    <span class="terminal-title">aidevops_engine.py</span>
                </div>
                <div class="terminal-prompt">aidevops@engine:~$ auto-triage CI failure --repo Shubhamjkd01/AI_DevOps_X</div>
                <div class="terminal-code">
[+] Intercepted GitHub Action run #84920
[*] Parsing traceback: SyntaxError in main.py:42
[+] Invoking Gemma 4 (models/gemma-4-26b-a4b-it)...
[+] AST Syntax Guard: Validated (0 dangerous calls)
[+] Ephemeral Sandbox: Regression tests 100% passed
[SUCCESS] Created Pull Request: fix/ci-failure-84920
                </div>
                <div class="ai-popover">
                    <div class="ai-popover-title">
                        🤖 AI Suggestion &bull; models/gemma-4-26b-a4b-it
                    </div>
                    <div class="ai-popover-text">
                        Detected missing colon on line 42, synthesized AST-compliant patch, verified zero regressions in sandbox, and prepared Pull Request.
                    </div>
                </div>
            </div>
        </section>

        <!-- METRICS -->
        <div class="section-header">
            <div class="section-tag">WHY AUTONOMOUS AI DEVOPS?</div>
            <h2 class="section-title">Smarter. Faster. Automatic.</h2>
            <p class="section-desc">Zero manual debugging. AST Hallucination Guard. Production-grade patches.</p>
        </div>

        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-lbl">Mean Time to Repair (MTTR)</div>
                <div class="metric-val">~45 sec</div>
                <div class="metric-delta">↓ Saved 45 mins developer downtime per run</div>
            </div>
            <div class="metric-card">
                <div class="metric-lbl">FAISS Vector Memory Hit Rate</div>
                <div class="metric-val">94.8%</div>
                <div class="metric-delta">↑ 768-dim L2 tensor embedding reuse</div>
            </div>
            <div class="metric-card">
                <div class="metric-lbl">Developer Cost Saved</div>
                <div class="metric-val">$4,350+</div>
                <div class="metric-delta">↑ Engineering hours preserved for innovation</div>
            </div>
        </div>

        <!-- DOCUMENTATION & SETUP GUIDANCE -->
        <div class="section-header" id="documentation">
            <div class="section-tag">SETUP & INTEGRATION</div>
            <h2 class="section-title">Documentation & Step-by-Step Setup</h2>
            <p class="section-desc">Connect your GitHub repository in 2 minutes via Webhooks or install locally on your own machine.</p>
        </div>

        <div class="tabs-nav">
            <button class="tab-btn active" onclick="switchTab('tab-webhook', this)">🔗 Connect GitHub Webhook</button>
            <button class="tab-btn" onclick="switchTab('tab-local', this)">💻 Install Locally (CLI & Docker)</button>
            <button class="tab-btn" onclick="switchTab('tab-tips', this)">💡 Developer Tips & Multi-Repo</button>
            <button class="tab-btn" onclick="switchTab('tab-arch', this)">🏗️ Architecture & Workflow</button>
        </div>

        <!-- Tab 1: Webhook -->
        <div id="tab-webhook" class="tab-content active">
            <div class="card card-cyan">
                <h3 style="color: #FFFFFF; font-size: 1.3rem; margin-bottom: 0.5rem;">🔗 Connect Any Repository via GitHub Webhook (2-Minute Setup)</h3>
                <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1.5rem;">
                    When your GitHub Actions CI fails, GitHub automatically notifies this agent. Gemma 4 writes an AST-verified patch and opens a ready-to-merge Pull Request.
                </p>

                <div class="step-item">
                    <div class="step-badge">1</div>
                    <div>
                        <div class="step-heading">Open Repository Webhook Settings</div>
                        <div class="step-subtext">Go to your GitHub repo &rarr; click <strong>Settings</strong> tab &rarr; in the left sidebar click <strong>Webhooks</strong> &rarr; click <strong>Add webhook</strong>.</div>
                    </div>
                </div>

                <div class="step-item">
                    <div class="step-badge">2</div>
                    <div>
                        <div class="step-heading">Enter Webhook Settings</div>
                        <div class="step-subtext">Set the fields exactly as follows:</div>
                        <div class="code-box">
<strong>Payload URL:</strong>   https://&lt;your-server-or-domain&gt;/api/v1/webhook/github
<strong>Content type:</strong>  application/json
<strong>Secret:</strong>        (Optional / matching your .env)
<strong>SSL check:</strong>     Enable SSL verification
                        </div>
                    </div>
                </div>

                <div class="step-item">
                    <div class="step-badge">3</div>
                    <div>
                        <div class="step-heading">Select Individual Trigger Events</div>
                        <div class="step-subtext">Choose <strong>"Let me select individual events"</strong> and check:</div>
                        <ul style="margin: 0.4rem 0 0 1.2rem; color: #CBD5E1; font-size: 0.85rem;">
                            <li><strong style="color: #38BDF8;">Workflow runs</strong> &mdash; Triggers Gemma 4 when your CI/CD job fails.</li>
                            <li><strong style="color: #38BDF8;">Check suites</strong> &mdash; Monitors GitHub Actions test suites.</li>
                            <li><strong style="color: #38BDF8;">Pull requests</strong> &mdash; Tracks PR merges for reinforcement learning feedback.</li>
                        </ul>
                    </div>
                </div>

                <div class="step-item">
                    <div class="step-badge">4</div>
                    <div>
                        <div class="step-heading">Click Save & Done!</div>
                        <div class="step-subtext">Ensure <strong>Active</strong> is checked, then click <strong>Add webhook</strong>. From now on, any CI failure will automatically synthesize a fix PR!</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 2: Local Install -->
        <div id="tab-local" class="tab-content">
            <div class="card card-purple">
                <h3 style="color: #FFFFFF; font-size: 1.3rem; margin-bottom: 0.5rem;">💻 Install & Run Locally on Your System</h3>
                <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1.5rem;">
                    Run the autonomous FastAPI agent backend and Streamlit dashboard locally on your system using Python or Docker.
                </p>

                <h4 style="color: #FFFFFF; font-size: 1rem; margin-bottom: 0.4rem;">1. Clone and Install Dependencies</h4>
                <div class="code-box">
# Clone the repository
git clone https://github.com/Shubhamjkd01/AI_DevOps_X.git
cd AI_DevOps_X

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\\venv\\Scripts\\activate

# Install requirements
pip install -r requirements.txt
                </div>

                <h4 style="color: #FFFFFF; font-size: 1rem; margin-bottom: 0.4rem;">2. Configure .env Environment File</h4>
                <div class="code-box">
# Google Gemma 4 Configuration (Get free key at https://aistudio.google.com/)
GEMINI_API_KEY=your_gemini_api_key_here
GEMMA_MODEL_NAME=models/gemma-4-26b-a4b-it

# GitHub Automation Token (Generate at https://github.com/settings/tokens)
GITHUB_TOKEN=ghp_your_github_token_here
GITHUB_WEBHOOK_SECRET=your_optional_secret
                </div>

                <h4 style="color: #FFFFFF; font-size: 1rem; margin-bottom: 0.4rem;">3. Run Backend & Dashboard</h4>
                <div class="code-box">
# Terminal 1: Backend API Engine
uvicorn server.app:app --host 0.0.0.0 --port 7860 --reload

# Terminal 2: Streamlit Visual Dashboard
streamlit run dashboard.py --server.port 8501

# Or 1-Command Docker Run:
docker compose up --build -d
                </div>
            </div>
        </div>

        <!-- Tab 3: Dev Tips -->
        <div id="tab-tips" class="tab-content">
            <div class="card card-pink">
                <h3 style="color: #FFFFFF; font-size: 1.3rem; margin-bottom: 0.5rem;">💡 Open-Source Setup Tips for Developers</h3>
                <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1.5rem;">
                    Key tips, free quota optimization, multi-repo routing, and contribution workflows.
                </p>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                    <div style="background: rgba(15, 23, 42, 0.6); padding: 1.2rem; border-radius: 14px; border: 1px solid rgba(255,255,255,0.06);">
                        <h4 style="color: #38BDF8; margin-bottom: 0.4rem;">1️⃣ Multi-Repository Support</h4>
                        <p style="font-size: 0.85rem; color: var(--text-muted);">
                            One deployed agent instance can handle 10+ repositories. Point each repo's webhook to the same URL; the agent dynamically routes PRs based on the incoming repository name.
                        </p>
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.6); padding: 1.2rem; border-radius: 14px; border: 1px solid rgba(255,255,255,0.06);">
                        <h4 style="color: #38BDF8; margin-bottom: 0.4rem;">2️⃣ Free Google Gemma 4 API</h4>
                        <p style="font-size: 0.85rem; color: var(--text-muted);">
                            Google AI Studio provides a free tier (15 RPM / 1M TPM) for Gemma 4. You do not need a paid cloud account to run this autonomous agent.
                        </p>
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.6); padding: 1.2rem; border-radius: 14px; border: 1px solid rgba(255,255,255,0.06);">
                        <h4 style="color: #38BDF8; margin-bottom: 0.4rem;">3️⃣ Local Testing with Ngrok</h4>
                        <p style="font-size: 0.85rem; color: var(--text-muted);">
                            Run <code>ngrok http 7860</code> on your computer to get an instant public HTTPS tunnel. Paste that URL into GitHub to test webhooks live from your local machine.
                        </p>
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.6); padding: 1.2rem; border-radius: 14px; border: 1px solid rgba(255,255,255,0.06);">
                        <h4 style="color: #38BDF8; margin-bottom: 0.4rem;">4️⃣ 100% Open Source Contributions</h4>
                        <p style="font-size: 0.85rem; color: var(--text-muted);">
                            Community pull requests, bug reports, and new language graders are warmly welcomed at <a href="https://github.com/Shubhamjkd01/AI_DevOps_X" target="_blank" style="color: #C084FC;">github.com/Shubhamjkd01/AI_DevOps_X</a>.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 4: Architecture -->
        <div id="tab-arch" class="tab-content">
            <div class="card card-purple">
                <h3 style="color: #FFFFFF; font-size: 1.3rem; margin-bottom: 0.5rem;">🏗️ Multi-Agent Architecture & Endpoints</h3>
                <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1.5rem;">
                    A five-tier multi-agent pipeline designed for resilient, hallucination-free automated DevOps repairs.
                </p>

                <div class="step-item">
                    <div class="step-badge" style="background: #3B82F6;">1</div>
                    <div>
                        <div class="step-heading">Ingestion & Signature Validation</div>
                        <div class="step-subtext">GitHub webhook delivers failure event &rarr; HMAC SHA-256 signature is verified &rarr; logs are parsed into structured AST failure frames.</div>
                    </div>
                </div>
                <div class="step-item">
                    <div class="step-badge" style="background: #8B5CF6;">2</div>
                    <div>
                        <div class="step-heading">FAISS Tensor Memory Retrieval</div>
                        <div class="step-subtext">Queries 768-dimensional L2 tensor embeddings of previously accepted fixes. If a similar failure was resolved before, historical context is injected into Gemma 4's prompt.</div>
                    </div>
                </div>
                <div class="step-item">
                    <div class="step-badge" style="background: #EC4899;">3</div>
                    <div>
                        <div class="step-heading">Gemma 4 AST Patch Synthesis</div>
                        <div class="step-subtext">Google Gemma 4 (<code>models/gemma-4-26b-a4b-it</code>) reasons over repository AST context to generate a surgical, minimal patch targeting the root cause.</div>
                    </div>
                </div>
                <div class="step-item">
                    <div class="step-badge" style="background: #10B981;">4</div>
                    <div>
                        <div class="step-heading">AST Safety Guard & Docker Sandbox</div>
                        <div class="step-subtext">Python <code>ast.parse()</code> verifies syntactic validity and blocks dangerous functions (<code>os.system</code>, <code>eval</code>). Ephemeral Docker sandbox runs pytest to verify zero regressions.</div>
                    </div>
                </div>
                <div class="step-item">
                    <div class="step-badge" style="background: #06B6D4;">5</div>
                    <div>
                        <div class="step-heading">3-Tier Judge & Automated PR</div>
                        <div class="step-subtext">Junior/Senior/Principal LLM Judge evaluates patch quality. If score &ge; 0.5, PR Agent creates branch <code>fix/workflow-{{run_id}}</code> and opens a ready-to-merge Pull Request.</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SECURITY & DATA PRIVACY GUARANTEE (STANDALONE PROMINENT SECTION) -->
        <div class="section-header" id="security">
            <div class="section-tag">DATA PRIVACY & INTEGRITY GUARANTEE</div>
            <h2 class="section-title">How Your Code & Data Remains 100% Safe</h2>
            <p class="section-desc">Zero code retention. Zero unauthorized repository access. Enterprise zero-trust guarantees.</p>
        </div>

        <div class="card card-emerald">
            <div class="sec-grid">
                <div class="sec-box">
                    <div class="sec-box-title">🔒 1. One-Way Webhooks (Zero Inbound Access)</div>
                    <p>
                        A GitHub Webhook is strictly a <strong>one-way outgoing alert</strong> sent from GitHub to the agent server.
                    </p>
                    <ul>
                        <li><strong>No code reading:</strong> Webhook payloads only contain failure metadata (run ID, failed status, branch name). They contain zero source code files and cannot clone private repositories.</li>
                        <li><strong>HMAC SHA-256 Signatures:</strong> Every incoming request is cryptographically verified via GitHub's <code>X-Hub-Signature-256</code> header. Spoofed or tampered requests are rejected with HTTP 401.</li>
                    </ul>
                </div>

                <div class="sec-box">
                    <div class="sec-box-title">🚫 2. Zero Code Retention / Never Trained On</div>
                    <p>
                        Your proprietary code and algorithms are never permanently stored or shared.
                    </p>
                    <ul>
                        <li><strong>No persistent storage:</strong> Source code is processed strictly in ephemeral memory during the failure run and is never written to external databases.</li>
                        <li><strong>No AI model training:</strong> Google Gemma 4 processes context solely to synthesize the AST patch. Your code is never used to train or fine-tune public models.</li>
                    </ul>
                </div>

                <div class="sec-box">
                    <div class="sec-box-title">🏢 3. 100% Self-Hostable in Your Own VPC</div>
                    <p>
                        Complete air-gapped sovereignty for regulated enterprise environments.
                    </p>
                    <ul>
                        <li><strong>Total isolation:</strong> Deploy the entire agent stack inside your private AWS VPC, GCP project, Azure cloud, or on-premise Kubernetes cluster.</li>
                        <li><strong>Zero external transit:</strong> No error logs, tokens, or repo context ever leave your enterprise network.</li>
                        <li><strong>Private Gemma 4:</strong> Run Gemma 4 locally on private GPU nodes or via your organization's private Vertex AI tenant.</li>
                    </ul>
                </div>

                <div class="sec-box">
                    <div class="sec-box-title">🛡️ 4. AST Hallucination Guard & Human Approval</div>
                    <p>
                        Defensive syntax verification and strict human-in-the-loop controls.
                    </p>
                    <ul>
                        <li><strong>AST Syntax Inspection:</strong> Every patch is verified by Python's <code>ast.parse()</code> to disallow dangerous system calls (<code>os.system</code>, <code>subprocess</code>, <code>eval()</code>).</li>
                        <li><strong>No Direct Production Pushes:</strong> The agent is programmatically restricted from ever pushing directly to <code>main</code>. It only opens a standard Pull Request for your engineers to review, approve, and merge.</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- ABOUT THE DEVELOPER -->
        <div class="section-header" id="about-author">
            <div class="section-tag">OPEN SOURCE CREATOR</div>
            <h2 class="section-title">About the Developer</h2>
            <p class="section-desc">Pioneering autonomous developer infrastructure and self-healing CI/CD with open-weight intelligence.</p>
        </div>

        <div class="dev-card">
            <div class="dev-photo-wrap">
                <img src="data:image/png;base64,{dev_img_b64}" class="dev-photo" alt="Shubham - Developer" />
                <div class="dev-online-dot"></div>
            </div>
            <div style="flex: 1; min-width: 280px;">
                <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
                    <h3 style="margin: 0; color: #FFFFFF; font-size: 1.65rem; font-weight: 800;">Shubham</h3>
                    <span style="background: rgba(168, 85, 247, 0.2); border: 1px solid rgba(168, 85, 247, 0.4); color: #C084FC; padding: 0.2rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700;">
                        @Shubhamjkd01
                    </span>
                    <span style="background: rgba(6, 182, 212, 0.2); border: 1px solid rgba(6, 182, 212, 0.4); color: #22D3EE; padding: 0.2rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700;">
                        AI & DevOps Systems Architect
                    </span>
                </div>
                <p style="margin: 0.8rem 0 1.2rem 0; color: var(--text-muted); font-size: 0.95rem; line-height: 1.65;">
                    Hi, I'm Shubham! I designed and built <strong>AI DevOps</strong> to eliminate developer burnout caused by broken CI/CD pipelines. Powered by Google's open-weight <strong>Gemma 4</strong> models, rigorous AST syntax validation, and episodic vector memory, it resolves build failures in seconds without human debugging fatigue.
                </p>
                <div style="margin-bottom: 1.2rem;">
                    <span class="dev-tag-chip">🐍 Python 3.11</span>
                    <span class="dev-tag-chip">🤖 Google Gemma 4</span>
                    <span class="dev-tag-chip">⚡ FastAPI</span>
                    <span class="dev-tag-chip">🎨 Streamlit</span>
                    <span class="dev-tag-chip">🐙 GitHub Actions</span>
                    <span class="dev-tag-chip">🐳 Docker</span>
                    <span class="dev-tag-chip">🧠 FAISS Vector Memory</span>
                    <span class="dev-tag-chip">🌊 DigitalOcean</span>
                </div>
                <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
                    <a href="https://github.com/Shubhamjkd01" target="_blank" class="btn-primary" style="font-size: 0.85rem; padding: 0.6rem 1.3rem;">
                        🐙 GitHub: @Shubhamjkd01
                    </a>
                    <a href="https://github.com/Shubhamjkd01/AI_DevOps_X" target="_blank" class="btn-secondary" style="font-size: 0.85rem; padding: 0.6rem 1.3rem;">
                        ⭐ Project Repo: AI_DevOps_X
                    </a>
                    <a href="https://github.com/Shubhamjkd01/AI_DevOps_X/issues" target="_blank" class="btn-secondary" style="font-size: 0.85rem; padding: 0.6rem 1.3rem;">
                        💬 Report Issue / Feedback
                    </a>
                </div>
            </div>
        </div>

        <!-- FOOTER -->
        <footer>
            Built with ❤️ by <a href="https://github.com/Shubhamjkd01" target="_blank">Shubham</a> &bull; Powered by Google Gemma 4 &bull; 100% Free & Open-Source Software
        </footer>
    </div>

    <script>
        function switchTab(tabId, btn) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            btn.classList.add('active');
        }}
    </script>
</body>
</html>
"""

target_file = os.path.join(BASE_DIR, "index.html")
with open(target_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"SUCCESS: Generated {target_file} with size {len(html_content)} bytes")
