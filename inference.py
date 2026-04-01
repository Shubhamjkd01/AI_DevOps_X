import asyncio
import os
import textwrap
from typing import List, Optional

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)
from client import GitHubAgentEnv, DevOpsAction

IMAGE_NAME = os.getenv("IMAGE_NAME") # If you are using docker image 
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
TASK_NAME = os.getenv("GITHUB_AGENT_TASK", "fix_ci_workflow")
BENCHMARK = os.getenv("GITHUB_AGENT_BENCHMARK", "devops_eval")
MAX_STEPS = 5
TEMPERATURE = 0.7
MAX_TOKENS = 512
SUCCESS_SCORE_THRESHOLD = 0.5

SYSTEM_PROMPT = textwrap.dedent(
    """
    You are an autonomous AI software engineer fixing CI/CD pipelines.
    You will be given the system state and the CI traceback logs.
    Your goal is to propose an exact code patch to fix the error.
    Return ONLY a JSON object representing your action in the exact format:
    {"action_type": "patch", "file_path": "<target_file>", "patch_content": "<corrected_code>"}
    """
).strip()


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


def build_user_prompt(step: int, ci_logs: str, last_reward: float) -> str:
    return textwrap.dedent(
        f"""
        Step: {step}
        Last reward: {last_reward:.2f}
        CI Traceback Logs:
        {ci_logs}
        
        Generate your JSON action.
        """
    ).strip()


def get_model_action(client: OpenAI, step: int, ci_logs: str, last_reward: float) -> DevOpsAction:
    user_prompt = build_user_prompt(step, ci_logs, last_reward)
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False,
        )
        text = (completion.choices[0].message.content or "").strip()
        import json
        clean_json = text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        return DevOpsAction(**data)
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return DevOpsAction(action_type="analyze", file_path="main.py", patch_content="")


async def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    env = await GitHubAgentEnv.from_docker_image(IMAGE_NAME)

    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        result = await env.reset()
        last_logs = result.observation.ci_logs
        last_reward = 0.0

        for step in range(1, MAX_STEPS + 1):
            if result.done:
                break

            action = get_model_action(client, step, last_logs, last_reward)
            
            # Action string without line breaks for correct parsing
            action_str = f"patch('{action.file_path}')" if action.action_type == "patch" else "analyze_env()"

            # Evaluate step execution
            result = await env.step(action)
            obs = result.observation
            reward = result.reward or 0.0
            done = result.done
            
            error = result.info.get("last_action_error")

            rewards.append(reward)
            steps_taken = step
            last_logs = obs.ci_logs
            last_reward = reward

            log_step(step=step, action=action_str, reward=reward, done=done, error=error)

            if done:
                break

        # Max total score possible logic
        score = sum(rewards) / len(rewards) if rewards else 0.0
        score = min(max(score, 0.0), 1.0)
        success = score >= SUCCESS_SCORE_THRESHOLD

    finally:
        try:
            await env.close()
        except Exception as e:
            print(f"[DEBUG] env.close() error: {e}", flush=True)
            
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    asyncio.run(main())
