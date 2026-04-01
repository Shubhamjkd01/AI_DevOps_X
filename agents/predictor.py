import logging
from services.llm import query_llm
from learning.episodic_memory import get_similar_patches, PRE_WARMED_CONTEXT

logger = logging.getLogger(__name__)

def predict_failure(commit_diff: str, commit_sha: str = "mock_commit_sha") -> dict:
    """
    Killer Feature: Predicts if a commit will fail CI before it even runs.
    """
    logger.info("Predictor Agent: Analyzing commit patterns for failure prediction...")
    prompt = f"""Predictor Agent: You are analyzing a git commit diff BEFORE it runs in CI/CD. 
Look for common issues that break builds (missing dependencies, syntax errors, mismatched versions).
Return your response formatted exactly like this:
Prediction: [Safe / High Risk]
Reason: [Your explanation of risk]
Confidence: [0-100]%

Here is the diff:
{commit_diff}
"""
    response = query_llm(prompt)
    logger.info(f"Predictor Agent Output: {response}")
    
    is_risk = "High Risk" in response
    
    if is_risk:
        logger.info(f"Predictor Agent: High Risk detected. Executing Predictive Pre-warming for {commit_sha}...")
        # Since we don't know the exact error yet, we embed the diff to find structurally similar past failures!
        similar = get_similar_patches(commit_diff, top_k=3)
        PRE_WARMED_CONTEXT[commit_sha] = similar
        logger.info(f"Predictor Agent: Pre-warmed {len(similar)} historical patches into Operational Memory.")

    return {
        "prediction": "High Risk" if is_risk else "Safe",
        "reason": response,
        "raw_response": response
    }
