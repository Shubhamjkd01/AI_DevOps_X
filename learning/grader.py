import logging
from typing import Dict

logger = logging.getLogger(__name__)

class OpenEnvGrader:
    """
    Evaluates actions against 3 deterministic, real-world tasks.
    Enforces partial progress and penalizes destructive behavior.
    """
    
    def __init__(self):
        self.current_score = 0.0
        self.task_history = []
        
    def grade_task_1_easy(self, action_type: str, file_path: str, patch: str) -> float:
        """Task 1: Syntax Error (Simple colon missing in main.py)"""
        score = 0.0
        if action_type == "analyze": return 0.2
        if action_type == "patch":
            if file_path == "main.py": score += 0.4
            if ":" in patch or "SyntaxError" not in patch: score += 0.4
        return score
        
    def grade_task_2_medium(self, action_type: str, file_path: str, patch: str) -> float:
        """Task 2: Dependency Mismatch (requirements.txt failure)"""
        score = 0.0
        if action_type == "analyze": return 0.2
        if action_type == "patch":
            if file_path == "requirements.txt": score += 0.3
            if "==" in patch or "streamlit" in patch: score += 0.5
        return score
        
    def grade_task_3_hard(self, action_type: str, file_path: str, patch: str) -> float:
        """Task 3: Multi-file Regression (orchestrator.py + fixer.py mismatch)"""
        score = 0.0
        if action_type == "analyze": return 0.3
        if action_type == "patch":
            if file_path in ["orchestrator.py", "agents/fixer.py"]: score += 0.3
            if "import" in patch and "def " in patch: score += 0.4
            # Penalty for infinite loops or destructive deletes
            if patch == "" or "while True:" in patch: score -= 0.5
        return max(0.0, score)

    def evaluate_step(self, task_id: str, action_type: str, file_path: str = "", patch: str = "") -> float:
        """Core OpenEnv Reward Function with Shaping."""
        if task_id == "task_1":
            reward = self.grade_task_1_easy(action_type, file_path, patch)
        elif task_id == "task_2":
            reward = self.grade_task_2_medium(action_type, file_path, patch)
        elif task_id == "task_3":
            reward = self.grade_task_3_hard(action_type, file_path, patch)
        else:
            reward = 0.0
            
        self.current_score = reward
        logger.info(f"OpenEnv Grader: Scored task [{task_id}] -> {reward:.2f}")
        return reward

# Global Singleton Grader for the API
global_grader = OpenEnvGrader()

def evaluate_patch_reward(validation_success: bool, regression_passed: bool) -> float:
    """Legacy wrapper for Orchestrator logic."""
    if validation_success and regression_passed:
        return 1.0
    elif validation_success and not regression_passed:
        return 0.5
    return 0.0
