#!/usr/bin/env python3
"""Parse build.yaml include entries and output JSON array to stdout."""
import json
import sys

with open("build.yaml") as f:
    lines = f.readlines()

entries = []
cur = None

for line in lines:
    s = line.rstrip("\n")
    stripped = s.strip()
    if not stripped or stripped.startswith("#"):
        continue
    if stripped in ("include:", "---"):
        continue
    if stripped.startswith("- "):
        if cur is not None:
            entries.append(cur)
        cur = {}
        rest = stripped[2:].strip()
        if ":" in rest:
            k, v = rest.split(":", 1)
            cur[k.strip()] = v.strip()
    elif cur is not None and ":" in stripped:
        k, v = stripped.split(":", 1)
        cur[k.strip()] = v.strip()

if cur:
    entries.append(cur)

json.dump(entries, sys.stdout)
