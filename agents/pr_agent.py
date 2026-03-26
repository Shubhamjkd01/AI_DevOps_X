from services.llm import query_llm
from services.github import create_pull_request, create_branch, modify_file
import logging

logger = logging.getLogger(__name__)

def create_fix_pr(repo_full_name: str, fix_data: dict, run_id: int) -> str:
    """
    Generates a PR description and orchestrates GitHub API calls to create the PR.
    """
    logger.info("PR Agent: Preparing pull request...")
    prompt = f"PR Agent: Write a PR title and description for this fix: {fix_data['explanation']}"
    llm_response = query_llm(prompt)
    
    from github import Github, Auth
    import os
    g = Github(auth=Auth.Token(os.getenv("GITHUB_TOKEN")))
    repo = g.get_repo(repo_full_name)
    base_branch = repo.default_branch
    new_branch = f"fix/workflow-{run_id}"
    
    create_branch(repo_full_name, base_branch, new_branch)
    modify_file(repo_full_name, fix_data["file_path"], new_branch, fix_data["content"], "Automated fix by Agent")
    
    # Build Hackathon Winning PR Body
    reason = fix_data.get("explanation", "Identified issue in logs")
    priority = fix_data.get("priority", "HIGH")
    conf_math = fix_data.get("conf_reason", "")
    confidence_score = fix_data.get('confidence', 0.85)
    
    confidence_display = f"\n\n### AI Auto-Fix Details\n"
    confidence_display += f"**Priority:** {priority} 🚨\n"
    confidence_display += f"**Fix Summary:** Automated Patch applied to `{fix_data.get('file_path')}`\n"
    confidence_display += f"```diff\n{fix_data.get('patch_diff', '+ AI Patch Applied')}\n```\n"
    confidence_display += f"**Confidence:** {confidence_score * 100:.0f}% — {conf_math}\n"
    confidence_display += f"**Reason:** {reason}\n\n"
    
    # Sales Pitch / Hackathon points
    sales_pitch = "---\n"
    sales_pitch += "### 🧠 Why AI > Rule-based\n"
    sales_pitch += "> Traditional systems rely on regex/log rules. Our system uses contextual reasoning across logs + codebase.\n\n"
    sales_pitch += "### 🛡️ Safety Layer\n"
    sales_pitch += "1. Runs in Docker sandbox\n"
    sales_pitch += "2. Cannot touch production directly\n"
    sales_pitch += "3. PR requires human approval\n"

    is_draft = confidence_score < 0.5
    if is_draft:
        sales_pitch += "\n> ⚠️ **Low confidence fix — human review heavily required.**\n"

    full_body = llm_response + confidence_display + sales_pitch

    pr_url = create_pull_request(repo_full_name, "Automated Fix for CI Failure", new_branch, base_branch, full_body, labels=["AI-generated"], draft=is_draft)
    
    logger.info(f"PR Agent Output: Created PR at {pr_url}")
    return pr_url
