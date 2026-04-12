import logging
import sys
import os
import importlib
from dotenv import load_dotenv
load_dotenv(override=True)

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import DevOpsAction, DevOpsObservation
from server.environment import EnvironmentSimulator
import uvicorn

app = FastAPI(
    title="AI_DevOps_Agent",
    description="Autonomous CI/CD Fixer Agent that repairs regressions and submits Pull Requests.",
    version="1.0.0"
)
simulator = EnvironmentSimulator()

# ============================================================
# Load graders eagerly at startup so the validator can call them
# ============================================================
TASK_GRADERS = {}
TASKS_CONFIG = [
    {
        "id": "task_1",
        "name": "Easy Syntax Error Fix",
        "description": "Solve the AST syntax issue dynamically.",
        "difficulty": "easy",
        "grader": "tasks.task_1.grader:grade",
    },
    {
        "id": "task_2",
        "name": "Medium Dependency Mismatch Fix",
        "description": "Upgrade missing pipeline requirements.",
        "difficulty": "medium",
        "grader": "tasks.task_2.grader:grade",
    },
    {
        "id": "task_3",
        "name": "Hard Regression Logic Fix",
        "description": "Repair the destructive PR logic.",
        "difficulty": "hard",
        "grader": "tasks.task_3.grader:grade",
    },
]

for task_cfg in TASKS_CONFIG:
    grader_path = task_cfg["grader"]
    module_path, func_name = grader_path.split(":")
    try:
        mod = importlib.import_module(module_path)
        grader_fn = getattr(mod, func_name)
        TASK_GRADERS[task_cfg["id"]] = grader_fn
        logger.info(f"Loaded grader for {task_cfg['id']}: {grader_path}")
    except Exception as e:
        logger.error(f"Failed to load grader for {task_cfg['id']}: {e}")


# ============================================================
# Pydantic models
# ============================================================
class StepResponse(BaseModel):
    observation: DevOpsObservation
    reward: float
    done: bool
    info: dict

class GradeRequest(BaseModel):
    task_id: str
    action_type: str = "analyze"
    file_path: str = ""
    patch_content: str = ""


# ============================================================
# OpenEnv REQUIRED Endpoints (core protocol)
# ============================================================
@app.get("/")
async def root():
    return {"status": "online", "message": "GitHub Agent OpenEnv Environment is live and verified."}

@app.get("/health")
async def health():
    """Required by OpenEnv runtime validation."""
    return {"status": "healthy"}

@app.get("/metadata")
async def metadata():
    """Required by OpenEnv runtime validation — returns name + description."""
    return {
        "name": "AI_DevOps_Agent",
        "description": "Autonomous CI/CD Fixer Agent that repairs regressions and submits Pull Requests.",
        "version": "1.0.0",
        "tasks_count": len(TASKS_CONFIG),
        "tasks_with_graders": len(TASK_GRADERS),
    }

@app.get("/schema")
async def schema():
    """Required by OpenEnv runtime validation — returns action, observation, state schemas."""
    return {
        "action": {
            "type": "object",
            "properties": {
                "action_type": {"type": "string", "description": "Type of action: 'analyze' or 'patch'"},
                "file_path": {"type": "string", "description": "Target file path (optional)"},
                "patch_content": {"type": "string", "description": "Patch content (optional)"},
            },
            "required": ["action_type"],
        },
        "observation": {
            "type": "object",
            "properties": {
                "system_state": {"type": "string"},
                "ci_logs": {"type": "string"},
                "target_files": {"type": "array", "items": {"type": "string"}},
            },
        },
        "state": {
            "type": "object",
            "properties": {
                "episode_id": {"type": "string"},
                "step_count": {"type": "integer"},
                "current_task": {"type": "string"},
            },
        },
    }


# ============================================================
# Core RL Endpoints: /reset, /step, /state
# ============================================================
@app.post("/reset", response_model=DevOpsObservation)
async def reset():
    return await simulator.reset()

@app.post("/step", response_model=StepResponse)
async def step(action: DevOpsAction):
    obs, reward, done, err = await simulator.step(action)
    info = {"status": "ok"}
    if err:
        info["last_action_error"] = err
    return StepResponse(observation=obs, reward=reward, done=done, info=info)

@app.get("/state", response_model=DevOpsObservation)
async def state():
    return await simulator.state()


# ============================================================
# Tasks & Graders Endpoints (hackathon validation)
# ============================================================
@app.get("/tasks")
def get_tasks():
    """Return all tasks with their grader info. Validator checks this."""
    tasks_list = []
    for task_cfg in TASKS_CONFIG:
        task_id = task_cfg["id"]
        grader_fn = TASK_GRADERS.get(task_id)

        # Actually call the grader to prove it works
        grader_score = None
        if grader_fn:
            try:
                grader_score = float(grader_fn(action_type="analyze"))
            except Exception:
                grader_score = None

        tasks_list.append({
            "id": task_id,
            "name": task_cfg["name"],
            "description": task_cfg["description"],
            "difficulty": task_cfg["difficulty"],
            "grader": task_cfg["grader"],
            "grader_callable": grader_fn is not None,
            "grader_score": grader_score,
        })

    return {"tasks": tasks_list}

@app.post("/grade")
def grade_task(req: GradeRequest):
    """Endpoint to invoke a grader directly — validator may use this."""
    grader_fn = TASK_GRADERS.get(req.task_id)
    if not grader_fn:
        return {"error": f"No grader found for {req.task_id}", "score": None}

    score = float(grader_fn(
        action_type=req.action_type,
        file_path=req.file_path,
        patch_content=req.patch_content,
    ))
    return {"task_id": req.task_id, "score": score, "grader_callable": True}

@app.post("/baseline")
async def baseline():
    """Run baseline graders for all tasks."""
    scores = []
    for task_cfg in TASKS_CONFIG:
        grader_fn = TASK_GRADERS.get(task_cfg["id"])
        if grader_fn:
            score = float(grader_fn(action_type="analyze"))
            scores.append(score)
        else:
            scores.append(0.1)
    return {"status": "success", "message": "Baseline executed.", "scores": scores}


# ============================================================
# Legacy webhooks
# ============================================================
try:
    from routes.webhooks import router as webhook_router
    app.include_router(webhook_router, prefix="/api/v1")
except Exception:
    pass


def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
