"""
Task 1 Grader: Easy Syntax Error Fix
Evaluates whether the agent correctly identified and patched a Python syntax error.
"""


def grade(*args, **kwargs) -> float:
    """
    OpenEnv-compliant grader function for Task 1.
    Returns a float score strictly between 0 and 1.
    """
    action_type = kwargs.get("action_type", "analyze")
    file_path = kwargs.get("file_path", "")
    patch = kwargs.get("patch_content", "")

    score = 0.1

    if action_type == "analyze":
        return 0.2

    if action_type == "patch":
        if file_path == "main.py":
            score += 0.4
        if ":" in patch or "SyntaxError" not in patch:
            score += 0.4

    # Strictly clamp to (0, 1) exclusive — never return 0.0 or 1.0
    return float(min(0.99, max(0.1, score)))
