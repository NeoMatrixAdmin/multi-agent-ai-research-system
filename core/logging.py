import json
from datetime import datetime

def log_artifact(name: str, data: dict):
    ts = datetime.utcnow().isoformat()
    with open(f"outputs/logs/{name}_{ts}.json", "w") as f:
        json.dump(data, f, indent=2)
