from services.llm import query_llm
from learning.episodic_memory import get_similar_patches, calculate_confidence, PRE_WARMED_CONTEXT
import logging
import re

logger = logging.getLogger(__name__)

def generate_fix(analysis: dict, repo_full_name: str) -> dict:
    """
    Generates a patch-based code fix utilizing RL memory and Repo Context.
    """
    logger.info("Fix Generator Agent: Generating patch-based fix...")
    
    logger.info("Fix Generator Agent: Fetching Episodic Patch Memory Context...")
    current_commit = "mock_commit_sha" # Passed from orchestrator theoretically
    if current_commit in PRE_WARMED_CONTEXT:
        similar_fixes = PRE_WARMED_CONTEXT[current_commit]
        logger.info("Predictive Pre-Warming: Cache Hit! Using pre-warmed context.")
    else:
        similar_fixes = get_similar_patches(analysis['error'], top_k=3)
        
    episodic_context = ""
    if similar_fixes:
        episodic_context = "\n[EPISODIC PATCH MEMORY: We use cosine similarity to retrieve past successful patches!]\n"
        for sim_score, fix in similar_fixes:
            episodic_context += f"Confidence Score: {sim_score:.2f} | Error: {fix.get('error','')}\nPatch: {fix.get('patch','')}\n---\n"

    logger.info("Fix Generator Agent: Fetching Repo Context Engine data...")
    from services.github import get_file_content
    file_path = analysis.get("file_path", "main.py")
    current_code = get_file_content(repo_full_name, file_path)
    
    repo_context = f"\n[REPO CONTEXT]: Architecting patch for {repo_full_name}. File executing on: {file_path}.\n[CURRENT FILE SOURCE CODE:]\n{current_code}\n[END SOURCE CODE]\n"
    
    prompt = f"""Fix Generator Agent: {episodic_context} {repo_context}
Root Error: {analysis['error']}
Why: {analysis['why']}

Generate a safe, patch-based fix. You must generate BOTH a unified Git diff (for the reviewer to see) AND the completely rewritten full file codebase (for the system to securely overwrite the file on GitHub).
Return your response formatted exactly like this:
Patch:
[your patch diff here]
Explanation: [Why this patch safely solves the problem]
Full Code:
[the entire modified file code with no markup]
Confidence: 0.XX
"""
    fix_content = query_llm(prompt)
    
    # Real Confidence Calculation using Cosine Similarity Vectors
    conf_value, conf_reason = calculate_confidence(analysis['error'])
        
    match_exp = re.search(r"Explanation:\s*(.*)(?:\n|$)", fix_content, re.IGNORECASE)
    explanation = match_exp.group(1) if match_exp else analysis.get('why', 'Applied safe patch-based fix based on context.')
    explanation += f"\n\nReal Confidence Math: {conf_reason}"
    confidence = conf_value

    patch_clean = fix_content
    if "Patch:" in fix_content:
        patch_clean = fix_content.split("Patch:")[1].split("Explanation:")[0].strip()
        
    full_code = fix_content
    if "Full Code:" in fix_content:
        full_code = fix_content.split("Full Code:")[1].strip()
        full_code = full_code.replace("```python", "").replace("```", "").strip()

    fix_data = {
        "file_path": file_path,
        "content": full_code, # Sent to GitHub wrapper to physically overwrite the branch file
        "patch_diff": patch_clean, # Handed to PR Agent for reviewer presentation
        "explanation": explanation,
        "confidence": confidence,
        "conf_reason": conf_reason,
        "priority": analysis.get("priority", "HIGH")
    }
    logger.info(f"Fix Generator Agent Output: Patch generated with {confidence*100}% confidence.")
    return fix_data
