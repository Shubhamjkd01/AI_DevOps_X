from github import Github
import os
from dotenv import load_dotenv

load_dotenv(override=True)
g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo("Shubhamjkd01/Nursesycn")

# Get most recent workflow run that failed
runs = repo.get_workflow_runs()
if runs.totalCount > 0:
    for run in runs:
        if run.conclusion == 'failure':
            run_id = run.id
            print(f"Triggering fix for Run ID: {run_id}")
            from agents.orchestrator import handle_workflow_failure
            pr_url = handle_workflow_failure("Shubhamjkd01/Nursesycn", run_id)
            print(f"DONE! PR URL: {pr_url}")
            break
else:
    print("NO WORKFLOWS!")

