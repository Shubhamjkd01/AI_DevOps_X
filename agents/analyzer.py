import logging
import json
import os
from services.llm import query_llm

logger = logging.getLogger(__name__)
HOT_ZONES_FILE = "c:/AI_DeVops/github_agent_backend/hot_zones.json"

def track_failure_trend(file_path: str) -> bool:
    if not file_path: return False
    try:
        if os.path.exists(HOT_ZONES_FILE):
            with open(HOT_ZONES_FILE, "r") as f:
                trends = json.load(f)
        else:
            trends = {}
            
        trends[file_path] = trends.get(file_path, 0) + 1
        
        with open(HOT_ZONES_FILE, "w") as f:
            json.dump(trends, f)
            
        if trends[file_path] >= 3:
            logger.warning(f"HOT ZONE DETECTED: {file_path} has failed {trends[file_path]} times.")
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to track hot zones: {e}")
        return False

def analyze_logs(logs: str, repo_full_name: str = "Shubhamjkd01/AI_DevOps_X") -> dict:
    """
    Analyzes the CI logs to find the prioritized root cause of the failure.
    Uses the physical repository file tree to correctly identify the target file.
    """
    logger.info("Analyzer Agent: Scanning logs for priority errors...")
    
    # RAG Repo Mapping
    from services.github import get_repo_file_tree
    repo_files = get_repo_file_tree(repo_full_name)
    file_tree_context = "\n".join(repo_files)
    
    prompt = f"""Analyzer Agent: Analyze these CI/CD logs: {logs}

[REPOSITORY FILE BLUEPRINT]
You must select the 'file_path' exclusively from this known physically existing list of files:
{file_tree_context}
[END BLUEPRINT]

Identify the main error and prioritize it.
Return ONLY a valid JSON object with EXACTLY these keys:
"priority": "HIGH", "MEDIUM", or "LOW"
"confidence": (float 0.0 to 1.0)
"file_path": "path/to/the/problematic/file.py"
"error": "Short description of the error"
"why": "Deep technical explanation of why this error occurred"
"failure_category": Must be one of ["SyntaxError", "MissingDependency", "EnvVariable", "TestAssertion", "ArchitecturalRegression"]
"""
    response = query_llm(prompt)
    
    try:
        cleaned = response.replace("```json", "").replace("```", "").strip()
        analysis = json.loads(cleaned)
    except Exception as e:
        logger.error("Failed to parse Analyzer JSON. Fallback active.")
        analysis = {
            "priority": "HIGH",
            "confidence": 0.90,
            "file_path": "main.py",
            "error": "Pipeline execution failed",
            "why": "Fallback triggered due to unparseable logs",
            "failure_category": "SyntaxError"
        }
        
    analysis["needs_refactor"] = track_failure_trend(analysis.get("file_path"))
    logger.info(f"Analyzer Agent Output: [Priority: {analysis['priority']}] [{analysis.get('failure_category', 'Unknown')}] Confidence {analysis['confidence']} - {analysis['error']}")
    return analysis
