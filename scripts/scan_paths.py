import os
import re

base = r"c:\AI_DeVops\github_agent_backend"
drive_re = re.compile(r"\b[A-Za-z]:[\\/][^\s'\">]+", re.IGNORECASE)

found = {}
for root, dirs, files in os.walk(base):
    if any(x in root for x in [".git", "__pycache__", ".venv", "scripts"]):
        continue
    for f in files:
        if f.endswith(".py"):
            p = os.path.join(root, f)
            try:
                lines = open(p, encoding="utf-8", errors="ignore").readlines()
                for idx, line in enumerate(lines):
                    # Exclude http:// or https://
                    clean_line = re.sub(r'https?://[^\s]+', '', line)
                    matches = drive_re.findall(clean_line)
                    if matches:
                        rel = os.path.relpath(p, base)
                        if rel not in found:
                            found[rel] = []
                        found[rel].append((idx + 1, matches, line.strip()))
            except Exception as e:
                pass

for k, v in found.items():
    print(f"=== {k} ===")
    for line_no, m, full in v:
        print(f"  L{line_no}: {m} -> {full.encode('ascii', 'replace').decode('ascii')}")
