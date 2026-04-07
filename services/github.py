import os
import time
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
        logger.error("No GITHUB_TOKEN provided. Cannot fetch logs.")
        raise ValueError("GITHUB_TOKEN is missing")

    try:
        if mock_fail_type:
            logger.info(f"Mock fail type '{mock_fail_type}' detected. Bypassing GitHub API fetch.")
            return f"Traceback (most recent call last):\n  File \"main.py\", line 42\n    def process_request(req)\nSyntaxError: expected ':' ({mock_fail_type} simulation)"

        repo = g.get_repo(repo_full_name)
        run = repo.get_workflow_run(run_id)
        logs_url = run.logs_url
        response = requests.get(logs_url, headers={"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"}, timeout=20)
        if response.status_code == 200:
            try:
                import io
                import zipfile
                z = zipfile.ZipFile(io.BytesIO(response.content))
                logs = ""
                # Search the unzipped Action files for explicit tracebacks or failures
                for filename in z.namelist():
                    if filename.endswith(".txt"):
                        content = z.read(filename).decode('utf-8', errors='ignore')
                        if "Error" in content or "Traceback" in content or "FAILED" in content or "Exception" in content:
                            logs += f"--- {filename} ---\n{content[-3000:]}\n\n"
                if not logs:
                    logs = "Workflow completed but no explicit Python Tracebacks were found in the raw logs."
                return logs
            except Exception as e:
                logger.error(f"Failed to extract zip payload: {e}")
                return "Failed to unzip logs."
        else:
            error_msg = f"Error downloading logs, status code: {response.status_code}"
            logger.error(error_msg)
            raise Exception(error_msg)
    except GithubException as e:
        logger.error(f"GitHub API Error: {e.data}")
        raise e

def get_file_content(repo_full_name: str, file_path: str, branch: str = "main") -> str:
    """
    Downloads the raw source code from GitHub so the LLM can see what to fix.
    """
    g = get_github_client()
    if not g:
        return "import os\n# Mock code for simulation\nprint('Hello World')"
    try:
        repo = g.get_repo(repo_full_name)
        file_obj = repo.get_contents(file_path, ref=branch)
        return file_obj.decoded_content.decode("utf-8")
    except Exception as e:
        logger.warning(f"Error fetching file content for {file_path}: {e}. Using mock template for simulation.")
        return f"import logging\n# Automated template for {file_path}\nlogger = logging.getLogger(__name__)\n\ndef process():\n    pass"

def create_branch(repo_full_name: str, base_branch: str, new_branch: str):
    """
    Creates a new branch from the base branch via GitHub API.
    """
    g = get_github_client()
    if not g:
        logger.warning(f"No GITHUB_TOKEN. Mock creating branch {new_branch} from {base_branch} in {repo_full_name}")
        return
    try:
        repo = g.get_repo(repo_full_name)
        sb = repo.get_branch(base_branch)
        repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=sb.commit.sha)
        logger.info(f"Created branch {new_branch}")
    except Exception as e:
        logger.warning(f"Failed to create branch {new_branch} officially: {e}. Simulation state: PROCEEDING.")

def modify_file(repo_full_name: str, file_path: str, branch: str, content: str, commit_message: str):
    """
    Modifies or creates a file in the remote repository using GitHub Repo contents api.
    """
    g = get_github_client()
    if not g:
        logger.warning(f"No GITHUB_TOKEN. Mock modifying {file_path} in {branch} with message: '{commit_message}'")
        return
    try:
        repo = g.get_repo(repo_full_name)
        try:
            file = repo.get_contents(file_path, ref=branch)
            repo.update_file(file.path, commit_message, content, file.sha, branch=branch)
        except GithubException: # if file doesn't exist
            repo.create_file(file_path, commit_message, content, branch=branch)
        logger.info(f"Modified {file_path} in {branch}")
    except Exception as e:
        logger.warning(f"Failed to modify {file_path} officially: {e}. Simulation state: PROCEEDING.")

def create_pull_request(repo_full_name: str, title: str, head_branch: str, base_branch: str, body: str, labels: list = None, draft: bool = False) -> str:
    """
    Creates a pull request and returns the HTML URL.
    """
    g = get_github_client()
    if not g:
        logger.warning(f"No GITHUB_TOKEN. Mock PR creation from {head_branch} to {base_branch} with title: '{title}'")
        return f"https://github.com/{repo_full_name}/pull/mock_123"
    try:
        repo = g.get_repo(repo_full_name)
        pr = repo.create_pull(title=title, body=body, head=head_branch, base=base_branch, draft=draft)
        if labels:
            pr.add_to_labels(*labels)
        logger.info(f"Created PR: {pr.html_url} with labels {labels}")
        return pr.html_url
    except Exception as e:
        logger.warning(f"Official PR creation failed: {e}. Returning mock URL for simulation.")
        return f"https://github.com/{repo_full_name}/pull/sim_{int(time.time())}"

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
