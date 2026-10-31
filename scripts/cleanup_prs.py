"""
PR Cleanup Script - Closes old test PRs, keeps only the latest 3.
Run this before hackathon submission to clean up the NurseSync repo.
"""
import os
from dotenv import load_dotenv
load_dotenv(override=True)

from github import Github, Auth

TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("TARGET_REPO", "Shubhamjkd01/Nursesycn")
KEEP_LATEST = 3  # Keep only the 3 most recent PRs open

def cleanup_prs():
    if not TOKEN:
        print("ERROR: No GITHUB_TOKEN in .env")
        return
    
    g = Github(auth=Auth.Token(TOKEN))
    repo = g.get_repo(REPO_NAME)
    
    # Get all open PRs
    open_prs = list(repo.get_pulls(state="open", sort="created", direction="desc"))
    print(f"Found {len(open_prs)} open PRs in {REPO_NAME}")
    
    if len(open_prs) <= KEEP_LATEST:
        print(f"Only {len(open_prs)} PRs open, nothing to clean up.")
        return
    
    # Keep the latest N, close the rest
    prs_to_close = open_prs[KEEP_LATEST:]
    print(f"Keeping latest {KEEP_LATEST} PRs, closing {len(prs_to_close)} old ones...\n")
    
    for pr in prs_to_close:
        try:
            pr.edit(state="closed")
            print(f"  ✅ Closed PR #{pr.number}: {pr.title}")
        except Exception as e:
            print(f"  ❌ Failed to close PR #{pr.number}: {e}")
    
    print(f"\nDone! {len(prs_to_close)} old PRs closed. {KEEP_LATEST} latest PRs remain open.")

if __name__ == "__main__":
    cleanup_prs()
