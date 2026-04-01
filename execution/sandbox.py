import logging
import py_compile
import tempfile
import os

logger = logging.getLogger(__name__)

def run_in_sandbox(file_path: str, content: str) -> bool:
    """
    Validates the fix by compiling it with Python's py_compile.
    """
    logger.info(f"Sandbox: Validating syntax for {file_path}")
    
    if not content.strip():
        logger.error("Sandbox: Validation failed! LLM returned empty content.")
        return False
        
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
        f.write(content.encode('utf-8'))
        temp_path = f.name
        
    logger.info(f"Sandbox DEBUG Code payload to compile:\n---\n{content}\n---")
    try:
        py_compile.compile(temp_path, doraise=True)
        logger.info("Sandbox: Validation passed. Code is syntactically correct.")
        return True
    except py_compile.PyCompileError as e:
        logger.error(f"Sandbox: Validation failed! Syntax error in LLM output: {e}")
        return False
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

