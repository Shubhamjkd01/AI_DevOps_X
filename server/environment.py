import logging
from typing import Optional, Dict, Any, Tuple
from models import DevOpsObservation, DevOpsAction

# We reuse our RL grader to map scores
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from learning.grader import global_grader
from agents.pr_agent import create_fix_pr
import os

logger = logging.getLogger(__name__)

class EnvironmentSimulator:
    def __init__(self):
        self.current_task_id = "task_1"
        self.step_count = 0
        self.max_steps = 10
        self.is_done = False

    async def reset(self) -> DevOpsObservation:
        """
        Resets the CI environment to the failed state, presenting the initial error trace.
        """
        self.step_count = 0
        self.is_done = False
        
        # We start with task 1
        self.current_task_id = "task_1"
        
        initial_logs = """============= CI PIPELINE LOGS =============
Running: pytest tests/
==================================== ERRORS ====================================
ImportError while importing test module 'main.py'.
Traceback:
  File "main.py", line 14
    class PredictRequest(BaseModel)
                                   ^
SyntaxError: expected ':'
"""
        
        return DevOpsObservation(
            system_state="Awaiting Code Fix",
            ci_logs=initial_logs,
            target_files=["main.py"]
        )

    async def step(self, action: DevOpsAction) -> Tuple[DevOpsObservation, float, bool, Optional[str]]:
        """
        Advances the environment based on the AI's patch/action.
        """
        self.step_count += 1
        
        # We dynamically change the task based on progression for the 3-task minimum constraint
        if self.step_count == 2:
            self.current_task_id = "task_2"
        elif self.step_count >= 3:
            self.current_task_id = "task_3"
            
        reward = global_grader.evaluate_step(
            task_id=self.current_task_id,
            action_type=action.action_type,
            file_path=action.file_path or "",
            patch=action.patch_content or ""
        )
        
        # STRICT HACKATHON ENFORCEMENT: Clamp reward completely to [0.0, 1.0]
        # Any negative reward (-1.0) will result in automatic disqualification!
        reward = float(max(0.0, min(1.0, reward)))
        
        # Build feedback based on reward
        if reward == 1.0:
            state_msg = "Task Solved! PR created successfully."
            
            # TRIGGER REAL GITHUB PR IF IN PRODUCTION MODE
            # Only create PR from /step endpoint, NOT from webhook flow (which has its own PR agent)
            if os.getenv("AGENT_MODE") == "PRODUCTION" and action.patch_content and len(action.patch_content.strip()) > 10:
                try:
                    repo = os.getenv("TARGET_REPO", "Shubhamjkd01/Nursesycn")
                    fix_data = {
                        "explanation": f"Automated OpenEnv fix for {self.current_task_id}",
                        "content": action.patch_content,
                        "file_path": action.file_path or "main.py",
                        "confidence": reward,
                        "priority": "HIGH",
                        "conf_reason": "OpenEnv grader score 1.0",
                        "patch_explanation": f"Fix applied via OpenEnv step endpoint for {self.current_task_id}",
                        "needs_refactor": False
                    }
                    create_fix_pr(repo, fix_data, self.step_count)
                    state_msg += " (Real GitHub PR Pushed!)"
                except Exception as e:
                    logger.error(f"Failed to create real PR: {e}")
                    state_msg += " (PR creation failed, fix still validated)"
        else:
            state_msg = "Failed simulation sandbox format or destructive code found."

        self.is_done = (reward >= 1.0) or (self.step_count >= self.max_steps)
        error_msg = None if reward > 0.0 else f"Sandbox reject: {action.action_type} executed improperly."
        
        obs = DevOpsObservation(
            system_state=state_msg,
            ci_logs=f"Simulated execution patch applied.",
            target_files=[action.file_path or "root"]
        )
        
        return obs, reward, self.is_done, error_msg

    async def state(self) -> DevOpsObservation:
        return DevOpsObservation(
            system_state=f"Running task {self.current_task_id}",
            ci_logs="Idle...",
            target_files=[]
        )
