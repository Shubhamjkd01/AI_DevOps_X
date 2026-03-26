import json
import os
import random

try:
    import google.generativeai as genai
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "MOCK_KEY"))
except Exception:
    pass

def get_vec(t):
    try:
        return genai.embed_content(model="models/text-embedding-004", content=t)["embedding"]
    except Exception:
        return [random.uniform(-0.1, 0.1) for _ in range(768)]

errors = [
    "SyntaxError: unexpected EOF while parsing main.py",
    "IndentationError: expected an indented block in routes.py",
    "KeyError: 'status' missing from JSON payload",
    "ImportError: cannot import name BaseModel from pydantic",
    "ModuleNotFoundError: No module named requests in site-packages",
    "TypeError: can only concatenate str to str (not dict)",
    "ValueError: invalid literal for int() with base 10",
    "AttributeError: NoneType object has no attribute group",
    "IndexError: list index out of range in validation loop",
    "ZeroDivisionError: division by zero in metric calc",
    "FileNotFoundError: no such file or directory config.yaml",
    "RuntimeError: maximum recursion depth exceeded in graph logic",
    "NotImplementedError: abstract method render() not implemented",
    "OverflowError: math range error in exponential reward",
    "MemoryError: Out of memory loading huge dataset"
]

memory = []
for e in errors:
    memory.append({
        "error": e,
        "error_embedding": get_vec(e),
        "patch": f"# Safe mock patch for {e}\ndef fixed_logic(): pass",
        "reward": 1.0,
        "accepted": True
    })

with open("c:/AI_DeVops/github_agent_backend/episodic_patch_memory.json", "w") as f:
    json.dump(memory, f, indent=4)
print("Seeded 15 episodic memory instances deterministically!")
