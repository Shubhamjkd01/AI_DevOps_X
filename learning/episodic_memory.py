import os
import json
import logging
import math
import numpy as np
import faiss
from services.llm import get_embedding

logger = logging.getLogger(__name__)

KNOWLEDGE_BASE_FILE = "c:/AI_DeVops/github_agent_backend/episodic_patch_memory.json"
PRE_WARMED_CONTEXT = {}

# Global FAISS index and metadata
index = None
metadata = []

def load_knowledge_base():
    global index, metadata
    if not os.path.exists(KNOWLEDGE_BASE_FILE):
        metadata = []
        index = faiss.IndexFlatL2(768)
        return
        
    try:
        with open(KNOWLEDGE_BASE_FILE, "r") as f:
            metadata = json.load(f)
            
        index = faiss.IndexFlatL2(768)
        if metadata:
            embeddings = np.array([m["error_embedding"] for m in metadata], dtype=np.float32)
            index.add(embeddings)
    except Exception as e:
        logger.error(f"Error loading FAISS knowledge base: {e}")
        metadata = []
        index = faiss.IndexFlatL2(768)

load_knowledge_base()

def get_similar_patches(error_text: str, top_k=3, failure_category: str = None):
    """
    Retrieval-augmented operational memory using FAISS vector database.
    """
    if index is None or index.ntotal == 0:
        return []
        
    current_emb = np.array([get_embedding(error_text)], dtype=np.float32)
    # L2 distance gives ascending order for closest match
    distances, indices = index.search(current_emb, top_k * 2) # Pull extra to filter by category if needed
    
    ranked = []
    for i, idx in enumerate(indices[0]):
        if idx == -1: 
            continue
        # Convert L2 distance to a pseudo-confidence score (0 to 1) for UI compatibility
        sim = 1.0 / (1.0 + distances[0][i])
        entry = metadata[idx]
        
        # Category Filter Match - Boosts Score
        if failure_category and entry.get("failure_category") == failure_category:
            sim += 0.2
            
        if (sim, entry) not in ranked:
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
    return conf, f"based on {successes}/{total} similar past patches passing validation from FAISS DB"

def update_patch_reward(pr_url: str, reward: float):
    global index, metadata
    updated = False
    for entry in metadata:
        if entry.get("pr_url") == pr_url:
            entry["reward"] = reward
            entry["accepted"] = reward > 0.0
            updated = True
            break
            
    if updated:
        with open(KNOWLEDGE_BASE_FILE, "w") as f:
            json.dump(metadata, f, indent=4)
        logger.info(f"Human Feedback: Updated PR {pr_url} reward to {reward} in FAISS memory.")

def penalize_latest_patch():
    global metadata
    if metadata:
        metadata[-1]["reward"] = -1.0
        metadata[-1]["accepted"] = False
        with open(KNOWLEDGE_BASE_FILE, "w") as f:
            json.dump(metadata, f, indent=4)
        logger.info("Rollback Agent: Penalized the most recent AI patch in FAISS memory.")

def save_patch_memory(error: str, patch: str, reward: float = 1.0, failure_category: str = "Unknown", pr_url: str = ""):
    global index, metadata
    emb = get_embedding(error)
    
    entry = {
        "error": error,
        "error_embedding": emb,
        "patch": patch,
        "reward": reward,
        "accepted": reward > 0.0,
        "failure_category": failure_category,
        "pr_url": pr_url
    }
    
    metadata.append(entry)
    index.add(np.array([emb], dtype=np.float32))
    
    with open(KNOWLEDGE_BASE_FILE, "w") as f:
        json.dump(metadata, f, indent=4)
        
    logger.info("Episodic Memory: Saved patch mapping to FAISS vector operational memory.")

def get_memory_hit_rate() -> float:
    if not metadata: return 0.0
    hits = sum(1 for m in metadata if m.get("accepted", False))
    return (hits / len(metadata)) * 100.0
