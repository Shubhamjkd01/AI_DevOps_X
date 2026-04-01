import json
import os
import logging
from services.llm import query_llm

logger = logging.getLogger(__name__)

MASTERY_FILE = "c:/AI_DeVops/github_agent_backend/mastery_scores.json"

def get_weakest_category() -> str:
    default_scores = {
        "syntax": 0.0,
        "dependency": 0.0,
        "env": 0.0,
        "architectural": 0.0,
        "test": 0.0
    }
    
    if not os.path.exists(MASTERY_FILE):
        with open(MASTERY_FILE, "w") as f:
            json.dump(default_scores, f, indent=4)
        scores = default_scores
    else:
        try:
            with open(MASTERY_FILE, "r") as f:
                scores = json.load(f)
        except Exception:
            scores = default_scores
            
    # Find the category with the minimum score
    weakest = min(scores, key=scores.get)
    logger.info(f"Adversarial Designer: Identified weakest mastery category as '{weakest}' (Score: {scores[weakest]})")
    return weakest

def generate_scenarios():
    """
    Runs automatically every 10 training episodes.
    Uses LLM to generate 3 compound failure scenarios targeting the weakest category.
    """
    weakest_category = get_weakest_category()
    
    prompt = f"""You are an Adversarial Scenario Generator acting as Claude in a Red-Team testing loop.
My CI fixing system tracks success rates across categories. The current weakest category is: {weakest_category.upper()}.

Task: Generate 3 new compound failure scenarios for this category.
A compound scenario MUST contain TWO simultaneous failures (e.g., an IndentationError AND a missing dependency).
You MUST also include red herrings — fake error messages or stack traces that look like genuine failures but are actually harmless noise, to test the agent's diagnosis ability.

Format your output strictly as a JSON list of objects:
[
  {{
    "title": "Scenario 1",
    "description": "...",
    "primary_failure": "...",
    "secondary_failure": "...",
    "red_herring": "...",
    "mock_logs": "..."
  }}
]
"""
    logger.info(f"Adversarial Designer: Requesting 3 compound adversarial scenarios for {weakest_category} from LLM...")
    response_text = query_llm(prompt)
    
    # Strip markup if present
    response_text = response_text.replace("```json", "").replace("```", "").strip()
    
    try:
        scenarios = json.loads(response_text)
        logger.info(f"Adversarial Designer: Successfully generated {len(scenarios)} compound adversarial scenarios.")
        
        # Save them to an adversarial queue file
        queue_file = "c:/AI_DeVops/github_agent_backend/adversarial_queue.json"
        
        queue = []
        if os.path.exists(queue_file):
            with open(queue_file, "r") as f:
                try:
                    queue = json.load(f)
                except:
                    pass
        
        queue.extend(scenarios)
        
        with open(queue_file, "w") as f:
            json.dump(queue, f, indent=4)
            
        logger.info("Adversarial Designer: Appended new scenarios to adversarial_queue.json")
    except Exception as e:
        logger.error(f"Adversarial Designer: Failed to parse generated scenarios. {e}")
        logger.debug(f"Raw Output: {response_text}")
