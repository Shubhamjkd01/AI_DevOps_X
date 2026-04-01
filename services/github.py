import os
import logging
import requests
from github import Github, Auth
from github.GithubException import GithubException

logger = logging.getLogger(__name__)

def get_github_client():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return None
    auth = Auth.Token(token)
    return Github(auth=auth)

def get_repo_file_tree(repo_full_name: str, branch: str = "main") -> list:
    """
    RAG Repo Scanner: Grabs the full repository mapping natively from GitHub instead of guessing.
    """
    g = get_github_client()
    if not g:
        # Mock tree for simulator
        return ["main.py", "tests/test_main.py", "requirements.txt", "agents/analyzer.py", "services/github.py"]
        
    try:
        repo = g.get_repo(repo_full_name)
        tree = repo.get_git_tree(branch, recursive=True)
        # Filter python files, configs, and ignore compiled binaries
        files = [t.path for t in tree.tree if t.type == "blob" and (t.path.endswith('.py') or t.path.endswith('.txt') or t.path.endswith('.json'))]
        return files
    except Exception as e:
        logger.error(f"Failed to fetch repo file tree for {repo_full_name}: {e}")
        return ["main.py"]

def fetch_workflow_logs(repo_full_name: str, run_id: int, mock_fail_type: str = None) -> str:
    """
    Fetches the logs for a specific workflow run.
    """
    g = get_github_client()
    if not g:
        logger.warning(f"No GITHUB_TOKEN. Returning mock logs for {mock_fail_type or 'syntax'}.")
        
        if mock_fail_type == "dependency":
            return """
============= CI PIPELINE LOGS =============
Running pip install -r requirements.txt
ERROR: Could not find a version that satisfies the requirement missing_fake_lib==9.9.9
ERROR: No matching distribution found for missing_fake_lib==9.9.9
            """
        elif mock_fail_type == "test":
            return """
============= CI PIPELINE LOGS =============
==================================== ERRORS ====================================
assert sum([1, 2, 3]) == 5
AssertionError: expected 5, got 6
            """
        else:
            return """
============= CI PIPELINE LOGS =============
Running: pytest tests/
==================================== ERRORS ====================================
ImportError while importing test module 'main.py'.
Traceback:
  File "main.py", line 14
    class PredictRequest(BaseModel)
                                   ^
SyntaxError: expected ':'
=========================== short test summary info ============================
ERROR tests/test_main.py
"""

    try:
        repo = g.get_repo(repo_full_name)
        run = repo.get_workflow_run(run_id)
        logs_url = run.logs_url
        response = requests.get(logs_url, headers={"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"})
        if response.status_code == 200:
            return f"Logs successfully fetched (ZIP payload at {logs_url})"
        return "Error downloading logs"
    except GithubException as e:
        logger.warning(f"GitHub API Error (Run {run_id} not found). Injecting Real-World Mock Logs for Demo.")
        return """
============= CI PIPELINE LOGS =============
Running: pytest tests/
==================================== ERRORS ====================================
ImportError while importing test module 'main.py'.
Traceback:
  File "main.py", line 14
    class PredictRequest(BaseModel)
                                   ^
SyntaxError: expected ':'
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

def create_issue(repo_full_name: str, title: str, body: str, labels: list = None) -> str:
    """
    Creates an issue on the repository. Used for self-improvement tracking.
    """
    g = get_github_client()
    if not g:
        logger.warning(f"No GITHUB_TOKEN. Mock creating issue '{title}' in {repo_full_name}")
        return "https://github.com/mock/issue/123"
    
    repo = g.get_repo(repo_full_name)
    issue = repo.create_issue(title=title, body=body, labels=labels or [])
    logger.info(f"Created Issue: {issue.html_url}")
    return issue.html_url
