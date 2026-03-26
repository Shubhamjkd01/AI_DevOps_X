import logging
import json
from services.llm import query_llm

logger = logging.getLogger(__name__)

def analyze_logs(logs: str) -> dict:
    """
    Analyzes the CI logs to find the prioritized root cause of the failure.
    """
    logger.info("Analyzer Agent: Scanning logs for priority errors...")
    
    prompt = f"""Analyzer Agent: Analyze these CI/CD logs: {logs}
Identify the main error and prioritize it.
Return ONLY a valid JSON object with EXACTLY these keys:
"priority": "HIGH", "MEDIUM", or "LOW"
"confidence": (float 0.0 to 1.0)
"file_path": "path/to/the/problematic/file.py"
"error": "Short description of the error"
"why": "Deep technical explanation of why this error occurred"
"""
    response = query_llm(prompt)
    
    try:
        cleaned = response.replace("```json", "").replace("```", "").strip()
        analysis = json.loads(cleaned)
    except Exception as e:
        logger.error("Failed to parse Analyzer JSON. Fallback active.")
        analysis = {
            "priority": "HIGH",
            "confidence": 0.90,
            "file_path": "main.py",
            "error": "Pipeline execution failed",
            "why": "Fallback triggered due to unparseable logs"
        }
        
    logger.info(f"Analyzer Agent Output: [Priority: {analysis['priority']}] Confidence {analysis['confidence']} - {analysis['error']}")
    return analysis
