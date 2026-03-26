import os
import json
import logging
import math
from services.llm import get_embedding

logger = logging.getLogger(__name__)

KNOWLEDGE_BASE_FILE = "c:/AI_DeVops/github_agent_backend/episodic_patch_memory.json"
PRE_WARMED_CONTEXT = {}

def get_knowledge_base():
    if not os.path.exists(KNOWLEDGE_BASE_FILE):
        return []
    try:
        with open(KNOWLEDGE_BASE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def cosine_similarity(v1, v2):
    if not v1 or not v2 or len(v1) != len(v2): return 0.0
    dot = sum(x*y for x, y in zip(v1, v2))
    mag1 = math.sqrt(sum(x*x for x in v1))
    mag2 = math.sqrt(sum(x*x for x in v2))
    if mag1 == 0 or mag2 == 0: return 0.0
    return dot / (mag1 * mag2)

def get_similar_patches(error_text: str, top_k=3):
    """
    Retrieval-augmented operational memory using cosine similarity over error embeddings.
    """
    kb = get_knowledge_base()
    if not kb: return []
    
    current_emb = get_embedding(error_text)
    ranked = []
    for entry in kb:
        sim = cosine_similarity(current_emb, entry.get("error_embedding", []))
        ranked.append((sim, entry))
        
    ranked.sort(key=lambda x: x[0], reverse=True)
    return ranked[:top_k]

def calculate_confidence(error_text: str) -> tuple[float, str]:
    """
    confidence = successful_similar_patches / total_similar_patches
    """
    similar = get_similar_patches(error_text, top_k=5)
    if not similar:
        return 0.5, "based on 0 similar past patches (first encounter)"
        
    total = len(similar)
    successes = sum(1 for sim, entry in similar if entry.get("accepted", False))
    conf = successes / total
    return conf, f"based on {successes}/{total} similar past patches passing validation"

def save_patch_memory(error: str, patch: str, reward: float = 1.0):
    kb = get_knowledge_base()
    emb = get_embedding(error)
    kb.append({
        "error": error,
        "error_embedding": emb,
        "patch": patch,
        "reward": reward,
        "accepted": reward > 0.0
    })
    with open(KNOWLEDGE_BASE_FILE, "w") as f:
        json.dump(kb, f)
    logger.info("Episodic Memory: Saved patch mapping to operational memory.")
