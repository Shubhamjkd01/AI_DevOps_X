import logging
import json
import os

logger = logging.getLogger(__name__)

SCORE_FILE = "c:/AI_DeVops/github_agent_backend/rl_scores.json"
KNOWLEDGE_BASE_FILE = "c:/AI_DeVops/github_agent_backend/knowledge_base.json"

def get_knowledge_base():
    if not os.path.exists(KNOWLEDGE_BASE_FILE):
        return []
    try:
        with open(KNOWLEDGE_BASE_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_fix_knowledge(error: str, fix: str, accepted: bool):
    """
    Real RL Memory: Saves the specific error mapping so the LLM learns continuously.
    """
    kb = get_knowledge_base()
    kb.append({
        "error": error,
        "fix": fix,
        "accepted": accepted
    })
    with open(KNOWLEDGE_BASE_FILE, "w") as f:
        json.dump(kb, f, indent=4)
        
def get_successful_fixes():
    kb = get_knowledge_base()
    return [entry for entry in kb if entry.get("accepted", False)]

def get_current_scores():
    if not os.path.exists(SCORE_FILE):
        return {"total_score": 0.0, "success_count": 0, "failure_count": 0, "total_time": 0.0}
    with open(SCORE_FILE, "r") as f:
        data = json.load(f)
        if "total_time" not in data:
            data["total_time"] = 0.0
        return data

def save_scores(scores):
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f)

def update_reward(outcome: str, delta: float, time_taken: float = 0.0):
    """
    Updates the agent's reward score and tracked latency.
    """
    scores = get_current_scores()
    scores["total_score"] += delta
    scores["total_time"] += time_taken
    
    if delta > 0:
        scores["success_count"] += 1
    else:
        scores["failure_count"] += 1
        
    save_scores(scores)
    logger.info(f"RL Loop: Reward updated by {delta}. Total score: {scores['total_score']}")
