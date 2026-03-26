import logging
import time
from services.github import fetch_workflow_logs
from agents.analyzer import analyze_logs
from agents.fixer import generate_fix
from agents.validator import validate_fix
from agents.pr_agent import create_fix_pr
from learning.episodic_memory import save_patch_memory
from learning.grader import evaluate_patch_reward

logger = logging.getLogger(__name__)

def handle_workflow_failure(repo_full_name: str, run_id: int):
    """
    Orchestrates the enterprise agents to handle a workflow failure.
    """
    start_time = time.time()
    logger.info(f"Orchestrator: Handling workflow failure for {repo_full_name} run {run_id}")
    try:
        # 1. Fetch Logs
        logs = fetch_workflow_logs(repo_full_name, run_id)
        
        # 2. Analyze Logs (Structured & Prioritized)
        analysis = analyze_logs(logs)
        
        # 3. Generate Fix (Patch-based & Context-aware)
        fix_data = generate_fix(analysis, repo_full_name)
        
        # 4. Validate Fix (Regression Check included)
        is_valid = validate_fix(fix_data)
        
        if is_valid:
            # 5. Create PR
            pr_url = create_fix_pr(repo_full_name, fix_data, run_id)
            
            # Observability: Time to fix
            time_to_fix = round(time.time() - start_time, 2)
            logger.info(f"Orchestrator: Process complete. PR created: {pr_url} (Time to Fix: {time_to_fix}s)")
            
            # Episodic Memory: Save Patch Details
            save_patch_memory(analysis['error'], fix_data["content"], True)
            
            return pr_url
        else:
            logger.warning("Orchestrator: Fix validation failed (Regression caught). Aborting PR.")
            return None
            
    except Exception as e:
        logger.error(f"Orchestrator: Error during processing: {str(e)}")
        raise
