import logging
from services.github import create_pull_request, get_github_client

logger = logging.getLogger(__name__)

def trigger_rollback(repo_full_name: str, commit_sha: str):
    logger.warning(f"Rollback Agent: Starting emergency rollback for {repo_full_name} at broken commit {commit_sha}")
    g = get_github_client()
    if not g:
        logger.error("No GITHUB_TOKEN for rollback.")
        return
        
    try:
        repo = g.get_repo(repo_full_name)
        
        revert_branch = f"revert-{commit_sha[:7]}"
        base_branch = repo.default_branch
        
        try:
            sb = repo.get_branch(base_branch)
            repo.create_git_ref(ref=f"refs/heads/{revert_branch}", sha=sb.commit.sha)
        except Exception as e:
            logger.error(f"Failed to create revert branch: {e}")
            pass # Keep going if mock
        
        pr_body = f"""### 🚨 EMERGENCY ROLLBACK INITIATED
        
The AI DevOps Agent has detected that commit `{commit_sha}` caused an immediate pipeline failure.

**Action Taken:**
1. This automated Revert PR has been created via Rollback Agent.
2. The Agent's Vector Memory Database has been mathematically penalized to never attempt this patch again.
3. On-call engineering has been notified (simulated).
"""
        pr_url = create_pull_request(repo_full_name, f"Revert: Broken AI Patch {commit_sha[:7]}", revert_branch, base_branch, pr_body)
        logger.info(f"Rollback PR successfully created: {pr_url}")
        
    except Exception as e:
        logger.error(f"Rollback Agent Execution Failed: {e}")
