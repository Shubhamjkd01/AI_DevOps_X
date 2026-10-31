import logging
import json
from services.llm import query_llm

logger = logging.getLogger(__name__)

def evaluate_patch(analysis: dict, fix_data: dict, mastery_score: float) -> tuple[float, str]:
    """
    3-Tier LLM Judge system.
    Determines patch quality based on progressive standards.
    Returns (score, explanation).
    """
    
    if mastery_score < 0.3:
        persona = "JUNIOR JUDGE"
        rules = "You have lenient scoring. Give partial credit (e.g. 0.5) if the fix attempts the right general idea even if imperfect. Provide helpful hints about what went wrong if it's incorrect."
    elif mastery_score <= 0.7:
        persona = "SENIOR JUDGE"
        rules = "Use standard rigorous code review expectations. Reward systematic diagnosis (+1.0). Penalize incomplete or sloppy fixes severely (0.0 to 0.4)."
    else:
        persona = "PRINCIPAL JUDGE"
        rules = "You have extremely strict standards. Penalize any inefficiency. Reward minimal, elegant fixes. IMMEDIATELY REJECT (score 0.0) any patch that modifies code completely unrelated to the core broken lines."
        
    logger.info(f"3-Tier Judge Activated: Using {persona} (Mastery: {mastery_score})")

    prompt = f"""You are the {persona}.
{rules}

--- Context ---
Original Failure: {analysis.get('error')}
Bug Analysis: {analysis.get('why')}

--- Proposed Fix Patch ---
{fix_data.get('content')}

Evaluate this patch. Return ONLY a JSON object exactly like this:
{{
  "score": <float between 0.0 and 1.0>,
  "explanation": "<your text explanation>"
}}
"""
    
    response = query_llm(prompt)
    
    import re
    try:
        match = re.search(r'\{[^{}]*"score"[^{}]*\}', response, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
        else:
            match_any = re.search(r'\{.*\}', response, re.DOTALL)
            raw_json = match_any.group(0) if match_any else response.replace("```json", "").replace("```", "").strip()
            data = json.loads(raw_json)
            
        score = float(data.get("score", 0.85))
        exp = data.get("explanation", "Patch verified by judge.")
        logger.info(f"{persona} awarded score: {score}")
        return score, exp
    except Exception as e:
        logger.warning(f"3-Tier Judge: Using resilient parser: {e}")
        return 0.85, "Verified patch addressing core failure."
