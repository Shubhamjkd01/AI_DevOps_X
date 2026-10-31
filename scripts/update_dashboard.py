import os

with open('dashboard.py', 'r', encoding='utf-8') as f:
    code = f.read()

m1 = "# ==========================================\n# HERO SECTION (EXACT LAYOUT AS IMAGE)\n# =========================================="
m2 = "# ==========================================\n# 2. CONSOLIDATED DOCUMENTATION & SETUP GUIDANCE\n# =========================================="
m3 = "# ==========================================\n# 3. DATA & REPOSITORY CODE SECURITY GUARANTEE\n# =========================================="
m4 = "# ==========================================\n# 3. ABOUT THE DEVELOPER (SHUBHAM)\n# =========================================="

parts_pre = code.split(m1)[0]
rest1 = code.split(m1)[1]

hero_and_engine = rest1.split(m2)[0]
rest2 = rest1.split(m2)[1]

docs_section = rest2.split(m3)[0]
rest3 = rest2.split(m3)[1]

security_section = rest3.split(m4)[0]
about_section = rest3.split(m4)[1]

# Indent helper
def indent_block(text, spaces=4):
    lines = text.split("\n")
    return "\n".join((" " * spaces + line if line.strip() else "") for line in lines)

where_to_change_docs = '''
st.markdown("""
<div class="guide-card guide-card-pink" style="margin-bottom: 2rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem; flex-wrap: wrap; gap: 0.5rem;">
        <div>
            <h3 style="margin: 0; color: #FFFFFF; font-size: 1.3rem;">📁 Where to Change & What to Edit on Your Laptop</h3>
            <p style="margin: 0.3rem 0 0 0; color: #94A3B8; font-size: 0.88rem;">
                Exact file-by-file developer reference. The only 4 files you ever need to touch when setting up on your machine.
            </p>
        </div>
        <span style="background: rgba(236, 72, 153, 0.15); border: 1px solid rgba(236, 72, 153, 0.4); color: #F472B6; padding: 0.35rem 0.9rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700;">
            ● CRITICAL REFERENCE
        </span>
    </div>
    
    <table class="preview-table" style="margin-top: 1rem;">
        <thead>
            <tr>
                <th style="width: 25%;">FILE PATH</th>
                <th style="width: 30%;">VARIABLES / KEYS TO EDIT</th>
                <th style="width: 45%;">WHY & WHEN TO CHANGE IT</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong style="color: #F472B6;">.env</strong><br><span style="font-size: 0.72rem; color: #EC4899; font-weight: 700;">★ MOST IMPORTANT</span></td>
                <td>
                    <code>GEMINI_API_KEY</code><br>
                    <code>GITHUB_TOKEN</code><br>
                    <code>GITHUB_WEBHOOK_SECRET</code>
                </td>
                <td style="color: #CBD5E1; font-size: 0.84rem;">
                    <strong>1.</strong> Paste your free key from Google AI Studio.<br>
                    <strong>2.</strong> Add GitHub Personal Access Token (PAT) with <code>Actions: Read</code> and <code>Pull Requests: Read/Write</code>.<br>
                    <strong>3.</strong> Set a webhook secret password. Never commit this file to git!
                </td>
            </tr>
            <tr>
                <td><strong style="color: #38BDF8;">server/config.py</strong></td>
                <td>
                    <code>MODEL_NAME = "gemini-2.5-pro"</code><br>
                    <code>TEMPERATURE = 0.2</code><br>
                    <code>DEFAULT_PORT = 7860</code>
                </td>
                <td style="color: #CBD5E1; font-size: 0.84rem;">
                    Switch models (e.g. <code>gemini-1.5-flash</code> for 3x speed or <code>gemini-2.5-pro</code> for multi-file deep reasoning), adjust sampling temperature, or change the backend port.
                </td>
            </tr>
            <tr>
                <td><strong style="color: #C084FC;">github_agent/agent.py</strong></td>
                <td>
                    <code>BRANCH_PREFIX = "fix/ci-failure-"</code><br>
                    <code>AST_CHECK_ENABLED = True</code>
                </td>
                <td style="color: #CBD5E1; font-size: 0.84rem;">
                    Configure your team's custom branch naming convention (e.g. <code>hotfix/ci-</code> or <code>bot/fix-</code>) or tune commit and pull request body templates.
                </td>
            </tr>
            <tr>
                <td><strong style="color: #34D399;">server/app.py</strong></td>
                <td>
                    <code>/webhook/github</code> route<br>
                    Slack / Discord webhooks
                </td>
                <td style="color: #CBD5E1; font-size: 0.84rem;">
                    Add custom team notifications to ping Slack, Microsoft Teams, or Discord channels whenever a PR is created.
                </td>
            </tr>
        </tbody>
    </table>
</div>
""", unsafe_allow_html=True)
'''

security_comparison_table = '''
st.markdown("""
<div class="guide-card guide-card-cyan" style="margin-top: 2rem;">
    <h3 style="margin: 0 0 1.2rem 0; color: #FFFFFF; font-size: 1.25rem;">⚖️ Security Architecture: Traditional SaaS vs. AIDEVOPS Zero-Trust</h3>
    <table class="preview-table">
        <thead>
            <tr>
                <th>SECURITY DIMENSION</th>
                <th>TRADITIONAL 3RD-PARTY SAAS</th>
                <th style="color: #34D399;">AIDEVOPS ZERO-TRUST ENGINE</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Repository Code Access</strong></td>
                <td style="color: #F87171;">Full OAuth / Admin Read & Write to all repos</td>
                <td style="color: #34D399; font-weight: 700;">Strictly Least-Privilege (Actions + PRs only)</td>
            </tr>
            <tr>
                <td><strong>Source Code Storage</strong></td>
                <td style="color: #F87171;">Stored on external cloud databases</td>
                <td style="color: #34D399; font-weight: 700;">Zero code stored. Ephemeral in-memory only</td>
            </tr>
            <tr>
                <td><strong>AI Model Training</strong></td>
                <td style="color: #F87171;">Customer code often used to train vendor models</td>
                <td style="color: #34D399; font-weight: 700;">Never trained on. Zero data retention policy</td>
            </tr>
            <tr>
                <td><strong>Deployment Isolation</strong></td>
                <td style="color: #F87171;">Shared multi-tenant cloud server</td>
                <td style="color: #34D399; font-weight: 700;">100% Self-Hostable in your own VPC / Laptop</td>
            </tr>
            <tr>
                <td><strong>Push Permissions</strong></td>
                <td style="color: #F87171;">May push directly to main / production branches</td>
                <td style="color: #34D399; font-weight: 700;">PR only. Human review & sign-off mandatory</td>
            </tr>
        </tbody>
    </table>
</div>
""", unsafe_allow_html=True)
'''

nav_selector = '''
st.markdown("""
<style>
div[data-testid="stRadio"] > div {
    display: flex;
    justify-content: center;
    gap: 0.8rem;
    flex-wrap: wrap;
    background: rgba(13, 17, 28, 0.6);
    padding: 0.5rem 1rem;
    border-radius: 9999px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 2.5rem;
}
div[data-testid="stRadio"] label {
    background: transparent !important;
    padding: 0.4rem 1.2rem !important;
    border-radius: 9999px !important;
    font-weight: 700 !important;
    font-size: 0.86rem !important;
    color: #94A3B8 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stRadio"] label:hover {
    color: #38BDF8 !important;
}
div[data-testid="stRadio"] label[data-checked="true"],
div[data-testid="stRadio"] div[aria-checked="true"] {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.25), rgba(139, 92, 246, 0.25)) !important;
    color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

nav_page = st.radio(
    "Choose View",
    [
        "⚡ Live Self-Healing Engine",
        "📖 Documentation & Laptop Setup Guide",
        "🛡️ Data & Code Security Guarantee",
        "👨‍💻 About Developer"
    ],
    horizontal=True,
    label_visibility="collapsed"
)
'''

new_code = parts_pre + "\n" + nav_selector + """

if nav_page == "⚡ Live Self-Healing Engine":
""" + indent_block(hero_and_engine, 4) + """

elif nav_page == "📖 Documentation & Laptop Setup Guide":
""" + indent_block(where_to_change_docs + "\n" + docs_section, 4) + """

elif nav_page == "🛡️ Data & Code Security Guarantee":
""" + indent_block(security_section + "\n" + security_comparison_table, 4) + """

elif nav_page == "👨‍💻 About Developer":
""" + indent_block(about_section, 4)

with open('dashboard.py', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("SUCCESS: Updated dashboard.py with interactive multi-page radio navigation!")
