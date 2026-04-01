import logging
import time
import os
from services.github import fetch_workflow_logs
from agents.analyzer import analyze_logs
from agents.fixer import generate_fix
from agents.validator import validate_fix
from agents.pr_agent import create_fix_pr
from learning.episodic_memory import save_patch_memory
from learning.curriculum import CurriculumController

logger = logging.getLogger(__name__)

def handle_workflow_failure(repo_full_name: str, run_id: int, mock_fail_type: str = None, llm_priority: str = None):
    """
    Orchestrates the enterprise agents to handle a workflow failure.
    """
    start_time = time.time()
    logger.info(f"Orchestrator: Handling workflow failure for {repo_full_name} run {run_id}")
    try:
        # 1. Fetch Logs
        logs = fetch_workflow_logs(repo_full_name, run_id, mock_fail_type)
        
        # 2. Analyze Logs (Structured & Prioritized)
        analysis = analyze_logs(logs, repo_full_name)
        
        # 3. Curriculum Check
        curriculum = CurriculumController()
        category = analysis.get('failure_category', 'syntax')
        curriculum_level = curriculum.get_difficulty(category)
        logger.info(f"Orchestrator: Adapting to Curriculum Level: {curriculum_level} for category {category}")
        
        # 4. Generate Fix (Patch-based & Context-aware)
        fix_data = generate_fix(analysis, repo_full_name, llm_priority, curriculum_level)
        
        # 5. Validate Fix (Regression Check included)
        is_valid = validate_fix(fix_data)
        
        # 6. 3-Tier LLM Judge Evaluation
        from agents.judge import evaluate_patch
        mastery_score = curriculum.get_raw_score(category)
        judge_score, judge_explanation = evaluate_patch(analysis, fix_data, mastery_score)
        logger.info(f"Orchestrator: 3-Tier LLM Judge Score: {judge_score} | Reason: {judge_explanation}")
        
        # Modify the explanation for PR review
        fix_data['explanation'] = f"{fix_data.get('explanation', '')}\n\n[Judge Evaluation: {judge_explanation}]"
        
        if is_valid and judge_score >= 0.5:
            # 7. Create PR / Dry Run Mode
            if os.getenv("DRY_RUN_MODE", "false").lower() == "true":
                logger.info("DRY_RUN_MODE enabled: Skipping PR creation. Simulating success.")
                pr_url = "http://localhost:8080/dashboard#dry-run"
            else:
                pr_url = create_fix_pr(repo_full_name, fix_data, run_id)
            
            # Observability: Time to fix
            time_to_fix = round(time.time() - start_time, 2)
            logger.info(f"Orchestrator: Process complete. PR created: {pr_url} (Time to Fix: {time_to_fix}s)")
            
            # Episodic Memory: Save Patch Details (Reward = judge_score on success)
            save_patch_memory(analysis['error'], fix_data["content"], reward=judge_score, failure_category=category, pr_url=pr_url)
            curriculum.update_mastery(category, success=True)
            
            return pr_url
        else:
            logger.warning("Orchestrator: Fix validation failed (Regression caught or Judge rejected). Aborting PR.")
            # Penalize failed fixes
            save_patch_memory(analysis.get('error', 'unknown error'), fix_data.get("content", ""), reward=0.0, failure_category=category)
            curriculum.update_mastery(category, success=False)
            
            # Record the failure for self-improvement
            from learning.env_monitor import log_failure
            log_failure(
                error_reason=analysis.get('error', 'unknown error'),
                command_tried="orchestrator_fix_attempt",
                error_response=f"Judge Score: {judge_score}, Sandbox Valid: {is_valid}"
            )
            return None
            
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Orchestrator: Agent execution crashed! Fault Tolerance Active. Reason: {error_msg}")
        save_patch_memory(f"SYSTEM_CRASH_OR_TIMEOUT: {error_msg}", "N/A", reward=0.0, failure_category="Unknown")
        raise
