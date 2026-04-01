from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Ensure root paths load for modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import DevOpsAction, DevOpsObservation
from server.environment import EnvironmentSimulator
import uvicorn

app = FastAPI(title="GitHub Agent Environment - OpenEnv Server")
simulator = EnvironmentSimulator()

class StepResponse(BaseModel):
    observation: DevOpsObservation
    reward: float
    done: bool
    info: dict

@app.get("/")
async def root():
    return {"status": "online", "message": "GitHub Agent OpenEnv Environment is live and verified."}

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

# Legacy webhooks
try:
    from routes.webhooks import router as webhook_router
    app.include_router(webhook_router, prefix="/api/v1")
except Exception:
    pass

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)
