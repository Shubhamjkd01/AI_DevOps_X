def get_vec(t):
    """
    Deterministic mock embedding as required by the OpenEnv Hackathon benchmark
    to avoid proxy-based embedding latency or failure.
    """
    import hashlib
    # Create a deterministic mock vector based on the hash of the error string
    h = hashlib.sha256(t.encode()).hexdigest()
    vec = [(int(h[i:i+2], 16) / 255.0) - 0.5 for i in range(0, 64, 2)]
    # Pad to 768 dimensions as expected by FAISS
    return vec + [0.0] * (768 - len(vec))

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
