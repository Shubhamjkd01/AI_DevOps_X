import json
import os
import logging

logger = logging.getLogger(__name__)

MASTERY_FILE = "c:/AI_DeVops/github_agent_backend/mastery_scores.json"

class CurriculumController:
    def __init__(self):
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(MASTERY_FILE):
            default_scores = {
                "syntax": 0.0,
                "dependency": 0.0,
                "env": 0.0,
                "architectural": 0.0,
                "test": 0.0
            }
            with open(MASTERY_FILE, "w") as f:
                json.dump(default_scores, f, indent=4)

    def _read_scores(self) -> dict:
        try:
            with open(MASTERY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def _write_scores(self, scores: dict):
        with open(MASTERY_FILE, "w") as f:
            json.dump(scores, f, indent=4)

    def update_mastery(self, category: str, success: bool):
        scores = self._read_scores()
        
        # Default to a generic category if unmapped
        if category not in scores:
            scores[category] = 0.0
            
        current = scores[category]
        if success:
            current += 0.1
        else:
            current -= 0.05
            
        # Clamp between 0.0 and 1.0
        current = max(0.0, min(1.0, current))
        scores[category] = round(current, 3)
        
        self._write_scores(scores)
        logger.info(f"Curriculum: Updated mastery for {category} to {current}")

    def get_raw_score(self, category: str) -> float:
        scores = self._read_scores()
        return scores.get(category, 0.0)

    def get_difficulty(self, category: str) -> str:
        scores = self._read_scores()
        score = scores.get(category, 0.0)
        
        if score <= 0.2:
            return "warmup (single simple errors)"
        elif score <= 0.4:
            return "beginner (single errors with noise)"
        elif score <= 0.6:
            return "intermediate (two simultaneous errors)"
        elif score <= 0.8:
            return "advanced (compound errors plus red herrings)"
        else:
            return "expert (cascading failures across multiple files)"
