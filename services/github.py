import os
import logging
import requests
from github import Github, Auth
from github.GithubException import GithubException

logger = logging.getLogger(__name__)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_github_client():
    if not GITHUB_TOKEN:
        return None
    auth = Auth.Token(GITHUB_TOKEN)
    return Github(auth=auth)

def fetch_workflow_logs(repo_full_name: str, run_id: int) -> str:
    """
    Fetches the logs for a specific workflow run.
    """
    g = get_github_client()
    if not g:
        logger.warning("No GITHUB_TOKEN. Returning mock logs.")
        return "MOCK_LOG: Error: SyntaxError: invalid syntax in app/main.py line 42"
        
    try:
        repo = g.get_repo(repo_full_name)
        run = repo.get_workflow_run(run_id)
        logs_url = run.logs_url
        response = requests.get(logs_url, headers={"Authorization": f"Bearer {GITHUB_TOKEN}"})
        if response.status_code == 200:
            return f"Logs successfully fetched (ZIP payload at {logs_url})"
        return "Error downloading logs"
    except GithubException as e:
        logger.warning(f"GitHub API Error (Run {run_id} not found). Injecting Real-World Mock Logs for Demo.")
        # Return a simulated real-world python CI failure log for the Hackathon presentation
        return f"""
============= CI PIPELINE LOGS =============
Running: pytest tests/
============================= test session starts ==============================
collected 0 items / 1 error
==================================== ERRORS ====================================
_______________________ ERROR collecting tests/test_main.py _______________________
ImportError while importing test module 'main.py'.
Traceback:
  File "main.py", line 14
    class PredictRequest(BaseModel)
                                   ^
SyntaxError: expected ':'
=========================== short test summary info ============================
ERROR tests/test_main.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
"""

def get_file_content(repo_full_name: str, file_path: str, branch: str = "main") -> str:
    """
    Downloads the raw source code from GitHub so the LLM can see what to fix.
    """
    g = get_github_client()
    if not g:
        return ""
    try:
        repo = g.get_repo(repo_full_name)
        file_obj = repo.get_contents(file_path, ref=branch)
        return file_obj.decoded_content.decode("utf-8")
    except Exception as e:
        logger.error(f"Error fetching file content for {file_path}: {e}")
        return ""

def create_branch(repo_full_name: str, base_branch: str, new_branch: str):
    """
    Creates a new branch from the base branch via GitHub API.
    """
    g = get_github_client()
    if not g:
        logger.warning(f"No GITHUB_TOKEN. Mock creating branch {new_branch} from {base_branch} in {repo_full_name}")
        return
    repo = g.get_repo(repo_full_name)
    sb = repo.get_branch(base_branch)
    repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=sb.commit.sha)
    logger.info(f"Created branch {new_branch}")

def modify_file(repo_full_name: str, file_path: str, branch: str, content: str, commit_message: str):
    """
    Modifies or creates a file in the remote repository using GitHub Repo contents api.
    """
    g = get_github_client()
    if not g:
        logger.warning(f"No GITHUB_TOKEN. Mock modifying {file_path} in {branch} with message: '{commit_message}'")
        return
    repo = g.get_repo(repo_full_name)
    try:
        file = repo.get_contents(file_path, ref=branch)
        repo.update_file(file.path, commit_message, content, file.sha, branch=branch)
    except GithubException: # if file doesn't exist
        repo.create_file(file_path, commit_message, content, branch=branch)
    logger.info(f"Modified {file_path} in {branch}")

def create_pull_request(repo_full_name: str, title: str, head_branch: str, base_branch: str, body: str, labels: list = None, draft: bool = False) -> str:
    """
    Creates a pull request and returns the HTML URL.
    """
    g = get_github_client()
    if not g:
        logger.warning(f"No GITHUB_TOKEN. Mock PR creation from {head_branch} to {base_branch} with title: '{title}'")
        return f"https://github.com/{repo_full_name}/pull/mock_123"
    repo = g.get_repo(repo_full_name)
    pr = repo.create_pull(title=title, body=body, head=head_branch, base=base_branch, draft=draft)
    if labels:
        pr.add_to_labels(*labels)
    logger.info(f"Created PR: {pr.html_url} with labels {labels}")
    return pr.html_url
