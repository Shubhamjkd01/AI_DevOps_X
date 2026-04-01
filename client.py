import os
import requests
from pydantic import BaseModel
from models import DevOpsAction, DevOpsObservation

class StepResult(BaseModel):
    observation: DevOpsObservation
    reward: float = 0.0
    done: bool = False
    info: dict = {}

class GitHubAgentEnv:
    """
    OpenEnv Client Wrapper.
    Routes to the container exposed by app.py automatically during evaluation.
    """
    def __init__(self, base_url="http://localhost:7860"):
        self.base_url = base_url

    async def reset(self) -> StepResult:
        resp = requests.post(f"{self.base_url}/reset")
        resp.raise_for_status()
        obs = DevOpsObservation(**resp.json())
        return StepResult(observation=obs, reward=0.0, done=False, info={})

    async def step(self, action: DevOpsAction) -> StepResult:
        resp = requests.post(f"{self.base_url}/step", json=action.dict())
        resp.raise_for_status()
        return StepResult(**resp.json())
        
    async def state(self) -> DevOpsObservation:
        resp = requests.get(f"{self.base_url}/state")
        resp.raise_for_status()
        return DevOpsObservation(**resp.json())
        
    async def close(self):
        pass
        
    @classmethod
    async def from_docker_image(cls, image_name: str = None):
        """Mock constructor as defined in OpenEnv standards to bind to internal containers."""
        # Assume sandbox environment is hooked to localhost:7860 inside the hackathon evaluator
        return cls("http://localhost:7860")
