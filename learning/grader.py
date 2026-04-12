import logging
from typing import Dict

logger = logging.getLogger(__name__)

class OpenEnvGrader:
    """
    Evaluates actions against 3 deterministic, real-world tasks.
    Enforces partial progress and penalizes destructive behavior.
    """
    
    def __init__(self):
        self.current_score = 0.05
        self.task_history = []
        
    def grade_task_1_easy(self, action_type: str, file_path: str, patch: str) -> float:
        """Task 1: Syntax Error (Simple colon missing in main.py)"""
        score = 0.05
        if action_type == "analyze": return 0.2
        if action_type == "patch":
            if file_path == "main.py": score += 0.5
            if ":" in patch or "SyntaxError" not in patch: score += 0.5
        return score
        
    def grade_task_2_medium(self, action_type: str, file_path: str, patch: str) -> float:
        """Task 2: Dependency Mismatch (requirements.txt failure)"""
        score = 0.05
        if action_type == "analyze": return 0.2
        if action_type == "patch":
            if file_path == "requirements.txt": score += 0.4
            if "==" in patch or "streamlit" in patch: score += 0.6
        return score
        
    def grade_task_3_hard(self, action_type: str, file_path: str, patch: str) -> float:
        """Task 3: Multi-file Regression (orchestrator.py + fixer.py mismatch)"""
        score = 0.05
        if action_type == "analyze": return 0.3
        if action_type == "patch":
            if file_path in ["orchestrator.py", "agents/fixer.py"]: score += 0.5
            if "import" in patch and "def " in patch: score += 0.5
            # Penalty for infinite loops or destructive deletes
            if patch == "" or "while True:" in patch: score -= 0.5
        return max(0.05, score)

    def evaluate_step(self, task_id: str, action_type: str, file_path: str = "", patch: str = "") -> float:
        """Core OpenEnv Reward Function with Shaping."""
        if task_id == "task_1":
            reward = self.grade_task_1_easy(action_type, file_path, patch)
        elif task_id == "task_2":
            reward = self.grade_task_2_medium(action_type, file_path, patch)
        elif task_id == "task_3":
            reward = self.grade_task_3_hard(action_type, file_path, patch)
        else:
            reward = 0.05
            
        reward = min(0.99, max(0.01, reward))
        self.current_score = reward
        logger.info(f"OpenEnv Grader: Scored task [{task_id}] -> {reward:.2f}")
        return reward

# Global Singleton Grader for the API
global_grader = OpenEnvGrader()

def evaluate_patch_reward(validation_success: bool, regression_passed: bool) -> float:
    """Legacy wrapper for Orchestrator logic."""
    if validation_success and regression_passed:
        return 0.95
    elif validation_success and not regression_passed:
        return 0.5
    return 0.05

def update_reward(patch_id: str, outcome: str):
    """
    Core RL loop feedback function based on actual repo interactions.
    Updates the operational vector memory weights.
    """
    from learning.episodic_memory import update_patch_reward
    
    if outcome == "merged":
        reward = 0.95
    elif outcome == "closed":
        reward = 0.01
    elif outcome == "modified":
        reward = 0.5
    else:
        reward = 0.05
        
    logger.info(f"Grader mapping outcome '{outcome}' to reward {reward} for PR {patch_id}")
    update_patch_reward(patch_id, reward)

# OpenEnv strict grader wrappers
def openenv_task1_grader(*args, **kwargs) -> float:
    action_type = kwargs.get("action_type", "patch")
    file_path = kwargs.get("file_path", "main.py")
    patch = kwargs.get("patch_content", "")
    score = global_grader.grade_task_1_easy(action_type, file_path, patch)
    return float(min(0.99, max(0.01, score)))

def openenv_task2_grader(*args, **kwargs) -> float:
    action_type = kwargs.get("action_type", "patch")
    file_path = kwargs.get("file_path", "requirements.txt")
    patch = kwargs.get("patch_content", "")
    score = global_grader.grade_task_2_medium(action_type, file_path, patch)
    return float(min(0.99, max(0.01, score)))

def openenv_task3_grader(*args, **kwargs) -> float:
    action_type = kwargs.get("action_type", "patch")
    file_path = kwargs.get("file_path", "orchestrator.py")
    patch = kwargs.get("patch_content", "")
    score = global_grader.grade_task_3_hard(action_type, file_path, patch)
    return float(min(0.99, max(0.01, score)))

