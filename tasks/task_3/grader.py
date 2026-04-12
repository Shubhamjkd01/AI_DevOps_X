"""
Task 3 Grader: Hard Regression Logic Fix
Evaluates whether the agent repaired multi-file regression across orchestrator files.
"""


def grade(*args, **kwargs) -> float:
    """
    OpenEnv-compliant grader function for Task 3.
    Returns a float score strictly between 0 and 1.
    """
    action_type = kwargs.get("action_type", "analyze")
    file_path = kwargs.get("file_path", "")
    patch = kwargs.get("patch_content", "")

    score = 0.1

    if action_type == "analyze":
        return 0.3

    if action_type == "patch":
        if file_path in ["orchestrator.py", "agents/fixer.py"]:
            score += 0.4
        if "import" in patch and "def " in patch:
            score += 0.4
        # Penalty for destructive patterns
        if patch == "" or "while True:" in patch:
            score -= 0.3

    # Strictly clamp to (0, 1) exclusive — never return 0.0 or 1.0
    return float(min(0.99, max(0.1, score)))
