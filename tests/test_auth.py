import os
from dotenv import load_dotenv
load_dotenv()
from github import Github, Auth
from github.GithubException import GithubException

token = os.getenv("GITHUB_TOKEN")
print(f"Token present: {bool(token)}")
try:
    g = Github(auth=Auth.Token(token))
    repo = g.get_repo("Shubhamjkd01/AI_DevOps_X")
    print("Successfully connected to repo:", repo.full_name)
    user = g.get_user().login
    print("Authenticated as:", user)
    # Check if we can get branches
    branch = repo.get_branch(repo.default_branch)
    print("Default branch:", branch.name)
except GithubException as e:
    print("GitHub Exception:", e)
