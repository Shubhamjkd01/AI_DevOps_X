import logging
import time
from services.github import fetch_workflow_logs
from agents.analyzer import analyze_logs
from agents.fixer import generate_fix
from agents.validator import validate_fix
from agents.pr_agent import create_fix_pr
from learning.episodic_memory import save_patch_memory

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
            
            # Episodic Memory: Save Patch Details (Reward = 1.0 on success)
            save_patch_memory(analysis['error'], fix_data["content"], reward=1.0)
            
            return pr_url
        else:
            logger.warning("Orchestrator: Fix validation failed (Regression caught). Aborting PR.")
            # Penalize failed fixes
            save_patch_memory(analysis.get('error', 'unknown error'), fix_data.get("content", ""), reward=0.0)
            return None
            
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Orchestrator: Agent execution crashed! Fault Tolerance Active. Reason: {error_msg}")
        save_patch_memory(f"SYSTEM_CRASH_OR_TIMEOUT: {error_msg}", "N/A", reward=0.0)
        raise
