from github import Github
import os
from dotenv import load_dotenv

load_dotenv(override=True)
token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("TARGET_REPO", "Shubhamjkd01/AI_DevOps_X")
g = Github(token)

print(f"Checking {repo_name} for recent PRs...")
try:
    repo = g.get_repo(repo_name)
    prs = repo.get_pulls(state='open', sort='created', direction='desc')
    if prs.totalCount > 0:
        pr = prs[0]
        print(f"FOUND PR: {pr.title}")
        print(f"URL: {pr.html_url}")
    else:
        print("No open PRs found. Maybe it's still generating or the validator blocked it.")
except Exception as e:
    print(f"Error querying GitHub: {e}")
