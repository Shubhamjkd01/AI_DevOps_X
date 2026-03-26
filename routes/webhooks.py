from fastapi import APIRouter, Request, HTTPException
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/webhook/github")
async def github_webhook(request: Request):
    """
    Endpoint to receive GitHub Webhooks, specifically workflow failures.
    """
    event = request.headers.get("X-GitHub-Event")
    if not event:
        raise HTTPException(status_code=400, detail="Missing X-GitHub-Event header")

    payload = await request.json()
    
    if event == "workflow_run":
        action = payload.get("action")
        workflow_run = payload.get("workflow_run", {})
        status = workflow_run.get("status")
        conclusion = workflow_run.get("conclusion")
        
        # We only care when a workflow has completed and failed
        if action == "completed" and conclusion == "failure":
            repo_name = payload.get("repository", {}).get("full_name")
            run_id = workflow_run.get("id")
            
            logger.info(f"Detected failed workflow {run_id} in {repo_name}. Triggering orchestrator.")
            from agents.orchestrator import handle_workflow_failure
            import threading
            
            # Run orchestrator in the background to avoid blocking the webhook response
            thread = threading.Thread(target=handle_workflow_failure, args=(repo_name, run_id))
            thread.start()
            
            return {"status": "triggered", "run_id": run_id, "repo": repo_name}
    
    return {"status": "ignored", "reason": f"Event {event} not handled or not a failure."}
