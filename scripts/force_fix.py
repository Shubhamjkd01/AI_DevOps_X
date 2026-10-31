from github import Github
import os
from dotenv import load_dotenv

load_dotenv(override=True)
token = os.getenv("GITHUB_TOKEN")
g = Github(token)
repo = g.get_repo("Shubhamjkd01/Nursesycn")

# Get most recent workflow run that failed TODAY
runs = repo.get_workflow_runs()
target_run = None
for run in runs:
    if run.conclusion == 'failure':
        target_run = run
        break

if target_run:
    print(f"Found target failed run_id: {target_run.id}")
    print(f"Triggering Orchestrator...")
    from agents.orchestrator import handle_workflow_failure
    try:
        pr_url = handle_workflow_failure("Shubhamjkd01/Nursesycn", target_run.id)
        if pr_url:
            print(f"SUCCESS! PR Created: {pr_url}")
        else:
            print("FAILED: Orchestrator didn't return a PR URL (Check logs context above).")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"CRITICAL ERROR: {e}")
else:
    print("No failed workflows found in Nursesycn!")
