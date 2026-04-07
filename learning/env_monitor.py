import os
import json
import logging
import datetime
from services.llm import query_llm
from services.github import create_issue

logger = logging.getLogger(__name__)

FAIL_FILE = "c:/AI_DeVops/github_agent_backend/failure_patterns.json"
META_FILE = "c:/AI_DeVops/github_agent_backend/env_metadata.json"

def log_failure(error_reason: str, command_tried: str, error_response: str):
    logger.info("Env Monitor: Logging failure to failure_patterns.json")
    
    entries = []
    if os.path.exists(FAIL_FILE):
        try:
            with open(FAIL_FILE, "r") as f:
                entries = json.load(f)
        except Exception:
            pass
            
    # Keep it clean
    entries.append({
        "error_reason": error_reason,
        "command_tried": command_tried,
        "error_response": error_response,
        "timestamp": datetime.datetime.now().isoformat()
    })
    
    with open(FAIL_FILE, "w") as f:
        json.dump(entries, f, indent=4)
        
    # Check if 5 identical failures happen
    _check_patterns(error_reason)

def _check_patterns(error_reason: str):
    if not os.path.exists(FAIL_FILE): return
    with open(FAIL_FILE, "r") as f:
        entries = json.load(f)
        
    same_type = [e for e in entries if e.get("error_reason") == error_reason]
    if len(same_type) >= 5:
        logger.warning(f"Env Monitor: Detected 5 recurring failures for {error_reason}. Triggering self-diagnosis.")
        _trigger_diagnosis(same_type)
        
        # Clear pattern after triggering so it doesn't spam
        entries = [e for e in entries if e.get("error_reason") != error_reason]
        with open(FAIL_FILE, "w") as f:
            json.dump(entries, f, indent=4)

def _trigger_diagnosis(failures: list):
    prompt = f"""You are the Self-Improvement System Monitor.
We have failed to fix the same issue 5 times in a row.
Here are the traces:
{json.dumps(failures[-3:], indent=2)}

Determine if this is caused by a BUG IN OUR PIPELINE (e.g. parser timeout, missing permissions, LLM truncation) or if it is just a genuinely hard code problem in the repo.
Return a valid JSON object:
{{
  "is_pipeline_bug": <true/false>,
  "description": "<detailed bug report to open an issue>"
}}
"""
    response = query_llm(prompt).replace("```json", "").replace("```", "").strip()
    try:
        diagnosis = json.loads(response)
        if diagnosis.get("is_pipeline_bug") is True:
            _report_bug(diagnosis.get("description", "Unknown pipeline glitch detected by AI."))
        else:
            logger.info("Env Monitor: LLM concluded this is just a genuinely hard problem, not an environment bug.")
    except Exception as e:
        logger.error(f"Env Monitor: Failed to parse self-diagnosis JSON. {e}")

def _report_bug(description: str):
    today = datetime.date.today().isoformat()
    meta = {"last_issue_date": "", "issues_today": 0, "total_bugs_found": 0, "fixed": 0}
    
    if os.path.exists(META_FILE):
        try:
            with open(META_FILE, "r") as f:
                meta = json.load(f)
        except Exception:
            pass
            
    if meta.get("last_issue_date") != today:
        meta["last_issue_date"] = today
        meta["issues_today"] = 0
        
    if meta["issues_today"] >= 3:
        logger.warning(f"Env Monitor: Daily rate limit (3) exceeded for GitHub Issue creation. Skipping bug report: {description}")
        return
        
    meta["issues_today"] += 1
    meta["total_bugs_found"] += 1
    
    with open(META_FILE, "w") as f:
        json.dump(meta, f, indent=4)
        
    logger.info(f"Env Monitor: Creating GitHub Issue for Env Bug! Rate limit used: {meta['issues_today']}/3")
    create_issue(repo_full_name="Shubhamjkd01/Nursesycn", title=f"ENV BUG: Pipeline Issue Detected", body=description, labels=["self-improvement"])

def get_health_stats() -> dict:
    meta = {"last_issue_date": "", "issues_today": 0, "total_bugs_found": 0, "fixed": 0}
    if os.path.exists(META_FILE):
        try:
            with open(META_FILE, "r") as f:
                meta = json.load(f)
        except Exception:
            pass
    total = meta.get("total_bugs_found", 0)
    fixed = meta.get("fixed", 0)
    reliability = max(10, 100 - (total * 5) + (fixed * 5))
    return {
        "status": "watching",
        "total_bugs_found": total,
        "fixed": fixed,
        "pipeline_reliability_score": f"{reliability}%"
    }
