"""
Task 2 Grader: Medium Dependency Mismatch Fix
Evaluates whether the agent resolved dependency version conflicts in requirements.txt.
"""


def grade(*args, **kwargs) -> float:
    """
    OpenEnv-compliant grader function for Task 2.
    Returns a float score strictly between 0 and 1.
    """
    action_type = kwargs.get("action_type", "analyze")
    file_path = kwargs.get("file_path", "")
    patch = kwargs.get("patch_content", "")

    score = 0.1

    if action_type == "analyze":
        return 0.25

    if action_type == "patch":
        if file_path == "requirements.txt":
            score += 0.35
        if "==" in patch or "streamlit" in patch:
            score += 0.45

    # Strictly clamp to (0, 1) exclusive — never return 0.0 or 1.0
    return float(min(0.99, max(0.1, score)))
