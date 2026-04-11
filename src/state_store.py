import json
from pathlib import Path

def load_state(path: str):
    p = Path(path)
    if not p.exists():
        return {"systems": {}}

    with open(p, "r") as f:
        return json.load(f)

def save_state(path: str, state: dict):
    with open(path, "w") as f:
        json.dump(state, f, indent=2)