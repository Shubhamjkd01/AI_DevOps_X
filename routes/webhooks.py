import os
import hmac
import hashlib
import json
from fastapi import APIRouter, Request, HTTPException
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/webhook/github")
@router.post("/webhook")
async def github_webhook(request: Request):
    """
    Endpoint to receive GitHub Webhooks, specifically workflow failures.
    Secured via HMAC SHA-256 signature verification when GITHUB_WEBHOOK_SECRET is set.
    """
    event = request.headers.get("X-GitHub-Event")
    if not event:
        raise HTTPException(status_code=400, detail="Missing X-GitHub-Event header")

    body_bytes = await request.body()
    secret = os.environ.get("GITHUB_WEBHOOK_SECRET")
    if secret:
        signature = request.headers.get("X-Hub-Signature-256")
        if not signature:
            logger.warning("Unauthorized webhook request: Missing X-Hub-Signature-256 header")
            raise HTTPException(status_code=401, detail="Missing X-Hub-Signature-256 header")
        
        expected_sig = "sha256=" + hmac.new(secret.encode(), body_bytes, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_sig, signature):
            logger.warning("Unauthorized webhook request: Invalid HMAC signature")
            raise HTTPException(status_code=401, detail="Invalid HMAC signature")

    try:
        payload = json.loads(body_bytes.decode('utf-8'))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    if event == "workflow_run":
        action = payload.get("action")
        workflow_run = payload.get("workflow_run", {})
        status = workflow_run.get("status")
        conclusion = workflow_run.get("conclusion")
        
        # We only care when a workflow has completed and failed
        if action == "completed" and conclusion == "failure":
            repo_name = payload.get("repository", {}).get("full_name")
            run_id = workflow_run.get("id")
            head_commit = workflow_run.get("head_commit", {})
            
            author_email = head_commit.get("author", {}).get("email", "")
            author_name = head_commit.get("author", {}).get("name", "")
            
            if "agent" in author_email.lower() or "ai" in author_name.lower():
                logger.warning(f"ROLLBACK AGENT TRIGGERED! Run {run_id} failed immediately after AI patch.")
                from agents.rollback_agent import trigger_rollback
                commit_sha = head_commit.get("id")
                
                # Dynamic hook for multi-repo rollback isolation
                import threading
                threading.Thread(target=trigger_rollback, args=(repo_name, commit_sha)).start()
                return {"status": "rollback_triggered", "repo": repo_name, "commit": commit_sha}
            
            logger.info(f"Detected failed workflow {run_id} in {repo_name}. Triggering orchestrator.")
            from agents.orchestrator import handle_workflow_failure
            import threading
            
            mock_fail_type = payload.get("mock_fail_type")
            llm_priority = payload.get("llm_priority")
            
            # Run orchestrator in the background to avoid blocking the webhook response
            thread = threading.Thread(target=handle_workflow_failure, args=(repo_name, run_id, mock_fail_type, llm_priority))
            thread.start()
            
            return {"status": "triggered", "run_id": run_id, "repo": repo_name}
            
    if event == "pull_request":
        action = payload.get("action")
        pr = payload.get("pull_request", {})
        merged = pr.get("merged", False)
        pr_url = pr.get("html_url")
        
        if action == "closed":
            from learning.grader import update_reward
            if merged:
                logger.info(f"PR MERGED! Reinforcing patch memory for {pr_url}")
                update_reward(pr_url, "merged")
            else:
                logger.warning(f"PR CLOSED/REJECTED! Penalizing patch memory for {pr_url}")
                update_reward(pr_url, "closed")
            return {"status": "feedback_logged", "merged": merged, "pr_url": pr_url}
        elif action == "synchronize":
            from learning.grader import update_reward
            logger.info(f"PR MODIFIED! Applying partial reward for {pr_url}")
            update_reward(pr_url, "modified")
            return {"status": "feedback_logged", "modified": True, "pr_url": pr_url}
    
    return {"status": "ignored", "reason": f"Event {event} not handled or not actionable."}
