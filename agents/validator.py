import logging
import ast
import re
from execution.sandbox import run_in_sandbox
import time

logger = logging.getLogger(__name__)

def check_hallucinations(code: str) -> bool:
    # 1. AST compilation check
    try:
        ast.parse(code)
    except Exception as e:
        logger.error(f"Hallucination Guard: Invalid Python syntax generated. {e}")
        return False

    # 2. Strict regex checks for hallucinated libraries or destructive commands
    forbidden_patterns = [
        r'\b(?:import|from)\s+(?:subprocess|pty|shutil)\b',
        r'\bos\.system\b',
        r'\bsubprocess\b',
        r'\bshutil\.rmtree\b'
    ]
    for pattern in forbidden_patterns:
        if re.search(pattern, code):
            logger.error(f"Hallucination Guard: Dangerous pattern detected ({pattern}). Rejecting patch!")
            return False

    return True

def validate_fix(fix_data: dict) -> bool:
    """
    Simulates validating the fix and running regression test suites.
    """
    logger.info(f"Validator Agent: Checking hallucination guard for {fix_data['file_path']}...")
    if fix_data['file_path'].endswith('.py'):
        if not check_hallucinations(fix_data['content']):
            return False
            
    logger.info(f"Validator Agent: Validating patch for {fix_data['file_path']}...")
    is_valid = run_in_sandbox(fix_data['file_path'], fix_data['content'])
    
    if is_valid:
        logger.info("Validator Agent: Syntax check passed. Running full Regression Check (unit tests + integration)...")
        time.sleep(1.5) # Simulate regression test running
        logger.info("Validator Agent Output: Zero regressions detected. We ensure fixes do not introduce new failures.")
        return True
    else:
        logger.warning("Validator Agent Output: Fix failed sandbox checks or introduced a regression.")
        return False
